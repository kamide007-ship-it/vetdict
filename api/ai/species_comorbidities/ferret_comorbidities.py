"""Ferret disease comorbidity relationships."""

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
    """Get ferret-specific comorbidity relationships."""
    relations = {}

    _add_relation(relations, "Adrenal Disease", "Hair Loss", 0.80, "hormonal", 1.2, 1.0)
    _add_relation(relations, "Lymphoma", "Splenomegaly", 0.75, "malignancy", 1.0, 1.3)
    _add_relation(relations, "Respiratory Infection", "Pneumonia", 0.60, "infection_spread", 1.1, 1.2)
    _add_relation(relations, "Hypoglycemia", "Insulinoma", 0.70, "pancreatic_tumor", 1.2, 1.25)
    _add_relation(relations, "Obesity", "Heart Disease", 0.50, "metabolic_cardiac", 1.15, 1.1)
    _add_relation(relations, "Intestinal Blockage", "Anorexia", 0.65, "obstruction", 1.0, 1.2)

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
