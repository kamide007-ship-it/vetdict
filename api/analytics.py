"""Lightweight server-side analytics using SQLite.

Records anonymous API usage statistics without collecting PII.
"""

import sqlite3
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from functools import wraps

from flask import Blueprint, jsonify, request

from api.database import DB_PATH, _ensure_dir

analytics_bp = Blueprint("analytics", __name__, url_prefix="/api/admin/analytics")

ANALYTICS_SCHEMA = """\
CREATE TABLE IF NOT EXISTS api_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    endpoint TEXT NOT NULL,
    method TEXT NOT NULL DEFAULT 'GET',
    species TEXT,
    status_code INTEGER,
    response_time_ms REAL,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
);

CREATE INDEX IF NOT EXISTS idx_usage_endpoint ON api_usage(endpoint);
CREATE INDEX IF NOT EXISTS idx_usage_created ON api_usage(created_at);
CREATE INDEX IF NOT EXISTS idx_usage_species ON api_usage(species);
"""


@contextmanager
def _get_analytics_conn():
    path = DB_PATH
    _ensure_dir(path)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_analytics():
    """Create analytics tables if they don't exist."""
    with _get_analytics_conn() as conn:
        conn.executescript(ANALYTICS_SCHEMA)


def record_api_call(
    endpoint: str,
    method: str = "GET",
    species: str | None = None,
    status_code: int = 200,
    response_time_ms: float = 0.0,
) -> None:
    """Record a single API call."""
    try:
        with _get_analytics_conn() as conn:
            conn.execute(
                "INSERT INTO api_usage (endpoint, method, species, status_code, response_time_ms) VALUES (?,?,?,?,?)",
                (endpoint, method, species, status_code, response_time_ms),
            )
    except Exception:
        pass  # Never let analytics break the main request


def track_request(f):
    """Decorator to automatically record API usage."""

    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time.monotonic()
        result = f(*args, **kwargs)
        elapsed = (time.monotonic() - start) * 1000

        status = 200
        if isinstance(result, tuple) and len(result) >= 2:
            status = result[1]

        species = request.args.get("species") or request.view_args.get("species") if request.view_args else None

        record_api_call(
            endpoint=request.endpoint or request.path,
            method=request.method,
            species=species,
            status_code=status,
            response_time_ms=round(elapsed, 2),
        )
        return result

    return wrapper


# ---------------------------------------------------------------------------
# Analytics API endpoints
# ---------------------------------------------------------------------------


@analytics_bp.route("/summary", methods=["GET"])
def analytics_summary():
    """Return usage summary statistics."""
    with _get_analytics_conn() as conn:
        total = conn.execute("SELECT COUNT(*) FROM api_usage").fetchone()[0]
        by_endpoint = conn.execute(
            "SELECT endpoint, COUNT(*) as cnt FROM api_usage GROUP BY endpoint ORDER BY cnt DESC LIMIT 20"
        ).fetchall()
        by_species = conn.execute(
            "SELECT species, COUNT(*) as cnt FROM api_usage WHERE species IS NOT NULL GROUP BY species ORDER BY cnt DESC"
        ).fetchall()
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        today_count = conn.execute("SELECT COUNT(*) FROM api_usage WHERE created_at >= ?", (today,)).fetchone()[0]
        avg_response = conn.execute(
            "SELECT AVG(response_time_ms) FROM api_usage WHERE response_time_ms > 0"
        ).fetchone()[0]

    return jsonify(
        {
            "success": True,
            "total_requests": total,
            "today_requests": today_count,
            "avg_response_time_ms": round(avg_response or 0, 2),
            "top_endpoints": {r["endpoint"]: r["cnt"] for r in by_endpoint},
            "by_species": {r["species"]: r["cnt"] for r in by_species},
        }
    )


@analytics_bp.route("/daily", methods=["GET"])
def analytics_daily():
    """Return daily request counts for the last 30 days."""
    with _get_analytics_conn() as conn:
        rows = conn.execute(
            """SELECT date(created_at) as day, COUNT(*) as cnt
               FROM api_usage
               WHERE created_at >= date('now', '-30 days')
               GROUP BY day ORDER BY day"""
        ).fetchall()
    return jsonify(
        {
            "success": True,
            "daily": {r["day"]: r["cnt"] for r in rows},
        }
    )
