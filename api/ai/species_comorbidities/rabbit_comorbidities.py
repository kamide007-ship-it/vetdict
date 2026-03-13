"""Lagomorph (rabbit) disease comorbidity relationships.

Evidence-based disease comorbidity database specific to rabbits.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass
class ComorbidityRelation:
    """Relationship between two diseases that commonly coexist."""

    disease_a: str
    disease_b: str
    base_probability: float
    mechanism: str
    age_factor: float
    severity_factor: float
    breed_predispositions: List[str] = None


def get_comorbidities() -> Dict[Tuple[str, str], ComorbidityRelation]:
    """Get all known rabbit comorbidity relationships."""
    relations = {}

    # GI stasis cascade - critical in rabbits
    _add_relation(
        relations,
        "Gastrointestinal Stasis",
        "Enterotoxemia",
        base_probability=0.70,
        mechanism="bacterial_overgrowth",
        age_factor=1.1,
        severity_factor=1.3,
    )

    _add_relation(
        relations,
        "Gastrointestinal Stasis",
        "Dehydration",
        base_probability=0.75,
        mechanism="fluid_loss",
        age_factor=1.1,
        severity_factor=1.2,
    )

    # Respiratory infections
    _add_relation(
        relations,
        "Pasteurellosis (Snuffles)",
        "Otitis Media/Interna",
        base_probability=0.60,
        mechanism="bacterial_spread",
        age_factor=1.0,
        severity_factor=1.15,
    )

    _add_relation(
        relations,
        "Pasteurellosis (Snuffles)",
        "Pneumonia",
        base_probability=0.50,
        mechanism="respiratory_infection",
        age_factor=1.0,
        severity_factor=1.2,
    )

    # Dental disease cascade
    _add_relation(
        relations,
        "Dental Disease",
        "Gastrointestinal Stasis",
        base_probability=0.65,
        mechanism="pain_induced_anorexia",
        age_factor=1.1,
        severity_factor=1.15,
    )

    _add_relation(
        relations,
        "Dental Disease",
        "Abscess Formation",
        base_probability=0.55,
        mechanism="bacterial_infection",
        age_factor=1.0,
        severity_factor=1.1,
    )

    # Parasitic infections
    _add_relation(
        relations,
        "Intestinal Parasites",
        "Gastrointestinal Stasis",
        base_probability=0.45,
        mechanism="irritation",
        age_factor=1.0,
        severity_factor=1.05,
    )

    # Urinary disease
    _add_relation(
        relations,
        "Urinary Calculi",
        "Urinary Tract Infection",
        base_probability=0.65,
        mechanism="obstruction_infection",
        age_factor=1.1,
        severity_factor=1.2,
    )

    # Viral infections
    _add_relation(
        relations,
        "Rabbit Hemorrhagic Disease (RHD)",
        "Secondary Infection",
        base_probability=0.80,
        mechanism="immune_suppression",
        age_factor=1.0,
        severity_factor=1.3,
    )

    # Obesity-related
    _add_relation(
        relations,
        "Obesity",
        "Gastrointestinal Stasis",
        base_probability=0.50,
        mechanism="mobility_reduction",
        age_factor=1.05,
        severity_factor=1.1,
    )

    # Myxomatosis
    _add_relation(
        relations,
        "Myxomatosis",
        "Secondary Infection",
        base_probability=0.75,
        mechanism="immune_suppression",
        age_factor=1.0,
        severity_factor=1.25,
    )

    return relations


def _add_relation(
    relations: Dict[Tuple[str, str], ComorbidityRelation],
    disease_a: str,
    disease_b: str,
    base_probability: float,
    mechanism: str,
    age_factor: float,
    severity_factor: float,
    breed_predispositions: Optional[List[str]] = None,
):
    """Helper to add bidirectional comorbidity relationships."""
    relation = ComorbidityRelation(
        disease_a=disease_a,
        disease_b=disease_b,
        base_probability=base_probability,
        mechanism=mechanism,
        age_factor=age_factor,
        severity_factor=severity_factor,
        breed_predispositions=breed_predispositions,
    )

    relations[(disease_a, disease_b)] = relation
    relations[(disease_b, disease_a)] = relation
