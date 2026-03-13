"""Tests for combined confidence scoring (Phase 6 Stage 4).

Tests Bayesian statistical methods for calculating combined disease
confidence scores with transparent breakdowns.
"""

import pytest
from api.ai.combined_confidence_calculator import (
    CombinedConfidenceCalculator,
    BayesianDiseaseCombiner,
    ConfidenceBreakdown,
)


class TestConfidenceBreakdown:
    """Test ConfidenceBreakdown data structure."""

    def test_confidence_breakdown_creation(self):
        """Test creating a ConfidenceBreakdown."""
        breakdown = ConfidenceBreakdown(
            diseases=["Disease A", "Disease B"],
            individual_confidences={"Disease A": 0.6, "Disease B": 0.5},
            symptom_allocation={"Disease A": ["symptom1"], "Disease B": ["symptom2"]},
            comorbidity_multiplier=1.2,
            independence_penalty=0.95,
            bayesian_posterior=0.35,
            evidence_integration_scores={"Disease A": 0.8, "Disease B": 0.7},
            symptom_likelihood_breakdown={"Disease A": {"symptom1": 1.0}},
            final_confidence=0.32,
            confidence_sources=["bayesian", "comorbidity_db"],
            explanation_en="Combined diagnosis explanation",
        )

        assert breakdown.diseases == ["Disease A", "Disease B"]
        assert breakdown.final_confidence == 0.32
        assert "bayesian" in breakdown.confidence_sources

    def test_confidence_breakdown_to_dict(self):
        """Test serialization of ConfidenceBreakdown."""
        breakdown = ConfidenceBreakdown(
            diseases=["Hip Dysplasia", "Osteoarthritis"],
            individual_confidences={"Hip Dysplasia": 0.7, "Osteoarthritis": 0.6},
            symptom_allocation={
                "Hip Dysplasia": ["limping"],
                "Osteoarthritis": ["stiffness"],
            },
            comorbidity_multiplier=1.15,
            independence_penalty=0.9,
            bayesian_posterior=0.45,
            evidence_integration_scores={
                "Hip Dysplasia": 0.85,
                "Osteoarthritis": 0.75,
            },
            symptom_likelihood_breakdown={},
            final_confidence=0.40,
            confidence_sources=["bayesian", "comorbidity_db"],
        )

        result = breakdown.to_dict()
        assert result["diseases"] == ["Hip Dysplasia", "Osteoarthritis"]
        assert isinstance(result["final_confidence"], float)
        assert result["final_confidence"] == 0.4


