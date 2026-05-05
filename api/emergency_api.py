"""emergency_api.py - 緊急プロトコルAPI Blueprint"""

from __future__ import annotations

from flask import Blueprint, jsonify, request

from api.emergency_protocols import (
    EMERGENCY_PROTOCOLS,
    PROTOCOL_CATEGORIES,
    get_protocol,
    list_protocols,
)

emergency_bp = Blueprint("emergency", __name__)


@emergency_bp.route("/api/emergency/protocols", methods=["GET"])
def api_list_emergency_protocols():
    """緊急プロトコル一覧。クエリ: species, category, search"""
    species = request.args.get("species", "")
    category = request.args.get("category", "")
    search = request.args.get("search", "")
    protocols = list_protocols(species=species, category=category, search=search)
    return jsonify(
        {
            "protocols": protocols,
            "total": len(protocols),
            "categories": PROTOCOL_CATEGORIES,
        }
    )


@emergency_bp.route("/api/emergency/protocols/<protocol_id>", methods=["GET"])
def api_get_emergency_protocol(protocol_id: str):
    """単一プロトコル詳細"""
    p = get_protocol(protocol_id)
    if not p:
        return jsonify({"error": "Protocol not found"}), 404
    return jsonify({"protocol": p})


@emergency_bp.route("/api/emergency/categories", methods=["GET"])
def api_emergency_categories():
    """緊急プロトコルカテゴリ"""
    cats = []
    for cat_id, names in PROTOCOL_CATEGORIES.items():
        count = sum(1 for p in EMERGENCY_PROTOCOLS if p.get("category") == cat_id)
        cats.append({"id": cat_id, "name_ja": names["ja"], "name_en": names["en"], "count": count})
    cats.sort(key=lambda c: c["count"], reverse=True)
    return jsonify({"categories": cats, "total_protocols": len(EMERGENCY_PROTOCOLS)})
