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


class TestPrevalenceKeysResolveToDiseases:
    """Prevalence keys are matched to diseases by exact English name in both the
    diagnostic prior (disease_matcher) and the /common-diseases endpoint. A key
    that matches no real disease is inert: it never adjusts a diagnostic score and
    it renders a chip with an empty Japanese label that only fuzzy-resolves on
    click. These tests guard the linkage.
    """

    @staticmethod
    def _disease_names(species):
        from api.chat.species_data import get_species_data

        data = get_species_data(species) or {}
        return {d.get("name", "") for d in data.get("diseases", [])}

    def test_previously_dead_keys_now_resolve(self):
        # Keys repaired in the 2026-08 prevalence remap. Each MUST match a real
        # disease so the diagnostic prior activates and the chip gets a JA label.
        fixed = {
            "dog": ["Xylitol Poisoning"],
            "cat": ["Pulmonary Edema"],
            "rabbit": ["Heatstroke (Neurological)"],
            "bird": [
                "Knemidocoptes (Scaly Face/Leg Mites)",
                "Trichomoniasis",
                "Crop Burns",
                "Zinc Toxicosis",
            ],
            "reptile": ["Bacterial Dermatitis", "Nematode Infection"],
            "hamster": ["Incisor Malocclusion", "Barbering", "Ear Infection (Otitis)"],
            "guinea_pig": ["Bloat (Gastric Dilation)", "Pedal Abscess"],
            "amphibian": ["Saprolegniasis", "Ammonia Toxicosis"],
            "chinchilla": ["Diabetes Mellitus - Chinchilla", "Conjunctivitis - Chinchilla"],
            "snake": ["Retained Spectacle (Retained Eye Cap)"],
            "tortoise": ["Shell Fracture / Trauma"],
        }
        for species, keys in fixed.items():
            names = self._disease_names(species)
            prev = SPECIES_PREVALENCE.get(species, {})
            for key in keys:
                assert key in prev, f"{species}: expected prevalence key {key!r} missing"
                assert key in names, (
                    f"{species}: prevalence key {key!r} matches no disease name"
                )

    def test_removed_duplicate_keys_stay_removed(self):
        # These dead keys duplicated an already-active canonical entry and were
        # removed. They must not reappear (they would render broken duplicate chips).
        removed = {
            "dog": "Immune-Mediated Hemolytic Anemia (IMHA)",
            "rabbit": "Snuffles (Bordetella)",
            "bird": "Psittacosis / Chlamydiosis",
            "guinea_pig": "Ovarian Cystic Disease",
            "chinchilla": "Penile Fur Ring",
        }
        for species, key in removed.items():
            assert key not in SPECIES_PREVALENCE.get(species, {}), (
                f"{species}: removed duplicate prevalence key {key!r} reappeared"
            )

    def test_dead_key_count_stays_capped(self):
        # Regression guard: the vast majority of prevalence keys must resolve to a
        # real disease. A handful remain for conditions genuinely absent from a
        # species' DB (e.g. aquarium diseases under exotic_other). Keep it small so
        # future edits don't silently reintroduce inert keys.
        dead = 0
        for species, diseases in SPECIES_PREVALENCE.items():
            names = self._disease_names(species)
            dead += sum(1 for k in diseases if k not in names)
        assert dead <= 40, f"{dead} prevalence keys resolve to no disease (cap 40)"
