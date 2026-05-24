"""Cross-species disease search fallback.

Low-memory deploys keep the SQLite ``diseases`` table empty (the full
migration peaks at ~535 MB RSS).  ``search_diseases`` must then fall back to
the prebuilt name index so that ``GET /api/diseases?q=`` — the cross-species
lookup used by the header search and the disease-DB tab when no species is
selected — keeps returning results.
"""

import os

os.environ.setdefault("SECRET_KEY", "test-key")
os.environ.setdefault("FLASK_DEBUG", "1")

from api import disease_store
from api.disease_store import _disease_search_index, search_diseases


class TestDiseaseSearchIndex:
    def test_index_artifact_is_populated(self):
        """The committed index artifact covers every species with names."""
        index = _disease_search_index()
        assert len(index) > 5000
        assert len({e["species"] for e in index}) == 21
        assert all(e.get("name") or e.get("name_ja") for e in index)


class TestCrossSpeciesSearchFallback:
    def test_falls_back_to_index_when_table_empty(self, monkeypatch):
        monkeypatch.setattr(disease_store, "_diseases_table_empty", lambda: True)

        results = search_diseases("diabetes", limit=20)
        assert results, "cross-species search must return results from the index"
        # Spans more than one species — the whole point of cross-species search.
        assert len({d["species"] for d in results}) >= 2
        assert all({"species", "name", "name_ja"} <= set(d) for d in results)

    def test_species_filter_narrows_results(self, monkeypatch):
        monkeypatch.setattr(disease_store, "_diseases_table_empty", lambda: True)

        results = search_diseases("diabetes", species="cat", limit=20)
        assert results
        assert all(d["species"] == "cat" for d in results)

    def test_japanese_query_matches_japanese_names(self, monkeypatch):
        monkeypatch.setattr(disease_store, "_diseases_table_empty", lambda: True)

        results = search_diseases("糖尿病", limit=20)
        assert results
        assert any("糖尿" in (d.get("name_ja") or "") for d in results)

    def test_multi_keyword_requires_all_terms(self, monkeypatch):
        monkeypatch.setattr(disease_store, "_diseases_table_empty", lambda: True)

        results = search_diseases("feline diabetes", limit=20)
        for d in results:
            haystack = ((d.get("name") or "") + (d.get("name_ja") or "")).lower()
            assert "feline" in haystack and "diabetes" in haystack

    def test_empty_query_returns_nothing(self, monkeypatch):
        monkeypatch.setattr(disease_store, "_diseases_table_empty", lambda: True)
        assert search_diseases("", limit=20) == []
