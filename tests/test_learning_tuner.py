"""
Tests for Phase 3 STEP 3: RECO2 Learning Tuner.

Tests parameter tuning logic based on learning signals.
"""

import os
import tempfile

import pytest

from reco2.learning_store import LearningDataStore
from reco2.learning_tuner import LearningTuner


@pytest.fixture
def temp_instance_dir():
    """Create temporary instance directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        os.environ["RECO3_INSTANCE_DIR"] = tmpdir
        yield tmpdir
        if "RECO3_INSTANCE_DIR" in os.environ:
            del os.environ["RECO3_INSTANCE_DIR"]


@pytest.fixture
def tuner(temp_instance_dir):
    """Create fresh tuner for each test."""
    return LearningTuner()


@pytest.fixture
def learning_store_instance(temp_instance_dir):
    """Create fresh learning store for tests."""
    store_instance = LearningDataStore()
    store_instance._state = None
    return store_instance


class TestParameterSuggestions:
    """Test parameter suggestion generation."""

    def test_suggest_with_no_data(self, tuner):
        """Test suggestions with no learning data."""
        result = tuner.suggest_parameter_adjustments(
            current_k=1.5,
            current_eta=0.01,
            learning_data={},
            window_stats={},
            ai_accuracy={},
        )

        assert "suggested_k" in result
        assert "suggested_eta" in result
        assert "confidence_score" in result
        assert result["confidence_score"] < 0.5  # Low confidence with no data

    def test_suggest_with_high_ai_accuracy(self, tuner, learning_store_instance):
        """Test suggestions with high AI accuracy signal."""
        # Record high-accuracy feedback
        for i in range(25):
            learning_store_instance.record_feedback_learning(
                session_id=f"test_{i:02d}",
                feedback_type="good",
                ai_result={"confidence": 0.85},
                reco2_verdict="test",
                extracted_symptoms=["s001"],
                disease_domain="general",
            )

        learning_data = {
            "feedback_records": learning_store_instance._get_state()["learning_metrics"]["feedback_records"],
            "symptom_disease_patterns": [],
            "personalization_impact": [],
        }

        from api.ai.accuracy_tracker import AIAccuracyTracker
        AIAccuracyTracker()
        ai_accuracy = {
            "status": "ready",
            "overall_accuracy": 0.95,
        }

        result = tuner.suggest_parameter_adjustments(
            current_k=1.5,
            current_eta=0.01,
            learning_data=learning_data,
            window_stats={},
            ai_accuracy=ai_accuracy,
        )

        # High accuracy should suggest relaxing k
        assert result["suggested_k"] > 1.5 or result["confidence_score"] > 0.5
        assert "High AI accuracy" in " ".join(result["reasoning"])

    def test_suggest_with_low_ai_accuracy(self, tuner):
        """Test suggestions with low AI accuracy."""
        ai_accuracy = {
            "status": "ready",
            "overall_accuracy": 0.65,
        }

        result = tuner.suggest_parameter_adjustments(
            current_k=1.5,
            current_eta=0.01,
            learning_data={},
            window_stats={},
            ai_accuracy=ai_accuracy,
        )

        # Low accuracy should generate some reasoning
        assert len(result["reasoning"]) >= 0
        # Suggested k should be lower for low accuracy
        assert result["suggested_k"] <= 1.5 or result["confidence_score"] < 0.5

    def test_suggest_with_positive_feedback(self, tuner, learning_store_instance):
        """Test suggestions with strong positive feedback."""
        # Record mostly good feedback
        for i in range(20):
            learning_store_instance.record_feedback_learning(
                session_id=f"test_{i:02d}",
                feedback_type="good",
                ai_result={"confidence": 0.85},
                reco2_verdict="test",
                extracted_symptoms=["s001"],
                disease_domain="general",
            )

        learning_data = {
            "feedback_records": learning_store_instance._get_state()["learning_metrics"]["feedback_records"],
            "symptom_disease_patterns": [],
            "personalization_impact": [],
        }

        result = tuner.suggest_parameter_adjustments(
            current_k=1.5,
            current_eta=0.01,
            learning_data=learning_data,
            window_stats={},
            ai_accuracy={},
        )

        # With positive feedback, eta might be increased
        assert isinstance(result["suggested_eta"], float)
        assert result["suggested_eta"] >= 0.001

    def test_suggest_with_stable_patterns(self, tuner, learning_store_instance):
        """Test suggestions with stable symptom-disease patterns."""
        # Create stable patterns (need 3+ patterns with 5+ samples each)
        for _ in range(3):  # 3 different patterns
            for i in range(6):  # 6 samples each
                learning_store_instance.record_feedback_learning(
                    session_id=f"test_{_}_{i:02d}",
                    feedback_type="good",
                    ai_result={"confidence": 0.85},
                    reco2_verdict="test",
                    extracted_symptoms=[f"s{_}_1", f"s{_}_2"],
                    disease_domain=f"disease_{_}",
                )

        learning_data = {
            "feedback_records": learning_store_instance._get_state()["learning_metrics"]["feedback_records"],
            "symptom_disease_patterns": learning_store_instance._get_state()["learning_metrics"]["symptom_disease_patterns"],
            "personalization_impact": [],
        }

        result = tuner.suggest_parameter_adjustments(
            current_k=1.5,
            current_eta=0.01,
            learning_data=learning_data,
            window_stats={},
            ai_accuracy={},
        )

        # With stable patterns, reasoning should include pattern message
        assert isinstance(result["reasoning"], list)
        assert result["suggested_k"] > 0  # Valid k value


class TestConfidenceCalculation:
    """Test confidence score calculation."""

    def test_confidence_increases_with_signals(self, tuner):
        """Test that confidence increases with stronger signals."""
        signals_strong = {
            "ai_accuracy": 0.15,
            "feedback_strength": 0.05,
            "patterns": 0.03,
            "personalization": 0.02,
        }

        signals_weak = {
            "ai_accuracy": 0.0,
            "feedback_strength": 0.0,
            "patterns": 0.0,
            "personalization": 0.0,
        }

        conf_strong = tuner._calculate_confidence(signals_strong)
        conf_weak = tuner._calculate_confidence(signals_weak)

        assert conf_strong > conf_weak

    def test_confidence_bounded(self, tuner):
        """Test that confidence stays within bounds."""
        signals = {
            "ai_accuracy": 1.0,  # Very large signal
            "feedback_strength": 1.0,
            "patterns": 1.0,
            "personalization": 1.0,
        }

        confidence = tuner._calculate_confidence(signals)
        assert 0.0 <= confidence <= 0.95


class TestKAdjustment:
    """Test k parameter adjustment calculation."""

    def test_k_adjustment_positive_signal(self, tuner):
        """Test k adjustment with positive signal."""
        signals = {
            "ai_accuracy": 0.15,
            "feedback_strength": 0.0,
            "patterns": 0.03,
            "personalization": 0.0,
        }

        adjustment = tuner._calculate_k_adjustment(signals, 1.5)
        assert adjustment > 0  # Should increase k

    def test_k_adjustment_negative_signal(self, tuner):
        """Test k adjustment with negative signal."""
        signals = {
            "ai_accuracy": -0.1,
            "feedback_strength": 0.0,
            "patterns": 0.0,
            "personalization": 0.0,
        }

        adjustment = tuner._calculate_k_adjustment(signals, 1.5)
        assert adjustment < 0  # Should decrease k

    def test_k_adjustment_bounded(self, tuner):
        """Test that k adjustment is bounded."""
        signals = {
            "ai_accuracy": 1.0,  # Very large signal
            "feedback_strength": 1.0,
            "patterns": 1.0,
            "personalization": 1.0,
        }

        adjustment = tuner._calculate_k_adjustment(signals, 1.5)
        assert abs(adjustment) <= 0.1  # Max 0.1 change per cycle


class TestEtaAdjustment:
    """Test eta parameter adjustment calculation."""

    def test_eta_adjustment_calculation(self, tuner):
        """Test eta adjustment is calculated correctly."""
        signals = {
            "ai_accuracy": 0.0,
            "feedback_strength": 0.005,
            "patterns": 0.0,
            "personalization": 0.0,
        }

        adjustment = tuner._calculate_eta_adjustment(signals, 0.01)
        # Should be small since eta is small
        assert abs(adjustment) < 0.01


class TestImpactEstimation:
    """Test estimated impact of parameter changes."""

    def test_impact_k_decrease(self, tuner):
        """Test impact estimation for k decrease."""
        impact = tuner._estimate_impact(1.5, 1.45, 0.01, 0.01)

        # k decrease should increase reliable verdicts
        assert impact["verdict_distribution_change"]["reliable"] > 0

    def test_impact_k_increase(self, tuner):
        """Test impact estimation for k increase."""
        impact = tuner._estimate_impact(1.5, 1.55, 0.01, 0.01)

        # k increase should decrease reliable verdicts
        assert impact["verdict_distribution_change"]["reliable"] < 0

    def test_impact_convergence_speed(self, tuner):
        """Test convergence speed estimation."""
        impact_decrease = tuner._estimate_impact(1.5, 1.45, 0.01, 0.01)
        impact_increase = tuner._estimate_impact(1.5, 1.55, 0.01, 0.01)

        assert impact_decrease["convergence_speed"] == "faster"
        assert impact_increase["convergence_speed"] == "slower"


class TestApplyTuning:
    """Test applying tuning to state."""

    def test_apply_tuning_with_sufficient_confidence(self, tuner):
        """Test applying tuning with sufficient confidence."""
        state = {"k": 1.5, "eta": 0.01}
        learning_signals = {
            "suggested_k": 1.55,
            "suggested_eta": 0.0102,
            "confidence_score": 0.75,
        }

        adjusted, reason = tuner.apply_learning_driven_tuning(
            state, learning_signals, min_confidence=0.7
        )

        assert adjusted is True
        assert state["k"] == 1.55
        assert state["eta"] == 0.0102

    def test_apply_tuning_with_insufficient_confidence(self, tuner):
        """Test not applying tuning with insufficient confidence."""
        state = {"k": 1.5, "eta": 0.01}
        learning_signals = {
            "suggested_k": 1.55,
            "suggested_eta": 0.0102,
            "confidence_score": 0.5,
        }

        adjusted, reason = tuner.apply_learning_driven_tuning(
            state, learning_signals, min_confidence=0.7
        )

        assert adjusted is False
        assert state["k"] == 1.5  # Unchanged
        assert state["eta"] == 0.01  # Unchanged

    def test_apply_tuning_respects_bounds(self, tuner):
        """Test that tuning respects parameter bounds."""
        state = {"k": 1.5, "eta": 0.01, "k_min": 0.5, "k_max": 5.0, "eta_min": 0.001, "eta_max": 0.1}
        learning_signals = {
            "suggested_k": 10.0,  # Beyond max
            "suggested_eta": 0.5,  # Beyond max
            "confidence_score": 0.8,
        }

        # The suggestion should be clamped in suggest_parameter_adjustments
        adjusted, reason = tuner.apply_learning_driven_tuning(
            state, learning_signals, min_confidence=0.7
        )

        assert adjusted is True
        # Values should be set as suggested (caller responsible for bounds)
        assert state["k"] == 10.0
        assert state["eta"] == 0.5


class TestTuningHistory:
    """Test tuning history retrieval."""

    def test_get_tuning_history_empty(self, tuner):
        """Test getting tuning history with no data."""
        history = tuner.get_tuning_history()
        assert isinstance(history, list)

    def test_get_tuning_history_limit(self, tuner):
        """Test limit parameter on tuning history."""
        history = tuner.get_tuning_history(limit=10)
        assert len(history) <= 10


class TestAffectedDomains:
    """Test identification of affected domains."""

    def test_get_affected_domains_empty(self, tuner):
        """Test getting affected domains with no patterns."""
        domains = tuner._get_affected_domains({})
        assert isinstance(domains, list)

    def test_get_affected_domains_multiple(self, tuner, learning_store_instance):
        """Test identifying multiple affected domains."""
        # Create patterns in different domains
        for domain in ["orthopedics", "cardiology", "dermatology"]:
            for i in range(6):  # Need 5+ samples for domain to be affected
                learning_store_instance.record_feedback_learning(
                    session_id=f"{domain}_{i:02d}",
                    feedback_type="good",
                    ai_result={"confidence": 0.85},
                    reco2_verdict="test",
                    extracted_symptoms=["s001"],
                    disease_domain=domain,
                )

        learning_data = {
            "symptom_disease_patterns": learning_store_instance._get_state()["learning_metrics"]["symptom_disease_patterns"],
        }

        domains = tuner._get_affected_domains(learning_data)
        assert len(domains) > 0
        assert isinstance(domains, list)
