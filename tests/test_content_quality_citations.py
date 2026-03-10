from api.content_quality import REFERENCE_CATALOG, enrich_disease_content
from api.vetdict_api import app


def test_enrich_disease_content_adds_canonical_sections_and_citations():
    enriched = enrich_disease_content(
        {
            "name": "Test Disease",
            "name_ja": "テスト疾患",
            "description": "desc",
            "symptoms": ["vomiting", "lethargy"],
        },
        "cat",
    )
    assert "sections" in enriched
    for key in ["pathophysiology", "prevention", "treatment", "etiology", "prognosis"]:
        assert key in enriched["sections"]
        assert enriched["sections"][key]["text"]
        assert enriched["sections"][key]["citations"]

    cids = enriched["sections"]["pathophysiology"]["citations"]
    assert all(isinstance(cid, int) for cid in cids)
    assert all(cid in REFERENCE_CATALOG for cid in cids)


def test_api_analyze_symptoms_includes_section_citations():
    client = app.test_client()
    resp = client.post(
        "/api/analyze-symptoms",
        json={"species": "cat", "symptoms": ["vomiting", "lethargy"]},
    )
    assert resp.status_code == 200
    payload = resp.get_json()
    diseases = payload.get("suspected_diseases") or payload.get("possible_conditions")
    assert diseases
    sample = diseases[0]
    assert "sections" in sample
    assert "reference_catalog_version" in sample
    assert isinstance(sample.get("reference_catalog"), list)
    assert sample["sections"]["treatment"]["citations"]
