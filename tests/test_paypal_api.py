"""Tests for PayPal subscription management API."""

import json
import os
from unittest.mock import patch

import flask

from api.paypal_api import (
    _load_subscribers,
    _load_waitlist,
    _save_subscribers,
    _save_waitlist,
    paypal_bp,
)


def _create_app():
    """Create a minimal Flask app with the PayPal blueprint."""
    app = flask.Flask(__name__)
    app.config["TESTING"] = True
    app.register_blueprint(paypal_bp)
    return app


# ---------------------------------------------------------------------------
# Subscriber storage helpers
# ---------------------------------------------------------------------------


class TestSubscriberStorage:
    """Tests for JSON-based subscriber persistence."""

    def test_load_subscribers_missing_file(self, tmp_path):
        with patch("api.paypal_api._SUBSCRIBERS_FILE", tmp_path / "missing.json"):
            result = _load_subscribers()
        assert result == {"subscribers": []}

    def test_load_subscribers_corrupt_file(self, tmp_path):
        bad = tmp_path / "corrupt.json"
        bad.write_text("{bad json", encoding="utf-8")
        with patch("api.paypal_api._SUBSCRIBERS_FILE", bad):
            result = _load_subscribers()
        assert result == {"subscribers": []}

    def test_save_and_load_roundtrip(self, tmp_path):
        path = tmp_path / "subs.json"
        data = {"subscribers": [{"subscription_id": "I-TEST123", "status": "active"}]}
        with patch("api.paypal_api._SUBSCRIBERS_FILE", path):
            _save_subscribers(data)
            loaded = _load_subscribers()
        assert loaded == data

    def test_save_creates_parent_dirs(self, tmp_path):
        path = tmp_path / "nested" / "dir" / "subs.json"
        with patch("api.paypal_api._SUBSCRIBERS_FILE", path):
            _save_subscribers({"subscribers": []})
        assert path.exists()


# ---------------------------------------------------------------------------
# Waitlist storage helpers
# ---------------------------------------------------------------------------


class TestWaitlistStorage:
    """Tests for JSON-based waitlist persistence."""

    def test_load_waitlist_missing_file(self, tmp_path):
        with patch("api.paypal_api._WAITLIST_FILE", tmp_path / "missing.json"):
            result = _load_waitlist()
        assert result == []

    def test_load_waitlist_corrupt_file(self, tmp_path):
        bad = tmp_path / "corrupt.json"
        bad.write_text("not json!", encoding="utf-8")
        with patch("api.paypal_api._WAITLIST_FILE", bad):
            result = _load_waitlist()
        assert result == []

    def test_save_and_load_roundtrip(self, tmp_path):
        path = tmp_path / "wl.json"
        data = [{"email": "vet@example.com", "signed_up_at": "2026-01-01T00:00:00"}]
        with patch("api.paypal_api._WAITLIST_FILE", path):
            _save_waitlist(data)
            loaded = _load_waitlist()
        assert loaded == data


# ---------------------------------------------------------------------------
# /api/paypal/activate endpoint
# ---------------------------------------------------------------------------


class TestActivateSubscription:
    """Tests for POST /api/paypal/activate."""

    def setup_method(self):
        self.app = _create_app()
        self.client = self.app.test_client()

    def test_activate_missing_subscription_id(self):
        resp = self.client.post(
            "/api/paypal/activate",
            json={"email": "test@example.com"},
        )
        assert resp.status_code == 400
        assert resp.get_json()["error"] == "subscription_id required"

    def test_activate_empty_subscription_id(self):
        resp = self.client.post(
            "/api/paypal/activate",
            json={"subscription_id": "  ", "email": "test@example.com"},
        )
        assert resp.status_code == 400

    def test_activate_success(self, tmp_path):
        path = tmp_path / "subs.json"
        with patch("api.paypal_api._SUBSCRIBERS_FILE", path):
            resp = self.client.post(
                "/api/paypal/activate",
                json={"subscription_id": "I-NEW123", "email": "vet@example.com"},
            )
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["status"] == "ok"
        assert data["subscription_id"] == "I-NEW123"

    def test_activate_duplicate_updates_email(self, tmp_path):
        path = tmp_path / "subs.json"
        initial = {
            "subscribers": [
                {"subscription_id": "I-DUP", "email": "", "status": "active"}
            ]
        }
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(initial), encoding="utf-8")

        with patch("api.paypal_api._SUBSCRIBERS_FILE", path):
            resp = self.client.post(
                "/api/paypal/activate",
                json={"subscription_id": "I-DUP", "email": "new@example.com"},
            )
        assert resp.status_code == 200
        # Verify email was updated
        saved = json.loads(path.read_text(encoding="utf-8"))
        assert saved["subscribers"][0]["email"] == "new@example.com"

    def test_activate_no_body(self):
        resp = self.client.post(
            "/api/paypal/activate",
            content_type="application/json",
            data="",
        )
        assert resp.status_code == 400


