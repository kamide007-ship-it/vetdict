"""Species prevalence data for stepwise differential diagnosis.

Provides prevalence classifications for diseases across 19 species, used to
weight candidate diagnoses by clinical frequency. See ``SPECIES_PREVALENCE``
for the primary data structure and ``get_prevalence_for_species`` for the
regional adjustments applied to match scores.
"""

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
# DATA SOURCES:
# - Primary: Ettinger & Feldman (2017), Nelson & Couto (2019),
#   Quesenberry & Carpenter (2020), Mader & Divers (2019)
# - Epidemiological: O'Neill et al. (2013) UK dog populations,
#   BanfieldPet Hospital State of Pet Health Reports (2019-2024)
# - Japanese context: 犬と猫の治療薬ガイド EduOne (2024),
#   日本獣医師会 小動物臨床部会 症例統計
#
# LIMITATIONS:
# - Prevalence tiers are primarily based on English-language veterinary
#   literature and may not fully reflect regional differences (e.g.,
#   heartworm is common in Japan but rare in the UK).
# - Exotic species prevalence is less well-documented and relies heavily
#   on clinical experience rather than epidemiological studies.
# - Tiers represent general clinical frequency, not population prevalence.
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
        # Pyotraumatic dermatitis — a top-10 canine presentation in humid
        # summer months (Muller & Kirk 7th ed; Holm 2004, Vet Dermatol).
        "Acute Moist Dermatitis (Hot Spot)": "common",
        # Northern-breed keratinization disorder; classic but not common
        # (White SD, JAVMA 2001; Colombini S, Vet Clin North Am 1999).
        "Zinc-Responsive Dermatosis": "uncommon",
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
        # --- Expanded dog entries (523 additional) ---
        "Acanthomatous Ameloblastoma": "uncommon",
        "Acetaminophen Toxicosis": "common",
        "Acral Lick Dermatitis": "very_common",
        "Alopecia X": "uncommon",
        "Anal Sac Adenocarcinoma": "uncommon",
        "Anaplasmosis": "uncommon",
        "Anticoagulant Rodenticide Toxicosis": "common",
        "Aortic Stenosis": "uncommon",
        "Aspiration Pneumonia": "common",
        "Atrial Fibrillation": "uncommon",
        "Aural Hematoma": "common",
        "Babesiosis": "uncommon",
        "Benign Prostatic Hyperplasia": "common",
        "Brachycephalic Airway Syndrome": "common",
        "Brain Tumor": "uncommon",
        "Boxer Arrhythmogenic Right Ventricular Cardiomyopathy": "common",
        "Caffeine Toxicosis": "common",
        "Canine Atopic Dermatitis": "very_common",
        "Canine Cognitive Dysfunction Syndrome": "common",
        "Canine Distemper": "common",
        "Canine Infectious Hepatitis": "common",
        "Canine Papillomatosis": "common",
        "Cavalier King Charles Spaniel Mitral Valve Disease (Early-Onset)": "common",
        "Chocolate Toxicosis": "common",
        "Chronic Bronchitis": "common",
        "Chronic Hepatitis": "common",
        "Chronic Otitis Media": "very_common",
        "Chylothorax": "uncommon",
        "Cognitive Dysfunction Syndrome (CDS)": "common",
        "Colitis": "common",
        "Corneal Dystrophy": "common",
        "Cranial Cruciate Ligament Rupture": "common",
        "Cutaneous Histiocytoma": "common",
        "Degenerative Myelopathy": "uncommon",
        "Diabetic Ketoacidosis (DKA)": "uncommon",
        "Diaphragmatic Hernia": "uncommon",
        "Discospondylitis": "uncommon",
        "Disseminated Intravascular Coagulation (DIC)": "uncommon",
        "Doberman Dilated Cardiomyopathy (Occult)": "common",
        "Dystocia": "common",
        "Ear Mite Infestation (Otodectes)": "common",
        "Eclampsia (Milk Fever)": "common",
        "Ectropion": "common",
        "Ehrlichiosis": "uncommon",
        "Elbow Dysplasia": "common",
        "Entropion": "common",
        "Esophageal Foreign Body": "common",
        "Ethylene Glycol Poisoning (Antifreeze)": "uncommon",
        "Eye Infection (Conjunctivitis)": "very_common",
        "Fear Aggression": "common",
        "Fibrosarcoma": "uncommon",
        "Gallbladder Mucocele": "uncommon",
        "Gastric Foreign Body": "common",
        "Grape/Raisin Toxicosis": "common",
        "Hemorrhagic Gastroenteritis (HGE)": "very_common",
        "Histiocytic Sarcoma": "rare",
        "Hookworm Infection": "very_common",
        "Horner's Syndrome": "uncommon",
        "Hydrocephalus": "uncommon",
        "Immune-Mediated Polyarthritis": "uncommon",
        "Inner Ear Infection (Otitis Interna)": "very_common",
        "Keratoconjunctivitis Sicca (Dry Eye)": "very_common",
        "Laryngeal Paralysis": "uncommon",
        "Lens Luxation": "common",
        "Malassezia Dermatitis": "very_common",
        "Marijuana Toxicosis": "common",
        "Masticatory Muscle Myositis": "uncommon",
        "Medial Patellar Luxation": "common",
        "Melanoma": "uncommon",
        "Meningioma": "uncommon",
        "Mushroom Toxicosis": "common",
        "NSAID Toxicosis": "common",
        "Nasal Tumor": "uncommon",
        "Nictitans Gland Prolapse (Cherry Eye)": "common",
        "Noise Phobia": "common",
        "Oral Melanoma": "uncommon",
        "Oral Papillomatosis": "common",
        "Osteosarcoma": "uncommon",
        "Panosteitis": "uncommon",
        "Patent Ductus Arteriosus (PDA)": "uncommon",
        "Pemphigus Foliaceus": "uncommon",
        "Perianal Fistula": "uncommon",
        "Pericardial Effusion": "uncommon",
        "Perineal Hernia": "uncommon",
        "Pneumonia": "common",
        "Progressive Retinal Atrophy (PRA)": "uncommon",
        "Prostatic Abscess": "common",
        "Protein-Losing Enteropathy (PLE)": "uncommon",
        "Pulmonary Hypertension": "uncommon",
        "Pyelonephritis": "common",
        "Rabies": "uncommon",
        "Rodenticide Poisoning": "common",
        "Roundworm Infection (Toxocara)": "common",
        "Sago Palm Toxicosis": "common",
        "Salmon Poisoning Disease": "common",
        "Sarcoptic Mange (Scabies)": "common",
        "Separation Anxiety": "common",
        "Snail Bait (Metaldehyde) Poisoning": "common",
        "Splenic Hemangiosarcoma": "uncommon",
        "Squamous Cell Carcinoma": "uncommon",
        "Steroid-Responsive Meningitis-Arteritis (SRMA)": "uncommon",
        "Tapeworm Infection (Dipylidium/Echinococcus)": "common",
        "Testicular Tumor": "common",
        "Thyroid Carcinoma": "uncommon",
        # Tick paralysis is region-bound (Ixodes holocyclus in Australia,
        # Dermacentor in N.America) — uncommon at best outside those areas.
        "Tick Paralysis": "uncommon",
        "Tooth Abscess": "common",
        "Tooth Fracture": "common",
        "Transitional Cell Carcinoma": "uncommon",
        "Uterine Stump Pyometra": "common",
        "Vestibular Disease": "common",
        "Vitamin D Toxicosis": "common",
        "Whipworm Infection (Trichuris)": "common",
        "Xylitol Poisoning": "common",
        "Zinc Toxicosis": "common",
        "von Willebrand Disease": "uncommon",
    },
    # ==================================================================
    # CAT — 230+ entries (expanded from ~73)
    # ==================================================================
    "cat": {
        # Neoplasia/toxicosis tiers: a bare 「しこり」 query ranked injection-site
        # sarcomas and melanoma above abscess/MCT; PU/PD queries ranked
        # cholecalciferol rodenticide toxicosis above CKD.
        "Feline Injection Site Sarcoma (FISS / Vaccine-Associated Sarcoma)": "uncommon",
        "Feline Vaccine-Associated Sarcoma (Non-Injection Site)": "rare",
        "Feline Melanoma": "rare",
        "Feline Cholecalciferol Rodenticide Toxicosis": "rare",
        "Feline Psychogenic Polydipsia": "uncommon",
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
        # --- Expanded cat entries (80+ additional) ---
        # very_common
        "Gingivitis and Periodontal Disease": "very_common",
        "Cat Bite Abscess": "very_common",
        "Foreign Body Obstruction": "very_common",
        "Feline Acne": "very_common",
        "Feline Chronic Vomiting (Idiopathic)": "very_common",
        "Feline Gastric Hairball Obstruction": "very_common",
        "Feline Linear Foreign Body": "very_common",
        "Feline Litter Box Aversion": "very_common",
        "Territorial Marking / Urine Spraying": "very_common",
        # common — seen monthly
        "Asthma": "common",
        "Chronic Kidney Disease": "common",
        "Chronic Rhinosinusitis": "common",
        "Cataracts": "common",
        "Feline Anxiety Disorder": "common",
        "Feline Cognitive Dysfunction Syndrome": "common",
        "Feline Herpesviral Keratitis": "common",
        "Feline Chronic Bronchitis": "common",
        "Feline Chronic Colitis": "common",
        "Feline Chronic Pancreatitis": "common",
        "Feline Eosinophilic Keratoconjunctivitis": "common",
        "Eosinophilic Granuloma Complex - Eosinophilic Plaque": "common",
        "Eosinophilic Granuloma Complex - Eosinophilic Ulcer": "common",
        "Eosinophilic Granuloma Complex - Linear Granuloma": "common",
        "Feline Oral Eosinophilic Granuloma": "common",
        "Feline Malassezia Dermatitis": "common",
        "Feline Cheyletiellosis (Walking Dandruff)": "common",
        "Feline Symmetric Alopecia": "common",
        "Feline Tail Gland Hyperplasia (Stud Tail)": "common",
        "Feline Anal Sac Disease": "common",
        "Feline Aural Hematoma": "common",
        "Entropion": "common",
        "Glaucoma": "common",
        "Retinal Detachment": "common",
        "Hypertensive Retinopathy": "common",
        "Feline Iris Melanosis": "common",
        "Tooth Root Abscess": "common",
        "Nasopharyngeal Polyp": "common",
        "Feline Nasal Polyp": "common",
        "Heartworm-Associated Respiratory Disease (HARD)": "common",
        "Pyometra": "common",
        "Dystocia (Difficult Birth)": "common",
        "Cryptorchidism": "common",
        "Mammary Hyperplasia (Fibroadenomatous Change)": "common",
        # Triple-negative is a molecular subtype of feline mammary carcinoma,
        # not an independently common diagnosis — the parent "Mammary Tumor"
        # (3rd most common feline tumor) carries the common tier.
        "Feline Mammary Carcinoma (Triple Negative)": "uncommon",
        # Overt pseudopregnancy is rare in queens (unlike bitches) because
        # ovulation is induced — Little, The Cat: Clinical Medicine & Management.
        "Pseudopregnancy (Feline)": "rare",
        "Mast Cell Tumor (Cutaneous)": "common",
        "Feline Congestive Heart Failure": "common",
        "Feline Arterial Hypertension (Secondary)": "common",
        "Pica": "common",
        "Redirected Aggression": "common",
        "Separation Anxiety": "common",
        "Feline Hyperesthesia Syndrome": "common",
        "Triaditis": "common",
        "Feline Neutrophilic Cholangitis": "common",
        "Feline Lymphocytic Cholangitis": "common",
        "Feline Struvite Urolithiasis": "common",
        "Feline Calcium Oxalate Urolithiasis": "common",
        "Urinary Obstruction (Blocked Cat)": "common",
        "Feline Urethral Plug": "common",
        "Acute Kidney Injury (AKI)": "common",
        "Lily Toxicosis": "common",
        "Permethrin Toxicosis": "common",
        "Rodenticide Poisoning (Anticoagulant)": "uncommon",
        "Acetaminophen (Paracetamol) Toxicosis": "common",
        "Feline Pyrethroid Toxicosis (Topical)": "common",
        "Fracture": "common",
        "High-Rise Syndrome": "common",
        # uncommon — several times per year
        "FIP Neurological Form": "uncommon",
        "Feline Infectious Anemia (Hemoplasma)": "uncommon",
        "Mycoplasma haemofelis Infection (Feline Infectious Anemia)": "uncommon",
        "Cryptococcosis": "uncommon",
        "Toxoplasmosis": "uncommon",
        "Feline Congenital Portosystemic Shunt": "uncommon",
        "Feline Hepatic Amyloidosis": "uncommon",
        "Chylothorax": "uncommon",
        "Pleural Effusion": "uncommon",
        "Pyothorax": "uncommon",
        "Feline Pneumothorax": "uncommon",
        "Diaphragmatic Hernia": "uncommon",
        "Mediastinal Lymphoma": "uncommon",
        "Nasal Lymphoma": "uncommon",
        "Hepatic Lymphoma": "uncommon",
        "Large Granular Lymphocyte Lymphoma": "uncommon",
        "Meningioma": "uncommon",
        "Osteosarcoma": "uncommon",
        "Basal Cell Tumor": "uncommon",
        "Feline Cutaneous Lymphoma": "uncommon",
        "Feline Fibrosarcoma (Non-Injection Site)": "uncommon",
        "Hemangiosarcoma": "uncommon",
        "Feline Oral Squamous Cell Carcinoma (Sublingual)": "uncommon",
        "Feline Squamous Cell Carcinoma (Nasal Planum)": "uncommon",
        "Intestinal Adenocarcinoma": "uncommon",
        "Feline Pancreatic Adenocarcinoma": "uncommon",
        "Feline Taurine Deficiency Cardiomyopathy": "uncommon",
        "Feline Hypertrophic Cardiomyopathy (Obstructive)": "uncommon",
        "Feline Mitral Valve Disease": "uncommon",
        "Corneal Sequestrum": "uncommon",
        "Feline Dry Eye (Keratoconjunctivitis Sicca)": "uncommon",
        "Feline Idiopathic Vestibular Disease": "uncommon",
        "Vestibular Disease": "uncommon",
        "Feline Audiogenic Reflex Seizures (FARS)": "uncommon",
        "Feline Status Epilepticus": "uncommon",
        "Feline Megaesophagus": "uncommon",
        "Feline Idiopathic Megacolon": "uncommon",
        "Feline Toxic Megacolon": "uncommon",
        "Immune-Mediated Polyarthritis": "uncommon",
        "Immune-Mediated Thrombocytopenia (ITP)": "uncommon",
        "Feline Exocrine Pancreatic Insufficiency (EPI)": "uncommon",
        "Ethylene Glycol (Antifreeze) Poisoning": "uncommon",
        "NSAID Toxicosis": "uncommon",
        "Feline Onion/Garlic Toxicosis": "uncommon",
        "Feline Marijuana Toxicosis": "uncommon",
        "Essential Oil Toxicosis": "uncommon",
        "Hypokalemic Polymyopathy": "uncommon",
        "Nutritional Secondary Hyperparathyroidism": "uncommon",
        "Thiamine Deficiency (Vitamin B1)": "uncommon",
        "Feline Stomatitis (Non-Lymphoplasmacytic)": "uncommon",
        "Feline Protein-Losing Enteropathy": "uncommon",
        "Pyelonephritis": "uncommon",
        "Feline Ureteral Obstruction": "uncommon",
        "Feline Bordetellosis": "uncommon",
        "Feline Pneumonia": "uncommon",
        "Pulmonary Edema": "uncommon",
        "Feline Compulsive Disorder": "uncommon",
        "Feline Night Vocalization Syndrome": "uncommon",
        "Cerebellar Hypoplasia": "uncommon",
        "Hydrocephalus": "uncommon",
        "Hip Dysplasia": "uncommon",
        "Luxating Patella": "uncommon",
        "Scottish Fold Osteochondrodysplasia": "uncommon",
        # rare — <0.5% prevalence
        "Feline Primary Hyperaldosteronism (Conn's Syndrome)": "rare",
        "Feline Pheochromocytoma": "rare",
        "Insulinoma": "rare",
        "Hyperadrenocorticism (Cushing's Disease)": "rare",
        "Hypoadrenocorticism (Addison's Disease)": "rare",
        "Feline Hyperparathyroidism (Primary)": "rare",
        "Feline Pituitary Dwarfism": "rare",
        "Pituitary Tumor": "rare",
        "Feline Acquired Myasthenia Gravis": "rare",
        "Systemic Lupus Erythematosus (SLE)": "rare",
        "Feline Degenerative Myelopathy": "rare",
        "Feline Ischemic Encephalopathy": "rare",
        "Dysautonomia (Key-Gaskell Syndrome)": "rare",
        "Plague (Yersinia pestis)": "rare",
        "Tularemia": "rare",
        "Feline Leishmaniasis": "rare",
        "Feline Leptospirosis": "rare",
        "Rabies": "rare",
        "Feline Botulism": "rare",
        "Cytauxzoon felis (Acute Cytauxzoonosis)": "rare",
        # Neonatal isoerythrolysis: restricted to type-B queen × type-A kitten
        # matings and the first days of life — must never outrank hepatic
        # lipidosis/cholangitis for an adult icterus complaint (round-14 audit:
        # the untiered NI entries took rank 1 for jaundice + lethargy).
        "Neonatal Isoerythrolysis": "rare",
        "Feline Neonatal Isoerythrolysis (Type B Queen x Type A Kitten)": "rare",
        "Feline Hemophilia A": "rare",
        "Feline von Willebrand Disease": "rare",
        "Disseminated Intravascular Coagulation (DIC)": "rare",
        "Feline Pythiosis": "rare",
        "Feline Histoplasmosis": "rare",
        "Sporotrichosis": "rare",
        "Lissencephaly": "rare",
        "Manx Syndrome": "rare",
        "Polydactyly": "rare",
    },
    # ==================================================================
    # HORSE — curated equine tiers (keys match equine DB names exactly)
    # Evidence: Reed & Bayly Equine Internal Medicine 4th ed; NAHMS Equine
    # 2015; Sykes 2015 ECEIM EGUS consensus; Wylie 2011 (laminitis);
    # McIlwraith 2012 (OA); Couetil 2016 equine asthma consensus;
    # McFarlane 2011 (PPID); Gerding & Gilger 2016 (ERU)
    # ==================================================================
    "horse": {
        # Colic-subtype and misc tiers: without these, single-finding colic
        # queries ranked uterine torsion / hydrops above the everyday causes
        # (subtype shares per Reed & Bayly 4th ed / surgical colic series).
        "Nephrosplenic Entrapment": "uncommon",
        "Intussusception": "uncommon",
        "Pedunculated Lipoma": "uncommon",
        "Uterine Torsion": "rare",
        "Hydrops (Allantois/Amnion)": "rare",
        "Deep Digital Flexor Tendinitis": "uncommon",
        "Black Walnut Toxicity": "rare",
        # very_common
        "Colic": "very_common",  # Leading equine emergency (NAHMS: 4-10/100 horse-yr)
        "Gastric Ulcers (EGUS)": "very_common",  # 37-93% by discipline (Sykes 2015)
        "Osteoarthritis": "very_common",  # Leading cause of lameness (McIlwraith 2012)
        "Internal Parasites": "very_common",  # Cyathostomins ubiquitous
        "Hoof Abscess": "very_common",  # Most common cause of acute severe lameness
        "Thrush": "very_common",  # Ubiquitous frog infection in wet management
        # common
        "Laminitis": "common",  # Wylie 2011: 1.5-34% prevalence estimates
        "Equine Asthma (IAD/RAO)": "common",  # Stabled horses (Couetil 2016)
        "Equine Sarcoid": "common",  # Most common equine skin tumor
        "Melanoma": "common",  # ~80% lifetime risk in gray horses
        "Sweet Itch (Culicoides Hypersensitivity)": "common",  # Most common allergic dermatosis
        "Dermatophilosis (Rain Scald)": "common",
        "Dermatophytosis (Ringworm)": "common",
        "Scratches (Pastern Dermatitis)": "common",
        "Urticaria (Hives)": "common",
        "Corneal Ulcer": "common",  # Most common equine ophthalmic emergency
        "Equine Recurrent Uveitis": "common",  # Leading cause of equine blindness
        "Pituitary Pars Intermedia Dysfunction": "common",  # >20% of aged horses
        "Equine Metabolic Syndrome (EMS)": "common",
        "Superficial Digital Flexor Tendinitis": "common",  # Athletic horses
        "Proximal Suspensory Desmitis": "common",  # Sport horses
        "Navicular Syndrome": "common",
        "Exertional Rhabdomyolysis (Tying Up)": "common",
        "Back Pain": "common",
        "Kissing Spines": "common",  # Radiographic ORDSP up to 39% (Zimmerman)
        "Splints": "common",  # Young working horses
        "Bone Spavin": "common",
        "Osteochondritis Dissecans": "common",  # Young sport horses
        "Angular Limb Deformities": "common",  # Foals
        "Strangles": "common",
        "Equine Influenza": "common",
        "Equine Herpesvirus (EHV-1/4)": "common",
        "Esophageal Obstruction (Choke)": "common",
        "Endometritis": "common",  # No.1 cause of broodmare subfertility
        "Retained Fetal Membranes": "common",  # 2-10% of foalings
        "Wound Infection": "common",
        "Cellulitis": "common",
        "White Line Disease": "common",
        # uncommon
        "Sand Colic": "uncommon",  # Region/management dependent
        "Enterolithiasis": "uncommon",
        "Colitis": "uncommon",
        # Esophageal disorders other than choke are genuinely infrequent in
        # horses (Reed & Bayly 4th ed) — untiered they outranked choke itself
        # on trivially perfect coverage for the ptyalism/dysphagia complaint.
        "Esophageal Stricture": "uncommon",
        "Megaesophagus": "uncommon",
        "Pleuropneumonia": "uncommon",
        "Sinusitis": "uncommon",
        "Guttural Pouch Empyema": "uncommon",
        "Guttural Pouch Mycosis": "uncommon",
        # 2026-09: 発熱+鼻汁の主訴で腺疫(common)より上位に出ていた汎用
        # アスペルギルス症エントリを実際の頻度に整合。肺型/全身性は免疫不全馬の
        # 稀な日和見感染、喉嚢真菌症型の主徴は鼻出血であり発熱+鼻汁の
        # ルーチン鑑別ではない（Reed & Bayly 4th ed）
        "Aspergillosis": "rare",
        "Tetanus": "uncommon",  # Vaccination-dependent
        "Cataracts": "uncommon",
        "Anhidrosis": "uncommon",  # Hot/humid climates
        "Equine Hyperlipemia": "uncommon",  # Ponies, donkeys, miniatures
        "Babesiosis": "uncommon",  # Tick-borne; JP override raises to common
        "Equine Protozoal Myeloencephalitis": "uncommon",  # Americas; JP override rare
        "West Nile Encephalitis": "uncommon",  # JP override rare
        "Rhodococcus equi Pneumonia (Foal)": "uncommon",  # Endemic farms
        "Neonatal Septicemia": "uncommon",
        "Fracture": "uncommon",
        "Lymphangitis": "uncommon",
        "Placentitis": "uncommon",
        "Cryptorchidism": "uncommon",
        "Bog Spavin": "uncommon",
        "Ringbone": "uncommon",
        "Habronemiasis (Summer Sores)": "uncommon",
        # rare
        "Canker": "rare",
        "Esophageal Diverticulum": "rare",  # Reed & Bayly 4th ed
        "Equine Sialolithiasis": "rare",
        "Botulism": "rare",
        "Mange": "rare",
        "Getah Virus": "rare",  # Asia-specific; JP override common
        "Japanese Encephalitis": "rare",  # Asia-specific; JP override common
        "African Horse Sickness": "rare",
        "Dourine": "rare",
        "Venezuelan Equine Encephalomyelitis": "rare",
        # -- 2026-09 Round 19: ophthalmic variant entries were untiered, so
        # rare diseases (lens luxation / habronemiasis / eyeworm) outranked
        # the high-frequency corneal ulcer / uveitis family on the classic
        # squinting + tearing complaint (Brooks, Equine Ophthalmology 3rd ed;
        # Gilger, Equine Ophthalmology).
        "Superficial Corneal Ulcer": "very_common",
        "Anterior Uveitis": "common",
        "Equine Recurrent Uveitis (Moon Blindness)": "common",
        "Deep / Melting Corneal Ulcer": "uncommon",
        "Fungal Keratitis": "uncommon",
        "Stromal Abscess": "uncommon",
        "Immune-Mediated Keratitis": "uncommon",
        "Nasolacrimal Duct Obstruction": "uncommon",
        "Ocular Habronemiasis": "uncommon",
        "Lens Luxation": "rare",
        "Eyeworm Disease": "rare",
        "Neurofibroma": "rare",
        # -- 2026-09 Round 19: spinal-ataxia differential — CVSM (Wobbler) is
        # the most common non-infectious spinal ataxia (Reed & Bayly 4th ed)
        # yet was untiered, while exotic encephalitides topped the list.
        "Cervical Vertebral Stenotic Myelopathy": "common",
        "Cervical Vertebral Malformation": "common",
        "Cervical Vertebral Stenotic Myelopathy Type II": "uncommon",
        "EHV-1 Myeloencephalopathy": "uncommon",
        "EHV-1 Myeloencephalopathy (EHM)": "uncommon",
        "Equine Degenerative Myeloencephalopathy": "uncommon",
        "Equine Neuroaxonal Dystrophy": "uncommon",
        "Hyponatremia": "uncommon",
        "Western Equine Encephalomyelitis": "rare",  # Americas; absent in JP
        "Eastern/Western Equine Encephalomyelitis": "rare",
        "Equine Encephalosis Virus": "rare",  # African orbivirus
        "Nipah Virus": "rare",
        # 2026-09: 豪州限定（オオコウモリ媒介）の人獣共通感染症 — 発熱+鼻汁の
        # ルーチン鑑別で上位に出ないよう Nipah と同様に rare を明示
        "Hendra Virus": "rare",
        "Cryptococcosis": "rare",
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
        # Rabbit megacolon is a congenital syndrome of En/En homozygous spotted
        # rabbits (KIT-associated aganglionosis) — genuinely rare in practice,
        # while GI stasis presents with the same small/scant pellets daily.
        "Megacolon": "rare",
        "Ileus (Paralytic)": "uncommon",
        "Colonic Impaction": "uncommon",
        "Sarcoptic Mange": "uncommon",
        "Thymoma": "uncommon",
        "Lymphoma": "uncommon",
        # Dental-origin retrobulbar abscess is a common rabbit exophthalmos
        # presentation (Harcourt-Brown, Textbook of Rabbit Medicine); the
        # elodontoma/pseudo-odontoma is primarily a degu/prairie-dog disease
        # and rare in rabbits (Capello & Lennox) — round-14 audit: the
        # untiered Elodontoma outranked the abscess for 眼球突出+鼻水.
        "Retrobulbar Abscess": "common",
        "Retrobulbar Dental Abscess": "common",
        "Elodontoma": "rare",
        # rare
        "Klebsiella Pneumonia": "rare",
        "Cecoliths": "rare",
        "Pulmonary Oedema": "rare",
        "Pulmonary Fibrosis": "rare",
        "Pyothorax": "rare",
        "Cecal Tympany": "rare",
        # --- Expanded rabbit entries ---
        "Cheek Tooth Overgrowth": "very_common",
        "Barbering (Fur Chewing)": "very_common",
        "Cecotrophy Disorders": "very_common",
        "Alopecia (Non-specific)": "very_common",
        "Constipation": "common",
        "Corneal Ulcer": "common",
        "Cataracts": "common",
        "Chronic Kidney Disease": "common",
        "Clostridial Enterotoxemia": "common",
        "Colitis": "common",
        "Cystitis": "common",
        "Heatstroke (Neurological)": "common",
        "Mastitis": "common",
        "Dehydration": "common",
        "Bladder Sludge (Hypercalciuria)": "common",
        "Cuterebra (Bot Fly Larva)": "uncommon",
        "Congestive Heart Failure": "uncommon",
        "Hepatic Lipidosis": "uncommon",
        "Dystocia": "uncommon",
        "Splenic Torsion": "rare",
        "Chordoma": "rare",
        "Buphthalmia (Congenital Glaucoma)": "rare",
        "Cerebellar Hypoplasia": "rare",
        # Acute-abdomen tiers: without these, the 2-sign presentation
        # "anorexia + distension" ranked case-report rarities (ectopic
        # pregnancy) above the everyday GI emergencies (Oglesbee 2nd ed).
        "Gastric Dilation (Bloat)": "common",
        "Intestinal Obstruction": "common",
        "Peritonitis": "uncommon",
        "Ectopic Pregnancy": "rare",
        # --- Additional rabbit entries ---
        "Encephalitozoonosis": "very_common",
        "Cheyletiella Mange (Fur Mites)": "very_common",
        "Dental Abscess": "very_common",
        "Dental Fistula": "common",
        "Periodontal Disease": "common",
        "E. coli Enteritis": "common",
        "Mucoid Enteropathy": "common",
        "Giardiasis": "common",
        "Bordetella Bronchiseptica Infection": "common",
        "Dewlap Fold Dermatitis": "common",
        "Red Urine (Non-pathological)": "common",
        "Urine Scald": "common",
        "Pseudopregnancy": "common",
        "Hutch Burn": "common",
        "Nail Overgrowth": "common",
        "Flystrike (Myiasis)": "common",
        "Rhinitis": "common",
        "Staphylococcal Dermatitis": "uncommon",
        "Enterotoxemia": "uncommon",
        "Diabetes Mellitus": "uncommon",
        "Endometrial Hyperplasia": "uncommon",
        "Rabbit Hemorrhagic Disease (RHD)": "uncommon",
        "Tyzzer Disease": "rare",
        "Rabbit Poxvirus Infection": "rare",
    },
    # ==================================================================
    # BIRD — 28+ entries (expanded from ~16)
    # ==================================================================
    "bird": {
        # Exposure-dependent toxicoses / incidental hemoparasites (see parakeet).
        "Copper Poisoning": "rare",
        "PTFE / Teflon Toxicosis": "rare",
        "Teflon/PTFE Toxicosis": "rare",
        "Essential Oil Toxicity": "rare",  # Exposure-dependent; untiered it outranked hypocalcemia for post-laying tremors
        "Blood Parasites (Haemoproteus)": "uncommon",
        # very_common
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
        "Megabacteriosis (AGY)": "common",
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
        "Prolapse of Cloaca": "uncommon",
        # --- Expanded bird entries ---
        "Avian Pox": "very_common",
        "Knemidocoptes (Scaly Face/Leg Mites)": "very_common",
        "Giardiasis": "very_common",
        "Trichomoniasis": "very_common",
        "Pacheco's Disease (Psittacid Herpesvirus)": "common",
        "Crop Burns": "common",
        "Mycobacteriosis (Avian TB)": "common",
        "Renal Failure (Acute / Chronic)": "common",
        "Iodine Deficiency (Thyroid Hyperplasia)": "common",
        "Cloacitis": "common",
        "Xanthomas": "common",
        "Cloacal Papillomatosis": "common",
        "Feather Cyst": "common",
        "Zinc Toxicosis": "common",
        "Lead Poisoning": "common",
        "Arteriosclerosis": "common",
        "Ovarian Tumor": "uncommon",
        "Renal Tumor": "uncommon",
        "Choanal Atresia": "uncommon",
        "Avian Influenza": "rare",
        "Fibrosarcoma": "rare",
        # --- Additional bird entries ---
        "Roundworm (Ascaridia)": "very_common",
        "Lice (Mallophaga)": "very_common",
        "Red Mite (Dermanyssus)": "very_common",
        "Feather Mites": "very_common",
        "Egg Binding": "common",
        "Egg Peritonitis": "common",
        "Chronic Egg Laying": "common",
        "Salpingitis": "common",
        "Iron Storage Disease (Hemochromatosis)": "common",
        "Fatty Liver Disease": "common",
        "Tracheal Mite (Sternostoma)": "common",
        "Capillaria (Hairworm)": "common",
        "Syngamus (Gapeworm)": "common",
        "Fracture (Wing)": "common",
        "Fracture (Leg)": "common",
        "Night Fright Injury": "common",
        "Crop Impaction": "common",
        "Foreign Body Ingestion": "common",
        "Psittacosis (Chlamydiosis)": "common",
        # Vector-borne blood parasite of outdoor/free-ranging birds — rare in
        # pet psittacines; untiered it outranked psittacosis on green droppings.
        "Leucocytozoonosis": "uncommon",
        "Avian Leucocytozoonosis": "uncommon",
        # Exposure-dependent toxicosis (same precedent as copper/PTFE = rare) —
        # untiered it topped the fluffed+green-droppings sick-bird complaint.
        "Avocado Toxicity": "rare",
        "Salmonellosis": "uncommon",
        "Squamous Cell Carcinoma": "uncommon",
        "Lipoma": "uncommon",
        "Pituitary Tumor": "uncommon",
        "Testicular Tumor": "uncommon",
        "Hepatocellular Carcinoma": "rare",
        "Hemangiosarcoma": "rare",
        # Poultry pathogens (ORT / avian metapneumovirus) — essentially absent
        # in pet psittacines/passerines; untiered they outranked sinusitis
        # (common) on the sneezing + nasal-discharge complaint.
        "Ornithobacterium rhinotracheale (ORT) Infection": "rare",
        "Ornithobacterium rhinotracheale (ORT) Pneumonia": "rare",
        "Avian Metapneumovirus Infection": "rare",
        "Avian Metapneumovirus Rhinotracheitis": "rare",
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
        "Vitamin A Deficiency": "very_common",
        "External Mites (Ophionyssus)": "very_common",
        "Dehydration": "very_common",
        # common
        "Infectious Stomatitis (Mouth Rot)": "common",
        "Gastrointestinal Impaction": "common",
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
        "Septicemia": "uncommon",
        "Hepatic Lipidosis (Fatty Liver Disease)": "uncommon",
        # rare
        "Adenovirus Infection": "rare",
        "Paramyxovirus Infection": "rare",
        # --- Expanded reptile entries ---
        "Bacterial Dermatitis": "very_common",
        "Herpesvirus Infection": "common",
        "Cloacal Prolapse": "common",
        "Flagellate Protozoal Infection": "common",
        "Obesity": "common",
        "Aural Abscess (Ear Abscess)": "common",
        "Hypocalcemia": "common",
        "Osteomyelitis": "uncommon",
        "Renal Failure (Chronic Kidney Disease)": "uncommon",
        "Hemipenal Prolapse": "uncommon",
        "Nematode Infection": "very_common",
        "Dermal Mycosis (Non-CANV Fungal Dermatitis)": "uncommon",
        "Hepatic Lipidosis": "uncommon",
        "Salmonellosis": "uncommon",
        "Neoplasia (General)": "uncommon",
        "Pentastomid Infection": "rare",
        "Chlamydiosis": "rare",
        "Mycobacteriosis": "rare",
        "Iridovirus Infection": "rare",
        "Intestinal Volvulus / Intussusception": "rare",
        # --- Additional reptile entries ---
        "Stomatitis (Mouth Rot)": "very_common",
        "Mite Infestation (Ophionyssus)": "very_common",
        "Constipation": "very_common",
        "Substrate Impaction": "common",
        "Blister Disease": "common",
        "Gout (Articular)": "common",
        "Gout (Visceral)": "common",
        "Burns": "common",
        "Fracture (Limb)": "common",
        "Foreign Body Ingestion": "common",
        "Conjunctivitis": "common",
        "Corneal Ulcer": "common",
        "Bite Wounds": "common",
        "Spectacle Retention": "common",
        "Egg Yolk Coelomitis": "uncommon",
        "Hexamita Infection": "uncommon",
        "Lymphoma": "uncommon",
        "Squamous Cell Carcinoma": "uncommon",
        "Fibrosarcoma": "uncommon",
        "Poxvirus Infection": "rare",
        "Sunshine Virus (Sunshinevirus)": "rare",
    },
    # ==================================================================
    # FISH — 25 entries (expanded from ~10)
    # ==================================================================
    "fish": {
        # very_common
        "Ichthyophthirius (White Spot Disease / Ich)": "very_common",
        "Fin Rot (Bacterial/Fungal)": "very_common",
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
        "Dermatophytosis (Ringworm)": "common",
        "Mammary Gland Tumor": "common",
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
        "Adrenal Gland Tumor": "uncommon",
        # rare
        "Lymphocytic Choriomeningitis (LCMV)": "rare",
        # --- Expanded hamster entries ---
        "Cheek Pouch Abscess": "very_common",
        "Acariasis (Mite Infestation)": "very_common",
        "Barbering": "very_common",
        "Ear Infection (Otitis)": "common",
        "Rectal Prolapse": "common",
        "Heat Stroke": "common",
        "Pyometra": "common",
        "Testicular Tumor": "common",
        "Skin Tumor (General)": "common",
        "Intussusception": "common",
        "Uterine Tumor": "common",
        "Constipation": "common",
        "Hypothermia": "common",
        "Incisor Malocclusion": "common",
        "Abdominal Tumor": "uncommon",
        "Hepatic Lipidosis": "uncommon",
        "Atrial Thrombosis": "uncommon",
        "Hyperthyroidism": "rare",
        "Cerebellar Ataxia": "rare",
        # --- Additional hamster entries ---
        "Hamster Polyomavirus - Clinical Form": "very_common",
        "Chromodacryorrhea (Red Tears)": "very_common",
        "Cheek Pouch Eversion": "common",
        "Cheek Pouch Mycosis": "common",
        "Hibernation Attempt (Torpor)": "common",
        "Flank Gland Hyperplasia": "common",
        "Flank Gland Tumor": "common",
        "Corneal Ulcer": "common",
        "Pinworm Infection (Syphacia)": "common",
        "Helicobacter Gastritis": "common",
        "Scent Gland Infection": "common",
        "Eye Proptosis": "common",
        "Fracture (Limb)": "common",
        "Exercise Wheel Injury": "common",
        "Bite Wounds": "common",
        "Mammary Adenocarcinoma": "uncommon",
        "Harderian Gland Tumor": "uncommon",
        "Pituitary Tumor": "uncommon",
        "Sendai Virus Infection": "uncommon",
        "Amyloidosis - Hepatic": "uncommon",
        "Tyzzer's Disease": "rare",
        "Cerebrovascular Accident (Stroke)": "rare",
        "Pneumocystis Pneumonia": "rare",
    },
    # ==================================================================
    # GUINEA PIG — 25+ entries (expanded from ~14)
    # ==================================================================
    "guinea_pig": {
        # very_common
        "Scurvy (Vitamin C Deficiency)": "very_common",
        "Upper Respiratory Infection (URI)": "very_common",
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
        "Urolithiasis": "common",
        "GI Stasis": "common",
        "Obesity": "common",
        "Barbering": "common",
        "Bladder Sludge": "common",
        "Urinary Tract Infection": "common",
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
        # --- Expanded guinea pig entries ---
        "Cervical Lymphadenitis": "very_common",
        "Lice Infestation (Gliricola/Gyropus)": "very_common",
        "Heat Stroke": "very_common",
        "Abscess (Subcutaneous)": "common",
        "Alopecia": "common",
        "Cystitis": "common",
        "Dystocia": "common",
        "Bloat (Gastric Dilation)": "common",
        "Intestinal Torsion": "common",
        "Mammary Tumors": "common",
        "Trichofolliculoma": "common",
        "Adenovirus Pneumonia": "common",
        "Rectal Prolapse": "common",
        "Pedal Abscess": "common",
        "Hepatic Lipidosis": "uncommon",
        "Heart Disease (Cardiomyopathy)": "uncommon",
        "Hyperthyroidism": "uncommon",
        "Fibrosarcoma": "rare",
        "Osteosarcoma": "rare",
        # --- Additional guinea pig entries ---
        "Hay Poke Injury": "very_common",
        "Chirodiscoides caviae Infestation": "very_common",
        "Nail Overgrowth": "very_common",
        "Chlamydiosis (Chlamydia caviae)": "common",
        "Bordetella Pneumonia": "common",
        "Bumblefoot (Pododermatitis)": "common",
        "Boar Glue (Excessive Grease Gland Secretion)": "common",
        "Corneal Ulcer": "common",
        "Perineal Sac Impaction": "common",
        "Dental Abscess": "common",
        "Gastric Ulcers": "common",
        "Flystrike (Myiasis)": "common",
        "Ileus": "common",
        "Ovarian Cysts - Follicular": "common",
        "Slobbers (Dental-related Ptyalism)": "common",
        "Cecal Dysbiosis": "uncommon",
        "Dilated Cardiomyopathy": "uncommon",
        "Intestinal Adenocarcinoma": "uncommon",
        "Squamous Cell Carcinoma": "uncommon",
        "Trixacarus caviae Mange": "uncommon",
        "Aortic Calcification": "uncommon",
        "Cytomegalovirus Infection": "rare",
        "Lymphocytic Choriomeningitis (LCMV)": "rare",
    },
    # ==================================================================
    # FERRET — 22+ entries (expanded from ~10)
    # ==================================================================
    "ferret": {
        # very_common
        "Adrenal Disease": "very_common",
        "Insulinoma": "very_common",
        "Intestinal Parasites (Roundworm / Hookworm)": "very_common",
        "Upper Respiratory Infection": "very_common",
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
        "Posterior Paresis": "common",
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
        "Botulism": "rare",
        # Rare opportunistic infection (immunosuppressed animals) — untiered
        # it outranked cardiomyopathy/CHF for the cough+dyspnea+ascites triad.
        "Pneumocystis Pneumonia": "rare",
        # Primary/idiopathic epilepsy is rare in ferrets — hypoglycemia from
        # insulinoma is the most common cause of ferret seizures (Quesenberry &
        # Carpenter 4th ed). Untiered, it outranked insulinoma for the
        # screaming+tonic-episode complaint.
        "Seizure Disorder (Epilepsy)": "rare",
        # 2026-08 第14弾: 血便主訴の是正。ヘリコバクター関連胃潰瘍はフェレットで
        # 極めて高頻度（H. mustelae はほぼ全頭が保有 — Quesenberry & Carpenter
        # 4th ed）なのに未ティアで、曝露依存のイブプロフェン中毒・繁殖個体限定の
        # 妊娠毒血症が血便＋元気消失の上位を占めていた。
        "Gastric Ulcer": "common",
        "Helicobacter Mustelae Gastric Ulcer": "common",
        "Coccidia (GI)": "common",
        "Ibuprofen Toxicosis": "rare",
        "Pregnancy Toxemia": "rare",
        "Parvovirus Enteritis": "rare",
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
        "Hypovitaminosis A": "very_common",
        "Chytridiomycosis (Bd)": "very_common",
        "Ranavirus Infection": "common",
        "Red Leg Syndrome": "very_common",
        "Edema / Hydrops (Dropsy)": "common",
        "Stomatitis (Mouth Rot)": "common",
        "Intestinal Impaction": "common",
        "Thermal Burns": "uncommon",
        "Thermal Stress (Hypothermia)": "uncommon",
        # --- Expanded amphibian entries ---
        "Bacterial Dermatitis": "very_common",
        "Mycobacteriosis": "very_common",
        "Metabolic Bone Disease (MBD)": "very_common",
        "Nutritional Secondary Hyperparathyroidism": "very_common",
        "Saprolegniasis": "very_common",
        "Dehydration": "common",
        "Obesity": "common",
        "Foreign Body Ingestion": "common",
        "Parasitic Dermatitis": "common",
        "Chromomycosis": "common",
        "Trematode Infection": "common",
        "Ammonia Poisoning": "common",
        "Organ Prolapse (Gastric/Intestinal/Cloacal)": "common",
        "Corneal Lipidosis": "uncommon",
        "Renal Failure": "uncommon",
        "Neoplasia / Tumors": "uncommon",
        "Thiamine Deficiency": "uncommon",
        "Septicemia": "uncommon",
        "Iridovirus Infection (non-Ranavirus)": "rare",
        "Lucke Tumor Herpesvirus (Renal Carcinoma)": "rare",
        # --- Additional amphibian entries ---
        "Flavobacterium Infection": "very_common",
        "Columnaris Disease (Flavobacterium columnare)": "common",
        "Constipation": "common",
        "Egg Binding (Dystocia)": "common",
        "Fracture (Limb)": "common",
        "Intestinal Obstruction": "common",
        "Nitrite Poisoning": "common",
        "Gastroenteritis": "common",
        "Saprolegnia Infection": "common",
        "Cloacal Prolapse": "common",
        "Spindly Leg Syndrome": "common",
        "Axolotl Floating Disorder": "common",
        "Gas Bubble Disease": "uncommon",
        "Lymphoma": "uncommon",
        "Squamous Cell Carcinoma": "uncommon",
        "Myxozoan Infection": "uncommon",
        "Batrachochytrium salamandrivorans (Bsal)": "uncommon",
        "Calicivirus Infection": "rare",
        "Perkinsea Infection": "rare",
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
        # Chinchilla fur is too dense for ectoparasites — fur mites are RARE
        # (Quesenberry & Carpenter 4th ed); the very_common tier belonged to
        # rabbit Cheyletiella and had leaked here, burying dermatophytosis.
        "Fur Mites": "rare",
        "Trichophyton mentagrophytes (Ringworm)": "common",
        "Pneumonia": "common",
        "Dermatophytosis (Ringworm)": "common",
        "Conjunctivitis - Chinchilla": "common",
        "Heat Stroke": "common",
        "Intussusception - Chinchilla": "uncommon",
        "Cecal Impaction": "uncommon",
        "Cecal Torsion": "rare",
        "Bloat (Gastric Tympany)": "uncommon",
        # --- Expanded chinchilla entries ---
        "Fur Slip": "very_common",
        "Fur Chewing (Barbering)": "very_common",
        "Ear Infection (Otitis)": "common",
        "Constipation": "common",
        "Cataracts": "common",
        "Diabetes Mellitus - Chinchilla": "common",
        "Urolithiasis": "common",
        "Skin Abscess": "common",
        "Prolapsed Rectum": "common",
        "Cardiomyopathy": "uncommon",
        "Lymphoma": "uncommon",
        "Listeriosis - Chinchilla": "uncommon",
        "Giardiasis": "uncommon",
        "Pyometra": "uncommon",
        "Toxoplasmosis": "rare",
        "Chordoma": "rare",
        # --- Additional chinchilla entries ---
        "Tooth Root Abscess": "very_common",
        "Dental Disease (Molar Elongation)": "very_common",
        "Slobbers (Dental-Related)": "very_common",
        "Bumblefoot (Pododermatitis)": "common",
        "Calcium Deficiency": "common",
        "Dental Resorption": "common",
        "Fracture (Limb)": "common",
        "Fur Ring (Penile)": "common",
        "Heatstroke (Chinchilla-Specific)": "common",
        "Intestinal Obstruction": "common",
        "Malocclusion - Progressive": "common",
        "Otitis Media/Interna": "common",
        "Pregnancy Toxemia": "common",
        "Rhinitis": "common",
        "Dental Disease - Resorptive Lesions": "uncommon",
        "Dilated Cardiomyopathy": "uncommon",
        "Encephalitozoon cuniculi Infection": "uncommon",
        "Hepatic Lipidosis": "uncommon",
        "Mammary Tumor": "uncommon",
        "Osteomyelitis": "uncommon",
        "Squamous Cell Carcinoma": "rare",
        "Iron Storage Disease": "rare",
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
        "Gastrointestinal Stasis": "common",
        "Intestinal Parasites": "common",
        "Seizures": "common",
        "Lymphoma": "common",
        # --- Expanded degu entries ---
        "Skin Abscess": "very_common",
        "Barbering": "very_common",
        "Tail Degloving Injury": "very_common",
        "Bumblefoot (Pododermatitis)": "very_common",
        "Malocclusion": "very_common",
        "Dermatophytosis": "common",
        "Ear Infection": "common",
        "Constipation": "common",
        "Obesity": "common",
        "Conjunctivitis": "common",
        "Pneumonia": "common",
        "Elodontoma (Dental Tumor)": "common",
        "Hepatic Lipidosis": "uncommon",
        "Cardiomyopathy": "uncommon",
        "Uterine Adenocarcinoma": "uncommon",
        "Mammary Tumor": "uncommon",
        "Chronic Kidney Disease": "uncommon",
        "Septicemia": "rare",
        "Toxoplasmosis": "rare",
        # --- Additional degu entries ---
        "Incisor Overgrowth": "very_common",
        "Molar Elongation": "very_common",
        "Molar Spurs": "very_common",
        "Cataracts (Diabetic)": "very_common",
        "Dental Abscess": "common",
        "Diabetic Cataracts": "common",
        "Diabetic Ketoacidosis": "common",
        "Fracture": "common",
        "Giardiasis": "common",
        "Heat Stroke": "common",
        "Intestinal Parasitism": "common",
        "Nail Overgrowth": "common",
        "Tail Slip (Degloving)": "common",
        "Tooth Root Abscess": "common",
        "Urinary Tract Infection": "common",
        "Bloat (Gastric Dilation)": "uncommon",
        "Cecal Impaction": "uncommon",
        "Fibrosarcoma": "uncommon",
        "Ovarian Cysts": "uncommon",
        "Diabetes-Related Cataracts": "uncommon",
        "Alzheimer's-like Disease": "rare",
        "Cognitive Dysfunction (Senile)": "rare",
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
        # --- Expanded exotic_other entries ---
        "Dental Disease (Exotic)": "very_common",
        "Dermatological Bacterial Infection": "very_common",
        "Obesity": "very_common",
        "Dehydration": "common",
        "Gastrointestinal Stasis": "common",
        "Pneumonia (Bacterial)": "common",
        "Heat Stress / Heat Stroke": "common",
        "Skin Abscess": "common",
        "Conjunctivitis": "common",
        "Diarrhea (Non-specific)": "common",
        "Constipation": "common",
        "Mite Infestation (Tarantula)": "common",
        "Fracture (Limb)": "common",
        "Trauma / Wound Infection (Exotic)": "common",
        "Hepatic Lipidosis": "uncommon",
        "Renal Disease": "uncommon",
        "Neoplasia (General)": "uncommon",
        "Cardiomyopathy": "uncommon",
        "Septicemia": "rare",
        "Chlamydiosis": "rare",
        # --- Additional exotic_other entries ---
        "Ferret Adrenal Gland Disease": "very_common",
        "Ferret Insulinoma": "very_common",
        "Hedgehog Skin Mites (Caparinia tripilis)": "very_common",
        "Hedgehog Ringworm (Trichophyton)": "very_common",
        "Ferret Lymphoma": "common",
        "Ferret ECE (Epizootic Catarrhal Enteritis)": "common",
        "Ferret Helicobacter Gastritis": "common",
        "Ferret Aleutian Disease": "common",
        "Hedgehog Wobbly Hedgehog Syndrome (WHS)": "common",
        "Hedgehog Obesity": "common",
        "Hedgehog Cardiomyopathy": "common",
        "Dippity Pig Syndrome": "common",
        "Mange (Sarcoptic)": "common",
        "Hoof Overgrowth / Cracks (Porcine)": "common",
        "Sugar Glider Self-Mutilation": "uncommon",
        "Sugar Glider Nutritional Osteodystrophy": "uncommon",
        "Odontoma (Prairie Dog)": "uncommon",
        "Ferret Canine Distemper": "rare",
        "Monkeypox": "rare",
        "Plague (Yersinia pestis)": "rare",
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
        "Burns": "common",
        # --- Additional lizard entries ---
        "Coccidia Infection": "very_common",
        "Dehydration": "very_common",
        "Internal Nematodes (Roundworms)": "very_common",
        "Constipation": "very_common",
        "Egg Binding (Dystocia)": "common",
        "Corneal Ulcer": "common",
        "Conjunctivitis": "common",
        "Bite Wounds": "common",
        "Fracture (Limb)": "common",
        "Obesity": "common",
        "Tail Autotomy Complication": "common",
        "Toe Necrosis (Retained Shed)": "common",
        "Gout (Articular)": "common",
        "Gout (Visceral)": "common",
        "Sand Impaction": "common",
        "Aural Abscess": "common",
        "Atadenovirus Infection": "uncommon",
        "Nannizziopsis Dermatitis": "uncommon",
        "Squamous Cell Carcinoma": "uncommon",
        "Lymphoma": "uncommon",
        "Hepatic Lipidosis": "uncommon",
        "Bearded Dragon Adenovirus": "uncommon",
        "Inclusion Body Disease (IBD)": "rare",
        "Chameleon Edema Syndrome": "rare",
    },
    # ==================================================================
    # PARAKEET
    # ==================================================================
    "parakeet": {
        # Exposure-dependent toxicoses are rare without a specific history,
        # and Haemoproteus is usually an incidental finding — without tiers
        # these outranked infectious/GI causes for nonspecific sick-bird signs.
        "Copper Poisoning": "rare",
        "Teflon (PTFE) Toxicosis": "rare",
        "Teflon Toxicosis (Parakeet)": "rare",
        "Essential Oil Toxicity": "rare",
        "Haemoproteus Infection": "uncommon",
        "Psittacosis (Chlamydiosis)": "very_common",
        "Aspergillosis": "very_common",
        "Upper Respiratory Infection": "very_common",
        "Nutritional Deficiency (General)": "very_common",
        "Feather Plucking": "very_common",
        "Avian Pox": "common",
        "Giardiasis": "common",
        "Fatty Liver Disease": "common",
        "Sinusitis": "common",
        # --- Additional parakeet entries ---
        "Megabacteriosis (AGY)": "very_common",
        "Candidiasis (Crop Mycosis)": "very_common",
        "Goiter (Thyroid Hyperplasia)": "very_common",
        "Knemidocoptes Mange (Scaly Face)": "very_common",
        "Macrorhabdus ornithogaster (Parakeet)": "common",
        "Egg Binding": "common",
        "Egg Yolk Peritonitis": "common",
        "Chronic Egg Laying": "common",
        "Iodine Deficiency (Thyroid Hyperplasia)": "common",
        "Crop Stasis": "common",
        "Wing Fractures": "common",
        "Night Fright Injury": "common",
        "Lead Poisoning": "common",
        "Zinc Toxicosis": "common",
        "Lipomas": "common",
        "French Moult": "common",
        "Sour Crop": "common",
        "Renal Adenocarcinoma": "uncommon",
        "Testicular Tumor (Cere Color Change)": "uncommon",
        "Budgerigar Fledgling Disease": "uncommon",
        "Xanthomas": "uncommon",
        "Psittacine Beak and Feather Disease (PBFD)": "uncommon",
        "Pacheco's Disease": "rare",
        "Polyomavirus Infection": "rare",
        "Budgerigar Herpesvirus": "rare",
    },
    # ==================================================================
    # PARROT
    # ==================================================================
    "parrot": {
        # Exposure-dependent toxicoses / incidental hemoparasites (see parakeet).
        "Copper Poisoning": "rare",
        "PTFE Toxicosis (Teflon Poisoning)": "rare",
        "Teflon/PTFE Toxicosis": "rare",
        "Essential Oil Toxicity": "rare",
        "Haemoproteus Infection": "uncommon",
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
        "Pneumonia (Bacterial)": "uncommon",
        # --- Additional parrot entries ---
        "Candidiasis (Crop Mycosis)": "very_common",
        "Vitamin A Deficiency": "very_common",
        "Rhinitis": "very_common",
        "Sinusitis": "common",
        "Egg Binding": "common",
        "Egg Peritonitis": "common",
        "Chronic Egg Laying": "common",
        "Psittacine Beak and Feather Disease (PBFD)": "common",
        "Proventricular Dilatation Disease (PDD)": "common",
        "Crop Stasis": "common",
        "Crop Impaction": "common",
        "Lead Poisoning": "common",
        "Zinc Toxicosis": "common",
        "Gout (Visceral/Articular)": "common",
        "Obesity": "common",
        "Lipoma": "common",
        "Self-Mutilation": "common",
        "Behavioral Feather Destructive Disorder": "common",
        "Fracture (Wing)": "common",
        "Knemidocoptes Mange (Scaly Face)": "uncommon",
        "Hepatic Amyloidosis": "uncommon",
        "Squamous Cell Carcinoma": "uncommon",
        "Pacheco's Disease": "rare",
        "Iron Storage Disease (Hemochromatosis)": "rare",
        "Macaw Wasting Disease": "rare",
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
        # --- Additional snake entries ---
        "Dysecdysis (Retained Shed)": "very_common",
        "Anorexia (Behavioral)": "very_common",
        "Dehydration": "very_common",
        "Constipation": "very_common",
        "Blister Disease": "common",
        "Burns": "common",
        "Cryptosporidiosis": "common",
        "Spectacle Retention": "common",
        "Prey Bite Injury": "common",
        "Rostral Abrasion": "common",
        "Stomatitis (Mouth Rot)": "common",
        "Retained Spectacle (Retained Eye Cap)": "common",
        "Penile/Hemipenal Prolapse": "common",
        "Substrate Impaction": "common",
        "Internal Nematodes (Roundworms)": "common",
        "Boid Nidovirus (Ball Python Nidovirus)": "uncommon",
        "Snake Fungal Disease (Ophidiomyces)": "uncommon",
        # Ophidian herpesvirus is a rare diagnosis in pet snakes (herpesviruses
        # are chiefly a chelonian problem) — without a tier it outranked the
        # very_common mouth rot on the stomatitis+anorexia complaint.
        "Ophidian Herpesvirus Infection": "rare",
        "Gout (Visceral)": "uncommon",
        "Lymphoma": "uncommon",
        "Arenavirus Infection": "uncommon",
        "Paramyxovirus Infection": "rare",
        "Kinking (Spinal Deformity)": "rare",
        "Sunshine Virus (Reptarenavirus)": "rare",
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
        # --- Additional sugar glider entries ---
        "Nutritional Osteodystrophy (MBD)": "very_common",
        "Obesity": "very_common",
        "Stress-Induced Alopecia": "very_common",
        "Calcium Deficiency": "very_common",
        "Self-Mutilation Syndrome": "common",
        "Dental Caries": "common",
        "Periodontal Disease": "common",
        "Patagium Tear": "common",
        "Corneal Ulcer": "common",
        "Diarrhea": "common",
        "Constipation": "common",
        "Hepatic Lipidosis": "common",
        "Posterior Paralysis": "common",
        "Pouch Infection (Marsupial)": "common",
        "Fracture": "common",
        "Lumpy Jaw (Mandibular Abscess)": "common",
        "Depression / Stress Syndrome": "common",
        "Joey Rejection": "common",
        "Urinary Tract Infection": "uncommon",
        "Mammary Tumor": "uncommon",
        "Ovarian Cysts": "uncommon",
        "Toxoplasmosis": "uncommon",
        "Iron Storage Disease (Hemochromatosis)": "rare",
        "Renal Amyloidosis": "rare",
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
        # --- Additional tortoise entries ---
        "Dehydration": "very_common",
        "Intestinal Nematodes (Roundworms)": "very_common",
        "Oxyurid Infection": "very_common",
        "Beak Overgrowth": "very_common",
        "Nail Overgrowth": "very_common",
        "Shell Pyramiding": "common",
        "Shell Fracture / Trauma": "common",
        "Bladder Stones (Urolithiasis)": "common",
        "Constipation": "common",
        "Rhinitis": "common",
        "Hexamita Infection": "common",
        "Herpesvirus Infection": "common",
        "Mycoplasmosis (Mycoplasma agassizii / testudineum)": "common",
        "Runny Nose Syndrome (RNS)": "common",
        "Gout (Articular)": "common",
        "Gout (Visceral)": "common",
        "Foreign Body Ingestion": "common",
        "Egg Binding (Dystocia)": "common",
        "Hepatic Lipidosis": "uncommon",
        "Fibrosarcoma": "uncommon",
        "Squamous Cell Carcinoma": "uncommon",
        "Tortoise Intranuclear Coccidia (TINC)": "uncommon",
        "Ranavirus Infection": "rare",
        "Tortoise Herpesvirus": "rare",
    },
}


