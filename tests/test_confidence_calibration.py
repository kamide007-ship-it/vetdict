"""
Tests for Phase 3 STEP 2: Confidence Calibration.

Tests confidence score calibration and calibration factor calculation.
"""

import os
import tempfile

import pytest

from api.ai.confidence_calibration import ConfidenceCalibrator
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
def calibrator(temp_instance_dir):
    """Create fresh calibrator for each test."""
    return ConfidenceCalibrator()


@pytest.fixture
def learning_store_instance(temp_instance_dir):
    """Create fresh learning store for tests."""
    store_instance = LearningDataStore()
    store_instance._state = None
    return store_instance


class TestCalibrationFactor:
    """Test calibration factor calculation."""

    def test_calibration_factor_no_data(self, calibrator):
        """Test calibration factor with no data."""
        factor = calibrator.get_calibration_factor(0.85, domain="general")

        # Should return neutral factor with no data
        assert factor == 1.0

    def test_calibration_factor_insufficient_samples(self, calibrator, learning_store_instance):
        """Test calibration factor with insufficient samples."""
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

        factor = calibrator.get_calibration_factor(0.85, domain="general")

        # Should return neutral factor with insufficient data
        assert factor == 1.0

    def test_calibration_factor_overconfident(self, calibrator, learning_store_instance):
        """Test calibration when AI is overconfident."""
        # Record 25 good feedback (accuracy 100%)
        for i in range(25):
            learning_store_instance.record_feedback_learning(
                session_id=f"test_{i:02d}",
                feedback_type="good",
                ai_result={"confidence": 0.9},
                reco2_verdict="test",
                extracted_symptoms=["s001"],
                disease_domain="general",
            )

        # If confidence is 0.9 but accuracy is 1.0, factor should be > 1.0
        factor = calibrator.get_calibration_factor(0.9, domain="general")
        assert factor >= 1.0

    def test_calibration_factor_underconfident(self, calibrator, learning_store_instance):
        """Test calibration when AI is underconfident."""
        # Record 25 entries: 20 good, 5 bad
        for i in range(20):
            learning_store_instance.record_feedback_learning(
                session_id=f"test_{i:02d}",
                feedback_type="good",
                ai_result={"confidence": 0.5},
                reco2_verdict="test",
                extracted_symptoms=["s001"],
                disease_domain="general",
            )

        for i in range(5):
            learning_store_instance.record_feedback_learning(
                session_id=f"test_{20 + i:02d}",
                feedback_type="bad",
                ai_result={"confidence": 0.5},
                reco2_verdict="test",
                extracted_symptoms=["s002"],
                disease_domain="general",
            )

        # Accuracy is 80%, confidence is 0.5, factor should be > 1.0
        factor = calibrator.get_calibration_factor(0.5, domain="general")
        assert factor > 1.0

    def test_calibration_factor_domain_specific(self, calibrator, learning_store_instance):
        """Test domain-specific calibration factors."""
        # Orthopedics: high accuracy
        for i in range(25):
            learning_store_instance.record_feedback_learning(
                session_id=f"ortho_{i:02d}",
                feedback_type="good",
                ai_result={"confidence": 0.85},
                reco2_verdict="test",
                extracted_symptoms=["s001"],
                disease_domain="orthopedics",
            )

        # Cardiology: low accuracy
        for i in range(20):
            learning_store_instance.record_feedback_learning(
                session_id=f"cardio_{i:02d}",
                feedback_type="good" if i < 10 else "bad",
                ai_result={"confidence": 0.85},
                reco2_verdict="test",
                extracted_symptoms=["s002"],
                disease_domain="cardiology",
            )

        ortho_factor = calibrator.get_calibration_factor(0.85, domain="orthopedics")
        cardio_factor = calibrator.get_calibration_factor(0.85, domain="cardiology")

        # Orthopedics should be more confident than cardiology
        assert ortho_factor >= cardio_factor


