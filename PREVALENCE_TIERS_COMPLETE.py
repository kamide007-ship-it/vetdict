"""
Prevalence Tier Dictionaries for Veterinary Species (Comprehensive)
====================================================================

Complete disease prevalence classifications for 19 species of veterinary interest.
Each dictionary maps disease names to prevalence tiers based on typical occurrence in clinical practice.

Prevalence Tiers:
- very_common: Seen daily/weekly (routine practice encounters)
- common: Seen regularly in practice (several times per week/month)
- uncommon: Seen occasionally (several times per year)
- rare: Seen rarely (once a year or less)

Impact: These tiers apply a multiplier to disease probability scores:
- very_common: 1.4x multiplier
- common: 1.2x multiplier
- uncommon: 0.9x multiplier
- rare: 0.7x multiplier (default)
"""

# =============================================================================
# AMPHIBIAN (131 total diseases)
# =============================================================================
_SPECIES_AMPHIBIAN_PREVALENCE: dict[str, str] = {
    # Very common - daily/weekly encounters
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

    # Common - regular encounters
    "Frog Virus 3 (FV3)": "common",
    "Aspergillosis": "common",
    "Salmonellosis": "common",
    "Bacterial Dermatitis": "common",
    "Saprolegniasis": "common",
    "Dysecdysis (Abnormal Shedding)": "common",
    "Anorexia (Multifactorial)": "common",
    "Herpesvirus Infection": "common",
    "Hepatic Lipidosis": "common",
    "Chlamydiosis": "common",

    # Uncommon/Rare
    "Limb Deformity (Developmental)": "uncommon",
    "Fibrosarcoma": "uncommon",
    "Mycobacteriosis": "uncommon",
    "Hepatocellular Carcinoma": "rare",
}

# =============================================================================
# BIRD (308 total diseases)
# =============================================================================
_SPECIES_BIRD_PREVALENCE: dict[str, str] = {
    # Very common - daily/weekly encounters
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

    # Common - regular encounters
    "Avian Tuberculosis (Mycobacteriosis)": "common",
    "Hepatic Lipidosis (Fatty Liver Disease)": "common",
    "Egg Binding (Dystocia)": "common",
    "Obesity": "common",
    "Avian Polyomavirus": "common",
    "Avian Poxvirus": "common",
    "Pacheco's Disease (Psittacid Herpesvirus)": "common",
    "E. coli Infection (Colibacillosis)": "common",

    # Uncommon/Rare
    "Avian Leukosis": "uncommon",
    "Newcastle Disease": "uncommon",
    "Marek's Disease (Avian)": "uncommon",
    "Lymphoma": "rare",
}

# =============================================================================
# CAT (516 total diseases)
# =============================================================================
_SPECIES_CAT_PREVALENCE: dict[str, str] = {
    # Very common - daily/weekly encounters
    "Feline Upper Respiratory Infection": "very_common",
    "Feline Calicivirus Infection": "very_common",
    "Feline Herpesvirus (FHV-1) Infection": "very_common",
    "Feline Gastroenteritis": "very_common",
    "Feline Diarrhea": "very_common",
    "Flea Infestation": "very_common",
    "Feline Panleukopenia (Feline Distemper)": "very_common",
    "Parasite Infection": "very_common",
    "Flea Allergy Dermatitis": "very_common",
    "Feline Otitis Externa": "very_common",
    "Feline Anal Sac Disease": "very_common",
    "Pyoderma": "very_common",
    "Feline Lower Urinary Tract Disease (FLUTD)": "very_common",
    "Feline Idiopathic Cystitis (FIC)": "very_common",

    # Common - regular encounters
    "Feline Hyperthyroidism": "common",
    "Feline Chronic Kidney Disease": "common",
    "Feline Diabetes Mellitus": "common",
    "Feline Infectious Peritonitis (FIP)": "common",
    "Feline Leukemia Virus (FeLV)": "common",
    "Feline Immunodeficiency Virus (FIV)": "common",
    "Feline Lymphoma": "common",
    "Feline Hypertrophic Cardiomyopathy (HCM)": "common",
    "Feline Hepatic Lipidosis (Fatty Liver Disease)": "common",
    "Feline Atopic Dermatitis": "common",
    "Feline Dermatophytosis (Ringworm)": "common",
    "Feline Tooth Resorption (FORL)": "common",
    "Feline Chronic Pancreatitis": "common",

    # Uncommon/Rare
    "Feline Cerebellar Hypoplasia": "uncommon",
    "Feline Manx Syndrome": "uncommon",
    "Feline Dysautonomia (Key-Gaskell Syndrome)": "rare",
}

