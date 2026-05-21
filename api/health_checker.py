"""
Comprehensive Health Symptom Checker for Dogs - Flask Blueprint

Provides veterinary health analysis with breed-specific risk assessment,
symptom-to-disease matching using Jaccard similarity, and diagnostic
test recommendations based on real veterinary medical knowledge.
"""

import importlib
import json
import logging
import os
import re
from functools import lru_cache

from flask import Blueprint, jsonify, request

from api.content_quality import enrich_disease_content

logger = logging.getLogger(__name__)

# Regex to detect CJK characters (Japanese, Chinese, Korean) in IDs.
_CJK_PATTERN = re.compile(r"[\u3000-\u9fff]")

# Medical abbreviations that should remain uppercase when humanizing snake_case IDs.
_KEEP_UPPER_ABBREVIATIONS = frozenset(
    {
        "cbc",
        "pcr",
        "mri",
        "ct",
        "ecg",
        "ekg",
        "hiv",
        "fiv",
        "felv",
        "fip",
        "igg",
        "igm",
        "ige",
        "aids",
        "hplc",
        "usg",
        "pbfd",
        "bmbv",
        "bsa",
        "acth",
        "ast",
        "alt",
        "alp",
        "crp",
        "ldh",
        "cpk",
        "tsh",
        "t3",
        "t4",
        "lh",
        "fsh",
        "adh",
    }
)

# ---------------------------------------------------------------------------
# Japanese name reading lookup for あいうえお sorting
# ---------------------------------------------------------------------------
_NAME_JA_READINGS: dict[str, str] = {}
_readings_path = os.path.join(os.path.dirname(__file__), "name_ja_readings.json")
if os.path.exists(_readings_path):
    try:
        with open(_readings_path, encoding="utf-8") as _f:
            _NAME_JA_READINGS = json.load(_f)
    except (OSError, ValueError) as _e:  # noqa: BLE001
        # Reading lookup is optional — sorting will fall back to default ordering
        import logging as _logging

        _logging.getLogger(__name__).warning(
            "Failed to load name_ja_readings.json (%s); JA sort will use default order",
            _e,
        )

health_bp = Blueprint("health_bp", __name__, url_prefix="/api/health-check")

# ---------------------------------------------------------------------------
# SYMPTOMS DATABASE (52 symptoms across 10 categories)
# ---------------------------------------------------------------------------

SYMPTOMS = [
    # Respiratory (6)
    {
        "id": "coughing",
        "name_ja": "咳",
        "name_en": "Coughing",
        "category": "respiratory",
    },
    {
        "id": "sneezing",
        "name_ja": "くしゃみ",
        "name_en": "Sneezing",
        "category": "respiratory",
    },
    {
        "id": "nasal_discharge",
        "name_ja": "鼻水",
        "name_en": "Nasal Discharge",
        "category": "respiratory",
    },
    {
        "id": "labored_breathing",
        "name_ja": "呼吸困難",
        "name_en": "Labored Breathing",
        "category": "respiratory",
    },
    {
        "id": "reverse_sneezing",
        "name_ja": "逆くしゃみ",
        "name_en": "Reverse Sneezing",
        "category": "respiratory",
    },
    {
        "id": "wheezing",
        "name_ja": "喘鳴",
        "name_en": "Wheezing",
        "category": "respiratory",
    },
    # Digestive (7)
    {
        "id": "vomiting",
        "name_ja": "嘔吐",
        "name_en": "Vomiting",
        "category": "digestive",
    },
    {
        "id": "diarrhea",
        "name_ja": "下痢",
        "name_en": "Diarrhea",
        "category": "digestive",
    },
    {
        "id": "loss_of_appetite",
        "name_ja": "食欲不振",
        "name_en": "Loss of Appetite",
        "category": "digestive",
    },
    {
        "id": "excessive_drooling",
        "name_ja": "過度のよだれ",
        "name_en": "Excessive Drooling",
        "category": "digestive",
    },
    {
        "id": "bloating",
        "name_ja": "腹部膨満",
        "name_en": "Bloating / Abdominal Distension",
        "category": "digestive",
    },
    {
        "id": "constipation",
        "name_ja": "便秘",
        "name_en": "Constipation",
        "category": "digestive",
    },
    {
        "id": "blood_in_stool",
        "name_ja": "血便",
        "name_en": "Blood in Stool",
        "category": "digestive",
    },
    # Neurological (6)
    {
        "id": "seizures",
        "name_ja": "痙攣",
        "name_en": "Seizures",
        "category": "neurological",
    },
    {
        "id": "disorientation",
        "name_ja": "方向感覚喪失",
        "name_en": "Disorientation",
        "category": "neurological",
    },
    {
        "id": "head_tilting",
        "name_ja": "首の傾き",
        "name_en": "Head Tilting",
        "category": "neurological",
    },
    {
        "id": "tremors",
        "name_ja": "震え",
        "name_en": "Tremors",
        "category": "neurological",
    },
    {
        "id": "paralysis",
        "name_ja": "麻痺",
        "name_en": "Paralysis / Paresis",
        "category": "neurological",
    },
    {
        "id": "circling",
        "name_ja": "旋回行動",
        "name_en": "Circling",
        "category": "neurological",
    },
    # Musculoskeletal (5)
    {
        "id": "limping",
        "name_ja": "跛行",
        "name_en": "Limping / Lameness",
        "category": "musculoskeletal",
    },
    {
        "id": "stiffness",
        "name_ja": "こわばり",
        "name_en": "Stiffness",
        "category": "musculoskeletal",
    },
    {
        "id": "joint_swelling",
        "name_ja": "関節の腫れ",
        "name_en": "Joint Swelling",
        "category": "musculoskeletal",
    },
    {
        "id": "reluctance_to_move",
        "name_ja": "動きたがらない",
        "name_en": "Reluctance to Move",
        "category": "musculoskeletal",
    },
    {
        "id": "muscle_wasting",
        "name_ja": "筋萎縮",
        "name_en": "Muscle Wasting / Atrophy",
        "category": "musculoskeletal",
    },
    # Dermatological (6)
    {
        "id": "itching",
        "name_ja": "かゆみ",
        "name_en": "Itching / Pruritus",
        "category": "dermatological",
    },
    {
        "id": "hair_loss",
        "name_ja": "脱毛",
        "name_en": "Hair Loss / Alopecia",
        "category": "dermatological",
    },
    {
        "id": "skin_rashes",
        "name_ja": "皮膚発疹",
        "name_en": "Skin Rashes / Lesions",
        "category": "dermatological",
    },
    {
        "id": "hot_spots",
        "name_ja": "ホットスポット",
        "name_en": "Hot Spots / Acute Moist Dermatitis",
        "category": "dermatological",
    },
    {
        "id": "dry_skin",
        "name_ja": "乾燥肌",
        "name_en": "Dry / Flaky Skin",
        "category": "dermatological",
    },
    {
        "id": "lumps_bumps",
        "name_ja": "しこり・腫瘤",
        "name_en": "Lumps and Bumps",
        "category": "dermatological",
    },
    # Urinary (5)
    {
        "id": "frequent_urination",
        "name_ja": "頻尿",
        "name_en": "Frequent Urination / Pollakiuria",
        "category": "urinary",
    },
    {
        "id": "blood_in_urine",
        "name_ja": "血尿",
        "name_en": "Blood in Urine / Hematuria",
        "category": "urinary",
    },
    {
        "id": "straining_to_urinate",
        "name_ja": "排尿困難",
        "name_en": "Straining to Urinate / Stranguria",
        "category": "urinary",
    },
    {
        "id": "incontinence",
        "name_ja": "尿失禁",
        "name_en": "Urinary Incontinence",
        "category": "urinary",
    },
    {
        "id": "excessive_thirst",
        "name_ja": "多飲",
        "name_en": "Excessive Thirst / Polydipsia",
        "category": "urinary",
    },
    # Ocular (5)
    {
        "id": "eye_discharge",
        "name_ja": "目やに",
        "name_en": "Eye Discharge",
        "category": "ocular",
    },
    {
        "id": "redness_in_eyes",
        "name_ja": "目の充血",
        "name_en": "Redness in Eyes / Conjunctival Hyperemia",
        "category": "ocular",
    },
    {
        "id": "cloudiness_in_eyes",
        "name_ja": "目の白濁",
        "name_en": "Cloudiness in Eyes / Corneal Opacity",
        "category": "ocular",
    },
    {
        "id": "squinting",
        "name_ja": "目を細める",
        "name_en": "Squinting / Blepharospasm",
        "category": "ocular",
    },
    {
        "id": "eye_swelling",
        "name_ja": "目の腫れ",
        "name_en": "Eye Swelling / Periorbital Edema",
        "category": "ocular",
    },
    # Cardiac (3)
    {
        "id": "exercise_intolerance",
        "name_ja": "運動不耐性",
        "name_en": "Exercise Intolerance",
        "category": "cardiac",
    },
    {
        "id": "fainting",
        "name_ja": "失神",
        "name_en": "Fainting / Syncope",
        "category": "cardiac",
    },
    {
        "id": "rapid_breathing",
        "name_ja": "頻呼吸",
        "name_en": "Rapid Breathing / Tachypnea",
        "category": "cardiac",
    },
    # Behavioral (4)
    {
        "id": "lethargy",
        "name_ja": "無気力",
        "name_en": "Lethargy / Depression",
        "category": "behavioral",
    },
    {
        "id": "aggression",
        "name_ja": "攻撃性",
        "name_en": "Aggression / Irritability",
        "category": "behavioral",
    },
    {
        "id": "anxiety",
        "name_ja": "不安行動",
        "name_en": "Anxiety / Restlessness",
        "category": "behavioral",
    },
    {
        "id": "excessive_licking",
        "name_ja": "過度の舐め行動",
        "name_en": "Excessive Licking",
        "category": "behavioral",
    },
    # General (5)
    {
        "id": "fever",
        "name_ja": "発熱",
        "name_en": "Fever / Pyrexia",
        "category": "general",
    },
    {
        "id": "weight_loss",
        "name_ja": "体重減少",
        "name_en": "Weight Loss",
        "category": "general",
    },
    {
        "id": "swollen_lymph_nodes",
        "name_ja": "リンパ節腫脹",
        "name_en": "Swollen Lymph Nodes / Lymphadenopathy",
        "category": "general",
    },
    {
        "id": "pale_gums",
        "name_ja": "歯茎の蒼白",
        "name_en": "Pale Gums / Pallor",
        "category": "general",
    },
    {
        "id": "jaundice",
        "name_ja": "黄疸",
        "name_en": "Jaundice / Icterus",
        "category": "general",
    },
]

SYMPTOM_IDS = {s["id"] for s in SYMPTOMS}

# ---------------------------------------------------------------------------
# DIAGNOSTIC TESTS DATABASE (34 tests)
# ---------------------------------------------------------------------------

DIAGNOSTIC_TESTS = [
    {
        "id": "cbc",
        "name_ja": "全血球計算",
        "name_en": "Complete Blood Count (CBC)",
        "priority": 1,
        "description": "Evaluates red cells, white cells, and platelets",
    },
    {
        "id": "blood_chemistry",
        "name_ja": "血液生化学検査",
        "name_en": "Blood Chemistry Panel",
        "priority": 1,
        "description": "Assesses organ function including liver and kidneys",
    },
    {
        "id": "urinalysis",
        "name_ja": "尿検査",
        "name_en": "Urinalysis",
        "priority": 2,
        "description": "Evaluates urine concentration, pH, protein, glucose, and sediment",
    },
    {
        "id": "xray",
        "name_ja": "レントゲン検査",
        "name_en": "X-ray / Radiograph",
        "priority": 2,
        "description": "Imaging of bones, chest, and abdomen",
    },
    {
        "id": "ultrasound",
        "name_ja": "超音波検査",
        "name_en": "Ultrasound / Ultrasonography",
        "priority": 2,
        "description": "Soft tissue imaging of organs and fluid",
    },
    {
        "id": "echocardiogram",
        "name_ja": "心エコー検査",
        "name_en": "Echocardiogram",
        "priority": 2,
        "description": "Ultrasound imaging of the heart structure and function",
    },
    {
        "id": "ecg",
        "name_ja": "心電図検査",
        "name_en": "Electrocardiogram (ECG/EKG)",
        "priority": 2,
        "description": "Records electrical activity of the heart",
    },
    {
        "id": "mri",
        "name_ja": "MRI検査",
        "name_en": "Magnetic Resonance Imaging (MRI)",
        "priority": 3,
        "description": "Detailed soft tissue imaging, especially brain and spinal cord",
    },
    {
        "id": "ct_scan",
        "name_ja": "CT検査",
        "name_en": "Computed Tomography (CT Scan)",
        "priority": 3,
        "description": "Cross-sectional imaging for complex anatomical evaluation",
    },
    {
        "id": "endoscopy",
        "name_ja": "内視鏡検査",
        "name_en": "Endoscopy",
        "priority": 3,
        "description": "Internal visualization of GI tract or airways",
    },
    {
        "id": "skin_scraping",
        "name_ja": "皮膚掻爬検査",
        "name_en": "Skin Scraping",
        "priority": 1,
        "description": "Microscopic evaluation of skin for parasites and fungi",
    },
    {
        "id": "skin_biopsy",
        "name_ja": "皮膚生検",
        "name_en": "Skin Biopsy",
        "priority": 3,
        "description": "Histopathological examination of skin tissue",
    },
    {
        "id": "allergy_testing",
        "name_ja": "アレルギー検査",
        "name_en": "Allergy Testing (Intradermal / Serum IgE)",
        "priority": 2,
        "description": "Identifies environmental and food allergens",
    },
    {
        "id": "thyroid_panel",
        "name_ja": "甲状腺パネル検査",
        "name_en": "Thyroid Panel (T4 / Free T4 / TSH)",
        "priority": 2,
        "description": "Evaluates thyroid gland function",
    },
    {
        "id": "acth_stimulation",
        "name_ja": "ACTH刺激試験",
        "name_en": "ACTH Stimulation Test",
        "priority": 3,
        "description": "Evaluates adrenal gland function for Cushing's or Addison's",
    },
    {
        "id": "ldds_test",
        "name_ja": "低用量デキサメタゾン抑制試験",
        "name_en": "Low-Dose Dexamethasone Suppression Test (LDDST)",
        "priority": 3,
        "description": "Confirms hyperadrenocorticism (Cushing's disease)",
    },
    {
        "id": "bile_acids",
        "name_ja": "胆汁酸検査",
        "name_en": "Bile Acids Test",
        "priority": 2,
        "description": "Assesses liver function and portal blood flow",
    },
    {
        "id": "fecal_exam",
        "name_ja": "糞便検査",
        "name_en": "Fecal Examination (Flotation / Smear)",
        "priority": 1,
        "description": "Detects intestinal parasites and abnormal bacteria",
    },
    {
        "id": "parvovirus_test",
        "name_ja": "パルボウイルス検査",
        "name_en": "Canine Parvovirus SNAP Test",
        "priority": 1,
        "description": "Rapid antigen test for parvovirus infection",
    },
    {
        "id": "heartworm_test",
        "name_ja": "フィラリア検査",
        "name_en": "Heartworm Antigen Test",
        "priority": 1,
        "description": "Detects Dirofilaria immitis antigen in blood",
    },
    {
        "id": "tick_panel",
        "name_ja": "ダニ媒介疾患パネル",
        "name_en": "Tick-Borne Disease Panel (4Dx)",
        "priority": 2,
        "description": "Tests for Lyme, Ehrlichia, Anaplasma, and heartworm",
    },
    {
        "id": "coagulation_panel",
        "name_ja": "凝固パネル検査",
        "name_en": "Coagulation Panel (PT / aPTT / Fibrinogen)",
        "priority": 2,
        "description": "Evaluates blood clotting function",
    },
    {
        "id": "joint_fluid_analysis",
        "name_ja": "関節液分析",
        "name_en": "Joint Fluid Analysis / Arthrocentesis",
        "priority": 3,
        "description": "Evaluates synovial fluid for inflammation or infection",
    },
    {
        "id": "ofa_radiograph",
        "name_ja": "OFAレントゲン検査",
        "name_en": "OFA Hip/Elbow Radiograph Evaluation",
        "priority": 2,
        "description": "Standardized radiographic evaluation of hip and elbow joints",
    },
    {
        "id": "cerf_exam",
        "name_ja": "CERF眼科検査",
        "name_en": "Ophthalmologic Exam (CERF/OFA Eye)",
        "priority": 2,
        "description": "Board-certified ophthalmologist examination",
    },
    {
        "id": "genetic_testing",
        "name_ja": "遺伝子検査",
        "name_en": "DNA / Genetic Testing",
        "priority": 2,
        "description": "Breed-specific DNA panel for hereditary conditions",
    },
    {
        "id": "tissue_biopsy",
        "name_ja": "組織生検",
        "name_en": "Tissue Biopsy / Histopathology",
        "priority": 3,
        "description": "Microscopic evaluation of tissue samples",
    },
    {
        "id": "fine_needle_aspirate",
        "name_ja": "細針吸引細胞診",
        "name_en": "Fine Needle Aspirate (FNA) Cytology",
        "priority": 2,
        "description": "Cytologic evaluation of lumps, lymph nodes, or organs",
    },
    {
        "id": "coombs_test",
        "name_ja": "クームス試験",
        "name_en": "Coombs Test (Direct Antiglobulin)",
        "priority": 3,
        "description": "Detects antibodies bound to red blood cells",
    },
    {
        "id": "csf_analysis",
        "name_ja": "脳脊髄液分析",
        "name_en": "Cerebrospinal Fluid (CSF) Analysis",
        "priority": 3,
        "description": "Evaluates CNS inflammation, infection, or neoplasia",
    },
    {
        "id": "emg",
        "name_ja": "筋電図検査",
        "name_en": "Electromyography (EMG)",
        "priority": 3,
        "description": "Evaluates electrical activity in muscles and nerves",
    },
    {
        "id": "blood_pressure",
        "name_ja": "血圧測定",
        "name_en": "Blood Pressure Measurement (Doppler / HDO)",
        "priority": 1,
        "description": "Non-invasive arterial blood pressure evaluation",
    },
    {
        "id": "fluorescein_stain",
        "name_ja": "フルオレセイン染色検査",
        "name_en": "Fluorescein Eye Stain Test",
        "priority": 1,
        "description": "Detects corneal ulcers and epithelial defects",
    },
    {
        "id": "tonometry",
        "name_ja": "眼圧検査",
        "name_en": "Tonometry (Intraocular Pressure)",
        "priority": 2,
        "description": "Measures intraocular pressure for glaucoma screening",
    },
]

DIAGNOSTIC_TEST_MAP = {t["id"]: t for t in DIAGNOSTIC_TESTS}

# ---------------------------------------------------------------------------
# SEVERITY CONFIGURATION
# ---------------------------------------------------------------------------

SEVERITY_WEIGHTS = {
    "emergency": 4.0,
    "high": 3.0,
    "moderate": 2.0,
    "low": 1.0,
}

# ---------------------------------------------------------------------------
# ONSET (TIME-COURSE) BY DISEASE ID
# ---------------------------------------------------------------------------
# Maps disease IDs to their typical onset patterns.
# "acute" = sudden (within 24h), "subacute" = days to ~1 week,
# "chronic" = weeks/months or persistent.

