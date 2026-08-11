"""Regression tests for collision-safe served-DB id allocation.

A disease newly inserted into a module list takes the list position an older
entry held when the id-lock sidecar (api/data/id_locks/<species>.json) was
generated; both entries then resolve to the same id and INSERT OR REPLACE
silently drops one row from the served DB. Found 2026-08: three appended
diseases (degu Elodontoma, guinea pig Intestinal Torsion, amphibian Parasitic
Dermatitis) vanished this way. The allocator must keep locked ids
authoritative and deterministically bump unlocked entries off taken ids.
"""

import sqlite3
from pathlib import Path

import pytest

SERVED_DB = Path(__file__).resolve().parent.parent / "instance" / "vetdict.db"


def test_unlocked_entry_bumps_off_locked_id(monkeypatch):
    import api.species.id_locks as id_locks
    from scripts.migrate_to_sqlite import _resolve_collision_free_ids

    new_entry = {"name": "New Disease", "name_ja": "新疾患"}
    locked_entry = {"name": "Old Disease", "name_ja": "既存疾患"}
    diseases = [new_entry, locked_entry]
    # new_entry sits at index 0; locked_entry is frozen to test_0000 (its
    # position before new_entry was inserted above it).
    orig_index = {id(new_entry): 0, id(locked_entry): 1}

    monkeypatch.setattr(
        id_locks,
        "locked_id_for",
        lambda sp, e: "test_0000" if e is locked_entry else None,
    )
    resolved = _resolve_collision_free_ids("test", diseases, orig_index)
    assert resolved[id(locked_entry)] == "test_0000"  # lock is authoritative
    assert resolved[id(new_entry)] == "test_0001"  # bumped, not clobbered
    assert len(set(resolved.values())) == 2


def test_explicit_ids_and_no_locks_preserve_positions(monkeypatch):
    import api.species.id_locks as id_locks
    from scripts.migrate_to_sqlite import _resolve_collision_free_ids

    a = {"name": "A", "name_ja": "あ"}
    b = {"name": "B", "name_ja": "い", "id": "custom_b"}
    diseases = [a, b]
    orig_index = {id(a): 0, id(b): 1}

    monkeypatch.setattr(id_locks, "locked_id_for", lambda sp, e: None)
    resolved = _resolve_collision_free_ids("test", diseases, orig_index)
    assert resolved[id(a)] == "test_0000"
    assert resolved[id(b)] == "custom_b"


def test_no_id_collisions_across_all_species_modules():
    """Every module entry must resolve to a unique id — the exact failure mode
    that dropped rows from the served DB."""
    import importlib

    from api.species.helpers import dedupe_disease_list
    from scripts.migrate_to_sqlite import SPECIES_MODULES, _resolve_collision_free_ids

    for species_key, module_path in sorted(SPECIES_MODULES.items()):
        mod = importlib.import_module(module_path)
        raw = getattr(mod, "DISEASES", [])
        diseases = dedupe_disease_list(raw)
        orig_index = {id(e): i for i, e in enumerate(raw)}
        resolved = _resolve_collision_free_ids(species_key, diseases, orig_index)
        ids = list(resolved.values())
        assert len(ids) == len(set(ids)), f"{species_key}: duplicate served ids"


def test_appended_audit_diseases_are_served():
    """The three 2026-08 additions must exist in the served DB with unique ids
    and must not have displaced the entries whose locked ids they collided with."""
    if not SERVED_DB.exists():
        pytest.skip("served DB not built")
    conn = sqlite3.connect(str(SERVED_DB))
    try:
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='diseases'")
        if not cur.fetchone():
            pytest.skip("served DB empty")
        expected = [
            ("degu", "Elodontoma (Dental Tumor)"),
            ("guinea_pig", "Intestinal Torsion"),
            ("amphibian", "Parasitic Dermatitis"),
            # Previously clobbered by the id collision — must survive:
            ("degu", "Cataracts (Diabetic)"),
            ("guinea_pig", "Pneumonia (Bacterial)"),
            ("amphibian", "Batrachochytrium salamandrivorans (Bsal)"),
        ]
        for species, name in expected:
            cur.execute(
                "SELECT COUNT(*) FROM diseases WHERE species=? AND name=?",
                (species, name),
            )
            assert cur.fetchone()[0] == 1, f"{species}/{name} missing from served DB"
    finally:
        conn.close()
