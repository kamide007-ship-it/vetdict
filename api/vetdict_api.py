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

from api.auth import require_internal_api_access
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
RATE_LIMIT_ERROR_MESSAGE = 'リクエスト制限に達しました。'

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
app.VERSION = VERSION  # Make VERSION available to decorators

_allowed_origins = os.getenv('CORS_ALLOWED_ORIGINS', '').strip()
if _allowed_origins:
    CORS(app, resources={r"/api/*": {"origins": _allowed_origins.split(',')}})
elif is_debug_mode_enabled():
    CORS(app)
    logger.warning("CORS_ALLOWED_ORIGINS not set — allowing all origins (debug mode only)")
else:
    CORS(app, resources={r"/api/*": {"origins": ["https://vetdict.info"]}})

ROOT_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = str(ROOT_DIR / 'templates')
STATIC_DIR = str(ROOT_DIR / 'static')

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


def _normalize_string_list(values, field_name, *, singular_name=None, require_non_empty=False):
    if not isinstance(values, list):
        return None, {'error': f'{field_name} must be a list of strings'}, 400

    normalized_values = []
    for value in values:
        if not isinstance(value, str):
            return None, {'error': f'{field_name} must contain only strings'}, 400
        normalized_value = value.strip()
        if normalized_value:
            normalized_values.append(normalized_value)

    if require_non_empty and not normalized_values:
        item_name = singular_name or field_name
        return None, {'error': f'At least one {item_name} required'}, 400

    return normalized_values, None, None


# Register blueprints
if HEALTH_CHECKER_AVAILABLE and health_bp:
    app.register_blueprint(health_bp)

if DIAGNOSTIC_CHAT_AVAILABLE and diagnostic_bp:
    app.register_blueprint(diagnostic_bp)

# PayPal subscription blueprint
try:
    from api.paypal_api import paypal_bp
    app.register_blueprint(paypal_bp)
except ImportError:
    pass

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

# Analytics blueprint (usage statistics)
try:
    from api.analytics import analytics_bp, init_analytics
    app.register_blueprint(analytics_bp)
    init_analytics()
    ANALYTICS_AVAILABLE = True
except ImportError:
    ANALYTICS_AVAILABLE = False
    logger.warning("Analytics module not available")

# Admin API blueprint (SQLite data management)
try:
    from api.routes.admin_api import admin_bp
    app.register_blueprint(admin_bp)
    ADMIN_API_AVAILABLE = True
except ImportError:
    ADMIN_API_AVAILABLE = False
    logger.warning("Admin API module not available")

# Public diseases API blueprint (SQLite read-only access)
try:
    from api.routes.diseases_api import diseases_bp
    app.register_blueprint(diseases_bp)
    DISEASES_API_AVAILABLE = True
except ImportError:
    DISEASES_API_AVAILABLE = False
    logger.warning("Diseases API module not available")

# Phase 3 Learning Insights blueprint (Continuous Learning Pipeline)
try:
    from api.learning_insights import bp as learning_insights_bp
    app.register_blueprint(learning_insights_bp)
    LEARNING_INSIGHTS_AVAILABLE = True
except ImportError:
    try:
        from learning_insights import bp as learning_insights_bp
        app.register_blueprint(learning_insights_bp)
        LEARNING_INSIGHTS_AVAILABLE = True
    except ImportError:
        LEARNING_INSIGHTS_AVAILABLE = False
        logger.warning("Learning insights (Phase 3) module not available")


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
                result.setdefault('success', True)
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
    """Add security headers to all responses."""
    # Content security headers
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'

    # Content Security Policy (prevent XSS, clickjacking, etc.)
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://www.googletagmanager.com https://www.paypal.com https://www.google-analytics.com; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:; "
        "font-src 'self' https:; "
        "connect-src 'self' https://www.google-analytics.com https://www.paypal.com https://api-m.paypal.com; "
        "frame-src https://www.paypal.com https://www.sandbox.paypal.com; "
        "frame-ancestors 'none'"
    )

    # HTTPS enforcement in production
    is_production = os.getenv('RENDER') or os.getenv('PRODUCTION')
    if is_production:
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
        response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'

    # Remove server version disclosure
    response.headers.pop('Server', None)
    response.headers.pop('X-Powered-By', None)

    # Cache policy: API responses are never cached; static files are revalidated
    path = request.path or ''
    if path.startswith('/api/') or path == '/':
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
    elif path.startswith('/static/'):
        # Immutable assets (SW handles revalidation): cache for 7 days
        if any(path.endswith(ext) for ext in ('.css', '.js', '.svg', '.png', '.woff2')):
            response.headers['Cache-Control'] = 'public, max-age=604800, stale-while-revalidate=86400'
        else:
            response.headers.setdefault('Cache-Control', 'public, max-age=3600, must-revalidate')

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


