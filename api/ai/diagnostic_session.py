"""Diagnostic session management with state tracking and Bayesian updates.

Maintains conversation state across multiple question-answer rounds,
enabling adaptive questioning and progressive disease narrowing.
"""

import json
import logging
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

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
        return self.round_number < 10

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
            "answer_timestamps": self.answer_timestamps,
            "breed": self.breed,
            "age_years": self.age_years,
            "gender": self.gender,
            "vaccination_status": self.vaccination_status,
            "confidence_threshold": self.confidence_threshold,
            "initial_candidates": self.initial_candidates,
            "current_candidates": self.current_candidates,
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

        Restores persisted candidates and answer history when available.
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
            session.answer_timestamps = data.get("answer_timestamps", {})
            session.confidence_threshold = data.get("confidence_threshold", 0.7)
            session.initial_candidates = data.get("initial_candidates", [])
            session.current_candidates = data.get("current_candidates", [])
            return session
        except Exception as e:
            logger.error(f"Failed to deserialize diagnostic session: {e}")
            return None


class DiagnosticSessionManager:
    """Manages diagnostic sessions (factory and storage)."""

    # In-memory session cache (would use Redis in production)
    _sessions: Dict[str, DiagnosticSession] = {}
    _storage_dir: Path = Path(__file__).resolve().parents[2] / ".diagnostic_sessions"

    @classmethod
    def _validate_session_id(cls, session_id: str) -> str:
        """Validate that session IDs are UUIDs."""
        return str(uuid.UUID(str(session_id).strip()))

    @classmethod
    def _get_session_file_path(cls, session_id: str) -> Path:
        """Build a validated, storage-local file path for a session."""
        validated_session_id = cls._validate_session_id(session_id)
        storage_dir = cls._storage_dir.resolve()
        file_path = (storage_dir / f"{validated_session_id}.json").resolve()

        if storage_dir not in file_path.parents:
            raise ValueError("Invalid session storage path")

        return file_path

    @classmethod
    def _save_session(cls, session: DiagnosticSession) -> None:
        """Persist a session to disk."""
        file_path = cls._get_session_file_path(session.session_id)
        file_path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        file_path.write_text(session.to_json(), encoding="utf-8")

    @classmethod
    def _load_session(cls, session_id: str) -> Optional[DiagnosticSession]:
        """Load a session from disk."""
        try:
            file_path = cls._get_session_file_path(session_id)
        except (ValueError, AttributeError):
            return None

        if not file_path.exists():
            return None

        session = DiagnosticSession.from_json(file_path.read_text(encoding="utf-8"))
        if session is not None:
            cls._sessions[session.session_id] = session
        return session

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
        cls._save_session(session)
        return session

    @classmethod
    def get_session(cls, session_id: str) -> Optional[DiagnosticSession]:
        """Retrieve a session by ID."""
        try:
            validated_session_id = cls._validate_session_id(session_id)
        except (ValueError, AttributeError):
            return None

        session = cls._sessions.get(validated_session_id)
        if session:
            return session

        return cls._load_session(validated_session_id)

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
        cls._save_session(session)

        return session

    @classmethod
    def clear_session(cls, session_id: str) -> None:
        """Delete a session."""
        try:
            validated_session_id = cls._validate_session_id(session_id)
        except (ValueError, AttributeError):
            return

        cls._sessions.pop(validated_session_id, None)

        file_path = cls._get_session_file_path(validated_session_id)
        if file_path.exists():
            file_path.unlink()

    @classmethod
    def list_sessions(cls) -> List[str]:
        """List all active session IDs."""
        return list(cls._sessions.keys())
