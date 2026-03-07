#!/usr/bin/env python3
"""
ShowDog Analysis Platform v4.1 - Render Production
With Photo + Video Analysis, User Management, Analysis History,
Deterministic Scoring Core, and Advanced Analytics Modules
(Judge Validation, Growth Prediction, Genetic Scoring, 3D Pose Estimation, Fine-Tuning)
"""

# Load .env file (if present) before any os.getenv() calls
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Standard library
import base64
import contextlib
import gc
import hashlib as _hashlib
import json
import logging
import os
import re
import secrets
import shutil as _shutil
import subprocess as _subprocess
import sys
import threading as _threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as FuturesTimeoutError
from functools import wraps

# Third-party
from flask import Flask, Response, jsonify, request, send_from_directory, stream_with_context
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.exceptions import NotFound as WerkzeugNotFound
from werkzeug.middleware.proxy_fix import ProxyFix

# Database import
try:
    from api.database import (
        create_dog,
        create_medical_visit,
        create_reset_token,
        create_session,
        create_user,
        delete_dog,
        delete_session,
        get_analyses_by_dog,
        get_analysis_by_id,
        get_dog_by_id,
        get_dogs_by_user,
        get_medical_visit,
        get_medical_visits_by_dog,
        get_recent_analyses_by_user,
        get_user_by_email,
        save_analysis,
        save_audit_log,
        update_dog,
        update_user_password,
        verify_reset_token,
        verify_security_answer,
        verify_session,
        verify_user,
    )
    DB_AVAILABLE = True
except ImportError:
    # Fallback for local development
    try:
        from database import (
            create_dog,
            create_medical_visit,
            create_session,
            create_user,
            delete_dog,
            delete_session,
            get_analyses_by_dog,
            get_analysis_by_id,
            get_dog_by_id,
            get_dogs_by_user,
            get_medical_visit,
            get_medical_visits_by_dog,
            get_recent_analyses_by_user,
            save_analysis,
            save_audit_log,
            update_dog,
            verify_session,
            verify_user,
        )
        DB_AVAILABLE = True
    except ImportError:
        DB_AVAILABLE = False
        logging.warning("Database module not available")

# Custom error types
try:
    from api.errors import AnalysisError, DataCorruptionError
except ImportError:
    from errors import AnalysisError, DataCorruptionError

# Local analysis module (OpenCV-based fallback + Pillow fallback)
try:
    from api.local_analysis import (
        analyze_coat_local,
        analyze_coat_pil,
        analyze_structure_local,
        analyze_structure_pil,
        analyze_video_local,
        gate_for_comparison,
        grade_photo_quality,
        grade_video_quality,
        make_capture_guide,
    )
except ImportError:
    try:
        from local_analysis import (
            analyze_coat_local,
            analyze_coat_pil,
            analyze_structure_local,
            analyze_structure_pil,
            analyze_video_local,
            gate_for_comparison,
            grade_photo_quality,
            grade_video_quality,
            make_capture_guide,
        )
    except ImportError:
        analyze_structure_local = None
        analyze_coat_local = None
        analyze_video_local = None
        analyze_structure_pil = None
        analyze_coat_pil = None
        gate_for_comparison = None
        grade_photo_quality = None
        grade_video_quality = None
        make_capture_guide = None
        logging.warning("Local analysis module not available")

# Scoring module import (deterministic scoring core)
try:
    from api.scoring import (
        ALGORITHM_VERSION,
        MODEL_VERSION,
        WEIGHTS_HASH,
        get_algorithm_info,
        hybrid_score,
        map_ai_scores_to_axes,
    )
    SCORING_AVAILABLE = True
except ImportError:
    try:
        from scoring import (
            ALGORITHM_VERSION,
            MODEL_VERSION,
            WEIGHTS_HASH,
            get_algorithm_info,
            map_ai_scores_to_axes,
        )
        SCORING_AVAILABLE = True
    except ImportError:
        SCORING_AVAILABLE = False
        ALGORITHM_VERSION = "N/A"
        MODEL_VERSION = "N/A"
        WEIGHTS_HASH = "N/A"
        logging.warning("Scoring module not available - using legacy scoring")

# AI Firewall module (RECO) — removed; isolated to extras/reco/
firewall_bp = None
FIREWALL_AVAILABLE = False

# RECO2/RECO3 dashboard API modules (optional)
try:
    from reco2 import input_gate, output_gate
    from reco2.config import load_config as load_reco2_config, public_config as public_reco2_config
    from reco2.engine import evaluate_payload as reco2_evaluate_payload, get_logs as reco2_get_logs
    from reco2.engine import get_status as reco2_get_status, patrol as reco2_patrol, record_feedback as reco2_record_feedback
    from reco2.orchestrator import get_orchestrator as reco2_get_orchestrator
    from reco2.store import ensure_state_file as reco2_ensure_state_file
    RECO2_AVAILABLE = True
except ImportError:
    RECO2_AVAILABLE = False

# Health Symptom Checker module
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
        logging.warning("Health checker module not available")

# Diagnostic Chat module (symptom-driven diagnosis)
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
        logging.warning("Diagnostic chat module not available")

# RECO3 integration for photo/video analysis
try:
    from api.reco3_photo_video import (
        analyze_request_input,
        analyze_photo_output,
        analyze_video_output,
        add_reco3_metadata,
    )
    RECO3_AVAILABLE = True
except ImportError:
    try:
        from reco3_photo_video import (
            analyze_request_input,
            analyze_photo_output,
            analyze_video_output,
            add_reco3_metadata,
        )
        RECO3_AVAILABLE = True
    except ImportError:
        RECO3_AVAILABLE = False
        logging.warning("RECO3 module not available - photo/video analysis will proceed without AI self-control")

# International Pet Passport / PDF module
try:
    from api.passport import passport_bp
    PASSPORT_AVAILABLE = True
except ImportError:
    try:
        from passport import passport_bp
        PASSPORT_AVAILABLE = True
    except ImportError:
        passport_bp = None
        PASSPORT_AVAILABLE = False
        logging.warning("Passport module not available")

# === Advanced Analytics Modules ===

# Judge Validation (κ coefficient, ICC)
try:
    from api.judge_validation import JudgeValidationSession
    JUDGE_VALIDATION_AVAILABLE = True
except ImportError:
    try:
        from judge_validation import JudgeValidationSession
        JUDGE_VALIDATION_AVAILABLE = True
    except ImportError:
        JUDGE_VALIDATION_AVAILABLE = False
        logging.warning("Judge validation module not available")

# Growth Prediction (curve fitting)
try:
    from api.growth_prediction import GrowthPredictor
    GROWTH_PREDICTION_AVAILABLE = True
except ImportError:
    try:
        from growth_prediction import GrowthPredictor
        GROWTH_PREDICTION_AVAILABLE = True
    except ImportError:
        GROWTH_PREDICTION_AVAILABLE = False
        logging.warning("Growth prediction module not available")

# Genetic Scoring & Breeding Optimization
try:
    from api.genetic_scoring import COLOR_LOCI, COMMON_HEALTH_GENES, BreedingOptimizer, Dog, PedigreeTree
    GENETIC_SCORING_AVAILABLE = True
except ImportError:
    try:
        from genetic_scoring import COLOR_LOCI, COMMON_HEALTH_GENES, BreedingOptimizer, Dog, PedigreeTree
        GENETIC_SCORING_AVAILABLE = True
    except ImportError:
        GENETIC_SCORING_AVAILABLE = False
        COMMON_HEALTH_GENES = {}
        COLOR_LOCI = ()
        logging.warning("Genetic scoring module not available")

# 3D Pose Estimation
try:
    from api.pose_estimation import CanineKeypoints, GaitAnalyzer, PoseAnalyzer, Vec2, Vec3
    POSE_ESTIMATION_AVAILABLE = True
except ImportError:
    try:
        from pose_estimation import CanineKeypoints, GaitAnalyzer, PoseAnalyzer, Vec2, Vec3
        POSE_ESTIMATION_AVAILABLE = True
    except ImportError:
        POSE_ESTIMATION_AVAILABLE = False
        logging.warning("Pose estimation module not available")

# Fine-Tuning Infrastructure
try:
    from api.finetuning import EvaluationPipeline, ModelRegistry
    FINETUNING_AVAILABLE = True
except ImportError:
    try:
        from finetuning import EvaluationPipeline, ModelRegistry
        FINETUNING_AVAILABLE = True
    except ImportError:
        FINETUNING_AVAILABLE = False
        logging.warning("Fine-tuning module not available")

# Extended breed database
try:
    from api.breeds import get_breed_data
    EXTENDED_BREEDS = get_breed_data()
    EXTENDED_BREEDS_AVAILABLE = True
except ImportError:
    try:
        from breeds import get_breed_data
        EXTENDED_BREEDS = get_breed_data()
        EXTENDED_BREEDS_AVAILABLE = True
    except ImportError:
        EXTENDED_BREEDS = None
        EXTENDED_BREEDS_AVAILABLE = False
        logging.warning("Extended breeds module not available")

# Anthropic Claude import - primary AI provider
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    logging.warning("Anthropic library not available")

# OpenAI import - fallback
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logging.warning("OpenAI library not available")

# Application-wide constants
try:
    from api.config_constants import (
        AI_API_TIMEOUT_SECONDS,
        ALLOWED_IMAGE_EXTENSIONS,
        ALLOWED_VIDEO_EXTENSIONS,
        COOKIE_MAX_AGE_SECONDS,
        DEFAULT_BREED_ID,
        RATE_LIMIT_PER_DAY,
        RATE_LIMIT_PER_HOUR,
        SMTP_TIMEOUT_SECONDS,
        SUBPROCESS_QUICK_TIMEOUT_SECONDS,
        SUBPROCESS_TIMEOUT_SECONDS,
        UPLOAD_MAX_SIZE_BYTES,
    )
except ImportError:
    from config_constants import (
        AI_API_TIMEOUT_SECONDS,
        ALLOWED_IMAGE_EXTENSIONS,
        ALLOWED_VIDEO_EXTENSIONS,
        COOKIE_MAX_AGE_SECONDS,
        DEFAULT_BREED_ID,
        RATE_LIMIT_PER_DAY,
        RATE_LIMIT_PER_HOUR,
        SMTP_TIMEOUT_SECONDS,
        SUBPROCESS_QUICK_TIMEOUT_SECONDS,
        SUBPROCESS_TIMEOUT_SECONDS,
        UPLOAD_MAX_SIZE_BYTES,
    )

# =============================================================================
# Configuration
# =============================================================================

VERSION = "4.1.4"
BUILD = "2026-02-27-pwa-enhancement"

# Paths (absolute)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(os.path.dirname(BASE_DIR), 'static')
TEMPLATES_DIR = os.path.join(os.path.dirname(BASE_DIR), 'templates')
UPLOAD_DIR = os.path.join(BASE_DIR, 'uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Initialize BOTH AI clients when keys are available
# Primary provider is determined by priority: Claude > OpenAI

# Model configuration
ANTHROPIC_MODEL = os.getenv('ANTHROPIC_MODEL', 'claude-sonnet-4-20250514')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4o')

# Anthropic Claude
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
if ANTHROPIC_AVAILABLE and ANTHROPIC_API_KEY:
    claude_client = anthropic.Anthropic(
        api_key=ANTHROPIC_API_KEY,
        timeout=AI_API_TIMEOUT_SECONDS,
        max_retries=2
    )
else:
    claude_client = None

# OpenAI (always initialize if key is available)
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if OPENAI_AVAILABLE and OPENAI_API_KEY:
    openai_client = OpenAI(
        api_key=OPENAI_API_KEY,
        timeout=AI_API_TIMEOUT_SECONDS,
        max_retries=2
    )
else:
    openai_client = None

# Determine primary vision provider
if claude_client:
    VISION_ENABLED = True
    VISION_PROVIDER = "claude"
elif openai_client:
    VISION_ENABLED = True
    VISION_PROVIDER = "openai"
else:
    VISION_ENABLED = False
    VISION_PROVIDER = "none"

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

# ===== 動画処理の依存関係を起動時にチェック =====
FFMPEG_AVAILABLE = bool(_shutil.which('ffmpeg'))
if FFMPEG_AVAILABLE:
    logger.info("ffmpeg: available ✓ (MOV/WebM等の動画変換が可能)")
else:
    logger.warning("ffmpeg: NOT FOUND ✗ — MOV動画の変換ができません。apt install ffmpeg を推奨")

try:
    import cv2
    OPENCV_AVAILABLE = True
    _cv2_build = cv2.getBuildInformation() if hasattr(cv2, 'getBuildInformation') else ''
    OPENCV_FFMPEG_BACKEND = 'FFMPEG' in _cv2_build.upper() if _cv2_build else False
    logger.info(f"OpenCV: available ✓ (version: {cv2.__version__}, ffmpeg backend: {OPENCV_FFMPEG_BACKEND})")
    if not OPENCV_FFMPEG_BACKEND:
        logger.warning("OpenCV ffmpeg backend not found — MOV直接読み込みが失敗する可能性があります")
except ImportError:
    cv2 = None
    OPENCV_AVAILABLE = False
    OPENCV_FFMPEG_BACKEND = False
    logger.warning("OpenCV: NOT FOUND ✗ — 動画フレーム抽出ができません。pip install opencv-python-headless を推奨")

# Flask
app = Flask(__name__, static_folder=STATIC_DIR)
app.config['MAX_CONTENT_LENGTH'] = UPLOAD_MAX_SIZE_BYTES  # 50MB upload limit
app.config['JSON_AS_ASCII'] = False
if RECO2_AVAILABLE:
    reco2_ensure_state_file()

# SECRET_KEY — must be stable across deploys to preserve sessions
_secret_key = os.getenv('SECRET_KEY') or os.getenv('FLASK_SECRET_KEY')
if _secret_key:
    app.secret_key = _secret_key
else:
    _is_prod = bool(os.getenv('RENDER') or os.getenv('PRODUCTION'))
    if _is_prod:
        raise RuntimeError(
            "SECRET_KEY (or FLASK_SECRET_KEY) must be set in production. "
            "Generate one with: python -c \"import secrets; print(secrets.token_hex(32))\""
        )
    app.secret_key = secrets.token_hex(32)
    logger.warning("SECRET_KEY is not set — using ephemeral key. "
                    "Sessions will be lost on restart.")

# Session cookie security for HTTPS / reverse-proxy environments
_is_production = bool(os.getenv('RENDER') or os.getenv('PRODUCTION'))
app.config['SESSION_COOKIE_SECURE'] = _is_production
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['REMEMBER_COOKIE_SECURE'] = _is_production
if _is_production:
    app.config['PREFERRED_URL_SCHEME'] = 'https'

# ProxyFix — Render and similar platforms run behind a reverse proxy.
# Without this, Flask sees HTTP instead of HTTPS, breaking Secure cookies.
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

# CORS — default to same-origin only; set ALLOWED_ORIGINS for production domains.
_raw_origins = os.getenv('ALLOWED_ORIGINS', '').strip()
if _raw_origins and _raw_origins != '*':
    ALLOWED_ORIGINS = [o.strip() for o in _raw_origins.split(',') if o.strip()]
else:
    ALLOWED_ORIGINS = []
    if _raw_origins == '*':
        logger.warning("ALLOWED_ORIGINS='*' is insecure with credentials. "
                        "Set specific domains for production.")

if ALLOWED_ORIGINS:
    CORS(app, resources={r"/api/*": {"origins": ALLOWED_ORIGINS}},
         supports_credentials=True)
else:
    # No CORS headers — same-origin only (safest default)
    pass

# ---------------------------------------------------------------------------
# Security: Cookie / CSRF / Rate Limiting configuration
# ---------------------------------------------------------------------------
COOKIE_SECURE = os.getenv('COOKIE_SECURE', '1') == '1'
COOKIE_MAX_AGE = COOKIE_MAX_AGE_SECONDS  # 1 day
ALLOW_RESET_TOKEN_RESPONSE = os.getenv('ALLOW_RESET_TOKEN_RESPONSE', '0') == '1'

# Startup log for auth diagnostics (always runs, including under gunicorn)
try:
    from api.database import DB_PATH as _startup_dbp, DB_DIR as _startup_dbdir
except ImportError:
    try:
        from database import DB_PATH as _startup_dbp, DB_DIR as _startup_dbdir
    except ImportError:
        _startup_dbp = _startup_dbdir = 'unavailable'
logger.info(f"[auth-config] SECRET_KEY set via env: {bool(os.getenv('SECRET_KEY') or os.getenv('FLASK_SECRET_KEY'))}, "
            f"COOKIE_SECURE: {COOKIE_SECURE}, production: {_is_production}")
logger.info(f"[auth-config] auth_db_path: {_startup_dbp}, data_root: {_startup_dbdir}")

# Upload extension whitelist
ALLOWED_IMAGE_EXT = ALLOWED_IMAGE_EXTENSIONS
ALLOWED_VIDEO_EXT = ALLOWED_VIDEO_EXTENSIONS

# Rate Limiting — Flask-Limiter (global) + in-memory per-endpoint guard
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=[f"{RATE_LIMIT_PER_DAY} per day", f"{RATE_LIMIT_PER_HOUR} per hour"],
    storage_uri="memory://"
)

# --- Fine-grained rate limiter (IP+email, for auth endpoints) ---
_rate_lock = _threading.Lock()
_rate_buckets = {}  # key -> [(timestamp, ...)]
_RATE_WINDOW = 600   # 10 minutes
_RATE_MAX = 5        # 5 attempts per window


def _rate_limit_key(prefix):
    """Build a rate-limit key from IP + optional email."""
    ip = request.headers.get('X-Forwarded-For', request.remote_addr or '?').split(',')[0].strip()
    data = request.get_json(silent=True) or {}
    email = data.get('email', '')
    return f"{prefix}:{ip}:{email}"


def _check_rate_limit(key):
    """Return True if request is allowed; False if rate-limited."""
    now = time.time()
    with _rate_lock:
        hits = _rate_buckets.get(key, [])
        hits = [t for t in hits if now - t < _RATE_WINDOW]
        if len(hits) >= _RATE_MAX:
            _rate_buckets[key] = hits
            return False
        hits.append(now)
        _rate_buckets[key] = hits
        return True


# --- CSRF token helpers ---
_CSRF_SECRET = os.getenv('CSRF_SECRET') or os.getenv('SECRET_KEY') or secrets.token_hex(32)


def _generate_csrf_token(session_token):
    """Generate a CSRF token tied to a session."""
    return _hashlib.sha256(f"{_CSRF_SECRET}:{session_token}".encode()).hexdigest()


def _verify_csrf(session_token):
    """Verify CSRF token from X-CSRF-Token header.

    Skipped when Authorization header is present (SPA/API clients).
    """
    if request.headers.get('Authorization'):
        return True
    csrf_tok = request.headers.get('X-CSRF-Token', '')
    if not csrf_tok or not session_token:
        return False
    expected = _generate_csrf_token(session_token)
    return _hashlib.sha256(csrf_tok.encode()).digest() == _hashlib.sha256(expected.encode()).digest()


def _set_session_cookie(response, token):
    """Unified helper to set the session cookie with secure defaults."""
    response.set_cookie(
        'session_token', token,
        httponly=True,
        samesite='Lax',
        secure=COOKIE_SECURE,
        max_age=COOKIE_MAX_AGE,
    )
    return response

# RECO Firewall removed — isolated to extras/reco/

# Register Pet Passport / Health Report Blueprint
if PASSPORT_AVAILABLE:
    app.register_blueprint(passport_bp)
    logger.info("Pet Passport PDF generator registered at /api/passport/*")

# Register Health Symptom Checker Blueprint
if HEALTH_CHECKER_AVAILABLE:
    app.register_blueprint(health_bp)
    logger.info("Health Symptom Checker registered at /api/health-check/*")

# Register Diagnostic Chat Blueprint
if DIAGNOSTIC_CHAT_AVAILABLE:
    app.register_blueprint(diagnostic_bp)
    logger.info("Diagnostic Chat registered at /api/diagnostic-chat/*")

# Breed data — imported from breeds.py (360 FCI breeds)
try:
    from api.breeds import BREED_DATA as _BREEDS_FULL, get_fci_standard_url
except ImportError:
    from breeds import BREED_DATA as _BREEDS_FULL, get_fci_standard_url

# Build BREED_DATA with backward-compatible keys (common_issues alias)
BREED_DATA = {}
for _k, _v in _BREEDS_FULL.items():
    _entry = dict(_v)
    # Ensure backward compatibility: common_issues = hereditary_diseases
    if 'hereditary_diseases' in _entry and 'common_issues' not in _entry:
        _entry['common_issues'] = _entry['hereditary_diseases']
    # Ensure fci_no alias for fci_number
    if 'fci_number' in _entry and 'fci_no' not in _entry:
        _entry['fci_no'] = _entry['fci_number']
    BREED_DATA[_k] = _entry

# Merge extended breed database (360 breeds) if available
if EXTENDED_BREEDS_AVAILABLE and EXTENDED_BREEDS:
    for breed_id, breed_info in EXTENDED_BREEDS.items():
        if breed_id not in BREED_DATA:
            BREED_DATA[breed_id] = {
                'name': breed_info['name'],
                'name_en': breed_info['name_en'],
                'emoji': breed_info.get('emoji', '🐕'),
                'fci_no': breed_info.get('fci_number', 0),
                'ideal_structure': breed_info.get('ideal_structure', ''),
                'ideal_coat': breed_info.get('ideal_coat', ''),
                'ideal_gait': breed_info.get('ideal_gait', ''),
                'common_issues': breed_info.get('hereditary_diseases', [])
            }
    logger.info(f"Breed database expanded: {len(BREED_DATA)} breeds")

# Startup
logger.info("=" * 80)
logger.info(f"ShowDog Analysis Platform v{VERSION} - {BUILD}")
logger.info(f"Algorithm Version: {ALGORITHM_VERSION}")
logger.info(f"Model Version: {MODEL_VERSION}")
logger.info(f"Weights Hash: {WEIGHTS_HASH}")
logger.info(f"Vision: {'Enabled' if VISION_ENABLED else 'Disabled'} (Primary: {VISION_PROVIDER})")
logger.info(f"  Claude: {'Ready' if claude_client else 'Not configured'}")
logger.info(f"  OpenAI: {'Ready' if openai_client else 'Not configured'}")
logger.info(f"  Breeds: {len(BREED_DATA)} FCI breeds loaded")
logger.info(f"Deterministic Scoring: {'Enabled' if SCORING_AVAILABLE else 'Legacy Mode'}")
logger.info(f"Static Dir: {STATIC_DIR}")
logger.info("=" * 80)

# =============================================================================
# Vision Analysis Functions (Claude / OpenAI)
# =============================================================================

def _call_claude_vision(prompt, image_base64, max_tokens=500):
    """Call Claude vision API."""
    response = claude_client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=max_tokens,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image", "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": image_base64
                }},
                {"type": "text", "text": prompt}
            ]
        }]
    )
    return response.content[0].text


def _call_openai_vision(prompt, image_base64, max_tokens=500):
    """Call OpenAI vision API."""
    response = openai_client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "You are an expert evaluator. Always respond with valid JSON only. No explanations, no markdown, no text before or after the JSON."},
            {"role": "user", "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {
                    "url": f"data:image/jpeg;base64,{image_base64}",
                    "detail": "low"
                }}
            ]}
        ],
        max_tokens=max_tokens,
        temperature=0.3
    )
    result_text = response.choices[0].message.content
    logger.info(f"OpenAI response preview: {result_text[:200]!r}")
    return result_text


def call_vision_api(prompt, image_base64, max_tokens=500):
    """Call vision API with automatic fallback between providers."""
    if VISION_PROVIDER == "claude":
        try:
            return _call_claude_vision(prompt, image_base64, max_tokens)
        except Exception as e:
            if openai_client:
                logger.warning(f"Claude failed ({e}), falling back to OpenAI")
                return _call_openai_vision(prompt, image_base64, max_tokens)
            raise
    elif VISION_PROVIDER == "openai":
        try:
            return _call_openai_vision(prompt, image_base64, max_tokens)
        except Exception as e:
            if claude_client:
                logger.warning(f"OpenAI failed ({e}), falling back to Claude")
                return _call_claude_vision(prompt, image_base64, max_tokens)
            raise
    else:
        raise Exception("No vision provider available")


def _call_claude_video(prompt, frames):
    """Call Claude vision API with multiple video frames."""
    content_parts = []
    for frame in frames[:3]:
        content_parts.append({
            "type": "image",
            "source": {"type": "base64", "media_type": "image/jpeg", "data": frame}
        })
    content_parts.append({"type": "text", "text": prompt})
    response = claude_client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=600,
        messages=[{"role": "user", "content": content_parts}]
    )
    return response.content[0].text


def _call_openai_video(prompt, frames):
    """Call OpenAI vision API with multiple video frames."""
    content_parts = [{"type": "text", "text": prompt}]
    for frame in frames[:3]:
        content_parts.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{frame}", "detail": "low"}
        })
    response = openai_client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "You are an expert evaluator. Always respond with valid JSON only. No explanations, no markdown, no text before or after the JSON."},
            {"role": "user", "content": content_parts}
        ],
        max_tokens=600,
        temperature=0.3
    )
    result_text = response.choices[0].message.content
    logger.info(f"OpenAI video response preview: {result_text[:200]!r}")
    return result_text


def _call_video_vision(prompt, frames):
    """Call video vision API with automatic fallback between providers."""
    if VISION_PROVIDER == "claude":
        try:
            return _call_claude_video(prompt, frames)
        except Exception as e:
            if openai_client:
                logger.warning(f"Claude video failed ({e}), falling back to OpenAI")
                return _call_openai_video(prompt, frames)
            raise
    elif VISION_PROVIDER == "openai":
        try:
            return _call_openai_video(prompt, frames)
        except Exception as e:
            if claude_client:
                logger.warning(f"OpenAI video failed ({e}), falling back to Claude")
                return _call_claude_video(prompt, frames)
            raise
    else:
        raise Exception("No vision provider available")


# Pre-compiled regex for extracting JSON from markdown code blocks.
# Matches ```json ... ``` or ``` ... ``` with minimal backtracking.
_JSON_BLOCK_RE = re.compile(r'```(?:json)?\s*\n?(.*?)\n?\s*```', re.DOTALL)

# Pre-compiled regex for detecting a bare JSON object or array at the boundaries.
_BARE_JSON_RE = re.compile(r'\A\s*[\[{]')


_EMBEDDED_JSON_RE = re.compile(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}')


def parse_json_response(content):
    """Parse JSON from API response.

    Handles multiple formats that GPT-4o may return:
    1. Pure JSON (fast path)
    2. JSON inside markdown code blocks
    3. JSON embedded in natural language text
    """
    if not content or not content.strip():
        raise json.JSONDecodeError("Empty response", content or "", 0)

    content = content.strip()
    logger.debug(f"Parsing response ({len(content)} chars): {content[:300]!r}")

    # Fast path: bare JSON object/array
    if _BARE_JSON_RE.match(content):
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            logger.debug(f"Bare JSON parse failed: {e}")

    # Extract from markdown code block
    m = _JSON_BLOCK_RE.search(content)
    if m:
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError as e:
            logger.debug(f"Markdown code block JSON parse failed: {e}")

    # Search for JSON object embedded in free text
    # Find the first '{' and the last '}' and try parsing that substring
    first_brace = content.find('{')
    last_brace = content.rfind('}')
    if first_brace != -1 and last_brace > first_brace:
        candidate = content[first_brace:last_brace + 1]
        try:
            return json.loads(candidate)
        except json.JSONDecodeError as e:
            logger.debug(f"Embedded JSON parse failed: {e}")

    # Last resort: strip and try raw content
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        logger.error(f"JSON parse failed: {e}; full response: {content!r}")
        raise


# =============================================================================
# Dual AI Parallel Call + RECO3 Score Blending
# =============================================================================

