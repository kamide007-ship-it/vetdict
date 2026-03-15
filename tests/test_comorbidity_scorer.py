"""Tests for comorbidity_scorer.py - Disease interaction quantification."""

import pytest

from api.ai.comorbidity_scorer import ComorbidityScorer, InteractionEffect


class TestInteractionEffect:

    def test_dataclass_fields(self):
        ie = InteractionEffect(
            disease_a="A", disease_b="B",
            base_interaction_score=0.5,
            symptom_overlap_ratio=0.3,
            confidence_amplification=1.1,
            explanation="test",
        )
        assert ie.disease_a == "A"
        assert ie.disease_b == "B"
        assert ie.base_interaction_score == 0.5


class TestCalculateInteractionEffect:

    def test_no_overlap_independent(self):
        """No symptom overlap → slightly positive interaction."""
        ie = ComorbidityScorer.calculate_interaction_effect(
            "Disease A", "Disease B",
            ["s1", "s2"], ["s3", "s4"],
            ["s1", "s3"],
        )
        assert ie.base_interaction_score >= 0.3
        assert ie.confidence_amplification >= 1.0
        assert ie.symptom_overlap_ratio == 0.0

    def test_high_overlap_competitive(self):
        """High symptom overlap → competitive (negative) interaction."""
        ie = ComorbidityScorer.calculate_interaction_effect(
            "Disease A", "Disease B",
            ["s1", "s2", "s3"], ["s1", "s2", "s3"],
            ["s1", "s2"],
        )
        assert ie.symptom_overlap_ratio > 0.7
        # High overlap gets negative base, but detected overlap adds 0.2
        assert ie.confidence_amplification < 1.15

    def test_moderate_overlap(self):
        """Moderate overlap → neutral interaction."""
        ie = ComorbidityScorer.calculate_interaction_effect(
            "Disease A", "Disease B",
            ["s1", "s2", "s3"], ["s2", "s3", "s4"],
            ["s1"],
        )
        assert 0.3 <= ie.symptom_overlap_ratio <= 0.7

    def test_detected_overlap_boosts(self):
        """When overlap symptoms are actually detected, interaction boosts."""
        ie = ComorbidityScorer.calculate_interaction_effect(
            "A", "B",
            ["s1", "s2", "s3"], ["s2", "s4", "s5"],
            ["s2"],  # s2 is shared and detected
        )
        # both_in_detected > 0, so +0.2 to base_interaction_score
        assert ie.base_interaction_score > 0.0

    def test_empty_symptoms(self):
        """Empty symptom sets."""
        ie = ComorbidityScorer.calculate_interaction_effect(
            "A", "B", [], [], [],
        )
        assert ie.symptom_overlap_ratio == 0.0


class TestGenerateInteractionExplanation:

    def test_positive_low_overlap(self):
        exp = ComorbidityScorer._generate_interaction_explanation("A", "B", 0.1, 0.5)
        assert "異なる器官系" in exp

    def test_positive_high_overlap(self):
        exp = ComorbidityScorer._generate_interaction_explanation("A", "B", 0.5, 0.5)
        assert "関連のある症状" in exp

    def test_negative_interaction(self):
        exp = ComorbidityScorer._generate_interaction_explanation("A", "B", 0.5, -0.5)
        assert "一方" in exp

    def test_neutral_interaction(self):
        exp = ComorbidityScorer._generate_interaction_explanation("A", "B", 0.5, 0.0)
        assert "独立" in exp


