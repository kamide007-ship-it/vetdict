"""
Symptom Checker Module for VetDict.

Maps dog symptoms to suspected diseases and recommended diagnostic tests.
Provides structured analysis output with severity assessment, Japanese
localization, and prioritized test recommendations.
"""

from __future__ import annotations

from typing import Any

# ---------------------------------------------------------------------------
# Symptom ID catalogue (for reference / validation)
# ---------------------------------------------------------------------------
VALID_SYMPTOMS: set[str] = {
    # General
    "lethargy", "fever", "weight_loss", "weight_gain", "appetite_loss",
    "appetite_increase", "excessive_thirst", "excessive_urination",
    # Digestive
    "vomiting", "diarrhea", "constipation", "bloody_stool",
    "bloated_abdomen", "excessive_gas", "regurgitation",
    "vomiting_after_drinking", "drooling", "abdominal_pain",
    "dehydration",
    # Respiratory
    "coughing", "sneezing", "nasal_discharge", "difficulty_breathing",
    "rapid_breathing", "reverse_sneezing", "snoring",
    # Eyes / Ears
    "eye_redness", "eye_discharge", "squinting", "ear_scratching",
    "ear_odor", "head_tilting",
    # Skin / Coat
    "itching", "hair_loss", "skin_redness", "lumps", "dry_skin",
    "hot_spots",
    # Musculoskeletal
    "limping_fl", "limping_fr", "limping_rl", "limping_rr", "stiffness",
    "reluctance_move", "swollen_joints", "pain_on_touch",
    # Behavioral
    "aggression_change", "anxiety", "excessive_panting", "hiding",
    "circling", "seizures",
    # Urinary / Reproductive
    "straining_urinate", "blood_urine", "incontinence",
    "genital_discharge",
    # Additional
    "swelling", "collapse", "ear_discharge", "head_shaking",
    "skin_lesions",
}

# Symptom ID -> bilingual name mapping (used for display in results)
_SYMPTOM_NAMES: dict[str, dict[str, str]] = {
    "lethargy": {"ja": "無気力", "en": "Lethargy"},
    "fever": {"ja": "発熱", "en": "Fever"},
    "weight_loss": {"ja": "体重減少", "en": "Weight Loss"},
    "weight_gain": {"ja": "体重増加", "en": "Weight Gain"},
    "appetite_loss": {"ja": "食欲不振", "en": "Appetite Loss"},
    "appetite_increase": {"ja": "食欲増進", "en": "Appetite Increase"},
    "excessive_thirst": {"ja": "多飲", "en": "Excessive Thirst"},
    "excessive_urination": {"ja": "頻尿", "en": "Excessive Urination"},
    "vomiting": {"ja": "嘔吐", "en": "Vomiting"},
    "diarrhea": {"ja": "下痢", "en": "Diarrhea"},
    "constipation": {"ja": "便秘", "en": "Constipation"},
    "bloody_stool": {"ja": "血便", "en": "Bloody Stool"},
    "bloated_abdomen": {"ja": "腹部膨満", "en": "Bloated Abdomen"},
    "excessive_gas": {"ja": "過度のガス", "en": "Excessive Gas"},
    "regurgitation": {"ja": "吐出", "en": "Regurgitation"},
    "vomiting_after_drinking": {"ja": "飲水後嘔吐", "en": "Vomiting After Drinking"},
    "drooling": {"ja": "よだれ・流涎", "en": "Drooling / Hypersalivation"},
    "abdominal_pain": {"ja": "腹痛", "en": "Abdominal Pain"},
    "dehydration": {"ja": "脱水", "en": "Dehydration"},
    "coughing": {"ja": "咳", "en": "Coughing"},
    "sneezing": {"ja": "くしゃみ", "en": "Sneezing"},
    "nasal_discharge": {"ja": "鼻水", "en": "Nasal Discharge"},
    "difficulty_breathing": {"ja": "呼吸困難", "en": "Difficulty Breathing"},
    "rapid_breathing": {"ja": "頻呼吸", "en": "Rapid Breathing"},
    "reverse_sneezing": {"ja": "逆くしゃみ", "en": "Reverse Sneezing"},
    "snoring": {"ja": "いびき", "en": "Snoring"},
    "eye_redness": {"ja": "目の充血", "en": "Eye Redness"},
    "eye_discharge": {"ja": "目やに", "en": "Eye Discharge"},
    "squinting": {"ja": "目を細める", "en": "Squinting"},
    "ear_scratching": {"ja": "耳を掻く", "en": "Ear Scratching"},
    "ear_odor": {"ja": "耳の悪臭", "en": "Ear Odor"},
    "head_tilting": {"ja": "首の傾き", "en": "Head Tilting"},
    "itching": {"ja": "かゆみ", "en": "Itching"},
    "hair_loss": {"ja": "脱毛", "en": "Hair Loss"},
    "skin_redness": {"ja": "皮膚の赤み", "en": "Skin Redness"},
    "lumps": {"ja": "しこり・腫瘤", "en": "Lumps"},
    "dry_skin": {"ja": "乾燥肌", "en": "Dry Skin"},
    "hot_spots": {"ja": "ホットスポット", "en": "Hot Spots"},
    "limping_fl": {"ja": "跛行（左前肢）", "en": "Limping (Front Left)"},
    "limping_fr": {"ja": "跛行（右前肢）", "en": "Limping (Front Right)"},
    "limping_rl": {"ja": "跛行（左後肢）", "en": "Limping (Rear Left)"},
    "limping_rr": {"ja": "跛行（右後肢）", "en": "Limping (Rear Right)"},
    "stiffness": {"ja": "こわばり", "en": "Stiffness"},
    "reluctance_move": {"ja": "動きたがらない", "en": "Reluctance to Move"},
    "swollen_joints": {"ja": "関節の腫れ", "en": "Swollen Joints"},
    "pain_on_touch": {"ja": "触ると痛がる", "en": "Pain on Touch"},
    "aggression_change": {"ja": "攻撃性の変化", "en": "Aggression Change"},
    "anxiety": {"ja": "不安行動", "en": "Anxiety"},
    "excessive_panting": {"ja": "過度のパンティング", "en": "Excessive Panting"},
    "hiding": {"ja": "隠れる", "en": "Hiding"},
    "circling": {"ja": "旋回行動", "en": "Circling"},
    "seizures": {"ja": "痙攣", "en": "Seizures"},
    "straining_urinate": {"ja": "排尿困難", "en": "Straining to Urinate"},
    "blood_urine": {"ja": "血尿", "en": "Blood in Urine"},
    "incontinence": {"ja": "尿失禁", "en": "Incontinence"},
    "genital_discharge": {"ja": "生殖器分泌物", "en": "Genital Discharge"},
    "swelling": {"ja": "腫れ・浮腫", "en": "Swelling / Edema"},
    "collapse": {"ja": "虚脱・失神", "en": "Collapse / Fainting"},
    "ear_discharge": {"ja": "耳だれ", "en": "Ear Discharge"},
    "head_shaking": {"ja": "頭を振る", "en": "Head Shaking"},
    "skin_lesions": {"ja": "皮膚病変", "en": "Skin Lesions"},
}

# Convenience group used by diseases that accept *any* limping symptom.
_ANY_LIMPING = {"limping_fl", "limping_fr", "limping_rl", "limping_rr"}

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
        ]
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
        ]
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
        ]
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
            {"ja": "開口呼吸", "en": "Open-mouth breathing", "symptom_ids": ["difficulty_breathing", "excessive_panting"]},
            {"ja": "呼吸が速い", "en": "Rapid breathing", "symptom_ids": ["rapid_breathing"]},
            {"ja": "呼吸が遅い", "en": "Slow breathing", "symptom_ids": ["difficulty_breathing"]},
        ]
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
        ]
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
        ]
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
        ]
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
        ]
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
        ]
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
        ]
    },
}

# Keywords that indicate abnormal/alert status (for red highlighting in UI/PDF)
ABNORMAL_KEYWORDS: list[str] = [
    "嘔吐", "下痢", "血便", "血尿", "出血", "けいれん",
    "呼吸困難", "意識障害", "麻痺", "発熱", "異物誤飲",
    "ぐったり", "立てない", "開口呼吸", "尿が出ない",
    "腹痛", "痛がる", "黒色便", "鼻血",
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
    "Canine Parvovirus":                        {"acute"},
    "Canine Distemper":                          {"acute", "subacute"},
    "Kennel Cough (Bordetella)":                 {"acute", "subacute"},
    "Canine Influenza (CIV)":                    {"acute"},
    "Leptospirosis":                             {"acute", "subacute"},
    "Canine Infectious Hepatitis":               {"acute"},
    "Canine Coronavirus (Enteric)":              {"acute"},
    "Rabies":                                    {"acute", "subacute"},
    "Canine Herpesvirus (CHV)":                  {"acute"},
    "Canine Papillomatosis":                     {"subacute", "chronic"},
    "Brucellosis":                               {"subacute", "chronic"},
    "Rocky Mountain Spotted Fever":              {"acute"},
    "Tetanus":                                   {"acute", "subacute"},
    "Nocardiosis":                               {"chronic"},
    "Actinomycosis":                             {"chronic"},
    # -- Parasitic --
    "Giardiasis":                                {"subacute", "chronic"},
    "Ehrlichiosis":                              {"acute", "chronic"},
    "Anaplasmosis":                              {"acute"},
    "Coccidiosis":                               {"acute", "subacute"},
    "Babesiosis":                                {"acute"},
    "Intestinal Parasites":                      {"subacute", "chronic"},
    "Heartworm Disease":                         {"chronic"},
    "Lyme Disease":                              {"subacute", "chronic"},
    "Leishmaniasis":                             {"chronic"},
    "Neosporosis":                               {"acute", "subacute"},
    "Toxoplasmosis":                             {"subacute"},
    "Hepatozoonosis":                            {"chronic"},
    "Roundworm Infection (Toxocara)":            {"subacute", "chronic"},
    "Hookworm Infection":                        {"subacute", "chronic"},
    "Whipworm Infection (Trichuris)":            {"chronic"},
    "Tapeworm Infection (Dipylidium/Echinococcus)": {"chronic"},
    "Ear Mite Infestation (Otodectes)":          {"subacute", "chronic"},
    "Flea Allergy Dermatitis":                   {"acute", "chronic"},
    "Sarcoptic Mange (Scabies)":                 {"subacute"},
    "Cheyletiellosis (Walking Dandruff)":        {"subacute", "chronic"},
    # -- Fungal --
    "Fungal Infection (Ringworm)":               {"subacute", "chronic"},
    "Blastomycosis":                             {"subacute", "chronic"},
    "Histoplasmosis":                            {"subacute", "chronic"},
    "Coccidioidomycosis (Valley Fever)":         {"subacute", "chronic"},
    "Cryptococcosis":                            {"subacute", "chronic"},
    "Aspergillosis":                             {"chronic"},
    "Sporotrichosis":                            {"subacute", "chronic"},
    # -- GI --
    "Gastric Dilatation-Volvulus (GDV/Bloat)":   {"acute"},
    "Pancreatitis":                              {"acute", "chronic"},
    "Gastroenteritis":                           {"acute"},
    "Hemorrhagic Gastroenteritis (HGE)":         {"acute"},
    "Foreign Body Obstruction":                  {"acute"},
    "Inflammatory Bowel Disease (IBD)":          {"chronic"},
    "Megaesophagus":                             {"chronic"},
    "Exocrine Pancreatic Insufficiency (EPI)":   {"chronic"},
    "Colitis":                                   {"acute", "chronic"},
    "Portosystemic Shunt (Liver Shunt)":         {"chronic"},
    "Gastric Ulcer":                             {"acute", "chronic"},
    "Esophagitis":                               {"acute", "subacute"},
    "Protein-Losing Enteropathy (PLE)":          {"chronic"},
    "Mesenteric Volvulus":                       {"acute"},
    "Rectal Prolapse":                           {"acute", "chronic"},
    "Anal Sac Disease":                          {"subacute", "chronic"},
    "Intestinal Intussusception":                {"acute"},
    "Megacolon":                                 {"chronic"},
    "Gastric Foreign Body":                      {"acute"},
    # -- Endocrine --
    "Hypothyroidism":                            {"chronic"},
    "Hyperthyroidism":                           {"chronic"},
    "Cushing's Disease":                         {"chronic"},
    "Addison's Disease":                         {"acute", "chronic"},
    "Diabetes Mellitus":                         {"chronic"},
    "Diabetes Insipidus":                        {"chronic"},
    "Pheochromocytoma":                          {"acute", "chronic"},
    "Growth Hormone-Responsive Dermatosis":      {"chronic"},
    "Insulinoma":                                {"acute", "chronic"},
    "Hyperparathyroidism":                       {"chronic"},
    # -- Urinary --
    "Urinary Tract Infection":                   {"acute", "subacute"},
    "Bladder Stones":                            {"subacute", "chronic"},
    "Kidney Disease (CKD)":                      {"chronic"},
    "Fanconi Syndrome":                          {"chronic"},
    "Ectopic Ureter":                            {"chronic"},
    "Glomerulonephritis":                        {"chronic"},
    "Pyelonephritis":                            {"acute", "subacute"},
    "Urethral Obstruction":                      {"acute"},
    "Cystinuria":                                {"chronic"},
    # -- Hepatic --
    "Liver Disease":                             {"subacute", "chronic"},
    "Copper Storage Disease":                    {"chronic"},
    "Portosystemic Shunt (Congenital)":          {"chronic"},
    "Hepatocellular Carcinoma":                  {"chronic"},
    # -- Cardiac --
    "Heart Disease/CHF":                         {"chronic"},
    "Dilated Cardiomyopathy (DCM)":              {"chronic"},
    "Patent Ductus Arteriosus (PDA)":            {"chronic"},
    "Aortic Stenosis":                           {"chronic"},
    "Pulmonic Stenosis":                         {"chronic"},
    "Pericardial Effusion":                      {"acute", "chronic"},
    "Mitral Valve Disease (MMVD)":               {"chronic"},
    "Sick Sinus Syndrome":                       {"chronic"},
    "Ventricular Septal Defect (VSD)":           {"chronic"},
    "Atrial Fibrillation":                       {"acute", "chronic"},
    "Infective Endocarditis":                    {"subacute", "chronic"},
    "Myocarditis":                               {"acute", "subacute"},
    "Chemodectoma (Heart Base Tumor)":           {"chronic"},
    # -- Respiratory --
    "Brachycephalic Airway Syndrome":            {"chronic"},
    "Tracheal Collapse":                         {"chronic"},
    "Laryngeal Paralysis":                       {"chronic"},
    "Pneumonia":                                 {"acute", "subacute"},
    "Aspiration Pneumonia":                      {"acute"},
    "Pleural Effusion":                          {"subacute", "chronic"},
    "Pulmonary Hypertension":                    {"chronic"},
    "Pulmonary Fibrosis":                        {"chronic"},
    "Nasal Tumor":                               {"chronic"},
    "Lung Lobe Torsion":                         {"acute"},
    "Nasal Adenocarcinoma":                      {"chronic"},
    "Chylothorax":                               {"subacute", "chronic"},
    # -- Dermatological --
    "Allergic Dermatitis":                       {"subacute", "chronic"},
    "Mange (Demodex/Sarcoptes)":                 {"subacute", "chronic"},
    "Pyoderma":                                  {"acute", "subacute"},
    "Sebaceous Adenitis":                        {"chronic"},
    "Pemphigus":                                 {"subacute", "chronic"},
    "Alopecia X":                                {"chronic"},
    "Acral Lick Dermatitis":                     {"chronic"},
    "Discoid Lupus Erythematosus (DLE)":         {"chronic"},
    "Follicular Dysplasia":                      {"chronic"},
    "Dermoid Sinus":                             {"chronic"},
    "Zinc-Responsive Dermatosis":                {"subacute", "chronic"},
    "Malassezia Dermatitis":                     {"subacute", "chronic"},
    "Systemic Lupus Erythematosus (SLE)":        {"subacute", "chronic"},
    "Interdigital Cyst (Furuncle)":              {"acute", "subacute"},
    "Seborrhea":                                 {"chronic"},
    "Cutaneous Histiocytoma":                    {"subacute"},
    # -- Ophthalmologic --
    "Eye Infection (Conjunctivitis)":            {"acute", "subacute"},
    "Glaucoma":                                  {"acute", "chronic"},
    "Cherry Eye":                                {"acute"},
    "Keratoconjunctivitis Sicca (Dry Eye)":      {"chronic"},
    "Entropion":                                 {"chronic"},
    "Corneal Ulcer":                             {"acute"},
    "Lens Luxation":                             {"acute"},
    "Retinal Detachment":                        {"acute"},
    "Ectropion":                                 {"chronic"},
    "Distichiasis":                              {"chronic"},
    "Nuclear Sclerosis":                         {"chronic"},
    "Retinal Dysplasia":                         {"chronic"},
    "Pannus (Chronic Superficial Keratitis)":    {"chronic"},
    "Uveitis":                                   {"acute", "subacute"},
    "Corneal Dystrophy":                         {"chronic"},
    "Collie Eye Anomaly (CEA)":                  {"chronic"},
    "Horner's Syndrome":                         {"acute", "subacute"},
    "Sudden Acquired Retinal Degeneration (SARDS)": {"acute"},
    "Progressive Retinal Atrophy (PRA)":         {"chronic"},
    "Cataracts":                                 {"chronic"},
    # -- Ear --
    "Ear Infection (Otitis)":                    {"acute", "subacute", "chronic"},
    "Foreign Body in Ear":                       {"acute"},
    "Aural Hematoma":                            {"acute"},
    # -- Musculoskeletal --
    "Osteoarthritis":                            {"chronic"},
    "Cruciate Ligament Injury":                  {"acute"},
    "Hip Dysplasia":                             {"chronic"},
    "Intervertebral Disc Disease (IVDD)":        {"acute", "chronic"},
    "Elbow Dysplasia":                           {"chronic"},
    "Legg-Calvé-Perthes Disease":                {"subacute", "chronic"},
    "Osteochondritis Dissecans (OCD)":           {"subacute", "chronic"},
    "Panosteitis":                               {"subacute"},
    "Hypertrophic Osteodystrophy (HOD)":         {"acute", "subacute"},
    "Patellar Luxation":                         {"acute", "chronic"},
    "Spondylosis Deformans":                     {"chronic"},
    "Masticatory Muscle Myositis":               {"acute", "subacute"},
    "Craniomandibular Osteopathy":               {"subacute"},
    "Immune-Mediated Polyarthritis (IMPA)":      {"acute", "subacute"},
    "Luxating Shoulder":                         {"acute", "chronic"},
    "Hypertrophic Osteopathy":                   {"subacute", "chronic"},
    # -- Neurological --
    "Epilepsy":                                  {"acute"},
    "Vestibular Disease":                        {"acute"},
    "Wobbler Syndrome":                          {"subacute", "chronic"},
    "Hydrocephalus":                             {"chronic"},
    "Syringomyelia (Chiari Malformation)":       {"chronic"},
    "Cognitive Dysfunction Syndrome (CDS)":      {"chronic"},
    "Myasthenia Gravis":                         {"subacute", "chronic"},
    "Granulomatous Meningoencephalitis (GME)":   {"acute", "subacute"},
    "Degenerative Myelopathy (DM)":              {"chronic"},
    "Cerebellar Hypoplasia":                     {"chronic"},
    "Tick Paralysis":                            {"acute", "subacute"},
    "Fibrocartilaginous Embolism (FCE)":         {"acute"},
    "Canine Distemper Encephalitis":             {"subacute"},
    "Scotty Cramp":                              {"acute"},
    "Cauda Equina Syndrome (Lumbosacral Stenosis)": {"chronic"},
    "Brain Tumor":                               {"subacute", "chronic"},
    # -- Oncology --
    "Cancer/Neoplasia":                          {"chronic"},
    "Hemangiosarcoma":                           {"acute", "chronic"},
    "Lymphoma":                                  {"subacute", "chronic"},
    "Osteosarcoma":                              {"subacute", "chronic"},
    "Mast Cell Tumor":                           {"subacute", "chronic"},
    "Melanoma":                                  {"chronic"},
    "Squamous Cell Carcinoma":                   {"chronic"},
    "Mammary Tumor":                             {"chronic"},
    "Transitional Cell Carcinoma":               {"chronic"},
    "Histiocytic Sarcoma":                       {"subacute", "chronic"},
    "Fibrosarcoma":                              {"chronic"},
    "Anal Sac Adenocarcinoma":                   {"chronic"},
    "Insulinoma (Pancreatic Beta Cell Tumor)":   {"subacute", "chronic"},
    "Thyroid Carcinoma":                         {"chronic"},
    "Perianal Adenoma":                          {"chronic"},
    "Soft Tissue Sarcoma":                       {"chronic"},
    "Lipoma":                                    {"chronic"},
    "Plasmacytoma":                              {"subacute", "chronic"},
    "Oral Melanoma":                             {"chronic"},
    "Epulis (Gingival Mass)":                    {"chronic"},
    # -- Reproductive --
    "Pyometra":                                  {"acute", "subacute"},
    "Prostate Disease":                          {"chronic"},
    "Cryptorchidism":                            {"chronic"},
    "Mastitis":                                  {"acute"},
    "Eclampsia (Milk Fever)":                    {"acute"},
    "Benign Prostatic Hyperplasia (BPH)":        {"chronic"},
    "Vaginitis":                                 {"subacute", "chronic"},
    "Testicular Tumor":                          {"chronic"},
    "Paraphimosis":                              {"acute"},
    "Dystocia":                                  {"acute"},
    # -- Hematological --
    "Immune-Mediated Hemolytic Anemia":          {"acute", "subacute"},
    "Thrombocytopenia":                          {"acute", "subacute"},
    "Hemophilia A":                              {"acute"},
    "Autoimmune Thrombocytopenia (ITP)":         {"acute", "subacute"},
    "von Willebrand Disease":                    {"acute"},
    "Exercise-Induced Collapse (EIC)":           {"acute"},
    "Disseminated Intravascular Coagulation (DIC)": {"acute"},
    "Anemia of Chronic Disease":                 {"chronic"},
    "Evan's Syndrome":                           {"acute", "subacute"},
    "Hemolytic Uremic Syndrome":                 {"acute"},
    # -- Toxicology --
    "Chocolate Toxicosis":                       {"acute"},
    "Grape/Raisin Toxicosis":                    {"acute"},
    "Xylitol Poisoning":                         {"acute"},
    "NSAID Toxicosis":                           {"acute"},
    "Rodenticide Poisoning":                     {"acute", "subacute"},
    "Onion/Garlic Toxicosis":                    {"acute", "subacute"},
    "Ethylene Glycol Poisoning (Antifreeze)":    {"acute"},
    "Marijuana Toxicosis":                       {"acute"},
    "Lead Poisoning":                            {"acute", "chronic"},
    # -- Environmental --
    "Heat Stroke":                               {"acute"},
    "Hypothermia":                               {"acute"},
    "Drowning / Near-Drowning":                  {"acute"},
    "Snakebite Envenomation":                    {"acute"},
    "Bee/Wasp Sting Anaphylaxis":                {"acute"},
    # -- Dental --
    "Periodontal Disease":                       {"chronic"},
    "Tooth Abscess":                             {"acute", "subacute"},
    "Tooth Fracture":                            {"acute"},
    "Stomatitis":                                {"subacute", "chronic"},
    "Cleft Palate":                              {"chronic"},
    # -- Behavioral --
    "Separation Anxiety":                        {"chronic"},
    "Compulsive Disorder (Canine OCD)":          {"chronic"},
    "Noise Phobia":                              {"acute", "chronic"},
    "Pica":                                      {"chronic"},
    # -- Congenital --
    "Congenital Deafness":                       {"chronic"},
    "Atlantoaxial Instability":                  {"acute", "chronic"},
    "Persistent Right Aortic Arch (PRAA)":       {"chronic"},
    "Mucopolysaccharidosis":                     {"chronic"},
    "Glycogen Storage Disease":                  {"chronic"},
    "Malignant Hyperthermia":                    {"acute"},
    "Juvenile Cellulitis (Puppy Strangles)":     {"acute", "subacute"},
}


