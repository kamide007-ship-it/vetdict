"""Common helpers for species-specific disease analysis.

This module provides a generic `analyze_symptoms_generic` function that can be
used by each species-specific module to perform basic differential diagnosis.
It mirrors the dog symptom checker output structure but operates on a custom
disease list and symptom name mapping. A shared advice dictionary is also
defined here for consistent messaging across species.
"""

from __future__ import annotations

import json
import math as _math
import os
from typing import Any, Dict, List, Set

# =============================================================================
# ENRICHMENT: Load supplementary fields from diseases_all_species.json
# =============================================================================
# The species module .py files define symptoms/urgency/recommended_tests for
# differential diagnosis. The JSON database has enriched content fields
# (pathophysiology, causes, treatment, prevention, prognosis, etc.).
# This loader merges them so the differential diagnosis cards show full content.

_ENRICHMENT_DATA: Dict[str, Dict[str, Any]] | None = None
_SUPPLEMENTARY_DATA: Dict[str, List[Dict[str, Any]]] | None = None
_ENRICHMENT_FIELDS = (
    "pathophysiology", "pathophysiology_ja",
    "causes", "causes_ja",
    "treatment", "treatment_ja",
    "prevention", "prevention_ja",
    "prognosis", "prognosis_ja",
    "clinical_signs", "clinical_signs_ja",
    "diagnosis", "diagnosis_ja",
    "transmission", "transmission_ja",
    "recommended_tests",
)


import re as _re

# Species prefix patterns used for normalized matching
_SPECIES_PREFIXES = (
    "canine ", "feline ", "equine ", "avian ", "porcine ",
    "bovine ", "ovine ", "caprine ",
)


def _normalize_disease_name(name: str) -> str:
    """Normalize a disease name for fuzzy matching.

    Strips parenthetical content, species prefixes, and normalises whitespace/case.
    """
    n = name.lower().strip()
    # Remove parenthetical content: "(Bloat)", "(URI)", "(HCM)" etc.
    n = _re.sub(r"\s*\([^)]*\)", "", n)
    # Remove species prefixes
    for prefix in _SPECIES_PREFIXES:
        if n.startswith(prefix):
            n = n[len(prefix):]
    # Remove slash-separated alternatives: "Shell Fracture / Trauma" -> "shell fracture"
    if " / " in n:
        n = n.split(" / ")[0]
    # Collapse whitespace
    n = _re.sub(r"\s+", " ", n).strip()
    return n


def _extract_all_name_variants(name: str) -> List[str]:
    """Generate multiple normalized variants for a disease name.

    Handles parenthetical swaps like 'Ringworm (Dermatophytosis)' producing
    both 'ringworm' and 'dermatophytosis'.
    """
    variants: List[str] = [_normalize_disease_name(name)]
    lower = name.lower().strip()

    # Extract parenthetical content and use it as an alternative name
    paren_match = _re.search(r"^([^(]+)\(([^)]+)\)", lower)
    if paren_match:
        main_part = paren_match.group(1).strip()
        paren_part = paren_match.group(2).strip()
        # Remove species prefixes from both
        for prefix in _SPECIES_PREFIXES:
            if main_part.startswith(prefix):
                main_part = main_part[len(prefix):]
            if paren_part.startswith(prefix):
                paren_part = paren_part[len(prefix):]
        # "Ringworm (Dermatophytosis)" -> also try "dermatophytosis"
        variants.append(paren_part)
        # "Ringworm (Dermatophytosis)" -> also try "dermatophytosis (ringworm)"
        variants.append(f"{paren_part} ({main_part})")

    # Slash alternatives: "Shell Fracture / Trauma" -> also keep full without parens
    if " / " in lower:
        parts = lower.split(" / ")
        for part in parts:
            part = part.strip()
            for prefix in _SPECIES_PREFIXES:
                if part.startswith(prefix):
                    part = part[len(prefix):]
            variants.append(part)

    return list(dict.fromkeys(variants))  # dedupe, preserve order


# Secondary index for normalized lookups: {(species, normalized_name): entry}
_ENRICHMENT_NORMALIZED: Dict[str, Dict[str, Any]] | None = None
# Index for "Multiple"-species entries (cross-species diseases)
_ENRICHMENT_MULTI: Dict[str, Dict[str, Any]] | None = None


def _load_enrichment_data() -> Dict[str, Dict[str, Any]]:
    """Load enrichment data from JSON, keyed by (species, name)."""
    global _ENRICHMENT_DATA, _ENRICHMENT_NORMALIZED, _ENRICHMENT_MULTI
    if _ENRICHMENT_DATA is not None:
        return _ENRICHMENT_DATA
    _ENRICHMENT_DATA = {}
    _ENRICHMENT_NORMALIZED = {}
    _ENRICHMENT_MULTI = {}
    db_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "diseases_all_species.json",
    )
    try:
        with open(db_path, encoding="utf-8") as f:
            for entry in json.load(f):
                sp = entry.get("species", "")
                nm = entry.get("name", "")
                _ENRICHMENT_DATA[(sp, nm)] = entry
                # Build normalized index with all variants
                for variant in _extract_all_name_variants(nm):
                    key = (sp, variant)
                    if key not in _ENRICHMENT_NORMALIZED:
                        _ENRICHMENT_NORMALIZED[key] = entry
                    # Index "Multiple" species entries by normalized name
                    if sp == "Multiple" and variant not in _ENRICHMENT_MULTI:
                        _ENRICHMENT_MULTI[variant] = entry
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return _ENRICHMENT_DATA


def _load_supplementary_data() -> Dict[str, List[Dict[str, Any]]]:
    """Load supplementary diseases (JSON-only diseases with inferred symptom sets).

    Returns a dict keyed by species name → list of disease dicts.
    """
    global _SUPPLEMENTARY_DATA
    if _SUPPLEMENTARY_DATA is not None:
        return _SUPPLEMENTARY_DATA
    _SUPPLEMENTARY_DATA = {}
    supp_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "data",
        "supplementary_diseases.json",
    )
    try:
        with open(supp_path, encoding="utf-8") as f:
            for entry in json.load(f):
                sp = entry.get("species", "")
                _SUPPLEMENTARY_DATA.setdefault(sp, []).append(entry)
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return _SUPPLEMENTARY_DATA


def _find_enrichment(species: str, disease_name: str) -> Dict[str, Any] | None:
    """Find enrichment data for a disease using multi-level matching.

    Matching order:
    1. Exact (species, name)
    2. Normalized (species, normalized_name)
    3. Cross-species "Multiple" by normalized name
    """
    data = _load_enrichment_data()

    # Level 1: exact match
    entry = data.get((species, disease_name))
    if entry:
        return entry

    # Level 2: normalized match within same species (try all variants)
    if _ENRICHMENT_NORMALIZED is not None:
        for variant in _extract_all_name_variants(disease_name):
            entry = _ENRICHMENT_NORMALIZED.get((species, variant))
            if entry:
                return entry

    # Level 3: substring / containment match within same species
    # e.g. "Adrenal Disease" matches "Adrenal Gland Disease"
    # Require the shorter string to be at least 60% of the longer to avoid spurious matches.
    if _ENRICHMENT_NORMALIZED is not None:
        query_variants = _extract_all_name_variants(disease_name)
        species_entries = [
            (k[1], v) for k, v in _ENRICHMENT_NORMALIZED.items() if k[0] == species
        ]
        for variant in query_variants:
            if len(variant) < 8:
                continue  # skip very short variants to avoid false matches
            for norm_name, entry in species_entries:
                if len(norm_name) < 8:
                    continue
                shorter, longer = (variant, norm_name) if len(variant) <= len(norm_name) else (norm_name, variant)
                if shorter in longer and len(shorter) / len(longer) >= 0.6:
                    return entry

    # Level 4: cross-species "Multiple" entries (try all variants)
    if _ENRICHMENT_MULTI is not None:
        for variant in _extract_all_name_variants(disease_name):
            entry = _ENRICHMENT_MULTI.get(variant)
            if entry:
                return entry

    return None


def _generate_fallback_content(disease: Dict[str, Any], species: str) -> Dict[str, str]:
    """Generate fallback content fields from the disease's existing description/name."""
    name = disease.get("name", "")
    name_ja = disease.get("name_ja", name)
    desc = disease.get("description", "")
    urgency = disease.get("urgency", "moderate")

    urgency_ja = {"emergency": "緊急", "high": "高", "moderate": "中等度", "low": "軽度"}.get(urgency, "中等度")

    content: Dict[str, str] = {}

    if not disease.get("pathophysiology"):
        content["pathophysiology"] = (
            f"{name} involves pathological changes in affected tissues and organ systems. "
            f"{desc} The condition progresses through stages of cellular injury, inflammatory response, "
            f"and potential tissue damage if left untreated."
        )
    if not disease.get("pathophysiology_ja"):
        # Prefer description_ja over generic template
        desc_ja = disease.get("description_ja", "")
        if desc_ja:
            content["pathophysiology_ja"] = desc_ja
        else:
            content["pathophysiology_ja"] = (
                f"{name_ja}は罹患組織および臓器系に病理学的変化をもたらす。"
                f"細胞障害・炎症反応・未治療の場合の組織損傷の段階を経て進行する。"
                f"早期の病態把握と介入が予後改善の鍵となる。"
            )
    if not disease.get("causes"):
        content["causes"] = (
            f"The causes of {name.lower()} in {species.lower()} include predisposing factors "
            f"related to genetics, environment, diet, and husbandry. {desc}"
        )
    if not disease.get("causes_ja"):
        desc_ja = disease.get("description_ja", "")
        if desc_ja:
            content["causes_ja"] = desc_ja
        else:
            content["causes_ja"] = (
                f"{name_ja}の原因には遺伝的要因、環境要因、食事・飼育管理に関連する素因が含まれる。"
                f"複数の要因が複合的に作用することが多い。"
            )
    if not disease.get("treatment"):
        content["treatment"] = (
            f"Treatment of {name.lower()} in {species.lower()} involves addressing the underlying cause, "
            f"supportive care, and species-appropriate therapeutic interventions. "
            f"Severity level: {urgency}. Consult a veterinarian experienced with {species.lower()} medicine."
        )
    if not disease.get("treatment_ja"):
        content["treatment_ja"] = (
            f"{name_ja}の治療は原因への対処、支持療法、および種に適した治療介入を含む。"
            f"重症度: {urgency_ja}。{species}の診療経験のある獣医師への相談が推奨される。"
        )
    if not disease.get("prevention"):
        content["prevention"] = (
            f"Prevention of {name.lower()} includes appropriate husbandry, proper diet, "
            f"regular veterinary check-ups, stress minimization, and maintaining a clean environment."
        )
    if not disease.get("prevention_ja"):
        content["prevention_ja"] = (
            f"{name_ja}の予防には適切な飼育管理、適正な食事、定期的な健康診断、"
            f"ストレスの最小化、清潔な環境の維持が含まれる。"
        )
    if not disease.get("prognosis"):
        content["prognosis"] = (
            f"Prognosis for {name.lower()} depends on severity, timeliness of diagnosis, "
            f"and response to treatment. Early detection and appropriate intervention improve outcomes."
        )
    if not disease.get("prognosis_ja"):
        content["prognosis_ja"] = (
            f"{name_ja}の予後は重症度、診断の迅速さ、治療への反応に依存する。"
            f"早期発見と適切な介入が転帰を改善する。"
        )
    return content


_TEMPLATE_MARKERS = (
    "適切な飼育管理、種に合ったバランスの取れた栄養、定期的な健康診断、ストレスの最小化、清潔な生活環境の維持",
    "適切な飼育管理、バランスの取れた栄養、定期的な獣医師による健康診断",
    "Proper husbandry, balanced nutrition, regular veterinary",
    "involves pathological changes in affected tissues and organ systems",
    "Prognosis depends on severity, timeliness of diagnosis",
)


def _is_template_text(value: str) -> bool:
    """Return True if the value contains known template/boilerplate text."""
    if not value:
        return False
    return any(marker in value for marker in _TEMPLATE_MARKERS)


def enrich_diseases(diseases: List[Dict[str, Any]], species: str) -> List[Dict[str, Any]]:
    """Merge enrichment fields from JSON into a species module's DISEASES list.

    Fills in fields that are missing, empty, or contain template text in the
    module definition, preserving any hand-curated content already present.
    Uses multi-level matching (exact → normalized → cross-species) before
    falling back to generated template content.

    Also appends supplementary diseases (from supplementary_diseases.json) that
    exist in the JSON database but not yet in the module's DISEASES list, so
    they can participate in differential diagnosis.
    """
    _load_enrichment_data()  # ensure indices are built

    # Append supplementary diseases that are not already in the module
    supp = _load_supplementary_data()
    existing_names: Set[str] = {d.get("name", "").lower() for d in diseases}
    for sd in supp.get(species, []):
        if sd.get("name", "").lower() not in existing_names:
            diseases.append(sd)
            existing_names.add(sd.get("name", "").lower())

    for disease in diseases:
        enrichment = _find_enrichment(species, disease.get("name", ""))
        if enrichment:
            for field in _ENRICHMENT_FIELDS:
                current = disease.get(field, "")
                replacement = enrichment.get(field, "")
                # Replace if empty OR if current is template but replacement is not
                if (not current and replacement) or (_is_template_text(current) and replacement and not _is_template_text(replacement)):
                    disease[field] = replacement
            if not disease.get("description_ja") and enrichment.get("description_ja"):
                disease["description_ja"] = enrichment["description_ja"]
            if not disease.get("name_ja") and enrichment.get("name_ja"):
                disease["name_ja"] = enrichment["name_ja"]
        # Always apply fallback for fields still missing after enrichment
        fallback = _generate_fallback_content(disease, species)
        for field, value in fallback.items():
            if not disease.get(field):
                disease[field] = value
    return diseases

# Import gender risk data
try:
    from api.data.gender_prevalence import GENDER_RISK_MULTIPLIERS
except ImportError:
    GENDER_RISK_MULTIPLIERS = {}

# Import extended symptom combinations
try:
    from api.data.symptom_combinations import (
        EXTENDED_SYMPTOM_PAIR_BOOST,
        SYMPTOM_TRIPLE_BOOST,
    )
except ImportError:
    EXTENDED_SYMPTOM_PAIR_BOOST = {}
    SYMPTOM_TRIPLE_BOOST = {}

# Default advice messages for various severity levels. These are used when
# species-specific modules do not supply their own advice dictionary.
ADVICE: Dict[str, Dict[str, str]] = {
    "low": {
        "en": "Low severity: Monitor the condition and consult a veterinarian if symptoms worsen.",
        "ja": "軽度: 様子を見て、症状が悪化した場合は獣医師に相談してください。",
    },
    "moderate": {
        "en": "Moderate severity: It is advisable to have the animal examined by a veterinarian soon.",
        "ja": "中等度: 早めに獣医師の診察を受けることをお勧めします。",
    },
    "high": {
        "en": "High severity: Prompt veterinary care is recommended.",
        "ja": "重度: 速やかに獣医師の診察を受けてください。",
    },
    "emergency": {
        "en": "Emergency: Seek immediate veterinary attention.",
        "ja": "緊急: 直ちに獣医師の診察を受けてください。",
    },
}


# =============================================================================
# BREED DATA PER SPECIES
# =============================================================================
# Each species maps breed_id -> {name, name_ja, risk: {disease_name: multiplier}}

