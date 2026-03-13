"""
Prevalence Tier Dictionaries for Veterinary Species
====================================================

This file contains disease prevalence classifications for 19 species of veterinary interest.
Each dictionary maps disease names to prevalence tiers based on typical occurrence in clinical practice.

Prevalence Tiers:
- very_common: Seen daily/weekly (routine practice encounters)
- common: Seen regularly in practice (several times per week/month)
- uncommon: Seen occasionally (several times per year)
- rare: Seen rarely (once a year or less)

Impact: These tiers are used to apply a multiplier to disease probability scores in the symptom checker.
- very_common: 1.4x multiplier
- common: 1.2x multiplier
- uncommon: 0.9x multiplier
- rare: 0.7x multiplier (default)
"""

# =============================================================================
# AMPHIBIAN (131 total diseases)
# =============================================================================
# Analysis: Amphibians present with mostly environmental and husbandry-related diseases
# Very common: Chytridiomycosis (Bd), metabolic bone disease, parasites, environmental stress
# Common: Fungal/bacterial infections, nutritional deficiencies, thermal stress
# Uncommon/Rare: Genetic conditions, exotic neoplasias

_SPECIES_AMPHIBIAN_PREVALENCE: dict[str, str] = {
    # ===== VERY COMMON =====
    "Chytridiomycosis (Bd)": "very_common",
    "Metabolic Bone Disease": "very_common",
    "Dehydration": "very_common",
    "Red Leg Syndrome": "very_common",
    "Ranavirus Infection": "very_common",
    "Parasitic Infection (Nematode)": "very_common",
    "Thermal Stress (Hypothermia)": "very_common",
    "Thermal Stress (Hyperthermia)": "very_common",
    "Nutritional Secondary Hyperparathyroidism": "very_common",
    "Intestinal Impaction": "very_common",
    "Oxyurid (Pinworm) Infection": "very_common",
    "Calcium Deficiency (Hypocalcemia)": "very_common",

    # ===== COMMON =====
    "Frog Virus 3 (FV3)": "common",
    "Aspergillosis": "common",
    "Salmonellosis": "common",
    "Bacterial Dermatitis": "common",
    "Fungal Infection (Saprolegniasis)": "common",
    "Dysecdysis (Abnormal Shedding)": "common",
    "Anorexia (Multifactorial)": "common",
    "Herpesvirus Infection": "common",
    "Hepatic Lipidosis": "common",
    "Chlamydiosis": "common",
    "Edema / Hydrops (Dropsy)": "common",
    "Coccidiosis": "common",
    "Low Dissolved Oxygen": "common",
    "Ammonia Poisoning": "common",
    "Iodine Deficiency (Goiter)": "common",
    "Vitamin D3 Deficiency": "common",

    # ===== UNCOMMON/RARE =====
    "Limb Deformity (Developmental)": "uncommon",
    "Fibrosarcoma": "uncommon",
    "Mycobacteriosis": "uncommon",
    "Polymyxoan Infection": "uncommon",
    "Hepatocellular Carcinoma": "rare",
    "Osteosarcoma": "rare",
    "Mucormycosis": "rare",
    "Chemical Toxicity (Pesticides/Metals)": "rare",
}

# =============================================================================
# BIRD (308 total diseases)
# =============================================================================
# Analysis: Birds have diverse disease profiles - respiratory, parasitic, viral
# Very common: Psittacosis, aspergillosis, air sac mites, feather disorders
# Common: Nutritional deficiencies, viral infections, bacterial infections
# Uncommon/Rare: Genetic conditions, exotic neoplasias

