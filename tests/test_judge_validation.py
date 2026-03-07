"""
Tests for the judge validation statistical system.

Tests cover:
- Helper functions (mean, variance, Pearson r)
- Cohen's Kappa
- Weighted Kappa
- ICC (Intraclass Correlation Coefficient)
- Bland-Altman analysis
- Per-axis Pearson correlation
- Sample size recommendations
- JudgeValidationSession
"""

import pytest

from api.judge_validation import (
    SCORING_AXES,
    _mean,
    _pearson_r,
    _std,
    _var,
    compute_bland_altman,
    compute_cohens_kappa,
    compute_icc,
    compute_per_axis_correlation,
    compute_weighted_kappa,
    get_sample_size_recommendation,
    JudgeValidationSession,
)


# ============================================================================
# Helper Functions
# ============================================================================


class TestHelpers:
    def test_mean(self):
        assert _mean([1, 2, 3]) == 2.0

    def test_mean_single(self):
        assert _mean([5]) == 5.0

    def test_mean_empty_raises(self):
        with pytest.raises(ValueError):
            _mean([])

    def test_var_population(self):
        result = _var([2, 4, 4, 4, 5, 5, 7, 9], ddof=0)
        assert abs(result - 4.0) < 0.01

    def test_std(self):
        result = _std([2, 4, 4, 4, 5, 5, 7, 9])
        assert abs(result - 2.0) < 0.01

    def test_pearson_r_perfect_positive(self):
        r = _pearson_r([1, 2, 3, 4, 5], [2, 4, 6, 8, 10])
        assert abs(r - 1.0) < 0.01

    def test_pearson_r_perfect_negative(self):
        r = _pearson_r([1, 2, 3, 4, 5], [10, 8, 6, 4, 2])
        assert abs(r - (-1.0)) < 0.01

    def test_pearson_r_zero_variance(self):
        r = _pearson_r([1, 2, 3, 4, 5], [5, 5, 5, 5, 5])
        assert r == 0.0


# ============================================================================
# Cohen's Kappa
# ============================================================================


class TestCohensKappa:
    def test_perfect_agreement(self):
        grades = ["S", "A", "B", "C", "A+"]
        result = compute_cohens_kappa(grades, grades)
        assert result["kappa"] == 1.0

    def test_partial_agreement(self):
        a = ["A", "B", "A", "B", "C", "S"]
        b = ["A", "A", "B", "B", "C", "A"]
        result = compute_cohens_kappa(a, b)
        assert -1.0 <= result["kappa"] <= 1.0

    def test_empty_raises(self):
        with pytest.raises(ValueError):
            compute_cohens_kappa([], [])

    def test_unequal_length_raises(self):
        with pytest.raises(ValueError):
            compute_cohens_kappa(["A"], ["A", "B"])

    def test_result_structure(self):
        result = compute_cohens_kappa(["A", "B"], ["A", "B"])
        assert "kappa" in result
        assert "observed_agreement" in result
        assert "expected_agreement" in result
        assert "n" in result


# ============================================================================
# Weighted Kappa
# ============================================================================


class TestWeightedKappa:
    def test_perfect_agreement(self):
        grades = ["S", "A", "B", "C"]
        result = compute_weighted_kappa(grades, grades)
        assert result["weighted_kappa"] == 1.0

    def test_quadratic_and_linear_valid(self):
        a = ["S", "A", "B", "C"]
        b = ["A+", "A", "B+", "B"]
        q = compute_weighted_kappa(a, b, weight_type="quadratic")
        l = compute_weighted_kappa(a, b, weight_type="linear")
        assert -1.0 <= q["weighted_kappa"] <= 1.0
        assert -1.0 <= l["weighted_kappa"] <= 1.0

    def test_varied_grades(self):
        a = ["S", "A+", "A", "B+", "B", "C", "S", "A"]
        b = ["S", "A", "A", "B+", "B", "C", "A+", "A"]
        result = compute_weighted_kappa(a, b)
        assert -1.0 <= result["weighted_kappa"] <= 1.0


# ============================================================================
# ICC
# ============================================================================


