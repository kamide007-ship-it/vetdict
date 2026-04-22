"""
VetDict SQLite database layer.

Provides schema creation, connection management, and query helpers
for the diseases and drugs tables.
"""

import json
import logging

logger = logging.getLogger(__name__)
import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path

DB_PATH = os.getenv("VETDICT_DB_PATH", str(Path(__file__).resolve().parent.parent / "instance" / "vetdict.db"))


def _ensure_dir(path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)


@contextmanager
def get_connection(db_path: str | None = None):
    """Yield a SQLite connection with WAL mode and foreign keys enabled."""
    path = db_path or DB_PATH
    _ensure_dir(path)
    conn = sqlite3.connect(path, timeout=10.0)
    conn.row_factory = sqlite3.Row
    try:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        # Integrity check on first connection to detect corruption early
        integrity = conn.execute("PRAGMA quick_check").fetchone()[0]
        if integrity != "ok":
            logger.critical("Database corruption detected: %s (path: %s)", integrity, path)
    except sqlite3.DatabaseError:
        logger.critical("Database error during connection setup (path: %s)", path, exc_info=True)
        conn.close()
        raise
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


SCHEMA_SQL = """\
-- Diseases table
CREATE TABLE IF NOT EXISTS diseases (
    id TEXT PRIMARY KEY,
    species TEXT NOT NULL,
    name TEXT NOT NULL,
    name_ja TEXT NOT NULL,
    description TEXT,
    description_ja TEXT,
    pathophysiology TEXT,
    pathophysiology_ja TEXT,
    causes TEXT,
    causes_ja TEXT,
    treatment TEXT,
    treatment_ja TEXT,
    prevention TEXT,
    prevention_ja TEXT,
    prognosis TEXT,
    prognosis_ja TEXT,
    urgency TEXT,
    symptoms TEXT,              -- JSON array of symptom IDs
    recommended_tests TEXT,     -- JSON array
    onset_pattern TEXT,         -- JSON array
    age_predisposition TEXT,    -- JSON array

    -- Treatment enrichment fields (Phase 1 expansion)
    prognosis_detailed TEXT,                       -- Extended prognosis with recovery timeline
    prognosis_detailed_ja TEXT,                    -- 日本語版
    rehabilitation_protocol TEXT,                  -- Evidence-based rehabilitation program
    rehabilitation_protocol_ja TEXT,               -- 日本語版
    nutrition_management TEXT,                     -- Nutritional support guidelines
    nutrition_management_ja TEXT,                  -- 日本語版

    -- Reference citations (JSON format)
    prognosis_references TEXT,                     -- JSON: [{"id": "...", "title": "...", "journal": "...", "year": ..., "doi": "...", ...}]
    rehabilitation_references TEXT,                -- JSON: reference list for rehabilitation
    nutrition_references TEXT,                     -- JSON: reference list for nutrition

    -- Clinical metrics
    recovery_timeline_weeks INTEGER,               -- Typical recovery period in weeks
    success_rate REAL,                             -- Treatment success rate (0.0-1.0)
    mortality_rate REAL,                           -- Mortality rate (0.0-1.0)

    enriched_at TEXT,
    enrichment_phase INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_diseases_species ON diseases(species);
CREATE INDEX IF NOT EXISTS idx_diseases_name ON diseases(name);

-- Symptoms table
CREATE TABLE IF NOT EXISTS symptoms (
    id TEXT PRIMARY KEY,
    name_en TEXT NOT NULL,
    name_ja TEXT NOT NULL,
    species TEXT NOT NULL,
    clinical_weight REAL DEFAULT 1.0
);

CREATE INDEX IF NOT EXISTS idx_symptoms_species ON symptoms(species);

-- Drugs table
CREATE TABLE IF NOT EXISTS drugs (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    name_ja TEXT NOT NULL,
    category TEXT,
    mechanism TEXT,
    mechanism_ja TEXT,
    contraindications TEXT,
    contraindications_ja TEXT,
    side_effects TEXT,          -- JSON array
    side_effects_ja TEXT,       -- JSON array
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_drugs_name ON drugs(name);
CREATE INDEX IF NOT EXISTS idx_drugs_category ON drugs(category);

-- Drug species info (dosage & safety per species)
CREATE TABLE IF NOT EXISTS drug_species_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    drug_id TEXT NOT NULL REFERENCES drugs(id) ON DELETE CASCADE,
    species TEXT NOT NULL,
    safe INTEGER NOT NULL DEFAULT 1,
    dosage TEXT,
    dosage_ja TEXT,
    notes TEXT,
    notes_ja TEXT,
    UNIQUE(drug_id, species)
);

CREATE INDEX IF NOT EXISTS idx_drug_species ON drug_species_info(drug_id, species);
"""


def init_db(db_path: str | None = None) -> None:
    """Create all tables and indexes if they don't exist."""
    with get_connection(db_path) as conn:
        conn.executescript(SCHEMA_SQL)
        _run_migrations(conn)


