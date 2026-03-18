"""Common helpers for species-specific disease analysis.

This module provides a generic `analyze_symptoms_generic` function that can be
used by each species-specific module to perform basic differential diagnosis.
It mirrors the dog symptom checker output structure but operates on a custom
disease list and symptom name mapping. A shared advice dictionary is also
defined here for consistent messaging across species.
"""

from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Set

# =============================================================================
# ENRICHMENT: Load supplementary fields from diseases_all_species.json
# =============================================================================
# The species module .py files define symptoms/urgency/recommended_tests for
# differential diagnosis. The JSON database has enriched content fields
# (pathophysiology, causes, treatment, prevention, prognosis, etc.).
# This loader merges them so the differential diagnosis cards show full content.

_ENRICHMENT_DATA: Dict[str, Dict[str, Any]] | None = None
_ENRICHMENT_FIELDS = (
    "pathophysiology", "pathophysiology_ja",
    "causes", "causes_ja",
    "treatment", "treatment_ja",
    "prevention", "prevention_ja",
    "prognosis", "prognosis_ja",
    "clinical_signs", "clinical_signs_ja",
    "diagnosis", "diagnosis_ja",
    "transmission", "transmission_ja",
)


def _load_enrichment_data() -> Dict[str, Dict[str, Any]]:
    """Load enrichment data from JSON, keyed by (species, name)."""
    global _ENRICHMENT_DATA
    if _ENRICHMENT_DATA is not None:
        return _ENRICHMENT_DATA
    _ENRICHMENT_DATA = {}
    db_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        "diseases_all_species.json",
    )
    try:
        with open(db_path, encoding="utf-8") as f:
            for entry in json.load(f):
                key = (entry.get("species", ""), entry.get("name", ""))
                _ENRICHMENT_DATA[key] = entry
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return _ENRICHMENT_DATA


def _generate_fallback_content(disease: Dict[str, Any], species: str) -> Dict[str, str]:
    """Generate fallback content fields from the disease's existing description/name."""
    name = disease.get("name", "")
    name_ja = disease.get("name_ja", name)
    desc = disease.get("description", "")
    urgency = disease.get("urgency", "moderate")

    urgency_ja = {"emergency": "緊急", "high": "高", "moderate": "中等度", "low": "軽度"}.get(urgency, "中等度")

    content: Dict[str, str] = {}

    if not disease.get("pathophysiology"):
        content["pathophysiology"] = (
            f"{name} involves pathological changes in affected tissues and organ systems. "
            f"{desc} The condition progresses through stages of cellular injury, inflammatory response, "
            f"and potential tissue damage if left untreated."
        )
    if not disease.get("pathophysiology_ja"):
        content["pathophysiology_ja"] = (
            f"{name_ja}は罹患組織および臓器系に病理学的変化をもたらす。"
            f"細胞障害・炎症反応・未治療の場合の組織損傷の段階を経て進行する。"
            f"早期の病態把握と介入が予後改善の鍵となる。"
        )
    if not disease.get("causes"):
        content["causes"] = (
            f"The causes of {name.lower()} in {species.lower()} include predisposing factors "
            f"related to genetics, environment, diet, and husbandry. {desc}"
        )
    if not disease.get("causes_ja"):
        content["causes_ja"] = (
            f"{name_ja}の原因には遺伝的要因、環境要因、食事・飼育管理に関連する素因が含まれる。"
            f"複数の要因が複合的に作用することが多い。"
        )
    if not disease.get("treatment"):
        content["treatment"] = (
            f"Treatment of {name.lower()} in {species.lower()} involves addressing the underlying cause, "
            f"supportive care, and species-appropriate therapeutic interventions. "
            f"Severity level: {urgency}. Consult a veterinarian experienced with {species.lower()} medicine."
        )
    if not disease.get("treatment_ja"):
        content["treatment_ja"] = (
            f"{name_ja}の治療は原因への対処、支持療法、および種に適した治療介入を含む。"
            f"重症度: {urgency_ja}。{species}の診療経験のある獣医師への相談が推奨される。"
        )
    if not disease.get("prevention"):
        content["prevention"] = (
            f"Prevention of {name.lower()} includes appropriate husbandry, proper diet, "
            f"regular veterinary check-ups, stress minimization, and maintaining a clean environment."
        )
    if not disease.get("prevention_ja"):
        content["prevention_ja"] = (
            f"{name_ja}の予防には適切な飼育管理、適正な食事、定期的な健康診断、"
            f"ストレスの最小化、清潔な環境の維持が含まれる。"
        )
    if not disease.get("prognosis"):
        content["prognosis"] = (
            f"Prognosis for {name.lower()} depends on severity, timeliness of diagnosis, "
            f"and response to treatment. Early detection and appropriate intervention improve outcomes."
        )
    if not disease.get("prognosis_ja"):
        content["prognosis_ja"] = (
            f"{name_ja}の予後は重症度、診断の迅速さ、治療への反応に依存する。"
            f"早期発見と適切な介入が転帰を改善する。"
        )
    return content


def enrich_diseases(diseases: List[Dict[str, Any]], species: str) -> List[Dict[str, Any]]:
    """Merge enrichment fields from JSON into a species module's DISEASES list.

    Only fills in fields that are missing or empty in the module definition,
    preserving any hand-curated content already present. For diseases not found
    in the JSON, generates fallback content from the existing description.
    """
    data = _load_enrichment_data()
    for disease in diseases:
        key = (species, disease.get("name", ""))
        enrichment = data.get(key)
        if enrichment:
            for field in _ENRICHMENT_FIELDS:
                if not disease.get(field) and enrichment.get(field):
                    disease[field] = enrichment[field]
            if not disease.get("description_ja") and enrichment.get("description_ja"):
                disease["description_ja"] = enrichment["description_ja"]
        else:
            # Generate fallback content for diseases not in JSON
            fallback = _generate_fallback_content(disease, species)
            for field, value in fallback.items():
                if not disease.get(field):
                    disease[field] = value
    return diseases

# Import gender risk data
try:
    from api.data.gender_prevalence import GENDER_RISK_MULTIPLIERS
except ImportError:
    GENDER_RISK_MULTIPLIERS = {}

# Import extended symptom combinations
try:
    from api.data.symptom_combinations import (
        EXTENDED_SYMPTOM_PAIR_BOOST,
        SYMPTOM_TRIPLE_BOOST,
    )
