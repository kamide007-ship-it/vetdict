"""Disease comorbidity modeling and interaction analysis.

Identifies which diseases commonly coexist in veterinary practice and models
their interactions for simultaneous multi-disease diagnosis.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set, Tuple
import logging

logger = logging.getLogger(__name__)


@dataclass
class ComorbidityRelation:
    """Relationship between two diseases that commonly coexist."""

    disease_a: str
    disease_b: str
    base_probability: float  # 0-1, base likelihood they coexist
    mechanism: str  # e.g., "secondary_arthritis", "cascade_effect"
    age_factor: float  # Multiplier for age (>1.0 for seniors)
    severity_factor: float  # Multiplier for severity (>1.0 for severe cases)
    breed_predispositions: List[str] = None  # Breeds predisposed to this pairing

    def to_dict(self):
        return {
            "disease_a": self.disease_a,
            "disease_b": self.disease_b,
            "base_probability": round(self.base_probability, 3),
            "mechanism": self.mechanism,
            "age_factor": round(self.age_factor, 3),
            "severity_factor": round(self.severity_factor, 3),
            "breed_predispositions": self.breed_predispositions or [],
        }


class DiseaseInteractionMatrix:
    """Matrix of disease comorbidities and interactions."""

    # Core comorbidity relationships
    # Key format: (disease_a, disease_b, species) for multi-species support
    # Legacy format: (disease_a, disease_b) for backward compatibility (defaults to 'dog')
    COMORBIDITY_DATABASE: Dict[Tuple[str, str], ComorbidityRelation] = {}
    SPECIES_COMORBIDITY_DATABASE: Dict[Tuple[str, str, str], ComorbidityRelation] = {}

    # Supported species
    SUPPORTED_SPECIES = {
        "dog", "cat", "rabbit", "hamster", "guinea_pig", "ferret",
        "bird", "reptile", "horse", "hedgehog"
    }

    @classmethod
    def initialize(cls):
        """Initialize comorbidity database with medical knowledge."""
        cls._load_known_comorbidities()

    @classmethod
    def _load_known_comorbidities(cls):
        """Load evidence-based disease comorbidity relationships."""

        # Orthopedic cascade: Hip Dysplasia → Osteoarthritis → Cognitive Dysfunction
        cls._add_comorbidity(
            "Hip Dysplasia",
            "Osteoarthritis",
            base_probability=0.85,
            mechanism="secondary_arthritis",
            age_factor=0.95,
            severity_factor=1.1,
            breed_predispositions=["German Shepherd", "Labrador", "Golden Retriever"],
        )

        cls._add_comorbidity(
            "Osteoarthritis",
            "Canine Cognitive Dysfunction",
            base_probability=0.45,
            mechanism="age_related_cascade",
            age_factor=1.3,
            severity_factor=0.9,
        )

        # Endocrine cascade: Pancreatitis → Diabetes
        cls._add_comorbidity(
            "Pancreatitis",
            "Diabetes Mellitus",
            base_probability=0.60,
            mechanism="endocrine_dysfunction",
            age_factor=1.05,
            severity_factor=0.85,
        )

        # GI complications: Pancreatitis + GDV
        cls._add_comorbidity(
            "Pancreatitis",
            "Gastric Dilatation-Volvulus (GDV/Bloat)",
            base_probability=0.35,
            mechanism="inflammatory_cascade",
            age_factor=0.9,
            severity_factor=1.25,
            breed_predispositions=["Great Dane", "German Shepherd", "Weimaraner"],
        )

        # GI disease: Pancreatitis + Gastroenteritis
        cls._add_comorbidity(
            "Pancreatitis",
            "Hemorrhagic Gastroenteritis (HGE)",
            base_probability=0.45,
            mechanism="inflammation_cascade",
            age_factor=0.95,
            severity_factor=1.15,
        )

        # Infection patterns: Viral → Secondary Bacterial
        cls._add_comorbidity(
            "Canine Parvovirus",
            "Bacterial Infection",
            base_probability=0.70,
            mechanism="immune_suppression",
            age_factor=1.05,
            severity_factor=1.20,
        )

        # Respiratory infections
        cls._add_comorbidity(
            "Pneumonia",
            "Tracheal Collapse",
            base_probability=0.40,
            mechanism="airway_inflammation",
            age_factor=1.1,
            severity_factor=1.0,
        )

        # Obesity cascade
        cls._add_comorbidity(
            "Obesity",
            "Diabetes Mellitus",
            base_probability=0.65,
            mechanism="metabolic_dysfunction",
            age_factor=1.1,
            severity_factor=0.95,
        )

        cls._add_comorbidity(
            "Obesity",
            "Hip Dysplasia",
            base_probability=0.55,
            mechanism="joint_stress",
            age_factor=1.05,
            severity_factor=1.05,
        )

        cls._add_comorbidity(
            "Obesity",
            "Pancreatitis",
            base_probability=0.50,
            mechanism="metabolic_dysfunction",
            age_factor=1.0,
            severity_factor=1.1,
        )

        # Systemic inflammation
        cls._add_comorbidity(
            "Inflammatory Bowel Disease (IBD)",
            "Canine Parvovirus",
            base_probability=0.30,
            mechanism="immune_dysregulation",
            age_factor=1.0,
            severity_factor=1.15,
        )

        # Urinary system
        cls._add_comorbidity(
            "Urinary Tract Infection",
            "Bladder Stones",
            base_probability=0.55,
            mechanism="crystal_formation",
            age_factor=1.1,
            severity_factor=0.9,
        )

        # Kidney disease cascade
        cls._add_comorbidity(
            "Kidney Disease (CKD)",
            "Hypertension",
            base_probability=0.60,
            mechanism="secondary_hypertension",
            age_factor=1.15,
            severity_factor=1.0,
        )

        cls._add_comorbidity(
            "Kidney Disease (CKD)",
            "Anemia",
            base_probability=0.50,
            mechanism="chronic_disease_anemia",
            age_factor=1.1,
            severity_factor=0.95,
        )

        # Heart disease
        cls._add_comorbidity(
            "Heart Disease/CHF",
            "Pneumonia",
            base_probability=0.40,
            mechanism="pulmonary_edema",
            age_factor=1.15,
            severity_factor=1.0,
        )

        # Dermatologic cascade
        cls._add_comorbidity(
            "Allergic Dermatitis",
            "Secondary Bacterial Infection",
            base_probability=0.75,
            mechanism="barrier_dysfunction",
            age_factor=1.0,
            severity_factor=1.2,
        )

        # Parasitic infections
        cls._add_comorbidity(
            "Intestinal Parasites",
            "Anemia",
            base_probability=0.40,
            mechanism="blood_loss",
            age_factor=1.1,
            severity_factor=0.9,
        )

    @classmethod
    def _add_comorbidity(
        cls,
        disease_a: str,
        disease_b: str,
        base_probability: float,
        mechanism: str,
        age_factor: float,
        severity_factor: float,
        breed_predispositions: List[str] = None,
    ):
        """Add a comorbidity relationship to the database (bidirectional)."""
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
        cls.COMORBIDITY_DATABASE[(disease_a, disease_b)] = relation
        cls.COMORBIDITY_DATABASE[(disease_b, disease_a)] = relation

    @classmethod
    def get_comorbidity_probability(
        cls,
        disease_a: str,
        disease_b: str,
        age_years: Optional[float] = None,
        severity: str = "moderate",
        breed: Optional[str] = None,
        species: str = "dog",
    ) -> float:
        """
        Get probability that two diseases coexist.

        Args:
            disease_a: First disease name
            disease_b: Second disease name
            age_years: Patient age (for age adjustment)
            severity: Symptom severity ("mild", "moderate", "severe")
            breed: Patient breed
            species: Patient species (default "dog" for backward compatibility)

        Returns:
            Coexistence probability (0-1)
        """
        species_lower = species.lower()

        # Validate species
        if species_lower not in cls.SUPPORTED_SPECIES:
            logger.warning(f"Unknown species: {species}, defaulting to 'dog'")
            species_lower = "dog"

        # Try species-specific relationship first
        relation = cls.SPECIES_COMORBIDITY_DATABASE.get(
            (disease_a, disease_b, species_lower)
        )

        # Fall back to legacy dog database for backward compatibility
        if not relation:
            relation = cls.COMORBIDITY_DATABASE.get((disease_a, disease_b))

        if not relation:
            return 0.0  # Unknown relationship = no assumed coexistence

        probability = relation.base_probability

        # Age adjustment (species-specific thresholds)
        if age_years is not None:
            age_threshold = cls._get_age_threshold(species_lower)
            if age_years > age_threshold:
                probability *= relation.age_factor

        # Severity adjustment
        if severity == "severe":
            probability *= relation.severity_factor
        elif severity == "mild":
            probability *= 0.8

        # Breed adjustment (mostly for dogs, but kept generic for future use)
        if breed and relation.breed_predispositions:
            if breed in relation.breed_predispositions:
                probability *= 1.1

        return min(probability, 1.0)

    @classmethod
    def find_likely_comorbidities(
        cls,
        primary_disease: str,
        age_years: Optional[float] = None,
        severity: str = "moderate",
        breed: Optional[str] = None,
        threshold: float = 0.30,
        species: str = "dog",
    ) -> List[Tuple[str, float, str]]:
        """
        Find diseases that likely coexist with a primary disease.

        Args:
            primary_disease: Index disease to find comorbidities for
            age_years: Patient age
            severity: Symptom severity
            breed: Patient breed
            threshold: Minimum probability to include (default 0.30)
            species: Patient species (default "dog")

        Returns:
            List of (disease_name, probability, mechanism) tuples
        """
        species_lower = species.lower()
        candidates = []
        seen_diseases = set()

        # Check species-specific relationships first
        for (d_a, d_b, sp), relation in cls.SPECIES_COMORBIDITY_DATABASE.items():
            if sp == species_lower and d_a == primary_disease:
                prob = cls.get_comorbidity_probability(
                    d_a, d_b, age_years, severity, breed, species
                )
                if prob >= threshold and d_b not in seen_diseases:
                    candidates.append((d_b, prob, relation.mechanism))
                    seen_diseases.add(d_b)

        # Fall back to legacy database for unmapped relationships
        for (d_a, d_b), relation in cls.COMORBIDITY_DATABASE.items():
            if d_a == primary_disease and d_b not in seen_diseases:
                prob = cls.get_comorbidity_probability(
                    d_a, d_b, age_years, severity, breed, species
                )
                if prob >= threshold:
                    candidates.append((d_b, prob, relation.mechanism))
                    seen_diseases.add(d_b)

        # Sort by probability (descending)
        candidates.sort(key=lambda x: x[1], reverse=True)
        return candidates

    @classmethod
    def _get_age_threshold(cls, species: str) -> float:
        """
        Get the age threshold for senior animals by species.

        Args:
            species: Target species

        Returns:
            Age in years when an animal is considered senior
        """
        # Species-specific senior age thresholds
        thresholds = {
            "dog": 7.0,
            "cat": 7.0,
            "rabbit": 5.0,
            "hamster": 2.0,
            "guinea_pig": 4.0,
            "ferret": 5.0,
            "bird": 10.0,
            "reptile": 10.0,
            "horse": 15.0,
            "hedgehog": 4.0,
        }
        return thresholds.get(species.lower(), 7.0)

    @classmethod
    def get_comorbidity_explanation(cls, disease_a: str, disease_b: str, species: str = "dog") -> str:
        """
        Get plain-text explanation of why two diseases coexist.

        Args:
            disease_a: First disease
            disease_b: Second disease
            species: Patient species (default "dog")

        Returns:
            Explanation string (Japanese friendly)
        """
        species_lower = species.lower()

        # Try species-specific explanation first
        relation = cls.SPECIES_COMORBIDITY_DATABASE.get(
            (disease_a, disease_b, species_lower)
        )

        # Fall back to legacy database
        if not relation:
            relation = cls.COMORBIDITY_DATABASE.get((disease_a, disease_b))
        if not relation:
            return f"{disease_a}と{disease_b}の関連性は不明です。"

        mechanism_descriptions = {
            "secondary_arthritis": "一次疾患により関節に過度なストレスがかかり、続発性関節炎が発生します。",
            "age_related_cascade": "加齢とともに複数の疾患が段階的に発生する傾向があります。",
            "cascade_effect": "初期疾患が他の疾患の発症につながります。",
            "inflammatory_cascade": "炎症反応が複数の器官系に波及します。",
            "immune_suppression": "免疫抑制により二次感染が容易になります。",
            "metabolic_dysfunction": "代謝異常により複数の内分泌疾患が発生します。",
            "joint_stress": "関節への機械的ストレス増加により変性が加速します。",
            "endocrine_dysfunction": "内分泌機能障害により他の代謝疾患が続発します。",
            "airway_inflammation": "気道炎症が複数の呼吸器疾患に関連します。",
            "crystal_formation": "尿路結晶形成により感染リスクが増加します。",
            "secondary_hypertension": "原発疾患により二次性高血圧が発生します。",
            "chronic_disease_anemia": "慢性疾患に伴う貧血が発生します。",
            "pulmonary_edema": "心不全により肺水腫と呼吸器感染が続発します。",
            "barrier_dysfunction": "皮膚バリア破綻により二次感染が容易になります。",
            "blood_loss": "寄生虫感染による失血性貧血が発生します。",
        }

        mechanism_desc = mechanism_descriptions.get(
            relation.mechanism, relation.mechanism
        )
        return f"{disease_a}と{disease_b}は共存することがあります。理由：{mechanism_desc}"


# Initialize database on import
DiseaseInteractionMatrix.initialize()
