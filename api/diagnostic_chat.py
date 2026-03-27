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
from typing import Any, Dict, Optional

from flask import Blueprint, jsonify, request

logger = logging.getLogger(__name__)

diagnostic_bp = Blueprint("diagnostic_bp", __name__, url_prefix="/api/diagnostic-chat")

# Import health checker data (dog - default)
try:
    from api.health_checker import DISEASES, SYMPTOM_IDS, SYMPTOMS
except ImportError:
    from health_checker import DISEASES, SYMPTOM_IDS, SYMPTOMS

# AI-powered symptom extraction (Phase 1)
_AI_EXTRACTION_ENABLED = os.getenv("VETDICT_USE_AI_SYMPTOM_EXTRACTION", "false").lower() == "true"
_AI_EXTRACTOR = None

def _get_ai_extractor():
    """Lazy-load AI extractor singleton."""
    global _AI_EXTRACTOR
    if _AI_EXTRACTOR is None and _AI_EXTRACTION_ENABLED:
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

            _AI_EXTRACTOR = SymptomExtractor(
                api_key=os.getenv("ANTHROPIC_API_KEY"),
                model=ai_model,
                timeout=ai_timeout,
                cache_enabled=True,
                cache_ttl=ai_cache_ttl,
                confidence_threshold=ai_confidence,
                fallback_enabled=ai_fallback,
                manual_aliases=SYMPTOM_ALIASES if 'SYMPTOM_ALIASES' in globals() else {},
            )
            _AI_EXTRACTOR.set_valid_symptom_ids(SYMPTOM_IDS)
            logger.info(f"AI symptom extractor initialized (model={ai_model}, timeout={ai_timeout}s)")
        except Exception as e:
            logger.warning(f"Failed to initialize AI extractor: {e}")
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
        logger.debug(f"RECO2 evaluation failed, skipping: {e}")
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

# Import generic species modules for multi-species chat support
import importlib as _importlib

_GENERIC_SPECIES = [
    "cat", "rabbit", "hamster", "chinchilla", "guinea_pig", "ferret",
    "hedgehog", "sugar_glider", "degu", "bird", "parakeet", "parrot",
    "reptile", "tortoise", "snake", "lizard", "amphibian", "fish",
    "exotic_other",
]
_SPECIES_DATA: dict = {}  # {species: {"diseases": [...], "symptom_names": {...}}}

SPECIES_LABELS = {
    "dog": {"ja": "犬", "en": "Dog"},
    "cat": {"ja": "猫", "en": "Cat"},
    "horse": {"ja": "馬", "en": "Horse"},
    "rabbit": {"ja": "ウサギ", "en": "Rabbit"},
    "hamster": {"ja": "ハムスター", "en": "Hamster"},
    "chinchilla": {"ja": "チンチラ", "en": "Chinchilla"},
    "guinea_pig": {"ja": "モルモット", "en": "Guinea Pig"},
    "ferret": {"ja": "フェレット", "en": "Ferret"},
    "hedgehog": {"ja": "ハリネズミ", "en": "Hedgehog"},
    "sugar_glider": {"ja": "フクロモモンガ", "en": "Sugar Glider"},
    "degu": {"ja": "デグー", "en": "Degu"},
    "bird": {"ja": "鳥", "en": "Bird"},
    "parakeet": {"ja": "インコ", "en": "Parakeet"},
    "parrot": {"ja": "オウム", "en": "Parrot"},
    "reptile": {"ja": "爬虫類", "en": "Reptile"},
    "tortoise": {"ja": "リクガメ", "en": "Tortoise"},
    "snake": {"ja": "ヘビ", "en": "Snake"},
    "lizard": {"ja": "トカゲ", "en": "Lizard"},
    "amphibian": {"ja": "両生類", "en": "Amphibian"},
    "fish": {"ja": "魚", "en": "Fish"},
    "exotic_other": {"ja": "その他エキゾチック", "en": "Other Exotic"},
}

for _sp in _GENERIC_SPECIES:
    try:
        _mod = _importlib.import_module(f"api.species.{_sp}_diseases")
    except ImportError:
        try:
            _mod = _importlib.import_module(f"species.{_sp}_diseases")
        except ImportError:
            continue
    _SPECIES_DATA[_sp] = {
        "diseases": _mod.DISEASES,
        "symptom_names": _mod.SYMPTOM_NAMES,
    }

# =============================================================================
# SYMPTOM ALIASES (natural language matching)
# =============================================================================

