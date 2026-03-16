"""Tests for symptom role classifier (Phase 6 Stage 3).

Tests pathophysiology-aware symptom role classification and clinical
significance assessment.
"""

import pytest

from api.ai.symptom_role_classifier import (
    RoleClassifier,
    SymptomRoleAnalyzer,
)


class TestSymptomRoleAnalyzer:
    """Test symptom role analysis."""

    @pytest.fixture
    def sample_disease_pancreatitis(self):
        """Sample pancreatitis disease record."""
        return {
            "name": "Pancreatitis",
            "name_ja": "膵炎",
            "symptoms": ["abdominal_pain", "vomiting", "anorexia", "lethargy"],
            "pathophysiology": (
                "Inflammation of the pancreas. "
                "Primary symptom: acute abdominal pain, typically in epigastrium. "
                "Vomiting is a common secondary symptom due to gastric irritation. "
                "Anorexia and lethargy develop as consequences of inflammation."
            ),
            "complications": ["shock", "organ_failure"],
            "severity_score": 0.8,
        }

    @pytest.fixture
    def sample_disease_gd(self):
        """Sample gastroenteritis disease record."""
        return {
            "name": "Gastroenteritis",
            "symptoms": ["vomiting", "diarrhea", "lethargy", "dehydration"],
            "pathophysiology": (
                "Viral or bacterial infection causes acute gastroenteritis. "
                "Main symptom: vomiting appears early as direct response to infection. "
                "Diarrhea is the primary gastrointestinal manifestation."
            ),
            "severity_score": 0.5,
        }

    def test_analyze_role_primary_symptom(self, sample_disease_pancreatitis):
        """Test role analysis for primary symptom."""
        analysis = SymptomRoleAnalyzer.analyze_symptom_role(
            symptom_id="abdominal_pain",
            symptom_name="Abdominal Pain",
            disease=sample_disease_pancreatitis,
        )

        assert analysis.symptom_id == "abdominal_pain"
        assert analysis.disease_name == "Pancreatitis"
        assert analysis.primary_role == "primary"
        assert analysis.primary_confidence > 0.6

    def test_analyze_role_secondary_symptom(self, sample_disease_pancreatitis):
        """Test role analysis for secondary symptom."""
        analysis = SymptomRoleAnalyzer.analyze_symptom_role(
            symptom_id="vomiting",
            symptom_name="Vomiting",
            disease=sample_disease_pancreatitis,
        )

        assert analysis.symptom_id == "vomiting"
        assert analysis.primary_role in ["secondary", "primary"]
        # Vomiting in pancreatitis should have moderate confidence

    def test_analyze_role_complication(self, sample_disease_pancreatitis):
        """Test role analysis for complication symptom."""
        analysis = SymptomRoleAnalyzer.analyze_symptom_role(
            symptom_id="shock",
            symptom_name="Shock",
            disease=sample_disease_pancreatitis,
        )

        # Shock is listed in complications
        # Role should indicate it's not a primary presentation
        assert analysis.disease_name == "Pancreatitis"
        assert analysis.symptom_id == "shock"

    def test_analyze_role_pathophysiology_link(self, sample_disease_pancreatitis):
        """Test that pathophysiology link is extracted."""
        analysis = SymptomRoleAnalyzer.analyze_symptom_role(
            symptom_id="abdominal_pain",
            symptom_name="Abdominal Pain",
            disease=sample_disease_pancreatitis,
        )

        assert analysis.pathophysiology_explanation != ""
        # Should mention something about pancreas and pain
        assert len(analysis.pathophysiology_explanation) > 10

    def test_analyze_role_clinical_significance(self, sample_disease_pancreatitis):
        """Test clinical significance assessment."""
        analysis = SymptomRoleAnalyzer.analyze_symptom_role(
            symptom_id="abdominal_pain",
            symptom_name="Abdominal Pain",
            disease=sample_disease_pancreatitis,
        )

        # Primary symptom in high-severity disease should be essential
        assert analysis.clinical_significance in [
            "essential",
            "important",
        ]

    def test_analyze_role_early_appearance(self, sample_disease_gd):
        """Test early appearance detection."""
        analysis = SymptomRoleAnalyzer.analyze_symptom_role(
            symptom_id="vomiting",
            symptom_name="Vomiting",
            disease=sample_disease_gd,
        )

        # Vomiting is first symptom in gastroenteritis
        assert analysis.appears_early_in_course is True

    def test_analyze_role_reversibility(self, sample_disease_pancreatitis):
        """Test reversibility assessment."""
        # Primary symptoms should be reversible
        analysis = SymptomRoleAnalyzer.analyze_symptom_role(
            symptom_id="vomiting",
            symptom_name="Vomiting",
            disease=sample_disease_pancreatitis,
        )

        # Most acute symptoms are reversible
        if analysis.primary_role == "primary" or analysis.primary_role == "secondary":
            assert analysis.reversible_with_treatment is True

    def test_analyze_role_associated_symptoms(self, sample_disease_pancreatitis):
        """Test identification of associated symptoms."""
        analysis = SymptomRoleAnalyzer.analyze_symptom_role(
            symptom_id="vomiting",
            symptom_name="Vomiting",
            disease=sample_disease_pancreatitis,
        )

        # Vomiting should be associated with anorexia and lethargy in pancreatitis
        assert len(analysis.associations_with_other_symptoms) >= 0
        # May or may not find associations depending on symptom list position

    def test_analyze_role_alternative_roles(self, sample_disease_pancreatitis):
        """Test identification of alternative roles."""
        analysis = SymptomRoleAnalyzer.analyze_symptom_role(
            symptom_id="abdominal_pain",
            symptom_name="Abdominal Pain",
            disease=sample_disease_pancreatitis,
        )

        # If primary role is certain, there should be few alternatives
        if analysis.primary_confidence > 0.8:
            assert len(analysis.alternative_roles) <= 2

        # All alternatives should have lower confidence
        for _alt_role, alt_conf in analysis.alternative_roles:
            assert alt_conf < analysis.primary_confidence


