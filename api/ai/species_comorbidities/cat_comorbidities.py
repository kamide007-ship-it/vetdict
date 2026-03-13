"""Feline (cat) disease comorbidity relationships.

Evidence-based disease comorbidity database specific to cats.
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
    Get all known cat comorbidity relationships.

    Returns:
        Dict mapping (disease_a, disease_b) to ComorbidityRelation
    """
    relations = {}

    # Urinary system - FIC and crystals are highly associated in cats
    _add_relation(
        relations,
        "Feline Idiopathic Cystitis (FIC)",
        "Urinary Crystals/Stones",
        base_probability=0.70,
        mechanism="inflammatory_predisposition",
        age_factor=1.1,
        severity_factor=1.2,
    )

    # Respiratory cascade in cats
    _add_relation(
        relations,
        "Feline Upper Respiratory Infection",
        "Feline Asthma",
        base_probability=0.45,
        mechanism="airway_inflammation",
        age_factor=1.0,
        severity_factor=1.1,
    )

    _add_relation(
        relations,
        "Feline Asthma",
        "Bronchitis",
        base_probability=0.55,
        mechanism="chronic_inflammation",
        age_factor=1.1,
        severity_factor=1.0,
    )

    # Thyroid disease and other age-related conditions
    _add_relation(
        relations,
        "Hyperthyroidism",
        "Heart Disease (HCM)",
        base_probability=0.50,
        mechanism="metabolic_cardiac_stress",
        age_factor=1.2,
        severity_factor=1.1,
    )

    _add_relation(
        relations,
        "Hyperthyroidism",
        "Hypertension",
        base_probability=0.60,
        mechanism="metabolic_hypertension",
        age_factor=1.15,
        severity_factor=1.0,
    )

    # Kidney disease cascade in geriatric cats
    _add_relation(
        relations,
        "Kidney Disease (CKD)",
        "Anemia",
        base_probability=0.55,
        mechanism="chronic_disease_anemia",
        age_factor=1.2,
        severity_factor=0.9,
    )

    _add_relation(
        relations,
        "Kidney Disease (CKD)",
        "Hypertension",
        base_probability=0.65,
        mechanism="secondary_hypertension",
        age_factor=1.2,
        severity_factor=1.0,
    )

    _add_relation(
        relations,
        "Kidney Disease (CKD)",
        "Hyperthyroidism",
        base_probability=0.35,
        mechanism="age_related_coexistence",
        age_factor=1.3,
        severity_factor=0.9,
    )

    # Diabetes in cats (often insulin-responsive)
    _add_relation(
        relations,
        "Diabetes Mellitus",
        "Obesity",
        base_probability=0.60,
        mechanism="metabolic_dysfunction",
        age_factor=1.1,
        severity_factor=1.0,
    )

    _add_relation(
        relations,
        "Diabetes Mellitus",
        "Pancreatitis",
        base_probability=0.50,
        mechanism="endocrine_inflammation",
        age_factor=1.0,
        severity_factor=1.2,
    )

    # GI disease in cats
    _add_relation(
        relations,
        "Inflammatory Bowel Disease (IBD)",
        "Pancreatitis",
        base_probability=0.55,
        mechanism="systemic_inflammation",
        age_factor=1.0,
        severity_factor=1.15,
    )

    _add_relation(
        relations,
        "Inflammatory Bowel Disease (IBD)",
        "Lymphoma",
        base_probability=0.40,
        mechanism="chronic_inflammatory_predisposition",
        age_factor=1.1,
        severity_factor=1.2,
    )

    # Viral infections (FIV, FeLV) and secondary conditions
    _add_relation(
        relations,
        "Feline Immunodeficiency Virus (FIV)",
        "Stomatitis",
        base_probability=0.65,
        mechanism="immune_suppression",
        age_factor=1.0,
        severity_factor=1.15,
    )

    _add_relation(
        relations,
        "Feline Immunodeficiency Virus (FIV)",
        "Secondary Infection",
        base_probability=0.75,
        mechanism="immune_suppression",
        age_factor=1.0,
        severity_factor=1.2,
    )

    _add_relation(
        relations,
        "Feline Leukemia Virus (FeLV)",
        "Lymphoma",
        base_probability=0.70,
        mechanism="viral_oncogenic",
        age_factor=1.0,
        severity_factor=1.3,
    )

    # Dermatologic conditions
    _add_relation(
        relations,
        "Allergic Dermatitis",
        "Secondary Bacterial Infection",
        base_probability=0.65,
        mechanism="barrier_dysfunction",
        age_factor=1.0,
        severity_factor=1.2,
    )

    _add_relation(
        relations,
        "Allergic Dermatitis",
        "Otitis (Ear Infection)",
        base_probability=0.55,
        mechanism="allergic_inflammatory",
        age_factor=1.0,
        severity_factor=1.0,
    )

    # Behavioral/stress-related conditions
    _add_relation(
        relations,
        "Feline Lower Urinary Tract Disease (FLUTD)",
        "Stress-Related Behavior",
        base_probability=0.50,
        mechanism="stress_triggered",
        age_factor=1.0,
        severity_factor=1.15,
    )

    # Arthritis in older cats
    _add_relation(
        relations,
        "Osteoarthritis",
        "Mobility Reduction",
        base_probability=0.80,
        mechanism="mechanical_joint_damage",
        age_factor=1.2,
        severity_factor=1.0,
    )

    # Heart disease associations
    _add_relation(
        relations,
        "Heart Disease (HCM)",
        "Hypertension",
        base_probability=0.55,
        mechanism="cardiovascular_dysfunction",
        age_factor=1.15,
        severity_factor=1.1,
    )

    _add_relation(
        relations,
        "Heart Disease (HCM)",
        "Thromboembolism",
        base_probability=0.45,
        mechanism="cardiac_stasis",
        age_factor=1.0,
        severity_factor=1.3,
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
