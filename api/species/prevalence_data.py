# ============================================================================
# Species Prevalence Data for Stepwise Differential Diagnosis
# ============================================================================
# This module provides prevalence classifications for diseases across 19 species
# Based on veterinary epidemiology and clinical practice patterns
#
# Tiers:
# - very_common (1.4x): Diseases seen daily/weekly (parasites, respiratory, GI)
# - common (1.2x): Diseases seen regularly (endocrine, neoplasia, systemic)
# - uncommon (0.9x): Occasional presentations (breed-specific, genetic)
# - rare (0.7x): Rarely encountered (exotic conditions, syndromes)
# ============================================================================

SPECIES_PREVALENCE = {
    # AMPHIBIAN
    "amphibian": {
        "Parasitic Infection": "very_common",
        "Bacterial Infection": "very_common",
        "Fungal Infection": "very_common",
        "Nutritional Deficiency": "very_common",
        "Chytrid Fungal Infection": "very_common",
        "Viral Infection": "common",
        "Red-leg Syndrome": "common",
        "Dropsy/Edema": "common",
        "Stomatitis": "common",
        "GI Impaction": "common",
    },

    # BIRD
    "bird": {
        "Psittacosis (Chlamydial Infection)": "very_common",
        "Aspergillosis": "very_common",
        "Respiratory Infection": "very_common",
        "Nutritional Deficiencies (Vitamin A)": "very_common",
        "Parasitic Infection": "very_common",
        "Dermatitis": "very_common",
        "Feather Plucking/Feather Loss": "very_common",
        "Bacterial Infection": "very_common",
        "Candidiasis": "very_common",
        "Giardiasis": "common",
        "Coccidia Infection": "common",
        "Viral Infection": "common",
        "Tumors/Neoplasia": "common",
        "Obesity": "common",
        "Arthrosis": "common",
        "Sinusitis": "common",
    },

    # CAT
    "cat": {
        "Upper Respiratory Infection (Feline)": "very_common",
        "Feline Panleukopenia": "very_common",
        "Feline Leukemia Virus (FeLV)": "very_common",
        "Feline Immunodeficiency Virus (FIV)": "very_common",
        "Enteritis": "very_common",
        "Gastroenteritis": "very_common",
        "Intestinal Parasites": "very_common",
        "Otitis (Ear Infection)": "very_common",
        "Urinary Tract Infection": "very_common",
        "Toxoplasma Infection": "very_common",
        "Flea Allergy Dermatitis": "very_common",
        "Hyperthyroidism": "common",
        "Diabetes Mellitus": "common",
        "Kidney Disease (CKD)": "common",
        "Hypertension": "common",
        "Heart Disease": "common",
        "Asthma/Lower Airway Disease": "common",
        "Dermatitis": "common",
        "Stomatitis": "common",
        "Periodontal Disease": "common",
        "Feline Uroliths": "common",
        "Lymphoma": "common",
        "Mammary Tumor": "common",
    },

    # CHINCHILLA
    "chinchilla": {
        "Respiratory Infection": "very_common",
        "Diarrhea": "very_common",
        "Dental Malocclusion": "very_common",
        "Parasitic Infection": "very_common",
        "Dermatitis": "very_common",
        "GI Stasis": "very_common",
        "Fur Mites": "very_common",
        "Pneumonia": "common",
        "Ringworm Infection": "common",
        "Urinary Calculi": "common",
        "Conjunctivitis": "common",
        "Heat Stroke": "common",
    },

    # DEGU
    "degu": {
        "Respiratory Infection": "very_common",
        "Dental Disease": "very_common",
        "Diabetes": "very_common",
        "Diarrhea": "very_common",
        "Eye Disease": "very_common",
        "Dermatitis": "very_common",
        "GI Stasis": "common",
        "Parasitic Infection": "common",
        "Seizures": "common",
        "Tumors": "common",
    },

    # EXOTIC OTHER
    "exotic_other": {
        "Parasitic Infection": "very_common",
        "Respiratory Infection": "very_common",
        "Nutritional Deficiency": "very_common",
        "Dermatitis": "very_common",
        "GI Impaction": "very_common",
        "Metabolic Bone Disease": "common",
        "Bacterial Infection": "common",
        "Fungal Infection": "common",
        "Neoplasia": "common",
    },

    # FERRET
    "ferret": {
        "Adrenal Gland Disease": "very_common",
        "Lymphoma": "very_common",
        "Parasitic Infection": "very_common",
        "Respiratory Infection": "very_common",
        "Diarrhea": "very_common",
        "Anal Sac Disease": "very_common",
        "Insulinoma": "common",
        "Spleen Enlargement": "common",
        "Heart Disease": "common",
        "Otitis": "common",
        "Dental Disease": "common",
        "GI Foreign Body": "common",
        "Intestinal Stasis": "common",
    },

    # GUINEA PIG
    "guinea_pig": {
        "Respiratory Infection": "very_common",
        "Vitamin C Deficiency": "very_common",
        "Dental Disease": "very_common",
        "Diarrhea": "very_common",
        "Intestinal Parasites": "very_common",
        "Otitis": "very_common",
        "Dermatitis": "very_common",
        "Pneumonia": "very_common",
        "GI Stasis": "common",
        "Obesity": "common",
        "Urinary Calculi": "common",
        "Barbering": "common",
        "Salmonella Infection": "common",
        "Mastitis": "common",
    },

    # HAMSTER
    "hamster": {
        "Cheek Pouch Impaction": "very_common",
        "Respiratory Infection": "very_common",
        "Diarrhea": "very_common",
        "Wet Tail": "very_common",
        "Dermatitis": "very_common",
        "Dental Overgrowth": "very_common",
        "Parasitic Infection": "very_common",
        "Tumors": "common",
        "Heart Disease": "common",
        "Diabetes": "common",
        "Pneumonia": "common",
        "Intestinal Obstruction": "common",
    },

    # HEDGEHOG
    "hedgehog": {
        "Parasitic Mites": "very_common",
        "Respiratory Infection": "very_common",
        "Dermatitis": "very_common",
        "Dental Disease": "very_common",
        "Obesity": "very_common",
        "GI Stasis": "very_common",
        "Wobbly Hedgehog Syndrome (WHS)": "common",
        "Salmonella Infection": "common",
        "Viral Infection": "common",
        "Liver Disease": "common",
        "Pneumonia": "common",
    },

    # LIZARD
    "lizard": {
        "Parasitic Infection": "very_common",
        "Respiratory Infection": "very_common",
        "Metabolic Bone Disease": "very_common",
        "Nutritional Deficiency": "very_common",
        "Dysecdysis": "very_common",
        "Dermatitis": "very_common",
        "Stomatitis": "very_common",
        "Impaction": "common",
        "Reproductive Issues": "common",
        "Abscesses": "common",
        "Thermal Burns": "common",
    },

    # PARAKEET
    "parakeet": {
        "Psittacosis": "very_common",
        "Aspergillosis": "very_common",
        "Respiratory Infection": "very_common",
        "Nutritional Deficiency": "very_common",
        "Parasitic Infection": "very_common",
        "Dermatitis": "very_common",
        "Feather Plucking": "very_common",
        "Polyoma Virus": "common",
        "Avian Pox": "common",
        "Giardiasis": "common",
        "Liver Disease": "common",
        "Sinusitis": "common",
    },

    # PARROT
    "parrot": {
        "Psittacosis": "very_common",
        "Aspergillosis": "very_common",
        "Respiratory Infection": "very_common",
        "Nutritional Deficiency": "very_common",
        "Parasitic Infection": "very_common",
        "Feather Plucking": "very_common",
        "Toxicity": "very_common",
        "Polyoma Virus": "common",
        "Avian Bornavirus": "common",
        "Liver Disease": "common",
        "Atherosclerosis": "common",
        "Neoplasia": "common",
    },

    # RABBIT
    "rabbit": {
        "Respiratory Infection": "very_common",
        "Gastrointestinal Stasis": "very_common",
        "Intestinal Parasites": "very_common",
        "Otitis": "very_common",
        "Malocclusion": "very_common",
        "Dermatitis": "very_common",
        "Conjunctivitis": "very_common",
        "Coccidiosis": "very_common",
        "Encephalitozoon cuniculi": "common",
        "Myxomatosis": "common",
        "Rabbit Hemorrhagic Disease": "common",
        "Dental Disease": "common",
        "Uterine Adenocarcinoma": "common",
        "Pasteurellosis": "common",
        "Hypertension": "common",
    },

    # REPTILE
    "reptile": {
        "Respiratory Infection": "very_common",
        "Parasitic Infection": "very_common",
        "Metabolic Bone Disease": "very_common",
        "Nutritional Deficiency": "very_common",
        "Dysecdysis": "very_common",
        "Stomatitis": "very_common",
        "Dermatitis": "very_common",
        "Impaction": "common",
        "Inclusion Body Disease": "common",
        "Pneumonia": "common",
        "Abscess": "common",
        "Thermal Burns": "common",
    },

    # SNAKE
    "snake": {
        "Parasitic Infection": "very_common",
        "Respiratory Infection": "very_common",
        "Inclusion Body Disease": "very_common",
        "Stomatitis": "very_common",
        "Regurgitation": "very_common",
        "Mites": "very_common",
        "Pneumonia": "common",
        "Metabolic Bone Disease": "common",
        "Nutritional Deficiency": "common",
        "Impaction": "common",
        "Scale Rot": "common",
    },

    # SUGAR GLIDER
    "sugar_glider": {
        "Nutritional Deficiency": "very_common",
        "Respiratory Infection": "very_common",
        "Parasitic Infection": "very_common",
        "Dermatitis": "very_common",
        "GI Stasis": "very_common",
        "Dental Disease": "very_common",
        "Metabolic Bone Disease": "common",
        "Neoplasia": "common",
        "Septicemia": "common",
        "Self-mutilation": "common",
    },

    # TORTOISE
    "tortoise": {
        "Respiratory Infection": "very_common",
        "Parasitic Infection": "very_common",
        "Metabolic Bone Disease": "very_common",
        "Nutritional Deficiency": "very_common",
        "Shell Disease": "very_common",
        "Stomatitis": "very_common",
        "Pneumonia": "common",
        "Dysecdysis": "common",
        "GI Impaction": "common",
        "Abscess": "common",
        "Nutritional Hyperparathyroidism": "common",
    },
}


def get_prevalence_for_species(species: str) -> dict[str, str]:
    """Get prevalence mapping for a specific species.

    Parameters
    ----------
    species : str
        Species key (e.g., 'cat', 'rabbit', 'bird')

    Returns
    -------
    dict[str, str]
        Mapping of disease names to prevalence tiers
    """
    return SPECIES_PREVALENCE.get(species, {})
