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
    # ==================================================================
    # DOG — 50 entries
    # ==================================================================
    "dog": {
        # very_common — daily/weekly presentations
        "Ear Infection (Otitis)": "very_common",
        "Periodontal Disease": "very_common",
        "Allergic Dermatitis": "very_common",
        "Flea Allergy Dermatitis": "very_common",
        "Gastroenteritis": "very_common",
        "Intestinal Parasites": "very_common",
        "Osteoarthritis": "very_common",
        "Pyoderma": "very_common",
        "Mange (Demodex/Sarcoptes)": "very_common",
        # common — regular presentations
        "Urinary Tract Infection": "common",
        "Hypothyroidism": "common",
        "Cushing's Disease": "common",
        "Diabetes Mellitus": "common",
        "Pancreatitis": "common",
        "Gastric Dilatation-Volvulus (GDV/Bloat)": "common",
        "Intervertebral Disc Disease (IVDD)": "common",
        "Cruciate Ligament Injury": "common",
        "Canine Parvovirus": "common",
        "Kennel Cough (Bordetella)": "common",
        "Leptospirosis": "common",
        "Pyometra": "common",
        "Mammary Tumor": "common",
        "Lymphoma": "common",
        "Mast Cell Tumor": "common",
        "Hemangiosarcoma": "common",
        "Cataracts": "common",
        "Glaucoma": "common",
        "Epilepsy": "common",
        "Kidney Disease (CKD)": "common",
        "Heart Disease/CHF": "common",
        "Mitral Valve Disease (MMVD)": "common",
        "Dilated Cardiomyopathy (DCM)": "common",
        "Patellar Luxation": "common",
        "Hip Dysplasia": "common",
        "Heartworm Disease": "common",
        "Corneal Ulcer": "common",
        "Cherry Eye": "common",
        "Inflammatory Bowel Disease (IBD)": "common",
        "Anal Sac Disease": "common",
        "Foreign Body Obstruction": "common",
        "Tracheal Collapse": "common",
        "Lyme Disease": "common",
        # uncommon
        "Addison's Disease": "uncommon",
        "Megaesophagus": "uncommon",
        "Exocrine Pancreatic Insufficiency (EPI)": "uncommon",
        "Immune-Mediated Hemolytic Anemia": "uncommon",
        "Autoimmune Thrombocytopenia (ITP)": "uncommon",
        "Myasthenia Gravis": "uncommon",
        "Systemic Lupus Erythematosus (SLE)": "uncommon",
        # rare
        "Portosystemic Shunt (Liver Shunt)": "rare",
        "Pheochromocytoma": "rare",
        "Insulinoma": "rare",
    },

    # ==================================================================
    # CAT — 65+ entries (expanded from ~37)
    # ==================================================================
    "cat": {
        # very_common
        "Feline Upper Respiratory Infection": "very_common",
        "Feline Herpesvirus (FHV-1) Infection": "very_common",
        "Feline Calicivirus Infection": "very_common",
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
        "Hyperthyroidism": "very_common",
        "Chronic Kidney Disease (CKD)": "very_common",
        "Periodontal Disease": "very_common",
        "Roundworm Infection (Toxocara cati)": "very_common",
        "Tapeworm Infection (Dipylidium caninum)": "very_common",
        "Ear Mite Infestation (Otodectes cynotis)": "very_common",
        "Flea Infestation": "very_common",
        "Dermatophytosis (Ringworm)": "very_common",
        # common
        "Feline Chlamydiosis": "common",
        "Constipation / Obstipation": "common",
        "Megacolon": "common",
        "Corneal Ulcer": "common",
        "Hepatic Lipidosis (Fatty Liver Disease)": "common",
        "Diabetes Mellitus": "common",
        "Systemic Hypertension": "common",
        "Hypertrophic Cardiomyopathy (HCM)": "common",
        "Feline Asthma": "common",
        "Feline Chronic Gingivostomatitis": "common",
        "Alimentary Lymphoma": "common",
        "Mammary Tumor": "common",
        "Hypothyroidism (Iatrogenic)": "common",
        "Feline Anterior Uveitis": "common",
        "Inflammatory Bowel Disease (IBD)": "common",
        "Feline Pancreatitis": "common",
        "Feline Tooth Resorption (FORL)": "common",
        "Conjunctivitis": "common",
        "Atopic Dermatitis": "common",
        "Food Allergy Dermatitis": "common",
        "Urolithiasis (Bladder Stones)": "common",
        "Gastrointestinal Lymphoma": "common",
        "Feline Epilepsy": "common",
        "Osteoarthritis (Degenerative Joint Disease)": "common",
        "Dilated Cardiomyopathy (DCM)": "common",
        "Squamous Cell Carcinoma (Oral)": "common",
        "Squamous Cell Carcinoma (Cutaneous)": "common",
        "Injection-Site Sarcoma (Fibrosarcoma)": "common",
        "Feline Heartworm Disease": "common",
        "Cholangitis / Cholangiohepatitis": "common",
        "Miliary Dermatitis": "common",
        "Psychogenic Alopecia": "common",
        "Hookworm Infection": "common",
        "Giardiasis": "common",
        "Coccidia Infection": "common",
        # uncommon
        "Feline Infectious Peritonitis (FIP) - Wet Form": "uncommon",
        "Feline Infectious Peritonitis (FIP) - Dry Form": "uncommon",
        "Aortic Thromboembolism (Saddle Thrombus)": "uncommon",
        "Renal Lymphoma": "uncommon",
        "Feline Interstitial Nephritis": "uncommon",
        "Feline Glomerulonephritis": "uncommon",
        "Diabetic Ketoacidosis (DKA)": "uncommon",
        "Polycystic Kidney Disease (PKD)": "uncommon",
        "Immune-Mediated Hemolytic Anemia (IMHA)": "uncommon",
        "Pemphigus Foliaceus": "uncommon",
        "Restrictive Cardiomyopathy": "uncommon",
        "Pericardial Effusion": "uncommon",
        # rare
        "Amyloidosis": "rare",
        "Hyperaldosteronism (Conn's Syndrome)": "rare",
        "Acromegaly (Hypersomatotropism)": "rare",
        "Portosystemic Shunt": "rare",
        "Myasthenia Gravis": "rare",
    },

    # ==================================================================
    # RABBIT — 35+ entries (expanded from ~23)
    # ==================================================================
    "rabbit": {
        # very_common
        "Gastrointestinal Stasis": "very_common",
        "Dental Malocclusion": "very_common",
        "Molar Spurs": "very_common",
        "Incisor Overgrowth": "very_common",
        "Pasteurellosis (Snuffles)": "very_common",
        "Upper Respiratory Infection": "very_common",
        "Coccidiosis (Intestinal)": "very_common",
        "Hepatic Coccidiosis": "very_common",
        "Otitis Externa": "very_common",
        "Dermatophytosis (Ringworm)": "very_common",
        "Conjunctivitis": "very_common",
        "Pinworms (Passalurus ambiguus)": "very_common",
        "Fur Mites (Cheyletiella parasitovorax)": "very_common",
        "Ear Mites (Psoroptes cuniculi)": "very_common",
        # common
        "Encephalitozoon cuniculi (E. cuniculi)": "common",
        "Myxomatosis": "common",
        "Rabbit Haemorrhagic Disease (RHDV/VHD)": "common",
        "RHDV2": "common",
        "Uterine Adenocarcinoma": "common",
        "Pododermatitis (Sore Hocks)": "common",
        "Vestibular Disease": "common",
        "Otitis Media / Interna": "common",
        "Subcutaneous Abscess": "common",
        "Tooth Root Abscess": "common",
        "Urinary Sludge": "common",
        "Urolithiasis (Bladder Stones)": "common",
        "Trichobezoar (Hairball)": "common",
        "Obesity": "common",
        "Intestinal Coccidiosis": "common",
        "Myiasis (Flystrike)": "common",
        "Pyometra": "common",
        "Hind Limb Paresis / Paralysis": "common",
        # uncommon
        "Treponematosis (Rabbit Syphilis)": "uncommon",
        "Bordetella Infection": "uncommon",
        "Mycoplasmosis": "uncommon",
        "Megacolon": "uncommon",
        "Ileus (Paralytic)": "uncommon",
        "Colonic Impaction": "uncommon",
        "Sarcoptic Mange": "uncommon",
        "Thymoma": "uncommon",
        "Lymphoma": "uncommon",
        # rare
        "Klebsiella Pneumonia": "rare",
        "Cecoliths": "rare",
        "Pulmonary Edema": "rare",
        "Pulmonary Fibrosis": "rare",
        "Pyothorax": "rare",
        "Cecal Tympany": "rare",
    },

    # ==================================================================
    # BIRD — 28+ entries (expanded from ~16)
    # ==================================================================
    "bird": {
        # very_common
        "Psittacosis / Chlamydiosis": "very_common",
        "Aspergillosis": "very_common",
        "Feather Plucking (Feather Destructive Behavior)": "very_common",
        "Vitamin A Deficiency (Hypovitaminosis A)": "very_common",
        "Gastrointestinal Parasitic Disease": "very_common",
        "Candidiasis": "very_common",
        "Ingluvitis (Crop Infection)": "very_common",
        "Crop Stasis (Crop Slowdown)": "very_common",
        "E. coli Infection (Colibacillosis)": "very_common",
        "Dermatitis": "very_common",
        # common
        "Psittacine Beak and Feather Disease (PBFD)": "common",
        "Proventricular Dilatation Disease (PDD / Bornavirus)": "common",
        "Avian Polyomavirus": "common",
        "Megabacteriosis (Avian Gastric Yeast / AGY)": "common",
        "Egg Binding (Dystocia)": "common",
        "Articular Gout": "common",
        "Visceral Gout": "common",
        "Obesity": "common",
        "Sinusitis": "common",
        "Rhinitis": "common",
        "Hepatic Lipidosis (Fatty Liver Disease)": "common",
        "Metabolic Bone Disease (MBD / Rickets)": "common",
        "Pododermatitis (Bumblefoot)": "common",
        "Pneumonia": "common",
        "Lymphoma": "common",
        "Calcium Deficiency (Hypocalcemia)": "common",
        "Air Sacculitis": "common",
        "Enteritis": "common",
        # uncommon
        "Avian Bornavirus (ABV)": "uncommon",
        "Hemochromatosis (Iron Storage Disease)": "uncommon",
        "Newcastle Disease": "uncommon",
        "Cryptococcosis": "uncommon",
        "Cloacal Prolapse": "uncommon",
    },

    # ==================================================================
    # REPTILE — 22+ entries (expanded from ~12)
    # ==================================================================
    "reptile": {
        # very_common
        "Metabolic Bone Disease (MBD)": "very_common",
        "Upper Respiratory Infection (URI)": "very_common",
        "Lower Respiratory Infection (Pneumonia)": "very_common",
        "Internal Parasites (Nematodes)": "very_common",
        "Dysecdysis (Retained Shed)": "very_common",
        "Shell Rot (Ulcerative Shell Disease)": "very_common",
        "Vitamin A Deficiency (Hypovitaminosis A)": "very_common",
        "External Mites (Ophionyssus)": "very_common",
        "Dehydration": "very_common",
        # common
        "Infectious Stomatitis (Mouth Rot)": "common",
        "Gastrointestinal Impaction": "common",
        "Thermal Burns": "common",
        "Scale Rot (Ulcerative Dermatitis)": "common",
        "Egg Binding (Dystocia)": "common",
        "Pre-ovulatory Follicular Stasis": "common",
        "Subcutaneous Abscess": "common",
        "Coccidia Infection": "common",
        "Cryptosporidiosis": "common",
        "Rostral Abrasion (Nose Rub)": "common",
        "Pneumonia": "common",
        "Nutritional Secondary Hyperparathyroidism": "common",
        # uncommon
        "Articular Gout": "uncommon",
        "Visceral Gout": "uncommon",
        "Inclusion Body Disease (IBD)": "uncommon",
        "Septicemia (Blood Poisoning)": "uncommon",
        "Hepatic Lipidosis (Fatty Liver Disease)": "uncommon",
        # rare
        "Adenovirus Infection": "rare",
        "Paramyxovirus Infection": "rare",
    },

    # ==================================================================
    # FISH — 25 entries (expanded from ~10)
    # ==================================================================
    "fish": {
        # very_common
        "Ichthyophthirius (White Spot Disease / Ich)": "very_common",
        "Columnaris Disease": "very_common",
        "Ammonia Poisoning": "very_common",
        "Swim Bladder Disorder": "very_common",
        "Aeromonas / Motile Aeromonad Septicemia": "very_common",
        "Saprolegnia (Water Mold / Cotton Wool Disease)": "very_common",
        "Nitrite Poisoning (Brown Blood Disease)": "very_common",
        "Skin Flukes (Gyrodactylus)": "very_common",
        "Marine Ich (Cryptocaryon irritans)": "very_common",
        # common
        "Dropsy (Pinecone Disease)": "common",
        "Velvet Disease (Oodinium / Piscinoodinium)": "common",
        "Anchor Worm (Lernaea)": "common",
        "Gill Flukes (Dactylogyrus)": "common",
        "Hexamita / Spironucleus (Internal Flagellates)": "common",
        "Costia (Ichthyobodo)": "common",
        "Fish Lice (Argulus)": "common",
        "Hole-in-the-Head Disease (HITH / HLLE)": "common",
        "Trichodina": "common",
        "pH Shock": "common",
        # uncommon
        "Lymphocystis": "uncommon",
        "Neon Tetra Disease (Pleistophora)": "uncommon",
        "Mycobacteriosis (Fish Tuberculosis)": "uncommon",
        "Egg Binding (Dystocia)": "uncommon",
        # rare
        "Koi Herpesvirus Disease (KHV / CyHV-3)": "rare",
        "Spring Viremia of Carp (SVC)": "rare",
    },

    # ==================================================================
    # HAMSTER — 25+ entries (expanded from ~12)
    # ==================================================================
    "hamster": {
        # very_common
        "Wet Tail (Proliferative Ileitis)": "very_common",
        "Cheek Pouch Impaction": "very_common",
        "Diarrhea (Non-specific)": "very_common",
        "Upper Respiratory Infection": "very_common",
        "Dental Malocclusion": "very_common",
        "Dental Overgrowth (Molar)": "very_common",
        "Flank Gland Dermatitis": "very_common",
        "Gastrointestinal Parasites": "very_common",
        "Demodex Mange": "very_common",
        # common
        "Diabetes Mellitus": "common",
        "Lymphoma": "common",
        "Dilated Cardiomyopathy": "common",
        "Pneumonia": "common",
        "Amyloidosis": "common",
        "Ringworm (Dermatophytosis)": "common",
        "Mammary Tumor": "common",
        "Skin Abscess": "common",
        "Conjunctivitis": "common",
        "Cataracts": "common",
        "Hibernation / Torpor": "common",
        "Intestinal Impaction": "common",
        "Obesity": "common",
        "Cheek Pouch Prolapse": "common",
        "Cystitis": "common",
        # uncommon
        "Cushing's Disease": "uncommon",
        "Congestive Heart Failure": "uncommon",
        "Chronic Renal Failure": "uncommon",
        "Hamster Polyomavirus": "uncommon",
        "Adrenal Tumor": "uncommon",
        # rare
        "Lymphocytic Choriomeningitis (LCMV)": "rare",
    },

    # ==================================================================
    # GUINEA PIG — 25+ entries (expanded from ~14)
    # ==================================================================
    "guinea_pig": {
        # very_common
        "Scurvy (Vitamin C Deficiency)": "very_common",
        "Upper Respiratory Infection (URI)": "very_common",
        "Bacterial Pneumonia": "very_common",
        "Dental Malocclusion": "very_common",
        "Intestinal Parasites": "very_common",
        "Otitis Externa (Outer Ear Infection)": "very_common",
        "Sarcoptic Mange (Trixacarus caviae)": "very_common",
        "Ovarian Cysts": "very_common",
        "Fungal Dermatitis (Ringworm)": "very_common",
        "Diarrhea": "very_common",
        "Staphylococcal Pododermatitis": "very_common",
        "Pneumonia (Bacterial)": "very_common",
        # common
        "Pododermatitis (Bumblefoot)": "common",
        "Urolithiasis (Bladder Stones)": "common",
        "GI Stasis": "common",
        "Obesity": "common",
        "Barbering": "common",
        "Bladder Sludge": "common",
        "Urinary Tract Infection (UTI)": "common",
        "Static Lice (Gliricola porcelli)": "common",
        "Bordetella bronchiseptica Infection": "common",
        "Streptococcus pneumoniae Infection": "common",
        "Conjunctivitis": "common",
        "Elongated Tooth Roots": "common",
        "Mastitis": "common",
        "Renal Calculi": "common",
        "Sebaceous Cyst": "common",
        # uncommon
        "Salmonellosis": "uncommon",
        "Pregnancy Toxemia (Ketosis)": "uncommon",
        "Diabetes Mellitus": "uncommon",
        "Lymphoma": "uncommon",
        "Chronic Kidney Disease": "uncommon",
        "Antibiotic-Associated Enterotoxemia": "uncommon",
        # rare
        "Lymphocytic Choriomeningitis Virus (LCMV)": "rare",
        "Leukemia": "rare",
    },

    # ==================================================================
    # FERRET — 22+ entries (expanded from ~10)
    # ==================================================================
    "ferret": {
        # very_common
        "Adrenal Disease": "very_common",
        "Insulinoma": "very_common",
        "Intestinal Parasites (Roundworm / Hookworm)": "very_common",
        "Upper Respiratory Infection (URI)": "very_common",
        "Ear Mites (Otodectes cynotis)": "very_common",
        "Dental Disease / Periodontal Disease": "very_common",
        # common
        "Lymphoma": "common",
        "Splenomegaly": "common",
        "Dilated Cardiomyopathy (DCM)": "common",
        "GI Foreign Body": "common",
        "Influenza (Human Flu)": "common",
        "Epizootic Catarrhal Enteritis (ECE / Green Slime Disease)": "common",
        "Aplastic Anemia (Estrogen Toxicity)": "common",
        "Helicobacter Mustelae Gastritis": "common",
        "Adrenal Alopecia": "common",
        "Adrenal Tumor (Adenoma / Adenocarcinoma)": "common",
        "Flea Dermatitis": "common",
        "Aleutian Disease (ADV)": "common",
        "Posterior Paresis / Hind Leg Weakness": "common",
        "Hairballs (Trichobezoars)": "common",
        # uncommon
        "Heartworm Disease": "uncommon",
        "Otitis Media/Interna": "uncommon",
        "Hypertrophic Cardiomyopathy (HCM)": "uncommon",
        "Ferret Systemic Coronavirus (FRSCV)": "uncommon",
        "Proliferative Colitis": "uncommon",
        # rare
        "Canine Distemper": "rare",
        "Rabies": "rare",
        "Chordoma": "rare",
    },

    # ==================================================================
    # HEDGEHOG — 22+ entries (expanded from ~10)
    # ==================================================================
    "hedgehog": {
        # very_common
        "Mite Infestation (Caparinia)": "very_common",
        "Obesity": "very_common",
        "Dental Disease": "very_common",
        "Upper Respiratory Infection": "very_common",
        "Dermatitis (Bacterial)": "very_common",
        "GI Stasis": "very_common",
        "Quilling (Physiological)": "very_common",
        "Internal Parasites (Intestinal Worms)": "very_common",
        # common
        "Wobbly Hedgehog Syndrome (WHS)": "common",
        "Ringworm (Dermatophytosis)": "common",
        "Periodontal Disease": "common",
        "Gingivitis": "common",
        "Pneumonia": "common",
        "Fatty Liver Disease": "common",
        "Hypothermia / Hibernation Attempt": "common",
        "Conjunctivitis": "common",
        "Cutaneous Squamous Cell Carcinoma": "common",
        "Mammary Gland Tumor": "common",
        "Lymphoma": "common",
        "Salmonellosis": "common",
        "Diarrhea (Non-specific)": "common",
        "Ear Infection (Otitis)": "common",
        "Tick Infestation": "common",
        "Flea Infestation": "common",
        # uncommon
        "Dilated Cardiomyopathy": "uncommon",
        "Chronic Kidney Disease": "uncommon",
        "Proptosis (Eye Protrusion)": "uncommon",
        "Uterine Adenocarcinoma": "uncommon",
        "Hemangiosarcoma": "uncommon",
        # rare
        "Herpesvirus Infection": "rare",
        "Balloon Syndrome": "rare",
    },

    # ==================================================================
    # AMPHIBIAN
    # ==================================================================
    "amphibian": {
        "Nematode Infection": "very_common",
        "Aeromonas Infection": "very_common",
        "Aspergillosis": "very_common",
        "Vitamin A Deficiency": "very_common",
        "Chytridiomycosis (Bd)": "very_common",
        "Ranavirus Infection": "common",
        "Red Leg Syndrome": "very_common",
        "Edema / Hydrops (Dropsy)": "common",
        "Stomatitis (Mouth Rot)": "common",
        "Intestinal Impaction": "common",
        "Thermal Burns": "uncommon",
        "Thermal Stress (Hypothermia)": "uncommon",
    },

    # ==================================================================
    # CHINCHILLA
    # ==================================================================
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
        "Intussusception": "uncommon",
        "Intussusception - Chinchilla": "uncommon",
        "Cecal Impaction": "uncommon",
        "Cecal Torsion": "rare",
        "Bloat (Gastric Tympany)": "uncommon",
    },

    # ==================================================================
    # DEGU
    # ==================================================================
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

    # ==================================================================
    # EXOTIC OTHER
    # ==================================================================
    "exotic_other": {
        "Intestinal Parasitism": "very_common",
        "Upper Respiratory Infection": "very_common",
        "Nutritional Deficiency": "very_common",
        "Contact Dermatitis": "very_common",
        "Metabolic Bone Disease": "common",
        "Dermatophytosis (Ringworm)": "common",
        "Lymphoma": "common",
    },

    # ==================================================================
    # LIZARD
    # ==================================================================
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

    # ==================================================================
    # PARAKEET
    # ==================================================================
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

    # ==================================================================
    # PARROT
    # ==================================================================
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
        "Bacterial Pneumonia": "uncommon",
    },

    # ==================================================================
    # SNAKE
    # ==================================================================
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

    # ==================================================================
    # SUGAR GLIDER
    # ==================================================================
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

    # ==================================================================
    # TORTOISE
    # ==================================================================
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
