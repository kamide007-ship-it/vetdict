"""Disease metadata auto-enrichment.

Many disease entries in species DBs lack `age_predisposition` and
`onset_pattern` metadata. This module infers conservative defaults from
disease names and urgency markers so the diagnostic matcher's age/onset
factors can fire on more entries without manual data backfill.

Inferences are deliberately HIGH-CONFIDENCE only — ambiguous cases are
left untouched. Apply once at module load (idempotent: skips entries
that already have the field set).
"""

from __future__ import annotations

import re
from typing import Iterable

# --- Pattern tables ---------------------------------------------------------

_AGE_YOUNG_PATTERNS = re.compile(
    r"\b("
    r"neonatal|puppy|kitten|fading\s+puppy|fading\s+kitten|juvenile|young|"
    r"foal|chick|hatchling|nursing|pediatric|"
    r"congenital|developmental|hereditary|inherited|"
    r"persistent\s+(ductus|right|left|fetal)|"
    r"patent\s+ductus|umbilical|portosystemic\s+shunt"
    r")\b",
    re.IGNORECASE,
)

_AGE_SENIOR_PATTERNS = re.compile(
    r"\b("
    r"senior|geriatric|elderly|age-related|"
    r"cognitive\s+dysfunction|degenerative\s+myelopathy|"
    r"old\s+dog|old\s+cat|old-age|"
    r"chronic\s+kidney\s+disease|chronic\s+renal|cushing|"
    r"prostatic\s+hyperplasia|laryngeal\s+paralysis|"
    r"intervertebral\s+disc"
    r")\b",
    re.IGNORECASE,
)

_ONSET_ACUTE_PATTERNS = re.compile(
    r"\b("
    r"acute|sudden|envenomation|snakebite|anaphylaxis|"
    r"torsion|volvulus|rupture|perforation|"
    r"obstruction|impaction|"
    r"trauma|laceration|fracture|fractures?|"
    r"shock|sepsis|sirs|cardiac\s+arrest|"
    r"hbc|hit\s+by\s+car|gdv|bloat|"
    r"toxicosis|toxicity|poisoning|envenom|"
    r"heatstroke|heat\s+stroke|electrocution|drowning"
    r")\b",
    re.IGNORECASE,
)

_ONSET_CHRONIC_PATTERNS = re.compile(
    r"\b("
    r"chronic|persistent|long-term|recurrent|recurring|"
    r"degenerative|progressive|"
    r"hyperplasia|fibrosis|sclerosis|"
    r"chronic\s+kidney|chronic\s+hepatitis|chronic\s+enteropathy|"
    r"cushing|atopic|"
    r"osteoarthritis|arthritis"
    r")\b",
    re.IGNORECASE,
)


def _infer_age_predisposition(name: str, name_ja: str = "") -> set[str] | None:
    """Return inferred age set or None if undecidable."""
    text = f"{name} {name_ja}"
    if _AGE_YOUNG_PATTERNS.search(text):
        return {"young"}
    if _AGE_SENIOR_PATTERNS.search(text):
        return {"senior"}
    return None


def _infer_onset_pattern(name: str, urgency: str = "", name_ja: str = "") -> set[str] | None:
    """Return inferred onset pattern set or None if undecidable.

    Combines name-pattern matching with the urgency hint:
      - urgency="emergency" strongly correlates with acute onset
      - explicit "chronic" keywords override
    """
    text = f"{name} {name_ja}"
    is_chronic = bool(_ONSET_CHRONIC_PATTERNS.search(text))
    is_acute = bool(_ONSET_ACUTE_PATTERNS.search(text)) or (urgency == "emergency")
    # Prefer the more specific signal: if both, return both
    if is_chronic and is_acute:
        return {"acute", "chronic"}
    if is_chronic:
        return {"chronic"}
    if is_acute:
        return {"acute"}
    return None


def enrich_diseases_inplace(diseases: Iterable[dict]) -> dict[str, int]:
    """Mutate disease dicts in-place, adding inferred metadata where missing.

    Returns a stats dict: {age_added, onset_added, total}.
    Skips entries that already have the field populated (idempotent).
    """
    n_age = 0
    n_onset = 0
    total = 0
    for d in diseases:
        if not isinstance(d, dict):
            continue
        total += 1
        name = d.get("name", "") or ""
        name_ja = d.get("name_ja", "") or ""
        urgency = d.get("urgency", "") or ""

        if not d.get("age_predisposition"):
            inferred = _infer_age_predisposition(name, name_ja)
            if inferred is not None:
                d["age_predisposition"] = inferred
                n_age += 1

        if not d.get("onset_pattern"):
            inferred = _infer_onset_pattern(name, urgency, name_ja)
            if inferred is not None:
                d["onset_pattern"] = inferred
                n_onset += 1

    return {"age_added": n_age, "onset_added": n_onset, "total": total}
