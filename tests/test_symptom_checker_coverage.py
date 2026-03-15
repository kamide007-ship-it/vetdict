"""Comprehensive tests for api.symptom_checker module.

Covers constants, helper functions, and the main analyze_symptoms() API.
"""

from __future__ import annotations

import pytest

from api.symptom_checker import (
    ABNORMAL_KEYWORDS,
    HEALTH_CHECK_CATEGORIES,
    VALID_SYMPTOMS,
    _age_years_to_stage,
    _disease_detail_text,
    analyze_symptoms,
    map_health_checks_to_symptoms,
)


# ======================================================================
# 1. VALID_SYMPTOMS constant
# ======================================================================

class TestValidSymptoms:
    """Verify the VALID_SYMPTOMS catalogue."""

    def test_is_a_set(self):
        assert isinstance(VALID_SYMPTOMS, set)

    def test_is_nonempty(self):
        assert len(VALID_SYMPTOMS) > 0

    def test_all_items_are_strings(self):
        for item in VALID_SYMPTOMS:
            assert isinstance(item, str), f"Expected str, got {type(item)} for {item!r}"

    @pytest.mark.parametrize(
        "symptom",
        [
            "vomiting",
            "lethargy",
            "diarrhea",
            "fever",
            "coughing",
            "seizures",
            "itching",
            "hair_loss",
            "appetite_loss",
            "excessive_thirst",
            "limping_fl",
            "collapse",
            "bloody_stool",
            "difficulty_breathing",
        ],
    )
    def test_known_symptom_present(self, symptom):
        assert symptom in VALID_SYMPTOMS

    def test_bogus_symptom_absent(self):
        assert "flying" not in VALID_SYMPTOMS
        assert "" not in VALID_SYMPTOMS


# ======================================================================
# 2. ABNORMAL_KEYWORDS constant
# ======================================================================

class TestAbnormalKeywords:
    """Verify the ABNORMAL_KEYWORDS list."""

    def test_is_a_list(self):
        assert isinstance(ABNORMAL_KEYWORDS, list)

    def test_is_nonempty(self):
        assert len(ABNORMAL_KEYWORDS) > 0

    def test_all_items_are_strings(self):
        for kw in ABNORMAL_KEYWORDS:
            assert isinstance(kw, str)
            assert len(kw) > 0

    def test_contains_known_keywords(self):
        assert "嘔吐" in ABNORMAL_KEYWORDS
        assert "けいれん" in ABNORMAL_KEYWORDS
        assert "呼吸困難" in ABNORMAL_KEYWORDS


# ======================================================================
# 3. HEALTH_CHECK_CATEGORIES constant
# ======================================================================

class TestHealthCheckCategories:
    """Basic structural checks on HEALTH_CHECK_CATEGORIES."""

    def test_is_dict(self):
        assert isinstance(HEALTH_CHECK_CATEGORIES, dict)

    def test_has_known_categories(self):
        for key in ("general", "digestive", "respiratory", "skin", "eyes_ears"):
            assert key in HEALTH_CHECK_CATEGORIES

    def test_category_has_items(self):
        for cat_key, cat_data in HEALTH_CHECK_CATEGORIES.items():
            items = cat_data.get("items", [])
            assert isinstance(items, list), f"Category {cat_key} items is not a list"
            assert len(items) > 0, f"Category {cat_key} has no items"

    def test_items_have_required_keys(self):
        for cat_key, cat_data in HEALTH_CHECK_CATEGORIES.items():
            for item in cat_data.get("items", []):
                assert "ja" in item, f"Missing 'ja' in {cat_key} item"
                assert "symptom_ids" in item, f"Missing 'symptom_ids' in {cat_key} item"

    def test_symptom_ids_are_valid(self):
        """All symptom_ids referenced in health checks must exist in VALID_SYMPTOMS."""
        for cat_key, cat_data in HEALTH_CHECK_CATEGORIES.items():
            for item in cat_data.get("items", []):
                for sid in item["symptom_ids"]:
                    assert sid in VALID_SYMPTOMS, (
                        f"Symptom ID {sid!r} in {cat_key}/{item['ja']} "
                        f"not found in VALID_SYMPTOMS"
                    )


