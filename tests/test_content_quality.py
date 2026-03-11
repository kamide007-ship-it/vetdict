from api.content_quality import enrich_disease_content


def test_enrich_disease_content_adds_landing_references_for_species():
    disease = {
        "name": "Feline Asthma",
        "name_ja": "猫喘息",
        "symptoms": ["coughing", "wheezing"],
    }

    enriched = enrich_disease_content(disease, "cat")

    assert 7 in enriched["reference_numbers"]
    assert 8 in enriched["reference_numbers"]
    assert any(src["id"] == "ref-7" for src in enriched["evidence_sources"])
    assert "description" in enriched["citation_map"]
    assert all(v.startswith("ref-") for vals in enriched["citation_map"].values() for v in vals)


def test_enrich_disease_content_keeps_custom_reference_numbers():
    disease = {
        "name": "Custom Disease",
        "symptoms": ["lethargy"],
        "reference_numbers": [59],
    }

    enriched = enrich_disease_content(disease, "horse")

    assert 59 in enriched["reference_numbers"]
    assert any(src.get("number") == "59" for src in enriched["evidence_sources"])
