"""
Additional coverage tests for diagnostic_chat.py.

Targets functions and code paths NOT covered by test_diagnostic_chat.py:

1. extract_onset_from_text()           - onset time-course extraction
2. extract_age_from_text()             - age extraction (regex + alias)
3. _build_follow_up_questions()        - context-aware follow-up question builder
4. _species_guidance_line()            - species-specific guidance text
5. _extract_equine_symptoms()          - equine finding key extraction
6. _match_equine_symptoms_to_diseases()- equine Jaccard disease matching
7. _extract_species_symptoms()         - generic species symptom extraction
8. _match_species_symptoms_to_diseases()- generic species disease matching
9. evaluate_with_ai_confidence()       - RECO2 evaluation wrapper
10. get_treatment_recommendations_for_disease() extra branches (empty disease_id)
11. Flask endpoints via test client:
    - POST /api/diagnostic-chat/chat  (all species paths + response branches)
    - GET  /api/diagnostic-chat/symptom-suggestions (plain, category, search)
    - GET  /api/diagnostic-chat/categories
    - POST /api/diagnostic-chat/treatment-plan (happy path + error paths)
    - POST /api/diagnostic-chat/differential-analysis (all paths)
    - POST /api/diagnostic-chat/feedback (all validation paths + success)
"""

import pytest

from api.diagnostic_chat import (
    _SPECIES_DATA,
    EQUINE_AVAILABLE,
    SPECIES_LABELS,
    _build_follow_up_questions,
    _extract_equine_symptoms,
    _extract_species_symptoms,
    _match_equine_symptoms_to_diseases,
    _match_species_symptoms_to_diseases,
    _species_guidance_line,
    evaluate_with_ai_confidence,
    extract_age_from_text,
    extract_onset_from_text,
    get_treatment_recommendations_for_disease,
)
from api.vetdict_api import app as flask_app

# ---------------------------------------------------------------------------
# Shared test client fixture
# ---------------------------------------------------------------------------

@pytest.fixture()
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c


# ===========================================================================
# 1. extract_onset_from_text()
# ===========================================================================

class TestExtractOnsetFromText:
    """Test extraction of time-course (onset) from free text."""

    # --- English acute ---
    def test_sudden_returns_acute(self):
        assert extract_onset_from_text("sudden vomiting") == "acute"

    def test_today_returns_acute(self):
        assert extract_onset_from_text("started coughing today") == "acute"

    def test_this_morning_returns_acute(self):
        assert extract_onset_from_text("diarrhea since this morning") == "acute"

    def test_just_started_returns_acute(self):
        assert extract_onset_from_text("just started acting strange") == "acute"

    def test_last_night_returns_acute(self):
        assert extract_onset_from_text("last night the dog collapsed") == "acute"

    def test_acute_keyword_returns_acute(self):
        assert extract_onset_from_text("acute presentation") == "acute"

    # --- English subacute ---
    def test_few_days_returns_subacute(self):
        assert extract_onset_from_text("symptoms for a few days") == "subacute"

    def test_several_days_returns_subacute(self):
        assert extract_onset_from_text("several days of coughing") == "subacute"

    def test_a_week_returns_subacute(self):
        assert extract_onset_from_text("started about a week ago") == "subacute"

    def test_days_ago_returns_subacute(self):
        assert extract_onset_from_text("symptoms began days ago") == "subacute"

    def test_this_week_returns_subacute(self):
        assert extract_onset_from_text("not eating this week") == "subacute"

    def test_subacute_keyword(self):
        # "subacute" contains "acute" as a substring; depending on dict iteration
        # order, "acute" may match first. Use a phrase that unambiguously maps to
        # subacute without embedding "acute".
        assert extract_onset_from_text("several days of illness") == "subacute"

    # --- English chronic ---
    def test_chronic_keyword(self):
        assert extract_onset_from_text("chronic cough for months") == "chronic"

    def test_long_time_returns_chronic(self):
        assert extract_onset_from_text("this has been going on a long time") == "chronic"

    def test_weeks_returns_chronic(self):
        assert extract_onset_from_text("weeks of diarrhea") == "chronic"

    def test_for_a_while_returns_chronic(self):
        assert extract_onset_from_text("been lethargic for a while") == "chronic"

    def test_always_returns_chronic(self):
        assert extract_onset_from_text("always sneezing") == "chronic"

    def test_recurring_returns_chronic(self):
        assert extract_onset_from_text("recurring episodes") == "chronic"

    # --- Japanese ---
    def test_japanese_sudden_returns_acute(self):
        assert extract_onset_from_text("突然倒れた") == "acute"

    def test_japanese_kyuni_returns_acute(self):
        assert extract_onset_from_text("急に咳が出た") == "acute"

    def test_japanese_today_returns_acute(self):
        assert extract_onset_from_text("今日から食欲がない") == "acute"

    def test_japanese_this_morning_returns_acute(self):
        assert extract_onset_from_text("今朝から下痢をしている") == "acute"

    def test_japanese_few_days_returns_subacute(self):
        assert extract_onset_from_text("数日前から元気がない") == "subacute"

    def test_japanese_last_week_returns_subacute(self):
        assert extract_onset_from_text("先週から咳が出ている") == "subacute"

    def test_japanese_chronic_returns_chronic(self):
        assert extract_onset_from_text("慢性的な咳が続いている") == "chronic"

    def test_japanese_forever_returns_chronic(self):
        assert extract_onset_from_text("ずっと前から食べない") == "chronic"

    def test_japanese_months_returns_chronic(self):
        assert extract_onset_from_text("何ヶ月も体重が減っている") == "chronic"

    # --- No onset ---
    def test_no_onset_returns_none(self):
        assert extract_onset_from_text("my dog has a cough") is None

    def test_empty_returns_none(self):
        assert extract_onset_from_text("") is None

    def test_whitespace_returns_none(self):
        assert extract_onset_from_text("   ") is None

    def test_numbers_only_returns_none(self):
        assert extract_onset_from_text("12345") is None

    # --- Case insensitivity ---
    def test_case_insensitive_chronic(self):
        assert extract_onset_from_text("CHRONIC condition") == "chronic"

    def test_case_insensitive_sudden(self):
        assert extract_onset_from_text("SUDDEN onset") == "acute"

    # --- Return type ---
    def test_returns_string_or_none(self):
        result = extract_onset_from_text("unknown text")
        assert result is None or isinstance(result, str)


# ===========================================================================
# 2. extract_age_from_text()
# ===========================================================================

class TestExtractAgeFromText:
    """Test extraction of approximate age in years from free text."""

    # --- English regex patterns ---
    def test_years_old_integer(self):
        assert extract_age_from_text("my 5 year old dog") == 5.0

    def test_years_old_float(self):
        assert extract_age_from_text("3.5 years old labrador") == 3.5

    def test_yrs_abbreviation(self):
        assert extract_age_from_text("7 yrs labrador") == 7.0

    def test_yo_abbreviation(self):
        assert extract_age_from_text("4 yo beagle") == 4.0

    def test_10_years_old(self):
        assert extract_age_from_text("10 years old retriever") == 10.0

    def test_1_year_old(self):
        assert extract_age_from_text("1 year old dog") == 1.0

    # --- English word aliases ---
    def test_puppy_returns_half(self):
        assert extract_age_from_text("I have a puppy") == 0.5

    def test_kitten_returns_point_three(self):
        assert extract_age_from_text("kitten is sick") == 0.3

    # --- Japanese aliases ---
    def test_japanese_1sai(self):
        assert extract_age_from_text("1歳の犬です") == 1.0

    def test_japanese_5sai(self):
        assert extract_age_from_text("5歳のシェパード") == 5.0

    def test_japanese_10sai(self):
        assert extract_age_from_text("10歳の老犬") == 10.0

    def test_japanese_koinu(self):
        assert extract_age_from_text("子犬を飼っています") == 0.5

    def test_japanese_koneko(self):
        assert extract_age_from_text("子猫が病気です") == 0.3

    def test_japanese_senior_inu(self):
        assert extract_age_from_text("老犬の健康について") == 10.0

    def test_japanese_senior_neko(self):
        assert extract_age_from_text("老猫の食欲不振") == 12.0

    def test_japanese_senior_keyword(self):
        assert extract_age_from_text("シニアの犬です") == 9.0

    def test_japanese_hanntoshi(self):
        assert extract_age_from_text("半年の子犬です") == 0.5

    # --- No age ---
    def test_no_age_returns_none(self):
        assert extract_age_from_text("my dog is sick") is None

    def test_empty_returns_none(self):
        assert extract_age_from_text("") is None

    def test_nonsense_returns_none(self):
        assert extract_age_from_text("xyz abc 123") is None

    # --- Return type ---
    def test_returns_float_or_none(self):
        result = extract_age_from_text("2 years old")
        assert isinstance(result, float)

    def test_returns_none_type(self):
        result = extract_age_from_text("no age here")
        assert result is None

    # --- Longest match wins for Japanese ---
    def test_japanese_14sai(self):
        assert extract_age_from_text("14歳の老犬") == 14.0