_DISEASE_ONSET_BY_ID: dict[str, set[str]] = {
    "brachycephalic_airway_syndrome": {"chronic"},
    "canine_parvovirus": {"acute"},
    "canine_distemper": {"acute", "subacute"},
    "kennel_cough": {"acute", "subacute"},
    "canine_influenza": {"acute"},
    "gdv_bloat": {"acute"},
    "hip_dysplasia": {"chronic"},
    "elbow_dysplasia": {"chronic"},
    "ivdd": {"acute", "chronic"},
    "degenerative_myelopathy": {"chronic"},
    "epilepsy": {"acute"},
    "atopic_dermatitis": {"subacute", "chronic"},
    "pyoderma": {"acute", "subacute"},
    "demodex_mange": {"subacute", "chronic"},
    "allergic_dermatitis": {"subacute", "chronic"},
    "hypothyroidism": {"chronic"},
    "cushings_disease": {"chronic"},
    "addisons_disease": {"acute", "chronic"},
    "diabetes_mellitus": {"chronic"},
    "chronic_kidney_disease": {"chronic"},
    "urinary_stones": {"subacute", "chronic"},
    "dcm": {"chronic"},
    "mitral_valve_disease": {"chronic"},
    "pda": {"chronic"},
    "cataracts": {"chronic"},
    "glaucoma": {"acute", "chronic"},
    "pra": {"chronic"},
    "cherry_eye": {"acute"},
    "pancreatitis": {"acute", "chronic"},
    "ibd": {"chronic"},
    "liver_disease": {"subacute", "chronic"},
    "hemangiosarcoma": {"acute", "chronic"},
    "lymphoma": {"subacute", "chronic"},
    "osteosarcoma": {"subacute", "chronic"},
    "mast_cell_tumor": {"subacute", "chronic"},
    "patellar_luxation": {"acute", "chronic"},
    "cruciate_ligament_rupture": {"acute"},
    "laryngeal_paralysis": {"chronic"},
    "megaesophagus": {"chronic"},
    "von_willebrand_disease": {"acute"},
    "imha": {"acute", "subacute"},
    "portosystemic_shunt": {"chronic"},
    "wobbler_syndrome": {"subacute", "chronic"},
    "legg_calve_perthes": {"subacute", "chronic"},
    "syringomyelia": {"chronic"},
    "tracheal_collapse": {"chronic"},
    "subaortic_stenosis": {"chronic"},
    "arvc": {"chronic"},
    "entropion": {"chronic"},
    "ectropion": {"chronic"},
    "lens_luxation": {"acute"},
    "corneal_dystrophy": {"chronic"},
    "retinal_dysplasia": {"chronic"},
    "collie_eye_anomaly": {"chronic"},
    "pug_encephalitis": {"acute", "subacute"},
    "cerebellar_ataxia": {"chronic"},
    "epi": {"chronic"},
    "familial_nephropathy": {"chronic"},
    "hemolytic_anemia": {"acute", "subacute"},
    "sebaceous_adenitis": {"chronic"},
    "dermatomyositis": {"subacute", "chronic"},
    "alopecia_x": {"chronic"},
}

# ---------------------------------------------------------------------------
# DISEASES DATABASE (43 diseases)
# ---------------------------------------------------------------------------

