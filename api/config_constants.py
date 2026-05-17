"""
Application-wide constants for VetDict Analysis Platform.

All hardcoded values should be defined here to centralise configuration.
"""

# ---------------------------------------------------------------------------
# File Upload
# ---------------------------------------------------------------------------
UPLOAD_MAX_SIZE_BYTES = 50 * 1024 * 1024  # 50MB
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}
ALLOWED_VIDEO_EXTENSIONS = {".mp4", ".mov", ".webm"}

# ---------------------------------------------------------------------------
# Timeout settings (seconds)
# ---------------------------------------------------------------------------
AI_API_TIMEOUT_SECONDS = 30.0
SUBPROCESS_TIMEOUT_SECONDS = 60
SUBPROCESS_QUICK_TIMEOUT_SECONDS = 10
SMTP_TIMEOUT_SECONDS = 10

# ---------------------------------------------------------------------------
# Security
# ---------------------------------------------------------------------------
COOKIE_MAX_AGE_SECONDS = 86400  # 24 hours

# ---------------------------------------------------------------------------
# Rate limiting
# ---------------------------------------------------------------------------
RATE_LIMIT_PER_DAY = 200
RATE_LIMIT_PER_HOUR = 50
RATE_LIMIT_WINDOW_SECONDS = 600  # 10 minutes

# ---------------------------------------------------------------------------
# Default values
# ---------------------------------------------------------------------------
DEFAULT_BREED_ID = "172d_poodle_toy"
DEFAULT_LANGUAGE = "ja"

# ---------------------------------------------------------------------------
# Pagination
# ---------------------------------------------------------------------------
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100

# ---------------------------------------------------------------------------
# AI Symptom Extraction (Phase 1)
# ---------------------------------------------------------------------------
AI_SYMPTOM_EXTRACTION_ENABLED_DEFAULT = False
AI_SYMPTOM_EXTRACTION_TIMEOUT = 30.0
AI_SYMPTOM_CACHE_TTL = 3600  # 1 hour
AI_SYMPTOM_CONFIDENCE_THRESHOLD = 0.7
AI_SYMPTOM_FALLBACK_ENABLED = True
AI_SYMPTOM_MODEL = "claude-opus-4-6"
