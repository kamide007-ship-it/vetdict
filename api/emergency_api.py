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

# ---------------------------------------------------------------------------
# key_drugs → 薬品辞書リンクの解決（一度だけ、インプレース）
# 救急プロトコルの主要薬品リストは素のテキストで、最も時間が切迫する画面で
# 用量詳細（辞書エントリ）への導線が無かった。各行を find_drugs_in_text で
# 辞書に解決し、解決できた行にのみ link_name（辞書の正準英語名）を付与する。
# フロントは link_name がある行だけをクリック可能にする（誤着地ゼロ設計）。
# ---------------------------------------------------------------------------
_key_drug_links_resolved = False


def _resolve_key_drug_links() -> None:
    global _key_drug_links_resolved
    if _key_drug_links_resolved:
        return
    try:
        from api.drug_dictionary import find_drugs_in_text
    except ImportError:  # pragma: no cover — formulary always importable in app
        _key_drug_links_resolved = True
        return
    import re

    def _toks(s: str) -> set:
        return {t for t in re.split(r"[^a-z0-9]+", (s or "").lower()) if len(t) >= 3}

    for p in EMERGENCY_PROTOCOLS:
        for d in p.get("key_drugs", []):
            if "link_name" in d:
                continue
            en = d.get("name", "")
            ja = d.get("name_ja", "")
            hits = find_drugs_in_text(f"{en} {ja}")
            if not hits:
                continue
            # 複数ヒット時は英語名トークンの重なりが最大のエントリを選ぶ
            # （"Ampicillin/sulbactam" が素の ampicillin ではなく
            #  ampicillin_sulbactam に着地するように）
            qt = _toks(en)
            best = max(hits, key=lambda h: len(qt & _toks(h.get("name", ""))))
            d["link_name"] = best.get("name", "")
    _key_drug_links_resolved = True


@emergency_bp.route("/api/emergency/protocols", methods=["GET"])
def api_list_emergency_protocols():
    """緊急プロトコル一覧。クエリ: species, category, search"""
    _resolve_key_drug_links()
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
    _resolve_key_drug_links()
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
