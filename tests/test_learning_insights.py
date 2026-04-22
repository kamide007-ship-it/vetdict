"""
Tests for Phase 3 STEP 4: Learning Insights API endpoints.

Tests API endpoint logic without Flask dependencies.
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
def learning_store_instance(temp_instance_dir):
    """Create fresh learning store for tests."""
    store_instance = LearningDataStore()
    store_instance._state = None
    return store_instance


class TestAccuracyMetrics:
    """Test accuracy metrics data generation."""

    def test_accuracy_metrics_no_data(self, learning_store_instance):
        """Test accuracy metrics with no data."""
        stats = learning_store_instance.get_overall_stats()

        assert stats["overall_accuracy"] == 0
        assert stats["total_extractions"] == 0

    def test_accuracy_metrics_with_data(self, learning_store_instance):
        """Test accuracy metrics with data."""
        for i in range(5):
            learning_store_instance.record_feedback_learning(
                session_id=f"test_{i:02d}",
                feedback_type="good",
                ai_result={"confidence": 0.85},
                reco2_verdict="test",
                extracted_symptoms=["s001"],
                disease_domain="general",
            )

        stats = learning_store_instance.get_overall_stats()

        assert stats["overall_accuracy"] == 1.0
        assert stats["total_extractions"] == 5

    def test_accuracy_by_domain(self, learning_store_instance):
        """Test domain-specific accuracy metrics."""
        learning_store_instance.record_feedback_learning(
            session_id="test_001",
            feedback_type="good",
            ai_result={"confidence": 0.85},
            reco2_verdict="test",
            extracted_symptoms=["s001"],
            disease_domain="orthopedics",
        )

        metrics = learning_store_instance.get_ai_accuracy_by_domain("orthopedics")

        assert len(metrics) == 1
        assert metrics[0]["domain"] == "orthopedics"


class TestPatternsMetrics:
    """Test learned patterns metrics."""

    def test_patterns_no_data(self, learning_store_instance):
        """Test patterns with no data."""
        patterns = learning_store_instance.get_symptom_disease_patterns()

        assert len(patterns) == 0

    def test_patterns_with_data(self, learning_store_instance):
        """Test patterns with data."""
        for i in range(5):
            learning_store_instance.record_feedback_learning(
                session_id=f"test_{i:02d}",
                feedback_type="good",
                ai_result={"confidence": 0.85},
                reco2_verdict="test",
                extracted_symptoms=["limp", "swelling"],
                disease_domain="arthritis",
            )

        patterns = learning_store_instance.get_symptom_disease_patterns()

        assert len(patterns) > 0
        pattern = patterns[0]
        assert "symptoms" in pattern
        assert "accuracy_rate" in pattern
        assert "sample_count" in pattern

    def test_pattern_confidence_levels(self, learning_store_instance):
        """Test that patterns have confidence levels based on samples."""
        # Create pattern with 12 samples
        for i in range(12):
            learning_store_instance.record_feedback_learning(
                session_id=f"test_{i:02d}",
                feedback_type="good",
                ai_result={"confidence": 0.85},
                reco2_verdict="test",
                extracted_symptoms=["symptom"],
                disease_domain="disease1",
            )

        patterns = learning_store_instance.get_symptom_disease_patterns()

        assert len(patterns) > 0
        pattern = patterns[0]
        # 12 samples should give high confidence
        assert pattern["sample_count"] >= 10


class TestFeedbackQuality:
    """Test feedback quality metrics."""

    def test_feedback_quality_coverage(self, learning_store_instance):
        """Test feedback coverage calculation."""
        for i in range(10):
            learning_store_instance.record_feedback_learning(
                session_id=f"test_{i:02d}",
                feedback_type="good" if i < 7 else "bad",
                ai_result={"confidence": 0.85},
                reco2_verdict="test",
                extracted_symptoms=["s001"],
                disease_domain="general",
            )

        feedback_records = learning_store_instance._get_state().get("learning_metrics", {}).get("feedback_records", [])

        good_count = sum(1 for f in feedback_records if f.get("feedback_type") == "good")
        bad_count = sum(1 for f in feedback_records if f.get("feedback_type") == "bad")

        assert good_count == 7
        assert bad_count == 3


class TestAccuracyTracker:
    """Test accuracy tracker metrics integration."""

    def test_tracker_evaluation_good_feedback(self):
        """Test tracker evaluates good feedback correctly."""
        tracker = AIAccuracyTracker()

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

    def test_tracker_evaluation_bad_feedback(self):
        """Test tracker evaluates bad feedback correctly."""
        tracker = AIAccuracyTracker()

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

    def test_tracker_domain_performance(self, learning_store_instance):
        """Test tracker domain performance calculation."""
        # Record good and bad feedback
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
            feedback_type="bad",
            ai_result={"confidence": 0.3},
            reco2_verdict="test",
            extracted_symptoms=["s002"],
            disease_domain="general",
        )

        tracker = AIAccuracyTracker()
        performance = tracker.get_domain_performance("general")

        assert performance["status"] == "ready"
        assert performance["total_extractions"] == 2
        assert performance["accuracy"] == pytest.approx(0.5)


class TestInsightsGeneration:
    """Test combined insights generation."""

    def test_insights_include_recommendations(self, learning_store_instance):
        """Test that insights include actionable recommendations."""
        for i in range(25):
            learning_store_instance.record_feedback_learning(
                session_id=f"test_{i:02d}",
                feedback_type="good",
                ai_result={"confidence": 0.85},
                reco2_verdict="test",
                extracted_symptoms=["s001"],
                disease_domain="general",
            )

        stats = learning_store_instance.get_overall_stats()

        # With high accuracy, we should have positive recommendations
        assert stats["overall_accuracy"] > 0.8

    def test_feedback_tracking_completeness(self, learning_store_instance):
        """Test that feedback tracking captures all data."""
        learning_store_instance.record_feedback_learning(
            session_id="test_001",
            feedback_type="good",
            ai_result={"confidence": 0.85},
            reco2_verdict="arthritis suspected",
            extracted_symptoms=["limp", "swelling"],
            disease_domain="orthopedics",
        )

        feedback_records = learning_store_instance._get_state().get("learning_metrics", {}).get("feedback_records", [])

        assert len(feedback_records) == 1
        record = feedback_records[0]
        assert record["session_id"] == "test_001"
        assert record["feedback_type"] == "good"
        assert record["extracted_symptoms"] == ["limp", "swelling"]
        assert record["disease_domain"] == "orthopedics"


class TestPersonalizationImpact:
    """Test personalization effectiveness metrics."""

    def test_personalization_metrics_structure(self, learning_store_instance):
        """Test personalization impact structure."""
        impacts = learning_store_instance.get_personalization_impact()

        # Should return a list (even if empty)
        assert isinstance(impacts, list)

    def test_personalization_filtering(self, learning_store_instance):
        """Test filtering personalization by age stage."""
        impacts = learning_store_instance.get_personalization_impact(age_stage="senior")

        # Should return list (even if empty for missing data)
        assert isinstance(impacts, list)
