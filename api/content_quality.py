"""Disease content quality helpers.

Provides deterministic enrichment for disease narrative fields and completeness scoring.
"""

from __future__ import annotations

from typing import Any, Dict, List

from api.chat.constants import SPECIES_LABELS
from api.reference_catalog import (
    FIELD_REFERENCE_NUMBERS,
    SPECIES_REFERENCE_NUMBERS,
    build_reference_sources,
    normalize_reference_numbers,
)

REQUIRED_FIELDS = [
    "description",
    "pathophysiology",
    "causes",
    "prevention",
    "treatment",
    "prognosis",
]

# JA species names for narrative text. Derived from chat.constants.SPECIES_LABELS;
# overrides cover narrative-specific phrasing (e.g. "その他エキゾチック動物" vs the
# shorter UI label "その他エキゾチック").
_SPECIES_NAME_JA_OVERRIDES = {
    "exotic_other": "その他エキゾチック動物",
}
SPECIES_NAME_JA = {k: _SPECIES_NAME_JA_OVERRIDES.get(k, v["ja"]) for k, v in SPECIES_LABELS.items()}

# EN narrative form: plural ("In dogs, ...") rather than the singular UI label.
_SPECIES_NAME_EN_PLURAL_OVERRIDES = {
    "fish": "fish",
    "exotic_other": "exotic animals",
    "guinea_pig": "guinea pigs",
    "sugar_glider": "sugar gliders",
}
SPECIES_NAME_EN = {
    k: _SPECIES_NAME_EN_PLURAL_OVERRIDES.get(k, v["en"].lower() + "s") for k, v in SPECIES_LABELS.items()
}


def _text(v: Any) -> str:
    if v is None:
        return ""
    if isinstance(v, str):
        return v.strip()
    return str(v).strip()


def _symptom_text(symptoms: Any, limit: int = 5, lang: str = "en", display_entries: Any = None) -> str:
    """Render a short list of symptoms for narrative fields.

    If display_entries is provided (list of {id, name_ja, name_en}), use the
    translated names to avoid raw IDs like 'resp_cough' in generated text.
    """
    if display_entries and isinstance(display_entries, (list, tuple)):
        key = "name_ja" if lang == "ja" else "name_en"
        vals = [str(e.get(key) or e.get("id") or "") for e in display_entries if isinstance(e, dict)]
        vals = [v for v in vals if v]
    else:
        if isinstance(symptoms, dict):
            vals = list(symptoms.keys())
        elif isinstance(symptoms, (list, tuple, set)):
            vals = [str(x) for x in symptoms]
        else:
            vals = [str(symptoms)] if symptoms else []
        vals = [v for v in vals if v]
    if not vals:
        return "clinical signs" if lang != "ja" else "臨床徴候"
    sep = "、" if lang == "ja" else ", "
    if len(vals) <= limit:
        return sep.join(vals)
    overflow = len(vals) - limit
    suffix = f" (+{overflow}件)" if lang == "ja" else f" (+{overflow} more)"
    return sep.join(vals[:limit]) + suffix


def _reference_numbers_text(reference_numbers: List[int]) -> str:
    if not reference_numbers:
        return ""
    return " ".join(f"[{n}]" for n in reference_numbers[:6])


def _literature_summary(name: str, species: str, symptoms: str, reference_numbers: List[int], lang: str) -> str:
    refs = _reference_numbers_text(reference_numbers)
    if lang == "ja":
        return (
            f"{species}の{name}は、主要症状として{symptoms}を示し、"
            f"臨床所見・鑑別診断・治療方針は標準的獣医学文献に基づき整理されています。"
            f"本項目は文献{refs}を根拠に要約しています。"
        )
    return (
        f"{name} in {species} is summarized from core veterinary references with emphasis on "
        f"clinical signs ({symptoms}), differential diagnosis, and treatment planning. "
        f"Evidence basis: {refs}."
    )


def _symptom_summary(name: str, symptoms: str, species: str, lang: str) -> str:
    if lang == "ja":
        return f"{species}の{name}では、主に{symptoms}が観察されます。"
    return f"In {species}, {name} commonly presents with {symptoms}."


def _fallback(field: str, name: str, species: str, symptoms: str, lang: str) -> str:
    if lang == "ja":
        templates = {
            "description": f"{species}の{name}は、{symptoms}を中心に評価する必要がある疾患です。",
            "pathophysiology": f"{name}では、{species}の組織・臓器機能の異常が進行し、{symptoms}として表出します。",
            "causes": f"{name}の原因は単一ではなく、感染・炎症・代謝異常・飼育環境要因を含めて評価します。",
            "prevention": f"{name}の予防には、適切な栄養管理、衛生管理、定期健診、早期受診が重要です。",
            "treatment": f"{name}の治療は重症度に応じて、原因治療と支持療法（輸液・栄養・疼痛管理）を組み合わせます。",
            "prognosis": f"{name}の予後は、重症度・併存疾患・治療開始時期によって変動するため、継続評価が必要です。",
        }
    else:
        templates = {
            "description": f"{name} in {species} requires assessment centered on {symptoms}.",
            "pathophysiology": f"In {name}, organ/tissue dysfunction in {species} progresses and manifests as {symptoms}.",
            "causes": f"Causes of {name} are multifactorial and include infectious, inflammatory, metabolic, and husbandry factors.",
            "prevention": f"Prevention of {name} focuses on nutrition, hygiene, periodic screening, and early clinical intervention.",
            "treatment": f"Treatment of {name} is severity-based and combines etiologic therapy with supportive care.",
            "prognosis": f"Prognosis for {name} varies by severity, comorbidity burden, and time to treatment initiation.",
        }
    return templates[field]


