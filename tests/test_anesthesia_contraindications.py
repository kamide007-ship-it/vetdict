"""Tests for anesthesia drug-disease contraindication system."""

import pytest

from api.anesthesia_contraindications import (
    DRUG_CONTRAINDICATIONS,
    SEVERITY_CAUTION,
    SEVERITY_CONTRAINDICATED,
    SEVERITY_MONITOR,
    check_contraindications,
    get_all_contraindications,
)


class TestContraindicationData:
    """Test contraindication data integrity."""

    def test_all_rules_have_required_fields(self):
        for rule in DRUG_CONTRAINDICATIONS:
            assert "drug_patterns" in rule
            assert "conditions" in rule
            assert "severity" in rule
            assert "message_ja" in rule
            assert "message_en" in rule
            assert len(rule["drug_patterns"]) > 0
            assert len(rule["conditions"]) > 0
            assert rule["severity"] in (
                SEVERITY_CONTRAINDICATED,
                SEVERITY_CAUTION,
                SEVERITY_MONITOR,
            )

    def test_messages_not_empty(self):
        for rule in DRUG_CONTRAINDICATIONS:
            assert len(rule["message_ja"]) > 10
            assert len(rule["message_en"]) > 10

    def test_rule_count(self):
        """Ensure we have a reasonable number of rules."""
        assert len(DRUG_CONTRAINDICATIONS) >= 20

    def test_severity_distribution(self):
        severities = [r["severity"] for r in DRUG_CONTRAINDICATIONS]
        assert SEVERITY_CONTRAINDICATED in severities
        assert SEVERITY_CAUTION in severities
        assert SEVERITY_MONITOR in severities