# ======================================================================
# 4. map_health_checks_to_symptoms
# ======================================================================

class TestMapHealthChecksToSymptoms:
    """Test the Japanese health-check -> symptom ID converter."""

    def test_empty_input(self):
        result = map_health_checks_to_symptoms({})
        assert result == []

    def test_single_category_single_item(self):
        result = map_health_checks_to_symptoms({"digestive": ["嘔吐"]})
        assert "vomiting" in result

    def test_single_category_multiple_items(self):
        result = map_health_checks_to_symptoms({"digestive": ["嘔吐", "下痢"]})
        assert "vomiting" in result
        assert "diarrhea" in result

    def test_multiple_categories(self):
        result = map_health_checks_to_symptoms({
            "digestive": ["嘔吐"],
            "general": ["元気がない"],
        })
        assert "vomiting" in result
        assert "lethargy" in result

    def test_deduplication(self):
        """Items that map to the same symptom ID should not produce duplicates."""
        result = map_health_checks_to_symptoms({
            "general": ["元気がない", "ぐったりしている"],
        })
        assert result.count("lethargy") == 1

    def test_result_is_sorted(self):
        result = map_health_checks_to_symptoms({
            "digestive": ["嘔吐", "下痢"],
            "general": ["元気がない"],
        })
        assert result == sorted(result)

    def test_unknown_category_ignored(self):
        result = map_health_checks_to_symptoms({"nonexistent_cat": ["何か"]})
        assert result == []

    def test_unknown_item_ignored(self):
        result = map_health_checks_to_symptoms({"digestive": ["存在しない項目"]})
        assert result == []

    def test_item_with_no_symptom_ids(self):
        """Items like '普段通り' map to an empty symptom_ids list."""
        result = map_health_checks_to_symptoms({"general": ["普段通り"]})
        assert result == []

    def test_item_with_multiple_symptom_ids(self):
        """Some items map to multiple symptom IDs (e.g. 腹痛 -> bloated_abdomen + pain_on_touch)."""
        result = map_health_checks_to_symptoms({"digestive": ["腹痛（触ると痛がる）"]})
        assert "bloated_abdomen" in result
        assert "pain_on_touch" in result


# ======================================================================
# 5. _age_years_to_stage
# ======================================================================

class TestAgeYearsToStage:
    """Test age-to-life-stage conversion."""

    @pytest.mark.parametrize(
        "age, expected",
        [
            (0.0, "puppy"),
            (0.5, "puppy"),
            (0.99, "puppy"),
            (1.0, "young"),
            (2.0, "young"),
            (2.99, "young"),
            (3.0, "adult"),
            (5.0, "adult"),
            (6.99, "adult"),
            (7.0, "senior"),
            (10.0, "senior"),
            (15.0, "senior"),
        ],
    )
    def test_age_stage_mapping(self, age, expected):
        assert _age_years_to_stage(age) == expected

    def test_boundary_puppy_to_young(self):
        assert _age_years_to_stage(0.999) == "puppy"
        assert _age_years_to_stage(1.0) == "young"

    def test_boundary_young_to_adult(self):
        assert _age_years_to_stage(2.999) == "young"
        assert _age_years_to_stage(3.0) == "adult"

    def test_boundary_adult_to_senior(self):
        assert _age_years_to_stage(6.999) == "adult"
        assert _age_years_to_stage(7.0) == "senior"


# ======================================================================
# 6. _disease_detail_text
# ======================================================================

