from api.chat.constants import detect_species_from_text
from api.vetdict_api import app


class TestSpeciesDetectionFromText:
    """Free-text chat must infer the patient species from the message itself.

    Clinicians type the species inline ("猫 多飲多尿", "5yo dog PU/PD"); the
    chat must not silently analyse a cat case against the dog database.
    """

    def test_japanese_leading_token(self):
        assert detect_species_from_text("猫 多飲多尿 体重減少 食欲増加") == "cat"
        assert detect_species_from_text("3歳猫 嘔吐 食欲廃絶 黄疸") == "cat"
        assert detect_species_from_text("犬 咳 発熱") == "dog"
        assert detect_species_from_text("うちのうさぎが食べない") == "rabbit"
        assert detect_species_from_text("リクガメの甲羅が柔らかい") == "tortoise"
        assert detect_species_from_text("セキセイインコ 羽を膨らませる") == "parakeet"

    def test_english_keywords(self):
        assert detect_species_from_text("5yo dog PU/PD weight loss") == "dog"
        assert detect_species_from_text("horse has cough fever and diarrhea") == "horse"
        assert detect_species_from_text("my kitten is sneezing") == "cat"

    def test_earliest_match_wins(self):
        # The patient species is whichever is mentioned first.
        assert detect_species_from_text("猫背気味の犬 嘔吐") == "dog"
        assert detect_species_from_text("犬歯の破折（猫）") == "cat"

    def test_false_positive_compounds_ignored(self):
        # 犬歯 = canine tooth, 猫背 = hunched posture — not a species mention.
        assert detect_species_from_text("犬歯破折") is None
        assert detect_species_from_text("猫背の改善") is None

    def test_no_species_returns_none(self):
        assert detect_species_from_text("coughing") is None
        assert detect_species_from_text("xyz nonsense 9999") is None
        assert detect_species_from_text("") is None
        assert detect_species_from_text(None) is None


def test_chat_detects_cat_despite_dog_default():
    """A fresh visitor typing a cat case (client default species=dog) must be
    routed to the cat database rather than analysed as a dog."""
    client = app.test_client()
    resp = client.post(
        "/api/diagnostic-chat/chat",
        json={"species": "dog", "message": "猫 多飲多尿 体重減少", "lang": "ja"},
    )
    assert resp.status_code == 200
    payload = resp.get_json()
    assert payload["species"] == "cat"
    assert "猫として解析" in payload["species_guidance"]


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


class TestFollowUpQuestionLabels:
    """Regression guard: follow-up question labels must never expose raw symptom IDs.

    Bug: when a missing_key_symptom ID (e.g. ``loss_of_appetite``) didn't appear
    directly in the species symptom_names map, the chat surfaced raw IDs like
    ``loss_of_appetiteはありますか？`` instead of localized labels.
    """

    def _follow_up_labels(self, species: str, message: str) -> list[tuple[str, str]]:
        client = app.test_client()
        r = client.post(
            "/api/diagnostic-chat/chat",
            json={"species": species, "message": message, "lang": "ja"},
        )
        assert r.status_code == 200
        data = r.get_json() or {}
        out: list[tuple[str, str]] = []
        for fq in data.get("follow_up_questions") or []:
            out.append((fq.get("question_ja", ""), fq.get("question_en", "")))
            for opt in fq.get("options") or []:
                out.append((opt.get("label_ja", ""), opt.get("label_en", "")))
        return out

    def _assert_no_snake_case_leak(self, pairs):
        for ja, en in pairs:
            for text in (ja, en):
                # Snake_case IDs always contain underscores; localized labels never do.
                assert "_" not in (text or ""), f"Raw symptom ID leaked into label: {text!r}"

    def test_dog_no_raw_ids(self):
        self._assert_no_snake_case_leak(self._follow_up_labels("dog", "咳と熱"))

    def test_cat_no_raw_ids(self):
        self._assert_no_snake_case_leak(self._follow_up_labels("cat", "下痢と嘔吐"))

    def test_horse_no_raw_ids(self):
        self._assert_no_snake_case_leak(self._follow_up_labels("horse", "fever and depression"))


class TestChatConfidencePercent:
    """Disease candidates returned to the chat UI must carry a calibrated
    ``confidence_percent`` so the frontend doesn't fall back to raw Jaccard.
    """

    def test_dog_candidate_has_confidence_percent(self):
        client = app.test_client()
        r = client.post(
            "/api/diagnostic-chat/chat",
            json={"species": "dog", "message": "咳と熱と食欲不振", "lang": "ja"},
        )
        assert r.status_code == 200
        cands = (r.get_json() or {}).get("disease_candidates") or []
        assert cands, "Expected at least one disease candidate"
        assert cands[0].get("confidence_percent") is not None
        assert 0 < cands[0]["confidence_percent"] <= 95.0

    def test_horse_candidate_has_confidence_percent(self):
        client = app.test_client()
        r = client.post(
            "/api/diagnostic-chat/chat",
            json={"species": "horse", "message": "fever and depression and ataxia", "lang": "en"},
        )
        assert r.status_code == 200
        cands = (r.get_json() or {}).get("disease_candidates") or []
        assert cands, "Expected at least one equine candidate"
        assert cands[0].get("confidence_percent") is not None
        assert 0 < cands[0]["confidence_percent"] <= 95.0


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
        r = client.post(
            "/api/diagnostic-chat/differential-analysis",
            json={
                "disease_id_1": "nonexistent_1",
                "disease_id_2": "nonexistent_2",
            },
        )
        assert r.status_code == 404


class TestTreatmentPlan:
    """Tests for POST /api/diagnostic-chat/treatment-plan."""

    def test_missing_disease_id(self):
        client = app.test_client()
        r = client.post("/api/diagnostic-chat/treatment-plan", json={})
        assert r.status_code == 400

    def test_unknown_disease_id(self):
        client = app.test_client()
        r = client.post(
            "/api/diagnostic-chat/treatment-plan",
            json={
                "disease_id": "nonexistent_disease",
            },
        )
        assert r.status_code == 404


class TestFeedback:
    """Tests for POST /api/diagnostic-chat/feedback."""

    def test_missing_session_id(self):
        client = app.test_client()
        r = client.post(
            "/api/diagnostic-chat/feedback",
            json={
                "feedback": "good",
            },
        )
        assert r.status_code == 400

    def test_invalid_feedback_type(self):
        client = app.test_client()
        r = client.post(
            "/api/diagnostic-chat/feedback",
            json={
                "session_id": "test-session",
                "feedback": "invalid_type",
            },
        )
        assert r.status_code == 400

    def test_valid_feedback(self):
        client = app.test_client()
        r = client.post(
            "/api/diagnostic-chat/feedback",
            json={
                "session_id": "test-session-123",
                "feedback": "good",
                "domain": "general",
            },
        )
        assert r.status_code == 201
        data = r.get_json()
        assert data["status"] == "recorded"
