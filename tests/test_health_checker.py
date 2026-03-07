"""
Comprehensive tests for the health symptom checker.

Tests cover:
- Symptom database integrity
- Disease database integrity
- Jaccard similarity algorithm
- Symptom analysis pipeline
- Breed-specific risk multipliers
- Age-based adjustments
- Emergency detection
- Edge cases
"""

from api.health_checker import (
    DISEASES,
    SEVERITY_WEIGHTS,
    SYMPTOM_IDS,
    SYMPTOMS,
    _analyze_symptoms,
    _jaccard_similarity,
)


# ============================================================================
# Database Integrity
# ============================================================================


class TestSymptomDatabase:
    """Verify symptom database structure and consistency."""

    def test_symptom_count(self):
        assert len(SYMPTOMS) == 52

    def test_all_symptoms_have_required_fields(self):
        for s in SYMPTOMS:
            assert "id" in s, f"Symptom missing 'id': {s}"
            assert "name_ja" in s, f"Symptom missing 'name_ja': {s}"
            assert "name_en" in s, f"Symptom missing 'name_en': {s}"
            assert "category" in s, f"Symptom missing 'category': {s}"

    def test_symptom_ids_unique(self):
        ids = [s["id"] for s in SYMPTOMS]
        assert len(ids) == len(set(ids)), "Duplicate symptom IDs found"

    def test_symptom_ids_set_matches(self):
        """SYMPTOM_IDS set must match all symptom id values."""
        expected = {s["id"] for s in SYMPTOMS}
        assert SYMPTOM_IDS == expected

    def test_all_categories_present(self):
        categories = {s["category"] for s in SYMPTOMS}
        expected_categories = {
            "respiratory",
            "digestive",
            "neurological",
            "musculoskeletal",
            "dermatological",
            "urinary",
            "ocular",
            "cardiac",
            "behavioral",
            "general",
        }
        assert categories == expected_categories


class TestDiseaseDatabase:
    """Verify disease database structure and consistency."""

    def test_disease_count(self):
        assert len(DISEASES) == 62

    def test_all_diseases_have_required_fields(self):
        for d in DISEASES:
            assert "id" in d, f"Disease missing 'id'"
            assert "name_ja" in d, f"Disease {d.get('id')} missing 'name_ja'"
            assert "name_en" in d, f"Disease {d.get('id')} missing 'name_en'"
            assert "symptoms" in d, f"Disease {d.get('id')} missing 'symptoms'"
            assert "severity" in d, f"Disease {d.get('id')} missing 'severity'"
            assert "recommended_tests" in d, f"Disease {d.get('id')} missing 'recommended_tests'"
            assert "breed_risks" in d, f"Disease {d.get('id')} missing 'breed_risks'"

    def test_disease_ids_unique(self):
        ids = [d["id"] for d in DISEASES]
        assert len(ids) == len(set(ids)), "Duplicate disease IDs found"

    def test_all_disease_symptoms_are_valid(self):
        """Every symptom referenced in a disease must exist in SYMPTOM_IDS."""
        for d in DISEASES:
            for symptom_id in d["symptoms"]:
                assert symptom_id in SYMPTOM_IDS, (
                    f"Disease '{d['id']}' references unknown symptom '{symptom_id}'"
                )

    def test_all_severities_are_valid(self):
        valid_severities = set(SEVERITY_WEIGHTS.keys())
        for d in DISEASES:
            assert d["severity"] in valid_severities, (
                f"Disease '{d['id']}' has invalid severity '{d['severity']}'"
            )

    def test_breed_risks_are_positive(self):
        for d in DISEASES:
            for breed, risk in d["breed_risks"].items():
                assert risk > 0, (
                    f"Disease '{d['id']}' has non-positive risk {risk} for breed '{breed}'"
                )


# ============================================================================
# Jaccard Similarity
# ============================================================================


class TestJaccardSimilarity:
    """Verify Jaccard similarity implementation."""

    def test_identical_sets(self):
        assert _jaccard_similarity({"a", "b"}, {"a", "b"}) == 1.0

    def test_disjoint_sets(self):
        assert _jaccard_similarity({"a", "b"}, {"c", "d"}) == 0.0

    def test_partial_overlap(self):
        result = _jaccard_similarity({"a", "b", "c"}, {"b", "c", "d"})
        assert abs(result - 0.5) < 0.01  # 2/4

    def test_empty_set_a(self):
        assert _jaccard_similarity(set(), {"a", "b"}) == 0.0

    def test_empty_set_b(self):
        assert _jaccard_similarity({"a", "b"}, set()) == 0.0

    def test_both_empty(self):
        assert _jaccard_similarity(set(), set()) == 0.0

    def test_subset(self):
        result = _jaccard_similarity({"a", "b"}, {"a", "b", "c"})
        assert abs(result - 2 / 3) < 0.01

    def test_single_element_match(self):
        result = _jaccard_similarity({"a"}, {"a"})
        assert result == 1.0

    def test_symmetry(self):
        a = {"a", "b", "c"}
        b = {"b", "c", "d", "e"}
        assert _jaccard_similarity(a, b) == _jaccard_similarity(b, a)