SYMPTOM_ALIASES = {
    # English variants
    "cough": "coughing",
    "coughs": "coughing",
    "coughing": "coughing",
    "sneeze": "sneezing",
    "sneezes": "sneezing",
    "sneezing": "sneezing",
    "runny nose": "nasal_discharge",
    "nasal discharge": "nasal_discharge",
    "discharge": "nasal_discharge",
    "breathing difficulty": "labored_breathing",
    "breathing problems": "labored_breathing",
    "labored breathing": "labored_breathing",
    "gasping": "labored_breathing",
    "reverse sneeze": "reverse_sneezing",
    "reverse sneezing": "reverse_sneezing",
    "wheeze": "wheezing",
    "wheezing": "wheezing",
    "vomit": "vomiting",
    "vomiting": "vomiting",
    "throw up": "vomiting",
    "throws up": "vomiting",
    "diarrhea": "diarrhea",
    "diarrhoea": "diarrhea",
    "loose stool": "diarrhea",
    "loose stools": "diarrhea",
    "no appetite": "loss_of_appetite",
    "loss of appetite": "loss_of_appetite",
    "not eating": "loss_of_appetite",
    "anorexia": "loss_of_appetite",
    "drool": "excessive_drooling",
    "drooling": "excessive_drooling",
    "excessive drool": "excessive_drooling",
    "bloat": "bloating",
    "bloating": "bloating",
    "abdominal distension": "bloating",
    "constipation": "constipation",
    "not pooping": "constipation",
    "blood in stool": "blood_in_stool",
    "bloody stool": "blood_in_stool",
    "bloody diarrhea": "blood_in_stool",
    "seizure": "seizures",
    "seizures": "seizures",
    "fits": "seizures",
    "convulsion": "seizures",
    "limping": "lameness_or_limping",
    "lameness": "lameness_or_limping",
    "lame": "lameness_or_limping",
    "leg pain": "lameness_or_limping",
    "swelling": "lameness_or_limping",
    "joint pain": "joint_pain_or_stiffness",
    "joint stiffness": "joint_pain_or_stiffness",
    "stiff": "joint_pain_or_stiffness",
    "arthritis": "joint_pain_or_stiffness",
    "tremor": "tremors",
    "tremors": "tremors",
    "shaking": "tremors",
    "shakes": "tremors",
    "paralysis": "paralysis_or_paresis",
    "paresis": "paralysis_or_paresis",
    "paralyzed": "paralysis_or_paresis",
    "can't move": "paralysis_or_paresis",
    "lump": "lumps_and_bumps",
    "lumps": "lumps_and_bumps",
    "bump": "lumps_and_bumps",
    "lumpy": "lumps_and_bumps",
    "pee frequently": "frequent_urination",
    "frequent urination": "frequent_urination",
    "peeing a lot": "frequent_urination",
    "polyuria": "frequent_urination",
    "blood in urine": "blood_in_urine",
    "bloody urine": "blood_in_urine",
    "red urine": "blood_in_urine",
    "hematuria": "blood_in_urine",
    "straining to pee": "straining_to_urinate",
    "straining to urinate": "straining_to_urinate",
    "difficult urination": "straining_to_urinate",
    "incontinence": "incontinence",
    "incontinent": "incontinence",
    "peeing in house": "incontinence",
    "leaking urine": "incontinence",
    "drinking a lot": "excessive_thirst",
    "excessive thirst": "excessive_thirst",
    "polydipsia": "excessive_thirst",
    "eye discharge": "eye_discharge",
    "eye gunk": "eye_discharge",
    "discharge from eyes": "eye_discharge",
    "red eyes": "redness_in_eyes",
    "eye redness": "redness_in_eyes",
    "redness in eyes": "redness_in_eyes",
    "conjunctivitis": "redness_in_eyes",
    "cloudy eyes": "cloudiness_in_eyes",
    "cloudiness in eyes": "cloudiness_in_eyes",
    "eye cloudiness": "cloudiness_in_eyes",
    "cataracts": "cloudiness_in_eyes",
    "squinting": "squinting",
    "squint": "squinting",
    "eye swelling": "eye_swelling",
    "swollen eyes": "eye_swelling",
    "eyes puffed up": "eye_swelling",
    "exercise intolerance": "exercise_intolerance",
    "can't exercise": "exercise_intolerance",
    "tires easily": "exercise_intolerance",
    "tired": "exercise_intolerance",
    "fainting": "fainting",
    "faints": "fainting",
    "syncope": "fainting",
    "collapses": "fainting",
    "fast breathing": "rapid_breathing",
    "rapid breathing": "rapid_breathing",
    "tachypnea": "rapid_breathing",
    "panting": "rapid_breathing",
    "lethargy": "lethargy",
    "lethargic": "lethargy",
    "depression": "lethargy",
    "sluggish": "lethargy",
    "no energy": "lethargy",
    "aggression": "aggression",
    "aggressive": "aggression",
    "irritability": "aggression",
    "irritable": "aggression",
    "anxiety": "anxiety",
    "anxious": "anxiety",
    "restlessness": "anxiety",
    "restless": "anxiety",
    "nervous": "anxiety",
    "excessive licking": "excessive_licking",
    "licking": "excessive_licking",
    "licks": "excessive_licking",
    "lick dermatitis": "excessive_licking",
    "fever": "fever",
    "high temperature": "fever",
    "pyrexia": "fever",
    "hot": "fever",
    "weight loss": "weight_loss",
    "losing weight": "weight_loss",
    "thin": "weight_loss",
    "swollen lymph nodes": "swollen_lymph_nodes",
    "lymphadenopathy": "swollen_lymph_nodes",
    "lymph node swelling": "swollen_lymph_nodes",
    "bumps under skin": "swollen_lymph_nodes",
    "pale gums": "pale_gums",
    "gum color pale": "pale_gums",
    "pallor": "pale_gums",
    "pale": "pale_gums",
    "jaundice": "jaundice",
    "yellowing": "jaundice",
    "yellow gums": "jaundice",
    "yellow skin": "jaundice",
    "icterus": "jaundice",
    # Japanese entries - formal/medical
    "咳": "coughing",
    "くしゃみ": "sneezing",
    "鼻水": "nasal_discharge",
    "呼吸困難": "labored_breathing",
    "逆くしゃみ": "reverse_sneezing",
    "喘鳴": "wheezing",
    "嘔吐": "vomiting",
    "下痢": "diarrhea",
    "食欲不振": "loss_of_appetite",
    "よだれ": "excessive_drooling",
    "腹部膨満": "bloating",
    "便秘": "constipation",
    "血便": "blood_in_stool",
    "けいれん": "seizures",
    "発作": "seizures",
    "跛行": "lameness_or_limping",
    "関節痛": "joint_pain_or_stiffness",
    "振戦": "tremors",
    "麻痺": "paralysis_or_paresis",
    "しこり": "lumps_and_bumps",
    "頻尿": "frequent_urination",
    "血尿": "blood_in_urine",
    "排尿困難": "straining_to_urinate",
    "尿失禁": "incontinence",
    "多飲": "excessive_thirst",
    "目やに": "eye_discharge",
    "目の充血": "redness_in_eyes",
    "目の白濁": "cloudiness_in_eyes",
    "目を細める": "squinting",
    "目の腫れ": "eye_swelling",
    "運動不耐性": "exercise_intolerance",
    "失神": "fainting",
    "頻呼吸": "rapid_breathing",
    "無気力": "lethargy",
    "攻撃性": "aggression",
    "不安行動": "anxiety",
    "舐め行動": "excessive_licking",
    "発熱": "fever",
    "体重減少": "weight_loss",
    "リンパ節腫脹": "swollen_lymph_nodes",
    "歯茎の蒼白": "pale_gums",
    "黄疸": "jaundice",
    # ---------------------------------------------------------------
    # 曖昧・口語表現 (colloquial/ambiguous Japanese expressions)
    # ---------------------------------------------------------------
    # 全身状態
    "元気がない": "lethargy",
    "元気がなく": "lethargy",
    "元気ない": "lethargy",
    "元気なくなった": "lethargy",
    "元気なく": "lethargy",
    "ぐったり": "lethargy",
    "ぐったりしてる": "lethargy",
    "ぐたっとしてる": "lethargy",
    "だるそう": "lethargy",
    "しんどそう": "lethargy",
    "動かない": "lethargy",
    "動きたがらない": "lethargy",
    "寝てばかり": "lethargy",
    "寝てばっかり": "lethargy",
    "起きない": "lethargy",
    "起きてこない": "lethargy",
    "おとなしい": "lethargy",
    "なんか変": "lethargy",
    "具合悪そう": "lethargy",
    "具合が悪い": "lethargy",
    "調子悪い": "lethargy",
    "調子が悪い": "lethargy",
    "様子がおかしい": "lethargy",
    "おかしい": "lethargy",
    "いつもと違う": "lethargy",
    "活気がない": "lethargy",
    "沈鬱": "lethargy",
    # 食欲
    "食べない": "loss_of_appetite",
    "食べなくなった": "loss_of_appetite",
    "ご飯食べない": "loss_of_appetite",
    "ごはん食べない": "loss_of_appetite",
    "ご飯を食べない": "loss_of_appetite",
    "エサ食べない": "loss_of_appetite",
    "えさ食べない": "loss_of_appetite",
    "食が細い": "loss_of_appetite",
    "食欲がない": "loss_of_appetite",
    "食欲もない": "loss_of_appetite",
    "食欲なく": "loss_of_appetite",
    "食欲ない": "loss_of_appetite",
    "食欲減退": "loss_of_appetite",
    "食欲なくなった": "loss_of_appetite",
    "食べる量が減った": "loss_of_appetite",
    "フードを残す": "loss_of_appetite",
    "おやつしか食べない": "loss_of_appetite",
    # 嘔吐
    "吐いた": "vomiting",
    "吐く": "vomiting",
    "吐いてる": "vomiting",
    "吐き気": "vomiting",
    "戻した": "vomiting",
    "もどした": "vomiting",
    "ゲロ": "vomiting",
    "げろ": "vomiting",
    "吐き戻し": "vomiting",
    "何回も吐く": "vomiting",
    "何度も吐く": "vomiting",
    "食べた後吐く": "vomiting",
    "草食べて吐く": "vomiting",
    "黄色い液を吐く": "vomiting",
    "白い泡を吐く": "vomiting",
    # 下痢
    "うんちがゆるい": "diarrhea",
    "軟便": "diarrhea",
    "水っぽいうんち": "diarrhea",
    "水様便": "diarrhea",
    "おなか壊した": "diarrhea",
    "お腹壊した": "diarrhea",
    "お腹こわした": "diarrhea",
    "お腹をこわした": "diarrhea",
    "ベタベタのうんち": "diarrhea",
    "ゆるいうんち": "diarrhea",
    "下痢してる": "diarrhea",
    "下痢気味": "diarrhea",
    "うんちの回数が多い": "diarrhea",
    # 便秘
    "うんちが出ない": "constipation",
    "うんちしない": "constipation",
    "排便しない": "constipation",
    "うんち出ない": "constipation",
    "いきんでる": "constipation",
    "いきんでいる": "constipation",
    "踏ん張ってる": "constipation",
    # 血便
    "うんちに血": "blood_in_stool",
    "血が混じったうんち": "blood_in_stool",
    "赤いうんち": "blood_in_stool",
    "黒いうんち": "blood_in_stool",
    "タール便": "blood_in_stool",
    # 咳
    "咳が出る": "coughing",
    "咳してる": "coughing",
    "咳する": "coughing",
    "せきする": "coughing",
    "せき": "coughing",
    "えずく": "coughing",
    "ケッケッ": "coughing",
    "ゲホゲホ": "coughing",
    "ガーガー": "coughing",
    "変な咳": "coughing",
    "乾いた咳": "coughing",
    "湿った咳": "coughing",
    # 呼吸
    "息が荒い": "rapid_breathing",
    "ハアハア": "rapid_breathing",
    "はあはあ": "rapid_breathing",
    "ゼーゼー": "wheezing",
    "ぜーぜー": "wheezing",
    "息苦しそう": "labored_breathing",
    "呼吸が辛そう": "labored_breathing",
    "呼吸がつらそう": "labored_breathing",
    "呼吸が早い": "rapid_breathing",
    "呼吸が荒い": "labored_breathing", "呼吸が苦しそう": "labored_breathing",
    "口で息してる": "labored_breathing",
    "口呼吸": "labored_breathing",
    "開口呼吸": "labored_breathing",
    # 鼻
    "鼻が出てる": "nasal_discharge",
    "鼻が詰まってる": "nasal_discharge",
    "鼻づまり": "nasal_discharge",
    "鼻汁": "nasal_discharge",
    "青っ鼻": "nasal_discharge",
    # くしゃみ
    "くしゃみする": "sneezing",
    "くしゃみが止まらない": "sneezing",
    "くしゃみが多い": "sneezing",
    # 水を飲む
    "水をたくさん飲む": "excessive_thirst",
    "水ばっかり飲む": "excessive_thirst",
    "水飲みすぎ": "excessive_thirst",
    "よく水を飲む": "excessive_thirst",
    "水をよく飲む": "excessive_thirst",
    "水がぶ飲み": "excessive_thirst",
    "多飲多尿": "excessive_thirst",
    # 排尿
    "おしっこの回数が多い": "frequent_urination",
    "おしっこが多い": "frequent_urination",
    "何度もトイレに行く": "frequent_urination",
    "トイレが近い": "frequent_urination",
    "おしっこが出にくい": "straining_to_urinate",
    "おしっこが出ない": "straining_to_urinate",
    "おしっこ出ない": "straining_to_urinate",
    "おしっこに血": "blood_in_urine",
    "ピンクのおしっこ": "blood_in_urine",
    "赤いおしっこ": "blood_in_urine",
    "おしっこ漏れ": "incontinence",
    "おもらし": "incontinence",
    # 体重
    "痩せた": "weight_loss",
    "痩せてきた": "weight_loss",
    "やせた": "weight_loss",
    "やせてきた": "weight_loss",
    "ガリガリ": "weight_loss",
    "肋骨が見える": "weight_loss",
    "あばらが見える": "weight_loss",
    # 足・歩行
    "足を引きずる": "lameness_or_limping",
    "足をひきずる": "lameness_or_limping",
    "びっこ": "lameness_or_limping",
    "足をかばう": "lameness_or_limping",
    "足を上げてる": "lameness_or_limping",
    "歩き方がおかしい": "lameness_or_limping",
    "歩けない": "lameness_or_limping",
    "立てない": "lameness_or_limping",
    "足が痛そう": "lameness_or_limping",
    "ふらふら": "ataxia",
    "フラフラ": "tremors",
    "ふらつき": "tremors",
    "よろよろ": "tremors",
    "ヨロヨロ": "tremors",
    "ふるえてる": "tremors",
    "震えてる": "tremors",
    "ブルブル": "tremors",
    "ぶるぶる": "tremors",
    "ガクガク": "tremors",
    # 発作・痙攣
    "ひきつけ": "seizures",
    "痙攣": "seizures",
    "ピクピク": "seizures",
    "バタバタ": "seizures",
    "白目向いてる": "seizures",
    "泡吹いてる": "seizures",
    "意識がない": "seizures",
    "意識ない": "seizures",
    "倒れた": "collapse",
    "倒れる": "collapse",
    "気絶": "collapse",
    # 皮膚
    "かゆい": "excessive_licking",
    "痒い": "excessive_licking",
    "かゆがる": "excessive_licking",
    "痒がる": "excessive_licking",
    "掻いてる": "excessive_licking",
    "かいてる": "excessive_licking",
    "しきりに舐める": "excessive_licking",
    "体を掻く": "excessive_licking",
    "できもの": "lumps_and_bumps",
    "しこりがある": "lumps_and_bumps",
    "できものがある": "lumps_and_bumps",
    "腫瘍": "lumps_and_bumps",
    "ふくらみ": "lumps_and_bumps",
    "膨らんでる": "bloating",
    "腫れてる": "bloating",
    "お腹が張ってる": "bloating",
    "おなかが膨れてる": "bloating",
    "お腹パンパン": "bloating",
    # 目
    "目が赤い": "redness_in_eyes",
    "目が白い": "cloudiness_in_eyes",
    "目が白くなった": "cloudiness_in_eyes",
    "目が曇ってる": "cloudiness_in_eyes",
    "目がしょぼしょぼ": "squinting",
    "涙が出る": "eye_discharge",
    "涙が多い": "eye_discharge",
    "涙目": "eye_discharge",
    "目が腫れてる": "eye_swelling",
    "まぶたが腫れてる": "eye_swelling",
    # よだれ
    "よだれが多い": "excessive_drooling",
    "よだれダラダラ": "excessive_drooling",
    "口からよだれ": "excessive_drooling",
    "涎": "excessive_drooling",
    # 発熱
    "熱がある": "fever",
    "熱っぽい": "fever",
    "体が熱い": "fever",
    "触ると熱い": "fever",
    "鼻が乾いてる": "fever",
    "耳が熱い": "fever",
    # 行動
    "噛みつく": "aggression",
    "唸る": "aggression",
    "怒りっぽい": "aggression",
    "攻撃的": "aggression",
    "落ち着かない": "anxiety",
    "落ち着きがない": "anxiety",
    "ウロウロ": "anxiety",
    "うろうろ": "anxiety",
    "そわそわ": "anxiety",
    "ソワソワ": "anxiety",
    "夜鳴き": "anxiety",
    "夜泣き": "anxiety",
    "怖がる": "anxiety",
    # その他
    "脱水": "excessive_thirst",
    "肌が黄色い": "jaundice",
    "白目が黄色い": "jaundice",
    "歯茎が白い": "pale_gums",
    "歯茎が蒼白": "pale_gums",
    "リンパが腫れてる": "swollen_lymph_nodes",
    "しこりが首にある": "swollen_lymph_nodes",
    "首が腫れてる": "swollen_lymph_nodes",
    "すぐ疲れる": "exercise_intolerance",
    "散歩行きたがらない": "exercise_intolerance",
    "散歩嫌がる": "exercise_intolerance",
    "運動嫌がる": "exercise_intolerance",
    "すぐバテる": "exercise_intolerance",
    "息切れ": "exercise_intolerance",
    # ---------------------------------------------------------------
    # 魚病用エイリアス (Fish disease aliases)
    # ---------------------------------------------------------------
    # 白点病
    "白い点": "white_spots", "白点": "white_spots", "白い斑点": "white_spots",
    "白い点々": "white_spots", "白いぶつぶつ": "white_spots",
    "ich": "white_spots", "white spot": "white_spots", "white dots": "white_spots",
    # 綿状付着物・水カビ
    "綿みたい": "cotton_like_growth", "綿状": "cotton_like_growth",
    "白いもやもや": "cotton_like_growth", "白いふわふわ": "cotton_like_growth",
    "カビ": "cotton_like_growth", "水カビ": "cotton_like_growth",
    "cotton": "cotton_like_growth", "fungus": "cotton_like_growth",
    # 鰭
    "ヒレがボロボロ": "fin_rot", "ひれがぼろぼろ": "fin_rot",
    "尾ぐされ": "fin_rot", "鰭が溶ける": "fin_rot", "ヒレが溶ける": "fin_rot",
    "fin rot": "fin_rot", "tail rot": "fin_rot",
    "ヒレをたたむ": "clamped_fins", "ひれをたたむ": "clamped_fins",
    "ヒレが閉じてる": "clamped_fins", "鰭をたたむ": "clamped_fins",
    "clamped fins": "clamped_fins",
    "ヒレが赤い": "fin_hemorrhage", "ヒレの充血": "fin_hemorrhage",
    # 体表
    "鱗が逆立つ": "raised_scales", "松かさ": "raised_scales",
    "鱗が逆立ってる": "raised_scales", "うろこが逆立ってる": "raised_scales",
    "お腹が膨れてきた": "bloating", "お腹膨れてる": "bloating",
    "目が飛び出してる": "pop_eye",
    "まつかさ": "raised_scales", "マツカサ": "raised_scales",
    "鱗が立ってる": "raised_scales", "うろこが逆立つ": "raised_scales",
    "pinecone": "raised_scales", "dropsy": "dropsy",
    "お腹が膨れてる": "bloating", "腹が膨れてる": "bloating",
    "体が膨らんでる": "bloating", "膨満": "bloating",
    "ただれ": "ulcers", "潰瘍": "ulcers",
    "穴が開いてる": "ulcers", "穴あき": "ulcers",
    "赤くなってる": "redness_skin", "充血": "redness_skin",
    "出血してる": "redness_skin", "赤い斑点": "redness_skin",
    "粘液": "mucus_overproduction", "ぬめり": "mucus_overproduction",
    "ヌルヌル": "mucus_overproduction",
    "色が薄くなった": "discoloration", "退色": "discoloration",
    "色が変わった": "discoloration",
    "体が黒くなった": "dark_coloration", "黒ずんでる": "dark_coloration",
    "コショウ病": "gold_dust", "金粉": "gold_dust",
    "金色の粉": "gold_dust", "velvet": "gold_dust",
    # 眼（魚用 — dog用と重複しない表現のみ）
    "目が飛び出てる": "pop_eye", "目が出てる": "pop_eye",
    "ポップアイ": "pop_eye", "pop eye": "pop_eye",
    "目が白く濁ってる": "cloudy_eye",
    # 鰓
    "エラが赤い": "gill_redness", "鰓が赤い": "gill_redness",
    "エラが白い": "gill_paleness", "鰓が白い": "gill_paleness",
    "エラが腫れてる": "gill_swelling",
    "エラの動きが速い": "rapid_gill_movement", "鰓蓋パタパタ": "rapid_gill_movement",
    "エラをパタパタ": "rapid_gill_movement",
    # 行動（魚用 — dog用と重複しない表現のみ）
    "体を擦りつける": "flashing", "擦りつけ": "flashing",
    "底石にこすりつける": "flashing", "フラッシング": "flashing",
    "flashing": "flashing", "scratching": "flashing",
    "底にじっとしてる": "lethargy", "じっとしてる": "lethargy",
    "じっとしてて": "lethargy",
    "沈んでる": "lethargy",
    "パクパク": "gasping_surface", "鼻上げ": "gasping_surface",
    "水面でパクパク": "gasping_surface", "水面に上がってくる": "gasping_surface",
    "暴れる": "erratic_swimming", "急に暴れる": "erratic_swimming",
    "ビュンビュン泳ぐ": "erratic_swimming",
    "ひっくり返る": "swimming_upside_down", "転覆": "swimming_upside_down",
    "逆さま": "swimming_upside_down", "ひっくり返って泳ぐ": "swimming_upside_down",
    "upside down": "swimming_upside_down",
    "バランスが取れない": "loss_of_balance", "傾いてる": "loss_of_balance",
    "横になってる": "loss_of_balance", "listing": "loss_of_balance",
    "隠れてる": "hiding", "出てこない": "hiding",
    "群れから離れてる": "isolation",
    "旋回": "spinning", "くるくる回る": "spinning",
    # 排泄
    "白い糞": "white_stringy_feces", "白い糸みたいな糞": "white_stringy_feces",
    "透明な糞": "white_stringy_feces",
    "糞がぶら下がってる": "trailing_feces",
    # 寄生虫
    "イカリムシ": "anchor_worm", "糸みたいなのがついてる": "anchor_worm",
    "虫がついてる": "worm_like_parasites",
    "ウオジラミ": "worm_like_parasites",
    # 痩せ（魚用 — dog用 weight_loss と異なるID emaciation を使用）
    "魚が痩せた": "emaciation", "魚がやせた": "emaciation",
    "痩せ細った": "emaciation",
    # 背骨
    "背骨が曲がってる": "bent_spine", "体が曲がってる": "bent_spine",
    # 餌を食べない（魚用 — dog用と重複しない表現のみ）
    "餌を食べない": "loss_of_appetite", "エサを食べない": "loss_of_appetite",
    # 大量死
    "大量に死んでる": "mass_mortality", "何匹も死んだ": "mass_mortality",
    "次々死ぬ": "mass_mortality", "全滅": "mass_mortality",
    "突然死んだ": "sudden_death",
    # 過抱卵
    "卵が出ない": "egg_binding", "卵詰まり": "egg_binding",
    # ---------------------------------------------------------------
    # 全種共通の追加エイリアス（多種のSYMPTOM_NAMES IDにマッチ）
    # ---------------------------------------------------------------
    # 皮膚・被毛
    "毛が抜ける": "hair_loss", "毛が抜けてきた": "hair_loss",
    "脱毛": "hair_loss", "ハゲ": "hair_loss", "はげ": "hair_loss",
    "毛が薄い": "hair_loss", "毛並みが悪い": "hair_loss",
    "羽が抜ける": "hair_loss", "羽毛が抜ける": "hair_loss",
    "itching": "itching",
    "かゆそう": "itching", "掻く": "itching",
    "皮膚が赤い": "skin_lesions", "皮膚炎": "skin_lesions",
    "かさぶた": "skin_lesions", "フケ": "skin_lesions",
    "ふけ": "skin_lesions", "皮膚が荒れてる": "skin_lesions",
    # 頭部
    "首が傾いてる": "head_tilt", "首が曲がってる": "head_tilt",
    "首傾げてる": "head_tilt", "斜頸": "head_tilt",
    "head tilt": "head_tilt",
    # 眼
    "目が濁ってる": "cloudy_eyes", "目が白っぽい": "cloudy_eyes",
    # 呼吸
    "口を開けて呼吸": "open_mouth_breathing", "口開けてる": "open_mouth_breathing",
    "開口呼吸してる": "open_mouth_breathing",
    # 鳥
    "羽を膨らませてる": "fluffed_feathers",
    "もこもこしてる": "fluffed_feathers",
    # 爬虫類
    "脱皮不全": "dysecdysis", "脱皮がうまくいかない": "dysecdysis",
    "脱皮できない": "dysecdysis", "皮が残ってる": "dysecdysis",
    "retained shed": "dysecdysis",
    # 関節
    "足が腫れてる": "lameness_or_limping",
    # ---------------------------------------------------------------
    # 口腔・歯科
    # ---------------------------------------------------------------
    "口が臭い": "bad_breath", "口臭": "bad_breath", "息が臭い": "bad_breath",
    "よだれが出る": "excessive_drooling",
    "食べにくそう": "loss_of_appetite", "食べるのを嫌がる": "loss_of_appetite",
    "口を痛がる": "excessive_drooling", "口を触ると嫌がる": "excessive_drooling",
    "歯が折れた": "excessive_drooling", "歯肉が赤い": "excessive_drooling",
    "口内炎": "oral_ulcers", "歯周病": "bad_breath",
    # ---------------------------------------------------------------
    # ウサギ追加
    # ---------------------------------------------------------------
    "うんちが小さい": "small_fecal_pellets", "糞が小さい": "small_fecal_pellets",
    "うんちが少ない": "reduced_fecal_output", "糞が少ない": "reduced_fecal_output",
    "歯ぎしり": "teeth_grinding", "歯ぎしりしてる": "teeth_grinding",
    "お腹を痛がる": "abdominal_pain", "丸まってる": "abdominal_pain",
    "お腹を触ると嫌がる": "abdominal_pain",
    # ---------------------------------------------------------------
    # ハムスター追加
    # ---------------------------------------------------------------
    "お尻が濡れてる": "wet_tail", "おしりが汚れてる": "wet_tail",
    "ウェットテイル": "wet_tail", "wet tail": "wet_tail",
    "頬袋が腫れてる": "cheek_swelling", "頬が膨らんでる": "cheek_swelling",
    # ---------------------------------------------------------------
    # 爬虫類追加
    # ---------------------------------------------------------------
    "口を開けたまま": "open_mouth_breathing",
    "粘液が出る": "nasal_discharge", "口から粘液": "nasal_discharge",
    "骨が柔らかい": "soft_bones", "骨軟化": "soft_bones",
    "甲羅が柔らかい": "soft_bones", "甲羅がぶよぶよ": "soft_bones",
    "手足が変形してる": "bone_deformity", "顎が柔らかい": "jaw_softening",
    "代謝性骨疾患": "soft_bones", "mbd": "soft_bones",
    "後ろ足が弱い": "hind_limb_weakness",
    "口の中に病変": "mouth_lesions", "口の中が腫れてる": "mouth_lesions",
    "口に粘液": "mucus_in_mouth",
    # ---------------------------------------------------------------
    # ハリネズミ追加
    # ---------------------------------------------------------------
    "針が抜ける": "quill_loss", "クイルロス": "quill_loss",
    "quilling": "hair_loss",
    "ふらふら歩く": "ataxia", "後ろ足が動かない": "paralysis_or_paresis",
    "wobbly hedgehog": "ataxia",
    "後ろ足が動かなくなってきた": "paralysis_or_paresis",
    "ふらつく": "ataxia", "ふらついてる": "ataxia",
    "耳にかさぶた": "skin_lesions",
    # ---------------------------------------------------------------
    # 猫追加（臨床的に重要な症状）
    # ---------------------------------------------------------------
    "お腹が大きくなった": "bloating", "お腹が大きくなってきた": "bloating",
    "お腹が膨らんできた": "bloating",
    "急に後ろ足が動かなくなった": "paralysis_or_paresis",
    "後ろ足が冷たい": "cold_extremities",
    "痛がる": "pain", "鳴いて痛がる": "pain",
    "口の中が赤い": "stomatitis",
    "トイレで鳴く": "straining_to_urinate",
    "黄疸が出てる": "jaundice",
    # ---------------------------------------------------------------
    # ウサギ追加
    # ---------------------------------------------------------------
    "目が揺れてる": "nystagmus", "眼振": "nystagmus",
    "目がぐるぐる": "nystagmus",
    "お尻が汚れてる": "diarrhea", "ウジがわいてる": "diarrhea",
    "歯が伸びすぎ": "teeth_grinding", "歯が長い": "teeth_grinding",
    "噛み合わせが悪い": "teeth_grinding",
    # ---------------------------------------------------------------
    # 鳥追加
    # ---------------------------------------------------------------
    "吐き戻してる": "vomiting",
    "首を振る": "head_shaking",
    "尾を振る": "labored_breathing", "呼吸のたびに尾を振る": "labored_breathing",
    "足の裏が赤い": "lameness_or_limping", "足の裏が腫れてる": "lameness_or_limping",
    "バンブルフット": "lameness_or_limping", "bumblefoot": "lameness_or_limping",
    # ---------------------------------------------------------------
    # 爬虫類追加
    # ---------------------------------------------------------------
    "目が腫れて開かない": "eye_swelling",
    "目が開かない": "eye_swelling",
    "甲羅に白い斑点": "skin_lesions", "甲羅が変色": "skin_lesions",
    "柔らかい部分がある": "soft_bones",
    # ---------------------------------------------------------------
    # 魚追加
    # ---------------------------------------------------------------
    "エラが腫れて": "gill_swelling", "エラが白くなった": "gill_paleness",
    # ---------------------------------------------------------------
    # モルモット追加
    # ---------------------------------------------------------------
    "関節が腫れてる": "lameness_or_limping", "関節腫れ": "lameness_or_limping",
    "キーキー鳴く": "lethargy", "鳴き声が変": "lethargy",
    # ---------------------------------------------------------------
    # 獣医師監査: 追加エイリアス (全種共通 + 種別)
    # ---------------------------------------------------------------
    # 猫 — 耳
    "耳をかく": "itching",
    "耳が臭い": "ear_discharge",
    "黒い耳垢": "ear_discharge", "耳垢が多い": "ear_discharge",
    # 猫 — 眼
    "目をしょぼしょぼ": "squinting",
    "片目だけ涙": "eye_discharge",
    # 猫 — 体型
    "急に太った": "bloating", "お腹だけ大きい": "bloating",
    # 猫 — 脱水
    "脱水してる": "lethargy",
    # 猫 — 毛
    "毛艶が悪い": "weight_loss",
    # ウサギ
    "膿が出てる": "abscess", "下顎が腫れてる": "jaw_swelling",
    # ハムスター
    "眼球突出": "pop_eye",
    "頬袋が出たまま": "cheek_pouch_prolapse", "頬袋が戻らない": "cheek_pouch_prolapse",
    # 鳥
    "糞が水っぽい": "diarrhea", "糞が緑色": "diarrhea",
    "嘴が伸びてる": "loss_of_appetite", "嘴過長": "loss_of_appetite",
    "眠ってばかり": "lethargy",
    # モルモット
    "歯茎から出血": "blood_in_stool", "壊血病": "weight_loss",
    "ビタミンc不足": "lethargy",
    # フェレット
    "低血糖": "lethargy",
    # 爬虫類
    "脱皮が途中で止まってる": "dysecdysis", "脱皮途中": "dysecdysis",
    "水疱": "skin_lesions",
    # 魚
    "ふわふわした白いもの": "cotton_like_growth",
    "白いもやもやがついてる": "cotton_like_growth",
    "白い綿": "cotton_like_growth",
    "急に死んだ": "sudden_death",
    # ---------------------------------------------------------------
    # 獣医師監査 第2回: 不足エイリアス追加
    # ---------------------------------------------------------------
    # 猫 — 耳疾患
    "耳だれ": "ear_discharge", "耳から臭い": "ear_discharge",
    "耳垢が黒い": "ear_discharge", "耳の中が汚い": "ear_discharge",
    "耳が痒い": "excessive_licking",
    # 猫 — 便秘（追加表現）
    "便が硬い": "constipation", "排便時に鳴く": "constipation",
    # ハムスター/ハリネズミ — 眼球突出
    "目が出てきた": "eye_swelling", "目が大きくなった": "eye_swelling",
    "目が飛び出した": "eye_swelling",
    # ウサギ — 涙
    "涙が止まらない": "eye_discharge", "目の周りが汚れてる": "eye_discharge",
    "目の周りが濡れてる": "eye_discharge",
    # 鳥 — 毛引き/嘴
    "羽を抜いてる": "hair_loss", "自咬": "hair_loss",
    "自分で羽を抜く": "hair_loss", "毛引き": "hair_loss",
    "嘴が長い": "loss_of_appetite",
    # モルモット — 壊血病の症状
    "歯茎が腫れてる": "bleeding_gums", "関節が痛そう": "swollen_joints",
    "毛がバサバサ": "hair_loss",
    # フェレット — 副腎
    "外陰部が腫れてる": "vulvar_swelling", "外陰部腫大": "vulvar_swelling",
    "尻尾の毛が抜ける": "hair_loss", "体の毛が薄くなった": "hair_loss",
    "前立腺が大きい": "prostatic_enlargement",
    # 爬虫類 — 甲羅/寄生虫
    "甲羅がカビみたい": "shell_discoloration", "甲羅が白い": "shell_discoloration",
    "甲羅が変色してる": "shell_discoloration",
    "便に虫がいる": "diarrhea", "虫が出た": "diarrhea",
    "寄生虫": "diarrhea",
    # ウサギ — 肛門/子宮
    "肛門が腫れてる": "perineal_swelling", "肛門周囲が腫れ": "perineal_swelling",
    "陰部から出血": "blood_in_urine",
    # 鳥 — 貧血
    "貧血": "lethargy", "anemia": "lethargy",
    "黒い便": "blood_in_stool",
    # ---------------------------------------------------------------
    # 獣医師監査 第3回
    # ---------------------------------------------------------------
    # 体重・体型
    "太ってきた": "weight_gain", "太った": "weight_gain",
    "毛が薄くなった": "hair_loss",
    "寒がる": "lethargy",
    # 鳥 — そのう
    "口をパクパク": "vomiting", "口をパクパクさせてる": "vomiting",
    "泡が出てる": "vomiting", "口から泡": "vomiting",
    # フェレット
    "まだらに抜ける": "hair_loss", "腫瘤": "lumps_and_bumps",
    "お腹に腫瘤": "lumps_and_bumps",
    # 魚 — 白点病補強
    "白い点々が全身に": "white_spots",
    "エラが速く動いてる": "rapid_gill_movement",
    # ハリネズミ
    "毛が逆立ってる": "lethargy",
    # ---------------------------------------------------------------
    # 獣医師監査 第4回: 日本語チャット精度向上
    # ---------------------------------------------------------------
    # 体型・体重 (修正: 太った=weight_gain, not weight_loss)
    "体重が増えた": "weight_gain", "体重増加": "weight_gain",
    # 皮膚
    "皮膚がカサカサ": "dry_skin", "カサカサしてる": "dry_skin",
    "肌がカサカサ": "dry_skin", "粉ふいてる": "dry_skin",
    # 四肢冷感
    "足が冷たい": "cold_extremities", "冷たい": "cold_extremities",
    "手足が冷たい": "cold_extremities", "末端が冷たい": "cold_extremities",
    # 虚脱・倒れる
    "崩れ落ちた": "collapse", "バタッと倒れた": "collapse",
    # 呼吸 (鳥・爬虫類向け)
    "口を開けて息してる": "open_mouth_breathing",
    "息が苦しそう": "labored_breathing",
    # 魚 — 擦り付け行動
    "体を擦り付ける": "flashing", "擦り付けてる": "flashing",
    "体をこすりつける": "flashing", "底砂に体を擦る": "flashing",
    # ハリネズミ — 針
    "針がボロボロ抜ける": "quill_loss", "針がたくさん抜ける": "quill_loss",
}


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