# ---------------------------------------------------------------------------
# /api/paypal/restore endpoint
# ---------------------------------------------------------------------------


class TestRestoreSubscription:
    """Tests for POST /api/paypal/restore."""

    def setup_method(self):
        self.app = _create_app()
        self.client = self.app.test_client()

    def test_restore_missing_email(self):
        resp = self.client.post("/api/paypal/restore", json={})
        assert resp.status_code == 400
        assert resp.get_json()["error"] == "email required"

    def test_restore_no_matching_subscription(self, tmp_path):
        path = tmp_path / "subs.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"subscribers": []}), encoding="utf-8")
        with patch("api.paypal_api._SUBSCRIBERS_FILE", path):
            resp = self.client.post(
                "/api/paypal/restore", json={"email": "nobody@example.com"}
            )
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["active"] is False
        assert data["error"] == "no_active_subscription"

    def test_restore_active_subscription_found(self, tmp_path):
        path = tmp_path / "subs.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        subs = {
            "subscribers": [
                {
                    "subscription_id": "I-RESTORE",
                    "email": "vet@example.com",
                    "status": "active",
                    "activated_at": "2026-01-15T10:00:00",
                }
            ]
        }
        path.write_text(json.dumps(subs), encoding="utf-8")
        with patch("api.paypal_api._SUBSCRIBERS_FILE", path):
            resp = self.client.post(
                "/api/paypal/restore", json={"email": "vet@example.com"}
            )
        data = resp.get_json()
        assert data["active"] is True
        assert data["subscription_id"] == "I-RESTORE"

    def test_restore_cancelled_subscription_not_returned(self, tmp_path):
        path = tmp_path / "subs.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        subs = {
            "subscribers": [
                {
                    "subscription_id": "I-CANCEL",
                    "email": "ex@example.com",
                    "status": "cancelled",
                }
            ]
        }
        path.write_text(json.dumps(subs), encoding="utf-8")
        with patch("api.paypal_api._SUBSCRIBERS_FILE", path):
            resp = self.client.post(
                "/api/paypal/restore", json={"email": "ex@example.com"}
            )
        assert resp.get_json()["active"] is False


# ---------------------------------------------------------------------------
# /api/paypal/verify endpoint
# ---------------------------------------------------------------------------


class TestVerifySubscription:
    """Tests for POST /api/paypal/verify."""

    def setup_method(self):
        self.app = _create_app()
        self.client = self.app.test_client()

    def test_verify_missing_id(self):
        resp = self.client.post("/api/paypal/verify", json={})
        assert resp.status_code == 400

    def test_verify_active(self, tmp_path):
        path = tmp_path / "subs.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        subs = {
            "subscribers": [
                {"subscription_id": "I-VERIFY", "status": "active"}
            ]
        }
        path.write_text(json.dumps(subs), encoding="utf-8")
        with patch("api.paypal_api._SUBSCRIBERS_FILE", path):
            resp = self.client.post(
                "/api/paypal/verify", json={"subscription_id": "I-VERIFY"}
            )
        data = resp.get_json()
        assert data["active"] is True

    def test_verify_inactive(self, tmp_path):
        path = tmp_path / "subs.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"subscribers": []}), encoding="utf-8")
        with patch("api.paypal_api._SUBSCRIBERS_FILE", path):
            resp = self.client.post(
                "/api/paypal/verify", json={"subscription_id": "I-MISSING"}
            )
        assert resp.get_json()["active"] is False


# ---------------------------------------------------------------------------
# /api/paypal/webhook endpoint
# ---------------------------------------------------------------------------


