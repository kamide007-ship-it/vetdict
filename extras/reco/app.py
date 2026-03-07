import logging
from functools import wraps

from flask import Flask, jsonify, render_template, request

from reco2 import input_gate, output_gate
from reco2.config import load_config, public_config
from reco2.engine import evaluate_payload, get_logs, get_status, patrol, record_feedback
from reco2.orchestrator import get_orchestrator
from reco2.store import ensure_state_file

logging.basicConfig(level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S")
log = logging.getLogger("reco3")

app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["JSON_AS_ASCII"] = False
ensure_state_file()

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        cfg = load_config()
        if not cfg.get("api_key_enabled", False):
            return f(*args, **kwargs)
        key = (request.headers.get("X-API-Key")
               or request.headers.get("Authorization", "").removeprefix("Bearer ").strip())
        valid_keys = cfg.get("api_keys", [])
        if not key or key not in valid_keys:
            return jsonify({"error": "unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated

@app.get("/")
def page_index():
    return render_template("index.html")

@app.get("/r3")
def page_r3():
    return render_template("reco3.html")

@app.post("/api/evaluate")
@require_api_key
def api_evaluate():
    payload = request.get_json(force=True, silent=False)
    return jsonify(evaluate_payload(payload))

@app.post("/api/feedback")
@require_api_key
def api_feedback():
    payload = request.get_json(force=True, silent=True) or {}
    res = record_feedback(payload)
    if isinstance(res, tuple):
        return jsonify(res[0]), res[1]
    return jsonify(res)

@app.post("/api/patrol")
@require_api_key
def api_patrol():
    return jsonify(patrol(manual=True))

@app.get("/api/status")
@require_api_key
def api_status():
    return jsonify(get_status())

@app.get("/api/logs")
@require_api_key
def api_logs():
    try:
        limit = int(request.args.get("limit", "50"))
    except Exception:
        limit = 50
    return jsonify(get_logs(limit=limit))

@app.post("/api/r3/chat")
@require_api_key
def api_r3_chat():
    data = request.get_json(force=True, silent=True) or {}
    prompt = str(data.get("prompt", ""))
    domain = str(data.get("domain", "general"))
    max_tokens = int(data.get("max_tokens", 1024) or 1024)
    orch = get_orchestrator()
    res = orch.process(prompt, domain=domain, context=data.get("context") or {}, max_tokens=max_tokens)
    return jsonify(res)

@app.post("/api/r3/analyze_input")
@require_api_key
def api_r3_analyze_input():
    data = request.get_json(force=True, silent=True) or {}
    text = str(data.get("text", ""))
    cfg = load_config()
    res = input_gate.analyze(
        text,
        w_ambiguity=float(cfg.get("input_w_ambiguity", 0.20)),
        w_assertion=float(cfg.get("input_w_assertion", 0.25)),
        w_emotion=float(cfg.get("input_w_emotion", 0.30)),
        w_unrealistic=float(cfg.get("input_w_unrealistic", 0.25)),
    )
    return jsonify(res)

@app.post("/api/r3/analyze_output")
@require_api_key
def api_r3_analyze_output():
    data = request.get_json(force=True, silent=True) or {}
    text = str(data.get("text", ""))
    cfg = load_config()
    res = output_gate.analyze(
        text,
        w_assertion=float(cfg.get("output_w_assertion", 0.30)),
        w_evidence=float(cfg.get("output_w_evidence", 0.30)),
        w_contradiction=float(cfg.get("output_w_contradiction", 0.25)),
        w_provocative=float(cfg.get("output_w_provocative", 0.15)),
    )
    return jsonify(res)

@app.get("/api/r3/config")
@require_api_key
def api_r3_config():
    return jsonify(public_config(load_config()))

def main():
    cfg = load_config()
    app.run(host=cfg.get("host", "0.0.0.0"), port=int(cfg.get("port", 5001)), debug=bool(cfg.get("debug", False)))

if __name__ == "__main__":
    main()
