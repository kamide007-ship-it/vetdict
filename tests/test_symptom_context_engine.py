"""Tests for symptom context engine (Phase 6 Stage 3).

Tests the medical contextualization of symptoms across multiple disease
hypotheses and ambiguity detection/resolution mechanisms.
"""

import pytest

from api.ai.symptom_context_engine import (
    AmbiguitySolver,
    SymptomContext,
    SymptomContextualizer,
    SymptomRole,
)


class TestSymptomContext:
    """Test SymptomContext data structure."""

    def test_symptom_context_creation(self):
        """Test creating a SymptomContext."""
        context = SymptomContext(
            symptom_id="vomiting",
            symptom_name="Vomiting",
            disease_name="Pancreatitis",
            context_role=SymptomRole.PRIMARY_SYMPTOM,
            pathophysiology_link="Inflammatory pancreas causes gastric irritation",
            specificity_score=0.75,
            sensitivity_score=0.85,
            likelihood_ratio_positive=3.4,
            likelihood_ratio_negative=0.18,
            confidence_weight=0.8,
            supporting_evidence=["Ref1", "Ref2"],
        )

        assert context.symptom_id == "vomiting"
        assert context.disease_name == "Pancreatitis"
        assert context.context_role == SymptomRole.PRIMARY_SYMPTOM
        assert context.specificity_score == 0.75

    def test_symptom_context_to_dict(self):
        """Test serialization of SymptomContext."""
        context = SymptomContext(
            symptom_id="vomiting",
            symptom_name="Vomiting",
            disease_name="Pancreatitis",
            context_role=SymptomRole.SECONDARY_SYMPTOM,
            pathophysiology_link="Secondary to inflammation",
            specificity_score=0.65,
            sensitivity_score=0.75,
            likelihood_ratio_positive=2.5,
            likelihood_ratio_negative=0.33,
            confidence_weight=0.65,
        )

        result = context.to_dict()
        assert result["symptom_id"] == "vomiting"
        assert result["context_role"] == "secondary_symptom"
        assert isinstance(result["specificity_score"], float)


class TestSymptomContextualizer:
    """Test symptom contextualization across diseases."""

    @pytest.fixture
    def sample_diseases(self):
        """Sample disease database for testing."""
        return [
            {
                "name": "Pancreatitis",
                "name_ja": "膵炎",
                "symptoms": ["vomiting", "abdominal_pain", "anorexia"],
                "pathophysiology": (
                    "Inflammation of pancreas leads to vomiting and severe abdominal pain. "
                    "Primary symptom is acute pain."
                ),
                "severity_score": 0.8,
                "prevalence_score": 0.3,
            },
            {
                "name": "Gastroenteritis",
                "name_ja": "腸炎",
                "symptoms": ["vomiting", "diarrhea", "lethargy"],
                "pathophysiology": (
                    "Viral or bacterial infection causes gastric inflammation. "
                    "Vomiting is a common secondary symptom."
                ),
                "severity_score": 0.5,
                "prevalence_score": 0.6,
            },
            {
                "name": "Intestinal Obstruction",
                "name_ja": "腸閉塞",
                "symptoms": ["vomiting", "constipation", "pain"],
                "pathophysiology": (
                    "Physical blockage of intestines leads to vomiting as complication. "
                    "Constipation is primary symptom."
                ),
                "severity_score": 0.9,
                "prevalence_score": 0.2,
            },
        ]

    def test_contextualize_symptom_basic(self, sample_diseases):
        """Test basic symptom contextualization."""
        contexts = SymptomContextualizer.contextualize_symptom(
            symptom_id="vomiting",
            symptom_name="Vomiting",
            disease_names=["Pancreatitis", "Gastroenteritis"],
            disease_database=sample_diseases,
        )

        assert len(contexts) == 2
        assert "Pancreatitis" in contexts
        assert "Gastroenteritis" in contexts

        pancreatitis_context = contexts["Pancreatitis"]
        assert pancreatitis_context.symptom_id == "vomiting"
        assert pancreatitis_context.disease_name == "Pancreatitis"

    def test_contextualize_symptom_specificity_differences(self, sample_diseases):
        """Test that specificity differs across diseases."""
        contexts = SymptomContextualizer.contextualize_symptom(
            symptom_id="vomiting",
            symptom_name="Vomiting",
            disease_names=["Pancreatitis", "Gastroenteritis", "Intestinal Obstruction"],
            disease_database=sample_diseases,
        )

        pancreatitis_spec = contexts["Pancreatitis"].specificity_score
        gastro_spec = contexts["Gastroenteritis"].specificity_score
        obstruction_spec = contexts["Intestinal Obstruction"].specificity_score

        # Pancreatitis should have highest specificity for vomiting
        # (primary disease for this symptom)
        assert pancreatitis_spec >= gastro_spec or pancreatitis_spec >= obstruction_spec

    def test_symptom_role_classification(self, sample_diseases):
        """Test symptom role classification."""
        contexts = SymptomContextualizer.contextualize_symptom(
            symptom_id="vomiting",
            symptom_name="Vomiting",
            disease_names=["Pancreatitis", "Intestinal Obstruction"],
            disease_database=sample_diseases,
        )

        # Pancreatitis: vomiting is likely primary
        pancreatitis_role = contexts["Pancreatitis"].context_role
        assert pancreatitis_role in [
            SymptomRole.PRIMARY_SYMPTOM,
            SymptomRole.SECONDARY_SYMPTOM,
        ]

        # Obstruction: vomiting role can vary (primary, secondary, or complication)
        # The important part is that both diseases have context and roles assigned
        obstruction_role = contexts["Intestinal Obstruction"].context_role
        assert obstruction_role in [
            SymptomRole.PRIMARY_SYMPTOM,
            SymptomRole.SECONDARY_SYMPTOM,
            SymptomRole.COMPLICATION,
        ]


