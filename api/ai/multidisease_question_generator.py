"""Multi-disease question generation for complex diagnosis scenarios.

Generates clinically effective questions that can distinguish between
multiple disease hypotheses simultaneously.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple
import logging
import math

logger = logging.getLogger(__name__)


@dataclass
class DiagnosticQuestion:
    """Represents a diagnostic question."""

    question_id: str
    question_text_en: str
    question_text_ja: str
    question_type: str  # "yes_no", "multiple_choice", "severity", "timeline"
    target_diseases: List[str] = field(default_factory=list)
    discriminative_score: float = 0.0
    likelihood_ratio_positive: float = 1.0
    likelihood_ratio_negative: float = 1.0
    information_gain: float = 0.0
    clinical_utility: str = ""  # "high", "medium", "low"
    answer_options: List[str] = field(default_factory=list)

    def to_dict(self):
        """Serialize to dictionary."""
        return {
            "question_id": self.question_id,
            "question_text_en": self.question_text_en,
            "question_text_ja": self.question_text_ja,
            "question_type": self.question_type,
            "target_diseases": self.target_diseases,
            "discriminative_score": round(self.discriminative_score, 3),
            "likelihood_ratio_positive": round(self.likelihood_ratio_positive, 3),
            "likelihood_ratio_negative": round(self.likelihood_ratio_negative, 3),
            "information_gain": round(self.information_gain, 3),
            "clinical_utility": self.clinical_utility,
            "answer_options": self.answer_options,
        }


class MultiDiseaseQuestionGenerator:
    """Generates questions for multi-disease diagnosis scenarios."""

    # Likelihood ratio thresholds (diagnostic utility)
    HIGH_LR_PLUS = 10.0  # Very useful to rule in disease
    MODERATE_LR_PLUS = 2.0
    HIGH_LR_MINUS = 0.1  # Very useful to rule out disease
    MODERATE_LR_MINUS = 0.5

    # Question templates for common clinical scenarios
    SYMPTOM_TIMING_TEMPLATES = [
        ("When did {symptom} start?", "{symptom}はいつから始まりましたか？"),
        ("How long has {symptom} been present?", "{symptom}はどのくらい続いていますか？"),
        ("Did {symptom} start suddenly or gradually?", "{symptom}は急に始まりましたか、それとも徐々に始まりましたか？"),
    ]

    SYMPTOM_SEVERITY_TEMPLATES = [
        ("On a scale of 1-10, how severe is {symptom}?", "1～10のスケールで、{symptom}の重症度はどの程度ですか？"),
        ("Is the {symptom} constant or intermittent?", "{symptom}は常にありますか、それとも間欠的ですか？"),
        ("Is the {symptom} worsening, stable, or improving?", "{symptom}は悪化していますか、安定していますか、それとも改善していますか？"),
    ]

    SYMPTOM_CHARACTER_TEMPLATES = [
        ("Describe the character of {symptom} (e.g., sharp, dull, cramping)", "{symptom}の性状を説明してください（例：鋭い、鈍い、けいれん性）"),
        ("Is there {related_finding} accompanying {symptom}?", "{symptom}に伴い{related_finding}がありますか？"),
        ("What triggers or worsens {symptom}?", "{symptom}のトリガーまたは悪化させるものは何ですか？"),
    ]

    CONTEXTUAL_TEMPLATES = [
        ("Has the animal had {medical_event} recently?", "ペットは最近{medical_event}を経験しましたか？"),
        ("Are there other animals in the household with similar symptoms?", "家族内に似たような症状のある他の動物がいますか？"),
        ("Any recent changes in diet or environment?", "食事や環境に最近の変化がありますか？"),
    ]

    @classmethod
    def generate_differentiating_question(
        cls,
        disease_a: str,
        disease_b: str,
        detected_symptoms: List[str],
        disease_database: List[Dict[str, Any]],
    ) -> Optional[DiagnosticQuestion]:
        """
        Generate a question that differentiates between two diseases.

        Args:
            disease_a: First disease to differentiate
            disease_b: Second disease to differentiate
            detected_symptoms: Currently detected symptoms
            disease_database: Disease information database

        Returns:
            DiagnosticQuestion or None if no good question found
        """

        # Find key differentiating features
        diff_features = cls._find_differentiating_features(
            disease_a, disease_b, disease_database
        )

        if not diff_features:
            return None

        # Pick most discriminative feature
        best_feature = max(
            diff_features,
            key=lambda x: abs(x["lr_positive"] - x["lr_negative"]),
        )

        # Generate question from feature
        question = cls._create_question_from_feature(
            best_feature, disease_a, disease_b
        )

        return question

    @classmethod
    def generate_combination_focused_questions(
        cls,
        diseases: List[str],
        detected_symptoms: List[str],
        disease_database: List[Dict[str, Any]],
    ) -> List[DiagnosticQuestion]:
        """
        Generate questions specifically for a disease combination.

        Args:
            diseases: List of diseases in the combination
            detected_symptoms: Currently detected symptoms
            disease_database: Disease database

        Returns:
            List of DiagnosticQuestion ordered by discriminative value
        """
        questions = []

        if len(diseases) < 2:
            return questions

        # Generate pairwise differentiating questions
        for i, disease_a in enumerate(diseases):
            for disease_b in diseases[i + 1 :]:
                q = cls.generate_differentiating_question(
                    disease_a,
                    disease_b,
                    detected_symptoms,
                    disease_database,
                )
                if q:
                    questions.append(q)

        # Sort by discriminative value
        questions.sort(key=lambda q: q.discriminative_score, reverse=True)

        return questions[:5]  # Top 5 questions

    @classmethod
    def _find_differentiating_features(
        cls,
        disease_a: str,
        disease_b: str,
        disease_database: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Find features that differentiate two diseases.

        Returns list of {feature, disease_a_rate, disease_b_rate, lr_positive, lr_negative}
        """

        # Get disease records
        record_a = next(
            (d for d in disease_database if d.get("name") == disease_a),
            None,
        )
        record_b = next(
            (d for d in disease_database if d.get("name") == disease_b),
            None,
        )

        if not record_a or not record_b:
            return []

        features = []

        # Compare symptoms
        symptoms_a = set(str(s).lower() for s in record_a.get("symptoms", []))
        symptoms_b = set(str(s).lower() for s in record_b.get("symptoms", []))

        # Unique to A
        unique_a = symptoms_a - symptoms_b
        for symptom in list(unique_a)[:3]:
            lr_pos = 5.0  # Presence in A, absence in B
            lr_neg = 0.5
            features.append(
                {
                    "feature": symptom,
                    "type": "symptom",
                    "disease_a_rate": 0.8,
                    "disease_b_rate": 0.1,
                    "lr_positive": lr_pos,
                    "lr_negative": lr_neg,
                }
            )

        # Unique to B
        unique_b = symptoms_b - symptoms_a
        for symptom in list(unique_b)[:3]:
            lr_pos = 5.0
            lr_neg = 0.5
            features.append(
                {
                    "feature": symptom,
                    "type": "symptom",
                    "disease_a_rate": 0.1,
                    "disease_b_rate": 0.8,
                    "lr_positive": lr_pos,
                    "lr_negative": lr_neg,
                }
            )

        # Onset characteristics
        patho_a = record_a.get("pathophysiology", "").lower()
        patho_b = record_b.get("pathophysiology", "").lower()

        if "sudden" in patho_a and "gradual" in patho_b:
            features.append(
                {
                    "feature": "onset_sudden",
                    "type": "timing",
                    "disease_a_rate": 0.7,
                    "disease_b_rate": 0.2,
                    "lr_positive": 3.5,
                    "lr_negative": 0.4,
                }
            )

        return features

    @classmethod
    def _create_question_from_feature(
        cls,
        feature: Dict[str, Any],
        disease_a: str,
        disease_b: str,
    ) -> DiagnosticQuestion:
        """Create a question from a differentiating feature."""

        feature_name = feature.get("feature", "")
        feature_type = feature.get("type", "symptom")
        lr_pos = feature.get("lr_positive", 2.0)
        lr_neg = feature.get("lr_negative", 0.5)

        # Generate question text
        if feature_type == "timing":
            question_en = "Did the symptoms start suddenly?"
            question_ja = "症状は急に始まりましたか？"
            options = ["Yes", "No", "Gradually"]
        elif feature_type == "severity":
            question_en = f"How severe is the {feature_name}?"
            question_ja = f"{feature_name}の重症度はどの程度ですか？"
            options = ["Mild", "Moderate", "Severe"]
        else:  # symptom
            question_en = f"Has the patient experienced {feature_name}?"
            question_ja = f"患者は{feature_name}を経験しましたか？"
            options = ["Yes", "No"]

        # Calculate discriminative score
        discriminative_score = cls._calculate_discriminative_value(lr_pos, lr_neg)

        # Calculate information gain
        information_gain = cls._calculate_information_gain(lr_pos, lr_neg)

        # Determine clinical utility
        if lr_pos > cls.HIGH_LR_PLUS or lr_neg < cls.HIGH_LR_MINUS:
            utility = "high"
        elif lr_pos > cls.MODERATE_LR_PLUS or lr_neg < cls.MODERATE_LR_MINUS:
            utility = "medium"
        else:
            utility = "low"

        question = DiagnosticQuestion(
            question_id=f"q_diff_{disease_a}_{disease_b}",
            question_text_en=question_en,
            question_text_ja=question_ja,
            question_type="yes_no" if len(options) == 2 else "multiple_choice",
            target_diseases=[disease_a, disease_b],
            discriminative_score=discriminative_score,
            likelihood_ratio_positive=lr_pos,
            likelihood_ratio_negative=lr_neg,
            information_gain=information_gain,
            clinical_utility=utility,
            answer_options=options,
        )

        return question

    @staticmethod
    def _calculate_discriminative_value(lr_positive: float, lr_negative: float) -> float:
        """
        Calculate discriminative value using likelihood ratios.

        High LR+ (>10) or low LR- (<0.1) = high discriminative value
        """
        # Normalize and combine LRs
        normalized_lr_pos = min(lr_positive / 10.0, 1.0)  # 0-1 range
        normalized_lr_neg = min(1.0 - (lr_negative / 0.1), 1.0) if lr_negative > 0 else 1.0

        discriminative = (normalized_lr_pos + normalized_lr_neg) / 2.0
        return min(1.0, max(0.0, discriminative))

    @staticmethod
    def _calculate_information_gain(lr_positive: float, lr_negative: float) -> float:
        """
        Calculate information gain (entropy reduction).

        Based on Shannon entropy and diagnostic likelihood ratio.
        """
        if lr_positive <= 0 or lr_negative <= 0:
            return 0.0

        # Information in bits
        info_gain = math.log2(lr_positive) if lr_positive > 1 else 0.0
        info_gain += math.log2(1.0 / lr_negative) if lr_negative < 1 else 0.0

        # Normalize to 0-1
        normalized_gain = min(1.0, max(0.0, info_gain / 10.0))
        return normalized_gain


