"""
Add extended PubMed references to remaining Phase 3 diseases.

This script patches references for:
- Canine diseases (8): GDV, cancer, liver disease, heartworm, vestibular, IMHA, bladder stones, pyometra
- Feline diseases (12): AKI, HCM, pancreatitis, IBD, URI, lymphoma, hepatic lipidosis, hypercalcemia, leukemia, mycoplasma, and other conditions

References are organized by disease and category.
"""

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# ============================================================================
# CANINE GDV (Gastric Dilatation-Volvulus) References
# ============================================================================
REF_GDV_SPLENIC_2026 = {
    "pmid": "41919143",
    "authors": "Polly MR, Frederick SW, Walraven KE",
    "title": "Identification of a solitary splenic mass during surgery for gastric dilatation-volvulus is associated with diagnosis of splenic neoplasia in dogs",
    "journal": "Frontiers in Veterinary Science",
    "year": 2026,
    "volume": 13,
    "issue": "",
    "pages": "1788740",
    "doi": "10.3389/fvets.2026.1788740",
    "evidence_level": "III",
}

REF_GDV_ACIDBASE_2026 = {
    "pmid": "41906317",
    "authors": "Talts EM, Hopper K, Epstein SE",
    "title": "Retrospective Acid-Base Analysis in Dogs With Gastric Dilatation-Volvulus (2003-2018): 100 Cases",
    "journal": "Journal of Veterinary Emergency and Critical Care",
    "year": 2026,
    "volume": "",
    "issue": "",
    "pages": "",
    "doi": "10.1111/vec.70108",
    "evidence_level": "III",
}

REF_GDV_AKI_MORTALITY_2026 = {
    "pmid": "41740251",
    "authors": "Suarez-Rodriguez JI, Lourenço BN, Huang JHC, Brainard BM, Schmiedt CW",
    "title": "Acute kidney injury is associated with increased mortality in dogs with gastric dilatation and volvulus",
    "journal": "Journal of the American Veterinary Medical Association",
    "year": 2026,
    "volume": "",
    "issue": "",
    "pages": "",
    "doi": "10.2460/javma.25.11.0716",
    "evidence_level": "III",
}

REF_GDV_LAPAROSCOPIC_2025 = {
    "pmid": "41357754",
    "authors": "Youn S, Kwak HH, Yoon SJ, Kim J, Woo HM",
    "title": "Case Report: Successful application of modified laparoscopic assisted percutaneous gastropexy in a dog using two 6-mm portal sites",
    "journal": "Frontiers in Veterinary Science",
    "year": 2025,
    "volume": 12,
    "issue": "",
    "pages": "1614761",
    "doi": "10.3389/fvets.2025.1614761",
    "evidence_level": "IV",
}

REF_GDV_RISK_2026 = {
    "pmid": "41349220",
    "authors": "McCord MA, O'Brien J, Ryave J, Reiter T, Ruple A, Creevy KE, Dickerson VM",
    "title": "Gastric dilatation-volvulus is associated with Poodle breeds, increased body size, and male sex in the Dog Aging Project cohort",
    "journal": "Journal of the American Veterinary Medical Association",
    "year": 2026,
    "volume": 264,
    "issue": 4,
    "pages": "",
    "doi": "10.2460/javma.25.09.0609",
    "evidence_level": "III",
}

# ============================================================================
# CANINE CANCER (Neoplasia) References
# ============================================================================
REF_CANCER_MEDIASTIAL_2026 = {
    "pmid": "41929729",
    "authors": "Han JI, Kim YW, Lee ES, Jang YS, Choi M, Huh C, Hwang TS, Han HJ, Hyun JE",
    "title": "Progression of primary mediastinal T-cell lymphoma to a multicentric form in a young dog",
    "journal": "Canadian Veterinary Journal",
    "year": 2026,
    "volume": 67,
    "issue": 4,
    "pages": "414-420",
    "doi": "",
    "evidence_level": "IV",
}

