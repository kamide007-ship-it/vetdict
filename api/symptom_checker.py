"""
Symptom Checker Module for VetDict.

Maps dog symptoms to suspected diseases and recommended diagnostic tests.
Provides structured analysis output with severity assessment, Japanese
localization, and prioritized test recommendations.
"""

from __future__ import annotations

from typing import Any

from api.species.dog_diseases import (
    _ANY_LIMPING as _ANY_LIMPING_MODULE,
)
from api.species.dog_diseases import (
    _DISEASE_PREVALENCE as _DISEASE_PREVALENCE_MODULE,
)
from api.species.dog_diseases import (
    _PREVALENCE_MULTIPLIER as _PREVALENCE_MULTIPLIER_MODULE,
)

# ---------------------------------------------------------------------------
# Import dog disease data from the species module
# ---------------------------------------------------------------------------
from api.species.dog_diseases import (
    DISEASES as _DISEASE_DB_MODULE,
)
from api.species.dog_diseases import (
    SYMPTOM_NAMES as _SYMPTOM_NAMES_MODULE,
)
from api.species.dog_diseases import (
    TEST_DB as _TEST_DB_MODULE,
)
from api.species.dog_diseases import (
    VALID_SYMPTOMS as VALID_SYMPTOMS_MODULE,
)

# ---------------------------------------------------------------------------
# Symptom ID catalogue (for reference / validation)
# ---------------------------------------------------------------------------
# Symptom ID catalogue imported from dog_diseases module
VALID_SYMPTOMS = VALID_SYMPTOMS_MODULE

# Symptom ID -> bilingual name mapping (used for display in results)
# Symptom names imported from dog_diseases module
_SYMPTOM_NAMES = _SYMPTOM_NAMES_MODULE

# Convenience group used by diseases that accept *any* limping symptom.
_ANY_LIMPING = _ANY_LIMPING_MODULE

# ---------------------------------------------------------------------------
# Extended Health Check Items (10 categories, 60+ items)
# Used by the vet visit documentation system. Each Japanese checkbox item
# maps to one or more English symptom IDs for disease matching.
# ---------------------------------------------------------------------------
HEALTH_CHECK_CATEGORIES: dict[str, list[dict[str, Any]]] = {
    "general": {
        "label": "全般状態",
        "label_en": "General Condition",
        "icon": "thermometer",
        "items": [
            {"ja": "元気がない", "en": "Lethargy", "symptom_ids": ["lethargy"]},
            {"ja": "ぐったりしている", "en": "Collapse / Severe lethargy", "symptom_ids": ["lethargy"]},
            {"ja": "普段通り", "en": "Normal", "symptom_ids": []},
            {"ja": "興奮している", "en": "Excited / Agitated", "symptom_ids": ["anxiety"]},
            {"ja": "落ち着きがない", "en": "Restless", "symptom_ids": ["anxiety"]},
        ],
    },
    "appetite": {
        "label": "食欲・飲水",
        "label_en": "Appetite & Drinking",
        "icon": "utensils",
        "items": [
            {"ja": "食欲なし", "en": "No appetite", "symptom_ids": ["appetite_loss"]},
            {"ja": "食欲低下", "en": "Decreased appetite", "symptom_ids": ["appetite_loss"]},
            {"ja": "食欲旺盛", "en": "Increased appetite", "symptom_ids": ["appetite_increase"]},
            {"ja": "食欲普通", "en": "Normal appetite", "symptom_ids": []},
            {"ja": "水を飲まない", "en": "Not drinking", "symptom_ids": ["appetite_loss"]},
            {"ja": "多飲（水をよく飲む）", "en": "Excessive drinking", "symptom_ids": ["excessive_thirst"]},
            {"ja": "飲水普通", "en": "Normal drinking", "symptom_ids": []},
        ],
    },
    "digestive": {
        "label": "消化器症状",
        "label_en": "Digestive",
        "icon": "stomach",
        "items": [
            {"ja": "嘔吐", "en": "Vomiting", "symptom_ids": ["vomiting"]},
            {"ja": "吐き気（よだれが多い）", "en": "Nausea / Drooling", "symptom_ids": ["vomiting"]},
            {"ja": "下痢", "en": "Diarrhea", "symptom_ids": ["diarrhea"]},
            {"ja": "軟便", "en": "Soft stool", "symptom_ids": ["diarrhea"]},
            {"ja": "便秘", "en": "Constipation", "symptom_ids": ["constipation"]},
            {"ja": "血便", "en": "Bloody stool", "symptom_ids": ["bloody_stool"]},
            {"ja": "黒色便", "en": "Dark/Tarry stool", "symptom_ids": ["bloody_stool"]},
            {"ja": "腹痛（触ると痛がる）", "en": "Abdominal pain", "symptom_ids": ["bloated_abdomen", "pain_on_touch"]},
            {"ja": "腹部膨満（お腹が張っている）", "en": "Bloated abdomen", "symptom_ids": ["bloated_abdomen"]},
            {"ja": "ゲップ・しゃっくり", "en": "Belching / Hiccup", "symptom_ids": ["excessive_gas"]},
        ],
    },
    "respiratory": {
        "label": "呼吸器症状",
        "label_en": "Respiratory",
        "icon": "lungs",
        "items": [
            {"ja": "咳", "en": "Cough", "symptom_ids": ["coughing"]},
            {"ja": "くしゃみ", "en": "Sneezing", "symptom_ids": ["sneezing"]},
            {"ja": "鼻水", "en": "Nasal discharge", "symptom_ids": ["nasal_discharge"]},
            {"ja": "鼻血", "en": "Nosebleed", "symptom_ids": ["nasal_discharge"]},
            {"ja": "鼻づまり", "en": "Nasal congestion", "symptom_ids": ["nasal_discharge", "snoring"]},
            {"ja": "呼吸困難", "en": "Difficulty breathing", "symptom_ids": ["difficulty_breathing"]},
            {"ja": "喘鳴（ゼーゼー音）", "en": "Wheezing", "symptom_ids": ["difficulty_breathing", "snoring"]},
            {
                "ja": "開口呼吸",
                "en": "Open-mouth breathing",
                "symptom_ids": ["difficulty_breathing", "excessive_panting"],
            },
            {"ja": "呼吸が速い", "en": "Rapid breathing", "symptom_ids": ["rapid_breathing"]},
            {"ja": "呼吸が遅い", "en": "Slow breathing", "symptom_ids": ["difficulty_breathing"]},
        ],
    },
    "urinary": {
        "label": "泌尿器症状",
        "label_en": "Urinary",
        "icon": "droplet",
        "items": [
            {"ja": "頻尿", "en": "Frequent urination", "symptom_ids": ["excessive_urination"]},
            {"ja": "排尿困難", "en": "Difficulty urinating", "symptom_ids": ["straining_urinate"]},
            {"ja": "血尿", "en": "Blood in urine", "symptom_ids": ["blood_urine"]},
            {"ja": "尿量減少", "en": "Decreased urine", "symptom_ids": ["straining_urinate"]},
            {"ja": "尿が出ない", "en": "Urinary blockage", "symptom_ids": ["straining_urinate"]},
            {"ja": "尿漏れ", "en": "Incontinence", "symptom_ids": ["incontinence"]},
            {"ja": "尿の色が濃い", "en": "Dark urine", "symptom_ids": ["blood_urine"]},
            {"ja": "尿の臭いが強い", "en": "Strong urine odor", "symptom_ids": ["straining_urinate"]},
        ],
    },
    "skin": {
        "label": "皮膚症状",
        "label_en": "Skin & Coat",
        "icon": "bandage",
        "items": [
            {"ja": "かゆみ（掻く・舐める）", "en": "Itching / Licking", "symptom_ids": ["itching"]},
            {"ja": "脱毛", "en": "Hair loss", "symptom_ids": ["hair_loss"]},
            {"ja": "発疹", "en": "Rash", "symptom_ids": ["skin_redness"]},
            {"ja": "腫れ", "en": "Swelling", "symptom_ids": ["lumps"]},
            {"ja": "ただれ", "en": "Sores", "symptom_ids": ["hot_spots"]},
            {"ja": "フケ", "en": "Dandruff", "symptom_ids": ["dry_skin"]},
            {"ja": "赤み", "en": "Redness", "symptom_ids": ["skin_redness"]},
            {"ja": "膿", "en": "Pus / Discharge", "symptom_ids": ["hot_spots"]},
            {"ja": "湿疹", "en": "Eczema", "symptom_ids": ["skin_redness", "itching"]},
            {"ja": "乾燥", "en": "Dry skin", "symptom_ids": ["dry_skin"]},
        ],
    },
    "eyes_ears": {
        "label": "眼・耳・鼻症状",
        "label_en": "Eyes & Ears",
        "icon": "eye",
        "items": [
            {"ja": "目やに", "en": "Eye discharge", "symptom_ids": ["eye_discharge"]},
            {"ja": "充血", "en": "Eye redness", "symptom_ids": ["eye_redness"]},
            {"ja": "涙が多い", "en": "Excessive tearing", "symptom_ids": ["eye_discharge"]},
            {"ja": "目が開かない", "en": "Squinting", "symptom_ids": ["squinting"]},
            {"ja": "目の腫れ", "en": "Eye swelling", "symptom_ids": ["eye_redness"]},
            {"ja": "耳を痒がる", "en": "Ear scratching", "symptom_ids": ["ear_scratching"]},
            {"ja": "耳垂れ", "en": "Ear discharge", "symptom_ids": ["ear_odor"]},
            {"ja": "耳の臭い", "en": "Ear odor", "symptom_ids": ["ear_odor"]},
            {"ja": "頭を振る", "en": "Head shaking", "symptom_ids": ["ear_scratching", "head_tilting"]},
            {"ja": "耳が赤い", "en": "Ear redness", "symptom_ids": ["ear_scratching"]},
        ],
    },
    "musculoskeletal": {
        "label": "運動器症状",
        "label_en": "Musculoskeletal",
        "icon": "bone",
        "items": [
            {"ja": "びっこ（片足を引く）", "en": "Limping", "symptom_ids": ["limping_fl"]},
            {"ja": "足を引きずる", "en": "Dragging leg", "symptom_ids": ["limping_rl"]},
            {"ja": "歩行困難", "en": "Difficulty walking", "symptom_ids": ["reluctance_move"]},
            {"ja": "立てない", "en": "Cannot stand", "symptom_ids": ["reluctance_move", "pain_on_touch"]},
            {"ja": "震え", "en": "Trembling", "symptom_ids": ["pain_on_touch"]},
            {"ja": "ふらつき", "en": "Wobbling / Ataxia", "symptom_ids": ["circling"]},
            {"ja": "関節の腫れ", "en": "Joint swelling", "symptom_ids": ["swollen_joints"]},
            {"ja": "関節の痛み", "en": "Joint pain", "symptom_ids": ["stiffness", "pain_on_touch"]},
            {"ja": "階段を嫌がる", "en": "Avoids stairs", "symptom_ids": ["stiffness", "reluctance_move"]},
        ],
    },
    "neurological": {
        "label": "神経症状",
        "label_en": "Neurological",
        "icon": "brain",
        "items": [
            {"ja": "けいれん", "en": "Seizures", "symptom_ids": ["seizures"]},
            {"ja": "意識障害", "en": "Consciousness disorder", "symptom_ids": ["seizures"]},
            {"ja": "麻痺", "en": "Paralysis", "symptom_ids": ["reluctance_move"]},
            {"ja": "旋回運動", "en": "Circling", "symptom_ids": ["circling"]},
            {"ja": "首を傾ける", "en": "Head tilt", "symptom_ids": ["head_tilting"]},
            {"ja": "眼振（目が揺れる）", "en": "Nystagmus", "symptom_ids": ["head_tilting"]},
            {"ja": "失禁", "en": "Incontinence", "symptom_ids": ["incontinence"]},
            {"ja": "反応が鈍い", "en": "Decreased response", "symptom_ids": ["lethargy"]},
        ],
    },
    "other": {
        "label": "その他",
        "label_en": "Other",
        "icon": "pin",
        "items": [
            {"ja": "発熱（体が熱い）", "en": "Fever", "symptom_ids": ["fever"]},
            {"ja": "出血", "en": "Bleeding", "symptom_ids": []},
            {"ja": "腫瘤（しこり）", "en": "Lump / Mass", "symptom_ids": ["lumps"]},
            {"ja": "痛がる", "en": "Pain", "symptom_ids": ["pain_on_touch"]},
            {"ja": "異物誤飲の疑い", "en": "Foreign body ingestion", "symptom_ids": ["vomiting"]},
            {"ja": "発作", "en": "Seizure episode", "symptom_ids": ["seizures"]},
            {"ja": "異常行動", "en": "Abnormal behavior", "symptom_ids": ["aggression_change"]},
            {"ja": "鳴き声の異常", "en": "Abnormal vocalization", "symptom_ids": ["pain_on_touch"]},
            {"ja": "体重減少", "en": "Weight loss", "symptom_ids": ["weight_loss"]},
            {"ja": "体重増加", "en": "Weight gain", "symptom_ids": ["weight_gain"]},
        ],
    },
}

# Keywords that indicate abnormal/alert status (for red highlighting in UI/PDF)
ABNORMAL_KEYWORDS: list[str] = [
    "嘔吐",
    "下痢",
    "血便",
    "血尿",
    "出血",
    "けいれん",
    "呼吸困難",
    "意識障害",
    "麻痺",
    "発熱",
    "異物誤飲",
    "ぐったり",
    "立てない",
    "開口呼吸",
    "尿が出ない",
    "腹痛",
    "痛がる",
    "黒色便",
    "鼻血",
]


def map_health_checks_to_symptoms(health_checks: dict[str, list[str]]) -> list[str]:
    """Convert Japanese health check selections to English symptom IDs.

    Args:
        health_checks: Dict of {category_key: [Japanese item labels]}
            e.g. {"digestive": ["嘔吐", "下痢"], "general": ["元気がない"]}

    Returns:
        Deduplicated list of English symptom IDs for analyze_symptoms().
    """
    symptom_set: set[str] = set()

    for cat_key, checked_items in health_checks.items():
        cat_data = HEALTH_CHECK_CATEGORIES.get(cat_key, {})
        items = cat_data.get("items", [])

        # Build a lookup by Japanese label
        ja_to_ids = {item["ja"]: item["symptom_ids"] for item in items}

        for checked in checked_items:
            ids = ja_to_ids.get(checked, [])
            symptom_set.update(ids)

    return sorted(symptom_set)


# ---------------------------------------------------------------------------
# Onset / Time-course & Age-predisposition tables
# ---------------------------------------------------------------------------
# onset_pattern: which time-courses are typical for each disease.
#   "acute"     = sudden onset (within 24 hours)
#   "subacute"  = develops over days to ~1 week
#   "chronic"   = gradual onset over weeks/months or persistent condition
# A disease can have multiple typical patterns (e.g. pancreatitis: acute OR chronic).
#
# age_predisposition: which life-stage groups are at higher risk.
#   "puppy"   = under 1 year
#   "young"   = 1–3 years
#   "adult"   = 3–7 years
#   "senior"  = 7+ years
# Empty set means no particular age predisposition (all ages equally).