class DiscriminativeQuestionRanker:
    """Ranks questions by discriminative value for disease combinations."""

    @classmethod
    def rank_questions_for_combination(
        cls,
        diseases: List[str],
        candidate_questions: List[DiagnosticQuestion],
        detected_symptoms: List[str],
    ) -> List[Tuple[DiagnosticQuestion, float, str]]:
        """
        Rank questions for a specific disease combination.

        Args:
            diseases: Target diseases
            candidate_questions: Candidate questions
            detected_symptoms: Current symptoms

        Returns:
            List of (question, score, explanation) sorted by score
        """
        ranked = []

        for question in candidate_questions:
            # Calculate ranking score
            score = cls._calculate_ranking_score(
                question=question,
                diseases=diseases,
                detected_symptoms=detected_symptoms,
            )

            explanation = cls._explain_ranking(question, score)

            ranked.append((question, score, explanation))

        # Sort by score descending
        ranked.sort(key=lambda x: x[1], reverse=True)

        return ranked

    @staticmethod
    def _calculate_ranking_score(
        question: DiagnosticQuestion,
        diseases: List[str],
        detected_symptoms: List[str],
    ) -> float:
        """
        Calculate ranking score for a question.

        Considers discriminative value, information gain, and target disease relevance.
        """

        # Base score from discriminative value
        score = question.discriminative_score * 0.5

        # Add information gain
        score += question.information_gain * 0.3

        # Bonus if targets current disease focus
        target_match = sum(
            1 for d in question.target_diseases if d in diseases
        )
        score += (target_match / max(len(question.target_diseases), 1)) * 0.2

        return min(1.0, max(0.0, score))

    @staticmethod
    def _explain_ranking(question: DiagnosticQuestion, score: float) -> str:
        """Generate explanation for ranking."""
        if score > 0.8:
            return f"Highly discriminative: {question.clinical_utility} utility"
        elif score > 0.6:
            return f"Moderately discriminative: {question.clinical_utility} utility"
        else:
            return f"Low discriminative value: {question.clinical_utility} utility"


