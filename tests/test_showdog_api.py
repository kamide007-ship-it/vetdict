"""Tests for api/showdog_api.py — VetDict Flask application.

Covers:
- GET /api/health — health check route and response structure
- POST /api/analyze-symptoms — input validation and dispatch paths
- GET/POST /api/status, /api/logs, /api/evaluate, /api/feedback, /api/patrol — RECO2 routes
- POST /api/r3/analyze_input, /api/r3/analyze_output, /api/r3/chat — RECO3 routes
- GET /api/r3/config — RECO3 config route
- Static file routes (/, /favicon.ico, /<path:filename>)
- ensure_json_response decorator behaviour
- Security headers applied by after_request hook
- Error handlers (404, 500)
- Module-level constants (VERSION, BUILD)
"""

import os
import sys
from unittest.mock import MagicMock, patch

import pytest

# Ensure repo root is importable
ROOT = os.path.join(os.path.dirname(__file__), "..")
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import api.showdog_api as showdog_mod

APP = showdog_mod.app
APP.config["TESTING"] = True

MODULE = "api.showdog_api"


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def client():
    """Shared test client; suitable for stateless GET/POST tests."""
    with APP.test_client() as c:
        yield c


# ---------------------------------------------------------------------------
# Module-level constants
# ---------------------------------------------------------------------------


class TestModuleConstants:
    def test_version_is_string(self):
        assert isinstance(showdog_mod.VERSION, str)
        assert len(showdog_mod.VERSION) > 0

    def test_build_is_string(self):
        assert isinstance(showdog_mod.BUILD, str)
        assert len(showdog_mod.BUILD) > 0

    def test_version_has_three_parts(self):
        parts = showdog_mod.VERSION.split(".")
        assert len(parts) == 3
        for part in parts:
            assert part.isdigit(), f"Non-numeric version part: {part!r}"

    def test_build_date_format(self):
        import re

        assert re.match(r"^\d{4}-\d{2}-\d{2}$", showdog_mod.BUILD), (
            f"BUILD '{showdog_mod.BUILD}' is not YYYY-MM-DD format"
        )

    def test_availability_flags_are_booleans(self):
        for attr in (
            "SYMPTOM_CHECKER_AVAILABLE",
            "SPECIES_ANALYZER_AVAILABLE",
            "HEALTH_CHECKER_AVAILABLE",
            "DIAGNOSTIC_CHAT_AVAILABLE",
            "DRUG_DICTIONARY_AVAILABLE",
            "RECO2_AVAILABLE",
        ):
            val = getattr(showdog_mod, attr)
            assert isinstance(val, bool), f"{attr} is not bool: {val!r}"


# ---------------------------------------------------------------------------
# GET /api/health
# ---------------------------------------------------------------------------


class TestHealthEndpoint:
    def test_returns_200(self, client):
        assert client.get("/api/health").status_code == 200

    def test_response_is_json(self, client):
        resp = client.get("/api/health")
        assert resp.content_type.startswith("application/json")

    def test_status_field_is_healthy(self, client):
        data = client.get("/api/health").get_json()
        assert data["status"] == "healthy"

    def test_version_field_present_and_correct(self, client):
        data = client.get("/api/health").get_json()
        assert data.get("version") == showdog_mod.VERSION

    def test_build_field_present(self, client):
        data = client.get("/api/health").get_json()
        assert "build" in data

    def test_features_dict_present(self, client):
        data = client.get("/api/health").get_json()
        assert isinstance(data.get("features"), dict)

    def test_features_has_all_expected_keys(self, client):
        features = client.get("/api/health").get_json()["features"]
        expected_keys = {
            "symptom_checker",
            "species_analyzer",
            "health_checker",
            "diagnostic_chat",
            "drug_dictionary",
            "reco2",
        }
        assert expected_keys.issubset(features.keys())

    def test_all_feature_values_are_booleans(self, client):
        features = client.get("/api/health").get_json()["features"]
        for key, val in features.items():
            assert isinstance(val, bool), f"Feature '{key}' = {val!r} is not bool"

    def test_health_is_get_only(self, client):
        assert client.post("/api/health").status_code == 405


