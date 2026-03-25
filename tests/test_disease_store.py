"""Tests for the disease_store data access layer and diseases API blueprint."""

import os

import pytest

os.environ.setdefault("SECRET_KEY", "test-key")
os.environ.setdefault("FLASK_DEBUG", "1")

from api.database import get_connection, init_db, upsert_disease, upsert_symptom
from api.disease_store import (
    get_disease_detail,
    get_diseases_by_symptom,
    get_species_stats,
    get_symptoms_for_species,
    get_urgency_by_species,
    get_urgency_stats,
    invalidate_cache,
    list_diseases,
    search_diseases,
)


@pytest.fixture()
def db_path(tmp_path, monkeypatch):
    """Create a temporary SQLite database with sample data."""
    path = str(tmp_path / "test_store.db")
    init_db(path)
    monkeypatch.setattr("api.disease_store.get_connection", lambda: get_connection.__wrapped__(path))
    # Patch get_connection to use the temp path via a context manager wrapper
    import contextlib

    @contextlib.contextmanager
    def _patched_conn():
        with get_connection(path) as conn:
            yield conn

    monkeypatch.setattr("api.disease_store.get_connection", _patched_conn)

    with get_connection(path) as conn:
        # Insert sample diseases
        upsert_disease(conn, {
            "id": "cat_0001",
            "species": "cat",
            "name": "Feline Asthma",
            "name_ja": "猫喘息",
            "description": "Chronic airway disease",
            "treatment": "Corticosteroids and bronchodilators",
            "treatment_ja": "コルチコステロイドと気管支拡張薬",
            "prevention": "Reduce airborne irritants",
            "prevention_ja": "空気中の刺激物を減らす",
            "prognosis": "Manageable long term",
            "prognosis_ja": "長期管理可能",
            "urgency": "high",
            "symptoms": {"coughing", "wheezing"},
            "recommended_tests": ["chest_xray", "cbc"],
        })
        upsert_disease(conn, {
            "id": "cat_0002",
            "species": "cat",
            "name": "Feline Pneumonia",
            "name_ja": "猫肺炎",
            "description": "Lung infection",
            "treatment": "Antibiotics and oxygen therapy",
            "urgency": "high",
            "symptoms": {"coughing", "fever"},
            "recommended_tests": ["chest_xray"],
        })
        upsert_disease(conn, {
            "id": "dog_0001",
            "species": "dog",
            "name": "Canine Parvovirus",
            "name_ja": "犬パルボウイルス感染症",
            "description": "Viral gastroenteritis",
            "treatment": "Supportive care",
            "urgency": "emergency",
            "symptoms": {"vomiting", "diarrhea"},
            "recommended_tests": ["parvo_snap"],
        })
        # Insert sample symptoms
        upsert_symptom(conn, "cat_coughing", "Coughing", "咳", "cat")
        upsert_symptom(conn, "cat_wheezing", "Wheezing", "喘鳴", "cat")
        upsert_symptom(conn, "cat_fever", "Fever", "発熱", "cat")

    invalidate_cache()
    return path


class TestGetSpeciesStats:
    def test_returns_species_with_counts(self, db_path):
        result = get_species_stats()
        assert "species" in result
        assert "total_diseases" in result
        assert result["total_diseases"] == 3

        cat_stats = next((s for s in result["species"] if s["id"] == "cat"), None)
        assert cat_stats is not None
        assert cat_stats["diseases"] == 2
        assert cat_stats["name"] == "猫"
        assert cat_stats["nameEn"] == "Cat"

        dog_stats = next((s for s in result["species"] if s["id"] == "dog"), None)
        assert dog_stats is not None
        assert dog_stats["diseases"] == 1


class TestGetUrgencyStats:
    def test_returns_urgency_with_counts(self, db_path):
        result = get_urgency_stats()
        assert "urgency_levels" in result
        assert "total_diseases" in result
        assert result["total_diseases"] == 3

        # From test data: cat_0001 and cat_0002 are "high", dog_0001 is "emergency"
        urgency_list = result["urgency_levels"]
        assert len(urgency_list) == 2  # "emergency" and "high"

        emergency = next((u for u in urgency_list if u["urgency"] == "emergency"), None)
        assert emergency is not None
        assert emergency["count"] == 1

        high = next((u for u in urgency_list if u["urgency"] == "high"), None)
        assert high is not None
        assert high["count"] == 2

    def test_urgency_by_species_cat(self, db_path):
        result = get_urgency_by_species("cat")
        assert result["species"] == "cat"
        assert result["total_diseases"] == 2
        # Both cat diseases are "high" urgency
        high = next((u for u in result["urgency_levels"] if u["urgency"] == "high"), None)
        assert high is not None
        assert high["count"] == 2

    def test_urgency_by_species_dog(self, db_path):
        result = get_urgency_by_species("dog")
        assert result["species"] == "dog"
        assert result["total_diseases"] == 1
        # Dog disease is "emergency" urgency
        emergency = next((u for u in result["urgency_levels"] if u["urgency"] == "emergency"), None)
        assert emergency is not None
        assert emergency["count"] == 1


