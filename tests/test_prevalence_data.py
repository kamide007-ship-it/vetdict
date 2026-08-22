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
                assert tier in VALID_TIERS, f"{species}/{disease_name}: invalid tier '{tier}'"

    def test_each_species_has_entries(self):
        for species, diseases in SPECIES_PREVALENCE.items():
            assert len(diseases) >= 5, f"{species} has only {len(diseases)} entries"

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
            assert "very_common" in tiers, f"{species} has no very_common diseases"

    def test_disease_names_are_nonempty_strings(self):
        for species, diseases in SPECIES_PREVALENCE.items():
            for name in diseases:
                assert isinstance(name, str) and len(name) > 0, f"{species}: empty disease name"


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
            # Ammonia Poisoning: the 2026-08 duplicate-card merge kept the
            # "Ammonia Poisoning" spelling and the key follows the survivor.
            "amphibian": ["Saprolegniasis", "Ammonia Poisoning"],
            "chinchilla": ["Diabetes Mellitus - Chinchilla", "Conjunctivitis - Chinchilla"],
            "snake": ["Retained Spectacle (Retained Eye Cap)"],
            "tortoise": ["Shell Fracture / Trauma"],
        }
        # Second remap (2026-08): renames to canonical names, plus new disease
        # entries added for previously-inert common-tier keys.
        fixed_round2 = {
            "chinchilla": ["Tooth Root Abscess", "Prolapsed Rectum"],
            "guinea_pig": [
                "Adenovirus Pneumonia",
                "Intestinal Torsion",  # new disease entry
            ],
            "bird": ["Cloacal Papillomatosis", "Renal Failure (Acute / Chronic)"],
            "amphibian": ["Renal Failure", "Parasitic Dermatitis"],  # latter is a new entry
            "reptile": ["Dermal Mycosis (Non-CANV Fungal Dermatitis)"],
            "degu": ["Elodontoma (Dental Tumor)"],  # new disease entry
            "exotic_other": [
                "Dermatological Bacterial Infection",
                # Survivor of the 2026-08 duplicate-card merge.
                "Heat Stress / Heat Stroke",
                "Mite Infestation (Tarantula)",
                "Fracture (Limb)",
                "Trauma / Wound Infection (Exotic)",
            ],
            "fish": ["Fin Rot (Bacterial/Fungal)"],
        }
        # Third remap (2026-08): keys renamed to the canonical duplicate-merge
        # survivor names so they resolve exactly in the served DB (chips) as well
        # as in the module data (chat prior).
        fixed_round3 = {
            "bird": ["Vitamin A Deficiency (Hypovitaminosis A)"],
            "guinea_pig": ["Abscess (Subcutaneous)", "Gastric Ulcers"],
            "parakeet": [
                "Copper Poisoning",
                "Egg Yolk Peritonitis",
                "Renal Adenocarcinoma",
            ],
            "tortoise": ["Bladder Stones (Urolithiasis)"],
            "degu": ["Uterine Adenocarcinoma"],
        }
        for species, keys in fixed_round2.items():
            fixed.setdefault(species, []).extend(keys)
        for species, keys in fixed_round3.items():
            fixed.setdefault(species, []).extend(keys)
        for species, keys in fixed.items():
            names = self._disease_names(species)
            prev = SPECIES_PREVALENCE.get(species, {})
            for key in keys:
                assert key in prev, f"{species}: expected prevalence key {key!r} missing"
                assert key in names, f"{species}: prevalence key {key!r} matches no disease name"

    def test_removed_duplicate_keys_stay_removed(self):
        # These dead keys duplicated an already-active canonical entry and were
        # removed. They must not reappear (they would render broken duplicate chips).
        removed = {
            "dog": ["Immune-Mediated Hemolytic Anemia (IMHA)"],
            "rabbit": [
                "Snuffles (Bordetella)",
                # Symptom-level key; acute rabbit diarrhea is covered by the active
                # Enterotoxemia / dysbiosis / coccidiosis entries.
                "Diarrhea (Acute)",
            ],
            "bird": ["Psittacosis / Chlamydiosis"],
            "guinea_pig": ["Ovarian Cystic Disease"],
            "chinchilla": [
                "Penile Fur Ring",
                "Fatty Liver Disease",  # duplicate of active "Hepatic Lipidosis"
            ],
            "degu": ["Heatstroke"],  # duplicate of active "Heat Stroke"
            "exotic_other": [
                # Duplicate of active "Intestinal Parasitism"
                "Gastrointestinal Parasites",
                # Aquarium fish diseases live under the dedicated fish species,
                # where each has an active canonical prevalence key.
                "Ich (White Spot Disease)",
                "Fin Rot",
                "Swim Bladder Disease",
                "Koi Herpesvirus Disease (KHV)",
            ],
        }
        for species, keys in removed.items():
            for key in keys:
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
            if species == "horse":
                # Horse is served by the dedicated equine engine, not the generic
                # chat species data — validated separately in TestHorsePrevalence.
                continue
            names = self._disease_names(species)
            dead += sum(1 for k in diseases if k not in names)
        assert dead <= 15, f"{dead} prevalence keys resolve to no disease (cap 15)"