@app.route('/terms')
def terms():
    return render_template('terms.html')


@app.route('/privacy')
def privacy():
    return render_template('privacy.html')


@app.route('/tokushoho')
def tokushoho():
    return render_template('tokushoho.html')


@app.route('/favicon.ico')
def favicon():
    try:
        return send_from_directory(STATIC_DIR, 'favicon.ico')
    except (FileNotFoundError, WerkzeugNotFound):
        try:
            return send_from_directory(TEMPLATES_DIR, 'favicon.ico')
        except (FileNotFoundError, WerkzeugNotFound):
            return '', 204


@app.route('/static/<path:filename>')
def static_assets(filename):
    try:
        return send_from_directory(STATIC_DIR, filename)
    except (FileNotFoundError, WerkzeugNotFound):
        return jsonify({'error': f'{filename} not found'}), 404


@app.route('/<path:filename>')
def static_files(filename):
    try:
        return send_from_directory(STATIC_DIR, filename)
    except (FileNotFoundError, WerkzeugNotFound):
        try:
            return send_from_directory(TEMPLATES_DIR, filename)
        except (FileNotFoundError, WerkzeugNotFound):
            return jsonify({'error': f'{filename} not found'}), 404


# =============================================================================
# API: Health Check
# =============================================================================

@app.route('/api/health', methods=['GET'])
@ensure_json_response
def health():
    import shutil
    import sqlite3 as _sqlite3

    checks = {}

    # Database connectivity (optional — absence is not an error)
    try:
        from api.database import DB_PATH as _db_path
        _db_file = Path(_db_path)
        if _db_file.exists() and _db_file.stat().st_size > 0:
            _conn = _sqlite3.connect(_db_path)
            _count = _conn.execute("SELECT COUNT(*) FROM diseases").fetchone()[0]
            _conn.close()
            checks["database"] = {"status": "ok", "diseases": _count}
        else:
            checks["database"] = {"status": "ok", "detail": "not configured"}
    except Exception:
        checks["database"] = {"status": "ok", "detail": "not configured"}

    # Disk space
    try:
        usage = shutil.disk_usage("/")
        free_pct = round(usage.free / usage.total * 100, 1)
        checks["disk"] = {"status": "ok" if free_pct > 5 else "warning", "free_percent": free_pct}
    except Exception:
        checks["disk"] = {"status": "unknown"}

    has_error = any(c.get("status") == "error" for c in checks.values())
    status_str = "degraded" if has_error else "healthy"

    return {
        'status': status_str,
        'version': VERSION,
        'build': BUILD,
        'checks': checks,
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
# API: Species Stats (from SQLite)
# =============================================================================

@app.route('/api/species-stats', methods=['GET'])
@ensure_json_response
def api_species_stats():
    """各動物種の疾患数・薬品数を SQLite から返す。"""
    from api.disease_store import get_species_stats
    return get_species_stats()


# =============================================================================
# API: Species-specific Symptoms (from SQLite)
# =============================================================================

@app.route('/api/species/<species>/symptoms', methods=['GET'])
@ensure_json_response
def api_species_symptoms(species: str):
    """Return symptom list for the selected species from SQLite."""
    from api.disease_store import get_symptoms_for_species
    species_key = (species or '').lower()
    return {"symptoms": get_symptoms_for_species(species_key)}


@app.route('/api/related-symptoms/<species>', methods=['POST'])
@ensure_json_response
def get_related_symptoms(species):
    """Suggest symptoms that commonly co-occur with selected ones."""
    data = request.get_json(silent=True) or {}
    selected = data.get('symptoms', [])
    if not selected or not isinstance(selected, list):
        return {'related': []}

    species_key = (species or '').lower()

    try:
        from api.disease_store import get_symptoms_for_species
        all_symptoms = get_symptoms_for_species(species_key)
        if not all_symptoms:
            return {'related': []}

        # Build a lookup from symptom id to symptom info
        sym_lookup = {s['id']: s for s in all_symptoms}

        # Query diseases for this species to build co-occurrence
        import json as _json

        from api.database import get_connection
        with get_connection() as conn:
            rows = conn.execute(
                "SELECT symptoms FROM diseases WHERE species = ? AND symptoms IS NOT NULL",
                (species_key,),
            ).fetchall()

        if not rows:
            return {'related': []}

        selected_set = set(selected)
        co_occur: dict[str, int] = {}
        for row in rows:
            try:
                disease_symptoms = set(_json.loads(row['symptoms']))
            except (ValueError, TypeError):
                continue
            overlap = disease_symptoms & selected_set
            if overlap:
                for s in disease_symptoms - selected_set:
                    co_occur[s] = co_occur.get(s, 0) + len(overlap)

        # Sort by co-occurrence frequency, take top 5
        sorted_symptoms = sorted(co_occur.items(), key=lambda x: -x[1])[:5]

        result = []
        for sym_id, score in sorted_symptoms:
            sym_info = sym_lookup.get(sym_id)
            if sym_info:
                result.append({
                    'id': sym_id,
                    'name_ja': sym_info.get('name_ja', sym_id),
                    'name_en': sym_info.get('name_en', sym_id),
                    'score': score,
                })

        return {'related': result}
    except Exception as e:
        logger.warning(f"Related symptoms error: {e}")
        return {'related': []}


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

    symptoms, error, status = _normalize_string_list(
        data['symptoms'], 'symptoms', singular_name='symptom', require_non_empty=True
    )
    if error:
        return error, status

    # Input size limits to prevent abuse
    MAX_SYMPTOMS = 50
    MAX_STRING_LEN = 256
    MAX_VACCINES = 20
    MAX_LAB_VALUES = 50

    if len(symptoms) > MAX_SYMPTOMS:
        return {'error': f'Too many symptoms (max {MAX_SYMPTOMS})'}, 400
    if any(len(s) > MAX_STRING_LEN for s in symptoms):
        return {'error': f'Symptom ID too long (max {MAX_STRING_LEN} chars)'}, 400

    species = data.get('species', 'dog')
    if isinstance(species, str) and len(species) > MAX_STRING_LEN:
        return {'error': 'species value too long'}, 400
    age_stage = data.get('age_stage')
    breed = data.get('breed')
    if isinstance(breed, str) and len(breed) > MAX_STRING_LEN:
        return {'error': 'breed value too long'}, 400
    onset = data.get('onset')  # "acute" | "subacute" | "chronic"
    age_years = data.get('age_years')  # numeric age in years
    lab_values_raw = data.get('lab_values')  # {item_id: numeric_value}
    gender = data.get('gender')  # "male" | "female"
    vaccines_raw = data.get('vaccines', [])  # List of vaccine IDs
    vaccination_status = data.get('vaccination_status')  # "current" | "outdated" | "none"
    pain_score = data.get('pain_score')  # 0-4 (CSU Canine Acute Pain Scale)

    # Validate onset
    if onset and onset not in ('acute', 'subacute', 'chronic'):
        return {'error': "onset must be 'acute', 'subacute', or 'chronic'"}, 400

    # Validate gender
    if gender and gender not in ('male', 'female'):
        return {'error': "gender must be 'male' or 'female'"}, 400

    # Validate vaccination_status
    if vaccination_status and vaccination_status not in ('current', 'outdated', 'none'):
        return {'error': "vaccination_status must be 'current', 'outdated', or 'none'"}, 400

    # Validate pain_score (CSU Canine Pain Scale 0-4)
    if pain_score is not None:
        try:
            pain_score = int(pain_score)
            if pain_score < 0 or pain_score > 4:
                return {'error': 'pain_score must be 0-4'}, 400
        except (ValueError, TypeError):
            return {'error': 'pain_score must be an integer 0-4'}, 400

    # Coerce vaccines to list of strings
    vaccines = []
    if vaccines_raw is not None:
        vaccines, error, status = _normalize_string_list(vaccines_raw, 'vaccines')
        if error:
            return error, status
        if len(vaccines) > MAX_VACCINES:
            return {'error': f'Too many vaccines (max {MAX_VACCINES})'}, 400

    # Coerce age_years to float and validate range
    if age_years is not None:
        try:
            age_years = float(age_years)
        except (ValueError, TypeError):
            return {'error': 'age_years must be a number'}, 400
        if age_years < 0 or age_years > 100:
            return {'error': 'age_years must be between 0 and 100'}, 400

    # Coerce lab_values to {str: float}
    lab_values = None
    if lab_values_raw is not None:
        if not isinstance(lab_values_raw, dict):
            return {'error': 'lab_values must be a JSON object'}, 400
        if len(lab_values_raw) > MAX_LAB_VALUES:
            return {'error': f'Too many lab values (max {MAX_LAB_VALUES})'}, 400
        lab_values = {}
        for k, v in lab_values_raw.items():
            if not isinstance(k, str) or len(k) > MAX_STRING_LEN:
                return {'error': 'lab_values keys must be strings'}, 400
            with contextlib.suppress(ValueError, TypeError):
                lab_values[str(k)] = float(v)
        if not lab_values:
            lab_values = None

    try:
        if species == 'dog' or species is None:
            result = analyze_symptoms(
                symptoms, breed=breed, onset=onset, age_years=age_years,
                lab_values=lab_values,
                gender=gender,
                vaccines=vaccines,
                vaccination_status=vaccination_status,
                pain_score=pain_score,
            )
        else:
            if not SPECIES_ANALYZER_AVAILABLE:
                return {'error': 'Species analyzer module not available'}, 500
            result = analyze_species_symptoms(
                species, symptoms, age_stage,
                breed=breed, onset=onset, age_years=age_years,
                lab_values=lab_values,
                gender=gender,
                vaccines=vaccines,
                vaccination_status=vaccination_status,
            )
        return result
    except ValueError as ve:
        logger.error(f"Symptom analysis error: {ve}", exc_info=True)
        return {'error': str(ve)}, 400
    except Exception as e:
        logger.error(f"Symptom analysis error: {e}", exc_info=True)
        return {'error': '症状解析に失敗しました'}, 500


# =============================================================================
# API: CSU Canine Acute Pain Scale
# =============================================================================
# Based on: Colorado State University Canine Acute Pain Scale
# Reference: Mathews K et al. (2014) JSAP 55(6):E10-E68
# Japanese version: 動物臨床医学研究所 (dourinken.com)

_CSU_PAIN_SCALE = [
    {
        "score": 0,
        "level": "no_pain",
        "level_ja": "痛みなし",
        "level_en": "No Pain",
        "color": "#16a34a",
        "behavioral": "Comfortable, relaxed, sleeping or resting normally",
        "behavioral_ja": "快適で、リラックスしている。正常な睡眠・休息。",
        "body_tension": "Minimal body tension, soft abdomen, relaxed muscles",
        "body_tension_ja": "体の緊張は最小限。腹部は柔らかく、筋肉はリラックス。",
        "response_to_palpation": "No response or normal response to gentle palpation of surgical site/wound",
        "response_to_palpation_ja": "手術部位/創傷の優しい触診に対して反応なし、または正常な反応。",
        "associated_conditions": [],
    },
    {
        "score": 1,
        "level": "mild",
        "level_ja": "軽度の痛み",
        "level_en": "Mild Pain",
        "color": "#ca8a04",
        "behavioral": "Content to slightly unsettled. Distracted or interested in surroundings. May look at affected area occasionally.",
        "behavioral_ja": "おおむね落ち着いているがやや不安定。周囲に関心を示す。時折患部を見る。",
        "body_tension": "Mild body tension, may shift weight occasionally",
        "body_tension_ja": "軽度の体の緊張。時折体重移動。",
        "response_to_palpation": "Mild response to palpation — may look, flinch, or pull away slightly",
        "response_to_palpation_ja": "触診に軽度の反応 — 見る、軽くビクッとする、わずかに引く。",
        "associated_conditions": ["post_minor_surgery", "mild_otitis", "mild_dermatitis", "early_arthritis"],
    },
    {
        "score": 2,
        "level": "moderate",
        "level_ja": "中等度の痛み",
        "level_en": "Moderate Pain",
        "color": "#ea580c",
        "behavioral": "Restless, shifting positions frequently. May whimper or vocalize occasionally. Reluctant to move. Reduced appetite.",
        "behavioral_ja": "落ち着きがなく、頻繁に体位を変える。時折クンクン鳴く。動きたがらない。食欲低下。",
        "body_tension": "Moderate body tension, guarding of affected area, may tremble",
        "body_tension_ja": "中等度の体の緊張。患部を守る姿勢。震えることがある。",
        "response_to_palpation": "Moderate response — flinches, pulls away, may vocalize or turn head toward site",
        "response_to_palpation_ja": "中等度の反応 — ビクッとする、引く、鳴く、または患部の方を向く。",
        "associated_conditions": ["fracture", "pancreatitis", "intervertebral_disc_disease", "moderate_otitis", "cystitis"],
    },
    {
        "score": 3,
        "level": "severe",
        "level_ja": "強い痛み",
        "level_en": "Severe Pain",
        "color": "#dc2626",
        "behavioral": "Restless, crying, groaning, or whimpering. May bite or chew at affected area. Reluctant to move or unable to get comfortable. Depressed, unresponsive to surroundings.",
        "behavioral_ja": "落ち着きがなく、鳴き声、うめき声。患部を噛む・舐め続ける。動けない、またはどの体勢でも落ち着けない。沈鬱、周囲に無反応。",
        "body_tension": "Significant body tension, rigid abdomen, protective posture, hunched back",
        "body_tension_ja": "著しい体の緊張。腹部硬直。防御姿勢。背中を丸める。",
        "response_to_palpation": "Strong response — cries, attempts to bite, significant withdrawal, aggressive when touched near area",
        "response_to_palpation_ja": "強い反応 — 鳴く、噛もうとする、著しく引く、患部付近の接触で攻撃的。",
        "associated_conditions": ["gdv", "peritonitis", "severe_trauma", "bone_cancer", "acute_abdomen", "disc_herniation"],
    },
    {
        "score": 4,
        "level": "excruciating",
        "level_ja": "激痛",
        "level_en": "Excruciating Pain",
        "color": "#991b1b",
        "behavioral": "Prostrate, unresponsive to environment. Constant vocalization (crying, screaming). May be rigid or thrashing. Potential for shock.",
        "behavioral_ja": "伏臥、環境に無反応。絶え間ない鳴き声（叫び声）。硬直またはのたうち回る。ショックに陥る可能性。",
        "body_tension": "Extreme tension, rigid body, may be in lateral recumbency unable to rise",
        "body_tension_ja": "極度の緊張。体の硬直。横臥して起立不能の場合がある。",
        "response_to_palpation": "Extreme response or paradoxical non-response (shock state). May scream, thrash, or become completely unresponsive.",
        "response_to_palpation_ja": "極度の反応、または逆説的な無反応（ショック状態）。叫ぶ、のたうつ、または完全に無反応。",
        "associated_conditions": ["gdv", "aortic_thromboembolism", "severe_burns", "multiple_fractures", "meningitis"],
    },
]

# Pain-associated disease boost multipliers
_PAIN_DISEASE_BOOST = {
    0: {},  # No pain → no boost
    1: {"Osteoarthritis": 1.3, "Otitis Externa": 1.2, "Dermatitis": 1.15},
    2: {"Pancreatitis": 1.5, "Fracture": 1.4, "Intervertebral Disc Disease": 1.5,
        "Cystitis": 1.3, "Otitis Media": 1.3, "Gastric Foreign Body": 1.3,
        "Peritonitis": 1.2, "Osteosarcoma": 1.2},
    3: {"Gastric Dilatation-Volvulus (GDV)": 1.6, "Peritonitis": 1.5,
        "Intervertebral Disc Disease": 1.4, "Osteosarcoma": 1.5,
        "Pancreatitis": 1.4, "Meningitis": 1.4, "Panosteitis": 1.3},
    4: {"Gastric Dilatation-Volvulus (GDV)": 1.8, "Aortic Thromboembolism": 1.7,
        "Meningitis": 1.6, "Peritonitis": 1.6, "Necrotizing Fasciitis": 1.5},
}


# =============================================================================
# API: Lab Reference Ranges
# =============================================================================

@app.route('/api/lab-ranges/<species>', methods=['GET'])
@ensure_json_response
def api_lab_ranges(species):
    """Return species-specific lab reference ranges for visualization."""
    try:
        from api.species.helpers import (
            LAB_ITEM_NAMES,
            LAB_REFERENCE_RANGES,
            SPECIES_LAB_REFERENCE_RANGES,
        )
    except ImportError:
        from species.helpers import (
            LAB_ITEM_NAMES,
            LAB_REFERENCE_RANGES,
            SPECIES_LAB_REFERENCE_RANGES,
        )

    # Get species-specific ranges, fall back to dog defaults
    ranges = SPECIES_LAB_REFERENCE_RANGES.get(species, LAB_REFERENCE_RANGES)

    # Build response with names and units
    result = {}
    for item_id, thresholds in ranges.items():
        names = LAB_ITEM_NAMES.get(item_id, {"en": item_id, "ja": item_id})
        result[item_id] = {
            "low": thresholds["low_threshold"],
            "high": thresholds["high_threshold"],
            "name_en": names.get("en", item_id),
            "name_ja": names.get("ja", item_id),
        }

    return {"species": species, "ranges": result}


@app.route('/api/pain-scale', methods=['GET'])
@ensure_json_response
def api_pain_scale():
    """Return CSU Canine Acute Pain Scale data for UI rendering."""
    try:
        from api.species.helpers import CANINE_PAIN_SCALE
    except ImportError:
        from species.helpers import CANINE_PAIN_SCALE

    return {"pain_scale": {str(k): v for k, v in CANINE_PAIN_SCALE.items()}}


# =============================================================================
# API: Species Breeds
# =============================================================================

@app.route('/api/breeds/<species>', methods=['GET'])
@ensure_json_response
def api_get_breeds(species):
    """Return available breeds for a given species with ecology info."""
    try:
        from api.species.helpers import SPECIES_BREEDS
    except ImportError:
        from species.helpers import SPECIES_BREEDS
    breeds = SPECIES_BREEDS.get(species, [])
    return {
        "species": species,
        "breeds": [{
            "id": b["id"], "name": b["name"], "name_ja": b["name_ja"],
            "ecology": b.get("ecology"),
        } for b in breeds],
    }


@app.route('/api/species/<species>/common-diseases', methods=['GET'])
@ensure_json_response
def api_common_diseases(species):
    """Return common/very_common diseases for a species with Japanese names."""
    try:
        from api.species.prevalence_data import SPECIES_PREVALENCE
    except ImportError:
        from species.prevalence_data import SPECIES_PREVALENCE
    prev = SPECIES_PREVALENCE.get(species, {})
    # Load disease data to get Japanese names
    try:
        from api.diagnostic_chat import _SPECIES_DATA
    except ImportError:
        _SPECIES_DATA = {}
    sp_data = _SPECIES_DATA.get(species, {})
    diseases_list = sp_data.get("diseases", [])
    name_map = {}
    for d in diseases_list:
        name_map[d.get("name", "")] = d.get("name_ja", "")
    result = []
    for name, tier in prev.items():
        if tier in ("very_common", "common"):
            result.append({
                "name": name,
                "name_ja": name_map.get(name, ""),
                "prevalence": tier,
            })
    # Sort: very_common first, then common
    result.sort(key=lambda x: (0 if x["prevalence"] == "very_common" else 1, x["name"]))
    return {"species": species, "common_diseases": result}


# =============================================================================
# API: RECO2 / RECO3 (AI Integrity Control)
# =============================================================================

@app.route('/api/status', methods=['GET'])
@ensure_json_response
@require_internal_api_access
def reco2_status_route():
    if not RECO2_AVAILABLE:
        return {'error': 'reco2 not available'}, 503
    return reco2_get_status()


@app.route('/api/logs', methods=['GET'])
@ensure_json_response
@require_internal_api_access
def reco2_logs_route():
    if not RECO2_AVAILABLE:
        return {'error': 'reco2 not available'}, 503
    try:
        limit = int(request.args.get('limit', '50'))
    except Exception:
        limit = 50
    return reco2_get_logs(limit=limit)


@app.route('/api/evaluate', methods=['POST'])
@ensure_json_response
@require_internal_api_access
def reco2_evaluate_route():
    if not RECO2_AVAILABLE:
        return {'error': 'reco2 not available'}, 503
    payload = request.get_json(force=True, silent=False)
    return reco2_evaluate_payload(payload)


@app.route('/api/feedback', methods=['POST'])
@ensure_json_response
@require_internal_api_access
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
@require_internal_api_access
def reco2_patrol_route():
    if not RECO2_AVAILABLE:
        return {'error': 'reco2 not available'}, 503
    return reco2_patrol(manual=True)


@app.route('/api/r3/analyze_input', methods=['POST'])
@ensure_json_response
@require_internal_api_access
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
@require_internal_api_access
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
@require_internal_api_access
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
@require_internal_api_access
def reco3_config():
    if not RECO2_AVAILABLE:
        return {'error': 'reco2 not available'}, 503
    return public_reco2_config(load_reco2_config())


# =============================================================================
# API: Admin Token Verification
# =============================================================================

@app.route('/api/admin/verify', methods=['POST'])
def verify_admin():
    """Server-side admin token verification."""
    body = request.get_json(silent=True) or {}
    token = body.get('token', '')
    admin_token = os.getenv('ADMIN_TOKEN', '')
    if not admin_token:
        return jsonify({'valid': False}), 403
    import hmac
    if hmac.compare_digest(token, admin_token):
        return jsonify({'valid': True})
    return jsonify({'valid': False}), 403


# =============================================================================
# Error Handlers
# =============================================================================

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found', 'version': VERSION}), 404

@app.errorhandler(429)
def rate_limited(e):
    return jsonify({'error': RATE_LIMIT_ERROR_MESSAGE, 'version': VERSION}), 429

@app.errorhandler(500)
def server_error(e):
    logger.error(f"500: {e}", exc_info=True)
    return jsonify({'error': 'Internal server error', 'version': VERSION}), 500


# =============================================================================
# API v1 aliases — versioned endpoints pointing to existing handlers
# =============================================================================

app.add_url_rule('/api/v1/health', endpoint='v1_health', view_func=health, methods=['GET'])
app.add_url_rule('/api/v1/species-stats', endpoint='v1_species_stats', view_func=api_species_stats, methods=['GET'])
app.add_url_rule('/api/v1/analyze-symptoms', endpoint='v1_analyze_symptoms', view_func=api_analyze_symptoms, methods=['POST'])
app.add_url_rule('/api/v1/breeds/<species>', endpoint='v1_breeds', view_func=api_get_breeds, methods=['GET'])

if SYMPTOM_CHECKER_AVAILABLE:
    app.add_url_rule('/api/v1/species/<species>/symptoms', endpoint='v1_species_symptoms', view_func=api_species_symptoms, methods=['GET'])


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
