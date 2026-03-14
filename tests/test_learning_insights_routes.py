"""Tests for learning_insights.py Flask route endpoints."""

import pytest
from unittest.mock import patch
from flask import Flask

from api.learning_insights import (
    bp,
    _generate_feedback_recommendations,
    _generate_accuracy_insights,
)


@pytest.fixture(autouse=True)
def _isolate_state(tmp_path):
    """Use a fresh temp dir for reco2 state to avoid file corruption."""
    state_file = str(tmp_path / "resonance_state.json")
    with patch("reco2.store.state_path", return_value=state_file):
        yield


@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(bp)
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()


class TestGetAccuracyMetrics:

    def test_returns_200(self, client):
        resp = client.get("/api/learning/accuracy")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "overall_accuracy" in data
        assert "accuracy_by_domain" in data
        assert "false_positive_rate" in data


class TestGetLearnedPatterns:

    def test_returns_200(self, client):
        resp = client.get("/api/learning/patterns")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "total_patterns" in data
        assert "patterns" in data
        assert "patterns_high_confidence" in data


class TestGetPersonalizationImpact:

    def test_returns_200(self, client):
        resp = client.get("/api/learning/personalization")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "total_segments" in data
        assert "by_age_stage" in data
        assert "puppy" in data["by_age_stage"]


class TestGetTuningHistory:

    def test_returns_200(self, client):
        resp = client.get("/api/learning/tuning-history")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "current_k" in data
        assert "current_eta" in data
        assert "recent_tuning" in data


class TestGetFeedbackQuality:

    def test_returns_200(self, client):
        resp = client.get("/api/learning/feedback-quality")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "feedback_rate" in data
        assert "signal_strength" in data
        assert "coverage" in data
        assert "recommendations" in data


class TestGetCombinedInsights:

    def test_returns_200(self, client):
        resp = client.get("/api/learning/insights")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "health_score" in data
        assert "ai_performance" in data
        assert "reco2_performance" in data
        assert "recommendations" in data


class TestRecordFeedback:

    def test_record_good_feedback(self, client):
        resp = client.post("/api/learning/feedback", json={
            "session_id": "test-123",
            "feedback": "good",
            "domain": "orthopedics",
        })
        assert resp.status_code == 201
        data = resp.get_json()
        assert data["status"] == "recorded"

    def test_record_with_ai_result(self, client):
        resp = client.post("/api/learning/feedback", json={
            "session_id": "test-789",
            "feedback": "good",
            "ai_result": {"symptoms": ["vomiting"], "confidence": 0.8},
            "correct_symptoms": ["vomiting"],
        })
        assert resp.status_code == 201
        data = resp.get_json()
        assert "ai_feedback" in data

    def test_empty_body(self, client):
        resp = client.post("/api/learning/feedback", json={})
        assert resp.status_code == 201


class TestGenerateFeedbackRecommendations:

    def test_low_rate(self):
        recs = _generate_feedback_recommendations(0.1, 30)
        assert any("Increase" in r for r in recs)

    def test_low_count(self):
        recs = _generate_feedback_recommendations(0.5, 5)
        assert any("Collect more" in r for r in recs)

    def test_good_quality(self):
        recs = _generate_feedback_recommendations(0.5, 30)
        assert recs == ["Good feedback signal quality"]


class TestGenerateAccuracyInsights:

    def test_correct_extraction(self):
        insights = _generate_accuracy_insights({"is_correct": True})
        assert any("accurate" in i for i in insights)

    def test_false_positives(self):
        insights = _generate_accuracy_insights({
            "false_positives": ["a", "b"],
        })
        assert any("2 symptoms" in i for i in insights)

    def test_false_negatives(self):
        insights = _generate_accuracy_insights({
            "false_negatives": ["c"],
        })
        assert any("Missed 1" in i for i in insights)

    def test_empty_evaluation(self):
        insights = _generate_accuracy_insights({})
        assert insights == ["Neutral feedback - no significant issues"]
