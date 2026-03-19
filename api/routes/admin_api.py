"""Admin API routes for managing diseases, drugs, and symptoms via SQLite."""


from flask import Blueprint, jsonify, request

from api.database import (
    count_diseases,
    delete_disease,
    get_all_drugs,
    get_connection,
    get_disease_by_id,
    get_diseases_by_species,
    get_drug_by_id,
    upsert_disease,
    upsert_drug,
)
from api.disease_store import invalidate_cache

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


# ---------------------------------------------------------------------------
# Diseases
# ---------------------------------------------------------------------------

@admin_bp.route("/diseases", methods=["GET"])
def list_diseases():
    """List diseases, optionally filtered by species."""
    species = request.args.get("species")
    with get_connection() as conn:
        if species:
            rows = get_diseases_by_species(conn, species)
        else:
            rows = [
                dict(r)
                for r in conn.execute(
                    "SELECT id, species, name, name_ja, urgency FROM diseases ORDER BY species, name LIMIT 1000"
                ).fetchall()
            ]
    return jsonify({"success": True, "count": len(rows), "diseases": rows})


@admin_bp.route("/diseases/<disease_id>", methods=["GET"])
def get_disease(disease_id: str):
    """Get a single disease by ID."""
    with get_connection() as conn:
        disease = get_disease_by_id(conn, disease_id)
    if not disease:
        return jsonify({"success": False, "error": "Disease not found"}), 404
    return jsonify({"success": True, "disease": disease})


@admin_bp.route("/diseases", methods=["POST"])
def create_disease():
    """Create or update a disease."""
    data = request.get_json(force=True)
    if not data or not data.get("id") or not data.get("species"):
        return jsonify({"success": False, "error": "id and species are required"}), 400
    with get_connection() as conn:
        upsert_disease(conn, data)
    invalidate_cache()
    return jsonify({"success": True, "id": data["id"]}), 201


@admin_bp.route("/diseases/<disease_id>", methods=["PUT"])
def update_disease(disease_id: str):
    """Update an existing disease."""
    data = request.get_json(force=True)
    if not data:
        return jsonify({"success": False, "error": "Request body required"}), 400
    data["id"] = disease_id
    with get_connection() as conn:
        existing = get_disease_by_id(conn, disease_id)
        if not existing:
            return jsonify({"success": False, "error": "Disease not found"}), 404
        # Merge: keep existing fields not provided in update
        merged = {**existing, **{k: v for k, v in data.items() if v is not None}}
        upsert_disease(conn, merged)
    invalidate_cache()
    return jsonify({"success": True, "id": disease_id})


@admin_bp.route("/diseases/<disease_id>", methods=["DELETE"])
def remove_disease(disease_id: str):
    """Delete a disease by ID."""
    with get_connection() as conn:
        deleted = delete_disease(conn, disease_id)
    if not deleted:
        return jsonify({"success": False, "error": "Disease not found"}), 404
    invalidate_cache()
    return jsonify({"success": True, "deleted": disease_id})


@admin_bp.route("/diseases/stats", methods=["GET"])
def disease_stats():
    """Return disease count statistics."""
    with get_connection() as conn:
        stats = count_diseases(conn)
    return jsonify({"success": True, **stats})


# ---------------------------------------------------------------------------
# Drugs
# ---------------------------------------------------------------------------

@admin_bp.route("/drugs", methods=["GET"])
def list_drugs():
    """List all drugs."""
    with get_connection() as conn:
        rows = get_all_drugs(conn)
    return jsonify({"success": True, "count": len(rows), "drugs": rows})


@admin_bp.route("/drugs/<drug_id>", methods=["GET"])
def get_drug(drug_id: str):
    """Get a single drug by ID with species info."""
    with get_connection() as conn:
        drug = get_drug_by_id(conn, drug_id)
    if not drug:
        return jsonify({"success": False, "error": "Drug not found"}), 404
    return jsonify({"success": True, "drug": drug})


@admin_bp.route("/drugs", methods=["POST"])
def create_drug():
    """Create or update a drug."""
    data = request.get_json(force=True)
    if not data or not data.get("id"):
        return jsonify({"success": False, "error": "id is required"}), 400
    with get_connection() as conn:
        upsert_drug(conn, data)
    return jsonify({"success": True, "id": data["id"]}), 201


# ---------------------------------------------------------------------------
# Bulk import
# ---------------------------------------------------------------------------

@admin_bp.route("/import", methods=["POST"])
def bulk_import():
    """Bulk import diseases from JSON payload."""
    data = request.get_json(force=True)
    diseases = data.get("diseases", [])
    if not diseases:
        return jsonify({"success": False, "error": "No diseases provided"}), 400
    with get_connection() as conn:
        for d in diseases:
            upsert_disease(conn, d)
    invalidate_cache()
    return jsonify({"success": True, "imported": len(diseases)}), 201
