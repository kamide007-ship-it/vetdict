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
    assert len(sample['evidence_sources']) > 0
    assert {'id', 'name', 'url'} <= set(sample['evidence_sources'][0].keys())
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


def test_api_cache_control_headers():
    client = app.test_client()
    resp = client.get('/api/health')
    assert resp.status_code == 200
    cc = resp.headers.get('Cache-Control', '')
    assert 'no-store' in cc


def test_species_symptoms_endpoint_merges_dog_localized_names():
    client = app.test_client()
    resp = client.get('/api/species/dog/symptoms')
    assert resp.status_code == 200
    payload = resp.get_json()
    symptoms = {item['id']: item for item in payload['symptoms']}
    assert symptoms['appetite_loss']['name_ja'] == '食欲不振'
    assert symptoms['appetite_loss']['name_en'] == 'Appetite Loss'


def test_species_symptoms_endpoint_merges_species_localized_names():
    client = app.test_client()
    resp = client.get('/api/species/cat/symptoms')
    assert resp.status_code == 200
    payload = resp.get_json()
    symptoms = {item['id']: item for item in payload['symptoms']}
    assert symptoms['cyanosis']['name_ja'] == 'チアノーゼ'
    assert symptoms['cyanosis']['name_en'] == 'Cyanosis'


def test_species_symptoms_endpoint_merges_horse_localized_names():
    client = app.test_client()
    resp = client.get('/api/species/horse/symptoms')
    assert resp.status_code == 200
    payload = resp.get_json()
    symptoms = {item['id']: item for item in payload['symptoms']}
    assert symptoms['limb_bucked_shin']['name_ja'] == 'すねの前面が腫れている（バックドシン）'
    assert symptoms['limb_bucked_shin']['name_en'] == 'Bucked Shin'
    assert symptoms['limb_bucked_shin']['category'] == 'limb'


def test_index_lab_bun_label_targets_bun_input():
    client = app.test_client()
    resp = client.get('/')
    assert resp.status_code == 200
    html = resp.get_data(as_text=True)
    assert '<label for="lab-bun">BUN <span class="lab-unit">mg/dL</span></label>' in html
    assert 'id="lab-bun"' in html
