"""Comprehensive test suite for MultiDiseaseExpander.

Tests cover combination expansion, interaction modeling, complexity scoring,
and association rule mining.
"""

import pytest
from typing import Dict, Tuple
import sys
import os

# Add API path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from api.ai.multidisease_expander import (
    MultiDiseaseExpander,
    DiseaseInteraction,
    CombinationPattern,
    InteractionType,
    InteractionRuleMiner,
)


class TestDiseaseInteraction:
    """Test DiseaseInteraction dataclass."""

    def test_disease_interaction_creation(self):
        """Test basic interaction creation."""
        interaction = DiseaseInteraction(
            disease_a="Hip Dysplasia",
            disease_b="Osteoarthritis",
            interaction_type=InteractionType.CASCADE,
            base_probability=0.85,
            mechanism="secondary_arthritis",
            age_factor=0.95,
            severity_factor=1.1,
        )

        assert interaction.disease_a == "Hip Dysplasia"
        assert interaction.disease_b == "Osteoarthritis"
        assert interaction.interaction_type == InteractionType.CASCADE

    def test_disease_interaction_to_dict(self):
        """Test serialization to dict."""
        interaction = DiseaseInteraction(
            disease_a="Disease A",
            disease_b="Disease B",
            interaction_type=InteractionType.SYNERGISTIC,
            base_probability=0.75,
            mechanism="test_mechanism",
            age_factor=1.0,
            severity_factor=1.0,
            breed_predispositions=["Breed1", "Breed2"],
        )

        result = interaction.to_dict()
        assert result["disease_a"] == "Disease A"
        assert result["interaction_type"] == "synergistic"
        assert result["base_probability"] == 0.75
        assert len(result["breed_predispositions"]) == 2


class TestCombinationPattern:
    """Test CombinationPattern dataclass."""

    def test_combination_pattern_creation(self):
        """Test basic pattern creation."""
        pattern = CombinationPattern(
            diseases=("Disease A", "Disease B", "Disease C"),
            interaction_types={
                ("Disease A", "Disease B"): InteractionType.CASCADE,
                ("Disease B", "Disease C"): InteractionType.SECONDARY,
            },
            combined_probability=0.45,
            cascade_order=["Disease A", "Disease B", "Disease C"],
            complexity_score=65.5,
            mechanism_description="cascade pattern",
            clinical_significance="High significance",
        )

        assert len(pattern.diseases) == 3
        assert pattern.combined_probability == 0.45
        assert pattern.complexity_score == 65.5

    def test_combination_pattern_to_dict(self):
        """Test serialization of pattern."""
        pattern = CombinationPattern(
            diseases=("A", "B", "C"),
            interaction_types={
                ("A", "B"): InteractionType.CASCADE,
            },
            combined_probability=0.5,
            cascade_order=["A", "B", "C"],
            complexity_score=70.0,
            mechanism_description="test",
            clinical_significance="High",
            supporting_cases=10,
        )

        result = pattern.to_dict()
        assert set(result["diseases"]) == {"A", "B", "C"}
        assert result["combined_probability"] == 0.5
        assert result["supporting_cases"] == 10


