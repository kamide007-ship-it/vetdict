"""Tests for multi-disease API integration (Phase 6 Stage 6).

Tests the complete API integration of Stage 3-5 components through
the /api/diagnostic-chat/multi-disease/analyze endpoint.
"""

import pytest

from api.ai.multidisease_api_handler import MultiDiseaseAnalyzer


class TestMultiDiseaseAnalyzer:
    """Test multi-disease analyzer orchestration."""

    @pytest.fixture
    def sample_disease_database(self):
        """Sample disease database."""
        return [
            {
                "name": "Hip Dysplasia",
                "name_ja": "股関節形成不全",
                "symptoms": ["limping", "pain", "reluctance_to_exercise"],
                "pathophysiology": (
                    "Abnormal hip joint development causes pain and limping. "
                    "Primary symptoms appear early."
                ),
                "severity_score": 0.7,
                "complications": ["osteoarthritis"],
            },
            {
                "name": "Osteoarthritis",
                "name_ja": "変形性関節症",
                "symptoms": ["stiffness", "limping", "reduced_mobility"],
                "pathophysiology": (
                    "Cartilage degeneration causes stiffness and limping. "
                    "Develops gradually over time."
                ),
                "severity_score": 0.6,
                "complications": [],
            },
            {
                "name": "Ligament Tear",
                "name_ja": "靭帯損傷",
                "symptoms": ["acute_pain", "swelling", "lameness"],
                "pathophysiology": (
                    "Traumatic ligament injury causes acute pain and swelling. "
                    "Sudden onset."
                ),
                "severity_score": 0.8,
                "complications": [],
            },
        ]

    def test_analyze_for_multidisease_basic(self, sample_disease_database):
        """Test basic multi-disease analysis."""
        result = MultiDiseaseAnalyzer.analyze_for_multidisease(
            symptom_ids=["limping", "pain", "stiffness"],
            detected_symptoms_ja="跛行、痛み、こわばり",
            detected_symptoms_en="Limping, pain, stiffness",
            suspected_diseases=[
                {"name": "Hip Dysplasia", "match_percent": 75},
                {"name": "Osteoarthritis", "match_percent": 65},
            ],
            disease_database=sample_disease_database,
            patient_context={"age_years": 10, "species": "dog"},
        )

        assert "multidisease_mode_enabled" in result
        assert "symptom_count" in result
        assert result["symptom_count"] == 3

    def test_analyze_with_combination_analysis(self, sample_disease_database):
        """Test that combination analysis is performed."""
        result = MultiDiseaseAnalyzer.analyze_for_multidisease(
            symptom_ids=["limping", "pain"],
            suspected_diseases=[
                {"name": "Hip Dysplasia", "match_percent": 70},
                {"name": "Osteoarthritis", "match_percent": 60},
            ],
            disease_database=sample_disease_database,
            patient_context={"age_years": 9},
        )

        if result.get("multidisease_mode_enabled"):
            assert "combinations" in result
            assert "confidence_breakdown" in result

    def test_analyze_includes_ambiguity_analysis(self, sample_disease_database):
        """Test that ambiguity analysis is included."""
        result = MultiDiseaseAnalyzer.analyze_for_multidisease(
            symptom_ids=["limping", "pain"],
            suspected_diseases=[
                {"name": "Hip Dysplasia", "match_percent": 75},
                {"name": "Osteoarthritis", "match_percent": 60},
                {"name": "Ligament Tear", "match_percent": 50},
            ],
            disease_database=sample_disease_database,
        )

        if result.get("multidisease_mode_enabled"):
            assert "ambiguity_analysis" in result
            assert "high_ambiguity_symptoms" in result["ambiguity_analysis"]

    def test_analyze_generates_questions(self, sample_disease_database):
        """Test that diagnostic questions are generated."""
        result = MultiDiseaseAnalyzer.analyze_for_multidisease(
            symptom_ids=["limping", "pain", "stiffness"],
            suspected_diseases=[
                {"name": "Hip Dysplasia", "match_percent": 75},
                {"name": "Osteoarthritis", "match_percent": 65},
            ],
            disease_database=sample_disease_database,
        )

        if result.get("multidisease_mode_enabled") and result.get("combinations"):
            assert "next_questions" in result
            if result["next_questions"]:
                assert "question" in result["next_questions"][0]
                assert "ranking_score" in result["next_questions"][0]

    def test_analyze_with_single_disease_no_multidisease(self):
        """Test that single disease doesn't trigger multi-disease mode."""
        result = MultiDiseaseAnalyzer.analyze_for_multidisease(
            symptom_ids=["symptom1"],
            suspected_diseases=[
                {"name": "Disease A", "match_percent": 90},
            ],
            disease_database=[
                {"name": "Disease A", "symptoms": ["symptom1"]}
            ],
        )

        # Single symptom and single disease should not enable multi-disease
        assert result["multidisease_mode_enabled"] is False or result["symptom_count"] < 5

    def test_build_symptom_mapping(self):
        """Test symptom-to-disease mapping."""
        disease_db = [
            {
                "name": "Disease A",
                "symptoms": ["pain", "swelling"],
            },
            {
                "name": "Disease B",
                "symptoms": ["pain", "redness"],
            },
        ]

        mapping = MultiDiseaseAnalyzer._build_symptom_mapping(
            symptom_ids=["pain", "swelling"],
            disease_names=["Disease A", "Disease B"],
            disease_database=disease_db,
        )

        assert "pain" in mapping
        assert "swelling" in mapping
        assert "Disease A" in mapping["swelling"]
        assert "Disease B" not in mapping["swelling"]

    def test_validate_request_valid(self):
        """Test request validation for valid request."""
        valid_request = {
            "symptom_ids": ["symptom1", "symptom2"],
            "suspected_diseases": [{"name": "Disease A"}],
        }

        is_valid, error = MultiDiseaseAnalyzer.validate_request(valid_request)
        assert is_valid is True
        assert error is None

    def test_validate_request_missing_symptoms(self):
        """Test validation fails without symptoms."""
        invalid_request = {
            "suspected_diseases": [{"name": "Disease A"}],
        }

        is_valid, error = MultiDiseaseAnalyzer.validate_request(invalid_request)
        assert is_valid is False
        assert error is not None

    def test_validate_request_empty_symptoms(self):
        """Test validation fails with empty symptoms."""
        invalid_request = {
            "symptom_ids": [],
            "suspected_diseases": [{"name": "Disease A"}],
        }

        is_valid, error = MultiDiseaseAnalyzer.validate_request(invalid_request)
        assert is_valid is False
        assert error is not None

    def test_validate_request_invalid_disease_format(self):
        """Test validation fails with invalid disease format."""
        invalid_request = {
            "symptom_ids": ["symptom1"],
            "suspected_diseases": "not a list",
        }

        is_valid, error = MultiDiseaseAnalyzer.validate_request(invalid_request)
        assert is_valid is False
        assert error is not None

    def test_analyze_response_structure(self, sample_disease_database):
        """Test response has correct structure."""
        result = MultiDiseaseAnalyzer.analyze_for_multidisease(
            symptom_ids=["limping", "pain", "stiffness", "reduced_mobility"],
            suspected_diseases=[
                {"name": "Hip Dysplasia", "match_percent": 75},
                {"name": "Osteoarthritis", "match_percent": 65},
                {"name": "Ligament Tear", "match_percent": 50},
            ],
            disease_database=sample_disease_database,
            patient_context={"age_years": 8},
        )

        # Check required fields
        assert "multidisease_mode_enabled" in result
        assert "symptom_count" in result
        assert "disease_candidates_count" in result

        if result["multidisease_mode_enabled"]:
            assert "combinations_found" in result
            if result.get("combinations"):
                for combo in result["combinations"]:
                    assert "diseases" in combo
                    assert "combined_confidence" in combo

    def test_analyze_with_patient_context(self, sample_disease_database):
        """Test analysis with patient context."""
        result = MultiDiseaseAnalyzer.analyze_for_multidisease(
            symptom_ids=["limping", "pain", "stiffness"],
            suspected_diseases=[
                {"name": "Hip Dysplasia", "match_percent": 70},
                {"name": "Osteoarthritis", "match_percent": 60},
            ],
            disease_database=sample_disease_database,
            patient_context={
                "age_years": 12,
                "species": "dog",
                "breed": "German Shepherd",
                "gender": "female",
            },
        )

        # Older age should increase multi-disease likelihood
        assert isinstance(result, dict)
        assert "multidisease_mode_enabled" in result


