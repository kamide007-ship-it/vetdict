"""Tests for server-rendered SEO pages: drug dictionary and anesthesia protocols.

These pages give every drug and every species' anesthesia routines a crawlable
URL with structured data, breadcrumbs and internal cross-links — turning the
clinical database into a long-tail SEO asset.
"""

import os

os.environ.setdefault("SECRET_KEY", "test-secret-key")
os.environ.setdefault("FLASK_DEBUG", "1")

import pytest

from api.vetdict_api import app as flask_app


@pytest.fixture()
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as c:
        yield c


# ---------------------------------------------------------------------------
# Drug dictionary pages
# ---------------------------------------------------------------------------


class TestDrugsHub:
    def test_hub_returns_200(self, client):
        resp = client.get("/drugs")
        assert resp.status_code == 200
        assert "text/html" in resp.content_type

    def test_hub_has_canonical_and_meta(self, client):
        body = client.get("/drugs").data.decode()
        assert 'rel="canonical" href="https://vetdict.info/drugs"' in body
        assert 'name="description"' in body
        assert "動物用医薬品辞典" in body

    def test_hub_links_to_drug_detail(self, client):
        body = client.get("/drugs").data.decode()
        assert "/drugs/amoxicillin" in body

    def test_hub_links_to_sibling_databases(self, client):
        body = client.get("/drugs").data.decode()
        assert "/diseases" in body
        assert "/anesthesia" in body


class TestDrugDetail:
    def test_known_drug_returns_200(self, client):
        resp = client.get("/drugs/amoxicillin")
        assert resp.status_code == 200

    def test_detail_has_structured_data(self, client):
        body = client.get("/drugs/amoxicillin").data.decode()
        assert "application/ld+json" in body
        assert '"@type": "Drug"' in body
        assert '"@type": "BreadcrumbList"' in body

    def test_detail_has_canonical(self, client):
        body = client.get("/drugs/amoxicillin").data.decode()
        assert 'rel="canonical" href="https://vetdict.info/drugs/amoxicillin"' in body

    def test_detail_shows_dosing_and_mechanism(self, client):
        body = client.get("/drugs/amoxicillin").data.decode()
        assert "アモキシシリン" in body
        assert "作用機序" in body
        assert "投与量" in body

    def test_detail_cross_links_to_diseases(self, client):
        body = client.get("/drugs/amoxicillin").data.decode()
        assert "/diseases/" in body

    def test_unknown_drug_returns_404(self, client):
        resp = client.get("/drugs/this_drug_does_not_exist_xyz")
        assert resp.status_code == 404

    def test_every_drug_id_renders(self, client):
        """Spot-check a sample of drug ids to ensure no template errors."""
        from api.drug_dictionary import DRUGS

        sample = [d["id"] for d in DRUGS if d.get("id")][:40]
        assert sample
        for did in sample:
            resp = client.get(f"/drugs/{did}")
            assert resp.status_code == 200, f"/drugs/{did} returned {resp.status_code}"


# ---------------------------------------------------------------------------
# Anesthesia protocol pages
# ---------------------------------------------------------------------------


class TestAnesthesiaHub:
    def test_hub_returns_200(self, client):
        resp = client.get("/anesthesia")
        assert resp.status_code == 200

    def test_hub_has_canonical_and_meta(self, client):
        body = client.get("/anesthesia").data.decode()
        assert 'rel="canonical" href="https://vetdict.info/anesthesia"' in body
        assert "鎮静・麻酔プロトコル" in body

    def test_hub_links_to_all_species(self, client):
        from api.anesthesia_protocols import ANESTHESIA_PROTOCOLS

        body = client.get("/anesthesia").data.decode()
        for sp in ANESTHESIA_PROTOCOLS:
            assert f"/anesthesia/{sp}" in body


class TestAnesthesiaDetail:
    def test_known_species_returns_200(self, client):
        resp = client.get("/anesthesia/dog")
        assert resp.status_code == 200

    def test_detail_has_structured_data(self, client):
        body = client.get("/anesthesia/dog").data.decode()
        assert '"@type": "MedicalProcedure"' in body
        assert '"@type": "BreadcrumbList"' in body

    def test_detail_has_canonical(self, client):
        body = client.get("/anesthesia/cat").data.decode()
        assert 'rel="canonical" href="https://vetdict.info/anesthesia/cat"' in body

    def test_detail_renders_protocols(self, client):
        body = client.get("/anesthesia/dog").data.decode()
        # drug dosing table headers present
        assert "用量" in body
        assert "経路" in body

    def test_detail_cross_links_to_species_diseases(self, client):
        body = client.get("/anesthesia/dog").data.decode()
        assert "/diseases/dog" in body

    def test_unknown_species_returns_404(self, client):
        resp = client.get("/anesthesia/not_a_species")
        assert resp.status_code == 404

    def test_every_species_renders(self, client):
        from api.anesthesia_protocols import ANESTHESIA_PROTOCOLS

        for sp in ANESTHESIA_PROTOCOLS:
            resp = client.get(f"/anesthesia/{sp}")
            assert resp.status_code == 200, f"/anesthesia/{sp} returned {resp.status_code}"


# ---------------------------------------------------------------------------
# Sitemap integration
# ---------------------------------------------------------------------------


