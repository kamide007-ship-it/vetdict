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
import gzip
import logging
import os
import secrets
from functools import wraps
from pathlib import Path

from flask import Flask, Response, g, jsonify, redirect, render_template, request, send_from_directory, url_for
from flask_cors import CORS
from werkzeug.exceptions import NotFound as WerkzeugNotFound

from api.auth import ClientIP, RateLimiter, require_internal_api_access
from api.debug_config import is_debug_mode_enabled

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
VERSION = "5.0.0"
BUILD = "2026-03-07"
RATE_LIMIT_ERROR_MESSAGE = "リクエスト制限に達しました。"

# ---------------------------------------------------------------------------
# Flask App
# ---------------------------------------------------------------------------
app = Flask(__name__, static_folder=None, template_folder=str(Path(__file__).resolve().parent.parent / "templates"))
app.config["DEBUG"] = is_debug_mode_enabled()
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB
# UTF-8 JSONをそのまま返す（日本語を\uXXXXにエスケープしない）。
# 日本語が多いレスポンスのペイロードを約25%削減する。
app.json.ensure_ascii = False
_secret = os.getenv("SECRET_KEY") or os.getenv("FLASK_SECRET_KEY")
if not _secret:
    if is_debug_mode_enabled():
        _secret = "dev-only-insecure-key"
        logger.warning("SECRET_KEY not set — using insecure default (debug mode only)")
    else:
        raise RuntimeError(
            "SECRET_KEY environment variable is required in production. "
            "Set SECRET_KEY or FLASK_SECRET_KEY before starting the application."
        )
app.secret_key = _secret
app.VERSION = VERSION  # Make VERSION available to decorators

_allowed_origins = os.getenv("CORS_ALLOWED_ORIGINS", "").strip()
if _allowed_origins:
    CORS(app, resources={r"/api/*": {"origins": _allowed_origins.split(",")}})
elif is_debug_mode_enabled():
    CORS(app)
    logger.warning("CORS_ALLOWED_ORIGINS not set — allowing all origins (debug mode only)")
else:
    CORS(app, resources={r"/api/*": {"origins": ["https://vetdict.info"]}})

ROOT_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = str(ROOT_DIR / "templates")
STATIC_DIR = str(ROOT_DIR / "static")


def _compute_asset_version() -> str:
    """Content hash of the main JS/CSS bundles, appended as ``?v=`` to asset
    URLs so a code change automatically busts the browser/CDN cache. Falls back
    to ``VERSION`` if the files cannot be read."""
    import hashlib

    h = hashlib.sha1()
    for rel in ("js/app.js", "css/main.css"):
        try:
            h.update((ROOT_DIR / "static" / rel).read_bytes())
        except OSError:
            return VERSION
    return f"{VERSION}-{h.hexdigest()[:8]}"


ASSET_VERSION = _compute_asset_version()

# ---------------------------------------------------------------------------
# Public API rate limiter (prevents abuse of compute-heavy endpoints)
# ---------------------------------------------------------------------------
_public_rate_limiter = RateLimiter(
    max_requests=int(os.getenv("PUBLIC_API_RATE_LIMIT", "60")),
    window_seconds=60,
)
_public_client_ip = ClientIP()


def _check_public_rate_limit():
    """Return a 429 response tuple if rate-limited, else None."""
    client_ip = _public_client_ip.get_client_ip()
    if _public_rate_limiter.is_limited(client_ip):
        return (
            jsonify(
                {
                    "error": "Rate limit exceeded. Please wait before retrying.",
                    "error_ja": "リクエスト制限に達しました。しばらくしてから再試行してください。",
                }
            ),
            429,
        )
    return None


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

# Content quality enrichment (completeness score + literature citations)
try:
    from api.content_quality import enrich_disease_content
except ImportError:
    try:
        from content_quality import enrich_disease_content
    except ImportError:
        enrich_disease_content = None
        logger.warning("Content quality module not available — diagnosis results will not carry citations")

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
        return None, {"error": f"{field_name} must be a list of strings"}, 400

    normalized_values = []
    for value in values:
        if not isinstance(value, str):
            return None, {"error": f"{field_name} must contain only strings"}, 400
        normalized_value = value.strip()
        if normalized_value:
            normalized_values.append(normalized_value)

    if require_non_empty and not normalized_values:
        item_name = singular_name or field_name
        return None, {"error": f"At least one {item_name} required"}, 400

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

# Anesthesia protocols blueprint
try:
    from api.anesthesia_api import anesthesia_bp

    app.register_blueprint(anesthesia_bp)
except ImportError:
    logger.warning("Anesthesia protocols module not available")

# Emergency protocols blueprint (Vetlexicon-style quick reference)
try:
    from api.emergency_api import emergency_bp

    app.register_blueprint(emergency_bp)
except ImportError:
    logger.warning("Emergency protocols module not available")

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
            if hasattr(result, "status_code"):
                return result
            if isinstance(result, tuple):
                body = result[0]
                status = result[1] if len(result) > 1 else 200
                if isinstance(body, dict):
                    body.setdefault("success", status < 400)
                    body.setdefault("version", VERSION)
                    resp = jsonify(body)
                    resp.status_code = status
                    return resp
                return result
            if isinstance(result, dict):
                result.setdefault("success", True)
                result.setdefault("version", VERSION)
                return jsonify(result)
            return result
        except Exception as e:
            logger.error("Error in %s: %s", f.__name__, e, exc_info=True)
            is_production = os.getenv("RENDER") or os.getenv("PRODUCTION")
            error_msg = "エラーが発生しました。しばらくしてからもう一度お試しください。" if is_production else str(e)
            return jsonify({"success": False, "error": error_msg, "version": VERSION}), 500

    return wrapper


# ---------------------------------------------------------------------------
# Security headers
# ---------------------------------------------------------------------------


@app.before_request
def generate_csp_nonce():
    """Generate a per-request nonce kept for template <script> tags.

    The nonce is no longer referenced in the CSP header (we use
    'unsafe-inline' + host allowlists instead so GA4 inline event
    handlers are not blocked), but templates still carry
    ``nonce="{{ g.csp_nonce }}"`` on their ``<script>`` tags for
    forward-compatibility if we re-enable nonce-based CSP later.
    """
    g.csp_nonce = secrets.token_urlsafe(16)
    g.asset_ver = ASSET_VERSION


