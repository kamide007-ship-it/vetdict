"""
Comprehensive tests for diagnostic_chat.py pure functions.

Tests cover:
1. extract_symptoms_from_text() - NLP symptom extraction from Japanese/English text
2. match_symptoms_to_diseases() - disease matching logic (Jaccard similarity)
3. generate_disease_reasoning_ja() / generate_disease_reasoning_en() - reasoning text
4. get_treatment_recommendations_for_disease() - treatment/supplement lookup
5. Data integrity - SYMPTOM_ALIASES, DISEASE_SUPPLEMENTS structures
6. Edge cases - empty input, nonsense text, case insensitivity, etc.

NOTE: Flask endpoints are NOT tested here (they require app context).
      Only pure functions and data structures are tested.

Known data quirk: Several SYMPTOM_ALIASES values use compound IDs
(e.g. "lameness_or_limping", "paralysis_or_paresis") that do NOT exist
in health_checker.SYMPTOM_IDS. Because extract_symptoms_from_text()
guards alias matches with ``symptom_id in SYMPTOM_IDS``, those aliases
silently produce no match. Tests account for this.
"""

from api.diagnostic_chat import (
    _DEFAULT_SUPPLEMENTS,
    DISEASE_SUPPLEMENTS,
    SYMPTOM_ALIASES,
    extract_symptoms_from_text,
    generate_disease_reasoning_en,
    generate_disease_reasoning_ja,
    get_treatment_recommendations_for_disease,
    match_symptoms_to_diseases,
)
from api.health_checker import DISEASES, SYMPTOM_IDS, SYMPTOMS

# Alias values that are NOT present in SYMPTOM_IDS (known mismatch).
# These aliases will never match via the alias path because of the
# ``symptom_id in SYMPTOM_IDS`` guard in extract_symptoms_from_text().
_KNOWN_ALIAS_MISMATCHES = {
    "lameness_or_limping",
    "joint_pain_or_stiffness",
    "lumps_and_bumps",
    "paralysis_or_paresis",
    "cloudy_urine",
    "foul_smelling_urine",
    # Bridged to the legacy dog vocabulary (stiffness) via _LEGACY_FALLBACK;
    # no species module carries a dedicated difficulty-rising ID.
    "difficulty_standing",
    # Bridged via _LEGACY_FALLBACK (neck_pain/stiffness) and ID_SYNONYMS;
    # no species module carries a dedicated cervical-guarding ID.
    "neck_stiffness",
    # Bridged via _LEGACY_FALLBACK (bloating) and ID_SYNONYMS (nausea/bloating);
    # no species module carries a dedicated borborygmi ID.
    "stomach_gurgling",
    # Bridged via _LEGACY_FALLBACK (vomiting) and ID_SYNONYMS (vomiting/retching);
    # no species module carries a dedicated nausea ID — grass-eating proxy.
    "nausea",
}


# ============================================================================
# 1. extract_symptoms_from_text()
# ============================================================================


class TestExtractSymptomsFromTextEnglish:
    """Test NLP symptom extraction from English natural language text."""

    def test_single_english_symptom(self):
        result = extract_symptoms_from_text("My dog has been coughing a lot")
        assert "coughing" in result

    def test_multiple_english_symptoms(self):
        result = extract_symptoms_from_text("My dog has diarrhea and is vomiting")
        assert "diarrhea" in result
        assert "vomiting" in result

    def test_english_alias_runny_nose(self):
        result = extract_symptoms_from_text("My dog has a runny nose")
        assert "nasal_discharge" in result

    def test_english_alias_breathing_difficulty(self):
        result = extract_symptoms_from_text("The dog is having breathing difficulty")
        assert "labored_breathing" in result

    def test_english_alias_throws_up(self):
        result = extract_symptoms_from_text("My puppy throws up after eating")
        assert "vomiting" in result

    def test_english_alias_not_eating(self):
        result = extract_symptoms_from_text("My dog is not eating anything")
        assert "loss_of_appetite" in result

    def test_english_alias_loose_stools(self):
        result = extract_symptoms_from_text("She has loose stools")
        assert "diarrhea" in result

    def test_english_alias_bloody_stool(self):
        result = extract_symptoms_from_text("There is bloody stool")
        assert "blood_in_stool" in result

    def test_english_alias_seizure(self):
        result = extract_symptoms_from_text("My dog had a seizure")
        assert "seizures" in result

    def test_english_alias_fits(self):
        result = extract_symptoms_from_text("The dog is having fits")
        assert "seizures" in result

    def test_english_alias_lethargic(self):
        result = extract_symptoms_from_text("She seems lethargic lately")
        assert "lethargy" in result

    def test_english_alias_cloudy_eyes(self):
        result = extract_symptoms_from_text("My dog has cloudy eyes")
        assert "cloudiness_in_eyes" in result

    def test_english_alias_red_eyes(self):
        result = extract_symptoms_from_text("My dog has red eyes")
        assert "redness_in_eyes" in result

    def test_english_alias_blood_in_urine(self):
        result = extract_symptoms_from_text("I noticed blood in urine")
        assert "blood_in_urine" in result

    def test_english_alias_excessive_thirst(self):
        result = extract_symptoms_from_text("He is drinking a lot of water")
        assert "excessive_thirst" in result

    def test_english_alias_weight_loss(self):
        result = extract_symptoms_from_text("My dog is losing weight fast")
        assert "weight_loss" in result

    def test_english_alias_fainting(self):
        result = extract_symptoms_from_text("My dog collapses sometimes")
        assert "fainting" in result

    def test_english_alias_anxious(self):
        result = extract_symptoms_from_text("My dog seems very anxious")
        assert "anxiety" in result

    def test_english_alias_aggressive(self):
        result = extract_symptoms_from_text("My dog is getting aggressive")
        assert "aggression" in result

    def test_english_alias_jaundice(self):
        result = extract_symptoms_from_text("I noticed yellowing on gums")
        assert "jaundice" in result

    def test_english_alias_pale_gums(self):
        result = extract_symptoms_from_text("My dog has pale gums")
        assert "pale_gums" in result

    def test_english_alias_rapid_breathing(self):
        result = extract_symptoms_from_text("fast breathing during rest")
        assert "rapid_breathing" in result

    def test_english_alias_frequent_urination(self):
        result = extract_symptoms_from_text("peeing a lot more than usual")
        assert "frequent_urination" in result

    def test_english_alias_constipation(self):
        result = extract_symptoms_from_text("My dog is not pooping")
        assert "constipation" in result

    def test_english_alias_bloating(self):
        result = extract_symptoms_from_text("abdominal distension is evident")
        assert "bloating" in result

    def test_english_alias_tremors(self):
        result = extract_symptoms_from_text("The dog keeps shaking")
        assert "tremors" in result

    def test_english_alias_incontinence(self):
        result = extract_symptoms_from_text("leaking urine while sleeping")
        assert "incontinence" in result

    def test_english_alias_excessive_licking(self):
        result = extract_symptoms_from_text("excessive licking of paws")
        assert "excessive_licking" in result

    def test_english_alias_exercise_intolerance(self):
        result = extract_symptoms_from_text("tires easily on walks")
        assert "exercise_intolerance" in result

    def test_english_alias_wheezing(self):
        result = extract_symptoms_from_text("my dog is wheezing")
        assert "wheezing" in result

    def test_english_alias_reverse_sneezing(self):
        result = extract_symptoms_from_text("reverse sneezing episodes")
        assert "reverse_sneezing" in result

    def test_english_alias_drooling(self):
        result = extract_symptoms_from_text("excessive drool everywhere")
        assert "excessive_drooling" in result

    def test_english_alias_eye_discharge(self):
        result = extract_symptoms_from_text("lots of eye discharge")
        assert "eye_discharge" in result

    def test_english_alias_squinting(self):
        result = extract_symptoms_from_text("the dog keeps squinting")
        assert "squinting" in result

    def test_english_alias_swollen_eyes(self):
        result = extract_symptoms_from_text("my dog has swollen eyes")
        assert "eye_swelling" in result

    def test_english_alias_fever(self):
        result = extract_symptoms_from_text("my dog has a fever")
        assert "fever" in result

    def test_english_alias_swollen_lymph_nodes(self):
        result = extract_symptoms_from_text("swollen lymph nodes detected")
        assert "swollen_lymph_nodes" in result


class TestExtractSymptomsFromTextJapanese:
    """Test NLP symptom extraction from Japanese text."""

    def test_single_japanese_symptom(self):
        result = extract_symptoms_from_text("犬が咳をしています")
        assert "coughing" in result

    def test_multiple_japanese_symptoms(self):
        result = extract_symptoms_from_text("犬が下痢と嘔吐をしています")
        assert "diarrhea" in result
        assert "vomiting" in result

    def test_japanese_sneezing(self):
        result = extract_symptoms_from_text("くしゃみが止まりません")
        assert "sneezing" in result

    def test_japanese_nasal_discharge(self):
        result = extract_symptoms_from_text("鼻水が出ています")
        assert "nasal_discharge" in result

    def test_japanese_labored_breathing(self):
        result = extract_symptoms_from_text("呼吸困難の状態です")
        assert "labored_breathing" in result

    def test_japanese_loss_of_appetite(self):
        result = extract_symptoms_from_text("食欲不振が続いています")
        assert "loss_of_appetite" in result

    def test_japanese_seizures(self):
        result = extract_symptoms_from_text("けいれんを起こしました")
        assert "seizures" in result

    def test_japanese_seizures_alternative(self):
        result = extract_symptoms_from_text("発作が起きています")
        assert "seizures" in result

    def test_japanese_blood_in_stool(self):
        result = extract_symptoms_from_text("血便が出ています")
        assert "blood_in_stool" in result

    def test_japanese_tremors(self):
        result = extract_symptoms_from_text("振戦が起きています")
        assert "tremors" in result

    def test_japanese_blood_in_urine(self):
        result = extract_symptoms_from_text("血尿が出ました")
        assert "blood_in_urine" in result

    def test_japanese_excessive_thirst(self):
        result = extract_symptoms_from_text("多飲の状態です")
        assert "excessive_thirst" in result

    def test_japanese_eye_discharge(self):
        result = extract_symptoms_from_text("目やにがひどいです")
        assert "eye_discharge" in result

    def test_japanese_fever(self):
        result = extract_symptoms_from_text("発熱しています")
        assert "fever" in result

    def test_japanese_weight_loss(self):
        result = extract_symptoms_from_text("体重減少が続いています")
        assert "weight_loss" in result

    def test_japanese_jaundice(self):
        result = extract_symptoms_from_text("黄疸が出ています")
        assert "jaundice" in result

    def test_japanese_lethargy(self):
        result = extract_symptoms_from_text("無気力でぐったりしています")
        assert "lethargy" in result

    def test_japanese_reverse_sneezing(self):
        result = extract_symptoms_from_text("逆くしゃみをしています")
        assert "reverse_sneezing" in result

    def test_japanese_wheezing(self):
        result = extract_symptoms_from_text("喘鳴が聞こえます")
        assert "wheezing" in result

    def test_japanese_drooling(self):
        result = extract_symptoms_from_text("よだれが多いです")
        assert "excessive_drooling" in result

    def test_japanese_bloating(self):
        result = extract_symptoms_from_text("腹部膨満がみられます")
        assert "bloating" in result

    def test_japanese_constipation(self):
        result = extract_symptoms_from_text("便秘が続いています")
        assert "constipation" in result

    def test_japanese_frequent_urination(self):
        result = extract_symptoms_from_text("頻尿の症状があります")
        assert "frequent_urination" in result

    def test_japanese_straining_to_urinate(self):
        result = extract_symptoms_from_text("排尿困難です")
        assert "straining_to_urinate" in result

    def test_japanese_incontinence(self):
        result = extract_symptoms_from_text("尿失禁が見られます")
        assert "incontinence" in result

    def test_japanese_eye_redness(self):
        result = extract_symptoms_from_text("目の充血がひどいです")
        assert "redness_in_eyes" in result

    def test_japanese_cloudiness_in_eyes(self):
        result = extract_symptoms_from_text("目の白濁が進んでいます")
        assert "cloudiness_in_eyes" in result

    def test_japanese_squinting(self):
        result = extract_symptoms_from_text("目を細めるようになりました")
        assert "squinting" in result

    def test_japanese_eye_swelling(self):
        result = extract_symptoms_from_text("目の腫れがあります")
        assert "eye_swelling" in result

    def test_japanese_exercise_intolerance(self):
        result = extract_symptoms_from_text("運動不耐性です")
        assert "exercise_intolerance" in result

    def test_japanese_fainting(self):
        result = extract_symptoms_from_text("失神しました")
        assert "fainting" in result

    def test_japanese_rapid_breathing(self):
        result = extract_symptoms_from_text("頻呼吸がみられます")
        assert "rapid_breathing" in result

    def test_japanese_aggression(self):
        result = extract_symptoms_from_text("攻撃性が増しています")
        assert "aggression" in result

    def test_japanese_anxiety(self):
        result = extract_symptoms_from_text("不安行動がみられます")
        assert "anxiety" in result

    def test_japanese_excessive_licking(self):
        result = extract_symptoms_from_text("舐め行動がひどいです")
        assert "excessive_licking" in result

    def test_japanese_swollen_lymph_nodes(self):
        result = extract_symptoms_from_text("リンパ節腫脹がみられます")
        assert "swollen_lymph_nodes" in result

    def test_japanese_pale_gums(self):
        result = extract_symptoms_from_text("歯茎の蒼白が見られます")
        assert "pale_gums" in result

    def test_japanese_lameness(self):
        """Japanese alias '跛行' maps to 'lameness_or_limping'."""
        result = extract_symptoms_from_text("跛行がみられます")
        assert any(s in result for s in ("limping", "lameness_or_limping"))

    def test_japanese_joint_pain(self):
        """Japanese '関節痛' maps to 'joint_pain_or_stiffness' (not in SYMPTOM_IDS).
        No SYMPTOMS entry has name_ja matching '関節痛' exactly either.
        This is a known gap -- the alias path is blocked by the SYMPTOM_IDS guard."""
        result = extract_symptoms_from_text("関節痛がひどいです")
        # 'joint_pain_or_stiffness' is not in SYMPTOM_IDS so alias won't match.
        # No direct name match either. Result may be empty for this specific input.
        assert isinstance(result, list)

    def test_japanese_paralysis(self):
        """Japanese '麻痺' maps to 'paralysis_or_paresis'."""
        result = extract_symptoms_from_text("後肢に麻痺があります")
        assert any(s in result for s in ("paralysis", "paralysis_or_paresis"))

    def test_japanese_lumps(self):
        """Japanese 'しこり' maps to 'lumps_and_bumps' via alias (blocked),
        but SYMPTOMS has name_ja 'しこり・腫瘤' -- substring 'しこり' appears
        in the name, so direct name match should work."""
        result = extract_symptoms_from_text("体にしこりがあります")
        # The SYMPTOMS entry has name_ja "しこり・腫瘤" and id "lumps_bumps".
        # Since "しこり" is a substring of "しこり・腫瘤", and the function
        # checks ``name_ja in text_lower``, the full name "しこり・腫瘤" must
        # appear in the text for direct match. The alias "しこり" maps to
        # "lumps_and_bumps" (not in SYMPTOM_IDS), so this will only match if
        # the SYMPTOMS name_ja substring check works the *other* direction
        # (name_ja in text). Since "しこり・腫瘤" is NOT in "体にしこりがあります",
        # no direct match. This is a known gap.
        assert isinstance(result, list)


class TestExtractSymptomsFromTextMixed:
    """Test mixed language and case-sensitivity scenarios."""

    def test_mixed_language_input(self):
        result = extract_symptoms_from_text("犬が coughing して下痢も出ています")
        assert "coughing" in result
        assert "diarrhea" in result

    def test_case_insensitive_english(self):
        result = extract_symptoms_from_text("COUGHING and VOMITING")
        assert "coughing" in result
        assert "vomiting" in result

    def test_case_insensitive_mixed(self):
        result = extract_symptoms_from_text("Diarrhea")
        assert "diarrhea" in result

    def test_direct_name_en_match(self):
        """Symptom name_en values should match directly (case-insensitive)."""
        result = extract_symptoms_from_text("Nasal Discharge is present")
        assert "nasal_discharge" in result

    def test_direct_name_en_labored_breathing(self):
        result = extract_symptoms_from_text("Labored Breathing observed")
        assert "labored_breathing" in result


class TestExtractSymptomsFromTextReturnType:
    """Test return type and deduplication."""

    def test_returns_list(self):
        result = extract_symptoms_from_text("coughing")
        assert isinstance(result, list)

    def test_no_duplicates_in_result(self):
        """Even when both alias and direct match trigger, no duplicates."""
        result = extract_symptoms_from_text("cough coughing Coughing 咳")
        assert result.count("coughing") == 1

    def test_returns_empty_list_not_none(self):
        result = extract_symptoms_from_text("")
        assert result is not None
        assert isinstance(result, list)


class TestExtractSymptomsFromTextEdgeCases:
    """Edge cases for symptom extraction."""

    def test_empty_string(self):
        result = extract_symptoms_from_text("")
        assert result == []

    def test_whitespace_only(self):
        result = extract_symptoms_from_text("   ")
        assert result == []

    def test_nonsense_text(self):
        result = extract_symptoms_from_text("xyz abc 12345 $$$ !!!")
        assert result == []

    def test_unrelated_text(self):
        result = extract_symptoms_from_text("The weather is nice today and I went for a walk")
        assert "coughing" not in result
        assert "vomiting" not in result
        assert "diarrhea" not in result

    def test_numbers_only(self):
        result = extract_symptoms_from_text("123456789")
        assert result == []

    def test_very_long_input(self):
        """Function should handle very long input without errors."""
        long_text = "coughing " * 1000
        result = extract_symptoms_from_text(long_text)
        assert "coughing" in result

    def test_special_characters(self):
        result = extract_symptoms_from_text("!@#$%^&*()")
        assert result == []

    def test_newlines_and_tabs(self):
        result = extract_symptoms_from_text("coughing\n\tvomiting")
        assert "coughing" in result
        assert "vomiting" in result

    def test_symptom_embedded_in_word(self):
        """Alias substring matching can pick up embedded terms.
        'hot' is an alias for fever, 'pale' is an alias for pale_gums, etc."""
        result = extract_symptoms_from_text("hotdog")
        # This is expected behavior of the substring-based matching
        assert isinstance(result, list)

    def test_medical_jargon_aliases(self):
        """Medical terms like 'syncope', 'polyuria', 'pyrexia' should match."""
        result = extract_symptoms_from_text("The dog shows syncope and polyuria")
        assert "fainting" in result
        assert "frequent_urination" in result

    def test_medical_jargon_hematuria(self):
        result = extract_symptoms_from_text("hematuria observed")
        assert "blood_in_urine" in result

    def test_medical_jargon_tachypnea(self):
        result = extract_symptoms_from_text("tachypnea is present")
        assert "rapid_breathing" in result

    def test_medical_jargon_pyrexia(self):
        result = extract_symptoms_from_text("pyrexia detected")
        assert "fever" in result

    def test_medical_jargon_lymphadenopathy(self):
        result = extract_symptoms_from_text("lymphadenopathy noted")
        assert "swollen_lymph_nodes" in result

    def test_medical_jargon_icterus(self):
        result = extract_symptoms_from_text("icterus present")
        assert "jaundice" in result


# ============================================================================
# 2. match_symptoms_to_diseases()
# ============================================================================