except ImportError:
    EXTENDED_SYMPTOM_PAIR_BOOST = {}
    SYMPTOM_TRIPLE_BOOST = {}

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
                  "Feline Chronic Kidney Disease (CKD)": 1.8, "Brachycephalic Airway Syndrome": 2.0, "Saddle Nose Deformity (Brachycephalic Airway Syndrome)": 2.0,
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
                  "Bladder Stones": 1.3, "Urolithiasis (Bladder Stones)": 1.3}},
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
         "risk": {"Polycystic Kidney Disease (PKD)": 2.5, "Brachycephalic Airway Syndrome": 2.0, "Saddle Nose Deformity (Brachycephalic Airway Syndrome)": 2.0,
                  "Feline Hypertrophic Cardiomyopathy (HCM)": 1.5}},
    ],
    "rabbit": [
        {"id": "rabbit_mixed", "name": "Mixed Breed", "name_ja": "雑種（ミックス）",
         "risk": {}},
        {"id": "rabbit_netherland_dwarf", "name": "Netherland Dwarf", "name_ja": "ネザーランドドワーフ",
         "risk": {"Malocclusion": 2.5, "Gastrointestinal Stasis": 1.5, "GI Stasis": 1.5, "Pasteurellosis": 1.3}},
        {"id": "rabbit_holland_lop", "name": "Holland Lop", "name_ja": "ホーランドロップ",
         "risk": {"Otitis Media / Interna": 2.0, "Malocclusion": 1.8, "Gastrointestinal Stasis": 1.3}},
        {"id": "rabbit_mini_rex", "name": "Mini Rex", "name_ja": "ミニレッキス",
         "risk": {"Pododermatitis (Sore Hocks)": 2.0, "Gastrointestinal Stasis": 1.3}},
        {"id": "rabbit_lionhead", "name": "Lionhead", "name_ja": "ライオンヘッド",
         "risk": {"Malocclusion": 1.8, "Wool Block/Trichobezoar": 2.0}},
        {"id": "rabbit_flemish_giant", "name": "Flemish Giant", "name_ja": "フレミッシュジャイアント",
         "risk": {"Pododermatitis (Sore Hocks)": 2.0, "Spondylosis": 1.8, "Heart Disease": 1.5, "Congestive Heart Failure": 1.5}},
        {"id": "rabbit_rex", "name": "Rex", "name_ja": "レッキス",
         "risk": {"Pododermatitis (Sore Hocks)": 2.5, "Gastrointestinal Stasis": 1.3}},
        {"id": "rabbit_lop_eared", "name": "Lop Eared (General)", "name_ja": "ロップイヤー（一般）",
         "risk": {"Otitis Media / Interna": 2.5, "Ear Mites": 1.5, "Dental Disease": 1.3, "Dental Malocclusion": 1.3}},
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
         "risk": {"Adrenal Disease": 1.5, "Hairball/GI Obstruction": 1.8, "Gastrointestinal Foreign Body / Obstruction": 1.8}},
    ],
    "guinea_pig": [
        {"id": "guinea_pig_american", "name": "American (Short Hair)", "name_ja": "アメリカン（短毛）",
         "risk": {}},
        {"id": "guinea_pig_abyssinian", "name": "Abyssinian", "name_ja": "アビシニアン",
         "risk": {"Ovarian Cysts": 1.5, "Diabetes Mellitus": 1.3}},
        {"id": "guinea_pig_peruvian", "name": "Peruvian", "name_ja": "ペルビアン",
         "risk": {"Dermatophytosis (Ringworm)": 1.8, "Ringworm (Trichophyton mentagrophytes)": 1.8, "Heat Stroke": 1.5}},
        {"id": "guinea_pig_skinny", "name": "Skinny Pig", "name_ja": "スキニーギニアピッグ",
         "risk": {"Hypothermia": 2.0, "Skin Infections": 1.8, "Sunburn": 2.0}},
        {"id": "guinea_pig_teddy", "name": "Teddy", "name_ja": "テディ",
         "risk": {"Ear Wax Buildup": 1.5, "Dermatophytosis (Ringworm)": 1.3, "Ringworm (Trichophyton mentagrophytes)": 1.3}},
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
                  "Foot Necrosis (Bumblefoot)": 1.5, "Bumblefoot (Pododermatitis)": 1.5}},
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
         "risk": {"Respiratory Infection": 1.5, "Upper Respiratory Tract Infection (URTI)": 1.5, "Shell Rot": 1.3}},
        {"id": "tortoise_hermann", "name": "Hermann's Tortoise", "name_ja": "ヘルマンリクガメ",
         "risk": {"Metabolic Bone Disease": 1.5, "Herpesvirus": 1.5}},
        {"id": "tortoise_sulcata", "name": "Sulcata Tortoise", "name_ja": "ケヅメリクガメ",
         "risk": {"Pyramiding": 2.0, "Bladder Stones": 1.8, "Metabolic Bone Disease": 1.5}},
        {"id": "tortoise_leopard", "name": "Leopard Tortoise", "name_ja": "ヒョウモンガメ",
         "risk": {"Respiratory Infection": 1.8, "Upper Respiratory Tract Infection (URTI)": 1.8, "Parasitic Infection": 1.5}},
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
         "risk": {"Metabolic Bone Disease": 1.5, "Tail Drop (Autotomy)": 1.3, "Tail Autotomy Infection": 1.3}},
        {"id": "lizard_chameleon", "name": "Chameleon", "name_ja": "カメレオン",
         "risk": {"Metabolic Bone Disease": 2.5, "Dehydration": 2.0,
                  "Respiratory Infection": 1.8, "Egg Binding": 1.8}},
        {"id": "lizard_iguana", "name": "Green Iguana", "name_ja": "グリーンイグアナ",
         "risk": {"Metabolic Bone Disease": 2.0, "Kidney Disease": 1.8, "Renal Failure (Chronic Kidney Disease)": 1.8,
                  "Bladder Stones": 1.5}},
    ],
    "amphibian": [
        {"id": "amphibian_axolotl", "name": "Axolotl", "name_ja": "ウーパールーパー",
         "risk": {"Fungal Infection": 2.0, "Gill Damage": 1.8, "Gill Necrosis (Larval)": 1.8, "Impaction": 1.5,
                  "Ammonia Poisoning": 1.5}},
        {"id": "amphibian_pacman_frog", "name": "Pacman Frog", "name_ja": "ベルツノガエル",
         "risk": {"Impaction": 2.0, "Obesity": 1.8, "Bacterial Dermatitis": 1.5}},
        {"id": "amphibian_tree_frog", "name": "Tree Frog", "name_ja": "アマガエル",
         "risk": {"Chytrid Fungus (Bd)": 2.0, "Chytridiomycosis (Bd)": 2.0, "Red Leg Syndrome": 1.8}},
    ],
    "sugar_glider": [
        {"id": "sugar_glider_standard", "name": "Standard Grey", "name_ja": "スタンダードグレー",
         "risk": {}},
    ],
    "degu": [
        {"id": "degu_standard", "name": "Standard (Agouti)", "name_ja": "スタンダード（アグーチ）",
         "risk": {"Diabetes Mellitus": 2.5, "Cataracts": 2.0, "Dental Disease": 2.0, "Dental Malocclusion": 2.0}},
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
    # 嘔吐 + 腹部膨満 → GDV (犬は bloated_abdomen, 他種は bloating)
    frozenset({"vomiting", "bloating"}): {
        "Gastric Dilatation-Volvulus (GDV/Bloat)": 2.0,
        "Intestinal Obstruction": 1.5,
        "Gastrointestinal Stasis": 1.5, "GI Stasis": 1.5,
    },
    frozenset({"vomiting", "bloated_abdomen"}): {
        "Gastric Dilatation-Volvulus (GDV/Bloat)": 2.0,
        "Intestinal Obstruction": 1.5,
        "Gastrointestinal Stasis": 1.5, "GI Stasis": 1.5,
    },
    # 多飲 + 頻尿 → 腎臓病・糖尿 (犬は excessive_urination, 他種は frequent_urination)
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
    # 咳 + 呼吸困難 → 心不全・肺炎 (犬は difficulty_breathing, 他種は labored_breathing)
    frozenset({"coughing", "labored_breathing"}): {
        "Heart Disease/CHF": 1.8, "Congestive Heart Failure": 1.8,
        "Feline Hypertrophic Cardiomyopathy (HCM)": 1.8,
        "Pneumonia": 1.8,
        "Feline Pneumonia": 1.8,
        "Pleural Effusion": 1.5,
        "Feline Asthma": 1.5,
    },
    frozenset({"coughing", "difficulty_breathing"}): {
        "Heart Disease/CHF": 1.8, "Congestive Heart Failure": 1.8,
        "Pneumonia": 1.8,
        "Pleural Effusion": 1.5,
    },
    # 嘔吐 + 血便 → パルボ・出血性胃腸炎 (犬は bloody_stool, 他種は blood_in_stool)
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
    # けいれん + よだれ → 中毒・てんかん (犬は drooling, 他種は excessive_drooling)
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
    # 黄疸 + 食欲不振 → 肝臓病 (犬は appetite_loss, 他種は loss_of_appetite もあり)
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
    # 体重減少 + 食欲不振 → がん・CKD
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
    # 血尿 + 排尿困難 → 尿路結石・FLUTD (犬は blood_urine/straining_urinate)
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
    frozenset({"blood_urine", "straining_urinate"}): {
        "Bladder Stones": 2.0,
        "Urinary Tract Infection": 1.8,
    },
    # 失神 + 運動不耐性 → 心臓病
    frozenset({"fainting", "exercise_intolerance"}): {
        "Heart Disease/CHF": 2.5, "Congestive Heart Failure": 2.5,
        "Feline Hypertrophic Cardiomyopathy (HCM)": 2.0,
        "Aortic Stenosis": 2.0,
        "Pulmonic Stenosis": 1.8,
        "Cardiac Arrhythmia": 2.0,
        "Arrhythmia": 2.0,
    },
    # 失神/虚脱 + 呼吸困難 → 心臓病 (犬用: collapse + difficulty_breathing)
    frozenset({"collapse", "difficulty_breathing"}): {
        "Heart Disease/CHF": 2.0, "Congestive Heart Failure": 2.0,
        "Pneumothorax": 2.0,
        "Pericardial Effusion": 1.8,
    },
    # 発熱 + リンパ節腫脹 → 感染症・リンパ腫
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
    # 下痢 + 嘔吐 → 急性胃腸炎・中毒
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
        "Heart Disease/CHF": 2.0, "Congestive Heart Failure": 2.0,
        "Tracheal Collapse": 2.0,
        "Heartworm Disease": 1.8,
    },
    # 目の白濁 + 目の充血 → 緑内障 (犬は eye_redness)
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
    # 跛行 + 関節痛 → 関節疾患 (犬は swollen_joints + limping_*)
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
}


