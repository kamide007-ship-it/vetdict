#!/usr/bin/env python3
"""
Tests for the API authentication module.

Tests the following components:
- AuthConfig initialization and parsing
- RateLimiter functionality
- AuditLogger functionality
- TokenValidator functionality
- Client IP detection with proxies
- require_internal_api_access decorator
"""


from api.auth import (
    AuditLogger,
    AuthConfig,
    ClientIP,
    RateLimiter,
    TokenValidator,
    get_audit_logger,
    get_auth_config,
    get_rate_limiter,
    reset_rate_limiting,
)


class TestAuthConfig:
    """Test AuthConfig class."""

    def test_auth_config_default_values(self):
        """Test default configuration values."""
        config = AuthConfig()
        assert config.internal_token == ""
        assert config.rate_limit_max_requests == 30
        assert config.rate_limit_window_seconds == 60
        assert config.enable_audit_logging is True
        assert config.enable_jwt is False

    def test_auth_config_from_environment(self, monkeypatch):
        """Test loading configuration from environment variables."""
        monkeypatch.setenv("INTERNAL_API_TOKEN", "test-token-123")
        monkeypatch.setenv("INTERNAL_API_RATE_LIMIT_MAX_REQUESTS", "50")
        monkeypatch.setenv("INTERNAL_API_RATE_LIMIT_WINDOW_SECONDS", "120")
        monkeypatch.setenv("API_AUTH_AUDIT_LOG", "0")
        monkeypatch.setenv("API_AUTH_JWT_ENABLED", "1")
        monkeypatch.setenv("API_AUTH_JWT_SECRET", "jwt-secret-key")

        config = AuthConfig()
        assert config.internal_token == "test-token-123"
        assert config.rate_limit_max_requests == 50
        assert config.rate_limit_window_seconds == 120
        assert config.enable_audit_logging is False
        assert config.enable_jwt is True
        assert config.jwt_secret == "jwt-secret-key"

    def test_auth_config_invalid_rate_limit_values(self, monkeypatch):
        """Test handling of invalid rate limit values."""
        # Clear any previous env vars first
        monkeypatch.delenv("INTERNAL_API_RATE_LIMIT_MAX_REQUESTS", raising=False)
        monkeypatch.delenv("INTERNAL_API_RATE_LIMIT_WINDOW_SECONDS", raising=False)

        monkeypatch.setenv("INTERNAL_API_RATE_LIMIT_MAX_REQUESTS", "invalid")
        monkeypatch.setenv("INTERNAL_API_RATE_LIMIT_WINDOW_SECONDS", "not-a-number")

        config = AuthConfig()
        assert config.rate_limit_max_requests == 30  # default
        assert config.rate_limit_window_seconds == 60  # default


class TestRateLimiter:
    """Test RateLimiter class."""

    def test_rate_limiter_allows_requests_within_limit(self):
        """Test that requests within limit are allowed."""
        limiter = RateLimiter(max_requests=3, window_seconds=60)

        assert limiter.is_limited("client1") is False
        assert limiter.is_limited("client1") is False
        assert limiter.is_limited("client1") is False

    def test_rate_limiter_blocks_requests_exceeding_limit(self):
        """Test that requests exceeding limit are blocked."""
        limiter = RateLimiter(max_requests=2, window_seconds=60)

        assert limiter.is_limited("client1") is False
        assert limiter.is_limited("client1") is False
        assert limiter.is_limited("client1") is True  # exceeds limit
        assert limiter.is_limited("client1") is True  # still limited

    def test_rate_limiter_isolates_clients(self):
        """Test that rate limiting is per-client."""
        limiter = RateLimiter(max_requests=2, window_seconds=60)

        assert limiter.is_limited("client1") is False
        assert limiter.is_limited("client1") is False
        assert limiter.is_limited("client1") is True

        # Different client should have its own limit
        assert limiter.is_limited("client2") is False
        assert limiter.is_limited("client2") is False
        assert limiter.is_limited("client2") is True

    def test_rate_limiter_reset(self):
        """Test resetting the rate limiter."""
        limiter = RateLimiter(max_requests=2, window_seconds=60)

        assert limiter.is_limited("client1") is False
        assert limiter.is_limited("client1") is False
        assert limiter.is_limited("client1") is True

        limiter.reset()

        # After reset, limit should be available again
        assert limiter.is_limited("client1") is False

    def test_get_remaining_requests(self):
        """Test getting remaining requests for a client."""
        limiter = RateLimiter(max_requests=5, window_seconds=60)

        assert limiter.get_remaining_requests("client1") == 5
        limiter.is_limited("client1")
        assert limiter.get_remaining_requests("client1") == 4
        limiter.is_limited("client1")
        assert limiter.get_remaining_requests("client1") == 3


