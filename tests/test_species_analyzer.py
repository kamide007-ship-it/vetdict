"""Tests for species_analyzer.py - Multi-species symptom analysis routing."""

import pytest

from api.species_analyzer import (
    SPECIES_HANDLERS,
    _horse_category,
    analyze_horse,
    analyze_species_symptoms,
)

# All 20 non-dog species (dog is handled specially)
_NON_DOG_SPECIES = [
    "cat", "rabbit", "hamster", "chinchilla", "guinea_pig",
    "ferret", "hedgehog", "sugar_glider", "degu", "bird", "parakeet",
    "parrot", "reptile", "tortoise", "snake", "lizard", "amphibian",
    "fish", "exotic_other", "horse",
]


# ---------------------------------------------------------------------------
# SPECIES_HANDLERS registry
# ---------------------------------------------------------------------------


class TestSpeciesHandlers:

    def test_all_21_species_registered(self):
        expected = {"dog"} | set(_NON_DOG_SPECIES)
        assert set(SPECIES_HANDLERS.keys()) == expected

    def test_handler_count(self):
        assert len(SPECIES_HANDLERS) == 21

    def test_dog_handler_is_none(self):
        """Dog is handled specially, so handler is None."""
        assert SPECIES_HANDLERS["dog"] is None

    def test_all_non_dog_handlers_are_callable(self):
        """After lazy loading, handlers are resolved via _resolve_handler()"""
        from api.species_analyzer import _resolve_handler
        for sp in _NON_DOG_SPECIES:
            handler = _resolve_handler(sp)
            assert callable(handler), f"{sp}: handler is not callable"


# ---------------------------------------------------------------------------
# analyze_species_symptoms - routing
# ---------------------------------------------------------------------------


class TestAnalyzeSpeciesSymptoms:

    def test_unsupported_species_raises(self):
        with pytest.raises(ValueError, match="Unsupported"):
            analyze_species_symptoms("unicorn", ["pain"])

    def test_none_species_defaults_to_dog(self):
        result = analyze_species_symptoms(None, ["vomiting"])
        assert isinstance(result, dict)
        assert "possible_conditions" in result or "suspected_diseases" in result

    def test_dog_routing(self):
        result = analyze_species_symptoms("dog", ["vomiting", "diarrhea"])
        assert isinstance(result, dict)

    def test_dog_with_all_params(self):
        result = analyze_species_symptoms(
            "dog", ["vomiting"],
            breed="french_bulldog",
            onset="acute",
            age_years=5.0,
            gender="female",
        )
        assert isinstance(result, dict)

    def test_cat_routing_with_params(self):
        result = analyze_species_symptoms(
            "cat", ["vomiting", "lethargy"],
            onset="acute",
            age_years=8.0,
            gender="male",
        )
        assert isinstance(result, dict)
        assert "suspected_diseases" in result

    def test_horse_routing(self):
        result = analyze_species_symptoms("horse", ["colic_signs"])
        assert isinstance(result, dict)
        assert "possible_conditions" in result

    @pytest.mark.parametrize("species", _NON_DOG_SPECIES)
    def test_every_species_returns_dict(self, species):
        """Every supported species should return a dict without errors."""
        # Use a generic symptom that most species have
        result = analyze_species_symptoms(species, ["lethargy"])
        assert isinstance(result, dict)

    def test_species_case_insensitive(self):
        result = analyze_species_symptoms("Cat", ["vomiting"])
        assert isinstance(result, dict)


# ---------------------------------------------------------------------------
# Result structure validation
# ---------------------------------------------------------------------------


class TestResultStructure:

    def test_cat_result_has_suspected_diseases(self):
        result = analyze_species_symptoms("cat", ["vomiting", "lethargy", "anorexia"])
        assert "suspected_diseases" in result
        assert isinstance(result["suspected_diseases"], list)

    def test_cat_conditions_have_required_fields(self):
        result = analyze_species_symptoms("cat", ["vomiting", "lethargy", "anorexia"])
        for cond in result["suspected_diseases"][:3]:
            assert "name" in cond
            assert "match_percent" in cond or "confidence" in cond

    def test_dog_result_has_suspected_diseases(self):
        result = analyze_species_symptoms("dog", ["vomiting", "diarrhea", "lethargy"])
        assert "suspected_diseases" in result

    def test_rabbit_result_structure(self):
        result = analyze_species_symptoms("rabbit", ["anorexia", "lethargy"])
        assert "suspected_diseases" in result

    def test_fish_result_structure(self):
        result = analyze_species_symptoms("fish", ["white_spots", "flashing"])
        assert "suspected_diseases" in result

    def test_horse_result_has_possible_conditions(self):
        """Horse uses possible_conditions (different engine)."""
        result = analyze_species_symptoms("horse", ["colic_signs"])
        assert "possible_conditions" in result

    def test_generic_result_common_keys(self):
        """All generic species results should have these keys."""
        result = analyze_species_symptoms("ferret", ["lethargy"])
        for key in ("severity", "recommended_tests", "onset_applied", "age_applied"):
            assert key in result, f"Missing key: {key}"


# ---------------------------------------------------------------------------
# analyze_horse
# ---------------------------------------------------------------------------


class TestAnalyzeHorse:

    def test_returns_dict(self):
        result = analyze_horse(["colic_signs"])
        assert isinstance(result, dict)

    def test_has_expected_keys(self):
        result = analyze_horse(["lameness"])
        assert "possible_conditions" in result
        assert "recommended_tests" in result
        assert "severity" in result

    def test_with_age_stage(self):
        result = analyze_horse(["colic_signs"], age_stage="adult")
        assert isinstance(result, dict)

    def test_empty_symptoms(self):
        result = analyze_horse([])
        assert "possible_conditions" in result

    def test_with_age_years(self):
        result = analyze_horse(["lameness"], age_years=12.0)
        assert result.get("age_applied") is True

    def test_with_onset(self):
        result = analyze_horse(["colic_signs"], onset="acute")
        assert result.get("onset_applied") is True

    def test_severity_field(self):
        result = analyze_horse(["colic_signs", "fever", "lameness"])
        assert result["severity"] in ("emergency", "high", "moderate", "low")

    def test_conditions_have_scoring_detail(self):
        result = analyze_horse(["colic_signs"])
        for cond in result["possible_conditions"][:3]:
            assert "scoring_detail" in cond
            detail = cond["scoring_detail"]
            assert "weighted_recall" in detail
            assert "confidence_level" in detail


# ---------------------------------------------------------------------------
# _horse_category helper
# ---------------------------------------------------------------------------


class TestHorseCategory:

    def test_viral(self):
        assert _horse_category("Equine Herpesvirus", "") == "viral"

    def test_bacterial(self):
        assert _horse_category("Strangles", "streptococcal infection") == "bacterial"

    def test_fungal(self):
        assert _horse_category("Ringworm", "dermatophytosis") == "fungal"

    def test_parasitic(self):
        assert _horse_category("Strongylosis", "parasitic infection") == "parasitic"

    def test_general_default(self):
        assert _horse_category("Navicular Syndrome", "hoof condition") == "general"
