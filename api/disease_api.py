#!/usr/bin/env python3
"""
Optimized disease API endpoints using SQLite backend

New endpoints provide fast queries with caching:
- GET /api/diseases/{disease_id}           — Single disease detail
- GET /api/diseases/search?q=<query>       — Full-text search
- GET /api/diseases/species/<species>      — Diseases by species
- GET /api/diseases/by-urgency/<urgency>   — Diseases by urgency
- GET /api/diseases/stats                  — Database statistics
"""

import logging

from flask import Blueprint, abort, jsonify, request

from api.caching import CACHE_TIMEOUTS, cache
from api.disease_database import DiseaseDatabase
from api.disease_search import DiseaseFullTextSearch

logger = logging.getLogger(__name__)

# Create blueprint
diseases_bp = Blueprint("diseases", __name__, url_prefix="/api/diseases")

# Initialize data access layers
db = DiseaseDatabase()
fts = DiseaseFullTextSearch()


def _parse_limit(default: int, hard_max: int) -> int:
    """Parse the `limit` query arg, returning a clamped int.

    Aborts with 400 on non-integer input rather than letting `int()` raise a 500.
    """
    raw = request.args.get("limit", default)
    try:
        value = int(raw)
    except (TypeError, ValueError):
        abort(400, description="'limit' must be an integer")
    return max(1, min(value, hard_max))


# --- Disease Detail Endpoints ---


@diseases_bp.route("/<disease_id>", methods=["GET"])
@cache.cached(timeout=CACHE_TIMEOUTS["disease_detail"])
def get_disease_detail(disease_id: str):
    """
    Get detailed information for a single disease

    Response (200):
        {
            "id": "cat_0001",
            "name_en": "Feline Leukemia Virus (FeLV)",
            "name_ja": "猫白血病ウイルス感染症（FeLV）",
            "species": "Cat",
            "urgency": "high",
            "pathophysiology_en": "...",
            "pathophysiology_ja": "...",
            ...
        }

    Response (404):
        {"error": "Disease not found"}
    """
    disease = db.get_disease_by_id(disease_id)
    if not disease:
        abort(404, description="Disease not found")

    return jsonify(disease)


# --- Search Endpoints ---


@diseases_bp.route("/search", methods=["GET"])
@cache.cached(timeout=CACHE_TIMEOUTS["fts_search"], query_string=True)
def search_diseases():
    """
    Full-text search for diseases

    Query parameters:
        q (required): Search query (supports AND/OR operators)
        limit (optional): Max results (default: 20, max: 100)
        species (optional): Filter by species

    Examples:
        GET /api/diseases/search?q=fever
        GET /api/diseases/search?q=fever%20AND%20respiratory&species=Dog
        GET /api/diseases/search?q=white%20blood%20cell&limit=50

    Response (200):
        {
            "query": "fever",
            "results": [
                {"id": "...", "name_en": "...", "species": "...", ...},
                ...
            ],
            "count": 45,
            "limit": 20,
            "execution_time_ms": 2.34
        }

    Response (400):
        {"error": "Query parameter 'q' is required"}
    """
    import time

    query = request.args.get("q", "").strip()
    if not query:
        abort(400, description="Query parameter 'q' is required")

    limit = _parse_limit(20, 100)
    species = request.args.get("species")

    start_time = time.time()

    # Execute search
    if species:
        results = fts.search_with_species_filter(query, species, limit)
    else:
        results = fts.simple_search(query, limit)

    elapsed_ms = (time.time() - start_time) * 1000

    return jsonify(
        {
            "query": query,
            "species_filter": species,
            "results": results,
            "count": len(results),
            "limit": limit,
            "execution_time_ms": round(elapsed_ms, 2),
        }
    )


@diseases_bp.route("/by-name", methods=["GET"])
@cache.cached(timeout=CACHE_TIMEOUTS["search_results"], query_string=True)
def search_by_name():
    """
    Search for diseases by name (prefix match)

    Query parameters:
        name (required): Disease name (EN or JA)
        language (optional): 'en' (default) or 'ja'
        limit (optional): Max results (default: 20)

    Examples:
        GET /api/diseases/by-name?name=leukemia
        GET /api/diseases/by-name?name=白血病&language=ja
    """
    name = request.args.get("name", "").strip()
    if not name:
        abort(400, description="Query parameter 'name' is required")

    language = request.args.get("language", "en").lower()
    limit = _parse_limit(20, 100)

    if language == "ja":
        results = db.search_by_name_ja(name, limit)
    else:
        results = db.search_by_name_en(name, limit)

    return jsonify(
        {
            "name": name,
            "language": language,
            "results": results,
            "count": len(results),
        }
    )


# --- Filter Endpoints ---


@diseases_bp.route("/by-species/<species>", methods=["GET"])
@cache.cached(timeout=CACHE_TIMEOUTS["disease_list"], query_string=True)
def get_by_species(species: str):
    """
    Get all diseases for a specific species

    Response (200):
        {
            "species": "Cat",
            "results": [...],
            "count": 537
        }
    """
    limit = _parse_limit(100, 1000)
    results = db.search_by_species(species, limit)

    return jsonify(
        {
            "species": species,
            "results": results,
            "count": len(results),
        }
    )


@diseases_bp.route("/by-urgency/<urgency>", methods=["GET"])
@cache.cached(timeout=CACHE_TIMEOUTS["urgency_stats"], query_string=True)
def get_by_urgency(urgency: str):
    """
    Get all diseases by urgency level

    Valid urgencies: emergency, high, normal

    Response (200):
        {
            "urgency": "emergency",
            "results": [...],
            "count": 617
        }
    """
    limit = _parse_limit(100, 1000)
    results = db.search_by_urgency(urgency, limit)

    return jsonify(
        {
            "urgency": urgency,
            "results": results,
            "count": len(results),
        }
    )


@diseases_bp.route("/by-species-urgency", methods=["GET"])
@cache.cached(timeout=CACHE_TIMEOUTS["disease_list"], query_string=True)
def get_by_species_urgency():
    """
    Get diseases filtered by species AND urgency

    Query parameters:
        species (required): Species name
        urgency (required): urgency level

    Example:
        GET /api/diseases/by-species-urgency?species=Dog&urgency=emergency
    """
    species = request.args.get("species")
    urgency = request.args.get("urgency")

    if not species or not urgency:
        abort(400, description="Both 'species' and 'urgency' parameters required")

    limit = _parse_limit(100, 1000)
    results = db.search_by_species_and_urgency(species, urgency, limit)

    return jsonify(
        {
            "species": species,
            "urgency": urgency,
            "results": results,
            "count": len(results),
        }
    )


# --- Statistics Endpoints ---


@diseases_bp.route("/stats", methods=["GET"])
@cache.cached(timeout=CACHE_TIMEOUTS["species_stats"])
def get_stats():
    """
    Get database statistics

    Response (200):
        {
            "total_count": 6449,
            "by_species": {"Cat": 537, "Dog": 575, ...},
            "by_urgency": {"emergency": 617, "high": 2615, "normal": 3217}
        }
    """
    return jsonify(
        {
            "total_count": db.get_total_disease_count(),
            "by_species": db.get_species_stats(),
            "by_urgency": db.get_urgency_stats(),
        }
    )


@diseases_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint for monitoring"""
    try:
        count = db.get_total_disease_count()
        return jsonify(
            {
                "status": "healthy",
                "database": "SQLite",
                "disease_count": count,
            }
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        abort(503, description="Database connection failed")
