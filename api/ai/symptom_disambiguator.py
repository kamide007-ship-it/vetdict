"""Stage 3: Symptom disambiguation engine for multi-species diagnosis.

Enables species-aware symptom resolution, normalization, and disambiguation
for accurate cross-species diagnostic support.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set, Tuple
import logging

logger = logging.getLogger(__name__)

from api.data.symptom_species_mapping import (
    SYMPTOM_SPECIES_ALIASES,
    SYMPTOM_SEVERITY_THRESHOLDS,
    SPECIES_SYMPTOM_COMPATIBILITY,
    SYMPTOM_EXCLUSIONS,
    SYMPTOM_PROMINENCE,
    normalize_symptom_for_species,
    get_symptom_severity_threshold,
    is_symptom_valid_for_species,
    get_symptom_prominence,
    get_compatible_symptoms,
)


@dataclass
class DisambiguatedSymptom:
    """Result of symptom disambiguation for a specific species."""

    original_symptom: str
    species: str
    normalized_symptom: str
    is_valid: bool
    severity_threshold: float
    prominence_multiplier: float
    confidence: float  # 0-1, how confident we are in this disambiguation
    explanation: str
    compatible_aliases: List[str]


class SymptomDisambiguationEngine:
    """Resolves symptom names and manifestations across all species."""

    def __init__(self):
        """Initialize the symptom disambiguation engine."""
        self.symptom_aliases = SYMPTOM_SPECIES_ALIASES
        self.severity_thresholds = SYMPTOM_SEVERITY_THRESHOLDS
        self.compatibility_matrix = SPECIES_SYMPTOM_COMPATIBILITY
        self.exclusions = SYMPTOM_EXCLUSIONS

    def disambiguate_symptom(
        self,
        symptom_id: str,
        species: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> DisambiguatedSymptom:
        """
        Disambiguate a symptom for a specific species.

        Resolves symptom name variations, validates species compatibility,
        and provides context-aware normalization.

        Args:
            symptom_id: Symptom identifier/name
            species: Target species
            context: Optional context dict with severity, age, etc.

        Returns:
            DisambiguatedSymptom with normalized info for the species
        """
        species_lower = species.lower().strip()

        # Check if symptom is valid for this species
        is_valid = is_symptom_valid_for_species(symptom_id, species)

        # Normalize symptom name
        normalized = normalize_symptom_for_species(symptom_id, species)

        # Get severity threshold
        severity = "moderate"
        if context:
            severity = context.get("severity", "moderate")

        severity_threshold = get_symptom_severity_threshold(
            symptom_id, species, severity
        )

        # Get prominence multiplier
        prominence = get_symptom_prominence(symptom_id, species)

        # Get compatible aliases
        compatible_aliases = self._get_compatible_aliases(symptom_id, species)

        # Calculate confidence
        confidence = self._calculate_disambiguation_confidence(
            symptom_id, species, is_valid, context
        )

        # Generate explanation
        explanation = self._generate_explanation(
            symptom_id, species, normalized, is_valid
        )

        return DisambiguatedSymptom(
            original_symptom=symptom_id,
            species=species,
            normalized_symptom=normalized,
            is_valid=is_valid,
            severity_threshold=severity_threshold,
            prominence_multiplier=prominence,
            confidence=confidence,
            explanation=explanation,
            compatible_aliases=compatible_aliases,
        )

    def disambiguate_symptoms(
        self,
        symptom_ids: List[str],
        species: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> List[DisambiguatedSymptom]:
        """
        Disambiguate multiple symptoms for a species.

        Args:
            symptom_ids: List of symptom identifiers
            species: Target species
            context: Optional context dict

        Returns:
            List of DisambiguatedSymptom objects
        """
        return [
            self.disambiguate_symptom(symptom_id, species, context)
            for symptom_id in symptom_ids
        ]

    def get_symptom_severity_threshold(
        self, symptom: str, species: str, severity_level: str = "moderate"
    ) -> float:
        """
        Get severity threshold for a symptom in a specific species.

        Args:
            symptom: Symptom name
            species: Target species
            severity_level: "mild", "moderate", or "severe"

        Returns:
            Severity threshold (0-1)
        """
        return get_symptom_severity_threshold(symptom, species, severity_level)

    def normalize_symptom_names(
        self,
        symptoms: List[str],
        species: str,
    ) -> Dict[str, str]:
        """
        Normalize a list of symptom names for a species.

        Args:
            symptoms: List of symptom names
            species: Target species

        Returns:
            Dict mapping original → normalized symptom names
        """
        mapping = {}
        for symptom in symptoms:
            normalized = normalize_symptom_for_species(symptom, species)
            mapping[symptom] = normalized
        return mapping

    def find_symptom_aliases(
        self,
        symptom: str,
        species: Optional[str] = None,
    ) -> Dict[str, List[str]]:
        """
        Find all known aliases for a symptom.

        Args:
            symptom: Symptom name
            species: Optional specific species to filter by

        Returns:
            Dict of species → aliases for the symptom
        """
        if symptom not in self.symptom_aliases:
            return {}

        if species:
            species_lower = species.lower()
            aliases = self.symptom_aliases[symptom].get(species_lower, [])
            return {species: aliases} if aliases else {}

        return self.symptom_aliases[symptom]

    def get_symptom_compatibility(
        self, symptom: str, species: str
    ) -> float:
        """
        Get compatibility score for a symptom in a species (0-1).

        Args:
            symptom: Symptom name
            species: Target species

        Returns:
            Compatibility score (1.0 = fully compatible, 0.0 = not compatible)
        """
        species_lower = species.lower()

        if symptom in self.exclusions.get(species_lower, []):
            return 0.0

        if symptom not in self.compatibility_matrix:
            return 1.0  # Unknown symptoms default to compatible

        return self.compatibility_matrix[symptom].get(species_lower, 0.5)

    def validate_symptom_set(
        self,
        symptoms: List[str],
        species: str,
    ) -> Tuple[bool, List[str], List[str]]:
        """
        Validate a set of symptoms for a species.

        Args:
            symptoms: List of symptom names
            species: Target species

        Returns:
            (is_valid, valid_symptoms, invalid_symptoms) tuple
        """
        valid_symptoms = []
        invalid_symptoms = []

        for symptom in symptoms:
            if is_symptom_valid_for_species(symptom, species):
                valid_symptoms.append(symptom)
            else:
                invalid_symptoms.append(symptom)

        is_valid = len(invalid_symptoms) == 0

        return is_valid, valid_symptoms, invalid_symptoms

    def resolve_symptom_ambiguity(
        self,
        ambiguous_symptom: str,
        species: str,
        candidates: Optional[List[str]] = None,
    ) -> Tuple[str, float, str]:
        """
        Resolve ambiguity when a symptom name could refer to multiple concepts.

        Args:
            ambiguous_symptom: Potentially ambiguous symptom name
            species: Target species
            candidates: Optional list of candidate symptom names to choose from

        Returns:
            (resolved_symptom, confidence, reasoning) tuple
        """
        species_lower = species.lower()

        # Check if it's a known primary symptom
        if ambiguous_symptom in self.symptom_aliases:
            normalized = normalize_symptom_for_species(ambiguous_symptom, species)
            return normalized, 0.95, "Direct mapping found"

        # If candidates provided, find best match
        if candidates:
            best_match = None
            best_score = 0.0

            for candidate in candidates:
                similarity = self._calculate_symptom_similarity(
                    ambiguous_symptom, candidate, species
                )
                if similarity > best_score:
                    best_score = similarity
                    best_match = candidate

            if best_match:
                normalized = normalize_symptom_for_species(best_match, species)
                return normalized, best_score, f"Matched to {best_match}"

        # Fallback: return original with low confidence
        return ambiguous_symptom, 0.3, "No clear match found"

    def _get_compatible_aliases(
        self, symptom: str, species: str
    ) -> List[str]:
        """Get list of compatible aliases for a symptom in a species."""
        species_lower = species.lower()

        if symptom not in self.symptom_aliases:
            return []

        species_aliases = self.symptom_aliases[symptom].get(species_lower, [])
        return species_aliases

    def _calculate_disambiguation_confidence(
        self,
        symptom: str,
        species: str,
        is_valid: bool,
        context: Optional[Dict[str, Any]] = None,
    ) -> float:
        """
        Calculate confidence in symptom disambiguation for a species.

        Args:
            symptom: Symptom name
            species: Target species
            is_valid: Whether symptom is valid for species
            context: Optional context

        Returns:
            Confidence score (0-1)
        """
        base_confidence = 0.8 if is_valid else 0.2

        # Adjust based on compatibility
        compatibility = self.get_symptom_compatibility(symptom, species)
        base_confidence *= compatibility

        # Adjust based on how well-mapped the symptom is
        aliases = self._get_compatible_aliases(symptom, species)
        if aliases:
            base_confidence *= (1.0 + 0.1 * len(aliases))

        return min(base_confidence, 1.0)

    def _generate_explanation(
        self,
        original: str,
        species: str,
        normalized: str,
        is_valid: bool,
    ) -> str:
        """Generate plain-text explanation of disambiguation."""
        if not is_valid:
            return (
                f"'{original}' is not a valid symptom for {species}. "
                f"Interpreted as '{normalized}' with reduced confidence."
            )

        if original == normalized:
            return f"'{original}' is directly applicable to {species}."

        return f"'{original}' → '{normalized}' for {species}."

    @staticmethod
    def _calculate_symptom_similarity(
        symptom_a: str,
        symptom_b: str,
        species: str,
    ) -> float:
        """
        Calculate similarity between two symptom names.

        Simple string similarity metric used for disambiguation.

        Args:
            symptom_a: First symptom
            symptom_b: Second symptom
            species: Target species

        Returns:
            Similarity score (0-1)
        """
        # Normalize strings
        a_lower = symptom_a.lower().strip()
        b_lower = symptom_b.lower().strip()

        # Exact match
        if a_lower == b_lower:
            return 1.0

        # Substring match
        if a_lower in b_lower or b_lower in a_lower:
            return 0.8

        # Levenshtein-like distance (simplified)
        a_words = set(a_lower.split("_"))
        b_words = set(b_lower.split("_"))

        if not a_words or not b_words:
            return 0.0

        overlap = len(a_words & b_words)
        total = len(a_words | b_words)

        return overlap / total if total > 0 else 0.0

    def get_species_symptom_profile(self, species: str) -> Dict[str, Any]:
        """
        Get comprehensive symptom profile for a species.

        Args:
            species: Target species

        Returns:
            Dict with symptom capabilities and characteristics for the species
        """
        species_lower = species.lower()
        compatible_symptoms = get_compatible_symptoms(species)

        return {
            "species": species,
            "compatible_symptom_count": len(compatible_symptoms),
            "compatible_symptoms": sorted(list(compatible_symptoms)),
            "excluded_symptoms": self.exclusions.get(species_lower, []),
            "total_mapped_symptoms": len(self.symptom_aliases),
        }


# Module-level convenience functions
_engine: Optional[SymptomDisambiguationEngine] = None


def get_engine() -> SymptomDisambiguationEngine:
    """Get or create the symptom disambiguation engine."""
    global _engine
    if _engine is None:
        _engine = SymptomDisambiguationEngine()
    return _engine


def disambiguate_symptom(
    symptom_id: str,
    species: str,
    context: Optional[Dict[str, Any]] = None,
) -> DisambiguatedSymptom:
    """
    Disambiguate a symptom for a species (convenience function).

    Args:
        symptom_id: Symptom identifier/name
        species: Target species
        context: Optional context dict

    Returns:
        DisambiguatedSymptom
    """
    return get_engine().disambiguate_symptom(symptom_id, species, context)


def validate_symptoms_for_species(
    symptoms: List[str],
    species: str,
) -> Tuple[List[str], List[str]]:
    """
    Validate symptoms for a species (convenience function).

    Args:
        symptoms: List of symptom names
        species: Target species

    Returns:
        (valid_symptoms, invalid_symptoms) tuple
    """
    is_valid, valid, invalid = get_engine().validate_symptom_set(symptoms, species)
    return valid, invalid
