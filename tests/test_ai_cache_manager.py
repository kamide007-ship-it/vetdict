"""Tests for AI cache manager module."""

import time
import pytest
from api.ai.cache_manager import SymptomCache


def test_cache_hit():
    """Test cache hit when data exists and not expired."""
    cache = SymptomCache(ttl_seconds=3600)
    text = "test input"
    result = {"symptoms": ["coughing"], "confidence": 0.95}

    cache.set(text, result)
    retrieved = cache.get(text)

    assert retrieved == result
    assert cache.hits == 1
    assert cache.misses == 0


def test_cache_miss():
    """Test cache miss when data not present."""
    cache = SymptomCache(ttl_seconds=3600)
    text = "nonexistent input"

    retrieved = cache.get(text)

    assert retrieved is None
    assert cache.hits == 0
    assert cache.misses == 1


def test_cache_expiration():
    """Test cache expiration after TTL."""
    cache = SymptomCache(ttl_seconds=1)
    text = "test input"
    result = {"symptoms": ["coughing"], "confidence": 0.95}

    cache.set(text, result)
    time.sleep(1.1)

    retrieved = cache.get(text)

    assert retrieved is None
    assert cache.misses == 1


def test_cache_stats():
    """Test cache statistics reporting."""
    cache = SymptomCache(ttl_seconds=3600)
    text1 = "test1"
    text2 = "test2"
    result = {"symptoms": [], "confidence": 0.5}

    cache.set(text1, result)
    cache.get(text1)  # hit
    cache.get(text2)  # miss
    cache.get(text1)  # hit

    stats = cache.stats()

    assert stats["hits"] == 2
    assert stats["misses"] == 1
    assert stats["total"] == 3
    assert stats["hit_rate_pct"] > 66.0


def test_cache_clear_all():
    """Test clearing all cache entries."""
    cache = SymptomCache(ttl_seconds=3600)
    cache.set("text1", {"symptoms": []})
    cache.set("text2", {"symptoms": []})

    cache.clear_all()

    assert cache.get("text1") is None
    assert cache.hits == 0
    assert cache.misses == 1


def test_multiple_entries():
    """Test multiple entries in cache."""
    cache = SymptomCache(ttl_seconds=3600)

    for i in range(10):
        cache.set(f"text{i}", {"symptoms": [f"symptom{i}"]})

    stats = cache.stats()
    assert stats["cache_size"] == 10

    # Verify all are retrievable
    for i in range(10):
        result = cache.get(f"text{i}")
        assert result["symptoms"] == [f"symptom{i}"]
