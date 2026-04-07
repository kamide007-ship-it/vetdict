"""Tests for the SQLite database layer and admin API."""

import json
import os

import pytest

os.environ.setdefault("SECRET_KEY", "test-key")
os.environ.setdefault("FLASK_DEBUG", "1")

from api.database import (
    count_diseases,
    delete_disease,
    get_all_drugs,
    get_connection,
    get_disease_by_id,
    get_diseases_by_species,
    get_drug_by_id,
    get_symptoms_by_species,
    init_db,
    upsert_disease,
    upsert_drug,
    upsert_symptom,
)


@pytest.fixture()
def db_path(tmp_path):
    path = str(tmp_path / "test.db")
    init_db(path)
    return path


class TestDatabaseSchema:
    def test_init_creates_tables(self, db_path):
        with get_connection(db_path) as conn:
            tables = [
                r[0]
                for r in conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
                ).fetchall()
            ]
        assert "diseases" in tables
        assert "drugs" in tables
        assert "symptoms" in tables
        assert "drug_species_info" in tables

    def test_init_is_idempotent(self, db_path):
        init_db(db_path)
        init_db(db_path)  # Should not raise


class TestDiseaseOperations:
    SAMPLE_DISEASE = {
        "id": "test_001",
        "species": "dog",
        "name": "Test Disease",
        "name_ja": "テスト疾患",
        "description": "A test disease",
        "urgency": "moderate",
        "symptoms": {"fever", "lethargy"},
        "recommended_tests": ["blood_test", "xray"],
    }

    def test_upsert_and_get(self, db_path):
        with get_connection(db_path) as conn:
            upsert_disease(conn, self.SAMPLE_DISEASE)
            result = get_disease_by_id(conn, "test_001")

        assert result is not None
        assert result["name"] == "Test Disease"
        assert result["species"] == "dog"
        assert set(json.loads(result["symptoms"])) == {"fever", "lethargy"}

    def test_get_nonexistent_returns_none(self, db_path):
        with get_connection(db_path) as conn:
            result = get_disease_by_id(conn, "nonexistent")
        assert result is None

    def test_upsert_updates_existing(self, db_path):
        with get_connection(db_path) as conn:
            upsert_disease(conn, self.SAMPLE_DISEASE)
            updated = {**self.SAMPLE_DISEASE, "name": "Updated Disease"}
            upsert_disease(conn, updated)
            result = get_disease_by_id(conn, "test_001")
        assert result["name"] == "Updated Disease"

    def test_get_by_species(self, db_path):
        with get_connection(db_path) as conn:
            upsert_disease(conn, self.SAMPLE_DISEASE)
            upsert_disease(conn, {**self.SAMPLE_DISEASE, "id": "test_002", "species": "cat"})
            dogs = get_diseases_by_species(conn, "dog")
            cats = get_diseases_by_species(conn, "cat")
        assert len(dogs) == 1
        assert len(cats) == 1
        assert dogs[0]["species"] == "dog"

    def test_delete_disease(self, db_path):
        with get_connection(db_path) as conn:
            upsert_disease(conn, self.SAMPLE_DISEASE)
            deleted = delete_disease(conn, "test_001")
            result = get_disease_by_id(conn, "test_001")
        assert deleted is True
        assert result is None

    def test_delete_nonexistent_returns_false(self, db_path):
        with get_connection(db_path) as conn:
            deleted = delete_disease(conn, "nonexistent")
        assert deleted is False

    def test_count_diseases(self, db_path):
        with get_connection(db_path) as conn:
            upsert_disease(conn, self.SAMPLE_DISEASE)
            upsert_disease(conn, {**self.SAMPLE_DISEASE, "id": "test_002"})
            upsert_disease(conn, {**self.SAMPLE_DISEASE, "id": "test_003", "species": "cat"})
            stats = count_diseases(conn)
        assert stats["total"] == 3
        assert stats["by_species"]["dog"] == 2
        assert stats["by_species"]["cat"] == 1


