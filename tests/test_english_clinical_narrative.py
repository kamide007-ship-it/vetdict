#!/usr/bin/env python3
"""Regression tests for English clinical narrative on Japanese-first records.

A subset of disease records were authored with curated *Japanese* clinical text
only, so their English narrative columns (causes / pathophysiology /
clinical_signs / prevention / prognosis) fell back to the Japanese string. An
English viewer of the disease browser or a differential-diagnosis result
therefore saw Japanese text.

Two fixes are guarded here:

1. Horse records get faithful English via ``*_en`` companion fields on the
   ``Disease`` dataclass (``equine_english_overlay``), preferred by the migrate
   step, ``health_checker`` and ``species_analyzer.analyze_horse``.
2. Fish / dog / exotic dict records get English via ``disease_english_overlay``
   applied at module import.

The Japanese ``*_ja`` companion fields must be preserved unchanged, and dosing
(``treatment``) is intentionally left Japanese pending human translation.
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
from api.species.disease_english_overlay import (  # noqa: E402
    DISEASE_ENGLISH,
    apply_english_overlay,
)
from api.species.equine_english_overlay import HORSE_ENGLISH  # noqa: E402
from scripts.migrate_to_sqlite import (  # noqa: E402
    migrate_equine,
    migrate_species_diseases,
)

_CJK = re.compile(r"[぀-ヿ一-鿿]")

# Horse Japanese-first records that now carry English narrative.
_HORSE_TRANSLATED = [
    "Equine Squamous Gastric Disease (ESGD)",
    "Equine Glandular Gastric Disease (EGGD)",
    "Right Dorsal Colitis (RDC)",
    "Colitis-X (Peracute Idiopathic Colitis)",
    "Foal Gastric Ulcer Syndrome (FGUS)",
    "Postpartum Hemorrhage / Uterine Artery Rupture",
    "Shaker Foal Syndrome (Toxico-Infectious Botulism)",
    "Premature Placental Separation (Red Bag Delivery)",
    "Atypical Myopathy (Sycamore Maple Seedling Toxicosis)",
    "Early Embryonic Death (EED) / Early Pregnancy Loss",
]

_EN_NARRATIVE = ("causes", "prevention", "prognosis", "clinical_signs", "pathophysiology")


def _migrated_horse_rows() -> dict[str, sqlite3.Row]:
    with tempfile.TemporaryDirectory() as tmp:
        db_path = str(Path(tmp) / "horse_test.db")
        init_db(db_path)
        with get_connection(db_path) as conn:
            migrate_equine(conn)
            rows = conn.execute("SELECT * FROM diseases WHERE species='horse'").fetchall()
    return {r["name"]: r for r in rows}


def _migrated_species_rows(species: str, module_path: str) -> dict[str, sqlite3.Row]:
    with tempfile.TemporaryDirectory() as tmp:
        db_path = str(Path(tmp) / f"{species}_test.db")
        init_db(db_path)
        with get_connection(db_path) as conn:
            migrate_species_diseases(conn, species, module_path)
            rows = conn.execute("SELECT * FROM diseases WHERE species=?", (species,)).fetchall()
    return {r["name"]: r for r in rows}


# --------------------------------------------------------------------------- horse


def test_horse_translated_english_narrative_has_no_japanese():
    rows = _migrated_horse_rows()
    for name in _HORSE_TRANSLATED:
        assert name in rows, f"missing horse disease: {name}"
        row = rows[name]
        for field in _EN_NARRATIVE:
            val = (row[field] or "").strip()
            assert val, f"{name}: English {field} is empty"
            assert not _CJK.search(val), f"{name}: English {field} still contains Japanese text"


def test_horse_japanese_narrative_is_preserved():
    """Providing English must not erase the Japanese companion columns."""
    rows = _migrated_horse_rows()
    for name in _HORSE_TRANSLATED:
        row = rows[name]
        for field in ("causes_ja", "prevention_ja", "prognosis_ja", "pathophysiology_ja"):
            val = (row[field] or "").strip()
            assert val and _CJK.search(val), f"{name}: {field} lost its Japanese text"


def test_horse_eggd_english_is_clinically_specific():
    rows = _migrated_horse_rows()
    eggd = rows["Equine Glandular Gastric Disease (EGGD)"]
    assert "sucralfate" in eggd["prevention"].lower() or "mucosal" in eggd["pathophysiology"].lower()
    assert "EGGD" in eggd["prognosis"] or "55-70%" in eggd["prognosis"]


def test_horse_treatment_remains_japanese_by_design():
    """Dosing text is intentionally not machine-translated for patient safety."""
    rows = _migrated_horse_rows()
    esgd = rows["Equine Squamous Gastric Disease (ESGD)"]
    assert _CJK.search(esgd["treatment_ja"] or ""), "ESGD treatment_ja should stay Japanese"


def test_horse_overlay_covers_expected_records():
    from api.species.equine_diseases import DISEASE_DATABASE

    ids_with_en = {d.id for d in DISEASE_DATABASE if d.etiology_en}
    assert ids_with_en == set(HORSE_ENGLISH.keys())
    # Every overlay entry must actually attach (id must exist in the database).
    db_ids = {d.id for d in DISEASE_DATABASE}
    for overlay_id in HORSE_ENGLISH:
        assert overlay_id in db_ids, f"overlay id not in horse database: {overlay_id}"


# ---------------------------------------------------------------- fish / dog / exotic


def test_fish_prevention_english_has_no_japanese():
    rows = _migrated_species_rows("fish", "api.species.fish_diseases")
    columnaris = rows["Columnaris Disease"]
    assert not _CJK.search(columnaris["prevention"] or ""), "fish prevention still Japanese"
    assert _CJK.search(columnaris["prevention_ja"] or ""), "fish prevention_ja lost Japanese"
    # Every fish overlay target must be Japanese-free in its English column.
    for (species, name), fields in DISEASE_ENGLISH.items():
        if species != "fish":
            continue
        row = rows.get(name)
        assert row is not None, f"missing fish disease: {name}"
        for field in fields:
            assert not _CJK.search(row[field] or ""), f"fish {name}: {field} still Japanese"


def test_dog_neonatal_english_has_no_japanese_and_preserves_ja():
    rows = _migrated_species_rows("dog", "api.species.dog_diseases")
    for name in ("Fading Puppy Syndrome", "Neonatal Puppy Mortality / Perinatal Death"):
        row = rows[name]
        for field in ("causes", "pathophysiology", "prevention", "prognosis"):
            assert not _CJK.search(row[field] or ""), f"dog {name}: {field} still Japanese"
            assert _CJK.search(row[field + "_ja"] or ""), f"dog {name}: {field}_ja lost Japanese"


def test_overlay_only_replaces_japanese_fields_and_is_idempotent():
    """apply_english_overlay must skip fields that already hold English."""
    ja = "水質管理の徹底、過密飼育回避。"
    en = "Rigorous water-quality management, avoidance of overcrowding, stress reduction and prevention of skin injury."
    records = [{"name": "Columnaris Disease", "prevention": ja, "prevention_ja": ja}]
    n = apply_english_overlay(records, "fish")
    assert n == 1
    assert not _CJK.search(records[0]["prevention"])
    assert records[0]["prevention_ja"] == ja  # untouched
    # Second run is a no-op (English already present).
    assert apply_english_overlay(records, "fish") == 0
    # A record already in English is never overwritten.
    already = [{"name": "Columnaris Disease", "prevention": en, "prevention_ja": ja}]
    assert apply_english_overlay(already, "fish") == 0
    assert already[0]["prevention"] == en
