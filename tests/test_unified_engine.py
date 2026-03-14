"""Integration tests for unified clinical engine.

Tests complete workflows across all Stage 1-4 components.
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from api.ai.unified_clinical_engine import (
    UnifiedClinicalEngine,
    ClinicalCase,
    DiagnosticWorkflow,
)
from api.ai.multidisease_expander import (
    DiseaseInteraction,
    InteractionType,
)


class TestUnifiedClinicalEngine:
    """Test unified clinical engine integration."""

    @pytest.fixture
    def engine(self):
        """Create engine instance."""
        return UnifiedClinicalEngine()

    @pytest.fixture
    def sample_interaction_matrix(self):
        """Create sample interaction matrix."""
        interactions = {}

        interactions[("Pancreatitis", "Diabetes Mellitus")] = DiseaseInteraction(
            disease_a="Pancreatitis",
            disease_b="Diabetes Mellitus",
            interaction_type=InteractionType.CASCADE,
            base_probability=0.60,
            mechanism="endocrine_dysfunction",
            age_factor=1.05,
            severity_factor=0.85,
        )

        interactions[("Diabetes Mellitus", "Kidney Disease")] = DiseaseInteraction(
            disease_a="Diabetes Mellitus",
            disease_b="Kidney Disease",
            interaction_type=InteractionType.SECONDARY,
            base_probability=0.70,
            mechanism="diabetic_nephropathy",
            age_factor=1.2,
            severity_factor=1.3,
        )

        return interactions

    def test_engine_initialization(self, engine):
        """Test engine initialization."""
        assert engine is not None
        assert engine.confidence_calculator is not None
        assert engine.prognostic_predictor is not None
        assert engine.treatment_predictor is not None

    def test_initialize_expander(self, engine, sample_interaction_matrix):
        """Test expander initialization."""
        engine.initialize_expander(sample_interaction_matrix)
        assert engine.expander is not None

    def test_comprehensive_analysis_workflow(self, engine, sample_interaction_matrix):
        """Test complete diagnostic workflow."""
        engine.initialize_expander(sample_interaction_matrix)

        case = ClinicalCase(
            case_id="case_001",
            patient_age=6.0,
            patient_species="dog",
            symptoms=["vomiting", "lethargy"],
            disease_severity=7.0,
            comorbidities=["Diabetes Mellitus"],
            veterinarian_id="vet_001",
            clinic_id="clinic_001",
        )

        initial_predictions = {
            "Pancreatitis": 0.80,
            "Gastroenteritis": 0.60,
            "Kidney Disease": 0.40,
        }

        diagnosis = engine.comprehensive_analysis(case, initial_predictions)

        # Verify complete diagnosis
        assert diagnosis.case_id == "case_001"
        assert diagnosis.primary_diagnosis is not None
        assert len(diagnosis.differential_diagnoses) > 0
        assert diagnosis.prognosis is not None
        assert diagnosis.treatment_recommendations is not None
        assert 0 <= diagnosis.confidence_level <= 1

    def test_workflow_logging(self, engine, sample_interaction_matrix):
        """Test workflow progression logging."""
        engine.initialize_expander(sample_interaction_matrix)

        case = ClinicalCase(
            case_id="case_002",
            patient_age=5.0,
            patient_species="dog",
            symptoms=["vomiting"],
            disease_severity=5.0,
        )

        initial_predictions = {"Pancreatitis": 0.75}

        engine.comprehensive_analysis(case, initial_predictions)

        # Should have logged multiple workflow stages
        assert len(engine.workflow_log) > 0
        assert any(log[1] == DiagnosticWorkflow.INITIAL_ASSESSMENT
                  for log in engine.workflow_log)
        assert any(log[1] == DiagnosticWorkflow.TREATMENT_PLANNING
                  for log in engine.workflow_log)

    def test_record_diagnosis_outcome(self, engine, sample_interaction_matrix):
        """Test outcome recording."""
        engine.initialize_expander(sample_interaction_matrix)

        # First, create a diagnosis
        case = ClinicalCase(
            case_id="case_003",
            patient_age=5.0,
            patient_species="dog",
            symptoms=["vomiting"],
            disease_severity=5.0,
            veterinarian_id="vet_001",
            clinic_id="clinic_001",
        )

        initial_predictions = {"Pancreatitis": 0.75, "Gastroenteritis": 0.60}
        diagnosis = engine.comprehensive_analysis(case, initial_predictions)

        # Record outcome
        engine.record_diagnosis_outcome(
            case_id="case_003",
            actual_diagnosis="Pancreatitis",
            treatment_used="Supportive Care",
            treatment_success=True,
        )

        # Verify feedback was collected
        stats = engine.confidence_calculator.get_feedback_statistics()
        assert stats["total_records"] > 0

    def test_export_import_case(self, engine, sample_interaction_matrix):
        """Test case export and import."""
        engine.initialize_expander(sample_interaction_matrix)

        case = ClinicalCase(
            case_id="case_004",
            patient_age=5.0,
            patient_species="dog",
            symptoms=["vomiting"],
            disease_severity=5.0,
        )

        initial_predictions = {"Pancreatitis": 0.75}
        diagnosis = engine.comprehensive_analysis(case, initial_predictions)

        # Export
        case_data = engine.export_case("case_004")
        assert case_data is not None
        assert case_data["case_id"] == "case_004"

        # Import
        success = engine.import_case(case_data)
        assert success is True

    def test_clinical_summary_generation(self, engine, sample_interaction_matrix):
        """Test human-readable clinical summary."""
        engine.initialize_expander(sample_interaction_matrix)

        case = ClinicalCase(
            case_id="case_005",
            patient_age=5.0,
            patient_species="dog",
            symptoms=["vomiting"],
            disease_severity=5.0,
        )

        initial_predictions = {"Pancreatitis": 0.75}
        engine.comprehensive_analysis(case, initial_predictions)

        summary = engine.get_clinical_summary("case_005")
        assert summary is not None
        assert "case_005" in summary
        assert "CLINICAL SUMMARY" in summary

    def test_system_statistics(self, engine, sample_interaction_matrix):
        """Test system statistics generation."""
        engine.initialize_expander(sample_interaction_matrix)

        # Run a few analyses
        for i in range(3):
            case = ClinicalCase(
                case_id=f"case_{i:03d}",
                patient_age=5.0,
                patient_species="dog",
                symptoms=["vomiting"],
                disease_severity=5.0,
            )

            initial_predictions = {"Pancreatitis": 0.75}
            engine.comprehensive_analysis(case, initial_predictions)

        stats = engine.get_system_statistics()

        assert stats["total_cases_analyzed"] == 3
        assert "confidence_feedback" in stats
        assert "treatment_outcomes" in stats

    def test_multiple_diagnoses(self, engine, sample_interaction_matrix):
        """Test handling multiple concurrent diagnoses."""
        engine.initialize_expander(sample_interaction_matrix)

        for i in range(5):
            case = ClinicalCase(
                case_id=f"multi_{i}",
                patient_age=5.0 + i,
                patient_species="dog",
                symptoms=["symptom_a", "symptom_b"],
                disease_severity=5.0 + i,
            )

            initial_predictions = {
                "Pancreatitis": max(0.5, 0.75 - i * 0.05),
                "Gastroenteritis": 0.60,
            }
            engine.comprehensive_analysis(case, initial_predictions)

        assert len(engine.diagnoses) == 5

    def test_treatment_recommendations_quality(self, engine, sample_interaction_matrix):
        """Test quality of treatment recommendations."""
        engine.initialize_expander(sample_interaction_matrix)

        case = ClinicalCase(
            case_id="case_treat",
            patient_age=5.0,
            patient_species="dog",
            symptoms=["vomiting"],
            disease_severity=5.0,
        )

        initial_predictions = {"Pancreatitis": 0.85}
        diagnosis = engine.comprehensive_analysis(case, initial_predictions)

        # Treatment recommendations should exist
        assert diagnosis.treatment_recommendations is not None
        if diagnosis.treatment_recommendations:
            # Should be sorted by success probability
            for i in range(len(diagnosis.treatment_recommendations) - 1):
                assert (diagnosis.treatment_recommendations[i].success_probability >=
                       diagnosis.treatment_recommendations[i + 1].success_probability)

    def test_monitoring_plan_generation(self, engine, sample_interaction_matrix):
        """Test monitoring plan generation."""
        engine.initialize_expander(sample_interaction_matrix)

        case = ClinicalCase(
            case_id="case_monitor",
            patient_age=5.0,
            patient_species="dog",
            symptoms=["vomiting"],
            disease_severity=8.0,  # Severe
        )

        initial_predictions = {"Pancreatitis": 0.80}
        diagnosis = engine.comprehensive_analysis(case, initial_predictions)

        # High severity should have detailed monitoring
        assert len(diagnosis.monitoring_plan) > 0
        # For severe disease (8.0), should include intensive monitoring
        monitoring_text = " ".join(diagnosis.monitoring_plan).lower()
        assert "monitoring" in monitoring_text or "assessment" in monitoring_text

    def test_confidence_level_calculation(self, engine, sample_interaction_matrix):
        """Test overall confidence calculation."""
        engine.initialize_expander(sample_interaction_matrix)

        # High confidence case
        high_conf_case = ClinicalCase(
            case_id="high_conf",
            patient_age=5.0,
            patient_species="dog",
            symptoms=["vomiting"],
            disease_severity=3.0,
        )

        high_conf_predictions = {"Pancreatitis": 0.95}
        high_diagnosis = engine.comprehensive_analysis(
            high_conf_case, high_conf_predictions
        )

        # Low confidence case
        low_conf_case = ClinicalCase(
            case_id="low_conf",
            patient_age=5.0,
            patient_species="dog",
            symptoms=["symptom"],
            disease_severity=9.0,
        )

        low_conf_predictions = {"Disease_A": 0.45, "Disease_B": 0.40}
        low_diagnosis = engine.comprehensive_analysis(
            low_conf_case, low_conf_predictions
        )

        # High confidence case should have higher confidence level
        assert high_diagnosis.confidence_level >= low_diagnosis.confidence_level

    def test_differentials_identification(self, engine, sample_interaction_matrix):
        """Test differential diagnosis identification."""
        engine.initialize_expander(sample_interaction_matrix)

        case = ClinicalCase(
            case_id="diff_test",
            patient_age=5.0,
            patient_species="dog",
            symptoms=["vomiting"],
            disease_severity=5.0,
        )

        initial_predictions = {
            "Pancreatitis": 0.80,
            "Gastroenteritis": 0.65,
            "Kidney Disease": 0.45,
        }

        diagnosis = engine.comprehensive_analysis(case, initial_predictions)

        # Primary should be highest probability
        assert diagnosis.primary_diagnosis == "Pancreatitis"

        # Differentials should exist and be sorted
        assert len(diagnosis.differential_diagnoses) > 0
        for i in range(len(diagnosis.differential_diagnoses) - 1):
            assert (diagnosis.differential_diagnoses[i][1] >=
                   diagnosis.differential_diagnoses[i + 1][1])

    def test_to_dict_export(self, engine, sample_interaction_matrix):
        """Test exporting engine state."""
        engine.initialize_expander(sample_interaction_matrix)

        case = ClinicalCase(
            case_id="export_test",
            patient_age=5.0,
            patient_species="dog",
            symptoms=["vomiting"],
            disease_severity=5.0,
        )

        initial_predictions = {"Pancreatitis": 0.75}
        engine.comprehensive_analysis(case, initial_predictions)

        state = engine.to_dict()

        assert "cases_analyzed" in state
        assert state["cases_analyzed"] == 1
        assert "system_statistics" in state


class TestClinicalAPIIntegration:
    """Test API handler integration with engine."""

    def test_api_handler_initialization(self):
        """Test API handler can be initialized."""
        try:
            from api.routes.clinical_api import ClinicalAPIHandler

            engine = UnifiedClinicalEngine()
            handler = ClinicalAPIHandler(engine)

            assert handler.engine is not None
        except ImportError:
            # Flask not installed, skip this test
            pytest.skip("Flask not available for API testing")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