_DISEASE_ONSET: dict[str, set[str]] = {
    # -- Infectious --
    "Canine Parvovirus": {"acute"},
    "Canine Distemper": {"acute", "subacute"},
    "Kennel Cough (Bordetella)": {"acute", "subacute"},
    "Canine Influenza (CIV)": {"acute"},
    "Leptospirosis": {"acute", "subacute"},
    "Canine Infectious Hepatitis": {"acute"},
    "Canine Coronavirus (Enteric)": {"acute"},
    "Rabies": {"acute", "subacute"},
    "Canine Herpesvirus (CHV)": {"acute"},
    "Canine Papillomatosis": {"subacute", "chronic"},
    "Brucellosis": {"subacute", "chronic"},
    "Rocky Mountain Spotted Fever": {"acute"},
    "Tetanus": {"acute", "subacute"},
    "Nocardiosis": {"chronic"},
    "Actinomycosis": {"chronic"},
    # -- Parasitic --
    "Giardiasis": {"subacute", "chronic"},
    "Ehrlichiosis": {"acute", "chronic"},
    "Anaplasmosis": {"acute"},
    "Coccidiosis": {"acute", "subacute"},
    "Babesiosis": {"acute"},
    "Intestinal Parasites": {"subacute", "chronic"},
    "Heartworm Disease": {"chronic"},
    "Lyme Disease": {"subacute", "chronic"},
    "Leishmaniasis": {"chronic"},
    "Neosporosis": {"acute", "subacute"},
    "Toxoplasmosis": {"subacute"},
    "Hepatozoonosis": {"chronic"},
    "Roundworm Infection (Toxocara)": {"subacute", "chronic"},
    "Hookworm Infection": {"subacute", "chronic"},
    "Whipworm Infection (Trichuris)": {"chronic"},
    "Tapeworm Infection (Dipylidium/Echinococcus)": {"chronic"},
    "Ear Mite Infestation (Otodectes)": {"subacute", "chronic"},
    "Flea Allergy Dermatitis": {"acute", "chronic"},
    "Sarcoptic Mange (Scabies)": {"subacute"},
    "Cheyletiellosis (Walking Dandruff)": {"subacute", "chronic"},
    # -- Fungal --
    "Fungal Infection (Ringworm)": {"subacute", "chronic"},
    "Blastomycosis": {"subacute", "chronic"},
    "Histoplasmosis": {"subacute", "chronic"},
    "Coccidioidomycosis (Valley Fever)": {"subacute", "chronic"},
    "Cryptococcosis": {"subacute", "chronic"},
    "Aspergillosis": {"chronic"},
    "Sporotrichosis": {"subacute", "chronic"},
    # -- GI --
    "Gastric Dilatation-Volvulus (GDV/Bloat)": {"acute"},
    "Pancreatitis": {"acute", "chronic"},
    "Gastroenteritis": {"acute"},
    "Hemorrhagic Gastroenteritis (HGE)": {"acute"},
    "Foreign Body Obstruction": {"acute"},
    "Inflammatory Bowel Disease (IBD)": {"chronic"},
    "Megaesophagus": {"chronic"},
    "Exocrine Pancreatic Insufficiency (EPI)": {"chronic"},
    "Colitis": {"acute", "chronic"},
    "Portosystemic Shunt (Liver Shunt)": {"chronic"},
    "Gastric Ulcer": {"acute", "chronic"},
    "Esophagitis": {"acute", "subacute"},
    "Protein-Losing Enteropathy (PLE)": {"chronic"},
    "Mesenteric Volvulus": {"acute"},
    "Rectal Prolapse": {"acute", "chronic"},
    "Anal Sac Disease": {"subacute", "chronic"},
    "Intestinal Intussusception": {"acute"},
    "Megacolon": {"chronic"},
    "Gastric Foreign Body": {"acute"},
    # -- Endocrine --
    "Hypothyroidism": {"chronic"},
    "Hyperthyroidism": {"chronic"},
    "Cushing's Disease": {"chronic"},
    "Addison's Disease": {"acute", "chronic"},
    "Diabetes Mellitus": {"chronic"},
    "Diabetes Insipidus": {"chronic"},
    "Pheochromocytoma": {"acute", "chronic"},
    "Growth Hormone-Responsive Dermatosis": {"chronic"},
    "Insulinoma": {"acute", "chronic"},
    "Hyperparathyroidism": {"chronic"},
    # -- Urinary --
    "Urinary Tract Infection": {"acute", "subacute"},
    "Bladder Stones": {"subacute", "chronic"},
    "Kidney Disease (CKD)": {"chronic"},
    "Fanconi Syndrome": {"chronic"},
    "Ectopic Ureter": {"chronic"},
    "Glomerulonephritis": {"chronic"},
    "Pyelonephritis": {"acute", "subacute"},
    "Urethral Obstruction": {"acute"},
    "Cystinuria": {"chronic"},
    # -- Hepatic --
    "Liver Disease": {"subacute", "chronic"},
    "Copper Storage Disease": {"chronic"},
    "Portosystemic Shunt (Congenital)": {"chronic"},
    "Hepatocellular Carcinoma": {"chronic"},
    # -- Cardiac --
    "Heart Disease/CHF": {"chronic"},
    "Dilated Cardiomyopathy (DCM)": {"chronic"},
    "Patent Ductus Arteriosus (PDA)": {"chronic"},
    "Aortic Stenosis": {"chronic"},
    "Pulmonic Stenosis": {"chronic"},
    "Pericardial Effusion": {"acute", "chronic"},
    "Mitral Valve Disease (MMVD)": {"chronic"},
    "Sick Sinus Syndrome": {"chronic"},
    "Ventricular Septal Defect (VSD)": {"chronic"},
    "Atrial Fibrillation": {"acute", "chronic"},
    "Infective Endocarditis": {"subacute", "chronic"},
    "Myocarditis": {"acute", "subacute"},
    "Chemodectoma (Heart Base Tumor)": {"chronic"},
    # -- Respiratory --
    "Brachycephalic Airway Syndrome": {"chronic"},
    "Tracheal Collapse": {"chronic"},
    "Laryngeal Paralysis": {"chronic"},
    "Pneumonia": {"acute", "subacute"},
    "Aspiration Pneumonia": {"acute"},
    "Pleural Effusion": {"subacute", "chronic"},
    "Pulmonary Hypertension": {"chronic"},
    "Pulmonary Fibrosis": {"chronic"},
    "Nasal Tumor": {"chronic"},
    "Lung Lobe Torsion": {"acute"},
    "Nasal Adenocarcinoma": {"chronic"},
    "Chylothorax": {"subacute", "chronic"},
    # -- Dermatological --
    "Allergic Dermatitis": {"subacute", "chronic"},
    "Mange (Demodex/Sarcoptes)": {"subacute", "chronic"},
    "Pyoderma": {"acute", "subacute"},
    "Sebaceous Adenitis": {"chronic"},
    "Pemphigus": {"subacute", "chronic"},
    "Alopecia X": {"chronic"},
    "Acral Lick Dermatitis": {"chronic"},
    "Discoid Lupus Erythematosus (DLE)": {"chronic"},
    "Follicular Dysplasia": {"chronic"},
    "Dermoid Sinus": {"chronic"},
    "Zinc-Responsive Dermatosis": {"subacute", "chronic"},
    "Malassezia Dermatitis": {"subacute", "chronic"},
    "Systemic Lupus Erythematosus (SLE)": {"subacute", "chronic"},
    "Interdigital Cyst (Furuncle)": {"acute", "subacute"},
    "Seborrhea": {"chronic"},
    "Cutaneous Histiocytoma": {"subacute"},
    # -- Ophthalmologic --
    "Eye Infection (Conjunctivitis)": {"acute", "subacute"},
    "Glaucoma": {"acute", "chronic"},
    "Cherry Eye": {"acute"},
    "Keratoconjunctivitis Sicca (Dry Eye)": {"chronic"},
    "Entropion": {"chronic"},
    "Corneal Ulcer": {"acute"},
    "Lens Luxation": {"acute"},
    "Retinal Detachment": {"acute"},
    "Ectropion": {"chronic"},
    "Distichiasis": {"chronic"},
    "Nuclear Sclerosis": {"chronic"},
    "Retinal Dysplasia": {"chronic"},
    "Pannus (Chronic Superficial Keratitis)": {"chronic"},
    "Uveitis": {"acute", "subacute"},
    "Corneal Dystrophy": {"chronic"},
    "Collie Eye Anomaly (CEA)": {"chronic"},
    "Horner's Syndrome": {"acute", "subacute"},
    "Sudden Acquired Retinal Degeneration (SARDS)": {"acute"},
    "Progressive Retinal Atrophy (PRA)": {"chronic"},
    "Cataracts": {"chronic"},
    # -- Ear --
    "Ear Infection (Otitis)": {"acute", "subacute", "chronic"},
    "Foreign Body in Ear": {"acute"},
    "Aural Hematoma": {"acute"},
    # -- Musculoskeletal --
    "Osteoarthritis": {"chronic"},
    "Cruciate Ligament Injury": {"acute"},
    "Hip Dysplasia": {"chronic"},
    "Intervertebral Disc Disease (IVDD)": {"acute", "chronic"},
    "Elbow Dysplasia": {"chronic"},
    "Legg-Calvé-Perthes Disease": {"subacute", "chronic"},
    "Osteochondritis Dissecans (OCD)": {"subacute", "chronic"},
    "Panosteitis": {"subacute"},
    "Hypertrophic Osteodystrophy (HOD)": {"acute", "subacute"},
    "Patellar Luxation": {"acute", "chronic"},
    "Spondylosis Deformans": {"chronic"},
    "Masticatory Muscle Myositis": {"acute", "subacute"},
    "Craniomandibular Osteopathy": {"subacute"},
    "Immune-Mediated Polyarthritis (IMPA)": {"acute", "subacute"},
    "Luxating Shoulder": {"acute", "chronic"},
    "Hypertrophic Osteopathy": {"subacute", "chronic"},
    # -- Neurological --
    "Epilepsy": {"acute"},
    "Vestibular Disease": {"acute"},
    "Wobbler Syndrome": {"subacute", "chronic"},
    "Hydrocephalus": {"chronic"},
    "Syringomyelia (Chiari Malformation)": {"chronic"},
    "Cognitive Dysfunction Syndrome (CDS)": {"chronic"},
    "Myasthenia Gravis": {"subacute", "chronic"},
    "Granulomatous Meningoencephalitis (GME)": {"acute", "subacute"},
    "Degenerative Myelopathy (DM)": {"chronic"},
    "Cerebellar Hypoplasia": {"chronic"},
    "Tick Paralysis": {"acute", "subacute"},
    "Fibrocartilaginous Embolism (FCE)": {"acute"},
    "Canine Distemper Encephalitis": {"subacute"},
    "Scotty Cramp": {"acute"},
    "Cauda Equina Syndrome (Lumbosacral Stenosis)": {"chronic"},
    "Brain Tumor": {"subacute", "chronic"},
    # -- Oncology --
    "Cancer/Neoplasia": {"chronic"},
    "Hemangiosarcoma": {"acute", "chronic"},
    "Lymphoma": {"subacute", "chronic"},
    "Osteosarcoma": {"subacute", "chronic"},
    "Mast Cell Tumor": {"subacute", "chronic"},
    "Melanoma": {"chronic"},
    "Squamous Cell Carcinoma": {"chronic"},
    "Mammary Tumor": {"chronic"},
    "Transitional Cell Carcinoma": {"chronic"},
    "Histiocytic Sarcoma": {"subacute", "chronic"},
    "Fibrosarcoma": {"chronic"},
    "Anal Sac Adenocarcinoma": {"chronic"},
    "Insulinoma (Pancreatic Beta Cell Tumor)": {"subacute", "chronic"},
    "Thyroid Carcinoma": {"chronic"},
    "Perianal Adenoma": {"chronic"},
    "Soft Tissue Sarcoma": {"chronic"},
    "Lipoma": {"chronic"},
    "Plasmacytoma": {"subacute", "chronic"},
    "Oral Melanoma": {"chronic"},
    "Epulis (Gingival Mass)": {"chronic"},
    # -- Reproductive --
    "Pyometra": {"acute", "subacute"},
    "Prostate Disease": {"chronic"},
    "Cryptorchidism": {"chronic"},
    "Mastitis": {"acute"},
    "Eclampsia (Milk Fever)": {"acute"},
    "Benign Prostatic Hyperplasia (BPH)": {"chronic"},
    "Vaginitis": {"subacute", "chronic"},
    "Testicular Tumor": {"chronic"},
    "Paraphimosis": {"acute"},
    "Dystocia": {"acute"},
    # -- Hematological --
    "Immune-Mediated Hemolytic Anemia": {"acute", "subacute"},
    "Thrombocytopenia": {"acute", "subacute"},
    "Hemophilia A": {"acute"},
    "Autoimmune Thrombocytopenia (ITP)": {"acute", "subacute"},
    "von Willebrand Disease": {"acute"},
    "Exercise-Induced Collapse (EIC)": {"acute"},
    "Disseminated Intravascular Coagulation (DIC)": {"acute"},
    "Anemia of Chronic Disease": {"chronic"},
    "Evan's Syndrome": {"acute", "subacute"},
    "Hemolytic Uremic Syndrome": {"acute"},
    # -- Toxicology --
    "Chocolate Toxicosis": {"acute"},
    "Grape/Raisin Toxicosis": {"acute"},
    "Xylitol Poisoning": {"acute"},
    "NSAID Toxicosis": {"acute"},
    "Rodenticide Poisoning": {"acute", "subacute"},
    "Onion/Garlic Toxicosis": {"acute", "subacute"},
    "Ethylene Glycol Poisoning (Antifreeze)": {"acute"},
    "Marijuana Toxicosis": {"acute"},
    "Lead Poisoning": {"acute", "chronic"},
    # -- Environmental --
    "Heat Stroke": {"acute"},
    "Hypothermia": {"acute"},
    "Drowning / Near-Drowning": {"acute"},
    "Snakebite Envenomation": {"acute"},
    "Bee/Wasp Sting Anaphylaxis": {"acute"},
    # -- Dental --
    "Periodontal Disease": {"chronic"},
    "Tooth Abscess": {"acute", "subacute"},
    "Tooth Fracture": {"acute"},
    "Stomatitis": {"subacute", "chronic"},
    "Cleft Palate": {"chronic"},
    # -- Behavioral --
    "Separation Anxiety": {"chronic"},
    "Compulsive Disorder (Canine OCD)": {"chronic"},
    "Noise Phobia": {"acute", "chronic"},
    "Pica": {"chronic"},
    # -- Congenital --
    "Congenital Deafness": {"chronic"},
    "Atlantoaxial Instability": {"acute", "chronic"},
    "Persistent Right Aortic Arch (PRAA)": {"chronic"},
    "Mucopolysaccharidosis": {"chronic"},
    "Glycogen Storage Disease": {"chronic"},
    "Malignant Hyperthermia": {"acute"},
    "Juvenile Cellulitis (Puppy Strangles)": {"acute", "subacute"},
}


