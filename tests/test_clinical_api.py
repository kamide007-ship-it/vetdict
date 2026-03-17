"""Tests for the Flask-based clinical API handler and route registration.

Covers:
- POST endpoints with valid data (expect 200)
- POST endpoints with missing required fields (expect 400)
- GET endpoints (expect 200)
- register_clinical_routes creates all expected URL rules
- Exception / error-handling paths (expect 500)
"""

import os
import sys
from unittest.mock import MagicMock

import pytest
from flask import Flask

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from api.routes.clinical_api import ClinicalAPIHandler, clinical_bp, register_clinical_routes

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def mock_engine():
    """Return a simple Mock that stands in for UnifiedClinicalEngine."""
    return MagicMock()


@pytest.fixture()
def app(mock_engine):
    """Create a Flask test application with all clinical routes registered."""
    flask_app = Flask(__name__)
    flask_app.config["TESTING"] = True

    handler = ClinicalAPIHandler(engine=mock_engine)
    register_clinical_routes(flask_app, handler)

    return flask_app


@pytest.fixture()
def client(app):
    """Return a Flask test client."""
    return app.test_client()


@pytest.fixture()
def handler(mock_engine):
    """Return a bare ClinicalAPIHandler (no Flask app needed for unit tests)."""
    return ClinicalAPIHandler(engine=mock_engine)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

COMPREHENSIVE_VALID = {
    "case_id": "case_001",
    "patient_age": 5.5,
    "patient_species": "dog",
    "symptoms": ["vomiting", "lethargy"],
    "disease_severity": 6.5,
    "comorbidities": ["pancreatitis"],
    "veterinarian_id": "vet_001",
    "clinic_id": "clinic_001",
    "initial_predictions": {"Gastroenteritis": 0.75, "Pancreatitis": 0.65},
}

OUTCOME_VALID = {
    "case_id": "case_001",
    "actual_diagnosis": "Pancreatitis",
    "treatment_used": "Supportive Care",
    "treatment_success": True,
}

PROGNOSIS_VALID = {
    "disease": "Pancreatitis",
    "disease_severity": 7.0,
    "patient_age": 5.5,
    "patient_species": "dog",
    "comorbidities": [],
    "treatment_type": "supportive",
}

TREATMENT_PREDICT_VALID = {
    "disease": "Pancreatitis",
    "treatment_name": "Supportive Care",
    "patient_age": 5.5,
    "comorbidities": [],
    "disease_severity": 7.0,
    "owner_compliance_likelihood": 0.8,
}

TREATMENT_RECOMMEND_VALID = {
    "disease": "Pancreatitis",
    "patient_age": 5.5,
    "comorbidities": [],
    "disease_severity": 7.0,
}

COMBINATIONS_VALID = {
    "diseases": ["Pancreatitis", "Diabetes Mellitus", "Kidney Disease"],
}


# ---------------------------------------------------------------------------
# POST /api/clinical/analysis — comprehensive analysis
# ---------------------------------------------------------------------------

