"""Unified data access layer for disease and symptom data from SQLite.

Provides cached, read-optimised access to the diseases and symptoms tables.
This module is the single entry point for API endpoints that need to read
disease/symptom data, replacing direct Python module imports for data
retrieval (symptom analysis still uses Python modules for performance).

Usage::

    from api.disease_store import (
        get_species_stats,
        get_symptoms_for_species,
        list_diseases,
        get_disease_detail,
        search_diseases,
    )
"""

from __future__ import annotations

import json
import logging
from functools import lru_cache
from typing import Any

from api.database import get_connection

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Species metadata (labels)
# ---------------------------------------------------------------------------

SPECIES_META: dict[str, tuple[str, str]] = {
    "dog": ("犬", "Dog"),
    "cat": ("猫", "Cat"),
    "horse": ("馬", "Horse"),
    "rabbit": ("うさぎ", "Rabbit"),
    "hamster": ("ハムスター", "Hamster"),
    "guinea_pig": ("モルモット", "Guinea Pig"),
    "chinchilla": ("チンチラ", "Chinchilla"),
    "ferret": ("フェレット", "Ferret"),
    "hedgehog": ("ハリネズミ", "Hedgehog"),
    "sugar_glider": ("フクロモモンガ", "Sugar Glider"),
    "degu": ("デグー", "Degu"),
    "bird": ("鳥", "Bird"),
    "parakeet": ("インコ", "Parakeet"),
    "parrot": ("オウム", "Parrot"),
    "reptile": ("爬虫類", "Reptile"),
    "tortoise": ("リクガメ", "Tortoise"),
    "snake": ("ヘビ", "Snake"),
    "lizard": ("トカゲ", "Lizard"),
    "amphibian": ("両生類", "Amphibian"),
    "exotic_other": ("その他エキゾチック", "Exotic Other"),
}


# ---------------------------------------------------------------------------
# Auto-initialise database on first access
# ---------------------------------------------------------------------------

_db_ready = False


def _ensure_db() -> None:
    """Create schema and run migration if the diseases table is empty."""
    global _db_ready
    if _db_ready:
        return
    from api.database import init_db
    init_db()
    with get_connection() as conn:
        try:
            count = conn.execute("SELECT COUNT(*) FROM diseases").fetchone()[0]
        except Exception:
            count = 0
    if count == 0:
        logger.info("diseases table is empty — running auto-migration")
        try:
            from scripts.migrate_to_sqlite import main as run_migration
            run_migration()
        except Exception:
            logger.exception("Auto-migration failed")
    _db_ready = True


# ---------------------------------------------------------------------------
# Cache helpers
# ---------------------------------------------------------------------------

_cache_version = 0


def invalidate_cache() -> None:
    """Clear all cached data (call after writes to the database)."""
    global _cache_version
    _cache_version += 1
    get_species_stats.cache_clear()
    get_urgency_stats.cache_clear()
    _get_symptoms_for_species_cached.cache_clear()


# ---------------------------------------------------------------------------
# Species statistics
# ---------------------------------------------------------------------------

