"""
AI extraction accuracy tracking and evaluation for Phase 3 STEP 2.

Monitors AI symptom extraction accuracy against user feedback,
measures calibration, and provides performance metrics.
"""

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class AIAccuracyTracker:
    """Monitors AI symptom extraction accuracy against feedback."""

    def __init__(self):
        """Initialize accuracy tracker."""
        pass

    def evaluate_extraction(
        self,
        ai_result: Dict[str, Any],
        feedback_type: str,  # "good", "bad", "recalculate"
        correct_symptoms: Optional[List[str]] = None,
        domain: str = "general",
    ) -> Dict[str, Any]:
        """
        Evaluate extraction accuracy against feedback.

        Args:
            ai_result: AI extraction result with confidence and metadata
            feedback_type: Type of feedback ("good", "bad", "recalculate")
            correct_symptoms: Optional ground truth symptom IDs
            domain: Domain name for categorization

        Returns:
            Dictionary with accuracy evaluation:
            {
                "accuracy_score": 0.0-1.0,
                "confidence_calibration": 0.0-1.0,
                "false_positives": [...],  # Extracted but not in feedback
                "false_negatives": [...],  # Not extracted but in feedback
                "personalization_impact": {
                    "age_boost_effective": bool,
                    "severity_factor_helped": bool
                }
            }
        """
        extracted_symptoms = ai_result.get("symptoms", [])
        ai_confidence = ai_result.get("confidence", 0.5)

        # Determine accuracy based on feedback type
        is_correct = feedback_type == "good"

        # If ground truth provided, calculate detailed metrics
        if correct_symptoms is not None:
            extracted_set = set(extracted_symptoms)
            correct_set = set(correct_symptoms)

            # Calculate false positives and negatives
            false_positives = list(extracted_set - correct_set)
            false_negatives = list(correct_set - extracted_set)
            true_positives = len(extracted_set & correct_set)

            # Accuracy: TP / (TP + FP + FN)
            total_errors = len(false_positives) + len(false_negatives)
            accuracy_score = (
                1.0 if total_errors == 0 else max(0.0, 1.0 - (total_errors / len(correct_set)))
                if correct_symptoms
                else (1.0 if is_correct else 0.0)
            )
        else:
            # Use feedback as proxy for accuracy
            accuracy_score = 1.0 if is_correct else 0.0
            false_positives = []
            false_negatives = []

        # Evaluate personalization impact if present
        personalization = ai_result.get("personalization", {})
        personalization_impact = {
            "age_boost_effective": bool(personalization.get("age_boost", 0) > 0 and is_correct),
            "severity_factor_helped": bool(personalization.get("severity_adjustment", 0) > 0 and is_correct),
        }

        return {
            "accuracy_score": accuracy_score,
            "confidence_calibration": ai_confidence if is_correct else 1.0 - ai_confidence,
            "false_positives": false_positives,
            "false_negatives": false_negatives,
            "is_correct": is_correct,
            "ai_confidence": ai_confidence,
            "personalization_impact": personalization_impact,
        }

    def get_calibration_curve(
        self,
        domain: Optional[str] = None,
        min_samples: int = 20,
    ) -> Dict[str, Any]:
        """
        Get confidence calibration curve.

        Returns expected accuracy at each confidence level.
        Well-calibrated: confidence 0.8 should yield ~80% accuracy

        Args:
            domain: Optional domain to filter
            min_samples: Minimum samples required for calibration

        Returns:
            Dictionary with calibration metrics
        """
        from reco2.learning_store import LearningDataStore

        store = LearningDataStore()
        store._state = None

        if domain:
            metrics = store.get_ai_accuracy_by_domain(domain=domain)
        else:
            metrics = store.get_ai_accuracy_by_domain()

        if not metrics:
            return {
                "domains": [],
                "overall_calibration": 0.0,
                "confidence_ranges": {},
                "status": "insufficient_data",
            }

        # Extract calibration data from metrics
        calibrations = []
        for metric in metrics:
            if metric.get("total_extractions", 0) >= min_samples:
                calibrations.append(metric)

        if not calibrations:
            return {
                "domains": [],
                "overall_calibration": 0.0,
                "confidence_ranges": {},
                "status": "insufficient_data",
            }

        # Calculate overall calibration across domains
        overall_calibration = sum(
            m.get("confidence_calibration", 0) for m in calibrations
        ) / len(calibrations)

        return {
            "domains": [m["domain"] for m in calibrations],
            "overall_calibration": overall_calibration,
            "domain_calibrations": {
                m["domain"]: {
                    "calibration": m.get("confidence_calibration", 0),
                    "avg_confidence": m.get("avg_confidence", 0),
                    "samples": m.get("total_extractions", 0),
                }
                for m in calibrations
            },
            "confidence_ranges": {
                "0.7-0.8": {"expected_accuracy": 0.75, "note": "Low confidence range"},
                "0.8-0.9": {"expected_accuracy": 0.85, "note": "Medium confidence range"},
                "0.9-1.0": {"expected_accuracy": 0.93, "note": "High confidence range"},
            },
            "status": "ready",
        }

    def get_extraction_metrics_by_symptom(
        self,
        symptom_id: str,
        domain: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Get per-symptom extraction accuracy and confusion patterns.

        Args:
            symptom_id: Symptom ID to analyze
            domain: Optional domain to filter

        Returns:
            Dictionary with per-symptom metrics
        """
        from reco2.learning_store import LearningDataStore

        store = LearningDataStore()
        store._state = None

        patterns = store.get_symptom_disease_patterns(symptom_ids=[symptom_id])

        if not patterns:
            return {
                "symptom_id": symptom_id,
                "status": "no_data",
                "patterns": [],
            }

        return {
            "symptom_id": symptom_id,
            "total_patterns": len(patterns),
            "patterns": patterns[:10],  # Top 10 patterns
            "overall_accuracy": sum(p.get("accuracy_rate", 0) for p in patterns) / len(patterns)
            if patterns
            else 0.0,
            "status": "ready",
        }

    def get_domain_performance(self, domain: str) -> Dict[str, Any]:
        """
        Get overall performance metrics for a domain.

        Args:
            domain: Domain name

        Returns:
            Dictionary with domain performance metrics
        """
        from reco2.learning_store import LearningDataStore

        store = LearningDataStore()
        store._state = None

        metrics = store.get_ai_accuracy_by_domain(domain=domain)

        if not metrics:
            return {
                "domain": domain,
                "status": "no_data",
            }

        metric = metrics[0]
        total = metric.get("total_extractions", 1)
        correct = metric.get("correct_extractions", 0)

        return {
            "domain": domain,
            "total_extractions": total,
            "accuracy": correct / total if total > 0 else 0.0,
            "avg_confidence": metric.get("avg_confidence", 0),
            "avg_confidence_failed": metric.get("avg_confidence_failed", 0),
            "confidence_calibration": metric.get("confidence_calibration", 0),
            "status": "ready",
        }