class TestCheckContraindications:
    """Test the check_contraindications function."""

    def test_empty_drug_returns_empty(self):
        assert check_contraindications("") == []
        assert check_contraindications(None) == []

    def test_no_conditions_returns_empty(self):
        assert check_contraindications("dexmedetomidine") == []

    def test_dexmedetomidine_cardiac(self):
        """Alpha-2 agonist + cardiac disease = contraindicated."""
        warnings = check_contraindications(
            "dexmedetomidine", conditions=["cardiac_disease"]
        )
        assert len(warnings) >= 1
        assert any(w["severity"] == SEVERITY_CONTRAINDICATED for w in warnings)

    def test_medetomidine_cardiac(self):
        warnings = check_contraindications(
            "medetomidine", conditions=["cardiac_disease"]
        )
        assert len(warnings) >= 1

    def test_thiopental_sighthound(self):
        """Thiopental + sighthound = contraindicated."""
        warnings = check_contraindications(
            "thiopental", breed="greyhound"
        )
        assert len(warnings) >= 1
        assert any(w["severity"] == SEVERITY_CONTRAINDICATED for w in warnings)

    def test_thiopental_gdv(self):
        warnings = check_contraindications(
            "thiopental", conditions=["gdv"]
        )
        assert len(warnings) >= 1
        assert any(w["severity"] == SEVERITY_CONTRAINDICATED for w in warnings)

    def test_nsaid_renal(self):
        """NSAIDs + renal disease = contraindicated."""
        warnings = check_contraindications(
            "meloxicam", conditions=["renal_disease"]
        )
        assert len(warnings) >= 1
        assert any(w["severity"] == SEVERITY_CONTRAINDICATED for w in warnings)

    def test_nsaid_gi_ulcer(self):
        warnings = check_contraindications(
            "carprofen", conditions=["gi_ulcer"]
        )
        assert len(warnings) >= 1

    def test_nsaid_hepatic_caution(self):
        warnings = check_contraindications(
            "meloxicam", conditions=["hepatic_disease"]
        )
        assert len(warnings) >= 1
        assert any(w["severity"] == SEVERITY_CAUTION for w in warnings)

    def test_nsaid_pregnancy(self):
        warnings = check_contraindications(
            "meloxicam", conditions=["pregnancy"]
        )
        assert len(warnings) >= 1

    def test_nsaid_coagulopathy(self):
        warnings = check_contraindications(
            "carprofen", conditions=["coagulopathy"]
        )
        assert len(warnings) >= 1

    def test_acepromazine_epilepsy(self):
        warnings = check_contraindications(
            "acepromazine", conditions=["epilepsy"]
        )
        assert len(warnings) >= 1
        assert any(w["severity"] == SEVERITY_CONTRAINDICATED for w in warnings)

    def test_acepromazine_boxer(self):
        warnings = check_contraindications(
            "acepromazine", breed="boxer"
        )
        assert len(warnings) >= 1

    def test_fipronil_rabbit(self):
        """Fipronil + rabbit = absolutely contraindicated."""
        warnings = check_contraindications(
            "fipronil", species="rabbit"
        )
        assert len(warnings) >= 1
        assert any(w["severity"] == SEVERITY_CONTRAINDICATED for w in warnings)

    def test_fipronil_chinchilla(self):
        warnings = check_contraindications(
            "fipronil", species="chinchilla"
        )
        assert len(warnings) >= 1
        assert any(w["severity"] == SEVERITY_CONTRAINDICATED for w in warnings)

    def test_alpha2_rabbit_caution(self):
        warnings = check_contraindications(
            "dexmedetomidine", species="rabbit"
        )
        assert len(warnings) >= 1

    def test_alpha2_diabetes(self):
        warnings = check_contraindications(
            "medetomidine", conditions=["diabetes"]
        )
        assert len(warnings) >= 1

    def test_ketamine_reptile(self):
        warnings = check_contraindications(
            "ketamine", species="reptile"
        )
        assert len(warnings) >= 1

    def test_safe_drug_no_warnings(self):
        """A drug with no matching conditions returns empty."""
        warnings = check_contraindications(
            "propofol", conditions=["cardiac_disease"]
        )
        assert warnings == []

    def test_multiple_conditions(self):
        """Multiple conditions can trigger multiple warnings."""
        warnings = check_contraindications(
            "meloxicam", conditions=["renal_disease", "gi_ulcer"]
        )
        assert len(warnings) >= 2

    def test_japanese_drug_name(self):
        """Japanese drug names should match."""
        warnings = check_contraindications(
            "デクスメデトミジン", conditions=["cardiac_disease"]
        )
        assert len(warnings) >= 1

    def test_xylazine_cardiac(self):
        warnings = check_contraindications(
            "xylazine", conditions=["cardiac_disease"]
        )
        assert len(warnings) >= 1
        assert any(w["severity"] == SEVERITY_CONTRAINDICATED for w in warnings)

    def test_morphine_brachycephalic(self):
        warnings = check_contraindications(
            "morphine", conditions=["brachycephalic"]
        )
        assert len(warnings) >= 1
        assert any(w["severity"] == SEVERITY_CAUTION for w in warnings)

    def test_alpha2_insulinoma(self):
        warnings = check_contraindications(
            "dexmedetomidine", conditions=["insulinoma"]
        )
        assert len(warnings) >= 1


class TestGetAllContraindications:
    """Test the get_all_contraindications function."""

    def test_returns_list(self):
        rules = get_all_contraindications()
        assert isinstance(rules, list)
        assert len(rules) == len(DRUG_CONTRAINDICATIONS)


class TestContraindicationAPI:
    """Test the contraindication API endpoint."""

    @pytest.fixture
    def client(self):
        from api.vetdict_api import app

        app.config["TESTING"] = True
        with app.test_client() as client:
            yield client

    def test_get_all_rules(self, client):
        resp = client.get("/api/anesthesia/contraindications?all=true")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "rules" in data
        assert data["total"] >= 20

    def test_check_drug(self, client):
        resp = client.get(
            "/api/anesthesia/contraindications?drug=dexmedetomidine&conditions=cardiac_disease"
        )
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["count"] >= 1
        assert data["warnings"][0]["severity"] == SEVERITY_CONTRAINDICATED

    def test_check_safe_drug(self, client):
        resp = client.get(
            "/api/anesthesia/contraindications?drug=propofol&conditions=cardiac_disease"
        )
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["count"] == 0

    def test_check_with_species(self, client):
        resp = client.get(
            "/api/anesthesia/contraindications?drug=fipronil&species=rabbit"
        )
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["count"] >= 1

    def test_check_empty_drug(self, client):
        resp = client.get("/api/anesthesia/contraindications?drug=")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["count"] == 0