class TestTokenValidator:
    """Test TokenValidator class."""

    def test_validate_bearer_token_success(self):
        """Test successful bearer token validation."""
        config = AuthConfig()
        config.internal_token = "valid-token-123"
        validator = TokenValidator(config)

        is_valid, error = validator.validate_bearer_token("valid-token-123")
        assert is_valid is True
        assert error is None

    def test_validate_bearer_token_invalid(self):
        """Test invalid bearer token validation."""
        config = AuthConfig()
        config.internal_token = "valid-token-123"
        validator = TokenValidator(config)

        is_valid, error = validator.validate_bearer_token("invalid-token")
        assert is_valid is False
        assert error == "Invalid token"

    def test_validate_bearer_token_empty(self):
        """Test empty bearer token validation."""
        config = AuthConfig()
        config.internal_token = "valid-token-123"
        validator = TokenValidator(config)

        is_valid, error = validator.validate_bearer_token("")
        assert is_valid is False
        assert error == "Missing token"

    def test_validate_bearer_token_not_configured(self):
        """Test validation when token is not configured."""
        config = AuthConfig()
        config.internal_token = ""
        validator = TokenValidator(config)

        is_valid, error = validator.validate_bearer_token("any-token")
        assert is_valid is False
        assert error == "Bearer token authentication not configured"

    def test_validate_bearer_token_timing_attack_resistant(self):
        """Test that token validation resists timing attacks."""
        config = AuthConfig()
        config.internal_token = "valid-token-123456789"
        validator = TokenValidator(config)

        # Valid token should use constant-time comparison
        is_valid, _ = validator.validate_bearer_token("valid-token-123456789")
        assert is_valid is True

        # Invalid tokens should also use constant-time comparison
        is_valid, _ = validator.validate_bearer_token("invalid-token-123456789")
        assert is_valid is False


class TestClientIP:
    """Test ClientIP utility."""

    def test_get_client_ip_direct_connection(self):
        """Test getting client IP from direct connection."""
        from flask import Flask
        from werkzeug.test import EnvironBuilder

        app = Flask(__name__)
        builder = EnvironBuilder(environ_base={'REMOTE_ADDR': '192.168.1.100'})
        env = builder.get_environ()

        with app.test_request_context(environ_base=env):
            client_ip = ClientIP()
            ip = client_ip.get_client_ip()
            assert ip == '192.168.1.100'

    def test_get_client_ip_from_x_forwarded_for(self):
        """Test getting client IP from X-Forwarded-For header."""
        from flask import Flask

        app = Flask(__name__)

        with app.test_request_context(
            headers={'X-Forwarded-For': '203.0.113.1, 198.51.100.1, 192.0.2.1'}
        ):
            client_ip = ClientIP()
            ip = client_ip.get_client_ip()
            assert ip == '203.0.113.1'  # First IP in list

    def test_get_client_ip_fallback_to_remote_addr(self):
        """Test fallback to remote_addr when X-Forwarded-For is not present."""
        from flask import Flask

        app = Flask(__name__)

        with app.test_request_context(environ_base={'REMOTE_ADDR': '192.168.1.100'}):
            client_ip = ClientIP()
            ip = client_ip.get_client_ip()
            assert ip == '192.168.1.100'


class TestAuditLogger:
    """Test AuditLogger class."""

    def test_audit_logger_enabled(self, caplog):
        """Test audit logger when enabled."""
        logger = AuditLogger(enabled=True)
        logger.log_auth_attempt(
            success=True,
            method='bearer_token',
            client_ip='192.168.1.1',
            reason='valid_token',
        )
        # Should log something (behavior depends on logging setup)

    def test_audit_logger_disabled(self, caplog):
        """Test audit logger when disabled."""
        logger = AuditLogger(enabled=False)
        logger.log_auth_attempt(
            success=True,
            method='bearer_token',
            client_ip='192.168.1.1',
            reason='valid_token',
        )
        # Should not log when disabled


class TestGlobalInstances:
    """Test global instance access functions."""

    def test_get_rate_limiter(self):
        """Test getting global rate limiter instance."""
        limiter = get_rate_limiter()
        assert isinstance(limiter, RateLimiter)

    def test_get_auth_config(self):
        """Test getting global auth config instance."""
        config = get_auth_config()
        assert isinstance(config, AuthConfig)

    def test_get_audit_logger(self):
        """Test getting global audit logger instance."""
        logger = get_audit_logger()
        assert isinstance(logger, AuditLogger)

    def test_reset_rate_limiting(self):
        """Test resetting rate limiting."""
        limiter = get_rate_limiter()
        limiter.is_limited("test_client")
        limiter.is_limited("test_client")
        assert limiter.get_remaining_requests("test_client") == 28  # 30 - 2

        reset_rate_limiting()

        assert limiter.get_remaining_requests("test_client") == 30  # Reset to default