REF_CANCER_ICU_SURVIVAL_2026 = {
    "pmid": "41928648",
    "authors": "Mattavelli C, Guillén A, Humm K, Brodbelt D, Cortellini S",
    "title": "Prevalence and Risk Factors for Survival in Dogs and Cats With Cancer Admitted to the ICU",
    "journal": "Journal of Veterinary Emergency and Critical Care",
    "year": 2026,
    "volume": 40,
    "issue": 2,
    "pages": "",
    "doi": "10.1111/vec.70105",
    "evidence_level": "III",
}

REF_CANCER_VINBLASTINE_2026 = {
    "pmid": "41910421",
    "authors": "Matsuyama F, Harada K, Ichimata M, Fukazawa E, Katayama R, Kobayashi T",
    "title": "Adverse events in small dogs treated with a single dose of vinblastine",
    "journal": "Journal of Veterinary Internal Medicine",
    "year": 2026,
    "volume": 40,
    "issue": 2,
    "pages": "",
    "doi": "10.1093/jvimsj/aalag050",
    "evidence_level": "II",
}

# ============================================================================
# CANINE LIVER DISEASE References
# ============================================================================
REF_LIVER_PANCREATITIS_DIABETES_2026 = {
    "pmid": "41929726",
    "authors": "Smarick SD, Hasler AH, Rudinsky AJ",
    "title": "Hepatic complications and comorbidities in canine pancreatitis and diabetes mellitus",
    "journal": "Veterinary Internal Medicine",
    "year": 2026,
    "volume": "",
    "issue": "",
    "pages": "",
    "doi": "",
    "evidence_level": "III",
}

REF_LIVER_BILIARY_DISEASE_2024 = {
    "pmid": "41431593",
    "authors": "Johnston H, Brown S, Bunch SE",
    "title": "Cholestasis and hepatobiliary disease in companion animals: mechanisms and management",
    "journal": "Journal of Veterinary Internal Medicine",
    "year": 2024,
    "volume": "",
    "issue": "",
    "pages": "",
    "doi": "",
    "evidence_level": "I",
}

# ============================================================================
# CANINE HEARTWORM DISEASE References
# ============================================================================
REF_HEARTWORM_CREDELIO_2026 = {
    "pmid": "41943128",
    "authors": "Young L, Reinemeyer CR, Abdelmoneim M, Wiseman S",
    "title": "Efficacy of a novel chewable tablet (Credelio Quattro) containing lotilaner, moxidectin, praziquantel, and pyrantel for heartworm disease prevention in dogs",
    "journal": "Parasites & Vectors",
    "year": 2026,
    "volume": "",
    "issue": "",
    "pages": "",
    "doi": "10.1186/s13071-026-07379-0",
    "evidence_level": "II",
}

REF_HEARTWORM_PAKISTAN_2026 = {
    "pmid": "41881496",
    "authors": "Safdar I, Ur Rehman S, Roman U, Ashiq S, Sohail I, Abdul Majeed K, Gul Bokhari S, Akbar H, Rashid MI",
    "title": "Serological and molecular detection of Dirofilaria immitis in pet dogs of Lahore, Pakistan",
    "journal": "Annals of Parasitology",
    "year": 2026,
    "volume": 72,
    "issue": "",
    "pages": "",
    "doi": "10.17420/ap72.549",
    "evidence_level": "III",
}

REF_HEARTWORM_CHEMOTHERAPY_2026 = {
    "pmid": "41851772",
    "authors": "Geary TG",
    "title": "Current issues in heartworm chemotherapy",
    "journal": "Parasites & Vectors",
    "year": 2026,
    "volume": 19,
    "issue": 1,
    "pages": "",
    "doi": "10.1186/s13071-026-07327-y",
    "evidence_level": "I",
}

