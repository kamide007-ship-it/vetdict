import datetime
import logging
import math
import os
import uuid
from typing import Any, Dict, List, Optional, Tuple

from reco2.confidence_adapter import (
    adjust_context_from_ai,
    scale_confidence_to_psi_multiplier,
)
from reco2.store import load_state, save_state

logger = logging.getLogger(__name__)


def _euclidean_distance(inference: Dict[str, float], profile: Dict[str, Dict[str, float]]) -> float:
    """推論(inference)と証拠(profile)のユークリッド距離"""
    keys = sorted(set(inference.keys()) & set(profile.keys()))
    if not keys:
        keys = sorted(set(inference.keys()) | set(profile.keys()))
    s = 0.0
    for k in keys:
        i = float(inference.get(k, 0.0))
        e = profile.get(k, {})
        m = float(e.get("median", 0.0)) if isinstance(e, dict) else 0.0
        d = i - m
        s += d * d
    return math.sqrt(s)

def _context_match_score(context: Dict[str, Any]) -> float:
    conf = float(context.get("confidence", 0.0))
    conf = max(0.0, min(1.0, conf))
    domain_known = bool(context.get("domain_known", False))
    missing = int(context.get("missing_fields", 0) or 0)
    warnings = int(context.get("warnings", 0) or 0)
    score = conf
    if domain_known:
        score = min(1.0, score + 0.10)
    score -= 0.03 * missing
    score -= 0.04 * warnings
    return max(0.0, min(1.0, score))

def _purity(context: Dict[str, Any]) -> float:
    s = _context_match_score(context)
    if not bool(context.get("domain_known", False)):
        s *= 0.90
    return max(0.0, min(1.0, s))

def _alpha(context_match_score: float) -> float:
    return 1.0 + (context_match_score * 0.2)

def _beta(purity: float) -> float:
    if purity > 0.8:
        return 1.0
    return max(0.5, purity)

def _temperature(t_base: float, k: float, dist: float) -> float:
    """t = t_base * exp(-k * dist)"""
    t = t_base * math.exp(-k * dist)
    return max(0.1, t)

def _integrity(t_final: float, alpha: float, beta: float) -> float:
    """ψ = (1/t) * α * β"""
    return (1.0 / t_final) * alpha * beta


def _apply_ai_confidence_to_psi(
    psi: float, ai_result: Optional[Dict[str, Any]]
) -> Tuple[float, Optional[float]]:
    """
    Apply AI confidence multiplier to psi if AI result available.

    Args:
        psi: Original integrity score
        ai_result: Optional Phase 2b extraction result with confidence metadata

    Returns:
        Tuple of (adjusted_psi, multiplier) or (original_psi, None) if no AI result
    """
    if not ai_result or not isinstance(ai_result, dict):
        return psi, None

    # Extract AI confidence from result
    ai_confidence = ai_result.get("confidence", 0.5)
    ai_confidence = max(0.0, min(1.0, float(ai_confidence)))

    # Get multiplier from confidence
    multiplier = scale_confidence_to_psi_multiplier(ai_confidence)

    # Apply multiplier to psi
    adjusted_psi = psi * multiplier
    adjusted_psi = max(0.0, adjusted_psi)

    logger.debug(
        f"Applied AI confidence to psi: "
        f"base_psi={psi:.3f}, confidence={ai_confidence:.3f}, "
        f"multiplier={multiplier:.3f}, adjusted_psi={adjusted_psi:.3f}"
    )

    return adjusted_psi, multiplier

def _verdict_from_psi(psi: float) -> Tuple[str, str]:
    if psi >= 1.2:
        return "reliable", "信頼できる"
    if psi >= 0.8:
        return "moderate", "ふつう"
    return "suspect", "あやしい"

def _now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat(timespec="seconds")

def _confidence_adjusted(base_conf: float, psi: float) -> float:
    base_conf = max(0.0, min(1.0, float(base_conf)))
    factor = max(0.6, min(1.25, psi / 1.2))
    return max(0.0, min(1.0, base_conf * factor))

def _get_domain_weight(state: Dict[str, Any], domain: str) -> float:
    dom = state.get("domains", {})
    w = dom.get(domain, 1.0) if isinstance(dom, dict) else 1.0
    try:
        return float(w)
    except Exception:
        return 1.0

