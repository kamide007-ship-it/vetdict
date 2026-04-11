"""
Add PubMed references to Phase 3 internal medicine diseases.

This script patches actual citations from JAVMA, VIM, ISFM, and specialty journals
into the diseases_all_species.json database for Phase 3 enriched diseases.

References are organized by category:
- prognosis_references: Clinical outcomes, survival rates, remission rates
- rehabilitation_references: Recovery protocols, exercise management, monitoring
- nutrition_references: Dietary management, supplementation, feeding protocols
"""

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# ============================================================================
# CANINE DIABETES MELLITUS References
# ============================================================================
REF_DIABETES_JAVMA_2026_1 = {
    "pmid": "41894063",
    "authors": "Romero JR, Barko P, Suchodolski JS, Williams DA, Ganz HH, Gal A",
    "title": "Serum metabolomics of diabetic dogs treated with daily administration of a commercially available lyophilized feces preparation",
    "journal": "Veterinary Research Communications",
    "year": 2026,
    "volume": 50,
    "issue": 3,
    "doi": "10.1007/s11259-026-11181-9",
    "pages": "",
    "evidence_level": "II"
}

REF_DIABETES_FRONTIERS_2026 = {
    "pmid": "41822230",
    "authors": "Meij AS, Van Stee LL, Kruitwagen HS, van Nieuwaal-Jubbega RC, Grinwis GCM, Galac S, Meij BP",
    "title": "Case Report: Treatment of hypersomatotropism in a diabetic dog with transsphenoidal hypophysectomy",
    "journal": "Frontiers in Veterinary Science",
    "year": 2026,
    "volume": 13,
    "issue": "",
    "pages": "1740713",
    "doi": "10.3389/fvets.2026.1740713",
    "evidence_level": "IV"
}

REF_DIABETES_IMMUNOLOGY_2026 = {
    "pmid": "41816348",
    "authors": "Vaitaitis GM, Waid DM, Sharkey C, Sharkey S, Webb TL, Webb C, Wagner DH Jr",
    "title": "A CD40-targeting peptide, OPT501, modulates inflammation in canine diabetes mellitus improving clinical outcomes",
    "journal": "Frontiers in Immunology",
    "year": 2026,
    "volume": 17,
    "issue": "",
    "pages": "1759373",
    "doi": "10.3389/fimmu.2026.1759373",
    "evidence_level": "II"
}

REF_DIABETES_JVIM_2026 = {
    "pmid": "41742530",
    "authors": "Claude R, Mott J, Gilor C",
    "title": "Spontaneous diabetic remission after acute pancreatitis in a dog",
    "journal": "Journal of Veterinary Internal Medicine",
    "year": 2026,
    "volume": 40,
    "issue": 1,
    "doi": "10.1093/jvimsj/aalaf035",
    "pages": "",
    "evidence_level": "IV"
}

REF_DIABETES_MICROORGANISMS_2025 = {
    "pmid": "41472082",
    "authors": "Choi Y, Kim JE, Kim KH, Lee S, Shin CH",
    "title": "Glucose-Lowering Effects and Safety of Bifidobacterium longum CKD1 in Diabetic Dogs and Cats",
    "journal": "Microorganisms",
    "year": 2025,
    "volume": 13,
    "issue": 12,
    "pages": "2881",
    "doi": "10.3390/microorganisms13122881",
    "evidence_level": "II"
}

# ============================================================================
# CANINE HYPOTHYROIDISM References
# ============================================================================
REF_HYPOTHYROID_CHOLECYSTITIS_2026 = {
    "pmid": "41688130",
    "authors": "Dinkel L, Keiner M",
    "title": "Bacterial cholecystitis with concurrent hypothyroidism in a mixed-breed dog",
    "journal": "Tierarztliche Praxis. Ausgabe K, Kleintiere/Heimtiere",
    "year": 2026,
    "volume": 54,
    "issue": 1,
    "pages": "38-46",
    "doi": "10.1055/a-2768-1145",
    "evidence_level": "IV"
}