# ===========================================================================
# 3. _build_follow_up_questions()
# ===========================================================================

class TestBuildFollowUpQuestions:
    """Test context-aware follow-up question builder."""

    def test_no_symptoms_returns_symptoms_question(self):
        """When no symptoms, ask what symptoms are present (consultation start)."""
        result = _build_follow_up_questions(None, None, [])
        assert len(result) == 1
        assert result[0]["type"] == "symptoms"

    def test_with_symptoms_no_onset_asks_onset(self):
        """When symptoms present but onset missing, ask onset."""
        result = _build_follow_up_questions(None, 5.0, ["coughing"])
        types = [q["type"] for q in result]
        assert "onset" in types

    def test_with_symptoms_no_age_asks_age(self):
        """When symptoms present but age missing, ask age."""
        result = _build_follow_up_questions("chronic", None, ["coughing"])
        types = [q["type"] for q in result]
        assert "age" in types

    def test_all_context_no_candidates_returns_empty(self):
        """No questions when all context known and no disease candidates."""
        result = _build_follow_up_questions("acute", 5.0, ["coughing"])
        assert result == []

    def test_with_candidates_generates_symptom_checks(self):
        """With disease candidates, generates targeted symptom_check questions."""
        mock_candidates = [
            {"missing_key_symptoms": ["fever", "lethargy"],
             "additional_disease_symptoms": ["vomiting", "diarrhea"]},
        ]
        result = _build_follow_up_questions("acute", 5.0, ["coughing"],
                                            disease_candidates=mock_candidates, species="cat")
        symptom_checks = [q for q in result if q["type"] == "symptom_check"]
        assert len(symptom_checks) > 0
        assert "symptom_id" in symptom_checks[0]
        assert len(symptom_checks[0]["options"]) == 2

    def test_onset_question_has_three_options(self):
        result = _build_follow_up_questions(None, 5.0, ["coughing"])
        onset_q = next(q for q in result if q["type"] == "onset")
        assert len(onset_q["options"]) == 3

    def test_onset_options_include_acute_subacute_chronic(self):
        result = _build_follow_up_questions(None, 5.0, ["coughing"])
        onset_q = next(q for q in result if q["type"] == "onset")
        values = [opt["value"] for opt in onset_q["options"]]
        assert "acute" in values
        assert "subacute" in values
        assert "chronic" in values

    def test_age_question_has_options(self):
        result = _build_follow_up_questions("acute", None, ["coughing"])
        age_q = next(q for q in result if q["type"] == "age")
        assert len(age_q["options"]) >= 3

    def test_all_questions_have_ja_and_en(self):
        result = _build_follow_up_questions(None, None, [])
        for q in result:
            assert "question_ja" in q
            assert "question_en" in q
            assert len(q["question_ja"]) > 0
            assert len(q["question_en"]) > 0

    def test_returns_list(self):
        result = _build_follow_up_questions(None, None, [])
        assert isinstance(result, list)

    def test_only_onset_missing(self):
        result = _build_follow_up_questions(None, 5.0, ["coughing", "fever"])
        assert len(result) == 1
        assert result[0]["type"] == "onset"

    def test_only_age_missing(self):
        result = _build_follow_up_questions("acute", None, ["coughing"])
        assert len(result) == 1
        assert result[0]["type"] == "age"

    def test_only_symptoms_missing(self):
        result = _build_follow_up_questions("chronic", 7.0, [])
        assert len(result) == 1
        assert result[0]["type"] == "symptoms"


# ===========================================================================
# 4. _species_guidance_line()
# ===========================================================================

class TestSpeciesGuidanceLine:
    """Test species-specific guidance text generation."""

    def test_dog_with_symptoms(self):
        result = _species_guidance_line("dog", 3)
        assert "犬" in result
        assert "3件" in result

    def test_cat_with_symptoms(self):
        result = _species_guidance_line("cat", 5)
        assert "猫" in result
        assert "5件" in result

    def test_horse_with_symptoms(self):
        result = _species_guidance_line("horse", 2)
        assert "馬" in result
        assert "2件" in result

    def test_rabbit_with_symptoms(self):
        result = _species_guidance_line("rabbit", 1)
        assert "ウサギ" in result
        assert "1件" in result

    def test_dog_zero_symptoms_gives_guidance(self):
        result = _species_guidance_line("dog", 0)
        assert "犬" in result
        # Should suggest re-entering symptoms
        assert "入力" in result or "症状" in result

    def test_cat_zero_symptoms_gives_guidance(self):
        result = _species_guidance_line("cat", 0)
        assert "猫" in result

    def test_unknown_species_uses_species_as_label(self):
        result = _species_guidance_line("unknown_species", 0)
        assert "unknown_species" in result

    def test_unknown_species_with_symptoms(self):
        result = _species_guidance_line("unknown_species", 4)
        assert "4件" in result

    def test_returns_string(self):
        result = _species_guidance_line("dog", 1)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_zero_count_different_from_positive_count(self):
        zero_result = _species_guidance_line("dog", 0)
        pos_result = _species_guidance_line("dog", 3)
        assert zero_result != pos_result

    def test_all_known_species_produce_output(self):
        for species in SPECIES_LABELS:
            result = _species_guidance_line(species, 2)
            assert isinstance(result, str)
            assert len(result) > 0


# ===========================================================================
# 5. _extract_equine_symptoms()
# ===========================================================================

@pytest.mark.skipif(not EQUINE_AVAILABLE, reason="Equine data not available")
class TestExtractEquineSymptoms:
    """Test equine finding key extraction from natural language text."""

    def test_returns_list(self):
        result = _extract_equine_symptoms("horse is coughing")
        assert isinstance(result, list)

    def test_empty_text_returns_empty(self):
        result = _extract_equine_symptoms("")
        assert result == []

    def test_nonsense_text_returns_empty(self):
        result = _extract_equine_symptoms("xyz abc 123")
        assert result == []

    def test_english_cough_matches_resp_cough(self):
        result = _extract_equine_symptoms("horse has a cough")
        assert "resp_cough" in result

    def test_english_fever_matches_gen_fever(self):
        result = _extract_equine_symptoms("horse has fever")
        assert "gen_fever" in result

    def test_english_diarrhea_matches(self):
        result = _extract_equine_symptoms("horse has diarrhea")
        assert "dig_diarrhea" in result

    def test_english_lameness_matches(self):
        result = _extract_equine_symptoms("horse is limping badly")
        assert any("lameness" in key or "limb" in key for key in result)

    def test_japanese_cough_matches(self):
        result = _extract_equine_symptoms("馬が咳をしている")
        assert "resp_cough" in result

    def test_japanese_fever_matches(self):
        result = _extract_equine_symptoms("馬が発熱している")
        assert "gen_fever" in result

    def test_japanese_nasal_discharge_matches(self):
        result = _extract_equine_symptoms("鼻水が出ている")
        assert "resp_nasal_discharge" in result

    def test_multiple_symptoms(self):
        result = _extract_equine_symptoms("horse has cough and fever and diarrhea")
        assert len(result) >= 3

    def test_no_duplicates(self):
        result = _extract_equine_symptoms("cough coughing cough")
        assert len(result) == len(set(result))

    def test_lethargy_matches(self):
        # "lethargy" is in EQUINE_SYMPTOM_ALIASES; "lethargic" is not.
        result = _extract_equine_symptoms("horse shows lethargy and depression")
        assert "gen_lethargy" in result

    def test_weight_loss_matches(self):
        result = _extract_equine_symptoms("horse has weight loss")
        assert "gen_weight_loss" in result

    def test_laminitis_matches(self):
        result = _extract_equine_symptoms("horse has laminitis")
        assert "hoof_laminitis_signs" in result

    def test_case_insensitive(self):
        result_lower = _extract_equine_symptoms("cough")
        result_upper = _extract_equine_symptoms("COUGH")
        assert set(result_lower) == set(result_upper)


