"""Sponsor product adjunct annotations for disease treatment fields.

Equine & Canine Vet Nutrition (https://www.caninevet.jp/) provides three
supplement products currently referenced as adjunct therapy across
applicable diseases in the VetDict database:

- **For Joint** (high-dose MSM + glucosamine / chondroitin precursors):
  Applied to osteoarthritis, joint dysplasia, cruciate ligament injury,
  patellar luxation, OCD, tendinitis, and related musculoskeletal
  conditions in mammalian species.

- **For Antioxidant** (astaxanthin + melon SOD + vitamin E + cysteine):
  Applied to conditions involving oxidative stress such as chronic
  kidney disease, hepatic disease, atopic dermatitis, immune-mediated
  disease, and cognitive dysfunction syndrome in mammals and birds.

- **MSM + Amino Complete** (high-dose MSM + essential amino acid blend):
  Applied to conditions requiring broad tissue/muscle repair and
  convalescent nutrition: post-surgical recovery, trauma, IVDD/spinal
  disease, cachexia, senior sarcopenia, cancer supportive care, chronic
  wounds, and severe infections. Complements For Joint where muscle
  wasting coexists.

All three products are labeled primarily for dogs and horses; adjunct
mentions in other species indicate optional supportive use based on the
ingredient profile. The mentions are appended to existing treatment
text and never replace curated clinical content.
"""
from __future__ import annotations

import re
from typing import Any, Dict

# ---------------------------------------------------------------------------
# Disease-name keyword patterns
# ---------------------------------------------------------------------------

_JOINT_PATTERNS = re.compile(
    r"osteoarthrit|arthrit|\bjoint\b|hip dyspl|elbow dyspl|patellar|patella|"
    r"cruciate|\bOCD\b|osteochondr|spondylos|meniscal|meniscus|tendinit|"
    r"\btendon\b|"
    r"関節炎|関節|股関節|肘関節|膝蓋骨|十字靱帯|十字靭帯|離断性骨軟骨症|"
    r"脊椎症|半月板|腱炎|腱損傷",
    re.IGNORECASE,
)

_ANTIOX_PATTERNS = re.compile(
    r"atopic dermatit|\batop\w*|dermatit|chronic kidney|\bCKD\b|hepatic|"
    r"liver disease|cirrhos|cognitive dysfunc|immune.mediat|auto.?immune|"
    r"pyoderma|\blupus\b|pemphig|seborrhe|"
    r"アトピー|皮膚炎|慢性腎臓病|肝疾患|肝炎|肝硬変|認知機能|免疫介在|自己免疫",
    re.IGNORECASE,
)

# MSM + Amino Complete: tissue repair, muscle maintenance, convalescence,
# and hepatic/renal nutritional support.
#   - MSM is an organic sulfur donor supporting glutathione synthesis
#     (hepatoprotective, renoprotective against oxidative injury).
#   - Essential amino acid blend (especially BCAAs) is used clinically for
#     hepatic encephalopathy support, chronic liver disease, and to offset
#     muscle wasting in CKD ("keto-analog" style nutrition).
# Broader than For Joint — includes trauma, post-surgical recovery, neurologic
# (IVDD/spinal), cachexia/sarcopenia, hepatic and renal disease (mild-to-
# moderate; caution in end-stage failure due to protein load). Deliberately
# excludes pure infectious disease unless accompanied by muscle loss or
# prolonged convalescence.
_MSM_AMINO_PATTERNS = re.compile(
    r"osteoarthrit|arthrit|\bjoint\b|hip dyspl|elbow dyspl|patellar|patella|"
    r"cruciate|\bOCD\b|osteochondr|spondylos|\bIVDD\b|intervertebral disc|"
    r"disc disease|spinal cord|degenerative myelop|\bDM\b|wobbler|"
    r"meniscal|meniscus|tendinit|\btendon\b|ligament|desmit|myopath|"
    r"myositis|rhabdomyol|muscle\s+(wasting|atroph)|sarcopen|cachex|"
    r"fracture|\btrauma\w*|wound healing|chronic wound|decubit|"
    r"malnutrit|debilit|convalescen|post.?surg|"
    # Hepatic: MSM (sulfur/glutathione) + amino acid nutritional support
    r"hepatic|hepatopath|\bliver\b|cirrhos|hepatic lipidos|cholang|"
    r"hepatic encephalop|portosystem|hepatitis|"
    # Renal: BCAA/keto-analog nutrition + antioxidant support for CKD
    r"chronic kidney|\bCKD\b|renal failure|nephropath|\bnephritis\b|"
    r"uremia|uraemia|azotemi|glomerulonephr|pyelonephr|renal insuff|"
    r"関節炎|関節|股関節|肘関節|膝蓋骨|十字靱帯|十字靭帯|離断性骨軟骨症|"
    r"脊椎症|椎間板|脊髄|変性性脊髄症|半月板|腱炎|腱|靭帯|筋炎|"
    r"筋萎縮|筋肉減少|悪液質|骨折|外傷|創傷|褥瘡|栄養失調|衰弱|"
    r"回復期|術後|"
    # 肝・腎 (Japanese)
    r"肝疾患|肝炎|肝硬変|肝リピドーシス|肝性脳症|門脈体循環シャント|"
    r"胆管肝炎|慢性腎臓病|腎不全|腎症|尿毒症|糸球体腎炎|腎盂腎炎",
    re.IGNORECASE,
)