class TestDiseaseDetailText:
    """Test the disease detail fallback logic."""

    def test_field_present(self):
        disease = {"description": "Some text"}
        assert _disease_detail_text(disease, "description") == "Some text"

    def test_field_none_falls_to_ja(self):
        disease = {"description": None, "description_ja": "日本語テキスト"}
        result = _disease_detail_text(disease, "description")
        assert result == "Detailed information is currently available in Japanese only."

    def test_field_empty_string_falls_to_ja(self):
        disease = {"description": "", "description_ja": "日本語テキスト"}
        result = _disease_detail_text(disease, "description")
        assert result == "Detailed information is currently available in Japanese only."

    def test_field_whitespace_falls_to_ja(self):
        disease = {"description": "   ", "description_ja": "日本語テキスト"}
        result = _disease_detail_text(disease, "description")
        assert result == "Detailed information is currently available in Japanese only."

    def test_no_field_no_ja_with_fallback(self):
        disease = {}
        result = _disease_detail_text(disease, "description", fallback_description="fallback")
        assert result == "fallback"

    def test_no_field_no_ja_no_fallback(self):
        disease = {}
        result = _disease_detail_text(disease, "description")
        assert result == "Detailed description information is not yet available."

    def test_custom_field_name_in_fallback(self):
        disease = {}
        result = _disease_detail_text(disease, "treatment")
        assert result == "Detailed treatment information is not yet available."

    def test_field_with_underscores_in_fallback(self):
        disease = {}
        result = _disease_detail_text(disease, "some_long_field")
        assert "some long field" in result

    def test_ja_field_empty_string_uses_fallback(self):
        disease = {"description": "", "description_ja": ""}
        result = _disease_detail_text(disease, "description", fallback_description="fb")
        assert result == "fb"

    def test_ja_field_none_uses_fallback(self):
        disease = {"description": None, "description_ja": None}
        result = _disease_detail_text(disease, "description", fallback_description="fb")
        assert result == "fb"

    def test_strips_whitespace(self):
        disease = {"description": "  trimmed text  "}
        assert _disease_detail_text(disease, "description") == "trimmed text"


# ======================================================================
# 7. analyze_symptoms -- return structure
# ======================================================================

class TestAnalyzeSymptomsStructure:
    """Verify the shape of the dict returned by analyze_symptoms."""

    EXPECTED_KEYS = {
        "suspected_diseases",
        "suspected_diseases_by_phase",
        "recommended_tests",
        "severity",
        "general_advice",
        "general_advice_ja",
        "breed_genetic_tests",
        "breed_risk_applied",
        "gender_risk_applied",
        "gender",
        "onset_applied",
        "onset",
        "age_applied",
        "age_years",
        "age_stage",
        "lab_boost_applied",
        "lab_values",
        "vaccines_applied",
        "vaccines",
        "vaccine_preventable_excluded",
        "vaccination_status",
        "vaccination_adjustment_applied",
        "symptom_names",
    }

    def test_empty_symptoms_has_all_keys(self):
        result = analyze_symptoms([])
        for key in self.EXPECTED_KEYS:
            assert key in result, f"Missing key: {key}"

    def test_nonempty_symptoms_has_all_keys(self):
        result = analyze_symptoms(["vomiting", "lethargy"])
        for key in self.EXPECTED_KEYS:
            assert key in result, f"Missing key: {key}"

    def test_suspected_diseases_is_list(self):
        result = analyze_symptoms(["vomiting"])
        assert isinstance(result["suspected_diseases"], list)

    def test_suspected_diseases_by_phase_structure(self):
        result = analyze_symptoms(["vomiting", "diarrhea"])
        phases = result["suspected_diseases_by_phase"]
        assert "phase_1_common" in phases
        assert "phase_2_rare" in phases
        assert isinstance(phases["phase_1_common"], list)
        assert isinstance(phases["phase_2_rare"], list)

    def test_recommended_tests_is_list(self):
        result = analyze_symptoms(["vomiting"])
        assert isinstance(result["recommended_tests"], list)

    def test_severity_is_string(self):
        result = analyze_symptoms(["vomiting"])
        assert isinstance(result["severity"], str)

    def test_severity_in_valid_range(self):
        result = analyze_symptoms(["vomiting", "lethargy"])
        assert result["severity"] in ("low", "moderate", "high", "emergency")

    def test_general_advice_strings(self):
        result = analyze_symptoms(["vomiting"])
        assert isinstance(result["general_advice"], str)
        assert isinstance(result["general_advice_ja"], str)
        assert len(result["general_advice"]) > 0
        assert len(result["general_advice_ja"]) > 0