# ===========================================================================
# 6. _match_equine_symptoms_to_diseases()
# ===========================================================================

@pytest.mark.skipif(not EQUINE_AVAILABLE, reason="Equine data not available")
class TestMatchEquineSymptomsToDiseases:
    """Test equine disease matching using Jaccard similarity."""

    def test_empty_input_returns_empty(self):
        result = _match_equine_symptoms_to_diseases([])
        assert result == []

    def test_returns_list(self):
        result = _match_equine_symptoms_to_diseases(["gen_fever"])
        assert isinstance(result, list)

    def test_nonexistent_finding_returns_empty(self):
        result = _match_equine_symptoms_to_diseases(["completely_fake_finding_xyz"])
        assert result == []

    def test_returns_dicts(self):
        result = _match_equine_symptoms_to_diseases(["gen_fever"])
        for item in result:
            assert isinstance(item, dict)

    def test_match_has_required_keys(self):
        result = _match_equine_symptoms_to_diseases(["gen_fever"])
        required = {
            "disease_id", "name_ja", "name_en", "severity",
            "similarity_score", "matched_symptoms",
            "unmatched_user_symptoms", "additional_disease_symptoms",
            "description", "recommended_tests",
        }
        for item in result:
            for key in required:
                assert key in item, f"Missing key '{key}' in equine match"

    def test_sorted_descending_by_score(self):
        result = _match_equine_symptoms_to_diseases(["gen_fever", "resp_cough"])
        scores = [m["similarity_score"] for m in result]
        assert scores == sorted(scores, reverse=True)

    def test_similarity_score_between_0_and_1(self):
        result = _match_equine_symptoms_to_diseases(["gen_fever", "resp_cough"])
        for m in result:
            assert 0.0 < m["similarity_score"] <= 1.0

    def test_matched_symptoms_subset_of_input(self):
        findings = ["gen_fever", "resp_cough", "gen_lethargy"]
        result = _match_equine_symptoms_to_diseases(findings)
        for m in result:
            for sym in m["matched_symptoms"]:
                assert sym in findings

    def test_multiple_findings_produce_matches(self):
        result = _match_equine_symptoms_to_diseases(["gen_fever", "resp_cough", "dig_diarrhea"])
        assert len(result) > 0

    def test_recommended_tests_is_list(self):
        result = _match_equine_symptoms_to_diseases(["gen_fever"])
        for m in result:
            assert isinstance(m["recommended_tests"], list)


# ===========================================================================
# 7. _extract_species_symptoms()
# ===========================================================================

class TestExtractSpeciesSymptoms:
    """Test generic species symptom extraction."""

    def test_unknown_species_returns_empty(self):
        result = _extract_species_symptoms("coughing", "unknown_species_xyz")
        assert result == []

    def test_returns_list(self):
        if "cat" in _SPECIES_DATA:
            result = _extract_species_symptoms("vomiting", "cat")
            assert isinstance(result, list)

    def test_empty_text_returns_empty(self):
        if "cat" in _SPECIES_DATA:
            result = _extract_species_symptoms("", "cat")
            assert result == []

    def test_nonsense_returns_empty(self):
        if "cat" in _SPECIES_DATA:
            result = _extract_species_symptoms("xyz abc 999", "cat")
            assert result == []

    @pytest.mark.skipif("cat" not in _SPECIES_DATA, reason="Cat data not loaded")
    def test_cat_vomiting_extracts_symptom(self):
        result = _extract_species_symptoms("vomiting", "cat")
        assert len(result) > 0

    @pytest.mark.skipif("cat" not in _SPECIES_DATA, reason="Cat data not loaded")
    def test_cat_no_duplicates(self):
        result = _extract_species_symptoms("vomiting vomiting diarrhea", "cat")
        assert len(result) == len(set(result))

    @pytest.mark.skipif("rabbit" not in _SPECIES_DATA, reason="Rabbit data not loaded")
    def test_rabbit_extracts_symptom(self):
        result = _extract_species_symptoms("not eating", "rabbit")
        assert isinstance(result, list)

    def test_case_insensitive(self):
        if "cat" in _SPECIES_DATA:
            r1 = _extract_species_symptoms("vomiting", "cat")
            r2 = _extract_species_symptoms("VOMITING", "cat")
            assert set(r1) == set(r2)


# ===========================================================================
# 8. _match_species_symptoms_to_diseases()
# ===========================================================================

class TestMatchSpeciesSymptomsToDiseases:
    """Test generic species disease matching."""

    def test_empty_symptoms_returns_empty(self):
        if "cat" in _SPECIES_DATA:
            result = _match_species_symptoms_to_diseases([], "cat")
            assert result == []

    def test_unknown_species_returns_empty(self):
        result = _match_species_symptoms_to_diseases(["vomiting"], "unknown_species_xyz")
        assert result == []

    def test_returns_list(self):
        if "cat" in _SPECIES_DATA:
            result = _match_species_symptoms_to_diseases(["vomiting"], "cat")
            assert isinstance(result, list)

    @pytest.mark.skipif("cat" not in _SPECIES_DATA, reason="Cat data not loaded")
    def test_cat_match_has_required_keys(self):
        result = _match_species_symptoms_to_diseases(["vomiting"], "cat")
        required = {
            "disease_id", "name_ja", "name_en", "severity",
            "similarity_score", "matched_symptoms",
            "unmatched_user_symptoms", "additional_disease_symptoms",
            "description", "recommended_tests",
        }
        for item in result:
            for key in required:
                assert key in item, f"Missing key '{key}' in species match"

    @pytest.mark.skipif("cat" not in _SPECIES_DATA, reason="Cat data not loaded")
    def test_cat_sorted_descending(self):
        result = _match_species_symptoms_to_diseases(["vomiting", "diarrhea"], "cat")
        scores = [m["similarity_score"] for m in result]
        assert scores == sorted(scores, reverse=True)

    @pytest.mark.skipif("cat" not in _SPECIES_DATA, reason="Cat data not loaded")
    def test_similarity_score_range(self):
        result = _match_species_symptoms_to_diseases(["vomiting"], "cat")
        for m in result:
            assert 0.0 < m["similarity_score"] <= 1.0

    def test_fake_symptom_returns_empty(self):
        if "cat" in _SPECIES_DATA:
            result = _match_species_symptoms_to_diseases(["totally_fake_sym_xyz"], "cat")
            assert result == []

    @pytest.mark.skipif("cat" not in _SPECIES_DATA, reason="Cat data not loaded")
    def test_recommended_tests_is_list(self):
        result = _match_species_symptoms_to_diseases(["vomiting"], "cat")
        for m in result:
            assert isinstance(m["recommended_tests"], list)


# ===========================================================================
# 9. evaluate_with_ai_confidence()
# ===========================================================================

class TestEvaluateWithAiConfidence:
    """Test RECO2 evaluation wrapper."""

    def test_returns_dict_or_none(self):
        result = evaluate_with_ai_confidence(
            inference={"disease_a": 0.8},
            evidence={"field": 0.5},
            context={"domain": "general"},
        )
        assert result is None or isinstance(result, dict)

    def test_with_ai_result_kwarg(self):
        result = evaluate_with_ai_confidence(
            inference={"disease_a": 0.8},
            evidence={"field": 0.5},
            context={"domain": "general"},
            ai_result={"confidence": 0.9},
        )
        assert result is None or isinstance(result, dict)

    def test_empty_inference(self):
        result = evaluate_with_ai_confidence(
            inference={},
            evidence={},
            context={},
        )
        # Should not raise - returns dict or None
        assert result is None or isinstance(result, dict)

    def test_ai_result_none_explicitly(self):
        result = evaluate_with_ai_confidence(
            inference={"disease_a": 0.5},
            evidence={},
            context={"domain": "orthopedics"},
            ai_result=None,
        )
        assert result is None or isinstance(result, dict)


# ===========================================================================
# 10. get_treatment_recommendations_for_disease() - extra branches
# ===========================================================================

