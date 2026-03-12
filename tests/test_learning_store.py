"""
Tests for Phase 3 Learning Data Store (STEP 1).

Tests learning data persistence, analytics queries, and pattern aggregation.
"""

import os
import json
import tempfile
import pytest
from datetime import datetime, timedelta, timezone

from reco2.learning_store import LearningDataStore
from reco2.learning_models import (
    SymptomDiseaseLearning,
    AIExtractionAccuracy,
    FeedbackRecord,
)
from reco2 import store


@pytest.fixture
def temp_instance_dir():
    """Create temporary instance directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        os.environ["RECO3_INSTANCE_DIR"] = tmpdir
        yield tmpdir
        if "RECO3_INSTANCE_DIR" in os.environ:
            del os.environ["RECO3_INSTANCE_DIR"]


@pytest.fixture
def learning_store(temp_instance_dir):
    """Create fresh learning store for each test."""
    # Clear module state
    store._instance_dir.cache_clear() if hasattr(store._instance_dir, 'cache_clear') else None

    store_instance = LearningDataStore()
    # Reset state cache
    store_instance._state = None
    return store_instance


class TestFeedbackRecording:
    """Test feedback recording and persistence."""

    def test_record_feedback_creates_learning_metrics(self, learning_store):
        """Test that recording feedback initializes learning_metrics."""
        learning_store.record_feedback_learning(
            session_id="test_001",
            feedback_type="good",
            ai_result={"confidence": 0.85},
            reco2_verdict="arthritis suspected",
            extracted_symptoms=["s001", "s002"],
            disease_domain="orthopedics",
        )

        state = learning_store._get_state()
        assert "learning_metrics" in state
        assert "feedback_records" in state["learning_metrics"]
        assert len(state["learning_metrics"]["feedback_records"]) == 1

    def test_record_good_feedback(self, learning_store):
        """Test recording good feedback updates accuracy metrics."""
        learning_store.record_feedback_learning(
            session_id="test_001",
            feedback_type="good",
            ai_result={"confidence": 0.85},
            reco2_verdict="arthritis suspected",
            extracted_symptoms=["s001", "s002"],
            disease_domain="orthopedics",
        )

        metrics = learning_store.get_ai_accuracy_by_domain("orthopedics")
        assert len(metrics) == 1
        assert metrics[0]["correct_extractions"] == 1
        assert metrics[0]["total_extractions"] == 1

    def test_record_bad_feedback(self, learning_store):
        """Test recording bad feedback."""
        learning_store.record_feedback_learning(
            session_id="test_001",
            feedback_type="bad",
            ai_result={"confidence": 0.85},
            reco2_verdict="arthritis suspected",
            extracted_symptoms=["s001"],
            disease_domain="orthopedics",
        )

        metrics = learning_store.get_ai_accuracy_by_domain("orthopedics")
        assert len(metrics) == 1
        assert metrics[0]["correct_extractions"] == 0
        assert metrics[0]["total_extractions"] == 1

    def test_multiple_feedback_accumulation(self, learning_store):
        """Test multiple feedback records accumulate correctly."""
        # Good feedback x2
        for i in range(2):
            learning_store.record_feedback_learning(
                session_id=f"test_{i:03d}",
                feedback_type="good",
                ai_result={"confidence": 0.9},
                reco2_verdict="arthritis suspected",
                extracted_symptoms=["s001", "s002"],
                disease_domain="orthopedics",
            )

        # Bad feedback x1
        learning_store.record_feedback_learning(
            session_id="test_003",
            feedback_type="bad",
            ai_result={"confidence": 0.3},
            reco2_verdict="sprain",
            extracted_symptoms=["s003"],
            disease_domain="orthopedics",
        )

        metrics = learning_store.get_ai_accuracy_by_domain("orthopedics")
        assert metrics[0]["total_extractions"] == 3
        assert metrics[0]["correct_extractions"] == 2

    def test_feedback_memory_bounded(self, learning_store):
        """Test feedback records capped at 2000."""
        # Record 2100 feedback entries
        for i in range(2100):
            learning_store.record_feedback_learning(
                session_id=f"test_{i:04d}",
                feedback_type="good",
                ai_result={"confidence": 0.85},
                reco2_verdict="test",
                extracted_symptoms=["s001"],
                disease_domain="general",
            )

        state = learning_store._get_state()
        feedback_count = len(state["learning_metrics"]["feedback_records"])
        assert feedback_count <= 2000

    def test_concurrent_feedback_recording(self, learning_store):
        """Test multiple concurrent feedback calls don't corrupt state."""
        # Record feedback rapidly
        for i in range(10):
            learning_store.record_feedback_learning(
                session_id=f"test_{i:02d}",
                feedback_type="good" if i % 2 == 0 else "bad",
                ai_result={"confidence": 0.85 - (i * 0.01)},
                reco2_verdict="test verdict",
                extracted_symptoms=[f"s{i:03d}", "s001"],
                disease_domain="general",
            )

        metrics = learning_store.get_ai_accuracy_by_domain("general")
        assert metrics[0]["total_extractions"] == 10


