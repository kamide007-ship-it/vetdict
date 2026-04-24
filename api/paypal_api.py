"""PayPal subscription management API.

Handles subscription activation, verification, and webhook events.
"""

from __future__ import annotations

import base64
import hmac
import json
import logging
import os
import urllib.request
from datetime import datetime
from pathlib import Path

from flask import Blueprint, jsonify, request

logger = logging.getLogger(__name__)

paypal_bp = Blueprint("paypal", __name__, url_prefix="/api/paypal")

# PayPal configuration — all credentials via environment variables only
PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID", "")
PAYPAL_SECRET = os.getenv("PAYPAL_SECRET", "")
PAYPAL_PLAN_ID = os.getenv("PAYPAL_PLAN_ID", "")
# Switch to https://api-m.sandbox.paypal.com for sandbox testing by setting
# PAYPAL_API_BASE in the environment. Defaults to production.
PAYPAL_API_BASE = os.getenv("PAYPAL_API_BASE", "https://api-m.paypal.com").rstrip("/")


def _get_paypal_token() -> str | None:
    """Get PayPal OAuth2 access token."""
    if not PAYPAL_SECRET:
        return None
    auth = base64.b64encode(f"{PAYPAL_CLIENT_ID}:{PAYPAL_SECRET}".encode()).decode()
    req = urllib.request.Request(
        f"{PAYPAL_API_BASE}/v1/oauth2/token",
        data=b"grant_type=client_credentials",
        headers={"Authorization": f"Basic {auth}", "Content-Type": "application/x-www-form-urlencoded"},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read()).get("access_token")
    except Exception as e:
        logger.error("PayPal token error: %s", e)
        return None

# Subscribers database (SQLite-backed)
_SUBSCRIBERS_DB = Path(__file__).resolve().parent.parent / "instance" / "subscribers.db"


def _get_subscribers_db():
    """Get a connection to the subscribers SQLite database."""
    import sqlite3 as _sqlite3

    db_path = str(_SUBSCRIBERS_DB)
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = _sqlite3.connect(db_path, timeout=5.0)
    conn.row_factory = _sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS subscribers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subscription_id TEXT UNIQUE NOT NULL,
            email TEXT DEFAULT '',
            status TEXT DEFAULT 'active',
            activated_at TEXT,
            last_payment TEXT,
            cancelled_at TEXT,
            ip TEXT DEFAULT ''
        )
    """)
    conn.commit()
    return conn


def _migrate_subscribers_json():
    """One-time migration: move subscribers.json data into SQLite."""
    json_path = Path(__file__).resolve().parent.parent / "instance" / "subscribers.json"
    if not json_path.exists():
        return
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        subs = data.get("subscribers", [])
        if not subs:
            json_path.unlink(missing_ok=True)
            return
        conn = _get_subscribers_db()
        try:
            for s in subs:
                conn.execute(
                    """INSERT OR IGNORE INTO subscribers
                       (subscription_id, email, status, activated_at, last_payment, cancelled_at, ip)
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (
                        s.get("subscription_id", ""),
                        s.get("email", ""),
                        s.get("status", "active"),
                        s.get("activated_at", ""),
                        s.get("last_payment", ""),
                        s.get("cancelled_at", ""),
                        s.get("ip", ""),
                    ),
                )
            conn.commit()
        finally:
            conn.close()
        json_path.unlink(missing_ok=True)
        logger.info("Migrated %d subscribers from JSON to SQLite", len(subs))
    except Exception as e:
        logger.error("Subscriber JSON migration error: %s", e)


# Run migration on module load
_migrate_subscribers_json()


