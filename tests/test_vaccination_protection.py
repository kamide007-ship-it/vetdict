"""Tests for api/data/vaccination_protection.py."""

from api.data.vaccination_protection import (
    VACCINATION_PROTECTION,
    VaccinationStatusHandler,
    VaccineProtection,
)

# ===================================================================
# VaccineProtection dataclass
# ===================================================================


class TestVaccineProtection:
    def test_to_dict_keys(self):
        vp = VaccineProtection(
            disease_name="Test Disease",
            vaccine_names=["VaccA", "VaccB"],
            protection_effectiveness=0.90,
            confidence_reduction=0.20,
            notes="Test note",
        )
        d = vp.to_dict()
        assert set(d.keys()) == {
            "disease_name",
            "vaccine_names",
            "protection_effectiveness",
            "confidence_reduction",
            "notes",
        }

    def test_to_dict_values(self):
        vp = VaccineProtection(
            disease_name="Rabies",
            vaccine_names=["Rabies"],
            protection_effectiveness=1.0,
            confidence_reduction=0.05,
            notes="Core vaccine.",
        )
        d = vp.to_dict()
        assert d["disease_name"] == "Rabies"
        assert d["vaccine_names"] == ["Rabies"]
        assert d["protection_effectiveness"] == 1.0
        assert d["confidence_reduction"] == 0.05
        assert d["notes"] == "Core vaccine."

    def test_default_notes_empty(self):
        vp = VaccineProtection(
            disease_name="X",
            vaccine_names=["X"],
            protection_effectiveness=0.5,
            confidence_reduction=0.5,
        )
        assert vp.notes == ""
        assert vp.to_dict()["notes"] == ""

    def test_vaccine_names_list(self):
        vp = VaccineProtection(
            disease_name="Multi",
            vaccine_names=["A", "B", "C"],
            protection_effectiveness=0.8,
            confidence_reduction=0.3,
        )
        assert isinstance(vp.vaccine_names, list)
        assert len(vp.vaccine_names) == 3


# ===================================================================
# VACCINATION_PROTECTION database integrity
# ===================================================================


class TestVaccinationProtectionDatabase:
    def test_database_nonempty(self):
        assert len(VACCINATION_PROTECTION) > 0

    def test_all_values_are_vaccine_protection(self):
        for name, vp in VACCINATION_PROTECTION.items():
            assert isinstance(vp, VaccineProtection), f"{name} is not VaccineProtection"

    def test_disease_name_matches_key(self):
        for key, vp in VACCINATION_PROTECTION.items():
            assert vp.disease_name == key, f"Key '{key}' doesn't match disease_name '{vp.disease_name}'"

    def test_protection_effectiveness_in_range(self):
        for name, vp in VACCINATION_PROTECTION.items():
            assert 0.0 <= vp.protection_effectiveness <= 1.0, (
                f"{name}: protection_effectiveness={vp.protection_effectiveness} out of range"
            )

    def test_confidence_reduction_in_range(self):
        for name, vp in VACCINATION_PROTECTION.items():
            assert 0.0 <= vp.confidence_reduction <= 1.0, (
                f"{name}: confidence_reduction={vp.confidence_reduction} out of range"
            )

    def test_vaccine_names_nonempty(self):
        for name, vp in VACCINATION_PROTECTION.items():
            assert len(vp.vaccine_names) > 0, f"{name} has empty vaccine_names"

    def test_known_diseases_present(self):
        expected = [
            "Canine Parvovirus",
            "Canine Distemper",
            "Rabies",
            "Feline Panleukopenia",
        ]
        for disease in expected:
            assert disease in VACCINATION_PROTECTION, f"Expected {disease} in database"

    def test_rabies_full_protection(self):
        assert VACCINATION_PROTECTION["Rabies"].protection_effectiveness == 1.0

    def test_parvovirus_high_protection(self):
        assert VACCINATION_PROTECTION["Canine Parvovirus"].protection_effectiveness >= 0.90


# ===================================================================
# VaccinationStatusHandler
# ===================================================================


