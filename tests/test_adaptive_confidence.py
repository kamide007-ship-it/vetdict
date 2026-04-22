"""Comprehensive test suite for AdaptiveConfidenceCalculator.

Tests cover feedback collection, feature engineering, model training,
and confidence adjustment mechanisms.
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from api.ai.adaptive_confidence_calculator import (
    AdaptiveConfidenceCalculator,
    BayesianPrior,
    DiagnosisFeedbackCollector,
    DiagnosisRecord,
    FeatureEngineer,
    ModelType,
)


class TestDiagnosisRecord:
    """Test DiagnosisRecord dataclass."""

    def test_record_creation(self):
        """Test basic record creation."""
        record = DiagnosisRecord(
            case_id="case_001",
            symptoms=["vomiting", "lethargy"],
            initial_predictions={"Pancreatitis": 0.75, "Gastroenteritis": 0.65},
            actual_diagnosis="Pancreatitis",
            final_diagnosis_confirmed=True,
            veterinarian_id="vet_001",
            clinic_id="clinic_001",
            patient_age=5.5,
            patient_species="dog",
            severity_score=7.5,
        )

        assert record.case_id == "case_001"
        assert len(record.symptoms) == 2
        assert record.actual_diagnosis == "Pancreatitis"

    def test_record_to_dict(self):
        """Test record serialization."""
        record = DiagnosisRecord(
            case_id="test_001",
            symptoms=["cough"],
            initial_predictions={"Pneumonia": 0.8},
            actual_diagnosis="Pneumonia",
            final_diagnosis_confirmed=True,
            veterinarian_id="vet_001",
            clinic_id="clinic_001",
            patient_age=3.0,
            patient_species="dog",
            severity_score=5.0,
            treatment_response="good",
            outcome="recovered",
        )

        result = record.to_dict()
        assert result["case_id"] == "test_001"
        assert result["treatment_response"] == "good"
        assert result["outcome"] == "recovered"


class TestDiagnosisFeedbackCollector:
    """Test DiagnosisFeedbackCollector functionality."""

    @pytest.fixture
    def collector(self):
        """Create feedback collector."""
        return DiagnosisFeedbackCollector(max_records=100)

    @pytest.fixture
    def sample_records(self):
        """Create sample diagnosis records."""
        records = []

        for i in range(5):
            record = DiagnosisRecord(
                case_id=f"case_{i:03d}",
                symptoms=["vomiting", "lethargy"],
                initial_predictions={
                    "Pancreatitis": 0.7 + i * 0.05,
                    "Gastroenteritis": 0.6,
                },
                actual_diagnosis="Pancreatitis",
                final_diagnosis_confirmed=i < 4,  # First 4 correct
                veterinarian_id=f"vet_{i % 2}",
                clinic_id=f"clinic_{i % 2}",
                patient_age=5.0 + i,
                patient_species="dog",
                severity_score=6.0 + i,
            )
            records.append(record)

        return records

    def test_collector_initialization(self, collector):
        """Test collector initialization."""
        assert len(collector.records) == 0
        assert collector.max_records == 100

    def test_add_record(self, collector, sample_records):
        """Test adding records."""
        record = sample_records[0]
        added = collector.add_record(record)

        assert added is True
        assert len(collector.records) == 1
        assert record.case_id in collector.record_index

    def test_add_multiple_records(self, collector, sample_records):
        """Test adding multiple records."""
        for record in sample_records:
            collector.add_record(record)

        assert len(collector.records) == len(sample_records)

    def test_max_records_limit(self):
        """Test max records limit."""
        collector = DiagnosisFeedbackCollector(max_records=3)

        for i in range(5):
            record = DiagnosisRecord(
                case_id=f"case_{i}",
                symptoms=["test"],
                initial_predictions={"Disease": 0.5},
                actual_diagnosis="Disease",
                final_diagnosis_confirmed=True,
                veterinarian_id="vet_001",
                clinic_id="clinic_001",
                patient_age=5.0,
                patient_species="dog",
                severity_score=5.0,
            )
            added = collector.add_record(record)

            if i < 3:
                assert added is True
            else:
                assert added is False

    def test_get_record(self, collector, sample_records):
        """Test retrieving a record."""
        record = sample_records[0]
        collector.add_record(record)

        retrieved = collector.get_record(record.case_id)
        assert retrieved is not None
        assert retrieved.case_id == record.case_id

    def test_get_records_by_veterinarian(self, collector, sample_records):
        """Test retrieving records by veterinarian."""
        for record in sample_records:
            collector.add_record(record)

        vet_records = collector.get_records_by_veterinarian("vet_0")
        assert len(vet_records) == 3  # Cases 0, 2, 4

    def test_get_records_by_clinic(self, collector, sample_records):
        """Test retrieving records by clinic."""
        for record in sample_records:
            collector.add_record(record)

        clinic_records = collector.get_records_by_clinic("clinic_0")
        assert len(clinic_records) == 3

    def test_get_records_by_disease(self, collector, sample_records):
        """Test retrieving records by disease."""
        for record in sample_records:
            collector.add_record(record)

        disease_records = collector.get_records_by_disease("Pancreatitis")
        assert len(disease_records) == 5

    def test_get_records_by_species(self, collector, sample_records):
        """Test retrieving records by species."""
        for record in sample_records:
            collector.add_record(record)

        species_records = collector.get_records_by_species("dog")
        assert len(species_records) == 5

    def test_calculate_statistics(self, collector, sample_records):
        """Test statistics calculation."""
        for record in sample_records:
            collector.add_record(record)

        stats = collector.calculate_statistics()

        assert stats["total_records"] == 5
        assert stats["unique_cases"] == 5
        assert stats["unique_vets"] == 2
        assert stats["unique_clinics"] == 2
        assert stats["unique_diseases"] == 1
        assert 0 <= stats["correct_predictions_percent"] <= 100

    def test_json_export_import(self, collector, sample_records):
        """Test JSON export and import."""
        for record in sample_records:
            collector.add_record(record)

        # Export
        json_str = collector.to_json()
        assert len(json_str) > 0

        # Import into new collector
        new_collector = DiagnosisFeedbackCollector()
        new_collector.from_json(json_str)

        assert len(new_collector.records) == len(sample_records)


class TestFeatureEngineer:
    """Test FeatureEngineer functionality."""

    @pytest.fixture
    def sample_record(self):
        """Create sample record for feature extraction."""
        return DiagnosisRecord(
            case_id="test_001",
            symptoms=["vomiting", "lethargy", "fever"],
            initial_predictions={
                "Pancreatitis": 0.75,
                "Gastroenteritis": 0.65,
                "Infection": 0.45,
            },
            actual_diagnosis="Pancreatitis",
            final_diagnosis_confirmed=True,
            veterinarian_id="vet_001",
            clinic_id="clinic_001",
            patient_age=5.5,
            patient_species="dog",
            severity_score=7.0,
            treatment_response="good",
        )

    def test_extract_features(self, sample_record):
        """Test feature extraction."""
        features = FeatureEngineer.extract_features(sample_record)

        assert "num_symptoms" in features
        assert "patient_age" in features
        assert "severity_score" in features
        assert "max_initial_confidence" in features
        assert "species_code" in features

    def test_feature_values(self, sample_record):
        """Test extracted feature values."""
        features = FeatureEngineer.extract_features(sample_record)

        assert features["num_symptoms"] == 3
        assert features["patient_age"] == 5.5
        assert features["severity_score"] == 7.0
        assert features["max_initial_confidence"] == 0.75
        assert features["species_code"] == 1.0  # dog

    def test_entropy_calculation(self):
        """Test entropy calculation."""
        values = [0.5, 0.3, 0.2]
        entropy = FeatureEngineer._calculate_entropy(values)

        assert 0 <= entropy <= 2  # Binary entropy range

    def test_entropy_uniform(self):
        """Test entropy for uniform distribution."""
        values = [0.25, 0.25, 0.25, 0.25]
        entropy = FeatureEngineer._calculate_entropy(values)

        # Should be high for uniform distribution
        assert entropy > 1.0

    def test_entropy_concentrated(self):
        """Test entropy for concentrated distribution."""
        values = [0.9, 0.05, 0.05]
        entropy = FeatureEngineer._calculate_entropy(values)

        # Should be low for concentrated distribution
        assert entropy < 1.0


class TestBayesianPrior:
    """Test BayesianPrior functionality."""

    def test_prior_creation(self):
        """Test creating Bayesian prior."""
        prior = BayesianPrior(
            disease="Pancreatitis",
            prior_probability=0.05,
            likelihood_given_symptoms=0.85,
        )

        assert prior.disease == "Pancreatitis"
        assert prior.prior_probability == 0.05

    def test_posterior_update(self):
        """Test posterior probability update."""
        prior = BayesianPrior(
            disease="Pancreatitis",
            prior_probability=0.05,
            likelihood_given_symptoms=0.85,
        )

        prior.update_posterior(0.85)
        assert prior.posterior_probability > 0
        assert prior.posterior_probability <= 1.0

    def test_prior_to_dict(self):
        """Test prior serialization."""
        prior = BayesianPrior(
            disease="Test Disease",
            prior_probability=0.1,
            likelihood_given_symptoms=0.8,
        )
        prior.update_posterior(0.8)

        result = prior.to_dict()
        assert result["disease"] == "Test Disease"
        assert "posterior_probability" in result


class TestAdaptiveConfidenceCalculator:
    """Test AdaptiveConfidenceCalculator functionality."""

    @pytest.fixture
    def calculator(self):
        """Create calculator instance."""
        return AdaptiveConfidenceCalculator()

    @pytest.fixture
    def training_records(self):
        """Create training records."""
        records = []

        for i in range(30):
            correct = i < 20  # First 20 correct

            record = DiagnosisRecord(
                case_id=f"case_{i:03d}",
                symptoms=["symptom_1", "symptom_2"],
                initial_predictions={
                    "Disease_A": 0.7 + (0.01 if correct else -0.1),
                    "Disease_B": 0.5,
                },
                actual_diagnosis="Disease_A" if correct else "Disease_B",
                final_diagnosis_confirmed=correct,
                veterinarian_id=f"vet_{i % 3}",
                clinic_id=f"clinic_{i % 2}",
                patient_age=5.0 + i,
                patient_species="dog",
                severity_score=5.0,
                treatment_response="good" if correct else "poor",
            )
            records.append(record)

        return records

    def test_calculator_initialization(self, calculator):
        """Test calculator initialization."""
        assert len(calculator.feedback_collector.records) == 0
        assert len(calculator.vet_calibrations) == 0

    def test_add_diagnosis_feedback(self, calculator, training_records):
        """Test adding diagnosis feedback."""
        record = training_records[0]
        added = calculator.add_diagnosis_feedback(record)

        assert added is True
        assert len(calculator.feedback_collector.records) == 1

    def test_add_multiple_feedback(self, calculator, training_records):
        """Test adding multiple feedback records."""
        for record in training_records:
            calculator.add_diagnosis_feedback(record)

        assert len(calculator.feedback_collector.records) == len(training_records)

    def test_veterinarian_calibration_update(self, calculator):
        """Test veterinarian calibration updates."""
        record = DiagnosisRecord(
            case_id="test_001",
            symptoms=["test"],
            initial_predictions={"Disease": 0.8},
            actual_diagnosis="Disease",
            final_diagnosis_confirmed=True,
            veterinarian_id="vet_001",
            clinic_id="clinic_001",
            patient_age=5.0,
            patient_species="dog",
            severity_score=5.0,
        )

        calculator.add_diagnosis_feedback(record)

        # Calibration should be updated to ~1.01
        assert "vet_001" in calculator.vet_calibrations
        assert calculator.vet_calibrations["vet_001"] > 1.0

    def test_adjust_predictions_vet_calibration(self, calculator):
        """Test prediction adjustment with vet calibration."""
        # Set up vet calibration
        calculator.vet_calibrations["vet_001"] = 1.2

        predictions = {"Disease_A": 0.75, "Disease_B": 0.60}
        adjusted = calculator.adjust_predictions(predictions, veterinarian_id="vet_001")

        # Adjusted confidence should be adjusted (may be higher or normalized)
        assert "Disease_A" in adjusted
        assert "Disease_B" in adjusted

    def test_clinic_pattern_adjustment(self, calculator, training_records):
        """Test clinic-specific pattern adjustment."""
        for record in training_records[:15]:
            calculator.add_diagnosis_feedback(record)

        predictions = {"Disease_A": 0.5, "Disease_B": 0.5}
        adjusted = calculator.adjust_predictions(predictions, clinic_id="clinic_0")

        # Should be normalized
        assert sum(adjusted.values()) <= 1.01  # Allow small floating point error

    def test_species_adjustment(self, calculator, training_records):
        """Test species-specific adjustment."""
        for record in training_records:
            calculator.add_diagnosis_feedback(record)

        predictions = {"Disease_A": 0.5, "Disease_B": 0.5}
        adjusted = calculator.adjust_predictions(predictions, species="dog")

        # Should be adjusted based on dog patterns
        assert len(adjusted) == 2

    def test_calculate_model_metrics(self, calculator, training_records):
        """Test model metrics calculation."""
        for record in training_records:
            calculator.add_diagnosis_feedback(record)

        metrics = calculator.calculate_model_metrics()

        assert metrics is not None
        assert 0 <= metrics.accuracy <= 1
        assert metrics.calibration_score >= 0

    def test_insufficient_records_for_metrics(self, calculator):
        """Test metrics with insufficient records."""
        record = DiagnosisRecord(
            case_id="test_001",
            symptoms=["test"],
            initial_predictions={"Disease": 0.5},
            actual_diagnosis="Disease",
            final_diagnosis_confirmed=True,
            veterinarian_id="vet_001",
            clinic_id="clinic_001",
            patient_age=5.0,
            patient_species="dog",
            severity_score=5.0,
        )
        calculator.add_diagnosis_feedback(record)

        metrics = calculator.calculate_model_metrics()
        assert metrics is None  # Less than 10 records

    def test_train_model(self, calculator, training_records):
        """Test model training."""
        for record in training_records:
            calculator.add_diagnosis_feedback(record)

        trained = calculator.train_model(ModelType.ENSEMBLE)

        assert trained is True
        assert ModelType.ENSEMBLE.value in calculator.models
        assert calculator.last_trained is not None

    def test_train_insufficient_data(self, calculator):
        """Test training with insufficient data."""
        record = DiagnosisRecord(
            case_id="test_001",
            symptoms=["test"],
            initial_predictions={"Disease": 0.5},
            actual_diagnosis="Disease",
            final_diagnosis_confirmed=True,
            veterinarian_id="vet_001",
            clinic_id="clinic_001",
            patient_age=5.0,
            patient_species="dog",
            severity_score=5.0,
        )
        calculator.add_diagnosis_feedback(record)

        trained = calculator.train_model()
        assert trained is False

    def test_get_feedback_statistics(self, calculator, training_records):
        """Test feedback statistics."""
        for record in training_records:
            calculator.add_diagnosis_feedback(record)

        stats = calculator.get_feedback_statistics()

        assert stats["total_records"] == len(training_records)
        assert "correct_predictions_percent" in stats

    def test_get_veterinarian_stats(self, calculator, training_records):
        """Test veterinarian statistics."""
        for record in training_records:
            calculator.add_diagnosis_feedback(record)

        vet_stats = calculator.get_veterinarian_stats("vet_0")

        assert "vet_id" in vet_stats
        assert "records" in vet_stats
        assert "accuracy" in vet_stats

    def test_get_clinic_stats(self, calculator, training_records):
        """Test clinic statistics."""
        for record in training_records:
            calculator.add_diagnosis_feedback(record)

        clinic_stats = calculator.get_clinic_stats("clinic_0")

        assert "clinic_id" in clinic_stats
        assert "records" in clinic_stats
        assert "accuracy" in clinic_stats

    def test_to_dict(self, calculator, training_records):
        """Test export to dict."""
        for record in training_records:
            calculator.add_diagnosis_feedback(record)

        result = calculator.to_dict()

        assert "feedback_statistics" in result
        assert "veterinarian_calibrations" in result
        assert "models" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