@app.after_request
def add_headers(response):
    """Add security headers to all responses."""
    # Content security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    # Use DENY to align with CSP frame-ancestors 'none' (we never embed our own
    # pages in frames). SAMEORIGIN here contradicted the stricter CSP directive.
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"

    # Content Security Policy (prevent XSS, clickjacking, etc.)
    # Note: nonce + 'unsafe-inline' causes browsers to ignore 'unsafe-inline'
    # (CSP Level 2 spec), and 'strict-dynamic' causes host allowlists to be
    # ignored.  GA4/GTM injects inline event handlers that cannot carry a nonce,
    # so we use 'unsafe-inline' + explicit host allowlists without nonce/
    # strict-dynamic to avoid blocking GA tracking after diagnosis events.
    response.headers["Content-Security-Policy"] = (
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
    is_production = os.getenv("RENDER") or os.getenv("PRODUCTION")
    if is_production:
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"

    # Remove server version disclosure
    response.headers.pop("Server", None)
    response.headers.pop("X-Powered-By", None)

    # Cache policy: API responses are never cached; static files are revalidated
    path = request.path or ""
    if path.startswith("/api/") or path == "/":
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    elif path.startswith("/static/"):
        # Immutable assets (SW handles revalidation): cache for 7 days
        if any(path.endswith(ext) for ext in (".css", ".js", ".svg", ".png", ".woff2")):
            response.headers["Cache-Control"] = "public, max-age=604800, stale-while-revalidate=86400"
        else:
            response.headers.setdefault("Cache-Control", "public, max-age=3600, must-revalidate")

    return response


_COMPRESSIBLE_TYPES = frozenset(
    {
        "application/json",
        "application/javascript",
        "text/javascript",
        "text/html",
        "text/css",
        "text/plain",
        "image/svg+xml",
        "application/xml",
        "text/xml",
    }
)
_COMPRESS_MIN_BYTES = 1024


@app.after_request
def compress_response(response):
    """大きめのテキスト/JSONレスポンスをgzip圧縮する（依存追加なし）。

    日本語を多く含むJSON（薬品辞書・麻酔プロトコル・疾患DB）や app.js /
    main.css などの転送量を大幅に削減し、モバイル回線でのUXを改善する。
    クライアントが gzip を受け入れる場合のみ、未圧縮の 2xx テキスト応答に適用。
    """
    try:
        if "gzip" not in request.headers.get("Accept-Encoding", "").lower():
            return response
        if not (200 <= response.status_code < 300):
            return response
        if response.headers.get("Content-Encoding"):
            return response
        ctype = (response.content_type or "").split(";", 1)[0].strip().lower()
        if ctype not in _COMPRESSIBLE_TYPES:
            return response
        # 静的ファイル等の passthrough 応答はサイズが判明していて妥当な場合のみ
        # バッファリングして圧縮する（巨大/ストリーミング応答は素通し）。
        if response.direct_passthrough:
            length = response.content_length
            if length is None or length > 5 * 1024 * 1024:
                return response
            response.direct_passthrough = False
        data = response.get_data()
        if len(data) < _COMPRESS_MIN_BYTES:
            return response
        compressed = gzip.compress(data, compresslevel=6)
        if len(compressed) >= len(data):
            return response
        response.set_data(compressed)
        response.headers["Content-Encoding"] = "gzip"
        response.headers["Content-Length"] = str(len(compressed))
        vary = response.headers.get("Vary")
        if not vary:
            response.headers["Vary"] = "Accept-Encoding"
        elif "accept-encoding" not in vary.lower():
            response.headers["Vary"] = f"{vary}, Accept-Encoding"
    except Exception:
        logger.exception("response compression failed; sending uncompressed")
    return response


# =============================================================================
# Static Files
# =============================================================================


@app.route("/")
def index():
    try:
        return render_template("index.html")
    except Exception:
        return jsonify({"error": "index.html not found"}), 404


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/tokushoho")
def tokushoho():
    return render_template("tokushoho.html")


@app.route("/favicon.ico")
def favicon():
    try:
        return send_from_directory(STATIC_DIR, "favicon.ico")
    except (FileNotFoundError, WerkzeugNotFound):
        try:
            return send_from_directory(TEMPLATES_DIR, "favicon.ico")
        except (FileNotFoundError, WerkzeugNotFound):
            return "", 204


@app.route("/static/<path:filename>")
def static_assets(filename):
    try:
        return send_from_directory(STATIC_DIR, filename)
    except (FileNotFoundError, WerkzeugNotFound):
        return jsonify({"error": f"{filename} not found"}), 404


import re as _re

# Module-level constants for disease page routing (used by sitemap, hub, index, detail)
_DISEASE_MODULES: dict[str, str] = {
    "dog": "api.species.dog_diseases",
    "cat": "api.species.cat_diseases",
    "horse": "api.species.equine_diseases",
    "rabbit": "api.species.rabbit_diseases",
    "hamster": "api.species.hamster_diseases",
    "guinea_pig": "api.species.guinea_pig_diseases",
    "chinchilla": "api.species.chinchilla_diseases",
    "ferret": "api.species.ferret_diseases",
    "hedgehog": "api.species.hedgehog_diseases",
    "sugar_glider": "api.species.sugar_glider_diseases",
    "degu": "api.species.degu_diseases",
    "bird": "api.species.bird_diseases",
    "parakeet": "api.species.parakeet_diseases",
    "parrot": "api.species.parrot_diseases",
    "reptile": "api.species.reptile_diseases",
    "tortoise": "api.species.tortoise_diseases",
    "snake": "api.species.snake_diseases",
    "lizard": "api.species.lizard_diseases",
    "amphibian": "api.species.amphibian_diseases",
    "fish": "api.species.fish_diseases",
    "exotic_other": "api.species.exotic_other_diseases",
}

_SPECIES_ICONS: dict[str, str] = {
    "dog": "\U0001f415",
    "cat": "\U0001f408",
    "horse": "\U0001f434",
    "rabbit": "\U0001f407",
    "hamster": "\U0001f439",
    "guinea_pig": "\U0001f439",
    "chinchilla": "\U0001f43f\ufe0f",
    "ferret": "\U0001f9a1",
    "hedgehog": "\U0001f994",
    "sugar_glider": "\U0001f43f\ufe0f",
    "degu": "\U0001f42d",
    "bird": "\U0001f426",
    "parakeet": "\U0001f99c",
    "parrot": "\U0001f99c",
    "reptile": "\U0001f98e",
    "tortoise": "\U0001f422",
    "snake": "\U0001f40d",
    "lizard": "\U0001f98e",
    "amphibian": "\U0001f438",
    "fish": "\U0001f41f",
    "exotic_other": "\U0001f999",
}


def _load_diseases(species_key: str) -> list:
    """Load DISEASES list for a species from its Python module."""
    mod_name = _DISEASE_MODULES.get(species_key)
    if not mod_name:
        return []
    try:
        import importlib

        mod = importlib.import_module(mod_name)
        raw = getattr(mod, "DISEASES", getattr(mod, "DISEASE_DATABASE", []))
        try:
            from api.species.helpers import dedupe_disease_list

            result = dedupe_disease_list(raw)
        except ImportError:
            return raw
        # Apply the non-destructive canonical consolidation map (T103), if any.
        try:
            from api.species.canonical import apply_canonical_map

            result = apply_canonical_map(result, species_key)
        except ImportError:
            pass
        return result
    except ImportError:
        return []


def _disease_slug(disease) -> str:
    """Generate a URL-safe slug from a disease dict or dataclass."""
    if isinstance(disease, dict):
        name = disease.get("name", "") or disease.get("name_en", "")
    else:
        name = getattr(disease, "name", "") or getattr(disease, "name_en", "")
    return _re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def _disease_get(disease, key, default=""):
    """Get attribute from disease dict or dataclass."""
    if isinstance(disease, dict):
        val = disease.get(key, default)
        # Fallback: "name" -> "name_en" for species using name_en (e.g. equine)
        if not val and key == "name":
            val = disease.get("name_en", default)
        return val
    val = getattr(disease, key, default)
    if not val and key == "name":
        val = getattr(disease, "name_en", default)
    return val


@app.route("/sitemap.xml")
def dynamic_sitemap():
    """Generate a dynamic sitemap including all species and feature pages."""
    from api.disease_store import SPECIES_META

    base = "https://vetdict.info"
    urls = [
        (f"{base}/", "weekly", "1.0"),
        (f"{base}/#checker", "weekly", "0.9"),
        (f"{base}/#database", "weekly", "0.9"),
        (f"{base}/diseases", "weekly", "0.9"),
        (f"{base}/drugs", "weekly", "0.9"),
        (f"{base}/anesthesia", "weekly", "0.8"),
        (f"{base}/symptoms", "weekly", "0.8"),
        (f"{base}/#chat", "weekly", "0.8"),
        (f"{base}/#drugs", "monthly", "0.8"),
    ]
    # Species-specific pages
    for sp in SPECIES_META:
        urls.append((f"{base}/?species={sp}#checker", "weekly", "0.7"))
        urls.append((f"{base}/?species={sp}#database", "weekly", "0.7"))
        urls.append((f"{base}/diseases/{sp}", "weekly", "0.8"))  # Disease index per species
        urls.append((f"{base}/symptoms/{sp}", "weekly", "0.6"))  # Symptom index per species

    # Disease detail pages (SEO: each disease = a crawlable page)
    for sp in _DISEASE_MODULES:
        if sp not in SPECIES_META:
            continue
        try:
            for _d in _load_diseases(sp):
                _slug = _disease_slug(_d)
                if _slug:
                    urls.append((f"{base}/diseases/{sp}/{_slug}", "monthly", "0.5"))
        except ImportError:
            pass

    # Symptom detail pages (SEO: each symptom = a crawlable disease-listing page)
    for sp in _DISEASE_MODULES:
        if sp not in SPECIES_META:
            continue
        try:
            _sym_names = _symptom_names_for_species(sp)
            _used = set()
            for _d in _load_diseases(sp):
                _used |= _disease_symptom_ids(_d)
            for _sid in _used & set(_sym_names.keys()):
                urls.append((f"{base}/symptoms/{sp}/{_sid}", "monthly", "0.4"))
        except ImportError:
            pass

    # Drug detail pages (SEO: each drug = a crawlable page)
    try:
        from api.drug_dictionary import DRUGS as _ALL_DRUGS

        for _dr in _ALL_DRUGS:
            _did = _dr.get("id", "")
            if _did:
                urls.append((f"{base}/drugs/{_did}", "monthly", "0.5"))
    except ImportError:
        pass

    # Anesthesia / sedation protocol pages (per species)
    try:
        from api.anesthesia_protocols import ANESTHESIA_PROTOCOLS as _AP

        for _sp in _AP:
            urls.append((f"{base}/anesthesia/{_sp}", "monthly", "0.6"))
    except ImportError:
        pass

    # Legal pages
    for page in ("terms", "privacy", "tokushoho"):
        urls.append((f"{base}/{page}", "monthly", "0.3"))

    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, freq, priority in urls:
        lines.append(f"  <url><loc>{loc}</loc><changefreq>{freq}</changefreq><priority>{priority}</priority></url>")
    lines.append("</urlset>")

    return Response("\n".join(lines), mimetype="application/xml")


@app.route("/diseases/search")
def diseases_search():
    """Cross-species disease search page."""
    from api.disease_store import SPECIES_META

    query = request.args.get("q", "").strip()
    if not query or len(query) < 2:
        return render_template(
            "diseases_search.html",
            query=query,
            results=[],
            total_results=0,
            searched=bool(query),
        )

    q_lower = query.lower()
    results = []
    for sp_id in _DISEASE_MODULES:
        if sp_id not in SPECIES_META:
            continue
        meta = SPECIES_META[sp_id]
        sp_name_ja = meta.get("name_ja", sp_id)
        sp_name_en = meta.get("name_en", sp_id.title())
        icon = _SPECIES_ICONS.get(sp_id, "\U0001f43e")
        diseases = _load_diseases(sp_id)
        matches = []
        for d in diseases:
            if isinstance(d, dict):
                name = d.get("name", "") or ""
                name_ja = d.get("name_ja", "") or ""
                desc = d.get("description", "") or ""
                urgency = d.get("urgency", "")
            else:
                name = getattr(d, "name", "") or ""
                name_ja = getattr(d, "name_ja", "") or ""
                desc = getattr(d, "description", "") or ""
                urgency = getattr(d, "urgency", "")
            if q_lower in name.lower() or q_lower in name_ja.lower():
                slug = _disease_slug(d)
                if slug:
                    cat = _classify_disease_dict({"name": name, "name_ja": name_ja, "description": desc})
                    cat_ja = _DISEASE_CAT_LABELS.get(cat, ("その他",))[0]
                    matches.append(
                        {
                            "name": name,
                            "name_ja": name_ja,
                            "slug": slug,
                            "urgency": urgency,
                            "category": cat,
                            "category_ja": cat_ja,
                        }
                    )
        if matches:
            matches.sort(key=lambda x: (x["name_ja"] or x["name"]).lower())
            results.append(
                {
                    "species_id": sp_id,
                    "species_ja": sp_name_ja,
                    "species_en": sp_name_en,
                    "icon": icon,
                    "diseases": matches,
                    "count": len(matches),
                }
            )
    results.sort(key=lambda x: -x["count"])
    total_results = sum(r["count"] for r in results)

    return render_template(
        "diseases_search.html",
        query=query,
        results=results,
        total_results=total_results,
        searched=True,
    )


@app.route("/diseases")
def diseases_hub():
    """Top-level diseases hub page listing all 21 species with disease counts."""
    from api.disease_store import SPECIES_META

    species_list = []
    total_diseases = 0
    category_totals: dict[str, int] = {}
    for sp_id in _DISEASE_MODULES:
        if sp_id not in SPECIES_META:
            continue
        meta = SPECIES_META[sp_id]
        diseases = _load_diseases(sp_id)
        count = len(diseases)
        total_diseases += count

        # Per-species category breakdown
        sp_cats: dict[str, int] = {}
        for d in diseases:
            dd = (
                d
                if isinstance(d, dict)
                else {
                    "name": getattr(d, "name", ""),
                    "name_ja": getattr(d, "name_ja", ""),
                    "description": getattr(d, "description", ""),
                }
            )
            cat = _classify_disease_dict(dd)
            sp_cats[cat] = sp_cats.get(cat, 0) + 1
            category_totals[cat] = category_totals.get(cat, 0) + 1

        species_list.append(
            {
                "id": sp_id,
                "name_ja": meta.get("name_ja", sp_id),
                "name_en": meta.get("name_en", sp_id.title()),
                "count": count,
                "icon": _SPECIES_ICONS.get(sp_id, "\U0001f43e"),
                "categories": sp_cats,
            }
        )
    species_list.sort(key=lambda x: x["count"], reverse=True)

    # Build ordered category list
    categories = []
    for cat_id in _DISEASE_CAT_ORDER + ["other"]:
        cnt = category_totals.get(cat_id, 0)
        if cnt > 0:
            ja, en = _DISEASE_CAT_LABELS.get(cat_id, ("その他", "Other"))
            categories.append({"id": cat_id, "ja": ja, "en": en, "count": cnt})

    return render_template(
        "diseases_hub.html",
        species=species_list,
        categories=categories,
        total=total_diseases,
    )


# Disease category classification (mirrors DISEASE_CATEGORIES in app.js)
_DISEASE_CAT_ORDER = [
    "infectious",
    "neoplastic",
    "cardiovascular",
    "respiratory",
    "gastrointestinal",
    "renal",
    "endocrine",
    "dermatological",
    "neurological",
    "musculoskeletal",
    "ophthalmological",
    "hematological",
    "dental",
    "parasitic",
    "reproductive",
    "toxicological",
    "behavioral",
    "congenital",
    "immune",
]
_DISEASE_CAT_PATTERNS = {
    "infectious": _re.compile(
        r"infect|viral|virus|bacter|feline\s+(herpes|calici|immuno|leuk|panleuk)|parvovir|distemper|leptospir|bordetella|chlamyd|mycoplasm|fungal|aspergill|crypto|blastomyc|histoplasm|fip\b|fiv\b|felv\b|septice|abscess|pyometra|peritonitis|pneumonia|ehrlich|anaplasm|babesi|leishman|borreli|bartonell|neorick|hemoplasm|mycobact|nocardia|actinomyc|pythio|coccidio|dermatophyt|ringworm|sporotrich",
        _re.IGNORECASE,
    ),
    "neoplastic": _re.compile(
        r"tumor|tumour|neoplas|cancer|carcinom|lymphom|sarcoma|melanom|adenocarcin|fibrosarcom|hemangio|mast\s*cell|leukemia|lymphosarcom|meningiom|osteosarcom|squamous\s*cell|thymom|insulinom|pheochromocyt|chemodectom|histiocyt|plasmacytom|seminoma|mammary.*neoplas",
        _re.IGNORECASE,
    ),
    "cardiovascular": _re.compile(
        r"cardi|heart|arrhythm|murmur|endocardi|myocardi|pericard|thromboembol|aortic|hypertens|dcm\b|hcm\b|valve|congesti.*heart|patent\s*ductus|tetralogy|atrial|ventricul|tachy|brady|fibrillat",
        _re.IGNORECASE,
    ),
    "respiratory": _re.compile(
        r"respir|pulmonar|lung|bronch|trache|laryn|pleural|pneumothorax|asthma|rhinit|nasal.*polyp|brachycephal.*airway|collaps.*trache|pyothorax|chylothorax|diaphragm",
        _re.IGNORECASE,
    ),
    "gastrointestinal": _re.compile(
        r"gastro|intestin|digest|bowel|colitis|enterit|pancrea|hepat|liver|cholang|esophag|megaesoph|bloat|gastric.*dilat|volvulus|obstruct|foreign\s*body|ibd\b|exocrine|lipidos|cirrhos|portosystem|intussuscept|megacolon|constipat|ileus|stomatit|gingivit",
        _re.IGNORECASE,
    ),
    "renal": _re.compile(
        r"renal|kidney|urinar|urolithi|cystit|bladder|ureter|urethr|nephro|glomerul|polycyst|azotemi|ckd\b|akut.*kidney|flutd|fus\b|hydronephros",
        _re.IGNORECASE,
    ),
    "endocrine": _re.compile(
        r"endocrin|thyroid|diabet|cushing|addison|adrenal|hyperadrenocort|hypoadrenocort|insulin|pituitar|parathyroid|hypoglyce|hyperglyce|hypothyroid|hyperthyroid|acromegal",
        _re.IGNORECASE,
    ),
    "dermatological": _re.compile(
        r"dermat|skin|cutane|alopecia|pyoderma|atop|allerg.*dermat|hot\s*spot|mange|demodex|scabies|flea.*allerg|pemphig|lupus.*erythematos|sebace|follicul|acne|interdig|pododermat|erythem|pruritus|urticar",
        _re.IGNORECASE,
    ),
    "neurological": _re.compile(
        r"neurolog|brain|spinal|seizure|epilep|vestibul|mening|encephal|myelop|disc\s*disease|ivdd|paralys|paresis|neuropath|polyneuropath|myasthenia|degenerat.*myelop|cerebell|hydrocephal|cognit.*dysfunction|wobbler|syringomyel|narcolep|head\s*tilt|ataxia",
        _re.IGNORECASE,
    ),
    "musculoskeletal": _re.compile(
        r"musculoskelet|orthop|fractur|luxat|cruciat|ligament|arthrit|dysplasia|osteochondr|spondyl|myosit|polymyosit|rhabdomyol|tendon|patella|elbow|hip\s*dysplasia|legg.*calve|hypertrophic.*osteodystro",
        _re.IGNORECASE,
    ),
    "ophthalmological": _re.compile(
        r"ophthalm|eye|ocular|cornea|conjunctiv|glaucom|catarct|uveitis|retinal|keratit|ulcer.*cornea|corneal.*ulcer|cherry\s*eye|entropion|ectropion|prolapse.*eye|proptosis|lens.*luxat|progressive.*retinal|pannus|dry\s*eye|kcs\b|exophthalm",
        _re.IGNORECASE,
    ),
    "hematological": _re.compile(
        r"hematolog|anemia|anaemia|thrombocytopen|pancytopen|coagulopath|hemolyt|polycythem|von\s*willebrand|hemophilia|dic\b|disseminat.*intravas|immune.*mediat.*anemia|imha\b|itp\b|blood.*parasit",
        _re.IGNORECASE,
    ),
    "dental": _re.compile(
        r"dental|tooth|teeth|periodon|oral.*mass|epulis|oral.*tumor|gingiv|stomatit|resorptive.*lesion|odontoclast",
        _re.IGNORECASE,
    ),
    "parasitic": _re.compile(
        r"parasit|heartworm|dirofilar|hookworm|roundworm|whipworm|tapeworm|giardia|coccidia|toxoplasm|tick.*borne|flea\b|mite|demodic|sarcoptic|ear\s*mite|cheyletiell|toxocar|ancylostom|trichuris|isospora|tritrichomonas",
        _re.IGNORECASE,
    ),
    "reproductive": _re.compile(
        r"reproduct|uterine|ovarian|testicular|prostat|mammary(?!.*neoplas)|dystocia|eclampsia|mastitis|cryptorchid|vaginal|vulvar|penile|balanoposthit",
        _re.IGNORECASE,
    ),
    "toxicological": _re.compile(
        r"toxic|poison|intoxicat|overdose|envenomation|xylitol|chocolate|antifreeze|lily\s*toxic|nsaid.*toxic|acetaminophen|rat.*poison|rodenticide|organophos|ethylene\s*glycol",
        _re.IGNORECASE,
    ),
    "behavioral": _re.compile(
        r"behavio|anxiety|aggress|compulsive|phobia|cognit.*dysfunct|separ.*anxiety|noise.*phobia", _re.IGNORECASE
    ),
    "congenital": _re.compile(
        r"congenit|develop|heredit|portosystem.*shunt|cleft.*palate|megaesoph.*congenit|atresia", _re.IGNORECASE
    ),
    "immune": _re.compile(
        r"immune.*mediat|auto.*immune|sle\b|systemic.*lupus|pemphig|polyarthrit.*immune|vasculit|eosinophil.*granulom",
        _re.IGNORECASE,
    ),
}
_DISEASE_CAT_LABELS = {
    "infectious": ("感染症", "Infectious"),
    "neoplastic": ("腫瘍", "Neoplastic"),
    "cardiovascular": ("循環器", "Cardiovascular"),
    "respiratory": ("呼吸器", "Respiratory"),
    "gastrointestinal": ("消化器", "Gastrointestinal"),
    "renal": ("泌尿器", "Renal/Urinary"),
    "endocrine": ("内分泌", "Endocrine"),
    "dermatological": ("皮膚", "Dermatological"),
    "neurological": ("神経", "Neurological"),
    "musculoskeletal": ("筋骨格", "Musculoskeletal"),
    "ophthalmological": ("眼科", "Ophthalmological"),
    "hematological": ("血液", "Hematological"),
    "dental": ("歯科", "Dental"),
    "parasitic": ("寄生虫", "Parasitic"),
    "reproductive": ("生殖器", "Reproductive"),
    "toxicological": ("中毒", "Toxicological"),
    "behavioral": ("行動", "Behavioral"),
    "congenital": ("先天性", "Congenital"),
    "immune": ("免疫", "Immune-mediated"),
    "other": ("その他", "Other"),
}


def _classify_disease_dict(d: dict) -> str:
    """Classify a disease dict into a category using keyword regex."""
    text = "%s %s %s" % (d.get("name", ""), d.get("name_ja", ""), d.get("description", ""))
    for cat_id in _DISEASE_CAT_ORDER:
        if _DISEASE_CAT_PATTERNS[cat_id].search(text):
            return cat_id
    return "other"


@app.route("/diseases/<species>")
def disease_index(species: str):
    """Server-rendered disease index page per species for SEO.

    Acts as a hub page linking to all individual disease pages,
    improving internal link structure and crawlability.
    """
    from api.disease_store import SPECIES_META

    species_key = species.lower()
    if species_key not in SPECIES_META or species_key not in _DISEASE_MODULES:
        try:
            return render_template("404.html"), 404
        except Exception:
            return jsonify({"error": "Unknown species"}), 404

    sp_meta = SPECIES_META[species_key]
    diseases = _load_diseases(species_key)

    # Build disease list with slugs and categories
    disease_list = []
    category_counts: dict[str, int] = {}
    for d in diseases:
        if isinstance(d, dict):
            name = d.get("name", "") or d.get("name_en", "")
            name_ja = d.get("name_ja", "")
            urgency = d.get("urgency", "")
            description = d.get("description", "")
        else:
            name = getattr(d, "name", "") or getattr(d, "name_en", "")
            name_ja = getattr(d, "name_ja", "")
            urgency = getattr(d, "urgency", "")
            description = getattr(d, "description", "")
        slug = _disease_slug(d)
        if slug:
            cat = _classify_disease_dict({"name": name, "name_ja": name_ja, "description": description})
            category_counts[cat] = category_counts.get(cat, 0) + 1
            disease_list.append({"name": name, "name_ja": name_ja, "urgency": urgency, "slug": slug, "category": cat})

    disease_list.sort(key=lambda x: (x["name_ja"] or x["name"]).lower())

    # Build ordered category list with counts
    categories = []
    for cat_id in _DISEASE_CAT_ORDER + ["other"]:
        cnt = category_counts.get(cat_id, 0)
        if cnt > 0:
            ja, en = _DISEASE_CAT_LABELS.get(cat_id, ("その他", "Other"))
            categories.append({"id": cat_id, "ja": ja, "en": en, "count": cnt})

    return render_template(
        "disease_index.html",
        diseases=disease_list,
        categories=categories,
        species=species_key,
        species_ja=sp_meta.get("name_ja", species_key),
        species_en=sp_meta.get("name_en", species_key.title()),
        count=len(disease_list),
    )


@app.route("/diseases/<species>/<disease_slug>")
def disease_detail(species: str, disease_slug: str):
    """Server-rendered disease detail page for SEO indexing.

    Each of the 6,400+ diseases gets its own URL that Google can crawl,
    turning the disease database into a long-tail SEO asset.
    """
    from api.disease_store import SPECIES_META

    species_key = species.lower()
    if species_key not in SPECIES_META or species_key not in _DISEASE_MODULES:
        logger.info("disease_detail: unknown species %s (slug=%s)", species_key, disease_slug)
        try:
            return render_template("404.html"), 404
        except Exception:
            return jsonify({"error": "Unknown species"}), 404

    sp_meta = SPECIES_META[species_key]
    diseases = _load_diseases(species_key)

    # Find matching disease by slug
    disease = None
    for d in diseases:
        if _disease_slug(d) == disease_slug:
            disease = d
            break

    if not disease:
        # A merged/archived (old) slug 301-redirects to its canonical page so
        # existing URLs never break after non-destructive consolidation (T103).
        try:
            from api.species.canonical import resolve_redirect

            canonical_slug = resolve_redirect(species_key, disease_slug)
        except ImportError:
            canonical_slug = None
        if canonical_slug and canonical_slug != disease_slug:
            return redirect(url_for("disease_detail", species=species, disease_slug=canonical_slug), code=301)

        logger.info(
            "disease_detail: slug not found species=%s slug=%s (total=%d)",
            species_key,
            disease_slug,
            len(diseases),
        )
        try:
            return render_template("404.html"), 404
        except Exception:
            return jsonify({"error": "Disease not found"}), 404

    # Normalize to dict for template rendering (handles dataclass objects)
    if not isinstance(disease, dict):
        from dataclasses import asdict

        try:
            disease = asdict(disease)
        except TypeError:
            disease = {
                k: getattr(disease, k, "")
                for k in (
                    "name",
                    "name_ja",
                    "description",
                    "description_ja",
                    "symptoms",
                    "causes",
                    "causes_ja",
                    "pathophysiology",
                    "pathophysiology_ja",
                    "treatment",
                    "treatment_ja",
                    "prevention",
                    "prevention_ja",
                    "prognosis",
                    "prognosis_ja",
                    "urgency",
                    "recommended_tests",
                )
            }

    sp_label_ja = sp_meta.get("name_ja", species_key)
    sp_label_en = sp_meta.get("name_en", species_key.title())

    # Load symptom names for human-readable display (handles equine findings too)
    _sym_full = _symptom_names_for_species(species_key)
    symptom_names = {k: v.get("ja", k) for k, v in _sym_full.items()}

    # Symptom ids for this disease (set converter; equine uses associated_findings),
    # sorted with only those that have a known name (so each can link to its page)
    disease_symptoms = _disease_symptom_ids(disease)
    symptom_ids = sorted(sid for sid in disease_symptoms if sid in _sym_full)
    related = []
    if disease_symptoms:
        for d in diseases:
            d_name = _disease_get(d, "name", "")
            if d_name == disease.get("name"):
                continue
            d_syms = _disease_get(d, "symptoms", set())
            if isinstance(d_syms, (set, list)):
                d_syms = set(d_syms)
            else:
                continue
            shared = disease_symptoms & d_syms
            if len(shared) >= 2:
                related.append(
                    {
                        "name": d_name,
                        "name_ja": _disease_get(d, "name_ja", ""),
                        "slug": _disease_slug(d),
                        "shared": len(shared),
                    }
                )
        related.sort(key=lambda x: -x["shared"])
        related = related[:8]

    # Extract mentioned drugs from treatment text
    mentioned_drugs = []
    treatment_text = (disease.get("treatment_ja", "") + " " + disease.get("treatment", "")).lower()
    if treatment_text.strip():
        try:
            from api.drug_dictionary import DRUGS as _ALL_DRUGS

            for dr in _ALL_DRUGS:
                dr_name = dr.get("name", "")
                dr_name_ja = dr.get("name_ja", "")
                if (dr_name and dr_name.lower() in treatment_text) or (dr_name_ja and dr_name_ja in treatment_text):
                    mentioned_drugs.append({"id": dr.get("id", ""), "name": dr_name, "name_ja": dr_name_ja})
            mentioned_drugs = mentioned_drugs[:10]
        except Exception:
            pass

    # Load PubMed references
    pubmed_refs = []
    try:
        from api.pubmed_references import get_references_for_disease

        pubmed_refs = get_references_for_disease(disease.get("name", ""))
    except Exception:
        pass

    # Classify this disease's category
    disease_cat = _classify_disease_dict(disease)
    cat_ja, cat_en = _DISEASE_CAT_LABELS.get(disease_cat, ("その他", "Other"))

    # Find same-category diseases for navigation
    same_cat_diseases = []
    for d in diseases:
        d_name = _disease_get(d, "name", "")
        if d_name == disease.get("name"):
            continue
        dd = {
            "name": d_name,
            "name_ja": _disease_get(d, "name_ja", ""),
            "description": _disease_get(d, "description", ""),
        }
        if _classify_disease_dict(dd) == disease_cat:
            slug = _disease_slug(d)
            if slug:
                same_cat_diseases.append(
                    {
                        "name": d_name,
                        "name_ja": dd["name_ja"],
                        "slug": slug,
                    }
                )
    same_cat_diseases.sort(key=lambda x: (x["name_ja"] or x["name"]).lower())
    same_cat_diseases = same_cat_diseases[:12]

    return render_template(
        "disease_detail.html",
        disease=disease,
        species=species_key,
        species_ja=sp_label_ja,
        species_en=sp_label_en,
        symptom_names=symptom_names,
        symptom_ids=symptom_ids,
        related_diseases=related,
        mentioned_drugs=mentioned_drugs,
        pubmed_refs=pubmed_refs,
        disease_category=disease_cat,
        disease_category_ja=cat_ja,
        disease_category_en=cat_en,
        same_category_diseases=same_cat_diseases,
    )


# =============================================================================
# Drug dictionary SEO pages (each drug = a crawlable long-tail page)
# =============================================================================

# Species labels for drug dosage tables (superset of disease SPECIES_META keys;
# drug data also uses "pig" and "others").
_DRUG_SPECIES_LABELS: dict[str, tuple[str, str]] = {
    "dog": ("犬", "Dog"),
    "cat": ("猫", "Cat"),
    "horse": ("馬", "Horse"),
    "rabbit": ("うさぎ", "Rabbit"),
    "hamster": ("ハムスター", "Hamster"),
    "guinea_pig": ("モルモット", "Guinea Pig"),
    "chinchilla": ("チンチラ", "Chinchilla"),
    "ferret": ("フェレット", "Ferret"),
    "hedgehog": ("ハリネズミ", "Hedgehog"),
    "sugar_glider": ("フクロモモンガ", "Sugar Glider"),
    "degu": ("デグー", "Degu"),
    "bird": ("鳥", "Bird"),
    "parakeet": ("インコ", "Parakeet"),
    "parrot": ("オウム", "Parrot"),
    "reptile": ("爬虫類", "Reptile"),
    "tortoise": ("リクガメ", "Tortoise"),
    "snake": ("ヘビ", "Snake"),
    "lizard": ("トカゲ", "Lizard"),
    "amphibian": ("両生類", "Amphibian"),
    "fish": ("魚", "Fish"),
    "pig": ("豚", "Pig"),
    "exotic_other": ("その他エキゾチック", "Exotic Other"),
    "others": ("その他", "Other"),
}

# Stable ordering for species columns in drug tables.
_DRUG_SPECIES_ORDER = list(_DRUG_SPECIES_LABELS.keys())


def _drug_cat_label(cat_id: str):
    """Return (ja, en) label for a drug category id."""
    from api.drug_dictionary import DRUG_CATEGORIES

    meta = DRUG_CATEGORIES.get(cat_id, {})
    return meta.get("ja", cat_id), meta.get("en", cat_id.replace("_", " ").title())


@app.route("/drugs")
def drugs_hub():
    """Top-level drug dictionary hub grouping every drug by category for SEO."""
    from api.drug_dictionary import DRUGS

    groups: dict[str, list] = {}
    for d in DRUGS:
        did = d.get("id", "")
        if not did:
            continue
        cat = d.get("category", "") or "miscellaneous"
        groups.setdefault(cat, []).append(
            {
                "id": did,
                "name": d.get("name", ""),
                "name_ja": d.get("name_ja", ""),
            }
        )

    categories = []
    for cat_id in sorted(groups, key=lambda c: -len(groups[c])):
        ja, en = _drug_cat_label(cat_id)
        items = sorted(groups[cat_id], key=lambda x: (x["name_ja"] or x["name"]).lower())
        categories.append({"id": cat_id, "ja": ja, "en": en, "count": len(items), "drugs": items})

    return render_template(
        "drugs_hub.html",
        categories=categories,
        total=sum(c["count"] for c in categories),
    )


@app.route("/drugs/<drug_id>")
def drug_detail(drug_id: str):
    """Server-rendered drug detail page for SEO indexing.

    Each drug in the dictionary gets its own crawlable URL with mechanism,
    species-specific dosing, side effects, interactions and links to the
    diseases it is used to treat.
    """
    from api.drug_dictionary import DRUGS, get_drug_by_id

    drug = get_drug_by_id(drug_id)
    if not drug:
        logger.info("drug_detail: unknown drug id=%s", drug_id)
        try:
            return render_template("404.html"), 404
        except Exception:
            return jsonify({"error": "Drug not found"}), 404

    cat_id = drug.get("category", "") or "miscellaneous"
    cat_ja, cat_en = _drug_cat_label(cat_id)

    # Species-specific dosing rows (ordered, labelled, JA preferred)
    species_info = drug.get("species_info") or {}
    dosing_rows = []
    for sp_key in _DRUG_SPECIES_ORDER:
        info = species_info.get(sp_key)
        if not isinstance(info, dict):
            continue
        ja, en = _DRUG_SPECIES_LABELS.get(sp_key, (sp_key, sp_key.title()))
        dosing_rows.append(
            {
                "species": sp_key,
                "species_ja": ja,
                "species_en": en,
                "safe": info.get("safe"),
                "dosage": info.get("dosage_ja") or info.get("dosage", ""),
                "dosage_en": info.get("dosage", ""),
                "notes": info.get("notes_ja") or info.get("notes", ""),
            }
        )
    # Append any species keys not in the canonical order (defensive)
    for sp_key, info in species_info.items():
        if sp_key in _DRUG_SPECIES_ORDER or not isinstance(info, dict):
            continue
        ja, en = _DRUG_SPECIES_LABELS.get(sp_key, (sp_key, sp_key.title()))
        dosing_rows.append(
            {
                "species": sp_key,
                "species_ja": ja,
                "species_en": en,
                "safe": info.get("safe"),
                "dosage": info.get("dosage_ja") or info.get("dosage", ""),
                "dosage_en": info.get("dosage", ""),
                "notes": info.get("notes_ja") or info.get("notes", ""),
            }
        )

    # Normalize side effects / contraindications to displayable forms
    def _as_text_list(val):
        if isinstance(val, (list, tuple)):
            return [str(x) for x in val if x]
        if isinstance(val, str) and val.strip():
            return [val.strip()]
        return []

    side_effects = _as_text_list(drug.get("side_effects_ja")) or _as_text_list(drug.get("side_effects"))
    contraindications = drug.get("contraindications_ja") or drug.get("contraindications") or ""

    interactions = []
    for it in drug.get("drug_interactions") or []:
        if isinstance(it, dict):
            interactions.append(
                {
                    "drug": it.get("drug", ""),
                    "effect": it.get("effect_ja") or it.get("effect", ""),
                }
            )

    # Diseases this drug is used to treat (cross-link to disease pages)
    treated = []
    try:
        from api.drug_dictionary import find_diseases_for_drug

        for row in find_diseases_for_drug(drug_id, limit=24):
            sp = row.get("species", "")
            if sp not in _DISEASE_MODULES:
                continue
            name = row.get("name", "")
            slug = _re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
            if not slug:
                continue
            sp_ja = _DRUG_SPECIES_LABELS.get(sp, (sp, sp))[0]
            treated.append(
                {
                    "species": sp,
                    "species_ja": sp_ja,
                    "name": name,
                    "name_ja": row.get("name_ja", ""),
                    "slug": slug,
                    "urgency": row.get("urgency", ""),
                }
            )
    except Exception:
        logger.debug("drug_detail: find_diseases_for_drug failed for %s", drug_id, exc_info=True)

    # Related drugs in the same category
    related_drugs = []
    for d in DRUGS:
        if d.get("id") == drug_id or (d.get("category") or "miscellaneous") != cat_id:
            continue
        if d.get("id"):
            related_drugs.append({"id": d["id"], "name": d.get("name", ""), "name_ja": d.get("name_ja", "")})
    related_drugs.sort(key=lambda x: (x["name_ja"] or x["name"]).lower())
    related_drugs = related_drugs[:12]

    return render_template(
        "drug_detail.html",
        drug=drug,
        drug_id=drug_id,
        category_id=cat_id,
        category_ja=cat_ja,
        category_en=cat_en,
        dosing_rows=dosing_rows,
        side_effects=side_effects,
        contraindications=contraindications,
        interactions=interactions,
        treated_diseases=treated,
        related_drugs=related_drugs,
    )


# =============================================================================
# Anesthesia / sedation protocol SEO pages (per-species clinical routines)
# =============================================================================


@app.route("/anesthesia")
def anesthesia_hub():
    """Hub page listing all species with their anesthesia/sedation protocols."""
    from api.anesthesia_protocols import ANESTHESIA_CATEGORIES, ANESTHESIA_PROTOCOLS

    species_list = []
    total = 0
    for sp_id, data in ANESTHESIA_PROTOCOLS.items():
        protocols = data.get("protocols", []) or []
        total += len(protocols)
        name = data.get("species_name", {}) or {}
        species_list.append(
            {
                "id": sp_id,
                "name_ja": name.get("ja", sp_id),
                "name_en": name.get("en", sp_id.title()),
                "icon": _SPECIES_ICONS.get(sp_id, "\U0001f43e"),
                "count": len(protocols),
            }
        )
    species_list.sort(key=lambda x: x["count"], reverse=True)

    categories = [
        {"id": cid, "ja": c.get("ja", cid), "en": c.get("en", cid)} for cid, c in ANESTHESIA_CATEGORIES.items()
    ]

    return render_template(
        "anesthesia_hub.html",
        species=species_list,
        categories=categories,
        total=total,
        species_count=len(species_list),
    )


@app.route("/anesthesia/<species>")
def anesthesia_species(species: str):
    """Server-rendered per-species anesthesia/sedation protocol page for SEO."""
    from api.anesthesia_protocols import ANESTHESIA_CATEGORIES, ANESTHESIA_PROTOCOLS

    sp_key = species.lower()
    data = ANESTHESIA_PROTOCOLS.get(sp_key)
    if not data:
        logger.info("anesthesia_species: unknown species %s", sp_key)
        try:
            return render_template("404.html"), 404
        except Exception:
            return jsonify({"error": "Unknown species"}), 404

    name = data.get("species_name", {}) or {}
    sp_ja = name.get("ja", sp_key)
    sp_en = name.get("en", sp_key.title())

    # Group protocols by category, preserving the canonical category order
    protocols = data.get("protocols", []) or []
    cat_order = list(ANESTHESIA_CATEGORIES.keys())
    grouped: dict[str, list] = {}
    for p in protocols:
        grouped.setdefault(p.get("category", "other"), []).append(p)

    sections = []
    for cid in cat_order:
        if cid in grouped:
            c = ANESTHESIA_CATEGORIES.get(cid, {})
            sections.append({"id": cid, "ja": c.get("ja", cid), "en": c.get("en", cid), "protocols": grouped[cid]})
    # Any categories not in the canonical order
    for cid, plist in grouped.items():
        if cid not in cat_order:
            sections.append({"id": cid, "ja": cid, "en": cid, "protocols": plist})

    # Other species links for cross-navigation
    other_species = []
    for osp, odata in ANESTHESIA_PROTOCOLS.items():
        if osp == sp_key:
            continue
        oname = odata.get("species_name", {}) or {}
        other_species.append(
            {
                "id": osp,
                "name_ja": oname.get("ja", osp),
                "icon": _SPECIES_ICONS.get(osp, "\U0001f43e"),
            }
        )

    return render_template(
        "anesthesia_detail.html",
        species=sp_key,
        species_ja=sp_ja,
        species_en=sp_en,
        overview=data.get("overview", {}) or {},
        fasting=data.get("fasting", {}) or {},
        breed_considerations=data.get("breed_considerations", {}) or {},
        references=data.get("references", []) or [],
        sections=sections,
        protocol_count=len(protocols),
        other_species=other_species,
    )


# =============================================================================
# Symptom SEO pages (disease ↔ symptom bipartite internal-link graph)
# =============================================================================


def _symptom_names_for_species(species_key: str) -> dict:
    """Return {symptom_id: {"ja": .., "en": ..}} for a species.

    Most species expose ``SYMPTOM_NAMES``; the equine module instead exposes
    ``HEALTH_CHECK_ITEMS`` (category -> list of (id, ja, en) tuples).
    """
    mod_name = _DISEASE_MODULES.get(species_key)
    if not mod_name:
        return {}
    try:
        import importlib

        mod = importlib.import_module(mod_name)
    except ImportError:
        return {}

    sym_names = getattr(mod, "SYMPTOM_NAMES", None)
    if isinstance(sym_names, dict) and sym_names:
        out = {}
        for sid, val in sym_names.items():
            if isinstance(val, dict):
                out[sid] = {"ja": val.get("ja", sid), "en": val.get("en", sid)}
            else:
                out[sid] = {"ja": str(val), "en": str(val)}
        return out

    # Equine (HEALTH_CHECK_ITEMS) fallback
    hci = getattr(mod, "HEALTH_CHECK_ITEMS", None)
    if isinstance(hci, dict):
        out = {}
        for items in hci.values():
            for tup in items:
                if len(tup) >= 3:
                    out[tup[0]] = {"ja": tup[1], "en": tup[2]}
        return out
    return {}


def _disease_symptom_ids(disease) -> set:
    """Return the set of symptom/finding ids for a disease (dict or dataclass)."""
    for key in ("symptoms", "associated_findings"):
        if isinstance(disease, dict):
            val = disease.get(key)
        else:
            val = getattr(disease, key, None)
        if val and isinstance(val, (set, list, tuple)):
            return set(val)
    return set()


@app.route("/symptoms")
def symptoms_hub():
    """Hub page linking to every species' symptom index for SEO."""
    from api.disease_store import SPECIES_META

    species_list = []
    for sp_id in _DISEASE_MODULES:
        if sp_id not in SPECIES_META:
            continue
        meta = SPECIES_META[sp_id]
        sym_names = _symptom_names_for_species(sp_id)
        # Count only symptoms actually used by at least one disease
        used = set()
        for d in _load_diseases(sp_id):
            used |= _disease_symptom_ids(d)
        used &= set(sym_names.keys())
        species_list.append(
            {
                "id": sp_id,
                "name_ja": meta.get("name_ja", sp_id),
                "name_en": meta.get("name_en", sp_id.title()),
                "icon": _SPECIES_ICONS.get(sp_id, "\U0001f43e"),
                "count": len(used),
            }
        )
    species_list.sort(key=lambda x: x["count"], reverse=True)

    return render_template(
        "symptoms_hub.html",
        species=species_list,
        species_count=len(species_list),
        total=sum(s["count"] for s in species_list),
    )


@app.route("/symptoms/<species>")
def symptoms_index(species: str):
    """Per-species index of symptoms, each linking to its symptom page."""
    from api.disease_store import SPECIES_META

    sp_key = species.lower()
    if sp_key not in SPECIES_META or sp_key not in _DISEASE_MODULES:
        try:
            return render_template("404.html"), 404
        except Exception:
            return jsonify({"error": "Unknown species"}), 404

    sp_meta = SPECIES_META[sp_key]
    sym_names = _symptom_names_for_species(sp_key)

    # Count diseases per symptom id
    counts: dict[str, int] = {}
    for d in _load_diseases(sp_key):
        for sid in _disease_symptom_ids(d):
            counts[sid] = counts.get(sid, 0) + 1

    symptoms = []
    for sid, cnt in counts.items():
        names = sym_names.get(sid)
        if not names:
            continue
        symptoms.append(
            {
                "id": sid,
                "ja": names["ja"],
                "en": names["en"],
                "count": cnt,
            }
        )
    symptoms.sort(key=lambda x: (-x["count"], x["ja"]))

    return render_template(
        "symptoms_index.html",
        species=sp_key,
        species_ja=sp_meta.get("name_ja", sp_key),
        species_en=sp_meta.get("name_en", sp_key.title()),
        symptoms=symptoms,
        count=len(symptoms),
    )


@app.route("/symptoms/<species>/<symptom_id>")
def symptom_detail(species: str, symptom_id: str):
    """List every disease in a species that presents a given symptom."""
    from api.disease_store import SPECIES_META

    sp_key = species.lower()
    if sp_key not in SPECIES_META or sp_key not in _DISEASE_MODULES:
        try:
            return render_template("404.html"), 404
        except Exception:
            return jsonify({"error": "Unknown species"}), 404

    sym_names = _symptom_names_for_species(sp_key)
    names = sym_names.get(symptom_id)
    if not names:
        try:
            return render_template("404.html"), 404
        except Exception:
            return jsonify({"error": "Unknown symptom"}), 404

    sp_meta = SPECIES_META[sp_key]

    # Diseases presenting this symptom, with their other symptoms for context
    diseases = []
    for d in _load_diseases(sp_key):
        sids = _disease_symptom_ids(d)
        if symptom_id not in sids:
            continue
        slug = _disease_slug(d)
        if not slug:
            continue
        other = []
        for sid in sids:
            if sid == symptom_id:
                continue
            on = sym_names.get(sid)
            if on:
                other.append({"id": sid, "ja": on["ja"]})
        other.sort(key=lambda x: x["ja"])
        diseases.append(
            {
                "name": _disease_get(d, "name", ""),
                "name_ja": _disease_get(d, "name_ja", ""),
                "slug": slug,
                "urgency": _disease_get(d, "urgency", ""),
                "category": _classify_disease_dict(
                    {
                        "name": _disease_get(d, "name", ""),
                        "name_ja": _disease_get(d, "name_ja", ""),
                        "description": _disease_get(d, "description", ""),
                    }
                ),
                "other_symptoms": other[:6],
            }
        )

    # Order: emergency first, then by name
    _urg_rank = {"emergency": 0, "high": 1, "moderate": 2, "low": 3, "": 4}
    diseases.sort(key=lambda x: (_urg_rank.get(x["urgency"], 4), (x["name_ja"] or x["name"]).lower()))

    # Related symptoms (co-occurring) for cross-linking
    co_counts: dict[str, int] = {}
    for d in _load_diseases(sp_key):
        sids = _disease_symptom_ids(d)
        if symptom_id not in sids:
            continue
        for sid in sids:
            if sid != symptom_id and sid in sym_names:
                co_counts[sid] = co_counts.get(sid, 0) + 1
    related = sorted(co_counts.items(), key=lambda x: -x[1])[:12]
    related_symptoms = [{"id": sid, "ja": sym_names[sid]["ja"], "count": c} for sid, c in related]

    return render_template(
        "symptom_detail.html",
        species=sp_key,
        species_ja=sp_meta.get("name_ja", sp_key),
        species_en=sp_meta.get("name_en", sp_key.title()),
        symptom_id=symptom_id,
        symptom_ja=names["ja"],
        symptom_en=names["en"],
        diseases=diseases,
        count=len(diseases),
        related_symptoms=related_symptoms,
    )


# =============================================================================
# Anesthesia protocol drug-name linking (link each drug to its /drugs/<id>)
# =============================================================================

_ANES_DRUG_LOOKUP: dict[str, str] | None = None
_ANES_SUFFIX_RE = _re.compile(
    r"\b(CRI|TIVA|IM|IV|IN|PO|SC|IP|q\d\S*|low[- ]?dose|premed\w*|intranasal|atomization|"
    r"combined|injection|cream|bath|immersion|infusion|drip|nebuli\w*|induction|step\s*\d)\b",
    _re.IGNORECASE,
)


def _build_anes_drug_lookup() -> dict[str, str]:
    """Lowercase drug-name / id -> drug_id map for linking protocol drugs."""
    global _ANES_DRUG_LOOKUP
    if _ANES_DRUG_LOOKUP is not None:
        return _ANES_DRUG_LOOKUP
    lookup: dict[str, str] = {}
    try:
        from api.drug_dictionary import DRUGS

        for d in DRUGS:
            did = d.get("id")
            if not did:
                continue
            lookup.setdefault(did.lower(), did)
            for key in (d.get("name"), d.get("name_ja")):
                if key:
                    lookup.setdefault(key.strip().lower(), did)
    except Exception:
        pass
    _ANES_DRUG_LOOKUP = lookup
    return lookup


def _match_anes_component(token: str):
    """Resolve a single drug-name component to a drug_id, or None."""
    lookup = _build_anes_drug_lookup()
    t = token.split("(")[0]
    t = _ANES_SUFFIX_RE.sub("", t)
    t = _re.sub(r"[^a-zA-Z0-9\- ]", " ", t).strip().lower()
    if not t:
        return None
    if t in lookup:
        return lookup[t]
    parts = t.split()
    if parts and parts[0] in lookup:
        return lookup[parts[0]]
    return None


def _anes_drug_segments(name: str) -> list:
    """Split a protocol drug-name into linkable segments.

    Returns a list of {"text": str, "id": str|None}. Combination entries
    ("Dexmedetomidine + Butorphanol") become separate linked components with
    the "+" separators preserved as plain text.
    """
    if not name:
        return []
    segments = []
    parts = name.split("+")
    for i, part in enumerate(parts):
        did = _match_anes_component(part)
        segments.append({"text": part.strip(), "id": did})
        if i < len(parts) - 1:
            segments.append({"text": " + ", "id": None})
    return segments


# Expose drug-name linking to Jinja templates (anesthesia protocol tables)
app.jinja_env.globals["anes_drug_links"] = _anes_drug_segments


@app.route("/<path:filename>")
def static_files(filename):
    try:
        return send_from_directory(STATIC_DIR, filename)
    except (FileNotFoundError, WerkzeugNotFound):
        try:
            return send_from_directory(TEMPLATES_DIR, filename)
        except (FileNotFoundError, WerkzeugNotFound):
            if _wants_html_response():
                try:
                    return render_template("404.html"), 404
                except Exception:
                    pass
            return jsonify({"error": f"{filename} not found"}), 404


# =============================================================================
# API: Health Check
# =============================================================================


@app.route("/api/health", methods=["GET"])
@ensure_json_response
def health():
    import shutil
    import sqlite3 as _sqlite3

    checks = {}

    # Database connectivity + integrity check
    import time as _time

    try:
        from api.database import DB_PATH as _db_path

        _db_file = Path(_db_path)
        if _db_file.exists() and _db_file.stat().st_size > 0:
            _t0 = _time.monotonic()
            _conn = _sqlite3.connect(_db_path, timeout=5.0)
            _sqlite_count = _conn.execute("SELECT COUNT(*) FROM diseases").fetchone()[0]
            _integrity = _conn.execute("PRAGMA quick_check").fetchone()[0]
            _conn.close()
            _latency_ms = round((_time.monotonic() - _t0) * 1000, 1)
            _db_ok = _integrity == "ok"
            # Report the count actually served by the API. When SQLite is empty
            # the disease_store falls back to in-memory Python modules, so a
            # bare SELECT COUNT(*) misrepresents the system as having 0
            # diseases. Use the effective count for monitoring/uptime checks.
            try:
                from api.disease_store import get_species_stats

                _effective_count = sum(s.get("diseases", 0) for s in get_species_stats().get("species", []))
            except Exception:
                _effective_count = _sqlite_count
            checks["database"] = {
                "status": "ok" if _db_ok else "error",
                "diseases": _effective_count,
                "diseases_sqlite": _sqlite_count,
                "integrity": _integrity,
                "latency_ms": _latency_ms,
            }
        else:
            checks["database"] = {"status": "ok", "detail": "not configured"}
    except Exception as _e:
        logger.error("Health check database error: %s", _e)
        checks["database"] = {"status": "error", "detail": "database unavailable"}

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
        "status": status_str,
        "version": VERSION,
        "build": BUILD,
        "checks": checks,
        "features": {
            "symptom_checker": SYMPTOM_CHECKER_AVAILABLE,
            "species_analyzer": SPECIES_ANALYZER_AVAILABLE,
            "health_checker": HEALTH_CHECKER_AVAILABLE,
            "diagnostic_chat": DIAGNOSTIC_CHAT_AVAILABLE,
            "drug_dictionary": DRUG_DICTIONARY_AVAILABLE,
            "reco2": RECO2_AVAILABLE,
        },
    }


