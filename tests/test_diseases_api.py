"""Tests for public read-only diseases API routes."""

from unittest.mock import patch

import flask

from api.routes.diseases_api import diseases_bp


def _create_app():
    app = flask.Flask(__name__)
    app.config["TESTING"] = True
    app.register_blueprint(diseases_bp)
    return app


# ---------------------------------------------------------------------------
# GET /api/diseases
# ---------------------------------------------------------------------------


class TestListDiseases:
    """Tests for GET /api/diseases."""

    def setup_method(self):
        self.app = _create_app()
        self.client = self.app.test_client()

    def test_list_diseases_default(self):
        mock_result = {"diseases": [{"id": "d1", "name": "Parvovirus"}], "total": 1}
        with patch("api.routes.diseases_api.list_diseases", return_value=mock_result):
            resp = self.client.get("/api/diseases")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["success"] is True
        assert "diseases" in data

    def test_list_diseases_with_species_filter(self):
        mock_result = {"diseases": [], "total": 0}
        with patch("api.routes.diseases_api.list_diseases", return_value=mock_result) as mock_fn:
            resp = self.client.get("/api/diseases?species=cat")
        assert resp.status_code == 200
        mock_fn.assert_called_once_with(species="cat", limit=200, offset=0)

    def test_list_diseases_with_search_query(self):
        mock_results = [{"id": "d1", "name": "FIP"}]
        with patch("api.routes.diseases_api.search_diseases", return_value=mock_results) as mock_fn:
            resp = self.client.get("/api/diseases?q=FIP&species=cat")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["total"] == 1
        mock_fn.assert_called_once_with("FIP", species="cat", limit=200)

    def test_list_diseases_invalid_limit(self):
        resp = self.client.get("/api/diseases?limit=abc")
        assert resp.status_code == 400
        assert "Invalid" in resp.get_json()["error"]

    def test_list_diseases_limit_clamped(self):
        mock_result = {"diseases": [], "total": 0}
        with patch("api.routes.diseases_api.list_diseases", return_value=mock_result) as mock_fn:
            self.client.get("/api/diseases?limit=5000")
        mock_fn.assert_called_once_with(species=None, limit=1000, offset=0)

    def test_list_diseases_pagination(self):
        mock_result = {"diseases": [], "total": 0}
        with patch("api.routes.diseases_api.list_diseases", return_value=mock_result) as mock_fn:
            self.client.get("/api/diseases?limit=50&offset=100")
        mock_fn.assert_called_once_with(species=None, limit=50, offset=100)


# ---------------------------------------------------------------------------
# GET /api/diseases/<id>
# ---------------------------------------------------------------------------


class TestGetDisease:
    """Tests for GET /api/diseases/<disease_id>."""

    def setup_method(self):
        self.app = _create_app()
        self.client = self.app.test_client()

    def test_get_disease_found(self):
        mock_disease = {"id": "canine_parvovirus", "name": "Parvovirus"}
        with patch("api.routes.diseases_api.get_disease_detail", return_value=mock_disease):
            resp = self.client.get("/api/diseases/canine_parvovirus")
        assert resp.status_code == 200
        assert resp.get_json()["disease"]["id"] == "canine_parvovirus"

    def test_get_disease_not_found(self):
        with patch("api.routes.diseases_api.get_disease_detail", return_value=None):
            resp = self.client.get("/api/diseases/nonexistent")
        assert resp.status_code == 404
        assert resp.get_json()["success"] is False


# ---------------------------------------------------------------------------
# GET /api/symptoms/<symptom_id>/diseases
# ---------------------------------------------------------------------------


class TestDiseasesBySymptom:
    """Tests for GET /api/symptoms/<symptom_id>/diseases."""

    def setup_method(self):
        self.app = _create_app()
        self.client = self.app.test_client()

    def test_diseases_by_symptom(self):
        mock = [{"id": "d1", "name": "Disease A"}]
        with patch("api.routes.diseases_api.get_diseases_by_symptom", return_value=mock):
            resp = self.client.get("/api/symptoms/vomiting/diseases")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["symptom_id"] == "vomiting"
        assert len(data["diseases"]) == 1

    def test_diseases_by_symptom_with_species(self):
        with patch("api.routes.diseases_api.get_diseases_by_symptom", return_value=[]) as mock_fn:
            self.client.get("/api/symptoms/vomiting/diseases?species=dog&limit=10")
        mock_fn.assert_called_once_with("vomiting", species="dog", limit=10)

    def test_diseases_by_symptom_invalid_limit_defaults(self):
        with patch("api.routes.diseases_api.get_diseases_by_symptom", return_value=[]) as mock_fn:
            self.client.get("/api/symptoms/fever/diseases?limit=abc")
        mock_fn.assert_called_once_with("fever", species=None, limit=50)


# ---------------------------------------------------------------------------
# GET /api/urgency-stats
# ---------------------------------------------------------------------------


class TestUrgencyStats:
    """Tests for urgency stats endpoints."""

    def setup_method(self):
        self.app = _create_app()
        self.client = self.app.test_client()

    def test_urgency_stats(self):
        mock = {"emergency": 50, "high": 100, "medium": 200}
        with patch("api.routes.diseases_api.get_urgency_stats", return_value=mock):
            resp = self.client.get("/api/urgency-stats")
        assert resp.status_code == 200
        assert resp.get_json()["success"] is True

    def test_urgency_by_species(self):
        mock = {"emergency": 5, "high": 10}
        with patch("api.routes.diseases_api.get_urgency_by_species", return_value=mock):
            resp = self.client.get("/api/species/cat/urgency-stats")
        assert resp.status_code == 200
        assert resp.get_json()["success"] is True
