"""Tests for api/anesthesia_protocols.py and api/anesthesia_api.py

Covers:
- All 21 species have protocol data
- Protocol data structure validation
- search_protocols() functionality
- Flask Blueprint route endpoints
- Bilingual (ja/en) content validation
"""

import sys
from pathlib import Path

import pytest
from flask import Flask

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from api.anesthesia_api import anesthesia_bp
from api.anesthesia_protocols import (
    ANESTHESIA_CATEGORIES,
    ANESTHESIA_PROTOCOLS,
    RISK_LEVELS,
    get_all_species_ids,
    get_protocols_for_species,
    search_protocols,
)

ALL_SPECIES = [
    "dog", "cat", "horse", "rabbit", "hamster", "guinea_pig",
    "chinchilla", "ferret", "hedgehog", "sugar_glider", "degu",
    "bird", "parakeet", "parrot", "reptile", "tortoise", "snake",
    "lizard", "amphibian", "fish", "exotic_other",
]


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def app():
    flask_app = Flask(__name__)
    flask_app.config["TESTING"] = True
    flask_app.register_blueprint(anesthesia_bp)
    return flask_app


@pytest.fixture(scope="module")
def client(app):
    return app.test_client()


# ---------------------------------------------------------------------------
# Data structure tests
# ---------------------------------------------------------------------------

class TestAnesthesiaData:
    """Validate the ANESTHESIA_PROTOCOLS data structure."""

    def test_all_21_species_present(self):
        assert len(ANESTHESIA_PROTOCOLS) == 21
        for sp in ALL_SPECIES:
            assert sp in ANESTHESIA_PROTOCOLS, f"Missing species: {sp}"

    def test_categories_structure(self):
        assert len(ANESTHESIA_CATEGORIES) >= 7
        for key, val in ANESTHESIA_CATEGORIES.items():
            assert "ja" in val, f"Category {key} missing 'ja'"
            assert "en" in val, f"Category {key} missing 'en'"

    def test_risk_levels_structure(self):
        assert "low" in RISK_LEVELS
        assert "moderate" in RISK_LEVELS
        assert "high" in RISK_LEVELS

    @pytest.mark.parametrize("species", ALL_SPECIES)
    def test_species_has_required_fields(self, species):
        data = ANESTHESIA_PROTOCOLS[species]
        assert "species_name" in data
        assert "ja" in data["species_name"]
        assert "en" in data["species_name"]
        assert "overview" in data
        assert "fasting" in data
        assert "protocols" in data
        assert len(data["protocols"]) >= 1

    @pytest.mark.parametrize("species", ALL_SPECIES)
    def test_species_overview_bilingual(self, species):
        ov = ANESTHESIA_PROTOCOLS[species]["overview"]
        assert "ja" in ov and len(ov["ja"]) > 20
        assert "en" in ov and len(ov["en"]) > 20

    @pytest.mark.parametrize("species", ALL_SPECIES)
    def test_species_fasting_bilingual(self, species):
        f = ANESTHESIA_PROTOCOLS[species]["fasting"]
        assert "ja" in f and len(f["ja"]) > 5
        assert "en" in f and len(f["en"]) > 5

    @pytest.mark.parametrize("species", ALL_SPECIES)
    def test_protocols_have_required_fields(self, species):
        for p in ANESTHESIA_PROTOCOLS[species]["protocols"]:
            assert "name" in p
            assert "ja" in p["name"]
            assert "en" in p["name"]
            assert "category" in p
            assert p["category"] in ANESTHESIA_CATEGORIES

    @pytest.mark.parametrize("species", ["dog", "cat", "horse"])
    def test_major_species_have_comprehensive_protocols(self, species):
        """Dog, cat, horse should have at least 7 protocol categories."""
        data = ANESTHESIA_PROTOCOLS[species]
        categories = {p["category"] for p in data["protocols"]}
        assert len(categories) >= 5, f"{species} has only {len(categories)} categories"

    def test_dog_has_breed_considerations(self):
        dog = ANESTHESIA_PROTOCOLS["dog"]
        assert "breed_considerations" in dog
        assert len(dog["breed_considerations"]) >= 3

    @pytest.mark.parametrize("species", ALL_SPECIES)
    def test_drugs_have_required_fields(self, species):
        for p in ANESTHESIA_PROTOCOLS[species]["protocols"]:
            for d in p.get("drugs", []):
                assert "name" in d, f"Drug missing name in {species}"
                assert "name_ja" in d, f"Drug missing name_ja in {species}"
                assert "dose" in d, f"Drug {d['name']} missing dose in {species}"
                assert "route" in d, f"Drug {d['name']} missing route in {species}"

    @pytest.mark.parametrize("species", ALL_SPECIES)
    def test_monitoring_params_structure(self, species):
        for p in ANESTHESIA_PROTOCOLS[species]["protocols"]:
            for m in p.get("monitoring_params", []):
                assert "param" in m
                assert "target" in m