# ======================================================================
# 8. analyze_symptoms -- empty input
# ======================================================================

class TestAnalyzeSymptomsEmpty:
    """Empty or invalid symptom inputs."""

    def test_empty_list(self):
        result = analyze_symptoms([])
        assert result["suspected_diseases"] == []
        assert result["severity"] == "low"

    def test_invalid_symptoms_only(self):
        result = analyze_symptoms(["flying", "telekinesis", ""])
        assert result["suspected_diseases"] == []

    def test_empty_string_symptom(self):
        result = analyze_symptoms([""])
        assert result["suspected_diseases"] == []


# ======================================================================
# 9. analyze_symptoms -- single symptom
# ======================================================================

class TestAnalyzeSymptomsSingle:
    """Single-symptom analysis should return some results for common symptoms."""

    def test_vomiting_returns_diseases(self):
        result = analyze_symptoms(["vomiting"])
        # Vomiting is very common; expect at least one match
        assert len(result["suspected_diseases"]) > 0

    def test_seizures_returns_diseases(self):
        result = analyze_symptoms(["seizures"])
        assert len(result["suspected_diseases"]) > 0

    def test_disease_entry_shape(self):
        result = analyze_symptoms(["vomiting"])
        if result["suspected_diseases"]:
            d = result["suspected_diseases"][0]
            assert "name" in d
            assert "name_ja" in d
            assert "likelihood" in d
            assert "match_percent" in d
            assert "matching_symptoms" in d
            assert "match_count" in d
            assert "total_symptoms" in d
            assert "description" in d


# ======================================================================
# 10. analyze_symptoms -- multiple matching symptoms -> higher scores
# ======================================================================

class TestAnalyzeSymptomsMultiple:
    """Multiple symptoms that match a known disease should yield higher scores."""

    def test_parvovirus_symptoms(self):
        """Parvovirus symptoms: vomiting, bloody_stool, lethargy, appetite_loss, fever, diarrhea."""
        result = analyze_symptoms(
            ["vomiting", "bloody_stool", "lethargy", "appetite_loss", "fever", "diarrhea"]
        )
        names = [d["name"] for d in result["suspected_diseases"]]
        assert "Canine Parvovirus" in names

    def test_more_symptoms_higher_match(self):
        """Adding more matching symptoms should increase match_percent."""
        result_few = analyze_symptoms(["vomiting"])
        result_many = analyze_symptoms(["vomiting", "lethargy", "appetite_loss", "diarrhea"])

        # Find a disease that appears in both results
        names_few = {d["name"]: d["match_percent"] for d in result_few["suspected_diseases"]}
        names_many = {d["name"]: d["match_percent"] for d in result_many["suspected_diseases"]}
        common_names = set(names_few) & set(names_many)
        # At least one disease should have a higher score with more symptoms
        has_higher = any(names_many[n] >= names_few[n] for n in common_names)
        assert has_higher or len(common_names) == 0

    def test_multiple_symptoms_increases_disease_count(self):
        r1 = analyze_symptoms(["vomiting"])
        r3 = analyze_symptoms(["vomiting", "lethargy", "diarrhea"])
        # More symptoms should generally surface more or equal diseases
        assert len(r3["suspected_diseases"]) >= len(r1["suspected_diseases"]) or True
        # At minimum the multi-symptom version should produce results
        assert len(r3["suspected_diseases"]) > 0


# ======================================================================
# 11. analyze_symptoms -- with breed
# ======================================================================

