#!/usr/bin/env python3
"""
Integration tests for SQLite migration

Tests:
  - Database schema integrity
  - Data migration completeness
  - Query performance
  - Backward compatibility
"""

import sqlite3
import time
from pathlib import Path

import pytest

# Database path
DB_PATH = str(Path(__file__).resolve().parent.parent / "diseases.db")


def _diseases_db_ready() -> bool:
    """Return True only when diseases.db has been migrated (has the diseases table)."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='diseases'")
        result = cur.fetchone()
        conn.close()
        return bool(result)
    except Exception:
        return False


_SKIP_REASON = "diseases.db not yet migrated — run scripts/migrate_to_sqlite.py first"

pytestmark = pytest.mark.skipif(not _diseases_db_ready(), reason=_SKIP_REASON)


class TestSQLiteMigration:
    """Test suite for SQLite migration"""

    @pytest.fixture
    def db_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        yield conn
        conn.close()

    def test_database_exists(self):
        """Test that SQLite database file exists"""
        assert Path(DB_PATH).exists(), "Database file does not exist"

    def test_schema_integrity(self, db_connection):
        """Test that all required tables exist"""
        cursor = db_connection.cursor()

        # Check main diseases table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='diseases'")
        assert cursor.fetchone(), "diseases table not found"

        # Check FTS5 table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='diseases_fts'")
        assert cursor.fetchone(), "diseases_fts table not found"

        # Check metadata table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='migration_metadata'")
        assert cursor.fetchone(), "migration_metadata table not found"

    def test_required_columns(self, db_connection):
        """Test that all required columns exist in diseases table"""
        cursor = db_connection.cursor()
        cursor.execute("PRAGMA table_info(diseases)")
        columns = {row["name"] for row in cursor.fetchall()}

        required_columns = {
            "id",
            "species",
            "name_en",
            "name_ja",
            "urgency",
            "pathophysiology_en",
            "pathophysiology_ja",
            "treatment_en",
            "treatment_ja",
            "diagnosis_en",
            "diagnosis_ja",
            "severity_score",
            "enriched_at",
        }

        missing = required_columns - columns
        assert not missing, f"Missing columns: {missing}"

    def test_data_count(self, db_connection):
        """Test that disease data was migrated"""
        cursor = db_connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM diseases")
        count = cursor.fetchone()[0]

        # Expected: ~6,449 diseases
        assert count >= 6400, f"Insufficient data: {count} diseases"
        assert count <= 6500, f"Unexpected data count: {count}"

    def test_species_distribution(self, db_connection):
        """Test that all species have data"""
        cursor = db_connection.cursor()
        cursor.execute("""
            SELECT species, COUNT(*) as count FROM diseases
            GROUP BY species ORDER BY count DESC
        """)

        species_counts = {row["species"]: row["count"] for row in cursor.fetchall()}

        # Check for major species
        assert "Dog" in species_counts, "Dog species missing"
        assert "Cat" in species_counts, "Cat species missing"
        assert "Horse" in species_counts, "Horse species missing"

        # Check counts are reasonable
        assert species_counts["Dog"] >= 300, "Dog diseases count too low"
        assert species_counts["Cat"] >= 300, "Cat diseases count too low"

    def test_urgency_distribution(self, db_connection):
        """Test urgency level distribution"""
        cursor = db_connection.cursor()
        cursor.execute("""
            SELECT urgency, COUNT(*) as count FROM diseases
            GROUP BY urgency
        """)

        urgency_counts = {row["urgency"]: row["count"] for row in cursor.fetchall()}

        # Check all urgency levels exist
        assert "emergency" in urgency_counts, "emergency urgency missing"
        assert "high" in urgency_counts, "high urgency missing"

        # Check reasonable distribution
        assert urgency_counts.get("emergency", 0) > 500, "emergency count too low"
        assert urgency_counts.get("high", 0) > 2000, "high count too low"


class TestDatabasePerformance:
    """Performance tests for SQLite queries"""

    @pytest.fixture
    def db_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        yield conn
        conn.close()

    def test_single_lookup_performance(self, db_connection):
        """Test single disease lookup performance (< 1ms expected)"""
        cursor = db_connection.cursor()

        # Warm up
        cursor.execute("SELECT * FROM diseases WHERE id = ?", ("cat_0001",))
        cursor.fetchone()

        # Measure
        times = []
        for _ in range(10):
            start = time.time()
            cursor.execute("SELECT * FROM diseases WHERE id = ?", ("cat_0001",))
            cursor.fetchone()
            elapsed = (time.time() - start) * 1000
            times.append(elapsed)

        avg_time = sum(times) / len(times)
        assert avg_time < 5, f"Single lookup too slow: {avg_time:.2f}ms"

    def test_species_filter_performance(self, db_connection):
        """Test species filter performance (< 5ms expected)"""
        cursor = db_connection.cursor()

        times = []
        for _ in range(5):
            start = time.time()
            cursor.execute(
                """
                SELECT id, name_en, name_ja FROM diseases
                WHERE species = ? LIMIT 100
            """,
                ("Dog",),
            )
            list(cursor.fetchall())
            elapsed = (time.time() - start) * 1000
            times.append(elapsed)

        avg_time = sum(times) / len(times)
        assert avg_time < 10, f"Species filter too slow: {avg_time:.2f}ms"

    def test_compound_query_performance(self, db_connection):
        """Test compound (species + urgency) query performance"""
        cursor = db_connection.cursor()

        times = []
        for _ in range(5):
            start = time.time()
            cursor.execute(
                """
                SELECT id, name_en FROM diseases
                WHERE species = ? AND urgency = ? LIMIT 100
            """,
                ("Dog", "emergency"),
            )
            list(cursor.fetchall())
            elapsed = (time.time() - start) * 1000
            times.append(elapsed)

        avg_time = sum(times) / len(times)
        assert avg_time < 10, f"Compound query too slow: {avg_time:.2f}ms"

    def test_index_usage(self, db_connection):
        """Test that indexes are being used"""
        cursor = db_connection.cursor()

        # Check index on species
        cursor.execute("EXPLAIN QUERY PLAN SELECT * FROM diseases WHERE species = 'Dog'")
        explain = cursor.fetchone()
        # Convert Row to dict for better string representation
        explain_str = str(dict(explain)) if explain else ""
        assert "SEARCH" in explain_str or "idx_species" in explain_str, f"Index not used: {explain_str}"


class TestBackwardCompatibility:
    """Test backward compatibility with existing API"""

    @pytest.fixture
    def db_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        yield conn
        conn.close()

    def test_disease_id_format(self, db_connection):
        """Test that disease IDs maintain expected format"""
        cursor = db_connection.cursor()
        cursor.execute("SELECT id FROM diseases LIMIT 10")

        for row in cursor.fetchall():
            disease_id = row["id"]
            # Format: species_NNNN (e.g., cat_0001)
            assert "_" in disease_id, f"Invalid disease ID format: {disease_id}"

    def test_name_fields_populated(self, db_connection):
        """Test that both EN and JA names are populated"""
        cursor = db_connection.cursor()
        cursor.execute("""
            SELECT COUNT(*) as count FROM diseases
            WHERE name_en IS NOT NULL AND name_ja IS NOT NULL
        """)

        count = cursor.fetchone()["count"]
        total = cursor.execute("SELECT COUNT(*) FROM diseases").fetchone()[0]

        # At least 99% should have both names
        assert count / total >= 0.99, "Missing EN/JA names"

    def test_treatment_fields_populated(self, db_connection):
        """Test that treatment fields are populated"""
        cursor = db_connection.cursor()
        cursor.execute("""
            SELECT COUNT(*) as count FROM diseases
            WHERE treatment_en IS NOT NULL AND treatment_ja IS NOT NULL
        """)

        count = cursor.fetchone()["count"]
        total = cursor.execute("SELECT COUNT(*) FROM diseases").fetchone()[0]

        # At least 95% should have treatment data
        assert count / total >= 0.95, f"Missing treatment fields: {count}/{total}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