class TestWebhook:
    """Tests for POST /api/paypal/webhook."""

    def setup_method(self):
        self.app = _create_app()
        self.client = self.app.test_client()

    def test_webhook_no_subscription_id(self):
        resp = self.client.post(
            "/api/paypal/webhook",
            json={"event_type": "BILLING.SUBSCRIPTION.ACTIVATED", "resource": {}},
        )
        assert resp.status_code == 200
        assert resp.get_json()["status"] == "ignored"

    def test_webhook_activation_creates_subscriber(self, tmp_path):
        path = tmp_path / "subs.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"subscribers": []}), encoding="utf-8")
        with patch("api.paypal_api._SUBSCRIBERS_FILE", path):
            resp = self.client.post(
                "/api/paypal/webhook",
                json={
                    "event_type": "BILLING.SUBSCRIPTION.ACTIVATED",
                    "resource": {"id": "I-HOOK1"},
                },
            )
        assert resp.status_code == 200
        saved = json.loads(path.read_text(encoding="utf-8"))
        assert len(saved["subscribers"]) == 1
        assert saved["subscribers"][0]["status"] == "active"

    def test_webhook_payment_completed_updates_existing(self, tmp_path):
        path = tmp_path / "subs.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        subs = {
            "subscribers": [
                {"subscription_id": "I-PAY", "status": "active"}
            ]
        }
        path.write_text(json.dumps(subs), encoding="utf-8")
        with patch("api.paypal_api._SUBSCRIBERS_FILE", path):
            resp = self.client.post(
                "/api/paypal/webhook",
                json={
                    "event_type": "PAYMENT.SALE.COMPLETED",
                    "resource": {"id": "I-PAY"},
                },
            )
        assert resp.status_code == 200
        saved = json.loads(path.read_text(encoding="utf-8"))
        assert saved["subscribers"][0].get("last_payment") is not None

    def test_webhook_cancellation(self, tmp_path):
        path = tmp_path / "subs.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        subs = {
            "subscribers": [
                {"subscription_id": "I-CANCEL", "status": "active"}
            ]
        }
        path.write_text(json.dumps(subs), encoding="utf-8")
        with patch("api.paypal_api._SUBSCRIBERS_FILE", path):
            resp = self.client.post(
                "/api/paypal/webhook",
                json={
                    "event_type": "BILLING.SUBSCRIPTION.CANCELLED",
                    "resource": {"id": "I-CANCEL"},
                },
            )
        assert resp.status_code == 200
        saved = json.loads(path.read_text(encoding="utf-8"))
        assert saved["subscribers"][0]["status"] == "cancelled"

    def test_webhook_billing_agreement_id_fallback(self, tmp_path):
        """Subscription ID from billing_agreement_id when id is absent."""
        path = tmp_path / "subs.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"subscribers": []}), encoding="utf-8")
        with patch("api.paypal_api._SUBSCRIBERS_FILE", path):
            resp = self.client.post(
                "/api/paypal/webhook",
                json={
                    "event_type": "PAYMENT.SALE.COMPLETED",
                    "resource": {"billing_agreement_id": "I-BILL"},
                },
            )
        assert resp.status_code == 200
        saved = json.loads(path.read_text(encoding="utf-8"))
        assert saved["subscribers"][0]["subscription_id"] == "I-BILL"

    def test_webhook_invalid_signature_rejected(self, tmp_path):
        """When PAYPAL_WEBHOOK_ID is set and verification fails, return 403."""
        path = tmp_path / "subs.json"
        with (
            patch.dict(os.environ, {"PAYPAL_WEBHOOK_ID": "WH-TEST123"}),
            patch("api.paypal_api._verify_webhook_signature", return_value=False),
            patch("api.paypal_api._SUBSCRIBERS_FILE", path),
        ):
            resp = self.client.post(
                "/api/paypal/webhook",
                json={
                    "event_type": "BILLING.SUBSCRIPTION.ACTIVATED",
                    "resource": {"id": "I-BAD"},
                },
            )
        assert resp.status_code == 403


# ---------------------------------------------------------------------------
# /api/paypal/subscribers (admin)
# ---------------------------------------------------------------------------