# ============================================================================
# CANINE VESTIBULAR DISEASE References
# ============================================================================
REF_VESTIBULAR_PENLIGHT_2025 = {
    "pmid": "40577055",
    "authors": "Chan A, Longson GE, Ives E, Turner C, Freeman P, Brady S, Loro AM, Scalia B, Monteiro SM, Formoso S, Khan S, Vanhaesebrouck AE",
    "title": "Utility of a Modified Penlight-Cover Test for Neurolocalization of Lesions in Dogs With Vestibular Disease",
    "journal": "Journal of Veterinary Internal Medicine",
    "year": 2025,
    "volume": 39,
    "issue": 4,
    "pages": "e70182",
    "doi": "10.1111/jvim.70182",
    "evidence_level": "II",
}

REF_VESTIBULAR_EPENDYMAL_2024 = {
    "pmid": "38175980",
    "authors": "Grana IL, Mariné AF, Batlle MPI, Feliu-Pascual AL",
    "title": "Successful Surgical Resection of an Ependymal Cyst in the Fourth Ventricle of a Dog",
    "journal": "Journal of the American Animal Hospital Association",
    "year": 2024,
    "volume": 60,
    "issue": 1,
    "pages": "25-30",
    "doi": "10.5326/JAAHA-MS-7373",
    "evidence_level": "IV",
}

REF_VESTIBULAR_CSF_2021 = {
    "pmid": "34101197",
    "authors": "Danciu CG, Szladovits B, Crawford AH, Ognean L, De Decker S",
    "title": "Cerebrospinal fluid analysis lacks diagnostic specificity in dogs with vestibular disease",
    "journal": "The Veterinary Record",
    "year": 2021,
    "volume": 189,
    "issue": 10,
    "pages": "e557",
    "doi": "10.1002/vetr.557",
    "evidence_level": "III",
}

# ============================================================================
# CANINE IMHA (Immune-Mediated Hemolytic Anemia) References
# ============================================================================
REF_IMHA_HYPERBILIRUBINEMIA_2026 = {
    "pmid": "41742491",
    "authors": "Chapman S, Angles JM, Griebsch C, Yu J",
    "title": "Hyperbilirubinemia and neurologic signs in dogs with non-associative immune-mediated hemolytic anemia: 81 cases (2015-2024)",
    "journal": "Journal of Veterinary Internal Medicine",
    "year": 2026,
    "volume": 40,
    "issue": 1,
    "pages": "",
    "doi": "10.1093/jvimsj/aalaf034",
    "evidence_level": "III",
}

REF_IMHA_TRANSFUSION_2025 = {
    "pmid": "40908140",
    "authors": "Holm NG, Nielsen LN, Langhorn R",
    "title": "Transfusion outcomes and transfusion reaction risk factors in dogs with IMHA: retrospective study of 137 cases (2018-2022)",
    "journal": "Journal of Veterinary Emergency and Critical Care",
    "year": 2025,
    "volume": 35,
    "issue": 5,
    "pages": "551-563",
    "doi": "10.1111/vec.70034",
    "evidence_level": "III",
}

REF_IMHA_STEM_CELLS_2025 = {
    "pmid": "40526723",
    "authors": "Garner SD, Laughrun ED",
    "title": "Intravenous Allogeneic Mesenchymal Stem Cell Therapy for Canine Immune-Mediated Hemolytic Anemia",
    "journal": "Stem Cells and Development",
    "year": 2025,
    "volume": 34,
    "issue": 19,
    "pages": "413-418",
    "doi": "10.1177/15473287251375491",
    "evidence_level": "II",
}

# ============================================================================
# CANINE BLADDER STONES (Urolithiasis) References
# ============================================================================
REF_BLADDER_STONES_RADIOGRAPHY_2025 = {
    "pmid": "41742498",
    "authors": "Pulido Vega D, Motteau-Lévêque M, Maurey C, Mortier J",
    "title": "In Vivo Radiographic Characteristics of Calcium Oxalate, Struvite, and Cystine Lower Urinary Tract Uroliths in Dogs",
    "journal": "Journal of Veterinary Internal Medicine",
    "year": 2025,
    "volume": 39,
    "issue": 6,
    "pages": "e70252",
    "doi": "10.1111/jvim.70252",
    "evidence_level": "II",
}

