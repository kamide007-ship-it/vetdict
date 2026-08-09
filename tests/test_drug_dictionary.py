"""Tests for api/drug_dictionary.py

Covers:
- DRUG_CATEGORIES structure and expected keys
- DRUGS list data structure validation
- search_drugs() with various queries and filters
- get_drugs_by_category() for valid and invalid categories
- get_drugs_by_species() for dogs, cats, rabbits
- get_drug_by_id() for existing and non-existent drugs
- Flask Blueprint route endpoints via test client
"""

import sys
from pathlib import Path

import pytest
from flask import Flask

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from api.drug_dictionary import (
    DRUG_CATEGORIES,
    DRUGS,
    drug_bp,
    get_drug_by_id,
    get_drugs_by_category,
    get_drugs_by_species,
    search_drugs,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def app():
    """Minimal Flask application with drug_bp registered."""
    flask_app = Flask(__name__)
    flask_app.config["TESTING"] = True
    flask_app.register_blueprint(drug_bp)
    return flask_app


@pytest.fixture(scope="module")
def client(app):
    return app.test_client()


# ---------------------------------------------------------------------------
# DRUG_CATEGORIES tests
# ---------------------------------------------------------------------------

EXPECTED_CATEGORY_KEYS = [
    "antibiotics",
    "antifungals",
    "antiparasitics",
    "nsaids",
    "analgesics",
    "anesthetics",
    "corticosteroids",
    "gi_drugs",
    "cardiovascular",
    "respiratory",
    "endocrine",
    "dermatological",
    "ophthalmic",
    "neurological",
    "urinary",
    "immunosuppressives",
    "antineoplastics",
    "supplements",
    "sedatives",
    "antiemetics",
    "antidiarrheals",
    "hepatoprotectants",
    "antihistamines",
    "bronchodilators",
    "diuretics",
    "ace_inhibitors",
    "antiarrhythmics",
    "muscle_relaxants",
    "hormones",
    "antiseptics",
]


def test_drug_categories_is_dict():
    assert isinstance(DRUG_CATEGORIES, dict)


def test_drug_categories_has_expected_keys():
    for key in EXPECTED_CATEGORY_KEYS:
        assert key in DRUG_CATEGORIES, f"Missing category key: {key}"


def test_drug_categories_entry_structure():
    for cat_id, names in DRUG_CATEGORIES.items():
        assert "ja" in names, f"Category '{cat_id}' missing 'ja'"
        assert "en" in names, f"Category '{cat_id}' missing 'en'"
        assert isinstance(names["ja"], str) and names["ja"], f"Category '{cat_id}' has empty 'ja'"
        assert isinstance(names["en"], str) and names["en"], f"Category '{cat_id}' has empty 'en'"


def test_drug_categories_antibiotics_values():
    assert DRUG_CATEGORIES["antibiotics"]["en"] == "Antibiotics"
    assert DRUG_CATEGORIES["antibiotics"]["ja"] == "抗菌薬・抗生物質"


def test_drug_categories_nsaids_values():
    assert DRUG_CATEGORIES["nsaids"]["en"] == "NSAIDs"


# ---------------------------------------------------------------------------
# DRUGS list / data structure tests
# ---------------------------------------------------------------------------


def test_drugs_is_non_empty_list():
    assert isinstance(DRUGS, list)
    assert len(DRUGS) > 0


REQUIRED_DRUG_FIELDS = {"id", "name", "name_ja", "category", "species_info"}


def test_every_drug_has_required_fields():
    for drug in DRUGS:
        for field in REQUIRED_DRUG_FIELDS:
            assert field in drug, f"Drug '{drug.get('id', '?')}' missing field '{field}'"


def test_every_drug_category_is_known():
    for drug in DRUGS:
        assert drug["category"] in DRUG_CATEGORIES, f"Drug '{drug['id']}' has unknown category '{drug['category']}'"


def test_drug_species_info_structure():
    """Each species entry must have dosing information ('dosage' or 'dose' key)."""
    for drug in DRUGS:
        for species, info in drug.get("species_info", {}).items():
            has_dosage = "dosage" in info or "dose" in info
            assert has_dosage, f"Drug '{drug['id']}' / species '{species}' missing 'dosage' or 'dose'"
            if "safe" in info:
                assert isinstance(info["safe"], bool), f"Drug '{drug['id']}' / species '{species}': 'safe' must be bool"


def test_amoxicillin_present_and_correct():
    drug = next((d for d in DRUGS if d["id"] == "amoxicillin"), None)
    assert drug is not None
    assert drug["name"] == "Amoxicillin"
    assert drug["category"] == "antibiotics"
    assert drug["species_info"]["dog"]["safe"] is True
    assert drug["species_info"]["rabbit"]["safe"] is False


def test_nondepolarizing_nmba_reversal_agent_is_documented():
    """A non-depolarizing NMBA (atracurium) points clinicians to neostigmine for
    reversal, so neostigmine must itself be a discoverable entry with dosing.
    Guards the gap where the manual referenced a drug it did not document."""
    atracurium = next((d for d in DRUGS if d["id"] == "atracurium"), None)
    assert atracurium is not None
    referenced = {i["drug"] for i in atracurium.get("drug_interactions", [])}
    assert "neostigmine" in referenced

    neostigmine = next((d for d in DRUGS if d["id"] == "neostigmine"), None)
    assert neostigmine is not None, "neostigmine reversal agent missing from drug manual"
    assert neostigmine["category"] in DRUG_CATEGORIES
    for species in ("dog", "cat"):
        info = neostigmine["species_info"][species]
        assert info["dosage"].strip()
        # Reversal must be paired with an anticholinergic to prevent muscarinic
        # bradycardia — the dose string should name one.
        assert "glycopyrrolate" in info["dosage"].lower() or "atropine" in info["dosage"].lower()


def test_aspirin_present_with_feline_dosing_caution():
    """Aspirin is a staple antiplatelet (feline ATE, canine hypercoagulability).
    Cats eliminate salicylate slowly, so the entry must not imply daily dosing."""
    aspirin = next((d for d in DRUGS if d["id"] == "aspirin"), None)
    assert aspirin is not None, "aspirin missing from drug manual"
    assert aspirin["category"] in DRUG_CATEGORIES
    cat = aspirin["species_info"]["cat"]
    assert cat["safe"] is True
    # Feline dosing must be intermittent (q48-72h), never daily.
    assert "q72h" in cat["dosage"].lower() or "q48" in cat["dosage"].lower()
    assert "q24h" not in cat["dosage"].lower()


def test_sglt2_inhibitors_present_with_edka_warning():
    """The cat Diabetes Mellitus entry recommends bexagliflozin (Bexacat) and
    velagliflozin (Senvelgo), so both SGLT2 inhibitors must be documented with
    dosing and the class-defining euglycemic-DKA / insulin-naive-only warnings.
    Guards the referenced-but-absent gap for this drug class."""
    for drug_id, dose_marker in (("bexagliflozin", "15 mg"), ("velagliflozin", "1 mg/kg")):
        entry = next((d for d in DRUGS if d["id"] == drug_id), None)
        assert entry is not None, f"{drug_id} missing from drug manual"
        assert entry["category"] in DRUG_CATEGORIES
        cat = entry["species_info"]["cat"]
        assert cat["safe"] is True
        assert dose_marker in cat["dosage"]
        # Insulin-naive restriction must be stated where the dose is read.
        assert "insulin-naive" in cat["dosage"].lower()
        # The euglycemic-DKA hazard must be documented (ketones can rise while
        # glucose stays normal — the single most important safety fact).
        combined = (cat.get("notes", "") + entry.get("side_effects", "")).lower()
        assert "ketoacidosis" in combined or "dka" in combined
        assert "ketone" in combined
        # Insulin must be listed as a contraindicated interaction.
        referenced = {i["drug"] for i in entry.get("drug_interactions", [])}
        assert "insulin" in referenced
        # Dogs must be flagged unestablished/not indicated, never dosed.
        dog = entry["species_info"]["dog"]
        assert dog["safe"] is False


def test_allopurinol_present_with_azathioprine_interaction():
    """Allopurinol is referenced as an interacting drug by azathioprine,
    cyclophosphamide and the aminopenicillins, and is itself a staple for urate
    urolithiasis and canine leishmaniasis. Guards the referenced-but-absent gap and
    the clinically critical xanthine-oxidase interaction with thiopurines."""
    allo = next((d for d in DRUGS if d["id"] == "allopurinol"), None)
    assert allo is not None, "allopurinol missing from drug manual"
    assert allo["category"] in DRUG_CATEGORIES
    dog = allo["species_info"]["dog"]
    assert dog["safe"] is True
    assert dog["dosage"].strip()
    # The dangerous azathioprine interaction must be documented on the entry.
    referenced = {i["drug"] for i in allo.get("drug_interactions", [])}
    assert "azathioprine" in referenced
    # And azathioprine's own entry must point back at allopurinol (bidirectional).
    aza = next((d for d in DRUGS if d["id"] == "azathioprine"), None)
    if aza is not None:
        aza_refs = {i.get("drug", "").lower() for i in aza.get("drug_interactions", [])}
        assert any("allopurinol" in r for r in aza_refs)


def test_enrofloxacin_present_and_correct():
    drug = next((d for d in DRUGS if d["id"] == "enrofloxacin"), None)
    assert drug is not None
    assert drug["name"] == "Enrofloxacin"
    assert drug["species_info"]["cat"]["safe"] is True
    assert drug["species_info"]["rabbit"]["safe"] is True


def test_all_drug_ids_unique():
    ids = [d["id"] for d in DRUGS]
    assert len(ids) == len(set(ids)), "Duplicate drug IDs found"


# ---------------------------------------------------------------------------
# search_drugs() tests
# ---------------------------------------------------------------------------


def test_search_drugs_returns_list():
    result = search_drugs("")
    assert isinstance(result, list)


def test_search_drugs_empty_query_returns_all():
    result = search_drugs("")
    assert len(result) == len(DRUGS)


def test_search_drugs_by_english_name():
    result = search_drugs("Amoxicillin")
    ids = [d["id"] for d in result]
    assert "amoxicillin" in ids


def test_search_drugs_case_insensitive():
    lower = search_drugs("amoxicillin")
    upper = search_drugs("AMOXICILLIN")
    assert {d["id"] for d in lower} == {d["id"] for d in upper}


def test_search_drugs_by_japanese_name():
    result = search_drugs("アモキシシリン")
    ids = [d["id"] for d in result]
    assert "amoxicillin" in ids


def test_search_drugs_by_mechanism_keyword():
    result = search_drugs("fluoroquinolone")
    ids = [d["id"] for d in result]
    assert "enrofloxacin" in ids


def test_search_drugs_no_match_returns_empty():
    result = search_drugs("xyznonexistentdrug12345")
    assert result == []


def test_search_drugs_with_category_filter():
    result = search_drugs("", category="antibiotics")
    assert len(result) > 0
    assert all(d["category"] == "antibiotics" for d in result)


def test_search_drugs_with_invalid_category_returns_empty():
    result = search_drugs("", category="not_a_real_category")
    assert result == []


def test_search_drugs_with_species_dog_excludes_unsafe():
    result = search_drugs("", species="dog")
    # All returned drugs must be safe for dogs (safe=True or safe absent means safe)
    for drug in result:
        info = drug["species_info"].get("dog", {})
        assert info.get("safe", True) is True, f"Drug '{drug['id']}' returned for 'dog' but is not safe"


def test_search_drugs_with_species_rabbit_excludes_amoxicillin():
    # Amoxicillin is contraindicated (safe=False) for rabbits
    result = search_drugs("", species="rabbit")
    ids = [d["id"] for d in result]
    assert "amoxicillin" not in ids


def test_search_drugs_with_species_rabbit_includes_enrofloxacin():
    result = search_drugs("", species="rabbit")
    ids = [d["id"] for d in result]
    assert "enrofloxacin" in ids


def test_search_drugs_species_with_no_species_info_excluded():
    # A drug with no rabbit entry at all should be excluded when filtering by rabbit
    result = search_drugs("", species="rabbit")
    for drug in result:
        assert "rabbit" in drug.get("species_info", {}), f"Drug '{drug['id']}' has no rabbit info but was returned"


def test_search_drugs_combined_query_and_category():
    result = search_drugs("amoxicillin", category="antibiotics")
    assert len(result) > 0
    assert all(d["category"] == "antibiotics" for d in result)
    ids = [d["id"] for d in result]
    assert "amoxicillin" in ids


def test_search_drugs_combined_query_and_species():
    result = search_drugs("doxycycline", species="cat")
    ids = [d["id"] for d in result]
    assert "doxycycline" in ids
    for drug in result:
        if "cat" in drug["species_info"]:
            assert drug["species_info"]["cat"]["safe"] is True


def test_search_drugs_none_query_treated_as_empty():
    result = search_drugs(None)
    assert isinstance(result, list)
    assert len(result) == len(DRUGS)


# ---------------------------------------------------------------------------
# get_drugs_by_category() tests
# ---------------------------------------------------------------------------


def test_get_drugs_by_category_antibiotics():
    result = get_drugs_by_category("antibiotics")
    assert isinstance(result, list)
    assert len(result) > 0
    assert all(d["category"] == "antibiotics" for d in result)


def test_get_drugs_by_category_contains_amoxicillin():
    result = get_drugs_by_category("antibiotics")
    ids = [d["id"] for d in result]
    assert "amoxicillin" in ids


def test_get_drugs_by_category_nsaids():
    result = get_drugs_by_category("nsaids")
    assert isinstance(result, list)
    # NSAIDs category may have drugs; all must be in that category
    assert all(d["category"] == "nsaids" for d in result)


def test_get_drugs_by_category_invalid_returns_empty():
    result = get_drugs_by_category("not_a_real_category")
    assert result == []


def test_get_drugs_by_category_empty_string_returns_empty():
    result = get_drugs_by_category("")
    assert result == []


def test_get_drugs_by_category_all_categories_return_lists():
    for cat_id in DRUG_CATEGORIES:
        result = get_drugs_by_category(cat_id)
        assert isinstance(result, list), f"Expected list for category '{cat_id}'"


# ---------------------------------------------------------------------------
# get_drugs_by_species() tests
# ---------------------------------------------------------------------------


def test_get_drugs_by_species_dog_returns_list():
    result = get_drugs_by_species("dog")
    assert isinstance(result, list)
    assert len(result) > 0


def test_get_drugs_by_species_dog_all_have_species_dosage():
    result = get_drugs_by_species("dog")
    for drug in result:
        assert "_species_dosage" in drug, f"Drug '{drug['id']}' missing '_species_dosage' key"


def test_get_drugs_by_species_dog_species_dosage_structure():
    result = get_drugs_by_species("dog")
    for drug in result:
        dosage_info = drug["_species_dosage"]
        has_dosage = "dosage" in dosage_info or "dose" in dosage_info
        assert has_dosage, f"Drug '{drug['id']}' missing 'dosage' or 'dose' in _species_dosage"


def test_get_drugs_by_species_dog_includes_amoxicillin():
    result = get_drugs_by_species("dog")
    ids = [d["id"] for d in result]
    assert "amoxicillin" in ids


def test_get_drugs_by_species_cat_returns_list():
    result = get_drugs_by_species("cat")
    assert isinstance(result, list)
    assert len(result) > 0


def test_get_drugs_by_species_cat_includes_enrofloxacin():
    result = get_drugs_by_species("cat")
    ids = [d["id"] for d in result]
    assert "enrofloxacin" in ids


def test_get_drugs_by_species_cat_species_dosage_matches_source():
    """_species_dosage must match the original species_info['cat'] entry."""
    result = get_drugs_by_species("cat")
    for drug in result:
        original_info = drug["species_info"]["cat"]
        assert drug["_species_dosage"] == original_info


def test_get_drugs_by_species_rabbit_returns_list():
    result = get_drugs_by_species("rabbit")
    assert isinstance(result, list)
    assert len(result) > 0


def test_get_drugs_by_species_rabbit_includes_enrofloxacin():
    result = get_drugs_by_species("rabbit")
    ids = [d["id"] for d in result]
    assert "enrofloxacin" in ids


def test_get_drugs_by_species_rabbit_includes_unsafe_drugs():
    """get_drugs_by_species returns ALL drugs with a species entry, including unsafe ones."""
    result = get_drugs_by_species("rabbit")
    ids = [d["id"] for d in result]
    # Amoxicillin has a rabbit entry (safe=False) so it must be included
    assert "amoxicillin" in ids


def test_get_drugs_by_species_unknown_species_returns_empty():
    result = get_drugs_by_species("dragon")
    assert result == []


def test_get_drugs_by_species_only_includes_drugs_with_that_species():
    result = get_drugs_by_species("hamster")
    for drug in result:
        assert "hamster" in drug.get("species_info", {}), f"Drug '{drug['id']}' has no hamster info but was returned"


# ---------------------------------------------------------------------------
# get_drug_by_id() tests
# ---------------------------------------------------------------------------


def test_get_drug_by_id_amoxicillin():
    drug = get_drug_by_id("amoxicillin")
    assert drug is not None
    assert drug["id"] == "amoxicillin"
    assert drug["name"] == "Amoxicillin"


def test_get_drug_by_id_enrofloxacin():
    drug = get_drug_by_id("enrofloxacin")
    assert drug is not None
    assert drug["id"] == "enrofloxacin"
    assert drug["category"] == "antibiotics"


def test_get_drug_by_id_doxycycline():
    drug = get_drug_by_id("doxycycline")
    assert drug is not None
    assert drug["name"] == "Doxycycline"


def test_get_drug_by_id_nonexistent_returns_none():
    result = get_drug_by_id("nonexistent_drug_xyz")
    assert result is None


def test_get_drug_by_id_empty_string_returns_none():
    result = get_drug_by_id("")
    assert result is None


def test_get_drug_by_id_returns_full_drug_dict():
    drug = get_drug_by_id("amoxicillin")
    for field in REQUIRED_DRUG_FIELDS:
        assert field in drug


def test_get_drug_by_id_case_sensitive():
    # IDs are lowercase; uppercase should not match
    result = get_drug_by_id("AMOXICILLIN")
    assert result is None


# ---------------------------------------------------------------------------
# Flask route tests
# ---------------------------------------------------------------------------


class TestApiListDrugs:
    def test_get_all_drugs_status_200(self, client):
        resp = client.get("/api/drugs")
        assert resp.status_code == 200

    def test_get_all_drugs_response_keys(self, client):
        resp = client.get("/api/drugs")
        data = resp.get_json()
        assert "drugs" in data
        assert "total" in data
        assert "categories" in data

    def test_get_all_drugs_total_matches_list(self, client):
        resp = client.get("/api/drugs")
        data = resp.get_json()
        assert data["total"] == len(data["drugs"])
        assert data["total"] == len(DRUGS)

    def test_drug_list_item_structure(self, client):
        resp = client.get("/api/drugs")
        data = resp.get_json()
        assert len(data["drugs"]) > 0
        for drug in data["drugs"]:
            assert "id" in drug
            assert "name" in drug
            assert "name_ja" in drug
            assert "category" in drug
            assert "category_ja" in drug
            assert "species_info" in drug

    def test_list_fields_always_serialized_as_lists(self, client):
        """side_effects/routes/formulations must be arrays in the API response.

        Some source entries store these as comma-separated strings; the
        frontend maps/joins them, so a stray string crashed the entire drug
        list render. The API normalizes them to lists at the boundary.
        """
        resp = client.get("/api/drugs")
        data = resp.get_json()
        list_fields = (
            "side_effects",
            "side_effects_ja",
            "routes",
            "routes_ja",
            "formulations",
            "formulations_ja",
        )
        for drug in data["drugs"]:
            for field in list_fields:
                if field in drug:
                    assert isinstance(drug[field], list), (
                        f"{drug['id']}.{field} should be a list, got {type(drug[field]).__name__}"
                    )

    def test_string_side_effects_split_into_list(self, client):
        """A drug whose source side_effects is a comma string is split to tags.

        Targets the canonical ``gabapentin`` id: the duplicate entries
        (``gabapentin_oral`` / ``gabapentin_pain``) are now logically merged into
        it, so they no longer appear as separate rows. Old ids still resolve via
        ``resolve_drug_id`` — covered by ``test_merged_drug_id_still_resolves``.
        """
        resp = client.get("/api/drugs?search=gabapentin")
        data = resp.get_json()
        gaba = next((d for d in data["drugs"] if d["id"] == "gabapentin"), None)
        assert gaba is not None
        assert isinstance(gaba["side_effects"], list)
        assert len(gaba["side_effects"]) >= 2

    def test_search_by_query_param(self, client):
        resp = client.get("/api/drugs?search=amoxicillin")
        data = resp.get_json()
        ids = [d["id"] for d in data["drugs"]]
        assert "amoxicillin" in ids

    def test_search_no_match_returns_empty_drugs(self, client):
        resp = client.get("/api/drugs?search=xyznonexistentdrug99999")
        data = resp.get_json()
        assert data["total"] == 0
        assert data["drugs"] == []

    def test_filter_by_category(self, client):
        resp = client.get("/api/drugs?category=antibiotics")
        data = resp.get_json()
        assert data["total"] > 0
        assert all(d["category"] == "antibiotics" for d in data["drugs"])

    def test_filter_by_invalid_category(self, client):
        resp = client.get("/api/drugs?category=fake_category")
        data = resp.get_json()
        assert data["total"] == 0

    def test_filter_by_species_dog(self, client):
        resp = client.get("/api/drugs?species=dog")
        data = resp.get_json()
        assert data["total"] > 0
        # All returned drugs must have dog info and be safe (safe=True or absent)
        for drug in data["drugs"]:
            dog_info = drug["species_info"].get("dog", {})
            assert dog_info.get("safe", True) is True

    def test_filter_by_species_rabbit_excludes_amoxicillin(self, client):
        resp = client.get("/api/drugs?species=rabbit")
        data = resp.get_json()
        ids = [d["id"] for d in data["drugs"]]
        assert "amoxicillin" not in ids

    def test_filter_by_species_and_query_combined(self, client):
        resp = client.get("/api/drugs?search=enrofloxacin&species=rabbit")
        data = resp.get_json()
        ids = [d["id"] for d in data["drugs"]]
        assert "enrofloxacin" in ids

    def test_categories_in_response(self, client):
        resp = client.get("/api/drugs")
        data = resp.get_json()
        assert "antibiotics" in data["categories"]
        assert data["categories"]["antibiotics"]["en"] == "Antibiotics"

    def test_list_includes_clinical_detail_fields(self, client):
        """The list payload must carry the fields the detail panel renders, so
        the expandable drug view shows mechanism / side effects / interactions /
        contraindications rather than blank sections."""
        resp = client.get("/api/drugs?search=meloxicam")
        data = resp.get_json()
        mel = next(d for d in data["drugs"] if d["id"] == "meloxicam")
        assert mel.get("mechanism_ja")
        assert mel.get("side_effects_ja") and isinstance(mel["side_effects_ja"], list)
        assert mel.get("drug_interactions") and len(mel["drug_interactions"]) > 0
        assert mel.get("contraindications")  # English contraindications
        assert mel.get("contraindications_ja")

    def test_list_omits_empty_optional_fields(self, client):
        """Optional fields absent from the source drug should not be emitted,
        keeping the payload lean."""
        resp = client.get("/api/drugs?search=meloxicam")
        data = resp.get_json()
        mel = next(d for d in data["drugs"] if d["id"] == "meloxicam")
        # meloxicam has no route/formulation/sponsor data → keys should be absent
        assert "routes" not in mel
        assert "sponsor" not in mel

    def test_sponsor_drugs_expose_sponsor_metadata(self, client):
        resp = client.get("/api/drugs")
        data = resp.get_json()
        sponsored = [d for d in data["drugs"] if d.get("sponsor")]
        assert sponsored, "expected at least one sponsor drug in catalog"
        for d in sponsored:
            assert d.get("sponsor_name")
            # frontend falls back sponsor_url -> sponsor_url_dog -> default
            assert d.get("sponsor_url") or d.get("sponsor_url_dog")


class TestApiGetDrug:
    def test_get_existing_drug_status_200(self, client):
        resp = client.get("/api/drugs/amoxicillin")
        assert resp.status_code == 200

    def test_get_existing_drug_response_structure(self, client):
        resp = client.get("/api/drugs/amoxicillin")
        data = resp.get_json()
        assert "drug" in data
        drug = data["drug"]
        assert drug["id"] == "amoxicillin"
        assert drug["name"] == "Amoxicillin"

    def test_get_enrofloxacin(self, client):
        resp = client.get("/api/drugs/enrofloxacin")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["drug"]["id"] == "enrofloxacin"

    def test_get_doxycycline(self, client):
        resp = client.get("/api/drugs/doxycycline")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["drug"]["name"] == "Doxycycline"

    def test_get_nonexistent_drug_status_404(self, client):
        resp = client.get("/api/drugs/nonexistent_drug_xyz")
        assert resp.status_code == 404

    def test_get_nonexistent_drug_error_message(self, client):
        resp = client.get("/api/drugs/nonexistent_drug_xyz")
        data = resp.get_json()
        assert "error" in data
        assert data["error"] == "Drug not found"

    def test_get_drug_contains_species_info(self, client):
        resp = client.get("/api/drugs/amoxicillin")
        data = resp.get_json()
        drug = data["drug"]
        assert "species_info" in drug
        assert "dog" in drug["species_info"]
        assert drug["species_info"]["dog"]["safe"] is True

    def test_get_drug_contraindicated_species(self, client):
        resp = client.get("/api/drugs/amoxicillin")
        data = resp.get_json()
        rabbit_info = data["drug"]["species_info"]["rabbit"]
        assert rabbit_info["safe"] is False


class TestApiDrugCategories:
    def test_categories_status_200(self, client):
        resp = client.get("/api/drug-categories")
        assert resp.status_code == 200

    def test_categories_response_keys(self, client):
        resp = client.get("/api/drug-categories")
        data = resp.get_json()
        assert "categories" in data
        assert "total_drugs" in data

    def test_total_drugs_matches_drugs_list(self, client):
        resp = client.get("/api/drug-categories")
        data = resp.get_json()
        assert data["total_drugs"] == len(DRUGS)

    def test_categories_list_structure(self, client):
        resp = client.get("/api/drug-categories")
        data = resp.get_json()
        assert isinstance(data["categories"], list)
        assert len(data["categories"]) > 0
        for cat in data["categories"]:
            assert "id" in cat
            assert "name_ja" in cat
            assert "name_en" in cat
            assert "count" in cat
            assert isinstance(cat["count"], int)

    def test_categories_sorted_by_count_descending(self, client):
        resp = client.get("/api/drug-categories")
        data = resp.get_json()
        counts = [cat["count"] for cat in data["categories"]]
        assert counts == sorted(counts, reverse=True)

    def test_antibiotics_in_categories(self, client):
        resp = client.get("/api/drug-categories")
        data = resp.get_json()
        cat_ids = [c["id"] for c in data["categories"]]
        assert "antibiotics" in cat_ids

    def test_antibiotics_category_names(self, client):
        resp = client.get("/api/drug-categories")
        data = resp.get_json()
        antibiotics = next(c for c in data["categories"] if c["id"] == "antibiotics")
        assert antibiotics["name_en"] == "Antibiotics"
        assert antibiotics["name_ja"] == "抗菌薬・抗生物質"

    def test_categories_cover_all_drug_categories(self, client):
        resp = client.get("/api/drug-categories")
        data = resp.get_json()
        returned_ids = {c["id"] for c in data["categories"]}
        for cat_id in DRUG_CATEGORIES:
            assert cat_id in returned_ids, f"Category '{cat_id}' missing from response"

    def test_category_counts_are_accurate(self, client):
        resp = client.get("/api/drug-categories")
        data = resp.get_json()
        for cat in data["categories"]:
            expected = len([d for d in DRUGS if d["category"] == cat["id"]])
            assert cat["count"] == expected, (
                f"Category '{cat['id']}' count mismatch: got {cat['count']}, expected {expected}"
            )


# =============================================================================
# Drug-Disease Linking
# =============================================================================


class TestDrugDiseaseLinking:
    """Auto-extraction of drugs mentioned in disease treatment text."""

    def test_keyword_index_built(self):
        from api.drug_dictionary import _DRUG_KEYWORD_INDEX

        assert len(_DRUG_KEYWORD_INDEX) > 100
        # Common drugs should be indexed
        assert "amoxicillin" in _DRUG_KEYWORD_INDEX
        assert "アモキシシリン" in _DRUG_KEYWORD_INDEX

    def test_find_drugs_in_text_basic(self):
        from api.drug_dictionary import find_drugs_in_text

        text = "Treat with amoxicillin 10 mg/kg PO q12h; add enrofloxacin if severe."
        result = find_drugs_in_text(text)
        ids = {d["id"] for d in result}
        assert "amoxicillin" in ids
        assert "enrofloxacin" in ids

    def test_find_drugs_in_text_empty(self):
        from api.drug_dictionary import find_drugs_in_text

        assert find_drugs_in_text("") == []
        assert find_drugs_in_text(None) == []

    def test_find_drugs_for_disease_dog(self):
        from api.drug_dictionary import find_drugs_for_disease

        result = find_drugs_for_disease("dog", "Sepsis and SIRS", lang="en")
        assert len(result) > 0
        ids = {d["id"] for d in result}
        # Sepsis treatment should mention common antibiotics
        assert any(i in ids for i in ("enrofloxacin", "metronidazole", "ampicillin"))

    def test_find_drugs_for_disease_unknown_returns_empty(self):
        from api.drug_dictionary import find_drugs_for_disease

        assert find_drugs_for_disease("dog", "Definitely Not A Real Disease 12345") == []

    def test_find_drugs_for_disease_unknown_species_returns_empty(self):
        from api.drug_dictionary import find_drugs_for_disease

        assert find_drugs_for_disease("dragon", "Anything") == []

    def test_api_drugs_for_disease_endpoint(self, client):
        resp = client.get("/api/drugs/for-disease?species=dog&name=Sepsis%20and%20SIRS")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "drugs" in data
        assert data["count"] >= 1

    def test_api_drugs_for_disease_missing_params(self, client):
        resp = client.get("/api/drugs/for-disease")
        assert resp.status_code == 400
        resp = client.get("/api/drugs/for-disease?species=dog")
        assert resp.status_code == 400

    # --- Reverse: drug → diseases ---
    def test_find_diseases_for_drug_returns_list(self):
        from api.drug_dictionary import find_diseases_for_drug

        diseases = find_diseases_for_drug("enrofloxacin", limit=20)
        assert isinstance(diseases, list)
        assert len(diseases) > 0
        for d in diseases:
            assert "species" in d and "name" in d and "urgency" in d

    def test_find_diseases_for_drug_species_filter(self):
        from api.drug_dictionary import find_diseases_for_drug

        all_results = find_diseases_for_drug("doxycycline", limit=200)
        dog_only = find_diseases_for_drug("doxycycline", species="dog", limit=200)
        assert len(dog_only) <= len(all_results)
        assert all(d["species"] == "dog" for d in dog_only)

    def test_find_diseases_for_drug_unknown_returns_empty(self):
        from api.drug_dictionary import find_diseases_for_drug

        assert find_diseases_for_drug("nonexistent_drug_xyz_12345") == []

    def test_find_diseases_for_drug_sorted_by_urgency(self):
        from api.drug_dictionary import find_diseases_for_drug

        results = find_diseases_for_drug("epinephrine", limit=50)
        urgencies = [d.get("urgency", "") for d in results]
        emergency_indices = [i for i, u in enumerate(urgencies) if u == "emergency"]
        normal_indices = [i for i, u in enumerate(urgencies) if u in ("normal", "")]
        if emergency_indices and normal_indices:
            assert max(emergency_indices) < min(normal_indices)

    def test_api_diseases_for_drug_endpoint(self, client):
        resp = client.get("/api/drugs/enrofloxacin/diseases?limit=10")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "diseases" in data
        assert data["drug_id"] == "enrofloxacin"
        assert isinstance(data["count"], int)

    def test_api_diseases_for_drug_not_found(self, client):
        resp = client.get("/api/drugs/nonexistent_xyz/diseases")
        assert resp.status_code == 404

    def test_api_diseases_for_drug_with_species_filter(self, client):
        resp = client.get("/api/drugs/doxycycline/diseases?species=cat&limit=20")
        assert resp.status_code == 200
        data = resp.get_json()
        assert all(d["species"] == "cat" for d in data["diseases"])


# =============================================================================
# Emergency Protocols additions (sepsis/mamushi/hemorrhagic/PTE/eclampsia)
# =============================================================================


class TestEmergencyProtocolsAdditions:
    """5 new emergency scenarios added to EMERGENCY_PROTOCOLS."""

    def test_new_protocols_present(self):
        from api.emergency_protocols import EMERGENCY_PROTOCOLS

        ids = {p["id"] for p in EMERGENCY_PROTOCOLS}
        for new_id in (
            "sepsis_septic_shock",
            "mamushi_envenomation",
            "hemorrhagic_shock",
            "ards_pulmonary_thromboembolism",
            "postpartum_eclampsia",
        ):
            assert new_id in ids, f"Missing new emergency protocol: {new_id}"

    def test_new_protocols_have_required_fields(self):
        from api.emergency_protocols import EMERGENCY_PROTOCOLS

        new_ids = {
            "sepsis_septic_shock",
            "mamushi_envenomation",
            "hemorrhagic_shock",
            "ards_pulmonary_thromboembolism",
            "postpartum_eclampsia",
        }
        for p in EMERGENCY_PROTOCOLS:
            if p["id"] in new_ids:
                assert p.get("category")
                assert p.get("title_ja") and p.get("title_en")
                assert p.get("trigger_signs_ja") and p.get("trigger_signs_en")
                assert p.get("steps") and len(p["steps"]) >= 3
                assert p.get("key_drugs") and len(p["key_drugs"]) >= 3
                assert p.get("monitoring")
                assert p.get("ref")


def test_batch33_referenced_but_absent_drugs_present():
    """2026-08 audit: five drugs referenced by the manual's own interaction
    lists or by the anesthesia protocols had no formulary entry. Guard the gap:
    methotrexate (10 interaction refs), quinidine (equine AF treatment of
    choice), pyrimethamine (EPM backbone), EMLA cream (named by rabbit
    anesthesia protocols), niacinamide (tetracycline/niacinamide combination
    for canine immune-mediated dermatoses)."""
    by_id = {d["id"]: d for d in DRUGS}
    for drug_id in ("methotrexate", "quinidine", "pyrimethamine", "emla_cream", "niacinamide"):
        entry = by_id.get(drug_id)
        assert entry is not None, f"{drug_id} missing from drug manual"
        assert entry["category"] in DRUG_CATEGORIES
        assert entry.get("mechanism") and entry.get("mechanism_ja")
        assert entry.get("side_effects_ja") and entry.get("contraindications_ja")
        for sp, info in entry["species_info"].items():
            if info.get("safe"):
                assert (info.get("dosage") or "").strip(), f"{drug_id}/{sp}: safe but no dosage"
                assert (info.get("dosage_ja") or "").strip(), f"{drug_id}/{sp}: safe but no dosage_ja"


def test_quinidine_equine_af_protocol_is_evidence_based():
    """Quinidine sulfate is the pharmacologic conversion agent for equine atrial
    fibrillation. The horse entry must state the 22 mg/kg q2h NGT protocol and
    the QRS-widening stop criterion (Reed & Bayly; ACVIM consensus 2014)."""
    quinidine = next(d for d in DRUGS if d["id"] == "quinidine")
    horse = quinidine["species_info"]["horse"]
    assert horse["safe"] is True
    assert "22 mg/kg" in horse["dosage"]
    assert "q2h" in horse["dosage"]
    assert "25%" in horse["dosage"]  # QRS widening >25% = stop signal
    # The classic digoxin doubling interaction must be documented.
    refs = {i["drug"].lower() for i in quinidine.get("drug_interactions", [])}
    assert "digoxin" in refs


def test_pyrimethamine_epm_combination_and_pregnancy_caution():
    """EPM therapy is pyrimethamine 1 mg/kg WITH sulfadiazine 20 mg/kg PO q24h
    (ReBalance, FDA NADA 141-240); folic acid supplementation in pregnant mares
    on this protocol is associated with congenital defects and must be warned."""
    pyri = next(d for d in DRUGS if d["id"] == "pyrimethamine")
    horse = pyri["species_info"]["horse"]
    assert "1 mg/kg" in horse["dosage"]
    assert "sulfadiazine" in horse["dosage"].lower()
    assert "20 mg/kg" in horse["dosage"]
    notes = horse.get("notes", "").lower()
    assert "folic" in notes and "pregnan" in notes


def test_emla_cream_feline_methemoglobinemia_caution():
    """EMLA is named by the rabbit anesthesia protocols; the entry must carry
    the prilocaine methemoglobinemia caution for cats and an occlusion/timing
    instruction for rabbits (Flecknell, BSAVA Manual of Rabbit Medicine)."""
    emla = next(d for d in DRUGS if d["id"] == "emla_cream")
    rabbit = emla["species_info"]["rabbit"]
    assert rabbit["safe"] is True
    assert "30-60" in rabbit["dosage"]
    cat_combined = (emla["species_info"]["cat"].get("notes", "") + emla.get("side_effects", "")).lower()
    assert "methemoglobin" in cat_combined
