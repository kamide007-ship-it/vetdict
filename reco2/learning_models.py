"""
Data models for Phase 3 continuous learning pipeline.

Defines structures for tracking AI accuracy, learned patterns,
and personalization effectiveness.
"""

from dataclasses import asdict, dataclass
from typing import List


@dataclass
class SymptomDiseaseLearning:
    """Learned pattern: symptom(s) → disease relationship strength."""

    symptoms: List[str]          # Symptom IDs
    disease_id: str              # Disease entity ID
    confidence_boost: float      # AI confidence impact (-0.3 to +0.3)
    accuracy_rate: float         # % correct verdicts (0.0-1.0)
    sample_count: int            # Feedback samples collected
    last_updated: str            # ISO timestamp

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> 'SymptomDiseaseLearning':
        return SymptomDiseaseLearning(**data)


@dataclass
class AIExtractionAccuracy:
    """AI extraction accuracy metrics per domain."""

    domain: str                  # Domain name (e.g., "orthopedics", "general")
    total_extractions: int       # Total extraction attempts
    correct_extractions: int     # Matched feedback ground truth
    avg_confidence: float        # Average confidence of correct extractions
    avg_confidence_failed: float # Average confidence of incorrect extractions
    confidence_calibration: float  # How well confidence predicts correctness (0-1)
    false_positive_rate: float   # % of extracted symptoms not in feedback
    false_negative_rate: float   # % of feedback symptoms not extracted
    last_updated: str            # ISO timestamp

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> 'AIExtractionAccuracy':
        return AIExtractionAccuracy(**data)


@dataclass
class PersonalizationImpact:
    """Personalization effectiveness metrics."""

    age_stage: str              # "puppy", "young", "adult", "senior"
    severity_level: str         # "mild", "moderate", "severe"
    verdict_accuracy: float     # % correct verdicts with this personalization
    sample_count: int           # Number of sessions
    avg_confidence_boost: float # Average confidence adjustment applied
    last_updated: str           # ISO timestamp

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> 'PersonalizationImpact':
        return PersonalizationImpact(**data)


@dataclass
class FeedbackRecord:
    """Record of user feedback on a diagnostic verdict."""

    session_id: str              # Session identifier
    feedback_type: str           # "good", "bad", "recalculate"
    extracted_symptoms: List[str]  # Symptoms AI extracted
    disease_domain: str          # Disease domain
    ai_confidence: float         # AI's confidence score
    reco2_verdict: str           # RECO2 verdict text
    timestamp: str               # ISO timestamp

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> 'FeedbackRecord':
        return FeedbackRecord(**data)
