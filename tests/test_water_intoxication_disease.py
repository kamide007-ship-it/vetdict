#!/usr/bin/env python3
"""Regression test for the canine Water Intoxication entry.

Water intoxication (acute dilutional hyponatremia) is a recognised, potentially
fatal emergency in dogs — commonly after biting/retrieving water while swimming
or dock-diving, or playing with hoses/sprinklers — yet the database previously
had no entry for it (dogs did not even carry a generic hyponatremia record).

The single most important clinical caveat is that sodium must be corrected
SLOWLY (over-rapid correction causes osmotic demyelination), so this test also
guards that safety note against accidental loss.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import pytest

from api.species.dog_diseases import DISEASES, VALID_SYMPTOMS


@pytest.fixture(scope="module")
def water_intoxication():
    matches = [d for d in DISEASES if "Water Intoxication" in d.get("name", "")]
    assert len(matches) == 1, "expected exactly one canine Water Intoxication entry"
    return matches[0]


def test_entry_is_present_and_bilingual(water_intoxication):
    d = water_intoxication
    assert d["name_ja"] and "水中毒" in d["name_ja"]
    assert d["urgency"] == "emergency"
    # Every symptom must be a real symptom id the checker knows about.
    assert d["symptoms"], "must list symptoms so the checker can surface it"
    assert not (set(d["symptoms"]) - set(VALID_SYMPTOMS)), "unknown symptom id"


def test_pathophysiology_names_the_mechanism(water_intoxication):
    d = water_intoxication
    for field in ("pathophysiology_ja", "causes_ja", "treatment_ja"):
        assert d[field].strip(), f"{field} must not be empty"
    # Dilutional hyponatremia → cerebral edema, not some generic template.
    assert "ナトリウム" in d["pathophysiology_ja"]
    assert "脳浮腫" in d["pathophysiology_ja"]


def test_treatment_keeps_the_slow_correction_safety_caveat(water_intoxication):
    """Over-rapid sodium correction is the classic iatrogenic killer here."""
    tx = water_intoxication["treatment_ja"]
    assert "0.5 mEq/L" in tx, "must keep the ≤0.5 mEq/L/hour correction-rate limit"
    assert "浸透圧性脱髄" in tx, "must warn about osmotic demyelination"