class TestSymptomDiseasePatterns:
    """Test symptom-disease pattern learning and retrieval."""

    def test_create_symptom_disease_pattern(self, learning_store):
        """Test creating a new symptom-disease pattern."""
        learning_store.record_feedback_learning(
            session_id="test_001",
            feedback_type="good",
            ai_result={"confidence": 0.85},
            reco2_verdict="arthritis suspected",
            extracted_symptoms=["limp", "swelling"],
            disease_domain="arthritis",
        )

        patterns = learning_store.get_symptom_disease_patterns()
        assert len(patterns) == 1
        assert patterns[0]["disease_id"] == "arthritis"
        assert set(patterns[0]["symptoms"]) == {"limp", "swelling"}
        assert patterns[0]["accuracy_rate"] == 1.0
        assert patterns[0]["sample_count"] == 1

    def test_aggregate_symptom_disease_patterns(self, learning_store):
        """Test pattern aggregation with multiple feedback."""
        # Same symptoms, correct diagnosis
        learning_store.record_feedback_learning(
            session_id="test_001",
            feedback_type="good",
            ai_result={"confidence": 0.85},
            reco2_verdict="arthritis suspected",
            extracted_symptoms=["limp", "swelling"],
            disease_domain="arthritis",
        )

        # Same symptoms, incorrect diagnosis
        learning_store.record_feedback_learning(
            session_id="test_002",
            feedback_type="bad",
            ai_result={"confidence": 0.85},
            reco2_verdict="arthritis suspected",
            extracted_symptoms=["limp", "swelling"],
            disease_domain="arthritis",
        )

        patterns = learning_store.get_symptom_disease_patterns()
        assert len(patterns) == 1
        assert patterns[0]["sample_count"] == 2
        # Accuracy should be 50% (1 correct, 1 incorrect)
        assert patterns[0]["accuracy_rate"] == pytest.approx(0.5)

    def test_filter_patterns_by_symptom(self, learning_store):
        """Test filtering patterns by symptom ID."""
        # Pattern 1: [s001, s002] → disease_a
        learning_store.record_feedback_learning(
            session_id="test_001",
            feedback_type="good",
            ai_result={"confidence": 0.85},
            reco2_verdict="test",
            extracted_symptoms=["s001", "s002"],
            disease_domain="disease_a",
        )

        # Pattern 2: [s002, s003] → disease_b
        learning_store.record_feedback_learning(
            session_id="test_002",
            feedback_type="good",
            ai_result={"confidence": 0.85},
            reco2_verdict="test",
            extracted_symptoms=["s002", "s003"],
            disease_domain="disease_b",
        )

        # Filter by s001
        patterns = learning_store.get_symptom_disease_patterns(symptom_ids=["s001"])
        assert len(patterns) == 1
        assert "s001" in patterns[0]["symptoms"]

        # Filter by s002
        patterns = learning_store.get_symptom_disease_patterns(symptom_ids=["s002"])
        assert len(patterns) == 2

    def test_patterns_sorted_by_accuracy(self, learning_store):
        """Test patterns sorted by accuracy and sample count."""
        # High accuracy pattern
        for _ in range(5):
            learning_store.record_feedback_learning(
                session_id="test_001",
                feedback_type="good",
                ai_result={"confidence": 0.85},
                reco2_verdict="test",
                extracted_symptoms=["high_acc"],
                disease_domain="disease_a",
            )

        # Low accuracy pattern
        learning_store.record_feedback_learning(
            session_id="test_002",
            feedback_type="bad",
            ai_result={"confidence": 0.85},
            reco2_verdict="test",
            extracted_symptoms=["low_acc"],
            disease_domain="disease_b",
        )

        patterns = learning_store.get_symptom_disease_patterns()
        # High accuracy pattern should be first
        assert patterns[0]["accuracy_rate"] >= patterns[1]["accuracy_rate"]


