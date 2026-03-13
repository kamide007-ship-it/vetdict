"""Diagnostic session management with state tracking and Bayesian updates.

Maintains conversation state across multiple question-answer rounds,
enabling adaptive questioning and progressive disease narrowing.
"""

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional, Set
from datetime import datetime
import json
import logging
import uuid

logger = logging.getLogger(__name__)


@dataclass
class DiagnosticSession:
    """Represents a single diagnostic conversation session."""

    session_id: str
    animal_species: str = "dog"
    symptom_ids: List[str] = field(default_factory=list)
    detected_symptoms_ja: Optional[str] = None
    detected_symptoms_en: Optional[str] = None

    # Disease tracking
    initial_candidates: List[Dict[str, Any]] = field(default_factory=list)
    current_candidates: List[Dict[str, Any]] = field(default_factory=list)

    # Question-answer history
    asked_questions: List[str] = field(default_factory=list)
    answers: Dict[str, str] = field(default_factory=dict)
    answer_timestamps: Dict[str, float] = field(default_factory=dict)

    # Session metadata
    user_language: str = "en"  # "en" or "ja"
    created_at: Optional[str] = None
    last_updated_at: Optional[str] = None
    round_number: int = 0
    confidence_threshold: float = 0.7  # Confidence to stop asking

    # Optional context
    breed: Optional[str] = None
    age_years: Optional[float] = None
    gender: Optional[str] = None
    vaccination_status: Optional[str] = None

    def __post_init__(self):
        """Initialize timestamps."""
        if not self.session_id:
            self.session_id = str(uuid.uuid4())
        if not self.created_at:
            now = datetime.utcnow().isoformat()
            self.created_at = now
            self.last_updated_at = now

    @classmethod
    def from_api_request(
        cls,
        symptoms: List[str],
        suspected_diseases: List[Dict[str, Any]],
        detected_symptoms_ja: Optional[str] = None,
        detected_symptoms_en: Optional[str] = None,
        species: str = "dog",
        user_language: str = "en",
        breed: Optional[str] = None,
        age_years: Optional[float] = None,
        gender: Optional[str] = None,
        vaccination_status: Optional[str] = None,
    ) -> "DiagnosticSession":
        """
        Create session from API request parameters.

        Args:
            symptoms: List of symptom IDs
            suspected_diseases: Initial disease candidates
            detected_symptoms_ja: Japanese description
            detected_symptoms_en: English description
            species: Animal species
            user_language: "en" or "ja"
            breed: Optional breed
            age_years: Optional age
            gender: Optional gender
            vaccination_status: Optional vaccination status

        Returns:
            DiagnosticSession instance
        """
        session = cls(
            session_id="",  # Will be auto-generated
            animal_species=species,
            symptom_ids=symptoms,
            detected_symptoms_ja=detected_symptoms_ja,
            detected_symptoms_en=detected_symptoms_en,
            initial_candidates=suspected_diseases.copy(),
            current_candidates=suspected_diseases.copy(),
            user_language=user_language,
            breed=breed,
            age_years=age_years,
            gender=gender,
            vaccination_status=vaccination_status,
        )
        return session

    def add_question_answer(
        self,
        question_id: str,
        answer: str,
    ) -> None:
        """
        Record a question-answer pair in this session.

        Args:
            question_id: ID of the asked question
            answer: User's answer to the question
        """
        import time

        self.asked_questions.append(question_id)
        self.answers[question_id] = answer
        self.answer_timestamps[question_id] = time.time()
        self.last_updated_at = datetime.utcnow().isoformat()
        self.round_number += 1

    def update_candidates(
        self,
        updated_candidates: List[Dict[str, Any]],
    ) -> None:
        """
        Update the current disease candidates after an answer.

        Args:
            updated_candidates: New disease list with updated scores
        """
        self.current_candidates = updated_candidates.copy()
        self.last_updated_at = datetime.utcnow().isoformat()

    def should_continue_questioning(self) -> bool:
        """
        Determine if we should ask more questions.

        Returns:
            True if should ask more, False if should stop
        """
        if not self.current_candidates:
            return False

        # Check if top candidate exceeds confidence threshold
        top_match = max(
            (d.get("match_percent", 0) / 100.0)
            for d in self.current_candidates
        )

        if top_match >= self.confidence_threshold:
            return False

        # Check if there's significant ambiguity
        if len(self.current_candidates) <= 1:
            return False

        # Ask at most 10 questions
        if self.round_number >= 10:
            return False

        return True

    def get_diagnosis_summary(self) -> Dict[str, Any]:
        """
        Get current diagnosis summary.

        Returns:
            {top_disease, confidence, alternatives, ...}
        """
        if not self.current_candidates:
            return {
                "top_disease": None,
                "confidence": 0.0,
                "alternatives": [],
            }

        # Sort by match_percent
        sorted_candidates = sorted(
            self.current_candidates,
            key=lambda d: d.get("match_percent", 0),
            reverse=True,
        )

        top = sorted_candidates[0] if sorted_candidates else None
        alternatives = sorted_candidates[1:4] if len(sorted_candidates) > 1 else []

        return {
            "top_disease": top.get("name") if top else None,
            "top_disease_ja": top.get("name_ja") if top else None,
            "confidence_percent": top.get("match_percent", 0) if top else 0,
            "confidence": (top.get("match_percent", 0) / 100.0) if top else 0.0,
            "alternatives": [
                {
                    "name": a.get("name", ""),
                    "name_ja": a.get("name_ja", ""),
                    "match_percent": a.get("match_percent", 0),
                }
                for a in alternatives
            ],
            "total_candidates": len(self.current_candidates),
            "rounds_asked": self.round_number,
        }

    def to_dict(self) -> Dict[str, Any]:
        """Serialize session to dict."""
        return {
            "session_id": self.session_id,
            "animal_species": self.animal_species,
            "symptom_ids": self.symptom_ids,
            "detected_symptoms_ja": self.detected_symptoms_ja,
            "detected_symptoms_en": self.detected_symptoms_en,
            "user_language": self.user_language,
            "created_at": self.created_at,
            "last_updated_at": self.last_updated_at,
            "round_number": self.round_number,
            "asked_questions": self.asked_questions,
            "answers": self.answers,
            "breed": self.breed,
            "age_years": self.age_years,
            "gender": self.gender,
            "vaccination_status": self.vaccination_status,
            "current_candidates_count": len(self.current_candidates),
            "diagnosis_summary": self.get_diagnosis_summary(),
        }

    def to_json(self) -> str:
        """Serialize session to JSON."""
        return json.dumps(self.to_dict(), default=str)

    @classmethod
    def from_json(cls, json_str: str) -> Optional["DiagnosticSession"]:
        """
        Deserialize session from JSON.

        Note: full reconstruction requires candidate data from API.
        This creates a minimal session for display purposes.
        """
        try:
            data = json.loads(json_str)
            session = cls(
                session_id=data.get("session_id", ""),
                animal_species=data.get("animal_species", "dog"),
                symptom_ids=data.get("symptom_ids", []),
                detected_symptoms_ja=data.get("detected_symptoms_ja"),
                detected_symptoms_en=data.get("detected_symptoms_en"),
                user_language=data.get("user_language", "en"),
                breed=data.get("breed"),
                age_years=data.get("age_years"),
                gender=data.get("gender"),
                vaccination_status=data.get("vaccination_status"),
            )
            session.created_at = data.get("created_at")
            session.last_updated_at = data.get("last_updated_at")
            session.round_number = data.get("round_number", 0)
            session.asked_questions = data.get("asked_questions", [])
            session.answers = data.get("answers", {})
            return session
        except Exception as e:
            logger.error(f"Failed to deserialize diagnostic session: {e}")
            return None


