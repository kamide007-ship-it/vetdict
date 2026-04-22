"""Tests for multi-disease question generation (Phase 6 Stage 5).

Tests question generation for clinical diagnostic efficiency in
multi-disease scenarios.
"""

import pytest

from api.ai.multidisease_question_generator import (
    DiagnosticQuestion,
    DiscriminativeQuestionRanker,
    MultiDiseaseQuestionGenerator,
    QuestionSequenceOptimizer,
)


class TestDiagnosticQuestion:
    """Test DiagnosticQuestion data structure."""

    def test_diagnostic_question_creation(self):
        """Test creating a DiagnosticQuestion."""
        question = DiagnosticQuestion(
            question_id="q_1",
            question_text_en="Does the patient have pain?",
            question_text_ja="患者は痛みがありますか？",
            question_type="yes_no",
            target_diseases=["Arthritis", "Fracture"],
            discriminative_score=0.75,
            likelihood_ratio_positive=3.0,
            likelihood_ratio_negative=0.3,
            information_gain=0.8,
            clinical_utility="high",
            answer_options=["Yes", "No"],
        )

        assert question.question_id == "q_1"
        assert question.discriminative_score == 0.75
        assert "Arthritis" in question.target_diseases

    def test_diagnostic_question_to_dict(self):
        """Test serialization of DiagnosticQuestion."""
        question = DiagnosticQuestion(
            question_id="q_test",
            question_text_en="Test question?",
            question_text_ja="テスト質問？",
            question_type="yes_no",
            target_diseases=["Disease A"],
            discriminative_score=0.7,
            likelihood_ratio_positive=2.5,
            likelihood_ratio_negative=0.4,
            information_gain=0.6,
            clinical_utility="medium",
        )

        result = question.to_dict()
        assert result["question_id"] == "q_test"
        assert isinstance(result["discriminative_score"], float)
        assert result["clinical_utility"] == "medium"


class TestMultiDiseaseQuestionGenerator:
    """Test multi-disease question generation."""

    @pytest.fixture
    def sample_diseases(self):
        """Sample diseases for testing."""
        return [
            {
                "name": "Hip Dysplasia",
                "symptoms": ["limping", "pain", "reluctance to exercise"],
                "pathophysiology": (
                    "Abnormal hip joint development. Symptoms start early and gradually worsen. "
                    "Pain and limping are primary manifestations."
                ),
                "complications": ["osteoarthritis", "lameness"],
            },
            {
                "name": "Osteoarthritis",
                "symptoms": ["stiffness", "limping", "pain", "reduced movement"],
                "pathophysiology": (
                    "Cartilage degeneration in joints. Symptoms develop gradually over time. "
                    "Morning stiffness is characteristic."
                ),
                "complications": ["chronic pain"],
            },
        ]

    def test_generate_differentiating_question(self, sample_diseases):
        """Test generating a question that differentiates between diseases."""
        question = MultiDiseaseQuestionGenerator.generate_differentiating_question(
            disease_a="Hip Dysplasia",
            disease_b="Osteoarthritis",
            detected_symptoms=["limping"],
            disease_database=sample_diseases,
        )

        assert question is not None
        assert question.question_text_en != ""
        assert question.question_text_ja != ""
        assert "Hip Dysplasia" in question.target_diseases
        assert "Osteoarthritis" in question.target_diseases

    def test_generate_combination_focused_questions(self, sample_diseases):
        """Test generating questions for a disease combination."""
        questions = MultiDiseaseQuestionGenerator.generate_combination_focused_questions(
            diseases=["Hip Dysplasia", "Osteoarthritis"],
            detected_symptoms=["limping", "pain"],
            disease_database=sample_diseases,
        )

        assert len(questions) > 0
        assert all(isinstance(q, DiagnosticQuestion) for q in questions)
        # Questions should target the diseases
        for q in questions:
            assert len(q.target_diseases) > 0

    def test_differentiating_question_discriminative_score(self, sample_diseases):
        """Test that differentiating questions have good discriminative scores."""
        question = MultiDiseaseQuestionGenerator.generate_differentiating_question(
            disease_a="Hip Dysplasia",
            disease_b="Osteoarthritis",
            detected_symptoms=[],
            disease_database=sample_diseases,
        )

        if question:
            # Good differentiating questions should have reasonable scores
            assert 0.0 <= question.discriminative_score <= 1.0
            assert question.information_gain >= 0.0

    def test_likelihood_ratios_reasonable(self, sample_diseases):
        """Test that likelihood ratios are reasonable."""
        question = MultiDiseaseQuestionGenerator.generate_differentiating_question(
            disease_a="Hip Dysplasia",
            disease_b="Osteoarthritis",
            detected_symptoms=[],
            disease_database=sample_diseases,
        )

        if question:
            # LR+ should generally be > 1 (or = 1 for neutral)
            # LR- should generally be < 1 (or = 1 for neutral)
            # Both should be positive
            assert question.likelihood_ratio_positive > 0
            assert question.likelihood_ratio_negative > 0

    def test_clinical_utility_assessment(self, sample_diseases):
        """Test that clinical utility is properly assigned."""
        question = MultiDiseaseQuestionGenerator.generate_differentiating_question(
            disease_a="Hip Dysplasia",
            disease_b="Osteoarthritis",
            detected_symptoms=[],
            disease_database=sample_diseases,
        )

        if question:
            assert question.clinical_utility in ["high", "medium", "low"]

    def test_question_language_support(self, sample_diseases):
        """Test that questions support both English and Japanese."""
        question = MultiDiseaseQuestionGenerator.generate_differentiating_question(
            disease_a="Hip Dysplasia",
            disease_b="Osteoarthritis",
            detected_symptoms=[],
            disease_database=sample_diseases,
        )

        if question:
            # Both language versions should be present
            assert len(question.question_text_en) > 0
            assert len(question.question_text_ja) > 0
            # Should not be identical
            assert question.question_text_en != question.question_text_ja