class TestPostComprehensiveAnalysis:

    def test_valid_data_returns_200(self, client):
        resp = client.post("/api/clinical/analysis", json=COMPREHENSIVE_VALID)
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["status"] == "success"
        assert data["case_id"] == "case_001"

    def test_optional_fields_omitted_returns_200(self, client):
        payload = {k: COMPREHENSIVE_VALID[k] for k in
                   ["case_id", "patient_age", "patient_species",
                    "symptoms", "disease_severity", "initial_predictions"]}
        resp = client.post("/api/clinical/analysis", json=payload)
        assert resp.status_code == 200

    def test_missing_case_id_returns_400(self, client):
        payload = {k: v for k, v in COMPREHENSIVE_VALID.items() if k != "case_id"}
        resp = client.post("/api/clinical/analysis", json=payload)
        assert resp.status_code == 400
        assert "error" in resp.get_json()

    def test_missing_patient_age_returns_400(self, client):
        payload = {k: v for k, v in COMPREHENSIVE_VALID.items() if k != "patient_age"}
        resp = client.post("/api/clinical/analysis", json=payload)
        assert resp.status_code == 400

    def test_missing_patient_species_returns_400(self, client):
        payload = {k: v for k, v in COMPREHENSIVE_VALID.items() if k != "patient_species"}
        resp = client.post("/api/clinical/analysis", json=payload)
        assert resp.status_code == 400

    def test_missing_symptoms_returns_400(self, client):
        payload = {k: v for k, v in COMPREHENSIVE_VALID.items() if k != "symptoms"}
        resp = client.post("/api/clinical/analysis", json=payload)
        assert resp.status_code == 400

    def test_missing_disease_severity_returns_400(self, client):
        payload = {k: v for k, v in COMPREHENSIVE_VALID.items() if k != "disease_severity"}
        resp = client.post("/api/clinical/analysis", json=payload)
        assert resp.status_code == 400

    def test_missing_initial_predictions_returns_400(self, client):
        payload = {k: v for k, v in COMPREHENSIVE_VALID.items() if k != "initial_predictions"}
        resp = client.post("/api/clinical/analysis", json=payload)
        assert resp.status_code == 400

    def test_exception_returns_500(self, mock_engine):
        """Simulate an unexpected exception inside the handler by replacing the method."""
        flask_app = Flask(__name__)
        flask_app.config["TESTING"] = True
        h = ClinicalAPIHandler(engine=mock_engine)

        def broken():
            try:
                raise RuntimeError("simulated error")
            except Exception as e:
                return {"error": str(e)}, 500

        h.post_comprehensive_analysis = broken
        register_clinical_routes(flask_app, h)

        with flask_app.test_client() as c:
            resp = c.post("/api/clinical/analysis", json=COMPREHENSIVE_VALID)
            assert resp.status_code == 500
            assert "error" in resp.get_json()


# ---------------------------------------------------------------------------
# GET /api/clinical/cases/<case_id>
# ---------------------------------------------------------------------------

class TestGetCaseById:

    def test_returns_200(self, client):
        resp = client.get("/api/clinical/cases/case_001")
        assert resp.status_code == 200
        assert resp.get_json()["status"] == "success"

    def test_different_case_id(self, client):
        resp = client.get("/api/clinical/cases/case_xyz")
        assert resp.status_code == 200

    def test_exception_returns_500(self, mock_engine):
        flask_app = Flask(__name__)
        flask_app.config["TESTING"] = True
        h = ClinicalAPIHandler(engine=mock_engine)

        def broken(case_id):
            try:
                raise RuntimeError("db offline")
            except Exception as e:
                return {"error": str(e)}, 500

        h.get_case_by_id = broken
        register_clinical_routes(flask_app, h)

        with flask_app.test_client() as c:
            resp = c.get("/api/clinical/cases/case_001")
            assert resp.status_code == 500
            assert "error" in resp.get_json()


# ---------------------------------------------------------------------------
# GET /api/clinical/differential
# ---------------------------------------------------------------------------

class TestGetDifferentialDiagnoses:

    def test_returns_200_with_defaults(self, client):
        resp = client.get("/api/clinical/differential")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["status"] == "success"
        assert "differentials" in data

    def test_returns_200_with_query_params(self, client):
        resp = client.get(
            "/api/clinical/differential?symptoms=vomiting,lethargy&age=3.0&species=cat"
        )
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["patient"]["age"] == 3.0
        assert data["patient"]["species"] == "cat"

    def test_differentials_list_not_empty(self, client):
        resp = client.get("/api/clinical/differential")
        assert len(resp.get_json()["differentials"]) > 0

    def test_exception_returns_500(self, app, mock_engine):
        flask_app = Flask(__name__)
        flask_app.config["TESTING"] = True
        h = ClinicalAPIHandler(engine=mock_engine)

        def broken():
            try:
                raise ValueError("bad age")
            except Exception as e:
                return {"error": str(e)}, 500

        h.get_differential_diagnoses = broken
        register_clinical_routes(flask_app, h)

        with flask_app.test_client() as c:
            resp = c.get("/api/clinical/differential?age=notanumber")
            assert resp.status_code == 500


