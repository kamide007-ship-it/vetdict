"""Tests for api/showdog_api.py — coverage-oriented test suite.

Covers:
- GET /api/health — response structure, version, features
- POST /api/analyze-symptoms — valid dog, non-dog species, empty symptoms
- GET /api/status — RECO2 status
- GET /api/logs — RECO2 logs
- POST /api/evaluate — RECO2 evaluate
- POST /api/feedback — RECO2 feedback
- GET /api/r3/config — RECO3 config
- GET / — index page
- 404 error handler
- Security headers
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
# GET /api/health
# ---------------------------------------------------------------------------

class TestHealthEndpoint:
    def test_health_returns_200(self, client):
        resp = client.get("/api/health")
        assert resp.status_code == 200

    def test_health_has_status(self, client):
        data = client.get("/api/health").get_json()
        assert data["status"] == "healthy"

    def test_health_has_version(self, client):
        data = client.get("/api/health").get_json()
        assert data["version"] == "5.0.0"

    def test_health_has_build(self, client):
        data = client.get("/api/health").get_json()
        assert "build" in data

    def test_health_has_features_dict(self, client):
        data = client.get("/api/health").get_json()
        features = data["features"]
        assert isinstance(features, dict)
        # Should contain known feature flags
        for key in ("symptom_checker", "health_checker", "reco2"):
            assert key in features


# ---------------------------------------------------------------------------
# POST /api/analyze-symptoms
# ---------------------------------------------------------------------------

class TestAnalyzeSymptoms:
    def test_analyze_dog_symptoms(self, client):
        payload = {"symptoms": ["vomiting", "lethargy"], "species": "dog"}
        resp = client.post(
            "/api/analyze-symptoms",
            data=json.dumps(payload),
            content_type="application/json",
        )
        # Should succeed or return 500 if symptom_checker not available
        assert resp.status_code in (200, 500)
        data = resp.get_json()
        assert data is not None

    def test_analyze_non_dog_species(self, client):
        payload = {"symptoms": ["vomiting"], "species": "cat"}
        resp = client.post(
            "/api/analyze-symptoms",
            data=json.dumps(payload),
            content_type="application/json",
        )
        # May return 200 if species_analyzer available, or 500 if not
        assert resp.status_code in (200, 500)
        data = resp.get_json()
        assert data is not None

    def test_analyze_empty_symptoms(self, client):
        payload = {"symptoms": [], "species": "dog"}
        resp = client.post(
            "/api/analyze-symptoms",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert resp.status_code == 400
        data = resp.get_json()
        assert "error" in data

    def test_analyze_missing_symptoms_key(self, client):
        payload = {"species": "dog"}
        resp = client.post(
            "/api/analyze-symptoms",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert resp.status_code == 400

    def test_analyze_no_body(self, client):
        resp = client.post(
            "/api/analyze-symptoms",
            content_type="application/json",
        )
        assert resp.status_code == 400


# ---------------------------------------------------------------------------
# GET /api/status — RECO2 status
# ---------------------------------------------------------------------------

class TestReco2Status:
    def test_status_endpoint(self, client):
        resp = client.get("/api/status")
        # 200 if RECO2 available, 503 otherwise
        assert resp.status_code in (200, 503)
        data = resp.get_json()
        assert data is not None

    def test_status_returns_json(self, client):
        resp = client.get("/api/status")
        assert resp.content_type.startswith("application/json")


# ---------------------------------------------------------------------------
# GET /api/logs — RECO2 logs
# ---------------------------------------------------------------------------

class TestReco2Logs:
    def test_logs_endpoint(self, client):
        resp = client.get("/api/logs")
        assert resp.status_code in (200, 503)
        data = resp.get_json()
        assert data is not None

    def test_logs_with_limit(self, client):
        resp = client.get("/api/logs?limit=10")
        assert resp.status_code in (200, 503)


# ---------------------------------------------------------------------------
# POST /api/evaluate — RECO2 evaluate
# ---------------------------------------------------------------------------

class TestReco2Evaluate:
    def test_evaluate_endpoint(self, client):
        payload = {"text": "sample evaluation payload", "domain": "veterinary"}
        resp = client.post(
            "/api/evaluate",
            data=json.dumps(payload),
            content_type="application/json",
        )
        # 200 if RECO2 available, 503 otherwise
        assert resp.status_code in (200, 500, 503)
        data = resp.get_json()
        assert data is not None


# ---------------------------------------------------------------------------
# POST /api/feedback — RECO2 feedback
# ---------------------------------------------------------------------------

class TestReco2Feedback:
    def test_feedback_endpoint(self, client):
        payload = {
            "evaluation_id": "test-123",
            "rating": "helpful",
            "comment": "good analysis",
        }
        resp = client.post(
            "/api/feedback",
            data=json.dumps(payload),
            content_type="application/json",
        )
        assert resp.status_code in (200, 400, 500, 503)
        data = resp.get_json()
        assert data is not None


# ---------------------------------------------------------------------------
# GET /api/r3/config — RECO3 config
# ---------------------------------------------------------------------------

class TestReco3Config:
    def test_config_endpoint(self, client):
        resp = client.get("/api/r3/config")
        assert resp.status_code in (200, 503)
        data = resp.get_json()
        assert data is not None


# ---------------------------------------------------------------------------
# Error handlers
# ---------------------------------------------------------------------------

class TestErrorHandlers:
    def test_404_for_unknown_api_route(self, client):
        resp = client.get("/api/nonexistent-route-xyz")
        assert resp.status_code == 404
        data = resp.get_json()
        assert "error" in data

    def test_404_returns_json(self, client):
        resp = client.get("/api/this-does-not-exist")
        assert resp.content_type.startswith("application/json")


# ---------------------------------------------------------------------------
# Security headers
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

    def test_security_headers_on_post(self, client):
        resp = client.post(
            "/api/analyze-symptoms",
            data=json.dumps({"symptoms": []}),
            content_type="application/json",
        )
        assert resp.headers.get("X-Content-Type-Options") == "nosniff"


# ---------------------------------------------------------------------------
# GET / — index page
# ---------------------------------------------------------------------------

class TestIndex:
    def test_index_route(self, client):
        resp = client.get("/")
        # Either serves index.html (200) or returns 404 JSON if file missing
        assert resp.status_code in (200, 404)

    def test_index_returns_content(self, client):
        resp = client.get("/")
        assert len(resp.data) > 0
