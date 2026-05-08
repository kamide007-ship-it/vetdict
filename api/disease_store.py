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
import threading
from functools import lru_cache
from pathlib import Path
from typing import Any

from api.database import DB_PATH, get_connection

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Species metadata (labels)
# ---------------------------------------------------------------------------

SPECIES_META: dict[str, dict[str, str]] = {
    "dog": {
        "name_ja": "犬",
        "name_en": "Dog",
        "desc_ja": "最も一般的なペットの疾患辞典",
        "desc_en": "Comprehensive disease dictionary for dogs",
    },
    "cat": {
        "name_ja": "猫",
        "name_en": "Cat",
        "desc_ja": "猫特有の疾患と症状",
        "desc_en": "Feline-specific diseases and symptoms",
    },
    "horse": {
        "name_ja": "馬",
        "name_en": "Horse",
        "desc_ja": "馬の疾患・運動器障害を網羅",
        "desc_en": "Equine diseases and musculoskeletal disorders",
    },
    "rabbit": {
        "name_ja": "うさぎ",
        "name_en": "Rabbit",
        "desc_ja": "うさぎに多い消化器・歯科疾患",
        "desc_en": "Common rabbit digestive and dental diseases",
    },
    "hamster": {
        "name_ja": "ハムスター",
        "name_en": "Hamster",
        "desc_ja": "ハムスターの腫瘍・皮膚疾患など",
        "desc_en": "Hamster tumors, skin conditions, and more",
    },
    "guinea_pig": {
        "name_ja": "モルモット",
        "name_en": "Guinea Pig",
        "desc_ja": "ビタミンC欠乏症や呼吸器疾患",
        "desc_en": "Vitamin C deficiency and respiratory diseases",
    },
    "chinchilla": {
        "name_ja": "チンチラ",
        "name_en": "Chinchilla",
        "desc_ja": "チンチラの歯科・消化器疾患",
        "desc_en": "Chinchilla dental and digestive conditions",
    },
    "ferret": {
        "name_ja": "フェレット",
        "name_en": "Ferret",
        "desc_ja": "フェレットの内分泌・腫瘍疾患",
        "desc_en": "Ferret endocrine and neoplastic diseases",
    },
    "hedgehog": {
        "name_ja": "ハリネズミ",
        "name_en": "Hedgehog",
        "desc_ja": "ハリネズミの皮膚・神経疾患",
        "desc_en": "Hedgehog skin and neurological conditions",
    },
    "sugar_glider": {
        "name_ja": "フクロモモンガ",
        "name_en": "Sugar Glider",
        "desc_ja": "栄養性疾患やストレス関連症状",
        "desc_en": "Nutritional diseases and stress-related conditions",
    },
    "degu": {
        "name_ja": "デグー",
        "name_en": "Degu",
        "desc_ja": "デグーの糖尿病・歯科疾患",
        "desc_en": "Degu diabetes and dental diseases",
    },
    "bird": {
        "name_ja": "鳥",
        "name_en": "Bird",
        "desc_ja": "鳥類全般の感染症・栄養疾患",
        "desc_en": "Avian infections and nutritional diseases",
    },
    "parakeet": {
        "name_ja": "インコ",
        "name_en": "Parakeet",
        "desc_ja": "インコの呼吸器・羽毛疾患",
        "desc_en": "Parakeet respiratory and feather disorders",
    },
    "parrot": {
        "name_ja": "オウム",
        "name_en": "Parrot",
        "desc_ja": "オウム病やPBFDなど大型鳥の疾患",
        "desc_en": "Psittacosis, PBFD, and large parrot diseases",
    },
    "reptile": {
        "name_ja": "爬虫類",
        "name_en": "Reptile",
        "desc_ja": "爬虫類全般の代謝性骨疾患など",
        "desc_en": "Metabolic bone disease and general reptile conditions",
    },
    "tortoise": {
        "name_ja": "リクガメ",
        "name_en": "Tortoise",
        "desc_ja": "リクガメの甲羅・呼吸器疾患",
        "desc_en": "Tortoise shell and respiratory disorders",
    },
    "snake": {
        "name_ja": "ヘビ",
        "name_en": "Snake",
        "desc_ja": "ヘビの呼吸器感染症・脱皮異常",
        "desc_en": "Snake respiratory infections and dysecdysis",
    },
    "lizard": {
        "name_ja": "トカゲ",
        "name_en": "Lizard",
        "desc_ja": "トカゲの寄生虫症・代謝疾患",
        "desc_en": "Lizard parasitic and metabolic diseases",
    },
    "amphibian": {
        "name_ja": "両生類",
        "name_en": "Amphibian",
        "desc_ja": "カエル・イモリのツボカビ症など",
        "desc_en": "Chytrid fungus and amphibian diseases",
    },
    "fish": {
        "name_ja": "魚",
        "name_en": "Fish",
        "desc_ja": "白点病・尾ぐされ病など観賞魚の疾患",
        "desc_en": "Ich, fin rot, dropsy and aquarium fish diseases",
    },
    "exotic_other": {
        "name_ja": "その他エキゾチック",
        "name_en": "Exotic Other",
        "desc_ja": "その他のエキゾチックアニマルの疾患",
        "desc_en": "Diseases of other exotic animals",
    },
}