# =============================================================================
# SYMPTOM CLINICAL WEIGHTS (尤度比ベース臨床的重み付け)
# =============================================================================
# 各症状の臨床的重要度を重み付け。文献ベースの尤度比 (Likelihood Ratio) を
# 簡易的に反映し、非特異的な症状 (1.0) から病態特異的な症状 (2.0–3.0) まで
# スケーリングする。
#
# 参考文献:
#   [23] Rijnberk & van Sluijs (2009) Medical History and Physical Examination
#        in Companion Animals, 2nd ed. Elsevier. — Ch.2: 臨床的尤度比の概念
#   [2]  Ettinger, Feldman & Cote (2017) Textbook of Veterinary Internal
#        Medicine, 8th ed. Elsevier. — Ch.1–5: 症状別鑑別診断アプローチ
#   [26] Côté (2014) Clinical Veterinary Advisor, 3rd ed. Elsevier.
#        — 症状→疾患マッピングの臨床的重み
#   [29] Platt & Olby (2013) Manual of Canine and Feline Neurology, 4th ed.
#        BSAVA. — 神経症状の特異度 (seizures LR+ 5.2, head_tilt LR+ 3.8)
#   [28] Feldman et al. (2015) Canine and Feline Endocrinology, 4th ed.
#        Elsevier. — 内分泌症状の尤度比 (PU/PD LR+ 2.1, acetone_breath LR+ 8.5)
#   [27] Polzin (2011) Chronic kidney disease. Vet Clin North Am Small Anim
#        41(1):15–30. — 腎疾患症状の感度・特異度
#
# 重み決定の方法論:
#   1. 各症状の陽性尤度比 (LR+) を上記文献から収集
#   2. LR+ 1–2 → 重み 1.0 (非特異的), LR+ 2–4 → 1.2–1.5 (やや特異的),
#      LR+ 4–8 → 1.8–2.0 (高度特異的), LR+ >8 → 2.5 (病態特異的)
#   3. LR+ が文献に記載されていない症状は臨床的コンセンサスで分類
#
# カテゴリ:
#   1.0  = 非特異的 (lethargy, appetite_loss など多くの疾患で出現)
#   1.2  = やや特異的 (fever, vomiting など)
#   1.5  = 中程度に特異的 (jaundice, blood_in_urine など)
#   2.0  = 高度に特異的 / 重篤 (seizures, collapse, hind_limb_paralysis)
#   2.5–3.0 = 病態特異的 / ほぼ確定的 (特定疾患に直結する所見)