SPECIES_BREEDS: Dict[str, List[Dict[str, Any]]] = {
    "cat": [
        {"id": "cat_mixed", "name": "Mixed Breed", "name_ja": "雑種（ミックス）",
         "risk": {},
         "ecology": {"temperature": {"min": 18, "max": 29, "unit": "°C"},
                     "humidity": {"min": 30, "max": 70, "unit": "%"},
                     "lifespan": {"min": 12, "max": 18, "unit": "years"},
                     "weight": {"min": 3.0, "max": 6.0, "unit": "kg"},
                     "diet": "Obligate carnivore; balanced commercial cat food with taurine supplementation",
                     "diet_ja": "完全肉食性。タウリン含有の総合栄養食",
                     "housing": "Indoor preferred; safe outdoor access optional with escape-proof enclosure",
                     "housing_ja": "室内飼育推奨。屋外は脱走防止柵付きが望ましい",
                     "notes": "Varies widely by genetic background; regular veterinary checkups recommended",
                     "notes_ja": "遺伝的背景が多様。定期的な健康診断を推奨"}},
        {"id": "cat_persian", "name": "Persian", "name_ja": "ペルシャ",
         "risk": {"Polycystic Kidney Disease (PKD)": 2.5, "Feline Hypertrophic Cardiomyopathy (HCM)": 1.5,
                  "Feline Chronic Kidney Disease (CKD)": 1.8, "Brachycephalic Airway Syndrome": 2.0, "Saddle Nose Deformity (Brachycephalic Airway Syndrome)": 2.0,
                  "Feline Lower Urinary Tract Disease (FLUTD)": 1.3},
         "ecology": {"temperature": {"min": 18, "max": 27, "unit": "°C"},
                     "humidity": {"min": 30, "max": 60, "unit": "%"},
                     "lifespan": {"min": 12, "max": 17, "unit": "years"},
                     "weight": {"min": 3.0, "max": 5.5, "unit": "kg"},
                     "diet": "Obligate carnivore; flat-faced breed formula recommended to ease food pickup",
                     "diet_ja": "完全肉食性。短頭種用フードで食べやすさに配慮",
                     "housing": "Indoor only; air-conditioned environment in hot climates due to brachycephalic airway",
                     "housing_ja": "完全室内飼育。短頭種のため暑い時期はエアコン必須",
                     "notes": "Daily grooming required for long coat; regular eye cleaning due to tear staining; monitor breathing",
                     "notes_ja": "長毛のため毎日のブラッシングが必要。流涙症のケアと呼吸状態の観察を行う"}},
        {"id": "cat_scottish_fold", "name": "Scottish Fold", "name_ja": "スコティッシュフォールド",
         "risk": {"Scottish Fold Osteochondrodysplasia": 3.0, "Feline Hypertrophic Cardiomyopathy (HCM)": 1.8,
                  "Polycystic Kidney Disease (PKD)": 1.5, "Osteoarthritis (Degenerative Joint Disease)": 2.0},
         "ecology": {"temperature": {"min": 18, "max": 28, "unit": "°C"},
                     "humidity": {"min": 30, "max": 65, "unit": "%"},
                     "lifespan": {"min": 11, "max": 15, "unit": "years"},
                     "weight": {"min": 2.7, "max": 6.0, "unit": "kg"},
                     "diet": "Obligate carnivore; joint-support formula with glucosamine/chondroitin recommended",
                     "diet_ja": "完全肉食性。関節サポート成分（グルコサミン・コンドロイチン）配合フード推奨",
                     "housing": "Indoor only; soft bedding to reduce joint stress",
                     "housing_ja": "完全室内飼育。関節負担軽減のため柔らかい寝床を用意",
                     "notes": "Never breed fold-to-fold; monitor joints and mobility closely; ear cleaning important for folded ears",
                     "notes_ja": "フォールド同士の交配は厳禁。関節と歩行状態を注意深く観察。折れ耳の定期的な清掃が必要"}},
        {"id": "cat_munchkin", "name": "Munchkin", "name_ja": "マンチカン",
         "risk": {"Osteoarthritis": 2.0, "Intervertebral Disc Disease": 1.8,
                  "Lordosis": 1.5},
         "ecology": {"temperature": {"min": 18, "max": 28, "unit": "°C"},
                     "humidity": {"min": 30, "max": 65, "unit": "%"},
                     "lifespan": {"min": 12, "max": 15, "unit": "years"},
                     "weight": {"min": 2.5, "max": 4.0, "unit": "kg"},
                     "diet": "Obligate carnivore; weight management important to reduce spinal/joint load",
                     "diet_ja": "完全肉食性。脊椎・関節への負担軽減のため体重管理が重要",
                     "housing": "Indoor only; low-entry litter boxes and ramps to reduce jumping strain",
                     "housing_ja": "完全室内飼育。入口の低いトイレやスロープで跳躍負荷を軽減",
                     "notes": "Monitor spine and joints; avoid obesity; short legs may limit jumping ability",
                     "notes_ja": "脊椎と関節を観察。肥満防止。短足のためジャンプ力が制限される場合あり"}},
        {"id": "cat_american_shorthair", "name": "American Shorthair", "name_ja": "アメリカンショートヘア",
         "risk": {"Feline Hypertrophic Cardiomyopathy (HCM)": 1.5, "Obesity": 1.3},
         "ecology": {"temperature": {"min": 18, "max": 29, "unit": "°C"},
                     "humidity": {"min": 30, "max": 70, "unit": "%"},
                     "lifespan": {"min": 15, "max": 20, "unit": "years"},
                     "weight": {"min": 3.5, "max": 6.5, "unit": "kg"},
                     "diet": "Obligate carnivore; calorie-controlled diet to prevent obesity",
                     "diet_ja": "完全肉食性。肥満予防のためカロリー管理が重要",
                     "housing": "Indoor preferred; adaptable to various environments",
                     "housing_ja": "室内飼育推奨。環境適応力が高い",
                     "notes": "Hardy breed; prone to weight gain so monitor food intake and encourage play",
                     "notes_ja": "丈夫な品種。太りやすいため食事量の管理と運動の促進が必要"}},
        {"id": "cat_russian_blue", "name": "Russian Blue", "name_ja": "ロシアンブルー",
         "risk": {"Feline Lower Urinary Tract Disease (FLUTD)": 1.5, "Obesity": 1.5},
         "ecology": {"temperature": {"min": 18, "max": 28, "unit": "°C"},
                     "humidity": {"min": 30, "max": 65, "unit": "%"},
                     "lifespan": {"min": 15, "max": 20, "unit": "years"},
                     "weight": {"min": 3.0, "max": 5.5, "unit": "kg"},
                     "diet": "Obligate carnivore; urinary health formula recommended; monitor water intake",
                     "diet_ja": "完全肉食性。尿路ケア用フード推奨。飲水量の確認",
                     "housing": "Indoor only; quiet environment preferred as breed is sensitive to stress",
                     "housing_ja": "完全室内飼育。ストレスに敏感なため静かな環境が望ましい",
                     "notes": "Shy and sensitive to change; encourage water intake to prevent FLUTD; dense double coat sheds seasonally",
                     "notes_ja": "シャイで環境変化に敏感。FLUTD予防のため飲水を促す。密なダブルコートは換毛期に抜ける"}},
        {"id": "cat_norwegian_forest", "name": "Norwegian Forest Cat", "name_ja": "ノルウェージャンフォレストキャット",
         "risk": {"Feline Hypertrophic Cardiomyopathy (HCM)": 1.8, "Hip Dysplasia": 1.5,
                  "Glycogen Storage Disease Type IV": 2.0},
         "ecology": {"temperature": {"min": 10, "max": 28, "unit": "°C"},
                     "humidity": {"min": 30, "max": 70, "unit": "%"},
                     "lifespan": {"min": 14, "max": 16, "unit": "years"},
                     "weight": {"min": 4.0, "max": 9.0, "unit": "kg"},
                     "diet": "Obligate carnivore; large-breed formula for slow, steady growth",
                     "diet_ja": "完全肉食性。大型猫用フードでゆっくり安定した成長を促す",
                     "housing": "Indoor with climbing structures; tolerates cold well due to thick double coat",
                     "housing_ja": "キャットタワー付きの室内飼育。厚いダブルコートで寒さに強い",
                     "notes": "Regular brushing 2-3 times per week; slow to mature (up to 5 years); screen for GSD IV",
                     "notes_ja": "週2〜3回のブラッシング。成熟に最大5年。GSD IVのスクリーニング推奨"}},
        {"id": "cat_maine_coon", "name": "Maine Coon", "name_ja": "メインクーン",
         "risk": {"Feline Hypertrophic Cardiomyopathy (HCM)": 2.5, "Hip Dysplasia": 1.8,
                  "Spinal Muscular Atrophy": 1.5, "Polycystic Kidney Disease (PKD)": 1.3},
         "ecology": {"temperature": {"min": 10, "max": 28, "unit": "°C"},
                     "humidity": {"min": 30, "max": 70, "unit": "%"},
                     "lifespan": {"min": 12, "max": 15, "unit": "years"},
                     "weight": {"min": 5.0, "max": 11.0, "unit": "kg"},
                     "diet": "Obligate carnivore; large-breed kitten formula during growth; joint-support diet for adults",
                     "diet_ja": "完全肉食性。成長期は大型猫用キトンフード、成猫は関節サポート食",
                     "housing": "Indoor with sturdy climbing structures; needs space due to large size",
                     "housing_ja": "頑丈なキャットタワー付きの広い室内。大型のためスペースが必要",
                     "notes": "Cardiac screening (echocardiography) recommended; slow to mature; regular grooming of semi-long coat",
                     "notes_ja": "心臓超音波検査を推奨。成熟に3〜5年。セミロングコートの定期的なグルーミングが必要"}},
        {"id": "cat_ragdoll", "name": "Ragdoll", "name_ja": "ラグドール",
         "risk": {"Feline Hypertrophic Cardiomyopathy (HCM)": 2.0, "Feline Lower Urinary Tract Disease (FLUTD)": 1.5,
                  "Bladder Stones": 1.3, "Urolithiasis (Bladder Stones)": 1.3},
         "ecology": {"temperature": {"min": 18, "max": 28, "unit": "°C"},
                     "humidity": {"min": 30, "max": 65, "unit": "%"},
                     "lifespan": {"min": 12, "max": 17, "unit": "years"},
                     "weight": {"min": 4.0, "max": 9.0, "unit": "kg"},
                     "diet": "Obligate carnivore; urinary health diet recommended; ensure adequate water intake",
                     "diet_ja": "完全肉食性。尿路ケア食推奨。十分な飲水を確保",
                     "housing": "Indoor only; gentle breed suited to calm households",
                     "housing_ja": "完全室内飼育。穏やかな性格で静かな家庭に適する",
                     "notes": "Regular grooming for semi-long coat; docile temperament — monitor for injuries as they may not show pain",
                     "notes_ja": "セミロングコートの定期グルーミング。おとなしいため痛みを見せにくく怪我に注意"}},
        {"id": "cat_bengal", "name": "Bengal", "name_ja": "ベンガル",
         "risk": {"Feline Hypertrophic Cardiomyopathy (HCM)": 1.5, "Progressive Retinal Atrophy (PRA)": 2.0,
                  "Feline Infectious Peritonitis (FIP)": 1.3},
         "ecology": {"temperature": {"min": 18, "max": 29, "unit": "°C"},
                     "humidity": {"min": 30, "max": 70, "unit": "%"},
                     "lifespan": {"min": 12, "max": 16, "unit": "years"},
                     "weight": {"min": 3.5, "max": 7.0, "unit": "kg"},
                     "diet": "Obligate carnivore; high-protein diet to match high energy level",
                     "diet_ja": "完全肉食性。高い活動量に見合う高タンパク食",
                     "housing": "Indoor with extensive enrichment; climbing structures, puzzle feeders, and water features appreciated",
                     "housing_ja": "豊富な環境エンリッチメント付きの室内飼育。キャットタワー、知育玩具、ウォーターファウンテン推奨",
                     "notes": "Very active and intelligent; needs mental stimulation; PRA DNA testing recommended for breeders",
                     "notes_ja": "非常に活発で知能が高い。精神的刺激が必要。繁殖にはPRA遺伝子検査を推奨"}},
        {"id": "cat_siamese", "name": "Siamese", "name_ja": "シャム（サイアミーズ）",
         "risk": {"Feline Asthma": 2.0, "Amyloidosis": 1.8,
                  "Megaesophagus": 1.5, "Progressive Retinal Atrophy (PRA)": 1.5},
         "ecology": {"temperature": {"min": 20, "max": 29, "unit": "°C"},
                     "humidity": {"min": 30, "max": 65, "unit": "%"},
                     "lifespan": {"min": 15, "max": 20, "unit": "years"},
                     "weight": {"min": 3.0, "max": 5.0, "unit": "kg"},
                     "diet": "Obligate carnivore; standard balanced diet; monitor for food allergies",
                     "diet_ja": "完全肉食性。バランスの取れた総合栄養食。食物アレルギーに注意",
                     "housing": "Indoor only; needs companionship — does not do well alone for long periods",
                     "housing_ja": "完全室内飼育。社交的で長時間の留守番に弱い。多頭飼いも検討",
                     "notes": "Vocal and social; predisposed to asthma — avoid smoking and aerosol irritants; coat darkens in cooler areas",
                     "notes_ja": "よく鳴き社交的。喘息素因があるため喫煙・エアロゾル刺激物を避ける。寒い部位の被毛が濃くなる"}},
        {"id": "cat_abyssinian", "name": "Abyssinian", "name_ja": "アビシニアン",
         "risk": {"Feline Chronic Kidney Disease (CKD)": 1.8, "Amyloidosis": 2.0,
                  "Progressive Retinal Atrophy (PRA)": 1.5, "Pyruvate Kinase Deficiency": 2.0},
         "ecology": {"temperature": {"min": 18, "max": 29, "unit": "°C"},
                     "humidity": {"min": 30, "max": 65, "unit": "%"},
                     "lifespan": {"min": 12, "max": 16, "unit": "years"},
                     "weight": {"min": 3.0, "max": 5.5, "unit": "kg"},
                     "diet": "Obligate carnivore; high-quality protein diet; renal support diet if CKD develops",
                     "diet_ja": "完全肉食性。高品質タンパク食。CKD発症時は腎臓サポート食に移行",
                     "housing": "Indoor with vertical space; extremely active and loves climbing",
                     "housing_ja": "高さのあるキャットタワー付き室内飼育。非常に活発で登るのを好む",
                     "notes": "Screen for PRA and PK deficiency; monitor kidney values annually after age 7; very playful and active",
                     "notes_ja": "PRAとPK欠損症のスクリーニング推奨。7歳以降は年1回の腎臓値モニタリング。非常に活発"}},
        {"id": "cat_british_shorthair", "name": "British Shorthair", "name_ja": "ブリティッシュショートヘア",
         "risk": {"Feline Hypertrophic Cardiomyopathy (HCM)": 2.0, "Polycystic Kidney Disease (PKD)": 1.5,
                  "Obesity": 1.5},
         "ecology": {"temperature": {"min": 18, "max": 28, "unit": "°C"},
                     "humidity": {"min": 30, "max": 65, "unit": "%"},
                     "lifespan": {"min": 12, "max": 17, "unit": "years"},
                     "weight": {"min": 4.0, "max": 8.0, "unit": "kg"},
                     "diet": "Obligate carnivore; calorie-controlled diet essential due to obesity tendency",
                     "diet_ja": "完全肉食性。肥満傾向のためカロリー管理が不可欠",
                     "housing": "Indoor preferred; calm breed but needs play sessions to maintain healthy weight",
                     "housing_ja": "室内飼育推奨。穏やかだが体重維持のため遊びの時間を確保",
                     "notes": "HCM screening recommended; prone to weight gain — portion control and interactive play important",
                     "notes_ja": "HCMスクリーニング推奨。太りやすいため食事量管理と遊びが重要"}},
        {"id": "cat_sphynx", "name": "Sphynx", "name_ja": "スフィンクス",
         "risk": {"Feline Hypertrophic Cardiomyopathy (HCM)": 2.5, "Skin Infections": 1.8,
                  "Urticaria Pigmentosa": 1.5},
         "ecology": {"temperature": {"min": 20, "max": 30, "unit": "°C"},
                     "humidity": {"min": 30, "max": 60, "unit": "%"},
                     "lifespan": {"min": 12, "max": 16, "unit": "years"},
                     "weight": {"min": 3.0, "max": 5.5, "unit": "kg"},
                     "diet": "Obligate carnivore; higher caloric needs due to heat loss from hairless body",
                     "diet_ja": "完全肉食性。無毛で体温放散が大きいためカロリー要求量が高い",
                     "housing": "Indoor only; warm environment essential; clothing or heated beds in cool weather",
                     "housing_ja": "完全室内飼育。暖かい環境が必須。寒い時期は衣服やヒーター付きベッドを使用",
                     "notes": "Weekly bathing to remove skin oil buildup; protect from sunburn and cold; HCM screening essential",
                     "notes_ja": "皮脂除去のため週1回の入浴。日焼けと寒さから保護。HCMスクリーニング必須"}},
        {"id": "cat_exotic_shorthair", "name": "Exotic Shorthair", "name_ja": "エキゾチックショートヘア",
         "risk": {"Polycystic Kidney Disease (PKD)": 2.5, "Brachycephalic Airway Syndrome": 2.0, "Saddle Nose Deformity (Brachycephalic Airway Syndrome)": 2.0,
                  "Feline Hypertrophic Cardiomyopathy (HCM)": 1.5},
         "ecology": {"temperature": {"min": 18, "max": 27, "unit": "°C"},
                     "humidity": {"min": 30, "max": 60, "unit": "%"},
                     "lifespan": {"min": 12, "max": 15, "unit": "years"},
                     "weight": {"min": 3.5, "max": 6.5, "unit": "kg"},
                     "diet": "Obligate carnivore; flat-faced breed formula for ease of eating",
                     "diet_ja": "完全肉食性。短頭種用フードで食べやすさに配慮",
                     "housing": "Indoor only; air conditioning in hot weather due to brachycephalic airway",
                     "housing_ja": "完全室内飼育。短頭種のため暑い時期はエアコン必須",
                     "notes": "Regular eye cleaning for tear staining; PKD ultrasound screening; less grooming than Persian but still needs weekly care",
                     "notes_ja": "涙やけの定期的な清掃。PKD超音波スクリーニング推奨。ペルシャより手入れは少ないが週1回のケアは必要"}},
    ],
    "rabbit": [
        {"id": "rabbit_mixed", "name": "Mixed Breed", "name_ja": "雑種（ミックス）",
         "risk": {},
         "ecology": {"temperature": {"min": 15, "max": 25, "unit": "°C"},
                     "humidity": {"min": 40, "max": 60, "unit": "%"},
                     "lifespan": {"min": 8, "max": 12, "unit": "years"},
                     "weight": {"min": 1.5, "max": 5.0, "unit": "kg"},
                     "diet": "Herbivore; unlimited timothy hay, fresh leafy greens, limited pellets",
                     "diet_ja": "草食性。チモシー牧草を常時摂取、新鮮な葉野菜、ペレットは少量",
                     "housing": "Spacious enclosure with room to hop; daily free-range exercise time essential",
                     "housing_ja": "跳ね回れる広いケージ。毎日の部屋んぽ（室内運動）が必須",
                     "notes": "Varies by genetic background; hay-based diet critical for dental and GI health",
                     "notes_ja": "遺伝的背景が多様。牧草中心の食事が歯と消化管の健康に不可欠"}},
        {"id": "rabbit_netherland_dwarf", "name": "Netherland Dwarf", "name_ja": "ネザーランドドワーフ",
         "risk": {"Malocclusion": 2.5, "Gastrointestinal Stasis": 1.5, "GI Stasis": 1.5, "Pasteurellosis": 1.3,
                  "Dental Malocclusion": 2.5, "Upper Respiratory Infection": 1.3},
         "ecology": {"temperature": {"min": 15, "max": 24, "unit": "°C"},
                     "humidity": {"min": 40, "max": 60, "unit": "%"},
                     "lifespan": {"min": 10, "max": 14, "unit": "years"},
                     "weight": {"min": 0.8, "max": 1.3, "unit": "kg"},
                     "diet": "Herbivore; unlimited timothy hay, small portions of pellets, fresh leafy greens",
                     "diet_ja": "草食性。チモシー牧草を常時摂取、ペレットは少量、新鮮な葉野菜",
                     "housing": "Small but spacious enclosure; gentle handling due to small size and fragile skeleton",
                     "housing_ja": "小型だが十分な広さのケージ。小さく骨が細いため丁寧な扱いが必要",
                     "notes": "Prone to dental malocclusion — regular dental checks essential; sensitive to heat stress",
                     "notes_ja": "不正咬合になりやすいため定期的な歯科検診が必須。暑さに弱い"}},
        {"id": "rabbit_holland_lop", "name": "Holland Lop", "name_ja": "ホーランドロップ",
         "risk": {"Otitis Media / Interna": 2.0, "Malocclusion": 1.8, "Gastrointestinal Stasis": 1.3,
                  "Head Tilt (Vestibular Disease)": 1.8, "Dental Malocclusion": 1.8},
         "ecology": {"temperature": {"min": 15, "max": 24, "unit": "°C"},
                     "humidity": {"min": 40, "max": 60, "unit": "%"},
                     "lifespan": {"min": 7, "max": 12, "unit": "years"},
                     "weight": {"min": 1.4, "max": 2.0, "unit": "kg"},
                     "diet": "Herbivore; unlimited timothy hay, fresh greens, limited pellets",
                     "diet_ja": "草食性。チモシー牧草を常時、新鮮な葉野菜、ペレットは制限",
                     "housing": "Spacious enclosure; lop ears require regular cleaning and monitoring for infection",
                     "housing_ja": "広めのケージ。垂れ耳は感染症予防のため定期的な清掃と観察が必要",
                     "notes": "Lop ears trap moisture and debris — check ears weekly; prone to otitis and dental issues",
                     "notes_ja": "垂れ耳は湿気や汚れが溜まりやすい。週1回の耳チェック。中耳炎と歯科疾患に注意"}},
        {"id": "rabbit_mini_rex", "name": "Mini Rex", "name_ja": "ミニレッキス",
         "risk": {"Pododermatitis (Sore Hocks)": 2.0, "Gastrointestinal Stasis": 1.3},
         "ecology": {"temperature": {"min": 15, "max": 24, "unit": "°C"},
                     "humidity": {"min": 40, "max": 60, "unit": "%"},
                     "lifespan": {"min": 7, "max": 10, "unit": "years"},
                     "weight": {"min": 1.4, "max": 2.0, "unit": "kg"},
                     "diet": "Herbivore; unlimited timothy hay, fresh leafy greens, limited pellets",
                     "diet_ja": "草食性。チモシー牧草を常時、新鮮な葉野菜、ペレットは少量",
                     "housing": "Soft bedding essential — thin fur on feet makes them prone to sore hocks on hard surfaces",
                     "housing_ja": "柔らかい床材が必須。足裏の毛が薄く硬い床ではソアホック（飛節びらん）になりやすい",
                     "notes": "Velvety short coat requires minimal grooming; soft flooring is critical to prevent pododermatitis",
                     "notes_ja": "ビロード状の短毛でグルーミングは最小限。ソアホック予防に柔らかい床材が不可欠"}},
        {"id": "rabbit_lionhead", "name": "Lionhead", "name_ja": "ライオンヘッド",
         "risk": {"Malocclusion": 1.8, "Wool Block/Trichobezoar": 2.0, "Dental Malocclusion": 1.8},
         "ecology": {"temperature": {"min": 15, "max": 24, "unit": "°C"},
                     "humidity": {"min": 40, "max": 60, "unit": "%"},
                     "lifespan": {"min": 7, "max": 10, "unit": "years"},
                     "weight": {"min": 1.3, "max": 1.7, "unit": "kg"},
                     "diet": "Herbivore; unlimited timothy hay critical for GI motility, fresh greens, limited pellets",
                     "diet_ja": "草食性。消化管運動のためチモシー牧草を常時、新鮮な葉野菜、ペレットは少量",
                     "housing": "Spacious enclosure; regular grooming area to manage mane",
                     "housing_ja": "広めのケージ。たてがみの管理のため定期的なグルーミングスペースが必要",
                     "notes": "Long mane requires regular grooming to prevent wool block from ingested fur; dental checks important",
                     "notes_ja": "長いたてがみは毛球症予防のため定期的なブラッシングが必要。歯科検診も重要"}},
        {"id": "rabbit_flemish_giant", "name": "Flemish Giant", "name_ja": "フレミッシュジャイアント",
         "risk": {"Pododermatitis (Sore Hocks)": 2.0, "Spondylosis": 1.8, "Heart Disease": 1.5,
                  "Congestive Heart Failure": 1.5, "Obesity": 1.5, "Hock Sores": 2.0},
         "ecology": {"temperature": {"min": 15, "max": 24, "unit": "°C"},
                     "humidity": {"min": 40, "max": 60, "unit": "%"},
                     "lifespan": {"min": 5, "max": 8, "unit": "years"},
                     "weight": {"min": 5.0, "max": 10.0, "unit": "kg"},
                     "diet": "Herbivore; unlimited timothy hay, generous fresh greens, controlled pellets to prevent obesity",
                     "diet_ja": "草食性。チモシー牧草を常時、たっぷりの葉野菜、肥満予防のためペレットは管理",
                     "housing": "Very large enclosure or dedicated room; sturdy flooring with soft bedding for heavy body",
                     "housing_ja": "非常に大きなケージまたは専用部屋。重い体を支える丈夫で柔らかい床材",
                     "notes": "Largest rabbit breed — needs strong support surfaces; prone to sore hocks, spondylosis, and heart disease",
                     "notes_ja": "最大のウサギ品種。頑丈な床が必要。ソアホック、脊椎症、心臓病に注意"}},
        {"id": "rabbit_rex", "name": "Rex", "name_ja": "レッキス",
         "risk": {"Pododermatitis (Sore Hocks)": 2.5, "Gastrointestinal Stasis": 1.3},
         "ecology": {"temperature": {"min": 15, "max": 24, "unit": "°C"},
                     "humidity": {"min": 40, "max": 60, "unit": "%"},
                     "lifespan": {"min": 7, "max": 10, "unit": "years"},
                     "weight": {"min": 3.0, "max": 5.0, "unit": "kg"},
                     "diet": "Herbivore; unlimited timothy hay, fresh leafy greens, limited pellets",
                     "diet_ja": "草食性。チモシー牧草を常時、新鮮な葉野菜、ペレットは少量",
                     "housing": "Soft padded flooring essential; short plush fur provides less protection for foot pads",
                     "housing_ja": "柔らかい床材が必須。短い毛が足裏の保護に不十分なためソアホックになりやすい",
                     "notes": "Very prone to sore hocks — never house on wire flooring; velvety coat needs minimal grooming",
                     "notes_ja": "ソアホックに非常になりやすい。金網床は厳禁。ビロード状の被毛はグルーミングが少なくて済む"}},
        {"id": "rabbit_lop_eared", "name": "Lop Eared (General)", "name_ja": "ロップイヤー（一般）",
         "risk": {"Otitis Media / Interna": 2.5, "Ear Mites": 1.5, "Dental Disease": 1.3, "Dental Malocclusion": 1.3,
                  "Head Tilt (Vestibular Disease)": 1.8},
         "ecology": {"temperature": {"min": 15, "max": 24, "unit": "°C"},
                     "humidity": {"min": 40, "max": 60, "unit": "%"},
                     "lifespan": {"min": 7, "max": 12, "unit": "years"},
                     "weight": {"min": 1.5, "max": 5.5, "unit": "kg"},
                     "diet": "Herbivore; unlimited timothy hay, fresh greens, limited pellets",
                     "diet_ja": "草食性。チモシー牧草を常時、新鮮な葉野菜、ペレットは制限",
                     "housing": "Spacious enclosure; clean, dry environment critical for ear health",
                     "housing_ja": "広めのケージ。耳の健康のため清潔で乾燥した環境が重要",
                     "notes": "Lop ears are prone to otitis media/interna — weekly ear inspection; watch for head tilt as an early sign",
                     "notes_ja": "垂れ耳は中耳炎・内耳炎になりやすい。週1回の耳チェック。斜頸は初期サインとして注意"}},
        {"id": "rabbit_angora", "name": "Angora", "name_ja": "アンゴラ",
         "risk": {"Wool Block/Trichobezoar": 2.5, "GI Stasis": 1.8, "Gastrointestinal Stasis": 1.8,
                  "Flystrike (Myiasis)": 1.8, "Heat Stroke": 1.5},
         "ecology": {"temperature": {"min": 15, "max": 22, "unit": "°C"},
                     "humidity": {"min": 40, "max": 60, "unit": "%"},
                     "lifespan": {"min": 7, "max": 12, "unit": "years"},
                     "weight": {"min": 2.0, "max": 5.5, "unit": "kg"},
                     "diet": "Herbivore; extra-high hay intake critical to prevent wool block; fresh greens, limited pellets",
                     "diet_ja": "草食性。毛球症予防のため特に多くの牧草摂取が重要。新鮮な葉野菜、ペレットは少量",
                     "housing": "Cool environment essential; daily grooming station needed; keep rear end clean to prevent flystrike",
                     "housing_ja": "涼しい環境が必須。毎日のグルーミングスペースが必要。フライストライク予防のため臀部を清潔に",
                     "notes": "Requires daily grooming to prevent matting and wool block; heat-sensitive due to thick coat; flystrike risk in summer",
                     "notes_ja": "毛玉・毛球症予防のため毎日のグルーミングが必要。厚い被毛で暑さに弱い。夏季はフライストライクに注意"}},
        {"id": "rabbit_dwarf_hotot", "name": "Dwarf Hotot", "name_ja": "ドワーフホト",
         "risk": {"Malocclusion": 2.0, "Dental Malocclusion": 2.0},
         "ecology": {"temperature": {"min": 15, "max": 24, "unit": "°C"},
                     "humidity": {"min": 40, "max": 60, "unit": "%"},
                     "lifespan": {"min": 7, "max": 10, "unit": "years"},
                     "weight": {"min": 1.0, "max": 1.4, "unit": "kg"},
                     "diet": "Herbivore; unlimited timothy hay, fresh leafy greens, limited pellets",
                     "diet_ja": "草食性。チモシー牧草を常時、新鮮な葉野菜、ペレットは少量",
                     "housing": "Compact but spacious enclosure; gentle handling for small breed",
                     "housing_ja": "小型だが十分な広さのケージ。小さいため丁寧な扱いが必要",
                     "notes": "Dwarf breed prone to dental malocclusion — regular dental exams; distinctive eye bands require no special care",
                     "notes_ja": "矮小品種で不正咬合になりやすいため定期歯科検診が必要。特徴的なアイバンドは特別なケア不要"}},
    ],
    "hamster": [
        {"id": "hamster_golden", "name": "Golden (Syrian)", "name_ja": "ゴールデン（シリアン）",
         "risk": {"Wet Tail (Proliferative Ileitis)": 2.0, "Hamster Pyometra": 1.8, "Amyloidosis": 1.5,
                  "Cardiomyopathy": 1.5, "Lymphoma": 1.5, "Cushing's Disease (Hyperadrenocorticism)": 1.3},
         "ecology": {"temperature": {"min": 20, "max": 26, "unit": "°C"},
                     "humidity": {"min": 40, "max": 60, "unit": "%"},
                     "lifespan": {"min": 2, "max": 3, "unit": "years"},
                     "weight": {"min": 100, "max": 200, "unit": "g"},
                     "diet": "Omnivore; commercial hamster mix with seeds, grains, dried vegetables, occasional protein (mealworms, egg)",
                     "diet_ja": "雑食性。種子・穀物・乾燥野菜のハムスター用混合飼料。時々ミルワームや卵で動物性タンパク質",
                     "housing": "Solitary housing only — aggressive to cage mates; large cage with deep bedding for burrowing; wheel essential",
                     "housing_ja": "単独飼育のみ。同居は攻撃的になる。深い床材で穴掘り可能な大きめのケージ。回し車必須",
                     "notes": "Strictly solitary; prone to wet tail especially in young; nocturnal — avoid disturbing daytime sleep; hibernation-like torpor below 15°C",
                     "notes_ja": "厳格な単独飼育。若齢ではウェットテイルに注意。夜行性のため昼間の睡眠を邪魔しない。15°C以下で擬似冬眠に注意"}},
        {"id": "hamster_djungarian", "name": "Djungarian (Winter White)", "name_ja": "ジャンガリアン",
         "risk": {"Diabetes Mellitus": 2.5, "Tumors/Neoplasia": 1.5, "Obesity": 1.3},
         "ecology": {"temperature": {"min": 18, "max": 24, "unit": "°C"},
                     "humidity": {"min": 40, "max": 60, "unit": "%"},
                     "lifespan": {"min": 1.5, "max": 2.5, "unit": "years"},
                     "weight": {"min": 25, "max": 50, "unit": "g"},
                     "diet": "Omnivore; low-sugar hamster mix essential due to diabetes risk; avoid fruit and sugary treats",
                     "diet_ja": "雑食性。糖尿病リスクが高いため低糖質のハムスター用飼料が必須。果物や甘いおやつは避ける",
                     "housing": "Can sometimes be kept in pairs if introduced young; deep bedding; wheel sized for dwarf hamsters",
                     "housing_ja": "若いうちに導入すればペア飼育も可能な場合あり。深い床材。ドワーフハムスター用サイズの回し車",
                     "notes": "Very high diabetes risk — strictly no sugary foods; coat turns white in winter with shorter daylight; monitor weight closely",
                     "notes_ja": "糖尿病リスクが非常に高い。甘い食べ物は厳禁。短日条件で冬毛（白）に変化。体重を注意深く管理"}},
        {"id": "hamster_campbell", "name": "Campbell's Dwarf", "name_ja": "キャンベル",
         "risk": {"Diabetes Mellitus": 3.0, "Glaucoma": 1.5, "Cataracts": 1.5,
                  "Tumors/Neoplasia": 1.5},
         "ecology": {"temperature": {"min": 18, "max": 24, "unit": "°C"},
                     "humidity": {"min": 40, "max": 60, "unit": "%"},
                     "lifespan": {"min": 1.5, "max": 2.5, "unit": "years"},
                     "weight": {"min": 25, "max": 50, "unit": "g"},
                     "diet": "Omnivore; strict low-sugar diet critical — highest diabetes risk of all hamster species",
                     "diet_ja": "雑食性。全ハムスター種で最も糖尿病リスクが高いため厳格な低糖質食が不可欠",
                     "housing": "Can sometimes be kept in pairs; deep bedding for burrowing; appropriately sized wheel",
                     "housing_ja": "ペア飼育が可能な場合もあり。穴掘り用の深い床材。適切なサイズの回し車",
                     "notes": "Extremely high diabetes risk — no fruit, honey, or sugar; prone to glaucoma and cataracts; may bite if startled",
                     "notes_ja": "糖尿病リスクが極めて高い。果物・蜂蜜・砂糖は厳禁。緑内障と白内障にも注意。驚くと噛むことがある"}},
        {"id": "hamster_roborovski", "name": "Roborovski", "name_ja": "ロボロフスキー",
         "risk": {"Tumors/Neoplasia": 1.3},
         "ecology": {"temperature": {"min": 18, "max": 24, "unit": "°C"},
                     "humidity": {"min": 30, "max": 50, "unit": "%"},
                     "lifespan": {"min": 3, "max": 4, "unit": "years"},
                     "weight": {"min": 20, "max": 30, "unit": "g"},
                     "diet": "Omnivore; small-seed mix suitable for tiny body; occasional small insects for protein",
                     "diet_ja": "雑食性。小さな体に合った小粒の種子ミックス。時々小さな昆虫でタンパク質補給",
                     "housing": "Can be kept in same-sex pairs or small groups; deep sandy bedding; very small — secure cage with narrow bar spacing",
                     "housing_ja": "同性ペアまたは小グループ飼育可能。深い砂状の床材。非常に小さいため隙間の狭いケージが必要",
                     "notes": "Smallest and longest-lived hamster species; extremely fast and difficult to handle; low disease incidence; prefers dry sandy substrate",
                     "notes_ja": "最小かつ最長寿のハムスター種。非常に素早くハンドリングが難しい。疾患発生率は低い。乾燥した砂質の床材を好む"}},
        {"id": "hamster_chinese", "name": "Chinese Hamster", "name_ja": "チャイニーズハムスター",
         "risk": {"Diabetes Mellitus": 2.0, "Tail Slip": 1.5, "Tumors/Neoplasia": 1.5},
         "ecology": {"temperature": {"min": 18, "max": 24, "unit": "°C"},
                     "humidity": {"min": 40, "max": 60, "unit": "%"},
                     "lifespan": {"min": 2, "max": 3, "unit": "years"},
                     "weight": {"min": 30, "max": 45, "unit": "g"},
                     "diet": "Omnivore; low-sugar hamster mix; moderate diabetes risk requires limiting sugary foods",
                     "diet_ja": "雑食性。低糖質ハムスター用飼料。中程度の糖尿病リスクがあるため甘い食べ物を制限",
                     "housing": "Solitary or same-sex pairs; good climbers — provide branches; secure cage as they can squeeze through small gaps",
                     "housing_ja": "単独またはペア飼育。登るのが得意なため枝を設置。小さな隙間から脱走するため安全なケージが必要",
                     "notes": "Long prehensile tail — never grab by tail as tail slip (degloving) can occur; agile climbers; diabetes monitoring important",
                     "notes_ja": "長い尾を持つが尾を掴まないこと（テイルスリップの危険）。器用な登り手。糖尿病のモニタリングが重要"}},
    ],
    "ferret": [
        {"id": "ferret_standard", "name": "Standard", "name_ja": "スタンダード",
         "risk": {},
         "ecology": {"temperature": {"min": 15, "max": 24, "unit": "°C"},
                     "humidity": {"min": 40, "max": 65, "unit": "%"},
                     "lifespan": {"min": 6, "max": 10, "unit": "years"},
                     "weight": {"min": 0.7, "max": 2.0, "unit": "kg"},
                     "diet": "Obligate carnivore; high-protein, high-fat, low-fiber commercial ferret food or whole prey",
                     "diet_ja": "完全肉食性。高タンパク・高脂肪・低繊維のフェレット用フードまたはホールプレイ",
                     "housing": "Multi-level ferret-proofed cage; 4+ hours daily free-roam in ferret-proofed room",
                     "housing_ja": "多段式のフェレット用ケージ。毎日4時間以上のフェレットプルーフした部屋での放し飼い",
                     "notes": "Prone to adrenal disease, insulinoma, and lymphoma after age 3; annual veterinary checkups essential; very curious — ferret-proof all rooms",
                     "notes_ja": "3歳以降は副腎疾患・インスリノーマ・リンパ腫に注意。年1回の健康診断必須。好奇心旺盛なため部屋の安全対策が必要"}},
        {"id": "ferret_marshall", "name": "Marshall Ferret", "name_ja": "マーシャルフェレット",
         "risk": {"Adrenal Disease": 2.0, "Insulinoma": 1.8, "Lymphoma": 1.5,
                  "Cardiomyopathy": 1.5, "Helicobacter Gastritis": 1.5},
         "ecology": {"temperature": {"min": 15, "max": 24, "unit": "°C"},
                     "humidity": {"min": 40, "max": 65, "unit": "%"},
                     "lifespan": {"min": 5, "max": 9, "unit": "years"},
                     "weight": {"min": 0.7, "max": 2.0, "unit": "kg"},
                     "diet": "Obligate carnivore; high-quality ferret food; avoid carbohydrates which may worsen insulinoma risk",
                     "diet_ja": "完全肉食性。高品質フェレットフード。インスリノーマリスク悪化のため炭水化物を避ける",
                     "housing": "Multi-level cage; extended daily exercise in ferret-proofed space",
                     "housing_ja": "多段式ケージ。フェレットプルーフした空間での十分な運動時間",
                     "notes": "Early neutering associated with higher adrenal disease rates; monitor blood glucose for insulinoma; semi-annual vet visits after age 3",
                     "notes_ja": "早期去勢は副腎疾患リスクを高める。インスリノーマのため血糖値をモニタリング。3歳以降は半年に1回の健診を推奨"}},
        {"id": "ferret_angora", "name": "Angora", "name_ja": "アンゴラ",
         "risk": {"Adrenal Disease": 1.5, "Hairball/GI Obstruction": 1.8, "Gastrointestinal Foreign Body / Obstruction": 1.8},
         "ecology": {"temperature": {"min": 15, "max": 24, "unit": "°C"},
                     "humidity": {"min": 40, "max": 65, "unit": "%"},
                     "lifespan": {"min": 6, "max": 10, "unit": "years"},
                     "weight": {"min": 0.8, "max": 2.0, "unit": "kg"},
                     "diet": "Obligate carnivore; high-protein ferret diet; hairball prevention treats may help",
                     "diet_ja": "完全肉食性。高タンパクフェレット食。毛球症予防のサプリメントが有効な場合あり",
                     "housing": "Multi-level cage; regular grooming area needed for long coat maintenance",
                     "housing_ja": "多段式ケージ。長毛の手入れのため定期的なグルーミングスペースが必要",
                     "notes": "Long coat requires regular brushing to prevent hairball GI obstruction; may have reduced nasal structure — monitor breathing",
                     "notes_ja": "長毛は毛球による消化管閉塞予防のため定期的なブラッシングが必要。鼻の構造が短い場合があり呼吸を観察"}},
        {"id": "ferret_albino", "name": "Albino (Dark-eyed White)", "name_ja": "アルビノ（ダークアイドホワイト）",
         "risk": {"Waardenburg Syndrome": 2.0, "Deafness": 1.8, "Adrenal Disease": 1.5},
         "ecology": {"temperature": {"min": 15, "max": 24, "unit": "°C"},
                     "humidity": {"min": 40, "max": 65, "unit": "%"},
                     "lifespan": {"min": 6, "max": 10, "unit": "years"},
                     "weight": {"min": 0.7, "max": 2.0, "unit": "kg"},
                     "diet": "Obligate carnivore; standard high-protein ferret diet",
                     "diet_ja": "完全肉食性。標準的な高タンパクフェレット食",
                     "housing": "Multi-level cage; may be deaf (Waardenburg) — use visual cues instead of auditory for training",
                     "housing_ja": "多段式ケージ。ワーデンブルグ症候群で聴覚障害の可能性あり。訓練には視覚的な合図を使用",
                     "notes": "High incidence of congenital deafness — test hearing early; sensitive to bright light; otherwise same care as standard ferrets",
                     "notes_ja": "先天性聴覚障害の発生率が高い。早期に聴力検査を実施。強い光に敏感。その他のケアはスタンダードと同様"}},
    ],
    "guinea_pig": [
        {"id": "guinea_pig_american", "name": "American (Short Hair)", "name_ja": "アメリカン（短毛）",
         "risk": {},
         "ecology": {"temperature": {"min": 18, "max": 24, "unit": "°C"},
                     "humidity": {"min": 40, "max": 60, "unit": "%"},
                     "lifespan": {"min": 5, "max": 7, "unit": "years"},
                     "weight": {"min": 700, "max": 1200, "unit": "g"},
                     "diet": "Herbivore; unlimited timothy hay, daily vitamin C supplement (cannot synthesize it), fresh vegetables, limited pellets",
                     "diet_ja": "草食性。チモシー牧草を常時、毎日のビタミンC補給（体内合成不可）、新鮮な野菜、ペレットは少量",
                     "housing": "Spacious floor-level enclosure (no wire floors); social species — keep in pairs or groups",
                     "housing_ja": "広いフラットなケージ（金網床不可）。社会性動物のためペアまたはグループ飼育",
                     "notes": "Must receive vitamin C daily (scurvy risk); social animals — never keep alone; short coat requires minimal grooming",
                     "notes_ja": "ビタミンCの毎日の摂取が必須（壊血病リスク）。社会性動物のため単独飼育は避ける。短毛でグルーミングは最小限"}},
        {"id": "guinea_pig_abyssinian", "name": "Abyssinian", "name_ja": "アビシニアン",
         "risk": {"Ovarian Cysts": 1.5, "Diabetes Mellitus": 1.3, "Urolithiasis (Bladder Stones)": 1.3},
         "ecology": {"temperature": {"min": 18, "max": 24, "unit": "°C"},
                     "humidity": {"min": 40, "max": 60, "unit": "%"},
                     "lifespan": {"min": 5, "max": 7, "unit": "years"},
                     "weight": {"min": 800, "max": 1200, "unit": "g"},
                     "diet": "Herbivore; unlimited timothy hay, daily vitamin C, fresh vegetables, limited pellets; monitor sugar intake for diabetes risk",
                     "diet_ja": "草食性。チモシー牧草を常時、毎日のビタミンC、新鮮な野菜、ペレットは少量。糖尿病リスクのため糖質管理",
                     "housing": "Spacious floor-level enclosure; social — keep in pairs or groups",
                     "housing_ja": "広いフラットなケージ。社会性動物のためペアまたはグループ飼育",
                     "notes": "Rosette coat needs regular brushing; prone to ovarian cysts in unspayed females; diabetes and bladder stone monitoring",
                     "notes_ja": "ロゼット状の被毛は定期的なブラッシングが必要。未避妊の雌は卵巣嚢胞に注意。糖尿病と膀胱結石のモニタリング"}},
        {"id": "guinea_pig_peruvian", "name": "Peruvian", "name_ja": "ペルビアン",
         "risk": {"Dermatophytosis (Ringworm)": 1.8, "Ringworm (Trichophyton mentagrophytes)": 1.8, "Heat Stroke": 1.5,
                  "Flystrike (Myiasis)": 1.8, "Pododermatitis (Bumblefoot)": 1.3},
         "ecology": {"temperature": {"min": 18, "max": 23, "unit": "°C"},
                     "humidity": {"min": 40, "max": 60, "unit": "%"},
                     "lifespan": {"min": 5, "max": 7, "unit": "years"},
                     "weight": {"min": 800, "max": 1400, "unit": "g"},
                     "diet": "Herbivore; unlimited timothy hay, daily vitamin C, fresh vegetables, limited pellets",
                     "diet_ja": "草食性。チモシー牧草を常時、毎日のビタミンC、新鮮な野菜、ペレットは少量",
                     "housing": "Spacious floor-level enclosure; keep in pairs; clean bedding critical to prevent coat soiling and flystrike",
                     "housing_ja": "広いフラットなケージ。ペア飼育。被毛汚れとフライストライク予防のため清潔な床材が重要",
                     "notes": "Very long coat requires daily grooming and trimming; heat-sensitive — keep cool; flystrike risk if coat becomes soiled",
                     "notes_ja": "非常に長い被毛は毎日のグルーミングとトリミングが必要。暑さに弱いため涼しく保つ。被毛汚染時はフライストライクに注意"}},
        {"id": "guinea_pig_skinny", "name": "Skinny Pig", "name_ja": "スキニーギニアピッグ",
         "risk": {"Hypothermia": 2.0, "Skin Infections": 1.8, "Sunburn": 2.0, "Ringworm (Trichophyton mentagrophytes)": 1.5},
         "ecology": {"temperature": {"min": 22, "max": 26, "unit": "°C"},
                     "humidity": {"min": 40, "max": 60, "unit": "%"},
                     "lifespan": {"min": 5, "max": 7, "unit": "years"},
                     "weight": {"min": 700, "max": 1100, "unit": "g"},
                     "diet": "Herbivore; unlimited timothy hay, daily vitamin C, fresh vegetables; higher caloric needs due to heat loss",
                     "diet_ja": "草食性。チモシー牧草を常時、毎日のビタミンC、新鮮な野菜。体温放散のためカロリー要求量が高い",
                     "housing": "Warm indoor enclosure only; no direct sunlight (sunburn); fleece bedding for warmth",
                     "housing_ja": "暖かい室内ケージのみ。直射日光は厳禁（日焼け）。保温のためフリースの床材を推奨",
                     "notes": "Hairless — requires warm environment, sun protection, and regular skin moisturizing; prone to skin infections and hypothermia",
                     "notes_ja": "無毛のため暖かい環境・日焼け防止・定期的な保湿が必要。皮膚感染症と低体温症に注意"}},
        {"id": "guinea_pig_teddy", "name": "Teddy", "name_ja": "テディ",
         "risk": {"Ear Wax Buildup": 1.5, "Dermatophytosis (Ringworm)": 1.3, "Ringworm (Trichophyton mentagrophytes)": 1.3},
         "ecology": {"temperature": {"min": 18, "max": 24, "unit": "°C"},
                     "humidity": {"min": 40, "max": 60, "unit": "%"},
                     "lifespan": {"min": 5, "max": 7, "unit": "years"},
                     "weight": {"min": 700, "max": 1200, "unit": "g"},
                     "diet": "Herbivore; unlimited timothy hay, daily vitamin C, fresh vegetables, limited pellets",
                     "diet_ja": "草食性。チモシー牧草を常時、毎日のビタミンC、新鮮な野菜、ペレットは少量",
                     "housing": "Spacious floor-level enclosure; social — keep in pairs or groups",
                     "housing_ja": "広いフラットなケージ。社会性動物のためペアまたはグループ飼育",
                     "notes": "Dense wiry coat traps debris — regular brushing needed; prone to ear wax buildup requiring regular cleaning",
                     "notes_ja": "密で硬い被毛にゴミが溜まりやすいため定期的なブラッシングが必要。耳垢が溜まりやすいため定期的な清掃を"}},
        {"id": "guinea_pig_coronet", "name": "Coronet", "name_ja": "コロネット",
         "risk": {"Dermatophytosis (Ringworm)": 1.5, "Heat Stroke": 1.3},
         "ecology": {"temperature": {"min": 18, "max": 24, "unit": "°C"},
                     "humidity": {"min": 40, "max": 60, "unit": "%"},
                     "lifespan": {"min": 5, "max": 7, "unit": "years"},
                     "weight": {"min": 800, "max": 1300, "unit": "g"},
                     "diet": "Herbivore; unlimited timothy hay, daily vitamin C, fresh vegetables, limited pellets",
                     "diet_ja": "草食性。チモシー牧草を常時、毎日のビタミンC、新鮮な野菜、ペレットは少量",
                     "housing": "Spacious floor-level enclosure; social — keep in pairs; clean bedding to prevent coat matting",
                     "housing_ja": "広いフラットなケージ。ペア飼育。被毛の絡まり防止のため清潔な床材",
                     "notes": "Long silky coat with central rosette; daily grooming and periodic trimming needed; heat-sensitive",
                     "notes_ja": "中央にロゼットのある長い絹のような被毛。毎日のグルーミングと定期的なトリミングが必要。暑さに弱い"}},
        {"id": "guinea_pig_texel", "name": "Texel", "name_ja": "テッセル",
         "risk": {"Dermatophytosis (Ringworm)": 1.8, "Heat Stroke": 1.5, "Flystrike (Myiasis)": 1.5},
         "ecology": {"temperature": {"min": 18, "max": 23, "unit": "°C"},
                     "humidity": {"min": 40, "max": 60, "unit": "%"},
                     "lifespan": {"min": 5, "max": 7, "unit": "years"},
                     "weight": {"min": 800, "max": 1300, "unit": "g"},
                     "diet": "Herbivore; unlimited timothy hay, daily vitamin C, fresh vegetables, limited pellets",
                     "diet_ja": "草食性。チモシー牧草を常時、毎日のビタミンC、新鮮な野菜、ペレットは少量",
                     "housing": "Spacious floor-level enclosure; social — keep in pairs; extra-clean bedding to prevent coat contamination",
                     "housing_ja": "広いフラットなケージ。ペア飼育。被毛汚染防止のため特に清潔な床材",
                     "notes": "Long curly coat requires daily grooming; high ringworm and flystrike risk; heat-sensitive — avoid temperatures above 23°C",
                     "notes_ja": "長いカーリーコートは毎日のグルーミングが必要。皮膚糸状菌症とフライストライクのリスクが高い。23°C以上を避ける"}},
    ],
    "chinchilla": [
        {"id": "chinchilla_standard", "name": "Standard Grey", "name_ja": "スタンダードグレー",
         "risk": {},
         "ecology": {"temperature": {"min": 15, "max": 21, "unit": "°C"},
                     "humidity": {"min": 30, "max": 50, "unit": "%"},
                     "lifespan": {"min": 15, "max": 20, "unit": "years"},
                     "weight": {"min": 400, "max": 700, "unit": "g"},
                     "diet": "Herbivore; unlimited timothy hay, chinchilla-specific pellets, occasional dried herbs; no fruit or sugary treats",
                     "diet_ja": "草食性。チモシー牧草を常時、チンチラ専用ペレット、時々ドライハーブ。果物や甘いおやつは厳禁",
                     "housing": "Tall multi-level cage for climbing; dust bath (not water) 2-3 times per week; cool room essential",
                     "housing_ja": "登れる多段式の背の高いケージ。週2〜3回の砂浴び（水浴びは不可）。涼しい部屋が必須",
                     "notes": "Extremely heat-sensitive — temperatures above 25°C can be fatal; dense fur (80 hairs per follicle) — never get wet; dental disease is common",
                     "notes_ja": "暑さに極めて弱い。25°C以上は致命的になりうる。超高密度の被毛（1毛穴80本）は絶対に濡らさない。歯科疾患が多い"}},
        {"id": "chinchilla_black_velvet", "name": "Black Velvet", "name_ja": "ブラックベルベット",
         "risk": {"Lethal Gene Issues": 1.5},
         "ecology": {"temperature": {"min": 15, "max": 21, "unit": "°C"},
                     "humidity": {"min": 30, "max": 50, "unit": "%"},
                     "lifespan": {"min": 15, "max": 20, "unit": "years"},
                     "weight": {"min": 400, "max": 700, "unit": "g"},
                     "diet": "Herbivore; unlimited timothy hay, chinchilla-specific pellets, occasional dried herbs; no fruit or sugary treats",
                     "diet_ja": "草食性。チモシー牧草を常時、チンチラ専用ペレット、時々ドライハーブ。果物や甘いおやつは厳禁",
                     "housing": "Tall multi-level cage; dust bath 2-3 times per week; cool room essential",
                     "housing_ja": "多段式の背の高いケージ。週2〜3回の砂浴び。涼しい部屋が必須",
                     "notes": "Never breed velvet-to-velvet (lethal gene); same heat sensitivity and care as standard chinchillas",
                     "notes_ja": "ベルベット同士の交配は厳禁（致死遺伝子）。暑さへの感受性とケアはスタンダードと同様"}},
        {"id": "chinchilla_white", "name": "White (Wilson White)", "name_ja": "ホワイト（ウィルソンホワイト）",
         "risk": {"Lethal Gene Issues": 1.5, "Dental Disease": 1.3, "Dental Malocclusion": 1.3},
         "ecology": {"temperature": {"min": 15, "max": 21, "unit": "°C"},
                     "humidity": {"min": 30, "max": 50, "unit": "%"},
                     "lifespan": {"min": 15, "max": 20, "unit": "years"},
                     "weight": {"min": 400, "max": 700, "unit": "g"},
                     "diet": "Herbivore; unlimited timothy hay, chinchilla-specific pellets; dental health focus with hay-heavy diet",
                     "diet_ja": "草食性。チモシー牧草を常時、チンチラ専用ペレット。牧草中心の食事で歯の健康維持",
                     "housing": "Tall multi-level cage; dust bath 2-3 times per week; cool room essential",
                     "housing_ja": "多段式の背の高いケージ。週2〜3回の砂浴び。涼しい部屋が必須",
                     "notes": "Never breed white-to-white (lethal gene); slightly higher dental disease risk — monitor teeth regularly",
                     "notes_ja": "ホワイト同士の交配は厳禁（致死遺伝子）。歯科疾患リスクがやや高いため定期的な歯のチェック"}},
        {"id": "chinchilla_beige", "name": "Beige (Heterozygous)", "name_ja": "ベージュ",
         "risk": {"Dental Disease": 1.3, "Dental Malocclusion": 1.3},
         "ecology": {"temperature": {"min": 15, "max": 21, "unit": "°C"},
                     "humidity": {"min": 30, "max": 50, "unit": "%"},
                     "lifespan": {"min": 15, "max": 20, "unit": "years"},
                     "weight": {"min": 400, "max": 700, "unit": "g"},
                     "diet": "Herbivore; unlimited timothy hay, chinchilla-specific pellets; dental health focus with hay-heavy diet",
                     "diet_ja": "草食性。チモシー牧草を常時、チンチラ専用ペレット。牧草中心の食事で歯の健康維持",
                     "housing": "Tall multi-level cage; dust bath 2-3 times per week; cool room essential",
                     "housing_ja": "多段式の背の高いケージ。週2〜3回の砂浴び。涼しい部屋が必須",
                     "notes": "Slightly higher dental disease risk — ensure unlimited hay access; same care as standard chinchillas otherwise",
                     "notes_ja": "歯科疾患リスクがやや高い。牧草の常時摂取を確保。その他のケアはスタンダードと同様"}},
        {"id": "chinchilla_ebony", "name": "Ebony", "name_ja": "エボニー",
         "risk": {},
         "ecology": {"temperature": {"min": 15, "max": 21, "unit": "°C"},
                     "humidity": {"min": 30, "max": 50, "unit": "%"},
                     "lifespan": {"min": 15, "max": 20, "unit": "years"},
                     "weight": {"min": 400, "max": 700, "unit": "g"},
                     "diet": "Herbivore; unlimited timothy hay, chinchilla-specific pellets, occasional dried herbs; no fruit or sugary treats",
                     "diet_ja": "草食性。チモシー牧草を常時、チンチラ専用ペレット、時々ドライハーブ。果物や甘いおやつは厳禁",
                     "housing": "Tall multi-level cage; dust bath 2-3 times per week; cool room essential",
                     "housing_ja": "多段式の背の高いケージ。週2〜3回の砂浴び。涼しい部屋が必須",
                     "notes": "No lethal gene concerns — can be bred with any color; same care as standard chinchillas",
                     "notes_ja": "致死遺伝子の懸念なし。どのカラーとも交配可能。ケアはスタンダードと同様"}},
    ],
    "hedgehog": [
        {"id": "hedgehog_four_toed", "name": "Four-toed (African Pygmy)", "name_ja": "ヨツユビハリネズミ",
         "risk": {"Wobbly Hedgehog Syndrome (WHS)": 2.0, "Tumors/Neoplasia": 2.0,
                  "Obesity": 1.5, "Mite Infestation": 1.3, "Fatty Liver Disease": 1.5,
                  "Squamous Cell Carcinoma": 1.8, "Cardiomyopathy": 1.5},
         "ecology": {"temperature": {"min": 24, "max": 29, "unit": "°C"},
                     "humidity": {"min": 40, "max": 60, "unit": "%"},
                     "lifespan": {"min": 3, "max": 6, "unit": "years"},
                     "weight": {"min": 300, "max": 600, "unit": "g"},
                     "diet": "Insectivore/omnivore; high-quality cat food (low-fat) as staple, live insects (mealworms, crickets), occasional vegetables",
                     "diet_ja": "食虫性/雑食性。低脂肪の高品質キャットフードを主食に、生きた昆虫（ミルワーム、コオロギ）、時々野菜",
                     "housing": "Large flat-bottom cage; wheel (solid surface, not wire) essential; hide box; heating to maintain 24-29°C",
                     "housing_ja": "広いフラットなケージ。回し車（ソリッド面、金網不可）必須。隠れ家。24〜29°Cを維持するヒーター",
                     "notes": "Very high tumor incidence after age 3; prone to WHS (progressive paralysis); torpor below 20°C can be fatal; obesity prevention critical",
                     "notes_ja": "3歳以降の腫瘍発生率が非常に高い。WHS（進行性麻痺）に注意。20°C以下の休眠は致命的。肥満予防が重要"}},
        {"id": "hedgehog_european", "name": "European Hedgehog", "name_ja": "ヨーロッパハリネズミ",
         "risk": {"Lungworm Infection": 2.0, "Parasitic Infection": 1.8,
                  "Ringworm (Dermatophytosis)": 1.5},
         "ecology": {"temperature": {"min": 15, "max": 25, "unit": "°C"},
                     "humidity": {"min": 40, "max": 70, "unit": "%"},
                     "lifespan": {"min": 3, "max": 8, "unit": "years"},
                     "weight": {"min": 600, "max": 1200, "unit": "g"},
                     "diet": "Insectivore/omnivore; insects, snails, supplemented cat food; no milk or bread",
                     "diet_ja": "食虫性/雑食性。昆虫、カタツムリ、補助的にキャットフード。牛乳やパンは厳禁",
                     "housing": "Outdoor garden or large indoor enclosure; hibernation box for winter; access to natural foraging area",
                     "housing_ja": "屋外の庭または大きな室内ケージ。冬季用の冬眠ボックス。自然な採餌エリアへのアクセス",
                     "notes": "Wild species — captive breeding restricted in many countries; natural hibernators; high parasite burden (lungworm especially)",
                     "notes_ja": "野生種。多くの国で飼育繁殖が制限されている。自然冬眠する。寄生虫（特に肺虫）の感染率が高い"}},
        {"id": "hedgehog_long_eared", "name": "Long-eared Hedgehog", "name_ja": "オオミミハリネズミ",
         "risk": {"Ear Infections": 1.5, "Mite Infestation": 1.5},
         "ecology": {"temperature": {"min": 22, "max": 30, "unit": "°C"},
                     "humidity": {"min": 30, "max": 50, "unit": "%"},
                     "lifespan": {"min": 3, "max": 6, "unit": "years"},
                     "weight": {"min": 200, "max": 500, "unit": "g"},
                     "diet": "Insectivore/omnivore; insects as primary diet, supplemented with low-fat cat food and occasional fruit",
                     "diet_ja": "食虫性/雑食性。昆虫を主食に、低脂肪キャットフードと時々の果物で補助",
                     "housing": "Warm, dry enclosure; large ears assist thermoregulation in arid climates; sand substrate appreciated",
                     "housing_ja": "暖かく乾燥したケージ。大きな耳が乾燥した気候での体温調節を助ける。砂の床材を好む",
                     "notes": "Desert-adapted species — prefers drier conditions than African pygmy; large ears prone to infections — check regularly; active runners",
                     "notes_ja": "砂漠適応種。ヨツユビハリネズミより乾燥した環境を好む。大きな耳は感染症になりやすいため定期チェック。活発に走る"}},
    ],
    "bird": [
        {"id": "bird_mixed", "name": "Mixed/Other", "name_ja": "その他",
         "risk": {},
         "ecology": {"temperature": {"min": 18, "max": 28, "unit": "°C"},
                     "humidity": {"min": 40, "max": 70, "unit": "%"},
                     "lifespan": {"min": 5, "max": 15, "unit": "years"},
                     "weight": {"min": 15, "max": 500, "unit": "g"},
                     "diet": "Varies by species; balanced seed/pellet mix with fresh fruits and vegetables",
                     "diet_ja": "種によって異なる。バランスの取れたシード/ペレットに新鮮な果物と野菜",
                     "housing": "Appropriate-sized cage with perches of varying diameter; daily out-of-cage time if tame",
                     "housing_ja": "適切なサイズのケージに太さの異なる止まり木。馴れている場合は毎日の放鳥時間",
                     "notes": "Species-specific care varies widely; avoid Teflon/PTFE fumes, scented candles, and aerosol sprays near birds",
                     "notes_ja": "種ごとのケアは大きく異なる。テフロン/PTFE煙・アロマキャンドル・エアゾールスプレーは鳥の近くで厳禁"}},
        {"id": "bird_canary", "name": "Canary", "name_ja": "カナリア",
         "risk": {"Air Sac Mites": 2.0, "Avian Pox": 1.5, "Coccidiosis": 1.5,
                  "Feather Cysts": 1.8, "Atoxoplasmosis": 2.0},
         "ecology": {"temperature": {"min": 16, "max": 26, "unit": "°C"},
                     "humidity": {"min": 40, "max": 65, "unit": "%"},
                     "lifespan": {"min": 10, "max": 15, "unit": "years"},
                     "weight": {"min": 15, "max": 30, "unit": "g"},
                     "diet": "Granivore; high-quality canary seed mix with pellets, fresh leafy greens, egg food during molting",
                     "diet_ja": "穀食性。高品質カナリアシードミックスとペレット、新鮮な葉野菜、換羽期にエッグフード",
                     "housing": "Wide flight cage (horizontal space more important than height); natural light cycle for singing and breeding",
                     "housing_ja": "横に広いフライトケージ（高さより横幅が重要）。さえずりと繁殖のため自然な明暗サイクル",
                     "notes": "Males sing — need 10-12 hours daylight; very sensitive to air quality and drafts; air sac mites are a major threat",
                     "notes_ja": "オスはさえずる。10〜12時間の日照が必要。空気の質と隙間風に非常に敏感。気嚢ダニが主要な脅威"}},
        {"id": "bird_finch", "name": "Finch", "name_ja": "フィンチ",
         "risk": {"Air Sac Mites": 2.0, "Coccidiosis": 1.5, "Scaly Leg Mites": 1.5,
                  "Atoxoplasmosis": 1.8},
         "ecology": {"temperature": {"min": 18, "max": 27, "unit": "°C"},
                     "humidity": {"min": 40, "max": 65, "unit": "%"},
                     "lifespan": {"min": 5, "max": 10, "unit": "years"},
                     "weight": {"min": 10, "max": 30, "unit": "g"},
                     "diet": "Granivore; finch seed mix, sprouted seeds, leafy greens, occasional egg food",
                     "diet_ja": "穀食性。フィンチ用シードミックス、発芽シード、葉野菜、時々エッグフード",
                     "housing": "Wide flight cage or aviary; social — best kept in pairs or small flocks; multiple perches",
                     "housing_ja": "横に広いフライトケージまたは禽舎。社会性が高くペアまたは小群で飼育。複数の止まり木",
                     "notes": "Social birds — should not be kept alone; prone to air sac mites — watch for open-mouth breathing and tail bobbing",
                     "notes_ja": "社会性の高い鳥で単独飼育は避ける。気嚢ダニに注意。開口呼吸や尾の上下運動は要注意サイン"}},
        {"id": "bird_java_sparrow", "name": "Java Sparrow", "name_ja": "文鳥",
         "risk": {"Egg Binding": 1.8, "Obesity": 1.5, "Iron Storage Disease": 1.5,
                  "Gout": 1.5, "Bumblefoot (Pododermatitis)": 1.3},
         "ecology": {"temperature": {"min": 20, "max": 28, "unit": "°C"},
                     "humidity": {"min": 40, "max": 65, "unit": "%"},
                     "lifespan": {"min": 7, "max": 12, "unit": "years"},
                     "weight": {"min": 22, "max": 35, "unit": "g"},
                     "diet": "Granivore; finch/java sparrow seed mix, pellets, leafy greens, cuttlebone for calcium",
                     "diet_ja": "穀食性。文鳥用シードミックス、ペレット、葉野菜、カルシウム補給にカトルボーン",
                     "housing": "Medium-sized cage with varied perch diameters; bathing dish essential — loves to bathe daily",
                     "housing_ja": "中型ケージに太さの異なる止まり木。水浴び容器は必須。毎日の水浴びを好む",
                     "notes": "Hand-raised individuals very social and affectionate; prone to egg binding in females — ensure calcium; monitor weight (obesity risk)",
                     "notes_ja": "手乗りの個体は非常に社交的で愛情深い。メスは卵詰まりに注意しカルシウムを確保。肥満に注意して体重管理"}},
        {"id": "bird_dove", "name": "Dove/Pigeon", "name_ja": "ハト",
         "risk": {"Trichomoniasis": 2.5, "Paramyxovirus Infection": 2.0,
                  "Coccidiosis": 1.8, "Candidiasis": 1.5},
         "ecology": {"temperature": {"min": 15, "max": 30, "unit": "°C"},
                     "humidity": {"min": 40, "max": 65, "unit": "%"},
                     "lifespan": {"min": 10, "max": 20, "unit": "years"},
                     "weight": {"min": 150, "max": 500, "unit": "g"},
                     "diet": "Granivore; pigeon/dove seed mix with grains, grit essential for digestion, fresh greens",
                     "diet_ja": "穀食性。ハト用シードミックスと穀物、消化のためグリットが必須、新鮮な野菜",
                     "housing": "Large cage or outdoor aviary; floor-dwellers — need flat perches and floor space; paired housing preferred",
                     "housing_ja": "大型ケージまたは屋外禽舎。地上性のため平らな止まり木と床面積が必要。ペア飼育推奨",
                     "notes": "Very prone to trichomoniasis (canker) — check for oral lesions; paramyxovirus vaccination available; gentle temperament",
                     "notes_ja": "トリコモナス症（キャンカー）に非常にかかりやすい。口腔内病変をチェック。パラミクソウイルスワクチンあり。穏やかな性格"}},
        {"id": "bird_mynah", "name": "Mynah Bird", "name_ja": "キュウカンチョウ",
         "risk": {"Iron Storage Disease": 3.0, "Hemochromatosis": 3.0, "Obesity": 1.5},
         "ecology": {"temperature": {"min": 20, "max": 30, "unit": "°C"},
                     "humidity": {"min": 50, "max": 70, "unit": "%"},
                     "lifespan": {"min": 12, "max": 25, "unit": "years"},
                     "weight": {"min": 150, "max": 250, "unit": "g"},
                     "diet": "Omnivore/frugivore; low-iron pellets critical, fresh fruit, insects; NO high-iron foods (grapes, raisins, red meat)",
                     "diet_ja": "雑食性/果食性。低鉄分ペレットが必須、新鮮な果物、昆虫。高鉄分食品（ブドウ、レーズン、赤肉）は厳禁",
                     "housing": "Large cage — very active and messy; daily bathing opportunity; easy to clean surfaces essential",
                     "housing_ja": "大型ケージ。非常に活発で食べ散らかす。毎日の水浴びの機会。掃除しやすい素材が必須",
                     "notes": "Extremely prone to iron storage disease (hemochromatosis) — low-iron diet is critical; excellent mimics of human speech",
                     "notes_ja": "鉄貯蔵病（ヘモクロマトーシス）に極めてかかりやすい。低鉄分食が不可欠。人間の声の模倣が非常に上手い"}},
    ],
    "parakeet": [
        {"id": "parakeet_budgerigar", "name": "Budgerigar", "name_ja": "セキセイインコ",
         "risk": {"Budgerigar Fledgling Disease (BFD)": 2.5, "Tumors/Neoplasia": 2.0,
                  "Scaly Face Mites": 1.8, "Megabacteriosis (AGY)": 2.0, "Goiter": 1.5},
         "ecology": {"temperature": {"min": 18, "max": 28, "unit": "°C"},
                     "humidity": {"min": 40, "max": 65, "unit": "%"},
                     "lifespan": {"min": 5, "max": 10, "unit": "years"},
                     "weight": {"min": 25, "max": 40, "unit": "g"},
                     "diet": "Granivore/herbivore; pellet-based diet with seed mix, fresh vegetables and fruits, cuttlebone for calcium and iodine",
                     "diet_ja": "穀食性/草食性。ペレット主体にシードミックス、新鮮な野菜と果物、カトルボーンでカルシウムとヨウ素補給",
                     "housing": "Wide cage for flight; multiple perches of varying diameters; toys for mental stimulation; daily out-of-cage time",
                     "housing_ja": "飛べる横幅のケージ。太さの異なる複数の止まり木。知育玩具。毎日の放鳥時間",
                     "notes": "Very high tumor rate (especially after age 5); iodine deficiency causes goiter — provide iodine supplement; prone to scaly face mites",
                     "notes_ja": "腫瘍発生率が非常に高い（特に5歳以降）。ヨウ素欠乏で甲状腺腫。ヨウ素補給が必要。疥癬ダニに注意"}},
        {"id": "parakeet_cockatiel", "name": "Cockatiel", "name_ja": "オカメインコ",
         "risk": {"Fatty Liver Disease (Hepatic Lipidosis)": 2.0, "Night Frights": 1.5,
                  "Egg Binding": 1.8, "Chronic Egg Laying": 2.0},
         "ecology": {"temperature": {"min": 18, "max": 28, "unit": "°C"},
                     "humidity": {"min": 40, "max": 65, "unit": "%"},
                     "lifespan": {"min": 15, "max": 25, "unit": "years"},
                     "weight": {"min": 75, "max": 120, "unit": "g"},
                     "diet": "Granivore/herbivore; pellet-based diet essential (seed-only leads to fatty liver); fresh vegetables, limited seeds and fruit",
                     "diet_ja": "穀食性/草食性。ペレット主体が必須（シードのみは脂肪肝の原因）。新鮮な野菜、シードと果物は少量",
                     "housing": "Large cage with horizontal bars for climbing; dim night light to prevent night frights; daily socialization",
                     "housing_ja": "横棒付きの大型ケージで登りやすく。夜のパニック予防に常夜灯。毎日のスキンシップ",
                     "notes": "Very prone to fatty liver on seed-only diet; night frights common — leave dim light at night; chronic egg laying in females — manage daylight hours",
                     "notes_ja": "シードのみの食事は脂肪肝を招く。夜のパニックが多い。常夜灯を。メスの慢性産卵には日照時間管理が必要"}},
        {"id": "parakeet_lovebird", "name": "Lovebird", "name_ja": "コザクラインコ/ボタンインコ",
         "risk": {"Psittacine Beak and Feather Disease (PBFD)": 1.5, "Feather Plucking": 1.5,
                  "Chronic Egg Laying": 1.8},
         "ecology": {"temperature": {"min": 18, "max": 28, "unit": "°C"},
                     "humidity": {"min": 40, "max": 65, "unit": "%"},
                     "lifespan": {"min": 10, "max": 20, "unit": "years"},
                     "weight": {"min": 40, "max": 60, "unit": "g"},
                     "diet": "Granivore/herbivore; pellet-based diet with fresh vegetables, small amount of seeds, fruit as treats",
                     "diet_ja": "穀食性/草食性。ペレット主体に新鮮な野菜、少量のシード、果物はおやつ程度",
                     "housing": "Medium-large cage; very active — need climbing toys and foraging enrichment; can be kept in pairs",
                     "housing_ja": "中〜大型ケージ。非常に活発で登り遊びと採餌エンリッチメントが必要。ペア飼育も可能",
                     "notes": "Strong pair bond — may become aggressive if kept singly without sufficient attention; chronic egg laying in females; nippy if not socialized",
                     "notes_ja": "強いペア結合。単独飼育で関心が不足すると攻撃的に。メスの慢性産卵に注意。社会化不足だと噛む傾向"}},
    ],
    "parrot": [
        {"id": "parrot_african_grey", "name": "African Grey", "name_ja": "ヨウム",
         "risk": {"Feather Plucking": 2.5, "Hypocalcemia": 2.5, "Aspergillosis": 2.0,
                  "Psittacine Beak and Feather Disease (PBFD)": 1.5},
         "ecology": {"temperature": {"min": 20, "max": 28, "unit": "°C"},
                     "humidity": {"min": 50, "max": 70, "unit": "%"},
                     "lifespan": {"min": 40, "max": 60, "unit": "years"},
                     "weight": {"min": 350, "max": 550, "unit": "g"},
                     "diet": "Omnivore; pellet-based diet with fresh vegetables, fruits, nuts; calcium-rich foods critical (broccoli, almonds)",
                     "diet_ja": "雑食性。ペレット主体に新鮮な野菜・果物・ナッツ。カルシウム豊富な食品（ブロッコリー、アーモンド）が重要",
                     "housing": "Very large cage with complex enrichment; foraging toys; daily social interaction essential for mental health",
                     "housing_ja": "複雑なエンリッチメント付きの非常に大きなケージ。採餌玩具。精神的健康のため毎日の社会的交流が必須",
                     "notes": "Extremely intelligent — needs extensive mental stimulation; very prone to hypocalcemia and feather plucking; can live 50+ years — lifetime commitment",
                     "notes_ja": "極めて知能が高く豊富な精神的刺激が必要。低カルシウム血症と毛引き症に非常になりやすい。50年以上生きるため終生飼養の覚悟が必要"}},
        {"id": "parrot_amazon", "name": "Amazon Parrot", "name_ja": "アマゾン",
         "risk": {"Fatty Liver Disease (Hepatic Lipidosis)": 2.5, "Obesity": 2.0,
                  "Foot Necrosis (Bumblefoot)": 1.5, "Bumblefoot (Pododermatitis)": 1.5},
         "ecology": {"temperature": {"min": 20, "max": 28, "unit": "°C"},
                     "humidity": {"min": 50, "max": 70, "unit": "%"},
                     "lifespan": {"min": 30, "max": 50, "unit": "years"},
                     "weight": {"min": 300, "max": 600, "unit": "g"},
                     "diet": "Omnivore; pellet-based diet with abundant vegetables; strictly limit seeds, nuts, and fatty foods (obesity/fatty liver risk)",
                     "diet_ja": "雑食性。ペレット主体に豊富な野菜。シード・ナッツ・脂肪の多い食品は厳しく制限（肥満・脂肪肝リスク）",
                     "housing": "Large, sturdy cage; strong chewer — needs hardwood perches and durable toys; daily exercise outside cage",
                     "housing_ja": "大型の頑丈なケージ。噛む力が強いため硬い木の止まり木と丈夫な玩具。毎日のケージ外運動",
                     "notes": "Very prone to obesity and fatty liver — calorie control essential; can become aggressive during breeding season; loud vocalizations",
                     "notes_ja": "肥満と脂肪肝に非常になりやすい。カロリー管理が不可欠。繁殖期に攻撃的になることがある。大きな声で鳴く"}},
        {"id": "parrot_macaw", "name": "Macaw", "name_ja": "コンゴウインコ",
         "risk": {"Proventricular Dilatation Disease (PDD)": 2.0, "Feather Plucking": 1.8,
                  "Psittacine Beak and Feather Disease (PBFD)": 1.5},
         "ecology": {"temperature": {"min": 20, "max": 30, "unit": "°C"},
                     "humidity": {"min": 50, "max": 70, "unit": "%"},
                     "lifespan": {"min": 50, "max": 80, "unit": "years"},
                     "weight": {"min": 900, "max": 1500, "unit": "g"},
                     "diet": "Omnivore; pellet-based diet with fresh fruits, vegetables, and nuts (higher fat needs than smaller parrots)",
                     "diet_ja": "雑食性。ペレット主体に新鮮な果物・野菜・ナッツ（小型インコより脂肪の必要量が多い）",
                     "housing": "Very large walk-in aviary or macaw-specific cage; extremely strong beak — needs heavy-duty construction",
                     "housing_ja": "非常に大型のウォークインアビアリーまたはコンゴウインコ専用ケージ。嘴の力が極めて強いため頑丈な構造が必要",
                     "notes": "Can live 80+ years — multi-generational commitment; PDD is a serious threat; very loud — consider neighbors; powerful beak can cause injury",
                     "notes_ja": "80年以上生きることがある。世代を超えた飼育の覚悟が必要。PDD（腺胃拡張症）は深刻な脅威。非常に大きな声。強力な嘴で怪我の危険"}},
        {"id": "parrot_cockatoo", "name": "Cockatoo", "name_ja": "オウム科",
         "risk": {"Feather Plucking": 3.0, "Psittacine Beak and Feather Disease (PBFD)": 2.0,
                  "Fatty Liver Disease (Hepatic Lipidosis)": 1.8},
         "ecology": {"temperature": {"min": 18, "max": 28, "unit": "°C"},
                     "humidity": {"min": 40, "max": 65, "unit": "%"},
                     "lifespan": {"min": 40, "max": 70, "unit": "years"},
                     "weight": {"min": 300, "max": 900, "unit": "g"},
                     "diet": "Omnivore; pellet-based diet with vegetables, limited seeds and nuts; low-fat diet to prevent hepatic lipidosis",
                     "diet_ja": "雑食性。ペレット主体に野菜。シードとナッツは制限。肝リピドーシス予防のため低脂肪食",
                     "housing": "Very large cage or aviary; extensive enrichment and foraging opportunities; needs hours of daily interaction",
                     "housing_ja": "非常に大きなケージまたはアビアリー。豊富なエンリッチメントと採餌機会。毎日数時間の触れ合いが必要",
                     "notes": "Highest feather plucking rate of all parrots — often stress/boredom-related; extremely needy and loud; powder-down dust allergy risk for owners",
                     "notes_ja": "全オウム目で最も毛引き率が高い。ストレス・退屈が原因のことが多い。非常に甘えん坊で大声。粉綿羽による飼い主のアレルギーリスクあり"}},
    ],
    "reptile": [
        {"id": "reptile_general", "name": "General Reptile", "name_ja": "爬虫類（一般）",
         "risk": {},
         "ecology": {"temperature": {"min": 24, "max": 32, "unit": "°C"},
                     "humidity": {"min": 40, "max": 70, "unit": "%"},
                     "lifespan": {"min": 10, "max": 30, "unit": "years"},
                     "weight": {"min": 20, "max": 5000, "unit": "g"},
                     "diet": "Varies by species; insectivores, herbivores, or carnivores",
                     "diet_ja": "種により異なる。食虫性、草食性、肉食性",
                     "housing": "Species-appropriate terrarium with thermal gradient, UVB lighting, and proper substrate",
                     "housing_ja": "温度勾配・UVBライト・適切な床材を備えた種に適したテラリウム",
                     "notes": "Ectothermic — proper temperature gradient critical; UVB essential for calcium metabolism in most species; quarantine new animals",
                     "notes_ja": "変温動物のため適切な温度勾配が不可欠。多くの種でカルシウム代謝にUVBが必須。新規個体は検疫を"}},
        {"id": "reptile_ball_python", "name": "Ball Python", "name_ja": "ボールパイソン",
         "risk": {"Respiratory Infection": 1.8, "Inclusion Body Disease (IBD)": 2.0,
                  "Mite Infestation": 1.5, "Anorexia/Feeding Refusal": 2.0},
         "ecology": {"temperature": {"min": 26, "max": 32, "unit": "°C"},
                     "humidity": {"min": 50, "max": 65, "unit": "%"},
                     "lifespan": {"min": 20, "max": 30, "unit": "years"},
                     "weight": {"min": 1200, "max": 2500, "unit": "g"},
                     "diet": "Carnivore; appropriately sized frozen-thawed rodents every 1-2 weeks (adults)",
                     "diet_ja": "肉食性。適切なサイズの冷凍解凍マウス/ラットを1〜2週間に1回（成体）",
                     "housing": "Enclosed terrarium with warm side (30-32°C) and cool side (26-28°C); multiple hides; water bowl for soaking",
                     "housing_ja": "温かい側（30〜32°C）と涼しい側（26〜28°C）の温度勾配付き密閉テラリウム。複数の隠れ家。浸かれる水入れ",
                     "notes": "Very common feeding refusal — often seasonal or stress-related, not always pathological; IBD is fatal and contagious; handle gently",
                     "notes_ja": "拒食が非常に多いが季節性やストレス性のことも多く必ずしも病的ではない。IBDは致死的で伝染性あり。穏やかに扱う"}},
        {"id": "reptile_bearded_dragon", "name": "Bearded Dragon", "name_ja": "フトアゴヒゲトカゲ",
         "risk": {"Metabolic Bone Disease": 2.0, "Adenovirus Infection": 2.0,
                  "Yellow Fungus Disease": 1.8, "Impaction": 1.5},
         "ecology": {"temperature": {"min": 26, "max": 40, "unit": "°C"},
                     "humidity": {"min": 30, "max": 50, "unit": "%"},
                     "lifespan": {"min": 8, "max": 15, "unit": "years"},
                     "weight": {"min": 300, "max": 600, "unit": "g"},
                     "diet": "Omnivore; juveniles 70% insects/30% vegetables, adults 70% vegetables/30% insects; calcium/D3 dusting essential",
                     "diet_ja": "雑食性。幼体は昆虫70%/野菜30%、成体は野菜70%/昆虫30%。カルシウム/D3のダスティングが必須",
                     "housing": "Large terrarium with basking spot (38-40°C), cool end (26-28°C), UVB 10-12% tube; desert substrate",
                     "housing_ja": "バスキングスポット（38〜40°C）、涼しい側（26〜28°C）、UVB 10-12%チューブ付き大型テラリウム。砂漠系床材",
                     "notes": "UVB lighting critical for MBD prevention; adenovirus (ADV) testing recommended; brumation is normal in winter; avoid loose particle substrate in juveniles",
                     "notes_ja": "MBD予防にUVBライトが不可欠。アデノウイルス（ADV）検査推奨。冬季の休眠（ブルメーション）は正常。幼体には粒子状床材を避ける"}},
        {"id": "reptile_leopard_gecko", "name": "Leopard Gecko", "name_ja": "ヒョウモントカゲモドキ",
         "risk": {"Metabolic Bone Disease": 1.5, "Cryptosporidiosis": 2.0,
                  "Impaction": 1.8},
         "ecology": {"temperature": {"min": 24, "max": 32, "unit": "°C"},
                     "humidity": {"min": 30, "max": 50, "unit": "%"},
                     "lifespan": {"min": 15, "max": 25, "unit": "years"},
                     "weight": {"min": 40, "max": 100, "unit": "g"},
                     "diet": "Insectivore; gut-loaded crickets, mealworms, dubia roaches; calcium/D3 dusting every feeding",
                     "diet_ja": "食虫性。ガットローディングしたコオロギ・ミルワーム・デュビアローチ。毎回カルシウム/D3ダスティング",
                     "housing": "Terrarium with under-tank heater (warm side 30-32°C, cool side 24-26°C); moist hide for shedding; no UVB required but beneficial",
                     "housing_ja": "パネルヒーター付きテラリウム（温かい側30〜32°C、涼しい側24〜26°C）。脱皮用のウェットシェルター。UVBは不要だが有益",
                     "notes": "Crepuscular — active at dawn/dusk; cryptosporidiosis is incurable and contagious — quarantine new animals; tail stores fat reserves",
                     "notes_ja": "薄明薄暮性。クリプトスポリジウム症は治癒不能で伝染性あり。新規個体は検疫必須。尾に脂肪を蓄える"}},
    ],
    "tortoise": [
        {"id": "tortoise_russian", "name": "Russian Tortoise", "name_ja": "ロシアリクガメ",
         "risk": {"Respiratory Infection": 1.5, "Upper Respiratory Tract Infection (URTI)": 1.5, "Shell Rot": 1.3},
         "ecology": {"temperature": {"min": 20, "max": 32, "unit": "°C"},
                     "humidity": {"min": 40, "max": 60, "unit": "%"},
                     "lifespan": {"min": 40, "max": 60, "unit": "years"},
                     "weight": {"min": 0.8, "max": 2.5, "unit": "kg"},
                     "diet": "Herbivore; dark leafy greens (dandelion, clover, endive), weeds, hay; no fruit or animal protein",
                     "diet_ja": "草食性。濃い葉野菜（タンポポ、クローバー、エンダイブ）、雑草、牧草。果物や動物性タンパク質は不可",
                     "housing": "Outdoor enclosure preferred; indoor terrarium with UVB and basking spot if kept inside; burrowing substrate",
                     "housing_ja": "屋外飼育が理想。室内ならUVBとバスキングスポット付きテラリウム。穴掘り可能な床材",
                     "notes": "Hardy species; active burrower — enclosure must prevent escape; hibernates in winter; prone to URTI in damp conditions",
                     "notes_ja": "丈夫な種。活発に穴を掘るため脱走防止が必要。冬季に冬眠。湿った環境では上部気道感染症に注意"}},
        {"id": "tortoise_hermann", "name": "Hermann's Tortoise", "name_ja": "ヘルマンリクガメ",
         "risk": {"Metabolic Bone Disease": 1.5, "Herpesvirus": 1.5},
         "ecology": {"temperature": {"min": 20, "max": 32, "unit": "°C"},
                     "humidity": {"min": 40, "max": 60, "unit": "%"},
                     "lifespan": {"min": 50, "max": 80, "unit": "years"},
                     "weight": {"min": 1.0, "max": 4.0, "unit": "kg"},
                     "diet": "Herbivore; Mediterranean weeds and leafy greens; high fiber, low protein; calcium supplementation with UVB",
                     "diet_ja": "草食性。地中海系の雑草と葉野菜。高繊維・低タンパク質。UVBと併せてカルシウム補給",
                     "housing": "Outdoor Mediterranean-style enclosure ideal; indoor with UVB (10-12%) and basking spot (30-32°C)",
                     "housing_ja": "屋外の地中海風飼育場が理想。室内ではUVB（10〜12%）とバスキングスポット（30〜32°C）",
                     "notes": "Herpesvirus is species-specific and fatal — never mix with other tortoise species; hibernation normal; long-lived — lifetime commitment",
                     "notes_ja": "ヘルペスウイルスは種特異的で致死的。他種のカメとの混合飼育は厳禁。冬眠は正常。長寿のため終生飼養の覚悟が必要"}},
        {"id": "tortoise_sulcata", "name": "Sulcata Tortoise", "name_ja": "ケヅメリクガメ",
         "risk": {"Pyramiding": 2.0, "Bladder Stones": 1.8, "Metabolic Bone Disease": 1.5},
         "ecology": {"temperature": {"min": 24, "max": 35, "unit": "°C"},
                     "humidity": {"min": 40, "max": 55, "unit": "%"},
                     "lifespan": {"min": 70, "max": 100, "unit": "years"},
                     "weight": {"min": 45, "max": 100, "unit": "kg"},
                     "diet": "Herbivore; grass and grass hay (80%+), broadleaf weeds; no fruit, minimal vegetables; high fiber critical to prevent pyramiding",
                     "diet_ja": "草食性。牧草と乾草が80%以上、広葉雑草。果物は不可、野菜は最小限。ピラミッド化予防のため高繊維が重要",
                     "housing": "Very large outdoor enclosure essential (adults 50-100kg); heated shelter for cold nights; strong fencing as they are powerful diggers",
                     "housing_ja": "成体50〜100kgのため非常に大きな屋外飼育場が必須。寒い夜は加温シェルター。強力な掘り手のため頑丈なフェンス",
                     "notes": "Third-largest tortoise species — grows very large very fast; pyramiding from low humidity/poor diet is common; bladder stones from dehydration; enormous space needed",
                     "notes_ja": "世界で3番目に大きなカメ。非常に早く大きくなる。低湿度・不適切な食事によるピラミッド化が多い。脱水による膀胱結石。膨大なスペースが必要"}},
        {"id": "tortoise_leopard", "name": "Leopard Tortoise", "name_ja": "ヒョウモンガメ",
         "risk": {"Respiratory Infection": 1.8, "Upper Respiratory Tract Infection (URTI)": 1.8, "Parasitic Infection": 1.5},
         "ecology": {"temperature": {"min": 24, "max": 34, "unit": "°C"},
                     "humidity": {"min": 40, "max": 60, "unit": "%"},
                     "lifespan": {"min": 50, "max": 100, "unit": "years"},
                     "weight": {"min": 15, "max": 40, "unit": "kg"},
                     "diet": "Herbivore; grass and grass hay, broadleaf weeds, mixed greens; avoid fruit and high-oxalate vegetables",
                     "diet_ja": "草食性。牧草と乾草、広葉雑草、混合葉野菜。果物やシュウ酸の多い野菜は避ける",
                     "housing": "Large outdoor enclosure with warm, dry conditions; does not hibernate — needs heated shelter in cold climates",
                     "housing_ja": "暖かく乾燥した大型屋外飼育場。冬眠しないため寒冷地では加温シェルターが必要",
                     "notes": "Sensitive to cold and damp — URTI risk in humid/cool conditions; does not hibernate (unlike Russian/Hermann's); parasite screening recommended",
                     "notes_ja": "寒さと湿気に弱い。湿度が高く涼しい環境ではURTIリスク。冬眠しない（ロシア/ヘルマンとは異なる）。寄生虫検査を推奨"}},
    ],
    "snake": [
        {"id": "snake_ball_python", "name": "Ball Python", "name_ja": "ボールパイソン",
         "risk": {"Respiratory Infection": 1.8, "Inclusion Body Disease (IBD)": 2.0,
                  "Anorexia/Feeding Refusal": 2.0, "Mite Infestation": 1.5},
         "ecology": {"temperature": {"min": 26, "max": 32, "unit": "°C"},
                     "humidity": {"min": 50, "max": 65, "unit": "%"},
                     "lifespan": {"min": 20, "max": 30, "unit": "years"},
                     "weight": {"min": 1200, "max": 2500, "unit": "g"},
                     "diet": "Carnivore; appropriately sized frozen-thawed rodents every 1-2 weeks (adults)",
                     "diet_ja": "肉食性。適切なサイズの冷凍解凍マウス/ラットを1〜2週間に1回（成体）",
                     "housing": "Enclosed terrarium with warm side (30-32°C) and cool side (26-28°C); multiple snug hides; water bowl for soaking",
                     "housing_ja": "温かい側（30〜32°C）と涼しい側（26〜28°C）の温度勾配付き密閉テラリウム。体にフィットする複数の隠れ家。浸かれる水入れ",
                     "notes": "Seasonal feeding refusal is common and usually not pathological; IBD is fatal — quarantine new snakes; shy species that curls into a ball when stressed",
                     "notes_ja": "季節的な拒食は一般的で通常は病的ではない。IBDは致死的。新規個体は検疫。ストレスでボール状に丸まるシャイな種"}},
        {"id": "snake_corn_snake", "name": "Corn Snake", "name_ja": "コーンスネーク",
         "risk": {"Inclusion Body Disease (IBD)": 1.3, "Dysecdysis (Retained Shed)": 1.5},
         "ecology": {"temperature": {"min": 22, "max": 30, "unit": "°C"},
                     "humidity": {"min": 40, "max": 60, "unit": "%"},
                     "lifespan": {"min": 15, "max": 20, "unit": "years"},
                     "weight": {"min": 250, "max": 600, "unit": "g"},
                     "diet": "Carnivore; appropriately sized frozen-thawed mice every 7-14 days (adults)",
                     "diet_ja": "肉食性。適切なサイズの冷凍解凍マウスを7〜14日に1回（成体）",
                     "housing": "Secure terrarium (excellent escape artists); warm side (28-30°C), cool side (22-24°C); climbing branches; humid hide for shedding",
                     "housing_ja": "脱走防止の安全なテラリウム（脱走の名手）。温かい側（28〜30°C）、涼しい側（22〜24°C）。登り枝。脱皮用ウェットシェルター",
                     "notes": "Excellent beginner snake; good appetite and temperament; ensure proper humidity for complete sheds; notorious escape artists — secure lid essential",
                     "notes_ja": "初心者に最適なヘビ。食欲旺盛で温和な性格。完全な脱皮のため適切な湿度を確保。脱走の名手のため蓋の固定が必須"}},
        {"id": "snake_king_snake", "name": "King Snake", "name_ja": "キングスネーク",
         "risk": {"Dysecdysis (Retained Shed)": 1.3},
         "ecology": {"temperature": {"min": 22, "max": 30, "unit": "°C"},
                     "humidity": {"min": 40, "max": 60, "unit": "%"},
                     "lifespan": {"min": 15, "max": 25, "unit": "years"},
                     "weight": {"min": 400, "max": 1500, "unit": "g"},
                     "diet": "Carnivore; frozen-thawed rodents every 7-14 days; ophiophagous — never house with other snakes",
                     "diet_ja": "肉食性。冷凍解凍マウスを7〜14日に1回。蛇食性のため他のヘビとの同居は厳禁",
                     "housing": "Secure terrarium; warm side (28-30°C), cool side (22-24°C); hides on both temperature ends; ALWAYS house alone",
                     "housing_ja": "安全なテラリウム。温かい側（28〜30°C）、涼しい側（22〜24°C）。両端に隠れ家。必ず単独飼育",
                     "notes": "Ophiophagous (eats other snakes) — strictly solitary housing; generally hardy with good feeding response; various species with different needs",
                     "notes_ja": "蛇食性（他のヘビを食べる）のため厳格な単独飼育。一般的に丈夫で食欲旺盛。種によって必要環境が異なる"}},
        {"id": "snake_boa", "name": "Boa Constrictor", "name_ja": "ボアコンストリクター",
         "risk": {"Inclusion Body Disease (IBD)": 2.5, "Respiratory Infection": 1.5,
                  "Mite Infestation": 1.5},
         "ecology": {"temperature": {"min": 26, "max": 33, "unit": "°C"},
                     "humidity": {"min": 55, "max": 75, "unit": "%"},
                     "lifespan": {"min": 20, "max": 30, "unit": "years"},
                     "weight": {"min": 7, "max": 27, "unit": "kg"},
                     "diet": "Carnivore; frozen-thawed rats or rabbits (based on size) every 2-4 weeks for adults",
                     "diet_ja": "肉食性。サイズに応じた冷凍解凍ラットまたはウサギを成体は2〜4週間に1回",
                     "housing": "Very large, secure enclosure (adults 2-3m); warm side (30-33°C), cool side (26-28°C); sturdy climbing branches; large water dish",
                     "housing_ja": "成体2〜3mのため非常に大きく安全な飼育容器。温かい側（30〜33°C）、涼しい側（26〜28°C）。頑丈な登り枝。大きな水入れ",
                     "notes": "IBD is the greatest threat — strict quarantine for new animals; can grow very large (2-3m); requires experienced keeper; higher humidity than most colubrids",
                     "notes_ja": "IBDが最大の脅威。新規個体は厳格な検疫。非常に大きくなる（2〜3m）。経験者向け。ナミヘビ類より高い湿度が必要"}},
    ],
    "lizard": [
        {"id": "lizard_leopard_gecko", "name": "Leopard Gecko", "name_ja": "ヒョウモントカゲモドキ",
         "risk": {"Metabolic Bone Disease": 1.5, "Cryptosporidiosis": 2.0,
                  "Dysecdysis (Retained Shed)": 1.5, "Impaction": 1.8},
         "ecology": {"temperature": {"min": 24, "max": 32, "unit": "°C"},
                     "humidity": {"min": 30, "max": 50, "unit": "%"},
                     "lifespan": {"min": 15, "max": 25, "unit": "years"},
                     "weight": {"min": 40, "max": 100, "unit": "g"},
                     "diet": "Insectivore; gut-loaded crickets, mealworms, dubia roaches; calcium/D3 dusting every feeding",
                     "diet_ja": "食虫性。ガットローディングしたコオロギ・ミルワーム・デュビアローチ。毎回カルシウム/D3ダスティング",
                     "housing": "Terrarium with under-tank heater (warm side 30-32°C, cool side 24-26°C); moist hide for shedding; no UVB required but beneficial",
                     "housing_ja": "パネルヒーター付きテラリウム（温かい側30〜32°C、涼しい側24〜26°C）。脱皮用ウェットシェルター。UVBは不要だが有益",
                     "notes": "Crepuscular — active at dawn/dusk; cryptosporidiosis is incurable and contagious — quarantine new animals; tail stores fat reserves",
                     "notes_ja": "薄明薄暮性。クリプトスポリジウム症は治癒不能で伝染性あり。新規個体は検疫必須。尾に脂肪を蓄える"}},
        {"id": "lizard_bearded_dragon", "name": "Bearded Dragon", "name_ja": "フトアゴヒゲトカゲ",
         "risk": {"Metabolic Bone Disease": 2.0, "Adenovirus Infection": 2.0,
                  "Yellow Fungus Disease": 1.8, "Impaction": 1.5, "Parasitic Infection": 1.5},
         "ecology": {"temperature": {"min": 26, "max": 40, "unit": "°C"},
                     "humidity": {"min": 30, "max": 50, "unit": "%"},
                     "lifespan": {"min": 8, "max": 15, "unit": "years"},
                     "weight": {"min": 300, "max": 600, "unit": "g"},
                     "diet": "Omnivore; juveniles 70% insects/30% vegetables, adults 70% vegetables/30% insects; calcium/D3 dusting essential",
                     "diet_ja": "雑食性。幼体は昆虫70%/野菜30%、成体は野菜70%/昆虫30%。カルシウム/D3のダスティングが必須",
                     "housing": "Large terrarium with basking spot (38-40°C), cool end (26-28°C), UVB 10-12% tube; desert substrate",
                     "housing_ja": "バスキングスポット（38〜40°C）、涼しい側（26〜28°C）、UVB 10-12%チューブ付き大型テラリウム。砂漠系床材",
                     "notes": "UVB lighting critical for MBD prevention; adenovirus (ADV) testing recommended; brumation is normal in winter; avoid loose substrate in juveniles",
                     "notes_ja": "MBD予防にUVBライトが不可欠。アデノウイルス（ADV）検査推奨。冬季のブルメーションは正常。幼体には粒子状床材を避ける"}},
        {"id": "lizard_crested_gecko", "name": "Crested Gecko", "name_ja": "クレステッドゲッコー",
         "risk": {"Metabolic Bone Disease": 1.5, "Tail Drop (Autotomy)": 1.3, "Tail Autotomy Infection": 1.3},
         "ecology": {"temperature": {"min": 20, "max": 27, "unit": "°C"},
                     "humidity": {"min": 60, "max": 80, "unit": "%"},
                     "lifespan": {"min": 15, "max": 20, "unit": "years"},
                     "weight": {"min": 35, "max": 55, "unit": "g"},
                     "diet": "Omnivore/frugivore; commercial crested gecko diet (CGD) as staple, supplemented with gut-loaded insects",
                     "diet_ja": "雑食性/果食性。市販のクレステッドゲッコーダイエット（CGD）を主食に、ガットローディングした昆虫で補助",
                     "housing": "Tall arboreal terrarium; misting 1-2 times daily for humidity; live or artificial plants; room temperature is often adequate",
                     "housing_ja": "背の高い樹上性テラリウム。湿度維持のため1日1〜2回の霧吹き。生体または人工植物。室温で飼育可能なことが多い",
                     "notes": "Tail does not regenerate once dropped — handle gently; no additional heating usually needed (room temp); simple care makes them great for beginners",
                     "notes_ja": "尾は一度落ちると再生しない。丁寧に扱う。追加の加温は通常不要（室温飼育可）。シンプルなケアで初心者に最適"}},
        {"id": "lizard_chameleon", "name": "Chameleon", "name_ja": "カメレオン",
         "risk": {"Metabolic Bone Disease": 2.5, "Dehydration": 2.0,
                  "Respiratory Infection": 1.8, "Egg Binding": 1.8},
         "ecology": {"temperature": {"min": 22, "max": 32, "unit": "°C"},
                     "humidity": {"min": 50, "max": 80, "unit": "%"},
                     "lifespan": {"min": 3, "max": 10, "unit": "years"},
                     "weight": {"min": 50, "max": 200, "unit": "g"},
                     "diet": "Insectivore; gut-loaded crickets, flies, silkworms; heavy calcium/D3 dusting; dripper or misting for water (will not drink from standing water)",
                     "diet_ja": "食虫性。ガットローディングしたコオロギ・ハエ・シルクワーム。カルシウム/D3の十分なダスティング。水はドリッパーまたは霧吹き（溜め水は飲まない）",
                     "housing": "Tall screen/mesh cage for ventilation; live plants; dripper system for hydration; UVB essential; basking spot with temperature gradient",
                     "housing_ja": "通気性の高い背の高いメッシュケージ。生きた植物。水分補給のドリッパーシステム。UVB必須。温度勾配のあるバスキングスポット",
                     "notes": "Very sensitive to husbandry errors — not for beginners; dehydration is the #1 killer; will not drink standing water — must have drip/mist system; MBD very common",
                     "notes_ja": "飼育ミスに非常に敏感で初心者向けではない。脱水が死因第1位。溜め水は飲まないためドリップ/ミストシステムが必須。MBDが非常に多い"}},
        {"id": "lizard_iguana", "name": "Green Iguana", "name_ja": "グリーンイグアナ",
         "risk": {"Metabolic Bone Disease": 2.0, "Kidney Disease": 1.8, "Renal Failure (Chronic Kidney Disease)": 1.8,
                  "Bladder Stones": 1.5},
         "ecology": {"temperature": {"min": 26, "max": 35, "unit": "°C"},
                     "humidity": {"min": 60, "max": 80, "unit": "%"},
                     "lifespan": {"min": 15, "max": 20, "unit": "years"},
                     "weight": {"min": 3, "max": 9, "unit": "kg"},
                     "diet": "Strict herbivore; dark leafy greens (collard, mustard, dandelion), squash, bell pepper; NO animal protein (causes kidney disease)",
                     "diet_ja": "厳格な草食性。濃い葉野菜（コラードグリーン、マスタードグリーン、タンポポ）、カボチャ、パプリカ。動物性タンパク質は厳禁（腎臓病の原因）",
                     "housing": "Very large enclosure or dedicated room (adults 1.5-2m); high humidity with misting; UVB essential; basking spot 35°C; climbing branches",
                     "housing_ja": "成体1.5〜2mのため非常に大きな飼育容器または専用部屋。霧吹きで高湿度維持。UVB必須。バスキングスポット35°C。登り枝",
                     "notes": "Grows very large — requires significant space commitment; animal protein causes fatal kidney disease; can become aggressive during breeding season; powerful tail whip",
                     "notes_ja": "非常に大きくなるため大きなスペースが必要。動物性タンパク質は致死的な腎臓病を引き起こす。繁殖期に攻撃的になることがある。尾の打撃は強力"}},
    ],
    "amphibian": [
        {"id": "amphibian_axolotl", "name": "Axolotl", "name_ja": "ウーパールーパー",
         "risk": {"Fungal Infection": 2.0, "Gill Damage": 1.8, "Gill Necrosis (Larval)": 1.8, "Impaction": 1.5,
                  "Ammonia Poisoning": 1.5},
         "ecology": {"temperature": {"min": 14, "max": 20, "unit": "°C"},
                     "humidity": {"min": 100, "max": 100, "unit": "%"},
                     "lifespan": {"min": 10, "max": 15, "unit": "years"},
                     "weight": {"min": 100, "max": 300, "unit": "g"},
                     "diet": "Carnivore; earthworms (primary), sinking pellets, frozen bloodworms; no live fish (parasite risk)",
                     "diet_ja": "肉食性。ミミズ（主食）、沈下性ペレット、冷凍アカムシ。生きた魚は寄生虫リスクがあり不可",
                     "housing": "Aquatic only; 75+ liter tank per axolotl; chilled water (14-20°C) with filter; fine sand or bare bottom (gravel causes impaction)",
                     "housing_ja": "完全水棲。1匹あたり75リットル以上の水槽。冷水（14〜20°C）でフィルター付き。細かい砂またはベアタンク（砂利は誤飲による閉塞の原因）",
                     "notes": "Neotenic (permanently larval) — never undergoes metamorphosis; very sensitive to water quality and temperature; above 22°C causes stress and disease; remarkable regeneration ability",
                     "notes_ja": "幼形成熟（永久幼生）で変態しない。水質と水温に非常に敏感。22°C以上はストレスと病気の原因。驚異的な再生能力を持つ"}},
        {"id": "amphibian_pacman_frog", "name": "Pacman Frog", "name_ja": "ベルツノガエル",
         "risk": {"Impaction": 2.0, "Obesity": 1.8, "Bacterial Dermatitis": 1.5},
         "ecology": {"temperature": {"min": 24, "max": 28, "unit": "°C"},
                     "humidity": {"min": 70, "max": 90, "unit": "%"},
                     "lifespan": {"min": 6, "max": 10, "unit": "years"},
                     "weight": {"min": 200, "max": 500, "unit": "g"},
                     "diet": "Carnivore; appropriately sized insects, earthworms, pinky mice (occasionally); calcium/D3 dusting; feed every 2-3 days (adults)",
                     "diet_ja": "肉食性。適切なサイズの昆虫、ミミズ、時々ピンクマウス。カルシウム/D3ダスティング。成体は2〜3日に1回",
                     "housing": "Small terrarium with moist coconut fiber substrate; shallow water dish; misting daily; minimal climbing as they are terrestrial ambush predators",
                     "housing_ja": "湿ったココナッツファイバー床材の小型テラリウム。浅い水入れ。毎日霧吹き。地上性の待ち伏せ型で登りは最小限",
                     "notes": "Voracious eater — prone to obesity; will attempt to eat anything that moves (including cage mates); impaction risk from substrate ingestion; sedentary lifestyle",
                     "notes_ja": "大食漢で肥満になりやすい。動くものは何でも食べようとする（同居個体含む）。床材誤飲による閉塞リスク。ほとんど動かない生活スタイル"}},
        {"id": "amphibian_tree_frog", "name": "Tree Frog", "name_ja": "アマガエル",
         "risk": {"Chytrid Fungus (Bd)": 2.0, "Chytridiomycosis (Bd)": 2.0, "Red Leg Syndrome": 1.8},
         "ecology": {"temperature": {"min": 20, "max": 26, "unit": "°C"},
                     "humidity": {"min": 60, "max": 85, "unit": "%"},
                     "lifespan": {"min": 5, "max": 15, "unit": "years"},
                     "weight": {"min": 2, "max": 30, "unit": "g"},
                     "diet": "Insectivore; small gut-loaded crickets, fruit flies (small species), springtails; calcium/D3 dusting",
                     "diet_ja": "食虫性。小さなガットローディング済みコオロギ、ショウジョウバエ（小型種）、トビムシ。カルシウム/D3ダスティング",
                     "housing": "Tall arboreal terrarium with live plants; misting 2-3 times daily; water dish changed daily; ventilation important to prevent stagnant air",
                     "housing_ja": "生きた植物を入れた背の高い樹上性テラリウム。1日2〜3回の霧吹き。水入れは毎日交換。空気のよどみ防止のため通気性が重要",
                     "notes": "Sensitive to water quality — use dechlorinated water only; chytridiomycosis is a major global threat; absorb toxins through skin — wash hands before handling; do not handle frequently",
                     "notes_ja": "水質に敏感。必ず塩素除去した水を使用。ツボカビ症は世界的な脅威。皮膚から毒素を吸収するため触る前に手洗い。頻繁なハンドリングは避ける"}},
    ],
    "sugar_glider": [
        {"id": "sugar_glider_standard", "name": "Standard Grey", "name_ja": "スタンダードグレー",
         "risk": {},
         "ecology": {"temperature": {"min": 22, "max": 28, "unit": "°C"},
                     "humidity": {"min": 40, "max": 70, "unit": "%"},
                     "lifespan": {"min": 10, "max": 15, "unit": "years"},
                     "weight": {"min": 90, "max": 150, "unit": "g"},
                     "diet": "Omnivore; balanced calcium:phosphorus diet essential (BML, HPW, or TPG diet); fresh fruits, vegetables, insects, nectar",
                     "diet_ja": "雑食性。カルシウム:リン比のバランスが重要（BML・HPW・TPG食）。新鮮な果物、野菜、昆虫、花蜜",
                     "housing": "Tall wire cage for gliding and climbing; bonding pouch for socialization; nocturnal — quiet during daytime",
                     "housing_ja": "滑空と登りのための背の高いワイヤーケージ。社会化のためのボンディングポーチ。夜行性のため昼間は静かに",
                     "notes": "Highly social — must be kept in pairs/groups or with extensive human bonding; calcium deficiency (MBD) is the #1 nutritional issue; self-mutilation if lonely/stressed",
                     "notes_ja": "非常に社会性が高くペア/グループ飼育または十分な人間との絆が必須。カルシウム欠乏（MBD）が栄養上の最大の問題。孤独・ストレスで自咬症"}},
        {"id": "sugar_glider_leucistic", "name": "Leucistic", "name_ja": "リューシスティック",
         "risk": {"Nutritional Secondary Hyperparathyroidism": 1.5, "Metabolic Bone Disease": 1.5},
         "ecology": {"temperature": {"min": 22, "max": 28, "unit": "°C"},
                     "humidity": {"min": 40, "max": 70, "unit": "%"},
                     "lifespan": {"min": 10, "max": 15, "unit": "years"},
                     "weight": {"min": 90, "max": 150, "unit": "g"},
                     "diet": "Omnivore; balanced calcium:phosphorus diet essential; extra calcium supplementation recommended due to higher MBD risk",
                     "diet_ja": "雑食性。カルシウム:リン比のバランスが重要。MBDリスクが高いため追加のカルシウム補給を推奨",
                     "housing": "Tall wire cage; bonding pouch; keep in pairs/groups; nocturnal",
                     "housing_ja": "背の高いワイヤーケージ。ボンディングポーチ。ペア/グループ飼育。夜行性",
                     "notes": "Higher risk of MBD and nutritional secondary hyperparathyroidism — strict calcium:phosphorus ratio monitoring; limited gene pool may cause other health issues",
                     "notes_ja": "MBDと栄養性二次性上皮小体機能亢進症のリスクが高い。厳格なカルシウム:リン比の管理。限られた遺伝子プールによる健康問題の可能性"}},
        {"id": "sugar_glider_white_faced_blonde", "name": "White Faced Blonde", "name_ja": "ホワイトフェイスブロンド",
         "risk": {"Self-Mutilation": 1.3, "Stress-Related Disorders": 1.3},
         "ecology": {"temperature": {"min": 22, "max": 28, "unit": "°C"},
                     "humidity": {"min": 40, "max": 70, "unit": "%"},
                     "lifespan": {"min": 10, "max": 15, "unit": "years"},
                     "weight": {"min": 90, "max": 150, "unit": "g"},
                     "diet": "Omnivore; balanced calcium:phosphorus diet essential; fresh fruits, vegetables, insects, nectar",
                     "diet_ja": "雑食性。カルシウム:リン比のバランスが重要。新鮮な果物、野菜、昆虫、花蜜",
                     "housing": "Tall wire cage; bonding pouch; must be kept with companions — especially prone to stress-related issues when isolated",
                     "housing_ja": "背の高いワイヤーケージ。ボンディングポーチ。仲間との飼育が必須。孤立時のストレス関連問題に特に注意",
                     "notes": "More prone to self-mutilation and stress disorders — ensure social enrichment; same basic care as standard sugar gliders",
                     "notes_ja": "自咬症とストレス障害になりやすい。社会的エンリッチメントを確保。基本的なケアはスタンダードと同様"}},
    ],
    "degu": [
        {"id": "degu_standard", "name": "Standard (Agouti)", "name_ja": "スタンダード（アグーチ）",
         "risk": {"Diabetes Mellitus": 2.5, "Cataracts": 2.0, "Dental Disease": 2.0, "Dental Malocclusion": 2.0},
         "ecology": {"temperature": {"min": 18, "max": 24, "unit": "°C"},
                     "humidity": {"min": 40, "max": 60, "unit": "%"},
                     "lifespan": {"min": 6, "max": 9, "unit": "years"},
                     "weight": {"min": 170, "max": 300, "unit": "g"},
                     "diet": "Herbivore; timothy hay, degu-specific pellets, fresh vegetables; strictly NO sugar or fruit (extreme diabetes risk)",
                     "diet_ja": "草食性。チモシー牧草、デグー専用ペレット、新鮮な野菜。糖分と果物は厳禁（極めて高い糖尿病リスク）",
                     "housing": "Large multi-level cage with solid floors; dust bath (like chinchillas); social — must keep in groups of 2+; exercise wheel",
                     "housing_ja": "ソリッドフロアの大型多段式ケージ。砂浴び（チンチラと同様）。社会性が高く2匹以上のグループ飼育が必須。回し車",
                     "notes": "Cannot metabolize sugar — diabetes and cataracts are extremely common; never feed fruit, honey, or sugar; diurnal (unlike most rodents); tail degloving if grabbed by tail",
                     "notes_ja": "糖を代謝できない。糖尿病と白内障が極めて多い。果物・蜂蜜・砂糖は絶対不可。昼行性（他の齧歯類と異なる）。尾を掴むとテイルスリップ（尾の皮膚剥離）"}},
        {"id": "degu_blue", "name": "Blue", "name_ja": "ブルー",
         "risk": {"Diabetes Mellitus": 2.5, "Cataracts": 2.0, "Dental Disease": 2.0, "Dental Malocclusion": 2.0},
         "ecology": {"temperature": {"min": 18, "max": 24, "unit": "°C"},
                     "humidity": {"min": 40, "max": 60, "unit": "%"},
                     "lifespan": {"min": 6, "max": 9, "unit": "years"},
                     "weight": {"min": 170, "max": 300, "unit": "g"},
                     "diet": "Herbivore; timothy hay, degu-specific pellets, fresh vegetables; strictly NO sugar or fruit",
                     "diet_ja": "草食性。チモシー牧草、デグー専用ペレット、新鮮な野菜。糖分と果物は厳禁",
                     "housing": "Large multi-level cage; dust bath; social — must keep in groups of 2+; exercise wheel",
                     "housing_ja": "大型多段式ケージ。砂浴び。2匹以上のグループ飼育が必須。回し車",
                     "notes": "Same care as standard degus; blue color mutation from limited gene pool — monitor for additional health issues; dental disease common",
                     "notes_ja": "ケアはスタンダードと同様。ブルーカラーは限られた遺伝子プールからの変異。追加の健康問題に注意。歯科疾患が多い"}},
        {"id": "degu_pied", "name": "Pied", "name_ja": "パイド",
         "risk": {"Diabetes Mellitus": 2.5, "Cataracts": 2.0},
         "ecology": {"temperature": {"min": 18, "max": 24, "unit": "°C"},
                     "humidity": {"min": 40, "max": 60, "unit": "%"},
                     "lifespan": {"min": 6, "max": 9, "unit": "years"},
                     "weight": {"min": 170, "max": 300, "unit": "g"},
                     "diet": "Herbivore; timothy hay, degu-specific pellets, fresh vegetables; strictly NO sugar or fruit",
                     "diet_ja": "草食性。チモシー牧草、デグー専用ペレット、新鮮な野菜。糖分と果物は厳禁",
                     "housing": "Large multi-level cage; dust bath; social — must keep in groups of 2+; exercise wheel",
                     "housing_ja": "大型多段式ケージ。砂浴び。2匹以上のグループ飼育が必須。回し車",
                     "notes": "Same care as standard degus; pied pattern from limited breeding — same diabetes and cataract risks",
                     "notes_ja": "ケアはスタンダードと同様。パイド模様は限られた繁殖から。糖尿病と白内障のリスクは同じ"}},
    ],
    "exotic_other": [
        {"id": "exotic_other_general", "name": "Other Exotic", "name_ja": "その他のエキゾチック",
         "risk": {},
         "ecology": {"temperature": {"min": 18, "max": 28, "unit": "°C"},
                     "humidity": {"min": 40, "max": 70, "unit": "%"},
                     "lifespan": {"min": 5, "max": 20, "unit": "years"},
                     "weight": {"min": 50, "max": 5000, "unit": "g"},
                     "diet": "Varies by species; consult species-specific veterinary resources",
                     "diet_ja": "種によって異なる。種ごとの獣医学資料を参照",
                     "housing": "Species-specific enclosure with appropriate environmental conditions",
                     "housing_ja": "適切な環境条件を備えた種に応じた飼育容器",
                     "notes": "Consult an exotic animal veterinarian for species-specific care guidelines; many exotic species have specialized needs",
                     "notes_ja": "種ごとのケアガイドラインについてはエキゾチック動物専門の獣医師に相談。多くのエキゾチック種には専門的なケアが必要"}},
    ],
}