class TestScoreDiseaseCombination:

    def test_returns_tuple(self):
        score, breakdown = ComorbidityScorer.score_disease_combination(
            "Hip Dysplasia", "Osteoarthritis", 0.7, 0.6,
        )
        assert isinstance(score, float)
        assert isinstance(breakdown, dict)
        assert 0.0 <= score <= 1.0

    def test_breakdown_has_expected_keys(self):
        _, breakdown = ComorbidityScorer.score_disease_combination(
            "A", "B", 0.5, 0.5,
        )
        assert "confidence_a" in breakdown
        assert "confidence_b" in breakdown
        assert "comorbidity_probability" in breakdown
        assert "symptom_overlap_penalty" in breakdown
        assert "combined_confidence" in breakdown
        assert "formula_explanation" in breakdown

    def test_higher_overlap_reduces_score(self):
        score_low, _ = ComorbidityScorer.score_disease_combination(
            "A", "B", 0.7, 0.6, symptom_overlap_ratio=0.1,
        )
        score_high, _ = ComorbidityScorer.score_disease_combination(
            "A", "B", 0.7, 0.6, symptom_overlap_ratio=0.9,
        )
        assert score_low >= score_high

    def test_with_age_and_breed(self):
        score, _ = ComorbidityScorer.score_disease_combination(
            "A", "B", 0.7, 0.6, age_years=10, severity="severe", breed="golden_retriever",
        )
        assert 0.0 <= score <= 1.0


class TestAdjustIndividualConfidences:

    def test_high_overlap_reduces(self):
        a, b = ComorbidityScorer.adjust_individual_confidences_for_combination(
            0.8, 0.7, 0.8,
        )
        assert a < 0.8
        assert b < 0.7

    def test_moderate_overlap(self):
        a, b = ComorbidityScorer.adjust_individual_confidences_for_combination(
            0.8, 0.7, 0.5,
        )
        assert a < 0.8  # 0.95 adjustment

    def test_low_overlap_known_comorbidity_boosts(self):
        a, b = ComorbidityScorer.adjust_individual_confidences_for_combination(
            0.8, 0.7, 0.2, comorbidity_known=True,
        )
        assert a > 0.8  # 1.05 boost

    def test_low_overlap_unknown_no_boost(self):
        a, b = ComorbidityScorer.adjust_individual_confidences_for_combination(
            0.8, 0.7, 0.2, comorbidity_known=False,
        )
        assert a == pytest.approx(0.8)

    def test_clamps_to_valid_range(self):
        a, b = ComorbidityScorer.adjust_individual_confidences_for_combination(
            1.0, 1.0, 0.1, comorbidity_known=True,
        )
        assert a <= 1.0
        assert b <= 1.0


class TestEstimateSymptomOverlap:

    def test_identical_sets(self):
        assert ComorbidityScorer.estimate_symptom_overlap(["a", "b"], ["a", "b"]) == 1.0

    def test_disjoint_sets(self):
        assert ComorbidityScorer.estimate_symptom_overlap(["a"], ["b"]) == 0.0

    def test_empty_list(self):
        assert ComorbidityScorer.estimate_symptom_overlap([], ["a"]) == 0.0

    def test_partial_overlap(self):
        result = ComorbidityScorer.estimate_symptom_overlap(["a", "b"], ["b", "c"])
        assert result == pytest.approx(1 / 3)


class TestComorbiditySeverityAdjustment:

    def test_severe_boosts(self):
        result = ComorbidityScorer.calculate_comorbidity_severity_adjustment(0.5, "severe")
        assert result > 0.5

    def test_mild_reduces(self):
        result = ComorbidityScorer.calculate_comorbidity_severity_adjustment(0.5, "mild")
        assert result < 0.5

    def test_moderate_unchanged(self):
        result = ComorbidityScorer.calculate_comorbidity_severity_adjustment(0.5, "moderate")
        assert result == 0.5


class TestRankDiseaseCombinations:

    def test_ranks_descending(self):
        combinations = [
            ("A", "B", 0.3, 0.3),
            ("C", "D", 0.9, 0.9),
            ("E", "F", 0.6, 0.6),
        ]
        ranked = ComorbidityScorer.rank_disease_combinations(combinations)
        scores = [r[2] for r in ranked]
        assert scores == sorted(scores, reverse=True)

    def test_empty_list(self):
        assert ComorbidityScorer.rank_disease_combinations([]) == []

    def test_filters_zero_scores(self):
        combinations = [
            ("A", "B", 0.0, 0.0),  # Should produce 0 combined
        ]
        ranked = ComorbidityScorer.rank_disease_combinations(combinations)
        assert len(ranked) == 0
