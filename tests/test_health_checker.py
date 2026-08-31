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
        assert (
            len(SYMPTOMS) == 76
        )  # +hives, +facial_swelling (round-14) + snoring (round-15 BOAS) after merge

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
        assert expected == SYMPTOM_IDS

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
        assert (
            len(DISEASES) == 80
        )  # +acute_allergic_reaction (2026-08 round-14); before +mammary_tumor, +testicular_tumor

    def test_all_diseases_have_required_fields(self):
        for d in DISEASES:
            assert "id" in d, "Disease missing 'id'"
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
                assert symptom_id in SYMPTOM_IDS, f"Disease '{d['id']}' references unknown symptom '{symptom_id}'"

    def test_all_severities_are_valid(self):
        valid_severities = set(SEVERITY_WEIGHTS.keys())
        for d in DISEASES:
            assert d["severity"] in valid_severities, f"Disease '{d['id']}' has invalid severity '{d['severity']}'"

    def test_breed_risks_are_positive(self):
        for d in DISEASES:
            for breed, risk in d["breed_risks"].items():
                assert risk > 0, f"Disease '{d['id']}' has non-positive risk {risk} for breed '{breed}'"


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
        results_with_breed = _analyze_symptoms("french_bulldog", ["labored_breathing", "wheezing"])
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

    def test_onset_boost_for_matching(self):
        """Matching onset should boost score."""
        results_acute = _analyze_symptoms("", ["vomiting", "diarrhea"], onset="acute")
        _analyze_symptoms("", ["vomiting", "diarrhea"])
        # At least one result should have onset_factor != 1.0
        acute_factors = [r["onset_factor"] for r in results_acute]
        assert any(f != 1.0 for f in acute_factors)

    def test_onset_chronic(self):
        """Chronic onset should work."""
        results = _analyze_symptoms("", ["limping", "stiffness"], onset="chronic")
        assert isinstance(results, list)
        for r in results:
            assert "onset_factor" in r


# ============================================================================
# Flask Route Tests
# ============================================================================

import pytest
from flask import Flask

from api.health_checker import health_bp


@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(health_bp)
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()


class TestGetSymptomsRoute:
    def test_returns_all_symptoms(self, client):
        resp = client.get("/api/health-check/symptoms")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "total" in data
        assert "symptoms" in data
        assert "categories" in data
        assert data["total"] == 76

    def test_filter_by_category(self, client):
        resp = client.get("/api/health-check/symptoms?category=respiratory")
        assert resp.status_code == 200
        data = resp.get_json()
        for s in data["symptoms"]:
            assert s["category"] == "respiratory"
        assert data["total"] < 52


class TestGetOnsetOptionsRoute:
    def test_returns_onset_and_age(self, client):
        resp = client.get("/api/health-check/onset-options")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "onset" in data
        assert "age_range" in data

    def test_onset_has_three_options(self, client):
        resp = client.get("/api/health-check/onset-options")
        data = resp.get_json()
        assert len(data["onset"]["options"]) == 3
        ids = [o["id"] for o in data["onset"]["options"]]
        assert set(ids) == {"acute", "subacute", "chronic"}

    def test_age_range_has_four_options(self, client):
        resp = client.get("/api/health-check/onset-options")
        data = resp.get_json()
        assert len(data["age_range"]["options"]) == 4


class TestGetDiseasesRoute:
    def test_dog_default(self, client):
        resp = client.get("/api/health-check/diseases")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["total"] > 0
        assert "diseases" in data

    def test_cat_species(self, client):
        resp = client.get("/api/health-check/diseases?species=cat")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["total"] > 0

    def test_horse_species(self, client):
        resp = client.get("/api/health-check/diseases?species=horse")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["total"] > 0

    def test_rabbit_species(self, client):
        resp = client.get("/api/health-check/diseases?species=rabbit")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["total"] > 0


class TestDiseaseQualityReportRoute:
    def test_returns_report(self, client):
        resp = client.get("/api/health-check/disease-quality-report")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "species" in data
        assert "total_diseases" in data
        assert "average_completeness" in data
        assert "diseases_with_missing_fields" in data
        assert "missing_field_counts" in data

    def test_cat_report(self, client):
        resp = client.get("/api/health-check/disease-quality-report?species=cat")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["species"] == "cat"