_DISEASE_AGE_PREDISPOSITION: dict[str, set[str]] = {
    # -- Puppy / young predispositions --
    "Canine Parvovirus": {"puppy", "young"},
    "Canine Distemper": {"puppy", "young"},
    "Canine Herpesvirus (CHV)": {"puppy"},
    "Canine Papillomatosis": {"puppy", "young"},
    "Roundworm Infection (Toxocara)": {"puppy"},
    "Hookworm Infection": {"puppy", "young"},
    "Coccidiosis": {"puppy", "young"},
    "Giardiasis": {"puppy", "young"},
    "Intestinal Parasites": {"puppy", "young"},
    "Cherry Eye": {"puppy", "young"},
    "Panosteitis": {"puppy", "young"},
    "Hypertrophic Osteodystrophy (HOD)": {"puppy"},
    "Legg-Calvé-Perthes Disease": {"puppy", "young"},
    "Osteochondritis Dissecans (OCD)": {"puppy", "young"},
    "Intestinal Intussusception": {"puppy", "young"},
    "Juvenile Cellulitis (Puppy Strangles)": {"puppy"},
    "Craniomandibular Osteopathy": {"puppy"},
    "Retinal Dysplasia": {"puppy"},
    "Collie Eye Anomaly (CEA)": {"puppy"},
    "Cleft Palate": {"puppy"},
    "Congenital Deafness": {"puppy"},
    "Atlantoaxial Instability": {"puppy", "young"},
    "Persistent Right Aortic Arch (PRAA)": {"puppy"},
    "Mucopolysaccharidosis": {"puppy"},
    "Glycogen Storage Disease": {"puppy"},
    "Patent Ductus Arteriosus (PDA)": {"puppy", "young"},
    "Ventricular Septal Defect (VSD)": {"puppy", "young"},
    "Portosystemic Shunt (Congenital)": {"puppy", "young"},
    "Hydrocephalus": {"puppy"},
    "Cerebellar Hypoplasia": {"puppy"},
    "Ectopic Ureter": {"puppy", "young"},
    # -- Young / adult --
    "Epilepsy": {"young", "adult"},
    "Allergic Dermatitis": {"young", "adult"},
    "Immune-Mediated Hemolytic Anemia": {"young", "adult"},
    "Autoimmune Thrombocytopenia (ITP)": {"young", "adult"},
    "Immune-Mediated Polyarthritis (IMPA)": {"young", "adult"},
    "Granulomatous Meningoencephalitis (GME)": {"young", "adult"},
    "Systemic Lupus Erythematosus (SLE)": {"young", "adult"},
    "Evan's Syndrome": {"young", "adult"},
    "Separation Anxiety": {"young", "adult"},
    "Exercise-Induced Collapse (EIC)": {"young", "adult"},
    "Cruciate Ligament Injury": {"adult"},
    "Pyometra": {"adult", "senior"},
    "Mastitis": {"adult"},
    "Eclampsia (Milk Fever)": {"adult"},
    "Dystocia": {"adult"},
    "Cutaneous Histiocytoma": {"young"},
    # -- Senior predispositions --
    "Hypothyroidism": {"adult", "senior"},
    "Cushing's Disease": {"adult", "senior"},
    "Diabetes Mellitus": {"adult", "senior"},
    "Kidney Disease (CKD)": {"senior"},
    "Heart Disease/CHF": {"adult", "senior"},
    "Dilated Cardiomyopathy (DCM)": {"adult", "senior"},
    "Mitral Valve Disease (MMVD)": {"adult", "senior"},
    "Osteoarthritis": {"adult", "senior"},
    "Cognitive Dysfunction Syndrome (CDS)": {"senior"},
    "Degenerative Myelopathy (DM)": {"adult", "senior"},
    "Laryngeal Paralysis": {"senior"},
    "Vestibular Disease": {"senior"},
    "Cancer/Neoplasia": {"adult", "senior"},
    "Hemangiosarcoma": {"adult", "senior"},
    "Lymphoma": {"adult", "senior"},
    "Osteosarcoma": {"adult", "senior"},
    "Mast Cell Tumor": {"adult", "senior"},
    "Melanoma": {"senior"},
    "Squamous Cell Carcinoma": {"adult", "senior"},
    "Mammary Tumor": {"adult", "senior"},
    "Transitional Cell Carcinoma": {"senior"},
    "Histiocytic Sarcoma": {"adult", "senior"},
    "Fibrosarcoma": {"adult", "senior"},
    "Anal Sac Adenocarcinoma": {"senior"},
    "Insulinoma (Pancreatic Beta Cell Tumor)": {"adult", "senior"},
    "Thyroid Carcinoma": {"adult", "senior"},
    "Perianal Adenoma": {"senior"},
    "Hepatocellular Carcinoma": {"senior"},
    "Soft Tissue Sarcoma": {"adult", "senior"},
    "Oral Melanoma": {"senior"},
    "Brain Tumor": {"adult", "senior"},
    "Prostate Disease": {"adult", "senior"},
    "Benign Prostatic Hyperplasia (BPH)": {"adult", "senior"},
    "Testicular Tumor": {"adult", "senior"},
    "Cataracts": {"senior"},
    "Nuclear Sclerosis": {"senior"},
    "Sudden Acquired Retinal Degeneration (SARDS)": {"adult", "senior"},
    "Progressive Retinal Atrophy (PRA)": {"adult", "senior"},
    "Sick Sinus Syndrome": {"senior"},
    "Atrial Fibrillation": {"senior"},
    "Pulmonary Fibrosis": {"senior"},
    "Nasal Tumor": {"senior"},
    "Nasal Adenocarcinoma": {"senior"},
    "Spondylosis Deformans": {"senior"},
    "Cauda Equina Syndrome (Lumbosacral Stenosis)": {"adult", "senior"},
    "Tracheal Collapse": {"adult", "senior"},
    "Periodontal Disease": {"adult", "senior"},
    "Hip Dysplasia": {"puppy", "young", "adult"},
    "Elbow Dysplasia": {"puppy", "young"},
    "Patellar Luxation": {"young", "adult"},
    "Intervertebral Disc Disease (IVDD)": {"adult", "senior"},
    "Wobbler Syndrome": {"young", "senior"},
    "Brachycephalic Airway Syndrome": {"young", "adult", "senior"},
    "Hepatozoonosis": {"young", "adult"},
    "Hyperparathyroidism": {"senior"},
    "Anemia of Chronic Disease": {"adult", "senior"},
    "Lipoma": {"adult", "senior"},
    "Alopecia X": {"adult"},
    "Keratoconjunctivitis Sicca (Dry Eye)": {"adult", "senior"},
    "Glaucoma": {"adult", "senior"},
    "Pericardial Effusion": {"adult", "senior"},
    "Infective Endocarditis": {"adult", "senior"},
    "Chemodectoma (Heart Base Tumor)": {"senior"},
    "Chylothorax": {"adult", "senior"},
    "Megacolon": {"adult", "senior"},
    "Copper Storage Disease": {"young", "adult"},
    "Myasthenia Gravis": {"young", "adult", "senior"},
    "Pemphigus": {"adult"},
    "Sebaceous Adenitis": {"young", "adult"},
    "Epulis (Gingival Mass)": {"adult", "senior"},
    "Plasmacytoma": {"adult", "senior"},
}


def _age_years_to_stage(age_years: float) -> str:
    """Convert numeric age to life-stage label."""
    if age_years < 1.0:
        return "puppy"
    if age_years < 3.0:
        return "young"
    if age_years < 7.0:
        return "adult"
    return "senior"


# ---------------------------------------------------------------------------
# Disease prevalence (有病率ベースの重み付け)
# ---------------------------------------------------------------------------
# 臨床的に一般的な疾患を上位に、稀な疾患を下位にランクさせるためのベイズ的事前確率。
# "very_common" (1.4x) > "common" (1.2x) > "uncommon" (0.9x) > "rare" (0.7x)
# デフォルト(未登録疾患) = 1.0 (neutral)
#
# 参考: Ettinger & Feldman (2017), Nelson & Couto (2019), 日本小動物獣医学会統計
_PREVALENCE_MULTIPLIER = _PREVALENCE_MULTIPLIER_MODULE

_DISEASE_PREVALENCE = _DISEASE_PREVALENCE_MODULE


# ---------------------------------------------------------------------------
# Disease database
# ---------------------------------------------------------------------------
# Each entry:
#   name            – English name
#   name_ja         – Japanese name
#   symptoms        – set of symptom IDs (use _ANY_LIMPING where any limb)
#   description     – short English description
#   urgency         – "normal" | "urgent" | "emergency"

# Disease database imported from dog_diseases module
_DISEASE_DB = _DISEASE_DB_MODULE

# ---------------------------------------------------------------------------
# Diagnostic-test database
# ---------------------------------------------------------------------------
# Each entry:
#   name            – English test name
#   name_ja         – Japanese name
#   purpose         – what it checks
#   related_diseases – set of disease names this test is indicated for

# Diagnostic test database imported from dog_diseases module
_TEST_DB = _TEST_DB_MODULE

# Enrichment and fallback content is handled in dog_diseases module

# ---------------------------------------------------------------------------
# Breed-specific disease risk multipliers
# ---------------------------------------------------------------------------
# Maps breed IDs to diseases they are predisposed to, with risk multipliers.
# A multiplier > 1.0 boosts the match score for that disease when the breed
# is known, reflecting genuine genetic/conformational predisposition.

_BREED_DISEASE_RISK: dict[str, dict[str, float]] = {
    "101_french_bulldog": {
        "Brachycephalic Airway Syndrome": 2.5,
        "Intervertebral Disc Disease (IVDD)": 2.0,
        "Allergic Dermatitis": 1.8,
        "Hip Dysplasia": 1.5,
    },
    "172d_poodle_toy": {
        "Osteoarthritis": 1.3,
        "Allergic Dermatitis": 1.5,
        "Epilepsy": 1.3,
    },
    "122_labrador_retriever": {
        "Hip Dysplasia": 2.0,
        "Osteoarthritis": 1.8,
        "Allergic Dermatitis": 1.5,
        "Cancer/Neoplasia": 1.5,
    },
    "166_german_shepherd": {
        "Hip Dysplasia": 2.5,
        "Intervertebral Disc Disease (IVDD)": 1.5,
        "Allergic Dermatitis": 1.5,
    },
    "111_golden_retriever": {
        "Hip Dysplasia": 2.0,
        "Heart Disease/CHF": 1.5,
        "Cancer/Neoplasia": 2.0,
        "Hypothyroidism": 1.5,
    },
    "218_chihuahua": {
        "Heart Disease/CHF": 1.5,
        "Osteoarthritis": 1.3,
    },
    "257_shiba": {
        "Allergic Dermatitis": 2.0,
        "Glaucoma": 1.8,
    },
    "161_beagle": {
        "Intervertebral Disc Disease (IVDD)": 1.5,
        "Epilepsy": 2.0,
        "Hypothyroidism": 1.5,
        "Glaucoma": 1.5,
    },
    "86_yorkshire_terrier": {
        "Heart Disease/CHF": 1.5,
        "Liver Disease": 1.5,
    },
    "39_welsh_corgi": {
        "Intervertebral Disc Disease (IVDD)": 2.5,
        "Hip Dysplasia": 1.5,
    },
    "102_english_bulldog": {
        "Brachycephalic Airway Syndrome": 2.5,
        "Hip Dysplasia": 2.0,
        "Allergic Dermatitis": 1.8,
        "Heart Disease/CHF": 1.3,
    },
    "103_pug": {
        "Brachycephalic Airway Syndrome": 2.5,
        "Eye Infection (Conjunctivitis)": 1.5,
        "Glaucoma": 1.3,
        "Allergic Dermatitis": 1.5,
    },
    "104_boston_terrier": {
        "Brachycephalic Airway Syndrome": 2.0,
        "Glaucoma": 1.5,
        "Allergic Dermatitis": 1.3,
    },
    "105_boxer": {
        "Cancer/Neoplasia": 2.0,
        "Heart Disease/CHF": 1.8,
        "Hypothyroidism": 1.3,
        "Allergic Dermatitis": 1.3,
    },
    "106_rottweiler": {
        "Hip Dysplasia": 2.0,
        "Cancer/Neoplasia": 1.8,
        "Cruciate Ligament Injury": 1.5,
        "Heart Disease/CHF": 1.3,
    },
    "107_doberman_pinscher": {
        "Heart Disease/CHF": 2.5,
        "Hypothyroidism": 1.5,
        "Hip Dysplasia": 1.3,
    },
    "108_great_dane": {
        "Gastric Dilatation-Volvulus (GDV/Bloat)": 2.5,
        "Heart Disease/CHF": 2.0,
        "Hip Dysplasia": 1.8,
        "Cancer/Neoplasia": 1.5,
    },
    "109_bernese_mountain_dog": {
        "Cancer/Neoplasia": 2.5,
        "Hip Dysplasia": 2.0,
        "Cruciate Ligament Injury": 1.5,
        "Gastric Dilatation-Volvulus (GDV/Bloat)": 1.3,
    },
    "110_cavalier_king_charles": {
        "Heart Disease/CHF": 2.5,
        "Epilepsy": 1.5,
        "Allergic Dermatitis": 1.3,
        "Eye Infection (Conjunctivitis)": 1.3,
    },
    "112_cocker_spaniel": {
        "Ear Infection (Otitis)": 2.0,
        "Allergic Dermatitis": 1.8,
        "Glaucoma": 1.5,
        "Hypothyroidism": 1.3,
    },
    "113_springer_spaniel": {
        "Ear Infection (Otitis)": 1.8,
        "Hip Dysplasia": 1.5,
        "Allergic Dermatitis": 1.3,
    },
    "114_dachshund": {
        "Intervertebral Disc Disease (IVDD)": 3.0,
        "Diabetes Mellitus": 1.3,
        "Cushing's Disease": 1.3,
    },
    "115_miniature_schnauzer": {
        "Pancreatitis": 2.0,
        "Diabetes Mellitus": 1.5,
        "Bladder Stones": 1.5,
        "Hyperthyroidism": 1.3,
    },
    "116_shih_tzu": {
        "Brachycephalic Airway Syndrome": 1.8,
        "Eye Infection (Conjunctivitis)": 1.5,
        "Kidney Disease (CKD)": 1.3,
        "Allergic Dermatitis": 1.3,
    },
    "117_maltese": {
        "Heart Disease/CHF": 1.5,
        "Liver Disease": 1.5,
        "Allergic Dermatitis": 1.3,
    },
    "118_havanese": {
        "Heart Disease/CHF": 1.3,
        "Liver Disease": 1.3,
        "Allergic Dermatitis": 1.3,
    },
    "119_bichon_frise": {
        "Allergic Dermatitis": 1.8,
        "Bladder Stones": 1.5,
        "Diabetes Mellitus": 1.3,
    },
    "120_pomeranian": {
        "Heart Disease/CHF": 1.5,
        "Hypothyroidism": 1.3,
        "Allergic Dermatitis": 1.3,
    },
    "121_shetland_sheepdog": {
        "Epilepsy": 1.5,
        "Hypothyroidism": 1.5,
        "Allergic Dermatitis": 1.3,
    },
    "123_border_collie": {
        "Epilepsy": 1.8,
        "Hip Dysplasia": 1.3,
        "Osteoarthritis": 1.3,
    },
    "124_australian_shepherd": {
        "Epilepsy": 1.5,
        "Hip Dysplasia": 1.5,
        "Cancer/Neoplasia": 1.3,
    },
    "125_siberian_husky": {
        "Glaucoma": 1.8,
        "Hypothyroidism": 1.5,
        "Hip Dysplasia": 1.3,
    },
    "126_alaskan_malamute": {
        "Hip Dysplasia": 1.8,
        "Hypothyroidism": 1.5,
        "Glaucoma": 1.3,
    },
    "127_akita": {
        "Hip Dysplasia": 1.8,
        "Hypothyroidism": 1.5,
        "Immune-Mediated Hemolytic Anemia": 1.5,
        "Glaucoma": 1.3,
    },
    "128_samoyed": {
        "Hip Dysplasia": 1.5,
        "Diabetes Mellitus": 1.5,
        "Hypothyroidism": 1.3,
    },
    "129_newfoundland": {
        "Heart Disease/CHF": 2.0,
        "Hip Dysplasia": 1.8,
        "Cruciate Ligament Injury": 1.5,
        "Gastric Dilatation-Volvulus (GDV/Bloat)": 1.3,
    },
    "130_saint_bernard": {
        "Hip Dysplasia": 2.0,
        "Gastric Dilatation-Volvulus (GDV/Bloat)": 2.0,
        "Heart Disease/CHF": 1.5,
        "Osteoarthritis": 1.5,
    },
    "131_irish_setter": {
        "Hip Dysplasia": 1.5,
        "Gastric Dilatation-Volvulus (GDV/Bloat)": 1.8,
        "Epilepsy": 1.3,
        "Hypothyroidism": 1.3,
    },
    "132_weimaraner": {
        "Gastric Dilatation-Volvulus (GDV/Bloat)": 2.0,
        "Hip Dysplasia": 1.5,
        "Hypothyroidism": 1.3,
    },
    "133_vizsla": {
        "Epilepsy": 1.5,
        "Allergic Dermatitis": 1.3,
        "Cancer/Neoplasia": 1.3,
    },
    "134_german_shorthaired_pointer": {
        "Hip Dysplasia": 1.5,
        "Cancer/Neoplasia": 1.3,
        "Gastric Dilatation-Volvulus (GDV/Bloat)": 1.3,
    },
    "135_brittany": {
        "Hip Dysplasia": 1.5,
        "Epilepsy": 1.3,
        "Hypothyroidism": 1.3,
    },
    "136_standard_poodle": {
        "Gastric Dilatation-Volvulus (GDV/Bloat)": 1.8,
        "Addison's Disease": 1.8,
        "Hip Dysplasia": 1.5,
        "Epilepsy": 1.3,
    },
    "137_miniature_poodle": {
        "Epilepsy": 1.5,
        "Glaucoma": 1.3,
        "Allergic Dermatitis": 1.3,
    },
    "138_west_highland_white_terrier": {
        "Allergic Dermatitis": 2.0,
        "Liver Disease": 1.5,
        "Addison's Disease": 1.3,
    },
    "139_scottish_terrier": {
        "Bladder Stones": 1.8,
        "Cancer/Neoplasia": 1.5,
        "Allergic Dermatitis": 1.3,
    },
    "140_cairn_terrier": {
        "Allergic Dermatitis": 1.5,
        "Liver Disease": 1.3,
        "Diabetes Mellitus": 1.3,
    },
    "141_jack_russell_terrier": {
        "Allergic Dermatitis": 1.3,
        "Glaucoma": 1.3,
        "Epilepsy": 1.3,
    },
    "142_staffordshire_bull_terrier": {
        "Allergic Dermatitis": 1.8,
        "Cruciate Ligament Injury": 1.5,
        "Cancer/Neoplasia": 1.3,
    },
    "143_bull_terrier": {
        "Kidney Disease (CKD)": 1.8,
        "Heart Disease/CHF": 1.5,
        "Allergic Dermatitis": 1.5,
    },
    "144_airedale_terrier": {
        "Allergic Dermatitis": 1.5,
        "Hip Dysplasia": 1.3,
        "Hypothyroidism": 1.3,
    },
    "145_whippet": {
        "Heart Disease/CHF": 1.3,
        "Eye Infection (Conjunctivitis)": 1.3,
    },
    "146_italian_greyhound": {
        "Epilepsy": 1.5,
        "Fractures/Osteoarthritis": 1.3,
        "Allergic Dermatitis": 1.3,
    },
    "147_greyhound": {
        "Cancer/Neoplasia": 1.5,
        "Hypothyroidism": 1.3,
        "Osteoarthritis": 1.3,
    },
    "148_basset_hound": {
        "Ear Infection (Otitis)": 2.0,
        "Intervertebral Disc Disease (IVDD)": 1.8,
        "Glaucoma": 1.5,
        "Hip Dysplasia": 1.3,
    },
    "149_bloodhound": {
        "Gastric Dilatation-Volvulus (GDV/Bloat)": 2.0,
        "Ear Infection (Otitis)": 1.8,
        "Hip Dysplasia": 1.5,
    },
    "150_dalmatian": {
        "Bladder Stones": 2.0,
        "Allergic Dermatitis": 1.5,
        "Epilepsy": 1.3,
    },
}

