# VetDict API Authentication

Production-grade API authentication for the VetDict multi-species veterinary diagnostic platform.

## Overview

VetDict provides a comprehensive API authentication system designed for production use. The system supports:

- **Bearer Token Authentication**: Secure token-based access control
- **Rate Limiting**: Protection against brute-force attacks and abuse
- **Audit Logging**: Complete audit trail of authentication events
- **IP-based Client Identification**: Support for proxied environments
- **Extensible Design**: Ready for JWT and API key authentication

## Configuration

### Environment Variables

Authentication is configured using environment variables:

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `INTERNAL_API_TOKEN` | string | (empty) | Bearer token for API access |
| `INTERNAL_API_RATE_LIMIT_MAX_REQUESTS` | int | 30 | Max requests per rate limit window |
| `INTERNAL_API_RATE_LIMIT_WINDOW_SECONDS` | int | 60 | Rate limit window duration in seconds |
| `API_AUTH_AUDIT_LOG` | bool | true | Enable audit logging of auth events |
| `API_AUTH_JWT_ENABLED` | bool | false | Enable JWT authentication (future) |
| `API_AUTH_JWT_SECRET` | string | (empty) | JWT secret key (future) |
| `TRUSTED_PROXIES` | string | (empty) | Comma-separated list of trusted proxy IPs |

### Setting Up Authentication

**Development Environment:**

```bash
export INTERNAL_API_TOKEN="dev-token-abc123def456"
export INTERNAL_API_RATE_LIMIT_MAX_REQUESTS=100
export INTERNAL_API_RATE_LIMIT_WINDOW_SECONDS=60
```

**Production Environment:**

```bash
export INTERNAL_API_TOKEN="your-secure-token-generated-by-secure-random"
export INTERNAL_API_RATE_LIMIT_MAX_REQUESTS=30
export INTERNAL_API_RATE_LIMIT_WINDOW_SECONDS=60
export API_AUTH_AUDIT_LOG=true
export TRUSTED_PROXIES="10.0.0.0/8,172.16.0.0/12"
```

#### Generating a Secure Token

Use a cryptographically secure random generator:

```bash
# Linux/macOS
openssl rand -hex 32

# Python
python3 -c "import secrets; print(secrets.token_hex(32))"
```

## Protected Endpoints

The following endpoints require Bearer token authentication:

### RECO2/RECO3 AI Integrity Control

- `GET /api/status` - System status
- `GET /api/logs` - System logs
- `POST /api/evaluate` - Evaluate diagnostic payload
- `POST /api/feedback` - Record user feedback
- `POST /api/patrol` - Run integrity patrol
- `GET /api/r3/config` - Get RECO3 configuration
- `POST /api/r3/analyze_input` - Analyze input text
- `POST /api/r3/analyze_output` - Analyze output text
- `POST /api/r3/chat` - RECO3 chat interface

### Public Endpoints

These endpoints do **NOT** require authentication:

- `GET /api/health` - Health check
- `GET /api/species-stats` - Species and drug statistics
- `GET /api/species/<species>/symptoms` - Get symptoms for species
- `POST /api/analyze-symptoms` - Analyze symptoms
- `GET /api/breeds/<species>` - Get breeds for species
- All UI routes (`/`, `/static/*`, etc.)

## Authentication Methods

### Bearer Token Authentication

The primary authentication method uses Bearer tokens in the Authorization header:

```http
GET /api/status HTTP/1.1
Host: api.example.com
Authorization: Bearer YOUR_TOKEN_HERE
```

**Using curl:**

```bash
curl -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  https://api.example.com/api/status
```

**Using Python requests:**

```python
import requests

headers = {"Authorization": "Bearer YOUR_TOKEN_HERE"}
response = requests.get("https://api.example.com/api/status", headers=headers)
print(response.json())
```

**Using Node.js/JavaScript:**

```javascript
const response = await fetch('https://api.example.com/api/status', {
  headers: {
    'Authorization': 'Bearer YOUR_TOKEN_HERE'
  }
});
const data = await response.json();
console.log(data);
```

