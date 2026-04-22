"""
RECO2 dynamic parameter tuning engine for Phase 3 STEP 3.

Intelligently optimizes k and eta parameters based on learning signals
from AI accuracy, feedback quality, and symptom-disease patterns.
"""

import logging
from typing import Any, Dict, List, Tuple

from .learning_store import LearningDataStore

logger = logging.getLogger(__name__)


class LearningTuner:
    """Intelligently tunes RECO2 k/eta parameters based on learning signals."""

    def __init__(self):
        """Initialize learning tuner."""
        self._store = LearningDataStore()

    def suggest_parameter_adjustments(
        self,
        current_k: float,
        current_eta: float,
        learning_data: Dict[str, Any],
        window_stats: Dict[str, Any],
        ai_accuracy: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Generate tuning suggestions based on multiple signals.

        Args:
            current_k: Current k parameter value
            current_eta: Current eta parameter value
            learning_data: Learning metrics from learning_store
            window_stats: Window analysis from patrol()
            ai_accuracy: AI accuracy metrics

        Returns:
            Dictionary with tuning suggestions:
            {
                "suggested_k": float,
                "suggested_eta": float,
                "confidence_score": 0.0-1.0,
                "reasoning": [...],
                "affected_domains": [...],
                "estimated_impact": {...}
            }
        """
        reasoning = []
        signals = {}

        # Signal 1: AI Accuracy Trend
        ai_signal = self._get_ai_accuracy_signal(ai_accuracy)
        signals["ai_accuracy"] = ai_signal["score"]
        if ai_signal["score"] > 0:
            reasoning.append(ai_signal["message"])

        # Signal 2: Feedback Signal Strength
        feedback_signal = self._get_feedback_signal(learning_data)
        signals["feedback_strength"] = feedback_signal["score"]
        if feedback_signal["score"] != 0:
            reasoning.append(feedback_signal["message"])

        # Signal 3: Symptom-Disease Patterns
        pattern_signal = self._get_pattern_signal(learning_data)
        signals["patterns"] = pattern_signal["score"]
        if pattern_signal["score"] != 0:
            reasoning.append(pattern_signal["message"])

        # Signal 4: Personalization Effectiveness
        personalization_signal = self._get_personalization_signal(learning_data)
        signals["personalization"] = personalization_signal["score"]

        # Calculate weighted composite signal
        confidence = self._calculate_confidence(signals)

        # Suggest adjustments based on signals
        k_adjustment = self._calculate_k_adjustment(signals, current_k)
        eta_adjustment = self._calculate_eta_adjustment(signals, current_eta)

        suggested_k = max(0.5, min(5.0, current_k + k_adjustment))
        suggested_eta = max(0.001, min(0.1, current_eta + eta_adjustment))

        return {
            "suggested_k": round(suggested_k, 3),
            "suggested_eta": round(suggested_eta, 4),
            "confidence_score": confidence,
            "reasoning": reasoning,
            "affected_domains": self._get_affected_domains(learning_data),
            "estimated_impact": self._estimate_impact(current_k, suggested_k, current_eta, suggested_eta),
            "signals": signals,
        }

    def _get_ai_accuracy_signal(self, ai_accuracy: Dict[str, Any]) -> Dict[str, Any]:
        """Extract signal from AI accuracy metrics."""
        if not ai_accuracy or ai_accuracy.get("status") != "ready":
            return {"score": 0, "message": ""}

        overall_accuracy = ai_accuracy.get("overall_accuracy", 0)

        if overall_accuracy > 0.9:
            # High and improving accuracy → relax k
            return {
                "score": 0.15,
                "message": f"High AI accuracy ({overall_accuracy:.1%}) → relax k by 0.05",
            }
        elif overall_accuracy > 0.8:
            # Good accuracy → slight relaxation
            return {
                "score": 0.05,
                "message": f"Good AI accuracy ({overall_accuracy:.1%}) → slight k relaxation",
            }
        elif overall_accuracy < 0.7:
            # Low accuracy → tighten k
            return {
                "score": -0.1,
                "message": f"Low AI accuracy ({overall_accuracy:.1%}) → tighten k robustness",
            }

        return {"score": 0, "message": ""}

    def _get_feedback_signal(self, learning_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract signal from feedback patterns."""
        feedback_records = learning_data.get("feedback_records", [])
        if len(feedback_records) < 10:
            return {"score": 0, "message": ""}

        # Count feedback types
        good_count = sum(1 for f in feedback_records if f.get("feedback_type") == "good")
        sum(1 for f in feedback_records if f.get("feedback_type") == "bad")

        if len(feedback_records) == 0:
            return {"score": 0, "message": ""}

        good_ratio = good_count / len(feedback_records)

        if good_ratio > 0.75:
            # Strong positive feedback → increase eta (trust AI more)
            return {
                "score": 0.005,
                "message": f"Strong positive feedback ({good_ratio:.0%}) → increase eta learning",
            }
        elif good_ratio < 0.5:
            # Strong negative feedback → increase eta (learn faster from corrections)
            return {
                "score": -0.002,
                "message": f"Frequent corrections ({(1 - good_ratio):.0%}) → adjust eta",
            }

        return {"score": 0, "message": ""}

    def _get_pattern_signal(self, learning_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract signal from learned symptom-disease patterns."""
        patterns = learning_data.get("symptom_disease_patterns", [])

        # Count stable, high-accuracy patterns
        stable_patterns = [p for p in patterns if p.get("sample_count", 0) >= 5 and p.get("accuracy_rate", 0) > 0.8]

        if len(stable_patterns) < 3:
            return {"score": 0, "message": ""}

        # Many stable patterns → symptoms are predictive, can relax k
        return {
            "score": 0.03,
            "message": f"Stable symptom patterns detected ({len(stable_patterns)}) → lower k penalty",
        }

    def _get_personalization_signal(self, learning_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract signal from personalization effectiveness."""
        impacts = learning_data.get("personalization_impact", [])

        if not impacts:
            return {"score": 0}

        # Calculate average effectiveness
        effective_count = sum(1 for i in impacts if i.get("verdict_accuracy", 0) > 0.8)

        if effective_count == 0:
            return {"score": -0.02}

        effectiveness = effective_count / len(impacts)
        if effectiveness > 0.7:
            return {"score": 0.02}

        return {"score": 0}

    def _calculate_confidence(self, signals: Dict[str, float]) -> float:
        """Calculate overall confidence in tuning suggestions."""
        # Base confidence on signal strength
        signal_strengths = [abs(s) for s in signals.values() if isinstance(s, (int, float))]

        if not signal_strengths:
            return 0.3

        # Average signal strength = confidence
        avg_signal = sum(signal_strengths) / len(signal_strengths)
        return min(0.95, avg_signal * 5)  # Normalize to 0-0.95 range

    def _calculate_k_adjustment(self, signals: Dict[str, float], current_k: float) -> float:
        """Calculate k adjustment based on signals."""
        # Weights for each signal
        weights = {
            "ai_accuracy": 0.4,
            "feedback_strength": 0.25,
            "patterns": 0.2,
            "personalization": 0.15,
        }

        weighted_signal = sum(signals.get(key, 0) * weight for key, weight in weights.items())

        # Cap adjustment per cycle (stability)
        max_adjustment = 0.1
        adjustment = max(-max_adjustment, min(max_adjustment, weighted_signal))

        return adjustment

    def _calculate_eta_adjustment(self, signals: Dict[str, float], current_eta: float) -> float:
        """Calculate eta adjustment based on signals."""
        # Eta adjusts faster, multiplicative factor
        feedback_signal = signals.get("feedback_strength", 0)

        # Eta adjustment: 1% of current value per signal unit
        adjustment = current_eta * feedback_signal * 0.01

        # Cap adjustment
        max_adjustment = current_eta * 0.02  # Max 2% change
        return max(-max_adjustment, min(max_adjustment, adjustment))

    def _get_affected_domains(self, learning_data: Dict[str, Any]) -> List[str]:
        """Identify which domains are affected by tuning."""
        patterns = learning_data.get("symptom_disease_patterns", [])
        domains = set()

        for pattern in patterns:
            if pattern.get("sample_count", 0) >= 5:
                domains.add(pattern.get("disease_id", "general"))

        return list(domains)[:5]  # Top 5 domains

    def _estimate_impact(
        self,
        old_k: float,
        new_k: float,
        old_eta: float,
        new_eta: float,
    ) -> Dict[str, Any]:
        """Estimate impact of parameter changes."""
        k_change = new_k - old_k
        eta_change = new_eta - old_eta

        # Estimate verdict distribution impact
        # k affects how strict the threshold is
        # Higher k → more conservative (fewer reliable verdicts)
        if k_change < 0:
            verdict_change = {
                "reliable": 0.02,
                "moderate": -0.01,
                "suspect": -0.01,
            }
            speed = "faster"
        elif k_change > 0:
            verdict_change = {
                "reliable": -0.02,
                "moderate": 0.01,
                "suspect": 0.01,
            }
            speed = "slower"
        else:
            verdict_change = {"reliable": 0, "moderate": 0, "suspect": 0}
            speed = "unchanged"

        return {
            "verdict_distribution_change": verdict_change,
            "convergence_speed": speed,
            "k_change": round(k_change, 3),
            "eta_change": round(eta_change, 4),
        }

    def apply_learning_driven_tuning(
        self,
        state: Dict[str, Any],
        learning_signals: Dict[str, Any],
        min_confidence: float = 0.7,
    ) -> Tuple[bool, str]:
        """
        Apply learning-driven tuning to state if confidence > threshold.

        Args:
            state: Current RECO2 state
            learning_signals: Learning signals from this method
            min_confidence: Minimum confidence to apply tuning

        Returns:
            Tuple of (adjusted: bool, reason: str)
        """
        if learning_signals.get("confidence_score", 0) < min_confidence:
            return (
                False,
                f"Confidence {learning_signals['confidence_score']:.2f} < threshold {min_confidence}",
            )

        old_k = state.get("k", 1.5)
        old_eta = state.get("eta", 0.01)

        state["k"] = learning_signals["suggested_k"]
        state["eta"] = learning_signals["suggested_eta"]

        reason = (
            f"Applied learning tuning: k {old_k:.2f} → {learning_signals['suggested_k']:.2f}, "
            f"eta {old_eta:.4f} → {learning_signals['suggested_eta']:.4f} "
            f"(confidence: {learning_signals['confidence_score']:.2f})"
        )

        return True, reason

    def get_tuning_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get recent tuning decisions and their impacts.

        Args:
            limit: Maximum number of entries to return

        Returns:
            List of tuning history dictionaries
        """
        self._store._ensure_learning_metrics()
        state = self._store._get_state()

        tuning_history = state.get("learning_tuning", {}).get("tuning_history", [])
        return tuning_history[-limit:]
