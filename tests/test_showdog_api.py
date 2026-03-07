"""
Integration tests for the ShowDog API routes.

Tests cover:
- Health check endpoint
- Algorithm info endpoint
- Authentication (register, login, logout, me)
- Dog CRUD (create, list, get)
- Breed & disease data endpoints
- Security headers
"""

import importlib

import pytest


@pytest.fixture()
def client(tmp_path, monkeypatch):
    """Create a test client with isolated database."""
    db_path = str(tmp_path / "test.db")
    monkeypatch.setenv("DATABASE_PATH", db_path)
    monkeypatch.setenv("RECO3_INSTANCE_DIR", str(tmp_path / "instance"))
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)

    import api.database as db_mod
    importlib.reload(db_mod)
    import api.showdog_api as api_mod
    importlib.reload(api_mod)

    api_mod.app.config["TESTING"] = True
    with api_mod.app.test_client() as c:
        yield c


@pytest.fixture()
def auth_client(client):
    """Create a test client with an authenticated user."""
    client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "TestPassword123!",
        "name": "Test User",
        "security_question": "Pet name?",
        "security_answer": "Buddy",
    })
    resp = client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "TestPassword123!",
    })
    token = resp.get_json().get("token", "")
    client.environ_base["HTTP_AUTHORIZATION"] = f"Bearer {token}"
    return client


# ============================================================================
# Health & System Endpoints
# ============================================================================


class TestHealthEndpoints:
    def test_health_check(self, client):
        resp = client.get("/api/health")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "version" in data

    def test_algorithm_info(self, client):
        resp = client.get("/api/algorithm")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "algorithm_version" in data
        assert "weights" in data

    def test_index_page(self, client):
        resp = client.get("/")
        assert resp.status_code == 200


# ============================================================================
# Security Headers
# ============================================================================


class TestSecurityHeaders:
    def test_x_content_type_options(self, client):
        resp = client.get("/api/health")
        assert resp.headers.get("X-Content-Type-Options") == "nosniff"

    def test_x_frame_options(self, client):
        resp = client.get("/api/health")
        assert resp.headers.get("X-Frame-Options") == "SAMEORIGIN"

    def test_referrer_policy(self, client):
        resp = client.get("/api/health")
        assert "strict-origin" in resp.headers.get("Referrer-Policy", "")

    def test_content_security_policy(self, client):
        resp = client.get("/api/health")
        csp = resp.headers.get("Content-Security-Policy", "")
        assert "default-src" in csp

    def test_permissions_policy(self, client):
        resp = client.get("/api/health")
        assert "camera=()" in resp.headers.get("Permissions-Policy", "")


# ============================================================================
# Authentication
# ============================================================================


class TestAuthentication:
    def test_register_success(self, client):
        resp = client.post("/api/auth/register", json={
            "email": "new@example.com",
            "password": "SecurePass123!",
            "name": "New User",
            "security_question": "Color?",
            "security_answer": "Blue",
        })
        assert resp.status_code in (200, 201)

    def test_register_duplicate_email(self, client):
        data = {
            "email": "dup@example.com",
            "password": "SecurePass123!",
            "name": "User",
            "security_question": "Q?",
            "security_answer": "A",
        }
        client.post("/api/auth/register", json=data)
        resp = client.post("/api/auth/register", json=data)
        assert resp.status_code in (400, 409)

    def test_register_missing_fields(self, client):
        resp = client.post("/api/auth/register", json={"email": "x@x.com"})
        assert resp.status_code == 400

    def test_login_success(self, client):
        client.post("/api/auth/register", json={
            "email": "login@example.com",
            "password": "SecurePass123!",
            "name": "Login User",
            "security_question": "Q?",
            "security_answer": "A",
        })
        resp = client.post("/api/auth/login", json={
            "email": "login@example.com",
            "password": "SecurePass123!",
        })
        assert resp.status_code == 200
        assert "token" in resp.get_json()

    def test_login_wrong_password(self, client):
        client.post("/api/auth/register", json={
            "email": "wrong@example.com",
            "password": "SecurePass123!",
            "name": "User",
            "security_question": "Q?",
            "security_answer": "A",
        })
        resp = client.post("/api/auth/login", json={
            "email": "wrong@example.com",
            "password": "WrongPassword!",
        })
        assert resp.status_code == 401

    def test_me_authenticated(self, auth_client):
        resp = auth_client.get("/api/auth/me")
        assert resp.status_code == 200
        data = resp.get_json()
        # Response contains user info
        assert "user" in data or "email" in data

    def test_me_unauthenticated(self, client):
        resp = client.get("/api/auth/me")
        assert resp.status_code == 401

    def test_logout(self, auth_client):
        resp = auth_client.post("/api/auth/logout")
        assert resp.status_code == 200


# ============================================================================
# Dog CRUD
# ============================================================================


class TestDogCRUD:
    def test_create_dog(self, auth_client):
        resp = auth_client.post("/api/dogs", json={
            "name": "Buddy",
            "breed_id": "122_labrador_retriever",
            "birth_date": "2023-01-15",
            "weight": 28.5,
            "gender": "male",
        })
        assert resp.status_code in (200, 201)
        data = resp.get_json()
        assert data.get("success") is True or "dog" in data or "id" in data

    def test_list_dogs(self, auth_client):
        auth_client.post("/api/dogs", json={
            "name": "Dog1",
            "breed_id": "122_labrador_retriever",
        })
        resp = auth_client.get("/api/dogs")
        assert resp.status_code == 200

    def test_create_dog_unauthenticated(self, client):
        resp = client.post("/api/dogs", json={
            "name": "NoDog",
            "breed_id": "122_labrador_retriever",
        })
        assert resp.status_code == 401

    def test_create_dog_missing_name(self, auth_client):
        resp = auth_client.post("/api/dogs", json={
            "breed_id": "122_labrador_retriever",
        })
        assert resp.status_code == 400

    def test_create_dog_null_name(self, auth_client):
        resp = auth_client.post("/api/dogs", json={
            "name": None,
            "breed_id": "122_labrador_retriever",
        })
        assert resp.status_code == 400

    def test_create_dog_null_notes(self, auth_client):
        resp = auth_client.post("/api/dogs", json={
            "name": "Buddy",
            "breed_id": "122_labrador_retriever",
            "notes": None,
        })
        assert resp.status_code in (200, 201)


