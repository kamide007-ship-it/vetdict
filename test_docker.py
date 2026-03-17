#!/usr/bin/env python3
"""
Docker Configuration Tests
Validates Dockerfile and docker-compose.yml without requiring Docker daemon
"""

import json
import yaml
from pathlib import Path


def test_dockerfile_exists():
    """Check that Dockerfile exists"""
    assert Path('Dockerfile').exists(), "Missing Dockerfile"
    assert Path('Dockerfile.prod').exists(), "Missing Dockerfile.prod"
    print("✓ Dockerfiles exist")


def test_dockerfile_content():
    """Validate Dockerfile content"""
    with open('Dockerfile', 'r') as f:
        content = f.read()
    
    required = [
        'FROM python:3.11-slim',
        'WORKDIR /app',
        'COPY requirements.txt',
        'RUN pip install',
        'COPY . .',
        'USER appuser',
        'HEALTHCHECK',
        'EXPOSE 8000',
        'EXPOSE 3000'
    ]
    
    for item in required:
        assert item in content, f"Missing in Dockerfile: {item}"
        print(f"✓ {item}")


def test_docker_compose_structure():
    """Validate docker-compose.yml structure"""
    with open('docker-compose.yml', 'r') as f:
        config = yaml.safe_load(f)
    
    assert 'services' in config, "Missing services section"
    assert 'vetdict' in config['services'], "Missing vetdict service"
    assert 'networks' in config, "Missing networks section"
    assert 'volumes' in config, "Missing volumes section"
    
    print("✓ docker-compose.yml structure valid")


def test_docker_compose_services():
    """Validate docker-compose services"""
    with open('docker-compose.yml', 'r') as f:
        config = yaml.safe_load(f)
    
    services = config['services']
    
    # Check main service
    vetdict = services['vetdict']
    assert 'build' in vetdict, "Missing build configuration"
    assert 'ports' in vetdict, "Missing ports"
    assert 'environment' in vetdict, "Missing environment"
    assert 'healthcheck' in vetdict, "Missing healthcheck"
    
    # Check optional services
    assert 'db' in services, "Missing database service"
    assert 'cache' in services, "Missing cache service"
    assert 'nginx' in services, "Missing nginx service"
    
    print("✓ All services configured")


def test_docker_compose_healthcheck():
    """Validate healthcheck configuration"""
    with open('docker-compose.yml', 'r') as f:
        config = yaml.safe_load(f)
    
    healthcheck = config['services']['vetdict']['healthcheck']
    assert 'test' in healthcheck, "Missing healthcheck test"
    assert 'interval' in healthcheck, "Missing interval"
    assert 'timeout' in healthcheck, "Missing timeout"
    assert 'retries' in healthcheck, "Missing retries"
    
    print("✓ Healthcheck properly configured")


def test_env_example():
    """Validate .env.example file"""
    assert Path('.env.example').exists(), "Missing .env.example"
    
    with open('.env.example', 'r') as f:
        content = f.read()
    
    required = [
        'ENVIRONMENT',
        'API_PORT',
        'WEB_PORT',
        'DB_USER',
        'DB_PASSWORD'
    ]
    
    for item in required:
        assert item in content, f"Missing environment variable: {item}"
        print(f"✓ {item} in .env.example")


def test_nginx_config():
    """Validate nginx configuration"""
    assert Path('nginx.conf').exists(), "Missing nginx.conf"
    
    with open('nginx.conf', 'r') as f:
        content = f.read()
    
    required = [
        'upstream api_backend',
        'upstream web_backend',
        'location /api/',
        'location /static/',
        'ssl_certificate',
        'gzip on'
    ]
    
    for item in required:
        assert item in content, f"Missing nginx config: {item}"
        print(f"✓ {item}")


def test_dockerignore():
    """Validate .dockerignore"""
    assert Path('.dockerignore').exists(), "Missing .dockerignore"
    
    with open('.dockerignore', 'r') as f:
        content = f.read()
    
    required = [
        '__pycache__',
        '.git',
        '.pytest_cache',
        'venv',
        '.env'
    ]
    
    for item in required:
        assert item in content, f"Missing in .dockerignore: {item}"
        print(f"✓ {item}")


def test_docker_documentation():
    """Validate DOCKER.md exists"""
    assert Path('DOCKER.md').exists(), "Missing DOCKER.md"
    
    with open('DOCKER.md', 'r') as f:
        content = f.read()
    
    sections = [
        'Quick Start',
        'Docker Compose Setup',
        'Production Build',
        'Health Checks',
        'Troubleshooting'
    ]
    
    for section in sections:
        assert section in content, f"Missing section: {section}"
        print(f"✓ {section}")


if __name__ == '__main__':
    print("=" * 70)
    print("VetDict Docker Configuration Tests")
    print("=" * 70)
    
    tests = [
        test_dockerfile_exists,
        test_dockerfile_content,
        test_docker_compose_structure,
        test_docker_compose_services,
        test_docker_compose_healthcheck,
        test_env_example,
        test_nginx_config,
        test_dockerignore,
        test_docker_documentation,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            print(f"\n{test.__name__}:")
            test()
            passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
    
    print("\n" + "=" * 70)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 70)
    
    if failed == 0:
        print("\n✅ All Docker configuration tests passed!")
        print("\nTo deploy:")
        print("  Development: docker-compose up")
        print("  Production:  docker build -f Dockerfile.prod -t vetdict:prod .")
        print("  With nginx:  docker-compose --profile nginx up -d")
    
    exit(0 if failed == 0 else 1)