_DISEASE_AGE_PREDISPOSITION: dict[str, set[str]] = {
    # -- Puppy / young predispositions --
    "Canine Parvovirus":                        {"puppy", "young"},
    "Canine Distemper":                          {"puppy", "young"},
    "Canine Herpesvirus (CHV)":                 {"puppy"},
    "Canine Papillomatosis":                    {"puppy", "young"},
    "Roundworm Infection (Toxocara)":           {"puppy"},
    "Hookworm Infection":                       {"puppy", "young"},
    "Coccidiosis":                              {"puppy", "young"},
    "Giardiasis":                               {"puppy", "young"},
    "Intestinal Parasites":                     {"puppy", "young"},
    "Cherry Eye":                               {"puppy", "young"},
    "Panosteitis":                              {"puppy", "young"},
    "Hypertrophic Osteodystrophy (HOD)":        {"puppy"},
    "Legg-Calvé-Perthes Disease":               {"puppy", "young"},
    "Osteochondritis Dissecans (OCD)":          {"puppy", "young"},
    "Intestinal Intussusception":               {"puppy", "young"},
    "Juvenile Cellulitis (Puppy Strangles)":    {"puppy"},
    "Craniomandibular Osteopathy":              {"puppy"},
    "Retinal Dysplasia":                        {"puppy"},
    "Collie Eye Anomaly (CEA)":                 {"puppy"},
    "Cleft Palate":                             {"puppy"},
    "Congenital Deafness":                      {"puppy"},
    "Atlantoaxial Instability":                 {"puppy", "young"},
    "Persistent Right Aortic Arch (PRAA)":      {"puppy"},
    "Mucopolysaccharidosis":                    {"puppy"},
    "Glycogen Storage Disease":                 {"puppy"},
    "Patent Ductus Arteriosus (PDA)":           {"puppy", "young"},
    "Ventricular Septal Defect (VSD)":          {"puppy", "young"},
    "Portosystemic Shunt (Congenital)":         {"puppy", "young"},
    "Hydrocephalus":                            {"puppy"},
    "Cerebellar Hypoplasia":                    {"puppy"},
    "Ectopic Ureter":                           {"puppy", "young"},
    # -- Young / adult --
    "Epilepsy":                                 {"young", "adult"},
    "Allergic Dermatitis":                      {"young", "adult"},
    "Immune-Mediated Hemolytic Anemia":         {"young", "adult"},
    "Autoimmune Thrombocytopenia (ITP)":        {"young", "adult"},
    "Immune-Mediated Polyarthritis (IMPA)":     {"young", "adult"},
    "Granulomatous Meningoencephalitis (GME)":  {"young", "adult"},
    "Systemic Lupus Erythematosus (SLE)":       {"young", "adult"},
    "Evan's Syndrome":                          {"young", "adult"},
    "Separation Anxiety":                       {"young", "adult"},
    "Exercise-Induced Collapse (EIC)":          {"young", "adult"},
    "Cruciate Ligament Injury":                 {"adult"},
    "Pyometra":                                 {"adult", "senior"},
    "Mastitis":                                 {"adult"},
    "Eclampsia (Milk Fever)":                   {"adult"},
    "Dystocia":                                 {"adult"},
    "Cutaneous Histiocytoma":                   {"young"},
    # -- Senior predispositions --
    "Hypothyroidism":                           {"adult", "senior"},
    "Cushing's Disease":                        {"adult", "senior"},
    "Diabetes Mellitus":                        {"adult", "senior"},
    "Kidney Disease (CKD)":                     {"senior"},
    "Heart Disease/CHF":                        {"adult", "senior"},
    "Dilated Cardiomyopathy (DCM)":             {"adult", "senior"},
    "Mitral Valve Disease (MMVD)":              {"adult", "senior"},
    "Osteoarthritis":                           {"adult", "senior"},
    "Cognitive Dysfunction Syndrome (CDS)":     {"senior"},
    "Degenerative Myelopathy (DM)":             {"adult", "senior"},
    "Laryngeal Paralysis":                      {"senior"},
    "Vestibular Disease":                       {"senior"},
    "Cancer/Neoplasia":                         {"adult", "senior"},
    "Hemangiosarcoma":                          {"adult", "senior"},
    "Lymphoma":                                 {"adult", "senior"},
    "Osteosarcoma":                             {"adult", "senior"},
    "Mast Cell Tumor":                          {"adult", "senior"},
    "Melanoma":                                 {"senior"},
    "Squamous Cell Carcinoma":                  {"adult", "senior"},
    "Mammary Tumor":                            {"adult", "senior"},
    "Transitional Cell Carcinoma":              {"senior"},
    "Histiocytic Sarcoma":                      {"adult", "senior"},
    "Fibrosarcoma":                             {"adult", "senior"},
    "Anal Sac Adenocarcinoma":                  {"senior"},
    "Insulinoma (Pancreatic Beta Cell Tumor)":  {"adult", "senior"},
    "Thyroid Carcinoma":                        {"adult", "senior"},
    "Perianal Adenoma":                         {"senior"},
    "Hepatocellular Carcinoma":                 {"senior"},
    "Soft Tissue Sarcoma":                      {"adult", "senior"},
    "Oral Melanoma":                            {"senior"},
    "Brain Tumor":                              {"adult", "senior"},
    "Prostate Disease":                         {"adult", "senior"},
    "Benign Prostatic Hyperplasia (BPH)":       {"adult", "senior"},
    "Testicular Tumor":                         {"adult", "senior"},
    "Cataracts":                                {"senior"},
    "Nuclear Sclerosis":                        {"senior"},
    "Sudden Acquired Retinal Degeneration (SARDS)": {"adult", "senior"},
    "Progressive Retinal Atrophy (PRA)":        {"adult", "senior"},
    "Sick Sinus Syndrome":                      {"senior"},
    "Atrial Fibrillation":                      {"senior"},
    "Pulmonary Fibrosis":                       {"senior"},
    "Nasal Tumor":                              {"senior"},
    "Nasal Adenocarcinoma":                     {"senior"},
    "Spondylosis Deformans":                    {"senior"},
    "Cauda Equina Syndrome (Lumbosacral Stenosis)": {"adult", "senior"},
    "Tracheal Collapse":                        {"adult", "senior"},
    "Periodontal Disease":                      {"adult", "senior"},
    "Hip Dysplasia":                            {"puppy", "young", "adult"},
    "Elbow Dysplasia":                          {"puppy", "young"},
    "Patellar Luxation":                        {"young", "adult"},
    "Intervertebral Disc Disease (IVDD)":       {"adult", "senior"},
    "Wobbler Syndrome":                         {"young", "senior"},
    "Brachycephalic Airway Syndrome":           {"young", "adult", "senior"},
    "Hepatozoonosis":                           {"young", "adult"},
    "Hyperparathyroidism":                      {"senior"},
    "Anemia of Chronic Disease":                {"adult", "senior"},
    "Lipoma":                                   {"adult", "senior"},
    "Alopecia X":                               {"adult"},
    "Keratoconjunctivitis Sicca (Dry Eye)":     {"adult", "senior"},
    "Glaucoma":                                 {"adult", "senior"},
    "Pericardial Effusion":                     {"adult", "senior"},
    "Infective Endocarditis":                   {"adult", "senior"},
    "Chemodectoma (Heart Base Tumor)":          {"senior"},
    "Chylothorax":                              {"adult", "senior"},
    "Megacolon":                                {"adult", "senior"},
    "Copper Storage Disease":                   {"young", "adult"},
    "Myasthenia Gravis":                        {"young", "adult", "senior"},
    "Pemphigus":                                {"adult"},
    "Sebaceous Adenitis":                       {"young", "adult"},
    "Epulis (Gingival Mass)":                   {"adult", "senior"},
    "Plasmacytoma":                             {"adult", "senior"},
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
# Disease database
# ---------------------------------------------------------------------------
# Each entry:
#   name            – English name
#   name_ja         – Japanese name
#   symptoms        – set of symptom IDs (use _ANY_LIMPING where any limb)
#   description     – short English description
#   urgency         – "normal" | "urgent" | "emergency"

_DISEASE_DB: list[dict[str, Any]] = [
    {
        "name": "Canine Parvovirus",
        "name_ja": "\u72ac\u30d1\u30eb\u30dc\u30a6\u30a4\u30eb\u30b9\u611f\u67d3\u75c7",
        "symptoms": {"vomiting", "bloody_stool", "lethargy", "appetite_loss",
                      "fever", "diarrhea"},
        "description": "A highly contagious and potentially fatal viral illness "
                       "that attacks the gastrointestinal tract, most dangerous "
                       "in puppies.",
        "description_ja": "消化管を攻撃する致死率の高い伝染性ウイルス疾患で、特に子犬に危険です。",
        "urgency": "normal",
    },
    {
        "name": "Canine Distemper",
        "name_ja": "\u72ac\u30b8\u30b9\u30c6\u30f3\u30d1\u30fc",
        "symptoms": {"fever", "nasal_discharge", "eye_discharge", "coughing",
                      "lethargy", "seizures", "vomiting"},
        "description": "A serious viral disease affecting the respiratory, "
                       "gastrointestinal, and nervous systems.",
        "description_ja": "呼吸器・消化器・神経系を侵す重篤なウイルス疾患です。",
        "urgency": "normal",
    },
    {
        "name": "Kennel Cough (Bordetella)",
        "name_ja": "\u30b1\u30f3\u30cd\u30eb\u30b3\u30d5\uff08\u30dc\u30eb\u30c7\u30c6\u30e9\u611f\u67d3\u75c7\uff09",
        "symptoms": {"coughing", "sneezing", "nasal_discharge",
                      "reverse_sneezing", "lethargy"},
        "description": "A highly contagious respiratory infection causing a "
                       "persistent, forceful cough.",
        "description_ja": "持続的な強い咳を引き起こす高伝染性の呼吸器感染症です。",
        "urgency": "normal",
    },
    {
        "name": "Gastric Dilatation-Volvulus (GDV/Bloat)",
        "name_ja": "\u80c3\u62e1\u5f35\u80c3\u6355\u8ee2\u75c7\u5019\u7fa4\uff08GDV\uff09",
        "symptoms": {"bloated_abdomen", "vomiting", "excessive_panting",
                      "lethargy", "anxiety"},
        "description": "A life-threatening condition where the stomach fills "
                       "with gas and rotates, cutting off blood supply. "
                       "Requires immediate emergency surgery.",
        "description_ja": "胃がガスで膨張し捻転する致命的な緊急疾患です。直ちに外科手術が必要です。",
        "urgency": "emergency",
    },
    {
        "name": "Pancreatitis",
        "name_ja": "\u81b5\u708e",
        "symptoms": {"vomiting", "appetite_loss", "lethargy", "pain_on_touch",
                      "diarrhea", "fever"},
        "description": "Inflammation of the pancreas causing severe abdominal "
                       "pain and digestive disturbance.",
        "description_ja": "膵臓の炎症により、激しい腹痛と消化障害を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Hypothyroidism",
        "name_ja": "\u7532\u72b6\u817a\u6a5f\u80fd\u4f4e\u4e0b\u75c7",
        "symptoms": {"weight_gain", "lethargy", "hair_loss", "dry_skin",
                      "stiffness"},
        "description": "An endocrine disorder where the thyroid gland produces "
                       "insufficient hormones, slowing metabolism.",
        "description_ja": "甲状腺ホルモンの不足により代謝が低下する内分泌疾患です。",
        "urgency": "normal",
    },
    {
        "name": "Hyperthyroidism",
        "name_ja": "\u7532\u72b6\u817a\u6a5f\u80fd\u4ea2\u9032\u75c7",
        "symptoms": {"weight_loss", "appetite_increase", "excessive_thirst",
                      "anxiety", "vomiting"},
        "description": "An endocrine disorder with excess thyroid hormone "
                       "production, causing increased metabolism.",
        "description_ja": "甲状腺ホルモンの過剰産生により代謝が亢進する内分泌疾患です。",
        "urgency": "normal",
    },
    {
        "name": "Cushing's Disease",
        "name_ja": "\u30af\u30c3\u30b7\u30f3\u30b0\u75c7\u5019\u7fa4",
        "symptoms": {"excessive_thirst", "excessive_urination", "weight_gain",
                      "hair_loss", "lethargy", "excessive_panting"},
        "description": "Overproduction of cortisol by the adrenal glands, "
                       "leading to a range of systemic effects.",
        "description_ja": "副腎からのコルチゾール過剰産生により、全身に様々な症状が現れます。",
        "urgency": "normal",
    },
    {
        "name": "Addison's Disease",
        "name_ja": "\u30a2\u30b8\u30bd\u30f3\u75c5",
        "symptoms": {"lethargy", "appetite_loss", "vomiting", "diarrhea",
                      "weight_loss", "dehydration", "collapse"},
        "description": "Insufficient production of adrenal hormones, causing "
                       "weakness, dehydration, and episodic collapse.",
        "description_ja": "副腎ホルモンの不足により、脱力感や消化器症状を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Diabetes Mellitus",
        "name_ja": "\u7cd6\u5c3f\u75c5",
        "symptoms": {"excessive_thirst", "excessive_urination", "weight_loss",
                      "appetite_increase", "lethargy"},
        "description": "A metabolic disorder where the body cannot properly "
                       "regulate blood sugar levels.",
        "description_ja": "血糖値を適切に調節できなくなる代謝疾患です。",
        "urgency": "normal",
    },
    {
        "name": "Urinary Tract Infection",
        "name_ja": "\u5c3f\u8def\u611f\u67d3\u75c7",
        "symptoms": {"straining_urinate", "blood_urine",
                      "excessive_urination", "fever", "lethargy"},
        "description": "A bacterial infection of the urinary tract causing "
                       "pain, frequent urination, and sometimes blood in urine.",
        "description_ja": "尿路の細菌感染により、痛み・頻尿・血尿を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Bladder Stones",
        "name_ja": "\u81a8\u80f1\u7d50\u77f3",
        "symptoms": {"straining_urinate", "blood_urine",
                      "excessive_urination", "pain_on_touch"},
        "description": "Mineral formations in the bladder causing urinary "
                       "obstruction and discomfort.",
        "description_ja": "膀胱内のミネラル結石により、排尿障害や不快感を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Kidney Disease (CKD)",
        "name_ja": "\u6162\u6027\u814e\u81d3\u75c5",
        "symptoms": {"excessive_thirst", "excessive_urination", "appetite_loss",
                      "vomiting", "weight_loss", "lethargy"},
        "description": "Progressive loss of kidney function leading to waste "
                       "build-up and systemic illness.",
        "description_ja": "腎機能が進行性に低下し、老廃物の蓄積と全身性疾患を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Liver Disease",
        "name_ja": "\u809d\u81d3\u75c5",
        "symptoms": {"appetite_loss", "vomiting", "lethargy", "weight_loss",
                      "excessive_thirst", "bloated_abdomen"},
        "description": "Impaired liver function affecting digestion, "
                       "detoxification, and metabolism.",
        "description_ja": "肝機能の低下により、消化・解毒・代謝に影響を及ぼします。",
        "urgency": "normal",
    },
    {
        "name": "Heart Disease/CHF",
        "name_ja": "\u5fc3\u81d3\u75c5\uff0f\u3046\u3063\u8840\u6027\u5fc3\u4e0d\u5168",
        "symptoms": {"coughing", "difficulty_breathing", "lethargy",
                      "excessive_panting", "bloated_abdomen"},
        "description": "Deterioration of heart function leading to fluid "
                       "build-up and reduced exercise tolerance.",
        "description_ja": "心機能の悪化により、体液貯留と運動耐性の低下を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Allergic Dermatitis",
        "name_ja": "\u30a2\u30ec\u30eb\u30ae\u30fc\u6027\u76ae\u819a\u708e",
        "symptoms": {"itching", "skin_redness", "hair_loss", "ear_scratching",
                      "hot_spots"},
        "description": "An inflammatory skin condition triggered by "
                       "environmental or food allergens.",
        "description_ja": "環境アレルゲンや食物アレルゲンにより引き起こされる炎症性皮膚疾患です。",
        "urgency": "normal",
    },
    {
        "name": "Ear Infection (Otitis)",
        "name_ja": "\u5916\u8033\u708e",
        "symptoms": {"ear_scratching", "ear_odor", "head_tilting",
                      "pain_on_touch"},
        "description": "Infection or inflammation of the ear canal, often "
                       "bacterial or yeast-related.",
        "description_ja": "外耳道の感染または炎症で、細菌性またはマラセチア関連が多いです。",
        "urgency": "normal",
    },
    {
        "name": "Eye Infection (Conjunctivitis)",
        "name_ja": "\u7d50\u819c\u708e",
        "symptoms": {"eye_redness", "eye_discharge", "squinting"},
        "description": "Inflammation of the conjunctiva causing redness, "
                       "discharge, and discomfort.",
        "description_ja": "結膜の炎症により、充血・分泌物・不快感を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Glaucoma",
        "name_ja": "\u7dd1\u5185\u969c",
        "symptoms": {"eye_redness", "squinting", "lethargy", "pain_on_touch"},
        "description": "Increased intraocular pressure that can rapidly lead "
                       "to blindness if untreated.",
        "description_ja": "眼圧の上昇により、治療しないと急速に失明に至る可能性があります。",
        "urgency": "urgent",
    },
    {
        "name": "Osteoarthritis",
        "name_ja": "\u5909\u5f62\u6027\u95a2\u7bc0\u75c7",
        "symptoms": {*_ANY_LIMPING, "stiffness", "reluctance_move",
                     "pain_on_touch", "swollen_joints"},
        "description": "Degenerative joint disease causing chronic pain, "
                       "stiffness, and reduced mobility.",
        "description_ja": "変形性関節疾患で、慢性の痛み・こわばり・可動域の低下を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Cruciate Ligament Injury",
        "name_ja": "\u524d\u5341\u5b57\u9774\u5e2f\u65ad\u88c2",
        "symptoms": {"limping_rl", "limping_rr", "swollen_joints",
                      "reluctance_move", "pain_on_touch"},
        "description": "Tear or rupture of the cranial cruciate ligament in "
                       "the knee, causing hind-limb lameness.",
        "description_ja": "膝の前十字靭帯の断裂で、後肢の跛行を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Hip Dysplasia",
        "name_ja": "\u80a1\u95a2\u7bc0\u5f62\u6210\u4e0d\u5168",
        "symptoms": {"limping_rl", "limping_rr", "stiffness",
                      "reluctance_move", "pain_on_touch"},
        "description": "A genetic skeletal condition where the hip joint "
                       "develops abnormally, leading to arthritis and pain.",
        "description_ja": "股関節の遺伝性骨格疾患で、関節炎や痛みを引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Intervertebral Disc Disease (IVDD)",
        "name_ja": "\u690e\u9593\u677f\u30d8\u30eb\u30cb\u30a2",
        "symptoms": {"pain_on_touch", "reluctance_move", *_ANY_LIMPING,
                      "stiffness", "anxiety"},
        "description": "Degeneration or herniation of spinal discs causing "
                       "pain, nerve damage, and potential paralysis.",
        "description_ja": "椎間板の変性やヘルニアにより、痛み・神経障害・麻痺を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Epilepsy",
        "name_ja": "\u3066\u3093\u304b\u3093",
        "symptoms": {"seizures", "circling", "anxiety", "lethargy"},
        "description": "A neurological disorder causing recurrent seizures "
                       "due to abnormal brain activity.",
        "description_ja": "脳の異常な電気活動により、反復性のけいれん発作を引き起こす神経疾患です。",
        "urgency": "normal",
    },
    {
        "name": "Vestibular Disease",
        "name_ja": "\u524d\u5ead\u75be\u60a3",
        "symptoms": {"head_tilting", "circling", "vomiting", "anxiety",
                      "lethargy"},
        "description": "A condition affecting the inner ear or brainstem, "
                       "causing loss of balance and disorientation.",
        "description_ja": "内耳や脳幹に影響を与え、平衡感覚の喪失や方向感覚障害を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Intestinal Parasites",
        "name_ja": "\u8178\u5185\u5bc4\u751f\u866b\u75c7",
        "symptoms": {"diarrhea", "vomiting", "weight_loss",
                      "bloated_abdomen", "appetite_loss"},
        "description": "Worms or protozoa living in the gastrointestinal "
                       "tract, stealing nutrients and causing irritation.",
        "description_ja": "消化管に寄生する線虫や原虫で、栄養を奪い消化管を刺激します。",
        "urgency": "normal",
    },
    {
        "name": "Heartworm Disease",
        "name_ja": "\u30d5\u30a3\u30e9\u30ea\u30a2\u75c7\uff08\u72ac\u7cf8\u72b6\u866b\u75c7\uff09",
        "symptoms": {"coughing", "lethargy", "difficulty_breathing",
                      "weight_loss", "bloated_abdomen", "excessive_panting"},
        "description": "Parasitic worms residing in the heart and pulmonary "
                       "arteries, causing progressive organ damage.",
        "description_ja": "心臓や肺動脈に寄生する寄生虫で、進行性の臓器障害を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Lyme Disease",
        "name_ja": "\u30e9\u30a4\u30e0\u75c5",
        "symptoms": {"fever", *_ANY_LIMPING, "swollen_joints", "lethargy",
                      "appetite_loss"},
        "description": "A tick-borne bacterial infection causing joint "
                       "inflammation, fever, and malaise.",
        "description_ja": "マダニ媒介の細菌感染症で、関節炎・発熱・倦怠感を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Pyometra",
        "name_ja": "\u5b50\u5bae\u84c4\u81bf\u75c7",
        "symptoms": {"genital_discharge", "excessive_thirst", "lethargy",
                      "fever", "bloated_abdomen", "vomiting"},
        "description": "A serious uterine infection in unspayed females "
                       "requiring emergency surgical intervention.",
        "description_ja": "未避妊の雌犬に発生する重篤な子宮感染症で、緊急手術が必要です。",
        "urgency": "emergency",
    },
    {
        "name": "Prostate Disease",
        "name_ja": "\u524d\u7acb\u817a\u75be\u60a3",
        "symptoms": {"straining_urinate", "blood_urine",
                      "genital_discharge", "constipation"},
        "description": "Enlargement or infection of the prostate gland "
                       "affecting urination and defecation.",
        "description_ja": "前立腺の肥大や感染により、排尿や排便に影響を与えます。",
        "urgency": "normal",
    },
    {
        "name": "Mange (Demodex/Sarcoptes)",
        "name_ja": "\u75a5\u7664\uff08\u30cb\u30ad\u30d3\u30c0\u30cb\uff0f\u30d2\u30bc\u30f3\u30c0\u30cb\uff09",
        "symptoms": {"hair_loss", "itching", "skin_redness", "dry_skin"},
        "description": "Skin disease caused by mites, leading to intense "
                       "itching, hair loss, and skin irritation.",
        "description_ja": "ダニによる皮膚疾患で、激しいかゆみ・脱毛・皮膚刺激を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Fungal Infection (Ringworm)",
        "name_ja": "\u771f\u83cc\u611f\u67d3\u75c7\uff08\u76ae\u819a\u7cf8\u72b6\u83cc\u75c7\uff09",
        "symptoms": {"hair_loss", "skin_redness", "dry_skin"},
        "description": "A contagious fungal skin infection causing circular "
                       "patches of hair loss and scaling.",
        "description_ja": "円形の脱毛斑と鱗屑を引き起こす伝染性の真菌性皮膚感染症です。",
        "urgency": "normal",
    },
    {
        "name": "Cancer/Neoplasia",
        "name_ja": "\u816b\u760d\uff08\u304c\u3093\uff09",
        "symptoms": {"lumps", "weight_loss", "lethargy", "appetite_loss"},
        "description": "Abnormal cell growth forming tumors that may be "
                       "benign or malignant, potentially spreading to other "
                       "organs.",
        "description_ja": "異常な細胞増殖により腫瘍を形成し、良性または悪性の場合があります。",
        "urgency": "normal",
    },
    {
        "name": "Immune-Mediated Hemolytic Anemia",
        "name_ja": "\u514d\u75ab\u4ecb\u5728\u6027\u6eb6\u8840\u6027\u8ca7\u8840",
        "symptoms": {"lethargy", "rapid_breathing", "appetite_loss", "fever"},
        "description": "The immune system destroys the body's own red blood "
                       "cells, causing severe anemia.",
        "description_ja": "免疫系が自身の赤血球を破壊し、重度の貧血を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Gastroenteritis",
        "name_ja": "\u80c3\u8178\u708e",
        "symptoms": {"vomiting", "diarrhea", "appetite_loss", "lethargy", "dehydration", "abdominal_pain"},
        "description": "Inflammation of the stomach and intestines, commonly "
                       "from dietary indiscretion or infection.",
        "description_ja": "食事の不摂生や感染により起こる胃腸の炎症です。",
        "urgency": "normal",
    },
    {
        "name": "Brachycephalic Airway Syndrome",
        "name_ja": "\u77ed\u982d\u7a2e\u6c17\u9053\u75c7\u5019\u7fa4",
        "symptoms": {"difficulty_breathing", "snoring", "excessive_panting",
                      "reverse_sneezing", "coughing"},
        "description": "A set of upper airway abnormalities common in "
                       "short-nosed breeds, causing breathing difficulties.",
        "description_ja": "短頭種に多い上気道の構造異常で、呼吸困難を引き起こします。",
        "urgency": "normal",
    },
    # ===========================================================================
    # Expanded Disease Database (diseases #37–100)
    # ===========================================================================
    # ---- Infectious ----
    {
        "name": "Canine Influenza (CIV)",
        "name_ja": "犬インフルエンザ",
        "symptoms": {"coughing", "sneezing", "nasal_discharge", "fever",
                      "lethargy", "appetite_loss"},
        "description": "A highly contagious respiratory virus (H3N2/H3N8) "
                       "causing persistent cough, nasal discharge, and fever.",
        "description_ja": "高い伝染性を持つ呼吸器ウイルス（H3N2/H3N8）で、持続する咳・鼻汁・発熱を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Leptospirosis",
        "name_ja": "レプトスピラ症",
        "symptoms": {"fever", "vomiting", "lethargy", "excessive_thirst",
                      "appetite_loss", "excessive_urination"},
        "description": "A bacterial zoonotic disease spread through contaminated "
                       "water, affecting kidneys and liver.",
        "description_ja": "汚染水を介して伝播する人獣共通細菌感染症で、腎臓と肝臓を侵します。",
        "urgency": "urgent",
    },
    {
        "name": "Canine Infectious Hepatitis",
        "name_ja": "犬伝染性肝炎（アデノウイルス）",
        "symptoms": {"fever", "lethargy", "vomiting", "appetite_loss",
                      "bloated_abdomen", "eye_redness"},
        "description": "A viral infection (Canine Adenovirus-1) targeting the "
                       "liver, kidneys, and blood vessel lining.",
        "description_ja": "犬アデノウイルス1型による肝臓・腎臓・血管内皮を標的とするウイルス感染症です。",
        "urgency": "urgent",
    },
    {
        "name": "Giardiasis",
        "name_ja": "ジアルジア症",
        "symptoms": {"diarrhea", "vomiting", "weight_loss", "appetite_loss",
                      "excessive_gas"},
        "description": "An intestinal parasitic infection caused by Giardia "
                       "protozoa, leading to chronic diarrhea.",
        "description_ja": "ジアルジア原虫による腸管寄生虫感染症で、慢性下痢を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Ehrlichiosis",
        "name_ja": "エールリヒア症",
        "symptoms": {"fever", "lethargy", "appetite_loss", "weight_loss",
                      *_ANY_LIMPING},
        "description": "A tick-borne rickettsial disease causing fever, "
                       "lethargy, and blood cell abnormalities.",
        "description_ja": "マダニ媒介のリケッチア感染症で、発熱・倦怠感・血球異常を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Anaplasmosis",
        "name_ja": "アナプラズマ症",
        "symptoms": {"fever", "lethargy", "stiffness", "appetite_loss",
                      "swollen_joints", "vomiting"},
        "description": "A tick-borne bacterial infection causing joint pain, "
                       "fever, and platelet abnormalities.",
        "description_ja": "マダニ媒介の細菌感染症で、関節痛・発熱・血小板異常を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Coccidiosis",
        "name_ja": "コクシジウム症",
        "symptoms": {"diarrhea", "bloody_stool", "weight_loss", "lethargy",
                      "appetite_loss"},
        "description": "A protozoal intestinal infection common in puppies, "
                       "causing watery or bloody diarrhea.",
        "description_ja": "子犬に多い原虫性の腸管感染症で、水様便や血便を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Babesiosis",
        "name_ja": "バベシア症",
        "symptoms": {"lethargy", "fever", "appetite_loss", "rapid_breathing",
                      "weight_loss"},
        "description": "A tick-borne protozoal disease that destroys red blood "
                       "cells, causing severe anemia.",
        "description_ja": "マダニ媒介の原虫疾患で、赤血球を破壊し重度の貧血を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Canine Coronavirus (Enteric)",
        "name_ja": "犬コロナウイルス腸炎",
        "symptoms": {"diarrhea", "vomiting", "appetite_loss", "lethargy", "dehydration", "fever"},
        "description": "An enteric coronavirus causing mild to moderate "
                       "gastrointestinal illness, primarily in puppies.",
        "description_ja": "子犬に多い腸管コロナウイルスで、軽度〜中等度の消化器症状を引き起こします。",
        "urgency": "normal",
    },
    # ---- Digestive ----
    {
        "name": "Inflammatory Bowel Disease (IBD)",
        "name_ja": "炎症性腸疾患（IBD）",
        "symptoms": {"diarrhea", "vomiting", "weight_loss", "appetite_loss",
                      "excessive_gas"},
        "description": "Chronic inflammation of the gastrointestinal tract "
                       "causing persistent digestive symptoms.",
        "description_ja": "消化管の慢性炎症により、持続する消化器症状を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Megaesophagus",
        "name_ja": "巨大食道症",
        "symptoms": {"regurgitation", "weight_loss", "coughing", "appetite_loss",
                      "difficulty_breathing", "drooling"},
        "description": "Dilation of the esophagus with loss of motility, "
                       "causing regurgitation (not vomiting) and aspiration risk.",
        "description_ja": "食道の拡張と運動機能低下により、吐き戻しと誤嚥のリスクが生じます。",
        "urgency": "normal",
    },
    {
        "name": "Exocrine Pancreatic Insufficiency (EPI)",
        "name_ja": "膵外分泌不全症（EPI）",
        "symptoms": {"diarrhea", "weight_loss", "appetite_increase",
                      "excessive_gas"},
        "description": "Insufficient production of digestive enzymes by the "
                       "pancreas, leading to malabsorption.",
        "description_ja": "膵臓の消化酵素産生不足により、栄養吸収障害を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Foreign Body Obstruction",
        "name_ja": "消化管異物閉塞",
        "symptoms": {"vomiting", "appetite_loss", "lethargy",
                      "bloated_abdomen", "pain_on_touch", "constipation"},
        "description": "Blockage of the gastrointestinal tract by an ingested "
                       "foreign object, requiring emergency surgery.",
        "description_ja": "異物の摂取による消化管閉塞で、緊急手術が必要になることがあります。",
        "urgency": "emergency",
    },
    {
        "name": "Hemorrhagic Gastroenteritis (HGE)",
        "name_ja": "出血性胃腸炎（HGE）",
        "symptoms": {"bloody_stool", "vomiting", "diarrhea", "lethargy",
                      "appetite_loss"},
        "description": "Acute hemorrhagic diarrhea syndrome with sudden onset "
                       "of bloody stool and rapid dehydration.",
        "description_ja": "血便の突然の発症と急速な脱水を伴う急性出血性下痢症候群です。",
        "urgency": "emergency",
    },
    {
        "name": "Colitis",
        "name_ja": "大腸炎",
        "symptoms": {"diarrhea", "bloody_stool", "constipation",
                      "excessive_gas", "appetite_loss"},
        "description": "Inflammation of the large intestine causing frequent "
                       "loose stools, often with mucus or blood.",
        "description_ja": "大腸の炎症で、粘液や血液を伴う頻繁な軟便を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Portosystemic Shunt (Liver Shunt)",
        "name_ja": "門脈体循環シャント",
        "symptoms": {"seizures", "vomiting", "lethargy", "excessive_thirst",
                      "weight_loss", "circling"},
        "description": "An abnormal blood vessel bypasses the liver, allowing "
                       "toxins to reach the brain and other organs.",
        "description_ja": "異常血管が肝臓を迂回し、毒素が脳や他の臓器に到達する先天性疾患です。",
        "urgency": "urgent",
    },
    # ---- Cardiac ----
    {
        "name": "Dilated Cardiomyopathy (DCM)",
        "name_ja": "拡張型心筋症（DCM）",
        "symptoms": {"coughing", "difficulty_breathing", "lethargy",
                      "bloated_abdomen", "weight_loss"},
        "description": "Heart muscle weakens and enlarges, reducing the "
                       "heart's pumping ability and leading to heart failure.",
        "description_ja": "心筋が弱くなり拡大することで、ポンプ機能が低下し心不全に至ります。",
        "urgency": "urgent",
    },
    {
        "name": "Patent Ductus Arteriosus (PDA)",
        "name_ja": "動脈管開存症（PDA）",
        "symptoms": {"difficulty_breathing", "lethargy", "coughing",
                      "excessive_panting"},
        "description": "A congenital heart defect where the ductus arteriosus "
                       "fails to close after birth.",
        "description_ja": "出生後に動脈管が閉鎖しない先天性心疾患です。",
        "urgency": "urgent",
    },
    {
        "name": "Aortic Stenosis",
        "name_ja": "大動脈弁狭窄症",
        "symptoms": {"lethargy", "difficulty_breathing", "coughing",
                      "excessive_panting"},
        "description": "Narrowing of the aortic valve obstructing blood flow "
                       "from the heart, common in large breeds.",
        "description_ja": "大動脈弁の狭窄により心臓からの血流が阻害される疾患で、大型犬に多いです。",
        "urgency": "urgent",
    },
    {
        "name": "Pulmonic Stenosis",
        "name_ja": "肺動脈弁狭窄症",
        "symptoms": {"lethargy", "difficulty_breathing", "bloated_abdomen",
                      "excessive_panting"},
        "description": "Congenital narrowing of the pulmonic valve, restricting "
                       "blood flow to the lungs.",
        "description_ja": "肺動脈弁の先天性狭窄により、肺への血流が制限されます。",
        "urgency": "normal",
    },
    {
        "name": "Pericardial Effusion",
        "name_ja": "心嚢水貯留",
        "symptoms": {"difficulty_breathing", "lethargy", "bloated_abdomen",
                      "rapid_breathing", "appetite_loss"},
        "description": "Fluid accumulation around the heart, compressing "
                       "it and reducing cardiac output.",
        "description_ja": "心臓周囲に液体が貯留し、心臓を圧迫して心拍出量を低下させます。",
        "urgency": "emergency",
    },
    # ---- Skin ----
    {
        "name": "Pyoderma",
        "name_ja": "膿皮症",
        "symptoms": {"skin_redness", "itching", "hair_loss", "hot_spots",
                      "lumps"},
        "description": "A bacterial skin infection causing pustules, crusts, "
                       "and hair loss, often secondary to allergies.",
        "description_ja": "膿疱・痂皮・脱毛を引き起こす細菌性皮膚感染症で、アレルギーに続発することが多いです。",
        "urgency": "normal",
    },
    {
        "name": "Sebaceous Adenitis",
        "name_ja": "脂腺炎",
        "symptoms": {"hair_loss", "dry_skin", "itching", "skin_redness"},
        "description": "An immune-mediated inflammatory disease targeting the "
                       "sebaceous glands, causing scaling and hair loss.",
        "description_ja": "脂腺を標的とする免疫介在性炎症疾患で、鱗屑と脱毛を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Pemphigus",
        "name_ja": "天疱瘡",
        "symptoms": {"skin_redness", "hair_loss", "itching", "lumps",
                      "lethargy"},
        "description": "An autoimmune skin disease causing blisters and "
                       "erosions on the skin and mucous membranes.",
        "description_ja": "皮膚や粘膜に水疱とびらんを生じる自己免疫性皮膚疾患です。",
        "urgency": "normal",
    },
    {
        "name": "Alopecia X",
        "name_ja": "脱毛症X",
        "symptoms": {"hair_loss", "dry_skin"},
        "description": "A cosmetic hair loss condition of unknown cause, "
                       "primarily affecting Nordic breeds.",
        "description_ja": "原因不明の脱毛症で、ノルディック系犬種に多く見られます。",
        "urgency": "normal",
    },
    {
        "name": "Acral Lick Dermatitis",
        "name_ja": "肢端舐性皮膚炎",
        "symptoms": {"itching", "skin_redness", "hair_loss", "anxiety"},
        "description": "A self-inflicted skin lesion from compulsive licking, "
                       "often with underlying psychological or physical causes.",
        "description_ja": "強迫的な舐め行動により生じる自傷性皮膚病変で、心因性または身体的原因があります。",
        "urgency": "normal",
    },
    # ---- Eye ----
    {
        "name": "Cherry Eye",
        "name_ja": "チェリーアイ（第三眼瞼腺脱出）",
        "symptoms": {"eye_redness", "eye_discharge"},
        "description": "Prolapse of the third eyelid gland, appearing as a "
                       "red mass in the corner of the eye.",
        "description_ja": "第三眼瞼腺の脱出で、目の内角に赤い塊として現れます。",
        "urgency": "normal",
    },
    {
        "name": "Keratoconjunctivitis Sicca (Dry Eye)",
        "name_ja": "乾性角結膜炎（ドライアイ）",
        "symptoms": {"eye_discharge", "squinting", "eye_redness"},
        "description": "Insufficient tear production causing chronic eye "
                       "irritation, discharge, and potential corneal damage.",
        "description_ja": "涙液分泌不足による慢性的な眼の刺激・分泌物・角膜障害のリスクがあります。",
        "urgency": "normal",
    },
    {
        "name": "Entropion",
        "name_ja": "眼瞼内反症",
        "symptoms": {"eye_redness", "eye_discharge", "squinting"},
        "description": "Inward rolling of the eyelid causing the lashes to "
                       "rub against the cornea, leading to irritation.",
        "description_ja": "眼瞼が内側に反転し、睫毛が角膜を擦って刺激を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Corneal Ulcer",
        "name_ja": "角膜潰瘍",
        "symptoms": {"squinting", "eye_discharge", "eye_redness",
                      "pain_on_touch"},
        "description": "An open sore on the corneal surface causing intense "
                       "pain and risk of permanent eye damage.",
        "description_ja": "角膜表面の開放性潰瘍で、強い痛みと永久的な眼障害のリスクがあります。",
        "urgency": "urgent",
    },
    {
        "name": "Lens Luxation",
        "name_ja": "水晶体脱臼",
        "symptoms": {"eye_redness", "squinting", "pain_on_touch"},
        "description": "Displacement of the lens from its normal position, "
                       "potentially leading to glaucoma and blindness.",
        "description_ja": "水晶体の正常位置からのずれで、緑内障や失明に至る可能性があります。",
        "urgency": "urgent",
    },
    {
        "name": "Retinal Detachment",
        "name_ja": "網膜剥離",
        "symptoms": {"squinting", "anxiety", "circling"},
        "description": "Separation of the retina from its underlying tissue, "
                       "causing sudden vision loss.",
        "description_ja": "網膜が下層組織から剥離し、突然の視力喪失を引き起こします。",
        "urgency": "emergency",
    },
    # ---- Musculoskeletal ----
    {
        "name": "Elbow Dysplasia",
        "name_ja": "肘関節形成不全",
        "symptoms": {"limping_fl", "limping_fr", "stiffness",
                      "reluctance_move", "pain_on_touch"},
        "description": "A developmental condition of the elbow joint causing "
                       "lameness and arthritis in young large-breed dogs.",
        "description_ja": "肘関節の発育異常で、若い大型犬に跛行と関節炎を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Legg-Calvé-Perthes Disease",
        "name_ja": "レッグ・ペルテス病",
        "symptoms": {"limping_rl", "limping_rr", "pain_on_touch",
                      "reluctance_move", "stiffness"},
        "description": "Avascular necrosis of the femoral head in small-breed "
                       "puppies, causing hip pain and lameness.",
        "description_ja": "小型犬の子犬に見られる大腿骨頭の無腐性壊死で、股関節の痛みと跛行を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Osteochondritis Dissecans (OCD)",
        "name_ja": "離断性骨軟骨症（OCD）",
        "symptoms": {"limping_fl", "limping_fr", "swollen_joints",
                      "stiffness", "pain_on_touch"},
        "description": "A joint disorder where cartilage separates from the "
                       "underlying bone, common in fast-growing large breeds.",
        "description_ja": "軟骨が骨から剥離する関節疾患で、急速に成長する大型犬に多いです。",
        "urgency": "normal",
    },
    {
        "name": "Panosteitis",
        "name_ja": "汎骨炎（成長痛）",
        "symptoms": {*_ANY_LIMPING, "pain_on_touch", "fever",
                      "appetite_loss"},
        "description": "Self-limiting inflammation of the long bones in "
                       "growing large-breed dogs, causing shifting lameness.",
        "description_ja": "成長期の大型犬の長骨に起こる自己限定的な炎症で、移動性の跛行を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Hypertrophic Osteodystrophy (HOD)",
        "name_ja": "肥大性骨異栄養症（HOD）",
        "symptoms": {"swollen_joints", "fever", "lethargy",
                      "reluctance_move", "pain_on_touch", "appetite_loss"},
        "description": "Painful bone disease of rapidly growing large-breed "
                       "puppies, causing swelling near joints.",
        "description_ja": "急速に成長する大型犬の子犬に見られる骨疾患で、関節付近の腫脹を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Wobbler Syndrome",
        "name_ja": "ウォブラー症候群（頸椎脊髄症）",
        "symptoms": {"stiffness", *_ANY_LIMPING, "reluctance_move",
                      "pain_on_touch"},
        "description": "Compression of the spinal cord in the neck region, "
                       "causing a wobbly gait, common in Great Danes and "
                       "Dobermans.",
        "description_ja": "頸部の脊髄圧迫により不安定な歩様を引き起こし、グレートデーンやドーベルマンに多いです。",
        "urgency": "normal",
    },
    # ---- Neuro ----
    {
        "name": "Hydrocephalus",
        "name_ja": "水頭症",
        "symptoms": {"seizures", "circling", "head_tilting", "lethargy",
                      "anxiety"},
        "description": "Abnormal accumulation of cerebrospinal fluid in the "
                       "brain, common in toy breeds.",
        "description_ja": "脳内の脳脊髄液の異常蓄積で、トイ犬種に多く見られます。",
        "urgency": "urgent",
    },
    {
        "name": "Syringomyelia (Chiari Malformation)",
        "name_ja": "脊髄空洞症（キアリ様奇形）",
        "symptoms": {"pain_on_touch", "ear_scratching", "anxiety",
                      "stiffness"},
        "description": "Fluid-filled cavities in the spinal cord caused by "
                       "skull malformation, especially in Cavalier King "
                       "Charles Spaniels.",
        "description_ja": "頭蓋骨奇形による脊髄内の液体貯留で、キャバリアに特に多く見られます。",
        "urgency": "normal",
    },
    {
        "name": "Cognitive Dysfunction Syndrome (CDS)",
        "name_ja": "認知機能不全症候群",
        "symptoms": {"circling", "anxiety", "incontinence", "hiding",
                      "aggression_change"},
        "description": "Age-related cognitive decline in senior dogs, similar "
                       "to dementia in humans.",
        "description_ja": "高齢犬に見られる加齢性の認知機能低下で、人間の認知症に類似しています。",
        "urgency": "normal",
    },
    {
        "name": "Myasthenia Gravis",
        "name_ja": "重症筋無力症",
        "symptoms": {"lethargy", "reluctance_move", "difficulty_breathing",
                      "vomiting"},
        "description": "An autoimmune neuromuscular disease causing muscle "
                       "weakness, often associated with megaesophagus.",
        "description_ja": "筋力低下を引き起こす自己免疫性神経筋疾患で、巨大食道症を伴うことが多いです。",
        "urgency": "normal",
    },
    {
        "name": "Granulomatous Meningoencephalitis (GME)",
        "name_ja": "肉芽腫性髄膜脳炎（GME）",
        "symptoms": {"seizures", "circling", "head_tilting", "lethargy",
                      "fever"},
        "description": "An inflammatory brain disease of unknown cause, "
                       "primarily affecting small-breed dogs.",
        "description_ja": "原因不明の脳炎症性疾患で、小型犬に多く見られます。",
        "urgency": "urgent",
    },
    # ---- Reproductive ----
    {
        "name": "Cryptorchidism",
        "name_ja": "停留精巣（陰睾）",
        "symptoms": {"genital_discharge"},
        "description": "Failure of one or both testicles to descend into the "
                       "scrotum, increasing cancer risk.",
        "description_ja": "片方または両方の精巣が陰嚢に下降しない疾患で、腫瘍リスクが上昇します。",
        "urgency": "normal",
    },
    {
        "name": "Mastitis",
        "name_ja": "乳腺炎",
        "symptoms": {"fever", "lethargy", "appetite_loss", "pain_on_touch"},
        "description": "Infection of the mammary glands in nursing females, "
                       "causing swelling, pain, and fever.",
        "description_ja": "授乳中の雌犬の乳腺感染症で、腫脹・痛み・発熱を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Eclampsia (Milk Fever)",
        "name_ja": "子癇（産褥テタニー）",
        "symptoms": {"seizures", "anxiety", "excessive_panting", "stiffness",
                      "fever"},
        "description": "A life-threatening drop in blood calcium in nursing "
                       "mothers, causing tremors and seizures.",
        "description_ja": "授乳中の母犬の血中カルシウム低下により、振戦とけいれんを引き起こす緊急疾患です。",
        "urgency": "emergency",
    },
    {
        "name": "Benign Prostatic Hyperplasia (BPH)",
        "name_ja": "良性前立腺肥大症",
        "symptoms": {"straining_urinate", "constipation",
                      "genital_discharge"},
        "description": "Non-cancerous enlargement of the prostate in intact "
                       "male dogs, common with aging.",
        "description_ja": "未去勢の雄犬に見られる良性の前立腺肥大で、加齢とともに増加します。",
        "urgency": "normal",
    },
    # ---- Respiratory ----
    {
        "name": "Tracheal Collapse",
        "name_ja": "気管虚脱",
        "symptoms": {"coughing", "difficulty_breathing", "reverse_sneezing",
                      "snoring"},
        "description": "Progressive weakening of tracheal cartilage rings, "
                       "causing airway obstruction, common in toy breeds.",
        "description_ja": "気管軟骨輪の進行性弱化により気道閉塞を引き起こし、トイ犬種に多いです。",
        "urgency": "normal",
    },
    {
        "name": "Laryngeal Paralysis",
        "name_ja": "喉頭麻痺",
        "symptoms": {"difficulty_breathing", "coughing", "snoring",
                      "excessive_panting", "lethargy"},
        "description": "Loss of nerve function to the larynx, causing "
                       "difficulty breathing, especially in older large breeds.",
        "description_ja": "喉頭の神経機能喪失により呼吸困難を引き起こし、高齢の大型犬に多いです。",
        "urgency": "urgent",
    },
    {
        "name": "Pneumonia",
        "name_ja": "肺炎",
        "symptoms": {"coughing", "fever", "difficulty_breathing", "lethargy",
                      "nasal_discharge", "appetite_loss"},
        "description": "Infection or inflammation of the lungs causing "
                       "cough, fever, and breathing difficulty.",
        "description_ja": "肺の感染症または炎症で、咳・発熱・呼吸困難を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Aspiration Pneumonia",
        "name_ja": "誤嚥性肺炎",
        "symptoms": {"coughing", "difficulty_breathing", "fever", "lethargy",
                      "nasal_discharge"},
        "description": "Lung infection caused by inhaling food, liquid, or "
                       "vomit into the airways.",
        "description_ja": "食物・液体・嘔吐物の気道への吸引により引き起こされる肺感染症です。",
        "urgency": "emergency",
    },
    {
        "name": "Pleural Effusion",
        "name_ja": "胸水貯留",
        "symptoms": {"difficulty_breathing", "lethargy", "rapid_breathing",
                      "appetite_loss"},
        "description": "Abnormal fluid accumulation in the chest cavity, "
                       "compressing the lungs.",
        "description_ja": "胸腔内の異常な液体貯留で、肺を圧迫します。",
        "urgency": "emergency",
    },
    {
        "name": "Pulmonary Hypertension",
        "name_ja": "肺高血圧症",
        "symptoms": {"difficulty_breathing", "coughing", "lethargy",
                      "excessive_panting"},
        "description": "Elevated blood pressure in the pulmonary arteries, "
                       "straining the right side of the heart.",
        "description_ja": "肺動脈の血圧上昇により、右心系に負担がかかります。",
        "urgency": "normal",
    },
    # ---- Genetic / Hereditary ----
    {
        "name": "von Willebrand Disease",
        "name_ja": "フォンウィルブランド病",
        "symptoms": {"lethargy", "bloody_stool", "blood_urine", "swelling", "genital_discharge"},
        "description": "The most common inherited bleeding disorder in dogs, "
                       "caused by deficiency of von Willebrand factor. Dogs "
                       "may experience prolonged bleeding, bloody stool/urine, and bruising.",
        "description_ja": "犬で最も多い遺伝性出血性疾患です。フォンウィルブランド因子の異常により、外傷後の出血遷延が起こります。",
        "urgency": "normal",
    },
    {
        "name": "Progressive Retinal Atrophy (PRA)",
        "name_ja": "進行性網膜萎縮症（PRA）",
        "symptoms": {"anxiety", "hiding"},
        "description": "A group of genetic diseases causing progressive "
                       "retinal degeneration, leading to vision loss and "
                       "eventual blindness. Night blindness is often the "
                       "first sign.",
        "description_ja": "網膜が進行性に変性する遺伝性疾患群です。視力が徐々に低下し最終的に失明に至ります。",
        "urgency": "normal",
    },
    {
        "name": "Cataracts",
        "name_ja": "白内障",
        "symptoms": {"squinting", "anxiety"},
        "description": "Clouding of the lens leading to decreased vision. "
                       "Can be hereditary, age-related, or secondary to "
                       "diabetes. Surgical removal is the primary treatment.",
        "description_ja": "水晶体が白濁し視力が低下する疾患です。遺伝性、老齢性、糖尿病性など原因は様々で、手術による治療が可能です。",
        "urgency": "normal",
    },
    {
        "name": "Patellar Luxation",
        "name_ja": "膝蓋骨脱臼（パテラ）",
        "symptoms": {"limping_rl", "limping_rr", "stiffness",
                      "reluctance_move"},
        "description": "A condition where the kneecap dislocates from its "
                       "normal position. Common in small breeds, graded 1–4. "
                       "Surgical correction may be needed.",
        "description_ja": "膝蓋骨が正常な位置からずれる疾患です。小型犬に多く、グレード1〜4で分類されます。",
        "urgency": "normal",
    },
    {
        "name": "Mitral Valve Disease (MMVD)",
        "name_ja": "僧帽弁閉鎖不全症",
        "symptoms": {"coughing", "difficulty_breathing", "lethargy",
                      "excessive_panting"},
        "description": "Progressive degeneration of the mitral valve causing "
                       "blood regurgitation. The most common acquired heart "
                       "disease in dogs.",
        "description_ja": "僧帽弁の進行性変性により血液が逆流する疾患です。犬で最も多い後天性心疾患です。",
        "urgency": "normal",
    },
    {
        "name": "Degenerative Myelopathy (DM)",
        "name_ja": "変性性脊髄症（DM）",
        "symptoms": {*_ANY_LIMPING, "stiffness", "reluctance_move"},
        "description": "A progressive neurological disease affecting the "
                       "spinal cord. Causes gradual loss of coordination and "
                       "strength in the hind limbs. No cure exists.",
        "description_ja": "脊髄の進行性変性疾患です。後肢の協調運動と筋力が徐々に低下します。治療法はありません。",
        "urgency": "normal",
    },
    {
        "name": "Copper Storage Disease",
        "name_ja": "銅蓄積症",
        "symptoms": {"vomiting", "appetite_loss", "lethargy", "weight_loss",
                      "excessive_thirst"},
        "description": "A genetic inability to properly excrete copper, "
                       "leading to toxic accumulation in the liver.",
        "description_ja": "銅の排泄障害により肝臓に銅が蓄積する遺伝性疾患です。",
        "urgency": "normal",
    },
    {
        "name": "Exercise-Induced Collapse (EIC)",
        "name_ja": "運動誘発性虚脱（EIC）",
        "symptoms": {"lethargy", "excessive_panting", "reluctance_move",
                      "stiffness"},
        "description": "A genetic condition in Labrador Retrievers causing "
                       "muscle weakness and collapse after intense exercise.",
        "description_ja": "ラブラドールに多い遺伝性疾患で、激しい運動後に筋力低下と虚脱を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Cystinuria",
        "name_ja": "シスチン尿症",
        "symptoms": {"straining_urinate", "blood_urine", "pain_on_touch"},
        "description": "A hereditary condition causing cystine stones in the "
                       "urinary tract, common in certain breeds.",
        "description_ja": "遺伝的に尿路にシスチン結石を形成する疾患で、特定犬種に多いです。",
        "urgency": "normal",
    },
    # ---- Tumors / Oncology ----
    {
        "name": "Hemangiosarcoma",
        "name_ja": "血管肉腫",
        "symptoms": {"lethargy", "bloated_abdomen", "weight_loss",
                      "appetite_loss", "rapid_breathing"},
        "description": "An aggressive malignant tumor of blood vessel walls, "
                       "most common in the spleen and heart. Often presents "
                       "with sudden internal bleeding.",
        "description_ja": "血管壁の悪性腫瘍で、脾臓と心臓に最も多いです。突然の内出血で発見されることが多いです。",
        "urgency": "emergency",
    },
    {
        "name": "Lymphoma",
        "name_ja": "リンパ腫",
        "symptoms": {"lumps", "weight_loss", "lethargy", "appetite_loss",
                      "excessive_thirst"},
        "description": "A common cancer of the lymphatic system, presenting "
                       "as enlarged lymph nodes throughout the body.",
        "description_ja": "リンパ系の悪性腫瘍で、全身のリンパ節腫大として現れます。",
        "urgency": "normal",
    },
    {
        "name": "Osteosarcoma",
        "name_ja": "骨肉腫",
        "symptoms": {"limping_fl", "limping_fr", "swollen_joints",
                      "pain_on_touch", "reluctance_move"},
        "description": "An aggressive bone cancer primarily affecting large "
                       "and giant breed dogs, usually in the limbs.",
        "description_ja": "大型・超大型犬に多い悪性骨腫瘍で、主に四肢に発生します。",
        "urgency": "urgent",
    },
    {
        "name": "Mast Cell Tumor",
        "name_ja": "肥満細胞腫",
        "symptoms": {"lumps", "itching", "vomiting", "lethargy",
                      "appetite_loss"},
        "description": "The most common malignant skin tumor in dogs, "
                       "varying from benign to highly aggressive forms.",
        "description_ja": "犬で最も多い悪性皮膚腫瘍で、良性から高悪性度まで様々な形態があります。",
        "urgency": "normal",
    },
    {
        "name": "Melanoma",
        "name_ja": "メラノーマ（黒色腫）",
        "symptoms": {"lumps", "weight_loss", "appetite_loss"},
        "description": "A tumor of melanocyte cells, most aggressive when "
                       "found in the mouth. Common in senior dogs.",
        "description_ja": "メラノサイト由来の腫瘍で、口腔内発生時に最も悪性度が高いです。",
        "urgency": "normal",
    },
    {
        "name": "Squamous Cell Carcinoma",
        "name_ja": "扁平上皮がん（SCC）",
        "symptoms": {"lumps", "weight_loss", "appetite_loss",
                      "pain_on_touch"},
        "description": "A malignant skin tumor arising from squamous "
                       "epithelial cells. UV exposure is a risk factor. "
                       "Early detection and excision are key.",
        "description_ja": "扁平上皮細胞由来の悪性腫瘍です。紫外線がリスク因子で、早期発見と外科的切除が重要です。",
        "urgency": "normal",
    },
    {
        "name": "Mammary Tumor",
        "name_ja": "乳腺腫瘍",
        "symptoms": {"lumps", "weight_loss", "appetite_loss"},
        "description": "Tumors of the mammary glands, common in unspayed "
                       "females. About 50% are malignant.",
        "description_ja": "乳腺の腫瘍で、未避妊の雌犬に多いです。約50%が悪性です。",
        "urgency": "normal",
    },
    {
        "name": "Transitional Cell Carcinoma",
        "name_ja": "移行上皮がん（膀胱がん）",
        "symptoms": {"blood_urine", "straining_urinate",
                      "excessive_urination", "incontinence"},
        "description": "A malignant tumor of the urinary bladder, most "
                       "common in Scottish Terriers.",
        "description_ja": "膀胱の悪性腫瘍で、スコティッシュテリアに最も多く見られます。",
        "urgency": "normal",
    },
    # ---- Hematologic / Immune ----
    {
        "name": "Thrombocytopenia",
        "name_ja": "血小板減少症",
        "symptoms": {"lethargy", "skin_redness", "appetite_loss"},
        "description": "Abnormally low platelet count causing bruising and "
                       "increased bleeding risk.",
        "description_ja": "血小板数の異常低下により、あざや出血リスクが増加します。",
        "urgency": "urgent",
    },
    {
        "name": "Hemophilia A",
        "name_ja": "血友病A",
        "symptoms": {"lethargy", "swollen_joints", "stiffness"},
        "description": "An inherited bleeding disorder caused by deficiency "
                       "of clotting factor VIII.",
        "description_ja": "第VIII凝固因子の欠乏による遺伝性出血性疾患です。",
        "urgency": "normal",
    },
    {
        "name": "Autoimmune Thrombocytopenia (ITP)",
        "name_ja": "免疫介在性血小板減少症（ITP）",
        "symptoms": {"lethargy", "skin_redness", "appetite_loss", "fever"},
        "description": "The immune system destroys the body's own platelets, "
                       "causing spontaneous bleeding.",
        "description_ja": "免疫系が自身の血小板を破壊し、自然出血を引き起こします。",
        "urgency": "urgent",
    },
    # ---- Dental ----
    {
        "name": "Periodontal Disease",
        "name_ja": "歯周病",
        "symptoms": {"appetite_loss", "pain_on_touch"},
        "description": "Progressive infection of the teeth and gums, the "
                       "most common disease in dogs. Can lead to tooth loss "
                       "and systemic infection.",
        "description_ja": "歯と歯肉の進行性感染症で、犬で最も一般的な疾患です。歯の喪失や全身感染に至ることがあります。",
        "urgency": "normal",
    },
    {
        "name": "Tooth Abscess",
        "name_ja": "歯根膿瘍",
        "symptoms": {"appetite_loss", "pain_on_touch", "fever",
                      "eye_discharge"},
        "description": "A bacterial infection at the tooth root causing "
                       "severe pain, facial swelling, and potential "
                       "eye/nasal discharge.",
        "description_ja": "歯根部の細菌感染症で、激しい痛み・顔面腫脹・眼や鼻の分泌物を引き起こします。",
        "urgency": "normal",
    },
    # ---- Endocrine (additional) ----
    {
        "name": "Insulinoma",
        "name_ja": "インスリノーマ",
        "symptoms": {"seizures", "lethargy", "anxiety", "stiffness",
                      "appetite_increase"},
        "description": "A pancreatic tumor that overproduces insulin, "
                       "causing dangerous drops in blood sugar.",
        "description_ja": "インスリンを過剰産生する膵臓腫瘍で、危険な血糖低下を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Hyperparathyroidism",
        "name_ja": "副甲状腺機能亢進症",
        "symptoms": {"excessive_thirst", "excessive_urination",
                      "appetite_loss", "lethargy", "vomiting"},
        "description": "Overproduction of parathyroid hormone causing "
                       "elevated blood calcium levels.",
        "description_ja": "副甲状腺ホルモンの過剰産生により、血中カルシウムが上昇します。",
        "urgency": "normal",
    },
    # ---- Urinary (additional) ----
    {
        "name": "Fanconi Syndrome",
        "name_ja": "ファンコニ症候群",
        "symptoms": {"excessive_thirst", "excessive_urination",
                      "weight_loss", "lethargy", "appetite_loss"},
        "description": "A kidney tubule disorder causing loss of essential "
                       "nutrients in urine, common in Basenjis.",
        "description_ja": "腎尿細管の障害により必須栄養素が尿中に喪失する疾患で、バセンジーに多いです。",
        "urgency": "normal",
    },
    {
        "name": "Ectopic Ureter",
        "name_ja": "異所性尿管",
        "symptoms": {"incontinence", "straining_urinate",
                      "genital_discharge"},
        "description": "A congenital defect where the ureter connects to an "
                       "abnormal location, causing urinary incontinence.",
        "description_ja": "尿管が異常な位置に接続する先天性欠陥で、尿失禁を引き起こします。",
        "urgency": "normal",
    },
    # ===========================================================================
    # World-class expansion (#116–250) — targeting 250 total diseases
    # ===========================================================================
    # ---- Viral ----
    {
        "name": "Rabies",
        "name_ja": "狂犬病",
        "symptoms": {"seizures", "aggression_change", "anxiety", "excessive_panting", "difficulty_breathing"},
        "description": "A fatal viral disease affecting the central nervous system, transmissible to humans through bites. Vaccination is legally required.",
        "description_ja": "中枢神経系を侵す致死性ウイルス疾患で、咬傷を通じて人に感染します。ワクチン接種が法律で義務付けられています。",
        "urgency": "emergency",
    },
    {
        "name": "Canine Herpesvirus (CHV)",
        "name_ja": "犬ヘルペスウイルス感染症",
        "symptoms": {"lethargy", "appetite_loss", "nasal_discharge", "fever"},
        "description": "A viral infection causing fatal hemorrhagic disease in neonatal puppies and respiratory/genital symptoms in adults.",
        "description_ja": "新生子犬に致死的な出血性疾患を引き起こし、成犬では呼吸器・生殖器症状を示すウイルス感染症です。",
        "urgency": "urgent",
    },
    {
        "name": "Canine Papillomatosis",
        "name_ja": "犬乳頭腫症（パピローマ）",
        "symptoms": {"lumps"},
        "description": "Benign wart-like growths caused by canine papillomavirus, commonly found on the mouth and lips of young dogs.",
        "description_ja": "犬パピローマウイルスによる良性の疣贅で、若齢犬の口腔周囲に好発します。",
        "urgency": "normal",
    },
    # ---- Bacterial ----
    {
        "name": "Brucellosis",
        "name_ja": "ブルセラ症",
        "symptoms": {"lethargy", "fever", "genital_discharge", "stiffness"},
        "description": "A bacterial zoonotic disease causing reproductive failure, spinal infection, and joint inflammation.",
        "description_ja": "繁殖障害・脊椎感染・関節炎を引き起こす細菌性人獣共通感染症です。",
        "urgency": "normal",
    },
    {
        "name": "Rocky Mountain Spotted Fever",
        "name_ja": "ロッキー山紅斑熱",
        "symptoms": {"fever", "lethargy", "appetite_loss", "swollen_joints", *_ANY_LIMPING},
        "description": "A serious tick-borne rickettsial disease causing fever, joint pain, and potential organ damage.",
        "description_ja": "マダニ媒介のリケッチア感染症で、発熱・関節痛・臓器障害を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Tetanus",
        "name_ja": "破傷風",
        "symptoms": {"stiffness", "seizures", "difficulty_breathing", "anxiety"},
        "description": "A bacterial toxin disease causing severe muscle rigidity and spasms, rare but serious in dogs.",
        "description_ja": "細菌毒素による重度の筋硬直と痙攣を引き起こす疾患で、犬では稀ですが重篤です。",
        "urgency": "emergency",
    },
    {
        "name": "Nocardiosis",
        "name_ja": "ノカルジア症",
        "symptoms": {"coughing", "difficulty_breathing", "fever", "lethargy", "lumps"},
        "description": "A bacterial infection causing chronic abscesses in the lungs, skin, and other organs.",
        "description_ja": "肺・皮膚・その他の臓器に慢性膿瘍を形成する細菌感染症です。",
        "urgency": "normal",
    },
    {
        "name": "Actinomycosis",
        "name_ja": "放線菌症",
        "symptoms": {"lumps", "fever", "lethargy", "pain_on_touch"},
        "description": "A chronic bacterial infection forming draining tracts and abscesses, often from penetrating wounds.",
        "description_ja": "穿通創から慢性的な排膿管と膿瘍を形成する細菌感染症です。",
        "urgency": "normal",
    },
    # ---- Fungal ----
    {
        "name": "Blastomycosis",
        "name_ja": "ブラストミセス症",
        "symptoms": {"coughing", "difficulty_breathing", "fever", "lethargy", "weight_loss", "eye_redness"},
        "description": "A systemic fungal infection primarily affecting the lungs and spreading to skin, eyes, and bones.",
        "description_ja": "主に肺を侵し、皮膚・眼・骨に広がる全身性真菌感染症です。",
        "urgency": "urgent",
    },
    {
        "name": "Histoplasmosis",
        "name_ja": "ヒストプラズマ症",
        "symptoms": {"coughing", "diarrhea", "weight_loss", "fever", "lethargy", "eye_redness", "skin_lesions"},
        "description": "A fungal infection from contaminated soil causing respiratory, gastrointestinal, and ocular disease.",
        "description_ja": "汚染土壌から感染する真菌症で、呼吸器と消化器に病変を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Coccidioidomycosis (Valley Fever)",
        "name_ja": "コクシジオイデス症（渓谷熱）",
        "symptoms": {"coughing", "fever", "lethargy", "weight_loss", *_ANY_LIMPING},
        "description": "A fungal infection endemic to arid regions, causing respiratory and disseminated disease.",
        "description_ja": "乾燥地域に固有の真菌感染症で、呼吸器疾患と播種性疾患を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Cryptococcosis",
        "name_ja": "クリプトコッカス症",
        "symptoms": {"sneezing", "nasal_discharge", "seizures", "eye_redness", "lethargy"},
        "description": "A fungal infection often affecting the nasal cavity and CNS, associated with pigeon droppings.",
        "description_ja": "鼻腔と中枢神経系を侵すことが多い真菌感染症で、鳩の糞と関連しています。",
        "urgency": "normal",
    },
    {
        "name": "Aspergillosis",
        "name_ja": "アスペルギルス症",
        "symptoms": {"sneezing", "nasal_discharge", "pain_on_touch", "lethargy"},
        "description": "A fungal infection primarily affecting the nasal cavity, causing chronic nasal discharge and pain.",
        "description_ja": "主に鼻腔を侵す真菌感染症で、慢性の鼻汁と痛みを引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Sporotrichosis",
        "name_ja": "スポロトリコーシス",
        "symptoms": {"lumps", "skin_redness", "lethargy"},
        "description": "A fungal infection of the skin and lymph nodes from contaminated soil or plant material.",
        "description_ja": "汚染土壌や植物から感染する皮膚とリンパ節の真菌症です。",
        "urgency": "normal",
    },
    # ---- Protozoal ----
    {
        "name": "Leishmaniasis",
        "name_ja": "リーシュマニア症",
        "symptoms": {"weight_loss", "hair_loss", "skin_redness", "lethargy", "appetite_loss", "dry_skin"},
        "description": "A sandfly-transmitted protozoal disease causing skin lesions, weight loss, and organ damage.",
        "description_ja": "サシチョウバエ媒介の原虫疾患で、皮膚病変・体重減少・臓器障害を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Neosporosis",
        "name_ja": "ネオスポラ症",
        "symptoms": {*_ANY_LIMPING, "stiffness", "seizures", "reluctance_move"},
        "description": "A protozoal infection causing neuromuscular disease, especially ascending paralysis in puppies.",
        "description_ja": "子犬の上行性麻痺を引き起こす原虫感染症です。",
        "urgency": "urgent",
    },
    {
        "name": "Toxoplasmosis",
        "name_ja": "トキソプラズマ症",
        "symptoms": {"fever", "lethargy", "difficulty_breathing", "diarrhea", "seizures"},
        "description": "A protozoal infection that can cause respiratory, neurological, and ocular disease in immunocompromised dogs.",
        "description_ja": "免疫抑制犬で呼吸器・神経・眼疾患を引き起こす原虫感染症です。",
        "urgency": "normal",
    },
    {
        "name": "Hepatozoonosis",
        "name_ja": "ヘパトゾーン症",
        "symptoms": {"fever", "lethargy", "weight_loss", "stiffness", "pain_on_touch"},
        "description": "A tick-borne protozoal disease causing muscle pain, fever, and wasting.",
        "description_ja": "マダニ媒介の原虫疾患で、筋肉痛・発熱・消耗を引き起こします。",
        "urgency": "normal",
    },
    # ---- Parasites (specific) ----
    {
        "name": "Roundworm Infection (Toxocara)",
        "name_ja": "回虫症（トキソカラ）",
        "symptoms": {"bloated_abdomen", "diarrhea", "vomiting", "weight_loss", "coughing"},
        "description": "Intestinal parasite common in puppies, causing pot-bellied appearance and potential zoonotic risk.",
        "description_ja": "子犬に多い腸管寄生虫で、腹部膨満を引き起こし、人獣共通感染のリスクがあります。",
        "urgency": "normal",
    },
    {
        "name": "Hookworm Infection",
        "name_ja": "鉤虫症",
        "symptoms": {"diarrhea", "bloody_stool", "weight_loss", "lethargy"},
        "description": "Blood-sucking intestinal parasites causing anemia, especially dangerous in puppies.",
        "description_ja": "吸血性の腸管寄生虫で、特に子犬では貧血を引き起こし危険です。",
        "urgency": "normal",
    },
    {
        "name": "Whipworm Infection (Trichuris)",
        "name_ja": "鞭虫症",
        "symptoms": {"diarrhea", "bloody_stool", "weight_loss"},
        "description": "Large intestine parasite causing chronic bloody diarrhea and weight loss.",
        "description_ja": "大腸に寄生し、慢性の血便と体重減少を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Tapeworm Infection (Dipylidium/Echinococcus)",
        "name_ja": "条虫症（瓜実条虫・エキノコックス）",
        "symptoms": {"weight_loss", "diarrhea", "appetite_increase"},
        "description": "Intestinal tapeworms transmitted by fleas or contaminated prey. Echinococcus is a serious zoonotic risk.",
        "description_ja": "ノミや汚染獲物から感染する条虫で、エキノコックスは重大な人獣共通感染リスクがあります。",
        "urgency": "normal",
    },
    {
        "name": "Ear Mite Infestation (Otodectes)",
        "name_ja": "耳ダニ感染症（ミミヒゼンダニ）",
        "symptoms": {"ear_scratching", "ear_odor", "head_tilting"},
        "description": "Highly contagious ear parasites causing intense itching and dark discharge, common in puppies.",
        "description_ja": "子犬に多い高伝染性の耳寄生虫で、激しい痒みと暗色分泌物を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Flea Allergy Dermatitis",
        "name_ja": "ノミアレルギー性皮膚炎",
        "symptoms": {"itching", "hair_loss", "skin_redness", "hot_spots"},
        "description": "An allergic reaction to flea saliva causing intense itching, especially at the tail base.",
        "description_ja": "ノミ唾液に対するアレルギー反応で、特に尾根部に激しい痒みを引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Sarcoptic Mange (Scabies)",
        "name_ja": "疥癬（ヒゼンダニ症）",
        "symptoms": {"itching", "hair_loss", "skin_redness", "dry_skin", "ear_scratching"},
        "description": "A highly contagious mite infestation causing intense itching and crusty skin. Zoonotic.",
        "description_ja": "激しい痒みと痂皮を引き起こす高伝染性のダニ感染症で、人にも感染します。",
        "urgency": "normal",
    },
    {
        "name": "Cheyletiellosis (Walking Dandruff)",
        "name_ja": "ツメダニ症",
        "symptoms": {"itching", "dry_skin", "hair_loss"},
        "description": "A mite infestation causing excessive dandruff and mild itching, visible as moving flakes.",
        "description_ja": "大量のフケと軽度の痒みを引き起こすダニ感染症で、フケが動いて見えることがあります。",
        "urgency": "normal",
    },
    # ---- Eye (expanded) ----
    {
        "name": "Ectropion",
        "name_ja": "眼瞼外反症",
        "symptoms": {"eye_redness", "eye_discharge"},
        "description": "Outward rolling of the lower eyelid exposing the conjunctiva, common in loose-skinned breeds.",
        "description_ja": "下眼瞼が外側に反転し結膜が露出する疾患で、皮膚の弛緩した犬種に多いです。",
        "urgency": "normal",
    },
    {
        "name": "Distichiasis",
        "name_ja": "睫毛重生",
        "symptoms": {"squinting", "eye_discharge", "eye_redness"},
        "description": "Extra eyelashes growing from abnormal locations, irritating the cornea.",
        "description_ja": "異常な位置から余分な睫毛が生え、角膜を刺激する疾患です。",
        "urgency": "normal",
    },
    {
        "name": "Nuclear Sclerosis",
        "name_ja": "核硬化症",
        "symptoms": {"squinting"},
        "description": "Normal age-related hardening of the lens causing a bluish haze, often mistaken for cataracts.",
        "description_ja": "加齢による水晶体の硬化で青みがかった曇りが生じ、白内障と間違われやすいです。",
        "urgency": "normal",
    },
    {
        "name": "Retinal Dysplasia",
        "name_ja": "網膜形成異常",
        "symptoms": {"squinting", "anxiety"},
        "description": "A congenital malformation of the retina ranging from mild folds to complete detachment.",
        "description_ja": "網膜の先天性奇形で、軽度のひだから完全剥離まで様々な程度があります。",
        "urgency": "normal",
    },
    {
        "name": "Pannus (Chronic Superficial Keratitis)",
        "name_ja": "パンヌス（慢性表層性角膜炎）",
        "symptoms": {"eye_redness", "squinting", "eye_discharge"},
        "description": "An immune-mediated progressive corneal disease common in German Shepherds, worsened by UV exposure.",
        "description_ja": "ジャーマンシェパードに多い免疫介在性の進行性角膜疾患で、紫外線で悪化します。",
        "urgency": "normal",
    },
    {
        "name": "Uveitis",
        "name_ja": "ぶどう膜炎",
        "symptoms": {"eye_redness", "squinting", "eye_discharge", "pain_on_touch"},
        "description": "Inflammation of the uveal tract causing pain, redness, and potential vision loss.",
        "description_ja": "ぶどう膜の炎症で、痛み・充血・視力低下を引き起こす可能性があります。",
        "urgency": "urgent",
    },
    {
        "name": "Corneal Dystrophy",
        "name_ja": "角膜ジストロフィー",
        "symptoms": {"squinting", "eye_redness"},
        "description": "A hereditary opacity of the cornea, usually bilateral and slowly progressive.",
        "description_ja": "遺伝性の角膜混濁で、通常両眼性で緩徐に進行します。",
        "urgency": "normal",
    },
    {
        "name": "Collie Eye Anomaly (CEA)",
        "name_ja": "コリー眼異常（CEA）",
        "symptoms": {"anxiety"},
        "description": "A congenital inherited eye disorder affecting Collies and related breeds, ranging from mild to blindness.",
        "description_ja": "コリー系犬種に見られる先天性遺伝性眼疾患で、軽度から失明まで様々です。",
        "urgency": "normal",
    },
    {
        "name": "Horner's Syndrome",
        "name_ja": "ホルネル症候群",
        "symptoms": {"squinting", "eye_redness"},
        "description": "Disruption of sympathetic nerve supply to the eye causing miosis, ptosis, and enophthalmos.",
        "description_ja": "眼への交感神経支配の障害により、縮瞳・眼瞼下垂・眼球陥凹を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Sudden Acquired Retinal Degeneration (SARDS)",
        "name_ja": "突発性後天性網膜変性症（SARDS）",
        "symptoms": {"anxiety", "hiding", "excessive_thirst", "weight_gain"},
        "description": "Sudden complete blindness with no visible retinal changes initially. No treatment available.",
        "description_ja": "初期には網膜変化なく突然の完全失明を起こす疾患で、治療法はありません。",
        "urgency": "urgent",
    },
    # ---- Cardiovascular (expanded) ----
    {
        "name": "Sick Sinus Syndrome",
        "name_ja": "洞不全症候群",
        "symptoms": {"lethargy", "seizures", "excessive_panting"},
        "description": "A disorder of the heart's electrical system causing abnormally slow heart rate and fainting.",
        "description_ja": "心臓の電気伝導系障害により、異常な徐脈と失神を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Ventricular Septal Defect (VSD)",
        "name_ja": "心室中隔欠損症（VSD）",
        "symptoms": {"difficulty_breathing", "lethargy", "coughing", "excessive_panting", "collapse"},
        "description": "A congenital hole between the heart's ventricles, causing abnormal blood flow and exercise intolerance.",
        "description_ja": "心室間の先天性欠損孔で、異常な血流を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Atrial Fibrillation",
        "name_ja": "心房細動",
        "symptoms": {"lethargy", "difficulty_breathing", "coughing", "bloated_abdomen"},
        "description": "An irregular heart rhythm common in large-breed dogs with underlying heart disease.",
        "description_ja": "心疾患を有する大型犬に多い不整脈で、心機能低下を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Infective Endocarditis",
        "name_ja": "感染性心内膜炎",
        "symptoms": {"fever", "lethargy", *_ANY_LIMPING, "appetite_loss"},
        "description": "A bacterial infection of the heart valves causing fever, lameness, and embolic complications.",
        "description_ja": "心臓弁の細菌感染で、発熱・跛行・塞栓性合併症を引き起こします。",
        "urgency": "emergency",
    },
    # ---- Respiratory (expanded) ----
    {
        "name": "Pulmonary Fibrosis",
        "name_ja": "肺線維症",
        "symptoms": {"coughing", "difficulty_breathing", "rapid_breathing", "lethargy"},
        "description": "Progressive scarring of lung tissue reducing oxygen exchange, common in West Highland White Terriers.",
        "description_ja": "肺組織の進行性線維化で、ウエスティに多く、酸素交換能が低下します。",
        "urgency": "normal",
    },
    {
        "name": "Nasal Tumor",
        "name_ja": "鼻腔腫瘍",
        "symptoms": {"sneezing", "nasal_discharge", "eye_redness", "pain_on_touch"},
        "description": "Tumors of the nasal cavity causing chronic nasal discharge, epistaxis, and facial deformity.",
        "description_ja": "鼻腔の腫瘍で、慢性鼻汁・鼻出血・顔面変形を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Lung Lobe Torsion",
        "name_ja": "肺葉捻転",
        "symptoms": {"difficulty_breathing", "coughing", "lethargy", "rapid_breathing"},
        "description": "Rotation of a lung lobe on its axis, cutting off blood supply and causing respiratory distress.",
        "description_ja": "肺葉が軸回転し血流が遮断される緊急疾患で、呼吸困難を引き起こします。",
        "urgency": "emergency",
    },
    # ---- Neuro (expanded) ----
    {
        "name": "Cerebellar Hypoplasia",
        "name_ja": "小脳低形成",
        "symptoms": {"circling", "head_tilting", "stiffness"},
        "description": "Underdevelopment of the cerebellum causing tremors and incoordination from birth.",
        "description_ja": "小脳の発育不全で、出生時から振戦と運動失調を示します。",
        "urgency": "normal",
    },
    {
        "name": "Tick Paralysis",
        "name_ja": "マダニ麻痺",
        "symptoms": {*_ANY_LIMPING, "stiffness", "difficulty_breathing", "reluctance_move"},
        "description": "Ascending paralysis caused by neurotoxin in tick saliva, reversible upon tick removal.",
        "description_ja": "マダニ唾液の神経毒による上行性麻痺で、ダニ除去により回復します。",
        "urgency": "emergency",
    },
    {
        "name": "Fibrocartilaginous Embolism (FCE)",
        "name_ja": "線維軟骨塞栓症（FCE）",
        "symptoms": {*_ANY_LIMPING, "pain_on_touch", "reluctance_move"},
        "description": "Sudden spinal cord infarction from disc material, causing acute non-progressive paralysis.",
        "description_ja": "椎間板物質による突然の脊髄梗塞で、急性の非進行性麻痺を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Canine Distemper Encephalitis",
        "name_ja": "ジステンパー脳炎",
        "symptoms": {"seizures", "circling", "head_tilting", "stiffness", "anxiety"},
        "description": "Neurological complications of canine distemper causing seizures and myoclonus.",
        "description_ja": "犬ジステンパーの神経学的合併症で、痙攣とミオクローヌスを引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Scotty Cramp",
        "name_ja": "スコティクランプ",
        "symptoms": {"stiffness", "reluctance_move", "anxiety"},
        "description": "A hereditary movement disorder in Scottish Terriers causing muscle stiffness during excitement.",
        "description_ja": "スコティッシュテリアの遺伝性運動障害で、興奮時に筋硬直を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Cauda Equina Syndrome (Lumbosacral Stenosis)",
        "name_ja": "馬尾症候群（腰仙部狭窄症）",
        "symptoms": {"pain_on_touch", "reluctance_move", "stiffness", "incontinence"},
        "description": "Compression of nerve roots at the lumbosacral junction causing pain and hind-limb weakness.",
        "description_ja": "腰仙部の神経根圧迫により、痛みと後肢の衰弱を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Brain Tumor",
        "name_ja": "脳腫瘍",
        "symptoms": {"seizures", "circling", "head_tilting", "aggression_change", "lethargy"},
        "description": "Primary or metastatic tumors of the brain causing progressive neurological signs.",
        "description_ja": "脳の原発性または転移性腫瘍で、進行性の神経症状を引き起こします。",
        "urgency": "urgent",
    },
    # ---- Musculoskeletal (expanded) ----
    {
        "name": "Spondylosis Deformans",
        "name_ja": "変形性脊椎症",
        "symptoms": {"stiffness", "reluctance_move", "pain_on_touch"},
        "description": "Age-related bony spurs along the spine, usually incidental but can cause stiffness.",
        "description_ja": "加齢に伴う脊椎の骨棘形成で、通常は偶発所見ですが硬直を引き起こすことがあります。",
        "urgency": "normal",
    },
    {
        "name": "Masticatory Muscle Myositis",
        "name_ja": "咀嚼筋炎",
        "symptoms": {"pain_on_touch", "appetite_loss", "fever", "swollen_joints"},
        "description": "An immune-mediated inflammatory disease of the jaw muscles causing pain and inability to open the mouth.",
        "description_ja": "咀嚼筋の免疫介在性炎症で、痛みと開口障害を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Craniomandibular Osteopathy",
        "name_ja": "頭蓋下顎骨骨症",
        "symptoms": {"pain_on_touch", "fever", "appetite_loss"},
        "description": "Abnormal bone growth of the skull and jaw in young terrier breeds, causing pain when eating.",
        "description_ja": "若齢テリア犬種の頭蓋骨と下顎の異常骨成長で、食事時の痛みを引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Immune-Mediated Polyarthritis (IMPA)",
        "name_ja": "免疫介在性多発性関節炎",
        "symptoms": {"swollen_joints", *_ANY_LIMPING, "fever", "lethargy", "stiffness"},
        "description": "An autoimmune condition causing inflammation in multiple joints simultaneously.",
        "description_ja": "複数の関節に同時に炎症を引き起こす自己免疫疾患です。",
        "urgency": "normal",
    },
    {
        "name": "Luxating Shoulder",
        "name_ja": "肩関節脱臼",
        "symptoms": {"limping_fl", "limping_fr", "pain_on_touch", "reluctance_move"},
        "description": "Displacement of the shoulder joint, either congenital or traumatic.",
        "description_ja": "肩関節の脱臼で、先天性または外傷性に分類されます。",
        "urgency": "normal",
    },
    {
        "name": "Hypertrophic Osteopathy",
        "name_ja": "肥大性骨症",
        "symptoms": {"swollen_joints", *_ANY_LIMPING, "lethargy"},
        "description": "Painful bone proliferation in the limbs secondary to intrathoracic disease (usually lung tumors).",
        "description_ja": "胸腔内疾患（主に肺腫瘍）に続発する四肢の骨増殖で、痛みを伴います。",
        "urgency": "urgent",
    },
    # ---- Skin (expanded) ----
    {
        "name": "Discoid Lupus Erythematosus (DLE)",
        "name_ja": "円板状エリテマトーデス",
        "symptoms": {"skin_redness", "hair_loss", "dry_skin"},
        "description": "An autoimmune skin disease causing depigmentation and crusting of the nose and face.",
        "description_ja": "鼻と顔面の色素脱失と痂皮を引き起こす自己免疫性皮膚疾患です。",
        "urgency": "normal",
    },
    {
        "name": "Follicular Dysplasia",
        "name_ja": "毛包形成異常",
        "symptoms": {"hair_loss", "dry_skin"},
        "description": "A hereditary hair follicle disorder causing patterned alopecia, often color-linked.",
        "description_ja": "遺伝性の毛包疾患で、パターン状の脱毛を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Dermoid Sinus",
        "name_ja": "類皮洞",
        "symptoms": {"lumps", "pain_on_touch", "fever"},
        "description": "A congenital neural tube defect causing tubular skin invaginations along the dorsal midline.",
        "description_ja": "背側正中線に沿った管状の皮膚陥入を引き起こす先天性神経管欠損です。",
        "urgency": "normal",
    },
    {
        "name": "Zinc-Responsive Dermatosis",
        "name_ja": "亜鉛反応性皮膚症",
        "symptoms": {"skin_redness", "dry_skin", "hair_loss"},
        "description": "Skin disease from zinc deficiency or malabsorption, common in Huskies and Malamutes.",
        "description_ja": "亜鉛欠乏または吸収障害による皮膚疾患で、ハスキーやマラミュートに多いです。",
        "urgency": "normal",
    },
    {
        "name": "Malassezia Dermatitis",
        "name_ja": "マラセチア皮膚炎",
        "symptoms": {"itching", "skin_redness", "ear_odor", "ear_scratching"},
        "description": "Yeast overgrowth on the skin causing greasy, itchy, malodorous skin and ear infections.",
        "description_ja": "皮膚の酵母過剰増殖で、脂っぽく痒みのある悪臭を伴う皮膚・耳感染症です。",
        "urgency": "normal",
    },
    {
        "name": "Systemic Lupus Erythematosus (SLE)",
        "name_ja": "全身性エリテマトーデス（SLE）",
        "symptoms": {"fever", "swollen_joints", "skin_redness", "lethargy", "appetite_loss"},
        "description": "A serious autoimmune disease affecting multiple organ systems including skin, joints, and kidneys.",
        "description_ja": "皮膚・関節・腎臓を含む多臓器を侵す重篤な自己免疫疾患です。",
        "urgency": "urgent",
    },
    {
        "name": "Interdigital Cyst (Furuncle)",
        "name_ja": "趾間嚢胞（フルンクル）",
        "symptoms": {"limping_fl", "limping_fr", "skin_redness", "pain_on_touch"},
        "description": "Painful nodules between the toes caused by foreign bodies, infection, or allergies.",
        "description_ja": "異物・感染・アレルギーによる趾間の痛みを伴う結節です。",
        "urgency": "normal",
    },
    {
        "name": "Seborrhea",
        "name_ja": "脂漏症",
        "symptoms": {"dry_skin", "itching", "ear_odor", "skin_redness"},
        "description": "Excessive scaling and greasiness of the skin, either primary (genetic) or secondary to other diseases.",
        "description_ja": "皮膚の過剰な落屑と脂っぽさで、原発性（遺伝性）または続発性があります。",
        "urgency": "normal",
    },
    # ---- Digestive (expanded) ----
    {
        "name": "Gastric Ulcer",
        "name_ja": "胃潰瘍",
        "symptoms": {"vomiting", "appetite_loss", "bloody_stool", "lethargy"},
        "description": "Erosions of the stomach lining often caused by NSAIDs, stress, or liver/kidney disease.",
        "description_ja": "NSAIDs・ストレス・肝腎疾患による胃粘膜のびらんです。",
        "urgency": "urgent",
    },
    {
        "name": "Esophagitis",
        "name_ja": "食道炎",
        "symptoms": {"vomiting", "appetite_loss", "pain_on_touch"},
        "description": "Inflammation of the esophagus from acid reflux, foreign bodies, or chemical irritants.",
        "description_ja": "酸逆流・異物・化学刺激物による食道の炎症です。",
        "urgency": "normal",
    },
    {
        "name": "Protein-Losing Enteropathy (PLE)",
        "name_ja": "蛋白漏出性腸症（PLE）",
        "symptoms": {"diarrhea", "weight_loss", "bloated_abdomen", "lethargy"},
        "description": "Severe intestinal protein loss causing hypoalbuminemia, edema, and effusions.",
        "description_ja": "腸管からの重度のタンパク質喪失で、低アルブミン血症・浮腫・胸腹水を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Mesenteric Volvulus",
        "name_ja": "腸間膜捻転",
        "symptoms": {"bloated_abdomen", "vomiting", "lethargy", "pain_on_touch"},
        "description": "Twisting of the intestines cutting off blood supply, a life-threatening surgical emergency.",
        "description_ja": "腸管の捻転により血流が遮断される致命的な外科的緊急疾患です。",
        "urgency": "emergency",
    },
    {
        "name": "Rectal Prolapse",
        "name_ja": "直腸脱",
        "symptoms": {"diarrhea", "constipation", "bloody_stool"},
        "description": "Protrusion of rectal tissue through the anus, often secondary to chronic straining.",
        "description_ja": "慢性の怒責に続発することが多い、肛門からの直腸組織の突出です。",
        "urgency": "urgent",
    },
    {
        "name": "Anal Sac Disease",
        "name_ja": "肛門嚢疾患",
        "symptoms": {"pain_on_touch", "constipation"},
        "description": "Impaction, infection, or abscess of the anal glands causing pain and scooting behavior.",
        "description_ja": "肛門腺の貯留・感染・膿瘍で、痛みと地面に尻をこする行動を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Intestinal Intussusception",
        "name_ja": "腸重積",
        "symptoms": {"vomiting", "bloody_stool", "lethargy", "appetite_loss", "bloated_abdomen"},
        "description": "Telescoping of one intestinal segment into another, a surgical emergency in puppies.",
        "description_ja": "腸管の一部が隣接部に嵌入する疾患で、子犬の外科的緊急疾患です。",
        "urgency": "emergency",
    },
    # ---- Endocrine (expanded) ----
    {
        "name": "Diabetes Insipidus",
        "name_ja": "尿崩症",
        "symptoms": {"excessive_thirst", "excessive_urination"},
        "description": "A disorder of water balance causing extreme thirst and dilute urine, unrelated to blood sugar.",
        "description_ja": "水分バランスの障害で、極度の多渇と希釈尿を引き起こします。血糖とは無関係です。",
        "urgency": "normal",
    },
    {
        "name": "Pheochromocytoma",
        "name_ja": "褐色細胞腫",
        "symptoms": {"anxiety", "excessive_panting", "lethargy", "appetite_loss"},
        "description": "An adrenal gland tumor producing excess catecholamines, causing episodic hypertension.",
        "description_ja": "副腎の腫瘍で過剰なカテコラミンを産生し、発作的な高血圧を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Growth Hormone-Responsive Dermatosis",
        "name_ja": "成長ホルモン反応性皮膚症",
        "symptoms": {"hair_loss", "dry_skin"},
        "description": "Bilateral symmetric alopecia related to growth hormone deficiency, common in Pomeranians.",
        "description_ja": "成長ホルモン不足に関連する両側対称性脱毛で、ポメラニアンに多いです。",
        "urgency": "normal",
    },
    # ---- Reproductive (expanded) ----
    {
        "name": "Vaginitis",
        "name_ja": "膣炎",
        "symptoms": {"genital_discharge", "excessive_urination"},
        "description": "Inflammation of the vagina causing discharge, common in prepubertal and spayed females.",
        "description_ja": "膣の炎症で分泌物を引き起こし、未発情犬や避妊犬に多いです。",
        "urgency": "normal",
    },
    {
        "name": "Testicular Tumor",
        "name_ja": "精巣腫瘍",
        "symptoms": {"genital_discharge", "hair_loss", "lethargy"},
        "description": "Tumors of the testicle including Sertoli cell, seminoma, and interstitial cell types.",
        "description_ja": "セルトリ細胞腫・セミノーマ・間質細胞腫を含む精巣の腫瘍です。",
        "urgency": "normal",
    },
    {
        "name": "Paraphimosis",
        "name_ja": "嵌頓包茎",
        "symptoms": {"genital_discharge", "anxiety", "pain_on_touch"},
        "description": "Inability to retract the penis into the prepuce, a urological emergency requiring prompt treatment.",
        "description_ja": "陰茎を包皮内に戻せない泌尿器科的緊急疾患です。",
        "urgency": "emergency",
    },
    {
        "name": "Dystocia",
        "name_ja": "難産",
        "symptoms": {"anxiety", "excessive_panting", "lethargy", "pain_on_touch"},
        "description": "Difficulty during labor requiring veterinary intervention, common in brachycephalic breeds.",
        "description_ja": "分娩困難で獣医学的介入を要し、短頭種に多いです。",
        "urgency": "emergency",
    },
    # ---- Toxicology / Poisoning ----
    {
        "name": "Chocolate Toxicosis",
        "name_ja": "チョコレート中毒",
        "symptoms": {"vomiting", "diarrhea", "anxiety", "excessive_panting", "seizures"},
        "description": "Theobromine and caffeine poisoning from chocolate ingestion, severity depends on type and amount.",
        "description_ja": "チョコレートに含まれるテオブロミンとカフェインによる中毒で、種類と量により重症度が異なります。",
        "urgency": "emergency",
    },
    {
        "name": "Grape/Raisin Toxicosis",
        "name_ja": "ブドウ・レーズン中毒",
        "symptoms": {"vomiting", "appetite_loss", "lethargy", "excessive_thirst"},
        "description": "Acute kidney injury from grape or raisin ingestion. Even small amounts can be fatal.",
        "description_ja": "ブドウやレーズンの摂取による急性腎障害で、少量でも致命的になりえます。",
        "urgency": "emergency",
    },
    {
        "name": "Xylitol Poisoning",
        "name_ja": "キシリトール中毒",
        "symptoms": {"vomiting", "lethargy", "seizures"},
        "description": "Severe hypoglycemia and liver failure from xylitol (sugar-free sweetener) ingestion.",
        "description_ja": "キシリトール（無糖甘味料）の摂取による重度の低血糖と肝不全です。",
        "urgency": "emergency",
    },
    {
        "name": "NSAID Toxicosis",
        "name_ja": "鎮痛剤中毒（NSAID）",
        "symptoms": {"vomiting", "appetite_loss", "bloody_stool", "lethargy"},
        "description": "GI ulceration and kidney damage from ibuprofen, naproxen, or other human painkillers.",
        "description_ja": "イブプロフェン等のヒト用鎮痛剤によるGI潰瘍と腎障害です。",
        "urgency": "emergency",
    },
    {
        "name": "Rodenticide Poisoning",
        "name_ja": "殺鼠剤中毒",
        "symptoms": {"lethargy", "difficulty_breathing", "bloated_abdomen", "appetite_loss"},
        "description": "Anticoagulant rat poison causing internal bleeding, or bromethalin causing neurological signs.",
        "description_ja": "抗凝固性殺鼠剤による内出血、またはブロメタリンによる神経症状です。",
        "urgency": "emergency",
    },
    {
        "name": "Onion/Garlic Toxicosis",
        "name_ja": "タマネギ・ニンニク中毒",
        "symptoms": {"vomiting", "diarrhea", "lethargy", "rapid_breathing"},
        "description": "Heinz body anemia from allium family vegetables destroying red blood cells.",
        "description_ja": "ネギ属の野菜による赤血球破壊（ハインツ小体貧血）です。",
        "urgency": "urgent",
    },
    {
        "name": "Ethylene Glycol Poisoning (Antifreeze)",
        "name_ja": "エチレングリコール中毒（不凍液）",
        "symptoms": {"vomiting", "excessive_thirst", "seizures", "lethargy"},
        "description": "Lethal antifreeze poisoning causing rapid kidney failure. Treatment must begin within hours.",
        "description_ja": "不凍液による致命的な中毒で、急速な腎不全を引き起こします。数時間以内の治療が必要です。",
        "urgency": "emergency",
    },
    {
        "name": "Marijuana Toxicosis",
        "name_ja": "大麻中毒",
        "symptoms": {"lethargy", "vomiting", "incontinence", "anxiety", "seizures"},
        "description": "THC intoxication causing depression, incoordination, and urinary incontinence.",
        "description_ja": "THC中毒で、沈鬱・運動失調・尿失禁を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Lead Poisoning",
        "name_ja": "鉛中毒",
        "symptoms": {"vomiting", "seizures", "lethargy", "appetite_loss"},
        "description": "Chronic or acute lead ingestion causing GI and neurological signs.",
        "description_ja": "鉛の慢性または急性摂取による消化器・神経症状です。",
        "urgency": "urgent",
    },
    # ---- Environmental / Other ----
    {
        "name": "Heat Stroke",
        "name_ja": "熱中症",
        "symptoms": {"excessive_panting", "lethargy", "vomiting", "rapid_breathing", "seizures"},
        "description": "Life-threatening hyperthermia from heat exposure, especially in brachycephalic breeds.",
        "description_ja": "高温環境による生命を脅かす高体温症で、短頭種に特に危険です。",
        "urgency": "emergency",
    },
    {
        "name": "Hypothermia",
        "name_ja": "低体温症",
        "symptoms": {"lethargy", "stiffness", "difficulty_breathing"},
        "description": "Dangerously low body temperature from cold exposure, especially in small or toy breeds.",
        "description_ja": "低温環境による危険な低体温で、小型犬・トイ犬種に特にリスクが高いです。",
        "urgency": "emergency",
    },
    {
        "name": "Drowning / Near-Drowning",
        "name_ja": "溺水・溺水ニアミス",
        "symptoms": {"coughing", "difficulty_breathing", "lethargy", "rapid_breathing", "fever"},
        "description": "Water aspiration causing pulmonary edema. Secondary drowning can occur hours later.",
        "description_ja": "水の誤嚥による肺水腫で、数時間後に二次的溺水が起こることがあります。",
        "urgency": "emergency",
    },
    {
        "name": "Snakebite Envenomation",
        "name_ja": "毒蛇咬傷",
        "symptoms": {"pain_on_touch", "lethargy", "vomiting", "difficulty_breathing", "swollen_joints"},
        "description": "Venomous snake bite causing local swelling, pain, and potentially fatal systemic effects.",
        "description_ja": "毒蛇咬傷による局所腫脹・痛み・致命的な全身影響を引き起こします。",
        "urgency": "emergency",
    },
    {
        "name": "Bee/Wasp Sting Anaphylaxis",
        "name_ja": "蜂刺傷アナフィラキシー",
        "symptoms": {"vomiting", "difficulty_breathing", "lethargy", "skin_redness"},
        "description": "Severe allergic reaction to insect stings causing facial swelling and potential anaphylactic shock.",
        "description_ja": "虫刺されに対する重篤なアレルギー反応で、顔面腫脹とアナフィラキシーショックを引き起こします。",
        "urgency": "emergency",
    },
    {
        "name": "Foreign Body in Ear",
        "name_ja": "耳内異物（草の実等）",
        "symptoms": {"ear_scratching", "head_tilting", "ear_odor", "pain_on_touch"},
        "description": "Grass awns or other foreign objects lodged in the ear canal causing acute pain and head shaking.",
        "description_ja": "草の実等が外耳道に入り込み、急性の痛みと頭を振る行動を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Gastric Foreign Body",
        "name_ja": "胃内異物",
        "symptoms": {"vomiting", "appetite_loss", "lethargy", "regurgitation", "vomiting_after_drinking", "drooling", "abdominal_pain"},
        "description": "Foreign objects in the stomach causing persistent vomiting even after drinking water, regurgitation, and drooling.",
        "description_ja": "胃内の異物で、水を飲んでも吐く持続的な嘔吐、吐出、流涎を引き起こします。",
        "urgency": "urgent",
    },
    # ---- Tumors (expanded) ----
    {
        "name": "Histiocytic Sarcoma",
        "name_ja": "組織球肉腫",
        "symptoms": {"lethargy", "weight_loss", "appetite_loss", "difficulty_breathing", *_ANY_LIMPING},
        "description": "An aggressive cancer of histiocyte cells, common in Bernese Mountain Dogs and Flat-Coated Retrievers.",
        "description_ja": "組織球由来の悪性腫瘍で、バーニーズやフラットコーテッドレトリーバーに多いです。",
        "urgency": "urgent",
    },
    {
        "name": "Fibrosarcoma",
        "name_ja": "線維肉腫",
        "symptoms": {"lumps", "pain_on_touch", *_ANY_LIMPING},
        "description": "A malignant tumor of connective tissue, locally aggressive with high recurrence rate.",
        "description_ja": "結合組織の悪性腫瘍で、局所浸潤性が高く再発率も高いです。",
        "urgency": "normal",
    },
    {
        "name": "Anal Sac Adenocarcinoma",
        "name_ja": "肛門嚢腺癌",
        "symptoms": {"constipation", "pain_on_touch", "excessive_thirst"},
        "description": "A malignant tumor of the anal glands causing elevated calcium levels and straining.",
        "description_ja": "肛門腺の悪性腫瘍で、高カルシウム血症と排便困難を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Insulinoma (Pancreatic Beta Cell Tumor)",
        "name_ja": "膵臓β細胞腫瘍",
        "symptoms": {"seizures", "lethargy", "stiffness", "anxiety"},
        "description": "A functional pancreatic tumor overproducing insulin and causing severe hypoglycemia.",
        "description_ja": "インスリンを過剰産生する膵臓の機能性腫瘍で、重度の低血糖を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Thyroid Carcinoma",
        "name_ja": "甲状腺がん",
        "symptoms": {"lumps", "coughing", "difficulty_breathing"},
        "description": "A malignant tumor of the thyroid gland, often presenting as a neck mass.",
        "description_ja": "甲状腺の悪性腫瘍で、頸部の腫瘤として発見されることが多いです。",
        "urgency": "normal",
    },
    {
        "name": "Perianal Adenoma",
        "name_ja": "肛門周囲腺腫",
        "symptoms": {"lumps", "constipation", "bloody_stool"},
        "description": "A common benign tumor around the anus in intact male dogs, hormone-dependent.",
        "description_ja": "未去勢のオス犬に多い肛門周囲の良性ホルモン依存性腫瘍です。",
        "urgency": "normal",
    },
    {
        "name": "Hepatocellular Carcinoma",
        "name_ja": "肝細胞がん",
        "symptoms": {"appetite_loss", "weight_loss", "lethargy", "bloated_abdomen", "vomiting"},
        "description": "A primary malignant liver tumor. Massive form has a better prognosis with surgical resection.",
        "description_ja": "肝臓の原発性悪性腫瘍で、巨大型は外科的切除により予後が比較的良好です。",
        "urgency": "normal",
    },
    {
        "name": "Chemodectoma (Heart Base Tumor)",
        "name_ja": "化学受容器腫（心基底部腫瘍）",
        "symptoms": {"difficulty_breathing", "coughing", "lethargy", "bloated_abdomen", "collapse"},
        "description": "A tumor at the base of the heart, common in brachycephalic breeds, causing pericardial effusion.",
        "description_ja": "心臓基底部の腫瘍で、短頭種に多く、心嚢液貯留を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Nasal Adenocarcinoma",
        "name_ja": "鼻腔腺がん",
        "symptoms": {"sneezing", "nasal_discharge", "eye_redness"},
        "description": "The most common malignant nasal tumor in dogs, causing chronic unilateral nasal discharge.",
        "description_ja": "犬で最も多い鼻腔悪性腫瘍で、片側性の慢性鼻汁を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Soft Tissue Sarcoma",
        "name_ja": "軟部組織肉腫",
        "symptoms": {"lumps", "pain_on_touch"},
        "description": "A group of locally invasive tumors arising from connective tissue beneath the skin.",
        "description_ja": "皮下の結合組織から発生する局所浸潤性の腫瘍群です。",
        "urgency": "normal",
    },
    {
        "name": "Lipoma",
        "name_ja": "脂肪腫",
        "symptoms": {"lumps"},
        "description": "A common benign fatty tumor found under the skin. Usually harmless but may need removal if large.",
        "description_ja": "皮下に発生する一般的な良性脂肪腫瘍で、大きくなった場合は切除が必要なこともあります。",
        "urgency": "normal",
    },
    {
        "name": "Plasmacytoma",
        "name_ja": "形質細胞腫",
        "symptoms": {"lumps", "skin_redness"},
        "description": "A tumor of plasma cells, often solitary and cutaneous with generally good prognosis after excision.",
        "description_ja": "形質細胞の腫瘍で、孤立性皮膚型が多く切除後の予後は一般に良好です。",
        "urgency": "normal",
    },
    # ---- Behavioral ----
    {
        "name": "Separation Anxiety",
        "name_ja": "分離不安症",
        "symptoms": {"anxiety", "hiding", "excessive_panting", "aggression_change"},
        "description": "Extreme distress when separated from owners, causing destructive behavior and vocalization.",
        "description_ja": "飼い主との分離時の極度の苦痛で、破壊行動や鳴き声を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Compulsive Disorder (Canine OCD)",
        "name_ja": "強迫性障害",
        "symptoms": {"circling", "anxiety", "itching"},
        "description": "Repetitive behaviors like tail chasing, flank sucking, or shadow chasing beyond normal patterns.",
        "description_ja": "尾追い・脇腹吸い・影追いなど正常範囲を超えた反復行動です。",
        "urgency": "normal",
    },
    {
        "name": "Noise Phobia",
        "name_ja": "音響恐怖症",
        "symptoms": {"anxiety", "hiding", "excessive_panting"},
        "description": "Extreme fear response to sounds like thunderstorms, fireworks, or gunshots.",
        "description_ja": "雷・花火・銃声などの音に対する極度の恐怖反応です。",
        "urgency": "normal",
    },
    {
        "name": "Pica",
        "name_ja": "異食症",
        "symptoms": {"vomiting", "diarrhea", "appetite_loss", "anxiety", "drooling", "abdominal_pain"},
        "description": "Compulsive eating of non-food objects like rocks, fabric, or plastic.",
        "description_ja": "石・布・プラスチックなど非食物を強迫的に食べる行動障害です。",
        "urgency": "normal",
    },
    # ---- Hematologic (expanded) ----
    {
        "name": "Disseminated Intravascular Coagulation (DIC)",
        "name_ja": "播種性血管内凝固（DIC）",
        "symptoms": {"lethargy", "rapid_breathing", "skin_redness", "vomiting"},
        "description": "A life-threatening coagulation cascade disorder causing simultaneous clotting and bleeding.",
        "description_ja": "凝固と出血が同時に起こる致命的な凝固異常で、基礎疾患の合併症です。",
        "urgency": "emergency",
    },
    {
        "name": "Anemia of Chronic Disease",
        "name_ja": "慢性疾患に伴う貧血",
        "symptoms": {"lethargy", "rapid_breathing", "appetite_loss"},
        "description": "Non-regenerative anemia secondary to chronic inflammation, infection, or cancer.",
        "description_ja": "慢性炎症・感染症・がんに続発する非再生性貧血です。",
        "urgency": "normal",
    },
    {
        "name": "Evan's Syndrome",
        "name_ja": "エバンス症候群",
        "symptoms": {"lethargy", "skin_redness", "rapid_breathing", "fever"},
        "description": "Concurrent IMHA and immune-mediated thrombocytopenia, a serious autoimmune condition.",
        "description_ja": "IMHAと免疫介在性血小板減少症の同時発生で、重篤な自己免疫疾患です。",
        "urgency": "emergency",
    },
    # ---- Urinary (expanded) ----
    {
        "name": "Glomerulonephritis",
        "name_ja": "糸球体腎炎",
        "symptoms": {"excessive_thirst", "excessive_urination", "weight_loss", "lethargy", "bloated_abdomen"},
        "description": "Immune-mediated inflammation of the kidney glomeruli causing protein loss and kidney failure.",
        "description_ja": "腎糸球体の免疫介在性炎症で、蛋白漏出と腎不全を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Pyelonephritis",
        "name_ja": "腎盂腎炎",
        "symptoms": {"fever", "vomiting", "appetite_loss", "excessive_thirst", "pain_on_touch"},
        "description": "Bacterial infection of the kidney, often ascending from the lower urinary tract.",
        "description_ja": "下部尿路から上行性に感染する腎臓の細菌感染症です。",
        "urgency": "urgent",
    },
    {
        "name": "Urethral Obstruction",
        "name_ja": "尿道閉塞",
        "symptoms": {"straining_urinate", "pain_on_touch", "vomiting", "lethargy"},
        "description": "Complete blockage of the urethra by stones or mucus plug, a life-threatening emergency in males.",
        "description_ja": "結石や粘液栓による尿道の完全閉塞で、オス犬では致命的な緊急疾患です。",
        "urgency": "emergency",
    },
    # ---- Dental (expanded) ----
    {
        "name": "Tooth Fracture",
        "name_ja": "歯の破折",
        "symptoms": {"appetite_loss", "pain_on_touch"},
        "description": "Broken teeth from chewing hard objects, potentially exposing the pulp and causing infection.",
        "description_ja": "硬い物を噛むことによる歯の破折で、歯髄露出と感染のリスクがあります。",
        "urgency": "normal",
    },
    {
        "name": "Oral Melanoma",
        "name_ja": "口腔メラノーマ",
        "symptoms": {"appetite_loss", "lumps", "weight_loss"},
        "description": "The most common malignant oral tumor in dogs, highly aggressive with early metastasis.",
        "description_ja": "犬で最も多い口腔悪性腫瘍で、早期に転移する高悪性度腫瘍です。",
        "urgency": "urgent",
    },
    {
        "name": "Epulis (Gingival Mass)",
        "name_ja": "エプリス（歯肉腫瘤）",
        "symptoms": {"lumps", "appetite_loss"},
        "description": "A benign or locally invasive gingival mass. Most common oral tumor in dogs.",
        "description_ja": "良性または局所浸潤性の歯肉腫瘤で、犬で最も多い口腔腫瘍です。",
        "urgency": "normal",
    },
    {
        "name": "Stomatitis",
        "name_ja": "口内炎",
        "symptoms": {"appetite_loss", "pain_on_touch", "fever"},
        "description": "Severe inflammation of the oral mucosa causing pain and difficulty eating.",
        "description_ja": "口腔粘膜の重度の炎症で、痛みと摂食困難を引き起こします。",
        "urgency": "normal",
    },
    # ---- Genetic / Congenital (expanded) ----
    {
        "name": "Cleft Palate",
        "name_ja": "口蓋裂",
        "symptoms": {"sneezing", "nasal_discharge", "coughing"},
        "description": "A congenital defect where the palate doesn't fuse, causing nasal regurgitation in neonates.",
        "description_ja": "口蓋が癒合しない先天性欠損で、新生子犬の鼻逆流を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Portosystemic Shunt (Congenital)",
        "name_ja": "先天性門脈体循環シャント",
        "symptoms": {"seizures", "circling", "vomiting", "weight_loss"},
        "description": "A congenital vascular anomaly bypassing the liver, causing hepatic encephalopathy.",
        "description_ja": "肝臓を迂回する先天性血管異常で、肝性脳症を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Congenital Deafness",
        "name_ja": "先天性聴覚障害",
        "symptoms": {"aggression_change"},
        "description": "Hereditary deafness associated with white coat color and merle pattern, common in Dalmatians.",
        "description_ja": "白色被毛やマール模様と関連する遺伝性聴覚障害で、ダルメシアンに多いです。",
        "urgency": "normal",
    },
    {
        "name": "Atlantoaxial Instability",
        "name_ja": "環軸椎不安定症",
        "symptoms": {"pain_on_touch", "stiffness", "reluctance_move", "seizures"},
        "description": "Instability between the first two cervical vertebrae causing spinal cord compression in toy breeds.",
        "description_ja": "第1・第2頸椎間の不安定性で、トイ犬種の脊髄圧迫を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Persistent Right Aortic Arch (PRAA)",
        "name_ja": "右大動脈弓遺残",
        "symptoms": {"regurgitation", "weight_loss", "coughing", "drooling", "difficulty_breathing"},
        "description": "A vascular ring anomaly compressing the esophagus, causing regurgitation in weaning puppies.",
        "description_ja": "食道を圧迫する血管輪異常で、離乳期の子犬に吐き戻しを引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Mucopolysaccharidosis",
        "name_ja": "ムコ多糖症",
        "symptoms": {"stiffness", "reluctance_move", "squinting"},
        "description": "A lysosomal storage disease causing skeletal abnormalities and corneal cloudiness.",
        "description_ja": "リソソーム蓄積症で、骨格異常と角膜混濁を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Glycogen Storage Disease",
        "name_ja": "グリコーゲン蓄積症",
        "symptoms": {"lethargy", "seizures", "reluctance_move"},
        "description": "A hereditary metabolic disorder affecting glycogen metabolism, causing muscle weakness.",
        "description_ja": "グリコーゲン代謝に影響する遺伝性代謝疾患で、筋力低下を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Malignant Hyperthermia",
        "name_ja": "悪性高熱症",
        "symptoms": {"fever", "stiffness", "rapid_breathing", "seizures"},
        "description": "A life-threatening reaction to certain anesthetics causing extreme body temperature rise.",
        "description_ja": "特定の麻酔薬に対する致死的反応で、極度の体温上昇を引き起こします。",
        "urgency": "emergency",
    },
    # --- Additional diseases to reach 250 ---
    {
        "name": "Juvenile Cellulitis (Puppy Strangles)",
        "name_ja": "若年性蜂窩織炎（パピーストラングル）",
        "symptoms": {"swelling", "fever", "appetite_loss", "lethargy"},
        "description": "An immune-mediated skin condition in puppies causing facial swelling and lymph node enlargement.",
        "description_ja": "子犬に発生する免疫介在性皮膚疾患で、顔面の腫脹やリンパ節腫大を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Chylothorax",
        "name_ja": "乳び胸",
        "symptoms": {"rapid_breathing", "coughing", "lethargy", "appetite_loss"},
        "description": "Accumulation of lymphatic fluid (chyle) in the chest cavity causing respiratory distress.",
        "description_ja": "胸腔内にリンパ液（乳び）が貯留し、呼吸困難を引き起こす疾患です。",
        "urgency": "urgent",
    },
    {
        "name": "Megacolon",
        "name_ja": "巨大結腸症",
        "symptoms": {"constipation", "appetite_loss", "lethargy", "vomiting"},
        "description": "Severe dilation of the colon resulting in chronic constipation and inability to defecate normally.",
        "description_ja": "結腸の重度な拡張により、慢性便秘と正常な排便不能を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Cutaneous Histiocytoma",
        "name_ja": "皮膚組織球腫",
        "symptoms": {"lumps", "skin_lesions"},
        "description": "A benign skin tumor commonly seen in young dogs, appearing as a round, raised, hairless mass.",
        "description_ja": "若い犬に多く見られる良性皮膚腫瘍で、円形の隆起した無毛の腫瘤として現れます。",
        "urgency": "normal",
    },
    {
        "name": "Myocarditis",
        "name_ja": "心筋炎",
        "symptoms": {"lethargy", "rapid_breathing", "collapse", "appetite_loss"},
        "description": "Inflammation of the heart muscle, often caused by infection, leading to cardiac dysfunction.",
        "description_ja": "心筋の炎症で、しばしば感染により引き起こされ、心機能障害を招きます。",
        "urgency": "emergency",
    },
    {
        "name": "Hemolytic Uremic Syndrome",
        "name_ja": "溶血性尿毒症症候群",
        "symptoms": {"lethargy", "vomiting", "blood_urine", "appetite_loss"},
        "description": "A condition involving hemolytic anemia, low platelet count, and kidney failure.",
        "description_ja": "溶血性貧血、血小板減少、腎不全を伴う疾患です。",
        "urgency": "emergency",
    },
    {
        "name": "Aural Hematoma",
        "name_ja": "耳介血腫",
        "symptoms": {"swelling", "head_shaking", "ear_discharge"},
        "description": "A collection of blood between the ear cartilage and skin, usually caused by head shaking or ear scratching.",
        "description_ja": "耳の軟骨と皮膚の間に血液が溜まる状態で、通常は頭を振ったり耳を掻くことで発生します。",
        "urgency": "normal",
    },
]

# ---------------------------------------------------------------------------
# Diagnostic-test database
# ---------------------------------------------------------------------------
# Each entry:
#   name            – English test name
#   name_ja         – Japanese name
#   purpose         – what it checks
#   related_diseases – set of disease names this test is indicated for

_TEST_DB: list[dict[str, Any]] = [
    {
        "name": "CBC (Complete Blood Count)",
        "name_ja": "\u5168\u8840\u7403\u8a08\u7b97\uff08CBC\uff09",
        "purpose": "Evaluates red/white blood cells and platelets to detect "
                   "infections, anemia, clotting disorders, and blood cancers.",
        "related_diseases": {
            "Canine Parvovirus", "Canine Distemper", "Pancreatitis",
            "Urinary Tract Infection", "Kidney Disease (CKD)",
            "Liver Disease", "Cancer/Neoplasia",
            "Immune-Mediated Hemolytic Anemia", "Gastroenteritis",
            "Addison's Disease", "Pyometra", "Lyme Disease",
            "Heartworm Disease", "Intestinal Parasites",
        },
    },
    {
        "name": "Blood Chemistry Panel",
        "name_ja": "\u8840\u6db2\u5316\u5b66\u30d1\u30cd\u30eb",
        "purpose": "Measures organ function markers including liver enzymes, "
                   "kidney values, glucose, and electrolytes.",
        "related_diseases": {
            "Liver Disease", "Kidney Disease (CKD)", "Diabetes Mellitus",
            "Cushing's Disease", "Addison's Disease", "Pancreatitis",
            "Hyperthyroidism", "Hypothyroidism", "Pyometra",
        },
    },
    {
        "name": "Urinalysis",
        "name_ja": "\u5c3f\u691c\u67fb",
        "purpose": "Analyzes urine composition for signs of infection, "
                   "crystals, glucose, protein, and kidney function.",
        "related_diseases": {
            "Urinary Tract Infection", "Bladder Stones",
            "Kidney Disease (CKD)", "Diabetes Mellitus",
            "Cushing's Disease", "Prostate Disease",
        },
    },
    {
        "name": "X-ray (Radiograph)",
        "name_ja": "\u30ec\u30f3\u30c8\u30b2\u30f3\u691c\u67fb",
        "purpose": "Produces images of bones, organs, and soft tissue to "
                   "identify fractures, masses, and organ enlargement.",
        "related_diseases": {
            "Gastric Dilatation-Volvulus (GDV/Bloat)", "Heart Disease/CHF",
            "Intervertebral Disc Disease (IVDD)", "Hip Dysplasia",
            "Bladder Stones", "Cancer/Neoplasia", "Heartworm Disease",
            "Osteoarthritis", "Cruciate Ligament Injury",
        },
    },
    {
        "name": "Ultrasound",
        "name_ja": "\u8d85\u97f3\u6ce2\u691c\u67fb",
        "purpose": "Uses sound waves to visualize internal organs in real "
                   "time, helpful for abdominal and cardiac evaluation.",
        "related_diseases": {
            "Gastric Dilatation-Volvulus (GDV/Bloat)", "Heart Disease/CHF",
            "Pyometra", "Cancer/Neoplasia", "Liver Disease",
            "Pancreatitis", "Kidney Disease (CKD)", "Bladder Stones",
            "Prostate Disease",
        },
    },
    {
        "name": "Thyroid Panel (T4/TSH)",
        "name_ja": "\u7532\u72b6\u817a\u30d1\u30cd\u30eb\uff08T4/TSH\uff09",
        "purpose": "Measures thyroid hormone levels to diagnose hypo- or "
                   "hyperthyroidism.",
        "related_diseases": {
            "Hypothyroidism", "Hyperthyroidism",
        },
    },
    {
        "name": "ACTH Stimulation Test",
        "name_ja": "ACTH\u523a\u6fc0\u8a66\u9a13",
        "purpose": "Evaluates adrenal gland function to diagnose Cushing's "
                   "or Addison's disease.",
        "related_diseases": {
            "Cushing's Disease", "Addison's Disease",
        },
    },
    {
        "name": "Heartworm Antigen Test",
        "name_ja": "\u30d5\u30a3\u30e9\u30ea\u30a2\u6297\u539f\u691c\u67fb",
        "purpose": "Detects heartworm proteins in the blood to confirm "
                   "active heartworm infection.",
        "related_diseases": {
            "Heartworm Disease",
        },
    },
    {
        "name": "Fecal Examination",
        "name_ja": "\u7cde\u4fbf\u691c\u67fb",
        "purpose": "Microscopic analysis of stool to identify intestinal "
                   "parasites, eggs, or protozoa.",
        "related_diseases": {
            "Intestinal Parasites", "Gastroenteritis",
        },
    },
    {
        "name": "Tick-borne Disease Panel (4Dx)",
        "name_ja": "\u30c0\u30cb\u5a92\u4ecb\u6027\u75be\u60a3\u30d1\u30cd\u30eb\uff084Dx\uff09",
        "purpose": "Screens for Lyme disease, ehrlichiosis, anaplasmosis, "
                   "and heartworm in a single test.",
        "related_diseases": {
            "Lyme Disease", "Heartworm Disease",
        },
    },
    {
        "name": "Skin Scraping",
        "name_ja": "\u76ae\u819a\u63bb\u722a\u691c\u67fb",
        "purpose": "Collects skin cells to identify mites, fungi, or "
                   "bacteria under a microscope.",
        "related_diseases": {
            "Mange (Demodex/Sarcoptes)", "Fungal Infection (Ringworm)",
            "Allergic Dermatitis",
        },
    },
    {
        "name": "Allergy Testing",
        "name_ja": "\u30a2\u30ec\u30eb\u30ae\u30fc\u691c\u67fb",
        "purpose": "Identifies specific environmental or food allergens "
                   "triggering immune responses.",
        "related_diseases": {
            "Allergic Dermatitis",
        },
    },
    {
        "name": "Echocardiogram",
        "name_ja": "\u5fc3\u30a8\u30b3\u30fc\u691c\u67fb",
        "purpose": "Ultrasound of the heart to assess chamber size, valve "
                   "function, and blood flow.",
        "related_diseases": {
            "Heart Disease/CHF",
        },
    },
    {
        "name": "Electrocardiogram (ECG)",
        "name_ja": "\u5fc3\u96fb\u56f3\uff08ECG\uff09",
        "purpose": "Records electrical activity of the heart to detect "
                   "arrhythmias and conduction abnormalities.",
        "related_diseases": {
            "Heart Disease/CHF",
        },
    },
    {
        "name": "MRI",
        "name_ja": "MRI\u691c\u67fb",
        "purpose": "Provides detailed cross-sectional images of soft tissue, "
                   "brain, and spinal cord.",
        "related_diseases": {
            "Intervertebral Disc Disease (IVDD)", "Cancer/Neoplasia",
            "Epilepsy",
        },
    },
    {
        "name": "CT Scan",
        "name_ja": "CT\u30b9\u30ad\u30e3\u30f3",
        "purpose": "Produces detailed cross-sectional images for cancer "
                   "staging and complex structural evaluation.",
        "related_diseases": {
            "Cancer/Neoplasia",
        },
    },
    {
        "name": "Joint Fluid Analysis",
        "name_ja": "\u95a2\u7bc0\u6db2\u691c\u67fb",
        "purpose": "Examines synovial fluid for signs of infection, "
                   "inflammation, or immune-mediated disease.",
        "related_diseases": {
            "Osteoarthritis", "Lyme Disease",
            "Immune-Mediated Hemolytic Anemia", "Cruciate Ligament Injury",
        },
    },
    {
        "name": "Biopsy",
        "name_ja": "\u751f\u691c",
        "purpose": "Removes a tissue sample for histopathological examination "
                   "to diagnose tumors or skin conditions.",
        "related_diseases": {
            "Cancer/Neoplasia", "Mange (Demodex/Sarcoptes)",
            "Fungal Infection (Ringworm)",
        },
    },
    {
        "name": "Ophthalmologic Exam",
        "name_ja": "\u773c\u79d1\u691c\u67fb",
        "purpose": "Comprehensive evaluation of intraocular pressure, retina, "
                   "and ocular structures.",
        "related_diseases": {
            "Glaucoma", "Eye Infection (Conjunctivitis)",
        },
    },
    {
        "name": "Urine Culture",
        "name_ja": "\u5c3f\u57f9\u990a\u691c\u67fb",
        "purpose": "Identifies the specific bacteria causing a urinary tract "
                   "infection and determines antibiotic sensitivity.",
        "related_diseases": {
            "Urinary Tract Infection",
        },
    },
    {
        "name": "Pancreatitis Test (cPL/Spec cPL)",
        "name_ja": "\u81b5\u708e\u691c\u67fb\uff08cPL/Spec cPL\uff09",
        "purpose": "Measures canine pancreatic lipase to confirm or rule out "
                   "pancreatitis.",
        "related_diseases": {
            "Pancreatitis",
        },
    },
    {
        "name": "Bile Acids Test",
        "name_ja": "\u80c6\u6c41\u9178\u691c\u67fb",
        "purpose": "Evaluates liver function by measuring bile acid levels "
                   "before and after a meal.",
        "related_diseases": {
            "Liver Disease",
        },
    },
    {
        "name": "Blood Glucose Curve",
        "name_ja": "\u8840\u7cd6\u5024\u30ab\u30fc\u30d6",
        "purpose": "Monitors blood sugar fluctuations over several hours to "
                   "guide insulin dosing in diabetic patients.",
        "related_diseases": {
            "Diabetes Mellitus",
        },
    },
    {
        "name": "Coagulation Panel",
        "name_ja": "\u51dd\u56fa\u691c\u67fb",
        "purpose": "Assesses blood clotting function to detect bleeding "
                   "disorders or DIC.",
        "related_diseases": {
            "Immune-Mediated Hemolytic Anemia", "Liver Disease",
            "Cancer/Neoplasia",
        },
    },
    {
        "name": "EEG (Electroencephalogram)",
        "name_ja": "\u8133\u6ce2\u691c\u67fb\uff08EEG\uff09",
        "purpose": "Records brain electrical activity to help diagnose "
                   "epilepsy and other neurological conditions.",
        "related_diseases": {
            "Epilepsy",
        },
    },
]

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
        {"test": "Brachycephalic Assessment", "test_ja": "\u77ed\u982d\u7a2e\u8a55\u4fa1", "purpose": "Evaluate airway obstruction severity"},
        {"test": "Spine X-ray/CT", "test_ja": "\u810a\u690e\u30ec\u30f3\u30c8\u30b2\u30f3/CT", "purpose": "Screen for IVDD and hemivertebrae"},
        {"test": "Patella Evaluation", "test_ja": "\u819d\u84cb\u9aa8\u8a55\u4fa1", "purpose": "Check for patellar luxation grade"},
        {"test": "Hip Radiograph (PennHIP/OFA)", "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3", "purpose": "Screen for hip dysplasia"},
    ],
    "172d_poodle_toy": [
        {"test": "Patella Evaluation", "test_ja": "\u819d\u84cb\u9aa8\u8a55\u4fa1", "purpose": "Screen for patellar luxation"},
        {"test": "PRA DNA Test", "test_ja": "PRA\u907a\u4f1d\u5b50\u691c\u67fb", "purpose": "Test for progressive retinal atrophy gene"},
        {"test": "Allergy Panel", "test_ja": "\u30a2\u30ec\u30eb\u30ae\u30fc\u30d1\u30cd\u30eb", "purpose": "Identify environmental or food allergens"},
        {"test": "Thyroid Panel", "test_ja": "\u7532\u72b6\u817a\u30d1\u30cd\u30eb", "purpose": "Screen for thyroid dysfunction"},
    ],
    "122_labrador_retriever": [
        {"test": "Hip Radiograph (PennHIP/OFA)", "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3", "purpose": "Screen for hip dysplasia"},
        {"test": "Elbow Radiograph", "test_ja": "\u8098\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3", "purpose": "Screen for elbow dysplasia"},
        {"test": "EIC DNA Test", "test_ja": "EIC\u907a\u4f1d\u5b50\u691c\u67fb", "purpose": "Test for exercise-induced collapse gene"},
        {"test": "Ophthalmologic Exam", "test_ja": "\u773c\u79d1\u691c\u67fb", "purpose": "Screen for progressive retinal atrophy"},
        {"test": "Cardiac Exam", "test_ja": "\u5fc3\u81d3\u691c\u67fb", "purpose": "Screen for tricuspid valve dysplasia"},
    ],
    "166_german_shepherd": [
        {"test": "Hip Radiograph (PennHIP/OFA)", "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3", "purpose": "Screen for hip dysplasia"},
        {"test": "Elbow Radiograph", "test_ja": "\u8098\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3", "purpose": "Screen for elbow dysplasia"},
        {"test": "DM DNA Test", "test_ja": "DM\u907a\u4f1d\u5b50\u691c\u67fb", "purpose": "Test for degenerative myelopathy gene"},
        {"test": "Cardiac Exam", "test_ja": "\u5fc3\u81d3\u691c\u67fb", "purpose": "Screen for aortic stenosis"},
        {"test": "Allergy Panel", "test_ja": "\u30a2\u30ec\u30eb\u30ae\u30fc\u30d1\u30cd\u30eb", "purpose": "Identify environmental or food allergens"},
    ],
    "111_golden_retriever": [
        {"test": "Hip Radiograph (PennHIP/OFA)", "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3", "purpose": "Screen for hip dysplasia"},
        {"test": "Elbow Radiograph", "test_ja": "\u8098\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3", "purpose": "Screen for elbow dysplasia"},
        {"test": "Cardiac Exam", "test_ja": "\u5fc3\u81d3\u691c\u67fb", "purpose": "Screen for subvalvular aortic stenosis"},
        {"test": "Ophthalmologic Exam", "test_ja": "\u773c\u79d1\u691c\u67fb", "purpose": "Screen for cataracts and PRA"},
        {"test": "Thyroid Panel", "test_ja": "\u7532\u72b6\u817a\u30d1\u30cd\u30eb", "purpose": "Screen for hypothyroidism"},
        {"test": "Cancer Screening (Oncology Panel)", "test_ja": "\u816b\u760d\u30b9\u30af\u30ea\u30fc\u30cb\u30f3\u30b0", "purpose": "Early detection of lymphoma and hemangiosarcoma"},
    ],
    "218_chihuahua": [
        {"test": "Cardiac Exam", "test_ja": "\u5fc3\u81d3\u691c\u67fb", "purpose": "Screen for mitral valve disease"},
        {"test": "Patella Evaluation", "test_ja": "\u819d\u84cb\u9aa8\u8a55\u4fa1", "purpose": "Check for patellar luxation grade"},
        {"test": "Ophthalmologic Exam", "test_ja": "\u773c\u79d1\u691c\u67fb", "purpose": "Screen for lens luxation and glaucoma"},
    ],
    "257_shiba": [
        {"test": "Allergy Panel", "test_ja": "\u30a2\u30ec\u30eb\u30ae\u30fc\u30d1\u30cd\u30eb", "purpose": "Identify environmental or food allergens"},
        {"test": "Ophthalmologic Exam", "test_ja": "\u773c\u79d1\u691c\u67fb", "purpose": "Screen for glaucoma and cataracts"},
        {"test": "Patella Evaluation", "test_ja": "\u819d\u84cb\u9aa8\u8a55\u4fa1", "purpose": "Check for patellar luxation"},
        {"test": "Hip Radiograph (PennHIP/OFA)", "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3", "purpose": "Screen for hip dysplasia"},
    ],
    "161_beagle": [
        {"test": "Ophthalmologic Exam", "test_ja": "\u773c\u79d1\u691c\u67fb", "purpose": "Screen for glaucoma and cherry eye"},
        {"test": "Thyroid Panel", "test_ja": "\u7532\u72b6\u817a\u30d1\u30cd\u30eb", "purpose": "Screen for hypothyroidism"},
        {"test": "MLS DNA Test", "test_ja": "MLS\u907a\u4f1d\u5b50\u691c\u67fb", "purpose": "Test for musladin-lueke syndrome gene"},
        {"test": "Cardiac Exam", "test_ja": "\u5fc3\u81d3\u691c\u67fb", "purpose": "Screen for pulmonic stenosis"},
        {"test": "Hip Radiograph (PennHIP/OFA)", "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3", "purpose": "Screen for hip dysplasia"},
    ],
    "86_yorkshire_terrier": [
        {"test": "Cardiac Exam", "test_ja": "\u5fc3\u81d3\u691c\u67fb", "purpose": "Screen for mitral valve disease"},
        {"test": "Bile Acids Test", "test_ja": "\u80c6\u6c41\u9178\u691c\u67fb", "purpose": "Screen for portosystemic shunt"},
        {"test": "Patella Evaluation", "test_ja": "\u819d\u84cb\u9aa8\u8a55\u4fa1", "purpose": "Check for patellar luxation grade"},
        {"test": "Ophthalmologic Exam", "test_ja": "\u773c\u79d1\u691c\u67fb", "purpose": "Screen for cataracts and dry eye"},
    ],
    "39_welsh_corgi": [
        {"test": "Spine X-ray/CT", "test_ja": "\u810a\u690e\u30ec\u30f3\u30c8\u30b2\u30f3/CT", "purpose": "Screen for IVDD"},
        {"test": "DM DNA Test", "test_ja": "DM\u907a\u4f1d\u5b50\u691c\u67fb", "purpose": "Test for degenerative myelopathy gene"},
        {"test": "Hip Radiograph (PennHIP/OFA)", "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3", "purpose": "Screen for hip dysplasia"},
        {"test": "Ophthalmologic Exam", "test_ja": "\u773c\u79d1\u691c\u67fb", "purpose": "Screen for PRA and cataracts"},
        {"test": "vWD DNA Test", "test_ja": "vWD\u907a\u4f1d\u5b50\u691c\u67fb", "purpose": "Test for von Willebrand disease gene"},
    ],
    "102_english_bulldog": [
        {"test": "Brachycephalic Assessment", "test_ja": "\u77ed\u982d\u7a2e\u8a55\u4fa1", "purpose": "Evaluate airway obstruction severity"},
        {"test": "Hip Radiograph (PennHIP/OFA)", "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3", "purpose": "Screen for hip dysplasia"},
        {"test": "Cardiac Exam", "test_ja": "\u5fc3\u81d3\u691c\u67fb", "purpose": "Screen for pulmonic stenosis"},
        {"test": "Patella Evaluation", "test_ja": "\u819d\u84cb\u9aa8\u8a55\u4fa1", "purpose": "Check for patellar luxation"},
        {"test": "Spine X-ray/CT", "test_ja": "\u810a\u690e\u30ec\u30f3\u30c8\u30b2\u30f3/CT", "purpose": "Screen for hemivertebrae"},
    ],
    "103_pug": [
        {"test": "Brachycephalic Assessment", "test_ja": "\u77ed\u982d\u7a2e\u8a55\u4fa1", "purpose": "Evaluate airway obstruction severity"},
        {"test": "Ophthalmologic Exam", "test_ja": "\u773c\u79d1\u691c\u67fb", "purpose": "Screen for corneal ulcers and PDE"},
        {"test": "PDE DNA Test", "test_ja": "PDE\u907a\u4f1d\u5b50\u691c\u67fb", "purpose": "Test for pug dog encephalitis gene"},
        {"test": "Hip Radiograph (PennHIP/OFA)", "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3", "purpose": "Screen for hip dysplasia"},
        {"test": "Patella Evaluation", "test_ja": "\u819d\u84cb\u9aa8\u8a55\u4fa1", "purpose": "Check for patellar luxation"},
    ],
    "104_boston_terrier": [
        {"test": "Brachycephalic Assessment", "test_ja": "\u77ed\u982d\u7a2e\u8a55\u4fa1", "purpose": "Evaluate airway obstruction severity"},
        {"test": "Ophthalmologic Exam", "test_ja": "\u773c\u79d1\u691c\u67fb", "purpose": "Screen for cataracts and cherry eye"},
        {"test": "Patella Evaluation", "test_ja": "\u819d\u84cb\u9aa8\u8a55\u4fa1", "purpose": "Check for patellar luxation"},
    ],
    "105_boxer": [
        {"test": "Cardiac Exam", "test_ja": "\u5fc3\u81d3\u691c\u67fb", "purpose": "Screen for aortic stenosis and ARVC"},
        {"test": "Holter Monitor", "test_ja": "\u30db\u30eb\u30bf\u30fc\u5fc3\u96fb\u56f3", "purpose": "24-hour ECG monitoring for arrhythmias"},
        {"test": "Cancer Screening (Oncology Panel)", "test_ja": "\u816b\u760d\u30b9\u30af\u30ea\u30fc\u30cb\u30f3\u30b0", "purpose": "Early detection of mast cell tumors and lymphoma"},
        {"test": "Thyroid Panel", "test_ja": "\u7532\u72b6\u817a\u30d1\u30cd\u30eb", "purpose": "Screen for hypothyroidism"},
        {"test": "DM DNA Test", "test_ja": "DM\u907a\u4f1d\u5b50\u691c\u67fb", "purpose": "Test for degenerative myelopathy gene"},
    ],
    "106_rottweiler": [
        {"test": "Hip Radiograph (PennHIP/OFA)", "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3", "purpose": "Screen for hip dysplasia"},
        {"test": "Elbow Radiograph", "test_ja": "\u8098\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3", "purpose": "Screen for elbow dysplasia"},
        {"test": "Cardiac Exam", "test_ja": "\u5fc3\u81d3\u691c\u67fb", "purpose": "Screen for aortic stenosis"},
        {"test": "Ophthalmologic Exam", "test_ja": "\u773c\u79d1\u691c\u67fb", "purpose": "Screen for PRA and cataracts"},
        {"test": "Cancer Screening (Oncology Panel)", "test_ja": "\u816b\u760d\u30b9\u30af\u30ea\u30fc\u30cb\u30f3\u30b0", "purpose": "Early detection of osteosarcoma"},
    ],
    "107_doberman_pinscher": [
        {"test": "Cardiac Exam", "test_ja": "\u5fc3\u81d3\u691c\u67fb", "purpose": "Screen for dilated cardiomyopathy"},
        {"test": "Holter Monitor", "test_ja": "\u30db\u30eb\u30bf\u30fc\u5fc3\u96fb\u56f3", "purpose": "24-hour ECG monitoring for arrhythmias"},
        {"test": "vWD DNA Test", "test_ja": "vWD\u907a\u4f1d\u5b50\u691c\u67fb", "purpose": "Test for von Willebrand disease gene"},
        {"test": "Thyroid Panel", "test_ja": "\u7532\u72b6\u817a\u30d1\u30cd\u30eb", "purpose": "Screen for hypothyroidism"},
        {"test": "Hip Radiograph (PennHIP/OFA)", "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3", "purpose": "Screen for hip dysplasia"},
    ],
    "108_great_dane": [
        {"test": "Cardiac Exam", "test_ja": "\u5fc3\u81d3\u691c\u67fb", "purpose": "Screen for dilated cardiomyopathy"},
        {"test": "Hip Radiograph (PennHIP/OFA)", "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3", "purpose": "Screen for hip dysplasia"},
        {"test": "Thyroid Panel", "test_ja": "\u7532\u72b6\u817a\u30d1\u30cd\u30eb", "purpose": "Screen for hypothyroidism"},
        {"test": "Ophthalmologic Exam", "test_ja": "\u773c\u79d1\u691c\u67fb", "purpose": "Screen for entropion and cataracts"},
    ],
    "109_bernese_mountain_dog": [
        {"test": "Hip Radiograph (PennHIP/OFA)", "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3", "purpose": "Screen for hip dysplasia"},
        {"test": "Elbow Radiograph", "test_ja": "\u8098\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3", "purpose": "Screen for elbow dysplasia"},
        {"test": "Cancer Screening (Oncology Panel)", "test_ja": "\u816b\u760d\u30b9\u30af\u30ea\u30fc\u30cb\u30f3\u30b0", "purpose": "Early detection of histiocytic sarcoma"},
        {"test": "Cardiac Exam", "test_ja": "\u5fc3\u81d3\u691c\u67fb", "purpose": "Screen for aortic stenosis"},
        {"test": "vWD DNA Test", "test_ja": "vWD\u907a\u4f1d\u5b50\u691c\u67fb", "purpose": "Test for von Willebrand disease gene"},
    ],
    "110_cavalier_king_charles": [
        {"test": "Cardiac Exam", "test_ja": "\u5fc3\u81d3\u691c\u67fb", "purpose": "Screen for mitral valve disease"},
        {"test": "MRI (Syringomyelia)", "test_ja": "MRI\uff08\u810a\u9ac4\u7a7a\u6d1e\u75c7\uff09", "purpose": "Screen for Chiari malformation/syringomyelia"},
        {"test": "Ophthalmologic Exam", "test_ja": "\u773c\u79d1\u691c\u67fb", "purpose": "Screen for cataracts and retinal dysplasia"},
        {"test": "Platelet Count", "test_ja": "\u8840\u5c0f\u677f\u6570", "purpose": "Screen for macrothrombocytopenia"},
        {"test": "Patella Evaluation", "test_ja": "\u819d\u84cb\u9aa8\u8a55\u4fa1", "purpose": "Check for patellar luxation"},
    ],
    "112_cocker_spaniel": [
        {"test": "Ophthalmologic Exam", "test_ja": "\u773c\u79d1\u691c\u67fb", "purpose": "Screen for glaucoma, cataracts, and PRA"},
        {"test": "Ear Exam (Otoscopy)", "test_ja": "\u8033\u93e1\u691c\u67fb", "purpose": "Evaluate ear canal health"},
        {"test": "Thyroid Panel", "test_ja": "\u7532\u72b6\u817a\u30d1\u30cd\u30eb", "purpose": "Screen for hypothyroidism"},
        {"test": "Hip Radiograph (PennHIP/OFA)", "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3", "purpose": "Screen for hip dysplasia"},
        {"test": "Allergy Panel", "test_ja": "\u30a2\u30ec\u30eb\u30ae\u30fc\u30d1\u30cd\u30eb", "purpose": "Identify environmental or food allergens"},
    ],
    "113_springer_spaniel": [
        {"test": "Ophthalmologic Exam", "test_ja": "\u773c\u79d1\u691c\u67fb", "purpose": "Screen for PRA and retinal dysplasia"},
        {"test": "Ear Exam (Otoscopy)", "test_ja": "\u8033\u93e1\u691c\u67fb", "purpose": "Evaluate ear canal health"},
        {"test": "Hip Radiograph (PennHIP/OFA)", "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3", "purpose": "Screen for hip dysplasia"},
        {"test": "PFK DNA Test", "test_ja": "PFK\u907a\u4f1d\u5b50\u691c\u67fb", "purpose": "Test for phosphofructokinase deficiency"},
    ],
    "114_dachshund": [
        {"test": "Spine X-ray/CT", "test_ja": "\u810a\u690e\u30ec\u30f3\u30c8\u30b2\u30f3/CT", "purpose": "Screen for IVDD"},
        {"test": "Ophthalmologic Exam", "test_ja": "\u773c\u79d1\u691c\u67fb", "purpose": "Screen for PRA and cataracts"},
        {"test": "Cardiac Exam", "test_ja": "\u5fc3\u81d3\u691c\u67fb", "purpose": "Screen for mitral valve disease"},
        {"test": "Patella Evaluation", "test_ja": "\u819d\u84cb\u9aa8\u8a55\u4fa1", "purpose": "Check for patellar luxation"},
    ],
    "115_miniature_schnauzer": [
        {"test": "Lipid Panel", "test_ja": "\u8102\u8cea\u30d1\u30cd\u30eb", "purpose": "Screen for hyperlipidemia"},
        {"test": "Urinalysis", "test_ja": "\u5c3f\u691c\u67fb", "purpose": "Screen for urinary stones"},
        {"test": "Ophthalmologic Exam", "test_ja": "\u773c\u79d1\u691c\u67fb", "purpose": "Screen for cataracts and PRA"},
        {"test": "Pancreatitis Test (cPL)", "test_ja": "\u81b5\u708e\u691c\u67fb\uff08cPL\uff09", "purpose": "Screen for pancreatitis risk"},
        {"test": "Blood Glucose Test", "test_ja": "\u8840\u7cd6\u691c\u67fb", "purpose": "Screen for diabetes mellitus"},
    ],
    "116_shih_tzu": [
        {"test": "Brachycephalic Assessment", "test_ja": "\u77ed\u982d\u7a2e\u8a55\u4fa1", "purpose": "Evaluate airway obstruction severity"},
        {"test": "Ophthalmologic Exam", "test_ja": "\u773c\u79d1\u691c\u67fb", "purpose": "Screen for cataracts, dry eye, and proptosis"},
        {"test": "Kidney Panel", "test_ja": "\u814e\u81d3\u30d1\u30cd\u30eb", "purpose": "Screen for renal dysplasia"},
        {"test": "Patella Evaluation", "test_ja": "\u819d\u84cb\u9aa8\u8a55\u4fa1", "purpose": "Check for patellar luxation"},
    ],
    "117_maltese": [
        {"test": "Cardiac Exam", "test_ja": "\u5fc3\u81d3\u691c\u67fb", "purpose": "Screen for mitral valve disease and PDA"},
        {"test": "Bile Acids Test", "test_ja": "\u80c6\u6c41\u9178\u691c\u67fb", "purpose": "Screen for portosystemic shunt"},
        {"test": "Patella Evaluation", "test_ja": "\u819d\u84cb\u9aa8\u8a55\u4fa1", "purpose": "Check for patellar luxation"},
    ],
    "118_havanese": [
        {"test": "Cardiac Exam", "test_ja": "\u5fc3\u81d3\u691c\u67fb", "purpose": "Screen for mitral valve disease"},
        {"test": "Ophthalmologic Exam", "test_ja": "\u773c\u79d1\u691c\u67fb", "purpose": "Screen for cataracts"},
        {"test": "Patella Evaluation", "test_ja": "\u819d\u84cb\u9aa8\u8a55\u4fa1", "purpose": "Check for patellar luxation"},
        {"test": "Hip Radiograph (PennHIP/OFA)", "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3", "purpose": "Screen for Legg-Calve-Perthes disease"},
    ],
    "119_bichon_frise": [
        {"test": "Allergy Panel", "test_ja": "\u30a2\u30ec\u30eb\u30ae\u30fc\u30d1\u30cd\u30eb", "purpose": "Identify environmental or food allergens"},
        {"test": "Urinalysis", "test_ja": "\u5c3f\u691c\u67fb", "purpose": "Screen for bladder stones"},
        {"test": "Blood Glucose Test", "test_ja": "\u8840\u7cd6\u691c\u67fb", "purpose": "Screen for diabetes mellitus"},
        {"test": "Patella Evaluation", "test_ja": "\u819d\u84cb\u9aa8\u8a55\u4fa1", "purpose": "Check for patellar luxation"},
    ],
    "120_pomeranian": [
        {"test": "Cardiac Exam", "test_ja": "\u5fc3\u81d3\u691c\u67fb", "purpose": "Screen for patent ductus arteriosus"},
        {"test": "Patella Evaluation", "test_ja": "\u819d\u84cb\u9aa8\u8a55\u4fa1", "purpose": "Check for patellar luxation"},
        {"test": "Thyroid Panel", "test_ja": "\u7532\u72b6\u817a\u30d1\u30cd\u30eb", "purpose": "Screen for hypothyroidism"},
        {"test": "Tracheal Exam", "test_ja": "\u6c17\u7ba1\u691c\u67fb", "purpose": "Screen for collapsing trachea"},
    ],
    "121_shetland_sheepdog": [
        {"test": "Ophthalmologic Exam", "test_ja": "\u773c\u79d1\u691c\u67fb", "purpose": "Screen for CEA and PRA"},
        {"test": "MDR1 DNA Test", "test_ja": "MDR1\u907a\u4f1d\u5b50\u691c\u67fb", "purpose": "Test for multidrug resistance gene"},
        {"test": "Thyroid Panel", "test_ja": "\u7532\u72b6\u817a\u30d1\u30cd\u30eb", "purpose": "Screen for hypothyroidism"},
        {"test": "Hip Radiograph (PennHIP/OFA)", "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3", "purpose": "Screen for hip dysplasia"},
        {"test": "vWD DNA Test", "test_ja": "vWD\u907a\u4f1d\u5b50\u691c\u67fb", "purpose": "Test for von Willebrand disease gene"},
    ],
    "123_border_collie": [
        {"test": "Hip Radiograph (PennHIP/OFA)", "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3", "purpose": "Screen for hip dysplasia"},
        {"test": "Ophthalmologic Exam", "test_ja": "\u773c\u79d1\u691c\u67fb", "purpose": "Screen for CEA and PRA"},
        {"test": "CEA DNA Test", "test_ja": "CEA\u907a\u4f1d\u5b50\u691c\u67fb", "purpose": "Test for collie eye anomaly gene"},
        {"test": "TNS DNA Test", "test_ja": "TNS\u907a\u4f1d\u5b50\u691c\u67fb", "purpose": "Test for trapped neutrophil syndrome"},
        {"test": "MDR1 DNA Test", "test_ja": "MDR1\u907a\u4f1d\u5b50\u691c\u67fb", "purpose": "Test for multidrug resistance gene"},
    ],
    "124_australian_shepherd": [
        {"test": "Hip Radiograph (PennHIP/OFA)", "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3", "purpose": "Screen for hip dysplasia"},
        {"test": "Ophthalmologic Exam", "test_ja": "\u773c\u79d1\u691c\u67fb", "purpose": "Screen for cataracts and CEA"},
        {"test": "MDR1 DNA Test", "test_ja": "MDR1\u907a\u4f1d\u5b50\u691c\u67fb", "purpose": "Test for multidrug resistance gene"},
        {"test": "Elbow Radiograph", "test_ja": "\u8098\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3", "purpose": "Screen for elbow dysplasia"},
    ],
    "125_siberian_husky": [
        {"test": "Ophthalmologic Exam", "test_ja": "\u773c\u79d1\u691c\u67fb", "purpose": "Screen for cataracts and PRA"},
        {"test": "Hip Radiograph (PennHIP/OFA)", "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3", "purpose": "Screen for hip dysplasia"},
        {"test": "Thyroid Panel", "test_ja": "\u7532\u72b6\u817a\u30d1\u30cd\u30eb", "purpose": "Screen for hypothyroidism"},
    ],
    "126_alaskan_malamute": [
        {"test": "Hip Radiograph (PennHIP/OFA)", "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3", "purpose": "Screen for hip dysplasia"},
        {"test": "Ophthalmologic Exam", "test_ja": "\u773c\u79d1\u691c\u67fb", "purpose": "Screen for cataracts and day blindness"},
        {"test": "Thyroid Panel", "test_ja": "\u7532\u72b6\u817a\u30d1\u30cd\u30eb", "purpose": "Screen for hypothyroidism"},
        {"test": "Polyneuropathy DNA Test", "test_ja": "\u591a\u767a\u6027\u795e\u7d4c\u969c\u5bb3\u907a\u4f1d\u5b50\u691c\u67fb", "purpose": "Test for hereditary polyneuropathy gene"},
    ],
    "127_akita": [
        {"test": "Hip Radiograph (PennHIP/OFA)", "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3", "purpose": "Screen for hip dysplasia"},
        {"test": "Ophthalmologic Exam", "test_ja": "\u773c\u79d1\u691c\u67fb", "purpose": "Screen for PRA and glaucoma"},
        {"test": "Thyroid Panel", "test_ja": "\u7532\u72b6\u817a\u30d1\u30cd\u30eb", "purpose": "Screen for hypothyroidism"},
        {"test": "Autoimmune Panel", "test_ja": "\u81ea\u5df1\u514d\u75ab\u30d1\u30cd\u30eb", "purpose": "Screen for autoimmune conditions (VKH, IMHA)"},
    ],
    "128_samoyed": [
        {"test": "Hip Radiograph (PennHIP/OFA)", "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3", "purpose": "Screen for hip dysplasia"},
        {"test": "Ophthalmologic Exam", "test_ja": "\u773c\u79d1\u691c\u67fb", "purpose": "Screen for PRA and glaucoma"},
        {"test": "Blood Glucose Test", "test_ja": "\u8840\u7cd6\u691c\u67fb", "purpose": "Screen for diabetes mellitus"},
        {"test": "Cardiac Exam", "test_ja": "\u5fc3\u81d3\u691c\u67fb", "purpose": "Screen for pulmonic stenosis"},
    ],
    "129_newfoundland": [
        {"test": "Cardiac Exam", "test_ja": "\u5fc3\u81d3\u691c\u67fb", "purpose": "Screen for subvalvular aortic stenosis"},
        {"test": "Hip Radiograph (PennHIP/OFA)", "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3", "purpose": "Screen for hip dysplasia"},
        {"test": "Elbow Radiograph", "test_ja": "\u8098\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3", "purpose": "Screen for elbow dysplasia"},
        {"test": "Cystinuria DNA Test", "test_ja": "\u30b7\u30b9\u30c1\u30f3\u5c3f\u75c7\u907a\u4f1d\u5b50\u691c\u67fb", "purpose": "Test for cystinuria gene"},
    ],
    "130_saint_bernard": [
        {"test": "Hip Radiograph (PennHIP/OFA)", "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3", "purpose": "Screen for hip dysplasia"},
        {"test": "Elbow Radiograph", "test_ja": "\u8098\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3", "purpose": "Screen for elbow dysplasia"},
        {"test": "Cardiac Exam", "test_ja": "\u5fc3\u81d3\u691c\u67fb", "purpose": "Screen for dilated cardiomyopathy"},
        {"test": "Ophthalmologic Exam", "test_ja": "\u773c\u79d1\u691c\u67fb", "purpose": "Screen for entropion and ectropion"},
    ],
    "131_irish_setter": [
        {"test": "Hip Radiograph (PennHIP/OFA)", "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3", "purpose": "Screen for hip dysplasia"},
        {"test": "Ophthalmologic Exam", "test_ja": "\u773c\u79d1\u691c\u67fb", "purpose": "Screen for PRA"},
        {"test": "Thyroid Panel", "test_ja": "\u7532\u72b6\u817a\u30d1\u30cd\u30eb", "purpose": "Screen for hypothyroidism"},
        {"test": "CLAD DNA Test", "test_ja": "CLAD\u907a\u4f1d\u5b50\u691c\u67fb", "purpose": "Test for canine leukocyte adhesion deficiency gene"},
    ],
    "132_weimaraner": [
        {"test": "Hip Radiograph (PennHIP/OFA)", "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3", "purpose": "Screen for hip dysplasia"},
        {"test": "Ophthalmologic Exam", "test_ja": "\u773c\u79d1\u691c\u67fb", "purpose": "Screen for entropion and distichiasis"},
        {"test": "Thyroid Panel", "test_ja": "\u7532\u72b6\u817a\u30d1\u30cd\u30eb", "purpose": "Screen for hypothyroidism"},
        {"test": "HUU DNA Test", "test_ja": "HUU\u907a\u4f1d\u5b50\u691c\u67fb", "purpose": "Test for hyperuricosuria gene"},
    ],
    "133_vizsla": [
        {"test": "Hip Radiograph (PennHIP/OFA)", "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3", "purpose": "Screen for hip dysplasia"},
        {"test": "Ophthalmologic Exam", "test_ja": "\u773c\u79d1\u691c\u67fb", "purpose": "Screen for cataracts and PRA"},
        {"test": "Thyroid Panel", "test_ja": "\u7532\u72b6\u817a\u30d1\u30cd\u30eb", "purpose": "Screen for hypothyroidism"},
    ],
    "134_german_shorthaired_pointer": [
        {"test": "Hip Radiograph (PennHIP/OFA)", "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3", "purpose": "Screen for hip dysplasia"},
        {"test": "Ophthalmologic Exam", "test_ja": "\u773c\u79d1\u691c\u67fb", "purpose": "Screen for cone degeneration"},
        {"test": "Cardiac Exam", "test_ja": "\u5fc3\u81d3\u691c\u67fb", "purpose": "Screen for aortic stenosis"},
        {"test": "vWD DNA Test", "test_ja": "vWD\u907a\u4f1d\u5b50\u691c\u67fb", "purpose": "Test for von Willebrand disease gene"},
    ],
    "135_brittany": [
        {"test": "Hip Radiograph (PennHIP/OFA)", "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3", "purpose": "Screen for hip dysplasia"},
        {"test": "Thyroid Panel", "test_ja": "\u7532\u72b6\u817a\u30d1\u30cd\u30eb", "purpose": "Screen for hypothyroidism"},
        {"test": "Ophthalmologic Exam", "test_ja": "\u773c\u79d1\u691c\u67fb", "purpose": "Screen for cataracts and lens luxation"},
    ],
    "136_standard_poodle": [
        {"test": "Hip Radiograph (PennHIP/OFA)", "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3", "purpose": "Screen for hip dysplasia"},
        {"test": "Ophthalmologic Exam", "test_ja": "\u773c\u79d1\u691c\u67fb", "purpose": "Screen for PRA and cataracts"},
        {"test": "vWD DNA Test", "test_ja": "vWD\u907a\u4f1d\u5b50\u691c\u67fb", "purpose": "Test for von Willebrand disease gene"},
        {"test": "Addison's Baseline Cortisol", "test_ja": "\u30a2\u30b8\u30bd\u30f3\u75c5\u30b3\u30eb\u30c1\u30be\u30fc\u30eb\u57fa\u6e96\u691c\u67fb", "purpose": "Screen for Addison's disease"},
        {"test": "Neonatal Encephalopathy DNA Test", "test_ja": "NEwS\u907a\u4f1d\u5b50\u691c\u67fb", "purpose": "Test for neonatal encephalopathy gene"},
    ],
    "137_miniature_poodle": [
        {"test": "Ophthalmologic Exam", "test_ja": "\u773c\u79d1\u691c\u67fb", "purpose": "Screen for PRA and cataracts"},
        {"test": "Patella Evaluation", "test_ja": "\u819d\u84cb\u9aa8\u8a55\u4fa1", "purpose": "Check for patellar luxation"},
        {"test": "PRA DNA Test", "test_ja": "PRA\u907a\u4f1d\u5b50\u691c\u67fb", "purpose": "Test for progressive retinal atrophy gene"},
    ],
    "138_west_highland_white_terrier": [
        {"test": "Allergy Panel", "test_ja": "\u30a2\u30ec\u30eb\u30ae\u30fc\u30d1\u30cd\u30eb", "purpose": "Identify environmental or food allergens"},
        {"test": "Bile Acids Test", "test_ja": "\u80c6\u6c41\u9178\u691c\u67fb", "purpose": "Screen for copper hepatopathy"},
        {"test": "Patella Evaluation", "test_ja": "\u819d\u84cb\u9aa8\u8a55\u4fa1", "purpose": "Check for patellar luxation"},
        {"test": "CMO Screening", "test_ja": "CMO\u30b9\u30af\u30ea\u30fc\u30cb\u30f3\u30b0", "purpose": "Screen for craniomandibular osteopathy"},
    ],
    "139_scottish_terrier": [
        {"test": "Urinalysis", "test_ja": "\u5c3f\u691c\u67fb", "purpose": "Screen for bladder cancer and stones"},
        {"test": "vWD DNA Test", "test_ja": "vWD\u907a\u4f1d\u5b50\u691c\u67fb", "purpose": "Test for von Willebrand disease gene"},
        {"test": "Patella Evaluation", "test_ja": "\u819d\u84cb\u9aa8\u8a55\u4fa1", "purpose": "Check for patellar luxation"},
        {"test": "CMO Screening", "test_ja": "CMO\u30b9\u30af\u30ea\u30fc\u30cb\u30f3\u30b0", "purpose": "Screen for craniomandibular osteopathy"},
    ],
    "140_cairn_terrier": [
        {"test": "Allergy Panel", "test_ja": "\u30a2\u30ec\u30eb\u30ae\u30fc\u30d1\u30cd\u30eb", "purpose": "Identify environmental or food allergens"},
        {"test": "Bile Acids Test", "test_ja": "\u80c6\u6c41\u9178\u691c\u67fb", "purpose": "Screen for portosystemic shunt"},
        {"test": "Ophthalmologic Exam", "test_ja": "\u773c\u79d1\u691c\u67fb", "purpose": "Screen for cataracts and PRA"},
    ],
    "141_jack_russell_terrier": [
        {"test": "Ophthalmologic Exam", "test_ja": "\u773c\u79d1\u691c\u67fb", "purpose": "Screen for lens luxation and PRA"},
        {"test": "Patella Evaluation", "test_ja": "\u819d\u84cb\u9aa8\u8a55\u4fa1", "purpose": "Check for patellar luxation"},
        {"test": "Allergy Panel", "test_ja": "\u30a2\u30ec\u30eb\u30ae\u30fc\u30d1\u30cd\u30eb", "purpose": "Identify environmental or food allergens"},
        {"test": "Cardiac Exam", "test_ja": "\u5fc3\u81d3\u691c\u67fb", "purpose": "Baseline cardiac evaluation"},
    ],
    "142_staffordshire_bull_terrier": [
        {"test": "L2-HGA DNA Test", "test_ja": "L2-HGA\u907a\u4f1d\u5b50\u691c\u67fb", "purpose": "Test for L-2-hydroxyglutaric aciduria gene"},
        {"test": "HC DNA Test", "test_ja": "HC\u907a\u4f1d\u5b50\u691c\u67fb", "purpose": "Test for hereditary cataracts gene"},
        {"test": "Patella Evaluation", "test_ja": "\u819d\u84cb\u9aa8\u8a55\u4fa1", "purpose": "Check for patellar luxation"},
        {"test": "Allergy Panel", "test_ja": "\u30a2\u30ec\u30eb\u30ae\u30fc\u30d1\u30cd\u30eb", "purpose": "Identify environmental or food allergens"},
    ],
    "143_bull_terrier": [
        {"test": "Urinalysis", "test_ja": "\u5c3f\u691c\u67fb", "purpose": "Screen for hereditary nephritis"},
        {"test": "UPC Ratio", "test_ja": "\u5c3f\u86cb\u767d\u30af\u30ec\u30a2\u30c1\u30cb\u30f3\u6bd4", "purpose": "Monitor kidney protein loss"},
        {"test": "Cardiac Exam", "test_ja": "\u5fc3\u81d3\u691c\u67fb", "purpose": "Screen for mitral valve disease"},
        {"test": "Allergy Panel", "test_ja": "\u30a2\u30ec\u30eb\u30ae\u30fc\u30d1\u30cd\u30eb", "purpose": "Identify environmental or food allergens"},
    ],
    "144_airedale_terrier": [
        {"test": "Hip Radiograph (PennHIP/OFA)", "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3", "purpose": "Screen for hip dysplasia"},
        {"test": "Cardiac Exam", "test_ja": "\u5fc3\u81d3\u691c\u67fb", "purpose": "Baseline cardiac evaluation"},
        {"test": "Thyroid Panel", "test_ja": "\u7532\u72b6\u817a\u30d1\u30cd\u30eb", "purpose": "Screen for hypothyroidism"},
    ],
    "145_whippet": [
        {"test": "Cardiac Exam", "test_ja": "\u5fc3\u81d3\u691c\u67fb", "purpose": "Screen for mitral valve disease"},
        {"test": "Ophthalmologic Exam", "test_ja": "\u773c\u79d1\u691c\u67fb", "purpose": "Screen for cataracts and PRA"},
        {"test": "BFJE DNA Test", "test_ja": "BFJE\u907a\u4f1d\u5b50\u691c\u67fb", "purpose": "Test for Bally forelimb joint disease gene"},
    ],
    "146_italian_greyhound": [
        {"test": "Patella Evaluation", "test_ja": "\u819d\u84cb\u9aa8\u8a55\u4fa1", "purpose": "Check for patellar luxation"},
        {"test": "Ophthalmologic Exam", "test_ja": "\u773c\u79d1\u691c\u67fb", "purpose": "Screen for PRA and cataracts"},
        {"test": "Thyroid Panel", "test_ja": "\u7532\u72b6\u817a\u30d1\u30cd\u30eb", "purpose": "Screen for hypothyroidism"},
    ],
    "147_greyhound": [
        {"test": "Cardiac Exam", "test_ja": "\u5fc3\u81d3\u691c\u67fb", "purpose": "Baseline cardiac evaluation"},
        {"test": "CBC (Complete Blood Count)", "test_ja": "\u5168\u8840\u7403\u8a08\u7b97", "purpose": "Greyhound-specific reference ranges"},
        {"test": "Thyroid Panel", "test_ja": "\u7532\u72b6\u817a\u30d1\u30cd\u30eb", "purpose": "Screen for hypothyroidism (breed-specific ranges)"},
        {"test": "Ophthalmologic Exam", "test_ja": "\u773c\u79d1\u691c\u67fb", "purpose": "Screen for pannus and cataracts"},
    ],
    "148_basset_hound": [
        {"test": "Ear Exam (Otoscopy)", "test_ja": "\u8033\u93e1\u691c\u67fb", "purpose": "Evaluate ear canal health"},
        {"test": "Spine X-ray/CT", "test_ja": "\u810a\u690e\u30ec\u30f3\u30c8\u30b2\u30f3/CT", "purpose": "Screen for IVDD"},
        {"test": "Ophthalmologic Exam", "test_ja": "\u773c\u79d1\u691c\u67fb", "purpose": "Screen for glaucoma and ectropion"},
        {"test": "Thrombopathia DNA Test", "test_ja": "\u8840\u5c0f\u677f\u6a5f\u80fd\u7570\u5e38\u907a\u4f1d\u5b50\u691c\u67fb", "purpose": "Test for platelet function disorder gene"},
    ],
    "149_bloodhound": [
        {"test": "Hip Radiograph (PennHIP/OFA)", "test_ja": "\u80a1\u95a2\u7bc0\u30ec\u30f3\u30c8\u30b2\u30f3", "purpose": "Screen for hip dysplasia"},
        {"test": "Ear Exam (Otoscopy)", "test_ja": "\u8033\u93e1\u691c\u67fb", "purpose": "Evaluate ear canal health"},
        {"test": "Ophthalmologic Exam", "test_ja": "\u773c\u79d1\u691c\u67fb", "purpose": "Screen for entropion and ectropion"},
        {"test": "Cardiac Exam", "test_ja": "\u5fc3\u81d3\u691c\u67fb", "purpose": "Baseline cardiac evaluation"},
    ],
    "150_dalmatian": [
        {"test": "HUU DNA Test", "test_ja": "HUU\u907a\u4f1d\u5b50\u691c\u67fb", "purpose": "Test for hyperuricosuria gene"},
        {"test": "Urinalysis", "test_ja": "\u5c3f\u691c\u67fb", "purpose": "Monitor urate crystal formation"},
        {"test": "BAER Test", "test_ja": "BAER\u8074\u899a\u691c\u67fb", "purpose": "Screen for congenital deafness"},
        {"test": "Ophthalmologic Exam", "test_ja": "\u773c\u79d1\u691c\u67fb", "purpose": "Screen for cataracts and iris sphincter dysplasia"},
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


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def analyze_symptoms(
    symptoms: list[str],
    *,
    breed: str | None = None,
    onset: str | None = None,
    age_years: float | None = None,
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

    Returns
    -------
    dict
        Analysis result containing ``suspected_diseases``,
        ``recommended_tests``, ``severity``, ``general_advice``,
        ``general_advice_ja``, ``breed_genetic_tests``,
        ``breed_risk_applied``, ``onset_applied``, and ``age_applied``.
    """
    symptom_set: set[str] = set(symptoms) & VALID_SYMPTOMS

    # Resolve age stage for predisposition lookup
    age_stage: str | None = None
    if age_years is not None:
        age_stage = _age_years_to_stage(age_years)

    # -- 1. Score diseases --------------------------------------------------
    suspected: list[dict[str, Any]] = []
    for disease in _DISEASE_DB:
        disease_symptoms: set[str] = disease["symptoms"]
        matching: set[str] = symptom_set & disease_symptoms
        match_count: int = len(matching)
        total: int = len(disease_symptoms)

        if total == 0 or match_count == 0:
            continue

        # Coverage: how many of the disease's symptoms did the user check?
        coverage: float = match_count / total
        # Jaccard: intersection / union (penalises unrelated extra symptoms)
        union_size = len(symptom_set | disease_symptoms)
        jaccard: float = match_count / union_size if union_size > 0 else 0.0
        # Composite score (same formula used in the frontend)
        raw_score: float = (jaccard * 0.4 + coverage * 0.6) * 100

        # Apply breed-specific risk multiplier
        breed_multiplier = 1.0
        if breed and breed in _BREED_DISEASE_RISK:
            breed_multiplier = _BREED_DISEASE_RISK[breed].get(disease["name"], 1.0)
        adjusted_score = min(raw_score * breed_multiplier, 100.0)

        # Apply onset (time-course) multiplier
        onset_multiplier = 1.0
        if onset:
            disease_onsets = _DISEASE_ONSET.get(disease["name"])
            if disease_onsets:
                if onset in disease_onsets:
                    # Matching onset pattern -> boost
                    onset_multiplier = 1.3
                else:
                    # Mismatch -> penalize
                    onset_multiplier = 0.7
            # If disease has no onset data, leave multiplier at 1.0
        adjusted_score = min(adjusted_score * onset_multiplier, 100.0)

        # Apply age predisposition multiplier
        age_multiplier = 1.0
        if age_stage:
            age_predisposition = _DISEASE_AGE_PREDISPOSITION.get(disease["name"])
            if age_predisposition:
                if age_stage in age_predisposition:
                    # Age group matches -> boost
                    age_multiplier = 1.25
                else:
                    # Age mismatch -> penalize
                    age_multiplier = 0.75
            # If disease has no age predisposition data, leave at 1.0
        adjusted_score = min(adjusted_score * age_multiplier, 100.0)

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
            color_class = "score-high"       # red
        elif match_percent >= 45:
            color_class = "score-moderate"    # orange
        elif match_percent >= 25:
            color_class = "score-low"         # yellow
        else:
            color_class = "score-minimal"     # green / grey

        suspected.append({
            "name": disease["name"],
            "name_ja": disease["name_ja"],
            "likelihood": likelihood,
            "match_percent": match_percent,
            "color_class": color_class,
            "description": disease["description"],
            "description_ja": disease.get("description_ja", ""),
            "matching_symptoms": sorted(matching),
            "match_count": match_count,
            "total_symptoms": total,
            # internal fields for later processing
            "_urgency": disease["urgency"],
            "_match_ratio": coverage,
        })

    # Sort: match_percent desc (primary), then match_count desc (tiebreak)
    suspected.sort(key=lambda d: (d["match_percent"], d["match_count"]),
                   reverse=True)

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
    symptom_names_lookup = {
        sid: _SYMPTOM_NAMES[sid]
        for sid in used_symptoms
        if sid in _SYMPTOM_NAMES
    }

    return {
        "suspected_diseases": suspected,
        "recommended_tests": recommended_tests,
        "severity": severity,
        "general_advice": advice_pair["en"],
        "general_advice_ja": advice_pair["ja"],
        "breed_genetic_tests": genetic_tests,
        "breed_risk_applied": breed is not None and breed in _BREED_DISEASE_RISK,
        "onset_applied": onset is not None,
        "onset": onset,
        "age_applied": age_years is not None,
        "age_years": age_years,
        "age_stage": age_stage,
        "symptom_names": symptom_names_lookup,
    }


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _compute_severity(suspected: list[dict[str, Any]]) -> str:
    """Derive the overall severity level from the list of suspected diseases.

    Rules (evaluated in order, first match wins):
    - Any EMERGENCY disease at "high" likelihood -> "emergency"
    - Any URGENT disease at "high" or "moderate" likelihood -> "high"
    - Any disease at "high" likelihood -> "moderate"
    - Otherwise -> "low"
    """
    has_high = False
    for d in suspected:
        urgency = d["_urgency"]
        likelihood = d["likelihood"]

        if urgency == "emergency" and likelihood == "high":
            return "emergency"
        if urgency == "urgent" and likelihood in ("high", "moderate"):
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
    disease_likelihood: dict[str, str] = {
        d["name"]: d["likelihood"] for d in suspected
    }

    for test in _TEST_DB:
        # Which suspected diseases does this test relate to?
        overlap: set[str] = test["related_diseases"] & suspected_names
        if not overlap:
            continue

        # Determine priority from the highest-likelihood related disease
        best_priority = "optional"
        for disease_name in overlap:
            candidate_priority = _LIKELIHOOD_TO_PRIORITY[
                disease_likelihood[disease_name]
            ]
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
        results.append({
            "name": name,
            "name_ja": test["name_ja"],
            "purpose": test["purpose"],
            "priority": test_priority[name],
            "related_diseases": sorted(test_related[name]),
        })

    results.sort(
        key=lambda t: (-_PRIORITY_RANK[t["priority"]], t["name"])
    )
    return results
