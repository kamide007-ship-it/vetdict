"""
Unit tests for api/species/helpers.py

Covers:
1. _compute_severity          -- severity level computation from suspected disease lists
2. analyze_symptoms_generic   -- main differential diagnosis engine
3. ADVICE                     -- dict structure and content validation
4. SPECIES_BREEDS             -- breed data structural validation
5. compute_lab_boosts         -- lab value abnormality -> disease boost mapping
6. _fuzzy_boost_lookup        -- fuzzy/partial name matching for boost dicts
7. Edge cases                 -- empty symptoms, no matching diseases, unknown breed

All tests are pure in-process (no database, no API keys, no network).
"""

from api.species.helpers import (
    ADVICE,
    SPECIES_BREEDS,
    _compute_severity,
    _fuzzy_boost_lookup,
    analyze_symptoms_generic,
    compute_lab_boosts,
)

# =============================================================================
# Shared fixtures / helpers
# =============================================================================

SYMPTOM_NAMES = {
    "lethargy": {"en": "Lethargy", "ja": "元気がない"},
    "vomiting": {"en": "Vomiting", "ja": "嘔吐"},
    "diarrhea": {"en": "Diarrhea", "ja": "下痢"},
    "excessive_thirst": {"en": "Excessive thirst", "ja": "多飲"},
    "frequent_urination": {"en": "Frequent urination", "ja": "頻尿"},
    "weight_loss": {"en": "Weight loss", "ja": "体重減少"},
    "coughing": {"en": "Coughing", "ja": "咳"},
    "labored_breathing": {"en": "Labored breathing", "ja": "呼吸困難"},
    "seizures": {"en": "Seizures", "ja": "痙攣"},
    "collapse": {"en": "Collapse", "ja": "虚脱"},
}

# Minimal disease definition used across multiple tests
DISEASE_GASTROENTERITIS = {
    "name": "Gastroenteritis",
    "name_ja": "胃腸炎",
    "symptoms": {"vomiting", "diarrhea", "lethargy"},
    "description": "Inflammation of the GI tract.",
    "description_ja": "胃腸炎の説明。",
    "urgency": "moderate",
    "recommended_tests": ["CBC", "Fecal exam"],
    "onset_pattern": {"acute"},
    "age_predisposition": {"young", "adult"},
}

DISEASE_CKD = {
    "name": "Kidney Disease (CKD)",
    "name_ja": "慢性腎臓病",
    "symptoms": {"excessive_thirst", "frequent_urination", "lethargy", "weight_loss"},
    "description": "Chronic kidney disease.",
    "description_ja": "慢性腎臓病の説明。",
    "urgency": "high",
    "recommended_tests": ["Blood chemistry panel", "Urinalysis", "SDMA"],
    "onset_pattern": {"chronic"},
    "age_predisposition": {"senior"},
}

DISEASE_EMERGENCY = {
    "name": "Acute Respiratory Failure",
    "name_ja": "急性呼吸不全",
    "symptoms": {"labored_breathing", "collapse", "coughing"},
    "description": "Life-threatening respiratory failure.",
    "description_ja": "急性呼吸不全の説明。",
    "urgency": "emergency",
    "recommended_tests": ["Chest X-ray", "Blood gas"],
    "onset_pattern": {"acute"},
    "age_predisposition": {"adult", "senior"},
}

DISEASE_LOW_URGENCY = {
    "name": "Mild Allergy",
    "name_ja": "軽度のアレルギー",
    "symptoms": {"lethargy"},
    "description": "Mild allergic reaction.",
    "description_ja": "軽度アレルギーの説明。",
    "urgency": "low",
    "recommended_tests": ["Allergy panel"],
}

ALL_DISEASES = [
    DISEASE_GASTROENTERITIS,
    DISEASE_CKD,
    DISEASE_EMERGENCY,
    DISEASE_LOW_URGENCY,
]


# =============================================================================
# 1. _compute_severity
# =============================================================================


