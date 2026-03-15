"""Tests for the disease database layer (api/database.py, api/disease_loader.py)."""

from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path
from typing import Any, Dict, List

import pytest

# Ensure project root is on sys.path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from flask import Flask


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def app_with_db(tmp_path):
    """Create a Flask app with a temporary SQLite database."""
    db_path = str(tmp_path / "test_diseases.db")
    os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"

    app = Flask(__name__)
    app.config["TESTING"] = True

    from api.database import db, init_db, Disease, disease_symptoms, disease_tests
    init_db(app)

    with app.app_context():
        db.create_all()
        yield app, db

    # Cleanup
    os.environ.pop("DATABASE_URL", None)


@pytest.fixture()
def sample_diseases() -> List[Dict[str, Any]]:
    """Sample disease data matching the Python dict format."""
    return [
        {
            "name": "Test Disease A",
            "name_ja": "テスト疾患A",
            "symptoms": {"fever", "coughing", "lethargy"},
            "description": "A test disease for unit testing.",
            "description_ja": "ユニットテスト用テスト疾患。",
            "causes": "Test causes",
            "causes_ja": "テスト原因",
            "treatment": "Test treatment",
            "treatment_ja": "テスト治療",
            "urgency": "moderate",
            "recommended_tests": ["blood_test", "xray"],
        },
        {
            "name": "Test Disease B",
            "name_ja": "テスト疾患B",
            "symptoms": {"vomiting", "diarrhea"},
            "description": "Another test disease.",
            "description_ja": "別のテスト疾患。",
            "urgency": "high",
            "recommended_tests": ["ultrasound"],
        },
    ]


# ---------------------------------------------------------------------------
# Tests: Database models
# ---------------------------------------------------------------------------

class TestDiseaseModel:
    """Tests for the Disease SQLAlchemy model."""

    def test_create_disease(self, app_with_db):
        app, db = app_with_db
        from api.database import Disease

        with app.app_context():
            d = Disease(
                species="cat",
                name="Test Feline Disease",
                name_ja="テスト猫疾患",
                urgency="high",
                description="A test disease",
            )
            db.session.add(d)
            db.session.commit()

            assert d.id is not None
            fetched = Disease.query.filter_by(name="Test Feline Disease").first()
            assert fetched is not None
            assert fetched.species == "cat"
            assert fetched.urgency == "high"

    def test_unique_constraint(self, app_with_db):
        app, db = app_with_db
        from api.database import Disease
        from sqlalchemy.exc import IntegrityError

        with app.app_context():
            d1 = Disease(species="dog", name="Parvo", name_ja="パルボ")
            db.session.add(d1)
            db.session.commit()

            d2 = Disease(species="dog", name="Parvo", name_ja="パルボ2")
            db.session.add(d2)
            with pytest.raises(IntegrityError):
                db.session.commit()
            db.session.rollback()

    def test_same_name_different_species(self, app_with_db):
        app, db = app_with_db
        from api.database import Disease

        with app.app_context():
            d1 = Disease(species="dog", name="Pneumonia", name_ja="犬肺炎")
            d2 = Disease(species="cat", name="Pneumonia", name_ja="猫肺炎")
            db.session.add_all([d1, d2])
            db.session.commit()

            assert Disease.query.filter_by(name="Pneumonia").count() == 2

    def test_to_dict(self, app_with_db):
        app, db = app_with_db
        from api.database import Disease, disease_symptoms, disease_tests

        with app.app_context():
            d = Disease(
                species="cat",
                name="URI",
                name_ja="上部呼吸器感染症",
                description="Upper respiratory infection",
                description_ja="上気道感染",
                causes="Virus",
                urgency="moderate",
            )
            db.session.add(d)
            db.session.flush()

            # Add symptoms
            for symptom in ["coughing", "sneezing", "fever"]:
                db.session.execute(
                    disease_symptoms.insert().values(disease_id=d.id, symptom_id=symptom)
                )

            # Add tests
            for i, test in enumerate(["xray", "blood_test"]):
                db.session.execute(
                    disease_tests.insert().values(disease_id=d.id, test_id=test, sort_order=i)
                )

            db.session.commit()

            result = d.to_dict()
            assert result["name"] == "URI"
            assert result["name_ja"] == "上部呼吸器感染症"
            assert result["symptoms"] == {"coughing", "sneezing", "fever"}
            assert result["recommended_tests"] == ["xray", "blood_test"]
            assert result["urgency"] == "moderate"
            assert result["causes"] == "Virus"


# ---------------------------------------------------------------------------
# Tests: Query helpers
# ---------------------------------------------------------------------------

