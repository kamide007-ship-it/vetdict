"""Tests for api/ai/symptom_interactions.py – focusing on TripleInteractionMatrix
and edge cases not covered by test_ai_symptom_interactions.py."""

import pytest

from api.ai.symptom_interactions import (
    InteractionScorer,
    SymptomInteractionMatrix,
    TripleInteractionMatrix,
    analyze_symptom_interactions,
)

# ===================================================================
# Fixtures
# ===================================================================

@pytest.fixture
def diseases_with_triples():
    """Diseases where each has 3+ symptoms to produce triple interactions."""
    return [
        {
            "id": "d1",
            "symptoms": {"fever", "cough", "lethargy", "nasal_discharge"},
        },
        {
            "id": "d2",
            "symptoms": {"fever", "cough", "lethargy", "vomiting"},
        },
        {
            "id": "d3",
            "symptoms": {"fever", "cough", "lethargy", "diarrhea"},
        },
        {
            "id": "d4",
            "symptoms": {"joint_pain", "swelling", "fever"},
        },
    ]


@pytest.fixture
def minimal_diseases():
    """Minimal disease set with pairs that meet min_frequency=1."""
    return [
        {"id": "x1", "symptoms": {"a", "b", "c"}},
        {"id": "x2", "symptoms": {"a", "b", "d"}},
    ]


@pytest.fixture
def small_diseases():
    """Diseases with fewer than 3 symptoms – should produce no triples."""
    return [
        {"id": "s1", "symptoms": {"fever", "cough"}},
        {"id": "s2", "symptoms": {"lethargy"}},
    ]


# ===================================================================
# TripleInteractionMatrix – _build_matrix and basic structure
# ===================================================================

class TestTripleInteractionMatrix:
    def test_init_with_triple_diseases(self, diseases_with_triples):
        matrix = TripleInteractionMatrix(diseases_with_triples)
        assert matrix.total_diseases == 4
        assert matrix.min_frequency == 1  # default

    def test_triples_built_from_diseases(self, diseases_with_triples):
        matrix = TripleInteractionMatrix(diseases_with_triples)
        # fever+cough+lethargy appears in d1, d2, d3 → should be in triple_weights
        assert len(matrix.triple_weights) > 0

    def test_triple_weights_normalized(self, diseases_with_triples):
        matrix = TripleInteractionMatrix(diseases_with_triples)
        for key, w in matrix.triple_weights.items():
            assert 0.0 < w <= 1.0, f"Weight {w} out of range for triple {key}"

    def test_triple_frequencies_counted(self, diseases_with_triples):
        matrix = TripleInteractionMatrix(diseases_with_triples)
        # fever+cough+lethargy appears in 3 of 4 diseases
        key = frozenset({"fever", "cough", "lethargy"})
        assert matrix.triple_frequencies[key] == 3

    def test_diseases_with_fewer_than_3_symptoms_skipped(self, small_diseases):
        matrix = TripleInteractionMatrix(small_diseases)
        assert len(matrix.triple_frequencies) == 0
        assert len(matrix.triple_weights) == 0

    def test_min_frequency_filtering(self, diseases_with_triples):
        matrix_min1 = TripleInteractionMatrix(diseases_with_triples, min_frequency=1)
        matrix_min4 = TripleInteractionMatrix(diseases_with_triples, min_frequency=4)
        # min_frequency=4 should exclude triples that appear < 4 times
        assert len(matrix_min4.triple_weights) <= len(matrix_min1.triple_weights)

    def test_list_symptoms_converted_to_set(self):
        diseases = [
            {"id": "l1", "symptoms": ["a", "b", "c"]},
            {"id": "l2", "symptoms": ["a", "b", "c"]},
        ]
        matrix = TripleInteractionMatrix(diseases, min_frequency=1)
        assert len(matrix.triple_weights) > 0

    def test_get_total_triples(self, diseases_with_triples):
        matrix = TripleInteractionMatrix(diseases_with_triples)
        total = matrix.get_total_triples()
        assert total == len(matrix.triple_weights)
        assert total >= 0

    def test_empty_diseases(self):
        matrix = TripleInteractionMatrix([])
        assert matrix.total_diseases == 0
        assert len(matrix.triple_weights) == 0
        assert matrix.get_total_triples() == 0

    def test_no_symptoms_key_disease(self):
        diseases = [{"id": "no_sym"}]  # no "symptoms" key
        matrix = TripleInteractionMatrix(diseases, min_frequency=1)
        assert len(matrix.triple_weights) == 0


# ===================================================================
# TripleInteractionMatrix – find_triple_interactions
# ===================================================================

