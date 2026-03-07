"""
Tests for the database layer.

Tests cover:
- User CRUD (create, verify, get, update password)
- Session management (create, verify, delete)
- Dog CRUD (create, list, get, update, delete)
- Analysis storage (save, retrieve, list)
- Medical visit records
- Data isolation between users
"""

import importlib

import pytest


@pytest.fixture()
def db(tmp_path, monkeypatch):
    """Provide an isolated database module."""
    db_path = str(tmp_path / "test.db")
    monkeypatch.setenv("DATABASE_PATH", db_path)

    import api.database as db_mod
    importlib.reload(db_mod)
    return db_mod


def _uid(result):
    """Extract user_id from create_user result (returns dict with 'id')."""
    if isinstance(result, dict):
        return result["id"]
    return result


def _did(result):
    """Extract dog_id from create_dog result (returns dict with 'id')."""
    if isinstance(result, dict):
        return result["id"]
    return result


# ============================================================================
# User Operations
# ============================================================================


class TestUserOperations:
    def test_create_user(self, db):
        result = db.create_user("alice@example.com", "SecurePass123!")
        assert result is not None
        assert _uid(result) is not None

    def test_create_user_with_security_question(self, db):
        result = db.create_user(
            "bob@example.com", "Pass123!",
            name="Bob", security_question="Pet?", security_answer="Rex",
        )
        assert result is not None

    def test_create_duplicate_user(self, db):
        db.create_user("dup@example.com", "Pass123!")
        result = db.create_user("dup@example.com", "Pass456!")
        assert result is None

    def test_verify_user_correct(self, db):
        db.create_user("verify@example.com", "Correct123!")
        user = db.verify_user("verify@example.com", "Correct123!")
        assert user is not None
        assert user["email"] == "verify@example.com"

    def test_verify_user_wrong_password(self, db):
        db.create_user("wrong@example.com", "Correct123!")
        user = db.verify_user("wrong@example.com", "Wrong456!")
        assert user is None

    def test_verify_user_nonexistent(self, db):
        user = db.verify_user("noone@example.com", "Pass123!")
        assert user is None

    def test_get_user_by_email(self, db):
        db.create_user("get@example.com", "Pass123!", name="Getter")
        user = db.get_user_by_email("get@example.com")
        assert user is not None
        assert user["name"] == "Getter"

    def test_get_user_by_email_nonexistent(self, db):
        user = db.get_user_by_email("nonexistent@example.com")
        assert user is None

    def test_update_user_password(self, db):
        result = db.create_user("update@example.com", "OldPass123!")
        user_id = _uid(result)
        db.update_user_password(user_id, "NewPass456!")
        assert db.verify_user("update@example.com", "OldPass123!") is None
        assert db.verify_user("update@example.com", "NewPass456!") is not None

    def test_verify_security_answer(self, db):
        db.create_user(
            "sec@example.com", "Pass123!",
            security_question="Pet?", security_answer="Buddy",
        )
        result = db.verify_security_answer("sec@example.com", "Buddy")
        assert result is not None

    def test_verify_security_answer_wrong(self, db):
        db.create_user(
            "sec2@example.com", "Pass123!",
            security_question="Pet?", security_answer="Buddy",
        )
        result = db.verify_security_answer("sec2@example.com", "WrongAnswer")
        assert result is None or result is False


# ============================================================================
# Session Management
# ============================================================================


class TestSessionManagement:
    def test_create_session(self, db):
        user_id = _uid(db.create_user("session@example.com", "Pass123!"))
        token = db.create_session(user_id)
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 10

    def test_verify_session(self, db):
        user_id = _uid(db.create_user("vsess@example.com", "Pass123!"))
        token = db.create_session(user_id)
        user = db.verify_session(token)
        assert user is not None
        assert user["id"] == user_id

    def test_verify_invalid_token(self, db):
        user = db.verify_session("invalid-token-xyz")
        assert user is None

    def test_delete_session(self, db):
        user_id = _uid(db.create_user("delsess@example.com", "Pass123!"))
        token = db.create_session(user_id)
        db.delete_session(token)
        user = db.verify_session(token)
        assert user is None

    def test_multiple_sessions(self, db):
        user_id = _uid(db.create_user("multi@example.com", "Pass123!"))
        token1 = db.create_session(user_id)
        token2 = db.create_session(user_id)
        assert token1 != token2
        assert db.verify_session(token1) is not None
        assert db.verify_session(token2) is not None


# ============================================================================
# Dog CRUD
# ============================================================================


