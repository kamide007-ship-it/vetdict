"""cache_manager.py – In-memory cache for symptom extraction results

Provides thread-safe caching with TTL-based expiration to reduce
repeated API calls and improve performance.
"""

import hashlib
import threading
import time
from typing import Any, Dict, Optional


class SymptomCache:
    """Thread-safe in-memory cache with TTL-based expiration."""

    def __init__(self, ttl_seconds: int = 3600):
        """
        Initialize cache.

        Args:
            ttl_seconds: Time-to-live in seconds (default 1 hour)
        """
        self._cache: Dict[str, tuple] = {}  # {text_hash: (result, timestamp)}
        self._lock = threading.RLock()
        self.ttl = ttl_seconds
        self.hits = 0
        self.misses = 0

    @staticmethod
    def _hash_text(text: str) -> str:
        """Hash text for cache key (SHA256)."""
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def get(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve cached result if available and not expired.

        Args:
            text: Input text to look up

        Returns:
            Cached result dict, or None if miss/expired
        """
        key = self._hash_text(text)
        with self._lock:
            if key not in self._cache:
                self.misses += 1
                return None

            result, timestamp = self._cache[key]
            if time.time() - timestamp > self.ttl:
                # Expired
                del self._cache[key]
                self.misses += 1
                return None

            self.hits += 1
            return result

    def set(self, text: str, result: Dict[str, Any]) -> None:
        """
        Store result in cache.

        Args:
            text: Input text (cache key)
            result: Result dictionary to cache
        """
        key = self._hash_text(text)
        with self._lock:
            self._cache[key] = (result, time.time())

    def clear(self) -> None:
        """Clear all expired entries."""
        with self._lock:
            current_time = time.time()
            expired_keys = [
                k for k, (_, ts) in self._cache.items()
                if current_time - ts > self.ttl
            ]
            for k in expired_keys:
                del self._cache[k]

    def clear_all(self) -> None:
        """Clear all cache entries."""
        with self._lock:
            self._cache.clear()
            self.hits = 0
            self.misses = 0

    def stats(self) -> Dict[str, Any]:
        """
        Return cache statistics.

        Returns:
            Dict with hit rate, size, and stats
        """
        with self._lock:
            total = self.hits + self.misses
            hit_rate = (self.hits / total * 100) if total > 0 else 0.0
            return {
                "hits": self.hits,
                "misses": self.misses,
                "total": total,
                "hit_rate_pct": round(hit_rate, 2),
                "cache_size": len(self._cache),
                "ttl_seconds": self.ttl,
            }