@lru_cache(maxsize=1)
def _fallback_disease_counts() -> dict[str, int]:
    """Count diseases per species from Python modules and JSON as fallback."""
    counts: dict[str, int] = {}

    # Map species id -> module info
    _MODULE_MAP = {
        "dog": ("api.symptom_checker", "_DISEASE_DB"),
        "horse": ("api.species.equine_diseases", "DISEASE_DATABASE"),
        "cat": ("api.species.cat_diseases", "DISEASES"),
        "rabbit": ("api.species.rabbit_diseases", "DISEASES"),
        "hamster": ("api.species.hamster_diseases", "DISEASES"),
        "guinea_pig": ("api.species.guinea_pig_diseases", "DISEASES"),
        "chinchilla": ("api.species.chinchilla_diseases", "DISEASES"),
        "ferret": ("api.species.ferret_diseases", "DISEASES"),
        "hedgehog": ("api.species.hedgehog_diseases", "DISEASES"),
        "sugar_glider": ("api.species.sugar_glider_diseases", "DISEASES"),
        "degu": ("api.species.degu_diseases", "DISEASES"),
        "bird": ("api.species.bird_diseases", "DISEASES"),
        "parakeet": ("api.species.parakeet_diseases", "DISEASES"),
        "parrot": ("api.species.parrot_diseases", "DISEASES"),
        "reptile": ("api.species.reptile_diseases", "DISEASES"),
        "tortoise": ("api.species.tortoise_diseases", "DISEASES"),
        "snake": ("api.species.snake_diseases", "DISEASES"),
        "lizard": ("api.species.lizard_diseases", "DISEASES"),
        "amphibian": ("api.species.amphibian_diseases", "DISEASES"),
        "exotic_other": ("api.species.exotic_other_diseases", "DISEASES"),
    }

    import importlib
    for sp_id, (mod_path, attr) in _MODULE_MAP.items():
        try:
            mod = importlib.import_module(mod_path)
            data = getattr(mod, attr, [])
            counts[sp_id] = len(data) if data else 0
        except Exception:
            pass

    # JSON fallback for any species still missing
    if any(counts.get(sp, 0) == 0 for sp in SPECIES_META):
        try:
            import json as _json
            from pathlib import Path as _Path
            data_file = _Path(__file__).parent.parent / "diseases_all_species.json"
            if data_file.exists():
                _name_to_id = {v[1]: k for k, v in SPECIES_META.items()}
                with open(data_file, "r", encoding="utf-8") as f:
                    for entry in _json.load(f):
                        sp_name = entry.get("species", "")
                        sp_id = _name_to_id.get(sp_name)
                        if sp_id and counts.get(sp_id, 0) == 0:
                            counts[sp_id] = counts.get(sp_id, 0) + 1
        except Exception:
            pass

    return counts


def _fallback_drug_counts() -> tuple[dict[str, int], int]:
    """Count drugs per species from Python module as fallback."""
    per_species: dict[str, int] = {}
    total = 0
    try:
        from api.drug_dictionary import DRUGS
        total = len(DRUGS)
        for d in DRUGS:
            for sp in d.get("species_info") or {}:
                per_species[sp] = per_species.get(sp, 0) + 1
    except Exception:
        pass
    return per_species, total


@lru_cache(maxsize=1)
def get_species_stats() -> dict[str, Any]:
    """Return per-species disease/drug counts from SQLite.

    Falls back to Python modules / JSON if the database is empty.

    Returns a dict with keys: ``species`` (list), ``total_diseases``,
    ``total_drugs``, ``total_species``.
    """
    disease_counts: dict[str, int] = {}
    drug_counts: dict[str, int] = {}
    total_drugs = 0

    try:
        _ensure_db()
        with get_connection() as conn:
            for row in conn.execute(
                "SELECT species, COUNT(*) AS cnt FROM diseases GROUP BY species ORDER BY species"
            ).fetchall():
                disease_counts[row["species"]] = row["cnt"]

            for row in conn.execute(
                "SELECT species, COUNT(*) AS cnt FROM drug_species_info GROUP BY species"
            ).fetchall():
                drug_counts[row["species"]] = row["cnt"]

            total_drugs = conn.execute("SELECT COUNT(*) FROM drugs").fetchone()[0]
    except Exception:
        logger.warning("SQLite query failed — will use fallback", exc_info=True)

    # Fallback: if SQLite has no disease data, use modules/JSON
    if sum(disease_counts.values()) == 0:
        logger.info("No disease data from SQLite — using module/JSON fallback")
        disease_counts = _fallback_disease_counts()

    if total_drugs == 0:
        drug_counts, total_drugs = _fallback_drug_counts()

    stats = []
    for sp_id, (name_ja, name_en) in SPECIES_META.items():
        stats.append({
            "id": sp_id,
            "name": name_ja,
            "nameEn": name_en,
            "diseases": disease_counts.get(sp_id, 0),
            "drugs": drug_counts.get(sp_id, 0),
        })

    return {
        "species": stats,
        "total_diseases": sum(s["diseases"] for s in stats),
        "total_drugs": total_drugs,
        "total_species": len(stats),
    }


@lru_cache(maxsize=1)
def get_urgency_stats() -> dict[str, Any]:
    """Return disease count by urgency level from SQLite.

    Returns a dict with keys: ``urgency_levels`` (list), ``total_diseases``.
    """
    with get_connection() as conn:
        urgency_rows = conn.execute(
            "SELECT urgency, COUNT(*) AS cnt FROM diseases "
            "WHERE urgency IS NOT NULL GROUP BY urgency ORDER BY urgency"
        ).fetchall()

    urgency_stats = []
    total_diseases = 0
    for row in urgency_rows:
        count = row["cnt"]
        urgency_stats.append({
            "urgency": row["urgency"],
            "count": count,
        })
        total_diseases += count

    return {
        "urgency_levels": urgency_stats,
        "total_diseases": total_diseases,
    }