class TestSitemapIncludesNewPages:
    def test_sitemap_has_drug_hub_and_details(self, client):
        body = client.get("/sitemap.xml").data.decode()
        assert "<loc>https://vetdict.info/drugs</loc>" in body
        assert "https://vetdict.info/drugs/amoxicillin" in body

    def test_sitemap_has_anesthesia_pages(self, client):
        body = client.get("/sitemap.xml").data.decode()
        assert "<loc>https://vetdict.info/anesthesia</loc>" in body
        assert "https://vetdict.info/anesthesia/dog" in body

    def test_sitemap_drug_count_matches(self, client):
        from api.drug_dictionary import DRUGS

        body = client.get("/sitemap.xml").data.decode()
        expected = sum(1 for d in DRUGS if d.get("id"))
        actual = body.count("https://vetdict.info/drugs/")
        # Each drug appears once as a detail URL (hub is /drugs, not /drugs/)
        assert actual == expected


# ---------------------------------------------------------------------------
# Disease pages cross-link to drug pages
# ---------------------------------------------------------------------------


class TestDiseaseToDrugCrossLinks:
    def test_disease_mentioning_drug_links_to_drug_page(self, client):
        # Cold agglutinin disease (dog) mentions prednisolone/azathioprine
        resp = client.get("/diseases/dog/cold-agglutinin-disease")
        if resp.status_code != 200:
            pytest.skip("disease slug not present in this build")
        body = resp.data.decode()
        assert "/drugs/" in body


# ---------------------------------------------------------------------------
# Symptom reverse-lookup pages (disease <-> symptom internal-link graph)
# ---------------------------------------------------------------------------


class TestSymptomsHub:
    def test_hub_returns_200(self, client):
        resp = client.get("/symptoms")
        assert resp.status_code == 200

    def test_hub_canonical_and_links(self, client):
        body = client.get("/symptoms").data.decode()
        assert 'rel="canonical" href="https://vetdict.info/symptoms"' in body
        assert "/symptoms/dog" in body
        assert "/symptoms/horse" in body


class TestSymptomsIndex:
    def test_known_species_returns_200(self, client):
        resp = client.get("/symptoms/dog")
        assert resp.status_code == 200

    def test_index_links_to_symptom_detail(self, client):
        import re

        body = client.get("/symptoms/cat").data.decode()
        assert re.search(r"/symptoms/cat/[a-z0-9_]+", body)

    def test_horse_index_uses_health_check_items(self, client):
        # Equine has no SYMPTOM_NAMES; it must fall back to HEALTH_CHECK_ITEMS
        resp = client.get("/symptoms/horse")
        assert resp.status_code == 200
        assert "/symptoms/horse/" in resp.data.decode()

    def test_unknown_species_404(self, client):
        assert client.get("/symptoms/not_a_species").status_code == 404


class TestSymptomDetail:
    def test_known_symptom_returns_200(self, client):
        resp = client.get("/symptoms/dog/lethargy")
        assert resp.status_code == 200

    def test_detail_structured_data_and_breadcrumb(self, client):
        body = client.get("/symptoms/dog/lethargy").data.decode()
        assert '"@type": "MedicalSignOrSymptom"' in body
        assert '"@type": "BreadcrumbList"' in body
        assert 'rel="canonical" href="https://vetdict.info/symptoms/dog/lethargy"' in body

    def test_detail_links_to_disease_pages(self, client):
        body = client.get("/symptoms/dog/lethargy").data.decode()
        assert "/diseases/dog/" in body

    def test_unknown_symptom_404(self, client):
        assert client.get("/symptoms/dog/not_a_real_symptom_xyz").status_code == 404

    def test_every_species_symptom_index_renders(self, client):
        from api.disease_store import SPECIES_META
        from api.vetdict_api import _DISEASE_MODULES

        for sp in _DISEASE_MODULES:
            if sp not in SPECIES_META:
                continue
            resp = client.get(f"/symptoms/{sp}")
            assert resp.status_code == 200, f"/symptoms/{sp} -> {resp.status_code}"


class TestSymptomSitemapAndLinks:
    def test_sitemap_has_symptom_pages(self, client):
        body = client.get("/sitemap.xml").data.decode()
        assert "<loc>https://vetdict.info/symptoms</loc>" in body
        assert "https://vetdict.info/symptoms/dog<" in body
        assert "https://vetdict.info/symptoms/dog/" in body

    def test_disease_detail_symptom_tags_link_to_symptom_pages(self, client):
        import re

        idx = client.get("/diseases/dog").data.decode()
        m = re.search(r"/diseases/dog/([a-z0-9-]+)\"", idx)
        assert m
        body = client.get(f"/diseases/dog/{m.group(1)}").data.decode()
        assert re.search(r"/symptoms/dog/[a-z0-9_]+", body)

    def test_horse_disease_detail_shows_symptoms(self, client):
        # Regression: equine pages previously had no symptom section
        import re

        idx = client.get("/diseases/horse").data.decode()
        m = re.search(r"/diseases/horse/([a-z0-9-]+)\"", idx)
        assert m
        body = client.get(f"/diseases/horse/{m.group(1)}").data.decode()
        assert "/symptoms/horse/" in body


# ---------------------------------------------------------------------------
# Anesthesia protocol tables link each drug to its drug page
# ---------------------------------------------------------------------------


class TestAnesthesiaDrugLinks:
    def test_protocol_drugs_link_to_drug_pages(self, client):
        import re

        body = client.get("/anesthesia/dog").data.decode()
        links = re.findall(r"/drugs/([a-z0-9_-]+)\"", body)
        assert links, "anesthesia protocol drugs are not linked"
        # linked drug ids must resolve
        for did in sorted(set(links))[:6]:
            assert client.get(f"/drugs/{did}").status_code == 200

    def test_combination_components_are_split_and_linked(self, client):
        from api.vetdict_api import _anes_drug_segments

        segs = _anes_drug_segments("Dexmedetomidine + Butorphanol + Midazolam")
        linked = [s for s in segs if s["id"]]
        # all three common anesthetics should resolve to drug ids
        assert len(linked) >= 3
