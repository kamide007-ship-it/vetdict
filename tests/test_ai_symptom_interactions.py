"""Tests for symptom interactions module."""

import pytest

from api.ai.symptom_interactions import (
    InteractionScorer,
    SymptomInteractionMatrix,
    analyze_symptom_interactions,
)


@pytest.fixture
def sample_diseases():
    """Sample disease database for testing."""
    return [
        {
            "id": "disease_1",
            "name": "pneumonia",
            "symptoms": {"coughing", "fever", "difficulty_breathing"},
        },
        {
            "id": "disease_2",
            "name": "gastroenteritis",
            "symptoms": {"vomiting", "diarrhea", "fever"},
        },
        {
            "id": "disease_3",
            "name": "flu",
            "symptoms": {"coughing", "fever", "lethargy"},
        },
        {
            "id": "disease_4",
            "name": "kennel_cough",
            "symptoms": {"coughing", "nasal_discharge"},
        },
    ]


def test_interaction_matrix_creation(sample_diseases):
    """Test SymptomInteractionMatrix initialization."""
    matrix = SymptomInteractionMatrix(sample_diseases)

    assert matrix.total_diseases == 4
    assert len(matrix.pair_weights) > 0
    # Verify pairs are frozensets
    for pair_key in matrix.pair_weights:
        assert isinstance(pair_key, frozenset)


def test_interaction_matrix_pair_weight(sample_diseases):
    """Test retrieving interaction weights for pairs."""
    matrix = SymptomInteractionMatrix(sample_diseases)

    # fever + coughing appears in disease_1 and disease_3 (2 times)
    weight = matrix.get_pair_weight("coughing", "fever")
    assert weight > 0.0
    assert weight <= 1.0

    # vomiting + diarrhea appears in disease_2 (1 time, below min_frequency)
    weight_low = matrix.get_pair_weight("vomiting", "diarrhea")
    assert weight_low == 0.0  # Below min_frequency of 2


def test_find_interactions(sample_diseases):
    """Test finding high-weight interactions in symptom set."""
    matrix = SymptomInteractionMatrix(sample_diseases)

    # Pneumonia symptoms should show fever + coughing interaction
    symptoms = ["coughing", "fever", "difficulty_breathing"]
    interactions = matrix.find_interactions(symptoms, weight_threshold=0.0)

    assert len(interactions) > 0
    # Check interaction structure
    for interaction in interactions:
        assert "pair" in interaction
        assert "weight" in interaction
        assert "boost_factor" in interaction
        assert len(interaction["pair"]) == 2


def test_find_interactions_sorted_by_weight(sample_diseases):
    """Test interactions are sorted by weight descending."""
    matrix = SymptomInteractionMatrix(sample_diseases)

    symptoms = ["coughing", "fever", "lethargy", "difficulty_breathing"]
    interactions = matrix.find_interactions(symptoms, weight_threshold=0.0)

    if len(interactions) > 1:
        weights = [i["weight"] for i in interactions]
        assert weights == sorted(weights, reverse=True)


def test_find_interactions_empty_symptoms(sample_diseases):
    """Test finding interactions with empty/single symptom."""
    matrix = SymptomInteractionMatrix(sample_diseases)

    # No interactions with single symptom
    interactions = matrix.find_interactions(["coughing"])
    assert len(interactions) == 0

    # No interactions with empty list
    interactions = matrix.find_interactions([])
    assert len(interactions) == 0


def test_find_interactions_weight_threshold(sample_diseases):
    """Test weight threshold filtering."""
    matrix = SymptomInteractionMatrix(sample_diseases)

    symptoms = ["coughing", "fever", "lethargy", "difficulty_breathing"]

    # With low threshold
    interactions_low = matrix.find_interactions(symptoms, weight_threshold=0.0)

    # With high threshold
    interactions_high = matrix.find_interactions(symptoms, weight_threshold=0.9)

    # Higher threshold should give fewer or equal results
    assert len(interactions_high) <= len(interactions_low)


def test_get_total_interactions(sample_diseases):
    """Test getting total interaction count."""
    matrix = SymptomInteractionMatrix(sample_diseases)

    total = matrix.get_total_interactions()
    assert total > 0
    assert total == len(matrix.pair_weights)


