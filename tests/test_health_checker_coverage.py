"""Tests for api/health_checker.py — health checker blueprint coverage.

The health_bp blueprint is registered on the main app and serves
endpoints under /api/health-check/.

Covers:
- GET /api/health-check/symptoms
- GET /api/health-check/onset-options
- GET /api/health-check/diseases
- POST /api/health-check/analyze — valid symptoms, with breed_id, with age_years
- GET /api/health-check/breed-risks/<breed_id>
- GET /api/health-check/disease-quality-report
"""

import json

import pytest

from api.showdog_api import app


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def client(temp_instance):
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


# ---------------------------------------------------------------------------
# GET /api/health-check/symptoms
# ---------------------------------------------------------------------------

class TestSymptomsEndpoint:
    def test_symptoms_returns_200(self, client):
        resp = client.get("/api/health-check/symptoms")
        assert resp.status_code == 200

    def test_symptoms_returns_list(self, client):
        data = client.get("/api/health-check/symptoms").get_json()
        assert "symptoms" in data
        assert isinstance(data["symptoms"], list)
        assert len(data["symptoms"]) > 0

    def test_symptoms_has_total(self, client):
        data = client.get("/api/health-check/symptoms").get_json()
        assert "total" in data
        assert data["total"] == len(data["symptoms"])

    def test_symptoms_has_categories(self, client):
        data = client.get("/api/health-check/symptoms").get_json()
        assert "categories" in data
        assert isinstance(data["categories"], list)

    def test_symptoms_filter_by_category(self, client):
        resp = client.get("/api/health-check/symptoms?category=respiratory")
        data = resp.get_json()
        assert resp.status_code == 200
        for symptom in data["symptoms"]:
            assert symptom["category"] == "respiratory"

    def test_symptom_structure(self, client):
        data = client.get("/api/health-check/symptoms").get_json()
        symptom = data["symptoms"][0]
        assert "id" in symptom
        assert "name_ja" in symptom
        assert "name_en" in symptom
        assert "category" in symptom


# ---------------------------------------------------------------------------
# GET /api/health-check/onset-options
# ---------------------------------------------------------------------------

class TestOnsetOptions:
    def test_onset_options_returns_200(self, client):
        resp = client.get("/api/health-check/onset-options")
        assert resp.status_code == 200

    def test_onset_options_has_onset(self, client):
        data = client.get("/api/health-check/onset-options").get_json()
        assert "onset" in data
        onset = data["onset"]
        assert "options" in onset
        assert isinstance(onset["options"], list)

    def test_onset_option_ids(self, client):
        data = client.get("/api/health-check/onset-options").get_json()
        option_ids = [o["id"] for o in data["onset"]["options"]]
        assert "acute" in option_ids
        assert "subacute" in option_ids
        assert "chronic" in option_ids


# ---------------------------------------------------------------------------
# GET /api/health-check/diseases
# ---------------------------------------------------------------------------

class TestDiseasesEndpoint:
    def test_diseases_returns_200(self, client):
        resp = client.get("/api/health-check/diseases")
        assert resp.status_code == 200

    def test_diseases_returns_list(self, client):
        data = client.get("/api/health-check/diseases").get_json()
        assert "diseases" in data
        assert isinstance(data["diseases"], list)

    def test_diseases_has_total(self, client):
        data = client.get("/api/health-check/diseases").get_json()
        assert "total" in data
        assert data["total"] == len(data["diseases"])


# ---------------------------------------------------------------------------
# POST /api/health-check/analyze
# ---------------------------------------------------------------------------