# ---------------------------------------------------------------------------
# Breed-specific recommended genetic/screening tests
# ---------------------------------------------------------------------------
# Maps breed IDs to a list of recommended genetic or screening tests,
# including Japanese localization and clinical purpose.

_BREED_GENETIC_TESTS: dict[str, list[dict[str, str]]] = {
    "101_french_bulldog": [
        {
            "test": "Brachycephalic Assessment",
            "test_ja": "\u77ed\u982d\u7a2e\u8a55\u4fa1",
            "purpose": "Evaluate airway obstruction severity",
        },
        {
            "test": "Spine X-ray/CT",
            "test_ja": "\u810a\u690e\u30ec\u30f3\u30c8\u30b2\u30f3/CT",
            "purpose": "Screen for IVDD and hemivertebrae",
        },
        {
            "test": "Patella Evaluation",
            "test_ja": "\u819d\u84cb\u9aa8\u8a55\u4fa1",
            "purpose": "Check for patellar luxation grade",
        },
        {
            "test": "Hip Radiograph (PennHIP/OFA)",
            "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3",
            "purpose": "Screen for hip dysplasia",
        },
    ],
    "172d_poodle_toy": [
        {
            "test": "Patella Evaluation",
            "test_ja": "\u819d\u84cb\u9aa8\u8a55\u4fa1",
            "purpose": "Screen for patellar luxation",
        },
        {
            "test": "PRA DNA Test",
            "test_ja": "PRA\u907a\u4f1d\u5b50\u691c\u67fb",
            "purpose": "Test for progressive retinal atrophy gene",
        },
        {
            "test": "Allergy Panel",
            "test_ja": "\u30a2\u30ec\u30eb\u30ae\u30fc\u30d1\u30cd\u30eb",
            "purpose": "Identify environmental or food allergens",
        },
        {
            "test": "Thyroid Panel",
            "test_ja": "\u7532\u72b6\u817a\u30d1\u30cd\u30eb",
            "purpose": "Screen for thyroid dysfunction",
        },
    ],
    "122_labrador_retriever": [
        {
            "test": "Hip Radiograph (PennHIP/OFA)",
            "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3",
            "purpose": "Screen for hip dysplasia",
        },
        {
            "test": "Elbow Radiograph",
            "test_ja": "\u8098\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3",
            "purpose": "Screen for elbow dysplasia",
        },
        {
            "test": "EIC DNA Test",
            "test_ja": "EIC\u907a\u4f1d\u5b50\u691c\u67fb",
            "purpose": "Test for exercise-induced collapse gene",
        },
        {
            "test": "Ophthalmologic Exam",
            "test_ja": "\u773c\u79d1\u691c\u67fb",
            "purpose": "Screen for progressive retinal atrophy",
        },
        {
            "test": "Cardiac Exam",
            "test_ja": "\u5fc3\u81d3\u691c\u67fb",
            "purpose": "Screen for tricuspid valve dysplasia",
        },
    ],
    "166_german_shepherd": [
        {
            "test": "Hip Radiograph (PennHIP/OFA)",
            "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3",
            "purpose": "Screen for hip dysplasia",
        },
        {
            "test": "Elbow Radiograph",
            "test_ja": "\u8098\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3",
            "purpose": "Screen for elbow dysplasia",
        },
        {
            "test": "DM DNA Test",
            "test_ja": "DM\u907a\u4f1d\u5b50\u691c\u67fb",
            "purpose": "Test for degenerative myelopathy gene",
        },
        {"test": "Cardiac Exam", "test_ja": "\u5fc3\u81d3\u691c\u67fb", "purpose": "Screen for aortic stenosis"},
        {
            "test": "Allergy Panel",
            "test_ja": "\u30a2\u30ec\u30eb\u30ae\u30fc\u30d1\u30cd\u30eb",
            "purpose": "Identify environmental or food allergens",
        },
    ],
    "111_golden_retriever": [
        {
            "test": "Hip Radiograph (PennHIP/OFA)",
            "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3",
            "purpose": "Screen for hip dysplasia",
        },
        {
            "test": "Elbow Radiograph",
            "test_ja": "\u8098\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3",
            "purpose": "Screen for elbow dysplasia",
        },
        {
            "test": "Cardiac Exam",
            "test_ja": "\u5fc3\u81d3\u691c\u67fb",
            "purpose": "Screen for subvalvular aortic stenosis",
        },
        {
            "test": "Ophthalmologic Exam",
            "test_ja": "\u773c\u79d1\u691c\u67fb",
            "purpose": "Screen for cataracts and PRA",
        },
        {
            "test": "Thyroid Panel",
            "test_ja": "\u7532\u72b6\u817a\u30d1\u30cd\u30eb",
            "purpose": "Screen for hypothyroidism",
        },
        {
            "test": "Cancer Screening (Oncology Panel)",
            "test_ja": "\u816b\u760d\u30b9\u30af\u30ea\u30fc\u30cb\u30f3\u30b0",
            "purpose": "Early detection of lymphoma and hemangiosarcoma",
        },
    ],
    "218_chihuahua": [
        {"test": "Cardiac Exam", "test_ja": "\u5fc3\u81d3\u691c\u67fb", "purpose": "Screen for mitral valve disease"},
        {
            "test": "Patella Evaluation",
            "test_ja": "\u819d\u84cb\u9aa8\u8a55\u4fa1",
            "purpose": "Check for patellar luxation grade",
        },
        {
            "test": "Ophthalmologic Exam",
            "test_ja": "\u773c\u79d1\u691c\u67fb",
            "purpose": "Screen for lens luxation and glaucoma",
        },
    ],
    "257_shiba": [
        {
            "test": "Allergy Panel",
            "test_ja": "\u30a2\u30ec\u30eb\u30ae\u30fc\u30d1\u30cd\u30eb",
            "purpose": "Identify environmental or food allergens",
        },
        {
            "test": "Ophthalmologic Exam",
            "test_ja": "\u773c\u79d1\u691c\u67fb",
            "purpose": "Screen for glaucoma and cataracts",
        },
        {
            "test": "Patella Evaluation",
            "test_ja": "\u819d\u84cb\u9aa8\u8a55\u4fa1",
            "purpose": "Check for patellar luxation",
        },
        {
            "test": "Hip Radiograph (PennHIP/OFA)",
            "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3",
            "purpose": "Screen for hip dysplasia",
        },
    ],
    "161_beagle": [
        {
            "test": "Ophthalmologic Exam",
            "test_ja": "\u773c\u79d1\u691c\u67fb",
            "purpose": "Screen for glaucoma and cherry eye",
        },
        {
            "test": "Thyroid Panel",
            "test_ja": "\u7532\u72b6\u817a\u30d1\u30cd\u30eb",
            "purpose": "Screen for hypothyroidism",
        },
        {
            "test": "MLS DNA Test",
            "test_ja": "MLS\u907a\u4f1d\u5b50\u691c\u67fb",
            "purpose": "Test for musladin-lueke syndrome gene",
        },
        {"test": "Cardiac Exam", "test_ja": "\u5fc3\u81d3\u691c\u67fb", "purpose": "Screen for pulmonic stenosis"},
        {
            "test": "Hip Radiograph (PennHIP/OFA)",
            "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3",
            "purpose": "Screen for hip dysplasia",
        },
    ],
    "86_yorkshire_terrier": [
        {"test": "Cardiac Exam", "test_ja": "\u5fc3\u81d3\u691c\u67fb", "purpose": "Screen for mitral valve disease"},
        {
            "test": "Bile Acids Test",
            "test_ja": "\u80c6\u6c41\u9178\u691c\u67fb",
            "purpose": "Screen for portosystemic shunt",
        },
        {
            "test": "Patella Evaluation",
            "test_ja": "\u819d\u84cb\u9aa8\u8a55\u4fa1",
            "purpose": "Check for patellar luxation grade",
        },
        {
            "test": "Ophthalmologic Exam",
            "test_ja": "\u773c\u79d1\u691c\u67fb",
            "purpose": "Screen for cataracts and dry eye",
        },
    ],
    "39_welsh_corgi": [
        {
            "test": "Spine X-ray/CT",
            "test_ja": "\u810a\u690e\u30ec\u30f3\u30c8\u30b2\u30f3/CT",
            "purpose": "Screen for IVDD",
        },
        {
            "test": "DM DNA Test",
            "test_ja": "DM\u907a\u4f1d\u5b50\u691c\u67fb",
            "purpose": "Test for degenerative myelopathy gene",
        },
        {
            "test": "Hip Radiograph (PennHIP/OFA)",
            "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3",
            "purpose": "Screen for hip dysplasia",
        },
        {
            "test": "Ophthalmologic Exam",
            "test_ja": "\u773c\u79d1\u691c\u67fb",
            "purpose": "Screen for PRA and cataracts",
        },
        {
            "test": "vWD DNA Test",
            "test_ja": "vWD\u907a\u4f1d\u5b50\u691c\u67fb",
            "purpose": "Test for von Willebrand disease gene",
        },
    ],
    "102_english_bulldog": [
        {
            "test": "Brachycephalic Assessment",
            "test_ja": "\u77ed\u982d\u7a2e\u8a55\u4fa1",
            "purpose": "Evaluate airway obstruction severity",
        },
        {
            "test": "Hip Radiograph (PennHIP/OFA)",
            "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3",
            "purpose": "Screen for hip dysplasia",
        },
        {"test": "Cardiac Exam", "test_ja": "\u5fc3\u81d3\u691c\u67fb", "purpose": "Screen for pulmonic stenosis"},
        {
            "test": "Patella Evaluation",
            "test_ja": "\u819d\u84cb\u9aa8\u8a55\u4fa1",
            "purpose": "Check for patellar luxation",
        },
        {
            "test": "Spine X-ray/CT",
            "test_ja": "\u810a\u690e\u30ec\u30f3\u30c8\u30b2\u30f3/CT",
            "purpose": "Screen for hemivertebrae",
        },
    ],
    "103_pug": [
        {
            "test": "Brachycephalic Assessment",
            "test_ja": "\u77ed\u982d\u7a2e\u8a55\u4fa1",
            "purpose": "Evaluate airway obstruction severity",
        },
        {
            "test": "Ophthalmologic Exam",
            "test_ja": "\u773c\u79d1\u691c\u67fb",
            "purpose": "Screen for corneal ulcers and PDE",
        },
        {
            "test": "PDE DNA Test",
            "test_ja": "PDE\u907a\u4f1d\u5b50\u691c\u67fb",
            "purpose": "Test for pug dog encephalitis gene",
        },
        {
            "test": "Hip Radiograph (PennHIP/OFA)",
            "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3",
            "purpose": "Screen for hip dysplasia",
        },
        {
            "test": "Patella Evaluation",
            "test_ja": "\u819d\u84cb\u9aa8\u8a55\u4fa1",
            "purpose": "Check for patellar luxation",
        },
    ],
    "104_boston_terrier": [
        {
            "test": "Brachycephalic Assessment",
            "test_ja": "\u77ed\u982d\u7a2e\u8a55\u4fa1",
            "purpose": "Evaluate airway obstruction severity",
        },
        {
            "test": "Ophthalmologic Exam",
            "test_ja": "\u773c\u79d1\u691c\u67fb",
            "purpose": "Screen for cataracts and cherry eye",
        },
        {
            "test": "Patella Evaluation",
            "test_ja": "\u819d\u84cb\u9aa8\u8a55\u4fa1",
            "purpose": "Check for patellar luxation",
        },
    ],
    "105_boxer": [
        {
            "test": "Cardiac Exam",
            "test_ja": "\u5fc3\u81d3\u691c\u67fb",
            "purpose": "Screen for aortic stenosis and ARVC",
        },
        {
            "test": "Holter Monitor",
            "test_ja": "\u30db\u30eb\u30bf\u30fc\u5fc3\u96fb\u56f3",
            "purpose": "24-hour ECG monitoring for arrhythmias",
        },
        {
            "test": "Cancer Screening (Oncology Panel)",
            "test_ja": "\u816b\u760d\u30b9\u30af\u30ea\u30fc\u30cb\u30f3\u30b0",
            "purpose": "Early detection of mast cell tumors and lymphoma",
        },
        {
            "test": "Thyroid Panel",
            "test_ja": "\u7532\u72b6\u817a\u30d1\u30cd\u30eb",
            "purpose": "Screen for hypothyroidism",
        },
        {
            "test": "DM DNA Test",
            "test_ja": "DM\u907a\u4f1d\u5b50\u691c\u67fb",
            "purpose": "Test for degenerative myelopathy gene",
        },
    ],
    "106_rottweiler": [
        {
            "test": "Hip Radiograph (PennHIP/OFA)",
            "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3",
            "purpose": "Screen for hip dysplasia",
        },
        {
            "test": "Elbow Radiograph",
            "test_ja": "\u8098\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3",
            "purpose": "Screen for elbow dysplasia",
        },
        {"test": "Cardiac Exam", "test_ja": "\u5fc3\u81d3\u691c\u67fb", "purpose": "Screen for aortic stenosis"},
        {
            "test": "Ophthalmologic Exam",
            "test_ja": "\u773c\u79d1\u691c\u67fb",
            "purpose": "Screen for PRA and cataracts",
        },
        {
            "test": "Cancer Screening (Oncology Panel)",
            "test_ja": "\u816b\u760d\u30b9\u30af\u30ea\u30fc\u30cb\u30f3\u30b0",
            "purpose": "Early detection of osteosarcoma",
        },
    ],
    "107_doberman_pinscher": [
        {"test": "Cardiac Exam", "test_ja": "\u5fc3\u81d3\u691c\u67fb", "purpose": "Screen for dilated cardiomyopathy"},
        {
            "test": "Holter Monitor",
            "test_ja": "\u30db\u30eb\u30bf\u30fc\u5fc3\u96fb\u56f3",
            "purpose": "24-hour ECG monitoring for arrhythmias",
        },
        {
            "test": "vWD DNA Test",
            "test_ja": "vWD\u907a\u4f1d\u5b50\u691c\u67fb",
            "purpose": "Test for von Willebrand disease gene",
        },
        {
            "test": "Thyroid Panel",
            "test_ja": "\u7532\u72b6\u817a\u30d1\u30cd\u30eb",
            "purpose": "Screen for hypothyroidism",
        },
        {
            "test": "Hip Radiograph (PennHIP/OFA)",
            "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3",
            "purpose": "Screen for hip dysplasia",
        },
    ],
    "108_great_dane": [
        {"test": "Cardiac Exam", "test_ja": "\u5fc3\u81d3\u691c\u67fb", "purpose": "Screen for dilated cardiomyopathy"},
        {
            "test": "Hip Radiograph (PennHIP/OFA)",
            "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3",
            "purpose": "Screen for hip dysplasia",
        },
        {
            "test": "Thyroid Panel",
            "test_ja": "\u7532\u72b6\u817a\u30d1\u30cd\u30eb",
            "purpose": "Screen for hypothyroidism",
        },
        {
            "test": "Ophthalmologic Exam",
            "test_ja": "\u773c\u79d1\u691c\u67fb",
            "purpose": "Screen for entropion and cataracts",
        },
    ],
    "109_bernese_mountain_dog": [
        {
            "test": "Hip Radiograph (PennHIP/OFA)",
            "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3",
            "purpose": "Screen for hip dysplasia",
        },
        {
            "test": "Elbow Radiograph",
            "test_ja": "\u8098\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3",
            "purpose": "Screen for elbow dysplasia",
        },
        {
            "test": "Cancer Screening (Oncology Panel)",
            "test_ja": "\u816b\u760d\u30b9\u30af\u30ea\u30fc\u30cb\u30f3\u30b0",
            "purpose": "Early detection of histiocytic sarcoma",
        },
        {"test": "Cardiac Exam", "test_ja": "\u5fc3\u81d3\u691c\u67fb", "purpose": "Screen for aortic stenosis"},
        {
            "test": "vWD DNA Test",
            "test_ja": "vWD\u907a\u4f1d\u5b50\u691c\u67fb",
            "purpose": "Test for von Willebrand disease gene",
        },
    ],
    "110_cavalier_king_charles": [
        {"test": "Cardiac Exam", "test_ja": "\u5fc3\u81d3\u691c\u67fb", "purpose": "Screen for mitral valve disease"},
        {
            "test": "MRI (Syringomyelia)",
            "test_ja": "MRI\uff08\u810a\u9ac4\u7a7a\u6d1e\u75c7\uff09",
            "purpose": "Screen for Chiari malformation/syringomyelia",
        },
        {
            "test": "Ophthalmologic Exam",
            "test_ja": "\u773c\u79d1\u691c\u67fb",
            "purpose": "Screen for cataracts and retinal dysplasia",
        },
        {
            "test": "Platelet Count",
            "test_ja": "\u8840\u5c0f\u677f\u6570",
            "purpose": "Screen for macrothrombocytopenia",
        },
        {
            "test": "Patella Evaluation",
            "test_ja": "\u819d\u84cb\u9aa8\u8a55\u4fa1",
            "purpose": "Check for patellar luxation",
        },
    ],
    "112_cocker_spaniel": [
        {
            "test": "Ophthalmologic Exam",
            "test_ja": "\u773c\u79d1\u691c\u67fb",
            "purpose": "Screen for glaucoma, cataracts, and PRA",
        },
        {"test": "Ear Exam (Otoscopy)", "test_ja": "\u8033\u93e1\u691c\u67fb", "purpose": "Evaluate ear canal health"},
        {
            "test": "Thyroid Panel",
            "test_ja": "\u7532\u72b6\u817a\u30d1\u30cd\u30eb",
            "purpose": "Screen for hypothyroidism",
        },
        {
            "test": "Hip Radiograph (PennHIP/OFA)",
            "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3",
            "purpose": "Screen for hip dysplasia",
        },
        {
            "test": "Allergy Panel",
            "test_ja": "\u30a2\u30ec\u30eb\u30ae\u30fc\u30d1\u30cd\u30eb",
            "purpose": "Identify environmental or food allergens",
        },
    ],
    "113_springer_spaniel": [
        {
            "test": "Ophthalmologic Exam",
            "test_ja": "\u773c\u79d1\u691c\u67fb",
            "purpose": "Screen for PRA and retinal dysplasia",
        },
        {"test": "Ear Exam (Otoscopy)", "test_ja": "\u8033\u93e1\u691c\u67fb", "purpose": "Evaluate ear canal health"},
        {
            "test": "Hip Radiograph (PennHIP/OFA)",
            "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3",
            "purpose": "Screen for hip dysplasia",
        },
        {
            "test": "PFK DNA Test",
            "test_ja": "PFK\u907a\u4f1d\u5b50\u691c\u67fb",
            "purpose": "Test for phosphofructokinase deficiency",
        },
    ],
    "114_dachshund": [
        {
            "test": "Spine X-ray/CT",
            "test_ja": "\u810a\u690e\u30ec\u30f3\u30c8\u30b2\u30f3/CT",
            "purpose": "Screen for IVDD",
        },
        {
            "test": "Ophthalmologic Exam",
            "test_ja": "\u773c\u79d1\u691c\u67fb",
            "purpose": "Screen for PRA and cataracts",
        },
        {"test": "Cardiac Exam", "test_ja": "\u5fc3\u81d3\u691c\u67fb", "purpose": "Screen for mitral valve disease"},
        {
            "test": "Patella Evaluation",
            "test_ja": "\u819d\u84cb\u9aa8\u8a55\u4fa1",
            "purpose": "Check for patellar luxation",
        },
    ],
    "115_miniature_schnauzer": [
        {"test": "Lipid Panel", "test_ja": "\u8102\u8cea\u30d1\u30cd\u30eb", "purpose": "Screen for hyperlipidemia"},
        {"test": "Urinalysis", "test_ja": "\u5c3f\u691c\u67fb", "purpose": "Screen for urinary stones"},
        {
            "test": "Ophthalmologic Exam",
            "test_ja": "\u773c\u79d1\u691c\u67fb",
            "purpose": "Screen for cataracts and PRA",
        },
        {
            "test": "Pancreatitis Test (cPL)",
            "test_ja": "\u81b5\u708e\u691c\u67fb\uff08cPL\uff09",
            "purpose": "Screen for pancreatitis risk",
        },
        {
            "test": "Blood Glucose Test",
            "test_ja": "\u8840\u7cd6\u691c\u67fb",
            "purpose": "Screen for diabetes mellitus",
        },
    ],
    "116_shih_tzu": [
        {
            "test": "Brachycephalic Assessment",
            "test_ja": "\u77ed\u982d\u7a2e\u8a55\u4fa1",
            "purpose": "Evaluate airway obstruction severity",
        },
        {
            "test": "Ophthalmologic Exam",
            "test_ja": "\u773c\u79d1\u691c\u67fb",
            "purpose": "Screen for cataracts, dry eye, and proptosis",
        },
        {"test": "Kidney Panel", "test_ja": "\u814e\u81d3\u30d1\u30cd\u30eb", "purpose": "Screen for renal dysplasia"},
        {
            "test": "Patella Evaluation",
            "test_ja": "\u819d\u84cb\u9aa8\u8a55\u4fa1",
            "purpose": "Check for patellar luxation",
        },
    ],
    "117_maltese": [
        {
            "test": "Cardiac Exam",
            "test_ja": "\u5fc3\u81d3\u691c\u67fb",
            "purpose": "Screen for mitral valve disease and PDA",
        },
        {
            "test": "Bile Acids Test",
            "test_ja": "\u80c6\u6c41\u9178\u691c\u67fb",
            "purpose": "Screen for portosystemic shunt",
        },
        {
            "test": "Patella Evaluation",
            "test_ja": "\u819d\u84cb\u9aa8\u8a55\u4fa1",
            "purpose": "Check for patellar luxation",
        },
    ],
    "118_havanese": [
        {"test": "Cardiac Exam", "test_ja": "\u5fc3\u81d3\u691c\u67fb", "purpose": "Screen for mitral valve disease"},
        {"test": "Ophthalmologic Exam", "test_ja": "\u773c\u79d1\u691c\u67fb", "purpose": "Screen for cataracts"},
        {
            "test": "Patella Evaluation",
            "test_ja": "\u819d\u84cb\u9aa8\u8a55\u4fa1",
            "purpose": "Check for patellar luxation",
        },
        {
            "test": "Hip Radiograph (PennHIP/OFA)",
            "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3",
            "purpose": "Screen for Legg-Calve-Perthes disease",
        },
    ],
    "119_bichon_frise": [
        {
            "test": "Allergy Panel",
            "test_ja": "\u30a2\u30ec\u30eb\u30ae\u30fc\u30d1\u30cd\u30eb",
            "purpose": "Identify environmental or food allergens",
        },
        {"test": "Urinalysis", "test_ja": "\u5c3f\u691c\u67fb", "purpose": "Screen for bladder stones"},
        {
            "test": "Blood Glucose Test",
            "test_ja": "\u8840\u7cd6\u691c\u67fb",
            "purpose": "Screen for diabetes mellitus",
        },
        {
            "test": "Patella Evaluation",
            "test_ja": "\u819d\u84cb\u9aa8\u8a55\u4fa1",
            "purpose": "Check for patellar luxation",
        },
    ],
    "120_pomeranian": [
        {
            "test": "Cardiac Exam",
            "test_ja": "\u5fc3\u81d3\u691c\u67fb",
            "purpose": "Screen for patent ductus arteriosus",
        },
        {
            "test": "Patella Evaluation",
            "test_ja": "\u819d\u84cb\u9aa8\u8a55\u4fa1",
            "purpose": "Check for patellar luxation",
        },
        {
            "test": "Thyroid Panel",
            "test_ja": "\u7532\u72b6\u817a\u30d1\u30cd\u30eb",
            "purpose": "Screen for hypothyroidism",
        },
        {"test": "Tracheal Exam", "test_ja": "\u6c17\u7ba1\u691c\u67fb", "purpose": "Screen for collapsing trachea"},
    ],
    "121_shetland_sheepdog": [
        {"test": "Ophthalmologic Exam", "test_ja": "\u773c\u79d1\u691c\u67fb", "purpose": "Screen for CEA and PRA"},
        {
            "test": "MDR1 DNA Test",
            "test_ja": "MDR1\u907a\u4f1d\u5b50\u691c\u67fb",
            "purpose": "Test for multidrug resistance gene",
        },
        {
            "test": "Thyroid Panel",
            "test_ja": "\u7532\u72b6\u817a\u30d1\u30cd\u30eb",
            "purpose": "Screen for hypothyroidism",
        },
        {
            "test": "Hip Radiograph (PennHIP/OFA)",
            "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3",
            "purpose": "Screen for hip dysplasia",
        },
        {
            "test": "vWD DNA Test",
            "test_ja": "vWD\u907a\u4f1d\u5b50\u691c\u67fb",
            "purpose": "Test for von Willebrand disease gene",
        },
    ],
    "123_border_collie": [
        {
            "test": "Hip Radiograph (PennHIP/OFA)",
            "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3",
            "purpose": "Screen for hip dysplasia",
        },
        {"test": "Ophthalmologic Exam", "test_ja": "\u773c\u79d1\u691c\u67fb", "purpose": "Screen for CEA and PRA"},
        {
            "test": "CEA DNA Test",
            "test_ja": "CEA\u907a\u4f1d\u5b50\u691c\u67fb",
            "purpose": "Test for collie eye anomaly gene",
        },
        {
            "test": "TNS DNA Test",
            "test_ja": "TNS\u907a\u4f1d\u5b50\u691c\u67fb",
            "purpose": "Test for trapped neutrophil syndrome",
        },
        {
            "test": "MDR1 DNA Test",
            "test_ja": "MDR1\u907a\u4f1d\u5b50\u691c\u67fb",
            "purpose": "Test for multidrug resistance gene",
        },
    ],
    "124_australian_shepherd": [
        {
            "test": "Hip Radiograph (PennHIP/OFA)",
            "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3",
            "purpose": "Screen for hip dysplasia",
        },
        {
            "test": "Ophthalmologic Exam",
            "test_ja": "\u773c\u79d1\u691c\u67fb",
            "purpose": "Screen for cataracts and CEA",
        },
        {
            "test": "MDR1 DNA Test",
            "test_ja": "MDR1\u907a\u4f1d\u5b50\u691c\u67fb",
            "purpose": "Test for multidrug resistance gene",
        },
        {
            "test": "Elbow Radiograph",
            "test_ja": "\u8098\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3",
            "purpose": "Screen for elbow dysplasia",
        },
    ],
    "125_siberian_husky": [
        {
            "test": "Ophthalmologic Exam",
            "test_ja": "\u773c\u79d1\u691c\u67fb",
            "purpose": "Screen for cataracts and PRA",
        },
        {
            "test": "Hip Radiograph (PennHIP/OFA)",
            "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3",
            "purpose": "Screen for hip dysplasia",
        },
        {
            "test": "Thyroid Panel",
            "test_ja": "\u7532\u72b6\u817a\u30d1\u30cd\u30eb",
            "purpose": "Screen for hypothyroidism",
        },
    ],
    "126_alaskan_malamute": [
        {
            "test": "Hip Radiograph (PennHIP/OFA)",
            "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3",
            "purpose": "Screen for hip dysplasia",
        },
        {
            "test": "Ophthalmologic Exam",
            "test_ja": "\u773c\u79d1\u691c\u67fb",
            "purpose": "Screen for cataracts and day blindness",
        },
        {
            "test": "Thyroid Panel",
            "test_ja": "\u7532\u72b6\u817a\u30d1\u30cd\u30eb",
            "purpose": "Screen for hypothyroidism",
        },
        {
            "test": "Polyneuropathy DNA Test",
            "test_ja": "\u591a\u767a\u6027\u795e\u7d4c\u969c\u5bb3\u907a\u4f1d\u5b50\u691c\u67fb",
            "purpose": "Test for hereditary polyneuropathy gene",
        },
    ],
    "127_akita": [
        {
            "test": "Hip Radiograph (PennHIP/OFA)",
            "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3",
            "purpose": "Screen for hip dysplasia",
        },
        {
            "test": "Ophthalmologic Exam",
            "test_ja": "\u773c\u79d1\u691c\u67fb",
            "purpose": "Screen for PRA and glaucoma",
        },
        {
            "test": "Thyroid Panel",
            "test_ja": "\u7532\u72b6\u817a\u30d1\u30cd\u30eb",
            "purpose": "Screen for hypothyroidism",
        },
        {
            "test": "Autoimmune Panel",
            "test_ja": "\u81ea\u5df1\u514d\u75ab\u30d1\u30cd\u30eb",
            "purpose": "Screen for autoimmune conditions (VKH, IMHA)",
        },
    ],
    "128_samoyed": [
        {
            "test": "Hip Radiograph (PennHIP/OFA)",
            "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3",
            "purpose": "Screen for hip dysplasia",
        },
        {
            "test": "Ophthalmologic Exam",
            "test_ja": "\u773c\u79d1\u691c\u67fb",
            "purpose": "Screen for PRA and glaucoma",
        },
        {
            "test": "Blood Glucose Test",
            "test_ja": "\u8840\u7cd6\u691c\u67fb",
            "purpose": "Screen for diabetes mellitus",
        },
        {"test": "Cardiac Exam", "test_ja": "\u5fc3\u81d3\u691c\u67fb", "purpose": "Screen for pulmonic stenosis"},
    ],
    "129_newfoundland": [
        {
            "test": "Cardiac Exam",
            "test_ja": "\u5fc3\u81d3\u691c\u67fb",
            "purpose": "Screen for subvalvular aortic stenosis",
        },
        {
            "test": "Hip Radiograph (PennHIP/OFA)",
            "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3",
            "purpose": "Screen for hip dysplasia",
        },
        {
            "test": "Elbow Radiograph",
            "test_ja": "\u8098\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3",
            "purpose": "Screen for elbow dysplasia",
        },
        {
            "test": "Cystinuria DNA Test",
            "test_ja": "\u30b7\u30b9\u30c1\u30f3\u5c3f\u75c7\u907a\u4f1d\u5b50\u691c\u67fb",
            "purpose": "Test for cystinuria gene",
        },
    ],
    "130_saint_bernard": [
        {
            "test": "Hip Radiograph (PennHIP/OFA)",
            "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3",
            "purpose": "Screen for hip dysplasia",
        },
        {
            "test": "Elbow Radiograph",
            "test_ja": "\u8098\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3",
            "purpose": "Screen for elbow dysplasia",
        },
        {"test": "Cardiac Exam", "test_ja": "\u5fc3\u81d3\u691c\u67fb", "purpose": "Screen for dilated cardiomyopathy"},
        {
            "test": "Ophthalmologic Exam",
            "test_ja": "\u773c\u79d1\u691c\u67fb",
            "purpose": "Screen for entropion and ectropion",
        },
    ],
    "131_irish_setter": [
        {
            "test": "Hip Radiograph (PennHIP/OFA)",
            "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3",
            "purpose": "Screen for hip dysplasia",
        },
        {"test": "Ophthalmologic Exam", "test_ja": "\u773c\u79d1\u691c\u67fb", "purpose": "Screen for PRA"},
        {
            "test": "Thyroid Panel",
            "test_ja": "\u7532\u72b6\u817a\u30d1\u30cd\u30eb",
            "purpose": "Screen for hypothyroidism",
        },
        {
            "test": "CLAD DNA Test",
            "test_ja": "CLAD\u907a\u4f1d\u5b50\u691c\u67fb",
            "purpose": "Test for canine leukocyte adhesion deficiency gene",
        },
    ],
    "132_weimaraner": [
        {
            "test": "Hip Radiograph (PennHIP/OFA)",
            "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3",
            "purpose": "Screen for hip dysplasia",
        },
        {
            "test": "Ophthalmologic Exam",
            "test_ja": "\u773c\u79d1\u691c\u67fb",
            "purpose": "Screen for entropion and distichiasis",
        },
        {
            "test": "Thyroid Panel",
            "test_ja": "\u7532\u72b6\u817a\u30d1\u30cd\u30eb",
            "purpose": "Screen for hypothyroidism",
        },
        {
            "test": "HUU DNA Test",
            "test_ja": "HUU\u907a\u4f1d\u5b50\u691c\u67fb",
            "purpose": "Test for hyperuricosuria gene",
        },
    ],
    "133_vizsla": [
        {
            "test": "Hip Radiograph (PennHIP/OFA)",
            "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3",
            "purpose": "Screen for hip dysplasia",
        },
        {
            "test": "Ophthalmologic Exam",
            "test_ja": "\u773c\u79d1\u691c\u67fb",
            "purpose": "Screen for cataracts and PRA",
        },
        {
            "test": "Thyroid Panel",
            "test_ja": "\u7532\u72b6\u817a\u30d1\u30cd\u30eb",
            "purpose": "Screen for hypothyroidism",
        },
    ],
    "134_german_shorthaired_pointer": [
        {
            "test": "Hip Radiograph (PennHIP/OFA)",
            "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3",
            "purpose": "Screen for hip dysplasia",
        },
        {
            "test": "Ophthalmologic Exam",
            "test_ja": "\u773c\u79d1\u691c\u67fb",
            "purpose": "Screen for cone degeneration",
        },
        {"test": "Cardiac Exam", "test_ja": "\u5fc3\u81d3\u691c\u67fb", "purpose": "Screen for aortic stenosis"},
        {
            "test": "vWD DNA Test",
            "test_ja": "vWD\u907a\u4f1d\u5b50\u691c\u67fb",
            "purpose": "Test for von Willebrand disease gene",
        },
    ],
    "135_brittany": [
        {
            "test": "Hip Radiograph (PennHIP/OFA)",
            "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3",
            "purpose": "Screen for hip dysplasia",
        },
        {
            "test": "Thyroid Panel",
            "test_ja": "\u7532\u72b6\u817a\u30d1\u30cd\u30eb",
            "purpose": "Screen for hypothyroidism",
        },
        {
            "test": "Ophthalmologic Exam",
            "test_ja": "\u773c\u79d1\u691c\u67fb",
            "purpose": "Screen for cataracts and lens luxation",
        },
    ],
    "136_standard_poodle": [
        {
            "test": "Hip Radiograph (PennHIP/OFA)",
            "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3",
            "purpose": "Screen for hip dysplasia",
        },
        {
            "test": "Ophthalmologic Exam",
            "test_ja": "\u773c\u79d1\u691c\u67fb",
            "purpose": "Screen for PRA and cataracts",
        },
        {
            "test": "vWD DNA Test",
            "test_ja": "vWD\u907a\u4f1d\u5b50\u691c\u67fb",
            "purpose": "Test for von Willebrand disease gene",
        },
        {
            "test": "Addison's Baseline Cortisol",
            "test_ja": "\u30a2\u30b8\u30bd\u30f3\u75c5\u30b3\u30eb\u30c1\u30be\u30fc\u30eb\u57fa\u6e96\u691c\u67fb",
            "purpose": "Screen for Addison's disease",
        },
        {
            "test": "Neonatal Encephalopathy DNA Test",
            "test_ja": "NEwS\u907a\u4f1d\u5b50\u691c\u67fb",
            "purpose": "Test for neonatal encephalopathy gene",
        },
    ],
    "137_miniature_poodle": [
        {
            "test": "Ophthalmologic Exam",
            "test_ja": "\u773c\u79d1\u691c\u67fb",
            "purpose": "Screen for PRA and cataracts",
        },
        {
            "test": "Patella Evaluation",
            "test_ja": "\u819d\u84cb\u9aa8\u8a55\u4fa1",
            "purpose": "Check for patellar luxation",
        },
        {
            "test": "PRA DNA Test",
            "test_ja": "PRA\u907a\u4f1d\u5b50\u691c\u67fb",
            "purpose": "Test for progressive retinal atrophy gene",
        },
    ],
    "138_west_highland_white_terrier": [
        {
            "test": "Allergy Panel",
            "test_ja": "\u30a2\u30ec\u30eb\u30ae\u30fc\u30d1\u30cd\u30eb",
            "purpose": "Identify environmental or food allergens",
        },
        {
            "test": "Bile Acids Test",
            "test_ja": "\u80c6\u6c41\u9178\u691c\u67fb",
            "purpose": "Screen for copper hepatopathy",
        },
        {
            "test": "Patella Evaluation",
            "test_ja": "\u819d\u84cb\u9aa8\u8a55\u4fa1",
            "purpose": "Check for patellar luxation",
        },
        {
            "test": "CMO Screening",
            "test_ja": "CMO\u30b9\u30af\u30ea\u30fc\u30cb\u30f3\u30b0",
            "purpose": "Screen for craniomandibular osteopathy",
        },
    ],
    "139_scottish_terrier": [
        {"test": "Urinalysis", "test_ja": "\u5c3f\u691c\u67fb", "purpose": "Screen for bladder cancer and stones"},
        {
            "test": "vWD DNA Test",
            "test_ja": "vWD\u907a\u4f1d\u5b50\u691c\u67fb",
            "purpose": "Test for von Willebrand disease gene",
        },
        {
            "test": "Patella Evaluation",
            "test_ja": "\u819d\u84cb\u9aa8\u8a55\u4fa1",
            "purpose": "Check for patellar luxation",
        },
        {
            "test": "CMO Screening",
            "test_ja": "CMO\u30b9\u30af\u30ea\u30fc\u30cb\u30f3\u30b0",
            "purpose": "Screen for craniomandibular osteopathy",
        },
    ],
    "140_cairn_terrier": [
        {
            "test": "Allergy Panel",
            "test_ja": "\u30a2\u30ec\u30eb\u30ae\u30fc\u30d1\u30cd\u30eb",
            "purpose": "Identify environmental or food allergens",
        },
        {
            "test": "Bile Acids Test",
            "test_ja": "\u80c6\u6c41\u9178\u691c\u67fb",
            "purpose": "Screen for portosystemic shunt",
        },
        {
            "test": "Ophthalmologic Exam",
            "test_ja": "\u773c\u79d1\u691c\u67fb",
            "purpose": "Screen for cataracts and PRA",
        },
    ],
    "141_jack_russell_terrier": [
        {
            "test": "Ophthalmologic Exam",
            "test_ja": "\u773c\u79d1\u691c\u67fb",
            "purpose": "Screen for lens luxation and PRA",
        },
        {
            "test": "Patella Evaluation",
            "test_ja": "\u819d\u84cb\u9aa8\u8a55\u4fa1",
            "purpose": "Check for patellar luxation",
        },
        {
            "test": "Allergy Panel",
            "test_ja": "\u30a2\u30ec\u30eb\u30ae\u30fc\u30d1\u30cd\u30eb",
            "purpose": "Identify environmental or food allergens",
        },
        {"test": "Cardiac Exam", "test_ja": "\u5fc3\u81d3\u691c\u67fb", "purpose": "Baseline cardiac evaluation"},
    ],
    "142_staffordshire_bull_terrier": [
        {
            "test": "L2-HGA DNA Test",
            "test_ja": "L2-HGA\u907a\u4f1d\u5b50\u691c\u67fb",
            "purpose": "Test for L-2-hydroxyglutaric aciduria gene",
        },
        {
            "test": "HC DNA Test",
            "test_ja": "HC\u907a\u4f1d\u5b50\u691c\u67fb",
            "purpose": "Test for hereditary cataracts gene",
        },
        {
            "test": "Patella Evaluation",
            "test_ja": "\u819d\u84cb\u9aa8\u8a55\u4fa1",
            "purpose": "Check for patellar luxation",
        },
        {
            "test": "Allergy Panel",
            "test_ja": "\u30a2\u30ec\u30eb\u30ae\u30fc\u30d1\u30cd\u30eb",
            "purpose": "Identify environmental or food allergens",
        },
    ],
    "143_bull_terrier": [
        {"test": "Urinalysis", "test_ja": "\u5c3f\u691c\u67fb", "purpose": "Screen for hereditary nephritis"},
        {
            "test": "UPC Ratio",
            "test_ja": "\u5c3f\u86cb\u767d\u30af\u30ec\u30a2\u30c1\u30cb\u30f3\u6bd4",
            "purpose": "Monitor kidney protein loss",
        },
        {"test": "Cardiac Exam", "test_ja": "\u5fc3\u81d3\u691c\u67fb", "purpose": "Screen for mitral valve disease"},
        {
            "test": "Allergy Panel",
            "test_ja": "\u30a2\u30ec\u30eb\u30ae\u30fc\u30d1\u30cd\u30eb",
            "purpose": "Identify environmental or food allergens",
        },
    ],
    "144_airedale_terrier": [
        {
            "test": "Hip Radiograph (PennHIP/OFA)",
            "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3",
            "purpose": "Screen for hip dysplasia",
        },
        {"test": "Cardiac Exam", "test_ja": "\u5fc3\u81d3\u691c\u67fb", "purpose": "Baseline cardiac evaluation"},
        {
            "test": "Thyroid Panel",
            "test_ja": "\u7532\u72b6\u817a\u30d1\u30cd\u30eb",
            "purpose": "Screen for hypothyroidism",
        },
    ],
    "145_whippet": [
        {"test": "Cardiac Exam", "test_ja": "\u5fc3\u81d3\u691c\u67fb", "purpose": "Screen for mitral valve disease"},
        {
            "test": "Ophthalmologic Exam",
            "test_ja": "\u773c\u79d1\u691c\u67fb",
            "purpose": "Screen for cataracts and PRA",
        },
        {
            "test": "BFJE DNA Test",
            "test_ja": "BFJE\u907a\u4f1d\u5b50\u691c\u67fb",
            "purpose": "Test for Bally forelimb joint disease gene",
        },
    ],
    "146_italian_greyhound": [
        {
            "test": "Patella Evaluation",
            "test_ja": "\u819d\u84cb\u9aa8\u8a55\u4fa1",
            "purpose": "Check for patellar luxation",
        },
        {
            "test": "Ophthalmologic Exam",
            "test_ja": "\u773c\u79d1\u691c\u67fb",
            "purpose": "Screen for PRA and cataracts",
        },
        {
            "test": "Thyroid Panel",
            "test_ja": "\u7532\u72b6\u817a\u30d1\u30cd\u30eb",
            "purpose": "Screen for hypothyroidism",
        },
    ],
    "147_greyhound": [
        {"test": "Cardiac Exam", "test_ja": "\u5fc3\u81d3\u691c\u67fb", "purpose": "Baseline cardiac evaluation"},
        {
            "test": "CBC (Complete Blood Count)",
            "test_ja": "\u5168\u8840\u7403\u8a08\u7b97",
            "purpose": "Greyhound-specific reference ranges",
        },
        {
            "test": "Thyroid Panel",
            "test_ja": "\u7532\u72b6\u817a\u30d1\u30cd\u30eb",
            "purpose": "Screen for hypothyroidism (breed-specific ranges)",
        },
        {
            "test": "Ophthalmologic Exam",
            "test_ja": "\u773c\u79d1\u691c\u67fb",
            "purpose": "Screen for pannus and cataracts",
        },
    ],
    "148_basset_hound": [
        {"test": "Ear Exam (Otoscopy)", "test_ja": "\u8033\u93e1\u691c\u67fb", "purpose": "Evaluate ear canal health"},
        {
            "test": "Spine X-ray/CT",
            "test_ja": "\u810a\u690e\u30ec\u30f3\u30c8\u30b2\u30f3/CT",
            "purpose": "Screen for IVDD",
        },
        {
            "test": "Ophthalmologic Exam",
            "test_ja": "\u773c\u79d1\u691c\u67fb",
            "purpose": "Screen for glaucoma and ectropion",
        },
        {
            "test": "Thrombopathia DNA Test",
            "test_ja": "\u8840\u5c0f\u677f\u6a5f\u80fd\u7570\u5e38\u907a\u4f1d\u5b50\u691c\u67fb",
            "purpose": "Test for platelet function disorder gene",
        },
    ],
    "149_bloodhound": [
        {
            "test": "Hip Radiograph (PennHIP/OFA)",
            "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3",
            "purpose": "Screen for hip dysplasia",
        },
        {"test": "Ear Exam (Otoscopy)", "test_ja": "\u8033\u93e1\u691c\u67fb", "purpose": "Evaluate ear canal health"},
        {
            "test": "Ophthalmologic Exam",
            "test_ja": "\u773c\u79d1\u691c\u67fb",
            "purpose": "Screen for entropion and ectropion",
        },
        {"test": "Cardiac Exam", "test_ja": "\u5fc3\u81d3\u691c\u67fb", "purpose": "Baseline cardiac evaluation"},
    ],
    "150_dalmatian": [
        {
            "test": "HUU DNA Test",
            "test_ja": "HUU\u907a\u4f1d\u5b50\u691c\u67fb",
            "purpose": "Test for hyperuricosuria gene",
        },
        {"test": "Urinalysis", "test_ja": "\u5c3f\u691c\u67fb", "purpose": "Monitor urate crystal formation"},
        {"test": "BAER Test", "test_ja": "BAER\u8074\u899a\u691c\u67fb", "purpose": "Screen for congenital deafness"},
        {
            "test": "Ophthalmologic Exam",
            "test_ja": "\u773c\u79d1\u691c\u67fb",
            "purpose": "Screen for cataracts and iris sphincter dysplasia",
        },
    ],
}