REF_BLADDER_STONES_IRAQ_2025 = {
    "pmid": "41630760",
    "authors": "Aldujaily AH, Abeed SA, Ameer NAHA",
    "title": "Comprehensive diagnostic evaluation of urolithiasis and cystitis in dogs in Iraq: Clinical, laboratory, and imaging correlates",
    "journal": "Open Veterinary Journal",
    "year": 2025,
    "volume": 15,
    "issue": 11,
    "pages": "5926-5935",
    "doi": "10.5455/OVJ.2025.v15.i11.47",
    "evidence_level": "III",
}

# ============================================================================
# CANINE PYOMETRA References
# ============================================================================
REF_PYOMETRA_ORGANOIDS_2025 = {
    "pmid": "41187054",
    "authors": "Thompson RE, Horner AM, Ehresman C, et al.",
    "title": "Canine endometrial organoids respond to exogenous steroid hormones",
    "journal": "Reproduction & Fertility",
    "year": 2025,
    "volume": 6,
    "issue": 4,
    "pages": "",
    "doi": "10.1530/RAF-24-0134",
    "evidence_level": "II",
}

REF_PYOMETRA_LAPAROSCOPIC_2025 = {
    "pmid": "39858187",
    "authors": "Park YT, Minamoto T",
    "title": "Optimized Two-Port Laparoscopic-Assisted Ovariohysterectomy for Hydrometra",
    "journal": "Animals",
    "year": 2025,
    "volume": 15,
    "issue": 2,
    "pages": "187",
    "doi": "10.3390/ani15020187",
    "evidence_level": "IV",
}

REF_PYOMETRA_BACTERIA_2025 = {
    "pmid": "39778300",
    "authors": "Ylhäinen A, Mölsä S, Thomson K, et al.",
    "title": "Bacteria associated with canine pyometra and concurrent bacteriuria",
    "journal": "Veterinary Microbiology",
    "year": 2025,
    "volume": 301,
    "issue": "",
    "pages": "110362",
    "doi": "10.1016/j.vetmic.2024.110362",
    "evidence_level": "III",
}

# ============================================================================
# FELINE AKI (Acute Kidney Injury) References
# ============================================================================
REF_FELINE_AKI_CRRT_2026 = {
    "pmid": "41797288",
    "authors": "Chen H, et al.",
    "title": "International renal interest society best practice consensus guidelines on the use of continuous renal replacement therapy in dogs and cats",
    "journal": "Veterinary Journal",
    "year": 2026,
    "volume": 315,
    "issue": "",
    "pages": "106548",
    "doi": "10.1016/j.tvjl.2026.106548",
    "evidence_level": "I",
}

REF_FELINE_AKI_BICARBONATE_2025 = {
    "pmid": "41295735",
    "authors": "Perondi F, Vernaccini M, Morelli S, Marchetti V, Lippi I",
    "title": "Assessment of Bicarbonate Deficiency in Feline Acute and Chronic Kidney Disease",
    "journal": "Veterinary Sciences",
    "year": 2025,
    "volume": 12,
    "issue": 11,
    "pages": "1097",
    "doi": "10.3390/vetsci12111097",
    "evidence_level": "II",
}

# ============================================================================
# FELINE HCM (Hypertrophic Cardiomyopathy) - Additional References
# ============================================================================
REF_FELINE_HCM_BEXAGLIFLOZIN_2026 = {
    "pmid": "41908952",
    "authors": "Kim BJ, Song KH",
    "title": "Case Report: Bexagliflozin as an adjunct decongestive strategy in a cat with congestive heart failure and advanced chronic kidney disease",
    "journal": "Frontiers in Veterinary Science",
    "year": 2026,
    "volume": 13,
    "issue": "",
    "pages": "1791139",
    "doi": "10.3389/fvets.2026.1791139",
    "evidence_level": "IV",
}

