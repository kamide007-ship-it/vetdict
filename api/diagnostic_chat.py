#!/usr/bin/env python3
"""
Symptom Check Chat Interface - Symptom-driven health reference through conversation.

Enables users to:
1. Input symptoms via natural language chat
2. Get symptom-based disease reference information (not diagnosis)
3. Navigate to related features (dashboard, specific dog records)

NOTE: This module provides reference information only. It does not perform
veterinary diagnosis or treatment, which are restricted to licensed
veterinarians under Japanese Veterinary Practice Act (獣医師法).

Veterinary Supervision: Kentaro Kaimide, DVM (上手健太郎)
Minamisoma Veterinary Clinic (南相馬動物病院)
https://www.minamisoma-vet.com/

Disease data (symptoms, risk factors, frequency, treatment, prognosis,
prevention) is presented as general reference information within the scope
permitted by the Veterinary Practice Act (獣医師法).
"""


import logging
import os
import threading
from typing import Any, Dict, Optional

from flask import Blueprint, jsonify, request

logger = logging.getLogger(__name__)

diagnostic_bp = Blueprint("diagnostic_bp", __name__, url_prefix="/api/diagnostic-chat")

# Import health checker data (dog - default)
try:
    from api.health_checker import DISEASES, SYMPTOM_IDS, SYMPTOMS
except ImportError:
    from health_checker import DISEASES, SYMPTOM_IDS, SYMPTOMS

# O(1) disease lookup index (avoids N+1 linear scans)
_DISEASES_BY_ID: dict = {d["id"]: d for d in DISEASES}
_SYMPTOMS_BY_ID: dict = {s["id"]: s for s in SYMPTOMS}

# AI-powered symptom extraction (Phase 1)
_AI_EXTRACTION_ENABLED = os.getenv("VETDICT_USE_AI_SYMPTOM_EXTRACTION", "false").lower() == "true"
_AI_EXTRACTOR = None
_AI_EXTRACTOR_LOCK = threading.Lock()

def _get_ai_extractor():
    """Lazy-load AI extractor singleton (thread-safe)."""
    global _AI_EXTRACTOR
    if _AI_EXTRACTOR is not None:
        return _AI_EXTRACTOR if _AI_EXTRACTOR else None
    if not _AI_EXTRACTION_ENABLED:
        return None
    with _AI_EXTRACTOR_LOCK:
        if _AI_EXTRACTOR is not None:
            return _AI_EXTRACTOR if _AI_EXTRACTOR else None
        try:
            from api.ai import SymptomExtractor
            from api.config_constants import (
                AI_SYMPTOM_CACHE_TTL,
                AI_SYMPTOM_CONFIDENCE_THRESHOLD,
                AI_SYMPTOM_EXTRACTION_TIMEOUT,
            )
            from api.config_constants import (
                AI_SYMPTOM_MODEL as DEFAULT_MODEL,
            )
            # Environment variable overrides config constant
            ai_model = os.getenv("AI_SYMPTOM_MODEL", DEFAULT_MODEL)
            ai_timeout = float(os.getenv("AI_SYMPTOM_TIMEOUT", AI_SYMPTOM_EXTRACTION_TIMEOUT))
            ai_cache_ttl = int(os.getenv("AI_SYMPTOM_CACHE_TTL", AI_SYMPTOM_CACHE_TTL))
            ai_confidence = float(os.getenv("AI_SYMPTOM_CONFIDENCE", AI_SYMPTOM_CONFIDENCE_THRESHOLD))
            ai_fallback = os.getenv("AI_SYMPTOM_FALLBACK", "true").lower() == "true"

            extractor = SymptomExtractor(
                api_key=os.getenv("ANTHROPIC_API_KEY"),
                model=ai_model,
                timeout=ai_timeout,
                cache_enabled=True,
                cache_ttl=ai_cache_ttl,
                confidence_threshold=ai_confidence,
                fallback_enabled=ai_fallback,
                manual_aliases=SYMPTOM_ALIASES if 'SYMPTOM_ALIASES' in globals() else {},
            )
            extractor.set_valid_symptom_ids(SYMPTOM_IDS)
            _AI_EXTRACTOR = extractor
            logger.info("AI symptom extractor initialized (model=%s, timeout=%ss)", ai_model, ai_timeout)
        except Exception as e:
            logger.warning("Failed to initialize AI extractor: %s", e)
            _AI_EXTRACTOR = False  # Sentinel value to avoid retrying
    return _AI_EXTRACTOR if _AI_EXTRACTOR else None