# =============================================================================
# SYMPTOM PAIR BOOST DICTIONARY
# =============================================================================
# When two specific symptoms co-occur, boost particular diseases.
# Format: {frozenset({symptom1, symptom2}): {disease_name: multiplier}}
# These represent clinically significant symptom combinations that strongly
# suggest specific diagnoses.

SYMPTOM_PAIR_BOOST: Dict[frozenset, Dict[str, float]] = {
    # 嘔吐 + 腹部膨満 → GDV (犬は bloated_abdomen, 他種は bloating)
    frozenset({"vomiting", "bloating"}): {
        "Gastric Dilatation-Volvulus (GDV/Bloat)": 2.0,
        "Intestinal Obstruction": 1.5,
        "Gastrointestinal Stasis": 1.5, "GI Stasis": 1.5,
    },
    frozenset({"vomiting", "bloated_abdomen"}): {
        "Gastric Dilatation-Volvulus (GDV/Bloat)": 2.0,
        "Intestinal Obstruction": 1.5,
        "Gastrointestinal Stasis": 1.5, "GI Stasis": 1.5,
    },
    # 多飲 + 頻尿 → 腎臓病・糖尿 (犬は excessive_urination, 他種は frequent_urination)
    frozenset({"excessive_thirst", "frequent_urination"}): {
        "Kidney Disease (CKD)": 2.0,
        "Feline Chronic Kidney Disease (CKD)": 2.0,
        "Diabetes Mellitus": 2.0,
        "Cushing's Disease": 1.5,
        "Hyperthyroidism": 1.5,
        "Pyometra": 1.5,
    },
    frozenset({"excessive_thirst", "excessive_urination"}): {
        "Kidney Disease (CKD)": 2.0,
        "Diabetes Mellitus": 2.0,
        "Cushing's Disease": 1.5,
        "Hyperthyroidism": 1.5,
        "Pyometra": 1.5,
    },
    # 咳 + 呼吸困難 → 心不全・肺炎 (犬は difficulty_breathing, 他種は labored_breathing)
    frozenset({"coughing", "labored_breathing"}): {
        "Heart Disease/CHF": 1.8, "Congestive Heart Failure": 1.8,
        "Feline Hypertrophic Cardiomyopathy (HCM)": 1.8,
        "Pneumonia": 1.8,
        "Feline Pneumonia": 1.8,
        "Pleural Effusion": 1.5,
        "Feline Asthma": 1.5,
    },
    frozenset({"coughing", "difficulty_breathing"}): {
        "Heart Disease/CHF": 1.8, "Congestive Heart Failure": 1.8,
        "Pneumonia": 1.8,
        "Pleural Effusion": 1.5,
    },
    # 嘔吐 + 血便 → パルボ・出血性胃腸炎 (犬は bloody_stool, 他種は blood_in_stool)
    frozenset({"vomiting", "blood_in_stool"}): {
        "Parvovirus Infection": 2.0,
        "Canine Parvovirus": 2.0,
        "Hemorrhagic Gastroenteritis (HGE)": 2.0,
        "Feline Panleukopenia": 2.0,
        "Feline Panleukopenia (Feline Distemper)": 2.0,
        "Intestinal Parasites": 1.5,
        "Inflammatory Bowel Disease (IBD)": 1.5,
    },
    frozenset({"vomiting", "bloody_stool"}): {
        "Canine Parvovirus": 2.0,
        "Hemorrhagic Gastroenteritis (HGE)": 2.0,
        "Intestinal Parasites": 1.5,
        "Inflammatory Bowel Disease (IBD)": 1.5,
    },
    # けいれん + よだれ → 中毒・てんかん (犬は drooling, 他種は excessive_drooling)
    frozenset({"seizures", "excessive_drooling"}): {
        "Poisoning/Toxicity": 2.0,
        "Epilepsy": 1.8,
        "Organophosphate Toxicity": 2.0,
        "Organophosphate Toxicosis": 2.0,
        "Rabies": 1.5,
    },
    frozenset({"seizures", "drooling"}): {
        "Poisoning/Toxicity": 2.0,
        "Epilepsy": 1.8,
        "Rabies": 1.5,
    },
    # 黄疸 + 食欲不振 → 肝臓病 (犬は appetite_loss, 他種は loss_of_appetite もあり)
    frozenset({"jaundice", "loss_of_appetite"}): {
        "Liver Disease": 2.0,
        "Feline Hepatic Lipidosis": 2.5,
        "Leptospirosis": 1.8,
        "Immune-Mediated Hemolytic Anemia": 1.8,
        "Cholangitis": 1.8,
    },
    frozenset({"jaundice", "appetite_loss"}): {
        "Liver Disease": 2.0,
        "Leptospirosis": 1.8,
        "Immune-Mediated Hemolytic Anemia": 1.8,
    },
    # 体重減少 + 食欲不振 → がん・CKD
    frozenset({"weight_loss", "loss_of_appetite"}): {
        "Cancer/Neoplasia": 1.8,
        "Kidney Disease (CKD)": 1.5,
        "Feline Chronic Kidney Disease (CKD)": 1.5,
        "Hyperthyroidism": 1.5,
        "Inflammatory Bowel Disease (IBD)": 1.5,
        "Feline Infectious Peritonitis (FIP)": 1.5,
    },
    frozenset({"weight_loss", "appetite_loss"}): {
        "Cancer/Neoplasia": 1.8,
        "Kidney Disease (CKD)": 1.5,
        "Hyperthyroidism": 1.5,
        "Inflammatory Bowel Disease (IBD)": 1.5,
    },
    # 血尿 + 排尿困難 → 尿路結石・FLUTD (犬は blood_urine/straining_urinate)
    frozenset({"blood_in_urine", "straining_to_urinate"}): {
        "Bladder Stones": 2.0,
        "Feline Lower Urinary Tract Disease (FLUTD)": 2.5,
        "Urinary Tract Infection": 1.8,
        "Urethral Obstruction": 2.0,
    },
    frozenset({"bloody_urine", "straining_to_urinate"}): {
        "Bladder Stones": 2.0,
        "Feline Lower Urinary Tract Disease (FLUTD)": 2.5,
        "Urinary Tract Infection": 1.8,
        "Urethral Obstruction": 2.0,
    },
    frozenset({"blood_urine", "straining_urinate"}): {
        "Bladder Stones": 2.0,
        "Urinary Tract Infection": 1.8,
    },
    # 失神 + 運動不耐性 → 心臓病
    frozenset({"fainting", "exercise_intolerance"}): {
        "Heart Disease/CHF": 2.5, "Congestive Heart Failure": 2.5,
        "Feline Hypertrophic Cardiomyopathy (HCM)": 2.0,
        "Aortic Stenosis": 2.0,
        "Pulmonic Stenosis": 1.8,
        "Cardiac Arrhythmia": 2.0,
        "Arrhythmia": 2.0,
    },
    # 失神/虚脱 + 呼吸困難 → 心臓病 (犬用: collapse + difficulty_breathing)
    frozenset({"collapse", "difficulty_breathing"}): {
        "Heart Disease/CHF": 2.0, "Congestive Heart Failure": 2.0,
        "Pneumothorax": 2.0,
        "Pericardial Effusion": 1.8,
    },
    # 発熱 + リンパ節腫脹 → 感染症・リンパ腫
    frozenset({"fever", "swollen_lymph_nodes"}): {
        "Lymphoma": 2.0,
        "Tick-borne Disease": 1.8,
        "Feline Leukemia Virus (FeLV)": 1.8,
        "Feline Immunodeficiency Virus (FIV)": 1.5,
        "Ehrlichiosis": 1.8,
    },
    frozenset({"fever", "swelling"}): {
        "Lymphoma": 1.5,
        "Abscess": 1.5,
    },
    # 下痢 + 嘔吐 → 急性胃腸炎・中毒
    frozenset({"diarrhea", "vomiting"}): {
        "Acute Gastroenteritis": 1.8,
        "Gastroenteritis": 1.8,
        "Pancreatitis": 1.8,
        "Poisoning/Toxicity": 1.5,
        "Foreign Body Ingestion": 1.5,
        "Foreign Body Obstruction": 1.5,
        "Feline Panleukopenia": 1.5,
        "Parvovirus Infection": 1.5,
        "Canine Parvovirus": 1.5,
    },
    # 蒼白 + 無気力 → 貧血
    frozenset({"pale_gums", "lethargy"}): {
        "Immune-Mediated Hemolytic Anemia": 2.0,
        "Internal Hemorrhage": 2.0,
        "Tick-borne Disease": 1.8,
        "Feline Infectious Anemia (Hemobartonellosis)": 2.0,
        "Rodenticide Poisoning": 1.8,
    },
    # 咳 + 運動不耐性 → 心臓病・気管虚脱
    frozenset({"coughing", "exercise_intolerance"}): {
        "Heart Disease/CHF": 2.0, "Congestive Heart Failure": 2.0,
        "Tracheal Collapse": 2.0,
        "Heartworm Disease": 1.8,
    },
    # 目の白濁 + 目の充血 → 緑内障 (犬は eye_redness)
    frozenset({"cloudiness_in_eyes", "redness_in_eyes"}): {
        "Glaucoma": 2.5,
        "Uveitis": 2.0,
        "Corneal Ulcer": 1.5,
    },
    frozenset({"squinting", "eye_redness"}): {
        "Glaucoma": 2.0,
        "Uveitis": 2.0,
        "Corneal Ulcer": 1.5,
    },
    # 跛行 + 関節痛 → 関節疾患 (犬は swollen_joints + limping_*)
    frozenset({"lameness_or_limping", "joint_pain_or_stiffness"}): {
        "Osteoarthritis": 2.0,
        "Hip Dysplasia": 1.8,
        "Cruciate Ligament Injury": 1.8,
        "Lyme Disease": 1.5,
        "Immune-Mediated Polyarthritis": 1.8,
    },
    frozenset({"swollen_joints", "stiffness"}): {
        "Osteoarthritis": 2.0,
        "Immune-Mediated Polyarthritis": 1.8,
        "Lyme Disease": 1.5,
    },
}


