"""Tests for admin API routes (disease/drug CRUD via SQLite)."""

from unittest.mock import MagicMock, patch

import flask

from api.routes.admin_api import admin_bp


def _create_app():
    app = flask.Flask(__name__)
    app.config["TESTING"] = True
    app.register_blueprint(admin_bp)
    return app


# ---------------------------------------------------------------------------
# GET /api/admin/diseases
# ---------------------------------------------------------------------------


class TestAdminListDiseases:
    def setup_method(self):
        self.app = _create_app()
        self.client = self.app.test_client()

    def test_list_diseases_no_filter(self):
        mock_conn = MagicMock()
        mock_conn.execute.return_value.fetchall.return_value = [
            {"id": "d1", "species": "dog", "name": "Parvo", "name_ja": "パルボ", "urgency": "emergency"}
        ]
        with patch("api.routes.admin_api.get_connection") as mock_gc:
            mock_gc.return_value.__enter__ = MagicMock(return_value=mock_conn)
            mock_gc.return_value.__exit__ = MagicMock(return_value=False)
            resp = self.client.get("/api/admin/diseases")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["success"] is True
        assert data["count"] == 1

    def test_list_diseases_with_species_filter(self):
        with (
            patch("api.routes.admin_api.get_connection") as mock_gc,
            patch("api.routes.admin_api.get_diseases_by_species", return_value=[]) as mock_fn,
        ):
            mock_gc.return_value.__enter__ = MagicMock(return_value=MagicMock())
            mock_gc.return_value.__exit__ = MagicMock(return_value=False)
            resp = self.client.get("/api/admin/diseases?species=cat")
        assert resp.status_code == 200
        mock_fn.assert_called_once()


# ---------------------------------------------------------------------------
# GET /api/admin/diseases/<id>
# ---------------------------------------------------------------------------


class TestAdminGetDisease:
    def setup_method(self):
        self.app = _create_app()
        self.client = self.app.test_client()

    def test_get_disease_found(self):
        mock_disease = {"id": "d1", "name": "Parvo", "species": "dog"}
        with patch("api.routes.admin_api.get_connection") as mock_gc:
            mock_gc.return_value.__enter__ = MagicMock(return_value=MagicMock())
            mock_gc.return_value.__exit__ = MagicMock(return_value=False)
            with patch("api.routes.admin_api.get_disease_by_id", return_value=mock_disease):
                resp = self.client.get("/api/admin/diseases/d1")
        assert resp.status_code == 200
        assert resp.get_json()["disease"]["id"] == "d1"

    def test_get_disease_not_found(self):
        with patch("api.routes.admin_api.get_connection") as mock_gc:
            mock_gc.return_value.__enter__ = MagicMock(return_value=MagicMock())
            mock_gc.return_value.__exit__ = MagicMock(return_value=False)
            with patch("api.routes.admin_api.get_disease_by_id", return_value=None):
                resp = self.client.get("/api/admin/diseases/nonexistent")
        assert resp.status_code == 404


# ---------------------------------------------------------------------------
# POST /api/admin/diseases
# ---------------------------------------------------------------------------


class TestAdminCreateDisease:
    def setup_method(self):
        self.app = _create_app()
        self.client = self.app.test_client()

    def test_create_disease_success(self):
        with (
            patch("api.routes.admin_api.get_connection") as mock_gc,
            patch("api.routes.admin_api.upsert_disease"),
            patch("api.routes.admin_api.invalidate_cache"),
        ):
            mock_gc.return_value.__enter__ = MagicMock(return_value=MagicMock())
            mock_gc.return_value.__exit__ = MagicMock(return_value=False)
            resp = self.client.post(
                "/api/admin/diseases",
                json={"id": "new_disease", "species": "cat", "name": "New Disease"},
            )
        assert resp.status_code == 201
        assert resp.get_json()["id"] == "new_disease"

    def test_create_disease_missing_id(self):
        resp = self.client.post(
            "/api/admin/diseases",
            json={"species": "cat", "name": "No ID"},
        )
        assert resp.status_code == 400

    def test_create_disease_missing_species(self):
        resp = self.client.post(
            "/api/admin/diseases",
            json={"id": "d1", "name": "No Species"},
        )
        assert resp.status_code == 400


