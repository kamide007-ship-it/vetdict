"""Bird disease comorbidity relationships."""

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
    """Get bird-specific comorbidity relationships."""
    relations = {}

    _add_relation(relations, "Respiratory Infection", "Pneumonia", 0.70, "infection_spread", 1.1, 1.3)
    _add_relation(relations, "Malnutrition", "Immunosuppression", 0.65, "nutrient_deficiency", 1.0, 1.2)
    _add_relation(relations, "Feather Plucking", "Dermatitis", 0.60, "behavioral_skin", 1.0, 1.1)
    _add_relation(relations, "Egg Binding", "Hypocalcemia", 0.75, "metabolic", 1.2, 1.3)
    _add_relation(relations, "Heavy Metal Toxicity", "Anemia", 0.70, "toxin_effect", 1.0, 1.25)
    _add_relation(relations, "Fungal Infection", "Respiratory Disease", 0.55, "aspergillosis", 1.1, 1.2)

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