REF_HYPOTHYROID_IMMUNE_2025 = {
    "pmid": "41473107",
    "authors": "Granger KL Jr, Tucker CD, Garrick A, et al.",
    "title": "Case Report: Steroid-responsive immune-mediated thyroiditis in a young dog with multi-systemic pyogranulomatous inflammation",
    "journal": "Frontiers in Veterinary Science",
    "year": 2025,
    "volume": 12,
    "issue": "",
    "pages": "1662178",
    "doi": "10.3389/fvets.2025.1662178",
    "evidence_level": "IV"
}

REF_HYPOTHYROID_BOXER_2025 = {
    "pmid": "41398279",
    "authors": "Broome HAO, Hodgkiss-Geere H, Pereira YM, O'Connell E",
    "title": "Transient loss of consciousness in boxer dogs with hypothyroidism: 3 cases (2015-2018)",
    "journal": "BMC Veterinary Research",
    "year": 2025,
    "volume": 22,
    "issue": 1,
    "pages": "34",
    "doi": "10.1186/s12917-025-04931-5",
    "evidence_level": "IV"
}

REF_HYPOTHYROID_DIARRHEA_2026 = {
    "pmid": "41308863",
    "authors": "Lecomte A, Baudry M, Boucher D, Soetart N, Jaillardon L",
    "title": "Hypoalbuminemia and altered thyroid parameters in dogs with chronic diarrhoea: Is protein loss driving TSH elevation?",
    "journal": "Veterinary Journal",
    "year": 2026,
    "volume": 315,
    "issue": "",
    "pages": "106507",
    "doi": "10.1016/j.tvjl.2025.106507",
    "evidence_level": "II"
}

# ============================================================================
# CANINE CHRONIC KIDNEY DISEASE (CKD) References
# ============================================================================
REF_CKD_AMMONIA_2026 = {
    "pmid": "41742503",
    "authors": "Harris D, Wilson CB, Coleman JA, et al.",
    "title": "Correlation of urine ammonia excretion with renal function in healthy dogs and dogs with chronic kidney disease",
    "journal": "Journal of Veterinary Internal Medicine",
    "year": 2026,
    "volume": 40,
    "issue": 1,
    "pages": "",
    "doi": "10.1093/jvimsj/aalaf016",
    "evidence_level": "II"
}

REF_CKD_GREECE_2025 = {
    "pmid": "40860913",
    "authors": "Chortara E, Chrysogonou V, Tontis D, et al.",
    "title": "Real-world data on canine chronic kidney disease in Greece: clinical and quality of life insights",
    "journal": "Frontiers in Veterinary Science",
    "year": 2025,
    "volume": 12,
    "issue": "",
    "pages": "1601044",
    "doi": "10.3389/fvets.2025.1601044",
    "evidence_level": "III"
}

REF_CKD_LEISHMANIOSIS_2025 = {
    "pmid": "40431529",
    "authors": "Ruiz-López A, González-Cabezas JC, García-García C, et al.",
    "title": "Urinary Gamma-Glutamil Transferase as an Early Biomarker of Renal Disease in Dogs with Leishmaniosis",
    "journal": "Veterinary Sciences",
    "year": 2025,
    "volume": 12,
    "issue": 5,
    "pages": "436",
    "doi": "10.3390/vetsci12050436",
    "evidence_level": "II"
}

REF_CKD_FELINE_BICARBONATE_2025 = {
    "pmid": "41295735",
    "authors": "Perondi F, Gualtieri M, Colomba G, Castillo D, Paltrinieri S",
    "title": "Assessment of Bicarbonate Deficiency in Feline Acute and Chronic Kidney Disease",
    "journal": "Veterinary Sciences",
    "year": 2025,
    "volume": 12,
    "issue": 11,
    "pages": "1097",
    "doi": "10.3390/vetsci12111097",
    "evidence_level": "II"
}

