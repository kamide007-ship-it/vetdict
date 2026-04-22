"""
Tests for Phase 3 STEP 2: AI Accuracy Tracker.

Tests extraction evaluation, accuracy measurement, and confidence tracking.
"""

import os
import tempfile

import pytest

from api.ai.accuracy_tracker import AIAccuracyTracker
from reco2.learning_store import LearningDataStore


@pytest.fixture
def temp_instance_dir():
    """Create temporary instance directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        os.environ["RECO3_INSTANCE_DIR"] = tmpdir
        yield tmpdir
        if "RECO3_INSTANCE_DIR" in os.environ:
            del os.environ["RECO3_INSTANCE_DIR"]


@pytest.fixture
def tracker(temp_instance_dir):
    """Create fresh accuracy tracker for each test."""
    return AIAccuracyTracker()


@pytest.fixture
def learning_store_instance(temp_instance_dir):
    """Create fresh learning store for tests."""
    store_instance = LearningDataStore()
    store_instance._state = None
    return store_instance


class TestExtractionEvaluation:
    """Test extraction accuracy evaluation."""

    def test_evaluate_good_feedback(self, tracker):
        """Test evaluation with good feedback."""
        ai_result = {
            "symptoms": ["s001", "s002"],
            "confidence": 0.85,
        }

        result = tracker.evaluate_extraction(
            ai_result=ai_result,
            feedback_type="good",
            domain="general",
        )

        assert result["accuracy_score"] == 1.0
        assert result["is_correct"] is True
        assert result["ai_confidence"] == 0.85

    def test_evaluate_bad_feedback(self, tracker):
        """Test evaluation with bad feedback."""
        ai_result = {
            "symptoms": ["s001"],
            "confidence": 0.3,
        }

        result = tracker.evaluate_extraction(
            ai_result=ai_result,
            feedback_type="bad",
            domain="general",
        )

        assert result["accuracy_score"] == 0.0
        assert result["is_correct"] is False

    def test_evaluate_with_ground_truth(self, tracker):
        """Test evaluation with ground truth symptoms."""
        ai_result = {
            "symptoms": ["s001", "s002", "s003"],  # s003 is wrong
            "confidence": 0.85,
        }
        correct_symptoms = ["s001", "s002"]

        result = tracker.evaluate_extraction(
            ai_result=ai_result,
            feedback_type="good",
            correct_symptoms=correct_symptoms,
            domain="general",
        )

        assert "s003" in result["false_positives"]
        assert len(result["false_negatives"]) == 0
        assert result["accuracy_score"] > 0  # Partial credit for correct ones

    def test_evaluate_with_missing_symptoms(self, tracker):
        """Test evaluation when symptoms are missed."""
        ai_result = {
            "symptoms": ["s001"],  # s002 was missed
            "confidence": 0.85,
        }
        correct_symptoms = ["s001", "s002"]

        result = tracker.evaluate_extraction(
            ai_result=ai_result,
            feedback_type="good",
            correct_symptoms=correct_symptoms,
            domain="general",
        )

        assert "s002" in result["false_negatives"]
        assert len(result["false_positives"]) == 0

    def test_evaluate_personalization_impact(self, tracker):
        """Test personalization impact tracking."""
        ai_result = {
            "symptoms": ["s001"],
            "confidence": 0.85,
            "personalization": {
                "age_boost": 0.05,
                "severity_adjustment": 0.1,
            },
        }

        result = tracker.evaluate_extraction(
            ai_result=ai_result,
            feedback_type="good",
            domain="general",
        )

        assert result["personalization_impact"]["age_boost_effective"] is True
        assert result["personalization_impact"]["severity_factor_helped"] is True

    def test_evaluate_personalization_not_helpful(self, tracker):
        """Test when personalization doesn't help."""
        ai_result = {
            "symptoms": ["s001"],
            "confidence": 0.85,
            "personalization": {
                "age_boost": 0.05,
                "severity_adjustment": 0.1,
            },
        }

        result = tracker.evaluate_extraction(
            ai_result=ai_result,
            feedback_type="bad",  # But feedback is bad
            domain="general",
        )

        assert result["personalization_impact"]["age_boost_effective"] is False
        assert result["personalization_impact"]["severity_factor_helped"] is False