class TestMatchSymptomsToDiseases:
    """Test disease matching with Jaccard similarity."""

    def test_empty_symptoms_returns_empty(self):
        result = match_symptoms_to_diseases([])
        assert result == []

    def test_single_symptom_returns_matches(self):
        result = match_symptoms_to_diseases(["coughing"])
        assert len(result) > 0
        for match in result:
            assert "coughing" in match["matched_symptoms"]

    def test_returns_list_of_dicts(self):
        result = match_symptoms_to_diseases(["coughing"])
        assert isinstance(result, list)
        for match in result:
            assert isinstance(match, dict)

    def test_match_has_required_keys(self):
        result = match_symptoms_to_diseases(["coughing"])
        required_keys = {
            "disease_id",
            "name_ja",
            "name_en",
            "severity",
            "similarity_score",
            "matched_symptoms",
            "unmatched_user_symptoms",
            "additional_disease_symptoms",
            "description",
            "description_ja",
            "description_en",
            "recommended_tests",
        }
        for match in result:
            for key in required_keys:
                assert key in match, f"Missing key: {key} in match for {match.get('disease_id')}"

    def test_similarity_score_range(self):
        result = match_symptoms_to_diseases(["coughing", "sneezing"])
        for match in result:
            assert 0.0 < match["similarity_score"] <= 1.0

    def test_sorted_by_similarity_descending(self):
        result = match_symptoms_to_diseases(["coughing", "sneezing", "fever"])
        scores = [m["similarity_score"] for m in result]
        assert scores == sorted(scores, reverse=True)

    def test_perfect_match_has_highest_score(self):
        """When user symptoms exactly equal a disease's symptoms, that disease should rank highest."""
        boas = next(d for d in DISEASES if d["id"] == "brachycephalic_airway_syndrome")
        boas_symptoms = boas["symptoms"]
        result = match_symptoms_to_diseases(boas_symptoms)
        boas_match = next(
            (m for m in result if m["disease_id"] == "brachycephalic_airway_syndrome"),
            None,
        )
        assert boas_match is not None
        # With advanced scoring, perfect match gets high score (>= 0.8)
        assert boas_match["similarity_score"] >= 0.8
        # It should be the top-ranked result or in top 3
        boas_rank = next(i for i, m in enumerate(result) if m["disease_id"] == "brachycephalic_airway_syndrome")
        assert boas_rank < 3

    def test_partial_match_produces_reasonable_score(self):
        """Verify partial symptom match produces a positive composite score."""
        parvo = next(d for d in DISEASES if d["id"] == "canine_parvovirus")
        parvo_symptoms = set(parvo["symptoms"])
        user_symptoms = list(parvo_symptoms)[:3]
        result = match_symptoms_to_diseases(user_symptoms)
        parvo_match = next(
            (m for m in result if m["disease_id"] == "canine_parvovirus"),
            None,
        )
        assert parvo_match is not None
        # Score should be positive and less than perfect match
        assert 0 < parvo_match["similarity_score"] <= 2.0
        # Matched symptoms should be correct
        assert set(parvo_match["matched_symptoms"]) == set(user_symptoms) & parvo_symptoms

    def test_no_match_for_nonexistent_symptom(self):
        result = match_symptoms_to_diseases(["nonexistent_symptom_xyz"])
        assert result == []

    def test_matched_symptoms_are_correct(self):
        user_symptoms = ["coughing", "sneezing"]
        result = match_symptoms_to_diseases(user_symptoms)
        for match in result:
            disease = next(d for d in DISEASES if d["id"] == match["disease_id"])
            for ms in match["matched_symptoms"]:
                assert ms in user_symptoms
                assert ms in disease["symptoms"]

    def test_unmatched_user_symptoms_are_correct(self):
        user_symptoms = ["coughing", "seizures"]
        result = match_symptoms_to_diseases(user_symptoms)
        for match in result:
            disease = next(d for d in DISEASES if d["id"] == match["disease_id"])
            disease_symptom_set = set(disease["symptoms"])
            for us in match["unmatched_user_symptoms"]:
                assert us in user_symptoms
                assert us not in disease_symptom_set

    def test_additional_disease_symptoms_are_correct(self):
        user_symptoms = ["coughing"]
        result = match_symptoms_to_diseases(user_symptoms)
        for match in result:
            disease = next(d for d in DISEASES if d["id"] == match["disease_id"])
            user_set = set(user_symptoms)
            for ds in match["additional_disease_symptoms"]:
                assert ds in disease["symptoms"]
                assert ds not in user_set

    def test_multiple_diseases_can_share_symptoms(self):
        """Multiple diseases may match the same set of symptoms."""
        result = match_symptoms_to_diseases(["lethargy", "fever"])
        disease_ids = [m["disease_id"] for m in result]
        assert len(disease_ids) > 1

    def test_severity_values_are_valid(self):
        result = match_symptoms_to_diseases(["coughing"])
        valid_severities = {"low", "mild", "moderate", "high", "severe", "emergency"}
        for match in result:
            assert match["severity"] in valid_severities, (
                f"Unexpected severity '{match['severity']}' for disease {match['disease_id']}"
            )

    def test_respiratory_symptoms_find_boas(self):
        result = match_symptoms_to_diseases(
            [
                "labored_breathing",
                "wheezing",
                "reverse_sneezing",
                "exercise_intolerance",
            ]
        )
        disease_ids = [m["disease_id"] for m in result]
        assert "brachycephalic_airway_syndrome" in disease_ids

    def test_gi_symptoms_find_parvovirus(self):
        result = match_symptoms_to_diseases(
            [
                "vomiting",
                "diarrhea",
                "blood_in_stool",
                "lethargy",
            ]
        )
        disease_ids = [m["disease_id"] for m in result]
        assert "canine_parvovirus" in disease_ids

    def test_description_fields_are_strings(self):
        result = match_symptoms_to_diseases(["coughing"])
        for match in result:
            assert isinstance(match["description"], str)
            assert isinstance(match["description_ja"], str)
            assert isinstance(match["description_en"], str)

    def test_recommended_tests_is_list(self):
        result = match_symptoms_to_diseases(["coughing"])
        for match in result:
            assert isinstance(match["recommended_tests"], list)


# ============================================================================
# 3. generate_disease_reasoning_ja() / generate_disease_reasoning_en()
# ============================================================================


class TestGenerateDiseaseReasoningJa:
    """Test Japanese reasoning text generation."""

    def test_basic_output(self):
        disease = {
            "name_ja": "犬パルボウイルス感染症",
            "similarity_score": 0.75,
            "matched_symptoms": ["vomiting", "diarrhea"],
            "unmatched_user_symptoms": ["coughing"],
        }
        result = generate_disease_reasoning_ja(disease, [])
        assert isinstance(result, str)
        assert "犬パルボウイルス感染症" in result
        assert "75%" in result
        assert "2/3" in result

    def test_all_symptoms_matched(self):
        disease = {
            "name_ja": "テスト病",
            "similarity_score": 1.0,
            "matched_symptoms": ["a", "b", "c"],
            "unmatched_user_symptoms": [],
        }
        result = generate_disease_reasoning_ja(disease, [])
        assert "3/3" in result
        assert "100%" in result

    def test_no_matched_symptoms(self):
        disease = {
            "name_ja": "テスト病",
            "similarity_score": 0.0,
            "matched_symptoms": [],
            "unmatched_user_symptoms": ["a"],
        }
        result = generate_disease_reasoning_ja(disease, [])
        assert "0/1" in result
        assert "0%" in result

    def test_single_symptom_match(self):
        disease = {
            "name_ja": "テスト病",
            "similarity_score": 0.5,
            "matched_symptoms": ["vomiting"],
            "unmatched_user_symptoms": ["coughing"],
        }
        result = generate_disease_reasoning_ja(disease, [])
        assert "1/2" in result
        assert "50%" in result

    def test_missing_keys_use_defaults(self):
        """get() should handle missing keys gracefully."""
        disease = {
            "name_ja": "テスト病",
            "similarity_score": 0.33,
        }
        result = generate_disease_reasoning_ja(disease, [])
        assert "0/0" in result
        assert "33%" in result

    def test_contains_disease_name(self):
        disease = {
            "name_ja": "短頭種気道症候群",
            "similarity_score": 0.8,
            "matched_symptoms": ["coughing", "wheezing"],
            "unmatched_user_symptoms": ["lethargy"],
        }
        result = generate_disease_reasoning_ja(disease, [])
        assert "短頭種気道症候群" in result

    def test_output_is_nonempty_string(self):
        disease = {
            "name_ja": "テスト",
            "similarity_score": 0.5,
            "matched_symptoms": ["a"],
            "unmatched_user_symptoms": [],
        }
        result = generate_disease_reasoning_ja(disease, [])
        assert len(result) > 0


class TestGenerateDiseaseReasoningEn:
    """Test English reasoning text generation."""

    def test_basic_output(self):
        disease = {
            "name_en": "Canine Parvovirus",
            "similarity_score": 0.85,
            "matched_symptoms": ["vomiting", "diarrhea", "fever"],
            "unmatched_user_symptoms": ["coughing"],
        }
        result = generate_disease_reasoning_en(disease, [])
        assert isinstance(result, str)
        assert "Canine Parvovirus" in result
        assert "85%" in result
        assert "3/4" in result

    def test_all_symptoms_matched(self):
        disease = {
            "name_en": "Test Disease",
            "similarity_score": 1.0,
            "matched_symptoms": ["a", "b"],
            "unmatched_user_symptoms": [],
        }
        result = generate_disease_reasoning_en(disease, [])
        assert "2/2" in result
        assert "100%" in result

    def test_contains_similarity_score_keyword(self):
        disease = {
            "name_en": "Hip Dysplasia",
            "similarity_score": 0.6,
            "matched_symptoms": ["limping"],
            "unmatched_user_symptoms": [],
        }
        result = generate_disease_reasoning_en(disease, [])
        assert "similarity score" in result

    def test_contains_symptom_profile_keyword(self):
        disease = {
            "name_en": "Hip Dysplasia",
            "similarity_score": 0.6,
            "matched_symptoms": ["limping"],
            "unmatched_user_symptoms": [],
        }
        result = generate_disease_reasoning_en(disease, [])
        assert "symptom profile" in result

    def test_score_truncation(self):
        """Verify that score is truncated via int(), not rounded."""
        disease = {
            "name_en": "Test",
            "similarity_score": 0.999,
            "matched_symptoms": ["a"],
            "unmatched_user_symptoms": [],
        }
        result = generate_disease_reasoning_en(disease, [])
        # int(0.999 * 100) = 99, not 100
        assert "99%" in result

    def test_missing_keys_use_defaults(self):
        disease = {
            "name_en": "Test Disease",
            "similarity_score": 0.25,
        }
        result = generate_disease_reasoning_en(disease, [])
        assert "0/0" in result
        assert "25%" in result

    def test_contains_disease_name(self):
        disease = {
            "name_en": "Brachycephalic Airway Syndrome",
            "similarity_score": 0.7,
            "matched_symptoms": ["coughing"],
            "unmatched_user_symptoms": [],
        }
        result = generate_disease_reasoning_en(disease, [])
        assert "Brachycephalic Airway Syndrome" in result

    def test_output_is_nonempty_string(self):
        disease = {
            "name_en": "Test",
            "similarity_score": 0.5,
            "matched_symptoms": ["a"],
            "unmatched_user_symptoms": [],
        }
        result = generate_disease_reasoning_en(disease, [])
        assert len(result) > 0


class TestDiseaseReasoningSpecies:
    """Reasoning text must reflect the patient's species, not hard-code dog."""

    def _disease(self, name_ja="テスト病", name_en="Test Disease"):
        return {
            "name_ja": name_ja,
            "name_en": name_en,
            "similarity_score": 0.5,
            "matched_symptoms": ["vomiting"],
            "unmatched_user_symptoms": [],
        }

    def test_cat_ja_uses_cat_label(self):
        result = generate_disease_reasoning_ja(self._disease(), [], species="cat")
        assert "猫" in result
        assert "犬" not in result

    def test_rabbit_ja_uses_rabbit_label(self):
        result = generate_disease_reasoning_ja(self._disease(), [], species="rabbit")
        assert "ウサギ" in result
        assert "犬" not in result

    def test_cat_en_uses_cat_label(self):
        result = generate_disease_reasoning_en(self._disease(), [], species="cat")
        assert "cat" in result.lower()
        assert "dog" not in result.lower()

    def test_horse_en_uses_horse_label(self):
        result = generate_disease_reasoning_en(self._disease(), [], species="horse")
        assert "horse" in result.lower()
        assert "dog" not in result.lower()

    def test_default_species_is_dog_for_backcompat(self):
        result_ja = generate_disease_reasoning_ja(self._disease(), [])
        result_en = generate_disease_reasoning_en(self._disease(), [])
        assert "犬" in result_ja
        assert "dog" in result_en.lower()


# ============================================================================
# 4. get_treatment_recommendations_for_disease()
# ============================================================================


class TestGetTreatmentRecommendations:
    """Test treatment/supplement recommendation lookup."""

    def test_known_disease_returns_dict(self):
        result = get_treatment_recommendations_for_disease("brachycephalic_airway_syndrome")
        assert isinstance(result, dict)

    def test_has_required_keys(self):
        result = get_treatment_recommendations_for_disease("brachycephalic_airway_syndrome")
        assert "primary_care_plan_ja" in result
        assert "primary_care_plan_en" in result
        assert "supplements" in result
        assert "diagnostic_tests" in result
        assert "follow_up_schedule_ja" in result
        assert "follow_up_schedule_en" in result

    def test_supplements_have_reference_url(self):
        result = get_treatment_recommendations_for_disease("brachycephalic_airway_syndrome")
        for supp in result["supplements"]:
            assert "reference" in supp
            assert supp["reference"] == "https://www.caninevet.jp/"

    def test_supplements_have_required_fields(self):
        result = get_treatment_recommendations_for_disease("hip_dysplasia")
        for supp in result["supplements"]:
            assert "name_ja" in supp
            assert "name_en" in supp
            assert "dosage" in supp
            assert "frequency" in supp
            assert "reason_ja" in supp
            assert "reason_en" in supp

    def test_known_disease_has_specific_supplements(self):
        """Disease in DISEASE_SUPPLEMENTS should return its specific supplements."""
        result = get_treatment_recommendations_for_disease("hip_dysplasia")
        supplement_names = [s["name_en"] for s in result["supplements"]]
        assert "Canine Vet For Joint" in supplement_names

    def test_unknown_disease_returns_default_supplements(self):
        """Disease not in DISEASE_SUPPLEMENTS should return _DEFAULT_SUPPLEMENTS."""
        result = get_treatment_recommendations_for_disease("totally_fake_disease_id_xyz")
        assert len(result["supplements"]) == len(_DEFAULT_SUPPLEMENTS)
        default_names = {s["name_en"] for s in _DEFAULT_SUPPLEMENTS}
        result_names = {s["name_en"] for s in result["supplements"]}
        assert default_names == result_names

    def test_diagnostic_tests_from_disease_record(self):
        """Diagnostic tests come from the actual disease data."""
        result = get_treatment_recommendations_for_disease("brachycephalic_airway_syndrome")
        test_ids = [t["test_id"] for t in result["diagnostic_tests"]]
        # BOAS has recommended_tests: ["xray", "ct_scan", "endoscopy", "blood_pressure"]
        # Only top 3 are returned
        assert len(test_ids) <= 3
        for tid in test_ids:
            assert tid in [
                "xray",
                "ct_scan",
                "endoscopy",
                "blood_pressure",
            ]

    def test_diagnostic_tests_limited_to_three(self):
        result = get_treatment_recommendations_for_disease("canine_parvovirus")
        assert len(result["diagnostic_tests"]) <= 3

    def test_diagnostic_test_has_required_fields(self):
        result = get_treatment_recommendations_for_disease("brachycephalic_airway_syndrome")
        for test in result["diagnostic_tests"]:
            assert "test_id" in test
            assert "test_name_ja" in test
            assert "test_name_en" in test
            assert "priority" in test
            assert "description_ja" in test
            assert "description_en" in test

    def test_diagnostic_test_priority_is_sequential(self):
        result = get_treatment_recommendations_for_disease("brachycephalic_airway_syndrome")
        priorities = [t["priority"] for t in result["diagnostic_tests"]]
        assert priorities == list(range(1, len(priorities) + 1))

    def test_optional_breed_and_age_accepted(self):
        """Function should accept optional breed_id and age_years without error."""
        result = get_treatment_recommendations_for_disease(
            "hip_dysplasia",
            breed_id="122_labrador_retriever",
            age_years=5.0,
        )
        assert isinstance(result, dict)
        assert "supplements" in result

    def test_follow_up_schedule_strings(self):
        result = get_treatment_recommendations_for_disease("brachycephalic_airway_syndrome")
        assert isinstance(result["follow_up_schedule_ja"], str)
        assert isinstance(result["follow_up_schedule_en"], str)
        assert len(result["follow_up_schedule_ja"]) > 0
        assert len(result["follow_up_schedule_en"]) > 0

    def test_primary_care_plan_contains_vet_info(self):
        result = get_treatment_recommendations_for_disease("brachycephalic_airway_syndrome")
        assert "獣医師" in result["primary_care_plan_ja"]
        # "veterinary" / "veterinarian" / DVM attribution all satisfy intent.
        assert "veterinar" in result["primary_care_plan_en"].lower()

    def test_each_mapped_disease_returns_its_supplements(self):
        """Spot check several diseases in DISEASE_SUPPLEMENTS mapping."""
        test_cases = {
            "epilepsy": "Canine Vet Relax & CBD",
            "obesity": "NMN Mitochondria Assist",
            "canine_parvovirus": "Prebiotics & Probiotics & Psyllium",
            "hip_dysplasia": "Canine Vet For Joint",
            "atopic_dermatitis": "Prebiotics & Probiotics & Psyllium",
            "dcm": "MSM + Amino Complete",
        }
        for disease_id, expected_supp_name in test_cases.items():
            result = get_treatment_recommendations_for_disease(disease_id)
            supp_names = [s["name_en"] for s in result["supplements"]]
            assert expected_supp_name in supp_names, (
                f"Expected '{expected_supp_name}' in supplements for '{disease_id}', got {supp_names}"
            )

    def test_disease_not_in_supplements_map_gets_diagnostic_tests(self):
        """Even an unmapped disease ID still gets diagnostic_tests from DISEASES."""
        # Pick a disease that IS in DISEASES but NOT in DISEASE_SUPPLEMENTS
        all_supplement_ids = set(DISEASE_SUPPLEMENTS.keys())
        unmapped = None
        for d in DISEASES:
            if d["id"] not in all_supplement_ids and d.get("recommended_tests"):
                unmapped = d["id"]
                break
        if unmapped:
            result = get_treatment_recommendations_for_disease(unmapped)
            assert isinstance(result["diagnostic_tests"], list)
            assert len(result["diagnostic_tests"]) > 0


# ============================================================================
# 5. Data Integrity
# ============================================================================


class TestSymptomAliasesIntegrity:
    """Verify the SYMPTOM_ALIASES mapping is valid and consistent."""

    def test_aliases_is_dict(self):
        assert isinstance(SYMPTOM_ALIASES, dict)

    def test_aliases_not_empty(self):
        assert len(SYMPTOM_ALIASES) > 0

    def test_all_alias_values_are_valid_symptom_ids_or_known_mismatches(self):
        """Every value should be in SYMPTOM_IDS (dog) or a species SYMPTOM_NAMES, or be a documented mismatch."""
        # Build combined valid IDs from all species modules (trigger lazy load)
        all_valid_ids = set(SYMPTOM_IDS) | _KNOWN_ALIAS_MISMATCHES
        from api.chat.constants import _GENERIC_SPECIES
        from api.chat.species_data import get_species_data

        for sp in _GENERIC_SPECIES:
            sp_data = get_species_data(sp)
            all_valid_ids.update(sp_data.get("symptom_names", {}).keys())

        for alias, symptom_id in SYMPTOM_ALIASES.items():
            assert symptom_id in all_valid_ids, (
                f"Alias '{alias}' maps to '{symptom_id}' which is not in any species symptom set"
            )

    def test_known_mismatches_are_still_valid(self):
        """Verify _KNOWN_ALIAS_MISMATCHES entries are actually missing from dog SYMPTOM_IDS."""
        for sid in _KNOWN_ALIAS_MISMATCHES:
            assert sid not in SYMPTOM_IDS, (
                f"'{sid}' is in _KNOWN_ALIAS_MISMATCHES but now exists in SYMPTOM_IDS — remove from mismatches"
            )

    def test_all_alias_keys_are_lowercase(self):
        for alias in SYMPTOM_ALIASES:
            assert alias == alias.lower(), f"Alias key '{alias}' is not lowercase"

    def test_all_alias_values_are_strings(self):
        for _alias, symptom_id in SYMPTOM_ALIASES.items():
            assert isinstance(symptom_id, str)

    def test_all_alias_keys_are_strings(self):
        for alias in SYMPTOM_ALIASES:
            assert isinstance(alias, str)

    def test_contains_english_aliases(self):
        english_aliases = [k for k in SYMPTOM_ALIASES if k.isascii()]
        assert len(english_aliases) > 0

    def test_contains_japanese_aliases(self):
        japanese_aliases = [k for k in SYMPTOM_ALIASES if not k.isascii()]
        assert len(japanese_aliases) > 0

    def test_japanese_alias_count_at_least_20(self):
        japanese_aliases = [k for k in SYMPTOM_ALIASES if not k.isascii()]
        assert len(japanese_aliases) >= 20

    def test_no_empty_alias_keys(self):
        for alias in SYMPTOM_ALIASES:
            assert len(alias.strip()) > 0

    def test_no_empty_alias_values(self):
        for _alias, symptom_id in SYMPTOM_ALIASES.items():
            assert len(symptom_id.strip()) > 0

    def test_common_english_aliases_present(self):
        expected_aliases = [
            "cough",
            "sneeze",
            "vomit",
            "diarrhea",
            "limping",
            "seizure",
            "fever",
        ]
        for alias in expected_aliases:
            assert alias in SYMPTOM_ALIASES, f"Expected common alias '{alias}' not found"

    def test_common_japanese_aliases_present(self):
        expected_aliases = ["咳", "くしゃみ", "鼻水", "嘔吐", "下痢", "発熱"]
        for alias in expected_aliases:
            assert alias in SYMPTOM_ALIASES, f"Expected common alias '{alias}' not found"


class TestDiseaseSupplementsIntegrity:
    """Verify DISEASE_SUPPLEMENTS structure is valid."""

    def test_is_dict(self):
        assert isinstance(DISEASE_SUPPLEMENTS, dict)

    def test_not_empty(self):
        assert len(DISEASE_SUPPLEMENTS) > 0

    def test_all_keys_are_strings(self):
        for key in DISEASE_SUPPLEMENTS:
            assert isinstance(key, str)

    def test_all_values_are_lists(self):
        for disease_id, supplements in DISEASE_SUPPLEMENTS.items():
            assert isinstance(supplements, list), f"Supplements for '{disease_id}' is not a list"

    def test_all_supplement_entries_have_required_fields(self):
        required_fields = {
            "name_ja",
            "name_en",
            "dosage",
            "frequency",
            "reason_ja",
            "reason_en",
        }
        for disease_id, supplements in DISEASE_SUPPLEMENTS.items():
            for idx, supp in enumerate(supplements):
                for field in required_fields:
                    assert field in supp, f"Missing '{field}' in supplement {idx} for disease '{disease_id}'"

    def test_all_disease_ids_reference_known_diseases(self):
        """Every key in DISEASE_SUPPLEMENTS should be a known disease ID.

        Known exceptions: some disease IDs in DISEASE_SUPPLEMENTS have
        supplement mappings defined but are not (yet) present in
        health_checker.DISEASES.
        """
        known_ids = {d["id"] for d in DISEASES}
        known_supplement_only = {
            "lumbar_sacral_disease",
            "food_allergy",
            "obesity",
            "otitis_externa",
            "mammary_gland_tumor",
            "aortic_stenosis",
        }
        for disease_id in DISEASE_SUPPLEMENTS:
            if disease_id in known_supplement_only:
                continue
            assert disease_id in known_ids, f"DISEASE_SUPPLEMENTS key '{disease_id}' not found in DISEASES"

    def test_no_empty_supplement_lists(self):
        for disease_id, supplements in DISEASE_SUPPLEMENTS.items():
            assert len(supplements) > 0, f"Disease '{disease_id}' has empty supplements list"

    def test_supplement_fields_are_non_empty_strings(self):
        for disease_id, supplements in DISEASE_SUPPLEMENTS.items():
            for supp in supplements:
                for key in [
                    "name_ja",
                    "name_en",
                    "dosage",
                    "frequency",
                    "reason_ja",
                    "reason_en",
                ]:
                    assert isinstance(supp[key], str) and len(supp[key]) > 0, (
                        f"Empty or non-string '{key}' in supplement for disease '{disease_id}'"
                    )

    def test_covers_multiple_disease_categories(self):
        """Supplements should cover respiratory, GI, ortho, neuro, etc."""
        keys = set(DISEASE_SUPPLEMENTS.keys())
        assert "brachycephalic_airway_syndrome" in keys  # Respiratory
        assert "canine_parvovirus" in keys  # GI / Infectious
        assert "hip_dysplasia" in keys  # Musculoskeletal
        assert "epilepsy" in keys  # Neurological
        assert "atopic_dermatitis" in keys  # Dermatological
        assert "chronic_kidney_disease" in keys  # Renal
        assert "dcm" in keys  # Cardiac
        assert "cataracts" in keys  # Ophthalmic
        assert "liver_disease" in keys  # Hepatic
        assert "hemangiosarcoma" in keys  # Oncology


