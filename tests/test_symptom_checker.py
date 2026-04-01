"""
Unit tests for api/symptom_checker.py

Covers:
1. map_health_checks_to_symptoms  -- Japanese health-check -> symptom ID mapping
2. analyze_symptoms               -- main symptom analysis engine
3. _compute_severity              -- severity calculation
4. Data integrity                 -- VALID_SYMPTOMS, _SYMPTOM_NAMES, disease DB,
                                     health-check categories, test DB
5. Edge cases                     -- empty inputs, unknown breed IDs, invalid
                                     symptom IDs, single symptoms, etc.

All tests are pure in-process (no database, no API keys).
"""

import re

from api.symptom_checker import (
    _ADVICE,
    _ANY_LIMPING,
    _BREED_DISEASE_RISK,
    _BREED_GENETIC_TESTS,
    _DISEASE_DB,
    _LIKELIHOOD_TO_PRIORITY,
    _PRIORITY_RANK,
    _SYMPTOM_NAMES,
    _TEST_DB,
    ABNORMAL_KEYWORDS,
    HEALTH_CHECK_CATEGORIES,
    VALID_SYMPTOMS,
    _collect_tests,
    _compute_severity,
    analyze_symptoms,
    map_health_checks_to_symptoms,
)

# ============================================================================
# 1. map_health_checks_to_symptoms
# ============================================================================


class TestMapHealthChecksToSymptoms:
    """Verify the Japanese health-check -> symptom ID mapping function."""

    # -- basic mapping -------------------------------------------------

    def test_single_category_single_item(self):
        result = map_health_checks_to_symptoms({"general": ["元気がない"]})
        assert result == ["lethargy"]

    def test_single_category_multiple_items(self):
        result = map_health_checks_to_symptoms(
            {"digestive": ["嘔吐", "下痢"]}
        )
        assert "vomiting" in result
        assert "diarrhea" in result

    def test_multiple_categories(self):
        result = map_health_checks_to_symptoms({
            "general": ["元気がない"],
            "respiratory": ["咳"],
        })
        assert "lethargy" in result
        assert "coughing" in result

    def test_item_with_multiple_symptom_ids(self):
        """Items like abdominal pain map to multiple symptom IDs."""
        result = map_health_checks_to_symptoms(
            {"digestive": ["腹痛（触ると痛がる）"]}
        )
        assert "bloated_abdomen" in result
        assert "pain_on_touch" in result

    def test_respiratory_nasal_congestion_maps_two_ids(self):
        result = map_health_checks_to_symptoms(
            {"respiratory": ["鼻づまり"]}
        )
        assert "nasal_discharge" in result
        assert "snoring" in result

    def test_skin_eczema_maps_two_ids(self):
        result = map_health_checks_to_symptoms(
            {"skin": ["湿疹"]}
        )
        assert "skin_redness" in result
        assert "itching" in result

    # -- deduplication -------------------------------------------------

    def test_deduplication_within_category(self):
        """Selecting two items that share a symptom ID should not duplicate."""
        result = map_health_checks_to_symptoms(
            {"digestive": ["嘔吐", "吐き気（よだれが多い）"]}
        )
        assert result.count("vomiting") == 1

    def test_deduplication_across_categories(self):
        """lethargy appears in general and neurological; should appear once."""
        result = map_health_checks_to_symptoms({
            "general": ["元気がない"],
            "neurological": ["反応が鈍い"],
        })
        assert result.count("lethargy") == 1

    def test_no_duplicates_in_result(self):
        """Result list should never contain duplicates regardless of input."""
        result = map_health_checks_to_symptoms({
            "digestive": ["嘔吐"],
            "other": ["異物誤飲の疑い"],
        })
        assert len(result) == len(set(result))

    # -- return type / ordering ----------------------------------------

    def test_returns_sorted_list(self):
        result = map_health_checks_to_symptoms({
            "general": ["元気がない", "興奮している"],
            "digestive": ["嘔吐"],
        })
        assert result == sorted(result)

    def test_returns_list_type(self):
        result = map_health_checks_to_symptoms({"general": ["普段通り"]})
        assert isinstance(result, list)

    # -- items with empty symptom_ids ----------------------------------

    def test_normal_status_maps_to_empty(self):
        """Items like 'Normal' have empty symptom_ids lists."""
        result = map_health_checks_to_symptoms({"general": ["普段通り"]})
        assert result == []

    def test_normal_appetite_maps_to_empty(self):
        result = map_health_checks_to_symptoms({"appetite": ["食欲普通"]})
        assert result == []

    def test_normal_drinking_maps_to_empty(self):
        result = map_health_checks_to_symptoms({"appetite": ["飲水普通"]})
        assert result == []

    def test_bleeding_has_no_symptom_ids(self):
        """'出血' (Bleeding) in 'other' has an empty symptom_ids list."""
        result = map_health_checks_to_symptoms({"other": ["出血"]})
        assert result == []

    # -- unknown category / item silently ignored ----------------------

    def test_unknown_category_key_ignored(self):
        result = map_health_checks_to_symptoms({"nonexistent": ["anything"]})
        assert result == []

    def test_unknown_japanese_label_ignored(self):
        result = map_health_checks_to_symptoms(
            {"general": ["存在しないラベル"]}
        )
        assert result == []

    def test_mix_known_and_unknown_labels(self):
        result = map_health_checks_to_symptoms(
            {"general": ["元気がない", "存在しないラベル"]}
        )
        assert result == ["lethargy"]

    # -- edge cases ----------------------------------------------------

    def test_empty_dict(self):
        assert map_health_checks_to_symptoms({}) == []

    def test_empty_item_list(self):
        assert map_health_checks_to_symptoms({"general": []}) == []

    def test_all_empty_item_lists(self):
        checks = {cat: [] for cat in HEALTH_CHECK_CATEGORIES}
        assert map_health_checks_to_symptoms(checks) == []

    # -- every category / item smoke test ------------------------------

    def test_all_category_keys_are_accepted(self):
        """All categories defined in HEALTH_CHECK_CATEGORIES should work."""
        for cat_key, cat_data in HEALTH_CHECK_CATEGORIES.items():
            first_item_ja = cat_data["items"][0]["ja"]
            result = map_health_checks_to_symptoms({cat_key: [first_item_ja]})
            assert isinstance(result, list), f"Failed for category {cat_key}"

    # -- specific category spot checks ---------------------------------

    def test_urinary_frequency(self):
        result = map_health_checks_to_symptoms({"urinary": ["頻尿"]})
        assert result == ["excessive_urination"]

    def test_eyes_ears_eye_discharge(self):
        result = map_health_checks_to_symptoms({"eyes_ears": ["目やに"]})
        assert result == ["eye_discharge"]

    def test_musculoskeletal_limping(self):
        result = map_health_checks_to_symptoms(
            {"musculoskeletal": ["びっこ（片足を引く）"]}
        )
        assert result == ["limping_fl"]

    def test_neurological_seizures(self):
        result = map_health_checks_to_symptoms(
            {"neurological": ["けいれん"]}
        )
        assert result == ["seizures"]

    def test_other_fever(self):
        result = map_health_checks_to_symptoms(
            {"other": ["発熱（体が熱い）"]}
        )
        assert result == ["fever"]