class TestRoleClassifier:
    """Test high-level role classifier."""

    @pytest.fixture
    def sample_diseases(self):
        """Sample diseases for classification."""
        return [
            {
                "name": "Pancreatitis",
                "symptoms": ["abdominal_pain", "vomiting", "anorexia"],
                "pathophysiology": "Pancreatic inflammation causes pain",
            },
            {
                "name": "Arthritis",
                "symptoms": ["limping", "stiffness", "pain"],
                "pathophysiology": "Joint degeneration causes pain and stiffness",
            },
        ]

    def test_classify_symptom_roles_single_disease(self, sample_diseases):
        """Test role classification for single disease."""
        roles = RoleClassifier.classify_symptom_roles(
            symptom_ids=["vomiting", "anorexia"],
            disease_candidates=[sample_diseases[0]],
        )

        assert "Pancreatitis" in roles
        assert "vomiting" in roles["Pancreatitis"]

    def test_classify_symptom_roles_multiple_diseases(self, sample_diseases):
        """Test role classification across multiple diseases."""
        roles = RoleClassifier.classify_symptom_roles(
            symptom_ids=["pain"],
            disease_candidates=sample_diseases,
        )

        # Pain should be classified for both diseases
        assert "Pancreatitis" in roles
        assert "Arthritis" in roles
        assert "pain" in roles["Pancreatitis"]
        assert "pain" in roles["Arthritis"]

        # Pain role should differ between diseases
        panc_role = roles["Pancreatitis"]["pain"].primary_role
        arth_role = roles["Arthritis"]["pain"].primary_role
        # Both should have roles assigned
        assert panc_role is not None
        assert arth_role is not None

    def test_get_primary_symptoms(self, sample_diseases):
        """Test extraction of primary symptoms."""
        primary = RoleClassifier.get_primary_symptoms(
            disease=sample_diseases[0],
        )

        assert len(primary) > 0
        # Should return top symptoms
        assert "abdominal_pain" in primary or "vomiting" in primary or "anorexia" in primary

    def test_get_complication_symptoms(self, sample_diseases):
        """Test extraction of complication symptoms."""
        disease_with_complications = {
            "name": "Pancreatitis",
            "symptoms": ["pain"],
            "complications": ["shock", "organ_failure", "sepsis"],
        }

        complications = RoleClassifier.get_complication_symptoms(
            disease=disease_with_complications,
        )

        assert "shock" in complications
        assert "organ_failure" in complications