# ============================================================================
# Regional Prevalence Adjustments (Japan)
# ============================================================================
# Override prevalence tiers for diseases with documented regional differences.
# These adjustments are applied when the UI language is Japanese (region=jp).
#
# EVIDENCE SOURCES:
# - Heartworm: Japan is endemic; year-round transmission in southern regions.
#   Atkins CE et al. (2014) Guidelines for Diagnosis, Prevention &
#   Management of Heartworm (Dirofilaria immitis) Infection in Dogs. ACVIM.
#   Japanese prevalence 10-30% in unprotected dogs (Venco et al., 2011).
# - Babesiosis: Babesia gibsoni common in Japan, especially in fighting dogs
#   and Shiba Inus. Irwin PJ (2009) Canine babesiosis. Vet Clin Small Anim.
# - SFTS (Severe Fever with Thrombocytopenia Syndrome): Tick-borne bunyavirus
#   endemic in western Japan since 2013. Zoonotic. Takahashi T et al. (2014).
# - FIP: High prevalence in multi-cat households; Japan has dense cattery
#   populations. Pedersen NC (2014) An update on feline infectious peritonitis.
# - Leptospirosis: Common in Japan due to high humidity and wildlife reservoirs.
#   Koizumi N et al. (2009) Japanese leptospirosis serovar distribution.
# - Salmon Poisoning: Neorickettsia helminthoeca — absent in Japan (Pacific NW
#   North America only). Gorham JR & Foreyt WJ (2006).
# - Rabies: Eliminated from Japan since 1957. Only imported cases since.
#   Ministry of Health, Labour and Welfare, Japan.
# - Blastomycosis/Coccidioidomycosis/Histoplasmosis: Endemic to Americas,
#   essentially absent in Japan. Imported cases only.
# - Chagas Disease (Trypanosomiasis): Americas only, absent in Japan.
# - Leishmaniasis (visceral): Mediterranean/South America, not endemic in Japan.
# ============================================================================