# ============================================================================
# 2. analyze_symptoms -- main analysis engine
# ============================================================================


class TestAnalyzeSymptoms:
    """Test the primary public API: analyze_symptoms()."""

    # -- return structure -----------------------------------------------

    def test_return_keys(self):
        result = analyze_symptoms(["vomiting", "lethargy"])
        expected_keys = {
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
            "pain_score",
        }
        assert set(result.keys()) == expected_keys

    def test_suspected_diseases_is_list(self):
        result = analyze_symptoms(["vomiting"])
        assert isinstance(result["suspected_diseases"], list)

    def test_recommended_tests_is_list(self):
        result = analyze_symptoms(["vomiting"])
        assert isinstance(result["recommended_tests"], list)

    def test_severity_is_valid_string(self):
        result = analyze_symptoms(["vomiting"])
        assert result["severity"] in {"emergency", "high", "moderate", "low"}

    # -- disease matching -----------------------------------------------

    def test_parvovirus_detected(self):
        """Parvovirus symptoms should yield Canine Parvovirus in results."""
        result = analyze_symptoms([
            "vomiting", "bloody_stool", "lethargy", "appetite_loss",
            "fever", "diarrhea",
        ])
        names = [d["name"] for d in result["suspected_diseases"]]
        assert "Canine Parvovirus" in names

    def test_kennel_cough_detected(self):
        result = analyze_symptoms([
            "coughing", "sneezing", "nasal_discharge",
            "reverse_sneezing", "lethargy",
        ])
        names = [d["name"] for d in result["suspected_diseases"]]
        assert "Kennel Cough (Bordetella)" in names

    def test_gdv_detected_with_matching_symptoms(self):
        result = analyze_symptoms([
            "bloated_abdomen", "vomiting", "excessive_panting",
            "lethargy", "anxiety",
        ])
        names = [d["name"] for d in result["suspected_diseases"]]
        assert "Gastric Dilatation-Volvulus (GDV/Bloat)" in names

    def test_hypothyroidism_detected(self):
        result = analyze_symptoms([
            "weight_gain", "lethargy", "hair_loss", "dry_skin",
        ])
        names = [d["name"] for d in result["suspected_diseases"]]
        assert "Hypothyroidism" in names

    # -- disease result entry structure --------------------------------

    def test_disease_entry_fields(self):
        result = analyze_symptoms([
            "vomiting", "bloody_stool", "lethargy", "appetite_loss",
        ])
        for entry in result["suspected_diseases"]:
            assert "name" in entry
            assert "name_ja" in entry
            assert "likelihood" in entry
            assert entry["likelihood"] in {"high", "moderate", "low"}
            assert "match_percent" in entry
            assert isinstance(entry["match_percent"], int)
            assert 0 <= entry["match_percent"] <= 100
            assert "color_class" in entry
            assert "description" in entry
            assert "description_ja" in entry
            assert "pathophysiology" in entry
            assert "pathophysiology_ja" in entry
            assert "causes" in entry
            assert "causes_ja" in entry
            assert "treatment" in entry
            assert "treatment_ja" in entry
            assert "prognosis" in entry
            assert "prognosis_ja" in entry
            assert "prevention" in entry
            assert "prevention_ja" in entry
            assert "matching_symptoms" in entry
            assert isinstance(entry["matching_symptoms"], list)
            assert "match_count" in entry
            assert "total_symptoms" in entry
            assert "clinical_frequency_data" in entry
            assert isinstance(entry["clinical_frequency_data"], dict)

    def test_disease_detail_fields_default_to_strings(self):
        result = analyze_symptoms(["vomiting", "lethargy", "diarrhea"])
        detail_fields = (
            "description",
            "pathophysiology",
            "causes",
            "prevention",
            "treatment",
            "prognosis",
        )
        translated_fields = (
            "description_ja",
            "pathophysiology_ja",
            "causes_ja",
            "prevention_ja",
            "treatment_ja",
            "prognosis_ja",
        )

        for entry in result["suspected_diseases"]:
            for field in detail_fields:
                value = entry.get(field)
                assert value, f"{field} should not be empty for {entry['name']}"
                assert isinstance(value, str)
            for field in translated_fields:
                assert isinstance(entry[field], str)

    def test_internal_fields_removed(self):
        """_urgency and _match_ratio must not appear in output."""
        result = analyze_symptoms(["vomiting", "lethargy", "diarrhea"])
        for entry in result["suspected_diseases"]:
            assert "_urgency" not in entry
            assert "_match_ratio" not in entry

    def test_matching_symptoms_are_sorted(self):
        result = analyze_symptoms([
            "vomiting", "lethargy", "diarrhea", "appetite_loss",
        ])
        for entry in result["suspected_diseases"]:
            assert entry["matching_symptoms"] == sorted(
                entry["matching_symptoms"]
            )

    # -- sorting --------------------------------------------------------

    def test_suspected_diseases_sorted_by_prevalence_then_score(self):
        """Results sorted by match quality tier, then prevalence, then score."""
        result = analyze_symptoms([
            "vomiting", "lethargy", "diarrhea", "appetite_loss", "fever",
        ])
        diseases = result["suspected_diseases"]
        prevalence_priority = {
            "very_common": 0,
            "common": 1,
            "uncommon": 2,
            "rare": 3,
            "unknown": 4,
        }

        def _match_quality_tier(d):
            pct = d["match_percent"]
            cnt = d["match_count"]
            if pct >= 50 or cnt >= 3:
                return 0
            if pct >= 25 or cnt >= 2:
                return 1
            return 2

        for i in range(len(diseases) - 1):
            a, b = diseases[i], diseases[i + 1]
            assert (
                _match_quality_tier(a),
                prevalence_priority.get(a["prevalence_tier"], 5),
                -a["match_percent"],
                -a["match_count"],
            ) <= (
                _match_quality_tier(b),
                prevalence_priority.get(b["prevalence_tier"], 5),
                -b["match_percent"],
                -b["match_count"],
            ), "suspected_diseases not sorted correctly"

    def test_vaccines_exclude_preventable_diseases(self):
        result = analyze_symptoms(
            ["vomiting", "bloody_stool", "lethargy", "appetite_loss", "fever", "diarrhea"],
            vaccines=["core_5in1"],
        )

        names = [d["name"] for d in result["suspected_diseases"]]
        assert "Canine Parvovirus" not in names
        assert result["vaccines_applied"] is True
        assert result["vaccines"] == ["core_5in1"]
        assert "Canine Parvovirus" in result["vaccine_preventable_excluded"]

    def test_vaccines_and_vaccination_status_can_coexist(self):
        symptoms = ["vomiting", "bloody_stool", "lethargy", "appetite_loss", "fever", "diarrhea"]
        status_only = analyze_symptoms(symptoms, vaccination_status="current")
        merged = analyze_symptoms(
            symptoms,
            vaccines=["rabies"],
            vaccination_status="current",
        )

        status_only_parvo = next(
            disease
            for disease in status_only["suspected_diseases"]
            if disease["name"] == "Canine Parvovirus"
        )
        merged_parvo = next(
            disease
            for disease in merged["suspected_diseases"]
            if disease["name"] == "Canine Parvovirus"
        )

        assert merged["vaccines"] == ["rabies"]
        assert merged["vaccination_status"] == "current"
        assert merged["vaccination_adjustment_applied"] is True
        assert merged_parvo["match_percent"] == status_only_parvo["match_percent"]
        assert merged_parvo["vaccination_adjustment_applied"] is True

    # -- color_class assignment -----------------------------------------

    def test_color_class_assignments(self):
        """Verify color_class thresholds across all results."""
        result = analyze_symptoms(list(VALID_SYMPTOMS))
        for d in result["suspected_diseases"]:
            mp = d["match_percent"]
            if mp >= 70:
                assert d["color_class"] == "score-high"
            elif mp >= 45:
                assert d["color_class"] == "score-moderate"
            elif mp >= 25:
                assert d["color_class"] == "score-low"
            else:
                assert d["color_class"] == "score-minimal"

    # -- breed risk applied flag ----------------------------------------

    def test_breed_risk_applied_true(self):
        result = analyze_symptoms(
            ["coughing", "sneezing"], breed="101_french_bulldog"
        )
        assert result["breed_risk_applied"] is True

    def test_breed_risk_applied_false_no_breed(self):
        result = analyze_symptoms(["coughing"])
        assert result["breed_risk_applied"] is False

    def test_breed_risk_applied_false_unknown_breed(self):
        result = analyze_symptoms(
            ["coughing"], breed="999_unknown_breed"
        )
        assert result["breed_risk_applied"] is False

    # -- breed multiplier boosts score ---------------------------------

    def test_breed_multiplier_boosts_score(self):
        """French Bulldog should boost Brachycephalic Airway Syndrome."""
        base = analyze_symptoms(
            ["snoring", "difficulty_breathing", "reverse_sneezing",
             "excessive_panting"]
        )
        boosted = analyze_symptoms(
            ["snoring", "difficulty_breathing", "reverse_sneezing",
             "excessive_panting"],
            breed="101_french_bulldog",
        )
        base_entry = next(
            (d for d in base["suspected_diseases"]
             if d["name"] == "Brachycephalic Airway Syndrome"),
            None,
        )
        boosted_entry = next(
            (d for d in boosted["suspected_diseases"]
             if d["name"] == "Brachycephalic Airway Syndrome"),
            None,
        )
        if base_entry and boosted_entry:
            assert boosted_entry["match_percent"] >= base_entry["match_percent"]

    # -- breed genetic tests -------------------------------------------

    def test_breed_genetic_tests_returned(self):
        result = analyze_symptoms(
            ["coughing"], breed="101_french_bulldog"
        )
        assert len(result["breed_genetic_tests"]) > 0
        for test in result["breed_genetic_tests"]:
            assert "test" in test
            assert "test_ja" in test
            assert "purpose" in test

    def test_breed_genetic_tests_empty_for_unknown_breed(self):
        result = analyze_symptoms(
            ["coughing"], breed="999_unknown_breed"
        )
        assert result["breed_genetic_tests"] == []

    def test_breed_genetic_tests_empty_when_no_breed(self):
        result = analyze_symptoms(["coughing"])
        assert result["breed_genetic_tests"] == []

    # -- symptom_names lookup in result --------------------------------

    def test_symptom_names_populated(self):
        result = analyze_symptoms(["vomiting", "lethargy"])
        for sid, names in result["symptom_names"].items():
            assert sid in VALID_SYMPTOMS
            assert "ja" in names
            assert "en" in names

    def test_symptom_names_only_for_relevant_symptoms(self):
        """symptom_names includes IDs from matching and missing_key symptoms."""
        result = analyze_symptoms(["vomiting", "lethargy"])
        used = set()
        for entry in result["suspected_diseases"]:
            used.update(entry["matching_symptoms"])
            used.update(entry.get("missing_key_symptoms", []))
        assert set(result["symptom_names"].keys()) <= used

    # -- recommended tests structure -----------------------------------

    def test_recommended_test_entry_fields(self):
        result = analyze_symptoms([
            "vomiting", "lethargy", "diarrhea",
        ])
        for test in result["recommended_tests"]:
            assert "name" in test
            assert "name_ja" in test
            assert "purpose" in test
            assert "priority" in test
            assert test["priority"] in {"urgent", "recommended", "optional"}
            assert "related_diseases" in test
            assert isinstance(test["related_diseases"], list)

    def test_recommended_tests_sorted_by_priority_then_name(self):
        result = analyze_symptoms([
            "vomiting", "lethargy", "diarrhea", "appetite_loss",
        ])
        tests = result["recommended_tests"]
        for i in range(len(tests) - 1):
            a_rank = _PRIORITY_RANK[tests[i]["priority"]]
            b_rank = _PRIORITY_RANK[tests[i + 1]["priority"]]
            if a_rank == b_rank:
                assert tests[i]["name"] <= tests[i + 1]["name"]
            else:
                assert a_rank >= b_rank

    # -- general advice ------------------------------------------------

    def test_general_advice_returned(self):
        result = analyze_symptoms(["vomiting"])
        assert isinstance(result["general_advice"], str)
        assert len(result["general_advice"]) > 0
        assert isinstance(result["general_advice_ja"], str)
        assert len(result["general_advice_ja"]) > 0

    # -- invalid / unknown symptom IDs silently ignored -----------------

    def test_unknown_symptoms_ignored(self):
        result = analyze_symptoms(["totally_fake_symptom"])
        assert result["suspected_diseases"] == []

    def test_mix_valid_and_invalid(self):
        """Invalid IDs should be dropped; result same as valid-only."""
        result = analyze_symptoms(["vomiting", "fake_one", "lethargy"])
        result_clean = analyze_symptoms(["vomiting", "lethargy"])
        assert result["suspected_diseases"] == result_clean["suspected_diseases"]

    # -- score capping at 100 -----------------------------------------

    def test_match_percent_never_exceeds_100(self):
        """Even with a breed multiplier, match_percent <= 100."""
        for breed_id in _BREED_DISEASE_RISK:
            result = analyze_symptoms(
                list(VALID_SYMPTOMS), breed=breed_id
            )
            for d in result["suspected_diseases"]:
                assert d["match_percent"] <= 100


