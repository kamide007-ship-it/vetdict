#!/usr/bin/env python3
"""Regression tests for horse-disease Japanese clinical-field routing.

Guards two defects fixed together:

1. ``migrate_equine`` used to treat a bare ``treatment_protocol`` string as
   English and route it into the English column, leaving ``treatment_ja`` (and
   the never-set ``causes_ja`` / ``pathophysiology_ja``) empty. For the ~18
   module-only horse diseases that the JSON overlay never touches, the
   Japanese-facing site therefore showed a blank treatment / cause / prognosis.

2. Those same module-only records carried no ``etiology`` / ``pathophysiology``,
   so they fell back to a generic "遺伝的素因・体型・運動負荷…" template. They now
   carry curated, disease-specific text.
"""

from __future__ import annotations

import re
import sqlite3
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from api.database import get_connection, init_db  # noqa: E402
from scripts.migrate_to_sqlite import migrate_equine  # noqa: E402

_CJK = re.compile(r"[぀-ヿ一-鿿]")
# The generic fallback markers the curated text must replace.
_GENERIC_CAUSES = "の原因には、遺伝的素因、体型、"
_GENERIC_PATHO = "は馬の組織に病理学的変化を引き起こす疾患である"

# Module-only horse diseases whose Japanese clinical fields used to be empty.
_MODULE_ONLY = [
    "Equine Squamous Gastric Disease (ESGD)",
    "Equine Glandular Gastric Disease (EGGD)",
    "Right Dorsal Colitis (RDC)",
    "Colitis-X (Peracute Idiopathic Colitis)",
    "Foal Gastric Ulcer Syndrome (FGUS)",
    "Postpartum Hemorrhage / Uterine Artery Rupture",
    "Shaker Foal Syndrome (Toxico-Infectious Botulism)",
]


def _migrated_horse_rows() -> dict[str, sqlite3.Row]:
    """Run migrate_equine into a throwaway DB and return {name: row}."""
    with tempfile.TemporaryDirectory() as tmp:
        db_path = str(Path(tmp) / "horse_test.db")
        init_db(db_path)
        with get_connection(db_path) as conn:  # get_connection is a @contextmanager
            migrate_equine(conn)
            rows = conn.execute("SELECT * FROM diseases WHERE species='horse'").fetchall()
    return {r["name"]: r for r in rows}


def test_module_only_horse_diseases_have_japanese_clinical_fields():
    rows = _migrated_horse_rows()
    for name in _MODULE_ONLY:
        assert name in rows, f"missing horse disease: {name}"
        row = rows[name]
        for field in ("treatment_ja", "causes_ja", "prognosis_ja", "pathophysiology_ja", "prevention_ja"):
            val = (row[field] or "").strip()
            assert val, f"{name}: {field} is empty (Japanese-facing site would show a blank)"
            assert _CJK.search(val), f"{name}: {field} contains no Japanese text"


def test_curated_etiology_pathophysiology_is_not_generic_template():
    rows = _migrated_horse_rows()
    for name in _MODULE_ONLY:
        row = rows[name]
        assert _GENERIC_CAUSES not in (row["causes_ja"] or ""), f"{name}: causes_ja still uses the generic template"
        assert _GENERIC_PATHO not in (row["pathophysiology_ja"] or ""), (
            f"{name}: pathophysiology_ja still uses the generic template"
        )


def test_esgd_japanese_treatment_matches_module_content():
    """The rich Japanese treatment_protocol must reach treatment_ja verbatim."""
    rows = _migrated_horse_rows()
    esgd = rows["Equine Squamous Gastric Disease (ESGD)"]
    assert "オメプラゾール" in esgd["treatment_ja"], "ESGD treatment_ja lost its omeprazole protocol"
    assert "ECEIM" in esgd["treatment_ja"], "ESGD treatment_ja lost its ECEIM grading detail"