class TestMultiDiseaseExpander:
    """Test MultiDiseaseExpander functionality."""

    @pytest.fixture
    def sample_interactions(self) -> Dict[Tuple[str, str], DiseaseInteraction]:
        """Create sample 2-disease interactions."""
        interactions = {}

        # Orthopedic cascade
        interactions[("Hip Dysplasia", "Osteoarthritis")] = DiseaseInteraction(
            disease_a="Hip Dysplasia",
            disease_b="Osteoarthritis",
            interaction_type=InteractionType.CASCADE,
            base_probability=0.85,
            mechanism="secondary_arthritis",
            age_factor=0.95,
            severity_factor=1.1,
        )

        interactions[("Osteoarthritis", "Canine Cognitive Dysfunction")] = DiseaseInteraction(
            disease_a="Osteoarthritis",
            disease_b="Canine Cognitive Dysfunction",
            interaction_type=InteractionType.CASCADE,
            base_probability=0.45,
            mechanism="age_related",
            age_factor=1.3,
            severity_factor=0.9,
        )

        # Endocrine cascade
        interactions[("Pancreatitis", "Diabetes Mellitus")] = DiseaseInteraction(
            disease_a="Pancreatitis",
            disease_b="Diabetes Mellitus",
            interaction_type=InteractionType.CASCADE,
            base_probability=0.60,
            mechanism="endocrine",
            age_factor=1.05,
            severity_factor=0.85,
        )

        # GI complications
        interactions[("Pancreatitis", "Gastric Dilatation-Volvulus")] = DiseaseInteraction(
            disease_a="Pancreatitis",
            disease_b="Gastric Dilatation-Volvulus",
            interaction_type=InteractionType.SYNERGISTIC,
            base_probability=0.35,
            mechanism="inflammatory",
            age_factor=0.9,
            severity_factor=1.25,
        )

        # Metabolic interactions
        interactions[("Diabetes Mellitus", "Kidney Disease")] = DiseaseInteraction(
            disease_a="Diabetes Mellitus",
            disease_b="Kidney Disease",
            interaction_type=InteractionType.SECONDARY,
            base_probability=0.70,
            mechanism="diabetic_nephropathy",
            age_factor=1.2,
            severity_factor=1.3,
        )

        # Immune-mediated
        interactions[("Pancreatitis", "Inflammatory Bowel Disease")] = DiseaseInteraction(
            disease_a="Pancreatitis",
            disease_b="Inflammatory Bowel Disease",
            interaction_type=InteractionType.SHARED_PATHWAY,
            base_probability=0.40,
            mechanism="shared_immune_pathway",
            age_factor=1.0,
            severity_factor=1.15,
        )

        return interactions

    def test_expander_initialization(self, sample_interactions):
        """Test expander initialization."""
        expander = MultiDiseaseExpander(sample_interactions)
        assert len(expander.interaction_matrix) == len(sample_interactions)
        assert len(expander.disease_clusters) > 0

    def test_expand_combinations_3_diseases(self, sample_interactions):
        """Test expanding 3-disease combinations."""
        expander = MultiDiseaseExpander(sample_interactions)

        diseases = ["Hip Dysplasia", "Osteoarthritis", "Canine Cognitive Dysfunction"]
        patterns = expander.expand_combinations(diseases, min_combined_prob=0.1)

        assert len(patterns) > 0
        assert patterns[0].diseases == tuple(sorted(diseases))

    def test_expand_combinations_4_diseases(self, sample_interactions):
        """Test expanding 4-disease combinations."""
        expander = MultiDiseaseExpander(sample_interactions)

        diseases = [
            "Pancreatitis",
            "Diabetes Mellitus",
            "Kidney Disease",
            "Inflammatory Bowel Disease",
        ]
        patterns = expander.expand_combinations(diseases, min_combined_prob=0.05)

        assert len(patterns) > 0
        for pattern in patterns:
            assert 3 <= len(pattern.diseases) <= 4

    def test_combination_probability_calculation(self, sample_interactions):
        """Test probability calculation for combinations."""
        expander = MultiDiseaseExpander(sample_interactions)

        # Test 3-disease combination
        diseases = ("Hip Dysplasia", "Osteoarthritis", "Canine Cognitive Dysfunction")
        pattern = expander._score_combination(diseases)

        assert pattern is not None
        assert 0 <= pattern.combined_probability <= 1
        # Should be lower than pairwise due to dampening
        assert pattern.combined_probability < 0.85

    def test_complexity_calculation(self, sample_interactions):
        """Test complexity score calculation."""
        expander = MultiDiseaseExpander(sample_interactions)

        pattern = CombinationPattern(
            diseases=("A", "B", "C"),
            interaction_types={
                ("A", "B"): InteractionType.CASCADE,
                ("B", "C"): InteractionType.CASCADE,
            },
            combined_probability=0.5,
            cascade_order=None,
            complexity_score=0,  # Will be recalculated
            mechanism_description="test",
            clinical_significance="test",
        )

        complexity = expander._calculate_complexity(
            pattern.diseases,
            pattern.interaction_types,
            pattern.combined_probability,
        )

        assert 0 <= complexity <= 100
        assert complexity > 30  # 3-disease cascade should be moderately complex

    def test_cascade_order_determination(self, sample_interactions):
        """Test cascade order detection."""
        expander = MultiDiseaseExpander(sample_interactions)

        # Create cascade pattern
        interactions = {
            ("A", "B"): InteractionType.CASCADE,
            ("B", "C"): InteractionType.CASCADE,
        }

        order = expander._determine_cascade_order(("A", "B", "C"), interactions)
        assert order is not None
        assert len(order) == 3

    def test_mechanism_description_generation(self, sample_interactions):
        """Test mechanism description generation."""
        expander = MultiDiseaseExpander(sample_interactions)

        # Cascade pattern
        cascade_interactions = {
            ("A", "B"): InteractionType.CASCADE,
            ("B", "C"): InteractionType.CASCADE,
        }
        desc = expander._generate_mechanism_description(
            ("A", "B", "C"), cascade_interactions
        )
        assert "cascade" in desc.lower()

        # Synergistic pattern
        synergistic_interactions = {
            ("A", "B"): InteractionType.SYNERGISTIC,
            ("B", "C"): InteractionType.SYNERGISTIC,
        }
        desc = expander._generate_mechanism_description(
            ("A", "B", "C"), synergistic_interactions
        )
        assert "synergistic" in desc.lower()

    def test_clinical_significance_assessment(self, sample_interactions):
        """Test clinical significance assessment."""
        expander = MultiDiseaseExpander(sample_interactions)

        high_sig = expander._assess_clinical_significance(
            ("A", "B", "C"), combined_prob=0.65, complexity=75
        )
        assert "High significance" in high_sig

        low_sig = expander._assess_clinical_significance(
            ("A", "B", "C"), combined_prob=0.15, complexity=25
        )
        assert "Low significance" in low_sig or "Rare" in low_sig

    def test_get_pattern_retrieval(self, sample_interactions):
        """Test pattern retrieval."""
        expander = MultiDiseaseExpander(sample_interactions)

        # Score a pattern first
        diseases = ("Hip Dysplasia", "Osteoarthritis", "Canine Cognitive Dysfunction")
        pattern1 = expander.get_pattern(diseases)

        # Retrieve it again - should return cached version
        pattern2 = expander.get_pattern(diseases)

        assert pattern1 is not None
        assert pattern2 is not None
        assert pattern1.combined_probability == pattern2.combined_probability

    def test_find_strongest_combinations(self, sample_interactions):
        """Test finding strongest combinations."""
        expander = MultiDiseaseExpander(sample_interactions)

        # Populate patterns
        diseases_list = [
            ["Hip Dysplasia", "Osteoarthritis", "Canine Cognitive Dysfunction"],
            ["Pancreatitis", "Diabetes Mellitus", "Kidney Disease"],
        ]

        for diseases in diseases_list:
            expander.expand_combinations(diseases)

        strongest = expander.find_strongest_combinations(max_combinations=5)
        assert len(strongest) > 0
        assert len(strongest) <= 5

        # Should be sorted by probability
        for i in range(len(strongest) - 1):
            assert strongest[i].combined_probability >= strongest[i + 1].combined_probability

    def test_disease_network_analysis(self, sample_interactions):
        """Test disease network analysis."""
        expander = MultiDiseaseExpander(sample_interactions)

        # Populate some patterns
        expander.expand_combinations(
            ["Hip Dysplasia", "Osteoarthritis", "Canine Cognitive Dysfunction"]
        )

        network = expander.analyze_disease_network()

        assert "total_diseases" in network
        assert "total_combinations" in network
        assert "clusters" in network
        assert "avg_combination_probability" in network
        assert "avg_complexity" in network

        assert network["total_combinations"] > 0
        assert 0 <= network["avg_combination_probability"] <= 1
        assert 0 <= network["avg_complexity"] <= 100