# ---------------------------------------------------------------------------
# Auto-initialise database on first access
# ---------------------------------------------------------------------------

_db_ready = False
_db_init_lock = threading.Lock()


def _ensure_db() -> None:
    """Create schema and run migration if the diseases table is empty or drugs are stale."""
    global _db_ready
    if _db_ready:
        return
    with _db_init_lock:
        if _db_ready:
            return
        from api.database import init_db

        init_db()
        with get_connection() as conn:
            try:
                count = conn.execute("SELECT COUNT(*) FROM diseases").fetchone()[0]
            except Exception:
                logger.debug("Could not count diseases in SQLite", exc_info=True)
                count = 0
        if count == 0:
            logger.info(
                "diseases table is empty — skipping full migration (OOM risk on 512MB); using Python module fallback"
            )
        else:
            try:
                with get_connection() as conn:
                    db_drug_count = conn.execute("SELECT COUNT(*) FROM drugs").fetchone()[0]
                from api.drug_dictionary import DRUGS

                if len(DRUGS) > db_drug_count:
                    logger.info(
                        "Drug count stale (SQLite=%d, Python=%d) — migrating drugs only",
                        db_drug_count,
                        len(DRUGS),
                    )
                    from api.database import upsert_drug

                    with get_connection() as conn:
                        for drug in DRUGS:
                            upsert_drug(conn, drug)
                        conn.commit()
                    logger.info("Drug-only migration complete (%d drugs)", len(DRUGS))
            except Exception:
                logger.debug("Could not check/fix drug staleness", exc_info=True)
        _db_ready = True


# ---------------------------------------------------------------------------
# Cache helpers
# ---------------------------------------------------------------------------

_cache_version = 0
_cache_lock = threading.Lock()


def invalidate_cache() -> None:
    """Clear all cached data (call after writes to the database)."""
    global _cache_version
    with _cache_lock:
        _cache_version += 1
        get_species_stats.cache_clear()
        get_urgency_stats.cache_clear()
        _get_symptoms_for_species_cached.cache_clear()
        _symptom_category_cache.clear()  # Clear category cache


# ---------------------------------------------------------------------------
# Species statistics
# ---------------------------------------------------------------------------


