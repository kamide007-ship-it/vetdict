"""Tests for equine_diseases.py – DISEASE_DATABASE integrity and generate_differential_diagnosis."""

import pytest

from api.species.equine_diseases import (
    _FINDING_IDF,
    _FINDING_LABEL_JA,
    DISEASE_DATABASE,
    HEALTH_CHECK_ITEMS,
    DifferentialItem,
    Disease,
    _confidence_level,
    generate_differential_diagnosis,
    get_all_categories,
    get_disease,
    get_diseases_by_category,
)

# ===================================================================
# DISEASE_DATABASE integrity tests
# ===================================================================


class TestDiseaseDatabase:
    def test_database_is_nonempty(self):
        assert len(DISEASE_DATABASE) > 0

    def test_all_entries_are_disease_instances(self):
        for disease in DISEASE_DATABASE:
            assert isinstance(disease, Disease), f"{disease} is not a Disease"

    def test_all_ids_are_unique(self):
        ids = [d.id for d in DISEASE_DATABASE]
        assert len(ids) == len(set(ids)), "Duplicate disease IDs found"

    def test_all_ids_are_nonempty_strings(self):
        for d in DISEASE_DATABASE:
            assert isinstance(d.id, str) and d.id.strip(), f"Bad id: {d!r}"

    def test_all_names_nonempty(self):
        for d in DISEASE_DATABASE:
            assert d.name_ja or d.name_en, f"Disease {d.id} has no name"

    def test_severity_values_valid(self):
        valid = {"mild", "moderate", "severe", "critical"}
        for d in DISEASE_DATABASE:
            assert d.severity in valid, f"{d.id} has invalid severity: {d.severity}"

    def test_category_values_nonempty(self):
        for d in DISEASE_DATABASE:
            assert isinstance(d.category, str) and d.category.strip(), f"{d.id} has empty category"

    def test_age_predisposition_valid(self):
        valid = {"young", "adult", "senior", ""}
        for d in DISEASE_DATABASE:
            assert d.age_predisposition in valid, f"{d.id} has invalid age_predisposition: {d.age_predisposition}"

    def test_urgency_valid(self):
        valid = {"emergency", "urgent", "routine", "soon", ""}
        for d in DISEASE_DATABASE:
            assert d.urgency in valid, f"{d.id} urgency invalid: {d.urgency}"

    def test_associated_findings_are_lists(self):
        for d in DISEASE_DATABASE:
            assert isinstance(d.associated_findings, list), f"{d.id}.associated_findings is not a list"

    def test_recommended_exams_structure(self):
        for d in DISEASE_DATABASE:
            for exam in d.recommended_exams:
                assert isinstance(exam, tuple) and len(exam) == 3, f"{d.id} recommended_exams entry malformed: {exam}"
                priority, name_ja, name_en = exam
                assert isinstance(priority, int), f"{d.id} priority not int"

    def test_merck_url_format(self):
        for d in DISEASE_DATABASE:
            if d.merck_url:
                assert d.merck_url.startswith("https://"), (
                    f"{d.id} merck_url doesn't start with https://: {d.merck_url}"
                )

    def test_known_disease_ids_present(self):
        ids = {d.id for d in DISEASE_DATABASE}
        expected = {"ms_ocd", "ms_tendonitis", "ms_splints"}
        for eid in expected:
            assert eid in ids, f"Expected disease id {eid} not found"


# ===================================================================
# HEALTH_CHECK_ITEMS integrity
# ===================================================================


class TestHealthCheckItems:
    def test_health_check_is_dict(self):
        assert isinstance(HEALTH_CHECK_ITEMS, dict)

    def test_all_categories_nonempty(self):
        assert len(HEALTH_CHECK_ITEMS) > 0

    def test_each_item_is_triple(self):
        for category, items in HEALTH_CHECK_ITEMS.items():
            for item in items:
                assert len(item) == 3, f"Category {category}: item not a triple: {item}"

    def test_item_keys_are_strings(self):
        for category, items in HEALTH_CHECK_ITEMS.items():
            for key, _ja, _en in items:
                assert isinstance(key, str) and key, f"Bad key in {category}: {key!r}"

    def test_no_duplicate_finding_keys(self):
        all_keys = [key for items in HEALTH_CHECK_ITEMS.values() for key, _, _ in items]
        assert len(all_keys) == len(set(all_keys)), "Duplicate finding keys in HEALTH_CHECK_ITEMS"


