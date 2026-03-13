"""Central registry for species-specific disease comorbidity databases.

Loads and manages comorbidity relationships for all supported species,
providing lazy-loaded access to avoid memory overhead.
"""

from typing import Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

# Lazy-loaded comorbidity databases per species
_SPECIES_DATABASES: Dict[str, Optional[Dict[Tuple[str, str], any]]] = {
    "dog": None,
    "cat": None,
    "rabbit": None,
    "hamster": None,
    "guinea_pig": None,
    "ferret": None,
    "bird": None,
    "reptile": None,
    "horse": None,
    "hedgehog": None,
}


def load_species_comorbidities(species: str) -> Dict[Tuple[str, str], any]:
    """
    Load comorbidity database for a specific species (lazy loading).

    Args:
        species: Target species name

    Returns:
        Dict of (disease_a, disease_b) → ComorbidityRelation

    Raises:
        ValueError: If species not supported
    """
    species_lower = species.lower()

    if species_lower not in _SPECIES_DATABASES:
        raise ValueError(f"Unsupported species: {species}")

    # Check if already loaded
    if _SPECIES_DATABASES[species_lower] is not None:
        return _SPECIES_DATABASES[species_lower]

    # Lazy load the appropriate module
    try:
        if species_lower == "dog":
            from . import dog_comorbidities
            comorbidities = dog_comorbidities.get_comorbidities()
        elif species_lower == "cat":
            from . import cat_comorbidities
            comorbidities = cat_comorbidities.get_comorbidities()
        elif species_lower == "rabbit":
            from . import rabbit_comorbidities
            comorbidities = rabbit_comorbidities.get_comorbidities()
        elif species_lower == "hamster":
            from . import hamster_comorbidities
            comorbidities = hamster_comorbidities.get_comorbidities()
        elif species_lower == "guinea_pig":
            from . import guinea_pig_comorbidities
            comorbidities = guinea_pig_comorbidities.get_comorbidities()
        elif species_lower == "ferret":
            from . import ferret_comorbidities
            comorbidities = ferret_comorbidities.get_comorbidities()
        elif species_lower == "bird":
            from . import bird_comorbidities
            comorbidities = bird_comorbidities.get_comorbidities()
        elif species_lower == "reptile":
            from . import reptile_comorbidities
            comorbidities = reptile_comorbidities.get_comorbidities()
        elif species_lower == "horse":
            from . import horse_comorbidities
            comorbidities = horse_comorbidities.get_comorbidities()
        elif species_lower == "hedgehog":
            from . import hedgehog_comorbidities
            comorbidities = hedgehog_comorbidities.get_comorbidities()
        else:
            comorbidities = {}

        _SPECIES_DATABASES[species_lower] = comorbidities
        logger.info(f"Loaded {len(comorbidities)} comorbidities for {species}")
        return comorbidities

    except ImportError as e:
        logger.warning(f"Could not load comorbidities for {species}: {e}")
        _SPECIES_DATABASES[species_lower] = {}
        return {}


def get_comorbidity_db(species: str) -> Dict[Tuple[str, str], any]:
    """
    Get comorbidity database for a species (wrapper for load_species_comorbidities).

    Args:
        species: Target species name

    Returns:
        Comorbidity database dict
    """
    return load_species_comorbidities(species)


def clear_cache():
    """Clear the lazy-loaded comorbidity cache."""
    global _SPECIES_DATABASES
    _SPECIES_DATABASES = {
        "dog": None,
        "cat": None,
        "rabbit": None,
        "hamster": None,
        "guinea_pig": None,
        "ferret": None,
        "bird": None,
        "reptile": None,
        "horse": None,
        "hedgehog": None,
    }


def get_supported_species() -> list:
    """Get list of supported species."""
    return list(_SPECIES_DATABASES.keys())