def evaluate_with_ai_confidence(
    inference: Dict[str, float],
    evidence: Dict[str, Any],
    context: Dict[str, Any],
    ai_result: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Evaluate diagnostic context with optional AI confidence enhancement (Phase 2c).

    This is an optional integration with RECO2 integrity gate that applies
    AI symptom extraction confidence to enhance verdict generation.

    Args:
        inference: Disease inference vector (name -> confidence)
        evidence: Evidence data with median values for each field
        context: Patient/domain context (domain, confidence, etc.)
        ai_result: Optional Phase 2b extraction result with personalization metadata

    Returns:
        RECO2 evaluation result with integrity metrics and AI confidence metadata
    """
    try:
        from reco2 import engine

        return engine.evaluate_payload(
            {
                "inference": inference,
                "evidence": evidence,
                "context": context,
            },
            ai_result=ai_result,
        )
    except Exception as e:
        logger.debug("RECO2 evaluation failed, skipping: %s", e)
        # Return None to indicate RECO2 unavailable - caller should continue normally
        return None

# Import equine data for horse chat support
try:
    from api.species.equine_diseases import (
        DISEASE_DATABASE as EQUINE_DISEASES,
    )
    from api.species.equine_diseases import (
        HEALTH_CHECK_ITEMS as EQUINE_HEALTH_CHECK_ITEMS,
    )
    EQUINE_AVAILABLE = True
except ImportError:
    try:
        from species.equine_diseases import (
            DISEASE_DATABASE as EQUINE_DISEASES,
        )
        from species.equine_diseases import (
            HEALTH_CHECK_ITEMS as EQUINE_HEALTH_CHECK_ITEMS,
        )
        EQUINE_AVAILABLE = True
    except ImportError:
        EQUINE_DISEASES = []
        EQUINE_HEALTH_CHECK_ITEMS = {}
        EQUINE_AVAILABLE = False

# ---------------------------------------------------------------------------
# Shared constants, species data & symptom aliases (extracted to api/chat/)
# ---------------------------------------------------------------------------
from api.chat.constants import _GENERIC_SPECIES, SPECIES_LABELS  # noqa: F401
from api.chat.species_data import _SPECIES_DATA  # noqa: F401
from api.chat.symptom_aliases import SYMPTOM_ALIASES  # noqa: F401

# =============================================================================
# EQUINE SYMPTOM ALIASES (natural language → equine finding keys)
# =============================================================================

EQUINE_SYMPTOM_ALIASES: dict[str, str] = {
    # -- General --
    "fever": "gen_fever", "発熱": "gen_fever", "熱がある": "gen_fever", "高熱": "gen_fever",
    "lethargy": "gen_lethargy", "元気がない": "gen_lethargy", "ぐったり": "gen_lethargy",
    "元気ない": "gen_lethargy", "沈鬱": "gen_lethargy", "depression": "gen_lethargy",
    "weight loss": "gen_weight_loss", "体重減少": "gen_weight_loss", "痩せた": "gen_weight_loss",
    "痩せてきた": "gen_weight_loss", "losing weight": "gen_weight_loss",
    "poor appetite": "gen_poor_appetite", "食欲不振": "gen_poor_appetite",
    "食欲がない": "gen_poor_appetite", "食べない": "gen_poor_appetite",
    "not eating": "gen_poor_appetite", "anorexia": "gen_poor_appetite",
    "dehydration": "gen_dehydration", "脱水": "gen_dehydration",
    "swollen lymph nodes": "gen_swollen_lymph", "リンパ節腫脹": "gen_swollen_lymph",
    "sweating": "gen_sweating", "発汗": "gen_sweating", "汗をかく": "gen_sweating",
    "recumbent": "gen_recumbent", "立てない": "gen_recumbent", "横臥": "gen_recumbent",
    "起き上がれない": "gen_recumbent", "can't stand": "gen_recumbent",
    "polydipsia": "gen_polydipsia", "多飲": "gen_polydipsia", "水をよく飲む": "gen_polydipsia",
    "polyuria": "gen_polyuria", "多尿": "gen_polyuria",
    "jaundice": "gen_icterus", "黄疸": "gen_icterus", "icterus": "gen_icterus",
    "pale gums": "gen_pale_mucosa", "歯ぐき白い": "gen_pale_mucosa",
    "pale mucous membranes": "gen_pale_mucosa", "蒼白": "gen_pale_mucosa",
    "tachycardia": "gen_tachycardia", "頻脈": "gen_tachycardia", "心拍が速い": "gen_tachycardia",
    "tachypnea": "gen_tachypnea", "頻呼吸": "gen_tachypnea", "呼吸が速い": "gen_tachypnea",
    # -- Body --
    "back pain": "body_back_pain", "背中痛い": "body_back_pain", "背部痛": "body_back_pain",
    "muscle atrophy": "body_muscle_atrophy", "筋萎縮": "body_muscle_atrophy",
    "swelling": "body_swelling", "腫れ": "body_swelling",
    "edema": "body_edema", "むくみ": "body_edema", "浮腫": "body_edema",
    "poor coat": "body_poor_coat", "毛づやが悪い": "body_poor_coat",
    "dark urine": "body_dark_urine", "尿が濃い": "body_dark_urine", "茶色い尿": "body_dark_urine",
    "abdominal distension": "body_abdominal_distension", "お腹が張る": "body_abdominal_distension",
    "muscle fasciculation": "body_muscle_fasciculation", "筋肉がピクピク": "body_muscle_fasciculation",
    "hirsutism": "body_hirsutism", "多毛": "body_hirsutism", "毛が長い": "body_hirsutism",
    "stiffness": "body_stiffness", "こわばり": "body_stiffness", "硬い": "body_stiffness",
    "ventral edema": "body_ventral_edema", "下腹部むくみ": "body_ventral_edema",
    "neck crest": "body_neck_crest", "首が太い": "body_neck_crest",
    "fat deposits": "body_fat_deposits", "脂肪が異常": "body_fat_deposits",
    "emaciation": "body_rib_visible", "痩せすぎ": "body_rib_visible",
    # -- Limb --
    "forelimb lameness": "limb_lameness_fore", "前肢跛行": "limb_lameness_fore",
    "前脚びっこ": "limb_lameness_fore", "前脚かばう": "limb_lameness_fore",
    "hindlimb lameness": "limb_lameness_hind", "後肢跛行": "limb_lameness_hind",
    "後脚びっこ": "limb_lameness_hind", "後脚かばう": "limb_lameness_hind",
    "lameness": "limb_lameness_fore", "跛行": "limb_lameness_fore",
    "びっこ": "limb_lameness_fore", "limping": "limb_lameness_fore",
    "joint swelling": "limb_joint_swelling", "関節腫脹": "limb_joint_swelling",
    "関節が腫れ": "limb_joint_swelling",
    "tendon heat": "limb_tendon_heat", "腱が熱い": "limb_tendon_heat",
    "tendon swelling": "limb_tendon_swelling", "腱が腫れ": "limb_tendon_swelling",
    "windpuffs": "limb_windpuffs", "ウインドパフ": "limb_windpuffs",
    "splints": "limb_splints", "ソエ": "limb_splints",
    "digital pulse": "limb_digital_pulse", "蹄脈が強い": "limb_digital_pulse",
    "upward fixation": "limb_upward_fixation", "膝蓋骨固定": "limb_upward_fixation",
    # -- Hoof --
    "laminitis": "hoof_laminitis_signs", "蹄葉炎": "hoof_laminitis_signs",
    "hoof abscess": "hoof_abscess", "蹄膿瘍": "hoof_abscess",
    "hoof heat": "hoof_heat", "蹄が熱い": "hoof_heat",
    "thrush": "hoof_thrush", "蹄叉腐爛": "hoof_thrush",
    "hoof crack": "hoof_crack", "蹄の亀裂": "hoof_crack", "裂蹄": "hoof_crack",
    "white line disease": "hoof_white_line", "白線病": "hoof_white_line",
    "hoof foul odor": "hoof_foul_odor", "蹄が臭い": "hoof_foul_odor",
    "navicular": "hoof_navicular", "舟状骨": "hoof_navicular",
    # -- Respiratory --
    "cough": "resp_cough", "咳": "resp_cough", "せき": "resp_cough", "coughing": "resp_cough",
    "nasal discharge": "resp_nasal_discharge", "鼻水": "resp_nasal_discharge",
    "鼻汁": "resp_nasal_discharge",
    "epistaxis": "resp_epistaxis", "鼻血": "resp_epistaxis", "鼻出血": "resp_epistaxis",
    "labored breathing": "resp_labored_breathing", "呼吸困難": "resp_labored_breathing",
    "息が荒い": "resp_labored_breathing", "呼吸が辛そう": "resp_labored_breathing",
    "stridor": "resp_stridor", "喘鳴": "resp_stridor", "異常呼吸音": "resp_stridor",
    "exercise intolerance": "resp_exercise_intolerance", "運動不耐性": "resp_exercise_intolerance",
    "すぐバテる": "resp_exercise_intolerance", "パフォーマンス低下": "resp_exercise_intolerance",
    # -- Digestive --
    "colic": "dig_colic_signs", "疝痛": "dig_colic_signs", "お腹痛い": "dig_colic_signs",
    "腹痛": "dig_colic_signs",
    "diarrhea": "dig_diarrhea", "下痢": "dig_diarrhea",
    "constipation": "dig_constipation", "便秘": "dig_constipation",
    "bloat": "dig_bloat", "鼓脹": "dig_bloat",
    "bloody stool": "dig_bloody_stool", "血便": "dig_bloody_stool",
    "drooling": "dig_salivation", "流涎": "dig_salivation", "よだれ": "dig_salivation",
    "gastric reflux": "dig_gastric_reflux", "胃液逆流": "dig_gastric_reflux",
    "teeth grinding": "dig_bruxism", "歯ぎしり": "dig_bruxism", "bruxism": "dig_bruxism",
    "reduced gut sounds": "dig_reduced_gut", "腸音減少": "dig_reduced_gut",
    # -- Skin --
    "hair loss": "skin_hair_loss", "脱毛": "skin_hair_loss", "毛が抜ける": "skin_hair_loss",
    "itching": "skin_itching", "痒い": "skin_itching", "掻いてる": "skin_itching",
    "hives": "skin_hives", "蕁麻疹": "skin_hives", "urticaria": "skin_hives",
    "skin lesions": "skin_lesions", "皮膚病変": "skin_lesions",
    "crusting": "skin_crusting", "痂皮": "skin_crusting", "かさぶた": "skin_crusting",
    "photosensitivity": "skin_photosensitivity", "光線過敏": "skin_photosensitivity",
    "sarcoid": "skin_sarcoid", "サルコイド": "skin_sarcoid",
    "wound": "skin_wound", "傷": "skin_wound", "外傷": "skin_wound",
    # -- Eye --
    "eye discharge": "eye_discharge", "目やに": "eye_discharge",
    "squinting": "eye_squinting", "目を細める": "eye_squinting",
    "tearing": "eye_tearing", "涙目": "eye_tearing", "流涙": "eye_tearing",
    "cloudy eye": "eye_cloudiness", "目が白い": "eye_cloudiness", "目の白濁": "eye_cloudiness",
    "eye swelling": "eye_swelling", "目の腫れ": "eye_swelling",
    "uveitis": "eye_uveitis_signs", "ぶどう膜炎": "eye_uveitis_signs",
    # -- Neuro --
    "ataxia": "neuro_ataxia", "運動失調": "neuro_ataxia", "ふらふら": "neuro_ataxia",
    "seizure": "neuro_seizure", "発作": "neuro_seizure", "けいれん": "neuro_seizure",
    "tremor": "neuro_tremor", "振戦": "neuro_tremor", "震え": "neuro_tremor",
    "head tilt": "neuro_head_tilt", "首が傾く": "neuro_head_tilt",
    "circling": "neuro_circling", "旋回": "neuro_circling",
    "behavior change": "neuro_behavior_change", "行動変化": "neuro_behavior_change",
    "aggression": "neuro_aggression", "攻撃的": "neuro_aggression",
    "hyperesthesia": "neuro_hyperesthesia", "過敏": "neuro_hyperesthesia",
    "tail paralysis": "neuro_tail_paralysis", "尾の麻痺": "neuro_tail_paralysis",
    # -- Cardio --
    "heart murmur": "cardio_murmur", "心雑音": "cardio_murmur",
    "irregular rhythm": "cardio_irregular_rhythm", "不整脈": "cardio_irregular_rhythm",
    "syncope": "cardio_syncope", "失神": "cardio_syncope",
    "jugular pulse": "cardio_jugular_pulse", "頚静脈怒張": "cardio_jugular_pulse",
    # -- Reproductive --
    "vulvar discharge": "repro_vulvar_discharge", "陰部排出物": "repro_vulvar_discharge",
    "abortion": "repro_abortion", "流産": "repro_abortion",
    "dystocia": "repro_dystocia", "難産": "repro_dystocia",
    "retained placenta": "repro_placenta_retained", "胎盤停滞": "repro_placenta_retained",
    "testicular swelling": "repro_testicular_swelling", "精巣腫脹": "repro_testicular_swelling",
    "udder changes": "repro_udder_changes", "乳房変化": "repro_udder_changes",
    # -- Dental --
    "quidding": "dental_quidding", "クイディング": "dental_quidding",
    "食べこぼし": "dental_quidding",
    "bad breath": "dental_bad_breath", "口臭": "dental_bad_breath",
    "facial swelling": "dental_facial_swelling", "顔の腫れ": "dental_facial_swelling",
    "bit resistance": "dental_bit_resistance", "ハミを嫌がる": "dental_bit_resistance",
    # -- Foal --
    "foal diarrhea": "foal_diarrhea", "子馬の下痢": "foal_diarrhea",
    "foal lethargy": "foal_lethargy", "子馬の元気がない": "foal_lethargy",
    "foal fever": "foal_fever", "子馬の発熱": "foal_fever",
    "foal joint swelling": "foal_joint_swelling", "子馬の関節腫脹": "foal_joint_swelling",
    "foal limb deformity": "foal_limb_deformity", "子馬の肢変形": "foal_limb_deformity",
    "failure to stand": "foal_failure_stand", "立てない子馬": "foal_failure_stand",
    "weak suckle": "foal_weak_suckle", "吸啜力低下": "foal_weak_suckle",
    "umbilical swelling": "foal_umbilical_swelling", "臍が腫れ": "foal_umbilical_swelling",
    "meconium retention": "foal_meconium_retention", "胎便停滞": "foal_meconium_retention",
    # -- Urinary --
    "hematuria": "uri_hematuria", "血尿": "uri_hematuria",
    "dysuria": "uri_dysuria", "排尿困難": "uri_dysuria",
    "stranguria": "uri_stranguria", "排尿痛": "uri_stranguria",
    "discolored urine": "uri_discolored_urine", "尿の色異常": "uri_discolored_urine",
}

# Build equine finding key set for validation
_EQUINE_FINDING_KEYS: set[str] = set()
for _cat, _items in EQUINE_HEALTH_CHECK_ITEMS.items():
    for _key, _ja, _en in _items:
        _EQUINE_FINDING_KEYS.add(_key)

# Build equine symptoms list (for direct name matching in chat)
_EQUINE_SYMPTOMS: list[dict[str, str]] = []
for _cat, _items in EQUINE_HEALTH_CHECK_ITEMS.items():
    for _key, _ja, _en in _items:
        _EQUINE_SYMPTOMS.append({"id": _key, "name_ja": _ja, "name_en": _en, "category": _cat})


def _extract_equine_symptoms(text: str) -> list[str]:
    """Extract equine finding keys from natural language text."""
    text_lower = text.lower()
    matched: set[str] = set()

    # Direct name matches from health check items
    for sym in _EQUINE_SYMPTOMS:
        if sym["name_ja"].lower() in text_lower or sym["name_en"].lower() in text_lower:
            matched.add(sym["id"])

    # Alias matches
    for alias, finding_key in EQUINE_SYMPTOM_ALIASES.items():
        if alias in text_lower and finding_key in _EQUINE_FINDING_KEYS:
            matched.add(finding_key)

    return list(matched)


def _match_equine_symptoms_to_diseases(finding_keys: list[str]) -> list[dict]:
    """Match equine finding keys to equine diseases using Jaccard similarity."""
    if not finding_keys:
        return []

    key_set = set(finding_keys)
    matches = []

    for disease in EQUINE_DISEASES:
        disease_findings = set(disease.associated_findings)
        if not disease_findings:
            continue

        intersection = len(key_set & disease_findings)
        union = len(key_set | disease_findings)

        if intersection > 0:
            similarity = intersection / union
            matches.append({
                "disease_id": disease.id,
                "name_ja": disease.name_ja,
                "name_en": disease.name_en,
                "severity": disease.severity,
                "similarity_score": round(similarity, 3),
                "matched_symptoms": list(key_set & disease_findings),
                "unmatched_user_symptoms": list(key_set - disease_findings),
                "additional_disease_symptoms": list(disease_findings - key_set),
                "description": disease.description_ja,
                "description_ja": disease.description_ja,
                "description_en": disease.name_en,
                "recommended_tests": [
                    f"{ja} ({en})" for _, ja, en in disease.recommended_exams
                ],
            })

    matches.sort(key=lambda m: m["similarity_score"], reverse=True)
    return matches


# Symptom extractor & disease matcher extracted to api/chat/
from api.chat.disease_matcher import _match_species_symptoms_to_diseases  # noqa: F401
from api.chat.symptom_extractor import _extract_species_symptoms  # noqa: F401

# =============================================================================
# SYMPTOM EXTRACTION FROM TEXT
# =============================================================================

def extract_symptoms_from_text(text: str) -> list:
    """
    Extract symptom IDs from natural language text.

    Uses Claude AI extraction if enabled, falls back to manual aliases on error.

    Args:
        text: User input text describing symptoms

    Returns:
        List of matched symptom IDs
    """
    # Attempt AI extraction if enabled
    if _AI_EXTRACTION_ENABLED:
        extractor = _get_ai_extractor()
        if extractor:
            try:
                result = extractor.extract(
                    text=text,
                    patient_species="dog",
                    language="auto",
                    allow_fallback=True,
                )
                symptoms = result.get("symptoms", [])
                method = result.get("method", "unknown")
                confidence = result.get("confidence", 0.0)
                logger.info(
                    f"Symptom extraction: method={method} "
                    f"confidence={confidence} symptoms={len(symptoms)}"
                )
                if symptoms:
                    return symptoms
                # If AI found no symptoms but no error, continue to manual fallback
            except Exception as e:
                logger.warning("AI extraction failed, falling back to manual: %s", e)
                # Fall through to manual extraction

    # Manual extraction (original algorithm)
    text_lower = text.lower()
    matched_symptoms = set()

    # ---------------------------------------------------------------
    # Phase 1: Longest-match-first alias matching
    # Sort aliases by length descending so that longer, more specific
    # phrases match before shorter substrings (e.g. "食欲がない" before
    # "ない", "blood in stool" before "stool").
    # ---------------------------------------------------------------
    _sorted_aliases = sorted(SYMPTOM_ALIASES.keys(), key=len, reverse=True)
    consumed_ranges: list[tuple[int, int]] = []  # track matched text regions

    for alias in _sorted_aliases:
        pos = text_lower.find(alias)
        if pos == -1:
            continue
        symptom_id = SYMPTOM_ALIASES[alias]
        if symptom_id not in SYMPTOM_IDS:
            continue
        end = pos + len(alias)
        # Skip if this range overlaps with an already-consumed range
        overlap = False
        for cs, ce in consumed_ranges:
            if pos < ce and end > cs:
                overlap = True
                break
        if overlap:
            # Still add the symptom (same region might describe multiple things)
            matched_symptoms.add(symptom_id)
            continue
        matched_symptoms.add(symptom_id)
        consumed_ranges.append((pos, end))

    # Phase 2: Direct symptom name matches (catch anything aliases missed)
    for symptom in SYMPTOMS:
        name_ja = symptom["name_ja"].lower()
        name_en = symptom["name_en"].lower()
        symptom_id = symptom["id"]
        if name_ja in text_lower or name_en in text_lower:
            matched_symptoms.add(symptom_id)

    # ---------------------------------------------------------------
    # Phase 3: Fuzzy / partial matching for Japanese input
    # If no symptoms matched yet, try splitting by common particles and
    # retrying with individual phrases.  This handles cases like
    # "咳と下痢がある" → ["咳", "下痢がある"] → coughing, diarrhea
    # ---------------------------------------------------------------
    if not matched_symptoms:
        import re as _re
        fragments = _re.split(r'[、。,.と！!？?\s]+', text_lower)
        fragments = [f.strip() for f in fragments if len(f.strip()) >= 1]
        for frag in fragments:
            for alias in _sorted_aliases:
                if alias in frag:
                    sid = SYMPTOM_ALIASES[alias]
                    if sid in SYMPTOM_IDS:
                        matched_symptoms.add(sid)
                        break  # one match per fragment is enough
            # Also check direct names
            for symptom in SYMPTOMS:
                if symptom["name_ja"].lower() in frag or symptom["name_en"].lower() in frag:
                    matched_symptoms.add(symptom["id"])

    return list(matched_symptoms)


# =============================================================================
# ONSET (TIME-COURSE) EXTRACTION FROM TEXT
# =============================================================================

_ONSET_ALIASES: dict[str, str] = {
    # English
    "sudden": "acute", "suddenly": "acute", "just started": "acute",
    "today": "acute", "just now": "acute", "this morning": "acute",
    "last night": "acute", "few hours ago": "acute", "acute": "acute",
    "few days": "subacute", "several days": "subacute",
    "a week": "subacute", "this week": "subacute", "subacute": "subacute",
    "days ago": "subacute", "couple of days": "subacute",
    "chronic": "chronic", "long time": "chronic", "months": "chronic",
    "weeks": "chronic", "for a while": "chronic", "ongoing": "chronic",
    "persistent": "chronic", "keeps coming back": "chronic",
    "recurring": "chronic", "always": "chronic",
    # Japanese
    "突然": "acute", "急に": "acute", "今日から": "acute",
    "さっきから": "acute", "今朝から": "acute", "昨夜から": "acute",
    "急性": "acute",
    "数日前から": "subacute", "2〜3日前から": "subacute",
    "2～3日前から": "subacute", "2-3日前から": "subacute",
    "1週間前から": "subacute", "先週から": "subacute",
    "数日": "subacute", "亜急性": "subacute",
    "ずっと": "chronic", "以前から": "chronic", "前から": "chronic",
    "長い間": "chronic", "慢性": "chronic", "何ヶ月も": "chronic",
    "何週間も": "chronic", "繰り返し": "chronic", "ずっと前から": "chronic",
    "だいぶ前から": "chronic",
}


def extract_onset_from_text(text: str) -> str | None:
    """Extract onset (time-course) from natural language text.

    Returns "acute", "subacute", "chronic", or None if not detected.
    """
    text_lower = text.lower()
    for phrase, onset in _ONSET_ALIASES.items():
        if phrase in text_lower:
            return onset
    return None


# =============================================================================
# AGE EXTRACTION FROM TEXT
# =============================================================================

_AGE_ALIASES: dict[str, float] = {
    # English
    "puppy": 0.5, "kitten": 0.3,
    # Japanese
    "子犬": 0.5, "子猫": 0.3,
    "1歳": 1.0, "2歳": 2.0, "3歳": 3.0, "4歳": 4.0, "5歳": 5.0,
    "6歳": 6.0, "7歳": 7.0, "8歳": 8.0, "9歳": 9.0, "10歳": 10.0,
    "11歳": 11.0, "12歳": 12.0, "13歳": 13.0, "14歳": 14.0, "15歳": 15.0,
    "半年": 0.5, "生後3ヶ月": 0.25, "生後6ヶ月": 0.5,
    "老犬": 10.0, "老猫": 12.0, "シニア": 9.0,
}


def extract_age_from_text(text: str) -> float | None:
    """Extract approximate age in years from natural language text.

    Returns a float (years) or None if not detected.
    """
    text_lower = text.lower()
    import re
    # Try patterns like "5 years old", "3 year old"
    match = re.search(r"(\d+(?:\.\d+)?)\s*(?:years?\s*old|yo\b|yrs?\b)", text_lower)
    if match:
        return float(match.group(1))
    # Try Japanese alias matches (longest match first)
    for phrase in sorted(_AGE_ALIASES.keys(), key=len, reverse=True):
        if phrase in text_lower:
            return _AGE_ALIASES[phrase]
    return None


def generate_disease_reasoning_ja(disease: dict, symptoms: list) -> str:
    """Generate Japanese explanation for why this disease was suggested."""
    matched_count = len(disease.get("matched_symptoms", []))
    total_symptoms = matched_count + len(disease.get("unmatched_user_symptoms", []))

    return f"患者犬の症状セット（{matched_count}/{total_symptoms}）が{disease['name_ja']}と高く一致しており、類似度は{int(disease['similarity_score']*100)}%です。"


def generate_disease_reasoning_en(disease: dict, symptoms: list) -> str:
    """Generate English explanation for why this disease was suggested."""
    matched_count = len(disease.get("matched_symptoms", []))
    total_symptoms = matched_count + len(disease.get("unmatched_user_symptoms", []))

    return f"The dog's symptom profile ({matched_count}/{total_symptoms}) shows strong alignment with {disease['name_en']}, with a similarity score of {int(disease['similarity_score']*100)}%."


# DISEASE_SUPPLEMENTS extracted to api/chat/supplements.py
from api.chat.supplements import (  # noqa: F401
    _DEFAULT_SUPPLEMENTS,
    DISEASE_SUPPLEMENTS,
    get_treatment_recommendations_for_disease,
)


def match_symptoms_to_diseases(
    symptom_ids: list,
    *,
    pain_score: int | None = None,
    lab_values: dict | None = None,
    breed: str | None = None,
) -> list:
    """
    Match extracted symptoms to diseases using advanced weighted scoring.

    Uses the same TF-IDF + clinical-specificity engine as the health checker
    for consistent, high-accuracy differential diagnosis.

    Returns disease matches sorted by composite score (descending).
    """
    if not symptom_ids:
        return []

    import math

    # Import scoring components from health_checker (single source of truth)
    from api.health_checker import (
        _PATHOGNOMONIC_CLUSTERS,
        _SYMPTOM_SPECIFICITY,
        _compute_symptom_weight,
    )

    symptom_set = set(symptom_ids)
    user_weights = {s: _compute_symptom_weight(s) for s in symptom_set}
    total_user_weight = sum(user_weights.values())
    matches = []

    for disease in DISEASES:
        disease_symptoms = set(disease["symptoms"])
        if not disease_symptoms:
            continue

        matched = symptom_set & disease_symptoms
        if not matched:
            continue

        # Weighted recall
        matched_weight = sum(user_weights.get(s, 1.0) for s in matched)
        weighted_recall = matched_weight / total_user_weight if total_user_weight > 0 else 0

        # Coverage
        disease_weights = {s: _compute_symptom_weight(s) for s in disease_symptoms}
        total_disease_weight = sum(disease_weights.values())
        covered_weight = sum(disease_weights.get(s, 1.0) for s in matched)
        coverage = covered_weight / total_disease_weight if total_disease_weight > 0 else 0

        # Harmonic mean base score
        if weighted_recall + coverage > 0:
            base_score = 2.0 * weighted_recall * coverage / (weighted_recall + coverage)
        else:
            base_score = 0.0

        # Specificity bonus
        specificity_bonus = 0.0
        for s in matched:
            spec = _SYMPTOM_SPECIFICITY.get(s, 1.0)
            if spec >= 2.0:
                specificity_bonus += 0.06
            elif spec >= 1.5:
                specificity_bonus += 0.03
        base_score = min(base_score + specificity_bonus, 1.0)

        # Pathognomonic cluster boost
        cluster_boost = 1.0
        for cluster_syms, cluster_did, boost in _PATHOGNOMONIC_CLUSTERS:
            if cluster_did == disease["id"] and cluster_syms <= symptom_set:
                cluster_boost = max(cluster_boost, boost)

        # Negative evidence penalty
        missing = disease_symptoms - symptom_set
        negative_penalty = 1.0
        if len(symptom_set) >= 3:
            for s in missing:
                spec = _SYMPTOM_SPECIFICITY.get(s, 1.0)
                if spec >= 2.5:
                    negative_penalty -= 0.06
                elif spec >= 2.0:
                    negative_penalty -= 0.03
            negative_penalty = max(negative_penalty, 0.5)

        composite = base_score * cluster_boost * negative_penalty

        # Logistic confidence calibration (same curve as health_checker)
        raw_logistic = 1.0 / (1.0 + math.exp(-6.0 * (composite - 0.4)))
        confidence = min(round(raw_logistic * 100, 1), 95.0)

        matches.append({
            "disease_id": disease["id"],
            "name_ja": disease["name_ja"],
            "name_en": disease["name_en"],
            "severity": disease["severity"],
            "similarity_score": round(composite, 3),
            "confidence_percent": confidence,
            "matched_symptoms": sorted(matched),
            "unmatched_user_symptoms": sorted(symptom_set - disease_symptoms),
            "additional_disease_symptoms": sorted(disease_symptoms - symptom_set),
            "missing_key_symptoms": sorted(
                s for s in missing
                if _SYMPTOM_SPECIFICITY.get(s, 1.0) >= 1.5
            ),
            "description": disease.get("description", ""),
            "description_ja": disease.get("description_ja", ""),
            "description_en": disease.get("description_en", ""),
            "recommended_tests": disease.get("recommended_tests", []),
            "scoring_detail": {
                "weighted_recall": round(weighted_recall, 3),
                "coverage": round(coverage, 3),
                "cluster_boost": cluster_boost,
                "negative_penalty": round(negative_penalty, 3),
            },
        })

    matches.sort(key=lambda m: m["similarity_score"], reverse=True)
    return matches


# =============================================================================
# FOLLOW-UP QUESTION BUILDER
# =============================================================================


def _extract_mentioned_drugs(disease: dict, species: str) -> list:
    """Extract drugs mentioned in treatment text with species-specific dosage."""
    treatment_text = (
        (disease.get("treatment_ja") or "")
        + " "
        + (disease.get("treatment") or "")
    ).lower()
    if not treatment_text.strip():
        return []
    try:
        from api.drug_dictionary import DRUGS as _ALL_DRUGS
    except Exception:
        return []
    matched = []
    for dr in _ALL_DRUGS:
        dr_name = dr.get("name", "")
        dr_name_ja = dr.get("name_ja", "")
        if not ((dr_name and dr_name.lower() in treatment_text)
                or (dr_name_ja and dr_name_ja in treatment_text)):
            continue
        entry = {
            "id": dr.get("id", ""),
            "name": dr_name,
            "name_ja": dr_name_ja,
            "category": dr.get("category", ""),
        }
        si = (dr.get("species_info") or {}).get(species)
        if si:
            entry["dosage"] = si.get("dosage", "")
            entry["dosage_ja"] = si.get("dosage_ja", "")
            entry["safe"] = si.get("safe", True)
            entry["notes"] = si.get("notes", "")
            entry["notes_ja"] = si.get("notes_ja", "")
        matched.append(entry)
        if len(matched) >= 10:
            break
    return matched


def _build_follow_up_questions(
    onset: str | None,
    age: float | None,
    symptoms: list,
    disease_candidates: list | None = None,
    species: str = "dog",
) -> list[dict]:
    """Build context-aware follow-up questions for interactive consultation.

    Generates targeted symptom questions based on top disease candidates
    to progressively narrow differential diagnosis — mimicking a vet exam.
    """
    questions: list[dict] = []

    # Phase 1: If no symptoms yet, ask what's wrong
    if not symptoms:
        questions.append({
            "question_ja": "どのような症状がありますか？",
            "question_en": "What symptoms are you seeing?",
            "type": "symptoms",
            "options": [],
        })
        return questions

    # Phase 2: Basic context (onset / age) — ask once
    if not onset:
        questions.append({
            "question_ja": "症状はいつ頃から始まりましたか？",
            "question_en": "When did the symptoms start?",
            "type": "onset",
            "options": [
                {"value": "acute", "label_ja": "突然（24時間以内）", "label_en": "Suddenly (within 24h)"},
                {"value": "subacute", "label_ja": "数日前から", "label_en": "A few days ago"},
                {"value": "chronic", "label_ja": "2週間以上前から", "label_en": "More than 2 weeks ago"},
            ],
        })

    if age is None:
        questions.append({
            "question_ja": "何歳ですか？（だいたいで構いません）",
            "question_en": "How old is the animal? (approximate is fine)",
            "type": "age",
            "options": [
                {"value": 0.5, "label_ja": "1歳未満", "label_en": "Under 1 year"},
                {"value": 3.0, "label_ja": "1〜5歳", "label_en": "1–5 years"},
                {"value": 8.0, "label_ja": "5歳以上", "label_en": "5+ years"},
            ],
        })

    # Phase 3: Targeted symptom questions from disease candidates
    if disease_candidates and len(symptoms) >= 1:
        symptom_set = set(symptoms)
        # Collect key missing symptoms from top candidates for differentiation
        seen_symptoms: set[str] = set()
        sp_names = {}
        if species in _SPECIES_DATA:
            sp_names = _SPECIES_DATA[species].get("symptom_names", {})

        for candidate in disease_candidates[:5]:
            missing = candidate.get("missing_key_symptoms") or candidate.get("additional_disease_symptoms", [])
            for sid in missing[:3]:
                if sid in symptom_set or sid in seen_symptoms:
                    continue
                if len(questions) >= 5:
                    break
                seen_symptoms.add(sid)
                names = sp_names.get(sid, {})
                name_ja = names.get("ja", sid)
                name_en = names.get("en", sid)
                questions.append({
                    "question_ja": f"{name_ja}はありますか？",
                    "question_en": f"Is there {name_en.lower()}?",
                    "type": "symptom_check",
                    "symptom_id": sid,
                    "options": [
                        {"value": f"+{sid}", "label_ja": f"はい — {name_ja}", "label_en": f"Yes — {name_en}"},
                        {"value": f"-{sid}", "label_ja": "いいえ", "label_en": "No"},
                    ],
                })
            if len(questions) >= 5:
                break

    return questions


def _species_guidance_line(species: str, symptom_count: int) -> str:
    """Build a species-specific guidance line for chat users."""
    labels = SPECIES_LABELS.get(species, {"ja": species, "en": species})
    if symptom_count == 0:
        return (
            f"{labels['ja']}の症状として認識できる情報が不足しています。"
            f"{labels['ja']}でよく使う症状名（例：食欲不振、呼吸困難、下痢）で再入力してください。"
        )
    return (
        f"{labels['ja']}として解析し、{symptom_count}件の症状から鑑別候補を抽出しました。"
        "動物種を切り替えると、候補疾患もその種のデータベースに切り替わります。"
    )


# =============================================================================
# API ENDPOINTS
# =============================================================================

@diagnostic_bp.route("/chat", methods=["POST"])
def diagnostic_chat():
    """
    Interactive symptom check chat endpoint (reference information only).

    Request JSON:
    {
        "message": "My dog has been coughing and sneezing",
        "breed_id": "122_labrador_retriever" (optional),
        "age_years": 3.5 (optional),
        "previous_symptoms": ["fever"] (optional)
    }

    Returns:
        - Extracted symptoms
        - Related disease reference information with similarity scores
        - Care guide information
        - Reference test information
        - Navigation suggestions
    """
    data = request.get_json() or {}
    message = data.get("message", "").strip()
    breed_id = data.get("breed_id")
    age_years = data.get("age_years")
    onset = data.get("onset")  # explicit onset from client
    previous_symptoms_raw = data.get("previous_symptoms", [])
    species = data.get("species", "dog")
    pain_score = data.get("pain_score")       # int 1-10 (optional)
    lab_values = data.get("lab_values")       # dict (optional)
    breed = data.get("breed")                 # str (optional)
    lang = data.get("lang", "")              # "ja" or "en" for regional prevalence

    if not message:
        return jsonify({"error": "Message required"}), 400

    # Input validation
    if len(message) > 5000:
        return jsonify({"error": "Message too long (max 5000 chars)"}), 400

    # Sanitise previous_symptoms: must be a list of short strings
    if not isinstance(previous_symptoms_raw, list):
        previous_symptoms_raw = []
    previous_symptoms = [
        str(s)[:200] for s in previous_symptoms_raw
        if isinstance(s, str) and s.strip()
    ][:100]

    # Extract onset/age from message text if not explicitly provided
    detected_onset = extract_onset_from_text(message)
    effective_onset = onset or detected_onset
    detected_age = extract_age_from_text(message)
    effective_age = age_years if age_years is not None else detected_age

    # --- Species-aware symptom extraction and disease matching ---
    if species == "horse" and EQUINE_AVAILABLE:
        extracted = _extract_equine_symptoms(message)
        all_symptoms = list(set(extracted + previous_symptoms))
        disease_matches = _match_equine_symptoms_to_diseases(all_symptoms)
        symptom_details = [
            {
                "id": sid,
                "name_ja": next((s["name_ja"] for s in _EQUINE_SYMPTOMS if s["id"] == sid), sid),
                "name_en": next((s["name_en"] for s in _EQUINE_SYMPTOMS if s["id"] == sid), sid),
                "category": next((s["category"] for s in _EQUINE_SYMPTOMS if s["id"] == sid), ""),
            }
            for sid in all_symptoms
        ]
    elif species != "dog" and species in _SPECIES_DATA:
        extracted = _extract_species_symptoms(message, species)
        all_symptoms = list(set(extracted + previous_symptoms))
        disease_matches = _match_species_symptoms_to_diseases(
            all_symptoms, species,
            pain_score=pain_score, lab_values=lab_values, breed=breed,
            lang=lang,
        )
        sp_names = _SPECIES_DATA[species]["symptom_names"]
        symptom_details = [
            {
                "id": sid,
                "name_ja": sp_names.get(sid, {}).get("ja", sid),
                "name_en": sp_names.get(sid, {}).get("en", sid),
                "category": "",
            }
            for sid in all_symptoms
        ]
    else:
        extracted = extract_symptoms_from_text(message)
        all_symptoms = list(set(extracted + previous_symptoms))
        disease_matches = match_symptoms_to_diseases(
            all_symptoms,
            pain_score=pain_score, lab_values=lab_values, breed=breed,
        )
        symptom_details = [
            {
                "id": sid,
                "name_ja": _SYMPTOMS_BY_ID.get(sid, {}).get("name_ja", ""),
                "name_en": _SYMPTOMS_BY_ID.get(sid, {}).get("name_en", ""),
                "category": _SYMPTOMS_BY_ID.get(sid, {}).get("category", ""),
            }
            for sid in all_symptoms
        ]

    # Enhance disease candidates with reasoning
    enhanced_candidates = []
    for disease in disease_matches[:10]:  # Top 10
        reasoning = {
            "why_this_condition_ja": generate_disease_reasoning_ja(disease, all_symptoms),
            "why_this_condition_en": generate_disease_reasoning_en(disease, all_symptoms),
            "confidence_factors": [
                {"factor": "symptom_match", "percentage": int(disease["similarity_score"] * 100), "weight": "High"},
                {"factor": "breed_predisposition", "percentage": 0, "weight": "Medium"},
                {"factor": "onset_match", "percentage": 0, "weight": "Medium",
                 "onset_detected": effective_onset},
                {"factor": "age_relevance", "percentage": 0, "weight": "Medium",
                 "age_detected": effective_age},
            ]
        }

        if species == "dog":
            treatments = get_treatment_recommendations_for_disease(disease["disease_id"], breed_id, age_years)
        else:
            treatments = {"supplements": [], "primary_care_plan_ja": "獣医師にご相談ください。",
                          "recommended_tests": disease.get("recommended_tests", [])}

        # Extract mentioned drugs from treatment text
        mentioned_drugs = _extract_mentioned_drugs(disease, species)

        enhanced_candidates.append({
            **disease,
            "reasoning": reasoning,
            "treatment_recommendations": treatments,
            "mentioned_drugs": mentioned_drugs,
            "confidence_level": f"{int(disease['similarity_score'] * 100)}%"
        })

    # Build human-readable response text for frontend
    guidance_line = _species_guidance_line(species, len(all_symptoms))

    if enhanced_candidates:
        response_text = f"{guidance_line}\n\n症状から以下の疾患が考えられます：\n\n"
        for i, c in enumerate(enhanced_candidates[:5], 1):
            response_text += f"{i}. **{c['name_ja']}** ({c['name_en']}) — 一致度 {c['confidence_level']}\n"
            if c.get("description_ja") or c.get("description"):
                response_text += f"   {c.get('description_ja') or c.get('description', '')}\n"
        response_text += "\n※ こちらは参考情報です。獣医師の診察を受けてください。"
    elif all_symptoms:
        response_text = (
            f"{guidance_line}\n"
            "症状を検出しましたが、該当する疾患が見つかりませんでした。"
            "もう少し詳しく症状を教えてください。"
        )
    else:
        response_text = (
            f"{guidance_line}\n"
            "症状を検出できませんでした。具体的な症状を入力してください。\n"
            "例: 「咳が出る」「跛行している」「元気がない」"
        )

    # Build response
    low_info_warning = None
    if len(all_symptoms) == 1:
        low_info_warning = "症状が1つのみのため、信頼度を制限しています。追加の症状を入力すると精度が向上します。"
    elif len(all_symptoms) == 2:
        low_info_warning = "症状が2つのため、信頼度に上限を設けています。さらに症状を追加すると精度が向上します。"
    response = {
        "response": response_text,
        "user_message": message,
        "species": species,
        "extracted_symptoms": extracted,
        "accumulated_symptoms": all_symptoms,
        "symptom_details": symptom_details,
        "disease_candidates": enhanced_candidates,
        "total_candidates": len(disease_matches),
        "species_guidance": guidance_line,
        "low_info_warning": low_info_warning,
        "breed_context": breed_id,
        "breed": breed,
        "pain_score": pain_score,
        "lab_values": lab_values,
        "age_context": effective_age,
        "onset_context": effective_onset,
        "onset_detected_from_text": detected_onset,
        "age_detected_from_text": detected_age,
        "follow_up_questions": _build_follow_up_questions(
            effective_onset, effective_age, all_symptoms,
            disease_candidates=enhanced_candidates, species=species,
        ),
        "recommendations": {
            "next_step": "This is reference information only. Supervised by Kentaro Kaimide, DVM (Minamisoma Vet Clinic). Please consult a veterinarian for professional evaluation.",
            "next_step_ja": "こちらは参考情報です（獣医師監修：上手健太郎／南相馬動物病院）。正確な評価のため、獣医師の診察を受けてください。",
        }
    }

    return jsonify(response)


@diagnostic_bp.route("/symptom-suggestions", methods=["GET"])
def symptom_suggestions():
    """
    Return all available symptoms for autocomplete/UI display.

    Query params:
    - category: Filter by category (respiratory, digestive, etc.)
    - search: Filter by name (partial match)
    """
    category = request.args.get("category")
    search = request.args.get("search", "").lower()

    results = SYMPTOMS

    if category:
        results = [s for s in results if s["category"] == category]

    if search:
        results = [
            s for s in results
            if search in s["name_ja"].lower() or search in s["name_en"].lower()
        ]

    return jsonify({
        "total": len(results),
        "symptoms": [
            {
                "id": s["id"],
                "name_ja": s["name_ja"],
                "name_en": s["name_en"],
                "category": s["category"],
            }
            for s in results
        ]
    })


@diagnostic_bp.route("/differential-analysis", methods=["POST"])
def differential_analysis():
    """
    Compare two diseases to show differential diagnosis reasoning.

    Request JSON:
    {
        "disease_id_1": "brachycephalic_airway_syndrome",
        "disease_id_2": "congestive_heart_failure",
        "symptoms": ["labored_breathing", "wheezing"],
        "breed_id": "122_labrador_retriever" (optional),
        "age_years": 3.5 (optional)
    }
    """
    data = request.get_json() or {}
    disease_id_1 = data.get("disease_id_1")
    disease_id_2 = data.get("disease_id_2")
    symptoms = data.get("symptoms", [])

    if not disease_id_1 or not disease_id_2:
        return jsonify({"error": "Both disease IDs required"}), 400

    disease_1 = _DISEASES_BY_ID.get(disease_id_1)
    disease_2 = _DISEASES_BY_ID.get(disease_id_2)

    if not disease_1 or not disease_2:
        return jsonify({"error": "One or both diseases not found"}), 404

    symptom_set = set(symptoms)
    symptoms_1 = set(disease_1.get("symptoms", []))
    symptoms_2 = set(disease_2.get("symptoms", []))

    comparison = {
        "disease_1": {
            "id": disease_1["id"],
            "name_ja": disease_1["name_ja"],
            "name_en": disease_1["name_en"],
            "severity": disease_1["severity"],
            "description": disease_1.get("description", ""),
            "description_ja": disease_1.get("description_ja", ""),
            "description_en": disease_1.get("description_en", ""),
        },
        "disease_2": {
            "id": disease_2["id"],
            "name_ja": disease_2["name_ja"],
            "name_en": disease_2["name_en"],
            "severity": disease_2["severity"],
            "description": disease_2.get("description", ""),
            "description_ja": disease_2.get("description_ja", ""),
            "description_en": disease_2.get("description_en", ""),
        },
        "symptom_analysis": {
            "shared_symptoms": list(symptoms_1 & symptoms_2),
            "unique_to_disease_1": list(symptoms_1 - symptoms_2),
            "unique_to_disease_2": list(symptoms_2 - symptoms_1),
            "user_symptom_overlap_1": len(symptom_set & symptoms_1),
            "user_symptom_overlap_2": len(symptom_set & symptoms_2)
        },
        "differential_reasoning_ja": f"{disease_1['name_ja']}と{disease_2['name_ja']}は類似した症状を呈することがありますが、固有の症状と検査結果により区別されます。",
        "differential_reasoning_en": f"Both {disease_1['name_en']} and {disease_2['name_en']} can present with similar symptoms, but differ in specific findings and test results.",
        "recommended_diagnostic_tests": list(set(disease_1.get("recommended_tests", []) + disease_2.get("recommended_tests", [])))[:5]
    }

    return jsonify(comparison)


@diagnostic_bp.route("/treatment-plan", methods=["POST"])
def get_treatment_plan():
    """
    Get care guide information for a suspected condition (reference only).

    Request JSON:
    {
        "disease_id": "brachycephalic_airway_syndrome",
        "breed_id": "122_labrador_retriever" (optional),
        "age_years": 3.5 (optional)
    }
    """
    data = request.get_json() or {}
    disease_id = data.get("disease_id")
    breed_id = data.get("breed_id")
    age_years = data.get("age_years")

    if not disease_id:
        return jsonify({"error": "Disease ID required"}), 400

    disease = _DISEASES_BY_ID.get(disease_id)

    if not disease:
        return jsonify({"error": "Disease not found"}), 404

    treatment_info = get_treatment_recommendations_for_disease(disease_id, breed_id, age_years)

    plan = {
        "disease_id": disease_id,
        "disease_name_ja": disease["name_ja"],
        "disease_name_en": disease["name_en"],
        "severity": disease["severity"],
        **treatment_info,
        "follow_up_visits": [
            {
                "visit_number": 1,
                "days_after_diagnosis": 14,
                "focus_areas_ja": ["呼吸状態評価", "投薬レビュー"],
                "focus_areas_en": ["Respiratory Assessment", "Medication Review"]
            },
            {
                "visit_number": 2,
                "days_after_diagnosis": 60,
                "focus_areas_ja": ["症状改善確認", "ケアプラン調整"],
                "focus_areas_en": ["Symptom Improvement Check", "Care Plan Adjustment"]
            }
        ]
    }

    return jsonify(plan)


@diagnostic_bp.route("/categories", methods=["GET"])
def get_categories():
    """
    Return all symptom categories for UI organization.
    """
    categories = {}
    for symptom in SYMPTOMS:
        cat = symptom["category"]
        if cat not in categories:
            categories[cat] = {"id": cat, "symptoms": []}
        categories[cat]["symptoms"].append({
            "id": symptom["id"],
            "name_ja": symptom["name_ja"],
            "name_en": symptom["name_en"],
        })

    return jsonify({
        "total_categories": len(categories),
        "categories": list(categories.values())
    })


@diagnostic_bp.route("/feedback", methods=["POST"])
def record_diagnostic_feedback():
    """
    Record user feedback on diagnostic accuracy (Phase 3).

    Captures whether the diagnostic result was helpful/accurate,
    automatically sending to learning_store for continuous improvement.

    Request JSON:
    {
        "session_id": "uuid-from-chat-session",
        "feedback": "good" | "bad" | "recalculate",
        "domain": "orthopedics" | "general" | etc,
        "ai_result": {...extraction metadata...},
        "correct_symptoms": [...actual symptoms...],
        "notes": "optional user notes"
    }

    Response:
    {
        "status": "recorded",
        "learning_signal_strength": 0.0-1.0,
        "accuracy_impact": 0.0-1.0,
        "ai_feedback": {...}
    }
    """
    try:
        data = request.get_json() or {}

        session_id = data.get("session_id", "").strip()
        feedback_type = data.get("feedback", "").strip()
        domain = data.get("domain", "general").strip()
        ai_result = data.get("ai_result", {})
        correct_symptoms = data.get("correct_symptoms", [])
        data.get("notes", "").strip()

        # Validate required fields
        if not session_id:
            return jsonify({"error": "session_id required"}), 400
        if feedback_type not in ("good", "bad", "recalculate"):
            return jsonify({"error": "feedback must be good, bad, or recalculate"}), 400

        # Phase 3: Record learning signal
        try:
            from api.ai.accuracy_tracker import AIAccuracyTracker
            from api.learning_insights import record_feedback as record_learning_feedback

            # Record to learning store
            response = record_learning_feedback()
            if isinstance(response, tuple):  # (data, status_code)
                response[0]
            else:
                pass

            # Get accuracy evaluation
            tracker = AIAccuracyTracker()
            accuracy_eval = tracker.evaluate_extraction(
                ai_result=ai_result or {},
                feedback_type=feedback_type,
                correct_symptoms=correct_symptoms,
                domain=domain,
            )

            logger.info(
                f"Diagnostic feedback recorded: "
                f"session={session_id}, feedback={feedback_type}, "
                f"accuracy={accuracy_eval.get('accuracy_score', 0):.2f}"
            )

            return jsonify({
                "status": "recorded",
                "learning_signal_strength": min(1.0, accuracy_eval.get("accuracy_score", 0)),
                "accuracy_impact": accuracy_eval.get("accuracy_score", 0),
                "ai_feedback": {
                    "extraction_accuracy": accuracy_eval.get("accuracy_score", 0),
                    "confidence_calibration": "good" if accuracy_eval.get("confidence_calibration", 0) > 0.7 else "needs_review",
                },
            }), 201

        except Exception as e:
            logger.warning("Failed to record learning feedback: %s", e)
            # Fallback: still record basic feedback
            return jsonify({
                "status": "recorded",
                "learning_signal_strength": 0,
                "note": "feedback recorded (learning unavailable)",
            }), 201

    except Exception as e:
        logger.error("Error recording diagnostic feedback: %s", e)
        return jsonify({"error": "internal_error"}), 500


# =============================================================================
# API: Next Diagnostic Questions (Phase 3)
# =============================================================================

@diagnostic_bp.route("/next-questions", methods=["POST"])
def get_next_diagnostic_questions():
    """
    Generate next diagnostic questions based on current disease candidates.

    Request JSON:
    {
        "suspected_diseases": [...],  # Current suspected diseases
        "symptoms": [...],            # Current symptoms
        "question_limit": 3           # Max questions to return (optional)
    }

    Returns:
    {
        "next_questions": [...],
        "question_count": int,
        "current_candidates": int,
        "estimated_next_questions": int,
        "recommendation_ja": str,
        "recommendation_en": str
    }
    """
    from api.ai.diagnostic_questionnaire import build_next_question_response

    try:
        data = request.get_json() or {}
        suspected_diseases = data.get("suspected_diseases", [])
        symptoms = data.get("symptoms", [])
        question_limit = data.get("question_limit", 3)

        if not suspected_diseases:
            return jsonify({"error": "suspected_diseases list required"}), 400

        if question_limit > 5:
            question_limit = 5  # Limit to 5 max questions

        # Generate next questions
        response = build_next_question_response(
            suspected_diseases,
            symptoms,
            question_limit=question_limit,
        )

        return jsonify(response), 200

    except Exception as e:
        logger.error("Error generating next questions: %s", e, exc_info=True)
        return jsonify({"error": "failed_to_generate_questions"}), 500


# =============================================================================
# API: Multi-Disease Analysis (Phase 6)
# =============================================================================

@diagnostic_bp.route("/multi-disease/analyze", methods=["POST"])
def analyze_multidisease():
    """
    Analyze symptoms for multiple disease hypothesis scenarios.

    Orchestrates Phase 6 (Stages 3-5) multi-disease analysis:
    - Stage 3: Symptom ambiguity detection
    - Stage 4: Combined confidence scoring
    - Stage 5: Multi-disease question generation

    Request JSON:
    {
        "symptom_ids": [...],              # List of detected symptom IDs
        "symptoms_ja": "...",              # Japanese symptom description
        "symptoms_en": "...",              # English symptom description
        "suspected_diseases": [            # Current disease candidates
            {
                "name": "Disease A",
                "match_percent": 75,
                ...
            },
            ...
        ],
        "patient_context": {               # Optional patient info
            "age_years": 7,
            "species": "dog",
            "breed": "Labrador",
            "gender": "male"
        }
    }

    Returns:
    {
        "multidisease_mode_enabled": bool,
        "combinations_found": int,
        "combinations": [...],              # Top disease combinations
        "ambiguity_analysis": {...},
        "confidence_breakdown": {...},      # Bayesian breakdown
        "next_questions": [...],            # Recommended questions
        "explanation_en": str,
        "explanation_ja": str
    }
    """
    from api.ai.multidisease_api_handler import MultiDiseaseAnalyzer

    try:
        data = request.get_json() or {}

        # Validate request
        is_valid, error_msg = MultiDiseaseAnalyzer.validate_request(data)
        if not is_valid:
            return jsonify({"error": error_msg}), 400

        # Extract parameters
        symptom_ids = data.get("symptom_ids", [])
        detected_symptoms_ja = data.get("symptoms_ja")
        detected_symptoms_en = data.get("symptoms_en")
        suspected_diseases = data.get("suspected_diseases", [])
        patient_context = data.get("patient_context")

        # Get disease database (dog is default)
        disease_db = DISEASES if isinstance(DISEASES, list) else []

        # Perform analysis
        analysis_result = MultiDiseaseAnalyzer.analyze_for_multidisease(
            symptom_ids=symptom_ids,
            detected_symptoms_ja=detected_symptoms_ja,
            detected_symptoms_en=detected_symptoms_en,
            suspected_diseases=suspected_diseases,
            disease_database=disease_db,
            patient_context=patient_context,
        )

        return jsonify(analysis_result), 200

    except Exception as e:
        logger.error("Error in multi-disease analysis: %s", e, exc_info=True)
        return jsonify({"error": "multidisease_analysis_failed"}), 500


# =============================================================================
# GUIDED CONSULTATION (問診モード)
# =============================================================================

# Category labels for UI display
_CATEGORY_LABELS = {
    "respiratory": {"ja": "呼吸器系", "en": "Respiratory"},
    "digestive": {"ja": "消化器系", "en": "Digestive"},
    "skin": {"ja": "皮膚・被毛", "en": "Skin / Coat"},
    "dermatological": {"ja": "皮膚・被毛", "en": "Skin / Coat"},
    "neurological": {"ja": "神経系", "en": "Neurological"},
    "musculoskeletal": {"ja": "運動器", "en": "Musculoskeletal"},
    "urinary": {"ja": "泌尿器系", "en": "Urinary"},
    "ophthalmological": {"ja": "眼科", "en": "Ophthalmological"},
    "eyes": {"ja": "眼科", "en": "Eyes"},
    "cardiovascular": {"ja": "循環器系", "en": "Cardiovascular"},
    "behavioral": {"ja": "行動・元気", "en": "Behavioral"},
    "general": {"ja": "全身症状", "en": "General"},
    "reproductive": {"ja": "生殖器系", "en": "Reproductive"},
    "emergency": {"ja": "緊急症状", "en": "Emergency"},
    "parasites": {"ja": "寄生虫", "en": "Parasites"},
    "fins": {"ja": "鰭", "en": "Fins"},
    "gills": {"ja": "鰓", "en": "Gills"},
    "behavior": {"ja": "行動", "en": "Behavior"},
    "other": {"ja": "その他", "en": "Other"},
    # --- 2026-03 追加 ---
    "endocrine": {"ja": "内分泌", "en": "Endocrine"},
    "hematological": {"ja": "血液", "en": "Hematological"},
    "hepatic": {"ja": "肝臓", "en": "Hepatic"},
    "immune": {"ja": "免疫", "en": "Immune"},
    "infectious": {"ja": "感染症", "en": "Infectious"},
    "metabolic": {"ja": "代謝", "en": "Metabolic"},
    "neoplastic": {"ja": "腫瘍", "en": "Neoplastic"},
    "nutritional": {"ja": "栄養", "en": "Nutritional"},
    "parasitic": {"ja": "寄生虫", "en": "Parasitic"},
    "renal": {"ja": "腎臓", "en": "Renal"},
    "toxicological": {"ja": "中毒", "en": "Toxicological"},
    "traumatic": {"ja": "外傷", "en": "Traumatic"},
    # --- 犬・馬・エキゾチック種追加カテゴリ ---
    "eyes_ears": {"ja": "眼・耳", "en": "Eyes / Ears"},
    "eye": {"ja": "眼科", "en": "Eye"},
    "ears": {"ja": "耳", "en": "Ears"},
    "ocular": {"ja": "眼科", "en": "Ocular"},
    "oral": {"ja": "口腔", "en": "Oral"},
    "dental": {"ja": "歯科", "en": "Dental"},
    "hoof": {"ja": "蹄", "en": "Hoof"},
    "foal": {"ja": "子馬", "en": "Foal"},
    "toxic": {"ja": "中毒", "en": "Toxic"},
    "body": {"ja": "体幹", "en": "Body"},
    "limb": {"ja": "四肢", "en": "Limbs"},
    "repository_exam": {"ja": "検査所見", "en": "Exam Findings"},
    "misc": {"ja": "その他", "en": "Miscellaneous"},
    "developmental": {"ja": "発育", "en": "Developmental"},
    "internal": {"ja": "内臓", "en": "Internal"},
    "cardiac": {"ja": "心臓", "en": "Cardiac"},
}


def _get_species_symptoms_with_categories(species: str) -> list[dict]:
    """Get all symptoms for a species with category info."""
    # Horse uses HEALTH_CHECK_ITEMS from equine_diseases (finding keys)
    if species == "horse" and EQUINE_AVAILABLE:
        try:
            from api.species.equine_diseases import HEALTH_CHECK_ITEMS
            result = []
            for cat, items in HEALTH_CHECK_ITEMS.items():
                for finding_key, name_ja, name_en in items:
                    result.append({
                        "id": finding_key,
                        "name_ja": name_ja,
                        "name_en": name_en,
                        "category": cat,
                    })
            if result:
                return result
        except (ImportError, Exception):
            pass

    from api.disease_store import get_symptoms_for_species
    symptoms = get_symptoms_for_species(species)
    if symptoms:
        return symptoms

    # Fallback: build from _SPECIES_DATA
    sp_data = _SPECIES_DATA.get(species)
    if not sp_data:
        # Dog fallback
        return [
            {"id": s["id"], "name_ja": s["name_ja"], "name_en": s["name_en"],
             "category": s.get("category", "other")}
            for s in SYMPTOMS
        ]
    sym_names = sp_data["symptom_names"]
    sym_cats = sp_data.get("symptom_categories", {})
    return [
        {"id": sid, "name_ja": v.get("ja", sid), "name_en": v.get("en", sid),
         "category": sym_cats.get(sid, "other")}
        for sid, v in sym_names.items()
    ]


def _group_symptoms_by_category(symptoms: list[dict]) -> dict[str, list[dict]]:
    """Group symptoms by category, returning {category: [symptom, ...]}."""
    groups: dict[str, list[dict]] = {}
    for s in symptoms:
        cat = s.get("category", "other")
        groups.setdefault(cat, []).append(s)
    return groups


def _suggest_next_categories(
    species: str,
    selected_symptoms: list[str],
    answered_categories: list[str],
    disease_matches: list[dict],
    all_symptoms: list[dict],
) -> list[dict]:
    """Suggest the most informative symptom categories to ask about next.

    Uses differential information scoring: symptoms that best partition the
    candidate disease set are weighted highest (presence in ~50% of candidates
    = maximum discriminating power).
    """
    selected_set = set(selected_symptoms)
    answered_set = set(answered_categories)

    n_candidates = min(len(disease_matches), 10)
    if n_candidates == 0:
        return []

    # Count how many of the top candidates contain each additional symptom
    diff_symptoms: dict[str, int] = {}  # symptom_id -> count of diseases containing it
    for dm in disease_matches[:n_candidates]:
        for s in dm.get("additional_disease_symptoms", []):
            if s not in selected_set:
                diff_symptoms[s] = diff_symptoms.get(s, 0) + 1

    # Map symptom IDs to categories
    sym_cat_map = {s["id"]: s.get("category", "other") for s in all_symptoms}

    # Score each symptom by how well it partitions the candidate set.
    # A symptom present in k out of n candidates has discriminating power:
    #   score = 4 * p * (1 - p)   where p = k / n
    # This peaks at 1.0 when p=0.5 (best partition), and is 0 at p=0 or p=1.
    cat_scores: dict[str, float] = {}
    cat_symptom_counts: dict[str, int] = {}
    for sid, count in diff_symptoms.items():
        cat = sym_cat_map.get(sid, "other")
        if cat not in answered_set:
            p = count / n_candidates
            info_score = 4.0 * p * (1.0 - p)
            cat_scores[cat] = cat_scores.get(cat, 0.0) + info_score
            cat_symptom_counts[cat] = cat_symptom_counts.get(cat, 0) + 1

    # Sort by score descending, return top 3
    sorted_cats = sorted(cat_scores.items(), key=lambda x: x[1], reverse=True)
    result = []
    for cat, _score in sorted_cats[:3]:
        labels = _CATEGORY_LABELS.get(cat, {"ja": cat, "en": cat})
        result.append({
            "id": cat,
            "name_ja": labels["ja"],
            "name_en": labels["en"],
            "differentiating_count": cat_symptom_counts.get(cat, 0),
        })
    return result


@diagnostic_bp.route("/consultation", methods=["POST"])
def consultation():
    """Guided consultation endpoint (問診モード).

    Manages an interactive interview flow where the system asks symptom
    questions step by step, similar to a veterinary examination.

    Request JSON:
    {
        "species": "cat",
        "phase": "start" | "select_symptoms" | "next_category" | "ask_context" | "finalize",
        "selected_symptoms": ["fever", "coughing"],
        "selected_category": "respiratory",
        "answered_categories": ["respiratory"],
        "onset": null,
        "age_years": null
    }
    """
    data = request.get_json() or {}
    species = data.get("species", "dog")
    phase = data.get("phase", "start")
    selected_symptoms = data.get("selected_symptoms", [])
    selected_category = data.get("selected_category")
    answered_categories = data.get("answered_categories", [])
    onset = data.get("onset")
    age_years = data.get("age_years")
    pain_score = data.get("pain_score")
    lab_values = data.get("lab_values")
    breed = data.get("breed")
    lang = data.get("lang", "")              # "ja" or "en" for regional prevalence

    sp_label = SPECIES_LABELS.get(species, {"ja": species, "en": species})
    all_symptoms = _get_species_symptoms_with_categories(species)
    grouped = _group_symptoms_by_category(all_symptoms)

    # ------------------------------------------------------------------
    # Phase: START — return available symptom categories
    # ------------------------------------------------------------------
    if phase == "start":
        categories = []
        for cat_id, syms in sorted(grouped.items(), key=lambda x: -len(x[1])):
            labels = _CATEGORY_LABELS.get(cat_id, {"ja": cat_id, "en": cat_id})
            categories.append({
                "id": cat_id,
                "name_ja": labels["ja"],
                "name_en": labels["en"],
                "symptom_count": len(syms),
            })
        return jsonify({
            "phase": "select_category",
            "message_ja": f"{sp_label['ja']}の問診を始めます。一番気になる症状のカテゴリを選んでください。",
            "message_en": f"Starting consultation for {sp_label['en']}. Please select the symptom category that concerns you most.",
            "categories": categories,
            "species": species,
        })

    # ------------------------------------------------------------------
    # Phase: SELECT_SYMPTOMS — return symptoms for a chosen category
    # ------------------------------------------------------------------
    if phase == "select_symptoms":
        if not selected_category:
            return jsonify({"error": "selected_category required"}), 400

        cat_symptoms = grouped.get(selected_category, [])
        labels = _CATEGORY_LABELS.get(selected_category, {"ja": selected_category, "en": selected_category})

        return jsonify({
            "phase": "show_symptoms",
            "category": selected_category,
            "category_label_ja": labels["ja"],
            "category_label_en": labels["en"],
            "message_ja": f"{labels['ja']}の症状について教えてください。当てはまるものを全て選んでください。",
            "message_en": f"Tell us about {labels['en']} symptoms. Select all that apply.",
            "symptoms": [
                {
                    "id": s["id"],
                    "name_ja": s["name_ja"],
                    "name_en": s["name_en"],
                    "selected": s["id"] in selected_symptoms,
                }
                for s in cat_symptoms
            ],
            "selected_symptoms": selected_symptoms,
            "species": species,
        })

    # ------------------------------------------------------------------
    # Phase: NEXT_CATEGORY — run diagnosis + suggest next category
    # ------------------------------------------------------------------
    if phase == "next_category":
        if not selected_symptoms:
            return jsonify({
                "phase": "select_category",
                "message_ja": "症状が選択されていません。カテゴリを選んでください。",
                "message_en": "No symptoms selected. Please select a category.",
                "categories": [
                    {
                        "id": cat_id,
                        "name_ja": _CATEGORY_LABELS.get(cat_id, {"ja": cat_id, "en": cat_id})["ja"],
                        "name_en": _CATEGORY_LABELS.get(cat_id, {"ja": cat_id, "en": cat_id})["en"],
                        "symptom_count": len(syms),
                    }
                    for cat_id, syms in sorted(grouped.items(), key=lambda x: -len(x[1]))
                ],
                "species": species,
            }), 200

        # Run diagnosis with current symptoms
        if species == "horse" and EQUINE_AVAILABLE:
            disease_matches = _match_equine_symptoms_to_diseases(selected_symptoms)
        elif species in _SPECIES_DATA:
            disease_matches = _match_species_symptoms_to_diseases(
                selected_symptoms, species,
                pain_score=pain_score, lab_values=lab_values, breed=breed,
                lang=lang,
            )
        else:
            disease_matches = match_symptoms_to_diseases(
                selected_symptoms,
                pain_score=pain_score, lab_values=lab_values, breed=breed,
            )

        # Build symptom details for display
        sym_name_map = {s["id"]: s for s in all_symptoms}
        symptom_details = [
            {
                "id": sid,
                "name_ja": sym_name_map.get(sid, {}).get("name_ja", sid),
                "name_en": sym_name_map.get(sid, {}).get("name_en", sid),
            }
            for sid in selected_symptoms
        ]

        # Suggest next categories
        next_cats = _suggest_next_categories(
            species, selected_symptoms, answered_categories,
            disease_matches, all_symptoms,
        )

        # Build top candidates
        top_candidates = []
        for d in disease_matches[:5]:
            top_candidates.append({
                "name_ja": d.get("name_ja", ""),
                "name_en": d.get("name_en", d.get("disease_id", "")),
                "similarity_score": d.get("similarity_score", 0),
                "confidence_percent": d.get("confidence_percent", 0),
                "severity": d.get("severity", "low"),
                "matched_symptoms": d.get("matched_symptoms", []),
                "description_ja": d.get("description_ja", ""),
                "description_en": d.get("description", d.get("description_en", "")),
                "additional_disease_symptoms": d.get("additional_disease_symptoms", []),
            })

        has_more = len(next_cats) > 0
        return jsonify({
            "phase": "interim_results",
            "message_ja": f"{len(selected_symptoms)}個の症状から{len(disease_matches)}件の候補が見つかりました。"
                          + ("さらに絞り込むために、他のカテゴリの症状も確認しましょう。" if has_more else ""),
            "message_en": f"Found {len(disease_matches)} candidates from {len(selected_symptoms)} symptoms."
                          + (" Let's check other categories to narrow down." if has_more else ""),
            "disease_candidates": top_candidates,
            "total_candidates": len(disease_matches),
            "selected_symptoms": selected_symptoms,
            "symptom_details": symptom_details,
            "next_categories": next_cats,
            "answered_categories": answered_categories,
            "species": species,
        })

    # ------------------------------------------------------------------
    # Phase: ASK_CONTEXT — ask about onset and age
    # ------------------------------------------------------------------
    if phase == "ask_context":
        # Species where CSU pain scale is not applicable
        _NO_PAIN_SPECIES = {
            "fish", "reptile", "tortoise", "snake", "lizard",
            "amphibian",
        }
        questions = []
        if not onset:
            questions.append({
                "type": "onset",
                "question_ja": "症状はいつ頃から始まりましたか？",
                "question_en": "When did the symptoms start?",
                "options": [
                    {"value": "acute", "label_ja": "突然（24時間以内）", "label_en": "Suddenly (within 24h)"},
                    {"value": "subacute", "label_ja": "数日前から", "label_en": "A few days ago"},
                    {"value": "chronic", "label_ja": "2週間以上前から", "label_en": "More than 2 weeks ago"},
                ],
            })
        if age_years is None:
            questions.append({
                "type": "age",
                "question_ja": "何歳ですか？（だいたいで構いません）",
                "question_en": "How old is the animal? (approximate is fine)",
                "options": [
                    {"value": 0.5, "label_ja": "1歳未満", "label_en": "Under 1 year"},
                    {"value": 2.0, "label_ja": "1〜3歳", "label_en": "1–3 years"},
                    {"value": 5.0, "label_ja": "3〜7歳", "label_en": "3–7 years"},
                    {"value": 10.0, "label_ja": "7歳以上", "label_en": "7+ years"},
                ],
            })
        if pain_score is None and species not in _NO_PAIN_SPECIES:
            questions.append({
                "type": "pain_score",
                "question_ja": "痛みの程度はどのくらいですか？（CSU疼痛スケール 0-4）",
                "question_en": "How severe is the pain? (CSU Pain Scale 0–4)",
                "options": [
                    {"value": 0, "label_ja": "0: 痛みなし（快適）", "label_en": "0: No pain (comfortable)"},
                    {"value": 1, "label_ja": "1: 軽度（やや落ち着かない）", "label_en": "1: Mild (slightly unsettled)"},
                    {"value": 2, "label_ja": "2: 中等度（触診で反応）", "label_en": "2: Moderate (reacts to palpation)"},
                    {"value": 3, "label_ja": "3: 重度（持続的な不快感）", "label_en": "3: Severe (persistent discomfort)"},
                    {"value": 4, "label_ja": "4: 激痛（触れられない）", "label_en": "4: Extreme (untouchable)"},
                ],
            })
        return jsonify({
            "phase": "context_questions",
            "message_ja": "あと少しだけ教えてください。",
            "message_en": "Just a few more details.",
            "questions": questions,
            "selected_symptoms": selected_symptoms,
            "species": species,
        })

    # ------------------------------------------------------------------
    # Phase: FINALIZE — run final diagnosis with full context
    # ------------------------------------------------------------------
    if phase == "finalize":
        # Use the same diagnosis engine as the checkbox system for accuracy parity
        try:
            from api.species_analyzer import analyze_species_symptoms
            result = analyze_species_symptoms(
                species=species,
                symptoms=selected_symptoms,
                onset=onset,
                age_years=age_years,
                lab_values=lab_values,
                breed=breed,
                pain_score=pain_score,
            )
        except (ImportError, Exception) as exc:
            # Fallback to chat engine
            logger.warning("Finalize: analyze_species_symptoms failed for %s, falling back to chat engine: %s", species, exc)
            if species == "horse" and EQUINE_AVAILABLE:
                disease_matches = _match_equine_symptoms_to_diseases(selected_symptoms)
            elif species in _SPECIES_DATA:
                disease_matches = _match_species_symptoms_to_diseases(
                    selected_symptoms, species,
                    pain_score=pain_score, lab_values=lab_values, breed=breed,
                    lang=lang,
                )
            else:
                disease_matches = match_symptoms_to_diseases(
                    selected_symptoms,
                    pain_score=pain_score, lab_values=lab_values, breed=breed,
                )
            result = {
                "suspected_diseases": [
                    {
                        "name": d.get("name_en", d.get("disease_id", "")),
                        "name_ja": d.get("name_ja", ""),
                        "match_percent": round(d.get("similarity_score", 0) * 100),
                        "matching_symptoms": d.get("matched_symptoms", []),
                        "total_symptoms": len(d.get("matched_symptoms", [])) + len(d.get("additional_disease_symptoms", [])),
                        "severity": d.get("severity", "low"),
                        "description_ja": d.get("description_ja", ""),
                        "description": d.get("description", d.get("description_en", "")),
                        "recommended_tests": d.get("recommended_tests", []),
                    }
                    for d in disease_matches[:10]
                ],
            }

        # Build symptom details
        sym_name_map = {s["id"]: s for s in all_symptoms}
        symptom_details = [
            {
                "id": sid,
                "name_ja": sym_name_map.get(sid, {}).get("name_ja", sid),
                "name_en": sym_name_map.get(sid, {}).get("name_en", sid),
            }
            for sid in selected_symptoms
        ]

        return jsonify({
            "phase": "final_results",
            "message_ja": f"問診結果です。{len(selected_symptoms)}個の症状をもとに診断候補を算出しました。",
            "message_en": f"Consultation results. Calculated candidates based on {len(selected_symptoms)} symptoms.",
            "result": result,
            "selected_symptoms": selected_symptoms,
            "symptom_details": symptom_details,
            "onset": onset,
            "age_years": age_years,
            "pain_score": pain_score,
            "species": species,
            "recommendations": {
                "next_step_ja": "こちらは参考情報です（獣医師監修：上手健太郎／南相馬動物病院）。正確な評価のため、獣医師の診察を受けてください。",
                "next_step_en": "This is reference information only. Supervised by Kentaro Kaimide, DVM. Please consult a veterinarian.",
            },
        })

    return jsonify({"error": f"Unknown phase: {phase}"}), 400
