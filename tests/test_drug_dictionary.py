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


def test_batch33_referenced_drugs_present_with_complete_dosing():
    """The 2026-08 audit found 14 drugs that disease treatments, interaction
    lists and anesthesia protocols reference but the formulary did not carry.
    Guards that each is present, categorised, and fully dosed for every
    species flagged safe."""
    expected = [
        "pyrimethamine",
        "quinidine",
        "valacyclovir",
        "meclizine",
        "colchicine",
        "leuprolide",
        "niacinamide",
        "dexrazoxane",
        "methotrexate",
        "thiamine_b1",
        "l_carnitine",
        "paromomycin",
        "emla_cream",
        "dextrose_50",
    ]
    index = {d["id"]: d for d in DRUGS}
    for drug_id in expected:
        entry = index.get(drug_id)
        assert entry is not None, f"{drug_id} missing from drug manual"
        assert entry["category"] in DRUG_CATEGORIES
        assert entry["mechanism_ja"].strip() and entry["mechanism"].strip()
        for species, info in entry["species_info"].items():
            if info.get("safe"):
                assert info["dosage"].strip(), f"{drug_id}/{species} missing dosage"
                assert info["dosage_ja"].strip(), f"{drug_id}/{species} missing dosage_ja"


def test_valacyclovir_is_flagged_fatal_in_cats():
    """Valacyclovir is the equine EHV-1/EHM antiviral, but at herpes-therapeutic
    doses it causes fatal hepatic/renal necrosis and marrow suppression in cats
    (Nasisse 1997). The feline entry must be safe:False and say so; famciclovir
    must be named as the feline alternative."""
    vala = next((d for d in DRUGS if d["id"] == "valacyclovir"), None)
    assert vala is not None
    horse = vala["species_info"]["horse"]
    assert horse["safe"] is True
    assert "27 mg/kg" in horse["dosage"]
    cat = vala["species_info"]["cat"]
    assert cat["safe"] is False
    combined = (cat.get("notes", "") + cat.get("dosage", "")).lower()
    assert "fatal" in combined
    assert "famciclovir" in combined


def test_quinidine_equine_af_protocol_with_digoxin_interaction():
    """Quinidine is the classic conversion drug for equine atrial fibrillation
    (Reef 2014 ACVIM consensus): 22 mg/kg via NGT q2h with the QRS > 25%
    widening stop rule, and it roughly doubles plasma digoxin. Digoxin's own
    interaction list references it, so the entry must exist and document both."""
    quin = next((d for d in DRUGS if d["id"] == "quinidine"), None)
    assert quin is not None
    horse = quin["species_info"]["horse"]
    assert horse["safe"] is True
    assert "22 mg/kg" in horse["dosage"]
    assert "25%" in horse["dosage"] or "25%" in horse.get("notes", "")
    referenced = {i["drug"].lower() for i in quin.get("drug_interactions", [])}
    assert "digoxin" in referenced
    # Cats have safer alternatives; the entry must not present quinidine as usable.
    assert quin["species_info"]["cat"]["safe"] is False


def test_paromomycin_feline_absorption_warning():
    """Oral paromomycin caused acute renal failure and deafness in cats treated
    for cryptosporidiosis — the damaged mucosa absorbs the aminoglycoside
    (Gookin 1999). The feline entry must be flagged and explain the mechanism."""
    paro = next((d for d in DRUGS if d["id"] == "paromomycin"), None)
    assert paro is not None
    cat = paro["species_info"]["cat"]
    assert cat["safe"] is False
    notes = cat.get("notes", "").lower()
    assert "renal" in notes
    assert "deafness" in notes


def test_dextrose_and_emla_carry_route_safety_warnings():
    """Dextrose 50% must warn against undiluted peripheral administration
    (phlebitis/necrosis) and EMLA must carry the feline prilocaine
    methemoglobinemia caution — both referenced by anesthesia protocols."""
    dex = next((d for d in DRUGS if d["id"] == "dextrose_50"), None)
    assert dex is not None
    dog = dex["species_info"]["dog"]
    assert "dilut" in dog["dosage"].lower()
    assert "necrosis" in (dog.get("notes", "") + dex.get("side_effects", "")).lower()
    # Ferret insulinoma rebound warning (the anesthesia protocol referencing it)
    ferret = dex["species_info"]["ferret"]
    assert "rebound" in (ferret.get("notes", "") + ferret.get("dosage", "")).lower()

    emla = next((d for d in DRUGS if d["id"] == "emla_cream"), None)
    assert emla is not None
    for sp in ("rabbit", "guinea_pig"):
        assert emla["species_info"][sp]["safe"] is True
        assert emla["species_info"][sp]["dosage"].strip()
    assert "methemoglobin" in (emla["species_info"]["cat"].get("notes", "") + emla.get("side_effects", "")).lower()


def test_pyrimethamine_epm_regimen_matches_consensus():
    """EPM disease entries reference pyrimethamine/sulfadiazine; the entry must
    carry the FDA-approved ReBalance regimen (1 + 20 mg/kg PO q24h) and the
    folate-antagonist marrow-suppression monitoring note."""
    pyri = next((d for d in DRUGS if d["id"] == "pyrimethamine"), None)
    assert pyri is not None
    horse = pyri["species_info"]["horse"]
    assert horse["safe"] is True
    assert "1 mg/kg" in horse["dosage"]
    assert "20 mg/kg" in horse["dosage"]
    combined = (horse.get("notes", "") + pyri.get("side_effects", "")).lower()
    assert "marrow" in combined or "cbc" in combined


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

    def test_keyword_index_indexes_japanese_base_name(self):
        """Japanese names with a parenthetical brand suffix must index the base
        name, so treatment text that writes only the generic drug name matches.

        Regression: "メチマゾール（タパゾール/フェリマゾール）" was indexed only as
        the full string, so Japanese treatment text saying "メチマゾール" matched
        nothing — Japanese users (the primary audience) got no drug links even
        though the English side matched fine.
        """
        from api.drug_dictionary import _DRUG_KEYWORD_INDEX

        assert _DRUG_KEYWORD_INDEX.get("メチマゾール") == "methimazole"
        assert _DRUG_KEYWORD_INDEX.get("マロピタント") == "maropitant"
        assert _DRUG_KEYWORD_INDEX.get("ピモベンダン") == "pimobendan"

    def test_find_drugs_in_text_japanese_generic_name(self):
        """The generic Japanese drug name in treatment text should match the
        drug even when the dictionary entry carries a brand suffix."""
        from api.drug_dictionary import find_drugs_in_text

        text = "内科治療：メチマゾール（フェリマゾール 2.5 mg PO q12h）で甲状腺ホルモンを抑制。"
        ids = {d["id"] for d in find_drugs_in_text(text)}
        assert "methimazole" in ids

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


def test_batch34_referenced_drugs_present_with_complete_dosing():
    """The 2026-08 second referenced-but-absent sweep found 11 agents that
    disease treatments and interaction lists reference but the formulary did
    not carry (vinblastine alone is named by 408 treatment entries; the
    crystalloid fluids by 1,700+). Guards that each is present, categorised,
    bilingual, and fully dosed for every species flagged safe."""
    expected = [
        "vinblastine",
        "lactated_ringers",
        "normosol_r",
        "l_theanine",
        "alpha_casozepine",
        "povidone_iodine",
        "folic_acid",
        "dmso",
        "mineral_oil",
        "lugols_iodine",
        "fluorescein",
    ]
    index = {d["id"]: d for d in DRUGS}
    for drug_id in expected:
        entry = index.get(drug_id)
        assert entry is not None, f"{drug_id} missing from drug manual"
        assert entry["category"] in DRUG_CATEGORIES
        assert entry["mechanism_ja"].strip() and entry["mechanism"].strip()
        for species, info in entry["species_info"].items():
            if info.get("safe"):
                assert info["dosage"].strip(), f"{drug_id}/{species} missing dosage"
                assert info["dosage_ja"].strip(), f"{drug_id}/{species} missing dosage_ja"


def test_vinblastine_mct_protocol_and_vesicant_warning():
    """Mast cell tumor protocols across the disease DB name vinblastine +
    prednisolone (Thamm 2006). The entry must carry the protocol dose, the
    CBC/neutrophil gate, and the vesicant handling that differs from
    doxorubicin (WARM compress for vinca extravasation)."""
    vin = next((d for d in DRUGS if d["id"] == "vinblastine"), None)
    assert vin is not None
    dog = vin["species_info"]["dog"]
    assert dog["safe"] is True
    assert "2 mg/m²" in dog["dosage"] or "2 mg/m2" in dog["dosage"]
    assert "3,000" in dog["dosage"]  # neutrophil hold threshold
    notes = dog["notes"].lower()
    assert "vesicant" in notes
    assert "warm" in notes  # vinca extravasation uses warm compress, not cold
    # It must not be presented as interchangeable with vincristine.
    assert "vincristine" in vin["contraindications"].lower()