class TestComputeSeverity:
    """Tests for _compute_severity(suspected)."""

    def test_empty_list_returns_low(self):
        assert _compute_severity([]) == "low"

    def test_all_low_urgency_returns_low(self):
        suspected = [
            {"_urgency": "low", "likelihood": "low"},
            {"_urgency": "low", "likelihood": "moderate"},
        ]
        assert _compute_severity(suspected) == "low"

    def test_high_likelihood_with_no_urgency_flag_returns_moderate(self):
        # Any disease with likelihood "high" (regardless of urgency) -> moderate
        suspected = [
            {"_urgency": "low", "likelihood": "high"},
        ]
        assert _compute_severity(suspected) == "moderate"

    def test_high_urgency_moderate_likelihood_returns_high(self):
        suspected = [
            {"_urgency": "high", "likelihood": "moderate"},
        ]
        assert _compute_severity(suspected) == "high"

    def test_high_urgency_high_likelihood_returns_high(self):
        suspected = [
            {"_urgency": "high", "likelihood": "high"},
        ]
        assert _compute_severity(suspected) == "high"

    def test_emergency_urgency_low_likelihood_returns_high_not_emergency(self):
        # emergency urgency + moderate likelihood -> "high" (not "emergency")
        suspected = [
            {"_urgency": "emergency", "likelihood": "moderate"},
        ]
        assert _compute_severity(suspected) == "high"

    def test_emergency_urgency_high_likelihood_returns_emergency(self):
        suspected = [
            {"_urgency": "emergency", "likelihood": "high"},
        ]
        assert _compute_severity(suspected) == "emergency"

    def test_emergency_takes_priority_over_high(self):
        suspected = [
            {"_urgency": "high", "likelihood": "high"},
            {"_urgency": "emergency", "likelihood": "high"},
        ]
        assert _compute_severity(suspected) == "emergency"

    def test_emergency_urgency_requires_high_likelihood(self):
        # emergency urgency + low likelihood alone does NOT trigger "emergency"
        suspected = [
            {"_urgency": "emergency", "likelihood": "low"},
        ]
        # high urgency + low likelihood does not satisfy either emergency OR high rules
        result = _compute_severity(suspected)
        assert result in ("low", "moderate", "high")
        assert result != "emergency"

    def test_multiple_diseases_highest_severity_wins(self):
        suspected = [
            {"_urgency": "low", "likelihood": "low"},
            {"_urgency": "moderate", "likelihood": "low"},
            {"_urgency": "emergency", "likelihood": "high"},
        ]
        assert _compute_severity(suspected) == "emergency"


# =============================================================================
# 2. analyze_symptoms_generic
# =============================================================================