# =============================================================================
# API: Species Stats (from SQLite)
# =============================================================================


@app.route("/api/species-stats", methods=["GET"])
@ensure_json_response
def api_species_stats():
    """各動物種の疾患数・薬品数を SQLite から返す。"""
    from api.disease_store import get_species_stats

    return get_species_stats()


@app.route("/api/dashboard-stats", methods=["GET"])
@ensure_json_response
def api_dashboard_stats():
    """ダッシュボード用サマリー統計を返す（疾患数・薬品数・動物種数・麻酔プロトコル数）。

    Returns:
        dict with keys: total_diseases, total_drugs, total_species, total_protocols
    """
    from api.disease_store import get_species_stats

    # Get disease/drug/species stats
    species_stats = get_species_stats()

    # Count anesthesia protocols: all protocols across all species
    total_protocols = 0
    try:
        from api.anesthesia_protocols import get_all_species_ids, get_protocols_for_species

        for species_id in get_all_species_ids():
            try:
                sp_data = get_protocols_for_species(species_id)
                if sp_data and "protocols" in sp_data:
                    total_protocols += len(sp_data["protocols"])
            except Exception:
                # Skip species if protocol fetch fails
                pass
    except Exception as e:
        logger.warning(f"Failed to count anesthesia protocols: {e}")
        # Fallback to last known value
        total_protocols = 188

    return {
        "total_diseases": species_stats.get("total_diseases", 0),
        "total_drugs": species_stats.get("total_drugs", 0),
        "total_species": species_stats.get("total_species", 0),
        "total_protocols": total_protocols if total_protocols > 0 else 188,
    }