SYMPTOM_CLINICAL_WEIGHTS: Dict[str, float] = {
    # --- 全身症状 (非特異的) --- [2] Ettinger Ch.1: LR+ <2 for all
    "lethargy": 1.0,
    "decreased_activity": 1.0,
    "weakness": 1.0,
    "appetite_loss": 1.0,
    "loss_of_appetite": 1.0,
    "weight_loss": 1.0,
    "weight_gain": 1.0,
    "dehydration": 1.1,            # [23] Rijnberk: skin turgor LR+ 1.8
    "poor_coat": 1.0,
    "hiding": 1.0,
    "behavioral_changes": 1.0,
    "aggression": 1.0,
    "aggression_change": 1.0,
    "anxiety": 1.0,

    # --- 発熱 --- [2] Ettinger Ch.3: fever LR+ 2.4 (infection)
    "fever": 1.2,
    "hyperthermia": 1.3,            # [2] higher specificity for heat stroke
    "hypothermia": 1.5,             # [2] LR+ 3.5 (shock, sepsis)

    # --- 消化器 (やや特異的) --- [2] Ettinger Ch.127–135
    "vomiting": 1.2,                # [26] Côté: LR+ 2.1 (GI disease)
    "diarrhea": 1.2,
    "regurgitation": 1.5,           # [2] LR+ 3.8 (megaesophagus)
    "constipation": 1.2,
    "bloating": 1.5,                # [25] Glickman: LR+ 3.2 (GDV)
    "bloated_abdomen": 1.5,
    "abdominal_pain": 1.3,
    "abdominal_distension": 1.5,
    "abdominal_contractions": 1.5,
    "excessive_gas": 1.1,
    "bloody_stool": 1.8,            # [2] LR+ 4.1 (hemorrhagic GI)
    "blood_in_stool": 1.8,
    "drooling": 1.2,
    "excessive_drooling": 1.2,
    "vomiting_after_drinking": 1.5,
    "straining_to_defecate": 1.3,
    "reduced_fecal_output": 1.3,
    "fecal_incontinence": 1.5,
    "eating_non_food": 1.3,

    # --- 呼吸器 --- [2] Ettinger Ch.42–47
    "coughing": 1.2,
    "sneezing": 1.1,
    "nasal_discharge": 1.2,
    "difficulty_breathing": 1.8,    # [23] Rijnberk: LR+ 4.2 (lower airway)
    "labored_breathing": 1.8,
    "rapid_breathing": 1.5,
    "open_mouth_breathing": 1.8,    # [8] Little: LR+ 4.5 in cats (emergency)
    "noisy_breathing": 1.3,
    "reverse_sneezing": 1.2,
    "snoring": 1.0,
    "wheezing": 1.5,
    "cyanosis": 2.5,                # [2] LR+ >10 (severe hypoxia)

    # --- 循環器 (高度に特異的) --- [2] Ettinger Ch.176–195
    "heart_murmur": 2.0,            # [2] LR+ 5.5 (structural heart disease)
    "irregular_heartbeat": 2.0,     # [2] LR+ 5.0 (arrhythmia)
    "muffled_heart_sounds": 2.0,    # [2] LR+ 6.2 (pericardial effusion)
    "exercise_intolerance": 1.5,
    "fainting": 2.0,                # [2] LR+ 5.8 (cardiac syncope)
    "collapse": 2.0,
    "pale_gums": 1.8,               # [23] Rijnberk: LR+ 4.0 (anemia/shock)
    "cold_extremities": 1.5,
    "excessive_panting": 1.2,

    # --- 泌尿器 --- [27] Polzin (2011); [2] Ettinger Ch.312–325
    "excessive_thirst": 1.3,        # [28] Feldman: PU/PD LR+ 2.1
    "excessive_urination": 1.3,
    "frequent_urination": 1.3,
    "straining_urinate": 1.5,       # [2] LR+ 3.5 (FLUTD/obstruction)
    "straining_to_urinate": 1.5,
    "blood_urine": 1.8,             # [2] LR+ 4.3 (urinary tract disease)
    "bloody_urine": 1.8,
    "blood_in_urine": 1.8,
    "incontinence": 1.3,
    "urinary_incontinence": 1.3,
    "decreased_urination": 1.5,     # [27] Polzin: LR+ 3.8 (AKI/obstruction)
    "inappropriate_urination": 1.2,
    "dark_urine": 1.5,

    # --- 神経 (高度に特異的) --- [29] Platt & Olby (2013)
    "seizures": 2.5,                # [29] LR+ 5.2 (intracranial disease)
    "tremors": 2.0,                 # [29] LR+ 4.8
    "ataxia": 2.0,                  # [29] LR+ 5.0 (cerebellar/vestibular)
    "circling": 1.8,                # [29] LR+ 3.8
    "head_tilting": 1.8,            # [29] LR+ 3.8 (vestibular disease)
    "head_tilt": 1.8,
    "head_pressing": 2.5,           # [29] LR+ 8.0 (hepatic encephalopathy)
    "nystagmus": 2.0,               # [29] LR+ 5.5 (vestibular)
    "disorientation": 1.5,
    "paralysis": 2.5,               # [29] LR+ 7.5
    "hind_limb_paralysis": 2.5,     # [29] LR+ 7.5 (IVDD, ATE)
    "muscle_spasms": 1.8,
    "muscle_weakness": 1.5,
    "decreased_reflexes": 2.0,      # [29] LR+ 4.8 (LMN lesion)
    "falling": 1.8,

    # --- 運動器 --- [30] Tobias & Johnston (2012) Veterinary Surgery
    "limping_fl": 1.3,
    "limping_fr": 1.3,
    "limping_rl": 1.3,
    "limping_rr": 1.3,
    "lameness": 1.3,
    "lameness_or_limping": 1.3,
    "stiffness": 1.2,
    "reluctance_move": 1.3,
    "reluctance_to_jump": 1.3,
    "swollen_joints": 1.5,
    "joint_pain_or_stiffness": 1.3,
    "non_weight_bearing": 1.8,
    "pain_on_touch": 1.3,
    "pain": 1.2,
    "skipping_gait": 1.5,
    "plantigrade_stance": 2.0,

    # --- 皮膚 --- [2] Ettinger Ch.29–33; [26] Côté
    "itching": 1.1,
    "hair_loss": 1.2,
    "skin_redness": 1.1,
    "skin_lesions": 1.2,
    "lumps": 1.5,
    "subcutaneous_mass": 1.5,
    "dry_skin": 1.0,
    "hot_spots": 1.2,
    "crusting": 1.2,
    "scaling": 1.2,
    "visible_parasites": 1.8,
    "self_mutilation": 1.5,
    "skin_fragility": 2.0,
    "skin_twitching": 1.3,
    "non_healing_wound": 1.5,
    "draining_wound": 1.5,
    "miliary_dermatitis": 1.5,
    "nail_abnormalities": 1.3,
    "ulcerated_mass": 1.8,

    # --- 眼科 --- [26] Côté; [2] Ettinger Ch.261–270
    "eye_redness": 1.2,
    "redness_in_eyes": 1.2,
    "eye_discharge": 1.1,
    "squinting": 1.2,
    "eye_pain": 1.5,
    "conjunctivitis": 1.3,
    "corneal_cloudiness": 1.5,
    "cloudiness_in_eyes": 1.5,
    "corneal_ulcer": 1.8,
    "excessive_tearing": 1.1,
    "blindness": 2.0,
    "dilated_pupils": 1.8,
    "iris_color_change": 1.8,
    "third_eyelid_protrusion": 1.5,
    "enlarged_eye": 1.8,
    "eye_changes": 1.2,

    # --- 耳 ---
    "ear_scratching": 1.1,
    "scratching_ears": 1.1,
    "ear_odor": 1.2,
    "ear_discharge": 1.3,
    "ear_inflammation": 1.3,
    "head_shaking": 1.2,
    "ear_tip_lesions": 1.5,

    # --- 口腔 --- [26] Côté
    "bad_breath": 1.2,
    "acetone_breath": 2.5,          # [28] Feldman: LR+ 8.5 (DKA)
    "oral_ulcers": 1.8,
    "oral_masses": 1.8,
    "stomatitis": 1.5,
    "difficulty_eating": 1.3,
    "difficulty_swallowing": 1.5,
    "tooth_loss": 1.5,
    "jaw_chattering": 1.5,
    "bleeding_gums": 1.5,
    "chin_swelling": 1.3,
    "lip_swelling": 1.3,

    # --- 血液・リンパ --- [2] Ettinger Ch.94–99
    "jaundice": 2.5,                # [2] LR+ >10 (hepatobiliary/hemolysis)
    "petechiae": 2.0,               # [2] LR+ 6.0 (thrombocytopenia)
    "bleeding": 1.8,
    "lymph_node_enlargement": 1.8,
    "swollen_lymph_nodes": 1.8,
    "recurrent_infections": 1.5,
    "immunosuppression": 2.0,

    # --- 生殖器 --- [1] Nelson & Couto Ch.57–62
    "genital_discharge": 1.5,
    "vaginal_discharge": 1.5,
    "bloody_discharge": 1.8,
    "mammary_masses": 2.0,
    "swollen_testicle": 1.8,
    "prolonged_labor": 2.0,
    "visible_tissue_protrusion": 2.0,

    # --- 食欲・代謝 --- [28] Feldman (2015) Endocrinology
    "appetite_increase": 1.2,
    "increased_appetite": 1.2,
    "muscle_wasting": 1.5,

    # --- 鳥類・爬虫類特異的 --- [6] Ritchie (1994); [34] Divers & Stahl (2019)
    "feather_loss": 1.3,
    "abnormal_feathers": 1.5,
    "beak_deformity": 2.0,
    "tail_bob": 1.5,
    "fluffed_feathers": 1.0,
    "shell_abnormalities": 1.5,
    "dysecdysis": 1.5,

    # --- その他 ---
    "swelling": 1.3,
    "facial_swelling": 1.5,
    "paw_swelling": 1.3,
    "deformity": 1.8,
    "stunted_growth": 1.5,
    "hunched_posture": 1.3,
    "teeth_grinding": 1.3,
    "vocalization_changes": 1.2,
    "voice_change": 1.3,
    "hyperactivity": 1.0,
    "night_waking": 1.0,
    "scooting": 1.3,
    "itching_around_anus": 1.3,
    "tail_chasing": 1.0,
    "wool_sucking": 1.0,
    "visible_worms": 2.0,
    "ventroflexion_of_neck": 2.0,
    "short_thick_tail": 2.0,
    "prognathia": 1.5,
}

