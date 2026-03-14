"""Multi-disease combination expander using hierarchical clustering and association rules.

Extends 2-disease interactions to 3+ disease combinations with complex interaction modeling.
Implements hierarchical clustering, association rule mining, and temporal progression patterns.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple
from itertools import combinations
import logging
from enum import Enum
import math

logger = logging.getLogger(__name__)


class InteractionType(Enum):
    """Types of disease interactions."""
    CAUSAL = "causal"  # Disease A causes Disease B
    CASCADE = "cascade"  # Disease A → Disease B → Disease C
    SYNERGISTIC = "synergistic"  # Diseases enhance each other's severity
    ANTAGONISTIC = "antagonistic"  # Diseases inhibit each other
    INDEPENDENT = "independent"  # No significant interaction
    SHARED_PATHWAY = "shared_pathway"  # Common biological pathway
    SECONDARY = "secondary"  # Disease B is complication of Disease A


@dataclass
class DiseaseInteraction:
    """Represents interaction between two diseases."""
    disease_a: str
    disease_b: str
    interaction_type: InteractionType
    base_probability: float  # 0-1, coexistence probability
    mechanism: str  # Description of interaction mechanism
    age_factor: float  # Age multiplier (>1.0 for seniors)
    severity_factor: float  # Severity multiplier
    breed_predispositions: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "disease_a": self.disease_a,
            "disease_b": self.disease_b,
            "interaction_type": self.interaction_type.value,
            "base_probability": round(self.base_probability, 3),
            "mechanism": self.mechanism,
            "age_factor": round(self.age_factor, 3),
            "severity_factor": round(self.severity_factor, 3),
            "breed_predispositions": self.breed_predispositions,
        }


@dataclass
class CombinationPattern:
    """Pattern of 3+ diseases that commonly coexist."""
    diseases: Tuple[str, ...]  # Sorted tuple of disease names
    interaction_types: Dict[Tuple[str, str], InteractionType]
    combined_probability: float  # Probability all 3+ coexist
    cascade_order: Optional[List[str]]  # Temporal order if cascade (optional)
    complexity_score: float  # 0-100, overall complexity
    mechanism_description: str
    clinical_significance: str
    supporting_cases: int = 0  # Number of clinical cases supporting this pattern

    def to_dict(self) -> Dict:
        return {
            "diseases": list(self.diseases),
            "combined_probability": round(self.combined_probability, 3),
            "cascade_order": self.cascade_order,
            "complexity_score": round(self.complexity_score, 2),
            "mechanism_description": self.mechanism_description,
            "clinical_significance": self.clinical_significance,
            "supporting_cases": self.supporting_cases,
            "interaction_types": {
                f"{d1}-{d2}": itype.value
                for (d1, d2), itype in self.interaction_types.items()
            }
        }


class MultiDiseaseExpander:
    """Expands disease combinations from 2-disease to 3+ diseases.

    Uses hierarchical clustering and association rules to identify and score
    complex multi-disease patterns with biological interactions.
    """

    def __init__(self, interaction_matrix: Dict[Tuple[str, str], DiseaseInteraction]):
        """Initialize expander with 2-disease interaction matrix.

        Args:
            interaction_matrix: Dict mapping (disease_a, disease_b) to DiseaseInteraction
        """
        self.interaction_matrix = interaction_matrix
        self.combination_patterns: Dict[Tuple[str, ...], CombinationPattern] = {}
        self.disease_clusters: Dict[str, Set[str]] = {}
        self._build_disease_clusters()

    def _build_disease_clusters(self):
        """Build disease clusters using hierarchical clustering."""
        # Group diseases by interaction strength
        all_diseases = set()
        disease_graph = {}

        # Build adjacency information
        for (d1, d2), interaction in self.interaction_matrix.items():
            all_diseases.add(d1)
            all_diseases.add(d2)

            if d1 not in disease_graph:
                disease_graph[d1] = []
            if d2 not in disease_graph:
                disease_graph[d2] = []

            disease_graph[d1].append((d2, interaction.base_probability))
            disease_graph[d2].append((d1, interaction.base_probability))

        # Perform clustering by connectivity (simple greedy approach)
        clustered = set()
        cluster_id = 0

        for disease in all_diseases:
            if disease in clustered:
                continue

            cluster = set()
            queue = [disease]

            while queue:
                current = queue.pop(0)
                if current in clustered:
                    continue

                cluster.add(current)
                clustered.add(current)

                # Add strongly connected neighbors
                if current in disease_graph:
                    for neighbor, prob in disease_graph[current]:
                        if neighbor not in clustered and prob >= 0.4:
                            queue.append(neighbor)

            self.disease_clusters[f"cluster_{cluster_id}"] = cluster
            cluster_id += 1

    def expand_combinations(self, diseases: List[str],
                           min_combined_prob: float = 0.15) -> List[CombinationPattern]:
        """Expand 2-disease pair to 3+ combinations.

        Args:
            diseases: List of 2+ diseases to combine
            min_combined_prob: Minimum combined probability threshold

        Returns:
            List of CombinationPattern objects for valid combinations
        """
        if len(diseases) < 2:
            return []

        patterns = []

        # Generate 3-disease combinations
        for combo in combinations(diseases, 3):
            pattern = self._score_combination(combo)
            if pattern and pattern.combined_probability >= min_combined_prob:
                patterns.append(pattern)
                self.combination_patterns[combo] = pattern

        # Generate 4-disease combinations if we have enough diseases
        if len(diseases) >= 4:
            for combo in combinations(diseases, 4):
                pattern = self._score_combination(combo)
                if pattern and pattern.combined_probability >= min_combined_prob * 0.8:
                    patterns.append(pattern)
                    self.combination_patterns[combo] = pattern

        # Sort by combined probability (descending)
        patterns.sort(key=lambda p: p.combined_probability, reverse=True)
        return patterns

    def _score_combination(self, diseases: Tuple[str, ...]) -> Optional[CombinationPattern]:
        """Score a specific disease combination.

        Args:
            diseases: Tuple of 2+ disease names

        Returns:
            CombinationPattern if valid, None otherwise
        """
        # Ensure sorted for consistent key
        diseases = tuple(sorted(diseases))

        if diseases in self.combination_patterns:
            return self.combination_patterns[diseases]

        # Get all pairwise interactions
        interactions = {}
        pairwise_probs = []
        valid_pairs = 0

        for d1, d2 in combinations(diseases, 2):
            key = tuple(sorted([d1, d2]))

            if key in self.interaction_matrix:
                interaction = self.interaction_matrix[key]
                interactions[key] = interaction.interaction_type
                pairwise_probs.append(interaction.base_probability)
                valid_pairs += 1

        # Need at least some interactions to be valid
        if valid_pairs == 0:
            return None

        # Calculate combined probability (multiplicative with dampening)
        # P(A AND B AND C) ≈ P(A) * P(B|A) * P(C|A,B)
        mean_pairwise = sum(pairwise_probs) / len(pairwise_probs) if pairwise_probs else 0

        # Dampening factor: more diseases = lower combined probability
        dampening = 1.0 / (1.0 + (len(diseases) - 2) * 0.3)
        combined_prob = mean_pairwise * dampening

        # Calculate complexity score
        complexity = self._calculate_complexity(diseases, interactions, combined_prob)

        # Determine cascade order if applicable
        cascade_order = self._determine_cascade_order(diseases, interactions)

        # Generate mechanism description
        mechanism = self._generate_mechanism_description(diseases, interactions)

        pattern = CombinationPattern(
            diseases=diseases,
            interaction_types=interactions,
            combined_probability=max(0, min(1, combined_prob)),
            cascade_order=cascade_order,
            complexity_score=complexity,
            mechanism_description=mechanism,
            clinical_significance=self._assess_clinical_significance(
                diseases, combined_prob, complexity
            )
        )

        return pattern

    def _calculate_complexity(self,
                             diseases: Tuple[str, ...],
                             interactions: Dict[Tuple[str, str], InteractionType],
                             combined_prob: float) -> float:
        """Calculate overall complexity score for disease combination.

        Complexity = f(
            number_of_diseases,
            interaction_strength,
            cascade_depth,
            pathway_overlap
        )
        """
        base_complexity = len(diseases) * 15  # 15 points per disease

        # Add interaction complexity
        interaction_points = 0
        for interaction_type in interactions.values():
            if interaction_type == InteractionType.CASCADE:
                interaction_points += 20
            elif interaction_type == InteractionType.SYNERGISTIC:
                interaction_points += 15
            elif interaction_type == InteractionType.SHARED_PATHWAY:
                interaction_points += 12
            elif interaction_type == InteractionType.SECONDARY:
                interaction_points += 10
            else:
                interaction_points += 5

        # Normalize by number of interactions
        num_interactions = len(interactions)
        if num_interactions > 0:
            interaction_points /= num_interactions
            interaction_points *= (num_interactions * 5)  # Scale back up

        # Factor in combined probability (rarer combinations are more complex)
        probability_factor = (1 - combined_prob) * 10

        total = base_complexity + interaction_points + probability_factor
        return min(100, total)  # Cap at 100

    def _determine_cascade_order(self,
                                diseases: Tuple[str, ...],
                                interactions: Dict[Tuple[str, str], InteractionType]
                                ) -> Optional[List[str]]:
        """Determine temporal progression order if cascade pattern exists.

        Returns:
            List of diseases in cascade order, or None if not a cascade
        """
        # Check if this is primarily a cascade pattern
        cascade_count = sum(
            1 for itype in interactions.values()
            if itype == InteractionType.CASCADE
        )

        if cascade_count < len(diseases) - 1:
            return None  # Not enough cascade interactions

        # Simple topological sort based on interaction directions
        # This is a simplified version - in production would need directed graph
        ordered = []
        remaining = set(diseases)

        while remaining:
            if not ordered:
                # Start with most central disease (most interactions)
                disease = max(
                    remaining,
                    key=lambda d: sum(
                        1 for (d1, d2) in interactions.keys()
                        if d in (d1, d2)
                    )
                )
            else:
                # Find next disease most connected to last
                last = ordered[-1]
                candidates = [
                    d for d in remaining
                    if tuple(sorted([last, d])) in interactions
                ]
                disease = candidates[0] if candidates else remaining.pop()

            ordered.append(disease)
            remaining.discard(disease)

        return ordered if len(ordered) > 1 else None

    def _generate_mechanism_description(self,
                                       diseases: Tuple[str, ...],
                                       interactions: Dict[Tuple[str, str], InteractionType]
                                       ) -> str:
        """Generate human-readable description of interaction mechanism."""
        if len(diseases) == 2:
            interaction_type = list(interactions.values())[0]
            return f"{interaction_type.value} interaction"

        # For 3+ diseases
        cascade_interactions = sum(
            1 for itype in interactions.values()
            if itype == InteractionType.CASCADE
        )
        synergistic = sum(
            1 for itype in interactions.values()
            if itype == InteractionType.SYNERGISTIC
        )
        shared_pathway = sum(
            1 for itype in interactions.values()
            if itype == InteractionType.SHARED_PATHWAY
        )

        parts = []
        if cascade_interactions >= len(diseases) - 1:
            parts.append("cascade pattern")
        if synergistic >= 2:
            parts.append("synergistic effects")
        if shared_pathway >= 2:
            parts.append("shared biological pathway")

        if parts:
            return " with ".join(parts)

        return "multiple disease interactions"

    def _assess_clinical_significance(self,
                                     diseases: Tuple[str, ...],
                                     combined_prob: float,
                                     complexity: float) -> str:
        """Assess clinical significance of combination."""
        if combined_prob >= 0.60 and complexity >= 70:
            return "High significance - monitor all concurrent disease progression"
        elif combined_prob >= 0.40 or complexity >= 60:
            return "Moderate significance - adjust treatment planning for interactions"
        elif combined_prob >= 0.20:
            return "Low significance - possible but consider primary disease focus"
        else:
            return "Rare combination - treat independently unless symptoms suggest otherwise"

    def get_pattern(self, diseases: Tuple[str, ...]) -> Optional[CombinationPattern]:
        """Retrieve scored pattern for disease combination.

        Args:
            diseases: Tuple of disease names

        Returns:
            CombinationPattern if exists, None otherwise
        """
        diseases = tuple(sorted(diseases))
        if diseases in self.combination_patterns:
            return self.combination_patterns[diseases]
        return self._score_combination(diseases)

    def find_strongest_combinations(self, max_combinations: int = 10) -> List[CombinationPattern]:
        """Find strongest disease combinations by combined probability.

        Args:
            max_combinations: Maximum number to return

        Returns:
            List of top CombinationPattern objects
        """
        sorted_patterns = sorted(
            self.combination_patterns.values(),
            key=lambda p: (p.combined_probability, p.complexity_score),
            reverse=True
        )
        return sorted_patterns[:max_combinations]

    def analyze_disease_network(self) -> Dict:
        """Analyze the disease interaction network.

        Returns:
            Dict with network statistics and insights
        """
        return {
            "total_diseases": len(set(
                d for combo in self.combination_patterns.keys()
                for d in combo
            )),
            "total_combinations": len(self.combination_patterns),
            "clusters": len(self.disease_clusters),
            "avg_combination_probability": round(
                sum(p.combined_probability for p in self.combination_patterns.values())
                / len(self.combination_patterns) if self.combination_patterns else 0,
                3
            ),
            "avg_complexity": round(
                sum(p.complexity_score for p in self.combination_patterns.values())
                / len(self.combination_patterns) if self.combination_patterns else 0,
                2
            ),
        }


class InteractionRuleMiner:
    """Mine association rules from disease combinations using apriori-like algorithm."""

    def __init__(self, min_support: float = 0.15, min_confidence: float = 0.4):
        """Initialize rule miner.

        Args:
            min_support: Minimum support threshold (0-1)
            min_confidence: Minimum confidence threshold (0-1)
        """
        self.min_support = min_support
        self.min_confidence = min_confidence
        self.rules = []

    def mine_rules(self, combinations: List[CombinationPattern]) -> List[Dict]:
        """Mine association rules from disease combinations.

        Rule format: If diseases A, B present → disease C likely present

        Args:
            combinations: List of CombinationPattern objects

        Returns:
            List of discovered association rules
        """
        rules = []

        for combo in combinations:
            if len(combo.diseases) < 2:
                continue

            # Generate rules: disease subset → remaining disease
            for excluded in combo.diseases:
                antecedent = tuple(d for d in combo.diseases if d != excluded)
                consequent = excluded

                # Support = probability of antecedent AND consequent together
                support = combo.combined_probability

                if support < self.min_support:
                    continue

                # Confidence = P(consequent | antecedent)
                # Simplified: use combined probability as proxy
                confidence = support * 1.2  # Boost since we're conditioning
                confidence = min(1.0, confidence)

                if confidence >= self.min_confidence:
                    rule = {
                        "antecedent": antecedent,
                        "consequent": consequent,
                        "support": round(support, 3),
                        "confidence": round(confidence, 3),
                        "lift": round(confidence / combo.combined_probability, 2),
                    }
                    rules.append(rule)

        self.rules = rules
        return sorted(rules, key=lambda r: r["confidence"], reverse=True)
