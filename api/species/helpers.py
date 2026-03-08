"""Common helpers for species-specific disease analysis.

This module provides a generic `analyze_symptoms_generic` function that can be
used by each species-specific module to perform basic differential diagnosis.
It mirrors the dog symptom checker output structure but operates on a custom
disease list and symptom name mapping. A shared advice dictionary is also
defined here for consistent messaging across species.
"""

from __future__ import annotations

from typing import Any, Dict, List, Set, Tuple

# Default advice messages for various severity levels. These are used when
# species-specific modules do not supply their own advice dictionary.
ADVICE: Dict[str, Dict[str, str]] = {
    "low": {
        "en": "Low severity: Monitor the condition and consult a veterinarian if symptoms worsen.",
        "ja": "軽度: 様子を見て、症状が悪化した場合は獣医師に相談してください。",
    },
    "moderate": {
        "en": "Moderate severity: It is advisable to have the animal examined by a veterinarian soon.",
        "ja": "中等度: 早めに獣医師の診察を受けることをお勧めします。",
    },
    "high": {
        "en": "High severity: Prompt veterinary care is recommended.",
        "ja": "重度: 速やかに獣医師の診察を受けてください。",
    },
    "emergency": {
        "en": "Emergency: Seek immediate veterinary attention.",
        "ja": "緊急: 直ちに獣医師の診察を受けてください。",
    },
}


# =============================================================================
# BREED DATA PER SPECIES
# =============================================================================
# Each species maps breed_id -> {name, name_ja, risk: {disease_name: multiplier}}