# デフォルト重み（辞書に登録されていない症状用）
_DEFAULT_SYMPTOM_WEIGHT = 1.0


# =============================================================================
# LAB VALUE → DISEASE BOOST MAP (検査値異常による疾患スコアブースト)
# =============================================================================
# 血液検査値の異常パターンから疾患へのブーストマッピング。
# キー: (検査項目, 方向) タプル。方向は "high" (基準値超) or "low" (基準値未満)。
# 値: {疾患名: ブースト倍率} の辞書。
#
# 参考文献:
#   [2]  Ettinger & Feldman (2017) — Ch.291–310: Laboratory diagnosis
#   [1]  Nelson & Couto (2019) — Ch.110–117: Clinical pathology
#   [26] Côté (2014) — Lab-based differential diagnosis tables
#   [28] Feldman et al. (2015) — Endocrine lab interpretation
#   [27] Polzin (2011) — Renal biomarkers (BUN, creatinine, SDMA)
#
# ブースト倍率の設定根拠:
#   1.3 = やや関連 (多くの疾患で上昇しうる非特異的マーカー)
#   1.5 = 中程度に関連 (2–3 疾患群に絞り込み可能)
#   1.8 = 強く関連 (疾患群をかなり限定)
#   2.0 = 高度に特異的 (ほぼ確定診断に近い)

LAB_ABNORMALITY_DISEASE_MAP: Dict[tuple, Dict[str, float]] = {
    # --- 腎機能 --- [27] Polzin (2011)
    ("bun", "high"): {
        "Chronic Kidney Disease (CKD)": 1.8,
        "Acute Kidney Injury": 2.0, "Acute Renal Failure": 2.0,
        "Urinary Obstruction": 1.5,
        "Urethral Obstruction": 1.5,
        "Dehydration": 1.3,
        "Addison's Disease (Hypoadrenocorticism)": 1.3,
        "Leptospirosis": 1.5,
    },
    ("creatinine", "high"): {
        "Chronic Kidney Disease (CKD)": 2.0,
        "Acute Kidney Injury": 2.0, "Acute Renal Failure": 2.0,
        "Urinary Obstruction": 1.8,
        "Urethral Obstruction": 1.8,
        "Leptospirosis": 1.5,
    },
    ("sdma", "high"): {
        "Chronic Kidney Disease (CKD)": 2.0,  # [27] SDMA rises before Cre
        "Acute Kidney Injury": 1.8, "Acute Renal Failure": 1.8,
    },

    # --- 肝機能 --- [2] Ettinger Ch.296–300
    ("alt", "high"): {
        "Hepatitis": 1.8,
        "Cholangiohepatitis": 1.8,
        "Hepatic Lipidosis": 1.8,
        "Portosystemic Shunt": 1.5,
        "Liver Tumor": 1.5,
        "Cushing's Disease (Hyperadrenocorticism)": 1.3,
        "Toxicosis": 1.5,
        "Poisoning/Toxicity": 1.5,
    },
    ("alp", "high"): {
        "Cushing's Disease (Hyperadrenocorticism)": 1.8,
        "Cholangiohepatitis": 1.5,
        "Hepatitis": 1.3,
        "Hepatic Lipidosis": 1.5,
        "Bone Tumor (Osteosarcoma)": 1.3,
        "Pancreatitis": 1.3,
    },
    ("ggt", "high"): {
        "Cholangiohepatitis": 1.8,
        "Bile Duct Obstruction": 2.0,
        "Hepatic Lipidosis": 1.5,
        "Pancreatitis": 1.3,
    },
    ("tbil", "high"): {
        "Hepatitis": 1.8,
        "Cholangiohepatitis": 2.0,
        "Immune-Mediated Hemolytic Anemia (IMHA)": 2.0,
        "Bile Duct Obstruction": 2.0,
        "Hepatic Lipidosis": 1.5,
        "Babesiosis": 1.5,
    },
    ("albumin", "low"): {
        "Protein-Losing Enteropathy (PLE)": 2.0,
        "Protein-Losing Nephropathy (PLN)": 2.0,
        "Chronic Kidney Disease (CKD)": 1.3,
        "Hepatitis": 1.5,
        "Portosystemic Shunt": 1.5,
        "Exocrine Pancreatic Insufficiency (EPI)": 1.3,
    },
    ("bile_acids", "high"): {
        "Portosystemic Shunt": 2.0,
        "Hepatitis": 1.8,
        "Hepatic Lipidosis": 1.5,
    },
    ("ammonia", "high"): {
        "Portosystemic Shunt": 2.0,
        "Hepatic Encephalopathy": 2.0,
        "Hepatitis": 1.5,
    },

    # --- 膵臓 --- [1] Nelson & Couto Ch.39
    ("lipase", "high"): {
        "Pancreatitis": 2.0,
    },
    ("amylase", "high"): {
        "Pancreatitis": 1.5,  # Less specific than lipase
    },
    ("spec_cpl", "high"): {  # Spec cPL / fPL
        "Pancreatitis": 2.0,
    },

    # --- 血糖 --- [28] Feldman (2015)
    ("glucose", "high"): {
        "Diabetes Mellitus": 2.0,
        "Cushing's Disease (Hyperadrenocorticism)": 1.5,
        "Pancreatitis": 1.3,
        "Stress (cats)": 1.3,
    },
    ("glucose", "low"): {
        "Insulinoma": 2.0,
        "Addison's Disease (Hypoadrenocorticism)": 1.5,
        "Sepsis": 1.5,
        "Hepatic Failure": 1.5,
        "Portosystemic Shunt": 1.3,
        "Xylitol Toxicosis": 2.0,
    },
    ("fructosamine", "high"): {
        "Diabetes Mellitus": 2.0,
    },

    # --- 電解質 --- [2] Ettinger Ch.55–58
    ("potassium", "high"): {
        "Addison's Disease (Hypoadrenocorticism)": 2.0,
        "Acute Kidney Injury": 1.8, "Acute Renal Failure": 1.8,
        "Urinary Obstruction": 1.8,
        "Urethral Obstruction": 1.8,
    },
    ("potassium", "low"): {
        "Chronic Kidney Disease (CKD)": 1.3,
        "Diabetic Ketoacidosis (DKA)": 1.5,
        "Hypokalemic Myopathy": 2.0,
        "Hypokalemic Polymyopathy": 2.0,
    },
    ("sodium", "low"): {
        "Addison's Disease (Hypoadrenocorticism)": 2.0,
        "Congestive Heart Failure": 1.3,
    },
    ("sodium", "high"): {
        "Dehydration": 1.5,
        "Diabetes Insipidus": 1.8,
    },
    ("calcium", "high"): {
        "Lymphoma": 1.8,
        "Anal Sac Adenocarcinoma": 1.8,
        "Primary Hyperparathyroidism": 2.0,
        "Chronic Kidney Disease (CKD)": 1.3,
        "Addison's Disease (Hypoadrenocorticism)": 1.3,
    },
    ("calcium", "low"): {
        "Eclampsia (Puerperal Hypocalcemia)": 2.0,
        "Hypoparathyroidism": 2.0,
        "Pancreatitis": 1.3,
        "Chronic Kidney Disease (CKD)": 1.3,
    },
    ("phosphorus", "high"): {
        "Chronic Kidney Disease (CKD)": 1.8,
        "Acute Kidney Injury": 1.5, "Acute Renal Failure": 1.5,
        "Hypoparathyroidism": 1.5,
    },

    # --- CBC (血球) --- [1] Nelson & Couto Ch.80–83
    ("wbc", "high"): {
        "Pyometra": 1.5,
        "Pneumonia": 1.3,
        "Abscess": 1.3,
        "Sepsis": 1.3,
        "Leukemia": 1.8,
    },
    ("wbc", "low"): {
        "Canine Parvovirus": 2.0,
        "Feline Panleukopenia": 2.0,
        "Sepsis": 1.5,
        "Ehrlichiosis": 1.5,
        "Bone Marrow Disease": 1.8,
    },
    ("rbc", "low"): {  # 貧血
        "Immune-Mediated Hemolytic Anemia (IMHA)": 2.0,
        "Chronic Kidney Disease (CKD)": 1.5,
        "Iron Deficiency Anemia": 1.8,
        "Feline Infectious Anemia (Hemoplasma)": 1.8,
        "Babesiosis": 1.5,
        "Internal Bleeding": 1.8,
    },
    ("pcv", "low"): {  # PCV/HCT
        "Immune-Mediated Hemolytic Anemia (IMHA)": 2.0,
        "Iron Deficiency Anemia": 1.8,
        "Chronic Kidney Disease (CKD)": 1.5,
        "Internal Bleeding": 1.8,
    },
    ("pcv", "high"): {  # 多血症
        "Dehydration": 1.5,
        "Polycythemia Vera": 2.0,
    },
    ("platelets", "low"): {
        "Immune-Mediated Thrombocytopenia (ITP)": 2.0,
        "Ehrlichiosis": 1.8,
        "Disseminated Intravascular Coagulation (DIC)": 1.8,
        "Babesiosis": 1.5,
        "Bone Marrow Disease": 1.5,
    },
    ("reticulocytes", "high"): {
        "Immune-Mediated Hemolytic Anemia (IMHA)": 1.8,
        "Iron Deficiency Anemia": 1.5,
        "Internal Bleeding": 1.5,
    },

    # --- 内分泌 --- [28] Feldman (2015)
    ("t4", "high"): {
        "Hyperthyroidism": 2.0,
    },
    ("t4", "low"): {
        "Hypothyroidism": 2.0,
    },
    ("tsh", "high"): {
        "Hypothyroidism": 2.0,
    },
    ("cortisol_post_acth", "high"): {
        "Cushing's Disease (Hyperadrenocorticism)": 2.0,
    },
    ("cortisol_post_acth", "low"): {
        "Addison's Disease (Hypoadrenocorticism)": 2.0,
    },
    ("cortisol_baseline", "low"): {
        "Addison's Disease (Hypoadrenocorticism)": 1.8,
    },

    # --- 尿検査 --- [2] Ettinger Ch.312
    ("usg", "low"): {  # 尿比重低下 (< 1.030 犬, < 1.035 猫)
        "Chronic Kidney Disease (CKD)": 1.8,
        "Diabetes Insipidus": 1.8,
        "Cushing's Disease (Hyperadrenocorticism)": 1.5,
        "Hyperthyroidism": 1.3,
    },
    ("upc", "high"): {  # 尿タンパク/クレアチニン比
        "Protein-Losing Nephropathy (PLN)": 2.0,
        "Glomerulonephritis": 2.0,
        "Chronic Kidney Disease (CKD)": 1.5,
    },

    # --- 炎症マーカー ---
    ("crp", "high"): {  # C-reactive protein
        "Pancreatitis": 1.5,
        "Immune-Mediated Polyarthritis": 1.5,
        "Pneumonia": 1.3,
        "Pyometra": 1.3,
        "Sepsis": 1.5,
    },

    # --- 凝固 ---
    ("pt", "high"): {  # プロトロンビン時間延長
        "Rodenticide Poisoning": 2.0,
        "Disseminated Intravascular Coagulation (DIC)": 1.8,
        "Hepatic Failure": 1.5,
    },
    ("aptt", "high"): {  # APTT延長
        "Rodenticide Poisoning": 2.0,
        "Hemophilia": 2.0,
        "Disseminated Intravascular Coagulation (DIC)": 1.8,
    },
}