DISEASES = [
    # ---- 1. Brachycephalic Airway Syndrome ----
    {
        "id": "brachycephalic_airway_syndrome",
        "name_ja": "短頭種気道症候群",
        "name_en": "Brachycephalic Obstructive Airway Syndrome (BOAS)",
        "description_ja": "短頭種に見られる上気道の構造的異常の総称です。狭窄性外鼻孔、軟口蓋過長などにより呼吸困難を引き起こします。",
        "description_en": "A group of upper airway abnormalities common in flat-faced breeds. Includes stenotic nares and elongated soft palate, causing breathing difficulties.",
        "symptoms": [
            "labored_breathing",
            "wheezing",
            "reverse_sneezing",
            "exercise_intolerance",
            "coughing",
            "fainting",
        ],
        "severity": "moderate",
        "recommended_tests": ["xray", "ct_scan", "endoscopy", "blood_pressure"],
        "breed_risks": {
            "french_bulldog": 2.5,
            "english_bulldog": 2.5,
            "pug": 2.3,
            "boston_terrier": 2.0,
            "shih_tzu": 1.8,
            "cavalier_king_charles": 1.5,
            "boxer": 1.5,
            "chow_chow": 1.3,
            "shar_pei": 1.3,
        },
    },
    # ---- 2. Canine Parvovirus ----
    {
        "id": "canine_parvovirus",
        "name_ja": "犬パルボウイルス感染症",
        "name_en": "Canine Parvovirus (CPV-2)",
        "description_ja": "特に子犬に致命的な高伝染性ウイルス疾患です。消化管を攻撃し、重度の脱水と免疫抑制を引き起こします。",
        "description_en": "A highly contagious and potentially fatal viral disease, especially in puppies. Attacks the gastrointestinal tract, causing severe dehydration and immunosuppression.",
        "symptoms": [
            "vomiting",
            "diarrhea",
            "blood_in_stool",
            "lethargy",
            "loss_of_appetite",
            "fever",
            "weight_loss",
        ],
        "severity": "emergency",
        "recommended_tests": [
            "parvovirus_test",
            "cbc",
            "blood_chemistry",
            "fecal_exam",
        ],
        "breed_risks": {
            "rottweiler": 2.0,
            "doberman": 1.8,
            "german_shepherd": 1.5,
            "labrador_retriever": 1.3,
            "pit_bull": 1.5,
            "staffordshire_terrier": 1.3,
        },
    },
    # ---- 3. Canine Distemper ----
    {
        "id": "canine_distemper",
        "name_ja": "犬ジステンパー",
        "name_en": "Canine Distemper Virus (CDV)",
        "description_ja": "呼吸器・消化器・神経系を侵す重篤なウイルス疾患です。致死率が高く、回復しても神経後遺症が残ることがあります。",
        "description_en": "A severe viral disease affecting the respiratory, gastrointestinal, and nervous systems. Has a high fatality rate and may leave neurological sequelae even after recovery.",
        "symptoms": [
            "coughing",
            "sneezing",
            "nasal_discharge",
            "fever",
            "lethargy",
            "loss_of_appetite",
            "vomiting",
            "diarrhea",
            "seizures",
            "eye_discharge",
            "tremors",
        ],
        "severity": "high",
        "recommended_tests": ["cbc", "blood_chemistry", "xray", "csf_analysis"],
        "breed_risks": {
            "german_shepherd": 1.2,
            "siberian_husky": 1.2,
            "weimaraner": 1.2,
        },
    },
    # ---- 4. Kennel Cough ----
    {
        "id": "kennel_cough",
        "name_ja": "ケンネルコフ",
        "name_en": "Infectious Tracheobronchitis (Kennel Cough)",
        "description_ja": "高伝染性の呼吸器感染症で、特徴的な乾いた咳が持続します。多くは自然回復しますが、子犬や高齢犬では重症化することがあります。",
        "description_en": "A highly contagious respiratory infection characterized by a persistent dry cough. Most dogs recover naturally, but puppies and senior dogs may develop severe symptoms.",
        "symptoms": [
            "coughing",
            "sneezing",
            "nasal_discharge",
            "lethargy",
            "loss_of_appetite",
        ],
        "severity": "low",
        "recommended_tests": ["xray", "cbc"],
        "breed_risks": {
            "french_bulldog": 1.3,
            "english_bulldog": 1.3,
            "pug": 1.2,
            "cavalier_king_charles": 1.1,
        },
    },
    # ---- 5. Canine Influenza ----
    {
        "id": "canine_influenza",
        "name_ja": "犬インフルエンザ",
        "name_en": "Canine Influenza Virus (CIV H3N2/H3N8)",
        "description_ja": "犬インフルエンザウイルスによる呼吸器感染症です。咳、鼻汁、発熱を伴い、多頭環境で急速に広がります。",
        "description_en": "A respiratory infection caused by canine influenza virus. Presents with coughing, nasal discharge, and fever, spreading rapidly in multi-dog environments.",
        "symptoms": [
            "coughing",
            "sneezing",
            "nasal_discharge",
            "fever",
            "lethargy",
            "loss_of_appetite",
            "labored_breathing",
        ],
        "severity": "low",
        "recommended_tests": ["xray", "cbc", "blood_chemistry"],
        "breed_risks": {
            "french_bulldog": 1.3,
            "english_bulldog": 1.3,
            "pug": 1.2,
        },
    },
    # ---- 6. Gastric Dilatation-Volvulus (GDV / Bloat) ----
    {
        "id": "gdv_bloat",
        "name_ja": "胃拡張捻転症候群",
        "name_en": "Gastric Dilatation-Volvulus (GDV / Bloat)",
        "description_ja": "胃がガスで膨張し捻転する生命を脅かす緊急疾患です。治療しなければ数時間で死亡する可能性があります。",
        "description_en": "A life-threatening emergency where the stomach fills with gas and twists. Without treatment, it can be fatal within hours.",
        "symptoms": [
            "bloating",
            "vomiting",
            "excessive_drooling",
            "lethargy",
            "rapid_breathing",
            "pale_gums",
            "anxiety",
        ],
        "severity": "emergency",
        "recommended_tests": [
            "xray",
            "blood_chemistry",
            "cbc",
            "ecg",
            "blood_pressure",
        ],
        "breed_risks": {
            "great_dane": 2.5,
            "weimaraner": 2.0,
            "saint_bernard": 2.0,
            "irish_wolfhound": 2.0,
            "german_shepherd": 1.8,
            "irish_setter": 1.8,
            "bloodhound": 1.8,
            "scottish_deerhound": 1.8,
            "doberman": 1.5,
            "basset_hound": 1.5,
            "old_english_sheepdog": 1.5,
            "boxer": 1.3,
            "rottweiler": 1.3,
            "newfoundland": 1.3,
            "akita": 1.3,
        },
    },
    # ---- 7. Hip Dysplasia ----
    {
        "id": "hip_dysplasia",
        "name_ja": "股関節形成不全",
        "name_en": "Hip Dysplasia",
        "description_ja": "股関節の発育異常で、関節の不適合により早期の変形性関節症を引き起こす遺伝性疾患です。",
        "description_en": "A hereditary condition where the hip joint develops abnormally, leading to joint instability and early-onset osteoarthritis.",
        "symptoms": [
            "limping",
            "stiffness",
            "reluctance_to_move",
            "muscle_wasting",
            "joint_swelling",
        ],
        "severity": "moderate",
        "recommended_tests": ["ofa_radiograph", "xray"],
        "breed_risks": {
            "german_shepherd": 2.0,
            "bernese_mountain_dog": 2.0,
            "saint_bernard": 2.0,
            "golden_retriever": 1.8,
            "labrador_retriever": 1.8,
            "rottweiler": 1.8,
            "newfoundland": 1.8,
            "english_bulldog": 1.5,
            "great_dane": 1.5,
            "chow_chow": 1.5,
            "old_english_sheepdog": 1.4,
            "giant_schnauzer": 1.3,
            "samoyed": 1.3,
        },
    },
    # ---- 8. Elbow Dysplasia ----
    {
        "id": "elbow_dysplasia",
        "name_ja": "肘関節形成不全",
        "name_en": "Elbow Dysplasia",
        "description_ja": "成長期の肘関節の発育異常の総称で、内側鉤状突起分離、離断性骨軟骨炎などの病態を含みます。",
        "description_en": "A group of developmental abnormalities of the elbow joint, including fragmented coronoid process and osteochondritis dissecans.",
        "symptoms": ["limping", "stiffness", "joint_swelling", "reluctance_to_move"],
        "severity": "moderate",
        "recommended_tests": ["ofa_radiograph", "xray", "ct_scan"],
        "breed_risks": {
            "labrador_retriever": 2.0,
            "bernese_mountain_dog": 2.0,
            "golden_retriever": 1.8,
            "german_shepherd": 1.8,
            "rottweiler": 1.8,
            "newfoundland": 1.8,
            "chow_chow": 1.5,
            "basset_hound": 1.5,
            "saint_bernard": 1.5,
            "shar_pei": 1.3,
        },
    },
    # ---- 9. Intervertebral Disc Disease (IVDD) ----
    {
        "id": "ivdd",
        "name_ja": "椎間板ヘルニア",
        "name_en": "Intervertebral Disc Disease (IVDD)",
        "description_ja": "椎間板が脊髄を圧迫する疾患で、突然の痛みや麻痺を引き起こします。ダックスフンドなどの軟骨異栄養犬種に多発します。",
        "description_en": "A condition where intervertebral discs compress the spinal cord, causing sudden pain or paralysis. Common in chondrodystrophic breeds like Dachshunds.",
        "symptoms": [
            "limping",
            "paralysis",
            "reluctance_to_move",
            "stiffness",
            "tremors",
            "incontinence",
        ],
        "severity": "moderate",
        "recommended_tests": ["mri", "xray", "ct_scan", "emg"],
        "breed_risks": {
            "dachshund": 2.5,
            "french_bulldog": 2.0,
            "corgi": 2.0,
            "basset_hound": 1.8,
            "beagle": 1.5,
            "cocker_spaniel": 1.5,
            "shih_tzu": 1.5,
            "lhasa_apso": 1.5,
        },
    },
    # ---- 10. Degenerative Myelopathy ----
    {
        "id": "degenerative_myelopathy",
        "name_ja": "変性性脊髄症",
        "name_en": "Degenerative Myelopathy (DM)",
        "description_ja": "脊髄の白質が進行性に変性する神経疾患です。後肢の麻痺が徐々に進行し、最終的には四肢麻痺に至ります。",
        "description_en": "A progressive neurological disease causing degeneration of the spinal cord white matter. Leads to gradual hind limb paralysis progressing to quadriplegia.",
        "symptoms": [
            "paralysis",
            "stiffness",
            "reluctance_to_move",
            "muscle_wasting",
            "incontinence",
        ],
        "severity": "high",
        "recommended_tests": ["mri", "genetic_testing", "emg", "csf_analysis"],
        "breed_risks": {
            "german_shepherd": 2.5,
            "corgi": 2.0,
            "boxer": 1.8,
            "rhodesian_ridgeback": 1.5,
            "bernese_mountain_dog": 1.5,
            "pug": 1.5,
            "irish_setter": 1.3,
        },
    },
    # ---- 11. Epilepsy ----
    {
        "id": "epilepsy",
        "name_ja": "てんかん",
        "name_en": "Idiopathic Epilepsy",
        "description_ja": "反復性の痙攣発作を特徴とする神経疾患です。特発性てんかんが最も多く、生涯にわたる投薬管理が必要です。",
        "description_en": "A neurological disorder characterized by recurrent seizures. Idiopathic epilepsy is the most common form and requires lifelong medication management.",
        "symptoms": [
            "seizures",
            "disorientation",
            "tremors",
            "excessive_drooling",
            "loss_of_appetite",
            "lethargy",
        ],
        "severity": "moderate",
        "recommended_tests": ["mri", "cbc", "blood_chemistry", "csf_analysis", "ecg"],
        "breed_risks": {
            "beagle": 2.0,
            "border_collie": 1.8,
            "german_shepherd": 1.8,
            "vizsla": 1.8,
            "golden_retriever": 1.5,
            "labrador_retriever": 1.5,
            "australian_shepherd": 1.5,
            "shetland_sheepdog": 1.5,
            "bernese_mountain_dog": 1.5,
            "irish_wolfhound": 1.5,
            "irish_setter": 1.3,
        },
    },
    # ---- 12. Atopic Dermatitis ----
    {
        "id": "atopic_dermatitis",
        "name_ja": "アトピー性皮膚炎",
        "name_en": "Canine Atopic Dermatitis (CAD)",
        "description_ja": "環境アレルゲン（ダニ、花粉、カビなど）に対する遺伝的素因を持つ犬に発症するアレルギー性皮膚疾患です。",
        "description_en": "An allergic skin condition in genetically predisposed dogs triggered by environmental allergens such as dust mites, pollen, and mold.",
        "symptoms": [
            "itching",
            "hair_loss",
            "skin_rashes",
            "hot_spots",
            "excessive_licking",
            "redness_in_eyes",
        ],
        "severity": "low",
        "recommended_tests": ["allergy_testing", "skin_scraping", "skin_biopsy"],
        "breed_risks": {
            "west_highland_terrier": 2.5,
            "french_bulldog": 2.0,
            "english_bulldog": 2.0,
            "shar_pei": 2.0,
            "golden_retriever": 1.8,
            "labrador_retriever": 1.8,
            "boxer": 1.5,
            "dalmatian": 1.5,
            "shih_tzu": 1.5,
            "cocker_spaniel": 1.5,
            "german_shepherd": 1.5,
            "lhasa_apso": 1.3,
        },
    },
    # ---- 13. Pyoderma ----
    {
        "id": "pyoderma",
        "name_ja": "膿皮症",
        "name_en": "Bacterial Pyoderma",
        "description_ja": "細菌感染による皮膚疾患で、膿疱や痂皮を形成します。アレルギーや免疫低下が基礎疾患となることが多いです。",
        "description_en": "A bacterial skin infection forming pustules and crusts. Often secondary to underlying allergies or immunosuppression.",
        "symptoms": ["itching", "hair_loss", "skin_rashes", "hot_spots", "fever"],
        "severity": "low",
        "recommended_tests": ["skin_scraping", "skin_biopsy", "cbc"],
        "breed_risks": {
            "german_shepherd": 2.0,
            "english_bulldog": 1.8,
            "shar_pei": 1.8,
            "cocker_spaniel": 1.5,
            "dalmatian": 1.3,
            "french_bulldog": 1.3,
            "boxer": 1.3,
        },
    },
    # ---- 14. Demodex Mange ----
    {
        "id": "demodex_mange",
        "name_ja": "毛包虫症（ニキビダニ症）",
        "name_en": "Demodectic Mange (Demodicosis)",
        "description_ja": "常在性のニキビダニが免疫低下時に異常増殖し、脱毛や皮膚炎を引き起こす寄生虫性皮膚疾患です。",
        "description_en": "A parasitic skin disease caused by overgrowth of Demodex mites during immune suppression, resulting in hair loss and dermatitis.",
        "symptoms": ["hair_loss", "skin_rashes", "itching", "dry_skin"],
        "severity": "moderate",
        "recommended_tests": ["skin_scraping", "skin_biopsy"],
        "breed_risks": {
            "shar_pei": 2.0,
            "english_bulldog": 1.8,
            "pit_bull": 1.5,
            "staffordshire_terrier": 1.5,
            "boxer": 1.3,
            "french_bulldog": 1.3,
            "boston_terrier": 1.2,
            "german_shepherd": 1.2,
        },
    },
    # ---- 15. Allergic Dermatitis ----
    {
        "id": "allergic_dermatitis",
        "name_ja": "アレルギー性皮膚炎",
        "name_en": "Allergic Dermatitis (Food / Contact)",
        "description_ja": "食物や接触アレルゲンに対する過敏反応による皮膚炎です。痒み、皮疹、消化器症状を伴うことがあります。",
        "description_en": "Dermatitis caused by hypersensitivity to food or contact allergens. May present with itching, skin rashes, and gastrointestinal symptoms.",
        "symptoms": [
            "itching",
            "skin_rashes",
            "hair_loss",
            "excessive_licking",
            "hot_spots",
            "vomiting",
            "diarrhea",
        ],
        "severity": "low",
        "recommended_tests": [
            "allergy_testing",
            "skin_scraping",
            "blood_chemistry",
            "fecal_exam",
        ],
        "breed_risks": {
            "west_highland_terrier": 2.0,
            "labrador_retriever": 1.8,
            "cocker_spaniel": 1.8,
            "french_bulldog": 1.8,
            "golden_retriever": 1.5,
            "german_shepherd": 1.5,
            "boxer": 1.5,
            "dalmatian": 1.3,
            "shar_pei": 1.5,
        },
    },
    # ---- 16. Hypothyroidism ----
    {
        "id": "hypothyroidism",
        "name_ja": "甲状腺機能低下症",
        "name_en": "Hypothyroidism",
        "description_ja": "犬で最も一般的な内分泌疾患の一つです。甲状腺ホルモンの不足により代謝が低下し、全身に様々な症状が現れます。",
        "description_en": "One of the most common endocrine disorders in dogs. Insufficient thyroid hormone production leads to decreased metabolism with widespread systemic effects.",
        "symptoms": [
            "lethargy",
            "hair_loss",
            "dry_skin",
            "stiffness",
            "exercise_intolerance",
        ],
        "severity": "moderate",
        "recommended_tests": ["thyroid_panel", "cbc", "blood_chemistry"],
        "breed_risks": {
            "golden_retriever": 2.0,
            "doberman": 2.0,
            "irish_setter": 1.8,
            "old_english_sheepdog": 1.5,
            "shetland_sheepdog": 1.5,
            "greyhound": 1.5,
            "cocker_spaniel": 1.5,
            "dachshund": 1.5,
            "great_dane": 1.3,
            "boxer": 1.3,
            "samoyed": 1.3,
        },
    },
    # ---- 17. Cushing's Disease ----
    {
        "id": "cushings_disease",
        "name_ja": "クッシング症候群（副腎皮質機能亢進症）",
        "name_en": "Hyperadrenocorticism (Cushing's Disease)",
        "description_ja": "コルチゾールが過剰に産生される疾患です。多飲多尿、腹部膨満、脱毛などの症状がゆっくり進行します。",
        "description_en": "A condition of excess cortisol production. Symptoms such as increased thirst/urination, abdominal distension, and hair loss progress gradually.",
        "symptoms": [
            "excessive_thirst",
            "frequent_urination",
            "hair_loss",
            "bloating",
            "lethargy",
            "muscle_wasting",
            "skin_rashes",
        ],
        "severity": "moderate",
        "recommended_tests": [
            "acth_stimulation",
            "ldds_test",
            "blood_chemistry",
            "urinalysis",
            "ultrasound",
        ],
        "breed_risks": {
            "poodle": 2.0,
            "dachshund": 2.0,
            "beagle": 1.8,
            "boxer": 1.8,
            "boston_terrier": 1.5,
            "yorkshire_terrier": 1.5,
            "german_shepherd": 1.3,
            "labrador_retriever": 1.2,
        },
    },
    # ---- 18. Addison's Disease ----
    {
        "id": "addisons_disease",
        "name_ja": "アジソン病（副腎皮質機能低下症）",
        "name_en": "Hypoadrenocorticism (Addison's Disease)",
        "description_ja": "副腎ホルモンの不足で起こる疾患です。症状が非特異的で診断が難しく「偉大な模倣者」と呼ばれます。",
        "description_en": "A condition caused by insufficient adrenal hormones. Known as 'the great imitator' due to its nonspecific symptoms that make diagnosis challenging.",
        "symptoms": [
            "lethargy",
            "vomiting",
            "diarrhea",
            "loss_of_appetite",
            "weight_loss",
            "tremors",
            "fainting",
        ],
        "severity": "high",
        "recommended_tests": ["acth_stimulation", "cbc", "blood_chemistry", "ecg"],
        "breed_risks": {
            "poodle": 2.0,
            "west_highland_terrier": 1.8,
            "great_dane": 1.5,
            "rottweiler": 1.3,
            "labrador_retriever": 1.3,
            "springer_spaniel": 1.3,
            "whippet": 1.3,
        },
    },
    # ---- 19. Diabetes Mellitus ----
    {
        "id": "diabetes_mellitus",
        "name_ja": "糖尿病",
        "name_en": "Diabetes Mellitus",
        "description_ja": "インスリンの不足または作用不全により血糖値が慢性的に高くなる代謝疾患です。生涯にわたるインスリン注射が必要です。",
        "description_en": "A metabolic disorder with chronically elevated blood sugar due to insulin deficiency or resistance. Requires lifelong insulin injections.",
        "symptoms": [
            "excessive_thirst",
            "frequent_urination",
            "weight_loss",
            "lethargy",
            "loss_of_appetite",
            "cloudiness_in_eyes",
        ],
        "severity": "moderate",
        "recommended_tests": ["blood_chemistry", "urinalysis", "cbc"],
        "breed_risks": {
            "samoyed": 2.5,
            "miniature_schnauzer": 1.8,
            "poodle": 1.5,
            "pug": 1.5,
            "bichon_frise": 1.5,
            "beagle": 1.3,
            "yorkshire_terrier": 1.2,
        },
    },
    # ---- 20. Chronic Kidney Disease ----
    {
        "id": "chronic_kidney_disease",
        "name_ja": "慢性腎臓病",
        "name_en": "Chronic Kidney Disease (CKD)",
        "description_ja": "腎機能が不可逆的に低下する進行性疾患です。早期発見が重要で、IRIS分類に基づくステージ管理が行われます。",
        "description_en": "A progressive condition with irreversible decline in kidney function. Early detection is crucial, managed according to IRIS staging guidelines.",
        "symptoms": [
            "excessive_thirst",
            "frequent_urination",
            "vomiting",
            "weight_loss",
            "loss_of_appetite",
            "lethargy",
            "pale_gums",
        ],
        "severity": "high",
        "recommended_tests": [
            "blood_chemistry",
            "urinalysis",
            "ultrasound",
            "blood_pressure",
            "cbc",
        ],
        "breed_risks": {
            "bull_terrier": 1.8,
            "cavalier_king_charles": 1.5,
            "shar_pei": 1.5,
            "cocker_spaniel": 1.5,
            "german_shepherd": 1.3,
            "bernese_mountain_dog": 1.3,
            "boxer": 1.2,
        },
    },
    # ---- 21. Urinary Stones ----
    {
        "id": "urinary_stones",
        "name_ja": "尿路結石症",
        "name_en": "Urolithiasis (Urinary Stones)",
        "description_ja": "膀胱内にミネラルの結晶が集まって結石を形成する疾患です。ストルバイトとシュウ酸カルシウムが最も多いタイプです。",
        "description_en": "A condition where mineral crystals accumulate in the bladder to form stones. Struvite and calcium oxalate are the most common types.",
        "symptoms": [
            "blood_in_urine",
            "straining_to_urinate",
            "frequent_urination",
            "vomiting",
            "lethargy",
            "loss_of_appetite",
        ],
        "severity": "moderate",
        "recommended_tests": ["urinalysis", "xray", "ultrasound", "blood_chemistry"],
        "breed_risks": {
            "dalmatian": 2.5,
            "miniature_schnauzer": 2.0,
            "english_bulldog": 1.8,
            "shih_tzu": 1.8,
            "yorkshire_terrier": 1.5,
            "lhasa_apso": 1.5,
            "bichon_frise": 1.5,
            "pug": 1.3,
        },
    },
    # ---- 22. Dilated Cardiomyopathy (DCM) ----
    {
        "id": "dcm",
        "name_ja": "拡張型心筋症",
        "name_en": "Dilated Cardiomyopathy (DCM)",
        "description_ja": "心筋が薄くなり心室が拡張する心疾患です。心臓のポンプ機能が低下し、鬱血性心不全に至ることがあります。",
        "description_en": "A heart disease where the heart muscle thins and ventricles enlarge. Leads to decreased pumping ability and may progress to congestive heart failure.",
        "symptoms": [
            "exercise_intolerance",
            "coughing",
            "lethargy",
            "fainting",
            "rapid_breathing",
            "loss_of_appetite",
            "bloating",
        ],
        "severity": "high",
        "recommended_tests": [
            "echocardiogram",
            "ecg",
            "xray",
            "cbc",
            "blood_chemistry",
        ],
        "breed_risks": {
            "doberman": 2.5,
            "great_dane": 2.0,
            "irish_wolfhound": 2.0,
            "boxer": 2.0,
            "scottish_deerhound": 1.8,
            "newfoundland": 1.8,
            "cocker_spaniel": 1.5,
            "dalmatian": 1.5,
            "saint_bernard": 1.5,
        },
    },
    # ---- 23. Mitral Valve Disease ----
    {
        "id": "mitral_valve_disease",
        "name_ja": "僧帽弁閉鎖不全症",
        "name_en": "Myxomatous Mitral Valve Disease (MMVD)",
        "description_ja": "犬で最も多い後天性心疾患です。僧帽弁の変性により弁が閉鎖不全となり、血液の逆流が生じます。",
        "description_en": "The most common acquired heart disease in dogs. Degeneration of the mitral valve causes incomplete closure and blood regurgitation.",
        "symptoms": [
            "coughing",
            "exercise_intolerance",
            "rapid_breathing",
            "fainting",
            "lethargy",
        ],
        "severity": "moderate",
        "recommended_tests": ["echocardiogram", "ecg", "xray"],
        "breed_risks": {
            "cavalier_king_charles": 2.5,
            "dachshund": 1.5,
            "chihuahua": 1.5,
            "poodle": 1.5,
            "maltese": 1.3,
            "yorkshire_terrier": 1.3,
            "cocker_spaniel": 1.3,
            "pomeranian": 1.3,
            "shih_tzu": 1.3,
            "whippet": 1.2,
        },
    },
    # ---- 24. Patent Ductus Arteriosus (PDA) ----
    {
        "id": "pda",
        "name_ja": "動脈管開存症",
        "name_en": "Patent Ductus Arteriosus (PDA)",
        "description_ja": "出生後に閉鎖すべき動脈管が開存し続ける先天性心疾患です。早期の外科的閉鎖により予後は良好です。",
        "description_en": "A congenital heart defect where the ductus arteriosus fails to close after birth. Early surgical closure provides an excellent prognosis.",
        "symptoms": [
            "exercise_intolerance",
            "coughing",
            "rapid_breathing",
            "fainting",
            "lethargy",
            "labored_breathing",
        ],
        "severity": "moderate",
        "recommended_tests": ["echocardiogram", "ecg", "xray"],
        "breed_risks": {
            "maltese": 2.0,
            "poodle": 2.0,
            "pomeranian": 1.8,
            "shetland_sheepdog": 1.8,
            "german_shepherd": 1.5,
            "cocker_spaniel": 1.5,
            "chihuahua": 1.5,
        },
    },
    # ---- 25. Cataracts ----
    {
        "id": "cataracts",
        "name_ja": "白内障",
        "name_en": "Cataracts",
        "description_ja": "水晶体が白濁し視力が低下する疾患です。遺伝性、老齢性、糖尿病性など原因は様々です。",
        "description_en": "A condition where the lens of the eye becomes cloudy, leading to decreased vision. Causes include hereditary, age-related, and diabetic factors.",
        "symptoms": ["cloudiness_in_eyes", "squinting", "eye_discharge"],
        "severity": "moderate",
        "recommended_tests": ["cerf_exam"],
        "breed_risks": {
            "boston_terrier": 2.0,
            "cocker_spaniel": 2.0,
            "poodle": 1.8,
            "siberian_husky": 1.8,
            "golden_retriever": 1.5,
            "labrador_retriever": 1.5,
            "bichon_frise": 1.5,
            "miniature_schnauzer": 1.5,
            "yorkshire_terrier": 1.3,
            "italian_greyhound": 1.3,
        },
    },
    # ---- 26. Glaucoma ----
    {
        "id": "glaucoma",
        "name_ja": "緑内障",
        "name_en": "Glaucoma",
        "description_ja": "眼圧の上昇により視神経が障害される疾患です。急性発作は非常に痛く、数時間で不可逆的な視力喪失を起こす緊急疾患です。",
        "description_en": "A condition where elevated intraocular pressure damages the optic nerve. Acute episodes are extremely painful and can cause irreversible vision loss within hours.",
        "symptoms": [
            "redness_in_eyes",
            "cloudiness_in_eyes",
            "squinting",
            "eye_swelling",
            "lethargy",
        ],
        "severity": "moderate",
        "recommended_tests": ["tonometry", "cerf_exam"],
        "breed_risks": {
            "cocker_spaniel": 2.5,
            "beagle": 2.0,
            "basset_hound": 2.0,
            "shar_pei": 1.8,
            "shiba_inu": 1.5,
            "siberian_husky": 1.5,
            "chow_chow": 1.5,
            "great_dane": 1.3,
            "dalmatian": 1.3,
        },
    },
    # ---- 27. Progressive Retinal Atrophy (PRA) ----
    {
        "id": "pra",
        "name_ja": "進行性網膜萎縮症",
        "name_en": "Progressive Retinal Atrophy (PRA)",
        "description_ja": "網膜の光受容細胞が進行性に変性・消失する遺伝性の眼疾患です。夜盲症から始まり、最終的に失明に至ります。",
        "description_en": "A hereditary eye disease where retinal photoreceptor cells progressively degenerate. Begins with night blindness and eventually leads to total blindness.",
        "symptoms": [
            "cloudiness_in_eyes",
            "squinting",
            "disorientation",
            "anxiety",
        ],
        "severity": "moderate",
        "recommended_tests": ["cerf_exam", "genetic_testing"],
        "breed_risks": {
            "cocker_spaniel": 2.0,
            "labrador_retriever": 2.0,
            "irish_setter": 2.0,
            "golden_retriever": 1.8,
            "miniature_schnauzer": 1.5,
            "dachshund": 1.5,
            "poodle": 1.5,
            "italian_greyhound": 1.3,
        },
    },
    # ---- 28. Cherry Eye ----
    {
        "id": "cherry_eye",
        "name_ja": "チェリーアイ（第三眼瞼腺逸脱）",
        "name_en": "Cherry Eye (Prolapsed Third Eyelid Gland)",
        "description_ja": "第三眼瞼の涙腺が突出する疾患です。赤いさくらんぼ状の腫れが目の内側に現れます。外科的整復が推奨されます。",
        "description_en": "A condition where the tear gland of the third eyelid prolapses, appearing as a red cherry-like swelling at the inner eye. Surgical repositioning is recommended.",
        "symptoms": [
            "eye_swelling",
            "redness_in_eyes",
            "eye_discharge",
            "squinting",
        ],
        "severity": "low",
        "recommended_tests": ["cerf_exam"],
        "breed_risks": {
            "english_bulldog": 2.5,
            "french_bulldog": 2.0,
            "cocker_spaniel": 2.0,
            "beagle": 1.8,
            "bloodhound": 1.8,
            "shar_pei": 1.5,
            "lhasa_apso": 1.5,
            "shih_tzu": 1.5,
            "boston_terrier": 1.5,
        },
    },
    # ---- 29. Pancreatitis ----
    {
        "id": "pancreatitis",
        "name_ja": "膵炎",
        "name_en": "Pancreatitis (Acute / Chronic)",
        "description_ja": "膵臓の炎症で、消化酵素が膵臓自体を消化してしまう自己消化が本態です。高脂肪食や肥満が誘因となります。",
        "description_en": "Inflammation of the pancreas where digestive enzymes begin to digest the pancreas itself. High-fat diets and obesity are common triggers.",
        "symptoms": [
            "vomiting",
            "diarrhea",
            "loss_of_appetite",
            "lethargy",
            "bloating",
            "fever",
        ],
        "severity": "moderate",
        "recommended_tests": ["blood_chemistry", "ultrasound", "cbc"],
        "breed_risks": {
            "miniature_schnauzer": 2.5,
            "cocker_spaniel": 1.8,
            "yorkshire_terrier": 1.5,
            "poodle": 1.3,
            "cavalier_king_charles": 1.3,
            "shetland_sheepdog": 1.3,
        },
    },
    # ---- 30. Inflammatory Bowel Disease (IBD) ----
    {
        "id": "ibd",
        "name_ja": "炎症性腸疾患",
        "name_en": "Inflammatory Bowel Disease (IBD)",
        "description_ja": "消化管壁に慢性的な炎症細胞浸潤を生じる疾患群です。慢性の嘔吐、下痢、体重減少を引き起こします。",
        "description_en": "A group of conditions with chronic inflammatory cell infiltration of the GI tract wall. Causes chronic vomiting, diarrhea, and weight loss.",
        "symptoms": [
            "vomiting",
            "diarrhea",
            "weight_loss",
            "loss_of_appetite",
            "blood_in_stool",
            "lethargy",
        ],
        "severity": "moderate",
        "recommended_tests": [
            "endoscopy",
            "tissue_biopsy",
            "blood_chemistry",
            "fecal_exam",
            "ultrasound",
        ],
        "breed_risks": {
            "german_shepherd": 2.0,
            "boxer": 1.8,
            "french_bulldog": 1.5,
            "irish_setter": 1.5,
            "basset_hound": 1.5,
            "rottweiler": 1.3,
            "yorkshire_terrier": 1.3,
        },
    },
    # ---- 31. Liver Disease ----
    {
        "id": "liver_disease",
        "name_ja": "肝臓病",
        "name_en": "Hepatopathy (Liver Disease)",
        "description_ja": "肝臓に影響する様々な疾患の総称です。肝臓は再生能力が高いため、症状が現れた時にはかなり進行していることが多いです。",
        "description_en": "A general term for various liver conditions. Due to the liver's strong regenerative capacity, symptoms often appear only at advanced stages.",
        "symptoms": [
            "jaundice",
            "vomiting",
            "loss_of_appetite",
            "weight_loss",
            "lethargy",
            "excessive_thirst",
            "bloating",
            "seizures",
        ],
        "severity": "high",
        "recommended_tests": [
            "blood_chemistry",
            "bile_acids",
            "ultrasound",
            "tissue_biopsy",
            "cbc",
        ],
        "breed_risks": {
            "yorkshire_terrier": 2.0,
            "maltese": 1.8,
            "doberman": 1.5,
            "irish_wolfhound": 1.5,
            "labrador_retriever": 1.3,
            "cocker_spaniel": 1.3,
        },
    },
    # ---- 32. Hemangiosarcoma ----
    {
        "id": "hemangiosarcoma",
        "name_ja": "血管肉腫",
        "name_en": "Hemangiosarcoma (HSA)",
        "description_ja": "血管内皮細胞由来の悪性腫瘍です。脾臓、心臓、肝臓に好発し、突然の内出血で発見されることが多いです。",
        "description_en": "A malignant tumor originating from blood vessel endothelial cells. Commonly affects the spleen, heart, and liver, often discovered after sudden internal bleeding.",
        "symptoms": [
            "lethargy",
            "loss_of_appetite",
            "pale_gums",
            "bloating",
            "weight_loss",
            "fainting",
            "rapid_breathing",
        ],
        "severity": "high",
        "recommended_tests": [
            "ultrasound",
            "cbc",
            "blood_chemistry",
            "xray",
            "fine_needle_aspirate",
        ],
        "breed_risks": {
            "german_shepherd": 2.5,
            "golden_retriever": 2.0,
            "labrador_retriever": 1.8,
            "boxer": 1.5,
            "bernese_mountain_dog": 1.5,
            "vizsla": 1.5,
            "greyhound": 1.5,
        },
    },
    # ---- 33. Lymphoma ----
    {
        "id": "lymphoma",
        "name_ja": "リンパ腫",
        "name_en": "Lymphoma (Lymphosarcoma)",
        "description_ja": "リンパ球の悪性腫瘍で、犬で最も多い血液系腫瘍です。リンパ節の腫大が特徴的で、化学療法に比較的良好に反応します。",
        "description_en": "A malignant tumor of lymphocytes and the most common hematopoietic cancer in dogs. Characterized by enlarged lymph nodes and relatively responsive to chemotherapy.",
        "symptoms": [
            "swollen_lymph_nodes",
            "lethargy",
            "loss_of_appetite",
            "weight_loss",
            "vomiting",
            "diarrhea",
        ],
        "severity": "high",
        "recommended_tests": [
            "fine_needle_aspirate",
            "tissue_biopsy",
            "cbc",
            "blood_chemistry",
            "ultrasound",
            "xray",
        ],
        "breed_risks": {
            "golden_retriever": 2.0,
            "boxer": 2.0,
            "bernese_mountain_dog": 1.8,
            "rottweiler": 1.5,
            "scottish_terrier": 1.5,
            "basset_hound": 1.3,
            "saint_bernard": 1.3,
            "english_bulldog": 1.2,
        },
    },
    # ---- 34. Osteosarcoma ----
    {
        "id": "osteosarcoma",
        "name_ja": "骨肉腫",
        "name_en": "Osteosarcoma (Bone Cancer)",
        "description_ja": "骨の悪性腫瘍で、犬の原発性骨腫瘍の約85%を占めます。大型犬の四肢に好発し、早期の転移が特徴です。",
        "description_en": "A malignant bone tumor accounting for approximately 85% of primary bone tumors in dogs. Common in large breed limbs with a tendency for early metastasis.",
        "symptoms": [
            "limping",
            "joint_swelling",
            "lethargy",
            "loss_of_appetite",
            "weight_loss",
        ],
        "severity": "high",
        "recommended_tests": ["xray", "tissue_biopsy", "cbc", "blood_chemistry"],
        "breed_risks": {
            "great_dane": 2.5,
            "irish_wolfhound": 2.5,
            "rottweiler": 2.0,
            "greyhound": 2.0,
            "saint_bernard": 1.8,
            "german_shepherd": 1.5,
            "doberman": 1.5,
            "golden_retriever": 1.3,
            "labrador_retriever": 1.3,
            "giant_schnauzer": 1.3,
        },
    },
    # ---- 35. Mast Cell Tumor ----
    {
        "id": "mast_cell_tumor",
        "name_ja": "肥満細胞腫",
        "name_en": "Mast Cell Tumor (MCT)",
        "description_ja": "犬の皮膚腫瘍で最も多い悪性腫瘍です。グレードにより予後が大きく異なり、早期の外科的切除が重要です。",
        "description_en": "The most common malignant skin tumor in dogs. Prognosis varies significantly by grade, and early surgical excision is crucial.",
        "symptoms": [
            "lumps_bumps",
            "itching",
            "vomiting",
            "loss_of_appetite",
            "lethargy",
        ],
        "severity": "moderate",
        "recommended_tests": [
            "fine_needle_aspirate",
            "tissue_biopsy",
            "cbc",
            "blood_chemistry",
            "ultrasound",
        ],
        "breed_risks": {
            "boxer": 2.5,
            "boston_terrier": 2.0,
            "pug": 1.8,
            "shar_pei": 1.8,
            "labrador_retriever": 1.5,
            "golden_retriever": 1.5,
            "rhodesian_ridgeback": 1.5,
            "staffordshire_terrier": 1.5,
            "beagle": 1.3,
        },
    },
    # ---- 36. Patellar Luxation ----
    {
        "id": "patellar_luxation",
        "name_ja": "膝蓋骨脱臼",
        "name_en": "Patellar Luxation",
        "description_ja": "膝蓋骨が正常な位置から内側または外側にずれる疾患です。小型犬に多く、グレード1〜4で重症度が分類されます。",
        "description_en": "A condition where the kneecap dislocates medially or laterally from its normal position. Common in small breeds, graded from 1 (mild) to 4 (severe).",
        "symptoms": ["limping", "stiffness", "reluctance_to_move"],
        "severity": "low",
        "recommended_tests": ["xray", "ofa_radiograph"],
        "breed_risks": {
            "yorkshire_terrier": 2.5,
            "chihuahua": 2.5,
            "pomeranian": 2.0,
            "maltese": 2.0,
            "italian_greyhound": 2.0,
            "french_bulldog": 1.8,
            "boston_terrier": 1.8,
            "poodle": 1.5,
            "bichon_frise": 1.5,
            "lhasa_apso": 1.5,
            "cavalier_king_charles": 1.3,
            "shih_tzu": 1.3,
            "havanese": 1.3,
        },
    },
    # ---- 37. Cruciate Ligament Rupture ----
    {
        "id": "cruciate_ligament_rupture",
        "name_ja": "前十字靭帯断裂",
        "name_en": "Cranial Cruciate Ligament (CCL) Rupture",
        "description_ja": "犬で最も多い整形外科疾患の一つです。膝関節の不安定性と疼痛を引き起こし、外科的治療が標準です。",
        "description_en": "One of the most common orthopedic conditions in dogs. Causes knee joint instability and pain, with surgical treatment as the standard of care.",
        "symptoms": [
            "limping",
            "joint_swelling",
            "stiffness",
            "reluctance_to_move",
        ],
        "severity": "moderate",
        "recommended_tests": ["xray", "mri", "joint_fluid_analysis"],
        "breed_risks": {
            "labrador_retriever": 2.0,
            "golden_retriever": 1.8,
            "rottweiler": 1.8,
            "newfoundland": 1.5,
            "staffordshire_terrier": 1.5,
            "boxer": 1.3,
            "akita": 1.3,
            "saint_bernard": 1.3,
        },
    },
    # ---- 38. Laryngeal Paralysis ----
    {
        "id": "laryngeal_paralysis",
        "name_ja": "喉頭麻痺",
        "name_en": "Laryngeal Paralysis (GOLPP)",
        "description_ja": "喉頭の軟骨が適切に開閉しなくなる神経筋疾患です。吸気時の呼吸困難や喘鳴が特徴で、高齢の大型犬に多発します。",
        "description_en": "A neuromuscular disorder where the laryngeal cartilages fail to open and close properly. Characterized by inspiratory dyspnea and stridor, common in older large breeds.",
        "symptoms": [
            "labored_breathing",
            "coughing",
            "exercise_intolerance",
            "wheezing",
            "fainting",
        ],
        "severity": "high",
        "recommended_tests": ["xray", "endoscopy", "thyroid_panel"],
        "breed_risks": {
            "labrador_retriever": 2.0,
            "golden_retriever": 1.8,
            "saint_bernard": 1.5,
            "irish_setter": 1.5,
            "newfoundland": 1.5,
            "great_dane": 1.3,
            "siberian_husky": 1.3,
        },
    },
    # ---- 39. Megaesophagus ----
    {
        "id": "megaesophagus",
        "name_ja": "巨大食道症",
        "name_en": "Megaesophagus",
        "description_ja": "食道の運動機能が低下し食道が拡張する疾患です。食物の逆流（吐出）が特徴で、誤嚥性肺炎のリスクがあります。",
        "description_en": "A condition where the esophagus loses motility and becomes dilated. Characterized by regurgitation and carries risk of aspiration pneumonia.",
        "symptoms": [
            "vomiting",
            "loss_of_appetite",
            "weight_loss",
            "coughing",
            "nasal_discharge",
            "labored_breathing",
        ],
        "severity": "moderate",
        "recommended_tests": [
            "xray",
            "blood_chemistry",
            "acth_stimulation",
            "thyroid_panel",
        ],
        "breed_risks": {
            "german_shepherd": 2.0,
            "irish_setter": 1.8,
            "great_dane": 1.5,
            "greyhound": 1.5,
            "shar_pei": 1.5,
            "miniature_schnauzer": 1.3,
            "newfoundland": 1.3,
        },
    },
    # ---- 40. Von Willebrand Disease ----
    {
        "id": "von_willebrand_disease",
        "name_ja": "フォンヴィレブランド病",
        "name_en": "Von Willebrand Disease (vWD)",
        "description_ja": "犬で最も多い遺伝性出血性疾患です。フォンヴィレブランド因子の異常により出血傾向を示します。",
        "description_en": "The most common hereditary bleeding disorder in dogs. Caused by deficiency or dysfunction of von Willebrand factor, leading to prolonged bleeding.",
        "symptoms": ["pale_gums", "lethargy", "blood_in_stool", "blood_in_urine"],
        "severity": "high",
        "recommended_tests": ["coagulation_panel", "genetic_testing", "cbc"],
        "breed_risks": {
            "doberman": 2.5,
            "scottish_terrier": 2.0,
            "german_shepherd": 1.8,
            "shetland_sheepdog": 1.8,
            "golden_retriever": 1.5,
            "poodle": 1.3,
            "bernese_mountain_dog": 1.3,
        },
    },
    # ---- 41. Immune-Mediated Hemolytic Anemia (IMHA) ----
    {
        "id": "imha",
        "name_ja": "免疫介在性溶血性貧血",
        "name_en": "Immune-Mediated Hemolytic Anemia (IMHA)",
        "description_ja": "自己免疫系が赤血球を破壊する自己免疫疾患です。急速に進行し致死率が高い緊急疾患です。",
        "description_en": "An autoimmune disease where the immune system destroys red blood cells. Progresses rapidly and has a high fatality rate, requiring emergency treatment.",
        "symptoms": [
            "pale_gums",
            "jaundice",
            "lethargy",
            "loss_of_appetite",
            "rapid_breathing",
            "fever",
            "vomiting",
        ],
        "severity": "emergency",
        "recommended_tests": [
            "coombs_test",
            "cbc",
            "blood_chemistry",
            "urinalysis",
            "xray",
        ],
        "breed_risks": {
            "cocker_spaniel": 2.5,
            "springer_spaniel": 1.8,
            "irish_setter": 1.8,
            "poodle": 1.5,
            "old_english_sheepdog": 1.5,
            "miniature_schnauzer": 1.3,
            "bichon_frise": 1.3,
            "maltese": 1.3,
        },
    },
    # ---- 42. Portosystemic Shunt ----
    {
        "id": "portosystemic_shunt",
        "name_ja": "門脈体循環シャント",
        "name_en": "Portosystemic Shunt (PSS / Liver Shunt)",
        "description_ja": "門脈血が肝臓を迂回する異常血管による疾患です。肝臓での解毒が行われず、神経症状や発育不良を引き起こします。",
        "description_en": "A condition caused by abnormal blood vessels that bypass the liver. Prevents hepatic detoxification, leading to neurological symptoms and poor growth.",
        "symptoms": [
            "seizures",
            "disorientation",
            "vomiting",
            "lethargy",
            "loss_of_appetite",
            "weight_loss",
            "excessive_thirst",
            "frequent_urination",
            "circling",
        ],
        "severity": "high",
        "recommended_tests": [
            "bile_acids",
            "blood_chemistry",
            "ultrasound",
            "ct_scan",
            "urinalysis",
        ],
        "breed_risks": {
            "yorkshire_terrier": 2.5,
            "maltese": 2.0,
            "irish_wolfhound": 2.0,
            "havanese": 1.8,
            "miniature_schnauzer": 1.5,
            "pug": 1.3,
            "lhasa_apso": 1.3,
            "shih_tzu": 1.3,
        },
    },
    # ---- 43. Wobbler Syndrome ----
    {
        "id": "wobbler_syndrome",
        "name_ja": "ウォブラー症候群（頸部脊椎不安定症）",
        "name_en": "Wobbler Syndrome (Cervical Spondylomyelopathy)",
        "description_ja": "頸部脊椎の不安定性や変形により脊髄が圧迫される疾患です。ふらつく歩様（ウォブリング）が特徴で、大型犬に多発します。",
        "description_en": "A condition where cervical spinal instability or malformation compresses the spinal cord. Characterized by a wobbly gait, predominantly affecting large breeds.",
        "symptoms": [
            "stiffness",
            "paralysis",
            "reluctance_to_move",
            "muscle_wasting",
            "tremors",
        ],
        "severity": "high",
        "recommended_tests": ["mri", "xray", "ct_scan", "csf_analysis", "emg"],
        "breed_risks": {
            "doberman": 2.5,
            "great_dane": 2.5,
            "rottweiler": 1.5,
            "irish_wolfhound": 1.5,
            "bernese_mountain_dog": 1.3,
            "basset_hound": 1.3,
            "weimaraner": 1.3,
        },
    },
    # ==================================================================
    # Extended hereditary disease entries (matching breeds.py coverage)
    # ==================================================================
    # ---- Orthopedic ----
    {
        "id": "legg_calve_perthes",
        "name_ja": "レッグ・カルベ・ペルテス病",
        "name_en": "Legg-Calvé-Perthes Disease",
        "description_ja": "大腿骨頭への血流障害により壊死が起こる疾患です。小型犬の若齢期に多く見られます。",
        "description_en": "Avascular necrosis of the femoral head due to disrupted blood supply. Most common in young small-breed dogs.",
        "symptoms": ["limping", "reluctance_to_move", "muscle_wasting", "stiffness"],
        "severity": "moderate",
        "recommended_tests": ["xray", "ofa_radiograph"],
        "breed_risks": {
            "yorkshire_terrier": 2.5,
            "poodle_miniature": 2.0,
            "chihuahua": 1.8,
            "west_highland_white_terrier": 2.0,
            "manchester_terrier": 1.8,
        },
    },
    {
        "id": "syringomyelia",
        "name_ja": "脊髄空洞症",
        "name_en": "Syringomyelia (SM)",
        "description_ja": "脊髄内に液体で満たされた空洞が形成される疾患です。キアリ様奇形に関連し、痛みやかゆみを引き起こします。",
        "description_en": "Fluid-filled cavities form within the spinal cord, often associated with Chiari-like malformation, causing pain and phantom scratching.",
        "symptoms": ["itching", "head_tilting", "stiffness", "reluctance_to_move", "seizures"],
        "severity": "high",
        "recommended_tests": ["mri", "emg", "csf_analysis"],
        "breed_risks": {
            "cavalier_king_charles": 3.0,
            "brussels_griffon": 2.0,
            "chihuahua": 1.5,
            "maltese": 1.3,
        },
    },
    {
        "id": "tracheal_collapse",
        "name_ja": "気管虚脱",
        "name_en": "Tracheal Collapse",
        "description_ja": "気管の軟骨環が弱くなり、気管が扁平化する疾患です。呼吸困難やガチョウ様の咳を引き起こします。",
        "description_en": "Weakening of tracheal cartilage rings causes the trachea to flatten, resulting in breathing difficulties and a honking cough.",
        "symptoms": ["coughing", "wheezing", "labored_breathing", "exercise_intolerance"],
        "severity": "moderate",
        "recommended_tests": ["xray", "endoscopy", "ct_scan"],
        "breed_risks": {
            "yorkshire_terrier": 2.5,
            "pomeranian": 2.5,
            "chihuahua": 2.0,
            "toy_poodle": 2.0,
            "shih_tzu": 1.8,
            "maltese": 1.8,
            "pug": 1.5,
            "lhasa_apso": 1.5,
        },
    },
    # ---- Cardiac ----
    {
        "id": "subaortic_stenosis",
        "name_ja": "大動脈弁下狭窄症",
        "name_en": "Subaortic Stenosis (SAS)",
        "description_ja": "大動脈弁の下に線維組織が形成され、左心室からの血流が狭窄する先天性心疾患です。",
        "description_en": "A congenital heart defect where fibrous tissue narrows the outflow from the left ventricle below the aortic valve.",
        "symptoms": ["exercise_intolerance", "fainting", "lethargy", "labored_breathing"],
        "severity": "high",
        "recommended_tests": ["echocardiogram", "ecg", "xray"],
        "breed_risks": {
            "golden_retriever": 2.5,
            "newfoundland": 2.5,
            "rottweiler": 2.0,
            "boxer": 1.8,
            "german_shepherd": 1.5,
            "bull_terrier": 1.5,
        },
    },
    {
        "id": "arvc",
        "name_ja": "ボクサー心筋症",
        "name_en": "Arrhythmogenic Right Ventricular Cardiomyopathy (ARVC)",
        "description_ja": "右心室の心筋が脂肪や線維組織に置換される遺伝性疾患です。不整脈や突然死のリスクがあります。",
        "description_en": "An inherited disease where right ventricular muscle is replaced by fat and fibrous tissue, causing arrhythmias and sudden death risk.",
        "symptoms": ["fainting", "exercise_intolerance", "labored_breathing", "lethargy"],
        "severity": "high",
        "recommended_tests": ["ecg", "echocardiogram", "genetic_testing"],
        "breed_risks": {
            "boxer": 3.0,
            "english_bulldog": 1.5,
        },
    },
    # ---- Eye ----
    {
        "id": "entropion",
        "name_ja": "眼瞼内反症",
        "name_en": "Entropion",
        "description_ja": "まぶたが内側に巻き込む疾患で、まつ毛が角膜を刺激し、痛みや角膜損傷を引き起こします。",
        "description_en": "The eyelid rolls inward, causing eyelashes to irritate the cornea, leading to pain, tearing, and potential corneal damage.",
        "symptoms": ["eye_discharge", "squinting", "redness_in_eyes"],
        "severity": "moderate",
        "recommended_tests": ["cerf_exam", "fluorescein_stain"],
        "breed_risks": {
            "shar_pei": 3.0,
            "chow_chow": 2.5,
            "english_bulldog": 2.0,
            "rottweiler": 1.8,
            "great_dane": 1.5,
            "labrador_retriever": 1.3,
            "saint_bernard": 2.0,
            "bloodhound": 2.0,
        },
    },
    {
        "id": "ectropion",
        "name_ja": "眼瞼外反症",
        "name_en": "Ectropion",
        "description_ja": "まぶたが外側に垂れ下がる疾患で、結膜が露出し、乾燥や感染のリスクが高まります。",
        "description_en": "The eyelid droops outward, exposing the conjunctiva, increasing risk of dryness and infection.",
        "symptoms": ["eye_discharge", "redness_in_eyes", "dry_skin"],
        "severity": "low",
        "recommended_tests": ["cerf_exam"],
        "breed_risks": {
            "bloodhound": 2.5,
            "basset_hound": 2.5,
            "saint_bernard": 2.0,
            "great_dane": 1.8,
            "english_bulldog": 1.5,
            "cocker_spaniel": 1.5,
        },
    },
    {
        "id": "lens_luxation",
        "name_ja": "水晶体脱臼",
        "name_en": "Lens Luxation",
        "description_ja": "水晶体を固定する靭帯が弱くなり、水晶体が正常な位置から脱臼する疾患です。緑内障の原因となります。",
        "description_en": "The zonular fibers holding the lens weaken, allowing the lens to dislocate. Can lead to secondary glaucoma.",
        "symptoms": ["cloudiness_in_eyes", "redness_in_eyes", "squinting", "eye_swelling"],
        "severity": "high",
        "recommended_tests": ["cerf_exam", "tonometry", "genetic_testing"],
        "breed_risks": {
            "jack_russell_terrier": 3.0,
            "miniature_bull_terrier": 2.5,
            "sealyham_terrier": 2.5,
            "wire_fox_terrier": 2.0,
            "tibetan_terrier": 2.0,
            "border_collie": 1.5,
        },
    },
    {
        "id": "corneal_dystrophy",
        "name_ja": "角膜ジストロフィー",
        "name_en": "Corneal Dystrophy",
        "description_ja": "角膜に脂質やカルシウムが沈着する遺伝性疾患です。通常は無痛ですが、重度の場合は視力に影響します。",
        "description_en": "An inherited condition where lipid or calcium deposits form in the cornea. Usually painless but may affect vision in severe cases.",
        "symptoms": ["cloudiness_in_eyes"],
        "severity": "low",
        "recommended_tests": ["cerf_exam", "fluorescein_stain"],
        "breed_risks": {
            "siberian_husky": 2.5,
            "samoyed": 2.0,
            "shetland_sheepdog": 1.8,
            "beagle": 1.5,
            "cavalier_king_charles": 1.5,
            "airedale_terrier": 1.5,
        },
    },
    {
        "id": "retinal_dysplasia",
        "name_ja": "網膜異形成",
        "name_en": "Retinal Dysplasia",
        "description_ja": "網膜の発育異常により、網膜のひだや剥離が生じる疾患です。軽度のものから失明に至る重度のものまであります。",
        "description_en": "Abnormal development of the retina causing folds or detachment. Ranges from mild (retinal folds) to severe (complete detachment and blindness).",
        "symptoms": ["cloudiness_in_eyes", "disorientation"],
        "severity": "moderate",
        "recommended_tests": ["cerf_exam", "genetic_testing"],
        "breed_risks": {
            "labrador_retriever": 2.0,
            "english_springer_spaniel": 2.0,
            "american_cocker_spaniel": 1.8,
            "cavalier_king_charles": 1.5,
            "golden_retriever": 1.3,
        },
    },
    {
        "id": "collie_eye_anomaly",
        "name_ja": "コリーアイ異常",
        "name_en": "Collie Eye Anomaly (CEA)",
        "description_ja": "コリー系犬種に見られる先天性の眼疾患で、脈絡膜の発達不全により視力障害が生じます。",
        "description_en": "A congenital, inherited eye condition in Collie-type breeds. Causes choroidal hypoplasia and can lead to retinal detachment.",
        "symptoms": ["cloudiness_in_eyes", "disorientation"],
        "severity": "moderate",
        "recommended_tests": ["cerf_exam", "genetic_testing"],
        "breed_risks": {
            "collie": 3.0,
            "shetland_sheepdog": 2.5,
            "border_collie": 2.0,
            "australian_shepherd": 1.8,
            "nova_scotia_duck_tolling_retriever": 1.5,
        },
    },
    # ---- Neurological ----
    {
        "id": "pug_encephalitis",
        "name_ja": "パグ脳炎",
        "name_en": "Pug Dog Encephalitis (Necrotizing Meningoencephalitis)",
        "description_ja": "脳の壊死性炎症を引き起こす遺伝性疾患で、パグに特異的です。発作や行動変化が特徴的です。",
        "description_en": "A breed-specific hereditary inflammatory brain disease causing necrotizing meningoencephalitis, seizures, and behavioral changes.",
        "symptoms": ["seizures", "disorientation", "circling", "head_tilting", "lethargy", "tremors"],
        "severity": "emergency",
        "recommended_tests": ["mri", "csf_analysis", "cbc", "blood_chemistry"],
        "breed_risks": {
            "pug": 3.0,
            "maltese": 1.3,
            "chihuahua": 1.3,
        },
    },
    {
        "id": "cerebellar_ataxia",
        "name_ja": "小脳失調症",
        "name_en": "Cerebellar Ataxia",
        "description_ja": "小脳の変性により、運動協調の障害、震え、異常歩行を引き起こします。",
        "description_en": "Degeneration of the cerebellum causing loss of coordination, tremors, and abnormal gait.",
        "symptoms": ["tremors", "disorientation", "head_tilting", "circling", "stiffness"],
        "severity": "high",
        "recommended_tests": ["mri", "genetic_testing", "csf_analysis"],
        "breed_risks": {
            "american_staffordshire_terrier": 2.0,
            "scottish_terrier": 2.0,
            "old_english_sheepdog": 1.8,
            "gordon_setter": 1.8,
        },
    },
    # ---- Gastrointestinal ----
    {
        "id": "epi",
        "name_ja": "外分泌膵機能不全",
        "name_en": "Exocrine Pancreatic Insufficiency (EPI)",
        "description_ja": "膵臓が消化酵素を十分に産生できなくなる疾患です。体重減少と栄養不良が起こります。",
        "description_en": "The pancreas fails to produce sufficient digestive enzymes, causing weight loss, poor nutrient absorption, and voluminous stools.",
        "symptoms": ["weight_loss", "diarrhea", "loss_of_appetite", "bloating"],
        "severity": "moderate",
        "recommended_tests": ["blood_chemistry", "fecal_exam", "ultrasound"],
        "breed_risks": {
            "german_shepherd": 3.0,
            "rough_collie": 2.0,
            "chow_chow": 1.5,
            "cavalier_king_charles": 1.3,
        },
    },
    # ---- Urinary ----
    {
        "id": "familial_nephropathy",
        "name_ja": "家族性腎症",
        "name_en": "Familial Nephropathy",
        "description_ja": "遺伝性の腎疾患で、若齢期に腎機能が進行性に低下します。",
        "description_en": "An inherited kidney disease with progressive loss of renal function, often presenting in young dogs.",
        "symptoms": ["excessive_thirst", "frequent_urination", "weight_loss", "vomiting", "lethargy"],
        "severity": "high",
        "recommended_tests": ["blood_chemistry", "urinalysis", "ultrasound", "genetic_testing"],
        "breed_risks": {
            "english_cocker_spaniel": 3.0,
            "bull_terrier": 2.5,
            "basenji": 2.0,
            "soft_coated_wheaten_terrier": 2.0,
        },
    },
    # ---- Hematologic ----
    {
        "id": "hemolytic_anemia",
        "name_ja": "溶血性貧血",
        "name_en": "Hemolytic Anemia",
        "description_ja": "赤血球が正常より速く破壊される疾患で、貧血、黄疸、虚脱を引き起こします。",
        "description_en": "Red blood cells are destroyed faster than they can be produced, causing anemia, jaundice, and collapse.",
        "symptoms": ["pale_gums", "lethargy", "jaundice", "loss_of_appetite", "rapid_breathing"],
        "severity": "high",
        "recommended_tests": ["cbc", "coombs_test", "blood_chemistry", "urinalysis"],
        "breed_risks": {
            "cocker_spaniel": 2.5,
            "english_springer_spaniel": 2.0,
            "old_english_sheepdog": 1.8,
            "irish_setter": 1.5,
            "miniature_schnauzer": 1.5,
            "poodle": 1.3,
        },
    },
    # ---- Dermatologic ----
    {
        "id": "sebaceous_adenitis",
        "name_ja": "皮脂腺炎",
        "name_en": "Sebaceous Adenitis (SA)",
        "description_ja": "皮脂腺が免疫系により破壊される疾患で、脱毛、乾燥肌、鱗屑を引き起こします。",
        "description_en": "The immune system destroys sebaceous glands, causing hair loss, dry skin, and scaling.",
        "symptoms": ["hair_loss", "dry_skin", "itching", "skin_rashes"],
        "severity": "moderate",
        "recommended_tests": ["skin_biopsy", "skin_scraping"],
        "breed_risks": {
            "standard_poodle": 3.0,
            "akita": 2.5,
            "samoyed": 2.0,
            "vizsla": 1.8,
            "german_shepherd": 1.3,
        },
    },
    {
        "id": "dermatomyositis",
        "name_ja": "皮膚筋炎",
        "name_en": "Dermatomyositis",
        "description_ja": "皮膚と筋肉の炎症を引き起こす遺伝性疾患で、顔面や四肢に脱毛や潰瘍が生じます。",
        "description_en": "An inherited inflammatory disease of skin and muscle, causing hair loss, ulceration, and muscle atrophy on face and extremities.",
        "symptoms": ["hair_loss", "skin_rashes", "muscle_wasting", "stiffness"],
        "severity": "moderate",
        "recommended_tests": ["skin_biopsy", "emg", "genetic_testing"],
        "breed_risks": {
            "shetland_sheepdog": 3.0,
            "collie": 3.0,
            "beauceron": 1.5,
        },
    },
    {
        "id": "alopecia_x",
        "name_ja": "脱毛症X",
        "name_en": "Alopecia X (Black Skin Disease)",
        "description_ja": "原因不明の脱毛症で、主に北方犬種に見られます。体幹部の対称性脱毛と皮膚の色素沈着が特徴です。",
        "description_en": "A pattern hair loss of unknown cause, mainly in Nordic breeds. Characterized by symmetrical trunk alopecia and skin hyperpigmentation.",
        "symptoms": ["hair_loss", "dry_skin"],
        "severity": "low",
        "recommended_tests": ["skin_biopsy", "thyroid_panel", "blood_chemistry"],
        "breed_risks": {
            "pomeranian": 3.0,
            "alaskan_malamute": 2.0,
            "siberian_husky": 1.5,
            "samoyed": 1.5,
            "chow_chow": 1.5,
            "miniature_poodle": 1.3,
        },
    },
]

