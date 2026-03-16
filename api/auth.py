#!/usr/bin/env python3
"""
VetDict API Authentication Module

Provides production-grade API authentication including:
- Bearer token validation
- API key management
- Rate limiting
- Audit logging
- Support for multiple authentication methods
"""

import hashlib
import hmac
import logging
import os
import threading
import time
from collections import deque
from datetime import datetime, timedelta
from functools import wraps
from typing import Callable, Dict, Optional, Tuple

from flask import jsonify, request

logger = logging.getLogger(__name__)


class AuthConfig:
    """Configuration for API authentication."""

    def __init__(self):
        self.internal_token = (os.getenv('INTERNAL_API_TOKEN') or '').strip()
        self.rate_limit_max_requests = self._parse_int(
            os.getenv('INTERNAL_API_RATE_LIMIT_MAX_REQUESTS', '30'), default=30
        )
        self.rate_limit_window_seconds = self._parse_int(
            os.getenv('INTERNAL_API_RATE_LIMIT_WINDOW_SECONDS', '60'), default=60
        )
        self.enable_audit_logging = os.getenv('API_AUTH_AUDIT_LOG', '1').lower() in ('1', 'true', 'yes')
        self.enable_jwt = os.getenv('API_AUTH_JWT_ENABLED', '0').lower() in ('1', 'true', 'yes')
        self.jwt_secret = (os.getenv('API_AUTH_JWT_SECRET') or '').strip()
        self.trusted_proxies = (os.getenv('TRUSTED_PROXIES') or '').split(',')

    @staticmethod
    def _parse_int(value: str, default: int = 30) -> int:
        """Parse positive integer from environment variable."""
        try:
            return max(1, int(value))
        except (TypeError, ValueError):
            return default


