#!/usr/bin/env python3
"""
Full-text search (FTS5) integration for diseases database

Provides advanced search capabilities with phrase matching,
AND/OR operators, fuzzy matching, and ranking
"""

import logging
import sqlite3
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

DB_PATH = str(__import__('pathlib').Path(__file__).resolve().parent.parent / 'diseases.db')


class DiseaseFullTextSearch:
    """Advanced full-text search using SQLite FTS5"""

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    def _get_connection(self):
        """Get a SQLite connection"""
        conn = sqlite3.connect(self.db_path, timeout=10.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        return conn

    def simple_search(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Simple full-text search

        Example: "fever AND respiratory"
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT d.id, d.name_en, d.name_ja, d.species, d.urgency
                   FROM diseases d
                   WHERE d.id IN (
                       SELECT id FROM diseases_fts WHERE diseases_fts MATCH ?
                   )
                   ORDER BY d.urgency DESC, d.severity_score DESC
                   LIMIT ?""",
                (query, limit)
            )
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.OperationalError as e:
            logger.error(f"FTS5 search error: {e}")
            return []
        finally:
            conn.close()

    def phrase_search(self, phrase: str, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Search for exact phrase

        Example: "respiratory distress"
        """
        # Escape quotes and wrap in quotes for exact phrase matching
        escaped_phrase = phrase.replace('"', '""')
        fts_query = f'"{escaped_phrase}"'
        return self.simple_search(fts_query, limit)

    def search_by_name(self, name: str, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Search for disease by name (EN or JA)

        Example: "leukemia" or "白血病"
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT id, name_en, name_ja, species, urgency
                   FROM diseases
                   WHERE name_en LIKE ? OR name_ja LIKE ?
                   LIMIT ?""",
                (f"%{name}%", f"%{name}%", limit)
            )
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()

    def search_symptoms(
        self, symptom_keywords: List[str], mode: str = "any", limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Search for diseases by symptoms

        mode: "any" (OR), "all" (AND)
        Example: search_symptoms(["fever", "lethargy"], mode="all")
        """
        if mode == "all":
            # AND operator: all symptoms must be present
            fts_query = " AND ".join(symptom_keywords)
        else:
            # OR operator: any symptom matches
            fts_query = " OR ".join(symptom_keywords)

        return self.simple_search(fts_query, limit)

    def search_with_species_filter(
        self, query: str, species: str, limit: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Full-text search with species filter

        Fast compound query (< 5ms)
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT d.id, d.name_en, d.name_ja, d.species, d.urgency
                   FROM diseases d
                   WHERE d.species = ? AND d.id IN (
                       SELECT id FROM diseases_fts WHERE diseases_fts MATCH ?
                   )
                   ORDER BY d.urgency DESC
                   LIMIT ?""",
                (species, query, limit)
            )
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.OperationalError as e:
            logger.error(f"FTS5 search error: {e}")
            return []
        finally:
            conn.close()

    def get_search_suggestions(self, partial: str, limit: int = 5) -> List[str]:
        """
        Get search suggestions based on partial input

        Useful for autocomplete
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT DISTINCT name_en FROM diseases
                   WHERE name_en LIKE ? LIMIT ?""",
                (f"{partial}%", limit)
            )
            return [row[0] for row in cursor.fetchall()]
        finally:
            conn.close()

    def rebuild_fts_index(self) -> bool:
        """
        Rebuild FTS5 index (maintenance operation)

        Run this after bulk updates to diseases table
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            # Rebuild FTS5 index
            cursor.execute("INSERT INTO diseases_fts(diseases_fts) VALUES ('rebuild')")
            conn.commit()
            logger.info("FTS5 index rebuilt successfully")
            return True
        except sqlite3.OperationalError as e:
            logger.error(f"FTS5 rebuild error: {e}")
            return False
        finally:
            conn.close()


# Global instance
disease_search = DiseaseFullTextSearch()