# ---------------------------------------------------------------------------
# General advice templates
# ---------------------------------------------------------------------------
_ADVICE: dict[str, dict[str, str]] = {
    "emergency": {
        "en": (
            "EMERGENCY: One or more symptoms strongly suggest a "
            "life-threatening condition. Seek immediate veterinary "
            "emergency care. Do not wait."
        ),
        "ja": (
            "\u3010\u7dca\u6025\u3011\u4e00\u3064\u4ee5\u4e0a\u306e\u75c7\u72b6"
            "\u304c\u751f\u547d\u306b\u95a2\u308f\u308b\u6df1\u523b\u306a\u72b6"
            "\u614b\u3092\u793a\u5506\u3057\u3066\u3044\u307e\u3059\u3002\u76f4"
            "\u3061\u306b\u7dca\u6025\u52d5\u7269\u75c5\u9662\u3092\u53d7\u8a3a"
            "\u3057\u3066\u304f\u3060\u3055\u3044\u3002"
        ),
    },
    "high": {
        "en": (
            "Some symptoms indicate a potentially serious condition that "
            "requires prompt veterinary attention. Schedule an appointment "
            "as soon as possible, ideally within 24 hours."
        ),
        "ja": (
            "\u3044\u304f\u3064\u304b\u306e\u75c7\u72b6\u304c\u6df1\u523b\u306a"
            "\u72b6\u614b\u3092\u793a\u3057\u3066\u3044\u308b\u53ef\u80fd\u6027"
            "\u304c\u3042\u308a\u307e\u3059\u3002\u3067\u304d\u308b\u3060\u3051"
            "\u65e9\u304f\uff08\u7406\u60f3\u7684\u306b\u306f24\u6642\u9593\u4ee5"
            "\u5185\u306b\uff09\u52d5\u7269\u75c5\u9662\u3092\u53d7\u8a3a\u3057"
            "\u3066\u304f\u3060\u3055\u3044\u3002"
        ),
    },
    "moderate": {
        "en": (
            "The combination of symptoms suggests a condition that should "
            "be evaluated by a veterinarian. Schedule an appointment within "
            "the next few days."
        ),
        "ja": (
            "\u75c7\u72b6\u306e\u7d44\u307f\u5408\u308f\u305b\u304b\u3089\u3001"
            "\u7363\u533b\u5e2b\u306b\u3088\u308b\u8a3a\u5bdf\u304c\u5fc5\u8981"
            "\u3067\u3059\u3002\u6570\u65e5\u4ee5\u5185\u306b\u52d5\u7269\u75c5"
            "\u9662\u3092\u53d7\u8a3a\u3057\u3066\u304f\u3060\u3055\u3044\u3002"
        ),
    },
    "low": {
        "en": (
            "The reported symptoms may indicate a minor issue, but "
            "monitoring is advised. If symptoms persist or worsen, consult "
            "a veterinarian."
        ),
        "ja": (
            "\u5831\u544a\u3055\u308c\u305f\u75c7\u72b6\u306f\u8efd\u5ea6\u306e"
            "\u554f\u984c\u3092\u793a\u3057\u3066\u3044\u308b\u53ef\u80fd\u6027"
            "\u304c\u3042\u308a\u307e\u3059\u304c\u3001\u7d4c\u904e\u89b3\u5bdf"
            "\u3092\u304a\u52e7\u3081\u3057\u307e\u3059\u3002\u75c7\u72b6\u304c"
            "\u7d9a\u304f\u307e\u305f\u306f\u60aa\u5316\u3059\u308b\u5834\u5408"
            "\u306f\u3001\u7363\u533b\u5e2b\u306b\u3054\u76f8\u8ac7\u304f\u3060"
            "\u3055\u3044\u3002"
        ),
    },
}