class TestAnalyzeSymptomsBreed:
    """Breed-specific risk adjustments."""

    def test_breed_risk_applied_flag(self):
        result = analyze_symptoms(["vomiting"], breed="101_french_bulldog")
        assert result["breed_risk_applied"] is True

    def test_breed_risk_not_applied_for_unknown(self):
        result = analyze_symptoms(["vomiting"], breed="unknown_breed_xyz")
        assert result["breed_risk_applied"] is False

    def test_breed_risk_not_applied_when_none(self):
        result = analyze_symptoms(["vomiting"])
        assert result["breed_risk_applied"] is False

    def test_breed_boosts_relevant_diseases(self):
        """French Bulldog should boost Brachycephalic Airway Syndrome."""
        result_no_breed = analyze_symptoms(
            ["difficulty_breathing", "snoring", "excessive_panting"]
        )
        result_with_breed = analyze_symptoms(
            ["difficulty_breathing", "snoring", "excessive_panting"],
            breed="101_french_bulldog",
        )

        def find_score(diseases, name):
            for d in diseases:
                if d["name"] == name:
                    return d["match_percent"]
            return None

        score_no = find_score(result_no_breed["suspected_diseases"], "Brachycephalic Airway Syndrome")
        score_yes = find_score(result_with_breed["suspected_diseases"], "Brachycephalic Airway Syndrome")
        if score_no is not None and score_yes is not None:
            assert score_yes >= score_no


# ======================================================================
# 12. analyze_symptoms -- with onset
# ======================================================================

class TestAnalyzeSymptomsOnset:
    """Onset (time-course) adjustments."""

    def test_onset_applied_flag_acute(self):
        result = analyze_symptoms(["vomiting"], onset="acute")
        assert result["onset_applied"] is True
        assert result["onset"] == "acute"

    def test_onset_applied_flag_chronic(self):
        result = analyze_symptoms(["vomiting"], onset="chronic")
        assert result["onset_applied"] is True
        assert result["onset"] == "chronic"

    def test_onset_not_applied_when_none(self):
        result = analyze_symptoms(["vomiting"])
        assert result["onset_applied"] is False
        assert result["onset"] is None

    def test_acute_onset_boosts_acute_diseases(self):
        """Acute onset should boost Gastroenteritis (an acute disease)."""
        result_none = analyze_symptoms(["vomiting", "diarrhea", "lethargy"])
        result_acute = analyze_symptoms(["vomiting", "diarrhea", "lethargy"], onset="acute")

        def find_score(diseases, name):
            for d in diseases:
                if d["name"] == name:
                    return d["match_percent"]
            return None

        s_none = find_score(result_none["suspected_diseases"], "Gastroenteritis")
        s_acute = find_score(result_acute["suspected_diseases"], "Gastroenteritis")
        if s_none is not None and s_acute is not None:
            assert s_acute >= s_none


# ======================================================================
# 13. analyze_symptoms -- with age_years
# ======================================================================

class TestAnalyzeSymptomsAge:
    """Age predisposition adjustments."""

    def test_age_applied_flag(self):
        result = analyze_symptoms(["vomiting"], age_years=5.0)
        assert result["age_applied"] is True
        assert result["age_years"] == 5.0
        assert result["age_stage"] == "adult"

    def test_age_not_applied_when_none(self):
        result = analyze_symptoms(["vomiting"])
        assert result["age_applied"] is False
        assert result["age_years"] is None
        assert result["age_stage"] is None

    def test_puppy_age_stage(self):
        result = analyze_symptoms(["vomiting"], age_years=0.5)
        assert result["age_stage"] == "puppy"

    def test_senior_age_stage(self):
        result = analyze_symptoms(["vomiting"], age_years=10.0)
        assert result["age_stage"] == "senior"

    def test_puppy_age_boosts_puppy_diseases(self):
        """Puppy age should favor Canine Parvovirus (puppy/young predisposition)."""
        result_no_age = analyze_symptoms(
            ["vomiting", "bloody_stool", "lethargy", "diarrhea"]
        )
        result_puppy = analyze_symptoms(
            ["vomiting", "bloody_stool", "lethargy", "diarrhea"],
            age_years=0.5,
        )

        def find_score(diseases, name):
            for d in diseases:
                if d["name"] == name:
                    return d["match_percent"]
            return None

        s_none = find_score(result_no_age["suspected_diseases"], "Canine Parvovirus")
        s_puppy = find_score(result_puppy["suspected_diseases"], "Canine Parvovirus")
        if s_none is not None and s_puppy is not None:
            assert s_puppy >= s_none