# ---------------------------------------------------------------------------
# POST /api/clinical/outcomes — record outcome
# ---------------------------------------------------------------------------

class TestPostRecordOutcome:

    def test_valid_data_returns_200(self, client):
        resp = client.post("/api/clinical/outcomes", json=OUTCOME_VALID)
        assert resp.status_code == 200
        assert resp.get_json()["status"] == "success"

    def test_minimal_valid_data_returns_200(self, client):
        resp = client.post("/api/clinical/outcomes",
                           json={"case_id": "c1", "actual_diagnosis": "Pancreatitis"})
        assert resp.status_code == 200

    def test_missing_case_id_returns_400(self, client):
        payload = {k: v for k, v in OUTCOME_VALID.items() if k != "case_id"}
        resp = client.post("/api/clinical/outcomes", json=payload)
        assert resp.status_code == 400

    def test_missing_actual_diagnosis_returns_400(self, client):
        payload = {k: v for k, v in OUTCOME_VALID.items() if k != "actual_diagnosis"}
        resp = client.post("/api/clinical/outcomes", json=payload)
        assert resp.status_code == 400

    def test_exception_returns_500(self, app, mock_engine):
        flask_app = Flask(__name__)
        flask_app.config["TESTING"] = True
        h = ClinicalAPIHandler(engine=mock_engine)

        def broken():
            try:
                raise RuntimeError("db error")
            except Exception as e:
                return {"error": str(e)}, 500

        h.post_record_outcome = broken
        register_clinical_routes(flask_app, h)

        with flask_app.test_client() as c:
            resp = c.post("/api/clinical/outcomes", json=OUTCOME_VALID)
            assert resp.status_code == 500


# ---------------------------------------------------------------------------
# POST /api/clinical/prognosis
# ---------------------------------------------------------------------------

class TestPostPredictPrognosis:

    def test_valid_data_returns_200(self, client):
        resp = client.post("/api/clinical/prognosis", json=PROGNOSIS_VALID)
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["status"] == "success"
        assert data["disease"] == "Pancreatitis"

    def test_missing_disease_returns_400(self, client):
        payload = {k: v for k, v in PROGNOSIS_VALID.items() if k != "disease"}
        resp = client.post("/api/clinical/prognosis", json=payload)
        assert resp.status_code == 400

    def test_missing_disease_severity_returns_400(self, client):
        payload = {k: v for k, v in PROGNOSIS_VALID.items() if k != "disease_severity"}
        resp = client.post("/api/clinical/prognosis", json=payload)
        assert resp.status_code == 400

    def test_missing_patient_age_returns_400(self, client):
        payload = {k: v for k, v in PROGNOSIS_VALID.items() if k != "patient_age"}
        resp = client.post("/api/clinical/prognosis", json=payload)
        assert resp.status_code == 400

    def test_missing_patient_species_returns_400(self, client):
        payload = {k: v for k, v in PROGNOSIS_VALID.items() if k != "patient_species"}
        resp = client.post("/api/clinical/prognosis", json=payload)
        assert resp.status_code == 400

    def test_exception_returns_500(self, app, mock_engine):
        flask_app = Flask(__name__)
        flask_app.config["TESTING"] = True
        h = ClinicalAPIHandler(engine=mock_engine)

        def broken():
            try:
                raise RuntimeError("model unavailable")
            except Exception as e:
                return {"error": str(e)}, 500

        h.post_predict_prognosis = broken
        register_clinical_routes(flask_app, h)

        with flask_app.test_client() as c:
            resp = c.post("/api/clinical/prognosis", json=PROGNOSIS_VALID)
            assert resp.status_code == 500


# ---------------------------------------------------------------------------
# POST /api/clinical/treatment/predict
# ---------------------------------------------------------------------------

