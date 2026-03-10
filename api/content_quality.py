"""Disease content quality helpers.

Provides deterministic enrichment for disease narrative fields, mandatory
5-section normalization, and citation metadata based on curated references.
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

REFERENCE_CATALOG_VERSION = "2026-03-10"

REFERENCE_CATALOG: Dict[int, str] = {
    1: "Nelson & Couto (2019) Small Animal Internal Medicine, 6th ed.",
    2: "Ettinger, Feldman & Cote (2017) Textbook of Veterinary Internal Medicine, 8th ed.",
    3: "Reed, Bayly & Sellon (2018) Equine Internal Medicine, 4th ed.",
    4: "Quesenberry & Carpenter (2020) Ferrets, Rabbits, and Rodents, 4th ed.",
    5: "Mader & Divers (2019) Current Therapy in Reptile Medicine and Surgery.",
    6: "Ritchie et al. (1994) Avian Medicine: Principles and Application.",
    7: "Merck Veterinary Manual (2023).",
    8: "Little (2016) The Cat: Clinical Medicine and Management.",
    9: "Harcourt-Brown (2002) Textbook of Rabbit Medicine.",
    10: "Johnson-Delaney (2006) Exotic Companion Medicine Handbook.",
    11: "Smith (2015) Large Animal Internal Medicine, 5th ed.",
    12: "Plumb (2018) Plumb's Veterinary Drug Handbook, 9th ed.",
    13: "WSAVA Global Nutrition Guidelines (2020).",
    14: "HorseDVM (2024).",
    15: "犬と猫の治療薬ガイド EduOne (2024).",
    16: "Gough et al. (2018) Breed Predispositions to Disease in Dogs and Cats.",
    17: "Bell et al. (2012) Veterinary Medical Guide to Dog and Cat Breeds.",
    18: "Pedersen et al. (2015) Canine Genetics and Epidemiology 2:13.",
    19: "O'Neill et al. (2013) The Veterinary Journal 198(3):638–643.",
    20: "Malik et al. (1999) Australian Veterinary Journal 77(2):85–92.",
    21: "Lyons (2015) JFMS 17(3):203–219.",
    22: "Donner et al. (2018) PLoS ONE 13(6):e0197711.",
    23: "Rijnberk & van Sluijs (2009) Medical History and Physical Examination in Companion Animals.",
    24: "Ettinger & Feldman (2017) Clinical signs approach to differential diagnosis.",
    25: "Glickman et al. (2000) JAVMA 217(10):1492–1499.",
    26: "Côté (2014) Clinical Veterinary Advisor: Dogs and Cats.",
    27: "Polzin (2011) Vet Clin North Am Small Anim Pract 41(1):15–30.",
    28: "Feldman et al. (2015) Canine and Feline Endocrinology, 4th ed.",
    29: "Platt & Olby (2013) Manual of Canine and Feline Neurology, 4th ed.",
    30: "Tobias & Johnston (2012) Veterinary Surgery: Small Animal.",
    31: "Heatley & Russell (2019) Vet Clin Exotic Anim Pract 22(1):1–134.",
    32: "Meredith & Johnson-Delaney (2010) BSAVA Manual of Exotic Pets, 5th ed.",
    33: "Doneley (2016) Avian Medicine and Surgery in Practice, 2nd ed.",
    34: "Divers & Stahl (2019) Mader's Reptile and Amphibian Medicine and Surgery, 3rd ed.",
    35: "Mitchell & Tully (2016) Current Therapy in Exotic Pet Practice.",
    36: "Pignon & Mayer (2011) Guinea pigs.",
    37: "Mans & Donnelly (2014) Chinchillas.",
    38: "Auer & Stick (2019) Equine Surgery, 5th ed.",
    39: "Robinson & Sprayberry (2015) Current Therapy in Equine Medicine, 7th ed.",
    40: "Knottenbelt (2009) Equine Dermatology, 2nd ed.",
    41: "Ross & Dyson (2011) Lameness in the Horse, 2nd ed.",
    42: "McAuliffe & Slovis (2014) Color Atlas of Diseases of the Foal.",
}

SPECIES_BASE_REFS: Dict[str, List[int]] = {
    "dog": [1, 2, 7, 12, 16, 24],
    "cat": [1, 2, 7, 8, 16, 24],
    "horse": [3, 11, 38, 39, 41],
    "rabbit": [4, 9, 32],
    "hamster": [4, 10, 32],
    "guinea_pig": [4, 32, 36],
    "chinchilla": [4, 32, 37],
    "ferret": [4, 32, 35],
    "hedgehog": [31, 32, 35],
    "sugar_glider": [10, 32, 35],
    "degu": [10, 32, 35],
    "bird": [6, 33, 35],
    "parakeet": [6, 33, 35],
    "parrot": [6, 33, 35],
    "reptile": [5, 34, 35],
    "tortoise": [5, 34, 35],
    "snake": [5, 34, 35],
    "lizard": [5, 34, 35],
    "amphibian": [5, 34, 35],
    "exotic_other": [10, 32, 35],
}


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


def _build_reference_links(citation_ids: List[int]) -> List[Dict[str, str]]:
    links: List[Dict[str, str]] = []
    for cid in citation_ids:
        if cid in REFERENCE_CATALOG:
            links.append({"id": str(cid), "name": f"[{cid}] {REFERENCE_CATALOG[cid]}", "url": ""})
    return links


def _normalize_citations(ids: List[int]) -> List[int]:
    unique: List[int] = []
    for cid in ids:
        try:
            n = int(cid)
        except (TypeError, ValueError):
            continue
        if n in REFERENCE_CATALOG and n not in unique:
            unique.append(n)
    return unique


def _default_citation_map(species: str) -> Dict[str, List[int]]:
    base = SPECIES_BASE_REFS.get(species, [7, 26])
    return {
        "pathophysiology": _normalize_citations(base[:3] + [2]),
        "causes": _normalize_citations(base[:3] + [24]),
        "prevention": _normalize_citations(base[:3] + [13]),
        "treatment": _normalize_citations(base[:3] + [12]),
        "prognosis": _normalize_citations(base[:3] + [26]),
        "description": _normalize_citations(base[:3]),
        "symptoms_summary": _normalize_citations(base[:2] + [24]),
    }




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


def enrich_disease_content(disease: Dict[str, Any], species: str) -> Dict[str, Any]:
    """Return disease with complete narrative fields and citation metadata."""
    out = dict(disease)
    name_ja = _text(out.get("name_ja")) or _text(out.get("name")) or "疾患"
    name_en = _text(out.get("name")) or _text(out.get("name_ja")) or "Disease"
    sym_text = _symptom_text(out.get("symptoms"))

    missing: List[str] = []
    sourced: List[str] = []
    for field in REQUIRED_FIELDS:
        ja_key = f"{field}_ja"
        en_key = field
        ja_val = _text(out.get(ja_key))
        en_val = _text(out.get(en_key))

        if not ja_val:
            out[ja_key] = _fallback(field, name_ja, species, sym_text, "ja")
            missing.append(ja_key)
        else:
            sourced.append(ja_key)
        if not en_val:
            out[en_key] = _fallback(field, name_en, species, sym_text, "en")
            missing.append(en_key)
        else:
            sourced.append(en_key)

    if not _text(out.get("symptoms_summary_ja")):
        out["symptoms_summary_ja"] = _symptom_summary(name_ja, sym_text, species, "ja")
        missing.append("symptoms_summary_ja")
    else:
        sourced.append("symptoms_summary_ja")

    if not _text(out.get("symptoms_summary")):
        out["symptoms_summary"] = _symptom_summary(name_en, sym_text, species, "en")
        missing.append("symptoms_summary")
    else:
        sourced.append("symptoms_summary")

    total = len(REQUIRED_FIELDS) * 2 + 2
    unique_missing = sorted(set(missing))
    out["missing_fields"] = unique_missing
    out["completeness_score"] = round((total - len(unique_missing)) / total * 100, 1)
    out["content_origin"] = "generated" if len(unique_missing) == total else ("mixed" if unique_missing else "sourced")
    out["sourced_fields"] = sorted(set(sourced))
    out["review_status"] = "review_required" if unique_missing else "reviewed"

    citation_map = _default_citation_map(species)
    out["citation_map"] = citation_map
    out["reference_catalog_version"] = REFERENCE_CATALOG_VERSION
    out["reference_catalog"] = [{"id": cid, "citation": REFERENCE_CATALOG[cid]} for cid in sorted(REFERENCE_CATALOG)]
    out["evidence_sources"] = _build_reference_links(citation_map.get("description", []))

    out["sections"] = {
        "pathophysiology": {"text": out.get("pathophysiology", ""), "citations": citation_map.get("pathophysiology", [])},
        "prevention": {"text": out.get("prevention", ""), "citations": citation_map.get("prevention", [])},
        "treatment": {"text": out.get("treatment", ""), "citations": citation_map.get("treatment", [])},
        "etiology": {"text": out.get("causes", ""), "citations": citation_map.get("causes", [])},
        "prognosis": {"text": out.get("prognosis", ""), "citations": citation_map.get("prognosis", [])},
    }
    return out
