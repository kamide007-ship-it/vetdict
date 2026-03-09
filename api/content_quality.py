"""Disease content quality helpers.

Provides deterministic enrichment for disease narrative fields and completeness scoring.
"""
from __future__ import annotations

from typing import Any, Dict, List

REQUIRED_FIELDS = [
    "description",
    "pathophysiology",
    "causes",
    "prevention",
    "treatment",
    "prognosis",
]


def _text(v: Any) -> str:
    if v is None:
        return ""
    if isinstance(v, str):
        return v.strip()
    return str(v).strip()


def _symptom_text(symptoms: Any, limit: int = 5) -> str:
    if isinstance(symptoms, dict):
        vals = list(symptoms.keys())
    elif isinstance(symptoms, (list, tuple, set)):
        vals = [str(x) for x in symptoms]
    else:
        vals = [str(symptoms)] if symptoms else []
    vals = [v for v in vals if v]
    if not vals:
        return "clinical signs"
    if len(vals) <= limit:
        return ", ".join(vals)
    return ", ".join(vals[:limit]) + f" (+{len(vals)-limit} more)"


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


def enrich_disease_content(disease: Dict[str, Any], species: str) -> Dict[str, Any]:
    """Return disease with complete narrative fields and quality metadata."""
    out = dict(disease)
    name_ja = _text(out.get("name_ja")) or _text(out.get("name")) or "疾患"
    name_en = _text(out.get("name")) or _text(out.get("name_ja")) or "Disease"
    sym_text = _symptom_text(out.get("symptoms"))

    missing: List[str] = []
    for field in REQUIRED_FIELDS:
        ja_key = f"{field}_ja"
        en_key = field
        ja_val = _text(out.get(ja_key))
        en_val = _text(out.get(en_key))

        if not ja_val:
            out[ja_key] = _fallback(field, name_ja, species, sym_text, "ja")
            missing.append(ja_key)
        if not en_val:
            out[en_key] = _fallback(field, name_en, species, sym_text, "en")
            missing.append(en_key)

    total = len(REQUIRED_FIELDS) * 2
    out["missing_fields"] = sorted(set(missing))
    out["completeness_score"] = round((total - len(set(missing))) / total * 100, 1)
    return out
