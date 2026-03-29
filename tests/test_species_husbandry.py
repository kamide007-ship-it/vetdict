"""Tests for species husbandry / care environment data."""

from api.species_husbandry import HUSBANDRY_DATA

# Required fields for every species entry
_REQUIRED_FIELDS = {"name", "name_ja", "temperature", "humidity", "housing", "diet", "enrichment", "socialization", "notes"}

# Each text field must have both en and ja keys
_BILINGUAL_FIELDS = {"temperature", "humidity", "housing", "diet", "enrichment", "socialization", "notes"}

# All 21 species from CLAUDE.md
_EXPECTED_SPECIES = {
    "dog", "cat", "horse", "rabbit", "hamster", "guinea_pig", "chinchilla",
    "ferret", "hedgehog", "sugar_glider", "degu", "bird", "parakeet", "parrot",
    "reptile", "tortoise", "snake", "lizard", "amphibian", "fish", "exotic_other",
}


class TestHusbandryDataStructure:
    def test_all_21_species_present(self):
        assert set(HUSBANDRY_DATA.keys()) == _EXPECTED_SPECIES

    def test_species_count(self):
        assert len(HUSBANDRY_DATA) == 21

    def test_required_fields_present(self):
        for species, data in HUSBANDRY_DATA.items():
            missing = _REQUIRED_FIELDS - set(data.keys())
            assert not missing, f"{species}: missing fields {missing}"

    def test_bilingual_content(self):
        for species, data in HUSBANDRY_DATA.items():
            for field in _BILINGUAL_FIELDS:
                val = data[field]
                assert isinstance(val, dict), f"{species}/{field}: expected dict"
                assert "en" in val, f"{species}/{field}: missing 'en'"
                assert "ja" in val, f"{species}/{field}: missing 'ja'"
                assert val["en"].strip(), f"{species}/{field}/en: empty"
                assert val["ja"].strip(), f"{species}/{field}/ja: empty"

    def test_name_fields_nonempty(self):
        for species, data in HUSBANDRY_DATA.items():
            assert data["name"].strip(), f"{species}: empty name"
            assert data["name_ja"].strip(), f"{species}: empty name_ja"

    def test_subtypes_structure(self):
        """Species with subtypes must have well-formed subtype entries."""
        for species, data in HUSBANDRY_DATA.items():
            if "subtypes" not in data:
                continue
            subtypes = data["subtypes"]
            assert isinstance(subtypes, list), f"{species}: subtypes not a list"
            assert len(subtypes) >= 1, f"{species}: empty subtypes"
            for i, sub in enumerate(subtypes):
                assert "name" in sub, f"{species}/subtype[{i}]: missing name"
                assert "name_ja" in sub, f"{species}/subtype[{i}]: missing name_ja"

    def test_dog_has_subtypes(self):
        assert "subtypes" in HUSBANDRY_DATA["dog"]
        assert len(HUSBANDRY_DATA["dog"]["subtypes"]) >= 2

    def test_lizard_has_subtypes(self):
        assert "subtypes" in HUSBANDRY_DATA["lizard"]

    def test_japanese_names_are_japanese(self):
        """Spot-check that name_ja contains Japanese characters."""
        for species in ["dog", "cat", "rabbit", "fish"]:
            name_ja = HUSBANDRY_DATA[species]["name_ja"]
            has_cjk = any("\u3000" <= c <= "\u9fff" or "\u30a0" <= c <= "\u30ff" for c in name_ja)
            assert has_cjk, f"{species}: name_ja '{name_ja}' doesn't contain Japanese"
