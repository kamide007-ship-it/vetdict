"""Canine (dog) disease comorbidity relationships.

Evidence-based disease comorbidity database specific to dogs.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass
class ComorbidityRelation:
    """Relationship between two diseases that commonly coexist."""

    disease_a: str
    disease_b: str
    base_probability: float  # 0-1, base likelihood they coexist
    mechanism: str  # e.g., "secondary_arthritis", "cascade_effect"
    age_factor: float  # Multiplier for age (>1.0 for seniors)
    severity_factor: float  # Multiplier for severity (>1.0 for severe cases)
    breed_predispositions: List[str] = None


def get_comorbidities() -> Dict[Tuple[str, str], ComorbidityRelation]:
    """
    Get all known dog comorbidity relationships.

    Returns:
        Dict mapping (disease_a, disease_b) to ComorbidityRelation
    """
    relations = {}

    # Orthopedic cascade: Hip Dysplasia → Osteoarthritis → Cognitive Dysfunction
    _add_relation(
        relations,
        "Hip Dysplasia",
        "Osteoarthritis",
        base_probability=0.85,
        mechanism="secondary_arthritis",
        age_factor=0.95,
        severity_factor=1.1,
        breed_predispositions=["German Shepherd", "Labrador", "Golden Retriever"],
    )

    _add_relation(
        relations,
        "Osteoarthritis",
        "Canine Cognitive Dysfunction",
        base_probability=0.45,
        mechanism="age_related_cascade",
        age_factor=1.3,
        severity_factor=0.9,
    )

    # Endocrine cascade: Pancreatitis → Diabetes
    _add_relation(
        relations,
        "Pancreatitis",
        "Diabetes Mellitus",
        base_probability=0.60,
        mechanism="endocrine_dysfunction",
        age_factor=1.05,
        severity_factor=0.85,
    )

    # GI complications: Pancreatitis + GDV
    _add_relation(
        relations,
        "Pancreatitis",
        "Gastric Dilatation-Volvulus (GDV/Bloat)",
        base_probability=0.35,
        mechanism="inflammatory_cascade",
        age_factor=0.9,
        severity_factor=1.25,
        breed_predispositions=["Great Dane", "German Shepherd", "Weimaraner"],
    )

    # GI disease: Pancreatitis + Gastroenteritis
    _add_relation(
        relations,
        "Pancreatitis",
        "Hemorrhagic Gastroenteritis (HGE)",
        base_probability=0.45,
        mechanism="inflammation_cascade",
        age_factor=0.95,
        severity_factor=1.15,
    )

    # Infection patterns: Viral → Secondary Bacterial
    _add_relation(
        relations,
        "Canine Parvovirus",
        "Bacterial Infection",
        base_probability=0.70,
        mechanism="immune_suppression",
        age_factor=1.05,
        severity_factor=1.20,
    )

    # Respiratory infections
    _add_relation(
        relations,
        "Pneumonia",
        "Tracheal Collapse",
        base_probability=0.40,
        mechanism="airway_inflammation",
        age_factor=1.1,
        severity_factor=1.0,
    )

    # Obesity cascade
    _add_relation(
        relations,
        "Obesity",
        "Diabetes Mellitus",
        base_probability=0.65,
        mechanism="metabolic_dysfunction",
        age_factor=1.1,
        severity_factor=0.95,
    )

    _add_relation(
        relations,
        "Obesity",
        "Hip Dysplasia",
        base_probability=0.55,
        mechanism="joint_stress",
        age_factor=1.05,
        severity_factor=1.05,
    )

    _add_relation(
        relations,
        "Obesity",
        "Pancreatitis",
        base_probability=0.50,
        mechanism="metabolic_dysfunction",
        age_factor=1.0,
        severity_factor=1.1,
    )

    # Systemic inflammation
    _add_relation(
        relations,
        "Inflammatory Bowel Disease (IBD)",
        "Canine Parvovirus",
        base_probability=0.30,
        mechanism="immune_dysregulation",
        age_factor=1.0,
        severity_factor=1.15,
    )

    # Urinary system
    _add_relation(
        relations,
        "Urinary Tract Infection",
        "Bladder Stones",
        base_probability=0.55,
        mechanism="crystal_formation",
        age_factor=1.1,
        severity_factor=0.9,
    )

    # Kidney disease cascade
    _add_relation(
        relations,
        "Kidney Disease (CKD)",
        "Hypertension",
        base_probability=0.60,
        mechanism="secondary_hypertension",
        age_factor=1.15,
        severity_factor=1.0,
    )

    _add_relation(
        relations,
        "Kidney Disease (CKD)",
        "Anemia",
        base_probability=0.50,
        mechanism="chronic_disease_anemia",
        age_factor=1.1,
        severity_factor=0.95,
    )

    # Heart disease
    _add_relation(
        relations,
        "Heart Disease/CHF",
        "Pneumonia",
        base_probability=0.40,
        mechanism="pulmonary_edema",
        age_factor=1.15,
        severity_factor=1.0,
    )

    # Dermatologic cascade
    _add_relation(
        relations,
        "Allergic Dermatitis",
        "Secondary Bacterial Infection",
        base_probability=0.75,
        mechanism="barrier_dysfunction",
        age_factor=1.0,
        severity_factor=1.2,
    )

    # Parasitic infections
    _add_relation(
        relations,
        "Intestinal Parasites",
        "Anemia",
        base_probability=0.40,
        mechanism="blood_loss",
        age_factor=1.1,
        severity_factor=0.9,
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

    # Add both directions (A→B and B→A)
    relations[(disease_a, disease_b)] = relation
    relations[(disease_b, disease_a)] = relation
