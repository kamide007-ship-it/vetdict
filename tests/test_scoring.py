"""
Comprehensive tests for the deterministic scoring engine.

Tests cover:
- Weight immutability and integrity
- Age adjustment determinism
- Grade boundary accuracy
- Score calculation determinism
- AI score mapping
- Breed sensitivity profiles
- Cross-axis consistency validation
- Hybrid scoring pipeline
- Edge cases and boundary conditions
"""

import pytest

from api.scoring import (
    ALGORITHM_VERSION,
    AXIS_CORRELATIONS,
    BREED_PROFILE_MAP,
    BREED_SENSITIVITY_PROFILES,
    WEIGHTS,
    WEIGHTS_HASH,
    aggregate_ai_correction,
    age_years_to_months,
    calculate_score,
    compute_weights_hash,
    get_age_adjustment,
    get_breed_sensitivity,
    get_grade,
    map_ai_scores_to_axes,
    validate_cross_axis_consistency,
)


# ============================================================================
# Weight Integrity
# ============================================================================


class TestWeightIntegrity:
    """Verify weights are immutable and correctly defined."""

    def test_weights_sum_to_one(self):
        assert abs(sum(WEIGHTS.values()) - 1.0) < 0.0001

    def test_weights_have_all_axes(self):
        expected = {"skeletal", "gait", "muscle", "coat", "temperament"}
        assert set(WEIGHTS.keys()) == expected

    def test_weights_hash_is_stable(self):
        """Hash must not change across runs (immutability check)."""
        assert WEIGHTS_HASH == compute_weights_hash()

    def test_individual_weight_values(self):
        assert WEIGHTS["skeletal"] == 0.25
        assert WEIGHTS["gait"] == 0.25
        assert WEIGHTS["muscle"] == 0.20
        assert WEIGHTS["coat"] == 0.20
        assert WEIGHTS["temperament"] == 0.10

    def test_algorithm_version_exists(self):
        assert ALGORITHM_VERSION is not None
        assert isinstance(ALGORITHM_VERSION, str)


# ============================================================================
# Age Adjustment
# ============================================================================


class TestAgeAdjustment:
    """Verify deterministic age adjustments."""

    @pytest.mark.parametrize(
        "months,expected",
        [
            (0, -5),
            (3, -5),
            (6, -5),
            (7, -3),
            (12, -3),
            (13, -1),
            (24, -1),
            (25, 0),
            (48, 0),
            (84, 0),
            (85, -1),
            (108, -1),
            (109, -3),
            (132, -3),
            (133, -5),
            (180, -5),
        ],
    )
    def test_age_adjustment_values(self, months, expected):
        assert get_age_adjustment(months) == expected

    def test_negative_age_clamped_to_zero(self):
        assert get_age_adjustment(-1) == -5
        assert get_age_adjustment(-100) == -5

    def test_age_conversion(self):
        assert age_years_to_months(1.0) == 12
        assert age_years_to_months(3.5) == 42
        assert age_years_to_months(0.0) == 0
        assert age_years_to_months(7.0) == 84

    def test_age_adjustment_is_deterministic(self):
        """Same input always produces same output."""
        for months in range(0, 200, 5):
            a = get_age_adjustment(months)
            b = get_age_adjustment(months)
            assert a == b, f"Non-deterministic at {months} months"


# ============================================================================
# Grading
# ============================================================================


class TestGrading:
    """Verify FCI grade boundaries."""

    @pytest.mark.parametrize(
        "score,grade",
        [
            (100, "S"),
            (95, "S"),
            (94.9, "A+"),
            (90, "A+"),
            (89.9, "A"),
            (85, "A"),
            (84.9, "B+"),
            (80, "B+"),
            (79.9, "B"),
            (70, "B"),
            (69.9, "C"),
            (50, "C"),
            (0, "C"),
        ],
    )
    def test_grade_boundaries(self, score, grade):
        result_grade, _ = get_grade(score)
        assert result_grade == grade

    def test_grade_returns_tuple(self):
        grade, grade_full = get_grade(95)
        assert isinstance(grade, str)
        assert isinstance(grade_full, str)
        assert grade in grade_full


# ============================================================================
# Score Calculation
# ============================================================================


