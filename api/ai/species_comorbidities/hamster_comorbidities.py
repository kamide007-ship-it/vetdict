"""Hamster disease comorbidity relationships."""

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
    """Get hamster-specific comorbidity relationships."""
    relations = {}

    _add_relation(relations, "Wet Tail", "Dehydration", 0.75, "fluid_loss", 1.2, 1.3)
    _add_relation(relations, "Wet Tail", "Secondary_Infection", 0.65, "bacterial_overgrowth", 1.0, 1.15)
    _add_relation(relations, "Respiratory Infection", "Pneumonia", 0.60, "infection_spread", 1.1, 1.2)
    _add_relation(relations, "Dental Overgrowth", "Anorexia", 0.70, "pain_induced", 1.1, 1.15)
    _add_relation(relations, "Obesity", "Diabetes", 0.55, "metabolic", 1.1, 1.0)
    _add_relation(relations, "Intestinal Parasites", "Anemia", 0.50, "blood_loss", 1.1, 0.95)

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
