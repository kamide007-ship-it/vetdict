"""
Learning Insights API endpoints for Phase 3 STEP 4.

Provides monitoring and analytics endpoints for AI accuracy, RECO2 performance,
and continuous learning metrics.
"""

import logging
from typing import Any, Dict

from flask import Blueprint, jsonify, request

from api.ai.accuracy_tracker import AIAccuracyTracker
from api.ai.confidence_calibration import ConfidenceCalibrator
from reco2.learning_store import LearningDataStore
from reco2.learning_tuner import LearningTuner

logger = logging.getLogger(__name__)

bp = Blueprint("learning_insights", __name__, url_prefix="/api/learning")


def _get_store() -> LearningDataStore:
    """Get learning data store instance."""
    store = LearningDataStore()
    store._state = None
    return store


@bp.route("/accuracy", methods=["GET"])
def get_accuracy_metrics():
    """
    GET /api/learning/accuracy - AI extraction accuracy metrics.

    Returns overall and domain-specific accuracy with calibration curves.
    """
    store = _get_store()
    tracker = AIAccuracyTracker()

    # Get overall stats
    stats = store.get_overall_stats()
    domain_metrics = store.get_ai_accuracy_by_domain()

    # Get calibration curve
    calibration = tracker.get_calibration_curve()

    return jsonify({
        "overall_accuracy": stats.get("overall_accuracy", 0),
        "total_extractions": stats.get("total_extractions", 0),
        "accuracy_by_domain": {
            m["domain"]: {
                "accuracy": (
                    m.get("correct_extractions", 0) / m.get("total_extractions", 1)
                    if m.get("total_extractions", 0) > 0
                    else 0
                ),
                "samples": m.get("total_extractions", 0),
                "avg_confidence": m.get("avg_confidence", 0),
                "confidence_calibration": m.get("confidence_calibration", 0),
            }
            for m in domain_metrics
        },
        "confidence_calibration_curve": calibration.get("domain_calibrations", {}),
        "false_positive_rate": (
            sum(m.get("total_extractions", 0) - m.get("correct_extractions", 0)
                for m in domain_metrics) / sum(m.get("total_extractions", 0) for m in domain_metrics)
            if sum(m.get("total_extractions", 0) for m in domain_metrics) > 0
            else 0
        ),
        "last_updated": stats.get("last_update"),
    }), 200


@bp.route("/patterns", methods=["GET"])
def get_learned_patterns():
    """
    GET /api/learning/patterns - Learned symptom-disease patterns.

    Returns discovered patterns with confidence and accuracy rates.
    """
    store = _get_store()

    # Get all patterns
    patterns = store.get_symptom_disease_patterns()

    return jsonify({
        "total_patterns": len(patterns),
        "patterns": [
            {
                "symptoms": p.get("symptoms", []),
                "disease": p.get("disease_id"),
                "accuracy": p.get("accuracy_rate", 0),
                "samples": p.get("sample_count", 0),
                "confidence": "high" if p.get("sample_count", 0) >= 10 else "medium" if p.get("sample_count", 0) >= 5 else "low",
                "last_updated": p.get("last_updated"),
            }
            for p in patterns
        ],
        "patterns_high_confidence": len([p for p in patterns if p.get("sample_count", 0) >= 10]),
        "last_updated": store._get_state().get("learning_metrics", {}).get("last_update"),
    }), 200


@bp.route("/personalization", methods=["GET"])
def get_personalization_impact():
    """
    GET /api/learning/personalization - Personalization effectiveness analysis.

    Shows how age/severity personalization affects verdict accuracy.
    """
    store = _get_store()

    impacts = store.get_personalization_impact()

    return jsonify({
        "total_segments": len(impacts),
        "by_age_stage": {
            "puppy": next(
                (i["verdict_accuracy"] for i in impacts if i.get("age_stage") == "puppy"),
                None
            ),
            "young": next(
                (i["verdict_accuracy"] for i in impacts if i.get("age_stage") == "young"),
                None
            ),
            "adult": next(
                (i["verdict_accuracy"] for i in impacts if i.get("age_stage") == "adult"),
                None
            ),
            "senior": next(
                (i["verdict_accuracy"] for i in impacts if i.get("age_stage") == "senior"),
                None
            ),
        },
        "segments": impacts,
    }), 200