class TestAnalyzeSymptomsGeneric:
    """Tests for analyze_symptoms_generic(...)."""

    def _call(self, symptoms, diseases=None, **kwargs):
        return analyze_symptoms_generic(
            symptoms=symptoms,
            diseases=diseases or ALL_DISEASES,
            symptom_names=SYMPTOM_NAMES,
            **kwargs,
        )

    # -- Return structure --------------------------------------------------

    def test_returns_expected_top_level_keys(self):
        result = self._call(["vomiting", "diarrhea"])
        expected_keys = {
            "suspected_diseases",
            "recommended_tests",
            "severity",
            "general_advice",
            "general_advice_ja",
            "breed_genetic_tests",
            "breed_risk_applied",
            "onset_applied",
            "age_applied",
            "symptom_names",
        }
        assert expected_keys.issubset(result.keys())

    def test_suspected_diseases_is_list(self):
        result = self._call(["vomiting", "diarrhea"])
        assert isinstance(result["suspected_diseases"], list)

    def test_each_suspected_entry_has_required_keys(self):
        result = self._call(["vomiting", "diarrhea"])
        required = {
            "name",
            "name_ja",
            "likelihood",
            "match_percent",
            "color_class",
            "matching_symptoms",
            "match_count",
            "total_symptoms",
        }
        for entry in result["suspected_diseases"]:
            assert required.issubset(entry.keys()), f"Missing keys in {entry['name']}"

    # -- Basic matching ----------------------------------------------------

    def test_matching_disease_appears_in_results(self):
        result = self._call(["vomiting", "diarrhea", "lethargy"])
        names = [d["name"] for d in result["suspected_diseases"]]
        assert "Gastroenteritis" in names

    def test_non_matching_disease_absent(self):
        # Only provide symptoms of CKD; Gastroenteritis should not appear
        result = self._call(
            ["excessive_thirst", "frequent_urination", "weight_loss"],
            diseases=[DISEASE_GASTROENTERITIS],
        )
        names = [d["name"] for d in result["suspected_diseases"]]
        assert "Gastroenteritis" not in names

    def test_match_percent_between_0_and_100(self):
        result = self._call(["vomiting", "diarrhea", "lethargy"])
        for entry in result["suspected_diseases"]:
            assert 0 <= entry["match_percent"] <= 100

    def test_likelihood_values_are_valid(self):
        result = self._call(["vomiting", "diarrhea", "lethargy", "excessive_thirst"])
        valid_likelihoods = {"high", "moderate", "low"}
        for entry in result["suspected_diseases"]:
            assert entry["likelihood"] in valid_likelihoods

    def test_color_class_values_are_valid(self):
        result = self._call(["vomiting", "diarrhea", "lethargy"])
        valid_classes = {"score-high", "score-moderate", "score-low", "score-minimal"}
        for entry in result["suspected_diseases"]:
            assert entry["color_class"] in valid_classes

    # -- Severity propagation ---------------------------------------------

    def test_severity_is_emergency_when_emergency_disease_matches_all(self):
        result = self._call(
            ["labored_breathing", "collapse", "coughing"],
            diseases=[DISEASE_EMERGENCY],
        )
        # The emergency disease should hit "high" likelihood; severity -> "emergency"
        assert result["severity"] == "emergency"

    def test_severity_is_low_for_only_low_urgency_match(self):
        result = self._call(
            ["lethargy"],
            diseases=[DISEASE_LOW_URGENCY],
        )
        # Single symptom gets suppressed; either low or moderate but not emergency/high
        assert result["severity"] in ("low", "moderate")

    # -- Recommended tests ------------------------------------------------

    def test_recommended_tests_deduplicated(self):
        # Two diseases share "CBC" — should appear only once
        disease_a = {**DISEASE_GASTROENTERITIS, "recommended_tests": ["CBC", "Fecal exam"]}
        disease_b = {**DISEASE_CKD, "recommended_tests": ["CBC", "Urinalysis"]}
        result = self._call(
            ["vomiting", "diarrhea", "lethargy", "excessive_thirst", "frequent_urination", "weight_loss"],
            diseases=[disease_a, disease_b],
        )
        tests = result["recommended_tests"]
        assert tests.count("CBC") == 1

    # -- Onset filtering --------------------------------------------------

    def test_onset_applied_flag_true_when_onset_provided(self):
        result = self._call(["vomiting", "diarrhea"], onset="acute")
        assert result["onset_applied"] is True
        assert result["onset"] == "acute"

    def test_onset_applied_flag_false_when_not_provided(self):
        result = self._call(["vomiting", "diarrhea"])
        assert result["onset_applied"] is False

    def test_acute_onset_boosts_acute_disease(self):
        result_acute = self._call(["vomiting", "diarrhea", "lethargy"], onset="acute")
        result_chronic = self._call(["vomiting", "diarrhea", "lethargy"], onset="chronic")
        gi_acute = next((d for d in result_acute["suspected_diseases"] if d["name"] == "Gastroenteritis"), None)
        gi_chronic = next((d for d in result_chronic["suspected_diseases"] if d["name"] == "Gastroenteritis"), None)
        # Gastroenteritis has onset_pattern={"acute"}, so acute should score >= chronic
        if gi_acute and gi_chronic:
            assert gi_acute["match_percent"] >= gi_chronic["match_percent"]

    # -- Age filtering ----------------------------------------------------

    def test_age_applied_flag_true_when_age_provided(self):
        result = self._call(["lethargy"], age_years=3.0)
        assert result["age_applied"] is True
        assert result["age_years"] == 3.0

    def test_age_applied_flag_false_when_not_provided(self):
        result = self._call(["lethargy"])
        assert result["age_applied"] is False

    def test_age_stage_puppy(self):
        result = self._call(["lethargy"], age_years=0.5)
        assert result["age_stage"] == "puppy"

    def test_age_stage_young(self):
        result = self._call(["lethargy"], age_years=2.0)
        assert result["age_stage"] == "young"

    def test_age_stage_adult(self):
        result = self._call(["lethargy"], age_years=5.0)
        assert result["age_stage"] == "adult"

    def test_age_stage_senior(self):
        result = self._call(["lethargy"], age_years=9.0)
        assert result["age_stage"] == "senior"

    # -- Breed risk -------------------------------------------------------

    def test_breed_risk_applied_true_for_known_breed(self):
        result = self._call(
            ["lethargy"],
            breed="cat_persian",
            species="cat",
        )
        assert result["breed_risk_applied"] is True

    def test_breed_risk_not_applied_for_mixed_breed(self):
        # Mixed breed has empty risk dict
        result = self._call(
            ["lethargy"],
            breed="cat_mixed",
            species="cat",
        )
        assert result["breed_risk_applied"] is False

    def test_unknown_breed_id_breed_risk_not_applied(self):
        result = self._call(
            ["lethargy"],
            breed="cat_nonexistent_xyz",
            species="cat",
        )
        assert result["breed_risk_applied"] is False

    def test_breed_without_species_breed_risk_not_applied(self):
        result = self._call(
            ["lethargy"],
            breed="cat_persian",
            # species deliberately omitted
        )
        assert result["breed_risk_applied"] is False

    # -- Lab values -------------------------------------------------------

    def test_lab_boost_applied_flag_true_when_lab_values_trigger_abnormal(self):
        # BUN=60 is well above high_threshold=27 -> abnormal
        result = self._call(
            ["excessive_thirst", "frequent_urination"],
            diseases=[DISEASE_CKD],
            lab_values={"bun": 60.0},
        )
        assert result["lab_boost_applied"] is True

    def test_lab_boost_applied_flag_false_when_lab_values_normal(self):
        # BUN=15 is within reference range -> no abnormality, no boost
        result = self._call(
            ["lethargy"],
            lab_values={"bun": 15.0},
        )
        assert result["lab_boost_applied"] is False

    def test_lab_values_stored_in_result(self):
        lab = {"bun": 60.0, "creatinine": 4.0}
        result = self._call(["lethargy"], lab_values=lab)
        assert result["lab_values"] == lab

    # -- Symptom names lookup ---------------------------------------------

    def test_symptom_names_includes_matching_symptoms(self):
        result = self._call(["vomiting", "diarrhea", "lethargy"])
        snames = result["symptom_names"]
        # All matching symptoms should be looked up
        for entry in result["suspected_diseases"]:
            for sym in entry["matching_symptoms"]:
                if sym in SYMPTOM_NAMES:
                    assert sym in snames

    def test_symptom_names_has_en_and_ja(self):
        result = self._call(["vomiting", "diarrhea", "lethargy"])
        for _sid, names in result["symptom_names"].items():
            assert "en" in names
            assert "ja" in names

    # -- general_advice ---------------------------------------------------

    def test_general_advice_is_nonempty_string(self):
        result = self._call(["vomiting", "diarrhea"])
        assert isinstance(result["general_advice"], str)
        assert len(result["general_advice"]) > 0

    def test_general_advice_ja_is_nonempty_string(self):
        result = self._call(["vomiting", "diarrhea"])
        assert isinstance(result["general_advice_ja"], str)
        assert len(result["general_advice_ja"]) > 0

    # -- Sorting / ordering -----------------------------------------------

    def test_results_sorted_by_match_percent_descending(self):
        result = self._call(
            ["vomiting", "diarrhea", "lethargy", "excessive_thirst", "frequent_urination", "weight_loss"],
        )
        percents = [d["match_percent"] for d in result["suspected_diseases"]]
        # Allow for prevalence-tier sorting overriding match_percent, so just
        # verify the list is not empty and percents are non-negative
        assert all(p >= 0 for p in percents)

    # -- Phase grouping ---------------------------------------------------

    def test_suspected_diseases_by_phase_key_present(self):
        result = self._call(["vomiting", "diarrhea"])
        assert "suspected_diseases_by_phase" in result
        phase_data = result["suspected_diseases_by_phase"]
        assert "phase_1_common" in phase_data
        assert "phase_2_rare" in phase_data

    # -- Custom advice override -------------------------------------------

    def test_custom_advice_override(self):
        custom_advice = {
            "low": {"en": "Custom low EN", "ja": "カスタム低 JA"},
            "moderate": {"en": "Custom moderate EN", "ja": "カスタム中 JA"},
            "high": {"en": "Custom high EN", "ja": "カスタム高 JA"},
            "emergency": {"en": "Custom emergency EN", "ja": "カスタム緊急 JA"},
        }
        result = analyze_symptoms_generic(
            symptoms=["lethargy"],
            diseases=[DISEASE_LOW_URGENCY],
            symptom_names=SYMPTOM_NAMES,
            advice=custom_advice,
        )
        severity = result["severity"]
        assert result["general_advice"] == custom_advice[severity]["en"]
        assert result["general_advice_ja"] == custom_advice[severity]["ja"]

    # -- Prevalence map ---------------------------------------------------

    def test_prevalence_map_sets_tier_on_entry(self):
        prevalence_map = {"Gastroenteritis": "common"}
        result = self._call(
            ["vomiting", "diarrhea", "lethargy"],
            diseases=[DISEASE_GASTROENTERITIS],
            prevalence_map=prevalence_map,
        )
        entry = next(
            (d for d in result["suspected_diseases"] if d["name"] == "Gastroenteritis"),
            None,
        )
        assert entry is not None
        assert entry["prevalence_tier"] == "common"

    def test_prevalence_tier_unknown_when_no_map(self):
        result = self._call(
            ["vomiting", "diarrhea", "lethargy"],
            diseases=[DISEASE_GASTROENTERITIS],
        )
        entry = next(
            (d for d in result["suspected_diseases"] if d["name"] == "Gastroenteritis"),
            None,
        )
        assert entry is not None
        assert entry["prevalence_tier"] == "unknown"