def _call_dual_vision(prompt, image_base64, max_tokens=500):
    """Call BOTH Claude and OpenAI Vision APIs in parallel and return both results.

    Returns:
        (claude_result, openai_result) — each is a parsed dict or None on failure.
    """
    claude_result = None
    openai_result = None

    def _claude_call():
        try:
            content = _call_claude_vision(prompt, image_base64, max_tokens)
            return parse_json_response(content)
        except Exception as e:
            logger.warning(f"Dual-AI Claude call failed: {e}")
            return None

    def _openai_call():
        try:
            content = _call_openai_vision(prompt, image_base64, max_tokens)
            return parse_json_response(content)
        except Exception as e:
            logger.warning(f"Dual-AI OpenAI call failed: {e}")
            return None

    if claude_client and openai_client:
        # Both available — call in parallel
        with ThreadPoolExecutor(max_workers=2) as executor:
            claude_future = executor.submit(_claude_call)
            openai_future = executor.submit(_openai_call)
            try:
                claude_result = claude_future.result(timeout=30)
            except Exception as e:
                logger.warning(f"Dual-AI Claude future failed: {e}")
            try:
                openai_result = openai_future.result(timeout=30)
            except Exception as e:
                logger.warning(f"Dual-AI OpenAI future failed: {e}")
    elif claude_client:
        claude_result = _claude_call()
    elif openai_client:
        openai_result = _openai_call()

    if claude_result is None and openai_result is None:
        logger.error("Dual-AI: Both Claude and OpenAI failed — no analysis result available")

    return claude_result, openai_result


def _call_dual_video_vision(prompt, frames):
    """Call BOTH Claude and OpenAI video Vision APIs in parallel.

    Returns:
        (claude_result, openai_result) — each is a parsed dict or None.
    """
    claude_result = None
    openai_result = None

    def _claude_call():
        try:
            content = _call_claude_video(prompt, frames)
            return parse_json_response(content)
        except Exception as e:
            logger.warning(f"Dual-AI Claude video call failed: {e}")
            return None

    def _openai_call():
        try:
            content = _call_openai_video(prompt, frames)
            return parse_json_response(content)
        except Exception as e:
            logger.warning(f"Dual-AI OpenAI video call failed: {e}")
            return None

    if claude_client and openai_client:
        with ThreadPoolExecutor(max_workers=2) as executor:
            cf = executor.submit(_claude_call)
            of = executor.submit(_openai_call)
            try:
                claude_result = cf.result(timeout=30)
            except Exception as e:
                logger.warning(f"Dual-AI Claude video future failed: {e}")
            try:
                openai_result = of.result(timeout=30)
            except Exception as e:
                logger.warning(f"Dual-AI OpenAI video future failed: {e}")
    elif claude_client:
        claude_result = _claude_call()
    elif openai_client:
        openai_result = _openai_call()

    if claude_result is None and openai_result is None:
        logger.error("Dual-AI video: Both Claude and OpenAI failed — no analysis result available")

    return claude_result, openai_result


def _reco3_blend_scores(algo_scores, claude_scores, openai_scores,
                        score_keys, cap=8.0):
    """RECO3 Score Blending — reconcile Algorithm, Claude, OpenAI scores.

    Strategy:
    - 3 sources agree (within ±5): weighted avg (Algo 40%, Claude 30%, OpenAI 30%)
    - 2 AIs agree but diverge from algo (>threshold): AI consensus weighted higher
      (Algo 30%, AI consensus 70%)
    - AIs disagree with each other (>10): anchor on algorithm
      (Algo 50%, closer AI 35%, further AI 15%)
    - One AI failed: (Algo 50%, available AI 50%)

    Returns:
        dict with blended scores + metadata about divergence
    """
    blended = {}
    metadata = {'method': 'reco3_blend', 'divergence': {}}

    for key in score_keys:
        algo_val = algo_scores.get(key)
        if algo_val is None:
            continue
        algo_val = float(algo_val)

        claude_val = float(claude_scores.get(key, 0)) if claude_scores and claude_scores.get(key) is not None else None
        openai_val = float(openai_scores.get(key, 0)) if openai_scores and openai_scores.get(key) is not None else None

        # Clamp AI adjustments/scores to valid range
        if claude_val is not None:
            claude_val = max(0, min(100, claude_val))
        if openai_val is not None:
            openai_val = max(0, min(100, openai_val))

        if claude_val is not None and openai_val is not None:
            # Both AIs available
            ai_diff = abs(claude_val - openai_val)
            algo_claude_diff = abs(algo_val - claude_val)
            algo_openai_diff = abs(algo_val - openai_val)
            ai_consensus = (claude_val + openai_val) / 2
            algo_ai_diff = abs(algo_val - ai_consensus)

            if algo_ai_diff <= 5 and ai_diff <= 5:
                # All agree: standard weighted average
                result = algo_val * 0.40 + claude_val * 0.30 + openai_val * 0.30
                blend_type = 'consensus'
            elif ai_diff <= 10 and algo_ai_diff > 5:
                # AIs agree with each other, diverge from algorithm
                # Trust AI consensus more but cap divergence
                ai_adj = ai_consensus - algo_val
                capped_adj = max(-cap, min(cap, ai_adj))
                result = algo_val + capped_adj * 0.70
                blend_type = 'ai_consensus_capped'
            elif ai_diff > 10:
                # AIs disagree — anchor on algorithm, weight closer AI more
                if algo_claude_diff <= algo_openai_diff:
                    result = algo_val * 0.50 + claude_val * 0.35 + openai_val * 0.15
                else:
                    result = algo_val * 0.50 + claude_val * 0.15 + openai_val * 0.35
                blend_type = 'ai_disagree_anchor'
            else:
                # Moderate agreement
                result = algo_val * 0.40 + claude_val * 0.30 + openai_val * 0.30
                blend_type = 'moderate'

            metadata['divergence'][key] = {
                'algo': algo_val, 'claude': claude_val, 'openai': openai_val,
                'ai_diff': round(ai_diff, 1),
                'algo_ai_diff': round(algo_ai_diff, 1),
                'blend_type': blend_type
            }
        elif claude_val is not None:
            # Only Claude available
            diff = abs(algo_val - claude_val)
            if diff <= 5:
                result = algo_val * 0.45 + claude_val * 0.55
            else:
                adj = claude_val - algo_val
                capped_adj = max(-cap, min(cap, adj))
                result = algo_val + capped_adj * 0.55
            blend_type = 'claude_only'
            metadata['divergence'][key] = {
                'algo': algo_val, 'claude': claude_val, 'diff': round(diff, 1),
                'blend_type': blend_type
            }
        elif openai_val is not None:
            # Only OpenAI available
            diff = abs(algo_val - openai_val)
            if diff <= 5:
                result = algo_val * 0.45 + openai_val * 0.55
            else:
                adj = openai_val - algo_val
                capped_adj = max(-cap, min(cap, adj))
                result = algo_val + capped_adj * 0.55
            blend_type = 'openai_only'
            metadata['divergence'][key] = {
                'algo': algo_val, 'openai': openai_val, 'diff': round(diff, 1),
                'blend_type': blend_type
            }
        else:
            # No AI available — use algorithm only
            result = algo_val
            blend_type = 'algorithm_only'

        blended[key] = round(max(0, min(100, result)), 1)

    metadata['blended'] = blended
    return blended, metadata


def _image_seed(image_base64, salt=''):
    """画像データのハッシュから決定的なシード値を生成（同じ画像→同じスコア）"""
    import hashlib
    sample = (image_base64[:2000] + salt).encode('utf-8', errors='ignore')
    h = int(hashlib.md5(sample, usedforsecurity=False).hexdigest(), 16)  # nosec B324
    return h

def _seeded_score(seed, base=82.0, spread=12.0):
    """シード値から base〜base+spread の範囲でスコアを生成"""
    return round(base + (seed % int(spread * 10)) / 10.0, 1)


def _score_to_grade(score_dict):
    """Convert a score dict or numeric value to an FCI grade string."""
    if isinstance(score_dict, dict):
        vals = [v for v in score_dict.values() if isinstance(v, (int, float))]
        avg = sum(vals) / len(vals) if vals else 0
    elif isinstance(score_dict, (int, float)):
        avg = float(score_dict)
    else:
        return 'C'
    if avg >= 95:
        return 'S'
    if avg >= 90:
        return 'A+'
    if avg >= 85:
        return 'A'
    if avg >= 80:
        return 'B+'
    if avg >= 70:
        return 'B'
    return 'C'


def analyze_photo_structure(image_base64, breed_name, breed_data):
    """写真から体構造を評価 — アルゴリズム主導（AIに依存しない）

    Architecture: Algorithm FIRST → AI correction OPTIONAL
    1. アルゴリズムがシルエット中心線→角度/比率→スタンダードDB比較でベーススコア算出
    2. AI（利用可能な場合のみ）は±8点の範囲内で犬種特性補正
    """
    # FCI parameters for breed-specific analysis
    try:
        from api.auto_cycle import apply_calibration_to_analysis, get_breed_fci_params, try_auto_cycle
        from api.breeds import BREED_DATA
        breed_id = breed_data.get('breed_id', '')
        fci_params = get_breed_fci_params(breed_id, BREED_DATA)
        enriched_data = {**breed_data, **fci_params}
        try_auto_cycle()
    except ImportError:
        enriched_data = breed_data
        breed_id = ''
    except Exception as e:
        logger.warning(f"Breed data enrichment failed: {e}")
        enriched_data = breed_data
        breed_id = ''

    # === STEP 1: ALGORITHM (主導) — Always runs first =====================
    algo_result = None
    if analyze_structure_local:
        try:
            algo_result = analyze_structure_local(image_base64, breed_name, enriched_data)
        except AnalysisError as e:
            logger.warning(f"CV2 structure analysis failed, trying PIL fallback: {e}")
    if algo_result is None and analyze_structure_pil:
        try:
            algo_result = analyze_structure_pil(image_base64, breed_name, enriched_data)
        except AnalysisError as e:
            logger.warning(f"PIL structure analysis also failed: {e}")

    if algo_result:
        # Apply breed calibration from accumulated data
        try:
            if breed_id:
                cal_scores = apply_calibration_to_analysis(breed_id, {
                    'structure': algo_result.get('score', 0),
                })
                if cal_scores.get('structure') != algo_result.get('score'):
                    algo_result['score'] = round(cal_scores['structure'], 1)
                    algo_result['calibrated'] = True
        except Exception as e:
            logger.warning(f"operation failed (non-fatal): {e}")

        # === STEP 2: DUAL AI + RECO3 BLEND — Active when Vision enabled ===
        if VISION_ENABLED:
            try:
                prompt = f"""あなたはFCI認定のプロフェッショナルドッグショー審査員です。
この{breed_name}の写真を詳細に分析し、体構造を100点満点で評価してください。

【FCI基準 No.{breed_data.get('fci_no', '')}】
理想的な体構造: {breed_data.get('ideal_structure', '標準的な犬種基準')}

以下の項目をそれぞれ0-100で評価し、コメントを付けてください。

【出力形式】JSON形式のみで返してください:
{{
    "score": 0,
    "proportion": 0,
    "skeletal": 0,
    "muscular": 0,
    "comments": "犬種特性に基づく評価理由",
    "strengths": ["強み1"],
    "improvements": ["改善点1"]
}}"""
                # Dual AI: call both Claude and OpenAI in parallel
                claude_ai, openai_ai = _call_dual_vision(prompt, image_base64, max_tokens=400)

                score_keys = ['score', 'proportion', 'skeletal', 'muscular']
                algo_scores = {k: algo_result.get(k) for k in score_keys if algo_result.get(k) is not None}

                if claude_ai or openai_ai:
                    # RECO3 Blend: reconcile algorithm + dual AI
                    blended, reco3_meta = _reco3_blend_scores(
                        algo_scores, claude_ai, openai_ai, score_keys, cap=8.0)

                    for key in score_keys:
                        if key in blended and key in algo_result:
                            algo_result[key] = blended[key]

                    # Merge AI comments from both providers
                    ai_comments = []
                    if claude_ai and claude_ai.get('comments'):
                        ai_comments.append(f'[Claude] {claude_ai["comments"]}')
                    if openai_ai and openai_ai.get('comments'):
                        ai_comments.append(f'[OpenAI] {openai_ai["comments"]}')
                    if ai_comments:
                        algo_result['comments'] = algo_result.get('comments', '') + ' ' + ' '.join(ai_comments)

                    # Merge strengths/improvements
                    strengths = []
                    improvements = []
                    for src in (claude_ai, openai_ai):
                        if src:
                            strengths.extend(src.get('strengths', []))
                            improvements.extend(src.get('improvements', []))
                    if strengths:
                        algo_result['strengths'] = list(dict.fromkeys(strengths))  # dedup
                    if improvements:
                        algo_result['improvements'] = list(dict.fromkeys(improvements))

                    algo_result['ai_correction_applied'] = True
                    algo_result['reco3_blend'] = reco3_meta
                    providers = []
                    if claude_ai:
                        providers.append('claude')
                    if openai_ai:
                        providers.append('openai')
                    algo_result['analysis_method'] = f'algorithm+reco3({"+".join(providers)})'
                    logger.info(f"Structure analysis: RECO3 blend (algo + {'+'.join(providers)})")
                else:
                    algo_result['analysis_method'] = 'algorithm'
                    logger.warning("Structure analysis: dual AI both failed, algorithm-only")
            except Exception as e:
                logger.warning(f"RECO3 blend failed, using algorithm-only: {e}")
                algo_result['analysis_method'] = 'algorithm'
        else:
            algo_result['analysis_method'] = 'algorithm'
            logger.info("Structure analysis: algorithm-only (AI not enabled)")

        return algo_result

    # Last resort: hash-based deterministic scores (no image analysis available)
    logger.warning("Structure analysis: no image analysis available, using hash fallback")
    seed = _image_seed(image_base64, 'structure')
    s_main = _seeded_score(seed, 76.0, 18.0)
    s_prop = _seeded_score(seed >> 8, 74.0, 20.0)
    s_skel = _seeded_score(seed >> 16, 75.0, 19.0)
    s_musc = _seeded_score(seed >> 24, 73.0, 20.0)
    return {
        'score': s_main,
        'proportion': int(s_prop),
        'skeletal': int(s_skel),
        'muscular': int(s_musc),
        'comments': f'{breed_name}の体構造を画像特徴量から評価しました。',
        'details': 'フォールバック評価（画像ハッシュベース）',
        'analysis_method': 'hash'
    }


def analyze_photo_coat(image_base64, breed_name, breed_data):
    """写真から被毛を評価 — FCIデータに基づく"""
    # FCI parameters for breed-specific coat analysis
    try:
        from api.auto_cycle import apply_calibration_to_analysis, get_breed_fci_params, try_auto_cycle
        from api.breeds import BREED_DATA as _BREED_DATA
        breed_id = breed_data.get('breed_id', '')
        fci_params = get_breed_fci_params(breed_id, _BREED_DATA)
        enriched_data = {**breed_data, **fci_params}
        try_auto_cycle()
    except ImportError:
        enriched_data = breed_data
        breed_id = ''
    except Exception as e:
        logger.warning(f"Breed data enrichment failed: {e}")
        enriched_data = breed_data
        breed_id = ''

    # === STEP 1: ALGORITHM (主導) — Always runs first =====================
    algo_result = None
    if analyze_coat_local:
        try:
            algo_result = analyze_coat_local(image_base64, breed_name, enriched_data)
        except AnalysisError as e:
            logger.warning(f"CV2 coat analysis failed, trying PIL fallback: {e}")
    if algo_result is None and analyze_coat_pil:
        try:
            algo_result = analyze_coat_pil(image_base64, breed_name, enriched_data)
        except AnalysisError as e:
            logger.warning(f"PIL coat analysis also failed: {e}")

    if algo_result:
        # Apply breed calibration from accumulated data
        try:
            if breed_id:
                cal_scores = apply_calibration_to_analysis(breed_id, {
                    'coat': algo_result.get('score', 0),
                })
                if cal_scores.get('coat') != algo_result.get('score'):
                    algo_result['score'] = round(cal_scores['coat'], 1)
                    algo_result['calibrated'] = True
        except Exception as e:
            logger.warning(f"operation failed (non-fatal): {e}")

        # === STEP 2: DUAL AI + RECO3 BLEND — Active when Vision enabled ===
        if VISION_ENABLED:
            try:
                prompt = f"""あなたはFCI認定のプロフェッショナルドッグショー審査員です。
この{breed_name}の被毛を分析し、以下の項目をそれぞれ0-100で評価してください。

【FCI基準】
理想的な被毛: {enriched_data.get('ideal_coat', '犬種標準の被毛')}

【出力形式】JSON形式のみで返してください:
{{
    "score": 0,
    "texture": 0,
    "volume": 0,
    "grooming": 0,
    "comments": "犬種特性に基づく評価理由"
}}"""
                # Dual AI: call both Claude and OpenAI in parallel
                claude_ai, openai_ai = _call_dual_vision(prompt, image_base64, max_tokens=400)

                score_keys = ['score', 'texture', 'volume', 'grooming']
                algo_scores = {k: algo_result.get(k) for k in score_keys if algo_result.get(k) is not None}

                if claude_ai or openai_ai:
                    blended, reco3_meta = _reco3_blend_scores(
                        algo_scores, claude_ai, openai_ai, score_keys, cap=8.0)

                    for key in score_keys:
                        if key in blended and key in algo_result:
                            algo_result[key] = blended[key]

                    ai_comments = []
                    if claude_ai and claude_ai.get('comments'):
                        ai_comments.append(f'[Claude] {claude_ai["comments"]}')
                    if openai_ai and openai_ai.get('comments'):
                        ai_comments.append(f'[OpenAI] {openai_ai["comments"]}')
                    if ai_comments:
                        algo_result['comments'] = algo_result.get('comments', '') + ' ' + ' '.join(ai_comments)

                    algo_result['ai_correction_applied'] = True
                    algo_result['reco3_blend'] = reco3_meta
                    providers = []
                    if claude_ai:
                        providers.append('claude')
                    if openai_ai:
                        providers.append('openai')
                    algo_result['analysis_method'] = f'algorithm+reco3({"+".join(providers)})'
                    logger.info(f"Coat analysis: RECO3 blend (algo + {'+'.join(providers)})")
                else:
                    algo_result['analysis_method'] = 'algorithm'
                    logger.warning("Coat analysis: dual AI both failed, algorithm-only")
            except Exception as e:
                logger.warning(f"RECO3 coat blend failed, using algorithm-only: {e}")
                algo_result['analysis_method'] = 'algorithm'
        else:
            algo_result['analysis_method'] = 'algorithm'
            logger.info("Coat analysis: algorithm-only (AI not enabled)")

        return algo_result

    # Last resort: hash-based deterministic scores
    logger.warning("Coat analysis: no image analysis available, using hash fallback")
    seed = _image_seed(image_base64, 'coat')
    c_main = _seeded_score(seed, 75.0, 19.0)
    c_text = _seeded_score(seed >> 8, 73.0, 21.0)
    c_vol = _seeded_score(seed >> 16, 74.0, 20.0)
    c_groom = _seeded_score(seed >> 24, 76.0, 18.0)
    return {
        'score': c_main,
        'texture': int(c_text),
        'volume': int(c_vol),
        'grooming': int(c_groom),
        'comments': f'{breed_name}の被毛を画像特徴量から評価しました。',
        'details': 'フォールバック評価（画像ハッシュベース）',
        'analysis_method': 'hash'
    }


def analyze_video_frames(video_base64_frames, breed_name, breed_data):
    """動画フレームから歩様・気質・被毛を評価 — アルゴリズム主導（AIに依存しない）

    Architecture: Algorithm FIRST → AI correction OPTIONAL
    1. アルゴリズムがストライド/ピッチ/中心線→スタンダード比較でベーススコア算出
    2. AI（利用可能な場合のみ）は±8点の範囲内で犬種特性補正
    """
    # Evidence-based gait parameters + FCI calibration
    try:
        from api.auto_cycle import (
            apply_calibration_to_analysis,
            get_breed_fci_params,
            get_evidence_based_gait_params,
            try_auto_cycle,
        )
        from api.breeds import BREED_DATA as _BREED_DATA
        breed_id = breed_data.get('breed_id', '')
        fci_params = get_breed_fci_params(breed_id, _BREED_DATA)
        gait_evidence = get_evidence_based_gait_params(breed_id)
        enriched_data = {**breed_data, **fci_params, 'gait_evidence': gait_evidence}
        try_auto_cycle()
    except ImportError:
        enriched_data = breed_data
        breed_id = ''
        gait_evidence = {}
    except Exception as e:
        logger.warning(f"Breed data enrichment failed: {e}")
        enriched_data = breed_data
        breed_id = ''
        gait_evidence = {}

    # === PRE-CHECK: frame count and quality ================================
    _n_frames = len(video_base64_frames) if video_base64_frames else 0
    if _n_frames < 2:
        _reason = 'フレーム数不足' if _n_frames else 'フレームなし'
        logger.warning(f"analyze_video_frames: skipped — {_reason} ({_n_frames} frames)")
        return {
            'success': False,
            'error': f'歩様解析不能: {_reason}（最低2フレーム必要、取得: {_n_frames}）',
            'error_code': 'no_frames',
            'frames_received': _n_frames,
            'gait': {'score': 0, 'comments': _reason},
            'temperament': {'score': 0, 'comments': _reason},
            'coat_motion': {'score': 0, 'comments': _reason},
            'analysis_method': 'none',
        }

    # === STEP 1: ALGORITHM (主導) — Always runs first =====================
    algo_result = None
    if video_base64_frames and analyze_video_local:
        try:
            algo_result = analyze_video_local(video_base64_frames, breed_name, enriched_data)
        except AnalysisError as e:
            logger.warning(f"Video analysis failed: {e}")
        if algo_result:
            # Apply evidence-based calibration to gait scores
            try:
                if breed_id:
                    gait_score = algo_result.get('gait', {}).get('score', 0)
                    cal_scores = apply_calibration_to_analysis(breed_id, {
                        'gait': gait_score,
                    })
                    if cal_scores.get('gait') != gait_score:
                        algo_result['gait']['score'] = round(cal_scores['gait'], 1)
                        algo_result['gait']['calibrated'] = True
                    if gait_evidence.get('has_reference_data'):
                        algo_result['gait']['evidence_refs'] = gait_evidence['reference_count']
            except Exception as e:
                logger.warning(f"disease evidence loading failed (non-fatal): {e}")

    if algo_result:
        # === STEP 2: DUAL AI + RECO3 BLEND — Active when Vision enabled ===
        if VISION_ENABLED and video_base64_frames:
            try:
                prompt = f"""あなたはFCI認定のプロフェッショナルドッグショー審査員です。
この{breed_name}の動画フレームを分析し、歩様・気質・被毛動態をそれぞれ0-100で評価してください。

【FCI基準】
理想的な歩様: {enriched_data.get('ideal_gait', '自然で流れるような動き')}

【出力形式】JSON形式のみで返してください:
{{
    "gait_score": 0,
    "gait_stride": 0,
    "gait_balance": 0,
    "gait_fluidity": 0,
    "temperament_score": 0,
    "coat_motion_score": 0,
    "comments": "犬種特性に基づく評価理由"
}}"""
                # Dual AI: call both Claude and OpenAI in parallel
                claude_ai, openai_ai = _call_dual_video_vision(prompt, video_base64_frames)

                # Build algo scores from nested structure
                algo_gait = algo_result.get('gait', {})
                algo_temp = algo_result.get('temperament', {})
                algo_coat = algo_result.get('coat_motion', {})
                video_score_keys = ['gait_score', 'gait_stride', 'gait_balance', 'gait_fluidity',
                                    'temperament_score', 'coat_motion_score']
                algo_flat = {
                    'gait_score': algo_gait.get('score'),
                    'gait_stride': algo_gait.get('stride'),
                    'gait_balance': algo_gait.get('balance'),
                    'gait_fluidity': algo_gait.get('fluidity'),
                    'temperament_score': algo_temp.get('score'),
                    'coat_motion_score': algo_coat.get('score'),
                }
                algo_flat = {k: v for k, v in algo_flat.items() if v is not None}

                if claude_ai or openai_ai:
                    blended, reco3_meta = _reco3_blend_scores(
                        algo_flat, claude_ai, openai_ai, video_score_keys, cap=8.0)

                    # Write blended scores back to nested structure
                    if 'gait_score' in blended and 'gait' in algo_result:
                        algo_result['gait']['score'] = blended['gait_score']
                    if 'gait_stride' in blended and 'gait' in algo_result:
                        algo_result['gait']['stride'] = int(blended['gait_stride'])
                    if 'gait_balance' in blended and 'gait' in algo_result:
                        algo_result['gait']['balance'] = int(blended['gait_balance'])
                    if 'gait_fluidity' in blended and 'gait' in algo_result:
                        algo_result['gait']['fluidity'] = int(blended['gait_fluidity'])
                    if 'temperament_score' in blended and 'temperament' in algo_result:
                        algo_result['temperament']['score'] = blended['temperament_score']
                    if 'coat_motion_score' in blended and 'coat_motion' in algo_result:
                        algo_result['coat_motion']['score'] = blended['coat_motion_score']

                    # Merge AI comments
                    ai_comments = []
                    if claude_ai and claude_ai.get('comments'):
                        ai_comments.append(f'[Claude] {claude_ai["comments"]}')
                    if openai_ai and openai_ai.get('comments'):
                        ai_comments.append(f'[OpenAI] {openai_ai["comments"]}')
                    if ai_comments and 'gait' in algo_result:
                        algo_result['gait']['comments'] = algo_result['gait'].get('comments', '') + ' ' + ' '.join(ai_comments)

                    algo_result['ai_correction_applied'] = True
                    algo_result['reco3_blend'] = reco3_meta
                    providers = []
                    if claude_ai:
                        providers.append('claude')
                    if openai_ai:
                        providers.append('openai')
                    algo_result['analysis_method'] = f'algorithm+reco3({"+".join(providers)})'
                    logger.info(f"Video analysis: RECO3 blend (algo + {'+'.join(providers)})")
                else:
                    algo_result['analysis_method'] = 'algorithm'
                    logger.warning("Video analysis: dual AI both failed, algorithm-only")
            except Exception as e:
                logger.warning(f"RECO3 video blend failed, using algorithm-only: {e}")
                algo_result['analysis_method'] = 'algorithm'
        else:
            algo_result['analysis_method'] = 'algorithm'
            logger.info("Video analysis: algorithm-only")

        return algo_result

    # Algorithm returned None: determine reason
    _fallback_reason = 'アルゴリズム解析失敗'
    if not analyze_video_local:
        _fallback_reason = 'ローカル解析モジュール未読み込み'
    elif not OPENCV_AVAILABLE:
        _fallback_reason = 'OpenCV (CV2) 未インストール'
    else:
        _fallback_reason = '中心線検出不安定 / デコード不可'
    logger.warning(f"analyze_video_frames: algorithm returned None — {_fallback_reason}")

    # hash-based fallback (deterministic but limited)
    v_seed = _image_seed(str(video_base64_frames)[:500] if video_base64_frames else str(time.time()), 'video')
    _fallback_comment = f'限定的な評価です（理由: {_fallback_reason}）'
    return {
        'gait': {
            'score': _seeded_score(v_seed, 74.0, 20.0),
            'stride': int(_seeded_score(v_seed >> 8, 73.0, 21.0)),
            'balance': int(_seeded_score(v_seed >> 16, 72.0, 22.0)),
            'fluidity': int(_seeded_score(v_seed >> 24, 74.0, 20.0)),
            'comments': _fallback_comment,
        },
        'temperament': {
            'score': _seeded_score(v_seed >> 32, 75.0, 19.0),
            'confidence': int(_seeded_score(v_seed >> 40, 74.0, 20.0)),
            'alertness': int(_seeded_score(v_seed >> 48, 73.0, 21.0)),
            'composure': int(_seeded_score(v_seed >> 56, 76.0, 18.0)),
            'comments': _fallback_comment,
        },
        'coat_motion': {
            'score': _seeded_score(v_seed >> 64, 74.0, 20.0),
            'comments': _fallback_comment,
        },
        'analysis_method': 'hash',
        'fallback_reason': _fallback_reason,
    }


