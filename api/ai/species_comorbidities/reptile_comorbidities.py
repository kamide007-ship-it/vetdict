"""Reptile disease comorbidity relationships."""

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
    """Get reptile-specific comorbidity relationships."""
    relations = {}

    _add_relation(relations, "Metabolic Bone Disease", "Kidney Disease", 0.70, "calcium_dysregulation", 1.2, 1.2)
    _add_relation(relations, "Respiratory Infection", "Pneumonia", 0.65, "infection_spread", 1.1, 1.3)
    _add_relation(relations, "Parasitic Infection", "Anemia", 0.60, "blood_loss", 1.1, 1.0)
    _add_relation(relations, "Thermal Stress", "Immunosuppression", 0.55, "temperature_stress", 1.0, 1.15)
    _add_relation(relations, "Mouth Rot", "Anorexia", 0.70, "pain_infection", 1.0, 1.2)
    _add_relation(relations, "Intestinal Impaction", "Anorexia", 0.65, "obstruction", 1.05, 1.25)

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