# ============================================================================
# 3. _compute_severity
# ============================================================================


class TestComputeSeverity:
    """Test the internal severity calculation helper."""

    def test_returns_low_for_empty_list(self):
        assert _compute_severity([]) == "low"

    def test_returns_low_for_only_low_likelihood(self):
        suspected = [
            {"_urgency": "normal", "likelihood": "low"},
        ]
        assert _compute_severity(suspected) == "low"

    def test_returns_moderate_for_high_likelihood_normal_urgency(self):
        suspected = [
            {"_urgency": "normal", "likelihood": "high"},
        ]
        assert _compute_severity(suspected) == "moderate"

    def test_returns_high_for_urgent_high_likelihood(self):
        suspected = [
            {"_urgency": "urgent", "likelihood": "high"},
        ]
        assert _compute_severity(suspected) == "high"

    def test_returns_high_for_urgent_moderate_likelihood(self):
        suspected = [
            {"_urgency": "urgent", "likelihood": "moderate"},
        ]
        assert _compute_severity(suspected) == "high"

    def test_returns_high_for_high_urgency_moderate_likelihood(self):
        suspected = [
            {"_urgency": "high", "likelihood": "moderate"},
        ]
        assert _compute_severity(suspected) == "high"

    def test_returns_emergency_for_emergency_high_likelihood(self):
        suspected = [
            {"_urgency": "emergency", "likelihood": "high"},
        ]
        assert _compute_severity(suspected) == "emergency"

    def test_emergency_urgency_moderate_likelihood_is_high(self):
        """Emergency disease at moderate likelihood should still trigger high severity."""
        suspected = [
            {"_urgency": "emergency", "likelihood": "moderate"},
        ]
        assert _compute_severity(suspected) == "high"

    def test_emergency_urgency_low_likelihood_is_low(self):
        suspected = [
            {"_urgency": "emergency", "likelihood": "low"},
        ]
        assert _compute_severity(suspected) == "low"

    def test_first_match_wins_emergency_over_high(self):
        """When multiple diseases, emergency should win over high."""
        suspected = [
            {"_urgency": "emergency", "likelihood": "high"},
            {"_urgency": "urgent", "likelihood": "high"},
        ]
        assert _compute_severity(suspected) == "emergency"

    def test_first_match_wins_high_over_moderate(self):
        suspected = [
            {"_urgency": "urgent", "likelihood": "moderate"},
            {"_urgency": "normal", "likelihood": "high"},
        ]
        assert _compute_severity(suspected) == "high"

    def test_mixed_normal_low_and_high(self):
        """Normal low + normal high yields moderate (has_high True)."""
        suspected = [
            {"_urgency": "normal", "likelihood": "low"},
            {"_urgency": "normal", "likelihood": "high"},
        ]
        assert _compute_severity(suspected) == "moderate"

    def test_only_moderate_likelihood_is_low(self):
        """Moderate likelihood with normal urgency gives low."""
        suspected = [
            {"_urgency": "normal", "likelihood": "moderate"},
            {"_urgency": "normal", "likelihood": "moderate"},
        ]
        assert _compute_severity(suspected) == "low"

    def test_multiple_normal_low_is_low(self):
        suspected = [
            {"_urgency": "normal", "likelihood": "low"},
            {"_urgency": "normal", "likelihood": "low"},
            {"_urgency": "normal", "likelihood": "low"},
        ]
        assert _compute_severity(suspected) == "low"

    def test_urgent_low_likelihood_is_low(self):
        """Urgent disease but only low likelihood does not trigger high."""
        suspected = [
            {"_urgency": "urgent", "likelihood": "low"},
        ]
        assert _compute_severity(suspected) == "low"

    # -- integration with analyze_symptoms --------------------------------

    def test_gdv_all_symptoms_triggers_emergency(self):
        """GDV with all symptoms -> high likelihood -> emergency."""
        result = analyze_symptoms([
            "bloated_abdomen", "vomiting", "excessive_panting",
            "lethargy", "anxiety",
        ])
        gdv = next(
            (d for d in result["suspected_diseases"]
             if d["name"] == "Gastric Dilatation-Volvulus (GDV/Bloat)"),
            None,
        )
        assert gdv is not None
        assert gdv["likelihood"] == "high"
        assert result["severity"] == "emergency"

    def test_severity_not_emergency_for_single_benign_symptom(self):
        """A single common symptom should not produce emergency severity."""
        result = analyze_symptoms(["dry_skin"])
        assert result["severity"] in {"low", "moderate"}


