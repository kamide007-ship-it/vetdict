# Multi-Disease Diagnostic System - Security Guide

## Phase 6: Production Security

**Version**: 1.0.0
**Date**: 2024-03-13
**Compliance**: OWASP Top 10 2021

---

## Security Overview

### Security Principles

1. **Input Validation** - All inputs validated server-side
2. **Output Encoding** - All outputs properly encoded
3. **Authentication** - API authentication if needed
4. **Authorization** - Role-based access control (future)
5. **Data Protection** - Sensitive data encrypted
6. **Error Handling** - Secure error messages
7. **Dependency Management** - Regular updates
8. **Logging & Monitoring** - Security event logging

---

## Threat Model

### Threats Considered

| Threat | Likelihood | Impact | Mitigation |
|--------|------------|--------|-----------|
| SQL Injection | Medium | High | Parameterized queries |
| XSS Attack | High | Medium | Input validation + encoding |
| DoS Attack | Medium | Medium | Rate limiting |
| Data Breach | Low | High | Encryption |
| API Abuse | Medium | Low | Rate limiting + auth |
| Dependency Vuln | High | Medium | Regular updates |

---

## OWASP Top 10 Mitigations

### 1. Injection Prevention

**SQL Injection**:
```python
# ✓ SAFE: Parameterized query
disease = Disease.query.filter_by(name=user_input).first()

# ❌ UNSAFE: String concatenation
disease = db.session.execute(f"SELECT * FROM diseases WHERE name='{user_input}'")
```

**Command Injection**:
- Never use `shell=True` in subprocess
- Use parameterized approaches
- Validate file paths

### 2. Authentication & Session Management

**Current**: None required (read-only API)
**Future Implementation**:
```python
from flask_jwt_extended import JWTManager, create_access_token

jwt = JWTManager(app)

@app.route('/api/protected')
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return {'data': 'protected'}
```

### 3. Sensitive Data Exposure

**Patient Data**:
- No patient identifiers stored in logs
- Disease database only
- De-identified case data

**API Keys/Secrets**:
- Use environment variables, not hardcoded
- Never commit secrets to repository
- Rotate regularly

**Transmission Security**:
- HTTPS required in production
- TLS 1.2+ only
- No unencrypted HTTP

### 4. XML External Entities (XXE)

**Not applicable** - System uses JSON, not XML

### 5. Broken Access Control

**Implementation**:
```python
# Future: Check user permissions
@app.route('/api/admin/settings')
@admin_required
def admin_settings():
    # Only admins can access
    pass
```

### 6. Security Misconfiguration

**Best Practices**:
- Debug mode OFF in production
- CORS properly configured
- Security headers set

```python
# Production configuration
DEBUG = False
TESTING = False

# Security headers
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000'
    return response
```

### 7. Cross-Site Scripting (XSS)

**Prevention**:
```python
# ✓ SAFE: Escaped output
{{ symptom_name | escape }}

# ✓ SAFE: Using safe filters in templates
{{ user_input | safe_html }}

# ❌ UNSAFE: Direct output
{{ symptom_name | safe }}
```

**Frontend**:
```javascript
// ✓ SAFE: Using textContent
element.textContent = userInput;

// ❌ UNSAFE: Using innerHTML
element.innerHTML = userInput;
```

### 8. Insecure Deserialization

**Prevention**:
- Never pickle untrusted data
- Use JSON for API communication
- Validate JSON schema

```python
# ✓ SAFE: JSON validation
from jsonschema import validate
validate(instance=data, schema=disease_schema)

# ❌ UNSAFE: Pickle untrusted data
disease = pickle.loads(user_data)
```

### 9. Using Components with Known Vulnerabilities

**Dependency Management**:
```bash
# Check for vulnerabilities
pip install safety
safety check

# Keep dependencies updated
pip list --outdated
pip install --upgrade package_name

# Automated scanning in CI/CD
# Using: Snyk, Dependabot, WhiteSource
```

### 10. Insufficient Logging & Monitoring

**Implementation**:
```python
import logging

logger = logging.getLogger('multidisease')

# Log security events
logger.warning(f"Invalid API request from {ip_address}")
logger.error(f"Database error in analysis: {error}")

# Monitor
- Failed API requests
- Database errors
- Cache failures
- Unusual patterns
```

---

## Input Validation

### Symptom IDs

```python
# Validate symptom IDs
VALID_SYMPTOMS = load_valid_symptoms()

symptom_ids = request.json.get('symptom_ids', [])
for symptom_id in symptom_ids:
    if not isinstance(symptom_id, str):
        return {'error': 'symptom_ids must be strings'}, 400
    if len(symptom_id) > 100:
        return {'error': 'symptom_id too long'}, 400
    if symptom_id not in VALID_SYMPTOMS:
        return {'error': f'Unknown symptom: {symptom_id}'}, 400
```

### Disease Names

```python
# Validate disease names
disease_names = request.json.get('suspected_diseases', [])
for disease in disease_names:
    if not isinstance(disease.get('name'), str):
        return {'error': 'Invalid disease format'}, 400
    if len(disease['name']) > 200:
        return {'error': 'Disease name too long'}, 400
```

### Numeric Values

```python
# Validate confidence scores
confidence = disease.get('confidence')
if not isinstance(confidence, (int, float)):
    return {'error': 'Invalid confidence type'}, 400
if not (0 <= confidence <= 1):
    return {'error': 'Confidence must be 0-1'}, 400
```

---

## Rate Limiting

### Implementation

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/multidisease/analyze')
@limiter.limit("30 per minute")
def analyze_multidisease():
    # Rate limited to 30 requests per minute
    pass
