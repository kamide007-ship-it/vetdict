"""
Learning data persistence and analytics engine for Phase 3.

Manages accumulated learning patterns from user feedback,
calculates AI accuracy metrics, and provides analytics queries.
"""

import logging
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from . import store
from .learning_models import (
    FeedbackRecord,
)

logger = logging.getLogger(__name__)


class LearningDataStore:
    """Manages persistent learning patterns and analytics."""

    def __init__(self):
        """Initialize learning data store."""
        self._state = None

    def _get_state(self) -> Dict[str, Any]:
        """Load current state from persistent storage."""
        if self._state is None:
            self._state = store.load_state()
        return self._state

    def _save_state(self) -> None:
        """Persist state to storage."""
        if self._state is not None:
            store.save_state(self._state)

    def _ensure_learning_metrics(self) -> None:
        """Ensure learning_metrics section exists in state."""
        state = self._get_state()
        if "learning_metrics" not in state:
            state["learning_metrics"] = {
                "ai_extraction_accuracy": [],
                "symptom_disease_patterns": [],
                "personalization_impact": [],
                "feedback_records": [],  # Aggregated, not individual patient data
                "last_update": store._now_iso(),
            }
            self._save_state()

    def record_feedback_learning(
        self,
        session_id: str,
        feedback_type: str,  # "good", "bad", "recalculate"
        ai_result: Dict[str, Any],
        reco2_verdict: str,
        extracted_symptoms: List[str],
        disease_domain: str,
    ) -> None:
        """
        Record learning signal from user feedback.

        Args:
            session_id: Session identifier
            feedback_type: Type of feedback ("good", "bad", "recalculate")
            ai_result: AI extraction result with confidence and metadata
            reco2_verdict: RECO2 verdict text
            extracted_symptoms: List of extracted symptom IDs
            disease_domain: Disease domain/category
        """
        self._ensure_learning_metrics()
        state = self._get_state()

        ai_confidence = ai_result.get("confidence", 0.5)

        # Record feedback (aggregated format, no patient data)
        feedback = FeedbackRecord(
            session_id=session_id,
            feedback_type=feedback_type,
            extracted_symptoms=extracted_symptoms,
            disease_domain=disease_domain,
            ai_confidence=ai_confidence,
            reco2_verdict=reco2_verdict,
            timestamp=store._now_iso(),
        )

        metrics = state["learning_metrics"]
        metrics["feedback_records"].append(feedback.to_dict())

        # Keep only last 2000 feedback records (memory bound)
        if len(metrics["feedback_records"]) > 2000:
            metrics["feedback_records"] = metrics["feedback_records"][-2000:]

        metrics["last_update"] = store._now_iso()
        self._save_state()

        # Update derived metrics
        self._update_ai_accuracy_metrics(state, feedback)
        self._update_symptom_disease_patterns(state, feedback)
        self._update_personalization_impact(state, feedback)

    def _update_ai_accuracy_metrics(self, state: Dict[str, Any], feedback: FeedbackRecord) -> None:
        """Update AI extraction accuracy metrics from feedback."""
        metrics = state["learning_metrics"]
        domain = feedback.disease_domain or "general"

        # Find or create domain entry
        accuracy_entries = metrics.get("ai_extraction_accuracy", [])
        domain_entry = next(
            (e for e in accuracy_entries if e.get("domain") == domain),
            None,
        )

        if domain_entry is None:
            domain_entry = {
                "domain": domain,
                "total_extractions": 0,
                "correct_extractions": 0,
                "incorrect_extractions": 0,
                "avg_confidence": 0.0,
                "avg_confidence_failed": 0.0,
                "confidence_calibration": 0.0,
                "false_positive_rate": 0.0,
                "false_negative_rate": 0.0,
                "last_updated": store._now_iso(),
            }
            accuracy_entries.append(domain_entry)
            metrics["ai_extraction_accuracy"] = accuracy_entries

        # Count as correct if feedback is "good"
        is_correct = feedback.feedback_type == "good"

        domain_entry["total_extractions"] += 1
        if is_correct:
            domain_entry["correct_extractions"] += 1
        else:
            domain_entry["incorrect_extractions"] = domain_entry.get("incorrect_extractions", 0) + 1

        # Update average confidence for correct extractions
        correct = domain_entry["correct_extractions"]
        old_avg = domain_entry["avg_confidence"]
        if is_correct:
            domain_entry["avg_confidence"] = (old_avg * (correct - 1) + feedback.ai_confidence) / correct

        # Update average confidence for failed extractions
        incorrect = domain_entry.get("incorrect_extractions", 0)
        old_avg_failed = domain_entry["avg_confidence_failed"]
        if not is_correct:
            domain_entry["avg_confidence_failed"] = (
                old_avg_failed * (incorrect - 1) + feedback.ai_confidence
            ) / incorrect

        # Calculate calibration and rates
        correct = domain_entry["correct_extractions"]
        total = domain_entry["total_extractions"]
        domain_entry["confidence_calibration"] = correct / total if total > 0 else 0.0

        domain_entry["last_updated"] = store._now_iso()
        self._save_state()

    def _update_symptom_disease_patterns(self, state: Dict[str, Any], feedback: FeedbackRecord) -> None:
        """Update learned symptom-disease patterns."""
        if not feedback.extracted_symptoms:
            return

        metrics = state["learning_metrics"]
        patterns = metrics.get("symptom_disease_patterns", [])

        # Create pattern key
        pattern_key = (
            tuple(sorted(feedback.extracted_symptoms)),
            feedback.disease_domain,
        )

        # Find or create pattern
        pattern = next(
            (p for p in patterns if (tuple(sorted(p.get("symptoms", []))), p.get("disease_id")) == pattern_key),
            None,
        )

        is_correct = feedback.feedback_type == "good"

        if pattern is None:
            pattern = {
                "symptoms": list(feedback.extracted_symptoms),
                "disease_id": feedback.disease_domain,
                "confidence_boost": 0.1 if is_correct else -0.1,
                "accuracy_rate": 1.0 if is_correct else 0.0,
                "sample_count": 1,
                "last_updated": store._now_iso(),
            }
            patterns.append(pattern)
        else:
            # Update existing pattern
            old_count = pattern["sample_count"]
            new_count = old_count + 1
            old_accuracy = pattern["accuracy_rate"]
            pattern["accuracy_rate"] = (old_accuracy * old_count + (1.0 if is_correct else 0.0)) / new_count
            pattern["sample_count"] = new_count
            pattern["last_updated"] = store._now_iso()

        metrics["symptom_disease_patterns"] = patterns
        self._save_state()

    def _update_personalization_impact(self, state: Dict[str, Any], feedback: FeedbackRecord) -> None:
        """Update personalization effectiveness metrics."""
        # Personalization data comes from ai_result
        # For now, we track general personalization impact
        # (more detailed tracking would require ai_result metadata)
        pass

    def get_symptom_disease_patterns(self, symptom_ids: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Retrieve learned symptom-disease relationships.

        Args:
            symptom_ids: Optional list of symptom IDs to filter

        Returns:
            List of pattern dictionaries
        """
        self._ensure_learning_metrics()
        state = self._get_state()
        patterns = state["learning_metrics"].get("symptom_disease_patterns", [])

        if symptom_ids:
            # Filter to patterns containing all specified symptoms
            patterns = [p for p in patterns if all(sid in p.get("symptoms", []) for sid in symptom_ids)]

        # Sort by accuracy and sample count
        return sorted(
            patterns,
            key=lambda p: (p.get("accuracy_rate", 0), p.get("sample_count", 0)),
            reverse=True,
        )

    def get_ai_accuracy_by_domain(
        self,
        domain: Optional[str] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """
        Get AI extraction accuracy metrics.

        Args:
            domain: Optional domain to filter
            limit: Maximum number of entries to return

        Returns:
            List of accuracy metric dictionaries
        """
        self._ensure_learning_metrics()
        state = self._get_state()
        metrics = state["learning_metrics"].get("ai_extraction_accuracy", [])

        if domain:
            metrics = [m for m in metrics if m.get("domain") == domain]

        return metrics[:limit]

    def get_personalization_impact(self, age_stage: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Analyze personalization effectiveness.

        Args:
            age_stage: Optional age stage to filter ("puppy", "young", "adult", "senior")

        Returns:
            List of personalization impact dictionaries
        """
        self._ensure_learning_metrics()
        state = self._get_state()
        impacts = state["learning_metrics"].get("personalization_impact", [])

        if age_stage:
            impacts = [i for i in impacts if i.get("age_stage") == age_stage]

        return impacts

    def prune_old_patterns(self, days: int = 90) -> int:
        """
        Remove patterns older than N days.

        Args:
            days: Age threshold in days

        Returns:
            Count of patterns removed
        """
        self._ensure_learning_metrics()
        state = self._get_state()
        metrics = state["learning_metrics"]

        cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
        patterns = metrics.get("symptom_disease_patterns", [])

        before_count = len(patterns)
        patterns = [p for p in patterns if datetime.fromisoformat(p.get("last_updated", "2000-01-01")) > cutoff_date]
        metrics["symptom_disease_patterns"] = patterns

        feedback_records = metrics.get("feedback_records", [])
        feedback_records = [
            f for f in feedback_records if datetime.fromisoformat(f.get("timestamp", "2000-01-01")) > cutoff_date
        ]
        metrics["feedback_records"] = feedback_records

        self._save_state()
        removed_count = before_count - len(patterns)

        logger.info(f"Pruned {removed_count} patterns older than {days} days")
        return removed_count

    def get_overall_stats(self) -> Dict[str, Any]:
        """Get overall learning statistics."""
        self._ensure_learning_metrics()
        state = self._get_state()
        metrics = state["learning_metrics"]

        accuracy_data = metrics.get("ai_extraction_accuracy", [])
        patterns = metrics.get("symptom_disease_patterns", [])
        feedback = metrics.get("feedback_records", [])

        total_extractions = sum(m.get("total_extractions", 0) for m in accuracy_data)
        total_correct = sum(m.get("correct_extractions", 0) for m in accuracy_data)

        return {
            "total_feedback_records": len(feedback),
            "total_patterns_learned": len(patterns),
            "total_extractions": total_extractions,
            "total_correct_extractions": total_correct,
            "overall_accuracy": (total_correct / total_extractions if total_extractions > 0 else 0.0),
            "domains_tracked": len(accuracy_data),
            "last_update": metrics.get("last_update"),
        }
