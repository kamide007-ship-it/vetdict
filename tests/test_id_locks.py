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


def test_current_order_ids_are_byte_identical():
    """The lock must not change any id a disease has today."""
    id_locks.clear_cache()
    _, dd, orig = _degu_entries()
    for d in dd:
        fb = d.get("id") or f"degu_{orig[id(d)]:04d}"
        assert stable_id_for("degu", d, fb) == fb


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