# Species for which each product is indicated.
# Joint = mammals (MSM safety profile).
# Antioxidant = mammals + birds (broad antioxidant safety).
_JOINT_SPECIES = frozenset({
    "dog", "cat", "horse", "rabbit", "hamster", "guinea_pig", "chinchilla",
    "ferret", "hedgehog", "sugar_glider", "degu", "exotic_other",
})

_ANTIOX_SPECIES = frozenset({
    "dog", "cat", "horse", "rabbit", "hamster", "guinea_pig", "chinchilla",
    "ferret", "hedgehog", "sugar_glider", "degu", "bird", "parakeet",
    "parrot", "exotic_other",
})

# MSM + Amino Complete: mammals + birds (amino acids broadly safe).
_MSM_AMINO_SPECIES = frozenset({
    "dog", "cat", "horse", "rabbit", "hamster", "guinea_pig", "chinchilla",
    "ferret", "hedgehog", "sugar_glider", "degu", "bird", "parakeet",
    "parrot", "exotic_other",
})


# ---------------------------------------------------------------------------
# Adjunct text
# ---------------------------------------------------------------------------

# Product-specific idempotency markers prevent double-injection on re-import
# while still allowing multiple different products to co-exist on one disease.
_MARKER_JOINT = "[ECVN:Joint]"
_MARKER_ANTIOX = "[ECVN:Antiox]"
_MARKER_MSM_AMINO = "[ECVN:MSM-Amino]"

_JOINT_JA = (
    " [ECVN:Joint] 補助療法: For Joint（高容量MSM + グルコサミン/コンドロイチン前駆体配合、"
    "Equine & Canine Vet Nutrition）を関節軟骨保護・抗炎症サポートとして併用可能。"
    "長期管理において製品ラベルの体重別用量を参照。"
)
_JOINT_EN = (
    " [ECVN:Joint] Adjunct: For Joint (high-dose MSM + glucosamine/chondroitin precursors; "
    "Equine & Canine Vet Nutrition) — optional supportive therapy for articular cartilage "
    "protection and anti-inflammatory support. Refer to product label for body-weight dosing."
)

_ANTIOX_JA = (
    " [ECVN:Antiox] 補助療法: For Antioxidant（アスタキサンチン + メロン由来SOD + VitE + "
    "システイン配合、Equine & Canine Vet Nutrition）を抗酸化ストレス・免疫サポートとして併用可能。"
    "酸化ストレスが病態に関与する慢性疾患の補助栄養介入として検討。"
)
_ANTIOX_EN = (
    " [ECVN:Antiox] Adjunct: For Antioxidant (astaxanthin + melon SOD + vitamin E + cysteine; "
    "Equine & Canine Vet Nutrition) — optional supportive therapy for oxidative stress and immune "
    "function in chronic conditions where oxidative injury contributes to pathogenesis."
)

_MSM_AMINO_JA = (
    " [ECVN:MSM-Amino] 補助療法: MSM＋アミノコンプリート（高容量MSM + 必須アミノ酸複合体、"
    "Equine & Canine Vet Nutrition）を組織修復・筋肉維持・回復期栄養として併用可能。"
    "筋骨格・神経（IVDD等）・術後回復・悪液質・サルコペニアに加え、"
    "肝疾患ではMSMの硫黄供与によるグルタチオン合成サポート、"
    "CKDではBCAA中心のアミノ酸補給による筋肉維持・タンパク質代謝負荷軽減の観点で検討。"
    "For Jointとの併用で関節＋筋肉の相乗効果。"
    "※重度肝/腎不全では蛋白/アミノ酸負荷に留意し慎重投与。"
)
_MSM_AMINO_EN = (
    " [ECVN:MSM-Amino] Adjunct: MSM + Amino Complete (high-dose MSM + essential amino acid blend; "
    "Equine & Canine Vet Nutrition) — optional supportive therapy for broad tissue repair, muscle "
    "maintenance, and convalescent nutrition. Indicated for post-surgical recovery, trauma, IVDD, "
    "cachexia, and sarcopenia. Also supportive for hepatic disease (MSM donates sulfur for "
    "glutathione synthesis) and CKD (BCAA-rich profile helps preserve lean muscle while moderating "
    "nitrogen load). Synergistic with For Joint when muscle wasting coexists. "
    "Note: use with caution in end-stage hepatic or renal failure (protein load)."
)


