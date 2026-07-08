"""T110 — species-aware citation binding v2 (curation + species guard), v1 kept."""

from __future__ import annotations

import json

import api.pubmed_references as pr


def test_v1_is_unchanged_and_still_species_blind():
    # v1 still returns a (wrong-species) citation for a degu disease by keyword.
    assert len(pr.get_references_for_disease("Cardiomyopathy")) >= 1


def test_v2_suppresses_cross_species_keyword_leaks():
    for name in ("Cardiomyopathy", "Chronic Kidney Disease", "Diabetes Mellitus"):
        assert pr.get_references_for_disease_v2(name, "degu") == []


def test_v2_keeps_species_appropriate_citations():
    assert pr.get_references_for_disease_v2("Hypertrophic Cardiomyopathy (HCM)", "cat")
    assert pr.get_references_for_disease_v2("Insulinoma", "ferret")
    assert pr.get_references_for_disease_v2("Wobbly Hedgehog Syndrome (WHS)", "hedgehog")
    # degu is a herbivore-exotic -> GI stasis / malocclusion literature applies.
    assert pr.get_references_for_disease_v2("Gastrointestinal Stasis", "degu")
    assert pr.get_references_for_disease_v2("Dental Malocclusion", "degu")


def test_v2_without_species_reproduces_v1():
    name = "Cardiomyopathy"
    assert pr.get_references_for_disease_v2(name, None) == pr.get_references_for_disease(name)


def test_curated_binding_takes_precedence(tmp_path, monkeypatch):
    d = tmp_path / "citations_v2"
    d.mkdir()
    curated = [{"title": "Degu-specific cardiomyopathy study", "journal": "J Exot Pet Med", "year": 2023}]
    (d / "degu.json").write_text(json.dumps({"bindings": {"cardiomyopathy": curated}}), encoding="utf-8")
    monkeypatch.setattr(pr, "_CITATIONS_V2_DIR", d)
    pr._curated_v2.cache_clear()
    assert pr.get_references_for_disease_v2("Cardiomyopathy", "degu") == curated
    pr._curated_v2.cache_clear()


def test_curated_can_explicitly_clear_bad_binding(tmp_path, monkeypatch):
    # A curator can bind an empty list to suppress a disease's citations entirely.
    d = tmp_path / "citations_v2"
    d.mkdir()
    (d / "degu.json").write_text(json.dumps({"bindings": {"insulinoma": []}}), encoding="utf-8")
    monkeypatch.setattr(pr, "_CITATIONS_V2_DIR", d)
    pr._curated_v2.cache_clear()
    assert pr.get_references_for_disease_v2("Insulinoma", "degu") == []
    pr._curated_v2.cache_clear()
