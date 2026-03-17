#!/usr/bin/env python3
"""
Test FastAPI endpoints
"""

from fastapi.testclient import TestClient

from fastapi_app import app, load_diseases_data

client = TestClient(app)


def test_health_check():
    """Test health endpoint"""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["total_diseases"] > 0
    print(f"✓ Health check passed - {data['total_diseases']} diseases loaded")


def test_list_diseases():
    """Test paginated list endpoint"""
    response = client.get("/api/diseases?page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] > 0
    assert len(data["data"]) <= 10
    assert data["page"] == 1
    print(f"✓ List diseases passed - {data['total']} total diseases")


def test_get_disease():
    """Test get single disease endpoint"""
    # Get first disease to find a valid ID
    diseases = load_diseases_data()
    if diseases:
        first_id = diseases[0]["id"]
        response = client.get(f"/api/diseases/{first_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == first_id
        print(f"✓ Get disease passed - Retrieved {data['name']}")


def test_search_diseases():
    """Test search endpoint"""
    response = client.get("/api/diseases/search?q=feline&search_type=name&limit=5")
    assert response.status_code == 200
    data = response.json()
    print(f"✓ Search passed - Found {data['total_results']} results for 'feline'")


def test_list_species():
    """Test species listing endpoint"""
    response = client.get("/api/species")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] > 0
    print(f"✓ Species list passed - {data['total']} species found")
    print(f"  Species: {', '.join(data['species'][:5])}...")


def test_statistics():
    """Test statistics endpoint"""
    response = client.get("/api/stats")
    assert response.status_code == 200
    data = response.json()
    assert data["total_diseases"] > 0
    print(f"✓ Statistics passed - {data['total_diseases']} diseases, {data['total_species']} species")


def test_invalid_disease_id():
    """Test 404 error handling"""
    response = client.get("/api/diseases/invalid_id_xyz")
    assert response.status_code == 404
    print("✓ 404 handling passed - Invalid ID correctly rejected")


def test_pagination_validation():
    """Test pagination edge cases"""
    response = client.get("/api/diseases?page=999999&page_size=10")
    assert response.status_code == 404
    print("✓ Pagination validation passed - Out-of-range page rejected")


def test_search_by_species():
    """Test species filter in list endpoint"""
    response = client.get("/api/diseases?species=Cat&page=1&page_size=10")
    assert response.status_code == 200
    data = response.json()
    for disease in data["data"]:
        assert disease["species"] == "Cat"
    print("✓ Species filter passed - All results are Cat diseases")


if __name__ == "__main__":
    print("=" * 70)
    print("VetDict FastAPI Test Suite")
    print("=" * 70)

    tests = [
        test_health_check,
        test_list_diseases,
        test_get_disease,
        test_search_diseases,
        test_list_species,
        test_statistics,
        test_invalid_disease_id,
        test_pagination_validation,
        test_search_by_species,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1

    print("=" * 70)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 70)
