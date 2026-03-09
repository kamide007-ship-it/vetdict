from api import vetdict_api


def _auth_header(token):
    return {"Authorization": f"Bearer {token}"}


def test_protected_endpoints_require_internal_token(monkeypatch):
    monkeypatch.setenv("INTERNAL_API_TOKEN", "secret-token")
    vetdict_api._RATE_LIMIT_BUCKETS.clear()

    client = vetdict_api.app.test_client()

    status_resp = client.get("/api/status")
    config_resp = client.get("/api/r3/config")

    assert status_resp.status_code == 401
    assert config_resp.status_code == 401
    assert status_resp.get_json()["error"] == "Unauthorized"
    assert config_resp.get_json()["error"] == "Unauthorized"


def test_unauthorized_protected_requests_are_rate_limited(monkeypatch):
    monkeypatch.setenv("INTERNAL_API_TOKEN", "secret-token")
    monkeypatch.setenv("INTERNAL_API_RATE_LIMIT_MAX_REQUESTS", "2")
    monkeypatch.setenv("INTERNAL_API_RATE_LIMIT_WINDOW_SECONDS", "60")
    vetdict_api._RATE_LIMIT_BUCKETS.clear()

    client = vetdict_api.app.test_client()

    first = client.get("/api/status")
    second = client.get("/api/status")
    third = client.get("/api/status")

    assert first.status_code == 401
    assert second.status_code == 401
    assert third.status_code == 429
    assert third.get_json()["error"] == "リクエスト制限に達しました。"


def test_valid_internal_token_allows_protected_request(monkeypatch):
    monkeypatch.setenv("INTERNAL_API_TOKEN", "secret-token")
    vetdict_api._RATE_LIMIT_BUCKETS.clear()

    client = vetdict_api.app.test_client()
    resp = client.get("/api/status", headers=_auth_header("secret-token"))

    assert resp.status_code in {200, 503}
    assert resp.get_json()["version"] == vetdict_api.VERSION
