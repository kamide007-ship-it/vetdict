#!/usr/bin/env python3
"""
VetDict — Multi-Species Veterinary Diagnostic Platform

Provides:
  - Symptom checker (checkbox-based) for 20+ animal species
  - Differential diagnosis engine
  - Diagnostic chat interface
  - RECO2/RECO3 AI integrity control layer
"""

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
else:
    CORS(app)

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
    from api.health_checker import SYMPTOMS as ALL_SYMPTOMS
    from api.health_checker import health_bp
    HEALTH_CHECKER_AVAILABLE = True
except ImportError:
    try:
        from health_checker import SYMPTOMS as ALL_SYMPTOMS
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
        "script-src 'self' 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:; "
        "font-src 'self'; "
        "connect-src 'self'; "
        "frame-ancestors 'none'"
    )

    # HTTPS enforcement in production
    is_production = os.getenv('RENDER') or os.getenv('PRODUCTION')
    if is_production:
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
        response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'

    # Remove server version disclosure
    response.headers.pop('Server', None)

    # Cache policy: API responses are never cached; static files are revalidated
    path = request.path or ''
    if path.startswith('/api/') or path == '/':
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
    elif path.startswith('/static/'):
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

    # Database connectivity
    try:
        from api.database import DB_PATH as _db_path
        if Path(_db_path).exists():
            _conn = _sqlite3.connect(_db_path)
            _count = _conn.execute("SELECT COUNT(*) FROM diseases").fetchone()[0]
            _conn.close()
            checks["database"] = {"status": "ok", "diseases": _count}
        else:
            checks["database"] = {"status": "ok", "detail": "not configured"}
    except Exception as e:
        checks["database"] = {"status": "error", "detail": str(e)}

    # Disk space
    try:
        usage = shutil.disk_usage("/")
        free_pct = round(usage.free / usage.total * 100, 1)
        checks["disk"] = {"status": "ok" if free_pct > 5 else "warning", "free_percent": free_pct}
    except Exception:
        checks["disk"] = {"status": "unknown"}

    all_ok = all(c.get("status") == "ok" for c in checks.values())
    status_str = "healthy" if all_ok else "degraded"

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
# API: Species Stats (dynamic disease/drug counts)
# =============================================================================

@app.route('/api/species-stats', methods=['GET'])
@ensure_json_response
def api_species_stats():
    """各動物種の疾患数・薬品数を動的に返す。"""
    stats = []
    species_modules = {
        "dog": ("犬", "Dog", "symptom_checker"),
        "cat": ("猫", "Cat", "cat_diseases"),
        "horse": ("馬", "Horse", "equine_diseases"),
        "rabbit": ("うさぎ", "Rabbit", "rabbit_diseases"),
        "hamster": ("ハムスター", "Hamster", "hamster_diseases"),
        "guinea_pig": ("モルモット", "Guinea Pig", "guinea_pig_diseases"),
        "chinchilla": ("チンチラ", "Chinchilla", "chinchilla_diseases"),
        "ferret": ("フェレット", "Ferret", "ferret_diseases"),
        "hedgehog": ("ハリネズミ", "Hedgehog", "hedgehog_diseases"),
        "sugar_glider": ("フクロモモンガ", "Sugar Glider", "sugar_glider_diseases"),
        "degu": ("デグー", "Degu", "degu_diseases"),
        "bird": ("鳥", "Bird", "bird_diseases"),
        "parakeet": ("インコ", "Parakeet", "parakeet_diseases"),
        "parrot": ("オウム", "Parrot", "parrot_diseases"),
        "reptile": ("爬虫類", "Reptile", "reptile_diseases"),
        "tortoise": ("リクガメ", "Tortoise", "tortoise_diseases"),
        "snake": ("ヘビ", "Snake", "snake_diseases"),
        "lizard": ("トカゲ", "Lizard", "lizard_diseases"),
        "amphibian": ("両生類", "Amphibian", "amphibian_diseases"),
        "exotic_other": ("その他エキゾチック", "Exotic Other", "exotic_other_diseases"),
    }

    drug_counts = {}
    try:
        from api.drug_dictionary import DRUGS
        for d in DRUGS:
            for sp in (d.get("species_info") or {}):
                drug_counts[sp] = drug_counts.get(sp, 0) + 1
    except Exception:
        pass

    for sp_id, (name_ja, name_en, module_name) in species_modules.items():
        disease_count = 0
        try:
            if sp_id == "dog":
                from api.symptom_checker import _DISEASE_DB as dog_diseases
                disease_count = len(dog_diseases)
            elif sp_id == "horse":
                from api.species.equine_diseases import DISEASE_DATABASE
                disease_count = len(DISEASE_DATABASE)
            else:
                import importlib
                mod = importlib.import_module(f"api.species.{module_name}")
                disease_count = len(getattr(mod, "DISEASES", []))
        except Exception:
            pass
        stats.append({
            "id": sp_id,
            "name": name_ja,
            "nameEn": name_en,
            "diseases": disease_count,
            "drugs": drug_counts.get(sp_id, 0),
        })

    total_diseases = sum(s["diseases"] for s in stats)
    total_drugs = 0
    try:
        from api.drug_dictionary import DRUGS
        total_drugs = len(DRUGS)
    except Exception:
        pass

    return {
        "species": stats,
        "total_diseases": total_diseases,
        "total_drugs": total_drugs,
        "total_species": len(stats),
    }


# =============================================================================
# API: Species-specific Symptoms
# =============================================================================