# ---------------------------------------------------------------------------
# POST /api/analyze-symptoms — input validation
# ---------------------------------------------------------------------------


class TestAnalyzeSymptomsValidation:
    def test_missing_body_returns_400(self, client):
        resp = client.post(
            "/api/analyze-symptoms",
            data="",
            content_type="application/json",
        )
        assert resp.status_code == 400

    def test_no_symptoms_key_returns_400(self, client):
        resp = client.post("/api/analyze-symptoms", json={"species": "dog"})
        assert resp.status_code == 400
        assert "error" in resp.get_json()

    def test_empty_symptoms_list_returns_400(self, client):
        resp = client.post("/api/analyze-symptoms", json={"symptoms": []})
        assert resp.status_code == 400

    def test_non_list_symptoms_returns_400(self, client):
        resp = client.post("/api/analyze-symptoms", json={"symptoms": "vomiting"})
        assert resp.status_code == 400

    def test_null_symptoms_returns_400(self, client):
        resp = client.post("/api/analyze-symptoms", json={"symptoms": None})
        assert resp.status_code == 400

    def test_error_response_is_json(self, client):
        resp = client.post("/api/analyze-symptoms", json={})
        assert resp.content_type.startswith("application/json")


# ---------------------------------------------------------------------------
# POST /api/analyze-symptoms — successful dispatch (dog)
# ---------------------------------------------------------------------------


class TestAnalyzeSymptomsSuccessfulDog:
    def test_dog_default_species_returns_200(self, client):
        with patch(f"{MODULE}.analyze_symptoms", return_value={"diseases": [], "tests": []}):
            resp = client.post("/api/analyze-symptoms", json={"symptoms": ["vomiting"]})
        assert resp.status_code == 200

    def test_dog_explicit_species_returns_200(self, client):
        with patch(f"{MODULE}.analyze_symptoms", return_value={"diseases": [], "tests": []}):
            resp = client.post(
                "/api/analyze-symptoms",
                json={"symptoms": ["lethargy"], "species": "dog"},
            )
        assert resp.status_code == 200

    def test_breed_passed_to_analyzer(self, client):
        mock_fn = MagicMock(return_value={"diseases": [], "tests": []})
        with patch(f"{MODULE}.analyze_symptoms", mock_fn):
            client.post(
                "/api/analyze-symptoms",
                json={"symptoms": ["cough"], "breed": "Labrador"},
            )
        mock_fn.assert_called_once()
        _, kwargs = mock_fn.call_args
        assert kwargs.get("breed") == "Labrador"

    def test_value_error_from_analyzer_returns_400(self, client):
        with patch(f"{MODULE}.analyze_symptoms", side_effect=ValueError("bad symptom")):
            resp = client.post("/api/analyze-symptoms", json={"symptoms": ["??"]})
        assert resp.status_code == 400

    def test_runtime_error_from_analyzer_returns_500(self, client):
        with patch(f"{MODULE}.analyze_symptoms", side_effect=RuntimeError("db error")):
            resp = client.post("/api/analyze-symptoms", json={"symptoms": ["cough"]})
        assert resp.status_code == 500

    def test_symptom_checker_unavailable_returns_500(self, client):
        with patch(f"{MODULE}.SYMPTOM_CHECKER_AVAILABLE", False):
            resp = client.post("/api/analyze-symptoms", json={"symptoms": ["vomiting"]})
        assert resp.status_code == 500
        assert "error" in resp.get_json()


# ---------------------------------------------------------------------------
# POST /api/analyze-symptoms — non-dog species dispatch
# ---------------------------------------------------------------------------