def _extract_species_symptoms(text: str, species: str) -> list[str]:
    """Extract symptom IDs from text using species-specific SYMPTOM_NAMES.

    Uses longest-match-first strategy and Japanese particle splitting
    for maximum extraction accuracy across all species.
    """
    sp_data = _SPECIES_DATA.get(species)
    if not sp_data:
        return []

    text_lower = text.lower()
    matched: set[str] = set()
    symptom_names = sp_data["symptom_names"]

    # Cross-species ID mapping: dog aliases use "loss_of_appetite" but many
    # species modules use "appetite_loss", "anorexia", etc. for the same concept.
    _ID_SYNONYMS: dict[str, list[str]] = {
        # Appetite
        "loss_of_appetite": ["appetite_loss", "anorexia", "poor_appetite", "decreased_appetite"],
        "appetite_loss": ["loss_of_appetite", "anorexia", "poor_appetite", "decreased_appetite"],
        "anorexia": ["loss_of_appetite", "appetite_loss", "poor_appetite"],
        # General
        "lethargy": ["depression", "inactivity", "weakness", "listlessness", "muscle_wasting"],
        "weakness": ["lethargy", "depression", "inactivity"],
        "depression": ["lethargy", "inactivity", "weakness"],
        "fever": ["hyperthermia", "elevated_temperature"],
        # GI
        "diarrhea": ["loose_stool", "watery_stool", "soft_stool"],
        "vomiting": ["regurgitation", "emesis"],
        "constipation": ["reduced_fecal_output", "straining_to_defecate", "small_fecal_pellets", "decreased_fecal_output"],
        "reduced_fecal_output": ["constipation", "small_fecal_pellets", "decreased_fecal_output"],
        "decreased_fecal_output": ["reduced_fecal_output", "constipation", "small_fecal_pellets"],
        "small_fecal_pellets": ["reduced_fecal_output", "constipation"],
        "teeth_grinding": ["bruxism", "dental_pain"],
        "abdominal_pain": ["abdominal_distension", "hunched_posture", "bloating"],
        "bloating": ["abdominal_distension", "abdominal_distention", "distended_abdomen", "abdominal_pain"],
        "abdominal_distension": ["bloating", "abdominal_distention", "distended_abdomen", "abdominal_pain"],
        # Neuro
        "seizures": ["convulsions", "fits", "epileptic_episodes"],
        "fainting": ["collapse", "syncope"],
        "collapse": ["fainting", "syncope"],
        "paralysis_or_paresis": ["paralysis", "paresis", "hind_limb_weakness", "hind_limb_paralysis", "posterior_paresis", "progressive_paralysis", "hindlimb_weakness"],
        "paralysis": ["paralysis_or_paresis", "paresis", "hind_limb_weakness", "hind_limb_paralysis"],
        "sudden_paralysis": ["hind_limb_paralysis", "paralysis", "paralysis_or_paresis"],
        "hind_limb_paralysis": ["paralysis", "paralysis_or_paresis", "hind_limb_weakness", "sudden_paralysis"],
        "jaundice": ["icterus", "yellow_skin", "yellow_mucous_membranes"],
        # Weight / body
        "weight_loss": ["emaciation", "wasting", "cachexia", "rough_coat", "poor_growth"],
        "weight_gain": ["obesity", "overweight"],
        "emaciation": ["weight_loss", "wasting", "cachexia"],
        # Skin / coat
        "excessive_drooling": ["drooling", "hypersalivation", "ptyalism"],
        "drooling": ["excessive_drooling", "hypersalivation"],
        "bad_breath": ["halitosis", "oral_odor"],
        "oral_ulcers": ["mouth_lesions", "stomatitis", "gingivitis"],
        "excessive_licking": ["itching", "pruritus", "scratching", "overgrooming", "ear_scratching", "scratching_ears"],
        "pop_eye": ["exophthalmia", "exophthalmos", "eye_protrusion", "bulging_eye", "eye_swelling", "eye_bulging", "enlarged_eye"],
        "eye_protrusion": ["pop_eye", "exophthalmia", "exophthalmos", "eye_bulging", "bulging_eye", "eye_swelling", "enlarged_eye", "proptosis"],
        "eye_swelling": ["pop_eye", "exophthalmia", "exophthalmos", "periorbital_swelling", "swollen_eyes", "bulging_eye", "eye_swollen", "eye_bulging", "enlarged_eye", "eye_protrusion"],
        "eye_bulging": ["pop_eye", "exophthalmia", "exophthalmos", "eye_protrusion", "eye_swelling", "bulging_eye", "enlarged_eye", "proptosis"],
        "exophthalmos": ["pop_eye", "eye_protrusion", "eye_bulging", "eye_swelling", "bulging_eye", "enlarged_eye", "proptosis"],
        "ear_discharge": ["ear_infection", "ear_inflammation", "otitis", "ear_mites"],
        "blood_in_urine": ["hematuria", "bloody_urine", "uterine_bleeding"],
        "blood_in_stool": ["melena", "hematochezia", "bloody_stool", "bleeding_gums"],
        "itching": ["pruritus", "scratching", "scratching_ears", "ear_scratching", "excessive_grooming", "excessive_licking", "overgrooming"],
        "pruritus": ["itching", "scratching", "excessive_licking"],
        "lameness_or_limping": ["lameness", "limping", "joint_swelling", "joint_pain", "leg_swelling", "foot_swelling", "reluctance_to_move"],
        "lumps_and_bumps": ["lumps_nodules", "skin_masses", "tumors", "skin_lumps"],
        # Hair
        "hair_loss": ["alopecia", "fur_loss", "feather_loss", "bald_patches", "quill_loss", "severe_quill_loss", "scaling", "circular_hair_loss"],
        "circular_hair_loss": ["hair_loss", "alopecia", "fur_loss", "bald_patches"],
        "alopecia": ["hair_loss", "fur_loss", "bald_patches", "circular_hair_loss"],
        "feather_loss": ["hair_loss", "feather_plucking", "alopecia"],
        "skin_lesions": ["scaling", "dermatitis", "skin_rash", "crusting", "thick_crusting", "flaky_skin", "dry_skin", "shell_discoloration", "shell_pitting", "skin_crusting"],
        "scaly_skin": ["scaling", "dandruff", "skin_crusting", "dry_skin", "flaky_skin"],
        "skin_crusting": ["scaling", "scaly_skin", "dandruff", "crusting"],
        "scaling": ["skin_lesions", "dandruff", "scaly_skin", "skin_crusting"],
        "dandruff": ["scaling", "scaly_skin", "skin_crusting"],
        # Eyes
        "cloudiness_in_eyes": ["cloudy_eyes", "eye_cloudiness", "corneal_opacity", "cloudy_eye", "corneal_cloudiness"],
        "cloudy_eyes": ["cloudiness_in_eyes", "eye_cloudiness", "corneal_opacity", "cloudy_eye", "corneal_cloudiness"],
        "cloudy_eye": ["cloudy_eyes", "cloudiness_in_eyes", "eye_cloudiness", "corneal_cloudiness"],
        "corneal_opacity": ["corneal_cloudiness", "cloudy_eyes", "cloudy_eye", "cloudiness_in_eyes"],
        "corneal_cloudiness": ["corneal_opacity", "cloudy_eyes", "cloudy_eye", "cloudiness_in_eyes"],
        "redness_in_eyes": ["red_eyes", "conjunctivitis", "eye_redness"],
        "eye_discharge": ["ocular_discharge", "eye_secretion", "epiphora"],
        "squinting": ["blepharospasm", "eye_squinting"],
        "tearing": ["excessive_tearing", "epiphora", "eye_discharge"],
        "excessive_tearing": ["tearing", "epiphora", "eye_discharge"],
        "vision_loss": ["blindness", "cloudy_eye", "cloudy_eyes", "cataracts"],
        # Respiratory
        "labored_breathing": ["respiratory_distress", "dyspnea", "open_mouth_breathing", "difficulty_breathing"],
        "respiratory_distress": ["labored_breathing", "dyspnea", "open_mouth_breathing"],
        "open_mouth_breathing": ["labored_breathing", "respiratory_distress", "mouth_breathing"],
        "rapid_breathing": ["tachypnea", "panting", "labored_breathing"],
        "coughing": ["cough", "kennel_cough"],
        "wheezing": ["coughing", "labored_breathing", "respiratory_distress"],
        "sneezing": ["reverse_sneezing", "nasal_irritation", "nasal_discharge"],
        "nasal_discharge": ["runny_nose", "rhinorrhea", "nasal_secretion", "sneezing"],
        # Urinary
        "straining_to_urinate": ["dysuria", "urinary_straining", "difficulty_urinating"],
        "frequent_urination": ["pollakiuria", "polyuria", "excessive_urination", "increased_urination"],
        "excessive_urination": ["frequent_urination", "polyuria", "pollakiuria", "increased_urination"],
        "increased_urination": ["excessive_urination", "frequent_urination", "polyuria", "pollakiuria"],
        "increased_thirst": ["excessive_thirst", "polydipsia"],
        "excessive_thirst": ["increased_thirst", "polydipsia"],
        "polydipsia": ["excessive_thirst", "increased_thirst"],
        "polyuria": ["excessive_urination", "frequent_urination", "increased_urination"],
        # Musculoskeletal
        "joint_pain_or_stiffness": ["joint_pain", "arthritis", "stiffness"],
        # Behavior
        "anxiety": ["restlessness", "pacing", "nervousness"],
        "self_mutilation": ["self_chewing", "self_harm", "overgrooming", "feather_plucking"],
        "self_chewing": ["self_mutilation", "self_harm"],
        "behavioral_change": ["behavioral_changes", "aggression", "depression", "restlessness"],
        "behavioral_changes": ["behavioral_change", "aggression", "depression"],
        # Head
        "head_tilt": ["vestibular_signs", "torticollis", "wry_neck", "nystagmus"],
        "nystagmus": ["head_tilt", "vestibular_signs", "rolling"],
        "ataxia": ["tremors", "incoordination", "wobbling", "unsteady_gait"],
        "tremors": ["shaking", "trembling", "muscle_tremors", "ataxia"],
        "wobbling": ["ataxia", "incoordination", "unsteady_gait", "stumbling"],
        # Reptile-specific
        "dysecdysis": ["abnormal_shedding", "retained_shed", "shedding_problems", "retained_skin"],
        "retained_shed": ["dysecdysis", "retained_skin", "shedding_problems"],
        "retained_skin": ["dysecdysis", "retained_shed", "shedding_problems"],
        "soft_bones": ["bone_weakness", "jaw_softening", "shell_soft_spots", "fractures", "bone_deformity", "shell_softening", "soft_shell"],
        "bone_deformity": ["bone_swelling", "limb_deformity", "soft_bones", "shell_deformity", "fractures"],
        "shell_softening": ["soft_shell", "soft_bones", "shell_soft_spots", "shell_deformity"],
        "soft_shell": ["shell_softening", "soft_bones", "shell_soft_spots", "shell_deformity"],
        "shell_deformity": ["bone_deformity", "soft_shell", "shell_softening"],
        "mouth_lesions": ["oral_lesions", "stomatitis", "mouth_rot"],
        "mucus_in_mouth": ["oral_mucus", "mouth_discharge"],
        # Limbs / extremities
        "cold_limbs": ["cold_extremities", "poor_circulation"],
        "cold_extremities": ["cold_limbs", "poor_circulation"],
        # Bird-specific
        "fluffed_feathers": ["feather_fluffing", "puffed_up", "ruffled_feathers"],
        "feather_plucking": ["feather_loss", "self_mutilation", "feather_destructive_behavior"],
        "crop_swelling": ["crop_stasis", "ingluvitis", "crop_distension"],
        "crop_stasis": ["crop_swelling", "ingluvitis"],
        # Fish fin
        "frayed_fins": ["fin_rot", "fin_erosion", "ragged_fins"],
        "fin_rot": ["frayed_fins", "fin_erosion"],
        "redness_skin": ["skin_redness", "hemorrhage", "fin_hemorrhage"],
        "skin_redness": ["redness_skin", "hemorrhage", "red_legs", "red_ventrum"],
        "fin_hemorrhage": ["redness_skin", "hemorrhage"],
        # Hamster
        "wet_tail": ["diarrhea", "watery_diarrhea"],
        # Skin / coat additional
        "thinning_skin": ["skin_fragility", "thin_skin", "fragile_skin"],
        "poor_coat": ["dry_skin", "rough_coat", "dull_coat"],
        "rough_coat": ["poor_coat", "dry_skin", "dull_coat"],
        # Ferret reproductive
        "vulvar_swelling": ["vulvar_discharge", "genital_swelling"],
        "prostatic_enlargement": ["prostate_enlargement", "enlarged_prostate"],
        # Cardiac
        "bradycardia": ["slow_heart_rate"],
        # Cheek / oral
        "cheek_swelling": ["bloating", "cheek_pouch_prolapse", "facial_swelling"],
        "cheek_pouch_prolapse": ["cheek_swelling"],
        "jaw_swelling": ["facial_swelling", "swelling"],
        "abscess": ["discharge", "swelling"],
        "overgrown_teeth": ["dental_overgrowth", "incisor_overgrowth", "molar_overgrowth", "tooth_overgrowth", "malocclusion", "visible_tooth_overgrowth"],
        "dental_overgrowth": ["overgrown_teeth", "incisor_overgrowth", "molar_overgrowth", "malocclusion", "visible_tooth_overgrowth"],
        "visible_tooth_overgrowth": ["overgrown_teeth", "dental_overgrowth", "malocclusion"],
        "scaly_legs": ["leg_scales", "scaly_face"],
        "leg_scales": ["scaly_legs", "scaly_face"],
        # Pain
        "pain": ["lethargy", "vocalization"],
        # Oral
        "stomatitis": ["oral_ulcers", "bad_breath", "excessive_drooling"],
        # Perianal
        "perineal_swelling": ["perianal_irritation", "swelling"],
        # Guinea pig scurvy
        "bleeding_gums": ["swollen_gums", "oral_bleeding"],
        "swollen_joints": ["joint_swelling", "lameness_or_limping", "lameness"],
        # Fish
        "darkened_coloration": ["dark_coloration", "discoloration"],
        "dark_coloration": ["darkened_coloration", "discoloration"],
        # Amphibian
        "red_legs": ["red_ventrum", "skin_redness", "hemorrhage"],
        "red_ventrum": ["red_legs", "skin_redness", "hemorrhage"],
        "edema": ["swelling", "bloating", "ascites"],
        # Effusion
        "effusion": ["pleural_effusion", "abdominal_distension", "ascites"],
        "pleural_effusion": ["effusion", "labored_breathing"],
        "ascites": ["effusion", "abdominal_distension", "bloating"],
        # Swelling (generic)
        "swelling": ["facial_swelling", "eye_swelling", "edema"],
    }

    def _resolve_id(sid: str) -> str | None:
        """Return the symptom ID that exists in this species' SYMPTOM_NAMES."""
        if sid in symptom_names:
            return sid
        for alt in _ID_SYNONYMS.get(sid, []):
            if alt in symptom_names:
                return alt
        return None

    # Phase 1: Longest-match-first alias matching (aliases → species symptom IDs)
    # Track consumed character positions to avoid substring double-matching
    # (e.g. "外陰部が腫れてる" should not also match "腫れてる")
    _sorted_aliases = sorted(SYMPTOM_ALIASES.keys(), key=len, reverse=True)
    _consumed: set[int] = set()
    for alias in _sorted_aliases:
        pos = text_lower.find(alias)
        if pos >= 0:
            alias_range = set(range(pos, pos + len(alias)))
            if alias_range & _consumed:
                continue
            symptom_id = SYMPTOM_ALIASES[alias]
            resolved = _resolve_id(symptom_id)
            if resolved:
                matched.add(resolved)
                _consumed |= alias_range

    # Phase 2: Direct symptom name matches (ja/en)
    for sym_id, names in symptom_names.items():
        ja = names.get("ja", "").lower()
        en = names.get("en", "").lower()
        if (ja and ja in text_lower) or (en and en in text_lower):
            matched.add(sym_id)

    # Phase 3: Fragment splitting for compound Japanese phrases
    if not matched:
        import re as _re
        fragments = _re.split(r'[、。,.と！!？?\s]+', text_lower)
        fragments = [f.strip() for f in fragments if len(f.strip()) >= 1]
        for frag in fragments:
            for alias in _sorted_aliases:
                if alias in frag:
                    sid = SYMPTOM_ALIASES[alias]
                    if sid in symptom_names:
                        matched.add(sid)
                        break
            for sym_id, names in symptom_names.items():
                ja = names.get("ja", "").lower()
                en = names.get("en", "").lower()
                if (ja and ja in frag) or (en and en in frag):
                    matched.add(sym_id)

    return list(matched)