def get_urgency_by_species(species: str) -> dict[str, Any]:
    """Return urgency-level breakdown for a specific species.

    Returns a dict with keys: ``species``, ``urgency_levels`` (list),
    ``total_diseases``.
    """
    with get_connection() as conn:
        urgency_rows = conn.execute(
            "SELECT urgency, COUNT(*) AS cnt FROM diseases "
            "WHERE species = ? AND urgency IS NOT NULL "
            "GROUP BY urgency ORDER BY urgency",
            (species,),
        ).fetchall()

    urgency_stats = []
    total_diseases = 0
    for row in urgency_rows:
        count = row["cnt"]
        urgency_stats.append({
            "urgency": row["urgency"],
            "count": count,
        })
        total_diseases += count

    return {
        "species": species,
        "urgency_levels": urgency_stats,
        "total_diseases": total_diseases,
    }


# ---------------------------------------------------------------------------
# Symptoms
# ---------------------------------------------------------------------------

def _load_horse_category_map() -> dict[str, str]:
    """Build symptom_id → category mapping from equine HEALTH_CHECK_ITEMS."""
    try:
        from api.species.equine_diseases import HEALTH_CHECK_ITEMS
        mapping: dict[str, str] = {}
        for category, items in HEALTH_CHECK_ITEMS.items():
            for symptom_id, _name_ja, _name_en in items:
                mapping[symptom_id] = category
        return mapping
    except ImportError:
        return {}