@app.route("/api/dashboard-stats/detailed", methods=["GET"])
@ensure_json_response
def api_dashboard_stats_detailed():
    """詳細ダッシュボード統計：種別疾患数・薬品カテゴリ別・緊急プロトコル等。

    Returns:
        dict containing:
        - species_disease_counts: list[{species, count}]
        - drug_category_counts: list[{category, name_ja, count}]
        - urgency_distribution: dict[species → dict[urgency → count]]
        - top_lab_combinations: list (lab patterns)
        - emergency_categories: dict[category → count]
        - ecvn_coverage: dict (sponsor adjunct coverage per species)
    """
    import importlib
    from collections import Counter

    # Species disease counts
    species_modules = [
        ("dog", "api.species.dog_diseases", "DISEASES"),
        ("cat", "api.species.cat_diseases", "DISEASES"),
        ("horse", "api.species.equine_diseases", "DISEASE_DATABASE"),
        ("rabbit", "api.species.rabbit_diseases", "DISEASES"),
        ("hamster", "api.species.hamster_diseases", "DISEASES"),
        ("guinea_pig", "api.species.guinea_pig_diseases", "DISEASES"),
        ("chinchilla", "api.species.chinchilla_diseases", "DISEASES"),
        ("ferret", "api.species.ferret_diseases", "DISEASES"),
        ("hedgehog", "api.species.hedgehog_diseases", "DISEASES"),
        ("sugar_glider", "api.species.sugar_glider_diseases", "DISEASES"),
        ("degu", "api.species.degu_diseases", "DISEASES"),
        ("bird", "api.species.bird_diseases", "DISEASES"),
        ("parakeet", "api.species.parakeet_diseases", "DISEASES"),
        ("parrot", "api.species.parrot_diseases", "DISEASES"),
        ("reptile", "api.species.reptile_diseases", "DISEASES"),
        ("tortoise", "api.species.tortoise_diseases", "DISEASES"),
        ("snake", "api.species.snake_diseases", "DISEASES"),
        ("lizard", "api.species.lizard_diseases", "DISEASES"),
        ("amphibian", "api.species.amphibian_diseases", "DISEASES"),
        ("fish", "api.species.fish_diseases", "DISEASES"),
        ("exotic_other", "api.species.exotic_other_diseases", "DISEASES"),
    ]

    species_counts = []
    urgency_dist: dict = {}
    ecvn_coverage: dict = {}
    ecvn_marker = "[ECVN:Block]"

    for sp, mod_name, attr in species_modules:
        try:
            mod = importlib.import_module(mod_name)
            diseases = getattr(mod, attr, [])
        except (ImportError, AttributeError):
            continue
        species_counts.append({"species": sp, "count": len(diseases)})
        # Urgency distribution
        u_counter: Counter = Counter()
        ecvn_count = 0
        for d in diseases:
            if isinstance(d, dict):
                u = d.get("urgency", "") or ""
                u_counter[u] += 1
                treatment_text = (d.get("treatment_ja") or "") + (d.get("treatment") or "")
                if ecvn_marker in treatment_text:
                    ecvn_count += 1
            else:
                # Equine Disease dataclass
                u = getattr(d, "urgency", "") or ""
                u_counter[u] += 1
                if ecvn_marker in (getattr(d, "treatment_protocol", "") or ""):
                    ecvn_count += 1
        urgency_dist[sp] = dict(u_counter)
        ecvn_coverage[sp] = {
            "covered": ecvn_count,
            "total": len(diseases),
            "pct": round(ecvn_count / len(diseases) * 100, 1) if diseases else 0,
        }

    # Drug category counts
    try:
        from api.drug_dictionary import DRUG_CATEGORIES, DRUGS

        drug_cat_counter: Counter = Counter()
        for d in DRUGS:
            drug_cat_counter[d.get("category", "")] += 1
        drug_category_counts = []
        for cat_id, info in DRUG_CATEGORIES.items():
            drug_category_counts.append(
                {
                    "category": cat_id,
                    "name_ja": info.get("ja", cat_id),
                    "name_en": info.get("en", cat_id),
                    "count": drug_cat_counter.get(cat_id, 0),
                }
            )
        drug_category_counts.sort(key=lambda x: -x["count"])
    except (ImportError, AttributeError):
        drug_category_counts = []

    # Emergency category breakdown
    try:
        from api.emergency_protocols import EMERGENCY_PROTOCOLS

        emergency_cat_counter: Counter = Counter()
        for p in EMERGENCY_PROTOCOLS:
            emergency_cat_counter[p.get("category", "")] += 1
        emergency_categories = dict(emergency_cat_counter)
    except (ImportError, AttributeError):
        emergency_categories = {}

    # Lab pattern count
    try:
        from api.species.helpers import LAB_COMBINATION_PATTERNS

        lab_pattern_count = len(LAB_COMBINATION_PATTERNS)
    except (ImportError, AttributeError):
        lab_pattern_count = 0

    return {
        "species_disease_counts": species_counts,
        "drug_category_counts": drug_category_counts,
        "urgency_distribution": urgency_dist,
        "emergency_categories": emergency_categories,
        "lab_combination_patterns": lab_pattern_count,
        "ecvn_coverage": ecvn_coverage,
        "total_emergency_protocols": sum(emergency_categories.values()),
    }