DISEASE_MAP = {d["id"]: d for d in DISEASES}

# ---------------------------------------------------------------------------
# BREED-SPECIFIC GENETIC TESTS AND SCREENING RECOMMENDATIONS (58 breeds)
# ---------------------------------------------------------------------------

BREED_GENETIC_TESTS = {
    "french_bulldog": {
        "name_ja": "フレンチ・ブルドッグ",
        "name_en": "French Bulldog",
        "dna_tests": [
            "DM (Degenerative Myelopathy - SOD1)",
            "JHC (Juvenile Hereditary Cataracts - HSF4)",
            "CMR1 (Canine Multifocal Retinopathy 1)",
            "HUU (Hyperuricosuria - SLC2A9)",
            "CDDY/CDPA (Chondrodystrophy & Chondrodysplasia - FGF4 retrogene)",
        ],
        "screening_recommendations": [
            "OFA Cardiac Evaluation",
            "OFA Patellar Evaluation",
            "OFA Eye Certification (CERF/CAER)",
            "BOAS Assessment",
            "Spinal Radiographs",
        ],
    },
    "english_bulldog": {
        "name_ja": "イングリッシュ・ブルドッグ",
        "name_en": "English Bulldog",
        "dna_tests": [
            "DM (Degenerative Myelopathy - SOD1)",
            "HUU (Hyperuricosuria - SLC2A9)",
            "CMR1 (Canine Multifocal Retinopathy 1)",
            "Cystinuria (SLC3A1)",
            "HNPK (Hereditary Nasal Parakeratosis - SUV39H2)",
        ],
        "screening_recommendations": [
            "OFA Cardiac Evaluation",
            "OFA Patellar Evaluation",
            "OFA Tracheal Hypoplasia Radiograph",
            "BOAS Assessment",
            "OFA Eye Certification",
        ],
    },
    "pug": {
        "name_ja": "パグ",
        "name_en": "Pug",
        "dna_tests": [
            "PDE (Pug Dog Encephalitis - NME marker panel)",
            "DM (Degenerative Myelopathy - SOD1)",
            "PKD (Pyruvate Kinase Deficiency - PKLR)",
        ],
        "screening_recommendations": [
            "OFA Patellar Evaluation",
            "OFA Hip Evaluation",
            "OFA Eye Certification",
            "BOAS Assessment",
        ],
    },
    "boston_terrier": {
        "name_ja": "ボストン・テリア",
        "name_en": "Boston Terrier",
        "dna_tests": [
            "DM (Degenerative Myelopathy - SOD1)",
            "JHC (Juvenile Hereditary Cataracts - HSF4)",
            "HNPK (Hereditary Nasal Parakeratosis)",
        ],
        "screening_recommendations": [
            "OFA Patellar Evaluation",
            "OFA Eye Certification",
            "BAER Hearing Test",
            "OFA Cardiac Evaluation",
        ],
    },
    "cavalier_king_charles": {
        "name_ja": "キャバリア・キング・チャールズ・スパニエル",
        "name_en": "Cavalier King Charles Spaniel",
        "dna_tests": [
            "EFS (Episodic Falling Syndrome - BCAN)",
            "CC/DE (Curly Coat / Dry Eye Syndrome - FAM83H)",
            "DM (Degenerative Myelopathy - SOD1)",
            "CKCSID (Macrothrombocytopenia - TUBB1)",
        ],
        "screening_recommendations": [
            "Annual Cardiac Auscultation & Echocardiogram (MVD Protocol)",
            "MRI for Syringomyelia/Chiari Malformation",
            "OFA Patellar Evaluation",
            "OFA Eye Certification",
        ],
    },
    "golden_retriever": {
        "name_ja": "ゴールデン・レトリーバー",
        "name_en": "Golden Retriever",
        "dna_tests": [
            "PRA1 (GR_PRA1 - SLC4A3)",
            "PRA2 (GR_PRA2 - TTC8)",
            "ICT (Ichthyosis - PNPLA1)",
            "DM (Degenerative Myelopathy - SOD1)",
            "NCL (Neuronal Ceroid Lipofuscinosis - CLN5)",
            "MD (Muscular Dystrophy - DMD, for males)",
        ],
        "screening_recommendations": [
            "OFA Hip Evaluation",
            "OFA Elbow Evaluation",
            "OFA Cardiac Evaluation",
            "OFA Eye Certification",
            "OFA Thyroid Evaluation",
        ],
    },
    "labrador_retriever": {
        "name_ja": "ラブラドール・レトリーバー",
        "name_en": "Labrador Retriever",
        "dna_tests": [
            "PRA-prcd (Progressive Rod-Cone Degeneration - PRCD)",
            "EIC (Exercise-Induced Collapse - DNM1)",
            "CNM (Centronuclear Myopathy - PTPLA)",
            "HNPK (Hereditary Nasal Parakeratosis - SUV39H2)",
            "DM (Degenerative Myelopathy - SOD1)",
            "SD2 (Skeletal Dysplasia 2 - COL11A2)",
        ],
        "screening_recommendations": [
            "OFA Hip Evaluation",
            "OFA Elbow Evaluation",
            "OFA Eye Certification",
            "OFA Cardiac Evaluation",
        ],
    },
    "german_shepherd": {
        "name_ja": "ジャーマン・シェパード",
        "name_en": "German Shepherd Dog",
        "dna_tests": [
            "DM (Degenerative Myelopathy - SOD1)",
            "MDR1 (Multi-Drug Resistance - ABCB1)",
            "Hemophilia A (Factor VIII)",
        ],
        "screening_recommendations": [
            "OFA Hip Evaluation",
            "OFA Elbow Evaluation",
            "OFA Cardiac Evaluation",
            "DM DNA Test",
            "OFA Temperament Test",
        ],
    },
    "dachshund": {
        "name_ja": "ダックスフンド",
        "name_en": "Dachshund",
        "dna_tests": [
            "PRA-cord1 (Cone-Rod Dystrophy 1 - RPGRIP1)",
            "DM (Degenerative Myelopathy - SOD1)",
            "CDDY/IVDD (Chondrodystrophy - FGF4 retrogene on CFA12)",
            "Lafora Disease (NHLRC1)",
            "NCL (Neuronal Ceroid Lipofuscinosis - TPP1/CLN2)",
        ],
        "screening_recommendations": [
            "OFA Patellar Evaluation",
            "OFA Eye Certification",
            "OFA Cardiac Evaluation",
            "Spinal Radiographs",
        ],
    },
    "beagle": {
        "name_ja": "ビーグル",
        "name_en": "Beagle",
        "dna_tests": [
            "MLS (Musladin-Lueke Syndrome - ADAMTSL2)",
            "FVII Deficiency (Factor VII - F7)",
            "IGS (Imerslund-Grasbeck Syndrome - CUBN)",
        ],
        "screening_recommendations": [
            "OFA Hip Evaluation",
            "OFA Eye Certification",
            "OFA Cardiac Evaluation",
            "OFA Thyroid Evaluation",
        ],
    },
    "boxer": {
        "name_ja": "ボクサー",
        "name_en": "Boxer",
        "dna_tests": [
            "DM (Degenerative Myelopathy - SOD1)",
            "ARVC (Arrhythmogenic Right Ventricular Cardiomyopathy - Striatin gene)",
        ],
        "screening_recommendations": [
            "OFA Cardiac Evaluation (Holter Monitor recommended)",
            "OFA Hip Evaluation",
            "OFA Thyroid Evaluation",
            "OFA Eye Certification",
            "AS (Aortic Stenosis) Echocardiogram Screening",
        ],
    },
    "rottweiler": {
        "name_ja": "ロットワイラー",
        "name_en": "Rottweiler",
        "dna_tests": [
            "JLPP (Juvenile Laryngeal Paralysis and Polyneuropathy - RAB3GAP1)",
            "DM (Degenerative Myelopathy - SOD1)",
        ],
        "screening_recommendations": [
            "OFA Hip Evaluation",
            "OFA Elbow Evaluation",
            "OFA Cardiac Evaluation",
            "OFA Eye Certification",
        ],
    },
    "doberman": {
        "name_ja": "ドーベルマン",
        "name_en": "Doberman Pinscher",
        "dna_tests": [
            "vWD Type 1 (Von Willebrand Disease - VWF)",
            "DM (Degenerative Myelopathy - SOD1)",
            "PHPV (Persistent Hyperplastic Primary Vitreous)",
            "Narcolepsy (HCRTR2)",
        ],
        "screening_recommendations": [
            "Annual DCM Screening (Echocardiogram + Holter Monitor)",
            "OFA Cardiac Evaluation",
            "OFA Hip Evaluation",
            "OFA Thyroid Evaluation",
            "OFA Eye Certification",
        ],
    },
    "great_dane": {
        "name_ja": "グレート・デーン",
        "name_en": "Great Dane",
        "dna_tests": [
            "DM (Degenerative Myelopathy - SOD1)",
        ],
        "screening_recommendations": [
            "OFA Cardiac Evaluation (DCM Screening)",
            "OFA Hip Evaluation",
            "OFA Eye Certification",
            "OFA Thyroid Evaluation",
            "Gastropexy Discussion (GDV Prevention)",
        ],
    },
    "bernese_mountain_dog": {
        "name_ja": "バーニーズ・マウンテン・ドッグ",
        "name_en": "Bernese Mountain Dog",
        "dna_tests": [
            "DM (Degenerative Myelopathy - SOD1A and SOD1B)",
            "vWD Type 1 (Von Willebrand Disease - VWF)",
        ],
        "screening_recommendations": [
            "OFA Hip Evaluation",
            "OFA Elbow Evaluation",
            "OFA Cardiac Evaluation",
            "OFA Eye Certification",
            "Histiocytic Sarcoma Awareness Screening",
        ],
    },
    "siberian_husky": {
        "name_ja": "シベリアン・ハスキー",
        "name_en": "Siberian Husky",
        "dna_tests": [
            "PRA-XL (X-Linked PRA - RPGR)",
            "DINGS (Canine Deafness marker)",
            "DM (Degenerative Myelopathy - SOD1)",
        ],
        "screening_recommendations": [
            "OFA Hip Evaluation",
            "OFA Eye Certification (Annual)",
            "OFA Cardiac Evaluation",
        ],
    },
    "poodle": {
        "name_ja": "プードル",
        "name_en": "Poodle (Standard / Miniature / Toy)",
        "dna_tests": [
            "PRA-prcd (Progressive Rod-Cone Degeneration - PRCD)",
            "vWD Type 1 (Von Willebrand Disease - VWF)",
            "DM (Degenerative Myelopathy - SOD1)",
            "NE (Neonatal Encephalopathy - ATF2)",
        ],
        "screening_recommendations": [
            "OFA Hip Evaluation",
            "OFA Eye Certification",
            "OFA Patellar Evaluation (Miniature/Toy)",
            "SA (Sebaceous Adenitis) Skin Biopsy Screening",
            "OFA Cardiac Evaluation",
        ],
    },
    "yorkshire_terrier": {
        "name_ja": "ヨークシャー・テリア",
        "name_en": "Yorkshire Terrier",
        "dna_tests": [
            "PLL (Primary Lens Luxation - ADAMTS17)",
            "DM (Degenerative Myelopathy - SOD1)",
        ],
        "screening_recommendations": [
            "OFA Patellar Evaluation",
            "OFA Eye Certification",
            "Legg-Calve-Perthes Radiograph Screening",
            "Bile Acids Test (Liver Shunt Screening)",
        ],
    },
    "chihuahua": {
        "name_ja": "チワワ",
        "name_en": "Chihuahua",
        "dna_tests": [
            "DM (Degenerative Myelopathy - SOD1)",
        ],
        "screening_recommendations": [
            "OFA Patellar Evaluation",
            "OFA Cardiac Evaluation",
            "OFA Eye Certification",
            "Molera Assessment",
        ],
    },
    "shih_tzu": {
        "name_ja": "シー・ズー",
        "name_en": "Shih Tzu",
        "dna_tests": [
            "DM (Degenerative Myelopathy - SOD1)",
            "PRA-prcd (Progressive Rod-Cone Degeneration - PRCD)",
            "HNPK (Hereditary Nasal Parakeratosis)",
        ],
        "screening_recommendations": [
            "OFA Eye Certification",
            "OFA Patellar Evaluation",
            "OFA Hip Evaluation",
        ],
    },
    "maltese": {
        "name_ja": "マルチーズ",
        "name_en": "Maltese",
        "dna_tests": [
            "DM (Degenerative Myelopathy - SOD1)",
            "PRA-prcd (Progressive Rod-Cone Degeneration - PRCD)",
        ],
        "screening_recommendations": [
            "OFA Patellar Evaluation",
            "OFA Cardiac Evaluation",
            "Bile Acids Test (Liver Shunt Screening)",
            "OFA Eye Certification",
        ],
    },
    "pomeranian": {
        "name_ja": "ポメラニアン",
        "name_en": "Pomeranian",
        "dna_tests": [
            "DM (Degenerative Myelopathy - SOD1)",
            "PRA-prcd (Progressive Rod-Cone Degeneration - PRCD)",
            "GR-PRA1 linkage (check breeder testing)",
        ],
        "screening_recommendations": [
            "OFA Patellar Evaluation",
            "OFA Cardiac Evaluation",
            "OFA Eye Certification",
            "Alopecia X Awareness Evaluation",
        ],
    },
    "cocker_spaniel": {
        "name_ja": "コッカー・スパニエル",
        "name_en": "Cocker Spaniel (American / English)",
        "dna_tests": [
            "PRA-prcd (Progressive Rod-Cone Degeneration - PRCD)",
            "FN (Familial Nephropathy - COL4A4)",
            "PFK Deficiency (Phosphofructokinase - PFKM)",
            "EIC (Exercise-Induced Collapse - DNM1)",
        ],
        "screening_recommendations": [
            "OFA Eye Certification (Annual)",
            "OFA Hip Evaluation",
            "OFA Patellar Evaluation",
            "OFA Cardiac Evaluation",
            "OFA Thyroid Evaluation",
        ],
    },
    "springer_spaniel": {
        "name_ja": "スプリンガー・スパニエル",
        "name_en": "English Springer Spaniel",
        "dna_tests": [
            "PFK Deficiency (Phosphofructokinase - PFKM)",
            "PRA-cord1 (Cone-Rod Dystrophy - RPGRIP1)",
            "FN (Familial Nephropathy - COL4A4)",
        ],
        "screening_recommendations": [
            "OFA Hip Evaluation",
            "OFA Eye Certification",
            "OFA Cardiac Evaluation",
            "PFK DNA Testing",
        ],
    },
    "border_collie": {
        "name_ja": "ボーダー・コリー",
        "name_en": "Border Collie",
        "dna_tests": [
            "CEA (Collie Eye Anomaly - NHEJ1)",
            "TNS (Trapped Neutrophil Syndrome - VPS13B)",
            "NCL (Neuronal Ceroid Lipofuscinosis - CLN5)",
            "IGS (Imerslund-Grasbeck Syndrome - CUBN)",
            "MDR1 (Multi-Drug Resistance - ABCB1)",
            "DM (Degenerative Myelopathy - SOD1)",
        ],
        "screening_recommendations": [
            "OFA Hip Evaluation",
            "OFA Eye Certification",
            "OFA Cardiac Evaluation",
        ],
    },
    "australian_shepherd": {
        "name_ja": "オーストラリアン・シェパード",
        "name_en": "Australian Shepherd",
        "dna_tests": [
            "CEA (Collie Eye Anomaly - NHEJ1)",
            "MDR1 (Multi-Drug Resistance - ABCB1)",
            "HSF4 (Hereditary Cataracts - HSF4)",
            "PRA-prcd (Progressive Rod-Cone Degeneration - PRCD)",
            "DM (Degenerative Myelopathy - SOD1)",
        ],
        "screening_recommendations": [
            "OFA Hip Evaluation",
            "OFA Elbow Evaluation",
            "OFA Eye Certification",
        ],
    },
    "shetland_sheepdog": {
        "name_ja": "シェットランド・シープドッグ",
        "name_en": "Shetland Sheepdog",
        "dna_tests": [
            "CEA (Collie Eye Anomaly - NHEJ1)",
            "MDR1 (Multi-Drug Resistance - ABCB1)",
            "vWD Type 3 (Von Willebrand Disease - VWF)",
            "DM (Degenerative Myelopathy - SOD1)",
            "DMS (Dermatomyositis - PAN2/MAP3K7CL)",
        ],
        "screening_recommendations": [
            "OFA Hip Evaluation",
            "OFA Eye Certification",
            "OFA Thyroid Evaluation",
        ],
    },
    "corgi": {
        "name_ja": "ウェルシュ・コーギー",
        "name_en": "Pembroke Welsh Corgi",
        "dna_tests": [
            "DM (Degenerative Myelopathy - SOD1)",
            "vWD Type 1 (Von Willebrand Disease - VWF)",
            "EIC (Exercise-Induced Collapse - DNM1)",
            "PRA-rcd3 (Rod-Cone Dysplasia 3 - PDE6A)",
        ],
        "screening_recommendations": [
            "OFA Hip Evaluation",
            "OFA Eye Certification",
            "OFA Cardiac Evaluation",
        ],
    },
    "basset_hound": {
        "name_ja": "バセット・ハウンド",
        "name_en": "Basset Hound",
        "dna_tests": [
            "POAG (Primary Open Angle Glaucoma - ADAMTS10)",
            "Thrombopathia (RASGRP1)",
            "DM (Degenerative Myelopathy - SOD1)",
        ],
        "screening_recommendations": [
            "OFA Eye Certification",
            "OFA Hip Evaluation",
            "OFA Cardiac Evaluation",
            "Platelet Function Screening",
        ],
    },
    "bloodhound": {
        "name_ja": "ブラッドハウンド",
        "name_en": "Bloodhound",
        "dna_tests": [
            "DM (Degenerative Myelopathy - SOD1)",
        ],
        "screening_recommendations": [
            "OFA Hip Evaluation",
            "OFA Elbow Evaluation",
            "OFA Cardiac Evaluation",
            "OFA Eye Certification",
        ],
    },
    "weimaraner": {
        "name_ja": "ワイマラナー",
        "name_en": "Weimaraner",
        "dna_tests": [
            "HUU (Hyperuricosuria - SLC2A9)",
            "DM (Degenerative Myelopathy - SOD1)",
            "SD (Spinal Dysraphism - NKX2-8)",
        ],
        "screening_recommendations": [
            "OFA Hip Evaluation",
            "OFA Eye Certification",
            "OFA Thyroid Evaluation",
            "Hypertrophic Osteodystrophy Awareness",
        ],
    },
    "irish_setter": {
        "name_ja": "アイリッシュ・セッター",
        "name_en": "Irish Setter",
        "dna_tests": [
            "PRA-rcd1 (Rod-Cone Dysplasia 1 - PDE6B)",
            "CLAD (Canine Leukocyte Adhesion Deficiency - ITGB2)",
            "DM (Degenerative Myelopathy - SOD1)",
        ],
        "screening_recommendations": [
            "OFA Hip Evaluation",
            "OFA Eye Certification",
            "OFA Thyroid Evaluation",
            "OFA Cardiac Evaluation",
        ],
    },
    "dalmatian": {
        "name_ja": "ダルメシアン",
        "name_en": "Dalmatian",
        "dna_tests": [
            "HUU (Hyperuricosuria - SLC2A9)",
            "DM (Degenerative Myelopathy - SOD1)",
        ],
        "screening_recommendations": [
            "BAER Hearing Test (Bilateral)",
            "OFA Hip Evaluation",
            "OFA Eye Certification",
            "OFA Cardiac Evaluation",
            "Urinalysis Monitoring for Urate Crystals",
        ],
    },
    "akita": {
        "name_ja": "秋田犬",
        "name_en": "Akita",
        "dna_tests": [
            "DM (Degenerative Myelopathy - SOD1)",
        ],
        "screening_recommendations": [
            "OFA Hip Evaluation",
            "OFA Eye Certification",
            "OFA Thyroid Evaluation",
            "VKH-like Syndrome Awareness (Uveodermatologic)",
        ],
    },
    "shiba_inu": {
        "name_ja": "柴犬",
        "name_en": "Shiba Inu",
        "dna_tests": [
            "GM1 Gangliosidosis (GLB1)",
            "DM (Degenerative Myelopathy - SOD1)",
        ],
        "screening_recommendations": [
            "OFA Patellar Evaluation",
            "OFA Eye Certification",
            "OFA Hip Evaluation",
        ],
    },
    "chow_chow": {
        "name_ja": "チャウチャウ",
        "name_en": "Chow Chow",
        "dna_tests": [
            "DM (Degenerative Myelopathy - SOD1)",
        ],
        "screening_recommendations": [
            "OFA Hip Evaluation",
            "OFA Elbow Evaluation",
            "OFA Eye Certification",
            "OFA Thyroid Evaluation",
        ],
    },
    "shar_pei": {
        "name_ja": "シャー・ペイ",
        "name_en": "Chinese Shar-Pei",
        "dna_tests": [
            "SPAID (Shar-Pei Autoinflammatory Disease - HAS2/MTBP region)",
            "DM (Degenerative Myelopathy - SOD1)",
            "PLL (Primary Lens Luxation - ADAMTS17)",
        ],
        "screening_recommendations": [
            "OFA Hip Evaluation",
            "OFA Elbow Evaluation",
            "OFA Eye Certification",
            "OFA Patellar Evaluation",
            "Shar-Pei Fever Monitoring",
        ],
    },
    "west_highland_terrier": {
        "name_ja": "ウエスト・ハイランド・ホワイト・テリア",
        "name_en": "West Highland White Terrier",
        "dna_tests": [
            "CMO (Craniomandibular Osteopathy marker)",
            "GCT (Globoid Cell Leukodystrophy - GALC)",
            "DM (Degenerative Myelopathy - SOD1)",
            "PKD (Pyruvate Kinase Deficiency - PKLR)",
        ],
        "screening_recommendations": [
            "OFA Patellar Evaluation",
            "OFA Eye Certification",
            "OFA Hip Evaluation",
            "Westie Lung Disease (IPF) Awareness",
        ],
    },
    "scottish_terrier": {
        "name_ja": "スコティッシュ・テリア",
        "name_en": "Scottish Terrier",
        "dna_tests": [
            "vWD Type 3 (Von Willebrand Disease - VWF)",
            "CMO (Craniomandibular Osteopathy marker)",
            "DM (Degenerative Myelopathy - SOD1)",
        ],
        "screening_recommendations": [
            "OFA Patellar Evaluation",
            "OFA Eye Certification",
            "vWD DNA Testing (Pre-Surgical Coagulation Screening)",
        ],
    },
    "bull_terrier": {
        "name_ja": "ブル・テリア",
        "name_en": "Bull Terrier",
        "dna_tests": [
            "PKD (Polycystic Kidney Disease - PKD1)",
            "LAD (Lethal Acrodermatitis - MKLN1)",
            "PLL (Primary Lens Luxation - ADAMTS17)",
        ],
        "screening_recommendations": [
            "OFA Cardiac Evaluation",
            "OFA Patellar Evaluation",
            "UPC Ratio Screening (Kidney Disease)",
            "OFA Eye Certification",
            "BAER Hearing Test",
        ],
    },
    "staffordshire_terrier": {
        "name_ja": "アメリカン・スタッフォードシャー・テリア",
        "name_en": "American Staffordshire Terrier",
        "dna_tests": [
            "NCL (Neuronal Ceroid Lipofuscinosis - CLN6/ARSG)",
            "HC (Hereditary Cataracts - HSF4)",
            "DM (Degenerative Myelopathy - SOD1)",
            "L-2-HGA (L-2-Hydroxyglutaric Aciduria - L2HGDH)",
        ],
        "screening_recommendations": [
            "OFA Hip Evaluation",
            "OFA Cardiac Evaluation",
            "OFA Elbow Evaluation",
            "OFA Eye Certification",
            "OFA Thyroid Evaluation",
        ],
    },
    "pit_bull": {
        "name_ja": "アメリカン・ピット・ブル・テリア",
        "name_en": "American Pit Bull Terrier",
        "dna_tests": [
            "DM (Degenerative Myelopathy - SOD1)",
            "NCL (Neuronal Ceroid Lipofuscinosis)",
        ],
        "screening_recommendations": [
            "OFA Hip Evaluation",
            "OFA Cardiac Evaluation",
            "OFA Eye Certification",
            "OFA Thyroid Evaluation",
        ],
    },
    "miniature_schnauzer": {
        "name_ja": "ミニチュア・シュナウザー",
        "name_en": "Miniature Schnauzer",
        "dna_tests": [
            "MAC (Mycobacterium Avium Complex susceptibility - CARD15/SLC11A1)",
            "PRA Type A (Miniature Schnauzer - PPT1)",
            "DM (Degenerative Myelopathy - SOD1)",
            "Factor VII Deficiency (F7)",
        ],
        "screening_recommendations": [
            "OFA Eye Certification",
            "OFA Cardiac Evaluation",
            "Fasting Lipid Panel (Hyperlipidemia Screening)",
            "Urinalysis (Urolithiasis Screening)",
        ],
    },
    "giant_schnauzer": {
        "name_ja": "ジャイアント・シュナウザー",
        "name_en": "Giant Schnauzer",
        "dna_tests": [
            "DM (Degenerative Myelopathy - SOD1)",
            "Factor VII Deficiency (F7)",
        ],
        "screening_recommendations": [
            "OFA Hip Evaluation",
            "OFA Eye Certification",
            "OFA Thyroid Evaluation",
            "OFA Cardiac Evaluation",
        ],
    },
    "newfoundland": {
        "name_ja": "ニューファンドランド",
        "name_en": "Newfoundland",
        "dna_tests": [
            "Cystinuria Type I (SLC3A1)",
            "DM (Degenerative Myelopathy - SOD1)",
        ],
        "screening_recommendations": [
            "OFA Cardiac Evaluation (Subvalvular Aortic Stenosis Screening)",
            "OFA Hip Evaluation",
            "OFA Elbow Evaluation",
            "OFA Eye Certification",
            "Cystinuria DNA Testing",
        ],
    },
    "saint_bernard": {
        "name_ja": "セント・バーナード",
        "name_en": "Saint Bernard",
        "dna_tests": [
            "DM (Degenerative Myelopathy - SOD1)",
            "Factor XI Deficiency (F11)",
        ],
        "screening_recommendations": [
            "OFA Hip Evaluation",
            "OFA Elbow Evaluation",
            "OFA Cardiac Evaluation",
            "OFA Eye Certification",
            "OFA Thyroid Evaluation",
        ],
    },
    "irish_wolfhound": {
        "name_ja": "アイリッシュ・ウルフハウンド",
        "name_en": "Irish Wolfhound",
        "dna_tests": [
            "DM (Degenerative Myelopathy - SOD1)",
        ],
        "screening_recommendations": [
            "Annual DCM Screening (Echocardiogram)",
            "OFA Cardiac Evaluation",
            "OFA Hip Evaluation",
            "OFA Elbow Evaluation",
            "OFA Eye Certification",
            "Portosystemic Shunt Bile Acids Screening",
            "Osteosarcoma Awareness Monitoring",
        ],
    },
    "scottish_deerhound": {
        "name_ja": "スコティッシュ・ディアハウンド",
        "name_en": "Scottish Deerhound",
        "dna_tests": [
            "Factor VII Deficiency (F7)",
            "DM (Degenerative Myelopathy - SOD1)",
        ],
        "screening_recommendations": [
            "DCM Screening (Echocardiogram)",
            "OFA Cardiac Evaluation",
            "OFA Eye Certification",
            "Osteosarcoma Awareness Monitoring",
        ],
    },
    "bichon_frise": {
        "name_ja": "ビション・フリーゼ",
        "name_en": "Bichon Frise",
        "dna_tests": [
            "DM (Degenerative Myelopathy - SOD1)",
            "PRA-prcd (Progressive Rod-Cone Degeneration - PRCD)",
        ],
        "screening_recommendations": [
            "OFA Patellar Evaluation",
            "OFA Eye Certification",
            "OFA Hip Evaluation",
            "OFA Cardiac Evaluation",
        ],
    },
    "havanese": {
        "name_ja": "ハバニーズ",
        "name_en": "Havanese",
        "dna_tests": [
            "DM (Degenerative Myelopathy - SOD1)",
            "PRA-prcd (Progressive Rod-Cone Degeneration - PRCD)",
            "CDDY (Chondrodysplasia/Chondrodystrophy - FGF4 retrogene)",
        ],
        "screening_recommendations": [
            "OFA Patellar Evaluation",
            "OFA Eye Certification",
            "OFA Hip Evaluation",
            "BAER Hearing Test",
            "Bile Acids Test (Liver Shunt Screening)",
        ],
    },
    "lhasa_apso": {
        "name_ja": "ラサ・アプソ",
        "name_en": "Lhasa Apso",
        "dna_tests": [
            "DM (Degenerative Myelopathy - SOD1)",
            "PRA-prcd (Progressive Rod-Cone Degeneration - PRCD)",
        ],
        "screening_recommendations": [
            "OFA Eye Certification",
            "OFA Patellar Evaluation",
            "OFA Hip Evaluation",
            "Kidney Function Screening",
        ],
    },
    "rhodesian_ridgeback": {
        "name_ja": "ローデシアン・リッジバック",
        "name_en": "Rhodesian Ridgeback",
        "dna_tests": [
            "DM (Degenerative Myelopathy - SOD1)",
            "ENAM (Amelogenesis Imperfecta - ENAM)",
            "JME (Juvenile Myoclonic Epilepsy - DIRAS1)",
        ],
        "screening_recommendations": [
            "OFA Hip Evaluation",
            "OFA Elbow Evaluation",
            "OFA Eye Certification",
            "OFA Thyroid Evaluation",
            "Dermoid Sinus Palpation at Birth",
        ],
    },
    "vizsla": {
        "name_ja": "ビズラ",
        "name_en": "Vizsla",
        "dna_tests": [
            "DM (Degenerative Myelopathy - SOD1)",
            "Cerebellar Ataxia (SNX14 / KCNIP4)",
            "HUU (Hyperuricosuria - SLC2A9)",
        ],
        "screening_recommendations": [
            "OFA Hip Evaluation",
            "OFA Eye Certification",
            "OFA Thyroid Evaluation",
            "OFA Cardiac Evaluation",
        ],
    },
    "whippet": {
        "name_ja": "ウィペット",
        "name_en": "Whippet",
        "dna_tests": [
            "DM (Degenerative Myelopathy - SOD1)",
            "BWMS (Bully Whippet Syndrome - Myostatin / MSTN)",
        ],
        "screening_recommendations": [
            "OFA Eye Certification",
            "OFA Cardiac Evaluation",
            "BAER Hearing Test",
        ],
    },
    "greyhound": {
        "name_ja": "グレーハウンド",
        "name_en": "Greyhound",
        "dna_tests": [
            "DM (Degenerative Myelopathy - SOD1)",
            "PRA (Greyhound-specific variant)",
            "Greyhound Polyneuropathy (NDRG1)",
        ],
        "screening_recommendations": [
            "OFA Eye Certification",
            "OFA Cardiac Evaluation",
            "Greyhound-specific CBC Reference Ranges",
            "OFA Thyroid Evaluation",
        ],
    },
    "italian_greyhound": {
        "name_ja": "イタリアン・グレーハウンド",
        "name_en": "Italian Greyhound",
        "dna_tests": [
            "DM (Degenerative Myelopathy - SOD1)",
            "PRA-prcd (Progressive Rod-Cone Degeneration - PRCD)",
            "PLL (Primary Lens Luxation - ADAMTS17)",
        ],
        "screening_recommendations": [
            "OFA Patellar Evaluation",
            "OFA Eye Certification",
            "OFA Hip Evaluation",
            "OFA Thyroid Evaluation",
            "Dental Assessment (Periodontal Awareness)",
        ],
    },
    "samoyed": {
        "name_ja": "サモエド",
        "name_en": "Samoyed",
        "dna_tests": [
            "PRA-XL (X-Linked PRA - RPGR)",
            "DM (Degenerative Myelopathy - SOD1)",
            "XL-HN (X-Linked Hereditary Nephritis - COL4A5)",
        ],
        "screening_recommendations": [
            "OFA Hip Evaluation",
            "OFA Eye Certification",
            "OFA Cardiac Evaluation",
            "OFA Thyroid Evaluation",
            "UPC Ratio Screening (Hereditary Nephritis)",
        ],
    },
    "old_english_sheepdog": {
        "name_ja": "オールド・イングリッシュ・シープドッグ",
        "name_en": "Old English Sheepdog",
        "dna_tests": [
            "DM (Degenerative Myelopathy - SOD1)",
            "PCD (Primary Ciliary Dyskinesia - CCDC39)",
            "EIC (Exercise-Induced Collapse - DNM1)",
            "MDR1 (Multi-Drug Resistance - ABCB1)",
        ],
        "screening_recommendations": [
            "OFA Hip Evaluation",
            "OFA Eye Certification",
            "OFA Thyroid Evaluation",
            "OFA Cardiac Evaluation",
            "BAER Hearing Test",
        ],
    },
}


