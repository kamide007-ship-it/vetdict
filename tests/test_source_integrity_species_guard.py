"""T108 — species guards for auto-attached citations and drug links.

Before this fix, two request-time keyword matchers attached references and
drugs to a disease purely by name/text substring match, with no species guard:

* ``get_references_for_disease`` attached dog/cat-oriented PubMed citations to
  exotic-species pages (e.g. the dogs-and-cats diabetes paper on a degu page).
* ``mentioned_drugs`` / ``_attach_mentioned_drugs`` linked drugs that had no
  dosing data for the species, presenting a drug with no species-appropriate
  dose — a clinical-safety hazard.

These tests lock in the guarded behaviour.
"""

from api.pubmed_references import get_references_for_disease


class TestCitationSpeciesGuard:
    def test_dogcat_citation_not_leaked_to_exotic(self):
        # The "diabetes mellitus" citation is dogs-and-cats literature.
        assert get_references_for_disease("Diabetes Mellitus", "degu") == []
        assert get_references_for_disease("Diabetes Mellitus", "hamster") == []

    def test_dogcat_citation_kept_for_dogcat(self):
        assert len(get_references_for_disease("Diabetes Mellitus", "cat")) >= 1
        assert len(get_references_for_disease("Diabetes Mellitus", "dog")) >= 1

    def test_exotic_citation_kept_for_correct_exotic(self):
        # Malocclusion refs are exotic-herbivore dental literature.
        assert len(get_references_for_disease("Malocclusion", "degu")) >= 1
        assert len(get_references_for_disease("Malocclusion", "chinchilla")) >= 1
        # ...and not offered to a cat (the cited studies are not feline).
        assert get_references_for_disease("Malocclusion", "cat") == []

    def test_gi_stasis_scoped_to_herbivores(self):
        assert len(get_references_for_disease("Gastrointestinal Stasis", "rabbit")) >= 1
        assert get_references_for_disease("Gastrointestinal Stasis", "dog") == []

    def test_ferret_scoped_citations(self):
        assert len(get_references_for_disease("Insulinoma", "ferret")) >= 1
        assert get_references_for_disease("Insulinoma", "dog") == []

    def test_no_species_preserves_legacy_behaviour(self):
        # Backward compatibility: species=None keeps the unguarded match.
        assert len(get_references_for_disease("Diabetes Mellitus")) >= 1


class TestDrugLinkSpeciesGuard:
    def _pick_drug_with_dog_but_not(self, drugs, missing_species):
        for d in drugs:
            si = d.get("species_info") or {}
            if "dog" in si and missing_species not in si and len(d.get("name", "")) >= 4:
                return d
        return None

    def test_drug_without_species_dosing_is_suppressed(self):
        from api.drug_dictionary import DRUGS
        from api.vetdict_api import _attach_mentioned_drugs

        drug = self._pick_drug_with_dog_but_not(DRUGS, "degu")
        assert drug is not None, "fixture drug (dog dosing, no degu dosing) not found"

        text = f"Treatment: administer {drug['name']} as indicated"
        # Exotic species without dosing -> drug link suppressed.
        res = {"suspected_diseases": [{"name": "T", "treatment": text, "treatment_ja": ""}]}
        _attach_mentioned_drugs(res, "degu")
        names = [x["name"] for x in res["suspected_diseases"][0].get("mentioned_drugs", [])]
        assert drug["name"] not in names

        # Dog (has dosing) -> drug link kept, with a species-specific dose.
        res2 = {"suspected_diseases": [{"name": "T", "treatment": text, "treatment_ja": ""}]}
        _attach_mentioned_drugs(res2, "dog")
        kept = res2["suspected_diseases"][0].get("mentioned_drugs", [])
        match = [x for x in kept if x["name"] == drug["name"]]
        assert match and match[0].get("dosage"), "dog drug link should carry a dose"

    def test_drug_with_species_dosing_is_kept(self):
        from api.drug_dictionary import DRUGS
        from api.vetdict_api import _attach_mentioned_drugs

        # A drug that DOES have degu dosing must still be surfaced on degu.
        drug = next(
            (d for d in DRUGS if "degu" in (d.get("species_info") or {}) and len(d.get("name", "")) >= 4),
            None,
        )
        assert drug is not None, "no drug with degu dosing found"
        text = f"Give {drug['name']} per protocol"
        res = {"suspected_diseases": [{"name": "T", "treatment": text, "treatment_ja": ""}]}
        _attach_mentioned_drugs(res, "degu")
        names = [x["name"] for x in res["suspected_diseases"][0].get("mentioned_drugs", [])]
        assert drug["name"] in names