## Rate Limiting

### How It Works

Rate limiting is applied per client IP address:

1. Unauthorized requests are rate limited to prevent brute-force attacks
2. Each client has a separate rate limit bucket
3. The rate limit window is sliding (most recent requests count)
4. Once the limit is exceeded, a `429 Too Many Requests` response is returned

### Rate Limit Response

When rate limited, you'll receive:

```json
{
  "success": false,
  "error": "リクエスト制限に達しました。",
  "version": "5.0.0"
}
```

HTTP Status: `429 Too Many Requests`

### Handling Rate Limits

Implement exponential backoff when receiving rate limit responses:

```python
import time
import requests

MAX_RETRIES = 3
BASE_WAIT = 2

for attempt in range(MAX_RETRIES):
    response = requests.get(
        "https://api.example.com/api/status",
        headers={"Authorization": "Bearer YOUR_TOKEN"}
    )

    if response.status_code == 429:
        wait_time = BASE_WAIT ** attempt
        print(f"Rate limited. Waiting {wait_time}s...")
        time.sleep(wait_time)
        continue

    if response.status_code == 200:
        print(response.json())
        break
    else:
        print(f"Error: {response.status_code}")
        break
```

### Tuning Rate Limits

Adjust rate limits based on your use case:

```bash
# Aggressive rate limiting (security-focused)
export INTERNAL_API_RATE_LIMIT_MAX_REQUESTS=10
export INTERNAL_API_RATE_LIMIT_WINDOW_SECONDS=60

# Relaxed rate limiting (developer-friendly)
export INTERNAL_API_RATE_LIMIT_MAX_REQUESTS=100
export INTERNAL_API_RATE_LIMIT_WINDOW_SECONDS=120
```

## Audit Logging

Authentication events are logged for audit trails and security monitoring.

### Log Entries

Each authentication attempt is logged with:
- Timestamp (ISO 8601 format)
- Success/failure status
- Authentication method
- Client IP address
- Failure reason (if applicable)

### Example Log Output

```
2026-03-12T15:30:45.123456 INFO api.auth: Auth success: bearer_token from 192.168.1.100 - valid_token
2026-03-12T15:30:46.234567 WARNING api.auth: Auth failure: bearer_token from 192.168.1.101 - invalid_token
2026-03-12T15:30:47.345678 WARNING api.auth: Auth failure: bearer_token from 192.168.1.102 - rate_limited
```

### Disabling Audit Logging

In development environments, you can disable audit logging:

```bash
export API_AUTH_AUDIT_LOG=false
```

## Security Best Practices

### 1. Use HTTPS in Production

Always use HTTPS to prevent token interception:

```bash
# Not secure
http://api.example.com/api/status

# Secure
https://api.example.com/api/status
```

### 2. Rotate Tokens Regularly

Implement a token rotation schedule:

```bash
# Monthly token rotation example
# 1. Generate new token
NEW_TOKEN=$(python3 -c "import secrets; print(secrets.token_hex(32))")

# 2. Update environment variable
# 3. Deploy updated configuration
# 4. Monitor for failed authentications
# 5. Retire old token after grace period
```

### 3. Limit Token Scope

If using multiple tokens, assign different privileges:

```python
# Future implementation could support role-based tokens
# For now, use a single global token for all protected endpoints
```

### 4. Monitor for Suspicious Activity

Regularly review audit logs for:
- Excessive failed authentication attempts
- Requests from unexpected IP addresses
- Rate limit violations

```bash
# Example: grep for failed auth attempts
grep "Auth failure" /var/log/vetdict.log | \
  grep -c "rate_limited" > threshold && alert
```

### 5. Use Environment Variables Securely

- Never commit tokens to version control
- Use secrets management systems (AWS Secrets Manager, HashiCorp Vault, etc.)
- Restrict file permissions on `.env` files

### 6. Implement CORS Properly

The API includes CORS headers. Configure appropriately for your environment:

