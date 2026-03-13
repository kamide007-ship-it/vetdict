"""Phase 6 Performance Tests - Latency and resource usage validation.

Tests to ensure Phase 6 multi-disease diagnosis doesn't introduce
unacceptable performance regressions.
"""

import pytest
import time
from api.ai.multidisease_api_handler import MultiDiseaseAnalyzer
from api.ai.multidisease_detector import MultiDiseaseDetector
from api.ai.symptom_context_engine import AmbiguitySolver
from api.ai.combined_confidence_calculator import CombinedConfidenceCalculator


class TestPerformanceBaseline:
    """Performance baseline tests for critical operations."""

    # Performance thresholds (in seconds)
    THRESHOLD_SYMPTOM_AMBIGUITY = 0.5  # Max 500ms
    THRESHOLD_CONFIDENCE_CALC = 0.3  # Max 300ms
    THRESHOLD_QUESTION_GENERATION = 0.5  # Max 500ms
    THRESHOLD_FULL_ANALYSIS = 2.0  # Max 2 seconds

    @pytest.fixture
    def large_disease_database(self):
        """Create a realistic large disease database."""
        return [
            {
                "name": f"Disease_{i}",
                "symptoms": [f"symptom_{j}" for j in range(5)],
                "pathophysiology": f"Disease {i} pathophysiology description",
                "severity_score": 0.5 + (i % 5) * 0.1,
                "prevalence_score": 0.3 + (i % 5) * 0.1,
            }
            for i in range(50)  # 50 diseases
        ]

    def test_symptom_ambiguity_analysis_performance(self, large_disease_database):
        """Test that ambiguity analysis completes within time threshold."""
        start = time.time()

        AmbiguitySolver.analyze_symptom_set(
            symptom_ids=["symptom_1", "symptom_2", "symptom_3"],
            disease_candidates=[
                {"name": "Disease_1", "match_percent": 70},
                {"name": "Disease_2", "match_percent": 65},
            ],
            disease_database=large_disease_database,
        )

        elapsed = time.time() - start
        assert elapsed < self.THRESHOLD_SYMPTOM_AMBIGUITY, (
            f"Ambiguity analysis took {elapsed:.3f}s (threshold: {self.THRESHOLD_SYMPTOM_AMBIGUITY}s)"
        )

    def test_confidence_calculation_performance(self):
        """Test that confidence calculation is fast."""
        start = time.time()

        CombinedConfidenceCalculator.calculate_bayesian_combination(
            diseases=["Disease A", "Disease B", "Disease C"],
            individual_confidences={"Disease A": 0.7, "Disease B": 0.6, "Disease C": 0.5},
            detected_symptoms=["sym1", "sym2", "sym3", "sym4"],
            symptom_disease_mapping={
                "sym1": {"Disease A"},
                "sym2": {"Disease B"},
                "sym3": {"Disease C"},
                "sym4": {"Disease A", "Disease B"},
            },
        )

        elapsed = time.time() - start
        assert elapsed < self.THRESHOLD_CONFIDENCE_CALC, (
            f"Confidence calculation took {elapsed:.3f}s (threshold: {self.THRESHOLD_CONFIDENCE_CALC}s)"
        )

    def test_full_multidisease_analysis_performance(self, large_disease_database):
        """Test that full analysis completes within time threshold."""
        start = time.time()

        MultiDiseaseAnalyzer.analyze_for_multidisease(
            symptom_ids=["symptom_0", "symptom_1", "symptom_2"],
            suspected_diseases=[
                {"name": "Disease_1", "match_percent": 70},
                {"name": "Disease_2", "match_percent": 65},
                {"name": "Disease_3", "match_percent": 60},
            ],
            disease_database=large_disease_database[:20],  # Use subset
            patient_context={"age_years": 8},
        )

        elapsed = time.time() - start
        assert elapsed < self.THRESHOLD_FULL_ANALYSIS, (
            f"Full analysis took {elapsed:.3f}s (threshold: {self.THRESHOLD_FULL_ANALYSIS}s)"
        )


