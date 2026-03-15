"""Database models and utilities for VetDict disease data.

This module defines SQLAlchemy models for storing disease data in SQLite,
replacing the hard-coded Python dictionaries in species/*_diseases.py files.
The Python files are kept as a fallback when the database is unavailable.
"""

from __future__ import annotations

import os
from typing import Any, Dict, List, Optional, Set

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Text

db = SQLAlchemy()

# Default database path (SQLite file next to app.py)
DEFAULT_DB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "vetdict_diseases.db",
)


def get_database_uri() -> str:
    """Return the SQLAlchemy database URI from env or default."""
    return os.getenv("DATABASE_URL", f"sqlite:///{DEFAULT_DB_PATH}")


# ---------------------------------------------------------------------------
# Association tables
# ---------------------------------------------------------------------------

disease_symptoms = db.Table(
    "disease_symptoms",
    db.Column("disease_id", db.Integer, db.ForeignKey("diseases.id"), primary_key=True),
    db.Column("symptom_id", db.String(100), primary_key=True),
)

disease_tests = db.Table(
    "disease_tests",
    db.Column("disease_id", db.Integer, db.ForeignKey("diseases.id"), primary_key=True),
    db.Column("test_id", db.String(100), primary_key=True),
    db.Column("sort_order", db.Integer, default=0),
)


# ---------------------------------------------------------------------------
# Models
# ---------------------------------------------------------------------------

class Disease(db.Model):  # type: ignore[name-defined]
    """A veterinary disease record."""

    __tablename__ = "diseases"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    species = db.Column(db.String(50), nullable=False, index=True)
    disease_key = db.Column(db.String(200), nullable=False, default="")
    name = db.Column(db.String(200), nullable=False)
    name_ja = db.Column(db.String(200), nullable=False, default="")
    category = db.Column(db.String(50), nullable=False, default="")
    description = db.Column(Text, default="")
    description_ja = db.Column(Text, default="")
    causes = db.Column(Text, default="")
    causes_ja = db.Column(Text, default="")
    pathophysiology = db.Column(Text, default="")
    pathophysiology_ja = db.Column(Text, default="")
    prevention = db.Column(Text, default="")
    prevention_ja = db.Column(Text, default="")
    treatment = db.Column(Text, default="")
    treatment_ja = db.Column(Text, default="")
    prognosis = db.Column(Text, default="")
    prognosis_ja = db.Column(Text, default="")
    urgency = db.Column(db.String(20), default="moderate")

    # Unique constraint using disease_key (original source ID) per species
    __table_args__ = (
        db.UniqueConstraint("species", "disease_key", name="uq_species_disease_key"),
    )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to the dictionary format expected by analyze_symptoms_generic."""
        # Fetch symptoms
        symptom_rows = db.session.execute(
            disease_symptoms.select().where(disease_symptoms.c.disease_id == self.id)
        ).fetchall()
        symptoms = {row.symptom_id for row in symptom_rows}

        # Fetch recommended tests (ordered)
        test_rows = db.session.execute(
            disease_tests.select()
            .where(disease_tests.c.disease_id == self.id)
            .order_by(disease_tests.c.sort_order)
        ).fetchall()
        tests = [row.test_id for row in test_rows]

        result: Dict[str, Any] = {
            "name": self.name,
            "name_ja": self.name_ja,
            "symptoms": symptoms,
            "description": self.description or "",
            "description_ja": self.description_ja or "",
            "urgency": self.urgency or "moderate",
            "recommended_tests": tests,
        }
        # Add optional text fields only if non-empty
        for field in ("causes", "causes_ja", "pathophysiology", "pathophysiology_ja",
                      "prevention", "prevention_ja", "treatment", "treatment_ja",
                      "prognosis", "prognosis_ja"):
            val = getattr(self, field, None)
            if val:
                result[field] = val
        return result


# ---------------------------------------------------------------------------
# Query helpers
# ---------------------------------------------------------------------------

def get_diseases_for_species(species: str) -> List[Dict[str, Any]]:
    """Load all diseases for a species from the database.

    Returns a list of disease dictionaries in the same format as the
    hard-coded DISEASES lists in species/*_diseases.py files.

    Raises RuntimeError if the database is not initialized.
    """
    diseases = Disease.query.filter_by(species=species).all()
    return [d.to_dict() for d in diseases]


def has_diseases_for_species(species: str) -> bool:
    """Check if the database has disease data for the given species."""
    try:
        count = Disease.query.filter_by(species=species).count()
        return count > 0
    except Exception:
        return False


# ---------------------------------------------------------------------------
# Init helper
# ---------------------------------------------------------------------------

def init_db(app):
    """Initialize the database with the Flask app."""
    uri = get_database_uri()
    app.config.setdefault("SQLALCHEMY_DATABASE_URI", uri)
    app.config.setdefault("SQLALCHEMY_TRACK_MODIFICATIONS", False)
    db.init_app(app)
    with app.app_context():
        db.create_all()
