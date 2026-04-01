#!/usr/bin/env python3
"""
VetDict — Multi-Species Veterinary Diagnostic Platform

Provides:
  - Symptom checker (checkbox-based) for 20+ animal species
  - Differential diagnosis engine
  - Diagnostic chat interface
  - RECO2/RECO3 AI integrity control layer
"""

import contextlib
import logging
import os
from functools import wraps
from pathlib import Path

from flask import Flask, jsonify, render_template, request, send_from_directory
from flask_cors import CORS
from werkzeug.exceptions import NotFound as WerkzeugNotFound

from api.debug_config import is_debug_mode_enabled

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s: %(message)s')
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
VERSION = "5.0.0"
BUILD = "2026-03-07"

# ---------------------------------------------------------------------------
# Flask App
# ---------------------------------------------------------------------------
app = Flask(__name__, static_folder=None, template_folder=str(Path(__file__).resolve().parent.parent / 'templates'))
app.config['DEBUG'] = is_debug_mode_enabled()
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB
_secret = os.getenv('SECRET_KEY') or os.getenv('FLASK_SECRET_KEY')
if not _secret:
    if is_debug_mode_enabled():
        _secret = 'dev-only-insecure-key'
        logger.warning("SECRET_KEY not set — using insecure default (debug mode only)")
    else:
        raise RuntimeError(
            "SECRET_KEY environment variable is required in production. "
            "Set SECRET_KEY or FLASK_SECRET_KEY before starting the application."
        )
app.secret_key = _secret

_allowed_origins = os.getenv('CORS_ALLOWED_ORIGINS', '').strip()
if _allowed_origins:
    CORS(app, resources={r"/api/*": {"origins": _allowed_origins.split(',')}})
else:
    CORS(app)

ROOT_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = str(ROOT_DIR / 'templates')
STATIC_DIR = str(ROOT_DIR / 'templates')

# ---------------------------------------------------------------------------
# Module imports — graceful degradation
# ---------------------------------------------------------------------------

# Symptom checker (dog)
try:
    from api.symptom_checker import analyze_symptoms
    SYMPTOM_CHECKER_AVAILABLE = True
except ImportError:
    try:
        from symptom_checker import analyze_symptoms
        SYMPTOM_CHECKER_AVAILABLE = True
    except ImportError:
        SYMPTOM_CHECKER_AVAILABLE = False
        analyze_symptoms = None
        logger.warning("Symptom checker module not available")

# Multi-species analyzer
try:
    from api.species_analyzer import analyze_species_symptoms
    SPECIES_ANALYZER_AVAILABLE = True
except ImportError:
    try:
        from species_analyzer import analyze_species_symptoms
        SPECIES_ANALYZER_AVAILABLE = True
    except ImportError:
        SPECIES_ANALYZER_AVAILABLE = False
        analyze_species_symptoms = None
        logger.warning("Species analyzer module not available")

# Health checker blueprint (checkbox UI)
try:
    from api.health_checker import health_bp
    HEALTH_CHECKER_AVAILABLE = True
except ImportError:
    try:
        from health_checker import health_bp
        HEALTH_CHECKER_AVAILABLE = True
    except ImportError:
        health_bp = None
        HEALTH_CHECKER_AVAILABLE = False
        logger.warning("Health checker module not available")

# Diagnostic chat blueprint
try:
    from api.diagnostic_chat import diagnostic_bp
    DIAGNOSTIC_CHAT_AVAILABLE = True
except ImportError:
    try:
        from diagnostic_chat import diagnostic_bp
        DIAGNOSTIC_CHAT_AVAILABLE = True
    except ImportError:
        diagnostic_bp = None
        DIAGNOSTIC_CHAT_AVAILABLE = False
        logger.warning("Diagnostic chat module not available")

# RECO2/RECO3 AI integrity layer
try:
    from reco2 import input_gate, output_gate
    from reco2.config import load_config as load_reco2_config
    from reco2.config import public_config as public_reco2_config
    from reco2.engine import evaluate_payload as reco2_evaluate_payload
    from reco2.engine import get_logs as reco2_get_logs
    from reco2.engine import get_status as reco2_get_status
    from reco2.engine import patrol as reco2_patrol
    from reco2.engine import record_feedback as reco2_record_feedback
    from reco2.orchestrator import get_orchestrator as reco2_get_orchestrator
    RECO2_AVAILABLE = True
except ImportError:
    RECO2_AVAILABLE = False
    logger.warning("RECO2 module not available")

# Register blueprints
if HEALTH_CHECKER_AVAILABLE and health_bp:
    app.register_blueprint(health_bp)

if DIAGNOSTIC_CHAT_AVAILABLE and diagnostic_bp:
    app.register_blueprint(diagnostic_bp)

# Drug dictionary blueprint
try:
    from api.drug_dictionary import drug_bp
    app.register_blueprint(drug_bp)
    DRUG_DICTIONARY_AVAILABLE = True