# ---------------------------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------------------------


def _jaccard_similarity(set_a, set_b):
    """Calculate Jaccard similarity coefficient between two sets."""
    if not set_a or not set_b:
        return 0.0
    intersection = set_a & set_b
    union = set_a | set_b
    return len(intersection) / len(union)


# ---------------------------------------------------------------------------
# ADVANCED DIAGNOSTIC SCORING ENGINE
# ---------------------------------------------------------------------------
# Uses TF-IDF-inspired symptom weighting, negative evidence, prevalence
# priors, pathognomonic clusters, and Bayesian-calibrated confidence.
# ---------------------------------------------------------------------------

import math as _math

# --- Precompute symptom IDF (inverse document frequency) ---
# Symptoms appearing in few diseases are more diagnostically specific.
# IDF = log(N / df) where N = total diseases, df = # diseases containing symptom


def _build_symptom_idf():
    """Compute IDF weights for all symptoms across the disease database."""
    n_diseases = len(DISEASES)
    doc_freq = {}
    for disease in DISEASES:
        for symptom in disease["symptoms"]:
            doc_freq[symptom] = doc_freq.get(symptom, 0) + 1
    idf = {}
    for symptom, df in doc_freq.items():
        idf[symptom] = _math.log((n_diseases + 1) / (df + 1)) + 1.0
    return idf