# Priority ranking (higher value = higher priority)
_PRIORITY_RANK: dict[str, int] = {
    "optional": 0,
    "recommended": 1,
    "urgent": 2,
}

_LIKELIHOOD_TO_PRIORITY: dict[str, str] = {
    "high": "urgent",
    "moderate": "recommended",
    "low": "optional",
}


def _disease_detail_text(
    disease: dict[str, Any],
    field: str,
    *,
    fallback_description: str = "",
) -> str:
    """Return a non-empty disease detail string for API responses.

    Prefers Japanese content to avoid English template text in the UI.
    """
    ja_value = str(disease.get(f"{field}_ja") or "").strip()
    if ja_value:
        return ja_value

    value = str(disease.get(field) or "").strip()
    if value:
        return value

    if fallback_description:
        return fallback_description

    _field_labels_ja = {
        "description": "説明",
        "pathophysiology": "病態生理",
        "causes": "原因",
        "treatment": "治療",
        "prevention": "予防",
        "prognosis": "予後",
    }
    field_label = _field_labels_ja.get(field, field.replace("_", " "))
    return f"{field_label}の詳細情報はまだ登録されていません。"


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def analyze_symptoms(  # noqa: C901
    symptoms: list[str],
    *,
    breed: str | None = None,
    onset: str | None = None,
    age_years: float | None = None,
    lab_values: dict[str, float] | None = None,
    gender: str | None = None,
    vaccines: list[str] | None = None,
    vaccination_status: str | None = None,
    pain_score: int | None = None,
) -> dict:
    """Analyze a list of symptom IDs and return suspected diseases, tests,
    severity assessment, and general advice.

    Parameters
    ----------
    symptoms:
        List of symptom ID strings (e.g. ``["vomiting", "lethargy"]``).
        Unknown symptom IDs are silently ignored.
    breed:
        Optional breed ID string (e.g. ``"101_french_bulldog"``).  When
        provided and present in ``_BREED_DISEASE_RISK``, disease match
        scores are boosted by breed-specific risk multipliers.
    onset:
        Optional time-course indicator: ``"acute"`` (within 24h),
        ``"subacute"`` (days to ~1 week), or ``"chronic"`` (weeks/months).
        When provided, diseases whose typical onset pattern matches receive
        a score boost; mismatches receive a penalty.
    age_years:
        Optional age of the animal in years.  When provided, diseases with
        a known age predisposition matching the animal's life stage receive
        a score boost; clear mismatches receive a penalty.
    vaccines:
        Optional vaccine ID list (e.g. ``["core_5in1", "rabies"]``). When
        provided, diseases directly covered by those vaccine records are
        excluded from the differential diagnosis.
    vaccination_status:
        Optional vaccination status: ``"current"`` (up-to-date), ``"outdated"``
        (lapsed), or ``"none"`` (unvaccinated). When ``"current"``, vaccine-preventable
        diseases have confidence significantly reduced. Default ``None`` (no adjustment).

    Returns
    -------
    dict
        Analysis result containing ``suspected_diseases``,
        ``recommended_tests``, ``severity``, ``general_advice``,
        ``general_advice_ja``, ``breed_genetic_tests``,
        ``breed_risk_applied``, ``onset_applied``, ``age_applied``,
        ``lab_boost_applied``, and ``lab_values``.
    """
    symptom_set: set[str] = set(symptoms) & VALID_SYMPTOMS
    vaccine_list = [str(vaccine) for vaccine in vaccines or [] if vaccine]

    # Resolve age stage for predisposition lookup
    age_stage: str | None = None
    if age_years is not None:
        age_stage = _age_years_to_stage(age_years)

    # Pre-compute symptom pair boosts and import clinical weights
    from api.species.helpers import (
        _DEFAULT_SYMPTOM_WEIGHT,
        SYMPTOM_CLINICAL_WEIGHTS,
        SYMPTOM_PAIR_BOOST,
        _fuzzy_boost_lookup,
        compute_lab_boosts,
    )

    # Load extended symptom combinations
    try:
        from api.data.symptom_combinations import (
            EXTENDED_SYMPTOM_PAIR_BOOST as extended_symptom_pair_boost,  # noqa: N811
        )
        from api.data.symptom_combinations import (
            SYMPTOM_TRIPLE_BOOST as symptom_triple_boost,  # noqa: N811
        )
    except ImportError:
        extended_symptom_pair_boost = {}
        symptom_triple_boost = {}

    # Load clinical frequency data (symptom presentation rates by region)
    try:
        from api.data.clinical_frequency import CLINICAL_FREQUENCY as clinical_frequency  # noqa: N811
    except ImportError:
        clinical_frequency = {}

    # Load evidence-based scoring
    try:
        from api.ai.evidence_calculator import EvidenceScorer as evidence_scorer_cls  # noqa: N813
    except ImportError:
        evidence_scorer_cls = None

    # Load vaccination protection data
    try:
        from api.data.vaccination_protection import VaccinationStatusHandler as vaccination_handler_cls  # noqa: N813
    except ImportError:
        vaccination_handler_cls = None

    # Load vaccine-preventable diseases mapping
    vaccine_preventable: set[str] = set()
    if vaccine_list:
        try:
            from api.data.vaccine_mapping import get_preventable_diseases

            vaccine_preventable = get_preventable_diseases(vaccine_list)
        except ImportError:
            pass

    pair_boosts: dict[str, float] = {}
    all_pair_boosts = {**SYMPTOM_PAIR_BOOST, **extended_symptom_pair_boost}
    for pair, disease_boosts in all_pair_boosts.items():
        if pair.issubset(symptom_set):
            for disease_name, multiplier in disease_boosts.items():
                if disease_name not in pair_boosts or multiplier > pair_boosts[disease_name]:
                    pair_boosts[disease_name] = multiplier

    # Pre-compute triple boosts
    triple_boosts: dict[str, float] = {}
    if len(symptom_set) >= 3 and symptom_triple_boost:
        for triple, disease_boosts in symptom_triple_boost.items():
            if triple.issubset(symptom_set):
                for disease_name, multiplier in disease_boosts.items():
                    if disease_name not in triple_boosts or multiplier > triple_boosts[disease_name]:
                        triple_boosts[disease_name] = multiplier

    # Pre-compute lab value boosts
    lab_boosts: dict[str, float] = {}
    if lab_values:
        lab_boosts = compute_lab_boosts(lab_values, species="dog")

    # Load gender risk data
    try:
        from api.data.gender_prevalence import GENDER_RISK_MULTIPLIERS as gender_risk_multipliers  # noqa: N811
    except ImportError:
        gender_risk_multipliers = {}

    # Pre-compute gender risk for dog species
    gender_risk: dict[str, float] = {}
    if gender and gender_risk_multipliers:
        species_genders = gender_risk_multipliers.get("dog", {})
        for disease_name, gender_mults in species_genders.items():
            if gender in gender_mults:
                mult = gender_mults[gender]
                gender_risk[disease_name] = mult

    # -- 1. Score diseases --------------------------------------------------
    suspected: list[dict[str, Any]] = []
    for disease in _DISEASE_DB:
        disease_symptoms: set[str] = disease["symptoms"]
        matching: set[str] = symptom_set & disease_symptoms
        match_count: int = len(matching)
        total: int = len(disease_symptoms)

        if total == 0 or match_count == 0 or disease["name"] in vaccine_preventable:
            continue

        # Weighted coverage: 臨床的重要度で重み付け
        # 病態特異的な症状 (seizures=2.5 etc.) の一致は非特異的な症状より高スコア
        _w = SYMPTOM_CLINICAL_WEIGHTS
        _dw = _DEFAULT_SYMPTOM_WEIGHT
        matching_weight = sum(_w.get(s, _dw) for s in matching)
        total_weight = sum(_w.get(s, _dw) for s in disease_symptoms)
        coverage: float = matching_weight / total_weight if total_weight > 0 else 0.0
        # Weighted Jaccard: weighted intersection / weighted union
        union_symptoms = symptom_set | disease_symptoms
        union_weight = sum(_w.get(s, _dw) for s in union_symptoms)
        jaccard: float = matching_weight / union_weight if union_weight > 0 else 0.0
        # Composite score (same formula used in the frontend)
        raw_score: float = (jaccard * 0.4 + coverage * 0.6) * 100

        # 症状数による補正: 疾患の定義症状が少ない場合、カバー率が過大に
        # なるためペナルティを適用。定義症状が多い疾患は特異性が高いため
        # ボーナスを付与する。
        if total <= 2:
            symptom_count_factor = 0.75
        elif total <= 4:
            symptom_count_factor = 0.9
        elif total >= 8:
            symptom_count_factor = 1.1
        else:
            symptom_count_factor = 1.0

        # 一致症状が1つだけの場合はスコアを抑制（ノイズ除去）
        if match_count == 1:
            symptom_count_factor *= 0.6

        raw_score *= symptom_count_factor

        # Apply breed-specific risk multiplier (上限を制限)
        breed_multiplier = 1.0
        if breed and breed in _BREED_DISEASE_RISK:
            breed_multiplier = min(_BREED_DISEASE_RISK[breed].get(disease["name"], 1.0), 1.8)

        # Apply gender-specific risk multiplier (上限を制限)
        gender_multiplier = 1.0
        if gender and disease["name"] in gender_risk:
            mult = gender_risk[disease["name"]]
            # If multiplier is 0, disease doesn't apply to this gender
            if mult == 0.0:
                continue  # Skip this disease entirely
            gender_multiplier = min(mult, 1.8)

        # Apply onset (time-course) multiplier (緩和: ペナルティを軽減)
        onset_multiplier = 1.0
        if onset:
            disease_onsets = _DISEASE_ONSET.get(disease["name"])
            if disease_onsets:
                onset_multiplier = 1.15 if onset in disease_onsets else 0.85
            # If disease has no onset data, leave multiplier at 1.0

        # Apply age predisposition multiplier (緩和: ペナルティを軽減)
        age_multiplier = 1.0
        if age_stage:
            age_predisposition = _DISEASE_AGE_PREDISPOSITION.get(disease["name"])
            if age_predisposition:
                age_multiplier = 1.15 if age_stage in age_predisposition else 0.85
            # If disease has no age predisposition data, leave at 1.0

        # Apply symptom pair boost (上限を制限、部分一致)
        pair_multiplier = min(_fuzzy_boost_lookup(disease["name"], pair_boosts), 1.5)

        # Apply symptom triple boost (上限を制限、部分一致)
        triple_multiplier = min(_fuzzy_boost_lookup(disease["name"], triple_boosts), 2.0)

        # Apply lab value boost (上限を制限、部分一致)
        lab_multiplier = min(_fuzzy_boost_lookup(disease["name"], lab_boosts), 1.5)

        # Apply clinical frequency boost (matching symptoms that commonly present)
        clinical_frequency_multiplier = 1.0
        disease_frequency = clinical_frequency.get(disease["name"], {})
        if disease_frequency:
            frequency_values = [
                symptom_frequency.get("global_average")
                for symptom_id, symptom_frequency in disease_frequency.items()
                if symptom_id in matching
                and isinstance(symptom_frequency, dict)
                and isinstance(symptom_frequency.get("global_average"), (int, float))
            ]
            if frequency_values:
                avg_frequency = sum(frequency_values) / len(frequency_values)
                clinical_frequency_multiplier = min(1.0 + (avg_frequency * 0.4), 1.5)

        # Apply prevalence (base rate) multiplier — 有病率ベイズ補正
        prevalence_cat = _DISEASE_PREVALENCE.get(disease["name"])
        prevalence_multiplier = _PREVALENCE_MULTIPLIER.get(prevalence_cat, 1.0) if prevalence_cat else 1.0

        # 複合ブースト倍率の上限を設定（過度なインフレ防止）
        combined_boost = (
            breed_multiplier
            * gender_multiplier
            * onset_multiplier
            * age_multiplier
            * pair_multiplier
            * triple_multiplier
            * lab_multiplier
            * clinical_frequency_multiplier
            * prevalence_multiplier
        )
        combined_boost = min(combined_boost, 3.0)  # 最大3.0倍（トリプルで強いブースト可能）
        if combined_boost < 1.0:
            combined_boost = max(combined_boost, 0.6)  # ペナルティ下限0.6

        adjusted_score = min(raw_score * combined_boost, 100.0)

        # Determine likelihood from adjusted score
        if adjusted_score >= 55 or match_count >= 4:
            likelihood = "high"
        elif adjusted_score >= 30 or match_count >= 3:
            likelihood = "moderate"
        elif adjusted_score >= 15 or match_count >= 2:
            likelihood = "low"
        else:
            continue  # not enough evidence

        # Color class for frontend display (red / orange / yellow / green)
        match_percent = round(adjusted_score)
        if match_percent >= 70:
            color_class = "score-high"  # red
        elif match_percent >= 45:
            color_class = "score-moderate"  # orange
        elif match_percent >= 25:
            color_class = "score-low"  # yellow
        else:
            color_class = "score-minimal"  # green / grey

        # Get prevalence tier for this disease
        prevalence_tier = _DISEASE_PREVALENCE.get(disease["name"], "unknown")

        clinical_freq_data = {
            symptom_id: disease_frequency[symptom_id]
            for symptom_id in sorted(matching)
            if symptom_id in disease_frequency
        }

        suspected.append(
            {
                "name": disease["name"],
                "name_ja": disease["name_ja"],
                "likelihood": likelihood,
                "match_percent": match_percent,
                "color_class": color_class,
                "prevalence_tier": prevalence_tier,  # 罹患率カテゴリ: very_common, common, uncommon, rare, unknown
                "description": _disease_detail_text(
                    disease,
                    "description",
                    fallback_description="Detailed disease overview is not yet available.",
                ),
                "description_ja": disease.get("description_ja", ""),
                "pathophysiology": _disease_detail_text(disease, "pathophysiology"),
                "pathophysiology_ja": disease.get("pathophysiology_ja", ""),
                "causes": _disease_detail_text(disease, "causes"),
                "causes_ja": disease.get("causes_ja", ""),
                "treatment": _disease_detail_text(disease, "treatment"),
                "treatment_ja": disease.get("treatment_ja", ""),
                "prognosis": _disease_detail_text(disease, "prognosis"),
                "prognosis_ja": disease.get("prognosis_ja", ""),
                "prevention": _disease_detail_text(disease, "prevention"),
                "prevention_ja": disease.get("prevention_ja", ""),
                "transmission": disease.get("transmission", ""),
                "transmission_ja": disease.get("transmission_ja", ""),
                "clinical_signs": disease.get("clinical_signs", ""),
                "clinical_signs_ja": disease.get("clinical_signs_ja", ""),
                "diagnosis": disease.get("diagnosis", ""),
                "diagnosis_ja": disease.get("diagnosis_ja", ""),
                "urgency": disease.get("urgency", "moderate"),
                "recommended_tests": disease.get("recommended_tests", []),
                "matching_symptoms": sorted(matching),
                "match_count": match_count,
                "total_symptoms": total,
                "clinical_frequency_data": clinical_freq_data,
                # Scoring transparency (consumed by frontend)
                "scoring_detail": {
                    "weighted_recall": round(matching_weight / total_weight if total_weight > 0 else 0, 3),
                    "coverage": round(coverage, 3),
                    "cluster_boost": round(max(pair_multiplier, triple_multiplier), 3),
                    "negative_penalty": round(symptom_count_factor, 3),
                    "specificity_bonus": round(
                        sum(
                            0.06 if _w.get(s, _dw) >= 2.0 else (0.03 if _w.get(s, _dw) >= 1.5 else 0) for s in matching
                        ),
                        3,
                    ),
                    "prevalence_prior": round(prevalence_multiplier, 3),
                    "breed_multiplier": round(breed_multiplier, 3),
                    "age_multiplier": round(age_multiplier, 3),
                    "onset_multiplier": round(onset_multiplier, 3),
                },
                # Key symptoms of this disease that the user has NOT reported
                "missing_key_symptoms": sorted(s for s in (disease_symptoms - symptom_set) if _w.get(s, _dw) >= 1.5),
                # internal fields for later processing
                "_urgency": disease["urgency"],
                "_match_ratio": coverage,
            }
        )

    # Sort: Match quality tier first, then prevalence within each tier.
    # This prevents low-confidence common diseases (e.g. Periodontal Disease at 22%)
    # from outranking high-confidence matches (e.g. Resource Guarding at 65%).
    prevalence_priority = {"very_common": 0, "common": 1, "uncommon": 2, "rare": 3, "unknown": 4}

    def _match_quality_tier(d: dict) -> int:
        pct = d["match_percent"]
        cnt = d["match_count"]
        if pct >= 50 or cnt >= 3:
            return 0  # Strong match
        if pct >= 25 or cnt >= 2:
            return 1  # Moderate match
        return 2  # Weak match (single symptom, low confidence)

    suspected.sort(
        key=lambda d: (
            _match_quality_tier(d),  # Primary: match quality tier
            prevalence_priority.get(d["prevalence_tier"], 5),  # Secondary: prevalence within tier
            -d["match_percent"],  # Tertiary: match_percent (descending)
            -d["match_count"],  # Quaternary: match_count (descending)
        )
    )

    # -- 2. Determine overall severity --------------------------------------
    severity = _compute_severity(suspected)

    # -- 3. Collect recommended tests ---------------------------------------
    recommended_tests = _collect_tests(suspected)

    # -- 4. Clean internal fields from output -------------------------------
    for entry in suspected:
        del entry["_urgency"]
        del entry["_match_ratio"]

    # -- 5. Advice ----------------------------------------------------------
    advice_pair = _ADVICE.get(severity, _ADVICE["low"])

    # -- 6. Breed-specific genetic/screening tests --------------------------
    genetic_tests: list[dict[str, str]] = []
    if breed and breed in _BREED_GENETIC_TESTS:
        genetic_tests = _BREED_GENETIC_TESTS[breed]

    # -- 7. Collect symptom name lookup for bilingual display ----------------
    used_symptoms: set[str] = set()
    for entry in suspected:
        used_symptoms.update(entry["matching_symptoms"])
        used_symptoms.update(entry.get("missing_key_symptoms", []))
    symptom_names_lookup = {sid: _SYMPTOM_NAMES[sid] for sid in used_symptoms if sid in _SYMPTOM_NAMES}

    # Apply evidence-based confidence adjustment (Phase 4)
    # Use evidence as a direct boost multiplier to the existing match_percent
    if evidence_scorer_cls:
        from api.data.disease_evidence import EvidenceRetriever

        for disease in suspected:
            disease_name = disease["name"]
            original_match_percent = disease["match_percent"]

            # Get evidence multiplier for this disease
            evidence_multiplier = EvidenceRetriever.get_multiplier(disease_name, default=1.0)

            # Apply evidence boost as an additional multiplier (capped at 15% boost max)
            # This ensures evidence provides meaningful improvement without overwhelming existing scores
            evidence_boost_factor = 1.0 + (evidence_multiplier - 1.0) * 0.15
            adjusted_match_percent = int(original_match_percent * evidence_boost_factor)
            adjusted_match_percent = min(adjusted_match_percent, 100)  # Cap at 100

            # Store original score and evidence adjustment info
            disease["match_percent_before_evidence"] = original_match_percent
            disease["match_percent"] = adjusted_match_percent
            disease["evidence_multiplier"] = round(evidence_multiplier, 3)
            disease["evidence_boost_applied"] = round(evidence_boost_factor, 3)

    # Apply vaccination status adjustment (Phase 4 enhancement)
    # Reduce confidence for vaccine-preventable diseases if vaccinated
    vaccination_adjustment_applied = False
    if vaccination_handler_cls and vaccination_status:
        for disease in suspected:
            disease_name = disease["name"]
            original_match_percent = disease["match_percent"]

            # Apply vaccination adjustment
            adjusted_percent, adjustment_applied = vaccination_handler_cls.apply_vaccination_adjustment(
                disease_name, original_match_percent, vaccination_status
            )

            if adjustment_applied:
                disease["match_percent_before_vaccination"] = original_match_percent
                disease["match_percent"] = adjusted_percent
                disease["vaccination_adjustment_applied"] = True
                vaccination_adjustment_applied = True
            else:
                disease["vaccination_adjustment_applied"] = False

    suspected.sort(
        key=lambda d: (
            _match_quality_tier(d),
            prevalence_priority.get(d["prevalence_tier"], 5),
            -d["match_percent"],
            -d["match_count"],
        )
    )

    # Group diseases by prevalence tier for stepwise differential diagnosis
    # Phase 1: Common diseases (very_common + common)
    # Phase 2: Rare diseases (uncommon + rare + unknown)
    phase1_diseases = [d for d in suspected if d["prevalence_tier"] in ("very_common", "common")]
    phase2_diseases = [d for d in suspected if d["prevalence_tier"] in ("uncommon", "rare", "unknown")]

    return {
        "suspected_diseases": suspected,  # All diseases (sorted by prevalence)
        "suspected_diseases_by_phase": {  # Grouped for stepwise presentation
            "phase_1_common": phase1_diseases,
            "phase_2_rare": phase2_diseases,
        },
        "recommended_tests": recommended_tests,
        "severity": severity,
        "general_advice": advice_pair["en"],
        "general_advice_ja": advice_pair["ja"],
        "breed_genetic_tests": genetic_tests,
        "breed_risk_applied": breed is not None and breed in _BREED_DISEASE_RISK,
        "gender_risk_applied": len(gender_risk) > 0,
        "gender": gender,
        "onset_applied": onset is not None,
        "onset": onset,
        "age_applied": age_years is not None,
        "age_years": age_years,
        "age_stage": age_stage,
        "lab_boost_applied": len(lab_boosts) > 0,
        "lab_values": lab_values,
        "vaccines_applied": len(vaccine_list) > 0,
        "vaccines": vaccine_list,
        "vaccine_preventable_excluded": sorted(vaccine_preventable),
        "vaccination_status": vaccination_status,
        "vaccination_adjustment_applied": vaccination_adjustment_applied,
        "symptom_names": symptom_names_lookup,
        "pain_score": pain_score,
    }


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _compute_severity(suspected: list[dict[str, Any]]) -> str:
    """Derive the overall severity level from the list of suspected diseases.

    Rules (evaluated in order, first match wins):
    - Any EMERGENCY disease at "high" likelihood -> "emergency"
    - Any URGENT / HIGH disease at "high" or "moderate" likelihood,
      or any EMERGENCY disease at "moderate" likelihood -> "high"
    - Any disease at "high" likelihood -> "moderate"
    - Otherwise -> "low"
    """
    has_high = False
    for d in suspected:
        urgency = d["_urgency"]
        likelihood = d["likelihood"]

        if urgency == "emergency" and likelihood == "high":
            return "emergency"
        if urgency in ("urgent", "high", "emergency") and likelihood in ("high", "moderate"):
            return "high"
        if likelihood == "high":
            has_high = True

    return "moderate" if has_high else "low"


