from api.vetdict_api import app


def test_health_check_diseases_include_quality_fields():
    client = app.test_client()
    resp = client.get('/api/health-check/diseases?species=cat')
    assert resp.status_code == 200
    payload = resp.get_json()
    assert 'diseases' in payload and payload['diseases']
    sample = payload['diseases'][0]
    assert 'completeness_score' in sample
    assert 'missing_fields' in sample
    assert isinstance(sample['missing_fields'], list)
    assert sample.get('content_origin') in {'sourced', 'mixed', 'generated'}
    assert sample.get('review_status') in {'reviewed', 'review_required'}
    assert isinstance(sample.get('evidence_sources'), list)
    for key in ['description', 'pathophysiology', 'causes', 'prevention', 'treatment', 'prognosis', 'symptoms_summary']:
        assert sample.get(key), f'{key} should be populated'


def test_disease_quality_report_endpoint():
    client = app.test_client()
    resp = client.get('/api/health-check/disease-quality-report?species=dog')
    assert resp.status_code == 200
    payload = resp.get_json()
    assert payload['species'] == 'dog'
    assert payload['total_diseases'] > 0
    assert 'average_completeness' in payload
    assert 'missing_field_counts' in payload


def test_api_cache_control_headers():
    client = app.test_client()
    resp = client.get('/api/health')
    assert resp.status_code == 200
    cc = resp.headers.get('Cache-Control', '')
    assert 'no-store' in cc