_SYMPTOM_IDF = _build_symptom_idf()

# --- Symptom specificity tiers (veterinary clinical knowledge) ---
# Pathognomonic: nearly unique to one disease family
# High: strong diagnostic value
# Moderate: useful but shared across conditions
# Low: non-specific, seen in many diseases

_SYMPTOM_SPECIFICITY = {
    # Pathognomonic / very high specificity
    "bloating": 3.0,
    "blood_in_stool": 2.5,
    "blood_in_urine": 2.5,
    "seizures": 2.5,
    "paralysis": 2.8,
    "jaundice": 2.8,
    "head_tilting": 2.5,
    "circling": 2.5,
    "fainting": 2.5,
    "reverse_sneezing": 2.2,
    "incontinence": 2.2,
    "cloudiness_in_eyes": 2.5,
    "pale_gums": 2.5,
    # High specificity
    "tremors": 2.0,
    "muscle_wasting": 2.0,
    "joint_swelling": 2.0,
    "hot_spots": 2.0,
    "lumps_bumps": 2.0,
    "excessive_drooling": 1.8,
    "straining_to_urinate": 2.0,
    "eye_swelling": 1.8,
    "swollen_lymph_nodes": 2.2,
    "squinting": 1.8,
    # Moderate specificity
    "coughing": 1.2,
    "sneezing": 1.2,
    "nasal_discharge": 1.3,
    "labored_breathing": 1.5,
    "wheezing": 1.5,
    "diarrhea": 1.1,
    "vomiting": 1.0,
    "constipation": 1.5,
    "limping": 1.3,
    "stiffness": 1.3,
    "skin_rashes": 1.3,
    "itching": 1.1,
    "hair_loss": 1.2,
    "dry_skin": 1.3,
    "redness_in_eyes": 1.3,
    "eye_discharge": 1.2,
    "frequent_urination": 1.5,
    "excessive_thirst": 1.5,
    "rapid_breathing": 1.4,
    "exercise_intolerance": 1.5,
    "aggression": 1.5,
    "excessive_licking": 1.3,
    # Low specificity (non-specific signs)
    "lethargy": 0.6,
    "loss_of_appetite": 0.6,
    "fever": 0.8,
    "weight_loss": 0.7,
    "anxiety": 0.8,
    "reluctance_to_move": 0.9,
}