# ---------------------------------------------------------------------------
# Utility function tests
# ---------------------------------------------------------------------------

class TestUtilityFunctions:

    def test_get_all_species_ids(self):
        ids = get_all_species_ids()
        assert len(ids) == 21
        for sp in ALL_SPECIES:
            assert sp in ids

    def test_get_protocols_for_species_valid(self):
        data = get_protocols_for_species("dog")
        assert data is not None
        assert data["species_name"]["en"] == "Dog"

    def test_get_protocols_for_species_invalid(self):
        assert get_protocols_for_species("unicorn") is None

    def test_search_protocols_no_filter(self):
        results = search_protocols()
        assert len(results) > 50  # At least 50 total protocols

    def test_search_protocols_by_species(self):
        results = search_protocols(species="cat")
        assert all(r["species"] == "cat" for r in results)
        assert len(results) >= 5

    def test_search_protocols_by_category(self):
        results = search_protocols(category="sedation")
        assert all(r["protocol"]["category"] == "sedation" for r in results)
        assert len(results) >= 5

    def test_search_protocols_by_query(self):
        results = search_protocols(query="propofol")
        assert len(results) >= 2  # At least dog and cat have propofol

    def test_search_protocols_combined_filter(self):
        results = search_protocols(query="ketamine", species="dog")
        assert len(results) >= 1
        assert all(r["species"] == "dog" for r in results)


# ---------------------------------------------------------------------------
# API endpoint tests
# ---------------------------------------------------------------------------

class TestAnesthesiaAPI:

    def test_get_protocols_no_species(self, client):
        resp = client.get("/api/anesthesia/protocols")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "results" in data
        assert "total" in data
        assert data["total"] > 50
        assert "categories" in data

    def test_get_protocols_with_species(self, client):
        resp = client.get("/api/anesthesia/protocols?species=dog")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["species"] == "dog"
        assert "overview" in data
        assert "fasting" in data
        assert "protocols" in data
        assert len(data["protocols"]) >= 7

    def test_get_protocols_with_category_filter(self, client):
        resp = client.get("/api/anesthesia/protocols?species=cat&category=sedation")
        assert resp.status_code == 200
        data = resp.get_json()
        assert all(p["category"] == "sedation" for p in data["protocols"])

    def test_get_protocols_with_search(self, client):
        resp = client.get("/api/anesthesia/protocols?species=dog&search=propofol")
        assert resp.status_code == 200
        data = resp.get_json()
        assert len(data["protocols"]) >= 1

    def test_get_protocols_invalid_species(self, client):
        resp = client.get("/api/anesthesia/protocols?species=unicorn")
        assert resp.status_code == 404

    @pytest.mark.parametrize("species", ALL_SPECIES)
    def test_all_species_return_200(self, client, species):
        resp = client.get(f"/api/anesthesia/protocols?species={species}")
        assert resp.status_code == 200
        data = resp.get_json()
        assert len(data["protocols"]) >= 1

    def test_get_species_list(self, client):
        resp = client.get("/api/anesthesia/species")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["total"] == 21
        assert len(data["species"]) == 21
        ids = [s["id"] for s in data["species"]]
        for sp in ALL_SPECIES:
            assert sp in ids

    def test_get_categories(self, client):
        resp = client.get("/api/anesthesia/categories")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "categories" in data
        assert "risk_levels" in data
        assert "sedation" in data["categories"]
        assert "induction" in data["categories"]