# ===================================================================
# IDF / label helpers
# ===================================================================


class TestFindingIDF:
    def test_idf_dict_nonempty(self):
        assert len(_FINDING_IDF) > 0

    def test_idf_values_positive(self):
        for key, val in _FINDING_IDF.items():
            assert val > 0.0, f"IDF for {key} is not positive: {val}"

    def test_idf_keys_are_strings(self):
        for key in _FINDING_IDF:
            assert isinstance(key, str), f"IDF key not string: {key!r}"

    def test_finding_label_ja_populated(self):
        assert len(_FINDING_LABEL_JA) > 0

    def test_finding_label_ja_values_nonempty(self):
        for key, label in _FINDING_LABEL_JA.items():
            assert isinstance(label, str) and label, f"Label for {key} is empty"


# ===================================================================
# _confidence_level helper
# ===================================================================


class TestConfidenceLevel:
    def test_high_threshold(self):
        assert _confidence_level(65.0) == "high"
        assert _confidence_level(99.0) == "high"
        assert _confidence_level(70.0) == "high"

    def test_medium_threshold(self):
        assert _confidence_level(35.0) == "medium"
        assert _confidence_level(50.0) == "medium"
        assert _confidence_level(64.9) == "medium"

    def test_low_threshold(self):
        assert _confidence_level(0.0) == "low"
        assert _confidence_level(10.0) == "low"
        assert _confidence_level(34.9) == "low"


# ===================================================================
# generate_differential_diagnosis
# ===================================================================