```python
# In app.py
CORS(app, origins=['https://app.example.com'])  # Production
CORS(app)  # Development (not recommended for production)
```

## Troubleshooting

### 401 Unauthorized

**Causes:**
- Missing or invalid Authorization header
- Incorrect Bearer token
- Token configured incorrectly on server

**Solutions:**

```bash
# Check that token is configured
echo $INTERNAL_API_TOKEN

# Verify token format
curl -v -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.example.com/api/status

# Check the exact error response
curl -s -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.example.com/api/status | jq .
```

### 429 Too Many Requests

**Causes:**
- Exceeded rate limit for your IP
- Multiple clients using same IP (behind proxy)

**Solutions:**

1. Wait for rate limit window to expire
2. Implement exponential backoff in client code
3. Configure proxy headers for accurate client IP detection

```bash
# If behind a proxy, server needs to know trusted proxy IPs
export TRUSTED_PROXIES="your-proxy-ip"

# Then clients can send X-Forwarded-For header
curl -H "X-Forwarded-For: 203.0.113.1" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.example.com/api/status
```

### 503 Service Unavailable

**Causes:**
- RECO2 module not available
- Missing dependencies

**Solutions:**

1. Check `/api/health` endpoint (public, no auth required)
2. Review server logs for dependency errors
3. Ensure all required modules are installed

```bash
GET https://api.example.com/api/health

{
  "status": "healthy",
  "version": "5.0.0",
  "features": {
    "reco2": true
  }
}
```

## Architecture

### Components

1. **AuthConfig**: Reads and manages authentication configuration
2. **RateLimiter**: Thread-safe rate limiting per client IP
3. **TokenValidator**: Validates Bearer tokens with constant-time comparison
4. **AuditLogger**: Logs authentication events for audit trails
5. **ClientIP**: Detects client IP with proxy support
6. **require_internal_api_access**: Decorator for protecting endpoints

### Data Flow

```
Request
  ↓
Parse Authorization Header
  ↓
Check Rate Limit
  ├→ Limited? → 429 Response
  ├→ Not Limited? → Continue
  ↓
Validate Bearer Token
  ├→ Invalid? → 401 Response
  ├→ Valid? → Continue
  ↓
Log Auth Event
  ↓
Call Protected Endpoint
```

## Future Enhancements

### Planned Features

1. **JWT Authentication**: Support for JSON Web Tokens
2. **API Key Management**: Persistent API keys with revocation
3. **OAuth 2.0**: Support for OAuth 2.0 authorization flows
4. **Scope-based Access Control**: Fine-grained endpoint permissions
5. **IP Whitelisting**: Restrict access to specific IP ranges
6. **Time-based Access**: Temporary tokens with expiration

### Contributing

To add new authentication methods:

1. Extend `TokenValidator` class
2. Add new validation method
3. Update `require_internal_api_access` decorator
4. Add comprehensive tests
5. Update this documentation

## API Reference

### require_internal_api_access Decorator

```python
from api.auth import require_internal_api_access

@app.route('/api/protected')
@require_internal_api_access
def protected_endpoint():
    return {'data': 'only visible to authenticated clients'}
```

### RateLimiter

```python
from api.auth import get_rate_limiter

limiter = get_rate_limiter()

# Check if rate limited
if limiter.is_limited("client_ip"):
    # Too many requests
    pass

# Get remaining requests
remaining = limiter.get_remaining_requests("client_ip")

# Reset for testing
limiter.reset()
```

### AuditLogger

```python
from api.auth import get_audit_logger

logger = get_audit_logger()
logger.log_auth_attempt(
    success=True,
    method='bearer_token',
    client_ip='192.168.1.1',
    reason='valid_token'
)
```

## Support

For issues or questions:

1. Check this documentation
2. Review the troubleshooting section
3. Check logs for error messages
4. Submit an issue: https://github.com/kamide007-ship-it/vetdict/issues

## Version History

- **5.0.0** (2026-03-12): Production authentication layer with rate limiting and audit logging