JAPAN_REGIONAL_ADJUSTMENTS = {
    "dog": {
        # MORE common in Japan
        "Heartworm Disease": "very_common",  # Endemic; southern Japan year-round
        "Babesiosis": "common",  # B. gibsoni in Shiba, Tosa, Akita
        "Periodontal Disease": "very_common",  # Small breeds very popular in Japan
        "Patellar Luxation": "very_common",  # Small breed predominance in Japan
        "Brachycephalic Airway Syndrome": "common",  # French Bulldog #1 breed in Japan
        "Acute Moist Dermatitis (Hot Spot)": "very_common",  # Hot humid summers (梅雨〜盛夏)
        "Leptospirosis": "common",  # High humidity, wildlife reservoirs
        # LESS common / absent in Japan
        "Salmon Poisoning Disease": "rare",  # Pacific NW North America only
        "Tick Paralysis": "rare",  # Ixodes holocyclus (Australia) / Dermacentor (N.America) phenomenon
        "Blastomycosis": "rare",  # Americas endemic, imported only
        "Coccidioidomycosis (Valley Fever)": "rare",  # Americas endemic
        "Histoplasmosis": "rare",  # Americas endemic
        "Rabies": "rare",  # Eliminated since 1957
        "Leishmaniasis": "rare",  # Not endemic
    },
    "cat": {
        # MORE common in Japan
        "Feline Infectious Peritonitis (FIP) - Wet Form": "common",  # High multi-cat density
        "Feline Infectious Peritonitis (FIP) - Dry Form": "common",  # High multi-cat density
        "Feline Leukemia Virus (FeLV)": "common",  # Outdoor cats common
        "Feline Immunodeficiency Virus (FIV)": "common",  # High outdoor cat population
        "Hyperthyroidism": "very_common",  # Aging cat population
        "Chronic Kidney Disease (CKD)": "very_common",  # #1 cause of death in JP cats
        # LESS common / absent in Japan
        "Rabies": "rare",  # Eliminated
        "Feline Histoplasmosis": "rare",  # Americas endemic
        "Cytauxzoon felis (Acute Cytauxzoonosis)": "rare",  # Americas (tick-borne)
    },
    "horse": {
        # MORE common in Japan
        "Japanese Encephalitis": "common",  # Endemic, mosquito-borne
        "Getah Virus": "common",  # Endemic in Japanese horses (JRA outbreaks)
        "Babesiosis": "common",  # Tick-borne, endemic
        # LESS common / absent in Japan
        "African Horse Sickness": "rare",  # Africa/Middle East
        "Dourine": "rare",  # Not present in Japan
        "Venezuelan Equine Encephalomyelitis": "rare",  # Americas only
        "Equine Protozoal Myeloencephalitis": "rare",  # Opossum host absent in Japan
        "West Nile Encephalitis": "rare",  # WNV not established in Japan
    },
    "rabbit": {
        # MORE common in Japan
        "Pasteurellosis (Snuffles)": "very_common",  # Most common rabbit pathogen in JP
        "Encephalitozoon cuniculi (E. cuniculi)": "common",  # Widespread in pet rabbits
        "Gastrointestinal Stasis": "very_common",  # No.1 rabbit emergency in JP practice
        # LESS common in Japan
        "Myxomatosis": "rare",  # No endemic myxoma in Japan
        "Rabbit Hemorrhagic Disease (RHD)": "uncommon",  # Outbreaks sporadic in JP
    },
    "ferret": {
        # MORE common in Japan
        "Adrenal Disease": "very_common",  # Very common in JP spayed/neutered
        "Insulinoma": "very_common",  # Common in older ferrets in JP
        "Heartworm Disease": "common",  # Japan is endemic
        # LESS common
        "Aleutian Disease": "uncommon",  # Less common in JP pet ferrets
    },
    "fish": {
        # Japan-specific aquaculture and ornamental fish diseases
        "Koi Herpesvirus Disease (KHV / CyHV-3)": "common",  # Reportable in Japan, outbreaks
        "Ichthyophthirius (White Spot Disease / Ich)": "very_common",
        "Columnaris Disease": "very_common",  # Warm water, common in JP summer
    },
}