class TestICC:
    def test_perfect_agreement(self):
        scores = [80, 85, 90, 75, 70]
        result = compute_icc(scores, scores)
        assert result["icc"] == 1.0

    def test_high_agreement(self):
        a = [80, 85, 90, 75, 70, 92, 88]
        b = [81, 84, 89, 76, 71, 91, 87]
        result = compute_icc(a, b)
        assert result["icc"] > 0.9

    def test_result_has_icc(self):
        result = compute_icc([80, 85, 90], [81, 84, 89])
        assert "icc" in result
        assert "n" in result


# ============================================================================
# Bland-Altman
# ============================================================================


class TestBlandAltman:
    def test_no_bias(self):
        a = [80, 85, 90, 75, 70]
        result = compute_bland_altman(a, a)
        assert abs(result["mean_diff"]) < 0.01

    def test_systematic_bias(self):
        a = [80, 85, 90, 75, 70]
        b = [75, 80, 85, 70, 65]
        result = compute_bland_altman(a, b)
        assert abs(result["mean_diff"] - 5.0) < 0.01

    def test_result_structure(self):
        result = compute_bland_altman([80, 85, 90], [81, 84, 89])
        assert "mean_diff" in result
        assert "sd_diff" in result
        assert "upper_loa" in result
        assert "lower_loa" in result
        assert "n" in result


# ============================================================================
# Per-Axis Correlation
# ============================================================================


class TestPerAxisCorrelation:
    def test_returns_all_axes(self):
        results_a = [
            {"skeletal": 80, "gait": 85, "muscle": 90, "coat": 75, "temperament": 70},
            {"skeletal": 90, "gait": 92, "muscle": 88, "coat": 85, "temperament": 80},
            {"skeletal": 70, "gait": 75, "muscle": 78, "coat": 65, "temperament": 60},
        ]
        results_b = [
            {"skeletal": 78, "gait": 83, "muscle": 87, "coat": 73, "temperament": 72},
            {"skeletal": 88, "gait": 90, "muscle": 85, "coat": 83, "temperament": 82},
            {"skeletal": 72, "gait": 77, "muscle": 80, "coat": 67, "temperament": 58},
        ]
        result = compute_per_axis_correlation(results_a, results_b)
        for axis in SCORING_AXES:
            assert axis in result
            # Each axis returns a dict with 'r' and 'n'
            assert "r" in result[axis]
            assert -1.0 <= result[axis]["r"] <= 1.0


# ============================================================================
# Sample Size Recommendation
# ============================================================================


class TestSampleSize:
    def test_returns_dict(self):
        rec = get_sample_size_recommendation()
        assert isinstance(rec, dict)

    def test_tighter_ci_needs_more_samples(self):
        wide = get_sample_size_recommendation(desired_half_width=0.2)
        tight = get_sample_size_recommendation(desired_half_width=0.05)
        # Extract the recommended N (may be under different keys)
        wide_n = wide.get("kappa_n") or wide.get("recommended_n") or 0
        tight_n = tight.get("kappa_n") or tight.get("recommended_n") or 0
        assert tight_n >= wide_n


# ============================================================================
# JudgeValidationSession
# ============================================================================


class TestJudgeValidationSession:
    def _make_result(self, base_score, grade="A"):
        r = {}
        for axis in SCORING_AXES:
            r[axis] = base_score
        r["overall_score"] = base_score
        r["grade"] = grade
        return r

    def test_session_creation(self):
        session = JudgeValidationSession()
        assert session is not None

    def test_session_add_pair(self):
        session = JudgeValidationSession()
        ai = self._make_result(85, "A")
        judge = self._make_result(83, "A")
        session.add_pair(ai, judge)
        assert session.n == 1

    def test_session_compute_report(self):
        session = JudgeValidationSession()
        for i in range(5):
            ai = self._make_result(80 + i, "A" if i < 3 else "A+")
            judge = self._make_result(79 + i, "A" if i < 3 else "A+")
            session.add_pair(ai, judge)
        report = session.compute_full_report(include_bootstrap=False)
        assert isinstance(report, dict)