# =============================================================================
# CSU CANINE ACUTE PAIN SCALE (Colorado State University)
# Reference: dourinken.com/wp-content/uploads/2019/04/pain_scale.pdf
# Score 0-4, used as urgency/disease modifier for dog symptom analysis
# =============================================================================

CANINE_PAIN_SCALE: Dict[int, Dict[str, Any]] = {
    0: {
        "level_en": "Comfortable / No Pain",
        "level_ja": "快適 / 痛みなし",
        "description_en": "Not bothered by palpation of wound or surgery site. Comfortable and interested in surroundings.",
        "description_ja": "創部や手術部位の触診に反応しない。快適で周囲に興味を示す。",
        "behavioral_signs_ja": "満足、快適に睡眠・休息、尾を振る、食事に興味を示す",
        "body_tension_ja": "リラックスした体勢、筋緊張は最小限",
        "urgency_modifier": 1.0,
    },
    1: {
        "level_en": "Mild Pain",
        "level_ja": "軽度の痛み",
        "description_en": "Content to slightly unsettled. May look at wound site. Responds to palpation with mild reaction.",
        "description_ja": "ほぼ快適だがやや落ち着かない。創部を気にする。触診にわずかに反応。",
        "behavioral_signs_ja": "やや落ち着きがない、リップリッキング・あくび、体重移動、患部を見る",
        "body_tension_ja": "やや緊張した体勢、軽度の防御姿勢",
        "urgency_modifier": 1.05,
    },
    2: {
        "level_en": "Moderate Pain",
        "level_ja": "中等度の痛み",
        "description_en": "Arises from rest or shifts body position. Flinches on palpation. May whimper occasionally.",
        "description_ja": "休息から起き上がる・体位変換。触診で逃避反応。時折うめき声。",
        "behavioral_signs_ja": "体位変換、患部の防御、断続的なうめき声、動きたがらない、食欲低下",
        "body_tension_ja": "中程度の筋緊張、患部の防御",
        "urgency_modifier": 1.15,
    },
    3: {
        "level_en": "Moderate to Severe Pain",
        "level_ja": "中等度〜重度の痛み",
        "description_en": "Unsettled, cries when touched. Reluctant to move, may not eat. Guards wound.",
        "description_ja": "不安定、触ると鳴き声。動きたがらない、食べない。創部を防御。",
        "behavioral_signs_ja": "落ち着きなし、鳴き声、動きたがらない、触ると攻撃的、食欲なし、震え、猫背姿勢",
        "body_tension_ja": "体の緊張、固定、触診で硬直",
        "urgency_modifier": 1.3,
    },
    4: {
        "level_en": "Severe Pain",
        "level_ja": "重度の痛み",
        "description_en": "Prostrate. Constantly groaning or screaming. May bite. Unresponsive. Extremely rigid.",
        "description_ja": "横臥。持続的なうなり声・叫び声。咬みつき。周囲に無反応。極度に硬直。",
        "behavioral_signs_ja": "横臥、持続的な発声、咬みつき、周囲への無反応、硬直、循環器系への影響",
        "body_tension_ja": "極度の緊張・硬直、外的刺激に無反応",
        "urgency_modifier": 1.5,
    },
}