class TestCalibrationCurve:
    """Test confidence calibration curve calculation."""

    def test_calibration_curve_no_data(self, tracker):
        """Test calibration curve with no data."""
        result = tracker.get_calibration_curve(domain="nonexistent")

        assert result["status"] == "insufficient_data"
        assert result["overall_calibration"] == 0.0

    def test_calibration_curve_insufficient_samples(self, tracker, learning_store_instance):
        """Test calibration curve with insufficient samples."""
        # Record only 5 feedback entries
        for i in range(5):
            learning_store_instance.record_feedback_learning(
                session_id=f"test_{i:02d}",
                feedback_type="good",
                ai_result={"confidence": 0.85},
                reco2_verdict="test",
                extracted_symptoms=["s001"],
                disease_domain="general",
            )

        result = tracker.get_calibration_curve(domain="general", min_samples=20)
        assert result["status"] == "insufficient_data"

    def test_calibration_curve_ready(self, tracker, learning_store_instance):
        """Test calibration curve with sufficient data."""
        # Record 25 good feedback entries
        for i in range(25):
            learning_store_instance.record_feedback_learning(
                session_id=f"test_{i:02d}",
                feedback_type="good",
                ai_result={"confidence": 0.85},
                reco2_verdict="test",
                extracted_symptoms=["s001"],
                disease_domain="general",
            )

        result = tracker.get_calibration_curve(domain="general", min_samples=20)
        assert result["status"] == "ready"
        assert "general" in result["domains"]
        assert result["overall_calibration"] > 0


class TestExtractionMetricsBySymptom:
    """Test per-symptom extraction metrics."""

    def test_get_metrics_no_data(self, tracker):
        """Test metrics retrieval with no data."""
        result = tracker.get_extraction_metrics_by_symptom("nonexistent")

        assert result["status"] == "no_data"
        assert len(result["patterns"]) == 0

    def test_get_metrics_with_patterns(self, tracker, learning_store_instance):
        """Test metrics retrieval with learned patterns."""
        # Create patterns
        learning_store_instance.record_feedback_learning(
            session_id="test_001",
            feedback_type="good",
            ai_result={"confidence": 0.85},
            reco2_verdict="test",
            extracted_symptoms=["s001", "s002"],
            disease_domain="arthritis",
        )

        result = tracker.get_extraction_metrics_by_symptom("s001")
        assert result["status"] == "ready"
        assert len(result["patterns"]) > 0
        assert result["overall_accuracy"] > 0


class TestDomainPerformance:
    """Test domain-level performance metrics."""

    def test_get_domain_performance_no_data(self, tracker):
        """Test domain performance with no data."""
        result = tracker.get_domain_performance("nonexistent")

        assert result["status"] == "no_data"

    def test_get_domain_performance_ready(self, tracker, learning_store_instance):
        """Test domain performance with data."""
        # Record some feedback
        learning_store_instance.record_feedback_learning(
            session_id="test_001",
            feedback_type="good",
            ai_result={"confidence": 0.85},
            reco2_verdict="test",
            extracted_symptoms=["s001"],
            disease_domain="orthopedics",
        )

        result = tracker.get_domain_performance("orthopedics")
        assert result["status"] == "ready"
        assert result["total_extractions"] == 1
        assert result["accuracy"] == 1.0
        assert result["domain"] == "orthopedics"

    def test_domain_accuracy_calculation(self, tracker, learning_store_instance):
        """Test accuracy calculation for domain."""
        # 2 good, 1 bad
        learning_store_instance.record_feedback_learning(
            session_id="test_001",
            feedback_type="good",
            ai_result={"confidence": 0.85},
            reco2_verdict="test",
            extracted_symptoms=["s001"],
            disease_domain="general",
        )
        learning_store_instance.record_feedback_learning(
            session_id="test_002",
            feedback_type="good",
            ai_result={"confidence": 0.85},
            reco2_verdict="test",
            extracted_symptoms=["s002"],
            disease_domain="general",
        )
        learning_store_instance.record_feedback_learning(
            session_id="test_003",
            feedback_type="bad",
            ai_result={"confidence": 0.3},
            reco2_verdict="test",
            extracted_symptoms=["s003"],
            disease_domain="general",
        )

        result = tracker.get_domain_performance("general")
        assert result["total_extractions"] == 3
        assert result["accuracy"] == pytest.approx(2.0 / 3.0)