_SPECIES_BIRD_PREVALENCE: dict[str, str] = {
    # ===== VERY COMMON =====
    "Psittacosis / Chlamydiosis": "very_common",
    "Aspergillosis": "very_common",
    "Air Sac Mites (Sternostoma tracheacolum)": "very_common",
    "Cnemidocoptes pilae (Scaly Leg Mite)": "very_common",
    "Feather Destructive Behavior (FDB)": "very_common",
    "Feather Plucking (Feather Destructive Behavior)": "very_common",
    "Candidiasis": "very_common",
    "Avian Coccidiosis (Eimeria)": "very_common",
    "Avian Salmonellosis (Paratyphoid)": "very_common",
    "Crop Stasis (Crop Slowdown)": "very_common",
    "Nutritional Secondary Hyperparathyroidism": "very_common",
    "Calcium Deficiency (Hypocalcemia)": "very_common",
    "Proventricular Dilatation Disease (PDD / Bornavirus)": "very_common",
    "Avian Influenza": "very_common",

    # ===== COMMON =====
    "Avian Tuberculosis (Mycobacteriosis)": "common",
    "Hepatic Lipidosis (Fatty Liver Disease)": "common",
    "Egg Binding (Dystocia)": "common",
    "Obesity": "common",
    "Avian Polyomavirus": "common",
    "Avian Poxvirus": "common",
    "Pacheco's Disease (Psittacid Herpesvirus)": "common",
    "E. coli Infection (Colibacillosis)": "common",
    "Avian Mycoplasmosis": "common",
    "Congestive Heart Failure": "common",
    "Diabetes Mellitus": "common",
    "Avian Nephropathy": "common",
    "Thyroid Goiter (Thyroid Hyperplasia)": "common",
    "Giardiasis": "common",
    "Avian Gastric Yeast (Macrorhabdus ornithogaster)": "common",

    # ===== UNCOMMON/RARE =====
    "Avian Herpesvirus – Internal Papillomatosis": "uncommon",
    "Avian Leukosis": "uncommon",
    "Newcastle Disease": "uncommon",
    "Marek's Disease (Avian)": "uncommon",
    "Lymphoma": "rare",
    "Hemangiosarcoma": "rare",
    "Adenocarcinoma (General)": "rare",
    "Fibrosarcoma": "rare",
}

# =============================================================================
# CAT (516 total diseases)
# =============================================================================
# Analysis: Cats have largest disease database - infectious, endocrine, neoplastic dominant
# Very common: Upper respiratory infection, parasites, allergic dermatitis, gastroenteritis
# Common: Hyperthyroidism, CKD, diabetes, FIP, neoplasias, cardiac disease
# Uncommon/Rare: Genetic syndromes, exotic infections, rare toxicities

_SPECIES_CAT_PREVALENCE: dict[str, str] = {
    # ===== VERY COMMON =====
    "Feline Upper Respiratory Infection": "very_common",
    "Feline Calicivirus Infection": "very_common",
    "Feline Herpesvirus (FHV-1) Infection": "very_common",
    "Feline Gastroenteritis": "very_common",
    "Flea Infestation": "very_common",
    "Feline Diarrhea (Infectious)": "very_common",
    "Feline Panleukopenia (Feline Distemper)": "very_common",
    "Parasite Infection (Roundworm/Hookworm)": "very_common",
    "Flea Allergy Dermatitis": "very_common",
    "Feline Otitis Externa": "very_common",
    "Feline Anal Sac Disease": "very_common",
    "Pyoderma": "very_common",
    "Feline Lower Urinary Tract Disease (FLUTD)": "very_common",
    "Feline Idiopathic Cystitis (FIC)": "very_common",
    "Feline Otitis Media": "very_common",

    # ===== COMMON =====
    "Feline Hyperthyroidism": "common",
    "Feline Chronic Kidney Disease Stage IV (IRIS)": "common",
    "Feline Diabetes Mellitus": "common",
    "Feline Infectious Peritonitis (FIP) - Dry Form": "common",
    "Feline Infectious Peritonitis (FIP) - Wet Form": "common",
    "Feline Leukemia Virus (FeLV)": "common",
    "Feline Immunodeficiency Virus (FIV)": "common",
    "Feline Lymphoma (Alimentary)": "common",
    "Feline Hypertrophic Cardiomyopathy (HCM)": "common",
    "Feline Aortic Thromboembolism (Saddle Thrombus)": "common",
    "Feline Hepatic Lipidosis (Fatty Liver Disease)": "common",
    "Feline Atopic Dermatitis": "common",
    "Feline Dermatophytosis (Ringworm)": "common",
    "Feline Tooth Resorption (FORL)": "common",
    "Feline Chronic Pancreatitis": "common",
    "Feline Pneumonia": "common",
    "Feline Kidney Disease (CKD)": "common",
    "Feline Mammary Carcinoma": "common",
    "Feline Mast Cell Tumor (Cutaneous)": "common",
    "Feline Skin Tumor (General)": "common",

    # ===== UNCOMMON/RARE =====
    "Feline Cerebellar Hypoplasia": "uncommon",
    "Feline Manx Syndrome": "uncommon",
    "Feline Spina Bifida": "uncommon",
    "Feline Hereditary Myopathy (Devon Rex)": "uncommon",
    "Feline Dysautonomia (Key-Gaskell Syndrome)": "rare",
    "Feline Mucopolysaccharidosis": "rare",
    "Feline Glycogen Storage Disease": "rare",
    "Feline Pituitary Dwarfism": "rare",
}