class TestCombinedConfidenceCalculator:
    """Test Bayesian combined confidence calculator."""

    @pytest.fixture
    def sample_symptom_mapping(self):
        """Sample symptom to disease mapping."""
        return {
            "limping": {"Hip Dysplasia", "Osteoarthritis", "Ligament Tear"},
            "pain": {"Hip Dysplasia", "Osteoarthritis", "Fracture"},
            "stiffness": {"Osteoarthritis", "Hip Dysplasia"},
            "swelling": {"Ligament Tear", "Fracture"},
            "heat": {"Inflammation"},
        }

    def test_calculate_bayesian_single_disease(self):
        """Test Bayesian calculation for single disease."""
        breakdown = CombinedConfidenceCalculator.calculate_bayesian_combination(
            diseases=["Pancreatitis"],
            individual_confidences={"Pancreatitis": 0.8},
            detected_symptoms=[],
            symptom_disease_mapping={},
        )

        assert len(breakdown.diseases) == 1
        assert breakdown.final_confidence == 0.8
        assert breakdown.diseases == ["Pancreatitis"]

    def test_calculate_bayesian_two_diseases(self, sample_symptom_mapping):
        """Test Bayesian combination for two diseases."""
        breakdown = CombinedConfidenceCalculator.calculate_bayesian_combination(
            diseases=["Hip Dysplasia", "Osteoarthritis"],
            individual_confidences={"Hip Dysplasia": 0.7, "Osteoarthritis": 0.6},
            detected_symptoms=["limping", "pain", "stiffness"],
            symptom_disease_mapping=sample_symptom_mapping,
        )

        assert len(breakdown.diseases) == 2
        assert breakdown.final_confidence > 0.0
        assert breakdown.final_confidence <= 1.0
        assert "Hip Dysplasia" in breakdown.individual_confidences
        assert "Osteoarthritis" in breakdown.individual_confidences

    def test_symptom_allocation_correctness(self, sample_symptom_mapping):
        """Test that symptoms are allocated correctly."""
        breakdown = CombinedConfidenceCalculator.calculate_bayesian_combination(
            diseases=["Hip Dysplasia", "Osteoarthritis"],
            individual_confidences={"Hip Dysplasia": 0.7, "Osteoarthritis": 0.6},
            detected_symptoms=["limping", "pain", "stiffness"],
            symptom_disease_mapping=sample_symptom_mapping,
        )

        # Check symptom allocation
        assert "Hip Dysplasia" in breakdown.symptom_allocation
        assert "Osteoarthritis" in breakdown.symptom_allocation

        # Each disease should have at least some symptoms
        hd_symptoms = breakdown.symptom_allocation["Hip Dysplasia"]
        oa_symptoms = breakdown.symptom_allocation["Osteoarthritis"]

        # Check that allocated symptoms are from detected
        all_allocated = set(hd_symptoms) | set(oa_symptoms)
        assert all_allocated.issubset(
            set(["limping", "pain", "stiffness"])
        )

    def test_independence_penalty_calculation(self):
        """Test that symptom overlap results in penalty."""
        # High overlap scenario (competing diagnoses)
        breakdown_high_overlap = CombinedConfidenceCalculator.calculate_bayesian_combination(
            diseases=["Disease A", "Disease B"],
            individual_confidences={"Disease A": 0.8, "Disease B": 0.7},
            detected_symptoms=["symptom1", "symptom2", "symptom3"],
            symptom_disease_mapping={
                "symptom1": {"Disease A", "Disease B"},
                "symptom2": {"Disease A", "Disease B"},
                "symptom3": {"Disease A", "Disease B"},
            },
        )

        # Low overlap scenario (complementary diagnoses)
        breakdown_low_overlap = CombinedConfidenceCalculator.calculate_bayesian_combination(
            diseases=["Disease A", "Disease B"],
            individual_confidences={"Disease A": 0.8, "Disease B": 0.7},
            detected_symptoms=["symptom1", "symptom2", "symptom3"],
            symptom_disease_mapping={
                "symptom1": {"Disease A"},
                "symptom2": {"Disease B"},
                "symptom3": {"Disease A", "Disease B"},
            },
        )

        # Low overlap should have higher confidence (less independence penalty)
        assert breakdown_low_overlap.final_confidence >= breakdown_high_overlap.final_confidence

    def test_comorbidity_multiplier_application(self):
        """Test that comorbidity data increases combined confidence."""
        # Without comorbidity data
        breakdown_no_comorb = CombinedConfidenceCalculator.calculate_bayesian_combination(
            diseases=["Hip Dysplasia", "Osteoarthritis"],
            individual_confidences={"Hip Dysplasia": 0.6, "Osteoarthritis": 0.5},
            detected_symptoms=["limping"],
            symptom_disease_mapping={"limping": {"Hip Dysplasia", "Osteoarthritis"}},
            comorbidity_data=None,
        )

        # With comorbidity data (high probability of coexistence)
        breakdown_with_comorb = CombinedConfidenceCalculator.calculate_bayesian_combination(
            diseases=["Hip Dysplasia", "Osteoarthritis"],
            individual_confidences={"Hip Dysplasia": 0.6, "Osteoarthritis": 0.5},
            detected_symptoms=["limping"],
            symptom_disease_mapping={"limping": {"Hip Dysplasia", "Osteoarthritis"}},
            comorbidity_data={("Hip Dysplasia", "Osteoarthritis"): 1.5},
        )

        # With comorbidity support, confidence should be higher
        assert breakdown_with_comorb.final_confidence >= breakdown_no_comorb.final_confidence

    def test_age_factor_in_comorbidity(self):
        """Test that age affects comorbidity probability."""
        # Young animal
        breakdown_young = CombinedConfidenceCalculator.calculate_bayesian_combination(
            diseases=["Hip Dysplasia", "Osteoarthritis"],
            individual_confidences={"Hip Dysplasia": 0.6, "Osteoarthritis": 0.5},
            detected_symptoms=["limping"],
            symptom_disease_mapping={"limping": {"Hip Dysplasia", "Osteoarthritis"}},
            patient_context={"age_years": 2},
        )

        # Old animal
        breakdown_old = CombinedConfidenceCalculator.calculate_bayesian_combination(
            diseases=["Hip Dysplasia", "Osteoarthritis"],
            individual_confidences={"Hip Dysplasia": 0.6, "Osteoarthritis": 0.5},
            detected_symptoms=["limping"],
            symptom_disease_mapping={"limping": {"Hip Dysplasia", "Osteoarthritis"}},
            patient_context={"age_years": 10},
        )

        # Older animals should have higher comorbidity multiplier
        assert breakdown_old.comorbidity_multiplier >= breakdown_young.comorbidity_multiplier

    def test_confidence_breakdown_explanation_en(self):
        """Test English explanation generation."""
        breakdown = CombinedConfidenceCalculator.calculate_bayesian_combination(
            diseases=["Hip Dysplasia", "Osteoarthritis"],
            individual_confidences={"Hip Dysplasia": 0.7, "Osteoarthritis": 0.6},
            detected_symptoms=["limping"],
            symptom_disease_mapping={"limping": {"Hip Dysplasia", "Osteoarthritis"}},
        )

        assert len(breakdown.explanation_en) > 0
        assert "Hip Dysplasia" in breakdown.explanation_en or "Osteoarthritis" in breakdown.explanation_en

    def test_confidence_breakdown_explanation_ja(self):
        """Test Japanese explanation generation."""
        breakdown = CombinedConfidenceCalculator.calculate_bayesian_combination(
            diseases=["股関節形成不全", "変形性関節症"],
            individual_confidences={"股関節形成不全": 0.7, "変形性関節症": 0.6},
            detected_symptoms=["跛行"],
            symptom_disease_mapping={"跛行": {"股関節形成不全", "変形性関節症"}},
        )

        assert len(breakdown.explanation_ja) > 0

    def test_confidence_sources_tracking(self):
        """Test that confidence sources are properly tracked."""
        breakdown = CombinedConfidenceCalculator.calculate_bayesian_combination(
            diseases=["Hip Dysplasia", "Osteoarthritis"],
            individual_confidences={"Hip Dysplasia": 0.7, "Osteoarthritis": 0.6},
            detected_symptoms=["limping"],
            symptom_disease_mapping={"limping": {"Hip Dysplasia", "Osteoarthritis"}},
            comorbidity_data={("Hip Dysplasia", "Osteoarthritis"): 1.2},
            evidence_scores={"Hip Dysplasia": 0.9, "Osteoarthritis": 0.8},
        )

        assert "bayesian_combination" in breakdown.confidence_sources
        assert "comorbidity_database" in breakdown.confidence_sources
        assert "evidence_quality" in breakdown.confidence_sources

    def test_final_confidence_bounds(self):
        """Test that final confidence stays within 0-1 bounds."""
        breakdown = CombinedConfidenceCalculator.calculate_bayesian_combination(
            diseases=["Disease A", "Disease B"],
            individual_confidences={"Disease A": 0.99, "Disease B": 0.98},
            detected_symptoms=[],
            symptom_disease_mapping={},
        )

        assert 0.0 <= breakdown.final_confidence <= 1.0

    def test_three_disease_combination(self):
        """Test Bayesian calculation with three diseases."""
        breakdown = CombinedConfidenceCalculator.calculate_bayesian_combination(
            diseases=["Disease A", "Disease B", "Disease C"],
            individual_confidences={
                "Disease A": 0.6,
                "Disease B": 0.5,
                "Disease C": 0.4,
            },
            detected_symptoms=["sym1", "sym2", "sym3"],
            symptom_disease_mapping={
                "sym1": {"Disease A"},
                "sym2": {"Disease B"},
                "sym3": {"Disease C"},
            },
        )

        assert len(breakdown.diseases) == 3
        assert 0.0 <= breakdown.final_confidence <= 1.0