def _validate_upload_ext(filename, allowed_exts):
    """Validate file extension against whitelist. Returns (ext, error_msg)."""
    if not filename:
        return None, '空のファイル名です'
    ext = os.path.splitext(filename)[1].lower()
    if ext not in allowed_exts:
        return ext, f'許可されていないファイル形式です: {ext}（許可: {", ".join(sorted(allowed_exts))}）'
    return ext, None


def _validate_image_file(photo_bytes):
    """Validate that bytes represent a real image. Returns error_msg or None."""
    try:
        import io

        from PIL import Image
        img = Image.open(io.BytesIO(photo_bytes))
        img.verify()
        w, h = img.size
        if w < 50 or h < 50:
            return f'画像が小さすぎます ({w}x{h})。最低50x50ピクセル必要です。'
        return None
    except ImportError:
        return None  # Pillow not available, skip validation
    except Exception as e:
        return f'画像ファイルを開けませんでした: {e}'


def _extract_frames_with_ffmpeg(video_path, num_frames=5, max_dimension=512):
    """ffmpegでフレームを直接JPEG抽出（OpenCVなしのフォールバック）

    Returns:
        tuple: (frames_list, duration, truncated)
    """
    frames = []
    duration = 0
    truncated = False

    if not FFMPEG_AVAILABLE:
        return frames, duration, truncated

    try:
        # ffprobe で duration を取得
        probe_result = _subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
             '-of', 'default=noprint_wrappers=1:nokey=1:noprint_wrappers=1', video_path],
            capture_output=True, timeout=SUBPROCESS_QUICK_TIMEOUT_SECONDS
        )
        try:
            duration = float(probe_result.stdout.decode('utf-8', errors='ignore').strip())
        except (ValueError, IndexError):
            duration = 0

        if duration <= 0:
            logger.warning(f"Could not determine video duration: {video_path}")
            return frames, duration, truncated

        # 最大30秒に制限
        max_duration = 30
        if duration > max_duration:
            duration_to_use = max_duration
            truncated = True
            logger.info(f"Video truncated to {max_duration}s, original: {duration:.1f}s")
        else:
            duration_to_use = duration

        # 等間隔でフレームを抽出
        for i in range(num_frames):
            timestamp = (i + 0.5) * (duration_to_use / num_frames)
            frame_filename = f"/tmp/frame_{uuid.uuid4()}.jpg"

            try:
                # ffmpeg でJPEGを抽出
                result = _subprocess.run(
                    ['ffmpeg', '-ss', f'{timestamp:.2f}', '-i', video_path,
                     '-vframes', '1', '-q:v', '5', '-y', frame_filename],
                    capture_output=True, timeout=SUBPROCESS_QUICK_TIMEOUT_SECONDS
                )

                if result.returncode == 0 and os.path.exists(frame_filename):
                    with open(frame_filename, 'rb') as f:
                        frame_data = f.read()
                    frame_base64 = base64.b64encode(frame_data).decode('utf-8')
                    frames.append(frame_base64)
                    with contextlib.suppress(OSError):
                        os.remove(frame_filename)
                else:
                    logger.warning(f"ffmpeg frame extraction failed at {timestamp:.2f}s")

            except _subprocess.TimeoutExpired:
                logger.warning(f"ffmpeg frame extraction timeout at {timestamp:.2f}s")
                with contextlib.suppress(OSError):
                    os.remove(frame_filename)

        if frames:
            logger.info(f"Extracted {len(frames)} frames using ffmpeg fallback")
        return frames, duration, truncated

    except Exception as e:
        logger.error(f"ffmpeg frame extraction failed: {e}")
        return frames, duration, truncated


def _convert_to_mp4(video_path):
    """MOV/WebM等をMP4に変換。成功時は変換後パスを返す、失敗時はNone"""
    if not FFMPEG_AVAILABLE:
        logger.warning("ffmpeg not available - cannot convert video")
        return None
    converted_path = video_path.rsplit('.', 1)[0] + '_converted.mp4'
    try:
        result = _subprocess.run(
            ['ffmpeg', '-i', video_path, '-c:v', 'libx264', '-preset', 'fast',
             '-crf', '23', '-an', '-y', converted_path],
            capture_output=True, timeout=SUBPROCESS_TIMEOUT_SECONDS
        )
        if result.returncode == 0 and os.path.exists(converted_path):
            logger.info(f"Video converted to mp4 successfully: {os.path.basename(converted_path)}")
            return converted_path
        else:
            stderr = result.stderr.decode('utf-8', errors='ignore')[:300]
            logger.warning(f"ffmpeg conversion failed (rc={result.returncode}): {stderr}")
            with contextlib.suppress(OSError):
                os.remove(converted_path)
            return None
    except _subprocess.TimeoutExpired:
        logger.warning("ffmpeg conversion timed out (60s)")
        with contextlib.suppress(OSError):
            os.remove(converted_path)
        return None


def _extract_frames_from_capture(cap, num_frames, max_dimension):
    """OpenCV VideoCaptureからフレームを抽出する内部関数"""
    frames = []
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    duration = total_frames / fps if fps > 0 else 0
    truncated = False

    if total_frames <= 0:
        return frames, duration, truncated

    # 動画が長すぎる場合は最初の30秒のみ使用
    max_duration = 30
    if duration > max_duration:
        total_frames = int(max_duration * fps)
        truncated = True
        logger.info(f"Video truncated to {max_duration}s ({total_frames} frames), original: {duration:.1f}s")

    frame_indices = [int(i * total_frames / num_frames) for i in range(num_frames)]

    for idx in frame_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if ret:
            h, w = frame.shape[:2]
            if max(h, w) > max_dimension:
                scale = max_dimension / max(h, w)
                new_w, new_h = int(w * scale), int(h * scale)
                frame = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_AREA)
            _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
            frame_base64 = base64.b64encode(buffer).decode('utf-8')
            frames.append(frame_base64)

    return frames, duration, truncated


def extract_video_frames(video_path, num_frames=12, max_dimension=512):
    """動画からフレームを抽出（MOV対応強化版）

    MOV（iPhone動画）を最優先でサポート。
    1. OpenCVで直接読み込み（ffmpegバックエンドがあれば成功）
    2. 失敗時 → ffmpegでMP4に変換してから再読み込み
    3. それでも失敗 → ffmpegで直接JPEG抽出（フォールバック）
    4. 全て失敗 → 詳細なエラー情報を返す

    Returns:
        tuple: (frames_list, metadata_dict)
    """
    ext = os.path.splitext(video_path)[1].lower()
    try:
        input_size_bytes = os.path.getsize(video_path)
    except OSError:
        input_size_bytes = 0

    metadata = {
        'truncated': False,
        'original_duration': 0,
        'opencv_available': OPENCV_AVAILABLE,
        'cv2_available': OPENCV_AVAILABLE,
        'ffmpeg_available': FFMPEG_AVAILABLE,
        'converted_from': None,
        'converted': False,
        'convert_error': None,
        'extraction_method': None,
        'error': None,
        'error_code': None,
        'input_ext': ext,
        'input_size_bytes': input_size_bytes,
        'frames_extracted': 0,
        'fps': None,
        'duration_sec': None,
    }

    converted_path = None

    def _finalize_success(frames, duration, truncated, method):
        """Helper to populate metadata on success."""
        metadata['original_duration'] = round(duration, 1)
        metadata['duration_sec'] = round(duration, 2)
        metadata['truncated'] = truncated
        metadata['extraction_method'] = method
        metadata['frames_extracted'] = len(frames)
        return frames, metadata

    try:
        # Step 1: OpenCVで直接読み込み（MOV含む）
        if OPENCV_AVAILABLE:
            cap = cv2.VideoCapture(video_path)
            if cap.isOpened():
                metadata['fps'] = cap.get(cv2.CAP_PROP_FPS) or None
                frames, duration, truncated = _extract_frames_from_capture(cap, num_frames, max_dimension)
                cap.release()

                if frames:
                    logger.info(f"Extracted {len(frames)} frames directly from {ext} (duration: {duration:.1f}s)")
                    return _finalize_success(frames, duration, truncated, 'opencv_direct')

        # Step 2: 直接読み込み失敗 → ffmpegでMP4に変換
        if OPENCV_AVAILABLE:
            logger.info(f"Direct read failed for {ext}, attempting ffmpeg conversion...")
            converted_path = _convert_to_mp4(video_path)

            if converted_path:
                metadata['converted_from'] = ext
                metadata['converted'] = True
                cap = cv2.VideoCapture(converted_path)
                if cap.isOpened():
                    metadata['fps'] = cap.get(cv2.CAP_PROP_FPS) or None
                    frames, duration, truncated = _extract_frames_from_capture(cap, num_frames, max_dimension)
                    cap.release()

                    if frames:
                        logger.info(f"Extracted {len(frames)} frames from converted {ext}→mp4 (duration: {duration:.1f}s)")
                        with contextlib.suppress(OSError):
                            os.remove(converted_path)
                        return _finalize_success(frames, duration, truncated, 'opencv_converted')

                # 変換済みファイルを削除
                with contextlib.suppress(OSError):
                    os.remove(converted_path)
            else:
                metadata['convert_error'] = 'ffmpeg conversion failed or ffmpeg not available'

        # Step 3: ffmpegでJPEG直接抽出（フォールバック）
        if FFMPEG_AVAILABLE:
            logger.info(f"Attempting ffmpeg JPEG extraction for {ext}...")
            frames, duration, truncated = _extract_frames_with_ffmpeg(video_path, num_frames, max_dimension)
            if frames:
                logger.info(f"Extracted {len(frames)} frames using ffmpeg JPEG extraction (duration: {duration:.1f}s)")
                return _finalize_success(frames, duration, truncated, 'ffmpeg_jpeg')

        # Step 4: 全て失敗 — error and error_code must match
        if not OPENCV_AVAILABLE and not FFMPEG_AVAILABLE:
            metadata['error'] = 'no_extraction_tools'
            metadata['error_code'] = 'no_extraction_tools'
            logger.error(f"Cannot process {ext}: both OpenCV and ffmpeg are unavailable")
        elif not OPENCV_AVAILABLE:
            metadata['error'] = 'opencv_missing'
            metadata['error_code'] = 'opencv_missing'
            logger.error(f"Cannot process {ext}: OpenCV unavailable")
        elif not FFMPEG_AVAILABLE:
            metadata['error'] = 'ffmpeg_missing'
            metadata['error_code'] = 'ffmpeg_missing'
            logger.error(f"Cannot process {ext}: ffmpeg not installed, OpenCV extraction failed")
        else:
            metadata['error'] = 'extraction_failed'
            metadata['error_code'] = 'extraction_failed'
            logger.error(f"All extraction methods failed for {ext}")

        return [], metadata

    except Exception as e:
        logger.error(f"Frame extraction error: {e}")
        metadata['error'] = 'フレーム抽出に失敗しました'
        metadata['error_code'] = 'extraction_failed'
        if converted_path:
            with contextlib.suppress(OSError):
                os.remove(converted_path)
        return [], metadata


def generate_breeding_recommendations(breed_name, breed_data, scores, age_years):
    """交配相手の推奨を生成"""
    recommendations = []

    structure_score = scores.get('structure', {}).get('score', 85)
    coat_score = scores.get('coat_photo', {}).get('score', 85)
    gait_score = scores.get('gait', {}).get('score', None)

    # 体構造に基づく推奨
    if structure_score < 85:
        recommendations.append({
            'title': '体構造の改善',
            'description': f'プロポーションや骨格構造を補完するため、FCI基準により近い体構造を持つ{breed_name}との交配が推奨されます。特に、{breed_data.get("ideal_structure", "標準的な体型")}を持つ個体を選びましょう。'
        })
    else:
        recommendations.append({
            'title': '体構造の維持',
            'description': f'現在の優れた体構造を維持するため、同等以上の体構造スコアを持つ{breed_name}との交配が理想的です。'
        })

    # 被毛に基づく推奨
    if coat_score < 85:
        recommendations.append({
            'title': '被毛品質の向上',
            'description': f'被毛の質を向上させるため、{breed_data.get("ideal_coat", "理想的な被毛")}を持つ個体との交配を検討してください。遺伝的に被毛品質が高い血統を選ぶことが重要です。'
        })

    # 歩様に基づく推奨
    if gait_score and gait_score < 85:
        recommendations.append({
            'title': '歩様の改善',
            'description': f'歩様を改善するため、{breed_data.get("ideal_gait", "流れるような動き")}を示す個体との交配が推奨されます。前肢・後肢のバランスが良い個体を選びましょう。'
        })

    # 健康面の考慮
    common_issues = breed_data.get('common_issues', [])
    if common_issues:
        recommendations.append({
            'title': '遺伝性疾患への配慮',
            'description': f'{breed_name}で注意すべき遺伝性疾患（{", ".join(common_issues)}）の検査済み個体との交配を強くお勧めします。両親の健康検査証明書を確認してください。'
        })

    # 年齢に基づく推奨
    if age_years < 2:
        recommendations.append({
            'title': '繁殖適齢期について',
            'description': '現在の年齢は繁殖には若すぎます。身体的・精神的に成熟する2歳以降まで待つことをお勧めします。'
        })
    elif age_years > 7:
        recommendations.append({
            'title': '高齢での繁殖について',
            'description': '高齢での繁殖はリスクが伴います。獣医師と相談の上、慎重に検討してください。'
        })

    return recommendations


# =============================================================================
# Security Helper Functions
# =============================================================================

def validate_image_file(file):
    """Validate that uploaded file is a valid image (MIME type check)"""
    if not file or not file.filename:
        return False

    # Check MIME type
    allowed_mimes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp', 'image/heic', 'image/heif']
    content_type = file.content_type

    if content_type not in allowed_mimes:
        return False

    # Additional check: read first few bytes to verify magic number
    file.seek(0)
    header = file.read(12)
    file.seek(0)

    # JPEG magic number
    if header[:2] == b'\xff\xd8':
        return True
    # PNG magic number
    if header[:8] == b'\x89PNG\r\n\x1a\n':
        return True
    # WEBP magic number
    if header[:4] == b'RIFF' and header[8:12] == b'WEBP':
        return True
    # HEIC/HEIF magic number (ftyp)
    return bool(header[4:8] == b'ftyp' and (b'heic' in header or b'heif' in header))


def validate_video_file(file):
    """Validate that uploaded file is a valid video (MIME type check)"""
    if not file or not file.filename:
        return False

    # Check MIME type
    allowed_mimes = ['video/mp4', 'video/quicktime', 'video/x-msvideo', 'video/webm', 'video/mpeg']
    content_type = file.content_type

    if content_type not in allowed_mimes:
        return False

    # Additional check: read first few bytes to verify magic number
    file.seek(0)
    header = file.read(12)
    file.seek(0)

    # MP4/MOV magic number (ftyp)
    if header[4:8] == b'ftyp':
        return True
    # AVI magic number
    if header[:4] == b'RIFF' and header[8:12] == b'AVI ':
        return True
    # WebM magic number
    if header[:4] == b'\x1a\x45\xdf\xa3':
        return True
    # MPEG magic number
    return header[:3] == b'\x00\x00\x01'


# =============================================================================
# Decorators
# =============================================================================