class TestGetVaccinationProtection:
    def test_known_disease_returns_protection(self):
        vp = VaccinationStatusHandler.get_vaccination_protection("Rabies")
        assert vp is not None
        assert isinstance(vp, VaccineProtection)

    def test_unknown_disease_returns_none(self):
        vp = VaccinationStatusHandler.get_vaccination_protection("NonexistentDisease")
        assert vp is None

    def test_empty_string_returns_none(self):
        vp = VaccinationStatusHandler.get_vaccination_protection("")
        assert vp is None


class TestGetConfidenceReduction:
    def test_known_disease(self):
        reduction = VaccinationStatusHandler.get_confidence_reduction("Rabies")
        assert reduction == VACCINATION_PROTECTION["Rabies"].confidence_reduction

    def test_unknown_disease_returns_default(self):
        reduction = VaccinationStatusHandler.get_confidence_reduction("Unknown")
        assert reduction == 1.0

    def test_unknown_disease_custom_default(self):
        reduction = VaccinationStatusHandler.get_confidence_reduction("Unknown", default=0.5)
        assert reduction == 0.5

    def test_parvovirus_confidence_reduction(self):
        reduction = VaccinationStatusHandler.get_confidence_reduction("Canine Parvovirus")
        assert reduction == 0.15


class TestIsVaccinePreventable:
    def test_known_disease_is_preventable(self):
        assert VaccinationStatusHandler.is_vaccine_preventable("Rabies") is True

    def test_unknown_disease_not_preventable(self):
        assert VaccinationStatusHandler.is_vaccine_preventable("Made Up Disease") is False

    def test_all_database_diseases_are_preventable(self):
        for disease_name in VACCINATION_PROTECTION:
            assert VaccinationStatusHandler.is_vaccine_preventable(disease_name) is True


class TestApplyVaccinationAdjustment:
    def test_current_vaccination_applies_reduction(self):
        adjusted, applied = VaccinationStatusHandler.apply_vaccination_adjustment(
            "Canine Parvovirus", 80, vaccination_status="current"
        )
        assert applied is True
        # 80 * 0.15 = 12
        assert adjusted == int(80 * VACCINATION_PROTECTION["Canine Parvovirus"].confidence_reduction)

    def test_outdated_vaccination_no_adjustment(self):
        adjusted, applied = VaccinationStatusHandler.apply_vaccination_adjustment(
            "Canine Parvovirus", 80, vaccination_status="outdated"
        )
        assert applied is False
        assert adjusted == 80

    def test_no_vaccination_status_no_adjustment(self):
        adjusted, applied = VaccinationStatusHandler.apply_vaccination_adjustment(
            "Canine Parvovirus", 80, vaccination_status="none"
        )
        assert applied is False
        assert adjusted == 80

    def test_none_vaccination_status_no_adjustment(self):
        adjusted, applied = VaccinationStatusHandler.apply_vaccination_adjustment(
            "Canine Parvovirus", 80, vaccination_status=None
        )
        assert applied is False
        assert adjusted == 80

    def test_unknown_disease_no_adjustment(self):
        adjusted, applied = VaccinationStatusHandler.apply_vaccination_adjustment(
            "Unknown Disease", 75, vaccination_status="current"
        )
        assert applied is False
        assert adjusted == 75

    def test_zero_match_percent(self):
        adjusted, applied = VaccinationStatusHandler.apply_vaccination_adjustment(
            "Rabies", 0, vaccination_status="current"
        )
        assert applied is True
        assert adjusted == 0

    def test_rabies_reduction_severe(self):
        adjusted, applied = VaccinationStatusHandler.apply_vaccination_adjustment(
            "Rabies", 100, vaccination_status="current"
        )
        assert applied is True
        assert adjusted == int(100 * 0.05)  # 5% remaining

    def test_returns_tuple(self):
        result = VaccinationStatusHandler.apply_vaccination_adjustment("Rabies", 50, vaccination_status="current")
        assert isinstance(result, tuple)
        assert len(result) == 2


