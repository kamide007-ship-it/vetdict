"""symptom_interactions.py – Symptom co-occurrence analysis and interaction scoring

Analyzes disease database to identify symptom pairs that frequently co-occur,
enabling confidence boost when both symptoms in a pair are detected.
"""

import logging
from collections import defaultdict
from typing import Any, Dict, List, Tuple

logger = logging.getLogger(__name__)


class SymptomInteractionMatrix:
    """Builds and manages symptom co-occurrence matrix from disease database."""

    def __init__(self, diseases: List[Dict[str, Any]], min_frequency: int = 2):
        """
        Initialize interaction matrix from diseases.

        Args:
            diseases: List of disease dicts with 'symptoms' key (set of symptom IDs)
            min_frequency: Minimum co-occurrence count to include pair
        """
        self.diseases = diseases
        self.min_frequency = min_frequency
        self.pair_frequencies: Dict[frozenset, int] = defaultdict(int)
        self.pair_weights: Dict[frozenset, float] = {}
        self.total_diseases = len(diseases)

        self._build_matrix()

    def _build_matrix(self) -> None:
        """Build symptom pair co-occurrence matrix from disease data."""
        # Count all symptom pairs in each disease
        for disease in self.diseases:
            symptoms = disease.get("symptoms", set())
            if not isinstance(symptoms, set):
                symptoms = set(symptoms)

            # Count all pairs in this disease
            symptom_list = sorted(list(symptoms))
            for i, symptom_a in enumerate(symptom_list):
                for symptom_b in symptom_list[i + 1 :]:
                    pair_key = frozenset({symptom_a, symptom_b})
                    self.pair_frequencies[pair_key] += 1

        # Calculate normalized weights (0.0-1.0)
        for pair, frequency in self.pair_frequencies.items():
            if frequency >= self.min_frequency:
                # Weight = frequency / total_diseases
                # Normalized to encourage pairs that appear together frequently
                weight = min(frequency / max(self.total_diseases, 1), 1.0)
                self.pair_weights[pair] = weight

        logger.info(
            f"Built SymptomInteractionMatrix: "
            f"{len(self.pair_weights)} pairs with frequency >= {self.min_frequency}"
        )

    def get_pair_weight(self, symptom_a: str, symptom_b: str) -> float:
        """
        Get interaction weight for a symptom pair.

        Args:
            symptom_a: First symptom ID
            symptom_b: Second symptom ID

        Returns:
            Weight (0.0-1.0), 0.0 if pair not found
        """
        pair_key = frozenset({symptom_a, symptom_b})
        return self.pair_weights.get(pair_key, 0.0)

    def find_interactions(
        self, symptoms: List[str], weight_threshold: float = 0.1
    ) -> List[Dict[str, Any]]:
        """
        Find all high-weight interactions in a symptom set.

        Args:
            symptoms: List of extracted symptom IDs
            weight_threshold: Minimum weight to include (0.0-1.0)

        Returns:
            List of interactions, sorted by weight descending:
            [{"pair": [str, str], "weight": float, "boost_factor": float}]
        """
        if len(symptoms) < 2:
            return []

        interactions = []
        symptom_set = set(symptoms)

        # Find all pairs in symptom set with sufficient weight
        symptom_list = sorted(list(symptom_set))
        for i, symptom_a in enumerate(symptom_list):
            for symptom_b in symptom_list[i + 1 :]:
                weight = self.get_pair_weight(symptom_a, symptom_b)
                if weight >= weight_threshold:
                    # Boost factor: scale weight to 0-0.15 (conservative boost)
                    boost_factor = weight * 0.15
                    interactions.append(
                        {
                            "pair": [symptom_a, symptom_b],
                            "weight": round(weight, 3),
                            "boost_factor": round(boost_factor, 3),
                        }
                    )

        # Sort by weight descending
        interactions.sort(key=lambda x: x["weight"], reverse=True)
        return interactions

    def get_total_interactions(self) -> int:
        """Get total number of discovered symptom pair interactions."""
        return len(self.pair_weights)

    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about interaction matrix."""
        if not self.pair_frequencies:
            return {
                "total_pairs": 0,
                "diseases_analyzed": self.total_diseases,
                "avg_frequency": 0.0,
                "max_frequency": 0,
            }

        frequencies = list(self.pair_frequencies.values())
        return {
            "total_pairs": len(self.pair_weights),
            "diseases_analyzed": self.total_diseases,
            "avg_frequency": round(sum(frequencies) / len(frequencies), 2),
            "max_frequency": max(frequencies),
        }


class InteractionScorer:
    """Scores symptom combinations based on interaction weights."""

    def __init__(self, interaction_matrix: SymptomInteractionMatrix):
        """
        Initialize scorer with interaction matrix.

        Args:
            interaction_matrix: SymptomInteractionMatrix instance
        """
        self.matrix = interaction_matrix

    def score_symptom_set(
        self,
        symptoms: List[str],
        base_confidence: float = 0.85,
        max_boost: float = 0.15,
    ) -> Tuple[float, List[Dict[str, Any]]]:
        """
        Calculate confidence score for symptom set based on interactions.

        Args:
            symptoms: List of extracted symptom IDs
            base_confidence: Starting confidence (0.0-1.0)
            max_boost: Maximum confidence boost from interactions (default 0.15)

        Returns:
            Tuple of (adjusted_confidence, interactions_found)
        """
        interactions = self.matrix.find_interactions(symptoms)

        if not interactions:
            return base_confidence, []

        # Apply boost from strongest interaction
        # Boost = (strongest interaction weight) * max_boost
        strongest_weight = interactions[0]["weight"]
        boost = strongest_weight * max_boost

        adjusted_confidence = min(base_confidence + boost, 1.0)

        logger.debug(
            f"Interaction scoring: base={base_confidence} "
            f"boost={round(boost, 3)} adjusted={round(adjusted_confidence, 3)} "
            f"interactions={len(interactions)}"
        )

        return adjusted_confidence, interactions


def analyze_symptom_interactions(
    symptoms: List[str],
    diseases: List[Dict[str, Any]],
    min_frequency: int = 2,
    weight_threshold: float = 0.1,
) -> Dict[str, Any]:
    """
    Convenience function to analyze interactions in a symptom set.

    Args:
        symptoms: List of extracted symptom IDs
        diseases: List of disease dicts for building matrix
        min_frequency: Minimum co-occurrence count
        weight_threshold: Minimum interaction weight

    Returns:
        Dict with interaction analysis:
        {
            "interactions": [...],
            "strongest_pair": (str, str) or None,
            "interaction_count": int,
            "boost_potential": float
        }
    """
    matrix = SymptomInteractionMatrix(diseases, min_frequency=min_frequency)
    interactions = matrix.find_interactions(symptoms, weight_threshold=weight_threshold)

    strongest_pair = None
    boost_potential = 0.0

    if interactions:
        strongest = interactions[0]
        strongest_pair = tuple(strongest["pair"])
        boost_potential = strongest["boost_factor"]

    return {
        "interactions": interactions,
        "strongest_pair": strongest_pair,
        "interaction_count": len(interactions),
        "boost_potential": round(boost_potential, 3),
    }


class TripleInteractionMatrix:
    """Analyzes and scores triple (3-symptom) co-occurrences."""

    def __init__(self, diseases: List[Dict[str, Any]], min_frequency: int = 1):
        """
        Initialize triple interaction matrix.

        Args:
            diseases: List of disease dicts with 'symptoms' key
            min_frequency: Minimum co-occurrence count to include triplet
        """
        self.diseases = diseases
        self.min_frequency = min_frequency
        self.triple_frequencies: Dict[frozenset, int] = defaultdict(int)
        self.triple_weights: Dict[frozenset, float] = {}
        self.total_diseases = len(diseases)

        self._build_matrix()

    def _build_matrix(self) -> None:
        """Build symptom triple co-occurrence matrix from disease data."""
        # Count all symptom triples in each disease
        for disease in self.diseases:
            symptoms = disease.get("symptoms", set())
            if not isinstance(symptoms, set):
                symptoms = set(symptoms)

            if len(symptoms) < 3:
                continue

            # Count all triples in this disease
            symptom_list = sorted(list(symptoms))
            for i, symptom_a in enumerate(symptom_list):
                for j, symptom_b in enumerate(symptom_list[i + 1 :], i + 1):
                    for symptom_c in symptom_list[j + 1 :]:
                        triple_key = frozenset({symptom_a, symptom_b, symptom_c})
                        self.triple_frequencies[triple_key] += 1

        # Calculate normalized weights
        for triple, frequency in self.triple_frequencies.items():
            if frequency >= self.min_frequency:
                weight = min(frequency / max(self.total_diseases, 1), 1.0)
                self.triple_weights[triple] = weight

        logger.info(
            f"Built TripleInteractionMatrix: "
            f"{len(self.triple_weights)} triples with frequency >= {self.min_frequency}"
        )

    def find_triple_interactions(
        self, symptoms: List[str], weight_threshold: float = 0.05
    ) -> List[Dict[str, Any]]:
        """
        Find all high-weight triple interactions in a symptom set.

        Args:
            symptoms: List of extracted symptom IDs
            weight_threshold: Minimum weight to include

        Returns:
            List of triple interactions sorted by weight descending
        """
        if len(symptoms) < 3:
            return []

        interactions = []
        symptom_set = set(symptoms)

        # Find all triples in symptom set with sufficient weight
        symptom_list = sorted(list(symptom_set))
        for i, symptom_a in enumerate(symptom_list):
            for j, symptom_b in enumerate(symptom_list[i + 1 :], i + 1):
                for symptom_c in symptom_list[j + 1 :]:
                    triple_key = frozenset({symptom_a, symptom_b, symptom_c})
                    weight = self.triple_weights.get(triple_key, 0.0)
                    if weight >= weight_threshold:
                        boost_factor = weight * 0.20  # Conservative boost for triples
                        interactions.append(
                            {
                                "triple": sorted([symptom_a, symptom_b, symptom_c]),
                                "weight": round(weight, 3),
                                "boost_factor": round(boost_factor, 3),
                            }
                        )

        # Sort by weight descending
        interactions.sort(key=lambda x: x["weight"], reverse=True)
        return interactions

    def get_total_triples(self) -> int:
        """Get total number of discovered symptom triple interactions."""
        return len(self.triple_weights)
