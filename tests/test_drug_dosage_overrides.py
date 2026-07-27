"""The formulary intake for drug dosing must be fail-closed.

481 (drug, species) entries are missing a route or a frequency, and 79% of them
cannot be closed from PubMed — the value has to be entered from a formulary by a
vet. The risk that matters is a half-finished or unsourced row reaching a
clinician as if it were established dosing, so the gate is asserted here rather
than left to process: a row is served only when it is BOTH marked published AND
carries a source.
"""

from __future__ import annotations

import json
from pathlib import Path

from api.drug_dosage_overrides import _is_publishable, apply_dosage_overrides, load_published_overrides

WORKLIST_DIR = Path(__file__).resolve().parent.parent / "api" / "data" / "dosage_overrides"


def test_draft_rows_are_never_publishable():
    assert not _is_publishable({"review_status": "draft", "dosage": "5 mg/kg PO q12h", "source": "Plumb's 10th"})


def test_published_without_a_source_is_never_publishable():
    """ "Approved" is not enough — an unsourced dose must not ship."""
    assert not _is_publishable({"review_status": "published", "dosage": "5 mg/kg PO q12h", "source": ""})
    assert not _is_publishable({"review_status": "published", "dosage": "5 mg/kg PO q12h"})


def test_published_without_a_dose_is_never_publishable():
    assert not _is_publishable({"review_status": "published", "dosage": "", "source": "Plumb's 10th"})


def test_fully_reviewed_and_sourced_row_is_publishable():
    assert _is_publishable(
        {"review_status": "published", "dosage": "5 mg/kg PO q12h", "source": "Carpenter 6th ed, p.412"}
    )


def test_generated_worklist_ships_nothing_yet():
    """The generated sheets are all drafts, so no dose is live until a vet fills them."""
    assert WORKLIST_DIR.is_dir(), "worklist sheets were not generated"
    assert load_published_overrides() == {}


def test_worklist_rows_carry_the_fields_a_vet_must_fill():
    sheets = sorted(WORKLIST_DIR.glob("*.json"))
    assert sheets, "no worklist sheets found"
    for sheet in sheets:
        payload = json.loads(sheet.read_text(encoding="utf-8"))
        for entry in payload["entries"]:
            for field in ("drug_id", "species", "current_dosage", "missing", "dosage", "source", "review_status"):
                assert field in entry, f"{sheet.name}: entry missing {field}"
            assert entry["review_status"] == "draft"
            assert entry["missing"], "a gap row must say what is missing"


def test_apply_is_a_no_op_while_everything_is_draft():
    drugs = [{"id": "ivermectin", "species_info": {"horse": {"dosage": "200 mcg/kg PO", "safe": True}}}]
    assert apply_dosage_overrides(drugs) == 0
    assert drugs[0]["species_info"]["horse"]["dosage"] == "200 mcg/kg PO"


def test_apply_writes_dose_and_provenance_but_never_touches_safe():
    """An override may correct dosing; it must not be able to flip a contraindication."""
    drugs = [{"id": "d1", "species_info": {"cat": {"dosage": "old", "safe": False}}}]
    published = {
        ("d1", "cat"): {
            "drug_id": "d1",
            "species": "cat",
            "dosage": "5 mg/kg PO q12h",
            "source": "Plumb's 10th",
            "evidence_grade": "C",
            "review_status": "published",
        }
    }
    import api.drug_dosage_overrides as mod

    original = mod.load_published_overrides
    mod.load_published_overrides = lambda: published
    try:
        assert mod.apply_dosage_overrides(drugs) == 1
    finally:
        mod.load_published_overrides = original

    entry = drugs[0]["species_info"]["cat"]
    assert entry["dosage"] == "5 mg/kg PO q12h"
    assert entry["dosage_source"] == "Plumb's 10th"
    assert entry["evidence_grade"] == "C"
    assert entry["safe"] is False, "an override must not be able to un-contraindicate a drug"