@paypal_bp.route("/create-subscription", methods=["POST"])
def create_subscription():
    """Create a PayPal subscription and return the approval URL."""
    token = _get_paypal_token()
    if not token:
        return jsonify({"error": "PayPal configuration incomplete"}), 500

    sub_data = {
        "plan_id": PAYPAL_PLAN_ID,
        "application_context": {
            "brand_name": "VetDict",
            "locale": "ja-JP",
            "user_action": "SUBSCRIBE_NOW",
            "return_url": request.host_url.rstrip("/") + "/?pro=activated",
            "cancel_url": request.host_url.rstrip("/") + "/#pricing",
        },
    }
    req = urllib.request.Request(
        f"{PAYPAL_API_BASE}/v1/billing/subscriptions",
        data=json.dumps(sub_data).encode(),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Prefer": "return=representation",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            sub = json.loads(resp.read())
            approve_url = next(
                (l["href"] for l in sub.get("links", []) if l["rel"] == "approve"), None
            )
            return jsonify({
                "subscription_id": sub.get("id"),
                "approve_url": approve_url,
                "status": sub.get("status"),
            })
    except Exception as e:
        logger.error("PayPal create subscription error: %s", e)
        return jsonify({"error": "PayPal subscription creation failed"}), 500


@paypal_bp.route("/activate", methods=["POST"])
def activate_subscription():
    """Record a new subscription activation from frontend."""
    body = request.get_json(silent=True) or {}
    subscription_id = body.get("subscription_id", "").strip()
    email = body.get("email", "").strip().lower()

    if not subscription_id:
        return jsonify({"error": "subscription_id required"}), 400

    conn = _get_subscribers_db()
    try:
        existing = conn.execute(
            "SELECT id, email FROM subscribers WHERE subscription_id = ?",
            (subscription_id,),
        ).fetchone()
        if existing:
            if email and not existing["email"]:
                conn.execute(
                    "UPDATE subscribers SET email = ? WHERE subscription_id = ?",
                    (email, subscription_id),
                )
                conn.commit()
        else:
            conn.execute(
                """INSERT INTO subscribers (subscription_id, email, status, activated_at, ip)
                   VALUES (?, ?, 'active', ?, ?)""",
                (subscription_id, email, datetime.utcnow().isoformat(), request.remote_addr or ""),
            )
            conn.commit()
            logger.info("PayPal subscription activated: %s (%s)", subscription_id, email)
    finally:
        conn.close()

    return jsonify({"status": "ok", "subscription_id": subscription_id})


@paypal_bp.route("/restore", methods=["POST"])
def restore_subscription():
    """Restore Pro access on a new device using email address."""
    body = request.get_json(silent=True) or {}
    email = body.get("email", "").strip().lower()

    if not email:
        return jsonify({"active": False, "error": "email required"}), 400

    conn = _get_subscribers_db()
    try:
        active_sub = conn.execute(
            "SELECT subscription_id, activated_at FROM subscribers WHERE email = ? AND status = 'active' LIMIT 1",
            (email,),
        ).fetchone()
    finally:
        conn.close()

    if active_sub:
        return jsonify({
            "active": True,
            "subscription_id": active_sub["subscription_id"],
            "activated_at": active_sub["activated_at"] or "",
        })

    return jsonify({"active": False, "error": "no_active_subscription"})


@paypal_bp.route("/verify", methods=["POST"])
def verify_subscription():
    """Verify if a subscription ID is active."""
    body = request.get_json(silent=True) or {}
    subscription_id = body.get("subscription_id", "").strip()

    if not subscription_id:
        return jsonify({"active": False}), 400

    conn = _get_subscribers_db()
    try:
        row = conn.execute(
            "SELECT 1 FROM subscribers WHERE subscription_id = ? AND status = 'active'",
            (subscription_id,),
        ).fetchone()
    finally:
        conn.close()

    return jsonify({"active": row is not None, "subscription_id": subscription_id})


def _verify_webhook_signature(request_obj) -> bool:
    """Verify PayPal webhook signature using transmission headers."""
    webhook_id = os.getenv("PAYPAL_WEBHOOK_ID", "")
    if not webhook_id:
        is_debug = os.getenv("FLASK_DEBUG", "0").strip().lower() in ("1", "true", "yes", "on")
        if is_debug:
            logger.warning("PAYPAL_WEBHOOK_ID not set — skipping verification (debug mode)")
            return True
        logger.error("PAYPAL_WEBHOOK_ID not set — rejecting webhook in production")
        return False

    token = _get_paypal_token()
    if not token:
        return False

    verify_data = {
        "auth_algo": request_obj.headers.get("Paypal-Auth-Algo", ""),
        "cert_url": request_obj.headers.get("Paypal-Cert-Url", ""),
        "transmission_id": request_obj.headers.get("Paypal-Transmission-Id", ""),
        "transmission_sig": request_obj.headers.get("Paypal-Transmission-Sig", ""),
        "transmission_time": request_obj.headers.get("Paypal-Transmission-Time", ""),
        "webhook_id": webhook_id,
        "webhook_event": request_obj.get_json(silent=True) or {},
    }

    req = urllib.request.Request(
        f"{PAYPAL_API_BASE}/v1/notifications/verify-webhook-signature",
        data=json.dumps(verify_data).encode(),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read())
            return result.get("verification_status") == "SUCCESS"
    except Exception as e:
        logger.error("Webhook signature verification failed: %s", e)
        return False


@paypal_bp.route("/webhook", methods=["POST"])
def paypal_webhook():
    """Handle PayPal webhook events (subscription lifecycle).

    Events:
    - BILLING.SUBSCRIPTION.ACTIVATED
    - BILLING.SUBSCRIPTION.CANCELLED
    - BILLING.SUBSCRIPTION.SUSPENDED
    - BILLING.SUBSCRIPTION.EXPIRED
    - PAYMENT.SALE.COMPLETED
    """
    body = request.get_json(silent=True) or {}

    # Always verify webhook signature (fails closed in production if WEBHOOK_ID not set)
    if not _verify_webhook_signature(request):
        logger.warning("Invalid PayPal webhook signature")
        return jsonify({"error": "invalid signature"}), 403

    event_type = body.get("event_type", "")
    resource = body.get("resource", {})

    logger.info("PayPal webhook: %s", event_type)

    subscription_id = resource.get("id", "")
    if not subscription_id:
        # For payment events, subscription ID is nested
        subscription_id = resource.get("billing_agreement_id", "")

    if not subscription_id:
        return jsonify({"status": "ignored"}), 200

    now = datetime.utcnow().isoformat()
    conn = _get_subscribers_db()
    try:
        if event_type in ("BILLING.SUBSCRIPTION.ACTIVATED", "PAYMENT.SALE.COMPLETED"):
            existing = conn.execute(
                "SELECT id FROM subscribers WHERE subscription_id = ?",
                (subscription_id,),
            ).fetchone()
            if existing:
                conn.execute(
                    "UPDATE subscribers SET status = 'active', last_payment = ? WHERE subscription_id = ?",
                    (now, subscription_id),
                )
            else:
                conn.execute(
                    """INSERT INTO subscribers (subscription_id, status, activated_at, last_payment)
                       VALUES (?, 'active', ?, ?)""",
                    (subscription_id, now, now),
                )
            conn.commit()
            logger.info("Subscription activated/confirmed: %s", subscription_id)

        elif event_type in (
            "BILLING.SUBSCRIPTION.CANCELLED",
            "BILLING.SUBSCRIPTION.SUSPENDED",
            "BILLING.SUBSCRIPTION.EXPIRED",
        ):
            conn.execute(
                "UPDATE subscribers SET status = 'cancelled', cancelled_at = ? WHERE subscription_id = ?",
                (now, subscription_id),
            )
            conn.commit()
            logger.info("Subscription cancelled/suspended: %s", subscription_id)
    finally:
        conn.close()

    return jsonify({"status": "processed"}), 200


@paypal_bp.route("/subscribers", methods=["GET"])
def list_subscribers():
    """Admin endpoint: list all subscribers (requires admin token)."""
    token = request.headers.get("X-Admin-Token", "")
    admin_token = os.getenv("ADMIN_TOKEN", "")
    if not admin_token or not hmac.compare_digest(token, admin_token):
        return jsonify({"error": "unauthorized"}), 403

    conn = _get_subscribers_db()
    try:
        rows = conn.execute(
            "SELECT subscription_id, email, status, activated_at, last_payment, cancelled_at FROM subscribers ORDER BY id"
        ).fetchall()
        subscribers = [dict(r) for r in rows]
        active_count = sum(1 for s in subscribers if s.get("status") == "active")
    finally:
        conn.close()

    return jsonify({
        "total": len(subscribers),
        "active": active_count,
        "subscribers": subscribers,
    })


# ---------------------------------------------------------------------------
# Email waitlist for launch notification (SQLite-backed)
# ---------------------------------------------------------------------------
_WAITLIST_DB = Path(__file__).resolve().parent.parent / "instance" / "waitlist.db"


def _get_waitlist_db():
    """Get a connection to the waitlist SQLite database."""
    import sqlite3 as _sqlite3

    db_path = str(_WAITLIST_DB)
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    conn = _sqlite3.connect(db_path, timeout=5.0)
    conn.row_factory = _sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS waitlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            signed_up_at TEXT NOT NULL
        )
    """)
    conn.commit()
    return conn


def _migrate_waitlist_json():
    """One-time migration: move waitlist.json data into SQLite, then remove the file."""
    json_path = Path(__file__).resolve().parent.parent / "instance" / "waitlist.json"
    if not json_path.exists():
        return
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            entries = json.load(f)
        if not entries:
            json_path.unlink(missing_ok=True)
            return
        conn = _get_waitlist_db()
        try:
            for entry in entries:
                email = entry.get("email", "").strip().lower()
                signed_up = entry.get("signed_up_at", datetime.utcnow().isoformat())
                if email:
                    conn.execute(
                        "INSERT OR IGNORE INTO waitlist (email, signed_up_at) VALUES (?, ?)",
                        (email, signed_up),
                    )
            conn.commit()
        finally:
            conn.close()
        json_path.unlink(missing_ok=True)
        logger.info("Migrated %d waitlist entries from JSON to SQLite", len(entries))
    except Exception as e:
        logger.error("Waitlist JSON migration error: %s", e)


# Run migration on module load
_migrate_waitlist_json()


@paypal_bp.route("/waitlist", methods=["POST"])
def join_waitlist():
    """Add email to launch notification waitlist."""
    body = request.get_json(silent=True) or {}
    email = body.get("email", "").strip().lower()

    if not email or "@" not in email:
        return jsonify({"error": "valid email required"}), 400

    conn = _get_waitlist_db()
    try:
        conn.execute(
            "INSERT OR IGNORE INTO waitlist (email, signed_up_at) VALUES (?, ?)",
            (email, datetime.utcnow().isoformat()),
        )
        conn.commit()
        total = conn.execute("SELECT COUNT(*) FROM waitlist").fetchone()[0]
    finally:
        conn.close()

    logger.info("Waitlist signup: %s", email)
    return jsonify({"status": "ok", "total": total})


@paypal_bp.route("/waitlist", methods=["GET"])
def get_waitlist():
    """Admin: list waitlist emails."""
    token = request.headers.get("X-Admin-Token", "")
    admin_token = os.getenv("ADMIN_TOKEN", "")
    if not admin_token or not hmac.compare_digest(token, admin_token):
        return jsonify({"error": "unauthorized"}), 403

    conn = _get_waitlist_db()
    try:
        rows = conn.execute("SELECT email, signed_up_at FROM waitlist ORDER BY id").fetchall()
        waitlist = [{"email": r["email"], "signed_up_at": r["signed_up_at"]} for r in rows]
    finally:
        conn.close()

    return jsonify({"total": len(waitlist), "emails": waitlist})
