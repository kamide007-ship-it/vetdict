"""Tests for the treatment dosage publish gate (T106) — must be fail-closed."""

from __future__ import annotations

import json

from api.species import treatment_overrides as to


def _write_map(tmp_path, monkeypatch, entries):
    d = tmp_path / "treatment_overrides"
    d.mkdir()
    (d / "testsp.json").write_text(json.dumps({"species": "testsp", "entries": entries}), encoding="utf-8")
    monkeypatch.setattr(to, "_DIR", d)
    to.load_overrides.cache_clear()
    to._published_index.cache_clear()


def _apply(name, species="testsp"):
    recs = [{"name": name, "name_ja": name, "treatment_ja": "ORIGINAL", "treatment": "ORIGINAL"}]
    return to.apply_treatment_overrides(recs, species)[0]


def test_draft_is_never_served(tmp_path, monkeypatch):
    _write_map(
        tmp_path,
        monkeypatch,
        [
            {"slug": "x", "name": "X", "review_status": "draft", "treatment_ja": "5 mg/kg PO", "sources": ["ref"]},
        ],
    )
    assert _apply("X")["treatment_ja"] == "ORIGINAL"  # draft held back


def test_approved_but_not_published_is_never_served(tmp_path, monkeypatch):
    _write_map(
        tmp_path,
        monkeypatch,
        [
            {"slug": "x", "name": "X", "review_status": "approved", "treatment_ja": "5 mg/kg PO", "sources": ["ref"]},
        ],
    )
    assert _apply("X")["treatment_ja"] == "ORIGINAL"


def test_published_without_sources_is_refused(tmp_path, monkeypatch):
    # Fail-closed: a dose can never go live uncited.
    _write_map(
        tmp_path,
        monkeypatch,
        [
            {"slug": "x", "name": "X", "review_status": "published", "treatment_ja": "5 mg/kg PO", "sources": []},
        ],
    )
    assert _apply("X")["treatment_ja"] == "ORIGINAL"


def test_published_with_sources_is_served(tmp_path, monkeypatch):
    _write_map(
        tmp_path,
        monkeypatch,
        [
            {
                "slug": "x",
                "name": "X",
                "review_status": "published",
                "treatment_ja": "5 mg/kg PO q12h",
                "sources": ["Carpenter Exotic Formulary 6th ed"],
            },
        ],
    )
    out = _apply("X")
    assert out["treatment_ja"] == "5 mg/kg PO q12h"
    assert out["treatment_reviewed"] is True
    assert out["treatment_sources"] == ["Carpenter Exotic Formulary 6th ed"]


def test_no_map_is_noop():
    recs = [{"name": "Y", "name_ja": "Y", "treatment_ja": "ORIG"}]
    assert to.apply_treatment_overrides(recs, "no_such_species") is recs


def test_degu_publishes_only_vet_approved_sourced_doses():
    # Fur mites is the one vet-approved, PubMed-sourced grade-A dose (published).
    # Every other degu entry stays draft and must NOT be served. Fail-closed:
    # any served entry must carry sources and a real dose.
    to.load_overrides.cache_clear()
    to._published_index.cache_clear()
    idx = to._published_index("degu")
    assert set(idx) == {"fur-mites-demodex-notoedres"}, idx
    entry = idx["fur-mites-demodex-notoedres"]
    assert entry["sources"], "published dose must be cited (fail-closed)"
    assert "mg/kg" in entry["treatment_ja"], "published entry must carry an actual dose"