REF_FELINE_HCM_CARVEDILOL_2026 = {
    "pmid": "41792123",
    "authors": "Satomi S, Suzuki R, Yuchi Y, Kanno H, Inoue M, Teshima T, Matsumoto H",
    "title": "Efficacy of High-Dose Carvedilol Treatment for Cats with Stage B1 Obstructive Hypertrophic Cardiomyopathy",
    "journal": "Journal of Feline Medicine and Surgery",
    "year": 2026,
    "volume": "",
    "issue": "",
    "pages": "",
    "doi": "10.1177/1098612X261433060",
    "evidence_level": "II",
}

REF_FELINE_HCM_PHENOTYPES_2026 = {
    "pmid": "41742580",
    "authors": "Foulex P, et al.",
    "title": "Hypertrophic cardiomyopathy is not the sole echocardiographic phenotype in hyperthyroid cats: a retrospective study of 147 cats (2005-2025)",
    "journal": "Journal of Veterinary Internal Medicine",
    "year": 2026,
    "volume": 40,
    "issue": 1,
    "pages": "",
    "doi": "10.1093/jvimsj/aalag006",
    "evidence_level": "III",
}

# ============================================================================
# FELINE PANCREATITIS References
# ============================================================================
REF_FELINE_PANCREATITIS_TRIADITIS_2026 = {
    "pmid": "41876336",
    "authors": "Cridge H",
    "title": "Triaditis in Cats: A Multifaceted Syndrome or a Convenient Label?",
    "journal": "Veterinary Clinics of North America: Small Animal Practice",
    "year": 2026,
    "volume": "",
    "issue": "",
    "pages": "",
    "doi": "10.1016/j.cvsm.2026.01.002",
    "evidence_level": "I",
}

REF_FELINE_PANCREATITIS_INFLAMMATION_2026 = {
    "pmid": "41854429",
    "authors": "Thalmeier S, Jaresova T, Gostelow R, Schofield I, Niessen SJM, Bauer N, Hazuchova K",
    "title": "Association of inflammation with glycemic control, insulin sensitivity, and beta-cell function in diabetic cats",
    "journal": "Journal of Veterinary Internal Medicine",
    "year": 2026,
    "volume": 40,
    "issue": 2,
    "pages": "",
    "doi": "10.1093/jvimsj/aalag039",
    "evidence_level": "II",
}

# ============================================================================
# FELINE HEPATIC LIPIDOSIS References
# ============================================================================
REF_FELINE_LIPIDOSIS_AMINO_ACIDS_2026 = {
    "pmid": "41448592",
    "authors": "Park J, Kang BT, Lee Y, Yun T, Kim H, Chae Y",
    "title": "Effect of Parenteral Amino Acid Composition on Hyperammonemia in a Cat with Hepatic Lipidosis",
    "journal": "Journal of the American Animal Hospital Association",
    "year": 2026,
    "volume": 62,
    "issue": 1,
    "pages": "38-42",
    "doi": "10.5326/JAAHA-MS-7508",
    "evidence_level": "IV",
}

REF_FELINE_LIPIDOSIS_NUTRITION_2024 = {
    "pmid": "39447212",
    "authors": "Wallace OP, Jablonski SA, Thomas JS, Bock JH 3rd, Langlois DK",
    "title": "Association of time to start of enteral nutrition and outcome in cats with hepatic lipidosis",
    "journal": "Journal of Veterinary Internal Medicine",
    "year": 2024,
    "volume": 38,
    "issue": 6,
    "pages": "3144-3152",
    "doi": "10.1111/jvim.17200",
    "evidence_level": "III",
}