def test_crystalloid_fluids_present_with_species_rates():
    """Fluid therapy is the single most-referenced intervention in the disease
    DB (乳酸リンゲル 710 entries, ノルモソル 1,059) yet the formulary carried no
    crystalloid. Guards shock/maintenance rates and the two class-defining
    safety facts: LRS clots citrated blood in the same line (calcium), and
    Normosol-R/Plasma-Lyte is the calcium-free, blood-compatible alternative."""
    lrs = next((d for d in DRUGS if d["id"] == "lactated_ringers"), None)
    assert lrs is not None
    dog = lrs["species_info"]["dog"]
    assert "10-20 mL/kg" in dog["dosage"]  # canine shock bolus
    cat = lrs["species_info"]["cat"]
    assert "5-10 mL/kg" in cat["dosage"]  # feline shock bolus is smaller
    referenced = " ".join(i["drug"].lower() for i in lrs["drug_interactions"])
    assert "blood products" in referenced
    assert "ceftriaxone" in referenced
    norm = next((d for d in DRUGS if d["id"] == "normosol_r"), None)
    assert norm is not None
    assert "calcium-free" in norm["mechanism"].lower()
    # Small-exotic support: warmed SC maintenance documented for rabbits.
    assert "80-100 mL/kg" in norm["species_info"]["rabbit"]["dosage"]
    assert "80-100 mL/kg" in lrs["species_info"]["rabbit"]["dosage"]


def test_folic_acid_pregnant_mare_warning():
    """Folic acid is referenced by the pyrimethamine/sulfadiazine EPM regimen,
    but oral folic acid given to pregnant mares on that combination is
    associated with congenital defects in their foals (Toribio 1998). The
    horse entry must carry that warning where the dose is read, and the
    methotrexate interaction must point to folinic acid instead."""
    fol = next((d for d in DRUGS if d["id"] == "folic_acid"), None)
    assert fol is not None
    horse = fol["species_info"]["horse"]
    assert "pregnant" in horse["dosage"].lower()
    assert "妊娠馬" in horse["dosage_ja"]
    interactions = {i["drug"].lower(): i["effect"].lower() for i in fol["drug_interactions"]}
    assert "pyrimethamine" in interactions
    assert "folinic" in interactions.get("methotrexate", "")


def test_mineral_oil_and_dmso_carry_route_safety_warnings():
    """Mineral oil's one fatal failure mode is aspiration (lipoid pneumonia):
    the equine dose must demand NGT placement confirmation and the small-animal
    doses must forbid direct syringing. DMSO IV must state the <= 10% dilution
    (haemolysis above that)."""
    oil = next((d for d in DRUGS if d["id"] == "mineral_oil"), None)
    assert oil is not None
    assert "confirm" in oil["species_info"]["horse"]["dosage"].lower()
    for sp in ("dog", "cat"):
        combined = (oil["species_info"][sp]["dosage"] + oil["species_info"][sp].get("notes", "")).lower()
        assert "never syringe" in combined or "syringe" in combined
    dmso = next((d for d in DRUGS if d["id"] == "dmso"), None)
    assert dmso is not None
    horse = dmso["species_info"]["horse"]
    assert "10%" in horse["dosage"]
    assert "hemolysis" in (horse.get("notes", "") + dmso["side_effects"]).lower()


def test_treatment_text_drug_matcher_precision_and_recall():
    """The related-drug keyword index must (a) resolve the names treatment
    texts actually use — fluid names without the 液 suffix, slash alternates,
    parenthetical-stripped stems — and (b) no longer surface a drug for bare
    generic words ('sodium restriction', 'critical care monitoring',
    'vitamin supplementation'), which previously mapped to nitroprusside,
    Oxbow Critical Care and vitamin K1. Capitalised 'Critical Care' (the
    product, 1,000+ treatment entries) must still match case-sensitively."""
    from api.drug_dictionary import find_drugs_in_text

    def ids(text):
        return [d["id"] for d in find_drugs_in_text(text)]

    # Recall: the spellings treatment texts actually use.
    assert "lactated_ringers" in ids("輸液: 乳酸リンゲル 10-20 mL/kg IV")
    assert "normosol_r" in ids("温輸液（ノルモソルR） 25 mL/kg SC")
    assert "mineral_oil" in ids("ミネラルオイル2-4 LをNGT投与")
    assert "fluorescein" in ids("フルオレセイン染色で潰瘍を確認")
    assert "critical_care_herbivore" in ids("Syringe-feed Critical Care q6-8h")
    # Precision: bare generic words must not resolve to a drug.
    assert ids("sodium restriction and vitamin supplementation") == []
    assert ids("critical care monitoring overnight") == []
    # Full compound names keep working.
    assert "calcium_gluconate" in ids("calcium gluconate 10% IV slowly")
    assert "nitroprusside" in ids("sodium nitroprusside CRI")


def test_batch35_referenced_drugs_present_with_complete_dosing():
    """The 2026-08 third referenced-but-absent sweep (katakana token frequency
    over treatment texts + the antidote cross-reference audit) found 15 agents
    the DB's own protocols dose but the formulary did not carry — pralidoxime
    alone is named by 184 treatment references. Guards that each is present,
    categorised, bilingual, and fully dosed for every species flagged safe."""
    expected = [
        "pralidoxime",
        "insulin_regular",
        "triamcinolone",
        "imidocarb",
        "succimer",
        "cidofovir_ophthalmic",
        "albendazole",
        "enilconazole",
        "esmolol",
        "oseltamivir",
        "flurbiprofen_ophthalmic",
        "idoxuridine_ophthalmic",
        "triclabendazole",
        "dimercaprol",
        "celecoxib",
    ]
    index = {d["id"]: d for d in DRUGS}
    for drug_id in expected:
        entry = index.get(drug_id)
        assert entry is not None, f"{drug_id} missing from drug manual"
        assert entry["category"] in DRUG_CATEGORIES
        assert entry["mechanism_ja"].strip() and entry["mechanism"].strip()
        for species, info in entry["species_info"].items():
            if info.get("safe"):
                assert info["dosage"].strip(), f"{drug_id}/{species} missing dosage"
                assert info["dosage_ja"].strip(), f"{drug_id}/{species} missing dosage_ja"


def test_pralidoxime_op_antidote_pairing_and_carbamate_caveat():
    """Organophosphate toxicosis entries across the DB instruct 'atropine +
    pralidoxime'. The 2-PAM entry must carry the 20 mg/kg dose, the atropine
    pairing, the early-administration/aging window, and the carbamate relative
    contraindication (reactivation unnecessary; worsens carbaryl toxicosis)."""
    pam = next((d for d in DRUGS if d["id"] == "pralidoxime"), None)
    assert pam is not None
    dog = pam["species_info"]["dog"]
    assert "20 mg/kg" in dog["dosage"]
    assert "atropine" in dog["dosage"].lower()
    combined = (dog.get("notes", "") + pam["mechanism"]).lower()
    assert "age" in combined  # enzyme aging window
    assert "carbamate" in pam["contraindications"].lower()
    assert "カーバメート" in pam["contraindications_ja"]


def test_regular_insulin_dka_and_hyperkalemia_protocols():
    """DKA CRI protocols (0.05-0.1 U/kg/h) and hyperkalemia shifting doses
    (0.25-0.5 U/kg IV + dextrose) are quoted throughout the disease DB
    (blocked cat, AKI, Addisonian crisis) — the entry must match them, demand
    dextrose co-administration, warn about IV-tubing adsorption, and forbid
    starting insulin before severe hypokalemia is being corrected."""
    ins = next((d for d in DRUGS if d["id"] == "insulin_regular"), None)
    assert ins is not None
    dog = ins["species_info"]["dog"]
    assert "0.05-0.1" in dog["dosage"]
    assert "0.25-0.5" in dog["dosage"]
    assert "dextrose" in dog["dosage"].lower()
    assert "adsorb" in dog["dosage"].lower() or "tubing" in dog["dosage"].lower()
    assert "hypokalemia" in ins["contraindications"].lower()
    cat = ins["species_info"]["cat"]
    assert "0.25-0.5" in cat["dosage"]
    # Equine hyperlipemia use is documented (McKenzie 2011).
    assert "hyperlipemia" in ins["species_info"]["horse"]["dosage"].lower()


def test_imidocarb_piroplasmosis_doses_and_donkey_warning():
    """Imidocarb is the large-Babesia standard of care (6.6 mg/kg IM x2) and
    the USDA T. equi clearance drug (4 mg/kg q72h x4) — but donkeys are highly
    sensitive to that dose, small Babesia responds poorly, and cholinergic
    premedication is standard. All four facts must be on the entry."""
    imi = next((d for d in DRUGS if d["id"] == "imidocarb"), None)
    assert imi is not None
    dog = imi["species_info"]["dog"]
    assert "6.6 mg/kg" in dog["dosage"]
    assert "gibsoni" in dog["dosage"]  # small Babesia responds poorly
    assert "atropine" in dog.get("notes", "").lower()
    horse = imi["species_info"]["horse"]
    assert "4 mg/kg" in horse["dosage"]
    assert "donkey" in horse.get("notes", "").lower()
    assert "ロバ" in horse.get("notes_ja", "")