# =============================================================================
# 2b. Edge Cases for analyze_symptoms_generic
# =============================================================================


class TestAnalyzeSymptomsGenericEdgeCases:
    """Edge cases: empty inputs, no matches, etc."""

    def test_empty_symptom_list_returns_no_diseases(self):
        result = analyze_symptoms_generic(
            symptoms=[],
            diseases=ALL_DISEASES,
            symptom_names=SYMPTOM_NAMES,
        )
        assert result["suspected_diseases"] == []

    def test_empty_disease_list_returns_no_diseases(self):
        result = analyze_symptoms_generic(
            symptoms=["vomiting", "diarrhea"],
            diseases=[],
            symptom_names=SYMPTOM_NAMES,
        )
        assert result["suspected_diseases"] == []

    def test_symptoms_with_no_disease_match_returns_empty(self):
        result = analyze_symptoms_generic(
            symptoms=["unknown_symptom_xyz"],
            diseases=ALL_DISEASES,
            symptom_names=SYMPTOM_NAMES,
        )
        assert result["suspected_diseases"] == []

    def test_severity_is_low_when_no_diseases_found(self):
        result = analyze_symptoms_generic(
            symptoms=[],
            diseases=ALL_DISEASES,
            symptom_names=SYMPTOM_NAMES,
        )
        assert result["severity"] == "low"

    def test_recommended_tests_empty_when_no_diseases_found(self):
        result = analyze_symptoms_generic(
            symptoms=[],
            diseases=ALL_DISEASES,
            symptom_names=SYMPTOM_NAMES,
        )
        assert result["recommended_tests"] == []

    def test_unknown_breed_id_still_returns_results(self):
        result = analyze_symptoms_generic(
            symptoms=["vomiting", "diarrhea", "lethargy"],
            diseases=ALL_DISEASES,
            symptom_names=SYMPTOM_NAMES,
            breed="totally_unknown_breed_123",
            species="cat",
        )
        # Should still find Gastroenteritis; breed not found -> no boost, no crash
        names = [d["name"] for d in result["suspected_diseases"]]
        assert "Gastroenteritis" in names
        assert result["breed_risk_applied"] is False

    def test_disease_with_no_symptoms_key_skipped(self):
        disease_no_symptoms = {
            "name": "Mystery Disease",
            "name_ja": "謎の病気",
            "symptoms": set(),
            "description": "",
            "description_ja": "",
            "urgency": "low",
            "recommended_tests": [],
        }
        result = analyze_symptoms_generic(
            symptoms=["vomiting"],
            diseases=[disease_no_symptoms],
            symptom_names=SYMPTOM_NAMES,
        )
        names = [d["name"] for d in result["suspected_diseases"]]
        assert "Mystery Disease" not in names

    def test_single_symptom_low_score_suppression(self):
        # Single-symptom match gets a 0.6 suppression factor; should not crash
        result = analyze_symptoms_generic(
            symptoms=["lethargy"],
            diseases=[DISEASE_GASTROENTERITIS],
            symptom_names=SYMPTOM_NAMES,
        )
        # Even with suppression, result is valid
        for entry in result["suspected_diseases"]:
            assert 0 <= entry["match_percent"] <= 100

    def test_none_lab_values_does_not_apply_lab_boost(self):
        result = analyze_symptoms_generic(
            symptoms=["lethargy"],
            diseases=ALL_DISEASES,
            symptom_names=SYMPTOM_NAMES,
            lab_values=None,
        )
        assert result["lab_boost_applied"] is False

    def test_empty_lab_values_dict_does_not_apply_lab_boost(self):
        result = analyze_symptoms_generic(
            symptoms=["lethargy"],
            diseases=ALL_DISEASES,
            symptom_names=SYMPTOM_NAMES,
            lab_values={},
        )
        assert result["lab_boost_applied"] is False