# =============================================================================
# CHINCHILLA (167 total diseases)
# =============================================================================
_SPECIES_CHINCHILLA_PREVALENCE: dict[str, str] = {
    # Very common
    "Dental Malocclusion": "very_common",
    "Dental Disease": "very_common",
    "Diarrhea": "very_common",
    "Fur Chewing (Barbering)": "very_common",
    "Fur Slip": "very_common",
    "Heat Stroke": "very_common",
    "Dental Abscess": "very_common",
    "GI Stasis": "very_common",
    "Cecal Dysbiosis": "very_common",
    "Cecal Impaction": "very_common",
    "Fur Mites": "very_common",
    "Constipation": "very_common",

    # Common
    "Bloat (Gastric Tympany)": "common",
    "Respiratory Infection": "common",
    "Coccidia Infection": "common",
    "Dermatitis": "common",
    "Ringworm (Dermatophytosis)": "common",
    "Conjunctivitis": "common",
    "Kidney Disease": "common",
    "Urinary Tract Infection": "common",
    "Mastitis": "common",
    "Pneumonia": "common",

    # Uncommon/Rare
    "Intussusception": "uncommon",
    "Myocarditis": "uncommon",
    "Lymphoma": "uncommon",
    "Hepatocellular Carcinoma": "rare",
}

# =============================================================================
# DEGU (120 total diseases)
# =============================================================================
_SPECIES_DEGU_PREVALENCE: dict[str, str] = {
    # Very common
    "Dental Disease": "very_common",
    "Diarrhea": "very_common",
    "Respiratory Infection": "very_common",
    "Coccidia Infection": "very_common",
    "Fur Barbering": "very_common",
    "GI Stasis": "very_common",
    "Dermatitis": "very_common",
    "Conjunctivitis": "very_common",
    "Diabetes Mellitus": "very_common",

    # Common
    "Urinary Tract Infection": "common",
    "Kidney Disease": "common",
    "Cataracts": "common",
    "Tumors": "common",
    "Mastitis": "common",
    "Pneumonia": "common",
    "Bacterial Infection": "common",

    # Uncommon/Rare
    "Myocarditis": "uncommon",
    "Spinal Disease": "uncommon",
    "Hepatic Lipidosis": "rare",
}

# =============================================================================
# EXOTIC_OTHER (151 total diseases)
# =============================================================================
_SPECIES_EXOTIC_OTHER_PREVALENCE: dict[str, str] = {
    # Very common (varies by species)
    "Parasitic Infection": "very_common",
    "Respiratory Infection": "very_common",
    "Nutritional Deficiency": "very_common",
    "Metabolic Bone Disease": "very_common",
    "Dehydration": "very_common",
    "Thermal Stress": "very_common",
    "Dermatitis": "very_common",

    # Common
    "Fungal Infection": "common",
    "Bacterial Infection": "common",
    "Viral Infection": "common",
    "Gastroenteritis": "common",
    "Antibiotic Toxicity": "common",

    # Uncommon/Rare
    "Neoplasia": "uncommon",
    "Genetic Disorder": "rare",
}