def _run_migrations(conn: sqlite3.Connection) -> None:
    """Run incremental schema migrations for backward compatibility."""
    cursor = conn.cursor()

    # Migration 1: Add treatment enrichment columns (Phase 1 expansion)
    try:
        cursor.execute("PRAGMA table_info(diseases)")
        columns = {row[1] for row in cursor.fetchall()}

        if "prognosis_detailed" not in columns:
            logger.info("Running migration: add treatment enrichment columns")
            cursor.execute("ALTER TABLE diseases ADD COLUMN prognosis_detailed TEXT")
            cursor.execute("ALTER TABLE diseases ADD COLUMN prognosis_detailed_ja TEXT")
            cursor.execute("ALTER TABLE diseases ADD COLUMN rehabilitation_protocol TEXT")
            cursor.execute("ALTER TABLE diseases ADD COLUMN rehabilitation_protocol_ja TEXT")
            cursor.execute("ALTER TABLE diseases ADD COLUMN nutrition_management TEXT")
            cursor.execute("ALTER TABLE diseases ADD COLUMN nutrition_management_ja TEXT")
            cursor.execute("ALTER TABLE diseases ADD COLUMN prognosis_references TEXT")
            cursor.execute("ALTER TABLE diseases ADD COLUMN rehabilitation_references TEXT")
            cursor.execute("ALTER TABLE diseases ADD COLUMN nutrition_references TEXT")
            cursor.execute("ALTER TABLE diseases ADD COLUMN recovery_timeline_weeks INTEGER")
            cursor.execute("ALTER TABLE diseases ADD COLUMN success_rate REAL")
            cursor.execute("ALTER TABLE diseases ADD COLUMN mortality_rate REAL")
            conn.commit()
            logger.info("Migration complete: treatment enrichment columns added")
    except sqlite3.OperationalError as e:
        logger.warning("Migration skipped (columns may already exist): %s", e)


# ---------------------------------------------------------------------------
# Disease helpers
# ---------------------------------------------------------------------------


def upsert_disease(conn: sqlite3.Connection, disease: dict) -> None:
    """Insert or replace a disease record."""

    # Helper to convert values to JSON string if they're dict/list but should be JSON
    def _to_json_if_needed(val, is_json_field=False):
        if val is None:
            return None
        if is_json_field and isinstance(val, (dict, list)):
            return json.dumps(val, ensure_ascii=False)
        if isinstance(val, (set, list)):
            return json.dumps(list(val), ensure_ascii=False)
        return val

    def _ensure_string(val):
        """Convert list fields to strings or JSON if needed."""
        if isinstance(val, list):
            # If it's a list, convert to JSON representation
            return json.dumps(val, ensure_ascii=False) if val else None
        return val

    conn.execute(
        """INSERT OR REPLACE INTO diseases
           (id, species, name, name_ja, description, description_ja,
            pathophysiology, pathophysiology_ja, causes, causes_ja,
            treatment, treatment_ja, prevention, prevention_ja,
            prognosis, prognosis_ja, urgency, symptoms,
            recommended_tests, onset_pattern, age_predisposition,
            prognosis_detailed, prognosis_detailed_ja,
            rehabilitation_protocol, rehabilitation_protocol_ja,
            nutrition_management, nutrition_management_ja,
            prognosis_references, rehabilitation_references, nutrition_references,
            recovery_timeline_weeks, success_rate, mortality_rate,
            enriched_at, enrichment_phase, updated_at)
           VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?, CURRENT_TIMESTAMP)""",
        (
            disease.get("id"),
            disease.get("species"),
            disease.get("name"),
            disease.get("name_ja"),
            _ensure_string(disease.get("description")),
            _ensure_string(disease.get("description_ja")),
            _ensure_string(disease.get("pathophysiology")),
            _ensure_string(disease.get("pathophysiology_ja")),
            _ensure_string(disease.get("causes")),
            _ensure_string(disease.get("causes_ja")),
            _ensure_string(disease.get("treatment")),
            _ensure_string(disease.get("treatment_ja")),
            _ensure_string(disease.get("prevention")),
            _ensure_string(disease.get("prevention_ja")),
            _ensure_string(disease.get("prognosis")),
            _ensure_string(disease.get("prognosis_ja")),
            disease.get("urgency"),
            _to_json_if_needed(disease.get("symptoms"), is_json_field=True),
            _to_json_if_needed(disease.get("recommended_tests"), is_json_field=True),
            _to_json_if_needed(disease.get("onset_pattern"), is_json_field=True),
            _to_json_if_needed(disease.get("age_predisposition"), is_json_field=True),
            _ensure_string(disease.get("prognosis_detailed")),
            _ensure_string(disease.get("prognosis_detailed_ja")),
            _ensure_string(disease.get("rehabilitation_protocol")),
            _ensure_string(disease.get("rehabilitation_protocol_ja")),
            _ensure_string(disease.get("nutrition_management")),
            _ensure_string(disease.get("nutrition_management_ja")),
            _to_json_if_needed(disease.get("prognosis_references"), is_json_field=True),
            _to_json_if_needed(disease.get("rehabilitation_references"), is_json_field=True),
            _to_json_if_needed(disease.get("nutrition_references"), is_json_field=True),
            disease.get("recovery_timeline_weeks"),
            disease.get("success_rate"),
            disease.get("mortality_rate"),
            disease.get("enriched_at"),
            disease.get("enrichment_phase"),
        ),
    )


