"""Drug safety and contraindication tests.

Ensures that dangerous drug-species combinations are correctly marked
as contraindicated and that critical warnings are present.
"""

import pytest


@pytest.fixture(scope="module")
def drugs():
    from api.drug_dictionary import DRUGS

    return {d["id"]: d for d in DRUGS}


# =========================================================================
# Oral beta-lactam contraindications for hindgut fermenters
# These drugs cause fatal dysbiosis if given orally to these species.
# =========================================================================
HINDGUT_FERMENTERS = ["rabbit", "guinea_pig", "chinchilla", "hamster"]

ORAL_BETA_LACTAMS = [
    "amoxicillin",
    "amoxicillin_clavulanate",
]

# Drugs that are safe=True for certain hindgut fermenters with restrictions
# (e.g., parenteral-only ampicillin for rabbits, cephalexin relatively safe for rabbits)
PARENTERAL_ONLY_EXCEPTIONS = {
    ("ampicillin", "rabbit"),  # Injectable only, safe=True is correct
    ("cephalexin", "rabbit"),  # Relatively safe among beta-lactams for rabbits
}


@pytest.mark.parametrize("drug_id", ORAL_BETA_LACTAMS)
@pytest.mark.parametrize("species", HINDGUT_FERMENTERS)
def test_oral_beta_lactam_contraindicated_for_hindgut_fermenters(drugs, drug_id, species):
    """Oral beta-lactams must be marked unsafe for hindgut fermenters."""
    if (drug_id, species) in PARENTERAL_ONLY_EXCEPTIONS:
        pytest.skip(f"{drug_id}/{species} has parenteral-only exception")
    drug = drugs.get(drug_id)
    if drug is None:
        pytest.skip(f"Drug {drug_id} not in database")
    sp_info = drug.get("species_info", {}).get(species)
    if sp_info is None:
        pytest.skip(f"No {species} data for {drug_id}")
    assert sp_info["safe"] is False, (
        f"{drug_id} is marked safe=True for {species} — oral beta-lactams cause fatal dysbiosis in hindgut fermenters"
    )


# =========================================================================
# Lincosamide/macrolide contraindications
# =========================================================================
LINCOSAMIDES_MACROLIDES = ["lincomycin", "erythromycin", "tylosin"]


@pytest.mark.parametrize("drug_id", LINCOSAMIDES_MACROLIDES)
def test_lincosamide_macrolide_contraindicated_chinchilla(drugs, drug_id):
    """Lincosamides/macrolides must be contraindicated for chinchillas."""
    drug = drugs.get(drug_id)
    if drug is None:
        pytest.skip(f"Drug {drug_id} not in database")
    sp_info = drug.get("species_info", {}).get("chinchilla")
    if sp_info is None:
        pytest.skip(f"No chinchilla data for {drug_id}")
    assert sp_info["safe"] is False, (
        f"{drug_id} is marked safe=True for chinchilla — lincosamides/macrolides cause fatal enterotoxemia"
    )


# =========================================================================
# Fipronil contraindication for chinchillas (reported fatalities)
# =========================================================================
def test_fipronil_contraindicated_chinchilla(drugs):
    """Fipronil must be contraindicated for chinchillas."""
    drug = drugs.get("fipronil")
    if drug is None:
        pytest.skip("Fipronil not in database")
    sp_info = drug.get("species_info", {}).get("chinchilla")
    if sp_info is None:
        pytest.skip("No chinchilla data for fipronil")
    assert sp_info["safe"] is False, "Fipronil is marked safe=True for chinchilla — reported fatalities in chinchillas"


# =========================================================================
# Enrofloxacin cat retinal toxicity warning
# =========================================================================
def test_enrofloxacin_cat_retinal_toxicity_warning(drugs):
    """Enrofloxacin for cats must contain retinal toxicity warning."""
    drug = drugs.get("enrofloxacin")
    assert drug is not None, "Enrofloxacin not in database"
    cat_info = drug.get("species_info", {}).get("cat")
    assert cat_info is not None, "No cat data for enrofloxacin"
    notes = (cat_info.get("notes", "") + cat_info.get("notes_ja", "")).lower()
    assert "retin" in notes or "網膜" in notes, "Enrofloxacin cat notes must warn about retinal toxicity"
    dosage = cat_info.get("dosage", "")
    assert "5" in dosage, "Enrofloxacin cat dosage must indicate 5 mg/kg max"


# =========================================================================
# Metronidazole cat neurotoxicity warning
# =========================================================================
def test_metronidazole_cat_neurotoxicity_warning(drugs):
    """Metronidazole for cats must contain neurotoxicity warning."""
    drug = drugs.get("metronidazole")
    assert drug is not None, "Metronidazole not in database"
    cat_info = drug.get("species_info", {}).get("cat")
    assert cat_info is not None, "No cat data for metronidazole"
    notes = (cat_info.get("notes", "") + cat_info.get("notes_ja", "")).lower()
    assert "neuro" in notes or "神経" in notes, "Metronidazole cat notes must warn about neurotoxicity"


# =========================================================================
# Permethrin contraindicated for cats (lethal)
# =========================================================================
def test_permethrin_contraindicated_cats(drugs):
    """Permethrin must be contraindicated for cats."""
    drug = drugs.get("permethrin")
    if drug is None:
        pytest.skip("Permethrin not in database")
    cat_info = drug.get("species_info", {}).get("cat")
    if cat_info is None:
        pytest.skip("No cat data for permethrin")
    assert cat_info["safe"] is False, "Permethrin is marked safe=True for cats — pyrethroids are lethal to cats"


# =========================================================================
# Generic: no drug should be safe=True with "CONTRAINDICATED" in notes
# =========================================================================
def test_no_safe_true_with_contraindicated_notes(drugs):
    """No drug should be marked safe=True if notes say it is CONTRAINDICATED.

    Notes may mention other drugs being contraindicated (e.g., "use when NSAIDs
    are contraindicated") — these are NOT violations. Only flag when the note
    says THIS drug is contraindicated for THIS species.
    """
    # Phrases that indicate another drug is contraindicated, not this one
    false_positive_phrases = [
        "where nsaids are contraindicated",
        "nsaids are contraindicated",
        "nsaids contraindicated",
        "nsaids禁忌",
        "nsaid禁忌",
        "parenteral only",  # injectable is safe, oral is contraindicated
        "注射剤のみ",
        "経口投与は絶対禁忌",  # oral is contraindicated but injectable is safe
    ]
    violations = []
    for drug_id, drug in drugs.items():
        for species, info in drug.get("species_info", {}).items():
            if not info.get("safe"):
                continue
            notes = info.get("notes", "") + " " + info.get("notes_ja", "")
            notes_upper = notes.upper()
            if "CONTRAINDICATED" not in notes_upper and "禁忌" not in notes:
                continue
            # Check if it's a false positive
            notes_lower = notes.lower()
            if any(fp in notes_lower for fp in false_positive_phrases):
                continue
            violations.append(f"{drug_id}/{species}: safe=True but notes say contraindicated: {notes[:80]}")
    assert not violations, "Safe/contraindicated conflicts:\n" + "\n".join(violations)