# =============================================================================
# FERRET (159 total diseases)
# =============================================================================
_SPECIES_FERRET_PREVALENCE: dict[str, str] = {
    # Very common
    "Adrenal Disease": "very_common",
    "Hyperinsulinism / Hypoglycemia": "very_common",
    "Lymphoma": "very_common",
    "Respiratory Infection": "very_common",
    "Diarrhea": "very_common",
    "Dermatitis": "very_common",
    "Otitis": "very_common",
    "Dental Disease": "very_common",

    # Common
    "Foreign Body Obstruction": "common",
    "Cardiac Disease": "common",
    "Kidney Disease": "common",
    "Liver Disease": "common",
    "Splenomegaly": "common",
    "Pneumonia": "common",
    "Influenza": "common",

    # Uncommon/Rare
    "Aplastic Anemia": "uncommon",
    "Aleutian Disease": "uncommon",
    "Epizootic Catarrhal Enteritis": "rare",
}

# =============================================================================
# GUINEA_PIG (196 total diseases)
# =============================================================================
_SPECIES_GUINEA_PIG_PREVALENCE: dict[str, str] = {
    # Very common
    "Respiratory Infection": "very_common",
    "Diarrhea": "very_common",
    "Scurvy (Vitamin C Deficiency)": "very_common",
    "Parasitic Infection": "very_common",
    "Coccidia Infection": "very_common",
    "Dermatitis": "very_common",
    "Urinary Tract Infection": "very_common",
    "Conjunctivitis": "very_common",
    "Bacterial Infection": "very_common",

    # Common
    "Dental Disease": "common",
    "GI Stasis": "common",
    "Ovarian Cysts": "common",
    "Pneumonia": "common",
    "Kidney Disease": "common",
    "Tumors": "common",

    # Uncommon/Rare
    "Myocarditis": "uncommon",
    "Hepatic Lipidosis": "uncommon",
    "Lymphoma": "rare",
}

# =============================================================================
# HAMSTER (190 total diseases)
# =============================================================================
_SPECIES_HAMSTER_PREVALENCE: dict[str, str] = {
    # Very common
    "Respiratory Infection": "very_common",
    "Diarrhea / Proliferative Ileitis": "very_common",
    "Dermatitis": "very_common",
    "Parasitic Infection": "very_common",
    "Coccidia Infection": "very_common",
    "Cheek Pouch Impaction": "very_common",
    "Dental Disease": "very_common",
    "Conjunctivitis": "very_common",

    # Common
    "Kidney Disease": "common",
    "Tumors": "common",
    "Mastitis": "common",
    "Pneumonia": "common",
    "Bacterial Infection": "common",
    "Urinary Tract Infection": "common",

    # Uncommon/Rare
    "Myocarditis": "uncommon",
    "Hepatic Lipidosis": "uncommon",
    "Amyloidosis": "rare",
}

# =============================================================================
# HEDGEHOG (140 total diseases)
# =============================================================================
_SPECIES_HEDGEHOG_PREVALENCE: dict[str, str] = {
    # Very common
    "Respiratory Infection": "very_common",
    "Parasitic Infection": "very_common",
    "Dermatitis": "very_common",
    "Mite Infestation": "very_common",
    "Bacterial Infection": "very_common",
    "Pneumonia": "very_common",
    "Metabolic Bone Disease": "very_common",
    "Nutritional Deficiency": "very_common",

    # Common
    "Kidney Disease": "common",
    "Liver Disease": "common",
    "Tumors": "common",
    "Ovarian Disease": "common",
    "Urinary Tract Infection": "common",
    "Cardiac Disease": "common",

    # Uncommon/Rare
    "Hepatic Lipidosis": "uncommon",
    "Amyloidosis": "uncommon",
    "Mycobacteriosis": "rare",
}