def test_heavy_metal_antidote_set_complete():
    """With succimer (DMSA) and dimercaprol (BAL) added, every classic
    heavy-metal chelator the disease DB references is carried: CaEDTA (lead),
    DMSA (avian lead/zinc, narrow margin), penicillamine (copper), BAL
    (arsenic; iron contraindication). Guards the avian overdose ceiling and
    the BAL-iron prohibition."""
    index = {d["id"]: d for d in DRUGS}
    for chelator in ("calcium_edta", "succimer", "penicillamine", "dimercaprol"):
        assert chelator in index, f"{chelator} missing"
    dmsa = index["succimer"]
    bird = dmsa["species_info"]["bird"]
    assert "25-35 mg/kg" in bird["dosage"]
    assert "80 mg/kg" in bird.get("notes", "")  # avian death threshold
    bal = index["dimercaprol"]
    contra = bal["contraindications"].lower()
    assert "iron" in contra and "cadmium" in contra
    interactions = " ".join(i["drug"].lower() for i in bal["drug_interactions"])
    assert "iron" in interactions


def test_batch35_species_toxicity_gates():
    """Species-specific safety gates: albendazole is not for routine feline
    use (aplastic anemia), enilconazole is not licensed for cats (grooming
    ingestion), and oseltamivir must not be presented as a canine parvo drug
    (Savigny 2010 showed no significant benefit)."""
    index = {d["id"]: d for d in DRUGS}
    alb_cat = index["albendazole"]["species_info"]["cat"]
    assert alb_cat["safe"] is False
    assert "fenbendazole" in alb_cat["dosage"].lower()
    enil_cat = index["enilconazole"]["species_info"]["cat"]
    assert enil_cat["safe"] is False
    assert "grooming" in enil_cat["dosage"].lower() or "lime sulfur" in enil_cat["dosage"].lower()
    osel_dog = index["oseltamivir"]["species_info"]["dog"]
    assert osel_dog["safe"] is False
    assert "parvo" in osel_dog["dosage"].lower()
    # Rabbit albendazole stays second-line to fenbendazole for E. cuniculi.
    alb_rab = index["albendazole"]["species_info"]["rabbit"]
    assert "フェンベンダゾール" in alb_rab["dosage_ja"]


def test_katakana_variant_aliases_resolve_in_text_matcher():
    """Treatment texts use legitimate katakana spelling variants that differ
    from the formulary's canonical name_ja (64 occurrences of デキサメサゾン
    alone). The keyword index must resolve them — and the new batch-35 agents
    — so the related-drug chips under treatment protocols actually appear."""
    from api.drug_dictionary import find_drugs_in_text

    cases = [
        ("デキサメサゾン 0.1 mg/kg IV", "dexamethasone"),
        ("ニスタチン 300,000 IU/kg PO", "nystatin"),
        ("シルバースルファジアジンクリーム塗布", "silver_sulfadiazine"),
        ("スルファサラジン 20 mg/kg PO", "sulfasalazine"),
        ("エチレングリコール中毒にはフォメピゾール", "fomepizole"),
        ("チアマゾール 2.5 mg PO q12h", "methimazole"),
        ("プロカインペニシリンG 42,000 IU/kg SC", "penicillin_g"),
        ("プラリドキシム 20 mg/kg IM", "pralidoxime"),
        ("2-PAM 20 mg/kg IM q8-12h", "pralidoxime"),
        ("レギュラーインスリン 0.1 U/kg/h CRI", "insulin_regular"),
        ("イミドカルブ 6.6 mg/kg IM", "imidocarb"),
        ("トリアムシノロン関節内注射", "triamcinolone"),
        ("DMSA 30 mg/kg PO", "succimer"),
        ("シドフォビル点眼 q12h", "cidofovir_ophthalmic"),
        ("フルルビプロフェン点眼", "flurbiprofen_ophthalmic"),
        ("イドクスウリジン0.1%点眼", "idoxuridine_ophthalmic"),
        ("セレコキシブ 10-20 mg/kg PO q24h", "celecoxib"),
    ]
    for text, expected_id in cases:
        ids = [d["id"] for d in find_drugs_in_text(text)]
        assert expected_id in ids, f"{text!r} did not resolve to {expected_id} (got {ids})"


def test_ja_form_suffix_and_combination_stems_resolve_in_text_matcher():
    """2026-08 4th sweep: treatment texts cite drugs without the formulary's
    dose-form/salt suffixes (オフロキサシン点眼 → 「オフロキサシン 1滴」,
    キニジン硫酸塩 → 「キニジン 22 mg/kg」) and cite one half of ・-joined
    combinations (トリメトプリム・スルファメトキサゾール). Before the suffix-strip
    and ・-split index rules 900+ treatment references — 732 for ペニシリン
    alone — never surfaced a related-drug chip although the drug was carried."""
    from api.drug_dictionary import find_drugs_in_text

    cases = [
        ("ペニシリン禁忌（モルモット・チンチラ）", "penicillin_g"),
        ("オフロキサシン 1滴 q6h", "ofloxacin_ophthalmic"),
        ("カルニチン 50 mg/kg PO", "l_carnitine"),
        ("チモロール 1滴 q12h", "timolol_ophthalmic"),
        ("シスプラチン化学療法", "cisplatin_injectable"),
        ("ナタマイシン点眼を頻回投与", "natamycin_ophthalmic"),
        ("リュープロレリン 700 μg/kg IM", "leuprolide"),
        ("スルファメトキサゾール 15 mg/kg", "trimethoprim_sulfa"),
        ("ピペラシリン 40 mg/kg IV", "piperacillin_tazobactam"),
        ("イミペネム 5 mg/kg SC", "imipenem_cilastatin"),
        ("キニジン 22 mg/kg NGT q2h", "quinidine"),
        ("ダルベポエチン 1 μg/kg SC 週1回", "darbepoetin"),
        ("ダーベポエチン投与", "darbepoetin"),
        ("アルブテロール吸入", "salbutamol"),
        ("ビタミンB1 25 mg/kg IM", "thiamine_b1"),
    ]
    for text, expected_id in cases:
        ids = [d["id"] for d in find_drugs_in_text(text)]
        assert expected_id in ids, f"{text!r} did not resolve to {expected_id} (got {ids})"

    # Precision guards: generic words must NOT surface chips.
    for text, forbidden in [
        ("ジョイントサポートを推奨", "ecvn_for_joint"),
        ("アンチオキシダント療法", "ecvn_for_antioxidant"),
        ("ビタミンB1欠乏", "vitamin_b12"),  # B1 text must never chip the B12 entry
    ]:
        ids = [d["id"] for d in find_drugs_in_text(text)]
        assert forbidden not in ids, f"{text!r} wrongly resolved to {forbidden}"


def test_enoxaparin_present_with_anti_xa_based_dosing():
    """Batch 36: 13 DIC/thromboembolism disease entries instruct enoxaparin with
    explicit doses, but the formulary carried only UFH and dalteparin. The entry
    must exist with the anti-Xa-based canine/feline regimens (Lunsford 2009 /
    Alwood 2007) and the hypocoagulable-DIC contraindication."""
    from api.drug_dictionary import find_drugs_in_text, get_drug_by_id

    d = get_drug_by_id("enoxaparin")
    assert d is not None, "enoxaparin missing from formulary"
    dog = d["species_info"]["dog"]
    cat = d["species_info"]["cat"]
    assert "0.8 mg/kg" in dog["dosage"] and "q6h" in dog["dosage"]
    assert "1.25 mg/kg" in cat["dosage"]
    for sp in ("dog", "cat", "horse", "rabbit"):
        info = d["species_info"][sp]
        assert info.get("dosage") and info.get("dosage_ja"), f"enoxaparin {sp} dosing incomplete"
    assert "DIC" in d["contraindications"]
    # The treatment texts' own wording must resolve to the new entry.
    ids = [x["id"] for x in find_drugs_in_text("エノキサパリン 0.8-1 mg/kg SC q12h、抗Xaモニタ")]
    assert "enoxaparin" in ids