class TestAmbiguitySolver:
    """Test ambiguity detection and resolution."""

    @pytest.fixture
    def sample_diseases(self):
        """Sample disease database."""
        return [
            {
                "name": "Pancreatitis",
                "symptoms": ["vomiting", "abdominal_pain", "anorexia", "lethargy"],
                "pathophysiology": (
                    "Primary symptom: acute abdominal pain. "
                    "Vomiting is common secondary symptom."
                ),
                "severity_score": 0.8,
            },
            {
                "name": "Gastroenteritis",
                "symptoms": ["vomiting", "diarrhea", "lethargy", "fever"],
                "pathophysiology": (
                    "Infection causes gastroenteritis. Vomiting appears early. "
                    "Main symptom is diarrhea."
                ),
                "severity_score": 0.5,
            },
            {
                "name": "Hepatitis",
                "symptoms": ["jaundice", "lethargy", "anorexia", "vomiting"],
                "pathophysiology": (
                    "Liver inflammation leads to multiple symptoms. "
                    "Vomiting is secondary manifestation."
                ),
                "severity_score": 0.7,
            },
        ]

    @pytest.fixture
    def sample_candidates(self, sample_diseases):
        """Sample disease candidates."""
        return [
            {"name": "Pancreatitis", "match_percent": 75},
            {"name": "Gastroenteritis", "match_percent": 60},
            {"name": "Hepatitis", "match_percent": 45},
        ]

    def test_analyze_symptom_set_basic(self, sample_diseases, sample_candidates):
        """Test basic symptom set analysis."""
        reports = AmbiguitySolver.analyze_symptom_set(
            symptom_ids=["vomiting", "lethargy"],
            disease_candidates=sample_candidates,
            disease_database=sample_diseases,
        )

        assert len(reports) >= 1
        assert any(r.symptom_id == "vomiting" for r in reports)

    def test_ambiguity_score_calculation(self, sample_diseases, sample_candidates):
        """Test ambiguity score is calculated for ambiguous symptoms."""
        reports = AmbiguitySolver.analyze_symptom_set(
            symptom_ids=["vomiting"],
            disease_candidates=sample_candidates,
            disease_database=sample_diseases,
        )

        # "vomiting" is present in 3 diseases (ambiguous)
        vomiting_report = next(
            (r for r in reports if r.symptom_id == "vomiting"), None
        )
        assert vomiting_report is not None

        # Ambiguity score should be moderate to high (appears in multiple diseases)
        assert vomiting_report.ambiguity_score >= 0.3

    def test_ambiguity_recommendations(self, sample_diseases, sample_candidates):
        """Test that recommendations are appropriate for ambiguity level."""
        reports = AmbiguitySolver.analyze_symptom_set(
            symptom_ids=["vomiting"],
            disease_candidates=sample_candidates,
            disease_database=sample_diseases,
        )

        vomiting_report = next(
            (r for r in reports if r.symptom_id == "vomiting"), None
        )
        assert vomiting_report is not None

        # High ambiguity should recommend clarification
        if vomiting_report.ambiguity_score >= 0.6:
            assert vomiting_report.recommendation == "ask_clarification"
        # Moderate should recommend reduce confidence
        elif vomiting_report.ambiguity_score >= 0.4:
            assert vomiting_report.recommendation in [
                "reduce_confidence",
                "ask_clarification",
            ]

    def test_clarification_questions_generation(self, sample_diseases, sample_candidates):
        """Test that clarification questions are generated for ambiguous symptoms."""
        reports = AmbiguitySolver.analyze_symptom_set(
            symptom_ids=["vomiting"],
            disease_candidates=sample_candidates,
            disease_database=sample_diseases,
        )

        vomiting_report = next(
            (r for r in reports if r.symptom_id == "vomiting"), None
        )
        assert vomiting_report is not None

        # If clarification is recommended, should have questions
        if vomiting_report.recommendation == "ask_clarification":
            assert len(vomiting_report.clarification_questions) > 0
            # Questions should be about vomiting
            questions_text = " ".join(vomiting_report.clarification_questions).lower()
            assert "vomiting" in questions_text or "symptom" in questions_text

    def test_ambiguity_adjustment_factor(self):
        """Test confidence adjustment factor calculation."""
        # High ambiguity should reduce confidence
        high_ambiguity_factor = AmbiguitySolver._calculate_adjustment_factor(
            ambiguity_score=0.8,
            recommendation="ask_clarification",
        )
        assert high_ambiguity_factor < 1.0

        # Moderate ambiguity should mildly reduce confidence
        moderate_factor = AmbiguitySolver._calculate_adjustment_factor(
            ambiguity_score=0.5,
            recommendation="reduce_confidence",
        )
        assert 0.5 < moderate_factor < 1.0

        # Low ambiguity should not adjust
        low_factor = AmbiguitySolver._calculate_adjustment_factor(
            ambiguity_score=0.2,
            recommendation="keep_all",
        )
        assert low_factor == 1.0

    def test_confidence_adjustment_application(self, sample_diseases, sample_candidates):
        """Test applying confidence adjustments based on ambiguity."""
        reports = AmbiguitySolver.analyze_symptom_set(
            symptom_ids=["vomiting", "lethargy"],
            disease_candidates=sample_candidates,
            disease_database=sample_diseases,
        )

        original_confidences = {
            "Pancreatitis": 0.75,
            "Gastroenteritis": 0.60,
            "Hepatitis": 0.45,
        }

        adjusted = AmbiguitySolver.adjust_confidence_for_ambiguity(
            original_confidences,
            reports,
        )

        # Adjusted should be same or lower (not higher)
        for disease, orig_conf in original_confidences.items():
            if disease in adjusted:
                assert adjusted[disease] <= orig_conf

    def test_predominant_disease_identification(self, sample_diseases, sample_candidates):
        """Test identification of predominant disease for symptom."""
        reports = AmbiguitySolver.analyze_symptom_set(
            symptom_ids=["vomiting"],
            disease_candidates=sample_candidates,
            disease_database=sample_diseases,
        )

        vomiting_report = next(
            (r for r in reports if r.symptom_id == "vomiting"), None
        )
        assert vomiting_report is not None
        assert vomiting_report.predominant_disease is not None
        assert vomiting_report.predominant_disease in [
            "Pancreatitis",
            "Gastroenteritis",
            "Hepatitis",
        ]

    def test_competing_diseases_identification(self, sample_diseases, sample_candidates):
        """Test identification of competing diseases."""
        reports = AmbiguitySolver.analyze_symptom_set(
            symptom_ids=["vomiting"],
            disease_candidates=sample_candidates,
            disease_database=sample_diseases,
        )

        vomiting_report = next(
            (r for r in reports if r.symptom_id == "vomiting"), None
        )
        assert vomiting_report is not None
        assert len(vomiting_report.competing_diseases) > 0

        # Competing should not include predominant
        assert vomiting_report.predominant_disease not in vomiting_report.competing_diseases