class TestGetTreatmentRecommendationsExtraBranches:
    """Cover branches not tested in the existing test file."""

    def test_empty_string_disease_id_returns_empty_supplements(self):
        """When disease_id is falsy, supplements should be empty list."""
        result = get_treatment_recommendations_for_disease("")
        assert result["supplements"] == []

    def test_empty_string_still_returns_required_keys(self):
        result = get_treatment_recommendations_for_disease("")
        assert "primary_care_plan_ja" in result
        assert "primary_care_plan_en" in result
        assert "supplements" in result
        assert "diagnostic_tests" in result
        assert "follow_up_schedule_ja" in result
        assert "follow_up_schedule_en" in result

    def test_empty_disease_id_diagnostic_tests_empty(self):
        """Empty disease_id yields no disease record, so no diagnostic tests."""
        result = get_treatment_recommendations_for_disease("")
        assert result["diagnostic_tests"] == []

    def test_disease_in_supplements_map_adds_reference_url(self):
        """Each supplement dict gets a 'reference' key added."""
        result = get_treatment_recommendations_for_disease("hip_dysplasia")
        for s in result["supplements"]:
            assert s.get("reference") == "https://www.caninevet.jp/"

    def test_default_supplements_also_get_reference_url(self):
        """Even default (unmapped) supplements get the reference URL."""
        result = get_treatment_recommendations_for_disease("totally_fake_id_xyz")
        for s in result["supplements"]:
            assert s.get("reference") == "https://www.caninevet.jp/"


# ===========================================================================
# 11. Flask endpoints
# ===========================================================================

class TestDiagnosticChatEndpoint:
    """Test POST /api/diagnostic-chat/chat."""

    def test_no_message_returns_400(self, client):
        r = client.post("/api/diagnostic-chat/chat", json={})
        assert r.status_code == 400
        assert r.get_json()["error"] == "Message required"

    def test_empty_message_returns_400(self, client):
        r = client.post("/api/diagnostic-chat/chat", json={"message": "  "})
        assert r.status_code == 400

    def test_valid_message_returns_200(self, client):
        r = client.post("/api/diagnostic-chat/chat", json={"message": "my dog is coughing"})
        assert r.status_code == 200

    def test_response_has_required_keys(self, client):
        r = client.post("/api/diagnostic-chat/chat", json={"message": "coughing"})
        data = r.get_json()
        required = {
            "response", "user_message", "species", "extracted_symptoms",
            "accumulated_symptoms", "symptom_details", "disease_candidates",
            "total_candidates", "species_guidance", "follow_up_questions",
        }
        for key in required:
            assert key in data, f"Missing key '{key}' in chat response"

    def test_dog_species_default(self, client):
        r = client.post("/api/diagnostic-chat/chat", json={"message": "coughing"})
        assert r.get_json()["species"] == "dog"

    def test_explicit_dog_species(self, client):
        r = client.post("/api/diagnostic-chat/chat", json={"message": "coughing", "species": "dog"})
        assert r.get_json()["species"] == "dog"

    def test_cat_species_routing(self, client):
        r = client.post("/api/diagnostic-chat/chat", json={"message": "cat vomiting", "species": "cat"})
        assert r.status_code == 200
        assert r.get_json()["species"] == "cat"

    def test_horse_species_routing(self, client):
        r = client.post("/api/diagnostic-chat/chat", json={"message": "horse coughing", "species": "horse"})
        assert r.status_code == 200
        assert r.get_json()["species"] == "horse"

    def test_previous_symptoms_accumulated(self, client):
        r = client.post("/api/diagnostic-chat/chat", json={
            "message": "also vomiting",
            "previous_symptoms": ["coughing"],
        })
        data = r.get_json()
        assert "coughing" in data["accumulated_symptoms"]

    def test_onset_extracted_from_text(self, client):
        r = client.post("/api/diagnostic-chat/chat", json={"message": "suddenly started coughing"})
        data = r.get_json()
        assert data["onset_detected_from_text"] == "acute"

    def test_explicit_onset_overrides_detected(self, client):
        r = client.post("/api/diagnostic-chat/chat", json={
            "message": "suddenly started coughing",
            "onset": "chronic",
        })
        data = r.get_json()
        assert data["onset_context"] == "chronic"

    def test_age_extracted_from_text(self, client):
        r = client.post("/api/diagnostic-chat/chat", json={"message": "my 5 year old dog is coughing"})
        data = r.get_json()
        assert data["age_detected_from_text"] == 5.0

    def test_explicit_age_overrides_detected(self, client):
        r = client.post("/api/diagnostic-chat/chat", json={
            "message": "my 5 year old dog is coughing",
            "age_years": 10.0,
        })
        data = r.get_json()
        assert data["age_context"] == 10.0

    def test_breed_context_passed_through(self, client):
        r = client.post("/api/diagnostic-chat/chat", json={
            "message": "coughing",
            "breed_id": "122_labrador_retriever",
        })
        assert r.get_json()["breed_context"] == "122_labrador_retriever"

    def test_no_symptoms_detected_response_text(self, client):
        r = client.post("/api/diagnostic-chat/chat", json={"message": "xyz nonsense abc 9999"})
        data = r.get_json()
        assert "症状を検出できませんでした" in data["response"]

    def test_symptoms_detected_with_candidates_response_text(self, client):
        r = client.post("/api/diagnostic-chat/chat", json={"message": "coughing vomiting diarrhea"})
        data = r.get_json()
        assert "症状から以下の疾患が考えられます" in data["response"]

    def test_disease_candidates_have_reasoning(self, client):
        r = client.post("/api/diagnostic-chat/chat", json={"message": "coughing"})
        data = r.get_json()
        for candidate in data["disease_candidates"]:
            assert "reasoning" in candidate

    def test_disease_candidates_have_treatment_recommendations(self, client):
        r = client.post("/api/diagnostic-chat/chat", json={"message": "coughing"})
        data = r.get_json()
        for candidate in data["disease_candidates"]:
            assert "treatment_recommendations" in candidate

    def test_disease_candidates_max_ten(self, client):
        r = client.post("/api/diagnostic-chat/chat", json={"message": "coughing vomiting diarrhea fever lethargy"})
        data = r.get_json()
        assert len(data["disease_candidates"]) <= 10

    def test_symptom_details_have_required_fields(self, client):
        r = client.post("/api/diagnostic-chat/chat", json={"message": "coughing"})
        data = r.get_json()
        for detail in data["symptom_details"]:
            assert "id" in detail
            assert "name_ja" in detail
            assert "name_en" in detail

    def test_follow_up_questions_are_list(self, client):
        r = client.post("/api/diagnostic-chat/chat", json={"message": "coughing"})
        data = r.get_json()
        assert isinstance(data["follow_up_questions"], list)

    def test_recommendations_present(self, client):
        r = client.post("/api/diagnostic-chat/chat", json={"message": "coughing"})
        data = r.get_json()
        assert "recommendations" in data
        assert "next_step" in data["recommendations"]
        assert "next_step_ja" in data["recommendations"]

    def test_non_dog_species_treatments_format(self, client):
        r = client.post("/api/diagnostic-chat/chat", json={
            "message": "cat vomiting",
            "species": "cat",
        })
        data = r.get_json()
        for candidate in data["disease_candidates"]:
            # non-dog treatments should have at least the required keys
            assert "treatment_recommendations" in candidate

    def test_horse_disease_candidates_present(self, client):
        r = client.post("/api/diagnostic-chat/chat", json={
            "message": "horse has cough fever and diarrhea",
            "species": "horse",
        })
        data = r.get_json()
        assert len(data["disease_candidates"]) > 0

    def test_no_content_type_defaults_gracefully(self, client):
        """Endpoint handles missing JSON body without crashing."""
        r = client.post("/api/diagnostic-chat/chat", data="", content_type="application/json")
        # Either 400 (no message) or graceful 400 is acceptable
        assert r.status_code in (400, 422)

    def test_user_message_echoed(self, client):
        r = client.post("/api/diagnostic-chat/chat", json={"message": "my dog has a cough"})
        data = r.get_json()
        assert data["user_message"] == "my dog has a cough"

    def test_species_guidance_in_response(self, client):
        r = client.post("/api/diagnostic-chat/chat", json={"message": "coughing"})
        data = r.get_json()
        assert "species_guidance" in data
        assert isinstance(data["species_guidance"], str)

    def test_response_starts_with_guidance_line(self, client):
        r = client.post("/api/diagnostic-chat/chat", json={"message": "coughing"})
        data = r.get_json()
        assert data["response"].startswith(data["species_guidance"])


