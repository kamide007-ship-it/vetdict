"""Tests for api/species/prevalence_data.py — Species prevalence tiers."""


from api.species.prevalence_data import SPECIES_PREVALENCE

VALID_TIERS = {"very_common", "common", "uncommon", "rare"}


class TestPrevalenceStructure:
    def test_prevalence_is_nonempty_dict(self):
        assert isinstance(SPECIES_PREVALENCE, dict)
        assert len(SPECIES_PREVALENCE) >= 15

    def test_all_tiers_are_valid(self):
        for species, diseases in SPECIES_PREVALENCE.items():
            for disease_name, tier in diseases.items():
                assert tier in VALID_TIERS, (
                    f"{species}/{disease_name}: invalid tier '{tier}'"
                )

    def test_each_species_has_entries(self):
        for species, diseases in SPECIES_PREVALENCE.items():
            assert len(diseases) >= 5, (
                f"{species} has only {len(diseases)} entries"
            )

    def test_total_entries_above_1000(self):
        total = sum(len(d) for d in SPECIES_PREVALENCE.values())
        assert total >= 1000, f"Only {total} total entries"


class TestKeySpecies:
    def test_dog_has_common_diseases(self):
        dog = SPECIES_PREVALENCE.get("dog", {})
        assert any("Otitis" in k for k in dog), "Dog should have otitis"
        assert any("Periodontal" in k for k in dog), "Dog should have periodontal"

    def test_cat_has_common_diseases(self):
        cat = SPECIES_PREVALENCE.get("cat", {})
        assert any("FIV" in k or "fiv" in k.lower() for k in cat), "Cat should have FIV"

    def test_fish_has_entries(self):
        fish = SPECIES_PREVALENCE.get("fish", {})
        assert len(fish) >= 5, "Fish should have prevalence data"

    def test_rabbit_has_entries(self):
        rabbit = SPECIES_PREVALENCE.get("rabbit", {})
        assert len(rabbit) >= 10

    def test_reptile_has_entries(self):
        reptile = SPECIES_PREVALENCE.get("reptile", {})
        assert len(reptile) >= 10


class TestTierDistribution:
    def test_each_species_has_very_common(self):
        for species, diseases in SPECIES_PREVALENCE.items():
            tiers = set(diseases.values())
            assert "very_common" in tiers, (
                f"{species} has no very_common diseases"
            )

    def test_disease_names_are_nonempty_strings(self):
        for species, diseases in SPECIES_PREVALENCE.items():
            for name in diseases:
                assert isinstance(name, str) and len(name) > 0, (
                    f"{species}: empty disease name"
                )