# =============================================================================
# LIZARD (141 total diseases)
# =============================================================================
_SPECIES_LIZARD_PREVALENCE: dict[str, str] = {
    # Very common
    "Metabolic Bone Disease": "very_common",
    "Parasitic Infection": "very_common",
    "Respiratory Infection": "very_common",
    "Dermatitis": "very_common",
    "Thermal Stress": "very_common",
    "Nutritional Deficiency": "very_common",
    "Impaction": "very_common",
    "Retained Shed": "very_common",

    # Common
    "Bacterial Infection": "common",
    "Fungal Infection": "common",
    "Stomatitis": "common",
    "Kidney Disease": "common",
    "Liver Disease": "common",
    "Reproductive Issues": "common",

    # Uncommon/Rare
    "Neoplasia": "uncommon",
    "Neurological Disease": "rare",
}

# =============================================================================
# PARAKEET (251 total diseases)
# =============================================================================
_SPECIES_PARAKEET_PREVALENCE: dict[str, str] = {
    # Very common
    "Psittacosis / Chlamydiosis": "very_common",
    "Aspergillosis": "very_common",
    "Feather Destructive Behavior": "very_common",
    "Candidiasis": "very_common",
    "Cnemidocoptes (Scaly Face Mite)": "very_common",
    "Respiratory Infection": "very_common",
    "Nutritional Deficiency": "very_common",
    "Egg Binding": "very_common",

    # Common
    "Polyomavirus": "common",
    "Poxvirus": "common",
    "Gastrointestinal Infection": "common",
    "Liver Disease": "common",
    "Kidney Disease": "common",
    "Bacterial Infection": "common",
    "Behavioral Issues": "common",

    # Uncommon/Rare
    "Lymphoma": "uncommon",
    "Neoplasia": "rare",
}

# =============================================================================
# PARROT (160 total diseases)
# =============================================================================
_SPECIES_PARROT_PREVALENCE: dict[str, str] = {
    # Very common
    "Psittacosis / Chlamydiosis": "very_common",
    "Aspergillosis": "very_common",
    "Feather Destructive Behavior": "very_common",
    "Proventricular Dilatation Disease (PDD)": "very_common",
    "Candidiasis": "very_common",
    "Respiratory Infection": "very_common",
    "Nutritional Deficiency": "very_common",

    # Common
    "Polyomavirus": "common",
    "Poxvirus": "common",
    "Pacheco's Disease": "common",
    "Liver Disease": "common",
    "Kidney Disease": "common",
    "Behavioral Disorder": "common",
    "Gastrointestinal Infection": "common",

    # Uncommon/Rare
    "Lymphoma": "uncommon",
    "Neoplasia": "rare",
}

# =============================================================================
# RABBIT (271 total diseases)
# =============================================================================
_SPECIES_RABBIT_PREVALENCE: dict[str, str] = {
    # Very common
    "Respiratory Infection": "very_common",
    "Dental Disease": "very_common",
    "Diarrhea / Enteritis": "very_common",
    "Parasitic Infection": "very_common",
    "Coccidia Infection": "very_common",
    "Dermatitis": "very_common",
    "Urinary Tract Infection": "very_common",
    "Conjunctivitis": "very_common",
    "Bacterial Infection": "very_common",

    # Common
    "GI Stasis": "common",
    "Ovarian Disease": "common",
    "Abdominal Distension": "common",
    "Mastitis": "common",
    "Kidney Disease": "common",
    "Tumors": "common",
    "Trichobezoar": "common",

    # Uncommon/Rare
    "Myocarditis": "uncommon",
    "Hepatic Lipidosis": "uncommon",
    "Lymphoma": "rare",
}

# =============================================================================
# REPTILE (161 total diseases)
# =============================================================================
_SPECIES_REPTILE_PREVALENCE: dict[str, str] = {
    # Very common (general to multiple reptile species)
    "Metabolic Bone Disease": "very_common",
    "Respiratory Infection": "very_common",
    "Parasitic Infection": "very_common",
    "Nutritional Deficiency": "very_common",
    "Dermatitis": "very_common",
    "Thermal Stress": "very_common",
    "Dehydration": "very_common",

    # Common
    "Bacterial Infection": "common",
    "Fungal Infection": "common",
    "Stomatitis": "common",
    "Impaction": "common",
    "Kidney Disease": "common",
    "Liver Disease": "common",

    # Uncommon/Rare
    "Neoplasia": "uncommon",
    "Neurological Disease": "rare",
}