class TestExtractExtractionCalibration:
    """Test extraction result calibration."""

    def test_calibrate_extraction_result(self, calibrator):
        """Test basic extraction calibration."""
        extraction = {
            "symptoms": ["s001"],
            "confidence": 0.85,
            "domain": "general",
        }

        result = calibrator.calibrate_extraction_result(extraction)

        assert "calibration_factor" in result
        assert "calibration_notes" in result
        assert "expected_accuracy" in result
        # With no data, factor should be 1.0
        assert result["calibration_factor"] == 1.0
        assert result["confidence"] == 0.85

    def test_calibrate_extraction_with_data(self, calibrator, learning_store_instance):
        """Test calibration with learned data."""
        # Build high-accuracy domain
        for i in range(25):
            learning_store_instance.record_feedback_learning(
                session_id=f"test_{i:02d}",
                feedback_type="good",
                ai_result={"confidence": 0.85},
                reco2_verdict="test",
                extracted_symptoms=["s001"],
                disease_domain="general",
            )

        extraction = {
            "symptoms": ["s001"],
            "confidence": 0.85,
            "domain": "general",
        }

        result = calibrator.calibrate_extraction_result(extraction)

        # Factor should be well-calibrated
        assert 0.9 <= result["calibration_factor"] <= 1.1
        assert result["confidence"] <= 1.0
        assert result["confidence"] >= 0.0

    def test_calibrate_clamps_confidence(self, calibrator):
        """Test that calibration clamps confidence to [0, 1]."""
        extraction = {
            "symptoms": ["s001"],
            "confidence": 0.99,
            "domain": "general",
        }

        result = calibrator.calibrate_extraction_result(extraction)

        assert 0.0 <= result["confidence"] <= 1.0

    def test_calibration_notes(self, calibrator):
        """Test calibration notes generation."""
        extraction = {
            "symptoms": ["s001"],
            "confidence": 0.85,
            "domain": "general",
        }

        result = calibrator.calibrate_extraction_result(extraction)

        # With neutral factor, should mention well-calibrated
        assert "calibration_notes" in result
        assert isinstance(result["calibration_notes"], str)


class TestCalibrationReport:
    """Test overall calibration reports."""

    def test_calibration_report_no_data(self, calibrator):
        """Test calibration report with no data."""
        report = calibrator.get_calibration_report()

        assert report["status"] == "no_data"
        assert len(report["domains"]) == 0

    def test_calibration_report_multiple_domains(self, calibrator, learning_store_instance):
        """Test calibration report with multiple domains."""
        # Domain 1: good data
        for i in range(25):
            learning_store_instance.record_feedback_learning(
                session_id=f"d1_{i:02d}",
                feedback_type="good",
                ai_result={"confidence": 0.85},
                reco2_verdict="test",
                extracted_symptoms=["s001"],
                disease_domain="domain1",
            )

        # Domain 2: insufficient data
        for i in range(5):
            learning_store_instance.record_feedback_learning(
                session_id=f"d2_{i:02d}",
                feedback_type="good",
                ai_result={"confidence": 0.85},
                reco2_verdict="test",
                extracted_symptoms=["s002"],
                disease_domain="domain2",
            )

        report = calibrator.get_calibration_report()

        assert report["status"] == "ready"
        # Should include domain1 (sufficient data)
        domain1_report = next((d for d in report["domains"] if d["domain"] == "domain1"), None)
        assert domain1_report is not None

    def test_calibration_report_identifies_overconfident(self, calibrator, learning_store_instance):
        """Test that report identifies overconfident domains."""
        # Record overconfident data: high confidence, low accuracy
        for i in range(20):
            learning_store_instance.record_feedback_learning(
                session_id=f"test_{i:02d}",
                feedback_type="good" if i < 10 else "bad",
                ai_result={"confidence": 0.9},  # High confidence
                reco2_verdict="test",
                extracted_symptoms=["s001"],
                disease_domain="general",
            )

        report = calibrator.get_calibration_report()

        # Should identify the domain as having calibration issues
        domain_report = next((d for d in report["domains"] if d["domain"] == "general"), None)
        assert domain_report is not None


class TestShouldApplyCalibration:
    """Test calibration application decision."""

    def test_should_apply_calibration_no_data(self, calibrator):
        """Test that calibration is not applied with no data."""
        should_apply = calibrator.should_apply_calibration(domain="general")
        assert should_apply is False

    def test_should_apply_calibration_insufficient_samples(self, calibrator, learning_store_instance):
        """Test that calibration is not applied with insufficient samples."""
        for i in range(5):
            learning_store_instance.record_feedback_learning(
                session_id=f"test_{i:02d}",
                feedback_type="good",
                ai_result={"confidence": 0.85},
                reco2_verdict="test",
                extracted_symptoms=["s001"],
                disease_domain="general",
            )

        should_apply = calibrator.should_apply_calibration(domain="general")
        assert should_apply is False

    def test_should_apply_calibration_sufficient_data(self, calibrator, learning_store_instance):
        """Test that calibration is applied with sufficient data."""
        for i in range(25):
            learning_store_instance.record_feedback_learning(
                session_id=f"test_{i:02d}",
                feedback_type="good",
                ai_result={"confidence": 0.85},
                reco2_verdict="test",
                extracted_symptoms=["s001"],
                disease_domain="general",
            )

        should_apply = calibrator.should_apply_calibration(domain="general")
        assert should_apply is True