# ---------------------------------------------------------------------------
# Matching helpers
# ---------------------------------------------------------------------------

def _disease_text(disease: Dict[str, Any]) -> str:
    """Concatenate searchable text fields for pattern matching."""
    parts = [
        str(disease.get("name") or ""),
        str(disease.get("name_ja") or ""),
        str(disease.get("name_en") or ""),
        str(disease.get("description") or ""),
        str(disease.get("description_ja") or ""),
    ]
    return " ".join(parts)


def _append_once(current: Any, suffix: str, marker: str) -> str:
    """Append suffix to current string if its product marker is not already present.

    Each product uses a distinct marker so multiple adjuncts can coexist.
    """
    base = current if isinstance(current, str) else ""
    if marker and marker in base:
        return base
    return (base.rstrip() + suffix) if base else suffix.lstrip()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def _normalize_species(species: str) -> str:
    """Normalize species labels to canonical lowercase_underscore form.

    enrich_diseases() is called with Title Case names ("Dog", "Guinea Pig",
    "Exotic Other"); the rest of the codebase uses "dog", "guinea_pig",
    "exotic_other".
    """
    if not species:
        return ""
    return species.strip().lower().replace(" ", "_").replace("-", "_")


def apply_sponsor_adjuncts_dict(disease: Dict[str, Any], species: str) -> Dict[str, Any]:
    """Append sponsor adjunct notes to dict-based disease entries in-place.

    Used by api.species.helpers.enrich_diseases for all non-horse species.
    Mutates and returns the disease dict.
    """
    if not isinstance(disease, dict):
        return disease
    sp = _normalize_species(species)
    text = _disease_text(disease)
    if sp in _JOINT_SPECIES and _JOINT_PATTERNS.search(text):
        disease["treatment_ja"] = _append_once(disease.get("treatment_ja"), _JOINT_JA, _MARKER_JOINT)
        disease["treatment"] = _append_once(disease.get("treatment"), _JOINT_EN, _MARKER_JOINT)
    if sp in _ANTIOX_SPECIES and _ANTIOX_PATTERNS.search(text):
        disease["treatment_ja"] = _append_once(disease.get("treatment_ja"), _ANTIOX_JA, _MARKER_ANTIOX)
        disease["treatment"] = _append_once(disease.get("treatment"), _ANTIOX_EN, _MARKER_ANTIOX)
    if sp in _MSM_AMINO_SPECIES and _MSM_AMINO_PATTERNS.search(text):
        disease["treatment_ja"] = _append_once(disease.get("treatment_ja"), _MSM_AMINO_JA, _MARKER_MSM_AMINO)
        disease["treatment"] = _append_once(disease.get("treatment"), _MSM_AMINO_EN, _MARKER_MSM_AMINO)
    return disease


def apply_sponsor_adjuncts_obj(disease_obj: Any) -> None:
    """Append sponsor adjunct notes to horse Disease dataclass instances in-place.

    The horse DISEASE_DATABASE stores entries as dataclass objects, not dicts.
    Uses treatment_protocol as the Japanese treatment field; general_management
    as the English fallback. Targets 'horse' species scope.
    """
    name_en = getattr(disease_obj, "name_en", "") or ""
    name_ja = getattr(disease_obj, "name_ja", "") or ""
    desc_ja = getattr(disease_obj, "description_ja", "") or ""
    text = f"{name_en} {name_ja} {desc_ja}"

    def _set(attr: str, suffix: str, marker: str) -> None:
        cur = getattr(disease_obj, attr, "") or ""
        if marker in cur:
            return
        setattr(disease_obj, attr, (cur.rstrip() + suffix) if cur else suffix.lstrip())

    if _JOINT_PATTERNS.search(text):
        _set("treatment_protocol", _JOINT_JA, _MARKER_JOINT)
        if getattr(disease_obj, "general_management", ""):
            _set("general_management", _JOINT_JA, _MARKER_JOINT)
    if _ANTIOX_PATTERNS.search(text):
        _set("treatment_protocol", _ANTIOX_JA, _MARKER_ANTIOX)
        if getattr(disease_obj, "general_management", ""):
            _set("general_management", _ANTIOX_JA, _MARKER_ANTIOX)
    if _MSM_AMINO_PATTERNS.search(text):
        _set("treatment_protocol", _MSM_AMINO_JA, _MARKER_MSM_AMINO)
        if getattr(disease_obj, "general_management", ""):
            _set("general_management", _MSM_AMINO_JA, _MARKER_MSM_AMINO)