# --- Pathognomonic symptom clusters ---
# Signature combinations that strongly indicate specific diseases.
# Each cluster: (required_symptoms_frozenset, disease_id, boost_factor)
_PATHOGNOMONIC_CLUSTERS = [
    # GDV: bloating + excessive drooling + rapid breathing
    (frozenset({"bloating", "excessive_drooling", "rapid_breathing"}), "gdv_bloat", 2.0),
    (frozenset({"bloating", "excessive_drooling", "pale_gums"}), "gdv_bloat", 2.0),
    # Parvovirus: bloody diarrhea + vomiting + lethargy in young dog
    (frozenset({"blood_in_stool", "vomiting", "diarrhea"}), "canine_parvovirus", 1.8),
    # Distemper: respiratory + neurological combination
    (frozenset({"coughing", "nasal_discharge", "seizures"}), "canine_distemper", 1.8),
    (frozenset({"coughing", "nasal_discharge", "tremors"}), "canine_distemper", 1.7),
    # BOAS: wheezing + reverse sneezing + labored breathing
    (frozenset({"wheezing", "reverse_sneezing", "labored_breathing"}), "brachycephalic_airway_syndrome", 1.8),
    # Epilepsy: seizures + disorientation
    (frozenset({"seizures", "disorientation"}), "epilepsy", 1.7),
    # Vestibular: head tilting + circling + disorientation
    (frozenset({"head_tilting", "circling", "disorientation"}), "vestibular_disease", 2.0),
    (frozenset({"head_tilting", "circling"}), "vestibular_disease", 1.8),
    # Cushing's: excessive thirst + frequent urination + hair loss
    (frozenset({"excessive_thirst", "frequent_urination", "hair_loss"}), "cushings_disease", 1.8),
    # CKD: excessive thirst + frequent urination + weight loss
    (frozenset({"excessive_thirst", "frequent_urination", "weight_loss"}), "chronic_kidney_disease", 1.7),
    # UTI: blood in urine + frequent urination + straining
    (frozenset({"blood_in_urine", "frequent_urination", "straining_to_urinate"}), "urinary_tract_infection", 2.0),
    # Pancreatitis: vomiting + loss of appetite + bloating
    (frozenset({"vomiting", "loss_of_appetite", "bloating"}), "pancreatitis", 1.6),
    # Glaucoma: cloudiness + eye swelling + squinting
    (frozenset({"cloudiness_in_eyes", "eye_swelling", "squinting"}), "glaucoma", 2.0),
    # Lymphoma: swollen lymph nodes + weight loss + lethargy
    (frozenset({"swollen_lymph_nodes", "weight_loss", "lethargy"}), "lymphoma", 1.7),
    # Allergic dermatitis: itching + skin rashes + hot spots
    (frozenset({"itching", "skin_rashes", "hot_spots"}), "allergic_dermatitis", 1.8),
    # IMHA: pale gums + jaundice + lethargy
    (frozenset({"pale_gums", "jaundice", "lethargy"}), "hemolytic_anemia", 2.0),
    # Liver disease: jaundice + vomiting + loss of appetite
    (frozenset({"jaundice", "vomiting", "loss_of_appetite"}), "liver_disease", 1.8),
    # Degenerative myelopathy: paralysis + muscle wasting + stiffness
    (frozenset({"paralysis", "muscle_wasting", "stiffness"}), "degenerative_myelopathy", 1.9),
    # Heart disease: fainting + exercise intolerance + coughing
    (frozenset({"fainting", "exercise_intolerance", "coughing"}), "dcm", 1.7),
    (frozenset({"fainting", "exercise_intolerance", "rapid_breathing"}), "mitral_valve_disease", 1.7),
    # Diabetes: excessive thirst + frequent urination + weight loss + loss_of_appetite
    (
        frozenset({"excessive_thirst", "frequent_urination", "weight_loss", "loss_of_appetite"}),
        "diabetes_mellitus",
        1.9,
    ),
]

# --- Prevalence tiers (prior probability weights) ---
# Common diseases should rank higher when evidence is ambiguous.
_PREVALENCE_PRIOR = {
    "very_common": 1.15,  # seen daily in practice
    "common": 1.08,  # seen weekly
    "uncommon": 0.95,  # seen monthly
    "rare": 0.85,  # seen < 1x/year
}

# --- Age-based disease category multipliers ---
# Generalizable by disease category tags rather than hardcoded IDs.
_AGE_CATEGORY_TAGS = {}
for _d in DISEASES:
    _did = _d["id"]
    _sev = _d["severity"]
    _syms = set(_d["symptoms"])
    tags = set()
    # Infectious diseases (typically affect young)
    if _did in ("canine_parvovirus", "canine_distemper", "kennel_cough", "canine_influenza", "leptospirosis"):
        tags.add("infectious")
    # Congenital / developmental
    if _did in ("hip_dysplasia", "elbow_dysplasia", "patellar_luxation", "portosystemic_shunt", "pda", "cherry_eye"):
        tags.add("congenital")
    # Degenerative / age-related
    if _did in (
        "degenerative_myelopathy",
        "wobbler_syndrome",
        "cataracts",
        "laryngeal_paralysis",
        "vestibular_disease",
        "chronic_kidney_disease",
        "liver_disease",
    ):
        tags.add("degenerative")
    # Neoplastic (cancer)
    if _did in ("hemangiosarcoma", "lymphoma", "osteosarcoma", "mast_cell_tumor", "melanoma"):
        tags.add("neoplastic")
    # Endocrine / metabolic
    if _did in ("hypothyroidism", "cushings_disease", "diabetes_mellitus", "addisons_disease", "pancreatitis", "ibd"):
        tags.add("metabolic")
    # Cardiac
    if _did in ("dcm", "mitral_valve_disease", "pda"):
        tags.add("cardiac")
    # Autoimmune
    if _did in ("hemolytic_anemia", "immune_mediated_thrombocytopenia", "pemphigus", "lupus", "dermatomyositis"):
        tags.add("autoimmune")
    # Neurological
    if "seizures" in _syms or "paralysis" in _syms or "head_tilting" in _syms:
        tags.add("neurological")
    _AGE_CATEGORY_TAGS[_did] = tags

# Age multiplier matrix: {age_bracket: {category_tag: multiplier}}
_AGE_MULTIPLIERS = {
    "puppy": {  # < 1 year
        "infectious": 1.5,
        "congenital": 1.4,
        "autoimmune": 0.8,
        "neoplastic": 0.5,
        "degenerative": 0.4,
        "metabolic": 0.7,
    },
    "young": {  # 1-3 years
        "infectious": 1.2,
        "congenital": 1.3,
        "autoimmune": 1.1,
        "neoplastic": 0.6,
        "degenerative": 0.5,
        "metabolic": 0.8,
    },
    "adult": {  # 4-7 years
        "infectious": 1.0,
        "congenital": 0.8,
        "autoimmune": 1.1,
        "neoplastic": 1.1,
        "degenerative": 0.9,
        "metabolic": 1.3,
        "cardiac": 1.2,
    },
    "senior": {  # 8+ years
        "infectious": 0.9,
        "congenital": 0.6,
        "autoimmune": 1.0,
        "neoplastic": 1.6,
        "degenerative": 1.5,
        "metabolic": 1.3,
        "cardiac": 1.4,
    },
}


def _get_age_bracket(age_years):
    """Map age in years to bracket."""
    if age_years is None:
        return None
    if age_years < 1:
        return "puppy"
    if age_years <= 3:
        return "young"
    if age_years <= 7:
        return "adult"
    return "senior"


def _compute_symptom_weight(symptom_id):
    """Combine IDF and clinical specificity for a symptom."""
    idf = _SYMPTOM_IDF.get(symptom_id, 1.0)
    specificity = _SYMPTOM_SPECIFICITY.get(symptom_id, 1.0)
    return idf * specificity


def _analyze_symptoms(breed_id, symptom_ids, age_years=None, onset=None):
    """
    Advanced diagnostic scoring engine.

    Scoring Components
    ------------------
    1. Weighted Recall: What fraction of user symptoms match the disease,
       weighted by symptom specificity (IDF * clinical weight)?
    2. Coverage: What fraction of the disease's symptoms are present?
       Missing key symptoms penalize.
    3. Pathognomonic Cluster Boost: Signature symptom combinations
       that strongly indicate specific diseases.
    4. Breed Risk Multiplier: Breed-specific predisposition.
    5. Age Factor: Category-based (not hardcoded) age adjustment.
    6. Onset Factor: Time-course match bonus/penalty.
    7. Prevalence Prior: Common diseases get small boost when
       evidence is ambiguous.
    8. Negative Evidence Penalty: Missing high-specificity symptoms
       that are expected for the disease reduce confidence.

    Confidence is calibrated via logistic function to avoid
    artificial capping and provide clinically meaningful percentages.
    """
    input_symptoms = set(symptom_ids)
    if not input_symptoms:
        return []

    # Precompute total weight of user symptoms
    user_symptom_weights = {s: _compute_symptom_weight(s) for s in input_symptoms}
    total_user_weight = sum(user_symptom_weights.values())

    results = []
    age_bracket = _get_age_bracket(age_years)

    for disease in DISEASES:
        disease_symptoms = set(disease["symptoms"])
        matched = input_symptoms & disease_symptoms

        if not matched:
            continue

        # --- 1. Weighted Recall ---
        # How well do the user's symptoms cover this disease, weighted by
        # diagnostic value? High-specificity matches count more.
        matched_weight = sum(user_symptom_weights.get(s, 1.0) for s in matched)
        weighted_recall = matched_weight / total_user_weight if total_user_weight > 0 else 0

        # --- 2. Coverage (sensitivity) ---
        # What fraction of the disease's expected symptoms are present?
        # Weight disease symptoms by their specificity too.
        disease_symptom_weights = {s: _compute_symptom_weight(s) for s in disease_symptoms}
        total_disease_weight = sum(disease_symptom_weights.values())
        covered_weight = sum(disease_symptom_weights.get(s, 1.0) for s in matched)
        coverage = covered_weight / total_disease_weight if total_disease_weight > 0 else 0

        # --- 3. Base score: harmonic mean of weighted recall and coverage ---
        # This balances "does the evidence support this disease?" with
        # "does this disease explain the symptoms?"
        if weighted_recall + coverage > 0:
            base_score = 2.0 * weighted_recall * coverage / (weighted_recall + coverage)
        else:
            base_score = 0.0

        # --- 4. Specificity bonus ---
        # Reward matches on highly specific symptoms (the diagnostic gems)
        specificity_bonus = 0.0
        for s in matched:
            spec = _SYMPTOM_SPECIFICITY.get(s, 1.0)
            if spec >= 2.0:
                specificity_bonus += 0.06  # pathognomonic
            elif spec >= 1.5:
                specificity_bonus += 0.03  # high specificity
        base_score = min(base_score + specificity_bonus, 1.0)

        # --- 5. Pathognomonic cluster boost ---
        cluster_boost = 1.0
        for cluster_symptoms, cluster_disease_id, boost in _PATHOGNOMONIC_CLUSTERS:
            if cluster_disease_id == disease["id"] and cluster_symptoms <= input_symptoms:
                cluster_boost = max(cluster_boost, boost)

        # --- 6. Negative evidence penalty ---
        # If a disease has highly specific symptoms that the user does NOT
        # report, that's evidence against the disease.
        missing = disease_symptoms - input_symptoms
        negative_penalty = 1.0
        n_user = len(input_symptoms)
        if n_user >= 3:
            # Only apply when user has reported enough symptoms to be meaningful
            for s in missing:
                spec = _SYMPTOM_SPECIFICITY.get(s, 1.0)
                if spec >= 2.5:
                    negative_penalty -= 0.06  # missing pathognomonic symptom
                elif spec >= 2.0:
                    negative_penalty -= 0.03  # missing highly specific symptom
            negative_penalty = max(negative_penalty, 0.5)  # floor

        # --- 7. Breed risk multiplier ---
        breed_multiplier = 1.0
        if breed_id:
            breed_multiplier = disease["breed_risks"].get(breed_id, 1.0)

        # --- 8. Severity context weight ---
        # Less aggressive than before: high-severity diseases get a small
        # boost to ensure they appear prominently, but don't overwhelm.
        severity_weight = {
            "emergency": 1.15,
            "high": 1.08,
            "moderate": 1.0,
            "low": 0.95,
        }.get(disease["severity"], 1.0)

        # --- 9. Onset factor ---
        onset_factor = 1.0
        if onset:
            disease_onsets = _DISEASE_ONSET_BY_ID.get(disease["id"])
            if disease_onsets:
                if onset in disease_onsets:
                    onset_factor = 1.2
                else:
                    onset_factor = 0.75

        # --- 10. Age factor (category-based) ---
        age_factor = 1.0
        if age_bracket:
            disease_tags = _AGE_CATEGORY_TAGS.get(disease["id"], set())
            bracket_multipliers = _AGE_MULTIPLIERS.get(age_bracket, {})
            # Use the highest matching multiplier across tags
            tag_factors = [bracket_multipliers.get(tag, 1.0) for tag in disease_tags]
            if tag_factors:
                age_factor = max(tag_factors)

        # --- 11. Prevalence prior ---
        prevalence_tier = disease.get("prevalence_tier", "common")
        prevalence_prior = _PREVALENCE_PRIOR.get(prevalence_tier, 1.0)

        # --- Composite score ---
        composite_score = (
            base_score
            * cluster_boost
            * negative_penalty
            * breed_multiplier
            * severity_weight
            * onset_factor
            * age_factor
            * prevalence_prior
        )

        # --- Confidence calibration ---
        # Use logistic function to map composite_score to clinically
        # meaningful percentage. Steepness and midpoint tuned so:
        #   - composite ~0.1 → ~15% confidence
        #   - composite ~0.3 → ~40% confidence
        #   - composite ~0.5 → ~60% confidence
        #   - composite ~0.8 → ~85% confidence
        #   - composite ~1.0+ → ~92% confidence
        # Never exceeds 95% (veterinary epistemic humility)
        raw_logistic = 1.0 / (1.0 + _math.exp(-6.0 * (composite_score - 0.4)))
        confidence = min(round(raw_logistic * 100, 1), 95.0)

        # Build recommended tests with priority
        rec_tests = []
        for test_id in disease["recommended_tests"]:
            test_info = DIAGNOSTIC_TEST_MAP.get(test_id)
            if test_info:
                rec_tests.append(
                    {
                        "test_id": test_info["id"],
                        "name_ja": test_info["name_ja"],
                        "name_en": test_info["name_en"],
                        "priority": test_info["priority"],
                    }
                )
        rec_tests.sort(key=lambda t: t["priority"])

        results.append(
            {
                "disease_id": disease["id"],
                "name_ja": disease["name_ja"],
                "name_en": disease["name_en"],
                "description_ja": disease.get("description_ja", ""),
                "description_en": disease.get("description_en", ""),
                "severity": disease["severity"],
                "confidence_percent": confidence,
                "composite_score": round(composite_score, 4),
                "breed_risk_multiplier": breed_multiplier,
                "onset_factor": onset_factor,
                "age_factor": age_factor,
                "matched_symptoms": sorted(matched),
                "matched_count": len(matched),
                "total_disease_symptoms": len(disease_symptoms),
                "missing_key_symptoms": sorted(s for s in missing if _SYMPTOM_SPECIFICITY.get(s, 1.0) >= 1.5),
                "recommended_tests": rec_tests,
                # Diagnostic transparency
                "scoring_detail": {
                    "weighted_recall": round(weighted_recall, 3),
                    "coverage": round(coverage, 3),
                    "base_score": round(base_score, 3),
                    "cluster_boost": cluster_boost,
                    "negative_penalty": round(negative_penalty, 3),
                    "specificity_bonus": round(specificity_bonus, 3),
                    "prevalence_prior": prevalence_prior,
                },
            }
        )

    # Sort by composite score descending
    results.sort(key=lambda r: r["composite_score"], reverse=True)
    return results