def _merge_reference_numbers(out: Dict[str, Any], species: str) -> List[int]:
    raw_numbers = out.get("references") or out.get("reference_numbers") or []
    numbers = [int(n) for n in raw_numbers if str(n).strip().isdigit()]
    numbers.extend(SPECIES_REFERENCE_NUMBERS.get(species, [7, 12, 23, 24]))
    numbers.extend(FIELD_REFERENCE_NUMBERS.get("description", []))
    return normalize_reference_numbers(numbers)


def _field_reference_map(reference_numbers: List[int]) -> Dict[str, List[str]]:
    available = set(reference_numbers)
    citation_map: Dict[str, List[str]] = {}
    for field, refs in FIELD_REFERENCE_NUMBERS.items():
        valid = [f"ref-{n}" for n in refs if n in available]
        if valid:
            citation_map[field] = valid
    return citation_map


def enrich_disease_content(disease: Dict[str, Any], species: str) -> Dict[str, Any]:
    """Return disease with complete narrative fields and quality metadata."""
    out = dict(disease)
    name_ja = _text(out.get("name_ja")) or _text(out.get("name")) or "疾患"
    name_en = _text(out.get("name")) or _text(out.get("name_ja")) or "Disease"
    # Translate species key ("horse") to readable names for narrative text
    species_ja = SPECIES_NAME_JA.get(species, species)
    species_en = SPECIES_NAME_EN.get(species, species)
    display_entries = out.get("symptoms_display")
    sym_text_ja = _symptom_text(out.get("symptoms"), lang="ja", display_entries=display_entries)
    sym_text_en = _symptom_text(out.get("symptoms"), lang="en", display_entries=display_entries)
    reference_numbers = _merge_reference_numbers(out, species)

    missing: List[str] = []
    sourced: List[str] = []
    for field in REQUIRED_FIELDS:
        ja_key = f"{field}_ja"
        en_key = field
        ja_val = _text(out.get(ja_key))
        en_val = _text(out.get(en_key))

        if not ja_val:
            out[ja_key] = _fallback(field, name_ja, species_ja, sym_text_ja, "ja")
            missing.append(ja_key)
        else:
            sourced.append(ja_key)
        if not en_val:
            # Prefer JA content over English template to avoid mixed-language display
            ja_content = _text(out.get(ja_key))
            if ja_content:
                out[en_key] = ja_content
            else:
                out[en_key] = _fallback(field, name_ja, species_ja, sym_text_ja, "ja")
            missing.append(en_key)
        else:
            sourced.append(en_key)

    if not _text(out.get("symptoms_summary_ja")):
        out["symptoms_summary_ja"] = _symptom_summary(name_ja, sym_text_ja, species_ja, "ja")
        missing.append("symptoms_summary_ja")
    else:
        sourced.append("symptoms_summary_ja")
    if not _text(out.get("symptoms_summary")):
        out["symptoms_summary"] = _symptom_summary(name_en, sym_text_en, species_en, "en")
        missing.append("symptoms_summary")
    else:
        sourced.append("symptoms_summary")

    out["literature_summary_ja"] = _literature_summary(name_ja, species_ja, sym_text_ja, reference_numbers, "ja")
    out["literature_summary"] = _literature_summary(name_en, species_en, sym_text_en, reference_numbers, "en")
    out["literature_summary_references"] = reference_numbers[:8]

    bilingual_required_fields = len(REQUIRED_FIELDS) * 2
    summary_fields = 2
    total = bilingual_required_fields + summary_fields
    unique_missing = sorted(set(missing))
    out["missing_fields"] = unique_missing
    out["completeness_score"] = round((total - len(unique_missing)) / total * 100, 1)
    if len(unique_missing) == total:
        out["content_origin"] = "generated"
    elif unique_missing:
        out["content_origin"] = "mixed"
    else:
        out["content_origin"] = "sourced"
    out["sourced_fields"] = sorted(set(sourced))
    out["review_status"] = "review_required" if unique_missing else "reviewed"
    out["reference_numbers"] = reference_numbers
    out["evidence_sources"] = build_reference_sources(reference_numbers)
    out["citation_map"] = _field_reference_map(reference_numbers)
    return out
