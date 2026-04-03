"""Anesthesia & sedation protocols API Blueprint."""

import logging

from flask import Blueprint, jsonify, request

from api.anesthesia_protocols import (
    ANESTHESIA_CATEGORIES,
    ANESTHESIA_PROTOCOLS,
    ASA_CLASSIFICATION,
    RISK_LEVELS,
    get_all_species_ids,
    get_protocols_for_species,
    search_protocols,
)

logger = logging.getLogger(__name__)

anesthesia_bp = Blueprint("anesthesia", __name__)


@anesthesia_bp.route("/api/anesthesia/protocols", methods=["GET"])
def api_anesthesia_protocols():
    """Return anesthesia protocols, optionally filtered by species/category/query."""
    species = request.args.get("species", "")
    category = request.args.get("category", "")
    query = request.args.get("search", "")

    if species:
        data = get_protocols_for_species(species)
        if not data:
            return jsonify({"error": "Species not found", "species": species}), 404
        # Apply category/query filter
        protocols = data.get("protocols", [])
        if category:
            protocols = [p for p in protocols if p.get("category") == category]
        if query:
            q = query.lower()
            filtered = []
            for p in protocols:
                searchable = " ".join([
                    p.get("name", {}).get("ja", ""),
                    p.get("name", {}).get("en", ""),
                    p.get("notes_ja", ""),
                    p.get("notes", ""),
                ] + [
                    d.get("name", "") + " " + d.get("name_ja", "")
                    for d in p.get("drugs", [])
                ]).lower()
                if q in searchable:
                    filtered.append(p)
            protocols = filtered

        return jsonify({
            "species": species,
            "species_name": data.get("species_name", {}),
            "overview": data.get("overview", {}),
            "fasting": data.get("fasting", {}),
            "protocols": protocols,
            "breed_considerations": data.get("breed_considerations", []),
            "references": data.get("references", []),
            "categories": ANESTHESIA_CATEGORIES,
            "risk_levels": RISK_LEVELS,
        })

    # No species specified — return summary for all species
    results = search_protocols(query=query, category=category)
    return jsonify({
        "results": results,
        "total": len(results),
        "categories": ANESTHESIA_CATEGORIES,
        "risk_levels": RISK_LEVELS,
    })


@anesthesia_bp.route("/api/anesthesia/species", methods=["GET"])
def api_anesthesia_species():
    """Return list of species with available anesthesia protocols."""
    species_list = []
    for sp_id in get_all_species_ids():
        sp_data = ANESTHESIA_PROTOCOLS.get(sp_id, {})
        species_list.append({
            "id": sp_id,
            "name": sp_data.get("species_name", {}),
            "protocol_count": len(sp_data.get("protocols", [])),
        })
    return jsonify({"species": species_list, "total": len(species_list)})


@anesthesia_bp.route("/api/anesthesia/categories", methods=["GET"])
def api_anesthesia_categories():
    """Return list of anesthesia categories."""
    return jsonify({
        "categories": ANESTHESIA_CATEGORIES,
        "risk_levels": RISK_LEVELS,
        "asa_classification": ASA_CLASSIFICATION,
    })