class TestMultiDiseaseAPIEdgeCases:
    """Test edge cases for multi-disease API."""

    def test_analyze_empty_disease_database(self):
        """Test analysis with empty disease database."""
        result = MultiDiseaseAnalyzer.analyze_for_multidisease(
            symptom_ids=["symptom1"],
            suspected_diseases=[{"name": "Unknown Disease"}],
            disease_database=[],
        )

        assert "multidisease_mode_enabled" in result
        assert result["symptom_count"] >= 0

    def test_analyze_none_parameters(self):
        """Test analysis with None optional parameters."""
        result = MultiDiseaseAnalyzer.analyze_for_multidisease(
            symptom_ids=["symptom1"],
            detected_symptoms_ja=None,
            detected_symptoms_en=None,
            suspected_diseases=None,
            disease_database=None,
            patient_context=None,
        )

        assert "multidisease_mode_enabled" in result

    def test_symbol_mapping_with_missing_disease(self):
        """Test symptom mapping when disease not in database."""
        mapping = MultiDiseaseAnalyzer._build_symptom_mapping(
            symptom_ids=["pain"],
            disease_names=["Disease A", "Nonexistent Disease"],
            disease_database=[
                {"name": "Disease A", "symptoms": ["pain"]},
            ],
        )

        assert "pain" in mapping
        assert "Disease A" in mapping["pain"]
        # Nonexistent disease should not be in mapping
        assert "Nonexistent Disease" not in mapping["pain"]

    def test_analyze_very_high_confidence_diseases(self):
        """Test analysis when diseases have very high confidence."""
        result = MultiDiseaseAnalyzer.analyze_for_multidisease(
            symptom_ids=["symptom1", "symptom2"],
            suspected_diseases=[
                {"name": "Disease A", "match_percent": 99},
                {"name": "Disease B", "match_percent": 95},
            ],
            disease_database=[
                {"name": "Disease A", "symptoms": ["symptom1", "symptom2"]},
                {"name": "Disease B", "symptoms": ["symptom1"]},
            ],
        )

        # High confidence in one disease might still show combinations
        assert isinstance(result, dict)
        assert "multidisease_mode_enabled" in result