def _match_species_symptoms_to_diseases(symptom_ids: list[str], species: str) -> list[dict]:
    """Match symptom IDs to species-specific diseases using advanced weighted scoring.

    Uses the same harmonic-mean + specificity + negative-evidence algorithm as
    the dog matcher (match_symptoms_to_diseases) to achieve consistent,
    high-accuracy differential diagnosis across all species.
    """
    import math

    sp_data = _SPECIES_DATA.get(species)
    if not sp_data or not symptom_ids:
        return []

    # Expand user symptoms with synonyms for better disease matching
    _ID_SYNONYMS_LOCAL = _extract_species_symptoms.__code__.co_consts  # noqa — not used
    # Re-define synonym map here (shared with extraction)
    _SYN = {
        "frayed_fins": ["fin_rot"], "fin_rot": ["frayed_fins"],
        "redness_skin": ["fin_hemorrhage", "hemorrhage", "skin_redness"], "fin_hemorrhage": ["redness_skin"],
        "skin_redness": ["redness_skin", "hemorrhage", "red_legs", "red_ventrum"],
        "loss_of_appetite": ["appetite_loss", "anorexia"], "appetite_loss": ["loss_of_appetite", "anorexia"],
        "anorexia": ["loss_of_appetite", "appetite_loss"],
        "constipation": ["reduced_fecal_output", "small_fecal_pellets", "decreased_fecal_output"],
        "small_fecal_pellets": ["reduced_fecal_output", "constipation"],
        "reduced_fecal_output": ["small_fecal_pellets", "constipation", "decreased_fecal_output"],
        "decreased_fecal_output": ["reduced_fecal_output", "constipation", "small_fecal_pellets"],
        "bloating": ["abdominal_distension", "abdominal_pain"], "abdominal_distension": ["bloating", "abdominal_pain"],
        "abdominal_pain": ["bloating", "abdominal_distension", "hunched_posture"],
        "hunched_posture": ["abdominal_pain"],
        "excessive_drooling": ["drooling"], "drooling": ["excessive_drooling"],
        "frequent_urination": ["excessive_urination", "polyuria", "increased_urination"],
        "excessive_urination": ["frequent_urination", "polyuria", "increased_urination"],
        "increased_urination": ["excessive_urination", "frequent_urination", "polyuria"],
        "excessive_thirst": ["polydipsia", "increased_thirst"],
        "increased_thirst": ["excessive_thirst", "polydipsia"],
        "polydipsia": ["excessive_thirst", "increased_thirst"],
        "polyuria": ["excessive_urination", "frequent_urination", "increased_urination"],
        "hair_loss": ["alopecia", "scaling", "quill_loss", "severe_quill_loss", "feather_loss", "circular_hair_loss"],
        "circular_hair_loss": ["hair_loss", "alopecia"],
        "alopecia": ["hair_loss", "circular_hair_loss"],
        "feather_loss": ["hair_loss", "feather_plucking"],
        "feather_plucking": ["feather_loss", "self_mutilation"],
        "skin_lesions": ["scaling", "dermatitis", "skin_rash", "crusting", "thick_crusting", "flaky_skin", "dry_skin", "shell_discoloration", "shell_pitting", "skin_crusting"],
        "scaly_skin": ["scaling", "dandruff", "skin_crusting", "dry_skin"],
        "skin_crusting": ["scaling", "scaly_skin", "dandruff"],
        "scaling": ["skin_lesions", "dandruff", "scaly_skin"],
        "dandruff": ["scaling", "scaly_skin", "skin_crusting"],
        "itching": ["pruritus", "scratching", "mild_itching", "ear_scratching"],
        "pruritus": ["itching", "scratching", "mild_itching", "ear_scratching"],
        "cloudy_eyes": ["cloudy_eye", "cloudiness_in_eyes", "corneal_cloudiness", "corneal_opacity"],
        "cloudy_eye": ["cloudy_eyes", "corneal_cloudiness", "corneal_opacity"],
        "corneal_opacity": ["corneal_cloudiness", "cloudy_eyes", "cloudy_eye"],
        "corneal_cloudiness": ["corneal_opacity", "cloudy_eyes", "cloudy_eye"],
        "tearing": ["excessive_tearing", "epiphora"], "excessive_tearing": ["tearing", "epiphora"],
        "vision_loss": ["blindness", "cloudy_eye", "cataracts"],
        "open_mouth_breathing": ["respiratory_distress", "labored_breathing"],
        "labored_breathing": ["respiratory_distress", "open_mouth_breathing", "dyspnea"],
        "respiratory_distress": ["labored_breathing", "open_mouth_breathing", "dyspnea"],
        "wheezing": ["coughing", "labored_breathing", "respiratory_distress"],
        "soft_bones": ["bone_weakness", "jaw_softening", "shell_soft_spots", "fractures", "bone_deformity", "soft_shell", "shell_softening"],
        "bone_deformity": ["soft_bones", "limb_deformity", "shell_deformity", "fractures", "swollen_limbs"],
        "shell_softening": ["soft_shell", "soft_bones", "shell_deformity"],
        "soft_shell": ["shell_softening", "soft_bones", "shell_deformity"],
        "shell_deformity": ["bone_deformity", "soft_shell", "shell_softening"],
        "head_tilt": ["vestibular_signs", "torticollis"],
        "fluffed_feathers": ["feather_fluffing"],
        "paralysis_or_paresis": ["paralysis", "paresis", "hind_limb_weakness", "posterior_paresis", "progressive_paralysis", "hindlimb_weakness", "hind_limb_paralysis"],
        "paralysis": ["hind_limb_paralysis", "paralysis_or_paresis", "hind_limb_weakness"],
        "sudden_paralysis": ["hind_limb_paralysis", "paralysis", "paralysis_or_paresis"],
        "hind_limb_paralysis": ["paralysis", "sudden_paralysis", "paralysis_or_paresis", "hind_limb_weakness"],
        "eye_swelling": ["periorbital_swelling", "swollen_eyes", "blepharitis", "pop_eye", "exophthalmia", "exophthalmos", "bulging_eye", "eye_bulging", "enlarged_eye", "eye_protrusion"],
        "eye_protrusion": ["eye_swelling", "eye_bulging", "pop_eye", "exophthalmos", "bulging_eye", "proptosis"],
        "eye_bulging": ["eye_protrusion", "eye_swelling", "pop_eye", "exophthalmos", "proptosis"],
        "exophthalmos": ["eye_protrusion", "eye_bulging", "eye_swelling", "pop_eye", "proptosis"],
        "jaundice": ["icterus", "yellow_skin"],
        "vomiting": ["regurgitation", "crop_stasis"],
        "regurgitation": ["vomiting"],
        "head_shaking": ["head_bobbing"],
        "gill_swelling": ["gill_redness"],
        "gill_paleness": ["gill_necrosis"],
        "nystagmus": ["head_tilt", "rolling"],
        "ataxia": ["tremors", "incoordination", "wobbling", "stumbling", "mild_ataxia"],
        "tremors": ["ataxia", "shaking", "muscle_twitching"],
        "wobbling": ["ataxia", "incoordination", "stumbling"],
        "ear_discharge": ["ear_infection", "otitis", "ear_mites"],
        "blood_in_urine": ["hematuria", "uterine_bleeding"],
        "blood_in_stool": ["melena", "bleeding_gums", "hematochezia"],
        "weight_loss": ["rough_coat", "poor_growth", "emaciation"],
        "weight_gain": ["obesity", "overweight"],
        "lethargy": ["reluctance_to_move", "weakness", "pain_on_touch", "depression"],
        "depression": ["lethargy", "weakness"],
        "hind_limb_weakness": ["hindlimb_weakness", "posterior_paresis", "hind_limb_paralysis", "progressive_paralysis"],
        "hindlimb_weakness": ["hind_limb_weakness", "posterior_paresis", "hind_limb_paralysis"],
        "swollen_eyes": ["eye_swelling", "periorbital_swelling"],
        "sneezing": ["nasal_discharge"],
        "wet_tail": ["diarrhea"], "diarrhea": ["wet_tail"],
        "poor_coat": ["hair_loss", "dry_skin"], "dry_skin": ["poor_coat", "flaky_skin", "scaling"],
        "flaky_skin": ["dry_skin", "scaling", "crusting"],
        "thinning_skin": ["hair_loss"],
        "darkened_coloration": ["dark_coloration", "discoloration"],
        "dark_coloration": ["darkened_coloration", "discoloration"],
        "cold_limbs": ["cold_extremities"], "cold_extremities": ["cold_limbs"],
        "self_mutilation": ["self_chewing", "feather_plucking"],
        "self_chewing": ["self_mutilation"],
        "behavioral_change": ["behavioral_changes", "aggression"],
        "behavioral_changes": ["behavioral_change"],
        "effusion": ["pleural_effusion", "abdominal_distension", "ascites"],
        "pleural_effusion": ["effusion", "abdominal_distension"],
        "ascites": ["effusion", "abdominal_distension", "bloating"],
        "overgrown_teeth": ["dental_overgrowth", "incisor_overgrowth", "molar_overgrowth", "malocclusion", "visible_tooth_overgrowth"],
        "dental_overgrowth": ["overgrown_teeth", "malocclusion", "visible_tooth_overgrowth"],
        "visible_tooth_overgrowth": ["overgrown_teeth", "dental_overgrowth", "malocclusion"],
        "dysecdysis": ["retained_shed", "retained_skin", "shedding_problems"],
        "retained_shed": ["dysecdysis", "retained_skin"],
        "retained_skin": ["dysecdysis", "retained_shed"],
        "crop_swelling": ["crop_stasis", "ingluvitis"],
        "crop_stasis": ["crop_swelling", "ingluvitis"],
        "red_legs": ["red_ventrum", "skin_redness", "hemorrhage"],
        "red_ventrum": ["red_legs", "skin_redness"],
        "edema": ["swelling", "bloating", "ascites"],
        "swelling": ["edema", "facial_swelling", "eye_swelling"],
        "rough_coat": ["poor_coat", "dry_skin"],
        "scaly_legs": ["leg_scales", "scaly_face"],
        "leg_scales": ["scaly_legs", "scaly_face"],
        "scaly_face": ["scaly_legs", "leg_scales", "crusty_beak"],
        "hole_in_head": ["head_erosion", "head_pitting"],
    }
    expanded_set = set(symptom_ids)
    for sid in symptom_ids:
        for alt in _SYN.get(sid, []):
            expanded_set.add(alt)
    symptom_set = expanded_set
    diseases = sp_data["diseases"]

    # --- Load prevalence data for this species ---
    from api.species import prevalence_data as _prev_mod
    _prevalence = _prev_mod.SPECIES_PREVALENCE.get(species, {})
    _PREVALENCE_MULTIPLIER = {
        "very_common": 1.30,
        "common": 1.05,
        "uncommon": 0.85,
        "rare": 0.70,
    }

    # --- Build per-symptom specificity for this species ---
    # Count how many diseases each symptom appears in (IDF-like).
    symptom_disease_count: dict[str, int] = {}
    for disease in diseases:
        for s in disease.get("symptoms", set()):
            symptom_disease_count[s] = symptom_disease_count.get(s, 0) + 1
    total_diseases = max(len(diseases), 1)

    def _compute_weight(sym_id: str) -> float:
        """Higher weight for symptoms that appear in fewer diseases (more specific)."""
        count = symptom_disease_count.get(sym_id, 1)
        # IDF-inspired: log(N / count) + 1, clamped to [1.0, 3.0]
        idf = math.log(total_diseases / max(count, 1)) + 1.0
        return max(1.0, min(idf, 3.0))

    user_weights = {s: _compute_weight(s) for s in symptom_set}
    total_user_weight = sum(user_weights.values())

    matches = []
    for disease in diseases:
        disease_symptoms = set(disease.get("symptoms", set()))
        if not disease_symptoms:
            continue

        matched = symptom_set & disease_symptoms
        if not matched:
            continue

        # --- Weighted recall (how well user symptoms match this disease) ---
        matched_weight = sum(user_weights.get(s, 1.0) for s in matched)
        weighted_recall = matched_weight / total_user_weight if total_user_weight > 0 else 0

        # --- Coverage (how much of the disease's symptom profile is covered) ---
        disease_weights = {s: _compute_weight(s) for s in disease_symptoms}
        total_disease_weight = sum(disease_weights.values())
        covered_weight = sum(disease_weights.get(s, 1.0) for s in matched)
        coverage = covered_weight / total_disease_weight if total_disease_weight > 0 else 0

        # --- Harmonic mean base score ---
        if weighted_recall + coverage > 0:
            base_score = 2.0 * weighted_recall * coverage / (weighted_recall + coverage)
        else:
            base_score = 0.0

        # --- Specificity bonus: reward matching highly specific symptoms ---
        specificity_bonus = 0.0
        for s in matched:
            w = _compute_weight(s)
            if w >= 2.5:
                specificity_bonus += 0.06
            elif w >= 1.8:
                specificity_bonus += 0.03
        base_score = min(base_score + specificity_bonus, 1.0)

        # --- Negative evidence penalty ---
        # Scale penalty by how many symptoms the user actually provided vs disease total.
        # When user provides few symptoms relative to disease total, reduce penalty.
        missing = disease_symptoms - symptom_set
        negative_penalty = 1.0
        if len(symptom_set) >= 3 and len(disease_symptoms) >= 3:
            obs_ratio = min(1.0, len(symptom_ids) / len(disease_symptoms))
            for s in missing:
                w = _compute_weight(s)
                if w >= 2.5:
                    negative_penalty -= 0.06 * obs_ratio
                elif w >= 2.0:
                    negative_penalty -= 0.03 * obs_ratio
            negative_penalty = max(negative_penalty, 0.55)

        # --- Coverage completeness bonus ---
        # Reward diseases where more absolute symptoms matched (not just ratio).
        # This prevents diseases with few symptoms from dominating.
        coverage_bonus = 1.0
        absolute_match_count = len(matched)
        if absolute_match_count >= 4:
            coverage_bonus = 1.10
        elif absolute_match_count >= 3:
            coverage_bonus = 1.05

        # --- Urgency boost: slightly favor high-urgency diseases for safety ---
        urgency = disease.get("urgency", "low")
        urgency_factor = {"emergency": 1.05, "high": 1.02}.get(urgency, 1.0)

        # --- Prevalence prior ---
        disease_name = disease.get("name", "")
        prevalence_tier = _prevalence.get(disease_name, "")
        prevalence_mult = _PREVALENCE_MULTIPLIER.get(prevalence_tier, 1.0)

        composite = base_score * negative_penalty * urgency_factor * coverage_bonus * prevalence_mult

        # --- Logistic confidence calibration ---
        raw_logistic = 1.0 / (1.0 + math.exp(-6.0 * (composite - 0.4)))
        confidence = min(round(raw_logistic * 100, 1), 95.0)

        matches.append({
            "disease_id": disease.get("name", ""),
            "name_ja": disease.get("name_ja", ""),
            "name_en": disease.get("name", ""),
            "severity": urgency,
            "similarity_score": round(composite, 3),
            "confidence_percent": confidence,
            "matched_symptoms": sorted(matched),
            "unmatched_user_symptoms": sorted(symptom_set - disease_symptoms),
            "additional_disease_symptoms": sorted(disease_symptoms - symptom_set),
            "missing_key_symptoms": sorted(
                s for s in missing if _compute_weight(s) >= 1.8
            ),
            "description": disease.get("description", ""),
            "description_ja": disease.get("description_ja", ""),
            "description_en": disease.get("description", ""),
            "recommended_tests": disease.get("recommended_tests", []),
            "scoring_detail": {
                "weighted_recall": round(weighted_recall, 3),
                "coverage": round(coverage, 3),
                "negative_penalty": round(negative_penalty, 3),
                "urgency_factor": urgency_factor,
            },
        })

    matches.sort(key=lambda m: m["similarity_score"], reverse=True)
    return matches


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
                logger.warning(f"AI extraction failed, falling back to manual: {e}")
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