@bp.route("/tuning-history", methods=["GET"])
def get_tuning_history():
    """
    GET /api/learning/tuning-history - RECO2 parameter tuning history.

    Shows recent k/eta adjustments and their reasoning.
    """
    store = _get_store()
    tuner = LearningTuner()

    state = store._get_state()
    current_k = state.get("k", 1.5)
    current_eta = state.get("eta", 0.01)

    history = tuner.get_tuning_history(limit=20)

    return jsonify({
        "current_k": current_k,
        "current_eta": current_eta,
        "recent_tuning": history,
        "total_tuning_events": len(
            state.get("learning_tuning", {}).get("tuning_history", [])
        ),
        "stability_score": 0.85,  # Placeholder: would calculate from variance
    }), 200


@bp.route("/feedback-quality", methods=["GET"])
def get_feedback_quality():
    """
    GET /api/learning/feedback-quality - Quality of feedback signal.

    Shows feedback collection rate, signal clarity, and coverage.
    """
    store = _get_store()

    stats = store.get_overall_stats()
    feedback_records = store._get_state().get("learning_metrics", {}).get("feedback_records", [])

    # Count feedback types
    good_count = sum(1 for f in feedback_records if f.get("feedback_type") == "good")
    bad_count = sum(1 for f in feedback_records if f.get("feedback_type") == "bad")
    recalc_count = sum(1 for f in feedback_records if f.get("feedback_type") == "recalculate")

    total = len(feedback_records)

    return jsonify({
        "feedback_rate": total / max(stats.get("total_extractions", 1), 1),
        "signal_strength": min(1.0, total / 50),  # Signal stronger with more feedback
        "coverage": {
            "good_feedback": good_count / total if total > 0 else 0,
            "bad_feedback": bad_count / total if total > 0 else 0,
            "recalculate_feedback": recalc_count / total if total > 0 else 0,
        },
        "total_feedback_records": total,
        "recommendations": _generate_feedback_recommendations(
            feedback_rate=total / max(stats.get("total_extractions", 1), 1),
            total_feedback=total,
        ),
    }), 200


def _generate_feedback_recommendations(feedback_rate: float, total_feedback: int) -> list:
    """Generate recommendations based on feedback quality."""
    recommendations = []

    if feedback_rate < 0.3:
        recommendations.append(
            "Increase feedback collection rate (currently {:.0%})".format(feedback_rate)
        )

    if total_feedback < 20:
        recommendations.append(
            "Collect more feedback to enable learning (need 20+, have {})".format(total_feedback)
        )

    if not recommendations:
        recommendations.append("Good feedback signal quality")

    return recommendations


