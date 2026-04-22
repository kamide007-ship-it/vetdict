"""Tests for Stage 8 Part 2: API Cache Integration.

Tests that caching is properly integrated into the multi-disease API handler.
"""

from unittest.mock import patch

import pytest

from api.ai.multidisease_api_handler import MultiDiseaseAnalyzer


class TestAPIHandlerCacheIntegration:
    """Test cache integration in API handler."""

    @pytest.fixture
    def sample_data(self):
        """Sample data for testing."""
        return {
            "symptom_ids": ["symptom1", "symptom2"],
            "disease_database": [
                {
                    "name": "Disease A",
                    "symptoms": ["symptom1", "symptom2"],
                    "prevalence": 0.1,
                },
                {
                    "name": "Disease B",
                    "symptoms": ["symptom2", "symptom3"],
                    "prevalence": 0.05,
                },
            ],
            "suspected_diseases": [
                {"name": "Disease A", "confidence": 0.7},
                {"name": "Disease B", "confidence": 0.4},
            ],
        }

    @pytest.fixture
    def mock_detector(self):
        """Mock MultiDiseaseDetector."""
        with patch("api.ai.multidisease_api_handler.MultiDiseaseDetector") as mock:
            yield mock

    @pytest.fixture
    def mock_confidence_calculator(self):
        """Mock CombinedConfidenceCalculator."""
        with patch("api.ai.multidisease_api_handler.CombinedConfidenceCalculator") as mock:
            yield mock

    @pytest.fixture
    def mock_question_generator(self):
        """Mock MultiDiseaseQuestionGenerator."""
        with patch("api.ai.multidisease_api_handler.MultiDiseaseQuestionGenerator") as mock:
            yield mock

    @pytest.fixture
    def mock_question_ranker(self):
        """Mock DiscriminativeQuestionRanker."""
        with patch("api.ai.multidisease_api_handler.DiscriminativeQuestionRanker") as mock:
            yield mock

    def test_analyze_without_cache_enabled(
        self,
        sample_data,
        mock_detector,
        mock_confidence_calculator,
        mock_question_generator,
        mock_question_ranker,
    ):
        """Test that analysis works with caching disabled."""
        # Setup mocks to return minimal values
        mock_detector.should_explore_multidisease.return_value = False

        response = MultiDiseaseAnalyzer.analyze_for_multidisease(
            symptom_ids=sample_data["symptom_ids"],
            disease_database=sample_data["disease_database"],
            use_cache=False,
        )

        assert response["cache_enabled"] is False
        assert "multidisease_mode_enabled" in response

    def test_analyze_with_cache_enabled(
        self,
        sample_data,
        mock_detector,
        mock_confidence_calculator,
        mock_question_generator,
        mock_question_ranker,
    ):
        """Test that analysis includes cache_enabled flag."""
        mock_detector.should_explore_multidisease.return_value = False

        response = MultiDiseaseAnalyzer.analyze_for_multidisease(
            symptom_ids=sample_data["symptom_ids"],
            disease_database=sample_data["disease_database"],
            use_cache=True,
        )

        assert response["cache_enabled"] is True

    def test_response_includes_cache_indicator(self, sample_data):
        """Test that response indicates if caching was used."""
        with patch("api.ai.multidisease_api_handler.MultiDiseaseDetector") as mock_detector:
            mock_detector.should_explore_multidisease.return_value = False

            response = MultiDiseaseAnalyzer.analyze_for_multidisease(
                symptom_ids=sample_data["symptom_ids"],
                use_cache=True,
            )

            assert "cache_enabled" in response


class TestSymptomMappingBuilding:
    """Test symptom-to-disease mapping utility."""

    def test_build_symptom_mapping(self):
        """Test building symptom mapping."""
        symptom_ids = ["symptom1", "symptom2"]
        disease_names = ["Disease A", "Disease B"]
        disease_database = [
            {
                "name": "Disease A",
                "symptoms": ["symptom1"],
            },
            {
                "name": "Disease B",
                "symptoms": ["symptom2", "symptom3"],
            },
        ]

        mapping = MultiDiseaseAnalyzer._build_symptom_mapping(symptom_ids, disease_names, disease_database)

        assert "symptom1" in mapping
        assert "symptom2" in mapping
        assert "Disease A" in mapping["symptom1"]
        assert "Disease B" in mapping["symptom2"]

    def test_symptom_mapping_empty_database(self):
        """Test symptom mapping with empty database."""
        symptom_ids = ["symptom1"]
        disease_names = ["Disease A"]
        disease_database = []

        mapping = MultiDiseaseAnalyzer._build_symptom_mapping(symptom_ids, disease_names, disease_database)

        assert "symptom1" in mapping
        assert len(mapping["symptom1"]) == 0


class TestRequestValidation:
    """Test request validation."""

    def test_validate_request_success(self):
        """Test successful validation."""
        request = {
            "symptom_ids": ["symptom1", "symptom2"],
        }

        is_valid, error = MultiDiseaseAnalyzer.validate_request(request)

        assert is_valid is True
        assert error is None

    def test_validate_missing_symptom_ids(self):
        """Test validation fails without symptom_ids."""
        request = {}

        is_valid, error = MultiDiseaseAnalyzer.validate_request(request)

        assert is_valid is False
        assert error is not None

    def test_validate_empty_symptom_ids(self):
        """Test validation fails with empty symptom_ids."""
        request = {"symptom_ids": []}

        is_valid, error = MultiDiseaseAnalyzer.validate_request(request)

        assert is_valid is False
        assert error is not None

    def test_validate_invalid_symptom_ids_type(self):
        """Test validation fails with non-list symptom_ids."""
        request = {"symptom_ids": "symptom1"}

        is_valid, error = MultiDiseaseAnalyzer.validate_request(request)

        assert is_valid is False
        assert error is not None

    def test_validate_invalid_disease_type(self):
        """Test validation fails with non-list suspected_diseases."""
        request = {
            "symptom_ids": ["symptom1"],
            "suspected_diseases": "disease1",
        }

        is_valid, error = MultiDiseaseAnalyzer.validate_request(request)

        assert is_valid is False
        assert error is not None