class TestGetSymptomsForSpecies:
    def test_returns_symptoms_from_symptoms_table(self, db_path):
        result = get_symptoms_for_species("cat")
        ids = {s["id"] for s in result}
        assert "coughing" in ids
        assert "wheezing" in ids
        assert "fever" in ids

    def test_returns_symptoms_from_disease_records(self, db_path):
        """Symptoms referenced in diseases but not in symptoms table are included."""
        result = get_symptoms_for_species("dog")
        ids = {s["id"] for s in result}
        # dog symptoms come from disease records (no explicit symptom table entries)
        assert "vomiting" in ids
        assert "diarrhea" in ids

    def test_empty_species_returns_empty(self, db_path):
        result = get_symptoms_for_species("nonexistent")
        assert result == []


class TestListDiseases:
    def test_list_all(self, db_path):
        result = list_diseases()
        assert result["total"] == 3
        assert len(result["diseases"]) == 3

    def test_filter_by_species(self, db_path):
        result = list_diseases(species="cat")
        assert result["total"] == 2
        assert all(d["species"] == "cat" for d in result["diseases"])

    def test_search_by_name(self, db_path):
        result = list_diseases(search="Asthma")
        assert result["total"] == 1
        assert result["diseases"][0]["name"] == "Feline Asthma"

    def test_search_by_japanese_name(self, db_path):
        result = list_diseases(search="喘息")
        assert result["total"] == 1
        assert result["diseases"][0]["id"] == "cat_0001"

    def test_pagination(self, db_path):
        result = list_diseases(limit=1, offset=0)
        assert result["total"] == 3
        assert len(result["diseases"]) == 1
        assert result["limit"] == 1
        assert result["offset"] == 0

    def test_combined_species_and_search(self, db_path):
        result = list_diseases(species="cat", search="Pneumonia")
        assert result["total"] == 1
        assert result["diseases"][0]["name"] == "Feline Pneumonia"


class TestGetDiseaseDetail:
    def test_returns_full_detail(self, db_path):
        disease = get_disease_detail("cat_0001")
        assert disease is not None
        assert disease["name"] == "Feline Asthma"
        assert disease["treatment"] == "Corticosteroids and bronchodilators"
        assert disease["treatment_ja"] == "コルチコステロイドと気管支拡張薬"
        assert disease["prevention"] == "Reduce airborne irritants"
        assert disease["prognosis"] == "Manageable long term"
        assert disease["urgency"] == "high"
        # JSON fields parsed
        assert isinstance(disease["symptoms"], list)
        assert "coughing" in disease["symptoms"]
        assert isinstance(disease["recommended_tests"], list)

    def test_not_found(self, db_path):
        assert get_disease_detail("nonexistent") is None


class TestSearchDiseases:
    def test_search_english(self, db_path):
        results = search_diseases("Parvo")
        assert len(results) == 1
        assert results[0]["species"] == "dog"

    def test_search_japanese(self, db_path):
        results = search_diseases("パルボ")
        assert len(results) == 1

    def test_search_with_species_filter(self, db_path):
        results = search_diseases("cough", species="cat")
        # Now searches in name, description, treatment, etc., so may find results
        # The test data has "coughing" in symptoms but not in description/treatment
        assert len(results) == 0

    def test_search_in_treatment_field(self, db_path):
        # Search for a treatment keyword (from test data: "Antibiotics")
        results = search_diseases("Antibiotics")
        assert len(results) >= 1
        assert any(d["name"] == "Feline Pneumonia" for d in results)

    def test_search_in_description_field(self, db_path):
        # Search for a description keyword (from test data: "Viral")
        results = search_diseases("Viral")
        assert len(results) >= 1
        assert any(d["name"] == "Canine Parvovirus" for d in results)

    def test_search_limit(self, db_path):
        results = search_diseases("Feline", limit=1)
        assert len(results) == 1


class TestGetDiseasesBySymptom:
    def test_find_diseases_by_symptom(self, db_path):
        # From test data: "coughing" is a symptom of cat_0001 and cat_0002
        results = get_diseases_by_symptom("coughing")
        assert len(results) >= 2
        names = {d["name"] for d in results}
        assert "Feline Asthma" in names
        assert "Feline Pneumonia" in names

    def test_find_diseases_by_symptom_with_species_filter(self, db_path):
        # Search for "coughing" in dog species (should return 0)
        results = get_diseases_by_symptom("coughing", species="dog")
        assert len(results) == 0

    def test_symptom_not_found_returns_empty(self, db_path):
        results = get_diseases_by_symptom("nonexistent_symptom")
        assert len(results) == 0

    def test_find_diseases_by_symptom_respects_limit(self, db_path):
        # Get coughing diseases with limit=1
        results = get_diseases_by_symptom("coughing", limit=1)
        assert len(results) == 1


