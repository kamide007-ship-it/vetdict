"""Species data loading for the diagnostic chat system.

Lazily loads disease and symptom data from species modules on first access.
Reduces startup memory from ~530MB to ~50MB (Render 512MB free tier).
"""

import importlib as _importlib
import logging

from api.chat.constants import _GENERIC_SPECIES

logger = logging.getLogger(__name__)

_SPECIES_DATA: dict = {}  # {species: {"diseases": [...], "symptom_names": {...}}}
_SPECIES_LOADED: set = set()


def _ensure_species_loaded(species: str) -> None:
    """Load a species module on first access."""
    if species in _SPECIES_LOADED:
        return
    _SPECIES_LOADED.add(species)
    try:
        _mod = _importlib.import_module(f"api.species.{species}_diseases")
    except ImportError:
        try:
            _mod = _importlib.import_module(f"species.{species}_diseases")
        except ImportError:
            return
    _SPECIES_DATA[species] = {
        "diseases": _mod.DISEASES,
        "symptom_names": _mod.SYMPTOM_NAMES,
        "symptom_categories": getattr(_mod, "SYMPTOM_CATEGORIES", {}),
    }


def get_species_data(species: str) -> dict:
    """Get species data, loading lazily if needed."""
    _ensure_species_loaded(species)
    return _SPECIES_DATA.get(species, {})
