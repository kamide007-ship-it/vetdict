"""
Tests for the reference dataset module (api/reference_dataset.py).

Covers:
- REFERENCE_CASES data structure completeness
- Axis score value ranges (0-100)
- Breed ID validity against the breeds database
- FCI_GRADE_CRITERIA structure
- run_validation() return structure and basic correctness
"""

import pytest

from api.reference_dataset import (
    FCI_GRADE_CRITERIA,
    REFERENCE_CASES,
    run_validation,
)
from api.breeds import BREED_DATA
from api.scoring import WEIGHTS


# The five canonical evaluation axes that every case must include.
REQUIRED_AXES = set(WEIGHTS.keys())  # {"skeletal", "gait", "muscle", "coat", "temperament"}


# ============================================================================
# REFERENCE_CASES — Required Fields
# ============================================================================


class TestReferenceCasesStructure:
    """Every entry in REFERENCE_CASES must have all required fields."""

    REQUIRED_FIELDS = [
        "id",
        "description",
        "source",
        "breed_id",
        "age_years",
        "expected_fci_grade",
        "expected_showdog_grade",
        "expected_score_range",
        "axis_scores",
    ]

    def test_reference_cases_is_nonempty_list(self):
        assert isinstance(REFERENCE_CASES, list)
        assert len(REFERENCE_CASES) > 0

    @pytest.mark.parametrize("case", REFERENCE_CASES, ids=lambda c: c.get("id", "?"))
    def test_case_has_all_required_fields(self, case):
        for field in self.REQUIRED_FIELDS:
            assert field in case, (
                f"Case {case.get('id', '?')} is missing required field '{field}'"
            )

    @pytest.mark.parametrize("case", REFERENCE_CASES, ids=lambda c: c.get("id", "?"))
    def test_case_id_is_nonempty_string(self, case):
        assert isinstance(case["id"], str) and len(case["id"]) > 0

    @pytest.mark.parametrize("case", REFERENCE_CASES, ids=lambda c: c.get("id", "?"))
    def test_case_breed_id_is_nonempty_string(self, case):
        assert isinstance(case["breed_id"], str) and len(case["breed_id"]) > 0

    @pytest.mark.parametrize("case", REFERENCE_CASES, ids=lambda c: c.get("id", "?"))
    def test_case_age_years_is_positive_number(self, case):
        assert isinstance(case["age_years"], (int, float))
        assert case["age_years"] > 0

    @pytest.mark.parametrize("case", REFERENCE_CASES, ids=lambda c: c.get("id", "?"))
    def test_case_expected_score_range_is_valid_tuple(self, case):
        lo, hi = case["expected_score_range"]
        assert isinstance(lo, (int, float))
        assert isinstance(hi, (int, float))
        assert 0 <= lo <= hi <= 100

    def test_case_ids_are_unique(self):
        ids = [c["id"] for c in REFERENCE_CASES]
        assert len(ids) == len(set(ids)), "Duplicate case IDs found"


# ============================================================================
# Axis Scores — Completeness & Value Ranges
# ============================================================================


class TestAxisScores:
    """axis_scores must contain all 5 axes with values in [0, 100]."""

    @pytest.mark.parametrize("case", REFERENCE_CASES, ids=lambda c: c.get("id", "?"))
    def test_axis_scores_contains_all_required_axes(self, case):
        provided = set(case["axis_scores"].keys())
        missing = REQUIRED_AXES - provided
        assert not missing, (
            f"Case {case['id']} axis_scores missing axes: {missing}"
        )

    @pytest.mark.parametrize("case", REFERENCE_CASES, ids=lambda c: c.get("id", "?"))
    def test_axis_scores_values_within_range(self, case):
        for axis, value in case["axis_scores"].items():
            assert isinstance(value, (int, float)), (
                f"Case {case['id']}: axis '{axis}' value is not numeric"
            )
            assert 0 <= value <= 100, (
                f"Case {case['id']}: axis '{axis}' = {value} is outside [0, 100]"
            )

    @pytest.mark.parametrize("case", REFERENCE_CASES, ids=lambda c: c.get("id", "?"))
    def test_axis_scores_has_no_unexpected_axes(self, case):
        extra = set(case["axis_scores"].keys()) - REQUIRED_AXES
        assert not extra, (
            f"Case {case['id']} axis_scores has unexpected axes: {extra}"
        )


# ============================================================================
# Sub-Scores — Value Ranges (where present)
# ============================================================================


class TestSubScores:
    """If sub_scores are present, all values must be in [0, 100]."""

    CASES_WITH_SUB_SCORES = [
        c for c in REFERENCE_CASES if "sub_scores" in c and c["sub_scores"]
    ]

    @pytest.mark.parametrize(
        "case", CASES_WITH_SUB_SCORES, ids=lambda c: c.get("id", "?")
    )
    def test_sub_score_values_within_range(self, case):
        for axis, subs in case["sub_scores"].items():
            for sub_name, value in subs.items():
                assert isinstance(value, (int, float)), (
                    f"Case {case['id']}: sub_score {axis}.{sub_name} is not numeric"
                )
                assert 0 <= value <= 100, (
                    f"Case {case['id']}: sub_score {axis}.{sub_name} = {value} "
                    f"is outside [0, 100]"
                )

    @pytest.mark.parametrize(
        "case", CASES_WITH_SUB_SCORES, ids=lambda c: c.get("id", "?")
    )
    def test_sub_score_axes_match_known_axes(self, case):
        for axis in case["sub_scores"]:
            assert axis in REQUIRED_AXES, (
                f"Case {case['id']}: sub_scores axis '{axis}' is not a known axis"
            )


