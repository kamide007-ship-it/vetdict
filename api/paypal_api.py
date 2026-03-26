"""PayPal subscription management API.

Handles subscription activation, verification, and webhook events.
"""

from __future__ import annotations

import base64
import json
import logging
import os
import urllib.request
from datetime import datetime
from pathlib import Path

from flask import Blueprint, jsonify, request

logger = logging.getLogger(__name__)

paypal_bp = Blueprint("paypal", __name__, url_prefix="/api/paypal")

# PayPal configuration
PAYPAL_CLIENT_ID = os.getenv(
    "PAYPAL_CLIENT_ID",
    "AX7kp51yXEJ_NiNH4dH-Y6NA-bDz7pFzT6uPgelYbXMjW3doC0I2wCGjHTGaIN2ExrixrLeXg4ZuVTUE",
)
PAYPAL_SECRET = os.getenv("PAYPAL_SECRET", "")
PAYPAL_PLAN_ID = os.getenv("PAYPAL_PLAN_ID", "P-5FB7289813535813HNHCF4OA")
PAYPAL_API_BASE = "https://api-m.paypal.com"


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
        logger.error(f"PayPal token error: {e}")
        return None

# Subscribers file (simple JSON-based storage)
_SUBSCRIBERS_FILE = Path(__file__).resolve().parent.parent / "instance" / "subscribers.json"