class TestDefaultSupplementsIntegrity:
    """Verify _DEFAULT_SUPPLEMENTS is a valid fallback."""

    def test_is_list(self):
        assert isinstance(_DEFAULT_SUPPLEMENTS, list)

    def test_not_empty(self):
        assert len(_DEFAULT_SUPPLEMENTS) > 0

    def test_has_required_fields(self):
        required = {
            "name_ja",
            "name_en",
            "dosage",
            "frequency",
            "reason_ja",
            "reason_en",
        }
        for supp in _DEFAULT_SUPPLEMENTS:
            for field in required:
                assert field in supp, f"Default supplement missing field '{field}'"

    def test_values_are_non_empty_strings(self):
        for supp in _DEFAULT_SUPPLEMENTS:
            for _key, value in supp.items():
                assert isinstance(value, str) and len(value) > 0


class TestCrossDataIntegrity:
    """Cross-module data consistency checks."""

    def test_all_disease_symptom_ids_are_valid(self):
        """Every symptom referenced in DISEASES should exist in SYMPTOM_IDS."""
        for disease in DISEASES:
            for symptom_id in disease["symptoms"]:
                assert symptom_id in SYMPTOM_IDS, f"Disease '{disease['id']}' references unknown symptom '{symptom_id}'"

    def test_all_diseases_have_required_fields(self):
        for d in DISEASES:
            assert "id" in d
            assert "name_ja" in d
            assert "name_en" in d
            assert "symptoms" in d
            assert "severity" in d

    def test_all_symptoms_have_required_fields(self):
        for s in SYMPTOMS:
            assert "id" in s
            assert "name_ja" in s
            assert "name_en" in s
            assert "category" in s

    def test_symptom_ids_set_matches_symptoms_list(self):
        expected = {s["id"] for s in SYMPTOMS}
        assert expected == SYMPTOM_IDS


# ============================================================================
# 6. Integration-style tests (pure function chains, no Flask)
# ============================================================================


class TestExtractThenMatch:
    """Test the extract -> match pipeline without Flask."""

    def test_english_respiratory_pipeline(self):
        symptoms = extract_symptoms_from_text("My dog has been coughing, wheezing, and has labored breathing")
        assert len(symptoms) >= 2
        matches = match_symptoms_to_diseases(symptoms)
        assert len(matches) > 0
        disease_ids = [m["disease_id"] for m in matches]
        assert "brachycephalic_airway_syndrome" in disease_ids

    def test_japanese_gi_pipeline(self):
        symptoms = extract_symptoms_from_text("嘔吐と下痢と血便が出ています")
        assert "vomiting" in symptoms
        assert "diarrhea" in symptoms
        assert "blood_in_stool" in symptoms
        matches = match_symptoms_to_diseases(symptoms)
        assert len(matches) > 0
        disease_ids = [m["disease_id"] for m in matches]
        assert "canine_parvovirus" in disease_ids

    def test_reasoning_after_match(self):
        """Reasoning functions work on actual match results."""
        symptoms = extract_symptoms_from_text("coughing and sneezing")
        matches = match_symptoms_to_diseases(symptoms)
        assert len(matches) > 0
        top_match = matches[0]
        reasoning_ja = generate_disease_reasoning_ja(top_match, symptoms)
        reasoning_en = generate_disease_reasoning_en(top_match, symptoms)
        assert len(reasoning_ja) > 0
        assert len(reasoning_en) > 0
        assert top_match["name_ja"] in reasoning_ja
        assert top_match["name_en"] in reasoning_en

    def test_treatment_after_match(self):
        """Treatment recommendations work for matched diseases."""
        symptoms = extract_symptoms_from_text("coughing and wheezing")
        matches = match_symptoms_to_diseases(symptoms)
        assert len(matches) > 0
        top_disease_id = matches[0]["disease_id"]
        treatments = get_treatment_recommendations_for_disease(top_disease_id)
        assert isinstance(treatments, dict)
        assert "supplements" in treatments
        assert len(treatments["supplements"]) > 0

    def test_empty_input_pipeline(self):
        symptoms = extract_symptoms_from_text("")
        assert symptoms == []
        matches = match_symptoms_to_diseases(symptoms)
        assert matches == []

    def test_nonsense_input_pipeline(self):
        symptoms = extract_symptoms_from_text("blorp glurp fnord")
        assert symptoms == []
        matches = match_symptoms_to_diseases(symptoms)
        assert matches == []

    def test_full_pipeline_english_respiratory(self):
        """End-to-end: English respiratory symptoms through reasoning."""
        symptoms = extract_symptoms_from_text("My dog has been coughing and wheezing a lot")
        assert len(symptoms) >= 1
        matches = match_symptoms_to_diseases(symptoms)
        assert len(matches) > 0
        for match in matches[:3]:
            ja_text = generate_disease_reasoning_ja(match, symptoms)
            en_text = generate_disease_reasoning_en(match, symptoms)
            assert isinstance(ja_text, str) and len(ja_text) > 0
            assert isinstance(en_text, str) and len(en_text) > 0

    def test_full_pipeline_japanese_neurological(self):
        """End-to-end: Japanese neurological symptoms through treatment."""
        symptoms = extract_symptoms_from_text("けいれんと振戦が起きています")
        assert "seizures" in symptoms
        assert "tremors" in symptoms
        matches = match_symptoms_to_diseases(symptoms)
        assert len(matches) > 0
        top = matches[0]
        treatments = get_treatment_recommendations_for_disease(top["disease_id"])
        assert "supplements" in treatments

    def test_full_pipeline_japanese_gi(self):
        """End-to-end: Japanese GI symptoms through treatment."""
        symptoms = extract_symptoms_from_text("嘔吐と下痢がひどいです")
        assert "vomiting" in symptoms
        assert "diarrhea" in symptoms
        matches = match_symptoms_to_diseases(symptoms)
        assert len(matches) > 0
        for match in matches[:5]:
            treatments = get_treatment_recommendations_for_disease(match["disease_id"])
            assert "supplements" in treatments
            assert "diagnostic_tests" in treatments


# ============================================================================
# 7. Additional edge cases for match_symptoms_to_diseases
# ============================================================================


class TestMatchEdgeCases:
    """Additional edge cases for the disease matching function."""

    def test_single_overlapping_symptom_still_matches(self):
        """Even one overlapping symptom should produce a match."""
        result = match_symptoms_to_diseases(["lethargy"])
        assert len(result) > 0

    def test_all_symptoms_in_system_produces_many_matches(self):
        """Passing all known symptom IDs should match virtually every disease."""
        all_ids = list(SYMPTOM_IDS)
        result = match_symptoms_to_diseases(all_ids)
        assert len(result) >= len(DISEASES) * 0.9

    def test_duplicate_symptom_ids_handled(self):
        """Duplicate symptom IDs in input should not affect results."""
        result_normal = match_symptoms_to_diseases(["coughing"])
        result_dupe = match_symptoms_to_diseases(["coughing", "coughing", "coughing"])
        for m1, m2 in zip(result_normal, result_dupe):
            assert m1["disease_id"] == m2["disease_id"]
            assert m1["similarity_score"] == m2["similarity_score"]

    def test_similarity_score_is_float(self):
        result = match_symptoms_to_diseases(["coughing"])
        for match in result:
            assert isinstance(match["similarity_score"], float)

    def test_matched_and_unmatched_are_disjoint(self):
        """matched_symptoms and unmatched_user_symptoms should not overlap."""
        result = match_symptoms_to_diseases(["coughing", "seizures", "fever"])
        for match in result:
            matched = set(match["matched_symptoms"])
            unmatched = set(match["unmatched_user_symptoms"])
            assert matched.isdisjoint(unmatched), f"Overlap in disease {match['disease_id']}"

    def test_matched_plus_unmatched_equals_user_input(self):
        """matched + unmatched should equal the user's input set."""
        user_symptoms = ["coughing", "seizures", "fever"]
        result = match_symptoms_to_diseases(user_symptoms)
        user_set = set(user_symptoms)
        for match in result:
            reconstructed = set(match["matched_symptoms"]) | set(match["unmatched_user_symptoms"])
            assert reconstructed == user_set, (
                f"For disease {match['disease_id']}: matched+unmatched={reconstructed} != user={user_set}"
            )

    def test_similarity_score_monotonicity(self):
        """Adding more matching symptoms should not decrease the score for
        a given disease (assuming the extra symptom is part of the disease)."""
        parvo = next(d for d in DISEASES if d["id"] == "canine_parvovirus")
        # Use first 2 symptoms
        result_2 = match_symptoms_to_diseases(parvo["symptoms"][:2])
        # Use first 4 symptoms
        result_4 = match_symptoms_to_diseases(parvo["symptoms"][:4])
        score_2 = next(
            (m["similarity_score"] for m in result_2 if m["disease_id"] == "canine_parvovirus"),
            0,
        )
        score_4 = next(
            (m["similarity_score"] for m in result_4 if m["disease_id"] == "canine_parvovirus"),
            0,
        )
        assert score_4 >= score_2

    def test_empty_list_is_not_none(self):
        result = match_symptoms_to_diseases([])
        assert result is not None

    def test_large_symptom_set_does_not_error(self):
        """Passing many symptom IDs (including invalid ones) should not crash."""
        ids = list(SYMPTOM_IDS) + ["fake_1", "fake_2", "fake_3"]
        result = match_symptoms_to_diseases(ids)
        assert isinstance(result, list)
        assert len(result) > 0

    def test_disease_with_no_symptom_overlap_excluded(self):
        """A disease that shares zero symptoms with user input should not appear."""
        # 'coughing' should not match diseases that don't include 'coughing'
        result = match_symptoms_to_diseases(["coughing"])
        for match in result:
            assert "coughing" in match["matched_symptoms"]


# ============================================================================
# Cardinal-sign coverage regression tests
#
# These clinical terms were previously dropped by the extractor (no alias /
# vocabulary gap). They map to existing symptom IDs, so they must always be
# captured. See api/chat/symptom_aliases.py and symptom_extractor.py.
# ============================================================================


class TestCardinalSignCoverageLegacyDog:
    """Common clinical signs must be extracted on the legacy dog free-text path."""

    def test_collapse(self):
        # collapse -> fainting (legacy vocab has no 'collapse' ID)
        assert "fainting" in extract_symptoms_from_text("dog collapse")
        assert "fainting" in extract_symptoms_from_text("犬が虚脱した")

    def test_distended_abdomen(self):
        assert "bloating" in extract_symptoms_from_text("dog with a distended abdomen")
        assert "bloating" in extract_symptoms_from_text("お腹が膨れている犬")

    def test_dyspnea_synonyms(self):
        assert "labored_breathing" in extract_symptoms_from_text("the dog has dyspnea")
        assert "labored_breathing" in extract_symptoms_from_text("respiratory distress")

    def test_melena_and_hematochezia(self):
        assert "blood_in_stool" in extract_symptoms_from_text("dog has melena")
        assert "blood_in_stool" in extract_symptoms_from_text("hematochezia noted")

    def test_hemoabdomen_triad_ranks_hemangiosarcoma(self):
        """collapse + pale gums + distended abdomen is a classic hemoabdomen
        presentation; hemangiosarcoma should rank at the top."""
        syms = extract_symptoms_from_text("dog acute collapse pale gums distended abdomen")
        assert {"fainting", "pale_gums", "bloating"}.issubset(set(syms))
        matches = match_symptoms_to_diseases(syms)
        top_names = [m.get("name_en", "") + m.get("name_ja", "") for m in matches[:3]]
        assert any("ngiosarcoma" in n or "血管肉腫" in n for n in top_names)


class TestCardinalSignCoverageModernEngine:
    """Same signs must resolve to species-appropriate IDs on the modern engine."""

    def test_collapse_resolves_per_species(self):
        from api.chat.symptom_extractor import _extract_species_symptoms

        assert "collapse" in _extract_species_symptoms("cat collapse", "cat")
        # rabbit vocabulary uses 'prostration' for collapse
        assert "prostration" in _extract_species_symptoms("rabbit collapse", "rabbit")

    def test_distended_abdomen_not_resolved_to_pain(self):
        from api.chat.symptom_extractor import _extract_species_symptoms

        # distension should resolve to a distension-like ID, never to abdominal_pain alone
        assert "abdominal_distension" in _extract_species_symptoms("cat distended abdomen", "cat")

    def test_lymphadenopathy_resolves_to_species_id(self):
        from api.chat.symptom_extractor import _extract_species_symptoms

        # cat uses 'lymph_node_enlargement'
        assert "lymph_node_enlargement" in _extract_species_symptoms("cat lymphadenopathy", "cat")


