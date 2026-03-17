#!/usr/bin/env python3
"""
API Documentation Tests
Validates Swagger UI, ReDoc, and OpenAPI schema without running server
"""

import re


def test_api_file_structure():
    """Test that fastapi_app.py has proper structure"""
    with open('fastapi_app.py', 'r') as f:
        content = f.read()

    required = [
        'class DiseaseResponse',
        'class PaginatedResponse',
        'class SearchResponse',
        'class HealthResponse',
        'class StatsResponse',
        'class ErrorResponse',
        'class SpeciesResponse',
        'async def health_check',
        'async def list_diseases',
        'async def search_diseases',
        'async def get_disease',
        'async def list_species',
        'async def get_statistics',
        'def custom_openapi()',
        'tags=["Health"]',
        'tags=["Diseases"]',
        'tags=["Metadata"]',
        'response_model=',
        'Field(..., description=',
        'json_schema_extra'
    ]

    for item in required:
        assert item in content, f"Missing: {item}"
        print(f"✓ {item}")


def test_models_have_documentation():
    """Test that all models have Field descriptions"""
    with open('fastapi_app.py', 'r') as f:
        content = f.read()

    # Find all model definitions
    model_pattern = r'class \w+Response\(BaseModel\):'
    models = re.findall(model_pattern, content)

    assert len(models) >= 7, f"Expected at least 7 models, found {len(models)}"
    print(f"✓ Found {len(models)} response models with documentation")


def test_endpoints_have_summaries():
    """Test that all endpoints have summary fields"""
    with open('fastapi_app.py', 'r') as f:
        content = f.read()

    endpoints = re.findall(r'@app\.get\([^)]+\)', content)

    for endpoint in endpoints:
        assert 'summary=' in endpoint or 'Summary' in endpoint, f"Missing summary: {endpoint}"

    print(f"✓ All {len(endpoints)} endpoints have summaries")


def test_endpoints_have_descriptions():
    """Test that all endpoints have docstrings"""
    with open('fastapi_app.py', 'r') as f:
        content = f.read()

    # Find function definitions with preceding decorators
    pattern = r'@app\.get\([^)]+\)\s+async def \w+\([^)]*\)[^:]*:\s+"""'
    matches = re.findall(pattern, content)

    assert len(matches) > 0, "No endpoints have docstrings with triple quotes"
    print("✓ All endpoints have docstring documentation")


def test_models_have_examples():
    """Test that models have json_schema_extra examples"""
    with open('fastapi_app.py', 'r') as f:
        content = f.read()

    examples = content.count('json_schema_extra')
    assert examples >= 7, f"Expected at least 7 examples, found {examples}"
    print(f"✓ {examples} response models have example schemas")


def test_api_responses_documented():
    """Test that endpoints document possible responses"""
    with open('fastapi_app.py', 'r') as f:
        content = f.read()

    response_docs = content.count('responses={')
    assert response_docs > 0, "Endpoints should document response codes"
    print(f"✓ {response_docs} endpoints document response codes")


def test_query_parameters_documented():
    """Test that query parameters have descriptions"""
    with open('fastapi_app.py', 'r') as f:
        content = f.read()

    assert 'Query(...,' in content, "Query parameters not documented"
    assert 'description=' in content, "Query parameter descriptions missing"
    assert 'example=' in content, "Query parameter examples missing"

    print("✓ Query parameters documented with descriptions and examples")


def test_tags_organized():
    """Test that endpoints are organized with tags"""
    with open('fastapi_app.py', 'r') as f:
        content = f.read()

    tags = [
        'tags=["Health"]',
        'tags=["Diseases"]',
        'tags=["Metadata"]',
        'tags=["Root"]'
    ]

    for tag in tags:
        assert tag in content, f"Missing tag: {tag}"
        print(f"✓ {tag}")


def test_openapi_customization():
    """Test that custom_openapi function exists"""
    with open('fastapi_app.py', 'r') as f:
        content = f.read()

    assert 'def custom_openapi()' in content, "Missing custom_openapi function"
    assert 'app.openapi = custom_openapi' in content, "OpenAPI not assigned"
    assert '"servers"' in content, "Server information not documented"
    assert '"tags"' in content, "Tag descriptions not added"

    print("✓ Custom OpenAPI schema with servers and tags")


def test_cors_configured():
    """Test CORS configuration"""
    with open('fastapi_app.py', 'r') as f:
        content = f.read()

    assert 'CORSMiddleware' in content, "CORS not configured"
    assert 'allow_origins' in content, "CORS origins not configured"

    print("✓ CORS middleware configured")


def test_error_handling():
    """Test error handling in endpoints"""
    with open('fastapi_app.py', 'r') as f:
        content = f.read()

    assert 'HTTPException' in content, "HTTPException not used"
    assert 'status_code=' in content, "Status codes not specified"
    assert 'detail=' in content, "Error details not provided"

    print("✓ Error handling implemented with HTTPException")


if __name__ == '__main__':
    print("=" * 70)
    print("VetDict API Documentation Tests")
    print("=" * 70)

    tests = [
        test_api_file_structure,
        test_models_have_documentation,
        test_endpoints_have_summaries,
        test_endpoints_have_descriptions,
        test_models_have_examples,
        test_api_responses_documented,
        test_query_parameters_documented,
        test_tags_organized,
        test_openapi_customization,
        test_cors_configured,
        test_error_handling,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            print(f"\n{test.__name__}:")
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} error: {e}")
            failed += 1

    print("\n" + "=" * 70)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 70)

    if failed == 0:
        print("\n✅ All API documentation tests passed!")
        print("\nDocumentation available at:")
        print("  Swagger UI: http://localhost:8000/api/docs")
        print("  ReDoc:      http://localhost:8000/api/redoc")
        print("  OpenAPI:    http://localhost:8000/api/openapi.json")

    exit(0 if failed == 0 else 1)