class TestBayesianDiseaseCombiner:
    """Test high-level Bayesian disease combiner."""

    def test_combine_two_diseases(self):
        """Test combining two diseases."""
        confidence, breakdown = BayesianDiseaseCombiner.combine_multiple_diseases(
            disease_list=["Hip Dysplasia", "Osteoarthritis"],
            confidences=[0.7, 0.6],
        )

        assert isinstance(confidence, float)
        assert 0.0 <= confidence <= 1.0
        assert isinstance(breakdown, ConfidenceBreakdown)

    def test_combine_with_interaction_matrix(self):
        """Test combining diseases with interaction data."""
        interaction_matrix = {
            ("Hip Dysplasia", "Osteoarthritis"): 1.3,
            ("Pancreatitis", "Gastroenteritis"): 0.7,
        }

        confidence, breakdown = BayesianDiseaseCombiner.combine_multiple_diseases(
            disease_list=["Hip Dysplasia", "Osteoarthritis"],
            confidences=[0.7, 0.6],
            interaction_matrix=interaction_matrix,
        )

        assert confidence > 0.0
        assert "comorbidity_database" in breakdown.confidence_sources

    def test_empty_disease_list(self):
        """Test handling of empty disease list."""
        confidence, breakdown = BayesianDiseaseCombiner.combine_multiple_diseases(
            disease_list=[],
            confidences=[],
        )

        assert confidence == 0.0
        assert len(breakdown.diseases) == 0


