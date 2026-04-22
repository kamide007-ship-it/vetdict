"""Multi-disease analysis caching and preprocessing manager.

Optimizes Phase 6 performance through intelligent caching of expensive
computations and preprocessing of disease database.
"""

import hashlib
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class PrecomputedDiseaseMeta:
    """Precomputed metadata for disease database optimization."""

    def __init__(self):
        """Initialize with empty cache."""
        self._symptom_index: Dict[str, set] = {}  # symptom_id -> {disease_names}
        self._disease_cache: Dict[str, Dict[str, Any]] = {}
        self._cache_timestamp: Optional[datetime] = None
        self._cache_ttl_seconds: int = 3600  # 1 hour default

    def build_from_database(self, disease_database: List[Dict[str, Any]]) -> None:
        """
        Build symptom index from disease database.

        Args:
            disease_database: Complete disease database
        """
        self._symptom_index.clear()
        self._disease_cache.clear()

        for disease in disease_database:
            disease_name = disease.get("name", "")
            symptoms = disease.get("symptoms", [])

            # Index symptoms
            for symptom in symptoms:
                symptom_id = str(symptom).lower()
                if symptom_id not in self._symptom_index:
                    self._symptom_index[symptom_id] = set()
                self._symptom_index[symptom_id].add(disease_name)

            # Cache disease
            self._disease_cache[disease_name] = disease

        self._cache_timestamp = datetime.utcnow()
        logger.info(
            f"Built disease metadata: {len(self._disease_cache)} diseases, {len(self._symptom_index)} unique symptoms"
        )

    def get_diseases_with_symptom(self, symptom_id: str) -> set:
        """Get diseases that have a symptom."""
        return self._symptom_index.get(symptom_id.lower(), set())

    def get_disease(self, disease_name: str) -> Optional[Dict[str, Any]]:
        """Get cached disease record."""
        return self._disease_cache.get(disease_name)

    def get_all_diseases(self) -> Dict[str, Dict[str, Any]]:
        """Get all cached diseases."""
        return self._disease_cache.copy()

    def is_valid(self) -> bool:
        """Check if cache is still valid."""
        if not self._cache_timestamp:
            return False
        age = datetime.utcnow() - self._cache_timestamp
        return age.total_seconds() < self._cache_ttl_seconds

    def invalidate(self) -> None:
        """Manually invalidate cache."""
        self._cache_timestamp = None


class SymptomContextCache:
    """Cache for symptom context computations (Stage 3)."""

    def __init__(self, max_size: int = 1000):
        """Initialize context cache."""
        self._cache: Dict[str, Any] = {}
        self._max_size = max_size
        self._hits = 0
        self._misses = 0

    def _make_key(
        self,
        symptom_id: str,
        disease_names: Tuple[str, ...],
    ) -> str:
        """Generate cache key."""
        key_data = f"{symptom_id}:{','.join(sorted(disease_names))}"
        return hashlib.md5(key_data.encode()).hexdigest()

    def get(
        self,
        symptom_id: str,
        disease_names: List[str],
    ) -> Optional[Dict[str, Any]]:
        """Get cached symptom context."""
        key = self._make_key(symptom_id, tuple(disease_names))
        result = self._cache.get(key)
        if result:
            self._hits += 1
        else:
            self._misses += 1
        return result

    def put(
        self,
        symptom_id: str,
        disease_names: List[str],
        contexts: Dict[str, Any],
    ) -> None:
        """Cache symptom context."""
        if len(self._cache) >= self._max_size:
            # Simple LRU: remove first item
            self._cache.pop(next(iter(self._cache)))

        key = self._make_key(symptom_id, tuple(disease_names))
        self._cache[key] = {
            "contexts": contexts,
            "timestamp": datetime.utcnow().isoformat(),
        }

    def clear(self) -> None:
        """Clear cache."""
        self._cache.clear()
        self._hits = 0
        self._misses = 0

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        total = self._hits + self._misses
        hit_rate = (self._hits / total * 100) if total > 0 else 0.0
        return {
            "hits": self._hits,
            "misses": self._misses,
            "hit_rate_percent": round(hit_rate, 1),
            "cached_items": len(self._cache),
            "max_size": self._max_size,
        }


class AmbiguityScoreCache:
    """Cache for ambiguity analysis scores (Stage 3)."""

    def __init__(self, max_size: int = 500):
        """Initialize ambiguity cache."""
        self._cache: Dict[str, Any] = {}
        self._max_size = max_size

    def _make_key(self, symptom_ids: Tuple[str, ...]) -> str:
        """Generate cache key."""
        key_data = ",".join(sorted(symptom_ids))
        return hashlib.md5(key_data.encode()).hexdigest()

    def get(self, symptom_ids: List[str]) -> Optional[List[Any]]:
        """Get cached ambiguity report."""
        key = self._make_key(tuple(symptom_ids))
        return self._cache.get(key)

    def put(
        self,
        symptom_ids: List[str],
        reports: List[Any],
    ) -> None:
        """Cache ambiguity reports."""
        if len(self._cache) >= self._max_size:
            self._cache.pop(next(iter(self._cache)))

        key = self._make_key(tuple(symptom_ids))
        self._cache[key] = reports

    def clear(self) -> None:
        """Clear cache."""
        self._cache.clear()