class TestFindTripleInteractions:
    def test_returns_empty_for_fewer_than_3_symptoms(self, diseases_with_triples):
        matrix = TripleInteractionMatrix(diseases_with_triples)
        assert matrix.find_triple_interactions([]) == []
        assert matrix.find_triple_interactions(["fever"]) == []
        assert matrix.find_triple_interactions(["fever", "cough"]) == []

    def test_finds_known_triple(self, diseases_with_triples):
        matrix = TripleInteractionMatrix(diseases_with_triples)
        # fever+cough+lethargy appears in 3 diseases → high weight
        interactions = matrix.find_triple_interactions(
            ["fever", "cough", "lethargy"], weight_threshold=0.0
        )
        assert len(interactions) > 0
        triples_found = [frozenset(i["triple"]) for i in interactions]
        assert frozenset({"fever", "cough", "lethargy"}) in triples_found

    def test_interaction_structure(self, diseases_with_triples):
        matrix = TripleInteractionMatrix(diseases_with_triples)
        interactions = matrix.find_triple_interactions(
            ["fever", "cough", "lethargy", "nasal_discharge"],
            weight_threshold=0.0,
        )
        for interaction in interactions:
            assert "triple" in interaction
            assert "weight" in interaction
            assert "boost_factor" in interaction
            assert len(interaction["triple"]) == 3
            assert isinstance(interaction["weight"], float)
            assert isinstance(interaction["boost_factor"], float)

    def test_sorted_by_weight_descending(self, diseases_with_triples):
        matrix = TripleInteractionMatrix(diseases_with_triples)
        interactions = matrix.find_triple_interactions(
            ["fever", "cough", "lethargy", "nasal_discharge", "vomiting"],
            weight_threshold=0.0,
        )
        if len(interactions) > 1:
            weights = [i["weight"] for i in interactions]
            assert weights == sorted(weights, reverse=True)

    def test_weight_threshold_filters_results(self, diseases_with_triples):
        matrix = TripleInteractionMatrix(diseases_with_triples)
        symptoms = ["fever", "cough", "lethargy", "nasal_discharge"]
        low = matrix.find_triple_interactions(symptoms, weight_threshold=0.0)
        high = matrix.find_triple_interactions(symptoms, weight_threshold=0.99)
        assert len(high) <= len(low)

    def test_boost_factor_is_weight_times_020(self, diseases_with_triples):
        matrix = TripleInteractionMatrix(diseases_with_triples)
        interactions = matrix.find_triple_interactions(
            ["fever", "cough", "lethargy"], weight_threshold=0.0
        )
        for i in interactions:
            expected_boost = round(i["weight"] * 0.20, 3)
            assert i["boost_factor"] == expected_boost

    def test_triple_sorted_alphabetically(self, diseases_with_triples):
        matrix = TripleInteractionMatrix(diseases_with_triples)
        interactions = matrix.find_triple_interactions(
            ["fever", "cough", "lethargy"], weight_threshold=0.0
        )
        for i in interactions:
            assert i["triple"] == sorted(i["triple"])

    def test_symptoms_with_no_matching_triples(self, diseases_with_triples):
        matrix = TripleInteractionMatrix(diseases_with_triples)
        # Use symptoms that are not in any disease triple; with threshold > 0.0
        # they should produce no results (weight would be 0.0, below threshold)
        interactions = matrix.find_triple_interactions(
            ["xyz_symptom_a", "xyz_symptom_b", "xyz_symptom_c"],
            weight_threshold=0.01,
        )
        assert interactions == []

    def test_weight_capped_at_one(self, diseases_with_triples):
        # More diseases than min_frequency but weight = freq/total <= 1
        matrix = TripleInteractionMatrix(diseases_with_triples)
        for w in matrix.triple_weights.values():
            assert w <= 1.0

    def test_default_threshold_filters_low_weight(self, minimal_diseases):
        # min_frequency=1, default weight_threshold=0.05
        matrix = TripleInteractionMatrix(minimal_diseases, min_frequency=1)
        symptoms = ["a", "b", "c"]
        # Default threshold is 0.05
        interactions_default = matrix.find_triple_interactions(symptoms)
        interactions_zero = matrix.find_triple_interactions(symptoms, weight_threshold=0.0)
        assert len(interactions_default) <= len(interactions_zero)


# ===================================================================
# SymptomInteractionMatrix – empty/edge cases not in existing tests
# ===================================================================

