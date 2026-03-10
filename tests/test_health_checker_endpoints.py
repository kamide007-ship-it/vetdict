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
    assert sample.get('evidence_sources') and {'id','name','url'} <= set(sample['evidence_sources'][0].keys())
    assert isinstance(sample.get('citation_map'), dict)
    assert sample['citation_map'].get('treatment')
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
    assert 'reference_coverage' in payload
    assert 'citation_coverage' in payload
    assert payload['reference_coverage'] >= 0
    assert payload['citation_coverage'] >= 0


def test_api_cache_control_headers():
    client = app.test_client()
    resp = client.get('/api/health')
    assert resp.status_code == 200
    cc = resp.headers.get('Cache-Control', '')
    assert 'no-store' in cc


def test_enrich_preserves_existing_citation_map():
    from api.content_quality import enrich_disease_content

    disease = {
        'name': 'Chronic Kidney Disease',
        'name_ja': '慢性腎臓病',
        'description': 'CKD',
        'description_ja': 'CKD',
        'pathophysiology': 'x',
        'pathophysiology_ja': 'x',
        'causes': 'x',
        'causes_ja': 'x',
        'prevention': 'x',
        'prevention_ja': 'x',
        'treatment': 'x',
        'treatment_ja': 'x',
        'prognosis': 'x',
        'prognosis_ja': 'x',
        'citation_map': {'treatment': ['custom-ref']},
    }
    out = enrich_disease_content(disease, 'cat')
    assert out['citation_map']['treatment'] == ['custom-ref']
    assert any('query=Chronic+Kidney+Disease' in r.get('url', '') for r in out.get('evidence_sources', []))