class TestCalculateScore:
    """Verify the core deterministic scoring function."""

    def _make_scores(self, val=80.0):
        return {
            "skeletal": val,
            "gait": val,
            "muscle": val,
            "coat": val,
            "temperament": val,
        }

    def test_basic_calculation(self):
        result = calculate_score(self._make_scores(80.0), age_years=3.0)
        assert result["final_score"] == 80.0
        assert result["grade"] == "B+"
        assert result["age_adjustment"] == 0
        assert result["algorithm_version"] == ALGORITHM_VERSION

    def test_perfect_score_prime_age(self):
        result = calculate_score(self._make_scores(100.0), age_years=3.0)
        assert result["final_score"] == 100.0
        assert result["grade"] == "S"

    def test_minimum_score(self):
        result = calculate_score(self._make_scores(0.0), age_years=3.0)
        assert result["final_score"] == 0.0
        assert result["grade"] == "C"

    def test_age_adjustment_applied(self):
        # Puppy (6 months) gets -5 adjustment
        result = calculate_score(self._make_scores(80.0), age_years=0.5)
        assert result["age_adjustment"] == -5
        assert result["final_score"] == 75.0

    def test_score_clamped_at_zero(self):
        result = calculate_score(self._make_scores(3.0), age_years=0.5)
        assert result["final_score"] >= 0.0

    def test_score_clamped_at_hundred(self):
        result = calculate_score(self._make_scores(100.0), age_years=3.0)
        assert result["final_score"] <= 100.0

    def test_weighted_sum_calculation(self):
        scores = {
            "skeletal": 90,
            "gait": 80,
            "muscle": 70,
            "coat": 60,
            "temperament": 50,
        }
        result = calculate_score(scores, age_years=3.0)
        expected_sum = 90 * 0.25 + 80 * 0.25 + 70 * 0.20 + 60 * 0.20 + 50 * 0.10
        assert abs(result["weighted_sum"] - expected_sum) < 0.01

    def test_missing_axis_raises_error(self):
        incomplete = {"skeletal": 80, "gait": 80}
        with pytest.raises(ValueError, match="Missing required axes"):
            calculate_score(incomplete, age_years=3.0)

    def test_none_score_treated_as_zero(self):
        scores = self._make_scores(80.0)
        scores["coat"] = None
        result = calculate_score(scores, age_years=3.0, validate=False)
        assert result["axis_scores"]["coat"] == 0.0

    def test_negative_score_clamped(self):
        scores = self._make_scores(80.0)
        scores["gait"] = -10
        result = calculate_score(scores, age_years=3.0, validate=False)
        assert result["axis_scores"]["gait"] == 0.0

    def test_over_100_score_clamped(self):
        scores = self._make_scores(80.0)
        scores["gait"] = 150
        result = calculate_score(scores, age_years=3.0, validate=False)
        assert result["axis_scores"]["gait"] == 100.0

    def test_result_has_all_fields(self):
        result = calculate_score(self._make_scores(80.0), age_years=3.0)
        required_fields = {
            "weighted_sum",
            "age_months",
            "age_adjustment",
            "final_score",
            "grade",
            "grade_full",
            "algorithm_version",
            "model_version",
            "weights_hash",
            "axis_scores",
            "weights",
            "calculation_timestamp",
        }
        assert required_fields.issubset(set(result.keys()))

    def test_determinism(self):
        """Same inputs must always produce the same output."""
        scores = {"skeletal": 87.3, "gait": 92.1, "muscle": 78.5, "coat": 81.0, "temperament": 90.0}
        r1 = calculate_score(scores, age_years=4.2)
        r2 = calculate_score(scores, age_years=4.2)
        assert r1["final_score"] == r2["final_score"]
        assert r1["grade"] == r2["grade"]
        assert r1["weighted_sum"] == r2["weighted_sum"]


# ============================================================================
# AI Score Mapping
# ============================================================================


class TestMapAiScores:
    """Verify AI output → canonical axis mapping."""

    def test_default_scores(self):
        result = map_ai_scores_to_axes()
        assert all(v == 75.0 for v in result.values())
        assert set(result.keys()) == {"skeletal", "gait", "muscle", "coat", "temperament"}

    def test_structure_score_maps_to_skeletal(self):
        result = map_ai_scores_to_axes(structure_score=90.0)
        assert result["skeletal"] == 90.0

    def test_structure_details_override(self):
        details = {"skeletal": 88.0, "muscular": 82.0, "proportion": 85.0}
        result = map_ai_scores_to_axes(structure_details=details)
        assert result["skeletal"] == 88.0
        assert result["muscle"] == 82.0

    def test_gait_details_averaging(self):
        details = {"stride": 80.0, "balance": 90.0, "fluidity": 85.0}
        result = map_ai_scores_to_axes(gait_details=details)
        assert result["gait"] == 85.0

    def test_temperament_details_averaging(self):
        details = {"confidence": 80.0, "alertness": 90.0, "composure": 70.0}
        result = map_ai_scores_to_axes(temperament_details=details)
        assert result["temperament"] == 80.0

    def test_coat_score_direct(self):
        result = map_ai_scores_to_axes(coat_score=95.0)
        assert result["coat"] == 95.0