def test_get_stats(sample_diseases):
    """Test statistics reporting."""
    matrix = SymptomInteractionMatrix(sample_diseases)

    stats = matrix.get_stats()

    assert "total_pairs" in stats
    assert "diseases_analyzed" in stats
    assert "avg_frequency" in stats
    assert "max_frequency" in stats
    assert stats["diseases_analyzed"] == 4
    assert stats["total_pairs"] > 0


def test_interaction_scorer_initialization(sample_diseases):
    """Test InteractionScorer initialization."""
    matrix = SymptomInteractionMatrix(sample_diseases)
    scorer = InteractionScorer(matrix)

    assert scorer.matrix == matrix


def test_interaction_scorer_score_symptom_set(sample_diseases):
    """Test scoring symptom set with interactions."""
    matrix = SymptomInteractionMatrix(sample_diseases)
    scorer = InteractionScorer(matrix)

    symptoms = ["coughing", "fever"]
    confidence, interactions = scorer.score_symptom_set(symptoms, base_confidence=0.80)

    assert 0.0 <= confidence <= 1.0
    assert isinstance(interactions, list)


def test_interaction_scorer_no_boost_with_no_interactions(sample_diseases):
    """Test no confidence boost when no interactions found."""
    matrix = SymptomInteractionMatrix(sample_diseases)
    scorer = InteractionScorer(matrix)

    # Single symptom has no interactions
    symptoms = ["nasal_discharge"]
    confidence, interactions = scorer.score_symptom_set(symptoms, base_confidence=0.80)

    # Confidence should not change without interactions
    assert confidence == 0.80
    assert len(interactions) == 0


def test_interaction_scorer_boost_applied(sample_diseases):
    """Test confidence boost is applied for strong interactions."""
    matrix = SymptomInteractionMatrix(sample_diseases)
    scorer = InteractionScorer(matrix)

    # fever + coughing is a strong pair (appears in 2 diseases)
    symptoms = ["coughing", "fever"]
    base_conf = 0.80
    confidence, interactions = scorer.score_symptom_set(symptoms, base_confidence=base_conf, max_boost=0.15)

    if interactions:  # If interaction found, confidence should be higher
        assert confidence > base_conf
        assert confidence <= 1.0


def test_interaction_scorer_capped_at_one(sample_diseases):
    """Test confidence is capped at 1.0."""
    matrix = SymptomInteractionMatrix(sample_diseases)
    scorer = InteractionScorer(matrix)

    # High base confidence + boost should not exceed 1.0
    symptoms = ["coughing", "fever"]
    confidence, _ = scorer.score_symptom_set(symptoms, base_confidence=0.95, max_boost=0.20)

    assert confidence <= 1.0


def test_analyze_symptom_interactions(sample_diseases):
    """Test convenience function for interaction analysis."""
    symptoms = ["coughing", "fever"]

    result = analyze_symptom_interactions(symptoms, sample_diseases)

    assert "interactions" in result
    assert "strongest_pair" in result
    assert "interaction_count" in result
    assert "boost_potential" in result
    assert isinstance(result["interactions"], list)
    assert isinstance(result["interaction_count"], int)


def test_analyze_symptom_interactions_no_pairs(sample_diseases):
    """Test analysis with symptom that has no interactions."""
    symptoms = ["nasal_discharge"]

    result = analyze_symptom_interactions(symptoms, sample_diseases)

    assert result["interaction_count"] == 0
    assert result["strongest_pair"] is None
    assert result["boost_potential"] == 0.0


def test_interaction_matrix_with_list_symptoms(sample_diseases):
    """Test matrix handles list-type symptoms (not just sets)."""
    # Convert sets to lists
    diseases_with_lists = [
        {
            "id": d["id"],
            "name": d["name"],
            "symptoms": list(d["symptoms"]),
        }
        for d in sample_diseases
    ]

    matrix = SymptomInteractionMatrix(diseases_with_lists)
    assert matrix.total_diseases == 4
    assert len(matrix.pair_weights) > 0


def test_interaction_weight_normalization(sample_diseases):
    """Test weights are properly normalized (0.0-1.0)."""
    matrix = SymptomInteractionMatrix(sample_diseases)

    for pair, weight in matrix.pair_weights.items():
        assert 0.0 <= weight <= 1.0, f"Weight {weight} out of range for pair {pair}"