def test_batch37_taurine_calcitonin_ampicillin_sulbactam():
    """Batch 37 (2026-08 5th referenced-but-absent sweep): taurine was the most
    referenced absent agent in the formulary's own treatment texts (768
    references — feline taurine-deficiency DCM's definitive therapy, Pion 1987);
    salmon calcitonin is cited with doses in rabbit/bird hypervitaminosis-D
    entries; ampicillin-sulbactam is the named empirical sepsis antibiotic in
    the parvo/panleukopenia protocols."""
    from api.drug_dictionary import find_drugs_in_text, get_drug_by_id

    tau = get_drug_by_id("taurine")
    assert tau is not None, "taurine missing from formulary"
    assert "250" in tau["species_info"]["cat"]["dosage"] and "q12h" in tau["species_info"]["cat"]["dosage"]
    assert "500" in tau["species_info"]["dog"]["dosage"]
    for sp in ("cat", "dog", "ferret", "guinea_pig"):
        info = tau["species_info"][sp]
        assert info.get("dosage") and info.get("dosage_ja"), f"taurine {sp} dosing incomplete"

    cal = get_drug_by_id("calcitonin_salmon")
    assert cal is not None, "calcitonin missing from formulary"
    assert "4-6 IU/kg" in cal["species_info"]["dog"]["dosage"]
    # Reptile NSHP: giving calcitonin before calcium correction is fatal —
    # the normocalcemia precondition must be stated (Mader 3rd ed).
    rep = cal["species_info"]["reptile"]
    assert "50 IU/kg" in rep["dosage"] and "normaliz" in rep["dosage"].lower()
    assert "テタニー" in rep["notes_ja"]
    assert "Hypocalcemia" in cal["contraindications"]

    amp = get_drug_by_id("ampicillin_sulbactam")
    assert amp is not None, "ampicillin-sulbactam missing from formulary"
    assert "22" in amp["species_info"]["dog"]["dosage"] and "q8h" in amp["species_info"]["dog"]["dosage"]
    # Hindgut fermenters: penicillins cause fatal enterotoxemia.
    for sp in ("rabbit", "guinea_pig", "hamster", "chinchilla"):
        assert amp["species_info"][sp]["safe"] is False, f"{sp} must be flagged unsafe"

    # The treatment texts' own wording must resolve to the new entries.
    ids = [x["id"] for x in find_drugs_in_text("タウリン補充 250-500 mg/cat PO q12h")]
    assert "taurine" in ids
    ids = [x["id"] for x in find_drugs_in_text("カルシトニン 4-6 IU/kg SC BID（重度高Ca血症時）")]
    assert "calcitonin_salmon" in ids
    ids = [x["id"] for x in find_drugs_in_text("アンピシリン・スルバクタム 22-30 mg/kg IV q8h")]
    assert "ampicillin_sulbactam" in ids


def test_batch38_pancrelipase_benzbromarone_metformin():
    """Batch 38 (2026-08 6th referenced-but-absent sweep): the dog/cat EPI
    flagship entries prescribe powdered pancreatic enzyme with a dose
    (1 tsp/10kg/meal) yet no PERT product was carried; the avian/reptile gout
    protocols name benzbromarone 5 mg/kg PO q24h; the horse EMS/insulin
    resistance entries name metformin 15-30 mg/kg (Durham 2008)."""
    from api.drug_dictionary import find_drugs_in_text, get_drug_by_id

    pert = get_drug_by_id("pancrelipase")
    assert pert is not None, "pancrelipase missing from formulary"
    assert "1 tsp" in pert["species_info"]["dog"]["dosage"]
    # Cobalamin co-supplementation is near-universal in EPI — must be stated.
    assert "B12" in pert["species_info"]["cat"]["notes_ja"]
    for sp in ("dog", "cat"):
        info = pert["species_info"][sp]
        assert info.get("dosage") and info.get("dosage_ja"), f"pancrelipase {sp} dosing incomplete"

    benz = get_drug_by_id("benzbromarone")
    assert benz is not None, "benzbromarone missing from formulary"
    assert "5 mg/kg" in benz["species_info"]["bird"]["dosage"]
    # Auto-extrapolation must reach the bird/reptile sub-species views.
    for sp in ("parakeet", "parrot", "reptile", "tortoise", "snake", "lizard"):
        assert sp in benz["species_info"], f"benzbromarone missing {sp} extrapolation"
    # Hydration precondition (urate deposition risk) must be stated.
    assert "水和" in benz["species_info"]["bird"]["notes_ja"]

    met = get_drug_by_id("metformin")
    assert met is not None, "metformin missing from formulary"
    horse = met["species_info"]["horse"]
    assert "15-30 mg/kg" in horse["dosage"] and "Durham" in horse["dosage"]
    # Canine diabetes is insulin-dependent — metformin must be flagged
    # not-indicated, and renal-impairment lactic acidosis must be warned.
    assert met["species_info"]["dog"]["safe"] is False
    assert "乳酸アシドーシス" in met["contraindications_ja"]

    # The treatment texts' own wording must resolve to the new entries.
    ids = [x["id"] for x in find_drugs_in_text("粉末状膵酵素（パンクレアチン/パンクレリパーゼ）を毎食に混合")]
    assert "pancrelipase" in ids
    ids = [x["id"] for x in find_drugs_in_text("ベンズブロマロン 5 mg/kg PO q24h（試験的）")]
    assert "benzbromarone" in ids
    ids = [x["id"] for x in find_drugs_in_text("メトホルミン30 mg/kg PO q12h（インスリン抵抗性改善）")]
    assert "metformin" in ids
    # Precision guard: the diagnostic phrase 膵酵素上昇 (elevated pancreatic
    # enzymes — a zinc-toxicosis lab finding) must NOT chip the PERT product.
    ids = [x["id"] for x in find_drugs_in_text("膵酵素上昇（>2 ppm = 中毒）")]
    assert "pancrelipase" not in ids


def test_katakana_sweep6_variant_aliases_resolve_in_text_matcher():
    """2026-08 sweep #6: treatment texts cite nine formulary drugs by bare or
    variant katakana spellings the canonical name never reduces to (フルニキシン
    198 refs, アセチルシステイン 131, デキストロース 81, リファンピシン 39,
    インターフェロンω 44, …). Each must resolve to its canonical entry."""
    from api.drug_dictionary import find_drugs_in_text

    cases = {
        "フルニキシン 1.1 mg/kg IV q12h": "flunixin",
        "アセチルシステイン 70 mg/kg PO": "n_acetylcysteine",
        "デキストロース 2.5%を輸液に添加": "dextrose_50",
        "アンホテリシンB リポソーム製剤": "amphotericin_b",
        "リファンピシン 5 mg/kg PO q12h": "rifampin",
        "サルファジメトキシン 50 mg/kg": "sulfadimethoxine",
        "インターフェロンω 1 MU/kg SC": "interferon_omega",
        "インターフェロンオメガ皮下投与": "interferon_omega",
        "ピリメサミン 0.25 mg/kg": "pyrimethamine",
        "α-カソゼピン 15 mg/kg": "alpha_casozepine",
    }
    for text, want in cases.items():
        ids = [x["id"] for x in find_drugs_in_text(text)]
        assert want in ids, f"{text!r} must resolve to {want}, got {ids}"


def test_no_garbled_pradofloxacin_or_sulbactam_typo_in_disease_json():
    """The feline mycobacteriosis protocol carried a garbled drug name
    (プラジコフロキサシン — a corruption of pradofloxacin prefixed with a
    nonsensical 'not praziquantel' clause), and the parvo/panleukopenia sepsis
    protocols misspelled sulbactam as サルバクタム. Both are corrected to real,
    resolvable formulary names; neither corruption may return."""
    import json
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    raw = (root / "diseases_all_species.json").read_text(encoding="utf-8")
    assert "プラジコフロキサシン" not in raw
    assert "サルバクタム" not in raw  # correct spelling is スルバクタム
    assert "プラジカンテルではなく" not in raw

    data = json.loads(raw)
    myco = [e for e in data if e.get("species") == "Cat" and "Mycobacterial Infection" in (e.get("name") or "")]
    assert myco, "feline mycobacteriosis entry missing"
    assert "プラドフロキサシン" in myco[0]["treatment_ja"], (
        "ISFM triple therapy must name pradofloxacin (Gunn-Moore, JFMS 2013)"
    )

    # Same corruption existed in the cat species module.
    mod = (root / "api" / "species" / "cat_diseases.py").read_text(encoding="utf-8")
    assert "プラジコフロキサシン" not in mod
    assert "サルバクタム" not in mod