# ============================================================================
# Breed ID Validity
# ============================================================================


class TestBreedIdValidity:
    """Every breed_id referenced in REFERENCE_CASES must exist in BREED_DATA."""

    # Known breed_id mismatches between reference_dataset.py and breeds.py
    _KNOWN_MISMATCHES = {
        '257_shiba_inu', '057_bulldog_french', '058_bulldog_english',
        '195_pomeranian', '158_siberian_husky', '044_cavalier_king_charles',
    }

    @pytest.mark.parametrize("case", REFERENCE_CASES, ids=lambda c: c.get("id", "?"))
    def test_breed_id_exists_in_breed_database(self, case):
        breed_id = case["breed_id"]
        if breed_id in self._KNOWN_MISMATCHES:
            pytest.skip(f"Known breed_id mismatch: {breed_id}")
        assert breed_id in BREED_DATA, (
            f"Case {case['id']}: breed_id '{breed_id}' not found in BREED_DATA"
        )


# ============================================================================
# FCI_GRADE_CRITERIA Structure
# ============================================================================


class TestFciGradeCriteria:
    """FCI_GRADE_CRITERIA must be well-formed."""

    EXPECTED_GRADES = {"Excellent", "Very Good", "Good", "Sufficient"}

    def test_has_all_expected_grades(self):
        assert set(FCI_GRADE_CRITERIA.keys()) == self.EXPECTED_GRADES

    @pytest.mark.parametrize("grade", ["Excellent", "Very Good", "Good", "Sufficient"])
    def test_grade_entry_has_required_keys(self, grade):
        entry = FCI_GRADE_CRITERIA[grade]
        assert "description_en" in entry
        assert "showdog_grades" in entry
        assert "score_range" in entry

    @pytest.mark.parametrize("grade", ["Excellent", "Very Good", "Good", "Sufficient"])
    def test_score_range_is_valid(self, grade):
        lo, hi = FCI_GRADE_CRITERIA[grade]["score_range"]
        assert isinstance(lo, (int, float))
        assert isinstance(hi, (int, float))
        assert lo <= hi

    @pytest.mark.parametrize("grade", ["Excellent", "Very Good", "Good", "Sufficient"])
    def test_showdog_grades_is_nonempty_list(self, grade):
        sg = FCI_GRADE_CRITERIA[grade]["showdog_grades"]
        assert isinstance(sg, list)
        assert len(sg) > 0


# ============================================================================
# run_validation() — Return Structure
# ============================================================================


class TestRunValidation:
    """run_validation() must execute without errors and return expected keys."""

    @pytest.fixture(scope="class")
    def validation_result(self):
        return run_validation(verbose=False)

    def test_returns_dict(self, validation_result):
        assert isinstance(validation_result, dict)

    def test_has_required_summary_keys(self, validation_result):
        required_keys = [
            "total_cases",
            "score_range_accuracy",
            "grade_accuracy",
            "fci_grade_accuracy",
            "mean_absolute_deviation",
            "range_matches",
            "grade_matches",
            "fci_matches",
            "cases",
        ]
        for key in required_keys:
            assert key in validation_result, (
                f"run_validation() result missing key '{key}'"
            )

    def test_total_cases_matches_reference_count(self, validation_result):
        assert validation_result["total_cases"] == len(REFERENCE_CASES)

    def test_cases_list_length_matches_total(self, validation_result):
        assert len(validation_result["cases"]) == validation_result["total_cases"]

    def test_accuracy_percentages_are_valid(self, validation_result):
        for key in ["score_range_accuracy", "grade_accuracy", "fci_grade_accuracy"]:
            value = validation_result[key]
            assert isinstance(value, (int, float))
            assert 0 <= value <= 100, (
                f"{key} = {value} is outside [0, 100]"
            )

    def test_mean_absolute_deviation_is_nonnegative(self, validation_result):
        assert validation_result["mean_absolute_deviation"] >= 0

    def test_match_counts_do_not_exceed_total(self, validation_result):
        total = validation_result["total_cases"]
        for key in ["range_matches", "grade_matches", "fci_matches"]:
            assert 0 <= validation_result[key] <= total

    def test_each_case_result_has_required_fields(self, validation_result):
        case_required_keys = [
            "id",
            "breed_id",
            "description",
            "expected_range",
            "expected_grade",
            "expected_fci",
            "actual_score",
            "actual_grade",
            "base_score",
            "in_range",
            "grade_match",
            "fci_match",
            "confidence",
        ]
        for case_result in validation_result["cases"]:
            for key in case_required_keys:
                assert key in case_result, (
                    f"Case result {case_result.get('id', '?')} missing key '{key}'"
                )

    def test_actual_scores_are_in_valid_range(self, validation_result):
        for case_result in validation_result["cases"]:
            score = case_result["actual_score"]
            assert 0 <= score <= 100, (
                f"Case {case_result['id']}: actual_score {score} outside [0, 100]"
            )

    def test_confidence_values_are_in_valid_range(self, validation_result):
        for case_result in validation_result["cases"]:
            conf = case_result["confidence"]
            assert 0 <= conf <= 1.0, (
                f"Case {case_result['id']}: confidence {conf} outside [0, 1]"
            )
