# Multi-Disease Diagnostic System - Deployment Guide

## Phase 6: Production Deployment

**Document Version**: 1.0.0
**Last Updated**: 2024-03-13
**Status**: Ready for Production

---

## Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [System Requirements](#system-requirements)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Database Setup](#database-setup)
6. [Testing](#testing)
7. [Performance Optimization](#performance-optimization)
8. [Monitoring](#monitoring)
9. [Scaling](#scaling)
10. [Rollback Procedures](#rollback-procedures)

---

## Pre-Deployment Checklist

### Code Quality

- [x] All tests passing (159+ tests)
- [x] Code review completed
- [x] Documentation complete
- [x] API specification finalized
- [x] Frontend assets validated

### Security

- [x] Input validation implemented
- [x] No hardcoded secrets
- [x] SQL injection prevention
- [x] XSS protection
- [x] CORS properly configured

### Performance

- [x] Caching system operational
- [x] Database indexes optimized
- [x] API latency < 100ms
- [x] Memory usage acceptable
- [x] Cache hit rate > 60%

### Documentation

- [x] API documentation complete
- [x] User guide written
- [x] Deployment guide available
- [x] Medical validation documented
- [x] Troubleshooting guide included

---

## System Requirements

### Hardware

**Minimum**:
- CPU: 2 cores @ 2.0 GHz
- RAM: 4 GB
- Storage: 20 GB (SSD recommended)
- Network: 100 Mbps

**Recommended**:
- CPU: 4+ cores @ 2.5+ GHz
- RAM: 8-16 GB
- Storage: 50 GB SSD
- Network: 1 Gbps

**High Load** (1000+ requests/day):
- CPU: 8+ cores @ 3.0+ GHz
- RAM: 32+ GB
- Storage: 100+ GB SSD cluster
- Network: 10 Gbps or load balancer

### Software

```bash
# Python
python >= 3.11
pip >= 23.0

# Web Framework
flask >= 2.3.0
werkzeug >= 2.3.0

# Database
postgresql >= 12
sqlite >= 3.36 (development only)

# Cache (optional but recommended)
redis >= 6.0

# Monitoring
prometheus (optional)
grafana (optional)
```

### Browser Support

- Chrome >= 90
- Firefox >= 88
- Safari >= 14
- Edge >= 90

---

## Installation

### 1. Clone Repository

```bash
git clone https://github.com/kamide007-ship-it/vetdict.git
cd vetdict
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
pip install poetry  # Recommended

poetry install  # If using poetry
```

### 4. Verify Installation

```bash
python -c "import flask; from api.ai.multidisease_api_handler import MultiDiseaseAnalyzer; print('✓ Installation successful')"
```

---

## Configuration

### Environment Variables

Create `.env` file in project root:

```bash
# Flask
FLASK_ENV=production
FLASK_DEBUG=false
SECRET_KEY=your-secret-key-here-change-in-production

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/vetdict
SQLALCHEMY_ECHO=false
SQLALCHEMY_POOL_SIZE=20
SQLALCHEMY_POOL_RECYCLE=3600

# Multi-Disease System
MULTIDISEASE_CACHE_TTL=3600
MULTIDISEASE_CACHE_SIZE=2000
MULTIDISEASE_CACHING_ENABLED=true
MULTIDISEASE_VALIDATION_ENABLED=true

# Cache Backend (optional)
CACHE_TYPE=redis  # redis or simple
REDIS_URL=redis://localhost:6379/0

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/vetdict/multidisease.log

# CORS
CORS_ORIGINS=["http://localhost:3000", "https://example.com"]

# API Rate Limiting
RATELIMIT_ENABLED=true
RATELIMIT_REQUESTS=1000
RATELIMIT_PERIOD=3600

# Monitoring
SENTRY_DSN=https://your-sentry-dsn-here
PROMETHEUS_ENABLED=true
```

### Configuration File

Alternatively, use `config.py`:

```python
# config.py
import os

class ProductionConfig:
    """Production configuration."""

    DEBUG = False
    TESTING = False

    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_POOL_SIZE = 20
    SQLALCHEMY_POOL_RECYCLE = 3600

    # Cache
    CACHE_TYPE = os.getenv('CACHE_TYPE', 'simple')
    CACHE_REDIS_URL = os.getenv('REDIS_URL')

    # Multi-Disease
    MULTIDISEASE_CACHE_TTL = int(os.getenv('MULTIDISEASE_CACHE_TTL', 3600))
    MULTIDISEASE_CACHE_SIZE = int(os.getenv('MULTIDISEASE_CACHE_SIZE', 2000))

class DevelopmentConfig(ProductionConfig):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_ECHO = True

class TestingConfig(ProductionConfig):
    """Testing configuration."""
    TESTING = True
    DATABASE_URL = 'sqlite:///:memory:'
```

---

## Database Setup

### 1. Create Database

```bash
createdb vetdict  # PostgreSQL

# Or use SQLAlchemy
python -c "from app import db; db.create_all()"
```

### 2. Load Initial Data

```bash
python scripts/load_disease_database.py

# Verify load
python -c "from app import db; from models import Disease; print(f'Loaded {Disease.query.count()} diseases')"
```

### 3. Create Indexes

```bash
# PostgreSQL
psql vetdict << EOF
CREATE INDEX idx_disease_name ON diseases(name);
CREATE INDEX idx_symptom_disease ON disease_symptoms(disease_id, symptom_id);
CREATE INDEX idx_symptom_text ON symptoms(symptom_text);
EOF
```

### 4. Backup Strategy

```bash
# Daily backup
0 2 * * * pg_dump vetdict | gzip > /backups/vetdict-$(date +\%Y\%m\%d).sql.gz

# Keep 30 days
find /backups -name "*.sql.gz" -mtime +30 -delete
```

---

## Testing

### Pre-Deployment Tests

```bash
# Run all tests
pytest tests/ -v --tb=short

# Multi-disease specific tests
pytest tests/test_multidisease*.py -v

# Coverage report
pytest tests/ --cov=api.ai --cov-report=html

# Frontend tests
pytest tests/test_multidisease_frontend.py -v
```

### Integration Tests

```bash
# Start test server
FLASK_ENV=testing python -m flask run &

# Run integration tests
pytest tests/integration/ -v

# Stop test server
kill %1
```

### Performance Tests

```bash
# Load testing with locust
locust -f locustfile.py --host=http://localhost:5000

# API latency benchmark
python scripts/benchmark_api.py
```

---

## Performance Optimization

### Database Optimization

```sql
-- Check query performance
EXPLAIN ANALYZE SELECT * FROM diseases WHERE name ILIKE '%Hip%';

-- Optimize slow queries
CREATE INDEX idx_disease_symptoms ON diseases USING GIN(symptoms);
```

### Cache Optimization

```python
# Monitor cache performance
cache_stats = MultiDiseaseAnalysisCache().get_cache_stats()
print(f"Hit rate: {cache_stats['symptom_context']['hit_rate_percent']}%")

# Tune cache sizes based on usage
MULTIDISEASE_CACHE_SIZE = 5000  # Increase if hit rate < 50%
```

### Web Server Optimization

```python
# Use production WSGI server (not Flask dev server)
# gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# uWSGI
pip install uwsgi
uwsgi --http :5000 --wsgi-file app.py --callable app --processes 4 --threads 2
```

### Frontend Optimization

```bash
# Minify CSS and JavaScript
python -m csscompressor static/css/multidisease-ui.css > static/css/multidisease-ui.min.css
python -m jsmin static/js/multidisease-ui.js > static/js/multidisease-ui.min.js

# Use minified versions in production
# Update index.html to use .min. files
```

---

## Monitoring

### Health Check Endpoint

```python
@app.route('/health')
def health_check():
    """System health check."""
    return {
        'status': 'healthy',
        'cache_hit_rate': cache.get_stats()['symptom_context']['hit_rate_percent'],
        'database': check_database_connection(),
        'timestamp': datetime.utcnow().isoformat()
    }
```

### Logging Configuration

```python
import logging
from logging.handlers import RotatingFileHandler

# Setup file handler
file_handler = RotatingFileHandler(
    '/var/log/vetdict/multidisease.log',
    maxBytes=10485760,  # 10MB
    backupCount=10
)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
))
app.logger.addHandler(file_handler)
```

### Metrics to Monitor

```
✓ API response time (target: < 100ms)
✓ Cache hit rate (target: > 60%)
✓ Database query time (target: < 50ms)
✓ Memory usage (monitor for leaks)
✓ Error rate (target: < 0.1%)
✓ Availability (target: > 99.9%)
```

### Alerting Rules

```
- Response time > 500ms → WARNING
- Error rate > 1% → CRITICAL
- Memory usage > 80% → WARNING
- Cache hit rate < 30% → INFO
- Database connection errors → CRITICAL
```

---

## Scaling

### Horizontal Scaling

```bash
# Load balancer (nginx)
# conf/nginx.conf

upstream app_backend {
    server app1.local:5000;
    server app2.local:5000;
    server app3.local:5000;
}

server {
    listen 80;
    location / {
        proxy_pass http://app_backend;
        proxy_set_header Host $host;
    }
}
```

### Vertical Scaling

1. Increase server resources (CPU, RAM)
2. Optimize database queries
3. Increase cache size
4. Use connection pooling

### Database Scaling

```sql
-- Read replicas for scale-out
-- Configure replication on PostgreSQL
```

---

## Rollback Procedures

### Code Rollback

```bash
# If deployment fails
git revert <commit-hash>
git push origin main

# Or redeploy previous version
git checkout <previous-tag>
git push origin main --force  # Only if necessary
```

### Database Rollback

```bash
# Restore from backup
pg_restore -d vetdict /backups/vetdict-<date>.sql.gz

# Or migrate to previous schema
flask db downgrade
```

### Cache Invalidation

```python
# After code update
from api.ai.multidisease_cache_manager import get_global_cache
cache = get_global_cache()
cache.clear_all()
```

---

## Post-Deployment Verification

### Smoke Tests

```bash
# Verify API is responding
curl http://localhost:5000/health

# Test multi-disease endpoint
curl -X POST http://localhost:5000/api/multidisease/analyze \
  -H "Content-Type: application/json" \
  -d '{"symptom_ids": ["test1", "test2"]}'

# Check frontend loads
curl http://localhost:5000/ | grep "multidisease-ui"
```

### User Acceptance Testing

1. Test multi-disease mode activation
2. Verify disease combinations display correctly
3. Validate ambiguity analysis
4. Test clarifying questions
5. Confirm confidence scores
6. Check multilingual support
7. Test mobile responsiveness

---

## Maintenance Schedule

### Daily
- Monitor error logs
- Check cache hit rate
- Verify API latency

### Weekly
- Review performance metrics
- Check database size growth
- Update security patches

### Monthly
- Backup verification
- Performance analysis
- Capacity planning

### Quarterly
- Security audit
- Load testing
- Medical validation review

---

## Support Contacts

- **Technical Issues**: dev@example.com
- **Medical Questions**: veterinary@example.com
- **Deployment Help**: ops@example.com

---

**Last Updated**: 2024-03-13
**Deployment Status**: Ready for Production
