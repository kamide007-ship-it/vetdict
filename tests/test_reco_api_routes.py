import importlib


def _client():
    import app as appmod

    importlib.reload(appmod)
    return appmod.app.test_client()


def test_reco_dashboard_route(temp_instance):
    c = _client()
    r = c.get("/r3")
    assert r.status_code == 200


def test_reco_status_and_evaluate_flow(temp_instance):
    c = _client()

    status = c.get("/api/status")
    assert status.status_code == 200
    assert "k" in status.get_json()

    payload = {
        "inference": {"a": 0.1},
        "evidence": {"a": {"median": 0.2}},
        "context": {"domain": "general", "confidence": 0.7},
    }
    ev = c.post("/api/evaluate", json=payload)
    assert ev.status_code == 200
    assert "session_id" in ev.get_json()


def test_reco_feedback_route(temp_instance):
    c = _client()

    payload = {
        "inference": {"a": 0.1},
        "evidence": {"a": {"median": 0.2}},
        "context": {"domain": "general", "confidence": 0.7},
    }
    ev = c.post("/api/evaluate", json=payload).get_json()

    fb = c.post("/api/feedback", json={"session_id": ev["session_id"], "domain": "general", "feedback": "good"})
    assert fb.status_code == 200
    assert fb.get_json()["status"] in ("recorded", "duplicate_ignored")


def test_reco_r3_analyze_routes(temp_instance):
    c = _client()

    in_res = c.post("/api/r3/analyze_input", json={"text": "今すぐ！"})
    out_res = c.post("/api/r3/analyze_output", json={"text": "必ず成功。"})

    assert in_res.status_code == 200
    assert out_res.status_code == 200
    assert "risk_level" in in_res.get_json()
    assert "psi_modifier" in out_res.get_json()