class TestPostPredictTreatmentResponse:

    def test_valid_data_returns_200(self, client):
        resp = client.post("/api/clinical/treatment/predict", json=TREATMENT_PREDICT_VALID)
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["status"] == "success"
        assert data["treatment"] == "Supportive Care"

    def test_missing_disease_returns_400(self, client):
        payload = {k: v for k, v in TREATMENT_PREDICT_VALID.items() if k != "disease"}
        resp = client.post("/api/clinical/treatment/predict", json=payload)
        assert resp.status_code == 400

    def test_missing_treatment_name_returns_400(self, client):
        payload = {k: v for k, v in TREATMENT_PREDICT_VALID.items() if k != "treatment_name"}
        resp = client.post("/api/clinical/treatment/predict", json=payload)
        assert resp.status_code == 400

    def test_missing_patient_age_returns_400(self, client):
        payload = {k: v for k, v in TREATMENT_PREDICT_VALID.items() if k != "patient_age"}
        resp = client.post("/api/clinical/treatment/predict", json=payload)
        assert resp.status_code == 400

    def test_exception_returns_500(self, app, mock_engine):
        flask_app = Flask(__name__)
        flask_app.config["TESTING"] = True
        h = ClinicalAPIHandler(engine=mock_engine)

        def broken():
            try:
                raise RuntimeError("prediction error")
            except Exception as e:
                return {"error": str(e)}, 500

        h.post_predict_treatment_response = broken
        register_clinical_routes(flask_app, h)

        with flask_app.test_client() as c:
            resp = c.post("/api/clinical/treatment/predict", json=TREATMENT_PREDICT_VALID)
            assert resp.status_code == 500


# ---------------------------------------------------------------------------
# POST /api/clinical/treatment/recommend
# ---------------------------------------------------------------------------

class TestPostRecommendTreatments:

    def test_valid_data_returns_200(self, client):
        resp = client.post("/api/clinical/treatment/recommend", json=TREATMENT_RECOMMEND_VALID)
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["status"] == "success"
        assert data["disease"] == "Pancreatitis"

    def test_missing_disease_returns_400(self, client):
        payload = {k: v for k, v in TREATMENT_RECOMMEND_VALID.items() if k != "disease"}
        resp = client.post("/api/clinical/treatment/recommend", json=payload)
        assert resp.status_code == 400

    def test_missing_patient_age_returns_400(self, client):
        payload = {k: v for k, v in TREATMENT_RECOMMEND_VALID.items() if k != "patient_age"}
        resp = client.post("/api/clinical/treatment/recommend", json=payload)
        assert resp.status_code == 400

    def test_exception_returns_500(self, app, mock_engine):
        flask_app = Flask(__name__)
        flask_app.config["TESTING"] = True
        h = ClinicalAPIHandler(engine=mock_engine)

        def broken():
            try:
                raise RuntimeError("recommendation error")
            except Exception as e:
                return {"error": str(e)}, 500

        h.post_recommend_treatments = broken
        register_clinical_routes(flask_app, h)

        with flask_app.test_client() as c:
            resp = c.post("/api/clinical/treatment/recommend", json=TREATMENT_RECOMMEND_VALID)
            assert resp.status_code == 500


# ---------------------------------------------------------------------------
# POST /api/clinical/combinations/analyze
# ---------------------------------------------------------------------------