class TestCombinedConfidenceEdgeCases:
    """Test edge cases in confidence calculation."""

    def test_zero_confidences(self):
        """Test with zero individual confidences."""
        breakdown = CombinedConfidenceCalculator.calculate_bayesian_combination(
            diseases=["Disease A", "Disease B"],
            individual_confidences={"Disease A": 0.0, "Disease B": 0.0},
            detected_symptoms=[],
            symptom_disease_mapping={},
        )

        assert breakdown.final_confidence == 0.0

    def test_one_high_one_low_confidence(self):
        """Test with one high and one low confidence."""
        breakdown = CombinedConfidenceCalculator.calculate_bayesian_combination(
            diseases=["Disease A", "Disease B"],
            individual_confidences={"Disease A": 0.95, "Disease B": 0.05},
            detected_symptoms=[],
            symptom_disease_mapping={},
        )

        # Combined should be low if one component is low
        assert breakdown.final_confidence < 0.5

    def test_perfect_symptom_allocation(self):
        """Test when each disease has unique symptoms."""
        breakdown = CombinedConfidenceCalculator.calculate_bayesian_combination(
            diseases=["Disease A", "Disease B"],
            individual_confidences={"Disease A": 0.7, "Disease B": 0.6},
            detected_symptoms=["sym_a", "sym_b"],
            symptom_disease_mapping={
                "sym_a": {"Disease A"},
                "sym_b": {"Disease B"},
            },
        )

        # Perfect allocation should result in no independence penalty
        assert breakdown.independence_penalty == 1.0

    def test_overlapping_symptoms(self):
        """Test when diseases share all symptoms."""
        breakdown = CombinedConfidenceCalculator.calculate_bayesian_combination(
            diseases=["Disease A", "Disease B"],
            individual_confidences={"Disease A": 0.7, "Disease B": 0.6},
            detected_symptoms=["sym1", "sym2"],
            symptom_disease_mapping={
                "sym1": {"Disease A", "Disease B"},
                "sym2": {"Disease A", "Disease B"},
            },
        )

        # When all symptoms could belong to multiple diseases but are allocated
        # to one, the algorithm correctly identifies this as low confidence
        # for the combined diagnosis (one disease explains everything)
        assert breakdown.final_confidence < 0.7  # Less than primary disease confidence