except ImportError:
    try:
        from drug_dictionary import drug_bp
        app.register_blueprint(drug_bp)
        DRUG_DICTIONARY_AVAILABLE = True
    except ImportError:
        DRUG_DICTIONARY_AVAILABLE = False
        logger.warning("Drug dictionary module not available")


# ---------------------------------------------------------------------------
# Decorators
# ---------------------------------------------------------------------------

def ensure_json_response(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            result = f(*args, **kwargs)
            if hasattr(result, 'status_code'):
                return result
            if isinstance(result, tuple):
                body = result[0]
                status = result[1] if len(result) > 1 else 200
                if isinstance(body, dict):
                    body.setdefault('success', status < 400)
                    body.setdefault('version', VERSION)
                    resp = jsonify(body)
                    resp.status_code = status
                    return resp
                return result
            if isinstance(result, dict):
                result.setdefault('version', VERSION)
                return jsonify(result)
            return result
        except Exception as e:
            logger.error(f"Error in {f.__name__}: {e}", exc_info=True)
            is_production = os.getenv('RENDER') or os.getenv('PRODUCTION')
            error_msg = 'エラーが発生しました。しばらくしてからもう一度お試しください。' if is_production else str(e)
            return jsonify({'success': False, 'error': error_msg, 'version': VERSION}), 500
    return wrapper


# ---------------------------------------------------------------------------
# Security headers
# ---------------------------------------------------------------------------

@app.after_request
def add_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    if os.getenv('RENDER') or os.getenv('PRODUCTION'):
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response


# =============================================================================
# Static Files
# =============================================================================

@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception:
        return jsonify({'error': 'index.html not found'}), 404


@app.route('/favicon.ico')
def favicon():
    try:
        return send_from_directory(STATIC_DIR, 'favicon.ico')
    except (FileNotFoundError, WerkzeugNotFound):
        return '', 204


@app.route('/<path:filename>')
def static_files(filename):
    try:
        return send_from_directory(STATIC_DIR, filename)
    except (FileNotFoundError, WerkzeugNotFound):
        return jsonify({'error': f'{filename} not found'}), 404


# =============================================================================
# API: Health Check
# =============================================================================

@app.route('/api/health', methods=['GET'])
@ensure_json_response
def health():
    return {
        'status': 'healthy',
        'version': VERSION,
        'build': BUILD,
        'features': {
            'symptom_checker': SYMPTOM_CHECKER_AVAILABLE,
            'species_analyzer': SPECIES_ANALYZER_AVAILABLE,
            'health_checker': HEALTH_CHECKER_AVAILABLE,
            'diagnostic_chat': DIAGNOSTIC_CHAT_AVAILABLE,
            'drug_dictionary': DRUG_DICTIONARY_AVAILABLE,
            'reco2': RECO2_AVAILABLE,
        },
    }


# =============================================================================
# API: Symptom Analysis (multi-species)
# =============================================================================

@app.route('/api/analyze-symptoms', methods=['POST'])
@ensure_json_response
def api_analyze_symptoms():
    """症状チェック → 疾患・検査リスト（全動物種対応）"""
    if not SYMPTOM_CHECKER_AVAILABLE:
        return {'error': 'Symptom checker module not available'}, 500

    data = request.get_json(silent=True)
    if not data or 'symptoms' not in data:
        return {'error': 'symptoms list required'}, 400

    symptoms = data['symptoms']
    if not isinstance(symptoms, list) or len(symptoms) == 0:
        return {'error': 'At least one symptom required'}, 400

    species = data.get('species', 'dog')
    age_stage = data.get('age_stage')
    breed = data.get('breed')
    onset = data.get('onset')
    gender = data.get('gender')

    # Parse age_years safely
    age_years = data.get('age_years')
    if age_years is not None:
        try:
            age_years = float(age_years)
        except (ValueError, TypeError):
            age_years = None

    # Parse lab_values safely: coerce to {str: float}
    raw_lab = data.get('lab_values')
    lab_values = None
    if isinstance(raw_lab, dict):
        lab_values = {}
        for k, v in raw_lab.items():
            with contextlib.suppress(ValueError, TypeError):
                lab_values[str(k)] = float(v)
        if not lab_values:
            lab_values = None

    # Parse vaccination fields
    vaccines = data.get('vaccines')
    vaccination_status = data.get('vaccination_status')

    try:
        if species == 'dog' or species is None:
            result = analyze_symptoms(
                symptoms,
                breed=breed,
                onset=onset,
                age_years=age_years,
                lab_values=lab_values,
                gender=gender,
                vaccines=vaccines,
                vaccination_status=vaccination_status,
            )
        else:
            if not SPECIES_ANALYZER_AVAILABLE:
                return {'error': 'Species analyzer module not available'}, 500
            result = analyze_species_symptoms(
                species, symptoms, age_stage,
                breed=breed,
                onset=onset,
                age_years=age_years,
                lab_values=lab_values,
                gender=gender,
            )
        return result
    except ValueError as ve:
        logger.error(f"Symptom analysis error: {ve}", exc_info=True)
        return {'error': str(ve)}, 400
    except Exception as e:
        logger.error(f"Symptom analysis error: {e}", exc_info=True)
        return {'error': '症状解析に失敗しました'}, 500


# =============================================================================
# API: RECO2 / RECO3 (AI Integrity Control)
# =============================================================================

@app.route('/api/status', methods=['GET'])
@ensure_json_response
def reco2_status_route():
    if not RECO2_AVAILABLE:
        return {'error': 'reco2 not available'}, 503
    return reco2_get_status()


@app.route('/api/logs', methods=['GET'])
@ensure_json_response
def reco2_logs_route():
    if not RECO2_AVAILABLE:
        return {'error': 'reco2 not available'}, 503
    try:
        limit = max(1, min(int(request.args.get('limit', '50')), 500))
    except (ValueError, TypeError):
        limit = 50
    return reco2_get_logs(limit=limit)


@app.route('/api/evaluate', methods=['POST'])
@ensure_json_response
def reco2_evaluate_route():
    if not RECO2_AVAILABLE:
        return {'error': 'reco2 not available'}, 503
    payload = request.get_json(force=True, silent=False)
    return reco2_evaluate_payload(payload)


@app.route('/api/feedback', methods=['POST'])
@ensure_json_response
def reco2_feedback_route():
    if not RECO2_AVAILABLE:
        return {'error': 'reco2 not available'}, 503
    payload = request.get_json(force=True, silent=True) or {}
    res = reco2_record_feedback(payload)
    if isinstance(res, tuple):
        return res[0], res[1]
    return res


@app.route('/api/patrol', methods=['POST'])
@ensure_json_response
def reco2_patrol_route():
    if not RECO2_AVAILABLE:
        return {'error': 'reco2 not available'}, 503
    return reco2_patrol(manual=True)


@app.route('/api/r3/analyze_input', methods=['POST'])
@ensure_json_response
def reco3_analyze_input():
    if not RECO2_AVAILABLE:
        return {'error': 'reco2 not available'}, 503
    data = request.get_json(force=True, silent=True) or {}
    text = str(data.get('text', ''))
    cfg = load_reco2_config()
    return input_gate.analyze(
        text,
        w_ambiguity=float(cfg.get('input_w_ambiguity', 0.20)),
        w_assertion=float(cfg.get('input_w_assertion', 0.25)),
        w_emotion=float(cfg.get('input_w_emotion', 0.30)),
        w_unrealistic=float(cfg.get('input_w_unrealistic', 0.25)),
    )


@app.route('/api/r3/analyze_output', methods=['POST'])
@ensure_json_response
def reco3_analyze_output():
    if not RECO2_AVAILABLE:
        return {'error': 'reco2 not available'}, 503
    data = request.get_json(force=True, silent=True) or {}
    text = str(data.get('text', ''))
    cfg = load_reco2_config()
    return output_gate.analyze(
        text,
        w_assertion=float(cfg.get('output_w_assertion', 0.30)),
        w_evidence=float(cfg.get('output_w_evidence', 0.30)),
        w_contradiction=float(cfg.get('output_w_contradiction', 0.25)),
        w_provocative=float(cfg.get('output_w_provocative', 0.15)),
    )


@app.route('/api/r3/chat', methods=['POST'])
@ensure_json_response
def reco3_chat():
    if not RECO2_AVAILABLE:
        return {'error': 'reco2 not available'}, 503
    data = request.get_json(force=True, silent=True) or {}
    prompt = str(data.get('prompt', ''))
    domain = str(data.get('domain', 'general'))
    max_tokens = int(data.get('max_tokens', 1024) or 1024)
    orch = reco2_get_orchestrator()
    return orch.process(prompt, domain=domain, context=data.get('context') or {}, max_tokens=max_tokens)


@app.route('/api/r3/config', methods=['GET'])
@ensure_json_response
def reco3_config():
    if not RECO2_AVAILABLE:
        return {'error': 'reco2 not available'}, 503
    return public_reco2_config(load_reco2_config())


# =============================================================================
# Error Handlers
# =============================================================================

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found', 'version': VERSION}), 404

@app.errorhandler(429)
def rate_limited(e):
    return jsonify({'error': 'リクエスト制限に達しました。', 'version': VERSION}), 429

@app.errorhandler(500)
def server_error(e):
    logger.error(f"500: {e}", exc_info=True)
    return jsonify({'error': 'Internal server error', 'version': VERSION}), 500


# =============================================================================
# Main
# =============================================================================

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    logger.info(f"VetDict v{VERSION} starting on port {port}")
    logger.info(f"Symptom checker: {SYMPTOM_CHECKER_AVAILABLE}")
    logger.info(f"Species analyzer: {SPECIES_ANALYZER_AVAILABLE}")
    logger.info(f"Health checker: {HEALTH_CHECKER_AVAILABLE}")
    logger.info(f"Diagnostic chat: {DIAGNOSTIC_CHAT_AVAILABLE}")
    logger.info(f"RECO2: {RECO2_AVAILABLE}")
    app.run(host='0.0.0.0', port=port, debug=is_debug_mode_enabled())