# ---------------------------------------------------------------------------
# PUT /api/admin/diseases/<id>
# ---------------------------------------------------------------------------


class TestAdminUpdateDisease:
    def setup_method(self):
        self.app = _create_app()
        self.client = self.app.test_client()

    def test_update_disease_success(self):
        existing = {"id": "d1", "name": "Old", "species": "dog"}
        with (
            patch("api.routes.admin_api.get_connection") as mock_gc,
            patch("api.routes.admin_api.get_disease_by_id", return_value=existing),
            patch("api.routes.admin_api.upsert_disease"),
            patch("api.routes.admin_api.invalidate_cache"),
        ):
            mock_gc.return_value.__enter__ = MagicMock(return_value=MagicMock())
            mock_gc.return_value.__exit__ = MagicMock(return_value=False)
            resp = self.client.put(
                "/api/admin/diseases/d1",
                json={"name": "Updated"},
            )
        assert resp.status_code == 200
        assert resp.get_json()["id"] == "d1"

    def test_update_disease_not_found(self):
        with (
            patch("api.routes.admin_api.get_connection") as mock_gc,
            patch("api.routes.admin_api.get_disease_by_id", return_value=None),
        ):
            mock_gc.return_value.__enter__ = MagicMock(return_value=MagicMock())
            mock_gc.return_value.__exit__ = MagicMock(return_value=False)
            resp = self.client.put(
                "/api/admin/diseases/missing",
                json={"name": "Update"},
            )
        assert resp.status_code == 404

    def test_update_disease_empty_body(self):
        resp = self.client.put(
            "/api/admin/diseases/d1",
            content_type="application/json",
            data="null",
        )
        assert resp.status_code == 400


# ---------------------------------------------------------------------------
# DELETE /api/admin/diseases/<id>
# ---------------------------------------------------------------------------


class TestAdminDeleteDisease:
    def setup_method(self):
        self.app = _create_app()
        self.client = self.app.test_client()

    def test_delete_disease_success(self):
        with (
            patch("api.routes.admin_api.get_connection") as mock_gc,
            patch("api.routes.admin_api.delete_disease", return_value=True),
            patch("api.routes.admin_api.invalidate_cache"),
        ):
            mock_gc.return_value.__enter__ = MagicMock(return_value=MagicMock())
            mock_gc.return_value.__exit__ = MagicMock(return_value=False)
            resp = self.client.delete("/api/admin/diseases/d1")
        assert resp.status_code == 200
        assert resp.get_json()["deleted"] == "d1"

    def test_delete_disease_not_found(self):
        with (
            patch("api.routes.admin_api.get_connection") as mock_gc,
            patch("api.routes.admin_api.delete_disease", return_value=False),
        ):
            mock_gc.return_value.__enter__ = MagicMock(return_value=MagicMock())
            mock_gc.return_value.__exit__ = MagicMock(return_value=False)
            resp = self.client.delete("/api/admin/diseases/missing")
        assert resp.status_code == 404


# ---------------------------------------------------------------------------
# GET /api/admin/diseases/stats
# ---------------------------------------------------------------------------


class TestAdminDiseaseStats:
    def setup_method(self):
        self.app = _create_app()
        self.client = self.app.test_client()

    def test_disease_stats(self):
        mock_stats = {"total": 6393, "by_species": {"dog": 579, "cat": 530}}
        with (
            patch("api.routes.admin_api.get_connection") as mock_gc,
            patch("api.routes.admin_api.count_diseases", return_value=mock_stats),
        ):
            mock_gc.return_value.__enter__ = MagicMock(return_value=MagicMock())
            mock_gc.return_value.__exit__ = MagicMock(return_value=False)
            resp = self.client.get("/api/admin/diseases/stats")
        assert resp.status_code == 200
        assert resp.get_json()["total"] == 6393