@lru_cache(maxsize=1)
def _fallback_disease_counts() -> dict[str, int]:
    """Count diseases per species without loading all modules into memory.

    Primary: read species_counts.json (written by migrate_to_sqlite.py at
    build time, <1 KB).  Fallback: load species modules one at a time via
    subprocess to avoid 550 MB peak RSS that would OOM on 512 MB hosts.
    """
    # Fast path: read pre-computed counts from build artifact
    counts_path = Path(DB_PATH).parent / "species_counts.json"
    if counts_path.exists():
        try:
            import json as _json

            data = _json.loads(counts_path.read_text())
            counts = {k: int(v) for k, v in data.get("disease_counts", {}).items()}
            if sum(counts.values()) > 0:
                logger.info("Loaded disease counts from %s (%d species)", counts_path, len(counts))
                return counts
        except Exception:
            logger.debug("Could not read species_counts.json", exc_info=True)

    # Slow path: count via subprocess to avoid OOM (each species ~50 MB peak)
    import json as _json
    import subprocess
    import sys

    script = (
        "import json,sys,importlib;sys.path.insert(0,'.');"
        "M={"
        "'dog':('api.species.dog_diseases','DISEASES'),"
        "'horse':('api.species.equine_diseases','DISEASE_DATABASE'),"
        "'cat':('api.species.cat_diseases','DISEASES'),"
        "'rabbit':('api.species.rabbit_diseases','DISEASES'),"
        "'hamster':('api.species.hamster_diseases','DISEASES'),"
        "'guinea_pig':('api.species.guinea_pig_diseases','DISEASES'),"
        "'chinchilla':('api.species.chinchilla_diseases','DISEASES'),"
        "'ferret':('api.species.ferret_diseases','DISEASES'),"
        "'hedgehog':('api.species.hedgehog_diseases','DISEASES'),"
        "'sugar_glider':('api.species.sugar_glider_diseases','DISEASES'),"
        "'degu':('api.species.degu_diseases','DISEASES'),"
        "'bird':('api.species.bird_diseases','DISEASES'),"
        "'parakeet':('api.species.parakeet_diseases','DISEASES'),"
        "'parrot':('api.species.parrot_diseases','DISEASES'),"
        "'reptile':('api.species.reptile_diseases','DISEASES'),"
        "'tortoise':('api.species.tortoise_diseases','DISEASES'),"
        "'snake':('api.species.snake_diseases','DISEASES'),"
        "'lizard':('api.species.lizard_diseases','DISEASES'),"
        "'amphibian':('api.species.amphibian_diseases','DISEASES'),"
        "'fish':('api.species.fish_diseases','DISEASES'),"
        "'exotic_other':('api.species.exotic_other_diseases','DISEASES'),"
        "};"
        "c={};"
        "[(c.__setitem__(s,len(getattr(importlib.import_module(m),a,[]))))for s,(m,a) in M.items()];"
        "print(json.dumps(c))"
    )
    try:
        result = subprocess.run(
            [sys.executable, "-c", script],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(Path(__file__).resolve().parent.parent),
        )
        if result.returncode == 0 and result.stdout.strip():
            counts = _json.loads(result.stdout.strip())
            logger.info("Counted diseases via subprocess (%d species)", len(counts))
            return counts
    except Exception:
        logger.warning("Subprocess disease count failed", exc_info=True)

    # Last resort: hardcoded counts (updated 2026-05-07 from Python modules)
    logger.warning("Using hardcoded disease counts as last-resort fallback")
    return {
        "dog": 611,
        "cat": 546,
        "horse": 621,
        "rabbit": 451,
        "hamster": 321,
        "guinea_pig": 346,
        "chinchilla": 278,
        "ferret": 277,
        "hedgehog": 244,
        "sugar_glider": 221,
        "degu": 200,
        "bird": 551,
        "parakeet": 458,
        "parrot": 283,
        "reptile": 286,
        "tortoise": 286,
        "snake": 248,
        "lizard": 250,
        "amphibian": 257,
        "fish": 36,
        "exotic_other": 289,
    }