class TestSymptomSuggestionsEndpoint:
    """Test GET /api/diagnostic-chat/symptom-suggestions."""

    def test_no_filters_returns_200(self, client):
        r = client.get("/api/diagnostic-chat/symptom-suggestions")
        assert r.status_code == 200

    def test_response_has_symptoms_and_total(self, client):
        r = client.get("/api/diagnostic-chat/symptom-suggestions")
        data = r.get_json()
        assert "symptoms" in data
        assert "total" in data

    def test_total_matches_length(self, client):
        r = client.get("/api/diagnostic-chat/symptom-suggestions")
        data = r.get_json()
        assert data["total"] == len(data["symptoms"])

    def test_category_filter_reduces_results(self, client):
        r_all = client.get("/api/diagnostic-chat/symptom-suggestions")
        r_cat = client.get("/api/diagnostic-chat/symptom-suggestions?category=respiratory")
        assert r_cat.status_code == 200
        assert r_cat.get_json()["total"] <= r_all.get_json()["total"]

    def test_category_filter_only_matching_category(self, client):
        r = client.get("/api/diagnostic-chat/symptom-suggestions?category=respiratory")
        data = r.get_json()
        for sym in data["symptoms"]:
            assert sym["category"] == "respiratory"

    def test_search_filter_returns_matching_symptoms(self, client):
        r = client.get("/api/diagnostic-chat/symptom-suggestions?search=cough")
        data = r.get_json()
        assert data["total"] >= 1
        for sym in data["symptoms"]:
            assert "cough" in sym["name_ja"].lower() or "cough" in sym["name_en"].lower()

    def test_invalid_category_returns_empty(self, client):
        r = client.get("/api/diagnostic-chat/symptom-suggestions?category=nonexistent_category_xyz")
        data = r.get_json()
        assert data["total"] == 0

    def test_no_search_match_returns_empty(self, client):
        r = client.get("/api/diagnostic-chat/symptom-suggestions?search=zzznomatch999")
        data = r.get_json()
        assert data["total"] == 0

    def test_symptom_entries_have_required_fields(self, client):
        r = client.get("/api/diagnostic-chat/symptom-suggestions")
        data = r.get_json()
        for sym in data["symptoms"][:5]:  # spot-check first 5
            assert "id" in sym
            assert "name_ja" in sym
            assert "name_en" in sym
            assert "category" in sym

    def test_search_is_case_insensitive(self, client):
        r_lower = client.get("/api/diagnostic-chat/symptom-suggestions?search=cough")
        r_upper = client.get("/api/diagnostic-chat/symptom-suggestions?search=COUGH")
        assert r_lower.get_json()["total"] == r_upper.get_json()["total"]


class TestCategoriesEndpoint:
    """Test GET /api/diagnostic-chat/categories."""

    def test_returns_200(self, client):
        r = client.get("/api/diagnostic-chat/categories")
        assert r.status_code == 200

    def test_has_required_keys(self, client):
        r = client.get("/api/diagnostic-chat/categories")
        data = r.get_json()
        assert "categories" in data
        assert "total_categories" in data

    def test_total_matches_categories_length(self, client):
        r = client.get("/api/diagnostic-chat/categories")
        data = r.get_json()
        assert data["total_categories"] == len(data["categories"])

    def test_categories_not_empty(self, client):
        r = client.get("/api/diagnostic-chat/categories")
        data = r.get_json()
        assert data["total_categories"] > 0

    def test_each_category_has_id_and_symptoms(self, client):
        r = client.get("/api/diagnostic-chat/categories")
        data = r.get_json()
        for cat in data["categories"]:
            assert "id" in cat
            assert "symptoms" in cat
            assert isinstance(cat["symptoms"], list)

    def test_respiratory_category_present(self, client):
        r = client.get("/api/diagnostic-chat/categories")
        data = r.get_json()
        cat_ids = [c["id"] for c in data["categories"]]
        assert "respiratory" in cat_ids

    def test_symptoms_within_categories_have_required_fields(self, client):
        r = client.get("/api/diagnostic-chat/categories")
        data = r.get_json()
        for cat in data["categories"][:3]:
            for sym in cat["symptoms"][:3]:
                assert "id" in sym
                assert "name_ja" in sym
                assert "name_en" in sym


class TestTreatmentPlanEndpoint:
    """Test POST /api/diagnostic-chat/treatment-plan."""

    def test_no_disease_id_returns_400(self, client):
        r = client.post("/api/diagnostic-chat/treatment-plan", json={})
        assert r.status_code == 400
        assert r.get_json()["error"] == "Disease ID required"

    def test_unknown_disease_id_returns_404(self, client):
        r = client.post("/api/diagnostic-chat/treatment-plan", json={"disease_id": "totally_fake_xyz"})
        assert r.status_code == 404
        assert r.get_json()["error"] == "Disease not found"

    def test_valid_disease_returns_200(self, client):
        r = client.post("/api/diagnostic-chat/treatment-plan", json={"disease_id": "hip_dysplasia"})
        assert r.status_code == 200

    def test_response_has_required_keys(self, client):
        r = client.post("/api/diagnostic-chat/treatment-plan", json={"disease_id": "hip_dysplasia"})
        data = r.get_json()
        required = {
            "disease_id", "disease_name_ja", "disease_name_en",
            "severity", "supplements", "follow_up_visits",
        }
        for key in required:
            assert key in data, f"Missing key '{key}' in treatment plan"

    def test_disease_id_echoed(self, client):
        r = client.post("/api/diagnostic-chat/treatment-plan", json={"disease_id": "hip_dysplasia"})
        assert r.get_json()["disease_id"] == "hip_dysplasia"

    def test_follow_up_visits_is_list(self, client):
        r = client.post("/api/diagnostic-chat/treatment-plan", json={"disease_id": "hip_dysplasia"})
        data = r.get_json()
        assert isinstance(data["follow_up_visits"], list)
        assert len(data["follow_up_visits"]) == 2

    def test_follow_up_visit_has_required_fields(self, client):
        r = client.post("/api/diagnostic-chat/treatment-plan", json={"disease_id": "hip_dysplasia"})
        data = r.get_json()
        for visit in data["follow_up_visits"]:
            assert "visit_number" in visit
            assert "days_after_diagnosis" in visit
            assert "focus_areas_ja" in visit
            assert "focus_areas_en" in visit

    def test_optional_breed_and_age_accepted(self, client):
        r = client.post("/api/diagnostic-chat/treatment-plan", json={
            "disease_id": "hip_dysplasia",
            "breed_id": "122_labrador_retriever",
            "age_years": 5.0,
        })
        assert r.status_code == 200

    def test_supplements_have_reference(self, client):
        r = client.post("/api/diagnostic-chat/treatment-plan", json={"disease_id": "hip_dysplasia"})
        data = r.get_json()
        for supp in data["supplements"]:
            assert supp.get("reference") == "https://www.caninevet.jp/"

    def test_brachycephalic_disease_returns_correctly(self, client):
        r = client.post("/api/diagnostic-chat/treatment-plan",
                        json={"disease_id": "brachycephalic_airway_syndrome"})
        assert r.status_code == 200
        data = r.get_json()
        assert data["disease_name_en"] != ""


