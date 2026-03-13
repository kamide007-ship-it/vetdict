"""Clinical frequency helpers for symptom presentation metadata."""

from __future__ import annotations

from typing import Any

CLINICAL_FREQUENCY: dict[str, dict[str, dict[str, Any]]] = {}


def get_clinical_frequency(
    disease_name: str,
    symptom_id: str,
) -> dict[str, Any] | None:
    """Return clinical frequency metadata for a disease/symptom pair."""
    return CLINICAL_FREQUENCY.get(disease_name, {}).get(symptom_id)


def get_all_regions_frequency(disease_name: str) -> dict[str, dict[str, Any]]:
    """Return all clinical frequency metadata for a disease."""
    return CLINICAL_FREQUENCY.get(disease_name, {})
