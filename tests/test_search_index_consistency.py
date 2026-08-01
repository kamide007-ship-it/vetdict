#!/usr/bin/env python3
"""The cross-species search index must describe exactly what is servable.

``GET /api/diseases?q=`` falls back to ``api/data/disease_search_index.json``
whenever SQLite is empty — which is the normal state on the 512 MB production
host, so this index *is* the search backend there.

It used to be built straight from the raw species modules, skipping the three
transforms the browse/detail paths apply (``dedupe_disease_list``,
``apply_canonical_map`` and the ``stable_id_for`` lock sidecar). The index
therefore advertised 7,103 diseases against 6,529 browsable ones, and 54 of its
ids resolved to nothing — a search hit that opened a dead page.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import pytest

INDEX_PATH = REPO_ROOT / "api" / "data" / "disease_search_index.json"


@pytest.fixture(scope="module")
def index() -> list[dict]:
    if not INDEX_PATH.is_file():
        pytest.skip("search index not built")
    return json.loads(INDEX_PATH.read_text(encoding="utf-8"))


def test_index_ids_are_unique(index):
    ids = [e["id"] for e in index]
    assert len(ids) == len(set(ids)), "duplicate ids in the search index"


def test_index_matches_advertised_disease_count(index):
    """The index size must equal the browsable count the site advertises."""
    from api.disease_store import _fallback_disease_counts

    advertised = sum(_fallback_disease_counts().values())
    assert len(index) == advertised, (
        f"search index has {len(index)} entries but the site advertises {advertised} "
        "browsable diseases — search would surface hits that cannot be opened"
    )


def test_index_applies_dedupe_and_canonical_map():
    """Rebuilding one species must go through the served-path transforms."""
    from scripts.build_disease_search_index import build_species_entries

    entries = build_species_entries("dog")
    names = [e["name"] for e in entries]
    assert len(names) == len(set(names)), "dedupe was not applied — duplicate names in index"

    # Position-derived ids drift when a disease is inserted mid-list, so the
    # builder must resolve the frozen id sidecar rather than use raw indices.
    from api.species.id_locks import stable_id_for

    from api.species.dog_diseases import DISEASES  # isort: skip

    locked = stable_id_for("dog", DISEASES[0], "dog_0000")
    assert any(e["id"] == locked for e in entries), "stable id lock was not honoured"
