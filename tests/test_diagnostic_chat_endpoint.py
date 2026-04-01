from api.vetdict_api import app


def test_chat_returns_species_guidance_for_cat():
    client = app.test_client()
    resp = client.post(
        "/api/diagnostic-chat/chat",
        json={"species": "cat", "message": "猫が咳と呼吸困難です"},
    )
    assert resp.status_code == 200
    payload = resp.get_json()
    assert payload["species"] == "cat"
    assert "species_guidance" in payload
    assert "猫として解析" in payload["species_guidance"]
    assert payload["response"].startswith(payload["species_guidance"])


def test_chat_species_guidance_differs_by_species():
    client = app.test_client()
    cat_resp = client.post(
        "/api/diagnostic-chat/chat",
        json={"species": "cat", "message": "猫が咳をしています"},
    )
    dog_resp = client.post(
        "/api/diagnostic-chat/chat",
        json={"species": "dog", "message": "犬が咳をしています"},
    )
    assert cat_resp.status_code == 200
    assert dog_resp.status_code == 200
    cat_payload = cat_resp.get_json()
    dog_payload = dog_resp.get_json()
    assert cat_payload["species_guidance"] != dog_payload["species_guidance"]
    assert "猫" in cat_payload["species_guidance"]
    assert "犬" in dog_payload["species_guidance"]


def test_multi_disease_endpoint_is_registered():
    routes = {rule.rule for rule in app.url_map.iter_rules()}
    assert "/api/diagnostic-chat/multi-disease/analyze" in routes


# =============================================================================
# Secondary endpoints
# =============================================================================


class TestSymptomSuggestions:
    """Tests for GET /api/diagnostic-chat/symptom-suggestions."""

    def test_returns_symptoms(self):
        client = app.test_client()
        r = client.get("/api/diagnostic-chat/symptom-suggestions")
        assert r.status_code == 200
        data = r.get_json()
        assert "symptoms" in data
        assert "total" in data
        assert data["total"] > 0
        sym = data["symptoms"][0]
        assert "id" in sym
        assert "name_ja" in sym
        assert "name_en" in sym
        assert "category" in sym

    def test_filter_by_category(self):
        client = app.test_client()
        r = client.get("/api/diagnostic-chat/symptom-suggestions?category=respiratory")
        data = r.get_json()
        assert data["total"] > 0
        for s in data["symptoms"]:
            assert s["category"] == "respiratory"

    def test_filter_by_search(self):
        client = app.test_client()
        r = client.get("/api/diagnostic-chat/symptom-suggestions?search=cough")
        data = r.get_json()
        assert data["total"] > 0

    def test_empty_search(self):
        client = app.test_client()
        r = client.get("/api/diagnostic-chat/symptom-suggestions?search=zzzznonexistent")
        data = r.get_json()
        assert data["total"] == 0


class TestCategories:
    """Tests for GET /api/diagnostic-chat/categories."""

    def test_returns_categories(self):
        client = app.test_client()
        r = client.get("/api/diagnostic-chat/categories")
        assert r.status_code == 200
        data = r.get_json()
        assert "total_categories" in data
        assert "categories" in data
        assert data["total_categories"] > 0
        cat = data["categories"][0]
        assert "id" in cat
        assert "symptoms" in cat
        assert len(cat["symptoms"]) > 0

    def test_category_symptoms_have_bilingual_names(self):
        client = app.test_client()
        r = client.get("/api/diagnostic-chat/categories")
        data = r.get_json()
        for cat in data["categories"][:3]:
            for sym in cat["symptoms"][:3]:
                assert "name_ja" in sym
                assert "name_en" in sym


class TestDifferentialAnalysis:
    """Tests for POST /api/diagnostic-chat/differential-analysis."""

    def test_missing_disease_ids(self):
        client = app.test_client()
        r = client.post("/api/diagnostic-chat/differential-analysis", json={})
        assert r.status_code == 400

    def test_unknown_disease_ids(self):
        client = app.test_client()
        r = client.post("/api/diagnostic-chat/differential-analysis", json={
            "disease_id_1": "nonexistent_1",
            "disease_id_2": "nonexistent_2",
        })
        assert r.status_code == 404


class TestTreatmentPlan:
    """Tests for POST /api/diagnostic-chat/treatment-plan."""

    def test_missing_disease_id(self):
        client = app.test_client()
        r = client.post("/api/diagnostic-chat/treatment-plan", json={})
        assert r.status_code == 400

    def test_unknown_disease_id(self):
        client = app.test_client()
        r = client.post("/api/diagnostic-chat/treatment-plan", json={
            "disease_id": "nonexistent_disease",
        })
        assert r.status_code == 404


class TestFeedback:
    """Tests for POST /api/diagnostic-chat/feedback."""

    def test_missing_session_id(self):
        client = app.test_client()
        r = client.post("/api/diagnostic-chat/feedback", json={
            "feedback": "good",
        })
        assert r.status_code == 400

    def test_invalid_feedback_type(self):
        client = app.test_client()
        r = client.post("/api/diagnostic-chat/feedback", json={
            "session_id": "test-session",
            "feedback": "invalid_type",
        })
        assert r.status_code == 400

    def test_valid_feedback(self):
        client = app.test_client()
        r = client.post("/api/diagnostic-chat/feedback", json={
            "session_id": "test-session-123",
            "feedback": "good",
            "domain": "general",
        })
        assert r.status_code == 201
        data = r.get_json()
        assert data["status"] == "recorded"