class RateLimiter:
    """Thread-safe rate limiter for API requests."""

    def __init__(self, max_requests: int = 30, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.buckets: Dict[str, deque] = {}
        self.lock = threading.Lock()

    def is_limited(self, bucket_key: str) -> bool:
        """Check if request is rate limited."""
        now = time.monotonic()
        cutoff = now - self.window_seconds

        with self.lock:
            self._prune_buckets(cutoff)
            bucket = self.buckets.setdefault(bucket_key, deque())

            if len(bucket) >= self.max_requests:
                return True

            bucket.append(now)
            return False

    def _prune_buckets(self, cutoff: float) -> None:
        """Remove old entries from all buckets."""
        for key in list(self.buckets):
            bucket = self.buckets[key]
            while bucket and bucket[0] <= cutoff:
                bucket.popleft()
            if not bucket:
                self.buckets.pop(key, None)

    def reset(self) -> None:
        """Reset all rate limit buckets."""
        with self.lock:
            self.buckets.clear()

    def get_remaining_requests(self, bucket_key: str) -> int:
        """Get remaining requests for a bucket."""
        now = time.monotonic()
        cutoff = now - self.window_seconds

        with self.lock:
            bucket = self.buckets.get(bucket_key, deque())
            valid_requests = sum(1 for t in bucket if t > cutoff)
            return max(0, self.max_requests - valid_requests)


class AuditLogger:
    """Logs authentication events for audit trails."""

    def __init__(self, enabled: bool = True):
        self.enabled = enabled
        self.logger = logging.getLogger(__name__)
        self.auth_log = logging.getLogger(f"{__name__}.auth")

    def log_auth_attempt(
        self,
        success: bool,
        method: str,
        client_ip: str,
        reason: Optional[str] = None,
        metadata: Optional[dict] = None,
    ) -> None:
        """Log an authentication attempt."""
        if not self.enabled:
            return

        timestamp = datetime.utcnow().isoformat()
        log_entry = {
            'timestamp': timestamp,
            'success': success,
            'method': method,
            'client_ip': client_ip,
            'reason': reason,
            'metadata': metadata or {},
        }

        log_level = logging.INFO if success else logging.WARNING
        self.auth_log.log(
            log_level,
            f"Auth {'success' if success else 'failure'}: {method} from {client_ip} - {reason}"
        )


class TokenValidator:
    """Validates various types of authentication tokens."""

    def __init__(self, config: AuthConfig):
        self.config = config

    def validate_bearer_token(self, token: str) -> Tuple[bool, Optional[str]]:
        """Validate Bearer token."""
        if not self.config.internal_token:
            return False, "Bearer token authentication not configured"

        if not token:
            return False, "Missing token"

        # Use constant-time comparison to prevent timing attacks
        if hmac.compare_digest(token, self.config.internal_token):
            return True, None

        return False, "Invalid token"

    def validate_api_key(self, api_key: str) -> Tuple[bool, Optional[str]]:
        """Validate API key (future implementation)."""
        # This can be extended to validate against a database of API keys
        return False, "API key validation not yet implemented"

    def validate_jwt(self, token: str) -> Tuple[bool, Optional[str]]:
        """Validate JWT token (future implementation)."""
        if not self.config.enable_jwt:
            return False, "JWT authentication not enabled"

        if not self.config.jwt_secret:
            return False, "JWT secret not configured"

        # JWT validation would be implemented here
        return False, "JWT validation not yet implemented"


class ClientIP:
    """Utility for getting client IP with proxy support."""

    def __init__(self, trusted_proxies: list = None):
        self.trusted_proxies = trusted_proxies or []

    def get_client_ip(self) -> str:
        """Get client IP address, accounting for proxies."""
        # Check X-Forwarded-For if behind a trusted proxy
        if 'X-Forwarded-For' in request.headers:
            # X-Forwarded-For can have multiple IPs, get the first one
            ips = request.headers.get('X-Forwarded-For', '').split(',')
            if ips:
                return ips[0].strip()

        # Fall back to remote_addr
        return request.remote_addr or 'unknown'


# Global instances
_auth_config = AuthConfig()
_rate_limiter = RateLimiter(
    max_requests=_auth_config.rate_limit_max_requests,
    window_seconds=_auth_config.rate_limit_window_seconds,
)
_audit_logger = AuditLogger(enabled=_auth_config.enable_audit_logging)
_token_validator = TokenValidator(_auth_config)
_client_ip = ClientIP(trusted_proxies=_auth_config.trusted_proxies)


def require_internal_api_access(f: Callable) -> Callable:
    """
    Decorator to require internal API access with Bearer token authentication.

    Expects: Authorization: Bearer <token>
    Enforces rate limiting and logs authentication attempts.
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        version_str = 'unknown'
        try:
            from api.vetdict_api import VERSION
            version_str = VERSION
        except (ImportError, AttributeError):
            pass

        # Re-read configuration on each request to support testing with monkeypatch
        current_config = AuthConfig()
        token_validator = TokenValidator(current_config)

        # Get client IP
        client_ip = _client_ip.get_client_ip()

        # Update rate limiter config if it has changed
        if (_rate_limiter.max_requests != current_config.rate_limit_max_requests or
            _rate_limiter.window_seconds != current_config.rate_limit_window_seconds):
            _rate_limiter.max_requests = current_config.rate_limit_max_requests
            _rate_limiter.window_seconds = current_config.rate_limit_window_seconds

        # Check rate limiting first (before validation) to prevent brute force
        if _rate_limiter.is_limited(client_ip):
            _audit_logger.log_auth_attempt(
                success=False,
                method='bearer_token',
                client_ip=client_ip,
                reason='rate_limited',
            )
            return (
                jsonify({
                    'success': False,
                    'error': 'リクエスト制限に達しました。',
                    'version': version_str,
                }),
                429,
            )

        # Parse Authorization header
        auth_header = (request.headers.get('Authorization') or '').strip()
        auth_scheme, _, provided_token = auth_header.partition(' ')

        # Check if token is provided and scheme is correct
        if not current_config.internal_token:
            if os.getenv('FLASK_DEBUG', '0').strip().lower() in ('1', 'true', 'yes', 'on'):
                logger.warning("INTERNAL_API_TOKEN not set — allowing unauthenticated access (debug mode)")
                return f(*args, **kwargs)
            else:
                logger.error("INTERNAL_API_TOKEN not configured in production")
                return (
                    jsonify({
                        'success': False,
                        'error': 'Server misconfiguration',
                        'version': version_str,
                    }),
                    500,
                )

        if auth_scheme != 'Bearer':
            _audit_logger.log_auth_attempt(
                success=False,
                method='bearer_token',
                client_ip=client_ip,
                reason='invalid_scheme',
            )
            return (
                jsonify({
                    'success': False,
                    'error': 'Unauthorized',
                    'version': version_str,
                }),
                401,
            )

        # Validate token
        is_valid, error_reason = token_validator.validate_bearer_token(provided_token)

        if not is_valid:
            _audit_logger.log_auth_attempt(
                success=False,
                method='bearer_token',
                client_ip=client_ip,
                reason=error_reason or 'invalid_token',
            )
            return (
                jsonify({
                    'success': False,
                    'error': 'Unauthorized',
                    'version': version_str,
                }),
                401,
            )

        # Log successful authentication
        _audit_logger.log_auth_attempt(
            success=True,
            method='bearer_token',
            client_ip=client_ip,
            reason='valid_token',
        )

        # Call the original function
        return f(*args, **kwargs)

    return wrapper


def get_rate_limiter() -> RateLimiter:
    """Get the global rate limiter instance."""
    return _rate_limiter


def get_auth_config() -> AuthConfig:
    """Get the authentication configuration."""
    return _auth_config


def get_audit_logger() -> AuditLogger:
    """Get the audit logger instance."""
    return _audit_logger


def reset_rate_limiting() -> None:
    """Reset all rate limiting buckets (useful for testing)."""
    _rate_limiter.reset()