SPECIES_BREEDS: Dict[str, List[Dict[str, Any]]] = {
    "cat": [
        {"id": "cat_mixed", "name": "Mixed Breed", "name_ja": "雑種（ミックス）",
         "risk": {}},
        {"id": "cat_persian", "name": "Persian", "name_ja": "ペルシャ",
         "risk": {"Polycystic Kidney Disease (PKD)": 2.5, "Feline Hypertrophic Cardiomyopathy (HCM)": 1.5,
                  "Feline Chronic Kidney Disease (CKD)": 1.8, "Brachycephalic Airway Syndrome": 2.0,
                  "Feline Lower Urinary Tract Disease (FLUTD)": 1.3}},
        {"id": "cat_scottish_fold", "name": "Scottish Fold", "name_ja": "スコティッシュフォールド",
         "risk": {"Scottish Fold Osteochondrodysplasia": 3.0, "Feline Hypertrophic Cardiomyopathy (HCM)": 1.8,
                  "Polycystic Kidney Disease (PKD)": 1.5, "Osteoarthritis (Degenerative Joint Disease)": 2.0}},
        {"id": "cat_munchkin", "name": "Munchkin", "name_ja": "マンチカン",
         "risk": {"Osteoarthritis": 2.0, "Intervertebral Disc Disease": 1.8,
                  "Lordosis": 1.5}},
        {"id": "cat_american_shorthair", "name": "American Shorthair", "name_ja": "アメリカンショートヘア",
         "risk": {"Feline Hypertrophic Cardiomyopathy (HCM)": 1.5, "Obesity": 1.3}},
        {"id": "cat_russian_blue", "name": "Russian Blue", "name_ja": "ロシアンブルー",
         "risk": {"Feline Lower Urinary Tract Disease (FLUTD)": 1.5, "Obesity": 1.5}},
        {"id": "cat_norwegian_forest", "name": "Norwegian Forest Cat", "name_ja": "ノルウェージャンフォレストキャット",
         "risk": {"Feline Hypertrophic Cardiomyopathy (HCM)": 1.8, "Hip Dysplasia": 1.5,
                  "Glycogen Storage Disease Type IV": 2.0}},
        {"id": "cat_maine_coon", "name": "Maine Coon", "name_ja": "メインクーン",
         "risk": {"Feline Hypertrophic Cardiomyopathy (HCM)": 2.5, "Hip Dysplasia": 1.8,
                  "Spinal Muscular Atrophy": 1.5, "Polycystic Kidney Disease (PKD)": 1.3}},
        {"id": "cat_ragdoll", "name": "Ragdoll", "name_ja": "ラグドール",
         "risk": {"Feline Hypertrophic Cardiomyopathy (HCM)": 2.0, "Feline Lower Urinary Tract Disease (FLUTD)": 1.5,
                  "Bladder Stones": 1.3}},
        {"id": "cat_bengal", "name": "Bengal", "name_ja": "ベンガル",
         "risk": {"Feline Hypertrophic Cardiomyopathy (HCM)": 1.5, "Progressive Retinal Atrophy (PRA)": 2.0,
                  "Feline Infectious Peritonitis (FIP)": 1.3}},
        {"id": "cat_siamese", "name": "Siamese", "name_ja": "シャム（サイアミーズ）",
         "risk": {"Feline Asthma": 2.0, "Amyloidosis": 1.8,
                  "Megaesophagus": 1.5, "Progressive Retinal Atrophy (PRA)": 1.5}},
        {"id": "cat_abyssinian", "name": "Abyssinian", "name_ja": "アビシニアン",
         "risk": {"Feline Chronic Kidney Disease (CKD)": 1.8, "Amyloidosis": 2.0,
                  "Progressive Retinal Atrophy (PRA)": 1.5, "Pyruvate Kinase Deficiency": 2.0}},
        {"id": "cat_british_shorthair", "name": "British Shorthair", "name_ja": "ブリティッシュショートヘア",
         "risk": {"Feline Hypertrophic Cardiomyopathy (HCM)": 2.0, "Polycystic Kidney Disease (PKD)": 1.5,
                  "Obesity": 1.5}},
        {"id": "cat_sphynx", "name": "Sphynx", "name_ja": "スフィンクス",
         "risk": {"Feline Hypertrophic Cardiomyopathy (HCM)": 2.5, "Skin Infections": 1.8,
                  "Urticaria Pigmentosa": 1.5}},
        {"id": "cat_exotic_shorthair", "name": "Exotic Shorthair", "name_ja": "エキゾチックショートヘア",
         "risk": {"Polycystic Kidney Disease (PKD)": 2.5, "Brachycephalic Airway Syndrome": 2.0,
                  "Feline Hypertrophic Cardiomyopathy (HCM)": 1.5}},
    ],
    "rabbit": [
        {"id": "rabbit_mixed", "name": "Mixed Breed", "name_ja": "雑種（ミックス）",
         "risk": {}},
        {"id": "rabbit_netherland_dwarf", "name": "Netherland Dwarf", "name_ja": "ネザーランドドワーフ",
         "risk": {"Malocclusion": 2.5, "Gastrointestinal Stasis": 1.5, "Pasteurellosis": 1.3}},
        {"id": "rabbit_holland_lop", "name": "Holland Lop", "name_ja": "ホーランドロップ",
         "risk": {"Otitis Media/Interna": 2.0, "Malocclusion": 1.8, "Gastrointestinal Stasis": 1.3}},
        {"id": "rabbit_mini_rex", "name": "Mini Rex", "name_ja": "ミニレッキス",
         "risk": {"Sore Hocks (Pododermatitis)": 2.0, "Gastrointestinal Stasis": 1.3}},
        {"id": "rabbit_lionhead", "name": "Lionhead", "name_ja": "ライオンヘッド",
         "risk": {"Malocclusion": 1.8, "Wool Block/Trichobezoar": 2.0}},
        {"id": "rabbit_flemish_giant", "name": "Flemish Giant", "name_ja": "フレミッシュジャイアント",
         "risk": {"Sore Hocks (Pododermatitis)": 2.0, "Spondylosis": 1.8, "Heart Disease": 1.5}},
        {"id": "rabbit_rex", "name": "Rex", "name_ja": "レッキス",
         "risk": {"Sore Hocks (Pododermatitis)": 2.5, "Gastrointestinal Stasis": 1.3}},
        {"id": "rabbit_lop_eared", "name": "Lop Eared (General)", "name_ja": "ロップイヤー（一般）",
         "risk": {"Otitis Media/Interna": 2.5, "Ear Mites": 1.5, "Dental Disease": 1.3}},
    ],
    "hamster": [
        {"id": "hamster_golden", "name": "Golden (Syrian)", "name_ja": "ゴールデン（シリアン）",
         "risk": {"Wet Tail (Proliferative Ileitis)": 2.0, "Hamster Pyometra": 1.8, "Amyloidosis": 1.5}},
        {"id": "hamster_djungarian", "name": "Djungarian (Winter White)", "name_ja": "ジャンガリアン",
         "risk": {"Diabetes Mellitus": 2.5, "Tumors/Neoplasia": 1.5}},
        {"id": "hamster_campbell", "name": "Campbell's Dwarf", "name_ja": "キャンベル",
         "risk": {"Diabetes Mellitus": 3.0, "Glaucoma": 1.5}},
        {"id": "hamster_roborovski", "name": "Roborovski", "name_ja": "ロボロフスキー",
         "risk": {"Tumors/Neoplasia": 1.3}},
    ],
    "ferret": [
        {"id": "ferret_standard", "name": "Standard", "name_ja": "スタンダード",
         "risk": {}},
        {"id": "ferret_marshall", "name": "Marshall Ferret", "name_ja": "マーシャルフェレット",
         "risk": {"Adrenal Disease": 2.0, "Insulinoma": 1.8, "Lymphoma": 1.5}},
        {"id": "ferret_angora", "name": "Angora", "name_ja": "アンゴラ",
         "risk": {"Adrenal Disease": 1.5, "Hairball/GI Obstruction": 1.8}},
    ],
    "guinea_pig": [
        {"id": "guinea_pig_american", "name": "American (Short Hair)", "name_ja": "アメリカン（短毛）",
         "risk": {}},
        {"id": "guinea_pig_abyssinian", "name": "Abyssinian", "name_ja": "アビシニアン",
         "risk": {"Ovarian Cysts": 1.5, "Diabetes Mellitus": 1.3}},
        {"id": "guinea_pig_peruvian", "name": "Peruvian", "name_ja": "ペルビアン",
         "risk": {"Dermatophytosis (Ringworm)": 1.8, "Heat Stroke": 1.5}},
        {"id": "guinea_pig_skinny", "name": "Skinny Pig", "name_ja": "スキニーギニアピッグ",
         "risk": {"Hypothermia": 2.0, "Skin Infections": 1.8, "Sunburn": 2.0}},
        {"id": "guinea_pig_teddy", "name": "Teddy", "name_ja": "テディ",
         "risk": {"Ear Wax Buildup": 1.5, "Dermatophytosis (Ringworm)": 1.3}},
    ],
    "chinchilla": [
        {"id": "chinchilla_standard", "name": "Standard Grey", "name_ja": "スタンダードグレー",
         "risk": {}},
        {"id": "chinchilla_velvet", "name": "Black Velvet", "name_ja": "ブラックベルベット",
         "risk": {"Lethal Gene Issues": 1.5}},
    ],
    "hedgehog": [
        {"id": "hedgehog_four_toed", "name": "Four-toed (African Pygmy)", "name_ja": "ヨツユビハリネズミ",
         "risk": {"Wobbly Hedgehog Syndrome (WHS)": 2.0, "Tumors/Neoplasia": 2.0,
                  "Obesity": 1.5, "Mite Infestation": 1.3}},
    ],
    "bird": [
        {"id": "bird_mixed", "name": "Mixed/Other", "name_ja": "その他",
         "risk": {}},
        {"id": "bird_canary", "name": "Canary", "name_ja": "カナリア",
         "risk": {"Air Sac Mites": 2.0, "Avian Pox": 1.5}},
        {"id": "bird_finch", "name": "Finch", "name_ja": "フィンチ",
         "risk": {"Air Sac Mites": 2.0, "Coccidiosis": 1.5}},
        {"id": "bird_java_sparrow", "name": "Java Sparrow", "name_ja": "文鳥",
         "risk": {"Egg Binding": 1.8, "Obesity": 1.5, "Iron Storage Disease": 1.5}},
    ],
    "parakeet": [
        {"id": "parakeet_budgerigar", "name": "Budgerigar", "name_ja": "セキセイインコ",
         "risk": {"Budgerigar Fledgling Disease (BFD)": 2.5, "Tumors/Neoplasia": 2.0,
                  "Scaly Face Mites": 1.8, "Megabacteriosis (AGY)": 2.0, "Goiter": 1.5}},
        {"id": "parakeet_cockatiel", "name": "Cockatiel", "name_ja": "オカメインコ",
         "risk": {"Fatty Liver Disease (Hepatic Lipidosis)": 2.0, "Night Frights": 1.5,
                  "Egg Binding": 1.8, "Chronic Egg Laying": 2.0}},
        {"id": "parakeet_lovebird", "name": "Lovebird", "name_ja": "コザクラインコ/ボタンインコ",
         "risk": {"Psittacine Beak and Feather Disease (PBFD)": 1.5, "Feather Plucking": 1.5,
                  "Chronic Egg Laying": 1.8}},
    ],
    "parrot": [
        {"id": "parrot_african_grey", "name": "African Grey", "name_ja": "ヨウム",
         "risk": {"Feather Plucking": 2.5, "Hypocalcemia": 2.5, "Aspergillosis": 2.0,
                  "Psittacine Beak and Feather Disease (PBFD)": 1.5}},
        {"id": "parrot_amazon", "name": "Amazon Parrot", "name_ja": "アマゾン",
         "risk": {"Fatty Liver Disease (Hepatic Lipidosis)": 2.5, "Obesity": 2.0,
                  "Foot Necrosis (Bumblefoot)": 1.5}},
        {"id": "parrot_macaw", "name": "Macaw", "name_ja": "コンゴウインコ",
         "risk": {"Proventricular Dilatation Disease (PDD)": 2.0, "Feather Plucking": 1.8,
                  "Psittacine Beak and Feather Disease (PBFD)": 1.5}},
        {"id": "parrot_cockatoo", "name": "Cockatoo", "name_ja": "オウム科",
         "risk": {"Feather Plucking": 3.0, "Psittacine Beak and Feather Disease (PBFD)": 2.0,
                  "Fatty Liver Disease (Hepatic Lipidosis)": 1.8}},
    ],
    "reptile": [
        {"id": "reptile_general", "name": "General Reptile", "name_ja": "爬虫類（一般）",
         "risk": {}},
    ],
    "tortoise": [
        {"id": "tortoise_russian", "name": "Russian Tortoise", "name_ja": "ロシアリクガメ",
         "risk": {"Respiratory Infection": 1.5, "Shell Rot": 1.3}},
        {"id": "tortoise_hermann", "name": "Hermann's Tortoise", "name_ja": "ヘルマンリクガメ",
         "risk": {"Metabolic Bone Disease": 1.5, "Herpesvirus": 1.5}},
        {"id": "tortoise_sulcata", "name": "Sulcata Tortoise", "name_ja": "ケヅメリクガメ",
         "risk": {"Pyramiding": 2.0, "Bladder Stones": 1.8, "Metabolic Bone Disease": 1.5}},
        {"id": "tortoise_leopard", "name": "Leopard Tortoise", "name_ja": "ヒョウモンガメ",
         "risk": {"Respiratory Infection": 1.8, "Parasitic Infection": 1.5}},
    ],
    "snake": [
        {"id": "snake_ball_python", "name": "Ball Python", "name_ja": "ボールパイソン",
         "risk": {"Respiratory Infection": 1.8, "Inclusion Body Disease (IBD)": 2.0,
                  "Anorexia/Feeding Refusal": 2.0, "Mite Infestation": 1.5}},
        {"id": "snake_corn_snake", "name": "Corn Snake", "name_ja": "コーンスネーク",
         "risk": {"Inclusion Body Disease (IBD)": 1.3, "Dysecdysis (Retained Shed)": 1.5}},
        {"id": "snake_king_snake", "name": "King Snake", "name_ja": "キングスネーク",
         "risk": {"Dysecdysis (Retained Shed)": 1.3}},
        {"id": "snake_boa", "name": "Boa Constrictor", "name_ja": "ボアコンストリクター",
         "risk": {"Inclusion Body Disease (IBD)": 2.5, "Respiratory Infection": 1.5,
                  "Mite Infestation": 1.5}},
    ],
    "lizard": [
        {"id": "lizard_leopard_gecko", "name": "Leopard Gecko", "name_ja": "ヒョウモントカゲモドキ",
         "risk": {"Metabolic Bone Disease": 1.5, "Cryptosporidiosis": 2.0,
                  "Dysecdysis (Retained Shed)": 1.5, "Impaction": 1.8}},
        {"id": "lizard_bearded_dragon", "name": "Bearded Dragon", "name_ja": "フトアゴヒゲトカゲ",
         "risk": {"Metabolic Bone Disease": 2.0, "Adenovirus Infection": 2.0,
                  "Yellow Fungus Disease": 1.8, "Impaction": 1.5, "Parasitic Infection": 1.5}},
        {"id": "lizard_crested_gecko", "name": "Crested Gecko", "name_ja": "クレステッドゲッコー",
         "risk": {"Metabolic Bone Disease": 1.5, "Tail Drop (Autotomy)": 1.3}},
        {"id": "lizard_chameleon", "name": "Chameleon", "name_ja": "カメレオン",
         "risk": {"Metabolic Bone Disease": 2.5, "Dehydration": 2.0,
                  "Respiratory Infection": 1.8, "Egg Binding": 1.8}},
        {"id": "lizard_iguana", "name": "Green Iguana", "name_ja": "グリーンイグアナ",
         "risk": {"Metabolic Bone Disease": 2.0, "Kidney Disease": 1.8,
                  "Bladder Stones": 1.5}},
    ],
    "amphibian": [
        {"id": "amphibian_axolotl", "name": "Axolotl", "name_ja": "ウーパールーパー",
         "risk": {"Fungal Infection": 2.0, "Gill Damage": 1.8, "Impaction": 1.5,
                  "Ammonia Poisoning": 1.5}},
        {"id": "amphibian_pacman_frog", "name": "Pacman Frog", "name_ja": "ベルツノガエル",
         "risk": {"Impaction": 2.0, "Obesity": 1.8, "Bacterial Dermatitis": 1.5}},
        {"id": "amphibian_tree_frog", "name": "Tree Frog", "name_ja": "アマガエル",
         "risk": {"Chytrid Fungus (Bd)": 2.0, "Red Leg Syndrome": 1.8}},
    ],
    "sugar_glider": [
        {"id": "sugar_glider_standard", "name": "Standard Grey", "name_ja": "スタンダードグレー",
         "risk": {}},
    ],
    "degu": [
        {"id": "degu_standard", "name": "Standard (Agouti)", "name_ja": "スタンダード（アグーチ）",
         "risk": {"Diabetes Mellitus": 2.5, "Cataracts": 2.0, "Dental Disease": 2.0}},
    ],
}


