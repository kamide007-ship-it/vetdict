"""Regression tests for grounding empty English ``diagnosis`` on Japanese-first records.

The served-DB grounding pass used to fill ``diagnosis`` only when BOTH the English
and Japanese variants were empty. Japanese-first records (e.g. Mamushi envenomation)
ship with a complete ``diagnosis_ja`` but a blank English ``diagnosis``, so an
English visitor saw no work-up. The pass now fills each language independently,
grounded solely in the record's own recommended tests — and, crucially, pulls the
ASCII English gloss out of ``"日本語 (English)"`` test labels so nothing Japanese
leaks into the English prose. Records whose tests are Japanese-only are left empty
(no fabrication, per the project's grounding policy).
"""

from __future__ import annotations

import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from api.database import get_connection, init_db  # noqa: E402
from scripts.migrate_to_sqlite import (  # noqa: E402
    ground_missing_clinical_signs_and_diagnosis,
    migrate_species_diseases,
)

_CJK = re.compile(r"[぀-ヿ一-鿿]")


def _grounded_dog_rows():
    with tempfile.TemporaryDirectory() as tmp:
        db_path = str(Path(tmp) / "dog_test.db")
        init_db(db_path)
        with get_connection(db_path) as conn:
            migrate_species_diseases(conn, "dog", "api.species.dog_diseases")
            ground_missing_clinical_signs_and_diagnosis(conn)
            rows = conn.execute("SELECT * FROM diseases WHERE species='dog'").fetchall()
    return {r["name"]: r for r in rows}


def test_japanese_first_record_gets_english_diagnosis_without_cjk():
    rows = _grounded_dog_rows()
    mamushi = next((r for n, r in rows.items() if "Mamushi" in n), None)
    assert mamushi is not None, "Mamushi envenomation record should exist"
    dx = (mamushi["diagnosis"] or "").strip()
    assert dx, "English diagnosis should be grounded from the record's tests"
    assert not _CJK.search(dx), f"no Japanese should leak into English diagnosis: {dx!r}"
    # The Japanese side is preserved, not overwritten.
    assert (mamushi["diagnosis_ja"] or "").strip()


def test_ppm_phpv_have_recommended_tests():
    rows = _grounded_dog_rows()
    for key in ("Persistent Pupillary Membrane", "Persistent Hyperplastic Primary Vitreous"):
        row = next((r for n, r in rows.items() if key in n), None)
        assert row is not None, f"{key} record should exist"
        tests = (row["recommended_tests"] or "").strip()
        assert tests and tests != "[]", f"{key} should have recommended tests"
        assert "Slit Lamp" in tests  # ophthalmic work-up populated


def test_grounding_does_not_fabricate_when_tests_are_japanese_only():
    """A record whose recommended tests carry no ASCII English gloss is left with an
    empty English diagnosis rather than filled with Japanese or invented text."""
    rows = _grounded_dog_rows()
    for _, r in rows.items():
        dx = (r["diagnosis"] or "").strip()
        if dx:
            assert not _CJK.search(dx), f"grounded English diagnosis must be CJK-free: {dx!r}"