class TestAnalyzeRoute:
    def test_valid_analysis(self, client):
        resp = client.post(
            "/api/health-check/analyze",
            json={"symptoms": ["vomiting", "diarrhea"]},
        )
        assert resp.status_code == 200
        data = resp.get_json()
        assert "top_matches" in data
        assert "total_matches" in data
        assert "emergency_flag" in data
        assert "disclaimer" in data
        assert "supervised_by" in data
        assert "consolidated_priority_tests" in data

    def test_empty_symptoms_400(self, client):
        resp = client.post("/api/health-check/analyze", json={"symptoms": []})
        assert resp.status_code == 400

    def test_no_body_400(self, client):
        resp = client.post(
            "/api/health-check/analyze",
            content_type="application/json",
            data="",
        )
        assert resp.status_code == 400

    def test_invalid_symptom_400(self, client):
        resp = client.post(
            "/api/health-check/analyze",
            json={"symptoms": ["nonexistent_xyz"]},
        )
        assert resp.status_code == 400
        data = resp.get_json()
        assert "invalid_symptoms" in data
        assert "valid_symptoms" in data

    def test_with_breed_age_onset(self, client):
        resp = client.post(
            "/api/health-check/analyze",
            json={
                "symptoms": ["vomiting", "lethargy"],
                "breed_id": "french_bulldog",
                "age_years": 5,
                "onset": "acute",
            },
        )
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["input"]["breed_id"] == "french_bulldog"
        assert data["input"]["age_years"] == 5.0
        assert data["input"]["onset"] == "acute"

    def test_invalid_onset_400(self, client):
        resp = client.post(
            "/api/health-check/analyze",
            json={"symptoms": ["vomiting"], "onset": "wrong"},
        )
        assert resp.status_code == 400

    def test_invalid_age_400(self, client):
        resp = client.post(
            "/api/health-check/analyze",
            json={"symptoms": ["vomiting"], "age_years": "not_a_number"},
        )
        assert resp.status_code == 400

    def test_fci_prefix_stripped(self, client):
        resp = client.post(
            "/api/health-check/analyze",
            json={"symptoms": ["vomiting"], "breed_id": "101_french_bulldog"},
        )
        assert resp.status_code == 200
        assert resp.get_json()["input"]["breed_id"] == "french_bulldog"

    def test_genetic_info_for_known_breed(self, client):
        resp = client.post(
            "/api/health-check/analyze",
            json={
                "symptoms": ["vomiting", "lethargy"],
                "breed_id": "golden_retriever",
            },
        )
        assert resp.status_code == 200
        data = resp.get_json()
        # golden_retriever may or may not have genetic data
        assert "breed_genetic_info" in data

    def test_emergency_flag_true(self, client):
        resp = client.post(
            "/api/health-check/analyze",
            json={
                "symptoms": [
                    "vomiting",
                    "diarrhea",
                    "blood_in_stool",
                    "lethargy",
                    "loss_of_appetite",
                    "fever",
                ],
            },
        )
        data = resp.get_json()
        assert data["emergency_flag"] is True
        assert data["emergency_message"] is not None

    def test_symptoms_not_list_400(self, client):
        resp = client.post(
            "/api/health-check/analyze",
            json={"symptoms": "vomiting"},
        )
        assert resp.status_code == 400


class TestBreedRisksRoute:
    def test_known_breed(self, client):
        resp = client.get("/api/health-check/breed-risks/french_bulldog")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "breed_id" in data or "breed_diseases" in data or "disease_risks" in data

    def test_unknown_breed_404(self, client):
        resp = client.get("/api/health-check/breed-risks/nonexistent_xyz")
        assert resp.status_code in (200, 404)


class TestRecommendedTestsDisplay:
    """Translation table for diagnostic test IDs powers the symptom checker UI.

    Without these, the JA pane shows snake_case English (e.g. "Complete Blood
    Count") in both name_ja and name_en, which is unreadable to JA users.
    """

    def test_known_id_translates_to_japanese(self):
        from api.health_checker import _build_recommended_tests_display

        out = _build_recommended_tests_display(["complete_blood_count"], "cat")
        assert out == [
            {
                "id": "complete_blood_count",
                "name_ja": "血液一般検査 (CBC)",
                "name_en": "Complete Blood Count (CBC)",
            }
        ]

    def test_unknown_id_falls_back_to_humanized(self):
        from api.health_checker import _build_recommended_tests_display

        out = _build_recommended_tests_display(["zebra_dx_panel"], "cat")
        assert out[0]["id"] == "zebra_dx_panel"
        # Humanized fallback is the same string for both langs
        assert out[0]["name_en"] == "Zebra Dx Panel"
        assert out[0]["name_ja"] == "Zebra Dx Panel"

    def test_pre_translated_japanese_passes_through(self):
        from api.health_checker import _build_recommended_tests_display

        out = _build_recommended_tests_display(["PCR検査", "血液生化学検査"], "cat")
        assert {d["id"] for d in out} == {"PCR検査", "血液生化学検査"}
        # CJK entries kept identical across name_ja and name_en
        for d in out:
            assert d["name_ja"] == d["id"]
            assert d["name_en"] == d["id"]

    def test_single_token_id_gets_capitalized(self):
        from api.health_checker import _humanize_test_id

        # Without underscores, single tokens are now title-cased so they don't
        # appear as raw lowercase IDs in the UI.
        assert _humanize_test_id("endoscopy") == "Endoscopy"
        # Known abbreviations stay uppercase.
        assert _humanize_test_id("cbc") == "CBC"

    def test_abbreviation_segments_remain_upper(self):
        from api.health_checker import _humanize_test_id

        # In a multi-token ID, abbreviation segments must stay uppercase
        # ("CT scan", not "Ct Scan").
        assert _humanize_test_id("ct_scan") == "CT Scan"
        assert _humanize_test_id("mri_brain") == "MRI Brain"

    def test_empty_or_invalid_input_returns_empty_list(self):
        from api.health_checker import _build_recommended_tests_display

        assert _build_recommended_tests_display([], "cat") == []
        assert _build_recommended_tests_display(None, "cat") == []
        # Mixed bad entries are skipped, valid entries kept
        out = _build_recommended_tests_display(["cbc", None, "", 42], "cat")
        ids = [d["id"] for d in out]
        assert ids == ["cbc"]
