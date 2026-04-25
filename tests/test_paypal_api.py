"""Tests for PayPal subscription management API (SQLite-backed)."""

import os
from unittest.mock import patch

import flask

from api.paypal_api import (
    _get_subscribers_db,
    _get_waitlist_db,
    paypal_bp,
)


def _create_app():
    """Create a minimal Flask app with the PayPal blueprint."""
    app = flask.Flask(__name__)
    app.config["TESTING"] = True
    app.register_blueprint(paypal_bp)
    return app


# ---------------------------------------------------------------------------
# Subscriber storage (SQLite)
# ---------------------------------------------------------------------------


class TestSubscriberStorage:
    """Tests for SQLite-based subscriber persistence."""

    def test_subscribers_db_creates_table(self, tmp_path):
        db_path = tmp_path / "subs.db"
        with patch("api.paypal_api._SUBSCRIBERS_DB", db_path):
            conn = _get_subscribers_db()
            try:
                tables = conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name='subscribers'"
                ).fetchall()
                assert len(tables) == 1
            finally:
                conn.close()

    def test_subscribers_db_insert_and_query(self, tmp_path):
        db_path = tmp_path / "subs.db"
        with patch("api.paypal_api._SUBSCRIBERS_DB", db_path):
            conn = _get_subscribers_db()
            try:
                conn.execute(
                    "INSERT INTO subscribers (subscription_id, email, status, activated_at) VALUES (?, ?, ?, ?)",
                    ("I-TEST", "vet@example.com", "active", "2026-01-01"),
                )
                conn.commit()
                row = conn.execute("SELECT * FROM subscribers WHERE subscription_id = 'I-TEST'").fetchone()
                assert row["email"] == "vet@example.com"
                assert row["status"] == "active"
            finally:
                conn.close()


# ---------------------------------------------------------------------------
# Waitlist storage (SQLite)
# ---------------------------------------------------------------------------