class TestAnalyzeEndpoint:
    def test_analyze_valid_symptoms(self, client):
        payload = {"symptoms": ["vomiting", "diarrhea"]}
        resp = client.post(
            "/api/health-check/analyze",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert resp.status_code == 200
        data = resp.get_json()
        assert "top_matches" in data
        assert "total_matches" in data
        assert "input" in data
        assert "disclaimer" in data

    def test_analyze_response_has_emergency_flag(self, client):
        payload = {"symptoms": ["vomiting", "bloating"]}
        resp = client.post(
            "/api/health-check/analyze",
            data=json.dumps(payload),
            content_type="application/json",
        )
        data = resp.get_json()
        assert "emergency_flag" in data

    def test_analyze_with_breed_id(self, client):
        payload = {"symptoms": ["coughing", "labored_breathing"], "breed_id": "french_bulldog"}
        resp = client.post(
            "/api/health-check/analyze",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["input"]["breed_id"] == "french_bulldog"
        # With a known breed, genetic info should be present
        assert "breed_genetic_info" in data

    def test_analyze_with_age_years(self, client):
        payload = {"symptoms": ["loss_of_appetite", "lethargy"], "age_years": 8}
        resp = client.post(
            "/api/health-check/analyze",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["input"]["age_years"] == 8

    def test_analyze_empty_symptoms_returns_400(self, client):
        payload = {"symptoms": []}
        resp = client.post(
            "/api/health-check/analyze",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert resp.status_code == 400
        data = resp.get_json()
        assert "error" in data

    def test_analyze_invalid_symptom_returns_400(self, client):
        payload = {"symptoms": ["nonexistent_symptom_xyz"]}
        resp = client.post(
            "/api/health-check/analyze",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert resp.status_code == 400
        data = resp.get_json()
        assert "error" in data

    def test_analyze_no_body_returns_400(self, client):
        resp = client.post(
            "/api/health-check/analyze",
            content_type="application/json",
        )
        assert resp.status_code == 400

    def test_analyze_has_consolidated_tests(self, client):
        payload = {"symptoms": ["vomiting", "diarrhea"]}
        resp = client.post(
            "/api/health-check/analyze",
            data=json.dumps(payload),
            content_type="application/json",
        )
        data = resp.get_json()
        assert "consolidated_priority_tests" in data

    def test_analyze_has_supervised_by(self, client):
        payload = {"symptoms": ["vomiting"]}
        resp = client.post(
            "/api/health-check/analyze",
            data=json.dumps(payload),
            content_type="application/json",
        )
        data = resp.get_json()
        assert "supervised_by" in data


# ---------------------------------------------------------------------------
# GET /api/health-check/breed-risks/<breed_id>
# ---------------------------------------------------------------------------

class TestBreedRisks:
    def test_breed_risks_known_breed(self, client):
        resp = client.get("/api/health-check/breed-risks/french_bulldog")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["breed_id"] == "french_bulldog"
        assert "total_elevated_risks" in data
        assert "disease_risks" in data
        assert isinstance(data["disease_risks"], list)

    def test_breed_risks_has_genetic_data(self, client):
        resp = client.get("/api/health-check/breed-risks/french_bulldog")
        data = resp.get_json()
        assert "breed_name_ja" in data
        assert "breed_name_en" in data
        assert "dna_tests" in data

    def test_breed_risks_unknown_breed(self, client):
        resp = client.get("/api/health-check/breed-risks/unknown_breed_xyz")
        assert resp.status_code == 404
        data = resp.get_json()
        assert "error" in data


# ---------------------------------------------------------------------------
# GET /api/health-check/disease-quality-report
# ---------------------------------------------------------------------------

class TestDiseaseQualityReport:
    def test_quality_report_returns_200(self, client):
        resp = client.get("/api/health-check/disease-quality-report")
        assert resp.status_code == 200

    def test_quality_report_structure(self, client):
        data = client.get("/api/health-check/disease-quality-report").get_json()
        assert "species" in data
        assert "total_diseases" in data
        assert "average_completeness" in data
        assert "diseases_with_missing_fields" in data
        assert "missing_field_counts" in data

    def test_quality_report_default_species_is_dog(self, client):
        data = client.get("/api/health-check/disease-quality-report").get_json()
        assert data["species"] == "dog"
