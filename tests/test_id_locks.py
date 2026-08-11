"""Regression tests for the stable disease-id freeze (Phase 2 quality program).

These are pure-Python (no Flask) so they run in any environment.
"""

import importlib
import json

import pytest

from api.species import id_locks
from api.species.id_locks import stable_id_for, stable_key


def _degu_entries():
    m = importlib.import_module("api.species.degu_diseases")
    from api.species.helpers import dedupe_disease_list

    raw = list(m.DISEASES)
    dd = dedupe_disease_list(raw)
    orig = {id(e): i for i, e in enumerate(raw)}
    return raw, dd, orig


def test_stable_key_uses_name_and_name_ja():
    assert stable_key({"name": "Diabetes", "name_ja": "糖尿病"}) != stable_key({"name": "Diabetes", "name_ja": "別物"})

    # Objects (dataclass-like) resolve via attributes too.
    class E:
        name = "Cataract"
        name_ja = "白内障"

    assert stable_key(E()) == stable_key({"name": "Cataract", "name_ja": "白内障"})


def test_missing_lock_falls_back_to_position_id():
    id_locks.clear_cache()
    # A species with no sidecar returns the caller's fallback unchanged.
    assert stable_id_for("no_such_species", {"name": "X", "name_ja": "X"}, "fallback_9") == "fallback_9"


def test_every_entry_is_locked_and_served_ids_match_locks():
    """Every current degu entry must be frozen in the sidecar, and the served-DB
    id allocator must assign exactly the locked id to each of them.

    (This replaces the original "locked id == today's position id" assertion,
    whose premise only held while the list composition never changed. Once a
    disease is legitimately inserted mid-list — e.g. appended to the .py list
    ahead of the supplementary block — later entries keep their FROZEN ids,
    which by design no longer equal their new positional fallbacks. What must
    hold instead: no entry is unlocked, and serving honours the lock.)"""
    id_locks.clear_cache()
    _, dd, orig = _degu_entries()
    from scripts.migrate_to_sqlite import _resolve_collision_free_ids

    resolved = _resolve_collision_free_ids("degu", dd, orig)
    for d in dd:
        locked = id_locks.locked_id_for("degu", d)
        assert locked, f"unlocked degu entry: {d.get('name')!r} — run scripts.quality.build_id_locks"
        assert resolved[id(d)] == locked, f"served id {resolved[id(d)]!r} != locked id {locked!r} for {d.get('name')!r}"
    ids = list(resolved.values())
    assert len(ids) == len(set(ids)), "duplicate served ids"


def test_ids_are_pinned_across_reorder():
    """After the source list is re-ordered, ids must not drift."""
    id_locks.clear_cache()
    raw, dd, orig = _degu_entries()
    from api.species.helpers import dedupe_disease_list

    def ids_for(raw_list):
        d2 = dedupe_disease_list(raw_list)
        o2 = {id(e): i for i, e in enumerate(raw_list)}
        return {
            (d.get("name") or d.get("name_ja")): stable_id_for("degu", d, d.get("id") or f"degu_{o2[id(d)]:04d}")
            for d in d2
        }

    base = ids_for(raw)
    reversed_ids = ids_for(list(reversed(raw)))
    assert base == reversed_ids, "ids drifted after reorder — freeze failed"


def test_lock_sidecar_has_no_duplicate_ids():
    """A frozen id must map to exactly one disease (no id collisions)."""
    id_locks.clear_cache()
    path = id_locks._LOCK_DIR + "/degu.json"
    with open(path, encoding="utf-8") as fh:
        locks = json.load(fh)["locks"]
    ids = list(locks.values())
    assert len(ids) == len(set(ids)), "duplicate frozen ids in degu lock"


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