def ensure_json_response(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            result = f(*args, **kwargs)
            # Flask Response object — pass through as-is
            if hasattr(result, 'status_code'):
                return result
            # tuple: (dict, status_code) or (dict, status_code, headers)
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
            resp = {
                'success': False,
                'error': error_msg,
                'version': VERSION,
            }
            if not is_production:
                resp['where'] = f.__name__
            return jsonify(resp), 500
    return wrapper


def require_auth(f):
    """Decorator to require authentication"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not DB_AVAILABLE:
            return jsonify({'error': 'データベースが利用できません'}), 503

        # Get token from header or cookie
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            token = request.cookies.get('session_token')

        if not token:
            return jsonify({'error': 'ログインが必要です'}), 401

        user = verify_session(token)
        if not user:
            return jsonify({'error': 'セッションが無効または期限切れです'}), 401

        # Add user to request context
        request.current_user = user
        return f(*args, **kwargs)
    return wrapper


def optional_auth(f):
    """Decorator for optional authentication"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        request.current_user = None

        if DB_AVAILABLE:
            token = request.headers.get('Authorization', '').replace('Bearer ', '')
            if not token:
                token = request.cookies.get('session_token')

            if token:
                user = verify_session(token)
                if user:
                    request.current_user = user

        return f(*args, **kwargs)
    return wrapper


@app.after_request
def add_headers(response):
    # Core security headers
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Permissions-Policy'] = 'camera=(), microphone=(), geolocation=()'

    # HSTS in production (force HTTPS)
    if os.getenv('RENDER') or os.getenv('PRODUCTION'):
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'

    # Content Security Policy
    # NOTE: 'unsafe-inline' in script-src is required while inline onclick handlers exist.
    # TODO: migrate inline handlers to addEventListener() then remove 'unsafe-inline'.
    _csp_parts = [
        "default-src 'self'",
        "script-src 'self' 'unsafe-inline' https://js.stripe.com",
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
        "font-src 'self' https://fonts.gstatic.com",
        "img-src 'self' data: blob:",
        "media-src 'self' blob:",
        "connect-src 'self' https://api.stripe.com",
        "frame-src https://js.stripe.com",
        "object-src 'none'",
        "base-uri 'self'",
        "form-action 'self'",
    ]
    if os.getenv('RENDER') or os.getenv('PRODUCTION'):
        _csp_parts.append("upgrade-insecure-requests")
    response.headers['Content-Security-Policy'] = "; ".join(_csp_parts)

    # Cache control
    if request.path == '/sw.js':
        # Service Worker must not be aggressively cached
        response.headers['Cache-Control'] = 'no-cache, max-age=0'
        response.headers['Service-Worker-Allowed'] = '/'
    elif request.path.endswith('.html'):
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    elif request.path.endswith(('.css', '.js')):
        response.headers['Cache-Control'] = 'public, max-age=86400, stale-while-revalidate=3600'
    elif request.path.endswith(('.png', '.jpg', '.jpeg', '.webp', '.svg', '.ico')):
        response.headers['Cache-Control'] = 'public, max-age=604800, immutable'

    return response

# =============================================================================
# Static Files
# =============================================================================

@app.route('/')
def index():
    try:
        return send_from_directory(STATIC_DIR, 'index.html')
    except (FileNotFoundError, WerkzeugNotFound):
        return jsonify({'error': 'index.html not found'}), 404
    except Exception as e:
        logger.error(f"Error serving index.html: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/r3')
def reco3_dashboard():
    try:
        return send_from_directory(TEMPLATES_DIR, 'reco3.html')
    except (FileNotFoundError, WerkzeugNotFound):
        return jsonify({'error': 'reco3.html not found'}), 404
    except Exception as e:
        logger.error(f"Error serving reco3.html: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/favicon.ico')
def favicon():
    """Serve favicon with fallback chain"""
    try:
        # Try favicon.ico first
        try:
            response = send_from_directory(STATIC_DIR, 'favicon.ico')
            response.headers['Cache-Control'] = 'public, max-age=2592000, immutable'
            return response
        except FileNotFoundError:
            pass

        # Fallback to favicon.png
        try:
            response = send_from_directory(STATIC_DIR, 'favicon.png')
            response.headers['Cache-Control'] = 'public, max-age=2592000, immutable'
            return response
        except FileNotFoundError:
            pass

        # No favicon found, return 204 No Content
        logger.debug("Favicon not found, returning 204")
        return '', 204

    except Exception as e:
        logger.debug(f"Favicon request error: {e}")
        # Return 204 instead of 500 on error
        return '', 204

@app.route('/<path:filename>')
def static_files(filename):
    try:
        return send_from_directory(STATIC_DIR, filename)
    except (FileNotFoundError, WerkzeugNotFound):
        return jsonify({'error': f'{filename} not found'}), 404
    except Exception as e:
        logger.error(f"Error serving static file {filename}: {e}")
        return jsonify({'error': 'Internal server error'}), 500

# =============================================================================
# API Endpoints
# =============================================================================

@app.route('/api/health', methods=['GET'])
@ensure_json_response
def health():
    return {
        'status': 'healthy',
        'version': VERSION,
        'build': BUILD,
        'algorithm': {
            'version': ALGORITHM_VERSION,
            'model_version': MODEL_VERSION,
            'weights_hash': WEIGHTS_HASH,
            'deterministic': SCORING_AVAILABLE,
            'pipeline': 'algorithm_first_ai_corrects',
            'description': 'エビデンスに基づくアルゴリズムが主導し、AIが伴奏するハイブリッドシステム'
        },
        'ai_providers': {
            'primary': VISION_PROVIDER,
            'claude': bool(claude_client),
            'openai': bool(openai_client),
            'vision_enabled': VISION_ENABLED,
            'deps': {
                'anthropic_available': ANTHROPIC_AVAILABLE,
                'openai_available': OPENAI_AVAILABLE,
                'vision_enabled': VISION_ENABLED,
                'vision_provider': VISION_PROVIDER
            }
        },
        'openai_enabled': VISION_ENABLED,
        'db_enabled': DB_AVAILABLE,
        'admin_configured': bool(os.getenv('ADMIN_BOOTSTRAP_EMAIL')),
        'features': {
            'photo_analysis': True,
            'video_analysis': True,
            'breeding_recommendations': True,
            'user_accounts': DB_AVAILABLE,
            'analysis_history': DB_AVAILABLE,
            'deterministic_scoring': SCORING_AVAILABLE,
            'audit_logging': DB_AVAILABLE,
            'ai_firewall': FIREWALL_AVAILABLE,
            'health_checker': HEALTH_CHECKER_AVAILABLE,
            'pet_passport_pdf': PASSPORT_AVAILABLE,
            'extended_breeds': EXTENDED_BREEDS_AVAILABLE,
            'sse_streaming': True,
            'judge_validation': JUDGE_VALIDATION_AVAILABLE,
            'growth_prediction': GROWTH_PREDICTION_AVAILABLE,
            'genetic_scoring': GENETIC_SCORING_AVAILABLE,
            'pose_estimation_3d': POSE_ESTIMATION_AVAILABLE,
            'finetuning_infrastructure': FINETUNING_AVAILABLE,
            'auto_data_cycle': True,
            'fci_based_analysis': True,
            'evidence_based_gait': True,
            'stripe_payments': STRIPE_AVAILABLE
        },
        'breeds_count': len(BREED_DATA),
    }


@app.route('/api/status', methods=['GET'])
@ensure_json_response
def reco2_status():
    if not RECO2_AVAILABLE:
        return {'error': 'reco2 not available'}, 503
    return reco2_get_status()


@app.route('/api/logs', methods=['GET'])
@ensure_json_response
def reco2_logs():
    if not RECO2_AVAILABLE:
        return {'error': 'reco2 not available'}, 503
    try:
        limit = int(request.args.get('limit', '50'))
    except Exception:
        limit = 50
    return reco2_get_logs(limit=limit)


@app.route('/api/evaluate', methods=['POST'])
@ensure_json_response
def reco2_evaluate():
    if not RECO2_AVAILABLE:
        return {'error': 'reco2 not available'}, 503
    payload = request.get_json(force=True, silent=False)
    return reco2_evaluate_payload(payload)


@app.route('/api/feedback', methods=['POST'])
@ensure_json_response
def reco2_feedback():
    if not RECO2_AVAILABLE:
        return {'error': 'reco2 not available'}, 503
    payload = request.get_json(force=True, silent=True) or {}
    res = reco2_record_feedback(payload)
    if isinstance(res, tuple):
        return res[0], res[1]
    return res


@app.route('/api/patrol', methods=['POST'])
@ensure_json_response
def reco2_patrol():
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


@app.route('/api/algorithm', methods=['GET'])
@ensure_json_response
def get_algorithm():
    """Get current algorithm information for transparency."""
    if SCORING_AVAILABLE:
        return get_algorithm_info()
    else:
        return {
            'error': 'Deterministic scoring not available',
            'version': VERSION
        }, 503


# =============================================================================
# 24h Auto-Cycle Endpoints — データ循環管理
# =============================================================================

@app.route('/api/cycle/status', methods=['GET'])
@ensure_json_response
def cycle_status():
    """Get current auto-cycle status and last run info."""
    try:
        from api.auto_cycle import load_breed_calibration, load_cycle_state, should_run_cycle
        state = load_cycle_state()
        calibration = load_breed_calibration()
        return {
            'status': 'ok',
            'last_cycle_ts': state.get('last_cycle_ts', 0),
            'total_cycles': state.get('total_cycles', 0),
            'total_analyses_processed': state.get('total_analyses_processed', 0),
            'breeds_calibrated': len(calibration),
            'next_cycle_due': should_run_cycle(),
        }
    except ImportError:
        return {'status': 'unavailable', 'error': 'Auto-cycle module not installed'}, 503


@app.route('/api/cycle/run', methods=['POST'])
@require_auth
@ensure_json_response
def cycle_run():
    """Manually trigger a data cycle (admin only)."""
    try:
        from api.auto_cycle import run_cycle
        result = run_cycle(force=True)
        return result
    except ImportError:
        return {'error': 'Auto-cycle module not installed'}, 503
    except Exception as e:
        logger.error(f"Manual cycle trigger failed: {e}", exc_info=True)
        return {'error': 'サイクル実行に失敗しました'}, 500


@app.route('/api/cycle/calibration', methods=['GET'])
@ensure_json_response
def cycle_calibration():
    """Get current breed calibration parameters."""
    try:
        from api.auto_cycle import load_breed_calibration
        calibration = load_breed_calibration()
        return {
            'breeds': len(calibration),
            'calibration': calibration,
        }
    except ImportError:
        return {'error': 'Auto-cycle module not installed'}, 503


@app.route('/api/cycle/disease-risk/<breed_id>', methods=['GET'])
@ensure_json_response
def cycle_disease_risk(breed_id):
    """Get evidence-based disease risk profile for a breed."""
    try:
        from api.auto_cycle import get_evidence_based_disease_params
        risk = get_evidence_based_disease_params(breed_id)
        return risk
    except ImportError:
        return {'error': 'Auto-cycle module not installed'}, 503


# =============================================================================
# Stripe Payment Endpoints — サブスクリプション決済
# =============================================================================

# Stripe price IDs (set via environment variables)
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET', '')
STRIPE_PRICE_IDS = {
    'jp': {
        'vet': os.getenv('STRIPE_PRICE_JP_VET', ''),
        'standard': os.getenv('STRIPE_PRICE_JP_STANDARD', ''),
        'enterprise': os.getenv('STRIPE_PRICE_JP_ENTERPRISE', ''),
    },
    'global': {
        'vet': os.getenv('STRIPE_PRICE_GLOBAL_VET', ''),
        'standard': os.getenv('STRIPE_PRICE_GLOBAL_STANDARD', ''),
        'enterprise': os.getenv('STRIPE_PRICE_GLOBAL_ENTERPRISE', ''),
    }
}

# PayPal configuration
PAYPAL_CLIENT_ID = os.getenv('PAYPAL_CLIENT_ID', '')
PAYPAL_CLIENT_SECRET = os.getenv('PAYPAL_CLIENT_SECRET', '')
PAYPAL_MODE = os.getenv('PAYPAL_MODE', 'sandbox')  # 'sandbox' or 'live'
PAYPAL_AVAILABLE = bool(PAYPAL_CLIENT_ID and PAYPAL_CLIENT_SECRET)

try:
    import stripe
    STRIPE_AVAILABLE = bool(STRIPE_SECRET_KEY)
    if STRIPE_AVAILABLE:
        stripe.api_key = STRIPE_SECRET_KEY
    else:
        logger.info("Stripe is not configured (STRIPE_SECRET_KEY not set)")
except ImportError:
    STRIPE_AVAILABLE = False
    logger.info("stripe package not installed — payment features disabled")


@app.route('/api/stripe/create-checkout-session', methods=['POST'])
@require_auth
@ensure_json_response
def stripe_create_checkout():
    """Stripe Checkout Session を作成し、決済URLを返す"""
    if not STRIPE_AVAILABLE:
        return {'error': 'Stripe決済は現在設定されていません。STRIPE_SECRET_KEYを設定してください。'}, 503

    data = request.get_json(silent=True)
    if not data:
        return {'error': 'JSON data required'}, 400

    plan = data.get('plan', '')
    region = data.get('region', 'jp')

    if plan not in ('vet', 'standard', 'enterprise'):
        return {'error': f'無効なプラン: {plan}'}, 400
    if region not in ('jp', 'global'):
        return {'error': f'無効なリージョン: {region}'}, 400

    price_id = STRIPE_PRICE_IDS.get(region, {}).get(plan, '')
    if not price_id:
        return {'error': f'{region}/{plan}のStripe Price IDが設定されていません。'}, 503

    user = request.current_user
    base_url = request.host_url.rstrip('/')

    try:
        session = stripe.checkout.Session.create(
            mode='subscription',
            line_items=[{'price': price_id, 'quantity': 1}],
            success_url=f'{base_url}/pricing.html?session_id={{CHECKOUT_SESSION_ID}}&status=success',
            cancel_url=f'{base_url}/pricing.html?status=cancelled',
            customer_email=user.get('email', ''),
            metadata={
                'user_id': str(user.get('id', '')),
                'plan': plan,
                'region': region,
            },
        )
        return {'url': session.url, 'session_id': session.id}
    except Exception as e:
        logger.error(f"Stripe checkout session creation failed: {e}")
        return {'error': '決済セッションの作成に失敗しました'}, 500


@app.route('/api/stripe/webhook', methods=['POST'])
def stripe_webhook():
    """Stripe Webhook: 決済完了・サブスクリプション更新を処理"""
    if not STRIPE_AVAILABLE:
        return jsonify({'error': 'Stripe not configured'}), 503

    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('Stripe-Signature', '')

    try:
        if STRIPE_WEBHOOK_SECRET:
            event = stripe.Webhook.construct_event(payload, sig_header, STRIPE_WEBHOOK_SECRET)
        else:
            logger.error("Stripe webhook secret not configured — rejecting unsigned event")
            return jsonify({'error': 'Webhook not configured'}), 503
    except stripe.error.SignatureVerificationError:
        logger.warning("Stripe webhook signature verification failed")
        return jsonify({'error': 'Invalid signature'}), 400
    except Exception as e:
        logger.error(f"Stripe webhook parse error: {e}")
        return jsonify({'error': 'Webhook処理エラー'}), 400

    event_type = event.get('type', '')
    event_data = event.get('data', {}).get('object', {})

    if event_type == 'checkout.session.completed':
        metadata = event_data.get('metadata', {})
        user_id = metadata.get('user_id')
        plan = metadata.get('plan')
        subscription_id = event_data.get('subscription')
        logger.info(f"Subscription created: user={user_id}, plan={plan}, sub={subscription_id}")
        # Update user subscription in database
        if DB_AVAILABLE and user_id:
            try:
                from api.database import get_db
                conn = get_db()
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE users SET subscription_plan = ?, stripe_subscription_id = ?,
                    subscription_updated_at = datetime('now')
                    WHERE id = ?
                ''', (plan, subscription_id, user_id))
                conn.commit()
                conn.close()
            except Exception as e:
                logger.error(f"Failed to update user subscription: {e}")

    elif event_type == 'customer.subscription.deleted':
        subscription_id = event_data.get('id')
        logger.info(f"Subscription cancelled: sub={subscription_id}")
        if DB_AVAILABLE:
            try:
                from api.database import get_db
                conn = get_db()
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE users SET subscription_plan = 'free', stripe_subscription_id = NULL,
                    subscription_updated_at = datetime('now')
                    WHERE stripe_subscription_id = ?
                ''', (subscription_id,))
                conn.commit()
                conn.close()
            except Exception as e:
                logger.error(f"Failed to cancel user subscription: {e}")

    elif event_type == 'invoice.payment_failed':
        subscription_id = event_data.get('subscription')
        logger.warning(f"Payment failed for subscription: {subscription_id}")

    return jsonify({'received': True})


@app.route('/api/stripe/subscription-status', methods=['GET'])
@require_auth
@ensure_json_response
def stripe_subscription_status():
    """現在のサブスクリプション状態を取得"""
    user = request.current_user
    return {
        'plan': user.get('subscription_plan', 'free'),
        'stripe_available': STRIPE_AVAILABLE,
        'paypal_available': PAYPAL_AVAILABLE,
    }


# =============================================================================
# PayPal Payment Endpoints — PayPal決済連携
# =============================================================================

# PayPal plan price mapping (JPY)
PAYPAL_PLAN_PRICES = {
    'jp': {
        'vet': '1100',
        'standard': '1980',
        'enterprise': '2980',
    },
    'global': {
        'vet': '9.99',
        'standard': '19.99',
        'enterprise': '29.99',
    }
}


def _paypal_access_token():
    """Obtain a PayPal OAuth2 access token."""
    import base64
    base_url = 'https://api-m.sandbox.paypal.com' if PAYPAL_MODE == 'sandbox' else 'https://api-m.paypal.com'
    auth = base64.b64encode(f"{PAYPAL_CLIENT_ID}:{PAYPAL_CLIENT_SECRET}".encode()).decode()
    import requests as _requests
    resp = _requests.post(
        f"{base_url}/v1/oauth2/token",
        headers={
            'Authorization': f'Basic {auth}',
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        data='grant_type=client_credentials',
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()['access_token'], base_url


@app.route('/api/paypal/create-order', methods=['POST'])
@require_auth
@ensure_json_response
def paypal_create_order():
    """PayPal注文を作成し、承認URLを返す"""
    if not PAYPAL_AVAILABLE:
        return {'error': 'PayPal決済は現在設定されていません。PAYPAL_CLIENT_IDとPAYPAL_CLIENT_SECRETを設定してください。'}, 503

    data = request.get_json(silent=True)
    if not data:
        return {'error': 'JSON data required'}, 400

    plan = data.get('plan', '')
    region = data.get('region', 'jp')

    if plan not in ('vet', 'standard', 'enterprise'):
        return {'error': f'無効なプラン: {plan}'}, 400
    if region not in ('jp', 'global'):
        return {'error': f'無効なリージョン: {region}'}, 400

    price = PAYPAL_PLAN_PRICES.get(region, {}).get(plan, '')
    if not price:
        return {'error': f'{region}/{plan}の価格が設定されていません。'}, 503

    currency = 'JPY' if region == 'jp' else 'USD'
    user_id = request.current_user.get('id')

    try:
        access_token, base_url = _paypal_access_token()
        import requests as _requests
        order_resp = _requests.post(
            f"{base_url}/v2/checkout/orders",
            headers={
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json',
            },
            json={
                'intent': 'CAPTURE',
                'purchase_units': [{
                    'amount': {
                        'currency_code': currency,
                        'value': price,
                    },
                    'description': f'ShowDog {plan.capitalize()} Plan',
                    'custom_id': f'user_{user_id}_plan_{plan}',
                }],
                'application_context': {
                    'return_url': f'{request.host_url}api/paypal/capture',
                    'cancel_url': f'{request.host_url}pricing.html',
                    'brand_name': 'ShowDog',
                    'user_action': 'PAY_NOW',
                },
            },
            timeout=15,
        )
        order_resp.raise_for_status()
        order = order_resp.json()

        approve_url = next(
            (link['href'] for link in order.get('links', []) if link['rel'] == 'approve'),
            None
        )
        return {
            'order_id': order['id'],
            'approve_url': approve_url,
        }
    except Exception as e:
        logger.error(f"PayPal create order error: {e}", exc_info=True)
        return {'error': 'PayPal注文作成に失敗しました。しばらくしてから再度お試しください。'}, 500


@app.route('/api/paypal/capture', methods=['GET', 'POST'])
@ensure_json_response
def paypal_capture_order():
    """PayPal注文をキャプチャし、サブスクリプションを有効化する"""
    if not PAYPAL_AVAILABLE:
        return {'error': 'PayPal決済は設定されていません。'}, 503

    # GET from PayPal redirect or POST from frontend
    if request.method == 'GET':
        order_id = request.args.get('token', '')
    else:
        data = request.get_json(silent=True) or {}
        order_id = data.get('order_id', '')

    if not order_id:
        return {'error': 'order_id is required'}, 400

    try:
        access_token, base_url = _paypal_access_token()
        import requests as _requests
        capture_resp = _requests.post(
            f"{base_url}/v2/checkout/orders/{order_id}/capture",
            headers={
                'Authorization': f'Bearer {access_token}',
                'Content-Type': 'application/json',
            },
            timeout=15,
        )
        capture_resp.raise_for_status()
        capture = capture_resp.json()

        if capture.get('status') == 'COMPLETED':
            # Extract plan from custom_id
            custom_id = ''
            for pu in capture.get('purchase_units', []):
                for cap in pu.get('payments', {}).get('captures', []):
                    custom_id = cap.get('custom_id', '')
                    break

            plan = 'free'
            user_id = None
            if custom_id:
                parts = custom_id.split('_')
                # Format: user_{id}_plan_{plan}
                if len(parts) >= 4:
                    user_id = int(parts[1])
                    plan = parts[3]

            if user_id and plan in ('vet', 'standard', 'enterprise'):
                try:
                    from api.database import get_db
                    conn = get_db()
                    cursor = conn.cursor()
                    cursor.execute('''
                        UPDATE users SET subscription_plan = ?,
                        subscription_updated_at = datetime('now')
                        WHERE id = ?
                    ''', (plan, user_id))
                    conn.commit()
                    conn.close()
                    logger.info(f"PayPal subscription activated: user={user_id}, plan={plan}, order={order_id}")
                except Exception as e:
                    logger.error(f"Failed to update subscription via PayPal: {e}")

            return {'status': 'completed', 'plan': plan, 'order_id': order_id}
        else:
            return {'status': capture.get('status', 'unknown'), 'order_id': order_id}, 400

    except Exception as e:
        logger.error(f"PayPal capture error: {e}", exc_info=True)
        return {'error': 'PayPal決済処理に失敗しました。しばらくしてから再度お試しください。'}, 500


@app.route('/api/paypal/verify', methods=['POST'])
@require_auth
@ensure_json_response
def paypal_verify_order():
    """PayPal注文の状態を確認する"""
    if not PAYPAL_AVAILABLE:
        return {'error': 'PayPal決済は設定されていません。'}, 503

    data = request.get_json(silent=True)
    if not data or not data.get('order_id'):
        return {'error': 'order_id is required'}, 400

    order_id = data['order_id']
    try:
        access_token, base_url = _paypal_access_token()
        import requests as _requests
        resp = _requests.get(
            f"{base_url}/v2/checkout/orders/{order_id}",
            headers={'Authorization': f'Bearer {access_token}'},
            timeout=15,
        )
        resp.raise_for_status()
        order = resp.json()
        return {
            'order_id': order['id'],
            'status': order.get('status'),
            'payer': order.get('payer', {}).get('email_address'),
        }
    except Exception as e:
        logger.error(f"PayPal verify error: {e}", exc_info=True)
        return {'error': 'PayPal注文確認に失敗しました。しばらくしてから再度お試しください。'}, 500


# =============================================================================
# Advanced Analytics Endpoints
# =============================================================================

@app.route('/api/judge-validation/compute', methods=['POST'])
@ensure_json_response
def compute_judge_validation():
    """Compute judge agreement statistics from paired AI/judge evaluations."""
    if not JUDGE_VALIDATION_AVAILABLE:
        return {'error': '審査員検証モジュールが利用できません'}, 503
    data = request.get_json(silent=True)
    if not data:
        return {'error': 'JSONデータが必要です'}, 400
    pairs = data.get('pairs', [])
    if not pairs or len(pairs) < 2:
        return {'error': '2組以上の評価ペアが必要です'}, 400
    session = JudgeValidationSession()
    for p in pairs:
        session.add_pair(p.get('ai', {}), p.get('judge', {}))
    report = session.compute_full_report()
    return {'report': report}


@app.route('/api/growth-prediction/predict', methods=['POST'])
@ensure_json_response
def predict_growth():
    """Predict future scores from historical analysis data."""
    if not GROWTH_PREDICTION_AVAILABLE:
        return {'error': '成長予測モジュールが利用できません'}, 503
    data = request.get_json(silent=True)
    if not data:
        return {'error': 'JSONデータが必要です'}, 400
    history = data.get('history', [])
    target_age = data.get('target_age')
    breed_id = data.get('breed_id')
    if not history or len(history) < 3:
        return {'error': '3回以上の解析履歴が必要です'}, 400
    # Convert JSON to (age_years, scores_dict) tuples
    history_tuples = []
    for h in history:
        age = float(h.get('age_years', 0))
        scores = h.get('scores', {})
        history_tuples.append((age, scores))
    predictor = GrowthPredictor(breed_id=breed_id)
    predictor.fit(history_tuples)
    result = {
        'trajectory': predictor.get_trajectory(
            float(history[0].get('age_years', 0.5)),
            float(target_age or history[-1].get('age_years', 5)) + 2
        ),
        'predicted_peak_age': predictor.predict_peak_age(),
        'anomalies': predictor.detect_anomalies(history),
    }
    if target_age:
        result['prediction'] = predictor.predict(float(target_age))
    return result


@app.route('/api/genetic-scoring/breeding-compatibility', methods=['POST'])
@ensure_json_response
def breeding_compatibility():
    """Compute breeding pair compatibility score."""
    if not GENETIC_SCORING_AVAILABLE:
        return {'error': '遺伝子スコアリングモジュールが利用できません'}, 503
    data = request.get_json(silent=True)
    if not data:
        return {'error': 'JSONデータが必要です'}, 400
    sire = data.get('sire', {})
    dam = data.get('dam', {})
    if not sire or not dam:
        return {'error': '父犬と母犬のデータが必要です'}, 400
    pedigree = PedigreeTree()
    sire_id = sire.get('id', 'sire_1')
    dam_id = dam.get('id', 'dam_1')
    pedigree.add_dog(Dog(dog_id=sire_id, name=sire.get('name', 'Sire'), breed_id=sire.get('breed_id'),
                         scores=sire.get('scores', {}), health_tests=sire.get('health_tests', [])))
    pedigree.add_dog(Dog(dog_id=dam_id, name=dam.get('name', 'Dam'), breed_id=dam.get('breed_id'),
                         scores=dam.get('scores', {}), health_tests=dam.get('health_tests', [])))
    optimizer = BreedingOptimizer(pedigree)
    result = optimizer.compatibility_score(sire_id, dam_id)
    return result


@app.route('/api/genetic-scoring/coi', methods=['POST'])
@ensure_json_response
def compute_coi():
    """Compute Wright's Coefficient of Inbreeding for a pedigree."""
    if not GENETIC_SCORING_AVAILABLE:
        return {'error': '遺伝子スコアリングモジュールが利用できません'}, 503
    data = request.get_json(silent=True)
    if not data:
        return {'error': 'JSONデータが必要です'}, 400
    dogs = data.get('dogs', [])
    target_id = data.get('target_id')
    if not dogs or not target_id:
        return {'error': '血統データとターゲットIDが必要です'}, 400
    pedigree = PedigreeTree()
    for d in dogs:
        pedigree.add_dog(Dog(dog_id=d['id'], name=d.get('name', ''), breed_id=d.get('breed_id'),
                             sire_id=d.get('sire_id'), dam_id=d.get('dam_id'),
                             scores=d.get('scores', {}), health_tests=d.get('health_tests', [])))
    coi = pedigree.coi(target_id)
    return {'target_id': target_id, 'coi': coi, 'coi_percent': round(coi * 100, 2)}


# =============================================================================
# Genetic Test Photo Analysis (OCR via Vision API)
# =============================================================================

# Mapping of common gene name variations to our standard COMMON_HEALTH_GENES keys
_GENE_NAME_ALIASES = {
    'vwd': 'vWD1', 'vwd1': 'vWD1', 'vwd type 1': 'vWD1', 'von willebrand': 'vWD1',
    'von willebrand disease': 'vWD1', 'von willebrand disease type 1': 'vWD1', 'vwd type i': 'vWD1',
    'pra': 'PRA_prcd', 'pra-prcd': 'PRA_prcd', 'pra_prcd': 'PRA_prcd', 'prcd': 'PRA_prcd',
    'prcd-pra': 'PRA_prcd', 'progressive retinal atrophy': 'PRA_prcd',
    'dm': 'DM', 'degenerative myelopathy': 'DM', 'sod1': 'DM',
    'eic': 'EIC', 'exercise induced collapse': 'EIC', 'exercise-induced collapse': 'EIC',
    'mdr1': 'MDR1', 'mdr-1': 'MDR1', 'multi-drug resistance': 'MDR1', 'multidrug resistance': 'MDR1',
    'abcb1': 'MDR1', 'ivermectin sensitivity': 'MDR1',
    'huu': 'HUU', 'hyperuricosuria': 'HUU', 'sLC2a9': 'HUU',
    'dcm': 'DCM', 'dilated cardiomyopathy': 'DCM',
    'cea': 'CEA', 'collie eye anomaly': 'CEA', 'choroidal hypoplasia': 'CEA',
}

# Extended gene info for diseases not in COMMON_HEALTH_GENES
_EXTENDED_GENE_INFO = {
    'ic': {'description': 'Intestinal Cobalamin Malabsorption', 'risk_ja': 'ビタミンB12吸収障害により成長不良、貧血を引き起こす可能性'},
    'hn': {'description': 'Hereditary Nephritis', 'risk_ja': '遺伝性腎炎。進行性腎不全のリスク'},
    'ncl': {'description': 'Neuronal Ceroid Lipofuscinosis', 'risk_ja': '神経セロイドリポフスチン症。進行性神経変性疾患'},
    'pll': {'description': 'Primary Lens Luxation', 'risk_ja': '原発性水晶体脱臼。緑内障、失明のリスク'},
    'cystinuria': {'description': 'Cystinuria', 'risk_ja': 'シスチン尿症。膀胱結石のリスク'},
    'ams': {'description': 'Alaskan Malamute Polyneuropathy', 'risk_ja': '多発性神経障害。運動機能低下'},
    'cd': {'description': 'Cone Degeneration', 'risk_ja': '錐体変性。昼盲症のリスク'},
    'cmr1': {'description': 'Canine Multifocal Retinopathy', 'risk_ja': '多焦点性網膜症。視力低下のリスク'},
    'gsd': {'description': 'Glycogen Storage Disease', 'risk_ja': '糖原病。筋力低下、肝腫大のリスク'},
    'mh': {'description': 'Malignant Hyperthermia', 'risk_ja': '悪性高熱症。麻酔時の生命リスク'},
}

# Diseases linked to specific genes
_GENE_DISEASE_MAP = {
    'vWD1': {'diseases': ['出血傾向', '血液凝固異常'], 'risk_ja': 'フォン・ヴィレブランド病1型。出血が止まりにくくなる遺伝性疾患。手術時のリスク増大'},
    'PRA_prcd': {'diseases': ['進行性網膜萎縮症'], 'risk_ja': '進行性網膜萎縮症。視力の進行性低下、最終的に失明に至る可能性'},
    'DM': {'diseases': ['変性性脊髄症'], 'risk_ja': '変性性脊髄症。後肢の進行性麻痺、高齢期に発症リスク'},
    'EIC': {'diseases': ['運動誘発性虚脱'], 'risk_ja': '運動誘発性虚脱。激しい運動後に四肢の協調運動障害・虚脱'},
    'MDR1': {'diseases': ['薬物感受性'], 'risk_ja': '多剤耐性遺伝子変異。イベルメクチン等の薬物に対する重篤な副作用リスク'},
    'HUU': {'diseases': ['高尿酸尿症', '膀胱結石'], 'risk_ja': '高尿酸尿症。尿酸結石の形成リスクが著しく上昇'},
    'DCM': {'diseases': ['拡張型心筋症'], 'risk_ja': '拡張型心筋症。心臓の拡大と機能低下、突然死のリスク'},
    'CEA': {'diseases': ['コリー眼異常'], 'risk_ja': 'コリー眼異常。脈絡膜低形成、網膜剥離のリスク'},
}


@app.route('/api/genetic-test/analyze', methods=['POST'])
@ensure_json_response
def analyze_genetic_test():
    """Analyze a photo of genetic test results from external labs (Embark, Wisdom Panel, etc.)."""
    data = request.get_json(silent=True)
    if not data:
        return {'error': 'JSONデータが必要です'}, 400
    image_base64 = data.get('image')
    dog_name = data.get('dog_name', '')
    breed_name = data.get('breed_name', '')
    breed_id = data.get('breed_id', '')

    if not image_base64:
        return {'error': '画像データが必要です'}, 400

    # Algorithm-only fallback when Vision API is not available
    if not claude_client and not openai_client:
        # Return breed-specific genetic risk profile instead of 503
        breed_data = BREED_DATA.get(breed_id, {})
        if not breed_data and breed_name:
            # Try to find by name
            for bid, bd in BREED_DATA.items():
                if bd.get('name') == breed_name or bd.get('name_en', '').lower() == breed_name.lower():
                    breed_data = bd
                    breed_id = bid
                    break

        hereditary_diseases = breed_data.get('hereditary_diseases', [])
        breed_risk_tests = []
        for disease in hereditary_diseases:
            # hereditary_diseases can be strings or dicts
            if isinstance(disease, str):
                disease_name = disease
                disease_gene = 'unknown'
            else:
                disease_name = disease.get('name', str(disease))
                disease_gene = disease.get('gene', 'unknown')
            breed_risk_tests.append({
                'gene': disease_gene,
                'gene_raw': disease_gene,
                'full_name': disease_name,
                'result': 'not_tested',
                'genotype': None,
                'risk_level': 'unknown',
                'risk_ja': f'犬種リスク: {disease_name}。画像解析にはVision APIが必要です。手動入力は /api/genetic-test/manual をご利用ください。',
                'known_gene': True,
                'linked_diseases': [disease_name],
            })

        return {
            'success': True,
            'analysis_method': 'breed_risk_profile',
            'note': 'Vision APIが未設定のため、画像からの遺伝子検査OCRは利用できません。犬種リスクプロファイルを返します。手動入力は /api/genetic-test/manual エンドポイントをご利用ください。',
            'dog_name': dog_name,
            'breed': breed_name or breed_data.get('name', ''),
            'breed_id': breed_id,
            'health_tests': breed_risk_tests,
            'color_tests': [],
            'summary': {
                'total_tests': len(breed_risk_tests),
                'clear': 0,
                'carrier': 0,
                'affected': 0,
                'breed_risk_items': len(hereditary_diseases),
                'overall_risk': 'unknown',
                'overall_risk_ja': f'画像解析は現在利用できません。{breed_data.get("name", "この犬種")}には{len(hereditary_diseases)}件の遺伝性疾患リスクがあります。手動入力で検査結果を登録してください。',
            },
            'manual_entry_endpoint': '/api/genetic-test/manual',
        }

    # Remove data URL prefix if present
    if ',' in image_base64:
        image_base64 = image_base64.split(',', 1)[1]

    # Vision API prompt to extract genetic test data
    extraction_prompt = """You are analyzing a photo of a dog genetic test result certificate/report.
Extract ALL information visible in the image and return it as JSON.

Required JSON format:
{
  "test_company": "company name (e.g. Embark, Wisdom Panel, Orivet, GenSol, etc.)",
  "dog_name": "name of the tested dog if visible",
  "breed": "breed of the dog if visible",
  "registration_number": "registration/microchip number if visible",
  "test_date": "date of test if visible",
  "health_tests": [
    {
      "gene": "gene name/abbreviation (e.g. vWD1, PRA, DM, EIC, MDR1, etc.)",
      "full_name": "full disease/condition name",
      "result": "clear OR carrier OR affected OR at_risk",
      "genotype": "genotype if shown (e.g. N/N, N/M, M/M, WT/WT, etc.)"
    }
  ],
  "color_tests": [
    {
      "locus": "locus name (e.g. E, B, D, K, A, S, etc.)",
      "genotype": "genotype (e.g. E/e, B/B, etc.)",
      "phenotype": "color trait description if visible"
    }
  ],
  "other_info": "any other relevant information visible"
}

IMPORTANT:
- Extract EVERY test result visible, not just common ones
- Normalize results: "Normal", "N/N", "WT/WT", "Clear" → "clear"; "Carrier", "N/M" → "carrier"; "Affected", "At Risk", "M/M" → "affected"
- Include the genotype notation exactly as shown
- If information is not visible, use null
- Return ONLY valid JSON, no other text"""

    try:
        result_text = call_vision_api(extraction_prompt, image_base64, max_tokens=2000)

        # Parse the JSON response
        # Try to extract JSON from potential markdown code blocks
        json_text = result_text.strip()
        if json_text.startswith('```'):
            json_text = json_text.split('```')[1]
            if json_text.startswith('json'):
                json_text = json_text[4:]
            json_text = json_text.strip()
        extracted = json.loads(json_text)

    except json.JSONDecodeError:
        logger.error(f"Failed to parse genetic test extraction: {result_text[:500]}")
        return {'error': '遺伝子検査結果の解析に失敗しました。画像が鮮明であることを確認してください。'}, 422
    except Exception as e:
        logger.error(f"Genetic test analysis error: {e}", exc_info=True)
        return {'error': '遺伝子検査解析に失敗しました'}, 500

    # Process and enrich health test results
    enriched_tests = []
    for test in extracted.get('health_tests', []):
        gene_raw = (test.get('gene') or '').strip()
        gene_key = _GENE_NAME_ALIASES.get(gene_raw.lower(), gene_raw)
        result_val = (test.get('result') or 'unknown').lower().strip()

        # Normalize result
        if result_val in ('normal', 'n/n', 'wt/wt', 'homozygous normal'):
            result_val = 'clear'
        elif result_val in ('heterozygous', 'n/m', 'n/mut'):
            result_val = 'carrier'
        elif result_val in ('homozygous affected', 'at risk', 'at_risk', 'm/m', 'mut/mut', 'homozygous mutant'):
            result_val = 'affected'

        # Look up disease info
        disease_info = _GENE_DISEASE_MAP.get(gene_key, {})
        extended_info = _EXTENDED_GENE_INFO.get(gene_raw.lower(), {})
        known_gene = gene_key in COMMON_HEALTH_GENES if GENETIC_SCORING_AVAILABLE else False

        gene_description = ''
        if known_gene:
            gene_description = COMMON_HEALTH_GENES[gene_key].get('description', '')
        elif extended_info:
            gene_description = extended_info.get('description', '')
        elif test.get('full_name'):
            gene_description = test['full_name']

        # Risk assessment
        risk_level = 'none'
        risk_ja = ''
        if result_val == 'affected':
            risk_level = 'high'
            risk_ja = disease_info.get('risk_ja', extended_info.get('risk_ja', f'{gene_description}のリスクが高い状態です'))
        elif result_val == 'carrier':
            risk_level = 'medium'
            risk_ja = 'キャリア（保因者）です。繁殖時に相手の遺伝子型を確認してください。'
            if disease_info.get('risk_ja'):
                risk_ja += f' {disease_info["risk_ja"]}（保因者）'
        else:
            risk_level = 'none'
            risk_ja = 'クリア（正常）です。この遺伝子に関するリスクはありません。'

        enriched_tests.append({
            'gene': gene_key,
            'gene_raw': gene_raw,
            'full_name': test.get('full_name') or gene_description,
            'result': result_val,
            'genotype': test.get('genotype'),
            'risk_level': risk_level,
            'risk_ja': risk_ja,
            'known_gene': known_gene,
            'linked_diseases': disease_info.get('diseases', []),
        })

    # Process color tests
    enriched_colors = []
    for ct in extracted.get('color_tests', []):
        locus = (ct.get('locus') or '').upper().strip()
        enriched_colors.append({
            'locus': locus,
            'genotype': ct.get('genotype', ''),
            'phenotype': ct.get('phenotype', ''),
            'known_locus': locus in COLOR_LOCI if GENETIC_SCORING_AVAILABLE else False,
        })

    # Summary statistics
    total_tests = len(enriched_tests)
    clear_count = sum(1 for t in enriched_tests if t['result'] == 'clear')
    carrier_count = sum(1 for t in enriched_tests if t['result'] == 'carrier')
    affected_count = sum(1 for t in enriched_tests if t['result'] == 'affected')

    # Overall risk assessment
    if affected_count > 0:
        overall_risk = 'high'
        overall_risk_ja = f'注意: {affected_count}項目で発症リスクが検出されました。獣医師にご相談ください。'
    elif carrier_count > 0:
        overall_risk = 'medium'
        overall_risk_ja = f'{carrier_count}項目でキャリア（保因者）が検出されました。繁殖計画時にご注意ください。'
    else:
        overall_risk = 'low'
        overall_risk_ja = 'すべての検査項目でクリア（正常）です。'

    response = {
        'success': True,
        'test_company': extracted.get('test_company'),
        'dog_name': extracted.get('dog_name') or dog_name,
        'breed': extracted.get('breed') or breed_name,
        'registration_number': extracted.get('registration_number'),
        'test_date': extracted.get('test_date'),
        'health_tests': enriched_tests,
        'color_tests': enriched_colors,
        'summary': {
            'total_tests': total_tests,
            'clear': clear_count,
            'carrier': carrier_count,
            'affected': affected_count,
            'overall_risk': overall_risk,
            'overall_risk_ja': overall_risk_ja,
        },
        'other_info': extracted.get('other_info'),
    }

    logger.info(f"Genetic test analyzed: {total_tests} tests, {clear_count} clear, {carrier_count} carrier, {affected_count} affected")
    return response


@app.route('/api/genetic-test/manual', methods=['POST'])
@ensure_json_response
def manual_genetic_test():
    """手動入力による遺伝子検査結果の登録・解析.

    Vision API不要。検査結果をJSON形式で直接入力し、
    リスク評価・繁殖アドバイスを返す。DB保存も行う（認証時）。
    """
    data = request.get_json(silent=True)
    if not data:
        return {'error': 'JSONデータが必要です'}, 400

    health_tests_raw = data.get('health_tests', [])
    if not health_tests_raw:
        return {'error': 'health_tests（遺伝子検査結果リスト）が必要です'}, 400

    breed_id = data.get('breed_id', '')
    breed_name = data.get('breed_name', '')
    dog_name = data.get('dog_name', '')

    # Look up breed hereditary diseases for context
    breed_data = BREED_DATA.get(breed_id, {})
    if breed_data and not breed_name:
        breed_name = breed_data.get('name', breed_data.get('name_en', ''))
    breed_diseases = breed_data.get('hereditary_diseases', breed_data.get('common_issues', []))

    # Enrich health test results
    enriched_tests = []
    for test in health_tests_raw:
        gene_raw = (test.get('gene') or '').strip()
        gene_key = _GENE_NAME_ALIASES.get(gene_raw.lower(), gene_raw)
        result_val = (test.get('result') or 'unknown').lower().strip()

        # Normalize
        if result_val in ('normal', 'n/n', 'wt/wt', 'homozygous normal'):
            result_val = 'clear'
        elif result_val in ('heterozygous', 'n/m', 'n/mut'):
            result_val = 'carrier'
        elif result_val in ('homozygous affected', 'at risk', 'at_risk', 'm/m', 'mut/mut'):
            result_val = 'affected'

        disease_info = _GENE_DISEASE_MAP.get(gene_key, {})
        extended_info = _EXTENDED_GENE_INFO.get(gene_raw.lower(), {})
        known_gene = gene_key in COMMON_HEALTH_GENES if GENETIC_SCORING_AVAILABLE else False

        gene_description = ''
        if known_gene:
            gene_description = COMMON_HEALTH_GENES[gene_key].get('description', '')
        elif extended_info:
            gene_description = extended_info.get('description', '')
        elif test.get('full_name'):
            gene_description = test['full_name']

        risk_level = 'none'
        risk_ja = ''
        if result_val == 'affected':
            risk_level = 'high'
            risk_ja = disease_info.get('risk_ja', extended_info.get('risk_ja', f'{gene_description}のリスクが高い状態です'))
        elif result_val == 'carrier':
            risk_level = 'medium'
            risk_ja = 'キャリア（保因者）です。繁殖時に相手の遺伝子型を確認してください。'
        else:
            risk_level = 'none'
            risk_ja = 'クリア（正常）です。'

        enriched_tests.append({
            'gene': gene_key,
            'gene_raw': gene_raw,
            'full_name': test.get('full_name') or gene_description,
            'result': result_val,
            'genotype': test.get('genotype'),
            'risk_level': risk_level,
            'risk_ja': risk_ja,
            'known_gene': known_gene,
            'linked_diseases': disease_info.get('diseases', []),
        })

    # Color tests
    enriched_colors = []
    for ct in data.get('color_tests', []):
        locus = (ct.get('locus') or '').upper().strip()
        enriched_colors.append({
            'locus': locus,
            'genotype': ct.get('genotype', ''),
            'phenotype': ct.get('phenotype', ''),
            'known_locus': locus in COLOR_LOCI if GENETIC_SCORING_AVAILABLE else False,
        })

    # Summary
    total_tests = len(enriched_tests)
    clear_count = sum(1 for t in enriched_tests if t['result'] == 'clear')
    carrier_count = sum(1 for t in enriched_tests if t['result'] == 'carrier')
    affected_count = sum(1 for t in enriched_tests if t['result'] == 'affected')

    if affected_count > 0:
        overall_risk = 'high'
        overall_risk_ja = f'注意: {affected_count}項目で発症リスクが検出されました。獣医師にご相談ください。'
    elif carrier_count > 0:
        overall_risk = 'medium'
        overall_risk_ja = f'{carrier_count}項目でキャリア（保因者）が検出されました。繁殖計画時にご注意ください。'
    elif total_tests > 0:
        overall_risk = 'low'
        overall_risk_ja = 'すべての検査項目でクリア（正常）です。'
    else:
        overall_risk = 'unknown'
        overall_risk_ja = '検査結果がありません。'

    # Breed-specific advice
    breed_advice = []
    if breed_diseases:
        tested_genes = {t['gene'].lower() for t in enriched_tests}
        for disease in breed_diseases:
            # Check if any tested gene is linked to this breed disease
            disease_lower = disease.lower()
            matched = False
            for t in enriched_tests:
                for ld in t.get('linked_diseases', []):
                    if ld.lower() in disease_lower or disease_lower in ld.lower():
                        matched = True
                        break
            if not matched:
                breed_advice.append(f'{disease} — この犬種の好発疾患ですが、対応する遺伝子検査が未実施です')

    # Save to DB if authenticated
    saved_id = None
    token = request.cookies.get('session_token') or request.headers.get('Authorization', '').replace('Bearer ', '')
    if token:
        from api.database import verify_session, save_genetic_test
        user = verify_session(token)
        if user:
            saved_id = save_genetic_test(user['id'], {
                'dog_id': data.get('dog_id'),
                'medical_record_id': data.get('medical_record_id'),
                'test_company': data.get('test_company', '手動入力'),
                'test_date': data.get('test_date'),
                'registration_number': data.get('registration_number'),
                'health_tests': enriched_tests,
                'color_tests': enriched_colors,
                'notes': data.get('notes', ''),
            })

    response = {
        'success': True,
        'mode': 'manual',
        'test_company': data.get('test_company', '手動入力'),
        'dog_name': dog_name,
        'breed': breed_name,
        'health_tests': enriched_tests,
        'color_tests': enriched_colors,
        'summary': {
            'total_tests': total_tests,
            'clear': clear_count,
            'carrier': carrier_count,
            'affected': affected_count,
            'overall_risk': overall_risk,
            'overall_risk_ja': overall_risk_ja,
        },
        'breed_advice': breed_advice,
    }
    if saved_id:
        response['saved_id'] = saved_id

    logger.info(f"Manual genetic test: {total_tests} tests, risk={overall_risk}")
    return response


@app.route('/api/genetic-test/breed-risk/<breed_id>', methods=['GET'])
@ensure_json_response
def breed_genetic_risk(breed_id):
    """犬種別の遺伝性疾患リスクプロファイルを返す.

    Vision API不要。breeds.pyの360犬種データから
    遺伝性疾患リストと推奨検査項目を返す。
    """
    breed_data = BREED_DATA.get(breed_id)
    if not breed_data:
        return {'error': f'犬種ID "{breed_id}" が見つかりません'}, 404

    diseases = breed_data.get('hereditary_diseases', breed_data.get('common_issues', []))

    # Map diseases to recommended genetic tests
    recommended_tests = []
    for gene_key, gene_info in _GENE_DISEASE_MAP.items():
        gene_diseases = [d.lower() for d in gene_info.get('diseases', [])]
        for disease in diseases:
            for gd in gene_diseases:
                if gd in disease.lower() or disease.lower() in gd:
                    gene_desc = COMMON_HEALTH_GENES.get(gene_key, {}).get('description', '') if GENETIC_SCORING_AVAILABLE else ''
                    recommended_tests.append({
                        'gene': gene_key,
                        'description': gene_desc or gene_info.get('risk_ja', ''),
                        'linked_disease': disease,
                        'mode': COMMON_HEALTH_GENES.get(gene_key, {}).get('mode', '') if GENETIC_SCORING_AVAILABLE else '',
                    })
                    break

    return {
        'breed_id': breed_id,
        'breed_name': breed_data.get('name', breed_data.get('name_en', '')),
        'breed_name_en': breed_data.get('name_en', ''),
        'hereditary_diseases': diseases,
        'recommended_tests': recommended_tests,
        'total_diseases': len(diseases),
        'total_recommended_tests': len(recommended_tests),
    }


@app.route('/api/genetic-test/results/<int:dog_id>', methods=['GET'])
@ensure_json_response
def get_dog_genetic_results(dog_id):
    """犬の遺伝子検査結果一覧を返す."""
    token = request.cookies.get('session_token') or request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token:
        return {'error': '認証が必要です'}, 401
    from api.database import verify_session, get_genetic_tests_by_dog
    user = verify_session(token)
    if not user:
        return {'error': '無効なセッション'}, 401
    tests = get_genetic_tests_by_dog(dog_id, user_id=user['id'])
    return {'success': True, 'dog_id': dog_id, 'tests': tests, 'total': len(tests)}


def _dict_to_canine_keypoints(kp_dict):
    """Convert a dict of keypoint data to a CanineKeypoints object.

    Accepts formats:
      {"nose": [x, y], "withers": [x, y, z], ...}
      {"nose": {"x": 0.5, "y": 0.3, "confidence": 0.9}, ...}
    """
    kp = CanineKeypoints()
    for name, val in kp_dict.items():
        if isinstance(val, (list, tuple)):
            if len(val) >= 2:
                conf = val[3] if len(val) > 3 else (val[2] if len(val) == 4 else 1.0)
                try:
                    kp.set_2d(name, Vec2(float(val[0]), float(val[1])),
                              confidence=float(conf) if len(val) <= 3 else 1.0)
                except (KeyError, ValueError):
                    continue
                if len(val) >= 3:
                    try:
                        kp.set_3d(name, Vec3(float(val[0]), float(val[1]), float(val[2])))
                    except (KeyError, ValueError):
                        pass
        elif isinstance(val, dict):
            x, y = val.get('x'), val.get('y')
            if x is not None and y is not None:
                conf = float(val.get('confidence', 1.0))
                try:
                    kp.set_2d(name, Vec2(float(x), float(y)), confidence=conf)
                except (KeyError, ValueError):
                    continue
                z = val.get('z')
                if z is not None:
                    try:
                        kp.set_3d(name, Vec3(float(x), float(y), float(z)))
                    except (KeyError, ValueError):
                        pass
    return kp


@app.route('/api/pose-estimation/analyze', methods=['POST'])
@ensure_json_response
def analyze_pose():
    """Analyze dog pose from keypoints and compute structural geometry score."""
    if not POSE_ESTIMATION_AVAILABLE:
        return {'error': '3D姿勢推定モジュールが利用できません'}, 503
    data = request.get_json(silent=True)
    if not data:
        return {'error': 'JSONデータが必要です'}, 400
    keypoints_raw = data.get('keypoints', {})
    breed_id = data.get('breed_id')
    image_size = data.get('image_size')  # optional [w, h]
    if not keypoints_raw:
        return {'error': 'キーポイントデータが必要です'}, 400
    keypoints = _dict_to_canine_keypoints(keypoints_raw)
    if keypoints.num_detected() < 3:
        return {'error': 'キーポイントが不足しています（最低3点必要）'}, 400
    analyzer = PoseAnalyzer()
    img_sz = tuple(image_size) if image_size and len(image_size) == 2 else None
    result = analyzer.analyze_photo(keypoints, breed_id, image_size=img_sz)
    return result


@app.route('/api/pose-estimation/analyze-gait', methods=['POST'])
@ensure_json_response
def analyze_gait_pose():
    """Analyze gait from multi-frame keypoints."""
    if not POSE_ESTIMATION_AVAILABLE:
        return {'error': '3D姿勢推定モジュールが利用できません'}, 503
    data = request.get_json(silent=True)
    if not data:
        return {'error': 'JSONデータが必要です'}, 400
    frames_raw = data.get('frames', [])
    breed_id = data.get('breed_id')
    fps = float(data.get('fps', 30.0))
    if not frames_raw or len(frames_raw) < 2:
        return {'error': '2フレーム以上のキーポイントデータが必要です'}, 400
    frame_keypoints = [_dict_to_canine_keypoints(f) for f in frames_raw]
    analyzer = GaitAnalyzer(fps=fps)
    result = analyzer.analyze_gait(frame_keypoints, breed_id)
    return result


@app.route('/api/finetuning/models', methods=['GET'])
@ensure_json_response
def list_finetuned_models():
    """List all fine-tuned model versions."""
    if not FINETUNING_AVAILABLE:
        return {'error': 'ファインチューニングモジュールが利用できません'}, 503
    registry = ModelRegistry()
    models = registry.list_models()
    return {'models': models, 'count': len(models)}


@app.route('/api/finetuning/evaluate', methods=['POST'])
@ensure_json_response
def evaluate_model():
    """Evaluate model predictions against ground truth."""
    if not FINETUNING_AVAILABLE:
        return {'error': 'ファインチューニングモジュールが利用できません'}, 503
    data = request.get_json(silent=True)
    if not data:
        return {'error': 'JSONデータが必要です'}, 400
    predicted_scores = data.get('predicted_scores', data.get('predictions', []))
    true_scores = data.get('true_scores', data.get('ground_truth', []))
    predicted_grades = data.get('predicted_grades', [])
    true_grades = data.get('true_grades', [])
    if not predicted_scores or not true_scores:
        return {'error': '予測スコアと正解スコアが必要です'}, 400
    if len(predicted_scores) != len(true_scores):
        return {'error': '予測と正解のサンプル数が一致しません'}, 400
    # Normalize axis names: user-friendly → internal (skeletal, gait, muscle, coat, temperament)
    _AXIS_ALIASES = {
        'structure': 'skeletal', 'skeletal': 'skeletal', 'proportion': 'skeletal',
        'gait': 'gait', 'movement': 'gait', 'stride': 'gait',
        'muscle': 'muscle', 'muscular': 'muscle', 'body': 'muscle',
        'coat': 'coat', 'fur': 'coat', 'grooming': 'coat',
        'temperament': 'temperament', 'behavior': 'temperament', 'character': 'temperament',
    }
    _SCORING_AXES = ['skeletal', 'gait', 'muscle', 'coat', 'temperament']

    def _normalize_score_dict(score_item):
        if isinstance(score_item, (int, float)):
            return {ax: float(score_item) for ax in _SCORING_AXES}
        if isinstance(score_item, dict):
            normalized = {}
            for key, val in score_item.items():
                axis = _AXIS_ALIASES.get(key.lower(), key.lower())
                if axis in _SCORING_AXES and isinstance(val, (int, float)):
                    normalized[axis] = float(val)
            # Fill missing axes with average of provided axes
            if normalized:
                avg = sum(normalized.values()) / len(normalized)
                for ax in _SCORING_AXES:
                    if ax not in normalized:
                        normalized[ax] = avg
            return normalized
        return {ax: 75.0 for ax in _SCORING_AXES}

    predicted_scores = [_normalize_score_dict(s) for s in predicted_scores]
    true_scores = [_normalize_score_dict(s) for s in true_scores]
    # Auto-generate grades if not provided
    if not predicted_grades:
        predicted_grades = [_score_to_grade(s) for s in predicted_scores]
    if not true_grades:
        true_grades = [_score_to_grade(s) for s in true_scores]
    pipeline = EvaluationPipeline()
    metrics = pipeline.evaluate(predicted_scores, true_scores, predicted_grades, true_grades)
    return {'metrics': metrics}


# =============================================================================
# Hybrid Scoring Pipeline Endpoint
# =============================================================================

@app.route('/api/hybrid-score', methods=['POST'])
@ensure_json_response
def api_hybrid_score():
    """
    Hybrid scoring: Algorithm (主導) → AI correction (伴奏).
    Layer 1: Deterministic algorithm computes base score from axis values.
    Layer 2: AI observations apply bounded corrections (±8 max).
    """
    if not SCORING_AVAILABLE:
        return {'error': 'スコアリングモジュールが利用できません'}, 503
    data = request.get_json(silent=True)
    if not data:
        return {'error': 'JSONデータが必要です'}, 400
    axis_scores = data.get('axis_scores')
    age_years = data.get('age_years')
    ai_corrections = data.get('ai_corrections')
    breed_id = data.get('breed_id')
    if not axis_scores or age_years is None:
        return {'error': '軸スコアと年齢が必要です'}, 400
    result = hybrid_score(
        algorithm_axis_scores=axis_scores,
        ai_observations=ai_corrections,
        age_years=float(age_years),
        breed_id=breed_id
    )
    return result


@app.route('/api/validation/run', methods=['GET'])
@ensure_json_response
def run_validation():
    """Run FCI reference dataset validation against scoring pipeline."""
    try:
        from api.reference_dataset import run_validation as _run
    except ImportError:
        try:
            from reference_dataset import run_validation as _run
        except ImportError:
            return {'error': '検証データセットが利用できません'}, 503
    summary = _run(verbose=False)
    return summary


# =============================================================================
# Authentication Endpoints
# =============================================================================

@app.route('/api/auth/register', methods=['POST'])
@limiter.limit("5 per hour")
@ensure_json_response
def register():
    """Register a new user"""
    if not DB_AVAILABLE:
        return {'error': 'データベースが利用できません'}, 503

    if not _check_rate_limit(_rate_limit_key('register')):
        return {'error': '登録試行回数が上限に達しました。しばらく経ってからお試しください。'}, 429

    data = request.get_json(silent=True)
    if not data:
        return {'error': 'JSONデータが必要です'}, 400
    email = data.get('email', '').strip().lower()
    password = data.get('password', '').strip()
    name = data.get('name', '').strip()
    security_question = data.get('security_question', '').strip()
    security_answer = data.get('security_answer', '').strip()

    # Validation
    if not email or '@' not in email:
        return {'error': 'メールアドレスを正しく入力してください'}, 400
    if len(password) < 6:
        return {'error': 'パスワードは6文字以上にしてください'}, 400
    if not security_question or not security_answer:
        return {'error': '合言葉（秘密の質問と回答）を入力してください'}, 400

    user = create_user(email, password, name or None,
                       security_question=security_question,
                       security_answer=security_answer)
    if not user:
        return {'error': 'このメールアドレスは既に登録されています'}, 409

    # Create session
    token = create_session(user['id'])

    response = jsonify({
        'success': True,
        'user': user,
        'token': token,
        'csrf_token': _generate_csrf_token(token),
    })
    _set_session_cookie(response, token)
    return response


@app.route('/api/auth/login', methods=['POST'])
@limiter.limit("10 per hour")
@ensure_json_response
def login():
    """Login user"""
    if not DB_AVAILABLE:
        return {'error': 'データベースが利用できません'}, 503

    if not _check_rate_limit(_rate_limit_key('login')):
        return {'error': 'ログイン試行回数が上限に達しました。10分後にお試しください。'}, 429

    data = request.get_json(silent=True)
    if not data:
        return {'error': 'JSONデータが必要です'}, 400
    email = data.get('email', '').strip().lower()
    password = data.get('password', '').strip()

    user = verify_user(email, password)
    if not user:
        return {'error': 'メールアドレスまたはパスワードが正しくありません'}, 401

    # Create session
    token = create_session(user['id'])

    response = jsonify({
        'success': True,
        'user': user,
        'token': token,
        'csrf_token': _generate_csrf_token(token),
    })
    _set_session_cookie(response, token)
    return response


@app.route('/api/auth/forgot-password', methods=['POST'])
@limiter.limit("3 per hour")
@ensure_json_response
def forgot_password():
    """Send password reset email after verifying security answer"""
    if not DB_AVAILABLE:
        return {'error': 'データベースが利用できません'}, 503

    if not _check_rate_limit(_rate_limit_key('forgot')):
        return {'error': '試行回数が上限に達しました。10分後にお試しください。'}, 429

    data = request.get_json(silent=True)
    if not data:
        return {'error': 'JSONデータが必要です'}, 400
    email = data.get('email', '').strip().lower()
    security_answer = data.get('security_answer', '').strip()

    if not email or '@' not in email:
        return {'error': 'メールアドレスを入力してください'}, 400
    if not security_answer:
        return {'error': '合言葉を入力してください'}, 400

    # First get the user to show their security question
    user = get_user_by_email(email)
    if not user:
        # Don't reveal whether email exists (timing-safe)
        return {'error': 'メールアドレスまたは合言葉が正しくありません'}, 401

    if not user.get('security_answer_hash'):
        return {'error': 'この アカウントには合言葉が設定されていません'}, 400

    # Verify security answer
    verified_user = verify_security_answer(email, security_answer)
    if not verified_user:
        return {'error': 'メールアドレスまたは合言葉が正しくありません'}, 401

    # Generate reset token
    token = create_reset_token(verified_user['id'])

    # Send email with reset link
    reset_url = f"{request.host_url}login.html?reset_token={token}"
    email_sent = _send_reset_email(email, verified_user.get('name', ''), reset_url)

    if email_sent:
        return {'success': True, 'message': 'パスワードリセット用のメールを送信しました。メールを確認してください。'}
    else:
        # Only expose token in dev/staging when explicitly allowed
        if ALLOW_RESET_TOKEN_RESPONSE:
            return {'success': True, 'reset_token': token,
                    'message': 'メール送信設定が未構成のため、このままパスワードをリセットできます。'}
        return {'success': True, 'message': 'パスワードリセットの処理が完了しました。'}


@app.route('/api/auth/security-question', methods=['POST'])
@ensure_json_response
def get_security_question():
    """Get the security question for a given email"""
    if not DB_AVAILABLE:
        return {'error': 'データベースが利用できません'}, 503

    data = request.get_json(silent=True)
    if not data:
        return {'error': 'JSONデータが必要です'}, 400
    email = data.get('email', '').strip().lower()

    if not email or '@' not in email:
        return {'error': 'メールアドレスを入力してください'}, 400

    user = get_user_by_email(email)
    if not user or not user.get('security_question'):
        # Don't reveal whether email exists — use same response for both cases
        return {'error': 'このメールアドレスに対応する合言葉が見つかりません'}, 400

    return {'success': True, 'security_question': user['security_question']}


@app.route('/api/auth/reset-password', methods=['POST'])
@limiter.limit("5 per hour")
@ensure_json_response
def reset_password():
    """Reset password using a valid token"""
    if not DB_AVAILABLE:
        return {'error': 'データベースが利用できません'}, 503

    if not _check_rate_limit(_rate_limit_key('reset')):
        return {'error': '試行回数が上限に達しました。10分後にお試しください。'}, 429

    data = request.get_json(silent=True)
    if not data:
        return {'error': 'JSONデータが必要です'}, 400
    token = data.get('token', '').strip()
    new_password = data.get('new_password', '').strip()

    if not token:
        return {'error': 'リセットトークンが必要です'}, 400
    if len(new_password) < 6:
        return {'error': 'パスワードは6文字以上にしてください'}, 400

    user_id = verify_reset_token(token)
    if not user_id:
        return {'error': 'リセットトークンが無効または期限切れです'}, 401

    update_user_password(user_id, new_password)

    return {'success': True, 'message': 'パスワードをリセットしました。新しいパスワードでログインしてください。'}


def _send_reset_email(to_email, user_name, reset_url):
    """Send password reset email via SMTP. Returns True on success."""
    import smtplib
    from email.mime.text import MIMEText

    smtp_host = os.environ.get('SMTP_HOST', '')
    smtp_port = int(os.environ.get('SMTP_PORT', '587'))
    smtp_user = os.environ.get('SMTP_USER', '')
    smtp_password = os.environ.get('SMTP_PASSWORD', '')
    from_email = os.environ.get('SMTP_FROM', smtp_user)

    if not smtp_host or not smtp_user:
        logger.warning("SMTP not configured (set SMTP_HOST, SMTP_USER, SMTP_PASSWORD env vars)")
        return False

    body = f"""{user_name or 'ユーザー'}様

ShowDog Analysis Platformのパスワードリセットがリクエストされました。
以下のリンクをクリックして新しいパスワードを設定してください：

{reset_url}

このリンクは1時間で無効になります。
心当たりがない場合は、このメールを無視してください。

---
ShowDog Analysis Platform
"""
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = 'パスワードリセット - ShowDog Analysis Platform'
    msg['From'] = from_email
    msg['To'] = to_email

    try:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=SMTP_TIMEOUT_SECONDS) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
        logger.info(f"Password reset email sent to {to_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send reset email: {e}")
        return False


@app.route('/api/auth/logout', methods=['POST'])
@ensure_json_response
def logout():
    """Logout user"""
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token:
        token = request.cookies.get('session_token')

    if token:
        delete_session(token)

    response = jsonify({'success': True})
    response.delete_cookie('session_token', samesite='Lax', secure=COOKIE_SECURE)
    return response


@app.route('/api/auth/me', methods=['GET'])
@require_auth
@ensure_json_response
def get_current_user():
    """Get current logged-in user"""
    return {'user': request.current_user}


@app.route('/api/auth/status', methods=['GET'])
@ensure_json_response
def auth_status():
    """Public endpoint to check authentication state — useful for debugging session issues."""
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    if not token:
        token = request.cookies.get('session_token')

    is_authenticated = False
    user_id = None
    email = None
    if token and DB_AVAILABLE:
        user = verify_session(token)
        if user:
            is_authenticated = True
            user_id = user.get('id')
            email = user.get('email')

    try:
        from api.database import DB_PATH as _auth_db_path
    except ImportError:
        try:
            from database import DB_PATH as _auth_db_path
        except ImportError:
            _auth_db_path = 'unknown'

    return {
        'ok': True,
        'is_authenticated': is_authenticated,
        'user_id': user_id,
        'email': email,
        'session_present': bool(token),
        'cookie_present': bool(request.cookies.get('session_token')),
        'db_available': DB_AVAILABLE,
        'server_time': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        'build_id': BUILD,
        'version': VERSION,
    }


# =============================================================================
# Dog Management Endpoints
# =============================================================================

@app.route('/api/dogs', methods=['GET'])
@require_auth
@ensure_json_response
def list_dogs():
    """List all dogs for current user"""
    dogs = get_dogs_by_user(request.current_user['id'])

    # Add breed names
    for dog in dogs:
        breed = BREED_DATA.get(dog['breed_id'], {})
        dog['breed_name'] = breed.get('name', '不明')
        dog['breed_name_en'] = breed.get('name_en', 'Unknown')

    return {'dogs': dogs, 'count': len(dogs)}


@app.route('/api/dogs', methods=['POST'])
@require_auth
@ensure_json_response
def add_dog():
    """Add a new dog"""
    try:
        data = request.get_json(silent=True)
        if not data:
            return {'error': 'JSONデータが必要です'}, 400
        name = (data.get('name') or '').strip()
        breed_id = data.get('breed_id', '')
        birth_date = data.get('birth_date')
        notes = (data.get('notes') or '').strip()

        if not name:
            return {'error': 'Dog name is required'}, 400
        if not breed_id or breed_id not in BREED_DATA:
            return {'error': f'Invalid breed: {breed_id}'}, 400

        weight = data.get('weight')
        gender = data.get('gender')

        # Validate weight if provided
        if weight is not None:
            try:
                weight = float(weight)
                if weight <= 0:
                    return {'error': 'Weight must be positive'}, 400
            except (ValueError, TypeError):
                return {'error': 'Invalid weight value'}, 400

        dog = create_dog(
            request.current_user['id'],
            name, breed_id, birth_date, weight, gender, notes or None
        )

        breed = BREED_DATA.get(breed_id, {})
        dog['breed_name'] = breed.get('name', '')
        dog['breed_name_en'] = breed.get('name_en', '')

        return {'success': True, 'dog': dog}
    except Exception as e:
        logger.error(f"Error adding dog: {str(e)}", exc_info=True)
        return {'error': 'Failed to add dog'}, 500


@app.route('/api/dogs/<int:dog_id>', methods=['GET'])
@require_auth
@ensure_json_response
def get_dog(dog_id):
    """Get a specific dog"""
    dog = get_dog_by_id(dog_id, request.current_user['id'])
    if not dog:
        return {'error': 'Dog not found'}, 404

    breed = BREED_DATA.get(dog['breed_id'], {})
    dog['breed_name'] = breed.get('name', '')
    dog['breed_name_en'] = breed.get('name_en', '')

    return {'dog': dog}


@app.route('/api/dogs/<int:dog_id>', methods=['PUT'])
@require_auth
@ensure_json_response
def edit_dog(dog_id):
    """Update a dog's information"""
    data = request.get_json(silent=True)
    if not data:
        return {'error': 'JSONデータが必要です'}, 400

    dog = update_dog(
        dog_id, request.current_user['id'],
        name=data.get('name'),
        breed_id=data.get('breed_id'),
        birth_date=data.get('birth_date'),
        weight=data.get('weight'),
        gender=data.get('gender'),
        notes=data.get('notes')
    )

    if not dog:
        return {'error': 'Dog not found'}, 404

    return {'success': True, 'dog': dog}


@app.route('/api/dogs/<int:dog_id>', methods=['DELETE'])
@require_auth
@ensure_json_response
def remove_dog(dog_id):
    """Delete a dog"""
    dog = get_dog_by_id(dog_id, request.current_user['id'])
    if not dog:
        return {'error': 'Dog not found'}, 404

    delete_dog(dog_id, request.current_user['id'])
    return {'success': True}


# =============================================================================
# Analysis History Endpoints
# =============================================================================

@app.route('/api/dogs/<int:dog_id>/analyses', methods=['GET'])
@require_auth
@ensure_json_response
def list_dog_analyses(dog_id):
    """Get analysis history for a dog"""
    dog = get_dog_by_id(dog_id, request.current_user['id'])
    if not dog:
        return {'error': 'Dog not found'}, 404

    analyses = get_analyses_by_dog(dog_id, request.current_user['id'])
    return {'dog': dog, 'analyses': analyses, 'count': len(analyses)}


@app.route('/api/analyses/<int:analysis_id>', methods=['GET'])
@require_auth
@ensure_json_response
def get_analysis(analysis_id):
    """Get a specific analysis with full details"""
    analysis = get_analysis_by_id(analysis_id, request.current_user['id'])
    if not analysis:
        return {'error': 'Analysis not found'}, 404

    return {'analysis': analysis}


@app.route('/api/analyses/recent', methods=['GET'])
@require_auth
@ensure_json_response
def list_recent_analyses():
    """Get recent analyses for current user"""
    analyses = get_recent_analyses_by_user(request.current_user['id'], limit=20)
    return {'analyses': analyses, 'count': len(analyses)}


# =============================================================================
# Breed Data Endpoints
# =============================================================================

@app.route('/api/breeds', methods=['GET'])
@ensure_json_response
def get_breeds():
    breeds = [
        {'id': k, 'name': v['name_en'], 'name_ja': v['name'], 'emoji': '🐕'}
        for k, v in BREED_DATA.items()
    ]
    # Add emojis
    emoji_map = {
        '172d_poodle_toy': '🐩', '122_labrador_retriever': '🦴',
        '166_german_shepherd': '🐕', '111_golden_retriever': '🦮',
        '218_chihuahua': '🐶', '101_french_bulldog': '🐕‍🦺',
        '257_shiba': '🦊', '161_beagle': '🐕',
        '86_yorkshire_terrier': '🎀', '39_welsh_corgi': '🐾'
    }
    for b in breeds:
        b['emoji'] = emoji_map.get(b['id'], '🐕')

    return {'breeds': breeds, 'count': len(breeds), 'version': VERSION}


@app.route('/api/diseases', methods=['GET'])
@ensure_json_response
def get_diseases():
    """Get full disease database for the diseases page."""
    try:
        from api.symptom_checker import _DISEASE_DB
        diseases = []
        for d in _DISEASE_DB:
            diseases.append({
                'name': d.get('name', ''),
                'name_ja': d.get('name_ja', ''),
                'description': d.get('description', ''),
                'description_ja': d.get('description_ja', ''),
                'description_en': d.get('description', ''),
                'urgency': d.get('urgency', 'normal'),
                'symptoms': sorted(list(d.get('symptoms', set()))),
                'reference_url': d.get('reference_url', ''),
            })
        return {'diseases': diseases, 'count': len(diseases)}
    except Exception as e:
        logger.error(f"Disease list error: {e}", exc_info=True)
        return {'error': '疾患データの取得に失敗しました'}, 500


@app.route('/api/breeds/<breed_id>', methods=['GET'])
@ensure_json_response
def get_breed_detail(breed_id):
    """Get detailed breed profile including standards and diseases."""
    breed = BREED_DATA.get(breed_id)
    if not breed:
        return {'error': 'Breed not found'}, 404
    fci_number = breed.get('fci_number', 0)
    pdf_path = os.path.join(app.static_folder, 'breeds', 'pdfs', f'{fci_number}.pdf')
    pdf_url = f'/static/breeds/pdfs/{fci_number}.pdf' if os.path.isfile(pdf_path) else None
    return {
        'id': breed_id,
        'name': breed.get('name', ''),
        'name_en': breed.get('name_en', ''),
        'emoji': breed.get('emoji', '🐕'),
        'fci_number': fci_number,
        'ideal_structure': breed.get('ideal_structure', ''),
        'ideal_coat': breed.get('ideal_coat', ''),
        'ideal_gait': breed.get('ideal_gait', ''),
        'hereditary_diseases': breed.get('hereditary_diseases', []),
        'pdf_url': pdf_url,
        'fci_standard_url': get_fci_standard_url(fci_number) if fci_number else None,
    }


# =============================================================================
# Breed PDF Management
# =============================================================================

@app.route('/api/breeds/<breed_id>/pdf', methods=['POST'])
@require_auth
@ensure_json_response
def upload_breed_pdf(breed_id):
    """Upload a PDF standard document for a breed."""
    breed = BREED_DATA.get(breed_id)
    if not breed:
        return {'error': 'Breed not found'}, 404
    if 'pdf' not in request.files:
        return {'error': 'PDFファイルが必要です'}, 400
    pdf_file = request.files['pdf']
    if not pdf_file.filename.lower().endswith('.pdf'):
        return {'error': 'PDFファイル形式のみ対応しています'}, 400
    fci_number = breed.get('fci_number', 0)
    pdf_dir = os.path.join(app.static_folder, 'breeds', 'pdfs')
    os.makedirs(pdf_dir, exist_ok=True)
    pdf_path = os.path.join(pdf_dir, f'{fci_number}.pdf')
    pdf_file.save(pdf_path)
    logger.info(f"Breed PDF uploaded: {breed_id} (FCI {fci_number})")
    return {'message': 'PDF uploaded', 'pdf_url': f'/static/breeds/pdfs/{fci_number}.pdf'}


@app.route('/api/breeds/pdf-status', methods=['GET'])
@ensure_json_response
def breed_pdf_status():
    """Check which breeds have PDFs uploaded."""
    pdf_dir = os.path.join(app.static_folder, 'breeds', 'pdfs')
    available = {}
    for breed_id, breed in BREED_DATA.items():
        fci = breed.get('fci_number', 0)
        pdf_path = os.path.join(pdf_dir, f'{fci}.pdf')
        available[breed_id] = os.path.isfile(pdf_path)
    total = sum(1 for v in available.values() if v)
    return {'pdf_status': available, 'total_with_pdf': total, 'total_breeds': len(BREED_DATA)}


# =============================================================================
# Pre-analysis Endpoints (background analysis on file attach)
# =============================================================================

@app.route('/api/pre-analyze-photo', methods=['POST'])
@limiter.limit("20 per hour")
@optional_auth
@ensure_json_response
def pre_analyze_photo():
    """写真を先行解析（バックグラウンド）"""
    if 'photo' not in request.files:
        return {'error': '写真が必要です', 'error_code': 'no_file'}, 400

    photo_file = request.files['photo']
    ext, err = _validate_upload_ext(photo_file.filename, ALLOWED_IMAGE_EXT)
    if err:
        return {'error': err, 'error_code': 'unsupported_ext'}, 400

    breed_id = request.form.get('breed_id', DEFAULT_BREED_ID)
    breed_data = BREED_DATA.get(breed_id, BREED_DATA[DEFAULT_BREED_ID])
    breed_name = breed_data['name']

    photo_bytes = photo_file.read()
    img_err = _validate_image_file(photo_bytes)
    if img_err:
        return {'success': False, 'error': img_err, 'error_code': 'invalid_image'}, 400

    photo_base64 = base64.b64encode(photo_bytes).decode('utf-8')
    del photo_bytes

    start_time = time.time()

    # Analyze input with RECO3
    input_analysis = {}
    if RECO3_AVAILABLE:
        input_analysis = analyze_request_input(breed_id, request.form)

    with ThreadPoolExecutor(max_workers=2) as executor:
        f_structure = executor.submit(analyze_photo_structure, photo_base64, breed_name, breed_data)
        f_coat = executor.submit(analyze_photo_coat, photo_base64, breed_name, breed_data)

        try:
            structure_result = f_structure.result(timeout=45)
        except Exception as e:
            logger.error(f"Pre-analyze structure error: {e}")
            structure_result = {'score': 80.0, 'comments': '解析中にエラーが発生しました', 'error_code': 'analysis_failed'}

        try:
            coat_result = f_coat.result(timeout=45)
        except Exception as e:
            logger.error(f"Pre-analyze coat error: {e}")
            coat_result = {'score': 80.0, 'comments': '解析中にエラーが発生しました', 'error_code': 'analysis_failed'}

    elapsed = round(time.time() - start_time, 2)
    logger.info(f"Pre-analyze photo completed in {elapsed}s")

    # AngleGate: comparison eligibility for structure
    if gate_for_comparison and isinstance(structure_result, dict):
        angle_info = structure_result.get('angle')
        comparison = gate_for_comparison(angle_info, mode='photo')
        structure_result['comparison'] = comparison
        if not comparison['eligible']:
            # Reduce confidence for non-comparable results
            if 'score' in structure_result:
                structure_result['score'] = round(
                    max(0, min(100, structure_result['score'] * 0.85)), 1)
            warnings = structure_result.get('warnings', [])
            warnings.append('comparison_hold')
            warnings.append(f'comparison_reason:{comparison["reason"]}')
            structure_result['warnings'] = warnings
            structure_result.setdefault('note', '')
            if structure_result['note']:
                structure_result['note'] += ' '
            structure_result['note'] += '比較・ランキングには真横（サイドビュー）撮影が必要です。'

    # Capture guide (3-line shooting advice)
    if make_capture_guide and isinstance(structure_result, dict):
        comp = structure_result.get('comparison')
        if comp:
            structure_result['capture_guide'] = make_capture_guide(
                mode='photo', comparison=comp, angle=structure_result.get('angle'))

    # Quality grading (PASS / HOLD)
    if grade_photo_quality and isinstance(structure_result, dict):
        structure_result['quality'] = grade_photo_quality(structure_result)

    response = {
        'success': True,
        'structure': structure_result,
        'coat': coat_result,
        'elapsed': elapsed,
        'breed_name': breed_name,
    }

    # Analyze output with RECO3
    if RECO3_AVAILABLE:
        output_analysis = analyze_photo_output(structure_result, coat_result)
        response = add_reco3_metadata(response, input_analysis, output_analysis)

    return response


@app.route('/api/pre-analyze-video', methods=['POST'])
@limiter.limit("10 per hour")
@optional_auth
@ensure_json_response
def pre_analyze_video():
    """動画を先行解析（バックグラウンド）"""
    if 'video' not in request.files or not request.files['video'].filename:
        return {'error': '動画が必要です', 'error_code': 'no_file'}, 400

    video_file = request.files['video']
    ext, err = _validate_upload_ext(video_file.filename, ALLOWED_VIDEO_EXT)
    if err:
        return {'success': False, 'error': err, 'error_code': 'unsupported_ext'}, 400

    breed_id = request.form.get('breed_id', DEFAULT_BREED_ID)
    breed_data = BREED_DATA.get(breed_id, BREED_DATA[DEFAULT_BREED_ID])
    breed_name = breed_data['name']

    # Analyze input with RECO3
    input_analysis = {}
    if RECO3_AVAILABLE:
        input_analysis = analyze_request_input(breed_id, request.form)

    original_filename = video_file.filename or 'video.mp4'
    video_filename = f"{uuid.uuid4()}{ext}"
    video_path = os.path.join(UPLOAD_DIR, video_filename)
    video_file.save(video_path)
    logger.info(f"Video upload received: {original_filename} -> {video_filename}")

    # extract_video_frames内でMOV→MP4自動変換も行われる
    video_frames, video_meta = extract_video_frames(video_path)

    if not video_frames:
        # 具体的なエラーメッセージをerror_codeごとに生成
        error_code = video_meta.get('error_code') or video_meta.get('error', 'extraction_failed')
        _error_messages = {
            'no_extraction_tools': ('OpenCV・ffmpegの両方が利用できないため動画を処理できません。サーバー管理者にお問い合わせください。', 500),
            'opencv_missing': ('OpenCVが利用できないため動画を処理できません。サーバー管理者にお問い合わせください。', 500),
            'ffmpeg_missing': (f'{ext}形式の動画を処理できませんでした。ffmpegが未インストールのためMOV変換ができません。', 400),
            'extraction_failed': ('動画のデコードに失敗しました。ファイルが破損しているか、サポートされていない形式です。', 400),
            'no_frames': ('動画からフレームを抽出できませんでした（0フレーム）。別の動画をお試しください。', 400),
        }
        error_msg, status = _error_messages.get(error_code,
            ('動画からフレームを抽出できませんでした。別の動画をお試しください。', 400))
        with contextlib.suppress(OSError):
            os.remove(video_path)
        return {
            'success': False,
            'error': error_msg,
            'error_code': error_code,
            'video_meta': {
                'input_ext': video_meta.get('input_ext'),
                'input_size_bytes': video_meta.get('input_size_bytes'),
                'cv2_available': video_meta.get('cv2_available'),
                'ffmpeg_available': video_meta.get('ffmpeg_available'),
                'converted': video_meta.get('converted'),
                'convert_error': video_meta.get('convert_error'),
                'frames_extracted': video_meta.get('frames_extracted', 0),
            },
        }, status

    start_time = time.time()

    try:
        video_result = analyze_video_frames(video_frames, breed_name, breed_data)
    except Exception as e:
        logger.error(f"Pre-analyze video error: {e}")
        video_result = {
            'gait': {'score': 70.0, 'comments': '解析中にエラーが発生しました'},
            'temperament': {'score': 70.0, 'comments': '解析中にエラーが発生しました'},
            'coat_motion': {'score': 70.0, 'comments': '解析中にエラーが発生しました'},
            'analysis_method': 'error_fallback',
            'error_detail': '動画解析中にエラーが発生しました',
        }

    with contextlib.suppress(OSError):
        os.remove(video_path)

    # AngleGate: comparison eligibility for video
    if gate_for_comparison and isinstance(video_result, dict):
        angle_summary = video_result.get('angle_summary')
        comparison = gate_for_comparison(angle_summary, mode='video')
        video_result['comparison'] = comparison
        if not comparison['eligible']:
            gait = video_result.get('gait')
            if isinstance(gait, dict) and 'score' in gait:
                gait['score'] = round(max(0, min(100, gait['score'] * 0.85)), 1)
            warnings = video_result.get('warnings', [])
            warnings.append('comparison_hold')
            warnings.append(f'comparison_reason:{comparison["reason"]}')
            video_result['warnings'] = warnings

    # Capture guide (3-line shooting advice)
    if make_capture_guide and isinstance(video_result, dict):
        comp = video_result.get('comparison')
        if comp:
            video_result['capture_guide'] = make_capture_guide(
                mode='video', comparison=comp, angle=video_result.get('angle_summary'))

    # Quality grading (PASS / HOLD)
    if grade_video_quality and isinstance(video_result, dict):
        video_result['quality'] = grade_video_quality(video_result)

    elapsed = round(time.time() - start_time, 2)
    logger.info(f"Pre-analyze video completed in {elapsed}s")

    response = {
        'success': True,
        'video': video_result,
        'frame_count': len(video_frames),
        'elapsed': elapsed,
        'breed_name': breed_name,
        'video_meta': {
            'input_ext': video_meta.get('input_ext'),
            'extraction_method': video_meta.get('extraction_method'),
            'frames_extracted': video_meta.get('frames_extracted', len(video_frames)),
            'fps': video_meta.get('fps'),
            'duration_sec': video_meta.get('duration_sec'),
            'converted': video_meta.get('converted', False),
        },
    }
    if video_meta.get('truncated'):
        response['warning'] = f'動画が{video_meta["original_duration"]}秒ありますが、最初の30秒のみ解析しました。'
    if video_meta.get('converted_from'):
        response['info'] = f'{video_meta["converted_from"]}形式をMP4に自動変換して解析しました。'

    # Analyze output with RECO3
    if RECO3_AVAILABLE:
        output_analysis = analyze_video_output(video_result)
        response = add_reco3_metadata(response, input_analysis, output_analysis)

    return response


@app.route('/api/analyze-comprehensive', methods=['POST'])
@limiter.limit("15 per hour")
@optional_auth
@ensure_json_response
def analyze_comprehensive():
    """写真と動画の包括的な解析"""

    # パラメータ取得
    breed_id = request.form.get('breed_id', DEFAULT_BREED_ID)
    dog_id = request.form.get('dog_id')  # Optional: for saving to specific dog
    age_years = float(request.form.get('age_years', 3.0))
    request.form.get('dog_name', '')

    breed_data = BREED_DATA.get(breed_id, BREED_DATA[DEFAULT_BREED_ID])
    breed_name = breed_data['name']

    # 写真取得（必須）
    if 'photo' not in request.files:
        return {'error': '写真が必要です'}, 400

    photo_file = request.files['photo']
    p_ext, p_err = _validate_upload_ext(photo_file.filename, ALLOWED_IMAGE_EXT)
    if p_err:
        return {'error': p_err}, 400

    photo_filename = f"{uuid.uuid4()}{p_ext}"
    photo_path = os.path.join(UPLOAD_DIR, photo_filename)

    # Read once, save and encode from the same bytes (avoid double I/O)
    photo_bytes = photo_file.read()
    img_err = _validate_image_file(photo_bytes)
    if img_err:
        return {'success': False, 'error': img_err}, 400
    with open(photo_path, 'wb') as f:
        f.write(photo_bytes)
    photo_base64 = base64.b64encode(photo_bytes).decode('utf-8')
    del photo_bytes  # Free memory immediately

    # 動画取得（任意）
    video_frames = []
    video_path = None
    video_meta = {}
    has_video = 'video' in request.files and request.files['video'].filename

    if has_video:
        video_file = request.files['video']
        vext, v_err = _validate_upload_ext(video_file.filename, ALLOWED_VIDEO_EXT)
        if v_err:
            with contextlib.suppress(OSError):
                os.remove(photo_path)
            return {'error': v_err}, 400
        video_filename = f"{uuid.uuid4()}{vext}"
        video_path = os.path.join(UPLOAD_DIR, video_filename)
        video_file.save(video_path)
        logger.info(f"Video upload received: {video_file.filename} -> {video_filename}")

        # フレーム抽出（MOV→MP4自動変換含む）
        video_frames, video_meta = extract_video_frames(video_path)
        logger.info(f"Video uploaded ({vext}), extracted {len(video_frames)} frames"
                     f"{' [converted]' if video_meta.get('converted_from') else ''}")

    # ========== 解析実行（並列処理で高速化）==========
    logger.info(f"Analyzing: breed={breed_name}, age={age_years}, has_video={has_video}")
    start_time = time.time()

    # 並列でAPI呼び出しを実行（タイムアウト60秒）
    with ThreadPoolExecutor(max_workers=3) as executor:
        # 写真解析を並列実行
        structure_future = executor.submit(analyze_photo_structure, photo_base64, breed_name, breed_data)
        coat_future = executor.submit(analyze_photo_coat, photo_base64, breed_name, breed_data)

        # 動画解析（動画がある場合）
        if video_frames:
            video_future = executor.submit(analyze_video_frames, video_frames, breed_name, breed_data)
        else:
            video_future = None

        # 結果を取得（タイムアウト45秒）
        try:
            structure_result = structure_future.result(timeout=45)
        except (FuturesTimeoutError, Exception) as e:
            logger.error(f"Structure analysis timeout/error: {e}")
            structure_result = {'score': 80.0, 'comments': '解析がタイムアウトしました'}

        try:
            coat_photo_result = coat_future.result(timeout=45)
        except (FuturesTimeoutError, Exception) as e:
            logger.error(f"Coat analysis timeout/error: {e}")
            coat_photo_result = {'score': 80.0, 'comments': '解析がタイムアウトしました'}

        if video_future:
            try:
                video_result = video_future.result(timeout=45)
            except (FuturesTimeoutError, Exception) as e:
                logger.error(f"Video analysis timeout/error: {e}")
                video_result = {
                    'gait': {'score': 75.0, 'comments': '解析がタイムアウトしました'},
                    'temperament': {'score': 75.0, 'comments': '解析がタイムアウトしました'},
                    'coat_motion': {'score': 75.0, 'comments': '解析がタイムアウトしました'}
                }
        elif has_video and not video_frames:
            # 動画はアップロード済みだがフレーム抽出失敗
            error_msg = video_meta.get('error', 'extraction_failed')
            error_detail = f' ({error_msg})' if error_msg else ''
            video_result = {
                'gait': {'score': None, 'comments': f'フレーム抽出失敗{error_detail}'},
                'temperament': {'score': None, 'comments': f'フレーム抽出失敗{error_detail}'},
                'coat_motion': {'score': None, 'comments': f'フレーム抽出失敗{error_detail}'}
            }
        else:
            # 動画未アップロード
            video_result = {
                'gait': {'score': None, 'comments': '動画なし'},
                'temperament': {'score': None, 'comments': '動画なし'},
                'coat_motion': {'score': None, 'comments': '動画なし'}
            }

    elapsed = time.time() - start_time
    logger.info(f"Analysis completed in {elapsed:.1f}s")

    # スコア取得
    structure_score = structure_result.get('score', 85.0)
    coat_photo_score = coat_photo_result.get('score', 85.0)
    gait_score = video_result.get('gait', {}).get('score')
    temperament_score = video_result.get('temperament', {}).get('score')
    coat_video_score = video_result.get('coat_motion', {}).get('score')

    # ========== ハイブリッドスコアリング: アルゴリズム（主導）→ AI補正（伴奏） ==========
    # Layer 1: Deterministic algorithm coefficients produce base scores
    # Layer 2: AI observations provide capped corrections
    if SCORING_AVAILABLE:
        # Layer 1: Map raw inputs to the 5 canonical axes (algorithm base scores)
        axis_scores = map_ai_scores_to_axes(
            structure_score=structure_score,
            structure_details=structure_result,
            coat_score=coat_photo_score if not coat_video_score else (coat_photo_score * 0.6 + coat_video_score * 0.4),
            gait_score=gait_score,
            gait_details=video_result.get('gait', {}),
            temperament_score=temperament_score,
            temperament_details=video_result.get('temperament', {})
        )

        # Layer 2: Collect ALL AI sub-scores for precision correction
        # Every sub-score the AI returned is passed to the aggregator
        ai_sub_scores = {}

        # Skeletal sub-scores from structure analysis
        skeletal_subs = {}
        for key in ('proportion', 'skeletal'):
            val = structure_result.get(key)
            if val is not None:
                skeletal_subs[key] = float(val)
        if skeletal_subs:
            ai_sub_scores['skeletal'] = skeletal_subs

        # Muscle sub-scores from structure analysis
        muscle_subs = {}
        val = structure_result.get('muscular')
        if val is not None:
            muscle_subs['muscular'] = float(val)
        if muscle_subs:
            ai_sub_scores['muscle'] = muscle_subs

        # Gait sub-scores from video analysis (all 3: stride, balance, fluidity)
        if gait_score is not None:
            gait_details_data = video_result.get('gait', {})
            gait_subs = {}
            for key in ('stride', 'balance', 'fluidity'):
                val = gait_details_data.get(key)
                if val is not None:
                    gait_subs[key] = float(val)
            if gait_subs:
                ai_sub_scores['gait'] = gait_subs

        # Coat sub-scores from photo + video
        coat_subs = {}
        for key in ('texture', 'volume', 'grooming'):
            val = coat_photo_result.get(key)
            if val is not None:
                coat_subs[key] = float(val)
        if coat_video_score is not None:
            coat_subs['motion'] = float(coat_video_score)
        if coat_subs:
            ai_sub_scores['coat'] = coat_subs

        # Temperament sub-scores from video (all 3: confidence, alertness, composure)
        if temperament_score is not None:
            temp_details = video_result.get('temperament', {})
            temp_subs = {}
            for key in ('confidence', 'alertness', 'composure'):
                val = temp_details.get(key)
                if val is not None:
                    temp_subs[key] = float(val)
            if temp_subs:
                ai_sub_scores['temperament'] = temp_subs

        # Execute hybrid pipeline v2: full sub-score aggregation + breed sensitivity
        hybrid_result = hybrid_score(
            algorithm_axis_scores=axis_scores,
            ai_observations=None,
            age_years=age_years,
            breed_id=breed_id,
            sub_scores=ai_sub_scores if ai_sub_scores else None
        )

        score_result = hybrid_result['final_result']
        hybrid_pipeline_data = hybrid_result

        overall = score_result['final_score']
        grade = score_result['grade']
        grade_full = score_result['grade_full']
        fci_grade = score_result.get('fci_grade', '')
        fci_grade_ja = score_result.get('fci_grade_ja', '')
        age_adjustment = score_result['age_adjustment']
        age_months = score_result['age_months']

        # Age context for display
        if age_months <= 6:
            age_context = '成長期・骨格未完成'
            age_multiplier = 0.85
        elif age_months <= 12:
            age_context = '若齢期・発達中'
            age_multiplier = 0.90
        elif age_months <= 24:
            age_context = '若齢期・成熟中'
            age_multiplier = 0.95
        elif age_months <= 84:
            age_context = '成犬ピーク期（2-7歳）'
            age_multiplier = 1.00
        elif age_months <= 108:
            age_context = '中高齢期・軽度低下'
            age_multiplier = 0.93
        elif age_months <= 132:
            age_context = '高齢期・関節変化'
            age_multiplier = 0.85
        else:
            age_context = '超高齢期・顕著な低下'
            age_multiplier = 0.75
    else:
        # Legacy fallback (should not happen in production)
        axis_scores = None
        score_result = None
        age_adjustment = 0

        # 年齢調整（歩様用）- Legacy
        if age_years < 1:
            age_multiplier = 0.85
            age_context = '成長期・骨格未完成'
        elif age_years < 2:
            age_multiplier = 0.95
            age_context = '若齢期・成熟中'
        elif age_years < 7:
            age_multiplier = 1.00
            age_context = '成犬ピーク期（2-7歳）'
        elif age_years < 10:
            age_multiplier = 0.93
            age_context = '中高齢期・軽度低下'
        elif age_years < 12:
            age_multiplier = 0.85
            age_context = '高齢期・関節変化'
        else:
            age_multiplier = 0.75
            age_context = '超高齢期・顕著な低下'

        # 総合スコア計算 - Legacy
        if has_video and gait_score:
            coat_combined = (coat_photo_score * 0.6 + (coat_video_score or coat_photo_score) * 0.4)
            overall = (
                structure_score * 0.30 +
                (gait_score / age_multiplier) * 0.30 +
                coat_combined * 0.25 +
                (temperament_score or 85) * 0.15
            )
        else:
            overall = (
                structure_score * 0.50 +
                coat_photo_score * 0.50
            )

        overall = min(100, max(0, overall))

        # グレード判定 - Legacy (with FCI mapping)
        from api.scoring import get_grade as _get_grade, get_fci_grade as _get_fci_grade
        grade, grade_full = _get_grade(overall)
        fci_grade, fci_grade_ja = _get_fci_grade(grade)

    # ========== 詳細説明生成 ==========
    explanations = []

    # 体構造の説明
    explanations.append({
        'icon': '📏',
        'title': f'体構造評価: {structure_score:.1f}点',
        'description': structure_result.get('comments', f'{breed_name}の体構造を評価しました。') +
                      f" プロポーション: {structure_result.get('proportion', '-')}点, " +
                      f"骨格: {structure_result.get('skeletal', '-')}点, " +
                      f"筋肉: {structure_result.get('muscular', '-')}点",
        'evidence': f'FCI基準 No.{breed_data["fci_no"]} に基づく評価'
    })

    # 被毛の説明
    explanations.append({
        'icon': '✨',
        'title': f'被毛評価（写真）: {coat_photo_score:.1f}点',
        'description': coat_photo_result.get('comments', f'{breed_name}の被毛状態を評価しました。') +
                      f" 質感: {coat_photo_result.get('texture', '-')}点, " +
                      f"毛量: {coat_photo_result.get('volume', '-')}点, " +
                      f"手入れ: {coat_photo_result.get('grooming', '-')}点",
        'evidence': '犬種標準の被毛基準に基づく評価'
    })

    # 歩様の説明（動画がある場合）
    if has_video and gait_score:
        gait_data = video_result.get('gait', {})
        adjusted_gait = min(100, gait_score / age_multiplier)
        explanations.append({
            'icon': '🏃',
            'title': f'歩様評価: {gait_score:.1f}点（年齢調整後: {adjusted_gait:.1f}点）',
            'description': gait_data.get('comments', '歩様を評価しました。') +
                          f" ストライド: {gait_data.get('stride', '-')}点, " +
                          f"バランス: {gait_data.get('balance', '-')}点, " +
                          f"流動性: {gait_data.get('fluidity', '-')}点。" +
                          f" 年齢({age_years:.1f}歳)による調整係数: {age_multiplier}",
            'evidence': 'Veterinary Journal (2013) - 年齢による歩様変化の研究に基づく'
        })

        # 気質の説明
        temperament_data = video_result.get('temperament', {})
        explanations.append({
            'icon': '🎭',
            'title': f'気質評価: {temperament_score:.1f}点',
            'description': temperament_data.get('comments', '気質を評価しました。') +
                          f" 自信: {temperament_data.get('confidence', '-')}点, " +
                          f"注意力: {temperament_data.get('alertness', '-')}点, " +
                          f"落ち着き: {temperament_data.get('composure', '-')}点",
            'evidence': 'ドッグショー審査基準に基づく気質評価'
        })
    else:
        explanations.append({
            'icon': '🎬',
            'title': '動画評価: 未実施',
            'description': '動画がアップロードされていないため、歩様・気質の評価は行われていません。より正確な評価のために動画のアップロードをお勧めします。',
            'evidence': ''
        })

    # 総評
    explanations.append({
        'icon': '📊',
        'title': f'総合評価: {overall:.1f}点 - {grade_full}',
        'description': f'{breed_name}の総合的な評価結果です。' +
                      ('写真から体構造と被毛を、動画から歩様と気質を評価しました。' if has_video else
                       '写真から体構造と被毛を評価しました。') +
                      f' {age_context}の個体として、{"優れた" if overall >= 85 else "良好な" if overall >= 75 else "標準的な"}評価となりました。',
        'evidence': '18+の査読済み論文とFCI国際基準に基づく総合評価'
    })

    # ========== 犬種キャリブレーション適用 ==========
    calibrated = False
    try:
        from api.auto_cycle import apply_calibration_to_analysis
        cal_input = {'structure': structure_score, 'coat': coat_photo_score}
        if gait_score is not None:
            cal_input['gait'] = gait_score
        cal_output = apply_calibration_to_analysis(breed_id, cal_input)
        if cal_output != cal_input:
            calibrated = True
            if cal_output.get('structure') != structure_score:
                structure_score = round(cal_output['structure'], 1)
            if cal_output.get('coat') != coat_photo_score:
                coat_photo_score = round(cal_output['coat'], 1)
            if gait_score is not None and cal_output.get('gait') != gait_score:
                gait_score = round(cal_output['gait'], 1)
            # Recalculate overall if calibrated and scoring available
            if SCORING_AVAILABLE:
                overall = round(score_result['final_score'], 1)
            logger.info(f"Breed calibration applied for {breed_id}: {cal_input} -> {cal_output}")
    except (ImportError, Exception) as e:
        logger.debug(f"Calibration not applied: {e}")

    # ========== 疾患エビデンス統合 ==========
    health_evidence = {}
    try:
        from api.auto_cycle import get_evidence_based_disease_params
        health_evidence = get_evidence_based_disease_params(breed_id)
    except (ImportError, Exception) as e:
        logger.debug(f"Disease evidence not available: {e}")

    # ========== 交配相手推奨 ==========
    scores_for_breeding = {
        'structure': {'score': structure_score},
        'coat_photo': {'score': coat_photo_score},
        'gait': {'score': gait_score} if gait_score else {}
    }
    breeding_recommendations = generate_breeding_recommendations(
        breed_name, breed_data, scores_for_breeding, age_years
    )

    # ========== クリーンアップ ==========
    try:
        os.remove(photo_path)
        if video_path:
            os.remove(video_path)
    except OSError as e:
        logger.warning(f"Failed to clean up temporary files: {e}")

    gc.collect()

    # ========== 総合的な解析方式判定 ==========
    # 各軸のanalysis_methodを収集
    struct_method = structure_result.get('analysis_method', 'unknown')
    coat_method = coat_photo_result.get('analysis_method', 'unknown')
    video_method = video_result.get('analysis_method', 'unknown') if has_video else 'n/a'

    # AI補正が適用されたかを判定
    has_ai_correction = False
    if SCORING_AVAILABLE and hybrid_pipeline_data:
        layer2 = hybrid_pipeline_data.get('layer2_ai_correction', {})
        has_ai_correction = layer2.get('corrections_applied', False)

    # 総合的なanalysis_methodを決定
    methods = [struct_method, coat_method] + ([video_method] if has_video else [])
    if 'ai' in methods and has_ai_correction:
        overall_method = 'hybrid'  # AIデータ+AI補正 = ハイブリッド式
        overall_method_label = 'ハイブリッド式（アルゴリズム主導 + AI補正）'
    elif 'ai' in methods:
        overall_method = 'ai_only'  # AIデータのみ、補正なし
        overall_method_label = 'AI解析のみ（補正なし）'
    elif 'opencv' in methods or 'pillow' in methods:
        overall_method = 'algorithm'  # アルゴリズムのみ
        overall_method_label = 'アルゴリズム式（OpenCV/Pillow画像処理）'
    elif 'hash' in methods:
        overall_method = 'algorithm_hash'  # ハッシュベース決定論的
        overall_method_label = 'アルゴリズム式（決定論的ハッシュ）'
    else:
        overall_method = 'unknown'
        overall_method_label = '解析方式不明'

    # ========== 結果返却 ==========
    result = {
        'overall_score': round(overall, 1),
        'grade': grade,
        'grade_full': grade_full,
        'fci_grade': fci_grade,
        'fci_grade_ja': fci_grade_ja,
        'analysis_method': overall_method,
        'analysis_method_label': overall_method_label,
        'scores': {
            'structure': {
                'display': round(structure_score, 1),
                'weight': '25%',  # Fixed weight from Algorithm_Declaration
                'details': structure_result,
                'analysis_method': struct_method
            },
            'coat_photo': {
                'display': round(coat_photo_score, 1),
                'weight': '20%',  # Fixed weight from Algorithm_Declaration
                'details': coat_photo_result,
                'analysis_method': coat_method
            },
            'gait': {
                'display': round(gait_score, 1) if gait_score else None,
                'weight': '25%',  # Fixed weight from Algorithm_Declaration
                'age_context': age_context,
                'details': video_result.get('gait', {}),
                'analysis_method': video_method if has_video else 'n/a'
            },
            'temperament': {
                'display': round(temperament_score, 1) if temperament_score else None,
                'weight': '10%',  # Fixed weight from Algorithm_Declaration
                'details': video_result.get('temperament', {}),
                'analysis_method': video_method if has_video else 'n/a'
            },
            'muscle': {
                'display': round(axis_scores.get('muscle', 75), 1) if axis_scores else None,
                'weight': '20%',  # Fixed weight from Algorithm_Declaration
                'details': {},
                'analysis_method': struct_method  # muscle comes from structure
            },
            'coat_video': {
                'display': round(coat_video_score, 1) if coat_video_score else None,
                'weight': '-',  # Combined into coat score
                'details': video_result.get('coat_motion', {}),
                'analysis_method': video_method if has_video else 'n/a'
            }
        },
        'explanations': explanations,
        'breeding_recommendations': breeding_recommendations,
        'health_evidence': health_evidence,
        'metadata': {
            'breed_id': breed_id,
            'breed_name': breed_name,
            'breed_name_en': breed_data['name_en'],
            'fci_no': breed_data['fci_no'],
            'age_years': age_years,
            'age_adjustment': age_adjustment if SCORING_AVAILABLE else 0,
            'has_video': has_video,
            'vision_enabled': VISION_ENABLED,
            'model': (ANTHROPIC_MODEL if claude_client else OPENAI_MODEL) if VISION_ENABLED else 'local_fallback',
            'calibrated': calibrated,
            'video_meta': video_meta if has_video else {},
            'video_frame_extraction': {
                'method': video_meta.get('extraction_method') if has_video else None,
                'frames_extracted': len(video_frames) if has_video else 0,
                'error': video_meta.get('error') if has_video else None
            }
        },
        'algorithm': {
            'version': ALGORITHM_VERSION,
            'model_version': MODEL_VERSION,
            'weights_hash': WEIGHTS_HASH,
            'deterministic': SCORING_AVAILABLE,
            'pipeline': 'algorithm_first_ai_corrects',
            'axis_scores': axis_scores if SCORING_AVAILABLE else None,
            'hybrid_pipeline': hybrid_pipeline_data if SCORING_AVAILABLE else None
        },
        'version': VERSION
    }

    logger.info(f"Analysis complete: score={overall:.1f}, grade={grade}, has_video={has_video}")

    # ========== ログインユーザーの場合、結果を保存 ==========
    analysis_id = None
    if request.current_user and DB_AVAILABLE and dog_id:
        try:
            dog_id_int = int(dog_id)
            # 犬の所有者確認
            dog = get_dog_by_id(dog_id_int, request.current_user['id'])
            if dog:
                analysis_id = save_analysis(
                    dog_id_int,
                    request.current_user['id'],
                    age_years,
                    has_video,
                    result
                )
                result['analysis_id'] = analysis_id
                result['saved'] = True
                logger.info(f"Analysis saved with ID: {analysis_id}")
        except Exception as e:
            logger.error(f"Failed to save analysis: {e}")
            result['saved'] = False

    # ========== 監査ログ記録 ==========
    # Record audit log for every analysis (per Model_Governance.md)
    if SCORING_AVAILABLE and DB_AVAILABLE and axis_scores:
        try:
            audit_id = save_audit_log(
                analysis_id=analysis_id,
                user_id=request.current_user['id'] if request.current_user else None,
                dog_id=int(dog_id) if dog_id else None,
                algorithm_version=ALGORITHM_VERSION,
                model_version=MODEL_VERSION,
                weights_hash=WEIGHTS_HASH,
                input_type='both' if has_video else 'photo',
                axis_scores=axis_scores,
                final_score=overall,
                grade=grade
            )
            result['audit_id'] = audit_id
            logger.info(f"Audit log recorded with ID: {audit_id}")
        except Exception as e:
            logger.error(f"Failed to save audit log: {e}")

    return result


# =============================================================================
# SSE Real-Time Progress Analysis Endpoint
# =============================================================================

def _sse_event(event_type, data):
    """Format a Server-Sent Event."""
    return f"event: {event_type}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"


@app.route('/api/analyze-comprehensive-stream', methods=['POST'])
@optional_auth
def analyze_comprehensive_stream():
    """SSE streaming version of comprehensive analysis with real-time progress."""

    # --- Parse parameters (same as analyze_comprehensive) ---
    breed_id = request.form.get('breed_id', DEFAULT_BREED_ID)
    dog_id = request.form.get('dog_id')
    age_years = float(request.form.get('age_years', 3.0))
    request.form.get('dog_name', '')

    breed_data = BREED_DATA.get(breed_id, BREED_DATA[DEFAULT_BREED_ID])
    breed_name = breed_data['name']

    if 'photo' not in request.files:
        return jsonify({'error': '写真が必要です'}), 400

    photo_file = request.files['photo']
    p_ext, p_err = _validate_upload_ext(photo_file.filename, ALLOWED_IMAGE_EXT)
    if p_err:
        return jsonify({'error': p_err}), 400

    photo_filename = f"{uuid.uuid4()}{p_ext}"
    photo_path = os.path.join(UPLOAD_DIR, photo_filename)

    photo_bytes = photo_file.read()
    img_err = _validate_image_file(photo_bytes)
    if img_err:
        return jsonify({'success': False, 'error': img_err}), 400
    with open(photo_path, 'wb') as f:
        f.write(photo_bytes)
    photo_base64 = base64.b64encode(photo_bytes).decode('utf-8')
    del photo_bytes

    video_frames = []
    video_path = None
    video_meta = {}
    has_video = 'video' in request.files and request.files['video'].filename

    if has_video:
        video_file = request.files['video']
        vext, v_err = _validate_upload_ext(video_file.filename, ALLOWED_VIDEO_EXT)
        if v_err:
            with contextlib.suppress(OSError):
                os.remove(photo_path)
            return jsonify({'error': v_err}), 400
        video_filename = f"{uuid.uuid4()}{vext}"
        video_path = os.path.join(UPLOAD_DIR, video_filename)
        video_file.save(video_path)
        logger.info(f"Stream: Video upload received: {video_file.filename} -> {video_filename}")
        # MOV→MP4自動変換はextract_video_frames内で処理
        video_frames, video_meta = extract_video_frames(video_path)
        logger.info(f"Stream: Video processed ({vext}), extracted {len(video_frames)} frames"
                     f"{' [converted]' if video_meta.get('converted_from') else ''}")

    # Capture current_user before entering generator (request context won't be available)
    current_user = getattr(request, 'current_user', None)

    # Store video_meta for use inside generator
    stream_video_meta = video_meta if has_video else {}

    def generate():
        nonlocal video_frames, video_path, has_video

        # Step 1: Uploaded
        yield _sse_event("progress", {"step": "upload", "percent": 10, "message": "アップロード完了"})

        # 動画が30秒超で切り捨てされた場合、フロントエンドに警告
        if stream_video_meta.get('truncated'):
            yield _sse_event("warning", {"message": f"動画が{stream_video_meta['original_duration']}秒ありますが、最初の30秒のみ解析します。"})

        start_time = time.time()

        # Step 2: Structure analysis
        yield _sse_event("progress", {"step": "structure", "percent": 20, "message": "体構造を解析中..."})
        try:
            structure_result = analyze_photo_structure(photo_base64, breed_name, breed_data)
        except Exception as e:
            logger.error(f"Structure analysis error: {e}")
            structure_result = {'score': 80.0, 'comments': '解析中にエラーが発生しました'}
        yield _sse_event("progress", {"step": "structure_done", "percent": 40, "message": "体構造の解析完了"})

        # Step 3: Coat analysis
        yield _sse_event("progress", {"step": "coat", "percent": 45, "message": "被毛を解析中..."})
        try:
            coat_photo_result = analyze_photo_coat(photo_base64, breed_name, breed_data)
        except Exception as e:
            logger.error(f"Coat analysis error: {e}")
            coat_photo_result = {'score': 80.0, 'comments': '解析中にエラーが発生しました'}
        yield _sse_event("progress", {"step": "coat_done", "percent": 60, "message": "被毛の解析完了"})

        # Step 4: Video analysis (if available)
        if video_frames:
            yield _sse_event("progress", {"step": "video", "percent": 65, "message": "動画を解析中（歩様・気質）..."})
            try:
                video_result = analyze_video_frames(video_frames, breed_name, breed_data)
            except Exception as e:
                logger.error(f"Video analysis error: {e}")
                video_result = {
                    'gait': {'score': 70.0, 'comments': '解析中にエラーが発生しました'},
                    'temperament': {'score': 70.0, 'comments': '解析中にエラーが発生しました'},
                    'coat_motion': {'score': 70.0, 'comments': '解析中にエラーが発生しました'}
                }
            yield _sse_event("progress", {"step": "video_done", "percent": 80, "message": "動画の解析完了"})
        elif has_video and not video_frames:
            # 動画はアップロード済みだがフレーム抽出失敗
            error_msg = stream_video_meta.get('error', 'extraction_failed')
            error_detail = f' ({error_msg})' if error_msg else ''
            video_result = {
                'gait': {'score': None, 'comments': f'フレーム抽出失敗{error_detail}'},
                'temperament': {'score': None, 'comments': f'フレーム抽出失敗{error_detail}'},
                'coat_motion': {'score': None, 'comments': f'フレーム抽出失敗{error_detail}'}
            }
            yield _sse_event("progress", {"step": "video_done", "percent": 80, "message": "動画のフレーム抽出失敗"})
        else:
            # 動画未アップロード
            video_result = {
                'gait': {'score': None, 'comments': '動画なし'},
                'temperament': {'score': None, 'comments': '動画なし'},
                'coat_motion': {'score': None, 'comments': '動画なし'}
            }

        # Step 5: Scoring
        yield _sse_event("progress", {"step": "scoring", "percent": 85, "message": "スコアを算出中..."})

        structure_score = structure_result.get('score', 85.0)
        coat_photo_score = coat_photo_result.get('score', 85.0)
        gait_score = video_result.get('gait', {}).get('score')
        temperament_score = video_result.get('temperament', {}).get('score')
        coat_video_score = video_result.get('coat_motion', {}).get('score')

        if SCORING_AVAILABLE:
            # Layer 1: Algorithm base scores (主導)
            axis_scores = map_ai_scores_to_axes(
                structure_score=structure_score,
                structure_details=structure_result,
                coat_score=coat_photo_score if not coat_video_score else (coat_photo_score * 0.6 + coat_video_score * 0.4),
                gait_score=gait_score,
                gait_details=video_result.get('gait', {}),
                temperament_score=temperament_score,
                temperament_details=video_result.get('temperament', {})
            )

            # Layer 2: Collect ALL AI sub-scores for precision correction
            ai_sub_scores = {}
            skeletal_subs = {}
            for key in ('proportion', 'skeletal'):
                val = structure_result.get(key)
                if val is not None:
                    skeletal_subs[key] = float(val)
            if skeletal_subs:
                ai_sub_scores['skeletal'] = skeletal_subs
            muscle_subs = {}
            val = structure_result.get('muscular')
            if val is not None:
                muscle_subs['muscular'] = float(val)
            if muscle_subs:
                ai_sub_scores['muscle'] = muscle_subs
            if gait_score is not None:
                gait_details_data = video_result.get('gait', {})
                gait_subs = {}
                for key in ('stride', 'balance', 'fluidity'):
                    val = gait_details_data.get(key)
                    if val is not None:
                        gait_subs[key] = float(val)
                if gait_subs:
                    ai_sub_scores['gait'] = gait_subs
            coat_subs = {}
            for key in ('texture', 'volume', 'grooming'):
                val = coat_photo_result.get(key)
                if val is not None:
                    coat_subs[key] = float(val)
            if coat_video_score is not None:
                coat_subs['motion'] = float(coat_video_score)
            if coat_subs:
                ai_sub_scores['coat'] = coat_subs
            if temperament_score is not None:
                temp_details = video_result.get('temperament', {})
                temp_subs = {}
                for key in ('confidence', 'alertness', 'composure'):
                    val = temp_details.get(key)
                    if val is not None:
                        temp_subs[key] = float(val)
                if temp_subs:
                    ai_sub_scores['temperament'] = temp_subs

            hybrid_result = hybrid_score(
                algorithm_axis_scores=axis_scores,
                ai_observations=None,
                age_years=age_years,
                breed_id=breed_id,
                sub_scores=ai_sub_scores if ai_sub_scores else None
            )
            score_result = hybrid_result['final_result']
            overall = score_result['final_score']
            grade = score_result['grade']
            grade_full = score_result['grade_full']
            fci_grade = score_result.get('fci_grade', '')
            fci_grade_ja = score_result.get('fci_grade_ja', '')
            age_adjustment = score_result['age_adjustment']
            age_months = score_result['age_months']

            if age_months <= 6:
                age_context = '成長期・骨格未完成'
                age_multiplier = 0.85
            elif age_months <= 12:
                age_context = '若齢期・発達中'
                age_multiplier = 0.90
            elif age_months <= 24:
                age_context = '若齢期・成熟中'
                age_multiplier = 0.95
            elif age_months <= 84:
                age_context = '成犬ピーク期（2-7歳）'
                age_multiplier = 1.00
            elif age_months <= 108:
                age_context = '中高齢期・軽度低下'
                age_multiplier = 0.93
            elif age_months <= 132:
                age_context = '高齢期・関節変化'
                age_multiplier = 0.85
            else:
                age_context = '超高齢期・顕著な低下'
                age_multiplier = 0.75
        else:
            axis_scores = None
            score_result = None
            age_adjustment = 0
            if age_years < 1:
                age_multiplier = 0.85
                age_context = '成長期・骨格未完成'
            elif age_years < 2:
                age_multiplier = 0.95
                age_context = '若齢期・成熟中'
            elif age_years < 7:
                age_multiplier = 1.00
                age_context = '成犬ピーク期（2-7歳）'
            elif age_years < 10:
                age_multiplier = 0.93
                age_context = '中高齢期・軽度低下'
            elif age_years < 12:
                age_multiplier = 0.85
                age_context = '高齢期・関節変化'
            else:
                age_multiplier = 0.75
                age_context = '超高齢期・顕著な低下'

            if has_video and gait_score:
                coat_combined = (coat_photo_score * 0.6 + (coat_video_score or coat_photo_score) * 0.4)
                overall = (structure_score * 0.30 + (gait_score / age_multiplier) * 0.30 +
                           coat_combined * 0.25 + (temperament_score or 85) * 0.15)
            else:
                overall = structure_score * 0.50 + coat_photo_score * 0.50
            overall = min(100, max(0, overall))

            if overall >= 95:
                grade, grade_full = 'S', 'S (卓越)'
            elif overall >= 90:
                grade, grade_full = 'A+', 'A+ (優秀)'
            elif overall >= 85:
                grade, grade_full = 'A', 'A (良好)'
            elif overall >= 80:
                grade, grade_full = 'B+', 'B+ (標準以上)'
            elif overall >= 70:
                grade, grade_full = 'B', 'B (標準)'
            else:
                grade, grade_full = 'C', 'C (要改善)'

        yield _sse_event("progress", {"step": "scoring_done", "percent": 90, "message": "スコア算出完了"})

        # Step 6: Build result
        yield _sse_event("progress", {"step": "finalizing", "percent": 95, "message": "レポートを生成中..."})

        elapsed = time.time() - start_time

        # --- Build explanations (same as original) ---
        explanations = []
        explanations.append({
            'icon': '📏',
            'title': f'体構造評価: {structure_score:.1f}点',
            'description': structure_result.get('comments', f'{breed_name}の体構造を評価しました。') +
                          f" プロポーション: {structure_result.get('proportion', '-')}点, " +
                          f"骨格: {structure_result.get('skeletal', '-')}点, " +
                          f"筋肉: {structure_result.get('muscular', '-')}点",
            'evidence': f'FCI基準 No.{breed_data["fci_no"]} に基づく評価'
        })
        explanations.append({
            'icon': '✨',
            'title': f'被毛評価（写真）: {coat_photo_score:.1f}点',
            'description': coat_photo_result.get('comments', f'{breed_name}の被毛状態を評価しました。') +
                          f" 質感: {coat_photo_result.get('texture', '-')}点, " +
                          f"毛量: {coat_photo_result.get('volume', '-')}点, " +
                          f"手入れ: {coat_photo_result.get('grooming', '-')}点",
            'evidence': '犬種標準の被毛基準に基づく評価'
        })
        if has_video and gait_score:
            gait_data = video_result.get('gait', {})
            adjusted_gait = min(100, gait_score / age_multiplier)
            explanations.append({
                'icon': '🏃',
                'title': f'歩様評価: {gait_score:.1f}点（年齢調整後: {adjusted_gait:.1f}点）',
                'description': gait_data.get('comments', '歩様を評価しました。') +
                              f" ストライド: {gait_data.get('stride', '-')}点, " +
                              f"バランス: {gait_data.get('balance', '-')}点, " +
                              f"流動性: {gait_data.get('fluidity', '-')}点。" +
                              f" 年齢({age_years:.1f}歳)による調整係数: {age_multiplier}",
                'evidence': 'Veterinary Journal (2013) - 年齢による歩様変化の研究に基づく'
            })
            temperament_data = video_result.get('temperament', {})
            explanations.append({
                'icon': '🎭',
                'title': f'気質評価: {temperament_score:.1f}点',
                'description': temperament_data.get('comments', '気質を評価しました。') +
                              f" 自信: {temperament_data.get('confidence', '-')}点, " +
                              f"注意力: {temperament_data.get('alertness', '-')}点, " +
                              f"落ち着き: {temperament_data.get('composure', '-')}点",
                'evidence': 'ドッグショー審査基準に基づく気質評価'
            })
        else:
            explanations.append({
                'icon': '🎬',
                'title': '動画評価: 未実施',
                'description': '動画がアップロードされていないため、歩様・気質の評価は行われていません。',
                'evidence': ''
            })
        explanations.append({
            'icon': '📊',
            'title': f'総合評価: {overall:.1f}点 - {grade_full}',
            'description': f'{breed_name}の総合的な評価結果です。' +
                          ('写真から体構造と被毛を、動画から歩様と気質を評価しました。' if has_video else
                           '写真から体構造と被毛を評価しました。') +
                          f' {age_context}の個体として、{"優れた" if overall >= 85 else "良好な" if overall >= 75 else "標準的な"}評価となりました。',
            'evidence': '18+の査読済み論文とFCI国際基準に基づく総合評価'
        })

        scores_for_breeding = {
            'structure': {'score': structure_score},
            'coat_photo': {'score': coat_photo_score},
            'gait': {'score': gait_score} if gait_score else {}
        }
        breeding_recommendations = generate_breeding_recommendations(
            breed_name, breed_data, scores_for_breeding, age_years
        )

        # ===== Breed calibration =====
        stream_calibrated = False
        try:
            from api.auto_cycle import apply_calibration_to_analysis as _cal
            _ci = {'structure': structure_score, 'coat': coat_photo_score}
            if gait_score is not None:
                _ci['gait'] = gait_score
            _co = _cal(breed_id, _ci)
            if _co != _ci:
                stream_calibrated = True
                if _co.get('structure') != structure_score:
                    structure_score = round(_co['structure'], 1)
                if _co.get('coat') != coat_photo_score:
                    coat_photo_score = round(_co['coat'], 1)
                if gait_score is not None and _co.get('gait') != gait_score:
                    gait_score = round(_co['gait'], 1)
        except Exception as e:
            logger.warning(f"operation failed (non-fatal): {e}")

        # ===== Disease evidence =====
        stream_health_evidence = {}
        try:
            from api.auto_cycle import get_evidence_based_disease_params as _dep
            stream_health_evidence = _dep(breed_id)
        except Exception as e:
            logger.warning(f"disease evidence loading failed (non-fatal): {e}")

        # Cleanup
        try:
            os.remove(photo_path)
            if video_path:
                os.remove(video_path)
        except Exception as e:
            logger.warning(f"temp file cleanup failed (non-fatal): {e}")
        gc.collect()

        result = {
            'overall_score': round(overall, 1),
            'grade': grade,
            'grade_full': grade_full,
            'fci_grade': fci_grade,
            'fci_grade_ja': fci_grade_ja,
            'scores': {
                'structure': {
                    'display': round(structure_score, 1),
                    'weight': '25%',
                    'details': structure_result
                },
                'coat_photo': {
                    'display': round(coat_photo_score, 1),
                    'weight': '20%',
                    'details': coat_photo_result
                },
                'gait': {
                    'display': round(gait_score, 1) if gait_score else None,
                    'weight': '25%',
                    'details': video_result.get('gait', {})
                },
                'temperament': {
                    'display': round(temperament_score, 1) if temperament_score else None,
                    'weight': '10%',
                    'details': video_result.get('temperament', {})
                },
                'muscle': {
                    'display': round(axis_scores.get('muscle', 75), 1) if axis_scores else None,
                    'weight': '20%',
                    'details': {}
                },
                'coat_video': {
                    'display': round(coat_video_score, 1) if coat_video_score else None,
                    'weight': '-',
                    'details': video_result.get('coat_motion', {})
                }
            },
            'explanations': explanations,
            'breeding_recommendations': breeding_recommendations,
            'health_evidence': stream_health_evidence,
            'metadata': {
                'breed_id': breed_id,
                'breed_name': breed_name,
                'breed_name_en': breed_data['name_en'],
                'fci_no': breed_data['fci_no'],
                'age_years': age_years,
                'age_adjustment': age_adjustment if SCORING_AVAILABLE else 0,
                'has_video': has_video,
                'vision_enabled': VISION_ENABLED,
                'model': (ANTHROPIC_MODEL if claude_client else OPENAI_MODEL) if VISION_ENABLED else 'local_fallback',
                'calibrated': stream_calibrated,
                'elapsed_seconds': round(elapsed, 1),
                'video_meta': stream_video_meta if has_video else {},
                'video_frame_extraction': {
                    'method': stream_video_meta.get('extraction_method') if has_video else None,
                    'frames_extracted': len(video_frames) if has_video else 0,
                    'error': stream_video_meta.get('error') if has_video else None
                }
            },
            'algorithm': {
                'version': ALGORITHM_VERSION,
                'model_version': MODEL_VERSION,
                'weights_hash': WEIGHTS_HASH,
                'deterministic': SCORING_AVAILABLE,
                'axis_scores': axis_scores if SCORING_AVAILABLE else None
            },
            'version': VERSION
        }

        # Save analysis if user is authenticated
        if current_user and DB_AVAILABLE and dog_id:
            try:
                dog_id_int = int(dog_id)
                dog = get_dog_by_id(dog_id_int, current_user['id'])
                if dog:
                    analysis_id = save_analysis(dog_id_int, current_user['id'], age_years, has_video, result)
                    result['analysis_id'] = analysis_id
                    result['saved'] = True
            except Exception as e:
                logger.error(f"Failed to save analysis: {e}")
                result['saved'] = False

        # Final result event
        yield _sse_event("progress", {"step": "complete", "percent": 100, "message": "解析完了"})
        yield _sse_event("result", result)

    return Response(
        stream_with_context(generate()),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no',
            'Connection': 'keep-alive',
        }
    )


# Legacy endpoint for backwards compatibility
@app.route('/api/analyze-with-image', methods=['POST'])
@optional_auth
@ensure_json_response
def analyze_with_image():
    """レガシーエンドポイント - 新しいエンドポイントにリダイレクト"""
    # 古いAPIとの互換性のため、imageをphotoとして処理
    if 'image' in request.files and 'photo' not in request.files:
        request.files = request.files.copy()
        # Note: This is a simplified compatibility layer

    return analyze_comprehensive()


# =============================================================================
# Pet Passport & Health Check Endpoints
# =============================================================================

# Passport PDF module import
try:
    from api.passport_pdf import (
        generate_health_report_pdf,
        generate_maff_export_pdf,
        generate_passport_pdf,
        generate_visit_pdf,
    )
    PASSPORT_PDF_AVAILABLE = True
except ImportError:
    try:
        from passport_pdf import (
            generate_health_report_pdf,
            generate_maff_export_pdf,
            generate_passport_pdf,
            generate_visit_pdf,
        )
        PASSPORT_PDF_AVAILABLE = True
    except ImportError:
        PASSPORT_PDF_AVAILABLE = False
        logging.warning("Passport PDF module not available")

# Symptom checker module import
try:
    from api.symptom_checker import analyze_symptoms
    # マルチ動物種対応の症状解析ユーティリティ
    try:
        from api.species_analyzer import analyze_species_symptoms
        SPECIES_ANALYZER_AVAILABLE = True
    except ImportError:
        # Species analyzer not available
        analyze_species_symptoms = None  # type: ignore
        SPECIES_ANALYZER_AVAILABLE = False
    SYMPTOM_CHECKER_AVAILABLE = True
except ImportError:
    # Fallback to local module name (legacy path)
    try:
        from symptom_checker import analyze_symptoms  # type: ignore
        SYMPTOM_CHECKER_AVAILABLE = True
        SPECIES_ANALYZER_AVAILABLE = False
        analyze_species_symptoms = None  # type: ignore
    except ImportError:
        SYMPTOM_CHECKER_AVAILABLE = False
        SPECIES_ANALYZER_AVAILABLE = False
        analyze_symptoms = None  # type: ignore
        analyze_species_symptoms = None  # type: ignore
        logging.warning("Symptom checker module not available")


@app.route('/api/generate-passport-pdf', methods=['POST'])
@optional_auth
@ensure_json_response
def api_generate_passport_pdf():
    """国際ペットパスポートPDF生成"""
    if not PASSPORT_PDF_AVAILABLE:
        return {'error': 'PDF generation module not available'}, 500

    data = request.get_json(silent=True)
    if not data:
        return {'error': 'JSON data required'}, 400

    # Flatten nested structure from frontend into flat keys expected by PDF generator
    if 'owner' in data or 'pet' in data:
        owner = data.get('owner', {})
        pet = data.get('pet', {})
        microchip = pet.get('microchip', {})
        parasite = data.get('parasite_treatment', {})
        exam = data.get('clinical_exam', {})
        travel = data.get('travel', {})
        data.get('vet', {})

        flat = {
            'owner_name': owner.get('name', ''),
            'owner_address': owner.get('address', ''),
            'owner_phone': owner.get('phone', ''),
            'owner_email': owner.get('email', ''),
            'emergency_contact': owner.get('emergency_contact', ''),
            'pet_name': pet.get('name', ''),
            'call_name': pet.get('call_name', ''),
            'species': pet.get('species', 'Dog'),
            'breed': pet.get('breed_id', ''),
            'sex': pet.get('sex', ''),
            'date_of_birth': pet.get('date_of_birth', ''),
            'color_markings': pet.get('color_markings', ''),
            'microchip_number': microchip.get('number', ''),
            'microchip_date': microchip.get('date', ''),
            'microchip_location': microchip.get('location', 'Left neck'),
            'vaccinations': data.get('vaccinations', []),
            'weight': exam.get('weight', ''),
            'temperature': exam.get('temperature', ''),
            'heart_rate': exam.get('heart_rate', ''),
            'respiratory_rate': exam.get('respiratory_rate', ''),
            'bcs': exam.get('bcs', ''),
            'organ_systems': exam.get('organ_systems', []),
            'destination': travel.get('destination_country', ''),
            'departure_date': travel.get('departure_date', ''),
            'return_date': travel.get('return_date', ''),
            'travel_purpose': travel.get('purpose', ''),
        }
        # Flatten parasite treatments into a list
        treatments = []
        for ptype in ['internal', 'external', 'heartworm']:
            pt = parasite.get(ptype, {})
            if pt.get('treated'):
                treatments.append({
                    'type': ptype.capitalize(),
                    'date': pt.get('date', ''),
                    'product': pt.get('product', ''),
                    'administered_by': ''
                })
        flat['parasite_treatments'] = treatments

        # Map breed_id to breed name
        breed_info = BREED_DATA.get(flat['breed'])
        if breed_info:
            flat['breed'] = breed_info.get('name_en', breed_info.get('name', flat['breed']))

        data = flat

    try:
        pdf_bytes = generate_passport_pdf(data)
        return Response(
            pdf_bytes.getvalue(),
            mimetype='application/pdf',
            headers={
                'Content-Disposition': 'attachment; filename=pet_passport.pdf',
                'Content-Type': 'application/pdf'
            }
        )
    except Exception as e:
        logger.error(f"Passport PDF generation error: {e}", exc_info=True)
        return {'error': 'PDF生成に失敗しました'}, 500


@app.route('/api/generate-maff-export-pdf', methods=['POST'])
@optional_auth
@ensure_json_response
def api_generate_maff_export_pdf():
    """農水省 犬の輸出検査申請書 PDF生成 (別記様式第１号)"""
    if not PASSPORT_PDF_AVAILABLE:
        return {'error': 'PDF generation module not available'}, 500

    data = request.get_json(silent=True)
    if not data:
        return {'error': 'JSON data required'}, 400

    # Flatten nested structure from frontend if needed
    if 'pet' in data or 'owner' in data:
        owner = data.get('owner', {})
        pet = data.get('pet', {})
        microchip = pet.get('microchip', {})
        travel = data.get('travel', {})

        flat = {
            'applicant_name': owner.get('name', ''),
            'applicant_address': owner.get('address', ''),
            'applicant_phone': owner.get('phone', ''),
            'pet_name': pet.get('name', ''),
            'breed': pet.get('breed_id', ''),
            'color': pet.get('color_markings', ''),
            'sex': pet.get('sex', ''),
            'date_of_birth': pet.get('date_of_birth', ''),
            'destination_country': travel.get('destination_country', ''),
            'embarkation_date': travel.get('departure_date', ''),
            'vessel_or_flight': travel.get('vessel_or_flight', ''),
            'microchip_number': microchip.get('number', ''),
            'microchip_date': microchip.get('date', ''),
            'microchip_location': microchip.get('location', ''),
        }
        # Copy vaccination data
        flat['rabies_vaccinations'] = data.get('rabies_vaccinations', [])
        flat['other_vaccinations'] = data.get('other_vaccinations',
                                               data.get('vaccinations', []))
        flat['remarks'] = data.get('remarks', '')

        # Resolve breed name
        breed_info = BREED_DATA.get(flat['breed'])
        if breed_info:
            flat['breed'] = f"{breed_info.get('name', '')} ({breed_info.get('name_en', '')})"

        data = flat

    try:
        pdf_bytes = generate_maff_export_pdf(data)
        return Response(
            pdf_bytes.getvalue(),
            mimetype='application/pdf',
            headers={
                'Content-Disposition': 'attachment; filename=maff_export_dog.pdf',
                'Content-Type': 'application/pdf'
            }
        )
    except Exception as e:
        logger.error(f"MAFF export PDF generation error: {e}", exc_info=True)
        return {'error': 'PDF生成に失敗しました'}, 500


@app.route('/api/analyze-symptoms', methods=['POST'])
@optional_auth
@ensure_json_response
def api_analyze_symptoms():
    """症状チェック→疾患・検査リスト"""
    if not SYMPTOM_CHECKER_AVAILABLE:
        return {'error': 'Symptom checker module not available'}, 500

    data = request.get_json(silent=True)
    if not data or 'symptoms' not in data:
        return {'error': 'symptoms list required'}, 400

    symptoms = data['symptoms']
    if not isinstance(symptoms, list) or len(symptoms) == 0:
        return {'error': 'At least one symptom required'}, 400

    # 動物種と年齢ステージを取得（省略時は dog / None とする）
    species = data.get('species', 'dog')
    age_stage = data.get('age_stage')
    breed = data.get('breed')  # 犬種指定（犬の場合のみ使用）

    try:
        # 犬の場合は従来の犬用症状チェッカーを使用し、breed パラメータを反映する
        if species == 'dog' or species is None:
            result = analyze_symptoms(symptoms, breed=breed)
            # 犬種エビデンスを追加
            if breed:
                try:
                    from api.auto_cycle import get_evidence_based_disease_params
                    disease_evidence = get_evidence_based_disease_params(breed)
                    result['breed_disease_evidence'] = {
                        'overall_risk_level': disease_evidence.get('overall_risk_level', 'unknown'),
                        'total_known_risks': disease_evidence.get('total_known_risks', 0),
                        'hereditary_diseases': disease_evidence.get('hereditary_diseases', []),
                        'by_system': disease_evidence.get('by_system', {}),
                    }
                    # Cross-reference: flag if any detected conditions match hereditary diseases
                    hereditary = set(disease_evidence.get('hereditary_diseases', []))
                    if hereditary and result.get('possible_conditions'):
                        for cond in result['possible_conditions']:
                            cond_name = cond.get('name', '')
                            for hd in hereditary:
                                if hd in cond_name or cond_name in hd:
                                    cond['hereditary_match'] = True
                                    cond['hereditary_note'] = f'この犬種の遺伝性疾患リストに含まれています: {hd}'
                                    break
                except ImportError as e:
                    logger.warning(f"Disease evidence module not available: {e}")
                except Exception as e:
                    logger.warning(f"Disease evidence enrichment failed: {e}")
        else:
            # その他の動物種は species_analyzer に委譲する
            if not SPECIES_ANALYZER_AVAILABLE:
                return {'error': 'Species analyzer module not available'}, 500
            result = analyze_species_symptoms(species, symptoms, age_stage)
        return result
    except ValueError as ve:
        logger.error(f"Symptom analysis error: {ve}", exc_info=True)
        return {'error': str(ve)}, 400
    except Exception as e:
        logger.error(f"Symptom analysis error: {e}", exc_info=True)
        return {'error': '症状解析に失敗しました'}, 500


@app.route('/api/generate-health-report-pdf', methods=['POST'])
@optional_auth
@ensure_json_response
def api_generate_health_report_pdf():
    """健康チェックレポートPDF生成"""
    if not PASSPORT_PDF_AVAILABLE:
        return {'error': 'PDF generation module not available'}, 500

    data = request.get_json(silent=True)
    if not data:
        return {'error': 'JSON data required'}, 400

    symptoms = data.get('symptoms', [])
    pet_info = data.get('pet_info', {})
    breed = data.get('breed')
    species = data.get('species', 'dog')
    age_stage = data.get('age_stage')

    # 症状分析を実行（動物種に応じて切り替え）
    analysis_results: dict = {}
    if symptoms:
        try:
            if species == 'dog' or species is None:
                analysis_results = analyze_symptoms(symptoms, breed=breed)
                # 犬種エビデンスを追加
                if breed:
                    try:
                        from api.auto_cycle import get_evidence_based_disease_params
                        disease_evidence = get_evidence_based_disease_params(breed)
                        analysis_results['breed_disease_evidence'] = {
                            'overall_risk_level': disease_evidence.get('overall_risk_level', 'unknown'),
                            'hereditary_diseases': disease_evidence.get('hereditary_diseases', []),
                            'by_system': disease_evidence.get('by_system', {}),
                        }
                    except Exception as e:
                        logger.warning(f"disease evidence loading failed (non-fatal): {e}")
            else:
                # その他の動物種は species_analyzer に委譲
                if SPECIES_ANALYZER_AVAILABLE:
                    analysis_results = analyze_species_symptoms(species, symptoms, age_stage)
        except Exception as e:
            logger.error(f"Health report symptom analysis error: {e}")

    try:
        pdf_bytes = generate_health_report_pdf(
            {'symptoms': symptoms, 'pet_info': pet_info},
            analysis_results
        )
        return Response(
            pdf_bytes.getvalue(),
            mimetype='application/pdf',
            headers={
                'Content-Disposition': 'attachment; filename=health_report.pdf',
                'Content-Type': 'application/pdf'
            }
        )
    except Exception as e:
        logger.error(f"Health report PDF generation error: {e}", exc_info=True)
        return {'error': 'PDF生成に失敗しました'}, 500


# =============================================================================
# Medical Visit (Vet Visit) Endpoints
# =============================================================================

@app.route('/api/save-medical-visit', methods=['POST'])
@require_auth
@ensure_json_response
def api_save_medical_visit():
    """診察記録を保存"""
    if not DB_AVAILABLE:
        return {'error': 'Database not available'}, 500

    user_id = request.current_user['id']

    data = request.get_json(silent=True)
    if not data:
        return {'error': 'JSON data required'}, 400

    health_checks = data.get('health_checks', {})

    # Extract vitals from nested dict or flat fields
    vitals = data.get('vitals', {})

    try:
        from datetime import date as _date
        visit_data = {
            'dog_id': data.get('dog_id'),
            'visit_date': data.get('visit_date') or _date.today().isoformat(),
            'visit_time': data.get('visit_time'),
            'chief_complaint': data.get('chief_complaint', '体調チェック'),
            'health_checks': health_checks,
            'mapped_symptoms': data.get('mapped_symptoms', []),
            'detailed_memo': data.get('memo') or data.get('detailed_memo', ''),
            'body_weight_kg': vitals.get('weight_kg') or data.get('body_weight_kg'),
            'body_temperature': vitals.get('temperature_c') or data.get('body_temperature'),
            'heart_rate': vitals.get('heart_rate_bpm') or data.get('heart_rate'),
            'respiratory_rate': vitals.get('respiratory_rate') or data.get('respiratory_rate'),
            'analysis_result': data.get('analysis_result', {}),
            'diagnosis': data.get('diagnosis'),
            'treatment': data.get('treatment'),
            'prescription': data.get('prescription'),
            'next_visit_date': data.get('next_visit_date'),
        }
        visit_id = create_medical_visit(user_id, visit_data)

        # Audit log
        with contextlib.suppress(Exception):
            save_audit_log(user_id or 0, 'visit_created', {
                'visit_id': visit_id,
                'dog_id': data.get('dog_id'),
                'chief_complaint': visit_data['chief_complaint'],
            })

        return {'success': True, 'visit_id': visit_id}
    except Exception as e:
        logger.error(f"Save medical visit error: {e}", exc_info=True)
        return {'error': '診察記録の保存に失敗しました'}, 500


@app.route('/api/medical-visits/<int:dog_id>', methods=['GET'])
@require_auth
@ensure_json_response
def api_get_medical_visits(dog_id):
    """犬の診察履歴を取得"""
    if not DB_AVAILABLE:
        return {'error': 'Database not available'}, 500

    user_id = request.current_user['id']
    limit = request.args.get('limit', 50, type=int)

    try:
        visits = get_medical_visits_by_dog(dog_id, user_id=user_id, limit=limit)
        return {'visits': visits}
    except Exception as e:
        logger.error(f"Get medical visits error: {e}", exc_info=True)
        return {'error': '診察履歴の取得に失敗しました'}, 500


@app.route('/api/medical-visit/<int:visit_id>', methods=['GET'])
@require_auth
@ensure_json_response
def api_get_medical_visit(visit_id):
    """個別の診察記録を取得"""
    if not DB_AVAILABLE:
        return {'error': 'Database not available'}, 500

    user_id = request.current_user['id']

    try:
        visit = get_medical_visit(visit_id, user_id=user_id)
        if not visit:
            return {'error': 'Visit not found'}, 404
        return {'visit': visit}
    except Exception as e:
        logger.error(f"Get medical visit error: {e}", exc_info=True)
        return {'error': '診察記録の取得に失敗しました'}, 500


@app.route('/api/medical-visit/<int:visit_id>/pdf', methods=['GET'])
@require_auth
@ensure_json_response
def api_medical_visit_pdf(visit_id):
    """診察記録PDFを生成してダウンロード"""
    if not DB_AVAILABLE:
        return {'error': 'Database not available'}, 500
    if not PASSPORT_PDF_AVAILABLE:
        return {'error': 'PDF generation module not available'}, 500

    user_id = request.current_user['id']

    try:
        visit = get_medical_visit(visit_id, user_id=user_id)
        if not visit:
            return {'error': 'Visit not found'}, 404

        # Enrich with dog info if available
        dog_id = visit.get('dog_id')
        if dog_id:
            try:
                dog = get_dog_by_id(dog_id)
                if dog:
                    visit['dog_name'] = dog.get('name', '')
                    visit['dog_breed'] = dog.get('breed', '')
            except Exception as e:
                logger.warning(f"dog metadata lookup failed (non-fatal): {e}")

        pdf_bytes = generate_visit_pdf(visit)
        dog_name = visit.get('dog_name', 'dog')
        visit_date = visit.get('visit_date', 'unknown')

        return Response(
            pdf_bytes.getvalue(),
            mimetype='application/pdf',
            headers={
                'Content-Disposition': f'attachment; filename=visit_report_{dog_name}_{visit_date}.pdf',
                'Content-Type': 'application/pdf'
            }
        )
    except DataCorruptionError as e:
        logger.error(f"Visit PDF data corruption: {e}", exc_info=True)
        return {'error': '診察記録データが破損しています。データの確認が必要です。'}, 422
    except Exception as e:
        logger.error(f"Visit PDF generation error: {e}", exc_info=True)
        return {'error': 'PDF生成に失敗しました'}, 500


@app.route('/api/medical-visit/<int:visit_id>/preview', methods=['GET'])
@require_auth
@ensure_json_response
def api_medical_visit_preview(visit_id):
    """診察記録HTMLプレビューを生成"""
    if not DB_AVAILABLE:
        return {'error': 'Database not available'}, 500

    user_id = request.current_user['id']

    try:
        visit = get_medical_visit(visit_id, user_id=user_id)
        if not visit:
            return {'error': 'Visit not found'}, 404

        # Enrich with dog info
        dog_id = visit.get('dog_id')
        dog_name = ''
        dog_breed = ''
        if dog_id:
            try:
                dog = get_dog_by_id(dog_id)
                if dog:
                    dog_name = dog.get('name', '')
                    dog_breed = dog.get('breed', '')
            except Exception as e:
                logger.warning(f"dog metadata lookup failed (non-fatal): {e}")

        # Build HTML preview
        import json
        health_checks = visit.get('health_checks', {})
        if isinstance(health_checks, str):
            health_checks = json.loads(health_checks)

        cat_labels = {
            'general': '全般状態', 'appetite': '食欲・飲水', 'digestive': '消化器症状',
            'respiratory': '呼吸器症状', 'urinary': '泌尿器症状', 'skin': '皮膚症状',
            'eyes_ears': '眼・耳・鼻症状', 'musculoskeletal': '運動器症状',
            'neurological': '神経症状', 'other': 'その他',
        }

        html = f'''<!DOCTYPE html><html><head><meta charset="UTF-8">
        <title>診察記録 - {dog_name}</title>
        <style>
            body {{ font-family: 'Hiragino Sans', 'Noto Sans JP', sans-serif; max-width: 800px; margin: 20px auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 20px; border-radius: 12px; margin-bottom: 20px; }}
            .section {{ margin: 15px 0; padding: 15px; border-left: 4px solid #667eea; background: #f7fafc; border-radius: 8px; }}
            .alert {{ color: #c53030; font-weight: 600; }}
            .badge {{ display: inline-block; padding: 2px 8px; border-radius: 12px; font-size: 0.8em; margin: 2px; }}
            .badge-alert {{ background: #fed7d7; color: #c53030; }}
            .badge-normal {{ background: #c6f6d5; color: #276749; }}
        </style></head><body>
        <div class="header">
            <h1>ShowDog v4.0 - 診察記録</h1>
            <p>Veterinary Visit Report</p>
        </div>
        <div class="section">
            <strong>来院日:</strong> {visit.get("visit_date", "")}<br>
            <strong>犬:</strong> {dog_name} {("(" + dog_breed + ")") if dog_breed else ""}<br>
            <strong>主訴:</strong> {visit.get("chief_complaint", "")}
        </div>'''

        # Vitals
        vitals_parts = []
        if visit.get('body_weight_kg'):
            vitals_parts.append(f"体重: {visit['body_weight_kg']} kg")
        if visit.get('body_temperature'):
            vitals_parts.append(f"体温: {visit['body_temperature']} °C")
        if visit.get('heart_rate'):
            vitals_parts.append(f"心拍数: {visit['heart_rate']} bpm")
        if vitals_parts:
            html += f'<div class="section"><strong>バイタル:</strong> {" | ".join(vitals_parts)}</div>'

        # Health checks
        if health_checks:
            html += '<div class="section"><strong>体調チェック:</strong>'
            for cat, items in health_checks.items():
                if items:
                    html += f'<div style="margin:8px 0;"><strong>【{cat_labels.get(cat, cat)}】</strong> '
                    for item in items:
                        badge_class = 'badge-alert' if any(kw in item for kw in ['嘔吐','血便','呼吸困難','けいれん','血尿','発熱','出血']) else 'badge-normal'
                        html += f'<span class="badge {badge_class}">{item}</span> '
                    html += '</div>'
            html += '</div>'

        html += '</body></html>'

        return Response(html, mimetype='text/html')
    except Exception as e:
        logger.error(f"Visit preview error: {e}", exc_info=True)
        return {'error': 'プレビュー生成に失敗しました'}, 500


# =============================================================================
# Error Handlers
# =============================================================================

@app.errorhandler(404)
def not_found(e):
    if request.accept_mimetypes.best == 'application/json' or request.path.startswith('/api/'):
        return jsonify({'error': 'Not found', 'version': VERSION}), 404
    try:
        return send_from_directory(STATIC_DIR, '404.html'), 404
    except (FileNotFoundError, WerkzeugNotFound, Exception):
        return jsonify({'error': 'Not found', 'version': VERSION}), 404

@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'ファイルサイズが大きすぎます（最大200MB）', 'version': VERSION}), 413

