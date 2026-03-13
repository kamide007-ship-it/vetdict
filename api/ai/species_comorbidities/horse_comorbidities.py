"""Equine (horse) disease comorbidity relationships."""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass
class ComorbidityRelation:
    disease_a: str
    disease_b: str
    base_probability: float
    mechanism: str
    age_factor: float
    severity_factor: float
    breed_predispositions: List[str] = None


def get_comorbidities() -> Dict[Tuple[str, str], ComorbidityRelation]:
    """Get horse-specific comorbidity relationships."""
    relations = {}

    _add_relation(relations, "Colic", "Dehydration", 0.75, "fluid_loss", 1.1, 1.3)
    _add_relation(relations, "Lameness", "Osteoarthritis", 0.80, "joint_stress", 1.15, 1.2)
    _add_relation(relations, "Equine Metabolic Syndrome (EMS)", "Laminitis", 0.85, "metabolic_inflammatory", 1.2, 1.3)
    _add_relation(relations, "Respiratory Disease", "Pneumonia", 0.65, "infection_spread", 1.1, 1.25)
    _add_relation(relations, "Heaves (COPD)", "Respiratory Infection", 0.70, "chronic_inflammation", 1.15, 1.1)
    _add_relation(relations, "Ulcers (EGUS)", "Colic", 0.60, "pain_dysfunction", 1.0, 1.2)
    _add_relation(relations, "Obesity", "Equine Metabolic Syndrome", 0.75, "metabolic_dysfunction", 1.15, 1.1)

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
    relation = ComorbidityRelation(
        disease_a, disease_b, base_probability, mechanism, age_factor, severity_factor, breed_predispositions
    )
    relations[(disease_a, disease_b)] = relation
    relations[(disease_b, disease_a)] = relation