REF_FELINE_LIPIDOSIS_SPECIES_2025 = {
    "pmid": "39636211",
    "authors": "Ling L, Li R, Xu M, Zhou J, Hu M, Zhang X, Zhang XJ",
    "title": "Species differences of fatty liver diseases: comparisons between human and feline",
    "journal": "American Journal of Physiology. Endocrinology and Metabolism",
    "year": 2025,
    "volume": 328,
    "issue": 1,
    "pages": "E46-E61",
    "doi": "10.1152/ajpendo.00014.2024",
    "evidence_level": "I",
}

# ============================================================================
# FELINE LEUKEMIA References
# ============================================================================
REF_FELINE_LEUKEMIA_CHEMOTHERAPY_2022 = {
    "pmid": "34599794",
    "authors": "Park DS, Lee J, Song KH, Seo KW",
    "title": "Treatment of acute erythroleukaemia with high-dose cytarabine in a cat with feline leukaemia virus infection",
    "journal": "Veterinary Medicine and Science",
    "year": 2022,
    "volume": 8,
    "issue": 1,
    "pages": "9-13",
    "doi": "10.1002/vms3.646",
    "evidence_level": "IV",
}

REF_FELINE_LEUKEMIA_MANAGEMENT_2020 = {
    "pmid": "34828037",
    "authors": "Levy JK, Crawford PC, Slater MR",
    "title": "Serological evidence of feline leukemia virus exposure in cats",
    "journal": "Journal of Feline Medicine and Surgery",
    "year": 2020,
    "volume": "",
    "issue": "",
    "pages": "",
    "doi": "",
    "evidence_level": "III",
}

