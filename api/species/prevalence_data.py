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
#
# IMPORTANT: Disease names must EXACTLY match the "name" field in the
# corresponding species disease module (api/species/*_diseases.py).
# ============================================================================

SPECIES_PREVALENCE = {
    # AMPHIBIAN
    "amphibian": {
        "Nematode Infection": "very_common",
        "Aeromonas Infection": "very_common",
        "Aspergillosis": "very_common",
        "Vitamin A Deficiency": "very_common",
        "Chytridiomycosis (Bd)": "very_common",
        "Ranavirus Infection": "common",
        "Red Leg Syndrome": "common",
        "Edema / Hydrops (Dropsy)": "common",
        "Stomatitis (Mouth Rot)": "common",
        "Intestinal Impaction": "common",
    },

    # BIRD
    "bird": {
        "Psittacosis (Chlamydiosis)": "very_common",
        "Aspergillosis": "very_common",
        "Chronic Respiratory Disease": "very_common",
        "Vitamin A Deficiency": "very_common",
        "Gastrointestinal Parasitic Disease": "very_common",
        "Dermatological Bacterial Infection": "very_common",
        "Feather Plucking": "very_common",
        "Gastrointestinal Bacterial Infection": "very_common",
        "Candidiasis": "very_common",
        "Giardiasis": "common",
        "Coccidia": "common",
        "Avian Polyomavirus": "common",
        "Lymphoma": "common",
        "Obesity": "common",
        "Articular Gout": "common",
        "Sinusitis": "common",
    },

    # CAT
    "cat": {
        "Feline Upper Respiratory Infection": "very_common",
        "Feline Herpesvirus (FHV-1) Infection": "very_common",
        "Feline Calicivirus Infection": "very_common",
        "Feline Chlamydiosis": "common",
        "Feline Panleukopenia (Feline Distemper)": "very_common",
        "Feline Leukemia Virus (FeLV)": "very_common",
        "Feline Immunodeficiency Virus (FIV)": "very_common",
        "Gastroenteritis": "very_common",
        "Intestinal Parasitism": "very_common",
        "Feline Otitis Externa": "very_common",
        "Urinary Tract Infection (UTI)": "very_common",
        "Flea Allergy Dermatitis": "very_common",
        "Feline Lower Urinary Tract Disease (FLUTD)": "very_common",
        "Feline Idiopathic Cystitis (FIC)": "very_common",
        "Constipation / Obstipation": "common",
        "Megacolon": "common",
        "Corneal Ulcer": "common",
        "Hepatic Lipidosis (Fatty Liver Disease)": "common",
        "Feline Infectious Peritonitis (FIP) - Wet Form": "uncommon",
        "Feline Infectious Peritonitis (FIP) - Dry Form": "uncommon",
        "Aortic Thromboembolism (Saddle Thrombus)": "uncommon",
        "Hyperthyroidism": "common",
        "Diabetes Mellitus": "common",
        "Chronic Kidney Disease (CKD)": "common",
        "Systemic Hypertension": "common",
        "Hypertrophic Cardiomyopathy (HCM)": "common",
        "Asthma": "common",
        "Feline Chronic Gingivostomatitis": "common",
        "Periodontal Disease": "common",
        "Alimentary Lymphoma": "common",
        "Mammary Tumor": "common",
    },

    # CHINCHILLA
    "chinchilla": {
        "Upper Respiratory Infection": "very_common",
        "Diarrhea": "very_common",
        "Dental Malocclusion - Incisor": "very_common",
        "Dental Malocclusion - Molar Spurs": "very_common",
        "GI Stasis": "very_common",
        "Fur Mites": "very_common",
        "Pneumonia": "common",
        "Dermatophytosis (Ringworm)": "common",
        "Conjunctivitis": "common",
        "Heat Stroke": "common",
    },

    # DEGU
    "degu": {
        "Upper Respiratory Infection": "very_common",
        "Dental Disease": "very_common",
        "Diabetes Mellitus": "very_common",
        "Diarrhea": "very_common",
        "Senile Cataracts": "very_common",
        "Sand Bath Dermatitis": "very_common",
        "GI Stasis": "common",
        "Intestinal Parasites": "common",
        "Seizures": "common",
        "Lymphoma": "common",
    },

    # EXOTIC OTHER
    "exotic_other": {
        "Intestinal Parasitism": "very_common",
        "Upper Respiratory Infection": "very_common",
        "Nutritional Deficiency": "very_common",
        "Contact Dermatitis": "very_common",
        "Metabolic Bone Disease": "common",
        "Dermatophytosis (Ringworm)": "common",
        "Lymphoma": "common",
    },

    # FERRET
    "ferret": {
        "Adrenal Disease": "very_common",
        "Lymphoma": "very_common",
        "Intestinal Parasites (Roundworm / Hookworm)": "very_common",
        "Upper Respiratory Infection": "very_common",
        "Insulinoma": "common",
        "Splenomegaly": "common",
        "Dilated Cardiomyopathy": "common",
        "Otitis Media/Interna": "common",
        "Dental Disease / Periodontal Disease": "common",
        "GI Foreign Body": "common",
    },

    # GUINEA PIG
    "guinea_pig": {
        "Upper Respiratory Infection": "very_common",
        "Scurvy (Vitamin C Deficiency)": "very_common",
        "Dental Malocclusion": "very_common",
        "Diarrhea": "very_common",
        "Intestinal Parasites": "very_common",
        "Otitis Externa (Outer Ear Infection)": "very_common",
        "Staphylococcal Pododermatitis": "very_common",
        "Pneumonia (Bacterial)": "very_common",
        "GI Stasis": "common",
        "Obesity": "common",
        "Renal Calculi": "common",
        "Barbering": "common",
        "Salmonellosis": "common",
        "Mastitis": "common",
    },

    # HAMSTER
    "hamster": {
        "Cheek Pouch Impaction": "very_common",
        "Upper Respiratory Infection": "very_common",
        "Diarrhea (Non-specific)": "very_common",
        "Wet Tail (Proliferative Ileitis)": "very_common",
        "Flank Gland Dermatitis": "very_common",
        "Dental Overgrowth (Molar)": "very_common",
        "Gastrointestinal Parasites": "very_common",
        "Lymphoma": "common",
        "Dilated Cardiomyopathy": "common",
        "Diabetes Mellitus": "common",
        "Pneumonia": "common",
        "Intestinal Impaction": "common",
    },

    # HEDGEHOG
    "hedgehog": {
        "Quill Mites (Chorioptes)": "very_common",
        "Upper Respiratory Infection": "very_common",
        "Dermatitis (Bacterial)": "very_common",
        "Dental Disease": "very_common",
        "Obesity": "very_common",
        "GI Stasis": "very_common",
        "Wobbly Hedgehog Syndrome (WHS)": "common",
        "Salmonellosis": "common",
        "Pneumonia": "common",
        "Fatty Liver Disease": "common",
    },

    # LIZARD
    "lizard": {
        "Mite Infestation (Ectoparasites)": "very_common",
        "Respiratory Infection": "very_common",
        "Metabolic Bone Disease (MBD)": "very_common",
        "Vitamin A Deficiency": "very_common",
        "Dysecdysis (Retained Shed)": "very_common",
        "Scale Rot (Ulcerative Dermatitis)": "very_common",
        "Stomatitis (Mouth Rot)": "very_common",
        "Gastrointestinal Impaction (Substrate Impaction)": "common",
        "Pre-ovulatory Follicular Stasis": "common",
        "Abscess": "common",
        "Thermal Burns": "common",
    },

    # PARAKEET
    "parakeet": {
        "Psittacosis (Chlamydiosis)": "very_common",
        "Aspergillosis": "very_common",
        "Upper Respiratory Infection": "very_common",
        "Nutritional Deficiency (General)": "very_common",
        "Scaly Face Mite (Knemidocoptes)": "very_common",
        "Feather Plucking": "very_common",
        "Avian Pox": "common",
        "Giardiasis": "common",
        "Fatty Liver Disease": "common",
        "Sinusitis": "common",
    },

    # PARROT
    "parrot": {
        "Psittacosis (Chlamydiosis)": "very_common",
        "Aspergillosis": "very_common",
        "Chronic Respiratory Disease": "very_common",
        "Nutritional Deficiency (General)": "very_common",
        "Intestinal Parasites (Roundworms/Tapeworms)": "very_common",
        "Feather Plucking": "very_common",
        "Avian Polyomavirus": "common",
        "Avian Bornavirus (ABV)": "common",
        "Fatty Liver Disease": "common",
        "Atherosclerosis": "common",
        "Lymphoma": "common",
    },

    # RABBIT
    "rabbit": {
        "Upper Respiratory Infection": "very_common",
        "Gastrointestinal Stasis": "very_common",
        "Coccidiosis (Intestinal)": "very_common",
        "Otitis Externa": "very_common",
        "Dental Malocclusion": "very_common",
        "Dermatophytosis (Ringworm)": "very_common",
        "Conjunctivitis": "very_common",
        "Hepatic Coccidiosis": "very_common",
        "Encephalitozoon cuniculi (E. cuniculi)": "common",
        "Myxomatosis": "common",
        "Rabbit Hemorrhagic Disease (RHD)": "common",
        "Pasteurellosis (Snuffles)": "common",
        "Uterine Adenocarcinoma": "common",
    },

    # REPTILE
    "reptile": {
        "Respiratory Infection": "very_common",
        "Internal Parasites (Nematodes)": "very_common",
        "Metabolic Bone Disease (MBD)": "very_common",
        "Vitamin A Deficiency": "very_common",
        "Dysecdysis (Retained Shed)": "very_common",
        "Stomatitis (Mouth Rot)": "very_common",
        "Shell Rot (Ulcerative Shell Disease)": "very_common",
        "Gastrointestinal Impaction": "common",
        "Inclusion Body Disease (IBD)": "common",
        "Pneumonia": "common",
        "Abscess": "common",
        "Thermal Burns": "common",
    },

    # SNAKE
    "snake": {
        "Hemoparasites (Blood Parasites)": "very_common",
        "Respiratory Infection": "very_common",
        "Inclusion Body Disease (IBD)": "very_common",
        "Infectious Stomatitis (Mouth Rot)": "very_common",
        "Regurgitation Syndrome": "very_common",
        "Snake Mites (Ophionyssus natricis)": "very_common",
        "Pneumonia": "common",
        "Metabolic Bone Disease (MBD)": "common",
        "Vitamin A Deficiency": "common",
        "Gastrointestinal Impaction": "common",
        "Scale Rot": "common",
    },

    # SUGAR GLIDER
    "sugar_glider": {
        "Malnutrition / Nutritional Deficiency": "very_common",
        "Upper Respiratory Infection": "very_common",
        "Intestinal Parasitism": "very_common",
        "Contact Dermatitis": "very_common",
        "GI Stasis": "very_common",
        "Dental Disease / Tartar Buildup": "very_common",
        "Metabolic Bone Disease (MBD)": "common",
        "Lymphoma": "common",
        "Septicemia": "common",
        "Self-Mutilation - Stress-Induced": "common",
    },

    # TORTOISE
    "tortoise": {
        "Respiratory Infection": "very_common",
        "Coccidia": "very_common",
        "Metabolic Bone Disease (MBD)": "very_common",
        "Vitamin A Deficiency": "very_common",
        "Shell Rot (Ulcerative Shell Disease)": "very_common",
        "Stomatitis (Mouth Rot)": "very_common",
        "Pneumonia": "common",
        "Dysecdysis (Retained Shed)": "common",
        "Gastrointestinal Impaction (Constipation)": "common",
        "Abscess": "common",
        "Nutritional Secondary Hyperparathyroidism": "common",
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
