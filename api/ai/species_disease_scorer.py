"""Stage 4: Multi-disease scoring with species-specific adjustments.

Calculates disease confidence scores with species-aware thresholds,
prevalence adjustments, and multi-disease interaction effects.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

from api.ai.species_comorbidities import load_species_comorbidities


@dataclass
class SpeciesAdjustmentFactors:
    """Species-specific adjustment factors for disease scoring."""

    species: str
    min_confidence_threshold: float  # Minimum confidence to consider disease
    prevalence_adjustment: float  # General prevalence in species
    symptom_weight_multiplier: float  # How heavily to weight symptoms
    age_factor: float  # Adjustment based on patient age
    severity_factor: float  # Adjustment based on symptom severity
    explanation: str


class SpeciesDiseaseScorer:
    """Scores diseases with species-specific adjustments."""

    # Species-specific confidence thresholds and adjustment factors
    SPECIES_SCORING_PROFILES: Dict[str, Dict[str, Any]] = {
        "dog": {
            "min_confidence_threshold": 0.25,
            "prevalence_adjustment": 1.0,  # Baseline
            "symptom_weight_multiplier": 1.0,
            "senior_age_threshold": 7.0,
        },
        "cat": {
            "min_confidence_threshold": 0.30,
            "prevalence_adjustment": 1.0,
            "symptom_weight_multiplier": 0.95,
            "senior_age_threshold": 7.0,
        },
        "rabbit": {
            "min_confidence_threshold": 0.35,
            "prevalence_adjustment": 0.8,  # Fewer exotic disease cases
            "symptom_weight_multiplier": 0.90,
            "senior_age_threshold": 5.0,
        },
        "hamster": {
            "min_confidence_threshold": 0.40,
            "prevalence_adjustment": 0.7,
            "symptom_weight_multiplier": 0.85,
            "senior_age_threshold": 2.0,
        },
        "guinea_pig": {
            "min_confidence_threshold": 0.35,
            "prevalence_adjustment": 0.8,
            "symptom_weight_multiplier": 0.90,
            "senior_age_threshold": 4.0,
        },
        "ferret": {
            "min_confidence_threshold": 0.30,
            "prevalence_adjustment": 0.85,
            "symptom_weight_multiplier": 0.92,
            "senior_age_threshold": 5.0,
        },
        "bird": {
            "min_confidence_threshold": 0.35,
            "prevalence_adjustment": 0.75,
            "symptom_weight_multiplier": 0.88,
            "senior_age_threshold": 10.0,
        },
        "reptile": {
            "min_confidence_threshold": 0.40,
            "prevalence_adjustment": 0.70,
            "symptom_weight_multiplier": 0.85,
            "senior_age_threshold": 10.0,
        },
        "horse": {
            "min_confidence_threshold": 0.25,
            "prevalence_adjustment": 1.0,
            "symptom_weight_multiplier": 1.0,
            "senior_age_threshold": 15.0,
        },
        "hedgehog": {
            "min_confidence_threshold": 0.35,
            "prevalence_adjustment": 0.75,
            "symptom_weight_multiplier": 0.90,
            "senior_age_threshold": 4.0,
        },
    }

    @classmethod
    def score_diseases_for_species(
        cls,
        diseases: List[Dict[str, Any]],
        symptoms: List[str],
        species: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Score diseases with species-specific adjustments.

        Args:
            diseases: List of disease dicts with 'name' and 'confidence'
            symptoms: List of detected symptom IDs
            species: Target species
            context: Optional context (age, severity, breed, etc.)

        Returns:
            List of diseases with species-adjusted scores
        """
        species_lower = species.lower()

        # Get species profile
        profile = cls.SPECIES_SCORING_PROFILES.get(
            species_lower,
            cls.SPECIES_SCORING_PROFILES["dog"]  # Fallback to dog
        )

        # Filter and adjust diseases
        adjusted_diseases = []

        for disease in diseases:
            if not isinstance(disease, dict):
                continue

            disease_name = disease.get("name")
            base_confidence = disease.get("confidence", disease.get("match_percent", 0))

            # Normalize confidence to 0-1
            if base_confidence > 1.0:
                base_confidence /= 100.0

            # Apply species adjustments
            adjusted_conf, factors = cls.calculate_species_adjusted_confidence(
                base_confidence,
                species,
                context or {},
                disease_name,
            )

            # Only include if meets species threshold
            if adjusted_conf >= profile["min_confidence_threshold"]:
                adjusted_disease = disease.copy()
                adjusted_disease["confidence"] = adjusted_conf
                adjusted_disease["match_percent"] = int(adjusted_conf * 100)
                adjusted_disease["species_adjustment"] = {
                    "original_confidence": base_confidence,
                    "adjusted_confidence": adjusted_conf,
                    "adjustment_factor": adjusted_conf / max(base_confidence, 0.01),
                    "adjustment_details": {
                        "prevalence_adjustment": factors.prevalence_adjustment,
                        "age_factor": factors.age_factor,
                        "severity_factor": factors.severity_factor,
                    },
                    "explanation": factors.explanation,
                }
                adjusted_diseases.append(adjusted_disease)

        # Sort by adjusted confidence
        adjusted_diseases.sort(
            key=lambda x: x.get("confidence", 0),
            reverse=True
        )

        return adjusted_diseases

    @classmethod
    def calculate_species_adjusted_confidence(
        cls,
        base_confidence: float,
        species: str,
        context: Dict[str, Any],
        disease_name: Optional[str] = None,
    ) -> Tuple[float, SpeciesAdjustmentFactors]:
        """
        Calculate species-adjusted confidence for a disease.

        Args:
            base_confidence: Original disease confidence (0-1)
            species: Target species
            context: Patient context (age, severity, breed, etc.)
            disease_name: Optional disease name for logging

        Returns:
            (adjusted_confidence, adjustment_factors) tuple
        """
        species_lower = species.lower()

        # Get species profile
        profile = cls.SPECIES_SCORING_PROFILES.get(
            species_lower,
            cls.SPECIES_SCORING_PROFILES["dog"]
        )

        # Extract context
        age_years = context.get("age_years")
        severity = context.get("severity", "moderate")
        breed = context.get("breed")

        # Start with base confidence
        adjusted_conf = base_confidence

        # Apply prevalence adjustment
        prevalence_adj = profile.get("prevalence_adjustment", 1.0)
        adjusted_conf *= prevalence_adj

        # Apply symptom weight multiplier
        symptom_weight = profile.get("symptom_weight_multiplier", 1.0)
        adjusted_conf *= symptom_weight

        # Age factor adjustment
        age_factor = cls._calculate_age_factor(
            age_years,
            species,
            profile.get("senior_age_threshold", 7.0)
        )
        adjusted_conf *= age_factor

        # Severity factor adjustment
        severity_factor = cls._calculate_severity_factor(severity)
        adjusted_conf *= severity_factor

        # Clamp to valid range
        adjusted_conf = max(0.0, min(adjusted_conf, 1.0))

        # Generate explanation
        explanation = cls._generate_adjustment_explanation(
            species, age_years, severity, prevalence_adj, age_factor, severity_factor
        )

        return adjusted_conf, SpeciesAdjustmentFactors(
            species=species,
            min_confidence_threshold=profile.get("min_confidence_threshold", 0.25),
            prevalence_adjustment=prevalence_adj,
            symptom_weight_multiplier=symptom_weight,
            age_factor=age_factor,
            severity_factor=severity_factor,
            explanation=explanation,
        )

    @staticmethod
    def _calculate_age_factor(
        age_years: Optional[float],
        species: str,
        senior_threshold: float,
    ) -> float:
        """Calculate age-based adjustment factor."""
        if age_years is None:
            return 1.0

        species_lower = species.lower()

        # Senior animals have higher disease likelihood overall
        if age_years > senior_threshold:
            # Increasingly higher factor for older animals
            years_over_threshold = age_years - senior_threshold
            return 1.0 + (years_over_threshold * 0.05)  # 5% per year over threshold

        # Young animals have lower disease likelihood for age-related conditions
        if age_years < 1.0:
            return 0.85

        # Prime adult years
        return 1.0

    @staticmethod
    def _calculate_severity_factor(severity: str) -> float:
        """Calculate severity-based adjustment factor."""
        severity_lower = severity.lower()

        if severity_lower == "severe":
            return 1.2  # Severe symptoms increase confidence in disease
        elif severity_lower == "mild":
            return 0.85  # Mild symptoms decrease confidence
        else:  # moderate
            return 1.0

    @staticmethod
    def _generate_adjustment_explanation(
        species: str,
        age_years: Optional[float],
        severity: str,
        prevalence_adj: float,
        age_factor: float,
        severity_factor: float,
    ) -> str:
        """Generate explanation of adjustment factors."""
        factors = []

        if abs(prevalence_adj - 1.0) > 0.05:
            if prevalence_adj < 1.0:
                factors.append(f"Lower prevalence in {species} ({prevalence_adj:.1%})")
            else:
                factors.append(f"Higher prevalence in {species} ({prevalence_adj:.1%})")

        if age_years:
            if age_factor > 1.0:
                factors.append(f"Senior age factor (+{(age_factor - 1.0) * 100:.0f}%)")
            elif age_factor < 1.0:
                factors.append(f"Young age factor ({(age_factor - 1.0) * 100:.0f}%)")

        if abs(severity_factor - 1.0) > 0.05:
            if severity_factor > 1.0:
                factors.append(f"Severe symptoms (+{(severity_factor - 1.0) * 100:.0f}%)")
            else:
                factors.append(f"Mild symptoms ({(severity_factor - 1.0) * 100:.0f}%)")

        if not factors:
            return "Species-standard scoring applied"

        return ", ".join(factors)

    @classmethod
    def filter_diseases_by_species(
        cls,
        diseases: List[Dict[str, Any]],
        species: str,
        min_confidence: Optional[float] = None,
    ) -> List[Dict[str, Any]]:
        """
        Filter disease list to those appropriate for species.

        Args:
            diseases: List of disease dicts
            species: Target species
            min_confidence: Optional minimum confidence threshold

        Returns:
            Filtered disease list
        """
        species_lower = species.lower()

        profile = cls.SPECIES_SCORING_PROFILES.get(
            species_lower,
            cls.SPECIES_SCORING_PROFILES["dog"]
        )

        threshold = min_confidence or profile.get("min_confidence_threshold", 0.25)

        filtered = []
        for disease in diseases:
            if not isinstance(disease, dict):
                continue

            confidence = disease.get("confidence", disease.get("match_percent", 0))
            if confidence > 1.0:
                confidence /= 100.0

            if confidence >= threshold:
                filtered.append(disease)

        return filtered

    @classmethod
    def get_species_profile(cls, species: str) -> Dict[str, Any]:
        """
        Get scoring profile for a species.

        Args:
            species: Target species

        Returns:
            Species profile dict
        """
        species_lower = species.lower()
        return cls.SPECIES_SCORING_PROFILES.get(
            species_lower,
            cls.SPECIES_SCORING_PROFILES.get("dog", {})
        )

    @classmethod
    def apply_comorbidity_adjustments(
        cls,
        diseases: List[Dict[str, Any]],
        species: str,
    ) -> List[Dict[str, Any]]:
        """
        Apply comorbidity-based adjustments to disease scores.

        Args:
            diseases: List of disease dicts with confidence scores
            species: Target species

        Returns:
            Diseases with comorbidity adjustments applied
        """
        # Load species comorbidity database
        try:
            comorbidity_db = load_species_comorbidities(species)
        except (ValueError, ImportError):
            logger.warning(f"Could not load comorbidities for {species}")
            return diseases

        if not comorbidity_db:
            return diseases

        # Find disease pairs in the list
        adjusted = []

        for disease in diseases:
            if not isinstance(disease, dict):
                adjusted.append(disease)
                continue

            disease_dict = disease.copy()
            disease_name = disease_dict.get("name")

            # Check if this disease has known comorbidities with other diseases
            comorbidity_boost = 1.0

            for other_disease in diseases:
                if not isinstance(other_disease, dict):
                    continue

                other_name = other_disease.get("name")
                if disease_name == other_name:
                    continue

                # Check if these diseases commonly coexist
                relation = comorbidity_db.get((disease_name, other_name))
                if relation:
                    # Boost confidence if other disease is also present
                    other_conf = other_disease.get("confidence", 0)
                    if other_conf > 0.3:
                        # Up to 10% boost for known comorbidities
                        comorbidity_boost = max(comorbidity_boost, 1.05)

            # Apply comorbidity boost
            if comorbidity_boost > 1.0:
                original_conf = disease_dict.get("confidence", 0)
                disease_dict["confidence"] = min(original_conf * comorbidity_boost, 1.0)
                disease_dict["match_percent"] = int(disease_dict["confidence"] * 100)

                if "species_adjustment" not in disease_dict:
                    disease_dict["species_adjustment"] = {}

                disease_dict["species_adjustment"]["comorbidity_boost"] = comorbidity_boost

            adjusted.append(disease_dict)

        return adjusted