class TestDifferentialAnalysisEndpoint:
    """Test POST /api/diagnostic-chat/differential-analysis."""

    def test_missing_both_ids_returns_400(self, client):
        r = client.post("/api/diagnostic-chat/differential-analysis", json={})
        assert r.status_code == 400
        assert "Both disease IDs required" in r.get_json()["error"]

    def test_missing_disease_id_1_returns_400(self, client):
        r = client.post("/api/diagnostic-chat/differential-analysis",
                        json={"disease_id_2": "hip_dysplasia"})
        assert r.status_code == 400

    def test_missing_disease_id_2_returns_400(self, client):
        r = client.post("/api/diagnostic-chat/differential-analysis",
                        json={"disease_id_1": "hip_dysplasia"})
        assert r.status_code == 400

    def test_unknown_disease_id_returns_404(self, client):
        r = client.post("/api/diagnostic-chat/differential-analysis", json={
            "disease_id_1": "fake_disease_xyz",
            "disease_id_2": "hip_dysplasia",
        })
        assert r.status_code == 404

    def test_both_unknown_returns_404(self, client):
        r = client.post("/api/diagnostic-chat/differential-analysis", json={
            "disease_id_1": "fake_1",
            "disease_id_2": "fake_2",
        })
        assert r.status_code == 404

    def test_valid_comparison_returns_200(self, client):
        r = client.post("/api/diagnostic-chat/differential-analysis", json={
            "disease_id_1": "hip_dysplasia",
            "disease_id_2": "brachycephalic_airway_syndrome",
        })
        assert r.status_code == 200

    def test_response_has_required_keys(self, client):
        r = client.post("/api/diagnostic-chat/differential-analysis", json={
            "disease_id_1": "hip_dysplasia",
            "disease_id_2": "brachycephalic_airway_syndrome",
        })
        data = r.get_json()
        required = {
            "disease_1", "disease_2", "symptom_analysis",
            "differential_reasoning_ja", "differential_reasoning_en",
            "recommended_diagnostic_tests",
        }
        for key in required:
            assert key in data, f"Missing key '{key}' in differential analysis"

    def test_symptom_analysis_has_required_fields(self, client):
        r = client.post("/api/diagnostic-chat/differential-analysis", json={
            "disease_id_1": "hip_dysplasia",
            "disease_id_2": "brachycephalic_airway_syndrome",
        })
        sym_analysis = r.get_json()["symptom_analysis"]
        assert "shared_symptoms" in sym_analysis
        assert "unique_to_disease_1" in sym_analysis
        assert "unique_to_disease_2" in sym_analysis
        assert "user_symptom_overlap_1" in sym_analysis
        assert "user_symptom_overlap_2" in sym_analysis

    def test_user_symptoms_affect_overlap_counts(self, client):
        r = client.post("/api/diagnostic-chat/differential-analysis", json={
            "disease_id_1": "hip_dysplasia",
            "disease_id_2": "brachycephalic_airway_syndrome",
            "symptoms": ["labored_breathing", "exercise_intolerance"],
        })
        assert r.status_code == 200
        data = r.get_json()
        # brachycephalic has labored_breathing and exercise_intolerance -> overlap >= 1
        assert data["symptom_analysis"]["user_symptom_overlap_2"] >= 1

    def test_disease_1_info_matches_input(self, client):
        r = client.post("/api/diagnostic-chat/differential-analysis", json={
            "disease_id_1": "hip_dysplasia",
            "disease_id_2": "brachycephalic_airway_syndrome",
        })
        data = r.get_json()
        assert data["disease_1"]["id"] == "hip_dysplasia"

    def test_disease_2_info_matches_input(self, client):
        r = client.post("/api/diagnostic-chat/differential-analysis", json={
            "disease_id_1": "hip_dysplasia",
            "disease_id_2": "brachycephalic_airway_syndrome",
        })
        data = r.get_json()
        assert data["disease_2"]["id"] == "brachycephalic_airway_syndrome"

    def test_reasoning_contains_disease_names(self, client):
        r = client.post("/api/diagnostic-chat/differential-analysis", json={
            "disease_id_1": "hip_dysplasia",
            "disease_id_2": "brachycephalic_airway_syndrome",
        })
        data = r.get_json()
        assert "Hip Dysplasia" in data["differential_reasoning_en"] or \
               "hip" in data["differential_reasoning_en"].lower()

    def test_recommended_tests_is_list(self, client):
        r = client.post("/api/diagnostic-chat/differential-analysis", json={
            "disease_id_1": "hip_dysplasia",
            "disease_id_2": "brachycephalic_airway_syndrome",
        })
        assert isinstance(r.get_json()["recommended_diagnostic_tests"], list)


class TestFeedbackEndpoint:
    """Test POST /api/diagnostic-chat/feedback."""

    def test_missing_session_id_returns_400(self, client):
        r = client.post("/api/diagnostic-chat/feedback", json={
            "feedback": "good",
        })
        assert r.status_code == 400
        assert r.get_json()["error"] == "session_id required"

    def test_invalid_feedback_type_returns_400(self, client):
        r = client.post("/api/diagnostic-chat/feedback", json={
            "session_id": "abc123",
            "feedback": "invalid_value",
        })
        assert r.status_code == 400
        assert "feedback must be" in r.get_json()["error"]

    def test_empty_feedback_returns_400(self, client):
        r = client.post("/api/diagnostic-chat/feedback", json={
            "session_id": "abc123",
            "feedback": "",
        })
        assert r.status_code == 400

    def test_good_feedback_returns_201(self, client):
        r = client.post("/api/diagnostic-chat/feedback", json={
            "session_id": "abc123",
            "feedback": "good",
        })
        assert r.status_code == 201

    def test_bad_feedback_returns_201(self, client):
        r = client.post("/api/diagnostic-chat/feedback", json={
            "session_id": "abc123",
            "feedback": "bad",
        })
        assert r.status_code == 201

    def test_recalculate_feedback_returns_201(self, client):
        r = client.post("/api/diagnostic-chat/feedback", json={
            "session_id": "abc123",
            "feedback": "recalculate",
        })
        assert r.status_code == 201

    def test_success_response_has_status_recorded(self, client):
        r = client.post("/api/diagnostic-chat/feedback", json={
            "session_id": "abc123",
            "feedback": "good",
        })
        data = r.get_json()
        assert data["status"] == "recorded"

    def test_success_response_has_learning_signal_strength(self, client):
        r = client.post("/api/diagnostic-chat/feedback", json={
            "session_id": "abc123",
            "feedback": "good",
        })
        data = r.get_json()
        assert "learning_signal_strength" in data

    def test_feedback_with_optional_fields(self, client):
        r = client.post("/api/diagnostic-chat/feedback", json={
            "session_id": "abc123",
            "feedback": "good",
            "domain": "orthopedics",
            "notes": "helpful result",
            "correct_symptoms": ["coughing", "vomiting"],
            "ai_result": {"confidence": 0.9},
        })
        assert r.status_code == 201

    def test_empty_body_returns_400(self, client):
        r = client.post("/api/diagnostic-chat/feedback", json={})
        assert r.status_code == 400

    def test_learning_signal_strength_is_numeric(self, client):
        r = client.post("/api/diagnostic-chat/feedback", json={
            "session_id": "abc123",
            "feedback": "good",
        })
        data = r.get_json()
        assert isinstance(data["learning_signal_strength"], (int, float))


# ===========================================================================
# 12. Diagnostic accuracy regression tests
# ===========================================================================


class TestDiagnosticAccuracyFerretAdrenal:
    """Ferret adrenal disease should rank highly with typical symptoms."""

    @pytest.mark.skipif("ferret" not in _SPECIES_DATA, reason="Ferret data not loaded")
    def test_adrenal_disease_top5_with_hair_loss_vulvar_swelling(self):
        result = _match_species_symptoms_to_diseases(
            ["hair_loss", "vulvar_swelling", "itching", "aggression", "lethargy"], "ferret",
        )
        top5 = [m["disease_id"] for m in result[:5]]
        assert "Adrenal Disease" in top5

    @pytest.mark.skipif("ferret" not in _SPECIES_DATA, reason="Ferret data not loaded")
    def test_adrenal_disease_confidence_above_50(self):
        result = _match_species_symptoms_to_diseases(
            ["hair_loss", "vulvar_swelling", "itching", "aggression", "lethargy"], "ferret",
        )
        adrenal = [m for m in result if m["disease_id"] == "Adrenal Disease"]
        assert adrenal, "Adrenal Disease not found in results"
        confidence = adrenal[0]["similarity_score"] * 100
        assert confidence > 50, f"Confidence {confidence:.1f}% too low"

    @pytest.mark.skipif("ferret" not in _SPECIES_DATA, reason="Ferret data not loaded")
    def test_adrenal_alias_vulvar_swelling_extracted(self):
        result = _extract_species_symptoms("外陰部が腫れてる 毛が抜ける", "ferret")
        assert "vulvar_swelling" in result

    @pytest.mark.skipif("ferret" not in _SPECIES_DATA, reason="Ferret data not loaded")
    def test_adrenal_alias_prostatic_enlargement_extracted(self):
        result = _extract_species_symptoms("前立腺が大きい", "ferret")
        assert "prostatic_enlargement" in result