def _set_domain_weight(state: Dict[str, Any], domain: str, w: float) -> None:
    if "domains" not in state or not isinstance(state["domains"], dict):
        state["domains"] = {}
    state["domains"][domain] = float(w)

def _append_session_log(state: Dict[str, Any], entry: Dict[str, Any]) -> None:
    logs = state.get("session_logs", [])
    if not isinstance(logs, list):
        logs = []
    logs.append(entry)
    if len(logs) > 2000:
        logs = logs[-2000:]
    state["session_logs"] = logs

def evaluate_payload(
    payload: Dict[str, Any], ai_result: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Evaluate payload with optional AI confidence enhancement.

    Args:
        payload: RECO2 payload with inference, evidence, context
        ai_result: Optional Phase 2b extraction result with confidence metadata

    Returns:
        Evaluation result with verdict and integrity metrics
    """
    if not isinstance(payload, dict):
        raise ValueError("Invalid JSON")
    inference = payload.get("inference", {})
    evidence = payload.get("evidence", {})
    context = payload.get("context", {})
    if not isinstance(inference, dict) or not isinstance(evidence, dict) or not isinstance(context, dict):
        raise ValueError("Invalid payload types")
    domain = str(context.get("domain", "")).strip()
    if not domain:
        raise ValueError("context.domain is required")

    # Enhance context with AI confidence if available
    if ai_result:
        context = adjust_context_from_ai(context, ai_result)

    state = load_state()
    dist = _euclidean_distance({k: float(v) for k, v in inference.items()}, evidence)
    k = float(state.get("k", 1.5))
    eta = float(state.get("eta", 0.01))
    t_base = float(state.get("T_base", 0.8))

    cms = _context_match_score(context)
    purity = _purity(context)
    alpha = _alpha(cms)
    beta = _beta(purity)
    temp = _temperature(t_base, k, dist)
    psi = _integrity(temp, alpha, beta)

    # Apply AI confidence multiplier to psi if available
    psi_multiplier = None
    if ai_result:
        psi, psi_multiplier = _apply_ai_confidence_to_psi(psi, ai_result)

    base_conf = float(context.get("confidence", 0.0))
    conf_adj = _confidence_adjusted(base_conf, psi)
    verdict, verdict_ja = _verdict_from_psi(psi)

    session_id = str(uuid.uuid4())
    ts = _now_iso()
    state["total_sessions"] = int(state.get("total_sessions", 0) or 0) + 1
    total_sessions = state["total_sessions"]

    entry = {
        "session_id": session_id, "ts": ts, "domain": domain,
        "D": round(dist, 6), "T": round(temp, 6), "psi": round(psi, 6),
        "verdict": verdict, "reward": None, "feedback": None,
    }
    _append_session_log(state, entry)
    save_state(state)

    if total_sessions % 10 == 0:
        patrol(manual=False)

    st2 = load_state()
    result = {
        "session_id": session_id,
        "deviation": round(dist, 6),
        "temperature": round(temp, 6),
        "integrity": round(psi, 6),
        "confidence_adjusted": round(conf_adj, 6),
        "verdict": verdict,
        "verdict_ja": verdict_ja,
        "meta": {
            "k": float(st2.get("k", k)),
            "eta": float(st2.get("eta", eta)),
            "total_sessions": total_sessions,
            "domain_weight": _get_domain_weight(st2, domain),
            "context_match_score": round(cms, 6),
            "purity": round(purity, 6),
            "alpha": round(alpha, 6),
            "beta": round(beta, 6),
        }
    }

    # Include AI confidence metadata if present
    if ai_result and context.get("ai_confidence"):
        result["ai_confidence"] = context["ai_confidence"]
        if psi_multiplier is not None:
            result["meta"]["ai_psi_multiplier"] = round(psi_multiplier, 3)

    return result

def record_feedback(payload: Dict[str, Any]):
    if not isinstance(payload, dict):
        return {"error": "invalid_json"}, 400
    session_id = str(payload.get("session_id", "")).strip()
    domain = str(payload.get("domain", "")).strip()
    fb = str(payload.get("feedback", "")).strip()
    if not session_id:
        return {"error": "session_id_required"}, 400
    if not domain:
        return {"error": "domain_required"}, 400
    if fb not in ("good", "bad", "recalculate"):
        return {"error": "invalid_feedback"}, 400

    reward = 1.0 if fb == "good" else (0.3 if fb == "recalculate" else -1.0)
    state = load_state()
    used = state.get("used_session_ids", {})
    if not isinstance(used, dict):
        used = {}
    if session_id in used:
        return {"status": "duplicate_ignored", "domain": domain}

    used[session_id] = _now_iso()
    state["used_session_ids"] = used
    eta = float(state.get("eta", 0.01))
    w_old = _get_domain_weight(state, domain)
    w_new = w_old + (eta * reward)
    _set_domain_weight(state, domain, w_new)

    logs = state.get("session_logs", [])
    if isinstance(logs, list):
        for i in range(len(logs) - 1, -1, -1):
            if logs[i].get("session_id") == session_id:
                logs[i]["reward"] = reward
                logs[i]["feedback"] = fb
                break
        state["session_logs"] = logs
    save_state(state)

    # Phase 3: Record learning signal for continuous improvement
    try:
        from reco2.learning_store import LearningDataStore
        learning_store = LearningDataStore()
        learning_store.record_feedback_learning(
            session_id=session_id,
            feedback_type=fb,
            ai_result={},  # Will be populated by diagnostic_chat integration
            reco2_verdict="",  # Will be populated by integration
            extracted_symptoms=[],
            disease_domain=domain,
        )
    except Exception as e:
        # Graceful degradation: learning not critical to feedback recording
        import logging
        logging.getLogger(__name__).debug(f"Learning store recording failed: {e}")

    return {"status": "recorded", "reward": reward, "new_weight": round(w_new, 6), "domain": domain}

def _clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))

def patrol(manual: bool = True) -> Dict[str, Any]:
    state = load_state()
    logs = state.get("session_logs", [])
    if not isinstance(logs, list) or not logs:
        return {"adjusted": False, "reason": "no_logs", "new_k": state.get("k", 1.5), "new_eta": state.get("eta", 0.01)}

    window = logs[-10:] if len(logs) >= 10 else logs[:]
    ds = [float(x.get("D", 0.0)) for x in window]
    rs = [x.get("reward", 0.0) for x in window if x.get("reward") is not None]
    psis = [float(x.get("psi", 0.0)) for x in window]
    avg_d = sum(ds) / max(1, len(ds))
    sum_r = sum(float(r) for r in rs)
    avg_psi = sum(psis) / max(1, len(psis))

    k = float(state.get("k", 1.5))
    eta = float(state.get("eta", 0.01))
    adjusted = False
    reasons = []

    if avg_d > 0.3 and sum_r < 0:
        k += 0.1
        eta *= 1.05
        adjusted = True
        reasons.append("avg_d>0.3 & sum_r<0 -> strictify")
    if avg_d < 0.1 and sum_r > 0:
        k -= 0.05
        adjusted = True
        reasons.append("avg_d<0.1 & sum_r>0 -> relax")
    if avg_d > 0.3 and sum_r > 0:
        eta *= 1.02
        adjusted = True
        reasons.append("avg_d>0.3 & sum_r>0 -> learn faster")
    if avg_psi < 0.5:
        k += 0.05
        adjusted = True
        reasons.append("avg_psi<0.5 -> tighten")

    k = _clamp(k, float(state.get("k_min", 0.5)), float(state.get("k_max", 5.0)))
    eta = _clamp(eta, float(state.get("eta_min", 0.001)), float(state.get("eta_max", 0.1)))
    state["k"] = k
    state["eta"] = eta
    save_state(state)

    # Phase 3: Apply learning-driven tuning (optional enhancement)
    learning_insights = {}
    if os.getenv("ENABLE_LEARNING_TUNING", "true").lower() == "true":
        try:
            from reco2.learning_store import LearningDataStore
            from reco2.learning_tuner import LearningTuner

            learning_store = LearningDataStore()
            tuner = LearningTuner()

            # Get current learning signals
            learning_data = learning_store._get_state().get("learning_metrics", {})
            ai_accuracy = {
                "status": "ready" if learning_data.get("ai_extraction_accuracy") else "no_data",
                "overall_accuracy": sum(
                    m.get("correct_extractions", 0) / max(m.get("total_extractions", 1), 1)
                    for m in learning_data.get("ai_extraction_accuracy", [])
                ) / max(len(learning_data.get("ai_extraction_accuracy", [])), 1),
            } if learning_data.get("ai_extraction_accuracy") else {"status": "no_data"}

            # Get tuning suggestions
            suggestions = tuner.suggest_parameter_adjustments(
                current_k=k,
                current_eta=eta,
                learning_data=learning_data,
                window_stats={"avg_d": avg_d, "sum_r": sum_r, "avg_psi": avg_psi},
                ai_accuracy=ai_accuracy,
            )

            # Apply if confident
            if suggestions.get("confidence_score", 0) > 0.7:
                old_k, old_eta = k, eta
                k = suggestions.get("suggested_k", k)
                eta = suggestions.get("suggested_eta", eta)

                # Re-clamp after learning adjustment
                k = _clamp(k, float(state.get("k_min", 0.5)), float(state.get("k_max", 5.0)))
                eta = _clamp(eta, float(state.get("eta_min", 0.001)), float(state.get("eta_max", 0.1)))

                if k != old_k or eta != old_eta:
                    state["k"] = k
                    state["eta"] = eta
                    save_state(state)
                    adjusted = True
                    reasons.append(
                        f"learning_tuning: k {old_k:.2f}→{k:.2f}, "
                        f"eta {old_eta:.4f}→{eta:.4f}"
                    )

                learning_insights = {
                    "learning_applied": True,
                    "tuning_confidence": suggestions.get("confidence_score", 0),
                    "reasoning": suggestions.get("reasoning", []),
                    "affected_domains": suggestions.get("affected_domains", []),
                }
            else:
                learning_insights = {
                    "learning_applied": False,
                    "tuning_confidence": suggestions.get("confidence_score", 0),
                    "reason": "confidence below threshold (0.7)",
                }

        except Exception as e:
            # Graceful degradation: learning tuning not critical
            import logging
            logging.getLogger(__name__).debug(f"Learning-driven tuning failed: {e}")
            learning_insights = {"learning_applied": False, "error": str(e)}

    return {
        "adjusted": adjusted,
        "reason": "; ".join(reasons) if reasons else "no_change",
        "new_k": round(k, 6), "new_eta": round(eta, 6),
        "window": {"avg_d": round(avg_d, 6), "sum_r": round(sum_r, 6), "avg_psi": round(avg_psi, 6), "window_size": len(window)},
        "manual": manual,
        "learning_insights": learning_insights,
    }

def get_status() -> Dict[str, Any]:
    state = load_state()
    logs = state.get("session_logs", [])
    avg_d = 0.0
    if isinstance(logs, list) and logs:
        slice_ = logs[-200:]
        avg_d = sum(float(x.get("D", 0.0)) for x in slice_) / max(1, len(slice_))
    dist = {"reliable": 0, "moderate": 0, "suspect": 0}
    if isinstance(logs, list):
        for x in logs[-200:]:
            v = x.get("verdict")
            if v in dist:
                dist[v] += 1
    total = sum(dist.values()) or 1
    dist_pct = {k: round(v / total, 4) for k, v in dist.items()}
    total_sessions = int(state.get("total_sessions", 0) or 0)
    to_next = 10 - (total_sessions % 10) if (total_sessions % 10) != 0 else 10
    dom = state.get("domains", {})
    domains = []
    if isinstance(dom, dict):
        for d, w in dom.items():
            domains.append({"domain": d, "weight": float(w)})
    domains.sort(key=lambda x: (-x["weight"], x["domain"]))
    return {
        "k": float(state.get("k", 1.5)), "eta": float(state.get("eta", 0.01)),
        "total_sessions": total_sessions, "avg_deviation": round(avg_d, 6),
        "to_next_patrol": to_next, "domains": domains,
        "verdict_distribution": dist, "verdict_distribution_pct": dist_pct,
        "ranges": {
            "k": [float(state.get("k_min", 0.5)), float(state.get("k_max", 5.0))],
            "eta": [float(state.get("eta_min", 0.001)), float(state.get("eta_max", 0.1))],
        }
    }

def get_logs(limit: int = 50) -> List[Dict[str, Any]]:
    state = load_state()
    logs = state.get("session_logs", [])
    if not isinstance(logs, list):
        return []
    return list(reversed(logs[-limit:]))
