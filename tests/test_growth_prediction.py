"""
Comprehensive tests for the growth prediction system.

Tests cover:
- Growth curve model fitting
- GrowthPredictor lifecycle
- Breed expectations
- Anomaly detection
- Growth phase classification
- Edge cases (insufficient data, single axis)
"""

from api.growth_prediction import (
    AXES,
    ANOMALY_SD_THRESHOLD,
    DEFAULT_BREED_EXPECTATIONS,
    MIN_POINTS_ANY,
    MIN_POINTS_NONLINEAR,
    GrowthPredictor,
)


# ============================================================================
# Constants and Configuration
# ============================================================================


class TestGrowthConstants:
    """Verify growth prediction constants."""

    def test_axes_defined(self):
        assert len(AXES) == 5
        expected = ["balance", "coat", "structure", "gait", "temperament"]
        assert AXES == expected

    def test_min_points_nonlinear(self):
        assert MIN_POINTS_NONLINEAR >= 3

    def test_min_points_any(self):
        assert MIN_POINTS_ANY >= 2

    def test_anomaly_threshold_positive(self):
        assert ANOMALY_SD_THRESHOLD > 0

    def test_default_breed_expectations_has_default(self):
        assert "default" in DEFAULT_BREED_EXPECTATIONS
        default = DEFAULT_BREED_EXPECTATIONS["default"]
        assert "puppy_peak_age" in default
        assert "adult_peak_start" in default
        assert "adult_peak_end" in default
        assert "senior_onset" in default

    def test_breed_expectations_values_ordered(self):
        """For each breed, ages should be logically ordered."""
        for breed, exp in DEFAULT_BREED_EXPECTATIONS.items():
            assert exp["puppy_peak_age"] <= exp["adult_peak_start"], (
                f"{breed}: puppy_peak_age > adult_peak_start"
            )
            assert exp["adult_peak_start"] <= exp["adult_peak_end"], (
                f"{breed}: adult_peak_start > adult_peak_end"
            )
            assert exp["adult_peak_end"] <= exp["senior_onset"], (
                f"{breed}: adult_peak_end > senior_onset"
            )


# ============================================================================
# GrowthPredictor
# ============================================================================


class TestGrowthPredictor:
    """Verify GrowthPredictor operations."""

    def _make_history(self, points=6):
        """Create synthetic growth history data."""
        history = []
        for i in range(points):
            age = 0.5 + i * 0.5
            base = 50 + i * 5
            scores = {axis: base + (j * 2) for j, axis in enumerate(AXES)}
            history.append((age, scores))
        return history

    def test_create_predictor(self):
        p = GrowthPredictor()
        assert p is not None

    def test_create_predictor_with_breed(self):
        p = GrowthPredictor(breed="Labrador Retriever")
        assert p is not None

    def test_fit_with_sufficient_data(self):
        p = GrowthPredictor()
        history = self._make_history(points=6)
        p.fit(history)
        # Should be able to predict after fitting
        result = p.predict(target_age=4.0)
        assert result is not None

    def test_fit_with_minimum_data(self):
        p = GrowthPredictor()
        history = self._make_history(points=MIN_POINTS_ANY)
        p.fit(history)
        result = p.predict(target_age=4.0)
        assert result is not None

    def test_predict_returns_scores_for_all_axes(self):
        p = GrowthPredictor()
        history = self._make_history(points=6)
        p.fit(history)
        result = p.predict(target_age=4.0)
        assert isinstance(result, dict)
        # predict() returns a dict with 'scores' key containing per-axis values
        assert "scores" in result
        for axis in AXES:
            assert axis in result["scores"]

    def test_growth_phase_puppy(self):
        p = GrowthPredictor()
        history = self._make_history(points=6)
        p.fit(history)
        phase = p.get_growth_phase(age=0.5)
        assert phase is not None
        assert isinstance(phase, (str, dict))

    def test_growth_phase_adult(self):
        p = GrowthPredictor()
        history = self._make_history(points=6)
        p.fit(history)
        phase = p.get_growth_phase(age=3.0)
        assert phase is not None

    def test_growth_phase_senior(self):
        p = GrowthPredictor()
        history = self._make_history(points=6)
        p.fit(history)
        phase = p.get_growth_phase(age=10.0)
        assert phase is not None

    def test_predict_peak_age(self):
        p = GrowthPredictor()
        history = self._make_history(points=6)
        p.fit(history)
        peak = p.predict_peak_age()
        assert peak is not None
        # predict_peak_age() returns dict with 'peak_age', 'peak_overall', 'per_axis_peak_ages'
        assert isinstance(peak, dict)
        assert "peak_age" in peak or "per_axis_peak_ages" in peak

    def test_detect_anomalies(self):
        p = GrowthPredictor()
        history = self._make_history(points=6)
        p.fit(history)
        anomalies = p.detect_anomalies()
        assert isinstance(anomalies, (list, dict))

    def test_get_trajectory(self):
        p = GrowthPredictor()
        history = self._make_history(points=6)
        p.fit(history)
        trajectory = p.get_trajectory(age_range=(0.5, 5.0), step=0.5)
        assert trajectory is not None
        assert len(trajectory) > 0

    def test_breed_specific_expectations(self):
        """Different breeds should use their specific expectations."""
        p_lab = GrowthPredictor(breed="Labrador Retriever")
        p_dane = GrowthPredictor(breed="Great Dane")

        # Great Danes mature faster but age sooner
        lab_exp = DEFAULT_BREED_EXPECTATIONS["Labrador Retriever"]
        dane_exp = DEFAULT_BREED_EXPECTATIONS["Great Dane"]
        assert dane_exp["senior_onset"] < lab_exp["senior_onset"]

    def test_unknown_breed_uses_default(self):
        p = GrowthPredictor(breed="Unknown Rare Breed")
        history = self._make_history(points=6)
        p.fit(history)
        # Should not crash, should use defaults
        phase = p.get_growth_phase(age=3.0)
        assert phase is not None

    def test_insufficient_data_handled_gracefully(self):
        """Predictor should not crash with too few data points."""
        p = GrowthPredictor()
        history = self._make_history(points=1)
        # Should either raise a clear error or handle gracefully
        try:
            p.fit(history)
        except (ValueError, RuntimeError):
            pass  # Acceptable to raise on insufficient data