# ============================================================================
# Breed Sensitivity
# ============================================================================


class TestBreedSensitivity:
    """Verify breed-specific sensitivity profiles."""

    def test_unknown_breed_returns_balanced(self):
        result = get_breed_sensitivity("unknown_breed_id")
        assert result == BREED_SENSITIVITY_PROFILES["balanced"]

    def test_none_breed_returns_balanced(self):
        result = get_breed_sensitivity(None)
        assert result == BREED_SENSITIVITY_PROFILES["balanced"]

    def test_known_breed_returns_correct_profile(self):
        result = get_breed_sensitivity("172d_poodle_toy")
        assert result == BREED_SENSITIVITY_PROFILES["coat_dominant"]

    def test_all_profiles_have_all_axes(self):
        for profile_name, profile in BREED_SENSITIVITY_PROFILES.items():
            assert set(profile.keys()) == set(WEIGHTS.keys()), (
                f"Profile {profile_name} missing axes"
            )

    def test_all_mapped_breeds_reference_valid_profiles(self):
        valid_profiles = set(BREED_SENSITIVITY_PROFILES.keys())
        for breed_id, profile_name in BREED_PROFILE_MAP.items():
            assert profile_name in valid_profiles, (
                f"Breed {breed_id} references unknown profile {profile_name}"
            )


# ============================================================================
# Cross-Axis Consistency
# ============================================================================


class TestCrossAxisConsistency:
    """Verify cross-axis consistency validation."""

    def test_consistent_scores(self):
        scores = {"skeletal": 85, "gait": 83, "muscle": 84, "coat": 80, "temperament": 82}
        result = validate_cross_axis_consistency(scores)
        assert result["consistency_score"] >= 0.8
        assert result["axes_checked"] == len(AXIS_CORRELATIONS)

    def test_highly_inconsistent_scores(self):
        scores = {"skeletal": 95, "gait": 30, "muscle": 20, "coat": 90, "temperament": 10}
        result = validate_cross_axis_consistency(scores)
        assert result["consistency_score"] < 0.8
        assert len(result["anomalies"]) > 0

    def test_equal_scores_are_consistent(self):
        scores = {"skeletal": 80, "gait": 80, "muscle": 80, "coat": 80, "temperament": 80}
        result = validate_cross_axis_consistency(scores)
        assert result["consistency_score"] == 1.0
        assert result["anomalies"] == []


# ============================================================================
# AI Correction Aggregation
# ============================================================================


class TestAggregateAiCorrection:
    """Verify AI correction aggregation."""

    def test_empty_sub_scores(self):
        assert aggregate_ai_correction({}, 80.0) == 0.0

    def test_none_sub_scores_ignored(self):
        assert aggregate_ai_correction({"a": None}, 80.0) == 0.0

    def test_zero_deviation(self):
        """Sub-scores matching base score produce zero correction."""
        correction = aggregate_ai_correction({"a": 80.0}, 80.0)
        assert correction == 0.0

    def test_positive_correction(self):
        correction = aggregate_ai_correction({"a": 90.0, "b": 95.0}, 80.0)
        assert correction > 0.0

    def test_negative_correction(self):
        correction = aggregate_ai_correction({"a": 60.0, "b": 55.0}, 80.0)
        assert correction < 0.0

    def test_breed_sensitivity_amplifies(self):
        base = aggregate_ai_correction({"a": 90.0}, 80.0, breed_sensitivity=1.0)
        amplified = aggregate_ai_correction({"a": 90.0}, 80.0, breed_sensitivity=1.6)
        assert abs(amplified) > abs(base)

    def test_more_sub_scores_increase_confidence(self):
        one = abs(aggregate_ai_correction({"a": 90.0}, 80.0))
        three = abs(aggregate_ai_correction({"a": 90.0, "b": 90.0, "c": 90.0}, 80.0))
        assert three >= one
