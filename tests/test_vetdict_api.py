#!/usr/bin/env python3
"""
Tests for api/vetdict_api.py

Covers:
1. Flask app and test client fixture setup
2. Static file routes (/, /favicon.ico, /static/<path>, /<path>)
3. GET /api/health — structure and feature flags
4. GET /api/species-stats — structure, totals
5. GET /api/species/<species>/symptoms — known/unknown species, merged labels
6. POST /api/analyze-symptoms — validation, dog path, species path
7. GET /api/breeds/<species>
8. Protected RECO2 routes (/api/status, /api/logs, /api/evaluate,
   /api/feedback, /api/patrol, /api/r3/*)
9. ensure_json_response decorator — version injection, error wrapping
10. Security headers added by after_request hook
11. Error handlers (404, 429, 500)
"""

import json
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest

# ---------------------------------------------------------------------------
# Make sure the project root is on sys.path (mirrors conftest.py)
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import api.vetdict_api as vetdict_api
from api.auth import reset_rate_limiting
from api.vetdict_api import VERSION
from api.vetdict_api import app as flask_app

# =============================================================================
# Fixtures
# =============================================================================


@pytest.fixture(autouse=True)
def _reset_rate_limits():
    """Reset rate-limit buckets before every test so tests are isolated."""
    reset_rate_limiting()
    yield
    reset_rate_limiting()


@pytest.fixture()
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as c:
        yield c