# 検査項目の表示名 (日英)
LAB_ITEM_NAMES: Dict[str, Dict[str, str]] = {
    "bun": {"en": "BUN (Blood Urea Nitrogen)", "ja": "BUN (血中尿素窒素)"},
    "creatinine": {"en": "Creatinine", "ja": "クレアチニン"},
    "sdma": {"en": "SDMA", "ja": "SDMA"},
    "alt": {"en": "ALT (GPT)", "ja": "ALT (GPT)"},
    "alp": {"en": "ALP", "ja": "ALP"},
    "ggt": {"en": "GGT", "ja": "GGT"},
    "tbil": {"en": "Total Bilirubin", "ja": "総ビリルビン"},
    "albumin": {"en": "Albumin", "ja": "アルブミン"},
    "bile_acids": {"en": "Bile Acids", "ja": "胆汁酸"},
    "ammonia": {"en": "Ammonia", "ja": "アンモニア"},
    "lipase": {"en": "Lipase", "ja": "リパーゼ"},
    "amylase": {"en": "Amylase", "ja": "アミラーゼ"},
    "spec_cpl": {"en": "Spec cPL/fPL", "ja": "Spec cPL/fPL"},
    "glucose": {"en": "Glucose", "ja": "血糖値"},
    "fructosamine": {"en": "Fructosamine", "ja": "フルクトサミン"},
    "potassium": {"en": "Potassium (K)", "ja": "カリウム (K)"},
    "sodium": {"en": "Sodium (Na)", "ja": "ナトリウム (Na)"},
    "calcium": {"en": "Calcium (Ca)", "ja": "カルシウム (Ca)"},
    "phosphorus": {"en": "Phosphorus (P)", "ja": "リン (P)"},
    "wbc": {"en": "WBC", "ja": "白血球数"},
    "rbc": {"en": "RBC", "ja": "赤血球数"},
    "pcv": {"en": "PCV/HCT", "ja": "ヘマトクリット"},
    "platelets": {"en": "Platelets", "ja": "血小板数"},
    "reticulocytes": {"en": "Reticulocytes", "ja": "網状赤血球"},
    "t4": {"en": "T4 (Thyroxine)", "ja": "T4 (サイロキシン)"},
    "tsh": {"en": "TSH", "ja": "TSH"},
    "cortisol_post_acth": {"en": "Cortisol (post-ACTH)", "ja": "コルチゾール (ACTH後)"},
    "cortisol_baseline": {"en": "Cortisol (Baseline)", "ja": "コルチゾール (基礎値)"},
    "usg": {"en": "USG (Urine Specific Gravity)", "ja": "尿比重"},
    "upc": {"en": "UPC (Urine Protein/Creatinine)", "ja": "尿蛋白/クレアチニン比"},
    "crp": {"en": "CRP", "ja": "CRP (C反応性蛋白)"},
    "pt": {"en": "PT (Prothrombin Time)", "ja": "PT (プロトロンビン時間)"},
    "aptt": {"en": "APTT", "ja": "APTT"},
}