class TestDiscriminativeQuestionRanker:
    """Test question ranking by discriminative value."""

    @pytest.fixture
    def sample_questions(self):
        """Sample diagnostic questions."""
        return [
            DiagnosticQuestion(
                question_id="q1",
                question_text_en="Is there morning stiffness?",
                question_text_ja="朝のこわばりはありますか？",
                question_type="yes_no",
                target_diseases=["Osteoarthritis"],
                discriminative_score=0.8,
                likelihood_ratio_positive=4.0,
                likelihood_ratio_negative=0.3,
                information_gain=0.85,
                clinical_utility="high",
            ),
            DiagnosticQuestion(
                question_id="q2",
                question_text_en="Did symptoms start suddenly?",
                question_text_ja="症状は急に始まりましたか？",
                question_type="yes_no",
                target_diseases=["Fracture"],
                discriminative_score=0.6,
                likelihood_ratio_positive=2.0,
                likelihood_ratio_negative=0.5,
                information_gain=0.5,
                clinical_utility="medium",
            ),
        ]

    def test_rank_questions_for_combination(self, sample_questions):
        """Test ranking questions for a disease combination."""
        ranked = DiscriminativeQuestionRanker.rank_questions_for_combination(
            diseases=["Osteoarthritis", "Fracture"],
            candidate_questions=sample_questions,
            detected_symptoms=["pain"],
        )

        assert len(ranked) == len(sample_questions)
        # First element should be (question, score, explanation)
        assert len(ranked[0]) == 3

    def test_ranked_questions_ordered_by_score(self, sample_questions):
        """Test that questions are ordered by score."""
        ranked = DiscriminativeQuestionRanker.rank_questions_for_combination(
            diseases=["Osteoarthritis"],
            candidate_questions=sample_questions,
            detected_symptoms=[],
        )

        # Questions should be sorted by score descending
        scores = [score for _, score, _ in ranked]
        assert scores == sorted(scores, reverse=True)

    def test_ranking_includes_explanation(self, sample_questions):
        """Test that rankings include explanation strings."""
        ranked = DiscriminativeQuestionRanker.rank_questions_for_combination(
            diseases=["Osteoarthritis"],
            candidate_questions=sample_questions,
            detected_symptoms=[],
        )

        for _, _, explanation in ranked:
            assert isinstance(explanation, str)
            assert len(explanation) > 0
            assert "utility" in explanation.lower()


