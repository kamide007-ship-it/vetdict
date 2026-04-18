"""Sponsor product adjunct annotations for disease treatment fields.

Equine & Canine Vet Nutrition (https://www.caninevet.jp/) provides two
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

Both products are labeled primarily for dogs and horses; adjunct
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


# ---------------------------------------------------------------------------
# Adjunct text
# ---------------------------------------------------------------------------

_MARKER = "[ECVN Adjunct]"  # Idempotency marker; prevents double-injection.

_JOINT_JA = (
    " [ECVN Adjunct] 補助療法: For Joint（高容量MSM + グルコサミン/コンドロイチン前駆体配合、"
    "Equine & Canine Vet Nutrition）を関節軟骨保護・抗炎症サポートとして併用可能。"
    "長期管理において製品ラベルの体重別用量を参照。"
)
_JOINT_EN = (
    " [ECVN Adjunct] Adjunct: For Joint (high-dose MSM + glucosamine/chondroitin precursors; "
    "Equine & Canine Vet Nutrition) — optional supportive therapy for articular cartilage "
    "protection and anti-inflammatory support. Refer to product label for body-weight dosing."
)

_ANTIOX_JA = (
    " [ECVN Adjunct] 補助療法: For Antioxidant（アスタキサンチン + メロン由来SOD + VitE + "
    "システイン配合、Equine & Canine Vet Nutrition）を抗酸化ストレス・免疫サポートとして併用可能。"
    "酸化ストレスが病態に関与する慢性疾患の補助栄養介入として検討。"
)
_ANTIOX_EN = (
    " [ECVN Adjunct] Adjunct: For Antioxidant (astaxanthin + melon SOD + vitamin E + cysteine; "
    "Equine & Canine Vet Nutrition) — optional supportive therapy for oxidative stress and immune "
    "function in chronic conditions where oxidative injury contributes to pathogenesis."
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


def _append_once(current: Any, suffix: str) -> str:
    """Append suffix to current string if the adjunct marker is not already present."""
    base = current if isinstance(current, str) else ""
    if _MARKER in base:
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
        disease["treatment_ja"] = _append_once(disease.get("treatment_ja"), _JOINT_JA)
        disease["treatment"] = _append_once(disease.get("treatment"), _JOINT_EN)
    if sp in _ANTIOX_SPECIES and _ANTIOX_PATTERNS.search(text):
        disease["treatment_ja"] = _append_once(disease.get("treatment_ja"), _ANTIOX_JA)
        disease["treatment"] = _append_once(disease.get("treatment"), _ANTIOX_EN)
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

    def _set(attr: str, suffix: str) -> None:
        cur = getattr(disease_obj, attr, "") or ""
        if _MARKER in cur:
            return
        setattr(disease_obj, attr, (cur.rstrip() + suffix) if cur else suffix.lstrip())

    if _JOINT_PATTERNS.search(text):
        _set("treatment_protocol", _JOINT_JA)
        if getattr(disease_obj, "general_management", ""):
            _set("general_management", _JOINT_JA)
    if _ANTIOX_PATTERNS.search(text):
        _set("treatment_protocol", _ANTIOX_JA)
        if getattr(disease_obj, "general_management", ""):
            _set("general_management", _ANTIOX_JA)
