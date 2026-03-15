"""Disease data loader with DB-first, Python-fallback strategy.

This module provides ``load_diseases`` which tries to load disease data from
the SQLite database first. If the database is unavailable or has no data for
the requested species, it falls back to the hard-coded Python dictionaries.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

# Cache to avoid repeated DB queries within a single process
_cache: Dict[str, List[Dict[str, Any]]] = {}


def load_diseases(species: str, fallback_diseases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Load diseases for a species, preferring the database.

    Parameters
    ----------
    species:
        Species key (e.g. "cat", "dog").
    fallback_diseases:
        The hard-coded DISEASES list from the Python module, used when the
        database is unavailable or empty for this species.

    Returns
    -------
    list
        Disease dictionaries compatible with ``analyze_symptoms_generic``.
    """
    if species in _cache:
        return _cache[species]

    try:
        from api.database import has_diseases_for_species, get_diseases_for_species
        if has_diseases_for_species(species):
            diseases = get_diseases_for_species(species)
            if diseases:
                logger.debug("Loaded %d diseases for %s from database", len(diseases), species)
                _cache[species] = diseases
                return diseases
    except Exception as exc:
        logger.debug("DB load failed for %s, using fallback: %s", species, exc)

    _cache[species] = fallback_diseases
    return fallback_diseases


def invalidate_cache(species: str | None = None):
    """Clear the disease cache, forcing a reload on next access.

    Parameters
    ----------
    species:
        If given, only invalidate cache for this species.
        If None, clear the entire cache.
    """
    if species is None:
        _cache.clear()
    else:
        _cache.pop(species, None)