def test_batch39_protamine_hydrocortisone_hypertonic_saline():
    """2026-08 sweep #7 (referenced-but-absent): the formulary's own heparin /
    enoxaparin / dalteparin entries name protamine as the reversal agent, the
    Addisonian-crisis protocols name hydrocortisone, and the shock/GDV/TBI
    protocols name 7.2% hypertonic saline — yet none was carried. All three
    must exist with complete bilingual dosing and their defining safety facts."""
    from api.drug_dictionary import find_drugs_in_text, get_drug_by_id

    protamine = get_drug_by_id("protamine_sulfate")
    assert protamine is not None, "protamine_sulfate missing from formulary"
    dog = protamine["species_info"]["dog"]
    assert "100 IU" in dog["dosage"], "protamine must be dosed per 100 IU heparin"
    assert "60%" in protamine["mechanism"], "partial LMWH reversal (~60%) must be stated"
    assert "緩徐" in dog["dosage_ja"] or "緩徐" in dog["notes_ja"], (
        "slow-injection requirement (hypotension/anaphylactoid risk) must be in Japanese text"
    )

    hydro = get_drug_by_id("hydrocortisone_succinate")
    assert hydro is not None, "hydrocortisone_succinate missing from formulary"
    dd = hydro["species_info"]["dog"]
    assert "0.5 mg/kg/h" in dd["dosage"], "Addisonian-crisis CRI dose (Lathan 2018) required"
    assert "ACTH" in dd["notes"], "assay cross-reactivity note (draw ACTH stim first) required"

    hts = get_drug_by_id("hypertonic_saline")
    assert hts is not None, "hypertonic_saline missing from formulary"
    assert "4-7 mL/kg" in hts["species_info"]["dog"]["dosage"], "canine shock dose (Silverstein)"
    assert "2-4 mL/kg" in hts["species_info"]["cat"]["dosage"], "feline dose is lower"
    assert "脱水" in hts["contraindications_ja"], (
        "dehydration contraindication (interstitial water is the volume source) required"
    )

    # All three resolve from treatment-text spellings.
    for text, want in {
        "プロタミンで部分中和": "protamine_sulfate",
        "ヒドロコルチゾン 0.5 mg/kg/h CRI": "hydrocortisone_succinate",
        "高張食塩水 4 mL/kg を5-10分で静注": "hypertonic_saline",
    }.items():
        ids = [x["id"] for x in find_drugs_in_text(text)]
        assert want in ids, f"{text!r} must resolve to {want}, got {ids}"


def test_katakana_sweep7_variant_aliases_resolve_in_text_matcher():
    """2026-08 sweep #7: treatment texts cite six formulary drugs by variant
    spellings the canonical name never reduces to (ドーパミン 19 refs,
    重炭酸ナトリウム, フィトナジオン, カルシウムグルコネート, ウルソジオール,
    炭酸カルシウム 13 refs). Each must resolve to its canonical entry."""
    from api.drug_dictionary import find_drugs_in_text

    cases = {
        "ドーパミン 5 µg/kg/分 CRI": "dopamine",
        "重炭酸ナトリウム 1 mEq/kg 緩徐静注": "sodium_bicarbonate",
        "フィトナジオン 2.5 mg/kg SC": "vitamin_k1",
        "カルシウムグルコネート 10%液": "calcium_gluconate",
        "ウルソジオール 10-15 mg/kg PO": "ursodiol",
        "炭酸カルシウム 50-100 mg/kg PO SID": "calcium_supplement_reptile",
    }
    for text, want in cases.items():
        ids = [x["id"] for x in find_drugs_in_text(text)]
        assert want in ids, f"{text!r} must resolve to {want}, got {ids}"


def test_digit_boundary_guard_b1_alias_never_chips_b12_text():
    """The ビタミンB1→thiamine alias used plain substring matching, so every
    ビタミンB12 mention spuriously chipped the thiamine entry. A keyword ending
    in a digit must not match inside a longer number; the true B1 spelling must
    still resolve."""
    from api.drug_dictionary import find_drugs_in_text

    b12_ids = [x["id"] for x in find_drugs_in_text("ビタミンB12 250 μg SC 週1回")]
    assert "thiamine_b1" not in b12_ids, f"B12 text must not chip thiamine, got {b12_ids}"
    assert "vitamin_b12" in b12_ids

    b1_ids = [x["id"] for x in find_drugs_in_text("ビタミンB1（チアミン）25-50 mg IM")]
    assert "thiamine_b1" in b1_ids, f"true B1 text must still resolve, got {b1_ids}"


def test_batch40_ethambutol_and_dihydrostreptomycin():
    """2026-08 sweep #8 (referenced-but-absent): the avian/reptile/dog/cat
    mycobacteriosis multi-drug protocols name ethambutol (13 disease entries),
    and the classic canine brucellosis regimen names dihydrostreptomycin
    10 mg/kg IM (9 entries) — yet neither was carried in the formulary."""
    from api.drug_dictionary import find_drugs_in_text, get_drug_by_id

    etb = get_drug_by_id("ethambutol")
    assert etb is not None, "ethambutol missing from formulary"
    for sp in ("dog", "cat", "bird", "reptile"):
        info = etb["species_info"][sp]
        assert info["safe"] is True
        assert info["dosage"].strip() and info["dosage_ja"].strip()
    # Never monotherapy — the defining resistance-prevention fact.
    assert "単剤" in etb["contraindications_ja"]
    assert "monotherapy" in etb["contraindications"].lower()
    # Avian dosing per Carpenter: 20-30 mg/kg within multi-drug protocols.
    assert "20-30 mg/kg" in etb["species_info"]["bird"]["dosage"]

    dsm = get_drug_by_id("dihydrostreptomycin")
    assert dsm is not None, "dihydrostreptomycin missing from formulary"
    dog = dsm["species_info"]["dog"]
    assert "10 mg/kg" in dog["dosage"] and "doxycycline" in dog["dosage"].lower()
    assert "ドキシサイクリン" in dog["dosage_ja"]
    # Defining safety fact: the most vestibulotoxic aminoglycoside.
    assert "前庭毒性" in dsm["side_effects_ja"]
    assert "vestibulotoxic" in dsm["side_effects"].lower()

    # Both resolve from actual treatment-text spellings, including the
    # bare-streptomycin form the brucellosis protocols use.
    for text, want in {
        "エタンブトール 30 mg/kg PO q24h": "ethambutol",
        "ジヒドロストレプトマイシン（10 mg/kg IM q12h×7日）": "dihydrostreptomycin",
        "ストレプトマイシン併用": "dihydrostreptomycin",
    }.items():
        ids = [x["id"] for x in find_drugs_in_text(text)]
        assert want in ids, f"{text!r} must resolve to {want}, got {ids}"


def test_no_garbled_ethiobutol_in_disease_content():
    """The avian TB triple-therapy protocols carried a garbled drug name
    エチオブトール (a corruption of エタンブトール / ethambutol) in the bird and
    parrot modules and the JSON overlay. The corruption may not return."""
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    for rel in (
        "diseases_all_species.json",
        "api/species/bird_diseases.py",
        "api/species/parrot_diseases.py",
        "scripts/template_elimination/template_content_library.py",
    ):
        raw = (root / rel).read_text(encoding="utf-8")
        assert "エチオブトール" not in raw, f"garbled ethambutol name found in {rel}"


def test_sweep8_variant_aliases_resolve():
    """アティパメゾール (ティ variant of アチパメゾール, emergency-kit texts) and
    bare ミルベマイシン (canonical name carries the オキシム suffix) must resolve
    through the katakana variant-alias registry."""
    from api.drug_dictionary import find_drugs_in_text

    cases = {
        "緊急機材：アティパメゾール（α2拮抗薬）": "atipamezole",
        "ミルベマイシンA錠 0.5-1 mg/kg PO 月1回": "milbemycin_oxime",
    }
    for text, want in cases.items():
        ids = [x["id"] for x in find_drugs_in_text(text)]
        assert want in ids, f"{text!r} must resolve to {want}, got {ids}"


def test_batch41_leishmania_first_line_pair_present():
    """Batch 41 (2026-08 9th referenced-but-absent sweep): the canine
    leishmaniosis entries prescribe both LeishVet first-line drugs with doses
    (miltefosine 2 mg/kg PO q24h ×28d; meglumine antimoniate SC 4-8 weeks,
    each + allopurinol) yet neither was carried."""
    from api.drug_dictionary import find_drugs_in_text, get_drug_by_id

    mil = get_drug_by_id("miltefosine")
    assert mil is not None, "miltefosine missing from formulary"
    dog = mil["species_info"]["dog"]
    assert "2 mg/kg" in dog["dosage"] and "28" in dog["dosage"]
    # Always combined with allopurinol (monotherapy = resistance risk).
    assert "アロプリノール" in dog["dosage_ja"]
    # Teratogenicity + pregnant-owner handling warning must be stated.
    assert "催奇形" in mil["contraindications_ja"]

    meg = get_drug_by_id("meglumine_antimoniate")
    assert meg is not None, "meglumine antimoniate missing from formulary"
    dog = meg["species_info"]["dog"]
    assert dog.get("dosage") and dog.get("dosage_ja")
    # Renal assessment before use is the defining safety fact for antimonials.
    assert "腎" in dog["notes_ja"]

    # The treatment texts' own wording must resolve to the new entries.
    ids = [x["id"] for x in find_drugs_in_text("ミルテホシン 2 mg/kg PO q24h（28日）")]
    assert "miltefosine" in ids
    ids = [x["id"] for x in find_drugs_in_text("メグルミンアンチモン酸塩 100 mg/kg SC q24h")]
    assert "meglumine_antimoniate" in ids
    # Flunixin meglumine must not be shadowed by the new antimonial alias.
    ids = [x["id"] for x in find_drugs_in_text("フルニキシン・メグルミン 1.1 mg/kg IV q12h")]
    assert "flunixin" in ids and "meglumine_antimoniate" not in ids