def _collect_tests(suspected: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Build a deduplicated list of recommended diagnostic tests based on the
    suspected diseases, assigning each test the highest applicable priority.
    """
    # Map test name -> best priority seen so far and related disease names
    test_priority: dict[str, str] = {}
    test_related: dict[str, set[str]] = {}

    suspected_names: set[str] = {d["name"] for d in suspected}
    disease_likelihood: dict[str, str] = {d["name"]: d["likelihood"] for d in suspected}

    for test in _TEST_DB:
        # Which suspected diseases does this test relate to?
        overlap: set[str] = test["related_diseases"] & suspected_names
        if not overlap:
            continue

        # Determine priority from the highest-likelihood related disease
        best_priority = "optional"
        for disease_name in overlap:
            candidate_priority = _LIKELIHOOD_TO_PRIORITY[disease_likelihood[disease_name]]
            if _PRIORITY_RANK[candidate_priority] > _PRIORITY_RANK[best_priority]:
                best_priority = candidate_priority

        test_name = test["name"]
        if test_name in test_priority:
            # Keep the higher priority
            if _PRIORITY_RANK[best_priority] > _PRIORITY_RANK[test_priority[test_name]]:
                test_priority[test_name] = best_priority
            test_related[test_name] |= overlap
        else:
            test_priority[test_name] = best_priority
            test_related[test_name] = set(overlap)

    # Build output sorted by priority (urgent first) then alphabetical
    results: list[dict[str, Any]] = []
    for test in _TEST_DB:
        name = test["name"]
        if name not in test_priority:
            continue
        results.append(
            {
                "name": name,
                "name_ja": test["name_ja"],
                "purpose": test["purpose"],
                "priority": test_priority[name],
                "related_diseases": sorted(test_related[name]),
            }
        )

    results.sort(key=lambda t: (-_PRIORITY_RANK[t["priority"]], t["name"]))
    return results
