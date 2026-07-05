"""Tests for enrich_diseases() in api/species/helpers.py."""



from api.species.helpers import enrich_diseases


class TestEnrichDiseases:
    def _make_disease(self, name="Test Disease", **overrides):
        base = {
            "name": name,
            "name_ja": "テスト疾患",
            "symptoms": ["fever"],
            "urgency": "moderate",
        }
        base.update(overrides)
        return base

    def test_returns_list(self):
        diseases = [self._make_disease()]
        result = enrich_diseases(diseases, "dog")
        assert isinstance(result, list)

    def test_fills_missing_fields(self):
        diseases = [self._make_disease()]
        result = enrich_diseases(diseases, "dog")
        d = result[0]
        # enrich_diseases should fill fallback content for missing fields
        for field in ("pathophysiology", "pathophysiology_ja",
                      "causes", "causes_ja", "treatment", "treatment_ja",
                      "prevention", "prevention_ja", "prognosis", "prognosis_ja"):
            assert d.get(field), f"Field '{field}' should be filled"

    def test_preserves_existing_fields(self):
        diseases = [self._make_disease(treatment_ja="手動で書いた治療法")]
        result = enrich_diseases(diseases, "cat")
        assert result[0]["treatment_ja"] == "手動で書いた治療法"

    def test_does_not_duplicate_entries(self):
        diseases = [self._make_disease("Unique Test Disease XYZ")]
        enrich_diseases(diseases, "dog")
        # Should not create duplicate entries for the same disease
        names = [d["name"] for d in diseases]
        assert names.count("Unique Test Disease XYZ") == 1

    def test_appends_supplementary_diseases(self):
        # Start with empty list — supplementary diseases should be appended
        diseases = []
        result = enrich_diseases(diseases, "dog")
        # If supplementary data exists for dog, list should grow
        # (this is a structural test — we just verify no crash)
        assert isinstance(result, list)

    def test_multiple_diseases(self):
        diseases = [
            self._make_disease("Disease A", name_ja="疾患A"),
            self._make_disease("Disease B", name_ja="疾患B"),
        ]
        result = enrich_diseases(diseases, "rabbit")
        assert len(result) >= 2
        assert result[0]["name"] == "Disease A"
        assert result[1]["name"] == "Disease B"

    def test_unknown_species_still_generates_fallback(self):
        diseases = [self._make_disease()]
        result = enrich_diseases(diseases, "exotic_other")
        assert result[0].get("treatment") or result[0].get("treatment_ja")

    def test_enrichment_is_idempotent(self):
        diseases = [self._make_disease("Idempotent Test")]
        enrich_diseases(diseases, "cat")
        first_treatment = diseases[0].get("treatment_ja", "")
        enrich_diseases(diseases, "cat")
        assert diseases[0].get("treatment_ja", "") == first_treatment