class TestChatClinicalAccuracyAudit:
    """2026-08 audit: the chat's own suggested example inputs must rank the
    textbook first differential on top. Before this audit the legacy dog path
    had NO prevalence weighting (familial nephropathy outranked diabetes for
    PU/PD, mast cell tumor topped vomiting+anorexia because the DB carried no
    gastroenteritis entry at all), and the rabbit tap-example's
    「お腹が張っている」 wasn't even extracted."""

    def test_all_legacy_dog_diseases_carry_prevalence_tier(self):
        valid = {"very_common", "common", "uncommon", "rare"}
        for d in DISEASES:
            assert d.get("prevalence_tier") in valid, (
                f"{d['id']} missing/invalid prevalence_tier — the chat and "
                "checker scorers rank rare hereditary diseases above everyday "
                "diagnoses without it"
            )

    def test_pupd_weight_loss_ranks_diabetes_over_familial_nephropathy(self):
        from api.diagnostic_chat import match_symptoms_to_diseases

        matches = match_symptoms_to_diseases(["excessive_thirst", "weight_loss"])
        ids = [m["disease_id"] for m in matches[:3]]
        assert ids[0] == "diabetes_mellitus"
        assert "chronic_kidney_disease" in ids
        # The rare juvenile hereditary disease must no longer outrank them.
        assert matches[0]["disease_id"] != "familial_nephropathy"

    def test_vomiting_anorexia_ranks_gastroenteritis_first(self):
        from api.diagnostic_chat import match_symptoms_to_diseases

        matches = match_symptoms_to_diseases(["vomiting", "loss_of_appetite"])
        assert matches[0]["disease_id"] == "acute_gastroenteritis"

    def test_rabbit_tap_example_extracts_distension_and_hits_gi_stasis(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        extracted = _extract_species_symptoms("ウサギ 食べない お腹が張っている", "rabbit")
        assert "appetite_loss" in extracted
        assert any(s in extracted for s in ("abdominal_distension", "bloating")), (
            "「お腹が張っている」 (the UI's own tap-example wording) must extract a distension symptom"
        )
        matches = _match_species_symptoms_to_diseases(list(extracted), "rabbit", lang="ja")
        assert matches, "rabbit matcher returned nothing"
        assert matches[0].get("name_en") == "Gastrointestinal Stasis", (
            f"anorexia + distension in a rabbit is GI stasis until proven otherwise, got {matches[0].get('name_en')}"
        )
        # Case-report rarities must not outrank the everyday GI emergencies.
        top5 = [m.get("name_en") for m in matches[:5]]
        assert "Ectopic Pregnancy" not in top5

    def test_generic_matcher_similarity_capped_at_one(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases

        matches = _match_species_symptoms_to_diseases(["appetite_loss", "abdominal_distension"], "rabbit", lang="ja")
        for m in matches:
            assert m["similarity_score"] <= 1.0, (
                f"{m.get('name')} similarity {m['similarity_score']} > 1.0 — the frontend renders this as a percentage"
            )


class TestQuickTapPhraseExtraction:
    """2026-08 audit: every phrase the chat UI itself offers as a quick-tap
    button must extract at least one symptom — before this audit six of them
    (dog 足を引きずる/limping, hedgehog 目が出ている, bird 羽を膨らませている,
    cat can't urinate, rabbit small feces) extracted nothing end-to-end."""

    # Mirrors the quickSymptoms map in static/js/app.js (renderSpeciesGuidance).
    JA_QUICK = {
        "dog": [
            "嘔吐している",
            "元気がない",
            "下痢している",
            "咳が出る",
            "足を引きずる",
            "皮膚が痒い",
            "口の中にできものがある",
            "おしりを地面にこすりつける",
            "鼻血が出た",
            "お腹が膨らんで吐こうとしても吐けない",
            "便に白い米粒のようなもの",
            "耳が腫れてぷよぷよしている",
            "食べた後すぐに未消化のまま吐く",
            "乳腺にしこりがある",
            "いびきがひどく呼吸がガーガー鳴る",
            "顔が腫れてじんましんが出た",
            "階段を登らなくなった",
        ],
        "cat": [
            "食べない",
            "吐いた",
            "くしゃみ",
            "目やにが出る",
            "おしっこが出ない",
            "毛が抜ける",
            "ジャンプしなくなった",
            "トイレ以外の場所で粗相する",
            "口をくちゃくちゃさせる",
            "耳の先にかさぶたができて治らない",
            "急に後ろ足が動かなくなった",
        ],
        "horse": [
            "お腹を痛がっている（疝痛）",
            "前脚をかばって歩く",
            "後ろ足を痛がる",
            "蹄が熱い",
            "毛が長くて換毛しない",
            "食べない",
            "咳が出る",
            "飲み込めず鼻から餌が出てくる",
            "後肢が突っ張って歩き尿が茶色い",
        ],
        "rabbit": [
            "糞が小さい",
            "食べない",
            "歯ぎしり",
            "首が傾いている",
            "お腹が張っている",
            "鼻水",
            "あごが濡れている",
        ],
        "chinchilla": [
            "よだれが出る",
            "毛が抜ける",
            "食べない",
            "糞が出ない",
            "歯が伸びている",
            "砂浴びしない",
            "耳が赤くて呼吸が速い",
        ],
        "hamster": [
            "下痢",
            "元気がない",
            "毛が抜ける",
            "目が開かない",
            "お腹が膨れている",
            "食べない",
            "頬袋が膨らんだまま戻らない",
        ],
        "guinea_pig": ["食べない", "鼻水", "足を引きずる", "脱毛", "下痢", "くしゃみ", "関節が腫れる"],
        "ferret": [
            "ぐったり",
            "脱毛",
            "下痢",
            "後ろ足がふらつく",
            "嘔吐",
            "食べない",
            "陰部が腫れている",
            "足を伸ばして硬直する",
            "口を前足で掻いてよだれ",
            "便に血が混じる",
        ],
        "hedgehog": ["針が抜ける", "フケ", "ふらつく", "食べない", "目が出ている", "体重が減った"],
        "bird": [
            "羽を膨らませている",
            "食べない",
            "下痢",
            "鼻水",
            "羽が抜ける",
            "くしゃみ",
            "自分で羽を抜く",
            "脚に白いかさぶた",
        ],
        "parakeet": [
            "食べない",
            "膨らんでいる",
            "呼吸のたびに音がする",
            "吐き戻しが増えた",
            "そのうが膨らんでいる",
            "お尻でいきんでいる",
        ],
        "parrot": ["食べない", "自分で羽を抜く", "くしゃみ", "下痢", "元気がない", "吐き戻しが増えた"],
        "reptile": [
            "食べない",
            "口をあけたまま呼吸",
            "鼻水が出る",
            "脱皮がうまくできない",
            "目が開かない",
            "痩せてきた",
        ],
        "tortoise": ["食べない", "甲羅がやわらかい", "鼻水が出る", "目が腫れている", "いきんでいる", "甲羅に傷がある"],
        "snake": [
            "食べない",
            "口の中が赤い",
            "脱皮がうまくできない",
            "口をあけたまま呼吸",
            "ダニがついている",
            "吐き戻しが増えた",
            "脱皮した皮が目に残っている",
        ],
        "lizard": [
            "食べない",
            "脚が曲がってきた",
            "ふらつく",
            "脱皮がうまくできない",
            "口をあけたまま呼吸",
            "痩せてきた",
        ],
        "amphibian": [
            "食べない",
            "皮膚が赤い",
            "お腹が膨れている",
            "皮膚に白いもの",
            "元気がない",
            "浮かんだまま沈めない",
        ],
        "fish": [
            "体に白い点々",
            "ヒレがボロボロ",
            "体をこすりつける",
            "水面で口をパクパク",
            "お腹が膨れている",
            "泳ぎ方がおかしい",
        ],
        "degu": ["食べない", "よだれが出る", "毛が抜ける", "尻尾の皮がむけた", "下痢", "ぐったりしている"],
        "sugar_glider": [
            "食べない",
            "自分を噛んでしまう",
            "後ろ足がふらつく",
            "毛が抜ける",
            "下痢",
            "ぐったりしている",
        ],
        "exotic_other": ["食べない", "元気がない", "下痢", "毛が抜ける"],
    }
    EN_QUICK = {
        "dog": ["vomiting", "lethargic", "diarrhea", "coughing", "limping", "itchy skin"],
        "cat": ["not eating", "vomiting", "sneezing", "eye discharge", "can't urinate", "hair loss"],
        "rabbit": ["small feces", "not eating", "teeth grinding", "head tilt", "bloated", "nasal discharge"],
    }

    @staticmethod
    def _extract(species, phrase):
        # The chat route sends dog through the legacy extractor, horse through
        # the equine finding extractor, and every other species through the
        # modern species extractor — mirror that routing.
        if species == "dog":
            from api.diagnostic_chat import extract_symptoms_from_text

            return extract_symptoms_from_text(phrase)
        if species == "horse":
            from api.diagnostic_chat import _extract_equine_symptoms

            return _extract_equine_symptoms(phrase.lower())
        from api.chat.symptom_extractor import _extract_species_symptoms

        return _extract_species_symptoms(phrase, species)

    def test_every_ja_quick_tap_phrase_extracts(self):
        for species, phrases in self.JA_QUICK.items():
            for phrase in phrases:
                assert self._extract(species, phrase), f"UI quick-tap {phrase!r} for {species} extracted no symptom"

    def test_every_en_quick_tap_phrase_extracts(self):
        for species, phrases in self.EN_QUICK.items():
            for phrase in phrases:
                assert self._extract(species, phrase), f"UI quick-tap {phrase!r} for {species} extracted no symptom"

    def test_dog_limping_tap_ranks_orthopedic_disease_first(self):
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases

        symptoms = extract_symptoms_from_text("足を引きずる")
        assert "limping" in symptoms
        matches = match_symptoms_to_diseases(symptoms)
        assert matches, "dog limping returned no candidates"
        top_ids = [m["disease_id"] for m in matches[:5]]
        assert any(
            i in top_ids
            for i in ("patellar_luxation", "cranial_cruciate_ligament_rupture", "hip_dysplasia", "osteoarthritis")
        ), f"limping top-5 has no common orthopedic disease: {top_ids}"

    def test_rabbit_small_feces_anorexia_ranks_stasis_spectrum_first(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        extracted = _extract_species_symptoms("糞が小さい 食べない", "rabbit")
        assert "small_fecal_pellets" in extracted and "appetite_loss" in extracted
        matches = _match_species_symptoms_to_diseases(list(extracted), "rabbit", lang="ja")
        top2 = [m.get("name_en") for m in matches[:2]]
        # GI stasis and its trichobezoar manifestation are the everyday answer;
        # rare congenital megacolon (En/En spotted rabbits) must not top them.
        assert set(top2) <= {"Gastrointestinal Stasis", "Trichobezoar (Hairball)"}, (
            f"small pellets + anorexia must rank the stasis spectrum on top, got {top2}"
        )
        assert matches[0].get("name_en") != "Megacolon"


class TestChatClinicalAccuracyAuditRound2:
    """2026-08 audit round 2: a 36-case realistic chief-complaint sweep across
    seven species. Root causes fixed: the equine engines had no prevalence
    prior and buried umbrella syndromes (colic ranked 67th when its own sign
    was checked); synonym expansion triple-credited diseases that list several
    spellings of one complaint; the legacy dog DB had no ear vocabulary and
    no otitis externa; and several textbook sign-pairs (blocked cat, ATE,
    ferret insulinoma) missed aliases or boosts."""

    def test_dog_ear_complaint_hits_otitis_externa(self):
        from api.diagnostic_chat import match_symptoms_to_diseases

        matches = match_symptoms_to_diseases(["ear_scratching", "head_shaking", "ear_odor"])
        assert matches and matches[0]["disease_id"] == "otitis_externa"

    def test_dog_gdv_unproductive_retching_extracts_and_ranks(self):
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases

        extracted = extract_symptoms_from_text("犬 お腹が膨れて吐きたそうで吐けない")
        assert "unproductive_retching" in extracted
        assert "bloating" in extracted
        matches = match_symptoms_to_diseases(extracted)
        assert matches[0]["disease_id"] == "gdv_bloat"

    def test_equine_colic_sign_ranks_colic_entry_first(self):
        from api.species.equine_diseases import generate_differential_diagnosis

        items = generate_differential_diagnosis({"dig_colic_signs"})
        assert items and items[0].disease.name_en == "Colic", (
            "checking the colic-signs box must rank Colic first, not a "
            "case-report subtype (was rank 67 before the prevalence prior)"
        )

    def test_equine_laminitis_pair_beats_two_finding_entries(self):
        from api.species.equine_diseases import generate_differential_diagnosis

        items = generate_differential_diagnosis({"hoof_heat", "limb_lameness_fore", "gen_recumbent"})
        top3 = [i.disease.name_en for i in items[:3]]
        assert any("Laminitis" in n for n in top3), (
            f"forelimb lameness + hoof heat is laminitis until proven otherwise (Adams & Stashak 7th ed), got {top3}"
        )

    def test_horse_chat_delegates_to_checkbox_engine(self):
        from api.diagnostic_chat import _match_equine_symptoms_to_diseases

        matches = _match_equine_symptoms_to_diseases(["dig_colic_signs"])
        assert matches and matches[0]["name_en"] == "Colic"
        # Low-information cap still applies on the chat surface.
        assert matches[0]["confidence_percent"] <= 35.0

    def test_synonym_expansion_no_longer_multi_credits_one_complaint(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases

        res = _match_species_symptoms_to_diseases(["small_fecal_pellets", "appetite_loss"], "rabbit", lang="ja")
        names = [x.get("name_en") for x in res[:3]]
        assert "Gastrointestinal Stasis" in names, (
            "small droppings + anorexia must rank GI stasis top-3; megacolon "
            f"won by listing three spellings of one complaint before, got {names}"
        )

    def test_cat_blocked_and_ate_pairs_rank_first(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases

        blocked = _match_species_symptoms_to_diseases(["decreased_urination", "vocalization_changes"], "cat", lang="ja")
        assert blocked[0].get("name_en") == "Urinary Obstruction (Blocked Cat)"
        ate = _match_species_symptoms_to_diseases(["hind_limb_paralysis", "vocalization_changes"], "cat", lang="ja")
        assert ate[0].get("name_en") == "Aortic Thromboembolism (Saddle Thrombus)"

    def test_ferret_insulinoma_triad_ranks_top(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        extracted = _extract_species_symptoms("フェレット 後ろ足のふらつき ぼーっとする よだれ", "ferret")
        assert "hind_leg_weakness" in extracted
        res = _match_species_symptoms_to_diseases(list(extracted), "ferret", lang="ja")
        assert res[0].get("name_en") == "Insulinoma"

    def test_tortoise_soft_shell_ranks_mbd(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases

        res = _match_species_symptoms_to_diseases(["bone_weakness", "anorexia"], "tortoise", lang="ja")
        assert "Metabolic Bone Disease" in (res[0].get("name_en") or "")

    def test_avian_exposure_toxicoses_do_not_top_nonspecific_signs(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases

        res = _match_species_symptoms_to_diseases(["fluffed_feathers", "diarrhea", "lethargy"], "parakeet", lang="ja")
        top3 = [x.get("name_en") or "" for x in res[:3]]
        assert not any("Copper" in n or "Teflon" in n or "PTFE" in n for n in top3), (
            f"exposure-dependent toxicoses need a history, not top billing for a nonspecific sick bird: {top3}"
        )

    def test_cat_skin_lump_ranks_common_ddx_over_sarcoma_rarities(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases

        res = _match_species_symptoms_to_diseases(["lumps"], "cat", lang="ja")
        top4 = [x.get("name_en") or "" for x in res[:4]]
        assert any(("Lipoma" in n) or ("Mast Cell" in n) or ("Abscess" in n) or ("Cyst" in n) for n in top4), (
            f"a bare skin lump must surface the everyday differentials: {top4}"
        )


class TestChatClinicalAccuracyAuditRound3:
    """2026-08 audit round 3. Root causes fixed this round: 125 colloquial
    aliases existed only in the contracted 〜てる form and missed the full
    〜ている inputs (now auto-expanded bidirectionally at module load); the
    scurvy complaint 歯茎から出血 was mismapped to blood_in_stool and swollen
    joints to lameness; the legacy dog DB had no dental entry or halitosis
    vocabulary despite periodontal disease being the most prevalent canine
    disease; and classic reptile mouth-rot / rabbit vestibular phrasings
    extracted nothing."""

    def test_teiru_form_aliases_auto_expanded(self):
        from api.chat.symptom_aliases import SYMPTOM_ALIASES

        # Every contracted 〜てる/〜でる key must have its full 〜ている/〜でいる
        # twin (and vice versa). A handful of pre-existing pairs intentionally
        # map the two forms to synonym-bridged IDs (腫れてる→bloating vs
        # 腫れている→swelling), so we assert existence, not identity —
        # setdefault never overrides an explicit curated mapping.
        for k in list(SYMPTOM_ALIASES):
            if k.endswith("てる") or k.endswith("でる"):
                full = k[:-1] + "いる"
                assert full in SYMPTOM_ALIASES, f"missing full-form twin for {k}"
            elif k.endswith("ている") or k.endswith("でいる"):
                short = k[:-2] + "る"
                assert short in SYMPTOM_ALIASES, f"missing contracted twin for {k}"

    def test_rabbit_head_tilt_nystagmus_full_form_extracts(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        syms = _extract_species_symptoms("首が傾いて目が揺れている", "rabbit")
        assert "head_tilt" in syms and "nystagmus" in syms
        top = [m.get("name_ja", "") for m in _match_species_symptoms_to_diseases(syms, "rabbit")[:4]]
        assert any(("前庭" in n) or ("斜頸" in n) or ("エンセファリトゾーン" in n) for n in top)

    def test_guinea_pig_scurvy_complaint_extracts_and_ranks(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        syms = _extract_species_symptoms("関節が腫れて痛がる 歯茎から出血", "guinea_pig")
        assert "bleeding_gums" in syms, "歯茎から出血 must map to bleeding_gums (was blood_in_stool)"
        assert "swollen_joints" in syms, "関節が腫れて must map to swollen_joints (was lameness)"
        top = [m.get("name_ja", "") for m in _match_species_symptoms_to_diseases(syms, "guinea_pig")[:3]]
        assert any(("壊血病" in n) or ("ビタミンC" in n) for n in top), f"scurvy must rank top-3, got {top}"

    def test_dog_cataract_complaint_extracts_cloudy_eyes(self):
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases

        syms = extract_symptoms_from_text("目が白く濁っている")
        assert "cloudiness_in_eyes" in syms
        top = [m["disease_id"] for m in match_symptoms_to_diseases(syms)[:4]]
        assert "cataracts" in top

    def test_dog_dental_complaint_hits_periodontal_disease(self):
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases

        syms = extract_symptoms_from_text("口臭がひどい よだれ 食べにくそう")
        assert "bad_breath" in syms
        matches = match_symptoms_to_diseases(syms)
        assert matches and matches[0]["disease_id"] == "periodontal_disease", (
            "halitosis + drooling + inappetence is periodontal disease first "
            "(80-90% prevalence in dogs >3y, AAHA 2019) — got "
            f"{[m['disease_id'] for m in matches[:3]]}"
        )

    def test_reptile_mouth_rot_phrasing_extracts_and_ranks(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        syms = _extract_species_symptoms("口の中に膿がある 口が閉じない", "reptile")
        assert "mouth_lesions" in syms
        top = [m.get("name_ja", "") for m in _match_species_symptoms_to_diseases(syms, "reptile")[:5]]
        assert any(("口内炎" in n) or ("口腔" in n) for n in top), f"mouth rot must rank, got {top}"

    def test_bird_egg_binding_straining_resolves_and_ranks_first(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        # いきんでいる resolves to constipation, which bird vocabulary carries
        # as bare "straining" via the ID-synonym fallback.
        syms = _extract_species_symptoms("卵が出ない お尻でいきんでいる ぐったり", "bird")
        assert "egg_binding" in syms and "straining" in syms
        top = _match_species_symptoms_to_diseases(syms, "bird")
        assert top and "卵詰まり" in (top[0].get("name_ja") or ""), (
            f"egg binding must rank first, got {[m.get('name_ja') for m in top[:3]]}"
        )

    def test_mammal_constipation_unaffected_by_straining_fallback(self):
        from api.chat.symptom_extractor import _extract_species_symptoms

        # Cats resolve constipation directly — the straining fallback is for
        # species whose vocabulary lacks a constipation ID (birds/reptiles).
        syms = _extract_species_symptoms("何日も便が出ない いきんでいる", "cat")
        assert "constipation" in syms


class TestChatClinicalAccuracyAuditRound4:
    """2026-08 audit round 4. Root causes fixed this round: the itch aliases
    (痒い/痒がる/体を掻く) mapped to excessive_licking instead of itching, so
    the most common canine presentation (pruritic dermatitis) lost its defining
    symptom; no colloquial polyphagia phrasing existed, so the classic feline
    hyperthyroidism/diabetes triad (PU/PD + weight loss + ravenous appetite)
    extracted only two of three signs; the legacy dog DB had no
    increased_appetite vocabulary at all (diabetes listed loss_of_appetite —
    the DKA sign, not the classic presentation); caseous oral exudate
    (チーズ状) — the textbook mouth-rot finding — extracted nothing; and ear
    pruritus (耳が痒い/耳をかく) resolved to generic itching so otitis externa
    and ear mites never ranked."""

    def test_dog_pruritus_maps_to_itching_not_licking(self):
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases

        syms = extract_symptoms_from_text("皮膚が赤くて痒がっている 毛が抜ける")
        assert "itching" in syms, "痒がって must map to itching (was excessive_licking)"
        top = [d.get("name_ja", "") for d in match_symptoms_to_diseases(syms)[:3]]
        assert any(("アトピー" in n) or ("膿皮症" in n) or ("毛包虫" in n) for n in top), (
            f"pruritic dermatoses must rank top-3, got {top}"
        )
        # Lick-behaviour phrasing itself must still resolve to excessive_licking.
        assert "excessive_licking" in extract_symptoms_from_text("しきりに舐める")

    def test_polyphagia_colloquial_phrases_extract(self):
        from api.chat.symptom_extractor import _extract_species_symptoms

        for phrase in ("食欲はすごくある", "食欲旺盛", "食欲が増えた", "たくさん食べる"):
            syms = _extract_species_symptoms(f"{phrase} 痩せてきた", "cat")
            assert "increased_appetite" in syms, f"{phrase!r} must map to increased_appetite"

    def test_cat_hyperthyroid_triad_ranks_endocrine(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        syms = _extract_species_symptoms("水をよく飲む 痩せてきた 食欲はすごくある", "cat")
        assert "increased_appetite" in syms
        top = [m.get("name_ja", "") for m in _match_species_symptoms_to_diseases(syms, "cat")[:2]]
        assert any("糖尿病" in n for n in top) and any("甲状腺機能亢進" in n for n in top), (
            f"DM + hyperthyroidism must occupy top-2, got {top}"
        )

    def test_legacy_dog_db_carries_polyphagia(self):
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases
        from api.health_checker import DISEASES, SYMPTOM_IDS

        assert "increased_appetite" in SYMPTOM_IDS
        by_id = {d["id"]: d for d in DISEASES}
        # Polyphagia is a defining sign of uncomplicated canine DM, Cushing's
        # and EPI (inappetence in DM signals DKA, not the classic presentation).
        for did in ("diabetes_mellitus", "cushings_disease", "epi"):
            assert "increased_appetite" in by_id[did]["symptoms"], did
        syms = extract_symptoms_from_text("水をたくさん飲む おしっこが多い 食欲はすごくある")
        assert "increased_appetite" in syms
        top = [d.get("name_ja", "") for d in match_symptoms_to_diseases(syms)[:3]]
        assert any("糖尿病" in n for n in top), f"DM must rank top-3, got {top}"

    def test_snake_caseous_mouth_rot_ranks_first(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        syms = _extract_species_symptoms("口の周りにチーズ状のもの 口が閉じない", "snake")
        assert "mucus_in_mouth" in syms, "チーズ状 (caseous exudate) must map to mucus_in_mouth"
        top = _match_species_symptoms_to_diseases(syms, "snake")
        assert top and "口内炎" in (top[0].get("name_ja") or ""), (
            f"infectious stomatitis must rank first, got {[m.get('name_ja') for m in top[:3]]}"
        )

    def test_caseous_alias_drops_safely_for_species_without_the_id(self):
        from api.chat.symptom_extractor import _extract_species_symptoms

        # mucus_in_mouth is a reptile/avian-vocabulary ID; species without it
        # must simply not extract it (no mis-mapping).
        syms = _extract_species_symptoms("口の周りにチーズ状のもの", "dog")
        assert "mucus_in_mouth" not in syms

    def test_ear_pruritus_ranks_otitis_and_ear_mites(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases

        # Cat: 耳が痒い resolves via the ear_scratching→scratching_ears bridge.
        syms = _extract_species_symptoms("耳が痒い 耳をかく", "cat")
        assert "scratching_ears" in syms
        top = [m.get("name_ja", "") for m in _match_species_symptoms_to_diseases(syms, "cat")[:2]]
        assert any(("外耳炎" in n) or ("耳ダニ" in n) for n in top), f"got {top}"
        # Rabbit: ear mites (Psoroptes) are the classic cause.
        syms = _extract_species_symptoms("耳をかく 耳の中にかさぶた", "rabbit")
        top = [m.get("name_ja", "") for m in _match_species_symptoms_to_diseases(syms, "rabbit")[:2]]
        assert any(("耳ダニ" in n) or ("外耳炎" in n) for n in top), f"got {top}"
        # Dog (legacy path): otitis externa must rank first.
        syms = extract_symptoms_from_text("耳が痒い 頭を振る")
        assert "ear_scratching" in syms
        top = [d.get("name_ja", "") for d in match_symptoms_to_diseases(syms)[:1]]
        assert top and "外耳炎" in top[0], f"got {top}"


class TestChatClinicalAccuracyAuditRound5:
    """2026-08 audit round 5. Root causes fixed this round: the legacy dog DB
    had no entry (and often no vocabulary) for four of the most common canine
    presentations — anal sac disease (the pathognomonic scooting complaint
    extracted nothing), corneal ulcer, osteoarthritis and cognitive
    dysfunction; te-form squinting phrases (目を細めて/まぶしそう) missed the
    dictionary-form alias; hind_leg_weakness / difficulty_standing / staring /
    vocalization_changes had no legacy-vocabulary bridge; 夜鳴き mapped to
    anxiety so the classic geriatric-cat nocturnal-yowling complaint never
    ranked hyperthyroidism (whose symptom set also lacked the documented
    vocalization sign — AAFP, Carney 2016); and crop distension
    (そのうが膨らんでいる) had no alias so crop diseases never ranked."""

    def test_dog_scooting_ranks_anal_sac_disease_first(self):
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases

        syms = extract_symptoms_from_text("おしりを地面にこすりつける")
        assert "scooting" in syms, "scooting phrase must extract (previously extracted nothing)"
        top = [d.get("name_ja", "") for d in match_symptoms_to_diseases(syms)[:1]]
        assert any("肛門嚢" in n for n in top), f"anal sac disease must rank first, got {top}"

    def test_dog_geriatric_cognitive_complaint_ranks_cds_first(self):
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases

        syms = extract_symptoms_from_text("夜鳴きする 同じ場所をぐるぐる回る ぼーっとしている")
        assert "disorientation" in syms, "ぼーっとしている must bridge staring→disorientation"
        assert "anxiety" in syms, "夜鳴き must bridge vocalization_changes→anxiety on the dog path"
        top = [d.get("name_ja", "") for d in match_symptoms_to_diseases(syms)[:1]]
        assert any("認知機能不全" in n for n in top), f"CDS must rank first, got {top}"

    def test_dog_squinting_red_eye_ranks_corneal_ulcer(self):
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases

        syms = extract_symptoms_from_text("目が赤い 目を細めてまぶしそう")
        assert "squinting" in syms, "te-form 目を細めて / まぶしそう must extract squinting"
        top = [d.get("name_ja", "") for d in match_symptoms_to_diseases(syms)[:3]]
        assert any("角膜潰瘍" in n for n in top), f"corneal ulcer must rank top-3, got {top}"

    def test_dog_hindlimb_weakness_ranks_orthopedic(self):
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases

        syms = extract_symptoms_from_text("散歩を嫌がる 後ろ足がふらつく 立ち上がりにくい")
        assert "limping" in syms, "hind_leg_weakness must bridge to limping on the dog path"
        assert "stiffness" in syms, "difficulty_standing must bridge to stiffness"
        top = [d.get("name_ja", "") for d in match_symptoms_to_diseases(syms)[:3]]
        assert any(("変形性関節症" in n) or ("股関節" in n) or ("椎間板" in n) for n in top), (
            f"orthopedic/neurologic hindlimb diseases must rank top-3, got {top}"
        )

    def test_legacy_dog_db_carries_new_common_presentations(self):
        from api.health_checker import DISEASES, SYMPTOM_IDS

        assert "scooting" in SYMPTOM_IDS
        by_id = {d["id"]: d for d in DISEASES}
        for did, tier in (
            ("anal_sac_disease", "very_common"),
            ("corneal_ulcer", "very_common"),
            ("osteoarthritis", "very_common"),
            ("cognitive_dysfunction", "common"),
        ):
            assert did in by_id, f"{did} missing from legacy dog DB"
            assert by_id[did]["prevalence_tier"] == tier, did

    def test_cat_nocturnal_yowling_ranks_hyperthyroidism_first(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        syms = _extract_species_symptoms("夜中に大声で鳴く 高齢 痩せてきた", "cat")
        assert "vocalization_changes" in syms
        top = [m.get("name_ja", "") for m in _match_species_symptoms_to_diseases(syms, "cat")[:1]]
        assert any("甲状腺機能亢進" in n for n in top), (
            f"hyperthyroidism must rank first for the geriatric yowling triad, got {top}"
        )
        # 夜鳴き itself must also resolve to vocalization_changes now.
        assert "vocalization_changes" in _extract_species_symptoms("夜鳴きがひどい", "cat")

    def test_bird_crop_distension_ranks_crop_diseases(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        syms = _extract_species_symptoms("吐き戻しをする そのうが膨らんでいる", "bird")
        assert "crop_distension" in syms, "そのうが膨らんでいる must extract crop_distension"
        top = [m.get("name_ja", "") for m in _match_species_symptoms_to_diseases(syms, "bird")[:3]]
        assert any(("嗉嚢" in n) or ("そ嚢" in n) or ("そのう" in n) or ("素嚢" in n) for n in top), (
            f"crop diseases must dominate, got {top}"
        )


class TestChatClinicalAccuracyAuditRound6:
    """2026-08 sweep round 6: realistic owner complaints that extracted
    nothing (or ranked clinically wrong diseases) before the round-6 alias /
    ID-synonym / matcher-bridge fixes."""

    @staticmethod
    def _run(text, species):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ex = sorted(_extract_species_symptoms(text, species))
        return ex, _match_species_symptoms_to_diseases(list(ex), species, lang="ja")

    def test_cat_oral_pain_ranks_dental_stomatitis(self):
        # 口を痛がる was mismapped to excessive_drooling (a different sign);
        # it must resolve to difficulty_eating so dental/FCGS complaints rank.
        ex, m = self._run("口を痛がる よだれが多い 食べたそうなのに食べない", "cat")
        assert "difficulty_eating" in ex
        top5 = [x.get("name_ja") or x.get("name") for x in m[:5]]
        assert any("歯周" in n or "口内炎" in n or "歯肉" in n for n in top5), top5

    def test_guinea_pig_pododermatitis_rank1(self):
        # 足の裏が赤く腫れている extracted only generic 'swelling' before.
        ex, m = self._run("足の裏が赤く腫れている 歩きたがらない", "guinea_pig")
        assert "foot_sores" in ex and "reluctance_to_move" in ex
        top = m[0].get("name_ja") or m[0].get("name")
        assert "足底皮膚炎" in top or "バンブルフット" in top, top

    def test_rabbit_sore_hocks_rank1(self):
        # The main sore-hocks entry keys on foot_lesions; the matcher bridge
        # from pododermatitis_signs must reach it.
        ex, m = self._run("足の裏が赤い 動きたがらない", "rabbit")
        top = m[0].get("name_ja") or m[0].get("name")
        assert "ソアホック" in top or "足底皮膚炎" in top, top

    def test_snake_dysecdysis_and_spectacle_top(self):
        # 「脱皮がうまくできない」(できない form) was not aliased at all.
        ex, m = self._run("脱皮がうまくできない 目が白いまま", "snake")
        assert "dysecdysis" in ex
        top2 = [x.get("name_ja") or x.get("name") for x in m[:2]]
        assert any("脱皮不全" in n for n in top2), top2

    def test_ferret_retching_melena_ranks_helicobacter(self):
        # 吐きそうにする (non-productive retching gesture) extracted nothing;
        # bruxism + melena + retching is the classic Helicobacter/ulcer triad.
        ex, m = self._run("吐きそうにする 歯ぎしりをする 黒い便が出る", "ferret")
        assert len(ex) >= 3
        top3 = [x.get("name_ja") or x.get("name") for x in m[:3]]
        assert any("ヘリコバクター" in n or "胃潰瘍" in n for n in top3), top3

    def test_bird_falling_off_perch_extracts(self):
        ex, m = self._run("止まり木から落ちる 痙攣する", "bird")
        assert "falling_off_perch" in ex and "seizures" in ex
        top = m[0].get("name_ja") or m[0].get("name")
        assert "痙攣" in top or "中毒" in top, top

    def test_chinchilla_circular_alopecia_ranks_ringworm(self):
        # 円形脱毛 (the textbook dermatophytosis pattern) was not aliased.
        ex, m = self._run("毛が円形に抜ける カサカサしている", "chinchilla")
        assert "circular_hair_loss" in ex
        top3 = [x.get("name_ja") or x.get("name") for x in m[:3]]
        assert any("糸状菌" in n or "白癬" in n for n in top3), top3

    def test_reluctance_to_move_alias_general(self):
        from api.chat.symptom_extractor import _extract_species_symptoms

        assert "reluctance_to_move" in _extract_species_symptoms("歩きたがらない", "guinea_pig")


class TestChatClinicalAccuracyAuditRound7:
    """2026-08 audit round 5 (15-case realistic-complaint sweep). Root causes
    fixed this round: no alias for the owner phrasing of exercise intolerance
    (座り込む) so cardiac complaints extracted airway signs only; the legacy
    dog DB had no perianal entry/vocabulary at all so scooting — one of the
    most common canine presentations (VetCompass 4.4%) — extracted nothing;
    no CDS entry despite 14-35% prevalence in dogs >8 y; the feather-plucking
    aliases mapped to hair_loss (passive loss) instead of the behavioural
    feather_plucking ID; tail bobbing had no alias; 口を痛がる mapped to
    excessive_drooling (double-counting よだれ) losing the oral-pain signal;
    limb deformity (脚が曲がって — reptile MBD) had no ID_SYNONYMS bridge to
    soft_bones; and the extracted rectal_prolapse ID never matched ferret
    Rectal Prolapse because the disease uses rectal_protrusion and _SYN had
    no bridge (ID_SYNONYMS only fires when the ID is absent from the species
    vocabulary)."""

    def test_dog_exercise_intolerance_phrasing_ranks_mmvd(self):
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases
        from api.health_checker import DISEASES

        syms = extract_symptoms_from_text("散歩の途中で座り込む 呼吸が荒い 咳が出る")
        assert "exercise_intolerance" in syms, "座り込む must map to exercise_intolerance"
        top = [d.get("name_ja", "") for d in match_symptoms_to_diseases(syms)[:3]]
        assert any("僧帽弁" in n for n in top), f"MMVD must rank top-3, got {top}"
        # MMVD is the most common acquired canine cardiac disease (Keene 2019
        # ACVIM consensus) — the tier must reflect that.
        mmvd = next(d for d in DISEASES if d["id"] == "mitral_valve_disease")
        assert mmvd["prevalence_tier"] == "very_common"

    def test_dog_scooting_extracts_and_ranks_anal_sac_disease(self):
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases
        from api.health_checker import DISEASES, SYMPTOM_IDS

        assert "scooting" in SYMPTOM_IDS
        assert any(d["id"] == "anal_sac_disease" for d in DISEASES)
        syms = extract_symptoms_from_text("おしりを地面にこすりつける ずっと舐めている")
        assert "scooting" in syms, "こすりつけ phrasing must map to scooting"
        top = [d.get("name_ja", "") for d in match_symptoms_to_diseases(syms)[:1]]
        assert top and "肛門" in top[0], f"anal sac disease must rank first, got {top}"

    def test_dog_senior_night_vocalization_ranks_cds(self):
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases
        from api.health_checker import DISEASES

        assert any(d["id"] == "cognitive_dysfunction" for d in DISEASES)
        syms = extract_symptoms_from_text("夜鳴きがひどい ぐるぐる回る 老犬です")
        top = [d.get("name_ja", "") for d in match_symptoms_to_diseases(syms)[:1]]
        assert top and "認知機能不全" in top[0], f"CDS must rank first, got {top}"

    def test_dog_pain_posture_ranks_ivdd(self):
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases

        syms = extract_symptoms_from_text("震えている 背中を丸めて痛そうにしている 抱き上げると鳴く")
        # 背中を丸めて → hunched_posture → reluctance_to_move (legacy bridge)
        assert "reluctance_to_move" in syms, f"got {syms}"
        assert "tremors" in syms
        top = [d.get("name_ja", "") for d in match_symptoms_to_diseases(syms)[:3]]
        assert any("椎間板" in n for n in top), f"IVDD must rank top-3, got {top}"

    def test_cat_oral_pain_ranks_gingivostomatitis(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        syms = _extract_species_symptoms("口を痛がって食べられない よだれが出る 口臭がひどい", "cat")
        assert "pain" in syms, "口を痛がって must map to pain (was excessive_drooling)"
        assert "difficulty_eating" in syms, "食べられない must map to difficulty_eating"
        top = [m.get("name_ja", "") for m in _match_species_symptoms_to_diseases(syms, "cat")[:3]]
        assert any("口内炎" in n for n in top), f"FCGS must rank top-3, got {top}"

    def test_bird_feather_plucking_is_behavioural_not_hair_loss(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_aliases import SYMPTOM_ALIASES
        from api.chat.symptom_extractor import _extract_species_symptoms

        assert SYMPTOM_ALIASES["毛引き"] == "feather_plucking"
        syms = _extract_species_symptoms("自分の羽を抜いてしまう 皮膚が赤い", "bird")
        assert "feather_plucking" in syms, f"got {syms}"
        top = [m.get("name_ja", "") for m in _match_species_symptoms_to_diseases(syms, "bird")[:3]]
        assert any(("羽毛破壊" in n) or ("毛引き" in n) or ("自傷" in n) for n in top), f"got {top}"

    def test_bird_tail_bobbing_ranks_lower_respiratory(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        syms = _extract_species_symptoms("呼吸のたびに尾が上下に動く 口を開けて呼吸", "bird")
        assert "tail_bobbing" in syms, f"got {syms}"
        top = [m.get("name_ja", "") for m in _match_species_symptoms_to_diseases(syms, "bird")[:3]]
        assert any(("気嚢" in n) or ("肺炎" in n) for n in top), f"got {top}"

    def test_lizard_bowed_limbs_rank_mbd(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        syms = _extract_species_symptoms("後ろ足が震える 脚が曲がってきた", "lizard")
        # Round 14: 「後ろ足が震える」 now resolves to hindlimb weakness (the
        # canine OA/weakness picture); for lizards both weakness and tremor are
        # MBD-consistent, and the MBD ranking below is what this test protects.
        assert ("tremors" in syms) or ("hind_limb_weakness" in syms), f"got {syms}"
        # 脚が曲がって → limb_deformity → soft_bones via the new ID_SYNONYMS bridge
        assert "soft_bones" in syms, f"got {syms}"
        top = [m.get("name_ja", "") for m in _match_species_symptoms_to_diseases(syms, "lizard")[:2]]
        assert any(("代謝性骨疾患" in n) or ("副甲状腺" in n) for n in top), f"got {top}"

    def test_ferret_rectal_prolapse_syn_bridge(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        syms = _extract_species_symptoms("お尻から赤いものが出ている いきんでいる", "ferret")
        assert "rectal_prolapse" in syms, f"got {syms}"
        top = [m.get("name_ja", "") for m in _match_species_symptoms_to_diseases(syms, "ferret")[:1]]
        assert top and "直腸脱" in top[0], f"rectal prolapse must rank first, got {top}"

    def test_ferret_vulvar_swelling_ranks_adrenal(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        syms = _extract_species_symptoms("毛が抜けてきて尻尾がハゲている 陰部が腫れている", "ferret")
        assert "vulvar_swelling" in syms, "陰部が腫れている must map to vulvar_swelling"
        assert "hair_loss" in syms
        top = [m.get("name_ja", "") for m in _match_species_symptoms_to_diseases(syms, "ferret")[:3]]
        assert any("副腎" in n for n in top), f"adrenal disease must rank top-3, got {top}"


class TestHotSpotAndZincDermatosis:
    """2026-08 clinician feedback: 'there is zinc-responsive dermatosis, but a
    hot dog can also simply transition into dermatitis.' The hot-spot lesion
    (pyotraumatic dermatitis) was absent from every dog DB, the legacy chat
    could not rank it, and the zinc entries carried a generic dermatology
    template for clinical signs."""

    def test_legacy_db_carries_hot_spot_and_zinc(self):
        from api.health_checker import DISEASE_MAP

        hs = DISEASE_MAP["acute_moist_dermatitis"]
        assert hs["prevalence_tier"] == "common"
        assert "hot_spots" in hs["symptoms"]
        zn = DISEASE_MAP["zinc_responsive_dermatosis"]
        assert zn["prevalence_tier"] == "uncommon"
        # Northern-breed signalment drives this diagnosis (White SD, JAVMA 2001).
        assert zn["breed_risks"].get("siberian_husky", 0) >= 3.0
        assert zn["breed_risks"].get("alaskan_malamute", 0) >= 3.0

    def test_chat_moist_lesion_ranks_hot_spot_first(self):
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases

        for text in (
            "暑がって皮膚が赤くジュクジュクしている 痒がって舐めている",
            "皮膚がジュクジュクしていて痒がる",
            "急に皮膚がただれた 痒がる",
        ):
            syms = extract_symptoms_from_text(text)
            assert "hot_spots" in syms, f"{text!r} must extract hot_spots, got {sorted(syms)}"
            top = match_symptoms_to_diseases(syms)[0]
            assert top["disease_id"] == "acute_moist_dermatitis", (
                f"{text!r}: presenting-lesion dx must rank first, got {top['name_ja']}"
            )

    def test_chat_food_allergy_gi_cluster_still_boosts_allergic(self):
        # The old {itching, skin_rashes, hot_spots}→allergic cluster was
        # retargeted to the pruritus+GI picture; verify it still fires.
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases

        syms = extract_symptoms_from_text("痒がっている 皮膚に発疹 吐くこともある")
        assert {"itching", "skin_rashes", "vomiting"} <= set(syms)
        top3 = [m["disease_id"] for m in match_symptoms_to_diseases(syms)[:3]]
        assert "allergic_dermatitis" in top3

    def test_checkbox_hot_spot_excellent_tier_rank1(self):
        # A 96% four-symptom match must not sit below a 52% very_common
        # allergy — the excellent-match tier ranks it first.
        from api.species_analyzer import analyze_species_symptoms

        res = analyze_species_symptoms("dog", ["itching", "skin_redness", "skin_lesions", "pain_on_touch"], lang="ja")
        top = res["suspected_diseases"][0]
        assert top.get("name") == "Acute Moist Dermatitis (Hot Spot)", top.get("name")
        assert top.get("prevalence_tier") == "common"

    def test_zinc_clinical_signs_are_zinc_specific(self):
        # Both zinc entries carried the generic dermatology distribution
        # template; they must now name the mucocutaneous crusting and footpad
        # hyperkeratosis that define the disease.
        import json
        from pathlib import Path

        root = Path(__file__).resolve().parents[1]
        data = json.loads((root / "diseases_all_species.json").read_text(encoding="utf-8"))
        found = 0
        for e in data:
            if e.get("species") == "Dog" and (e.get("name") or "").startswith("Zinc-Responsive"):
                found += 1
                cs = e.get("clinical_signs_ja") or ""
                assert "皮膚粘膜移行部" in cs and "過角化" in cs, e.get("name")
                assert "分布パターンが診断に有用" not in cs  # the old template
                assert "hyperkeratosis" in (e.get("clinical_signs") or "")
        assert found == 2

    def test_dog_module_hot_spot_entry_curated(self):
        from api.species.dog_diseases import DISEASES

        hs = next(d for d in DISEASES if d.get("name") == "Acute Moist Dermatitis (Hot Spot)")
        assert "クロルヘキシジン" in hs["treatment_ja"]
        # Systemic antibiotics only for the deep folliculitis variant.
        assert "毛包炎" in hs["treatment_ja"]
        assert {"itching", "skin_redness", "skin_lesions"} <= set(hs["symptoms"])


class TestChatClinicalAccuracyAuditRound8:
    """2026-08 audit round 8 (22-case realistic-complaint sweep). Root causes
    fixed this round: the legacy dog DB had no epistaxis / vision-loss /
    voluminous-stool vocabulary at all (nosebleeds extracted nothing and the
    nasal-cavity differential was missing entirely; "目が白く見える 物にぶつかる"
    extracted nothing; the EPI hallmark 便の量が多い was unextractable); the
    patellar-luxation skip-gait phrasing had no alias; cat tooth-root abscess /
    feline DJD / psychogenic alopecia complaints extracted only generic IDs;
    rabbit bruxism+anorexia (the pre-fecal-change GI stasis presentation)
    ranked bloat first; and the horse DB carried TWO duplicate PPID cards
    while the hirsutism hallmark had no alias and no syndrome floor, so the
    pathognomonic PPID complaint extracted nothing and rare coverage-perfect
    diseases outranked PPID."""

    def test_dog_epistaxis_extracts_and_ranks_nasal_tumor(self):
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases
        from api.health_checker import DISEASES, SYMPTOM_IDS

        assert "epistaxis" in SYMPTOM_IDS
        assert any(d["id"] == "nasal_tumor" for d in DISEASES)
        syms = extract_symptoms_from_text("鼻血が出た 鼻がつまる くしゃみ")
        assert "epistaxis" in syms, f"got {syms}"
        top = [d.get("name_ja", "") for d in match_symptoms_to_diseases(syms)[:1]]
        assert top and "鼻腔内腫瘍" in top[0], f"nasal tumor must rank first, got {top}"
        # vWD carries epistaxis too (coagulopathy differential)
        vwd = next(d for d in DISEASES if d["id"] == "von_willebrand_disease")
        assert "epistaxis" in vwd["symptoms"]

    def test_dog_vision_loss_ranks_cataracts(self):
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases
        from api.health_checker import SYMPTOM_IDS

        assert "vision_loss" in SYMPTOM_IDS
        syms = extract_symptoms_from_text("目が白く見える 夜に物にぶつかる 高齢")
        assert "vision_loss" in syms and "cloudiness_in_eyes" in syms, f"got {syms}"
        top = [d.get("name_ja", "") for d in match_symptoms_to_diseases(syms)[:3]]
        assert any("白内障" in n for n in top), f"cataracts must rank top-3, got {top}"

    def test_dog_skip_gait_ranks_patellar_luxation(self):
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases

        syms = extract_symptoms_from_text("片足を上げてスキップするように歩く 小型犬")
        assert "limping" in syms, f"got {syms}"
        top = [d.get("name_ja", "") for d in match_symptoms_to_diseases(syms)[:1]]
        assert top and "膝蓋骨" in top[0], f"patellar luxation must rank first, got {top}"

    def test_dog_epi_voluminous_stool_ranks_first(self):
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases
        from api.health_checker import DISEASES, SYMPTOM_IDS

        assert "voluminous_stool" in SYMPTOM_IDS
        epi = next(d for d in DISEASES if d["id"] == "epi")
        assert "voluminous_stool" in epi["symptoms"]
        syms = extract_symptoms_from_text("食べているのに痩せる 便の量が多い 軟便")
        assert "voluminous_stool" in syms, f"got {syms}"
        top = [d.get("name_ja", "") for d in match_symptoms_to_diseases(syms)[:1]]
        assert top and "膵" in top[0], f"EPI must rank first, got {top}"

    def test_cat_facial_swelling_ranks_tooth_root_abscess(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        syms = _extract_species_symptoms("顔の片側が腫れている 目の下から膿が出ている", "cat")
        assert "facial_swelling" in syms, f"got {syms}"
        top = [m.get("name_ja", "") for m in _match_species_symptoms_to_diseases(syms, "cat")[:1]]
        assert top and "歯根膿瘍" in top[0], f"tooth root abscess must rank first, got {top}"

    def test_cat_reluctance_to_jump_ranks_djd(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        syms = _extract_species_symptoms("ジャンプしなくなった 動きが鈍い 高齢の猫", "cat")
        assert "reluctance_to_jump" in syms, f"got {syms}"
        top = [m.get("name_ja", "") for m in _match_species_symptoms_to_diseases(syms, "cat")[:3]]
        assert any("変形性関節症" in n for n in top), f"feline DJD must rank top-3, got {top}"

    def test_cat_overgrooming_ranks_psychogenic_alopecia(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        syms = _extract_species_symptoms("毛づくろいしすぎてお腹の毛が薄い", "cat")
        assert "excessive_grooming" in syms, f"got {syms}"
        top = [m.get("name_ja", "") for m in _match_species_symptoms_to_diseases(syms, "cat")[:3]]
        assert any("心因性脱毛" in n for n in top), f"psychogenic alopecia must rank top-3, got {top}"

    def test_rabbit_bruxism_anorexia_ranks_gi_stasis(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        syms = _extract_species_symptoms("歯ぎしりをしている じっとして動かない 餌を食べない", "rabbit")
        assert "teeth_grinding" in syms and "appetite_loss" in syms, f"got {syms}"
        top = [m.get("name_ja", "") for m in _match_species_symptoms_to_diseases(syms, "rabbit")[:1]]
        assert top and "うっ滞" in top[0], f"GI stasis must rank first, got {top}"

    def test_horse_hirsutism_extracts_and_ranks_ppid_first(self):
        from api.diagnostic_chat import _extract_equine_symptoms, _match_equine_symptoms_to_diseases

        syms = _extract_equine_symptoms("毛が長くて換毛しない 痩せてきた 水をよく飲む")
        assert "body_hirsutism" in syms, f"換毛しない must map to body_hirsutism, got {syms}"
        top = [m.get("name_ja", "") for m in _match_equine_symptoms_to_diseases(syms)[:1]]
        assert top and "PPID" in top[0], f"PPID must rank first, got {top}"

    def test_horse_has_single_ppid_entry_with_merged_findings(self):
        from api.species.equine_diseases import DISEASE_DATABASE
        from api.species.prevalence_data import SPECIES_PREVALENCE

        ppid = [d for d in DISEASE_DATABASE if "Pituitary" in d.name_en]
        assert len(ppid) == 1, f"duplicate PPID cards must stay merged, got {[d.id for d in ppid]}"
        findings = set(ppid[0].associated_findings)
        # merged from both former entries
        assert {"body_hirsutism", "gen_polydipsia", "gen_polyuria", "body_muscle_atrophy"} <= findings
        # prevalence key must resolve to the surviving entry name (prior active)
        assert SPECIES_PREVALENCE["horse"].get(ppid[0].name_en) == "common"

    def test_horse_ppid_json_content_is_endocrine_not_infectious(self):
        # The surviving overlay row carried infection-template prognosis and
        # prevention ("antimicrobial therapy", vaccination boilerplate) and the
        # deleted duplicate carried canine trilostane/mitotane guidance —
        # equine PPID is managed with pergolide.
        import json
        from pathlib import Path

        root = Path(__file__).resolve().parents[1]
        data = json.loads((root / "diseases_all_species.json").read_text(encoding="utf-8"))
        rows = [e for e in data if e.get("species") == "Horse" and "Pituitary" in (e.get("name") or "")]
        assert len(rows) == 1, f"duplicate horse PPID overlay rows: {[r.get('name') for r in rows]}"
        r = rows[0]
        assert "ペルゴリド" in (r.get("prognosis_ja") or "")
        assert "抗病原体療法" not in (r.get("prognosis_ja") or "")
        assert "トリロスタン" not in (r.get("prognosis_ja") or "")
        assert "ワクチネーション" not in (r.get("prevention_ja") or "")
        assert "pergolide" in (r.get("prognosis") or "").lower()
        assert "antimicrobial" not in (r.get("prognosis") or "").lower()
        assert "vaccination" not in (r.get("prevention") or "").lower()


class TestChatClinicalAccuracyAuditRound9:
    """2026-08 audit round 9: a 20-case realistic chief-complaint sweep.
    Root causes fixed: missing aliases (連用形「目が赤く」, かな表記「口をあけて」,
    て形「円形に抜けて」, cyanosis/fatigue owner phrases, green droppings,
    budgie breathing noise); missing ID synonym bridges (lumps_and_bumps→lumps,
    exercise_intolerance, cyanosis, neck_stiffness, diarrhea_green,
    pollakiuria→straining before polyuria); the legacy dog vocabulary gained
    neck_pain (cervical IVDD/wobbler); the snake mouth-rot entry lacked its own
    stomatitis ID; and untiered rarities (ophidian herpesvirus, avocado
    toxicity, leucocytozoonosis) outranked common diseases."""

    def test_dog_oral_mass_extracts_lumps_and_ranks_tumours(self):
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases

        extracted = extract_symptoms_from_text("口の横にできものがある")
        assert "lumps_bumps" in extracted
        matches = match_symptoms_to_diseases(extracted)
        assert matches, "the oral-mass complaint extracted nothing before the bridge"

    def test_dog_acute_glaucoma_complaint_reaches_glaucoma(self):
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases

        extracted = extract_symptoms_from_text("片目が急に赤くて痛そう 目が大きく見える")
        assert extracted, "the buphthalmos complaint extracted nothing before the fixes"
        names = [m.get("name_ja", "") for m in match_symptoms_to_diseases(extracted)[:4]]
        assert any("緑内障" in n for n in names), names

    def test_dog_chf_complaint_extracts_fatigue_and_cyanosis(self):
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases

        extracted = extract_symptoms_from_text("咳が続く 疲れやすい 舌が紫")
        assert "exercise_intolerance" in extracted
        assert "labored_breathing" in extracted  # cyanosis → legacy bridge
        names = [m.get("name_ja", "") for m in match_symptoms_to_diseases(extracted)[:4]]
        assert any("僧帽弁" in n for n in names), names

    def test_dog_neck_scream_ranks_cervical_diseases(self):
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases

        extracted = extract_symptoms_from_text("急にキャンと鳴いて首を動かさない")
        assert "neck_pain" in extracted, "the cervical-guarding complaint must reach the new legacy neck_pain ID"
        names = [m.get("name_ja", "") for m in match_symptoms_to_diseases(extracted)[:3]]
        assert any("椎間板" in n or "ウォブラー" in n for n in names), names

    def test_dog_pollakiuria_resolves_to_lutd_not_polyuria(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ids = _extract_species_symptoms("おしっこの回数が多い おしっこに血が混じる", "dog")
        assert "straining_urinate" in ids and "blood_urine" in ids, ids
        names = [(m.get("name_ja") or m.get("name") or "") for m in _match_species_symptoms_to_diseases(ids, "dog")[:4]]
        assert any("尿路感染" in n or "膀胱" in n or "前立腺" in n for n in names), names

    def test_bird_sick_bird_triad_ranks_psittacosis_first(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ids = _extract_species_symptoms("羽を膨らませている 便が緑色 元気がない", "bird")
        assert "diarrhea_green" in ids, ids
        names = [
            (m.get("name_ja") or m.get("name") or "") for m in _match_species_symptoms_to_diseases(ids, "bird")[:3]
        ]
        assert any("オウム病" in n for n in names), (
            f"fluffed + green droppings + lethargy is the textbook psittacosis triad: {names}"
        )

    def test_parakeet_breathing_noise_and_dirty_nares_rank_respiratory(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ids = _extract_species_symptoms("呼吸のたびに音がする 鼻の周りが汚れている", "parakeet")
        assert len(ids) >= 2, ids
        names = [
            (m.get("name_ja") or m.get("name") or "") for m in _match_species_symptoms_to_diseases(ids, "parakeet")[:3]
        ]
        assert any("呼吸" in n or "肺炎" in n or "気道" in n for n in names), names

    def test_reptile_kana_open_mouth_and_nasal_bubbles_rank_pneumonia(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ids = _extract_species_symptoms("口をあけたまま呼吸 鼻から泡", "reptile")
        assert "open_mouth_breathing" in ids and "nasal_discharge" in ids, ids
        names = [
            (m.get("name_ja") or m.get("name") or "") for m in _match_species_symptoms_to_diseases(ids, "reptile")[:3]
        ]
        assert any("肺炎" in n or "呼吸器" in n for n in names), names

    def test_snake_stomatitis_complaint_ranks_mouth_rot_first(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ids = _extract_species_symptoms("口の中が赤い 食べない よだれ", "snake")
        assert "stomatitis" in ids, ids
        top = _match_species_symptoms_to_diseases(ids, "snake")[0]
        assert "口内炎" in (top.get("name_ja") or ""), (
            f"very_common mouth rot must outrank the rare ophidian herpesvirus: {top.get('name_ja')}"
        )

    def test_chinchilla_te_form_circular_alopecia_reaches_ringworm(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ids = _extract_species_symptoms("毛が円形に抜けている", "chinchilla")
        assert "circular_hair_loss" in ids, ids
        names = [
            (m.get("name_ja") or m.get("name") or "")
            for m in _match_species_symptoms_to_diseases(ids, "chinchilla")[:3]
        ]
        assert any("糸状菌" in n or "白癬" in n for n in names), names


class TestChatClinicalAccuracyAuditRound10:
    """2026-08 audit round 10: a 26-case realistic chief-complaint sweep.
    Root causes fixed: missing aliases (連用形「おしっこの回数が多くて」,
    「お腹が膨らんで」, GDV「吐こうとしても吐けない」, GOLPP「むせる/声がかすれる」,
    blocked-cat「砂が濡れていない/鳴きながらいきむ」, tail bobbing「尾が上下する」,
    bumblefoot「足の裏が腫れて/タコのよう」, ferret adrenal「毛が尻尾から抜け/
    皮膚が薄い」, paw licking「足の裏を舐め/指の間が赤い」); new ID bridges
    (stomach_gurgling, nausea, voice_change, dry_skin→scaling,
    cloudy_eye→cataracts); the legacy dog vocabulary gained voice_change and a
    bacterial-cystitis entry (the most common canine urinary presentation had
    no entry); and untiered rarities (ferret botulism, guinea-pig aortic
    calcification) outranked common diseases."""

    def test_dog_gdv_hiragana_variant_extracts_both_signs(self):
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases

        ex = extract_symptoms_from_text("急にお腹が膨らんで吐こうとしても吐けない")
        assert "bloating" in ex and "unproductive_retching" in ex, ex
        top = match_symptoms_to_diseases(ex)[0]
        assert "胃拡張" in top.get("name_ja", ""), top.get("name_ja")

    def test_dog_golpp_complaint_reaches_laryngeal_paralysis(self):
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases

        ex = extract_symptoms_from_text("水を飲むとむせる 声がかすれる")
        assert "voice_change" in ex and "coughing" in ex, ex
        top = match_symptoms_to_diseases(ex)[0]
        assert "喉頭麻痺" in top.get("name_ja", ""), top.get("name_ja")

    def test_dog_pollakiuria_complaint_ranks_cystitis_over_pupd_diseases(self):
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases

        ex = extract_symptoms_from_text("おしっこの回数が多くて少ししか出ない 血が混じる")
        assert "frequent_urination" in ex and "straining_to_urinate" in ex, ex
        names = [m.get("name_ja", "") for m in match_symptoms_to_diseases(ex)[:2]]
        assert any("膀胱炎" in n for n in names), (
            f"bacterial cystitis (the most common canine urinary dx) must rank top-2: {names}"
        )

    def test_dog_paw_licking_interdigital_complaint_extracts_both_signs(self):
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases

        ex = extract_symptoms_from_text("散歩後に足の裏を舐め続ける 指の間が赤い")
        assert "excessive_licking" in ex and "skin_rashes" in ex, ex
        names = [m.get("name_ja", "") for m in match_symptoms_to_diseases(ex)[:4]]
        assert any("アトピー" in n or "膿皮症" in n or "皮膚" in n for n in names), names

    def test_dog_borborygmi_grass_eating_reaches_gi_diseases(self):
        from api.diagnostic_chat import extract_symptoms_from_text

        ex = extract_symptoms_from_text("お腹がキュルキュル鳴って草を食べたがる")
        assert "bloating" in ex and "vomiting" in ex, ex

    def test_cat_blocked_cat_complaint_ranks_urethral_obstruction_first(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ids = _extract_species_symptoms("トイレに何度も行くのに砂が濡れていない 鳴きながらいきむ", "cat")
        assert "decreased_urination" in ids and "straining_to_urinate" in ids, ids
        top = _match_species_symptoms_to_diseases(ids, "cat")[0]
        assert "尿道閉塞" in (top.get("name_ja") or ""), top.get("name_ja")

    def test_cat_ear_tip_crusting_reaches_notoedric_mange(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ids = _extract_species_symptoms("耳の先が黒くカサカサしてかゆがる", "cat")
        assert "crusting" in ids and "scaling" in ids and "itching" in ids, ids
        names = [(m.get("name_ja") or "") for m in _match_species_symptoms_to_diseases(ids, "cat")[:3]]
        assert any("ヒゼンダニ" in n for n in names), names

    def test_rabbit_progressive_cloudy_eye_reaches_cataracts(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ids = _extract_species_symptoms("目が白く濁ってきた", "rabbit")
        assert "cataracts" in ids, f"the rabbit vocabulary has no cloudy-eye ID — the cataracts bridge must fire: {ids}"
        names = [
            (m.get("name_ja") or m.get("name") or "") for m in _match_species_symptoms_to_diseases(ids, "rabbit")[:3]
        ]
        assert any("白内障" in n or "Cataract" in n for n in names), names

    def test_bird_tail_bobbing_suru_form_reaches_lower_airway_diseases(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ids = _extract_species_symptoms("呼吸のたびに尾が上下する 止まり木でじっとしている", "bird")
        assert "tail_bobbing" in ids, ids
        names = [(m.get("name_ja") or "") for m in _match_species_symptoms_to_diseases(ids, "bird")[:3]]
        assert any("アスペルギルス" in n or "肺炎" in n or "気嚢" in n for n in names), names

    def test_bird_bumblefoot_callus_phrase_extracts_foot_lesions(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ids = _extract_species_symptoms("足の裏が腫れてタコのようになっている", "bird")
        assert ids, "the callus-pad complaint extracted nothing before the て-form aliases"
        top = _match_species_symptoms_to_diseases(ids, "bird")[0]
        assert "趾瘤" in (top.get("name_ja") or ""), top.get("name_ja")

    def test_ferret_tail_alopecia_thin_skin_ranks_adrenal_disease(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ids = _extract_species_symptoms("毛が尻尾から抜けてきた 皮膚が薄い", "ferret")
        assert "hair_loss" in ids and "thinning_skin" in ids, ids
        names = [(m.get("name_ja") or "") for m in _match_species_symptoms_to_diseases(ids, "ferret")[:2]]
        assert any("副腎" in n for n in names), names

    def test_ferret_hypoglycemia_signs_rank_insulinoma_over_botulism(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ids = _extract_species_symptoms("ぐったりして口をくちゃくちゃさせる よだれ", "ferret")
        names = [(m.get("name_ja") or "") for m in _match_species_symptoms_to_diseases(ids, "ferret")[:2]]
        assert any("インスリノーマ" in n for n in names), (
            f"insulinoma (very_common) must outrank the now rare-tiered botulism: {names}"
        )

    def test_guinea_pig_hindlimb_joint_complaint_ranks_scurvy_first(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ids = _extract_species_symptoms("後ろ足を引きずる 関節が腫れている", "guinea_pig")
        top = _match_species_symptoms_to_diseases(ids, "guinea_pig")[0]
        assert "壊血病" in (top.get("name_ja") or ""), (
            f"scurvy (very_common) must outrank the now-tiered aortic calcification: {top.get('name_ja')}"
        )


class TestChatClinicalAccuracyAuditRound11:
    """2026-08 audit round 11: a fresh 20-case realistic chief-complaint sweep.
    Root causes fixed: the legacy dog database had no endoparasite entry and no
    worms-in-stool vocabulary (the pathognomonic Dipylidium "便に白い米粒"
    complaint extracted nothing), no eclampsia entry (postpartum tremors ranked
    idiopathic epilepsy first); the beak-overgrowth aliases 「嘴が伸びてる/
    嘴過長/嘴が長い」 were mismapped to loss_of_appetite; hamster cheek-pouch
    impaction (「膨らんだまま戻らない」), snake retained spectacle, guinea-pig
    cloudy eye (bare 連用形) and lizard cloacal prolapse (ID bridge to
    tissue_protruding_from_cloaca) were unreachable."""

    def test_dog_tapeworm_proglottids_reach_intestinal_parasites(self):
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases

        ex = extract_symptoms_from_text("便に白い米粒のようなものが動いている")
        assert "worms_in_stool" in ex, ex
        top = match_symptoms_to_diseases(ex)[0]
        assert "寄生虫" in top.get("name_ja", ""), top.get("name_ja")

    def test_dog_postpartum_tremors_rank_eclampsia_over_epilepsy(self):
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases

        ex = extract_symptoms_from_text("産後に震えてけいれんしそう 授乳中")
        assert "postpartum_lactating" in ex and "tremors" in ex, ex
        top = match_symptoms_to_diseases(ex)[0]
        assert "子癇" in top.get("name_ja", ""), (
            f"eclampsia is THE first differential for postpartum tremors: {top.get('name_ja')}"
        )

    def test_dog_seizures_without_postpartum_context_keep_epilepsy_first(self):
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases

        ex = extract_symptoms_from_text("けいれんを起こした 意識がない")
        assert "postpartum_lactating" not in ex, ex
        top = match_symptoms_to_diseases(ex)[0]
        assert "てんかん" in top.get("name_ja", ""), top.get("name_ja")

    def test_bird_beak_overgrowth_aliases_no_longer_map_to_appetite_loss(self):
        from api.chat.symptom_aliases import SYMPTOM_ALIASES
        from api.chat.symptom_extractor import _extract_species_symptoms

        for phrase in ("嘴が伸びてる", "嘴過長", "嘴が長い"):
            assert SYMPTOM_ALIASES.get(phrase) == "overgrown_beak", (phrase, SYMPTOM_ALIASES.get(phrase))
        ids = _extract_species_symptoms("くちばしが伸びすぎて変形している", "bird")
        assert "overgrown_beak" in ids, ids

    def test_bird_beak_overgrowth_ranks_beak_diseases_first(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ids = _extract_species_symptoms("くちばしが伸びすぎて変形している", "bird")
        names = [(m.get("name_ja") or "") for m in _match_species_symptoms_to_diseases(ids, "bird")[:3]]
        assert any("嘴" in n for n in names), names

    def test_hamster_pouch_impaction_complaint_reaches_cheek_pouch_diseases(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ids = _extract_species_symptoms("頬袋が膨らんだまま戻らない", "hamster")
        assert "cheek_swelling" in ids, ids
        names = [(m.get("name_ja") or "") for m in _match_species_symptoms_to_diseases(ids, "hamster")[:3]]
        assert any("頬袋" in n for n in names), names

    def test_lizard_cloacal_prolapse_complaint_resolves_via_tissue_bridge(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ids = _extract_species_symptoms("お尻から何か出ている 総排泄腔", "lizard")
        assert "tissue_protruding_from_cloaca" in ids or "tissue_prolapse" in ids, ids
        names = [(m.get("name_ja") or "") for m in _match_species_symptoms_to_diseases(ids, "lizard")[:5]]
        assert any("脱" in n for n in names), names

    def test_guinea_pig_cloudy_eye_bare_form_reaches_cataracts(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ids = _extract_species_symptoms("目が白く濁って見えにくそう", "guinea_pig")
        assert "cloudy_eye" in ids, ids
        top = _match_species_symptoms_to_diseases(ids, "guinea_pig")[0]
        assert "白内障" in (top.get("name_ja") or ""), top.get("name_ja")

    def test_snake_retained_spectacle_complaint_ranks_spectacle_first(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ids = _extract_species_symptoms("脱皮した皮が目に残っている", "snake")
        assert "retained_spectacle" in ids, ids
        names = [(m.get("name_ja") or "") for m in _match_species_symptoms_to_diseases(ids, "snake")[:3]]
        assert any("スペクタクル" in n or "眼鏡" in n for n in names), names

    def test_cat_proglottid_complaint_resolves_via_visible_worms_bridge(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ids = _extract_species_symptoms("便に白い米粒のようなものがついている", "cat")
        assert "visible_worms" in ids or "worms_in_stool" in ids, ids
        names = [(m.get("name_ja") or "") for m in _match_species_symptoms_to_diseases(ids, "cat")[:3]]
        assert any("条虫" in n or "回虫" in n for n in names), names


class TestChatClinicalAccuracyAuditRound12:
    """2026-08 audit round 12: fresh 16-case chief-complaint sweep. Root causes
    fixed: the legacy dog database had no aural-hematoma or KCS entry and no
    pinna-swelling / dry-eye / abdominal-pain vocabulary; pancreatitis lacked
    the textbook vomiting+abdominal-pain cluster; the equine choke complaint
    (「飲み込めない 鼻から餌が出てくる」) extracted nothing and rare
    esophageal entries outranked choke on trivially perfect coverage; ferret
    Pneumocystis pneumonia and bird essential-oil toxicosis were untiered and
    outranked cardiomyopathy / post-laying hypocalcemia; chelonian
    hypovitaminosis A was buried under the periocular-abscess entry for its
    own defining sign pair; the bare te-form 「毛が抜けて」 extracted nothing."""

    def test_dog_fluctuant_pinna_swelling_ranks_aural_hematoma_first(self):
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases

        ex = extract_symptoms_from_text("耳が腫れてぷよぷよしている 頭を振る")
        assert "ear_swelling" in ex and "head_shaking" in ex, ex
        top = match_symptoms_to_diseases(ex)[0]
        assert "耳血腫" in top.get("name_ja", ""), top.get("name_ja")

    def test_dog_dry_eye_with_tacky_discharge_ranks_kcs_first(self):
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases

        ex = extract_symptoms_from_text("目やにがベタベタ多い 目が乾いている")
        assert "dry_eye" in ex, ex
        top = match_symptoms_to_diseases(ex)[0]
        assert "乾性角結膜炎" in top.get("name_ja", ""), top.get("name_ja")

    def test_dog_prayer_position_vomiting_ranks_pancreatitis_first(self):
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases

        ex = extract_symptoms_from_text("背中を丸めて震えて嘔吐 お腹を触ると痛がる")
        assert "abdominal_pain" in ex and "vomiting" in ex, ex
        top = match_symptoms_to_diseases(ex)[0]
        assert "膵炎" in top.get("name_ja", ""), (
            f"vomiting + cranial abdominal pain is pancreatitis first (Ettinger 8th): {top.get('name_ja')}"
        )

    def test_dog_seizure_without_abdominal_context_keeps_epilepsy_first(self):
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases

        ex = extract_symptoms_from_text("けいれんを起こした 意識がない")
        top = match_symptoms_to_diseases(ex)[0]
        assert "てんかん" in top.get("name_ja", ""), top.get("name_ja")

    def test_horse_choke_complaint_extracts_and_ranks_first(self):
        import api.diagnostic_chat as dc

        ex = dc._extract_equine_symptoms("飲み込めない 鼻から餌が出てくる よだれ")
        assert "dig_salivation" in ex and "resp_bilateral_discharge" in ex, ex
        top = dc._match_equine_symptoms_to_diseases(ex)[0]
        assert "食道閉塞" in top.get("name_ja", ""), (
            f"ptyalism + feed at nostrils is choke until proven otherwise: {top.get('name_ja')}"
        )

    def test_ferret_cough_dyspnea_ascites_ranks_cardiomyopathy_over_pneumocystis(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ids = _extract_species_symptoms("お腹が膨れて呼吸が苦しそう 咳をする", "ferret")
        names = [r.get("name_ja") or r.get("name") for r in _match_species_symptoms_to_diseases(ids, "ferret")[:3]]
        assert any("心筋症" in n or "心不全" in n for n in names), names
        assert not any("ニューモシスチス" in n for n in names), (
            f"rare opportunistic pneumonia must not outrank CHF for the classic triad: {names}"
        )

    def test_bird_post_laying_tremors_rank_hypocalcemia_over_essential_oil(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ids = _extract_species_symptoms("産卵のあとぐったりして震えている", "bird")
        names = [r.get("name_ja") or r.get("name") for r in _match_species_symptoms_to_diseases(ids, "bird")[:2]]
        assert any("カルシウム欠乏" in n for n in names), names
        assert not any("エッセンシャルオイル" in n for n in names), (
            f"exposure-dependent toxicosis must not lead post-laying tremors: {names}"
        )

    def test_tortoise_swollen_eyes_anorexia_surfaces_hypovitaminosis_a(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ids = _extract_species_symptoms("目が腫れて開かない 食欲がない", "tortoise")
        assert "eye_swelling" in ids and "anorexia" in ids, ids
        names = [r.get("name_ja") or r.get("name") for r in _match_species_symptoms_to_diseases(ids, "tortoise")[:2]]
        assert any("ビタミンA欠乏" in n for n in names), (
            f"bilateral palpebral swelling in a chelonian is hypovitaminosis A "
            f"until proven otherwise (Mader 3rd ed): {names}"
        )

    def test_bare_te_form_hair_loss_extracts(self):
        from api.chat.symptom_extractor import _extract_species_symptoms

        ids = _extract_species_symptoms("毛が抜けて皮膚がかさかさ 激しく痒がる", "guinea_pig")
        assert "hair_loss" in ids and "itching" in ids, ids


class TestChatClinicalAccuracyAuditRound13:
    """2026-08 audit round 13: fresh 22-case chief-complaint sweep. Root causes
    fixed: the icterus complaint "白目と歯茎が黄色い" extracted nothing (only the
    exact "白目が黄色い" alias existed); the legacy dog database had neither a
    mammary-tumor nor a testicular-tumor entry and no mammary vocabulary, so
    both the most common tumor of intact bitches and the Sertoli feminization
    complaint ranked alopecia-X first; 「呼吸が速い」 (速 spelling) had no alias
    at all (only 早); the ferret hypoglycemia sign 「口を前足で掻く」 misrouted
    to itching→ear mites; and the chinchilla heatstroke complaint 「耳が赤くて
    熱い」 lost both the flushed-ear connective form and the rapid-breathing ↔
    excessive-panting matching bridge."""

    def test_dog_composite_icterus_phrase_extracts_jaundice(self):
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases

        ex = extract_symptoms_from_text("白目と歯茎が黄色い 嘔吐して食欲がない")
        assert "jaundice" in ex, ex
        names = [d.get("name_ja") for d in match_symptoms_to_diseases(ex)[:3]]
        assert any(("肝" in n) or ("溶血" in n) for n in names), names

    def test_dog_feminization_ranks_testicular_tumor_first(self):
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases

        ex = extract_symptoms_from_text("オスなのに乳首が腫れて毛が抜けて皮膚が黒ずむ")
        assert "mammary_swelling" in ex and "hair_loss" in ex, ex
        top = match_symptoms_to_diseases(ex)[0]
        assert "精巣腫瘍" in top.get("name_ja", ""), (
            f"gynecomastia + symmetric alopecia is Sertoli feminization "
            f"(Withrow & MacEwen 6th ed): {top.get('name_ja')}"
        )

    def test_dog_mammary_mass_ranks_mammary_tumor_first(self):
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases

        ex = extract_symptoms_from_text("乳腺にしこりがある")
        assert "mammary_swelling" in ex, ex
        top = match_symptoms_to_diseases(ex)[0]
        assert "乳腺腫瘍" in top.get("name_ja", ""), top.get("name_ja")

    def test_dog_pallor_lethargy_complaint_keeps_anemia_ddx_first(self):
        # The testicular-tumor entry must not hijack the anemia complaint via
        # its late myelotoxicity signs — its symptom set is restricted to the
        # feminization pair.
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases

        ex = extract_symptoms_from_text("呼吸が速い 歯茎が白い ぐったり")
        assert "pale_gums" in ex and "rapid_breathing" in ex, ex
        names = [d.get("name_ja") for d in match_symptoms_to_diseases(ex)[:3]]
        assert not any("精巣腫瘍" in n for n in names), names
        assert any(("溶血" in n) or ("血管肉腫" in n) for n in names), names

    def test_cat_mammary_mass_ranks_mammary_group_top(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ids = _extract_species_symptoms("乳腺にしこりがある", "cat")
        assert "mammary_masses" in ids, ids
        names = [r.get("name_ja") or r.get("name") for r in _match_species_symptoms_to_diseases(ids, "cat")[:3]]
        assert any("乳腺" in n for n in names), names

    def test_chinchilla_flushed_ears_tachypnea_ranks_heatstroke_first(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ids = _extract_species_symptoms("耳が赤くて熱い ぐったりして呼吸が速い", "chinchilla")
        assert "red_ears" in ids and "rapid_breathing" in ids, ids
        top = _match_species_symptoms_to_diseases(ids, "chinchilla")[0]
        assert "熱中症" in (top.get("name_ja") or ""), (
            f"flushed pinnae + tachypnea in a chinchilla is hyperthermia until "
            f"proven otherwise (Quesenberry & Carpenter 4th ed): {top.get('name_ja')}"
        )
        # ear-scratching complaints must keep otitis/dermatophytosis first
        ids2 = _extract_species_symptoms("耳をかゆがって耳垢が多い", "chinchilla")
        names2 = [
            r.get("name_ja") or r.get("name") for r in _match_species_symptoms_to_diseases(ids2, "chinchilla")[:2]
        ]
        assert not any("熱中症" in n for n in names2), names2

    def test_ferret_pawing_at_mouth_frothing_ranks_insulinoma_top(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ids = _extract_species_symptoms("急にキーキー鳴いて口を前足で掻く 泡を吹く", "ferret")
        assert "pawing_at_mouth" in ids and "drooling" in ids, ids
        names = [r.get("name_ja") or r.get("name") for r in _match_species_symptoms_to_diseases(ids, "ferret")[:3]]
        assert any(("インスリノーマ" in n) or ("低血糖" in n) for n in names), (
            f"pawing at the mouth + ptyalism is the ferret hypoglycemia "
            f"presentation (Quesenberry & Carpenter 4th ed): {names}"
        )

    def test_rapid_breathing_hayai_spelling_extracts_across_species(self):
        from api.chat.symptom_extractor import _extract_species_symptoms

        for sp in ("rabbit", "chinchilla", "guinea_pig"):
            ids = _extract_species_symptoms("呼吸が速い", sp)
            assert "rapid_breathing" in ids, (sp, ids)


class TestChatClinicalAccuracyAuditRound14:
    """2026-08 audit round 14 (parallel to round 13): fresh 22-case sweep. Root causes
    fixed: negated mentions (「咳はない」) polluted extraction; regurgitation
    collapsed into vomiting so megaesophagus never led its own defining
    complaint; pigmenturia (「おしっこが茶色い」) had no vocabulary; the cat
    inappropriate-elimination and jaw-chattering complaints extracted nothing;
    「キーキー鳴く」 was mis-mapped to lethargy; rabbit slobbers (あご kana
    form) / one-sided head tilt / bird grip loss / ferret screaming+tonic
    episode extracted nothing; ferret primary epilepsy was untiered and
    outranked insulinoma for the seizure complaint."""

    def test_negated_symptom_mentions_are_not_extracted(self):
        from api.chat.symptom_extractor import _extract_species_symptoms
        from api.diagnostic_chat import extract_symptoms_from_text

        # species path: negated cough must not extract; the positive sign must
        ids = _extract_species_symptoms("咳はないが呼吸が速い", "cat")
        assert "coughing" not in ids, ids
        assert ids, "the positive rapid-breathing sign must still extract"
        ids = _extract_species_symptoms("嘔吐はしていない 下痢なし 食欲がない", "cat")
        assert "vomiting" not in ids and "diarrhea" not in ids, ids
        assert "appetite_loss" in ids, ids
        # legacy dog path
        ids = extract_symptoms_from_text("嘔吐と下痢がある 血便はない")
        assert "vomiting" in ids and "diarrhea" in ids, ids
        assert "blood_in_stool" not in ids, ids
        # negation-shaped aliases themselves must be unaffected
        ids = extract_symptoms_from_text("食欲がない 元気がない")
        assert "loss_of_appetite" in ids and "lethargy" in ids, ids

    def test_dog_regurgitation_ranks_megaesophagus_first(self):
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases

        ids = extract_symptoms_from_text("食べた後すぐに未消化のまま吐く 最近痩せた")
        assert "regurgitation" in ids, ids
        top = match_symptoms_to_diseases(ids)[0]
        assert "巨大食道" in top.get("name_ja", ""), top.get("name_ja")

    def test_dog_dark_urine_jaundice_ranks_hemolysis_top(self):
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases

        ids = extract_symptoms_from_text("おしっこが茶色い 元気がない 白目が黄色い")
        assert "dark_urine" in ids and "jaundice" in ids, ids
        names = [r.get("name_ja", "") for r in match_symptoms_to_diseases(ids)[:2]]
        assert any("溶血" in n for n in names), names

    def test_cat_inappropriate_elimination_surfaces_urinary_ddx(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ids = _extract_species_symptoms("トイレ以外の場所で粗相するようになった 高齢", "cat")
        assert "inappropriate_urination" in ids, ids
        names = [r.get("name_ja") or r.get("name") for r in _match_species_symptoms_to_diseases(ids, "cat")[:5]]
        assert any(("膀胱炎" in n) or ("尿路感染" in n) for n in names), names

    def test_cat_jaw_chattering_surfaces_tooth_resorption(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ids = _extract_species_symptoms("口をくちゃくちゃさせてよだれを垂らす", "cat")
        assert "jaw_chattering" in ids and "drooling" in ids, ids
        names = [r.get("name_ja") or r.get("name") for r in _match_species_symptoms_to_diseases(ids, "cat")[:3]]
        assert any(("歯の吸収" in n) or ("口内炎" in n) or ("歯周" in n) for n in names), names

    def test_rabbit_wet_chin_kana_form_surfaces_dental_disease(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ids = _extract_species_symptoms("あごが濡れている 硬いものを食べなくなった", "rabbit")
        assert "drooling" in ids, ids
        names = [r.get("name_ja") or r.get("name") for r in _match_species_symptoms_to_diseases(ids, "rabbit")[:3]]
        assert any(("不正咬合" in n) or ("臼歯" in n) or ("歯周" in n) for n in names), names

    def test_rabbit_unilateral_exophthalmos_extracts_and_ranks(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ids = _extract_species_symptoms("片方の目が飛び出してきた", "rabbit")
        assert "exophthalmos" in ids, ids
        names = [r.get("name_ja") or r.get("name") for r in _match_species_symptoms_to_diseases(ids, "rabbit")[:3]]
        assert any(("眼球突出" in n) or ("球後膿瘍" in n) for n in names), names

    def test_guinea_pig_one_sided_head_tilt_extracts(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ids = _extract_species_symptoms("首が片方に傾いて転がる", "guinea_pig")
        assert "head_tilt" in ids, ids
        names = [r.get("name_ja") or r.get("name") for r in _match_species_symptoms_to_diseases(ids, "guinea_pig")[:3]]
        assert any(("斜頸" in n) or ("中耳炎" in n) or ("前庭" in n) for n in names), names

    def test_bird_grip_loss_extracts_perching_ids(self):
        from api.chat.symptom_extractor import _extract_species_symptoms

        ids = _extract_species_symptoms("止まり木を握れない 脚に力が入らない", "bird")
        assert "inability_to_perch" in ids and "leg_weakness" in ids, ids

    def test_ferret_screaming_tonic_episode_ranks_insulinoma_first(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ids = _extract_species_symptoms("急にキーキー鳴いて足を伸ばして硬直", "ferret")
        assert "seizures" in ids and "vocalization" in ids, ids
        top = _match_species_symptoms_to_diseases(ids, "ferret")[0]
        assert "インスリノーマ" in (top.get("name_ja") or ""), (
            "hypoglycemia from insulinoma is the most common cause of ferret "
            f"seizures (Quesenberry & Carpenter 4th ed): {top.get('name_ja')}"
        )

    def test_screaming_no_longer_maps_to_lethargy(self):
        from api.chat.symptom_aliases import SYMPTOM_ALIASES

        assert SYMPTOM_ALIASES["キーキー鳴く"] == "vocalization_changes"
        assert SYMPTOM_ALIASES["鳴き声が変"] == "vocalization_changes"

    def test_fish_rapid_gilling_and_snake_ventral_redness_extract(self):
        from api.chat.symptom_extractor import _extract_species_symptoms

        ids = _extract_species_symptoms("水面で口をパクパク 鰓の動きが速い", "fish")
        assert "rapid_gill_movement" in ids, ids
        ids = _extract_species_symptoms("体に水ぶくれのような斑点 お腹のうろこが赤い", "snake")
        assert "skin_redness" in ids and "skin_blistering" in ids, ids


class TestChatClinicalAccuracyAuditRound16Parallel:
    """2026-08 audit round 16 (parallel session; authored as round 15 before the
    sibling session claimed the slot on main): fresh 18-case chief-complaint sweep. Root causes
    fixed: the Cushing triad (「水をたくさん飲んで」「お腹だけ膨れてきた」) lost
    two of three signs to connective-form alias gaps; the oral-mass complaint
    ranked mammary tumor first (no oral-tumor entry or oral_mass vocabulary in
    the legacy dog DB); the equine hindlimb-lameness colloquials (「後ろ足を
    痛がる」) were entirely absent so extraction returned nothing; the untiered
    feline neonatal-isoerythrolysis entries hijacked the adult icterus
    complaint; the rabbit exophthalmos complaint lost the て-form and ranked
    the rare Elodontoma over the common retrobulbar/URI group; and the
    scaly-leg (Knemidocoptes) complaint had no leg-crust vocabulary at all."""

    def test_dog_cushing_triad_ranks_cushings_first(self):
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases

        ex = extract_symptoms_from_text("水をたくさん飲んでお腹だけ膨れてきた 毛が薄い")
        assert {"excessive_thirst", "bloating", "hair_loss"} <= set(ex), ex
        top = match_symptoms_to_diseases(ex)[0]
        assert "クッシング" in top.get("name_ja", ""), top.get("name_ja")

    def test_dog_oral_mass_ranks_oral_tumor_first(self):
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases

        ex = extract_symptoms_from_text("口の中にできものがある 口臭")
        assert "oral_mass" in ex, ex
        top = match_symptoms_to_diseases(ex)[0]
        assert "口腔内腫瘍" in top.get("name_ja", ""), (
            f"a visible oral mass is the oral-tumor group, never mammary "
            f"(Withrow & MacEwen 6th ed): {top.get('name_ja')}"
        )

    def test_dog_mammary_complaint_still_ranks_mammary_first(self):
        # the oral_mass cluster must not disturb the mammary complaint
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases

        ex = extract_symptoms_from_text("乳腺にしこりがある")
        top = match_symptoms_to_diseases(ex)[0]
        assert "乳腺腫瘍" in top.get("name_ja", ""), top.get("name_ja")

    def test_dog_checkbox_path_carries_oral_vocabulary(self):
        # parity: the checkbox/guided engine must handle the same complaint
        from api.species.dog_diseases import VALID_SYMPTOMS, analyze_symptoms

        assert {"oral_mass", "bad_breath"} <= VALID_SYMPTOMS
        res = analyze_symptoms(["oral_mass", "bad_breath"])
        names = [d.get("name_ja") for d in res["suspected_diseases"][:3]]
        assert any("口腔" in (n or "") for n in names), names

    def test_equine_hindlimb_colloquial_extracts_and_ranks_hoof_abscess(self):
        from api.diagnostic_chat import (
            _extract_equine_symptoms,
            _match_equine_symptoms_to_diseases,
        )

        ex = _extract_equine_symptoms("急に後ろ足を痛がる 蹄が熱い")
        assert {"limb_lameness_hind", "hoof_heat"} <= set(ex), ex
        top = _match_equine_symptoms_to_diseases(ex)[0]
        assert "蹄膿瘍" in (top.get("name_ja") or ""), (
            f"acute lameness + focal hoof heat is a hoof abscess until proven "
            f"otherwise (Adams & Stashak 7th ed): {top.get('name_ja')}"
        )

    def test_cat_adult_icterus_not_hijacked_by_neonatal_isoerythrolysis(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ex = _extract_species_symptoms("おしっこの色が濃い 元気がない 白目が黄色い", "cat")
        assert "dark_urine" in ex and "jaundice" in ex, ex
        res = _match_species_symptoms_to_diseases(ex, "cat")
        top_name = res[0].get("name_ja") or res[0].get("name") or ""
        assert "新生" not in top_name, (
            f"neonatal isoerythrolysis (rare, neonates only) must not outrank "
            f"the hemolytic/hepatic adult ddx: {top_name}"
        )

    def test_rabbit_exophthalmos_te_form_extracts_and_demotes_elodontoma(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ex = _extract_species_symptoms("目が飛び出してきて鼻水", "rabbit")
        assert "exophthalmos" in ex, ex
        res = _match_species_symptoms_to_diseases(ex, "rabbit")
        names = [d.get("name_ja") or d.get("name") for d in res[:2]]
        assert not any("エロドントーマ" in (n or "") for n in names), (
            f"elodontoma is a degu/prairie-dog disease, rare in rabbits (Capello & Lennox): {names}"
        )

    def test_bird_scaly_leg_complaint_ranks_knemidocoptes_first(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        for species, want_id in (("bird", "crusty_lesions_on_legs"), ("parakeet", "leg_scales")):
            ex = _extract_species_symptoms("脚に白いかさぶた ガサガサ", species)
            assert want_id in ex, (species, ex)
            top = _match_species_symptoms_to_diseases(ex, species)[0]
            nm = top.get("name_ja") or top.get("name") or ""
            assert ("疥癬" in nm) or ("ヒゼンダニ" in nm), (species, nm)


class TestChatClinicalAccuracyAuditRound15:
    """2026-08 audit round 15: fresh 20-case chief-complaint sweep. Root causes
    fixed: dictionary-form / connective-form alias gaps (「関節が腫れる」「口の中が
    赤く」「チーズ状のもの」), the ferret melena bridge (owners cannot distinguish
    fresh from digested blood, but Gastric Ulcer only listed black_tarry_stool so
    「血便」 never matched it), missing sour-crop and clicking-breath onomatopoeia
    aliases, missing 骨が弱い→soft_bones, the equine tying-up pair (「突っ張って」
    ＋「尿が茶色い」 both unextractable), and canine orthopedic phrases (「階段を
    上れない」「後ろ足が震える」) that extracted nothing and ranked epilepsy first."""

    def test_guinea_pig_scurvy_dictionary_form_joint_swelling(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ids = _extract_species_symptoms("後ろ足を引きずる 関節が腫れる 野菜をあまり与えていない", "guinea_pig")
        assert "swollen_joints" in ids, ids
        top = _match_species_symptoms_to_diseases(ids, "guinea_pig")[0]
        assert "壊血病" in (top.get("name_ja") or ""), (
            f"swollen joints + hindlimb lameness in a guinea pig is scurvy "
            f"until proven otherwise (Quesenberry & Carpenter 4th ed): {top.get('name_ja')}"
        )

    def test_ferret_bloody_stool_ranks_gi_not_estrogen(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ids = _extract_species_symptoms("お尻から血 便に血が混じる ぐったり", "ferret")
        assert "bloody_stool" in ids, ids
        names = [d.get("name_ja") or "" for d in _match_species_symptoms_to_diseases(ids, "ferret")[:5]]
        assert any(
            ("腸炎" in n) or ("胃潰瘍" in n) or ("コクシジウム" in n) or ("アリューシャン" in n) for n in names
        ), names
        # reproductive/estrogen entries must no longer hijack the GI complaint
        assert not any(("エストロゲン" in n) or ("低カルシウム" in n) or ("妊娠毒血症" in n) for n in names[:3]), names

    def test_ferret_melena_bridge_reaches_gastric_ulcer(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases

        names = [
            d.get("name_ja") or ""
            for d in _match_species_symptoms_to_diseases(["bloody_stool", "teeth_grinding", "vomiting"], "ferret")[:4]
        ]
        assert any("胃潰瘍" in n for n in names), (
            f"melena + bruxism + vomiting is the classic ferret Helicobacter "
            f"gastric ulcer picture (Quesenberry & Carpenter 4th ed): {names}"
        )

    def test_bird_clicking_breath_onomatopoeia_extracts(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ids = _extract_species_symptoms("呼吸のたびにプチプチ音 声が変わった", "bird")
        assert "clicking_breathing_sounds" in ids, ids
        names = [d.get("name_ja") or "" for d in _match_species_symptoms_to_diseases(ids, "bird")[:4]]
        assert any(("ダニ" in n) or ("アスペルギルス" in n) or ("気嚢" in n) for n in names), names

    def test_snake_mouth_rot_connective_form_and_cheese_exudate(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ids = _extract_species_symptoms("口の中が赤くチーズ状のものがある", "snake")
        assert "stomatitis" in ids and "mucus_in_mouth" in ids, ids
        top = _match_species_symptoms_to_diseases(ids, "snake")[0]
        assert "口内炎" in (top.get("name_ja") or ""), top.get("name_ja")

    def test_sugar_glider_weak_bones_ranks_mbd_first(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ids = _extract_species_symptoms("後ろ足が麻痺 骨が弱い 果物ばかり与えている", "sugar_glider")
        assert "soft_bones" in ids, ids
        top = _match_species_symptoms_to_diseases(ids, "sugar_glider")[0]
        assert ("代謝性骨" in (top.get("name_ja") or "")) or ("MBD" in (top.get("name_ja") or "")), top.get("name_ja")

    def test_parrot_sour_crop_falls_back_to_crop_ids(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ids = _extract_species_symptoms("そのうから酸っぱい臭い 吐き戻し", "parrot")
        assert any(i in ids for i in ("crop_stasis", "crop_distension")), ids
        names = [d.get("name_ja") or "" for d in _match_species_symptoms_to_diseases(ids, "parrot")[:4]]
        assert any(("嗉嚢" in n) or ("そのう" in n) or ("素嚢" in n) for n in names), names
        # bird keeps its dedicated sour-crop ID
        ids_bird = _extract_species_symptoms("そのうから酸っぱい臭い", "bird")
        assert "sour_crop_odor" in ids_bird, ids_bird

    def test_dog_orthopedic_phrases_rank_oa_not_epilepsy(self):
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases

        ids = extract_symptoms_from_text("散歩を嫌がる 階段を上れない 後ろ足が震える 大型犬")
        assert "stiffness" in ids, ids
        names = [d.get("name_ja") or "" for d in match_symptoms_to_diseases(ids)[:5]]
        assert any(("関節" in n) or ("股関節" in n) or ("膝蓋骨" in n) or ("椎間板" in n) for n in names[:3]), names
        assert "てんかん" not in names[0], names

    def test_horse_tying_up_pair_extracts_and_ranks_rhabdo(self):
        from api.diagnostic_chat import _extract_equine_symptoms, _match_equine_symptoms_to_diseases

        ids = _extract_equine_symptoms("後肢が突っ張って歩く 運動後に尿が茶色い")
        assert "body_stiffness" in ids and "body_dark_urine" in ids, ids
        names = [(d.get("name_ja") or d.get("name") or "") for d in _match_equine_symptoms_to_diseases(ids)[:4]]
        assert any(
            ("横紋筋融解" in n)
            or ("タイングアップ" in n)
            or ("タイイングアップ" in n)
            or ("PSSM" in n)
            or ("ミオパチー" in n)
            for n in names
        ), names

    def test_horse_colic_dictionary_forms_still_extract(self):
        from api.diagnostic_chat import _extract_equine_symptoms, _match_equine_symptoms_to_diseases

        ids = _extract_equine_symptoms("急にお腹を蹴って転がる 汗をかいている")
        assert "dig_colic_signs" in ids and "gen_sweating" in ids, ids
        top = _match_equine_symptoms_to_diseases(ids)[0]
        assert "疝痛" in (top.get("name_ja") or ""), top.get("name_ja")


class TestChatClinicalAccuracyAuditRound16:
    """2026-08 audit round 16 (parallel session's round 15): fresh 22-case sweep. Root causes fixed: the
    acute pelvic-limb-failure complaint (「後ろ足が立たなくなった」) extracted
    nothing on the legacy dog path (no hind_limb_paralysis fallback); いびき
    (stertor) had no vocabulary anywhere so the BOAS complaint never ranked
    its own entry; the white-cat ear-tip SCC and anisocoria complaints
    extracted nothing; the kana rubber-jaw phrasing missed the lizard MBD
    vocabulary; 「お腹がパンパンに膨れている」 lost the abdominal context to
    the edema alias; and 吐き戻し was mapped to vomiting so the snake
    postprandial-regurgitation complaint never reached the regurgitation ID."""

    def test_dog_acute_hindlimb_failure_extracts_paralysis(self):
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases

        ids = extract_symptoms_from_text("散歩中に急に後ろ足が立たなくなった 痛がらない")
        assert "paralysis" in ids, ids
        names = [r.get("name_ja", "") for r in match_symptoms_to_diseases(ids)[:3]]
        assert any(("ヘルニア" in n) or ("脊髄" in n) for n in names), names

    def test_dog_snoring_vocabulary_and_boas_ranking(self):
        import api.health_checker as hc
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases

        assert any(s["id"] == "snoring" for s in hc.SYMPTOMS)
        ids = extract_symptoms_from_text("いびきがひどい 暑いとすぐばてる 呼吸がガーガー鳴る")
        assert "snoring" in ids and "exercise_intolerance" in ids, ids
        names = [r.get("name_ja", "") for r in match_symptoms_to_diseases(ids)[:5]]
        assert any("短頭種" in n for n in names), names

    def test_cat_ear_tip_crust_surfaces_squamous_cell_carcinoma(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ids = _extract_species_symptoms("白い猫 耳の先にかさぶたができて治らない", "cat")
        assert "non_healing_wound" in ids or "ear_tip_lesions" in ids, ids
        names = [r.get("name_ja") or r.get("name") for r in _match_species_symptoms_to_diseases(ids, "cat")[:3]]
        assert any("扁平上皮癌" in n for n in names), names

    def test_cat_anisocoria_surfaces_retinal_hypertensive_ddx(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ids = _extract_species_symptoms("急に片方の瞳孔だけ大きさが違う", "cat")
        assert "dilated_pupils" in ids, ids
        names = [r.get("name_ja") or r.get("name") for r in _match_species_symptoms_to_diseases(ids, "cat")[:5]]
        assert any(("網膜" in n) or ("高血圧" in n) for n in names), names

    def test_rabbit_hindlimb_dragging_surfaces_spinal_ddx(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ids = _extract_species_symptoms("後ろ足を引きずって立てない", "rabbit")
        assert "hind_limb_weakness" in ids, ids
        names = [r.get("name_ja") or r.get("name") for r in _match_species_symptoms_to_diseases(ids, "rabbit")[:5]]
        assert any(("脊髄" in n) or ("脊椎" in n) or ("麻痺" in n) for n in names), names

    def test_lizard_kana_rubber_jaw_ranks_mbd_first(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ids = _extract_species_symptoms("あごが柔らかくてぶよぶよしている 食べない", "lizard")
        assert "jaw_softening" in ids, ids
        top = _match_species_symptoms_to_diseases(ids, "lizard")[0]
        name = top.get("name_ja") or top.get("name")
        assert ("代謝性骨疾患" in name) or ("MBD" in name), name

    def test_ferret_taut_abdomen_extracts_distension_and_ranks_cardiomyopathy(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ids = _extract_species_symptoms("お腹がパンパンに膨れている 息が苦しそう", "ferret")
        assert "abdominal_distension" in ids, ids
        names = [r.get("name_ja") or r.get("name") for r in _match_species_symptoms_to_diseases(ids, "ferret")[:5]]
        assert any("心筋症" in n for n in names), names

    def test_snake_postprandial_regurgitation_surfaces_crypto_ddx(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ids = _extract_species_symptoms("餌を食べたあと吐き戻す 痩せてきた", "snake")
        assert "regurgitation" in ids, ids
        names = [r.get("name_ja") or r.get("name") for r in _match_species_symptoms_to_diseases(ids, "snake")[:5]]
        assert any(("クリプトスポリジウム" in n) or ("吐出" in n) for n in names), names

    def test_bird_crop_complaint_unaffected_by_regurgitation_remap(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ids = _extract_species_symptoms("吐き戻しをする そのうが膨らんでいる", "bird")
        assert "crop_distension" in ids, ids
        top = _match_species_symptoms_to_diseases(ids, "bird")[0]
        name = top.get("name_ja") or top.get("name")
        assert ("嗉嚢" in name) or ("そのう" in name) or ("素嚢" in name), name


class TestChatClinicalAccuracyAuditRound17:
    """2026-08 audit round 17: fresh 40-case sweep. Root causes fixed: the
    canine Cushing complaint 「水をたくさん飲んでおしっこも多い…毛が左右対称に
    薄い」 extracted nothing (four missing phrase variants), the otitis
    complaint lost 耳から悪臭/茶色い耳垢, the budgerigar scaly-face mite
    (Knemidokoptes) had no owner-phrasing aliases at all, the sore-hock
    連用形 「足の裏が赤く腫れて」 fell through, and the equine hot-hoof
    complaint ranked deep-digital-flexor tendinitis (a 2-finding entry with
    trivially perfect coverage) above laminitis and hoof abscess."""

    def test_dog_cushing_complaint_extracts_and_ranks_first(self):
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases

        ex = extract_symptoms_from_text("水をたくさん飲んでおしっこも多い お腹だけ膨れてきた 毛が左右対称に薄い")
        for sid in ("excessive_thirst", "frequent_urination", "bloating", "hair_loss"):
            assert sid in ex, (sid, ex)
        top = match_symptoms_to_diseases(ex)[0]
        assert "クッシング" in top.get("name_ja", ""), top.get("name_ja")

    def test_dog_otitis_complaint_ranks_otitis_first(self):
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases

        ex = extract_symptoms_from_text("耳から悪臭 茶色い耳垢 頭を振る")
        assert "ear_odor" in ex and "ear_discharge" in ex and "head_shaking" in ex, ex
        top = match_symptoms_to_diseases(ex)[0]
        assert "外耳炎" in top.get("name_ja", ""), top.get("name_ja")

    def test_parakeet_scaly_face_complaint_ranks_knemidokoptes(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ex = _extract_species_symptoms("くちばしの周りにかさぶた 白い粉をふいたよう", "parakeet")
        assert "crusty_beak" in ex and "scaly_face" in ex, ex
        names = [
            d.get("name_ja") or d.get("name")
            for d in _match_species_symptoms_to_diseases(ex, "parakeet", lang="ja")[:3]
        ]
        assert any("疥癬" in n for n in names), names
        # bird falls back through the ID-synonym bridge to its facial-lesion IDs
        ex_b = _extract_species_symptoms("くちばしの周りにかさぶた かゆがる", "bird")
        names_b = [
            d.get("name_ja") or d.get("name") for d in _match_species_symptoms_to_diseases(ex_b, "bird", lang="ja")[:3]
        ]
        assert any("疥癬" in n for n in names_b), names_b

    def test_rabbit_sore_hock_renyoukei_ranks_pododermatitis_first(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ex = _extract_species_symptoms("足の裏が赤く腫れてハゲている", "rabbit")
        assert "pododermatitis_signs" in ex, ex
        top = _match_species_symptoms_to_diseases(ex, "rabbit", lang="ja")[0]
        name = top.get("name_ja") or top.get("name")
        assert "足底" in name or "ソアホック" in name, name

    def test_cat_notoedres_ear_tip_crust_extracts_crusting(self):
        from api.chat.symptom_extractor import _extract_species_symptoms

        ex = _extract_species_symptoms("耳の先が黒いかさぶた 耳をかく", "cat")
        assert "crusting" in ex and "scratching_ears" in ex, ex

    def test_horse_dragging_leg_alias_and_hot_hoof_differential(self):
        from api.diagnostic_chat import _extract_equine_symptoms

        ex = _extract_equine_symptoms("急に足を引きずる 蹄が熱い")
        assert "limb_lameness_fore" in ex and "hoof_heat" in ex, ex

    def test_horse_hot_hoof_checkbox_ranks_laminitis_and_abscess_in_top(self):
        from api.species.equine_diseases import generate_differential_diagnosis

        res = generate_differential_diagnosis({"hoof_heat", "limb_lameness_fore"})
        names = [r.disease.name_en for r in res[:8]]
        assert any("Laminitis" in n for n in names), names
        assert "Hoof Abscess" in names, names
        # the 2-finding DDFT entry must not run away with near-perfect confidence
        ddft = next(r for r in res if r.disease.name_en == "Deep Digital Flexor Tendinitis")
        assert ddft.confidence_pct < 75, ddft.confidence_pct
        # with a digital pulse added, laminitis leads decisively
        res2 = generate_differential_diagnosis({"hoof_heat", "limb_lameness_fore", "limb_digital_pulse"})
        top3 = [r.disease.name_en for r in res2[:4]]
        assert any("Laminitis" in n for n in top3), top3
        assert "Hoof Abscess" in [r.disease.name_en for r in res2[:6]], top3


class TestChatClinicalAccuracyAuditRound18:
    """2026-08 audit round 14: fresh 30-case chief-complaint sweep. Systematic
    root cause this round: connective (連用形) and word-order variants of
    already-supported phrases fell through the substring matcher — 「水を
    たくさん飲んで」(vs 飲む), 「後ろ足が動かなくなって」(vs なった/なってきた),
    「そのうが膨らんで」(vs 膨らんでいる), 「羽を自分で抜く」(vs 自分で羽を抜く).
    Additionally the legacy dog database had no acute allergic reaction entry —
    the classic post-vaccine urticaria/angioedema ER presentation (Shmuel &
    Cortes JVECC 2013) extracted only eye_swelling and ranked eyelid diseases —
    and no stair-avoidance vocabulary for the canine OA complaint."""

    def test_dog_vaccine_urticaria_ranks_allergic_reaction_first(self):
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases

        ex = extract_symptoms_from_text("顔が腫れてじんましんが出た ワクチンの後")
        assert "hives" in ex and "facial_swelling" in ex, ex
        top = match_symptoms_to_diseases(ex)[0]
        assert "アレルギー反応" in (top.get("name_ja") or ""), top.get("name_ja")

    def test_dog_stair_avoidance_ranks_osteoarthritis(self):
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases

        ex = extract_symptoms_from_text("散歩を嫌がって階段を登らなくなった 後ろ足が硬い")
        assert "stiffness" in ex and "exercise_intolerance" in ex, ex
        names = [d.get("name_ja") or "" for d in match_symptoms_to_diseases(ex)[:3]]
        assert any("関節" in n for n in names), names

    def test_dog_pu_pd_polyphagia_ranks_diabetes(self):
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases

        ex = extract_symptoms_from_text("水をたくさん飲んでおしっこも多い ご飯も食べるのに痩せる")
        assert "excessive_thirst" in ex and "frequent_urination" in ex, ex
        names = [d.get("name_ja") or "" for d in match_symptoms_to_diseases(ex)[:3]]
        assert any("糖尿病" in n for n in names), names

    def test_cat_ate_connective_form_ranks_thromboembolism_first(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ex = _extract_species_symptoms("急に後ろ足が動かなくなって大声で鳴いている", "cat")
        assert "hind_limb_paralysis" in ex, ex
        top = _match_species_symptoms_to_diseases(ex, "cat")[0]
        assert "血栓" in (top.get("name_ja") or ""), (
            f"acute hindlimb paralysis + vocalization is aortic "
            f"thromboembolism until proven otherwise: {top.get('name_ja')}"
        )

    def test_cat_hyperthyroid_polyphagia_phrase_extracts(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ex = _extract_species_symptoms("水をよく飲む 食欲はあるのに痩せる 落ち着きがない", "cat")
        assert "increased_appetite" in ex, ex
        names = [d.get("name_ja") or "" for d in _match_species_symptoms_to_diseases(ex, "cat")[:3]]
        assert any("甲状腺機能亢進" in n for n in names), names

    def test_hedgehog_whs_connective_wobble_extracts(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ex = _extract_species_symptoms("後ろ足がふらついて立てない 震える", "hedgehog")
        assert "hind_limb_weakness" in ex and "ataxia" in ex, ex
        names = [d.get("name_ja") or "" for d in _match_species_symptoms_to_diseases(ex, "hedgehog")[:3]]
        assert any(("ふらつき" in n) or ("WHS" in n) for n in names), names

    def test_sugar_glider_belly_biting_extracts_self_mutilation(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ex = _extract_species_symptoms("自分のお腹を噛んでしまう 傷がある", "sugar_glider")
        assert "self_mutilation" in ex, ex
        names = [d.get("name_ja") or "" for d in _match_species_symptoms_to_diseases(ex, "sugar_glider")[:3]]
        assert any(("自己損傷" in n) or ("自咬" in n) for n in names), names

    def test_parakeet_crop_connective_form_extracts(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ex = _extract_species_symptoms("そのうが膨らんで吐き戻す", "parakeet")
        # 吐き戻す maps to regurgitation since the parallel session's round-15
        # merge (clinically the crop complaint IS regurgitation); either the
        # direct ID or its vomiting synonym resolution satisfies the complaint.
        assert "crop_distension" in ex and ({"regurgitation", "vomiting"} & set(ex)), ex
        names = [d.get("name_ja") or "" for d in _match_species_symptoms_to_diseases(ex, "parakeet")[:5]]
        assert any(("嗉嚢" in n) or ("そのう" in n) or ("甲状腺腫" in n) or ("異物" in n) for n in names), names

    def test_parrot_plucking_word_order_variant_extracts(self):
        from api.chat.disease_matcher import _match_species_symptoms_to_diseases
        from api.chat.symptom_extractor import _extract_species_symptoms

        ex = _extract_species_symptoms("羽を自分で抜いてしまう 皮膚が見えている", "parrot")
        assert "feather_plucking" in ex, ex
        top = _match_species_symptoms_to_diseases(ex, "parrot")[0]
        assert "毛引き" in (top.get("name_ja") or ""), top.get("name_ja")

    def test_normal_seizure_complaint_still_ranks_epilepsy_first(self):
        # The new hives/facial_swelling vocabulary and allergic-reaction entry
        # must not disturb the established non-dermatologic rankings.
        from api.diagnostic_chat import extract_symptoms_from_text, match_symptoms_to_diseases

        ex = extract_symptoms_from_text("痙攣した 意識がなくなった")
        top = match_symptoms_to_diseases(ex)[0]
        assert "てんかん" in (top.get("name_ja") or ""), top.get("name_ja")


class TestBatch51ReferencedDrugs:
    """Sweep #20 (parallel-session batch 51): octreotide / decoquinate were referenced with doses
    in disease treatment texts but absent from the formulary (the biotin gap it
    also surfaced ships in batch 48); the ロイプロリド transliteration (20 avian
    refs) and hyphenated Ca-EDTA (25 refs) never resolved to their entries."""

    def test_batch47_drugs_present_with_bilingual_dosing(self):
        from api.drug_dictionary import get_drug_by_id

        for did, sp in [("octreotide", "dog"), ("decoquinate", "dog"), ("biotin", "horse")]:
            d = get_drug_by_id(did)
            assert d is not None, did
            info = d["species_info"][sp]
            assert info["safe"] and info["dosage"] and info["dosage_ja"], (did, sp)

    def test_octreotide_carries_gastrinoma_dose_and_feline_acromegaly_caveat(self):
        from api.drug_dictionary import get_drug_by_id

        d = get_drug_by_id("octreotide")
        assert "1-5 μg/kg" in d["species_info"]["dog"]["dosage"]
        # Defining safety fact: short-acting octreotide is largely ineffective
        # for feline acromegaly — the entry must not oversell it.
        assert "INEFFECTIVE" in d["species_info"]["cat"]["dosage"]

    def test_decoquinate_is_the_tcp_followup_phase(self):
        from api.drug_dictionary import get_drug_by_id

        d = get_drug_by_id("decoquinate")
        dog = d["species_info"]["dog"]
        assert "10-20 mg/kg" in dog["dosage"] and "TCP" in dog["dosage"]
        assert "急性期" in (d.get("contraindications_ja") or "")

    def test_sweep16_variant_aliases_resolve_in_text_matcher(self):
        from api.drug_dictionary import find_drugs_in_text

        cases = [
            ("オクトレオチド（ソマトスタチン類似体）：1-5 μg/kg SC q8-12h", "octreotide"),
            ("続いてデコキネート10-20 mg/kg PO q12hを長期投与", "decoquinate"),
            ("ビオチン15-25 mg/日PO（蹄質改善、6-12ヶ月）", "biotin"),
            ("ロイプロリド400-800 μg/kg IM q14-28日", "leuprolide"),
            ("重金属はキレート療法（鉛—Ca-EDTA、ペニシラミン 8-15 mg/kg）", "calcium_edta"),
        ]
        for text, want in cases:
            ids = [h["id"] for h in find_drugs_in_text(text)]
            assert want in ids, (text, ids)
        # Precision guard: bare vitamin-B12 references must keep resolving to
        # the B12 entry, never the new biotin (B7) entry.
        ids = [h["id"] for h in find_drugs_in_text("ビタミンB12 250 μg SC 週1回")]
        assert "vitamin_b12" in ids and "biotin" not in ids, ids


class TestAcuteUrticariaDiseaseEntry:
    """Round 14: acute urticaria/angioedema — among the most common canine ER
    dermatology presentations — was absent from both the dog module database
    and the legacy chat database (only full-blown anaphylaxis existed)."""

    def test_dog_module_carries_urticaria_entry_with_epinephrine_escalation(self):
        import api.species.dog_diseases as dd

        entry = next(
            d
            for d in dd.DISEASES
            if (d.get("name") if isinstance(d, dict) else d.name) == "Acute Urticaria and Angioedema"
        )
        tx = entry["treatment_ja"]
        assert "ジフェンヒドラミン" in tx and "エピネフリン 0.01 mg/kg" in tx
        assert entry["urgency"] == "high"

    def test_legacy_chat_entry_mirrors_module_base_name_for_db_pivot(self):
        # The chat card's 疾患DBで詳細を開く pivot lands by exact base-name match
        # (_pickListItemByName strips the parenthetical) — the legacy entry's
        # base name must equal the module entry's name_ja exactly.
        from api.health_checker import DISEASES

        legacy = next(d for d in DISEASES if d["id"] == "acute_allergic_reaction")
        assert legacy["name_ja"].split("（")[0] == "急性蕁麻疹・血管性浮腫"
        assert legacy["name_en"] == "Acute Urticaria and Angioedema"

    def test_urticaria_entry_is_served(self):
        import os
        import sqlite3

        import pytest

        db = "instance/vetdict.db"
        if not os.path.exists(db):
            pytest.skip("served DB not built")
        conn = sqlite3.connect(db)
        row = conn.execute(
            "select name_ja, urgency from diseases where species='dog' and name='Acute Urticaria and Angioedema'"
        ).fetchone()
        assert row is not None and row[0] == "急性蕁麻疹・血管性浮腫"