class TestSymptomInteractionMatrixEdgeCases:
    def test_empty_disease_list(self):
        matrix = SymptomInteractionMatrix([])
        assert matrix.total_diseases == 0
        assert len(matrix.pair_weights) == 0
        assert matrix.get_total_interactions() == 0

    def test_get_stats_empty_matrix(self):
        matrix = SymptomInteractionMatrix([])
        stats = matrix.get_stats()
        assert stats["total_pairs"] == 0
        assert stats["diseases_analyzed"] == 0
        assert stats["avg_frequency"] == 0.0
        assert stats["max_frequency"] == 0

    def test_get_pair_weight_unknown_pair(self):
        diseases = [{"id": "d1", "symptoms": {"a", "b"}}]
        matrix = SymptomInteractionMatrix(diseases, min_frequency=1)
        weight = matrix.get_pair_weight("unknown_x", "unknown_y")
        assert weight == 0.0

    def test_disease_with_no_symptoms_key(self):
        diseases = [{"id": "no_sym"}]
        matrix = SymptomInteractionMatrix(diseases, min_frequency=1)
        assert len(matrix.pair_weights) == 0

    def test_min_frequency_1_includes_single_occurrences(self):
        diseases = [{"id": "d1", "symptoms": {"x", "y", "z"}}]
        matrix = SymptomInteractionMatrix(diseases, min_frequency=1)
        assert len(matrix.pair_weights) > 0

    def test_get_stats_with_data(self):
        diseases = [
            {"id": "d1", "symptoms": {"a", "b", "c"}},
            {"id": "d2", "symptoms": {"a", "b"}},
        ]
        matrix = SymptomInteractionMatrix(diseases, min_frequency=1)
        stats = matrix.get_stats()
        assert stats["diseases_analyzed"] == 2
        assert stats["max_frequency"] >= 2  # a+b appears twice
        assert stats["avg_frequency"] > 0.0


# ===================================================================
# InteractionScorer – edge cases
# ===================================================================

class TestInteractionScorerEdgeCases:
    def test_score_capped_at_one(self):
        diseases = [
            {"id": "d1", "symptoms": {"a", "b"}},
            {"id": "d2", "symptoms": {"a", "b"}},
            {"id": "d3", "symptoms": {"a", "b"}},
        ]
        matrix = SymptomInteractionMatrix(diseases, min_frequency=1)
        scorer = InteractionScorer(matrix)
        # Very high base confidence
        confidence, interactions = scorer.score_symptom_set(
            ["a", "b"], base_confidence=0.99, max_boost=0.5
        )
        assert confidence <= 1.0

    def test_score_empty_symptoms(self):
        diseases = [{"id": "d1", "symptoms": {"a", "b"}}]
        matrix = SymptomInteractionMatrix(diseases, min_frequency=1)
        scorer = InteractionScorer(matrix)
        confidence, interactions = scorer.score_symptom_set([], base_confidence=0.5)
        assert confidence == 0.5
        assert interactions == []

    def test_score_single_symptom(self):
        diseases = [{"id": "d1", "symptoms": {"a", "b"}}]
        matrix = SymptomInteractionMatrix(diseases, min_frequency=1)
        scorer = InteractionScorer(matrix)
        confidence, interactions = scorer.score_symptom_set(["a"], base_confidence=0.6)
        assert confidence == 0.6
        assert interactions == []


# ===================================================================
# analyze_symptom_interactions – edge cases
# ===================================================================

class TestAnalyzeSymptomInteractionsEdgeCases:
    def test_with_min_frequency_1(self):
        diseases = [{"id": "d1", "symptoms": {"fever", "cough", "lethargy"}}]
        result = analyze_symptom_interactions(
            ["fever", "cough"], diseases, min_frequency=1
        )
        assert result["interaction_count"] >= 1
        assert result["strongest_pair"] is not None

    def test_strongest_pair_is_tuple(self):
        diseases = [
            {"id": "d1", "symptoms": {"a", "b"}},
            {"id": "d2", "symptoms": {"a", "b"}},
        ]
        result = analyze_symptom_interactions(["a", "b"], diseases, min_frequency=1)
        if result["strongest_pair"] is not None:
            assert isinstance(result["strongest_pair"], tuple)
            assert len(result["strongest_pair"]) == 2

    def test_boost_potential_value(self):
        diseases = [
            {"id": "d1", "symptoms": {"x", "y"}},
            {"id": "d2", "symptoms": {"x", "y"}},
        ]
        result = analyze_symptom_interactions(["x", "y"], diseases, min_frequency=1)
        assert isinstance(result["boost_potential"], float)
        assert result["boost_potential"] >= 0.0

    def test_weight_threshold_parameter_used(self):
        diseases = [
            {"id": "d1", "symptoms": {"a", "b"}},
            {"id": "d2", "symptoms": {"a", "b"}},
        ]
        result_low = analyze_symptom_interactions(
            ["a", "b"], diseases, min_frequency=1, weight_threshold=0.0
        )
        result_high = analyze_symptom_interactions(
            ["a", "b"], diseases, min_frequency=1, weight_threshold=0.99
        )
        assert result_high["interaction_count"] <= result_low["interaction_count"]

    def test_empty_symptoms_list(self):
        diseases = [{"id": "d1", "symptoms": {"a", "b"}}]
        result = analyze_symptom_interactions([], diseases)
        assert result["interaction_count"] == 0
        assert result["strongest_pair"] is None
        assert result["boost_potential"] == 0.0

    def test_empty_diseases(self):
        result = analyze_symptom_interactions(["a", "b"], [])
        assert result["interaction_count"] == 0