class TestAnalyzeSymptomsNonDog:
    def test_cat_uses_species_analyzer(self, client):
        mock_fn = MagicMock(return_value={"diseases": [], "tests": []})
        with patch(f"{MODULE}.analyze_species_symptoms", mock_fn):
            resp = client.post(
                "/api/analyze-symptoms",
                json={"symptoms": ["sneezing"], "species": "cat"},
            )
        assert resp.status_code == 200
        mock_fn.assert_called_once()

    def test_non_dog_passes_age_stage(self, client):
        mock_fn = MagicMock(return_value={"diseases": [], "tests": []})
        with patch(f"{MODULE}.analyze_species_symptoms", mock_fn):
            client.post(
                "/api/analyze-symptoms",
                json={"symptoms": ["diarrhea"], "species": "rabbit", "age_stage": "adult"},
            )
        args, _ = mock_fn.call_args
        assert "adult" in args

    def test_species_analyzer_unavailable_returns_500(self, client):
        with (
            patch(f"{MODULE}.SPECIES_ANALYZER_AVAILABLE", False),
            patch(f"{MODULE}.analyze_species_symptoms", None),
        ):
            resp = client.post(
                "/api/analyze-symptoms",
                json={"symptoms": ["sneezing"], "species": "cat"},
            )
        assert resp.status_code == 500

    def test_value_error_from_species_analyzer_returns_400(self, client):
        with patch(f"{MODULE}.analyze_species_symptoms", side_effect=ValueError("unknown")):
            resp = client.post(
                "/api/analyze-symptoms",
                json={"symptoms": ["x"], "species": "ferret"},
            )
        assert resp.status_code == 400


# ---------------------------------------------------------------------------
# RECO2 routes — module unavailable  →  503
# ---------------------------------------------------------------------------


class TestReco2UnavailableRoutes:
    """All RECO2/RECO3 routes must return 503 when RECO2_AVAILABLE is False."""

    def _assert_503(self, client, method, path, **kwargs):
        with patch(f"{MODULE}.RECO2_AVAILABLE", False):
            resp = client.get(path, **kwargs) if method == "GET" else client.post(path, **kwargs)
        assert resp.status_code == 503, f"{method} {path} returned {resp.status_code}, expected 503"
        assert "error" in resp.get_json()

    def test_status_returns_503(self, client):
        self._assert_503(client, "GET", "/api/status")

    def test_logs_returns_503(self, client):
        self._assert_503(client, "GET", "/api/logs")

    def test_evaluate_returns_503(self, client):
        self._assert_503(client, "POST", "/api/evaluate", json={})

    def test_feedback_returns_503(self, client):
        self._assert_503(client, "POST", "/api/feedback", json={})

    def test_patrol_returns_503(self, client):
        self._assert_503(client, "POST", "/api/patrol", json={})

    def test_r3_analyze_input_returns_503(self, client):
        self._assert_503(client, "POST", "/api/r3/analyze_input", json={"text": "hi"})

    def test_r3_analyze_output_returns_503(self, client):
        self._assert_503(client, "POST", "/api/r3/analyze_output", json={"text": "hi"})

    def test_r3_chat_returns_503(self, client):
        self._assert_503(client, "POST", "/api/r3/chat", json={"prompt": "hello"})

    def test_r3_config_returns_503(self, client):
        self._assert_503(client, "GET", "/api/r3/config")


# ---------------------------------------------------------------------------
# GET /api/status
# ---------------------------------------------------------------------------


class TestReco2StatusRoute:
    def test_returns_200(self, client):
        with patch(f"{MODULE}.reco2_get_status", return_value={"status": "ok"}):
            resp = client.get("/api/status")
        assert resp.status_code == 200

    def test_response_is_json(self, client):
        with patch(f"{MODULE}.reco2_get_status", return_value={"status": "ok"}):
            resp = client.get("/api/status")
        assert resp.content_type.startswith("application/json")

    def test_delegates_to_get_status(self, client):
        mock_fn = MagicMock(return_value={"status": "running"})
        with patch(f"{MODULE}.reco2_get_status", mock_fn):
            client.get("/api/status")
        mock_fn.assert_called_once()