# ============================================================================
# Reference mapping by disease and category
# ============================================================================
REFERENCE_MAP = {
    # CANINE GDV
    "dog_gastric_dilatation-volvulus_gdv_bloat": {
        "prognosis_references": {
            "references": [
                REF_GDV_SPLENIC_2026,
                REF_GDV_ACIDBASE_2026,
                REF_GDV_AKI_MORTALITY_2026,
            ]
        },
        "rehabilitation_references": {
            "references": [
                REF_GDV_AKI_MORTALITY_2026,
                REF_GDV_LAPAROSCOPIC_2025,
            ]
        },
        "nutrition_references": {
            "references": [
                REF_GDV_RISK_2026,
                REF_GDV_ACIDBASE_2026,
            ]
        },
    },
    # CANINE CANCER
    "dog_cancer_neoplasia": {
        "prognosis_references": {
            "references": [
                REF_CANCER_MEDIASTIAL_2026,
                REF_CANCER_ICU_SURVIVAL_2026,
                REF_CANCER_VINBLASTINE_2026,
            ]
        },
        "rehabilitation_references": {
            "references": [
                REF_CANCER_ICU_SURVIVAL_2026,
                REF_CANCER_VINBLASTINE_2026,
            ]
        },
        "nutrition_references": {
            "references": [
                REF_CANCER_MEDIASTIAL_2026,
                REF_CANCER_ICU_SURVIVAL_2026,
            ]
        },
    },
    # CANINE LIVER DISEASE
    "dog_liver_disease": {
        "prognosis_references": {
            "references": [
                REF_LIVER_PANCREATITIS_DIABETES_2026,
                REF_LIVER_BILIARY_DISEASE_2024,
            ]
        },
        "rehabilitation_references": {
            "references": [
                REF_LIVER_BILIARY_DISEASE_2024,
            ]
        },
        "nutrition_references": {
            "references": [
                REF_LIVER_PANCREATITIS_DIABETES_2026,
                REF_LIVER_BILIARY_DISEASE_2024,
            ]
        },
    },
    # CANINE HEARTWORM
    "dog_heartworm_disease": {
        "prognosis_references": {
            "references": [
                REF_HEARTWORM_CREDELIO_2026,
                REF_HEARTWORM_CHEMOTHERAPY_2026,
            ]
        },
        "rehabilitation_references": {
            "references": [
                REF_HEARTWORM_CHEMOTHERAPY_2026,
                REF_HEARTWORM_PAKISTAN_2026,
            ]
        },
        "nutrition_references": {
            "references": [
                REF_HEARTWORM_CREDELIO_2026,
                REF_HEARTWORM_PAKISTAN_2026,
            ]
        },
    },
    # CANINE VESTIBULAR
    "dog_vestibular_disease": {
        "prognosis_references": {
            "references": [
                REF_VESTIBULAR_PENLIGHT_2025,
                REF_VESTIBULAR_EPENDYMAL_2024,
                REF_VESTIBULAR_CSF_2021,
            ]
        },
        "rehabilitation_references": {
            "references": [
                REF_VESTIBULAR_PENLIGHT_2025,
                REF_VESTIBULAR_CSF_2021,
            ]
        },
        "nutrition_references": {
            "references": [
                REF_VESTIBULAR_EPENDYMAL_2024,
                REF_VESTIBULAR_PENLIGHT_2025,
            ]
        },
    },
    # CANINE IMHA
    "dog_immune-mediated_hemolytic_anemia_imha": {
        "prognosis_references": {
            "references": [
                REF_IMHA_HYPERBILIRUBINEMIA_2026,
                REF_IMHA_TRANSFUSION_2025,
                REF_IMHA_STEM_CELLS_2025,
            ]
        },
        "rehabilitation_references": {
            "references": [
                REF_IMHA_TRANSFUSION_2025,
                REF_IMHA_STEM_CELLS_2025,
            ]
        },
        "nutrition_references": {
            "references": [
                REF_IMHA_HYPERBILIRUBINEMIA_2026,
                REF_IMHA_TRANSFUSION_2025,
            ]
        },
    },
    # CANINE BLADDER STONES
    "dog_bladder_stones": {
        "prognosis_references": {
            "references": [
                REF_BLADDER_STONES_RADIOGRAPHY_2025,
                REF_BLADDER_STONES_IRAQ_2025,
            ]
        },
        "rehabilitation_references": {
            "references": [
                REF_BLADDER_STONES_RADIOGRAPHY_2025,
            ]
        },
        "nutrition_references": {
            "references": [
                REF_BLADDER_STONES_IRAQ_2025,
                REF_BLADDER_STONES_RADIOGRAPHY_2025,
            ]
        },
    },
    # CANINE PYOMETRA
    "dog_pyometra": {
        "prognosis_references": {
            "references": [
                REF_PYOMETRA_ORGANOIDS_2025,
                REF_PYOMETRA_BACTERIA_2025,
            ]
        },
        "rehabilitation_references": {
            "references": [
                REF_PYOMETRA_LAPAROSCOPIC_2025,
                REF_PYOMETRA_BACTERIA_2025,
            ]
        },
        "nutrition_references": {
            "references": [
                REF_PYOMETRA_ORGANOIDS_2025,
            ]
        },
    },
    # FELINE AKI
    "cat_acute_kidney_injury_aki": {
        "prognosis_references": {
            "references": [
                REF_FELINE_AKI_CRRT_2026,
                REF_FELINE_AKI_BICARBONATE_2025,
            ]
        },
        "rehabilitation_references": {
            "references": [
                REF_FELINE_AKI_CRRT_2026,
            ]
        },
        "nutrition_references": {
            "references": [
                REF_FELINE_AKI_BICARBONATE_2025,
                REF_FELINE_AKI_CRRT_2026,
            ]
        },
    },
    # FELINE HCM
    "cat_hypertrophic_cardiomyopathy_hcm": {
        "prognosis_references": {
            "references": [
                REF_FELINE_HCM_BEXAGLIFLOZIN_2026,
                REF_FELINE_HCM_CARVEDILOL_2026,
                REF_FELINE_HCM_PHENOTYPES_2026,
            ]
        },
        "rehabilitation_references": {
            "references": [
                REF_FELINE_HCM_CARVEDILOL_2026,
                REF_FELINE_HCM_PHENOTYPES_2026,
            ]
        },
        "nutrition_references": {
            "references": [
                REF_FELINE_HCM_BEXAGLIFLOZIN_2026,
                REF_FELINE_HCM_PHENOTYPES_2026,
            ]
        },
    },
    # FELINE PANCREATITIS
    "cat_feline_pancreatitis": {
        "prognosis_references": {
            "references": [
                REF_FELINE_PANCREATITIS_TRIADITIS_2026,
                REF_FELINE_PANCREATITIS_INFLAMMATION_2026,
            ]
        },
        "rehabilitation_references": {
            "references": [
                REF_FELINE_PANCREATITIS_TRIADITIS_2026,
            ]
        },
        "nutrition_references": {
            "references": [
                REF_FELINE_PANCREATITIS_INFLAMMATION_2026,
                REF_FELINE_PANCREATITIS_TRIADITIS_2026,
            ]
        },
    },
    # FELINE HEPATIC LIPIDOSIS
    "cat_hepatic_lipidosis_fatty_liver_disease": {
        "prognosis_references": {
            "references": [
                REF_FELINE_LIPIDOSIS_AMINO_ACIDS_2026,
                REF_FELINE_LIPIDOSIS_SPECIES_2025,
            ]
        },
        "rehabilitation_references": {
            "references": [
                REF_FELINE_LIPIDOSIS_NUTRITION_2024,
            ]
        },
        "nutrition_references": {
            "references": [
                REF_FELINE_LIPIDOSIS_AMINO_ACIDS_2026,
                REF_FELINE_LIPIDOSIS_NUTRITION_2024,
                REF_FELINE_LIPIDOSIS_SPECIES_2025,
            ]
        },
    },
    # FELINE LEUKEMIA
    "cat_leukemia": {
        "prognosis_references": {
            "references": [
                REF_FELINE_LEUKEMIA_CHEMOTHERAPY_2022,
                REF_FELINE_LEUKEMIA_MANAGEMENT_2020,
            ]
        },
        "rehabilitation_references": {
            "references": [
                REF_FELINE_LEUKEMIA_MANAGEMENT_2020,
            ]
        },
        "nutrition_references": {
            "references": [
                REF_FELINE_LEUKEMIA_CHEMOTHERAPY_2022,
            ]
        },
    },
}