# ============================================================================
# 4. _collect_tests
# ============================================================================


class TestCollectTests:
    """Test the recommended diagnostic test collection helper."""

    def test_empty_suspected_returns_empty(self):
        assert _collect_tests([]) == []

    def test_returns_list_of_dicts(self):
        suspected = [{
            "name": "Canine Parvovirus",
            "likelihood": "high",
        }]
        result = _collect_tests(suspected)
        assert isinstance(result, list)
        for entry in result:
            assert isinstance(entry, dict)

    def test_related_diseases_are_sorted(self):
        suspected = [
            {"name": "Canine Parvovirus", "likelihood": "high"},
            {"name": "Pancreatitis", "likelihood": "moderate"},
        ]
        result = _collect_tests(suspected)
        for test in result:
            assert test["related_diseases"] == sorted(test["related_diseases"])

    def test_priority_reflects_highest_likelihood(self):
        """If a test relates to both a high- and low-likelihood disease,
        its priority should reflect the highest."""
        suspected = [
            {"name": "Canine Parvovirus", "likelihood": "high"},
            {"name": "Gastroenteritis", "likelihood": "low"},
        ]
        result = _collect_tests(suspected)
        cbc = next(
            (t for t in result if t["name"] == "CBC (Complete Blood Count)"),
            None,
        )
        if cbc:
            assert cbc["priority"] == "urgent"

    def test_no_duplicate_test_names(self):
        suspected = [
            {"name": "Canine Parvovirus", "likelihood": "high"},
            {"name": "Pancreatitis", "likelihood": "moderate"},
            {"name": "Liver Disease", "likelihood": "low"},
        ]
        result = _collect_tests(suspected)
        names = [t["name"] for t in result]
        assert len(names) == len(set(names)), "Duplicate test names found"

    def test_output_sorted_by_priority_then_name(self):
        suspected = [
            {"name": "Canine Parvovirus", "likelihood": "high"},
            {"name": "Kidney Disease (CKD)", "likelihood": "moderate"},
        ]
        result = _collect_tests(suspected)
        for i in range(len(result) - 1):
            a_rank = _PRIORITY_RANK[result[i]["priority"]]
            b_rank = _PRIORITY_RANK[result[i + 1]["priority"]]
            if a_rank == b_rank:
                assert result[i]["name"] <= result[i + 1]["name"]
            else:
                assert a_rank >= b_rank