class TestDogCRUD:
    def test_create_dog(self, db):
        user_id = _uid(db.create_user("dogowner@example.com", "Pass123!"))
        dog_id = _did(db.create_dog(user_id, "Rex", "122_labrador_retriever"))
        assert dog_id is not None

    def test_create_dog_with_details(self, db):
        user_id = _uid(db.create_user("detail@example.com", "Pass123!"))
        dog_id = _did(db.create_dog(
            user_id, "Bella", "111_golden_retriever",
            birth_date="2023-06-15", weight=25.0, gender="female", notes="Friendly",
        ))
        assert dog_id is not None

    def test_get_dogs_by_user(self, db):
        user_id = _uid(db.create_user("list@example.com", "Pass123!"))
        db.create_dog(user_id, "Dog1", "122_labrador_retriever")
        db.create_dog(user_id, "Dog2", "166_german_shepherd")
        dogs = db.get_dogs_by_user(user_id)
        assert len(dogs) == 2

    def test_get_dogs_empty(self, db):
        user_id = _uid(db.create_user("empty@example.com", "Pass123!"))
        dogs = db.get_dogs_by_user(user_id)
        assert len(dogs) == 0

    def test_get_dog_by_id(self, db):
        user_id = _uid(db.create_user("getdog@example.com", "Pass123!"))
        dog_id = _did(db.create_dog(user_id, "Fetch", "257_shiba_inu"))
        dog = db.get_dog_by_id(dog_id, user_id)
        assert dog is not None
        assert dog["name"] == "Fetch"

    def test_get_dog_wrong_user(self, db):
        user1 = _uid(db.create_user("user1@example.com", "Pass123!"))
        user2 = _uid(db.create_user("user2@example.com", "Pass123!"))
        dog_id = _did(db.create_dog(user1, "Private", "122_labrador_retriever"))
        dog = db.get_dog_by_id(dog_id, user2)
        assert dog is None

    def test_update_dog(self, db):
        user_id = _uid(db.create_user("updog@example.com", "Pass123!"))
        dog_id = _did(db.create_dog(user_id, "OldName", "122_labrador_retriever"))
        db.update_dog(dog_id, user_id, name="NewName", weight=30.0)
        dog = db.get_dog_by_id(dog_id, user_id)
        assert dog["name"] == "NewName"

    def test_delete_dog(self, db):
        user_id = _uid(db.create_user("deldog@example.com", "Pass123!"))
        dog_id = _did(db.create_dog(user_id, "Goodbye", "172d_poodle_toy"))
        db.delete_dog(dog_id, user_id)
        dog = db.get_dog_by_id(dog_id, user_id)
        assert dog is None


# ============================================================================
# Analysis Storage
# ============================================================================


class TestAnalysisStorage:
    def test_save_analysis(self, db):
        user_id = _uid(db.create_user("analysis@example.com", "Pass123!"))
        dog_id = _did(db.create_dog(user_id, "Analyzed", "122_labrador_retriever"))
        results = {"overall_score": 85.0, "grade": "A", "structure_score": 82.0}
        analysis_id = db.save_analysis(dog_id, user_id, 3.5, False, results)
        assert analysis_id is not None

    def test_get_analyses_by_dog(self, db):
        user_id = _uid(db.create_user("analyses@example.com", "Pass123!"))
        dog_id = _did(db.create_dog(user_id, "Multi", "166_german_shepherd"))
        for i in range(3):
            db.save_analysis(dog_id, user_id, 2.0 + i, False, {"score": 80 + i})
        analyses = db.get_analyses_by_dog(dog_id, user_id)
        assert len(analyses) == 3

    def test_get_analysis_by_id(self, db):
        user_id = _uid(db.create_user("single@example.com", "Pass123!"))
        dog_id = _did(db.create_dog(user_id, "Single", "111_golden_retriever"))
        aid = db.save_analysis(dog_id, user_id, 4.0, True, {"grade": "A+"})
        analysis = db.get_analysis_by_id(aid, user_id)
        assert analysis is not None

    def test_get_recent_analyses(self, db):
        user_id = _uid(db.create_user("recent@example.com", "Pass123!"))
        dog_id = _did(db.create_dog(user_id, "Recent", "122_labrador_retriever"))
        for i in range(5):
            db.save_analysis(dog_id, user_id, 3.0, False, {"score": 70 + i})
        recent = db.get_recent_analyses_by_user(user_id, limit=3)
        assert len(recent) <= 3


# ============================================================================
# Medical Visits
# ============================================================================


class TestMedicalVisits:
    def test_create_medical_visit(self, db):
        user_id = _uid(db.create_user("vet@example.com", "Pass123!"))
        dog_id = _did(db.create_dog(user_id, "Patient", "122_labrador_retriever"))
        visit_id = db.create_medical_visit(user_id, {
            "dog_id": dog_id,
            "visit_date": "2024-01-15",
            "chief_complaint": "Limping",
        })
        assert visit_id is not None

    def test_get_medical_visit(self, db):
        user_id = _uid(db.create_user("getvisit@example.com", "Pass123!"))
        dog_id = _did(db.create_dog(user_id, "Checkup", "166_german_shepherd"))
        visit_id = db.create_medical_visit(user_id, {
            "dog_id": dog_id,
            "visit_date": "2024-02-01",
            "chief_complaint": "Annual checkup",
        })
        visit = db.get_medical_visit(visit_id, user_id)
        assert visit is not None

    def test_get_medical_visits_by_dog(self, db):
        user_id = _uid(db.create_user("dogvisits@example.com", "Pass123!"))
        dog_id = _did(db.create_dog(user_id, "Frequent", "111_golden_retriever"))
        for i in range(3):
            db.create_medical_visit(user_id, {
                "dog_id": dog_id,
                "visit_date": f"2024-0{i+1}-01",
                "chief_complaint": f"Visit {i+1}",
            })
        visits = db.get_medical_visits_by_dog(dog_id, user_id)
        assert len(visits) == 3
