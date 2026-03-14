"""Tests for species_analyzer.py - Multi-species symptom analysis routing."""

import pytest

from api.species_analyzer import (
    SPECIES_HANDLERS,
    analyze_horse,
    analyze_species_symptoms,
)


class TestSpeciesHandlers:

    def test_dog_in_handlers(self):
        assert "dog" in SPECIES_HANDLERS

    def test_cat_in_handlers(self):
        assert "cat" in SPECIES_HANDLERS

    def test_horse_in_handlers(self):
        assert "horse" in SPECIES_HANDLERS

    def test_rabbit_in_handlers(self):
        assert "rabbit" in SPECIES_HANDLERS

    def test_all_expected_species(self):
        expected = [
            "dog", "cat", "rabbit", "hamster", "chinchilla", "guinea_pig",
            "ferret", "hedgehog", "sugar_glider", "degu", "bird", "parakeet",
            "parrot", "reptile", "tortoise", "snake", "lizard", "amphibian",
            "exotic_other", "horse",
        ]
        for sp in expected:
            assert sp in SPECIES_HANDLERS

    def test_dog_handler_is_none(self):
        """Dog is handled specially, so handler is None."""
        assert SPECIES_HANDLERS["dog"] is None


class TestAnalyzeSpeciesSymptoms:

    def test_dog_returns_dict(self):
        result = analyze_species_symptoms("dog", ["vomiting", "diarrhea"])
        assert isinstance(result, dict)

    def test_cat_returns_dict(self):
        result = analyze_species_symptoms("cat", ["vomiting"])
        assert isinstance(result, dict)

    def test_rabbit_returns_dict(self):
        result = analyze_species_symptoms("rabbit", ["anorexia"])
        assert isinstance(result, dict)

    def test_horse_returns_dict(self):
        result = analyze_species_symptoms("horse", ["colic_signs"])
        assert isinstance(result, dict)

    def test_unsupported_species_raises(self):
        with pytest.raises(ValueError, match="Unsupported"):
            analyze_species_symptoms("unicorn", ["pain"])

    def test_none_species_defaults_to_dog(self):
        result = analyze_species_symptoms(None, ["vomiting"])
        assert isinstance(result, dict)

    def test_dog_with_breed(self):
        result = analyze_species_symptoms(
            "dog", ["vomiting"], breed="french_bulldog",
        )
        assert isinstance(result, dict)

    def test_cat_with_extra_params(self):
        result = analyze_species_symptoms(
            "cat", ["vomiting"], breed="cat_persian",
            onset="acute", age_years=5.0, gender="female",
        )
        assert isinstance(result, dict)


class TestAnalyzeHorse:

    def test_returns_dict(self):
        result = analyze_horse(["colic_signs"])
        assert isinstance(result, dict)

    def test_has_expected_keys(self):
        result = analyze_horse(["lameness"])
        assert "possible_conditions" in result
        assert "recommended_tests" in result

    def test_with_age_stage(self):
        result = analyze_horse(["colic_signs"], age_stage="adult")
        assert isinstance(result, dict)

    def test_empty_symptoms(self):
        result = analyze_horse([])
        assert "possible_conditions" in result