# International baseline: diseases more common outside Japan
INTERNATIONAL_REGIONAL_ADJUSTMENTS = {
    "dog": {
        "Heartworm Disease": "common",  # Varies by region globally
        "Salmon Poisoning Disease": "uncommon",  # Pacific NW North America
        "Blastomycosis": "uncommon",  # Ohio/Mississippi river valleys
        "Coccidioidomycosis (Valley Fever)": "uncommon",  # US Southwest, Central America
        "Histoplasmosis": "uncommon",  # Americas
        "Babesiosis": "uncommon",  # Global but more focal
        "Rabies": "common",  # Still endemic in most countries
        "Leishmaniasis": "uncommon",  # Mediterranean, South America
    },
    "cat": {
        "Rabies": "uncommon",  # Still endemic globally
        "Cytauxzoon felis (Acute Cytauxzoonosis)": "uncommon",  # US Southeast
        "Feline Histoplasmosis": "uncommon",  # Americas
    },
    "horse": {
        "African Horse Sickness": "uncommon",  # Africa, Middle East
        "Japanese Encephalitis": "rare",  # Asia-specific
        "Getah Virus": "rare",  # Asia-specific
    },
    "rabbit": {
        "Myxomatosis": "common",  # Endemic in Europe, Australia
        "Rabbit Hemorrhagic Disease (RHD)": "common",  # Endemic in Europe, Australia
    },
}


def get_prevalence_for_species(species: str, region: str = "") -> dict[str, str]:
    """Get prevalence mapping for a specific species with optional regional adjustments.

    Parameters
    ----------
    species : str
        Species key (e.g., 'cat', 'rabbit', 'bird')
    region : str
        Regional context: 'jp' for Japan, 'intl' for international.
        Empty string returns base prevalence without regional adjustments.

    Returns
    -------
    dict[str, str]
        Mapping of disease names to prevalence tiers
    """
    base = dict(SPECIES_PREVALENCE.get(species, {}))
    if region == "jp":
        overrides = JAPAN_REGIONAL_ADJUSTMENTS.get(species, {})
        base.update(overrides)
    elif region == "intl":
        overrides = INTERNATIONAL_REGIONAL_ADJUSTMENTS.get(species, {})
        base.update(overrides)
    return base
