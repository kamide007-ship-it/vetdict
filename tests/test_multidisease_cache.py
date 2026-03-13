"""Tests for multi-disease caching and optimization (Phase 6 Stage 8).

Tests cache functionality and performance optimization mechanisms.
"""

import pytest
from api.ai.multidisease_cache_manager import (
    PrecomputedDiseaseMeta,
    SymptomContextCache,
    AmbiguityScoreCache,
    ConfidenceCalculationCache,
    QuestionTemplateCache,
    MultiDiseaseAnalysisCache,
    get_global_cache,
    initialize_caches,
)


class TestPrecomputedDiseaseMeta:
    """Test disease metadata precomputation."""

    @pytest.fixture
    def sample_diseases(self):
        """Sample diseases for caching tests."""
        return [
            {
                "name": "Hip Dysplasia",
                "symptoms": ["limping", "pain", "rear_limb_weakness"],
            },
            {
                "name": "Osteoarthritis",
                "symptoms": ["stiffness", "limping", "pain"],
            },
            {
                "name": "Gastroenteritis",
                "symptoms": ["vomiting", "diarrhea", "lethargy"],
            },
        ]

    def test_build_symptom_index(self, sample_diseases):
        """Test building symptom-to-disease index."""
        meta = PrecomputedDiseaseMeta()
        meta.build_from_database(sample_diseases)

        # Check symptom index is built
        assert "limping" in meta._symptom_index
        assert "pain" in meta._symptom_index
        assert "vomiting" in meta._symptom_index

    def test_get_diseases_with_symptom(self, sample_diseases):
        """Test retrieving diseases with a symptom."""
        meta = PrecomputedDiseaseMeta()
        meta.build_from_database(sample_diseases)

        # Limping is in Hip Dysplasia and Osteoarthritis
        limping_diseases = meta.get_diseases_with_symptom("limping")
        assert "Hip Dysplasia" in limping_diseases
        assert "Osteoarthritis" in limping_diseases
        assert len(limping_diseases) == 2

    def test_get_disease_record(self, sample_diseases):
        """Test retrieving cached disease record."""
        meta = PrecomputedDiseaseMeta()
        meta.build_from_database(sample_diseases)

        disease = meta.get_disease("Hip Dysplasia")
        assert disease is not None
        assert disease["name"] == "Hip Dysplasia"

    def test_cache_validity(self, sample_diseases):
        """Test cache validity checking."""
        meta = PrecomputedDiseaseMeta()
        meta.build_from_database(sample_diseases)

        # Should be valid right after building
        assert meta.is_valid() is True

        # Invalidate manually
        meta.invalidate()
        assert meta.is_valid() is False


class TestSymptomContextCache:
    """Test symptom context caching."""

    def test_cache_hit_miss(self):
        """Test cache hit and miss tracking."""
        cache = SymptomContextCache(max_size=10)

        # Cache miss
        result = cache.get("symptom1", ["disease_a", "disease_b"])
        assert result is None
        assert cache._misses == 1

        # Cache hit
        test_contexts = {"disease_a": "context_a", "disease_b": "context_b"}
        cache.put("symptom1", ["disease_a", "disease_b"], test_contexts)
        result = cache.get("symptom1", ["disease_a", "disease_b"])
        assert result is not None
        assert cache._hits == 1

    def test_cache_size_limit(self):
        """Test that cache respects size limit."""
        cache = SymptomContextCache(max_size=5)

        # Fill cache
        for i in range(5):
            cache.put(f"symptom_{i}", ["disease_a"], {"test": f"data_{i}"})

        assert len(cache._cache) == 5

        # Add one more (should evict oldest)
        cache.put("symptom_5", ["disease_a"], {"test": "data_5"})
        assert len(cache._cache) == 5

    def test_get_cache_stats(self):
        """Test cache statistics."""
        cache = SymptomContextCache()

        cache.get("symptom1", ["disease_a"])  # Miss
        cache.put("symptom1", ["disease_a"], {"test": "data"})
        cache.get("symptom1", ["disease_a"])  # Hit
        cache.get("symptom2", ["disease_a"])  # Miss

        stats = cache.get_stats()
        assert stats["hits"] == 1
        assert stats["misses"] == 2
        assert stats["cached_items"] == 1