# =============================================================================
# SYMPTOM PAIR BOOST DICTIONARY
# =============================================================================
# When two specific symptoms co-occur, boost particular diseases.
# Format: {frozenset({symptom1, symptom2}): {disease_name: multiplier}}
# These represent clinically significant symptom combinations that strongly
# suggest specific diagnoses.

SYMPTOM_PAIR_BOOST: Dict[frozenset, Dict[str, float]] = {
    # 嘔吐 + 腹部膨満 → GDV (犬・全種共通で適用)
    frozenset({"vomiting", "bloating"}): {
        "Gastric Dilatation-Volvulus (GDV/Bloat)": 2.0,
        "Intestinal Obstruction": 1.5,
        "Gastrointestinal Stasis": 1.5,
    },
    # 多飲 + 頻尿 → 腎臓病・糖尿
    frozenset({"excessive_thirst", "frequent_urination"}): {
        "Kidney Disease (CKD)": 2.0,
        "Feline Chronic Kidney Disease (CKD)": 2.0,
        "Diabetes Mellitus": 2.0,
        "Cushing's Disease": 1.5,
        "Hyperthyroidism": 1.5,
        "Pyometra": 1.5,
    },
    # 咳 + 呼吸困難 → 心不全・肺炎
    frozenset({"coughing", "labored_breathing"}): {
        "Heart Disease/CHF": 1.8,
        "Feline Hypertrophic Cardiomyopathy (HCM)": 1.8,
        "Pneumonia": 1.8,
        "Feline Pneumonia": 1.8,
        "Pleural Effusion": 1.5,
        "Feline Asthma": 1.5,
    },
    # 嘔吐 + 血便 → パルボ・出血性胃腸炎
    frozenset({"vomiting", "blood_in_stool"}): {
        "Parvovirus Infection": 2.0,
        "Hemorrhagic Gastroenteritis (HGE)": 2.0,
        "Feline Panleukopenia": 2.0,
        "Intestinal Parasites": 1.5,
        "Inflammatory Bowel Disease (IBD)": 1.5,
    },
    # けいれん + よだれ → 中毒・てんかん
    frozenset({"seizures", "excessive_drooling"}): {
        "Poisoning/Toxicity": 2.0,
        "Epilepsy": 1.8,
        "Organophosphate Toxicity": 2.0,
        "Rabies": 1.5,
    },
    # 黄疸 + 食欲不振 → 肝臓病
    frozenset({"jaundice", "loss_of_appetite"}): {
        "Liver Disease": 2.0,
        "Feline Hepatic Lipidosis": 2.5,
        "Leptospirosis": 1.8,
        "Immune-Mediated Hemolytic Anemia": 1.8,
        "Cholangitis": 1.8,
    },
    # 体重減少 + 食欲不振 → がん・CKD
    frozenset({"weight_loss", "loss_of_appetite"}): {
        "Cancer/Neoplasia": 1.8,
        "Kidney Disease (CKD)": 1.5,
        "Feline Chronic Kidney Disease (CKD)": 1.5,
        "Hyperthyroidism": 1.5,
        "Inflammatory Bowel Disease (IBD)": 1.5,
        "Feline Infectious Peritonitis (FIP)": 1.5,
    },
    # 血尿 + 排尿困難 → 尿路結石・FLUTD
    frozenset({"blood_in_urine", "straining_to_urinate"}): {
        "Bladder Stones": 2.0,
        "Feline Lower Urinary Tract Disease (FLUTD)": 2.5,
        "Urinary Tract Infection": 1.8,
        "Urethral Obstruction": 2.0,
    },
    # 失神 + 運動不耐性 → 心臓病
    frozenset({"fainting", "exercise_intolerance"}): {
        "Heart Disease/CHF": 2.5,
        "Feline Hypertrophic Cardiomyopathy (HCM)": 2.0,
        "Aortic Stenosis": 2.0,
        "Pulmonic Stenosis": 1.8,
        "Cardiac Arrhythmia": 2.0,
    },
    # 発熱 + リンパ節腫脹 → 感染症・リンパ腫
    frozenset({"fever", "swollen_lymph_nodes"}): {
        "Lymphoma": 2.0,
        "Tick-borne Disease": 1.8,
        "Feline Leukemia Virus (FeLV)": 1.8,
        "Feline Immunodeficiency Virus (FIV)": 1.5,
        "Ehrlichiosis": 1.8,
    },
    # 下痢 + 嘔吐 → 急性胃腸炎・中毒
    frozenset({"diarrhea", "vomiting"}): {
        "Acute Gastroenteritis": 1.8,
        "Pancreatitis": 1.8,
        "Poisoning/Toxicity": 1.5,
        "Foreign Body Ingestion": 1.5,
        "Feline Panleukopenia": 1.5,
        "Parvovirus Infection": 1.5,
    },
    # 蒼白 + 無気力 → 貧血
    frozenset({"pale_gums", "lethargy"}): {
        "Immune-Mediated Hemolytic Anemia": 2.0,
        "Internal Hemorrhage": 2.0,
        "Tick-borne Disease": 1.8,
        "Feline Infectious Anemia (Hemobartonellosis)": 2.0,
        "Rodenticide Poisoning": 1.8,
    },
    # 咳 + 運動不耐性 → 心臓病・気管虚脱
    frozenset({"coughing", "exercise_intolerance"}): {
        "Heart Disease/CHF": 2.0,
        "Tracheal Collapse": 2.0,
        "Heartworm Disease": 1.8,
    },
    # 目の白濁 + 目の充血 → 緑内障
    frozenset({"cloudiness_in_eyes", "redness_in_eyes"}): {
        "Glaucoma": 2.5,
        "Uveitis": 2.0,
        "Corneal Ulcer": 1.5,
    },
    # 跛行 + 関節痛 → 関節疾患
    frozenset({"lameness_or_limping", "joint_pain_or_stiffness"}): {
        "Osteoarthritis": 2.0,
        "Hip Dysplasia": 1.8,
        "Cruciate Ligament Injury": 1.8,
        "Lyme Disease": 1.5,
        "Immune-Mediated Polyarthritis": 1.8,
    },
}