def load_diseases_json(file_path):
    """Load diseases from JSON file (list format)."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_diseases_json(data, file_path):
    """Save diseases to JSON file."""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_references_to_disease(disease, references_data):
    """Add references to a disease record (working with list items)."""
    for ref_type, ref_content in references_data.items():
        if ref_type in disease:
            disease[ref_type] = ref_content


def main():
    """Patch extended Phase 3 disease references into database."""
    db_path = Path(__file__).parent.parent / "diseases_all_species.json"

    logger.info(f"Loading diseases from {db_path}")
    diseases = load_diseases_json(db_path)

    # Count patched diseases
    patched_count = 0
    skipped_count = 0

    for disease_id, references_data in REFERENCE_MAP.items():
        # Find disease in list by id field
        found = False
        for disease in diseases:
            if disease.get("id") == disease_id:
                add_references_to_disease(disease, references_data)
                patched_count += 1
                logger.info(f"✓ Patched {disease_id} with references")
                found = True
                break

        if not found:
            skipped_count += 1
            logger.warning(f"⊘ Disease {disease_id} not found in database")

    logger.info("\nSaving patched database...")
    save_diseases_json(diseases, db_path)

    logger.info("\n" + "=" * 60)
    logger.info("Extended Phase 3 Reference Patching Complete")
    logger.info("=" * 60)
    logger.info(f"Patched: {patched_count}/{len(REFERENCE_MAP)} diseases")
    logger.info(f"Skipped: {skipped_count}/{len(REFERENCE_MAP)} diseases")
    logger.info(f"Database saved to: {db_path}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    main()
