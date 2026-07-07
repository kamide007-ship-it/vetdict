"""VetDict quality detectors — READ-ONLY.

Detectors flag suspected quality problems in the disease database. They NEVER
mutate any source (Python modules, JSON overlays, or the served SQLite). Each
detector returns a plain list of findings; the CLI (``run_detectors.py``)
serialises them to a JSON + Markdown report for human (veterinarian) review.

Detectors implemented here:

- T101  duplicate / split-family clustering  (name normalisation)
- T102  non-clinical entry detection         (research-model / human-medicine)
- T104  empty-treatment detection            (no dosage pattern present)

The served view of a species is loaded through the real application pipeline
(``api.species.<species>_diseases.DISEASES`` -> ``helpers.enrich_diseases`` ->
``helpers.dedupe_disease_list``) so that a detector sees exactly what a user
sees, including the JSON overlay and de-duplication. Horse is special-cased
because it uses ``DISEASE_DATABASE`` (dataclasses) instead of ``DISEASES``.
"""

from __future__ import annotations

import importlib
import re
import unicodedata
from dataclasses import asdict, is_dataclass
from typing import Any

# ---------------------------------------------------------------------------
# Loading the served view (read-only)
# ---------------------------------------------------------------------------


def _as_dict(rec: Any) -> dict[str, Any]:
    if is_dataclass(rec):
        return asdict(rec)
    if isinstance(rec, dict):
        return dict(rec)
    return dict(getattr(rec, "__dict__", {}))


def load_species_diseases(species: str) -> list[dict[str, Any]]:
    """Return the served disease list for *species* (read-only).

    Falls back gracefully: if enrichment/dedup helpers are unavailable the raw
    module list is returned. Never writes anything.
    """
    module_name = f"api.species.{species}_diseases"
    mod = importlib.import_module(module_name)

    raw = getattr(mod, "DISEASES", None)
    if raw is None:
        raw = getattr(mod, "DISEASE_DATABASE", [])
    records = [_as_dict(r) for r in raw]

    try:
        from api.species.helpers import dedupe_disease_list, enrich_diseases

        records = enrich_diseases([dict(r) for r in records], species)
        records = dedupe_disease_list(records)
        records = [_as_dict(r) for r in records]
    except Exception:  # pragma: no cover - defensive; report is still useful
        pass
    return records


# ---------------------------------------------------------------------------
# Name normalisation (shared by T101)
# ---------------------------------------------------------------------------

# Trailing/parenthetical qualifiers that do not change disease identity.
_PAREN_RE = re.compile(r"[（(][^）)]*[）)]")
_WS_RE = re.compile(r"\s+")
# Common orthographic variants -> canonical token.
_VARIANT_MAP = {
    "尾脱皮": "尾部脱皮",
    "バーバリング": "過剰毛繕い",
    "毛繕い": "毛繕い",
}


def normalize_name(name: str) -> str:
    """Normalise a disease name for duplicate clustering.

    NFKC-folds full/half width, lower-cases, strips parenthetical qualifiers and
    whitespace, and removes trailing punctuation. Intentionally conservative:
    it aims to collapse *orthographic* variants of the same name, not to merge
    genuinely distinct diseases.
    """
    if not name:
        return ""
    s = unicodedata.normalize("NFKC", str(name))
    s = _PAREN_RE.sub("", s)
    s = s.strip().lower()
    s = _WS_RE.sub("", s)
    s = s.strip("・,.-—–　 ")
    for a, b in _VARIANT_MAP.items():
        s = s.replace(a.lower(), b.lower())
    return s


# Base-stem extraction for "split-family" detection. A family is a set of
# entries whose names share a leading clinical stem (e.g. 糖尿病 -> 糖尿病 /
# 糖尿病性ケトアシドーシス / 糖尿病性白内障). This is a REVIEW signal, not a
# merge instruction — many families contain genuinely distinct entities.
_STEM_MIN_LEN = 2


def base_stem(name_ja: str) -> str:
    s = normalize_name(name_ja)
    # Cut at common derivational suffixes that spawn split families.
    for sep in ("性", "症性", "による", "に伴う", "続発", "合併"):
        idx = s.find(sep)
        if idx >= _STEM_MIN_LEN:
            return s[:idx]
    return s


# ---------------------------------------------------------------------------
# T101 — duplicate / split-family detector
# ---------------------------------------------------------------------------


