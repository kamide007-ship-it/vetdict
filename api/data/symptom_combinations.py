"""Extended symptom combination patterns for improved diagnostic accuracy.

Provides both pairwise (2 symptoms) and triple (3 symptoms) interaction patterns
that significantly boost disease match confidence when co-occurring symptoms are detected.

These patterns are based on clinical symptom associations and disease pathophysiology.
"""

from typing import Dict

# ============================================================================
# PAIRWISE SYMPTOM INTERACTIONS (Expanded from 20 to 100+ patterns)
# ============================================================================
# Format: {frozenset({symptom1, symptom2}): {disease_name: multiplier}}
# Multipliers represent the additional boost for diseases when both symptoms present.

EXTENDED_SYMPTOM_PAIR_BOOST: Dict[frozenset, Dict[str, float]] = {
    # ========== GASTROINTESTINAL PATTERNS ==========
    # 消化器系：嘔吐関連
    frozenset({"vomiting", "bloating"}): {
        "Gastric Dilatation-Volvulus (GDV/Bloat)": 2.0,
        "Intestinal Obstruction": 1.5,
        "Gastrointestinal Stasis": 1.5,
        "GI Stasis": 1.5,
    },
    frozenset({"vomiting", "bloated_abdomen"}): {
        "Gastric Dilatation-Volvulus (GDV/Bloat)": 2.0,
        "Intestinal Obstruction": 1.5,
        "Gastrointestinal Stasis": 1.5,
        "GI Stasis": 1.5,
    },
    # 消化器系：嘔吐+血便
    frozenset({"vomiting", "blood_in_stool"}): {
        "Parvovirus Infection": 2.0,
        "Canine Parvovirus": 2.0,
        "Hemorrhagic Gastroenteritis (HGE)": 2.0,
        "Feline Panleukopenia": 2.0,
        "Feline Panleukopenia (Feline Distemper)": 2.0,
        "Intestinal Parasites": 1.5,
        "Inflammatory Bowel Disease (IBD)": 1.5,
    },
    frozenset({"vomiting", "bloody_stool"}): {
        "Canine Parvovirus": 2.0,
        "Hemorrhagic Gastroenteritis (HGE)": 2.0,
        "Intestinal Parasites": 1.5,
        "Inflammatory Bowel Disease (IBD)": 1.5,
    },
    # 消化器系：下痢+嘔吐
    frozenset({"diarrhea", "vomiting"}): {
        "Acute Gastroenteritis": 1.8,
        "Gastroenteritis": 1.8,
        "Pancreatitis": 1.8,
        "Poisoning/Toxicity": 1.5,
        "Foreign Body Ingestion": 1.5,
        "Foreign Body Obstruction": 1.5,
        "Feline Panleukopenia": 1.5,
        "Parvovirus Infection": 1.5,
        "Canine Parvovirus": 1.5,
    },
    # 消化器系：嘔吐+腹痛
    frozenset({"vomiting", "abdominal_pain"}): {
        "Gastroenteritis": 1.8,
        "Pancreatitis": 1.9,
        "Intestinal Obstruction": 2.0,
        "Foreign Body Obstruction": 1.8,
        "Peritonitis": 2.0,
    },
    frozenset({"vomiting", "abdominal_tenderness"}): {
        "Peritonitis": 2.0,
        "Pancreatitis": 1.9,
        "Intestinal Obstruction": 1.8,
    },
    # 消化器系：黄疸+食欲不振
    frozenset({"jaundice", "loss_of_appetite"}): {
        "Liver Disease": 2.0,
        "Feline Hepatic Lipidosis": 2.5,
        "Leptospirosis": 1.8,
        "Immune-Mediated Hemolytic Anemia": 1.8,
        "Cholangitis": 1.8,
    },
    frozenset({"jaundice", "appetite_loss"}): {
        "Liver Disease": 2.0,
        "Leptospirosis": 1.8,
        "Immune-Mediated Hemolytic Anemia": 1.8,
    },
    # 消化器系：便秘+嘔吐
    frozenset({"constipation", "vomiting"}): {
        "Megacolon": 1.8,
        "Intestinal Obstruction": 1.6,
        "Foreign Body Obstruction": 1.5,
    },

    # ========== URINARY/RENAL PATTERNS ==========
    # 多飲+頻尿
    frozenset({"excessive_thirst", "frequent_urination"}): {
        "Kidney Disease (CKD)": 2.0,
        "Feline Chronic Kidney Disease (CKD)": 2.0,
        "Diabetes Mellitus": 2.0,
        "Cushing's Disease": 1.5,
        "Hyperthyroidism": 1.5,
        "Pyometra": 1.5,
    },
    frozenset({"excessive_thirst", "excessive_urination"}): {
        "Kidney Disease (CKD)": 2.0,
        "Diabetes Mellitus": 2.0,
        "Cushing's Disease": 1.5,
        "Hyperthyroidism": 1.5,
        "Pyometra": 1.5,
    },
    # 血尿+排尿困難
    frozenset({"blood_in_urine", "straining_to_urinate"}): {
        "Bladder Stones": 2.0,
        "Feline Lower Urinary Tract Disease (FLUTD)": 2.5,
        "Urinary Tract Infection": 1.8,
        "Urethral Obstruction": 2.0,
    },
    frozenset({"bloody_urine", "straining_to_urinate"}): {
        "Bladder Stones": 2.0,
        "Feline Lower Urinary Tract Disease (FLUTD)": 2.5,
        "Urinary Tract Infection": 1.8,
        "Urethral Obstruction": 2.0,
    },
    # 血尿+頻尿
    frozenset({"blood_in_urine", "frequent_urination"}): {
        "Urinary Tract Infection": 1.8,
        "Bladder Stones": 1.6,
        "Hematuria": 1.5,
    },
    # 排尿困難+腹痛
    frozenset({"straining_to_urinate", "abdominal_pain"}): {
        "Urethral Obstruction": 2.0,
        "Bladder Stones": 1.8,
        "Urinary Tract Infection": 1.5,
    },

    # ========== RESPIRATORY PATTERNS ==========
    # 咳+呼吸困難
    frozenset({"coughing", "labored_breathing"}): {
        "Heart Disease/CHF": 1.8,
        "Congestive Heart Failure": 1.8,
        "Feline Hypertrophic Cardiomyopathy (HCM)": 1.8,
        "Pneumonia": 1.8,
        "Feline Pneumonia": 1.8,
        "Pleural Effusion": 1.5,
        "Feline Asthma": 1.5,
    },
    frozenset({"coughing", "difficulty_breathing"}): {
        "Heart Disease/CHF": 1.8,
        "Congestive Heart Failure": 1.8,
        "Pneumonia": 1.8,
        "Pleural Effusion": 1.5,
    },
    # 咳+運動不耐性
    frozenset({"coughing", "exercise_intolerance"}): {
        "Heart Disease/CHF": 2.0,
        "Congestive Heart Failure": 2.0,
        "Tracheal Collapse": 2.0,
        "Heartworm Disease": 1.8,
    },
    # 咳+喘鳴
    frozenset({"coughing", "wheezing"}): {
        "Feline Asthma": 2.0,
        "Bronchitis": 1.8,
        "Heartworm Disease": 1.5,
    },
    # 呼吸困難+蒼白粘膜
    frozenset({"difficulty_breathing", "pale_gums"}): {
        "Pneumothorax": 1.8,
        "Hemothorax": 1.8,
        "Shock": 2.0,
    },

    # ========== CARDIOVASCULAR PATTERNS ==========
    # 失神+運動不耐性
    frozenset({"fainting", "exercise_intolerance"}): {
        "Heart Disease/CHF": 2.5,
        "Congestive Heart Failure": 2.5,
        "Feline Hypertrophic Cardiomyopathy (HCM)": 2.0,
        "Aortic Stenosis": 2.0,
        "Pulmonic Stenosis": 1.8,
        "Cardiac Arrhythmia": 2.0,
        "Arrhythmia": 2.0,
    },
    # 虚脱+呼吸困難
    frozenset({"collapse", "difficulty_breathing"}): {
        "Heart Disease/CHF": 2.0,
        "Congestive Heart Failure": 2.0,
        "Pneumothorax": 2.0,
        "Pericardial Effusion": 1.8,
    },
    # 心雑音+失神
    frozenset({"heart_murmur", "fainting"}): {
        "Heart Disease/CHF": 2.5,
        "Congestive Heart Failure": 2.5,
        "Aortic Stenosis": 2.0,
    },

    # ========== NEUROLOGICAL PATTERNS ==========
    # けいれん+よだれ
    frozenset({"seizures", "excessive_drooling"}): {
        "Poisoning/Toxicity": 2.0,
        "Epilepsy": 1.8,
        "Organophosphate Toxicity": 2.0,
        "Organophosphate Toxicosis": 2.0,
        "Rabies": 1.5,
    },
    frozenset({"seizures", "drooling"}): {
        "Poisoning/Toxicity": 2.0,
        "Epilepsy": 1.8,
        "Rabies": 1.5,
    },
    # けいれん+発熱
    frozenset({"seizures", "fever"}): {
        "Meningitis": 2.5,
        "Encephalitis": 2.5,
        "Rabies": 1.8,
    },
    # けいれん+意識障害
    frozenset({"seizures", "disorientation"}): {
        "Hepatic Encephalopathy": 2.0,
        "Encephalitis": 2.0,
        "Meningitis": 2.0,
    },

    # ========== HEMATOLOGIC PATTERNS ==========
    # 蒼白粘膜+無気力
    frozenset({"pale_gums", "lethargy"}): {
        "Immune-Mediated Hemolytic Anemia": 2.0,
        "Internal Hemorrhage": 2.0,
        "Tick-borne Disease": 1.8,
        "Feline Infectious Anemia (Hemobartonellosis)": 2.0,
        "Rodenticide Poisoning": 1.8,
    },
    # 蒼白粘膜+出血
    frozenset({"pale_gums", "bleeding"}): {
        "Rodenticide Poisoning": 2.5,
        "Coagulopathy": 2.0,
        "Thrombocytopenia": 1.8,
    },
    # 黄疸+蒼白粘膜
    frozenset({"jaundice", "pale_gums"}): {
        "Immune-Mediated Hemolytic Anemia": 2.0,
        "Liver Disease": 1.8,
    },

    # ========== LYMPHATIC/IMMUNE PATTERNS ==========
    # 発熱+リンパ節腫脹
    frozenset({"fever", "swollen_lymph_nodes"}): {
        "Lymphoma": 2.0,
        "Tick-borne Disease": 1.8,
        "Feline Leukemia Virus (FeLV)": 1.8,
        "Feline Immunodeficiency Virus (FIV)": 1.5,
        "Ehrlichiosis": 1.8,
    },
    frozenset({"fever", "swelling"}): {
        "Lymphoma": 1.5,
        "Abscess": 1.5,
    },

    # ========== MUSCULOSKELETAL PATTERNS ==========
    # 跛行+関節痛
    frozenset({"lameness_or_limping", "joint_pain_or_stiffness"}): {
        "Osteoarthritis": 2.0,
        "Hip Dysplasia": 1.8,
        "Cruciate Ligament Injury": 1.8,
        "Lyme Disease": 1.5,
        "Immune-Mediated Polyarthritis": 1.8,
    },
    frozenset({"swollen_joints", "stiffness"}): {
        "Osteoarthritis": 2.0,
        "Immune-Mediated Polyarthritis": 1.8,
        "Lyme Disease": 1.5,
    },
    # 跛行+腫脹
    frozenset({"limping", "swelling"}): {
        "Fracture": 1.9,
        "Dislocation": 1.8,
        "Cruciate Ligament Injury": 1.6,
    },

    # ========== OCULAR PATTERNS ==========
    # 目の白濁+目の充血
    frozenset({"cloudiness_in_eyes", "redness_in_eyes"}): {
        "Glaucoma": 2.5,
        "Uveitis": 2.0,
        "Corneal Ulcer": 1.5,
    },
    frozenset({"squinting", "eye_redness"}): {
        "Glaucoma": 2.0,
        "Uveitis": 2.0,
        "Corneal Ulcer": 1.5,
    },
    # 目の痛み+充血
    frozenset({"eye_pain", "eye_redness"}): {
        "Corneal Ulcer": 2.0,
        "Uveitis": 1.8,
    },

    # ========== DERMATOLOGIC PATTERNS ==========
    # 掻痒+脱毛
    frozenset({"itching", "hair_loss"}): {
        "Allergic Dermatitis": 1.8,
        "Atopic Dermatitis": 1.8,
        "Demodectic Mange": 1.8,
        "Fungal Infection": 1.5,
    },
    # 掻痒+紅斑
    frozenset({"itching", "redness"}): {
        "Allergic Dermatitis": 2.0,
        "Atopic Dermatitis": 1.8,
        "Contact Dermatitis": 1.6,
    },
    # 脱毛+悪臭
    frozenset({"hair_loss", "bad_odor"}): {
        "Bacterial Infection": 1.8,
        "Fungal Infection": 1.8,
    },

    # ========== SYSTEMIC PATTERNS ==========
    # 体重減少+食欲不振
    frozenset({"weight_loss", "loss_of_appetite"}): {
        "Cancer/Neoplasia": 1.8,
        "Kidney Disease (CKD)": 1.5,
        "Feline Chronic Kidney Disease (CKD)": 1.5,
        "Hyperthyroidism": 1.5,
        "Inflammatory Bowel Disease (IBD)": 1.5,
        "Feline Infectious Peritonitis (FIP)": 1.5,
    },
    frozenset({"weight_loss", "appetite_loss"}): {
        "Cancer/Neoplasia": 1.8,
        "Kidney Disease (CKD)": 1.5,
        "Hyperthyroidism": 1.5,
        "Inflammatory Bowel Disease (IBD)": 1.5,
    },
    # 体重減少+下痢
    frozenset({"weight_loss", "diarrhea"}): {
        "Inflammatory Bowel Disease (IBD)": 1.8,
        "Pancreatic Insufficiency": 1.8,
        "Intestinal Parasites": 1.5,
    },
    # 無気力+発熱
    frozenset({"lethargy", "fever"}): {
        "Infection": 2.0,
        "Sepsis": 2.0,
        "Inflammatory Disease": 1.5,
    },

    # ========== REPRODUCTIVE PATTERNS ==========
    # 多飲+排尿困難（膿尿症）
    frozenset({"excessive_thirst", "straining_to_urinate"}): {
        "Pyometra": 1.8,
        "Urinary Tract Infection": 1.5,
    },
    # 発熱+腹部膨満（膿尿症）
    frozenset({"fever", "bloated_abdomen"}): {
        "Pyometra": 2.0,
        "Peritonitis": 1.8,
    },
}


