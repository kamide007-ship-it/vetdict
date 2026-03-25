"""PayPal subscription management API.

Handles subscription activation, verification, and webhook events.
"""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime
from pathlib import Path

from flask import Blueprint, jsonify, request

logger = logging.getLogger(__name__)

paypal_bp = Blueprint("paypal", __name__, url_prefix="/api/paypal")

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


@paypal_bp.route("/activate", methods=["POST"])
def activate_subscription():
    """Record a new subscription activation from frontend."""
    body = request.get_json(silent=True) or {}
    subscription_id = body.get("subscription_id", "").strip()

    if not subscription_id:
        return jsonify({"error": "subscription_id required"}), 400

    data = _load_subscribers()
    # Check for duplicate
    existing = [s for s in data["subscribers"] if s["subscription_id"] == subscription_id]
    if not existing:
        data["subscribers"].append({
            "subscription_id": subscription_id,
            "status": "active",
            "activated_at": datetime.utcnow().isoformat(),
            "ip": request.remote_addr,
        })
        _save_subscribers(data)
        logger.info(f"PayPal subscription activated: {subscription_id}")

    return jsonify({"status": "ok", "subscription_id": subscription_id})


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