# Pain-associated disease boost mapping
PAIN_LEVEL_DISEASE_BOOST: Dict[int, Dict[str, float]] = {
    2: {
        "Osteoarthritis": 1.3, "Intervertebral Disc Disease": 1.2,
        "Pancreatitis": 1.3, "Gastric Ulcer": 1.2,
        "Urinary Tract Infection": 1.2, "Otitis Media": 1.2,
    },
    3: {
        "Pancreatitis": 1.5, "Intervertebral Disc Disease": 1.5,
        "Fracture": 1.4, "Peritonitis": 1.5, "Pyelonephritis": 1.3,
        "Urolithiasis": 1.4, "Foreign Body Obstruction": 1.4,
        "Immune-Mediated Polyarthritis": 1.3, "Meningitis": 1.4,
        "Osteosarcoma": 1.3, "Acute Abdomen": 1.5,
    },
    4: {
        "Gastric Dilatation-Volvulus (GDV)": 1.8, "Pancreatitis": 1.6,
        "Peritonitis": 1.8, "Meningitis": 1.6,
        "Intervertebral Disc Disease": 1.6, "Fracture": 1.6,
        "Urethral Obstruction": 1.6, "Spinal Fracture": 1.7,
        "Acute Abdomen": 1.8, "Aortic Thromboembolism": 1.7,
    },
}