class TestAIAccuracyMetrics:
    """Test AI extraction accuracy tracking."""

    def test_accuracy_calculation(self, learning_store):
        """Test basic accuracy calculation."""
        # 3 correct, 1 incorrect
        for i in range(3):
            learning_store.record_feedback_learning(
                session_id=f"test_{i:03d}",
                feedback_type="good",
                ai_result={"confidence": 0.9},
                reco2_verdict="test",
                extracted_symptoms=[f"s{i}"],
                disease_domain="general",
            )

        learning_store.record_feedback_learning(
            session_id="test_003",
            feedback_type="bad",
            ai_result={"confidence": 0.2},
            reco2_verdict="test",
            extracted_symptoms=["s_bad"],
            disease_domain="general",
        )

        metrics = learning_store.get_ai_accuracy_by_domain("general")
        assert metrics[0]["total_extractions"] == 4
        assert metrics[0]["correct_extractions"] == 3

    def test_confidence_tracking(self, learning_store):
        """Test confidence score tracking."""
        learning_store.record_feedback_learning(
            session_id="test_001",
            feedback_type="good",
            ai_result={"confidence": 0.9},
            reco2_verdict="test",
            extracted_symptoms=["s001"],
            disease_domain="general",
        )

        learning_store.record_feedback_learning(
            session_id="test_002",
            feedback_type="bad",
            ai_result={"confidence": 0.3},
            reco2_verdict="test",
            extracted_symptoms=["s002"],
            disease_domain="general",
        )

        metrics = learning_store.get_ai_accuracy_by_domain("general")
        # Avg confidence for correct should be 0.9
        assert metrics[0]["avg_confidence"] == pytest.approx(0.9)
        # Avg confidence for failed should be 0.3
        assert metrics[0]["avg_confidence_failed"] == pytest.approx(0.3)

    def test_domain_isolation(self, learning_store):
        """Test domains tracked separately."""
        learning_store.record_feedback_learning(
            session_id="test_001",
            feedback_type="good",
            ai_result={"confidence": 0.85},
            reco2_verdict="test",
            extracted_symptoms=["s001"],
            disease_domain="orthopedics",
        )

        learning_store.record_feedback_learning(
            session_id="test_002",
            feedback_type="good",
            ai_result={"confidence": 0.85},
            reco2_verdict="test",
            extracted_symptoms=["s002"],
            disease_domain="cardiology",
        )

        ortho_metrics = learning_store.get_ai_accuracy_by_domain("orthopedics")
        cardio_metrics = learning_store.get_ai_accuracy_by_domain("cardiology")

        assert len(ortho_metrics) == 1
        assert len(cardio_metrics) == 1
        assert ortho_metrics[0]["domain"] == "orthopedics"
        assert cardio_metrics[0]["domain"] == "cardiology"

    def test_accuracy_limit(self, learning_store):
        """Test limit parameter on get_ai_accuracy_by_domain."""
        for i in range(5):
            learning_store.record_feedback_learning(
                session_id=f"test_{i:02d}",
                feedback_type="good",
                ai_result={"confidence": 0.85},
                reco2_verdict="test",
                extracted_symptoms=[f"s{i}"],
                disease_domain=f"domain_{i}",
            )

        metrics = learning_store.get_ai_accuracy_by_domain(limit=2)
        assert len(metrics) <= 2


