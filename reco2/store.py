import contextlib
import json
import os
from typing import Any, Dict


def _project_root() -> str:
    return os.path.dirname(os.path.dirname(__file__))

def _instance_dir() -> str:
    # Test-friendly override
    return os.environ.get("RECO3_INSTANCE_DIR") or os.path.join(_project_root(), "instance")

def state_path() -> str:
    return os.path.join(_instance_dir(), "resonance_state.json")

def _now_iso() -> str:
    import datetime
    return datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat(timespec="seconds")

def default_state() -> Dict[str, Any]:
    return {
        "k": 1.5,
        "eta": 0.01,
        "T_base": 0.8,
        "k_min": 0.5,
        "k_max": 5.0,
        "eta_min": 0.001,
        "eta_max": 0.1,
        "total_sessions": 0,
        "domains": {},
        "used_session_ids": {},
        "session_logs": [],
        "last_patrol_at_sessions": 0,
        "learning_metrics": {
            "ai_extraction_accuracy": [],
            "symptom_disease_patterns": [],
            "personalization_impact": [],
            "feedback_records": [],
            "last_update": _now_iso(),
        },
        "created_at": _now_iso(),
        "updated_at": _now_iso(),
    }

def _secure_dir(path: str) -> None:
    """ディレクトリを owner-only にする (macOS/Linux)"""
    with contextlib.suppress(OSError):
        os.chmod(path, 0o700)

def ensure_state_file() -> None:
    d = _instance_dir()
    os.makedirs(d, exist_ok=True)
    _secure_dir(d)
    sp = state_path()
    if not os.path.exists(sp):
        save_state(default_state())

def load_state() -> Dict[str, Any]:
    ensure_state_file()
    with open(state_path(), "r", encoding="utf-8") as f:
        state = json.load(f)

    # Auto-migrate old state.json format (Phase 3 learning metrics)
    if "learning_metrics" not in state:
        state["learning_metrics"] = {
            "ai_extraction_accuracy": [],
            "symptom_disease_patterns": [],
            "personalization_impact": [],
            "feedback_records": [],
            "last_update": _now_iso(),
        }
        save_state(state)

    return state

def save_state(state: Dict[str, Any]) -> None:
    state["updated_at"] = _now_iso()
    sp = state_path()
    tmp = sp + ".tmp"
    # owner-only file
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    os.replace(tmp, sp)