class DiagnosticSessionManager:
    """Manages diagnostic sessions (factory and storage)."""

    # In-memory session cache (would use Redis in production)
    _sessions: Dict[str, DiagnosticSession] = {}

    @classmethod
    def create_session(
        cls,
        symptoms: List[str],
        suspected_diseases: List[Dict[str, Any]],
        **kwargs,
    ) -> DiagnosticSession:
        """Create and store a new diagnostic session."""
        session = DiagnosticSession.from_api_request(
            symptoms=symptoms,
            suspected_diseases=suspected_diseases,
            **kwargs,
        )
        cls._sessions[session.session_id] = session
        return session

    @classmethod
    def get_session(cls, session_id: str) -> Optional[DiagnosticSession]:
        """Retrieve a session by ID."""
        return cls._sessions.get(session_id)

    @classmethod
    def update_session(
        cls,
        session_id: str,
        question_id: str,
        answer: str,
        updated_candidates: Optional[List[Dict[str, Any]]] = None,
    ) -> Optional[DiagnosticSession]:
        """Update session with new answer."""
        session = cls.get_session(session_id)
        if not session:
            return None

        session.add_question_answer(question_id, answer)
        if updated_candidates:
            session.update_candidates(updated_candidates)

        return session

    @classmethod
    def clear_session(cls, session_id: str) -> None:
        """Delete a session."""
        cls._sessions.pop(session_id, None)

    @classmethod
    def list_sessions(cls) -> List[str]:
        """List all active session IDs."""
        return list(cls._sessions.keys())