# =============================================================================
# API: Species-specific Symptoms (from SQLite)
# =============================================================================


@app.route("/api/species/<species>/symptoms", methods=["GET"])
@ensure_json_response
def api_species_symptoms(species: str):
    """Return symptom list for the selected species from SQLite."""
    from api.disease_store import get_symptoms_for_species

    species_key = (species or "").lower()
    return {"symptoms": get_symptoms_for_species(species_key)}


@app.route("/api/related-symptoms/<species>", methods=["POST"])
@ensure_json_response
def get_related_symptoms(species):
    """Suggest symptoms that commonly co-occur with selected ones."""
    data = request.get_json(silent=True) or {}
    selected = data.get("symptoms", [])
    if not selected or not isinstance(selected, list):
        return {"related": []}

    species_key = (species or "").lower()

    try:
        from api.disease_store import get_symptoms_for_species

        all_symptoms = get_symptoms_for_species(species_key)
        if not all_symptoms:
            return {"related": []}

        # Build a lookup from symptom id to symptom info
        sym_lookup = {s["id"]: s for s in all_symptoms}

        # Query diseases for this species to build co-occurrence
        import json as _json

        from api.database import get_connection

        with get_connection() as conn:
            rows = conn.execute(
                "SELECT symptoms FROM diseases WHERE species = ? AND symptoms IS NOT NULL",
                (species_key,),
            ).fetchall()

        # Build the list of per-disease symptom sets. Prefer SQLite, but fall
        # back to the in-memory disease modules when the table has no rows for
        # this species (e.g. migration skipped on memory-constrained hosts) so
        # the co-occurrence suggestions still work.
        disease_symptom_sets: list[set] = []
        if rows:
            for row in rows:
                try:
                    disease_symptom_sets.append(set(_json.loads(row["symptoms"])))
                except (ValueError, TypeError):
                    logger.warning("Corrupted symptoms JSON for disease %s", row.get("id", "unknown"))
                    continue
        else:
            for d in _load_diseases(species_key):
                syms = d.get("symptoms") if isinstance(d, dict) else getattr(d, "symptoms", None)
                if syms:
                    disease_symptom_sets.append(set(syms))

        if not disease_symptom_sets:
            return {"related": []}

        selected_set = set(selected)
        co_occur: dict[str, int] = {}
        for disease_symptoms in disease_symptom_sets:
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
                result.append(
                    {
                        "id": sym_id,
                        "name_ja": sym_info.get("name_ja", sym_id),
                        "name_en": sym_info.get("name_en", sym_id),
                        "score": score,
                    }
                )

        return {"related": result}
    except Exception as e:
        logger.warning("Related symptoms error: %s", e)
        return {"related": []}


