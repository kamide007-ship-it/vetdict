"""Fail-closed intake for formulary-sourced drug dosing.

The drug dictionary has 481 (drug, species) entries that carry a dose but no
route or no frequency, and 476 of them cannot be closed from data the record
already holds — the value has to come off a formulary shelf (Plumb's, Carpenter)
or out of a paper. This module is where those vet-entered values land.

The gate is structural, not procedural:

* an entry is served **only** when ``review_status == "published"`` **and** it
  carries a non-empty ``source``;
* anything still ``draft``, or published without a source, is ignored;
* so there is no code path that can put an unsourced dose in front of a vet, and
  "forgot to review it" fails safe instead of shipping.

This mirrors ``api/species/treatment_overrides.py``, which gates disease
treatment dosing the same way.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

_OVERRIDE_DIR = Path(__file__).resolve().parent / "data" / "dosage_overrides"

# Fields a published entry must fill in for it to reach the site.
_REQUIRED = ("dosage", "source")


def _is_publishable(entry: dict[str, Any]) -> bool:
    if entry.get("review_status") != "published":
        return False
    return all(str(entry.get(field) or "").strip() for field in _REQUIRED)


def load_published_overrides() -> dict[tuple[str, str], dict[str, Any]]:
    """Return {(drug_id, species): entry} for vet-approved, sourced dosing only."""
    published: dict[tuple[str, str], dict[str, Any]] = {}
    if not _OVERRIDE_DIR.is_dir():
        return published
    for path in sorted(_OVERRIDE_DIR.glob("*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            logger.warning("could not read dosage overrides: %s", path)
            continue
        for entry in payload.get("entries") or []:
            if not isinstance(entry, dict) or not _is_publishable(entry):
                continue
            drug_id, species = entry.get("drug_id"), entry.get("species")
            if drug_id and species:
                published[(str(drug_id), str(species))] = entry
    return published


def apply_dosage_overrides(drugs: list[dict[str, Any]]) -> int:
    """Apply published dosing to ``drugs`` in place. Returns the number applied.

    Only the dose text and its provenance are written; ``safe`` is never changed
    here, so an override can never silently flip a contraindication.
    """
    published = load_published_overrides()
    if not published:
        return 0
    applied = 0
    for drug in drugs:
        drug_id = drug.get("id")
        if not drug_id:
            continue
        for species, info in (drug.get("species_info") or {}).items():
            entry = published.get((str(drug_id), str(species)))
            if not isinstance(info, dict) or entry is None:
                continue
            info["dosage"] = entry["dosage"]
            if entry.get("dosage_ja"):
                info["dosage_ja"] = entry["dosage_ja"]
            info["dosage_source"] = entry["source"]
            if entry.get("evidence_grade"):
                info["evidence_grade"] = entry["evidence_grade"]
            applied += 1
    return applied