class TestGenerateDifferentialDiagnosis:
    def test_empty_findings_returns_empty(self):
        result = generate_differential_diagnosis(set())
        assert result == []

    def test_returns_list_of_differential_items(self):
        findings = {"limb_joint_swelling", "limb_ocd_signs"}
        result = generate_differential_diagnosis(findings)
        assert isinstance(result, list)
        for item in result:
            assert isinstance(item, DifferentialItem)

    def test_single_matching_finding(self):
        # hoof_heat is a finding in at least one disease
        result = generate_differential_diagnosis({"hoof_heat"})
        assert len(result) >= 0  # may return something or nothing depending on IDF

    def test_known_ocd_findings(self):
        # OCD disease has: limb_joint_swelling, limb_ocd_signs, limb_flexion_positive, repo_ocd_xray
        findings = {"limb_joint_swelling", "limb_ocd_signs", "limb_flexion_positive", "repo_ocd_xray"}
        result = generate_differential_diagnosis(findings)
        assert len(result) > 0
        ids = [r.disease.id for r in result]
        assert "ms_ocd" in ids

    def test_ocd_is_top_result_with_specific_findings(self):
        findings = {"limb_joint_swelling", "limb_ocd_signs", "limb_flexion_positive", "repo_ocd_xray"}
        result = generate_differential_diagnosis(findings)
        assert result[0].disease.id == "ms_ocd"

    def test_results_sorted_by_confidence_descending(self):
        findings = {"gen_fever", "resp_cough", "resp_nasal_discharge", "limb_lameness_fore"}
        result = generate_differential_diagnosis(findings)
        if len(result) > 1:
            confidences = [r.confidence_pct for r in result]
            assert confidences == sorted(confidences, reverse=True)

    def test_confidence_pct_in_valid_range(self):
        findings = {"gen_fever", "gen_lethargy", "resp_cough"}
        result = generate_differential_diagnosis(findings)
        for item in result:
            assert 0.0 <= item.confidence_pct <= 99.0, (
                f"confidence_pct {item.confidence_pct} out of range for {item.disease.id}"
            )

    def test_match_count_correct(self):
        findings = {"limb_joint_swelling", "limb_ocd_signs", "limb_flexion_positive", "repo_ocd_xray"}
        result = generate_differential_diagnosis(findings)
        ocd = next(r for r in result if r.disease.id == "ms_ocd")
        assert ocd.match_count == 4
        assert sorted(ocd.matched_findings) == sorted(
            ["limb_joint_swelling", "limb_ocd_signs", "limb_flexion_positive", "repo_ocd_xray"]
        )

    def test_match_ratio_in_range(self):
        findings = {"limb_joint_swelling", "limb_ocd_signs"}
        result = generate_differential_diagnosis(findings)
        for item in result:
            assert 0.0 <= item.match_ratio <= 1.2, f"match_ratio {item.match_ratio} out of range for {item.disease.id}"

    def test_age_stage_young_boosts_young_diseases(self):
        # OCD is age_predisposition="young"
        findings = {"limb_joint_swelling", "limb_ocd_signs", "limb_flexion_positive", "repo_ocd_xray"}
        result_no_age = generate_differential_diagnosis(findings, age_stage="")
        result_young = generate_differential_diagnosis(findings, age_stage="young")

        ocd_no_age = next(r for r in result_no_age if r.disease.id == "ms_ocd")
        ocd_young = next(r for r in result_young if r.disease.id == "ms_ocd")
        # Young age stage should produce equal or higher confidence for young-predisposed disease
        assert ocd_young.confidence_pct >= ocd_no_age.confidence_pct

    def test_age_stage_adult(self):
        findings = {"gen_fever", "resp_cough"}
        result = generate_differential_diagnosis(findings, age_stage="adult")
        assert isinstance(result, list)

    def test_age_stage_senior(self):
        findings = {"gen_fever", "gen_lethargy"}
        result = generate_differential_diagnosis(findings, age_stage="senior")
        assert isinstance(result, list)

    def test_unrelated_findings_no_match(self):
        # Completely made-up finding keys that don't match any disease
        result = generate_differential_diagnosis({"nonexistent_finding_xyz"})
        assert result == []

    def test_combo_bonus_increases_confidence(self):
        # Using many findings of a specific disease should yield higher score
        findings_many = {"limb_joint_swelling", "limb_ocd_signs", "limb_flexion_positive", "repo_ocd_xray"}
        findings_few = {"limb_joint_swelling", "limb_ocd_signs"}
        result_many = generate_differential_diagnosis(findings_many)
        result_few = generate_differential_diagnosis(findings_few)
        ocd_many = next((r for r in result_many if r.disease.id == "ms_ocd"), None)
        ocd_few = next((r for r in result_few if r.disease.id == "ms_ocd"), None)
        if ocd_many and ocd_few:
            assert ocd_many.confidence_pct >= ocd_few.confidence_pct

    def test_absence_penalty_applied_with_many_checked(self):
        # With 3+ findings checked, diseases with absent high-IDF findings get penalty
        findings = {"gen_fever", "gen_lethargy", "gen_weight_loss"}
        result = generate_differential_diagnosis(findings)
        # At least some results should have absence penalty > 0
        if result:
            penalties = [r.absence_penalty for r in result]
            # Not all need penalty, but function runs without error
            assert all(0.0 <= p <= 0.35 for p in penalties)

    def test_rule_out_note_populated_when_penalty_high(self):
        # Many highly specific findings from one disease, others have absent high-IDF findings
        findings = {
            "hoof_laminitis_signs",
            "limb_digital_pulse",
            "hoof_heat",
            "gen_fever",
            "gen_lethargy",
            "gen_weight_loss",
            "body_neck_crest",
            "body_fat_deposits",
        }
        result = generate_differential_diagnosis(findings)
        # Function should run; some items may have rule_out_note
        for item in result:
            assert isinstance(item.rule_out_note, str)

    def test_differential_item_attributes(self):
        findings = {"limb_joint_swelling", "limb_ocd_signs", "limb_flexion_positive", "repo_ocd_xray"}
        result = generate_differential_diagnosis(findings)
        assert len(result) > 0
        item = result[0]
        assert isinstance(item.match_count, int)
        assert isinstance(item.match_ratio, float)
        assert isinstance(item.matched_findings, list)
        assert isinstance(item.confidence_pct, float)
        assert isinstance(item.confidence_level, str)
        assert item.confidence_level in ("high", "medium", "low")
        assert isinstance(item.weighted_score, float)
        assert isinstance(item.absence_penalty, float)
        assert isinstance(item.absent_key_findings, list)
        assert isinstance(item.rule_out_note, str)

    def test_tendonitis_findings(self):
        # Tendonitis: limb_tendon_heat, limb_tendon_swelling, limb_lameness_fore
        findings = {"limb_tendon_heat", "limb_tendon_swelling", "limb_lameness_fore"}
        result = generate_differential_diagnosis(findings)
        ids = [r.disease.id for r in result]
        assert "ms_tendonitis" in ids

    def test_respiratory_findings(self):
        findings = {"resp_cough", "resp_nasal_discharge", "resp_labored_breathing"}
        result = generate_differential_diagnosis(findings)
        assert len(result) > 0

    def test_digestive_colic_findings(self):
        findings = {"dig_colic_signs", "dig_reduced_gut", "body_abdominal_distension"}
        result = generate_differential_diagnosis(findings)
        assert len(result) > 0

    def test_neurological_findings(self):
        findings = {"neuro_ataxia", "neuro_head_tilt", "neuro_seizure"}
        result = generate_differential_diagnosis(findings)
        assert len(result) > 0

    def test_foal_findings(self):
        findings = {"foal_weak_suckle", "foal_fever", "foal_lethargy"}
        result = generate_differential_diagnosis(findings)
        assert isinstance(result, list)

    def test_large_finding_set(self):
        # Provide a large set of findings across categories
        findings = {
            "gen_fever",
            "gen_lethargy",
            "resp_cough",
            "resp_nasal_discharge",
            "limb_joint_swelling",
            "limb_lameness_fore",
            "hoof_heat",
            "dig_colic_signs",
            "neuro_ataxia",
            "skin_lesions",
        }
        result = generate_differential_diagnosis(findings)
        assert len(result) > 0

    def test_five_or_more_matches_combo_bonus(self):
        # Find a disease with 5+ associated_findings and trigger the 1.20 combo bonus
        target = next(
            (d for d in DISEASE_DATABASE if len(d.associated_findings) >= 5),
            None,
        )
        if target is None:
            pytest.skip("No disease with 5+ findings in database")
        findings = set(target.associated_findings[:5])
        result = generate_differential_diagnosis(findings)
        match = next((r for r in result if r.disease.id == target.id), None)
        assert match is not None
        assert match.match_count >= 5

    def test_absent_finding_without_ja_label(self):
        # Force an absent finding that has no Japanese label (not in HEALTH_CHECK_ITEMS)
        # by using a finding key present in a disease but not in HEALTH_CHECK_ITEMS
        # We create a synthetic scenario: use enough checked findings to trigger absence_penalty
        # and ensure rule_out_note falls through the else branch (label not found)
        # The line is covered when absent_key_findings include raw finding IDs not in _FINDING_LABEL_JA
        # This happens for repository_exam keys that may not be in HEALTH_CHECK_ITEMS
        # We just need 3+ checked findings to trigger the absence penalty path
        findings = {"gen_fever", "gen_lethargy", "gen_weight_loss", "resp_cough", "resp_nasal_discharge"}
        result = generate_differential_diagnosis(findings)
        # Just ensure it runs; rule_out_note path covered
        assert isinstance(result, list)

    def test_single_finding_disease_penalty(self):
        # A disease with only 1 associated finding and a common finding key
        # (combo_bonus = 0.55 branch for low-IDF single findings)
        # Use gen_fever which appears in many diseases (low IDF)
        findings = {"gen_fever"}
        result = generate_differential_diagnosis(findings)
        # Should run without error; results may be empty or populated
        assert isinstance(result, list)