def _compute_severity(suspected: List[Dict[str, Any]]) -> str:
    """Determine the overall severity level from the list of suspected diseases.

    The rules are similar to the dog implementation: if any emergency
    disease is highly likely, return "emergency". If any high-urgency disease
    is high or moderately likely, return "high". If any disease is highly
    likely, return "moderate". Otherwise return "low".
    """
    # Emergency override
    for disease in suspected:
        if disease.get("_urgency") == "emergency" and disease.get("likelihood") == "high":
            return "emergency"
    # High severity conditions
    for disease in suspected:
        if disease.get("_urgency") in ("high", "emergency") and disease.get("likelihood") in ("high", "moderate"):
            return "high"
    # Moderate severity if any high likelihood
    for disease in suspected:
        if disease.get("likelihood") == "high":
            return "moderate"
    return "low"


def analyze_symptoms_generic(
    symptoms: List[str],
    diseases: List[Dict[str, Any]],
    symptom_names: Dict[str, Dict[str, str]],
    advice: Dict[str, Dict[str, str]] | None = None,
    *,
    onset: str | None = None,
    age_years: float | None = None,
    breed: str | None = None,
    species: str | None = None,
) -> Dict[str, Any]:
    """Generic differential diagnosis engine.

    Parameters
    ----------
    symptoms:
        A list of symptom identifiers provided by the user.
    diseases:
        A list of dictionaries representing diseases. Each dictionary must
        include the keys: ``name``, ``name_ja``, ``symptoms`` (a set of
        identifiers), ``description``, ``description_ja``, ``urgency``, and
        ``recommended_tests`` (list of strings).
        Optionally: ``onset_pattern`` (set of "acute"/"subacute"/"chronic")
        and ``age_predisposition`` (set of "puppy"/"young"/"adult"/"senior").
    symptom_names:
        A mapping from symptom identifiers to their bilingual names. Only
        identifiers present in this mapping will be included in the output.
    advice:
        Optional advice dictionary overriding the global ADVICE. Must follow
        the same structure as ADVICE if provided.
    onset:
        Optional time-course: "acute", "subacute", or "chronic".
    age_years:
        Optional age of the animal in years.
    breed:
        Optional breed identifier for breed-specific risk adjustment.
    species:
        Optional species identifier used to look up breed data.

    Returns
    -------
    dict
        A dictionary with the same structure as the dog symptom checker
        response: ``suspected_diseases``, ``recommended_tests``, ``severity``,
        ``general_advice``, ``general_advice_ja``, ``breed_genetic_tests``,
        ``breed_risk_applied``, ``onset_applied``, ``age_applied``,
        and ``symptom_names``.
    """
    symptom_set: Set[str] = set(symptoms)
    suspected: List[Dict[str, Any]] = []

    # Resolve age stage
    age_stage: str | None = None
    if age_years is not None:
        if age_years < 1.0:
            age_stage = "puppy"
        elif age_years < 3.0:
            age_stage = "young"
        elif age_years < 7.0:
            age_stage = "adult"
        else:
            age_stage = "senior"

    # Look up breed risk data
    breed_risk: Dict[str, float] = {}
    breed_risk_applied = False
    if breed and species:
        breeds_for_species = SPECIES_BREEDS.get(species, [])
        for b in breeds_for_species:
            if b["id"] == breed:
                breed_risk = b.get("risk", {})
                if breed_risk:
                    breed_risk_applied = True
                break

    # Pre-compute symptom pair boosts for current symptom set
    pair_boosts: Dict[str, float] = {}
    for pair, disease_boosts in SYMPTOM_PAIR_BOOST.items():
        if pair.issubset(symptom_set):
            for disease_name, multiplier in disease_boosts.items():
                # Keep highest boost if multiple pairs match same disease
                if disease_name not in pair_boosts or multiplier > pair_boosts[disease_name]:
                    pair_boosts[disease_name] = multiplier

    for disease in diseases:
        disease_symptoms = set(disease.get("symptoms", set()))
        if not disease_symptoms:
            continue
        matching = symptom_set & disease_symptoms
        if not matching:
            continue
        coverage = len(matching) / len(disease_symptoms)
        match_percent = round(coverage * 100)

        # Apply onset multiplier
        onset_multiplier = 1.0
        if onset:
            disease_onsets = disease.get("onset_pattern")
            if disease_onsets:
                if onset in disease_onsets:
                    onset_multiplier = 1.3
                else:
                    onset_multiplier = 0.7

        # Apply age multiplier
        age_multiplier = 1.0
        if age_stage:
            age_predisposition = disease.get("age_predisposition")
            if age_predisposition:
                if age_stage in age_predisposition:
                    age_multiplier = 1.25
                else:
                    age_multiplier = 0.75

        # Apply breed risk multiplier
        breed_multiplier = breed_risk.get(disease["name"], 1.0)

        # Apply symptom pair boost
        pair_multiplier = pair_boosts.get(disease["name"], 1.0)

        # Adjusted match percent
        adjusted_percent = min(round(match_percent * onset_multiplier * age_multiplier * breed_multiplier * pair_multiplier), 100)

        # Determine likelihood tiers similar to dog algorithm
        if adjusted_percent >= 50:
            likelihood = "high"
        elif adjusted_percent >= 30:
            likelihood = "moderate"
        else:
            likelihood = "low"
        # Map coverage percentage to a simple color class
        if adjusted_percent >= 70:
            color_class = "score-high"
        elif adjusted_percent >= 45:
            color_class = "score-moderate"
        elif adjusted_percent >= 25:
            color_class = "score-low"
        else:
            color_class = "score-minimal"
        suspected.append({
            "name": disease["name"],
            "name_ja": disease["name_ja"],
            "likelihood": likelihood,
            "match_percent": adjusted_percent,
            "color_class": color_class,
            "description": disease.get("description", ""),
            "description_ja": disease.get("description_ja", ""),
            "pathophysiology": disease.get("pathophysiology", ""),
            "pathophysiology_ja": disease.get("pathophysiology_ja", ""),
            "causes": disease.get("causes", ""),
            "causes_ja": disease.get("causes_ja", ""),
            "prevention": disease.get("prevention", ""),
            "prevention_ja": disease.get("prevention_ja", ""),
            "treatment": disease.get("treatment", ""),
            "treatment_ja": disease.get("treatment_ja", ""),
            "prognosis": disease.get("prognosis", ""),
            "prognosis_ja": disease.get("prognosis_ja", ""),
            "matching_symptoms": sorted(matching),
            "match_count": len(matching),
            "total_symptoms": len(disease_symptoms),
            "_urgency": disease.get("urgency", "low"),
            "_match_ratio": coverage,
        })

    # Sort results primarily by match_percent then by number of matching symptoms
    suspected.sort(key=lambda d: (d["match_percent"], d["match_count"]), reverse=True)

    # Compute overall severity
    severity = _compute_severity(suspected)

    # Collect recommended tests, preserving order and uniqueness. We look up
    # the corresponding disease definition by name and extend the list with
    # its recommended tests only once per unique test.
    recommended_tests: List[str] = []
    seen_tests: Set[str] = set()
    for entry in suspected:
        for disease in diseases:
            if disease.get("name") == entry.get("name"):
                for test in disease.get("recommended_tests", []):
                    if test not in seen_tests:
                        recommended_tests.append(test)
                        seen_tests.add(test)
                break

    # Clean internal fields
    for entry in suspected:
        entry.pop("_urgency", None)
        entry.pop("_match_ratio", None)

    # Determine advice dictionary
    advice_dict = advice or ADVICE
    advice_pair = advice_dict.get(severity, advice_dict["low"])

    # Build symptom names lookup
    used_symptoms: Set[str] = set()
    for entry in suspected:
        used_symptoms.update(entry["matching_symptoms"])
    symptom_names_lookup: Dict[str, Dict[str, str]] = {
        sid: symptom_names[sid] for sid in used_symptoms if sid in symptom_names
    }

    return {
        "suspected_diseases": suspected,
        "recommended_tests": recommended_tests,
        "severity": severity,
        "general_advice": advice_pair["en"],
        "general_advice_ja": advice_pair["ja"],
        "breed_genetic_tests": [],
        "breed_risk_applied": breed_risk_applied,
        "breed": breed,
        "onset_applied": onset is not None,
        "onset": onset,
        "age_applied": age_years is not None,
        "age_years": age_years,
        "age_stage": age_stage,
        "pair_boost_applied": len(pair_boosts) > 0,
        "symptom_names": symptom_names_lookup,
    }