# ---------------------------------------------------------------------------
# Content quality tests
# ---------------------------------------------------------------------------

class TestContentQuality:

    def test_dog_propofol_dosage(self):
        """Verify propofol dose is clinically accurate for dogs."""
        dog = ANESTHESIA_PROTOCOLS["dog"]
        induction = [p for p in dog["protocols"] if p["category"] == "induction"]
        assert len(induction) >= 1
        drugs = [d for p in induction for d in p.get("drugs", []) if "Propofol" in d["name"]]
        assert len(drugs) >= 1
        assert "2-6 mg/kg" in drugs[0]["dose"]

    def test_cat_laryngospasm_warning(self):
        """Cat intubation notes should mention laryngospasm."""
        cat = ANESTHESIA_PROTOCOLS["cat"]
        induction = [p for p in cat["protocols"] if p["category"] == "induction"]
        all_notes = " ".join(p.get("notes", "") + p.get("notes_ja", "") for p in induction)
        assert "laryngospasm" in all_notes.lower() or "喉頭痙攣" in all_notes

    def test_horse_recovery_danger(self):
        """Horse recovery should note it as the most dangerous phase."""
        horse = ANESTHESIA_PROTOCOLS["horse"]
        recovery = [p for p in horse["protocols"] if p["category"] == "recovery"]
        assert len(recovery) >= 1
        notes = recovery[0].get("notes", "") + recovery[0].get("notes_ja", "")
        assert "dangerous" in notes.lower() or "危険" in notes

    def test_rabbit_no_fasting(self):
        """Rabbits should not require fasting."""
        rabbit = ANESTHESIA_PROTOCOLS["rabbit"]
        fasting = rabbit["fasting"]["en"].lower()
        assert "no fasting" in fasting

    def test_fish_immersion(self):
        """Fish anesthesia should use immersion."""
        fish = ANESTHESIA_PROTOCOLS["fish"]
        all_text = " ".join(p.get("notes", "") for p in fish["protocols"])
        assert "immersion" in all_text.lower() or "浸漬" in fish["overview"]["ja"]

    def test_reptile_potz(self):
        """Reptile protocols should mention POTZ."""
        reptile = ANESTHESIA_PROTOCOLS["reptile"]
        overview = reptile["overview"]["en"]
        assert "POTZ" in overview

    def test_chinchilla_fipronil_warning(self):
        """Chinchilla protocols should warn about fipronil."""
        chin = ANESTHESIA_PROTOCOLS["chinchilla"]
        all_notes = " ".join(
            p.get("notes", "") + p.get("notes_ja", "")
            for p in chin["protocols"]
        )
        assert "fipronil" in all_notes.lower() or "フィプロニル" in all_notes

    def test_ferret_insulinoma_glucose(self):
        """Ferret protocols should mention insulinoma/glucose monitoring."""
        ferret = ANESTHESIA_PROTOCOLS["ferret"]
        overview = ferret["overview"]["en"].lower()
        assert "insulinoma" in overview or "glucose" in overview

    def test_amphibian_ms222(self):
        """Amphibian should use MS-222."""
        amp = ANESTHESIA_PROTOCOLS["amphibian"]
        drugs = [d for p in amp["protocols"] for d in p.get("drugs", []) if "MS-222" in d["name"]]
        assert len(drugs) >= 1

    def test_bird_uncuffed_et_tube(self):
        """Bird intubation should specify uncuffed ET tubes."""
        bird = ANESTHESIA_PROTOCOLS["bird"]
        all_notes = " ".join(
            p.get("notes", "") + p.get("notes_ja", "")
            for p in bird["protocols"]
        )
        assert "uncuffed" in all_notes.lower() or "非カフ" in all_notes