def detect_duplicates(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Cluster records by normalised name (exact dups) and by base stem (split
    families). Read-only. Returns structured findings."""
    exact: dict[str, list[dict[str, Any]]] = {}
    for i, r in enumerate(records):
        keys = {normalize_name(r.get("name_ja", "")), normalize_name(r.get("name", ""))}
        keys.discard("")
        for k in keys:
            exact.setdefault(k, []).append({"idx": i, "name": r.get("name"), "name_ja": r.get("name_ja")})

    exact_dups = [
        {"key": k, "count": len(v), "members": v}
        for k, v in sorted(exact.items(), key=lambda kv: -len(kv[1]))
        if len(v) > 1
    ]

    families: dict[str, list[dict[str, Any]]] = {}
    for i, r in enumerate(records):
        stem = base_stem(r.get("name_ja", ""))
        if len(stem) >= _STEM_MIN_LEN:
            families.setdefault(stem, []).append({"idx": i, "name_ja": r.get("name_ja"), "name": r.get("name")})

    split_families = [
        {"stem": k, "count": len(v), "members": v}
        for k, v in sorted(families.items(), key=lambda kv: -len(kv[1]))
        if len(v) >= 3
    ]

    return {
        "exact_duplicate_clusters": exact_dups,
        "split_family_clusters": split_families,
        "n_exact_duplicate_records": sum(c["count"] for c in exact_dups),
        "n_split_family_clusters": len(split_families),
    }


# ---------------------------------------------------------------------------
# T102 — non-clinical / research-model / human-medicine detector
# ---------------------------------------------------------------------------

# Each entry: (label, regex). Matched against name / name_ja / description(_ja).
# Kept as a small, auditable dictionary — expandable per species review.
_NONCLINICAL_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("research_model_alzheimer", re.compile(r"アルツハイマー|alzheimer|amyloid|βアミロイド|アミロイド斑", re.I)),
    ("research_model_neurodegen", re.compile(r"パーキンソン|parkinson|神経変性.*モデル|タウ病理", re.I)),
    ("research_model_generic", re.compile(r"研究モデル|動物モデル|疾患モデル|実験的誘発|induced model|research model", re.I)),
    ("human_transplant_footulcer", re.compile(r"糖尿病性足潰瘍|足壊疽|diabetic foot", re.I)),
    ("human_transplant_retinopathy", re.compile(r"糖尿病性網膜症|diabetic retinopathy", re.I)),
    ("human_transplant_nephropathy", re.compile(r"糖尿病性腎症|diabetic nephropathy", re.I)),
    ("human_transplant_neuropathy_dm", re.compile(r"糖尿病性(多発)?神経(障害|症)|diabetic (poly)?neuropathy", re.I)),
    ("human_transplant_metabolic", re.compile(r"メタボリックシンドローム|metabolic syndrome", re.I)),
    ("human_transplant_atherosclerosis", re.compile(r"アテローム性動脈硬化|atherosclerosis", re.I)),
]


def detect_nonclinical(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Flag records that look like research-model or human-medicine transplants
    rather than genuine spontaneous companion-animal diseases. Read-only."""
    findings: list[dict[str, Any]] = []
    for i, r in enumerate(records):
        haystack = " ".join(
            str(r.get(f, "") or "")
            for f in ("name", "name_ja", "description", "description_ja")
        )
        hits = [label for label, rx in _NONCLINICAL_PATTERNS if rx.search(haystack)]
        if hits:
            findings.append(
                {
                    "idx": i,
                    "name": r.get("name"),
                    "name_ja": r.get("name_ja"),
                    "flags": hits,
                }
            )
    return {"flagged": findings, "n_flagged": len(findings)}


# ---------------------------------------------------------------------------
# T104 — empty-treatment detector (no dosage pattern)
# ---------------------------------------------------------------------------

# Dosage / route / frequency tokens that indicate a real, actionable protocol.
_DOSE_RE = re.compile(
    r"""
    \d+\s*(?:\.\d+)?\s*(?:mg|µg|mcg|ug|g|iu|ml|l)\s*/\s*(?:kg|m2|m²|animal|羽|頭|匹|回|日|day)  # mg/kg etc.
    | \d+\s*(?:mg|µg|mcg|ug|iu|ml)\b            # bare mg / IU / mL amount
    | \bq\s?\d+\s?h\b                            # q12h dosing interval
    | \b(?:sid|bid|tid|qid|q\d+h)\b              # frequency abbreviations
    | \b(?:po|sc|iv|im|ip|io)\b                  # routes
    | \d+\s*%                                     # percentage solutions/dips
    """,
    re.I | re.X,
)


def _has_dose(text: str) -> bool:
    return bool(_DOSE_RE.search(text or ""))


def detect_empty_treatment(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Flag records whose treatment fields contain no dosage/route/frequency
    pattern — i.e. 'headings only', no actionable protocol. Read-only.

    Reports separately for JA (primary audience) and EN so a record with a
    good EN protocol but empty JA is still surfaced."""
    findings: list[dict[str, Any]] = []
    for i, r in enumerate(records):
        tx_ja = str(r.get("treatment_ja", "") or "")
        tx_en = str(r.get("treatment", "") or "")
        ja_dose = _has_dose(tx_ja)
        en_dose = _has_dose(tx_en)
        if not ja_dose:
            findings.append(
                {
                    "idx": i,
                    "name": r.get("name"),
                    "name_ja": r.get("name_ja"),
                    "ja_len": len(tx_ja),
                    "ja_has_dose": ja_dose,
                    "en_has_dose": en_dose,
                    "severity": "empty" if not tx_ja.strip() else ("no_dose" if not en_dose else "no_dose_ja_only"),
                }
            )
    return {
        "flagged": findings,
        "n_flagged": len(findings),
        "n_ja_empty": sum(1 for f in findings if f["severity"] == "empty"),
        "n_no_dose_either": sum(1 for f in findings if f["severity"] == "no_dose"),
    }


def run_all(species: str) -> dict[str, Any]:
    records = load_species_diseases(species)
    return {
        "species": species,
        "n_records": len(records),
        "T101_duplicates": detect_duplicates(records),
        "T102_nonclinical": detect_nonclinical(records),
        "T104_empty_treatment": detect_empty_treatment(records),
    }