# ---------------------------------------------------------------------------
# GET /api/logs
# ---------------------------------------------------------------------------


class TestReco2LogsRoute:
    def test_returns_200(self, client):
        with patch(f"{MODULE}.reco2_get_logs", return_value={"logs": []}):
            resp = client.get("/api/logs")
        assert resp.status_code == 200

    def test_default_limit_is_50(self, client):
        mock_fn = MagicMock(return_value={"logs": []})
        with patch(f"{MODULE}.reco2_get_logs", mock_fn):
            client.get("/api/logs")
        mock_fn.assert_called_once_with(limit=50)

    def test_custom_limit_via_query_param(self, client):
        mock_fn = MagicMock(return_value={"logs": []})
        with patch(f"{MODULE}.reco2_get_logs", mock_fn):
            client.get("/api/logs?limit=10")
        mock_fn.assert_called_once_with(limit=10)

    def test_invalid_limit_falls_back_to_50(self, client):
        mock_fn = MagicMock(return_value={"logs": []})
        with patch(f"{MODULE}.reco2_get_logs", mock_fn):
            client.get("/api/logs?limit=notanumber")
        mock_fn.assert_called_once_with(limit=50)


# ---------------------------------------------------------------------------
# POST /api/evaluate
# ---------------------------------------------------------------------------


class TestReco2EvaluateRoute:
    def test_returns_200_with_payload(self, client):
        with patch(f"{MODULE}.reco2_evaluate_payload", return_value={"result": "pass"}):
            resp = client.post("/api/evaluate", json={"input": "test"})
        assert resp.status_code == 200

    def test_delegates_payload_to_evaluate(self, client):
        mock_fn = MagicMock(return_value={"result": "pass"})
        with patch(f"{MODULE}.reco2_evaluate_payload", mock_fn):
            client.post("/api/evaluate", json={"foo": "bar"})
        mock_fn.assert_called_once_with({"foo": "bar"})

    def test_response_is_json(self, client):
        with patch(f"{MODULE}.reco2_evaluate_payload", return_value={"result": "pass"}):
            resp = client.post("/api/evaluate", json={})
        assert resp.content_type.startswith("application/json")


# ---------------------------------------------------------------------------
# POST /api/feedback
# ---------------------------------------------------------------------------


class TestReco2FeedbackRoute:
    def test_returns_200(self, client):
        with patch(f"{MODULE}.reco2_record_feedback", return_value={"recorded": True}):
            resp = client.post("/api/feedback", json={"rating": 5})
        assert resp.status_code == 200

    def test_empty_body_accepted(self, client):
        with patch(f"{MODULE}.reco2_record_feedback", return_value={"recorded": True}):
            resp = client.post("/api/feedback", json={})
        assert resp.status_code == 200

    def test_delegates_to_record_feedback(self, client):
        mock_fn = MagicMock(return_value={"recorded": True})
        with patch(f"{MODULE}.reco2_record_feedback", mock_fn):
            client.post("/api/feedback", json={"rating": 4})
        mock_fn.assert_called_once()

    def test_tuple_response_forwarded_correctly(self, client):
        """When record_feedback returns (body, status), the status code is preserved."""
        with patch(f"{MODULE}.reco2_record_feedback", return_value=({"ok": True}, 201)):
            resp = client.post("/api/feedback", json={})
        assert resp.status_code == 201


# ---------------------------------------------------------------------------
# POST /api/patrol
# ---------------------------------------------------------------------------


class TestReco2PatrolRoute:
    def test_returns_200(self, client):
        with patch(f"{MODULE}.reco2_patrol", return_value={"patrolled": True}):
            resp = client.post("/api/patrol", json={})
        assert resp.status_code == 200

    def test_delegates_with_manual_true(self, client):
        mock_fn = MagicMock(return_value={"patrolled": True})
        with patch(f"{MODULE}.reco2_patrol", mock_fn):
            client.post("/api/patrol", json={})
        mock_fn.assert_called_once_with(manual=True)