# =============================================================================
# SYMPTOM CLINICAL WEIGHTS (尤度比ベース臨床的重み付け)
# =============================================================================
# 各症状の臨床的重要度を重み付け。文献ベースの尤度比 (Likelihood Ratio) を
# 簡易的に反映し、非特異的な症状 (1.0) から病態特異的な症状 (2.0–3.0) まで
# スケーリングする。
#
# 参考文献:
#   [23] Rijnberk & van Sluijs (2009) Medical History and Physical Examination
#        in Companion Animals, 2nd ed. Elsevier. — Ch.2: 臨床的尤度比の概念
#   [2]  Ettinger, Feldman & Cote (2017) Textbook of Veterinary Internal
#        Medicine, 8th ed. Elsevier. — Ch.1–5: 症状別鑑別診断アプローチ
#   [26] Côté (2014) Clinical Veterinary Advisor, 3rd ed. Elsevier.
#        — 症状→疾患マッピングの臨床的重み
#   [29] Platt & Olby (2013) Manual of Canine and Feline Neurology, 4th ed.
#        BSAVA. — 神経症状の特異度 (seizures LR+ 5.2, head_tilt LR+ 3.8)
#   [28] Feldman et al. (2015) Canine and Feline Endocrinology, 4th ed.
#        Elsevier. — 内分泌症状の尤度比 (PU/PD LR+ 2.1, acetone_breath LR+ 8.5)
#   [27] Polzin (2011) Chronic kidney disease. Vet Clin North Am Small Anim
#        41(1):15–30. — 腎疾患症状の感度・特異度
#
# 重み決定の方法論:
#   1. 各症状の陽性尤度比 (LR+) を上記文献から収集
#   2. LR+ 1–2 → 重み 1.0 (非特異的), LR+ 2–4 → 1.2–1.5 (やや特異的),
#      LR+ 4–8 → 1.8–2.0 (高度特異的), LR+ >8 → 2.5 (病態特異的)
#   3. LR+ が文献に記載されていない症状は臨床的コンセンサスで分類
#
# カテゴリ:
#   1.0  = 非特異的 (lethargy, appetite_loss など多くの疾患で出現)
#   1.2  = やや特異的 (fever, vomiting など)
#   1.5  = 中程度に特異的 (jaundice, blood_in_urine など)
#   2.0  = 高度に特異的 / 重篤 (seizures, collapse, hind_limb_paralysis)
#   2.5–3.0 = 病態特異的 / ほぼ確定的 (特定疾患に直結する所見)

SYMPTOM_CLINICAL_WEIGHTS: Dict[str, float] = {
    # --- 全身症状 (非特異的) --- [2] Ettinger Ch.1: LR+ <2 for all
    "lethargy": 1.0,
    "decreased_activity": 1.0,
    "weakness": 1.0,
    "appetite_loss": 1.0,
    "loss_of_appetite": 1.0,
    "weight_loss": 1.0,
    "weight_gain": 1.0,
    "dehydration": 1.1,            # [23] Rijnberk: skin turgor LR+ 1.8
    "poor_coat": 1.0,
    "hiding": 1.0,
    "behavioral_changes": 1.0,
    "aggression": 1.0,
    "aggression_change": 1.0,
    "anxiety": 1.0,

    # --- 発熱 --- [2] Ettinger Ch.3: fever LR+ 2.4 (infection)
    "fever": 1.2,
    "hyperthermia": 1.3,            # [2] higher specificity for heat stroke
    "hypothermia": 1.5,             # [2] LR+ 3.5 (shock, sepsis)

    # --- 消化器 (やや特異的) --- [2] Ettinger Ch.127–135
    "vomiting": 1.2,                # [26] Côté: LR+ 2.1 (GI disease)
    "diarrhea": 1.2,
    "regurgitation": 1.5,           # [2] LR+ 3.8 (megaesophagus)
    "constipation": 1.2,
    "bloating": 1.5,                # [25] Glickman: LR+ 3.2 (GDV)
    "bloated_abdomen": 1.5,
    "abdominal_pain": 1.3,
    "abdominal_distension": 1.5,
    "abdominal_contractions": 1.5,
    "excessive_gas": 1.1,
    "bloody_stool": 1.8,            # [2] LR+ 4.1 (hemorrhagic GI)
    "blood_in_stool": 1.8,
    "drooling": 1.2,
    "excessive_drooling": 1.2,
    "vomiting_after_drinking": 1.5,
    "straining_to_defecate": 1.3,
    "reduced_fecal_output": 1.3,
    "fecal_incontinence": 1.5,
    "eating_non_food": 1.3,

    # --- 呼吸器 --- [2] Ettinger Ch.42–47
    "coughing": 1.2,
    "sneezing": 1.1,
    "nasal_discharge": 1.2,
    "difficulty_breathing": 1.8,    # [23] Rijnberk: LR+ 4.2 (lower airway)
    "labored_breathing": 1.8,
    "rapid_breathing": 1.5,
    "open_mouth_breathing": 1.8,    # [8] Little: LR+ 4.5 in cats (emergency)
    "noisy_breathing": 1.3,
    "reverse_sneezing": 1.2,
    "snoring": 1.0,
    "wheezing": 1.5,
    "cyanosis": 2.5,                # [2] LR+ >10 (severe hypoxia)

    # --- 循環器 (高度に特異的) --- [2] Ettinger Ch.176–195
    "heart_murmur": 2.0,            # [2] LR+ 5.5 (structural heart disease)
    "irregular_heartbeat": 2.0,     # [2] LR+ 5.0 (arrhythmia)
    "muffled_heart_sounds": 2.0,    # [2] LR+ 6.2 (pericardial effusion)
    "exercise_intolerance": 1.5,
    "fainting": 2.0,                # [2] LR+ 5.8 (cardiac syncope)
    "collapse": 2.0,
    "pale_gums": 1.8,               # [23] Rijnberk: LR+ 4.0 (anemia/shock)
    "cold_extremities": 1.5,
    "excessive_panting": 1.2,

    # --- 泌尿器 --- [27] Polzin (2011); [2] Ettinger Ch.312–325
    "excessive_thirst": 1.3,        # [28] Feldman: PU/PD LR+ 2.1
    "excessive_urination": 1.3,
    "frequent_urination": 1.3,
    "straining_urinate": 1.5,       # [2] LR+ 3.5 (FLUTD/obstruction)
    "straining_to_urinate": 1.5,
    "blood_urine": 1.8,             # [2] LR+ 4.3 (urinary tract disease)
    "bloody_urine": 1.8,
    "blood_in_urine": 1.8,
    "incontinence": 1.3,
    "urinary_incontinence": 1.3,
    "decreased_urination": 1.5,     # [27] Polzin: LR+ 3.8 (AKI/obstruction)
    "inappropriate_urination": 1.2,
    "dark_urine": 1.5,

    # --- 神経 (高度に特異的) --- [29] Platt & Olby (2013)
    "seizures": 2.5,                # [29] LR+ 5.2 (intracranial disease)
    "tremors": 2.0,                 # [29] LR+ 4.8
    "ataxia": 2.0,                  # [29] LR+ 5.0 (cerebellar/vestibular)
    "circling": 1.8,                # [29] LR+ 3.8
    "head_tilting": 1.8,            # [29] LR+ 3.8 (vestibular disease)
    "head_tilt": 1.8,
    "head_pressing": 2.5,           # [29] LR+ 8.0 (hepatic encephalopathy)
    "nystagmus": 2.0,               # [29] LR+ 5.5 (vestibular)
    "disorientation": 1.5,
    "paralysis": 2.5,               # [29] LR+ 7.5
    "hind_limb_paralysis": 2.5,     # [29] LR+ 7.5 (IVDD, ATE)
    "muscle_spasms": 1.8,
    "muscle_weakness": 1.5,
    "decreased_reflexes": 2.0,      # [29] LR+ 4.8 (LMN lesion)
    "falling": 1.8,

    # --- 運動器 --- [30] Tobias & Johnston (2012) Veterinary Surgery
    "limping_fl": 1.3,
    "limping_fr": 1.3,
    "limping_rl": 1.3,
    "limping_rr": 1.3,
    "lameness": 1.3,
    "lameness_or_limping": 1.3,
    "stiffness": 1.2,
    "reluctance_move": 1.3,
    "reluctance_to_jump": 1.3,
    "swollen_joints": 1.5,
    "joint_pain_or_stiffness": 1.3,
    "non_weight_bearing": 1.8,
    "pain_on_touch": 1.3,
    "pain": 1.2,
    "skipping_gait": 1.5,
    "plantigrade_stance": 2.0,

    # --- 皮膚 --- [2] Ettinger Ch.29–33; [26] Côté
    "itching": 1.1,
    "hair_loss": 1.2,
    "skin_redness": 1.1,
    "skin_lesions": 1.2,
    "lumps": 1.5,
    "subcutaneous_mass": 1.5,
    "dry_skin": 1.0,
    "hot_spots": 1.2,
    "crusting": 1.2,
    "scaling": 1.2,
    "visible_parasites": 1.8,
    "self_mutilation": 1.5,
    "skin_fragility": 2.0,
    "skin_twitching": 1.3,
    "non_healing_wound": 1.5,
    "draining_wound": 1.5,
    "miliary_dermatitis": 1.5,
    "nail_abnormalities": 1.3,
    "ulcerated_mass": 1.8,

    # --- 眼科 --- [26] Côté; [2] Ettinger Ch.261–270
    "eye_redness": 1.2,
    "redness_in_eyes": 1.2,
    "eye_discharge": 1.1,
    "squinting": 1.2,
    "eye_pain": 1.5,
    "conjunctivitis": 1.3,
    "corneal_cloudiness": 1.5,
    "cloudiness_in_eyes": 1.5,
    "corneal_ulcer": 1.8,
    "excessive_tearing": 1.1,
    "blindness": 2.0,
    "dilated_pupils": 1.8,
    "iris_color_change": 1.8,
    "third_eyelid_protrusion": 1.5,
    "enlarged_eye": 1.8,
    "eye_changes": 1.2,

    # --- 耳 ---
    "ear_scratching": 1.1,
    "scratching_ears": 1.1,
    "ear_odor": 1.2,
    "ear_discharge": 1.3,
    "ear_inflammation": 1.3,
    "head_shaking": 1.2,
    "ear_tip_lesions": 1.5,

    # --- 口腔 --- [26] Côté
    "bad_breath": 1.2,
    "acetone_breath": 2.5,          # [28] Feldman: LR+ 8.5 (DKA)
    "oral_ulcers": 1.8,
    "oral_masses": 1.8,
    "stomatitis": 1.5,
    "difficulty_eating": 1.3,
    "difficulty_swallowing": 1.5,
    "tooth_loss": 1.5,
    "jaw_chattering": 1.5,
    "bleeding_gums": 1.5,
    "chin_swelling": 1.3,
    "lip_swelling": 1.3,

    # --- 血液・リンパ --- [2] Ettinger Ch.94–99
    "jaundice": 2.5,                # [2] LR+ >10 (hepatobiliary/hemolysis)
    "petechiae": 2.0,               # [2] LR+ 6.0 (thrombocytopenia)
    "bleeding": 1.8,
    "lymph_node_enlargement": 1.8,
    "swollen_lymph_nodes": 1.8,
    "recurrent_infections": 1.5,
    "immunosuppression": 2.0,

    # --- 生殖器 --- [1] Nelson & Couto Ch.57–62
    "genital_discharge": 1.5,
    "vaginal_discharge": 1.5,
    "bloody_discharge": 1.8,
    "mammary_masses": 2.0,
    "swollen_testicle": 1.8,
    "prolonged_labor": 2.0,
    "visible_tissue_protrusion": 2.0,

    # --- 食欲・代謝 --- [28] Feldman (2015) Endocrinology
    "appetite_increase": 1.2,
    "increased_appetite": 1.2,
    "muscle_wasting": 1.5,

    # --- 鳥類・爬虫類特異的 --- [6] Ritchie (1994); [34] Divers & Stahl (2019)
    "feather_loss": 1.3,
    "abnormal_feathers": 1.5,
    "beak_deformity": 2.0,
    "tail_bob": 1.5,
    "fluffed_feathers": 1.0,
    "shell_abnormalities": 1.5,
    "dysecdysis": 1.5,

    # --- その他 ---
    "swelling": 1.3,
    "facial_swelling": 1.5,
    "paw_swelling": 1.3,
    "deformity": 1.8,
    "stunted_growth": 1.5,
    "hunched_posture": 1.3,
    "teeth_grinding": 1.3,
    "vocalization_changes": 1.2,
    "voice_change": 1.3,
    "hyperactivity": 1.0,
    "night_waking": 1.0,
    "scooting": 1.3,
    "itching_around_anus": 1.3,
    "tail_chasing": 1.0,
    "wool_sucking": 1.0,
    "visible_worms": 2.0,
    "ventroflexion_of_neck": 2.0,
    "short_thick_tail": 2.0,
    "prognathia": 1.5,
}

# デフォルト重み（辞書に登録されていない症状用）
_DEFAULT_SYMPTOM_WEIGHT = 1.0

# Prevalence multiplier for Bayesian-like prior adjustment
_PREVALENCE_MULTIPLIER: Dict[str, float] = {
    "very_common": 1.35,
    "common": 1.125,
    "uncommon": 0.875,
    "rare": 0.70,
}


# =============================================================================
# LAB VALUE → DISEASE BOOST MAP (検査値異常による疾患スコアブースト)
# =============================================================================
# 血液検査値の異常パターンから疾患へのブーストマッピング。
# キー: (検査項目, 方向) タプル。方向は "high" (基準値超) or "low" (基準値未満)。
# 値: {疾患名: ブースト倍率} の辞書。
#
# 参考文献:
#   [2]  Ettinger & Feldman (2017) — Ch.291–310: Laboratory diagnosis
#   [1]  Nelson & Couto (2019) — Ch.110–117: Clinical pathology
#   [26] Côté (2014) — Lab-based differential diagnosis tables
#   [28] Feldman et al. (2015) — Endocrine lab interpretation
#   [27] Polzin (2011) — Renal biomarkers (BUN, creatinine, SDMA)
#
# ブースト倍率の設定根拠:
#   1.3 = やや関連 (多くの疾患で上昇しうる非特異的マーカー)
#   1.5 = 中程度に関連 (2–3 疾患群に絞り込み可能)
#   1.8 = 強く関連 (疾患群をかなり限定)
#   2.0 = 高度に特異的 (ほぼ確定診断に近い)

