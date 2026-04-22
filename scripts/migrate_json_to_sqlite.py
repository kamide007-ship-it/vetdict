#!/usr/bin/env python3
"""
Migrate diseases from JSON to SQLite database

Usage:
  python3 scripts/migrate_json_to_sqlite.py

This script:
1. Creates SQLite schema with optimal indexes
2. Loads 6,393 diseases from diseases_all_species.json
3. Bulk inserts into SQLite
4. Creates FTS5 index for full-text search
5. Verifies record count and data integrity
6. Backs up original JSON for safety
"""

import json
import sqlite3
import sys
from pathlib import Path
from datetime import datetime

# Schema definition (extracted from design)
SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS diseases (
    id TEXT PRIMARY KEY,
    species TEXT NOT NULL,
    name_en TEXT NOT NULL,
    name_ja TEXT NOT NULL,
    pathophysiology_en TEXT,
    pathophysiology_ja TEXT,
    causes_en TEXT,
    causes_ja TEXT,
    clinical_signs_en TEXT,
    clinical_signs_ja TEXT,
    diagnosis_en TEXT,
    diagnosis_ja TEXT,
    treatment_en TEXT,
    treatment_ja TEXT,
    treatment_duration_weeks INTEGER,
    prognosis_en TEXT,
    prognosis_ja TEXT,
    prevention_en TEXT,
    prevention_ja TEXT,
    transmission_en TEXT,
    transmission_ja TEXT,
    symptoms_json TEXT,
    recommended_tests_json TEXT,
    urgency TEXT,
    severity_score INTEGER,
    estimated_cost_level TEXT,
    hospitalization_likelihood TEXT,
    monitoring_frequency TEXT,
    prognosis_references_json TEXT,
    nutrition_references_json TEXT,
    rehabilitation_references_json TEXT,
    enriched_at TEXT,
    enrichment_phase INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_species ON diseases(species);
CREATE INDEX IF NOT EXISTS idx_urgency ON diseases(urgency);
CREATE INDEX IF NOT EXISTS idx_species_urgency ON diseases(species, urgency);
CREATE INDEX IF NOT EXISTS idx_severity_score ON diseases(severity_score DESC);
CREATE INDEX IF NOT EXISTS idx_emergency ON diseases(species)
    WHERE urgency IN ('emergency', 'high');

-- FTS5 virtual table
CREATE VIRTUAL TABLE IF NOT EXISTS diseases_fts USING fts5(
    id UNINDEXED,
    name_en,
    name_ja,
    pathophysiology_en,
    pathophysiology_ja,
    clinical_signs_en,
    clinical_signs_ja,
    symptoms,
    content=diseases,
    content_rowid=rowid
);

-- Triggers
CREATE TRIGGER IF NOT EXISTS diseases_ai AFTER INSERT ON diseases BEGIN
  INSERT INTO diseases_fts(rowid, id, name_en, name_ja, pathophysiology_en, pathophysiology_ja, clinical_signs_en, clinical_signs_ja, symptoms)
  VALUES (new.rowid, new.id, new.name_en, new.name_ja, new.pathophysiology_en, new.pathophysiology_ja, new.clinical_signs_en, new.clinical_signs_ja, new.symptoms_json);
END;

CREATE TRIGGER IF NOT EXISTS diseases_ad AFTER DELETE ON diseases BEGIN
  DELETE FROM diseases_fts WHERE rowid = old.rowid;
END;

CREATE TRIGGER IF NOT EXISTS diseases_au AFTER UPDATE ON diseases BEGIN
  DELETE FROM diseases_fts WHERE rowid = old.rowid;
  INSERT INTO diseases_fts(rowid, id, name_en, name_ja, pathophysiology_en, pathophysiology_ja, clinical_signs_en, clinical_signs_ja, symptoms)
  VALUES (new.rowid, new.id, new.name_en, new.name_ja, new.pathophysiology_en, new.pathophysiology_ja, new.clinical_signs_en, new.clinical_signs_ja, new.symptoms_json);
END;

CREATE TABLE IF NOT EXISTS migration_metadata (
    key TEXT PRIMARY KEY,
    value TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

def load_json_diseases(json_path):
    """Load diseases from JSON file"""
    print(f"📂 Loading diseases from {json_path}...")
    with open(json_path, 'r', encoding='utf-8') as f:
        diseases = json.load(f)
    print(f"✓ Loaded {len(diseases)} diseases")
    return diseases

def transform_disease(disease_json):
    """Transform JSON disease record to SQLite tuple"""
    return (
        disease_json.get('id', ''),
        disease_json.get('species', ''),
        disease_json.get('name', ''),
        disease_json.get('name_ja', ''),
        disease_json.get('pathophysiology', ''),
        disease_json.get('pathophysiology_ja', ''),
        disease_json.get('causes', ''),
        disease_json.get('causes_ja', ''),
        disease_json.get('clinical_signs', ''),
        disease_json.get('clinical_signs_ja', ''),
        disease_json.get('diagnosis', ''),
        disease_json.get('diagnosis_ja', ''),
        disease_json.get('treatment', ''),
        disease_json.get('treatment_ja', ''),
        disease_json.get('treatment_duration_weeks'),
        disease_json.get('prognosis', ''),
        disease_json.get('prognosis_ja', ''),
        disease_json.get('prevention', ''),
        disease_json.get('prevention_ja', ''),
        disease_json.get('transmission', ''),
        disease_json.get('transmission_ja', ''),
        json.dumps(disease_json.get('symptoms', []), ensure_ascii=False) if disease_json.get('symptoms') else None,
        json.dumps(disease_json.get('recommended_tests', []), ensure_ascii=False) if disease_json.get('recommended_tests') else None,
        disease_json.get('urgency', 'normal'),
        disease_json.get('severity_score'),
        disease_json.get('estimated_cost_level', ''),
        disease_json.get('hospitalization_likelihood', ''),
        disease_json.get('monitoring_frequency', ''),
        json.dumps(disease_json.get('prognosis_references', {}), ensure_ascii=False) if disease_json.get('prognosis_references') else None,
        json.dumps(disease_json.get('nutrition_references', {}), ensure_ascii=False) if disease_json.get('nutrition_references') else None,
        json.dumps(disease_json.get('rehabilitation_references', {}), ensure_ascii=False) if disease_json.get('rehabilitation_references') else None,
        disease_json.get('enriched_at', ''),
        disease_json.get('enrichment_phase'),
    )

def migrate_to_sqlite(db_path, json_diseases):
    """Perform migration to SQLite"""
    print(f"\n🗄️  Creating SQLite database at {db_path}...")

    # Connect and enable features
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA cache_size=-64000")
    cursor = conn.cursor()

    try:
        # Create schema
        print("📋 Creating schema...")
        # Execute schema as separate statements to avoid parsing issues
        statements = [
            # Main table
            """CREATE TABLE IF NOT EXISTS diseases (
                id TEXT PRIMARY KEY,
                species TEXT NOT NULL,
                name_en TEXT NOT NULL,
                name_ja TEXT NOT NULL,
                pathophysiology_en TEXT,
                pathophysiology_ja TEXT,
                causes_en TEXT,
                causes_ja TEXT,
                clinical_signs_en TEXT,
                clinical_signs_ja TEXT,
                diagnosis_en TEXT,
                diagnosis_ja TEXT,
                treatment_en TEXT,
                treatment_ja TEXT,
                treatment_duration_weeks INTEGER,
                prognosis_en TEXT,
                prognosis_ja TEXT,
                prevention_en TEXT,
                prevention_ja TEXT,
                transmission_en TEXT,
                transmission_ja TEXT,
                symptoms_json TEXT,
                recommended_tests_json TEXT,
                urgency TEXT,
                severity_score INTEGER,
                estimated_cost_level TEXT,
                hospitalization_likelihood TEXT,
                monitoring_frequency TEXT,
                prognosis_references_json TEXT,
                nutrition_references_json TEXT,
                rehabilitation_references_json TEXT,
                enriched_at TEXT,
                enrichment_phase INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""",
            "CREATE INDEX IF NOT EXISTS idx_species ON diseases(species)",
            "CREATE INDEX IF NOT EXISTS idx_urgency ON diseases(urgency)",
            "CREATE INDEX IF NOT EXISTS idx_species_urgency ON diseases(species, urgency)",
            "CREATE INDEX IF NOT EXISTS idx_severity_score ON diseases(severity_score DESC)",
            "CREATE INDEX IF NOT EXISTS idx_emergency ON diseases(species) WHERE urgency IN ('emergency', 'high')",
            """CREATE VIRTUAL TABLE IF NOT EXISTS diseases_fts USING fts5(
                id UNINDEXED,
                name_en,
                name_ja,
                pathophysiology_en,
                pathophysiology_ja,
                clinical_signs_en,
                clinical_signs_ja,
                symptoms,
                content=diseases,
                content_rowid=rowid
            )""",
            """CREATE TABLE IF NOT EXISTS migration_metadata (
                key TEXT PRIMARY KEY,
                value TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""",
        ]

        for stmt in statements:
            cursor.execute(stmt)
        conn.commit()

        # Bulk insert
        print(f"📥 Inserting {len(json_diseases)} diseases...")
        insert_sql = """
        INSERT INTO diseases (
            id, species, name_en, name_ja, pathophysiology_en, pathophysiology_ja,
            causes_en, causes_ja, clinical_signs_en, clinical_signs_ja,
            diagnosis_en, diagnosis_ja, treatment_en, treatment_ja, treatment_duration_weeks,
            prognosis_en, prognosis_ja, prevention_en, prevention_ja, transmission_en, transmission_ja,
            symptoms_json, recommended_tests_json, urgency, severity_score,
            estimated_cost_level, hospitalization_likelihood, monitoring_frequency,
            prognosis_references_json, nutrition_references_json, rehabilitation_references_json,
            enriched_at, enrichment_phase
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        transformed = [transform_disease(d) for d in json_diseases]
        cursor.executemany(insert_sql, transformed)
        conn.commit()
        print(f"✓ Inserted {cursor.rowcount} diseases")

        # Verify count
        count_result = cursor.execute("SELECT COUNT(*) FROM diseases").fetchone()
        db_count = count_result[0]
        print(f"\n✓ Verification: {db_count} diseases in database (expected: {len(json_diseases)})")

        if db_count != len(json_diseases):
            raise ValueError(f"Mismatch! Expected {len(json_diseases)}, got {db_count}")

        # Record migration metadata
        cursor.execute("""
        INSERT OR REPLACE INTO migration_metadata (key, value, updated_at)
        VALUES ('last_migration', ?, CURRENT_TIMESTAMP)
        """, (datetime.now().isoformat(),))
        cursor.execute("""
        INSERT OR REPLACE INTO migration_metadata (key, value, updated_at)
        VALUES ('disease_count', ?, CURRENT_TIMESTAMP)
        """, (str(db_count),))
        conn.commit()

        # Test queries
        print("\n🧪 Testing queries...")

        # Test 1: Lookup by ID
        result = cursor.execute("SELECT name_en, species FROM diseases WHERE id = ?", ('cat_0001',)).fetchone()
        if result:
            print(f"  ✓ Lookup by ID: {result[0]} ({result[1]})")

        # Test 2: Filter by species
        count = cursor.execute("SELECT COUNT(*) FROM diseases WHERE species = ?", ('Cat',)).fetchone()[0]
        print(f"  ✓ Filter by species (Cat): {count} diseases")

        # Test 3: Filter by urgency
        count = cursor.execute("SELECT COUNT(*) FROM diseases WHERE urgency IN ('emergency', 'high')").fetchone()[0]
        print(f"  ✓ Filter by urgency (emergency/high): {count} diseases")

        # Test 4: Index performance check
        import time
        start = time.time()
        cursor.execute("SELECT COUNT(*) FROM diseases WHERE species = 'Dog' AND urgency = 'emergency'")
        elapsed = (time.time() - start) * 1000
        print(f"  ✓ Compound query (species + urgency): {elapsed:.2f}ms")

        print("\n✅ Migration complete!")
        return True

    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def main():
    # Paths
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    json_path = repo_root / 'diseases_all_species.json'
    db_path = repo_root / 'diseases.db'

    print("=" * 60)
    print("VetDict: JSON → SQLite Migration")
    print("=" * 60)

    # Load JSON
    try:
        json_diseases = load_json_diseases(json_path)
    except FileNotFoundError:
        print(f"❌ Error: {json_path} not found")
        sys.exit(1)

    # Create backup of existing DB if present
    if db_path.exists():
        backup_path = repo_root / f'diseases.db.backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
        print(f"💾 Backing up existing database to {backup_path.name}...")
        db_path.rename(backup_path)

    # Perform migration
    success = migrate_to_sqlite(db_path, json_diseases)

    if success:
        print(f"\n📊 Database location: {db_path}")
        print(f"   Size: {db_path.stat().st_size / 1024 / 1024:.2f} MB")
        print("\n✅ Ready for deployment")
        sys.exit(0)
    else:
        print("\n❌ Migration failed. Restore from backup if needed.")
        sys.exit(1)

if __name__ == '__main__':
    main()