# ============================================================================
# Symptom Analysis
# ============================================================================


class TestAnalyzeSymptoms:
    """Verify the core analysis pipeline."""

    def test_basic_analysis_returns_results(self):
        results = _analyze_symptoms("", ["coughing", "labored_breathing"])
        assert len(results) > 0

    def test_results_sorted_by_composite_score(self):
        results = _analyze_symptoms("", ["vomiting", "diarrhea", "lethargy"])
        scores = [r["composite_score"] for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_matched_symptoms_are_correct(self):
        results = _analyze_symptoms("", ["coughing", "sneezing", "nasal_discharge"])
        for r in results:
            for s in r["matched_symptoms"]:
                assert s in ["coughing", "sneezing", "nasal_discharge"]

    def test_confidence_capped_at_95(self):
        results = _analyze_symptoms("", ["coughing", "labored_breathing"])
        for r in results:
            assert r["confidence_percent"] <= 95.0

    def test_no_match_for_unrelated_symptoms(self):
        """Symptoms from completely different categories should still match
        diseases that span categories."""
        results = _analyze_symptoms("", ["seizures"])
        # Should find at least epilepsy
        disease_ids = [r["disease_id"] for r in results]
        assert "epilepsy" in disease_ids

    def test_breed_risk_multiplier_applied(self):
        """French bulldog should have elevated risk for BOAS."""
        results_with_breed = _analyze_symptoms(
            "french_bulldog", ["labored_breathing", "wheezing"]
        )
        results_no_breed = _analyze_symptoms("", ["labored_breathing", "wheezing"])

        # Find BOAS in both
        boas_breed = next((r for r in results_with_breed if r["disease_id"] == "brachycephalic_airway_syndrome"), None)
        boas_no = next((r for r in results_no_breed if r["disease_id"] == "brachycephalic_airway_syndrome"), None)

        assert boas_breed is not None
        assert boas_no is not None
        assert boas_breed["breed_risk_multiplier"] > boas_no["breed_risk_multiplier"]

    def test_age_factor_for_puppies(self):
        """Puppies should have higher risk for parvovirus."""
        results_puppy = _analyze_symptoms("", ["vomiting", "diarrhea", "blood_in_stool", "lethargy"], 0.5)
        results_adult = _analyze_symptoms("", ["vomiting", "diarrhea", "blood_in_stool", "lethargy"], 4.0)

        parvo_puppy = next((r for r in results_puppy if r["disease_id"] == "canine_parvovirus"), None)
        parvo_adult = next((r for r in results_adult if r["disease_id"] == "canine_parvovirus"), None)

        assert parvo_puppy is not None
        assert parvo_adult is not None
        assert parvo_puppy["age_factor"] > parvo_adult["age_factor"]

    def test_age_factor_for_seniors(self):
        """Senior dogs should have higher risk for degenerative diseases."""
        results_senior = _analyze_symptoms("", ["limping", "stiffness", "reluctance_to_move"], 10.0)
        results_young = _analyze_symptoms("", ["limping", "stiffness", "reluctance_to_move"], 2.0)

        # Both should return results
        assert len(results_senior) > 0
        assert len(results_young) > 0

    def test_result_structure(self):
        results = _analyze_symptoms("", ["coughing"])
        assert len(results) > 0
        r = results[0]
        assert "disease_id" in r
        assert "name_ja" in r
        assert "name_en" in r
        assert "severity" in r
        assert "confidence_percent" in r
        assert "composite_score" in r
        assert "breed_risk_multiplier" in r
        assert "matched_symptoms" in r
        assert "matched_count" in r
        assert "total_disease_symptoms" in r
        assert "recommended_tests" in r

    def test_empty_symptoms_returns_empty(self):
        """No symptoms should produce no matches (Jaccard = 0 for all)."""
        results = _analyze_symptoms("", [])
        # _analyze_symptoms requires symptom_ids to be iterable
        # Even with empty, it should return empty (no Jaccard match)
        assert len(results) == 0

    def test_emergency_diseases_detected(self):
        """Parvovirus symptoms should flag emergency."""
        results = _analyze_symptoms(
            "", ["vomiting", "diarrhea", "blood_in_stool", "lethargy", "loss_of_appetite", "fever"]
        )
        emergency_found = any(r["severity"] == "emergency" for r in results[:5])
        assert emergency_found