# ---------------------------------------------------------------------------
# POST /api/r3/analyze_input
# ---------------------------------------------------------------------------


class TestReco3AnalyzeInputRoute:
    def test_returns_200_with_text(self, client):
        with patch(f"{MODULE}.input_gate") as mock_gate:
            mock_gate.analyze.return_value = {"score": 0.0, "flags": []}
            with patch(f"{MODULE}.load_reco2_config", return_value={}):
                resp = client.post("/api/r3/analyze_input", json={"text": "Is my dog sick?"})
        assert resp.status_code == 200

    def test_empty_body_returns_200(self, client):
        with patch(f"{MODULE}.input_gate") as mock_gate:
            mock_gate.analyze.return_value = {"score": 0.0, "flags": []}
            with patch(f"{MODULE}.load_reco2_config", return_value={}):
                resp = client.post("/api/r3/analyze_input", json={})
        assert resp.status_code == 200

    def test_text_passed_to_input_gate(self, client):
        with patch(f"{MODULE}.input_gate") as mock_gate:
            mock_gate.analyze.return_value = {"score": 0.0, "flags": []}
            with patch(f"{MODULE}.load_reco2_config", return_value={}):
                client.post("/api/r3/analyze_input", json={"text": "hello world"})
        mock_gate.analyze.assert_called_once()
        args, _ = mock_gate.analyze.call_args
        assert args[0] == "hello world"

    def test_non_string_text_coerced_to_string(self, client):
        with patch(f"{MODULE}.input_gate") as mock_gate:
            mock_gate.analyze.return_value = {"score": 0.0, "flags": []}
            with patch(f"{MODULE}.load_reco2_config", return_value={}):
                client.post("/api/r3/analyze_input", json={"text": 42})
        args, _ = mock_gate.analyze.call_args
        assert args[0] == "42"

    def test_config_weights_forwarded(self, client):
        cfg = {
            "input_w_ambiguity": "0.15",
            "input_w_assertion": "0.20",
            "input_w_emotion": "0.35",
            "input_w_unrealistic": "0.30",
        }
        with patch(f"{MODULE}.input_gate") as mock_gate:
            mock_gate.analyze.return_value = {"score": 0.0, "flags": []}
            with patch(f"{MODULE}.load_reco2_config", return_value=cfg):
                client.post("/api/r3/analyze_input", json={"text": "test"})
        _, kwargs = mock_gate.analyze.call_args
        assert kwargs["w_ambiguity"] == pytest.approx(0.15)
        assert kwargs["w_assertion"] == pytest.approx(0.20)
        assert kwargs["w_emotion"] == pytest.approx(0.35)
        assert kwargs["w_unrealistic"] == pytest.approx(0.30)


# ---------------------------------------------------------------------------
# POST /api/r3/analyze_output
# ---------------------------------------------------------------------------