class TestCacheInvalidation:
    def test_invalidate_clears_stats(self, db_path):
        stats1 = get_species_stats()
        # Add a new disease directly
        with get_connection(db_path) as conn:
            upsert_disease(conn, {
                "id": "cat_9999",
                "species": "cat",
                "name": "Test Disease",
                "name_ja": "テスト疾患",
                "symptoms": set(),
            })
        # Before invalidation, cache returns old data
        stats_cached = get_species_stats()
        assert stats_cached["total_diseases"] == stats1["total_diseases"]
        # After invalidation, new data is returned
        invalidate_cache()
        stats2 = get_species_stats()
        assert stats2["total_diseases"] == stats1["total_diseases"] + 1


# ---------------------------------------------------------------------------
# Diseases API endpoint tests
# ---------------------------------------------------------------------------

@pytest.fixture()
def client(db_path):
    """Create a Flask test client with the diseases blueprint."""
    from api.vetdict_api import app
    app.config["TESTING"] = True
    return app.test_client()


class TestDiseasesAPI:
    def test_list_diseases_endpoint(self, client, db_path):
        resp = client.get("/api/diseases")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["success"] is True
        assert data["total"] >= 3

    def test_list_diseases_with_species_filter(self, client, db_path):
        resp = client.get("/api/diseases?species=cat")
        assert resp.status_code == 200
        data = resp.get_json()
        assert all(d["species"] == "cat" for d in data["diseases"])

    def test_list_diseases_with_search(self, client, db_path):
        resp = client.get("/api/diseases?q=Asthma")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["total"] >= 1
        assert any("Asthma" in d["name"] for d in data["diseases"])

    def test_get_disease_detail_endpoint(self, client, db_path):
        resp = client.get("/api/diseases/cat_0001")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["success"] is True
        disease = data["disease"]
        assert disease["name"] == "Feline Asthma"
        assert disease["treatment"] is not None

    def test_get_disease_not_found(self, client, db_path):
        resp = client.get("/api/diseases/nonexistent_999")
        assert resp.status_code == 404
        data = resp.get_json()
        assert data["success"] is False

    def test_get_diseases_by_symptom_endpoint(self, client, db_path):
        # Get diseases with "coughing" symptom
        resp = client.get("/api/symptoms/coughing/diseases")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["success"] is True
        assert data["symptom_id"] == "coughing"
        assert len(data["diseases"]) >= 1
        assert any(d["name"] == "Feline Asthma" for d in data["diseases"])

    def test_get_diseases_by_symptom_with_species_filter(self, client, db_path):
        # Get diseases with "coughing" symptom for dog species (should return 0)
        resp = client.get("/api/symptoms/coughing/diseases?species=dog")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["success"] is True
        assert len(data["diseases"]) == 0

    def test_get_diseases_by_nonexistent_symptom(self, client, db_path):
        resp = client.get("/api/symptoms/nonexistent_symptom_xyz/diseases")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["success"] is True
        assert len(data["diseases"]) == 0

    def test_get_urgency_stats_endpoint(self, client, db_path):
        resp = client.get("/api/urgency-stats")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["success"] is True
        assert "urgency_levels" in data
        assert "total_diseases" in data
        assert data["total_diseases"] == 3
        assert len(data["urgency_levels"]) == 2

    def test_get_urgency_by_species_endpoint(self, client, db_path):
        resp = client.get("/api/species/cat/urgency-stats")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["success"] is True
        assert data["species"] == "cat"
        assert data["total_diseases"] == 2
        assert len(data["urgency_levels"]) == 1
        assert data["urgency_levels"][0]["urgency"] == "high"
        assert data["urgency_levels"][0]["count"] == 2


class TestSpeciesMetaConsistency:
    """Validate that SPECIES_META matches the JS-side SPECIES array (21 species)."""

    def test_species_meta_has_21_entries(self):
        from api.disease_store import SPECIES_META
        assert len(SPECIES_META) == 21

    def test_all_expected_species_present(self):
        from api.disease_store import SPECIES_META
        expected = {
            "dog", "cat", "horse", "rabbit", "hamster", "guinea_pig",
            "chinchilla", "ferret", "hedgehog", "sugar_glider", "degu",
            "bird", "parakeet", "parrot", "reptile", "tortoise",
            "snake", "lizard", "amphibian", "fish", "exotic_other",
        }
        assert set(SPECIES_META.keys()) == expected


class TestFallbackWhenDbEmpty:
    """When SQLite has no diseases, get_species_stats falls back to modules/JSON."""

    def test_fallback_returns_all_species(self, tmp_path, monkeypatch):
        """Even with an empty DB, all 21 species should be returned."""
        path = str(tmp_path / "empty.db")
        init_db(path)
        import contextlib

        @contextlib.contextmanager
        def _patched():
            with get_connection(path) as conn:
                yield conn

        monkeypatch.setattr("api.disease_store.get_connection", _patched)
        monkeypatch.setattr("api.disease_store._db_ready", True)
        invalidate_cache()

        result = get_species_stats()
        assert result["total_species"] == 21
        species_ids = {s["id"] for s in result["species"]}
        assert len(species_ids) == 21