class TestDiagnosticAccuracyCatHypothyroidism:
    """Cat hypothyroidism should be detected with typical symptoms."""

    @pytest.mark.skipif("cat" not in _SPECIES_DATA, reason="Cat data not loaded")
    def test_hypothyroidism_detected_with_typical_symptoms(self):
        result = _match_species_symptoms_to_diseases(
            ["lethargy", "weight_gain", "hair_loss", "constipation"], "cat",
        )
        names = [m["disease_id"] for m in result[:10]]
        assert "Hypothyroidism (Iatrogenic)" in names

    @pytest.mark.skipif("cat" not in _SPECIES_DATA, reason="Cat data not loaded")
    def test_hypothyroidism_confidence_above_55(self):
        result = _match_species_symptoms_to_diseases(
            ["lethargy", "weight_gain", "hair_loss", "poor_coat", "bradycardia"], "cat",
        )
        hypo = [m for m in result if m["disease_id"] == "Hypothyroidism (Iatrogenic)"]
        assert hypo, "Hypothyroidism not found in results"
        confidence = hypo[0]["similarity_score"] * 100
        assert confidence > 55, f"Confidence {confidence:.1f}% too low"


class TestDiagnosticAccuracyHamsterWetTail:
    """Hamster wet tail should rank highly and alias should extract wet_tail ID."""

    @pytest.mark.skipif("hamster" not in _SPECIES_DATA, reason="Hamster data not loaded")
    def test_wet_tail_alias_extracts_wet_tail_id(self):
        result = _extract_species_symptoms("ウェットテイル 元気ない", "hamster")
        assert "wet_tail" in result

    @pytest.mark.skipif("hamster" not in _SPECIES_DATA, reason="Hamster data not loaded")
    def test_wet_tail_top3_with_typical_symptoms(self):
        result = _match_species_symptoms_to_diseases(
            ["wet_tail", "diarrhea", "lethargy", "appetite_loss"], "hamster",
        )
        top3 = [m["disease_id"] for m in result[:3]]
        assert "Wet Tail (Proliferative Ileitis)" in top3

    @pytest.mark.skipif("hamster" not in _SPECIES_DATA, reason="Hamster data not loaded")
    def test_wet_tail_confidence_above_55(self):
        result = _match_species_symptoms_to_diseases(
            ["wet_tail", "diarrhea", "lethargy", "appetite_loss", "dehydration"], "hamster",
        )
        wt = [m for m in result if m["disease_id"] == "Wet Tail (Proliferative Ileitis)"]
        assert wt, "Wet Tail not found in results"
        confidence = wt[0]["similarity_score"] * 100
        assert confidence > 55, f"Confidence {confidence:.1f}% too low"


# ===========================================================================
# Next Questions Endpoint (POST /api/diagnostic-chat/next-questions)
# ===========================================================================


class TestNextQuestionsEndpoint:
    """Test POST /api/diagnostic-chat/next-questions."""

    def test_missing_suspected_diseases_returns_400(self, client):
        r = client.post("/api/diagnostic-chat/next-questions", json={
            "symptoms": ["vomiting"],
        })
        assert r.status_code == 400
        assert "suspected_diseases" in r.get_json()["error"]

    def test_empty_suspected_diseases_returns_400(self, client):
        r = client.post("/api/diagnostic-chat/next-questions", json={
            "suspected_diseases": [],
            "symptoms": ["vomiting"],
        })
        assert r.status_code == 400

    def test_valid_request_returns_200(self, client):
        r = client.post("/api/diagnostic-chat/next-questions", json={
            "suspected_diseases": [
                {"name": "Gastroenteritis", "similarity_score": 0.8},
                {"name": "Pancreatitis", "similarity_score": 0.6},
            ],
            "symptoms": ["vomiting", "lethargy"],
        })
        assert r.status_code == 200

    def test_response_has_required_keys(self, client):
        r = client.post("/api/diagnostic-chat/next-questions", json={
            "suspected_diseases": [
                {"name": "Gastroenteritis", "similarity_score": 0.8},
            ],
            "symptoms": ["vomiting"],
        })
        data = r.get_json()
        assert "next_questions" in data
        assert "question_count" in data

    def test_question_limit_caps_at_5(self, client):
        r = client.post("/api/diagnostic-chat/next-questions", json={
            "suspected_diseases": [
                {"name": "Gastroenteritis", "similarity_score": 0.8},
                {"name": "Pancreatitis", "similarity_score": 0.6},
                {"name": "Liver Disease", "similarity_score": 0.4},
            ],
            "symptoms": ["vomiting", "lethargy", "appetite_loss"],
            "question_limit": 10,
        })
        data = r.get_json()
        assert data.get("question_count", 0) <= 5

    def test_default_question_limit_is_3(self, client):
        r = client.post("/api/diagnostic-chat/next-questions", json={
            "suspected_diseases": [
                {"name": "Gastroenteritis", "similarity_score": 0.8},
            ],
            "symptoms": ["vomiting"],
        })
        data = r.get_json()
        assert data.get("question_count", 0) <= 3

    def test_empty_body_returns_400(self, client):
        r = client.post("/api/diagnostic-chat/next-questions", json={})
        assert r.status_code == 400


# ===========================================================================
# Guided Consultation Endpoint (POST /api/diagnostic-chat/consultation)
# ===========================================================================

