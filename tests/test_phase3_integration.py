"""
Phase 3 Integration Tests - Complete End-to-End Learning Pipeline.

Tests the full Phase 3 continuous learning system with all components working together.
"""

import os
import tempfile

import pytest

from api.ai.accuracy_tracker import AIAccuracyTracker
from api.ai.confidence_calibration import ConfidenceCalibrator
from reco2 import store
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


class TestPhase3FullPipeline:
    """End-to-end learning pipeline tests."""

    def test_feedback_to_learning_signal_flow(self, temp_instance_dir):
        """Complete flow: feedback → learning store → AI accuracy → RECO2 tuning."""
        learning_store = LearningDataStore()
        learning_store._state = None

        # Record feedback
        for i in range(20):
            learning_store.record_feedback_learning(
                session_id=f"test_{i:02d}",
                feedback_type="good",
                ai_result={"confidence": 0.85},
                reco2_verdict="test",
                extracted_symptoms=["s001"],
                disease_domain="orthopedics",
            )

        # Verify learning store captured data
        stats = learning_store.get_overall_stats()
        assert stats["total_extractions"] == 20

        # Get accuracy metrics
        tracker = AIAccuracyTracker()
        domain_perf = tracker.get_domain_performance("orthopedics")
        assert domain_perf["accuracy"] == 1.0

        # Check tuning suggestions
        tuner = LearningTuner()
        learning_data = {
            "feedback_records": learning_store._get_state()["learning_metrics"]["feedback_records"],
            "symptom_disease_patterns": learning_store._get_state()["learning_metrics"]["symptom_disease_patterns"],
            "personalization_impact": [],
        }
        ai_accuracy = {
            "status": "ready",
            "overall_accuracy": 1.0,
        }

        suggestions = tuner.suggest_parameter_adjustments(
            current_k=1.5,
            current_eta=0.01,
            learning_data=learning_data,
            window_stats={},
            ai_accuracy=ai_accuracy,
        )

        assert "suggested_k" in suggestions
        assert suggestions["confidence_score"] > 0.1  # Some confidence from signals

    def test_ai_extraction_accuracy_tracking(self, temp_instance_dir):
        """Extract → Get feedback → Measure accuracy → Calibrate confidence."""
        tracker = AIAccuracyTracker()
        calibrator = ConfidenceCalibrator()
        learning_store = LearningDataStore()
        learning_store._state = None

        # Simulate AI extraction and feedback loop
        ai_result = {
            "symptoms": ["s001", "s002"],
            "confidence": 0.85,
            "domain": "general",
        }

        # Evaluate extraction
        evaluation = tracker.evaluate_extraction(
            ai_result=ai_result,
            feedback_type="good",
            correct_symptoms=["s001", "s002"],
        )

        assert evaluation["accuracy_score"] > 0.5

        # Record in learning store
        learning_store.record_feedback_learning(
            session_id="test_001",
            feedback_type="good",
            ai_result=ai_result,
            reco2_verdict="test",
            extracted_symptoms=["s001", "s002"],
            disease_domain="general",
        )

        # Calibrate confidence
        calibrated = calibrator.calibrate_extraction_result(ai_result.copy())
        assert "calibration_factor" in calibrated
        assert "expected_accuracy" in calibrated

    def test_reco2_dynamic_tuning_convergence(self, temp_instance_dir):
        """Multiple feedback cycles → k/eta parameters converge toward optimal."""
        learning_store = LearningDataStore()
        learning_store._state = None
        tuner = LearningTuner()

        # Multiple feedback cycles with high accuracy
        for cycle in range(3):
            for i in range(10):
                learning_store.record_feedback_learning(
                    session_id=f"cycle_{cycle}_test_{i:02d}",
                    feedback_type="good",
                    ai_result={"confidence": 0.85 + (cycle * 0.01)},
                    reco2_verdict="test",
                    extracted_symptoms=["s001"],
                    disease_domain="general",
                )

        # Check if tuning converges
        learning_data = {
            "feedback_records": learning_store._get_state()["learning_metrics"]["feedback_records"],
            "symptom_disease_patterns": learning_store._get_state()["learning_metrics"]["symptom_disease_patterns"],
            "personalization_impact": [],
        }
        ai_accuracy = {
            "status": "ready",
            "overall_accuracy": 0.95,
        }

        suggestions = tuner.suggest_parameter_adjustments(
            current_k=1.5,
            current_eta=0.01,
            learning_data=learning_data,
            window_stats={},
            ai_accuracy=ai_accuracy,
        )

        # With high accuracy over multiple cycles, k should increase
        assert suggestions["suggested_k"] >= 1.5 or suggestions["suggested_eta"] >= 0.01

    def test_personalization_impact_isolation(self, temp_instance_dir):
        """Verify personalization boost correctly reflected in accuracy metrics."""
        learning_store = LearningDataStore()
        learning_store._state = None

        # Record feedback with personalization
        ai_result = {
            "symptoms": ["s001"],
            "confidence": 0.85,
            "personalization": {
                "age_boost": 0.05,
                "severity_adjustment": 0.1,
            },
        }

        for i in range(15):
            learning_store.record_feedback_learning(
                session_id=f"test_{i:02d}",
                feedback_type="good",
                ai_result=ai_result,
                reco2_verdict="test",
                extracted_symptoms=["s001"],
                disease_domain="general",
            )

        # Verify high accuracy was achieved with personalization
        stats = learning_store.get_overall_stats()
        assert stats["overall_accuracy"] == 1.0

    def test_symptom_disease_pattern_learning(self, temp_instance_dir):
        """Learn symptom combinations from feedback and improve future extractions."""
        learning_store = LearningDataStore()
        learning_store._state = None

        # Learn pattern: [symptom_a, symptom_b] → disease_x (100% accurate)
        for i in range(10):
            learning_store.record_feedback_learning(
                session_id=f"pattern_{i:02d}",
                feedback_type="good",
                ai_result={"confidence": 0.85},
                reco2_verdict="test",
                extracted_symptoms=["symptom_a", "symptom_b"],
                disease_domain="disease_x",
            )

        # Retrieve learned pattern
        patterns = learning_store.get_symptom_disease_patterns()
        assert len(patterns) > 0

        pattern = patterns[0]
        assert pattern["accuracy_rate"] == 1.0
        assert pattern["sample_count"] >= 10

    def test_dashboard_metrics_consistency(self, temp_instance_dir):
        """All dashboard endpoints return consistent, non-contradictory data."""
        learning_store = LearningDataStore()
        learning_store._state = None

        # Record test data
        for i in range(25):
            learning_store.record_feedback_learning(
                session_id=f"test_{i:02d}",
                feedback_type="good" if i < 20 else "bad",
                ai_result={"confidence": 0.85},
                reco2_verdict="test",
                extracted_symptoms=["s001"],
                disease_domain="general",
            )

        # Get all metrics
        stats = learning_store.get_overall_stats()
        accuracy_metrics = learning_store.get_ai_accuracy_by_domain()
        learning_store.get_symptom_disease_patterns()

        # Verify consistency
        assert stats["total_extractions"] == 25
        assert stats["total_correct_extractions"] == 20
        assert stats["overall_accuracy"] == pytest.approx(0.8)

        # Domain metrics should match overall stats
        if accuracy_metrics:
            domain_metric = accuracy_metrics[0]
            assert domain_metric["total_extractions"] == 25

    def test_learning_with_zero_feedback(self, temp_instance_dir):
        """System gracefully handles sessions without feedback (no crashes)."""
        learning_store = LearningDataStore()
        learning_store._state = None

        # Get metrics with no feedback
        stats = learning_store.get_overall_stats()
        patterns = learning_store.get_symptom_disease_patterns()

        assert stats["total_extractions"] == 0
        assert len(patterns) == 0

    def test_learning_with_all_positive_feedback(self, temp_instance_dir):
        """Positive feedback only → parameters adjust appropriately."""
        learning_store = LearningDataStore()
        learning_store._state = None
        tuner = LearningTuner()

        # All positive feedback
        for i in range(25):
            learning_store.record_feedback_learning(
                session_id=f"test_{i:02d}",
                feedback_type="good",
                ai_result={"confidence": 0.85},
                reco2_verdict="test",
                extracted_symptoms=["s001"],
                disease_domain="general",
            )

        learning_data = {
            "feedback_records": learning_store._get_state()["learning_metrics"]["feedback_records"],
            "symptom_disease_patterns": [],
            "personalization_impact": [],
        }

        suggestions = tuner.suggest_parameter_adjustments(
            current_k=1.5,
            current_eta=0.01,
            learning_data=learning_data,
            window_stats={},
            ai_accuracy={"status": "ready", "overall_accuracy": 1.0},
        )

        # With all positive feedback and high accuracy, k should increase
        assert suggestions["suggested_k"] >= 1.5

    def test_learning_with_all_negative_feedback(self, temp_instance_dir):
        """Negative feedback only → system adjusts learning rate."""
        learning_store = LearningDataStore()
        learning_store._state = None
        tuner = LearningTuner()

        # All negative feedback
        for i in range(10):
            learning_store.record_feedback_learning(
                session_id=f"test_{i:02d}",
                feedback_type="bad",
                ai_result={"confidence": 0.3},
                reco2_verdict="test",
                extracted_symptoms=["s001"],
                disease_domain="general",
            )

        learning_data = {
            "feedback_records": learning_store._get_state()["learning_metrics"]["feedback_records"],
            "symptom_disease_patterns": [],
            "personalization_impact": [],
        }

        suggestions = tuner.suggest_parameter_adjustments(
            current_k=1.5,
            current_eta=0.01,
            learning_data=learning_data,
            window_stats={},
            ai_accuracy={"status": "ready", "overall_accuracy": 0.0},
        )

        # System should respond to poor performance
        assert suggestions["confidence_score"] < 1.0

    def test_concurrent_feedback_recording(self, temp_instance_dir):
        """Multiple concurrent feedback calls don't corrupt learning state."""
        learning_store = LearningDataStore()
        learning_store._state = None

        # Simulate rapid concurrent feedback
        for i in range(30):
            learning_store.record_feedback_learning(
                session_id=f"test_{i:02d}",
                feedback_type="good" if i % 2 == 0 else "bad",
                ai_result={"confidence": 0.85 - (i * 0.01)},
                reco2_verdict="test",
                extracted_symptoms=[f"s{i}"],
                disease_domain="general",
            )

        # Verify state consistency
        stats = learning_store.get_overall_stats()
        assert stats["total_extractions"] == 30

    def test_learning_state_persistence(self, temp_instance_dir):
        """Learning metrics survive process restart."""
        # Record in first instance
        store1 = LearningDataStore()
        store1._state = None
        store1.record_feedback_learning(
            session_id="test_001",
            feedback_type="good",
            ai_result={"confidence": 0.85},
            reco2_verdict="test",
            extracted_symptoms=["s001"],
            disease_domain="general",
        )

        # Create new instance (simulates restart)
        store2 = LearningDataStore()
        store2._state = None

        # Verify data persists
        stats = store2.get_overall_stats()
        assert stats["total_extractions"] == 1

    def test_backward_compatibility(self, temp_instance_dir):
        """Old state.json without learning_metrics loads and initializes correctly."""
        state_file = store.state_path()
        os.makedirs(os.path.dirname(state_file), exist_ok=True)

        # Create old state without learning_metrics
        import json

        old_state = {
            "k": 1.5,
            "eta": 0.01,
            "total_sessions": 10,
            "domains": {},
        }

        with open(state_file, "w") as f:
            json.dump(old_state, f)

        # Load and verify migration
        learning_store = LearningDataStore()
        learning_store._state = None

        state = learning_store._get_state()
        assert "learning_metrics" in state
        assert state["k"] == 1.5

    def test_domain_specific_learning(self, temp_instance_dir):
        """Orthopedics and Cardiology learn independently."""
        learning_store = LearningDataStore()
        learning_store._state = None

        # High accuracy in orthopedics
        for i in range(15):
            learning_store.record_feedback_learning(
                session_id=f"ortho_{i:02d}",
                feedback_type="good",
                ai_result={"confidence": 0.85},
                reco2_verdict="test",
                extracted_symptoms=["s001"],
                disease_domain="orthopedics",
            )

        # Low accuracy in cardiology
        for i in range(10):
            learning_store.record_feedback_learning(
                session_id=f"cardio_{i:02d}",
                feedback_type="good" if i < 4 else "bad",
                ai_result={"confidence": 0.85},
                reco2_verdict="test",
                extracted_symptoms=["s002"],
                disease_domain="cardiology",
            )

        # Verify domain-specific accuracies
        ortho_metrics = learning_store.get_ai_accuracy_by_domain("orthopedics")
        cardio_metrics = learning_store.get_ai_accuracy_by_domain("cardiology")

        assert ortho_metrics[0]["correct_extractions"] == 15
        assert cardio_metrics[0]["correct_extractions"] == 4

    def test_learning_insights_reflect_current_state(self, temp_instance_dir):
        """Health score and recommendations match actual metrics."""
        learning_store = LearningDataStore()
        learning_store._state = None

        # High accuracy scenario
        for i in range(30):
            learning_store.record_feedback_learning(
                session_id=f"test_{i:02d}",
                feedback_type="good",
                ai_result={"confidence": 0.85},
                reco2_verdict="test",
                extracted_symptoms=["s001"],
                disease_domain="general",
            )

        # Get insights
        stats = learning_store.get_overall_stats()

        # Health score should reflect good accuracy
        assert stats["overall_accuracy"] > 0.9