def _auth_header(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


# =============================================================================
# 1. Health endpoint
# =============================================================================


class TestHealthEndpoint:
    def test_returns_200(self, client):
        resp = client.get('/api/health')
        assert resp.status_code == 200

    def test_response_has_status_healthy(self, client):
        payload = client.get('/api/health').get_json()
        assert payload['status'] == 'healthy'

    def test_response_has_version(self, client):
        payload = client.get('/api/health').get_json()
        assert payload['version'] == VERSION

    def test_response_has_build(self, client):
        payload = client.get('/api/health').get_json()
        assert 'build' in payload

    def test_features_dict_present(self, client):
        payload = client.get('/api/health').get_json()
        assert 'features' in payload
        features = payload['features']
        for key in ('symptom_checker', 'species_analyzer', 'health_checker',
                    'diagnostic_chat', 'drug_dictionary', 'reco2'):
            assert key in features, f"Missing feature key: {key}"
            assert isinstance(features[key], bool)

    def test_content_type_is_json(self, client):
        resp = client.get('/api/health')
        assert 'application/json' in resp.content_type


# =============================================================================
# 2. Security headers (after_request hook)
# =============================================================================


class TestSecurityHeaders:
    def test_x_content_type_options(self, client):
        resp = client.get('/api/health')
        assert resp.headers.get('X-Content-Type-Options') == 'nosniff'

    def test_x_frame_options(self, client):
        resp = client.get('/api/health')
        # DENY aligns with CSP frame-ancestors 'none'; we never embed our own pages.
        assert resp.headers.get('X-Frame-Options') == 'DENY'

    def test_permissions_policy(self, client):
        resp = client.get('/api/health')
        pp = resp.headers.get('Permissions-Policy', '')
        assert 'geolocation=()' in pp
        assert 'camera=()' in pp

    def test_referrer_policy(self, client):
        resp = client.get('/api/health')
        assert resp.headers.get('Referrer-Policy') == 'strict-origin-when-cross-origin'

    def test_content_security_policy_present(self, client):
        resp = client.get('/api/health')
        csp = resp.headers.get('Content-Security-Policy', '')
        assert "default-src 'self'" in csp

    def test_csp_allows_inline_and_ga_hosts(self, client):
        resp = client.get('/api/health')
        csp = resp.headers.get('Content-Security-Policy', '')
        script_src = csp.split("script-src")[1].split(";")[0]
        # 'unsafe-inline' must be present for GA4 inline event handlers
        assert "'unsafe-inline'" in script_src
        # GA/GTM host allowlists must be present
        assert "https://www.googletagmanager.com" in script_src
        assert "https://www.google-analytics.com" in script_src
        # nonce and strict-dynamic must NOT be present (they cause
        # browsers to ignore 'unsafe-inline' and host allowlists)
        assert "'nonce-" not in csp
        assert "'strict-dynamic'" not in script_src

    def test_server_header_removed(self, client):
        resp = client.get('/api/health')
        assert 'Server' not in resp.headers

    def test_api_routes_have_no_store_cache_control(self, client):
        resp = client.get('/api/health')
        cc = resp.headers.get('Cache-Control', '')
        assert 'no-store' in cc

    def test_root_route_has_no_store_cache_control(self, client):
        resp = client.get('/')
        # Either it serves a file (200) or returns a 404; either way cache header
        # should be no-store because path == '/'
        cc = resp.headers.get('Cache-Control', '')
        assert 'no-store' in cc

    def test_hsts_not_set_outside_production(self, monkeypatch, client):
        monkeypatch.delenv('RENDER', raising=False)
        monkeypatch.delenv('PRODUCTION', raising=False)
        resp = client.get('/api/health')
        assert 'Strict-Transport-Security' not in resp.headers

    def test_hsts_set_in_production(self, monkeypatch, client):
        monkeypatch.setenv('RENDER', '1')
        resp = client.get('/api/health')
        assert 'Strict-Transport-Security' in resp.headers
        assert 'max-age=31536000' in resp.headers['Strict-Transport-Security']


# =============================================================================
# 3. Static / HTML file routes
# =============================================================================


class TestStaticRoutes:
    def test_index_returns_404_when_no_template(self, client):
        # In test environment index.html typically doesn't exist;
        # the route should return 404 gracefully.
        resp = client.get('/')
        assert resp.status_code in (200, 404)

    def test_favicon_returns_204_or_file(self, client):
        resp = client.get('/favicon.ico')
        assert resp.status_code in (200, 204, 404)

    def test_static_asset_missing_returns_404(self, client):
        resp = client.get('/static/nonexistent_asset_xyz.js')
        assert resp.status_code == 404
        payload = resp.get_json()
        assert 'error' in payload

    def test_arbitrary_path_missing_returns_404(self, client):
        resp = client.get('/nonexistent_page_xyz')
        assert resp.status_code == 404

    def test_static_404_error_body_has_filename(self, client):
        resp = client.get('/static/no_such_file.css')
        assert resp.status_code == 404
        payload = resp.get_json()
        assert 'no_such_file.css' in payload.get('error', '')


class TestDynamicSitemap:
    def test_sitemap_returns_xml(self, client):
        resp = client.get('/sitemap.xml')
        assert resp.status_code == 200
        assert 'xml' in resp.content_type

    def test_sitemap_contains_base_urls(self, client):
        data = client.get('/sitemap.xml').data.decode()
        assert 'https://vetdict.info/' in data
        assert '#checker' in data
        assert '#database' in data
        assert '#chat' in data
        assert '#drugs' in data

    def test_sitemap_contains_species(self, client):
        data = client.get('/sitemap.xml').data.decode()
        assert 'species=dog' in data
        assert 'species=cat' in data
        assert 'species=fish' in data

    def test_sitemap_contains_legal_pages(self, client):
        data = client.get('/sitemap.xml').data.decode()
        assert '/terms' in data
        assert '/privacy' in data
        assert '/tokushoho' in data

    def test_sitemap_has_all_species(self, client):
        from api.disease_store import SPECIES_META
        data = client.get('/sitemap.xml').data.decode()
        for sp in SPECIES_META:
            assert f'species={sp}' in data


# =============================================================================
# 4. Error handlers
# =============================================================================


class TestErrorHandlers:
    def test_404_handler_returns_json(self, client):
        # /api/ prefix routes that don't exist fall through to static_files;
        # use a path that is not caught by catch-all static routes
        resp = client.get('/api/health/does_not_exist/xyzzy')
        assert resp.status_code == 404
        payload = resp.get_json()
        assert 'error' in payload

    def test_404_handler_on_registered_api_prefix(self, client):
        # The Flask 404 error handler fires for paths under /api/ only when
        # no other route matches. The static catch-all handles non-/api/ paths.
        resp = client.get('/api/health/does_not_exist/xyzzy')
        assert resp.status_code == 404
        assert resp.get_json() is not None

    def test_500_handler_returns_json(self, client, monkeypatch):
        # Trigger a 500 via ensure_json_response catching an unexpected error
        # from an existing view rather than registering a new route.
        monkeypatch.setattr(vetdict_api, 'RECO2_AVAILABLE', True)
        monkeypatch.setattr(vetdict_api, 'reco2_get_status',
                            MagicMock(side_effect=RuntimeError("forced crash")))
        monkeypatch.delenv('INTERNAL_API_TOKEN', raising=False)

        resp = client.get('/api/status')
        assert resp.status_code == 500
        payload = resp.get_json()
        assert 'error' in payload


# =============================================================================
# 5. ensure_json_response decorator
# =============================================================================


class TestEnsureJsonResponseDecorator:
    """Test the ensure_json_response decorator in isolation via the health endpoint
    as a representative decorated view."""

    def test_version_injected_into_dict_response(self, client):
        payload = client.get('/api/health').get_json()
        assert payload['version'] == VERSION

    def test_error_in_view_returns_500_json(self, monkeypatch, client):
        """When the underlying view raises an unexpected exception, the decorator
        should catch it and return a structured 500 response."""
        def _raise(_):
            raise RuntimeError("test explosion")

        monkeypatch.setattr(vetdict_api, 'SYMPTOM_CHECKER_AVAILABLE', True)
        monkeypatch.setattr(vetdict_api, 'analyze_symptoms', _raise)

        resp = client.post(
            '/api/analyze-symptoms',
            json={'symptoms': ['vomiting'], 'species': 'dog'},
        )
        # The error may be caught at the decorator level (500) or the view level (500)
        assert resp.status_code == 500
        payload = resp.get_json()
        assert payload.get('success') is False
        assert payload.get('version') == VERSION

    def test_production_error_message_is_japanese(self, monkeypatch, client):
        """ensure_json_response wraps uncaught exceptions with a Japanese message in prod.

        We target /api/health because it has no inner try/except, so an exception
        raised there will propagate out to the decorator.
        """
        monkeypatch.setenv('RENDER', '1')

        # Patch the dict that health() returns into a callable that raises
        vetdict_api.health.__wrapped__ if hasattr(vetdict_api.health, '__wrapped__') else None

        def _raise_health():
            raise RuntimeError("db down")

        # Swap the health view function body by patching through the app's view functions map
        with flask_app.test_request_context('/api/health'):
            # Directly test the decorator by constructing a wrapped function
            from api.vetdict_api import ensure_json_response

            @ensure_json_response
            def bad_view():
                raise RuntimeError("production crash")

            monkeypatch.setenv('RENDER', '1')
            # Call directly — not via HTTP — so we get a Response object
            resp = bad_view()
            if isinstance(resp, tuple):
                body, status = resp
                payload = json.loads(body.get_data(as_text=True))
                assert status == 500
            else:
                payload = json.loads(resp.get_data(as_text=True))
                assert resp.status_code == 500
            assert payload.get('error') == 'エラーが発生しました。しばらくしてからもう一度お試しください。'
            assert payload.get('success') is False


# =============================================================================
# 6. POST /api/analyze-symptoms — validation
# =============================================================================


class TestAnalyzeSymptomsValidation:
    def test_missing_body_returns_400(self, client):
        resp = client.post('/api/analyze-symptoms', data='not json',
                           content_type='text/plain')
        assert resp.status_code == 400

    def test_missing_symptoms_key_returns_400(self, client):
        resp = client.post('/api/analyze-symptoms', json={'species': 'dog'})
        assert resp.status_code == 400
        assert 'symptoms' in resp.get_json()['error'].lower()

    def test_empty_symptoms_list_returns_400(self, client):
        resp = client.post('/api/analyze-symptoms',
                           json={'symptoms': [], 'species': 'dog'})
        assert resp.status_code == 400

    def test_symptoms_not_a_list_returns_400(self, client):
        resp = client.post('/api/analyze-symptoms',
                           json={'symptoms': 'vomiting', 'species': 'dog'})
        assert resp.status_code == 400

    def test_non_string_symptoms_return_400(self, client):
        resp = client.post('/api/analyze-symptoms',
                           json={'symptoms': ['vomiting', 1], 'species': 'dog'})
        assert resp.status_code == 400
        assert 'strings' in resp.get_json()['error']

    def test_blank_symptoms_return_400(self, client):
        resp = client.post('/api/analyze-symptoms',
                           json={'symptoms': ['   '], 'species': 'dog'})
        assert resp.status_code == 400
        assert 'At least one symptom' in resp.get_json()['error']

    def test_blank_symptom_items_are_filtered_before_forwarding(self, monkeypatch, client):
        captured = {}

        def fake_analyze(symptoms, **kwargs):
            captured['symptoms'] = symptoms
            return {'suspected_diseases': [], 'recommended_tests': [],
                    'severity': 'low', 'general_advice': '', 'general_advice_ja': ''}

        monkeypatch.setattr(vetdict_api, 'SYMPTOM_CHECKER_AVAILABLE', True)
        monkeypatch.setattr(vetdict_api, 'analyze_symptoms', fake_analyze)

        resp = client.post('/api/analyze-symptoms',
                           json={'symptoms': [' vomiting ', '   ', 'diarrhea'], 'species': 'dog'})

        assert resp.status_code == 200
        assert captured['symptoms'] == ['vomiting', 'diarrhea']

    def test_invalid_onset_returns_400(self, client):
        resp = client.post('/api/analyze-symptoms',
                           json={'symptoms': ['vomiting'], 'onset': 'immediate'})
        assert resp.status_code == 400
        assert 'onset' in resp.get_json()['error']

    def test_valid_onset_values_accepted(self, monkeypatch, client):
        fake = MagicMock(return_value={'suspected_diseases': [], 'recommended_tests': [],
                                       'severity': 'low', 'general_advice': '', 'general_advice_ja': ''})
        monkeypatch.setattr(vetdict_api, 'SYMPTOM_CHECKER_AVAILABLE', True)
        monkeypatch.setattr(vetdict_api, 'analyze_symptoms', fake)

        for onset in ('acute', 'subacute', 'chronic'):
            resp = client.post('/api/analyze-symptoms',
                               json={'symptoms': ['vomiting'], 'onset': onset})
            assert resp.status_code == 200, f"onset={onset!r} rejected unexpectedly"

    def test_invalid_gender_returns_400(self, client):
        resp = client.post('/api/analyze-symptoms',
                           json={'symptoms': ['vomiting'], 'gender': 'unknown'})
        assert resp.status_code == 400
        assert resp.get_json()['error'] == "gender must be 'male' or 'female'"

    def test_valid_gender_values_accepted(self, monkeypatch, client):
        fake = MagicMock(return_value={'suspected_diseases': [], 'recommended_tests': [],
                                       'severity': 'low', 'general_advice': '', 'general_advice_ja': ''})
        monkeypatch.setattr(vetdict_api, 'SYMPTOM_CHECKER_AVAILABLE', True)
        monkeypatch.setattr(vetdict_api, 'analyze_symptoms', fake)

        for gender in ('male', 'female'):
            resp = client.post('/api/analyze-symptoms',
                               json={'symptoms': ['vomiting'], 'gender': gender})
            assert resp.status_code == 200, f"gender={gender!r} rejected unexpectedly"

    def test_invalid_vaccination_status_returns_400(self, client):
        resp = client.post('/api/analyze-symptoms',
                           json={'symptoms': ['vomiting'], 'vaccination_status': 'partial'})
        assert resp.status_code == 400
        assert "vaccination_status must be" in resp.get_json()['error']

    def test_valid_vaccination_status_values_accepted(self, monkeypatch, client):
        fake = MagicMock(return_value={'suspected_diseases': [], 'recommended_tests': [],
                                       'severity': 'low', 'general_advice': '', 'general_advice_ja': ''})
        monkeypatch.setattr(vetdict_api, 'SYMPTOM_CHECKER_AVAILABLE', True)
        monkeypatch.setattr(vetdict_api, 'analyze_symptoms', fake)

        for vs in ('current', 'outdated', 'none'):
            resp = client.post('/api/analyze-symptoms',
                               json={'symptoms': ['vomiting'], 'vaccination_status': vs})
            assert resp.status_code == 200, f"vaccination_status={vs!r} rejected unexpectedly"

    def test_non_numeric_age_years_returns_400(self, client):
        resp = client.post('/api/analyze-symptoms',
                           json={'symptoms': ['vomiting'], 'age_years': 'old'})
        assert resp.status_code == 400
        assert 'age_years' in resp.get_json()['error']

    def test_numeric_age_years_coerced_to_float(self, monkeypatch, client):
        captured = {}

        def fake_analyze(symptoms, **kwargs):
            captured['age_years'] = kwargs.get('age_years')
            return {'suspected_diseases': [], 'recommended_tests': [],
                    'severity': 'low', 'general_advice': '', 'general_advice_ja': ''}

        monkeypatch.setattr(vetdict_api, 'SYMPTOM_CHECKER_AVAILABLE', True)
        monkeypatch.setattr(vetdict_api, 'analyze_symptoms', fake_analyze)

        client.post('/api/analyze-symptoms',
                    json={'symptoms': ['vomiting'], 'age_years': 5})
        assert captured['age_years'] == 5.0

    def test_string_numeric_age_years_coerced(self, monkeypatch, client):
        captured = {}

        def fake_analyze(symptoms, **kwargs):
            captured['age_years'] = kwargs.get('age_years')
            return {'suspected_diseases': [], 'recommended_tests': [],
                    'severity': 'low', 'general_advice': '', 'general_advice_ja': ''}

        monkeypatch.setattr(vetdict_api, 'SYMPTOM_CHECKER_AVAILABLE', True)
        monkeypatch.setattr(vetdict_api, 'analyze_symptoms', fake_analyze)

        client.post('/api/analyze-symptoms',
                    json={'symptoms': ['vomiting'], 'age_years': '2.5'})
        assert captured['age_years'] == 2.5

    def test_lab_values_coerced_to_float(self, monkeypatch, client):
        captured = {}

        def fake_analyze(symptoms, **kwargs):
            captured['lab_values'] = kwargs.get('lab_values')
            return {'suspected_diseases': [], 'recommended_tests': [],
                    'severity': 'low', 'general_advice': '', 'general_advice_ja': ''}

        monkeypatch.setattr(vetdict_api, 'SYMPTOM_CHECKER_AVAILABLE', True)
        monkeypatch.setattr(vetdict_api, 'analyze_symptoms', fake_analyze)

        client.post('/api/analyze-symptoms',
                    json={'symptoms': ['vomiting'], 'lab_values': {'bun': '25', 'creatinine': 1.2}})
        assert captured['lab_values'] == {'bun': 25.0, 'creatinine': 1.2}

    def test_invalid_lab_values_entries_skipped(self, monkeypatch, client):
        captured = {}

        def fake_analyze(symptoms, **kwargs):
            captured['lab_values'] = kwargs.get('lab_values')
            return {'suspected_diseases': [], 'recommended_tests': [],
                    'severity': 'low', 'general_advice': '', 'general_advice_ja': ''}

        monkeypatch.setattr(vetdict_api, 'SYMPTOM_CHECKER_AVAILABLE', True)
        monkeypatch.setattr(vetdict_api, 'analyze_symptoms', fake_analyze)

        client.post('/api/analyze-symptoms',
                    json={'symptoms': ['vomiting'],
                          'lab_values': {'bun': 'not_a_number', 'creatinine': 1.2}})
        # 'bun' should be skipped; 'creatinine' should be kept
        assert captured['lab_values'] == {'creatinine': 1.2}

    def test_all_invalid_lab_values_become_none(self, monkeypatch, client):
        captured = {}

        def fake_analyze(symptoms, **kwargs):
            captured['lab_values'] = kwargs.get('lab_values')
            return {'suspected_diseases': [], 'recommended_tests': [],
                    'severity': 'low', 'general_advice': '', 'general_advice_ja': ''}

        monkeypatch.setattr(vetdict_api, 'SYMPTOM_CHECKER_AVAILABLE', True)
        monkeypatch.setattr(vetdict_api, 'analyze_symptoms', fake_analyze)

        client.post('/api/analyze-symptoms',
                    json={'symptoms': ['vomiting'],
                          'lab_values': {'bun': 'bad', 'alt': 'worse'}})
        assert captured['lab_values'] is None

    def test_valid_vaccines_forwarded(self, monkeypatch, client):
        captured = {}

        def fake_analyze(symptoms, **kwargs):
            captured['vaccines'] = kwargs.get('vaccines')
            return {'suspected_diseases': [], 'recommended_tests': [],
                    'severity': 'low', 'general_advice': '', 'general_advice_ja': ''}

        monkeypatch.setattr(vetdict_api, 'SYMPTOM_CHECKER_AVAILABLE', True)
        monkeypatch.setattr(vetdict_api, 'analyze_symptoms', fake_analyze)

        client.post('/api/analyze-symptoms',
                    json={'symptoms': ['vomiting'], 'vaccines': ['core_5in1', 'rabies']})
        assert captured['vaccines'] == ['core_5in1', 'rabies']

    def test_blank_vaccine_ids_are_filtered_out(self, monkeypatch, client):
        captured = {}

        def fake_analyze(symptoms, **kwargs):
            captured['vaccines'] = kwargs.get('vaccines')
            return {'suspected_diseases': [], 'recommended_tests': [],
                    'severity': 'low', 'general_advice': '', 'general_advice_ja': ''}

        monkeypatch.setattr(vetdict_api, 'SYMPTOM_CHECKER_AVAILABLE', True)
        monkeypatch.setattr(vetdict_api, 'analyze_symptoms', fake_analyze)

        client.post('/api/analyze-symptoms',
                    json={'symptoms': ['vomiting'], 'vaccines': [' rabies ', '   ']})
        assert captured['vaccines'] == ['rabies']

    def test_vaccines_not_a_list_returns_400(self, client):
        resp = client.post('/api/analyze-symptoms',
                           json={'symptoms': ['vomiting'], 'vaccines': 'rabies'})
        assert resp.status_code == 400
        assert 'vaccines' in resp.get_json()['error']

    def test_non_string_vaccines_return_400(self, client):
        resp = client.post('/api/analyze-symptoms',
                           json={'symptoms': ['vomiting'], 'vaccines': ['rabies', 1]})
        assert resp.status_code == 400
        assert 'strings' in resp.get_json()['error']

    def test_symptom_checker_unavailable_returns_500(self, monkeypatch, client):
        monkeypatch.setattr(vetdict_api, 'SYMPTOM_CHECKER_AVAILABLE', False)
        resp = client.post('/api/analyze-symptoms',
                           json={'symptoms': ['vomiting']})
        assert resp.status_code == 500
        assert 'not available' in resp.get_json()['error'].lower()


# =============================================================================
# 7. POST /api/analyze-symptoms — successful calls
# =============================================================================


class TestAnalyzeSymptomsSuccess:
    def _fake_result(self):
        return {
            'suspected_diseases': [{'name': 'Gastritis', 'likelihood': 0.8}],
            'recommended_tests': ['CBC'],
            'severity': 'moderate',
            'general_advice': 'See a vet',
            'general_advice_ja': '獣医に行く',
        }

    def test_dog_path_calls_analyze_symptoms(self, monkeypatch, client):
        mock = MagicMock(return_value=self._fake_result())
        monkeypatch.setattr(vetdict_api, 'SYMPTOM_CHECKER_AVAILABLE', True)
        monkeypatch.setattr(vetdict_api, 'analyze_symptoms', mock)

        resp = client.post('/api/analyze-symptoms',
                           json={'symptoms': ['vomiting', 'diarrhea'], 'species': 'dog'})
        assert resp.status_code == 200
        mock.assert_called_once()
        args, kwargs = mock.call_args
        assert 'vomiting' in args[0]

    def test_none_species_defaults_to_dog_path(self, monkeypatch, client):
        mock = MagicMock(return_value=self._fake_result())
        monkeypatch.setattr(vetdict_api, 'SYMPTOM_CHECKER_AVAILABLE', True)
        monkeypatch.setattr(vetdict_api, 'analyze_symptoms', mock)

        resp = client.post('/api/analyze-symptoms',
                           json={'symptoms': ['lethargy']})
        assert resp.status_code == 200
        mock.assert_called_once()

    def test_non_dog_species_calls_species_analyzer(self, monkeypatch, client):
        mock = MagicMock(return_value=self._fake_result())
        monkeypatch.setattr(vetdict_api, 'SYMPTOM_CHECKER_AVAILABLE', True)
        monkeypatch.setattr(vetdict_api, 'SPECIES_ANALYZER_AVAILABLE', True)
        monkeypatch.setattr(vetdict_api, 'analyze_species_symptoms', mock)

        resp = client.post('/api/analyze-symptoms',
                           json={'symptoms': ['lethargy'], 'species': 'cat'})
        assert resp.status_code == 200
        mock.assert_called_once()
        args, _ = mock.call_args
        assert args[0] == 'cat'

    def test_non_dog_species_without_species_analyzer_returns_500(self, monkeypatch, client):
        monkeypatch.setattr(vetdict_api, 'SYMPTOM_CHECKER_AVAILABLE', True)
        monkeypatch.setattr(vetdict_api, 'SPECIES_ANALYZER_AVAILABLE', False)

        resp = client.post('/api/analyze-symptoms',
                           json={'symptoms': ['lethargy'], 'species': 'cat'})
        assert resp.status_code == 500
        assert 'not available' in resp.get_json()['error'].lower()

    def test_value_error_from_analyzer_returns_400(self, monkeypatch, client):
        monkeypatch.setattr(vetdict_api, 'SYMPTOM_CHECKER_AVAILABLE', True)
        monkeypatch.setattr(vetdict_api, 'analyze_symptoms',
                            MagicMock(side_effect=ValueError("bad symptoms")))

        resp = client.post('/api/analyze-symptoms',
                           json={'symptoms': ['vomiting'], 'species': 'dog'})
        assert resp.status_code == 400
        assert 'bad symptoms' in resp.get_json()['error']

    def test_unexpected_exception_from_analyzer_returns_500(self, monkeypatch, client):
        monkeypatch.setattr(vetdict_api, 'SYMPTOM_CHECKER_AVAILABLE', True)
        monkeypatch.setattr(vetdict_api, 'analyze_symptoms',
                            MagicMock(side_effect=RuntimeError("db crash")))

        resp = client.post('/api/analyze-symptoms',
                           json={'symptoms': ['vomiting'], 'species': 'dog'})
        assert resp.status_code == 500

    def test_all_optional_params_forwarded_to_analyze_symptoms(self, monkeypatch, client):
        captured = {}

        def fake(symptoms, **kwargs):
            captured.update({'symptoms': symptoms, **kwargs})
            return {'suspected_diseases': [], 'recommended_tests': [],
                    'severity': 'low', 'general_advice': '', 'general_advice_ja': ''}

        monkeypatch.setattr(vetdict_api, 'SYMPTOM_CHECKER_AVAILABLE', True)
        monkeypatch.setattr(vetdict_api, 'analyze_symptoms', fake)

        client.post('/api/analyze-symptoms', json={
            'symptoms': ['vomiting'],
            'species': 'dog',
            'breed': 'labrador',
            'onset': 'acute',
            'age_years': 3.0,
            'lab_values': {'alt': 45.0},
            'gender': 'male',
            'vaccines': ['rabies'],
            'vaccination_status': 'current',
        })

        assert captured['breed'] == 'labrador'
        assert captured['onset'] == 'acute'
        assert captured['age_years'] == 3.0
        assert captured['lab_values'] == {'alt': 45.0}
        assert captured['gender'] == 'male'
        assert captured['vaccines'] == ['rabies']
        assert captured['vaccination_status'] == 'current'


# =============================================================================
# 8. GET /api/species/<species>/symptoms
# =============================================================================


class TestSpeciesSymptomsEndpoint:
    def test_dog_symptoms_returns_200(self, client):
        resp = client.get('/api/species/dog/symptoms')
        assert resp.status_code == 200

    def test_dog_symptoms_has_symptoms_key(self, client):
        payload = client.get('/api/species/dog/symptoms').get_json()
        assert 'symptoms' in payload
        assert isinstance(payload['symptoms'], list)

    def test_dog_symptoms_items_have_required_fields(self, client):
        symptoms = client.get('/api/species/dog/symptoms').get_json()['symptoms']
        assert len(symptoms) > 0
        for s in symptoms[:5]:  # spot-check first 5
            assert 'id' in s
            assert 'name_ja' in s
            assert 'name_en' in s
            assert 'category' in s

    def test_dog_localized_appetite_loss_label(self, client):
        symptoms = {s['id']: s for s in client.get('/api/species/dog/symptoms').get_json()['symptoms']}
        assert symptoms['appetite_loss']['name_ja'] == '食欲不振'
        assert symptoms['appetite_loss']['name_en'] == 'Appetite Loss'

    def test_cat_symptoms_returns_200(self, client):
        resp = client.get('/api/species/cat/symptoms')
        assert resp.status_code == 200

    def test_cat_symptoms_has_symptoms_key(self, client):
        payload = client.get('/api/species/cat/symptoms').get_json()
        assert 'symptoms' in payload

    def test_cat_localized_cyanosis_label(self, client):
        symptoms = {s['id']: s for s in client.get('/api/species/cat/symptoms').get_json()['symptoms']}
        assert symptoms['cyanosis']['name_ja'] == 'チアノーゼ'
        assert symptoms['cyanosis']['name_en'] == 'Cyanosis'

    def test_horse_symptoms_returns_200(self, client):
        resp = client.get('/api/species/horse/symptoms')
        assert resp.status_code == 200

    def test_horse_has_equine_specific_symptom(self, client):
        symptoms = {s['id']: s for s in client.get('/api/species/horse/symptoms').get_json()['symptoms']}
        assert 'limb_bucked_shin' in symptoms
        assert symptoms['limb_bucked_shin']['name_en'] == 'Bucked Shin'
        assert symptoms['limb_bucked_shin']['category'] == 'limb'

    def test_unknown_species_returns_empty_symptoms(self, client):
        payload = client.get('/api/species/dragon/symptoms').get_json()
        assert payload.get('symptoms') == []

    def test_rabbit_symptoms_endpoint_accessible(self, client):
        resp = client.get('/api/species/rabbit/symptoms')
        assert resp.status_code == 200
        assert 'symptoms' in resp.get_json()

    def test_bird_symptoms_endpoint_accessible(self, client):
        resp = client.get('/api/species/bird/symptoms')
        assert resp.status_code == 200
        assert 'symptoms' in resp.get_json()


# =============================================================================
# 9. GET /api/species-stats
# =============================================================================


class TestSpeciesStatsEndpoint:
    def test_returns_200(self, client):
        resp = client.get('/api/species-stats')
        assert resp.status_code == 200

    def test_has_species_list(self, client):
        payload = client.get('/api/species-stats').get_json()
        assert 'species' in payload
        assert isinstance(payload['species'], list)

    def test_species_count_matches_total_species(self, client):
        payload = client.get('/api/species-stats').get_json()
        assert payload['total_species'] == len(payload['species'])
        assert payload['total_species'] == 21

    def test_totals_are_non_negative_integers(self, client):
        payload = client.get('/api/species-stats').get_json()
        assert isinstance(payload['total_diseases'], int)
        assert payload['total_diseases'] >= 0
        assert isinstance(payload['total_drugs'], int)
        assert payload['total_drugs'] >= 0

    def test_each_species_entry_has_required_fields(self, client):
        species_list = client.get('/api/species-stats').get_json()['species']
        for entry in species_list:
            assert 'id' in entry
            assert 'name' in entry
            assert 'nameEn' in entry
            assert 'diseases' in entry
            assert 'drugs' in entry

    def test_dog_entry_exists_in_species_list(self, client):
        species_list = client.get('/api/species-stats').get_json()['species']
        ids = [s['id'] for s in species_list]
        assert 'dog' in ids

    def test_dog_disease_count_is_positive(self, client):
        species_list = client.get('/api/species-stats').get_json()['species']
        dog = next(s for s in species_list if s['id'] == 'dog')
        assert dog['diseases'] > 0

    def test_total_diseases_equals_sum_of_per_species_diseases(self, client):
        payload = client.get('/api/species-stats').get_json()
        computed = sum(s['diseases'] for s in payload['species'])
        assert payload['total_diseases'] == computed

    def test_version_injected(self, client):
        payload = client.get('/api/species-stats').get_json()
        assert payload.get('version') == VERSION


# =============================================================================
# 10. GET /api/breeds/<species>
# =============================================================================


class TestBreedsEndpoint:
    def test_dog_breeds_returns_200(self, client):
        resp = client.get('/api/breeds/dog')
        assert resp.status_code == 200

    def test_response_has_species_and_breeds(self, client):
        payload = client.get('/api/breeds/dog').get_json()
        assert payload.get('species') == 'dog'
        assert 'breeds' in payload
        assert isinstance(payload['breeds'], list)

    def test_each_breed_has_required_fields(self, client):
        breeds = client.get('/api/breeds/dog').get_json()['breeds']
        for breed in breeds[:5]:
            assert 'id' in breed
            assert 'name' in breed
            assert 'name_ja' in breed

    def test_unknown_species_returns_empty_breeds(self, client):
        payload = client.get('/api/breeds/unicorn').get_json()
        assert payload.get('breeds') == []
        assert payload.get('species') == 'unicorn'


# =============================================================================
# 10b. Husbandry endpoint
# =============================================================================


class TestHusbandryEndpoint:
    def test_dog_husbandry_returns_200(self, client):
        resp = client.get('/api/species/dog/husbandry')
        assert resp.status_code == 200

    def test_response_has_species_and_husbandry(self, client):
        payload = client.get('/api/species/dog/husbandry').get_json()
        assert payload.get('species') == 'dog'
        assert 'husbandry' in payload

    def test_husbandry_has_required_fields(self, client):
        data = client.get('/api/species/cat/husbandry').get_json()['husbandry']
        for field in ('name', 'name_ja', 'temperature', 'humidity', 'housing', 'diet'):
            assert field in data, f"Missing field: {field}"

    def test_bilingual_fields(self, client):
        data = client.get('/api/species/rabbit/husbandry').get_json()['husbandry']
        assert 'en' in data['temperature']
        assert 'ja' in data['temperature']

    def test_unknown_species_returns_404(self, client):
        resp = client.get('/api/species/unicorn/husbandry')
        assert resp.status_code == 404

    def test_all_species_return_200(self, client):
        species_list = [
            'dog', 'cat', 'rabbit', 'hamster', 'guinea_pig', 'chinchilla',
            'ferret', 'hedgehog', 'sugar_glider', 'degu', 'bird', 'parakeet',
            'parrot', 'reptile', 'tortoise', 'snake', 'lizard', 'amphibian',
            'fish', 'exotic_other', 'horse',
        ]
        for sp in species_list:
            resp = client.get(f'/api/species/{sp}/husbandry')
            assert resp.status_code == 200, f"{sp}: expected 200, got {resp.status_code}"


# =============================================================================
# 11. Protected RECO2 routes — authentication / 503
# =============================================================================


class TestProtectedRoutes:
    """Protected routes require INTERNAL_API_TOKEN env var + Bearer header.
    When RECO2 is unavailable they return 503."""

    PROTECTED_GET_ROUTES = ['/api/status', '/api/logs', '/api/r3/config']
    PROTECTED_POST_ROUTES = ['/api/evaluate', '/api/feedback', '/api/patrol',
                              '/api/r3/analyze_input', '/api/r3/analyze_output', '/api/r3/chat']

    def _disable_token(self, monkeypatch):
        monkeypatch.delenv('INTERNAL_API_TOKEN', raising=False)

    def _set_token(self, monkeypatch, token='test-token'):
        monkeypatch.setenv('INTERNAL_API_TOKEN', token)

    # --- Without token configured, requests pass through to the route body ---

    def test_status_without_token_config_returns_503_when_reco2_unavailable(
            self, monkeypatch, client):
        self._disable_token(monkeypatch)
        monkeypatch.setattr(vetdict_api, 'RECO2_AVAILABLE', False)

        resp = client.get('/api/status')
        assert resp.status_code == 503
        assert resp.get_json()['error'] == 'reco2 not available'

    def test_logs_without_token_config_returns_503_when_reco2_unavailable(
            self, monkeypatch, client):
        self._disable_token(monkeypatch)
        monkeypatch.setattr(vetdict_api, 'RECO2_AVAILABLE', False)

        resp = client.get('/api/logs')
        assert resp.status_code == 503

    def test_evaluate_without_token_config_returns_503_when_reco2_unavailable(
            self, monkeypatch, client):
        self._disable_token(monkeypatch)
        monkeypatch.setattr(vetdict_api, 'RECO2_AVAILABLE', False)

        resp = client.post('/api/evaluate', json={})
        assert resp.status_code == 503

    def test_feedback_without_token_config_returns_503_when_reco2_unavailable(
            self, monkeypatch, client):
        self._disable_token(monkeypatch)
        monkeypatch.setattr(vetdict_api, 'RECO2_AVAILABLE', False)

        resp = client.post('/api/feedback', json={})
        assert resp.status_code == 503

    def test_patrol_without_token_config_returns_503_when_reco2_unavailable(
            self, monkeypatch, client):
        self._disable_token(monkeypatch)
        monkeypatch.setattr(vetdict_api, 'RECO2_AVAILABLE', False)

        resp = client.post('/api/patrol', json={})
        assert resp.status_code == 503

    def test_r3_config_without_token_config_returns_503_when_reco2_unavailable(
            self, monkeypatch, client):
        self._disable_token(monkeypatch)
        monkeypatch.setattr(vetdict_api, 'RECO2_AVAILABLE', False)

        resp = client.get('/api/r3/config')
        assert resp.status_code == 503

    def test_r3_analyze_input_without_token_config_returns_503_when_reco2_unavailable(
            self, monkeypatch, client):
        self._disable_token(monkeypatch)
        monkeypatch.setattr(vetdict_api, 'RECO2_AVAILABLE', False)

        resp = client.post('/api/r3/analyze_input', json={'text': 'test'})
        assert resp.status_code == 503

    def test_r3_analyze_output_without_token_config_returns_503_when_reco2_unavailable(
            self, monkeypatch, client):
        self._disable_token(monkeypatch)
        monkeypatch.setattr(vetdict_api, 'RECO2_AVAILABLE', False)

        resp = client.post('/api/r3/analyze_output', json={'text': 'test'})
        assert resp.status_code == 503

    def test_r3_chat_without_token_config_returns_503_when_reco2_unavailable(
            self, monkeypatch, client):
        self._disable_token(monkeypatch)
        monkeypatch.setattr(vetdict_api, 'RECO2_AVAILABLE', False)

        resp = client.post('/api/r3/chat', json={'prompt': 'hello'})
        assert resp.status_code == 503

    # --- With token configured, missing/wrong auth returns 401 ---

    def test_get_routes_return_401_without_auth_header(self, monkeypatch, client):
        self._set_token(monkeypatch)
        for route in self.PROTECTED_GET_ROUTES:
            resp = client.get(route)
            assert resp.status_code == 401, f"{route} should be 401, got {resp.status_code}"
            assert resp.get_json()['error'] == 'Unauthorized'

    def test_post_routes_return_401_without_auth_header(self, monkeypatch, client):
        self._set_token(monkeypatch)
        for route in self.PROTECTED_POST_ROUTES:
            resp = client.post(route, json={})
            assert resp.status_code == 401, f"{route} should be 401, got {resp.status_code}"

    def test_wrong_token_returns_401(self, monkeypatch, client):
        self._set_token(monkeypatch, token='correct-token')
        resp = client.get('/api/status',
                          headers=_auth_header('wrong-token'))
        assert resp.status_code == 401

    def test_correct_token_passes_auth_gate(self, monkeypatch, client):
        self._set_token(monkeypatch, token='my-secret')
        monkeypatch.setattr(vetdict_api, 'RECO2_AVAILABLE', False)

        resp = client.get('/api/status', headers=_auth_header('my-secret'))
        # RECO2 unavailable, so 503 — but 401 was NOT returned
        assert resp.status_code == 503
        assert resp.get_json()['error'] == 'reco2 not available'

    def test_rate_limiting_returns_429(self, monkeypatch, client):
        monkeypatch.setenv('INTERNAL_API_TOKEN', 'rate-test-token')
        monkeypatch.setenv('INTERNAL_API_RATE_LIMIT_MAX_REQUESTS', '2')
        monkeypatch.setenv('INTERNAL_API_RATE_LIMIT_WINDOW_SECONDS', '60')
        reset_rate_limiting()

        r1 = client.get('/api/status')
        r2 = client.get('/api/status')
        r3 = client.get('/api/status')

        assert r1.status_code == 401
        assert r2.status_code == 401
        assert r3.status_code == 429
        assert r3.get_json()['error'] == vetdict_api.RATE_LIMIT_ERROR_MESSAGE

    def test_rate_limited_response_includes_version(self, monkeypatch, client):
        monkeypatch.setenv('INTERNAL_API_TOKEN', 'rate-test-token')
        monkeypatch.setenv('INTERNAL_API_RATE_LIMIT_MAX_REQUESTS', '1')
        monkeypatch.setenv('INTERNAL_API_RATE_LIMIT_WINDOW_SECONDS', '60')
        reset_rate_limiting()

        client.get('/api/status')  # exhaust limit
        resp = client.get('/api/status')
        assert resp.status_code == 429
        assert resp.get_json().get('version') == VERSION

    def test_logs_limit_query_param_defaults_to_50(self, monkeypatch, client):
        self._disable_token(monkeypatch)
        mock_get_logs = MagicMock(return_value={'logs': [], 'total': 0})
        monkeypatch.setattr(vetdict_api, 'RECO2_AVAILABLE', True)
        monkeypatch.setattr(vetdict_api, 'reco2_get_logs', mock_get_logs)

        client.get('/api/logs')
        mock_get_logs.assert_called_once_with(limit=50)

    def test_logs_limit_query_param_respected(self, monkeypatch, client):
        self._disable_token(monkeypatch)
        mock_get_logs = MagicMock(return_value={'logs': [], 'total': 0})
        monkeypatch.setattr(vetdict_api, 'RECO2_AVAILABLE', True)
        monkeypatch.setattr(vetdict_api, 'reco2_get_logs', mock_get_logs)

        client.get('/api/logs?limit=10')
        mock_get_logs.assert_called_once_with(limit=10)

    def test_logs_invalid_limit_falls_back_to_50(self, monkeypatch, client):
        self._disable_token(monkeypatch)
        mock_get_logs = MagicMock(return_value={'logs': [], 'total': 0})
        monkeypatch.setattr(vetdict_api, 'RECO2_AVAILABLE', True)
        monkeypatch.setattr(vetdict_api, 'reco2_get_logs', mock_get_logs)

        client.get('/api/logs?limit=abc')
        mock_get_logs.assert_called_once_with(limit=50)


# =============================================================================
# 12. RECO2 routes — successful calls (RECO2 mocked as available)
# =============================================================================


class TestReco2RoutesWithMocks:
    def _no_token(self, monkeypatch):
        monkeypatch.delenv('INTERNAL_API_TOKEN', raising=False)

    def test_status_returns_reco2_status(self, monkeypatch, client):
        self._no_token(monkeypatch)
        monkeypatch.setattr(vetdict_api, 'RECO2_AVAILABLE', True)
        mock_status = MagicMock(return_value={'status': 'ok', 'patrol_count': 5})
        monkeypatch.setattr(vetdict_api, 'reco2_get_status', mock_status)

        resp = client.get('/api/status')
        assert resp.status_code == 200
        assert resp.get_json()['status'] == 'ok'

    def test_evaluate_forwards_payload(self, monkeypatch, client):
        self._no_token(monkeypatch)
        monkeypatch.setattr(vetdict_api, 'RECO2_AVAILABLE', True)
        mock_eval = MagicMock(return_value={'score': 0.9})
        monkeypatch.setattr(vetdict_api, 'reco2_evaluate_payload', mock_eval)

        resp = client.post('/api/evaluate', json={'text': 'test input'})
        assert resp.status_code == 200
        mock_eval.assert_called_once()

    def test_feedback_forwards_payload(self, monkeypatch, client):
        self._no_token(monkeypatch)
        monkeypatch.setattr(vetdict_api, 'RECO2_AVAILABLE', True)
        mock_feedback = MagicMock(return_value={'recorded': True})
        monkeypatch.setattr(vetdict_api, 'reco2_record_feedback', mock_feedback)

        resp = client.post('/api/feedback', json={'rating': 5})
        assert resp.status_code == 200

    def test_feedback_returns_tuple_response(self, monkeypatch, client):
        """When reco2_record_feedback returns a (body, status) tuple the route unwraps it."""
        self._no_token(monkeypatch)
        monkeypatch.setattr(vetdict_api, 'RECO2_AVAILABLE', True)
        monkeypatch.setattr(vetdict_api, 'reco2_record_feedback',
                            MagicMock(return_value=({'recorded': False, 'reason': 'missing id'}, 400)))

        resp = client.post('/api/feedback', json={})
        assert resp.status_code == 400

    def test_patrol_calls_reco2_patrol(self, monkeypatch, client):
        self._no_token(monkeypatch)
        monkeypatch.setattr(vetdict_api, 'RECO2_AVAILABLE', True)
        mock_patrol = MagicMock(return_value={'patrolled': True})
        monkeypatch.setattr(vetdict_api, 'reco2_patrol', mock_patrol)

        resp = client.post('/api/patrol', json={})
        assert resp.status_code == 200
        mock_patrol.assert_called_once_with(manual=True)

    def test_r3_config_returns_public_config(self, monkeypatch, client):
        self._no_token(monkeypatch)
        monkeypatch.setattr(vetdict_api, 'RECO2_AVAILABLE', True)
        monkeypatch.setattr(vetdict_api, 'load_reco2_config', MagicMock(return_value={}))
        monkeypatch.setattr(vetdict_api, 'public_reco2_config',
                            MagicMock(return_value={'public_key': 'value'}))

        resp = client.get('/api/r3/config')
        assert resp.status_code == 200
        assert resp.get_json()['public_key'] == 'value'

    def test_r3_analyze_input_calls_input_gate(self, monkeypatch, client):
        self._no_token(monkeypatch)
        monkeypatch.setattr(vetdict_api, 'RECO2_AVAILABLE', True)
        mock_gate = MagicMock()
        mock_gate.analyze = MagicMock(return_value={'score': 0.1})
        monkeypatch.setattr(vetdict_api, 'input_gate', mock_gate)
        monkeypatch.setattr(vetdict_api, 'load_reco2_config', MagicMock(return_value={
            'input_w_ambiguity': 0.2, 'input_w_assertion': 0.25,
            'input_w_emotion': 0.3, 'input_w_unrealistic': 0.25,
        }))

        resp = client.post('/api/r3/analyze_input', json={'text': 'my dog is sick'})
        assert resp.status_code == 200
        mock_gate.analyze.assert_called_once()
        call_args = mock_gate.analyze.call_args
        assert call_args[0][0] == 'my dog is sick'

    def test_r3_analyze_output_calls_output_gate(self, monkeypatch, client):
        self._no_token(monkeypatch)
        monkeypatch.setattr(vetdict_api, 'RECO2_AVAILABLE', True)
        mock_gate = MagicMock()
        mock_gate.analyze = MagicMock(return_value={'score': 0.2})
        monkeypatch.setattr(vetdict_api, 'output_gate', mock_gate)
        monkeypatch.setattr(vetdict_api, 'load_reco2_config', MagicMock(return_value={
            'output_w_assertion': 0.3, 'output_w_evidence': 0.3,
            'output_w_contradiction': 0.25, 'output_w_provocative': 0.15,
        }))

        resp = client.post('/api/r3/analyze_output', json={'text': 'diagnosis output'})
        assert resp.status_code == 200
        mock_gate.analyze.assert_called_once()

    def test_r3_chat_calls_orchestrator_process(self, monkeypatch, client):
        self._no_token(monkeypatch)
        monkeypatch.setattr(vetdict_api, 'RECO2_AVAILABLE', True)
        mock_orch = MagicMock()
        mock_orch.process = MagicMock(return_value={'response': 'result'})
        monkeypatch.setattr(vetdict_api, 'reco2_get_orchestrator',
                            MagicMock(return_value=mock_orch))

        resp = client.post('/api/r3/chat', json={
            'prompt': 'what ails my cat?',
            'domain': 'veterinary',
            'max_tokens': 512,
        })
        assert resp.status_code == 200
        mock_orch.process.assert_called_once_with(
            'what ails my cat?', domain='veterinary', context={}, max_tokens=512
        )

    def test_r3_chat_defaults_domain_and_max_tokens(self, monkeypatch, client):
        self._no_token(monkeypatch)
        monkeypatch.setattr(vetdict_api, 'RECO2_AVAILABLE', True)
        mock_orch = MagicMock()
        mock_orch.process = MagicMock(return_value={'response': 'ok'})
        monkeypatch.setattr(vetdict_api, 'reco2_get_orchestrator',
                            MagicMock(return_value=mock_orch))

        client.post('/api/r3/chat', json={'prompt': 'hello'})
        _, kwargs = mock_orch.process.call_args
        assert kwargs['domain'] == 'general'
        assert kwargs['max_tokens'] == 1024

    def test_r3_analyze_input_empty_body_uses_empty_string(self, monkeypatch, client):
        self._no_token(monkeypatch)
        monkeypatch.setattr(vetdict_api, 'RECO2_AVAILABLE', True)
        mock_gate = MagicMock()
        mock_gate.analyze = MagicMock(return_value={'score': 0.0})
        monkeypatch.setattr(vetdict_api, 'input_gate', mock_gate)
        monkeypatch.setattr(vetdict_api, 'load_reco2_config', MagicMock(return_value={}))

        resp = client.post('/api/r3/analyze_input', json={})
        assert resp.status_code == 200
        call_args = mock_gate.analyze.call_args
        assert call_args[0][0] == ''


# =============================================================================
# 13. App-level constants and configuration
# =============================================================================


class TestAppConstants:
    def test_version_is_string(self):
        assert isinstance(VERSION, str)
        assert VERSION == '5.0.0'

    def test_rate_limit_error_message_is_japanese(self):
        assert vetdict_api.RATE_LIMIT_ERROR_MESSAGE == 'リクエスト制限に達しました。'

    def test_app_max_content_length_is_16mb(self):
        assert flask_app.config['MAX_CONTENT_LENGTH'] == 16 * 1024 * 1024

    def test_app_has_secret_key(self):
        assert flask_app.secret_key is not None
        assert flask_app.secret_key != ''

    def test_feature_flags_are_booleans(self):
        for attr in ('SYMPTOM_CHECKER_AVAILABLE', 'SPECIES_ANALYZER_AVAILABLE',
                     'HEALTH_CHECKER_AVAILABLE', 'DIAGNOSTIC_CHAT_AVAILABLE',
                     'DRUG_DICTIONARY_AVAILABLE', 'RECO2_AVAILABLE'):
            assert isinstance(getattr(vetdict_api, attr), bool), f"{attr} should be bool"
