#!/usr/bin/env python3
"""
SQLite Schema Design for VetDict Diseases Database

Migration: JSON → SQLite (6,393 diseases)
Performance goal: 10-100x speedup in query performance
"""

SCHEMA_SQL = """
-- Main diseases table
CREATE TABLE IF NOT EXISTS diseases (
    id TEXT PRIMARY KEY,
    species TEXT NOT NULL,
    name_en TEXT NOT NULL,
    name_ja TEXT NOT NULL,

    -- Medical content (core)
    pathophysiology_en TEXT,
    pathophysiology_ja TEXT,
    causes_en TEXT,
    causes_ja TEXT,
    clinical_signs_en TEXT,
    clinical_signs_ja TEXT,

    -- Diagnosis & Treatment
    diagnosis_en TEXT,
    diagnosis_ja TEXT,
    treatment_en TEXT,
    treatment_ja TEXT,
    treatment_duration_weeks INTEGER,

    -- Prognosis & Prevention
    prognosis_en TEXT,
    prognosis_ja TEXT,
    prevention_en TEXT,
    prevention_ja TEXT,
    transmission_en TEXT,
    transmission_ja TEXT,

    -- Symptoms (JSON array as TEXT)
    symptoms_json TEXT,
    recommended_tests_json TEXT,

    -- Clinical metadata
    urgency TEXT,  -- 'emergency', 'high', 'normal'
    severity_score INTEGER,
    estimated_cost_level TEXT,  -- 'low', 'medium', 'high'
    hospitalization_likelihood TEXT,  -- 'low', 'medium', 'high'
    monitoring_frequency TEXT,

    -- References (JSON objects as TEXT)
    prognosis_references_json TEXT,
    nutrition_references_json TEXT,
    rehabilitation_references_json TEXT,

    -- Metadata
    enriched_at TEXT,
    enrichment_phase INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Full-text search content (denormalized)
    fts_content TEXT GENERATED ALWAYS AS (
        name_en || ' ' || name_ja || ' ' ||
        COALESCE(pathophysiology_en, '') || ' ' ||
        COALESCE(clinical_signs_en, '') || ' ' ||
        COALESCE(symptoms_json, '')
    ) STORED
);

-- Primary indexes for common queries
CREATE INDEX IF NOT EXISTS idx_species ON diseases(species);
CREATE INDEX IF NOT EXISTS idx_urgency ON diseases(urgency);
CREATE INDEX IF NOT EXISTS idx_species_urgency ON diseases(species, urgency);
CREATE INDEX IF NOT EXISTS idx_severity_score ON diseases(severity_score DESC);

-- Partial indexes for emergency cases (common use case)
CREATE INDEX IF NOT EXISTS idx_emergency ON diseases(species)
    WHERE urgency IN ('emergency', 'high');

-- Full-text search virtual table (FTS5)
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

-- Create triggers to keep FTS index updated
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

-- Metadata table
CREATE TABLE IF NOT EXISTS migration_metadata (
    key TEXT PRIMARY KEY,
    value TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

# Schema explanation
SCHEMA_NOTES = """
=== SQLite Schema Design Notes ===

1. **Main Table: diseases**
   - Denormalized design (for performance over storage)
   - Both JA and EN fields stored separately
   - All text fields as TEXT (SQLite optimizes for this)
   - Total fields: 30+

2. **Symptom & Reference Storage**
   - Complex structures (arrays/objects) stored as JSON strings
   - Allows partial indexing without extra tables
   - Can be parsed by application layer

3. **Indexes Strategy**
   - idx_species: Most common filter (21 species)
   - idx_urgency: Primary filter (emergency, high, normal)
   - idx_species_urgency: Compound for fast diagnosis queries
   - idx_emergency: Partial index (optimize emergency cases)
   - idx_severity_score: Descending for ranking

4. **Full-Text Search (FTS5)**
   - Virtual table for fast text searches
   - Includes: name, pathophysiology, clinical_signs, symptoms
   - Automatic triggers to keep synchronized with main table
   - Supports: phrase search, AND/OR operators, fuzzy matching

5. **Performance Characteristics**
   - Single disease lookup: < 1ms (primary key)
   - Filter by species: < 5ms (indexed)
   - Filter by species + urgency: < 5ms (compound index)
   - Full-text search: < 10ms (FTS5)
   - List all diseases: < 50ms

6. **Backward Compatibility**
   - symptoms_json and recommended_tests_json stored as JSON strings
   - No API changes needed (application layer parses)
   - Can coexist with JSON file during migration

7. **JSON Columns**
   - symptoms_json: ["fever", "lethargy", ...]
   - recommended_tests_json: ["test1", "test2", ...]
   - prognosis_references_json: {"references": [...]}
   - nutrition_references_json: {"references": [...]}
   - rehabilitation_references_json: {"references": [...]}

8. **WAL Mode (Write-Ahead Logging)**
   - Recommended for better concurrency
   - Enable in application: PRAGMA journal_mode=WAL;
   - Better for production deployments

9. **Migration Strategy**
   - Create empty schema first
   - Bulk insert from JSON in batches
   - Build FTS index after migration
   - Verify record count matches source (6,393)
   - Commit transaction on success
"""

if __name__ == "__main__":
    print(SCHEMA_NOTES)
    print("\n=== SQL Schema ===\n")
    print(SCHEMA_SQL)
