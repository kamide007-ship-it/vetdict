"""Public read-only API routes for browsing diseases from SQLite.

These endpoints provide unified access to the enriched disease database.
The ``/api/diseases`` and ``/api/diseases/<id>`` endpoints are new; the
existing ``/api/species-stats`` and ``/api/species/<sp>/symptoms`` routes
are updated in ``vetdict_api.py`` to use the same SQLite-backed store.
"""

from flask import Blueprint, jsonify, request

from api.disease_store import (
    get_disease_detail,
    list_diseases,
    search_diseases,
)

diseases_bp = Blueprint("diseases", __name__, url_prefix="/api")


@diseases_bp.route("/diseases", methods=["GET"])
def api_list_diseases():
    """List diseases with optional filtering.

    Query params:
        species: filter by species key (e.g. "cat", "dog")
        q: search by name (English or Japanese)
        limit: max results (default 200, max 1000)
        offset: pagination offset (default 0)
    """
    species = request.args.get("species")
    query = request.args.get("q")
    limit = min(int(request.args.get("limit", 200)), 1000)
    offset = max(int(request.args.get("offset", 0)), 0)

    if query:
        results = search_diseases(query, species=species, limit=limit)
        return jsonify({"success": True, "diseases": results, "total": len(results)})

    result = list_diseases(species=species, limit=limit, offset=offset)
    return jsonify({"success": True, **result})


@diseases_bp.route("/diseases/<disease_id>", methods=["GET"])
def api_get_disease(disease_id: str):
    """Get full disease detail by ID.

    Returns all fields including treatment, prevention, prognosis,
    pathophysiology, causes, and recommended tests.
    """
    disease = get_disease_detail(disease_id)
    if not disease:
        return jsonify({"success": False, "error": "Disease not found"}), 404
    return jsonify({"success": True, "disease": disease})