class TestApplyVaccinationToDiseases:
    def _sample_diseases(self):
        return [
            {"name": "Canine Parvovirus", "match_percent": 80},
            {"name": "Canine Distemper", "match_percent": 60},
            {"name": "Unknown Disease", "match_percent": 50},
        ]

    def test_current_status_adjusts_preventable(self):
        diseases = self._sample_diseases()
        result = VaccinationStatusHandler.apply_vaccination_to_diseases(diseases, vaccination_status="current")
        assert len(result) == 3
        parvo = next(d for d in result if d["name"] == "Canine Parvovirus")
        assert parvo["vaccination_adjustment_applied"] is True
        assert parvo["match_percent"] < 80
        assert parvo["match_percent_before_vaccination"] == 80

    def test_unknown_disease_not_adjusted(self):
        diseases = self._sample_diseases()
        result = VaccinationStatusHandler.apply_vaccination_to_diseases(diseases, vaccination_status="current")
        unknown = next(d for d in result if d["name"] == "Unknown Disease")
        assert unknown["vaccination_adjustment_applied"] is False
        assert unknown["match_percent"] == 50

    def test_outdated_status_no_adjustment_applied(self):
        diseases = self._sample_diseases()
        result = VaccinationStatusHandler.apply_vaccination_to_diseases(diseases, vaccination_status="outdated")
        # With outdated status, apply_vaccination_adjustment returns no adjustment
        for d in result:
            assert d["vaccination_adjustment_applied"] is False

    def test_none_status_returns_unchanged(self):
        diseases = self._sample_diseases()
        result = VaccinationStatusHandler.apply_vaccination_to_diseases(diseases, vaccination_status=None)
        # No vaccination_status → returns diseases unchanged
        assert result == diseases

    def test_empty_status_returns_unchanged(self):
        diseases = self._sample_diseases()
        result = VaccinationStatusHandler.apply_vaccination_to_diseases(diseases, vaccination_status="")
        assert result == diseases

    def test_invalid_status_returns_unchanged(self):
        diseases = self._sample_diseases()
        result = VaccinationStatusHandler.apply_vaccination_to_diseases(diseases, vaccination_status="unknown_status")
        assert result == diseases

    def test_none_vaccination_status_default(self):
        diseases = self._sample_diseases()
        result = VaccinationStatusHandler.apply_vaccination_to_diseases(diseases)
        assert result == diseases

    def test_original_dicts_not_mutated(self):
        diseases = [{"name": "Canine Parvovirus", "match_percent": 80}]
        _ = VaccinationStatusHandler.apply_vaccination_to_diseases(diseases, vaccination_status="current")
        # Original dict untouched
        assert diseases[0]["match_percent"] == 80
        assert "vaccination_adjustment_applied" not in diseases[0]

    def test_empty_diseases_list(self):
        result = VaccinationStatusHandler.apply_vaccination_to_diseases([], vaccination_status="current")
        assert result == []

    def test_none_status_applies_no_adjustment_on_outdated(self):
        diseases = [{"name": "Rabies", "match_percent": 90}]
        result = VaccinationStatusHandler.apply_vaccination_to_diseases(diseases, vaccination_status="none")
        rabies = result[0]
        # "none" is in the valid set but apply_vaccination_adjustment("none") => no adjustment
        assert rabies["vaccination_adjustment_applied"] is False

    def test_returns_copies_not_originals(self):
        diseases = [{"name": "Rabies", "match_percent": 90}]
        result = VaccinationStatusHandler.apply_vaccination_to_diseases(diseases, vaccination_status="current")
        # Result items are copies
        assert result[0] is not diseases[0]

    def test_distemper_adjustment_correct(self):
        diseases = [{"name": "Canine Distemper", "match_percent": 100}]
        result = VaccinationStatusHandler.apply_vaccination_to_diseases(diseases, vaccination_status="current")
        assert result[0]["match_percent"] == int(100 * 0.1)  # confidence_reduction=0.1

    def test_feline_diseases_adjusted(self):
        diseases = [
            {"name": "Feline Panleukopenia", "match_percent": 70},
            {"name": "Feline Rabies", "match_percent": 50},
        ]
        result = VaccinationStatusHandler.apply_vaccination_to_diseases(diseases, vaccination_status="current")
        for d in result:
            assert d["vaccination_adjustment_applied"] is True