# 検査項目の基準値範囲 (犬・猫共通の代表値; 種別の精密な基準値は将来拡張)
# "low_threshold" 未満 → "low", "high_threshold" 超 → "high"
LAB_REFERENCE_RANGES: Dict[str, Dict[str, float]] = {
    "bun":        {"low_threshold": 7,    "high_threshold": 27},    # mg/dL
    "creatinine": {"low_threshold": 0.5,  "high_threshold": 1.8},   # mg/dL
    "sdma":       {"low_threshold": 0,    "high_threshold": 14},     # µg/dL
    "alt":        {"low_threshold": 10,   "high_threshold": 125},    # U/L
    "alp":        {"low_threshold": 23,   "high_threshold": 212},    # U/L
    "ggt":        {"low_threshold": 0,    "high_threshold": 11},     # U/L
    "tbil":       {"low_threshold": 0,    "high_threshold": 0.5},    # mg/dL
    "albumin":    {"low_threshold": 2.3,  "high_threshold": 4.0},    # g/dL
    "bile_acids": {"low_threshold": 0,    "high_threshold": 25},     # µmol/L
    "ammonia":    {"low_threshold": 0,    "high_threshold": 98},     # µg/dL
    "lipase":     {"low_threshold": 10,   "high_threshold": 160},    # U/L
    "amylase":    {"low_threshold": 500,  "high_threshold": 1500},   # U/L
    "spec_cpl":   {"low_threshold": 0,    "high_threshold": 200},    # µg/L (Spec cPL)
    "glucose":    {"low_threshold": 74,   "high_threshold": 143},    # mg/dL
    "fructosamine": {"low_threshold": 190, "high_threshold": 340},   # µmol/L
    "potassium":  {"low_threshold": 3.5,  "high_threshold": 5.8},    # mEq/L
    "sodium":     {"low_threshold": 140,  "high_threshold": 155},    # mEq/L
    "calcium":    {"low_threshold": 7.9,  "high_threshold": 12.0},   # mg/dL
    "phosphorus": {"low_threshold": 2.5,  "high_threshold": 6.8},    # mg/dL
    "wbc":        {"low_threshold": 5.5,  "high_threshold": 16.9},   # ×10³/µL
    "rbc":        {"low_threshold": 5.5,  "high_threshold": 8.5},    # ×10⁶/µL
    "pcv":        {"low_threshold": 37,   "high_threshold": 55},     # %
    "platelets":  {"low_threshold": 175,  "high_threshold": 500},    # ×10³/µL
    "reticulocytes": {"low_threshold": 0, "high_threshold": 60},     # ×10³/µL
    "t4":         {"low_threshold": 1.0,  "high_threshold": 4.0},    # µg/dL
    "tsh":        {"low_threshold": 0.03, "high_threshold": 0.5},    # ng/mL
    "cortisol_post_acth": {"low_threshold": 6, "high_threshold": 18},  # µg/dL
    "cortisol_baseline":  {"low_threshold": 1, "high_threshold": 5},   # µg/dL
    "usg":        {"low_threshold": 1.030, "high_threshold": 99},    # no upper abnormal
    "upc":        {"low_threshold": 0,     "high_threshold": 0.5},   # ratio
    "crp":        {"low_threshold": 0,     "high_threshold": 10},    # mg/L
    "pt":         {"low_threshold": 0,     "high_threshold": 17},    # seconds
    "aptt":       {"low_threshold": 0,     "high_threshold": 25},    # seconds
}


def compute_lab_boosts(
    lab_values: Dict[str, float],
) -> Dict[str, float]:
    """検査値の異常パターンから疾患ブーストマッピングを計算する。

    Parameters
    ----------
    lab_values:
        {検査項目ID: 数値} の辞書。例: {"bun": 45, "creatinine": 3.2}

    Returns
    -------
    Dict[str, float]
        {疾患名: 最大ブースト倍率} の辞書。
        複数の検査値異常が同一疾患を指す場合は最大倍率を採用。
    """
    boosts: Dict[str, float] = {}
    abnormalities: list[str] = []

    for item, value in lab_values.items():
        ref = LAB_REFERENCE_RANGES.get(item)
        if ref is None:
            continue

        direction = None
        if value > ref["high_threshold"]:
            direction = "high"
        elif value < ref["low_threshold"]:
            direction = "low"

        if direction is None:
            continue

        # 異常値を記録
        arrow = "↑" if direction == "high" else "↓"
        name_info = LAB_ITEM_NAMES.get(item, {"ja": item, "en": item})
        abnormalities.append(f"{name_info['ja']}{arrow} ({value})")

        # 疾患ブーストを適用
        key = (item, direction)
        disease_boosts = LAB_ABNORMALITY_DISEASE_MAP.get(key, {})
        for disease_name, multiplier in disease_boosts.items():
            if disease_name not in boosts or multiplier > boosts[disease_name]:
                boosts[disease_name] = multiplier

    return boosts


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