class TestAmbiguityScoreCache:
    """Test ambiguity score caching."""

    def test_cache_ambiguity_reports(self):
        """Test caching ambiguity reports."""
        cache = AmbiguityScoreCache()

        symptom_ids = ["symptom1", "symptom2"]
        reports = [{"symptom_id": "symptom1", "ambiguity_score": 0.5}]

        # Initially not cached
        assert cache.get(symptom_ids) is None

        # Cache it
        cache.put(symptom_ids, reports)
        result = cache.get(symptom_ids)
        assert result == reports

    def test_symptom_order_independent(self):
        """Test that symptom order doesn't affect cache lookup."""
        cache = AmbiguityScoreCache()

        reports = [{"test": "data"}]
        cache.put(["symptom1", "symptom2"], reports)

        # Should find with different order
        result = cache.get(["symptom2", "symptom1"])
        assert result == reports


class TestConfidenceCalculationCache:
    """Test confidence calculation caching."""

    def test_cache_confidence_breakdown(self):
        """Test caching confidence breakdowns."""
        cache = ConfidenceCalculationCache()

        diseases = ["disease_a", "disease_b"]
        symptom_ids = ["symptom1", "symptom2"]
        breakdown = {"final_confidence": 0.65, "bayesian_posterior": 0.6}

        # Cache it
        cache.put(diseases, symptom_ids, breakdown)

        # Retrieve it
        result = cache.get(diseases, symptom_ids)
        assert result == breakdown

    def test_disease_order_independent(self):
        """Test that disease order doesn't affect cache."""
        cache = ConfidenceCalculationCache()

        breakdown = {"test": "data"}
        cache.put(["disease_a", "disease_b"], ["symptom1"], breakdown)

        # Should find with different disease order
        result = cache.get(["disease_b", "disease_a"], ["symptom1"])
        assert result == breakdown


class TestQuestionTemplateCache:
    """Test question template caching."""

    def test_cache_questions_for_disease_pair(self):
        """Test caching questions for disease pairs."""
        cache = QuestionTemplateCache()

        questions = [
            {"question_id": "q1", "text": "Question 1"},
            {"question_id": "q2", "text": "Question 2"},
        ]

        cache.cache_questions("disease_a", "disease_b", questions)
        result = cache.get_differentiating_questions("disease_a", "disease_b")
        assert result == questions

    def test_disease_order_independent(self):
        """Test that disease order is normalized."""
        cache = QuestionTemplateCache()

        questions = [{"question_id": "q1"}]
        cache.cache_questions("disease_a", "disease_b", questions)

        # Should find with reversed order
        result = cache.get_differentiating_questions("disease_b", "disease_a")
        assert result == questions


class TestMultiDiseaseAnalysisCache:
    """Test master cache manager."""

    @pytest.fixture
    def sample_diseases(self):
        """Sample diseases."""
        return [
            {"name": "Disease A", "symptoms": ["symptom1"]},
            {"name": "Disease B", "symptoms": ["symptom2"]},
        ]

    def test_initialize_from_database(self, sample_diseases):
        """Test initializing all caches from database."""
        cache_mgr = MultiDiseaseAnalysisCache()
        cache_mgr.initialize_from_database(sample_diseases)

        # Disease metadata should be initialized
        assert cache_mgr.disease_meta.is_valid() is True
        assert "Disease A" in cache_mgr.disease_meta.get_all_diseases()

    def test_clear_all_caches(self, sample_diseases):
        """Test clearing all caches at once."""
        cache_mgr = MultiDiseaseAnalysisCache()
        cache_mgr.initialize_from_database(sample_diseases)

        # Add some cached data
        cache_mgr.symptom_context.put("sym1", ["disease_a"], {"test": "data"})
        cache_mgr.question_templates.cache_questions("a", "b", [{"q": "1"}])

        # Clear all
        cache_mgr.clear_all()

        # Verify caches are cleared
        assert cache_mgr.symptom_context.get("sym1", ["disease_a"]) is None
        assert cache_mgr.question_templates.get_differentiating_questions("a", "b") is None

    def test_get_cache_stats(self, sample_diseases):
        """Test getting statistics from all caches."""
        cache_mgr = MultiDiseaseAnalysisCache()
        cache_mgr.initialize_from_database(sample_diseases)

        stats = cache_mgr.get_cache_stats()

        assert "symptom_context" in stats
        assert "ambiguity_scores" in stats
        assert "confidence_calculations" in stats
        assert "question_templates" in stats
        assert "disease_metadata" in stats


class TestGlobalCacheInstance:
    """Test global cache singleton."""

    def test_global_cache_singleton(self):
        """Test that global cache is a singleton."""
        cache1 = get_global_cache()
        cache2 = get_global_cache()

        assert cache1 is cache2

    def test_initialize_global_caches(self):
        """Test initializing global caches."""
        diseases = [
            {"name": "Disease X", "symptoms": ["symptom_x"]},
        ]

        initialize_caches(diseases)
        cache = get_global_cache()

        assert cache.disease_meta.is_valid() is True