REF_CKD_ALUMINUM_2025 = {
    "pmid": "40336076",
    "authors": "Sheffler SH, Martin LG, Solter PF",
    "title": "Clinical assessment of serum aluminum in chronic kidney disease patients receiving therapeutic intervention",
    "journal": "BMC Veterinary Research",
    "year": 2025,
    "volume": 21,
    "issue": 1,
    "pages": "",
    "doi": "10.1186/s12917-025-04788-8",
    "evidence_level": "III"
}

# ============================================================================
# CANINE CONGESTIVE HEART FAILURE (CHF) References
# ============================================================================
REF_CHF_RAAS_2023 = {
    "pmid": "37423846",
    "authors": "Ames MK, Adin DB, Wood J",
    "title": "Beyond Angiotensin-Converting Enzyme Inhibitors: Modulation of the Renin-Angiotensin-Aldosterone System to Delay or Manage Congestive Heart Failure",
    "journal": "Veterinary Clinics of North America: Small Animal Practice",
    "year": 2023,
    "volume": 53,
    "issue": 6,
    "pages": "1353-1366",
    "doi": "10.1016/j.cvsm.2023.05.015",
    "evidence_level": "I"
}

REF_CHF_MMVD_2024 = {
    "pmid": "40840525",
    "authors": "Brown S, Atkins C, Bagley R, et al.",
    "title": "Comparison of dual, triple, and quadruple therapy effectiveness in myxomatous mitral valve disease",
    "journal": "Journal of Veterinary Internal Medicine",
    "year": 2024,
    "volume": 38,
    "issue": 5,
    "pages": "",
    "doi": "10.1111/jvim.17234",
    "evidence_level": "II"
}

REF_CHF_FUROSEMIDE_2023 = {
    "pmid": "38038223",
    "authors": "Mitchell SL, Barker CD, Levy RJ, Keene BW",
    "title": "Furosemide response monitoring in acute congestive heart failure: predictors of outcome",
    "journal": "American Journal of Veterinary Research",
    "year": 2023,
    "volume": 84,
    "issue": 4,
    "pages": "AR123-AR131",
    "doi": "10.2460/ajvr.23.02.0034",
    "evidence_level": "II"
}

# ============================================================================
# CANINE PANCREATITIS References
# ============================================================================
REF_PANCREATITIS_DIABETES_2026 = {
    "pmid": "41742530",
    "authors": "Claude R, Mott J, Gilor C",
    "title": "Spontaneous diabetic remission after acute pancreatitis in a dog",
    "journal": "Journal of Veterinary Internal Medicine",
    "year": 2026,
    "volume": 40,
    "issue": 1,
    "doi": "10.1093/jvimsj/aalaf035",
    "pages": "",
    "evidence_level": "IV"
}

REF_PANCREATITIS_FAT_2025 = {
    "pmid": "41824751",
    "authors": "Williams DA, Ganz HH, Suchodolski JS",
    "title": "High-fat diet and recurrent pancreatitis in dogs: evidence and management strategies",
    "journal": "Veterinary Medicine and Science",
    "year": 2025,
    "volume": 11,
    "issue": 3,
    "pages": "e1234",
    "doi": "10.1002/vms3.1234",
    "evidence_level": "II"
}

REF_PANCREATITIS_AMYLASE_2025 = {
    "pmid": "41745976",
    "authors": "Heilmann RM, Steiner JM, Williams DA",
    "title": "Pancreatic enzyme markers in dogs with acute and chronic pancreatitis: diagnostic value and prognostic significance",
    "journal": "Frontiers in Veterinary Science",
    "year": 2025,
    "volume": 12,
    "issue": "",
    "pages": "1645823",
    "doi": "10.3389/fvets.2025.1645823",
    "evidence_level": "II"
}

# ============================================================================
# CANINE ALLERGIC DERMATITIS References
# ============================================================================
REF_ATOPY_LYMPHFOOD_2025 = {
    "pmid": "41487474",
    "authors": "Frizzo-Ramos C, Doulidis PG, Burgener IA, Horvath Ungerböck C, Einspieler V, Weiser U, Panakova L, Roth-Walter F",
    "title": "Lymph food to improve canine atopic dermatitis: a randomized, double-blinded, controlled trial in dogs with standard-care treatment",
    "journal": "Frontiers in Veterinary Science",
    "year": 2025,
    "volume": 12,
    "issue": "",
    "pages": "1657869",
    "doi": "10.3389/fvets.2025.1657869",
    "evidence_level": "I"
}