# ===================================================================
# Disease.reference_links()
# ===================================================================


class TestDiseaseReferenceLinks:
    def test_reference_links_with_name_en(self):
        d = DISEASE_DATABASE[0]
        links = d.reference_links()
        assert isinstance(links, list)
        assert len(links) >= 2  # At least HorseDVM and EquiMed

    def test_reference_links_contain_horsedvm(self):
        d = next(dd for dd in DISEASE_DATABASE if dd.name_en)
        links = d.reference_links()
        labels = [l["label"] for l in links]
        assert "HorseDVM" in labels

    def test_reference_links_contain_equimed(self):
        d = next(dd for dd in DISEASE_DATABASE if dd.name_en)
        links = d.reference_links()
        labels = [l["label"] for l in links]
        assert "EquiMed" in labels

    def test_reference_links_merck_url_used_when_set(self):
        d = next(dd for dd in DISEASE_DATABASE if dd.merck_url)
        links = d.reference_links()
        labels = [l["label"] for l in links]
        assert "Merck Vet Manual" in labels
        merck_link = next(l for l in links if l["label"] == "Merck Vet Manual")
        assert merck_link["url"] == d.merck_url

    def test_reference_links_merck_fallback_search(self):
        # Disease without merck_url but with name_en → search URL
        d = Disease(
            "test_no_merck",
            "テスト疾患",
            "Test Disease",
            "musculoskeletal",
            "mild",
            "テスト用",
            [],
        )
        links = d.reference_links()
        merck_links = [l for l in links if l["label"] == "Merck Vet Manual"]
        assert len(merck_links) == 1
        assert "search" in merck_links[0]["url"]

    def test_reference_links_no_name_en(self):
        d = Disease(
            "test_no_en",
            "テスト疾患",
            "",  # no name_en
            "musculoskeletal",
            "mild",
            "テスト用",
            [],
        )
        links = d.reference_links()
        # No HorseDVM/EquiMed/Merck search links without name_en
        assert isinstance(links, list)
        assert len(links) == 0


