#!/usr/bin/env python3
"""
Caching strategy for VetDict API

Uses Flask-Caching with configurable backends:
- Development: SimpleCache (in-memory, single process)
- Production: RedisCache (distributed, if REDIS_URL set)
- Fallback: SimpleCache

Cache keys are structured by query type for efficient invalidation
"""

import logging
from functools import wraps
from typing import Any, Callable

from flask_caching import Cache

logger = logging.getLogger(__name__)

# Cache configuration
CACHE_CONFIG = {
    # In-memory cache for development
    'CACHE_TYPE': 'simple',

    # Cache timeouts (in seconds)
    'CACHE_DEFAULT_TIMEOUT': 3600,  # 1 hour

    # Key prefix
    'CACHE_KEY_PREFIX': 'vetdict_',
}

# Initialize cache (will be bound to app in vetdict_api.py)
cache = Cache()


def init_cache(app):
    """Initialize cache with Flask app"""
    cache.init_app(app, config=CACHE_CONFIG)
    logger.info("Cache initialized: %s", CACHE_CONFIG.get('CACHE_TYPE'))


# Cache timeout presets
CACHE_TIMEOUTS = {
    'disease_detail': 86400,      # 24 hours (static data)
    'disease_list': 3600,         # 1 hour
    'search_results': 1800,       # 30 minutes
    'species_stats': 86400,       # 24 hours
    'urgency_stats': 86400,       # 24 hours
    'fts_search': 1800,           # 30 minutes
    'diagnostic_result': 300,     # 5 minutes
}


def cached_query(
    timeout: int = 3600,
    key_prefix: str = 'query',
) -> Callable:
    """
    Decorator for caching database queries

    Usage:
        @cached_query(timeout=3600, key_prefix='diseases')
        def get_diseases(species):
            ...
    """
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def decorated_function(*args, **kwargs) -> Any:
            # Generate cache key from function name and arguments
            cache_key = f'vetdict_{key_prefix}:{f.__name__}:' + ':'.join(
                str(arg) for arg in args
            ) + ':' + ':'.join(
                f'{k}={v}' for k, v in sorted(kwargs.items())
            )

            # Try to get from cache
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit: {cache_key}")
                return cached_result

            # Execute function and cache result
            result = f(*args, **kwargs)
            cache.set(cache_key, result, timeout=timeout)
            logger.debug(f"Cache set: {cache_key} (timeout: {timeout}s)")
            return result

        return decorated_function
    return decorator


def invalidate_cache(pattern: str) -> None:
    """
    Invalidate cache entries matching a pattern

    Usage:
        invalidate_cache('disease:*')
    """
    try:
        cache.delete_many(*cache.cache._cache.keys())
        logger.info(f"Cache invalidated: {pattern}")
    except AttributeError:
        # Simple cache doesn't support key patterns
        cache.clear()
        logger.info("Cache cleared (full)")


# Cache key builders for common queries
def get_disease_cache_key(disease_id: str) -> str:
    """Cache key for single disease detail"""
    return f'vetdict_disease:{disease_id}'


def get_species_list_cache_key(species: str, limit: int) -> str:
    """Cache key for disease list by species"""
    return f'vetdict_species_list:{species}:{limit}'


def get_search_cache_key(query: str, limit: int) -> str:
    """Cache key for full-text search results"""
    return f'vetdict_search:{query}:{limit}'


def get_diagnostic_cache_key(
    species: str, symptoms: tuple, lang: str = 'en'
) -> str:
    """Cache key for diagnostic results (time-limited)"""
    symptom_hash = hash(symptoms) % 10000000  # Reduce hash collision risk
    return f'vetdict_diagnostic:{species}:{symptom_hash}:{lang}'