# =============================================================================
# API: Symptom Analysis (multi-species)
# =============================================================================


def _iter_result_disease_lists(result):
    """Yield each list of disease dicts contained in an analysis result.

    Covers the flat ranked list (``suspected_diseases`` / ``possible_conditions``)
    and the phase-split lists used by the stepwise UI.
    """
    if not isinstance(result, dict):
        return
    for key in ("suspected_diseases", "possible_conditions"):
        value = result.get(key)
        if isinstance(value, list):
            yield value
    by_phase = result.get("suspected_diseases_by_phase", {})
    if isinstance(by_phase, dict):
        for phase_diseases in by_phase.values():
            if isinstance(phase_diseases, list):
                yield phase_diseases


def _cap_result_diseases(result, max_total=50):
    """Trim the differential to the top ``max_total`` ranked diseases.

    The engine returns every disease that matches at least one symptom (often
    150+ entries, the long tail matching a single non-specific sign). The UI
    only ever shows ~18 cards plus a "show more" tail, so returning the full
    list bloats the response (multi-MB JSON) and wastes downstream enrichment
    CPU. The list is already ranked, so we keep the clinically relevant head
    and re-derive the phase buckets from the survivors (they reference the same
    dict objects, so identity matching keeps them consistent). Overall severity
    has already been computed from the full list upstream, so capping here does
    not change triage.
    """
    if not isinstance(result, dict):
        return
    sd = result.get("suspected_diseases")
    if not isinstance(sd, list) or len(sd) <= max_total:
        return
    capped = sd[:max_total]
    result["suspected_diseases"] = capped
    if isinstance(result.get("possible_conditions"), list):
        result["possible_conditions"] = capped
    kept_ids = {id(d) for d in capped}
    by_phase = result.get("suspected_diseases_by_phase")
    if isinstance(by_phase, dict):
        for phase_key, phase_diseases in by_phase.items():
            if isinstance(phase_diseases, list):
                by_phase[phase_key] = [d for d in phase_diseases if id(d) in kept_ids]