def get_diseases_by_species(conn: sqlite3.Connection, species: str) -> list[dict]:
    """Return all diseases for a given species."""
    rows = conn.execute("SELECT * FROM diseases WHERE species = ? ORDER BY name", (species,)).fetchall()
    return [dict(r) for r in rows]


def get_disease_by_id(conn: sqlite3.Connection, disease_id: str) -> dict | None:
    """Return a single disease by ID."""
    row = conn.execute("SELECT * FROM diseases WHERE id = ?", (disease_id,)).fetchone()
    return dict(row) if row else None


def delete_disease(conn: sqlite3.Connection, disease_id: str) -> bool:
    """Delete a disease by ID. Returns True if a row was deleted."""
    cursor = conn.execute("DELETE FROM diseases WHERE id = ?", (disease_id,))
    return cursor.rowcount > 0


def count_diseases(conn: sqlite3.Connection) -> dict:
    """Return total disease count and per-species breakdown."""
    total = conn.execute("SELECT COUNT(*) FROM diseases").fetchone()[0]
    rows = conn.execute("SELECT species, COUNT(*) as cnt FROM diseases GROUP BY species ORDER BY species").fetchall()
    return {"total": total, "by_species": {r["species"]: r["cnt"] for r in rows}}


# ---------------------------------------------------------------------------
# Drug helpers
# ---------------------------------------------------------------------------


def upsert_drug(conn: sqlite3.Connection, drug: dict) -> None:
    """Insert or replace a drug record and its species info."""
    conn.execute(
        """INSERT OR REPLACE INTO drugs
           (id, name, name_ja, category, mechanism, mechanism_ja,
            contraindications, contraindications_ja, side_effects, side_effects_ja,
            updated_at)
           VALUES (?,?,?,?,?,?,?,?,?,?, CURRENT_TIMESTAMP)""",
        (
            drug.get("id"),
            drug.get("name"),
            drug.get("name_ja"),
            drug.get("category"),
            drug.get("mechanism"),
            drug.get("mechanism_ja"),
            drug.get("contraindications"),
            drug.get("contraindications_ja"),
            json.dumps(drug["side_effects"])
            if isinstance(drug.get("side_effects"), list)
            else drug.get("side_effects"),
            json.dumps(drug["side_effects_ja"])
            if isinstance(drug.get("side_effects_ja"), list)
            else drug.get("side_effects_ja"),
        ),
    )
    for species, info in (drug.get("species_info") or {}).items():
        conn.execute(
            """INSERT OR REPLACE INTO drug_species_info
               (drug_id, species, safe, dosage, dosage_ja, notes, notes_ja)
               VALUES (?,?,?,?,?,?,?)""",
            (
                drug["id"],
                species,
                1 if info.get("safe", True) else 0,
                info.get("dosage"),
                info.get("dosage_ja"),
                info.get("notes"),
                info.get("notes_ja"),
            ),
        )


def get_all_drugs(conn: sqlite3.Connection) -> list[dict]:
    """Return all drugs."""
    rows = conn.execute("SELECT * FROM drugs ORDER BY name").fetchall()
    return [dict(r) for r in rows]


def get_drug_by_id(conn: sqlite3.Connection, drug_id: str) -> dict | None:
    """Return a drug with species info."""
    row = conn.execute("SELECT * FROM drugs WHERE id = ?", (drug_id,)).fetchone()
    if not row:
        return None
    drug = dict(row)
    species_rows = conn.execute("SELECT * FROM drug_species_info WHERE drug_id = ?", (drug_id,)).fetchall()
    drug["species_info"] = {r["species"]: dict(r) for r in species_rows}
    return drug


# ---------------------------------------------------------------------------
# Symptom helpers
# ---------------------------------------------------------------------------


def upsert_symptom(
    conn: sqlite3.Connection, symptom_id: str, name_en: str, name_ja: str, species: str, weight: float = 1.0
) -> None:
    """Insert or replace a symptom."""
    conn.execute(
        "INSERT OR REPLACE INTO symptoms (id, name_en, name_ja, species, clinical_weight) VALUES (?,?,?,?,?)",
        (symptom_id, name_en, name_ja, species, weight),
    )


def get_symptoms_by_species(conn: sqlite3.Connection, species: str) -> list[dict]:
    """Return all symptoms for a species."""
    rows = conn.execute("SELECT * FROM symptoms WHERE species = ? ORDER BY id", (species,)).fetchall()
    return [dict(r) for r in rows]