class TestHorsePrevalence:
    """Horse was the only species with no base prevalence data: the
    common-diseases chips rendered empty and the diagnostic prior was inert for
    the platform developer's own species. These tests guard the curated equine
    tier set added 2026-08 (Reed & Bayly 4th ed; NAHMS Equine 2015; Sykes 2015
    ECEIM EGUS consensus; Wylie 2011; McIlwraith 2012)."""

    @staticmethod
    def _horse_names():
        from api.species.equine_diseases import DISEASE_DATABASE

        vals = DISEASE_DATABASE.values() if isinstance(DISEASE_DATABASE, dict) else DISEASE_DATABASE
        return {d.name_en for d in vals}

    def test_horse_has_base_prevalence(self):
        horse = SPECIES_PREVALENCE.get("horse", {})
        assert len(horse) >= 40, "horse base prevalence set went missing"
        assert horse.get("Colic") == "very_common"
        assert horse.get("Gastric Ulcers (EGUS)") == "very_common"
        assert horse.get("Laminitis") == "common"

    def test_all_horse_keys_resolve_to_equine_db_names(self):
        names = self._horse_names()
        horse = SPECIES_PREVALENCE.get("horse", {})
        dead = [k for k in horse if k not in names]
        assert not dead, f"horse prevalence keys match no equine disease: {dead}"

    def test_horse_regional_adjustment_keys_resolve(self):
        from api.species.prevalence_data import (
            INTERNATIONAL_REGIONAL_ADJUSTMENTS,
            JAPAN_REGIONAL_ADJUSTMENTS,
        )

        names = self._horse_names()
        for label, adj in (
            ("jp", JAPAN_REGIONAL_ADJUSTMENTS),
            ("intl", INTERNATIONAL_REGIONAL_ADJUSTMENTS),
        ):
            dead = [k for k in adj.get("horse", {}) if k not in names]
            assert not dead, f"{label} horse regional keys match no disease: {dead}"


class TestRegionalAdjustmentKeysResolve:
    """Regional overrides merge into the base map by exact disease name; a key
    that matches no disease silently never overrides anything. All JP/INTL
    adjustment keys (fixed 2026-08: FIP wet/dry split, Pasteurellosis
    (Snuffles), Gastrointestinal Stasis, KHV/Ich canonical fish names, etc.)
    must resolve."""

    def test_all_regional_keys_resolve(self):
        from api.chat.species_data import get_species_data
        from api.species.prevalence_data import (
            INTERNATIONAL_REGIONAL_ADJUSTMENTS,
            JAPAN_REGIONAL_ADJUSTMENTS,
        )

        for label, adj in (
            ("jp", JAPAN_REGIONAL_ADJUSTMENTS),
            ("intl", INTERNATIONAL_REGIONAL_ADJUSTMENTS),
        ):
            for species, overrides in adj.items():
                if species == "horse":
                    continue  # covered by TestHorsePrevalence
                data = get_species_data(species) or {}
                names = {d.get("name", "") for d in data.get("diseases", [])}
                if not names:
                    continue
                dead = [k for k in overrides if k not in names]
                assert not dead, f"{label}/{species}: regional keys match no disease: {dead}"