def _fallback_drug_counts() -> tuple[dict[str, int], int]:
    """Count drugs per species — prefer species_counts.json, then Python module."""
    counts_path = Path(DB_PATH).parent / "species_counts.json"
    if counts_path.exists():
        try:
            import json as _json

            data = _json.loads(counts_path.read_text())
            per_sp = {k: int(v) for k, v in data.get("drug_counts", {}).items()}
            total = int(data.get("total_drugs", 0))
            if total > 0:
                return per_sp, total
        except Exception:
            logger.debug("Could not read drug counts from species_counts.json", exc_info=True)

    per_species: dict[str, int] = {}
    total = 0
    try:
        from api.drug_dictionary import DRUGS

        total = len(DRUGS)
        for d in DRUGS:
            for sp in d.get("species_info") or {}:
                per_species[sp] = per_species.get(sp, 0) + 1
    except Exception:
        logger.debug("Failed to load drug dictionary for counts", exc_info=True)
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
    else:
        # Supplement species that were never migrated to SQLite.
        # Check which species have zero rows in the DB — those need fallback.
        try:
            with get_connection() as conn:
                _db_species = {row[0] for row in conn.execute("SELECT DISTINCT species FROM diseases").fetchall()}
        except Exception:
            _db_species = set(disease_counts.keys())

        _unmigrated = [sp for sp in SPECIES_META if sp not in _db_species]
        if _unmigrated:
            _fb = _fallback_disease_counts()
            for sp in _unmigrated:
                if _fb.get(sp, 0) > 0:
                    disease_counts[sp] = _fb[sp]

    if total_drugs == 0:
        drug_counts, total_drugs = _fallback_drug_counts()
    else:
        # Supplement species with no drug rows in SQLite
        try:
            with get_connection() as conn:
                _db_drug_species = {
                    row[0] for row in conn.execute("SELECT DISTINCT species FROM drug_species_info").fetchall()
                }
        except Exception:
            _db_drug_species = set(drug_counts.keys())

        _unmigrated_drugs = [sp for sp in SPECIES_META if sp not in _db_drug_species]
        if _unmigrated_drugs:
            _fb_drugs, _fb_total = _fallback_drug_counts()
            for sp in _unmigrated_drugs:
                if _fb_drugs.get(sp, 0) > 0:
                    drug_counts[sp] = _fb_drugs[sp]
            if _fb_total > total_drugs:
                total_drugs = _fb_total

    stats = []
    for sp_id, meta in SPECIES_META.items():
        stats.append(
            {
                "id": sp_id,
                "name": meta["name_ja"],
                "nameEn": meta["name_en"],
                "description": meta.get("desc_en", ""),
                "description_ja": meta.get("desc_ja", ""),
                "diseases": disease_counts.get(sp_id, 0),
                "drugs": drug_counts.get(sp_id, 0),
            }
        )

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
            "SELECT urgency, COUNT(*) AS cnt FROM diseases WHERE urgency IS NOT NULL GROUP BY urgency ORDER BY urgency"
        ).fetchall()

    urgency_stats = []
    total_diseases = 0
    for row in urgency_rows:
        count = row["cnt"]
        urgency_stats.append(
            {
                "urgency": row["urgency"],
                "count": count,
            }
        )
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
        urgency_stats.append(
            {
                "urgency": row["urgency"],
                "count": count,
            }
        )
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
    try:
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
    except Exception:
        return []

    # Load category map from species module or horse HEALTH_CHECK_ITEMS
    category_map: dict[str, str] = {}
    if species == "horse":
        category_map = _load_horse_category_map()
    else:
        try:
            import importlib as _il

            _smod = _il.import_module(f"api.species.{species}_diseases")
            raw_cats = getattr(_smod, "SYMPTOM_CATEGORIES", {})
            # Detect format: {symptom_id: category} vs {category: {symptoms: [...]}}
            if raw_cats:
                first_val = next(iter(raw_cats.values()))
                if isinstance(first_val, str):
                    # Standard format: {symptom_id: category_name}
                    category_map = raw_cats
                elif isinstance(first_val, dict) and "symptoms" in first_val:
                    # Dog-style format: {category: {name_ja, name_en, symptoms: [...]}}
                    for cat_id, cat_info in raw_cats.items():
                        for sym_id in cat_info.get("symptoms", []):
                            category_map[sym_id] = cat_id
        except (ImportError, Exception):
            pass

    # Symptom records from symptoms table
    symptom_map: dict[str, dict] = {}
    for r in rows:
        raw_id = r["id"].removeprefix(f"{species}_")
        symptom_map[raw_id] = {
            "id": raw_id,
            "name_ja": r["name_ja"],
            "name_en": r["name_en"],
            "category": category_map.get(raw_id, "other"),
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
                    "category": category_map.get(sid, "other"),
                }

    return sorted(symptom_map.values(), key=lambda s: s["id"])