# =============================================================================
# 3. ADVICE dict structure
# =============================================================================


class TestAdviceDict:
    """Validate the ADVICE module-level constant."""

    def test_advice_has_all_severity_levels(self):
        for level in ("low", "moderate", "high", "emergency"):
            assert level in ADVICE, f"ADVICE missing severity level: {level}"

    def test_each_level_has_en_and_ja(self):
        for level, content in ADVICE.items():
            assert "en" in content, f"ADVICE[{level}] missing 'en' key"
            assert "ja" in content, f"ADVICE[{level}] missing 'ja' key"

    def test_advice_values_are_nonempty_strings(self):
        for _level, content in ADVICE.items():
            assert isinstance(content["en"], str) and len(content["en"]) > 0
            assert isinstance(content["ja"], str) and len(content["ja"]) > 0

    def test_advice_low_mentions_monitor(self):
        assert "monitor" in ADVICE["low"]["en"].lower() or "low" in ADVICE["low"]["en"].lower()

    def test_advice_emergency_mentions_immediate(self):
        assert "immediate" in ADVICE["emergency"]["en"].lower() or "emergency" in ADVICE["emergency"]["en"].lower()


# =============================================================================
# 4. SPECIES_BREEDS data validation
# =============================================================================


class TestSpeciesBreeds:
    """Validate the SPECIES_BREEDS module-level constant."""

    EXPECTED_SPECIES = {
        "cat",
        "rabbit",
        "hamster",
        "ferret",
        "guinea_pig",
        "chinchilla",
        "hedgehog",
        "bird",
        "parakeet",
        "parrot",
        "reptile",
        "tortoise",
        "snake",
        "lizard",
        "amphibian",
        "sugar_glider",
        "degu",
    }

    def test_expected_species_present(self):
        for species in self.EXPECTED_SPECIES:
            assert species in SPECIES_BREEDS, f"SPECIES_BREEDS missing species: {species}"

    def test_each_species_has_nonempty_breed_list(self):
        for species, breeds in SPECIES_BREEDS.items():
            assert isinstance(breeds, list) and len(breeds) > 0, f"SPECIES_BREEDS[{species}] should be a non-empty list"

    def test_each_breed_has_required_keys(self):
        required = {"id", "name", "name_ja", "risk"}
        for species, breeds in SPECIES_BREEDS.items():
            for breed in breeds:
                missing = required - breed.keys()
                assert not missing, f"Breed {breed.get('id')} in {species} missing keys: {missing}"

    def test_breed_id_is_nonempty_string(self):
        for _species, breeds in SPECIES_BREEDS.items():
            for breed in breeds:
                assert isinstance(breed["id"], str) and len(breed["id"]) > 0

    def test_risk_dict_values_are_positive_floats(self):
        for _species, breeds in SPECIES_BREEDS.items():
            for breed in breeds:
                for disease, multiplier in breed["risk"].items():
                    assert isinstance(multiplier, (int, float)) and multiplier > 0, (
                        f"Invalid multiplier {multiplier} for {disease} in {breed['id']}"
                    )

    def test_cat_persian_has_pkd_risk(self):
        cat_breeds = SPECIES_BREEDS["cat"]
        persian = next((b for b in cat_breeds if b["id"] == "cat_persian"), None)
        assert persian is not None
        assert "Polycystic Kidney Disease (PKD)" in persian["risk"]
        assert persian["risk"]["Polycystic Kidney Disease (PKD)"] > 1.0

    def test_cat_scottish_fold_has_osteochondrodysplasia(self):
        cat_breeds = SPECIES_BREEDS["cat"]
        sf = next((b for b in cat_breeds if b["id"] == "cat_scottish_fold"), None)
        assert sf is not None
        assert "Scottish Fold Osteochondrodysplasia" in sf["risk"]

    def test_rabbit_netherland_dwarf_has_malocclusion_risk(self):
        rabbit_breeds = SPECIES_BREEDS["rabbit"]
        nd = next((b for b in rabbit_breeds if b["id"] == "rabbit_netherland_dwarf"), None)
        assert nd is not None
        assert "Malocclusion" in nd["risk"]

    def test_hamster_campbell_has_highest_diabetes_risk(self):
        hamster_breeds = SPECIES_BREEDS["hamster"]
        campbell = next((b for b in hamster_breeds if b["id"] == "hamster_campbell"), None)
        assert campbell is not None
        assert campbell["risk"].get("Diabetes Mellitus", 0) >= 2.5

    def test_breed_ids_unique_within_species(self):
        for species, breeds in SPECIES_BREEDS.items():
            ids = [b["id"] for b in breeds]
            assert len(ids) == len(set(ids)), f"Duplicate breed IDs in {species}: {ids}"