# ---------------------------------------------------------------------------
# ROUTES
# ---------------------------------------------------------------------------


_SYMPTOM_NAME_CACHE: dict[str, dict[str, dict[str, str]]] = {}


def _get_species_symptom_names(species: str) -> dict[str, dict[str, str]]:
    """Return {symptom_id: {'ja': ..., 'en': ...}} for the given species.

    Horse uses HEALTH_CHECK_ITEMS (id, ja, en) tuples; all other species use
    SYMPTOM_NAMES dicts. Results are cached after first load.
    """
    if species in _SYMPTOM_NAME_CACHE:
        return _SYMPTOM_NAME_CACHE[species]

    names: dict[str, dict[str, str]] = {}
    try:
        if species == "horse":
            try:
                from api.species.equine_diseases import HEALTH_CHECK_ITEMS
            except ImportError:
                from species.equine_diseases import HEALTH_CHECK_ITEMS  # type: ignore
            for _cat, items in HEALTH_CHECK_ITEMS.items():
                for sid, ja_name, en_name in items:
                    names[sid] = {"ja": ja_name, "en": en_name}
        else:
            mod_name = "dog_diseases" if species == "dog" else f"{species}_diseases"
            try:
                mod = importlib.import_module(f"api.species.{mod_name}")
            except ImportError:
                mod = importlib.import_module(f"species.{mod_name}")
            sn = getattr(mod, "SYMPTOM_NAMES", {}) or {}
            for sid, entry in sn.items():
                if isinstance(entry, dict):
                    names[sid] = {"ja": entry.get("ja", sid), "en": entry.get("en", sid)}
    except (ImportError, AttributeError, ValueError, TypeError) as exc:
        logger.warning("Could not load symptom names for species=%s: %s", species, exc)

    _SYMPTOM_NAME_CACHE[species] = names
    return names


@lru_cache(maxsize=2048)
def _humanize_test_id(tid: str) -> str:
    """Convert a snake_case test id to a readable label.

    Preserves entries that already contain Japanese characters or parenthetical
    English glosses (e.g. 'KOH直接鏡検 (KOH Direct Exam)'). For snake_case IDs,
    replaces underscores with spaces and title-cases Latin segments while
    keeping common abbreviations (CBC, PCR, MRI, CT, ECG) uppercase.
    """
    if not tid or not isinstance(tid, str):
        return tid
    # If contains CJK or spaces, leave as-is
    if _CJK_PATTERN.search(tid) or " " in tid:
        return tid
    if "_" not in tid:
        return tid
    parts = tid.split("_")
    out_parts = []
    for p in parts:
        if p.lower() in _KEEP_UPPER_ABBREVIATIONS:
            out_parts.append(p.upper())
        else:
            out_parts.append(p.capitalize())
    return " ".join(out_parts)


def _build_recommended_tests_display(tests, species: str) -> list[dict[str, str]]:
    """Build display list for recommended_tests. Uses humanized labels for
    snake_case IDs. Preserves existing Japanese/mixed labels."""
    if not tests:
        return []
    if isinstance(tests, (list, tuple, set)):
        ids = list(tests)
    else:
        return []
    out: list[dict[str, str]] = []
    for tid in ids:
        if not isinstance(tid, str) or not tid:
            continue
        label = _humanize_test_id(tid)
        out.append({"id": tid, "name_ja": label, "name_en": label})
    return out


def _build_symptoms_display(symptoms, species: str) -> list[dict[str, str]]:
    """Translate a list of symptom IDs into display entries with ja/en names."""
    if not symptoms:
        return []
    if isinstance(symptoms, dict):
        ids = list(symptoms.keys())
    elif isinstance(symptoms, (list, tuple, set)):
        ids = list(symptoms)
    else:
        return []
    name_map = _get_species_symptom_names(species)
    out: list[dict[str, str]] = []
    for sid in ids:
        if not isinstance(sid, str):
            continue
        entry = name_map.get(sid)
        if entry:
            out.append({"id": sid, "name_ja": entry["ja"], "name_en": entry["en"]})
        else:
            # Fallback: humanize the id (e.g. "resp_cough" -> "Resp Cough")
            pretty = sid.replace("_", " ").title()
            out.append({"id": sid, "name_ja": pretty, "name_en": pretty})
    return out


@health_bp.route("/symptoms", methods=["GET"])
def get_symptoms():
    """Return all symptoms, optionally filtered by category."""
    category = request.args.get("category")
    filtered = [s for s in SYMPTOMS if s["category"] == category] if category else SYMPTOMS

    categories = sorted({s["category"] for s in SYMPTOMS})
    return jsonify(
        {
            "total": len(filtered),
            "categories": categories,
            "symptoms": filtered,
        }
    )


@health_bp.route("/onset-options", methods=["GET"])
def get_onset_options():
    """Return available onset (time-course) and age-range options for the UI."""
    return jsonify(
        {
            "onset": {
                "label_ja": "発症時期",
                "label_en": "Onset / Time Course",
                "description_ja": "症状がいつ頃から始まったかを選択してください",
                "description_en": "Select when the symptoms started",
                "options": [
                    {
                        "id": "acute",
                        "label_ja": "急性（24時間以内）",
                        "label_en": "Acute (within 24 hours)",
                        "description_ja": "突然発症した症状",
                        "description_en": "Sudden onset symptoms",
                    },
                    {
                        "id": "subacute",
                        "label_ja": "亜急性（数日〜1週間）",
                        "label_en": "Subacute (days to ~1 week)",
                        "description_ja": "数日かけて徐々に現れた症状",
                        "description_en": "Symptoms developed over several days",
                    },
                    {
                        "id": "chronic",
                        "label_ja": "慢性（2週間以上）",
                        "label_en": "Chronic (2 weeks or more)",
                        "description_ja": "長期間にわたり持続している症状",
                        "description_en": "Persistent symptoms over weeks/months",
                    },
                ],
            },
            "age_range": {
                "label_ja": "年齢",
                "label_en": "Age",
                "description_ja": "動物の年齢を選択してください",
                "description_en": "Select the animal's age range",
                "options": [
                    {
                        "id": "puppy",
                        "label_ja": "子犬（1歳未満）",
                        "label_en": "Puppy (under 1 year)",
                        "age_range": [0, 1],
                    },
                    {
                        "id": "young",
                        "label_ja": "若齢（1〜3歳）",
                        "label_en": "Young (1–3 years)",
                        "age_range": [1, 3],
                    },
                    {
                        "id": "adult",
                        "label_ja": "成犬（3〜7歳）",
                        "label_en": "Adult (3–7 years)",
                        "age_range": [3, 7],
                    },
                    {
                        "id": "senior",
                        "label_ja": "高齢（7歳以上）",
                        "label_en": "Senior (7+ years)",
                        "age_range": [7, 20],
                    },
                ],
            },
        }
    )


@health_bp.route("/diseases", methods=["GET"])
def get_diseases():
    """Return diseases from the full database, optionally filtered by species."""
    species = request.args.get("species", "dog")

    output = []
    if species == "dog" or species is None:
        try:
            from api.species.dog_diseases import DISEASES as _DISEASE_DB
        except ImportError:
            from species.dog_diseases import DISEASES as _DISEASE_DB
        for d in _DISEASE_DB:
            symptoms = d.get("symptoms", set())
            if isinstance(symptoms, set):
                symptoms = sorted(symptoms)
            output.append(
                enrich_disease_content(
                    {
                        "name": d.get("name", ""),
                        "name_ja": d.get("name_ja", ""),
                        "description": d.get("description", ""),
                        "description_ja": d.get("description_ja", ""),
                        "pathophysiology": d.get("pathophysiology", ""),
                        "pathophysiology_ja": d.get("pathophysiology_ja", ""),
                        "causes": d.get("causes", ""),
                        "causes_ja": d.get("causes_ja", ""),
                        "prevention": d.get("prevention", ""),
                        "prevention_ja": d.get("prevention_ja", ""),
                        "treatment": d.get("treatment", ""),
                        "treatment_ja": d.get("treatment_ja", ""),
                        "prognosis": d.get("prognosis", ""),
                        "prognosis_ja": d.get("prognosis_ja", ""),
                        "severity": d.get("urgency", d.get("severity", "")),
                        "symptoms": symptoms,
                        "symptoms_display": _build_symptoms_display(symptoms, "dog"),
                        "recommended_tests_display": _build_recommended_tests_display(
                            d.get("recommended_tests") or [], "dog"
                        ),
                    },
                    "dog",
                )
            )
    elif species == "horse":
        try:
            from api.species.equine_diseases import DISEASE_DATABASE
        except ImportError:
            from species.equine_diseases import DISEASE_DATABASE

        def _ga(obj, attr, default=""):
            return getattr(obj, attr, default) if not isinstance(obj, dict) else obj.get(attr, default)

        for d in DISEASE_DATABASE:
            findings = _ga(d, "associated_findings", [])
            exams = _ga(d, "recommended_exams", []) or []
            # Horse uses (priority, ja, en) tuples; convert to display list
            exams_display = []
            exams_flat = []
            for item in exams:
                if isinstance(item, tuple) and len(item) >= 3:
                    _prio, ja_name, en_name = item[0], item[1], item[2]
                    exams_display.append({"id": en_name, "name_ja": ja_name, "name_en": en_name})
                    exams_flat.append(en_name)
                elif isinstance(item, str):
                    exams_display.append({"id": item, "name_ja": item, "name_en": item})
                    exams_flat.append(item)
            output.append(
                enrich_disease_content(
                    {
                        "name": _ga(d, "name_en"),
                        "name_ja": _ga(d, "name_ja"),
                        "description": _ga(d, "clinical_signs_detail"),
                        "description_ja": _ga(d, "description_ja"),
                        "pathophysiology": "",
                        "pathophysiology_ja": _ga(d, "pathophysiology"),
                        "causes": "",
                        "causes_ja": _ga(d, "etiology") or _ga(d, "risk_factors"),
                        "prevention": "",
                        "prevention_ja": _ga(d, "prevention"),
                        "treatment": "",
                        "treatment_ja": _ga(d, "treatment_protocol") or _ga(d, "general_management"),
                        "prognosis": "",
                        "prognosis_ja": _ga(d, "prognosis"),
                        "severity": _ga(d, "severity"),
                        "symptoms": findings,
                        "symptoms_display": _build_symptoms_display(findings, "horse"),
                        "recommended_tests": exams_flat,
                        "recommended_tests_display": exams_display,
                    },
                    "horse",
                )
            )
    else:
        import importlib

        try:
            mod = importlib.import_module(f"api.species.{species}_diseases")
        except ImportError:
            mod = importlib.import_module(f"species.{species}_diseases")
        diseases = getattr(mod, "DISEASES", [])
        for d in diseases:
            symptoms = d.get("symptoms", [])
            if isinstance(symptoms, set):
                symptoms = sorted(symptoms)
            rec_tests = d.get("recommended_tests", [])
            if isinstance(rec_tests, set):
                rec_tests = sorted(rec_tests)
            output.append(
                enrich_disease_content(
                    {
                        "name": d.get("name", d.get("name_en", "")),
                        "name_ja": d.get("name_ja", ""),
                        "description": d.get("description", d.get("description_en", "")),
                        "description_ja": d.get("description_ja", ""),
                        "pathophysiology": d.get("pathophysiology", d.get("pathophysiology_en", "")),
                        "pathophysiology_ja": d.get("pathophysiology_ja", ""),
                        "causes": d.get("causes", d.get("causes_en", "")),
                        "causes_ja": d.get("causes_ja", ""),
                        "prevention": d.get("prevention", d.get("prevention_en", "")),
                        "prevention_ja": d.get("prevention_ja", ""),
                        "treatment": d.get("treatment", d.get("treatment_en", "")),
                        "treatment_ja": d.get("treatment_ja", ""),
                        "prognosis": d.get("prognosis", d.get("prognosis_en", "")),
                        "prognosis_ja": d.get("prognosis_ja", ""),
                        "severity": d.get("urgency", d.get("severity", "")),
                        "symptoms": symptoms,
                        "symptoms_display": _build_symptoms_display(symptoms, species),
                        "recommended_tests": rec_tests,
                        "recommended_tests_display": _build_recommended_tests_display(rec_tests, species),
                    },
                    species,
                )
            )

    # Inject hiragana reading for あいうえお sorting
    for item in output:
        name_ja = item.get("name_ja", "")
        if name_ja and name_ja in _NAME_JA_READINGS:
            item["name_ja_sort"] = _NAME_JA_READINGS[name_ja]

    return jsonify(
        {
            "total": len(output),
            "diseases": output,
        }
    )


@health_bp.route("/disease-quality-report", methods=["GET"])
def disease_quality_report():
    """Return per-species disease content completeness summary."""
    species = request.args.get("species", "dog")
    base = get_diseases().get_json()
    diseases = base.get("diseases", [])
    total = len(diseases)
    avg = round(sum(float(d.get("completeness_score", 0)) for d in diseases) / total, 1) if total else 0.0
    with_missing = [d for d in diseases if d.get("missing_fields")]
    top_missing = {}
    for d in with_missing:
        for f in d.get("missing_fields", []):
            top_missing[f] = top_missing.get(f, 0) + 1
    return jsonify(
        {
            "species": species,
            "total_diseases": total,
            "average_completeness": avg,
            "diseases_with_missing_fields": len(with_missing),
            "missing_field_counts": dict(sorted(top_missing.items(), key=lambda x: x[1], reverse=True)),
        }
    )


@health_bp.route("/analyze", methods=["POST"])
def analyze():
    """
    Accept symptoms and return matched diseases.

    Request JSON:
    {
        "breed_id": "french_bulldog",    (optional)
        "symptoms": ["coughing", "labored_breathing", ...],
        "age_years": 3                    (optional)
    }
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    symptom_ids = data.get("symptoms", [])
    if not symptom_ids or not isinstance(symptom_ids, list):
        return jsonify({"error": "symptoms must be a non-empty list"}), 400

    # Validate symptom IDs
    invalid = [s for s in symptom_ids if s not in SYMPTOM_IDS]
    if invalid:
        return (
            jsonify(
                {
                    "error": "Unknown symptom IDs",
                    "invalid_symptoms": invalid,
                    "valid_symptoms": sorted(SYMPTOM_IDS),
                }
            ),
            400,
        )

    raw_breed_id = data.get("breed_id", "")
    # Normalize breed_id: strip leading FCI number prefix (e.g. "101_french_bulldog" → "french_bulldog")
    breed_id = raw_breed_id
    if breed_id and "_" in breed_id:
        parts = breed_id.split("_", 1)
        # If first part looks like a number (FCI prefix), strip it
        if parts[0].rstrip("d").isdigit():
            breed_id = parts[1]
    age_years = data.get("age_years")

    if age_years is not None:
        try:
            age_years = float(age_years)
        except (ValueError, TypeError):
            return jsonify({"error": "age_years must be a number"}), 400

    # Onset (time-course) parameter
    onset = data.get("onset")
    if onset and onset not in ("acute", "subacute", "chronic"):
        return jsonify({"error": "onset must be 'acute', 'subacute', or 'chronic'"}), 400

    # Run analysis
    matches = _analyze_symptoms(breed_id, symptom_ids, age_years, onset=onset)

    # Build genetic test info if breed is known
    genetic_info = None
    if breed_id and breed_id in BREED_GENETIC_TESTS:
        breed_genetics = BREED_GENETIC_TESTS[breed_id]
        genetic_info = {
            "breed_name_ja": breed_genetics["name_ja"],
            "breed_name_en": breed_genetics["name_en"],
            "recommended_dna_tests": breed_genetics["dna_tests"],
            "screening_recommendations": breed_genetics["screening_recommendations"],
        }

    # Emergency flag
    has_emergency = any(m["severity"] == "emergency" for m in matches[:5])

    # Collect all unique recommended tests across top matches (up to 10)
    all_test_ids_seen = set()
    priority_tests = []
    for match in matches[:10]:
        for test in match["recommended_tests"]:
            if test["test_id"] not in all_test_ids_seen:
                all_test_ids_seen.add(test["test_id"])
                priority_tests.append(test)
    priority_tests.sort(key=lambda t: t["priority"])

    return jsonify(
        {
            "input": {
                "breed_id": breed_id,
                "symptoms": symptom_ids,
                "age_years": age_years,
                "onset": onset,
            },
            "emergency_flag": has_emergency,
            "emergency_message": (
                "緊急度の高い所見です。安定化と緊急の検査を優先してください。"
                " / EMERGENCY: prioritize stabilization and urgent workup."
                if has_emergency
                else None
            ),
            "total_matches": len(matches),
            "top_matches": matches[:10],
            "consolidated_priority_tests": priority_tests,
            "breed_genetic_info": genetic_info,
            "disclaimer": (
                "この結果は参考情報であり、獣医師による診察の代替ではありません。"
                "疾患データ（症状・リスク因子・頻度・治療法・予後・予防策）は"
                "獣医師法に触れない範囲で一般的な参考情報として記載しています。"
                " / This is for reference only and does not replace professional "
                "veterinary consultation. Disease data (symptoms, risk factors, "
                "frequency, treatment, prognosis, prevention) is presented as "
                "general reference information within the scope permitted by the "
                "Veterinary Practice Act."
            ),
            "supervised_by": {
                "name_ja": "上手 健太郎",
                "name_en": "Kentaro Kamide, DVM",
                "clinic_ja": "南相馬アニマルクリニック",
                "clinic_en": "Minamisoma Animal Clinic",
                "url": "https://www.minamisoma-vet.com/",
            },
        }
    )


@health_bp.route("/breed-risks/<breed_id>", methods=["GET"])
def get_breed_risks(breed_id):
    """Return breed-specific disease risks and genetic tests for a given breed."""
    # Find all diseases where this breed has elevated risk
    breed_diseases = []
    for disease in DISEASES:
        multiplier = disease["breed_risks"].get(breed_id)
        if multiplier is not None:
            breed_diseases.append(
                {
                    "disease_id": disease["id"],
                    "name_ja": disease["name_ja"],
                    "name_en": disease["name_en"],
                    "severity": disease["severity"],
                    "risk_multiplier": multiplier,
                    "symptoms": disease["symptoms"],
                    "recommended_tests": disease["recommended_tests"],
                }
            )

    # Sort by risk multiplier descending
    breed_diseases.sort(key=lambda d: d["risk_multiplier"], reverse=True)

    # Get genetic tests
    genetic_data = BREED_GENETIC_TESTS.get(breed_id)
    if not genetic_data and not breed_diseases:
        return (
            jsonify(
                {
                    "error": f"No data found for breed_id: {breed_id}",
                    "available_breeds": sorted(BREED_GENETIC_TESTS.keys()),
                }
            ),
            404,
        )

    response = {
        "breed_id": breed_id,
        "total_elevated_risks": len(breed_diseases),
        "disease_risks": breed_diseases,
    }

    if genetic_data:
        response["breed_name_ja"] = genetic_data["name_ja"]
        response["breed_name_en"] = genetic_data["name_en"]
        response["dna_tests"] = genetic_data["dna_tests"]
        response["screening_recommendations"] = genetic_data["screening_recommendations"]
    else:
        response["breed_name_ja"] = None
        response["breed_name_en"] = None
        response["dna_tests"] = []
        response["screening_recommendations"] = []

    return jsonify(response)