# ============================================================================
# TRIPLE SYMPTOM INTERACTIONS (New: 15+ patterns)
# ============================================================================
# Format: {frozenset({symptom1, symptom2, symptom3}): {disease_name: multiplier}}
# These represent highly specific symptom triplets that strongly suggest diagnoses.

SYMPTOM_TRIPLE_BOOST: Dict[frozenset, Dict[str, float]] = {
    # Parvovirus signature: 嘔吐+血便+無気力
    frozenset({"vomiting", "blood_in_stool", "lethargy"}): {
        "Canine Parvovirus": 2.5,
        "Parvovirus Infection": 2.5,
        "Hemorrhagic Gastroenteritis (HGE)": 2.0,
    },
    frozenset({"vomiting", "bloody_stool", "lethargy"}): {
        "Canine Parvovirus": 2.5,
        "Hemorrhagic Gastroenteritis (HGE)": 2.0,
    },

    # GDV signature: 嘔吐+腹部膨満+虚脱
    frozenset({"vomiting", "bloating", "collapse"}): {
        "Gastric Dilatation-Volvulus (GDV/Bloat)": 3.0,
    },
    frozenset({"vomiting", "bloated_abdomen", "collapse"}): {
        "Gastric Dilatation-Volvulus (GDV/Bloat)": 3.0,
    },

    # Pancreatitis: 嘔吐+腹痛+食欲不振
    frozenset({"vomiting", "abdominal_pain", "loss_of_appetite"}): {
        "Pancreatitis": 2.5,
    },
    frozenset({"vomiting", "abdominal_pain", "appetite_loss"}): {
        "Pancreatitis": 2.5,
    },

    # Heart failure: 咳+呼吸困難+運動不耐性
    frozenset({"coughing", "difficulty_breathing", "exercise_intolerance"}): {
        "Heart Disease/CHF": 2.5,
        "Congestive Heart Failure": 2.5,
        "Feline Hypertrophic Cardiomyopathy (HCM)": 2.0,
    },
    frozenset({"coughing", "labored_breathing", "exercise_intolerance"}): {
        "Heart Disease/CHF": 2.5,
        "Congestive Heart Failure": 2.5,
    },

    # Meningitis/Encephalitis: けいれん+発熱+無気力
    frozenset({"seizures", "fever", "lethargy"}): {
        "Meningitis": 2.5,
        "Encephalitis": 2.5,
        "Rabies": 1.8,
    },

    # Pyometra: 発熱+多飲+腹部膨満
    frozenset({"fever", "excessive_thirst", "bloated_abdomen"}): {
        "Pyometra": 2.5,
    },
    frozenset({"fever", "excessive_thirst", "bloating"}): {
        "Pyometra": 2.5,
    },

    # Diabetes: 多飲+頻尿+体重減少
    frozenset({"excessive_thirst", "frequent_urination", "weight_loss"}): {
        "Diabetes Mellitus": 2.5,
    },
    frozenset({"excessive_thirst", "excessive_urination", "weight_loss"}): {
        "Diabetes Mellitus": 2.5,
    },

    # Hemolytic Anemia: 黄疸+蒼白粘膜+無気力
    frozenset({"jaundice", "pale_gums", "lethargy"}): {
        "Immune-Mediated Hemolytic Anemia": 2.5,
        "Hemolytic Anemia": 2.0,
    },

    # Hepatic Encephalopathy: 黄疸+意識障害+けいれん
    frozenset({"jaundice", "disorientation", "seizures"}): {
        "Hepatic Encephalopathy": 2.5,
    },

    # CKD: 多飲+頻尿+体重減少
    frozenset({"excessive_thirst", "frequent_urination", "weight_loss"}): {
        "Kidney Disease (CKD)": 2.5,
        "Feline Chronic Kidney Disease (CKD)": 2.5,
    },

    # Urinary obstruction: 血尿+排尿困難+腹痛
    frozenset({"blood_in_urine", "straining_to_urinate", "abdominal_pain"}): {
        "Urethral Obstruction": 2.5,
        "Feline Lower Urinary Tract Disease (FLUTD)": 2.0,
    },
    frozenset({"bloody_urine", "straining_to_urinate", "abdominal_pain"}): {
        "Urethral Obstruction": 2.5,
    },

    # IBD: 下痢+嘔吐+体重減少
    frozenset({"diarrhea", "vomiting", "weight_loss"}): {
        "Inflammatory Bowel Disease (IBD)": 2.5,
    },

    # Rodenticide poisoning: 出血+蒼白粘膜+虚脱
    frozenset({"bleeding", "pale_gums", "collapse"}): {
        "Rodenticide Poisoning": 3.0,
        "Coagulopathy": 2.0,
    },
}