class ConfidenceCalculationCache:
    """Cache for Bayesian confidence calculations (Stage 4)."""

    def __init__(self, max_size: int = 500):
        """Initialize confidence cache."""
        self._cache: Dict[str, Any] = {}
        self._max_size = max_size

    def _make_key(
        self,
        diseases: Tuple[str, ...],
        symptom_ids: Tuple[str, ...],
    ) -> str:
        """Generate cache key."""
        key_data = f"{','.join(sorted(diseases))}|{','.join(sorted(symptom_ids))}"
        return hashlib.md5(key_data.encode()).hexdigest()

    def get(
        self,
        diseases: List[str],
        symptom_ids: List[str],
    ) -> Optional[Dict[str, Any]]:
        """Get cached confidence breakdown."""
        key = self._make_key(tuple(diseases), tuple(symptom_ids))
        return self._cache.get(key)

    def put(
        self,
        diseases: List[str],
        symptom_ids: List[str],
        breakdown: Dict[str, Any],
    ) -> None:
        """Cache confidence breakdown."""
        if len(self._cache) >= self._max_size:
            self._cache.pop(next(iter(self._cache)))

        key = self._make_key(tuple(diseases), tuple(symptom_ids))
        self._cache[key] = breakdown

    def clear(self) -> None:
        """Clear cache."""
        self._cache.clear()


class QuestionTemplateCache:
    """Cache for diagnostic question templates (Stage 5)."""

    def __init__(self):
        """Initialize question template cache."""
        self._templates: Dict[Tuple[str, str], List[Dict[str, Any]]] = {}

    def get_differentiating_questions(
        self,
        disease_a: str,
        disease_b: str,
    ) -> Optional[List[Dict[str, Any]]]:
        """Get cached questions for disease pair."""
        key = tuple(sorted([disease_a, disease_b]))
        return self._templates.get(key)

    def cache_questions(
        self,
        disease_a: str,
        disease_b: str,
        questions: List[Dict[str, Any]],
    ) -> None:
        """Cache questions for disease pair."""
        key = tuple(sorted([disease_a, disease_b]))
        self._templates[key] = questions

    def clear(self) -> None:
        """Clear template cache."""
        self._templates.clear()

    def get_size(self) -> int:
        """Get cache size."""
        return len(self._templates)


class MultiDiseaseAnalysisCache:
    """Master cache manager for all Phase 6 operations."""

    def __init__(self):
        """Initialize all caches."""
        self.disease_meta = PrecomputedDiseaseMeta()
        self.symptom_context = SymptomContextCache()
        self.ambiguity_scores = AmbiguityScoreCache()
        self.confidence_calcs = ConfidenceCalculationCache()
        self.question_templates = QuestionTemplateCache()

    def initialize_from_database(self, disease_database: List[Dict[str, Any]]) -> None:
        """
        Initialize all caches from disease database.

        Called at application startup.

        Args:
            disease_database: Complete disease database
        """
        logger.info("Initializing multi-disease analysis caches...")
        self.disease_meta.build_from_database(disease_database)
        logger.info("Multi-disease caches initialized")

    def clear_all(self) -> None:
        """Clear all caches (for testing or cache invalidation)."""
        self.symptom_context.clear()
        self.ambiguity_scores.clear()
        self.confidence_calcs.clear()
        self.question_templates.clear()
        self.disease_meta.invalidate()

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get statistics across all caches."""
        return {
            "symptom_context": self.symptom_context.get_stats(),
            "ambiguity_scores": {
                "cached_items": len(self.ambiguity_scores._cache),
            },
            "confidence_calculations": {
                "cached_items": len(self.confidence_calcs._cache),
            },
            "question_templates": {
                "cached_pairs": self.question_templates.get_size(),
            },
            "disease_metadata": {
                "diseases": len(self.disease_meta.get_all_diseases()),
                "valid": self.disease_meta.is_valid(),
            },
        }


# Global cache instance (singleton)
_global_cache: Optional[MultiDiseaseAnalysisCache] = None


def get_global_cache() -> MultiDiseaseAnalysisCache:
    """Get global cache instance."""
    global _global_cache
    if _global_cache is None:
        _global_cache = MultiDiseaseAnalysisCache()
    return _global_cache


def initialize_caches(disease_database: List[Dict[str, Any]]) -> None:
    """
    Initialize global caches at application startup.

    Args:
        disease_database: Complete disease database
    """
    cache = get_global_cache()
    cache.initialize_from_database(disease_database)