def get_symptoms_for_species(species: str) -> list[dict]:
    """Return symptom list for a species from SQLite, with module fallback."""
    result = _get_symptoms_for_species_cached(species, _cache_version)
    if result:
        return result

    # Fallback: load from Python species module if SQLite has no data
    import importlib as _importlib

    try:
        mod = _importlib.import_module(f"api.species.{species}_diseases")
        sym_names = getattr(mod, "SYMPTOM_NAMES", {})
        raw_cats = getattr(mod, "SYMPTOM_CATEGORIES", {})
        # Normalize category map format
        sym_cats: dict[str, str] = {}
        if raw_cats:
            first_val = next(iter(raw_cats.values()), None)
            if isinstance(first_val, str):
                sym_cats = raw_cats
            elif isinstance(first_val, dict) and "symptoms" in first_val:
                for cat_id, cat_info in raw_cats.items():
                    for s_id in cat_info.get("symptoms", []):
                        sym_cats[s_id] = cat_id
        if sym_names:
            return sorted(
                [
                    {
                        "id": sid,
                        "name_ja": v.get("ja", sid),
                        "name_en": v.get("en", sid),
                        "category": sym_cats.get(sid, "other"),
                    }
                    for sid, v in sym_names.items()
                ],
                key=lambda s: (s["category"], s["id"]),
            )
    except (ImportError, Exception):
        logger.debug("Fallback symptom loading failed for species module")
    return result


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
    # Parse reference JSON fields (enrichment fields)
    for field in ("prognosis_references", "rehabilitation_references", "nutrition_references"):
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
    # Clamp pagination parameters to prevent abuse
    limit = max(1, min(limit, 500))
    offset = max(0, offset)

    search_clause = (
        "(name LIKE ? ESCAPE '\\' OR name_ja LIKE ? ESCAPE '\\' OR "
        "description LIKE ? ESCAPE '\\' OR description_ja LIKE ? ESCAPE '\\' OR "
        "treatment LIKE ? ESCAPE '\\' OR treatment_ja LIKE ? ESCAPE '\\' OR "
        "prevention LIKE ? ESCAPE '\\' OR prevention_ja LIKE ? ESCAPE '\\' OR "
        "pathophysiology LIKE ? ESCAPE '\\' OR pathophysiology_ja LIKE ? ESCAPE '\\')"
    )

    with get_connection() as conn:
        conditions: list[str] = []
        params: list = []

        if species:
            conditions.append("species = ?")
            params.append(species)
        if search:
            like_pattern = "%" + search.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_") + "%"
            conditions.append(search_clause)
            params.extend([like_pattern] * 10)

        where = " WHERE " + " AND ".join(conditions) if conditions else ""

        _row = conn.execute(_COUNT_DISEASES_BASE + where, params).fetchone()
        total = _row[0] if _row else 0

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


# Cache for symptom categories by species (performance optimization)
_symptom_category_cache: dict[str, dict[str, str]] = {}


def _get_symptom_categories_for_species(species: str) -> dict[str, str]:
    """Get cached symptom ID -> category mapping for a species."""
    if species in _symptom_category_cache:
        return _symptom_category_cache[species]

    symptoms = get_symptoms_for_species(species)
    symptom_cats = {s["id"]: s.get("category", "other") for s in symptoms}
    _symptom_category_cache[species] = symptom_cats
    return symptom_cats