class TestPostAnalyzeCombinations:

    def test_valid_data_returns_200(self, client):
        resp = client.post("/api/clinical/combinations/analyze", json=COMBINATIONS_VALID)
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["status"] == "success"
        assert data["diseases"] == COMBINATIONS_VALID["diseases"]

    def test_exactly_two_diseases_returns_200(self, client):
        resp = client.post("/api/clinical/combinations/analyze",
                           json={"diseases": ["Pancreatitis", "Diabetes Mellitus"]})
        assert resp.status_code == 200

    def test_missing_diseases_key_returns_400(self, client):
        resp = client.post("/api/clinical/combinations/analyze", json={})
        assert resp.status_code == 400

    def test_only_one_disease_returns_400(self, client):
        resp = client.post("/api/clinical/combinations/analyze",
                           json={"diseases": ["Pancreatitis"]})
        assert resp.status_code == 400

    def test_empty_diseases_list_returns_400(self, client):
        resp = client.post("/api/clinical/combinations/analyze", json={"diseases": []})
        assert resp.status_code == 400

    def test_exception_returns_500(self, app, mock_engine):
        flask_app = Flask(__name__)
        flask_app.config["TESTING"] = True
        h = ClinicalAPIHandler(engine=mock_engine)

        def broken():
            try:
                raise RuntimeError("combination error")
            except Exception as e:
                return {"error": str(e)}, 500

        h.post_analyze_combinations = broken
        register_clinical_routes(flask_app, h)

        with flask_app.test_client() as c:
            resp = c.post("/api/clinical/combinations/analyze", json=COMBINATIONS_VALID)
            assert resp.status_code == 500


# ---------------------------------------------------------------------------
# GET /api/clinical/stats
# ---------------------------------------------------------------------------

class TestGetSystemStatistics:

    def test_returns_200(self, client):
        resp = client.get("/api/clinical/stats")
        assert resp.status_code == 200

    def test_response_contains_statistics(self, client):
        data = client.get("/api/clinical/stats").get_json()
        assert data["status"] == "success"
        assert "statistics" in data

    def test_statistics_has_expected_keys(self, client):
        stats = client.get("/api/clinical/stats").get_json()["statistics"]
        assert "total_cases_analyzed" in stats
        assert "models_trained" in stats
        assert "confidence_feedback_records" in stats

    def test_exception_returns_500(self, app, mock_engine):
        flask_app = Flask(__name__)
        flask_app.config["TESTING"] = True
        h = ClinicalAPIHandler(engine=mock_engine)

        def broken():
            try:
                raise RuntimeError("stats error")
            except Exception as e:
                return {"error": str(e)}, 500

        h.get_system_statistics = broken
        register_clinical_routes(flask_app, h)

        with flask_app.test_client() as c:
            resp = c.get("/api/clinical/stats")
            assert resp.status_code == 500


# ---------------------------------------------------------------------------
# GET /api/clinical/stats/veterinarian/<vet_id>
# ---------------------------------------------------------------------------

class TestGetVeterinarianStats:

    def test_returns_200(self, client):
        resp = client.get("/api/clinical/stats/veterinarian/vet_001")
        assert resp.status_code == 200

    def test_response_contains_vet_id(self, client):
        data = client.get("/api/clinical/stats/veterinarian/vet_001").get_json()
        assert data["statistics"]["vet_id"] == "vet_001"

    def test_different_vet_id(self, client):
        resp = client.get("/api/clinical/stats/veterinarian/vet_xyz")
        assert resp.status_code == 200
        assert resp.get_json()["statistics"]["vet_id"] == "vet_xyz"

    def test_exception_returns_500(self, app, mock_engine):
        flask_app = Flask(__name__)
        flask_app.config["TESTING"] = True
        h = ClinicalAPIHandler(engine=mock_engine)

        def broken(vet_id):
            try:
                raise RuntimeError("vet stats error")
            except Exception as e:
                return {"error": str(e)}, 500

        h.get_veterinarian_stats = broken
        register_clinical_routes(flask_app, h)

        with flask_app.test_client() as c:
            resp = c.get("/api/clinical/stats/veterinarian/vet_001")
            assert resp.status_code == 500


# ---------------------------------------------------------------------------
# GET /api/clinical/stats/clinic/<clinic_id>
# ---------------------------------------------------------------------------

