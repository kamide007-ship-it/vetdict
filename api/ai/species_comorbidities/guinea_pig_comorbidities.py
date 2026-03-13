"""Guinea pig disease comorbidity relationships."""

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
    """Get guinea pig-specific comorbidity relationships."""
    relations = {}

    _add_relation(relations, "Respiratory Infection", "Pneumonia", 0.65, "infection_spread", 1.1, 1.25)
    _add_relation(relations, "Scurvy (Vitamin C Deficiency)", "Infection", 0.55, "immune_suppression", 1.0, 1.15)
    _add_relation(relations, "Diarrhea", "Dehydration", 0.70, "fluid_loss", 1.1, 1.2)
    _add_relation(relations, "Obesity", "Metabolic_Disease", 0.50, "metabolic_dysfunction", 1.1, 1.0)
    _add_relation(relations, "Dental Disease", "Anorexia", 0.65, "pain_induced", 1.15, 1.2)
    _add_relation(relations, "Intestinal Parasites", "Malnutrition", 0.45, "nutrient_loss", 1.0, 0.95)

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