def _infer_disease_categories(disease: dict, species: str) -> set[str]:
    """Infer disease categories from its symptoms.

    Uses cached symptom category mappings for performance.
    """
    symptoms_json = disease.get("symptoms")
    if not symptoms_json:
        return {"other"}

    try:
        symptom_ids = json.loads(symptoms_json)
    except (json.JSONDecodeError, TypeError):
        return {"other"}

    # Get cached symptom category mapping
    symptom_cats = _get_symptom_categories_for_species(species)

    categories = set()
    for sym_id in symptom_ids:
        cat = symptom_cats.get(sym_id, "other")
        if cat:
            categories.add(cat)

    return categories if categories else {"other"}


def search_diseases(query: str, species: str | None = None, category: str | None = None, limit: int = 50) -> list[dict]:
    """Search diseases by name, description, treatment, and other fields.

    Searches both English and Japanese fields with multiple keyword support.
    Each keyword must appear in at least one field (AND logic).
    Results are ranked by relevance (name match prioritized).
    """
    if not query or not query.strip():
        return []

    # Split query into keywords (space-separated)
    keywords = [k.strip() for k in query.split() if k.strip()]
    if not keywords:
        return []

    # Escape special characters
    def escape_like(s):
        return s.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")

    # Build AND clauses for each keyword (each must match at least one field)
    and_clauses = []
    params = []
    for keyword in keywords:
        like_pattern = "%" + escape_like(keyword) + "%"
        # OR within each keyword (match any field)
        or_clause = (
            "(name LIKE ? ESCAPE '\\' OR name_ja LIKE ? ESCAPE '\\' OR "
            "description LIKE ? ESCAPE '\\' OR description_ja LIKE ? ESCAPE '\\' OR "
            "treatment LIKE ? ESCAPE '\\' OR treatment_ja LIKE ? ESCAPE '\\' OR "
            "prevention LIKE ? ESCAPE '\\' OR prevention_ja LIKE ? ESCAPE '\\' OR "
            "pathophysiology LIKE ? ESCAPE '\\' OR pathophysiology_ja LIKE ? ESCAPE '\\')"
        )
        and_clauses.append(or_clause)
        # Add same pattern 10 times (one for each field)
        params.extend([like_pattern] * 10)

    search_clause = " AND ".join(f"({c})" for c in and_clauses)

    with get_connection() as conn:
        if species:
            query_str = (
                "SELECT id, species, name, name_ja, urgency, symptoms FROM diseases "
                "WHERE " + search_clause + " AND species = ? ORDER BY name LIMIT ?"
            )
            rows = conn.execute(
                query_str,
                [*params, species, limit],
            ).fetchall()
        else:
            query_str = (
                "SELECT id, species, name, name_ja, urgency, symptoms FROM diseases "
                "WHERE " + search_clause + " ORDER BY species, name LIMIT ?"
            )
            rows = conn.execute(
                query_str,
                [*params, limit],
            ).fetchall()

    # Score results for better relevance ranking + category filtering
    results = []
    for row in rows:
        result = _row_to_disease_summary(row)
        row_species = row["species"]
        score = 0
        name = (result.get("name") or "").lower()
        name_ja = (result.get("name_ja") or "").lower()

        # Score: name matches are prioritized
        for keyword in keywords:
            kw_lower = keyword.lower()
            if kw_lower in name:
                score += 100  # Exact name match is highest priority
            if kw_lower in name_ja:
                score += 100
            # For each additional match in name, add points
            score += name.count(kw_lower) * 10

        # Category filtering
        if category:
            # Infer disease categories from symptoms
            disease_cats = _infer_disease_categories(dict(row), row_species)
            if category not in disease_cats:
                continue  # Skip if category doesn't match

        results.append((score, result))

    # Sort by score (descending), then by name
    results.sort(key=lambda x: (-x[0], x[1].get("name", "")))
    return [r[1] for r in results]


def get_diseases_by_symptom(symptom_id: str, species: str | None = None, limit: int = 50) -> list[dict]:
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