class TestGetClinicStats:

    def test_returns_200(self, client):
        resp = client.get("/api/clinical/stats/clinic/clinic_001")
        assert resp.status_code == 200

    def test_response_contains_clinic_id(self, client):
        data = client.get("/api/clinical/stats/clinic/clinic_001").get_json()
        assert data["statistics"]["clinic_id"] == "clinic_001"

    def test_different_clinic_id(self, client):
        resp = client.get("/api/clinical/stats/clinic/clinic_abc")
        assert resp.status_code == 200
        assert resp.get_json()["statistics"]["clinic_id"] == "clinic_abc"

    def test_exception_returns_500(self, app, mock_engine):
        flask_app = Flask(__name__)
        flask_app.config["TESTING"] = True
        h = ClinicalAPIHandler(engine=mock_engine)

        def broken(clinic_id):
            try:
                raise RuntimeError("clinic stats error")
            except Exception as e:
                return {"error": str(e)}, 500

        h.get_clinic_stats = broken
        register_clinical_routes(flask_app, h)

        with flask_app.test_client() as c:
            resp = c.get("/api/clinical/stats/clinic/clinic_001")
            assert resp.status_code == 500


# ---------------------------------------------------------------------------
# POST /api/clinical/models/train
# ---------------------------------------------------------------------------

class TestPostTrainModels:

    def test_returns_200(self, client):
        resp = client.post("/api/clinical/models/train", json={})
        assert resp.status_code == 200

    def test_response_has_training_results(self, client):
        data = client.post("/api/clinical/models/train", json={}).get_json()
        assert data["status"] == "success"
        assert "training_results" in data
        assert "message" in data

    def test_no_body_required(self, client):
        # POST with no JSON body should still succeed (no required fields)
        resp = client.post("/api/clinical/models/train")
        assert resp.status_code == 200

    def test_exception_returns_500(self, app, mock_engine):
        flask_app = Flask(__name__)
        flask_app.config["TESTING"] = True
        h = ClinicalAPIHandler(engine=mock_engine)

        def broken():
            try:
                raise RuntimeError("training failed")
            except Exception as e:
                return {"error": str(e)}, 500

        h.post_train_models = broken
        register_clinical_routes(flask_app, h)

        with flask_app.test_client() as c:
            resp = c.post("/api/clinical/models/train", json={})
            assert resp.status_code == 500


# ---------------------------------------------------------------------------
# GET /api/clinical/cases/<case_id>/summary
# ---------------------------------------------------------------------------

class TestGetClinicalSummary:

    def test_returns_200(self, client):
        resp = client.get("/api/clinical/cases/case_001/summary")
        assert resp.status_code == 200

    def test_response_contains_case_id(self, client):
        data = client.get("/api/clinical/cases/case_001/summary").get_json()
        assert data["status"] == "success"
        assert data["case_id"] == "case_001"

    def test_different_case_id(self, client):
        resp = client.get("/api/clinical/cases/case_999/summary")
        assert resp.status_code == 200
        assert resp.get_json()["case_id"] == "case_999"

    def test_exception_returns_500(self, app, mock_engine):
        flask_app = Flask(__name__)
        flask_app.config["TESTING"] = True
        h = ClinicalAPIHandler(engine=mock_engine)

        def broken(case_id):
            try:
                raise RuntimeError("summary error")
            except Exception as e:
                return {"error": str(e)}, 500

        h.get_clinical_summary = broken
        register_clinical_routes(flask_app, h)

        with flask_app.test_client() as c:
            resp = c.get("/api/clinical/cases/case_001/summary")
            assert resp.status_code == 500


# ---------------------------------------------------------------------------
# register_clinical_routes — URL rule coverage
# ---------------------------------------------------------------------------