# ============================================================================
# 5. Data integrity
# ============================================================================


class TestDataIntegrity:
    """Validate the internal data structures for consistency."""

    # -- VALID_SYMPTOMS vs _SYMPTOM_NAMES ------------------------------

    def test_symptom_names_covers_valid_symptoms(self):
        """Every VALID_SYMPTOMS ID should have an entry in _SYMPTOM_NAMES."""
        missing = VALID_SYMPTOMS - set(_SYMPTOM_NAMES.keys())
        assert missing == set(), f"Missing from _SYMPTOM_NAMES: {missing}"

    def test_symptom_names_keys_are_valid(self):
        """_SYMPTOM_NAMES should not contain IDs absent from VALID_SYMPTOMS."""
        extra = set(_SYMPTOM_NAMES.keys()) - VALID_SYMPTOMS
        assert extra == set(), f"Extra keys in _SYMPTOM_NAMES: {extra}"

    def test_symptom_names_bilingual(self):
        for sid, names in _SYMPTOM_NAMES.items():
            assert "ja" in names, f"{sid} missing 'ja'"
            assert "en" in names, f"{sid} missing 'en'"
            assert isinstance(names["ja"], str) and len(names["ja"]) > 0
            assert isinstance(names["en"], str) and len(names["en"]) > 0

    def test_valid_symptoms_non_empty(self):
        assert len(VALID_SYMPTOMS) > 20

    def test_valid_symptoms_all_lowercase_snake_case(self):
        for s in VALID_SYMPTOMS:
            assert re.match(r"^[a-z][a-z0-9_]*$", s), (
                f"Invalid symptom ID format: {s}"
            )

    # -- Disease DB symptom references ---------------------------------

    def test_all_disease_symptoms_are_valid(self):
        """Every symptom in _DISEASE_DB must be in VALID_SYMPTOMS."""
        for disease in _DISEASE_DB:
            invalid = disease["symptoms"] - VALID_SYMPTOMS
            assert invalid == set(), (
                f"Disease '{disease['name']}' references invalid "
                f"symptom IDs: {invalid}"
            )

    def test_all_diseases_have_required_fields(self):
        required = {"name", "name_ja", "symptoms", "description", "urgency"}
        for disease in _DISEASE_DB:
            missing = required - set(disease.keys())
            assert missing == set(), (
                f"Disease '{disease.get('name', '???')}' missing: {missing}"
            )

    def test_disease_urgency_values(self):
        valid_urgency = {"low", "moderate", "normal", "high", "urgent", "emergency"}
        for disease in _DISEASE_DB:
            assert disease["urgency"] in valid_urgency, (
                f"Disease '{disease['name']}' has invalid urgency: "
                f"{disease['urgency']}"
            )

    def test_disease_symptoms_non_empty(self):
        for disease in _DISEASE_DB:
            assert len(disease["symptoms"]) > 0, (
                f"Disease '{disease['name']}' has empty symptoms set"
            )

    def test_disease_names_unique(self):
        names = [d["name"] for d in _DISEASE_DB]
        assert len(names) == len(set(names)), "Duplicate disease names"

    def test_disease_symptoms_are_sets(self):
        for disease in _DISEASE_DB:
            assert isinstance(disease["symptoms"], set), (
                f"Disease '{disease['name']}' symptoms should be a set"
            )

    # -- Health check category symptom references ----------------------

    def test_health_check_symptom_ids_are_valid(self):
        for cat_key, cat_data in HEALTH_CHECK_CATEGORIES.items():
            for item in cat_data["items"]:
                for sid in item["symptom_ids"]:
                    assert sid in VALID_SYMPTOMS, (
                        f"Category '{cat_key}', item '{item['ja']}' "
                        f"references invalid symptom ID: {sid}"
                    )

    def test_health_check_categories_have_labels(self):
        for cat_key, cat_data in HEALTH_CHECK_CATEGORIES.items():
            assert "label" in cat_data, f"'{cat_key}' missing 'label'"
            assert "label_en" in cat_data, f"'{cat_key}' missing 'label_en'"
            assert "icon" in cat_data, f"'{cat_key}' missing 'icon'"
            assert "items" in cat_data, f"'{cat_key}' missing 'items'"

    def test_health_check_items_structure(self):
        for cat_key, cat_data in HEALTH_CHECK_CATEGORIES.items():
            for item in cat_data["items"]:
                assert "ja" in item, f"Item missing 'ja' in {cat_key}"
                assert "en" in item, f"Item missing 'en' in {cat_key}"
                assert "symptom_ids" in item, (
                    f"Item missing 'symptom_ids' in {cat_key}"
                )
                assert isinstance(item["symptom_ids"], list)

    def test_health_check_categories_non_empty(self):
        assert len(HEALTH_CHECK_CATEGORIES) >= 10
        for cat_key, cat_data in HEALTH_CHECK_CATEGORIES.items():
            assert len(cat_data["items"]) > 0, (
                f"Category '{cat_key}' has no items"
            )

    # -- Test DB references valid diseases -----------------------------

    def test_test_db_related_diseases_exist(self):
        disease_names = {d["name"] for d in _DISEASE_DB}
        for test in _TEST_DB:
            invalid = test["related_diseases"] - disease_names
            assert invalid == set(), (
                f"Test '{test['name']}' references unknown diseases: "
                f"{invalid}"
            )

    def test_test_db_has_required_fields(self):
        required = {"name", "name_ja", "purpose", "related_diseases"}
        for test in _TEST_DB:
            missing = required - set(test.keys())
            assert missing == set(), (
                f"Test '{test.get('name', '???')}' missing: {missing}"
            )

    def test_test_db_related_diseases_are_sets(self):
        for test in _TEST_DB:
            assert isinstance(test["related_diseases"], set), (
                f"Test '{test['name']}' related_diseases should be a set"
            )

    def test_test_db_names_unique(self):
        names = [t["name"] for t in _TEST_DB]
        assert len(names) == len(set(names)), "Duplicate test names"

    # -- Breed disease risk references valid diseases -------------------

    def test_breed_risk_disease_names_exist(self):
        disease_names = {d["name"] for d in _DISEASE_DB}
        # Known data issues in the source module (disease name referenced
        # in _BREED_DISEASE_RISK but absent from _DISEASE_DB).
        known_missing = {
            ("146_italian_greyhound", "Fractures/Osteoarthritis"),
        }
        for breed_id, risks in _BREED_DISEASE_RISK.items():
            for disease_name in risks:
                if (breed_id, disease_name) in known_missing:
                    continue
                assert disease_name in disease_names, (
                    f"Breed '{breed_id}' risk references unknown disease: "
                    f"'{disease_name}'"
                )

    def test_known_missing_breed_risk_diseases_documented(self):
        """Document known data inconsistencies so they are not silently lost."""
        disease_names = {d["name"] for d in _DISEASE_DB}
        missing_pairs: list[tuple[str, str]] = []
        for breed_id, risks in _BREED_DISEASE_RISK.items():
            for disease_name in risks:
                if disease_name not in disease_names:
                    missing_pairs.append((breed_id, disease_name))
        # If this assertion breaks, a previously-missing disease was added
        # to _DISEASE_DB (good!) or new missing references appeared (bad).
        assert missing_pairs == [
            ("146_italian_greyhound", "Fractures/Osteoarthritis"),
        ], f"Unexpected missing breed-risk disease references: {missing_pairs}"

    def test_breed_risk_multipliers_positive(self):
        for breed_id, risks in _BREED_DISEASE_RISK.items():
            for disease_name, mult in risks.items():
                assert mult > 0, (
                    f"Breed '{breed_id}', disease '{disease_name}': "
                    f"non-positive multiplier {mult}"
                )

    def test_breed_risk_multipliers_are_numeric(self):
        for breed_id, risks in _BREED_DISEASE_RISK.items():
            for disease_name, mult in risks.items():
                assert isinstance(mult, (int, float)), (
                    f"Breed '{breed_id}', disease '{disease_name}': "
                    f"multiplier type is {type(mult)}"
                )

    # -- Breed genetic tests structure ---------------------------------

    def test_breed_genetic_tests_structure(self):
        for _breed_id, tests in _BREED_GENETIC_TESTS.items():
            assert isinstance(tests, list)
            for test in tests:
                assert "test" in test
                assert "test_ja" in test
                assert "purpose" in test

    def test_breed_genetic_tests_non_empty(self):
        for breed_id, tests in _BREED_GENETIC_TESTS.items():
            assert len(tests) > 0, (
                f"Breed '{breed_id}' has empty genetic tests list"
            )

    # -- _ANY_LIMPING consistency ---------------------------------------

    def test_any_limping_members_are_valid(self):
        assert _ANY_LIMPING <= VALID_SYMPTOMS

    def test_any_limping_has_four_limbs(self):
        assert len(_ANY_LIMPING) == 4
        assert {
            "limping_fl", "limping_fr", "limping_rl", "limping_rr"
        } == _ANY_LIMPING

    # -- Advice dictionary ---------------------------------------------

    def test_advice_keys(self):
        assert set(_ADVICE.keys()) == {"emergency", "high", "moderate", "low"}

    def test_advice_bilingual(self):
        for key, pair in _ADVICE.items():
            assert "en" in pair, f"Advice '{key}' missing 'en'"
            assert "ja" in pair, f"Advice '{key}' missing 'ja'"
            assert isinstance(pair["en"], str) and len(pair["en"]) > 0
            assert isinstance(pair["ja"], str) and len(pair["ja"]) > 0

    # -- Priority / likelihood mappings --------------------------------

    def test_priority_rank_keys(self):
        assert set(_PRIORITY_RANK.keys()) == {
            "optional", "recommended", "urgent"
        }

    def test_priority_rank_ordering(self):
        assert _PRIORITY_RANK["optional"] < _PRIORITY_RANK["recommended"]
        assert _PRIORITY_RANK["recommended"] < _PRIORITY_RANK["urgent"]

    def test_likelihood_to_priority_keys(self):
        assert set(_LIKELIHOOD_TO_PRIORITY.keys()) == {
            "high", "moderate", "low"
        }

    def test_likelihood_to_priority_values_are_valid(self):
        for lik, prio in _LIKELIHOOD_TO_PRIORITY.items():
            assert prio in _PRIORITY_RANK, (
                f"Likelihood '{lik}' maps to unknown priority '{prio}'"
            )

    # -- ABNORMAL_KEYWORDS non-empty -----------------------------------

    def test_abnormal_keywords_non_empty(self):
        assert len(ABNORMAL_KEYWORDS) > 0
        for kw in ABNORMAL_KEYWORDS:
            assert isinstance(kw, str) and len(kw) > 0