def _fuzzy_boost_lookup(
    disease_name: str,
    boost_dict: Dict[str, float],
) -> float:
    """疾患名の部分一致でブースト辞書を検索する。

    完全一致を優先し、見つからない場合はブースト辞書のキーが疾患名に含まれるか、
    またはその逆で一致するものを探す。括弧内の追加情報を除いた基本名でも照合する。
    """
    # 1. 完全一致
    if disease_name in boost_dict:
        return boost_dict[disease_name]

    # 2. 正規化名での照合
    disease_lower = disease_name.lower()
    base_name = disease_name.split("(")[0].strip().lower()
    best_multiplier = 1.0
    for boost_name, multiplier in boost_dict.items():
        boost_lower = boost_name.lower()
        boost_base = boost_name.split("(")[0].strip().lower()
        # 基本名の部分一致（どちらかが相手に含まれる）
        if (base_name and boost_base and
            (base_name in boost_base or boost_base in base_name)):
            if multiplier > best_multiplier:
                best_multiplier = multiplier
            continue
        # 全文部分一致（括弧内含む、例: "Brachycephalic" in "Saddle Nose (Brachycephalic ...)"）
        if boost_lower in disease_lower or disease_lower in boost_lower:
            if multiplier > best_multiplier:
                best_multiplier = multiplier
            continue
        # スラッシュ区切りの各部分で照合（例: "Tumors/Neoplasia" → ["tumors", "neoplasia"]）
        if "/" in boost_name:
            parts = [p.strip().lower() for p in boost_name.split("/")]
            if any(p in disease_lower for p in parts if len(p) > 3) and multiplier > best_multiplier:
                best_multiplier = multiplier
    return best_multiplier


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
    lab_values: Dict[str, float] | None = None,
    prevalence_map: Dict[str, str] | None = None,  # New: prevalence tier map
    gender: str | None = None,  # New: "male" | "female" | None
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

    # Look up gender risk data
    gender_risk: Dict[str, float] = {}
    gender_risk_applied = False
    if gender and species and GENDER_RISK_MULTIPLIERS:
        species_genders = GENDER_RISK_MULTIPLIERS.get(species, {})
        for disease_name, gender_mults in species_genders.items():
            if gender in gender_mults:
                mult = gender_mults[gender]
                gender_risk[disease_name] = mult
        if gender_risk:
            gender_risk_applied = True

    # Pre-compute symptom pair boosts for current symptom set
    # Combine original SYMPTOM_PAIR_BOOST with extended patterns
    pair_boosts: Dict[str, float] = {}
    all_pair_boosts = {**SYMPTOM_PAIR_BOOST, **EXTENDED_SYMPTOM_PAIR_BOOST}
    for pair, disease_boosts in all_pair_boosts.items():
        if pair.issubset(symptom_set):
            for disease_name, multiplier in disease_boosts.items():
                # Keep highest boost if multiple pairs match same disease
                if disease_name not in pair_boosts or multiplier > pair_boosts[disease_name]:
                    pair_boosts[disease_name] = multiplier

    # Pre-compute triple (3-symptom) boosts for current symptom set
    triple_boosts: Dict[str, float] = {}
    if len(symptom_set) >= 3 and SYMPTOM_TRIPLE_BOOST:
        for triple, disease_boosts in SYMPTOM_TRIPLE_BOOST.items():
            if triple.issubset(symptom_set):
                for disease_name, multiplier in disease_boosts.items():
                    # Keep highest boost if multiple triples match same disease
                    if disease_name not in triple_boosts or multiplier > triple_boosts[disease_name]:
                        triple_boosts[disease_name] = multiplier

    # Pre-compute lab value boosts
    lab_boosts: Dict[str, float] = {}
    if lab_values:
        lab_boosts = compute_lab_boosts(lab_values)

    for disease in diseases:
        disease_symptoms = set(disease.get("symptoms", set()))
        if not disease_symptoms:
            continue
        matching = symptom_set & disease_symptoms
        if not matching:
            continue

        match_count = len(matching)
        total_count = len(disease_symptoms)

        # Weighted coverage: 臨床的重要度で重み付けしたカバー率
        # 病態特異的な症状（seizures=2.5, jaundice=2.5 等）が一致すると
        # 非特異的な症状（lethargy=1.0）より大きくスコアに寄与する
        matching_weight = sum(
            SYMPTOM_CLINICAL_WEIGHTS.get(s, _DEFAULT_SYMPTOM_WEIGHT) for s in matching
        )
        total_weight = sum(
            SYMPTOM_CLINICAL_WEIGHTS.get(s, _DEFAULT_SYMPTOM_WEIGHT) for s in disease_symptoms
        )
        coverage = matching_weight / total_weight

        # 症状数による補正: 疾患の定義症状が少ない場合、カバー率が過大に
        # なるためペナルティを適用。定義症状が多い疾患は特異性が高いため
        # ボーナスを付与する。
        if total_count <= 2:
            symptom_count_factor = 0.75
        elif total_count <= 4:
            symptom_count_factor = 0.9
        elif total_count >= 8:
            symptom_count_factor = 1.1
        else:
            symptom_count_factor = 1.0

        # 一致症状が1つだけの場合はスコアを抑制（ノイズ除去）
        if match_count == 1:
            symptom_count_factor *= 0.6

        match_percent = round(coverage * symptom_count_factor * 100)

        # Apply onset multiplier (緩和: ペナルティを軽減)
        onset_multiplier = 1.0
        if onset:
            disease_onsets = disease.get("onset_pattern")
            if disease_onsets:
                onset_multiplier = 1.15 if onset in disease_onsets else 0.85

        # Apply age multiplier (緩和: ペナルティを軽減)
        age_multiplier = 1.0
        if age_stage:
            age_predisposition = disease.get("age_predisposition")
            if age_predisposition:
                age_multiplier = 1.15 if age_stage in age_predisposition else 0.85

        # Apply breed risk multiplier (上限を制限、部分一致)
        breed_multiplier = min(_fuzzy_boost_lookup(disease["name"], breed_risk), 1.8)

        # Apply gender risk multiplier (上限を制限、部分一致)
        gender_multiplier = min(_fuzzy_boost_lookup(disease["name"], gender_risk), 1.8)
        # If gender multiplier is 0, disease doesn't apply to this gender
        if gender_multiplier == 0.0:
            continue  # Skip this disease entirely

        # Apply symptom pair boost (上限を制限、部分一致)
        pair_multiplier = min(_fuzzy_boost_lookup(disease["name"], pair_boosts), 1.5)

        # Apply symptom triple boost (上限を制限、部分一致)
        triple_multiplier = min(_fuzzy_boost_lookup(disease["name"], triple_boosts), 2.0)

        # Apply lab value boost (上限を制限、部分一致)
        lab_multiplier = min(_fuzzy_boost_lookup(disease["name"], lab_boosts), 1.5)

        # 複合ブースト倍率の上限を設定（過度なインフレ防止）
        combined_boost = onset_multiplier * age_multiplier * breed_multiplier * gender_multiplier * pair_multiplier * triple_multiplier * lab_multiplier
        combined_boost = min(combined_boost, 3.0)  # 最大3.0倍（トリプルで強いブースト可能）
        if combined_boost < 1.0:
            # ペナルティの下限: 0.6（40%以上は削らない）
            combined_boost = max(combined_boost, 0.6)

        # Adjusted match percent
        adjusted_percent = min(round(match_percent * combined_boost), 100)

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
        # Get prevalence tier if prevalence_map provided
        prevalence_tier = "unknown"
        if prevalence_map:
            disease_name = disease.get("name", "")
            prevalence_tier = prevalence_map.get(disease_name, "unknown")

        suspected.append({
            "name": disease["name"],
            "name_ja": disease["name_ja"],
            "likelihood": likelihood,
            "match_percent": adjusted_percent,
            "color_class": color_class,
            "prevalence_tier": prevalence_tier,  # New: prevalence classification
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

    # Sort results: Prevalence tier first (if available), then match_percent, then match_count
    # This creates a stepwise differential diagnosis aligned with clinical practice
    prevalence_priority = {"very_common": 0, "common": 1, "uncommon": 2, "rare": 3, "unknown": 4}
    suspected.sort(
        key=lambda d: (
            prevalence_priority.get(d.get("prevalence_tier", "unknown"), 5),  # Primary: prevalence (ascending)
            -d["match_percent"],                                              # Secondary: match_percent (descending)
            -d["match_count"]                                                 # Tertiary: match_count (descending)
        )
    )

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

    # Group diseases by prevalence tier for stepwise presentation (if prevalence_map provided)
    phase1_diseases = [d for d in suspected if d.get("prevalence_tier") in ("very_common", "common")]
    phase2_diseases = [d for d in suspected if d.get("prevalence_tier") in ("uncommon", "rare", "unknown")]

    return {
        "suspected_diseases": suspected,
        "suspected_diseases_by_phase": {  # New: grouped for stepwise presentation
            "phase_1_common": phase1_diseases,
            "phase_2_rare": phase2_diseases,
        },
        "recommended_tests": recommended_tests,
        "severity": severity,
        "general_advice": advice_pair["en"],
        "general_advice_ja": advice_pair["ja"],
        "breed_genetic_tests": [],
        "breed_risk_applied": breed_risk_applied,
        "breed": breed,
        "gender_risk_applied": gender_risk_applied,
        "gender": gender,
        "onset_applied": onset is not None,
        "onset": onset,
        "age_applied": age_years is not None,
        "age_years": age_years,
        "age_stage": age_stage,
        "pair_boost_applied": len(pair_boosts) > 0,
        "lab_boost_applied": len(lab_boosts) > 0,
        "lab_values": lab_values,
        "symptom_names": symptom_names_lookup,
    }