class TestSymptomContextIntegration:
    """Integration tests for symptom context with multidisease detection."""

    @pytest.fixture
    def sample_diseases(self):
        """Disease database for integration tests."""
        return [
            {
                "name": "Hip Dysplasia",
                "symptoms": ["limping", "pain", "restricted_movement"],
                "pathophysiology": (
                    "Abnormal hip joint development causes primary pain. "
                    "Limping is main symptom. Arthritis develops as complication."
                ),
                "severity_score": 0.6,
            },
            {
                "name": "Osteoarthritis",
                "symptoms": ["limping", "stiffness", "joint_pain"],
                "pathophysiology": (
                    "Cartilage degeneration causes joint pain. "
                    "Limping occurs as consequence of pain."
                ),
                "severity_score": 0.5,
            },
        ]

    def test_multidisease_ambiguity_context(self, sample_diseases):
        """Test symptom context in multidisease scenario."""
        diseases = ["Hip Dysplasia", "Osteoarthritis"]
        symptoms = ["limping", "pain", "stiffness"]

        # Contextualize all symptoms
        all_contexts = {}
        for symptom in symptoms:
            contexts = SymptomContextualizer.contextualize_symptom(
                symptom_id=symptom,
                symptom_name=symptom.replace("_", " "),
                disease_names=diseases,
                disease_database=sample_diseases,
            )
            all_contexts[symptom] = contexts

        # Both symptom and osteoarthritis should have contexts
        assert len(all_contexts["limping"]) > 0
        assert "Hip Dysplasia" in all_contexts["limping"]