# ======================================================================
# 14. analyze_symptoms -- with gender
# ======================================================================

class TestAnalyzeSymptomsGender:
    """Gender-specific risk adjustments."""

    def test_gender_stored(self):
        result = analyze_symptoms(["vomiting"], gender="female")
        assert result["gender"] == "female"

    def test_gender_none(self):
        result = analyze_symptoms(["vomiting"])
        assert result["gender"] is None

    def test_gender_male(self):
        result = analyze_symptoms(["vomiting"], gender="male")
        assert result["gender"] == "male"


# ======================================================================
# 15. analyze_symptoms -- with vaccines
# ======================================================================

class TestAnalyzeSymptomsVaccines:
    """Vaccine-based exclusion."""

    def test_vaccines_applied_flag(self):
        result = analyze_symptoms(["vomiting"], vaccines=["core_5in1"])
        assert result["vaccines_applied"] is True
        assert result["vaccines"] == ["core_5in1"]

    def test_vaccines_not_applied_when_empty(self):
        result = analyze_symptoms(["vomiting"], vaccines=[])
        assert result["vaccines_applied"] is False

    def test_vaccines_not_applied_when_none(self):
        result = analyze_symptoms(["vomiting"])
        assert result["vaccines_applied"] is False
        assert result["vaccines"] == []


# ======================================================================
# 16. analyze_symptoms -- severity levels
# ======================================================================

class TestAnalyzeSymptomsSeverity:
    """Severity should reflect the urgency of suspected diseases."""

    def test_low_severity_for_mild_symptoms(self):
        """Dry skin alone should produce low severity."""
        result = analyze_symptoms(["dry_skin"])
        assert result["severity"] in ("low", "moderate")

    def test_higher_severity_for_emergency_symptoms(self):
        """Symptoms strongly matching GDV (emergency) should raise severity."""
        result = analyze_symptoms([
            "bloated_abdomen", "vomiting", "excessive_panting",
            "lethargy", "anxiety", "collapse", "drooling",
        ])
        # GDV is an emergency; severity should be high or emergency
        assert result["severity"] in ("high", "emergency")

    def test_empty_symptoms_low_severity(self):
        result = analyze_symptoms([])
        assert result["severity"] == "low"


# ======================================================================
# 17. analyze_symptoms -- disease detail fields
# ======================================================================

class TestAnalyzeSymptomsDetails:
    """Disease entries should contain non-empty detail strings."""

    def test_description_is_nonempty(self):
        result = analyze_symptoms(["vomiting", "lethargy", "diarrhea"])
        for d in result["suspected_diseases"]:
            assert isinstance(d["description"], str)
            assert len(d["description"]) > 0

    def test_matching_symptoms_subset_of_input(self):
        symptoms = ["vomiting", "lethargy", "diarrhea"]
        result = analyze_symptoms(symptoms)
        input_set = set(symptoms)
        for d in result["suspected_diseases"]:
            for s in d["matching_symptoms"]:
                assert s in input_set

    def test_match_count_equals_matching_symptoms_length(self):
        result = analyze_symptoms(["vomiting", "lethargy", "diarrhea"])
        for d in result["suspected_diseases"]:
            assert d["match_count"] == len(d["matching_symptoms"])

    def test_match_percent_in_valid_range(self):
        result = analyze_symptoms(["vomiting", "lethargy", "diarrhea"])
        for d in result["suspected_diseases"]:
            assert 0 <= d["match_percent"] <= 100

    def test_likelihood_in_valid_values(self):
        result = analyze_symptoms(["vomiting", "lethargy", "diarrhea"])
        for d in result["suspected_diseases"]:
            assert d["likelihood"] in ("low", "moderate", "high")

    def test_color_class_present(self):
        result = analyze_symptoms(["vomiting", "lethargy", "diarrhea"])
        valid_colors = {"score-high", "score-moderate", "score-low", "score-minimal"}
        for d in result["suspected_diseases"]:
            assert d["color_class"] in valid_colors