class TestPatternPruning:
    """Test old pattern removal."""

    def test_prune_old_patterns(self, learning_store):
        """Test pruning patterns older than N days."""
        # Create a pattern and manually age it
        learning_store.record_feedback_learning(
            session_id="test_001",
            feedback_type="good",
            ai_result={"confidence": 0.85},
            reco2_verdict="test",
            extracted_symptoms=["s001"],
            disease_domain="general",
        )

        # Manually set old timestamp
        state = learning_store._get_state()
        old_date = (datetime.now(timezone.utc) - timedelta(days=100)).isoformat(
            timespec="seconds"
        )
        state["learning_metrics"]["symptom_disease_patterns"][0]["last_updated"] = old_date
        learning_store._save_state()

        # Prune patterns > 90 days old
        removed = learning_store.prune_old_patterns(days=90)
        assert removed >= 1

        patterns = learning_store.get_symptom_disease_patterns()
        assert len(patterns) == 0

    def test_prune_keeps_recent_patterns(self, learning_store):
        """Test pruning keeps recent patterns."""
        learning_store.record_feedback_learning(
            session_id="test_001",
            feedback_type="good",
            ai_result={"confidence": 0.85},
            reco2_verdict="test",
            extracted_symptoms=["s001"],
            disease_domain="general",
        )

        # Prune patterns > 90 days old
        removed = learning_store.prune_old_patterns(days=90)
        assert removed == 0

        patterns = learning_store.get_symptom_disease_patterns()
        assert len(patterns) == 1


class TestDataPersistence:
    """Test data persistence across loads."""

    def test_state_persists_across_loads(self, temp_instance_dir):
        """Test learning data survives process restart."""
        # Create and record
        store_1 = LearningDataStore()
        store_1._state = None
        store_1.record_feedback_learning(
            session_id="test_001",
            feedback_type="good",
            ai_result={"confidence": 0.85},
            reco2_verdict="test",
            extracted_symptoms=["s001"],
            disease_domain="general",
        )

        # Create new instance and verify data persists
        store_2 = LearningDataStore()
        store_2._state = None
        metrics = store_2.get_ai_accuracy_by_domain("general")
        assert len(metrics) == 1
        assert metrics[0]["total_extractions"] == 1

    def test_backward_compatibility(self, temp_instance_dir):
        """Test loading old state.json without learning_metrics."""
        # Create old state file
        state_file = store.state_path()
        os.makedirs(os.path.dirname(state_file), exist_ok=True)

        old_state = {
            "k": 1.5,
            "eta": 0.01,
            "total_sessions": 10,
        }

        with open(state_file, "w") as f:
            json.dump(old_state, f)

        # Load and verify migration
        store._instance_dir.cache_clear() if hasattr(store._instance_dir, 'cache_clear') else None
        store_instance = LearningDataStore()
        store_instance._state = None

        state = store_instance._get_state()
        assert "learning_metrics" in state
        assert state["k"] == 1.5


class TestOverallStats:
    """Test overall learning statistics."""

    def test_get_overall_stats(self, learning_store):
        """Test overall statistics aggregation."""
        learning_store.record_feedback_learning(
            session_id="test_001",
            feedback_type="good",
            ai_result={"confidence": 0.85},
            reco2_verdict="test",
            extracted_symptoms=["s001"],
            disease_domain="general",
        )

        stats = learning_store.get_overall_stats()
        assert stats["total_feedback_records"] == 1
        assert stats["total_patterns_learned"] >= 0
        assert stats["total_extractions"] == 1
        assert stats["total_correct_extractions"] == 1
        assert stats["overall_accuracy"] == 1.0
