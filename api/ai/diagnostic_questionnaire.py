"""Diagnostic questionnaire engine for step-by-step disease narrowing.

Generates yes/no follow-up questions to efficiently narrow down differential diagnosis
candidates based on the current disease matches and symptom set.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


@dataclass
class DiagnosticQuestion:
    """Represents a single diagnostic follow-up question."""

    id: str
    question_ja: str
    question_en: str
    question_type: str  # "binary", "multiselect", "numeric"
    priority: int  # 1=highest priority
    options: List[Dict[str, str]]  # {value, label_ja, label_en}
    disease_targets: List[str]  # Diseases this helps differentiate
    reasoning_ja: str  # Why ask this question
    reasoning_en: str


class DiagnosticQuestionnaireEngine:
    """Generates targeted diagnostic questions to narrow down disease list."""

    # Question templates database
    QUESTION_TEMPLATES = {
        # Gastrointestinal
        "vomiting_frequency": {
            "question_ja": "嘔吐は1日に何回ですか？",
            "question_en": "How often does vomiting occur per day?",
            "question_type": "multiselect",
            "options": [
                {"value": "once", "label_ja": "1回", "label_en": "1 time"},
                {"value": "2_to_3", "label_ja": "2～3回", "label_en": "2-3 times"},
                {"value": "frequent", "label_ja": "3回以上/継続的", "label_en": "3+ times/continuous"},
            ],
            "disease_targets": [
                "Gastric Dilatation-Volvulus (GDV/Bloat)",
                "Canine Parvovirus",
                "Pancreatitis",
            ],
        },
        "blood_in_vomit": {
            "question_ja": "嘔吐物に血液が含まれていますか？",
            "question_en": "Is there blood in the vomit?",
            "question_type": "binary",
            "options": [
                {"value": "yes", "label_ja": "はい", "label_en": "Yes"},
                {"value": "no", "label_ja": "いいえ", "label_en": "No"},
            ],
            "disease_targets": [
                "Canine Parvovirus",
                "Hemorrhagic Gastroenteritis (HGE)",
            ],
        },
        "diarrhea_consistency": {
            "question_ja": "下痢の性状は？",
            "question_en": "What is the stool consistency?",
            "question_type": "multiselect",
            "options": [
                {"value": "watery", "label_ja": "水様便", "label_en": "Watery"},
                {"value": "soft", "label_ja": "軟便", "label_en": "Soft"},
                {"value": "bloody", "label_ja": "血液混在", "label_en": "Bloody"},
            ],
            "disease_targets": [
                "Canine Parvovirus",
                "Inflammatory Bowel Disease (IBD)",
                "Intestinal Parasites",
            ],
        },
        # Respiratory
        "cough_type": {
            "question_ja": "咳の性質は？",
            "question_en": "What type of cough?",
            "question_type": "multiselect",
            "options": [
                {"value": "dry", "label_ja": "乾性", "label_en": "Dry"},
                {"value": "wet", "label_ja": "湿性", "label_en": "Wet"},
                {"value": "honking", "label_ja": "アザラシのような", "label_en": "Honking"},
            ],
            "disease_targets": [
                "Tracheal Collapse",
                "Pneumonia",
                "Heart Disease/CHF",
            ],
        },
        # Urinary
        "urine_color": {
            "question_ja": "尿の色は？",
            "question_en": "What is the urine color?",
            "question_type": "multiselect",
            "options": [
                {"value": "normal", "label_ja": "正常", "label_en": "Normal"},
                {"value": "dark", "label_ja": "濃い/茶色", "label_en": "Dark/brown"},
                {"value": "red", "label_ja": "赤い", "label_en": "Red/pink"},
            ],
            "disease_targets": [
                "Bladder Stones",
                "Urinary Tract Infection",
                "Hemolytic Anemia",
            ],
        },
        # Systemic
        "onset_timeline": {
            "question_ja": "症状の発症はいつですか？",
            "question_en": "When did symptoms start?",
            "question_type": "multiselect",
            "options": [
                {"value": "acute_24h", "label_ja": "急発（24時間以内）", "label_en": "Acute (< 24h)"},
                {"value": "subacute", "label_ja": "亜急性（数日）", "label_en": "Subacute (days)"},
                {"value": "chronic", "label_ja": "慢性（数週間以上）", "label_en": "Chronic (weeks+)"},
            ],
            "disease_targets": [
                "Canine Parvovirus",
                "Pancreatitis",
                "Kidney Disease (CKD)",
            ],
        },
        "vaccine_status": {
            "question_ja": "予防接種は最新ですか？",
            "question_en": "Are vaccinations current?",
            "question_type": "binary",
            "options": [
                {"value": "yes", "label_ja": "はい（最新）", "label_en": "Yes (current)"},
                {"value": "no", "label_ja": "いいえ（古い/未実施）", "label_en": "No (outdated/none)"},
            ],
            "disease_targets": [
                "Canine Parvovirus",
                "Feline Panleukopenia",
            ],
        },
        "fever_present": {
            "question_ja": "体温は上昇していますか？（38.5°C以上）",
            "question_en": "Is body temperature elevated (> 38.5°C / 101.3°F)?",
            "question_type": "binary",
            "options": [
                {"value": "yes", "label_ja": "はい", "label_en": "Yes"},
                {"value": "no", "label_ja": "いいえ", "label_en": "No"},
            ],
            "disease_targets": [
                "Infection",
                "Meningitis",
                "Pyometra",
            ],
        },
    }

    @classmethod
    def generate_questions(
        cls,
        suspected_diseases: List[Dict[str, Any]],
        symptoms: List[str],
        limit: int = 3,
    ) -> List[DiagnosticQuestion]:
        """
        Generate the next diagnostic questions to narrow down disease list.

        Args:
            suspected_diseases: List of current suspected disease matches
            symptoms: Currently detected symptoms
            limit: Maximum number of questions to return

        Returns:
            List of prioritized diagnostic questions
        """
        if not suspected_diseases or len(suspected_diseases) <= 1:
            return []

        # Extract disease names from top candidates
        top_diseases = set(d.get("name", "") for d in suspected_diseases[:5])

        # Find questions that differentiate between top candidates
        candidate_questions = []
        for q_id, q_data in cls.QUESTION_TEMPLATES.items():
            # Calculate how useful this question is
            targets = set(q_data.get("disease_targets", []))

            # Find diseases in top candidates that this question targets
            covered_diseases = top_diseases & targets
            uncovered_diseases = top_diseases - targets

            # Score: prefer questions that split the candidates
            if covered_diseases and uncovered_diseases:
                coverage_score = len(covered_diseases) / len(top_diseases)
                priority = int(coverage_score * 100)  # Higher score = higher priority

                candidate_questions.append({
                    "id": q_id,
                    "priority": priority,
                    "coverage": len(covered_diseases),
                    "q_data": q_data,
                })

        # Sort by priority (descending) and return top N
        candidate_questions.sort(key=lambda x: x["priority"], reverse=True)

        questions = []
        for item in candidate_questions[:limit]:
            q_data = item["q_data"]
            question = DiagnosticQuestion(
                id=item["id"],
                question_ja=q_data["question_ja"],
                question_en=q_data["question_en"],
                question_type=q_data["question_type"],
                priority=item["priority"],
                options=q_data["options"],
                disease_targets=q_data["disease_targets"],
                reasoning_ja=f"この質問は{item['coverage']}個の候補疾患を絞り込むのに役立ちます。",
                reasoning_en=f"This question helps narrow down {item['coverage']} candidate diseases.",
            )
            questions.append(question)

        return questions

    @classmethod
    def update_diseases_from_answer(
        cls,
        suspected_diseases: List[Dict[str, Any]],
        question_id: str,
        answer: str,
    ) -> List[Dict[str, Any]]:
        """
        Update disease matches based on answer to a diagnostic question.

        Args:
            suspected_diseases: Current disease list
            question_id: ID of answered question
            answer: User's answer value

        Returns:
            Updated disease list with adjusted confidences
        """
        if question_id not in cls.QUESTION_TEMPLATES:
            return suspected_diseases

        q_data = cls.QUESTION_TEMPLATES[question_id]
        target_diseases = set(q_data.get("disease_targets", []))

        # Apply confidence adjustments based on answer
        adjustment_factor = cls._get_adjustment_factor(question_id, answer)

        updated = []
        for disease in suspected_diseases:
            disease_copy = disease.copy()
            disease_name = disease_copy.get("name", "")

            if disease_name in target_diseases:
                # Apply adjustment to target diseases
                original_confidence = disease_copy.get("match_percent", 0)
                disease_copy["match_percent"] = int(original_confidence * adjustment_factor)

            updated.append(disease_copy)

        # Re-sort by match_percent
        updated.sort(key=lambda d: d.get("match_percent", 0), reverse=True)

        return updated

    @staticmethod
    def _get_adjustment_factor(question_id: str, answer: str) -> float:
        """
        Get confidence adjustment factor based on answer.

        Typically:
        - answer = "yes" → factor = 1.3 (increase confidence)
        - answer = "no" → factor = 0.7 (decrease confidence)
        """
        if answer == "yes":
            return 1.3
        elif answer == "no":
            return 0.7
        else:
            return 1.0  # Neutral for other answers


def build_next_question_response(
    suspected_diseases: List[Dict[str, Any]],
    symptoms: List[str],
    question_limit: int = 3,
) -> Dict[str, Any]:
    """
    Build complete response for next diagnostic questions.

    Returns API response object with questions and metadata.
    """
    engine = DiagnosticQuestionnaireEngine()
    questions = engine.generate_questions(
        suspected_diseases,
        symptoms,
        limit=question_limit,
    )

    # Convert to serializable format
    serialized_questions = []
    for q in questions:
        serialized_questions.append({
            "id": q.id,
            "question_ja": q.question_ja,
            "question_en": q.question_en,
            "type": q.question_type,
            "options": q.options,
            "priority": q.priority,
            "targets": q.disease_targets,
            "reasoning_ja": q.reasoning_ja,
            "reasoning_en": q.reasoning_en,
        })

    remaining_candidates = len(suspected_diseases)
    estimated_next_questions = max(0, (remaining_candidates - 1) // 2)

    return {
        "next_questions": serialized_questions,
        "question_count": len(serialized_questions),
        "current_candidates": remaining_candidates,
        "estimated_next_questions": estimated_next_questions,
        "recommendation_ja": (
            f"あと{estimated_next_questions}～{estimated_next_questions + 1}回の質問で"
            "候補を3つまで絞り込める可能性があります。"
        ),
        "recommendation_en": (
            f"About {estimated_next_questions}-{estimated_next_questions + 1} more questions "
            "may narrow candidates down to ~3 diseases."
        ),
    }