class TestDrugOperations:
    SAMPLE_DRUG = {
        "id": "amoxicillin",
        "name": "Amoxicillin",
        "name_ja": "アモキシシリン",
        "category": "antibiotics",
        "mechanism": "Beta-lactam antibiotic",
        "mechanism_ja": "β-ラクタム系抗生物質",
        "contraindications": "Penicillin allergy",
        "contraindications_ja": "ペニシリンアレルギー",
        "side_effects": ["GI upset", "diarrhea"],
        "side_effects_ja": ["消化器症状", "下痢"],
        "species_info": {
            "dog": {"safe": True, "dosage": "10-20 mg/kg", "dosage_ja": "10-20 mg/kg", "notes": "Safe", "notes_ja": "安全"},
            "rabbit": {"safe": False, "dosage": "N/A", "dosage_ja": "使用不可", "notes": "Contraindicated", "notes_ja": "禁忌"},
        },
    }

    def test_upsert_and_get(self, db_path):
        with get_connection(db_path) as conn:
            upsert_drug(conn, self.SAMPLE_DRUG)
            result = get_drug_by_id(conn, "amoxicillin")
        assert result is not None
        assert result["name"] == "Amoxicillin"
        assert "dog" in result["species_info"]
        assert result["species_info"]["rabbit"]["safe"] == 0

    def test_get_all_drugs(self, db_path):
        with get_connection(db_path) as conn:
            upsert_drug(conn, self.SAMPLE_DRUG)
            drugs = get_all_drugs(conn)
        assert len(drugs) == 1


class TestSymptomOperations:
    def test_upsert_and_get(self, db_path):
        with get_connection(db_path) as conn:
            upsert_symptom(conn, "dog_fever", "Fever", "発熱", "dog", 1.2)
            upsert_symptom(conn, "dog_lethargy", "Lethargy", "元気消失", "dog")
            symptoms = get_symptoms_by_species(conn, "dog")
        assert len(symptoms) == 2
        assert symptoms[0]["name_en"] == "Fever"


class TestAdminAPI:
    @pytest.fixture()
    def client(self, db_path, monkeypatch):
        import api.database
        monkeypatch.setattr(api.database, "DB_PATH", db_path)
        from api.vetdict_api import app
        app.config["TESTING"] = True
        with app.test_client() as c:
            yield c

    def test_list_diseases_empty(self, client):
        resp = client.get("/api/admin/diseases")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["success"] is True
        assert data["count"] == 0

    def test_create_and_get_disease(self, client):
        disease = {"id": "test_001", "species": "dog", "name": "Test", "name_ja": "テスト"}
        resp = client.post("/api/admin/diseases", json=disease)
        assert resp.status_code == 201

        resp = client.get("/api/admin/diseases/test_001")
        assert resp.status_code == 200
        assert resp.get_json()["disease"]["name"] == "Test"

    def test_update_disease(self, client):
        client.post("/api/admin/diseases", json={"id": "test_001", "species": "dog", "name": "Old", "name_ja": "旧"})
        resp = client.put("/api/admin/diseases/test_001", json={"name": "New"})
        assert resp.status_code == 200

        resp = client.get("/api/admin/diseases/test_001")
        assert resp.get_json()["disease"]["name"] == "New"

    def test_delete_disease(self, client):
        client.post("/api/admin/diseases", json={"id": "test_001", "species": "dog", "name": "X", "name_ja": "X"})
        resp = client.delete("/api/admin/diseases/test_001")
        assert resp.status_code == 200
        assert resp.get_json()["success"] is True

        resp = client.get("/api/admin/diseases/test_001")
        assert resp.status_code == 404

    def test_disease_stats(self, client):
        client.post("/api/admin/diseases", json={"id": "d1", "species": "dog", "name": "A", "name_ja": "A"})
        client.post("/api/admin/diseases", json={"id": "d2", "species": "cat", "name": "B", "name_ja": "B"})
        resp = client.get("/api/admin/diseases/stats")
        data = resp.get_json()
        assert data["total"] == 2
        assert data["by_species"]["dog"] == 1

    def test_create_disease_missing_fields(self, client):
        resp = client.post("/api/admin/diseases", json={"name": "No ID"})
        assert resp.status_code == 400

    def test_drug_crud(self, client):
        drug = {"id": "test_drug", "name": "Test Drug", "name_ja": "テスト薬"}
        resp = client.post("/api/admin/drugs", json=drug)
        assert resp.status_code == 201

        resp = client.get("/api/admin/drugs/test_drug")
        assert resp.status_code == 200
        assert resp.get_json()["drug"]["name"] == "Test Drug"

    def test_bulk_import(self, client):
        diseases = [
            {"id": f"bulk_{i}", "species": "dog", "name": f"Disease {i}", "name_ja": f"疾患{i}"}
            for i in range(5)
        ]
        resp = client.post("/api/admin/import", json={"diseases": diseases})
        assert resp.status_code == 201
        assert resp.get_json()["imported"] == 5
