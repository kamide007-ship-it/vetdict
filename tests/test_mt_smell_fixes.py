"""T109 — SAFE machine-translation-smell fixes are applied to sources; the
context-dependent 'review' terms are left untouched for veterinarian judgement."""

from __future__ import annotations

from pathlib import Path

import scripts.quality.apply_mt_smell as mt
import scripts.quality.detect as detect

ROOT = Path(__file__).resolve().parents[1]
_SOURCES = [
    ROOT / "diseases_all_species.json",
    ROOT / "api" / "data" / "supplementary_diseases.json",
    *sorted((ROOT / "api" / "species").glob("*_diseases.py")),
]


def _count(term: str) -> int:
    return sum(p.read_text(encoding="utf-8").count(term) for p in _SOURCES if p.exists())


def test_safe_terms_are_eliminated_from_sources():
    for entry in detect._MT_LEXICON:
        if entry["category"] == "safe":
            assert _count(entry["term"]) == 0, f"safe MT term still present: {entry['term']}"


def test_apply_is_idempotent_dry_run_finds_nothing():
    # After the fixes are committed, the applier finds no further safe changes.
    for term, _suggest in mt._safe_pairs():
        assert _count(term) == 0


def test_review_terms_are_not_auto_replaced():
    # Context-dependent terms must NOT be blindly stripped (they may be valid,
    # e.g. 遺伝学的検査). At least one review term should still exist in sources.
    assert any(_count(e["term"]) > 0 for e in detect._MT_LEXICON if e["category"] != "safe")
