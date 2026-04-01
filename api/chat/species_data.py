"""Species data loading for the diagnostic chat system.

Loads disease and symptom data from all species modules at import time.
Provides _SPECIES_DATA dict used by extractors and matchers.
"""

import importlib as _importlib
import logging

from api.chat.constants import _GENERIC_SPECIES

logger = logging.getLogger(__name__)

_SPECIES_DATA: dict = {}  # {species: {"diseases": [...], "symptom_names": {...}}}

for _sp in _GENERIC_SPECIES:
    try:
        _mod = _importlib.import_module(f"api.species.{_sp}_diseases")
    except ImportError:
        try:
            _mod = _importlib.import_module(f"species.{_sp}_diseases")
        except ImportError:
            continue
    _SPECIES_DATA[_sp] = {
        "diseases": _mod.DISEASES,
        "symptom_names": _mod.SYMPTOM_NAMES,
        "symptom_categories": getattr(_mod, "SYMPTOM_CATEGORIES", {}),
    }
