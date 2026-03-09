from api.vetdict_api import app


def test_api_health_includes_csp_header():
    client = app.test_client()
    resp = client.get('/api/health')
    assert resp.status_code == 200
    assert 'Content-Security-Policy' in resp.headers
    assert "default-src 'self'" in resp.headers['Content-Security-Policy']


def test_api_rate_limit_triggers_429():
    app.config['TESTING'] = True
    client = app.test_client()

    from api import vetdict_api

    # tighten window for test determinism
    old_max = vetdict_api.RATE_LIMIT_MAX_REQUESTS
    old_window = vetdict_api.RATE_LIMIT_WINDOW_SEC
    vetdict_api.RATE_LIMIT_MAX_REQUESTS = 2
    vetdict_api.RATE_LIMIT_WINDOW_SEC = 60
    vetdict_api._RATE_LIMIT_BUCKETS.clear()

    try:
        r1 = client.get('/api/health')
        r2 = client.get('/api/health')
        r3 = client.get('/api/health')
        assert r1.status_code == 200
        assert r2.status_code == 200
        assert r3.status_code == 429
    finally:
        vetdict_api.RATE_LIMIT_MAX_REQUESTS = old_max
        vetdict_api.RATE_LIMIT_WINDOW_SEC = old_window
        vetdict_api._RATE_LIMIT_BUCKETS.clear()