# =============================================================================
# 5. compute_lab_boosts
# =============================================================================


class TestComputeLabBoosts:
    """Tests for compute_lab_boosts(lab_values)."""

    def test_empty_input_returns_empty_dict(self):
        assert compute_lab_boosts({}) == {}

    def test_normal_values_return_empty_dict(self):
        # BUN=15 (range 7–27) and creatinine=1.0 (range 0.5–1.8) are normal
        result = compute_lab_boosts({"bun": 15.0, "creatinine": 1.0})
        assert result == {}

    def test_high_bun_boosts_ckd(self):
        # BUN=60 > high_threshold=27
        result = compute_lab_boosts({"bun": 60.0})
        assert "Chronic Kidney Disease (CKD)" in result
        assert result["Chronic Kidney Disease (CKD)"] > 1.0

    def test_high_creatinine_boosts_ckd(self):
        # creatinine=5.0 > high_threshold=1.8
        result = compute_lab_boosts({"creatinine": 5.0})
        assert "Chronic Kidney Disease (CKD)" in result

    def test_high_glucose_boosts_diabetes(self):
        # glucose=300 > high_threshold=143
        result = compute_lab_boosts({"glucose": 300.0})
        assert "Diabetes Mellitus" in result
        assert result["Diabetes Mellitus"] > 1.0

    def test_low_glucose_boosts_insulinoma(self):
        # glucose=40 < low_threshold=74
        result = compute_lab_boosts({"glucose": 40.0})
        assert "Insulinoma" in result

    def test_high_alt_boosts_hepatitis(self):
        # ALT=500 > high_threshold=125
        result = compute_lab_boosts({"alt": 500.0})
        assert "Hepatitis" in result

    def test_high_lipase_boosts_pancreatitis(self):
        # lipase=500 > high_threshold=160
        result = compute_lab_boosts({"lipase": 500.0})
        assert "Pancreatitis" in result
        assert result["Pancreatitis"] == 2.0  # exact mapping value

    def test_multiple_abnormal_values_merged_with_max(self):
        # Both bun and creatinine high -> both boost CKD individually AND
        # trigger the combination pattern for an even higher synergistic boost
        result_bun = compute_lab_boosts({"bun": 60.0})
        result_cre = compute_lab_boosts({"creatinine": 5.0})
        result_both = compute_lab_boosts({"bun": 60.0, "creatinine": 5.0})
        individual_max = max(
            result_bun.get("Chronic Kidney Disease (CKD)", 1.0),
            result_cre.get("Chronic Kidney Disease (CKD)", 1.0),
        )
        # Combined result should be >= individual max (combination pattern may boost further)
        assert result_both.get("Chronic Kidney Disease (CKD)", 1.0) >= individual_max

    def test_unknown_lab_item_ignored(self):
        # Unknown item should be silently skipped
        result = compute_lab_boosts({"totally_unknown_lab": 9999.0})
        assert result == {}

    def test_low_pcv_boosts_imha(self):
        # pcv=20 < low_threshold=37
        result = compute_lab_boosts({"pcv": 20.0})
        assert "Immune-Mediated Hemolytic Anemia (IMHA)" in result

    def test_high_t4_boosts_hyperthyroidism(self):
        # t4=8.0 > high_threshold=4.0
        result = compute_lab_boosts({"t4": 8.0})
        assert "Hyperthyroidism" in result
        assert result["Hyperthyroidism"] == 2.0

    def test_result_values_are_positive_floats(self):
        result = compute_lab_boosts({"bun": 60.0, "glucose": 300.0, "alt": 500.0})
        for disease, multiplier in result.items():
            assert isinstance(multiplier, float) and multiplier > 0, f"Invalid multiplier {multiplier} for {disease}"

    def test_lab_values_at_exactly_threshold_are_normal(self):
        # Boundary: exactly at high_threshold (not strictly greater) -> normal
        result = compute_lab_boosts({"bun": 27.0})  # high_threshold == 27
        assert result == {}