class TestWaitlistStorage:
    """Tests for SQLite-based waitlist persistence."""

    def test_waitlist_db_creates_table(self, tmp_path):
        db_path = tmp_path / "wl.db"
        with patch("api.paypal_api._WAITLIST_DB", db_path):
            conn = _get_waitlist_db()
            try:
                tables = conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' AND name='waitlist'"
                ).fetchall()
                assert len(tables) == 1
            finally:
                conn.close()

    def test_waitlist_unique_email(self, tmp_path):
        db_path = tmp_path / "wl.db"
        with patch("api.paypal_api._WAITLIST_DB", db_path):
            conn = _get_waitlist_db()
            try:
                conn.execute(
                    "INSERT INTO waitlist (email, signed_up_at) VALUES (?, ?)",
                    ("vet@example.com", "2026-01-01"),
                )
                conn.commit()
                conn.execute(
                    "INSERT OR IGNORE INTO waitlist (email, signed_up_at) VALUES (?, ?)",
                    ("vet@example.com", "2026-01-02"),
                )
                conn.commit()
                count = conn.execute("SELECT COUNT(*) FROM waitlist").fetchone()[0]
                assert count == 1
            finally:
                conn.close()


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
        db_path = tmp_path / "subs.db"
        with patch("api.paypal_api._SUBSCRIBERS_DB", db_path):
            resp = self.client.post(
                "/api/paypal/activate",
                json={"subscription_id": "I-NEW123", "email": "vet@example.com"},
            )
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["status"] == "ok"
        assert data["subscription_id"] == "I-NEW123"

    def test_activate_duplicate_updates_email(self, tmp_path):
        db_path = tmp_path / "subs.db"
        with patch("api.paypal_api._SUBSCRIBERS_DB", db_path):
            # First activation without email
            conn = _get_subscribers_db()
            try:
                conn.execute(
                    "INSERT INTO subscribers (subscription_id, email, status, activated_at) VALUES (?, ?, ?, ?)",
                    ("I-DUP", "", "active", "2026-01-01"),
                )
                conn.commit()
            finally:
                conn.close()

            resp = self.client.post(
                "/api/paypal/activate",
                json={"subscription_id": "I-DUP", "email": "new@example.com"},
            )
        assert resp.status_code == 200
        # Verify email was updated
        with patch("api.paypal_api._SUBSCRIBERS_DB", db_path):
            conn = _get_subscribers_db()
            try:
                row = conn.execute("SELECT email FROM subscribers WHERE subscription_id = 'I-DUP'").fetchone()
                assert row["email"] == "new@example.com"
            finally:
                conn.close()

    def test_activate_no_body(self):
        resp = self.client.post(
            "/api/paypal/activate",
            content_type="application/json",
            data="",
        )
        assert resp.status_code == 400

    def test_activate_rejects_malformed_email(self):
        resp = self.client.post(
            "/api/paypal/activate",
            json={"subscription_id": "I-BAD", "email": "not-an-email"},
        )
        assert resp.status_code == 400
        assert resp.get_json()["error"] == "invalid email format"


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

    def test_restore_rejects_malformed_email(self):
        resp = self.client.post("/api/paypal/restore", json={"email": "garbage"})
        assert resp.status_code == 400
        assert resp.get_json()["error"] == "invalid email format"

    def test_restore_no_matching_subscription(self, tmp_path):
        db_path = tmp_path / "subs.db"
        with patch("api.paypal_api._SUBSCRIBERS_DB", db_path):
            resp = self.client.post(
                "/api/paypal/restore", json={"email": "nobody@example.com"}
            )
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["active"] is False
        assert data["error"] == "no_active_subscription"

    def test_restore_active_subscription_found(self, tmp_path):
        db_path = tmp_path / "subs.db"
        with patch("api.paypal_api._SUBSCRIBERS_DB", db_path):
            conn = _get_subscribers_db()
            try:
                conn.execute(
                    "INSERT INTO subscribers (subscription_id, email, status, activated_at) VALUES (?, ?, ?, ?)",
                    ("I-RESTORE", "vet@example.com", "active", "2026-01-15T10:00:00"),
                )
                conn.commit()
            finally:
                conn.close()

            resp = self.client.post(
                "/api/paypal/restore", json={"email": "vet@example.com"}
            )
        data = resp.get_json()
        assert data["active"] is True
        assert data["subscription_id"] == "I-RESTORE"

    def test_restore_cancelled_subscription_not_returned(self, tmp_path):
        db_path = tmp_path / "subs.db"
        with patch("api.paypal_api._SUBSCRIBERS_DB", db_path):
            conn = _get_subscribers_db()
            try:
                conn.execute(
                    "INSERT INTO subscribers (subscription_id, email, status) VALUES (?, ?, ?)",
                    ("I-CANCEL", "ex@example.com", "cancelled"),
                )
                conn.commit()
            finally:
                conn.close()

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
        db_path = tmp_path / "subs.db"
        with patch("api.paypal_api._SUBSCRIBERS_DB", db_path):
            conn = _get_subscribers_db()
            try:
                conn.execute(
                    "INSERT INTO subscribers (subscription_id, status) VALUES (?, ?)",
                    ("I-VERIFY", "active"),
                )
                conn.commit()
            finally:
                conn.close()

            resp = self.client.post(
                "/api/paypal/verify", json={"subscription_id": "I-VERIFY"}
            )
        data = resp.get_json()
        assert data["active"] is True

    def test_verify_inactive(self, tmp_path):
        db_path = tmp_path / "subs.db"
        with patch("api.paypal_api._SUBSCRIBERS_DB", db_path):
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
        with patch("api.paypal_api._verify_webhook_signature", return_value=True):
            resp = self.client.post(
                "/api/paypal/webhook",
                json={"event_type": "BILLING.SUBSCRIPTION.ACTIVATED", "resource": {}},
            )
        assert resp.status_code == 200
        assert resp.get_json()["status"] == "ignored"

    def test_webhook_activation_creates_subscriber(self, tmp_path):
        db_path = tmp_path / "subs.db"
        with (
            patch("api.paypal_api._SUBSCRIBERS_DB", db_path),
            patch("api.paypal_api._verify_webhook_signature", return_value=True),
        ):
            resp = self.client.post(
                "/api/paypal/webhook",
                json={
                    "event_type": "BILLING.SUBSCRIPTION.ACTIVATED",
                    "resource": {"id": "I-HOOK1"},
                },
            )
        assert resp.status_code == 200
        with patch("api.paypal_api._SUBSCRIBERS_DB", db_path):
            conn = _get_subscribers_db()
            try:
                row = conn.execute("SELECT * FROM subscribers WHERE subscription_id = 'I-HOOK1'").fetchone()
                assert row is not None
                assert row["status"] == "active"
            finally:
                conn.close()

    def test_webhook_payment_completed_updates_existing(self, tmp_path):
        db_path = tmp_path / "subs.db"
        with patch("api.paypal_api._SUBSCRIBERS_DB", db_path):
            conn = _get_subscribers_db()
            try:
                conn.execute(
                    "INSERT INTO subscribers (subscription_id, status) VALUES (?, ?)",
                    ("I-PAY", "active"),
                )
                conn.commit()
            finally:
                conn.close()

        with (
            patch("api.paypal_api._SUBSCRIBERS_DB", db_path),
            patch("api.paypal_api._verify_webhook_signature", return_value=True),
        ):
            resp = self.client.post(
                "/api/paypal/webhook",
                json={
                    "event_type": "PAYMENT.SALE.COMPLETED",
                    "resource": {"id": "I-PAY"},
                },
            )
        assert resp.status_code == 200
        with patch("api.paypal_api._SUBSCRIBERS_DB", db_path):
            conn = _get_subscribers_db()
            try:
                row = conn.execute("SELECT last_payment FROM subscribers WHERE subscription_id = 'I-PAY'").fetchone()
                assert row["last_payment"] is not None
            finally:
                conn.close()

    def test_webhook_cancellation(self, tmp_path):
        db_path = tmp_path / "subs.db"
        with patch("api.paypal_api._SUBSCRIBERS_DB", db_path):
            conn = _get_subscribers_db()
            try:
                conn.execute(
                    "INSERT INTO subscribers (subscription_id, status) VALUES (?, ?)",
                    ("I-CANCEL", "active"),
                )
                conn.commit()
            finally:
                conn.close()

        with (
            patch("api.paypal_api._SUBSCRIBERS_DB", db_path),
            patch("api.paypal_api._verify_webhook_signature", return_value=True),
        ):
            resp = self.client.post(
                "/api/paypal/webhook",
                json={
                    "event_type": "BILLING.SUBSCRIPTION.CANCELLED",
                    "resource": {"id": "I-CANCEL"},
                },
            )
        assert resp.status_code == 200
        with patch("api.paypal_api._SUBSCRIBERS_DB", db_path):
            conn = _get_subscribers_db()
            try:
                row = conn.execute("SELECT status FROM subscribers WHERE subscription_id = 'I-CANCEL'").fetchone()
                assert row["status"] == "cancelled"
            finally:
                conn.close()

    def test_webhook_billing_agreement_id_fallback(self, tmp_path):
        """Subscription ID from billing_agreement_id when id is absent."""
        db_path = tmp_path / "subs.db"
        with (
            patch("api.paypal_api._SUBSCRIBERS_DB", db_path),
            patch("api.paypal_api._verify_webhook_signature", return_value=True),
        ):
            resp = self.client.post(
                "/api/paypal/webhook",
                json={
                    "event_type": "PAYMENT.SALE.COMPLETED",
                    "resource": {"billing_agreement_id": "I-BILL"},
                },
            )
        assert resp.status_code == 200
        with patch("api.paypal_api._SUBSCRIBERS_DB", db_path):
            conn = _get_subscribers_db()
            try:
                row = conn.execute("SELECT * FROM subscribers WHERE subscription_id = 'I-BILL'").fetchone()
                assert row is not None
            finally:
                conn.close()

    def test_webhook_invalid_signature_rejected(self):
        """When verification fails, return 403."""
        with patch("api.paypal_api._verify_webhook_signature", return_value=False):
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
        db_path = tmp_path / "subs.db"
        with patch("api.paypal_api._SUBSCRIBERS_DB", db_path):
            conn = _get_subscribers_db()
            try:
                conn.execute(
                    "INSERT INTO subscribers (subscription_id, status) VALUES (?, ?)",
                    ("I-A", "active"),
                )
                conn.execute(
                    "INSERT INTO subscribers (subscription_id, status) VALUES (?, ?)",
                    ("I-B", "cancelled"),
                )
                conn.commit()
            finally:
                conn.close()

        with (
            patch.dict(os.environ, {"ADMIN_TOKEN": "secret123"}),
            patch("api.paypal_api._SUBSCRIBERS_DB", db_path),
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
        db_path = tmp_path / "wl.db"
        with patch("api.paypal_api._WAITLIST_DB", db_path):
            resp = self.client.post(
                "/api/paypal/waitlist", json={"email": "vet@example.com"}
            )
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["status"] == "ok"
        assert data["total"] == 1

    def test_join_waitlist_duplicate_ignored(self, tmp_path):
        db_path = tmp_path / "wl.db"
        with patch("api.paypal_api._WAITLIST_DB", db_path):
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
        db_path = tmp_path / "wl.db"
        with patch("api.paypal_api._WAITLIST_DB", db_path):
            conn = _get_waitlist_db()
            try:
                conn.execute(
                    "INSERT INTO waitlist (email, signed_up_at) VALUES (?, ?)",
                    ("a@b.com", "2026-01-01"),
                )
                conn.commit()
            finally:
                conn.close()

        with (
            patch.dict(os.environ, {"ADMIN_TOKEN": "secret"}),
            patch("api.paypal_api._WAITLIST_DB", db_path),
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
        """Without PAYPAL_SECRET, token retrieval fails -> 500."""
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