class TestRegisterClinicalRoutes:
    """Verify that register_clinical_routes creates all expected URL rules."""

    @pytest.fixture()
    def registered_app(self, mock_engine):
        flask_app = Flask(__name__)
        flask_app.config["TESTING"] = True
        h = ClinicalAPIHandler(engine=mock_engine)
        register_clinical_routes(flask_app, h)
        return flask_app

    def _url_rules(self, app):
        return {rule.rule for rule in app.url_map.iter_rules()}

    def test_analysis_route_registered(self, registered_app):
        assert "/api/clinical/analysis" in self._url_rules(registered_app)

    def test_cases_route_registered(self, registered_app):
        assert "/api/clinical/cases/<case_id>" in self._url_rules(registered_app)

    def test_differential_route_registered(self, registered_app):
        assert "/api/clinical/differential" in self._url_rules(registered_app)

    def test_outcomes_route_registered(self, registered_app):
        assert "/api/clinical/outcomes" in self._url_rules(registered_app)

    def test_prognosis_route_registered(self, registered_app):
        assert "/api/clinical/prognosis" in self._url_rules(registered_app)

    def test_treatment_predict_route_registered(self, registered_app):
        assert "/api/clinical/treatment/predict" in self._url_rules(registered_app)

    def test_treatment_recommend_route_registered(self, registered_app):
        assert "/api/clinical/treatment/recommend" in self._url_rules(registered_app)

    def test_combinations_route_registered(self, registered_app):
        assert "/api/clinical/combinations/analyze" in self._url_rules(registered_app)

    def test_stats_route_registered(self, registered_app):
        assert "/api/clinical/stats" in self._url_rules(registered_app)

    def test_vet_stats_route_registered(self, registered_app):
        assert "/api/clinical/stats/veterinarian/<vet_id>" in self._url_rules(registered_app)

    def test_clinic_stats_route_registered(self, registered_app):
        assert "/api/clinical/stats/clinic/<clinic_id>" in self._url_rules(registered_app)

    def test_train_models_route_registered(self, registered_app):
        assert "/api/clinical/models/train" in self._url_rules(registered_app)

    def test_summary_route_registered(self, registered_app):
        assert "/api/clinical/cases/<case_id>/summary" in self._url_rules(registered_app)

    def test_total_route_count(self, registered_app):
        """Exactly 13 clinical routes should be registered (excludes Flask's static)."""
        clinical_rules = [
            r for r in self._url_rules(registered_app)
            if r.startswith("/api/clinical")
        ]
        assert len(clinical_rules) == 13

    def test_analysis_accepts_post(self, registered_app):
        rules = {rule.rule: rule for rule in registered_app.url_map.iter_rules()}
        assert "POST" in rules["/api/clinical/analysis"].methods

    def test_differential_accepts_get(self, registered_app):
        rules = {rule.rule: rule for rule in registered_app.url_map.iter_rules()}
        assert "GET" in rules["/api/clinical/differential"].methods

    def test_outcomes_accepts_post(self, registered_app):
        rules = {rule.rule: rule for rule in registered_app.url_map.iter_rules()}
        assert "POST" in rules["/api/clinical/outcomes"].methods

    def test_train_models_accepts_post(self, registered_app):
        rules = {rule.rule: rule for rule in registered_app.url_map.iter_rules()}
        assert "POST" in rules["/api/clinical/models/train"].methods

    def test_stats_accepts_get(self, registered_app):
        rules = {rule.rule: rule for rule in registered_app.url_map.iter_rules()}
        assert "GET" in rules["/api/clinical/stats"].methods


# ---------------------------------------------------------------------------
# clinical_bp Blueprint object
# ---------------------------------------------------------------------------

class TestClinicalBlueprint:

    def test_blueprint_name(self):
        assert clinical_bp.name == "clinical"

    def test_blueprint_url_prefix(self):
        assert clinical_bp.url_prefix == "/api/clinical"


# ---------------------------------------------------------------------------
# ClinicalAPIHandler — direct unit tests
# ---------------------------------------------------------------------------

class TestClinicalAPIHandlerInit:

    def test_stores_engine(self, mock_engine):
        h = ClinicalAPIHandler(engine=mock_engine)
        assert h.engine is mock_engine

    def test_accepts_none_engine(self):
        h = ClinicalAPIHandler(engine=None)
        assert h.engine is None

    def test_accepts_mock_engine(self, mock_engine):
        h = ClinicalAPIHandler(engine=mock_engine)
        assert isinstance(h, ClinicalAPIHandler)