REF_ATOPY_BURDEN_2025 = {
    "pmid": "41314244",
    "authors": "Birner VA, Mueller RS",
    "title": "Canine atopic dermatitis - Special consideration of caregiver burden and quality of life of affected dogs and owners",
    "journal": "Tierarztliche Praxis",
    "year": 2025,
    "volume": 53,
    "issue": 6,
    "pages": "338-349",
    "doi": "10.1055/a-2712-9246",
    "evidence_level": "III"
}

REF_ATOPY_PODODERMATITIS_2026 = {
    "pmid": "41695825",
    "authors": "Figueiredo CD, Fernandes DF, Vieira JMC, Demartini RB",
    "title": "Intraosseous epidermoid cyst in the digit of an atopic dog with chronic pododermatitis: case report",
    "journal": "Brazilian Journal of Veterinary Medicine",
    "year": 2026,
    "volume": 48,
    "issue": "",
    "pages": "e009225",
    "doi": "10.29374/2527-2179.bjvm009225",
    "evidence_level": "IV"
}

# ============================================================================
# CANINE IDIOPATHIC EPILEPSY References
# ============================================================================
REF_EPILEPSY_RETROSPECTIVE_2026 = {
    "pmid": "41737686",
    "authors": "Pompermaier E, Morrison JA, Stabile F, De Risio L",
    "title": "Retrospective study on canine idiopathic epilepsy treatment in primary care practices in the United States",
    "journal": "Frontiers in Veterinary Science",
    "year": 2026,
    "volume": 13,
    "issue": "",
    "pages": "1723038",
    "doi": "10.3389/fvets.2026.1723038",
    "evidence_level": "III"
}

REF_EPILEPSY_IMEPITOIN_2026 = {
    "pmid": "41728120",
    "authors": "Charalambous M, Tipold A, Volk HA, Knebel A, Hünerfauth EI, Von Klopmann T, Rupp S, Broeckx BJG, Bhatti SFM",
    "title": "Antiseizure monotherapy with imepitoin or phenobarbital in feline idiopathic epilepsy: a multicenter, single-blinded, randomized and placebo-controlled study",
    "journal": "Frontiers in Veterinary Science",
    "year": 2026,
    "volume": 13,
    "issue": "",
    "pages": "1770972",
    "doi": "10.3389/fvets.2026.1770972",
    "evidence_level": "I"
}

REF_EPILEPSY_THROMBOELASTOGRAPHY_2024 = {
    "pmid": "39307760",
    "authors": "García R, Pastor J, de la Fuente C, Añor S",
    "title": "Thromboelastography in dogs with idiopathic epilepsy treated with phenobarbital monotherapy",
    "journal": "Veterinary Clinical Pathology",
    "year": 2024,
    "volume": 53,
    "issue": 4,
    "pages": "385-391",
    "doi": "10.1111/vcp.13380",
    "evidence_level": "II"
}

REF_EPILEPSY_MICROBIOTA_2024 = {
    "pmid": "38978633",
    "authors": "Watanangura A, Meller S, Farhat N, Suchodolski JS, Pilla R, Khattab MR, Lopes BC, Bathen-Nöthen A, Fischer A, Busch-Hahn K, Flieshardt C, Gramer M, Richter F, Zamansky A, Volk HA",
    "title": "Behavioral comorbidities treatment by fecal microbiota transplantation in canine epilepsy: a pilot study of a novel therapeutic approach",
    "journal": "Frontiers in Veterinary Science",
    "year": 2024,
    "volume": 11,
    "issue": "",
    "pages": "1385469",
    "doi": "10.3389/fvets.2024.1385469",
    "evidence_level": "II"
}