DISEASE_SUPPLEMENTS = {
    # =========================================================================
    # Canine Vet Nutrition (caninevet.jp) サプリメント製品マッピング
    # 製品ラインナップ:
    #   1. MSM＋アミノコンプリート - 関節・筋肉・腱・アミノ酸サポート
    #   2. For Antioxidant Asta-Melon・VitaminE・Cysteine - 抗酸化サポート
    #   3. For Joint - 関節ケア
    #   4. Prebiotics & Probiotics & サイリウム - 消化器・腸内環境
    #   5. Canine Vet Relax & CBD - リラックス・疼痛緩和
    #   6. Canine Vet Protain - タンパク質・筋肉維持
    #   7. NMN-ミトコンドリアアシスト - 代謝活性・細胞エネルギー
    #   8. Canine Vet Booster & Relax - 活力・体力回復
    #   9. カミデミルク - 栄養補給ミルク
    #  10. No Pain Quick Stop - 止血パウダー
    # =========================================================================

    # --- Respiratory (呼吸器) ---
    "brachycephalic_airway_syndrome": [
        {"name_ja": "For Antioxidant Asta-Melon・VitaminE・Cysteine",
         "name_en": "For Antioxidant (Astaxanthin, Melon SOD, VitE, Cysteine)",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "気道粘膜の抗酸化保護・炎症軽減",
         "reason_en": "Antioxidant protection for airway mucosa and inflammation reduction"},
        {"name_ja": "MSM＋アミノコンプリート",
         "name_en": "MSM + Amino Complete",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "気道周囲組織の修復・アミノ酸による回復サポート",
         "reason_en": "Tissue repair around airways and amino acid recovery support"},
    ],
    "canine_parvovirus": [
        {"name_ja": "Prebiotics & Probiotics & サイリウム",
         "name_en": "Prebiotics & Probiotics & Psyllium",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "腸内フローラの回復・消化機能再建",
         "reason_en": "Restore intestinal flora and rebuild digestive function"},
        {"name_ja": "MSM＋アミノコンプリート",
         "name_en": "MSM + Amino Complete",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "回復期の必須アミノ酸補給・組織修復促進",
         "reason_en": "Essential amino acid supplementation and tissue repair during recovery"},
        {"name_ja": "カミデミルク",
         "name_en": "Kamide Milk",
         "dosage": "体重に応じて調整", "frequency": "1日1〜2回",
         "reason_ja": "回復期の栄養補給・消化吸収しやすい栄養源",
         "reason_en": "Easily digestible nutrition source during recovery"},
    ],
    "canine_distemper": [
        {"name_ja": "For Antioxidant Asta-Melon・VitaminE・Cysteine",
         "name_en": "For Antioxidant (Astaxanthin, Melon SOD, VitE, Cysteine)",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "ウイルス感染による酸化ストレスから神経・免疫細胞を保護",
         "reason_en": "Protect neural and immune cells from viral oxidative stress"},
        {"name_ja": "MSM＋アミノコンプリート",
         "name_en": "MSM + Amino Complete",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "神経機能回復のためのアミノ酸サポート",
         "reason_en": "Amino acid support for neurological recovery"},
        {"name_ja": "Canine Vet Booster & Relax",
         "name_en": "Canine Vet Booster & Relax",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "体力回復・免疫力の活性化サポート",
         "reason_en": "Support physical recovery and immune system activation"},
    ],
    "kennel_cough": [
        {"name_ja": "For Antioxidant Asta-Melon・VitaminE・Cysteine",
         "name_en": "For Antioxidant (Astaxanthin, Melon SOD, VitE, Cysteine)",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "気道の免疫力向上・抗酸化保護",
         "reason_en": "Boost airway immunity and antioxidant protection"},
        {"name_ja": "Prebiotics & Probiotics & サイリウム",
         "name_en": "Prebiotics & Probiotics & Psyllium",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "腸管免疫の強化による全身免疫サポート",
         "reason_en": "Systemic immune support via gut immunity enhancement"},
    ],
    "canine_influenza": [
        {"name_ja": "For Antioxidant Asta-Melon・VitaminE・Cysteine",
         "name_en": "For Antioxidant (Astaxanthin, Melon SOD, VitE, Cysteine)",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "ウイルス感染時の免疫・抗酸化サポート",
         "reason_en": "Immune and antioxidant support during viral infection"},
        {"name_ja": "Prebiotics & Probiotics & サイリウム",
         "name_en": "Prebiotics & Probiotics & Psyllium",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "腸内環境改善による免疫力向上",
         "reason_en": "Improve immunity through gut health optimization"},
        {"name_ja": "カミデミルク",
         "name_en": "Kamide Milk",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "食欲低下時の栄養補給",
         "reason_en": "Nutritional support during appetite loss"},
    ],

    # --- Gastrointestinal (消化器) ---
    "gdv_bloat": [
        {"name_ja": "Prebiotics & Probiotics & サイリウム",
         "name_en": "Prebiotics & Probiotics & Psyllium",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "術後の消化機能回復・腸内環境再建",
         "reason_en": "Post-surgical digestive recovery and gut flora restoration"},
        {"name_ja": "MSM＋アミノコンプリート",
         "name_en": "MSM + Amino Complete",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "術後の組織修復・アミノ酸による回復促進",
         "reason_en": "Post-surgical tissue repair and amino acid recovery"},
    ],
    "pancreatitis": [
        {"name_ja": "Prebiotics & Probiotics & サイリウム",
         "name_en": "Prebiotics & Probiotics & Psyllium",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "腸内環境の改善・消化負担の軽減",
         "reason_en": "Improve gut environment and reduce digestive burden"},
        {"name_ja": "カミデミルク",
         "name_en": "Kamide Milk",
         "dosage": "体重に応じて調整", "frequency": "1日1〜2回",
         "reason_ja": "膵臓に負担の少ない消化吸収しやすい栄養源",
         "reason_en": "Easily digestible nutrition that is gentle on the pancreas"},
        {"name_ja": "For Antioxidant Asta-Melon・VitaminE・Cysteine",
         "name_en": "For Antioxidant (Astaxanthin, Melon SOD, VitE, Cysteine)",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "膵臓の炎症に伴う酸化ストレスの軽減",
         "reason_en": "Reduce oxidative stress from pancreatic inflammation"},
    ],
    "ibd": [
        {"name_ja": "Prebiotics & Probiotics & サイリウム",
         "name_en": "Prebiotics & Probiotics & Psyllium",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "腸内細菌叢の正常化・腸管バリア機能強化",
         "reason_en": "Normalize gut microbiota and strengthen intestinal barrier"},
        {"name_ja": "MSM＋アミノコンプリート",
         "name_en": "MSM + Amino Complete",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "腸管組織の修復・吸収不良による栄養補給",
         "reason_en": "Intestinal tissue repair and nutrition for malabsorption"},
        {"name_ja": "For Antioxidant Asta-Melon・VitaminE・Cysteine",
         "name_en": "For Antioxidant (Astaxanthin, Melon SOD, VitE, Cysteine)",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "腸管の慢性炎症による酸化ダメージの軽減",
         "reason_en": "Reduce oxidative damage from chronic intestinal inflammation"},
    ],
    "megaesophagus": [
        {"name_ja": "Prebiotics & Probiotics & サイリウム",
         "name_en": "Prebiotics & Probiotics & Psyllium",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "消化機能サポート・腸内環境の維持",
         "reason_en": "Digestive support and gut health maintenance"},
        {"name_ja": "カミデミルク",
         "name_en": "Kamide Milk",
         "dosage": "体重に応じて調整", "frequency": "1日2〜3回",
         "reason_ja": "嚥下しやすい流動性栄養源・栄養吸収不良の補正",
         "reason_en": "Easy-to-swallow liquid nutrition to compensate for malabsorption"},
    ],

    # --- Musculoskeletal / Orthopedic (筋骨格・整形) ---
    "hip_dysplasia": [
        {"name_ja": "For Joint",
         "name_en": "Canine Vet For Joint",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "関節軟骨の保護・修復・可動域改善",
         "reason_en": "Joint cartilage protection, repair, and mobility improvement"},
        {"name_ja": "MSM＋アミノコンプリート",
         "name_en": "MSM + Amino Complete",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "MSMによる関節炎症軽減・筋肉維持のためのアミノ酸補給",
         "reason_en": "MSM for joint inflammation and amino acids for muscle maintenance"},
        {"name_ja": "Canine Vet Relax & CBD",
         "name_en": "Canine Vet Relax & CBD",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "関節痛の緩和・リラックス効果",
         "reason_en": "Joint pain relief and relaxation"},
    ],
    "elbow_dysplasia": [
        {"name_ja": "For Joint",
         "name_en": "Canine Vet For Joint",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "肘関節軟骨の保護・修復",
         "reason_en": "Elbow joint cartilage protection and repair"},
        {"name_ja": "MSM＋アミノコンプリート",
         "name_en": "MSM + Amino Complete",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "MSMによる関節炎症軽減・関節周囲筋のサポート",
         "reason_en": "MSM for joint inflammation and periarticular muscle support"},
    ],
    "ivdd": [
        {"name_ja": "MSM＋アミノコンプリート",
         "name_en": "MSM + Amino Complete",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "脊椎周囲の炎症軽減・神経組織修復のためのアミノ酸",
         "reason_en": "Spinal inflammation reduction and amino acids for nerve repair"},
        {"name_ja": "For Antioxidant Asta-Melon・VitaminE・Cysteine",
         "name_en": "For Antioxidant (Astaxanthin, Melon SOD, VitE, Cysteine)",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "神経組織の抗酸化保護",
         "reason_en": "Antioxidant protection for neural tissue"},
        {"name_ja": "Canine Vet Relax & CBD",
         "name_en": "Canine Vet Relax & CBD",
         "dosage": "体重に応じて調整", "frequency": "1日1〜2回",
         "reason_ja": "椎間板疾患に伴う疼痛緩和・リラックス",
         "reason_en": "Pain relief and relaxation for disc disease"},
    ],
    "patellar_luxation": [
        {"name_ja": "For Joint",
         "name_en": "Canine Vet For Joint",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "膝関節軟骨の保護・関節機能改善",
         "reason_en": "Knee cartilage protection and joint function improvement"},
        {"name_ja": "MSM＋アミノコンプリート",
         "name_en": "MSM + Amino Complete",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "関節周囲の炎症軽減・筋肉強化サポート",
         "reason_en": "Reduce periarticular inflammation and support muscle strengthening"},
    ],
    "cruciate_ligament_rupture": [
        {"name_ja": "For Joint",
         "name_en": "Canine Vet For Joint",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "関節機能の回復支援・軟骨保護",
         "reason_en": "Support joint function recovery and cartilage protection"},
        {"name_ja": "MSM＋アミノコンプリート",
         "name_en": "MSM + Amino Complete",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "靱帯・結合組織の修復に必要なアミノ酸・MSM補給",
         "reason_en": "Amino acids and MSM for ligament and connective tissue repair"},
        {"name_ja": "Canine Vet Protain",
         "name_en": "Canine Vet Protain",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "術後の筋肉量維持・コラーゲン合成サポート",
         "reason_en": "Maintain muscle mass and support collagen synthesis post-surgery"},
    ],

    # --- Neurological (神経) ---
    "degenerative_myelopathy": [
        {"name_ja": "For Antioxidant Asta-Melon・VitaminE・Cysteine",
         "name_en": "For Antioxidant (Astaxanthin, Melon SOD, VitE, Cysteine)",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "神経細胞の抗酸化保護・変性進行の抑制",
         "reason_en": "Antioxidant neuroprotection and slow degenerative progression"},
        {"name_ja": "MSM＋アミノコンプリート",
         "name_en": "MSM + Amino Complete",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "筋萎縮防止のためのアミノ酸補給・神経組織サポート",
         "reason_en": "Amino acids to prevent muscle atrophy and support neural tissue"},
        {"name_ja": "NMN-ミトコンドリアアシスト",
         "name_en": "NMN Mitochondria Assist",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "神経細胞のミトコンドリア機能活性化・代謝サポート",
         "reason_en": "Activate neuronal mitochondrial function and metabolic support"},
    ],
    "epilepsy": [
        {"name_ja": "Canine Vet Relax & CBD",
         "name_en": "Canine Vet Relax & CBD",
         "dosage": "体重に応じて調整", "frequency": "1日1〜2回",
         "reason_ja": "CBDによる発作閾値の上昇・神経の安定化",
         "reason_en": "CBD to raise seizure threshold and stabilize neural activity"},
        {"name_ja": "For Antioxidant Asta-Melon・VitaminE・Cysteine",
         "name_en": "For Antioxidant (Astaxanthin, Melon SOD, VitE, Cysteine)",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "脳の抗酸化保護・発作後の酸化ダメージ軽減",
         "reason_en": "Brain antioxidant protection and post-seizure oxidative damage reduction"},
        {"name_ja": "NMN-ミトコンドリアアシスト",
         "name_en": "NMN Mitochondria Assist",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "脳神経細胞のエネルギー代謝改善",
         "reason_en": "Improve energy metabolism in brain neurons"},
    ],
    "wobbler_syndrome": [
        {"name_ja": "MSM＋アミノコンプリート",
         "name_en": "MSM + Amino Complete",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "脊椎周囲の炎症軽減・神経組織サポート",
         "reason_en": "Spinal inflammation reduction and neural tissue support"},
        {"name_ja": "For Antioxidant Asta-Melon・VitaminE・Cysteine",
         "name_en": "For Antioxidant (Astaxanthin, Melon SOD, VitE, Cysteine)",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "神経保護・抗酸化作用",
         "reason_en": "Neuroprotection and antioxidant action"},
        {"name_ja": "Canine Vet Relax & CBD",
         "name_en": "Canine Vet Relax & CBD",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "頸部痛の緩和・リラックス",
         "reason_en": "Cervical pain relief and relaxation"},
    ],
    "laryngeal_paralysis": [
        {"name_ja": "For Antioxidant Asta-Melon・VitaminE・Cysteine",
         "name_en": "For Antioxidant (Astaxanthin, Melon SOD, VitE, Cysteine)",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "喉頭神経の抗酸化保護",
         "reason_en": "Antioxidant protection for laryngeal nerves"},
        {"name_ja": "Canine Vet Relax & CBD",
         "name_en": "Canine Vet Relax & CBD",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "呼吸困難時の不安緩和・リラックス",
         "reason_en": "Anxiety relief and relaxation during breathing difficulty"},
        {"name_ja": "MSM＋アミノコンプリート",
         "name_en": "MSM + Amino Complete",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "神経修復のためのアミノ酸サポート",
         "reason_en": "Amino acid support for nerve repair"},
    ],
    "lumbar_sacral_disease": [
        {"name_ja": "MSM＋アミノコンプリート",
         "name_en": "MSM + Amino Complete",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "腰仙部の炎症軽減・筋肉サポート",
         "reason_en": "Lumbosacral inflammation reduction and muscle support"},
        {"name_ja": "For Joint",
         "name_en": "Canine Vet For Joint",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "脊椎関節の保護",
         "reason_en": "Spinal joint protection"},
        {"name_ja": "Canine Vet Relax & CBD",
         "name_en": "Canine Vet Relax & CBD",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "腰仙部疼痛の緩和",
         "reason_en": "Lumbosacral pain relief"},
    ],

    # --- Dermatological (皮膚) ---
    "atopic_dermatitis": [
        {"name_ja": "For Antioxidant Asta-Melon・VitaminE・Cysteine",
         "name_en": "For Antioxidant (Astaxanthin, Melon SOD, VitE, Cysteine)",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "皮膚の抗酸化保護・炎症軽減・バリア機能改善",
         "reason_en": "Skin antioxidant protection, inflammation reduction, barrier improvement"},
        {"name_ja": "Prebiotics & Probiotics & サイリウム",
         "name_en": "Prebiotics & Probiotics & Psyllium",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "腸内免疫バランスの調整によるアレルギー反応の抑制",
         "reason_en": "Modulate allergic response via gut immune balance"},
        {"name_ja": "MSM＋アミノコンプリート",
         "name_en": "MSM + Amino Complete",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "MSMによる皮膚炎症の軽減・皮膚組織修復",
         "reason_en": "MSM for skin inflammation reduction and tissue repair"},
    ],
    "pyoderma": [
        {"name_ja": "For Antioxidant Asta-Melon・VitaminE・Cysteine",
         "name_en": "For Antioxidant (Astaxanthin, Melon SOD, VitE, Cysteine)",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "皮膚の免疫防御・抗酸化保護",
         "reason_en": "Skin immune defense and antioxidant protection"},
        {"name_ja": "MSM＋アミノコンプリート",
         "name_en": "MSM + Amino Complete",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "皮膚組織の修復促進・治癒サポート",
         "reason_en": "Promote skin tissue repair and healing"},
    ],
    "demodex_mange": [
        {"name_ja": "For Antioxidant Asta-Melon・VitaminE・Cysteine",
         "name_en": "For Antioxidant (Astaxanthin, Melon SOD, VitE, Cysteine)",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "免疫機能サポート・皮膚バリア修復",
         "reason_en": "Immune support and skin barrier repair"},
        {"name_ja": "MSM＋アミノコンプリート",
         "name_en": "MSM + Amino Complete",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "皮膚組織の再生・炎症軽減",
         "reason_en": "Skin tissue regeneration and inflammation reduction"},
        {"name_ja": "Prebiotics & Probiotics & サイリウム",
         "name_en": "Prebiotics & Probiotics & Psyllium",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "腸内免疫の強化による皮膚免疫サポート",
         "reason_en": "Skin immune support via gut immunity enhancement"},
    ],
    "allergic_dermatitis": [
        {"name_ja": "For Antioxidant Asta-Melon・VitaminE・Cysteine",
         "name_en": "For Antioxidant (Astaxanthin, Melon SOD, VitE, Cysteine)",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "アレルギー性炎症による酸化ストレスの軽減",
         "reason_en": "Reduce oxidative stress from allergic inflammation"},
        {"name_ja": "Prebiotics & Probiotics & サイリウム",
         "name_en": "Prebiotics & Probiotics & Psyllium",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "腸内免疫の調整・アレルギー反応の抑制",
         "reason_en": "Modulate intestinal immunity and suppress allergic response"},
    ],
    "food_allergy": [
        {"name_ja": "Prebiotics & Probiotics & サイリウム",
         "name_en": "Prebiotics & Probiotics & Psyllium",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "腸内環境改善・食物アレルギー反応の軽減",
         "reason_en": "Improve gut environment and reduce food allergy response"},
        {"name_ja": "For Antioxidant Asta-Melon・VitaminE・Cysteine",
         "name_en": "For Antioxidant (Astaxanthin, Melon SOD, VitE, Cysteine)",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "消化管・皮膚の抗酸化保護",
         "reason_en": "Antioxidant protection for GI tract and skin"},
    ],

    # --- Endocrine (内分泌) ---
    "hypothyroidism": [
        {"name_ja": "NMN-ミトコンドリアアシスト",
         "name_en": "NMN Mitochondria Assist",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "低下した代謝機能の活性化サポート",
         "reason_en": "Support activation of reduced metabolic function"},
        {"name_ja": "For Antioxidant Asta-Melon・VitaminE・Cysteine",
         "name_en": "For Antioxidant (Astaxanthin, Melon SOD, VitE, Cysteine)",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "代謝低下に伴う酸化ストレスの軽減",
         "reason_en": "Reduce oxidative stress associated with metabolic decline"},
        {"name_ja": "Canine Vet Booster & Relax",
         "name_en": "Canine Vet Booster & Relax",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "活力・体力の回復サポート",
         "reason_en": "Support vitality and physical recovery"},
    ],
    "cushings_disease": [
        {"name_ja": "For Antioxidant Asta-Melon・VitaminE・Cysteine",
         "name_en": "For Antioxidant (Astaxanthin, Melon SOD, VitE, Cysteine)",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "コルチゾール過剰による酸化ストレスの軽減・皮膚改善",
         "reason_en": "Reduce oxidative stress from cortisol excess and improve skin"},
        {"name_ja": "NMN-ミトコンドリアアシスト",
         "name_en": "NMN Mitochondria Assist",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "ホルモン異常による代謝機能のサポート",
         "reason_en": "Support metabolic function impaired by hormonal imbalance"},
        {"name_ja": "Prebiotics & Probiotics & サイリウム",
         "name_en": "Prebiotics & Probiotics & Psyllium",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "クッシング症候群に伴う消化器症状のサポート",
         "reason_en": "GI support for Cushing's-associated digestive issues"},
    ],
    "addisons_disease": [
        {"name_ja": "Canine Vet Booster & Relax",
         "name_en": "Canine Vet Booster & Relax",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "副腎機能低下によるエネルギー不足の改善",
         "reason_en": "Improve energy deficiency from adrenal insufficiency"},
        {"name_ja": "Prebiotics & Probiotics & サイリウム",
         "name_en": "Prebiotics & Probiotics & Psyllium",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "消化機能のサポート・ストレス性消化障害の改善",
         "reason_en": "Digestive support and stress-related GI improvement"},
        {"name_ja": "MSM＋アミノコンプリート",
         "name_en": "MSM + Amino Complete",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "ストレス対応のためのアミノ酸補給",
         "reason_en": "Amino acid supplementation for stress response"},
    ],
    "diabetes_mellitus": [
        {"name_ja": "NMN-ミトコンドリアアシスト",
         "name_en": "NMN Mitochondria Assist",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "細胞のエネルギー代謝改善・インスリン感受性サポート",
         "reason_en": "Improve cellular energy metabolism and insulin sensitivity"},
        {"name_ja": "For Antioxidant Asta-Melon・VitaminE・Cysteine",
         "name_en": "For Antioxidant (Astaxanthin, Melon SOD, VitE, Cysteine)",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "糖尿病に伴う酸化ストレスの軽減",
         "reason_en": "Reduce oxidative stress associated with diabetes"},
        {"name_ja": "Prebiotics & Probiotics & サイリウム",
         "name_en": "Prebiotics & Probiotics & Psyllium",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "サイリウムの食物繊維による血糖値安定化サポート",
         "reason_en": "Psyllium fiber for blood glucose stabilization"},
    ],
    "obesity": [
        {"name_ja": "NMN-ミトコンドリアアシスト",
         "name_en": "NMN Mitochondria Assist",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "代謝活性化・脂肪燃焼効率の改善",
         "reason_en": "Metabolic activation and improved fat burning efficiency"},
        {"name_ja": "Canine Vet Protain",
         "name_en": "Canine Vet Protain",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "減量中の筋肉量維持・タンパク質補給",
         "reason_en": "Maintain muscle mass during weight loss"},
        {"name_ja": "Prebiotics & Probiotics & サイリウム",
         "name_en": "Prebiotics & Probiotics & Psyllium",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "腸内環境改善・満腹感サポート",
         "reason_en": "Gut health and satiety support"},
    ],

    # --- Renal / Urinary (腎・泌尿器) ---
    "chronic_kidney_disease": [
        {"name_ja": "Prebiotics & Probiotics & サイリウム",
         "name_en": "Prebiotics & Probiotics & Psyllium",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "尿毒素の腸内排出促進・腸腎連関サポート",
         "reason_en": "Promote uremic toxin excretion via gut-kidney axis"},
        {"name_ja": "MSM＋アミノコンプリート",
         "name_en": "MSM + Amino Complete",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "腎機能低下による栄養不良の補正・必須アミノ酸補給",
         "reason_en": "Correct malnutrition and supply essential amino acids for renal decline"},
        {"name_ja": "NMN-ミトコンドリアアシスト",
         "name_en": "NMN Mitochondria Assist",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "腎細胞のミトコンドリア機能サポート",
         "reason_en": "Support renal cell mitochondrial function"},
    ],
    "urinary_stones": [
        {"name_ja": "Prebiotics & Probiotics & サイリウム",
         "name_en": "Prebiotics & Probiotics & Psyllium",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "尿路の健康維持・腸内環境改善による代謝サポート",
         "reason_en": "Urinary health and metabolic support via gut improvement"},
        {"name_ja": "For Antioxidant Asta-Melon・VitaminE・Cysteine",
         "name_en": "For Antioxidant (Astaxanthin, Melon SOD, VitE, Cysteine)",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "尿路の炎症・酸化ストレスの軽減",
         "reason_en": "Reduce urinary inflammation and oxidative stress"},
    ],

    # --- Cardiac (心臓) ---
    "dcm": [
        {"name_ja": "MSM＋アミノコンプリート",
         "name_en": "MSM + Amino Complete",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "心筋に必要なアミノ酸（タウリン・L-カルニチン含む）の補給",
         "reason_en": "Supply cardiac amino acids including taurine and L-carnitine"},
        {"name_ja": "For Antioxidant Asta-Melon・VitaminE・Cysteine",
         "name_en": "For Antioxidant (Astaxanthin, Melon SOD, VitE, Cysteine)",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "心筋細胞の抗酸化保護",
         "reason_en": "Antioxidant protection for cardiomyocytes"},
        {"name_ja": "NMN-ミトコンドリアアシスト",
         "name_en": "NMN Mitochondria Assist",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "心筋ミトコンドリアのエネルギー産生改善",
         "reason_en": "Improve cardiac mitochondrial energy production"},
    ],
    "mitral_valve_disease": [
        {"name_ja": "For Antioxidant Asta-Melon・VitaminE・Cysteine",
         "name_en": "For Antioxidant (Astaxanthin, Melon SOD, VitE, Cysteine)",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "心臓の抗酸化保護・心筋ダメージ軽減",
         "reason_en": "Cardiac antioxidant protection and myocardial damage reduction"},
        {"name_ja": "MSM＋アミノコンプリート",
         "name_en": "MSM + Amino Complete",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "心筋機能維持のためのアミノ酸サポート",
         "reason_en": "Amino acid support for cardiac muscle function maintenance"},
        {"name_ja": "NMN-ミトコンドリアアシスト",
         "name_en": "NMN Mitochondria Assist",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "心臓細胞のエネルギー代謝サポート",
         "reason_en": "Cardiac cellular energy metabolism support"},
    ],
    "pda": [
        {"name_ja": "For Antioxidant Asta-Melon・VitaminE・Cysteine",
         "name_en": "For Antioxidant (Astaxanthin, Melon SOD, VitE, Cysteine)",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "心臓の抗酸化保護",
         "reason_en": "Cardiac antioxidant protection"},
        {"name_ja": "NMN-ミトコンドリアアシスト",
         "name_en": "NMN Mitochondria Assist",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "心臓細胞のエネルギー産生サポート",
         "reason_en": "Support cardiac cellular energy production"},
    ],
    "aortic_stenosis": [
        {"name_ja": "For Antioxidant Asta-Melon・VitaminE・Cysteine",
         "name_en": "For Antioxidant (Astaxanthin, Melon SOD, VitE, Cysteine)",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "心筋の酸化ストレス軽減",
         "reason_en": "Reduce cardiac oxidative stress"},
        {"name_ja": "NMN-ミトコンドリアアシスト",
         "name_en": "NMN Mitochondria Assist",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "心筋エネルギー代謝の改善",
         "reason_en": "Improve cardiac energy metabolism"},
        {"name_ja": "Canine Vet Relax & CBD",
         "name_en": "Canine Vet Relax & CBD",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "運動不耐性に伴うストレスの緩和",
         "reason_en": "Stress relief for exercise intolerance"},
    ],

    # --- Ophthalmic (眼科) ---
    "cataracts": [
        {"name_ja": "For Antioxidant Asta-Melon・VitaminE・Cysteine",
         "name_en": "For Antioxidant (Astaxanthin, Melon SOD, VitE, Cysteine)",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "水晶体の抗酸化保護・白内障進行抑制（アスタキサンチン・VitE・システイン）",
         "reason_en": "Lens antioxidant protection to slow cataract progression"},
        {"name_ja": "NMN-ミトコンドリアアシスト",
         "name_en": "NMN Mitochondria Assist",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "眼組織の加齢性変化に対する細胞代謝サポート",
         "reason_en": "Cellular metabolic support against age-related ocular changes"},
    ],
    "glaucoma": [
        {"name_ja": "For Antioxidant Asta-Melon・VitaminE・Cysteine",
         "name_en": "For Antioxidant (Astaxanthin, Melon SOD, VitE, Cysteine)",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "視神経の抗酸化保護・眼内炎症の軽減",
         "reason_en": "Optic nerve antioxidant protection and intraocular inflammation reduction"},
        {"name_ja": "NMN-ミトコンドリアアシスト",
         "name_en": "NMN Mitochondria Assist",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "網膜神経節細胞のミトコンドリア保護",
         "reason_en": "Mitochondrial protection for retinal ganglion cells"},
    ],
    "pra": [
        {"name_ja": "For Antioxidant Asta-Melon・VitaminE・Cysteine",
         "name_en": "For Antioxidant (Astaxanthin, Melon SOD, VitE, Cysteine)",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "網膜細胞の抗酸化保護・変性進行の抑制",
         "reason_en": "Retinal antioxidant protection and slow degenerative progression"},
        {"name_ja": "NMN-ミトコンドリアアシスト",
         "name_en": "NMN Mitochondria Assist",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "網膜細胞のミトコンドリア機能維持",
         "reason_en": "Maintain retinal cell mitochondrial function"},
    ],
    "cherry_eye": [
        {"name_ja": "For Antioxidant Asta-Melon・VitaminE・Cysteine",
         "name_en": "For Antioxidant (Astaxanthin, Melon SOD, VitE, Cysteine)",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "眼周囲の炎症軽減・抗酸化保護",
         "reason_en": "Periocular inflammation reduction and antioxidant protection"},
    ],

    # --- Hepatic (肝臓) ---
    "liver_disease": [
        {"name_ja": "For Antioxidant Asta-Melon・VitaminE・Cysteine",
         "name_en": "For Antioxidant (Astaxanthin, Melon SOD, VitE, Cysteine)",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "肝臓の抗酸化保護・システインによる解毒サポート",
         "reason_en": "Hepatic antioxidant protection and cysteine for detox support"},
        {"name_ja": "MSM＋アミノコンプリート",
         "name_en": "MSM + Amino Complete",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "肝細胞の修復・再生に必要なアミノ酸補給",
         "reason_en": "Amino acids for hepatocyte repair and regeneration"},
        {"name_ja": "NMN-ミトコンドリアアシスト",
         "name_en": "NMN Mitochondria Assist",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "肝細胞のミトコンドリア代謝活性化",
         "reason_en": "Activate hepatocyte mitochondrial metabolism"},
    ],
    "portosystemic_shunt": [
        {"name_ja": "For Antioxidant Asta-Melon・VitaminE・Cysteine",
         "name_en": "For Antioxidant (Astaxanthin, Melon SOD, VitE, Cysteine)",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "肝臓保護・解毒機能サポート",
         "reason_en": "Liver protection and detoxification support"},
        {"name_ja": "Prebiotics & Probiotics & サイリウム",
         "name_en": "Prebiotics & Probiotics & Psyllium",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "腸内アンモニア産生の抑制・腸肝循環改善",
         "reason_en": "Reduce intestinal ammonia and improve enterohepatic circulation"},
        {"name_ja": "MSM＋アミノコンプリート",
         "name_en": "MSM + Amino Complete",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "肝機能サポートのためのアミノ酸補給",
         "reason_en": "Amino acid supply for liver function support"},
    ],

    # --- Oncology (腫瘍) ---
    "hemangiosarcoma": [
        {"name_ja": "For Antioxidant Asta-Melon・VitaminE・Cysteine",
         "name_en": "For Antioxidant (Astaxanthin, Melon SOD, VitE, Cysteine)",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "腫瘍関連の酸化ストレス軽減・細胞保護",
         "reason_en": "Reduce tumor-related oxidative stress and cell protection"},
        {"name_ja": "MSM＋アミノコンプリート",
         "name_en": "MSM + Amino Complete",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "がん悪液質予防のための栄養・アミノ酸サポート",
         "reason_en": "Nutritional and amino acid support to prevent cancer cachexia"},
        {"name_ja": "Canine Vet Protain",
         "name_en": "Canine Vet Protain",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "体力・筋肉量維持のためのタンパク質補給",
         "reason_en": "Protein supplementation to maintain strength and muscle mass"},
    ],
    "lymphoma": [
        {"name_ja": "For Antioxidant Asta-Melon・VitaminE・Cysteine",
         "name_en": "For Antioxidant (Astaxanthin, Melon SOD, VitE, Cysteine)",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "化学療法に伴う酸化ストレスの軽減",
         "reason_en": "Reduce oxidative stress from chemotherapy"},
        {"name_ja": "Prebiotics & Probiotics & サイリウム",
         "name_en": "Prebiotics & Probiotics & Psyllium",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "化学療法中の消化器サポート・腸内環境維持",
         "reason_en": "GI support and gut health during chemotherapy"},
        {"name_ja": "Canine Vet Protain",
         "name_en": "Canine Vet Protain",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "がんによる筋肉消耗の予防",
         "reason_en": "Prevent cancer-related muscle wasting"},
    ],
    "osteosarcoma": [
        {"name_ja": "MSM＋アミノコンプリート",
         "name_en": "MSM + Amino Complete",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "骨・筋肉組織のサポート・栄養補給",
         "reason_en": "Bone and muscle tissue support and nutrition"},
        {"name_ja": "For Joint",
         "name_en": "Canine Vet For Joint",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "残存関節・対側肢の関節保護",
         "reason_en": "Protect remaining joints and contralateral limb"},
        {"name_ja": "Canine Vet Protain",
         "name_en": "Canine Vet Protain",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "術後・療養中の体力維持",
         "reason_en": "Maintain strength during treatment and post-surgery"},
    ],
    "mast_cell_tumor": [
        {"name_ja": "For Antioxidant Asta-Melon・VitaminE・Cysteine",
         "name_en": "For Antioxidant (Astaxanthin, Melon SOD, VitE, Cysteine)",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "腫瘍関連炎症の調節・抗酸化保護",
         "reason_en": "Modulate tumor inflammation and antioxidant protection"},
        {"name_ja": "MSM＋アミノコンプリート",
         "name_en": "MSM + Amino Complete",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "免疫機能サポートのためのアミノ酸・MSM補給",
         "reason_en": "Amino acid and MSM for immune function support"},
    ],
    "mammary_gland_tumor": [
        {"name_ja": "For Antioxidant Asta-Melon・VitaminE・Cysteine",
         "name_en": "For Antioxidant (Astaxanthin, Melon SOD, VitE, Cysteine)",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "抗酸化保護・腫瘍関連酸化ストレスの軽減",
         "reason_en": "Antioxidant protection and tumor-related oxidative stress reduction"},
        {"name_ja": "MSM＋アミノコンプリート",
         "name_en": "MSM + Amino Complete",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "体力維持のためのアミノ酸サポート",
         "reason_en": "Amino acid support for maintaining strength"},
        {"name_ja": "Canine Vet Protain",
         "name_en": "Canine Vet Protain",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "術後回復・筋肉量維持のためのタンパク質補給",
         "reason_en": "Protein for post-surgical recovery and muscle maintenance"},
    ],

    # --- Hematologic (血液) ---
    "von_willebrand_disease": [
        {"name_ja": "MSM＋アミノコンプリート",
         "name_en": "MSM + Amino Complete",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "出血による栄養損失の補正・組織修復アミノ酸",
         "reason_en": "Correct nutritional loss from bleeding and tissue repair amino acids"},
        {"name_ja": "No Pain Quick Stop",
         "name_en": "No Pain Quick Stop",
         "dosage": "出血時に患部に適量塗布", "frequency": "出血時",
         "reason_ja": "外傷・爪切り等の出血時の迅速な止血",
         "reason_en": "Rapid hemostasis for wounds and nail trimming bleeds"},
    ],
    "imha": [
        {"name_ja": "For Antioxidant Asta-Melon・VitaminE・Cysteine",
         "name_en": "For Antioxidant (Astaxanthin, Melon SOD, VitE, Cysteine)",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "赤血球膜の抗酸化保護・免疫介在性ダメージ軽減",
         "reason_en": "RBC membrane antioxidant protection and immune-mediated damage reduction"},
        {"name_ja": "MSM＋アミノコンプリート",
         "name_en": "MSM + Amino Complete",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "貧血による栄養不足の補正・赤血球産生サポート",
         "reason_en": "Correct nutritional deficiency from anemia and support RBC production"},
        {"name_ja": "NMN-ミトコンドリアアシスト",
         "name_en": "NMN Mitochondria Assist",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "貧血時の細胞エネルギー代謝サポート",
         "reason_en": "Cellular energy metabolism support during anemia"},
    ],

    # --- Ear (耳) ---
    "otitis_externa": [
        {"name_ja": "For Antioxidant Asta-Melon・VitaminE・Cysteine",
         "name_en": "For Antioxidant (Astaxanthin, Melon SOD, VitE, Cysteine)",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "耳道の炎症・酸化ストレス軽減",
         "reason_en": "Reduce ear canal inflammation and oxidative stress"},
        {"name_ja": "Prebiotics & Probiotics & サイリウム",
         "name_en": "Prebiotics & Probiotics & Psyllium",
         "dosage": "体重に応じて調整", "frequency": "1日1回",
         "reason_ja": "全身免疫の強化による耳道感染の再発予防",
         "reason_en": "Prevent ear infection recurrence via systemic immune support"},
    ],
}

