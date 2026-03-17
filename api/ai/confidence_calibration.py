"""
Confidence score calibration engine for Phase 3 STEP 2.

Dynamically calibrates AI confidence scores based on historical accuracy.
Applies corrections to extract over/underconfident behavior per domain.
"""

import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


class ConfidenceCalibrator:
    """Dynamically calibrate AI confidence scores based on historical accuracy."""

    def __init__(self):
        """Initialize confidence calibrator."""
        self._calibration_cache = {}

    def get_calibration_factor(
        self,
        raw_confidence: float,
        domain: str = "general",
    ) -> float:
        """
        Get multiplier to adjust raw AI confidence.

        Example:
        - raw_confidence=0.9 with calibration_factor=0.95
        - returns adjusted_confidence=0.855 (more conservative if overconfident)

        Args:
            raw_confidence: Raw AI confidence score (0-1)
            domain: Domain name

        Returns:
            Calibration factor to multiply with raw confidence (0.9-1.1 range typical)
        """
        from reco2.learning_store import LearningDataStore

        store = LearningDataStore()
        store._state = None

        metrics = store.get_ai_accuracy_by_domain(domain=domain)

        if not metrics or metrics[0].get("total_extractions", 0) < 20:
            # Not enough samples, use neutral factor
            return 1.0

        metric = metrics[0]
        total = metric.get("total_extractions", 1)
        correct = metric.get("correct_extractions", 0)
        actual_accuracy = correct / total if total > 0 else 0.0

        # Calculate calibration factor
        # If confidence=0.8 but actual accuracy is 0.7, factor = 0.7/0.8 = 0.875
        # This will adjust future 0.8 confidence to 0.7
        factor = min(1.1, max(0.9, actual_accuracy / raw_confidence)) if raw_confidence > 0 else 1.0

        return round(factor, 3)

    def calibrate_extraction_result(
        self,
        extraction_result: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Apply calibration adjustments to extraction result.

        Args:
            extraction_result: Extraction result from symptom_extractor

        Returns:
            Updated extraction result with calibrated confidence
        """
        if not extraction_result:
            return extraction_result

        domain = extraction_result.get("domain", "general")
        raw_confidence = extraction_result.get("confidence", 0.5)

        # Get calibration factor
        factor = self.get_calibration_factor(raw_confidence, domain)

        # Apply calibration
        calibrated_confidence = min(1.0, max(0.0, raw_confidence * factor))

        # Update result
        extraction_result["confidence"] = calibrated_confidence
        extraction_result["calibration_factor"] = factor
        extraction_result["calibration_notes"] = self._get_calibration_notes(
            raw_confidence, calibrated_confidence, factor
        )

        # Estimate expected accuracy at new confidence level
        extraction_result["expected_accuracy"] = calibrated_confidence

        return extraction_result

    def _get_calibration_notes(
        self,
        raw_confidence: float,
        calibrated_confidence: float,
        factor: float,
    ) -> str:
        """Generate human-readable notes about calibration adjustment."""
        if abs(factor - 1.0) < 0.01:
            return "Well-calibrated (factor: 1.0)"
        elif factor > 1.0:
            return f"Underconfident historically (boosted by {(factor-1.0)*100:.0f}%)"
        else:
            return f"Overconfident historically (reduced by {(1.0-factor)*100:.0f}%)"

    def get_calibration_report(self) -> Dict[str, Any]:
        """
        Return calibration status across domains.

        Shows which domains are over/under-confident.

        Returns:
            Dictionary with calibration report
        """
        from reco2.learning_store import LearningDataStore

        store = LearningDataStore()
        store._state = None

        all_metrics = store.get_ai_accuracy_by_domain()

        if not all_metrics:
            return {
                "status": "no_data",
                "domains": [],
            }

        domain_reports = []

        for metric in all_metrics:
            domain = metric.get("domain", "unknown")
            total = metric.get("total_extractions", 0)

            if total < 20:
                status = "insufficient_data"
            else:
                correct = metric.get("correct_extractions", 0)
                actual_accuracy = correct / total
                avg_confidence = metric.get("avg_confidence", 0.5)

                if abs(actual_accuracy - avg_confidence) < 0.05:
                    status = "well_calibrated"
                elif actual_accuracy < avg_confidence:
                    status = "overconfident"
                else:
                    status = "underconfident"

            domain_reports.append({
                "domain": domain,
                "status": status,
                "samples": total,
                "avg_confidence": metric.get("avg_confidence", 0),
                "actual_accuracy": (
                    metric.get("correct_extractions", 0) / metric.get("total_extractions", 1)
                    if metric.get("total_extractions", 0) > 0
                    else 0
                ),
                "calibration_factor": self.get_calibration_factor(
                    metric.get("avg_confidence", 0.5), domain
                ),
            })

        return {
            "status": "ready",
            "domains": domain_reports,
            "domains_needing_attention": [
                d for d in domain_reports if d["status"] in ("overconfident", "underconfident")
            ],
        }

    def should_apply_calibration(self, domain: str = "general") -> bool:
        """
        Check if calibration should be applied for a domain.

        Returns False if insufficient data.

        Args:
            domain: Domain name

        Returns:
            True if calibration should be applied
        """
        from reco2.learning_store import LearningDataStore

        store = LearningDataStore()
        store._state = None

        metrics = store.get_ai_accuracy_by_domain(domain=domain)

        if not metrics:
            return False

        return metrics[0].get("total_extractions", 0) >= 20