# ---------------------------------------------------------------------------
# Drug endpoints
# ---------------------------------------------------------------------------


class TestAdminDrugs:
    def setup_method(self):
        self.app = _create_app()
        self.client = self.app.test_client()

    def test_list_drugs(self):
        with (
            patch("api.routes.admin_api.get_connection") as mock_gc,
            patch("api.routes.admin_api.get_all_drugs", return_value=[{"id": "amoxicillin"}]),
        ):
            mock_gc.return_value.__enter__ = MagicMock(return_value=MagicMock())
            mock_gc.return_value.__exit__ = MagicMock(return_value=False)
            resp = self.client.get("/api/admin/drugs")
        assert resp.status_code == 200
        assert resp.get_json()["count"] == 1

    def test_get_drug_found(self):
        mock_drug = {"id": "amoxicillin", "name": "Amoxicillin"}
        with (
            patch("api.routes.admin_api.get_connection") as mock_gc,
            patch("api.routes.admin_api.get_drug_by_id", return_value=mock_drug),
        ):
            mock_gc.return_value.__enter__ = MagicMock(return_value=MagicMock())
            mock_gc.return_value.__exit__ = MagicMock(return_value=False)
            resp = self.client.get("/api/admin/drugs/amoxicillin")
        assert resp.status_code == 200
        assert resp.get_json()["drug"]["id"] == "amoxicillin"

    def test_get_drug_not_found(self):
        with (
            patch("api.routes.admin_api.get_connection") as mock_gc,
            patch("api.routes.admin_api.get_drug_by_id", return_value=None),
        ):
            mock_gc.return_value.__enter__ = MagicMock(return_value=MagicMock())
            mock_gc.return_value.__exit__ = MagicMock(return_value=False)
            resp = self.client.get("/api/admin/drugs/nonexistent")
        assert resp.status_code == 404

    def test_create_drug_success(self):
        with (
            patch("api.routes.admin_api.get_connection") as mock_gc,
            patch("api.routes.admin_api.upsert_drug"),
        ):
            mock_gc.return_value.__enter__ = MagicMock(return_value=MagicMock())
            mock_gc.return_value.__exit__ = MagicMock(return_value=False)
            resp = self.client.post(
                "/api/admin/drugs",
                json={"id": "new_drug", "name": "New Drug"},
            )
        assert resp.status_code == 201

    def test_create_drug_missing_id(self):
        resp = self.client.post(
            "/api/admin/drugs",
            json={"name": "No ID Drug"},
        )
        assert resp.status_code == 400


# ---------------------------------------------------------------------------
# POST /api/admin/import (bulk)
# ---------------------------------------------------------------------------


class TestAdminBulkImport:
    def setup_method(self):
        self.app = _create_app()
        self.client = self.app.test_client()

    def test_bulk_import_success(self):
        diseases = [
            {"id": "d1", "species": "cat", "name": "Disease 1"},
            {"id": "d2", "species": "cat", "name": "Disease 2"},
        ]
        with (
            patch("api.routes.admin_api.get_connection") as mock_gc,
            patch("api.routes.admin_api.upsert_disease"),
            patch("api.routes.admin_api.invalidate_cache"),
        ):
            mock_gc.return_value.__enter__ = MagicMock(return_value=MagicMock())
            mock_gc.return_value.__exit__ = MagicMock(return_value=False)
            resp = self.client.post(
                "/api/admin/import",
                json={"diseases": diseases},
            )
        assert resp.status_code == 201
        assert resp.get_json()["imported"] == 2

    def test_bulk_import_empty_list(self):
        resp = self.client.post(
            "/api/admin/import",
            json={"diseases": []},
        )
        assert resp.status_code == 400