class TestReco3AnalyzeOutputRoute:
    def test_returns_200_with_text(self, client):
        with patch(f"{MODULE}.output_gate") as mock_gate:
            mock_gate.analyze.return_value = {"score": 0.0, "flags": []}
            with patch(f"{MODULE}.load_reco2_config", return_value={}):
                resp = client.post("/api/r3/analyze_output", json={"text": "The dog is fine."})
        assert resp.status_code == 200

    def test_empty_body_returns_200(self, client):
        with patch(f"{MODULE}.output_gate") as mock_gate:
            mock_gate.analyze.return_value = {"score": 0.0, "flags": []}
            with patch(f"{MODULE}.load_reco2_config", return_value={}):
                resp = client.post("/api/r3/analyze_output", json={})
        assert resp.status_code == 200

    def test_text_passed_to_output_gate(self, client):
        with patch(f"{MODULE}.output_gate") as mock_gate:
            mock_gate.analyze.return_value = {"score": 0.0, "flags": []}
            with patch(f"{MODULE}.load_reco2_config", return_value={}):
                client.post("/api/r3/analyze_output", json={"text": "result text"})
        args, _ = mock_gate.analyze.call_args
        assert args[0] == "result text"

    def test_config_weights_forwarded(self, client):
        cfg = {
            "output_w_assertion": "0.30",
            "output_w_evidence": "0.30",
            "output_w_contradiction": "0.25",
            "output_w_provocative": "0.15",
        }
        with patch(f"{MODULE}.output_gate") as mock_gate:
            mock_gate.analyze.return_value = {"score": 0.0, "flags": []}
            with patch(f"{MODULE}.load_reco2_config", return_value=cfg):
                client.post("/api/r3/analyze_output", json={"text": "test"})
        _, kwargs = mock_gate.analyze.call_args
        assert kwargs["w_assertion"] == pytest.approx(0.30)
        assert kwargs["w_evidence"] == pytest.approx(0.30)
        assert kwargs["w_contradiction"] == pytest.approx(0.25)
        assert kwargs["w_provocative"] == pytest.approx(0.15)


# ---------------------------------------------------------------------------
# POST /api/r3/chat
# ---------------------------------------------------------------------------


class TestReco3ChatRoute:
    def _mock_orch(self, return_value=None):
        mock_orch = MagicMock()
        mock_orch.process.return_value = return_value or {"response": "ok"}
        return mock_orch

    def test_returns_200_with_prompt(self, client):
        with patch(f"{MODULE}.reco2_get_orchestrator", return_value=self._mock_orch()):
            resp = client.post("/api/r3/chat", json={"prompt": "What is wrong with my cat?"})
        assert resp.status_code == 200

    def test_empty_body_returns_200(self, client):
        with patch(f"{MODULE}.reco2_get_orchestrator", return_value=self._mock_orch()):
            resp = client.post("/api/r3/chat", json={})
        assert resp.status_code == 200

    def test_prompt_passed_to_orchestrator(self, client):
        orch = self._mock_orch()
        with patch(f"{MODULE}.reco2_get_orchestrator", return_value=orch):
            client.post("/api/r3/chat", json={"prompt": "hello", "domain": "vet"})
        orch.process.assert_called_once()
        args, kwargs = orch.process.call_args
        assert args[0] == "hello"
        assert kwargs.get("domain") == "vet"

    def test_default_domain_is_general(self, client):
        orch = self._mock_orch()
        with patch(f"{MODULE}.reco2_get_orchestrator", return_value=orch):
            client.post("/api/r3/chat", json={"prompt": "test"})
        _, kwargs = orch.process.call_args
        assert kwargs.get("domain") == "general"

    def test_default_max_tokens_is_1024(self, client):
        orch = self._mock_orch()
        with patch(f"{MODULE}.reco2_get_orchestrator", return_value=orch):
            client.post("/api/r3/chat", json={"prompt": "test"})
        _, kwargs = orch.process.call_args
        assert kwargs.get("max_tokens") == 1024

    def test_custom_max_tokens_forwarded(self, client):
        orch = self._mock_orch()
        with patch(f"{MODULE}.reco2_get_orchestrator", return_value=orch):
            client.post("/api/r3/chat", json={"prompt": "test", "max_tokens": 512})
        _, kwargs = orch.process.call_args
        assert kwargs.get("max_tokens") == 512


# ---------------------------------------------------------------------------
# GET /api/r3/config
# ---------------------------------------------------------------------------