class TestListSubscribers:
    """Tests for GET /api/paypal/subscribers."""

    def setup_method(self):
        self.app = _create_app()
        self.client = self.app.test_client()

    def test_unauthorized_without_token(self):
        resp = self.client.get("/api/paypal/subscribers")
        assert resp.status_code == 403

    def test_unauthorized_wrong_token(self):
        with patch.dict(os.environ, {"ADMIN_TOKEN": "secret123"}):
            resp = self.client.get(
                "/api/paypal/subscribers",
                headers={"X-Admin-Token": "wrong"},
            )
        assert resp.status_code == 403

    def test_authorized_returns_subscribers(self, tmp_path):
        path = tmp_path / "subs.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        subs = {
            "subscribers": [
                {"subscription_id": "I-A", "status": "active"},
                {"subscription_id": "I-B", "status": "cancelled"},
            ]
        }
        path.write_text(json.dumps(subs), encoding="utf-8")
        with (
            patch.dict(os.environ, {"ADMIN_TOKEN": "secret123"}),
            patch("api.paypal_api._SUBSCRIBERS_FILE", path),
        ):
            resp = self.client.get(
                "/api/paypal/subscribers",
                headers={"X-Admin-Token": "secret123"},
            )
        data = resp.get_json()
        assert data["total"] == 2
        assert data["active"] == 1


# ---------------------------------------------------------------------------
# /api/paypal/waitlist endpoints
# ---------------------------------------------------------------------------


class TestWaitlistEndpoints:
    """Tests for POST/GET /api/paypal/waitlist."""

    def setup_method(self):
        self.app = _create_app()
        self.client = self.app.test_client()

    def test_join_waitlist_invalid_email(self):
        resp = self.client.post("/api/paypal/waitlist", json={"email": "nope"})
        assert resp.status_code == 400

    def test_join_waitlist_empty_email(self):
        resp = self.client.post("/api/paypal/waitlist", json={"email": ""})
        assert resp.status_code == 400

    def test_join_waitlist_success(self, tmp_path):
        path = tmp_path / "wl.json"
        with patch("api.paypal_api._WAITLIST_FILE", path):
            resp = self.client.post(
                "/api/paypal/waitlist", json={"email": "vet@example.com"}
            )
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["status"] == "ok"
        assert data["total"] == 1

    def test_join_waitlist_duplicate_ignored(self, tmp_path):
        path = tmp_path / "wl.json"
        with patch("api.paypal_api._WAITLIST_FILE", path):
            self.client.post(
                "/api/paypal/waitlist", json={"email": "vet@example.com"}
            )
            resp = self.client.post(
                "/api/paypal/waitlist", json={"email": "vet@example.com"}
            )
        assert resp.get_json()["total"] == 1

    def test_get_waitlist_unauthorized(self):
        resp = self.client.get("/api/paypal/waitlist")
        assert resp.status_code == 403

    def test_get_waitlist_authorized(self, tmp_path):
        path = tmp_path / "wl.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps([{"email": "a@b.com", "signed_up_at": "2026-01-01"}]),
            encoding="utf-8",
        )
        with (
            patch.dict(os.environ, {"ADMIN_TOKEN": "secret"}),
            patch("api.paypal_api._WAITLIST_FILE", path),
        ):
            resp = self.client.get(
                "/api/paypal/waitlist",
                headers={"X-Admin-Token": "secret"},
            )
        data = resp.get_json()
        assert data["total"] == 1


# ---------------------------------------------------------------------------
# /api/paypal/create-subscription endpoint
# ---------------------------------------------------------------------------


class TestCreateSubscription:
    """Tests for POST /api/paypal/create-subscription."""

    def setup_method(self):
        self.app = _create_app()
        self.client = self.app.test_client()

    def test_create_subscription_no_secret(self):
        """Without PAYPAL_SECRET, token retrieval fails → 500."""
        with patch("api.paypal_api.PAYPAL_SECRET", ""):
            resp = self.client.post("/api/paypal/create-subscription")
        assert resp.status_code == 500
        assert "incomplete" in resp.get_json()["error"].lower()


# ---------------------------------------------------------------------------
# _get_paypal_token
# ---------------------------------------------------------------------------


class TestGetPaypalToken:
    """Tests for _get_paypal_token helper."""

    def test_returns_none_without_secret(self):
        from api.paypal_api import _get_paypal_token

        with patch("api.paypal_api.PAYPAL_SECRET", ""):
            assert _get_paypal_token() is None

    def test_returns_none_on_network_error(self):
        from api.paypal_api import _get_paypal_token

        with (
            patch("api.paypal_api.PAYPAL_SECRET", "test-secret"),
            patch("urllib.request.urlopen", side_effect=Exception("network error")),
        ):
            assert _get_paypal_token() is None
