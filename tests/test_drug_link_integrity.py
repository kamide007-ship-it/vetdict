"""T111 — drug-link integrity: sponsor/ECVN products excluded from the
evidence-based drug matcher, and Latin keywords match on word boundaries."""

from __future__ import annotations

from api.drug_dictionary import (
    _DRUG_KEYWORD_INDEX,
    find_drugs_for_disease,
    find_drugs_in_text,
)


def test_ecvn_sponsor_products_not_in_drug_matcher():
    # Generic ECVN first-words that used to pollute matches are gone.
    for bad in ("amino", "canine", "kamide"):
        assert bad not in _DRUG_KEYWORD_INDEX
    # No ECVN product surfaces from text that name-drops its ingredients.
    hits = find_drugs_in_text("supplement with amino acids and cbd for a canine patient")
    assert not any("Equine & Canine Vet Nutrition" in d["name"] for d in hits)


def test_latin_keywords_match_on_word_boundary():
    # "iron" must not match inside "environment"; "amino" not in "amino acids".
    assert find_drugs_in_text("keep the patient in a clean environment") == []
    assert find_drugs_in_text("provide amino acids in the diet") == []


def test_real_drug_mentions_still_match():
    names = {d["name"] for d in find_drugs_in_text("amoxicillin 20 mg/kg PO q12h plus meloxicam 0.1 mg/kg")}
    assert "Amoxicillin" in names
    assert "Meloxicam" in names


def test_index_still_populated_and_has_common_drug():
    assert len(_DRUG_KEYWORD_INDEX) > 100
    assert "amoxicillin" in _DRUG_KEYWORD_INDEX


def test_degu_diabetes_related_drugs_have_no_sponsor_product():
    drugs = find_drugs_for_disease("degu", "糖尿病", "ja")
    assert drugs  # still finds the real drug(s)
    assert not any("Equine & Canine Vet Nutrition" in d["name"] for d in drugs)