# ============================================================================
# 6. Edge cases
# ============================================================================


class TestEdgeCases:
    """Exercise boundary conditions and unusual inputs."""

    # -- empty / no symptoms -------------------------------------------

    def test_empty_symptom_list(self):
        result = analyze_symptoms([])
        assert result["suspected_diseases"] == []
        assert result["recommended_tests"] == []
        assert result["severity"] == "low"

    def test_empty_symptom_list_with_breed(self):
        result = analyze_symptoms([], breed="101_french_bulldog")
        assert result["suspected_diseases"] == []
        assert result["breed_genetic_tests"] != []

    # -- single symptom ------------------------------------------------

    def test_single_symptom_vomiting(self):
        result = analyze_symptoms(["vomiting"])
        assert isinstance(result["suspected_diseases"], list)
        assert result["severity"] in {"low", "moderate", "high", "emergency"}

    def test_single_rare_symptom(self):
        result = analyze_symptoms(["reverse_sneezing"])
        assert isinstance(result["suspected_diseases"], list)

    def test_single_symptom_seizures(self):
        result = analyze_symptoms(["seizures"])
        assert isinstance(result["suspected_diseases"], list)

    # -- all symptoms at once -----------------------------------------

    def test_all_valid_symptoms(self):
        """Feeding every valid symptom should not crash."""
        result = analyze_symptoms(list(VALID_SYMPTOMS))
        assert isinstance(result["suspected_diseases"], list)
        assert len(result["suspected_diseases"]) > 0

    # -- duplicate symptoms --------------------------------------------

    def test_duplicate_symptoms_ignored(self):
        result_dup = analyze_symptoms(
            ["vomiting", "vomiting", "lethargy", "lethargy"]
        )
        result_clean = analyze_symptoms(["vomiting", "lethargy"])
        assert (
            result_dup["suspected_diseases"]
            == result_clean["suspected_diseases"]
        )

    # -- unknown breed -------------------------------------------------

    def test_unknown_breed_id(self):
        result = analyze_symptoms(
            ["vomiting", "lethargy"], breed="999_unknown_breed"
        )
        assert result["breed_risk_applied"] is False
        assert result["breed_genetic_tests"] == []
        assert isinstance(result["suspected_diseases"], list)

    # -- breed = None ---------------------------------------------------

    def test_breed_none(self):
        result = analyze_symptoms(["vomiting"], breed=None)
        assert result["breed_risk_applied"] is False

    # -- only invalid symptoms -----------------------------------------

    def test_all_invalid_symptoms(self):
        result = analyze_symptoms(["fake_a", "fake_b", "fake_c"])
        assert result["suspected_diseases"] == []
        assert result["recommended_tests"] == []
        assert result["severity"] == "low"

    # -- map_health_checks round-trip ---------------------------------

    def test_health_check_to_analysis_round_trip(self):
        """map_health_checks_to_symptoms output -> analyze_symptoms."""
        symptom_ids = map_health_checks_to_symptoms({
            "digestive": ["嘔吐", "下痢", "血便"],
            "general": ["元気がない"],
        })
        result = analyze_symptoms(symptom_ids)
        assert len(result["suspected_diseases"]) > 0
        assert result["severity"] in {"emergency", "high", "moderate", "low"}

    # -- severity consistency with advice ------------------------------

    def test_advice_matches_severity(self):
        """Returned advice text must correspond to the severity level."""
        for symptoms_input in [
            ["sneezing"],
            ["vomiting", "lethargy", "diarrhea"],
            ["bloated_abdomen", "vomiting", "excessive_panting",
             "lethargy", "anxiety"],
        ]:
            result = analyze_symptoms(symptoms_input)
            severity = result["severity"]
            expected = _ADVICE.get(severity, _ADVICE["low"])
            assert result["general_advice"] == expected["en"]
            assert result["general_advice_ja"] == expected["ja"]

    # -- every known breed works without error -------------------------

    def test_all_known_breeds_in_breed_disease_risk(self):
        for breed_id in _BREED_DISEASE_RISK:
            result = analyze_symptoms(
                ["vomiting", "lethargy"], breed=breed_id
            )
            assert result["breed_risk_applied"] is True

    def test_all_breed_genetic_tests_returned(self):
        for breed_id in _BREED_GENETIC_TESTS:
            result = analyze_symptoms(["vomiting"], breed=breed_id)
            assert len(result["breed_genetic_tests"]) > 0, (
                f"No genetic tests for breed {breed_id}"
            )

    # -- limping symptoms specifically --------------------------------

    def test_limping_symptoms_match_diseases(self):
        result = analyze_symptoms([
            "limping_fl", "stiffness", "reluctance_move", "pain_on_touch",
        ])
        assert len(result["suspected_diseases"]) > 0

    # -- urinary symptoms ---------------------------------------------

    def test_urinary_symptoms_match(self):
        result = analyze_symptoms([
            "straining_urinate", "blood_urine", "excessive_urination",
        ])
        assert len(result["suspected_diseases"]) > 0

    # -- skin symptoms ------------------------------------------------

    def test_skin_symptoms_match(self):
        result = analyze_symptoms([
            "itching", "hair_loss", "skin_redness", "hot_spots",
        ])
        assert len(result["suspected_diseases"]) > 0

    # -- eye symptoms -------------------------------------------------

    def test_eye_symptoms_match(self):
        result = analyze_symptoms([
            "eye_redness", "eye_discharge", "squinting",
        ])
        assert len(result["suspected_diseases"]) > 0

    # -- recommended tests relate to suspected diseases ----------------

    def test_recommended_tests_relate_to_suspected_diseases(self):
        result = analyze_symptoms([
            "vomiting", "lethargy", "diarrhea", "appetite_loss",
        ])
        suspected_names = {
            d["name"] for d in result["suspected_diseases"]
        }
        for test in result["recommended_tests"]:
            related = set(test["related_diseases"])
            assert related & suspected_names, (
                f"Test '{test['name']}' unrelated to suspected diseases"
            )

    # -- match_count <= total_symptoms --------------------------------

    def test_match_count_lte_total_symptoms(self):
        result = analyze_symptoms(list(VALID_SYMPTOMS))
        for d in result["suspected_diseases"]:
            assert d["match_count"] <= d["total_symptoms"]