class TestQueryHelpers:
    """Tests for get_diseases_for_species / has_diseases_for_species."""

    def test_has_diseases_empty(self, app_with_db):
        app, _ = app_with_db
        from api.database import has_diseases_for_species

        with app.app_context():
            assert has_diseases_for_species("cat") is False

    def test_has_diseases_with_data(self, app_with_db):
        app, db = app_with_db
        from api.database import Disease, has_diseases_for_species

        with app.app_context():
            db.session.add(Disease(species="cat", name="URI", name_ja="URI"))
            db.session.commit()
            assert has_diseases_for_species("cat") is True
            assert has_diseases_for_species("dog") is False

    def test_get_diseases_for_species(self, app_with_db):
        app, db = app_with_db
        from api.database import Disease, disease_symptoms, get_diseases_for_species

        with app.app_context():
            d = Disease(species="rabbit", name="GI Stasis", name_ja="消化管うっ滞", urgency="high")
            db.session.add(d)
            db.session.flush()
            db.session.execute(
                disease_symptoms.insert().values(disease_id=d.id, symptom_id="appetite_loss")
            )
            db.session.commit()

            diseases = get_diseases_for_species("rabbit")
            assert len(diseases) == 1
            assert diseases[0]["name"] == "GI Stasis"
            assert "appetite_loss" in diseases[0]["symptoms"]


# ---------------------------------------------------------------------------
# Tests: Disease loader (DB-first, Python-fallback)
# ---------------------------------------------------------------------------

class TestDiseaseLoader:
    """Tests for api/disease_loader.py."""

    def test_fallback_when_no_db(self):
        """Without a Flask app context, load_diseases should use fallback."""
        from api.disease_loader import load_diseases, invalidate_cache
        invalidate_cache()

        fallback = [{"name": "Fallback Disease", "symptoms": {"fever"}}]
        result = load_diseases("unknown_species", fallback)
        assert result == fallback

    def test_loads_from_db_when_available(self, app_with_db):
        """With a DB containing data, load_diseases should return DB data."""
        app, db = app_with_db
        from api.database import Disease, disease_symptoms
        from api.disease_loader import load_diseases, invalidate_cache
        invalidate_cache()

        with app.app_context():
            d = Disease(species="test_sp", name="DB Disease", name_ja="DB疾患", urgency="low")
            db.session.add(d)
            db.session.flush()
            db.session.execute(
                disease_symptoms.insert().values(disease_id=d.id, symptom_id="fever")
            )
            db.session.commit()

            fallback = [{"name": "Fallback", "symptoms": {"cough"}}]
            result = load_diseases("test_sp", fallback)

            assert len(result) == 1
            assert result[0]["name"] == "DB Disease"

    def test_cache_invalidation(self, app_with_db):
        """invalidate_cache should clear cached data."""
        app, db = app_with_db
        from api.disease_loader import load_diseases, invalidate_cache, _cache
        invalidate_cache()

        with app.app_context():
            fallback = [{"name": "Cached"}]
            load_diseases("cache_test", fallback)
            assert "cache_test" in _cache

            invalidate_cache("cache_test")
            assert "cache_test" not in _cache

    def test_cache_invalidation_all(self, app_with_db):
        app, _ = app_with_db
        from api.disease_loader import load_diseases, invalidate_cache, _cache
        invalidate_cache()

        with app.app_context():
            load_diseases("sp1", [{"name": "A"}])
            load_diseases("sp2", [{"name": "B"}])
            assert "sp1" in _cache
            assert "sp2" in _cache

            invalidate_cache()
            assert len(_cache) == 0


# ---------------------------------------------------------------------------
# Tests: Seed script
# ---------------------------------------------------------------------------

class TestSeedScript:
    """Tests for seed_db.py."""

    def test_seed_species(self, app_with_db):
        """Test seeding a single species from Python data."""
        app, db = app_with_db
        from api.database import Disease

        with app.app_context():
            # Import and run seed for cat
            from seed_db import seed_species
            count = seed_species("cat", "api.species.cat_diseases", "DISEASES")
            assert count > 0

            # Verify data
            cat_diseases = Disease.query.filter_by(species="cat").all()
            assert len(cat_diseases) == count
            assert cat_diseases[0].name  # has a name

    def test_seed_idempotent(self, app_with_db):
        """Seeding twice should not duplicate data."""
        app, db = app_with_db
        from api.database import Disease

        with app.app_context():
            from seed_db import seed_species
            count1 = seed_species("cat", "api.species.cat_diseases", "DISEASES")
            count2 = seed_species("cat", "api.species.cat_diseases", "DISEASES")

            assert count1 > 0
            assert count2 == 0  # No new records added

    def test_disease_data_integrity(self, app_with_db):
        """Verify that seeded data matches the Python source."""
        app, db = app_with_db

        with app.app_context():
            from seed_db import seed_species
            seed_species("cat", "api.species.cat_diseases", "DISEASES")

            from api.database import get_diseases_for_species
            from api.species.cat_diseases import DISEASES as CAT_DISEASES

            db_diseases = get_diseases_for_species("cat")
            db_names = {d["name"] for d in db_diseases}
            py_names = {d["name"] for d in CAT_DISEASES}

            # All Python diseases should be in the DB
            assert py_names == db_names

            # Spot-check first disease
            first_py = CAT_DISEASES[0]
            first_db = next(d for d in db_diseases if d["name"] == first_py["name"])
            assert first_db["name_ja"] == first_py["name_ja"]
            assert first_db["urgency"] == first_py["urgency"]
            assert first_db["symptoms"] == first_py["symptoms"]
            assert first_db["recommended_tests"] == first_py["recommended_tests"]