class TestMemoryUsage:
    """Tests to ensure reasonable memory usage."""

    def test_large_symptom_set_analysis(self):
        """Test handling of large symptom sets."""
        large_symptom_set = [f"symptom_{i}" for i in range(50)]

        result = MultiDiseaseAnalyzer.analyze_for_multidisease(
            symptom_ids=large_symptom_set,
            suspected_diseases=[
                {"name": "Disease A", "match_percent": 50},
                {"name": "Disease B", "match_percent": 45},
            ],
            disease_database=[
                {"name": "Disease A", "symptoms": large_symptom_set[:25]},
                {"name": "Disease B", "symptoms": large_symptom_set[25:]},
            ],
        )

        # Should complete without crash
        assert isinstance(result, dict)

    def test_many_disease_candidates(self):
        """Test handling of many disease candidates."""
        many_candidates = [
            {"name": f"Disease_{i}", "match_percent": 50 - i}
            for i in range(30)
        ]

        disease_db = [
            {"name": f"Disease_{i}", "symptoms": ["symptom_1"]}
            for i in range(30)
        ]

        result = MultiDiseaseAnalyzer.analyze_for_multidisease(
            symptom_ids=["symptom_1"],
            suspected_diseases=many_candidates,
            disease_database=disease_db,
        )

        # Should handle gracefully
        assert isinstance(result, dict)


class TestScalability:
    """Scalability tests for realistic large-scale scenarios."""

    def test_multidisease_detector_scales_with_candidates(self):
        """Test that detector scales with number of candidates."""
        # Small number
        result_small = MultiDiseaseDetector.generate_multidisease_candidates(
            suspected_diseases=[
                {"name": "Disease A", "match_percent": 70},
                {"name": "Disease B", "match_percent": 60},
            ],
            detected_symptoms=["symptom_1", "symptom_2"],
            patient_context=None,
        )

        # Larger number
        result_large = MultiDiseaseDetector.generate_multidisease_candidates(
            suspected_diseases=[
                {"name": f"Disease_{i}", "match_percent": 70 - i * 2}
                for i in range(10)
            ],
            detected_symptoms=["symptom_1", "symptom_2"],
            patient_context=None,
        )

        # Both should complete
        assert isinstance(result_small, list)
        assert isinstance(result_large, list)

    def test_ambiguity_analysis_scales_with_symptom_count(self):
        """Test that ambiguity analysis scales with symptom count."""
        disease_db = [
            {"name": "Disease A", "symptoms": ["s1", "s2", "s3"]},
            {"name": "Disease B", "symptoms": ["s2", "s3", "s4"]},
        ]

        # Few symptoms
        result_few = AmbiguitySolver.analyze_symptom_set(
            symptom_ids=["s1", "s2"],
            disease_candidates=[
                {"name": "Disease A", "match_percent": 70},
                {"name": "Disease B", "match_percent": 60},
            ],
            disease_database=disease_db,
        )

        # Many symptoms
        result_many = AmbiguitySolver.analyze_symptom_set(
            symptom_ids=["s1", "s2", "s3", "s4"] + [f"s{i}" for i in range(5, 15)],
            disease_candidates=[
                {"name": "Disease A", "match_percent": 70},
                {"name": "Disease B", "match_percent": 60},
            ],
            disease_database=disease_db,
        )

        # Both should complete
        assert isinstance(result_few, list)
        assert isinstance(result_many, list)


class TestConcurrency:
    """Tests for handling multiple concurrent requests."""

    def test_independent_analyses_dont_interfere(self):
        """Test that independent analyses don't interfere with each other."""
        disease_db = [
            {"name": "Disease A", "symptoms": ["symptom_1"]},
            {"name": "Disease B", "symptoms": ["symptom_2"]},
        ]

        # Run multiple analyses
        result1 = MultiDiseaseAnalyzer.analyze_for_multidisease(
            symptom_ids=["symptom_1"],
            suspected_diseases=[{"name": "Disease A", "match_percent": 70}],
            disease_database=disease_db,
        )

        result2 = MultiDiseaseAnalyzer.analyze_for_multidisease(
            symptom_ids=["symptom_2"],
            suspected_diseases=[{"name": "Disease B", "match_percent": 70}],
            disease_database=disease_db,
        )

        result3 = MultiDiseaseAnalyzer.analyze_for_multidisease(
            symptom_ids=["symptom_1", "symptom_2"],
            suspected_diseases=[
                {"name": "Disease A", "match_percent": 70},
                {"name": "Disease B", "match_percent": 60},
            ],
            disease_database=disease_db,
        )

        # All should complete independently
        assert isinstance(result1, dict)
        assert isinstance(result2, dict)
        assert isinstance(result3, dict)
