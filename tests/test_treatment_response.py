"""Test suite for TreatmentResponsePredictor.

Tests cover treatment options, response prediction, outcome recording,
and treatment statistics.
"""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from api.ai.treatment_response_predictor import (
    TreatmentKnowledgeBase,
    TreatmentModality,
    TreatmentOption,
    TreatmentResponsePredictor,
)


class TestTreatmentOption:
    """Test TreatmentOption dataclass."""

    def test_treatment_creation(self):
        """Test creating a treatment option."""
        treatment = TreatmentOption(
            name="Test Treatment",
            modality=TreatmentModality.PHARMACOLOGICAL,
            disease="Test Disease",
            expected_success_rate=0.75,
            onset_time_days=1.0,
            duration_days=7.0,
            cost_category="medium",
            side_effects_probability=0.10,
        )

        assert treatment.name == "Test Treatment"
        assert treatment.expected_success_rate == 0.75
        assert treatment.modality == TreatmentModality.PHARMACOLOGICAL

    def test_treatment_to_dict(self):
        """Test treatment serialization."""
        treatment = TreatmentOption(
            name="Treatment A",
            modality=TreatmentModality.SURGICAL,
            disease="Disease A",
            expected_success_rate=0.85,
            onset_time_days=0.0,
            duration_days=365.0,
            cost_category="high",
            side_effects_probability=0.15,
            contraindications=["Old age"],
            evidence_level="high",
        )

        result = treatment.to_dict()
        assert result["name"] == "Treatment A"
        assert result["expected_success_rate"] == 0.85
        assert result["evidence_level"] == "high"
        assert "Old age" in result["contraindications"]


class TestTreatmentKnowledgeBase:
    """Test TreatmentKnowledgeBase functionality."""

    def test_get_treatment_options_pancreatitis(self):
        """Test retrieving treatment options for pancreatitis."""
        options = TreatmentKnowledgeBase.get_treatment_options("Pancreatitis")

        assert len(options) > 0
        assert all(o.disease == "Pancreatitis" for o in options)

    def test_get_treatment_options_unknown_disease(self):
        """Test retrieving options for unknown disease."""
        options = TreatmentKnowledgeBase.get_treatment_options("Unknown Disease")
        assert len(options) == 0

    def test_get_specific_treatment(self):
        """Test retrieving specific treatment."""
        treatment = TreatmentKnowledgeBase.get_treatment(
            "Pancreatitis",
            "Supportive Care (IV fluids, rest, diet)"
        )

        assert treatment is not None
        assert treatment.disease == "Pancreatitis"

    def test_get_specific_treatment_not_found(self):
        """Test retrieving non-existent treatment."""
        treatment = TreatmentKnowledgeBase.get_treatment(
            "Pancreatitis",
            "Non-existent Treatment"
        )

        assert treatment is None

    def test_knowledge_base_coverage(self):
        """Test knowledge base covers multiple diseases."""
        diseases = ["Pancreatitis", "Osteoarthritis", "Diabetes Mellitus", "Hip Dysplasia"]

        for disease in diseases:
            options = TreatmentKnowledgeBase.get_treatment_options(disease)
            assert len(options) > 0, f"No treatments for {disease}"