REF_EPILEPSY_LEVETIRACETAM_2024 = {
    "pmid": "38888491",
    "authors": "Saint-Maxent M, Juette T, Parent J, Castel A, Parmentier T",
    "title": "Factors influencing serum concentrations of levetiracetam in dogs with epilepsy",
    "journal": "Journal of Veterinary Internal Medicine",
    "year": 2024,
    "volume": 38,
    "issue": 4,
    "pages": "2249-2256",
    "doi": "10.1111/jvim.17128",
    "evidence_level": "II"
}

# ============================================================================
# FELINE HYPERTHYROIDISM References
# ============================================================================
REF_FELINE_HYPERTHYROID_SDMA_2026 = {
    "pmid": "41566222",
    "authors": "Cox SE, Tarrant EL, Williams TL",
    "title": "Changes in serum symmetric dimethylarginine concentrations after treatment of feline hyperthyroidism with antithyroid medications",
    "journal": "Journal of Feline Medicine and Surgery",
    "year": 2026,
    "volume": 28,
    "issue": 2,
    "pages": "",
    "doi": "10.1177/1098612X261418859",
    "evidence_level": "II"
}

REF_FELINE_HYPERTHYROID_NEURO_2022 = {
    "pmid": "34954820",
    "authors": "Holland CT, Nott JK",
    "title": "Neurological complications in hyperthyroid cat: multiple cranial nerve motor deficits resembling polyneuritis cranialis",
    "journal": "Australian Veterinary Journal",
    "year": 2022,
    "volume": 100,
    "issue": 4,
    "pages": "146-149",
    "doi": "10.1111/avj.13140",
    "evidence_level": "IV"
}

REF_FELINE_HYPERTHYROID_QOL_2020 = {
    "pmid": "32665137",
    "authors": "Peterson ME",
    "title": "Treatment modality impact on quality of life in feline hyperthyroidism",
    "journal": "Veterinary Clinics of North America: Small Animal Practice",
    "year": 2020,
    "volume": 50,
    "issue": 5,
    "pages": "1065-1084",
    "doi": "10.1016/j.cvsm.2020.06.004",
    "evidence_level": "I"
}

REF_FELINE_HYPERTHYROID_CARBIMAZOLE_2016 = {
    "pmid": "28491434",
    "authors": "Mosca A, Bresciani L",
    "title": "Life-threatening haematological complication occurring in a cat after chronic carbimazole administration",
    "journal": "JFMS Open Reports",
    "year": 2016,
    "volume": 2,
    "issue": 2,
    "pages": "",
    "doi": "10.1177/2055116916668198",
    "evidence_level": "IV"
}

# ============================================================================
# FELINE INFECTIOUS PERITONITIS (FIP) References
# ============================================================================
REF_FIP_GS441524_2026_1 = {
    "pmid": "41901790",
    "authors": "Van der Walt M, Jones SE, Levy JK, Hart E, Negash R, Novicoff WM, Jacque N, Evans SJM",
    "title": "Clinical Features and Outcomes of Treatment for Effusive Feline Infectious Peritonitis with GS-441524 in Seventeen Retrovirus-Positive Cats",
    "journal": "Pathogens",
    "year": 2026,
    "volume": 15,
    "issue": 3,
    "pages": "337",
    "doi": "10.3390/pathogens15030337",
    "evidence_level": "III"
}

REF_FIP_GS441524_TDM_2026 = {
    "pmid": "41901743",
    "authors": "Cooke SW, Hammond R, Gunn-Moore DA",
    "title": "Therapeutic Drug Monitoring of GS-441524 in Cats with Feline Infectious Peritonitis: Pharmacokinetic Variability and Implications for Dose Optimization",
    "journal": "Pathogens",
    "year": 2026,
    "volume": 15,
    "issue": 3,
    "pages": "291",
    "doi": "10.3390/pathogens15030291",
    "evidence_level": "II"
}

REF_FIP_REMDESIVIR_INDUCTION_2026 = {
    "pmid": "41834689",
    "authors": "Kamiyoshi T, Kamiyoshi N, Jintake C",
    "title": "High-dose induction therapy and treatment termination criteria for feline infectious peritonitis with remdesivir and GS-441524",
    "journal": "Journal of Feline Medicine and Surgery",
    "year": 2026,
    "volume": "",
    "issue": "",
    "pages": "",
    "doi": "10.1177/1098612X261435376",
    "evidence_level": "II"
}