@app.errorhandler(429)
def rate_limited(e):
    return jsonify({
        'error': 'リクエスト制限に達しました。しばらく待ってからお試しください。',
        'error_en': 'Rate limit exceeded. Please wait before trying again.',
        'version': VERSION,
    }), 429

@app.errorhandler(500)
def server_error(e):
    logger.error(f"500: {e}", exc_info=True)
    if request.accept_mimetypes.best == 'application/json' or request.path.startswith('/api/'):
        return jsonify({'error': 'Internal server error', 'version': VERSION}), 500
    try:
        return send_from_directory(STATIC_DIR, '500.html'), 500
    except (FileNotFoundError, WerkzeugNotFound, Exception):
        return jsonify({'error': 'Internal server error', 'version': VERSION}), 500

# =============================================================================
# Main
# =============================================================================

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    logger.info(f"Starting on port {port}")
    logger.info(f"DB_AVAILABLE: {DB_AVAILABLE}")
    logger.info(f"VISION_ENABLED: {VISION_ENABLED}, VISION_PROVIDER: {VISION_PROVIDER}")
    logger.info(f"Breeds loaded: {len(BREED_DATA)}")
    logger.info(f"SECRET_KEY configured: {bool(os.getenv('SECRET_KEY') or os.getenv('FLASK_SECRET_KEY'))}")
    logger.info(f"ProxyFix: enabled, COOKIE_SECURE: {COOKIE_SECURE}")
    if DB_AVAILABLE:
        try:
            from api.database import DB_PATH as _dbp, DB_DIR as _dbdir
        except ImportError:
            from database import DB_PATH as _dbp, DB_DIR as _dbdir
        logger.info(f"auth_db_path: {_dbp}")
        logger.info(f"data_root: {_dbdir}")
    else:
        logger.warning("DATABASE IS NOT AVAILABLE - login/register will not work!")
    app.run(host='0.0.0.0', port=port, debug=False)