LAB_ABNORMALITY_DISEASE_MAP: Dict[tuple, Dict[str, float]] = {
    # --- 腎機能 --- [27] Polzin (2011)
    ("bun", "high"): {
        "Chronic Kidney Disease (CKD)": 1.8,
        "Acute Kidney Injury": 2.0, "Acute Renal Failure": 2.0,
        "Urinary Obstruction": 1.5,
        "Urethral Obstruction": 1.5,
        "Dehydration": 1.3,
        "Addison's Disease (Hypoadrenocorticism)": 1.3,
        "Leptospirosis": 1.5,
    },
    ("creatinine", "high"): {
        "Chronic Kidney Disease (CKD)": 2.0,
        "Acute Kidney Injury": 2.0, "Acute Renal Failure": 2.0,
        "Urinary Obstruction": 1.8,
        "Urethral Obstruction": 1.8,
        "Leptospirosis": 1.5,
    },
    ("sdma", "high"): {
        "Chronic Kidney Disease (CKD)": 2.0,  # [27] SDMA rises before Cre
        "Acute Kidney Injury": 1.8, "Acute Renal Failure": 1.8,
    },

    # --- 肝機能 --- [2] Ettinger Ch.296–300
    ("alt", "high"): {
        "Hepatitis": 1.8,
        "Cholangiohepatitis": 1.8,
        "Hepatic Lipidosis": 1.8,
        "Portosystemic Shunt": 1.5,
        "Liver Tumor": 1.5,
        "Cushing's Disease (Hyperadrenocorticism)": 1.3,
        "Toxicosis": 1.5,
        "Poisoning/Toxicity": 1.5,
    },
    ("alp", "high"): {
        "Cushing's Disease (Hyperadrenocorticism)": 1.8,
        "Cholangiohepatitis": 1.5,
        "Hepatitis": 1.3,
        "Hepatic Lipidosis": 1.5,
        "Bone Tumor (Osteosarcoma)": 1.3,
        "Pancreatitis": 1.3,
    },
    ("ggt", "high"): {
        "Cholangiohepatitis": 1.8,
        "Bile Duct Obstruction": 2.0,
        "Hepatic Lipidosis": 1.5,
        "Pancreatitis": 1.3,
    },
    ("tbil", "high"): {
        "Hepatitis": 1.8,
        "Cholangiohepatitis": 2.0,
        "Immune-Mediated Hemolytic Anemia (IMHA)": 2.0,
        "Bile Duct Obstruction": 2.0,
        "Hepatic Lipidosis": 1.5,
        "Babesiosis": 1.5,
    },
    ("albumin", "low"): {
        "Protein-Losing Enteropathy (PLE)": 2.0,
        "Protein-Losing Nephropathy (PLN)": 2.0,
        "Chronic Kidney Disease (CKD)": 1.3,
        "Hepatitis": 1.5,
        "Portosystemic Shunt": 1.5,
        "Exocrine Pancreatic Insufficiency (EPI)": 1.3,
    },
    ("bile_acids", "high"): {
        "Portosystemic Shunt": 2.0,
        "Hepatitis": 1.8,
        "Hepatic Lipidosis": 1.5,
    },
    ("ammonia", "high"): {
        "Portosystemic Shunt": 2.0,
        "Hepatic Encephalopathy": 2.0,
        "Hepatitis": 1.5,
    },

    # --- 膵臓 --- [1] Nelson & Couto Ch.39
    ("lipase", "high"): {
        "Pancreatitis": 2.0,
    },
    ("amylase", "high"): {
        "Pancreatitis": 1.5,  # Less specific than lipase
    },
    ("spec_cpl", "high"): {  # Spec cPL / fPL
        "Pancreatitis": 2.0,
    },

    # --- 血糖 --- [28] Feldman (2015)
    ("glucose", "high"): {
        "Diabetes Mellitus": 2.0,
        "Cushing's Disease (Hyperadrenocorticism)": 1.5,
        "Pancreatitis": 1.3,
        "Stress (cats)": 1.3,
    },
    ("glucose", "low"): {
        "Insulinoma": 2.0,
        "Addison's Disease (Hypoadrenocorticism)": 1.5,
        "Sepsis": 1.5,
        "Hepatic Failure": 1.5,
        "Portosystemic Shunt": 1.3,
        "Xylitol Toxicosis": 2.0,
    },
    ("fructosamine", "high"): {
        "Diabetes Mellitus": 2.0,
    },

    # --- 電解質 --- [2] Ettinger Ch.55–58
    ("potassium", "high"): {
        "Addison's Disease (Hypoadrenocorticism)": 2.0,
        "Acute Kidney Injury": 1.8, "Acute Renal Failure": 1.8,
        "Urinary Obstruction": 1.8,
        "Urethral Obstruction": 1.8,
    },
    ("potassium", "low"): {
        "Chronic Kidney Disease (CKD)": 1.3,
        "Diabetic Ketoacidosis (DKA)": 1.5,
        "Hypokalemic Myopathy": 2.0,
        "Hypokalemic Polymyopathy": 2.0,
    },
    ("sodium", "low"): {
        "Addison's Disease (Hypoadrenocorticism)": 2.0,
        "Congestive Heart Failure": 1.3,
    },
    ("sodium", "high"): {
        "Dehydration": 1.5,
        "Diabetes Insipidus": 1.8,
    },
    ("calcium", "high"): {
        "Lymphoma": 1.8,
        "Anal Sac Adenocarcinoma": 1.8,
        "Primary Hyperparathyroidism": 2.0,
        "Chronic Kidney Disease (CKD)": 1.3,
        "Addison's Disease (Hypoadrenocorticism)": 1.3,
    },
    ("calcium", "low"): {
        "Eclampsia (Puerperal Hypocalcemia)": 2.0,
        "Hypoparathyroidism": 2.0,
        "Pancreatitis": 1.3,
        "Chronic Kidney Disease (CKD)": 1.3,
    },
    ("phosphorus", "high"): {
        "Chronic Kidney Disease (CKD)": 1.8,
        "Acute Kidney Injury": 1.5, "Acute Renal Failure": 1.5,
        "Hypoparathyroidism": 1.5,
    },

    # --- CBC (血球) --- [1] Nelson & Couto Ch.80–83
    ("wbc", "high"): {
        "Pyometra": 1.5,
        "Pneumonia": 1.3,
        "Abscess": 1.3,
        "Sepsis": 1.3,
        "Leukemia": 1.8,
    },
    ("wbc", "low"): {
        "Canine Parvovirus": 2.0,
        "Feline Panleukopenia": 2.0,
        "Sepsis": 1.5,
        "Ehrlichiosis": 1.5,
        "Bone Marrow Disease": 1.8,
    },
    ("rbc", "low"): {  # 貧血
        "Immune-Mediated Hemolytic Anemia (IMHA)": 2.0,
        "Chronic Kidney Disease (CKD)": 1.5,
        "Iron Deficiency Anemia": 1.8,
        "Feline Infectious Anemia (Hemoplasma)": 1.8,
        "Babesiosis": 1.5,
        "Internal Bleeding": 1.8,
    },
    ("pcv", "low"): {  # PCV/HCT
        "Immune-Mediated Hemolytic Anemia (IMHA)": 2.0,
        "Iron Deficiency Anemia": 1.8,
        "Chronic Kidney Disease (CKD)": 1.5,
        "Internal Bleeding": 1.8,
    },
    ("pcv", "high"): {  # 多血症
        "Dehydration": 1.5,
        "Polycythemia Vera": 2.0,
    },
    ("platelets", "low"): {
        "Immune-Mediated Thrombocytopenia (ITP)": 2.0,
        "Ehrlichiosis": 1.8,
        "Disseminated Intravascular Coagulation (DIC)": 1.8,
        "Babesiosis": 1.5,
        "Bone Marrow Disease": 1.5,
    },
    ("reticulocytes", "high"): {
        "Immune-Mediated Hemolytic Anemia (IMHA)": 1.8,
        "Iron Deficiency Anemia": 1.5,
        "Internal Bleeding": 1.5,
    },

    # --- 内分泌 --- [28] Feldman (2015)
    ("t4", "high"): {
        "Hyperthyroidism": 2.0,
    },
    ("t4", "low"): {
        "Hypothyroidism": 2.0,
    },
    ("tsh", "high"): {
        "Hypothyroidism": 2.0,
    },
    ("cortisol_post_acth", "high"): {
        "Cushing's Disease (Hyperadrenocorticism)": 2.0,
    },
    ("cortisol_post_acth", "low"): {
        "Addison's Disease (Hypoadrenocorticism)": 2.0,
    },
    ("cortisol_baseline", "low"): {
        "Addison's Disease (Hypoadrenocorticism)": 1.8,
    },

    # --- 尿検査 --- [2] Ettinger Ch.312
    ("usg", "low"): {  # 尿比重低下 (< 1.030 犬, < 1.035 猫)
        "Chronic Kidney Disease (CKD)": 1.8,
        "Diabetes Insipidus": 1.8,
        "Cushing's Disease (Hyperadrenocorticism)": 1.5,
        "Hyperthyroidism": 1.3,
    },
    ("upc", "high"): {  # 尿タンパク/クレアチニン比
        "Protein-Losing Nephropathy (PLN)": 2.0,
        "Glomerulonephritis": 2.0,
        "Chronic Kidney Disease (CKD)": 1.5,
    },

    # --- 炎症マーカー ---
    ("crp", "high"): {  # C-reactive protein
        "Pancreatitis": 1.5,
        "Immune-Mediated Polyarthritis": 1.5,
        "Pneumonia": 1.3,
        "Pyometra": 1.3,
        "Sepsis": 1.5,
    },

    # --- 凝固 ---
    ("pt", "high"): {  # プロトロンビン時間延長
        "Rodenticide Poisoning": 2.0,
        "Disseminated Intravascular Coagulation (DIC)": 1.8,
        "Hepatic Failure": 1.5,
    },
    ("aptt", "high"): {  # APTT延長
        "Rodenticide Poisoning": 2.0,
        "Hemophilia": 2.0,
        "Disseminated Intravascular Coagulation (DIC)": 1.8,
    },
}

# 検査項目の表示名 (日英)
LAB_ITEM_NAMES: Dict[str, Dict[str, str]] = {
    "bun": {"en": "BUN (Blood Urea Nitrogen)", "ja": "BUN (血中尿素窒素)"},
    "creatinine": {"en": "Creatinine", "ja": "クレアチニン"},
    "sdma": {"en": "SDMA", "ja": "SDMA"},
    "alt": {"en": "ALT (GPT)", "ja": "ALT (GPT)"},
    "alp": {"en": "ALP", "ja": "ALP"},
    "ggt": {"en": "GGT", "ja": "GGT"},
    "tbil": {"en": "Total Bilirubin", "ja": "総ビリルビン"},
    "albumin": {"en": "Albumin", "ja": "アルブミン"},
    "bile_acids": {"en": "Bile Acids", "ja": "胆汁酸"},
    "ammonia": {"en": "Ammonia", "ja": "アンモニア"},
    "lipase": {"en": "Lipase", "ja": "リパーゼ"},
    "amylase": {"en": "Amylase", "ja": "アミラーゼ"},
    "spec_cpl": {"en": "Spec cPL/fPL", "ja": "Spec cPL/fPL"},
    "glucose": {"en": "Glucose", "ja": "血糖値"},
    "fructosamine": {"en": "Fructosamine", "ja": "フルクトサミン"},
    "potassium": {"en": "Potassium (K)", "ja": "カリウム (K)"},
    "sodium": {"en": "Sodium (Na)", "ja": "ナトリウム (Na)"},
    "calcium": {"en": "Calcium (Ca)", "ja": "カルシウム (Ca)"},
    "phosphorus": {"en": "Phosphorus (P)", "ja": "リン (P)"},
    "wbc": {"en": "WBC", "ja": "白血球数"},
    "rbc": {"en": "RBC", "ja": "赤血球数"},
    "pcv": {"en": "PCV/HCT", "ja": "ヘマトクリット"},
    "platelets": {"en": "Platelets", "ja": "血小板数"},
    "reticulocytes": {"en": "Reticulocytes", "ja": "網状赤血球"},
    "t4": {"en": "T4 (Thyroxine)", "ja": "T4 (サイロキシン)"},
    "tsh": {"en": "TSH", "ja": "TSH"},
    "cortisol_post_acth": {"en": "Cortisol (post-ACTH)", "ja": "コルチゾール (ACTH後)"},
    "cortisol_baseline": {"en": "Cortisol (Baseline)", "ja": "コルチゾール (基礎値)"},
    "usg": {"en": "USG (Urine Specific Gravity)", "ja": "尿比重"},
    "upc": {"en": "UPC (Urine Protein/Creatinine)", "ja": "尿蛋白/クレアチニン比"},
    "crp": {"en": "CRP", "ja": "CRP (C反応性蛋白)"},
    "pt": {"en": "PT (Prothrombin Time)", "ja": "PT (プロトロンビン時間)"},
    "aptt": {"en": "APTT", "ja": "APTT"},
}

# 検査項目の基準値範囲 (犬・猫共通の代表値; 種別の精密な基準値は将来拡張)
# "low_threshold" 未満 → "low", "high_threshold" 超 → "high"
LAB_REFERENCE_RANGES: Dict[str, Dict[str, float]] = {
    "bun":        {"low_threshold": 7,    "high_threshold": 27},    # mg/dL
    "creatinine": {"low_threshold": 0.5,  "high_threshold": 1.8},   # mg/dL
    "sdma":       {"low_threshold": 0,    "high_threshold": 14},     # µg/dL
    "alt":        {"low_threshold": 10,   "high_threshold": 125},    # U/L
    "alp":        {"low_threshold": 23,   "high_threshold": 212},    # U/L
    "ggt":        {"low_threshold": 0,    "high_threshold": 11},     # U/L
    "tbil":       {"low_threshold": 0,    "high_threshold": 0.5},    # mg/dL
    "albumin":    {"low_threshold": 2.3,  "high_threshold": 4.0},    # g/dL
    "bile_acids": {"low_threshold": 0,    "high_threshold": 25},     # µmol/L
    "ammonia":    {"low_threshold": 0,    "high_threshold": 98},     # µg/dL
    "lipase":     {"low_threshold": 10,   "high_threshold": 160},    # U/L
    "amylase":    {"low_threshold": 500,  "high_threshold": 1500},   # U/L
    "spec_cpl":   {"low_threshold": 0,    "high_threshold": 200},    # µg/L (Spec cPL)
    "glucose":    {"low_threshold": 74,   "high_threshold": 143},    # mg/dL
    "fructosamine": {"low_threshold": 190, "high_threshold": 340},   # µmol/L
    "potassium":  {"low_threshold": 3.5,  "high_threshold": 5.8},    # mEq/L
    "sodium":     {"low_threshold": 140,  "high_threshold": 155},    # mEq/L
    "calcium":    {"low_threshold": 7.9,  "high_threshold": 12.0},   # mg/dL
    "phosphorus": {"low_threshold": 2.5,  "high_threshold": 6.8},    # mg/dL
    "wbc":        {"low_threshold": 5.5,  "high_threshold": 16.9},   # ×10³/µL
    "rbc":        {"low_threshold": 5.5,  "high_threshold": 8.5},    # ×10⁶/µL
    "pcv":        {"low_threshold": 37,   "high_threshold": 55},     # %
    "platelets":  {"low_threshold": 175,  "high_threshold": 500},    # ×10³/µL
    "reticulocytes": {"low_threshold": 0, "high_threshold": 60},     # ×10³/µL
    "t4":         {"low_threshold": 1.0,  "high_threshold": 4.0},    # µg/dL
    "tsh":        {"low_threshold": 0.03, "high_threshold": 0.5},    # ng/mL
    "cortisol_post_acth": {"low_threshold": 6, "high_threshold": 18},  # µg/dL
    "cortisol_baseline":  {"low_threshold": 1, "high_threshold": 5},   # µg/dL
    "usg":        {"low_threshold": 1.030, "high_threshold": 99},    # no upper abnormal
    "upc":        {"low_threshold": 0,     "high_threshold": 0.5},   # ratio
    "crp":        {"low_threshold": 0,     "high_threshold": 10},    # mg/L
    "pt":         {"low_threshold": 0,     "high_threshold": 17},    # seconds
    "aptt":       {"low_threshold": 0,     "high_threshold": 25},    # seconds
}


# ---------------------------------------------------------------------------
# SPECIES-SPECIFIC LAB REFERENCE RANGES
# ---------------------------------------------------------------------------
# Each species has its own normal reference ranges for lab values.
# Based on veterinary clinical pathology references:
# - Willard & Tvedten: Small Animal Clinical Diagnosis by Laboratory Methods
# - Quesenberry & Carpenter: Ferrets, Rabbits, and Rodents
# - Meredith & Lord: BSAVA Manual of Rabbit Medicine
# - Kaneko et al: Clinical Biochemistry of Domestic Animals

SPECIES_LAB_REFERENCE_RANGES: Dict[str, Dict[str, Dict[str, float]]] = {
    "cat": {
        "bun":        {"low_threshold": 16,   "high_threshold": 36},
        "creatinine": {"low_threshold": 0.8,  "high_threshold": 2.4},
        "sdma":       {"low_threshold": 0,    "high_threshold": 14},
        "alt":        {"low_threshold": 12,   "high_threshold": 130},
        "alp":        {"low_threshold": 14,   "high_threshold": 111},
        "ggt":        {"low_threshold": 0,    "high_threshold": 4},
        "tbil":       {"low_threshold": 0,    "high_threshold": 0.4},
        "albumin":    {"low_threshold": 2.1,  "high_threshold": 3.9},
        "glucose":    {"low_threshold": 74,   "high_threshold": 159},
        "potassium":  {"low_threshold": 3.5,  "high_threshold": 5.8},
        "sodium":     {"low_threshold": 147,  "high_threshold": 156},
        "calcium":    {"low_threshold": 8.0,  "high_threshold": 11.8},
        "phosphorus": {"low_threshold": 3.1,  "high_threshold": 6.8},
        "wbc":        {"low_threshold": 5.5,  "high_threshold": 19.5},
        "pcv":        {"low_threshold": 30,   "high_threshold": 45},
        "platelets":  {"low_threshold": 175,  "high_threshold": 500},
        "t4":         {"low_threshold": 1.0,  "high_threshold": 5.0},
        "crp":        {"low_threshold": 0,    "high_threshold": 5},
    },
    "rabbit": {
        "bun":        {"low_threshold": 13,   "high_threshold": 29},
        "creatinine": {"low_threshold": 0.5,  "high_threshold": 2.5},
        "alt":        {"low_threshold": 14,   "high_threshold": 80},
        "alp":        {"low_threshold": 10,   "high_threshold": 70},
        "ggt":        {"low_threshold": 0,    "high_threshold": 14},
        "tbil":       {"low_threshold": 0,    "high_threshold": 0.5},
        "albumin":    {"low_threshold": 2.7,  "high_threshold": 4.6},
        "glucose":    {"low_threshold": 75,   "high_threshold": 150},
        "potassium":  {"low_threshold": 3.5,  "high_threshold": 7.0},
        "sodium":     {"low_threshold": 131,  "high_threshold": 155},
        "calcium":    {"low_threshold": 12.0, "high_threshold": 16.0},
        "phosphorus": {"low_threshold": 4.0,  "high_threshold": 6.9},
        "wbc":        {"low_threshold": 5.0,  "high_threshold": 12.0},
        "pcv":        {"low_threshold": 33,   "high_threshold": 45},
        "platelets":  {"low_threshold": 250,  "high_threshold": 650},
    },
    "hamster": {
        "bun":        {"low_threshold": 12,   "high_threshold": 25},
        "creatinine": {"low_threshold": 0.3,  "high_threshold": 1.0},
        "alt":        {"low_threshold": 22,   "high_threshold": 128},
        "alp":        {"low_threshold": 25,   "high_threshold": 110},
        "albumin":    {"low_threshold": 2.6,  "high_threshold": 4.1},
        "glucose":    {"low_threshold": 60,   "high_threshold": 150},
        "potassium":  {"low_threshold": 3.9,  "high_threshold": 5.5},
        "sodium":     {"low_threshold": 128,  "high_threshold": 144},
        "calcium":    {"low_threshold": 5.3,  "high_threshold": 12.0},
        "phosphorus": {"low_threshold": 3.4,  "high_threshold": 8.2},
        "wbc":        {"low_threshold": 3.0,  "high_threshold": 11.0},
        "pcv":        {"low_threshold": 36,   "high_threshold": 55},
    },
    "guinea_pig": {
        "bun":        {"low_threshold": 9,    "high_threshold": 31},
        "creatinine": {"low_threshold": 0.6,  "high_threshold": 2.2},
        "alt":        {"low_threshold": 10,   "high_threshold": 100},
        "alp":        {"low_threshold": 18,   "high_threshold": 105},
        "albumin":    {"low_threshold": 2.1,  "high_threshold": 3.9},
        "glucose":    {"low_threshold": 60,   "high_threshold": 125},
        "potassium":  {"low_threshold": 4.0,  "high_threshold": 8.0},
        "sodium":     {"low_threshold": 120,  "high_threshold": 152},
        "calcium":    {"low_threshold": 8.2,  "high_threshold": 12.0},
        "phosphorus": {"low_threshold": 4.0,  "high_threshold": 7.5},
        "wbc":        {"low_threshold": 5.5,  "high_threshold": 17.5},
        "pcv":        {"low_threshold": 37,   "high_threshold": 48},
    },
    "ferret": {
        "bun":        {"low_threshold": 10,   "high_threshold": 45},
        "creatinine": {"low_threshold": 0.2,  "high_threshold": 0.9},
        "alt":        {"low_threshold": 78,   "high_threshold": 289},
        "alp":        {"low_threshold": 9,    "high_threshold": 84},
        "albumin":    {"low_threshold": 2.8,  "high_threshold": 3.8},
        "glucose":    {"low_threshold": 63,   "high_threshold": 134},
        "potassium":  {"low_threshold": 4.5,  "high_threshold": 7.7},
        "sodium":     {"low_threshold": 137,  "high_threshold": 162},
        "calcium":    {"low_threshold": 8.0,  "high_threshold": 11.8},
        "phosphorus": {"low_threshold": 4.0,  "high_threshold": 9.1},
        "wbc":        {"low_threshold": 2.5,  "high_threshold": 8.6},
        "pcv":        {"low_threshold": 42,   "high_threshold": 55},
        "platelets":  {"low_threshold": 172,  "high_threshold": 613},
    },
    "chinchilla": {
        "bun":        {"low_threshold": 10,   "high_threshold": 25},
        "creatinine": {"low_threshold": 0.4,  "high_threshold": 1.3},
        "alt":        {"low_threshold": 10,   "high_threshold": 35},
        "alp":        {"low_threshold": 6,    "high_threshold": 36},
        "albumin":    {"low_threshold": 2.3,  "high_threshold": 4.4},
        "glucose":    {"low_threshold": 60,   "high_threshold": 120},
        "calcium":    {"low_threshold": 8.0,  "high_threshold": 14.0},
        "phosphorus": {"low_threshold": 4.0,  "high_threshold": 8.0},
        "wbc":        {"low_threshold": 4.0,  "high_threshold": 18.0},
        "pcv":        {"low_threshold": 33,   "high_threshold": 45},
    },
    "hedgehog": {
        "bun":        {"low_threshold": 13,   "high_threshold": 42},
        "creatinine": {"low_threshold": 0.2,  "high_threshold": 0.5},
        "alt":        {"low_threshold": 18,   "high_threshold": 60},
        "alp":        {"low_threshold": 10,   "high_threshold": 52},
        "glucose":    {"low_threshold": 63,   "high_threshold": 148},
        "calcium":    {"low_threshold": 7.3,  "high_threshold": 11.0},
        "wbc":        {"low_threshold": 5.0,  "high_threshold": 18.0},
        "pcv":        {"low_threshold": 30,   "high_threshold": 45},
    },
    "bird": {
        "bun":        {"low_threshold": 0,    "high_threshold": 11},
        "creatinine": {"low_threshold": 0.1,  "high_threshold": 0.4},
        "alt":        {"low_threshold": 19,   "high_threshold": 50},
        "alp":        {"low_threshold": 10,   "high_threshold": 75},
        "tbil":       {"low_threshold": 0,    "high_threshold": 0.3},
        "albumin":    {"low_threshold": 1.0,  "high_threshold": 2.5},
        "glucose":    {"low_threshold": 200,  "high_threshold": 450},
        "calcium":    {"low_threshold": 8.0,  "high_threshold": 13.0},
        "wbc":        {"low_threshold": 5.0,  "high_threshold": 13.0},
        "pcv":        {"low_threshold": 35,   "high_threshold": 55},
    },
    "reptile": {
        "bun":        {"low_threshold": 0,    "high_threshold": 15},
        "creatinine": {"low_threshold": 0.1,  "high_threshold": 0.5},
        "alt":        {"low_threshold": 5,    "high_threshold": 30},
        "alp":        {"low_threshold": 10,   "high_threshold": 100},
        "glucose":    {"low_threshold": 40,   "high_threshold": 200},
        "calcium":    {"low_threshold": 8.0,  "high_threshold": 14.0},
        "phosphorus": {"low_threshold": 1.5,  "high_threshold": 5.5},
        "wbc":        {"low_threshold": 3.0,  "high_threshold": 15.0},
        "pcv":        {"low_threshold": 20,   "high_threshold": 40},
    },
    "horse": {
        "bun":        {"low_threshold": 10,   "high_threshold": 27},
        "creatinine": {"low_threshold": 1.0,  "high_threshold": 2.0},
        "alt":        {"low_threshold": 3,    "high_threshold": 23},
        "alp":        {"low_threshold": 143,  "high_threshold": 395},
        "ggt":        {"low_threshold": 4,    "high_threshold": 44},
        "tbil":       {"low_threshold": 1.0,  "high_threshold": 3.5},
        "albumin":    {"low_threshold": 2.6,  "high_threshold": 3.7},
        "glucose":    {"low_threshold": 75,   "high_threshold": 115},
        "potassium":  {"low_threshold": 2.8,  "high_threshold": 4.7},
        "sodium":     {"low_threshold": 132,  "high_threshold": 146},
        "calcium":    {"low_threshold": 11.2, "high_threshold": 13.6},
        "phosphorus": {"low_threshold": 2.3,  "high_threshold": 4.7},
        "wbc":        {"low_threshold": 5.4,  "high_threshold": 14.3},
        "pcv":        {"low_threshold": 32,   "high_threshold": 53},
        "platelets":  {"low_threshold": 100,  "high_threshold": 350},
    },
}

# Alias species to share reference ranges
for _alias, _source in [
    ("parakeet", "bird"), ("parrot", "bird"),
    ("snake", "reptile"), ("lizard", "reptile"),
    ("tortoise", "reptile"), ("amphibian", "reptile"),
    ("sugar_glider", "hamster"), ("degu", "chinchilla"),
    ("exotic_other", "hamster"),
]:
    SPECIES_LAB_REFERENCE_RANGES[_alias] = SPECIES_LAB_REFERENCE_RANGES[_source]

# ---------------------------------------------------------------------------
# LAB COMBINATION PATTERNS (synergistic multi-lab abnormality detection)
# ---------------------------------------------------------------------------
# When multiple lab values are simultaneously abnormal, these combinations
# provide stronger evidence than any single lab value alone.

LAB_COMBINATION_PATTERNS: Dict[frozenset, Dict[str, float]] = {
    frozenset({("bun", "high"), ("creatinine", "high")}): {
        "Chronic Kidney Disease (CKD)": 2.8,
        "Acute Kidney Injury": 3.0,
        "Leptospirosis": 2.0,
    },
    frozenset({("bun", "high"), ("creatinine", "high"), ("phosphorus", "high")}): {
        "Chronic Kidney Disease (CKD)": 3.2,
        "Acute Kidney Injury": 3.5,
    },
    frozenset({("alt", "high"), ("alp", "high")}): {
        "Hepatitis": 2.5,
        "Cholangiohepatitis": 2.5,
        "Liver Disease": 2.5,
    },
    frozenset({("alt", "high"), ("alp", "high"), ("tbil", "high")}): {
        "Hepatitis": 3.0,
        "Cholangiohepatitis": 3.2,
        "Liver Disease": 3.0,
        "Portosystemic Shunt": 2.5,
    },
    frozenset({("glucose", "high"), ("fructosamine", "high")}): {
        "Diabetes Mellitus": 3.5,
    },
    frozenset({("t4", "low"), ("tsh", "high")}): {
        "Hypothyroidism": 3.5,
    },
    frozenset({("t4", "high"),}): {
        "Hyperthyroidism": 2.5,
    },
    frozenset({("cortisol_post_acth", "high"), ("alp", "high")}): {
        "Cushing's Disease (Hyperadrenocorticism)": 3.0,
    },
    frozenset({("wbc", "high"), ("crp", "high")}): {
        "Sepsis": 2.0,
        "Pyometra": 2.2,
        "Peritonitis": 2.0,
    },
    frozenset({("pcv", "low"), ("platelets", "low")}): {
        "Immune-Mediated Hemolytic Anemia (IMHA)": 2.5,
        "Ehrlichiosis": 2.3,
        "Hemangiosarcoma": 2.0,
    },
    frozenset({("albumin", "low"), ("calcium", "low")}): {
        "Protein-Losing Enteropathy (PLE)": 2.5,
        "Inflammatory Bowel Disease (IBD)": 2.0,
    },
    frozenset({("potassium", "high"), ("sodium", "low")}): {
        "Addison's Disease (Hypoadrenocorticism)": 3.5,
    },
    frozenset({("bun", "low"), ("albumin", "low")}): {
        "Liver Disease": 2.2,
        "Portosystemic Shunt": 2.8,
    },
}