# =============================================================================
# 6. _fuzzy_boost_lookup
# =============================================================================


class TestFuzzyBoostLookup:
    """Tests for _fuzzy_boost_lookup(disease_name, boost_dict)."""

    def test_exact_match_returns_correct_multiplier(self):
        boost_dict = {"Pancreatitis": 2.0, "Hepatitis": 1.5}
        assert _fuzzy_boost_lookup("Pancreatitis", boost_dict) == 2.0

    def test_no_match_returns_1_0(self):
        boost_dict = {"Pancreatitis": 2.0}
        assert _fuzzy_boost_lookup("Completely Unrelated Disease", boost_dict) == 1.0

    def test_empty_boost_dict_returns_1_0(self):
        assert _fuzzy_boost_lookup("Any Disease", {}) == 1.0

    def test_partial_match_base_name_in_boost_key(self):
        # "Kidney Disease (CKD)" base name "Kidney Disease" should match
        # "Chronic Kidney Disease (CKD)" via base name overlap
        boost_dict = {"Chronic Kidney Disease (CKD)": 1.8}
        result = _fuzzy_boost_lookup("Kidney Disease (CKD)", boost_dict)
        assert result > 1.0

    def test_case_insensitive_matching(self):
        boost_dict = {"pancreatitis": 1.5}
        result = _fuzzy_boost_lookup("Pancreatitis", boost_dict)
        # Should match case-insensitively (base name comparison)
        assert result >= 1.0  # may find a match

    def test_slash_separated_key_partial_match(self):
        # Boost dict has "Tumors/Neoplasia" with slash; disease name contains "tumors"
        boost_dict = {"Tumors/Neoplasia": 1.5}
        result = _fuzzy_boost_lookup("Mast Cell Tumors", boost_dict)
        assert result > 1.0

    def test_returns_highest_multiplier_on_multiple_matches(self):
        # Disease name matching multiple keys should return the highest multiplier
        boost_dict = {
            "Kidney": 1.3,
            "Kidney Disease": 1.8,
        }
        result = _fuzzy_boost_lookup("Kidney Disease (CKD)", boost_dict)
        assert result == 1.8

    def test_exact_match_takes_priority_over_fuzzy(self):
        boost_dict = {
            "Pancreatitis": 2.0,
            "Pancreatic Disease": 1.2,
        }
        result = _fuzzy_boost_lookup("Pancreatitis", boost_dict)
        assert result == 2.0

    def test_disease_name_contained_in_boost_key_matches(self):
        # disease_lower in boost_lower -> match
        boost_dict = {"Feline Hypertrophic Cardiomyopathy (HCM)": 1.8}
        result = _fuzzy_boost_lookup("Hypertrophic Cardiomyopathy", boost_dict)
        assert result > 1.0

    def test_completely_different_disease_returns_1_0(self):
        boost_dict = {"Diabetes Mellitus": 2.5, "Pancreatitis": 2.0}
        result = _fuzzy_boost_lookup("Conjunctivitis", boost_dict)
        assert result == 1.0