class TestInteractionRuleMiner:
    """Test InteractionRuleMiner functionality."""

    @pytest.fixture
    def sample_patterns(self) -> list:
        """Create sample patterns for mining."""
        return [
            CombinationPattern(
                diseases=("A", "B", "C"),
                interaction_types={
                    ("A", "B"): InteractionType.CASCADE,
                    ("B", "C"): InteractionType.CASCADE,
                },
                combined_probability=0.6,
                cascade_order=["A", "B", "C"],
                complexity_score=70,
                mechanism_description="cascade",
                clinical_significance="High",
            ),
            CombinationPattern(
                diseases=("B", "C", "D"),
                interaction_types={
                    ("B", "C"): InteractionType.SECONDARY,
                    ("C", "D"): InteractionType.SYNERGISTIC,
                },
                combined_probability=0.45,
                cascade_order=None,
                complexity_score=60,
                mechanism_description="mixed",
                clinical_significance="Moderate",
            ),
        ]

    def test_miner_initialization(self):
        """Test rule miner initialization."""
        miner = InteractionRuleMiner(min_support=0.20, min_confidence=0.50)
        assert miner.min_support == 0.20
        assert miner.min_confidence == 0.50

    def test_mine_rules_basic(self, sample_patterns):
        """Test basic rule mining."""
        miner = InteractionRuleMiner(min_support=0.4, min_confidence=0.5)
        rules = miner.mine_rules(sample_patterns)

        assert len(rules) > 0
        for rule in rules:
            assert "antecedent" in rule
            assert "consequent" in rule
            assert "support" in rule
            assert "confidence" in rule
            assert "lift" in rule

    def test_rule_quality_metrics(self, sample_patterns):
        """Test rule quality metrics."""
        miner = InteractionRuleMiner(min_support=0.4, min_confidence=0.5)
        rules = miner.mine_rules(sample_patterns)

        for rule in rules:
            assert 0 <= rule["support"] <= 1
            assert 0 <= rule["confidence"] <= 1
            assert rule["lift"] >= 0

    def test_rule_filtering_by_confidence(self, sample_patterns):
        """Test rule filtering by confidence threshold."""
        miner_strict = InteractionRuleMiner(
            min_support=0.1, min_confidence=0.8
        )
        rules_strict = miner_strict.mine_rules(sample_patterns)

        miner_loose = InteractionRuleMiner(
            min_support=0.1, min_confidence=0.3
        )
        rules_loose = miner_loose.mine_rules(sample_patterns)

        # Stricter threshold should have fewer rules
        assert len(rules_strict) <= len(rules_loose)

        # All strict rules should have high confidence
        for rule in rules_strict:
            assert rule["confidence"] >= 0.8

    def test_rule_antecedent_consequent_structure(self, sample_patterns):
        """Test rule antecedent/consequent structure."""
        miner = InteractionRuleMiner()
        rules = miner.mine_rules(sample_patterns)

        for rule in rules:
            antecedent = rule["antecedent"]
            consequent = rule["consequent"]

            # Antecedent should be tuple
            assert isinstance(antecedent, tuple)
            # Consequent should be string
            assert isinstance(consequent, str)
            # Consequent should not be in antecedent
            assert consequent not in antecedent