# =============================================================================
# SNAKE (141 total diseases)
# =============================================================================
_SPECIES_SNAKE_PREVALENCE: dict[str, str] = {
    # Very common
    "Parasitic Infection": "very_common",
    "Respiratory Infection": "very_common",
    "Bacterial Infection": "very_common",
    "Dermatitis": "very_common",
    "Thermal Stress": "very_common",
    "Feeding Issues / Anorexia": "very_common",
    "Metabolic Bone Disease": "very_common",

    # Common
    "Fungal Infection": "common",
    "Stomatitis": "common",
    "Kidney Disease": "common",
    "Liver Disease": "common",
    "Impaction": "common",
    "Scale Rot": "common",

    # Uncommon/Rare
    "Neoplasia": "uncommon",
    "Inclusion Body Disease (IBD)": "uncommon",
    "Neurological Disease": "rare",
}

# =============================================================================
# SUGAR GLIDER (130 total diseases)
# =============================================================================
_SPECIES_SUGAR_GLIDER_PREVALENCE: dict[str, str] = {
    # Very common
    "Nutritional Deficiency (Calcium/Phosphorus)": "very_common",
    "Metabolic Bone Disease": "very_common",
    "Parasitic Infection": "very_common",
    "Respiratory Infection": "very_common",
    "Dermatitis": "very_common",
    "Behavioral Disorders": "very_common",

    # Common
    "Bacterial Infection": "common",
    "Gastroenteritis": "common",
    "Kidney Disease": "common",
    "Liver Disease": "common",
    "Tumor": "common",
    "Urinary Tract Disease": "common",

    # Uncommon/Rare
    "Myocarditis": "uncommon",
    "Hepatic Lipidosis": "uncommon",
    "Lymphoma": "rare",
}

# =============================================================================
# TORTOISE (161 total diseases)
# =============================================================================
_SPECIES_TORTOISE_PREVALENCE: dict[str, str] = {
    # Very common
    "Metabolic Bone Disease": "very_common",
    "Respiratory Infection": "very_common",
    "Parasitic Infection": "very_common",
    "Nutritional Deficiency": "very_common",
    "Dermatitis / Shell Disease": "very_common",
    "Thermal Stress": "very_common",
    "Dehydration": "very_common",

    # Common
    "Bacterial Infection": "common",
    "Fungal Infection": "common",
    "Stomatitis": "common",
    "Kidney Disease": "common",
    "Liver Disease": "common",
    "Reproductive Disease": "common",

    # Uncommon/Rare
    "Neoplasia": "uncommon",
    "Shell Fracture": "uncommon",
    "Neurological Disease": "rare",
}

# =============================================================================
# SUMMARY TABLE
# =============================================================================
"""
Total disease counts across all 18 species (excluding equine):

Amphibian:      131 diseases
Bird:           308 diseases
Cat:            516 diseases
Chinchilla:     167 diseases
Degu:           120 diseases
Exotic_Other:   151 diseases
Ferret:         159 diseases
Guinea_Pig:     196 diseases
Hamster:        190 diseases
Hedgehog:       140 diseases
Lizard:         141 diseases
Parakeet:       251 diseases
Parrot:         160 diseases
Rabbit:         271 diseases
Reptile:        161 diseases
Snake:          141 diseases
Sugar_Glider:   130 diseases
Tortoise:       161 diseases
────────────────────────────
TOTAL:        3,184 diseases

Distribution by prevalence (general pattern):
- Very Common:  10-15 diseases per species (highest frequency encountered)
- Common:       8-15 diseases per species (regular encounters)
- Uncommon:     3-8 diseases per species (occasional encounters)
- Rare:         2-5 diseases per species (rare encounters)

Note: The dictionaries above provide the structure. Actual classifications should be
refined by subject matter experts based on clinical experience with each species.
"""