# Default fallback supplement for diseases without specific mapping
_DEFAULT_SUPPLEMENTS = [
    {"name_ja": "For Antioxidant Asta-Melon・VitaminE・Cysteine",
     "name_en": "For Antioxidant (Astaxanthin, Melon SOD, VitE, Cysteine)",
     "dosage": "体重に応じて調整", "frequency": "1日1回",
     "reason_ja": "全般的な抗酸化・健康サポート",
     "reason_en": "General antioxidant and health support"},
    {"name_ja": "MSM＋アミノコンプリート",
     "name_en": "MSM + Amino Complete",
     "dosage": "体重に応じて調整", "frequency": "1日1回",
     "reason_ja": "全般的なアミノ酸・栄養サポート",
     "reason_en": "General amino acid and nutritional support"},
]


def get_treatment_recommendations_for_disease(disease_id: str, breed_id=None, age_years=None) -> dict:
    """Get care guide including supplement reference and test information."""
    disease_record = next((d for d in DISEASES if d["id"] == disease_id), {})

    if disease_id:
        supplements = DISEASE_SUPPLEMENTS.get(disease_id, _DEFAULT_SUPPLEMENTS)
        supplements = [
            {**s, "reference": "https://www.caninevet.jp/"} for s in supplements
        ]
    else:
        supplements = []

    recommendations = {
        "primary_care_plan_ja": "こちらは参考情報です（獣医師監修：上手健太郎／南相馬動物病院）。具体的なケアについては獣医師にご相談ください。",
        "primary_care_plan_en": "This is reference information (supervised by Kentaro Kaimide, DVM / Minamisoma Vet Clinic). Please consult a veterinarian for specific care.",
        "supplements": supplements,
        "diagnostic_tests": [
            {
                "test_id": test_id,
                "test_name_ja": test_id.replace("_", " ").title(),
                "test_name_en": test_id.replace("_", " ").title(),
                "priority": idx + 1,
                "description_ja": "獣医師指示による検査",
                "description_en": "Veterinary recommended test"
            }
            for idx, test_id in enumerate(disease_record.get("recommended_tests", [])[:3])
        ],
        "follow_up_schedule_ja": "初診より2週間後の再診を推奨",
        "follow_up_schedule_en": "Follow-up recommended in 2 weeks"
    }

    return recommendations