def _enrich_result_diseases(result, species):
    """Add completeness score + literature citations to each diagnosed disease.

    Mirrors the enrichment applied by /api/health-check/diseases so the
    differential-diagnosis view shows an accurate completeness badge and the
    same evidence-source / citation-map references as the Disease DB tab —
    instead of a hard-coded "100%" placeholder. Cheap (pure dict work) and
    safe: failures fall back to the unenriched result.
    """
    if enrich_disease_content is None:
        return
    sp = species or "dog"
    for diseases in _iter_result_disease_lists(result):
        for i, disease in enumerate(diseases):
            if not isinstance(disease, dict):
                continue
            try:
                diseases[i] = enrich_disease_content(disease, sp)
            except Exception:
                logger.exception("disease enrichment failed for %s", disease.get("name", "?"))


def _attach_recommended_tests_display(result, species):
    """Add a translated ``recommended_tests_display`` field to each disease.

    Disease modules emit ``recommended_tests`` as snake_case IDs
    (e.g. "complete_blood_count"). The UI needs both JA and EN labels per
    selected language, so we attach a parallel display list using the curated
    translations in ``health_checker._build_recommended_tests_display``. Costs
    a few µs per disease (in-memory dict lookup) — runs after capping so the
    cost scales only with the top-N differentials shown to the user.
    """
    try:
        from api.health_checker import _build_recommended_tests_display
    except Exception:
        return
    sp = species or "dog"

    # Per-disease enrichment
    for diseases in _iter_result_disease_lists(result):
        for disease in diseases:
            if not isinstance(disease, dict):
                continue
            if "recommended_tests_display" in disease:
                continue  # already supplied by a species handler
            tests = disease.get("recommended_tests")
            if not tests:
                continue
            try:
                disease["recommended_tests_display"] = _build_recommended_tests_display(tests, sp)
            except Exception:
                logger.exception(
                    "recommended_tests display enrichment failed for %s",
                    disease.get("name", "?"),
                )

    # Top-level aggregate enrichment
    if (
        isinstance(result, dict)
        and isinstance(result.get("recommended_tests"), list)
        and "recommended_tests_display" not in result
    ):
        try:
            result["recommended_tests_display"] = _build_recommended_tests_display(result["recommended_tests"], sp)
        except Exception:
            logger.exception("top-level recommended_tests display enrichment failed")


def _attach_mentioned_drugs(result, species):
    """Attach mentioned_drugs with species-specific dosage to each disease."""
    try:
        from api.drug_dictionary import DRUGS as _ALL_DRUGS
    except Exception:
        return

    disease_lists = []
    for key in ("suspected_diseases", "possible_conditions"):
        if key in result:
            disease_lists.append(result[key])
    by_phase = result.get("suspected_diseases_by_phase", {})
    for phase_diseases in by_phase.values():
        if isinstance(phase_diseases, list):
            disease_lists.append(phase_diseases)

    for diseases in disease_lists:
        for disease in diseases:
            treatment_text = (
                (disease.get("treatment_ja", "") or "") + " " + (disease.get("treatment", "") or "")
            ).lower()
            if not treatment_text.strip():
                continue
            matched = []
            for dr in _ALL_DRUGS:
                dr_name = dr.get("name", "")
                dr_name_ja = dr.get("name_ja", "")
                if not (
                    (dr_name and dr_name.lower() in treatment_text) or (dr_name_ja and dr_name_ja in treatment_text)
                ):
                    continue
                entry = {
                    "id": dr.get("id", ""),
                    "name": dr_name,
                    "name_ja": dr_name_ja,
                    "category": dr.get("category", ""),
                }
                si = (dr.get("species_info") or {}).get(species)
                if si:
                    entry["dosage"] = si.get("dosage", "")
                    entry["dosage_ja"] = si.get("dosage_ja", "")
                    entry["safe"] = si.get("safe", True)
                    entry["notes"] = si.get("notes", "")
                    entry["notes_ja"] = si.get("notes_ja", "")
                matched.append(entry)
                if len(matched) >= 10:
                    break
            if matched:
                disease["mentioned_drugs"] = matched


@app.route("/api/analyze-symptoms", methods=["POST"])
@ensure_json_response
def api_analyze_symptoms():
    """症状チェック → 疾患・検査リスト（全動物種対応）"""
    rate_err = _check_public_rate_limit()
    if rate_err:
        return rate_err
    if not SYMPTOM_CHECKER_AVAILABLE:
        return {"error": "Symptom checker module not available"}, 500

    data = request.get_json(silent=True)
    if not data or "symptoms" not in data:
        return {"error": "symptoms list required"}, 400

    symptoms, error, status = _normalize_string_list(
        data["symptoms"], "symptoms", singular_name="symptom", require_non_empty=True
    )
    if error:
        return error, status

    # Input size limits to prevent abuse
    MAX_SYMPTOMS = 50
    MAX_STRING_LEN = 256
    MAX_VACCINES = 20
    MAX_LAB_VALUES = 50

    if len(symptoms) > MAX_SYMPTOMS:
        return {"error": f"Too many symptoms (max {MAX_SYMPTOMS})"}, 400
    if any(len(s) > MAX_STRING_LEN for s in symptoms):
        return {"error": f"Symptom ID too long (max {MAX_STRING_LEN} chars)"}, 400

    species = data.get("species", "dog")
    if isinstance(species, str) and len(species) > MAX_STRING_LEN:
        return {"error": "species value too long"}, 400
    age_stage = data.get("age_stage")
    breed = data.get("breed")
    if isinstance(breed, str) and len(breed) > MAX_STRING_LEN:
        return {"error": "breed value too long"}, 400
    onset = data.get("onset")  # "acute" | "subacute" | "chronic"
    age_years = data.get("age_years")  # numeric age in years
    lab_values_raw = data.get("lab_values")  # {item_id: numeric_value}
    gender = data.get("gender")  # "male" | "female"
    vaccines_raw = data.get("vaccines", [])  # List of vaccine IDs
    vaccination_status = data.get("vaccination_status")  # "current" | "outdated" | "none"
    pain_score = data.get("pain_score")  # 0-4 (CSU Canine Acute Pain Scale)
    lang = data.get("lang", "")  # "ja" or "en" for regional prevalence adjustments

    # Validate onset
    if onset and onset not in ("acute", "subacute", "chronic"):
        return {"error": "onset must be 'acute', 'subacute', or 'chronic'"}, 400

    # Validate gender
    if gender and gender not in ("male", "female"):
        return {"error": "gender must be 'male' or 'female'"}, 400

    # Validate vaccination_status
    if vaccination_status and vaccination_status not in ("current", "outdated", "none"):
        return {"error": "vaccination_status must be 'current', 'outdated', or 'none'"}, 400

    # Validate pain_score (CSU Canine Pain Scale 0-4)
    if pain_score is not None:
        try:
            pain_score = int(pain_score)
            if pain_score < 0 or pain_score > 4:
                return {"error": "pain_score must be 0-4"}, 400
        except (ValueError, TypeError):
            return {"error": "pain_score must be an integer 0-4"}, 400

    # Coerce vaccines to list of strings
    vaccines = []
    if vaccines_raw is not None:
        vaccines, error, status = _normalize_string_list(vaccines_raw, "vaccines")
        if error:
            return error, status
        if len(vaccines) > MAX_VACCINES:
            return {"error": f"Too many vaccines (max {MAX_VACCINES})"}, 400

    # Coerce age_years to float and validate range
    if age_years is not None:
        try:
            age_years = float(age_years)
        except (ValueError, TypeError):
            return {"error": "age_years must be a number"}, 400
        if age_years < 0 or age_years > 100:
            return {"error": "age_years must be between 0 and 100"}, 400

    # Coerce lab_values to {str: float}
    lab_values = None
    if lab_values_raw is not None:
        if not isinstance(lab_values_raw, dict):
            return {"error": "lab_values must be a JSON object"}, 400
        if len(lab_values_raw) > MAX_LAB_VALUES:
            return {"error": f"Too many lab values (max {MAX_LAB_VALUES})"}, 400
        lab_values = {}
        for k, v in lab_values_raw.items():
            if not isinstance(k, str) or len(k) > MAX_STRING_LEN:
                return {"error": "lab_values keys must be strings"}, 400
            with contextlib.suppress(ValueError, TypeError):
                lab_values[str(k)] = float(v)
        if not lab_values:
            lab_values = None

    try:
        if species == "dog" or species is None:
            result = analyze_symptoms(
                symptoms,
                breed=breed,
                onset=onset,
                age_years=age_years,
                lab_values=lab_values,
                gender=gender,
                vaccines=vaccines,
                vaccination_status=vaccination_status,
                pain_score=pain_score,
            )
        else:
            if not SPECIES_ANALYZER_AVAILABLE:
                return {"error": "Species analyzer module not available"}, 500
            result = analyze_species_symptoms(
                species,
                symptoms,
                age_stage,
                breed=breed,
                onset=onset,
                age_years=age_years,
                lab_values=lab_values,
                gender=gender,
                vaccines=vaccines,
                vaccination_status=vaccination_status,
                lang=lang,
            )

        # Trim the long tail of single-symptom matches before the expensive
        # per-disease enrichment + drug-matching passes run, so we only do that
        # work for the differentials the UI actually shows.
        _cap_result_diseases(result)

        # Enrich each disease with completeness score + literature citations so
        # the differential view matches the Disease DB tab (accurate quality
        # badge + evidence sources), then attach species-specific drug dosing
        # and translated diagnostic-test labels.
        _enrich_result_diseases(result, species or "dog")
        _attach_recommended_tests_display(result, species or "dog")
        _attach_mentioned_drugs(result, species or "dog")

        return result
    except ValueError as ve:
        logger.error("Symptom analysis error: %s", ve, exc_info=True)
        return {"error": str(ve)}, 400
    except Exception as e:
        logger.error("Symptom analysis error: %s", e, exc_info=True)
        return {"error": "症状解析に失敗しました"}, 500


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
        "associated_conditions": [
            "fracture",
            "pancreatitis",
            "intervertebral_disc_disease",
            "moderate_otitis",
            "cystitis",
        ],
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
        "associated_conditions": [
            "gdv",
            "peritonitis",
            "severe_trauma",
            "bone_cancer",
            "acute_abdomen",
            "disc_herniation",
        ],
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
    2: {
        "Pancreatitis": 1.5,
        "Fracture": 1.4,
        "Intervertebral Disc Disease": 1.5,
        "Cystitis": 1.3,
        "Otitis Media": 1.3,
        "Gastric Foreign Body": 1.3,
        "Peritonitis": 1.2,
        "Osteosarcoma": 1.2,
    },
    3: {
        "Gastric Dilatation-Volvulus (GDV)": 1.6,
        "Peritonitis": 1.5,
        "Intervertebral Disc Disease": 1.4,
        "Osteosarcoma": 1.5,
        "Pancreatitis": 1.4,
        "Meningitis": 1.4,
        "Panosteitis": 1.3,
    },
    4: {
        "Gastric Dilatation-Volvulus (GDV)": 1.8,
        "Aortic Thromboembolism": 1.7,
        "Meningitis": 1.6,
        "Peritonitis": 1.6,
        "Necrotizing Fasciitis": 1.5,
    },
}


# =============================================================================
# API: Lab Reference Ranges
# =============================================================================


@app.route("/api/lab-ocr/text", methods=["POST"])
@ensure_json_response
def api_lab_parse_text():
    """Parse free-text lab report → structured {lab_id: value}.

    Body JSON: {text: "BUN 45 mg/dL ALT 220 U/L ..."}
    Response: {labs: {...}, count: int}
    """
    rate_limited = _check_public_rate_limit()
    if rate_limited:
        return rate_limited
    try:
        from api.lab_ocr import parse_lab_text
    except ImportError:
        return {"error": "Lab parser unavailable"}, 503
    data = request.get_json(silent=True) or {}
    text = str(data.get("text") or "").strip()
    if not text:
        return {"error": "text parameter required"}, 400
    if len(text) > 20000:
        return {"error": "text too long (max 20000 chars)"}, 413
    labs = parse_lab_text(text)
    return {"labs": labs, "count": len(labs)}