@lru_cache(maxsize=32)
def _get_symptoms_for_species_cached(species: str, _version: int = 0) -> list[dict]:
    """Cached implementation; ``_version`` key busts cache on invalidation."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, name_en, name_ja, species, clinical_weight FROM symptoms WHERE species = ? ORDER BY id",
            (species,),
        ).fetchall()
        # Also gather unique symptom IDs from disease records for this species
        disease_syms_raw = conn.execute(
            "SELECT symptoms FROM diseases WHERE species = ? AND symptoms IS NOT NULL",
            (species,),
        ).fetchall()

    # Horse has category-aware symptoms from HEALTH_CHECK_ITEMS
    horse_categories = _load_horse_category_map() if species == "horse" else {}

    # Symptom records from symptoms table
    symptom_map: dict[str, dict] = {}
    for r in rows:
        raw_id = r["id"].removeprefix(f"{species}_")
        symptom_map[raw_id] = {
            "id": raw_id,
            "name_ja": r["name_ja"],
            "name_en": r["name_en"],
            "category": horse_categories.get(raw_id, "other"),
        }

    # Ensure every symptom referenced in diseases is present
    for row in disease_syms_raw:
        try:
            sym_list = json.loads(row["symptoms"])
        except (json.JSONDecodeError, TypeError):
            continue
        for sid in sym_list:
            if sid not in symptom_map:
                symptom_map[sid] = {
                    "id": sid,
                    "name_ja": sid,
                    "name_en": sid,
                    "category": horse_categories.get(sid, "other"),
                }

    return sorted(symptom_map.values(), key=lambda s: s["id"])


def get_symptoms_for_species(species: str) -> list[dict]:
    """Return symptom list for a species from SQLite."""
    return _get_symptoms_for_species_cached(species, _cache_version)


# ---------------------------------------------------------------------------
# Disease listing & detail
# ---------------------------------------------------------------------------

def _parse_json_field(value: str | None) -> list | None:
    """Parse a JSON-encoded field, returning None on failure."""
    if not value:
        return None
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return None


def _row_to_disease_summary(row) -> dict:
    """Convert a SQLite row to a compact disease summary dict."""
    return {
        "id": row["id"],
        "species": row["species"],
        "name": row["name"],
        "name_ja": row["name_ja"],
        "urgency": row["urgency"],
    }


def _row_to_disease_detail(row) -> dict:
    """Convert a SQLite row to a full disease detail dict."""
    d = dict(row)
    # Parse JSON fields back to lists
    for field in ("symptoms", "recommended_tests", "onset_pattern", "age_predisposition"):
        d[field] = _parse_json_field(d.get(field))
    return d


_LIST_DISEASES_BASE = "SELECT id, species, name, name_ja, urgency FROM diseases"
_COUNT_DISEASES_BASE = "SELECT COUNT(*) FROM diseases"


def list_diseases(
    species: str | None = None,
    limit: int = 200,
    offset: int = 0,
    search: str | None = None,
) -> dict[str, Any]:
    """List diseases with optional species filter and comprehensive search.

    Search matches against name, description, treatment, prevention, and
    pathophysiology fields in both English and Japanese.

    Returns ``{"diseases": [...], "total": N, "limit": L, "offset": O}``.
    """
    search_clause = (
        "(name LIKE ? OR name_ja LIKE ? OR "
        "description LIKE ? OR description_ja LIKE ? OR "
        "treatment LIKE ? OR treatment_ja LIKE ? OR "
        "prevention LIKE ? OR prevention_ja LIKE ? OR "
        "pathophysiology LIKE ? OR pathophysiology_ja LIKE ?)"
    )

    with get_connection() as conn:
        conditions: list[str] = []
        params: list = []

        if species:
            conditions.append("species = ?")
            params.append(species)
        if search:
            like_pattern = "%" + search + "%"
            conditions.append(search_clause)
            params.extend([like_pattern] * 10)

        where = " WHERE " + " AND ".join(conditions) if conditions else ""

        total = conn.execute(_COUNT_DISEASES_BASE + where, params).fetchone()[0]

        rows = conn.execute(
            _LIST_DISEASES_BASE + where + " ORDER BY species, name LIMIT ? OFFSET ?",
            [*params, limit, offset],
        ).fetchall()

    return {
        "diseases": [_row_to_disease_summary(r) for r in rows],
        "total": total,
        "limit": limit,
        "offset": offset,
    }


def get_disease_detail(disease_id: str) -> dict | None:
    """Return full disease detail by ID, or None if not found."""
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM diseases WHERE id = ?", (disease_id,)).fetchone()
    if not row:
        return None
    return _row_to_disease_detail(row)


def search_diseases(query: str, species: str | None = None, limit: int = 50) -> list[dict]:
    """Search diseases by name, description, treatment, and other fields.

    Searches both English and Japanese fields. Returns results ordered by
    relevance (name match prioritized) then by species and name.
    """
    like_pattern = "%" + query + "%"
    search_clause = (
        "(name LIKE ? OR name_ja LIKE ? OR "
        "description LIKE ? OR description_ja LIKE ? OR "
        "treatment LIKE ? OR treatment_ja LIKE ? OR "
        "prevention LIKE ? OR prevention_ja LIKE ? OR "
        "pathophysiology LIKE ? OR pathophysiology_ja LIKE ?)"
    )

    with get_connection() as conn:
        # Prepare search parameters (one for each field)
        search_params = [like_pattern] * 10

        if species:
            query_str = (
                "SELECT id, species, name, name_ja, urgency FROM diseases "
                "WHERE " + search_clause + " AND species = ? ORDER BY name LIMIT ?"
            )
            rows = conn.execute(
                query_str,
                [*search_params, species, limit],
            ).fetchall()
        else:
            query_str = (
                "SELECT id, species, name, name_ja, urgency FROM diseases "
                "WHERE " + search_clause + " ORDER BY species, name LIMIT ?"
            )
            rows = conn.execute(
                query_str,
                [*search_params, limit],
            ).fetchall()
    return [_row_to_disease_summary(r) for r in rows]


def get_diseases_by_symptom(
    symptom_id: str, species: str | None = None, limit: int = 50
) -> list[dict]:
    """Return diseases that have a given symptom.

    Searches for diseases with this symptom in their symptoms JSON field.
    Optionally filters by species.
    """
    with get_connection() as conn:
        if species:
            rows = conn.execute(
                "SELECT id, species, name, name_ja, urgency, symptoms FROM diseases "
                "WHERE species = ? AND symptoms IS NOT NULL "
                "ORDER BY name",
                (species,),
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT id, species, name, name_ja, urgency, symptoms FROM diseases "
                "WHERE symptoms IS NOT NULL "
                "ORDER BY species, name",
            ).fetchall()

    # Filter results by checking JSON array membership
    result = []
    for row in rows:
        symptoms_json = row["symptoms"]
        if symptoms_json:
            try:
                symptoms = json.loads(symptoms_json)
                if symptom_id in symptoms:
                    result.append(_row_to_disease_summary(row))
                    if len(result) >= limit:
                        break
            except (json.JSONDecodeError, TypeError):
                continue
    return result