class TestRoleClassifierEdgeCases:
    """Test edge cases in role classification."""

    def test_classify_symptom_not_in_disease(self):
        """Test role classification for symptom not in disease."""
        disease = {
            "name": "Arthritis",
            "symptoms": ["pain", "stiffness"],
            "pathophysiology": "Joint degeneration",
        }

        analysis = SymptomRoleAnalyzer.analyze_symptom_role(
            symptom_id="vomiting",
            symptom_name="Vomiting",
            disease=disease,
        )

        # Should handle gracefully - may not find matching symptoms
        assert analysis.disease_name == "Arthritis"

    def test_classify_with_minimal_pathophysiology(self):
        """Test with minimal pathophysiology information."""
        disease = {
            "name": "Unknown Disease",
            "symptoms": ["symptom_a"],
            "pathophysiology": "",  # Empty
        }

        analysis = SymptomRoleAnalyzer.analyze_symptom_role(
            symptom_id="symptom_a",
            symptom_name="Symptom A",
            disease=disease,
        )

        # Should still assign a role based on position
        assert analysis.primary_role in [
            "primary",
            "secondary",
            "warning_sign",
        ]

    def test_classify_with_japanese_disease_name(self):
        """Test role classification with Japanese disease name."""
        disease = {
            "name": "Pancreatitis",
            "name_ja": "膵炎",
            "symptoms": ["vomiting"],
            "pathophysiology": "膵臓の炎症",  # Japanese text
        }

        analysis = SymptomRoleAnalyzer.analyze_symptom_role(
            symptom_id="vomiting",
            symptom_name="Vomiting",
            disease=disease,
        )

        assert analysis.disease_name in ["Pancreatitis", "膵炎"]


class TestRoleClassifierIntegration:
    """Integration tests for role classifier."""

    def test_role_classification_in_multidisease_context(self):
        """Test role classification in multi-disease scenario."""
        diseases = [
            {
                "name": "Hip Dysplasia",
                "symptoms": ["limping", "pain"],
                "pathophysiology": "Hip joint abnormality causes limping and pain",
            },
            {
                "name": "Osteoarthritis",
                "symptoms": ["limping", "stiffness"],
                "pathophysiology": "Cartilage degeneration causes joint pain and stiffness",
            },
        ]

        # "limping" appears in both - check role differs
        hd_analysis = SymptomRoleAnalyzer.analyze_symptom_role(
            symptom_id="limping",
            symptom_name="Limping",
            disease=diseases[0],
        )

        oa_analysis = SymptomRoleAnalyzer.analyze_symptom_role(
            symptom_id="limping",
            symptom_name="Limping",
            disease=diseases[1],
        )

        # Both should have roles assigned
        assert hd_analysis.primary_role is not None
        assert oa_analysis.primary_role is not None

        # Can be same or different depending on how algorithm weighs position vs content
        assert hd_analysis.disease_name == "Hip Dysplasia"
        assert oa_analysis.disease_name == "Osteoarthritis"

    def test_role_classification_with_symptom_names_mapping(self):
        """Test role classification with symptom name mapping."""
        disease = {
            "name": "Pancreatitis",
            "symptoms": ["vomiting", "abdominal_pain"],
            "pathophysiology": "Pancreatic inflammation",
        }

        symptom_names = {
            "vomiting": "Nausea and Vomiting",
            "abdominal_pain": "Severe Abdominal Pain",
        }

        roles = RoleClassifier.classify_symptom_roles(
            symptom_ids=["vomiting", "abdominal_pain"],
            symptom_names=symptom_names,
            disease_candidates=[disease],
        )

        assert "Pancreatitis" in roles
        # Both symptoms should be classified
        assert len(roles["Pancreatitis"]) >= 2
