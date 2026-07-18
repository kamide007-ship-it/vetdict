"""Regression tests for the T108 corpus-load guard (detector robustness).

The T108 detector mirrors the drug/citation auto-match to count mis-links. Its
corpus (``api.drug_dictionary.DRUGS`` / ``api.pubmed_references.DISEASE_REFERENCES``)
is never legitimately empty, so a failed import (e.g. a bare environment missing
Flask) must NOT silently read as a clean "0 mismatch" result. These tests pin
that a corpus-load failure is surfaced loudly instead of collapsing to a false
clean baseline.
"""

from __future__ import annotations

import scripts.quality.detect as det
from scripts.quality.detect import detect_source_integrity, run


def _records():
    return det.load_species_records("degu", served=False)


def test_healthy_corpus_reports_loaded_and_nonempty():
    t8 = run("degu", served=False)["T108"]
    assert t8["drug_corpus_loaded"] is True
    assert t8["citation_corpus_loaded"] is True
    assert t8["corpus_incomplete"] is False
    assert t8["corpus_warning"] is None
    # The corpus is substantial; a healthy load is never empty.
    assert t8["drug_available"] > 0
    assert t8["ref_keys_available"] > 0


def test_failed_drug_corpus_flags_incomplete(monkeypatch):
    monkeypatch.setattr(det, "_load_drugs", lambda: ([], False))
    t8 = detect_source_integrity(_records(), "degu")
    assert t8["drug_corpus_loaded"] is False
    assert t8["corpus_incomplete"] is True
    # Count collapses to 0 but must be flagged, not trusted as clean.
    assert t8["drug_mismatch_count"] == 0
    assert t8["corpus_warning"] and "薬品辞書" in t8["corpus_warning"]


def test_failed_citation_corpus_flags_incomplete(monkeypatch):
    monkeypatch.setattr(det, "_load_disease_reference_keys", lambda: ([], False))
    t8 = detect_source_integrity(_records(), "degu")
    assert t8["citation_corpus_loaded"] is False
    assert t8["corpus_incomplete"] is True
    assert t8["citation_mismatch_count"] == 0
    assert t8["corpus_warning"] and "出典キー" in t8["corpus_warning"]


def test_markdown_emits_warning_banner_when_corpus_incomplete(monkeypatch):
    monkeypatch.setattr(det, "_load_drugs", lambda: ([], False))
    monkeypatch.setattr(det, "_load_disease_reference_keys", lambda: ([], False))
    md = det._markdown_summary(run("degu", served=False))
    assert "⚠️ **参照コーパス未読み込み" in md
    assert "ロード**失敗**" in md


def test_healthy_markdown_has_no_incomplete_banner():
    md = det._markdown_summary(run("degu", served=False))
    assert "参照コーパス未読み込み" not in md
    # But the corpus-size transparency line is always present.
    assert "参照コーパス: 薬品" in md