def _load_subscribers() -> dict:
    """Load subscribers from JSON file."""
    if _SUBSCRIBERS_FILE.exists():
        try:
            with open(_SUBSCRIBERS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return {"subscribers": []}


def _save_subscribers(data: dict) -> None:
    """Save subscribers to JSON file."""
    _SUBSCRIBERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(_SUBSCRIBERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


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
        logger.error(f"PayPal create subscription error: {e}")
        return jsonify({"error": str(e)}), 500


@paypal_bp.route("/activate", methods=["POST"])
def activate_subscription():
    """Record a new subscription activation from frontend."""
    body = request.get_json(silent=True) or {}
    subscription_id = body.get("subscription_id", "").strip()
    email = body.get("email", "").strip().lower()

    if not subscription_id:
        return jsonify({"error": "subscription_id required"}), 400

    data = _load_subscribers()
    # Check for duplicate
    existing = [s for s in data["subscribers"] if s["subscription_id"] == subscription_id]
    if existing:
        # Update email if provided
        if email and not existing[0].get("email"):
            existing[0]["email"] = email
            _save_subscribers(data)
    else:
        data["subscribers"].append({
            "subscription_id": subscription_id,
            "email": email,
            "status": "active",
            "activated_at": datetime.utcnow().isoformat(),
            "ip": request.remote_addr,
        })
        _save_subscribers(data)
        logger.info(f"PayPal subscription activated: {subscription_id} ({email})")

    return jsonify({"status": "ok", "subscription_id": subscription_id})


@paypal_bp.route("/restore", methods=["POST"])
def restore_subscription():
    """Restore Pro access on a new device using email address."""
    body = request.get_json(silent=True) or {}
    email = body.get("email", "").strip().lower()

    if not email:
        return jsonify({"active": False, "error": "email required"}), 400

    data = _load_subscribers()
    active_sub = next(
        (s for s in data["subscribers"]
         if s.get("email") == email and s.get("status") == "active"),
        None,
    )

    if active_sub:
        return jsonify({
            "active": True,
            "subscription_id": active_sub["subscription_id"],
            "activated_at": active_sub.get("activated_at", ""),
        })

    return jsonify({"active": False, "error": "no_active_subscription"})


@paypal_bp.route("/verify", methods=["POST"])
def verify_subscription():
    """Verify if a subscription ID is active."""
    body = request.get_json(silent=True) or {}
    subscription_id = body.get("subscription_id", "").strip()

    if not subscription_id:
        return jsonify({"active": False}), 400

    data = _load_subscribers()
    active = any(
        s["subscription_id"] == subscription_id and s.get("status") == "active"
        for s in data["subscribers"]
    )

    return jsonify({"active": active, "subscription_id": subscription_id})


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
    event_type = body.get("event_type", "")
    resource = body.get("resource", {})

    logger.info(f"PayPal webhook: {event_type}")

    subscription_id = resource.get("id", "")
    if not subscription_id:
        # For payment events, subscription ID is nested
        subscription_id = resource.get("billing_agreement_id", "")

    if not subscription_id:
        return jsonify({"status": "ignored"}), 200

    data = _load_subscribers()

    if event_type in ("BILLING.SUBSCRIPTION.ACTIVATED", "PAYMENT.SALE.COMPLETED"):
        # Activate or confirm
        existing = [s for s in data["subscribers"] if s["subscription_id"] == subscription_id]
        if existing:
            existing[0]["status"] = "active"
            existing[0]["last_payment"] = datetime.utcnow().isoformat()
        else:
            data["subscribers"].append({
                "subscription_id": subscription_id,
                "status": "active",
                "activated_at": datetime.utcnow().isoformat(),
                "last_payment": datetime.utcnow().isoformat(),
            })
        _save_subscribers(data)
        logger.info(f"Subscription activated/confirmed: {subscription_id}")

    elif event_type in (
        "BILLING.SUBSCRIPTION.CANCELLED",
        "BILLING.SUBSCRIPTION.SUSPENDED",
        "BILLING.SUBSCRIPTION.EXPIRED",
    ):
        # Deactivate
        for s in data["subscribers"]:
            if s["subscription_id"] == subscription_id:
                s["status"] = "cancelled"
                s["cancelled_at"] = datetime.utcnow().isoformat()
        _save_subscribers(data)
        logger.info(f"Subscription cancelled/suspended: {subscription_id}")

    return jsonify({"status": "processed"}), 200


@paypal_bp.route("/subscribers", methods=["GET"])
def list_subscribers():
    """Admin endpoint: list all subscribers (requires admin token)."""
    token = request.headers.get("X-Admin-Token", "")
    admin_token = os.getenv("ADMIN_TOKEN", "kamide007")
    if token != admin_token:
        return jsonify({"error": "unauthorized"}), 403

    data = _load_subscribers()
    active_count = sum(1 for s in data["subscribers"] if s.get("status") == "active")

    return jsonify({
        "total": len(data["subscribers"]),
        "active": active_count,
        "subscribers": data["subscribers"],
    })


# ---------------------------------------------------------------------------
# Email waitlist for launch notification
# ---------------------------------------------------------------------------
_WAITLIST_FILE = Path(__file__).resolve().parent.parent / "instance" / "waitlist.json"


def _load_waitlist() -> list:
    if _WAITLIST_FILE.exists():
        try:
            with open(_WAITLIST_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return []


def _save_waitlist(data: list) -> None:
    _WAITLIST_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(_WAITLIST_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


@paypal_bp.route("/waitlist", methods=["POST"])
def join_waitlist():
    """Add email to launch notification waitlist."""
    body = request.get_json(silent=True) or {}
    email = body.get("email", "").strip().lower()

    if not email or "@" not in email:
        return jsonify({"error": "valid email required"}), 400

    waitlist = _load_waitlist()
    if email not in [e.get("email") for e in waitlist]:
        waitlist.append({
            "email": email,
            "signed_up_at": datetime.utcnow().isoformat(),
        })
        _save_waitlist(waitlist)
        logger.info(f"Waitlist signup: {email}")

    return jsonify({"status": "ok", "total": len(waitlist)})


@paypal_bp.route("/waitlist", methods=["GET"])
def get_waitlist():
    """Admin: list waitlist emails."""
    token = request.headers.get("X-Admin-Token", "")
    admin_token = os.getenv("ADMIN_TOKEN", "kamide007")
    if token != admin_token:
        return jsonify({"error": "unauthorized"}), 403
    waitlist = _load_waitlist()
    return jsonify({"total": len(waitlist), "emails": waitlist})