def compute_lab_boosts(
    lab_values: Dict[str, float],
    species: str = "dog",
) -> Dict[str, float]:
    """検査値の異常パターンから疾患ブーストマッピングを計算する。

    Parameters
    ----------
    lab_values:
        {検査項目ID: 数値} の辞書。例: {"bun": 45, "creatinine": 3.2}
    species:
        動物種ID。種別基準範囲が存在する場合はそちらを使用。

    Returns
    -------
    Dict[str, float]
        {疾患名: 最大ブースト倍率} の辞書。
        複数の検査値異常が同一疾患を指す場合は最大倍率を採用。
        検査値組合せパターンが一致する場合はさらに高い倍率を適用。
    """
    # Select species-specific reference ranges, fall back to dog
    ref_ranges = SPECIES_LAB_REFERENCE_RANGES.get(species, LAB_REFERENCE_RANGES)

    boosts: Dict[str, float] = {}
    abnormalities: list[str] = []
    detected_abnormals: set = set()  # Track (item, direction) for combination patterns

    for item, value in lab_values.items():
        # Try species-specific range first, then fall back to dog range
        ref = ref_ranges.get(item) if isinstance(ref_ranges, dict) else None
        if ref is None:
            ref = LAB_REFERENCE_RANGES.get(item)
        if ref is None:
            continue

        direction = None
        if value > ref["high_threshold"]:
            direction = "high"
        elif value < ref["low_threshold"]:
            direction = "low"

        if direction is None:
            continue

        detected_abnormals.add((item, direction))

        # 異常値を記録
        arrow = "↑" if direction == "high" else "↓"
        name_info = LAB_ITEM_NAMES.get(item, {"ja": item, "en": item})
        abnormalities.append(f"{name_info['ja']}{arrow} ({value})")

        # 疾患ブーストを適用
        key = (item, direction)
        disease_boosts = LAB_ABNORMALITY_DISEASE_MAP.get(key, {})
        for disease_name, multiplier in disease_boosts.items():
            if disease_name not in boosts or multiplier > boosts[disease_name]:
                boosts[disease_name] = multiplier

    # Apply combination pattern boosts (synergistic multi-lab detection)
    if len(detected_abnormals) >= 2:
        for pattern, pattern_boosts in LAB_COMBINATION_PATTERNS.items():
            if pattern <= detected_abnormals:
                for disease_name, multiplier in pattern_boosts.items():
                    if disease_name not in boosts or multiplier > boosts[disease_name]:
                        boosts[disease_name] = multiplier

    return boosts


def _compute_severity(suspected: List[Dict[str, Any]]) -> str:
    """Determine the overall severity level from the list of suspected diseases.

    The rules are similar to the dog implementation: if any emergency
    disease is highly likely, return "emergency". If any high-urgency disease
    is high or moderately likely, return "high". If any disease is highly
    likely, return "moderate". Otherwise return "low".
    """
    # Emergency override
    for disease in suspected:
        if disease.get("_urgency") == "emergency" and disease.get("likelihood") == "high":
            return "emergency"
    # High severity conditions
    for disease in suspected:
        if disease.get("_urgency") in ("high", "emergency") and disease.get("likelihood") in ("high", "moderate"):
            return "high"
    # Moderate severity if any high likelihood
    for disease in suspected:
        if disease.get("likelihood") == "high":
            return "moderate"
    return "low"


def _fuzzy_boost_lookup(
    disease_name: str,
    boost_dict: Dict[str, float],
) -> float:
    """疾患名の部分一致でブースト辞書を検索する。

    完全一致を優先し、見つからない場合はブースト辞書のキーが疾患名に含まれるか、
    またはその逆で一致するものを探す。括弧内の追加情報を除いた基本名でも照合する。
    """
    # 1. 完全一致
    if disease_name in boost_dict:
        return boost_dict[disease_name]

    # 2. 正規化名での照合
    disease_lower = disease_name.lower()
    base_name = disease_name.split("(")[0].strip().lower()
    best_multiplier = 1.0
    for boost_name, multiplier in boost_dict.items():
        boost_lower = boost_name.lower()
        boost_base = boost_name.split("(")[0].strip().lower()
        # 基本名の部分一致（どちらかが相手に含まれる）
        if (base_name and boost_base and
            (base_name in boost_base or boost_base in base_name)):
            if multiplier > best_multiplier:
                best_multiplier = multiplier
            continue
        # 全文部分一致（括弧内含む、例: "Brachycephalic" in "Saddle Nose (Brachycephalic ...)"）
        if boost_lower in disease_lower or disease_lower in boost_lower:
            if multiplier > best_multiplier:
                best_multiplier = multiplier
            continue
        # スラッシュ区切りの各部分で照合（例: "Tumors/Neoplasia" → ["tumors", "neoplasia"]）
        if "/" in boost_name:
            parts = [p.strip().lower() for p in boost_name.split("/")]
            if any(p in disease_lower for p in parts if len(p) > 3) and multiplier > best_multiplier:
                best_multiplier = multiplier
    return best_multiplier


def analyze_symptoms_generic(
    symptoms: List[str],
    diseases: List[Dict[str, Any]],
    symptom_names: Dict[str, Dict[str, str]],
    advice: Dict[str, Dict[str, str]] | None = None,
    *,
    onset: str | None = None,
    age_years: float | None = None,
    breed: str | None = None,
    species: str | None = None,
    lab_values: Dict[str, float] | None = None,
    prevalence_map: Dict[str, str] | None = None,
    gender: str | None = None,
    vaccines: list | None = None,
    vaccination_status: str | None = None,
    pain_score: int | None = None,
) -> Dict[str, Any]:
    """Generic differential diagnosis engine.

    Parameters
    ----------
    symptoms:
        A list of symptom identifiers provided by the user.
    diseases:
        A list of dictionaries representing diseases. Each dictionary must
        include the keys: ``name``, ``name_ja``, ``symptoms`` (a set of
        identifiers), ``description``, ``description_ja``, ``urgency``, and
        ``recommended_tests`` (list of strings).
        Optionally: ``onset_pattern`` (set of "acute"/"subacute"/"chronic")
        and ``age_predisposition`` (set of "puppy"/"young"/"adult"/"senior").
    symptom_names:
        A mapping from symptom identifiers to their bilingual names. Only
        identifiers present in this mapping will be included in the output.
    advice:
        Optional advice dictionary overriding the global ADVICE. Must follow
        the same structure as ADVICE if provided.
    onset:
        Optional time-course: "acute", "subacute", or "chronic".
    age_years:
        Optional age of the animal in years.
    breed:
        Optional breed identifier for breed-specific risk adjustment.
    species:
        Optional species identifier used to look up breed data.

    Returns
    -------
    dict
        A dictionary with the same structure as the dog symptom checker
        response: ``suspected_diseases``, ``recommended_tests``, ``severity``,
        ``general_advice``, ``general_advice_ja``, ``breed_genetic_tests``,
        ``breed_risk_applied``, ``onset_applied``, ``age_applied``,
        and ``symptom_names``.
    """
    symptom_set: Set[str] = set(symptoms)
    suspected: List[Dict[str, Any]] = []

    # =========================================================================
    # IDF (Inverse Disease Frequency) weighted scoring v2.0
    # 馬エンジンと同等: 稀な症状ほど高い重みを持つ
    # IDF(s) = log(N / df(s))  where df(s) = 症状 s を持つ疾患数
    # =========================================================================
    n_diseases = len(diseases)
    symptom_df: Dict[str, int] = {}  # document frequency per symptom
    for d in diseases:
        for s in d.get("symptoms", set()):
            symptom_df[s] = symptom_df.get(s, 0) + 1
    symptom_idf: Dict[str, float] = {}
    for s, df_count in symptom_df.items():
        # Laplace smoothing: log((N+1) / df) で N=1 でも IDF > 0 を保証
        symptom_idf[s] = _math.log((n_diseases + 1) / df_count) if df_count > 0 else 1.0

    # Resolve age stage
    age_stage: str | None = None
    if age_years is not None:
        if age_years < 1.0:
            age_stage = "puppy"
        elif age_years < 3.0:
            age_stage = "young"
        elif age_years < 7.0:
            age_stage = "adult"
        else:
            age_stage = "senior"

    # Look up breed risk data
    breed_risk: Dict[str, float] = {}
    breed_risk_applied = False
    if breed and species:
        breeds_for_species = SPECIES_BREEDS.get(species, [])
        for b in breeds_for_species:
            if b["id"] == breed:
                breed_risk = b.get("risk", {})
                if breed_risk:
                    breed_risk_applied = True
                break

    # Look up gender risk data
    gender_risk: Dict[str, float] = {}
    gender_risk_applied = False
    if gender and species and GENDER_RISK_MULTIPLIERS:
        species_genders = GENDER_RISK_MULTIPLIERS.get(species, {})
        for disease_name, gender_mults in species_genders.items():
            if gender in gender_mults:
                mult = gender_mults[gender]
                gender_risk[disease_name] = mult
        if gender_risk:
            gender_risk_applied = True

    # Pre-compute symptom pair boosts for current symptom set
    # Combine original SYMPTOM_PAIR_BOOST with extended patterns
    pair_boosts: Dict[str, float] = {}
    all_pair_boosts = {**SYMPTOM_PAIR_BOOST, **EXTENDED_SYMPTOM_PAIR_BOOST}
    for pair, disease_boosts in all_pair_boosts.items():
        if pair.issubset(symptom_set):
            for disease_name, multiplier in disease_boosts.items():
                # Keep highest boost if multiple pairs match same disease
                if disease_name not in pair_boosts or multiplier > pair_boosts[disease_name]:
                    pair_boosts[disease_name] = multiplier

    # Pre-compute triple (3-symptom) boosts for current symptom set
    triple_boosts: Dict[str, float] = {}
    if len(symptom_set) >= 3 and SYMPTOM_TRIPLE_BOOST:
        for triple, disease_boosts in SYMPTOM_TRIPLE_BOOST.items():
            if triple.issubset(symptom_set):
                for disease_name, multiplier in disease_boosts.items():
                    # Keep highest boost if multiple triples match same disease
                    if disease_name not in triple_boosts or multiplier > triple_boosts[disease_name]:
                        triple_boosts[disease_name] = multiplier

    # Pre-compute lab value boosts (species-specific reference ranges)
    lab_boosts: Dict[str, float] = {}
    if lab_values:
        lab_boosts = compute_lab_boosts(lab_values, species=species or "dog")

    # Pre-compute pain level boosts (CSU Canine Pain Scale)
    pain_boosts: Dict[str, float] = {}
    pain_urgency_modifier = 1.0
    if pain_score is not None and pain_score in CANINE_PAIN_SCALE:
        pain_urgency_modifier = CANINE_PAIN_SCALE[pain_score]["urgency_modifier"]
        pain_boosts = PAIN_LEVEL_DISEASE_BOOST.get(pain_score, {})

    # Pre-compute vaccine-preventable diseases (skip from results if vaccinated)
    vaccine_preventable: set = set()
    vaccine_list = [str(v) for v in (vaccines or []) if v]
    if vaccine_list:
        try:
            from api.data.vaccine_mapping import get_preventable_diseases
            vaccine_preventable = get_preventable_diseases(vaccine_list)
        except ImportError:
            pass

    # Load vaccination status handler for score adjustment
    _VaccinationStatusHandler = None
    if vaccination_status:
        try:
            from api.data.vaccination_protection import VaccinationStatusHandler
            _VaccinationStatusHandler = VaccinationStatusHandler
        except ImportError:
            pass

    n_checked = len(symptom_set)

    for disease in diseases:
        disease_symptoms = set(disease.get("symptoms", set()))
        if not disease_symptoms:
            continue
        matching = symptom_set & disease_symptoms
        # Skip vaccine-preventable diseases if animal is vaccinated
        if disease.get("name", "") in vaccine_preventable:
            continue
        if not matching:
            continue

        match_count = len(matching)
        total_count = len(disease_symptoms)

        # =====================================================================
        # IDF重み付きスコア（馬エンジンと同等のアルゴリズム）
        # 臨床的重要度 (SYMPTOM_CLINICAL_WEIGHTS) と統計的希少性 (IDF) を
        # ハイブリッドで組み合わせる
        # =====================================================================
        # IDF重み付きカバー率
        matched_idf = sum(symptom_idf.get(s, 1.0) for s in matching)
        total_idf = sum(symptom_idf.get(s, 1.0) for s in disease_symptoms)
        idf_ratio = matched_idf / total_idf if total_idf > 0 else 0.0

        # 臨床的重み付きカバー率（既存）
        matching_weight = sum(
            SYMPTOM_CLINICAL_WEIGHTS.get(s, _DEFAULT_SYMPTOM_WEIGHT) for s in matching
        )
        total_weight = sum(
            SYMPTOM_CLINICAL_WEIGHTS.get(s, _DEFAULT_SYMPTOM_WEIGHT) for s in disease_symptoms
        )
        clinical_ratio = matching_weight / total_weight if total_weight > 0 else 0.0

        # ハイブリッドスコア: IDF 60% + 臨床重み 40%
        # IDF は疾患DB内での統計的希少性、臨床重みは医学的重要度
        coverage = idf_ratio * 0.6 + clinical_ratio * 0.4

        # --- 組合せボーナス（馬エンジンと同等） ---
        # 複数症状が一致するほど信頼度が上昇
        combo_bonus = 1.0
        if match_count >= 5:
            combo_bonus = 1.20
        elif match_count >= 4:
            combo_bonus = 1.15
        elif match_count >= 3:
            combo_bonus = 1.08
        elif match_count == 2:
            combo_bonus = 1.0

        # 症状数による補正（疾患の定義症状が少ない場合のペナルティ）
        if total_count <= 2:
            symptom_count_factor = 0.75
        elif total_count <= 4:
            symptom_count_factor = 0.9
        elif total_count >= 8:
            symptom_count_factor = 1.1
        else:
            symptom_count_factor = 1.0

        # ノイズ抑制: 1症状マッチの場合
        if match_count == 1:
            if total_count >= 3:
                # 大きな疾患に1症状だけマッチ → 信頼度を大幅に下げる
                combo_bonus = 0.5
            elif total_count == 1:
                # 1症状疾患 → IDFが低い（汎用症状）ならペナルティ
                the_symptom = next(iter(disease_symptoms))
                s_idf = symptom_idf.get(the_symptom, 3.0)
                if s_idf < 3.0:
                    combo_bonus = 0.55
                elif s_idf < 4.0:
                    combo_bonus = 0.75
            else:
                combo_bonus = 0.6

        # =====================================================================
        # ベイズ除外診断: 症状の不在によるペナルティ（馬エンジンと同等）
        # P(D|absent_symptom) ∝ P(D) × (1 - P(symptom|D) × observability)
        # =====================================================================
        absence_penalty = 0.0
        absent_key_symptoms: List[str] = []

        if n_checked >= 3 and total_count >= 3:
            absent = disease_symptoms - matching
            for s in absent:
                s_idf = symptom_idf.get(s, 1.0)
                # IDF ≥ 4.0 の特徴的症状が不在 → 除外根拠
                if s_idf >= 4.0:
                    absent_key_symptoms.append(s)

            if absent_key_symptoms:
                # 観察徹底度: ユーザーがチェックした症状数に応じた重み
                observability = min(0.7, n_checked * 0.1)
                absent_idf_sum = sum(symptom_idf.get(s, 1.0) for s in absent_key_symptoms)
                max_penalty = absent_idf_sum / (total_idf + 1.0)
                absence_penalty = min(0.35, max_penalty * observability)

        # 基本スコア（IDF + 組合せ + ノイズ抑制 + ベイズ除外）
        match_percent = round(
            coverage * symptom_count_factor * combo_bonus * (1.0 - absence_penalty) * 100
        )

        # Apply onset multiplier (緩和: ペナルティを軽減)
        onset_multiplier = 1.0
        if onset:
            disease_onsets = disease.get("onset_pattern")
            if disease_onsets:
                onset_multiplier = 1.15 if onset in disease_onsets else 0.85

        # Apply age multiplier (緩和: ペナルティを軽減)
        age_multiplier = 1.0
        if age_stage:
            age_predisposition = disease.get("age_predisposition")
            if age_predisposition:
                age_multiplier = 1.15 if age_stage in age_predisposition else 0.85

        # Apply breed risk multiplier (上限を制限、部分一致)
        breed_multiplier = min(_fuzzy_boost_lookup(disease["name"], breed_risk), 1.8)

        # Apply gender risk multiplier (上限を制限、部分一致)
        gender_multiplier = min(_fuzzy_boost_lookup(disease["name"], gender_risk), 1.8)
        # If gender multiplier is 0, disease doesn't apply to this gender
        if gender_multiplier == 0.0:
            continue  # Skip this disease entirely

        # Apply symptom pair boost (上限を制限、部分一致)
        pair_multiplier = min(_fuzzy_boost_lookup(disease["name"], pair_boosts), 1.5)

        # Apply symptom triple boost (上限を制限、部分一致)
        triple_multiplier = min(_fuzzy_boost_lookup(disease["name"], triple_boosts), 2.0)

        # Apply lab value boost (上限を制限、部分一致)
        lab_multiplier = min(_fuzzy_boost_lookup(disease["name"], lab_boosts), 1.5)

        # Apply pain level boost (CSU Pain Scale disease-specific, 上限制限)
        pain_multiplier = min(_fuzzy_boost_lookup(disease["name"], pain_boosts), 1.8) if pain_boosts else pain_urgency_modifier

        # 複合ブースト倍率の上限を設定（過度なインフレ防止）
        combined_boost = onset_multiplier * age_multiplier * breed_multiplier * gender_multiplier * pair_multiplier * triple_multiplier * lab_multiplier * pain_multiplier
        combined_boost = min(combined_boost, 3.0)  # 最大3.0倍（トリプルで強いブースト可能）
        if combined_boost < 1.0:
            # ペナルティの下限: 0.6（40%以上は削らない）
            combined_boost = max(combined_boost, 0.6)

        # Adjusted match percent
        adjusted_percent = min(round(match_percent * combined_boost), 100)

        # Determine likelihood tiers similar to dog algorithm
        if adjusted_percent >= 50:
            likelihood = "high"
        elif adjusted_percent >= 30:
            likelihood = "moderate"
        else:
            likelihood = "low"
        # Map coverage percentage to a simple color class
        if adjusted_percent >= 70:
            color_class = "score-high"
        elif adjusted_percent >= 45:
            color_class = "score-moderate"
        elif adjusted_percent >= 25:
            color_class = "score-low"
        else:
            color_class = "score-minimal"
        # Get prevalence tier if prevalence_map provided
        prevalence_tier = "unknown"
        prevalence_multiplier = 1.0
        if prevalence_map:
            disease_name = disease.get("name", "")
            prevalence_tier = prevalence_map.get(disease_name, "unknown")
            prevalence_multiplier = _PREVALENCE_MULTIPLIER.get(prevalence_tier, 1.0)
            combined_boost *= prevalence_multiplier
            combined_boost = min(combined_boost, 3.0)  # Re-cap after prevalence
            if combined_boost < 1.0:
                combined_boost = max(combined_boost, 0.6)
            adjusted_percent = min(round(match_percent * combined_boost), 100)

        suspected.append({
            "name": disease["name"],
            "name_ja": disease["name_ja"],
            "likelihood": likelihood,
            "match_percent": adjusted_percent,
            "color_class": color_class,
            "prevalence_tier": prevalence_tier,
            "description": disease.get("description", ""),
            "description_ja": disease.get("description_ja", ""),
            "pathophysiology": disease.get("pathophysiology", ""),
            "pathophysiology_ja": disease.get("pathophysiology_ja", ""),
            "causes": disease.get("causes", ""),
            "causes_ja": disease.get("causes_ja", ""),
            "prevention": disease.get("prevention", ""),
            "prevention_ja": disease.get("prevention_ja", ""),
            "treatment": disease.get("treatment", ""),
            "treatment_ja": disease.get("treatment_ja", ""),
            "prognosis": disease.get("prognosis", ""),
            "prognosis_ja": disease.get("prognosis_ja", ""),
            "transmission": disease.get("transmission", ""),
            "transmission_ja": disease.get("transmission_ja", ""),
            "clinical_signs": disease.get("clinical_signs", ""),
            "clinical_signs_ja": disease.get("clinical_signs_ja", ""),
            "diagnosis": disease.get("diagnosis", ""),
            "diagnosis_ja": disease.get("diagnosis_ja", ""),
            "urgency": disease.get("urgency", "moderate"),
            "recommended_tests": disease.get("recommended_tests", []),
            "matching_symptoms": sorted(matching),
            "match_count": len(matching),
            "total_symptoms": len(disease_symptoms),
            # Scoring transparency (consumed by frontend)
            "scoring_detail": {
                "idf_ratio": round(idf_ratio, 3),
                "clinical_ratio": round(clinical_ratio, 3),
                "weighted_recall": round(coverage, 3),
                "coverage": round(coverage, 3),
                "combo_bonus": round(combo_bonus, 3),
                "absence_penalty": round(absence_penalty, 3),
                "cluster_boost": round(max(pair_multiplier, triple_multiplier), 3),
                "negative_penalty": round(symptom_count_factor, 3),
                "specificity_bonus": round(
                    sum(
                        0.06 if SYMPTOM_CLINICAL_WEIGHTS.get(s, _DEFAULT_SYMPTOM_WEIGHT) >= 2.0
                        else (0.03 if SYMPTOM_CLINICAL_WEIGHTS.get(s, _DEFAULT_SYMPTOM_WEIGHT) >= 1.5 else 0)
                        for s in matching
                    ), 3
                ),
                "prevalence_prior": round(prevalence_multiplier, 3),
                "breed_multiplier": round(breed_multiplier, 3),
                "gender_multiplier": round(gender_multiplier, 3),
                "age_multiplier": round(age_multiplier, 3),
                "onset_multiplier": round(onset_multiplier, 3),
                "lab_multiplier": round(lab_multiplier, 3),
                "pain_multiplier": round(pain_multiplier, 3),
                "confidence_level": (
                    "high" if adjusted_percent >= 50 else
                    "medium" if adjusted_percent >= 30 else "low"
                ),
            },
            # Key symptoms of this disease that the user has NOT reported
            # IDF ≥ 3.0 の特徴的症状 OR 臨床重み ≥ 1.5 の重要症状
            "missing_key_symptoms": sorted(
                s for s in (disease_symptoms - symptom_set)
                if symptom_idf.get(s, 1.0) >= 3.0 or SYMPTOM_CLINICAL_WEIGHTS.get(s, _DEFAULT_SYMPTOM_WEIGHT) >= 1.5
            ),
            # ベイズ除外: 不在の特徴的症状（高IDF）
            "absent_key_symptoms": sorted(absent_key_symptoms),
            "rule_out_note": (
                f"特徴的症状の不在: {', '.join(sorted(absent_key_symptoms)[:3])}"
                if absent_key_symptoms and absence_penalty > 0.05 else ""
            ),
            "_urgency": disease.get("urgency", "low"),
            "_match_ratio": coverage,
        })

    # Apply vaccination status adjustment (reduce confidence for vaccine-preventable diseases)
    vaccination_adjustment_applied = False
    if _VaccinationStatusHandler and vaccination_status:
        for entry in suspected:
            original = entry["match_percent"]
            adjusted, applied = _VaccinationStatusHandler.apply_vaccination_adjustment(
                entry["name"], original, vaccination_status
            )
            if applied:
                entry["match_percent_before_vaccination"] = original
                entry["match_percent"] = adjusted
                entry["vaccination_adjustment_applied"] = True
                vaccination_adjustment_applied = True
            else:
                entry["vaccination_adjustment_applied"] = False

    # Sort: Match quality tier first, then prevalence within each tier.
    # This prevents low-confidence common diseases from outranking
    # high-confidence matches just because of prevalence.
    prevalence_priority = {"very_common": 0, "common": 1, "uncommon": 2, "rare": 3, "unknown": 4}

    def _match_quality_tier(d: dict) -> int:
        pct = d["match_percent"]
        cnt = d["match_count"]
        if pct >= 50 or cnt >= 3:
            return 0  # Strong match
        if pct >= 25 or cnt >= 2:
            return 1  # Moderate match
        return 2  # Weak match (single symptom, low confidence)

    suspected.sort(
        key=lambda d: (
            _match_quality_tier(d),                                           # Primary: match quality tier
            prevalence_priority.get(d.get("prevalence_tier", "unknown"), 5),  # Secondary: prevalence within tier
            -d["match_percent"],                                              # Tertiary: match_percent (descending)
            -d["match_count"]                                                 # Quaternary: match_count (descending)
        )
    )

    # Compute overall severity
    severity = _compute_severity(suspected)

    # Collect recommended tests, preserving order and uniqueness. We look up
    # the corresponding disease definition by name and extend the list with
    # its recommended tests only once per unique test.
    recommended_tests: List[str] = []
    seen_tests: Set[str] = set()
    for entry in suspected:
        for disease in diseases:
            if disease.get("name") == entry.get("name"):
                for test in disease.get("recommended_tests", []):
                    if test not in seen_tests:
                        recommended_tests.append(test)
                        seen_tests.add(test)
                break

    # Clean internal fields
    for entry in suspected:
        entry.pop("_urgency", None)
        entry.pop("_match_ratio", None)

    # Determine advice dictionary
    advice_dict = advice or ADVICE
    advice_pair = advice_dict.get(severity, advice_dict["low"])

    # Build symptom names lookup (include missing_key_symptoms for frontend)
    used_symptoms: Set[str] = set()
    for entry in suspected:
        used_symptoms.update(entry["matching_symptoms"])
        used_symptoms.update(entry.get("missing_key_symptoms", []))
    symptom_names_lookup: Dict[str, Dict[str, str]] = {
        sid: symptom_names[sid] for sid in used_symptoms if sid in symptom_names
    }

    # Group diseases by prevalence tier for stepwise presentation (if prevalence_map provided)
    phase1_diseases = [d for d in suspected if d.get("prevalence_tier") in ("very_common", "common")]
    phase2_diseases = [d for d in suspected if d.get("prevalence_tier") in ("uncommon", "rare", "unknown")]

    return {
        "suspected_diseases": suspected,
        "suspected_diseases_by_phase": {  # New: grouped for stepwise presentation
            "phase_1_common": phase1_diseases,
            "phase_2_rare": phase2_diseases,
        },
        "recommended_tests": recommended_tests,
        "severity": severity,
        "general_advice": advice_pair["en"],
        "general_advice_ja": advice_pair["ja"],
        "breed_genetic_tests": [],
        "breed_risk_applied": breed_risk_applied,
        "breed": breed,
        "gender_risk_applied": gender_risk_applied,
        "gender": gender,
        "onset_applied": onset is not None,
        "onset": onset,
        "age_applied": age_years is not None,
        "age_years": age_years,
        "age_stage": age_stage,
        "pair_boost_applied": len(pair_boosts) > 0,
        "lab_boost_applied": len(lab_boosts) > 0,
        "lab_values": lab_values,
        "pain_score": pain_score,
        "pain_applied": pain_score is not None and pain_score > 0,
        "vaccination_adjustment_applied": vaccination_adjustment_applied,
        "vaccine_preventable_excluded": len(vaccine_preventable) > 0,
        "symptom_names": symptom_names_lookup,
    }