class TestReco3ConfigRoute:
    def test_returns_200(self, client):
        with (
            patch(f"{MODULE}.load_reco2_config", return_value={}),
            patch(f"{MODULE}.public_reco2_config", return_value={"mode": "test"}),
        ):
            resp = client.get("/api/r3/config")
        assert resp.status_code == 200

    def test_response_is_json(self, client):
        with (
            patch(f"{MODULE}.load_reco2_config", return_value={}),
            patch(f"{MODULE}.public_reco2_config", return_value={"mode": "test"}),
        ):
            resp = client.get("/api/r3/config")
        assert resp.content_type.startswith("application/json")

    def test_delegates_to_public_config(self, client):
        mock_pub = MagicMock(return_value={"mode": "production"})
        with (
            patch(f"{MODULE}.load_reco2_config", return_value={"k": "v"}),
            patch(f"{MODULE}.public_reco2_config", mock_pub),
        ):
            client.get("/api/r3/config")
        mock_pub.assert_called_once()


# ---------------------------------------------------------------------------
# ensure_json_response decorator
# ---------------------------------------------------------------------------


class TestEnsureJsonResponseDecorator:
    def test_success_response_includes_version(self, client):
        with patch(f"{MODULE}.reco2_get_status", return_value={"status": "ok"}):
            data = client.get("/api/status").get_json()
        assert "version" in data

    def test_error_response_sets_success_false(self, client):
        resp = client.post("/api/analyze-symptoms", json={})
        data = resp.get_json()
        assert data.get("success") is False

    def test_internal_exception_returns_500_with_error(self, client):
        with patch(f"{MODULE}.reco2_get_status", side_effect=RuntimeError("boom")):
            resp = client.get("/api/status")
        assert resp.status_code == 500
        data = resp.get_json()
        assert "error" in data
        assert data.get("success") is False

    def test_version_injected_on_error_response(self, client):
        with patch(f"{MODULE}.reco2_get_status", side_effect=RuntimeError("boom")):
            data = client.get("/api/status").get_json()
        assert data.get("version") == showdog_mod.VERSION


# ---------------------------------------------------------------------------
# Security headers (after_request hook)
# ---------------------------------------------------------------------------


class TestSecurityHeaders:
    def test_x_content_type_options(self, client):
        resp = client.get("/api/health")
        assert resp.headers.get("X-Content-Type-Options") == "nosniff"

    def test_x_frame_options(self, client):
        resp = client.get("/api/health")
        assert resp.headers.get("X-Frame-Options") == "SAMEORIGIN"

    def test_x_xss_protection(self, client):
        resp = client.get("/api/health")
        assert resp.headers.get("X-XSS-Protection") == "1; mode=block"

    def test_referrer_policy(self, client):
        resp = client.get("/api/health")
        assert resp.headers.get("Referrer-Policy") == "strict-origin-when-cross-origin"

    def test_no_hsts_without_production_env(self, client):
        """HSTS must only appear in production (RENDER/PRODUCTION env vars)."""
        resp = client.get("/api/health")
        assert "Strict-Transport-Security" not in resp.headers

    def test_hsts_present_when_render_env_set(self, client):
        with patch.dict(os.environ, {"RENDER": "1"}):
            resp = client.get("/api/health")
        assert "Strict-Transport-Security" in resp.headers


# ---------------------------------------------------------------------------
# Static file routes
# ---------------------------------------------------------------------------


class TestStaticFileRoutes:
    def test_index_route_registered(self):
        rules = {rule.rule for rule in APP.url_map.iter_rules()}
        assert "/" in rules

    def test_favicon_route_registered(self):
        rules = {rule.rule for rule in APP.url_map.iter_rules()}
        assert "/favicon.ico" in rules

    def test_index_without_file_returns_404_or_200(self, client):
        resp = client.get("/")
        assert resp.status_code in (200, 404)

    def test_index_404_is_json(self, client):
        resp = client.get("/")
        if resp.status_code == 404:
            assert resp.content_type.startswith("application/json")

    def test_favicon_without_file_returns_204_or_200_or_404(self, client):
        resp = client.get("/favicon.ico")
        assert resp.status_code in (200, 204, 404)

    def test_nonexistent_static_file_returns_404(self, client):
        resp = client.get("/this_file_does_not_exist_abc.js")
        assert resp.status_code == 404

    def test_nonexistent_static_file_error_in_json(self, client):
        resp = client.get("/this_file_does_not_exist_abc.js")
        data = resp.get_json()
        assert data is not None
        assert "error" in data