class QuestionSequenceOptimizer:
    """Optimizes the sequence of questions for multi-disease diagnosis."""

    @classmethod
    def optimize_question_sequence(
        cls,
        initial_questions: List[DiagnosticQuestion],
        disease_confidences: Dict[str, float],
    ) -> List[DiagnosticQuestion]:
        """
        Optimize question sequence for maximum diagnostic efficiency.

        Args:
            initial_questions: Available questions
            disease_confidences: Current disease confidence scores

        Returns:
            Optimized question sequence
        """

        optimized = []
        remaining = initial_questions.copy()

        while remaining and len(optimized) < 5:
            # Select question that maximizes information gain
            best_question = max(
                remaining,
                key=lambda q: cls._calculate_expected_gain(q, disease_confidences),
                default=None,
            )

            if best_question:
                optimized.append(best_question)
                remaining.remove(best_question)

        return optimized

    @staticmethod
    def _calculate_expected_gain(
        question: DiagnosticQuestion,
        disease_confidences: Dict[str, float],
    ) -> float:
        """
        Calculate expected information gain from asking a question.

        High gain if question can significantly change disease probabilities.
        """
        if not disease_confidences:
            return question.information_gain

        # For each possible answer, calculate new confidence
        max_gain = 0.0

        for target_disease in question.target_diseases:
            current_conf = disease_confidences.get(target_disease, 0.5)

            # Simulate positive answer
            new_conf_pos = min(1.0, current_conf * question.likelihood_ratio_positive)
            gain_pos = abs(new_conf_pos - current_conf)

            # Simulate negative answer
            new_conf_neg = max(0.0, current_conf * question.likelihood_ratio_negative)
            gain_neg = abs(new_conf_neg - current_conf)

            max_gain = max(max_gain, gain_pos, gain_neg)

        return max_gain