def test_batch41_hivig_single_dose_and_thromboprophylaxis():
    """hIVIG is referenced ~30-40 times as the IMHA/ITP refractory rescue
    (0.5-1 g/kg IV). Single-use (anti-human-protein sensitization) and
    thromboembolism cautions are the class-defining safety facts."""
    from api.drug_dictionary import find_drugs_in_text, get_drug_by_id

    ivig = get_drug_by_id("human_ivig")
    assert ivig is not None, "hIVIG missing from formulary"
    dog = ivig["species_info"]["dog"]
    assert "0.5-1.5 g/kg" in dog["dosage"]
    # Single infusion only — re-exposure anaphylaxis risk must be stated.
    assert "単回" in dog["dosage_ja"] or "単回" in dog["notes_ja"]
    assert "アナフィラキシー" in ivig["contraindications_ja"]
    # IMHA patients are hypercoagulable — thromboprophylaxis must be advised.
    assert "血栓" in dog["notes_ja"]

    ids = [x["id"] for x in find_drugs_in_text("ヒト免疫グロブリン（IVIG）0.5-1 g/kg IV 単回")]
    assert "human_ivig" in ids


def test_batch41_interferon_alpha_does_not_shadow_omega():
    """Human IFN-α (~33 refs: avian PBFD adjunct, feline retrovirus oral
    low-dose) was absent — only feline IFN-ω was carried. The new aliases
    must not capture interferon-omega references."""
    from api.drug_dictionary import find_drugs_in_text, get_drug_by_id

    ifn = get_drug_by_id("interferon_alpha")
    assert ifn is not None, "interferon alpha missing from formulary"
    cat = ifn["species_info"]["cat"]
    assert "30 IU" in cat["dosage"]
    # Neutralizing-antibody limitation of high-dose parenteral use.
    assert "中和抗体" in cat["dosage_ja"]
    # Omega preference where licensed must be stated.
    assert "オメガ" in cat["notes_ja"] or "ω" in cat["notes_ja"]
    bird = ifn["species_info"]["bird"]
    assert bird.get("dosage") and bird.get("dosage_ja")

    ids = [x["id"] for x in find_drugs_in_text("組換えαインターフェロン 1-10万IU/kg SC q24h")]
    assert "interferon_alpha" in ids
    # Omega references must still resolve to interferon_omega, not alpha.
    ids = [x["id"] for x in find_drugs_in_text("インターフェロンオメガ 1 MU/kg SC q48h")]
    assert "interferon_omega" in ids and "interferon_alpha" not in ids


class TestBatch42IsotonicSalineAndCholecalciferol:
    """2026-08 10th referenced-but-absent sweep: 0.9% normal saline (293
    treatment references — the formulary carried LRS/Normosol and 7.2%
    hypertonic but no isotonic saline) and cholecalciferol/vitamin D3 (96
    references — only the active metabolite calcitriol was carried)."""

    def test_normal_saline_present_with_species_dosing_and_never_confused_with_hypertonic(self):
        from api.drug_dictionary import find_drugs_in_text, get_drug_by_id

        ns = get_drug_by_id("normal_saline")
        assert ns is not None
        for sp in ("dog", "cat", "horse", "rabbit", "bird", "reptile"):
            info = ns["species_info"][sp]
            assert info.get("safe") is True
            assert (info.get("dosage") or "").strip()
            assert (info.get("dosage_ja") or "").strip()
        # class-defining safety facts: chloride-rich/acidifying, K-free,
        # slow correction of chronic hyponatremia
        assert "hyperchloremic" in ns["side_effects"].lower()
        assert "0.5 mEq/L" in ns["contraindications"]
        # the 7.2% small-volume fluid must never be conflated with isotonic
        assert any(
            i.get("drug") == "Hypertonic Saline 7.2-7.5%" and i.get("severity") == "major"
            for i in ns["drug_interactions"]
        )
        # treatment-text resolution (saline nebulization protocols)
        ids = [h["id"] for h in find_drugs_in_text("ネブライザー 生理食塩水 q4-6h")]
        assert "normal_saline" in ids and "hypertonic_saline" not in ids
        # and the hypertonic complaint text still resolves to hypertonic only
        ids2 = [h["id"] for h in find_drugs_in_text("高張食塩水 4 mL/kg IV")]
        assert "hypertonic_saline" in ids2 and "normal_saline" not in ids2

    def test_cholecalciferol_present_with_narrow_margin_warnings(self):
        from api.drug_dictionary import find_drugs_in_text, get_drug_by_id

        d = get_drug_by_id("cholecalciferol")
        assert d is not None
        # calcitriol preferred for titratability; reptile NSHP husbandry-first
        assert "カルシトリオール" in d["species_info"]["dog"]["dosage_ja"]
        assert "UV-B" in d["species_info"]["reptile"]["notes"]
        # rodenticide-syndrome warning (same molecule)
        assert "rodenticide" in d["side_effects"].lower() or "rodenticide" in d["contraindications"].lower()
        ids = [h["id"] for h in find_drugs_in_text("ビタミンD3（コレカルシフェロール）4,000-6,000 IU/kg/日 PO")]
        assert "cholecalciferol" in ids
        # the numeric-boundary guard must keep B12 references clean
        ids_b12 = [h["id"] for h in find_drugs_in_text("ビタミンB12 250 μg SC 週1回")]
        assert "cholecalciferol" not in ids_b12

    def test_variant_aliases_resolve_zinc_salts_tmp_sulfa_and_bare_ringer(self):
        from api.drug_dictionary import find_drugs_in_text

        cases = {
            "硫酸亜鉛 10 mg/kg/日 PO（食事と別に）": "zinc_acetate",
            "グルコン酸亜鉛に変更可": "zinc_acetate",
            "TMP-スルファ 15-30 mg/kg 経口 12時間ごと": "trimethoprim_sulfa",
            "TMP/S 30 mg/kg PO q12h": "trimethoprim_sulfa",
            "4°Cリンゲル液IVで冷却輸液": "lactated_ringers",
        }
        for text, target in cases.items():
            ids = [h["id"] for h in find_drugs_in_text(text)]
            assert target in ids, f"{text!r} -> {ids}"


class TestBatch43CytarabineImiquimodAndMmfAlias:
    """2026-08 11th referenced-but-absent sweep: cytarabine (8 dosed MUO
    references) and imiquimod 5% cream (5 dosed references — equine sarcoid /
    aural plaques, feline SCC in situ) were absent; mycophenolate turned out
    to be present already, so only its bare acid-stem alias was added."""

    def test_cytarabine_present_with_muo_cycle_and_safe_handling(self):
        from api.drug_dictionary import find_drugs_in_text, get_drug_by_id

        d = get_drug_by_id("cytarabine")
        assert d is not None, "cytarabine missing from formulary"
        dog = d["species_info"]["dog"]
        # the exact MUO cycle VetDict's own neurology entries reference
        assert "50 mg/m²" in dog["dosage"] and "q12h" in dog["dosage"]
        assert "50 mg/m²" in dog["dosage_ja"]
        # blood-brain barrier property is the defining reason this drug exists here
        assert "blood-brain" in d["mechanism"].lower()
        assert "血液脳関門" in d["mechanism_ja"]
        # myelosuppression nadir + cytotoxic handling must be stated
        assert "5-7" in dog["notes"] or "5-7" in d["side_effects"]
        assert "手袋" in dog["notes_ja"] or "手袋" in d["contraindications_ja"]
        cat = d["species_info"]["cat"]
        assert (cat.get("dosage") or "").strip() and (cat.get("dosage_ja") or "").strip()
        ids = [h["id"] for h in find_drugs_in_text("シタラビン（Ara-C）50 mg/m² SC q12h × 2日間、4週毎")]
        assert "cytarabine" in ids

    def test_imiquimod_present_for_equine_sarcoid_and_feline_scc_in_situ(self):
        from api.drug_dictionary import find_drugs_in_text, get_drug_by_id

        d = get_drug_by_id("imiquimod")
        assert d is not None, "imiquimod missing from formulary"
        horse = d["species_info"]["horse"]
        assert "サルコイド" in horse["dosage_ja"]
        # painful application / sedation caveat (Torres 2010) must be stated
        assert "鎮静" in horse["dosage_ja"] or "鎮静" in horse["notes_ja"]
        cat = d["species_info"]["cat"]
        # grooming-ingestion prevention is the defining feline safety fact
        assert "エリザベスカラー" in cat["dosage_ja"] or "エリザベスカラー" in cat["notes_ja"]
        ids = [h["id"] for h in find_drugs_in_text("イミキモド5%クリーム外用q48h×数ヶ月")]
        assert "imiquimod" in ids

    def test_bare_mycophenolic_acid_resolves_to_existing_entry(self):
        from api.drug_dictionary import find_drugs_in_text, get_drug_by_id

        # MMF itself must remain a single entry (no duplicate card)
        assert get_drug_by_id("mycophenolate") is not None
        assert get_drug_by_id("mycophenolate_mofetil") is None
        # the SARDS entry cites the bare acid stem without モフェチル
        ids = [h["id"] for h in find_drugs_in_text("IVIg 0.5 g/kg IV × 1回 + ミコフェノール酸 20 mg/kg PO q12h")]
        assert "mycophenolate" in ids
        # and the full spelling still resolves to the same entry
        ids2 = [h["id"] for h in find_drugs_in_text("ミコフェノール酸モフェチル（MMF）10 mg/kg PO q12h")]
        assert ids2.count("mycophenolate") == 1 and "mycophenolate_mofetil" not in ids2


