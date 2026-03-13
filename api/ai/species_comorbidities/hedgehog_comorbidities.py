"""Hedgehog disease comorbidity relationships."""

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
    """Get hedgehog-specific comorbidity relationships."""
    relations = {}

    _add_relation(relations, "Respiratory Infection", "Pneumonia", 0.65, "infection_spread", 1.1, 1.25)
    _add_relation(relations, "Hedgehog Wobbly Syndrome", "Neurological Decline", 0.70, "degenerative", 1.3, 1.15)
    _add_relation(relations, "Obesity", "Metabolic Disease", 0.60, "metabolic_dysfunction", 1.1, 1.0)
    _add_relation(relations, "Dental Disease", "Anorexia", 0.65, "pain_induced", 1.0, 1.2)
    _add_relation(relations, "Intestinal Parasites", "Malnutrition", 0.50, "nutrient_loss", 1.05, 1.0)
    _add_relation(relations, "Quill Loss", "Skin Infection", 0.55, "barrier_dysfunction", 1.0, 1.1)

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