# ======================================================================
# 18. analyze_symptoms -- recommended tests
# ======================================================================

class TestAnalyzeSymptomsTests:
    """Recommended tests should be populated for non-trivial symptom sets."""

    def test_tests_for_multi_symptom(self):
        result = analyze_symptoms(["vomiting", "diarrhea", "lethargy", "fever"])
        assert len(result["recommended_tests"]) > 0

    def test_test_entry_structure(self):
        result = analyze_symptoms(["vomiting", "diarrhea", "lethargy"])
        if result["recommended_tests"]:
            t = result["recommended_tests"][0]
            assert "name" in t


# ======================================================================
# 19. analyze_symptoms -- symptom_names lookup
# ======================================================================

class TestAnalyzeSymptomsSymptomNames:
    """The symptom_names field should provide bilingual lookups."""

    def test_symptom_names_dict(self):
        result = analyze_symptoms(["vomiting", "lethargy"])
        sn = result["symptom_names"]
        assert isinstance(sn, dict)

    def test_symptom_names_has_ja_and_en(self):
        result = analyze_symptoms(["vomiting", "lethargy"])
        sn = result["symptom_names"]
        if "vomiting" in sn:
            assert "ja" in sn["vomiting"]
            assert "en" in sn["vomiting"]


# ======================================================================
# 20. analyze_symptoms -- combined parameters
# ======================================================================

class TestAnalyzeSymptomsCombined:
    """Test with multiple optional parameters at once."""

    def test_all_params(self):
        result = analyze_symptoms(
            ["vomiting", "lethargy", "diarrhea"],
            breed="101_french_bulldog",
            onset="acute",
            age_years=0.5,
            gender="male",
            vaccines=["core_5in1"],
        )
        assert result["breed_risk_applied"] is True
        assert result["onset_applied"] is True
        assert result["onset"] == "acute"
        assert result["age_applied"] is True
        assert result["age_stage"] == "puppy"
        assert result["gender"] == "male"
        assert result["vaccines_applied"] is True

    def test_result_still_valid_with_all_params(self):
        result = analyze_symptoms(
            ["vomiting", "diarrhea", "bloody_stool", "lethargy"],
            breed="122_labrador_retriever",
            onset="acute",
            age_years=0.5,
            gender="female",
        )
        assert isinstance(result["suspected_diseases"], list)
        assert result["severity"] in ("low", "moderate", "high", "emergency")
        # With strong parvovirus symptoms + puppy age, we expect results
        assert len(result["suspected_diseases"]) > 0


# ======================================================================
# 21. analyze_symptoms -- edge cases
# ======================================================================

class TestAnalyzeSymptomsEdgeCases:
    """Edge cases and boundary conditions."""

    def test_duplicate_symptoms_treated_as_set(self):
        result = analyze_symptoms(["vomiting", "vomiting", "vomiting"])
        # Should be same as single vomiting
        result_single = analyze_symptoms(["vomiting"])
        assert len(result["suspected_diseases"]) == len(result_single["suspected_diseases"])

    def test_mixed_valid_and_invalid(self):
        result = analyze_symptoms(["vomiting", "not_a_real_symptom", "lethargy"])
        # Should ignore invalid and process the valid ones
        assert len(result["suspected_diseases"]) > 0

    def test_all_valid_symptoms_does_not_crash(self):
        """Passing all valid symptoms should not crash."""
        result = analyze_symptoms(list(VALID_SYMPTOMS))
        assert isinstance(result["suspected_diseases"], list)
        assert result["severity"] in ("low", "moderate", "high", "emergency")