# ============================================================================
# Breed & Disease Data
# ============================================================================


class TestBreedData:
    def test_list_breeds(self, client):
        resp = client.get("/api/breeds")
        assert resp.status_code == 200

    def test_get_breed_detail(self, client):
        resp = client.get("/api/breeds/122_labrador_retriever")
        assert resp.status_code == 200

    def test_get_diseases(self, client):
        resp = client.get("/api/diseases")
        assert resp.status_code == 200


# ============================================================================
# Regression Tests — Bug Fixes
# ============================================================================


class TestJsonNullValidation:
    """POST endpoints must return 400 (not 500) when JSON body is missing."""

    def test_judge_validation_no_json(self, client):
        resp = client.post("/api/judge-validation/compute", data="not json")
        assert resp.status_code in (400, 503)

    def test_growth_prediction_no_json(self, client):
        resp = client.post("/api/growth-prediction/predict", data="not json")
        assert resp.status_code in (400, 503)

    def test_breeding_compatibility_no_json(self, client):
        resp = client.post("/api/genetic-scoring/breeding-compatibility", data="not json")
        assert resp.status_code in (400, 503)

    def test_coi_no_json(self, client):
        resp = client.post("/api/genetic-scoring/coi", data="not json")
        assert resp.status_code in (400, 503)

    def test_genetic_test_no_json(self, client):
        resp = client.post("/api/genetic-test/analyze", data="not json")
        assert resp.status_code in (400, 503)

    def test_pose_estimation_no_json(self, client):
        resp = client.post("/api/pose-estimation/analyze", data="not json")
        assert resp.status_code in (400, 503)

    def test_gait_analysis_no_json(self, client):
        resp = client.post("/api/pose-estimation/analyze-gait", data="not json")
        assert resp.status_code in (400, 503)

    def test_finetuning_evaluate_no_json(self, client):
        resp = client.post("/api/finetuning/evaluate", data="not json")
        assert resp.status_code in (400, 503)


class TestErrorResponseSanitization:
    """Error responses must not leak internal exception details."""

    def test_diseases_error_no_leak(self, client):
        resp = client.get("/api/diseases")
        # Even if it fails, error message should not contain traceback/class names
        data = resp.get_json()
        if "error" in data:
            assert "Traceback" not in data["error"]
            assert "Exception" not in data["error"]

    def test_cycle_run_requires_auth(self, client):
        """cycle/run must require authentication."""
        resp = client.post("/api/cycle/run")
        assert resp.status_code == 401


class TestStripeWebhookSecurity:
    """Stripe webhook must reject unsigned events when secret is not configured."""

    def test_webhook_rejects_without_secret(self, client):
        resp = client.post("/api/stripe/webhook",
                           data='{"type": "checkout.session.completed"}',
                           content_type="application/json")
        # Should be 503 (not configured) or 400, never 200
        assert resp.status_code in (400, 503)


# ============================================================================
# Silent Error Prevention Tests
# ============================================================================


class TestNoSilentErrors:
    """Verify that error paths produce observable output, not silent failures."""

    def test_no_bare_except_pass_in_api(self):
        """No 'except Exception: pass' should remain in showdog_api.py."""
        import re
        with open("api/showdog_api.py") as f:
            content = f.read()
        matches = re.findall(r"except Exception:\s*\n\s+pass", content)
        assert len(matches) == 0, (
            f"Found {len(matches)} bare 'except Exception: pass' blocks "
            f"that silently swallow errors"
        )

    def test_no_bare_except_pass_in_auto_cycle(self):
        """No 'except Exception: pass' should remain in auto_cycle.py."""
        import re
        with open("api/auto_cycle.py") as f:
            content = f.read()
        matches = re.findall(r"except Exception:\s*\n\s+pass", content)
        assert len(matches) == 0, (
            f"Found {len(matches)} bare 'except Exception: pass' blocks "
            f"in auto_cycle.py"
        )

    def test_no_bare_except_pass_in_growth_prediction(self):
        """No 'except Exception: pass' should remain in growth_prediction.py."""
        import re
        with open("api/growth_prediction.py") as f:
            content = f.read()
        matches = re.findall(r"except Exception:\s*\n\s+pass", content)
        assert len(matches) == 0, (
            f"Found {len(matches)} bare 'except Exception: pass' blocks "
            f"in growth_prediction.py"
        )

    def test_error_responses_no_str_e_leak(self):
        """Error responses must not leak raw exception strings to clients."""
        import re
        with open("api/showdog_api.py") as f:
            content = f.read()
        # Pattern: 'error': ... str(e) ... }, 500  (in return statements)
        leaks = re.findall(r"return\s+\{.*?'error'.*?str\(e\).*?\},\s*5\d\d", content)
        assert len(leaks) == 0, (
            f"Found {len(leaks)} error responses leaking str(e) to client"
        )