@app.route("/api/lab-ocr/image", methods=["POST"])
@ensure_json_response
def api_lab_parse_image():
    """OCR an uploaded image of a lab report → structured {lab_id: value}.

    Accepts: multipart/form-data with field 'image' (PNG/JPEG ≤8 MB), or
    JSON body {image_base64: "..."} for paste-from-clipboard flows.
    Response: {labs: {...}, ocr_text: str, meta: {...}}
    """
    rate_limited = _check_public_rate_limit()
    if rate_limited:
        return rate_limited
    try:
        from api.lab_ocr import extract_labs_from_image
    except ImportError:
        return {"error": "OCR module unavailable"}, 503

    image_bytes: bytes | None = None
    # Multipart upload path
    if "image" in request.files:
        f = request.files["image"]
        if f.filename:
            image_bytes = f.read()
    # JSON base64 path (for paste support)
    elif request.is_json:
        import base64

        b64 = (request.get_json(silent=True) or {}).get("image_base64", "")
        if isinstance(b64, str) and b64:
            # Allow optional data URL prefix
            if b64.startswith("data:") and "base64," in b64:
                b64 = b64.split("base64,", 1)[1]
            try:
                image_bytes = base64.b64decode(b64)
            except (ValueError, TypeError):
                return {"error": "invalid base64 image data"}, 400

    if not image_bytes:
        return {"error": "image (multipart) or image_base64 (JSON) required"}, 400
    if len(image_bytes) > 8 * 1024 * 1024:
        return {"error": "image too large (max 8 MB)"}, 413

    try:
        result = extract_labs_from_image(image_bytes)
    except RuntimeError as exc:
        # Most common cause: Tesseract not installed on host
        logger.warning("Lab OCR failed: %s", exc)
        return {"error": str(exc), "fallback": "Use /api/lab-ocr/text with manually typed values"}, 503
    except Exception as exc:  # noqa: BLE001 — sanitize OCR errors
        logger.exception("Unexpected lab OCR error")
        return {"error": f"OCR processing error: {type(exc).__name__}"}, 500
    return result


@app.route("/api/lab-ranges/<species>", methods=["GET"])
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


@app.route("/api/pain-scale", methods=["GET"])
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


@app.route("/api/breeds/<species>", methods=["GET"])
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
        "breeds": [
            {
                "id": b["id"],
                "name": b["name"],
                "name_ja": b["name_ja"],
                "ecology": b.get("ecology"),
            }
            for b in breeds
        ],
    }


@app.route("/api/species/<species>/husbandry", methods=["GET"])
@ensure_json_response
def api_species_husbandry(species: str):
    """Return husbandry / care environment data for a species."""
    try:
        from api.species_husbandry import HUSBANDRY_DATA
    except ImportError:
        from species_husbandry import HUSBANDRY_DATA
    species_key = (species or "").lower()
    data = HUSBANDRY_DATA.get(species_key)
    if not data:
        return {"error": "No husbandry data for this species"}, 404
    return {"species": species_key, "husbandry": data}


@app.route("/api/species/<species>/common-diseases", methods=["GET"])
@ensure_json_response
def api_common_diseases(species):
    """Return common/very_common diseases for a species with Japanese names."""
    try:
        from api.species.prevalence_data import SPECIES_PREVALENCE
    except ImportError:
        from species.prevalence_data import SPECIES_PREVALENCE
    prev = SPECIES_PREVALENCE.get(species, {})
    # Load disease data to get Japanese names (lazy-loaded; trigger via accessor)
    try:
        from api.chat.species_data import get_species_data
    except ImportError:
        try:
            from chat.species_data import get_species_data
        except ImportError:
            get_species_data = lambda _s: {}  # noqa: E731
    sp_data = get_species_data(species)
    diseases_list = sp_data.get("diseases", [])
    name_map = {}
    for d in diseases_list:
        name_map[d.get("name", "")] = d.get("name_ja", "")
    result = []
    for name, tier in prev.items():
        if tier in ("very_common", "common"):
            result.append(
                {
                    "name": name,
                    "name_ja": name_map.get(name, ""),
                    "prevalence": tier,
                }
            )
    # Sort: very_common first, then common
    result.sort(key=lambda x: (0 if x["prevalence"] == "very_common" else 1, x["name"]))
    return {"species": species, "common_diseases": result}


# =============================================================================
# API: RECO2 / RECO3 (AI Integrity Control)
# =============================================================================


@app.route("/api/status", methods=["GET"])
@ensure_json_response
@require_internal_api_access
def reco2_status_route():
    if not RECO2_AVAILABLE:
        return {"error": "reco2 not available"}, 503
    return reco2_get_status()


@app.route("/api/logs", methods=["GET"])
@ensure_json_response
@require_internal_api_access
def reco2_logs_route():
    if not RECO2_AVAILABLE:
        return {"error": "reco2 not available"}, 503
    try:
        limit = max(1, min(int(request.args.get("limit", "50")), 500))
    except (ValueError, TypeError):
        limit = 50
    return reco2_get_logs(limit=limit)


@app.route("/api/evaluate", methods=["POST"])
@ensure_json_response
@require_internal_api_access
def reco2_evaluate_route():
    if not RECO2_AVAILABLE:
        return {"error": "reco2 not available"}, 503
    payload = request.get_json(force=True, silent=False)
    return reco2_evaluate_payload(payload)


@app.route("/api/feedback", methods=["POST"])
@ensure_json_response
@require_internal_api_access
def reco2_feedback_route():
    if not RECO2_AVAILABLE:
        return {"error": "reco2 not available"}, 503
    payload = request.get_json(force=True, silent=True) or {}
    res = reco2_record_feedback(payload)
    if isinstance(res, tuple):
        return res[0], res[1]
    return res


@app.route("/api/patrol", methods=["POST"])
@ensure_json_response
@require_internal_api_access
def reco2_patrol_route():
    if not RECO2_AVAILABLE:
        return {"error": "reco2 not available"}, 503
    return reco2_patrol(manual=True)


@app.route("/api/r3/analyze_input", methods=["POST"])
@ensure_json_response
@require_internal_api_access
def reco3_analyze_input():
    if not RECO2_AVAILABLE:
        return {"error": "reco2 not available"}, 503
    data = request.get_json(force=True, silent=True) or {}
    text = str(data.get("text", ""))
    cfg = load_reco2_config()
    return input_gate.analyze(
        text,
        w_ambiguity=float(cfg.get("input_w_ambiguity", 0.20)),
        w_assertion=float(cfg.get("input_w_assertion", 0.25)),
        w_emotion=float(cfg.get("input_w_emotion", 0.30)),
        w_unrealistic=float(cfg.get("input_w_unrealistic", 0.25)),
    )


@app.route("/api/r3/analyze_output", methods=["POST"])
@ensure_json_response
@require_internal_api_access
def reco3_analyze_output():
    if not RECO2_AVAILABLE:
        return {"error": "reco2 not available"}, 503
    data = request.get_json(force=True, silent=True) or {}
    text = str(data.get("text", ""))
    cfg = load_reco2_config()
    return output_gate.analyze(
        text,
        w_assertion=float(cfg.get("output_w_assertion", 0.30)),
        w_evidence=float(cfg.get("output_w_evidence", 0.30)),
        w_contradiction=float(cfg.get("output_w_contradiction", 0.25)),
        w_provocative=float(cfg.get("output_w_provocative", 0.15)),
    )


@app.route("/api/r3/chat", methods=["POST"])
@ensure_json_response
@require_internal_api_access
def reco3_chat():
    if not RECO2_AVAILABLE:
        return {"error": "reco2 not available"}, 503
    data = request.get_json(force=True, silent=True) or {}
    prompt = str(data.get("prompt", ""))
    domain = str(data.get("domain", "general"))
    max_tokens = int(data.get("max_tokens", 1024) or 1024)
    orch = reco2_get_orchestrator()
    return orch.process(prompt, domain=domain, context=data.get("context") or {}, max_tokens=max_tokens)


@app.route("/api/r3/config", methods=["GET"])
@ensure_json_response
@require_internal_api_access
def reco3_config():
    if not RECO2_AVAILABLE:
        return {"error": "reco2 not available"}, 503
    return public_reco2_config(load_reco2_config())


# =============================================================================
# API: Admin Token Verification
# =============================================================================


@app.route("/api/admin/verify", methods=["POST"])
def verify_admin():
    """Server-side admin token verification."""
    body = request.get_json(silent=True) or {}
    token = body.get("token", "")
    admin_token = os.getenv("ADMIN_TOKEN", "")
    if not admin_token:
        return jsonify({"valid": False}), 403
    import hmac

    if hmac.compare_digest(token, admin_token):
        return jsonify({"valid": True})
    return jsonify({"valid": False}), 403


# =============================================================================
# Error Handlers
# =============================================================================


def _wants_html_response() -> bool:
    """True when the client prefers HTML (browser navigation) over JSON."""
    path = request.path or ""
    if path.startswith("/api/"):
        return False
    accept = request.accept_mimetypes
    # Default to HTML for non-API paths unless the client explicitly wants JSON
    return accept.best_match(["text/html", "application/json"]) != "application/json"


@app.errorhandler(404)
def not_found(e):
    if _wants_html_response():
        try:
            return render_template("404.html"), 404
        except Exception:
            logger.warning("404 template render failed", exc_info=True)
    return jsonify({"error": "Not found", "version": VERSION}), 404


@app.errorhandler(429)
def rate_limited(e):
    if _wants_html_response():
        return (
            "<!doctype html><meta charset='utf-8'><title>429 Too Many Requests</title>"
            "<body style='font-family:system-ui,sans-serif;max-width:560px;margin:60px auto;padding:0 20px;text-align:center'>"
            "<h1 style='color:#1a3068'>429 — Too Many Requests</h1>"
            "<p>" + RATE_LIMIT_ERROR_MESSAGE + " / Please slow down and try again in a moment.</p>"
            "<p><a href='/' style='color:#22a84f;font-weight:600'>← Home</a></p></body>",
            429,
            {"Content-Type": "text/html; charset=utf-8"},
        )
    return jsonify({"error": RATE_LIMIT_ERROR_MESSAGE, "version": VERSION}), 429


@app.errorhandler(500)
def server_error(e):
    logger.error("500: %s", e, exc_info=True)
    if _wants_html_response():
        return (
            "<!doctype html><meta charset='utf-8'><title>500 Server Error</title>"
            "<body style='font-family:system-ui,sans-serif;max-width:560px;margin:60px auto;padding:0 20px;text-align:center'>"
            "<h1 style='color:#1a3068'>500 — Server Error</h1>"
            "<p>サーバー内部でエラーが発生しました。 / An internal error occurred. Please try again later.</p>"
            "<p><a href='/' style='color:#22a84f;font-weight:600'>← Home</a></p></body>",
            500,
            {"Content-Type": "text/html; charset=utf-8"},
        )
    return jsonify({"error": "Internal server error", "version": VERSION}), 500


# =============================================================================
# API v1 aliases — versioned endpoints pointing to existing handlers
# =============================================================================

app.add_url_rule("/api/v1/health", endpoint="v1_health", view_func=health, methods=["GET"])
app.add_url_rule("/api/v1/species-stats", endpoint="v1_species_stats", view_func=api_species_stats, methods=["GET"])
app.add_url_rule(
    "/api/v1/analyze-symptoms", endpoint="v1_analyze_symptoms", view_func=api_analyze_symptoms, methods=["POST"]
)
app.add_url_rule("/api/v1/breeds/<species>", endpoint="v1_breeds", view_func=api_get_breeds, methods=["GET"])

if SYMPTOM_CHECKER_AVAILABLE:
    app.add_url_rule(
        "/api/v1/species/<species>/symptoms",
        endpoint="v1_species_symptoms",
        view_func=api_species_symptoms,
        methods=["GET"],
    )


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    logger.info("VetDict v%s starting on port %s", VERSION, port)
    logger.info("Symptom checker: %s", SYMPTOM_CHECKER_AVAILABLE)
    logger.info("Species analyzer: %s", SPECIES_ANALYZER_AVAILABLE)
    logger.info("Health checker: %s", HEALTH_CHECKER_AVAILABLE)
    logger.info("Diagnostic chat: %s", DIAGNOSTIC_CHAT_AVAILABLE)
    logger.info("RECO2: %s", RECO2_AVAILABLE)
    app.run(host="0.0.0.0", port=port, debug=is_debug_mode_enabled())