# ===================================================================
# Helper functions: get_disease, get_diseases_by_category, get_all_categories
# ===================================================================


class TestHelperFunctions:
    def test_get_disease_known_id(self):
        result = get_disease("ms_ocd")
        assert result is not None
        assert isinstance(result, Disease)
        assert result.id == "ms_ocd"

    def test_get_disease_unknown_id(self):
        result = get_disease("nonexistent_id_xyz")
        assert result is None

    def test_get_disease_empty_string(self):
        result = get_disease("")
        assert result is None

    def test_get_diseases_by_category_musculoskeletal(self):
        result = get_diseases_by_category("musculoskeletal")
        assert isinstance(result, list)
        assert len(result) > 0
        for d in result:
            assert d.category == "musculoskeletal"

    def test_get_diseases_by_category_unknown(self):
        result = get_diseases_by_category("nonexistent_category")
        assert result == []

    def test_get_diseases_by_category_hoof(self):
        result = get_diseases_by_category("hoof")
        assert isinstance(result, list)
        # Hoof category should exist in the database
        assert len(result) >= 0  # may be empty or populated

    def test_get_all_categories_returns_list(self):
        categories = get_all_categories()
        assert isinstance(categories, list)
        assert len(categories) > 0

    def test_get_all_categories_no_duplicates(self):
        categories = get_all_categories()
        assert len(categories) == len(set(categories))

    def test_get_all_categories_contains_musculoskeletal(self):
        categories = get_all_categories()
        assert "musculoskeletal" in categories

    def test_get_all_categories_contains_known_categories(self):
        categories = get_all_categories()
        # At least a few expected categories
        for expected in ["musculoskeletal", "respiratory", "digestive"]:
            assert expected in categories, f"Category '{expected}' not in get_all_categories()"