class TestBatch44SimethiconeTrientineOlopatadine:
    """2026-08 12th referenced-but-absent sweep: simethicone (37 dosed GI-stasis
    references across 6 herbivore/small-mammal species), trientine (the named
    second-line copper chelator in the canine copper-hepatopathy entries) and
    olopatadine 0.1% ophthalmic were absent; DOCP turned out to be present
    already (desoxycorticosterone) — only the bare acronym failed to resolve,
    fixed via _KATAKANA_VARIANT_ALIASES."""

    def test_simethicone_present_with_herbivore_stasis_dosing(self):
        from api.drug_dictionary import find_drugs_in_text, get_drug_by_id

        d = get_drug_by_id("simethicone")
        assert d is not None, "simethicone missing from formulary"
        # luminal-only action is the defining safety fact
        assert "not absorbed" in d["mechanism"].lower()
        assert "吸収されない" in d["mechanism_ja"]
        for sp in ("rabbit", "guinea_pig", "chinchilla", "hamster", "dog", "cat"):
            info = d["species_info"][sp]
            assert (info.get("dosage") or "").strip() and (info.get("dosage_ja") or "").strip(), sp
        # adjunct-not-substitute + obstruction caveat must be stated
        assert "閉塞" in d["contraindications_ja"]
        ids = [h["id"] for h in find_drugs_in_text("ガス軽減：シメチコン40-50mg/kg PO q6-8h")]
        assert "simethicone" in ids

    def test_trientine_present_as_second_line_copper_chelator(self):
        from api.drug_dictionary import find_drugs_in_text, get_drug_by_id

        d = get_drug_by_id("trientine")
        assert d is not None, "trientine missing from formulary"
        dog = d["species_info"]["dog"]
        assert "10-15 mg/kg" in dog["dosage"] and "10-15 mg/kg" in dog["dosage_ja"]
        # empty-stomach administration and penicillamine relationship are defining facts
        assert "空腹時" in dog["dosage_ja"]
        assert "ペニシラミン" in d["mechanism_ja"]
        interactions = {i["drug"].lower(): i for i in d["drug_interactions"]}
        assert any("zinc" in k for k in interactions)
        ids = [h["id"] for h in find_drugs_in_text("トリエンチン 10-15 mg/kg PO q12h（空腹時）")]
        assert "trientine" in ids

    def test_olopatadine_present_and_feline_herpes_caveat(self):
        from api.drug_dictionary import find_drugs_in_text, get_drug_by_id

        d = get_drug_by_id("olopatadine_ophthalmic")
        assert d is not None, "olopatadine missing from formulary"
        cat = d["species_info"]["cat"]
        # FHV-1-first caveat is the defining feline safety fact
        assert "FHV-1" in (cat.get("notes") or "") or "FHV-1" in (cat.get("notes_ja") or "")
        ids = [h["id"] for h in find_drugs_in_text("オロパタジン0.1%点眼 q12h（抗ヒスタミン+マスト細胞安定化）")]
        assert "olopatadine_ophthalmic" in ids

    def test_docp_acronym_resolves_to_existing_entry(self):
        from api.drug_dictionary import find_drugs_in_text, get_drug_by_id

        assert get_drug_by_id("desoxycorticosterone") is not None
        ids = [h["id"] for h in find_drugs_in_text("長期：DOCP（2.2 mg/kg IM q25日）が鉱質コルチコイド第一選択")]
        assert "desoxycorticosterone" in ids


def test_sweep13_acronym_and_word_order_aliases_resolve():
    """2026-08 sweep #13: chelation/hepatoprotectant/fluid texts cite CaEDTA
    (51 refs), UDCA (41 refs), ヘタスターチ and the reversed word order
    カルシウムグルコン酸(塩) (21 refs) — none of which the canonical names
    reduce to, so the related-drug chips silently failed to resolve."""
    from api.drug_dictionary import find_drugs_in_text

    cases = {
        "キレート療法：CaEDTA 75 mg/kg IV slow q12h×5日": "calcium_edta",
        "UDCA 10-15 mg/kg PO q24h: 利胆作用": "ursodiol",
        "膠質液（ヘタスターチ 10-20 mL/kg/日）で循環血液量を回復": "hetastarch",
        "カルシウムグルコン酸23% 250-500 mL IV slow": "calcium_gluconate",
        "カルシウムグルコン酸塩100 mg/kg ICe q12h": "calcium_gluconate",
    }
    for text, expected in cases.items():
        ids = [h["id"] for h in find_drugs_in_text(text)]
        assert expected in ids, (text, ids)
    # precision guards: generic mentions must not produce chips
    for text in ("カルシウム補給を行う", "educated guess による経験的治療"):
        ids = [h["id"] for h in find_drugs_in_text(text)]
        assert "calcium_gluconate" not in ids and "ursodiol" not in ids, (text, ids)


class TestBatch45FinasterideOsateroneFilgrastim:
    """2026-08 14th referenced-but-absent sweep: the canine BPH entries dose
    finasteride and osaterone acetate verbatim, and 7 entries dose filgrastim
    (rhG-CSF 5 µg/kg SC q24h) — none existed in the formulary. The same sweep
    caught the tylosin mis-transliteration (チロシン = tyrosine, the amino
    acid; the antibiotic is タイロシン) in 6 dog/cat GI entries."""

    def test_finasteride_present_with_bph_dosing_and_teratogenic_warning(self):
        from api.drug_dictionary import find_drugs_in_text, get_drug_by_id

        d = get_drug_by_id("finasteride")
        assert d is not None, "finasteride missing from formulary"
        dog = d["species_info"]["dog"]
        assert "0.1-0.5 mg/kg" in dog["dosage"] and "0.1-0.5 mg/kg" in dog["dosage_ja"]
        # fertility preservation is the defining clinical fact vs castration
        assert "繁殖" in d["mechanism_ja"] or "精液" in d["mechanism_ja"]
        # teratogenicity / pregnant-handler warning is the defining safety fact
        assert "催奇形" in d["contraindications_ja"]
        assert d["species_info"]["cat"]["safe"] is False
        ids = [h["id"] for h in find_drugs_in_text("フィナステリド 0.1-0.5 mg/kg 経口 24時間ごと")]
        assert "finasteride" in ids
        ids_en = [h["id"] for h in find_drugs_in_text("Finasteride 0.1-0.5 mg/kg PO")]
        assert "finasteride" in ids_en

    def test_osaterone_present_with_seven_day_course_and_cortisol_caveat(self):
        from api.drug_dictionary import find_drugs_in_text, get_drug_by_id

        d = get_drug_by_id("osaterone")
        assert d is not None, "osaterone missing from formulary"
        dog = d["species_info"]["dog"]
        assert "0.25-0.5 mg/kg" in dog["dosage"] and "7" in dog["dosage"]
        assert "0.25-0.5 mg/kg" in dog["dosage_ja"] and "7日間" in dog["dosage_ja"]
        # transient ACTH/cortisol attenuation is the defining safety fact (SPC)
        assert "ACTH" in (dog.get("notes_ja") or "") or "コルチゾール" in (dog.get("notes_ja") or "")
        ids = [h["id"] for h in find_drugs_in_text("酢酸オサテロン（Ypozane 0.25-0.5 mg/kg PO 7日間）")]
        assert "osaterone" in ids

    def test_filgrastim_present_with_short_course_antibody_warning(self):
        from api.drug_dictionary import find_drugs_in_text, get_drug_by_id

        d = get_drug_by_id("filgrastim")
        assert d is not None, "filgrastim missing from formulary"
        for sp in ("dog", "cat", "ferret"):
            info = d["species_info"][sp]
            assert "5 µg/kg" in info["dosage"] or "5 μg/kg" in info["dosage"], sp
            assert (info.get("dosage_ja") or "").strip(), sp
        # heterologous-protein antibody formation → short course is the
        # defining safety fact for rhG-CSF in dogs and cats
        assert "抗体" in d["mechanism_ja"] and "抗体" in d["contraindications_ja"]
        ids = [h["id"] for h in find_drugs_in_text("G-CSF（フィルグラスチム5 μg/kg SC q24h）は急性好中球減少に有効")]
        assert "filgrastim" in ids
        # bare acronym in the parvo protocol must also resolve
        ids2 = [h["id"] for h in find_drugs_in_text("組換え犬G-CSF 5 µg/kg SC q24h（重度好中球減少）")]
        assert "filgrastim" in ids2
        # precision guard: GM-CSF is a different cytokine
        assert "filgrastim" not in [h["id"] for h in find_drugs_in_text("GM-CSF投与")]


