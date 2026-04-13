#!/usr/bin/env python3
"""
Flask API integration for SQLite diseases database

Provides optimized query methods for the new SQLite schema
"""

import json
import logging
import sqlite3
from pathlib import Path
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)

# Use the migrated SQLite database
DB_PATH = str(Path(__file__).resolve().parent.parent / 'diseases.db')


class DiseaseDatabase:
    """High-performance SQLite query interface for diseases"""

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    def _get_connection(self):
        """Get a SQLite connection with optimizations"""
        conn = sqlite3.connect(self.db_path, timeout=10.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        conn.execute("PRAGMA cache_size=-64000")
        return conn

    def get_disease_by_id(self, disease_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a single disease by ID (< 1ms)"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT * FROM diseases WHERE id = ?""",
                (disease_id,)
            )
            row = cursor.fetchone()
            if row:
                return dict(row)
        finally:
            conn.close()
        return None

    def search_by_species(self, species: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all diseases for a species (< 5ms with index)"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT id, name_en, name_ja, urgency, severity_score
                   FROM diseases WHERE species = ? LIMIT ?""",
                (species, limit)
            )
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()

    def search_by_urgency(self, urgency: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get diseases filtered by urgency level (< 5ms with index)"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT id, name_en, name_ja, species, severity_score
                   FROM diseases WHERE urgency = ? LIMIT ?""",
                (urgency, limit)
            )
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()

    def search_by_species_and_urgency(
        self, species: str, urgency: str, limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Fast compound query (< 5ms with compound index)"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT id, name_en, name_ja, severity_score
                   FROM diseases WHERE species = ? AND urgency = ? LIMIT ?""",
                (species, urgency, limit)
            )
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()

    def full_text_search(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Full-text search using FTS5 (< 10ms)"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT d.id, d.name_en, d.name_ja, d.species, d.urgency
                   FROM diseases d
                   WHERE d.id IN (
                       SELECT id FROM diseases_fts WHERE diseases_fts MATCH ?
                   ) LIMIT ?""",
                (query, limit)
            )
            return [dict(row) for row in cursor.fetchall()]
        finally:
            conn.close()

    def get_species_stats(self) -> Dict[str, int]:
        """Get disease count per species"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT species, COUNT(*) as count
                   FROM diseases GROUP BY species ORDER BY species"""
            )
            return {row['species']: row['count'] for row in cursor.fetchall()}
        finally:
            conn.close()

    def get_urgency_stats(self) -> Dict[str, int]:
        """Get disease count per urgency level"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT urgency, COUNT(*) as count
                   FROM diseases GROUP BY urgency ORDER BY urgency"""
            )
            return {row['urgency']: row['count'] for row in cursor.fetchall()}
        finally:
            conn.close()

    def get_total_disease_count(self) -> int:
        """Get total number of diseases in database"""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as count FROM diseases")
            return cursor.fetchone()['count']
        finally:
            conn.close()


# Global instance
disease_db = DiseaseDatabase()