class TestIntegration:
    """Integration tests combining multiple components."""

    @pytest.fixture
    def full_interaction_matrix(self) -> Dict[Tuple[str, str], DiseaseInteraction]:
        """Create full test interaction matrix."""
        interactions = {}

        disease_pairs = [
            ("Hip Dysplasia", "Osteoarthritis", 0.85, InteractionType.CASCADE),
            ("Osteoarthritis", "Mobility Loss", 0.60, InteractionType.SECONDARY),
            ("Pancreatitis", "Diabetes", 0.60, InteractionType.CASCADE),
            ("Diabetes", "Kidney Disease", 0.70, InteractionType.SECONDARY),
            ("Kidney Disease", "Anemia", 0.55, InteractionType.SECONDARY),
        ]

        for d1, d2, prob, itype in disease_pairs:
            interactions[(d1, d2)] = DiseaseInteraction(
                disease_a=d1,
                disease_b=d2,
                interaction_type=itype,
                base_probability=prob,
                mechanism="test",
                age_factor=1.0,
                severity_factor=1.0,
            )

        return interactions

    def test_full_pipeline(self, full_interaction_matrix):
        """Test full pipeline from expansion to rule mining."""
        # Initialize expander
        expander = MultiDiseaseExpander(full_interaction_matrix)

        # Expand combinations
        diseases = ["Hip Dysplasia", "Osteoarthritis", "Mobility Loss"]
        patterns = expander.expand_combinations(diseases)

        assert len(patterns) > 0

        # Mine rules
        miner = InteractionRuleMiner()
        rules = miner.mine_rules(patterns)

        assert len(rules) > 0

        # Analyze network
        network = expander.analyze_disease_network()
        assert network["total_combinations"] > 0

    def test_pattern_progression(self, full_interaction_matrix):
        """Test disease progression in patterns."""
        expander = MultiDiseaseExpander(full_interaction_matrix)

        # Orthopedic progression
        ortho_diseases = ["Hip Dysplasia", "Osteoarthritis", "Mobility Loss"]
        ortho_patterns = expander.expand_combinations(ortho_diseases)

        assert len(ortho_patterns) > 0

        # Endocrine progression
        endo_diseases = ["Pancreatitis", "Diabetes", "Kidney Disease"]
        endo_patterns = expander.expand_combinations(endo_diseases)

        assert len(endo_patterns) > 0

        # Orthopedic should have cascade interactions
        if ortho_patterns:
            cascades = sum(
                1 for itype in ortho_patterns[0].interaction_types.values()
                if itype == InteractionType.CASCADE
            )
            assert cascades > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