@bp.route("/insights", methods=["GET"])
def get_combined_insights():
    """
    GET /api/learning/insights - Combined AI + RECO2 insights.

    Returns health score and actionable recommendations.
    """
    store = _get_store()
    AIAccuracyTracker()
    calibrator = ConfidenceCalibrator()

    stats = store.get_overall_stats()
    store.get_ai_accuracy_by_domain()

    # Calculate health score (0-1)
    accuracy = stats.get("overall_accuracy", 0)
    pattern_count = stats.get("total_patterns_learned", 0)
    feedback_signal = min(1.0, stats.get("total_feedback_records", 0) / 50)

    health_score = (accuracy * 0.4 + min(1.0, pattern_count / 10) * 0.3 + feedback_signal * 0.3)

    # Get calibration report
    calibration_report = calibrator.get_calibration_report()

    # Generate recommendations
    recommendations = []
    if accuracy > 0.9:
        recommendations.append("AI extraction accuracy is excellent - maintain current settings")
    elif accuracy > 0.8:
        recommendations.append("AI extraction accuracy is good - minor tuning recommended")
    else:
        recommendations.append("AI extraction accuracy needs improvement - increase feedback")

    if pattern_count >= 10:
        recommendations.append("Strong learned patterns detected - confidence in predictions high")

    calibration_domains = calibration_report.get("domains_needing_attention", [])
    if calibration_domains:
        recommendations.append(
            f"Domain {calibration_domains[0]['domain']} shows calibration issues - monitor confidence"
        )

    return jsonify({
        "health_score": round(health_score, 2),
        "ai_performance": {
            "status": "improving" if accuracy > 0.85 else "stable" if accuracy > 0.7 else "needs_attention",
            "accuracy": round(accuracy, 3),
            "samples": stats.get("total_extractions", 0),
        },
        "reco2_performance": {
            "stability": 0.85,
            "parameter_changes": "minimal" if len(store._get_state().get("learning_tuning", {}).get("tuning_history", [])) < 5 else "active",
        },
        "personalization": {
            "effectiveness": "good" if len(store.get_personalization_impact()) > 0 else "unknown",
        },
        "recommendations": recommendations,
        "last_updated": stats.get("last_update"),
    }), 200


@bp.route("/feedback", methods=["POST"])
def record_feedback():
    """
    POST /api/learning/feedback - Record feedback with AI context (Enhanced for Phase 3).

    Request body:
    {
        "session_id": "uuid",
        "feedback": "good|bad|recalculate",
        "domain": "orthopedics",
        "ai_result": {...},  # Optional
        "correct_symptoms": [...],  # Optional ground truth
        "notes": "User notes..."
    }
    """
    data = request.get_json() or {}

    session_id = data.get("session_id", "unknown")
    feedback_type = data.get("feedback", "good")
    domain = data.get("domain", "general")
    ai_result = data.get("ai_result", {})
    correct_symptoms = data.get("correct_symptoms")
    notes = data.get("notes", "")

    if not session_id:
        return jsonify({"error": "session_id required"}), 400

    store = _get_store()
    tracker = AIAccuracyTracker()

    # Record in learning store
    store.record_feedback_learning(
        session_id=session_id,
        feedback_type=feedback_type,
        ai_result=ai_result,
        reco2_verdict=notes,
        extracted_symptoms=ai_result.get("symptoms", []),
        disease_domain=domain,
    )

    # Evaluate extraction accuracy if ai_result provided
    accuracy_eval = {}
    if ai_result:
        accuracy_eval = tracker.evaluate_extraction(
            ai_result=ai_result,
            feedback_type=feedback_type,
            correct_symptoms=correct_symptoms,
            domain=domain,
        )

    return jsonify({
        "status": "recorded",
        "accuracy_impact": accuracy_eval.get("accuracy_score", 0),
        "learning_signal_strength": min(1.0, len(store._get_state().get("learning_metrics", {}).get("feedback_records", [])) / 50),
        "ai_feedback": {
            "extraction_accuracy": accuracy_eval.get("accuracy_score", 0),
            "confidence_calibration": "good" if accuracy_eval.get("confidence_calibration", 0) > 0.7 else "needs_review",
            "actionable_insights": _generate_accuracy_insights(accuracy_eval),
        },
    }), 201


def _generate_accuracy_insights(evaluation: Dict[str, Any]) -> list:
    """Generate actionable insights from accuracy evaluation."""
    insights = []

    if evaluation.get("is_correct"):
        insights.append("Extraction was accurate")

    if evaluation.get("personalization_impact", {}).get("age_boost_effective"):
        insights.append("Age personalization factor worked well")

    if evaluation.get("false_positives"):
        insights.append(
            f"Extracted {len(evaluation['false_positives'])} symptoms not in feedback"
        )

    if evaluation.get("false_negatives"):
        insights.append(
            f"Missed {len(evaluation['false_negatives'])} symptoms in feedback"
        )

    return insights if insights else ["Neutral feedback - no significant issues"]