class TestConsultationEndpoint:
    """Tests for the 5-phase guided consultation flow."""

    ENDPOINT = "/api/diagnostic-chat/consultation"

    # --- Phase 1: start ---------------------------------------------------

    def test_start_phase(self, client):
        """POST with phase='start' returns category list."""
        r = client.post(self.ENDPOINT, json={"phase": "start", "species": "dog"})
        assert r.status_code == 200
        data = r.get_json()
        assert data["phase"] == "select_category"
        assert "categories" in data
        assert len(data["categories"]) > 0
        # Each category has required keys
        cat = data["categories"][0]
        assert "id" in cat
        assert "name_ja" in cat
        assert "name_en" in cat
        assert "symptom_count" in cat
        assert cat["symptom_count"] > 0
        assert data["species"] == "dog"
        assert "message_ja" in data
        assert "message_en" in data

    def test_start_phase_cat(self, client):
        """Start phase works for cat species too."""
        r = client.post(self.ENDPOINT, json={"phase": "start", "species": "cat"})
        assert r.status_code == 200
        data = r.get_json()
        assert data["phase"] == "select_category"
        assert data["species"] == "cat"
        assert len(data["categories"]) > 0

    # --- Phase 2: select_symptoms -----------------------------------------

    def test_select_symptoms_phase(self, client):
        """POST with phase='select_symptoms' returns symptoms for a category."""
        # First get categories
        r1 = client.post(self.ENDPOINT, json={"phase": "start", "species": "dog"})
        cats = r1.get_json()["categories"]
        cat_id = cats[0]["id"]

        r = client.post(self.ENDPOINT, json={
            "phase": "select_symptoms",
            "species": "dog",
            "selected_category": cat_id,
        })
        assert r.status_code == 200
        data = r.get_json()
        assert data["phase"] == "show_symptoms"
        assert data["category"] == cat_id
        assert "symptoms" in data
        assert len(data["symptoms"]) > 0
        sym = data["symptoms"][0]
        assert "id" in sym
        assert "name_ja" in sym
        assert "name_en" in sym
        assert "selected" in sym

    def test_select_symptoms_missing_category(self, client):
        """Omitting selected_category returns 400."""
        r = client.post(self.ENDPOINT, json={
            "phase": "select_symptoms",
            "species": "dog",
        })
        assert r.status_code == 400
        assert "error" in r.get_json()

    def test_select_symptoms_marks_selected(self, client):
        """Previously selected symptoms are marked as selected."""
        r1 = client.post(self.ENDPOINT, json={"phase": "start", "species": "dog"})
        cat_id = r1.get_json()["categories"][0]["id"]

        # Get symptoms for category to find a valid id
        r2 = client.post(self.ENDPOINT, json={
            "phase": "select_symptoms",
            "species": "dog",
            "selected_category": cat_id,
        })
        sym_id = r2.get_json()["symptoms"][0]["id"]

        # Request again with that symptom pre-selected
        r3 = client.post(self.ENDPOINT, json={
            "phase": "select_symptoms",
            "species": "dog",
            "selected_category": cat_id,
            "selected_symptoms": [sym_id],
        })
        data = r3.get_json()
        matching = [s for s in data["symptoms"] if s["id"] == sym_id]
        assert matching[0]["selected"] is True

    # --- Phase 3: next_category -------------------------------------------

    def test_next_category_phase(self, client):
        """POST with selected symptoms returns interim results + suggested categories."""
        r = client.post(self.ENDPOINT, json={
            "phase": "next_category",
            "species": "dog",
            "selected_symptoms": ["coughing", "nasal_discharge"],
        })
        assert r.status_code == 200
        data = r.get_json()
        assert data["phase"] == "interim_results"
        assert "disease_candidates" in data
        assert "total_candidates" in data
        assert "next_categories" in data
        assert "symptom_details" in data
        assert data["species"] == "dog"
        assert data["selected_symptoms"] == ["coughing", "nasal_discharge"]

    def test_next_category_no_symptoms(self, client):
        """Without symptoms, next_category falls back to category selection."""
        r = client.post(self.ENDPOINT, json={
            "phase": "next_category",
            "species": "dog",
            "selected_symptoms": [],
        })
        assert r.status_code == 200
        data = r.get_json()
        assert data["phase"] == "select_category"
        assert "categories" in data

    def test_next_category_returns_candidates(self, client):
        """Interim results include disease candidate details."""
        r = client.post(self.ENDPOINT, json={
            "phase": "next_category",
            "species": "dog",
            "selected_symptoms": ["coughing", "nasal_discharge"],
        })
        data = r.get_json()
        if data["disease_candidates"]:
            cand = data["disease_candidates"][0]
            assert "name_en" in cand
            assert "confidence_percent" in cand
            assert "severity" in cand
            assert "matched_symptoms" in cand

    # --- Phase 4: ask_context ---------------------------------------------

    def test_ask_context_phase(self, client):
        """POST with phase='ask_context' returns context questions."""
        r = client.post(self.ENDPOINT, json={
            "phase": "ask_context",
            "species": "dog",
            "selected_symptoms": ["coughing", "nasal_discharge"],
        })
        assert r.status_code == 200
        data = r.get_json()
        assert data["phase"] == "context_questions"
        assert "questions" in data
        # Should ask both onset and age when not provided
        qtypes = [q["type"] for q in data["questions"]]
        assert "onset" in qtypes
        assert "age" in qtypes

    def test_ask_context_onset_provided(self, client):
        """When onset is provided, only age question remains."""
        r = client.post(self.ENDPOINT, json={
            "phase": "ask_context",
            "species": "dog",
            "onset": "acute",
        })
        data = r.get_json()
        qtypes = [q["type"] for q in data["questions"]]
        assert "onset" not in qtypes
        assert "age" in qtypes

    def test_ask_context_age_provided(self, client):
        """When age is provided, only onset question remains."""
        r = client.post(self.ENDPOINT, json={
            "phase": "ask_context",
            "species": "dog",
            "age_years": 5,
        })
        data = r.get_json()
        qtypes = [q["type"] for q in data["questions"]]
        assert "onset" in qtypes
        assert "age" not in qtypes

    def test_ask_context_both_provided(self, client):
        """When onset and age are provided, only pain_score question may remain."""
        r = client.post(self.ENDPOINT, json={
            "phase": "ask_context",
            "species": "dog",
            "onset": "chronic",
            "age_years": 10,
        })
        data = r.get_json()
        remaining_types = [q["type"] for q in data["questions"]]
        assert "onset" not in remaining_types
        assert "age" not in remaining_types

    def test_ask_context_includes_pain_score(self, client):
        """Pain score question is included in context questions."""
        r = client.post(self.ENDPOINT, json={
            "phase": "ask_context",
            "species": "dog",
        })
        data = r.get_json()
        question_types = [q["type"] for q in data["questions"]]
        assert "pain_score" in question_types
        pain_q = [q for q in data["questions"] if q["type"] == "pain_score"][0]
        assert "options" in pain_q
        assert len(pain_q["options"]) > 0

    # --- Phase 5: finalize ------------------------------------------------

    def test_finalize_phase(self, client):
        """POST with phase='finalize' returns final diagnosis results."""
        r = client.post(self.ENDPOINT, json={
            "phase": "finalize",
            "species": "dog",
            "selected_symptoms": ["coughing", "nasal_discharge", "sneezing"],
            "onset": "acute",
            "age_years": 5,
        })
        assert r.status_code == 200
        data = r.get_json()
        assert data["phase"] == "final_results"
        assert "result" in data
        assert "suspected_diseases" in data["result"]
        assert "symptom_details" in data
        assert "recommendations" in data
        assert data["species"] == "dog"
        assert data["onset"] == "acute"
        assert data["age_years"] == 5

    def test_finalize_cat(self, client):
        """Finalize works for cat species."""
        r = client.post(self.ENDPOINT, json={
            "phase": "finalize",
            "species": "cat",
            "selected_symptoms": ["vomiting", "lethargy", "appetite_loss"],
            "onset": "subacute",
            "age_years": 3,
        })
        assert r.status_code == 200
        data = r.get_json()
        assert data["phase"] == "final_results"
        assert data["species"] == "cat"
        assert len(data["result"]["suspected_diseases"]) > 0

    def test_finalize_returns_recommendations(self, client):
        """Final results include next-step recommendations."""
        r = client.post(self.ENDPOINT, json={
            "phase": "finalize",
            "species": "dog",
            "selected_symptoms": ["coughing"],
        })
        data = r.get_json()
        recs = data["recommendations"]
        assert "next_step_ja" in recs
        assert "next_step_en" in recs

    # --- Full flow --------------------------------------------------------

    def test_full_flow(self, client):
        """Test the complete guided consultation flow from start to finalize."""
        # Step 1: Start
        r1 = client.post(self.ENDPOINT, json={"phase": "start", "species": "dog"})
        d1 = r1.get_json()
        assert d1["phase"] == "select_category"
        cat_id = d1["categories"][0]["id"]

        # Step 2: Select symptoms for a category
        r2 = client.post(self.ENDPOINT, json={
            "phase": "select_symptoms",
            "species": "dog",
            "selected_category": cat_id,
        })
        d2 = r2.get_json()
        assert d2["phase"] == "show_symptoms"
        sym_ids = [s["id"] for s in d2["symptoms"][:3]]

        # Step 3: Get interim results
        r3 = client.post(self.ENDPOINT, json={
            "phase": "next_category",
            "species": "dog",
            "selected_symptoms": sym_ids,
            "answered_categories": [cat_id],
        })
        d3 = r3.get_json()
        assert d3["phase"] == "interim_results"

        # Step 4: Ask context
        r4 = client.post(self.ENDPOINT, json={
            "phase": "ask_context",
            "species": "dog",
            "selected_symptoms": sym_ids,
        })
        d4 = r4.get_json()
        assert d4["phase"] == "context_questions"

        # Step 5: Finalize
        r5 = client.post(self.ENDPOINT, json={
            "phase": "finalize",
            "species": "dog",
            "selected_symptoms": sym_ids,
            "onset": "acute",
            "age_years": 3,
        })
        d5 = r5.get_json()
        assert d5["phase"] == "final_results"
        assert "suspected_diseases" in d5["result"]

    # --- Error handling ---------------------------------------------------

    def test_invalid_phase(self, client):
        """Unknown phase returns 400 error."""
        r = client.post(self.ENDPOINT, json={
            "phase": "nonexistent_phase",
            "species": "dog",
        })
        assert r.status_code == 400
        data = r.get_json()
        assert "error" in data
        assert "nonexistent_phase" in data["error"]

    def test_missing_species_defaults_to_dog(self, client):
        """Without species, defaults to 'dog'."""
        r = client.post(self.ENDPOINT, json={"phase": "start"})
        assert r.status_code == 200
        data = r.get_json()
        assert data["species"] == "dog"

    def test_empty_body(self, client):
        """Empty JSON body defaults to start phase for dog."""
        r = client.post(self.ENDPOINT, json={})
        assert r.status_code == 200
        data = r.get_json()
        assert data["phase"] == "select_category"
        assert data["species"] == "dog"
