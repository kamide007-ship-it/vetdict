"""Tests for the analytics API endpoints and helper functions."""

import pytest

from api.analytics import init_analytics, record_api_call
from api.vetdict_api import app as flask_app


@pytest.fixture()
def client():
    flask_app.config["TESTING"] = True
    # Ensure analytics tables exist
    init_analytics()
    with flask_app.test_client() as c:
        yield c


class TestAnalyticsEndpoints:
    """Tests for /api/admin/analytics/* endpoints."""

    def test_summary_empty(self, client):
        """Summary endpoint returns valid response with no data."""
        r = client.get("/api/admin/analytics/summary")
        assert r.status_code == 200
        data = r.get_json()
        assert data["success"] is True
        assert "total_requests" in data
        assert "today_requests" in data
        assert "avg_response_time_ms" in data
        assert "top_endpoints" in data
        assert "by_species" in data

    def test_daily_empty(self, client):
        """Daily endpoint returns valid response with no data."""
        r = client.get("/api/admin/analytics/daily")
        assert r.status_code == 200
        data = r.get_json()
        assert data["success"] is True
        assert "daily" in data
        assert isinstance(data["daily"], dict)

    def test_summary_after_recording(self, client):
        """Summary reflects recorded API calls."""
        record_api_call("/api/analyze-symptoms", "POST", "dog", 200, 50.0)
        record_api_call("/api/analyze-symptoms", "POST", "cat", 200, 30.0)
        record_api_call("/api/drugs", "GET", None, 200, 10.0)

        r = client.get("/api/admin/analytics/summary")
        data = r.get_json()
        assert data["total_requests"] >= 3
        assert data["avg_response_time_ms"] > 0

    def test_daily_after_recording(self, client):
        """Daily endpoint shows today's data after recording."""
        record_api_call("/api/test", "GET", None, 200, 5.0)

        r = client.get("/api/admin/analytics/daily")
        data = r.get_json()
        assert len(data["daily"]) >= 1

    def test_summary_species_breakdown(self, client):
        """Summary includes species breakdown for calls with species."""
        record_api_call("/api/analyze-symptoms", "POST", "rabbit", 200, 20.0)

        r = client.get("/api/admin/analytics/summary")
        data = r.get_json()
        assert "rabbit" in data["by_species"]


class TestRecordApiCall:
    """Tests for the record_api_call helper."""

    def test_record_does_not_raise(self):
        """Recording should never raise exceptions."""
        init_analytics()
        # Should not raise even with unusual values
        record_api_call("/test", "GET", None, 200, 0.0)
        record_api_call("/test", "POST", "dog", 500, 999.99)

    def test_record_with_none_species(self):
        """Recording with None species should work."""
        init_analytics()
        record_api_call("/test", "GET", None, 200, 1.0)