# ---------------------------------------------------------------------------
# Error handlers
# ---------------------------------------------------------------------------


class TestErrorHandlers:
    def test_unknown_api_path_returns_404(self, client):
        resp = client.get("/api/totally/unknown/route/xyz")
        # Flask may return 404 directly or via the static_files catch-all
        assert resp.status_code == 404

    def test_404_response_is_json(self, client):
        resp = client.get("/api/totally/unknown/route/xyz")
        assert resp.content_type.startswith("application/json")
        assert "error" in resp.get_json()

    def test_500_handler_registered(self):
        assert 500 in APP.error_handler_spec.get(None, {})

    def test_404_handler_registered(self):
        assert 404 in APP.error_handler_spec.get(None, {})


# ---------------------------------------------------------------------------
# URL rule coverage / HTTP method constraints
# ---------------------------------------------------------------------------


class TestUrlRules:
    @pytest.fixture(autouse=True)
    def _rules(self):
        self.rules = {rule.rule for rule in APP.url_map.iter_rules()}
        self.rule_map = {rule.rule: rule for rule in APP.url_map.iter_rules()}

    def test_health_route_registered(self):
        assert "/api/health" in self.rules

    def test_analyze_symptoms_route_registered(self):
        assert "/api/analyze-symptoms" in self.rules

    def test_status_route_registered(self):
        assert "/api/status" in self.rules

    def test_logs_route_registered(self):
        assert "/api/logs" in self.rules

    def test_evaluate_route_registered(self):
        assert "/api/evaluate" in self.rules

    def test_feedback_route_registered(self):
        assert "/api/feedback" in self.rules

    def test_patrol_route_registered(self):
        assert "/api/patrol" in self.rules

    def test_r3_analyze_input_registered(self):
        assert "/api/r3/analyze_input" in self.rules

    def test_r3_analyze_output_registered(self):
        assert "/api/r3/analyze_output" in self.rules

    def test_r3_chat_registered(self):
        assert "/api/r3/chat" in self.rules

    def test_r3_config_registered(self):
        assert "/api/r3/config" in self.rules

    def test_index_route_registered(self):
        assert "/" in self.rules

    def test_favicon_route_registered(self):
        assert "/favicon.ico" in self.rules

    def test_analyze_symptoms_accepts_post_only(self):
        methods = self.rule_map["/api/analyze-symptoms"].methods
        assert "POST" in methods
        assert "GET" not in methods

    def test_health_accepts_get_only(self):
        methods = self.rule_map["/api/health"].methods
        assert "GET" in methods
        assert "POST" not in methods

    def test_logs_accepts_get_only(self):
        methods = self.rule_map["/api/logs"].methods
        assert "GET" in methods
        assert "POST" not in methods

    def test_evaluate_accepts_post_only(self):
        methods = self.rule_map["/api/evaluate"].methods
        assert "POST" in methods
        assert "GET" not in methods

    def test_feedback_accepts_post_only(self):
        methods = self.rule_map["/api/feedback"].methods
        assert "POST" in methods
        assert "GET" not in methods

    def test_patrol_accepts_post_only(self):
        methods = self.rule_map["/api/patrol"].methods
        assert "POST" in methods
        assert "GET" not in methods

    def test_r3_config_accepts_get_only(self):
        methods = self.rule_map["/api/r3/config"].methods
        assert "GET" in methods
        assert "POST" not in methods

    def test_r3_chat_accepts_post_only(self):
        methods = self.rule_map["/api/r3/chat"].methods
        assert "POST" in methods
        assert "GET" not in methods