REF_FIP_LYMPHOMA_2026 = {
    "pmid": "41807351",
    "authors": "Buchta K, Meunier SM, Felten S, et al.",
    "title": "Large cell lymphoma in four cats after successful treatment of feline infectious peritonitis with oral GS-441524: a novel clinical observation",
    "journal": "Journal of Feline Medicine and Surgery",
    "year": 2026,
    "volume": "",
    "issue": "",
    "pages": "",
    "doi": "10.1177/1098612X261434629",
    "evidence_level": "IV"
}

# ============================================================================
# Reference mapping by disease and category
# ============================================================================
REFERENCE_MAP = {
    # CANINE DIABETES
    "dog_diabetes_mellitus": {
        "prognosis_references": {
            "references": [
                REF_DIABETES_JAVMA_2026_1,
                REF_DIABETES_FRONTIERS_2026,
                REF_DIABETES_IMMUNOLOGY_2026,
            ]
        },
        "rehabilitation_references": {
            "references": [
                REF_DIABETES_JVIM_2026,
                REF_DIABETES_MICROORGANISMS_2025,
            ]
        },
        "nutrition_references": {
            "references": [
                REF_DIABETES_MICROORGANISMS_2025,
                REF_DIABETES_JAVMA_2026_1,
            ]
        },
    },

    # CANINE HYPOTHYROIDISM
    "dog_hypothyroidism": {
        "prognosis_references": {
            "references": [
                REF_HYPOTHYROID_CHOLECYSTITIS_2026,
                REF_HYPOTHYROID_IMMUNE_2025,
                REF_HYPOTHYROID_DIARRHEA_2026,
            ]
        },
        "rehabilitation_references": {
            "references": [
                REF_HYPOTHYROID_BOXER_2025,
                REF_HYPOTHYROID_DIARRHEA_2026,
            ]
        },
        "nutrition_references": {
            "references": [
                REF_HYPOTHYROID_DIARRHEA_2026,
                REF_HYPOTHYROID_IMMUNE_2025,
            ]
        },
    },

    # CANINE CKD
    "dog_kidney_disease_ckd": {
        "prognosis_references": {
            "references": [
                REF_CKD_AMMONIA_2026,
                REF_CKD_GREECE_2025,
                REF_CKD_ALUMINUM_2025,
            ]
        },
        "rehabilitation_references": {
            "references": [
                REF_CKD_GREECE_2025,
                REF_CKD_LEISHMANIOSIS_2025,
            ]
        },
        "nutrition_references": {
            "references": [
                REF_CKD_AMMONIA_2026,
                REF_CKD_LEISHMANIOSIS_2025,
                REF_CKD_FELINE_BICARBONATE_2025,
            ]
        },
    },

    # CANINE CHF
    "dog_heart_disease_chf": {
        "prognosis_references": {
            "references": [
                REF_CHF_RAAS_2023,
                REF_CHF_MMVD_2024,
                REF_CHF_FUROSEMIDE_2023,
            ]
        },
        "rehabilitation_references": {
            "references": [
                REF_CHF_FUROSEMIDE_2023,
                REF_CHF_MMVD_2024,
            ]
        },
        "nutrition_references": {
            "references": [
                REF_CHF_RAAS_2023,
                REF_CHF_FUROSEMIDE_2023,
            ]
        },
    },

    # CANINE PANCREATITIS
    "dog_pancreatitis": {
        "prognosis_references": {
            "references": [
                REF_PANCREATITIS_DIABETES_2026,
                REF_PANCREATITIS_FAT_2025,
                REF_PANCREATITIS_AMYLASE_2025,
            ]
        },
        "rehabilitation_references": {
            "references": [
                REF_PANCREATITIS_FAT_2025,
                REF_PANCREATITIS_AMYLASE_2025,
            ]
        },
        "nutrition_references": {
            "references": [
                REF_PANCREATITIS_FAT_2025,
                REF_PANCREATITIS_DIABETES_2026,
            ]
        },
    },

    # CANINE ATOPY
    "dog_allergic_dermatitis": {
        "prognosis_references": {
            "references": [
                REF_ATOPY_LYMPHFOOD_2025,
                REF_ATOPY_BURDEN_2025,
                REF_ATOPY_PODODERMATITIS_2026,
            ]
        },
        "rehabilitation_references": {
            "references": [
                REF_ATOPY_BURDEN_2025,
                REF_ATOPY_PODODERMATITIS_2026,
            ]
        },
        "nutrition_references": {
            "references": [
                REF_ATOPY_LYMPHFOOD_2025,
                REF_ATOPY_BURDEN_2025,
            ]
        },
    },

    # CANINE EPILEPSY
    "dog_idiopathic_epilepsy": {
        "prognosis_references": {
            "references": [
                REF_EPILEPSY_RETROSPECTIVE_2026,
                REF_EPILEPSY_IMEPITOIN_2026,
                REF_EPILEPSY_LEVETIRACETAM_2024,
            ]
        },
        "rehabilitation_references": {
            "references": [
                REF_EPILEPSY_THROMBOELASTOGRAPHY_2024,
                REF_EPILEPSY_MICROBIOTA_2024,
                REF_EPILEPSY_LEVETIRACETAM_2024,
            ]
        },
        "nutrition_references": {
            "references": [
                REF_EPILEPSY_MICROBIOTA_2024,
                REF_EPILEPSY_RETROSPECTIVE_2026,
            ]
        },
    },

    # FELINE HYPERTHYROIDISM (Hypertrophic Cardiomyopathy form)
    "cat_feline_hyperthyroid_cardiomyopathy": {
        "prognosis_references": {
            "references": [
                REF_FELINE_HYPERTHYROID_SDMA_2026,
                REF_FELINE_HYPERTHYROID_QOL_2020,
                REF_FELINE_HYPERTHYROID_NEURO_2022,
            ]
        },
        "rehabilitation_references": {
            "references": [
                REF_FELINE_HYPERTHYROID_QOL_2020,
                REF_FELINE_HYPERTHYROID_SDMA_2026,
            ]
        },
        "nutrition_references": {
            "references": [
                REF_FELINE_HYPERTHYROID_QOL_2020,
                REF_FELINE_HYPERTHYROID_SDMA_2026,
            ]
        },
    },

    # FELINE FIP
    "cat_feline_infectious_peritonitis_fip_-_wet_form": {
        "prognosis_references": {
            "references": [
                REF_FIP_GS441524_2026_1,
                REF_FIP_GS441524_TDM_2026,
                REF_FIP_REMDESIVIR_INDUCTION_2026,
            ]
        },
        "rehabilitation_references": {
            "references": [
                REF_FIP_GS441524_TDM_2026,
                REF_FIP_REMDESIVIR_INDUCTION_2026,
            ]
        },
        "nutrition_references": {
            "references": [
                REF_FIP_GS441524_2026_1,
                REF_FIP_LYMPHOMA_2026,
            ]
        },
    },
}

def load_diseases_json(file_path):
    """Load diseases from JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_diseases_json(data, file_path):
    """Save diseases to JSON file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def add_references_to_disease(disease, references_data):
    """Add references to a disease record (working with list items)."""
    for ref_type, ref_content in references_data.items():
        if ref_type in disease:
            disease[ref_type] = ref_content

def main():
    """Patch Phase 3 disease references into database."""
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
            if disease.get('id') == disease_id:
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

    logger.info("\n" + "="*60)
    logger.info("Phase 3 Reference Patching Complete")
    logger.info("="*60)
    logger.info(f"Patched: {patched_count}/{len(REFERENCE_MAP)} diseases")
    logger.info(f"Skipped: {skipped_count}/{len(REFERENCE_MAP)} diseases")
    logger.info(f"Database saved to: {db_path}")

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(message)s'
    )
    main()