def test_no_tyrosine_typo_for_tylosin_in_disease_content():
    """The antibiotic tylosin (タイロシン) was mis-transliterated as チロシン
    (tyrosine, the amino acid) in the dog IBD/EPI/SIBO/ARD/CCE and cat EPI
    entries — a wrong drug name a clinician would trip over. Legitimate
    tyrosine-kinase (チロシンキナーゼ) mentions must survive, as must the
    genuine tyrosine amino-acid supplement in the equine anhidrosis entry."""
    import re
    from pathlib import Path

    root = Path(__file__).resolve().parents[1]
    raw = (root / "diseases_all_species.json").read_text(encoding="utf-8")
    # any non-kinase チロシン immediately followed by a dose is the typo
    assert not re.search(r"チロシン(?!キナーゼ)[（(]?\s*[0-9]", raw), (
        "tylosin must be written タイロシン, not チロシン, in dose contexts"
    )
    assert "チロシン（タイロシン" not in raw

    for mod in ("dog_diseases.py", "cat_diseases.py"):
        src = (root / "api" / "species" / mod).read_text(encoding="utf-8")
        assert not re.search(r"チロシン(?!キナーゼ)", src), mod

    # tylosin itself must resolve so the corrected texts produce drug chips
    from api.drug_dictionary import find_drugs_in_text

    ids = [h["id"] for h in find_drugs_in_text("タイロシン（15-25 mg/kg PO q12h×6-8週）")]
    assert "tylosin" in ids


def test_sweep15_brand_paren_and_variant_aliases_resolve():
    """2026-08 sweep #15: treatment texts cite ProZinc (プロジンク, 41 refs),
    tiludronate by its standard transliteration (ティルドロネート — canonical
    name_ja uses チルドロン酸), sodium selenite for white-muscle disease, and
    the reversed word order 銀スルファジアジン (47 refs). ProZinc also exposed
    a systemic gap: brand aliases contained only in a name's parenthetical
    suffix were skipped by the brand merge, yet the keyword index strips
    parentheses — so they were unreachable in both search and text matching."""
    from api.drug_dictionary import find_drugs_in_text, search_drugs

    cases = {
        "プロジンク 0.5-1 IU/動物 SC q12hから開始": "insulin_pzi",
        "グラルギン（ランタス）0.25 U/kg SC q12h": "insulin_glargine",
        "ティルドロネート 1 mg/kg IV（ビスホスホネート）": "tiludronate",
        "セレン酸ナトリウム0.05-0.1 mg/kg IM単回": "selenium_vitamin_e",
        "クロルヘキシジン洗浄＋銀スルファジアジンクリーム塗布": "silver_sulfadiazine",
    }
    for text, expected in cases.items():
        ids = [h["id"] for h in find_drugs_in_text(text)]
        assert expected in ids, (text, ids)
    # brand search must also resolve (hiragana input normalised)
    assert any(r["id"] == "insulin_pzi" for r in search_drugs("ぷろじんく"))
    # precision guards: unrelated mentions must not chip
    for text, banned in (
        ("セレギリン 0.5 mg/kg PO q24h", "selenium_vitamin_e"),
        ("ビタミンB12 250 μg SC 週1", "selenium_vitamin_e"),
        ("スルファジアジン銀ではなく全身投与のスルファジアジン 25 mg/kg", None),
    ):
        ids = [h["id"] for h in find_drugs_in_text(text)]
        if banned:
            assert banned not in ids, (text, ids)


class TestBatch46DiazoxideRivaroxabanAntivenomGlucagon:
    """2026-08 15th referenced-but-absent sweep, surfaced by the emergency-tab
    key-drug linkification audit: diazoxide (standard second-line insulinoma
    therapy, 44 treatment refs), rivaroxaban (the only oral factor Xa
    inhibitor — feline ATE emergency key drug), mamushi antivenom (the most
    Japan-clinically-relevant antivenom, an emergency key drug), and glucagon
    (refractory-hypoglycemia CRI, 20 refs) were all absent from the
    formulary."""

    def test_diazoxide_present_with_insulinoma_dosing(self):
        from api.drug_dictionary import find_drugs_in_text, get_drug_by_id

        d = get_drug_by_id("diazoxide")
        assert d is not None, "diazoxide missing from formulary"
        for sp in ("ferret", "dog"):
            info = d["species_info"][sp]
            assert info["safe"] and "5" in info["dosage"] and "30" in info["dosage"]
            assert info["dosage_ja"]
        # defining safety facts: give with food, never a dextrose substitute
        assert "食事と共に" in d["species_info"]["ferret"]["dosage_ja"]
        assert "50%ブドウ糖" in d["contraindications_ja"]
        ids = [h["id"] for h in find_drugs_in_text("ジアゾキシド 5-30 mg/kg PO q12h を追加")]
        assert "diazoxide" in ids

    def test_rivaroxaban_present_with_curative_dosing_and_bleeding_gates(self):
        from api.drug_dictionary import find_drugs_in_text, get_drug_by_id

        d = get_drug_by_id("rivaroxaban")
        assert d is not None, "rivaroxaban missing from formulary"
        cat = d["species_info"]["cat"]
        assert "2.5 mg" in cat["dosage"] and "2.5 mg" in cat["dosage_ja"]
        # clopidogrel stays the evidence-based feline first line (FATCAT)
        assert "クロピドグレル" in cat["notes_ja"]
        dog = d["species_info"]["dog"]
        assert "1-2 mg/kg" in dog["dosage"]
        # therapeutic-anticoagulant co-administration must be flagged major
        assert any(
            i.get("severity") == "major" and "heparin" in i.get("drug", "").lower() for i in d["drug_interactions"]
        )
        ids = [h["id"] for h in find_drugs_in_text("リバロキサバン 2.5 mg/頭 PO q24h")]
        assert "rivaroxaban" in ids

    def test_mamushi_antivenom_present_with_anaphylaxis_precautions(self):
        from api.drug_dictionary import find_drugs_in_text, get_drug_by_id

        d = get_drug_by_id("mamushi_antivenom")
        assert d is not None, "mamushi antivenom missing from formulary"
        dog = d["species_info"]["dog"]
        assert "6,000" in dog["dosage"] and "エピネフリン" in dog["dosage_ja"]
        # supportive-care-first triage note (most canine bites survive without it)
        assert "支持療法" in dog["notes_ja"]
        assert "血清病" in d["side_effects_ja"]
        ids = [h["id"] for h in find_drugs_in_text("マムシ抗毒素血清 1バイアル 緩徐静注")]
        assert "mamushi_antivenom" in ids

    def test_glucagon_present_with_cri_dosing_and_rebound_warning(self):
        from api.drug_dictionary import find_drugs_in_text, get_drug_by_id

        d = get_drug_by_id("glucagon")
        assert d is not None, "glucagon missing from formulary"
        dog = d["species_info"]["dog"]
        assert "50 ng/kg" in dog["dosage"] and "5-40 ng/kg" in dog["dosage"]
        assert "反跳" in d["side_effects_ja"] or "反跳" in dog["notes_ja"]
        ids = [h["id"] for h in find_drugs_in_text("グルカゴン CRI 5-40 ng/kg/分")]
        assert "glucagon" in ids

    def test_emergency_key_drugs_resolve_to_formulary_links(self):
        """The emergency API must resolve key-drug rows to formulary links so
        the救急 tab's drug names are one-tap navigable; only blood products /
        thrombolytics absent from the formulary may stay unlinked."""
        from api.emergency_api import _resolve_key_drug_links
        from api.emergency_protocols import EMERGENCY_PROTOCOLS

        _resolve_key_drug_links()
        total = linked = 0
        unlinked = []
        by_name = {}
        for p in EMERGENCY_PROTOCOLS:
            for d in p.get("key_drugs", []):
                total += 1
                if d.get("link_name"):
                    linked += 1
                    by_name[d.get("name", "")] = d["link_name"]
                else:
                    unlinked.append(d.get("name", ""))
        assert linked / total >= 0.9, (linked, total, unlinked)
        # combination row must land on the combination entry, not bare ampicillin
        assert "Sulbactam" in by_name.get("Ampicillin/sulbactam", ""), by_name.get("Ampicillin/sulbactam")
        assert "Mamushi" in by_name.get("Mamushi antivenin", "")
        assert "Dextrose" in by_name.get("50% Dextrose", "")
        # blood products stay plain text (no dead-end links)
        assert all(n in {"FFP", "tPA (alteplase)"} for n in unlinked), unlinked