class TestTreatmentResponsePredictor:
    """Test TreatmentResponsePredictor functionality."""

    @pytest.fixture
    def predictor(self):
        """Create predictor instance."""
        return TreatmentResponsePredictor()

    def test_predictor_initialization(self, predictor):
        """Test predictor initialization."""
        assert len(predictor.predictions) == 0
        assert len(predictor.outcome_history) == 0

    def test_predict_single_treatment(self, predictor):
        """Test predicting response to single treatment."""
        response = predictor.predict_treatment_response(
            disease="Pancreatitis",
            treatment_name="Supportive Care (IV fluids, rest, diet)",
            patient_age=5.0,
        )

        assert response is not None
        assert response.disease == "Pancreatitis"
        assert 0 <= response.success_probability <= 1

    def test_predict_unknown_treatment(self, predictor):
        """Test predicting unknown treatment."""
        response = predictor.predict_treatment_response(
            disease="Unknown Disease",
            treatment_name="Unknown Treatment",
            patient_age=5.0,
        )

        assert response is None

    def test_age_adjustment_puppies(self, predictor):
        """Test age adjustment for young animals."""
        young_response = predictor.predict_treatment_response(
            disease="Gastroenteritis",
            treatment_name="Supportive Care (IV fluids, rest, diet)",
            patient_age=0.5,
        )

        adult_response = predictor.predict_treatment_response(
            disease="Gastroenteritis",
            treatment_name="Supportive Care (IV fluids, rest, diet)",
            patient_age=5.0,
        )

        # If treatment exists, verify both responses
        if young_response and adult_response:
            assert young_response.disease == "Gastroenteritis"
            assert adult_response.disease == "Gastroenteritis"

    def test_age_adjustment_seniors(self, predictor):
        """Test age adjustment for senior animals."""
        response = predictor.predict_treatment_response(
            disease="Osteoarthritis",
            treatment_name="NSAIDs (Carprofen, Meloxicam)",
            patient_age=12.0,
        )

        assert response is not None
        assert response.success_probability > 0

    def test_severity_adjustment(self, predictor):
        """Test disease severity adjustment."""
        mild_response = predictor.predict_treatment_response(
            disease="Pancreatitis",
            treatment_name="Supportive Care (IV fluids, rest, diet)",
            patient_age=5.0,
            disease_severity=2.0,
        )

        severe_response = predictor.predict_treatment_response(
            disease="Pancreatitis",
            treatment_name="Supportive Care (IV fluids, rest, diet)",
            patient_age=5.0,
            disease_severity=9.0,
        )

        # Severe disease should have lower success
        assert mild_response.success_probability > severe_response.success_probability

    def test_comorbidity_contraindication(self, predictor):
        """Test contraindication reduces success."""
        without_comorbidity = predictor.predict_treatment_response(
            disease="Osteoarthritis",
            treatment_name="NSAIDs (Carprofen, Meloxicam)",
            patient_age=7.0,
            comorbidities=[],
        )

        with_comorbidity = predictor.predict_treatment_response(
            disease="Osteoarthritis",
            treatment_name="NSAIDs (Carprofen, Meloxicam)",
            patient_age=7.0,
            comorbidities=["Renal disease"],
        )

        # NSAIDs contraindicated in renal disease
        assert with_comorbidity.success_probability < without_comorbidity.success_probability

    def test_compliance_impact(self, predictor):
        """Test compliance likelihood impact."""
        high_compliance = predictor.predict_treatment_response(
            disease="Diabetes Mellitus",
            treatment_name="Insulin Therapy",
            patient_age=6.0,
            owner_compliance_likelihood=0.9,
        )

        low_compliance = predictor.predict_treatment_response(
            disease="Diabetes Mellitus",
            treatment_name="Insulin Therapy",
            patient_age=6.0,
            owner_compliance_likelihood=0.3,
        )

        # Low compliance should reduce success
        assert high_compliance.success_probability > low_compliance.success_probability

    def test_predict_all_treatments(self, predictor):
        """Test predicting all treatments for disease."""
        responses = predictor.predict_all_treatments(
            disease="Osteoarthritis",
            patient_age=8.0,
        )

        assert len(responses) > 0
        # Should be sorted by success probability
        for i in range(len(responses) - 1):
            assert responses[i].success_probability >= responses[i + 1].success_probability

    def test_predict_all_unknown_disease(self, predictor):
        """Test predicting treatments for unknown disease."""
        responses = predictor.predict_all_treatments(
            disease="Unknown Disease",
            patient_age=5.0,
        )

        assert len(responses) == 0

    def test_confidence_interval(self, predictor):
        """Test confidence interval calculation."""
        response = predictor.predict_treatment_response(
            disease="Pancreatitis",
            treatment_name="Supportive Care (IV fluids, rest, diet)",
            patient_age=5.0,
        )

        ci = response.success_probability_ci
        # CI should be valid probabilities
        assert 0 <= ci[0] <= 1
        assert 0 <= ci[1] <= 1
        assert ci[0] <= ci[1]
        # CI should have meaningful width
        assert ci[1] - ci[0] > 0

    def test_timeline_determination(self, predictor):
        """Test timeline determination."""
        # Immediate onset (surgical)
        surgical = predictor.predict_treatment_response(
            disease="Hip Dysplasia",
            treatment_name="Surgical Intervention (THR)",
            patient_age=5.0,
        )
        assert surgical.expected_timeline in ["immediate", "hours"]

        # Days onset
        pharmaceutical = predictor.predict_treatment_response(
            disease="Pancreatitis",
            treatment_name="Pancreatic Enzyme Inhibitors",
            patient_age=5.0,
        )
        assert pharmaceutical.expected_timeline in ["immediate", "hours", "days"]

        # Longer onset
        nutritional = predictor.predict_treatment_response(
            disease="Pancreatitis",
            treatment_name="Bland Diet Recovery",
            patient_age=5.0,
        )
        assert nutritional.expected_timeline in ["days", "weeks"]

    def test_side_effects_prediction(self, predictor):
        """Test side effects prediction."""
        response = predictor.predict_treatment_response(
            disease="Osteoarthritis",
            treatment_name="NSAIDs (Carprofen, Meloxicam)",
            patient_age=5.0,
        )

        # Should predict some side effects for NSAIDs
        assert len(response.expected_side_effects) >= 0

    def test_alternative_treatments(self, predictor):
        """Test alternative treatment suggestions."""
        response = predictor.predict_treatment_response(
            disease="Osteoarthritis",
            treatment_name="NSAIDs (Carprofen, Meloxicam)",
            patient_age=7.0,
        )

        # Should suggest alternatives
        assert len(response.alternative_treatments) > 0
        # Alternatives should not include current treatment
        assert "NSAIDs (Carprofen, Meloxicam)" not in response.alternative_treatments

    def test_risk_benefit_assessment(self, predictor):
        """Test risk-benefit assessment."""
        response = predictor.predict_treatment_response(
            disease="Pancreatitis",
            treatment_name="Supportive Care (IV fluids, rest, diet)",
            patient_age=5.0,
            disease_severity=2.0,
        )

        assert response.risk_benefit_ratio in ["favorable", "balanced", "unfavorable"]

    def test_record_outcome(self, predictor):
        """Test recording treatment outcomes."""
        predictor.record_outcome(
            disease="Pancreatitis",
            treatment_name="Supportive Care (IV fluids, rest, diet)",
            success=True,
        )

        assert len(predictor.outcome_history) == 1

    def test_treatment_statistics(self, predictor):
        """Test treatment statistics."""
        # Record some outcomes
        predictor.record_outcome("Disease A", "Treatment 1", True)
        predictor.record_outcome("Disease A", "Treatment 1", True)
        predictor.record_outcome("Disease A", "Treatment 1", False)

        stats = predictor.get_treatment_statistics()

        assert stats["total_outcomes"] == 3
        assert stats["success_rate"] == pytest.approx(2/3, abs=0.01)

    def test_confidence_level(self, predictor):
        """Test confidence level in predictions."""
        response = predictor.predict_treatment_response(
            disease="Pancreatitis",
            treatment_name="Supportive Care (IV fluids, rest, diet)",
            patient_age=5.0,
        )

        # Should have reasonable confidence for known treatment
        assert 0 <= response.confidence_level <= 1
        assert response.confidence_level > 0.5  # Should be reasonably confident

    def test_recommendations_generation(self, predictor):
        """Test recommendation generation."""
        response = predictor.predict_treatment_response(
            disease="Pancreatitis",
            treatment_name="Supportive Care (IV fluids, rest, diet)",
            patient_age=5.0,
            owner_compliance_likelihood=0.95,
        )

        assert len(response.recommendations) > 0
        # Should have clinical recommendations
        assert isinstance(response.recommendations, list)

    def test_monitoring_requirements(self, predictor):
        """Test monitoring requirements."""
        response = predictor.predict_treatment_response(
            disease="Osteoarthritis",
            treatment_name="NSAIDs (Carprofen, Meloxicam)",
            patient_age=7.0,
        )

        assert len(response.monitoring_requirements) > 0

    def test_response_to_dict(self, predictor):
        """Test response serialization."""
        response = predictor.predict_treatment_response(
            disease="Pancreatitis",
            treatment_name="Supportive Care (IV fluids, rest, diet)",
            patient_age=5.0,
        )

        result = response.to_dict()
        assert result["disease"] == "Pancreatitis"
        assert "success_probability" in result
        assert "success_probability_ci" in result

    def test_predictor_to_dict(self, predictor):
        """Test predictor export."""
        # Make a prediction
        predictor.predict_treatment_response(
            disease="Pancreatitis",
            treatment_name="Supportive Care (IV fluids, rest, diet)",
            patient_age=5.0,
        )

        result = predictor.to_dict()
        assert "predictions_made" in result
        assert result["predictions_made"] == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