@app.route('/api/species/<species>/symptoms', methods=['GET'])
@ensure_json_response
def api_species_symptoms(species: str):
    """Return symptom list relevant to the selected species."""
    species_key = (species or '').lower()
    species_modules = {
        "cat": "cat_diseases",
        "rabbit": "rabbit_diseases",
        "hamster": "hamster_diseases",
        "chinchilla": "chinchilla_diseases",
        "guinea_pig": "guinea_pig_diseases",
        "ferret": "ferret_diseases",
        "hedgehog": "hedgehog_diseases",
        "sugar_glider": "sugar_glider_diseases",
        "degu": "degu_diseases",
        "bird": "bird_diseases",
        "parakeet": "parakeet_diseases",
        "parrot": "parrot_diseases",
        "reptile": "reptile_diseases",
        "tortoise": "tortoise_diseases",
        "snake": "snake_diseases",
        "lizard": "lizard_diseases",
        "amphibian": "amphibian_diseases",
        "exotic_other": "exotic_other_diseases",
    }
    diseases = []
    species_module = None
    try:
        if species_key == "dog":
            from api.symptom_checker import _DISEASE_DB as dog_db
            diseases = dog_db
        elif species_key == "horse":
            from api.species.equine_diseases import DISEASE_DATABASE
            diseases = DISEASE_DATABASE
        else:
            mod_name = species_modules.get(species_key)
            if mod_name is None:
                return {"symptoms": []}
            import importlib
            species_module = importlib.import_module(f"api.species.{mod_name}")
            diseases = getattr(species_module, "DISEASES", [])
    except Exception:
        return {"symptoms": []}

    unique_syms = set()
    for dis in diseases:
        if isinstance(dis, dict):
            syms = dis.get("symptoms", [])
        else:
            syms = getattr(dis, "symptoms", []) or getattr(dis, "observations", []) or getattr(dis, "associated_findings", [])
        if isinstance(syms, (set, list, tuple)):
            unique_syms.update(syms)
    id_to_info = {s["id"]: s for s in ALL_SYMPTOMS}

    def merge_symptom_names(symptom_names):
        if not isinstance(symptom_names, dict):
            return
        for symptom_id, names in symptom_names.items():
            if not isinstance(names, dict):
                continue
            current = id_to_info.get(symptom_id, {"id": symptom_id, "category": "other"})
            id_to_info[symptom_id] = {
                "id": symptom_id,
                "name_ja": names.get("ja") or current.get("name_ja") or symptom_id,
                "name_en": names.get("en") or current.get("name_en") or symptom_id,
                "category": current.get("category") or "other",
            }

    # Horse has an expanded symptom namespace that is not fully covered by
    # generic SYMPTOMS. Merge equine labels so UI does not fall back to raw IDs.
    if species_key == "horse":
        try:
            from api.species.equine_diseases import HEALTH_CHECK_ITEMS

            for category, items in HEALTH_CHECK_ITEMS.items():
                for symptom_id, name_ja, name_en in items:
                    id_to_info[symptom_id] = {
                        "id": symptom_id,
                        "name_ja": name_ja,
                        "name_en": name_en,
                        "category": category,
                    }
        except Exception:
            pass
    elif species_key == "dog":
        try:
            from api.symptom_checker import _SYMPTOM_NAMES

            merge_symptom_names(_SYMPTOM_NAMES)
        except Exception:
            pass
    elif species_module is not None:
        merge_symptom_names(getattr(species_module, "SYMPTOM_NAMES", None))

    result = []
    for sid in sorted(unique_syms):
        info = id_to_info.get(sid)
        if info is None:
            result.append({"id": sid, "name_ja": sid, "name_en": sid, "category": "other"})
        else:
            result.append(info)
    return {"symptoms": result}


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

    species = data.get('species', 'dog')
    age_stage = data.get('age_stage')
    breed = data.get('breed')
    onset = data.get('onset')  # "acute" | "subacute" | "chronic"
    age_years = data.get('age_years')  # numeric age in years
    lab_values_raw = data.get('lab_values')  # {item_id: numeric_value}
    gender = data.get('gender')  # "male" | "female"
    vaccines_raw = data.get('vaccines', [])  # List of vaccine IDs
    vaccination_status = data.get('vaccination_status')  # "current" | "outdated" | "none"

    # Validate onset
    if onset and onset not in ('acute', 'subacute', 'chronic'):
        return {'error': "onset must be 'acute', 'subacute', or 'chronic'"}, 400

    # Validate gender
    if gender and gender not in ('male', 'female'):
        return {'error': "gender must be 'male' or 'female'"}, 400

    # Validate vaccination_status
    if vaccination_status and vaccination_status not in ('current', 'outdated', 'none'):
        return {'error': "vaccination_status must be 'current', 'outdated', or 'none'"}, 400

    # Coerce vaccines to list of strings
    vaccines = []
    if vaccines_raw is not None:
        vaccines, error, status = _normalize_string_list(vaccines_raw, 'vaccines')
        if error:
            return error, status

    # Coerce age_years to float
    if age_years is not None:
        try:
            age_years = float(age_years)
        except (ValueError, TypeError):
            return {'error': 'age_years must be a number'}, 400

    # Coerce lab_values to {str: float}
    lab_values = None
    if lab_values_raw and isinstance(lab_values_raw, dict):
        lab_values = {}
        for k, v in lab_values_raw.items():
            try:
                lab_values[str(k)] = float(v)
            except (ValueError, TypeError):
                continue
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
# API: Species Breeds
# =============================================================================

@app.route('/api/breeds/<species>', methods=['GET'])
@ensure_json_response
def api_get_breeds(species):
    """Return available breeds for a given species."""
    try:
        from api.species.helpers import SPECIES_BREEDS
    except ImportError:
        from species.helpers import SPECIES_BREEDS
    breeds = SPECIES_BREEDS.get(species, [])
    return {
        "species": species,
        "breeds": [{"id": b["id"], "name": b["name"], "name_ja": b["name_ja"]} for b in breeds],
    }


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