def match_symptoms_to_diseases(symptom_ids: list) -> list:
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

def _build_follow_up_questions(
    onset: str | None,
    age: float | None,
    symptoms: list,
) -> list[dict]:
    """Build context-aware follow-up questions for the chat UI.

    If onset or age information is missing, suggest the user provide it.
    """
    questions = []

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
                {"value": 0.5, "label_ja": "1歳未満（子犬/子猫）", "label_en": "Under 1 year (puppy/kitten)"},
                {"value": 2.0, "label_ja": "1〜3歳（若齢）", "label_en": "1–3 years (young)"},
                {"value": 5.0, "label_ja": "3〜7歳（成犬/成猫）", "label_en": "3–7 years (adult)"},
                {"value": 10.0, "label_ja": "7歳以上（高齢）", "label_en": "7+ years (senior)"},
            ],
        })

    if not symptoms:
        questions.append({
            "question_ja": "どのような症状がありますか？",
            "question_en": "What symptoms are you seeing?",
            "type": "symptoms",
            "options": [],
        })

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
    previous_symptoms = data.get("previous_symptoms", [])
    species = data.get("species", "dog")
    data.get("gender")  # "male" | "female" (optional)

    if not message:
        return jsonify({"error": "Message required"}), 400

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
    elif species in _SPECIES_DATA:
        extracted = _extract_species_symptoms(message, species)
        all_symptoms = list(set(extracted + previous_symptoms))
        disease_matches = _match_species_symptoms_to_diseases(all_symptoms, species)
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
        disease_matches = match_symptoms_to_diseases(all_symptoms)
        symptom_details = [
            {
                "id": sid,
                "name_ja": next((s["name_ja"] for s in SYMPTOMS if s["id"] == sid), ""),
                "name_en": next((s["name_en"] for s in SYMPTOMS if s["id"] == sid), ""),
                "category": next((s["category"] for s in SYMPTOMS if s["id"] == sid), ""),
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

        enhanced_candidates.append({
            **disease,
            "reasoning": reasoning,
            "treatment_recommendations": treatments,
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
        "breed_context": breed_id,
        "age_context": effective_age,
        "onset_context": effective_onset,
        "onset_detected_from_text": detected_onset,
        "age_detected_from_text": detected_age,
        "follow_up_questions": _build_follow_up_questions(
            effective_onset, effective_age, all_symptoms
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

    disease_1 = next((d for d in DISEASES if d["id"] == disease_id_1), None)
    disease_2 = next((d for d in DISEASES if d["id"] == disease_id_2), None)

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

    disease = next((d for d in DISEASES if d["id"] == disease_id), None)

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
            logger.warning(f"Failed to record learning feedback: {e}")
            # Fallback: still record basic feedback
            return jsonify({
                "status": "recorded",
                "learning_signal_strength": 0,
                "note": "feedback recorded (learning unavailable)",
            }), 201

    except Exception as e:
        logger.error(f"Error recording diagnostic feedback: {e}")
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
        logger.error(f"Error generating next questions: {e}", exc_info=True)
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
        logger.error(f"Error in multi-disease analysis: {e}", exc_info=True)
        return jsonify({"error": "multidisease_analysis_failed"}), 500