class TestQuestionSequenceOptimizer:
    """Test optimization of question sequences."""

    @pytest.fixture
    def sample_questions(self):
        """Sample diagnostic questions."""
        return [
            DiagnosticQuestion(
                question_id="q1",
                question_text_en="Q1?",
                question_text_ja="Q1？",
                question_type="yes_no",
                target_diseases=["Disease A"],
                information_gain=0.8,
                likelihood_ratio_positive=5.0,
                likelihood_ratio_negative=0.2,
            ),
            DiagnosticQuestion(
                question_id="q2",
                question_text_en="Q2?",
                question_text_ja="Q2？",
                question_type="yes_no",
                target_diseases=["Disease B"],
                information_gain=0.7,
                likelihood_ratio_positive=3.0,
                likelihood_ratio_negative=0.4,
            ),
            DiagnosticQuestion(
                question_id="q3",
                question_text_en="Q3?",
                question_text_ja="Q3？",
                question_type="yes_no",
                target_diseases=["Disease C"],
                information_gain=0.5,
                likelihood_ratio_positive=2.0,
                likelihood_ratio_negative=0.6,
            ),
        ]

    def test_optimize_question_sequence(self, sample_questions):
        """Test optimizing question sequence."""
        optimized = QuestionSequenceOptimizer.optimize_question_sequence(
            initial_questions=sample_questions,
            disease_confidences={"Disease A": 0.6, "Disease B": 0.5, "Disease C": 0.4},
        )

        assert len(optimized) <= len(sample_questions)
        assert all(isinstance(q, DiagnosticQuestion) for q in optimized)

    def test_optimized_sequence_prioritizes_high_gain(self, sample_questions):
        """Test that optimization prioritizes high information gain."""
        optimized = QuestionSequenceOptimizer.optimize_question_sequence(
            initial_questions=sample_questions,
            disease_confidences={"Disease A": 0.6, "Disease B": 0.5, "Disease C": 0.4},
        )

        if len(optimized) > 0:
            # First question should have high information gain
            first_gain = optimized[0].information_gain
            # Should be at least as good as average
            average_gain = sum(q.information_gain for q in sample_questions) / len(sample_questions)
            assert first_gain >= average_gain * 0.8

    def test_optimized_sequence_limits_length(self, sample_questions):
        """Test that optimized sequence is limited to reasonable length."""
        optimized = QuestionSequenceOptimizer.optimize_question_sequence(
            initial_questions=sample_questions,
            disease_confidences={},
        )

        # Should limit to 5 questions max
        assert len(optimized) <= 5


class TestQuestionGenerationEdgeCases:
    """Test edge cases in question generation."""

    def test_generate_question_with_empty_disease_db(self):
        """Test generating question with empty database."""
        question = MultiDiseaseQuestionGenerator.generate_differentiating_question(
            disease_a="Unknown Disease",
            disease_b="Another Unknown",
            detected_symptoms=[],
            disease_database=[],
        )

        # Should handle gracefully
        assert question is None or isinstance(question, DiagnosticQuestion)

    def test_generate_question_single_disease(self):
        """Test generating questions with single disease."""
        questions = MultiDiseaseQuestionGenerator.generate_combination_focused_questions(
            diseases=["Single Disease"],
            detected_symptoms=[],
            disease_database=[{"name": "Single Disease", "symptoms": ["symptom1"]}],
        )

        # Should return empty list for single disease
        assert len(questions) == 0

    def test_rank_questions_empty_list(self):
        """Test ranking empty question list."""
        ranked = DiscriminativeQuestionRanker.rank_questions_for_combination(
            diseases=["Disease A"],
            candidate_questions=[],
            detected_symptoms=[],
        )

        assert ranked == []