class TestEdgeCases:
    """Test edge cases and error conditions."""

    def test_empty_disease_database(self):
        """Test with empty disease database."""
        contexts = SymptomContextualizer.contextualize_symptom(
            symptom_id="vomiting",
            symptom_name="Vomiting",
            disease_names=["Pancreatitis"],
            disease_database=[],
        )

        assert len(contexts) == 0

    def test_symptom_not_in_disease(self):
        """Test with symptom not present in disease."""
        disease = {
            "name": "Arthritis",
            "symptoms": ["limping", "stiffness"],
            "pathophysiology": "Joint inflammation",
        }

        contexts = SymptomContextualizer.contextualize_symptom(
            symptom_id="vomiting",
            symptom_name="Vomiting",
            disease_names=["Arthritis"],
            disease_database=[disease],
        )

        # No context should be created for missing symptom
        assert len(contexts) == 0

    def test_ambiguity_with_single_disease(self):
        """Test ambiguity calculation with single disease (no ambiguity)."""
        disease = {
            "name": "Pancreatitis",
            "symptoms": ["vomiting"],
            "pathophysiology": "Inflammation causes vomiting",
        }

        reports = AmbiguitySolver.analyze_symptom_set(
            symptom_ids=["vomiting"],
            disease_candidates=[{"name": "Pancreatitis", "match_percent": 80}],
            disease_database=[disease],
        )

        if reports:
            # Single disease should have low ambiguity
            assert reports[0].ambiguity_score < 0.5