```

### Rate Limit Headers

```
X-RateLimit-Limit: 30
X-RateLimit-Remaining: 28
X-RateLimit-Reset: 1710345000
```

---

## Secure Coding Practices

### SQL Queries

```python
# ✓ GOOD: Use ORM/parameterized queries
user = User.query.filter_by(email=email).first()

# ✓ GOOD: Use parameters with raw SQL
disease = db.session.execute(
    "SELECT * FROM diseases WHERE name = :name",
    {"name": disease_name}
)

# ❌ BAD: String concatenation
disease = db.session.execute(f"SELECT * FROM diseases WHERE name = '{disease_name}'")
```

### File Handling

```python
# ✓ GOOD: Use secure paths
import os
safe_path = os.path.join('/uploads/', secure_filename(filename))

# ❌ BAD: Direct user path
unsafe_path = f"/uploads/{user_filename}"
```

### Error Messages

```python
# ✓ GOOD: Generic error messages
return {'error': 'Database error occurred'}, 500

# ❌ BAD: Expose internal details
return {'error': f'SQL error: {e.sql_statement}'}, 500
```

### Logging

```python
# ✓ GOOD: Log security events
logger.warning(f"Invalid token from {request.remote_addr}")

# ❌ BAD: Log sensitive data
logger.info(f"User password: {password}")
```

---

## API Security

### Endpoint Protection

```python
@app.route('/api/multidisease/analyze', methods=['POST'])
def analyze():
    # 1. Validate request format
    if not request.is_json:
        return {'error': 'Content-Type must be application/json'}, 400

    # 2. Validate input
    data = request.json
    is_valid, error = MultiDiseaseAnalyzer.validate_request(data)
    if not is_valid:
        return {'error': error}, 422

    # 3. Process safely
    try:
        result = MultiDiseaseAnalyzer.analyze_for_multidisease(**data)
        return result, 200
    except ValueError as e:
        return {'error': 'Invalid input'}, 400
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return {'error': 'Server error'}, 500
```

### CORS Configuration

```python
from flask_cors import CORS

# Allow specific origins only
CORS(app, resources={
    r"/api/*": {
        "origins": ["https://example.com"],
        "methods": ["GET", "POST"],
        "allow_headers": ["Content-Type"]
    }
})
```

### Content Security Policy

```python
@app.after_request
def set_csp(response):
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:"
    )
    return response
```

---

## Data Protection

### Patient Data Handling

✓ **DO**:
- Anonymize case data
- Use de-identified disease databases
- Encrypt sensitive fields
- Secure database access

❌ **DON'T**:
- Store patient names/IDs
- Log patient information
- Share data without consent
- Keep unencrypted sensitive data

### Database Security

```sql
-- Secure database user
CREATE USER vetdict_app WITH PASSWORD 'strong_password';
GRANT SELECT, INSERT ON diseases, symptoms TO vetdict_app;
REVOKE ALL ON users FROM vetdict_app;

-- Encrypt sensitive data
ALTER TABLE patient_cases
ADD COLUMN medical_history_encrypted TEXT;
```

### Backup Security

```bash
# Encrypt backups
pg_dump vetdict | gzip | gpg --encrypt > backup.sql.gz.gpg

# Store securely
# - Off-site location
# - Restricted access
# - Versioned
```

---

## Dependency Security

### Regular Updates

```bash
# Check outdated packages
pip list --outdated

# Update specific package
pip install --upgrade flask

# Update all
pip install --upgrade -r requirements.txt
```

### Vulnerability Scanning

```bash
# Install safety
pip install safety

# Check for known vulnerabilities
safety check

# Generate report
safety check --json > security_report.json
```

### Continuous Monitoring

- Enable Dependabot on GitHub
- Set up automated PRs for updates
- Review and test updates before merging
- Use pinned versions for stability

---

## Security Testing

### Static Analysis

```bash
# Install security linter
pip install bandit

# Check code for security issues
bandit -r api/

# Generate report
bandit -r api/ -f json -o security_report.json
```

### Dynamic Testing

```bash
# OWASP ZAP scanning
zaproxy --cmd -quickurl http://localhost:5000 -quickout report.html
```

### Penetration Testing

- Annual professional penetration testing
- Focus on API endpoints
- Test authentication/authorization
- Verify input validation

---

## Incident Response

### Security Incident Procedure

1. **Detect** - Monitor logs for suspicious activity
2. **Contain** - Isolate affected systems
3. **Investigate** - Determine scope and impact
4. **Eradicate** - Remove root cause
5. **Recover** - Restore normal operations
6. **Document** - Record what happened

### Contact Information

- **Security Team**: security@example.com
- **Incident Response**: incidents@example.com
- **Emergency**: +1-555-SECURITY

---

## Compliance

### Standards & Frameworks

✓ OWASP Top 10 2021
✓ NIST Cybersecurity Framework
✓ CWE Top 25
✓ SANS Top 25

### Audit Trail

```python
# Log all sensitive operations
def log_audit(action, user, details):
    logger.info(f"AUDIT: {action} by {user} - {details}")
```

---

## Security Checklist

- [ ] All inputs validated
- [ ] No hardcoded secrets
- [ ] HTTPS enforced
- [ ] Database encrypted
- [ ] Backups secured
- [ ] Dependencies updated
- [ ] Security headers set
- [ ] CORS configured
- [ ] Rate limiting enabled
- [ ] Errors logged securely
- [ ] Code reviewed
- [ ] Tests passing
- [ ] Dependencies scanned
- [ ] Documentation complete

---

## Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [NIST Cybersecurity](https://www.nist.gov/cybersecurity)
- [Flask Security](https://flask.palletsprojects.com/en/2.0.x/security/)

---

**Last Updated**: 2024-03-13
**Status**: Security Review Completed
**Next Review**: Quarterly
