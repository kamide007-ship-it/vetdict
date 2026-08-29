"""drug_dictionary.py - 獣医薬品辞書モジュール

動物種別の薬品安全性情報・投与量データベースを提供します。
カテゴリ別・動物種別に検索・フィルタリングが可能です。

参考文献:
- Plumb's Veterinary Drug Handbook, 9th ed.
- BSAVA Small Animal Formulary
- Carpenter's Exotic Animal Formulary
"""

from __future__ import annotations

import json
import os
import re
import unicodedata
from typing import Any, Dict, List, Optional

from flask import Blueprint, jsonify, request

from api.drug_batch_1 import DRUGS_BATCH_1
from api.drug_batch_2 import DRUGS_BATCH_2
from api.drug_batch_3 import SPECIES_INFO_PATCH
from api.drug_batch_4 import FISH_DRUGS, FISH_SPECIES_INFO_PATCH
from api.drug_batch_5 import DRUGS_BATCH_5, SPECIES_INFO_PATCH_5
from api.drug_batch_6 import DRUG_INTERACTIONS_PATCH_6, DRUGS_BATCH_6, SPECIES_INFO_PATCH_6
from api.drug_batch_7 import CHINCHILLA_SPECIES_PATCH
from api.drug_batch_8 import DRUGS_BATCH_8
from api.drug_batch_9 import DRUGS_BATCH_9, ISCAID_UTI_NOTES_PATCH
from api.drug_batch_10 import DRUGS_BATCH_10
from api.drug_batch_11 import DRUGS_BATCH_11
from api.drug_batch_12 import DRUGS_BATCH_12
from api.drug_batch_13 import DRUGS_BATCH_13
from api.drug_batch_14 import DRUGS_BATCH_14
from api.drug_batch_15 import DRUGS_BATCH_15
from api.drug_batch_16 import DRUGS_BATCH_16
from api.drug_batch_17 import DRUGS_BATCH_17
from api.drug_batch_18 import DRUGS_BATCH_18
from api.drug_batch_19 import DRUGS_BATCH_19
from api.drug_batch_20 import DRUGS_BATCH_20
from api.drug_batch_21 import DRUGS_BATCH_21
from api.drug_batch_22 import DRUGS_BATCH_22
from api.drug_batch_23 import DRUGS_BATCH_23
from api.drug_batch_24 import DRUGS_BATCH_24
from api.drug_batch_25 import DRUG_INTERACTIONS_PATCH_25
from api.drug_batch_26 import DRUG_INTERACTIONS_PATCH_26
from api.drug_batch_27 import DRUG_INTERACTIONS_PATCH_27, DRUG_INTERACTIONS_PATCH_27B
from api.drug_batch_28 import SPECIES_INFO_PATCH_28
from api.drug_batch_29 import SPECIES_INFO_PATCH_29
from api.drug_batch_30 import (
    DRUGS_BATCH_30,
    METOCLOPRAMIDE_DOG_LACTATION_NOTE,
    METOCLOPRAMIDE_DOG_LACTATION_NOTE_EN,
    METOCLOPRAMIDE_LACTATION_PATCH_30,
)
from api.drug_batch_31 import DRUGS_BATCH_31
from api.drug_batch_32 import DRUGS_BATCH_32
from api.drug_batch_33 import DRUGS_BATCH_33
from api.drug_batch_34 import DRUGS_BATCH_34
from api.drug_batch_35 import DRUGS_BATCH_35
from api.drug_batch_36 import DRUGS_BATCH_36
from api.drug_batch_37 import DRUGS_BATCH_37
from api.drug_batch_38 import DRUGS_BATCH_38
from api.drug_batch_39 import DRUGS_BATCH_39
from api.drug_batch_40 import DRUGS_BATCH_40
from api.drug_batch_41 import DRUGS_BATCH_41
from api.drug_batch_42 import DRUGS_BATCH_42
from api.drug_batch_43 import DRUGS_BATCH_43
from api.drug_batch_44 import DRUGS_BATCH_44
from api.drug_batch_45 import DRUGS_BATCH_45
from api.drug_batch_46 import DRUGS_BATCH_46
from api.drug_batch_47 import DRUGS_BATCH_47
from api.drug_brand_names import BRAND_NAME_ALIASES

drug_bp = Blueprint("drug_dictionary", __name__)

# ---------------------------------------------------------------------------
# 薬品カテゴリ定義
# ---------------------------------------------------------------------------
DRUG_CATEGORIES: Dict[str, Dict[str, str]] = {
    "antibiotics": {"ja": "抗菌薬・抗生物質", "en": "Antibiotics"},
    "antifungals": {"ja": "抗真菌薬", "en": "Antifungals"},
    "antiparasitics": {"ja": "駆虫薬・抗寄生虫薬", "en": "Antiparasitics"},
    "nsaids": {"ja": "非ステロイド性抗炎症薬", "en": "NSAIDs"},
    "analgesics": {"ja": "鎮痛薬", "en": "Analgesics"},
    "anesthetics": {"ja": "麻酔薬", "en": "Anesthetics"},
    "corticosteroids": {"ja": "副腎皮質ステロイド", "en": "Corticosteroids"},
    "gi_drugs": {"ja": "消化器薬", "en": "Gastrointestinal Drugs"},
    "cardiovascular": {"ja": "循環器薬", "en": "Cardiovascular Drugs"},
    "respiratory": {"ja": "呼吸器薬", "en": "Respiratory Drugs"},
    "endocrine": {"ja": "内分泌薬", "en": "Endocrine Drugs"},
    "dermatological": {"ja": "皮膚科薬", "en": "Dermatological Drugs"},
    "ophthalmic": {"ja": "眼科薬", "en": "Ophthalmic Drugs"},
    "neurological": {"ja": "神経薬", "en": "Neurological Drugs"},
    "urinary": {"ja": "泌尿器薬", "en": "Urinary Drugs"},
    "immunosuppressives": {"ja": "免疫抑制薬", "en": "Immunosuppressives"},
    "immunosuppressive": {"ja": "免疫抑制薬", "en": "Immunosuppressives"},
    "biologics": {"ja": "生物学的製剤", "en": "Biologics / Monoclonal Antibodies"},
    "antivirals": {"ja": "抗ウイルス薬", "en": "Antivirals"},
    "antineoplastics": {"ja": "抗腫瘍薬", "en": "Antineoplastics"},
    "supplements": {"ja": "ビタミン・サプリメント", "en": "Vitamins & Supplements"},
    "sedatives": {"ja": "鎮静薬", "en": "Sedatives"},
    "antiemetics": {"ja": "制吐薬", "en": "Antiemetics"},
    "antidiarrheals": {"ja": "止瀉薬", "en": "Antidiarrheals"},
    "hepatoprotectants": {"ja": "肝臓保護薬", "en": "Hepatoprotectants"},
    "antihistamines": {"ja": "抗ヒスタミン薬", "en": "Antihistamines"},
    "bronchodilators": {"ja": "気管支拡張薬", "en": "Bronchodilators"},
    "diuretics": {"ja": "利尿薬", "en": "Diuretics"},
    "ace_inhibitors": {"ja": "ACE阻害薬", "en": "ACE Inhibitors"},
    "antiarrhythmics": {"ja": "抗不整脈薬", "en": "Antiarrhythmics"},
    "muscle_relaxants": {"ja": "筋弛緩薬", "en": "Muscle Relaxants"},
    "hormones": {"ja": "ホルモン薬", "en": "Hormones"},
    "antiseptics": {"ja": "消毒薬", "en": "Antiseptics"},
    "lactation_support": {"ja": "乳汁分泌促進薬", "en": "Lactation Support Agents"},
    "reproductive_hormones": {"ja": "生殖ホルモン", "en": "Reproductive Hormones"},
    "analgesics_lactation": {"ja": "鎮痛・乳汁分泌促進薬", "en": "Analgesics (Lactation Use)"},
    "anticoagulants": {"ja": "抗凝固薬", "en": "Anticoagulants"},
    "vitamins_minerals": {"ja": "ビタミン・ミネラル", "en": "Vitamins & Minerals"},
    "behavioral": {"ja": "行動薬・向精神薬", "en": "Behavioral / Psychotropic Drugs"},
    "antineoplastic": {"ja": "抗腫瘍薬", "en": "Antineoplastic Agents"},
    "antiparasitic": {"ja": "駆虫薬・抗寄生虫薬", "en": "Antiparasitic Agents"},
    "dermatology": {"ja": "皮膚科薬", "en": "Dermatology"},
    "gastrointestinal": {"ja": "消化器薬", "en": "Gastrointestinal"},
    "hepatic": {"ja": "肝臓保護薬", "en": "Hepatoprotective Agents"},
    "musculoskeletal": {"ja": "筋骨格薬", "en": "Musculoskeletal Drugs"},
    "ophthalmology": {"ja": "眼科薬", "en": "Ophthalmology"},
    "reproductive": {"ja": "生殖薬", "en": "Reproductive Drugs"},
    "analgesic": {"ja": "鎮痛薬", "en": "Analgesics"},
    "miscellaneous": {"ja": "その他", "en": "Miscellaneous"},
}


# ---------------------------------------------------------------------------
# 薬品データベース
# ---------------------------------------------------------------------------
DRUGS: List[Dict[str, Any]] = [
    # ══════════════════════════════════════════════════════════════════════
    # 抗菌薬・抗生物質 (Antibiotics)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": "amoxicillin",
        "name": "Amoxicillin",
        "name_ja": "アモキシシリン",
        "category": "antibiotics",
        "mechanism": "Beta-lactam antibiotic; inhibits bacterial cell wall synthesis by binding to penicillin-binding proteins.",
        "mechanism_ja": "β-ラクタム系抗生物質。ペニシリン結合蛋白に結合し細菌の細胞壁合成を阻害する。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "10-20 mg/kg PO q8-12h",
                "dosage_ja": "10-20 mg/kg 経口 8-12時間毎",
                "notes": "Well tolerated; common first-line antibiotic",
                "notes_ja": "忍容性良好、第一選択薬として広く使用",
            },
            "cat": {
                "safe": True,
                "dosage": "10-20 mg/kg PO q8-12h",
                "dosage_ja": "10-20 mg/kg 経口 8-12時間毎",
                "notes": "Generally well tolerated",
                "notes_ja": "一般的に忍容性良好",
            },
            "horse": {
                "safe": True,
                "dosage": "20-30 mg/kg PO q6-8h",
                "dosage_ja": "20-30 mg/kg 経口 6-8時間毎",
                "notes": "Poor oral bioavailability in adult horses; IV/IM preferred",
                "notes_ja": "成馬では経口バイオアベイラビリティが低い。静脈/筋注推奨",
            },
            "rabbit": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "CONTRAINDICATED orally - causes fatal dysbiosis and enterotoxemia",
                "notes_ja": "【禁忌】経口投与不可 - 致死的な腸内細菌叢異常・エンテロトキセミアを引き起こす",
            },
            "hamster": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "CONTRAINDICATED - causes fatal antibiotic-associated enteritis",
                "notes_ja": "【禁忌】致死的な抗生物質関連腸炎を引き起こす",
            },
            "guinea_pig": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "CONTRAINDICATED orally - causes fatal dysbiosis",
                "notes_ja": "【禁忌】経口投与不可 - 致死的な腸内細菌叢異常",
            },
            "chinchilla": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "CONTRAINDICATED orally - causes fatal dysbiosis",
                "notes_ja": "【禁忌】経口投与不可 - 致死的な腸内細菌叢異常",
            },
            "ferret": {
                "safe": True,
                "dosage": "20 mg/kg PO q8-12h",
                "dosage_ja": "20 mg/kg 経口 8-12時間毎",
                "notes": "Well tolerated",
                "notes_ja": "忍容性良好",
            },
            "bird": {
                "safe": True,
                "dosage": "150 mg/kg PO q8-12h",
                "dosage_ja": "150 mg/kg 経口 8-12時間毎",
                "notes": "Higher doses needed due to rapid metabolism",
                "notes_ja": "代謝が速いため高用量が必要",
            },
            "reptile": {
                "safe": True,
                "dosage": "22 mg/kg PO q12-24h",
                "dosage_ja": "22 mg/kg 経口 12-24時間毎",
                "notes": "Temperature-dependent metabolism; adjust with ambient temp",
                "notes_ja": "温度依存性代謝。環境温度で調整",
            },
        },
        "side_effects": ["GI upset", "diarrhea", "allergic reactions", "rash"],
        "side_effects_ja": ["消化器症状", "下痢", "アレルギー反応", "発疹"],
        "contraindications": "Hypersensitivity to penicillins. CONTRAINDICATED in rabbits, guinea pigs, hamsters, chinchillas (oral).",
        "contraindications_ja": "ペニシリン過敏症。ウサギ・モルモット・ハムスター・チンチラへの経口投与は禁忌。",
    },
    {
        "id": "amoxicillin_clavulanate",
        "name": "Amoxicillin-Clavulanate",
        "name_ja": "アモキシシリン・クラブラン酸",
        "category": "antibiotics",
        "mechanism": "Amoxicillin with beta-lactamase inhibitor; broadens spectrum against beta-lactamase producing bacteria.",
        "mechanism_ja": "アモキシシリンとβ-ラクタマーゼ阻害剤の合剤。β-ラクタマーゼ産生菌にも有効。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "12.5-25 mg/kg PO q8-12h",
                "dosage_ja": "12.5-25 mg/kg 経口 8-12時間毎",
                "notes": "Excellent broad-spectrum; first-line for many infections",
                "notes_ja": "優れた広域スペクトル。多くの感染症の第一選択薬",
            },
            "cat": {
                "safe": True,
                "dosage": "12.5-25 mg/kg PO q12h",
                "dosage_ja": "12.5-25 mg/kg 経口 12時間毎",
                "notes": "Common first-line antibiotic for cats",
                "notes_ja": "猫の第一選択抗生物質として一般的",
            },
            "horse": {
                "safe": True,
                "dosage": "Not commonly used orally; 10 mg/kg IV q6-8h (amoxicillin component)",
                "dosage_ja": "経口は一般的でない。静注 10 mg/kg 6-8時間毎（アモキシシリン成分）",
                "notes": "Limited oral use",
                "notes_ja": "経口使用は限定的",
            },
            "rabbit": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "CONTRAINDICATED orally - same risks as amoxicillin",
                "notes_ja": "【禁忌】経口投与不可 - アモキシシリンと同様のリスク",
            },
            "guinea_pig": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "CONTRAINDICATED orally",
                "notes_ja": "【禁忌】経口投与不可",
            },
            "ferret": {
                "safe": True,
                "dosage": "12.5-25 mg/kg PO q12h",
                "dosage_ja": "12.5-25 mg/kg 経口 12時間毎",
                "notes": "Well tolerated",
                "notes_ja": "忍容性良好",
            },
        },
        "side_effects": ["GI upset", "diarrhea", "vomiting"],
        "side_effects_ja": ["消化器症状", "下痢", "嘔吐"],
        "contraindications": "Same as amoxicillin. Not for use in hindgut fermenters.",
        "contraindications_ja": "アモキシシリンと同様。後腸発酵動物には使用不可。",
    },
    {
        "id": "enrofloxacin",
        "name": "Enrofloxacin",
        "name_ja": "エンロフロキサシン",
        "category": "antibiotics",
        "mechanism": "Fluoroquinolone; inhibits bacterial DNA gyrase and topoisomerase IV, preventing DNA replication.",
        "mechanism_ja": "フルオロキノロン系。細菌のDNAジャイレースとトポイソメラーゼIVを阻害しDNA複製を妨げる。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "5-20 mg/kg PO/IV q24h",
                "dosage_ja": "5-20 mg/kg 経口/静注 24時間毎",
                "notes": "Avoid in growing puppies (cartilage damage). Concentration-dependent killing.",
                "notes_ja": "成長期の子犬には使用回避（軟骨障害）。濃度依存性殺菌作用。",
            },
            "cat": {
                "safe": True,
                "dosage": "5 mg/kg PO/IV q24h (max)",
                "dosage_ja": "5 mg/kg 経口/静注 24時間毎（最大）",
                "notes": "DO NOT exceed 5 mg/kg/day - retinal toxicity risk. Can cause blindness.",
                "notes_ja": "【重要】5 mg/kg/日を超えないこと - 網膜毒性のリスク。失明の可能性あり。",
            },
            "horse": {
                "safe": True,
                "dosage": "5-7.5 mg/kg PO/IV q24h",
                "dosage_ja": "5-7.5 mg/kg 経口/静注 24時間毎",
                "notes": "Avoid in young growing horses",
                "notes_ja": "成長期の若馬には使用回避",
            },
            "rabbit": {
                "safe": True,
                "dosage": "5-20 mg/kg PO/SC/IM q12-24h",
                "dosage_ja": "5-20 mg/kg 経口/皮下/筋注 12-24時間毎",
                "notes": "One of the safest antibiotics for rabbits",
                "notes_ja": "ウサギに最も安全な抗生物質の一つ",
            },
            "guinea_pig": {
                "safe": True,
                "dosage": "5-10 mg/kg PO/SC q12h",
                "dosage_ja": "5-10 mg/kg 経口/皮下 12時間毎",
                "notes": "Safe and commonly used",
                "notes_ja": "安全で一般的に使用される",
            },
            "hamster": {
                "safe": True,
                "dosage": "5-10 mg/kg PO/SC q12h",
                "dosage_ja": "5-10 mg/kg 経口/皮下 12時間毎",
                "notes": "Good choice for hamsters",
                "notes_ja": "ハムスターに良い選択肢",
            },
            "chinchilla": {
                "safe": True,
                "dosage": "5-15 mg/kg PO/SC q12h",
                "dosage_ja": "5-15 mg/kg 経口/皮下 12時間毎",
                "notes": "Safe for chinchillas",
                "notes_ja": "チンチラに安全",
            },
            "ferret": {
                "safe": True,
                "dosage": "5-10 mg/kg PO/IM q12h",
                "dosage_ja": "5-10 mg/kg 経口/筋注 12時間毎",
                "notes": "Commonly used",
                "notes_ja": "一般的に使用",
            },
            "hedgehog": {
                "safe": True,
                "dosage": "5-10 mg/kg PO/SC q12h",
                "dosage_ja": "5-10 mg/kg 経口/皮下 12時間毎",
                "notes": "Safe for hedgehogs",
                "notes_ja": "ハリネズミに安全",
            },
            "bird": {
                "safe": True,
                "dosage": "15-30 mg/kg PO q12h; 10 mg/kg IM q12h",
                "dosage_ja": "15-30 mg/kg 経口 12時間毎; 10 mg/kg 筋注 12時間毎",
                "notes": "Widely used in avian medicine. May cause regurgitation.",
                "notes_ja": "鳥類医療で広く使用。嘔吐を起こすことがある。",
            },
            "reptile": {
                "safe": True,
                "dosage": "5-10 mg/kg PO/IM q24-48h",
                "dosage_ja": "5-10 mg/kg 経口/筋注 24-48時間毎",
                "notes": "Adjust interval based on temperature",
                "notes_ja": "温度により投与間隔を調整",
            },
        },
        "side_effects": [
            "GI upset",
            "retinal degeneration (cats)",
            "cartilage damage in young animals",
            "crystalluria",
        ],
        "side_effects_ja": ["消化器症状", "網膜変性（猫）", "若齢動物の軟骨障害", "結晶尿"],
        "contraindications": "Young growing animals. Cats: do not exceed 5 mg/kg/day.",
        "contraindications_ja": "成長期の若齢動物。猫: 5 mg/kg/日を超えないこと。",
    },
    {
        "id": "doxycycline",
        "name": "Doxycycline",
        "name_ja": "ドキシサイクリン",
        "category": "antibiotics",
        "mechanism": "Tetracycline antibiotic; inhibits protein synthesis by binding to 30S ribosomal subunit.",
        "mechanism_ja": "テトラサイクリン系抗生物質。30Sリボソームサブユニットに結合しタンパク質合成を阻害する。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "5-10 mg/kg PO q12-24h",
                "dosage_ja": "5-10 mg/kg 経口 12-24時間毎",
                "notes": "Give with food to reduce GI upset. Excellent for tick-borne diseases.",
                "notes_ja": "消化器症状軽減のため食事と共に投与。ダニ媒介性疾患に優れた効果。",
            },
            "cat": {
                "safe": True,
                "dosage": "5-10 mg/kg PO q12-24h",
                "dosage_ja": "5-10 mg/kg 経口 12-24時間毎",
                "notes": "Give with food or follow with water - risk of esophageal stricture in cats if tablet lodges.",
                "notes_ja": "食事と共に投与するか水で流す。錠剤が食道に留まると食道狭窄のリスク。",
            },
            "horse": {
                "safe": True,
                "dosage": "10 mg/kg PO q12h; 4 mg/kg IV q12h (slow)",
                "dosage_ja": "10 mg/kg 経口 12時間毎; 4 mg/kg 静注 12時間毎（緩徐に）",
                "notes": "IV must be given slowly and diluted to avoid cardiac arrest",
                "notes_ja": "静注は心停止を避けるため緩徐に希釈投与すること",
            },
            "rabbit": {
                "safe": True,
                "dosage": "2.5-5 mg/kg PO q12h",
                "dosage_ja": "2.5-5 mg/kg 経口 12時間毎",
                "notes": "Safest tetracycline for rabbits. Good for Pasteurella.",
                "notes_ja": "ウサギに最も安全なテトラサイクリン。パスツレラに有効。",
            },
            "guinea_pig": {
                "safe": True,
                "dosage": "2.5-5 mg/kg PO q12h",
                "dosage_ja": "2.5-5 mg/kg 経口 12時間毎",
                "notes": "Safe for guinea pigs",
                "notes_ja": "モルモットに安全",
            },
            "hamster": {
                "safe": True,
                "dosage": "2.5-5 mg/kg PO q12h",
                "dosage_ja": "2.5-5 mg/kg 経口 12時間毎",
                "notes": "Safe option",
                "notes_ja": "安全な選択肢",
            },
            "ferret": {
                "safe": True,
                "dosage": "5-10 mg/kg PO q12h",
                "dosage_ja": "5-10 mg/kg 経口 12時間毎",
                "notes": "Commonly used for Helicobacter, respiratory infections",
                "notes_ja": "ヘリコバクター・呼吸器感染症に一般的に使用",
            },
            "bird": {
                "safe": True,
                "dosage": "25-50 mg/kg PO q12-24h",
                "dosage_ja": "25-50 mg/kg 経口 12-24時間毎",
                "notes": "Drug of choice for chlamydiosis (psittacosis). Long treatment course needed (45 days).",
                "notes_ja": "クラミジア症（オウム病）の第一選択薬。長期投与が必要（45日間）。",
            },
            "reptile": {
                "safe": True,
                "dosage": "10 mg/kg PO q24h",
                "dosage_ja": "10 mg/kg 経口 24時間毎",
                "notes": "Useful for respiratory infections in reptiles",
                "notes_ja": "爬虫類の呼吸器感染症に有用",
            },
        },
        "side_effects": [
            "GI upset",
            "esophageal stricture (cats)",
            "photosensitivity",
            "tooth discoloration in young animals",
        ],
        "side_effects_ja": ["消化器症状", "食道狭窄（猫）", "光線過敏症", "若齢動物の歯の変色"],
        "contraindications": "Pregnancy (tooth/bone effects on fetus). Use caution in hepatic insufficiency.",
        "contraindications_ja": "妊娠中（胎児の歯・骨への影響）。肝不全では注意して使用。",
    },
    {
        "id": "metronidazole",
        "name": "Metronidazole",
        "name_ja": "メトロニダゾール",
        "category": "antibiotics",
        "mechanism": "Nitroimidazole; disrupts DNA synthesis in anaerobic bacteria and protozoa.",
        "mechanism_ja": "ニトロイミダゾール系。嫌気性菌とプロトゾアのDNA合成を阻害する。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "10-15 mg/kg PO q12h",
                "dosage_ja": "10-15 mg/kg 経口 12時間毎",
                "notes": "Neurotoxicity at high doses or prolonged use. Bitter taste.",
                "notes_ja": "高用量や長期投与で神経毒性。苦味がある。",
            },
            "cat": {
                "safe": True,
                "dosage": "10-15 mg/kg PO q24h (or 5-7.5 mg/kg q12h; max 7.5 mg/kg/dose)",
                "dosage_ja": "10-15 mg/kg 経口 24時間毎（または5-7.5 mg/kg 12時間毎。1回最大7.5 mg/kg）",
                "notes": "CATS SENSITIVE — max 7.5 mg/kg/dose. Neurotoxicity (ataxia, seizures) at higher doses or >5 days. Stop immediately if neurological signs appear.",
                "notes_ja": "【猫は神経毒性に敏感】1回7.5 mg/kgを超えないこと。高用量や5日以上の投与で運動失調・痙攣のリスク。神経症状が出たら直ちに中止。",
            },
            "horse": {
                "safe": True,
                "dosage": "15-25 mg/kg PO q6-8h",
                "dosage_ja": "15-25 mg/kg 経口 6-8時間毎",
                "notes": "Used for anaerobic infections, clostridial diseases",
                "notes_ja": "嫌気性感染症・クロストリジウム症に使用",
            },
            "rabbit": {
                "safe": True,
                "dosage": "20 mg/kg PO q12h",
                "dosage_ja": "20 mg/kg 経口 12時間毎",
                "notes": "Use with caution; monitor for GI disturbance",
                "notes_ja": "注意して使用。消化器症状を観察",
            },
            "guinea_pig": {
                "safe": True,
                "dosage": "20 mg/kg PO q12h",
                "dosage_ja": "20 mg/kg 経口 12時間毎",
                "notes": "Use with caution",
                "notes_ja": "注意して使用",
            },
            "ferret": {
                "safe": True,
                "dosage": "15-20 mg/kg PO q12h",
                "dosage_ja": "15-20 mg/kg 経口 12時間毎",
                "notes": "Commonly used for Helicobacter therapy (triple therapy)",
                "notes_ja": "ヘリコバクター治療（三剤併用療法）に一般的に使用",
            },
            "bird": {
                "safe": True,
                "dosage": "20-50 mg/kg PO q12-24h",
                "dosage_ja": "20-50 mg/kg 経口 12-24時間毎",
                "notes": "Used for trichomoniasis, anaerobic infections",
                "notes_ja": "トリコモナス症・嫌気性感染症に使用",
            },
            "reptile": {
                "safe": True,
                "dosage": "20 mg/kg PO q48h",
                "dosage_ja": "20 mg/kg 経口 48時間毎",
                "notes": "Extended interval due to slow reptile metabolism",
                "notes_ja": "爬虫類の代謝が遅いため投与間隔を延長",
            },
        },
        "side_effects": ["neurotoxicity (ataxia, seizures)", "anorexia", "hepatotoxicity", "neutropenia"],
        "side_effects_ja": ["神経毒性（運動失調・痙攣）", "食欲不振", "肝毒性", "好中球減少"],
        "contraindications": "Pregnancy. Known hypersensitivity. Hepatic disease (use with caution).",
        "contraindications_ja": "妊娠中。過敏症。肝疾患（注意して使用）。",
    },
    {
        "id": "cephalexin",
        "name": "Cephalexin",
        "name_ja": "セファレキシン",
        "category": "antibiotics",
        "mechanism": "First-generation cephalosporin; inhibits bacterial cell wall synthesis.",
        "mechanism_ja": "第一世代セファロスポリン。細菌の細胞壁合成を阻害する。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "22-30 mg/kg PO q8-12h",
                "dosage_ja": "22-30 mg/kg 経口 8-12時間毎",
                "notes": "Excellent for skin infections (pyoderma)",
                "notes_ja": "皮膚感染症（膿皮症）に優れた効果",
            },
            "cat": {
                "safe": True,
                "dosage": "15-30 mg/kg PO q8-12h",
                "dosage_ja": "15-30 mg/kg 経口 8-12時間毎",
                "notes": "Well tolerated",
                "notes_ja": "忍容性良好",
            },
            "horse": {
                "safe": True,
                "dosage": "30 mg/kg PO q8h",
                "dosage_ja": "30 mg/kg 経口 8時間毎",
                "notes": "Limited use due to poor oral absorption",
                "notes_ja": "経口吸収が不良のため使用は限定的",
            },
            "rabbit": {
                "safe": True,
                "dosage": "15-25 mg/kg PO q8-12h",
                "dosage_ja": "15-25 mg/kg 経口 8-12時間毎",
                "notes": "Relatively safe for rabbits among beta-lactams",
                "notes_ja": "β-ラクタム系の中ではウサギに比較的安全",
            },
            "ferret": {
                "safe": True,
                "dosage": "15-25 mg/kg PO q8-12h",
                "dosage_ja": "15-25 mg/kg 経口 8-12時間毎",
                "notes": "Well tolerated",
                "notes_ja": "忍容性良好",
            },
        },
        "side_effects": ["GI upset", "vomiting", "diarrhea", "allergic reactions"],
        "side_effects_ja": ["消化器症状", "嘔吐", "下痢", "アレルギー反応"],
        "contraindications": "Hypersensitivity to cephalosporins or penicillins (cross-reactivity).",
        "contraindications_ja": "セファロスポリンまたはペニシリン過敏症（交差反応性）。",
    },
    {
        "id": "marbofloxacin",
        "name": "Marbofloxacin",
        "name_ja": "マルボフロキサシン",
        "category": "antibiotics",
        "mechanism": "Fluoroquinolone; inhibits DNA gyrase and topoisomerase IV.",
        "mechanism_ja": "フルオロキノロン系。DNAジャイレースとトポイソメラーゼIVを阻害。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "2-5.5 mg/kg PO q24h",
                "dosage_ja": "2-5.5 mg/kg 経口 24時間毎",
                "notes": "Good tissue penetration",
                "notes_ja": "良好な組織移行性",
            },
            "cat": {
                "safe": True,
                "dosage": "2 mg/kg PO q24h",
                "dosage_ja": "2 mg/kg 経口 24時間毎",
                "notes": "Safer than enrofloxacin for cats (less retinal toxicity risk)",
                "notes_ja": "エンロフロキサシンより猫に安全（網膜毒性リスクが低い）",
            },
            "rabbit": {
                "safe": True,
                "dosage": "5 mg/kg PO q24h",
                "dosage_ja": "5 mg/kg 経口 24時間毎",
                "notes": "Safe for rabbits",
                "notes_ja": "ウサギに安全",
            },
        },
        "side_effects": ["GI upset", "cartilage damage in young animals"],
        "side_effects_ja": ["消化器症状", "若齢動物の軟骨障害"],
        "contraindications": "Young growing animals.",
        "contraindications_ja": "成長期の若齢動物。",
    },
    {
        "id": "pradofloxacin",
        "name": "Pradofloxacin",
        "name_ja": "プラドフロキサシン",
        "category": "antibiotics",
        "mechanism": "Third-generation fluoroquinolone; dual-target inhibition of DNA gyrase and topoisomerase IV.",
        "mechanism_ja": "第三世代フルオロキノロン系。DNAジャイレースとトポイソメラーゼIVの二重標的阻害。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "3-4.5 mg/kg PO q24h",
                "dosage_ja": "3-4.5 mg/kg 経口 24時間毎",
                "notes": "Broad spectrum including anaerobes",
                "notes_ja": "嫌気性菌を含む広域スペクトル",
            },
            "cat": {
                "safe": True,
                "dosage": "5-10 mg/kg PO q24h",
                "dosage_ja": "5-10 mg/kg 経口 24時間毎",
                "notes": "Licensed for cats; oral suspension available",
                "notes_ja": "猫に認可済み。経口懸濁液あり",
            },
        },
        "side_effects": ["GI upset", "soft stool"],
        "side_effects_ja": ["消化器症状", "軟便"],
        "contraindications": "Young growing animals. Pregnancy.",
        "contraindications_ja": "成長期の若齢動物。妊娠中。",
    },
    {
        "id": "clindamycin",
        "name": "Clindamycin",
        "name_ja": "クリンダマイシン",
        "category": "antibiotics",
        "mechanism": "Lincosamide antibiotic; inhibits protein synthesis at 50S ribosomal subunit.",
        "mechanism_ja": "リンコサミド系抗生物質。50Sリボソームサブユニットでタンパク質合成を阻害。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "5.5-11 mg/kg PO q12h",
                "dosage_ja": "5.5-11 mg/kg 経口 12時間毎",
                "notes": "Excellent bone penetration. Good for dental/osteomyelitis.",
                "notes_ja": "優れた骨組織移行性。歯科感染症・骨髄炎に有効。",
            },
            "cat": {
                "safe": True,
                "dosage": "5.5-11 mg/kg PO q12-24h",
                "dosage_ja": "5.5-11 mg/kg 経口 12-24時間毎",
                "notes": "Good for toxoplasmosis treatment",
                "notes_ja": "トキソプラズマ症治療に有効",
            },
            "rabbit": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "CONTRAINDICATED - causes fatal enterotoxemia",
                "notes_ja": "【禁忌】致死的なエンテロトキセミアを引き起こす",
            },
            "guinea_pig": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "CONTRAINDICATED - causes fatal dysbiosis",
                "notes_ja": "【禁忌】致死的な腸内細菌叢異常",
            },
            "hamster": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "CONTRAINDICATED",
                "notes_ja": "【禁忌】",
            },
            "ferret": {
                "safe": True,
                "dosage": "5.5-11 mg/kg PO q12h",
                "dosage_ja": "5.5-11 mg/kg 経口 12時間毎",
                "notes": "Well tolerated in ferrets",
                "notes_ja": "フェレットでは忍容性良好",
            },
        },
        "side_effects": ["GI upset", "esophageal stricture (cats)", "pseudomembranous colitis"],
        "side_effects_ja": ["消化器症状", "食道狭窄（猫）", "偽膜性大腸炎"],
        "contraindications": "Rabbits, guinea pigs, hamsters, chinchillas (oral). History of GI disease.",
        "contraindications_ja": "ウサギ・モルモット・ハムスター・チンチラ（経口）。消化器疾患の既往。",
    },
    {
        "id": "azithromycin",
        "name": "Azithromycin",
        "name_ja": "アジスロマイシン",
        "category": "antibiotics",
        "mechanism": "Macrolide antibiotic; inhibits protein synthesis at 50S ribosomal subunit. Long tissue half-life.",
        "mechanism_ja": "マクロライド系抗生物質。50Sリボソームサブユニットでタンパク質合成を阻害。組織半減期が長い。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "5-10 mg/kg PO q24h for 3-5 days, then q48h",
                "dosage_ja": "5-10 mg/kg 経口 24時間毎×3-5日、その後48時間毎",
                "notes": "Long half-life allows pulse dosing",
                "notes_ja": "半減期が長いためパルス投与が可能",
            },
            "cat": {
                "safe": True,
                "dosage": "5-10 mg/kg PO q24-48h",
                "dosage_ja": "5-10 mg/kg 経口 24-48時間毎",
                "notes": "Used for Bartonella, Mycoplasma, and upper respiratory infections",
                "notes_ja": "バルトネラ・マイコプラズマ・上部呼吸器感染症に使用",
            },
            "rabbit": {
                "safe": True,
                "dosage": "15-30 mg/kg PO q24h",
                "dosage_ja": "15-30 mg/kg 経口 24時間毎",
                "notes": "Safe for rabbits",
                "notes_ja": "ウサギに安全",
            },
            "guinea_pig": {
                "safe": True,
                "dosage": "15-30 mg/kg PO q24h",
                "dosage_ja": "15-30 mg/kg 経口 24時間毎",
                "notes": "Safe option",
                "notes_ja": "安全な選択肢",
            },
            "ferret": {
                "safe": True,
                "dosage": "5-10 mg/kg PO q24h",
                "dosage_ja": "5-10 mg/kg 経口 24時間毎",
                "notes": "Used for Helicobacter triple therapy",
                "notes_ja": "ヘリコバクター三剤併用療法に使用",
            },
            "bird": {
                "safe": True,
                "dosage": "40-50 mg/kg PO q24-48h",
                "dosage_ja": "40-50 mg/kg 経口 24-48時間毎",
                "notes": "Good for respiratory infections",
                "notes_ja": "呼吸器感染症に有効",
            },
        },
        "side_effects": ["GI upset", "diarrhea", "hepatotoxicity (rare)"],
        "side_effects_ja": ["消化器症状", "下痢", "肝毒性（まれ）"],
        "contraindications": "Hepatic disease. Known macrolide hypersensitivity.",
        "contraindications_ja": "肝疾患。マクロライド系過敏症。",
    },
    {
        "id": "trimethoprim_sulfa",
        "search_aliases": ["TMP-スルファ", "TMPスルファ", "TMP-S", "TMP/S", "TMS合剤"],
        "name": "Trimethoprim-Sulfamethoxazole",
        "name_ja": "トリメトプリム・スルファメトキサゾール",
        "category": "antibiotics",
        "mechanism": "Synergistic combination inhibiting sequential steps in folic acid synthesis.",
        "mechanism_ja": "葉酸合成の連続する段階を阻害する相乗的な合剤。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "15-30 mg/kg PO q12h",
                "dosage_ja": "15-30 mg/kg 経口 12時間毎",
                "notes": "Monitor for KCS (dry eye) with prolonged use",
                "notes_ja": "長期使用ではKCS（乾性角結膜炎）を監視",
            },
            "cat": {
                "safe": True,
                "dosage": "15-30 mg/kg PO q12h",
                "dosage_ja": "15-30 mg/kg 経口 12時間毎",
                "notes": "Anorexia and drooling may occur",
                "notes_ja": "食欲不振と流涎が起こることがある",
            },
            "horse": {
                "safe": True,
                "dosage": "24-30 mg/kg PO q12h",
                "dosage_ja": "24-30 mg/kg 経口 12時間毎",
                "notes": "Common first-line for many equine infections",
                "notes_ja": "多くの馬の感染症の第一選択薬",
            },
            "rabbit": {
                "safe": True,
                "dosage": "30 mg/kg PO q12h",
                "dosage_ja": "30 mg/kg 経口 12時間毎",
                "notes": "Good safety profile for rabbits",
                "notes_ja": "ウサギに良好な安全性プロファイル",
            },
            "guinea_pig": {
                "safe": True,
                "dosage": "30 mg/kg PO q12h",
                "dosage_ja": "30 mg/kg 経口 12時間毎",
                "notes": "Safe and effective",
                "notes_ja": "安全かつ有効",
            },
            "ferret": {
                "safe": True,
                "dosage": "15-30 mg/kg PO q12h",
                "dosage_ja": "15-30 mg/kg 経口 12時間毎",
                "notes": "Well tolerated",
                "notes_ja": "忍容性良好",
            },
            "bird": {
                "safe": True,
                "dosage": "30 mg/kg PO q12h",
                "dosage_ja": "30 mg/kg 経口 12時間毎",
                "notes": "Useful for various avian infections",
                "notes_ja": "鳥類の各種感染症に有用",
            },
        },
        "side_effects": ["KCS (dogs)", "bone marrow suppression", "hepatotoxicity", "hypersensitivity"],
        "side_effects_ja": ["KCS/乾性角結膜炎（犬）", "骨髄抑制", "肝毒性", "過敏症"],
        "contraindications": "Sulfonamide hypersensitivity. Hepatic/renal insufficiency. Avoid in Dobermans (idiosyncratic reactions).",
        "contraindications_ja": "スルホンアミド過敏症。肝・腎不全。ドーベルマンでは回避（特異体質性反応）。",
    },
    {
        "id": "chloramphenicol",
        "name": "Chloramphenicol",
        "name_ja": "クロラムフェニコール",
        "category": "antibiotics",
        "mechanism": "Broad-spectrum antibiotic; inhibits protein synthesis at 50S ribosomal subunit.",
        "mechanism_ja": "広域抗生物質。50Sリボソームサブユニットでタンパク質合成を阻害。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "40-50 mg/kg PO q8h",
                "dosage_ja": "40-50 mg/kg 経口 8時間毎",
                "notes": "Caution: can cause aplastic anemia in humans handling drug",
                "notes_ja": "注意：薬剤を取り扱うヒトに再生不良性貧血のリスク",
            },
            "cat": {
                "safe": True,
                "dosage": "25-50 mg/kg PO q12h",
                "dosage_ja": "25-50 mg/kg 経口 12時間毎",
                "notes": "Cats metabolize more slowly; use lower dose/longer interval",
                "notes_ja": "猫は代謝が遅い。低用量・長間隔で使用",
            },
            "horse": {
                "safe": True,
                "dosage": "50 mg/kg PO q6-8h",
                "dosage_ja": "50 mg/kg 経口 6-8時間毎",
                "notes": "Good CNS penetration",
                "notes_ja": "良好なCNS移行性",
            },
            "rabbit": {
                "safe": True,
                "dosage": "30-50 mg/kg PO q12h",
                "dosage_ja": "30-50 mg/kg 経口 12時間毎",
                "notes": "Safe for rabbits",
                "notes_ja": "ウサギに安全",
            },
            "bird": {
                "safe": True,
                "dosage": "50-80 mg/kg PO q6-8h",
                "dosage_ja": "50-80 mg/kg 経口 6-8時間毎",
                "notes": "Effective broad-spectrum option for birds",
                "notes_ja": "鳥類に有効な広域スペクトル選択肢",
            },
            "reptile": {
                "safe": True,
                "dosage": "20-50 mg/kg PO/SC q12-24h",
                "dosage_ja": "20-50 mg/kg 経口/皮下 12-24時間毎",
                "notes": "Temperature-dependent pharmacokinetics",
                "notes_ja": "温度依存性薬物動態",
            },
        },
        "side_effects": ["bone marrow suppression", "aplastic anemia (human handler risk)", "GI upset"],
        "side_effects_ja": ["骨髄抑制", "再生不良性貧血（ヒトの取扱者リスク）", "消化器症状"],
        "contraindications": "Bone marrow suppression. Neonates. Pregnant/nursing animals.",
        "contraindications_ja": "骨髄抑制。新生児。妊娠中・授乳中の動物。",
    },
    {
        "id": "gentamicin",
        "name": "Gentamicin",
        "name_ja": "ゲンタマイシン",
        "category": "antibiotics",
        "mechanism": "Aminoglycoside; inhibits protein synthesis by binding to 30S ribosomal subunit. Bactericidal.",
        "mechanism_ja": "アミノグリコシド系。30Sリボソームサブユニットに結合しタンパク質合成を阻害。殺菌的。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "6-8 mg/kg IV/IM/SC q24h",
                "dosage_ja": "6-8 mg/kg 静注/筋注/皮下 24時間毎",
                "notes": "Nephrotoxic and ototoxic. Monitor renal function. Once-daily dosing reduces toxicity.",
                "notes_ja": "腎毒性・聴覚毒性あり。腎機能を監視。1日1回投与で毒性軽減。",
            },
            "cat": {
                "safe": True,
                "dosage": "5-8 mg/kg IV/IM/SC q24h",
                "dosage_ja": "5-8 mg/kg 静注/筋注/皮下 24時間毎",
                "notes": "Same precautions as dogs",
                "notes_ja": "犬と同様の注意事項",
            },
            "horse": {
                "safe": True,
                "dosage": "6.6 mg/kg IV/IM q24h",
                "dosage_ja": "6.6 mg/kg 静注/筋注 24時間毎",
                "notes": "Nephrotoxic risk especially in dehydrated horses",
                "notes_ja": "特に脱水した馬では腎毒性のリスクが高い",
            },
            "rabbit": {
                "safe": True,
                "dosage": "5 mg/kg SC/IM q24h",
                "dosage_ja": "5 mg/kg 皮下/筋注 24時間毎",
                "notes": "Use parenteral only; not oral",
                "notes_ja": "非経口のみ使用。経口不可。",
            },
            "reptile": {
                "safe": True,
                "dosage": "2.5 mg/kg IM q72h",
                "dosage_ja": "2.5 mg/kg 筋注 72時間毎",
                "notes": "Inject in forelimb only (not hindlimb due to renal portal system)",
                "notes_ja": "前肢にのみ注射（腎門脈系のため後肢不可）",
            },
        },
        "side_effects": ["nephrotoxicity", "ototoxicity", "neuromuscular blockade"],
        "side_effects_ja": ["腎毒性", "聴覚毒性", "神経筋遮断"],
        "contraindications": "Renal insufficiency. Dehydration. Concurrent use of other nephrotoxic drugs.",
        "contraindications_ja": "腎不全。脱水。他の腎毒性薬剤との併用。",
    },
    {
        "id": "cefovecin",
        "name": "Cefovecin (Convenia)",
        "name_ja": "セフォベシン（コンベニア）",
        "category": "antibiotics",
        "mechanism": "Third-generation cephalosporin with ultra-long duration (14 days single injection).",
        "mechanism_ja": "第三世代セファロスポリン。単回注射で14日間持続する超長時間作用型。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "8 mg/kg SC single injection, repeat in 14 days",
                "dosage_ja": "8 mg/kg 皮下 単回注射、14日後に反復可",
                "notes": "Convenient but inflexible dosing; cannot be removed once injected",
                "notes_ja": "便利だが調整不可。注射後は除去できない。",
            },
            "cat": {
                "safe": True,
                "dosage": "8 mg/kg SC single injection, repeat in 14 days",
                "dosage_ja": "8 mg/kg 皮下 単回注射、14日後に反復可",
                "notes": "Useful for fractious cats or non-compliant owners",
                "notes_ja": "気性の荒い猫や投薬困難な飼い主に有用",
            },
            "rabbit": {
                "safe": True,
                "dosage": "8 mg/kg SC q14 days",
                "dosage_ja": "8 mg/kg 皮下 14日毎",
                "notes": "Used off-label; safe in rabbits",
                "notes_ja": "適応外使用。ウサギに安全。",
            },
        },
        "side_effects": ["injection site reactions", "GI upset", "allergic reactions"],
        "side_effects_ja": ["注射部位反応", "消化器症状", "アレルギー反応"],
        "contraindications": "Cephalosporin/penicillin hypersensitivity. Not recommended for serious infections requiring dose adjustment.",
        "contraindications_ja": "セファロスポリン/ペニシリン過敏症。用量調整が必要な重篤な感染症には非推奨。",
    },
    {
        "id": "tylosin",
        "name": "Tylosin",
        "name_ja": "タイロシン",
        "category": "antibiotics",
        "mechanism": "Macrolide antibiotic; inhibits protein synthesis. Also has anti-inflammatory properties in the gut.",
        "mechanism_ja": "マクロライド系抗生物質。タンパク質合成を阻害。腸管での抗炎症作用も持つ。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "10-40 mg/kg PO q12h",
                "dosage_ja": "10-40 mg/kg 経口 12時間毎",
                "notes": "Often used for chronic colitis and antibiotic-responsive diarrhea",
                "notes_ja": "慢性大腸炎・抗生物質反応性下痢に頻用",
            },
            "cat": {
                "safe": True,
                "dosage": "10-15 mg/kg PO q12h",
                "dosage_ja": "10-15 mg/kg 経口 12時間毎",
                "notes": "Used for chronic enteritis",
                "notes_ja": "慢性腸炎に使用",
            },
            "bird": {
                "safe": True,
                "dosage": "30 mg/kg PO q8-12h",
                "dosage_ja": "30 mg/kg 経口 8-12時間毎",
                "notes": "Used for Mycoplasma infections in poultry",
                "notes_ja": "家禽のマイコプラズマ感染症に使用",
            },
        },
        "side_effects": ["GI upset", "pain at injection site"],
        "side_effects_ja": ["消化器症状", "注射部位の痛み"],
        "contraindications": "Macrolide hypersensitivity.",
        "contraindications_ja": "マクロライド系過敏症。",
    },
    {
        "id": "florfenicol",
        "name": "Florfenicol",
        "name_ja": "フロルフェニコール",
        "category": "antibiotics",
        "mechanism": "Phenicol antibiotic; inhibits protein synthesis. Analog of chloramphenicol without aplastic anemia risk.",
        "mechanism_ja": "フェニコール系抗生物質。タンパク質合成を阻害。クロラムフェニコール類似体だが再生不良性貧血のリスクなし。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "20 mg/kg PO q8h",
                "dosage_ja": "20 mg/kg 経口 8時間毎",
                "notes": "Limited canine use",
                "notes_ja": "犬での使用は限定的",
            },
            "cat": {
                "safe": True,
                "dosage": "22 mg/kg PO/SC q12h",
                "dosage_ja": "22 mg/kg 経口/皮下 12時間毎",
                "notes": "Off-label use",
                "notes_ja": "適応外使用",
            },
            "horse": {
                "safe": True,
                "dosage": "22 mg/kg IM q48h",
                "dosage_ja": "22 mg/kg 筋注 48時間毎",
                "notes": "Long-acting formulation available",
                "notes_ja": "長時間作用型製剤あり",
            },
        },
        "side_effects": ["decreased appetite", "soft stool"],
        "side_effects_ja": ["食欲低下", "軟便"],
        "contraindications": "Breeding animals.",
        "contraindications_ja": "繁殖用動物。",
    },
    {
        "id": "penicillin_g",
        "name": "Penicillin G",
        "name_ja": "ペニシリンG",
        "category": "antibiotics",
        "mechanism": "Natural penicillin; inhibits cell wall synthesis. Narrow spectrum, mainly gram-positive.",
        "mechanism_ja": "天然ペニシリン。細胞壁合成を阻害。狭域スペクトル、主にグラム陽性菌に有効。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "22,000-40,000 IU/kg IM/SC q12-24h",
                "dosage_ja": "22,000-40,000 IU/kg 筋注/皮下 12-24時間毎",
                "notes": "Parenteral use; procaine penicillin for sustained release",
                "notes_ja": "非経口使用。プロカインペニシリンで持続放出。",
            },
            "cat": {
                "safe": True,
                "dosage": "22,000-40,000 IU/kg IM/SC q12-24h",
                "dosage_ja": "22,000-40,000 IU/kg 筋注/皮下 12-24時間毎",
                "notes": "Cats sensitive to procaine - use benzathine preparations with care",
                "notes_ja": "猫はプロカインに敏感。ベンザチン製剤は注意して使用。",
            },
            "horse": {
                "safe": True,
                "dosage": "22,000 IU/kg IM q12-24h (procaine penicillin)",
                "dosage_ja": "22,000 IU/kg 筋注 12-24時間毎（プロカインペニシリン）",
                "notes": "Mainstay equine antibiotic. Procaine reactions possible.",
                "notes_ja": "馬の主要抗生物質。プロカイン反応の可能性あり。",
            },
            "rabbit": {
                "safe": True,
                "dosage": "42,000-84,000 IU/kg SC q48h",
                "dosage_ja": "42,000-84,000 IU/kg 皮下 48時間毎",
                "notes": "PARENTERAL ONLY. Oral penicillin is lethal to rabbits.",
                "notes_ja": "【非経口のみ】経口ペニシリンはウサギに致死的。",
            },
        },
        "side_effects": ["injection site reactions", "allergic reactions", "anaphylaxis"],
        "side_effects_ja": ["注射部位反応", "アレルギー反応", "アナフィラキシー"],
        "contraindications": "Penicillin hypersensitivity. Oral use in rabbits and rodents.",
        "contraindications_ja": "ペニシリン過敏症。ウサギ・げっ歯類への経口投与。",
    },
    {
        "id": "oxytetracycline",
        "name": "Oxytetracycline",
        "name_ja": "オキシテトラサイクリン",
        "category": "antibiotics",
        "mechanism": "Tetracycline antibiotic; inhibits protein synthesis at 30S ribosome.",
        "mechanism_ja": "テトラサイクリン系抗生物質。30Sリボソームでタンパク質合成を阻害。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "20 mg/kg PO q8h",
                "dosage_ja": "20 mg/kg 経口 8時間毎",
                "notes": "Doxycycline often preferred due to better absorption",
                "notes_ja": "吸収が良好なドキシサイクリンが好まれることが多い",
            },
            "cat": {
                "safe": True,
                "dosage": "20 mg/kg PO q8h",
                "dosage_ja": "20 mg/kg 経口 8時間毎",
                "notes": "Same as above; chelates with calcium in food",
                "notes_ja": "上記と同様。食物中のカルシウムとキレート化する。",
            },
            "horse": {
                "safe": True,
                "dosage": "6.6 mg/kg IV q12h (slow)",
                "dosage_ja": "6.6 mg/kg 静注 12時間毎（緩徐に）",
                "notes": "IV infusion must be slow; causes collapse if given rapidly",
                "notes_ja": "静注は緩徐に。急速投与で虚脱を引き起こす。",
            },
            "bird": {
                "safe": True,
                "dosage": "50 mg/kg IM q24-48h",
                "dosage_ja": "50 mg/kg 筋注 24-48時間毎",
                "notes": "Used for chlamydiosis but doxycycline preferred",
                "notes_ja": "クラミジア症に使用されるがドキシサイクリンが好ましい",
            },
        },
        "side_effects": ["GI upset", "photosensitivity", "tooth discoloration"],
        "side_effects_ja": ["消化器症状", "光線過敏症", "歯の変色"],
        "contraindications": "Pregnancy. Young growing animals. Renal failure.",
        "contraindications_ja": "妊娠中。成長期の若齢動物。腎不全。",
    },
    {
        "id": "ampicillin",
        "name": "Ampicillin",
        "name_ja": "アンピシリン",
        "category": "antibiotics",
        "mechanism": "Aminopenicillin; broader spectrum than penicillin G, includes some gram-negatives.",
        "mechanism_ja": "アミノペニシリン。ペニシリンGより広いスペクトルで一部のグラム陰性菌にも有効。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "10-20 mg/kg IV/IM/SC q6-8h",
                "dosage_ja": "10-20 mg/kg 静注/筋注/皮下 6-8時間毎",
                "notes": "Parenteral preferred due to poor oral absorption",
                "notes_ja": "経口吸収が不良のため非経口が好ましい",
            },
            "cat": {
                "safe": True,
                "dosage": "10-20 mg/kg IV/IM/SC q6-8h",
                "dosage_ja": "10-20 mg/kg 静注/筋注/皮下 6-8時間毎",
                "notes": "Same as dogs",
                "notes_ja": "犬と同様",
            },
            "horse": {
                "safe": True,
                "dosage": "10-20 mg/kg IV/IM q6-8h",
                "dosage_ja": "10-20 mg/kg 静注/筋注 6-8時間毎",
                "notes": "Not absorbed orally in horses",
                "notes_ja": "馬では経口吸収されない",
            },
            "hamster": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "CONTRAINDICATED - causes fatal enteritis",
                "notes_ja": "【禁忌】致死的な腸炎を引き起こす",
            },
            "guinea_pig": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "CONTRAINDICATED orally",
                "notes_ja": "【禁忌】経口投与不可",
            },
        },
        "side_effects": ["GI upset", "allergic reactions", "diarrhea"],
        "side_effects_ja": ["消化器症状", "アレルギー反応", "下痢"],
        "contraindications": "Penicillin hypersensitivity. Oral use in hamsters and guinea pigs.",
        "contraindications_ja": "ペニシリン過敏症。ハムスター・モルモットへの経口投与。",
    },
    {
        "id": "rifampin",
        "name": "Rifampin",
        "name_ja": "リファンピン",
        "category": "antibiotics",
        "mechanism": "Inhibits bacterial RNA polymerase. Excellent intracellular penetration.",
        "mechanism_ja": "細菌RNAポリメラーゼを阻害。優れた細胞内移行性。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "5-10 mg/kg PO q24h",
                "dosage_ja": "5-10 mg/kg 経口 24時間毎",
                "notes": "Always use in combination; resistance develops rapidly if used alone. Turns urine/tears orange.",
                "notes_ja": "必ず併用投与。単独使用では急速に耐性化。尿・涙液がオレンジ色になる。",
            },
            "cat": {
                "safe": True,
                "dosage": "10-15 mg/kg PO q24h",
                "dosage_ja": "10-15 mg/kg 経口 24時間毎",
                "notes": "Same precautions as dogs",
                "notes_ja": "犬と同様の注意事項",
            },
            "horse": {
                "safe": True,
                "dosage": "5 mg/kg PO q12h",
                "dosage_ja": "5 mg/kg 経口 12時間毎",
                "notes": "Essential for Rhodococcus equi in foals (combined with macrolide)",
                "notes_ja": "子馬のロドコッカス・エクイに必須（マクロライドと併用）",
            },
        },
        "side_effects": [
            "hepatotoxicity",
            "GI upset",
            "orange discoloration of body fluids",
            "drug interactions (CYP inducer)",
        ],
        "side_effects_ja": ["肝毒性", "消化器症状", "体液のオレンジ色変色", "薬物相互作用（CYP誘導）"],
        "contraindications": "Hepatic disease. Never use as monotherapy.",
        "contraindications_ja": "肝疾患。単剤療法としては決して使用しない。",
    },
    # ══════════════════════════════════════════════════════════════════════
    # 抗真菌薬 (Antifungals)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": "itraconazole",
        "name": "Itraconazole",
        "name_ja": "イトラコナゾール",
        "category": "antifungals",
        "mechanism": "Triazole antifungal; inhibits ergosterol synthesis by blocking lanosterol 14-alpha-demethylase.",
        "mechanism_ja": "トリアゾール系抗真菌薬。ラノステロール14α-脱メチル化酵素を阻害しエルゴステロール合成を阻害。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "5-10 mg/kg PO q24h",
                "dosage_ja": "5-10 mg/kg 経口 24時間毎",
                "notes": "Give with food for better absorption. Pulse therapy option.",
                "notes_ja": "吸収改善のため食事と共に投与。パルス療法も選択肢。",
            },
            "cat": {
                "safe": True,
                "dosage": "5-10 mg/kg PO q24h",
                "dosage_ja": "5-10 mg/kg 経口 24時間毎",
                "notes": "Drug of choice for dermatophytosis in cats. Monitor liver enzymes.",
                "notes_ja": "猫の皮膚糸状菌症の第一選択薬。肝酵素を監視。",
            },
            "horse": {
                "safe": True,
                "dosage": "5 mg/kg PO q24h",
                "dosage_ja": "5 mg/kg 経口 24時間毎",
                "notes": "Used for guttural pouch mycosis",
                "notes_ja": "喉嚢真菌症に使用",
            },
            "bird": {
                "safe": True,
                "dosage": "5-10 mg/kg PO q12-24h",
                "dosage_ja": "5-10 mg/kg 経口 12-24時間毎",
                "notes": "Drug of choice for aspergillosis",
                "notes_ja": "アスペルギルス症の第一選択薬",
            },
            "reptile": {
                "safe": True,
                "dosage": "5 mg/kg PO q24h",
                "dosage_ja": "5 mg/kg 経口 24時間毎",
                "notes": "Used for systemic mycoses",
                "notes_ja": "全身性真菌症に使用",
            },
            "ferret": {
                "safe": True,
                "dosage": "25-33 mg/kg PO q24h",
                "dosage_ja": "25-33 mg/kg 経口 24時間毎",
                "notes": "Safe for ferrets",
                "notes_ja": "フェレットに安全",
            },
        },
        "side_effects": ["hepatotoxicity", "GI upset", "vasculitis (dogs)", "anorexia"],
        "side_effects_ja": ["肝毒性", "消化器症状", "血管炎（犬）", "食欲不振"],
        "contraindications": "Hepatic disease. Pregnancy. Concurrent use with certain drugs (CYP3A4 interactions).",
        "contraindications_ja": "肝疾患。妊娠中。特定の薬剤との併用（CYP3A4相互作用）。",
    },
    {
        "id": "fluconazole",
        "name": "Fluconazole",
        "name_ja": "フルコナゾール",
        "category": "antifungals",
        "mechanism": "Triazole antifungal; inhibits ergosterol synthesis. Excellent CNS penetration.",
        "mechanism_ja": "トリアゾール系抗真菌薬。エルゴステロール合成を阻害。優れたCNS移行性。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "5-10 mg/kg PO q12-24h",
                "dosage_ja": "5-10 mg/kg 経口 12-24時間毎",
                "notes": "Preferred for CNS fungal infections due to excellent BBB penetration",
                "notes_ja": "優れたBBB通過性のためCNS真菌感染症に好ましい",
            },
            "cat": {
                "safe": True,
                "dosage": "5-10 mg/kg PO q12-24h",
                "dosage_ja": "5-10 mg/kg 経口 12-24時間毎",
                "notes": "Good for cryptococcosis",
                "notes_ja": "クリプトコッカス症に有効",
            },
            "rabbit": {
                "safe": True,
                "dosage": "5-10 mg/kg PO q24h",
                "dosage_ja": "5-10 mg/kg 経口 24時間毎",
                "notes": "Used for Encephalitozoon cuniculi adjunct treatment",
                "notes_ja": "エンセファリトゾーン・クニクリの補助治療に使用",
            },
            "bird": {
                "safe": True,
                "dosage": "5-15 mg/kg PO q24h",
                "dosage_ja": "5-15 mg/kg 経口 24時間毎",
                "notes": "Alternative for aspergillosis; less hepatotoxic than itraconazole",
                "notes_ja": "アスペルギルス症の代替薬。イトラコナゾールより肝毒性が少ない。",
            },
            "reptile": {
                "safe": True,
                "dosage": "5 mg/kg PO q24-48h",
                "dosage_ja": "5 mg/kg 経口 24-48時間毎",
                "notes": "Safe for reptiles",
                "notes_ja": "爬虫類に安全",
            },
        },
        "side_effects": ["hepatotoxicity (less than ketoconazole)", "GI upset"],
        "side_effects_ja": ["肝毒性（ケトコナゾールより少ない）", "消化器症状"],
        "contraindications": "Hepatic disease (use with caution).",
        "contraindications_ja": "肝疾患（注意して使用）。",
    },
    {
        "id": "ketoconazole",
        "name": "Ketoconazole",
        "name_ja": "ケトコナゾール",
        "category": "antifungals",
        "mechanism": "Imidazole antifungal; inhibits ergosterol synthesis and adrenal steroidogenesis.",
        "mechanism_ja": "イミダゾール系抗真菌薬。エルゴステロール合成と副腎ステロイド合成を阻害。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "5-10 mg/kg PO q12h",
                "dosage_ja": "5-10 mg/kg 経口 12時間毎",
                "notes": "More hepatotoxic than newer azoles. Also used for Cushing's (off-label).",
                "notes_ja": "新世代アゾールより肝毒性が高い。クッシング症候群にも使用（適応外）。",
            },
            "cat": {
                "safe": True,
                "dosage": "5-10 mg/kg PO q12-24h",
                "dosage_ja": "5-10 mg/kg 経口 12-24時間毎",
                "notes": "Higher hepatotoxicity risk in cats. Monitor closely.",
                "notes_ja": "猫では肝毒性リスクが高い。注意深く監視。",
            },
            "bird": {
                "safe": True,
                "dosage": "20-30 mg/kg PO q12h",
                "dosage_ja": "20-30 mg/kg 経口 12時間毎",
                "notes": "Less effective than itraconazole for aspergillosis",
                "notes_ja": "アスペルギルス症にはイトラコナゾールより効果が劣る",
            },
        },
        "side_effects": ["hepatotoxicity", "GI upset", "adrenal suppression", "teratogenic"],
        "side_effects_ja": ["肝毒性", "消化器症状", "副腎抑制", "催奇形性"],
        "contraindications": "Pregnancy. Hepatic disease. Concurrent use with drugs metabolized by CYP3A4.",
        "contraindications_ja": "妊娠中。肝疾患。CYP3A4で代謝される薬剤との併用。",
    },
    {
        "id": "terbinafine",
        "name": "Terbinafine",
        "name_ja": "テルビナフィン",
        "category": "antifungals",
        "mechanism": "Allylamine antifungal; inhibits squalene epoxidase in ergosterol synthesis.",
        "mechanism_ja": "アリルアミン系抗真菌薬。エルゴステロール合成のスクアレンエポキシダーゼを阻害。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "30-40 mg/kg PO q24h",
                "dosage_ja": "30-40 mg/kg 経口 24時間毎",
                "notes": "Effective for dermatophytosis",
                "notes_ja": "皮膚糸状菌症に有効",
            },
            "cat": {
                "safe": True,
                "dosage": "30-40 mg/kg PO q24h",
                "dosage_ja": "30-40 mg/kg 経口 24時間毎",
                "notes": "Can be combined with itraconazole for refractory cases",
                "notes_ja": "難治性症例ではイトラコナゾールと併用可",
            },
            "rabbit": {
                "safe": True,
                "dosage": "20-40 mg/kg PO q24h",
                "dosage_ja": "20-40 mg/kg 経口 24時間毎",
                "notes": "Safe for rabbits",
                "notes_ja": "ウサギに安全",
            },
        },
        "side_effects": ["GI upset", "hepatotoxicity (rare)"],
        "side_effects_ja": ["消化器症状", "肝毒性（まれ）"],
        "contraindications": "Hepatic disease.",
        "contraindications_ja": "肝疾患。",
    },
    {
        "id": "amphotericin_b",
        "name": "Amphotericin B",
        "name_ja": "アムホテリシンB",
        "category": "antifungals",
        "mechanism": "Polyene antifungal; binds ergosterol in fungal cell membrane, creating pores.",
        "mechanism_ja": "ポリエン系抗真菌薬。真菌細胞膜のエルゴステロールに結合し孔を形成する。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "0.5-1 mg/kg IV q48h (conventional); lipid complex: 1-5 mg/kg IV q48h",
                "dosage_ja": "0.5-1 mg/kg 静注 48時間毎（従来型）; 脂質複合体: 1-5 mg/kg 静注 48時間毎",
                "notes": "Highly nephrotoxic. Pre-hydrate with saline. Monitor BUN/creatinine.",
                "notes_ja": "腎毒性が高い。生理食塩水で事前水和。BUN/クレアチニンを監視。",
            },
            "cat": {
                "safe": True,
                "dosage": "0.25-0.5 mg/kg IV q48h",
                "dosage_ja": "0.25-0.5 mg/kg 静注 48時間毎",
                "notes": "Cats very sensitive to nephrotoxicity. Use lipid complex if possible.",
                "notes_ja": "猫は腎毒性に非常に敏感。可能であれば脂質複合体を使用。",
            },
            "bird": {
                "safe": True,
                "dosage": "1-1.5 mg/kg IV q12h for 3-5 days; intratracheal: 1 mg/kg",
                "dosage_ja": "1-1.5 mg/kg 静注 12時間毎×3-5日; 気管内: 1 mg/kg",
                "notes": "Used for severe aspergillosis. Nebulization also used.",
                "notes_ja": "重度アスペルギルス症に使用。噴霧投与も可。",
            },
        },
        "side_effects": ["nephrotoxicity", "fever/chills during infusion", "hypokalemia", "anemia"],
        "side_effects_ja": ["腎毒性", "投与中の発熱・悪寒", "低カリウム血症", "貧血"],
        "contraindications": "Renal disease. Concurrent nephrotoxic drugs.",
        "contraindications_ja": "腎疾患。腎毒性薬剤との併用。",
    },
    {
        "id": "griseofulvin",
        "name": "Griseofulvin",
        "name_ja": "グリセオフルビン",
        "category": "antifungals",
        "mechanism": "Disrupts mitotic spindle function in fungi, inhibiting cell division.",
        "mechanism_ja": "真菌の有糸分裂紡錘体機能を阻害し細胞分裂を抑制する。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "50-100 mg/kg PO q24h (microsize); 25-50 mg/kg (ultramicrosize)",
                "dosage_ja": "50-100 mg/kg 経口 24時間毎（マイクロサイズ）; 25-50 mg/kg（ウルトラマイクロサイズ）",
                "notes": "Give with fatty meal. Being replaced by newer azoles.",
                "notes_ja": "脂肪食と共に投与。新世代アゾールに置き換えられつつある。",
            },
            "cat": {
                "safe": True,
                "dosage": "50-100 mg/kg PO q24h",
                "dosage_ja": "50-100 mg/kg 経口 24時間毎",
                "notes": "TERATOGENIC - do not use in pregnant cats. Bone marrow suppression in FIV+ cats.",
                "notes_ja": "【催奇形性】妊娠猫には使用不可。FIV陽性猫で骨髄抑制。",
            },
        },
        "side_effects": ["teratogenicity", "bone marrow suppression", "hepatotoxicity", "GI upset"],
        "side_effects_ja": ["催奇形性", "骨髄抑制", "肝毒性", "消化器症状"],
        "contraindications": "Pregnancy (teratogenic). FIV-positive cats. Hepatic disease.",
        "contraindications_ja": "妊娠中（催奇形性）。FIV陽性猫。肝疾患。",
    },
    {
        "id": "voriconazole",
        "name": "Voriconazole",
        "name_ja": "ボリコナゾール",
        "category": "antifungals",
        "mechanism": "Second-generation triazole; inhibits ergosterol synthesis. Broader spectrum than fluconazole.",
        "mechanism_ja": "第二世代トリアゾール。エルゴステロール合成を阻害。フルコナゾールより広いスペクトル。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "4-6 mg/kg PO q12h",
                "dosage_ja": "4-6 mg/kg 経口 12時間毎",
                "notes": "Rapid metabolism in dogs; may need higher doses",
                "notes_ja": "犬では代謝が速い。高用量が必要な場合がある。",
            },
            "cat": {
                "safe": True,
                "dosage": "5-6 mg/kg PO q12h",
                "dosage_ja": "5-6 mg/kg 経口 12時間毎",
                "notes": "Better tolerated than in dogs",
                "notes_ja": "犬より忍容性が良好",
            },
            "bird": {
                "safe": True,
                "dosage": "10-12 mg/kg PO q12h",
                "dosage_ja": "10-12 mg/kg 経口 12時間毎",
                "notes": "Emerging choice for avian aspergillosis",
                "notes_ja": "鳥類アスペルギルス症の新しい選択肢",
            },
        },
        "side_effects": ["hepatotoxicity", "visual disturbances", "GI upset"],
        "side_effects_ja": ["肝毒性", "視覚障害", "消化器症状"],
        "contraindications": "Hepatic disease. Concurrent use with CYP-interacting drugs.",
        "contraindications_ja": "肝疾患。CYP相互作用のある薬剤との併用。",
    },
    # ══════════════════════════════════════════════════════════════════════
    # 駆虫薬・抗寄生虫薬 (Antiparasitics)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": "ivermectin",
        "name": "Ivermectin",
        "name_ja": "イベルメクチン",
        "category": "antiparasitics",
        "mechanism": "Macrocyclic lactone; activates glutamate-gated chloride channels in parasites, causing paralysis.",
        "mechanism_ja": "大環状ラクトン。寄生虫のグルタミン酸依存性塩素チャネルを活性化し麻痺を引き起こす。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "6-12 mcg/kg PO monthly (heartworm prevention); 200-400 mcg/kg PO q24h (demodicosis)",
                "dosage_ja": "6-12 mcg/kg 経口 月1回（フィラリア予防）; 200-400 mcg/kg 経口 24時間毎（毛包虫症）",
                "notes": "LETHAL in MDR1-mutant dogs (Collies, Shelties, etc.) at high doses. Test MDR1 status first.",
                "notes_ja": "【警告】MDR1変異犬（コリー・シェルティ等）では高用量で致死的。事前にMDR1検査を。",
            },
            "cat": {
                "safe": True,
                "dosage": "24 mcg/kg PO monthly (heartworm prevention); 200-300 mcg/kg SC (ear mites)",
                "dosage_ja": "24 mcg/kg 経口 月1回（フィラリア予防）; 200-300 mcg/kg 皮下（耳ダニ）",
                "notes": "Generally safe at recommended doses",
                "notes_ja": "推奨用量では一般的に安全",
            },
            "horse": {
                "safe": True,
                "dosage": "200 mcg/kg PO (paste)",
                "dosage_ja": "200 mcg/kg 経口（ペースト）",
                "notes": "Standard equine dewormer",
                "notes_ja": "標準的な馬の駆虫薬",
            },
            "rabbit": {
                "safe": True,
                "dosage": "200-400 mcg/kg SC q10-14 days",
                "dosage_ja": "200-400 mcg/kg 皮下 10-14日毎",
                "notes": "Used for ear mites, fur mites",
                "notes_ja": "耳ダニ・毛ダニに使用",
            },
            "guinea_pig": {
                "safe": True,
                "dosage": "200-500 mcg/kg SC q10-14 days",
                "dosage_ja": "200-500 mcg/kg 皮下 10-14日毎",
                "notes": "Used for mites (Trixacarus)",
                "notes_ja": "ダニ（トリキサカルス）に使用",
            },
            "hamster": {
                "safe": True,
                "dosage": "200-400 mcg/kg SC q10-14 days",
                "dosage_ja": "200-400 mcg/kg 皮下 10-14日毎",
                "notes": "Used for Demodex in hamsters",
                "notes_ja": "ハムスターのニキビダニに使用",
            },
            "ferret": {
                "safe": True,
                "dosage": "20 mcg/kg PO monthly (heartworm); 200-400 mcg/kg SC (ear mites)",
                "dosage_ja": "20 mcg/kg 経口 月1回（フィラリア）; 200-400 mcg/kg 皮下（耳ダニ）",
                "notes": "Safe at recommended doses",
                "notes_ja": "推奨用量では安全",
            },
            "bird": {
                "safe": True,
                "dosage": "200 mcg/kg PO/topical; dilute for small birds",
                "dosage_ja": "200 mcg/kg 経口/局所; 小鳥は希釈",
                "notes": "Narrow safety margin in small birds. Overdose is fatal.",
                "notes_ja": "小鳥では安全域が狭い。過量投与は致死的。",
            },
            "tortoise": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "CONTRAINDICATED in chelonians (tortoises/turtles) - can be lethal",
                "notes_ja": "【禁忌】カメ類には致死的な可能性",
            },
            "reptile": {
                "safe": True,
                "dosage": "200 mcg/kg PO/SC q14 days (snakes, lizards)",
                "dosage_ja": "200 mcg/kg 経口/皮下 14日毎（ヘビ・トカゲ）",
                "notes": "NEVER use in chelonians. Safe in snakes and lizards.",
                "notes_ja": "カメ類には絶対に使用しない。ヘビ・トカゲには安全。",
            },
        },
        "side_effects": ["ataxia", "tremors", "mydriasis", "blindness (MDR1 dogs)", "death at toxic doses"],
        "side_effects_ja": ["運動失調", "振戦", "散瞳", "失明（MDR1犬）", "中毒量で死亡"],
        "contraindications": "MDR1-mutant dogs (Collies, Shelties, Australian Shepherds) at high doses. Chelonians (tortoises/turtles).",
        "contraindications_ja": "MDR1変異犬（コリー・シェルティ・オーストラリアンシェパード）の高用量。カメ類（リクガメ・ウミガメ）。",
    },
    {
        "id": "selamectin",
        "name": "Selamectin (Revolution/Stronghold)",
        "name_ja": "セラメクチン（レボリューション）",
        "category": "antiparasitics",
        "mechanism": "Macrocyclic lactone; topical parasiticide for fleas, heartworm, ear mites, sarcoptic mange.",
        "mechanism_ja": "大環状ラクトン。ノミ・フィラリア・耳ダニ・疥癬の局所駆虫薬。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "6 mg/kg topical monthly",
                "dosage_ja": "6 mg/kg 局所 月1回",
                "notes": "Safe for MDR1-mutant dogs at labeled dose",
                "notes_ja": "表示用量ではMDR1変異犬にも安全",
            },
            "cat": {
                "safe": True,
                "dosage": "6 mg/kg topical monthly",
                "dosage_ja": "6 mg/kg 局所 月1回",
                "notes": "Excellent safety profile",
                "notes_ja": "優れた安全性プロファイル",
            },
            "rabbit": {
                "safe": True,
                "dosage": "6-18 mg/kg topical monthly",
                "dosage_ja": "6-18 mg/kg 局所 月1回",
                "notes": "Safe for rabbits; used for fur mites, ear mites",
                "notes_ja": "ウサギに安全。毛ダニ・耳ダニに使用。",
            },
            "ferret": {
                "safe": True,
                "dosage": "6-18 mg/kg topical monthly",
                "dosage_ja": "6-18 mg/kg 局所 月1回",
                "notes": "Safe and commonly used",
                "notes_ja": "安全で一般的に使用",
            },
            "guinea_pig": {
                "safe": True,
                "dosage": "15 mg/kg topical monthly",
                "dosage_ja": "15 mg/kg 局所 月1回",
                "notes": "Off-label but widely used",
                "notes_ja": "適応外だが広く使用",
            },
            "hedgehog": {
                "safe": True,
                "dosage": "6-18 mg/kg topical q30 days",
                "dosage_ja": "6-18 mg/kg 局所 30日毎",
                "notes": "Used for mite treatment",
                "notes_ja": "ダニ治療に使用",
            },
        },
        "side_effects": ["temporary hair loss at application site", "mild GI upset if ingested"],
        "side_effects_ja": ["塗布部位の一時的脱毛", "経口摂取時の軽度消化器症状"],
        "contraindications": "Kittens/puppies under 6 weeks of age.",
        "contraindications_ja": "6週齢未満の子猫・子犬。",
    },
    {
        "id": "fenbendazole",
        "name": "Fenbendazole",
        "name_ja": "フェンベンダゾール",
        "category": "antiparasitics",
        "mechanism": "Benzimidazole; inhibits tubulin polymerization in parasites, disrupting cellular structure.",
        "mechanism_ja": "ベンズイミダゾール系。寄生虫のチューブリン重合を阻害し細胞構造を破壊する。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "50 mg/kg PO q24h for 3-5 days",
                "dosage_ja": "50 mg/kg 経口 24時間毎×3-5日",
                "notes": "Very safe; wide safety margin. Effective against Giardia.",
                "notes_ja": "非常に安全。広い安全域。ジアルジアにも有効。",
            },
            "cat": {
                "safe": True,
                "dosage": "50 mg/kg PO q24h for 3-5 days",
                "dosage_ja": "50 mg/kg 経口 24時間毎×3-5日",
                "notes": "Safe for cats",
                "notes_ja": "猫に安全",
            },
            "horse": {
                "safe": True,
                "dosage": "5-10 mg/kg PO single dose",
                "dosage_ja": "5-10 mg/kg 経口 単回投与",
                "notes": "Widely used equine dewormer",
                "notes_ja": "広く使用される馬の駆虫薬",
            },
            "rabbit": {
                "safe": True,
                "dosage": "20 mg/kg PO q24h for 5 days",
                "dosage_ja": "20 mg/kg 経口 24時間毎×5日",
                "notes": "Used for E. cuniculi treatment",
                "notes_ja": "E. cuniculi治療に使用",
            },
            "guinea_pig": {
                "safe": True,
                "dosage": "20-50 mg/kg PO q24h for 5 days",
                "dosage_ja": "20-50 mg/kg 経口 24時間毎×5日",
                "notes": "Safe and effective",
                "notes_ja": "安全かつ有効",
            },
            "bird": {
                "safe": True,
                "dosage": "20-50 mg/kg PO q24h for 3-5 days",
                "dosage_ja": "20-50 mg/kg 経口 24時間毎×3-5日",
                "notes": "CAUTION: Toxic in some species (vultures, storks, doves). Monitor WBC counts.",
                "notes_ja": "【注意】一部の鳥種（ハゲワシ・コウノトリ・ハト）に毒性。白血球数を監視。",
            },
            "reptile": {
                "safe": True,
                "dosage": "50-100 mg/kg PO, repeat in 14 days",
                "dosage_ja": "50-100 mg/kg 経口、14日後に反復",
                "notes": "Effective against common reptile nematodes",
                "notes_ja": "一般的な爬虫類線虫に有効",
            },
        },
        "side_effects": ["bone marrow suppression (prolonged use)", "hepatotoxicity (rare)"],
        "side_effects_ja": ["骨髄抑制（長期使用）", "肝毒性（まれ）"],
        "contraindications": "Some bird species (vultures, storks). Early pregnancy (teratogenic in lab animals).",
        "contraindications_ja": "一部の鳥種（ハゲワシ・コウノトリ）。妊娠初期（実験動物で催奇形性）。",
    },
    {
        "id": "praziquantel",
        "name": "Praziquantel",
        "name_ja": "プラジカンテル",
        "category": "antiparasitics",
        "mechanism": "Increases cell membrane permeability in cestodes and trematodes, causing paralysis and disintegration.",
        "mechanism_ja": "条虫・吸虫の細胞膜透過性を増加させ麻痺と崩壊を引き起こす。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "5 mg/kg PO/SC/IM single dose (tapeworms)",
                "dosage_ja": "5 mg/kg 経口/皮下/筋注 単回投与（条虫）",
                "notes": "Very safe; wide margin",
                "notes_ja": "非常に安全。広い安全域。",
            },
            "cat": {
                "safe": True,
                "dosage": "5 mg/kg PO/SC/IM single dose",
                "dosage_ja": "5 mg/kg 経口/皮下/筋注 単回投与",
                "notes": "Safe for cats",
                "notes_ja": "猫に安全",
            },
            "horse": {
                "safe": True,
                "dosage": "1-2 mg/kg PO single dose",
                "dosage_ja": "1-2 mg/kg 経口 単回投与",
                "notes": "Used for tapeworms in horses",
                "notes_ja": "馬の条虫に使用",
            },
            "rabbit": {
                "safe": True,
                "dosage": "5-10 mg/kg PO/SC, repeat in 10-14 days",
                "dosage_ja": "5-10 mg/kg 経口/皮下、10-14日後に反復",
                "notes": "Safe for rabbits",
                "notes_ja": "ウサギに安全",
            },
            "bird": {
                "safe": True,
                "dosage": "10-20 mg/kg PO single dose",
                "dosage_ja": "10-20 mg/kg 経口 単回投与",
                "notes": "Effective for avian tapeworms",
                "notes_ja": "鳥類の条虫に有効",
            },
            "reptile": {
                "safe": True,
                "dosage": "5-8 mg/kg PO, repeat in 14 days",
                "dosage_ja": "5-8 mg/kg 経口、14日後に反復",
                "notes": "Safe for reptiles",
                "notes_ja": "爬虫類に安全",
            },
        },
        "side_effects": ["transient GI upset", "drooling (cats)", "diarrhea"],
        "side_effects_ja": ["一過性の消化器症状", "流涎（猫）", "下痢"],
        "contraindications": "Puppies/kittens under 4 weeks.",
        "contraindications_ja": "4週齢未満の子犬・子猫。",
    },
    {
        "id": "fipronil",
        "name": "Fipronil (Frontline)",
        "name_ja": "フィプロニル（フロントライン）",
        "category": "antiparasitics",
        "mechanism": "Phenylpyrazole; blocks GABA-gated chloride channels in arthropods.",
        "mechanism_ja": "フェニルピラゾール系。節足動物のGABA依存性塩素チャネルを遮断。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Topical spot-on monthly",
                "dosage_ja": "局所スポットオン 月1回",
                "notes": "Effective for fleas and ticks",
                "notes_ja": "ノミ・ダニに有効",
            },
            "cat": {
                "safe": True,
                "dosage": "Topical spot-on monthly",
                "dosage_ja": "局所スポットオン 月1回",
                "notes": "Cat-specific formulation only",
                "notes_ja": "猫専用製剤のみ使用",
            },
            "rabbit": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "CONTRAINDICATED - toxicity and deaths reported in rabbits",
                "notes_ja": "【禁忌】ウサギでの中毒・死亡報告あり",
            },
            "ferret": {
                "safe": True,
                "dosage": "Cat-size spot-on topical monthly",
                "dosage_ja": "猫サイズのスポットオン 局所 月1回",
                "notes": "Use cat formulation",
                "notes_ja": "猫用製剤を使用",
            },
        },
        "side_effects": ["skin irritation at application site", "hypersalivation if licked"],
        "side_effects_ja": ["塗布部位の皮膚刺激", "舐めた場合の流涎"],
        "contraindications": "Rabbits. Kittens/puppies under 8 weeks.",
        "contraindications_ja": "ウサギ。8週齢未満の子猫・子犬。",
    },
    {
        "id": "fluralaner",
        "name": "Fluralaner (Bravecto)",
        "name_ja": "フルララネル（ブラベクト）",
        "category": "antiparasitics",
        "mechanism": "Isoxazoline; inhibits GABA and glutamate-gated chloride channels in arthropods.",
        "mechanism_ja": "イソキサゾリン系。節足動物のGABAおよびグルタミン酸依存性塩素チャネルを阻害。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "25-56 mg/kg PO single dose, lasts 12 weeks",
                "dosage_ja": "25-56 mg/kg 経口 単回投与、12週間持続",
                "notes": "Long-acting flea and tick prevention",
                "notes_ja": "長時間作用型ノミ・ダニ予防",
            },
            "cat": {
                "safe": True,
                "dosage": "40-94 mg/kg topical, lasts 12 weeks",
                "dosage_ja": "40-94 mg/kg 局所、12週間持続",
                "notes": "Topical formulation for cats",
                "notes_ja": "猫用局所製剤",
            },
            "rabbit": {
                "safe": True,
                "dosage": "15-25 mg/kg PO single dose",
                "dosage_ja": "15-25 mg/kg 経口 単回投与",
                "notes": "Off-label; increasingly used for Cheyletiella and fur mites",
                "notes_ja": "適応外。ツメダニ・毛ダニに使用が増加中。",
            },
        },
        "side_effects": ["vomiting", "diarrhea", "lethargy", "seizures (rare, mainly dogs with history)"],
        "side_effects_ja": ["嘔吐", "下痢", "無気力", "痙攣（まれ、主に既往歴のある犬）"],
        "contraindications": "Dogs with seizure history (use with caution). Not labeled for rabbits.",
        "contraindications_ja": "痙攣既往歴のある犬（注意して使用）。ウサギには未承認。",
    },
    {
        "id": "moxidectin",
        "name": "Moxidectin",
        "name_ja": "モキシデクチン",
        "category": "antiparasitics",
        "mechanism": "Macrocyclic lactone; similar to ivermectin but with longer duration and higher lipophilicity.",
        "mechanism_ja": "大環状ラクトン。イベルメクチンに類似するが持続時間が長く脂溶性が高い。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "3 mcg/kg PO monthly (heartworm); topical: per product label",
                "dosage_ja": "3 mcg/kg 経口 月1回（フィラリア）; 局所: 製品ラベルに従う",
                "notes": "Available as injectable sustained-release (ProHeart 12)",
                "notes_ja": "注射用持続放出型（プロハート12）あり",
            },
            "cat": {
                "safe": True,
                "dosage": "Topical as per product label",
                "dosage_ja": "局所 製品ラベルに従う",
                "notes": "Available in combination products",
                "notes_ja": "合剤製品で入手可能",
            },
            "horse": {
                "safe": True,
                "dosage": "400 mcg/kg PO (gel)",
                "dosage_ja": "400 mcg/kg 経口（ジェル）",
                "notes": "Effective against encysted small strongyles",
                "notes_ja": "被嚢小円虫に有効",
            },
        },
        "side_effects": ["lethargy", "ataxia (if overdosed)", "MDR1 sensitivity similar to ivermectin"],
        "side_effects_ja": ["無気力", "運動失調（過量投与時）", "イベルメクチン同様のMDR1感受性"],
        "contraindications": "MDR1-mutant dogs (at high doses). Caution in chelonians.",
        "contraindications_ja": "MDR1変異犬（高用量）。カメ類では注意。",
    },
    {
        "id": "milbemycin_oxime",
        "name": "Milbemycin Oxime",
        "name_ja": "ミルベマイシンオキシム",
        "category": "antiparasitics",
        "mechanism": "Macrocyclic lactone; heartworm prevention and intestinal parasite control.",
        "mechanism_ja": "大環状ラクトン。フィラリア予防と消化管寄生虫駆除。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "0.5-1 mg/kg PO monthly",
                "dosage_ja": "0.5-1 mg/kg 経口 月1回",
                "notes": "Safe at labeled doses even in MDR1 dogs. Interceptor/Sentinel.",
                "notes_ja": "MDR1犬でも表示用量では安全。インターセプター/センチネル。",
            },
            "cat": {
                "safe": True,
                "dosage": "2 mg/kg PO monthly",
                "dosage_ja": "2 mg/kg 経口 月1回",
                "notes": "Part of heartworm prevention programs",
                "notes_ja": "フィラリア予防プログラムの一部",
            },
        },
        "side_effects": ["rare at labeled doses"],
        "side_effects_ja": ["表示用量ではまれ"],
        "contraindications": "None at labeled doses.",
        "contraindications_ja": "表示用量では特になし。",
    },
    {
        "id": "toltrazuril",
        "name": "Toltrazuril",
        "name_ja": "トルトラズリル",
        "category": "antiparasitics",
        "mechanism": "Triazinetrione; coccidiostat that targets all intracellular stages of coccidia.",
        "mechanism_ja": "トリアジントリオン系。コクシジウムの全ての細胞内段階を標的とする抗コクシジウム薬。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "10-20 mg/kg PO q24h for 3 days",
                "dosage_ja": "10-20 mg/kg 経口 24時間毎×3日",
                "notes": "Effective coccidiosis treatment. Baycox.",
                "notes_ja": "コクシジウム症の有効な治療薬。バイコックス。",
            },
            "cat": {
                "safe": True,
                "dosage": "10-20 mg/kg PO q24h for 3 days",
                "dosage_ja": "10-20 mg/kg 経口 24時間毎×3日",
                "notes": "Isospora treatment",
                "notes_ja": "イソスポーラ治療",
            },
            "rabbit": {
                "safe": True,
                "dosage": "25 mg/kg PO q24h for 2 days, repeat in 5 days",
                "dosage_ja": "25 mg/kg 経口 24時間毎×2日、5日後に反復",
                "notes": "Excellent for hepatic and intestinal coccidiosis",
                "notes_ja": "肝コクシジウム症・腸コクシジウム症に優れた効果",
            },
            "bird": {
                "safe": True,
                "dosage": "7-10 mg/kg PO q24h for 2-3 days",
                "dosage_ja": "7-10 mg/kg 経口 24時間毎×2-3日",
                "notes": "Used in poultry and companion birds",
                "notes_ja": "家禽・伴侶鳥に使用",
            },
        },
        "side_effects": ["generally well tolerated"],
        "side_effects_ja": ["一般的に忍容性良好"],
        "contraindications": "None significant at labeled doses.",
        "contraindications_ja": "表示用量では特になし。",
    },
    # ══════════════════════════════════════════════════════════════════════
    # 非ステロイド性抗炎症薬 NSAIDs
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": "meloxicam",
        "name": "Meloxicam",
        "name_ja": "メロキシカム",
        "category": "nsaids",
        "mechanism": "Preferential COX-2 inhibitor; provides anti-inflammatory, analgesic, and antipyretic effects.",
        "mechanism_ja": "選択的COX-2阻害薬。抗炎症・鎮痛・解熱作用を持つ。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "0.1 mg/kg PO q24h (after 0.2 mg/kg loading dose)",
                "dosage_ja": "0.1 mg/kg 経口 24時間毎（初回0.2 mg/kgローディング後）",
                "notes": "Licensed for long-term use in dogs. Monitor renal function.",
                "notes_ja": "犬での長期使用が認可。腎機能を監視。",
            },
            "cat": {
                "safe": True,
                "dosage": "0.05 mg/kg PO q24h (short-term); 0.01-0.03 mg/kg q24h (long-term, off-label)",
                "dosage_ja": "0.05 mg/kg 経口 24時間毎（短期）; 0.01-0.03 mg/kg 24時間毎（長期、適応外）",
                "notes": "CAUTION with long-term use - renal toxicity. Use lowest effective dose.",
                "notes_ja": "【注意】長期使用では腎毒性。最小有効用量を使用。",
            },
            "horse": {
                "safe": True,
                "dosage": "0.6 mg/kg IV/PO q24h",
                "dosage_ja": "0.6 mg/kg 静注/経口 24時間毎",
                "notes": "Licensed for horses",
                "notes_ja": "馬に認可済み",
            },
            "rabbit": {
                "safe": True,
                "dosage": "0.3-0.5 mg/kg PO/SC q24h",
                "dosage_ja": "0.3-0.5 mg/kg 経口/皮下 24時間毎",
                "notes": "Primary NSAID for rabbits. Well tolerated.",
                "notes_ja": "ウサギの主要NSAID。忍容性良好。",
            },
            "guinea_pig": {
                "safe": True,
                "dosage": "0.1-0.3 mg/kg PO/SC q24h",
                "dosage_ja": "0.1-0.3 mg/kg 経口/皮下 24時間毎",
                "notes": "Safe for guinea pigs",
                "notes_ja": "モルモットに安全",
            },
            "hamster": {
                "safe": True,
                "dosage": "0.1-0.3 mg/kg PO/SC q24h",
                "dosage_ja": "0.1-0.3 mg/kg 経口/皮下 24時間毎",
                "notes": "Used for pain management",
                "notes_ja": "疼痛管理に使用",
            },
            "ferret": {
                "safe": True,
                "dosage": "0.1-0.2 mg/kg PO/SC q24h",
                "dosage_ja": "0.1-0.2 mg/kg 経口/皮下 24時間毎",
                "notes": "Safe for ferrets",
                "notes_ja": "フェレットに安全",
            },
            "hedgehog": {
                "safe": True,
                "dosage": "0.1-0.2 mg/kg PO/SC q24h",
                "dosage_ja": "0.1-0.2 mg/kg 経口/皮下 24時間毎",
                "notes": "Commonly used for pain in hedgehogs",
                "notes_ja": "ハリネズミの疼痛管理に一般的に使用",
            },
            "bird": {
                "safe": True,
                "dosage": "0.1-0.5 mg/kg PO q12-24h",
                "dosage_ja": "0.1-0.5 mg/kg 経口 12-24時間毎",
                "notes": "Primary NSAID for birds",
                "notes_ja": "鳥類の主要NSAID",
            },
            "reptile": {
                "safe": True,
                "dosage": "0.1-0.2 mg/kg PO/IM q24-48h",
                "dosage_ja": "0.1-0.2 mg/kg 経口/筋注 24-48時間毎",
                "notes": "One of the safest NSAIDs for reptiles",
                "notes_ja": "爬虫類に最も安全なNSAIDの一つ",
            },
        },
        "side_effects": ["GI ulceration", "renal toxicity", "hepatotoxicity"],
        "side_effects_ja": ["消化管潰瘍", "腎毒性", "肝毒性"],
        "contraindications": "Renal disease. Hepatic disease. Dehydration. Concurrent corticosteroid or other NSAID use.",
        "contraindications_ja": "腎疾患。肝疾患。脱水。副腎皮質ステロイドまたは他のNSAIDとの併用。",
    },
    {
        "id": "carprofen",
        "name": "Carprofen (Rimadyl)",
        "name_ja": "カルプロフェン（リマダイル）",
        "category": "nsaids",
        "mechanism": "Preferential COX-2 inhibitor; primarily used for osteoarthritis pain in dogs.",
        "mechanism_ja": "選択的COX-2阻害薬。主に犬の変形性関節症の疼痛管理に使用。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "2-4 mg/kg PO q12-24h",
                "dosage_ja": "2-4 mg/kg 経口 12-24時間毎",
                "notes": "Licensed for long-term use in dogs. Hepatotoxicity risk.",
                "notes_ja": "犬での長期使用が認可。肝毒性リスクあり。",
            },
            "cat": {
                "safe": True,
                "dosage": "1-2 mg/kg SC single dose (perioperative only)",
                "dosage_ja": "1-2 mg/kg 皮下 単回投与（周術期のみ）",
                "notes": "NOT for long-term use in cats. Single perioperative dose only.",
                "notes_ja": "猫の長期使用は不可。周術期の単回投与のみ。",
            },
            "horse": {
                "safe": True,
                "dosage": "0.7 mg/kg IV q24h",
                "dosage_ja": "0.7 mg/kg 静注 24時間毎",
                "notes": "Off-label equine use",
                "notes_ja": "馬への適応外使用",
            },
            "ferret": {
                "safe": True,
                "dosage": "1-5 mg/kg PO/SC q12-24h",
                "dosage_ja": "1-5 mg/kg 経口/皮下 12-24時間毎",
                "notes": "Used for musculoskeletal pain",
                "notes_ja": "筋骨格系の疼痛に使用",
            },
        },
        "side_effects": ["hepatotoxicity (dogs)", "GI ulceration", "renal toxicity"],
        "side_effects_ja": ["肝毒性（犬）", "消化管潰瘍", "腎毒性"],
        "contraindications": "Hepatic disease. Renal disease. Dehydration. Concurrent NSAID or steroid use.",
        "contraindications_ja": "肝疾患。腎疾患。脱水。NSAIDまたはステロイドとの併用。",
    },
    {
        "id": "firocoxib",
        "name": "Firocoxib (Previcox)",
        "name_ja": "フィロコキシブ（プレビコックス）",
        "category": "nsaids",
        "mechanism": "Highly selective COX-2 inhibitor (coxib class).",
        "mechanism_ja": "高選択的COX-2阻害薬（コキシブ系）。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "5 mg/kg PO q24h",
                "dosage_ja": "5 mg/kg 経口 24時間毎",
                "notes": "Licensed for osteoarthritis. Good GI safety compared to older NSAIDs.",
                "notes_ja": "変形性関節症に認可。旧世代NSAIDより消化管安全性が良好。",
            },
            "horse": {
                "safe": True,
                "dosage": "0.1 mg/kg PO q24h",
                "dosage_ja": "0.1 mg/kg 経口 24時間毎",
                "notes": "Licensed for horses (Equioxx)",
                "notes_ja": "馬に認可済み（エクイオックス）",
            },
            "cat": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Not recommended for cats",
                "notes_ja": "猫には推奨されない",
            },
        },
        "side_effects": ["GI upset", "renal effects"],
        "side_effects_ja": ["消化器症状", "腎障害"],
        "contraindications": "Cats. Renal or hepatic disease.",
        "contraindications_ja": "猫。腎疾患または肝疾患。",
    },
    {
        "id": "robenacoxib",
        "name": "Robenacoxib (Onsior)",
        "name_ja": "ロベナコキシブ（オンシオール）",
        "category": "nsaids",
        "mechanism": "Highly selective COX-2 inhibitor specifically developed for companion animals.",
        "mechanism_ja": "伴侶動物専用に開発された高選択的COX-2阻害薬。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "1-2 mg/kg PO q24h",
                "dosage_ja": "1-2 mg/kg 経口 24時間毎",
                "notes": "Good safety profile",
                "notes_ja": "良好な安全性プロファイル",
            },
            "cat": {
                "safe": True,
                "dosage": "1-2 mg/kg PO/SC q24h (up to 3 days for acute; up to 6 days PO)",
                "dosage_ja": "1-2 mg/kg 経口/皮下 24時間毎（急性：最大3日; 経口：最大6日）",
                "notes": "One of the few NSAIDs with cat labeling. Limited duration.",
                "notes_ja": "猫に表示のある数少ないNSAIDの一つ。使用期間は限定的。",
            },
        },
        "side_effects": ["GI upset (milder than non-selective)", "injection site reactions"],
        "side_effects_ja": ["消化器症状（非選択的NSAIDより軽度）", "注射部位反応"],
        "contraindications": "Renal disease. Dehydration. Not for long-term use in cats.",
        "contraindications_ja": "腎疾患。脱水。猫の長期使用は不可。",
    },
    {
        "id": "phenylbutazone",
        "name": "Phenylbutazone",
        "name_ja": "フェニルブタゾン",
        "category": "nsaids",
        "mechanism": "Non-selective COX inhibitor; potent anti-inflammatory primarily used in horses.",
        "mechanism_ja": "非選択的COX阻害薬。主に馬に使用される強力な抗炎症薬。",
        "species_info": {
            "horse": {
                "safe": True,
                "dosage": "2.2-4.4 mg/kg PO/IV q12h (reduce to lowest effective dose)",
                "dosage_ja": "2.2-4.4 mg/kg 経口/静注 12時間毎（最小有効用量に減量）",
                "notes": "Mainstay equine NSAID. Risk of GI ulceration, right dorsal colitis. Do NOT exceed recommended dose.",
                "notes_ja": "馬の主要NSAID。消化管潰瘍・右背側結腸炎のリスク。推奨用量を超えないこと。",
            },
            "dog": {
                "safe": True,
                "dosage": "3-5 mg/kg PO q8h (short-term only)",
                "dosage_ja": "3-5 mg/kg 経口 8時間毎（短期のみ）",
                "notes": "Rarely used in dogs; safer alternatives available",
                "notes_ja": "犬ではほとんど使用されない。より安全な代替薬あり。",
            },
            "cat": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "CONTRAINDICATED - very long half-life, high toxicity",
                "notes_ja": "【禁忌】非常に長い半減期、高い毒性",
            },
        },
        "side_effects": [
            "GI ulceration",
            "right dorsal colitis (horses)",
            "renal papillary necrosis",
            "bone marrow suppression",
        ],
        "side_effects_ja": ["消化管潰瘍", "右背側結腸炎（馬）", "腎乳頭壊死", "骨髄抑制"],
        "contraindications": "Cats. Renal disease. GI ulceration. Concurrent NSAID/steroid use.",
        "contraindications_ja": "猫。腎疾患。消化管潰瘍。NSAID/ステロイドとの併用。",
    },
    {
        "id": "flunixin",
        "name": "Flunixin Meglumine (Banamine)",
        "name_ja": "フルニキシンメグルミン（バナミン）",
        "category": "nsaids",
        "mechanism": "Non-selective COX inhibitor; potent anti-inflammatory and analgesic, especially for visceral pain.",
        "mechanism_ja": "非選択的COX阻害薬。内臓痛に特に有効な強力な抗炎症・鎮痛薬。",
        "species_info": {
            "horse": {
                "safe": True,
                "dosage": "1.1 mg/kg IV q12-24h (max 5 days)",
                "dosage_ja": "1.1 mg/kg 静注 12-24時間毎（最大5日）",
                "notes": "Drug of choice for colic pain. DO NOT give IM (causes clostridial myonecrosis).",
                "notes_ja": "疝痛の第一選択薬。筋注は不可（クロストリジウム筋壊死の原因）。",
            },
            "dog": {
                "safe": True,
                "dosage": "1.1 mg/kg IV single dose",
                "dosage_ja": "1.1 mg/kg 静注 単回投与",
                "notes": "Very limited use in dogs. Single dose only.",
                "notes_ja": "犬での使用は非常に限定的。単回投与のみ。",
            },
            "cat": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "CONTRAINDICATED - renal toxicity",
                "notes_ja": "【禁忌】腎毒性",
            },
        },
        "side_effects": ["GI ulceration", "renal toxicity", "clostridial myonecrosis (if given IM in horses)"],
        "side_effects_ja": ["消化管潰瘍", "腎毒性", "クロストリジウム筋壊死（馬への筋注時）"],
        "contraindications": "Cats. IM injection in horses. Renal disease.",
        "contraindications_ja": "猫。馬への筋肉注射。腎疾患。",
    },
    # ══════════════════════════════════════════════════════════════════════
    # 鎮痛薬 (Analgesics)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": "tramadol",
        "name": "Tramadol",
        "name_ja": "トラマドール",
        "category": "analgesics",
        "mechanism": "Weak mu-opioid receptor agonist; also inhibits serotonin and norepinephrine reuptake.",
        "mechanism_ja": "弱いμオピオイド受容体作動薬。セロトニン・ノルエピネフリン再取り込みも阻害。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "2-5 mg/kg PO q8-12h",
                "dosage_ja": "2-5 mg/kg 経口 8-12時間毎",
                "notes": "Limited analgesic efficacy in dogs (poor CYP2D6 metabolism). Serotonin syndrome risk.",
                "notes_ja": "犬での鎮痛効果は限定的（CYP2D6代謝が不良）。セロトニン症候群のリスク。",
            },
            "cat": {
                "safe": True,
                "dosage": "1-4 mg/kg PO q12h",
                "dosage_ja": "1-4 mg/kg 経口 12時間毎",
                "notes": "Better analgesic in cats than dogs (better M1 metabolite production)",
                "notes_ja": "猫は犬より良好な鎮痛効果（M1代謝物産生が良好）",
            },
            "horse": {
                "safe": True,
                "dosage": "2-5 mg/kg PO q12h",
                "dosage_ja": "2-5 mg/kg 経口 12時間毎",
                "notes": "Variable efficacy; used as adjunct analgesic",
                "notes_ja": "効果は不定。補助的鎮痛薬として使用。",
            },
            "rabbit": {
                "safe": True,
                "dosage": "5-15 mg/kg PO q8-12h",
                "dosage_ja": "5-15 mg/kg 経口 8-12時間毎",
                "notes": "Used for moderate pain",
                "notes_ja": "中等度の疼痛に使用",
            },
            "ferret": {
                "safe": True,
                "dosage": "5-10 mg/kg PO q12-24h",
                "dosage_ja": "5-10 mg/kg 経口 12-24時間毎",
                "notes": "Adjunct analgesic for ferrets",
                "notes_ja": "フェレットの補助的鎮痛薬",
            },
        },
        "side_effects": ["sedation", "GI upset", "serotonin syndrome", "seizures at high doses"],
        "side_effects_ja": ["鎮静", "消化器症状", "セロトニン症候群", "高用量での痙攣"],
        "contraindications": "Concurrent SSRI/MAOI use (serotonin syndrome risk). Seizure history.",
        "contraindications_ja": "SSRI/MAO阻害薬との併用（セロトニン症候群リスク）。痙攣既往歴。",
    },
    {
        "id": "gabapentin",
        "name": "Gabapentin",
        "name_ja": "ガバペンチン",
        "category": "analgesics",
        "mechanism": "GABA analog; binds alpha-2-delta subunit of voltage-gated calcium channels. Neuropathic pain relief.",
        "mechanism_ja": "GABA類似体。電位依存性カルシウムチャネルのα2δサブユニットに結合。神経障害性疼痛に有効。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "5-10 mg/kg PO q8-12h (pain); 10-20 mg/kg q8h (seizures)",
                "dosage_ja": "5-10 mg/kg 経口 8-12時間毎（疼痛）; 10-20 mg/kg 8時間毎（痙攣）",
                "notes": "Increasingly popular for chronic pain. Mild sedation.",
                "notes_ja": "慢性疼痛管理に使用増加中。軽度鎮静作用。",
            },
            "cat": {
                "safe": True,
                "dosage": "3-10 mg/kg PO q8-12h",
                "dosage_ja": "3-10 mg/kg 経口 8-12時間毎",
                "notes": "Excellent for anxiety/stress reduction pre-visit. Also for chronic pain.",
                "notes_ja": "来院前の不安・ストレス軽減に優れる。慢性疼痛にも有効。",
            },
            "horse": {
                "safe": True,
                "dosage": "2.5-5 mg/kg PO q8-12h",
                "dosage_ja": "2.5-5 mg/kg 経口 8-12時間毎",
                "notes": "Used for neuropathic pain, headshaking",
                "notes_ja": "神経障害性疼痛・ヘッドシェイキングに使用",
            },
            "rabbit": {
                "safe": True,
                "dosage": "5 mg/kg PO q8-12h",
                "dosage_ja": "5 mg/kg 経口 8-12時間毎",
                "notes": "Safe for pain management in rabbits",
                "notes_ja": "ウサギの疼痛管理に安全",
            },
            "bird": {
                "safe": True,
                "dosage": "10-15 mg/kg PO q8-12h",
                "dosage_ja": "10-15 mg/kg 経口 8-12時間毎",
                "notes": "Used for chronic pain in birds",
                "notes_ja": "鳥類の慢性疼痛に使用",
            },
        },
        "side_effects": ["sedation", "ataxia", "withdrawal syndrome if stopped abruptly"],
        "side_effects_ja": ["鎮静", "運動失調", "急な中止で離脱症状"],
        "contraindications": "Renal dose adjustment needed. Avoid abrupt discontinuation (taper).",
        "contraindications_ja": "腎用量調整が必要。急な中止は回避（漸減）。",
    },
    {
        "id": "buprenorphine",
        "name": "Buprenorphine",
        "name_ja": "ブプレノルフィン",
        "category": "analgesics",
        "mechanism": "Partial mu-opioid agonist; provides moderate to good analgesia with ceiling effect.",
        "mechanism_ja": "部分的μオピオイド作動薬。天井効果のある中等度～良好な鎮痛作用。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "0.01-0.03 mg/kg IV/IM/SC q6-8h; sustained release: 0.12 mg/kg SC q72h",
                "dosage_ja": "0.01-0.03 mg/kg 静注/筋注/皮下 6-8時間毎; 持続型: 0.12 mg/kg 皮下 72時間毎",
                "notes": "Good for moderate pain. Long-acting formulation available.",
                "notes_ja": "中等度の疼痛に有効。長時間作用型製剤あり。",
            },
            "cat": {
                "safe": True,
                "dosage": "0.01-0.03 mg/kg IV/IM q6-8h; 0.01-0.03 mg/kg OTM q6-8h",
                "dosage_ja": "0.01-0.03 mg/kg 静注/筋注 6-8時間毎; 0.01-0.03 mg/kg 口腔粘膜 6-8時間毎",
                "notes": "GOLD STANDARD analgesic for cats. Excellent OTM (oral transmucosal) absorption in cats.",
                "notes_ja": "猫の鎮痛薬のゴールドスタンダード。猫では口腔粘膜吸収が優れている。",
            },
            "horse": {
                "safe": True,
                "dosage": "0.005-0.01 mg/kg IV q6-12h",
                "dosage_ja": "0.005-0.01 mg/kg 静注 6-12時間毎",
                "notes": "Less commonly used in horses; can cause excitement",
                "notes_ja": "馬では使用頻度が低い。興奮を引き起こすことがある。",
            },
            "rabbit": {
                "safe": True,
                "dosage": "0.03-0.05 mg/kg SC/IV q6-8h",
                "dosage_ja": "0.03-0.05 mg/kg 皮下/静注 6-8時間毎",
                "notes": "Excellent analgesic for rabbits",
                "notes_ja": "ウサギに優れた鎮痛薬",
            },
            "bird": {
                "safe": True,
                "dosage": "0.05-0.1 mg/kg IM q8-12h",
                "dosage_ja": "0.05-0.1 mg/kg 筋注 8-12時間毎",
                "notes": "Variable efficacy among bird species",
                "notes_ja": "鳥種による効果の差が大きい",
            },
            "reptile": {
                "safe": True,
                "dosage": "0.02-0.1 mg/kg IM/SC q24h",
                "dosage_ja": "0.02-0.1 mg/kg 筋注/皮下 24時間毎",
                "notes": "Limited efficacy data in reptiles",
                "notes_ja": "爬虫類での有効性データは限定的",
            },
        },
        "side_effects": ["sedation", "respiratory depression (minimal)", "dysphoria", "decreased GI motility"],
        "side_effects_ja": ["鎮静", "呼吸抑制（軽度）", "不快感", "消化管運動低下"],
        "contraindications": "Concurrent full mu-agonist opioids (may reduce their effect).",
        "contraindications_ja": "完全μ作動薬オピオイドとの併用（効果を減弱させる可能性）。",
    },
    {
        "id": "butorphanol",
        "name": "Butorphanol",
        "name_ja": "ブトルファノール",
        "category": "analgesics",
        "mechanism": "Kappa-agonist, mu-antagonist opioid. Mild to moderate analgesia, good sedation and antitussive effect.",
        "mechanism_ja": "κ作動薬・μ拮抗薬オピオイド。軽度～中等度の鎮痛作用、良好な鎮静・鎮咳作用。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "0.1-0.5 mg/kg IV/IM/SC q2-4h",
                "dosage_ja": "0.1-0.5 mg/kg 静注/筋注/皮下 2-4時間毎",
                "notes": "Short-acting. Good for visceral pain. Strong sedation in combo with alpha-2 agonists.",
                "notes_ja": "短時間作用。内臓痛に有効。α2作動薬との併用で強い鎮静。",
            },
            "cat": {
                "safe": True,
                "dosage": "0.1-0.4 mg/kg IV/IM/SC q2-4h",
                "dosage_ja": "0.1-0.4 mg/kg 静注/筋注/皮下 2-4時間毎",
                "notes": "Commonly used for procedural sedation",
                "notes_ja": "処置時の鎮静に一般的に使用",
            },
            "horse": {
                "safe": True,
                "dosage": "0.01-0.1 mg/kg IV",
                "dosage_ja": "0.01-0.1 mg/kg 静注",
                "notes": "Commonly combined with detomidine for standing sedation",
                "notes_ja": "デトミジンと併用して立位鎮静に一般的に使用",
            },
            "rabbit": {
                "safe": True,
                "dosage": "0.1-0.5 mg/kg IV/IM/SC q4h",
                "dosage_ja": "0.1-0.5 mg/kg 静注/筋注/皮下 4時間毎",
                "notes": "Mild analgesia only; often used for sedation",
                "notes_ja": "軽度の鎮痛のみ。鎮静目的で使用されることが多い。",
            },
            "bird": {
                "safe": True,
                "dosage": "1-4 mg/kg IM q2-4h",
                "dosage_ja": "1-4 mg/kg 筋注 2-4時間毎",
                "notes": "Standard analgesic/sedative for birds",
                "notes_ja": "鳥類の標準的鎮痛・鎮静薬",
            },
            "reptile": {
                "safe": True,
                "dosage": "0.4-2 mg/kg IM q12-24h",
                "dosage_ja": "0.4-2 mg/kg 筋注 12-24時間毎",
                "notes": "Used for analgesia in reptiles",
                "notes_ja": "爬虫類の鎮痛に使用",
            },
        },
        "side_effects": ["sedation", "respiratory depression", "decreased GI motility"],
        "side_effects_ja": ["鎮静", "呼吸抑制", "消化管運動低下"],
        "contraindications": "Head trauma (increases intracranial pressure).",
        "contraindications_ja": "頭部外傷（頭蓋内圧上昇）。",
    },
    # ══════════════════════════════════════════════════════════════════════
    # 麻酔薬 (Anesthetics)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": "ketamine",
        "name": "Ketamine",
        "name_ja": "ケタミン",
        "category": "anesthetics",
        "mechanism": "NMDA receptor antagonist; produces dissociative anesthesia with analgesia.",
        "mechanism_ja": "NMDA受容体拮抗薬。鎮痛作用を伴う解離性麻酔を引き起こす。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "5-10 mg/kg IV (induction); 2-10 mcg/kg/min CRI (adjunct)",
                "dosage_ja": "5-10 mg/kg 静注（導入）; 2-10 mcg/kg/分 CRI（補助）",
                "notes": "Always combine with benzodiazepine or alpha-2 agonist",
                "notes_ja": "常にベンゾジアゼピンまたはα2作動薬と併用",
            },
            "cat": {
                "safe": True,
                "dosage": "5-10 mg/kg IM (with midazolam); 2-5 mg/kg IV",
                "dosage_ja": "5-10 mg/kg 筋注（ミダゾラムと）; 2-5 mg/kg 静注",
                "notes": "Widely used for cat sedation/anesthesia combinations",
                "notes_ja": "猫の鎮静・麻酔の組み合わせに広く使用",
            },
            "horse": {
                "safe": True,
                "dosage": "2.2 mg/kg IV (with xylazine for induction)",
                "dosage_ja": "2.2 mg/kg 静注（キシラジンと導入）",
                "notes": "Standard field anesthesia induction agent for horses",
                "notes_ja": "馬のフィールド麻酔導入の標準薬",
            },
            "rabbit": {
                "safe": True,
                "dosage": "10-35 mg/kg IM (with medetomidine); 5-10 mg/kg IV",
                "dosage_ja": "10-35 mg/kg 筋注（メデトミジンと）; 5-10 mg/kg 静注",
                "notes": "Common in rabbit anesthesia protocols",
                "notes_ja": "ウサギの麻酔プロトコールで一般的",
            },
            "bird": {
                "safe": True,
                "dosage": "10-30 mg/kg IM",
                "dosage_ja": "10-30 mg/kg 筋注",
                "notes": "Used for restraint and minor procedures",
                "notes_ja": "保定と軽度の処置に使用",
            },
            "reptile": {
                "safe": True,
                "dosage": "20-80 mg/kg IM",
                "dosage_ja": "20-80 mg/kg 筋注",
                "notes": "Commonly used; slow onset in reptiles",
                "notes_ja": "一般的に使用される。爬虫類では発現が遅い。",
            },
        },
        "side_effects": [
            "increased intracranial pressure",
            "apneustic breathing",
            "hypersalivation",
            "muscle rigidity",
        ],
        "side_effects_ja": ["頭蓋内圧上昇", "持続性吸気", "流涎", "筋硬直"],
        "contraindications": "Head trauma. Hepatic disease (cats). Never use alone (combine with sedative).",
        "contraindications_ja": "頭部外傷。肝疾患（猫）。単独使用不可（鎮静薬と併用）。",
    },
    {
        "id": "propofol",
        "name": "Propofol",
        "name_ja": "プロポフォール",
        "category": "anesthetics",
        "mechanism": "GABA-A receptor agonist; ultra-short-acting IV anesthetic for induction and short procedures.",
        "mechanism_ja": "GABA-A受容体作動薬。導入および短時間処置用の超短時間作用型静脈麻酔薬。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "4-6 mg/kg IV to effect",
                "dosage_ja": "4-6 mg/kg 静注 効果が出るまで",
                "notes": "Gold standard IV induction agent. Give slowly to effect.",
                "notes_ja": "静脈麻酔導入のゴールドスタンダード。効果が出るまでゆっくり投与。",
            },
            "cat": {
                "safe": True,
                "dosage": "4-8 mg/kg IV to effect",
                "dosage_ja": "4-8 mg/kg 静注 効果が出るまで",
                "notes": "Avoid repeated/prolonged use (Heinz body formation, oxidative injury to RBCs)",
                "notes_ja": "反復・長時間使用は回避（ハインツ小体形成、赤血球の酸化障害）",
            },
            "horse": {
                "safe": True,
                "dosage": "2 mg/kg IV (after sedation)",
                "dosage_ja": "2 mg/kg 静注（鎮静後）",
                "notes": "Used for induction after appropriate sedation",
                "notes_ja": "適切な鎮静後の導入に使用",
            },
            "rabbit": {
                "safe": True,
                "dosage": "6-10 mg/kg IV to effect",
                "dosage_ja": "6-10 mg/kg 静注 効果が出るまで",
                "notes": "Apnea risk - have intubation/O2 ready",
                "notes_ja": "無呼吸リスク - 挿管/O2の準備を",
            },
            "bird": {
                "safe": True,
                "dosage": "3-5 mg/kg IV/IO",
                "dosage_ja": "3-5 mg/kg 静注/骨内",
                "notes": "Good for avian induction; rapid recovery",
                "notes_ja": "鳥類の導入に良好。迅速な回復。",
            },
        },
        "side_effects": ["apnea", "hypotension", "pain on injection", "Heinz body anemia (cats, prolonged)"],
        "side_effects_ja": ["無呼吸", "低血圧", "注射時疼痛", "ハインツ小体貧血（猫、長時間投与時）"],
        "contraindications": "Hypovolemia. No IV access. Cats: avoid prolonged infusion.",
        "contraindications_ja": "循環血液量減少。静脈アクセスなし。猫: 長時間持続投与は回避。",
    },
    {
        "id": "alfaxalone",
        "name": "Alfaxalone (Alfaxan)",
        "name_ja": "アルファキサロン（アルファキサン）",
        "category": "anesthetics",
        "mechanism": "Neuroactive steroid; GABA-A receptor modulator. IV anesthetic for induction and maintenance.",
        "mechanism_ja": "神経活性ステロイド。GABA-A受容体調節薬。導入と維持の静脈麻酔薬。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "1-3 mg/kg IV to effect",
                "dosage_ja": "1-3 mg/kg 静注 効果が出るまで",
                "notes": "Good alternative to propofol. Licensed for dogs.",
                "notes_ja": "プロポフォールの良い代替薬。犬に認可済み。",
            },
            "cat": {
                "safe": True,
                "dosage": "2-5 mg/kg IV to effect; 5 mg/kg IM (sedation)",
                "dosage_ja": "2-5 mg/kg 静注 効果が出るまで; 5 mg/kg 筋注（鎮静）",
                "notes": "Safer than propofol for cats; can be given IM for sedation",
                "notes_ja": "猫にはプロポフォールより安全。鎮静目的で筋注も可。",
            },
            "rabbit": {
                "safe": True,
                "dosage": "2-3 mg/kg IV; 6-12 mg/kg IM",
                "dosage_ja": "2-3 mg/kg 静注; 6-12 mg/kg 筋注",
                "notes": "Excellent for rabbit induction",
                "notes_ja": "ウサギの導入に優れている",
            },
            "bird": {
                "safe": True,
                "dosage": "5-10 mg/kg IM; 3-5 mg/kg IV",
                "dosage_ja": "5-10 mg/kg 筋注; 3-5 mg/kg 静注",
                "notes": "Can be given IM which is advantageous for birds",
                "notes_ja": "筋注可能なのが鳥類に有利",
            },
            "reptile": {
                "safe": True,
                "dosage": "5-20 mg/kg IM/IV",
                "dosage_ja": "5-20 mg/kg 筋注/静注",
                "notes": "Useful in reptile anesthesia",
                "notes_ja": "爬虫類の麻酔に有用",
            },
        },
        "side_effects": ["apnea", "hypotension (less than propofol)"],
        "side_effects_ja": ["無呼吸", "低血圧（プロポフォールより軽度）"],
        "contraindications": "Same as general anesthetics. Hypovolemia.",
        "contraindications_ja": "全身麻酔薬と同様の注意事項。循環血液量減少。",
    },
    # ══════════════════════════════════════════════════════════════════════
    # 副腎皮質ステロイド (Corticosteroids)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": "prednisolone",
        "name": "Prednisolone",
        "name_ja": "プレドニゾロン",
        "category": "corticosteroids",
        "mechanism": "Intermediate-acting glucocorticoid; anti-inflammatory and immunosuppressive.",
        "mechanism_ja": "中間作用型糖質コルチコイド。抗炎症・免疫抑制作用。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "0.5-1 mg/kg PO q12-24h (anti-inflammatory); 2-4 mg/kg q12h (immunosuppressive)",
                "dosage_ja": "0.5-1 mg/kg 経口 12-24時間毎（抗炎症）; 2-4 mg/kg 12時間毎（免疫抑制）",
                "notes": "Taper gradually to avoid adrenal crisis. Many side effects with chronic use.",
                "notes_ja": "副腎クリーゼ回避のため漸減。長期使用で多くの副作用。",
            },
            "cat": {
                "safe": True,
                "dosage": "1-2 mg/kg PO q12-24h (anti-inflammatory); 2-4 mg/kg q12h (immunosuppressive)",
                "dosage_ja": "1-2 mg/kg 経口 12-24時間毎（抗炎症）; 2-4 mg/kg 12時間毎（免疫抑制）",
                "notes": "Use prednisolone NOT prednisone in cats (cats cannot convert prednisone efficiently).",
                "notes_ja": "猫にはプレドニゾロンを使用（猫はプレドニゾンを効率的に変換できない）。",
            },
            "horse": {
                "safe": True,
                "dosage": "0.5-1 mg/kg PO/IM q24h",
                "dosage_ja": "0.5-1 mg/kg 経口/筋注 24時間毎",
                "notes": "Risk of laminitis with systemic steroids in horses",
                "notes_ja": "馬では全身性ステロイドで蹄葉炎のリスク",
            },
            "rabbit": {
                "safe": True,
                "dosage": "0.5-2 mg/kg PO q12-24h",
                "dosage_ja": "0.5-2 mg/kg 経口 12-24時間毎",
                "notes": "Use with caution; immunosuppression increases pasteurellosis risk",
                "notes_ja": "注意して使用。免疫抑制でパスツレラ症リスク増加。",
            },
            "ferret": {
                "safe": True,
                "dosage": "0.5-2.5 mg/kg PO q12-24h",
                "dosage_ja": "0.5-2.5 mg/kg 経口 12-24時間毎",
                "notes": "Used for lymphoma, IBD, insulinoma crisis",
                "notes_ja": "リンパ腫・IBD・インスリノーマクリーゼに使用",
            },
            "bird": {
                "safe": True,
                "dosage": "0.5-1 mg/kg PO/IM q12h",
                "dosage_ja": "0.5-1 mg/kg 経口/筋注 12時間毎",
                "notes": "Use with great caution - immunosuppression is dangerous in birds",
                "notes_ja": "細心の注意を払って使用。鳥類の免疫抑制は危険。",
            },
        },
        "side_effects": [
            "PU/PD",
            "polyphagia",
            "muscle wasting",
            "hepatopathy",
            "immunosuppression",
            "iatrogenic Cushing's",
        ],
        "side_effects_ja": ["多飲多尿", "多食", "筋萎縮", "肝障害", "免疫抑制", "医原性クッシング症候群"],
        "contraindications": "Active infections. GI ulceration. Diabetes. Concurrent NSAID use.",
        "contraindications_ja": "活動性感染症。消化管潰瘍。糖尿病。NSAIDとの併用。",
    },
    {
        "id": "dexamethasone",
        "name": "Dexamethasone",
        "name_ja": "デキサメタゾン",
        "category": "corticosteroids",
        "mechanism": "Long-acting, potent glucocorticoid (25x potency of cortisol). Anti-inflammatory and immunosuppressive.",
        "mechanism_ja": "長時間作用型の強力な糖質コルチコイド（コルチゾールの25倍の力価）。抗炎症・免疫抑制作用。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "0.05-0.2 mg/kg IV/IM/PO q24h (anti-inflammatory)",
                "dosage_ja": "0.05-0.2 mg/kg 静注/筋注/経口 24時間毎（抗炎症）",
                "notes": "Very potent; use lowest effective dose. Not for long-term use.",
                "notes_ja": "非常に強力。最小有効用量を使用。長期使用は不可。",
            },
            "cat": {
                "safe": True,
                "dosage": "0.1-0.5 mg/kg IV/IM/PO q24h",
                "dosage_ja": "0.1-0.5 mg/kg 静注/筋注/経口 24時間毎",
                "notes": "Risk of diabetes with repeated injections",
                "notes_ja": "反復注射で糖尿病のリスク",
            },
            "horse": {
                "safe": True,
                "dosage": "0.02-0.2 mg/kg IV/IM q24h",
                "dosage_ja": "0.02-0.2 mg/kg 静注/筋注 24時間毎",
                "notes": "LAMINITIS RISK. Use with extreme caution.",
                "notes_ja": "蹄葉炎リスク。細心の注意を払って使用。",
            },
            "bird": {
                "safe": True,
                "dosage": "2-4 mg/kg IM once (emergency only)",
                "dosage_ja": "2-4 mg/kg 筋注 単回（緊急時のみ）",
                "notes": "Emergency use only (shock, head trauma). Immunosuppression risk.",
                "notes_ja": "緊急時のみ使用（ショック・頭部外傷）。免疫抑制リスク。",
            },
        },
        "side_effects": ["more pronounced than prednisolone due to potency", "laminitis (horses)", "diabetes (cats)"],
        "side_effects_ja": ["プレドニゾロンより力価が強いため副作用も顕著", "蹄葉炎（馬）", "糖尿病（猫）"],
        "contraindications": "Horses (laminitis risk). Diabetes. Active infections.",
        "contraindications_ja": "馬（蹄葉炎リスク）。糖尿病。活動性感染症。",
    },
    {
        "id": "budesonide",
        "name": "Budesonide",
        "name_ja": "ブデソニド",
        "category": "corticosteroids",
        "mechanism": "Locally-acting glucocorticoid with high first-pass hepatic metabolism; less systemic effects.",
        "mechanism_ja": "肝初回通過代謝が高い局所作用型糖質コルチコイド。全身性副作用が少ない。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "1-3 mg/dog PO q24h",
                "dosage_ja": "1-3 mg/頭 経口 24時間毎",
                "notes": "Used for IBD to minimize systemic steroid effects. Not truly topical in GI - some systemic absorption.",
                "notes_ja": "IBDの全身性ステロイド副作用軽減に使用。消化管での局所作用は完全でなく一部全身吸収あり。",
            },
            "cat": {
                "safe": True,
                "dosage": "0.5-1 mg/cat PO q24h",
                "dosage_ja": "0.5-1 mg/頭 経口 24時間毎",
                "notes": "Used for IBD in cats",
                "notes_ja": "猫のIBDに使用",
            },
        },
        "side_effects": ["less than systemic steroids but still possible PU/PD, appetite increase"],
        "side_effects_ja": ["全身性ステロイドより少ないが多飲多尿・食欲増加の可能性あり"],
        "contraindications": "Hepatic disease (may increase systemic exposure due to reduced first-pass metabolism).",
        "contraindications_ja": "肝疾患（初回通過代謝低下により全身曝露が増加する可能性）。",
    },
    # ══════════════════════════════════════════════════════════════════════
    # 消化器薬 (Gastrointestinal Drugs)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": "omeprazole",
        "name": "Omeprazole",
        "name_ja": "オメプラゾール",
        "category": "gi_drugs",
        "mechanism": "Proton pump inhibitor (PPI); irreversibly blocks H+/K+ ATPase in gastric parietal cells.",
        "mechanism_ja": "プロトンポンプ阻害薬（PPI）。胃壁細胞のH+/K+ ATPaseを不可逆的に阻害。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "1-2 mg/kg PO q12-24h",
                "dosage_ja": "1-2 mg/kg 経口 12-24時間毎",
                "notes": "Gold standard for GI ulcer treatment/prevention",
                "notes_ja": "消化管潰瘍の治療・予防のゴールドスタンダード",
            },
            "cat": {
                "safe": True,
                "dosage": "1 mg/kg PO q24h",
                "dosage_ja": "1 mg/kg 経口 24時間毎",
                "notes": "Effective acid suppression",
                "notes_ja": "効果的な酸分泌抑制",
            },
            "horse": {
                "safe": True,
                "dosage": "4 mg/kg PO q24h (GastroGard)",
                "dosage_ja": "4 mg/kg 経口 24時間毎（ガストロガード）",
                "notes": "Treatment of choice for equine gastric ulcer syndrome (EGUS)",
                "notes_ja": "馬胃潰瘍症候群（EGUS）の第一選択治療",
            },
            "ferret": {
                "safe": True,
                "dosage": "1-4 mg/kg PO q24h",
                "dosage_ja": "1-4 mg/kg 経口 24時間毎",
                "notes": "Used for Helicobacter-associated gastritis",
                "notes_ja": "ヘリコバクター関連胃炎に使用",
            },
        },
        "side_effects": ["generally well tolerated", "possible rebound acid hypersecretion on discontinuation"],
        "side_effects_ja": ["一般的に忍容性良好", "中止時に反跳性酸過分泌の可能性"],
        "contraindications": "None significant.",
        "contraindications_ja": "特になし。",
    },
    {
        "id": "famotidine",
        "name": "Famotidine",
        "name_ja": "ファモチジン",
        "category": "gi_drugs",
        "mechanism": "H2 receptor antagonist; reduces gastric acid secretion.",
        "mechanism_ja": "H2受容体拮抗薬。胃酸分泌を抑制する。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "0.5-1 mg/kg PO/IV q12-24h",
                "dosage_ja": "0.5-1 mg/kg 経口/静注 12-24時間毎",
                "notes": "Less potent than omeprazole but good for mild cases",
                "notes_ja": "オメプラゾールより弱いが軽症例に有効",
            },
            "cat": {
                "safe": True,
                "dosage": "0.5 mg/kg PO/IV q12-24h",
                "dosage_ja": "0.5 mg/kg 経口/静注 12-24時間毎",
                "notes": "Commonly used",
                "notes_ja": "一般的に使用",
            },
            "ferret": {
                "safe": True,
                "dosage": "0.25-0.5 mg/kg PO/SC q24h",
                "dosage_ja": "0.25-0.5 mg/kg 経口/皮下 24時間毎",
                "notes": "Safe for ferrets",
                "notes_ja": "フェレットに安全",
            },
        },
        "side_effects": ["generally well tolerated"],
        "side_effects_ja": ["一般的に忍容性良好"],
        "contraindications": "Renal dose adjustment may be needed.",
        "contraindications_ja": "腎用量調整が必要な場合がある。",
    },
    {
        "id": "sucralfate",
        "name": "Sucralfate",
        "name_ja": "スクラルファート",
        "category": "gi_drugs",
        "mechanism": "Mucosal protectant; forms a gel-like barrier over ulcerated mucosa in acidic environment.",
        "mechanism_ja": "粘膜保護薬。酸性環境で潰瘍粘膜上にゲル状バリアを形成する。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "0.5-1 g/dog PO q8-12h",
                "dosage_ja": "0.5-1 g/頭 経口 8-12時間毎",
                "notes": "Give on empty stomach, 1-2h before other medications",
                "notes_ja": "空腹時に投与。他の薬剤の1-2時間前。",
            },
            "cat": {
                "safe": True,
                "dosage": "0.25-0.5 g/cat PO q8-12h",
                "dosage_ja": "0.25-0.5 g/頭 経口 8-12時間毎",
                "notes": "May interfere with absorption of other drugs",
                "notes_ja": "他の薬剤の吸収を妨げる可能性",
            },
            "horse": {
                "safe": True,
                "dosage": "20-40 mg/kg PO q6-8h",
                "dosage_ja": "20-40 mg/kg 経口 6-8時間毎",
                "notes": "Used for gastric and colonic ulcers",
                "notes_ja": "胃潰瘍・結腸潰瘍に使用",
            },
            "ferret": {
                "safe": True,
                "dosage": "25-125 mg/ferret PO q8h",
                "dosage_ja": "25-125 mg/頭 経口 8時間毎",
                "notes": "Useful for gastric protection",
                "notes_ja": "胃粘膜保護に有用",
            },
        },
        "side_effects": ["constipation (aluminum content)", "drug interaction (reduces absorption of other drugs)"],
        "side_effects_ja": ["便秘（アルミニウム含有）", "薬物相互作用（他剤の吸収低下）"],
        "contraindications": "Give separately from other oral medications.",
        "contraindications_ja": "他の経口薬とは間隔を空けて投与。",
    },
    {
        "id": "metoclopramide",
        "name": "Metoclopramide",
        "name_ja": "メトクロプラミド",
        "category": "gi_drugs",
        "mechanism": "Dopamine D2 antagonist; prokinetic and antiemetic. Enhances upper GI motility.",
        "mechanism_ja": "ドパミンD2拮抗薬。消化管運動促進・制吐作用。上部消化管の運動性を亢進。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "0.2-0.5 mg/kg PO/SC q6-8h; 1-2 mg/kg/day CRI",
                "dosage_ja": "0.2-0.5 mg/kg 経口/皮下 6-8時間毎; 1-2 mg/kg/日 CRI",
                "notes": "Crosses blood-brain barrier; may cause extrapyramidal signs",
                "notes_ja": "血液脳関門を通過。錐体外路症状を起こすことがある。",
            },
            "cat": {
                "safe": True,
                "dosage": "0.2-0.4 mg/kg PO/SC q6-8h",
                "dosage_ja": "0.2-0.4 mg/kg 経口/皮下 6-8時間毎",
                "notes": "Used for gastric motility disorders",
                "notes_ja": "胃運動障害に使用",
            },
            "rabbit": {
                "safe": True,
                "dosage": "0.5-1 mg/kg PO/SC q6-8h",
                "dosage_ja": "0.5-1 mg/kg 経口/皮下 6-8時間毎",
                "notes": "Useful for GI stasis in rabbits",
                "notes_ja": "ウサギの消化管うっ滞に有用",
            },
            "bird": {
                "safe": True,
                "dosage": "0.5-1 mg/kg PO/IM q8-12h",
                "dosage_ja": "0.5-1 mg/kg 経口/筋注 8-12時間毎",
                "notes": "Used for crop stasis",
                "notes_ja": "素嚢うっ滞に使用",
            },
        },
        "side_effects": ["extrapyramidal signs", "behavior changes", "restlessness"],
        "side_effects_ja": ["錐体外路症状", "行動変化", "不穏"],
        "contraindications": "GI obstruction. Epilepsy. Pheochromocytoma.",
        "contraindications_ja": "消化管閉塞。てんかん。褐色細胞腫。",
    },
    {
        "id": "maropitant",
        "name": "Maropitant (Cerenia)",
        "name_ja": "マロピタント（セレニア）",
        "category": "antiemetics",
        "mechanism": "NK1 receptor antagonist; blocks substance P at the vomiting center. Also provides visceral analgesia. Substance P/NK1-R signaling is involved in airway inflammation and the cough reflex, supporting an off-label antitussive use in canine chronic bronchitis.",
        "mechanism_ja": "NK1受容体拮抗薬。嘔吐中枢のサブスタンスPを遮断。内臓鎮痛作用も持つ。サブスタンスP/NK1-Rシグナルは気道炎症と咳反射に関与しており、犬の慢性気管支炎に対する適応外の鎮咳用途を支持する。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Antiemetic: 1 mg/kg SC q24h or 2 mg/kg PO q24h × up to 5 days. Motion sickness: 8 mg/kg PO q24h × up to 2 days. Antitussive (off-label, chronic bronchitis): 2 mg/kg PO q48h (every other day, EOD) × 14+ days — reduces cough frequency and severity but does not reduce underlying airway inflammation, so not a substitute for anti-inflammatory therapy.",
                "dosage_ja": "制吐：1 mg/kg 皮下 q24h または 2 mg/kg 経口 q24h、最長5日間。乗り物酔い：8 mg/kg 経口 q24h、最長2日間。鎮咳（適応外、慢性気管支炎）：2 mg/kg 経口 q48h（隔日投与・EOD）×14日以上—咳の頻度・重症度を低減するが気道炎症は改善しないため、抗炎症療法の代替にはならない。",
                "notes": "Best antiemetic for dogs. Antitussive evidence: Grobman & Reinero JVIM 2016 (n=8 chronic bronchitis dogs, 2 mg/kg PO EOD × 14d significantly reduced cough frequency and severity). Use as adjunct to glucocorticoid/bronchodilator therapy, not monotherapy. SC injection stings (refrigerate to reduce). Consider concurrent anti-inflammatory (prednisone) since maropitant masks cough but does not address inflammation.",
                "notes_ja": "犬の最良の制吐薬。鎮咳エビデンス：Grobman & Reinero JVIM 2016（慢性気管支炎犬n=8、2 mg/kg PO EOD ×14日で咳頻度・重症度が有意に低下）。グルココルチコイド・気管支拡張薬の補助として使用、単剤療法は不可。皮下注射は刺痛あり（冷蔵で軽減）。マロピタントは咳を抑えるが炎症は治療しないため、併用抗炎症薬（プレドニゾロン）を考慮。",
            },
            "cat": {
                "safe": True,
                "dosage": "1 mg/kg SC q24h",
                "dosage_ja": "1 mg/kg 皮下 24時間毎",
                "notes": "Licensed for cats. Very effective antiemetic.",
                "notes_ja": "猫に認可済み。非常に有効な制吐薬。",
            },
            "ferret": {
                "safe": True,
                "dosage": "1 mg/kg SC q24h",
                "dosage_ja": "1 mg/kg 皮下 24時間毎",
                "notes": "Off-label but effective",
                "notes_ja": "適応外だが有効",
            },
        },
        "side_effects": ["pain at injection site", "hypotension (rare, IV)", "diarrhea"],
        "side_effects_ja": ["注射部位の痛み", "低血圧（まれ、静注時）", "下痢"],
        "contraindications": "Not studied in very young animals (FDA label: ≥7 weeks for SC, ≥16 weeks for PO motion sickness). Use caution with hepatic disease (hepatic metabolism via CYP450 2D15 + 3A12). Antitussive use is off-label and should not replace anti-inflammatory treatment of underlying airway disease.",
        "contraindications_ja": "非常に若い動物では未検討（FDAラベル：皮下7週齢以上、経口乗り物酔い16週齢以上）。肝疾患では注意して使用（CYP450 2D15 + 3A12による肝代謝）。鎮咳用途は適応外であり、原因気道疾患の抗炎症治療の代替としない。",
    },
    {
        "id": "ondansetron",
        "name": "Ondansetron",
        "name_ja": "オンダンセトロン",
        "category": "antiemetics",
        "mechanism": "5-HT3 receptor antagonist; blocks serotonin at the chemoreceptor trigger zone.",
        "mechanism_ja": "5-HT3受容体拮抗薬。化学受容器引金帯のセロトニンを遮断する。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "0.1-1 mg/kg IV/PO q8-12h",
                "dosage_ja": "0.1-1 mg/kg 静注/経口 8-12時間毎",
                "notes": "Alternative antiemetic to maropitant",
                "notes_ja": "マロピタントの代替制吐薬",
            },
            "cat": {
                "safe": True,
                "dosage": "0.1-1 mg/kg IV/PO q8-12h",
                "dosage_ja": "0.1-1 mg/kg 静注/経口 8-12時間毎",
                "notes": "Useful when maropitant insufficient",
                "notes_ja": "マロピタントが不十分な場合に有用",
            },
            "ferret": {
                "safe": True,
                "dosage": "0.5-1 mg/kg IV/PO q12h",
                "dosage_ja": "0.5-1 mg/kg 静注/経口 12時間毎",
                "notes": "Alternative antiemetic for ferrets",
                "notes_ja": "フェレットの代替制吐薬",
            },
        },
        "side_effects": ["constipation", "headache"],
        "side_effects_ja": ["便秘", "頭痛"],
        "contraindications": "None significant.",
        "contraindications_ja": "特になし。",
    },
    {
        "id": "lactulose",
        "name": "Lactulose",
        "name_ja": "ラクツロース",
        "category": "gi_drugs",
        "mechanism": "Osmotic laxative; draws water into the colon. Also reduces ammonia absorption (hepatic encephalopathy).",
        "mechanism_ja": "浸透圧性下剤。結腸に水分を引き込む。アンモニア吸収も低減（肝性脳症）。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "0.5-1 mL/kg PO q8-12h",
                "dosage_ja": "0.5-1 mL/kg 経口 8-12時間毎",
                "notes": "Used for constipation and hepatic encephalopathy",
                "notes_ja": "便秘・肝性脳症に使用",
            },
            "cat": {
                "safe": True,
                "dosage": "0.5 mL/kg PO q8-12h",
                "dosage_ja": "0.5 mL/kg 経口 8-12時間毎",
                "notes": "Common for megacolon/constipation in cats",
                "notes_ja": "猫の巨大結腸症・便秘に一般的",
            },
            "rabbit": {
                "safe": True,
                "dosage": "0.5 mL/kg PO q12h",
                "dosage_ja": "0.5 mL/kg 経口 12時間毎",
                "notes": "Use with caution; monitor hydration",
                "notes_ja": "注意して使用。水分状態を監視。",
            },
        },
        "side_effects": ["flatulence", "diarrhea if overdosed", "dehydration"],
        "side_effects_ja": ["鼓腸", "過量投与で下痢", "脱水"],
        "contraindications": "Intestinal obstruction.",
        "contraindications_ja": "腸閉塞。",
    },
    # ══════════════════════════════════════════════════════════════════════
    # 循環器薬 (Cardiovascular Drugs)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": "pimobendan",
        "name": "Pimobendan (Vetmedin)",
        "name_ja": "ピモベンダン（ベトメディン）",
        "category": "cardiovascular",
        "mechanism": "Calcium sensitizer and PDE3 inhibitor; positive inotrope and vasodilator (inodilator).",
        "mechanism_ja": "カルシウム感受性増強薬・PDE3阻害薬。陽性変力作用と血管拡張作用（inodilator）。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "0.25-0.3 mg/kg PO q12h",
                "dosage_ja": "0.25-0.3 mg/kg 経口 12時間毎",
                "notes": "Standard treatment for DCM and MMVD (stage B2 and above). Give on empty stomach.",
                "notes_ja": "DCMとMMVD（B2ステージ以上）の標準治療。空腹時に投与。",
            },
            "cat": {
                "safe": True,
                "dosage": "0.625-1.25 mg/cat PO q12h",
                "dosage_ja": "0.625-1.25 mg/頭 経口 12時間毎",
                "notes": "Used for feline CHF, but controversial. May worsen HCM obstruction.",
                "notes_ja": "猫のCHFに使用されるが議論あり。HCMの閉塞を悪化させる可能性。",
            },
        },
        "side_effects": ["GI upset", "arrhythmias (rare)"],
        "side_effects_ja": ["消化器症状", "不整脈（まれ）"],
        "contraindications": "Hypertrophic cardiomyopathy with dynamic outflow tract obstruction. Aortic stenosis.",
        "contraindications_ja": "動的流出路閉塞を伴う肥大型心筋症。大動脈弁狭窄症。",
    },
    {
        "id": "benazepril",
        "name": "Benazepril (Fortekor)",
        "name_ja": "ベナゼプリル（フォルテコール）",
        "category": "ace_inhibitors",
        "mechanism": "ACE inhibitor; reduces angiotensin II production, lowering blood pressure and reducing cardiac afterload.",
        "mechanism_ja": "ACE阻害薬。アンジオテンシンII産生を減少させ血圧を低下させ心臓後負荷を軽減。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "0.25-0.5 mg/kg PO q12-24h",
                "dosage_ja": "0.25-0.5 mg/kg 経口 12-24時間毎",
                "notes": "Used for heart failure and proteinuria/CKD",
                "notes_ja": "心不全・蛋白尿/CKDに使用",
            },
            "cat": {
                "safe": True,
                "dosage": "0.25-0.5 mg/kg PO q24h",
                "dosage_ja": "0.25-0.5 mg/kg 経口 24時間毎",
                "notes": "Licensed for CKD in cats (Fortekor). Hepatic elimination (advantage in renal disease).",
                "notes_ja": "猫のCKDに認可（フォルテコール）。肝排泄型（腎疾患に有利）。",
            },
            "horse": {
                "safe": True,
                "dosage": "0.25-0.5 mg/kg PO q24h",
                "dosage_ja": "0.25-0.5 mg/kg 経口 24時間毎",
                "notes": "Used for equine heart disease",
                "notes_ja": "馬の心疾患に使用",
            },
        },
        "side_effects": ["hypotension", "hyperkalemia", "azotemia (monitor renal values)"],
        "side_effects_ja": ["低血圧", "高カリウム血症", "高窒素血症（腎数値を監視）"],
        "contraindications": "Hypotension. Bilateral renal artery stenosis. Pregnancy.",
        "contraindications_ja": "低血圧。両側腎動脈狭窄。妊娠中。",
    },
    {
        "id": "enalapril",
        "name": "Enalapril (Enacard)",
        "name_ja": "エナラプリル（エナカルド）",
        "category": "ace_inhibitors",
        "mechanism": "ACE inhibitor; similar to benazepril but renally eliminated.",
        "mechanism_ja": "ACE阻害薬。ベナゼプリルに類似するが腎排泄型。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "0.25-0.5 mg/kg PO q12-24h",
                "dosage_ja": "0.25-0.5 mg/kg 経口 12-24時間毎",
                "notes": "Commonly used for heart failure in dogs",
                "notes_ja": "犬の心不全に一般的に使用",
            },
            "cat": {
                "safe": True,
                "dosage": "0.25-0.5 mg/kg PO q12-24h",
                "dosage_ja": "0.25-0.5 mg/kg 経口 12-24時間毎",
                "notes": "Renally eliminated - adjust dose in CKD. Benazepril often preferred for cats.",
                "notes_ja": "腎排泄型 - CKDでは用量調整。猫にはベナゼプリルが好まれることが多い。",
            },
        },
        "side_effects": ["same as benazepril"],
        "side_effects_ja": ["ベナゼプリルと同様"],
        "contraindications": "Renal insufficiency (use benazepril instead). Hypotension.",
        "contraindications_ja": "腎不全（代わりにベナゼプリルを使用）。低血圧。",
    },
    {
        "id": "furosemide",
        "name": "Furosemide (Lasix)",
        "name_ja": "フロセミド（ラシックス）",
        "category": "diuretics",
        "mechanism": "Loop diuretic; inhibits Na+/K+/2Cl- cotransporter in loop of Henle.",
        "mechanism_ja": "ループ利尿薬。ヘンレ係蹄のNa+/K+/2Cl-共輸送体を阻害。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "1-4 mg/kg IV/IM/PO q8-12h (maintenance); up to 6 mg/kg IV q1h (acute CHF)",
                "dosage_ja": "1-4 mg/kg 静注/筋注/経口 8-12時間毎（維持）; 最大6 mg/kg 静注 1時間毎（急性CHF）",
                "notes": "Essential for CHF management. Monitor electrolytes and renal values.",
                "notes_ja": "CHF管理に必須。電解質と腎数値を監視。",
            },
            "cat": {
                "safe": True,
                "dosage": "1-2 mg/kg IV/IM/PO q8-12h",
                "dosage_ja": "1-2 mg/kg 静注/筋注/経口 8-12時間毎",
                "notes": "Used for CHF and pleural effusion in cats",
                "notes_ja": "猫のCHF・胸水に使用",
            },
            "horse": {
                "safe": True,
                "dosage": "0.5-1 mg/kg IV/IM q12h",
                "dosage_ja": "0.5-1 mg/kg 静注/筋注 12時間毎",
                "notes": "Used for pulmonary edema, exercise-induced pulmonary hemorrhage",
                "notes_ja": "肺水腫・運動誘発性肺出血に使用",
            },
            "rabbit": {
                "safe": True,
                "dosage": "1-4 mg/kg IV/IM/PO q12h",
                "dosage_ja": "1-4 mg/kg 静注/筋注/経口 12時間毎",
                "notes": "Used for heart failure in rabbits",
                "notes_ja": "ウサギの心不全に使用",
            },
            "ferret": {
                "safe": True,
                "dosage": "1-4 mg/kg PO/IM/IV q8-12h",
                "dosage_ja": "1-4 mg/kg 経口/筋注/静注 8-12時間毎",
                "notes": "Essential for ferret cardiac disease",
                "notes_ja": "フェレットの心疾患に必須",
            },
        },
        "side_effects": [
            "dehydration",
            "hypokalemia",
            "hypochloremic alkalosis",
            "ototoxicity (high doses)",
            "prerenal azotemia",
        ],
        "side_effects_ja": [
            "脱水",
            "低カリウム血症",
            "低クロール性アルカローシス",
            "聴覚毒性（高用量）",
            "腎前性高窒素血症",
        ],
        "contraindications": "Dehydration. Electrolyte imbalance. Anuria.",
        "contraindications_ja": "脱水。電解質異常。無尿。",
    },
    {
        "id": "amlodipine",
        "name": "Amlodipine",
        "name_ja": "アムロジピン",
        "category": "cardiovascular",
        "mechanism": "Calcium channel blocker (dihydropyridine); arterial vasodilator, reduces blood pressure.",
        "mechanism_ja": "カルシウムチャネル遮断薬（ジヒドロピリジン系）。動脈血管拡張薬。血圧を低下させる。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "0.05-0.1 mg/kg PO q24h",
                "dosage_ja": "0.05-0.1 mg/kg 経口 24時間毎",
                "notes": "Used as add-on antihypertensive in dogs",
                "notes_ja": "犬の追加降圧薬として使用",
            },
            "cat": {
                "safe": True,
                "dosage": "0.125-0.25 mg/cat PO q24h (start low, titrate)",
                "dosage_ja": "0.125-0.25 mg/頭 経口 24時間毎（低用量から開始、漸増）",
                "notes": "DRUG OF CHOICE for feline hypertension. Very effective.",
                "notes_ja": "猫の高血圧の第一選択薬。非常に有効。",
            },
        },
        "side_effects": ["hypotension", "tachycardia", "gingival hyperplasia (rare)"],
        "side_effects_ja": ["低血圧", "頻脈", "歯肉増殖（まれ）"],
        "contraindications": "Severe aortic stenosis. Hypotension.",
        "contraindications_ja": "重度大動脈弁狭窄症。低血圧。",
    },
    {
        "id": "atenolol",
        "name": "Atenolol",
        "name_ja": "アテノロール",
        "category": "cardiovascular",
        "mechanism": "Beta-1 selective adrenergic blocker; reduces heart rate and myocardial oxygen demand.",
        "mechanism_ja": "β1選択的アドレナリン遮断薬。心拍数と心筋酸素需要を減少させる。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "0.25-1 mg/kg PO q12-24h",
                "dosage_ja": "0.25-1 mg/kg 経口 12-24時間毎",
                "notes": "Used for SVT, ventricular arrhythmias",
                "notes_ja": "上室性頻拍・心室性不整脈に使用",
            },
            "cat": {
                "safe": True,
                "dosage": "6.25-12.5 mg/cat PO q12-24h",
                "dosage_ja": "6.25-12.5 mg/頭 経口 12-24時間毎",
                "notes": "Drug of choice for feline HCM to reduce heart rate and dynamic obstruction",
                "notes_ja": "猫のHCMの第一選択薬。心拍数と動的閉塞を軽減。",
            },
        },
        "side_effects": ["bradycardia", "hypotension", "lethargy", "bronchospasm"],
        "side_effects_ja": ["徐脈", "低血圧", "無気力", "気管支痙攣"],
        "contraindications": "CHF (acute). Bradycardia. AV block. Asthma.",
        "contraindications_ja": "急性CHF。徐脈。房室ブロック。喘息。",
    },
    {
        "id": "spironolactone",
        "name": "Spironolactone",
        "name_ja": "スピロノラクトン",
        "category": "diuretics",
        "mechanism": "Aldosterone antagonist; potassium-sparing diuretic with antifibrotic cardiac effects.",
        "mechanism_ja": "アルドステロン拮抗薬。カリウム保持性利尿薬で抗線維化心保護作用を持つ。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "1-2 mg/kg PO q12h",
                "dosage_ja": "1-2 mg/kg 経口 12時間毎",
                "notes": "Added to heart failure therapy for cardiac remodeling benefit",
                "notes_ja": "心臓リモデリング改善のため心不全治療に追加",
            },
            "cat": {
                "safe": True,
                "dosage": "1-2 mg/kg PO q12h",
                "dosage_ja": "1-2 mg/kg 経口 12時間毎",
                "notes": "Used for CHF in cats",
                "notes_ja": "猫のCHFに使用",
            },
        },
        "side_effects": ["hyperkalemia", "GI upset", "facial dermatitis (cats)"],
        "side_effects_ja": ["高カリウム血症", "消化器症状", "顔面皮膚炎（猫）"],
        "contraindications": "Hyperkalemia. Severe renal insufficiency.",
        "contraindications_ja": "高カリウム血症。重度腎不全。",
    },
    # ══════════════════════════════════════════════════════════════════════
    # 内分泌薬 (Endocrine Drugs)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": "methimazole",
        "name": "Methimazole (Tapazole/Felimazole)",
        "name_ja": "メチマゾール（タパゾール/フェリマゾール）",
        "category": "endocrine",
        "mechanism": "Antithyroid drug; inhibits thyroid peroxidase, blocking thyroid hormone synthesis.",
        "mechanism_ja": "抗甲状腺薬。甲状腺ペルオキシダーゼを阻害し甲状腺ホルモン合成を遮断。",
        "species_info": {
            "cat": {
                "safe": True,
                "dosage": "1.25-2.5 mg/cat PO q12h (starting dose); titrate based on T4 levels",
                "dosage_ja": "1.25-2.5 mg/頭 経口 12時間毎（開始用量）; T4値に基づき調整",
                "notes": "Standard treatment for feline hyperthyroidism. Monitor T4, renal values, CBC.",
                "notes_ja": "猫の甲状腺機能亢進症の標準治療。T4・腎数値・CBCを監視。",
            },
            "dog": {
                "safe": True,
                "dosage": "Rarely used; thyroid tumors in dogs usually require surgery",
                "dosage_ja": "ほとんど使用しない。犬の甲状腺腫瘍は通常手術が必要。",
                "notes": "Not commonly needed in dogs",
                "notes_ja": "犬ではあまり必要とされない",
            },
        },
        "side_effects": ["GI upset", "facial excoriation/pruritus", "hepatotoxicity", "bone marrow suppression (rare)"],
        "side_effects_ja": ["消化器症状", "顔面掻痒・擦過傷", "肝毒性", "骨髄抑制（まれ）"],
        "contraindications": "Hepatic disease. Pre-existing hematologic abnormalities.",
        "contraindications_ja": "肝疾患。既存の血液学的異常。",
    },
    {
        "id": "levothyroxine",
        "name": "Levothyroxine (Soloxine/Thyro-Tabs)",
        "name_ja": "レボチロキシン（ソロキシン）",
        "category": "endocrine",
        "mechanism": "Synthetic T4 (thyroxine); replacement therapy for hypothyroidism.",
        "mechanism_ja": "合成T4（サイロキシン）。甲状腺機能低下症の補充療法。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "0.02-0.04 mg/kg PO q12h",
                "dosage_ja": "0.02-0.04 mg/kg 経口 12時間毎",
                "notes": "Standard for canine hypothyroidism. Monitor T4 levels 4-6 hours post-pill. Give on empty stomach.",
                "notes_ja": "犬の甲状腺機能低下症の標準治療。投薬4-6時間後のT4を監視。空腹時投与。",
            },
            "cat": {
                "safe": True,
                "dosage": "0.05-0.1 mg/cat PO q24h",
                "dosage_ja": "0.05-0.1 mg/頭 経口 24時間毎",
                "notes": "Rare in cats; iatrogenic after thyroidectomy or I-131",
                "notes_ja": "猫ではまれ。甲状腺切除術またはI-131後の医原性に。",
            },
            "horse": {
                "safe": True,
                "dosage": "0.04-0.08 mg/kg PO q24h",
                "dosage_ja": "0.04-0.08 mg/kg 経口 24時間毎",
                "notes": "Used for equine metabolic syndrome (off-label)",
                "notes_ja": "馬のメタボリックシンドロームに使用（適応外）",
            },
        },
        "side_effects": ["hyperthyroidism signs if overdosed (tachycardia, weight loss, restlessness)"],
        "side_effects_ja": ["過量投与で甲状腺機能亢進症の徴候（頻脈・体重減少・不穏）"],
        "contraindications": "Adrenal insufficiency (correct first). Thyrotoxicosis.",
        "contraindications_ja": "副腎不全（先に是正）。甲状腺中毒症。",
    },
    {
        "id": "trilostane",
        "name": "Trilostane (Vetoryl)",
        "name_ja": "トリロスタン（ベトリル）",
        "category": "endocrine",
        "mechanism": "3-beta-hydroxysteroid dehydrogenase inhibitor; blocks cortisol synthesis for Cushing's treatment.",
        "mechanism_ja": "3β-ヒドロキシステロイドデヒドロゲナーゼ阻害薬。コルチゾール合成を遮断しクッシング症候群を治療。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "1-3 mg/kg PO q12h (start low); adjust based on ACTH stimulation test",
                "dosage_ja": "1-3 mg/kg 経口 12時間毎（低用量開始）; ACTH刺激試験に基づき調整",
                "notes": "Drug of choice for canine Cushing's. Regular ACTH stim monitoring essential. Give with food.",
                "notes_ja": "犬のクッシング症候群の第一選択薬。定期的なACTH刺激試験が必須。食事と共に投与。",
            },
            "ferret": {
                "safe": True,
                "dosage": "1-2 mg/kg PO q12-24h",
                "dosage_ja": "1-2 mg/kg 経口 12-24時間毎",
                "notes": "Used for ferret adrenal disease when surgery not possible",
                "notes_ja": "手術不可能な場合のフェレット副腎疾患に使用",
            },
        },
        "side_effects": [
            "adrenal necrosis (rare, acute)",
            "hypoadrenocorticism (Addisonian crisis)",
            "lethargy",
            "GI upset",
        ],
        "side_effects_ja": ["副腎壊死（まれ、急性）", "副腎皮質機能低下症（アジソンクリーゼ）", "無気力", "消化器症状"],
        "contraindications": "Hepatic or renal disease. Pregnancy.",
        "contraindications_ja": "肝・腎疾患。妊娠中。",
    },
    {
        "id": "insulin_vetsulin",
        "name": "Insulin (Veterinary - Vetsulin/Caninsulin, ProZinc, Glargine)",
        "name_ja": "インスリン（獣医用 - ベトスリン/カニンスリン、プロジンク、グラルギン）",
        "category": "endocrine",
        "mechanism": "Exogenous insulin; facilitates glucose uptake into cells for diabetes mellitus management.",
        "mechanism_ja": "外因性インスリン。細胞へのグルコース取り込みを促進し糖尿病を管理する。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Vetsulin (Lente): 0.25-0.5 IU/kg SC q12h (starting dose)",
                "dosage_ja": "ベトスリン（レンテ）: 0.25-0.5 IU/kg 皮下 12時間毎（開始用量）",
                "notes": "Titrate based on blood glucose curves. Most dogs need q12h dosing.",
                "notes_ja": "血糖曲線に基づき調整。多くの犬は12時間毎の投与が必要。",
            },
            "cat": {
                "safe": True,
                "dosage": "ProZinc: 1-2 IU/cat SC q12h; Glargine: 1-2 IU/cat SC q12h",
                "dosage_ja": "プロジンク: 1-2 IU/頭 皮下 12時間毎; グラルギン: 1-2 IU/頭 皮下 12時間毎",
                "notes": "Glargine preferred for diabetic remission potential. Monitor closely for hypoglycemia.",
                "notes_ja": "糖尿病寛解の可能性があるグラルギンが好ましい。低血糖に注意して監視。",
            },
            "horse": {
                "safe": True,
                "dosage": "0.1-0.2 IU/kg IM q12-24h (for specific conditions)",
                "dosage_ja": "0.1-0.2 IU/kg 筋注 12-24時間毎（特定の病態に）",
                "notes": "Equine diabetes is rare; insulin used for metabolic testing",
                "notes_ja": "馬の糖尿病はまれ。代謝試験に使用。",
            },
            "ferret": {
                "safe": True,
                "dosage": "NOT for insulinoma (would worsen hypoglycemia). Used for rare diabetic ferrets: 0.5-1 IU/ferret SC q12h",
                "dosage_ja": "インスリノーマには不可（低血糖悪化）。まれな糖尿病フェレット: 0.5-1 IU/頭 皮下 12時間毎",
                "notes": "Ferret diabetes is extremely rare; insulinoma is common (different treatment)",
                "notes_ja": "フェレットの糖尿病は極めてまれ。インスリノーマが一般的（治療法が異なる）。",
            },
        },
        "side_effects": ["hypoglycemia (most important)", "injection site reactions"],
        "side_effects_ja": ["低血糖（最も重要）", "注射部位反応"],
        "contraindications": "Insulinoma (would worsen hypoglycemia). Hypoglycemia.",
        "contraindications_ja": "インスリノーマ（低血糖を悪化させる）。低血糖。",
    },
    # ══════════════════════════════════════════════════════════════════════
    # 神経薬 (Neurological Drugs)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": "phenobarbital",
        "name": "Phenobarbital",
        "name_ja": "フェノバルビタール",
        "category": "neurological",
        "mechanism": "Barbiturate anticonvulsant; enhances GABA-A receptor activity, reducing neuronal excitability.",
        "mechanism_ja": "バルビツール系抗痙攣薬。GABA-A受容体活性を増強し神経興奮性を低下させる。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "2-5 mg/kg PO q12h",
                "dosage_ja": "2-5 mg/kg 経口 12時間毎",
                "notes": "First-line anticonvulsant for dogs. Monitor serum levels (15-40 mcg/mL). Hepatotoxicity with long-term use.",
                "notes_ja": "犬の第一選択抗痙攣薬。血中濃度を監視（15-40 mcg/mL）。長期使用で肝毒性。",
            },
            "cat": {
                "safe": True,
                "dosage": "1-2 mg/kg PO q12h",
                "dosage_ja": "1-2 mg/kg 経口 12時間毎",
                "notes": "Used for feline epilepsy but levetiracetam often preferred",
                "notes_ja": "猫のてんかんに使用されるがレベチラセタムが好まれることが多い",
            },
            "horse": {
                "safe": True,
                "dosage": "6.6-11 mg/kg IV loading; maintenance varies",
                "dosage_ja": "6.6-11 mg/kg 静注ローディング; 維持量は可変",
                "notes": "Used for neonatal seizures",
                "notes_ja": "新生子の痙攣に使用",
            },
        },
        "side_effects": [
            "sedation",
            "ataxia",
            "PU/PD",
            "polyphagia",
            "hepatotoxicity",
            "bone marrow suppression (rare)",
        ],
        "side_effects_ja": ["鎮静", "運動失調", "多飲多尿", "多食", "肝毒性", "骨髄抑制（まれ）"],
        "contraindications": "Hepatic disease. Hypovolemia.",
        "contraindications_ja": "肝疾患。循環血液量減少。",
    },
    {
        "id": "levetiracetam",
        "name": "Levetiracetam (Keppra)",
        "name_ja": "レベチラセタム（イーケプラ）",
        "category": "neurological",
        "mechanism": "Binds SV2A protein on synaptic vesicles, modulating neurotransmitter release.",
        "mechanism_ja": "シナプス小胞のSV2A蛋白に結合し神経伝達物質放出を調節する。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "20-60 mg/kg PO q8h (regular); 30-60 mg/kg PO q12h (extended release)",
                "dosage_ja": "20-60 mg/kg 経口 8時間毎（通常型）; 30-60 mg/kg 経口 12時間毎（徐放型）",
                "notes": "Excellent safety profile. Often added to phenobarbital. Minimal hepatic metabolism.",
                "notes_ja": "優れた安全性。フェノバルビタールに追加されることが多い。肝代謝が最小限。",
            },
            "cat": {
                "safe": True,
                "dosage": "20-30 mg/kg PO q8h",
                "dosage_ja": "20-30 mg/kg 経口 8時間毎",
                "notes": "Increasingly preferred as first-line for cats due to safety",
                "notes_ja": "安全性から猫の第一選択薬として使用増加中",
            },
        },
        "side_effects": ["sedation (mild)", "GI upset", "behavioral changes"],
        "side_effects_ja": ["鎮静（軽度）", "消化器症状", "行動変化"],
        "contraindications": "Renal dose adjustment. Do not crush extended-release tablets.",
        "contraindications_ja": "腎用量調整。徐放錠は砕かないこと。",
    },
    {
        "id": "diazepam",
        "name": "Diazepam (Valium)",
        "name_ja": "ジアゼパム（バリウム）",
        "category": "sedatives",
        "mechanism": "Benzodiazepine; enhances GABA-A activity. Anticonvulsant, anxiolytic, muscle relaxant, sedative.",
        "mechanism_ja": "ベンゾジアゼピン系。GABA-A活性を増強。抗痙攣・抗不安・筋弛緩・鎮静作用。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "0.5-1 mg/kg IV (status epilepticus); 0.5-2 mg/kg rectal (at-home emergency)",
                "dosage_ja": "0.5-1 mg/kg 静注（てんかん重積）; 0.5-2 mg/kg 経直腸（在宅緊急用）",
                "notes": "Drug of choice for status epilepticus. Oral has poor bioavailability in dogs.",
                "notes_ja": "てんかん重積の第一選択薬。犬では経口バイオアベイラビリティが低い。",
            },
            "cat": {
                "safe": True,
                "dosage": "0.5-1 mg/kg IV (seizures); 1-2.5 mg/cat PO q12h (appetite stimulant)",
                "dosage_ja": "0.5-1 mg/kg 静注（痙攣）; 1-2.5 mg/頭 経口 12時間毎（食欲増進）",
                "notes": "CAUTION: rare fatal hepatotoxicity with oral diazepam in cats. IV is safe.",
                "notes_ja": "【注意】猫への経口投与でまれに致死的肝毒性。静注は安全。",
            },
            "horse": {
                "safe": True,
                "dosage": "0.01-0.04 mg/kg IV",
                "dosage_ja": "0.01-0.04 mg/kg 静注",
                "notes": "Used for foal seizures",
                "notes_ja": "子馬の痙攣に使用",
            },
            "rabbit": {
                "safe": True,
                "dosage": "1-3 mg/kg IM/IV",
                "dosage_ja": "1-3 mg/kg 筋注/静注",
                "notes": "Muscle relaxant and sedative for rabbits",
                "notes_ja": "ウサギの筋弛緩薬・鎮静薬",
            },
        },
        "side_effects": ["sedation", "paradoxical excitement", "hepatotoxicity (cats, oral)", "respiratory depression"],
        "side_effects_ja": ["鎮静", "逆説的興奮", "肝毒性（猫、経口）", "呼吸抑制"],
        "contraindications": "Cats (oral). Hepatic disease. Respiratory depression.",
        "contraindications_ja": "猫（経口）。肝疾患。呼吸抑制。",
    },
    # ══════════════════════════════════════════════════════════════════════
    # 免疫抑制薬 (Immunosuppressives)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": "cyclosporine",
        "name": "Cyclosporine (Atopica)",
        "name_ja": "シクロスポリン（アトピカ）",
        "category": "immunosuppressives",
        "mechanism": "Calcineurin inhibitor; blocks T-cell activation and IL-2 production.",
        "mechanism_ja": "カルシネュリン阻害薬。T細胞活性化とIL-2産生を遮断する。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "5 mg/kg PO q24h (Atopica, modified); can reduce to q48h after 4-6 weeks",
                "dosage_ja": "5 mg/kg 経口 24時間毎（アトピカ、改良型）; 4-6週後にq48hに減量可能",
                "notes": "Licensed for atopic dermatitis. Give on empty stomach (2h before food).",
                "notes_ja": "アトピー性皮膚炎に認可。空腹時に投与（食事の2時間前）。",
            },
            "cat": {
                "safe": True,
                "dosage": "7 mg/kg PO q24h",
                "dosage_ja": "7 mg/kg 経口 24時間毎",
                "notes": "Used for allergic dermatitis, stomatitis, IBD",
                "notes_ja": "アレルギー性皮膚炎・口内炎・IBDに使用",
            },
            "horse": {
                "safe": True,
                "dosage": "5-10 mg/kg PO q24h",
                "dosage_ja": "5-10 mg/kg 経口 24時間毎",
                "notes": "Very expensive for horses due to body weight",
                "notes_ja": "体重のため馬では非常に高価",
            },
        },
        "side_effects": ["GI upset", "gingival hyperplasia", "papillomatosis", "hirsutism"],
        "side_effects_ja": ["消化器症状", "歯肉増殖", "乳頭腫症", "多毛症"],
        "contraindications": "Active neoplasia. Concurrent ketoconazole (increases levels).",
        "contraindications_ja": "活動性腫瘍。ケトコナゾールとの併用（血中濃度上昇）。",
    },
    {
        "id": "chlorambucil",
        "name": "Chlorambucil (Leukeran)",
        "name_ja": "クロラムブシル（ロイケラン）",
        "category": "antineoplastics",
        "mechanism": "Alkylating agent; cross-links DNA strands, preventing cell division. Immunosuppressive and antineoplastic.",
        "mechanism_ja": "アルキル化薬。DNA鎖を架橋し細胞分裂を阻害。免疫抑制・抗腫瘍作用。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "2-6 mg/m2 PO q24-48h",
                "dosage_ja": "2-6 mg/m2 経口 24-48時間毎",
                "notes": "Used for lymphoma, CLL, IMHA/ITP",
                "notes_ja": "リンパ腫・CLL・IMHA/ITPに使用",
            },
            "cat": {
                "safe": True,
                "dosage": "2-6 mg/m2 PO q24-48h; or 20 mg/m2 q14 days (pulse)",
                "dosage_ja": "2-6 mg/m2 経口 24-48時間毎; または20 mg/m2 14日毎（パルス）",
                "notes": "Commonly used for GI lymphoma in cats. Well tolerated.",
                "notes_ja": "猫の消化管リンパ腫に一般的に使用。忍容性良好。",
            },
        },
        "side_effects": ["bone marrow suppression", "GI upset", "hepatotoxicity (rare)"],
        "side_effects_ja": ["骨髄抑制", "消化器症状", "肝毒性（まれ）"],
        "contraindications": "Active infection. Pre-existing bone marrow suppression.",
        "contraindications_ja": "活動性感染症。既存の骨髄抑制。",
    },
    # ══════════════════════════════════════════════════════════════════════
    # 皮膚科薬 (Dermatological)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": "oclacitinib",
        "name": "Oclacitinib (Apoquel)",
        "name_ja": "オクラシチニブ（アポキル）",
        "category": "dermatological",
        "mechanism": "Janus kinase (JAK) inhibitor; selectively inhibits JAK1-dependent cytokines involved in itch and inflammation.",
        "mechanism_ja": "ヤヌスキナーゼ（JAK）阻害薬。痒みと炎症に関与するJAK1依存性サイトカインを選択的に阻害。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "0.4-0.6 mg/kg PO q12h for 14 days, then q24h",
                "dosage_ja": "0.4-0.6 mg/kg 経口 12時間毎×14日、その後24時間毎",
                "notes": "Licensed for atopic dermatitis in dogs. Rapid onset (within 4h). Not for dogs <12 months.",
                "notes_ja": "犬のアトピー性皮膚炎に認可。速効性（4時間以内）。12ヶ月未満の犬には不可。",
            },
            "cat": {
                "safe": True,
                "dosage": "1 mg/kg PO q12h (off-label)",
                "dosage_ja": "1 mg/kg 経口 12時間毎（適応外）",
                "notes": "Off-label but increasingly used for feline allergic dermatitis",
                "notes_ja": "適応外だが猫のアレルギー性皮膚炎に使用が増加中",
            },
        },
        "side_effects": [
            "increased infection susceptibility",
            "demodicosis",
            "GI upset",
            "neoplasia (theoretical concern)",
        ],
        "side_effects_ja": ["感染感受性増加", "毛包虫症", "消化器症状", "腫瘍（理論的懸念）"],
        "contraindications": "Dogs under 12 months. Known neoplasia. Active serious infections.",
        "contraindications_ja": "12ヶ月未満の犬。既知の腫瘍。活動性の重篤な感染症。",
    },
    # ══════════════════════════════════════════════════════════════════════
    # 抗ヒスタミン薬 (Antihistamines)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": "diphenhydramine",
        "name": "Diphenhydramine (Benadryl)",
        "name_ja": "ジフェンヒドラミン（ベナドリル）",
        "category": "antihistamines",
        "mechanism": "First-generation H1 antihistamine; blocks histamine receptors. Also has anticholinergic and sedative effects.",
        "mechanism_ja": "第一世代H1抗ヒスタミン薬。ヒスタミン受容体を遮断。抗コリン作用・鎮静作用も持つ。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "2-4 mg/kg PO q8-12h",
                "dosage_ja": "2-4 mg/kg 経口 8-12時間毎",
                "notes": "Often used for mild allergic reactions. Limited efficacy for atopic dermatitis.",
                "notes_ja": "軽度アレルギー反応に使用。アトピー性皮膚炎への効果は限定的。",
            },
            "cat": {
                "safe": True,
                "dosage": "1-2 mg/kg PO q8-12h",
                "dosage_ja": "1-2 mg/kg 経口 8-12時間毎",
                "notes": "Safe for cats; causes sedation",
                "notes_ja": "猫に安全。鎮静を引き起こす。",
            },
            "rabbit": {
                "safe": True,
                "dosage": "1-2 mg/kg PO/SC q8-12h",
                "dosage_ja": "1-2 mg/kg 経口/皮下 8-12時間毎",
                "notes": "Used for allergic reactions",
                "notes_ja": "アレルギー反応に使用",
            },
            "ferret": {
                "safe": True,
                "dosage": "1-2 mg/kg PO q8-12h",
                "dosage_ja": "1-2 mg/kg 経口 8-12時間毎",
                "notes": "Safe for ferrets",
                "notes_ja": "フェレットに安全",
            },
        },
        "side_effects": ["sedation", "dry mouth", "urinary retention"],
        "side_effects_ja": ["鎮静", "口渇", "尿閉"],
        "contraindications": "Glaucoma. Urinary obstruction.",
        "contraindications_ja": "緑内障。尿路閉塞。",
    },
    # ══════════════════════════════════════════════════════════════════════
    # サプリメント・肝保護薬 (Supplements / Hepatoprotectants)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": "same",
        "name": "S-Adenosylmethionine (SAMe/Denosyl)",
        "name_ja": "S-アデノシルメチオニン（SAMe/デノシル）",
        "category": "hepatoprotectants",
        "mechanism": "Methyl donor and glutathione precursor; hepatoprotective and antioxidant.",
        "mechanism_ja": "メチル供与体・グルタチオン前駆体。肝保護・抗酸化作用。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "20 mg/kg PO q24h on empty stomach",
                "dosage_ja": "20 mg/kg 経口 24時間毎 空腹時",
                "notes": "Give on empty stomach for best absorption. Enteric-coated tablets should not be split.",
                "notes_ja": "最良の吸収のため空腹時投与。腸溶錠は分割不可。",
            },
            "cat": {
                "safe": True,
                "dosage": "90-200 mg/cat PO q24h on empty stomach",
                "dosage_ja": "90-200 mg/頭 経口 24時間毎 空腹時",
                "notes": "Essential support for hepatic lipidosis and cholangitis",
                "notes_ja": "肝リピドーシス・胆管炎の必須サポート",
            },
        },
        "side_effects": ["generally well tolerated", "mild GI upset if not given on empty stomach"],
        "side_effects_ja": ["一般的に忍容性良好", "空腹時でない場合に軽度の消化器症状"],
        "contraindications": "None significant.",
        "contraindications_ja": "特になし。",
    },
    {
        "id": "omega3",
        "name": "Omega-3 Fatty Acids (EPA/DHA)",
        "name_ja": "オメガ3脂肪酸（EPA/DHA）",
        "category": "supplements",
        "mechanism": "Anti-inflammatory; modulates eicosanoid production, reduces inflammatory cytokines.",
        "mechanism_ja": "抗炎症作用。エイコサノイド産生を調節し炎症性サイトカインを減少させる。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "EPA 40-70 mg/kg + DHA 25-45 mg/kg PO q24h",
                "dosage_ja": "EPA 40-70 mg/kg + DHA 25-45 mg/kg 経口 24時間毎",
                "notes": "Beneficial for skin, joints, kidney, heart. Use fish oil source.",
                "notes_ja": "皮膚・関節・腎臓・心臓に有益。魚油源を使用。",
            },
            "cat": {
                "safe": True,
                "dosage": "EPA 30-50 mg/kg + DHA 20-30 mg/kg PO q24h",
                "dosage_ja": "EPA 30-50 mg/kg + DHA 20-30 mg/kg 経口 24時間毎",
                "notes": "Supportive for CKD, IBD, skin conditions",
                "notes_ja": "CKD・IBD・皮膚疾患のサポートに",
            },
        },
        "side_effects": ["fish odor", "GI upset at high doses", "may affect platelet function"],
        "side_effects_ja": ["魚の臭い", "高用量で消化器症状", "血小板機能に影響する可能性"],
        "contraindications": "None significant at recommended doses.",
        "contraindications_ja": "推奨用量では特になし。",
    },
    {
        "id": "glucosamine",
        "name": "Glucosamine/Chondroitin",
        "name_ja": "グルコサミン・コンドロイチン",
        "category": "supplements",
        "mechanism": "Provides building blocks for cartilage repair; mild anti-inflammatory effects.",
        "mechanism_ja": "軟骨修復の構成要素を提供。軽度の抗炎症作用。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Glucosamine: 20 mg/kg PO q24h; Chondroitin: 15 mg/kg PO q24h",
                "dosage_ja": "グルコサミン: 20 mg/kg 経口 24時間毎; コンドロイチン: 15 mg/kg 経口 24時間毎",
                "notes": "Joint supplement for osteoarthritis. Evidence mixed but safe.",
                "notes_ja": "変形性関節症の関節サプリメント。エビデンスは混在するが安全。",
            },
            "cat": {
                "safe": True,
                "dosage": "Glucosamine: 120-500 mg/cat PO q24h",
                "dosage_ja": "グルコサミン: 120-500 mg/頭 経口 24時間毎",
                "notes": "Used for feline osteoarthritis and FLUTD",
                "notes_ja": "猫の変形性関節症・FLUTDに使用",
            },
            "horse": {
                "safe": True,
                "dosage": "Varies by product; typically 5-10 g/day PO",
                "dosage_ja": "製品により異なる。通常5-10 g/日 経口",
                "notes": "Very common equine joint supplement",
                "notes_ja": "非常に一般的な馬の関節サプリメント",
            },
        },
        "side_effects": ["generally well tolerated"],
        "side_effects_ja": ["一般的に忍容性良好"],
        "contraindications": "Shellfish allergy (glucosamine from shellfish sources).",
        "contraindications_ja": "甲殻類アレルギー（甲殻類由来のグルコサミンの場合）。",
    },
    # ── Equine & Canine Vet Nutrition（スポンサー製品）────────────────────
    {
        "id": "ecvn_nmn_mito_assist",
        "name": "NMN-Mitochondria Assist (Equine & Canine Vet Nutrition)",
        "name_ja": "NMN-ミトコンドリアアシスト（Equine & Canine Vet Nutrition）",
        "category": "supplements",
        "mechanism": "NMN (nicotinamide mononucleotide) is converted to NAD+ in vivo, activating sirtuin longevity genes and supporting mitochondrial function. Combined with cysteine, α-lipoic acid, psyllium husk, and probiotics (lactobacillus, butyric acid bacteria, saccharification bacteria) for comprehensive metabolic and GI support.",
        "mechanism_ja": "NMN（ニコチンアミドモノヌクレオチド）は体内でNAD+に変換され、サーチュイン長寿遺伝子を活性化しミトコンドリア機能をサポートする。システイン、α-リポ酸、サイリウムハスク、プロバイオティクス（乳酸菌・酪酸菌・糖化菌）を配合し、代謝と消化管を包括的にサポート。",
        "routes": ["PO"],
        "routes_ja": ["経口"],
        "formulations": ["Powder (mix with feed)"],
        "formulations_ja": ["粉末（飼料に混合）"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Refer to product label for body weight-based dosing",
                "dosage_ja": "体重に応じた製品ラベルの用量を参照",
                "notes": "NMN 5000mg + Cysteine 10500mg + α-Lipoic acid 1700mg per package. Supports cellular energy, anti-aging, cognitive dysfunction (CDS), cardiomyopathy (DCM/MVD), CKD, and senior ophthalmic disease. Manufactured in Japan, tested by Racing Chemistry Laboratory.",
                "notes_ja": "NMN5000mg + システイン10500mg + α-リポ酸1700mg配合。細胞エネルギー・抗老化・認知機能不全（CDS）・心筋症（DCM/僧帽弁疾患）・CKD・加齢性眼疾患をサポート。国内製造、競走馬理化学研究所検査合格。",
            },
            "cat": {
                "safe": True,
                "dosage": "Refer to product label; start at low dose",
                "dosage_ja": "製品ラベル参照。低用量から開始",
                "notes": "For senior cats with CDS, HCM, CKD, diabetes, and age-related retinal degeneration. Mitochondrial support is particularly relevant in feline CKD and HCM pathogenesis.",
                "notes_ja": "CDS、HCM、CKD、糖尿病、加齢性網膜変性の高齢猫に。ミトコンドリアサポートは猫CKDとHCMの病態に特に関連。",
            },
            "horse": {
                "safe": True,
                "dosage": "Refer to product label for body weight-based dosing",
                "dosage_ja": "体重に応じた製品ラベルの用量を参照",
                "notes": "Safe for all stages. Applications: PPID (Cushing's), EMS, senior horse performance support, and chronic fatigue. Passed Racing Chemistry Laboratory testing — suitable for competition horses.",
                "notes_ja": "あらゆるステージに安全。PPID（クッシング）、EMS、高齢馬のパフォーマンス維持、慢性疲労に。競走馬理化学研究所検査合格 - 競技馬にも使用可能。",
            },
            "rabbit": {
                "safe": True,
                "dosage": "Refer to product label; adjust for body weight",
                "dosage_ja": "製品ラベル参照。体重に応じて調整",
                "notes": "For senior rabbits with chronic conditions, cognitive decline, and age-related cardiac disease.",
                "notes_ja": "慢性疾患、認知機能低下、加齢性心疾患の高齢ウサギに。",
            },
            "ferret": {
                "safe": True,
                "dosage": "Minimal dose; refer to product label",
                "dosage_ja": "最小量。製品ラベル参照",
                "notes": "Supportive for insulinoma, cardiomyopathy, and senior cognitive issues in ferrets.",
                "notes_ja": "フェレットのインスリノーマ、心筋症、高齢期の認知機能問題の支持療法に。",
            },
            "hamster": {
                "safe": True,
                "dosage": "Minimal dose; refer to product label",
                "dosage_ja": "最小量。製品ラベル参照",
                "notes": "For senior hamsters with cardiac or metabolic disease.",
                "notes_ja": "心疾患や代謝性疾患の高齢ハムスターに。",
            },
            "guinea_pig": {
                "safe": True,
                "dosage": "Minimal dose; refer to product label",
                "dosage_ja": "最小量。製品ラベル参照",
                "notes": "Adjunct for senior guinea pigs with cardiac or cognitive decline. Does not replace vitamin C supplementation.",
                "notes_ja": "心機能や認知機能の低下した高齢モルモットの併用療法。ビタミンC補給の代替にはならない。",
            },
            "chinchilla": {
                "safe": True,
                "dosage": "Minimal dose; refer to product label",
                "dosage_ja": "最小量。製品ラベル参照",
                "notes": "For senior chinchillas with cardiac or hepatic disease.",
                "notes_ja": "心疾患や肝疾患の高齢チンチラに。",
            },
            "hedgehog": {
                "safe": True,
                "dosage": "Minimal dose; refer to product label",
                "dosage_ja": "最小量。製品ラベル参照",
                "notes": "Supportive for WHS (mitochondrial neuronal support), cardiomyopathy, and neoplasia in hedgehogs.",
                "notes_ja": "ハリネズミのWHS（ミトコンドリア神経支持）、心筋症、腫瘍の支持療法に。",
            },
            "sugar_glider": {
                "safe": True,
                "dosage": "Minimal dose; refer to product label",
                "dosage_ja": "最小量。製品ラベル参照",
                "notes": "For senior sugar gliders with metabolic or neurologic concerns.",
                "notes_ja": "代謝性・神経学的問題のある高齢フクロモモンガに。",
            },
            "degu": {
                "safe": True,
                "dosage": "Minimal dose; refer to product label",
                "dosage_ja": "最小量。製品ラベル参照",
                "notes": "For senior degus with diabetes, cardiomyopathy, or cataract.",
                "notes_ja": "糖尿病、心筋症、白内障の高齢デグーに。",
            },
        },
        "side_effects": ["generally well tolerated"],
        "side_effects_ja": ["一般的に忍容性良好"],
        "contraindications": "None known at recommended doses.",
        "contraindications_ja": "推奨用量では特に知られていない。",
        "drug_interactions": [],
        "sponsor": True,
        "sponsor_url": "https://www.caninevet.jp/",
        "sponsor_name": "Equine & Canine Vet Nutrition",
    },
    {
        "id": "ecvn_amino_complete",
        "name": "Amino Complete (Equine & Canine Vet Nutrition)",
        "name_ja": "アミノコンプリート（Equine & Canine Vet Nutrition）",
        "category": "supplements",
        "mechanism": "Comprehensive amino acid supplement centered on BCAAs (branched-chain amino acids). BCAAs bypass hepatic metabolism and are directly metabolized in muscle cells, serving as an immediate energy source. Contains all essential amino acids plus carnitine, citrulline, glutamine, and vitamin C.",
        "mechanism_ja": "BCAA（分岐鎖アミノ酸）を中心とした包括的アミノ酸サプリメント。BCAAは肝臓を経由せず筋肉細胞で直接代謝され、即座のエネルギー源となる。全必須アミノ酸に加えカルニチン、シトルリン、グルタミン、ビタミンCを配合。",
        "routes": ["PO"],
        "routes_ja": ["経口"],
        "formulations": ["Powder (mix with feed)"],
        "formulations_ja": ["粉末（飼料に混合）"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Refer to product label (MSM+Amino Complete formulation)",
                "dosage_ja": "製品ラベル参照（MSM+アミノコンプリート配合）",
                "notes": "Canine formulation includes MSM for joint/muscle/tendon support combined with amino acid complex. Ideal for active dogs, post-surgery recovery, and senior dogs.",
                "notes_ja": "犬用はMSM配合で関節・筋肉・腱をサポートしつつアミノ酸複合体を提供。活動的な犬、術後回復期、シニア犬に最適。",
            },
            "horse": {
                "safe": True,
                "dosage": "BCAA set at maximum evidence-based dose for horses. Administer before training or after high-intensity work. May dose twice daily.",
                "dosage_ja": "BCAAは馬のエビデンスに基づく最大量に設定。調教前または高強度運動後に投与。1日2回投与も可。",
                "notes": "Formulated with BCAA, phenylalanine, methionine, lysine, arginine, histidine, threonine, tryptophan, alanine, asparagine, carnitine, citrulline, cystine, glycine, glutamine, serine, tyrosine, vitamin C, and citric acid. Rapid absorption for pre-training amino acid loading.",
                "notes_ja": "BCAA、フェニルアラニン、メチオニン、リジン、アルギニン、ヒスチジン、トレオニン、トリプトファン、アラニン、アスパラギン、カルニチン、シトルリン、シスチン、グリシン、グルタミン、セリン、チロシン、ビタミンC、クエン酸配合。調教前のアミノ酸ローディングに素早い吸収。",
            },
        },
        "side_effects": ["generally well tolerated"],
        "side_effects_ja": ["一般的に忍容性良好"],
        "contraindications": "None known at recommended doses.",
        "contraindications_ja": "推奨用量では特に知られていない。",
        "drug_interactions": [],
        "sponsor": True,
        "sponsor_url_horse": "https://www.evet-nutrition.com/amino-complete/",
        "sponsor_url_dog": "https://www.caninevet.jp/",
        "sponsor_name": "Equine & Canine Vet Nutrition",
    },
    {
        "id": "ecvn_cp_powder",
        "name": "CP Powder (Equine & Canine Vet Nutrition)",
        "name_ja": "CPパウダー（Equine & Canine Vet Nutrition）",
        "category": "supplements",
        "mechanism": "Psyllium-based soluble fiber supplement with prebiotics and probiotics. Soluble fiber has strong water-retention capacity in the intestinal lumen, increasing viscosity of GI contents and facilitating smooth transit. Prebiotics and probiotics suppress abnormal intestinal fermentation.",
        "mechanism_ja": "サイリウムベースの水溶性繊維サプリメントにプレバイオティクスとプロバイオティクスを配合。水溶性繊維は腸管内で強い水分保持能力を有し、消化管内容物の粘調性を増し円滑な輸送を促進。プレバイオティクスとプロバイオティクスが腸管内の異常発酵を抑制。",
        "routes": ["PO"],
        "routes_ja": ["経口"],
        "formulations": ["Powder (mix with feed)"],
        "formulations_ja": ["粉末（飼料に混合）"],
        "species_info": {
            "horse": {
                "safe": True,
                "dosage": "50 g/day PO mixed with feed",
                "dosage_ja": "50 g/日 経口 飼料に混合",
                "notes": "Indicated for sand colic, constipation colic, and general GI motility support. At 50g/day dosing, produces well-hydrated, soft fecal balls. Contains psyllium + prebiotics + probiotics.",
                "notes_ja": "砂疝、便秘疝、消化管運動サポートに適応。50g/日投与で保水量の多いモチモチしたボロを確認。サイリウム+プレバイオティクス+プロバイオティクス配合。",
            },
            "dog": {
                "safe": True,
                "dosage": "Refer to product label (Prebiotics & Probiotics & Psyllium formulation)",
                "dosage_ja": "製品ラベル参照（プレバイオティクス&プロバイオティクス&サイリウム配合）",
                "notes": "For constipation, diarrhea, IBD, post-pancreatitis recovery, atopy (gut-immune axis), and CKD (uremic toxin binding).",
                "notes_ja": "便秘、下痢、IBD、膵炎後の回復、アトピー（腸腎連関）、CKD（尿毒素排出促進）に。",
            },
            "cat": {
                "safe": True,
                "dosage": "Refer to product label; start at low dose",
                "dosage_ja": "製品ラベル参照。低用量から開始",
                "notes": "For constipation (common in senior cats), megacolon adjunct, IBD, and CKD support. Psyllium is well-tolerated in cats.",
                "notes_ja": "便秘（高齢猫で頻発）、巨大結腸症の併用、IBD、CKDサポートに。サイリウムは猫で忍容性良好。",
            },
            "rabbit": {
                "safe": True,
                "dosage": "Refer to product label; adjust for body weight",
                "dosage_ja": "製品ラベル参照。体重に応じて調整",
                "notes": "Beneficial for GI stasis prevention and recovery, hairball management, and dysbiosis. Critical for hindgut fermenters.",
                "notes_ja": "GI stasisの予防と回復、ヘアボール管理、腸内細菌叢異常症に有益。後腸発酵動物に重要。",
            },
            "guinea_pig": {
                "safe": True,
                "dosage": "Refer to product label; adjust for body weight",
                "dosage_ja": "製品ラベル参照。体重に応じて調整",
                "notes": "For GI dysbiosis (especially post-antibiotic), constipation, and hindgut fermentation support. Critical for hindgut fermenters.",
                "notes_ja": "腸内細菌叢異常（特に抗菌薬投与後）、便秘、後腸発酵サポートに。後腸発酵動物に重要。",
            },
            "chinchilla": {
                "safe": True,
                "dosage": "Minimal dose; refer to product label",
                "dosage_ja": "最小量。製品ラベル参照",
                "notes": "For GI stasis, dysbiosis, and constipation in chinchillas.",
                "notes_ja": "チンチラのGI stasis、腸内細菌叢異常、便秘に。",
            },
            "hamster": {
                "safe": True,
                "dosage": "Minimal dose; refer to product label",
                "dosage_ja": "最小量。製品ラベル参照",
                "notes": "For constipation, wet tail (proliferative ileitis) recovery, and dysbiosis.",
                "notes_ja": "便秘、ウェットテイル（増殖性回腸炎）回復期、腸内細菌叢異常に。",
            },
            "ferret": {
                "safe": True,
                "dosage": "Refer to product label; start at low dose",
                "dosage_ja": "製品ラベル参照。低用量から開始",
                "notes": "For ECE/chronic diarrhea, IBD, and Helicobacter-associated gastritis recovery.",
                "notes_ja": "ECE/慢性下痢、IBD、ヘリコバクター関連胃炎の回復期に。",
            },
            "hedgehog": {
                "safe": True,
                "dosage": "Minimal dose; refer to product label",
                "dosage_ja": "最小量。製品ラベル参照",
                "notes": "For constipation and GI dysbiosis in hedgehogs.",
                "notes_ja": "便秘、腸内細菌叢異常のハリネズミに。",
            },
            "sugar_glider": {
                "safe": True,
                "dosage": "Minimal dose; refer to product label",
                "dosage_ja": "最小量。製品ラベル参照",
                "notes": "For diarrhea, constipation, and dysbiosis.",
                "notes_ja": "下痢、便秘、腸内細菌叢異常に。",
            },
            "degu": {
                "safe": True,
                "dosage": "Minimal dose; refer to product label",
                "dosage_ja": "最小量。製品ラベル参照",
                "notes": "For GI stasis, constipation, and hindgut support. Critical for hindgut fermenters.",
                "notes_ja": "GI stasis、便秘、後腸サポートに。後腸発酵動物に重要。",
            },
            "bird": {
                "safe": True,
                "dosage": "Refer to product label; adjust for body size",
                "dosage_ja": "製品ラベル参照。体格に応じて調整",
                "notes": "For crop stasis, diarrhea, and post-antibiotic dysbiosis in birds.",
                "notes_ja": "鳥のそのう停滞、下痢、抗菌薬投与後の腸内細菌叢異常に。",
            },
            "parakeet": {
                "safe": True,
                "dosage": "Minimal dose; refer to product label",
                "dosage_ja": "最小量。製品ラベル参照",
                "notes": "For dysbiosis and chronic GI issues in budgerigars.",
                "notes_ja": "セキセイインコの腸内細菌叢異常、慢性GI問題に。",
            },
            "parrot": {
                "safe": True,
                "dosage": "Refer to product label; adjust for body size",
                "dosage_ja": "製品ラベル参照。体格に応じて調整",
                "notes": "For crop stasis, PDD support, and dysbiosis in parrots.",
                "notes_ja": "オウムのそのう停滞、PDD支持療法、腸内細菌叢異常に。",
            },
        },
        "side_effects": ["generally well tolerated", "increased fecal water content (expected therapeutic effect)"],
        "side_effects_ja": ["一般的に忍容性良好", "糞便含水量の増加（期待される治療効果）"],
        "contraindications": "Complete intestinal obstruction.",
        "contraindications_ja": "完全な腸閉塞。",
        "drug_interactions": [
            {
                "drug": "oral medications",
                "effect": "Psyllium may delay absorption of concurrently administered oral drugs - separate dosing by 1-2 hours",
                "effect_ja": "サイリウムが同時投与の経口薬の吸収を遅延させる可能性 - 投与を1-2時間ずらす",
            }
        ],
        "sponsor": True,
        "sponsor_url": "https://www.evet-nutrition.com/cp-powder/",
        "sponsor_name": "Equine & Canine Vet Nutrition",
    },
    {
        "id": "ecvn_for_antioxidant",
        "name": "For Antioxidant (Equine & Canine Vet Nutrition)",
        "name_ja": "フォー・アンチオキシダント（抗酸化／Equine & Canine Vet Nutrition）",
        "category": "supplements",
        "mechanism": "Antioxidant complex combining astaxanthin (potent carotenoid antioxidant from microalgae), melon-derived SOD, vitamin E (tocopherol), and cysteine (glutathione precursor). Provides multi-pathway oxidative stress protection.",
        "mechanism_ja": "アスタキサンチン（微細藻類由来の強力なカロテノイド抗酸化物質）、メロン由来SOD、ビタミンE（トコフェロール）、システイン（グルタチオン前駆体）を組み合わせた抗酸化複合体。多経路の酸化ストレス防御を提供。",
        "routes": ["PO"],
        "routes_ja": ["経口"],
        "formulations": ["Powder / Tablets"],
        "formulations_ja": ["粉末 / 錠剤"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Refer to product label for body weight-based dosing",
                "dosage_ja": "体重に応じた製品ラベルの用量を参照",
                "notes": "Supports skin health, coat quality, immune function, and anti-aging. Astaxanthin is 6000x more potent than vitamin C as an antioxidant.",
                "notes_ja": "皮膚の健康、被毛の質、免疫機能、抗老化をサポート。アスタキサンチンはビタミンCの6000倍の抗酸化力。",
            },
            "cat": {
                "safe": True,
                "dosage": "Refer to product label; start at low dose",
                "dosage_ja": "製品ラベル参照。低用量から開始",
                "notes": "Adjunct for CKD, hepatic disease, atopic dermatitis, and senior support. Astaxanthin and VitE safety well-established in cats.",
                "notes_ja": "CKD・肝疾患・アトピー性皮膚炎・シニアサポートの併用療法。アスタキサンチンとビタミンEの猫での安全性は確立されている。",
            },
            "horse": {
                "safe": True,
                "dosage": "Refer to product label",
                "dosage_ja": "製品ラベル参照",
                "notes": "Astaxanthin and amino acids for cosmetic improvement and reproductive support.",
                "notes_ja": "アスタキサンチンとアミノ酸によるコズミ改善と繁殖サポート。",
            },
            "rabbit": {
                "safe": True,
                "dosage": "Refer to product label; adjust for body weight",
                "dosage_ja": "製品ラベル参照。体重に応じて調整",
                "notes": "Supportive for GI stasis recovery, skin/coat issues, and senior rabbits with oxidative stress.",
                "notes_ja": "GI stasis回復期、皮膚・被毛不良、酸化ストレス関連の高齢ウサギに。",
            },
            "ferret": {
                "safe": True,
                "dosage": "Refer to product label; start at low dose",
                "dosage_ja": "製品ラベル参照。低用量から開始",
                "notes": "Adjunct for adrenal disease, insulinoma, and chronic inflammatory conditions.",
                "notes_ja": "副腎疾患、インスリノーマ、慢性炎症性疾患の併用療法。",
            },
            "hamster": {
                "safe": True,
                "dosage": "Minimal dose; refer to product label",
                "dosage_ja": "最小量。製品ラベル参照",
                "notes": "For senior hamsters with oxidative stress-related conditions. Monitor for dosing accuracy.",
                "notes_ja": "酸化ストレス関連疾患の高齢ハムスターに。用量の正確性に注意。",
            },
            "guinea_pig": {
                "safe": True,
                "dosage": "Minimal dose; refer to product label",
                "dosage_ja": "最小量。製品ラベル参照",
                "notes": "Adjunct for skin disease, chronic inflammation, and GI issues. Complements vitamin C supplementation.",
                "notes_ja": "皮膚疾患、慢性炎症、GI問題の併用療法。ビタミンC補給と併用で相乗効果。",
            },
            "chinchilla": {
                "safe": True,
                "dosage": "Minimal dose; refer to product label",
                "dosage_ja": "最小量。製品ラベル参照",
                "notes": "For dental, skin, and GI-related oxidative stress in chinchillas.",
                "notes_ja": "チンチラの歯科・皮膚・GI関連の酸化ストレスサポート。",
            },
            "hedgehog": {
                "safe": True,
                "dosage": "Minimal dose; refer to product label",
                "dosage_ja": "最小量。製品ラベル参照",
                "notes": "Adjunct for WHS, neoplasia, and chronic inflammatory conditions.",
                "notes_ja": "WHS、腫瘍、慢性炎症性疾患の併用療法。",
            },
            "sugar_glider": {
                "safe": True,
                "dosage": "Minimal dose; refer to product label",
                "dosage_ja": "最小量。製品ラベル参照",
                "notes": "Supportive for chronic stress/self-mutilation and senior conditions.",
                "notes_ja": "慢性ストレス・自咬症、高齢期の支持療法。",
            },
            "degu": {
                "safe": True,
                "dosage": "Minimal dose; refer to product label",
                "dosage_ja": "最小量。製品ラベル参照",
                "notes": "For senior degus with diabetes, dental disease, or chronic conditions. Note: avoid high sugar supplements.",
                "notes_ja": "糖尿病、歯科疾患、慢性疾患の高齢デグーに。高糖分サプリは避ける。",
            },
            "bird": {
                "safe": True,
                "dosage": "Refer to product label; adjust for body size",
                "dosage_ja": "製品ラベル参照。体格に応じて調整",
                "notes": "Supportive for chronic viral infections, feather/skin issues, and senior birds.",
                "notes_ja": "慢性ウイルス感染、羽毛・皮膚問題、高齢鳥の支持療法。",
            },
            "parakeet": {
                "safe": True,
                "dosage": "Minimal dose; refer to product label",
                "dosage_ja": "最小量。製品ラベル参照",
                "notes": "For PBFD, polyomavirus, and chronic feather plucking.",
                "notes_ja": "PBFD、ポリオーマウイルス、慢性羽毛毟りに。",
            },
            "parrot": {
                "safe": True,
                "dosage": "Refer to product label; adjust for body size",
                "dosage_ja": "製品ラベル参照。体格に応じて調整",
                "notes": "For PBFD, proventricular dilatation disease, and atherosclerosis management.",
                "notes_ja": "PBFD、腺胃拡張症、動脈硬化症の管理に。",
            },
        },
        "side_effects": ["generally well tolerated"],
        "side_effects_ja": ["一般的に忍容性良好"],
        "contraindications": "None known.",
        "contraindications_ja": "特に知られていない。",
        "drug_interactions": [],
        "sponsor": True,
        "sponsor_url": "https://www.caninevet.jp/",
        "sponsor_name": "Equine & Canine Vet Nutrition",
    },
    {
        "id": "ecvn_for_joint",
        "name": "For Joint (Equine & Canine Vet Nutrition)",
        "name_ja": "フォー・ジョイント（関節ケア／Equine & Canine Vet Nutrition）",
        "category": "supplements",
        "mechanism": "Joint support supplement with high-dose MSM (methylsulfonylmethane) for anti-inflammatory and connective tissue support, combined with glucosamine and chondroitin precursors for cartilage maintenance.",
        "mechanism_ja": "高容量MSM（メチルスルフォニルメタン）による抗炎症・結合組織サポートに、グルコサミン・コンドロイチン前駆体を組み合わせた関節サポートサプリメント。",
        "routes": ["PO"],
        "routes_ja": ["経口"],
        "formulations": ["Powder / Tablets"],
        "formulations_ja": ["粉末 / 錠剤"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Refer to product label for body weight-based dosing",
                "dosage_ja": "体重に応じた製品ラベルの用量を参照",
                "notes": "For osteoarthritis, hip/elbow dysplasia, post-surgical joint recovery, and active/working dogs.",
                "notes_ja": "変形性関節症、股関節/肘関節形成不全、術後の関節回復、活動的な犬・使役犬に。",
            },
            "cat": {
                "safe": True,
                "dosage": "Refer to product label; start at low dose",
                "dosage_ja": "製品ラベル参照。低用量から開始",
                "notes": "For feline OA (underdiagnosed — >60% cats >12y), post-trauma joint recovery, and senior mobility support.",
                "notes_ja": "猫のOA（12歳以上の60%以上で罹患 — 診断不足傾向）、外傷後の関節回復、高齢猫の運動機能サポートに。",
            },
            "horse": {
                "safe": True,
                "dosage": "Refer to product label - high-dose MSM formulation",
                "dosage_ja": "製品ラベル参照 - 高容量MSM配合",
                "notes": "Designed for equine joint, muscle, and tendon support. High-dose MSM is the key differentiator.",
                "notes_ja": "馬の関節・筋肉・腱のサポート用に設計。高容量MSMが特徴。",
            },
            "rabbit": {
                "safe": True,
                "dosage": "Refer to product label; adjust for body weight",
                "dosage_ja": "製品ラベル参照。体重に応じて調整",
                "notes": "For spondylosis (very common in senior rabbits) and OA. Environmental enrichment (ramps, soft bedding) is equally important.",
                "notes_ja": "脊椎症（高齢ウサギで非常に一般的）、OAに。環境改善（スロープ、軟質寝具）も同様に重要。",
            },
            "ferret": {
                "safe": True,
                "dosage": "Refer to product label; start at low dose",
                "dosage_ja": "製品ラベル参照。低用量から開始",
                "notes": "For OA, intervertebral disc disease, and post-surgical recovery in ferrets.",
                "notes_ja": "フェレットのOA、椎間板疾患、術後回復に。",
            },
            "hamster": {
                "safe": True,
                "dosage": "Minimal dose; refer to product label",
                "dosage_ja": "最小量。製品ラベル参照",
                "notes": "For senior hamsters with joint stiffness or traumatic musculoskeletal conditions.",
                "notes_ja": "関節硬直や外傷性筋骨格疾患の高齢ハムスターに。",
            },
            "guinea_pig": {
                "safe": True,
                "dosage": "Minimal dose; refer to product label",
                "dosage_ja": "最小量。製品ラベル参照",
                "notes": "Adjunct for pododermatitis-associated inflammation, OA, and post-trauma recovery.",
                "notes_ja": "足底皮膚炎関連の炎症、OA、外傷後回復の併用療法。",
            },
            "chinchilla": {
                "safe": True,
                "dosage": "Minimal dose; refer to product label",
                "dosage_ja": "最小量。製品ラベル参照",
                "notes": "For senior chinchillas with OA or traumatic joint injury.",
                "notes_ja": "OAや外傷性関節損傷の高齢チンチラに。",
            },
            "hedgehog": {
                "safe": True,
                "dosage": "Minimal dose; refer to product label",
                "dosage_ja": "最小量。製品ラベル参照",
                "notes": "For WHS-related mobility issues (palliative), OA, and fracture recovery.",
                "notes_ja": "WHS関連の運動機能障害（緩和）、OA、骨折回復に。",
            },
            "sugar_glider": {
                "safe": True,
                "dosage": "Minimal dose; refer to product label",
                "dosage_ja": "最小量。製品ラベル参照",
                "notes": "For metabolic bone disease (Ca deficiency) recovery and traumatic joint injury.",
                "notes_ja": "代謝性骨疾患（Ca欠乏）回復期、外傷性関節損傷に。",
            },
            "degu": {
                "safe": True,
                "dosage": "Minimal dose; refer to product label",
                "dosage_ja": "最小量。製品ラベル参照",
                "notes": "For senior degus with OA. Avoid concurrent high-sugar supplements.",
                "notes_ja": "OAの高齢デグーに。高糖分サプリの併用は避ける。",
            },
        },
        "side_effects": ["generally well tolerated", "mild GI upset at initiation (rare)"],
        "side_effects_ja": ["一般的に忍容性良好", "開始時の軽度消化器症状（まれ）"],
        "contraindications": "None known at recommended doses.",
        "contraindications_ja": "推奨用量では特に知られていない。",
        "drug_interactions": [],
        "sponsor": True,
        "sponsor_url": "https://www.caninevet.jp/",
        "sponsor_name": "Equine & Canine Vet Nutrition",
    },
    {
        "id": "ecvn_msm_amino_complete",
        "name": "MSM + Amino Complete (Equine & Canine Vet Nutrition)",
        "name_ja": "MSM＋アミノコンプリート（Equine & Canine Vet Nutrition）",
        "category": "supplements",
        "mechanism": "Combination product featuring high-dose MSM (methylsulfonylmethane) as an organic sulfur donor for glutathione synthesis (hepatoprotective, renoprotective against oxidative injury) and anti-inflammatory / connective tissue support, paired with a comprehensive essential amino acid complex (BCAAs, lysine, methionine, arginine, etc.) for tissue repair, muscle maintenance, and convalescent nutrition. Clinical use spans musculoskeletal/neurologic recovery (OA, IVDD, post-surgical), hepatic disease (BCAAs support hepatic encephalopathy management; sulfur-containing AAs support glutathione), and CKD (BCAA-rich profile helps preserve lean muscle while moderating nitrogen load). Differs from For Joint by emphasizing broad tissue/muscle repair plus hepatic/renal nutritional support rather than cartilage-specific support.",
        "mechanism_ja": "高容量MSM（メチルスルフォニルメタン）を有機硫黄ドナーとして提供し、グルタチオン合成サポート（肝・腎の酸化ストレス防御）と抗炎症・結合組織サポートを発揮。必須アミノ酸複合体（BCAA、リジン、メチオニン、アルギニン等）を組織修復・筋肉維持・回復期栄養として組み合わせた複合製品。臨床応用は筋骨格・神経系回復（OA・IVDD・術後）に加え、肝疾患（BCAAは肝性脳症管理を支援、含硫アミノ酸はグルタチオン合成に寄与）、CKD（BCAA中心のアミノ酸構成で窒素負荷を抑えつつ除脂肪体重を維持）にも及ぶ。For Jointと異なり関節軟骨特化ではなく、広範な組織・筋肉修復＋肝腎の栄養サポートに焦点。",
        "routes": ["PO"],
        "routes_ja": ["経口"],
        "formulations": ["Powder / Tablets"],
        "formulations_ja": ["粉末 / 錠剤"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Refer to product label for body weight-based dosing",
                "dosage_ja": "体重に応じた製品ラベルの用量を参照",
                "notes": "For OA, hip/elbow dysplasia, IVDD, post-surgical recovery, cachexia, senior sarcopenia, convalescence, chronic hepatic disease (MSM sulfur for glutathione + BCAA for encephalopathy), and CKD nutritional support (BCAA-rich AAs preserve lean muscle). Complements For Joint when muscle wasting coexists.",
                "notes_ja": "OA、股関節/肘関節形成不全、IVDD、術後回復、悪液質、シニアの筋肉減少症、回復期、慢性肝疾患（MSMの硫黄がグルタチオン合成をサポート、BCAAは肝性脳症管理に寄与）、CKDの栄養支持療法（BCAA中心で除脂肪体重を維持）に。筋肉減少を伴う場合はFor Jointと併用で相乗効果。",
            },
            "cat": {
                "safe": True,
                "dosage": "Refer to product label; start at low dose",
                "dosage_ja": "製品ラベル参照。低用量から開始",
                "notes": "For senior sarcopenia, feline OA, post-surgical recovery, CKD-associated muscle wasting (IRIS stages 2-3; BCAA-rich AAs moderate nitrogen load), hepatic lipidosis recovery, and cholangiohepatitis support. MSM donates sulfur for glutathione synthesis. Note: cats have unique taurine/methionine requirements.",
                "notes_ja": "高齢サルコペニア、猫のOA、術後回復、CKD関連筋肉減少（IRIS 2-3期；BCAA中心で窒素負荷を抑制）、肝リピドーシスの回復期、胆管肝炎の支持療法に。MSMの硫黄がグルタチオン合成をサポート。注：猫は独自のタウリン/メチオニン要求性あり。",
            },
            "horse": {
                "safe": True,
                "dosage": "Refer to product label - high-dose MSM formulation",
                "dosage_ja": "製品ラベル参照 - 高容量MSM配合",
                "notes": "For tendinitis, suspensory desmitis, post-training muscle recovery, wound healing, and equine hepatic/renal disease supportive nutrition. Synergistic with For Joint for comprehensive musculoskeletal support.",
                "notes_ja": "腱炎、繋靱帯炎、調教後の筋肉回復、創傷治癒、馬の肝腎疾患の栄養支持に。For Jointと併用で筋骨格全体のサポートに相乗効果。",
            },
            "rabbit": {
                "safe": True,
                "dosage": "Refer to product label; adjust for body weight",
                "dosage_ja": "製品ラベル参照。体重に応じて調整",
                "notes": "For GI stasis recovery, post-surgical care, OA with muscle wasting, and convalescence. Amino acids support hindgut fermentation.",
                "notes_ja": "GI stasis回復期、術後ケア、筋肉減少を伴うOA、回復期に。アミノ酸が後腸発酵をサポート。",
            },
            "ferret": {
                "safe": True,
                "dosage": "Refer to product label; start at low dose",
                "dosage_ja": "製品ラベル参照。低用量から開始",
                "notes": "For insulinoma-related muscle wasting, post-adrenalectomy recovery, and lymphoma supportive care.",
                "notes_ja": "インスリノーマ関連の筋肉減少、副腎摘出後の回復、リンパ腫の支持療法に。",
            },
            "hamster": {
                "safe": True,
                "dosage": "Minimal dose; refer to product label",
                "dosage_ja": "最小量。製品ラベル参照",
                "notes": "For senior hamsters with muscle wasting and post-trauma recovery.",
                "notes_ja": "筋肉減少や外傷後回復の高齢ハムスターに。",
            },
            "guinea_pig": {
                "safe": True,
                "dosage": "Minimal dose; refer to product label",
                "dosage_ja": "最小量。製品ラベル参照",
                "notes": "For pododermatitis healing, post-trauma recovery, and senior mobility support. Does not replace vitamin C supplementation.",
                "notes_ja": "足底皮膚炎の治癒、外傷後回復、高齢期の運動機能サポートに。ビタミンC補給の代替にはならない。",
            },
            "chinchilla": {
                "safe": True,
                "dosage": "Minimal dose; refer to product label",
                "dosage_ja": "最小量。製品ラベル参照",
                "notes": "For fur ring injury, dental disease recovery, and convalescence after GI/dental surgery.",
                "notes_ja": "ファーリング損傷、歯科疾患回復期、GI/歯科術後の回復期に。",
            },
            "hedgehog": {
                "safe": True,
                "dosage": "Minimal dose; refer to product label",
                "dosage_ja": "最小量。製品ラベル参照",
                "notes": "For WHS supportive care, post-surgical recovery, and neoplasia-related cachexia.",
                "notes_ja": "WHS支持療法、術後回復、腫瘍関連悪液質に。",
            },
            "sugar_glider": {
                "safe": True,
                "dosage": "Minimal dose; refer to product label",
                "dosage_ja": "最小量。製品ラベル参照",
                "notes": "For metabolic bone disease recovery, self-mutilation wound healing, and convalescence.",
                "notes_ja": "代謝性骨疾患回復期、自咬症の創傷治癒、回復期に。",
            },
            "degu": {
                "safe": True,
                "dosage": "Minimal dose; refer to product label",
                "dosage_ja": "最小量。製品ラベル参照",
                "notes": "For tail degloving recovery, post-surgical care, and OA-related muscle loss in seniors.",
                "notes_ja": "尾剥離後の回復、術後ケア、高齢デグーのOA関連筋肉減少に。",
            },
            "bird": {
                "safe": True,
                "dosage": "Refer to product label; adjust for body size",
                "dosage_ja": "製品ラベル参照。体格に応じて調整",
                "notes": "For post-surgical tissue repair, wound healing after trauma, and convalescence from chronic infection.",
                "notes_ja": "術後の組織修復、外傷後の創傷治癒、慢性感染からの回復期に。",
            },
            "parakeet": {
                "safe": True,
                "dosage": "Minimal dose; refer to product label",
                "dosage_ja": "最小量。製品ラベル参照",
                "notes": "For feather-pluck tissue repair, wound healing, and convalescence.",
                "notes_ja": "羽毛毟り組織修復、創傷治癒、回復期に。",
            },
            "parrot": {
                "safe": True,
                "dosage": "Refer to product label; adjust for body size",
                "dosage_ja": "製品ラベル参照。体格に応じて調整",
                "notes": "For post-surgical tissue repair, chronic wound healing, and supportive care for chronic infections.",
                "notes_ja": "術後の組織修復、慢性創傷の治癒、慢性感染の支持療法に。",
            },
        },
        "side_effects": ["generally well tolerated", "mild GI upset at initiation (rare)"],
        "side_effects_ja": ["一般的に忍容性良好", "開始時の軽度消化器症状（まれ）"],
        "contraindications": "None known at recommended doses. Use with caution in severe hepatic or renal failure (protein/amino acid load).",
        "contraindications_ja": "推奨用量では特に知られていない。重度の肝/腎不全ではタンパク質・アミノ酸負荷に注意し慎重に使用。",
        "drug_interactions": [],
        "sponsor": True,
        "sponsor_url": "https://www.caninevet.jp/canineサプリメント/msm-アミノコンプリート/",
        "sponsor_name": "Equine & Canine Vet Nutrition",
    },
    {
        "id": "ecvn_no_pain_quick_stop",
        "name": "No Pain Quick Stop (Equine & Canine Vet Nutrition)",
        "name_ja": "ノーペインクイックストップ（Equine & Canine Vet Nutrition）",
        "category": "antiseptics",
        "mechanism": "Hemostatic powder based on sodium cellulose glycolate and arginine. Rapidly stops bleeding from nail trims, minor cuts, and superficial wounds without causing pain (styptic).",
        "mechanism_ja": "カルボキシメチルセルロースナトリウムとアルギニンベースの止血パウダー。爪切り、小さな切り傷、表在性創傷からの出血を痛みなく迅速に止める（止血剤）。",
        "routes": ["Topical"],
        "routes_ja": ["局所"],
        "formulations": ["Powder"],
        "formulations_ja": ["粉末"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Apply directly to bleeding site",
                "dosage_ja": "出血部位に直接塗布",
                "notes": "Pain-free hemostatic powder. Ideal for nail quick bleeding, minor surgical sites, and superficial wounds.",
                "notes_ja": "痛みを与えない止血パウダー。爪の出血、小規模な手術部位、表在性創傷に最適。",
            },
            "cat": {
                "safe": True,
                "dosage": "Apply directly to bleeding site",
                "dosage_ja": "出血部位に直接塗布",
                "notes": "Safe for cats. Gentle formulation.",
                "notes_ja": "猫に安全。やさしい配合。",
            },
            "horse": {
                "safe": True,
                "dosage": "Apply directly to bleeding site",
                "dosage_ja": "出血部位に直接塗布",
                "notes": "For minor wounds and post-procedure hemostasis.",
                "notes_ja": "小さな傷や処置後の止血に。",
            },
        },
        "side_effects": ["generally well tolerated"],
        "side_effects_ja": ["一般的に忍容性良好"],
        "contraindications": "Not for deep or arterial bleeding.",
        "contraindications_ja": "深部出血や動脈出血には使用不可。",
        "drug_interactions": [],
        "sponsor": True,
        "sponsor_url": "https://www.caninevet.jp/",
        "sponsor_name": "Equine & Canine Vet Nutrition",
    },
    {
        "id": "ecvn_relax_cbd",
        "name": "Canine Vet Relax & CBD (Equine & Canine Vet Nutrition)",
        "name_ja": "Canine Vet Relax & CBD（Equine & Canine Vet Nutrition）",
        "category": "supplements",
        "mechanism": "Full-spectrum CBD (cannabidiol) supplement combined with calming botanicals. CBD acts on the endocannabinoid system (CB1/CB2 receptors) to modulate pain perception, anxiety, seizure threshold, and inflammation without psychoactive effects (negligible THC).",
        "mechanism_ja": "フルスペクトラムCBD（カンナビジオール）とリラックス系ボタニカルの複合製品。CBDは内因性カンナビノイド系（CB1/CB2受容体）に作用し、疼痛知覚・不安・発作閾値・炎症を調節。精神作用は無視できるレベル（THC極微量）。",
        "routes": ["PO"],
        "routes_ja": ["経口"],
        "formulations": ["Oil / Capsules"],
        "formulations_ja": ["オイル／カプセル"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Refer to product label; typical range 0.5-2 mg/kg PO q12h",
                "dosage_ja": "製品ラベル参照。一般的には0.5-2 mg/kg 経口 12時間毎",
                "notes": "For chronic pain (OA, IVDD, cancer), anxiety (separation, noise phobia), refractory epilepsy (CBD increases seizure threshold — Epidiolex evidence class), and end-of-life comfort care. Monitor liver enzymes with long-term use.",
                "notes_ja": "慢性疼痛（OA・IVDD・がん）、不安（分離不安・騒音恐怖）、難治性てんかん（CBDが発作閾値を上昇 — Epidiolexエビデンスクラス）、ターミナルケアに。長期使用時は肝酵素モニタリング。",
            },
            "cat": {
                "safe": True,
                "dosage": "Refer to product label; start at low dose 0.1-0.5 mg/kg PO q12h",
                "dosage_ja": "製品ラベル参照。0.1-0.5 mg/kg 経口 12時間毎で低用量開始",
                "notes": "For chronic pain and anxiety in cats. Cats are slower CBD metabolizers — start low. Monitor for ataxia/sedation.",
                "notes_ja": "猫の慢性疼痛と不安に。猫はCBD代謝が遅いため低用量から開始。運動失調・鎮静に注意。",
            },
            "horse": {
                "safe": True,
                "dosage": "Refer to product label; higher mg doses for body mass",
                "dosage_ja": "製品ラベル参照。体格に応じた高用量",
                "notes": "For anxiety (transport, stall rest), chronic musculoskeletal pain, and behavioral issues. Check FEI/competition regulations on CBD.",
                "notes_ja": "不安（輸送・厩舎安静）、慢性筋骨格痛、行動問題に。CBDに関するFEI・競技規則を確認。",
            },
            "rabbit": {
                "safe": True,
                "dosage": "Very low dose; refer to product label",
                "dosage_ja": "極低用量。製品ラベル参照",
                "notes": "For chronic pain (OA, spondylosis) and stress management. Limited species-specific data — use conservatively.",
                "notes_ja": "慢性疼痛（OA・脊椎症）とストレス管理に。種特異データ限定のため慎重に使用。",
            },
            "ferret": {
                "safe": True,
                "dosage": "Very low dose; refer to product label",
                "dosage_ja": "極低用量。製品ラベル参照",
                "notes": "For chronic pain and anxiety in ferrets with adrenal disease or lymphoma.",
                "notes_ja": "副腎疾患やリンパ腫のフェレットの慢性疼痛・不安に。",
            },
        },
        "side_effects": ["mild sedation", "mild GI upset", "elevated liver enzymes (long-term)"],
        "side_effects_ja": ["軽度鎮静", "軽度消化器症状", "肝酵素上昇（長期使用）"],
        "contraindications": "Severe hepatic dysfunction (CBD is hepatically metabolized via CYP450). Caution with concurrent CYP450 inhibitors.",
        "contraindications_ja": "重度肝機能障害（CBDはCYP450代謝）。CYP450阻害薬併用時は注意。",
        "drug_interactions": [
            {
                "drug": "CYP450 substrates (e.g., phenobarbital, warfarin)",
                "effect": "CBD inhibits CYP450 enzymes; may increase levels of co-administered drugs",
                "effect_ja": "CBDはCYP450を阻害し、併用薬の血中濃度を上昇させる可能性",
            }
        ],
        "sponsor": True,
        "sponsor_url": "https://www.caninevet.jp/",
        "sponsor_name": "Equine & Canine Vet Nutrition",
    },
    {
        "id": "ecvn_protain",
        "name": "Canine Vet Protain (Equine & Canine Vet Nutrition)",
        "name_ja": "Canine Vet Protain（Equine & Canine Vet Nutrition）",
        "category": "supplements",
        "mechanism": "High-quality protein supplement with collagen synthesis precursors. Designed to maintain lean muscle mass during weight loss, cancer cachexia, and post-surgical recovery. Provides essential amino acids and hydroxyproline for collagen/connective tissue support.",
        "mechanism_ja": "高品質タンパク質とコラーゲン合成前駆体を配合したサプリメント。減量中・がん悪液質・術後回復期の除脂肪体重維持に設計。必須アミノ酸とヒドロキシプロリンによる結合組織・コラーゲンサポートを提供。",
        "routes": ["PO"],
        "routes_ja": ["経口"],
        "formulations": ["Powder (mix with feed)"],
        "formulations_ja": ["粉末（飼料に混合）"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Refer to product label for body weight-based dosing",
                "dosage_ja": "体重に応じた製品ラベルの用量を参照",
                "notes": "For cancer cachexia (lymphoma, hemangiosarcoma, osteosarcoma, mammary tumor), post-orthopedic surgery (cruciate ligament repair), and obesity management (preserves muscle during weight loss).",
                "notes_ja": "がん悪液質（リンパ腫・血管肉腫・骨肉腫・乳腺腫瘍）、整形外科術後（十字靱帯修復）、肥満管理（減量中の筋肉維持）に。",
            },
            "cat": {
                "safe": True,
                "dosage": "Refer to product label; start at low dose",
                "dosage_ja": "製品ラベル参照。低用量から開始",
                "notes": "For feline cancer cachexia, post-surgical recovery, and senior muscle maintenance. Note: cats require higher protein intake than dogs — verify adequate total protein.",
                "notes_ja": "猫のがん悪液質、術後回復、高齢期の筋肉維持に。注：猫は犬より高タンパク要求。総タンパク摂取量を確認。",
            },
            "horse": {
                "safe": True,
                "dosage": "Refer to product label",
                "dosage_ja": "製品ラベル参照",
                "notes": "For equine post-surgical recovery, muscle wasting, and athletic conditioning.",
                "notes_ja": "馬の術後回復、筋萎縮、競技馬のコンディショニングに。",
            },
        },
        "side_effects": ["generally well tolerated"],
        "side_effects_ja": ["一般的に忍容性良好"],
        "contraindications": "Severe hepatic or renal failure (protein load).",
        "contraindications_ja": "重度の肝・腎不全（タンパク負荷）。",
        "drug_interactions": [],
        "sponsor": True,
        "sponsor_url": "https://www.caninevet.jp/",
        "sponsor_name": "Equine & Canine Vet Nutrition",
    },
    {
        "id": "ecvn_booster_relax",
        "name": "Canine Vet Booster & Relax (Equine & Canine Vet Nutrition)",
        "name_ja": "Canine Vet Booster & Relax（Equine & Canine Vet Nutrition）",
        "category": "supplements",
        "mechanism": "Vitality restoration supplement combining adaptogens, B-complex vitamins, and calming botanicals. Supports energy metabolism and immune function during convalescence while modulating stress response.",
        "mechanism_ja": "アダプトゲン、Bビタミン複合体、リラックス系ボタニカルを配合した活力回復サプリメント。回復期のエネルギー代謝と免疫機能をサポートしつつ、ストレス応答を調整。",
        "routes": ["PO"],
        "routes_ja": ["経口"],
        "formulations": ["Powder / Capsules"],
        "formulations_ja": ["粉末／カプセル"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Refer to product label for body weight-based dosing",
                "dosage_ja": "体重に応じた製品ラベルの用量を参照",
                "notes": "For convalescence from viral infection (distemper, parvo), hypothyroidism energy support, Addison's adjunct, and general fatigue in senior dogs.",
                "notes_ja": "ウイルス感染（ジステンパー・パルボ）からの回復期、甲状腺機能低下症のエネルギーサポート、アジソン病の補助療法、高齢犬の一般的疲労に。",
            },
            "cat": {
                "safe": True,
                "dosage": "Refer to product label; start at low dose",
                "dosage_ja": "製品ラベル参照。低用量から開始",
                "notes": "For post-infection recovery and chronic fatigue in senior cats.",
                "notes_ja": "感染後の回復期、高齢猫の慢性疲労に。",
            },
            "horse": {
                "safe": True,
                "dosage": "Refer to product label",
                "dosage_ja": "製品ラベル参照",
                "notes": "For fatigue, post-exercise recovery, and convalescence.",
                "notes_ja": "疲労、運動後回復、病後回復期に。",
            },
        },
        "side_effects": ["generally well tolerated"],
        "side_effects_ja": ["一般的に忍容性良好"],
        "contraindications": "None known at recommended doses.",
        "contraindications_ja": "推奨用量では特に知られていない。",
        "drug_interactions": [],
        "sponsor": True,
        "sponsor_url": "https://www.caninevet.jp/",
        "sponsor_name": "Equine & Canine Vet Nutrition",
    },
    {
        "id": "ecvn_kamide_milk",
        "name": "Kamide Milk (Equine & Canine Vet Nutrition)",
        "name_ja": "カミデミルク（Equine & Canine Vet Nutrition）",
        "category": "supplements",
        "mechanism": "Easily digestible liquid nutrition formulation. Designed for critical care / convalescent feeding with highly bioavailable protein, moderate fat, and complete micronutrients. Suitable for syringe/tube feeding.",
        "mechanism_ja": "消化吸収しやすい流動性栄養製品。生体利用率の高いタンパク質、適度な脂質、完全な微量栄養素を配合し、クリティカルケア・回復期給餌向けに設計。シリンジ・経管投与に適応。",
        "routes": ["PO", "NG tube", "E tube"],
        "routes_ja": ["経口", "経鼻胃管", "食道瘻管"],
        "formulations": ["Liquid / Powder (reconstitute)"],
        "formulations_ja": ["液体／粉末（溶解型）"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Refer to product label; typical 50-100 kcal/kg/day in recovery",
                "dosage_ja": "製品ラベル参照。回復期は50-100 kcal/kg/日が目安",
                "notes": "For anorexic/inappetent dogs, post-viral convalescence (parvo, distemper), pancreatitis (low-fat, easy digestion), megaesophagus (liquid swallows easier), and critical care feeding.",
                "notes_ja": "食欲不振・食欲低下犬、ウイルス感染後の回復期（パルボ・ジステンパー）、膵炎（低脂肪で消化しやすい）、巨大食道（液体は嚥下しやすい）、クリティカルケア給餌に。",
            },
            "cat": {
                "safe": True,
                "dosage": "Refer to product label",
                "dosage_ja": "製品ラベル参照",
                "notes": "For feline hepatic lipidosis (must feed calories early), anorexia, post-surgical feeding, and tube feeding support. Prevents hepatic lipidosis in anorexic cats.",
                "notes_ja": "猫の肝リピドーシス（早期の熱量投与が重要）、食欲不振、術後給餌、経管栄養サポートに。食欲不振猫の肝リピドーシスを予防。",
            },
            "horse": {
                "safe": True,
                "dosage": "Refer to product label for foals/convalescent horses",
                "dosage_ja": "子馬・回復期馬向けは製品ラベル参照",
                "notes": "For orphan/rejected foals, post-surgical enteral feeding, and convalescent nutrition in horses unable to eat solid feed.",
                "notes_ja": "孤児・母馬拒絶の子馬、術後経腸栄養、固形飼料を摂取できない回復期の馬に。",
            },
            "rabbit": {
                "safe": True,
                "dosage": "Minimal dose; refer to product label",
                "dosage_ja": "最小量。製品ラベル参照",
                "notes": "Critical care feeding for anorexic rabbits with GI stasis. Syringe-feed to maintain gut motility.",
                "notes_ja": "GI stasisの食欲不振ウサギのクリティカルケア給餌。シリンジ給餌で腸運動を維持。",
            },
            "ferret": {
                "safe": True,
                "dosage": "Refer to product label; start at low dose",
                "dosage_ja": "製品ラベル参照。低用量から開始",
                "notes": "For anorexic ferrets with insulinoma (prevents hypoglycemia) or post-surgical recovery.",
                "notes_ja": "インスリノーマ（低血糖予防）や術後回復の食欲不振フェレットに。",
            },
            "hamster": {
                "safe": True,
                "dosage": "Minimal dose; refer to product label",
                "dosage_ja": "最小量。製品ラベル参照",
                "notes": "For critical care feeding of debilitated hamsters.",
                "notes_ja": "衰弱したハムスターのクリティカルケア給餌に。",
            },
            "guinea_pig": {
                "safe": True,
                "dosage": "Minimal dose; refer to product label",
                "dosage_ja": "最小量。製品ラベル参照",
                "notes": "For anorexic guinea pigs with GI stasis or dental disease.",
                "notes_ja": "GI stasisや歯科疾患の食欲不振モルモットに。",
            },
            "chinchilla": {
                "safe": True,
                "dosage": "Minimal dose; refer to product label",
                "dosage_ja": "最小量。製品ラベル参照",
                "notes": "Critical care feeding for chinchillas with dental or GI disease.",
                "notes_ja": "歯科・消化器疾患のチンチラのクリティカルケア給餌に。",
            },
            "bird": {
                "safe": True,
                "dosage": "Refer to product label; adjust for body size",
                "dosage_ja": "製品ラベル参照。体格に応じて調整",
                "notes": "For hand-feeding chicks, anorexic adults, and crop feeding during illness.",
                "notes_ja": "雛の人工育雛、食欲不振成鳥、疾病時のそのう給餌に。",
            },
        },
        "side_effects": ["generally well tolerated", "osmotic diarrhea if diluted incorrectly"],
        "side_effects_ja": ["一般的に忍容性良好", "希釈不適切時の浸透圧性下痢"],
        "contraindications": "Complete intestinal obstruction. Severe pancreatitis (use reduced-fat version).",
        "contraindications_ja": "完全腸閉塞。重症膵炎では低脂肪配合を使用。",
        "drug_interactions": [],
        "sponsor": True,
        "sponsor_url": "https://www.caninevet.jp/",
        "sponsor_name": "Equine & Canine Vet Nutrition",
    },
    # ══════════════════════════════════════════════════════════════════════
    # 眼科薬 (Ophthalmic)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": "tobramycin_ophthalmic",
        "name": "Tobramycin (Ophthalmic)",
        "name_ja": "トブラマイシン（眼科用）",
        "category": "ophthalmic",
        "mechanism": "Aminoglycoside antibiotic eye drops; bactericidal against gram-negative organisms.",
        "mechanism_ja": "アミノグリコシド系抗生物質点眼薬。グラム陰性菌に殺菌作用。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "1 drop q6-8h in affected eye",
                "dosage_ja": "1滴 6-8時間毎 患眼に",
                "notes": "First-line for bacterial conjunctivitis/keratitis",
                "notes_ja": "細菌性結膜炎・角膜炎の第一選択",
            },
            "cat": {
                "safe": True,
                "dosage": "1 drop q6-8h in affected eye",
                "dosage_ja": "1滴 6-8時間毎 患眼に",
                "notes": "Safe for cats",
                "notes_ja": "猫に安全",
            },
            "horse": {
                "safe": True,
                "dosage": "1 drop q4-6h for corneal ulcers",
                "dosage_ja": "1滴 4-6時間毎 角膜潰瘍に",
                "notes": "Essential for equine ulcerative keratitis",
                "notes_ja": "馬の潰瘍性角膜炎に必須",
            },
        },
        "side_effects": ["mild ocular irritation"],
        "side_effects_ja": ["軽度の眼刺激"],
        "contraindications": "None significant for topical use.",
        "contraindications_ja": "局所使用では特になし。",
    },
    # ══════════════════════════════════════════════════════════════════════
    # 禁忌薬品リスト (Commonly Dangerous Drugs)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": "acetaminophen",
        "name": "Acetaminophen (Paracetamol/Tylenol)",
        "name_ja": "アセトアミノフェン（パラセタモール/タイレノール）",
        "category": "analgesics",
        "mechanism": "Analgesic/antipyretic; mechanism unclear but involves central COX inhibition and endocannabinoid system.",
        "mechanism_ja": "鎮痛・解熱薬。機序は不明だが中枢性COX阻害とエンドカンナビノイド系が関与。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "10-15 mg/kg PO q8-12h (short-term, with caution)",
                "dosage_ja": "10-15 mg/kg 経口 8-12時間毎（短期、注意して）",
                "notes": "Can be used in dogs with caution, but NSAIDs preferred. Hepatotoxicity risk.",
                "notes_ja": "犬には注意して使用可能だがNSAIDsが好ましい。肝毒性リスク。",
            },
            "cat": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "LETHAL TO CATS - even one dose can be fatal. Causes methemoglobinemia, Heinz body anemia, hepatic necrosis.",
                "notes_ja": "【猫に致死的】1回の投与でも死亡する可能性。メトヘモグロビン血症・ハインツ小体貧血・肝壊死を引き起こす。",
            },
            "snake": {
                "safe": False,
                "dosage": "N/A - used only as euthanasia/pest control for invasive species",
                "dosage_ja": "使用不可 - 侵略的外来種の安楽死/駆除のみ",
                "notes": "Toxic to reptiles",
                "notes_ja": "爬虫類に毒性",
            },
        },
        "side_effects": ["hepatotoxicity (dogs)", "methemoglobinemia (cats - LETHAL)", "renal damage"],
        "side_effects_ja": ["肝毒性（犬）", "メトヘモグロビン血症（猫 - 致死的）", "腎障害"],
        "contraindications": "ABSOLUTE CONTRAINDICATION IN CATS. Liver disease. Concurrent NSAID use.",
        "contraindications_ja": "猫への使用は絶対禁忌。肝疾患。NSAIDとの併用。",
    },
    {
        "id": "permethrin",
        "name": "Permethrin",
        "name_ja": "ペルメトリン",
        "category": "antiparasitics",
        "mechanism": "Synthetic pyrethroid; disrupts sodium channels in arthropod nervous system.",
        "mechanism_ja": "合成ピレスロイド。節足動物の神経系のナトリウムチャネルを破壊。",
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Per product label (spot-on or spray)",
                "dosage_ja": "製品ラベルに従う（スポットオンまたはスプレー）",
                "notes": "Safe for dogs at labeled doses",
                "notes_ja": "表示用量では犬に安全",
            },
            "cat": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "LETHAL TO CATS - causes severe neurotoxicity (tremors, seizures, death). Most common cat poisoning from well-meaning owners using dog products.",
                "notes_ja": "【猫に致死的】重度の神経毒性（振戦・痙攣・死亡）。善意で犬用製品を使用した飼い主による最も一般的な猫の中毒。",
            },
            "rabbit": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Toxic to rabbits",
                "notes_ja": "ウサギに毒性",
            },
            "bird": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Toxic to birds and aquatic organisms",
                "notes_ja": "鳥類・水生生物に毒性",
            },
        },
        "side_effects": ["cats: tremors, seizures, death", "dogs: generally safe"],
        "side_effects_ja": ["猫: 振戦・痙攣・死亡", "犬: 一般的に安全"],
        "contraindications": "ABSOLUTE CONTRAINDICATION IN CATS. Rabbits. Birds. Aquatic species.",
        "contraindications_ja": "猫への使用は絶対禁忌。ウサギ。鳥類。水棲動物。",
    },
    {
        "id": "ibuprofen",
        "name": "Ibuprofen (Advil/Motrin)",
        "name_ja": "イブプロフェン（アドビル/モトリン）",
        "category": "nsaids",
        "mechanism": "Non-selective COX inhibitor; OTC human NSAID.",
        "mechanism_ja": "非選択的COX阻害薬。ヒト用OTC NSAID。",
        "species_info": {
            "dog": {
                "safe": False,
                "dosage": "N/A - NOT recommended",
                "dosage_ja": "使用不可 - 推奨されない",
                "notes": "TOXIC TO DOGS - causes GI ulceration, renal failure at relatively low doses. Use veterinary NSAIDs instead.",
                "notes_ja": "【犬に毒性】比較的低用量で消化管潰瘍・腎不全を引き起こす。獣医用NSAIDsを使用すること。",
            },
            "cat": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "EXTREMELY TOXIC TO CATS - even small doses cause severe GI and renal damage",
                "notes_ja": "【猫に極めて毒性】少量でも重度の消化管・腎障害",
            },
            "ferret": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "CONTRAINDICATED in ferrets - GI ulceration",
                "notes_ja": "【禁忌】フェレットでは消化管潰瘍",
            },
        },
        "side_effects": ["GI ulceration", "renal failure", "hepatotoxicity", "coagulopathy"],
        "side_effects_ja": ["消化管潰瘍", "腎不全", "肝毒性", "凝固障害"],
        "contraindications": "ALL veterinary species - use veterinary-approved NSAIDs instead.",
        "contraindications_ja": "全ての動物種 - 獣医用承認NSAIDsを使用すること。",
    },
    {
        "id": "cefazolin",
        "name": "Cefazolin",
        "name_ja": "セファゾリン",
        "category": "antibiotics",
        "mechanism": "First-generation cephalosporin; inhibits bacterial cell wall synthesis.",
        "mechanism_ja": "第一世代セファロスポリン。細菌の細胞壁合成を阻害する。",
        "routes": ["IV", "IM"],
        "routes_ja": ["静脈内", "筋肉内"],
        "formulations": ["Injectable solution"],
        "formulations_ja": ["注射液"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "20-35 mg/kg IV/IM q8h",
                "dosage_ja": "20-35 mg/kg 静注/筋注 8時間毎",
                "notes": "Excellent perioperative antibiotic",
                "notes_ja": "周術期抗菌薬として優秀",
            },
            "cat": {
                "safe": True,
                "dosage": "20-35 mg/kg IV/IM q8h",
                "dosage_ja": "20-35 mg/kg 静注/筋注 8時間毎",
                "notes": "Standard perioperative use",
                "notes_ja": "標準的な周術期使用",
            },
            "horse": {
                "safe": True,
                "dosage": "11 mg/kg IV q8h",
                "dosage_ja": "11 mg/kg 静注 8時間毎",
                "notes": "Good for orthopedic surgery prophylaxis",
                "notes_ja": "整形外科手術の予防に適する",
            },
            "rabbit": {
                "safe": True,
                "dosage": "25-50 mg/kg IV/IM q8h",
                "dosage_ja": "25-50 mg/kg 静注/筋注 8時間毎",
                "notes": "Safe parenteral cephalosporin",
                "notes_ja": "安全な非経口セファロスポリン",
            },
            "ferret": {
                "safe": True,
                "dosage": "20-25 mg/kg IV/IM q8h",
                "dosage_ja": "20-25 mg/kg 静注/筋注 8時間毎",
                "notes": "Standard surgical prophylaxis",
                "notes_ja": "標準的な外科予防",
            },
            "bird": {
                "safe": True,
                "dosage": "50-100 mg/kg IM q6-8h",
                "dosage_ja": "50-100 mg/kg 筋注 6-8時間毎",
                "notes": "Higher doses needed",
                "notes_ja": "高用量が必要",
            },
        },
        "side_effects": ["pain at injection site", "rare allergic reaction"],
        "side_effects_ja": ["注射部位の疼痛", "まれなアレルギー反応"],
        "contraindications": "Known cephalosporin/penicillin allergy.",
        "contraindications_ja": "セファロスポリン/ペニシリンアレルギー。",
        "drug_interactions": [
            {
                "drug": "aminoglycosides",
                "effect": "Potential nephrotoxicity when combined",
                "effect_ja": "併用で腎毒性の可能性",
            }
        ],
    },
    {
        "id": "ceftriaxone",
        "name": "Ceftriaxone",
        "name_ja": "セフトリアキソン",
        "category": "antibiotics",
        "mechanism": "Third-generation cephalosporin with broad-spectrum activity including some gram-negatives.",
        "mechanism_ja": "グラム陰性菌を含む広域スペクトルを持つ第三世代セファロスポリン。",
        "routes": ["IV", "IM", "SC"],
        "routes_ja": ["静脈内", "筋肉内", "皮下"],
        "formulations": ["Injectable powder"],
        "formulations_ja": ["注射用粉末"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "25-50 mg/kg IV/IM/SC q12-24h",
                "dosage_ja": "25-50 mg/kg 静注/筋注/皮下 12-24時間毎",
                "notes": "Excellent for CNS infections",
                "notes_ja": "中枢神経系感染症に優秀",
            },
            "cat": {
                "safe": True,
                "dosage": "25-50 mg/kg IV/IM/SC q12-24h",
                "dosage_ja": "25-50 mg/kg 静注/筋注/皮下 12-24時間毎",
                "notes": "Good CNS penetration",
                "notes_ja": "良好な中枢神経系移行性",
            },
            "horse": {
                "safe": True,
                "dosage": "25-50 mg/kg IV q12h",
                "dosage_ja": "25-50 mg/kg 静注 12時間毎",
                "notes": "Used for serious infections",
                "notes_ja": "重症感染症に使用",
            },
            "rabbit": {
                "safe": True,
                "dosage": "25-50 mg/kg SC/IM q12-24h",
                "dosage_ja": "25-50 mg/kg 皮下/筋注 12-24時間毎",
                "notes": "Safe parenteral option",
                "notes_ja": "安全な非経口選択肢",
            },
            "bird": {
                "safe": True,
                "dosage": "50-100 mg/kg IM q12-24h",
                "dosage_ja": "50-100 mg/kg 筋注 12-24時間毎",
                "notes": "Used for severe infections",
                "notes_ja": "重症感染症に使用",
            },
            "reptile": {
                "safe": True,
                "dosage": "20-40 mg/kg IM q24-72h",
                "dosage_ja": "20-40 mg/kg 筋注 24-72時間毎",
                "notes": "Longer dosing intervals due to slow metabolism",
                "notes_ja": "代謝が遅いため投与間隔を延長",
            },
        },
        "side_effects": ["diarrhea", "pain at injection site", "hypersensitivity"],
        "side_effects_ja": ["下痢", "注射部位の疼痛", "過敏症"],
        "contraindications": "Cephalosporin allergy. Caution with calcium-containing IV fluids.",
        "contraindications_ja": "セファロスポリンアレルギー。カルシウム含有輸液との併用注意。",
        "drug_interactions": [
            {
                "drug": "calcium solutions",
                "effect": "Precipitate formation - do not mix",
                "effect_ja": "沈殿物形成 - 混合しないこと",
            }
        ],
    },
    {
        "id": "ceftiofur",
        "name": "Ceftiofur",
        "name_ja": "セフチオフル",
        "category": "antibiotics",
        "mechanism": "Third-generation cephalosporin developed specifically for veterinary use.",
        "mechanism_ja": "獣医学専用に開発された第三世代セファロスポリン。",
        "routes": ["IM", "SC"],
        "routes_ja": ["筋肉内", "皮下"],
        "formulations": ["Injectable suspension", "Injectable solution"],
        "formulations_ja": ["注射用懸濁液", "注射液"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "2.2 mg/kg SC q24h",
                "dosage_ja": "2.2 mg/kg 皮下 24時間毎",
                "notes": "Veterinary-specific cephalosporin",
                "notes_ja": "動物用セファロスポリン",
            },
            "cat": {
                "safe": True,
                "dosage": "2.2 mg/kg SC q24h",
                "dosage_ja": "2.2 mg/kg 皮下 24時間毎",
                "notes": "Well tolerated",
                "notes_ja": "忍容性良好",
            },
            "horse": {
                "safe": True,
                "dosage": "2.2-4.4 mg/kg IM/IV q12-24h",
                "dosage_ja": "2.2-4.4 mg/kg 筋注/静注 12-24時間毎",
                "notes": "FDA-approved for equine respiratory infections",
                "notes_ja": "馬の呼吸器感染症にFDA承認済",
            },
            "rabbit": {
                "safe": True,
                "dosage": "2.2 mg/kg SC q12-24h",
                "dosage_ja": "2.2 mg/kg 皮下 12-24時間毎",
                "notes": "Safe parenteral choice for rabbits",
                "notes_ja": "ウサギに安全な非経口抗菌薬",
            },
            "bird": {
                "safe": True,
                "dosage": "10-20 mg/kg IM q12-24h",
                "dosage_ja": "10-20 mg/kg 筋注 12-24時間毎",
                "notes": "Used in avian practice",
                "notes_ja": "鳥類診療で使用",
            },
            "reptile": {
                "safe": True,
                "dosage": "2.2 mg/kg IM q24-48h",
                "dosage_ja": "2.2 mg/kg 筋注 24-48時間毎",
                "notes": "Extended intervals for reptiles",
                "notes_ja": "爬虫類では投与間隔を延長",
            },
        },
        "side_effects": ["injection site reactions", "rare allergic reaction"],
        "side_effects_ja": ["注射部位反応", "まれなアレルギー反応"],
        "contraindications": "Cephalosporin hypersensitivity.",
        "contraindications_ja": "セファロスポリン過敏症。",
        "drug_interactions": [],
    },
    {
        "id": "lincomycin",
        "name": "Lincomycin",
        "name_ja": "リンコマイシン",
        "category": "antibiotics",
        "mechanism": "Lincosamide antibiotic; binds to 50S ribosomal subunit, inhibiting protein synthesis.",
        "mechanism_ja": "リンコサミド系抗生物質。50Sリボソームサブユニットに結合し蛋白合成を阻害する。",
        "routes": ["PO", "IM", "IV"],
        "routes_ja": ["経口", "筋肉内", "静脈内"],
        "formulations": ["Tablets", "Injectable solution", "Oral liquid"],
        "formulations_ja": ["錠剤", "注射液", "経口液"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "15-25 mg/kg PO q12h",
                "dosage_ja": "15-25 mg/kg 経口 12時間毎",
                "notes": "Effective against gram-positives and anaerobes",
                "notes_ja": "グラム陽性菌・嫌気性菌に有効",
            },
            "cat": {
                "safe": True,
                "dosage": "15-25 mg/kg PO q12h",
                "dosage_ja": "15-25 mg/kg 経口 12時間毎",
                "notes": "Similar to clindamycin use",
                "notes_ja": "クリンダマイシンと類似の使用",
            },
            "horse": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "CONTRAINDICATED - causes fatal colitis/enterocolitis",
                "notes_ja": "【禁忌】致死的な大腸炎/腸炎を引き起こす",
            },
            "rabbit": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "CONTRAINDICATED - causes fatal dysbiosis",
                "notes_ja": "【禁忌】致死的な腸内細菌叢異常",
            },
            "guinea_pig": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "CONTRAINDICATED - fatal enterotoxemia risk",
                "notes_ja": "【禁忌】致死的エンテロトキセミアのリスク",
            },
            "hamster": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "CONTRAINDICATED",
                "notes_ja": "【禁忌】",
            },
            "bird": {
                "safe": True,
                "dosage": "50-75 mg/kg PO/IM q12h",
                "dosage_ja": "50-75 mg/kg 経口/筋注 12時間毎",
                "notes": "Used for mycoplasma",
                "notes_ja": "マイコプラズマに使用",
            },
        },
        "side_effects": ["diarrhea", "vomiting", "pseudomembranous colitis"],
        "side_effects_ja": ["下痢", "嘔吐", "偽膜性大腸炎"],
        "contraindications": "Horses, rabbits, guinea pigs, hamsters, chinchillas (fatal dysbiosis).",
        "contraindications_ja": "馬・ウサギ・モルモット・ハムスター・チンチラ（致死的腸内細菌叢異常）。",
        "drug_interactions": [
            {"drug": "erythromycin", "effect": "Antagonistic - do not combine", "effect_ja": "拮抗作用 - 併用不可"}
        ],
    },
    {
        "id": "erythromycin",
        "name": "Erythromycin",
        "name_ja": "エリスロマイシン",
        "category": "antibiotics",
        "mechanism": "Macrolide antibiotic; binds 50S ribosomal subunit. Also has prokinetic effects.",
        "mechanism_ja": "マクロライド系抗生物質。50Sリボソームに結合。消化管運動促進作用もある。",
        "routes": ["PO", "IV", "topical"],
        "routes_ja": ["経口", "静脈内", "外用"],
        "formulations": ["Tablets", "Ophthalmic ointment", "Injectable"],
        "formulations_ja": ["錠剤", "眼軟膏", "注射剤"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "10-20 mg/kg PO q8-12h",
                "dosage_ja": "10-20 mg/kg 経口 8-12時間毎",
                "notes": "Prokinetic at low doses (0.5-1 mg/kg)",
                "notes_ja": "低用量(0.5-1 mg/kg)で消化管運動促進",
            },
            "cat": {
                "safe": True,
                "dosage": "10-15 mg/kg PO q8h",
                "dosage_ja": "10-15 mg/kg 経口 8時間毎",
                "notes": "GI side effects common",
                "notes_ja": "消化器副作用が多い",
            },
            "horse": {
                "safe": True,
                "dosage": "25 mg/kg PO q6-8h (foals)",
                "dosage_ja": "25 mg/kg 経口 6-8時間毎(子馬)",
                "notes": "Used in foals for Rhodococcus equi; adult horses risk fatal colitis",
                "notes_ja": "子馬のRhodococcus equi感染に使用。成馬では致死的大腸炎リスク",
            },
            "rabbit": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "CONTRAINDICATED orally - dysbiosis risk",
                "notes_ja": "【禁忌】経口投与 - 腸内細菌叢異常リスク",
            },
            "ferret": {
                "safe": True,
                "dosage": "10 mg/kg PO q8h",
                "dosage_ja": "10 mg/kg 経口 8時間毎",
                "notes": "Used for GI motility disorders",
                "notes_ja": "消化管運動障害に使用",
            },
            "bird": {
                "safe": True,
                "dosage": "40-60 mg/kg PO q8-12h",
                "dosage_ja": "40-60 mg/kg 経口 8-12時間毎",
                "notes": "Used for respiratory infections",
                "notes_ja": "呼吸器感染症に使用",
            },
        },
        "side_effects": ["GI upset", "vomiting", "diarrhea", "hepatotoxicity"],
        "side_effects_ja": ["消化器症状", "嘔吐", "下痢", "肝毒性"],
        "contraindications": "Rabbits, guinea pigs (oral). Hepatic dysfunction.",
        "contraindications_ja": "ウサギ・モルモット（経口）。肝機能障害。",
        "drug_interactions": [
            {"drug": "theophylline", "effect": "Increases theophylline levels", "effect_ja": "テオフィリン血中濃度上昇"}
        ],
    },
    {
        "id": "neomycin",
        "name": "Neomycin",
        "name_ja": "ネオマイシン",
        "category": "antibiotics",
        "mechanism": "Aminoglycoside; binds 30S ribosomal subunit. Poorly absorbed orally - used topically or for GI decontamination.",
        "mechanism_ja": "アミノグリコシド系。30Sリボソームに結合。経口吸収不良 - 外用またはGI除染に使用。",
        "routes": ["PO", "topical"],
        "routes_ja": ["経口", "外用"],
        "formulations": ["Tablets", "Topical ointment", "Oral solution"],
        "formulations_ja": ["錠剤", "外用軟膏", "経口液"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "10-20 mg/kg PO q6-12h (GI); topical q8-12h",
                "dosage_ja": "10-20 mg/kg 経口 6-12時間毎(GI用); 外用 8-12時間毎",
                "notes": "For hepatic encephalopathy and topical infections",
                "notes_ja": "肝性脳症および外用感染症に",
            },
            "cat": {
                "safe": True,
                "dosage": "10-20 mg/kg PO q6-12h",
                "dosage_ja": "10-20 mg/kg 経口 6-12時間毎",
                "notes": "Caution: ototoxic and nephrotoxic if absorbed systemically",
                "notes_ja": "注意: 全身吸収時に聴覚・腎毒性",
            },
            "horse": {
                "safe": True,
                "dosage": "4-8 mg/kg PO q6-12h",
                "dosage_ja": "4-8 mg/kg 経口 6-12時間毎",
                "notes": "For GI decontamination; avoid parenteral use",
                "notes_ja": "消化管除染用。非経口使用は避ける",
            },
            "rabbit": {
                "safe": True,
                "dosage": "30 mg/kg PO q12h",
                "dosage_ja": "30 mg/kg 経口 12時間毎",
                "notes": "Oral only; topical use safe",
                "notes_ja": "経口のみ。外用は安全",
            },
            "bird": {
                "safe": True,
                "dosage": "Topical application",
                "dosage_ja": "外用",
                "notes": "Topical use only; systemic aminoglycosides very toxic to birds",
                "notes_ja": "外用のみ。全身性アミノグリコシドは鳥類に非常に毒性",
            },
            "reptile": {
                "safe": True,
                "dosage": "Topical application",
                "dosage_ja": "外用",
                "notes": "Topical use; avoid systemic",
                "notes_ja": "外用。全身投与は避ける",
            },
        },
        "side_effects": ["nephrotoxicity", "ototoxicity", "neuromuscular blockade", "malabsorption"],
        "side_effects_ja": ["腎毒性", "聴覚毒性", "神経筋遮断", "吸収不良"],
        "contraindications": "Renal impairment. Do not use parenterally. Intestinal obstruction.",
        "contraindications_ja": "腎障害。非経口投与不可。腸閉塞。",
        "drug_interactions": [
            {"drug": "furosemide", "effect": "Increased ototoxicity risk", "effect_ja": "聴覚毒性リスク増加"},
            {"drug": "other aminoglycosides", "effect": "Additive toxicity", "effect_ja": "毒性の加算"},
        ],
    },
    {
        "id": "amikacin",
        "name": "Amikacin",
        "name_ja": "アミカシン",
        "category": "antibiotics",
        "mechanism": "Aminoglycoside; binds 30S ribosome. Broadest spectrum of aminoglycosides.",
        "mechanism_ja": "アミノグリコシド系。30Sリボソームに結合。アミノグリコシド中最も広いスペクトル。",
        "routes": ["IV", "IM", "SC"],
        "routes_ja": ["静脈内", "筋肉内", "皮下"],
        "formulations": ["Injectable solution"],
        "formulations_ja": ["注射液"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "15-30 mg/kg IV/IM/SC q24h",
                "dosage_ja": "15-30 mg/kg 静注/筋注/皮下 24時間毎",
                "notes": "Once-daily dosing preferred; monitor renal function",
                "notes_ja": "1日1回投与推奨。腎機能モニタリング",
            },
            "cat": {
                "safe": True,
                "dosage": "10-15 mg/kg IV/IM/SC q24h",
                "dosage_ja": "10-15 mg/kg 静注/筋注/皮下 24時間毎",
                "notes": "More sensitive to nephrotoxicity than dogs",
                "notes_ja": "犬より腎毒性に敏感",
            },
            "horse": {
                "safe": True,
                "dosage": "10-25 mg/kg IV/IM q24h",
                "dosage_ja": "10-25 mg/kg 静注/筋注 24時間毎",
                "notes": "Monitor renal values closely",
                "notes_ja": "腎機能値を厳密にモニタリング",
            },
            "rabbit": {
                "safe": True,
                "dosage": "8-16 mg/kg SC/IM q24h",
                "dosage_ja": "8-16 mg/kg 皮下/筋注 24時間毎",
                "notes": "Monitor for nephrotoxicity",
                "notes_ja": "腎毒性をモニタリング",
            },
            "bird": {
                "safe": True,
                "dosage": "15-20 mg/kg IM q12h",
                "dosage_ja": "15-20 mg/kg 筋注 12時間毎",
                "notes": "Important for Pseudomonas infections",
                "notes_ja": "緑膿菌感染症に重要",
            },
            "reptile": {
                "safe": True,
                "dosage": "5 mg/kg IM q48-72h",
                "dosage_ja": "5 mg/kg 筋注 48-72時間毎",
                "notes": "Extended intervals; ensure hydration",
                "notes_ja": "投与間隔延長。水分補給を確保",
            },
        },
        "side_effects": ["nephrotoxicity", "ototoxicity", "neuromuscular blockade"],
        "side_effects_ja": ["腎毒性", "聴覚毒性", "神経筋遮断"],
        "contraindications": "Dehydration. Pre-existing renal disease. Concurrent nephrotoxic drugs.",
        "contraindications_ja": "脱水。既存の腎疾患。腎毒性薬剤との併用。",
        "drug_interactions": [
            {"drug": "furosemide", "effect": "Increased nephro/ototoxicity", "effect_ja": "腎/聴覚毒性増加"},
            {"drug": "NSAIDs", "effect": "Increased nephrotoxicity risk", "effect_ja": "腎毒性リスク増加"},
        ],
    },
    {
        "id": "nitrofurantoin",
        "name": "Nitrofurantoin",
        "name_ja": "ニトロフラントイン",
        "category": "antibiotics",
        "mechanism": "Reduces to reactive intermediates that damage bacterial DNA. Concentrated in urine.",
        "mechanism_ja": "反応性中間体に還元され細菌DNAを損傷する。尿中に濃縮される。",
        "routes": ["PO"],
        "routes_ja": ["経口"],
        "formulations": ["Capsules", "Oral suspension"],
        "formulations_ja": ["カプセル", "経口懸濁液"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "4.4 mg/kg PO q8h",
                "dosage_ja": "4.4 mg/kg 経口 8時間毎",
                "notes": "Excellent for lower UTI",
                "notes_ja": "下部尿路感染症に優秀",
            },
            "cat": {
                "safe": True,
                "dosage": "4.4 mg/kg PO q8h",
                "dosage_ja": "4.4 mg/kg 経口 8時間毎",
                "notes": "Give with food to reduce GI upset",
                "notes_ja": "消化器症状軽減のため食事と共に投与",
            },
            "horse": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Not practical - urine concentration too variable",
                "notes_ja": "実用的でない。尿中濃度が不安定",
            },
            "rabbit": {
                "safe": True,
                "dosage": "4 mg/kg PO q12h",
                "dosage_ja": "4 mg/kg 経口 12時間毎",
                "notes": "Safe for rabbit UTIs",
                "notes_ja": "ウサギの尿路感染症に安全",
            },
            "ferret": {
                "safe": True,
                "dosage": "4.4 mg/kg PO q8h",
                "dosage_ja": "4.4 mg/kg 経口 8時間毎",
                "notes": "For urinary tract infections",
                "notes_ja": "尿路感染症に",
            },
            "guinea_pig": {
                "safe": True,
                "dosage": "5 mg/kg PO q12h",
                "dosage_ja": "5 mg/kg 経口 12時間毎",
                "notes": "For UTIs",
                "notes_ja": "尿路感染症に",
            },
        },
        "side_effects": ["GI upset", "hepatotoxicity (chronic use)", "pulmonary reactions"],
        "side_effects_ja": ["消化器症状", "肝毒性(長期使用)", "肺反応"],
        "contraindications": "Renal impairment (drug requires renal concentration). Pregnancy.",
        "contraindications_ja": "腎障害（腎濃縮が必要）。妊娠中。",
        "drug_interactions": [],
    },
    {
        "id": "polymyxin_b",
        "name": "Polymyxin B",
        "name_ja": "ポリミキシンB",
        "category": "antibiotics",
        "mechanism": "Polypeptide antibiotic; disrupts gram-negative bacterial cell membranes.",
        "mechanism_ja": "ポリペプチド系抗生物質。グラム陰性菌の細胞膜を破壊する。",
        "routes": ["topical", "ophthalmic"],
        "routes_ja": ["外用", "点眼"],
        "formulations": ["Ophthalmic drops", "Topical ointment", "Otic solution"],
        "formulations_ja": ["点眼液", "外用軟膏", "耳用液"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Topical: apply q8-12h",
                "dosage_ja": "外用: 8-12時間毎に塗布",
                "notes": "Commonly used in combination topical products",
                "notes_ja": "外用配合製品として広く使用",
            },
            "cat": {
                "safe": True,
                "dosage": "Topical/ophthalmic: apply q8-12h",
                "dosage_ja": "外用/点眼: 8-12時間毎",
                "notes": "Safe for topical use",
                "notes_ja": "外用として安全",
            },
            "horse": {
                "safe": True,
                "dosage": "Topical/ophthalmic use",
                "dosage_ja": "外用/点眼",
                "notes": "For eye and wound infections",
                "notes_ja": "眼および創傷感染症に",
            },
            "rabbit": {
                "safe": True,
                "dosage": "Topical: apply q8-12h",
                "dosage_ja": "外用: 8-12時間毎",
                "notes": "Topical only",
                "notes_ja": "外用のみ",
            },
            "bird": {
                "safe": True,
                "dosage": "Ophthalmic: 1 drop q6-8h",
                "dosage_ja": "点眼: 1滴 6-8時間毎",
                "notes": "Safe for topical/ophthalmic",
                "notes_ja": "外用/点眼として安全",
            },
            "reptile": {
                "safe": True,
                "dosage": "Topical application",
                "dosage_ja": "外用",
                "notes": "For shell/skin infections",
                "notes_ja": "甲羅/皮膚感染症に",
            },
        },
        "side_effects": ["local irritation", "nephrotoxicity (systemic only)", "neurotoxicity (systemic only)"],
        "side_effects_ja": ["局所刺激", "腎毒性(全身投与のみ)", "神経毒性(全身投与のみ)"],
        "contraindications": "Do not use systemically - severe nephro/neurotoxicity. Topical use only.",
        "contraindications_ja": "全身投与不可 - 重度の腎/神経毒性。外用のみ。",
        "drug_interactions": [],
    },
    {
        "id": "mupirocin",
        "name": "Mupirocin",
        "name_ja": "ムピロシン",
        "category": "antibiotics",
        "mechanism": "Inhibits bacterial isoleucyl-tRNA synthetase. Effective against Staphylococcus.",
        "mechanism_ja": "細菌のイソロイシルtRNA合成酵素を阻害する。ブドウ球菌に有効。",
        "routes": ["topical"],
        "routes_ja": ["外用"],
        "formulations": ["Topical ointment 2%"],
        "formulations_ja": ["外用軟膏2%"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Apply thin layer q8-12h",
                "dosage_ja": "薄く塗布 8-12時間毎",
                "notes": "Excellent for superficial pyoderma, MRSP",
                "notes_ja": "表在性膿皮症・MRSPに優秀",
            },
            "cat": {
                "safe": True,
                "dosage": "Apply thin layer q8-12h",
                "dosage_ja": "薄く塗布 8-12時間毎",
                "notes": "Safe topically; avoid ingestion",
                "notes_ja": "外用として安全。摂取を避ける",
            },
            "horse": {
                "safe": True,
                "dosage": "Apply to affected area q12h",
                "dosage_ja": "患部に12時間毎に塗布",
                "notes": "For wound infections",
                "notes_ja": "創傷感染症に",
            },
            "rabbit": {
                "safe": True,
                "dosage": "Apply q12h",
                "dosage_ja": "12時間毎に塗布",
                "notes": "Use E-collar to prevent ingestion",
                "notes_ja": "摂取防止にエリザベスカラー使用",
            },
            "ferret": {
                "safe": True,
                "dosage": "Apply q12h",
                "dosage_ja": "12時間毎に塗布",
                "notes": "Topical use safe",
                "notes_ja": "外用として安全",
            },
            "hedgehog": {
                "safe": True,
                "dosage": "Apply q12h",
                "dosage_ja": "12時間毎に塗布",
                "notes": "Useful for skin infections",
                "notes_ja": "皮膚感染症に有用",
            },
        },
        "side_effects": ["local irritation", "rare contact dermatitis"],
        "side_effects_ja": ["局所刺激", "まれな接触性皮膚炎"],
        "contraindications": "Large open wounds (polyethylene glycol base can be absorbed).",
        "contraindications_ja": "大きな開放創（ポリエチレングリコール基剤が吸収される可能性）。",
        "drug_interactions": [],
    },
    {
        "id": "nystatin",
        "name": "Nystatin",
        "name_ja": "ナイスタチン",
        "category": "antifungals",
        "mechanism": "Polyene antifungal; binds ergosterol in fungal cell membranes causing cell lysis.",
        "mechanism_ja": "ポリエン系抗真菌薬。真菌細胞膜のエルゴステロールに結合し細胞溶解を起こす。",
        "routes": ["PO", "topical"],
        "routes_ja": ["経口", "外用"],
        "formulations": ["Oral suspension", "Topical cream", "Tablets"],
        "formulations_ja": ["経口懸濁液", "外用クリーム", "錠剤"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "100,000 U/kg PO q6-8h",
                "dosage_ja": "100,000 U/kg 経口 6-8時間毎",
                "notes": "Not absorbed systemically; for GI candidiasis",
                "notes_ja": "全身吸収されない。消化管カンジダ症に",
            },
            "cat": {
                "safe": True,
                "dosage": "100,000 U/cat PO q6-8h",
                "dosage_ja": "100,000 U/匹 経口 6-8時間毎",
                "notes": "For oral/GI candidiasis",
                "notes_ja": "口腔/消化管カンジダ症に",
            },
            "horse": {
                "safe": True,
                "dosage": "Topical application",
                "dosage_ja": "外用",
                "notes": "For superficial fungal infections",
                "notes_ja": "表在性真菌感染症に",
            },
            "rabbit": {
                "safe": True,
                "dosage": "100,000 U PO q6-8h",
                "dosage_ja": "100,000 U 経口 6-8時間毎",
                "notes": "Safe for GI yeast overgrowth",
                "notes_ja": "消化管真菌過増殖に安全",
            },
            "bird": {
                "safe": True,
                "dosage": "300,000 U/kg PO q8-12h",
                "dosage_ja": "300,000 U/kg 経口 8-12時間毎",
                "notes": "Common for crop candidiasis",
                "notes_ja": "素嚢カンジダ症に一般的",
            },
            "reptile": {
                "safe": True,
                "dosage": "100,000 U/kg PO q24h",
                "dosage_ja": "100,000 U/kg 経口 24時間毎",
                "notes": "For GI fungal infections",
                "notes_ja": "消化管真菌感染症に",
            },
        },
        "side_effects": ["GI upset", "nausea", "vomiting"],
        "side_effects_ja": ["消化器症状", "悪心", "嘔吐"],
        "contraindications": "None significant for topical/oral use.",
        "contraindications_ja": "外用/経口使用では特になし。",
        "drug_interactions": [],
    },
    {
        "id": "miconazole",
        "name": "Miconazole",
        "name_ja": "ミコナゾール",
        "category": "antifungals",
        "mechanism": "Imidazole antifungal; inhibits ergosterol synthesis via cytochrome P450 14-alpha-demethylase.",
        "mechanism_ja": "イミダゾール系抗真菌薬。チトクロムP450 14α-脱メチル化酵素を介してエルゴステロール合成を阻害。",
        "routes": ["topical", "otic"],
        "routes_ja": ["外用", "耳用"],
        "formulations": ["Topical cream", "Topical spray", "Otic solution", "Shampoo"],
        "formulations_ja": ["外用クリーム", "外用スプレー", "耳用液", "シャンプー"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Apply q12-24h topically",
                "dosage_ja": "外用 12-24時間毎に塗布",
                "notes": "Common in combination ear products; for dermatophytosis",
                "notes_ja": "耳用配合製品に一般的。皮膚糸状菌症に",
            },
            "cat": {
                "safe": True,
                "dosage": "Apply q12-24h topically",
                "dosage_ja": "外用 12-24時間毎に塗布",
                "notes": "Safe topically for ringworm",
                "notes_ja": "外用として皮膚糸状菌症に安全",
            },
            "horse": {
                "safe": True,
                "dosage": "Apply q12-24h",
                "dosage_ja": "12-24時間毎に塗布",
                "notes": "For girth itch, rain rot fungal component",
                "notes_ja": "帯状皮膚炎、レインロットの真菌成分に",
            },
            "rabbit": {
                "safe": True,
                "dosage": "Apply q12-24h",
                "dosage_ja": "12-24時間毎に塗布",
                "notes": "Topical use safe",
                "notes_ja": "外用として安全",
            },
            "guinea_pig": {
                "safe": True,
                "dosage": "Apply q12-24h",
                "dosage_ja": "12-24時間毎に塗布",
                "notes": "For dermatophytosis",
                "notes_ja": "皮膚糸状菌症に",
            },
            "hedgehog": {
                "safe": True,
                "dosage": "Apply q12-24h",
                "dosage_ja": "12-24時間毎に塗布",
                "notes": "For dermatophytosis",
                "notes_ja": "皮膚糸状菌症に",
            },
        },
        "side_effects": ["local irritation", "contact dermatitis"],
        "side_effects_ja": ["局所刺激", "接触性皮膚炎"],
        "contraindications": "Known hypersensitivity to azole antifungals.",
        "contraindications_ja": "アゾール系抗真菌薬に対する過敏症。",
        "drug_interactions": [],
    },
    {
        "id": "clotrimazole",
        "name": "Clotrimazole",
        "name_ja": "クロトリマゾール",
        "category": "antifungals",
        "mechanism": "Imidazole antifungal; inhibits ergosterol synthesis. Used topically.",
        "mechanism_ja": "イミダゾール系抗真菌薬。エルゴステロール合成を阻害。外用で使用。",
        "routes": ["topical", "intranasal"],
        "routes_ja": ["外用", "鼻腔内"],
        "formulations": ["Topical cream", "Topical solution", "Nasal infusion"],
        "formulations_ja": ["外用クリーム", "外用液", "鼻腔内注入"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Apply topically q12h; intranasal infusion for aspergillosis",
                "dosage_ja": "外用 12時間毎; アスペルギルス症に鼻腔内注入",
                "notes": "Gold standard for nasal aspergillosis (topical infusion)",
                "notes_ja": "鼻腔アスペルギルス症のゴールドスタンダード（局所注入）",
            },
            "cat": {
                "safe": True,
                "dosage": "Apply topically q12h",
                "dosage_ja": "外用 12時間毎",
                "notes": "For dermatophytosis",
                "notes_ja": "皮膚糸状菌症に",
            },
            "horse": {
                "safe": True,
                "dosage": "Apply topically q12h",
                "dosage_ja": "外用 12時間毎",
                "notes": "For superficial fungal infections",
                "notes_ja": "表在性真菌感染症に",
            },
            "rabbit": {
                "safe": True,
                "dosage": "Apply topically q12h",
                "dosage_ja": "外用 12時間毎",
                "notes": "Safe topically",
                "notes_ja": "外用として安全",
            },
            "guinea_pig": {
                "safe": True,
                "dosage": "Apply topically q12h",
                "dosage_ja": "外用 12時間毎",
                "notes": "For dermatophyte infections",
                "notes_ja": "皮膚糸状菌感染症に",
            },
            "bird": {
                "safe": True,
                "dosage": "Apply topically q12h",
                "dosage_ja": "外用 12時間毎",
                "notes": "For superficial fungal lesions",
                "notes_ja": "表在性真菌病変に",
            },
        },
        "side_effects": ["local irritation", "erythema"],
        "side_effects_ja": ["局所刺激", "紅斑"],
        "contraindications": "None significant for topical use.",
        "contraindications_ja": "外用では特になし。",
        "drug_interactions": [],
    },
    {
        "id": "lufenuron",
        "name": "Lufenuron",
        "name_ja": "ルフェヌロン",
        "category": "antiparasitics",
        "mechanism": "Chitin synthesis inhibitor; prevents flea egg/larval development.",
        "mechanism_ja": "キチン合成阻害剤。ノミの卵/幼虫の発育を阻止する。",
        "routes": ["PO", "SC"],
        "routes_ja": ["経口", "皮下"],
        "formulations": ["Tablets", "Oral suspension", "Injectable (cats)"],
        "formulations_ja": ["錠剤", "経口懸濁液", "注射剤(猫)"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "10 mg/kg PO monthly",
                "dosage_ja": "10 mg/kg 経口 月1回",
                "notes": "Insect growth regulator; does not kill adult fleas",
                "notes_ja": "昆虫成長調節剤。成虫ノミは駆除しない",
            },
            "cat": {
                "safe": True,
                "dosage": "30 mg/kg PO monthly or 10 mg/kg SC q6mo",
                "dosage_ja": "30 mg/kg 経口 月1回 または 10 mg/kg 皮下 6ヶ月毎",
                "notes": "Injectable form available for cats",
                "notes_ja": "猫用注射剤あり",
            },
            "rabbit": {
                "safe": True,
                "dosage": "30 mg/kg PO monthly",
                "dosage_ja": "30 mg/kg 経口 月1回",
                "notes": "Off-label; anecdotal safety",
                "notes_ja": "適応外使用。経験的に安全",
            },
            "ferret": {
                "safe": True,
                "dosage": "30 mg/kg PO monthly",
                "dosage_ja": "30 mg/kg 経口 月1回",
                "notes": "Off-label use",
                "notes_ja": "適応外使用",
            },
            "guinea_pig": {
                "safe": True,
                "dosage": "30 mg/kg PO monthly",
                "dosage_ja": "30 mg/kg 経口 月1回",
                "notes": "Off-label",
                "notes_ja": "適応外使用",
            },
            "bird": {
                "safe": True,
                "dosage": "0.5 mg/mL in drinking water",
                "dosage_ja": "0.5 mg/mL 飲水に添加",
                "notes": "For feather mites prevention",
                "notes_ja": "羽毛ダニ予防に",
            },
        },
        "side_effects": ["rare GI upset"],
        "side_effects_ja": ["まれな消化器症状"],
        "contraindications": "None significant. Does not kill adult parasites.",
        "contraindications_ja": "特になし。成虫寄生虫は駆除しない。",
        "drug_interactions": [],
    },
    {
        "id": "pyrantel",
        "name": "Pyrantel Pamoate",
        "name_ja": "ピランテルパモ酸塩",
        "category": "antiparasitics",
        "mechanism": "Depolarizing neuromuscular blocking agent for nematodes; causes spastic paralysis of worms.",
        "mechanism_ja": "線虫に対する脱分極性神経筋遮断薬。虫体の痙性麻痺を引き起こす。",
        "routes": ["PO"],
        "routes_ja": ["経口"],
        "formulations": ["Oral suspension", "Tablets", "Paste"],
        "formulations_ja": ["経口懸濁液", "錠剤", "ペースト"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "5-10 mg/kg PO once; repeat in 2-3 weeks",
                "dosage_ja": "5-10 mg/kg 経口 1回; 2-3週後に再投与",
                "notes": "For roundworms and hookworms; very safe",
                "notes_ja": "回虫・鉤虫に。非常に安全",
            },
            "cat": {
                "safe": True,
                "dosage": "5-10 mg/kg PO once; repeat in 2-3 weeks",
                "dosage_ja": "5-10 mg/kg 経口 1回; 2-3週後に再投与",
                "notes": "Safe for kittens from 2 weeks of age",
                "notes_ja": "生後2週齢の子猫から安全",
            },
            "horse": {
                "safe": True,
                "dosage": "6.6 mg/kg PO once",
                "dosage_ja": "6.6 mg/kg 経口 1回",
                "notes": "For small strongyles and ascarids",
                "notes_ja": "小型円虫・回虫に",
            },
            "rabbit": {
                "safe": True,
                "dosage": "5-10 mg/kg PO; repeat in 10-14 days",
                "dosage_ja": "5-10 mg/kg 経口; 10-14日後に再投与",
                "notes": "For Passalurus ambiguus (pinworms)",
                "notes_ja": "ウサギ蟯虫に",
            },
            "bird": {
                "safe": True,
                "dosage": "7 mg/kg PO; repeat in 14 days",
                "dosage_ja": "7 mg/kg 経口; 14日後に再投与",
                "notes": "For roundworms; very safe in birds",
                "notes_ja": "回虫に。鳥類で非常に安全",
            },
            "ferret": {
                "safe": True,
                "dosage": "4.4 mg/kg PO; repeat in 14 days",
                "dosage_ja": "4.4 mg/kg 経口; 14日後に再投与",
                "notes": "For hookworms and roundworms",
                "notes_ja": "鉤虫・回虫に",
            },
        },
        "side_effects": ["rare GI upset", "rare vomiting"],
        "side_effects_ja": ["まれな消化器症状", "まれな嘔吐"],
        "contraindications": "Do not combine with levamisole or morantel (similar mechanism).",
        "contraindications_ja": "レバミゾールまたはモランテルとの併用不可（類似の作用機序）。",
        "drug_interactions": [
            {"drug": "levamisole", "effect": "Antagonistic - do not combine", "effect_ja": "拮抗作用 - 併用不可"},
            {"drug": "piperazine", "effect": "Antagonistic effects", "effect_ja": "拮抗作用"},
        ],
    },
    {
        "id": "sarolaner",
        "name": "Sarolaner",
        "name_ja": "サロラネル",
        "category": "antiparasitics",
        "mechanism": "Isoxazoline; inhibits GABA and glutamate-gated chloride channels in arthropod nervous system.",
        "mechanism_ja": "イソオキサゾリン系。節足動物のGABAおよびグルタミン酸依存性塩素チャネルを阻害。",
        "routes": ["PO"],
        "routes_ja": ["経口"],
        "formulations": ["Chewable tablets (Simparica)"],
        "formulations_ja": ["チュアブル錠（シンパリカ）"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "2 mg/kg PO monthly",
                "dosage_ja": "2 mg/kg 経口 月1回",
                "notes": "FDA-approved (Simparica); for fleas, ticks, mites",
                "notes_ja": "FDA承認（シンパリカ）。ノミ・ダニ・疥癬に",
            },
            "cat": {
                "safe": True,
                "dosage": "1.2 mg/kg topical monthly (Simparica Trio for cats)",
                "dosage_ja": "1.2 mg/kg 外用 月1回",
                "notes": "Available in combination product",
                "notes_ja": "配合製品で利用可能",
            },
            "horse": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Not approved for horses",
                "notes_ja": "馬には未承認",
            },
            "rabbit": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Safety not established in rabbits",
                "notes_ja": "ウサギでの安全性は確立されていない",
            },
            "ferret": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Not approved; safety not established",
                "notes_ja": "未承認。安全性未確立",
            },
            "bird": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Toxic to birds",
                "notes_ja": "鳥類に毒性",
            },
        },
        "side_effects": ["vomiting", "diarrhea", "lethargy", "rare seizures"],
        "side_effects_ja": ["嘔吐", "下痢", "元気消失", "まれに痙攣"],
        "contraindications": "Dogs with history of seizures (use with caution). Not for use in cats <6 months.",
        "contraindications_ja": "痙攣歴のある犬（慎重投与）。6ヶ月齢未満の猫には使用不可。",
        "drug_interactions": [],
    },
    {
        "id": "afoxolaner",
        "name": "Afoxolaner",
        "name_ja": "アフォキソラネル",
        "category": "antiparasitics",
        "mechanism": "Isoxazoline; inhibits GABA-gated chloride channels in ectoparasites.",
        "mechanism_ja": "イソオキサゾリン系。外部寄生虫のGABA依存性塩素チャネルを阻害。",
        "routes": ["PO"],
        "routes_ja": ["経口"],
        "formulations": ["Chewable tablets (NexGard)"],
        "formulations_ja": ["チュアブル錠（ネクスガード）"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "2.5 mg/kg PO monthly",
                "dosage_ja": "2.5 mg/kg 経口 月1回",
                "notes": "FDA-approved (NexGard); for fleas and ticks",
                "notes_ja": "FDA承認（ネクスガード）。ノミ・ダニに",
            },
            "cat": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Not approved for cats (NexGard dog formulation)",
                "notes_ja": "猫用未承認（犬用ネクスガード製剤）",
            },
            "horse": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Not approved",
                "notes_ja": "未承認",
            },
            "rabbit": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Safety not established",
                "notes_ja": "安全性未確立",
            },
            "ferret": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Not approved",
                "notes_ja": "未承認",
            },
            "bird": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Toxic to avian species",
                "notes_ja": "鳥類に毒性",
            },
        },
        "side_effects": ["vomiting", "diarrhea", "lethargy", "decreased appetite", "seizures (rare)"],
        "side_effects_ja": ["嘔吐", "下痢", "元気消失", "食欲低下", "痙攣(まれ)"],
        "contraindications": "Dogs with history of seizures. Not for puppies <8 weeks or <2 kg.",
        "contraindications_ja": "痙攣歴のある犬。8週齢未満または2kg未満の子犬。",
        "drug_interactions": [],
    },
    {
        "id": "imidacloprid",
        "name": "Imidacloprid",
        "name_ja": "イミダクロプリド",
        "category": "antiparasitics",
        "mechanism": "Neonicotinoid; binds nicotinic acetylcholine receptors in insects, causing paralysis.",
        "mechanism_ja": "ネオニコチノイド系。昆虫のニコチン性アセチルコリン受容体に結合し麻痺を引き起こす。",
        "routes": ["topical"],
        "routes_ja": ["外用"],
        "formulations": ["Spot-on solution (Advantage)"],
        "formulations_ja": ["スポットオン液（アドバンテージ）"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "10 mg/kg topical monthly",
                "dosage_ja": "10 mg/kg 外用 月1回",
                "notes": "For fleas; often combined with moxidectin (Advocate)",
                "notes_ja": "ノミに。モキシデクチンとの配合剤あり（アドボケート）",
            },
            "cat": {
                "safe": True,
                "dosage": "10 mg/kg topical monthly",
                "dosage_ja": "10 mg/kg 外用 月1回",
                "notes": "Safe for cats; for fleas",
                "notes_ja": "猫に安全。ノミに",
            },
            "rabbit": {
                "safe": True,
                "dosage": "10-20 mg/kg topical monthly",
                "dosage_ja": "10-20 mg/kg 外用 月1回",
                "notes": "Off-label but widely used for fleas in rabbits",
                "notes_ja": "適応外だがウサギのノミに広く使用",
            },
            "ferret": {
                "safe": True,
                "dosage": "10 mg/kg topical monthly",
                "dosage_ja": "10 mg/kg 外用 月1回",
                "notes": "Advantage approved for ferrets in some countries",
                "notes_ja": "一部の国でフェレットにアドバンテージ承認",
            },
            "guinea_pig": {
                "safe": True,
                "dosage": "10 mg/kg topical monthly",
                "dosage_ja": "10 mg/kg 外用 月1回",
                "notes": "Off-label; commonly used",
                "notes_ja": "適応外。一般的に使用",
            },
            "bird": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Not recommended for birds",
                "notes_ja": "鳥類には推奨されない",
            },
        },
        "side_effects": ["transient skin irritation", "rare lethargy"],
        "side_effects_ja": ["一過性の皮膚刺激", "まれな元気消失"],
        "contraindications": "Kittens/puppies <8 weeks.",
        "contraindications_ja": "8週齢未満の子猫/子犬。",
        "drug_interactions": [],
    },
    {
        "id": "emodepside",
        "name": "Emodepside",
        "name_ja": "エモデプシド",
        "category": "antiparasitics",
        "mechanism": "Cyclic depsipeptide; stimulates presynaptic latrophilin receptors causing paralysis of nematodes.",
        "mechanism_ja": "環状デプシペプチド。前シナプスのラトロフィリン受容体を刺激し線虫の麻痺を引き起こす。",
        "routes": ["topical", "PO"],
        "routes_ja": ["外用", "経口"],
        "formulations": ["Spot-on (Profender with praziquantel)", "Oral solution"],
        "formulations_ja": ["スポットオン（プロフェンダー・プラジクアンテル配合）", "経口液"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "1 mg/kg PO once",
                "dosage_ja": "1 mg/kg 経口 1回",
                "notes": "For roundworms, hookworms; newer anthelmintic",
                "notes_ja": "回虫・鉤虫に。新しい駆虫薬",
            },
            "cat": {
                "safe": True,
                "dosage": "3 mg/kg topical once (Profender)",
                "dosage_ja": "3 mg/kg 外用 1回（プロフェンダー）",
                "notes": "Combined with praziquantel in Profender",
                "notes_ja": "プロフェンダーでプラジクアンテルと配合",
            },
            "horse": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Not approved for equines",
                "notes_ja": "馬類には未承認",
            },
            "rabbit": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Safety not established",
                "notes_ja": "安全性未確立",
            },
            "ferret": {
                "safe": True,
                "dosage": "Cat dose topical off-label",
                "dosage_ja": "猫用量を外用（適応外）",
                "notes": "Off-label use",
                "notes_ja": "適応外使用",
            },
            "bird": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Not studied in birds",
                "notes_ja": "鳥類では未研究",
            },
        },
        "side_effects": ["transient salivation (cats, if licked)", "vomiting", "diarrhea"],
        "side_effects_ja": ["一過性の流涎(猫、舐めた場合)", "嘔吐", "下痢"],
        "contraindications": "Kittens <8 weeks or <0.5 kg.",
        "contraindications_ja": "8週齢未満または0.5kg未満の子猫。",
        "drug_interactions": [],
    },
    {
        "id": "tepoxalin",
        "name": "Tepoxalin",
        "name_ja": "テポキサリン",
        "category": "nsaids",
        "mechanism": "Dual COX/LOX inhibitor; inhibits both cyclooxygenase and 5-lipoxygenase.",
        "mechanism_ja": "デュアルCOX/LOX阻害薬。シクロオキシゲナーゼと5-リポキシゲナーゼの両方を阻害。",
        "routes": ["PO"],
        "routes_ja": ["経口"],
        "formulations": ["Rapidly disintegrating tablets (Zubrin)"],
        "formulations_ja": ["速崩壊錠（ズブリン）"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "10-20 mg/kg PO q24h (day 1: 20 mg/kg, then 10 mg/kg)",
                "dosage_ja": "10-20 mg/kg 経口 24時間毎（初日20mg/kg、以後10mg/kg）",
                "notes": "Dual mechanism may reduce GI side effects vs traditional NSAIDs",
                "notes_ja": "デュアル機序により従来NSAIDsより消化器副作用が少ない可能性",
            },
            "cat": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Not approved for cats",
                "notes_ja": "猫には未承認",
            },
            "horse": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Not studied in horses",
                "notes_ja": "馬では未研究",
            },
            "rabbit": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Safety not established",
                "notes_ja": "安全性未確立",
            },
            "ferret": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Not approved",
                "notes_ja": "未承認",
            },
            "bird": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Not safe for avian species",
                "notes_ja": "鳥類には安全でない",
            },
        },
        "side_effects": ["GI ulceration", "vomiting", "diarrhea", "hepatotoxicity", "renal effects"],
        "side_effects_ja": ["消化管潰瘍", "嘔吐", "下痢", "肝毒性", "腎障害"],
        "contraindications": "GI ulceration. Renal/hepatic disease. Other NSAIDs or corticosteroids.",
        "contraindications_ja": "消化管潰瘍。腎/肝疾患。他のNSAIDsまたはコルチコステロイドとの併用。",
        "drug_interactions": [
            {"drug": "other NSAIDs", "effect": "Increased GI toxicity", "effect_ja": "消化管毒性増加"},
            {"drug": "corticosteroids", "effect": "Increased GI ulceration risk", "effect_ja": "消化管潰瘍リスク増加"},
        ],
    },
    {
        "id": "deracoxib",
        "name": "Deracoxib",
        "name_ja": "デラコキシブ",
        "category": "nsaids",
        "mechanism": "COX-2 selective NSAID; preferentially inhibits cyclooxygenase-2.",
        "mechanism_ja": "COX-2選択的NSAID。シクロオキシゲナーゼ-2を選択的に阻害。",
        "routes": ["PO"],
        "routes_ja": ["経口"],
        "formulations": ["Chewable tablets (Deramaxx)"],
        "formulations_ja": ["チュアブル錠（デラマックス）"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "1-2 mg/kg PO q24h (postop: 3-4 mg/kg/day x 7 days)",
                "dosage_ja": "1-2 mg/kg 経口 24時間毎（術後: 3-4 mg/kg/日 x 7日間）",
                "notes": "COX-2 selective; FDA-approved for dogs",
                "notes_ja": "COX-2選択的。犬にFDA承認",
            },
            "cat": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Not approved; cats very sensitive to NSAIDs",
                "notes_ja": "未承認。猫はNSAIDsに非常に敏感",
            },
            "horse": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Not approved for equines",
                "notes_ja": "馬には未承認",
            },
            "rabbit": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Not studied",
                "notes_ja": "未研究",
            },
            "ferret": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Safety not established",
                "notes_ja": "安全性未確立",
            },
            "bird": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Not approved",
                "notes_ja": "未承認",
            },
        },
        "side_effects": ["GI upset", "vomiting", "decreased appetite", "diarrhea", "elevated liver enzymes"],
        "side_effects_ja": ["消化器症状", "嘔吐", "食欲低下", "下痢", "肝酵素上昇"],
        "contraindications": "GI ulceration. Other NSAIDs. Corticosteroids. Renal/hepatic impairment.",
        "contraindications_ja": "消化管潰瘍。他のNSAIDs。コルチコステロイド。腎/肝障害。",
        "drug_interactions": [
            {"drug": "other NSAIDs", "effect": "Increased GI toxicity", "effect_ja": "消化管毒性増加"}
        ],
    },
    {
        "id": "grapiprant",
        "name": "Grapiprant",
        "name_ja": "グラピプラント",
        "category": "nsaids",
        "mechanism": "EP4 prostaglandin receptor antagonist (piprant class); blocks pain/inflammation without inhibiting COX.",
        "mechanism_ja": "EP4プロスタグランジン受容体拮抗薬（ピプラント系）。COX阻害なしに疼痛・炎症を遮断。",
        "routes": ["PO"],
        "routes_ja": ["経口"],
        "formulations": ["Tablets (Galliprant)"],
        "formulations_ja": ["錠剤（ガリプラント）"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "2 mg/kg PO q24h",
                "dosage_ja": "2 mg/kg 経口 24時間毎",
                "notes": "Novel mechanism; may be safer GI profile than traditional NSAIDs; for OA pain",
                "notes_ja": "新規機序。従来NSAIDsより消化管安全性が高い可能性。変形性関節症の疼痛に",
            },
            "cat": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Not approved for cats yet",
                "notes_ja": "猫には未承認",
            },
            "horse": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Not approved for horses",
                "notes_ja": "馬には未承認",
            },
            "rabbit": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Not studied",
                "notes_ja": "未研究",
            },
            "ferret": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Not approved",
                "notes_ja": "未承認",
            },
            "bird": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Not studied",
                "notes_ja": "未研究",
            },
        },
        "side_effects": ["vomiting", "diarrhea", "decreased appetite", "soft stool"],
        "side_effects_ja": ["嘔吐", "下痢", "食欲低下", "軟便"],
        "contraindications": "Dogs <3.6 kg or <9 months. Other NSAIDs or corticosteroids.",
        "contraindications_ja": "3.6kg未満または9ヶ月齢未満の犬。他のNSAIDsまたはコルチコステロイド。",
        "drug_interactions": [{"drug": "other NSAIDs", "effect": "Do not combine", "effect_ja": "併用不可"}],
    },
    {
        "id": "ketoprofen",
        "name": "Ketoprofen",
        "name_ja": "ケトプロフェン",
        "category": "nsaids",
        "mechanism": "Non-selective COX inhibitor with additional anti-bradykinin effects.",
        "mechanism_ja": "非選択的COX阻害薬。追加の抗ブラジキニン作用あり。",
        "routes": ["PO", "IV", "IM", "SC"],
        "routes_ja": ["経口", "静脈内", "筋肉内", "皮下"],
        "formulations": ["Tablets", "Injectable solution"],
        "formulations_ja": ["錠剤", "注射液"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "1-2 mg/kg PO/SC q24h (max 5 days)",
                "dosage_ja": "1-2 mg/kg 経口/皮下 24時間毎（最大5日間）",
                "notes": "Short-term use only",
                "notes_ja": "短期使用のみ",
            },
            "cat": {
                "safe": True,
                "dosage": "1-2 mg/kg SC once, then 1 mg/kg PO q24h (max 3 days)",
                "dosage_ja": "1-2 mg/kg 皮下 1回、その後1 mg/kg 経口 24時間毎（最大3日間）",
                "notes": "Very short-term only; feline-appropriate formulation needed",
                "notes_ja": "非常に短期のみ。猫用製剤が必要",
            },
            "horse": {
                "safe": True,
                "dosage": "2.2 mg/kg IV q24h",
                "dosage_ja": "2.2 mg/kg 静注 24時間毎",
                "notes": "Approved in many countries for horses",
                "notes_ja": "多くの国で馬に承認済",
            },
            "rabbit": {
                "safe": True,
                "dosage": "1-3 mg/kg SC/IM q12-24h",
                "dosage_ja": "1-3 mg/kg 皮下/筋注 12-24時間毎",
                "notes": "Used perioperatively in rabbits",
                "notes_ja": "ウサギの周術期に使用",
            },
            "bird": {
                "safe": True,
                "dosage": "2-5 mg/kg IM q8-24h",
                "dosage_ja": "2-5 mg/kg 筋注 8-24時間毎",
                "notes": "One of the better studied NSAIDs in birds",
                "notes_ja": "鳥類で比較的よく研究されたNSAIDs",
            },
            "reptile": {
                "safe": True,
                "dosage": "2 mg/kg IM q24h",
                "dosage_ja": "2 mg/kg 筋注 24時間毎",
                "notes": "Limited data in reptiles",
                "notes_ja": "爬虫類でのデータは限定的",
            },
        },
        "side_effects": ["GI ulceration", "vomiting", "renal effects", "bleeding"],
        "side_effects_ja": ["消化管潰瘍", "嘔吐", "腎障害", "出血"],
        "contraindications": "GI ulceration. Renal disease. Coagulopathy. Other NSAIDs.",
        "contraindications_ja": "消化管潰瘍。腎疾患。凝固異常。他のNSAIDs。",
        "drug_interactions": [
            {"drug": "other NSAIDs", "effect": "Increased GI risk", "effect_ja": "消化管リスク増加"},
            {"drug": "anticoagulants", "effect": "Increased bleeding risk", "effect_ja": "出血リスク増加"},
        ],
    },
    {
        "id": "piroxicam",
        "name": "Piroxicam",
        "name_ja": "ピロキシカム",
        "category": "nsaids",
        "mechanism": "Non-selective COX inhibitor. Has antitumor properties via COX-2 inhibition and other mechanisms.",
        "mechanism_ja": "非選択的COX阻害薬。COX-2阻害およびその他の機序により抗腫瘍作用を持つ。",
        "routes": ["PO"],
        "routes_ja": ["経口"],
        "formulations": ["Capsules"],
        "formulations_ja": ["カプセル"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "0.3 mg/kg PO q48h",
                "dosage_ja": "0.3 mg/kg 経口 48時間毎",
                "notes": "Used for transitional cell carcinoma; strong GI side effect profile",
                "notes_ja": "移行上皮癌に使用。消化管副作用が強い",
            },
            "cat": {
                "safe": True,
                "dosage": "0.3 mg/kg PO q48-72h",
                "dosage_ja": "0.3 mg/kg 経口 48-72時間毎",
                "notes": "Used for squamous cell carcinoma; careful monitoring required",
                "notes_ja": "扁平上皮癌に使用。慎重なモニタリングが必要",
            },
            "horse": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Not recommended; high GI toxicity risk in horses",
                "notes_ja": "推奨されない。馬で高い消化管毒性リスク",
            },
            "rabbit": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Not studied",
                "notes_ja": "未研究",
            },
            "ferret": {
                "safe": True,
                "dosage": "0.3 mg/kg PO q48h",
                "dosage_ja": "0.3 mg/kg 経口 48時間毎",
                "notes": "Used for adrenal disease-related prostatomegaly",
                "notes_ja": "副腎疾患関連の前立腺肥大に使用",
            },
            "bird": {
                "safe": True,
                "dosage": "0.5 mg/kg PO q12h",
                "dosage_ja": "0.5 mg/kg 経口 12時間毎",
                "notes": "Used for neoplasia in birds",
                "notes_ja": "鳥類の腫瘍性疾患に使用",
            },
        },
        "side_effects": ["GI ulceration/perforation", "renal papillary necrosis", "anorexia", "melena"],
        "side_effects_ja": ["消化管潰瘍/穿孔", "腎乳頭壊死", "食欲不振", "黒色便"],
        "contraindications": "GI ulceration. Renal/hepatic disease. Other NSAIDs. Corticosteroids.",
        "contraindications_ja": "消化管潰瘍。腎/肝疾患。他のNSAIDs。コルチコステロイド。",
        "drug_interactions": [
            {"drug": "other NSAIDs", "effect": "Severely increased GI toxicity", "effect_ja": "消化管毒性の著しい増加"},
            {"drug": "corticosteroids", "effect": "Increased ulceration risk", "effect_ja": "潰瘍リスク増加"},
        ],
    },
    {
        "id": "fentanyl",
        "name": "Fentanyl",
        "name_ja": "フェンタニル",
        "category": "analgesics",
        "mechanism": "Synthetic mu-opioid receptor agonist; 80-100x more potent than morphine.",
        "mechanism_ja": "合成μオピオイド受容体作動薬。モルヒネの80-100倍の効力。",
        "routes": ["IV", "IM", "transdermal", "CRI"],
        "routes_ja": ["静脈内", "筋肉内", "経皮", "持続点滴"],
        "formulations": ["Injectable solution", "Transdermal patch"],
        "formulations_ja": ["注射液", "経皮パッチ"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "2-5 mcg/kg IV bolus; 2-5 mcg/kg/hr CRI; patch: 2-5 mcg/kg/hr",
                "dosage_ja": "2-5 mcg/kg 静注ボーラス; 2-5 mcg/kg/hr 持続点滴; パッチ: 2-5 mcg/kg/hr",
                "notes": "Excellent perioperative analgesic; respiratory depression at high doses",
                "notes_ja": "優れた周術期鎮痛薬。高用量で呼吸抑制",
            },
            "cat": {
                "safe": True,
                "dosage": "1-3 mcg/kg IV; 1-4 mcg/kg/hr CRI; 25mcg/hr patch",
                "dosage_ja": "1-3 mcg/kg 静注; 1-4 mcg/kg/hr 持続点滴; 25mcg/hrパッチ",
                "notes": "Cats more sensitive; lower doses",
                "notes_ja": "猫はより敏感。低用量で",
            },
            "horse": {
                "safe": True,
                "dosage": "1-5 mcg/kg IV; 3-5 mcg/kg/hr CRI",
                "dosage_ja": "1-5 mcg/kg 静注; 3-5 mcg/kg/hr 持続点滴",
                "notes": "Can cause excitement if given alone; combine with alpha-2 agonist",
                "notes_ja": "単独投与で興奮の可能性。α2作動薬と併用",
            },
            "rabbit": {
                "safe": True,
                "dosage": "Transdermal patch: 12-25 mcg/hr",
                "dosage_ja": "経皮パッチ: 12-25 mcg/hr",
                "notes": "Patches useful; absorption variable due to fur",
                "notes_ja": "パッチが有用。被毛による吸収変動あり",
            },
            "ferret": {
                "safe": True,
                "dosage": "5 mcg/kg IM/IV; patch: variable",
                "dosage_ja": "5 mcg/kg 筋注/静注; パッチ: 変動",
                "notes": "Effective analgesic in ferrets",
                "notes_ja": "フェレットに有効な鎮痛薬",
            },
            "bird": {
                "safe": True,
                "dosage": "0.02-0.1 mg/kg IM",
                "dosage_ja": "0.02-0.1 mg/kg 筋注",
                "notes": "Variable efficacy in birds; species-dependent",
                "notes_ja": "鳥類での有効性は変動。種依存性",
            },
        },
        "side_effects": ["respiratory depression", "bradycardia", "hypothermia", "ileus", "dysphoria"],
        "side_effects_ja": ["呼吸抑制", "徐脈", "低体温", "イレウス", "不快感"],
        "contraindications": "Severe respiratory disease. Head trauma with increased ICP. MAO inhibitor use.",
        "contraindications_ja": "重度呼吸器疾患。頭蓋内圧亢進を伴う頭部外傷。MAO阻害薬使用中。",
        "drug_interactions": [
            {
                "drug": "MAO inhibitors",
                "effect": "Fatal serotonin syndrome possible",
                "effect_ja": "致死的セロトニン症候群の可能性",
            },
            {"drug": "benzodiazepines", "effect": "Enhanced respiratory depression", "effect_ja": "呼吸抑制の増強"},
        ],
    },
    {
        "id": "morphine",
        "name": "Morphine",
        "name_ja": "モルヒネ",
        "category": "analgesics",
        "mechanism": "Natural mu-opioid receptor agonist; prototype opioid analgesic.",
        "mechanism_ja": "天然μオピオイド受容体作動薬。オピオイド鎮痛薬の原型。",
        "routes": ["IV", "IM", "SC", "epidural"],
        "routes_ja": ["静脈内", "筋肉内", "皮下", "硬膜外"],
        "formulations": ["Injectable solution"],
        "formulations_ja": ["注射液"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "0.5-1 mg/kg IM/SC q4-6h; 0.1-0.3 mg/kg/hr CRI",
                "dosage_ja": "0.5-1 mg/kg 筋注/皮下 4-6時間毎; 0.1-0.3 mg/kg/hr 持続点滴",
                "notes": "Gold standard opioid; causes histamine release with rapid IV",
                "notes_ja": "ゴールドスタンダードのオピオイド。急速静注でヒスタミン遊離",
            },
            "cat": {
                "safe": True,
                "dosage": "0.1-0.3 mg/kg IM/SC q4-6h",
                "dosage_ja": "0.1-0.3 mg/kg 筋注/皮下 4-6時間毎",
                "notes": "Lower doses than dogs; can cause excitement/dysphoria",
                "notes_ja": "犬より低用量。興奮/不快感を起こす可能性",
            },
            "horse": {
                "safe": True,
                "dosage": "0.05-0.1 mg/kg IV; epidural: 0.1-0.2 mg/kg",
                "dosage_ja": "0.05-0.1 mg/kg 静注; 硬膜外: 0.1-0.2 mg/kg",
                "notes": "IV can cause excitement; epidural provides excellent analgesia",
                "notes_ja": "静注で興奮の可能性。硬膜外で優れた鎮痛効果",
            },
            "rabbit": {
                "safe": True,
                "dosage": "1-5 mg/kg SC/IM q2-4h",
                "dosage_ja": "1-5 mg/kg 皮下/筋注 2-4時間毎",
                "notes": "Rabbits require higher doses; effective for post-surgical pain",
                "notes_ja": "ウサギはより高用量が必要。術後疼痛に有効",
            },
            "ferret": {
                "safe": True,
                "dosage": "0.5-5 mg/kg SC/IM q2-6h",
                "dosage_ja": "0.5-5 mg/kg 皮下/筋注 2-6時間毎",
                "notes": "Effective analgesic",
                "notes_ja": "有効な鎮痛薬",
            },
            "bird": {
                "safe": True,
                "dosage": "1-5 mg/kg IM q4h",
                "dosage_ja": "1-5 mg/kg 筋注 4時間毎",
                "notes": "Variable efficacy; parrots may need higher doses",
                "notes_ja": "有効性は変動。オウムはより高用量が必要な場合",
            },
        },
        "side_effects": [
            "respiratory depression",
            "sedation",
            "histamine release (IV)",
            "nausea/vomiting",
            "ileus",
            "miosis",
        ],
        "side_effects_ja": ["呼吸抑制", "鎮静", "ヒスタミン遊離(静注)", "悪心/嘔吐", "イレウス", "縮瞳"],
        "contraindications": "Severe respiratory depression. Head injury with raised ICP. Give IV slowly.",
        "contraindications_ja": "重度の呼吸抑制。頭蓋内圧上昇を伴う頭部外傷。静注はゆっくり行う。",
        "drug_interactions": [
            {
                "drug": "phenothiazines",
                "effect": "Enhanced CNS/respiratory depression",
                "effect_ja": "CNS/呼吸抑制の増強",
            }
        ],
    },
    {
        "id": "hydromorphone",
        "name": "Hydromorphone",
        "name_ja": "ヒドロモルフォン",
        "category": "analgesics",
        "mechanism": "Semi-synthetic mu-opioid agonist; 5-7x more potent than morphine. No histamine release.",
        "mechanism_ja": "半合成μオピオイド作動薬。モルヒネの5-7倍の効力。ヒスタミン遊離なし。",
        "routes": ["IV", "IM", "SC"],
        "routes_ja": ["静脈内", "筋肉内", "皮下"],
        "formulations": ["Injectable solution"],
        "formulations_ja": ["注射液"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "0.05-0.2 mg/kg IV/IM/SC q4-6h",
                "dosage_ja": "0.05-0.2 mg/kg 静注/筋注/皮下 4-6時間毎",
                "notes": "Preferred over morphine - no histamine release",
                "notes_ja": "モルヒネより好まれる - ヒスタミン遊離なし",
            },
            "cat": {
                "safe": True,
                "dosage": "0.025-0.1 mg/kg IV/IM/SC q4-6h",
                "dosage_ja": "0.025-0.1 mg/kg 静注/筋注/皮下 4-6時間毎",
                "notes": "Can cause hyperthermia in cats; monitor temperature",
                "notes_ja": "猫で高体温を起こす可能性。体温モニタリング",
            },
            "horse": {
                "safe": True,
                "dosage": "0.04-0.08 mg/kg IV",
                "dosage_ja": "0.04-0.08 mg/kg 静注",
                "notes": "Less excitation than morphine",
                "notes_ja": "モルヒネより興奮が少ない",
            },
            "rabbit": {
                "safe": True,
                "dosage": "0.1-0.2 mg/kg SC/IM q6-8h",
                "dosage_ja": "0.1-0.2 mg/kg 皮下/筋注 6-8時間毎",
                "notes": "Good analgesic for rabbits",
                "notes_ja": "ウサギに良好な鎮痛薬",
            },
            "ferret": {
                "safe": True,
                "dosage": "0.1 mg/kg IV/IM/SC q6-8h",
                "dosage_ja": "0.1 mg/kg 静注/筋注/皮下 6-8時間毎",
                "notes": "Effective perioperative use",
                "notes_ja": "効果的な周術期使用",
            },
            "bird": {
                "safe": True,
                "dosage": "0.1-0.6 mg/kg IM q4-6h",
                "dosage_ja": "0.1-0.6 mg/kg 筋注 4-6時間毎",
                "notes": "Limited studies in birds",
                "notes_ja": "鳥類での研究は限定的",
            },
        },
        "side_effects": ["respiratory depression", "bradycardia", "sedation", "hyperthermia (cats)", "panting (dogs)"],
        "side_effects_ja": ["呼吸抑制", "徐脈", "鎮静", "高体温(猫)", "パンティング(犬)"],
        "contraindications": "Severe respiratory compromise. Significant head trauma.",
        "contraindications_ja": "重度呼吸不全。重度頭部外傷。",
        "drug_interactions": [
            {
                "drug": "phenothiazines",
                "effect": "Enhanced sedation/respiratory depression",
                "effect_ja": "鎮静/呼吸抑制の増強",
            }
        ],
    },
    {
        "id": "methadone",
        "name": "Methadone",
        "name_ja": "メサドン",
        "category": "analgesics",
        "mechanism": "Mu-opioid agonist and NMDA receptor antagonist; provides both opioid and neuropathic pain relief.",
        "mechanism_ja": "μオピオイド作動薬およびNMDA受容体拮抗薬。オピオイド性および神経障害性疼痛の両方を緩和。",
        "routes": ["IV", "IM", "SC"],
        "routes_ja": ["静脈内", "筋肉内", "皮下"],
        "formulations": ["Injectable solution"],
        "formulations_ja": ["注射液"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "0.1-0.5 mg/kg IV/IM q4-6h",
                "dosage_ja": "0.1-0.5 mg/kg 静注/筋注 4-6時間毎",
                "notes": "Dual mechanism; no histamine release; gaining popularity as perioperative opioid",
                "notes_ja": "デュアル機序。ヒスタミン遊離なし。周術期オピオイドとして人気上昇中",
            },
            "cat": {
                "safe": True,
                "dosage": "0.1-0.5 mg/kg IV/IM q4-6h",
                "dosage_ja": "0.1-0.5 mg/kg 静注/筋注 4-6時間毎",
                "notes": "Well tolerated in cats; good perioperative analgesic",
                "notes_ja": "猫で忍容性良好。良好な周術期鎮痛薬",
            },
            "horse": {
                "safe": True,
                "dosage": "0.1-0.2 mg/kg IV q4-6h",
                "dosage_ja": "0.1-0.2 mg/kg 静注 4-6時間毎",
                "notes": "Less excitation than morphine",
                "notes_ja": "モルヒネより興奮が少ない",
            },
            "rabbit": {
                "safe": True,
                "dosage": "0.3-0.5 mg/kg SC/IM q4-6h",
                "dosage_ja": "0.3-0.5 mg/kg 皮下/筋注 4-6時間毎",
                "notes": "Effective in rabbits",
                "notes_ja": "ウサギに有効",
            },
            "ferret": {
                "safe": True,
                "dosage": "0.1-0.25 mg/kg IM q4-6h",
                "dosage_ja": "0.1-0.25 mg/kg 筋注 4-6時間毎",
                "notes": "Good analgesic option",
                "notes_ja": "良好な鎮痛選択肢",
            },
            "bird": {
                "safe": True,
                "dosage": "1-6 mg/kg IM q4-8h",
                "dosage_ja": "1-6 mg/kg 筋注 4-8時間毎",
                "notes": "Some evidence of efficacy in raptors",
                "notes_ja": "猛禽類での有効性のエビデンスあり",
            },
        },
        "side_effects": ["respiratory depression", "sedation", "bradycardia", "dysphoria"],
        "side_effects_ja": ["呼吸抑制", "鎮静", "徐脈", "不快感"],
        "contraindications": "Severe respiratory disease. MAO inhibitors.",
        "contraindications_ja": "重度呼吸器疾患。MAO阻害薬。",
        "drug_interactions": [
            {
                "drug": "MAO inhibitors",
                "effect": "Potentially fatal interaction",
                "effect_ja": "致死的な相互作用の可能性",
            }
        ],
    },
    {
        "id": "lidocaine",
        "name": "Lidocaine",
        "name_ja": "リドカイン",
        "category": "anesthetics",
        "mechanism": "Amide local anesthetic; blocks sodium channels. Also class IB antiarrhythmic and CRI analgesic.",
        "mechanism_ja": "アミド型局所麻酔薬。ナトリウムチャネルを遮断。クラスIB抗不整脈薬・CRI鎮痛薬としても使用。",
        "routes": ["local", "IV", "topical", "epidural"],
        "routes_ja": ["局所", "静脈内", "外用", "硬膜外"],
        "formulations": ["Injectable 2%", "Topical spray/gel", "CRI solution"],
        "formulations_ja": ["注射液2%", "外用スプレー/ジェル", "CRI用液"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Local: 2-4 mg/kg; CRI: 25-80 mcg/kg/min; antiarrhythmic: 2 mg/kg IV bolus",
                "dosage_ja": "局所: 2-4 mg/kg; CRI: 25-80 mcg/kg/min; 抗不整脈: 2 mg/kg 静注ボーラス",
                "notes": "Multimodal use: local block, CRI analgesia, antiarrhythmic",
                "notes_ja": "多目的使用: 局所麻酔、CRI鎮痛、抗不整脈",
            },
            "cat": {
                "safe": True,
                "dosage": "Local: 1-2 mg/kg (max 4 mg/kg total); CRI: 10-25 mcg/kg/min",
                "dosage_ja": "局所: 1-2 mg/kg (最大4 mg/kg); CRI: 10-25 mcg/kg/min",
                "notes": "CAUTION: cats very sensitive - lower doses; CNS toxicity at lower thresholds",
                "notes_ja": "【注意】猫は非常に敏感 - 低用量で。より低い閾値でCNS毒性",
            },
            "horse": {
                "safe": True,
                "dosage": "Local: up to 4 mg/kg; CRI: 50 mcg/kg/min; IV bolus: 1.3 mg/kg",
                "dosage_ja": "局所: 最大4 mg/kg; CRI: 50 mcg/kg/min; 静注: 1.3 mg/kg",
                "notes": "Widely used for nerve blocks and CRI analgesia",
                "notes_ja": "神経ブロックとCRI鎮痛に広く使用",
            },
            "rabbit": {
                "safe": True,
                "dosage": "Local: 1-2 mg/kg",
                "dosage_ja": "局所: 1-2 mg/kg",
                "notes": "For local/regional blocks",
                "notes_ja": "局所/区域ブロックに",
            },
            "ferret": {
                "safe": True,
                "dosage": "Local: 1-2 mg/kg",
                "dosage_ja": "局所: 1-2 mg/kg",
                "notes": "Use with caution; small body size",
                "notes_ja": "注意して使用。小さな体格",
            },
            "bird": {
                "safe": True,
                "dosage": "Local: 1-4 mg/kg (max 4 mg/kg)",
                "dosage_ja": "局所: 1-4 mg/kg (最大4 mg/kg)",
                "notes": "For regional blocks; do not exceed max dose",
                "notes_ja": "区域ブロックに。最大用量を超えないこと",
            },
        },
        "side_effects": [
            "CNS toxicity (tremors, seizures)",
            "cardiovascular depression",
            "methemoglobinemia (excessive doses)",
        ],
        "side_effects_ja": ["CNS毒性(振戦、痙攣)", "心血管抑制", "メトヘモグロビン血症(過量投与)"],
        "contraindications": "Heart block. Severe hepatic disease (metabolized by liver). Cats: strict dose limits.",
        "contraindications_ja": "心ブロック。重度肝疾患（肝臓で代謝）。猫: 厳密な用量制限。",
        "drug_interactions": [
            {"drug": "beta-blockers", "effect": "Enhanced cardiac depression", "effect_ja": "心抑制の増強"},
            {"drug": "cimetidine", "effect": "Decreased lidocaine metabolism", "effect_ja": "リドカイン代謝の低下"},
        ],
    },
    {
        "id": "isoflurane",
        "name": "Isoflurane",
        "name_ja": "イソフルラン",
        "category": "anesthetics",
        "mechanism": "Volatile halogenated ether anesthetic; produces dose-dependent CNS depression via GABA enhancement.",
        "mechanism_ja": "揮発性ハロゲン化エーテル麻酔薬。GABA増強による用量依存性CNS抑制を生じる。",
        "routes": ["inhalation"],
        "routes_ja": ["吸入"],
        "formulations": ["Volatile liquid for vaporizer"],
        "formulations_ja": ["気化器用揮発性液体"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "MAC 1.28%; maintenance 1-2%",
                "dosage_ja": "MAC 1.28%; 維持 1-2%",
                "notes": "Most commonly used inhalant anesthetic",
                "notes_ja": "最も一般的に使用される吸入麻酔薬",
            },
            "cat": {
                "safe": True,
                "dosage": "MAC 1.63%; maintenance 1.5-3%",
                "dosage_ja": "MAC 1.63%; 維持 1.5-3%",
                "notes": "Cats have higher MAC than dogs",
                "notes_ja": "猫は犬よりMACが高い",
            },
            "horse": {
                "safe": True,
                "dosage": "MAC 1.31%; maintenance 1-1.5%",
                "dosage_ja": "MAC 1.31%; 維持 1-1.5%",
                "notes": "Standard equine inhalant; hypotension at higher concentrations",
                "notes_ja": "標準的な馬の吸入麻酔薬。高濃度で低血圧",
            },
            "rabbit": {
                "safe": True,
                "dosage": "MAC ~2%; maintenance 1.5-3%",
                "dosage_ja": "MAC約2%; 維持 1.5-3%",
                "notes": "Higher MAC; breath-holding common on induction",
                "notes_ja": "MACが高い。導入時の息止めが一般的",
            },
            "bird": {
                "safe": True,
                "dosage": "Induction 3-5%; maintenance 1.5-3%",
                "dosage_ja": "導入 3-5%; 維持 1.5-3%",
                "notes": "Rapid induction/recovery in birds; preferred inhalant",
                "notes_ja": "鳥類で迅速な導入/覚醒。好ましい吸入麻酔薬",
            },
            "reptile": {
                "safe": True,
                "dosage": "Induction 3-5%; maintenance 1-3%",
                "dosage_ja": "導入 3-5%; 維持 1-3%",
                "notes": "Slow induction due to breath-holding; may need intubation",
                "notes_ja": "息止めにより導入が遅い。挿管が必要な場合あり",
            },
        },
        "side_effects": [
            "dose-dependent hypotension",
            "respiratory depression",
            "hypothermia",
            "malignant hyperthermia (rare, pigs)",
        ],
        "side_effects_ja": ["用量依存性低血圧", "呼吸抑制", "低体温", "悪性高熱(まれ、ブタ)"],
        "contraindications": "Known malignant hyperthermia susceptibility. Severe hypovolemia without fluid support.",
        "contraindications_ja": "悪性高熱素因が既知の場合。輸液サポートなしの重度循環血液量減少。",
        "drug_interactions": [
            {"drug": "aminoglycosides", "effect": "Enhanced neuromuscular blockade", "effect_ja": "神経筋遮断の増強"}
        ],
    },
    {
        "id": "sevoflurane",
        "name": "Sevoflurane",
        "name_ja": "セボフルラン",
        "category": "anesthetics",
        "mechanism": "Volatile halogenated ether; lower blood-gas solubility than isoflurane, allowing faster induction/recovery.",
        "mechanism_ja": "揮発性ハロゲン化エーテル。イソフルランより血液/ガス分配係数が低く、迅速な導入/覚醒が可能。",
        "routes": ["inhalation"],
        "routes_ja": ["吸入"],
        "formulations": ["Volatile liquid for vaporizer"],
        "formulations_ja": ["気化器用揮発性液体"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "MAC 2.36%; induction 5-7%; maintenance 2-3%",
                "dosage_ja": "MAC 2.36%; 導入 5-7%; 維持 2-3%",
                "notes": "Smoother/faster induction than isoflurane",
                "notes_ja": "イソフルランよりスムーズで速い導入",
            },
            "cat": {
                "safe": True,
                "dosage": "MAC 2.58%; induction 5-7%; maintenance 2.5-4%",
                "dosage_ja": "MAC 2.58%; 導入 5-7%; 維持 2.5-4%",
                "notes": "Well accepted for mask induction in cats",
                "notes_ja": "猫のマスク導入によく受け入れられる",
            },
            "horse": {
                "safe": True,
                "dosage": "MAC 2.31%; maintenance 2.5-3.5%",
                "dosage_ja": "MAC 2.31%; 維持 2.5-3.5%",
                "notes": "More expensive than isoflurane; slightly less hypotension",
                "notes_ja": "イソフルランより高価。低血圧がやや少ない",
            },
            "rabbit": {
                "safe": True,
                "dosage": "Induction 5-8%; maintenance 2-4%",
                "dosage_ja": "導入 5-8%; 維持 2-4%",
                "notes": "Excellent for rabbit anesthesia; rapid recovery",
                "notes_ja": "ウサギ麻酔に優秀。迅速な覚醒",
            },
            "bird": {
                "safe": True,
                "dosage": "Induction 4-6%; maintenance 2-4%",
                "dosage_ja": "導入 4-6%; 維持 2-4%",
                "notes": "Rapid induction preferred for stressed birds",
                "notes_ja": "ストレス下の鳥類に迅速導入が好まれる",
            },
            "reptile": {
                "safe": True,
                "dosage": "Induction 5-8%; maintenance 2-4%",
                "dosage_ja": "導入 5-8%; 維持 2-4%",
                "notes": "Faster induction than isoflurane in reptiles",
                "notes_ja": "爬虫類でイソフルランより速い導入",
            },
        },
        "side_effects": [
            "dose-dependent hypotension",
            "respiratory depression",
            "hypothermia",
            "Compound A production (with CO2 absorbers)",
        ],
        "side_effects_ja": ["用量依存性低血圧", "呼吸抑制", "低体温", "化合物A産生(CO2吸収剤使用時)"],
        "contraindications": "Same as isoflurane. More expensive.",
        "contraindications_ja": "イソフルランと同様。より高価。",
        "drug_interactions": [],
    },
    {
        "id": "medetomidine",
        "name": "Medetomidine",
        "name_ja": "メデトミジン",
        "category": "sedatives",
        "mechanism": "Alpha-2 adrenergic agonist; produces dose-dependent sedation, muscle relaxation, and analgesia.",
        "mechanism_ja": "α2アドレナリン作動薬。用量依存性の鎮静、筋弛緩、鎮痛を生じる。",
        "routes": ["IV", "IM", "SC"],
        "routes_ja": ["静脈内", "筋肉内", "皮下"],
        "formulations": ["Injectable solution (Domitor)"],
        "formulations_ja": ["注射液（ドミトール）"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "5-40 mcg/kg IV/IM",
                "dosage_ja": "5-40 mcg/kg 静注/筋注",
                "notes": "Profound sedation; causes bradycardia and initial hypertension then hypotension",
                "notes_ja": "深い鎮静。徐脈、初期高血圧→低血圧を引き起こす",
            },
            "cat": {
                "safe": True,
                "dosage": "40-80 mcg/kg IM",
                "dosage_ja": "40-80 mcg/kg 筋注",
                "notes": "Excellent sedation in cats; reliable emesis",
                "notes_ja": "猫で優れた鎮静。確実な催吐作用",
            },
            "horse": {
                "safe": True,
                "dosage": "5-10 mcg/kg IV",
                "dosage_ja": "5-10 mcg/kg 静注",
                "notes": "Standing sedation; combine with opioid for procedures",
                "notes_ja": "立位鎮静。処置にはオピオイドと併用",
            },
            "rabbit": {
                "safe": True,
                "dosage": "200-500 mcg/kg IM/SC",
                "dosage_ja": "200-500 mcg/kg 筋注/皮下",
                "notes": "High doses needed; combine with ketamine for anesthesia",
                "notes_ja": "高用量が必要。麻酔にはケタミンと併用",
            },
            "ferret": {
                "safe": True,
                "dosage": "80-100 mcg/kg IM",
                "dosage_ja": "80-100 mcg/kg 筋注",
                "notes": "Good sedation; always reverse with atipamezole",
                "notes_ja": "良好な鎮静。必ずアチパメゾールで拮抗",
            },
            "bird": {
                "safe": True,
                "dosage": "50-100 mcg/kg IM",
                "dosage_ja": "50-100 mcg/kg 筋注",
                "notes": "Variable efficacy; use with ketamine",
                "notes_ja": "有効性は変動。ケタミンと併用",
            },
        },
        "side_effects": [
            "bradycardia",
            "hypertension then hypotension",
            "hypothermia",
            "vomiting",
            "decreased cardiac output",
        ],
        "side_effects_ja": ["徐脈", "高血圧→低血圧", "低体温", "嘔吐", "心拍出量低下"],
        "contraindications": "Cardiac disease. Hepatic/renal insufficiency. Shock. Geriatric/debilitated patients.",
        "contraindications_ja": "心疾患。肝/腎不全。ショック。高齢/衰弱患者。",
        "drug_interactions": [
            {"drug": "other sedatives", "effect": "Enhanced CNS depression", "effect_ja": "CNS抑制の増強"}
        ],
    },
    {
        "id": "dexmedetomidine",
        "name": "Dexmedetomidine",
        "name_ja": "デクスメデトミジン",
        "category": "sedatives",
        "mechanism": "Active enantiomer of medetomidine; alpha-2 agonist with 2x potency of racemic medetomidine.",
        "mechanism_ja": "メデトミジンの活性エナンチオマー。ラセミ体メデトミジンの2倍の効力を持つα2作動薬。",
        "routes": ["IV", "IM", "SC", "buccal"],
        "routes_ja": ["静脈内", "筋肉内", "皮下", "口腔粘膜"],
        "formulations": ["Injectable (Dexdomitor)", "Oromucosal gel (Sileo)"],
        "formulations_ja": ["注射液（デクスドミトール）", "口腔粘膜用ジェル（シレオ）"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "2-20 mcg/kg IV/IM; Sileo: 125 mcg/m2 buccal",
                "dosage_ja": "2-20 mcg/kg 静注/筋注; シレオ: 125 mcg/m2 口腔粘膜",
                "notes": "Sileo gel approved for noise aversion; half the dose of medetomidine",
                "notes_ja": "シレオジェルは騒音恐怖症に承認。メデトミジンの半量",
            },
            "cat": {
                "safe": True,
                "dosage": "20-40 mcg/kg IM",
                "dosage_ja": "20-40 mcg/kg 筋注",
                "notes": "Half the dose of medetomidine",
                "notes_ja": "メデトミジンの半量",
            },
            "horse": {
                "safe": True,
                "dosage": "3-5 mcg/kg IV",
                "dosage_ja": "3-5 mcg/kg 静注",
                "notes": "Excellent standing sedation",
                "notes_ja": "優れた立位鎮静",
            },
            "rabbit": {
                "safe": True,
                "dosage": "100-250 mcg/kg IM",
                "dosage_ja": "100-250 mcg/kg 筋注",
                "notes": "Half medetomidine dose",
                "notes_ja": "メデトミジンの半量",
            },
            "ferret": {
                "safe": True,
                "dosage": "40-50 mcg/kg IM",
                "dosage_ja": "40-50 mcg/kg 筋注",
                "notes": "Always reverse with atipamezole",
                "notes_ja": "必ずアチパメゾールで拮抗",
            },
            "bird": {
                "safe": True,
                "dosage": "25-75 mcg/kg IM",
                "dosage_ja": "25-75 mcg/kg 筋注",
                "notes": "Used in combination protocols",
                "notes_ja": "併用プロトコルで使用",
            },
        },
        "side_effects": [
            "bradycardia",
            "hypertension/hypotension",
            "vomiting",
            "hypothermia",
            "decreased cardiac output",
        ],
        "side_effects_ja": ["徐脈", "高血圧/低血圧", "嘔吐", "低体温", "心拍出量低下"],
        "contraindications": "Same as medetomidine. Cardiac disease. Debilitated patients.",
        "contraindications_ja": "メデトミジンと同様。心疾患。衰弱患者。",
        "drug_interactions": [{"drug": "other sedatives", "effect": "Enhanced sedation", "effect_ja": "鎮静の増強"}],
    },
    {
        "id": "acepromazine",
        "name": "Acepromazine",
        "name_ja": "アセプロマジン",
        "category": "sedatives",
        "mechanism": "Phenothiazine tranquilizer; blocks dopamine receptors. Produces sedation and anxiolysis without analgesia.",
        "mechanism_ja": "フェノチアジン系鎮静薬。ドパミン受容体を遮断。鎮痛作用なしに鎮静・抗不安作用を生じる。",
        "routes": ["IV", "IM", "SC", "PO"],
        "routes_ja": ["静脈内", "筋肉内", "皮下", "経口"],
        "formulations": ["Injectable solution", "Tablets"],
        "formulations_ja": ["注射液", "錠剤"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "0.01-0.1 mg/kg IV/IM; 0.5-2 mg/kg PO",
                "dosage_ja": "0.01-0.1 mg/kg 静注/筋注; 0.5-2 mg/kg 経口",
                "notes": "Low doses adequate; avoid in boxers/brachycephalic breeds (hypotension)",
                "notes_ja": "低用量で十分。ボクサー/短頭種では低血圧のため避ける",
            },
            "cat": {
                "safe": True,
                "dosage": "0.05-0.1 mg/kg IM; 0.5-1 mg/kg PO",
                "dosage_ja": "0.05-0.1 mg/kg 筋注; 0.5-1 mg/kg 経口",
                "notes": "Commonly used premed; lowers seizure threshold",
                "notes_ja": "一般的な前投薬。痙攣閾値を低下させる",
            },
            "horse": {
                "safe": True,
                "dosage": "0.03-0.1 mg/kg IV/IM",
                "dosage_ja": "0.03-0.1 mg/kg 静注/筋注",
                "notes": "Causes penile prolapse - avoid in breeding stallions",
                "notes_ja": "陰茎脱出を起こす - 種牡馬では避ける",
            },
            "rabbit": {
                "safe": True,
                "dosage": "0.25-1 mg/kg IM/SC",
                "dosage_ja": "0.25-1 mg/kg 筋注/皮下",
                "notes": "Can be used as premed; mild sedation only",
                "notes_ja": "前投薬として使用可能。軽度の鎮静のみ",
            },
            "ferret": {
                "safe": True,
                "dosage": "0.1-0.25 mg/kg IM",
                "dosage_ja": "0.1-0.25 mg/kg 筋注",
                "notes": "Light sedation",
                "notes_ja": "軽度の鎮静",
            },
            "bird": {
                "safe": True,
                "dosage": "0.5-1 mg/kg IM",
                "dosage_ja": "0.5-1 mg/kg 筋注",
                "notes": "Provides mild sedation; unreliable in some species",
                "notes_ja": "軽度の鎮静。一部の種では効果不安定",
            },
        },
        "side_effects": [
            "hypotension",
            "hypothermia",
            "penile prolapse (horses)",
            "lowered seizure threshold",
            "paradoxical excitement",
        ],
        "side_effects_ja": ["低血圧", "低体温", "陰茎脱出(馬)", "痙攣閾値低下", "逆説的興奮"],
        "contraindications": "Epilepsy. Hypovolemia/shock. Boxers (severe hypotension). Breeding stallions.",
        "contraindications_ja": "てんかん。循環血液量減少/ショック。ボクサー（重度低血圧）。種牡馬。",
        "drug_interactions": [
            {
                "drug": "opioids",
                "effect": "Synergistic sedation (desired in protocols)",
                "effect_ja": "相乗的鎮静（プロトコルで意図的）",
            }
        ],
    },
    {
        "id": "midazolam",
        "name": "Midazolam",
        "name_ja": "ミダゾラム",
        "category": "sedatives",
        "mechanism": "Short-acting benzodiazepine; enhances GABA-A receptor activity. Provides anxiolysis, muscle relaxation, and amnesia.",
        "mechanism_ja": "短時間作用型ベンゾジアゼピン。GABA-A受容体活性を増強。抗不安、筋弛緩、健忘を提供。",
        "routes": ["IV", "IM", "intranasal"],
        "routes_ja": ["静脈内", "筋肉内", "鼻腔内"],
        "formulations": ["Injectable solution"],
        "formulations_ja": ["注射液"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "0.1-0.5 mg/kg IV/IM",
                "dosage_ja": "0.1-0.5 mg/kg 静注/筋注",
                "notes": "May cause paradoxical excitement in healthy young dogs if given alone",
                "notes_ja": "健康な若犬に単独投与で逆説的興奮の可能性",
            },
            "cat": {
                "safe": True,
                "dosage": "0.1-0.5 mg/kg IV/IM",
                "dosage_ja": "0.1-0.5 mg/kg 静注/筋注",
                "notes": "Good co-induction agent; muscle relaxant",
                "notes_ja": "良好な共導入薬。筋弛緩薬",
            },
            "horse": {
                "safe": True,
                "dosage": "0.02-0.06 mg/kg IV",
                "dosage_ja": "0.02-0.06 mg/kg 静注",
                "notes": "Always combine with other agents; ataxia if used alone",
                "notes_ja": "必ず他薬と併用。単独で運動失調",
            },
            "rabbit": {
                "safe": True,
                "dosage": "0.5-2 mg/kg IV/IM/intranasal",
                "dosage_ja": "0.5-2 mg/kg 静注/筋注/鼻腔内",
                "notes": "Excellent co-induction; intranasal route useful",
                "notes_ja": "優れた共導入薬。鼻腔内投与が有用",
            },
            "ferret": {
                "safe": True,
                "dosage": "0.25-0.5 mg/kg IM",
                "dosage_ja": "0.25-0.5 mg/kg 筋注",
                "notes": "Good muscle relaxation",
                "notes_ja": "良好な筋弛緩",
            },
            "bird": {
                "safe": True,
                "dosage": "0.5-2 mg/kg IM/intranasal",
                "dosage_ja": "0.5-2 mg/kg 筋注/鼻腔内",
                "notes": "Intranasal administration effective in birds",
                "notes_ja": "鳥類で鼻腔内投与が有効",
            },
        },
        "side_effects": ["paradoxical excitement", "ataxia", "respiratory depression", "excessive sedation"],
        "side_effects_ja": ["逆説的興奮", "運動失調", "呼吸抑制", "過度の鎮静"],
        "contraindications": "Severe CNS depression. Acute narrow-angle glaucoma.",
        "contraindications_ja": "重度CNS抑制。急性狭隅角緑内障。",
        "drug_interactions": [
            {
                "drug": "opioids",
                "effect": "Enhanced sedation/respiratory depression",
                "effect_ja": "鎮静/呼吸抑制の増強",
            }
        ],
    },
    {
        "id": "atipamezole",
        "name": "Atipamezole",
        "name_ja": "アチパメゾール",
        "category": "sedatives",
        "mechanism": "Alpha-2 adrenergic antagonist; reverses effects of medetomidine/dexmedetomidine.",
        "mechanism_ja": "α2アドレナリン拮抗薬。メデトミジン/デクスメデトミジンの作用を拮抗する。",
        "routes": ["IM"],
        "routes_ja": ["筋肉内"],
        "formulations": ["Injectable (Antisedan)"],
        "formulations_ja": ["注射液（アンチセダン）"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Same volume as medetomidine given IM",
                "dosage_ja": "投与したメデトミジンと同容量を筋注",
                "notes": "Reversal within 5-10 minutes; monitor for re-sedation",
                "notes_ja": "5-10分以内に拮抗。再鎮静をモニタリング",
            },
            "cat": {
                "safe": True,
                "dosage": "Same volume as medetomidine given IM",
                "dosage_ja": "投与したメデトミジンと同容量を筋注",
                "notes": "Effective reversal; reverses vomiting",
                "notes_ja": "効果的な拮抗。嘔吐も消失",
            },
            "horse": {
                "safe": True,
                "dosage": "5x medetomidine dose IV slowly",
                "dosage_ja": "メデトミジン用量の5倍を静注（ゆっくり）",
                "notes": "Use with caution; may cause excitement",
                "notes_ja": "注意して使用。興奮を起こす可能性",
            },
            "rabbit": {
                "safe": True,
                "dosage": "Same volume as medetomidine IM",
                "dosage_ja": "メデトミジンと同容量を筋注",
                "notes": "Essential reversal in rabbit protocols",
                "notes_ja": "ウサギのプロトコルで必須の拮抗薬",
            },
            "ferret": {
                "safe": True,
                "dosage": "Same volume as medetomidine IM",
                "dosage_ja": "メデトミジンと同容量を筋注",
                "notes": "Always reverse alpha-2 in ferrets post-procedure",
                "notes_ja": "フェレットでは処置後必ずα2を拮抗",
            },
            "bird": {
                "safe": True,
                "dosage": "5x medetomidine dose IM",
                "dosage_ja": "メデトミジン用量の5倍を筋注",
                "notes": "Important reversal agent",
                "notes_ja": "重要な拮抗薬",
            },
        },
        "side_effects": ["transient tachycardia", "excitement", "muscle tremors", "hypotension"],
        "side_effects_ja": ["一過性頻脈", "興奮", "筋振戦", "低血圧"],
        "contraindications": "Caution in animals with cardiac disease (abrupt sympathetic activation).",
        "contraindications_ja": "心疾患のある動物では注意（急激な交感神経活性化）。",
        "drug_interactions": [],
    },
    {
        "id": "naloxone",
        "name": "Naloxone",
        "name_ja": "ナロキソン",
        "category": "analgesics",
        "mechanism": "Pure opioid antagonist; competitively blocks mu, kappa, and delta opioid receptors. Reverses opioid effects.",
        "mechanism_ja": "純粋オピオイド拮抗薬。μ、κ、δオピオイド受容体を競合的に遮断。オピオイド作用を拮抗する。",
        "routes": ["IV", "IM", "SC"],
        "routes_ja": ["静脈内", "筋肉内", "皮下"],
        "formulations": ["Injectable solution"],
        "formulations_ja": ["注射液"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "0.01-0.04 mg/kg IV (titrate); full reversal: 0.04 mg/kg",
                "dosage_ja": "0.01-0.04 mg/kg 静注（漸増）; 完全拮抗: 0.04 mg/kg",
                "notes": "Titrate to effect to maintain some analgesia; short duration (30-60 min)",
                "notes_ja": "効果が出るまで漸増投与し鎮痛を維持。短時間作用(30-60分)",
            },
            "cat": {
                "safe": True,
                "dosage": "0.01-0.04 mg/kg IV",
                "dosage_ja": "0.01-0.04 mg/kg 静注",
                "notes": "Same as dog; titrate carefully",
                "notes_ja": "犬と同様。慎重に漸増",
            },
            "horse": {
                "safe": True,
                "dosage": "0.01-0.02 mg/kg IV",
                "dosage_ja": "0.01-0.02 mg/kg 静注",
                "notes": "Reverses opioid-induced excitement; short acting",
                "notes_ja": "オピオイドによる興奮を拮抗。短時間作用",
            },
            "rabbit": {
                "safe": True,
                "dosage": "0.01-0.1 mg/kg IV/IM/SC",
                "dosage_ja": "0.01-0.1 mg/kg 静注/筋注/皮下",
                "notes": "For opioid overdose reversal",
                "notes_ja": "オピオイド過量投与の拮抗に",
            },
            "ferret": {
                "safe": True,
                "dosage": "0.01-0.03 mg/kg IV/IM",
                "dosage_ja": "0.01-0.03 mg/kg 静注/筋注",
                "notes": "Standard reversal",
                "notes_ja": "標準的拮抗",
            },
            "bird": {
                "safe": True,
                "dosage": "0.01-0.1 mg/kg IV/IM",
                "dosage_ja": "0.01-0.1 mg/kg 静注/筋注",
                "notes": "For butorphanol reversal",
                "notes_ja": "ブトルファノールの拮抗に",
            },
        },
        "side_effects": [
            "abrupt pain return",
            "tachycardia",
            "hypertension",
            "pulmonary edema (rare)",
            "re-narcotization (short duration)",
        ],
        "side_effects_ja": ["急激な疼痛の再現", "頻脈", "高血圧", "肺水腫(まれ)", "再麻薬化(短時間作用)"],
        "contraindications": "None absolute. Monitor for re-sedation (naloxone duration shorter than most opioids).",
        "contraindications_ja": "絶対的禁忌なし。再鎮静をモニタリング（ナロキソンの作用時間は多くのオピオイドより短い）。",
        "drug_interactions": [],
    },
    {
        "id": "flumazenil",
        "name": "Flumazenil",
        "name_ja": "フルマゼニル",
        "category": "sedatives",
        "mechanism": "Benzodiazepine antagonist; competitively binds GABA-A receptor benzodiazepine site.",
        "mechanism_ja": "ベンゾジアゼピン拮抗薬。GABA-A受容体のベンゾジアゼピン結合部位に競合的に結合。",
        "routes": ["IV"],
        "routes_ja": ["静脈内"],
        "formulations": ["Injectable solution"],
        "formulations_ja": ["注射液"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "0.01-0.02 mg/kg IV",
                "dosage_ja": "0.01-0.02 mg/kg 静注",
                "notes": "Reverses diazepam/midazolam; rapid onset",
                "notes_ja": "ジアゼパム/ミダゾラムを拮抗。速効性",
            },
            "cat": {
                "safe": True,
                "dosage": "0.01-0.02 mg/kg IV",
                "dosage_ja": "0.01-0.02 mg/kg 静注",
                "notes": "Effective reversal of benzodiazepines",
                "notes_ja": "ベンゾジアゼピンの効果的な拮抗",
            },
            "horse": {
                "safe": True,
                "dosage": "0.01 mg/kg IV",
                "dosage_ja": "0.01 mg/kg 静注",
                "notes": "Rarely needed; benzodiazepines uncommon in equine anesthesia",
                "notes_ja": "まれに必要。馬の麻酔でベンゾジアゼピンは一般的でない",
            },
            "rabbit": {
                "safe": True,
                "dosage": "0.01-0.1 mg/kg IV",
                "dosage_ja": "0.01-0.1 mg/kg 静注",
                "notes": "For reversing midazolam in rabbit protocols",
                "notes_ja": "ウサギプロトコルでミダゾラムの拮抗に",
            },
            "ferret": {
                "safe": True,
                "dosage": "0.01-0.02 mg/kg IV",
                "dosage_ja": "0.01-0.02 mg/kg 静注",
                "notes": "For benzodiazepine reversal",
                "notes_ja": "ベンゾジアゼピンの拮抗に",
            },
            "bird": {
                "safe": True,
                "dosage": "0.02-0.1 mg/kg IV/IM",
                "dosage_ja": "0.02-0.1 mg/kg 静注/筋注",
                "notes": "For midazolam reversal in avian patients",
                "notes_ja": "鳥類患者のミダゾラム拮抗に",
            },
        },
        "side_effects": ["seizures (if benzodiazepine was controlling them)", "anxiety", "agitation"],
        "side_effects_ja": ["痙攣(ベンゾジアゼピンが抑制していた場合)", "不安", "興奮"],
        "contraindications": "Patients receiving benzodiazepines for seizure control. Tricyclic antidepressant overdose.",
        "contraindications_ja": "痙攣管理のためにベンゾジアゼピンを投与中の患者。三環系抗うつ薬過量投与。",
        "drug_interactions": [],
    },
    {
        "id": "atropine",
        "name": "Atropine",
        "name_ja": "アトロピン",
        "category": "cardiovascular",
        "mechanism": "Anticholinergic (parasympatholytic); blocks muscarinic receptors, increasing heart rate and reducing secretions.",
        "mechanism_ja": "抗コリン薬（副交感神経遮断薬）。ムスカリン受容体を遮断し心拍数増加・分泌抑制。",
        "routes": ["IV", "IM", "SC"],
        "routes_ja": ["静脈内", "筋肉内", "皮下"],
        "formulations": ["Injectable solution"],
        "formulations_ja": ["注射液"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "0.02-0.04 mg/kg IV/IM/SC",
                "dosage_ja": "0.02-0.04 mg/kg 静注/筋注/皮下",
                "notes": "For bradycardia, organophosphate toxicity, preanesthetic",
                "notes_ja": "徐脈、有機リン中毒、麻酔前投薬に",
            },
            "cat": {
                "safe": True,
                "dosage": "0.02-0.04 mg/kg IV/IM/SC",
                "dosage_ja": "0.02-0.04 mg/kg 静注/筋注/皮下",
                "notes": "Standard anticholinergic",
                "notes_ja": "標準的な抗コリン薬",
            },
            "horse": {
                "safe": True,
                "dosage": "0.01-0.02 mg/kg IV",
                "dosage_ja": "0.01-0.02 mg/kg 静注",
                "notes": "Causes GI stasis - use with caution; may promote colic",
                "notes_ja": "消化管運動停止を引き起こす - 注意して使用。疝痛を促進する可能性",
            },
            "rabbit": {
                "safe": True,
                "dosage": "0.01-0.02 mg/kg SC/IM",
                "dosage_ja": "0.01-0.02 mg/kg 皮下/筋注",
                "notes": "Many rabbits have atropinase enzyme - glycopyrrolate preferred",
                "notes_ja": "多くのウサギはアトロピン分解酵素を持つ - グリコピロレートが好ましい",
            },
            "ferret": {
                "safe": True,
                "dosage": "0.02-0.04 mg/kg IM/SC",
                "dosage_ja": "0.02-0.04 mg/kg 筋注/皮下",
                "notes": "Standard dose",
                "notes_ja": "標準用量",
            },
            "bird": {
                "safe": True,
                "dosage": "0.01-0.02 mg/kg IM",
                "dosage_ja": "0.01-0.02 mg/kg 筋注",
                "notes": "For bradycardia during anesthesia",
                "notes_ja": "麻酔中の徐脈に",
            },
        },
        "side_effects": ["tachycardia", "mydriasis", "decreased GI motility", "dry mouth", "urinary retention"],
        "side_effects_ja": ["頻脈", "散瞳", "消化管運動低下", "口渇", "尿閉"],
        "contraindications": "Tachycardia. Glaucoma. GI obstruction. Horses (use glycopyrrolate instead).",
        "contraindications_ja": "頻脈。緑内障。消化管閉塞。馬（代わりにグリコピロレートを使用）。",
        "drug_interactions": [
            {
                "drug": "alpha-2 agonists",
                "effect": "Antagonizes alpha-2 induced bradycardia but may cause severe tachycardia/hypertension",
                "effect_ja": "α2誘発性徐脈を拮抗するが重度頻脈/高血圧を起こす可能性",
            }
        ],
    },
    {
        "id": "glycopyrrolate",
        "name": "Glycopyrrolate",
        "name_ja": "グリコピロレート",
        "category": "cardiovascular",
        "mechanism": "Synthetic quaternary ammonium anticholinergic; does not cross blood-brain barrier. Longer acting than atropine.",
        "mechanism_ja": "合成第四級アンモニウム抗コリン薬。血液脳関門を通過しない。アトロピンより作用時間が長い。",
        "routes": ["IV", "IM", "SC"],
        "routes_ja": ["静脈内", "筋肉内", "皮下"],
        "formulations": ["Injectable solution (Robinul-V)"],
        "formulations_ja": ["注射液（ロビナール-V）"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "0.005-0.01 mg/kg IV/IM/SC",
                "dosage_ja": "0.005-0.01 mg/kg 静注/筋注/皮下",
                "notes": "Preferred over atropine - less tachycardia, no CNS effects",
                "notes_ja": "アトロピンより好まれる - 頻脈が少ない、CNS作用なし",
            },
            "cat": {
                "safe": True,
                "dosage": "0.005-0.01 mg/kg IV/IM/SC",
                "dosage_ja": "0.005-0.01 mg/kg 静注/筋注/皮下",
                "notes": "Preferred anticholinergic for feline anesthesia",
                "notes_ja": "猫の麻酔に好まれる抗コリン薬",
            },
            "horse": {
                "safe": True,
                "dosage": "0.005 mg/kg IV",
                "dosage_ja": "0.005 mg/kg 静注",
                "notes": "Preferred over atropine in horses - less GI effects",
                "notes_ja": "馬ではアトロピンより好まれる - 消化器作用が少ない",
            },
            "rabbit": {
                "safe": True,
                "dosage": "0.01-0.02 mg/kg SC/IM",
                "dosage_ja": "0.01-0.02 mg/kg 皮下/筋注",
                "notes": "PREFERRED over atropine in rabbits (no atropinase issue)",
                "notes_ja": "ウサギではアトロピンより好まれる（アトロピン分解酵素の問題なし）",
            },
            "ferret": {
                "safe": True,
                "dosage": "0.01 mg/kg IM/SC",
                "dosage_ja": "0.01 mg/kg 筋注/皮下",
                "notes": "Good anticholinergic choice",
                "notes_ja": "良好な抗コリン薬の選択肢",
            },
            "bird": {
                "safe": True,
                "dosage": "0.01 mg/kg IM",
                "dosage_ja": "0.01 mg/kg 筋注",
                "notes": "For perioperative use",
                "notes_ja": "周術期使用に",
            },
        },
        "side_effects": ["tachycardia (less than atropine)", "decreased GI motility", "mydriasis", "urinary retention"],
        "side_effects_ja": ["頻脈(アトロピンより少ない)", "消化管運動低下", "散瞳", "尿閉"],
        "contraindications": "Tachyarrhythmias. GI obstruction/ileus.",
        "contraindications_ja": "頻脈性不整脈。消化管閉塞/イレウス。",
        "drug_interactions": [],
    },
    {
        "id": "digoxin",
        "name": "Digoxin",
        "name_ja": "ジゴキシン",
        "category": "cardiovascular",
        "mechanism": "Cardiac glycoside; inhibits Na+/K+-ATPase, increases intracellular calcium, enhances cardiac contractility. Also slows AV conduction.",
        "mechanism_ja": "強心配糖体。Na+/K+-ATPaseを阻害し細胞内カルシウムを増加させ心収縮力を増強。房室伝導も減速。",
        "routes": ["PO", "IV"],
        "routes_ja": ["経口", "静脈内"],
        "formulations": ["Tablets", "Elixir", "Injectable"],
        "formulations_ja": ["錠剤", "エリキシル", "注射剤"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "0.005-0.008 mg/kg PO q12h (0.22 mg/m2 q12h)",
                "dosage_ja": "0.005-0.008 mg/kg 経口 12時間毎",
                "notes": "Narrow therapeutic index; monitor serum levels (1-2 ng/mL); for supraventricular tachycardia, dilated cardiomyopathy",
                "notes_ja": "治療域が狭い。血中濃度モニタリング(1-2 ng/mL)。上室性頻拍、拡張型心筋症に",
            },
            "cat": {
                "safe": True,
                "dosage": "0.007 mg/kg PO q48h or 1/4 of 0.125mg tab q48h",
                "dosage_ja": "0.007 mg/kg 経口 48時間毎",
                "notes": "Cats very sensitive - lower doses, less frequent; toxic at low levels",
                "notes_ja": "猫は非常に敏感 - 低用量、低頻度。低濃度で中毒",
            },
            "horse": {
                "safe": True,
                "dosage": "0.011 mg/kg PO q12h",
                "dosage_ja": "0.011 mg/kg 経口 12時間毎",
                "notes": "For atrial fibrillation; monitor closely",
                "notes_ja": "心房細動に。厳密にモニタリング",
            },
            "ferret": {
                "safe": True,
                "dosage": "0.005-0.01 mg/kg PO q12-24h",
                "dosage_ja": "0.005-0.01 mg/kg 経口 12-24時間毎",
                "notes": "For dilated cardiomyopathy",
                "notes_ja": "拡張型心筋症に",
            },
            "rabbit": {
                "safe": True,
                "dosage": "0.005 mg/kg PO q12-24h",
                "dosage_ja": "0.005 mg/kg 経口 12-24時間毎",
                "notes": "Limited use; monitor closely",
                "notes_ja": "限定的使用。厳密にモニタリング",
            },
            "bird": {
                "safe": True,
                "dosage": "0.02-0.05 mg/kg PO q12-24h",
                "dosage_ja": "0.02-0.05 mg/kg 経口 12-24時間毎",
                "notes": "For congestive heart failure in birds",
                "notes_ja": "鳥類のうっ血性心不全に",
            },
        },
        "side_effects": [
            "anorexia",
            "vomiting",
            "diarrhea",
            "cardiac arrhythmias",
            "lethargy",
            "toxicity with hypokalemia",
        ],
        "side_effects_ja": ["食欲不振", "嘔吐", "下痢", "心不整脈", "元気消失", "低カリウム血症で毒性増強"],
        "contraindications": "Hypertrophic cardiomyopathy. Ventricular arrhythmias. Hypokalemia. Hypercalcemia. Renal insufficiency (dose adjust).",
        "contraindications_ja": "肥大型心筋症。心室性不整脈。低カリウム血症。高カルシウム血症。腎不全（用量調整）。",
        "drug_interactions": [
            {
                "drug": "furosemide",
                "effect": "Hypokalemia increases digoxin toxicity",
                "effect_ja": "低カリウム血症がジゴキシン毒性を増加",
            },
            {"drug": "diltiazem", "effect": "Increased digoxin levels", "effect_ja": "ジゴキシン血中濃度上昇"},
            {"drug": "quinidine", "effect": "Doubles digoxin levels", "effect_ja": "ジゴキシン濃度を2倍に上昇"},
        ],
    },
    {
        "id": "diltiazem",
        "name": "Diltiazem",
        "name_ja": "ジルチアゼム",
        "category": "cardiovascular",
        "mechanism": "Calcium channel blocker (benzothiazepine class); reduces heart rate, slows AV conduction, mild vasodilation.",
        "mechanism_ja": "カルシウムチャネル遮断薬（ベンゾチアゼピン系）。心拍数低下、房室伝導減速、軽度血管拡張。",
        "routes": ["PO", "IV"],
        "routes_ja": ["経口", "静脈内"],
        "formulations": ["Tablets", "Extended-release capsules", "Injectable"],
        "formulations_ja": ["錠剤", "徐放性カプセル", "注射剤"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "0.5-1.5 mg/kg PO q8h; IV: 0.15-0.25 mg/kg bolus",
                "dosage_ja": "0.5-1.5 mg/kg 経口 8時間毎; 静注: 0.15-0.25 mg/kg ボーラス",
                "notes": "For supraventricular tachycardia, atrial fibrillation rate control",
                "notes_ja": "上室性頻拍、心房細動のレートコントロールに",
            },
            "cat": {
                "safe": True,
                "dosage": "1.5-2.5 mg/kg PO q8h; diltiazem CD: 10 mg/kg PO q24h",
                "dosage_ja": "1.5-2.5 mg/kg 経口 8時間毎; ジルチアゼムCD: 10 mg/kg 経口 24時間毎",
                "notes": "Drug of choice for feline HCM; reduces heart rate and improves diastolic function",
                "notes_ja": "猫HCMの第一選択薬。心拍数低下と拡張機能改善",
            },
            "horse": {
                "safe": True,
                "dosage": "0.125 mg/kg/min IV CRI",
                "dosage_ja": "0.125 mg/kg/min 静注持続点滴",
                "notes": "For atrial fibrillation conversion",
                "notes_ja": "心房細動の変換に",
            },
            "ferret": {
                "safe": True,
                "dosage": "3.75-7.5 mg/ferret PO q12h",
                "dosage_ja": "3.75-7.5 mg/匹 経口 12時間毎",
                "notes": "For hypertrophic cardiomyopathy",
                "notes_ja": "肥大型心筋症に",
            },
            "rabbit": {
                "safe": True,
                "dosage": "0.5-1 mg/kg PO q12h",
                "dosage_ja": "0.5-1 mg/kg 経口 12時間毎",
                "notes": "Limited data; for tachyarrhythmias",
                "notes_ja": "データ限定的。頻脈性不整脈に",
            },
            "bird": {
                "safe": True,
                "dosage": "Not well established",
                "dosage_ja": "十分に確立されていない",
                "notes": "Limited avian data",
                "notes_ja": "鳥類のデータは限定的",
            },
        },
        "side_effects": ["bradycardia", "hypotension", "AV block", "anorexia", "lethargy"],
        "side_effects_ja": ["徐脈", "低血圧", "房室ブロック", "食欲不振", "元気消失"],
        "contraindications": "Severe bradycardia. High-grade AV block. Systolic heart failure (negative inotrope). Concurrent beta-blocker use.",
        "contraindications_ja": "重度徐脈。高度房室ブロック。収縮性心不全（陰性変力作用）。β遮断薬との併用。",
        "drug_interactions": [
            {"drug": "beta-blockers", "effect": "Severe bradycardia/heart block", "effect_ja": "重度徐脈/心ブロック"},
            {"drug": "digoxin", "effect": "Increased digoxin levels", "effect_ja": "ジゴキシン濃度上昇"},
        ],
    },
    {
        "id": "sildenafil",
        "name": "Sildenafil",
        "name_ja": "シルデナフィル",
        "category": "cardiovascular",
        "mechanism": "Phosphodiesterase-5 (PDE5) inhibitor; causes pulmonary vasodilation by increasing cGMP.",
        "mechanism_ja": "ホスホジエステラーゼ5（PDE5）阻害薬。cGMP増加により肺血管拡張を引き起こす。",
        "routes": ["PO"],
        "routes_ja": ["経口"],
        "formulations": ["Tablets"],
        "formulations_ja": ["錠剤"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "1-2 mg/kg PO q8-12h",
                "dosage_ja": "1-2 mg/kg 経口 8-12時間毎",
                "notes": "For pulmonary hypertension; becoming standard of care",
                "notes_ja": "肺高血圧症に。標準治療になりつつある",
            },
            "cat": {
                "safe": True,
                "dosage": "1-2 mg/kg PO q8-12h",
                "dosage_ja": "1-2 mg/kg 経口 8-12時間毎",
                "notes": "For pulmonary hypertension secondary to cardiac disease",
                "notes_ja": "心疾患に続発する肺高血圧症に",
            },
            "horse": {
                "safe": True,
                "dosage": "1-2 mg/kg PO q12h",
                "dosage_ja": "1-2 mg/kg 経口 12時間毎",
                "notes": "Limited equine data; used in neonatal pulmonary hypertension",
                "notes_ja": "馬のデータは限定的。新生子肺高血圧症に使用",
            },
            "ferret": {
                "safe": True,
                "dosage": "1-2 mg/kg PO q8-12h",
                "dosage_ja": "1-2 mg/kg 経口 8-12時間毎",
                "notes": "For pulmonary hypertension",
                "notes_ja": "肺高血圧症に",
            },
            "rabbit": {
                "safe": True,
                "dosage": "1 mg/kg PO q12h",
                "dosage_ja": "1 mg/kg 経口 12時間毎",
                "notes": "Limited data",
                "notes_ja": "データ限定的",
            },
            "bird": {
                "safe": True,
                "dosage": "Not well established",
                "dosage_ja": "十分に確立されていない",
                "notes": "Limited avian data",
                "notes_ja": "鳥類のデータは限定的",
            },
        },
        "side_effects": ["hypotension", "facial flushing", "nasal congestion", "tachycardia"],
        "side_effects_ja": ["低血圧", "顔面紅潮", "鼻閉", "頻脈"],
        "contraindications": "Concurrent nitrate therapy. Severe systemic hypotension.",
        "contraindications_ja": "硝酸薬との併用。重度全身性低血圧。",
        "drug_interactions": [
            {"drug": "nitrates", "effect": "CONTRAINDICATED - severe hypotension", "effect_ja": "【禁忌】重度低血圧"}
        ],
    },
    {
        "id": "aminophylline",
        "name": "Aminophylline",
        "name_ja": "アミノフィリン",
        "category": "bronchodilators",
        "mechanism": "Methylxanthine bronchodilator; inhibits phosphodiesterase, antagonizes adenosine, stimulates diaphragm.",
        "mechanism_ja": "メチルキサンチン系気管支拡張薬。ホスホジエステラーゼ阻害、アデノシン拮抗、横隔膜刺激。",
        "routes": ["PO", "IV"],
        "routes_ja": ["経口", "静脈内"],
        "formulations": ["Tablets", "Injectable solution"],
        "formulations_ja": ["錠剤", "注射液"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "10 mg/kg PO q8h; IV: 5-10 mg/kg slow IV",
                "dosage_ja": "10 mg/kg 経口 8時間毎; 静注: 5-10 mg/kg ゆっくり静注",
                "notes": "For bronchospasm, collapsing trachea; narrow therapeutic index",
                "notes_ja": "気管支痙攣、気管虚脱に。治療域が狭い",
            },
            "cat": {
                "safe": True,
                "dosage": "5 mg/kg PO q12h",
                "dosage_ja": "5 mg/kg 経口 12時間毎",
                "notes": "For feline asthma; cats more sensitive",
                "notes_ja": "猫喘息に。猫はより敏感",
            },
            "horse": {
                "safe": True,
                "dosage": "5-10 mg/kg IV slowly",
                "dosage_ja": "5-10 mg/kg ゆっくり静注",
                "notes": "For heaves/RAO; give IV slowly to avoid arrhythmias",
                "notes_ja": "鼻膿漏/RAOに。不整脈予防のためゆっくり静注",
            },
            "rabbit": {
                "safe": True,
                "dosage": "4-8 mg/kg PO q8-12h",
                "dosage_ja": "4-8 mg/kg 経口 8-12時間毎",
                "notes": "For respiratory conditions",
                "notes_ja": "呼吸器疾患に",
            },
            "bird": {
                "safe": True,
                "dosage": "10 mg/kg PO q12h",
                "dosage_ja": "10 mg/kg 経口 12時間毎",
                "notes": "For air sac disease",
                "notes_ja": "気嚢疾患に",
            },
            "reptile": {
                "safe": True,
                "dosage": "Not well established",
                "dosage_ja": "十分に確立されていない",
                "notes": "Limited data",
                "notes_ja": "データ限定的",
            },
        },
        "side_effects": ["tachycardia", "restlessness", "GI upset", "seizures (overdose)", "arrhythmias"],
        "side_effects_ja": ["頻脈", "不穏", "消化器症状", "痙攣(過量投与)", "不整脈"],
        "contraindications": "Active seizure disorder. Severe cardiac arrhythmias. Gastric ulcers.",
        "contraindications_ja": "活動性痙攣障害。重度心不整脈。胃潰瘍。",
        "drug_interactions": [
            {
                "drug": "fluoroquinolones",
                "effect": "Increased theophylline levels",
                "effect_ja": "テオフィリン濃度上昇",
            },
            {"drug": "erythromycin", "effect": "Increased theophylline levels", "effect_ja": "テオフィリン濃度上昇"},
        ],
    },
    {
        "id": "terbutaline",
        "name": "Terbutaline",
        "name_ja": "テルブタリン",
        "category": "bronchodilators",
        "mechanism": "Selective beta-2 adrenergic agonist; relaxes bronchial smooth muscle.",
        "mechanism_ja": "選択的β2アドレナリン作動薬。気管支平滑筋を弛緩させる。",
        "routes": ["PO", "SC", "IV"],
        "routes_ja": ["経口", "皮下", "静脈内"],
        "formulations": ["Tablets", "Injectable solution"],
        "formulations_ja": ["錠剤", "注射液"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "1.25-5 mg/dog PO q8-12h; 0.01 mg/kg SC/IM for acute",
                "dosage_ja": "1.25-5 mg/匹 経口 8-12時間毎; 急性: 0.01 mg/kg 皮下/筋注",
                "notes": "For bronchospasm, collapsing trachea, status asthmaticus",
                "notes_ja": "気管支痙攣、気管虚脱、喘息重積に",
            },
            "cat": {
                "safe": True,
                "dosage": "0.01 mg/kg SC for acute; 0.625 mg/cat PO q12h",
                "dosage_ja": "急性: 0.01 mg/kg 皮下; 0.625 mg/匹 経口 12時間毎",
                "notes": "Emergency bronchodilator for feline asthma",
                "notes_ja": "猫喘息の緊急気管支拡張薬",
            },
            "horse": {
                "safe": True,
                "dosage": "0.02 mg/kg IV slowly",
                "dosage_ja": "0.02 mg/kg ゆっくり静注",
                "notes": "For acute bronchospasm",
                "notes_ja": "急性気管支痙攣に",
            },
            "guinea_pig": {
                "safe": True,
                "dosage": "0.01 mg/kg SC/IM",
                "dosage_ja": "0.01 mg/kg 皮下/筋注",
                "notes": "For respiratory distress",
                "notes_ja": "呼吸困難に",
            },
            "rabbit": {
                "safe": True,
                "dosage": "0.01 mg/kg SC",
                "dosage_ja": "0.01 mg/kg 皮下",
                "notes": "For respiratory emergencies",
                "notes_ja": "呼吸器の緊急時に",
            },
            "bird": {
                "safe": True,
                "dosage": "0.01 mg/kg IM",
                "dosage_ja": "0.01 mg/kg 筋注",
                "notes": "For acute respiratory distress",
                "notes_ja": "急性呼吸困難に",
            },
        },
        "side_effects": ["tachycardia", "tremors", "restlessness", "hypokalemia"],
        "side_effects_ja": ["頻脈", "振戦", "不穏", "低カリウム血症"],
        "contraindications": "Tachyarrhythmias. Severe cardiac disease.",
        "contraindications_ja": "頻脈性不整脈。重度心疾患。",
        "drug_interactions": [
            {"drug": "beta-blockers", "effect": "Antagonistic effects", "effect_ja": "拮抗作用"},
            {"drug": "MAO inhibitors", "effect": "Enhanced cardiovascular effects", "effect_ja": "心血管作用の増強"},
        ],
    },
    {
        "id": "cisapride",
        "name": "Cisapride",
        "name_ja": "シサプリド",
        "category": "gi_drugs",
        "mechanism": "Serotonin 5-HT4 receptor agonist; enhances GI motility throughout the GI tract.",
        "mechanism_ja": "セロトニン5-HT4受容体作動薬。消化管全体の運動を促進する。",
        "routes": ["PO"],
        "routes_ja": ["経口"],
        "formulations": ["Compounded oral suspension", "Compounded tablets"],
        "formulations_ja": ["院内調製経口懸濁液", "院内調製錠剤"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "0.1-0.5 mg/kg PO q8-12h",
                "dosage_ja": "0.1-0.5 mg/kg 経口 8-12時間毎",
                "notes": "For gastroparesis, chronic constipation; compounded only",
                "notes_ja": "胃不全麻痺、慢性便秘に。院内調製のみ",
            },
            "cat": {
                "safe": True,
                "dosage": "2.5-5 mg/cat PO q8-12h",
                "dosage_ja": "2.5-5 mg/匹 経口 8-12時間毎",
                "notes": "Drug of choice for feline megacolon/constipation",
                "notes_ja": "猫の巨大結腸症/便秘の第一選択薬",
            },
            "horse": {
                "safe": True,
                "dosage": "0.1-0.2 mg/kg IV/PO q6-8h",
                "dosage_ja": "0.1-0.2 mg/kg 静注/経口 6-8時間毎",
                "notes": "For post-operative ileus",
                "notes_ja": "術後イレウスに",
            },
            "rabbit": {
                "safe": True,
                "dosage": "0.5 mg/kg PO q8-12h",
                "dosage_ja": "0.5 mg/kg 経口 8-12時間毎",
                "notes": "For GI stasis - very important in rabbit medicine",
                "notes_ja": "消化管鬱滞に - ウサギ医学で非常に重要",
            },
            "guinea_pig": {
                "safe": True,
                "dosage": "0.5 mg/kg PO q8h",
                "dosage_ja": "0.5 mg/kg 経口 8時間毎",
                "notes": "For GI stasis",
                "notes_ja": "消化管鬱滞に",
            },
            "ferret": {
                "safe": True,
                "dosage": "0.5 mg/kg PO q8h",
                "dosage_ja": "0.5 mg/kg 経口 8時間毎",
                "notes": "For hairball-related GI stasis",
                "notes_ja": "毛球関連の消化管鬱滞に",
            },
        },
        "side_effects": ["diarrhea", "cramping", "rare cardiac arrhythmias (QT prolongation)"],
        "side_effects_ja": ["下痢", "腹部痙攣", "まれな心不整脈(QT延長)"],
        "contraindications": "GI obstruction. Concurrent QT-prolonging drugs. GI perforation/hemorrhage.",
        "contraindications_ja": "消化管閉塞。QT延長薬との併用。消化管穿孔/出血。",
        "drug_interactions": [
            {
                "drug": "ketoconazole",
                "effect": "Increased cisapride levels - cardiac risk",
                "effect_ja": "シサプリド濃度上昇 - 心臓リスク",
            },
            {"drug": "erythromycin", "effect": "QT prolongation risk", "effect_ja": "QT延長リスク"},
        ],
    },
    {
        "id": "mosapride",
        "name": "Mosapride",
        "name_ja": "モサプリド",
        "category": "gi_drugs",
        "mechanism": "Selective serotonin 5-HT4 receptor agonist; enhances gastric emptying and upper GI motility without QT prolongation risk (unlike cisapride).",
        "mechanism_ja": "選択的セロトニン5-HT4受容体作動薬。シサプリドと異なりQT延長リスクなく、胃排出能・上部消化管運動を促進する。",
        "routes": ["PO"],
        "routes_ja": ["経口"],
        "formulations": ["Tablets (Gasmotin 5mg)", "Powder"],
        "formulations_ja": ["錠剤（ガスモチン5mg）", "散剤"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "0.25-1.0 mg/kg PO q8-12h",
                "dosage_ja": "0.25-1.0 mg/kg 経口 8-12時間毎",
                "notes": "For gastroparesis, functional dyspepsia, post-operative ileus. Safer cardiac profile than cisapride.",
                "notes_ja": "胃不全麻痺、機能性ディスペプシア、術後イレウスに。シサプリドより心臓安全性が高い。",
            },
            "cat": {
                "safe": True,
                "dosage": "0.25-0.5 mg/kg PO q8-12h",
                "dosage_ja": "0.25-0.5 mg/kg 経口 8-12時間毎",
                "notes": "For delayed gastric emptying, chronic vomiting. May be less effective than cisapride for megacolon.",
                "notes_ja": "胃排出遅延、慢性嘔吐に。巨大結腸症にはシサプリドより効果が劣る可能性。",
            },
            "rabbit": {
                "safe": True,
                "dosage": "0.5-1.0 mg/kg PO q8-12h",
                "dosage_ja": "0.5-1.0 mg/kg 経口 8-12時間毎",
                "notes": "For GI stasis; alternative to cisapride. Commercially available in Japan (Gasmotin).",
                "notes_ja": "消化管鬱滞に。シサプリドの代替。日本では市販品（ガスモチン）が入手可能。",
            },
            "guinea_pig": {
                "safe": True,
                "dosage": "0.5 mg/kg PO q8-12h",
                "dosage_ja": "0.5 mg/kg 経口 8-12時間毎",
                "notes": "For GI stasis. Limited species-specific data; extrapolated from rabbit dosing.",
                "notes_ja": "消化管鬱滞に。種特異的データは限定的。ウサギの用量から外挿。",
            },
            "ferret": {
                "safe": True,
                "dosage": "0.5 mg/kg PO q8-12h",
                "dosage_ja": "0.5 mg/kg 経口 8-12時間毎",
                "notes": "For GI motility disorders. Alternative to cisapride.",
                "notes_ja": "消化管運動障害に。シサプリドの代替。",
            },
            "horse": {
                "safe": True,
                "dosage": "0.5-1.0 mg/kg PO q8-12h",
                "dosage_ja": "0.5-1.0 mg/kg 経口 8-12時間毎",
                "notes": "For post-operative ileus. Limited equine data.",
                "notes_ja": "術後イレウスに。馬のデータは限定的。",
            },
        },
        "side_effects": ["diarrhea", "soft stool", "abdominal discomfort"],
        "side_effects_ja": ["下痢", "軟便", "腹部不快感"],
        "contraindications": "GI obstruction. GI perforation/hemorrhage.",
        "contraindications_ja": "消化管閉塞。消化管穿孔/出血。",
        "drug_interactions": [
            {
                "drug": "erythromycin",
                "effect": "Additive prokinetic effect; monitor for diarrhea",
                "effect_ja": "消化管運動促進の相加作用。下痢に注意",
            },
            {
                "drug": "anticholinergics",
                "effect": "Antagonistic on GI motility",
                "effect_ja": "消化管運動に対して拮抗",
            },
        ],
    },
    {
        "id": "scopolamine_butylbromide",
        "name": "Scopolamine Butylbromide",
        "name_ja": "ブチルスコポラミン臭化物",
        "category": "gi_drugs",
        "mechanism": "Anticholinergic (antimuscarinic) antispasmodic; blocks muscarinic receptors on GI and urogenital smooth muscle, relieving spasm without significant CNS effects (quaternary ammonium, does not cross BBB).",
        "mechanism_ja": "抗コリン薬（抗ムスカリン薬）鎮痙薬。消化管・泌尿生殖器の平滑筋ムスカリン受容体を遮断し痙攣を緩和する。第四級アンモニウム化合物のため血液脳関門を通過しない。",
        "routes": ["IV", "IM", "SC", "PO"],
        "routes_ja": ["静脈内", "筋肉内", "皮下", "経口"],
        "formulations": ["Tablets (Buscopan/Scapal 10mg)", "Injectable solution (20mg/mL)"],
        "formulations_ja": ["錠剤（ブスコパン/スカパール 10mg）", "注射液（20mg/mL）"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "0.3-0.5 mg/kg IV/IM/SC; PO: 0.3-0.5 mg/kg q8-12h",
                "dosage_ja": "0.3-0.5 mg/kg 静注/筋注/皮下; 経口: 0.3-0.5 mg/kg 8-12時間毎",
                "notes": "For GI spasm, colic-like abdominal pain, urinary tract spasm. Short-acting (20-30 min IV).",
                "notes_ja": "消化管痙攣、疝痛様腹痛、尿路痙攣に。作用時間は短い（静注で20-30分）。",
            },
            "cat": {
                "safe": True,
                "dosage": "0.3-0.5 mg/kg IV/IM/SC; PO: 0.3-0.5 mg/kg q8-12h",
                "dosage_ja": "0.3-0.5 mg/kg 静注/筋注/皮下; 経口: 0.3-0.5 mg/kg 8-12時間毎",
                "notes": "For GI spasm, urinary tract spasm. Use cautiously - may mask signs of obstruction.",
                "notes_ja": "消化管痙攣、尿路痙攣に。閉塞の徴候をマスクする可能性があるため慎重に使用。",
            },
            "horse": {
                "safe": True,
                "dosage": "0.3 mg/kg IV (max 5 mL of 20mg/mL)",
                "dosage_ja": "0.3 mg/kg 静注（20mg/mL製剤で最大5mL）",
                "notes": "Antispasmodic indicated for spasmodic, flatulent, and simple impaction colic (Roelvink 1991; Boehringer field trial: 88% success vs 42% placebo). NOT a primary analgesic — flunixin meglumine 1.1 mg/kg IV is the first-line analgesic for colic pain control (BEVA 2020 Analgesia Guidelines; Bowen et al. EVJ 2020). Typically used as adjunct to flunixin when spasmodic component is suspected. Causes transient tachycardia (20-30 min) and decreased borborygmi, which may temporarily mask abdominal auscultation findings.",
                "notes_ja": "痙攣性・鼓腸性・単純閉塞性疝痛に適応のある鎮痙薬（Roelvink 1991; Boehringer 臨床試験: 成功率88% vs プラセボ42%）。本剤は一次鎮痛薬ではない — 疝痛の疼痛コントロールにおける第一選択はフルニキシンメグルミン1.1 mg/kg 静注である（BEVA 2020 鎮痛ガイドライン; Bowen et al. EVJ 2020）。痙攣性要素が疑われる場合にフルニキシンの補助として併用されるのが一般的。一過性頻脈（20-30分）と腸蠕動音低下を引き起こし、腹部聴診所見を一時的にマスクする可能性あり。",
            },
            "rabbit": {
                "safe": True,
                "dosage": "0.3-0.5 mg/kg SC/IM",
                "dosage_ja": "0.3-0.5 mg/kg 皮下/筋注",
                "notes": "For GI spasm. Use with caution - anticholinergics can worsen GI stasis. Short-term use only.",
                "notes_ja": "消化管痙攣に。抗コリン薬は消化管鬱滞を悪化させる可能性があるため慎重に。短期使用のみ。",
            },
            "guinea_pig": {
                "safe": True,
                "dosage": "0.3-0.5 mg/kg SC/IM",
                "dosage_ja": "0.3-0.5 mg/kg 皮下/筋注",
                "notes": "For acute GI spasm only. May reduce GI motility; avoid prolonged use.",
                "notes_ja": "急性消化管痙攣のみに使用。消化管運動を低下させるため長期使用は避ける。",
            },
            "ferret": {
                "safe": True,
                "dosage": "0.3-0.5 mg/kg SC/IM",
                "dosage_ja": "0.3-0.5 mg/kg 皮下/筋注",
                "notes": "For acute abdominal spasm. Short-term use.",
                "notes_ja": "急性腹部痙攣に。短期使用。",
            },
        },
        "side_effects": [
            "tachycardia",
            "decreased GI motility",
            "mydriasis",
            "dry mouth",
            "urinary retention",
            "transient ileus",
        ],
        "side_effects_ja": ["頻脈", "消化管運動低下", "散瞳", "口渇", "尿閉", "一過性イレウス"],
        "contraindications": "GI obstruction (mechanical). Paralytic ileus. Glaucoma. Tachyarrhythmias. Megacolon.",
        "contraindications_ja": "消化管閉塞（機械的）。麻痺性イレウス。緑内障。頻脈性不整脈。巨大結腸症。",
        "drug_interactions": [
            {
                "drug": "metoclopramide/cisapride/mosapride",
                "effect": "Antagonistic on GI motility; concurrent use reduces prokinetic efficacy",
                "effect_ja": "消化管運動に対して拮抗。併用により消化管運動促進薬の効果が低下",
            },
            {
                "drug": "antihistamines/tricyclic antidepressants",
                "effect": "Additive anticholinergic effects (tachycardia, dry mouth, urinary retention)",
                "effect_ja": "抗コリン作用の相加（頻脈、口渇、尿閉）",
            },
        ],
    },
    {
        "id": "mirtazapine",
        "name": "Mirtazapine",
        "name_ja": "ミルタザピン",
        "category": "antiemetics",
        "mechanism": "Tetracyclic antidepressant; 5-HT3 antagonist with appetite-stimulating properties. Also antiemetic.",
        "mechanism_ja": "四環系抗うつ薬。食欲刺激特性を持つ5-HT3拮抗薬。制吐作用もある。",
        "routes": ["PO", "transdermal"],
        "routes_ja": ["経口", "経皮"],
        "formulations": ["Tablets", "Transdermal ointment (Mirataz for cats)"],
        "formulations_ja": ["錠剤", "経皮軟膏（猫用ミラタズ）"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "1.88 mg/dog (<10kg) to 3.75 mg/dog (>10kg) PO q24h",
                "dosage_ja": "1.88 mg/匹(<10kg) ～ 3.75 mg/匹(>10kg) 経口 24時間毎",
                "notes": "Effective appetite stimulant; also antiemetic",
                "notes_ja": "効果的な食欲刺激薬。制吐作用もあり",
            },
            "cat": {
                "safe": True,
                "dosage": "1.88 mg/cat PO q48h; Mirataz: 2-inch strip on inner ear pinna q24h",
                "dosage_ja": "1.88 mg/匹 経口 48時間毎; ミラタズ: 2インチを耳介内側に24時間毎",
                "notes": "FDA-approved transdermal (Mirataz) for weight loss in cats; excellent appetite stimulant",
                "notes_ja": "猫の体重減少にFDA承認経皮製剤（ミラタズ）。優れた食欲刺激薬",
            },
            "horse": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Not studied in horses",
                "notes_ja": "馬では未研究",
            },
            "rabbit": {
                "safe": True,
                "dosage": "0.5-1 mg/kg PO q24h",
                "dosage_ja": "0.5-1 mg/kg 経口 24時間毎",
                "notes": "Off-label appetite stimulant",
                "notes_ja": "適応外の食欲刺激薬",
            },
            "ferret": {
                "safe": True,
                "dosage": "0.9 mg/kg PO q48h",
                "dosage_ja": "0.9 mg/kg 経口 48時間毎",
                "notes": "Effective appetite stimulant in ferrets",
                "notes_ja": "フェレットの効果的な食欲刺激薬",
            },
            "bird": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Safety not established in birds",
                "notes_ja": "鳥類での安全性未確立",
            },
        },
        "side_effects": ["vocalization", "restlessness", "serotonin syndrome (overdose)", "tachycardia"],
        "side_effects_ja": ["発声", "不穏", "セロトニン症候群(過量投与)", "頻脈"],
        "contraindications": "Concurrent SSRI/MAOI use (serotonin syndrome risk). Hepatic disease (cats - adjust interval to q72h).",
        "contraindications_ja": "SSRI/MAOI併用（セロトニン症候群リスク）。肝疾患（猫 - 投与間隔をq72hに調整）。",
        "drug_interactions": [
            {"drug": "SSRIs", "effect": "Serotonin syndrome risk", "effect_ja": "セロトニン症候群リスク"},
            {"drug": "tramadol", "effect": "Serotonin syndrome risk", "effect_ja": "セロトニン症候群リスク"},
        ],
    },
    {
        "id": "toceranib",
        "name": "Toceranib Phosphate",
        "name_ja": "トセラニブリン酸塩",
        "category": "antineoplastics",
        "mechanism": "Multi-targeted receptor tyrosine kinase inhibitor (Palladia); inhibits VEGFR, PDGFR, Kit.",
        "mechanism_ja": "多標的受容体チロシンキナーゼ阻害薬（パラディア）。VEGFR、PDGFR、Kitを阻害。",
        "routes": ["PO"],
        "routes_ja": ["経口"],
        "formulations": ["Tablets (Palladia)"],
        "formulations_ja": ["錠剤（パラディア）"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "2.75 mg/kg PO every other day",
                "dosage_ja": "2.75 mg/kg 経口 隔日",
                "notes": "FDA-approved for canine mast cell tumors; first veterinary TKI",
                "notes_ja": "犬肥満細胞腫にFDA承認。初の動物用TKI",
            },
            "cat": {
                "safe": True,
                "dosage": "2.5 mg/kg PO every other day",
                "dosage_ja": "2.5 mg/kg 経口 隔日",
                "notes": "Off-label use for various feline tumors; SCC, lymphoma",
                "notes_ja": "各種猫腫瘍に適応外使用。扁平上皮癌、リンパ腫",
            },
            "horse": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Not studied",
                "notes_ja": "未研究",
            },
            "rabbit": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Not approved",
                "notes_ja": "未承認",
            },
            "ferret": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Limited data",
                "notes_ja": "データ限定的",
            },
            "bird": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Not studied",
                "notes_ja": "未研究",
            },
        },
        "side_effects": ["diarrhea", "anorexia", "lameness", "weight loss", "vomiting", "neutropenia", "GI hemorrhage"],
        "side_effects_ja": ["下痢", "食欲不振", "跛行", "体重減少", "嘔吐", "好中球減少", "消化管出血"],
        "contraindications": "Pregnancy. Concurrent NSAIDs (increased GI bleeding). Handler precautions required.",
        "contraindications_ja": "妊娠中。NSAIDs併用（消化管出血増加）。取扱者の注意が必要。",
        "drug_interactions": [
            {"drug": "NSAIDs", "effect": "Increased GI ulceration/hemorrhage", "effect_ja": "消化管潰瘍/出血増加"}
        ],
    },
    {
        "id": "azathioprine",
        "name": "Azathioprine",
        "name_ja": "アザチオプリン",
        "category": "immunosuppressives",
        "mechanism": "Purine analog; inhibits DNA/RNA synthesis in rapidly dividing immune cells.",
        "mechanism_ja": "プリンアナログ。急速に分裂する免疫細胞のDNA/RNA合成を阻害。",
        "routes": ["PO"],
        "routes_ja": ["経口"],
        "formulations": ["Tablets"],
        "formulations_ja": ["錠剤"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "2 mg/kg PO q24h (then q48h after 2 weeks)",
                "dosage_ja": "2 mg/kg 経口 24時間毎（2週間後q48h）",
                "notes": "For IMHA, IMTP, IBD; monitor CBC biweekly",
                "notes_ja": "IMHA・IMTP・IBDに。隔週でCBCモニタリング",
            },
            "cat": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "CONTRAINDICATED - causes fatal bone marrow suppression in cats",
                "notes_ja": "【禁忌】猫で致死的な骨髄抑制を引き起こす",
            },
            "horse": {
                "safe": True,
                "dosage": "3 mg/kg PO q24h",
                "dosage_ja": "3 mg/kg 経口 24時間毎",
                "notes": "For immune-mediated conditions; limited equine data",
                "notes_ja": "免疫介在性疾患に。馬のデータは限定的",
            },
            "rabbit": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Risk of bone marrow suppression",
                "notes_ja": "骨髄抑制のリスク",
            },
            "ferret": {
                "safe": True,
                "dosage": "0.9 mg/kg PO q24-72h",
                "dosage_ja": "0.9 mg/kg 経口 24-72時間毎",
                "notes": "Limited use; monitor closely",
                "notes_ja": "限定的使用。厳密にモニタリング",
            },
            "bird": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Not recommended",
                "notes_ja": "推奨されない",
            },
        },
        "side_effects": [
            "bone marrow suppression",
            "hepatotoxicity",
            "pancreatitis",
            "GI upset",
            "increased infection risk",
        ],
        "side_effects_ja": ["骨髄抑制", "肝毒性", "膵炎", "消化器症状", "感染リスク増加"],
        "contraindications": "Cats (fatal). Pregnancy. Active infection. Concurrent allopurinol (potentiates toxicity).",
        "contraindications_ja": "猫（致死的）。妊娠中。活動性感染。アロプリノール併用（毒性増強）。",
        "drug_interactions": [
            {
                "drug": "allopurinol",
                "effect": "Dramatically increases azathioprine toxicity - dose must be reduced 75%",
                "effect_ja": "アザチオプリン毒性を劇的に増加 - 75%減量が必要",
            }
        ],
    },
    {
        "id": "mycophenolate",
        "name": "Mycophenolate Mofetil",
        "name_ja": "ミコフェノール酸モフェチル",
        "category": "immunosuppressives",
        "mechanism": "Reversible inhibitor of inosine monophosphate dehydrogenase; selectively inhibits lymphocyte proliferation.",
        "mechanism_ja": "イノシン一リン酸脱水素酵素の可逆的阻害薬。リンパ球増殖を選択的に阻害。",
        "routes": ["PO", "IV"],
        "routes_ja": ["経口", "静脈内"],
        "formulations": ["Tablets", "Capsules", "Injectable"],
        "formulations_ja": ["錠剤", "カプセル", "注射剤"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "10-20 mg/kg PO q12h",
                "dosage_ja": "10-20 mg/kg 経口 12時間毎",
                "notes": "Alternative to azathioprine; for IMHA, IMTP, meningoencephalitis",
                "notes_ja": "アザチオプリンの代替。IMHA・IMTP・髄膜脳炎に",
            },
            "cat": {
                "safe": True,
                "dosage": "10 mg/kg PO q12h",
                "dosage_ja": "10 mg/kg 経口 12時間毎",
                "notes": "Safer alternative to azathioprine for cats; for IMHA, IBD",
                "notes_ja": "猫でアザチオプリンより安全な代替。IMHA・IBDに",
            },
            "horse": {
                "safe": True,
                "dosage": "Not well established",
                "dosage_ja": "十分に確立されていない",
                "notes": "Limited equine data",
                "notes_ja": "馬のデータは限定的",
            },
            "rabbit": {
                "safe": True,
                "dosage": "Not well established",
                "dosage_ja": "十分に確立されていない",
                "notes": "Very limited data",
                "notes_ja": "データは非常に限定的",
            },
            "ferret": {
                "safe": True,
                "dosage": "Not well established",
                "dosage_ja": "十分に確立されていない",
                "notes": "Limited data",
                "notes_ja": "データ限定的",
            },
            "bird": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Not studied",
                "notes_ja": "未研究",
            },
        },
        "side_effects": ["diarrhea", "anorexia", "bone marrow suppression", "increased infection risk"],
        "side_effects_ja": ["下痢", "食欲不振", "骨髄抑制", "感染リスク増加"],
        "contraindications": "Pregnancy. Active severe infection.",
        "contraindications_ja": "妊娠中。重度活動性感染。",
        "drug_interactions": [{"drug": "antacids", "effect": "Decreased absorption", "effect_ja": "吸収低下"}],
    },
    {
        "id": "cetirizine",
        "name": "Cetirizine",
        "name_ja": "セチリジン",
        "category": "antihistamines",
        "mechanism": "Second-generation H1 antihistamine; less sedating than first-generation antihistamines.",
        "mechanism_ja": "第二世代H1抗ヒスタミン薬。第一世代より鎮静作用が少ない。",
        "routes": ["PO"],
        "routes_ja": ["経口"],
        "formulations": ["Tablets", "Oral solution"],
        "formulations_ja": ["錠剤", "経口液"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "1-2 mg/kg PO q12-24h",
                "dosage_ja": "1-2 mg/kg 経口 12-24時間毎",
                "notes": "Less sedating than diphenhydramine; for allergic dermatitis, atopy",
                "notes_ja": "ジフェンヒドラミンより鎮静が少ない。アレルギー性皮膚炎、アトピーに",
            },
            "cat": {
                "safe": True,
                "dosage": "5 mg/cat PO q12-24h (1/2 of 10mg tablet)",
                "dosage_ja": "5 mg/匹 経口 12-24時間毎",
                "notes": "Commonly used for feline allergic skin disease",
                "notes_ja": "猫のアレルギー性皮膚疾患に一般的に使用",
            },
            "horse": {
                "safe": True,
                "dosage": "0.2-0.4 mg/kg PO q12h",
                "dosage_ja": "0.2-0.4 mg/kg 経口 12時間毎",
                "notes": "For urticaria, insect bite hypersensitivity",
                "notes_ja": "蕁麻疹、昆虫刺咬過敏症に",
            },
            "rabbit": {
                "safe": True,
                "dosage": "0.5-1 mg/kg PO q12-24h",
                "dosage_ja": "0.5-1 mg/kg 経口 12-24時間毎",
                "notes": "For allergic conditions",
                "notes_ja": "アレルギー性疾患に",
            },
            "guinea_pig": {
                "safe": True,
                "dosage": "0.5 mg/kg PO q12h",
                "dosage_ja": "0.5 mg/kg 経口 12時間毎",
                "notes": "Safe antihistamine",
                "notes_ja": "安全な抗ヒスタミン薬",
            },
            "ferret": {
                "safe": True,
                "dosage": "0.5-1 mg/kg PO q12h",
                "dosage_ja": "0.5-1 mg/kg 経口 12時間毎",
                "notes": "For allergic conditions",
                "notes_ja": "アレルギー性疾患に",
            },
        },
        "side_effects": ["mild sedation", "dry mouth", "GI upset"],
        "side_effects_ja": ["軽度の鎮静", "口渇", "消化器症状"],
        "contraindications": "Severe hepatic disease (dose adjust). Renal impairment (dose adjust).",
        "contraindications_ja": "重度肝疾患（用量調整）。腎障害（用量調整）。",
        "drug_interactions": [],
    },
    {
        "id": "cyproheptadine",
        "name": "Cyproheptadine",
        "name_ja": "シプロヘプタジン",
        "category": "antihistamines",
        "mechanism": "First-generation antihistamine with anti-serotonin properties. Appetite stimulant.",
        "mechanism_ja": "抗セロトニン作用を持つ第一世代抗ヒスタミン薬。食欲刺激薬。",
        "routes": ["PO"],
        "routes_ja": ["経口"],
        "formulations": ["Tablets", "Oral syrup"],
        "formulations_ja": ["錠剤", "経口シロップ"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "1.1 mg/kg PO q8-12h",
                "dosage_ja": "1.1 mg/kg 経口 8-12時間毎",
                "notes": "Antihistamine and serotonin syndrome antidote",
                "notes_ja": "抗ヒスタミン薬およびセロトニン症候群の解毒薬",
            },
            "cat": {
                "safe": True,
                "dosage": "1-4 mg/cat PO q12h",
                "dosage_ja": "1-4 mg/匹 経口 12時間毎",
                "notes": "Classic appetite stimulant for cats; for serotonin syndrome, feline asthma adjunct",
                "notes_ja": "猫の古典的食欲刺激薬。セロトニン症候群、猫喘息の補助治療に",
            },
            "horse": {
                "safe": True,
                "dosage": "0.25-0.5 mg/kg PO q8-12h",
                "dosage_ja": "0.25-0.5 mg/kg 経口 8-12時間毎",
                "notes": "For heaves/RAO adjunct; appetite stimulant",
                "notes_ja": "鼻膿漏/RAOの補助。食欲刺激薬",
            },
            "rabbit": {
                "safe": True,
                "dosage": "1-2 mg/kg PO q12h",
                "dosage_ja": "1-2 mg/kg 経口 12時間毎",
                "notes": "Appetite stimulant for inappetent rabbits",
                "notes_ja": "食欲不振ウサギの食欲刺激薬",
            },
            "bird": {
                "safe": True,
                "dosage": "2 mg/kg PO q12h",
                "dosage_ja": "2 mg/kg 経口 12時間毎",
                "notes": "Appetite stimulant for birds",
                "notes_ja": "鳥類の食欲刺激薬",
            },
            "ferret": {
                "safe": True,
                "dosage": "2 mg/ferret PO q12h",
                "dosage_ja": "2 mg/匹 経口 12時間毎",
                "notes": "Appetite stimulant",
                "notes_ja": "食欲刺激薬",
            },
        },
        "side_effects": ["sedation", "increased appetite", "weight gain", "anticholinergic effects"],
        "side_effects_ja": ["鎮静", "食欲増進", "体重増加", "抗コリン作用"],
        "contraindications": "Glaucoma. Urinary retention. GI obstruction.",
        "contraindications_ja": "緑内障。尿閉。消化管閉塞。",
        "drug_interactions": [
            {
                "drug": "SSRIs",
                "effect": "Antagonizes serotonin effects (therapeutic in serotonin syndrome)",
                "effect_ja": "セロトニン作用を拮抗（セロトニン症候群では治療的）",
            }
        ],
    },
    {
        "id": "vitamin_k1",
        "name": "Vitamin K1 (Phytonadione)",
        "name_ja": "ビタミンK1（フィトナジオン）",
        "category": "supplements",
        "mechanism": "Fat-soluble vitamin essential for synthesis of clotting factors II, VII, IX, X. Antidote for anticoagulant rodenticides.",
        "mechanism_ja": "凝固因子II、VII、IX、Xの合成に必須の脂溶性ビタミン。抗凝固性殺鼠剤の解毒薬。",
        "routes": ["PO", "SC", "IM"],
        "routes_ja": ["経口", "皮下", "筋肉内"],
        "formulations": ["Tablets", "Injectable solution", "Capsules"],
        "formulations_ja": ["錠剤", "注射液", "カプセル"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "2.5-5 mg/kg PO q12h (rodenticide); maintenance: 1-2.5 mg/kg PO q12h",
                "dosage_ja": "2.5-5 mg/kg 経口 12時間毎（殺鼠剤中毒）; 維持: 1-2.5 mg/kg 経口 12時間毎",
                "notes": "Give with fatty meal for absorption; treat 4-6 weeks for 2nd-gen rodenticides",
                "notes_ja": "吸収のため脂肪食と投与。第2世代殺鼠剤では4-6週間治療",
            },
            "cat": {
                "safe": True,
                "dosage": "2.5-5 mg/kg PO/SC q12h",
                "dosage_ja": "2.5-5 mg/kg 経口/皮下 12時間毎",
                "notes": "Same protocol as dogs; less common rodenticide exposure",
                "notes_ja": "犬と同じプロトコル。殺鼠剤暴露は少ない",
            },
            "horse": {
                "safe": True,
                "dosage": "0.5-2.5 mg/kg SC/IM q12h",
                "dosage_ja": "0.5-2.5 mg/kg 皮下/筋注 12時間毎",
                "notes": "For warfarin/rodenticide toxicity, liver disease coagulopathy",
                "notes_ja": "ワルファリン/殺鼠剤中毒、肝疾患性凝固障害に",
            },
            "rabbit": {
                "safe": True,
                "dosage": "1-10 mg/kg SC/IM q12-24h",
                "dosage_ja": "1-10 mg/kg 皮下/筋注 12-24時間毎",
                "notes": "For rodenticide exposure",
                "notes_ja": "殺鼠剤暴露に",
            },
            "bird": {
                "safe": True,
                "dosage": "2.5-5 mg/kg IM q12-24h",
                "dosage_ja": "2.5-5 mg/kg 筋注 12-24時間毎",
                "notes": "For coagulopathy",
                "notes_ja": "凝固障害に",
            },
            "ferret": {
                "safe": True,
                "dosage": "1-2.5 mg/kg PO/SC q12h",
                "dosage_ja": "1-2.5 mg/kg 経口/皮下 12時間毎",
                "notes": "For rodenticide toxicity",
                "notes_ja": "殺鼠剤中毒に",
            },
        },
        "side_effects": ["anaphylaxis (IV - AVOID IV route)", "pain at injection site", "hematoma"],
        "side_effects_ja": ["アナフィラキシー(静注 - 静注は避ける)", "注射部位の疼痛", "血腫"],
        "contraindications": "NEVER give IV (anaphylaxis risk). Hepatic failure (won't work without functional liver).",
        "contraindications_ja": "【絶対禁忌】静注不可（アナフィラキシーリスク）。肝不全（機能的な肝臓がなければ無効）。",
        "drug_interactions": [
            {
                "drug": "anticoagulants",
                "effect": "Antagonizes anticoagulant effects (therapeutic)",
                "effect_ja": "抗凝固作用を拮抗（治療的）",
            }
        ],
    },
    {
        "id": "ursodiol",
        "name": "Ursodiol (UDCA)",
        "name_ja": "ウルソデオキシコール酸",
        "category": "hepatoprotectants",
        "mechanism": "Hydrophilic bile acid; displaces toxic hydrophobic bile acids, provides hepatoprotection and choleresis.",
        "mechanism_ja": "親水性胆汁酸。毒性のある疎水性胆汁酸を置換し、肝保護作用と利胆作用を提供。",
        "routes": ["PO"],
        "routes_ja": ["経口"],
        "formulations": ["Tablets", "Capsules"],
        "formulations_ja": ["錠剤", "カプセル"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "10-15 mg/kg PO q24h",
                "dosage_ja": "10-15 mg/kg 経口 24時間毎",
                "notes": "For cholestatic liver disease, gallbladder mucocele, chronic hepatitis",
                "notes_ja": "胆汁うっ滞性肝疾患、胆嚢粘液嚢腫、慢性肝炎に",
            },
            "cat": {
                "safe": True,
                "dosage": "10-15 mg/kg PO q24h",
                "dosage_ja": "10-15 mg/kg 経口 24時間毎",
                "notes": "For cholangitis, hepatic lipidosis adjunct, cholestasis",
                "notes_ja": "胆管炎、肝リピドーシスの補助治療、胆汁うっ滞に",
            },
            "horse": {
                "safe": True,
                "dosage": "10-15 mg/kg PO q24h",
                "dosage_ja": "10-15 mg/kg 経口 24時間毎",
                "notes": "For cholestatic liver conditions",
                "notes_ja": "胆汁うっ滞性肝疾患に",
            },
            "rabbit": {
                "safe": True,
                "dosage": "10-15 mg/kg PO q24h",
                "dosage_ja": "10-15 mg/kg 経口 24時間毎",
                "notes": "For hepatic disease",
                "notes_ja": "肝疾患に",
            },
            "ferret": {
                "safe": True,
                "dosage": "10-15 mg/kg PO q24h",
                "dosage_ja": "10-15 mg/kg 経口 24時間毎",
                "notes": "For liver disease",
                "notes_ja": "肝疾患に",
            },
            "bird": {
                "safe": True,
                "dosage": "10-15 mg/kg PO q12-24h",
                "dosage_ja": "10-15 mg/kg 経口 12-24時間毎",
                "notes": "For hepatic disease in birds",
                "notes_ja": "鳥類の肝疾患に",
            },
        },
        "side_effects": ["diarrhea (rare)", "no significant side effects at therapeutic doses"],
        "side_effects_ja": ["下痢(まれ)", "治療用量では有意な副作用なし"],
        "contraindications": "Complete biliary obstruction (bile duct).",
        "contraindications_ja": "完全胆道閉塞（胆管）。",
        "drug_interactions": [{"drug": "antacids", "effect": "Decreased absorption", "effect_ja": "吸収低下"}],
    },
    {
        "id": "n_acetylcysteine",
        "name": "N-Acetylcysteine (NAC)",
        "name_ja": "N-アセチルシステイン",
        "category": "hepatoprotectants",
        "mechanism": "Glutathione precursor; replenishes hepatic glutathione stores. Acetaminophen antidote. Also mucolytic.",
        "mechanism_ja": "グルタチオン前駆体。肝臓のグルタチオン貯蔵を補充する。アセトアミノフェン解毒薬。粘液溶解薬でもある。",
        "routes": ["PO", "IV"],
        "routes_ja": ["経口", "静脈内"],
        "formulations": ["Oral solution", "Injectable solution"],
        "formulations_ja": ["経口液", "注射液"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "140 mg/kg IV/PO loading, then 70 mg/kg q6h x 7 doses (acetaminophen toxicity)",
                "dosage_ja": "140 mg/kg 静注/経口 初回、その後70 mg/kg 6時間毎x7回（アセトアミノフェン中毒）",
                "notes": "Critical antidote for acetaminophen toxicity; also hepatoprotectant",
                "notes_ja": "アセトアミノフェン中毒の重要な解毒薬。肝保護薬としても",
            },
            "cat": {
                "safe": True,
                "dosage": "140 mg/kg IV loading, then 70 mg/kg IV q6h x 12 doses minimum",
                "dosage_ja": "140 mg/kg 静注初回、その後70 mg/kg 静注6時間毎x最低12回",
                "notes": "CRITICAL for feline acetaminophen toxicity - cats form toxic metabolite at low doses",
                "notes_ja": "猫のアセトアミノフェン中毒に【必須】- 猫は低用量で毒性代謝物を形成",
            },
            "horse": {
                "safe": True,
                "dosage": "140 mg/kg PO loading, then 70 mg/kg q6h",
                "dosage_ja": "140 mg/kg 経口初回、その後70 mg/kg 6時間毎",
                "notes": "For hepatotoxicity from various causes",
                "notes_ja": "各種原因による肝毒性に",
            },
            "rabbit": {
                "safe": True,
                "dosage": "140 mg/kg IV/PO loading",
                "dosage_ja": "140 mg/kg 静注/経口初回",
                "notes": "For hepatoprotection",
                "notes_ja": "肝保護に",
            },
            "ferret": {
                "safe": True,
                "dosage": "Same protocol as cats",
                "dosage_ja": "猫と同じプロトコル",
                "notes": "For toxicity cases",
                "notes_ja": "中毒症例に",
            },
            "bird": {
                "safe": True,
                "dosage": "100-200 mg/kg PO q8h",
                "dosage_ja": "100-200 mg/kg 経口 8時間毎",
                "notes": "Hepatoprotectant; also mucolytic for respiratory",
                "notes_ja": "肝保護薬。呼吸器の粘液溶解薬としても",
            },
        },
        "side_effects": ["nausea/vomiting (oral)", "anaphylactoid reactions (IV - rare)", "bronchospasm (nebulized)"],
        "side_effects_ja": ["悪心/嘔吐(経口)", "アナフィラキシー様反応(静注 - まれ)", "気管支痙攣(ネブライザー)"],
        "contraindications": "None absolute for toxicity treatment.",
        "contraindications_ja": "中毒治療においては絶対的禁忌なし。",
        "drug_interactions": [],
    },
    {
        "id": "cyclosporine_ophthalmic",
        "name": "Cyclosporine Ophthalmic",
        "name_ja": "シクロスポリン点眼薬",
        "category": "ophthalmic",
        "mechanism": "Calcineurin inhibitor (topical); stimulates tear production by inhibiting T-cell activation in lacrimal gland.",
        "mechanism_ja": "カルシニューリン阻害薬（外用）。涙腺でT細胞活性化を阻害し涙液産生を刺激する。",
        "routes": ["ophthalmic"],
        "routes_ja": ["点眼"],
        "formulations": ["Ophthalmic ointment 0.2% (Optimmune)", "Compounded drops 1-2%"],
        "formulations_ja": ["点眼軟膏0.2%（オプティミューン）", "院内調製点眼液1-2%"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "1/4 inch strip q12h (Optimmune) or 1 drop q8-12h (compounded)",
                "dosage_ja": "1/4インチ 12時間毎（オプティミューン）または1滴 8-12時間毎（院内調製）",
                "notes": "Drug of choice for KCS (dry eye); also for chronic superficial keratitis (pannus)",
                "notes_ja": "KCS（ドライアイ）の第一選択薬。慢性表在性角膜炎（パンヌス）にも",
            },
            "cat": {
                "safe": True,
                "dosage": "Same as dog",
                "dosage_ja": "犬と同様",
                "notes": "For eosinophilic keratitis; less common KCS in cats",
                "notes_ja": "好酸球性角膜炎に。猫のKCSはまれ",
            },
            "horse": {
                "safe": True,
                "dosage": "Topical q8-12h",
                "dosage_ja": "8-12時間毎に点眼",
                "notes": "For immune-mediated keratitis",
                "notes_ja": "免疫介在性角膜炎に",
            },
            "rabbit": {
                "safe": True,
                "dosage": "Topical q12h",
                "dosage_ja": "12時間毎に点眼",
                "notes": "For dry eye",
                "notes_ja": "ドライアイに",
            },
            "guinea_pig": {
                "safe": True,
                "dosage": "Topical q12h",
                "dosage_ja": "12時間毎に点眼",
                "notes": "For ocular surface disease",
                "notes_ja": "眼表面疾患に",
            },
            "bird": {
                "safe": True,
                "dosage": "Topical q12h",
                "dosage_ja": "12時間毎に点眼",
                "notes": "For dry eye in birds",
                "notes_ja": "鳥類のドライアイに",
            },
        },
        "side_effects": ["transient ocular irritation", "mild blepharospasm"],
        "side_effects_ja": ["一過性の眼刺激", "軽度眼瞼痙攣"],
        "contraindications": "Active ocular fungal or viral infection (relative).",
        "contraindications_ja": "活動性の眼真菌または ウイルス感染（相対的）。",
        "drug_interactions": [],
    },
    {
        "id": "dorzolamide",
        "name": "Dorzolamide",
        "name_ja": "ドルゾラミド",
        "category": "ophthalmic",
        "mechanism": "Topical carbonic anhydrase inhibitor; reduces aqueous humor production to lower intraocular pressure.",
        "mechanism_ja": "外用炭酸脱水酵素阻害薬。房水産生を低下させ眼圧を下げる。",
        "routes": ["ophthalmic"],
        "routes_ja": ["点眼"],
        "formulations": ["Ophthalmic solution 2%", "Combination with timolol (Cosopt)"],
        "formulations_ja": ["点眼液2%", "チモロールとの配合剤（コソプト）"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "1 drop q8h (alone) or q12h (with timolol)",
                "dosage_ja": "1滴 8時間毎（単独）または12時間毎（チモロールと併用）",
                "notes": "For glaucoma; often combined with timolol for better IOP control",
                "notes_ja": "緑内障に。より良い眼圧コントロールのためチモロールと併用することが多い",
            },
            "cat": {
                "safe": True,
                "dosage": "1 drop q8-12h",
                "dosage_ja": "1滴 8-12時間毎",
                "notes": "For glaucoma; feline glaucoma often secondary to uveitis",
                "notes_ja": "緑内障に。猫の緑内障は多くの場合ぶどう膜炎に続発",
            },
            "horse": {
                "safe": True,
                "dosage": "1 drop q8-12h",
                "dosage_ja": "1滴 8-12時間毎",
                "notes": "For equine glaucoma",
                "notes_ja": "馬の緑内障に",
            },
            "rabbit": {
                "safe": True,
                "dosage": "1 drop q8-12h",
                "dosage_ja": "1滴 8-12時間毎",
                "notes": "For glaucoma (especially NZW rabbit)",
                "notes_ja": "緑内障に（特にNZWウサギ）",
            },
            "guinea_pig": {
                "safe": True,
                "dosage": "1 drop q8-12h",
                "dosage_ja": "1滴 8-12時間毎",
                "notes": "For glaucoma",
                "notes_ja": "緑内障に",
            },
            "bird": {
                "safe": True,
                "dosage": "1 drop q8-12h",
                "dosage_ja": "1滴 8-12時間毎",
                "notes": "Limited data",
                "notes_ja": "データ限定的",
            },
        },
        "side_effects": ["ocular stinging", "conjunctival hyperemia", "bitter taste"],
        "side_effects_ja": ["眼の刺激感", "結膜充血", "苦味"],
        "contraindications": "Sulfonamide allergy (structurally related).",
        "contraindications_ja": "サルファ剤アレルギー（構造的に関連）。",
        "drug_interactions": [],
    },
    {
        "id": "zonisamide",
        "name": "Zonisamide",
        "name_ja": "ゾニサミド",
        "category": "neurological",
        "mechanism": "Anticonvulsant; blocks sodium and T-type calcium channels, enhances GABA, free radical scavenger.",
        "mechanism_ja": "抗痙攣薬。ナトリウムチャネルとT型カルシウムチャネルを遮断、GABA増強、フリーラジカル捕捉。",
        "routes": ["PO"],
        "routes_ja": ["経口"],
        "formulations": ["Capsules"],
        "formulations_ja": ["カプセル"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "5-10 mg/kg PO q12h",
                "dosage_ja": "5-10 mg/kg 経口 12時間毎",
                "notes": "Alternative/adjunct to phenobarbital; fewer hepatic effects",
                "notes_ja": "フェノバルビタールの代替/補助。肝臓への影響が少ない",
            },
            "cat": {
                "safe": True,
                "dosage": "5-10 mg/kg PO q12-24h",
                "dosage_ja": "5-10 mg/kg 経口 12-24時間毎",
                "notes": "Well tolerated in cats; gaining popularity",
                "notes_ja": "猫で忍容性良好。人気上昇中",
            },
            "horse": {
                "safe": True,
                "dosage": "Not well established",
                "dosage_ja": "十分に確立されていない",
                "notes": "Limited equine data",
                "notes_ja": "馬のデータは限定的",
            },
            "rabbit": {
                "safe": True,
                "dosage": "Not well established",
                "dosage_ja": "十分に確立されていない",
                "notes": "Limited data",
                "notes_ja": "データ限定的",
            },
            "ferret": {
                "safe": True,
                "dosage": "Not well established",
                "dosage_ja": "十分に確立されていない",
                "notes": "Limited data",
                "notes_ja": "データ限定的",
            },
            "bird": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Not studied",
                "notes_ja": "未研究",
            },
        },
        "side_effects": [
            "sedation",
            "ataxia",
            "decreased appetite",
            "vomiting",
            "hepatotoxicity (rare)",
            "renal tubular acidosis",
        ],
        "side_effects_ja": ["鎮静", "運動失調", "食欲低下", "嘔吐", "肝毒性(まれ)", "腎尿細管性アシドーシス"],
        "contraindications": "Severe hepatic or renal disease. Sulfonamide allergy (structurally related).",
        "contraindications_ja": "重度肝・腎疾患。サルファ剤アレルギー（構造的に関連）。",
        "drug_interactions": [
            {
                "drug": "phenobarbital",
                "effect": "Induces zonisamide metabolism - may need higher doses",
                "effect_ja": "ゾニサミド代謝を誘導 - より高用量が必要な場合あり",
            }
        ],
    },
    {
        "id": "potassium_bromide",
        "name": "Potassium Bromide",
        "name_ja": "臭化カリウム",
        "category": "neurological",
        "mechanism": "Anticonvulsant; bromide ions compete with chloride for cellular uptake, hyperpolarizing neurons.",
        "mechanism_ja": "抗痙攣薬。臭化物イオンが塩化物と細胞取り込みを競合し、ニューロンを過分極させる。",
        "routes": ["PO"],
        "routes_ja": ["経口"],
        "formulations": ["Oral solution", "Capsules (compounded)"],
        "formulations_ja": ["経口液", "カプセル（院内調製）"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "20-30 mg/kg PO q24h (40-60 mg/kg if monotherapy)",
                "dosage_ja": "20-30 mg/kg 経口 24時間毎（単独療法: 40-60 mg/kg）",
                "notes": "Long half-life (25 days); takes 3-4 months for steady state. Monitor serum levels (1-3 mg/mL)",
                "notes_ja": "長い半減期(25日)。定常状態まで3-4ヶ月。血中濃度モニタリング(1-3 mg/mL)",
            },
            "cat": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "CONTRAINDICATED - causes severe lower airway disease (eosinophilic bronchitis)",
                "notes_ja": "【禁忌】重度下気道疾患（好酸球性気管支炎）を引き起こす",
            },
            "horse": {
                "safe": True,
                "dosage": "Not commonly used",
                "dosage_ja": "一般的には使用されない",
                "notes": "Very long elimination in horses",
                "notes_ja": "馬では排泄が非常に遅い",
            },
            "rabbit": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Safety not established",
                "notes_ja": "安全性未確立",
            },
            "ferret": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Safety not established",
                "notes_ja": "安全性未確立",
            },
            "bird": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Not recommended",
                "notes_ja": "推奨されない",
            },
        },
        "side_effects": [
            "sedation",
            "polydipsia/polyuria",
            "polyphagia",
            "hind limb weakness",
            "pancreatitis",
            "skin rash",
        ],
        "side_effects_ja": ["鎮静", "多飲多尿", "多食", "後肢衰弱", "膵炎", "皮疹"],
        "contraindications": "Cats (severe respiratory disease). Renal insufficiency. High-chloride diets alter levels.",
        "contraindications_ja": "猫（重度呼吸器疾患）。腎不全。高塩素食で血中濃度変動。",
        "drug_interactions": [
            {
                "drug": "furosemide",
                "effect": "Increases bromide excretion, lowering levels",
                "effect_ja": "臭化物排泄を増加し濃度を低下させる",
            },
            {
                "drug": "chloride-containing fluids",
                "effect": "Competitive excretion - reduces bromide levels",
                "effect_ja": "競合的排泄 - 臭化物濃度を低下させる",
            },
        ],
    },
    {
        "id": "oxytocin",
        "name": "Oxytocin",
        "name_ja": "オキシトシン",
        "category": "hormones",
        "mechanism": "Posterior pituitary hormone; stimulates uterine smooth muscle contraction and milk let-down.",
        "mechanism_ja": "下垂体後葉ホルモン。子宮平滑筋収縮と射乳反射を刺激する。",
        "routes": ["IV", "IM", "SC"],
        "routes_ja": ["静脈内", "筋肉内", "皮下"],
        "formulations": ["Injectable solution"],
        "formulations_ja": ["注射液"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "0.5-5 U/dog IM (dystocia); 0.5-2 U/dog IM (milk letdown)",
                "dosage_ja": "0.5-5 U/匹 筋注（難産）; 0.5-2 U/匹 筋注（射乳）",
                "notes": "Only after confirming cervix is dilated; start low dose",
                "notes_ja": "子宮頸管が開大していることを確認後のみ使用。低用量から開始",
            },
            "cat": {
                "safe": True,
                "dosage": "0.5-3 U/cat IM",
                "dosage_ja": "0.5-3 U/匹 筋注",
                "notes": "For dystocia; confirm no obstruction first",
                "notes_ja": "難産に。先に閉塞がないことを確認",
            },
            "horse": {
                "safe": True,
                "dosage": "5-20 U IV (retained placenta); 2.5-10 U IV (milk letdown)",
                "dosage_ja": "5-20 U 静注（胎盤停滞）; 2.5-10 U 静注（射乳）",
                "notes": "For retained fetal membranes; can cause abdominal cramping",
                "notes_ja": "胎膜停滞に。腹部痙攣を起こす可能性",
            },
            "rabbit": {
                "safe": True,
                "dosage": "0.5-3 U/kg IM/SC",
                "dosage_ja": "0.5-3 U/kg 筋注/皮下",
                "notes": "For dystocia in rabbits",
                "notes_ja": "ウサギの難産に",
            },
            "guinea_pig": {
                "safe": True,
                "dosage": "0.2-3 U/kg SC/IM",
                "dosage_ja": "0.2-3 U/kg 皮下/筋注",
                "notes": "For dystocia; guinea pigs prone to dystocia",
                "notes_ja": "難産に。モルモットは難産になりやすい",
            },
            "bird": {
                "safe": True,
                "dosage": "1-5 U/kg IM",
                "dosage_ja": "1-5 U/kg 筋注",
                "notes": "For egg binding",
                "notes_ja": "卵詰まりに",
            },
        },
        "side_effects": [
            "uterine rupture (if obstruction present)",
            "abdominal pain",
            "water intoxication (high doses)",
        ],
        "side_effects_ja": ["子宮破裂(閉塞がある場合)", "腹痛", "水中毒(高用量)"],
        "contraindications": "Obstructive dystocia. Undilated cervix. Fetal malpresentation.",
        "contraindications_ja": "閉塞性難産。子宮頸管未開大。胎子位置異常。",
        "drug_interactions": [],
    },
    {
        "id": "melatonin",
        "name": "Melatonin",
        "name_ja": "メラトニン",
        "category": "hormones",
        "mechanism": "Pineal hormone; regulates circadian rhythm. Anti-gonadotropic effects in ferrets.",
        "mechanism_ja": "松果体ホルモン。概日リズムを調節する。フェレットで抗生殖腺刺激ホルモン作用。",
        "routes": ["PO", "implant"],
        "routes_ja": ["経口", "インプラント"],
        "formulations": ["Tablets", "Implant"],
        "formulations_ja": ["錠剤", "インプラント"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "3-6 mg/dog PO q12h",
                "dosage_ja": "3-6 mg/匹 経口 12時間毎",
                "notes": "For alopecia X, anxiety, Cushing's disease adjunct, noise phobia",
                "notes_ja": "X脱毛症、不安、クッシング病補助、騒音恐怖症に",
            },
            "cat": {
                "safe": True,
                "dosage": "1.5-3 mg/cat PO q12h",
                "dosage_ja": "1.5-3 mg/匹 経口 12時間毎",
                "notes": "For psychogenic alopecia, seasonal flank alopecia",
                "notes_ja": "心因性脱毛症、季節性側腹部脱毛症に",
            },
            "horse": {
                "safe": True,
                "dosage": "Not commonly used",
                "dosage_ja": "一般的には使用されない",
                "notes": "Limited equine data",
                "notes_ja": "馬のデータは限定的",
            },
            "ferret": {
                "safe": True,
                "dosage": "0.5-1 mg/ferret PO q24h or implant",
                "dosage_ja": "0.5-1 mg/匹 経口 24時間毎またはインプラント",
                "notes": "For adrenal disease; delays return of clinical signs; implant preferred",
                "notes_ja": "副腎疾患に。臨床症状の再発を遅延。インプラントが好ましい",
            },
            "rabbit": {
                "safe": True,
                "dosage": "0.5-1 mg/kg PO q24h",
                "dosage_ja": "0.5-1 mg/kg 経口 24時間毎",
                "notes": "For anxiety/stress",
                "notes_ja": "不安/ストレスに",
            },
            "bird": {
                "safe": True,
                "dosage": "Not well established",
                "dosage_ja": "十分に確立されていない",
                "notes": "Limited data",
                "notes_ja": "データ限定的",
            },
        },
        "side_effects": ["sedation", "weight gain", "altered reproductive cycles"],
        "side_effects_ja": ["鎮静", "体重増加", "生殖周期の変化"],
        "contraindications": "Breeding animals (alters reproductive hormones).",
        "contraindications_ja": "繁殖用動物（生殖ホルモンを変化させる）。",
        "drug_interactions": [],
    },
    {
        "id": "deslorelin",
        "name": "Deslorelin",
        "name_ja": "デスロレリン",
        "category": "hormones",
        "mechanism": "GnRH agonist; initially stimulates then suppresses gonadotropin release (chemical castration).",
        "mechanism_ja": "GnRH作動薬。初期に性腺刺激ホルモン放出を刺激し、その後抑制する（化学的去勢）。",
        "routes": ["implant"],
        "routes_ja": ["インプラント"],
        "formulations": ["Subcutaneous implant (Suprelorin)"],
        "formulations_ja": ["皮下インプラント（スプレロリン）"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "4.7 mg or 9.4 mg implant SC",
                "dosage_ja": "4.7 mg または 9.4 mg インプラント皮下",
                "notes": "Chemical castration; duration 6-12+ months depending on dose",
                "notes_ja": "化学的去勢。用量により6-12ヶ月以上持続",
            },
            "cat": {
                "safe": True,
                "dosage": "4.7 mg implant SC",
                "dosage_ja": "4.7 mg インプラント皮下",
                "notes": "For chemical sterilization",
                "notes_ja": "化学的不妊化に",
            },
            "horse": {
                "safe": True,
                "dosage": "Not well established",
                "dosage_ja": "十分に確立されていない",
                "notes": "Research use for stallion management",
                "notes_ja": "種牡馬管理の研究用途",
            },
            "ferret": {
                "safe": True,
                "dosage": "4.7 mg implant SC",
                "dosage_ja": "4.7 mg インプラント皮下",
                "notes": "Drug of choice for ferret adrenal disease; suppresses sex steroid production",
                "notes_ja": "フェレット副腎疾患の第一選択薬。性ステロイド産生を抑制",
            },
            "rabbit": {
                "safe": True,
                "dosage": "4.7 mg implant SC",
                "dosage_ja": "4.7 mg インプラント皮下",
                "notes": "Chemical castration alternative to surgery",
                "notes_ja": "外科手術の代替としての化学的去勢",
            },
            "bird": {
                "safe": True,
                "dosage": "4.7 mg implant SC/IM",
                "dosage_ja": "4.7 mg インプラント皮下/筋注",
                "notes": "For chronic egg-laying; very effective",
                "notes_ja": "慢性産卵に。非常に有効",
            },
        },
        "side_effects": ["initial flare of reproductive activity (1-2 weeks)", "weight gain", "behavior changes"],
        "side_effects_ja": ["初期の生殖活動フレア(1-2週間)", "体重増加", "行動変化"],
        "contraindications": "Pregnant animals. Initial flare may worsen prostatic disease temporarily.",
        "contraindications_ja": "妊娠動物。初期フレアにより一時的に前立腺疾患が悪化する可能性。",
        "drug_interactions": [],
    },
    {
        "id": "pergolide",
        "name": "Pergolide",
        "name_ja": "ペルゴリド",
        "category": "endocrine",
        "mechanism": "Dopamine receptor agonist (D1 and D2); reduces ACTH secretion from pars intermedia. For equine PPID (Cushing's).",
        "mechanism_ja": "ドパミン受容体作動薬(D1およびD2)。中間部からのACTH分泌を減少。馬のPPID(クッシング病)に。",
        "routes": ["PO"],
        "routes_ja": ["経口"],
        "formulations": ["Tablets (Prascend)"],
        "formulations_ja": ["錠剤（プラスケンド）"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Not commonly used (trilostane preferred)",
                "dosage_ja": "一般的には使用されない（トリロスタンが好まれる）",
                "notes": "Was used for pituitary-dependent Cushing's; trilostane replaced it",
                "notes_ja": "下垂体依存性クッシング病に使用されていた。トリロスタンに置き換わった",
            },
            "cat": {
                "safe": True,
                "dosage": "Not commonly used",
                "dosage_ja": "一般的には使用されない",
                "notes": "Limited data",
                "notes_ja": "データ限定的",
            },
            "horse": {
                "safe": True,
                "dosage": "0.002 mg/kg PO q24h (start), titrate up",
                "dosage_ja": "0.002 mg/kg 経口 24時間毎（開始）、漸増",
                "notes": "Drug of choice for equine PPID/Cushing's (Prascend); FDA-approved for horses",
                "notes_ja": "馬のPPID/クッシング病の第一選択薬（プラスケンド）。馬にFDA承認",
            },
            "rabbit": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Not studied",
                "notes_ja": "未研究",
            },
            "ferret": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Not recommended",
                "notes_ja": "推奨されない",
            },
            "bird": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Not studied",
                "notes_ja": "未研究",
            },
        },
        "side_effects": ["decreased appetite (initial)", "diarrhea", "lethargy", "colic (horses)"],
        "side_effects_ja": ["食欲低下(初期)", "下痢", "元気消失", "疝痛(馬)"],
        "contraindications": "Pregnancy. Caution in horses with history of laminitis (monitor during initial treatment).",
        "contraindications_ja": "妊娠中。蹄葉炎歴のある馬では注意（初期治療中モニタリング）。",
        "drug_interactions": [
            {"drug": "dopamine antagonists", "effect": "May reduce efficacy", "effect_ja": "有効性を低下させる可能性"}
        ],
    },
    {
        "id": "glipizide",
        "name": "Glipizide",
        "name_ja": "グリピジド",
        "category": "endocrine",
        "mechanism": "Sulfonylurea; stimulates pancreatic beta-cell insulin secretion. For type 2 diabetes.",
        "mechanism_ja": "スルホニル尿素薬。膵β細胞のインスリン分泌を刺激する。2型糖尿病に。",
        "routes": ["PO"],
        "routes_ja": ["経口"],
        "formulations": ["Tablets"],
        "formulations_ja": ["錠剤"],
        "species_info": {
            "dog": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Dogs have type 1 diabetes - insulin is required, not oral hypoglycemics",
                "notes_ja": "犬は1型糖尿病 - インスリンが必要。経口血糖降下薬ではない",
            },
            "cat": {
                "safe": True,
                "dosage": "2.5-5 mg/cat PO q12h",
                "dosage_ja": "2.5-5 mg/匹 経口 12時間毎",
                "notes": "For newly diagnosed feline type 2 diabetes; many cats achieve remission; insulin preferred by most internists",
                "notes_ja": "新規診断の猫2型糖尿病に。多くの猫で寛解達成。多くの内科医はインスリンを好む",
            },
            "horse": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Not appropriate for equine metabolic syndrome",
                "notes_ja": "馬のメタボリックシンドロームには不適切",
            },
            "rabbit": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Not studied",
                "notes_ja": "未研究",
            },
            "ferret": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Ferrets have insulinoma not diabetes type 2",
                "notes_ja": "フェレットはインスリノーマであり2型糖尿病ではない",
            },
            "bird": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Not studied",
                "notes_ja": "未研究",
            },
        },
        "side_effects": ["hypoglycemia", "vomiting", "hepatotoxicity", "icterus"],
        "side_effects_ja": ["低血糖", "嘔吐", "肝毒性", "黄疸"],
        "contraindications": "Dogs (type 1 DM). Hepatic disease. Already on insulin.",
        "contraindications_ja": "犬（1型糖尿病）。肝疾患。既にインスリン使用中。",
        "drug_interactions": [{"drug": "insulin", "effect": "Additive hypoglycemia", "effect_ja": "低血糖の加算"}],
    },
    {
        "id": "vincristine",
        "name": "Vincristine",
        "name_ja": "ビンクリスチン",
        "category": "antineoplastics",
        "mechanism": "Vinca alkaloid; binds tubulin, inhibiting microtubule assembly and arresting cell division in metaphase.",
        "mechanism_ja": "ビンカアルカロイド。チューブリンに結合し微小管の組み立てを阻害、中期で細胞分裂を停止。",
        "routes": ["IV"],
        "routes_ja": ["静脈内"],
        "formulations": ["Injectable solution"],
        "formulations_ja": ["注射液"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "0.5-0.7 mg/m2 IV once weekly",
                "dosage_ja": "0.5-0.7 mg/m2 静注 週1回",
                "notes": "Part of CHOP lymphoma protocol; also for IMTP (stimulates platelet release)",
                "notes_ja": "CHOPリンパ腫プロトコルの一部。IMTPにも（血小板放出を刺激）",
            },
            "cat": {
                "safe": True,
                "dosage": "0.5 mg/m2 IV once weekly",
                "dosage_ja": "0.5 mg/m2 静注 週1回",
                "notes": "For feline lymphoma protocols",
                "notes_ja": "猫リンパ腫プロトコルに",
            },
            "horse": {
                "safe": True,
                "dosage": "Not commonly used",
                "dosage_ja": "一般的には使用されない",
                "notes": "Limited equine oncology data",
                "notes_ja": "馬の腫瘍学データは限定的",
            },
            "ferret": {
                "safe": True,
                "dosage": "0.12 mg/kg IV weekly",
                "dosage_ja": "0.12 mg/kg 静注 週1回",
                "notes": "For ferret lymphoma",
                "notes_ja": "フェレットリンパ腫に",
            },
            "rabbit": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Limited data; risk-benefit unfavorable",
                "notes_ja": "データ限定的。リスク・ベネフィットが不利",
            },
            "bird": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Not recommended",
                "notes_ja": "推奨されない",
            },
        },
        "side_effects": [
            "severe perivascular tissue necrosis if extravasated",
            "GI upset",
            "peripheral neuropathy",
            "constipation/ileus",
            "myelosuppression (mild)",
        ],
        "side_effects_ja": [
            "血管外漏出で重度組織壊死",
            "消化器症状",
            "末梢神経障害",
            "便秘/イレウス",
            "骨髄抑制(軽度)",
        ],
        "contraindications": "NEVER give intrathecally (fatal). Severe peripheral neuropathy. Verify secure IV catheter.",
        "contraindications_ja": "【絶対禁忌】髄腔内投与不可（致死的）。重度末梢神経障害。安全な静脈カテーテルを確認。",
        "drug_interactions": [
            {
                "drug": "L-asparaginase",
                "effect": "Give vincristine 12-24h before L-asparaginase to reduce hepatotoxicity",
                "effect_ja": "肝毒性軽減のためL-アスパラギナーゼの12-24時間前にビンクリスチンを投与",
            }
        ],
    },
    {
        "id": "doxorubicin",
        "name": "Doxorubicin",
        "name_ja": "ドキソルビシン",
        "category": "antineoplastics",
        "mechanism": "Anthracycline; intercalates DNA, inhibits topoisomerase II, generates free radicals.",
        "mechanism_ja": "アントラサイクリン系。DNAに挿入し、トポイソメラーゼIIを阻害、フリーラジカルを産生。",
        "routes": ["IV"],
        "routes_ja": ["静脈内"],
        "formulations": ["Injectable solution"],
        "formulations_ja": ["注射液"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "30 mg/m2 IV q21 days (max cumulative: 180-240 mg/m2)",
                "dosage_ja": "30 mg/m2 静注 21日毎（最大累積: 180-240 mg/m2）",
                "notes": "Key drug in CHOP lymphoma protocol; cumulative cardiotoxicity; monitor echo",
                "notes_ja": "CHOPリンパ腫プロトコルの主要薬。累積性心毒性。エコーモニタリング",
            },
            "cat": {
                "safe": True,
                "dosage": "1 mg/kg IV q21 days (max cumulative: 6 doses)",
                "dosage_ja": "1 mg/kg 静注 21日毎（最大累積: 6回）",
                "notes": "Lower doses in cats; nephrotoxic in cats (unlike dogs)",
                "notes_ja": "猫では低用量。猫では腎毒性あり（犬と異なる）",
            },
            "horse": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Not used in equine oncology",
                "notes_ja": "馬の腫瘍学では使用されない",
            },
            "ferret": {
                "safe": True,
                "dosage": "1 mg/kg IV q21 days",
                "dosage_ja": "1 mg/kg 静注 21日毎",
                "notes": "For ferret lymphoma; similar to cat dosing",
                "notes_ja": "フェレットリンパ腫に。猫の用量と同様",
            },
            "rabbit": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Not recommended",
                "notes_ja": "推奨されない",
            },
            "bird": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Not studied",
                "notes_ja": "未研究",
            },
        },
        "side_effects": [
            "cumulative dose-dependent cardiotoxicity",
            "myelosuppression (nadir 7-10 days)",
            "severe tissue necrosis if extravasated",
            "anaphylaxis",
            "GI toxicity",
            "alopecia",
        ],
        "side_effects_ja": [
            "累積用量依存性心毒性",
            "骨髄抑制(最低値7-10日目)",
            "血管外漏出で重度組織壊死",
            "アナフィラキシー",
            "消化管毒性",
            "脱毛",
        ],
        "contraindications": "Pre-existing cardiac disease. Prior cumulative dose limit reached. Myelosuppression.",
        "contraindications_ja": "既存の心疾患。累積用量上限に達した場合。骨髄抑制。",
        "drug_interactions": [
            {"drug": "cyclophosphamide", "effect": "Additive cardiotoxicity", "effect_ja": "心毒性の加算"}
        ],
    },
    {
        "id": "cyclophosphamide",
        "name": "Cyclophosphamide",
        "name_ja": "シクロホスファミド",
        "category": "antineoplastics",
        "mechanism": "Alkylating agent; cross-links DNA strands preventing replication and transcription.",
        "mechanism_ja": "アルキル化薬。DNA鎖を架橋し複製と転写を阻害する。",
        "routes": ["PO", "IV"],
        "routes_ja": ["経口", "静脈内"],
        "formulations": ["Tablets", "Injectable powder"],
        "formulations_ja": ["錠剤", "注射用粉末"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "200-250 mg/m2 IV q21 days; or 50 mg/m2 PO q48h (metronomic)",
                "dosage_ja": "200-250 mg/m2 静注 21日毎; または50 mg/m2 経口 48時間毎（メトロノミック）",
                "notes": "CHOP protocol component; also for IMHA. Sterile hemorrhagic cystitis risk - give with furosemide",
                "notes_ja": "CHOPプロトコル構成薬。IMHAにも。無菌性出血性膀胱炎リスク - フロセミドと投与",
            },
            "cat": {
                "safe": True,
                "dosage": "200-250 mg/m2 IV q21 days; 10 mg/kg PO days 1-4 q3 weeks",
                "dosage_ja": "200-250 mg/m2 静注 21日毎; 10 mg/kg 経口 1-4日目 3週毎",
                "notes": "For lymphoma, IMHA; less hemorrhagic cystitis risk than dogs",
                "notes_ja": "リンパ腫、IMHAに。犬より出血性膀胱炎リスクが低い",
            },
            "horse": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Not used in equine practice",
                "notes_ja": "馬の診療では使用されない",
            },
            "ferret": {
                "safe": True,
                "dosage": "10 mg/kg IV/PO q21 days",
                "dosage_ja": "10 mg/kg 静注/経口 21日毎",
                "notes": "For lymphoma protocols",
                "notes_ja": "リンパ腫プロトコルに",
            },
            "rabbit": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Not recommended",
                "notes_ja": "推奨されない",
            },
            "bird": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Not studied",
                "notes_ja": "未研究",
            },
        },
        "side_effects": [
            "myelosuppression",
            "sterile hemorrhagic cystitis",
            "GI toxicity",
            "alopecia",
            "immunosuppression",
        ],
        "side_effects_ja": ["骨髄抑制", "無菌性出血性膀胱炎", "消化管毒性", "脱毛", "免疫抑制"],
        "contraindications": "Active urinary tract infection. Bone marrow suppression. Pregnancy.",
        "contraindications_ja": "活動性尿路感染症。骨髄抑制。妊娠中。",
        "drug_interactions": [
            {"drug": "allopurinol", "effect": "Increased myelosuppression", "effect_ja": "骨髄抑制増加"}
        ],
    },
    {
        "id": "chlorhexidine",
        "name": "Chlorhexidine",
        "name_ja": "クロルヘキシジン",
        "category": "antiseptics",
        "mechanism": "Biguanide antiseptic; disrupts cell membranes. Broad spectrum against bacteria, some fungi and viruses.",
        "mechanism_ja": "ビグアニド系消毒薬。細胞膜を破壊する。細菌、一部の真菌・ウイルスに広域スペクトル。",
        "routes": ["topical"],
        "routes_ja": ["外用"],
        "formulations": ["Solution 2-4%", "Scrub", "Shampoo", "Oral rinse 0.12%", "Ear flush"],
        "formulations_ja": ["液2-4%", "スクラブ", "シャンプー", "口腔リンス0.12%", "耳洗浄液"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "2% solution for surgical prep; 0.5-2% for wound lavage; shampoo q3-7d",
                "dosage_ja": "2%液で手術部位消毒; 0.5-2%で創傷洗浄; シャンプー3-7日毎",
                "notes": "Gold standard surgical antiseptic; excellent residual activity",
                "notes_ja": "ゴールドスタンダードの外科用消毒薬。優れた残留活性",
            },
            "cat": {
                "safe": True,
                "dosage": "Same as dog; diluted solutions preferred",
                "dosage_ja": "犬と同様。希釈液が好ましい",
                "notes": "Well tolerated topically; avoid ingestion",
                "notes_ja": "外用として忍容性良好。摂取を避ける",
            },
            "horse": {
                "safe": True,
                "dosage": "2-4% for surgical prep; diluted for wound care",
                "dosage_ja": "2-4%で手術部位消毒; 希釈して創傷ケア",
                "notes": "Standard equine surgical prep",
                "notes_ja": "標準的な馬の手術消毒",
            },
            "rabbit": {
                "safe": True,
                "dosage": "Diluted 0.05% for wound care",
                "dosage_ja": "0.05%に希釈して創傷ケア",
                "notes": "Use diluted; rabbits sensitive to concentrated solutions",
                "notes_ja": "希釈して使用。ウサギは濃厚液に敏感",
            },
            "bird": {
                "safe": True,
                "dosage": "0.5% for wound care",
                "dosage_ja": "0.5%で創傷ケア",
                "notes": "Dilute for avian patients; avoid contact with eyes",
                "notes_ja": "鳥類患者には希釈。眼接触を避ける",
            },
            "reptile": {
                "safe": True,
                "dosage": "0.5-2% for wound care, shell repair",
                "dosage_ja": "0.5-2%で創傷ケア、甲羅修復",
                "notes": "Excellent for shell fractures/injuries in chelonians",
                "notes_ja": "カメ類の甲羅骨折/損傷に優秀",
            },
        },
        "side_effects": [
            "ototoxicity if used in ruptured tympanic membrane",
            "tissue irritation at high concentrations",
            "contact dermatitis",
        ],
        "side_effects_ja": ["鼓膜穿孔に使用で聴覚毒性", "高濃度で組織刺激", "接触性皮膚炎"],
        "contraindications": "NEVER use in ears with ruptured tympanic membrane (ototoxic). Avoid eye contact.",
        "contraindications_ja": "【禁忌】鼓膜穿孔のある耳には使用不可（聴覚毒性）。眼接触を避ける。",
        "drug_interactions": [],
    },
    {
        "id": "ketoconazole_shampoo",
        "name": "Ketoconazole Shampoo",
        "name_ja": "ケトコナゾールシャンプー",
        "category": "dermatological",
        "mechanism": "Topical azole antifungal shampoo; inhibits ergosterol synthesis on skin surface.",
        "mechanism_ja": "外用アゾール系抗真菌シャンプー。皮膚表面のエルゴステロール合成を阻害。",
        "routes": ["topical"],
        "routes_ja": ["外用"],
        "formulations": ["Shampoo 1-2%"],
        "formulations_ja": ["シャンプー1-2%"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Apply, lather 10 min, rinse; 2-3x/week for 2-4 weeks",
                "dosage_ja": "塗布、10分泡立て、すすぐ; 2-3回/週 x 2-4週間",
                "notes": "For Malassezia dermatitis, dermatophytosis",
                "notes_ja": "マラセチア皮膚炎、皮膚糸状菌症に",
            },
            "cat": {
                "safe": True,
                "dosage": "Same as dog",
                "dosage_ja": "犬と同様",
                "notes": "For dermatophytosis (ringworm)",
                "notes_ja": "皮膚糸状菌症（白癬）に",
            },
            "horse": {
                "safe": True,
                "dosage": "Same application",
                "dosage_ja": "同じ適用方法",
                "notes": "For rain rot fungal component, dermatophytosis",
                "notes_ja": "レインロットの真菌成分、皮膚糸状菌症に",
            },
            "rabbit": {
                "safe": True,
                "dosage": "Apply carefully; avoid stress",
                "dosage_ja": "注意深く塗布。ストレスを避ける",
                "notes": "For dermatophytosis",
                "notes_ja": "皮膚糸状菌症に",
            },
            "guinea_pig": {
                "safe": True,
                "dosage": "Careful application",
                "dosage_ja": "注意深く塗布",
                "notes": "For Trichophyton mentagrophytes",
                "notes_ja": "Trichophyton mentagrophytesに",
            },
            "hedgehog": {
                "safe": True,
                "dosage": "Diluted foot bath/soak",
                "dosage_ja": "希釈した足浴/浸漬",
                "notes": "For dermatophytosis - common in hedgehogs",
                "notes_ja": "皮膚糸状菌症に - ハリネズミで一般的",
            },
        },
        "side_effects": ["skin dryness", "irritation", "rare allergic reaction"],
        "side_effects_ja": ["皮膚乾燥", "刺激", "まれなアレルギー反応"],
        "contraindications": "Open wounds (may sting).",
        "contraindications_ja": "開放創（刺激の可能性）。",
        "drug_interactions": [],
    },
    {
        "id": "aluminum_hydroxide",
        "name": "Aluminum Hydroxide",
        "name_ja": "水酸化アルミニウム",
        "category": "urinary",
        "mechanism": "Phosphate binder; binds dietary phosphorus in the GI tract, reducing absorption. For CKD hyperphosphatemia.",
        "mechanism_ja": "リン吸着薬。消化管内で食事中のリンに結合し吸収を低下させる。CKDの高リン血症に。",
        "routes": ["PO"],
        "routes_ja": ["経口"],
        "formulations": ["Oral suspension", "Capsules", "Powder"],
        "formulations_ja": ["経口懸濁液", "カプセル", "粉末"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "30-90 mg/kg PO with meals",
                "dosage_ja": "30-90 mg/kg 経口 食事と共に",
                "notes": "Must be given WITH food to bind phosphorus; for CKD",
                "notes_ja": "リンに結合するため食事と共に投与が必須。CKDに",
            },
            "cat": {
                "safe": True,
                "dosage": "30-90 mg/kg PO with meals",
                "dosage_ja": "30-90 mg/kg 経口 食事と共に",
                "notes": "Very important in feline CKD management; palatability can be an issue",
                "notes_ja": "猫CKD管理に非常に重要。嗜好性が問題になることも",
            },
            "horse": {
                "safe": True,
                "dosage": "Not commonly needed",
                "dosage_ja": "通常は不要",
                "notes": "CKD uncommon in horses",
                "notes_ja": "馬ではCKDはまれ",
            },
            "rabbit": {
                "safe": True,
                "dosage": "30-90 mg/kg PO with meals",
                "dosage_ja": "30-90 mg/kg 経口 食事と共に",
                "notes": "For renal disease",
                "notes_ja": "腎疾患に",
            },
            "ferret": {
                "safe": True,
                "dosage": "30 mg/kg PO with meals",
                "dosage_ja": "30 mg/kg 経口 食事と共に",
                "notes": "For CKD",
                "notes_ja": "CKDに",
            },
            "bird": {
                "safe": True,
                "dosage": "30-50 mg/kg PO with meals",
                "dosage_ja": "30-50 mg/kg 経口 食事と共に",
                "notes": "For renal disease in birds",
                "notes_ja": "鳥類の腎疾患に",
            },
        },
        "side_effects": [
            "constipation",
            "aluminum accumulation (long-term/renal failure)",
            "phosphorus depletion (overdose)",
        ],
        "side_effects_ja": ["便秘", "アルミニウム蓄積(長期/腎不全)", "リン欠乏(過量投与)"],
        "contraindications": "Not effective if not given with food.",
        "contraindications_ja": "食事と共に投与しないと効果なし。",
        "drug_interactions": [
            {
                "drug": "fluoroquinolones",
                "effect": "Decreased antibiotic absorption - separate by 2h",
                "effect_ja": "抗菌薬吸収低下 - 2時間間隔を空ける",
            },
            {"drug": "tetracyclines", "effect": "Decreased absorption", "effect_ja": "吸収低下"},
        ],
    },
    {
        "id": "methocarbamol",
        "name": "Methocarbamol",
        "name_ja": "メトカルバモール",
        "category": "muscle_relaxants",
        "mechanism": "Centrally-acting muscle relaxant; depresses polysynaptic reflexes in the spinal cord and brainstem.",
        "mechanism_ja": "中枢作用型筋弛緩薬。脊髄と脳幹の多シナプス反射を抑制する。",
        "routes": ["PO", "IV"],
        "routes_ja": ["経口", "静脈内"],
        "formulations": ["Tablets (Robaxin-V)", "Injectable solution"],
        "formulations_ja": ["錠剤（ロバキシン-V）", "注射液"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "20-44 mg/kg PO q8h; IV: 44-220 mg/kg (max 330 mg/kg/day)",
                "dosage_ja": "20-44 mg/kg 経口 8時間毎; 静注: 44-220 mg/kg（最大330 mg/kg/日）",
                "notes": "For muscle spasms, IVDD, strychnine/metaldehyde poisoning, tetanus",
                "notes_ja": "筋痙攣、IVDD、ストリキニーネ/メタアルデヒド中毒、破傷風に",
            },
            "cat": {
                "safe": True,
                "dosage": "20-44 mg/kg PO q8h",
                "dosage_ja": "20-44 mg/kg 経口 8時間毎",
                "notes": "For muscle spasms; lower end of dose range",
                "notes_ja": "筋痙攣に。用量範囲の低用量",
            },
            "horse": {
                "safe": True,
                "dosage": "4.4-44 mg/kg IV slowly",
                "dosage_ja": "4.4-44 mg/kg ゆっくり静注",
                "notes": "For exertional rhabdomyolysis (tying up), tetanus",
                "notes_ja": "労作性横紋筋融解症（タイイングアップ）、破傷風に",
            },
            "rabbit": {
                "safe": True,
                "dosage": "Not well established",
                "dosage_ja": "十分に確立されていない",
                "notes": "Limited data",
                "notes_ja": "データ限定的",
            },
            "ferret": {
                "safe": True,
                "dosage": "Not well established",
                "dosage_ja": "十分に確立されていない",
                "notes": "Limited use",
                "notes_ja": "限定的使用",
            },
            "bird": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Not recommended",
                "notes_ja": "推奨されない",
            },
        },
        "side_effects": ["sedation", "weakness", "salivation", "vomiting", "brown discoloration of urine"],
        "side_effects_ja": ["鎮静", "衰弱", "流涎", "嘔吐", "尿の褐色変色"],
        "contraindications": "Known hypersensitivity. Renal impairment (injectable contains polyethylene glycol).",
        "contraindications_ja": "過敏症既知。腎障害（注射剤にポリエチレングリコール含有）。",
        "drug_interactions": [{"drug": "CNS depressants", "effect": "Additive sedation", "effect_ja": "鎮静の加算"}],
    },
    {
        "id": "loperamide",
        "name": "Loperamide",
        "name_ja": "ロペラミド",
        "category": "antidiarrheals",
        "mechanism": "Synthetic opioid; acts on mu-opioid receptors in GI wall to slow motility and increase absorption.",
        "mechanism_ja": "合成オピオイド。消化管壁のμオピオイド受容体に作用し運動を減速、吸収を増加させる。",
        "routes": ["PO"],
        "routes_ja": ["経口"],
        "formulations": ["Capsules", "Oral liquid (Imodium)"],
        "formulations_ja": ["カプセル", "経口液（イモジウム）"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "0.1-0.2 mg/kg PO q8-12h",
                "dosage_ja": "0.1-0.2 mg/kg 経口 8-12時間毎",
                "notes": "CAUTION: TOXIC to Collies and MDR1 mutation carriers (crosses BBB → CNS depression)",
                "notes_ja": "【注意】コリーおよびMDR1変異キャリアには毒性（BBBを通過→CNS抑制）",
            },
            "cat": {
                "safe": True,
                "dosage": "0.08-0.16 mg/kg PO q12h",
                "dosage_ja": "0.08-0.16 mg/kg 経口 12時間毎",
                "notes": "Use with caution; lower doses than dogs",
                "notes_ja": "注意して使用。犬より低用量",
            },
            "horse": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Can cause fatal ileus in horses",
                "notes_ja": "馬で致死的イレウスを起こす可能性",
            },
            "rabbit": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "CONTRAINDICATED - GI stasis risk",
                "notes_ja": "【禁忌】消化管鬱滞リスク",
            },
            "guinea_pig": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "CONTRAINDICATED",
                "notes_ja": "【禁忌】",
            },
            "ferret": {
                "safe": True,
                "dosage": "0.2 mg/kg PO q12h",
                "dosage_ja": "0.2 mg/kg 経口 12時間毎",
                "notes": "Short-term only",
                "notes_ja": "短期のみ",
            },
        },
        "side_effects": ["constipation", "bloating", "CNS depression (MDR1 dogs)", "ileus", "sedation"],
        "side_effects_ja": ["便秘", "膨満", "CNS抑制(MDR1犬)", "イレウス", "鎮静"],
        "contraindications": "Collies and MDR1 (+/+) dogs. Horses. Rabbits. Young animals. Infectious diarrhea (toxin retention).",
        "contraindications_ja": "コリーおよびMDR1(+/+)犬。馬。ウサギ。幼若動物。感染性下痢（毒素滞留）。",
        "drug_interactions": [
            {
                "drug": "P-glycoprotein inhibitors",
                "effect": "Increased CNS penetration (ketoconazole, erythromycin)",
                "effect_ja": "CNS移行性増加（ケトコナゾール、エリスロマイシン）",
            }
        ],
    },
    {
        "id": "calcium_gluconate",
        "name": "Calcium Gluconate",
        "name_ja": "グルコン酸カルシウム",
        "category": "supplements",
        "mechanism": "Calcium salt; provides ionized calcium for cardiac and neuromuscular function. For eclampsia/hypocalcemia.",
        "mechanism_ja": "カルシウム塩。心臓・神経筋機能に必要なイオン化カルシウムを供給。子癇/低カルシウム血症に。",
        "routes": ["IV", "PO"],
        "routes_ja": ["静脈内", "経口"],
        "formulations": ["Injectable 10%", "Oral solution"],
        "formulations_ja": ["注射液10%", "経口液"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "50-150 mg/kg IV slowly over 10-20 min with ECG monitoring",
                "dosage_ja": "50-150 mg/kg 10-20分かけてゆっくり静注（ECGモニタリング下）",
                "notes": "For puerperal hypocalcemia (eclampsia); monitor ECG for bradycardia/arrhythmia",
                "notes_ja": "産褥期低カルシウム血症（子癇）に。徐脈/不整脈のECGモニタリング",
            },
            "cat": {
                "safe": True,
                "dosage": "50-100 mg/kg IV slowly with ECG monitoring",
                "dosage_ja": "50-100 mg/kg ゆっくり静注（ECGモニタリング下）",
                "notes": "For eclampsia; less common in cats than dogs",
                "notes_ja": "子癇に。猫では犬より少ない",
            },
            "horse": {
                "safe": True,
                "dosage": "100-200 mL of 23% calcium borogluconate IV slowly",
                "dosage_ja": "23%ボログルコン酸カルシウム100-200 mL ゆっくり静注",
                "notes": "For lactation tetany, transport tetany",
                "notes_ja": "泌乳テタニー、輸送テタニーに",
            },
            "rabbit": {
                "safe": True,
                "dosage": "50-100 mg/kg IV slowly",
                "dosage_ja": "50-100 mg/kg ゆっくり静注",
                "notes": "For hypocalcemia/eclampsia",
                "notes_ja": "低カルシウム血症/子癇に",
            },
            "guinea_pig": {
                "safe": True,
                "dosage": "50-100 mg/kg IV/SC slowly",
                "dosage_ja": "50-100 mg/kg ゆっくり静注/皮下",
                "notes": "For pregnancy toxemia with hypocalcemia",
                "notes_ja": "低カルシウム血症を伴う妊娠中毒症に",
            },
            "bird": {
                "safe": True,
                "dosage": "50-100 mg/kg IV/IM slowly",
                "dosage_ja": "50-100 mg/kg ゆっくり静注/筋注",
                "notes": "For hypocalcemia, egg binding",
                "notes_ja": "低カルシウム血症、卵詰まりに",
            },
        },
        "side_effects": ["bradycardia/cardiac arrest (too rapid IV)", "tissue necrosis if SC/perivascular", "vomiting"],
        "side_effects_ja": ["徐脈/心停止(急速静注で)", "皮下/血管周囲で組織壊死", "嘔吐"],
        "contraindications": "Hypercalcemia. Digitalis therapy (potentiates toxicity). Give IV slowly with ECG.",
        "contraindications_ja": "高カルシウム血症。ジギタリス療法（毒性を増強）。ECGモニタリング下でゆっくり静注。",
        "drug_interactions": [
            {
                "drug": "digoxin",
                "effect": "Increased cardiac toxicity - use with extreme caution",
                "effect_ja": "心毒性増加 - 細心の注意で使用",
            }
        ],
    },
    {
        "id": "tacrolimus_ophthalmic",
        "name": "Tacrolimus Ophthalmic",
        "name_ja": "タクロリムス点眼薬",
        "category": "ophthalmic",
        "mechanism": "Calcineurin inhibitor (topical); more potent than cyclosporine for tear stimulation.",
        "mechanism_ja": "カルシニューリン阻害薬（外用）。涙液刺激においてシクロスポリンより強力。",
        "routes": ["ophthalmic"],
        "routes_ja": ["点眼"],
        "formulations": ["Compounded ointment 0.02-0.03%"],
        "formulations_ja": ["院内調製軟膏0.02-0.03%"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "Apply q12h",
                "dosage_ja": "12時間毎に塗布",
                "notes": "For KCS refractory to cyclosporine; 10-100x more potent",
                "notes_ja": "シクロスポリン不応のKCSに。10-100倍強力",
            },
            "cat": {
                "safe": True,
                "dosage": "Apply q12h",
                "dosage_ja": "12時間毎に塗布",
                "notes": "For eosinophilic keratitis refractory to CsA",
                "notes_ja": "CsA不応の好酸球性角膜炎に",
            },
            "horse": {
                "safe": True,
                "dosage": "Apply q12h",
                "dosage_ja": "12時間毎に塗布",
                "notes": "For immune-mediated keratitis",
                "notes_ja": "免疫介在性角膜炎に",
            },
            "rabbit": {
                "safe": True,
                "dosage": "Apply q12h",
                "dosage_ja": "12時間毎に塗布",
                "notes": "For dry eye",
                "notes_ja": "ドライアイに",
            },
            "guinea_pig": {
                "safe": True,
                "dosage": "Apply q12h",
                "dosage_ja": "12時間毎に塗布",
                "notes": "Limited data",
                "notes_ja": "データ限定的",
            },
            "bird": {
                "safe": True,
                "dosage": "Apply q12h",
                "dosage_ja": "12時間毎に塗布",
                "notes": "Limited data",
                "notes_ja": "データ限定的",
            },
        },
        "side_effects": ["transient irritation"],
        "side_effects_ja": ["一過性の刺激"],
        "contraindications": "Active ocular infection.",
        "contraindications_ja": "活動性の眼感染症。",
        "drug_interactions": [],
    },
    {
        "id": "latanoprost",
        "name": "Latanoprost",
        "name_ja": "ラタノプロスト",
        "category": "ophthalmic",
        "mechanism": "Prostaglandin F2α analog; increases uveoscleral aqueous humor outflow, reducing IOP.",
        "mechanism_ja": "プロスタグランジンF2αアナログ。ブドウ膜強膜流出路からの房水排出を増加し眼圧を低下。",
        "routes": ["ophthalmic"],
        "routes_ja": ["点眼"],
        "formulations": ["Ophthalmic solution 0.005%"],
        "formulations_ja": ["点眼液0.005%"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "1 drop q12-24h",
                "dosage_ja": "1滴 12-24時間毎",
                "notes": "Most effective single IOP-lowering agent in dogs; causes miosis",
                "notes_ja": "犬で最も効果的な単剤眼圧降下薬。縮瞳を起こす",
            },
            "cat": {
                "safe": True,
                "dosage": "1 drop q12-24h",
                "dosage_ja": "1滴 12-24時間毎",
                "notes": "Less effective in cats than dogs; may cause anterior uveitis",
                "notes_ja": "犬より猫で効果が低い。前部ぶどう膜炎を起こす可能性",
            },
            "horse": {
                "safe": True,
                "dosage": "1 drop q12h",
                "dosage_ja": "1滴 12時間毎",
                "notes": "For equine glaucoma",
                "notes_ja": "馬の緑内障に",
            },
            "rabbit": {
                "safe": True,
                "dosage": "1 drop q12h",
                "dosage_ja": "1滴 12時間毎",
                "notes": "Effective for glaucoma",
                "notes_ja": "緑内障に有効",
            },
            "guinea_pig": {
                "safe": True,
                "dosage": "1 drop q12h",
                "dosage_ja": "1滴 12時間毎",
                "notes": "For glaucoma",
                "notes_ja": "緑内障に",
            },
            "bird": {
                "safe": True,
                "dosage": "1 drop q12h",
                "dosage_ja": "1滴 12時間毎",
                "notes": "Limited data",
                "notes_ja": "データ限定的",
            },
        },
        "side_effects": ["miosis", "conjunctival hyperemia", "anterior uveitis", "iris color change"],
        "side_effects_ja": ["縮瞳", "結膜充血", "前部ぶどう膜炎", "虹彩色変化"],
        "contraindications": "Active uveitis. Lens luxation (miosis can trap lens).",
        "contraindications_ja": "活動性ぶどう膜炎。水晶体脱臼（縮瞳で水晶体を捕捉する可能性）。",
        "drug_interactions": [],
    },
    {
        "id": "sotalol",
        "name": "Sotalol",
        "name_ja": "ソタロール",
        "category": "antiarrhythmics",
        "mechanism": "Class III antiarrhythmic (potassium channel blocker) with class II (beta-blocker) properties.",
        "mechanism_ja": "クラスIII抗不整脈薬（カリウムチャネル遮断）。クラスII（β遮断）の特性も持つ。",
        "routes": ["PO"],
        "routes_ja": ["経口"],
        "formulations": ["Tablets"],
        "formulations_ja": ["錠剤"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "1-3 mg/kg PO q12h",
                "dosage_ja": "1-3 mg/kg 経口 12時間毎",
                "notes": "For ventricular arrhythmias (VPCs, VT); Boxer arrhythmogenic right ventricular cardiomyopathy",
                "notes_ja": "心室性不整脈(VPC、VT)に。ボクサーの不整脈原性右室心筋症に",
            },
            "cat": {
                "safe": True,
                "dosage": "1-2 mg/kg PO q12h",
                "dosage_ja": "1-2 mg/kg 経口 12時間毎",
                "notes": "For ventricular arrhythmias in cats",
                "notes_ja": "猫の心室性不整脈に",
            },
            "horse": {
                "safe": True,
                "dosage": "Not commonly used",
                "dosage_ja": "一般的には使用されない",
                "notes": "Limited equine data",
                "notes_ja": "馬のデータは限定的",
            },
            "ferret": {
                "safe": True,
                "dosage": "Not well established",
                "dosage_ja": "十分に確立されていない",
                "notes": "Limited data",
                "notes_ja": "データ限定的",
            },
            "rabbit": {
                "safe": True,
                "dosage": "Not well established",
                "dosage_ja": "十分に確立されていない",
                "notes": "Limited data",
                "notes_ja": "データ限定的",
            },
            "bird": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Not studied",
                "notes_ja": "未研究",
            },
        },
        "side_effects": ["bradycardia", "hypotension", "bronchospasm", "weakness", "proarrhythmic effects"],
        "side_effects_ja": ["徐脈", "低血圧", "気管支痙攣", "衰弱", "催不整脈作用"],
        "contraindications": "Sinus bradycardia. AV block. Asthma. Decompensated heart failure. Hypokalemia.",
        "contraindications_ja": "洞性徐脈。房室ブロック。喘息。非代償性心不全。低カリウム血症。",
        "drug_interactions": [
            {
                "drug": "calcium channel blockers",
                "effect": "Severe bradycardia/hypotension",
                "effect_ja": "重度徐脈/低血圧",
            }
        ],
    },
    {
        "id": "clopidogrel",
        "name": "Clopidogrel",
        "name_ja": "クロピドグレル",
        "category": "cardiovascular",
        "mechanism": "Antiplatelet agent; irreversibly inhibits P2Y12 ADP receptor on platelets, preventing aggregation.",
        "mechanism_ja": "抗血小板薬。血小板上のP2Y12 ADP受容体を不可逆的に阻害し凝集を阻止。",
        "routes": ["PO"],
        "routes_ja": ["経口"],
        "formulations": ["Tablets"],
        "formulations_ja": ["錠剤"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "1-2 mg/kg PO q24h",
                "dosage_ja": "1-2 mg/kg 経口 24時間毎",
                "notes": "For hypercoagulable states: IMHA, PLE, cardiac disease thrombi prevention",
                "notes_ja": "過凝固状態に: IMHA、PLE、心疾患の血栓予防",
            },
            "cat": {
                "safe": True,
                "dosage": "18.75 mg/cat PO q24h (1/4 of 75mg tab)",
                "dosage_ja": "18.75 mg/匹 経口 24時間毎（75mg錠の1/4）",
                "notes": "KEY drug for feline ATE prevention; superior to aspirin per FAT CAT study",
                "notes_ja": "猫ATE予防の重要薬。FAT CAT研究でアスピリンより優秀",
            },
            "horse": {
                "safe": True,
                "dosage": "Not well established",
                "dosage_ja": "十分に確立されていない",
                "notes": "Limited equine data",
                "notes_ja": "馬のデータは限定的",
            },
            "ferret": {
                "safe": True,
                "dosage": "Not well established",
                "dosage_ja": "十分に確立されていない",
                "notes": "Limited data",
                "notes_ja": "データ限定的",
            },
            "rabbit": {
                "safe": True,
                "dosage": "Not well established",
                "dosage_ja": "十分に確立されていない",
                "notes": "Limited data",
                "notes_ja": "データ限定的",
            },
            "bird": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Not studied",
                "notes_ja": "未研究",
            },
        },
        "side_effects": ["bleeding", "GI upset", "rare hepatotoxicity"],
        "side_effects_ja": ["出血", "消化器症状", "まれな肝毒性"],
        "contraindications": "Active bleeding. Upcoming surgery (discontinue 5-7 days prior).",
        "contraindications_ja": "活動性出血。手術予定（5-7日前に中止）。",
        "drug_interactions": [{"drug": "NSAIDs", "effect": "Increased bleeding risk", "effect_ja": "出血リスク増加"}],
    },
    {
        "id": "mannitol",
        "name": "Mannitol",
        "name_ja": "マンニトール",
        "category": "diuretics",
        "mechanism": "Osmotic diuretic; increases plasma osmolality, drawing fluid from tissues (brain, eye).",
        "mechanism_ja": "浸透圧利尿薬。血漿浸透圧を上昇させ組織（脳、眼）から水分を引き出す。",
        "routes": ["IV"],
        "routes_ja": ["静脈内"],
        "formulations": ["Injectable solution 20-25%"],
        "formulations_ja": ["注射液20-25%"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "0.5-1 g/kg IV over 15-20 min",
                "dosage_ja": "0.5-1 g/kg 15-20分かけて静注",
                "notes": "For acute glaucoma, cerebral edema (head trauma); do not repeat more than 3x",
                "notes_ja": "急性緑内障、脳浮腫(頭部外傷)に。3回以上反復しない",
            },
            "cat": {
                "safe": True,
                "dosage": "0.5-1 g/kg IV over 15-20 min",
                "dosage_ja": "0.5-1 g/kg 15-20分かけて静注",
                "notes": "For acute glaucoma, cerebral edema",
                "notes_ja": "急性緑内障、脳浮腫に",
            },
            "horse": {
                "safe": True,
                "dosage": "0.25-1 g/kg IV over 15-20 min",
                "dosage_ja": "0.25-1 g/kg 15-20分かけて静注",
                "notes": "For cerebral edema",
                "notes_ja": "脳浮腫に",
            },
            "rabbit": {
                "safe": True,
                "dosage": "0.5-1 g/kg IV over 15-20 min",
                "dosage_ja": "0.5-1 g/kg 15-20分かけて静注",
                "notes": "For head trauma/cerebral edema",
                "notes_ja": "頭部外傷/脳浮腫に",
            },
            "ferret": {
                "safe": True,
                "dosage": "0.5 g/kg IV over 15-20 min",
                "dosage_ja": "0.5 g/kg 15-20分かけて静注",
                "notes": "For emergencies",
                "notes_ja": "緊急時に",
            },
            "bird": {
                "safe": True,
                "dosage": "0.5-1 g/kg IV slowly",
                "dosage_ja": "0.5-1 g/kg ゆっくり静注",
                "notes": "For head trauma",
                "notes_ja": "頭部外傷に",
            },
        },
        "side_effects": ["rebound cerebral edema", "dehydration", "electrolyte imbalances", "volume overload"],
        "side_effects_ja": ["リバウンド脳浮腫", "脱水", "電解質異常", "体液量過剰"],
        "contraindications": "Pulmonary edema. Congestive heart failure. Active intracranial hemorrhage. Anuria.",
        "contraindications_ja": "肺水腫。うっ血性心不全。活動性頭蓋内出血。無尿。",
        "drug_interactions": [],
    },
    {
        "id": "misoprostol",
        "name": "Misoprostol",
        "name_ja": "ミソプロストール",
        "category": "gi_drugs",
        "mechanism": "Synthetic prostaglandin E1 analog; replaces protective prostaglandins inhibited by NSAIDs. Cytoprotective.",
        "mechanism_ja": "合成プロスタグランジンE1アナログ。NSAIDsにより阻害された防御的プロスタグランジンを補充。細胞保護作用。",
        "routes": ["PO"],
        "routes_ja": ["経口"],
        "formulations": ["Tablets"],
        "formulations_ja": ["錠剤"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "2-5 mcg/kg PO q8h",
                "dosage_ja": "2-5 mcg/kg 経口 8時間毎",
                "notes": "For NSAID-induced GI ulceration prevention/treatment",
                "notes_ja": "NSAID誘発性消化管潰瘍の予防/治療に",
            },
            "cat": {
                "safe": True,
                "dosage": "5 mcg/kg PO q8h",
                "dosage_ja": "5 mcg/kg 経口 8時間毎",
                "notes": "For GI ulceration; less commonly used in cats",
                "notes_ja": "消化管潰瘍に。猫では使用頻度低い",
            },
            "horse": {
                "safe": True,
                "dosage": "5 mcg/kg PO q8-12h",
                "dosage_ja": "5 mcg/kg 経口 8-12時間毎",
                "notes": "For NSAID-induced right dorsal colitis prevention",
                "notes_ja": "NSAID誘発性右背側結腸炎の予防に",
            },
            "rabbit": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Not well studied; abortifacient risk",
                "notes_ja": "十分に研究されていない。流産惹起リスク",
            },
            "ferret": {
                "safe": True,
                "dosage": "1-5 mcg/kg PO q8h",
                "dosage_ja": "1-5 mcg/kg 経口 8時間毎",
                "notes": "For GI ulceration",
                "notes_ja": "消化管潰瘍に",
            },
            "bird": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Not studied",
                "notes_ja": "未研究",
            },
        },
        "side_effects": ["diarrhea", "abdominal cramping", "abortion (pregnant animals)"],
        "side_effects_ja": ["下痢", "腹部痙攣", "流産(妊娠動物)"],
        "contraindications": "PREGNANCY (potent abortifacient). Human handlers who are pregnant must not handle.",
        "contraindications_ja": "【禁忌】妊娠中（強力な流産惹起薬）。妊娠中のヒト取扱者は取り扱い不可。",
        "drug_interactions": [],
    },
    {
        "id": "sulfasalazine",
        "name": "Sulfasalazine",
        "name_ja": "サラゾスルファピリジン",
        "category": "gi_drugs",
        "mechanism": "Aminosalicylate; metabolized to 5-ASA (anti-inflammatory) and sulfapyridine in colon. For IBD/colitis.",
        "mechanism_ja": "アミノサリチル酸。大腸で5-ASA(抗炎症)とスルファピリジンに代謝される。IBD/大腸炎に。",
        "routes": ["PO"],
        "routes_ja": ["経口"],
        "formulations": ["Tablets"],
        "formulations_ja": ["錠剤"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "20-30 mg/kg PO q8-12h",
                "dosage_ja": "20-30 mg/kg 経口 8-12時間毎",
                "notes": "For large bowel IBD/colitis; may cause KCS - monitor Schirmer tear test",
                "notes_ja": "大腸IBD/大腸炎に。KCSを起こす可能性 - シルマー涙液試験をモニタリング",
            },
            "cat": {
                "safe": True,
                "dosage": "10-20 mg/kg PO q12h (short-term only)",
                "dosage_ja": "10-20 mg/kg 経口 12時間毎（短期のみ）",
                "notes": "Cats sensitive to salicylates; short-term only; monitor for anorexia/fever",
                "notes_ja": "猫はサリチル酸に敏感。短期のみ。食欲不振/発熱をモニタリング",
            },
            "horse": {
                "safe": True,
                "dosage": "Not commonly used",
                "dosage_ja": "一般的には使用されない",
                "notes": "Limited equine data",
                "notes_ja": "馬のデータは限定的",
            },
            "rabbit": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Sulfonamide component risky",
                "notes_ja": "サルファ剤成分にリスク",
            },
            "ferret": {
                "safe": True,
                "dosage": "10-20 mg/kg PO q12h",
                "dosage_ja": "10-20 mg/kg 経口 12時間毎",
                "notes": "For colitis",
                "notes_ja": "大腸炎に",
            },
            "bird": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Not studied",
                "notes_ja": "未研究",
            },
        },
        "side_effects": ["KCS (dry eye)", "vomiting", "hepatotoxicity", "hemolytic anemia", "allergic reaction"],
        "side_effects_ja": ["KCS(ドライアイ)", "嘔吐", "肝毒性", "溶血性貧血", "アレルギー反応"],
        "contraindications": "Sulfonamide allergy. KCS history. Hepatic disease.",
        "contraindications_ja": "サルファ剤アレルギー。KCS既往。肝疾患。",
        "drug_interactions": [],
    },
    {
        "id": "vitamin_b12",
        "name": "Vitamin B12 (Cobalamin)",
        "name_ja": "ビタミンB12（コバラミン）",
        "category": "supplements",
        "mechanism": "Essential cofactor for methylmalonyl-CoA mutase and methionine synthase. Deficiency causes GI/neurological disease.",
        "mechanism_ja": "メチルマロニルCoAムターゼとメチオニン合成酵素の必須補因子。欠乏は消化器/神経疾患を引き起こす。",
        "routes": ["SC", "IM", "PO"],
        "routes_ja": ["皮下", "筋肉内", "経口"],
        "formulations": ["Injectable solution", "Oral tablets", "Oral transmucosal"],
        "formulations_ja": ["注射液", "経口錠", "経口粘膜"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "250-1500 mcg/dog SC q1-4wk based on body weight",
                "dosage_ja": "250-1500 mcg/匹 皮下 体重に基づき1-4週毎",
                "notes": "For GI malabsorption (EPI, IBD, SIBO); check serum levels",
                "notes_ja": "消化管吸収不良(EPI、IBD、SIBO)に。血清レベル確認",
            },
            "cat": {
                "safe": True,
                "dosage": "250 mcg/cat SC q1-2wk; or 250mcg PO q24h",
                "dosage_ja": "250 mcg/匹 皮下 1-2週毎; または250mcg 経口 24時間毎",
                "notes": "Very commonly deficient in feline GI disease; check serum cobalamin",
                "notes_ja": "猫の消化器疾患で非常に一般的に欠乏。血清コバラミン確認",
            },
            "horse": {
                "safe": True,
                "dosage": "Not commonly supplemented",
                "dosage_ja": "通常は補充不要",
                "notes": "Synthesized by hindgut bacteria in horses",
                "notes_ja": "馬では後腸細菌により合成される",
            },
            "rabbit": {
                "safe": True,
                "dosage": "50-200 mcg/rabbit SC q7-14d",
                "dosage_ja": "50-200 mcg/匹 皮下 7-14日毎",
                "notes": "For GI disease",
                "notes_ja": "消化器疾患に",
            },
            "ferret": {
                "safe": True,
                "dosage": "250 mcg/ferret SC q7-14d",
                "dosage_ja": "250 mcg/匹 皮下 7-14日毎",
                "notes": "For GI disease, IBD",
                "notes_ja": "消化器疾患、IBDに",
            },
            "bird": {
                "safe": True,
                "dosage": "50-250 mcg/kg IM q7-14d",
                "dosage_ja": "50-250 mcg/kg 筋注 7-14日毎",
                "notes": "For malabsorption",
                "notes_ja": "吸収不良に",
            },
        },
        "side_effects": ["none significant at therapeutic doses"],
        "side_effects_ja": ["治療用量では有意な副作用なし"],
        "contraindications": "None known.",
        "contraindications_ja": "知られていない。",
        "drug_interactions": [],
    },
    {
        "id": "iron_dextran",
        "name": "Iron Dextran",
        "name_ja": "鉄デキストラン",
        "category": "supplements",
        "mechanism": "Injectable iron supplement; provides elemental iron for hemoglobin synthesis.",
        "mechanism_ja": "注射用鉄剤。ヘモグロビン合成に必要な元素鉄を供給する。",
        "routes": ["IM", "IV"],
        "routes_ja": ["筋肉内", "静脈内"],
        "formulations": ["Injectable solution"],
        "formulations_ja": ["注射液"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "10-20 mg/kg IM (one-time or repeat in 2-4 weeks)",
                "dosage_ja": "10-20 mg/kg 筋注（1回または2-4週後に再投与）",
                "notes": "For iron deficiency anemia (chronic blood loss, hookworms)",
                "notes_ja": "鉄欠乏性貧血（慢性失血、鉤虫）に",
            },
            "cat": {
                "safe": True,
                "dosage": "10-20 mg/kg IM",
                "dosage_ja": "10-20 mg/kg 筋注",
                "notes": "For iron deficiency; less common in cats",
                "notes_ja": "鉄欠乏に。猫ではまれ",
            },
            "horse": {
                "safe": True,
                "dosage": "1-2 g IM (foals); adults rarely needed",
                "dosage_ja": "1-2 g 筋注（子馬）; 成馬ではまれに必要",
                "notes": "For neonatal iron deficiency",
                "notes_ja": "新生子鉄欠乏に",
            },
            "rabbit": {
                "safe": True,
                "dosage": "10 mg/kg IM",
                "dosage_ja": "10 mg/kg 筋注",
                "notes": "For iron deficiency anemia",
                "notes_ja": "鉄欠乏性貧血に",
            },
            "ferret": {
                "safe": True,
                "dosage": "10 mg/kg IM",
                "dosage_ja": "10 mg/kg 筋注",
                "notes": "For chronic disease anemia",
                "notes_ja": "慢性疾患性貧血に",
            },
            "bird": {
                "safe": True,
                "dosage": "10 mg/kg IM once",
                "dosage_ja": "10 mg/kg 筋注 1回",
                "notes": "For iron deficiency",
                "notes_ja": "鉄欠乏に",
            },
        },
        "side_effects": ["pain at injection site", "staining of tissues", "anaphylaxis (rare)", "iron overload"],
        "side_effects_ja": ["注射部位の疼痛", "組織の着色", "アナフィラキシー(まれ)", "鉄過剰"],
        "contraindications": "Iron overload. Hemolytic anemia (not iron deficient). Hepatic disease.",
        "contraindications_ja": "鉄過剰。溶血性貧血（鉄欠乏ではない）。肝疾患。",
        "drug_interactions": [],
    },
    {
        "id": "erythropoietin",
        "name": "Erythropoietin (EPO)",
        "name_ja": "エリスロポエチン",
        "category": "endocrine",
        "mechanism": "Recombinant human glycoprotein; stimulates red blood cell production in bone marrow. For CKD anemia.",
        "mechanism_ja": "組換えヒト糖蛋白。骨髄での赤血球産生を刺激する。CKD貧血に。",
        "routes": ["SC"],
        "routes_ja": ["皮下"],
        "formulations": ["Injectable solution (Epogen/Procrit)"],
        "formulations_ja": ["注射液（エポジェン/プロクリット）"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "100 U/kg SC 3x/week until PCV normalizes, then reduce frequency",
                "dosage_ja": "100 U/kg 皮下 週3回 PCV正常化まで、その後頻度減少",
                "notes": "For CKD non-regenerative anemia; 25-40% develop anti-EPO antibodies → pure red cell aplasia",
                "notes_ja": "CKD非再生性貧血に。25-40%が抗EPO抗体を産生→純赤芽球無形成症",
            },
            "cat": {
                "safe": True,
                "dosage": "100 U/kg SC 3x/week",
                "dosage_ja": "100 U/kg 皮下 週3回",
                "notes": "Same antibody risk as dogs; darbepoetin (Aranesp) may be preferred",
                "notes_ja": "犬と同じ抗体リスク。ダルベポエチン（アラネスプ）が好ましい場合あり",
            },
            "horse": {
                "safe": False,
                "dosage": "N/A",
                "dosage_ja": "使用不可",
                "notes": "Used as doping agent - prohibited in competition",
                "notes_ja": "ドーピング薬として使用される - 競技では禁止",
            },
            "ferret": {
                "safe": True,
                "dosage": "50-150 U/kg SC 2-3x/week",
                "dosage_ja": "50-150 U/kg 皮下 週2-3回",
                "notes": "For CKD, estrogen-induced aplastic anemia",
                "notes_ja": "CKD、エストロゲン誘発性再生不良性貧血に",
            },
            "rabbit": {
                "safe": True,
                "dosage": "100 U/kg SC 2-3x/week",
                "dosage_ja": "100 U/kg 皮下 週2-3回",
                "notes": "Limited data",
                "notes_ja": "データ限定的",
            },
            "bird": {
                "safe": True,
                "dosage": "Not well established",
                "dosage_ja": "十分に確立されていない",
                "notes": "Limited avian data",
                "notes_ja": "鳥類のデータは限定的",
            },
        },
        "side_effects": [
            "anti-EPO antibody formation → pure red cell aplasia",
            "hypertension",
            "seizures",
            "iron deficiency",
            "polycythemia",
        ],
        "side_effects_ja": ["抗EPO抗体形成→純赤芽球無形成症", "高血圧", "痙攣", "鉄欠乏", "多血症"],
        "contraindications": "Uncontrolled hypertension. Adequate iron stores required.",
        "contraindications_ja": "コントロールされていない高血圧。十分な鉄貯蔵が必要。",
        "drug_interactions": [],
    },
    {
        "id": "desmopressin",
        "name": "Desmopressin (DDAVP)",
        "name_ja": "デスモプレシン",
        "category": "endocrine",
        "mechanism": "Synthetic analog of antidiuretic hormone (ADH/vasopressin); increases water reabsorption in collecting ducts.",
        "mechanism_ja": "抗利尿ホルモン(ADH/バソプレシン)の合成アナログ。集合管での水分再吸収を増加させる。",
        "routes": ["intranasal", "IV", "SC", "conjunctival"],
        "routes_ja": ["鼻腔内", "静脈内", "皮下", "結膜"],
        "formulations": ["Nasal spray", "Injectable", "Ophthalmic drops (off-label use)"],
        "formulations_ja": ["鼻腔スプレー", "注射剤", "点眼液(適応外使用)"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "1-4 drops intranasally or conjunctivally q12-24h; diagnostic: 0.5 mcg/kg SC",
                "dosage_ja": "1-4滴 鼻腔内または結膜 12-24時間毎; 診断: 0.5 mcg/kg 皮下",
                "notes": "For central diabetes insipidus (diagnostic test and treatment); von Willebrand's disease bleeding",
                "notes_ja": "中枢性尿崩症（診断テストおよび治療）に。フォンビルブランド病の出血に",
            },
            "cat": {
                "safe": True,
                "dosage": "1-2 drops intranasally q12-24h",
                "dosage_ja": "1-2滴 鼻腔内 12-24時間毎",
                "notes": "For central DI; less common in cats",
                "notes_ja": "中枢性尿崩症に。猫ではまれ",
            },
            "horse": {
                "safe": True,
                "dosage": "0.25 mcg/kg IV (diagnostic)",
                "dosage_ja": "0.25 mcg/kg 静注（診断用）",
                "notes": "Primarily diagnostic for DI",
                "notes_ja": "主に尿崩症の診断用",
            },
            "ferret": {
                "safe": True,
                "dosage": "1 drop intranasally q12-24h",
                "dosage_ja": "1滴 鼻腔内 12-24時間毎",
                "notes": "For central DI",
                "notes_ja": "中枢性尿崩症に",
            },
            "rabbit": {
                "safe": True,
                "dosage": "Not commonly needed",
                "dosage_ja": "通常は不要",
                "notes": "DI rare in rabbits",
                "notes_ja": "ウサギでは尿崩症はまれ",
            },
            "bird": {
                "safe": True,
                "dosage": "Not well established",
                "dosage_ja": "十分に確立されていない",
                "notes": "Limited data",
                "notes_ja": "データ限定的",
            },
        },
        "side_effects": ["water intoxication/hyponatremia (if water not restricted)", "facial flushing", "headache"],
        "side_effects_ja": ["水中毒/低ナトリウム血症(飲水制限しない場合)", "顔面紅潮", "頭痛"],
        "contraindications": "Nephrogenic DI (won't respond). Heart failure. Hyponatremia.",
        "contraindications_ja": "腎性尿崩症（反応しない）。心不全。低ナトリウム血症。",
        "drug_interactions": [],
    },
    {
        "id": "calcitriol",
        "name": "Calcitriol",
        "name_ja": "カルシトリオール",
        "category": "endocrine",
        "mechanism": "Active form of vitamin D3 (1,25-dihydroxycholecalciferol); increases calcium absorption and regulates PTH.",
        "mechanism_ja": "ビタミンD3の活性型（1,25-ジヒドロキシコレカルシフェロール）。カルシウム吸収を増加しPTHを調節。",
        "routes": ["PO"],
        "routes_ja": ["経口"],
        "formulations": ["Capsules", "Oral solution"],
        "formulations_ja": ["カプセル", "経口液"],
        "species_info": {
            "dog": {
                "safe": True,
                "dosage": "2.5-3.5 ng/kg PO q24h",
                "dosage_ja": "2.5-3.5 ng/kg 経口 24時間毎",
                "notes": "For renal secondary hyperparathyroidism (CKD); monitor ionized calcium closely",
                "notes_ja": "腎性続発性副甲状腺機能亢進症(CKD)に。イオン化カルシウムを厳密にモニタリング",
            },
            "cat": {
                "safe": True,
                "dosage": "2.5-3.5 ng/kg PO q24h",
                "dosage_ja": "2.5-3.5 ng/kg 経口 24時間毎",
                "notes": "For CKD; very small doses - nanogram dosing",
                "notes_ja": "CKDに。非常に少量 - ナノグラム単位の投与",
            },
            "horse": {
                "safe": True,
                "dosage": "Not commonly used",
                "dosage_ja": "一般的には使用されない",
                "notes": "Limited equine data",
                "notes_ja": "馬のデータは限定的",
            },
            "rabbit": {
                "safe": True,
                "dosage": "Not well established",
                "dosage_ja": "十分に確立されていない",
                "notes": "Limited data; rabbits have unique calcium metabolism",
                "notes_ja": "データ限定的。ウサギは独特のカルシウム代謝を持つ",
            },
            "ferret": {
                "safe": True,
                "dosage": "Not well established",
                "dosage_ja": "十分に確立されていない",
                "notes": "Limited data",
                "notes_ja": "データ限定的",
            },
            "bird": {
                "safe": True,
                "dosage": "Not well established",
                "dosage_ja": "十分に確立されていない",
                "notes": "For hypocalcemia",
                "notes_ja": "低カルシウム血症に",
            },
        },
        "side_effects": ["hypercalcemia", "soft tissue mineralization", "polyuria/polydipsia", "anorexia", "vomiting"],
        "side_effects_ja": ["高カルシウム血症", "軟部組織石灰化", "多尿/多飲", "食欲不振", "嘔吐"],
        "contraindications": "Hypercalcemia. Hyperphosphatemia (must control phosphorus first). Must monitor iCa regularly.",
        "contraindications_ja": "高カルシウム血症。高リン血症（先にリンをコントロールする必要）。定期的にiCaモニタリングが必要。",
        "drug_interactions": [
            {
                "drug": "thiazide diuretics",
                "effect": "Increased hypercalcemia risk",
                "effect_ja": "高カルシウム血症リスク増加",
            }
        ],
    },
]

# バッチファイルの薬品を統合（重複IDを除外）
_existing_ids = {d["id"] for d in DRUGS}
for _batch in (DRUGS_BATCH_1, DRUGS_BATCH_2):
    for _drug in _batch:
        if _drug["id"] not in _existing_ids:
            DRUGS.append(_drug)
            _existing_ids.add(_drug["id"])

# species_info パッチを適用（既存薬品に動物種別投与量を追加）
_drug_index = {d["id"]: d for d in DRUGS}
for _drug_id, _species_patch in SPECIES_INFO_PATCH.items():
    if _drug_id in _drug_index:
        _target = _drug_index[_drug_id].setdefault("species_info", {})
        for _sp, _info in _species_patch.items():
            if _sp not in _target:
                _target[_sp] = _info

# 魚用薬品を統合
for _fish_drug in FISH_DRUGS:
    if _fish_drug["id"] not in _existing_ids:
        DRUGS.append(_fish_drug)
        _existing_ids.add(_fish_drug["id"])
        _drug_index[_fish_drug["id"]] = _fish_drug

# 魚用 species_info パッチを適用
for _drug_id, _fish_info in FISH_SPECIES_INFO_PATCH.items():
    if _drug_id in _drug_index:
        _target = _drug_index[_drug_id].setdefault("species_info", {})
        if "fish" not in _target:
            _target["fish"] = _fish_info["fish"]

# バッチ5 薬品を統合（最新薬品 2023-2025）
for _drug5 in DRUGS_BATCH_5:
    if _drug5["id"] not in _existing_ids:
        DRUGS.append(_drug5)
        _existing_ids.add(_drug5["id"])
        _drug_index[_drug5["id"]] = _drug5

# バッチ5 species_info パッチを適用
for _drug_id, _species_patch in SPECIES_INFO_PATCH_5.items():
    if _drug_id in _drug_index:
        _target = _drug_index[_drug_id].setdefault("species_info", {})
        for _sp, _info in _species_patch.items():
            if _sp not in _target:
                _target[_sp] = _info

# バッチ6 薬品を統合（救急・循環器・その他）
for _drug6 in DRUGS_BATCH_6:
    if _drug6["id"] not in _existing_ids:
        DRUGS.append(_drug6)
        _existing_ids.add(_drug6["id"])
        _drug_index[_drug6["id"]] = _drug6

# バッチ6 species_info パッチを適用
for _drug_id, _species_patch in SPECIES_INFO_PATCH_6.items():
    if _drug_id in _drug_index:
        _target = _drug_index[_drug_id].setdefault("species_info", {})
        for _sp, _info in _species_patch.items():
            if _sp not in _target:
                _target[_sp] = _info

# バッチ6 薬物相互作用パッチを適用
for _drug_id, _interactions in DRUG_INTERACTIONS_PATCH_6.items():
    if _drug_id in _drug_index:
        _existing = _drug_index[_drug_id].get("drug_interactions", [])
        if not _existing:
            _drug_index[_drug_id]["drug_interactions"] = _interactions


# バッチ7 チンチラ species_info パッチを適用
for _drug_id, _species_patch in CHINCHILLA_SPECIES_PATCH.items():
    if _drug_id in _drug_index:
        _target = _drug_index[_drug_id].setdefault("species_info", {})
        for _sp, _info in _species_patch.items():
            if _sp not in _target:
                _target[_sp] = _info

# バッチ8 繁殖医学薬品を統合（乳汁分泌促進・ホルモン・抗凝固薬等）
for _drug8 in DRUGS_BATCH_8:
    if _drug8["id"] not in _existing_ids:
        DRUGS.append(_drug8)
        _existing_ids.add(_drug8["id"])
        _drug_index[_drug8["id"]] = _drug8

# バッチ9 ISCAID尿路感染症ガイドライン薬品を統合（ホスホマイシン、カルバペネム等）
for _drug9 in DRUGS_BATCH_9:
    if _drug9["id"] not in _existing_ids:
        DRUGS.append(_drug9)
        _existing_ids.add(_drug9["id"])
        _drug_index[_drug9["id"]] = _drug9

# バッチ9 ISCAID UTI投与ノートを既存薬品に追記
for _drug_id, _species_notes in ISCAID_UTI_NOTES_PATCH.items():
    if _drug_id in _drug_index:
        _si = _drug_index[_drug_id].get("species_info", {})
        for _sp, _patch in _species_notes.items():
            if _sp in _si:
                if "notes_append" in _patch and "notes" in _si[_sp]:
                    _si[_sp]["notes"] += _patch["notes_append"]
                if "notes_ja_append" in _patch and "notes_ja" in _si[_sp]:
                    _si[_sp]["notes_ja"] += _patch["notes_ja_append"]

# バッチ10-19 薬品を統合
for _batch_new in (
    DRUGS_BATCH_10,
    DRUGS_BATCH_11,
    DRUGS_BATCH_12,
    DRUGS_BATCH_13,
    DRUGS_BATCH_14,
    DRUGS_BATCH_15,
    DRUGS_BATCH_16,
    DRUGS_BATCH_17,
    DRUGS_BATCH_18,
    DRUGS_BATCH_19,
    DRUGS_BATCH_20,
    DRUGS_BATCH_21,
    DRUGS_BATCH_22,
    DRUGS_BATCH_23,
    DRUGS_BATCH_24,
):
    for _drug_new in _batch_new:
        if _drug_new["id"] not in _existing_ids:
            DRUGS.append(_drug_new)
            _existing_ids.add(_drug_new["id"])
            _drug_index[_drug_new["id"]] = _drug_new

# バッチ25-26: 薬物相互作用パッチ適用
for _interactions_patch in (
    DRUG_INTERACTIONS_PATCH_25,
    DRUG_INTERACTIONS_PATCH_26,
    DRUG_INTERACTIONS_PATCH_27,
    DRUG_INTERACTIONS_PATCH_27B,
):
    for _drug_id, _interactions in _interactions_patch.items():
        if _drug_id in _drug_index:
            _drug_index[_drug_id]["drug_interactions"] = _interactions

# バッチ28-29: 動物種カバレッジ拡張パッチ適用
for _species_patch_batch in (SPECIES_INFO_PATCH_28, SPECIES_INFO_PATCH_29):
    for _drug_id, _species_patch in _species_patch_batch.items():
        if _drug_id in _drug_index:
            _target = _drug_index[_drug_id].setdefault("species_info", {})
            for _sp, _info in _species_patch.items():
                if _sp not in _target:
                    _target[_sp] = _info

# バッチ30: D2拮抗系の催乳作用（スルピリド新規収載＋メトクロプラミドの欠落補完）
for _drug30 in DRUGS_BATCH_30:
    if _drug30["id"] not in _drug_index:
        DRUGS.append(_drug30)
        _drug_index[_drug30["id"]] = _drug30

for _drug_id, _patch30 in METOCLOPRAMIDE_LACTATION_PATCH_30.items():
    if _drug_id in _drug_index:
        _drug_index[_drug_id].update(_patch30)

# 犬の催乳用法は既存の消化管用量を上書きせず notes に併記する（用量欄の書き換えはしない）
_metoc = _drug_index.get("metoclopramide")
if _metoc:
    _dog = (_metoc.get("species_info") or {}).get("dog")
    if isinstance(_dog, dict):
        for _key, _text in (
            ("notes_ja", METOCLOPRAMIDE_DOG_LACTATION_NOTE),
            ("notes", METOCLOPRAMIDE_DOG_LACTATION_NOTE_EN),
        ):
            _existing = _dog.get(_key) or ""
            if "29359978" not in _existing:
                _dog[_key] = f"{_existing} {_text}".strip()

# バッチ31: 麻酔プロトコルが参照するのに未収載だった麻酔関連薬6剤
# （チオペンタール, グアイフェネシン/GGE, デトミジン, メピバカイン,
#  2-フェノキシエタノール, ヨヒンビン）
for _drug31 in DRUGS_BATCH_31:
    if _drug31["id"] not in _drug_index:
        DRUGS.append(_drug31)
        _drug_index[_drug31["id"]] = _drug31

# バッチ32: 猫糖尿病の疾患エントリが推奨するのに未収載だったSGLT2阻害薬2剤
# （ベキサグリフロジン/Bexacat, ベラグリフロジン/Senvelgo — 正常血糖DKA警告付き）
for _drug32 in DRUGS_BATCH_32:
    if _drug32["id"] not in _drug_index:
        DRUGS.append(_drug32)
        _drug_index[_drug32["id"]] = _drug32

# バッチ33: 疾患治療・相互作用・麻酔プロトコルが参照するのに未収載だった14剤
# （ピリメタミン/EPM, キニジン/馬AF, バラシクロビル/EHM(猫致死警告),
#  メクリジン, コルヒチン, リュープロレリン, ナイアシンアミド, デクスラゾキサン,
#  メトトレキサート, チアミン, L-カルニチン, パロモマイシン(猫腎不全警告),
#  EMLAクリーム(猫メトヘモグロビン警告), 50%ブドウ糖(希釈警告)）
for _drug33 in DRUGS_BATCH_33:
    if _drug33["id"] not in _drug_index:
        DRUGS.append(_drug33)
        _drug_index[_drug33["id"]] = _drug33

# バッチ34: 2026-08 第2回 referenced-but-absent 監査で検出された11剤
# （ビンブラスチン/肥満細胞腫408参照, 乳酸リンゲル・ノルモソルR/輸液1,700+参照,
#  L-テアニン, α-カソゼピン, ポビドンヨード, 葉酸(妊娠馬警告), DMSO,
#  ミネラルオイル(誤嚥警告), ルゴール液/セキセイ甲状腺腫, フルオレセイン）
for _drug34 in DRUGS_BATCH_34:
    if _drug34["id"] not in _drug_index:
        DRUGS.append(_drug34)
        _drug_index[_drug34["id"]] = _drug34

# バッチ35: 2026-08 第3回 referenced-but-absent 監査で検出された15剤
# （プラリドキシム/有機リン184参照, レギュラーインスリン/DKA・高K血症16参照,
#  トリアムシノロン/馬関節内31参照, イミドカルブ/バベシア22参照,
#  サクシマーDMSA/鳥鉛キレート12参照, シドフォビル点眼/FHV-1,
#  アルベンダゾール(骨髄毒性警告), エニルコナゾール(猫グルーミング警告),
#  エスモロール, オセルタミビル(犬パルボ非推奨明記), フルルビプロフェン点眼,
#  イドクスウリジン点眼, トリクラベンダゾール/肝蛭, ジメルカプロールBAL,
#  セレコキシブ/鳥PDD）
for _drug35 in DRUGS_BATCH_35:
    if _drug35["id"] not in _drug_index:
        DRUGS.append(_drug35)
        _drug_index[_drug35["id"]] = _drug35

# バッチ36: 2026-08 第4回 referenced-but-absent 監査で検出
# （エノキサパリン/LMWH — DIC・血栓塞栓症プロトコル13疾患エントリが用量付きで参照）
for _drug36 in DRUGS_BATCH_36:
    if _drug36["id"] not in _drug_index:
        DRUGS.append(_drug36)
        _drug_index[_drug36["id"]] = _drug36

# バッチ37: 2026-08 第5回 referenced-but-absent 監査で検出
# （タウリン — 治療テキスト768参照の最多欠落、猫欠乏性DCMの根本治療;
#  カルシトニン — ウサギ/鳥のビタミンD中毒・爬虫類NSHPが用量付きで参照;
#  アンピシリン・スルバクタム — パルボ/汎白血球減少症の敗血症予防が参照）
for _drug37 in DRUGS_BATCH_37:
    if _drug37["id"] not in _drug_index:
        DRUGS.append(_drug37)
        _drug_index[_drug37["id"]] = _drug37

# バッチ38: 2026-08 第6回 referenced-but-absent 監査で検出
# （パンクレリパーゼ — 犬猫EPIフラグシップが「1 tsp/10kg/食」と用量指示するのに未収載;
#  ベンズブロマロン — 鳥/爬虫類痛風プロトコルが 5 mg/kg PO q24h で参照;
#  メトホルミン — 馬EMS/インスリン抵抗性/慢性蹄葉炎が 15-30 mg/kg で参照）
for _drug38 in DRUGS_BATCH_38:
    if _drug38["id"] not in _drug_index:
        DRUGS.append(_drug38)
        _drug_index[_drug38["id"]] = _drug38

# バッチ39: 2026-08 第7回 referenced-but-absent 監査で検出
# （プロタミン — ヘパリン/エノキサパリン/ダルテパリンの各entryが拮抗薬として名指しするのに未収載;
#  ヒドロコルチゾン — アジソンクリーゼの標準グルココルチコイドが未収載;
#  高張食塩水 — ショック/GDV/頭部外傷プロトコルが参照する少量蘇生輸液が未収載）
for _drug39 in DRUGS_BATCH_39:
    if _drug39["id"] not in _drug_index:
        DRUGS.append(_drug39)
        _drug_index[_drug39["id"]] = _drug39

# バッチ40: 2026-08 第8回 referenced-but-absent 監査で検出
# （エタンブトール — 鳥/爬虫類/犬猫の抗酸菌症多剤プロトコルが13エントリで参照するのに未収載;
#  ジヒドロストレプトマイシン — 犬ブルセラ症の古典的標準レジメンが9エントリで参照するのに未収載）
for _drug40 in DRUGS_BATCH_40:
    if _drug40["id"] not in _drug_index:
        DRUGS.append(_drug40)
        _drug_index[_drug40["id"]] = _drug40

# バッチ41: 2026-08 第9回 referenced-but-absent 監査で検出
# （ミルテホシン/メグルミンアンチモン酸塩 — 犬リーシュマニア症のLeishVet第一選択2剤が
#  用量付きで参照されるのに両方未収載; ヒト免疫グロブリンIVIG — IMHA/ITP難治例レスキューが
#  30-40参照で最多欠落; インターフェロンα — 鳥PBFD/猫レトロウイルス補助療法33参照、ω型のみ収載だった）
for _drug41 in DRUGS_BATCH_41:
    if _drug41["id"] not in _drug_index:
        DRUGS.append(_drug41)
        _drug_index[_drug41["id"]] = _drug41

# バッチ42: 2026-08 第10回 referenced-but-absent 監査で検出
# （生理食塩水0.9% — 293参照で最多欠落の輸液。高張7.2%のみ収載で等張液が無く、
#  高Ca血症・血液製剤ライン・ネブライゼーションの標準液が引けなかった;
#  コレカルシフェロール/ビタミンD3 — 上皮小体機能低下症・爬虫類NSHPが96参照、
#  活性型カルシトリオールのみ収載だった）
for _drug42 in DRUGS_BATCH_42:
    if _drug42["id"] not in _drug_index:
        DRUGS.append(_drug42)
        _drug_index[_drug42["id"]] = _drug42

# バッチ43: 2026-08 第11回 referenced-but-absent 監査で検出
# （シタラビンAra-C — MUO(GME/NME/NLE)標準補助療法が8エントリで用量付き参照されるのに未収載;
#  イミキモド5%クリーム — 馬サルコイド/耳介プラーク・猫SCC in situ の5参照。
#  MMFは既収載(mycophenolate)のため、裸の「ミコフェノール酸」表記のエイリアスのみ追加）
for _drug43 in DRUGS_BATCH_43:
    if _drug43["id"] not in _drug_index:
        DRUGS.append(_drug43)
        _drug_index[_drug43["id"]] = _drug43

# バッチ44: 2026-08 第12回 referenced-but-absent 監査で検出
# （シメチコン — 草食小型哺乳類6種のGIうっ滞/鼓脹プロトコルが40-50 mg/kg等の用量付きで
#  37参照するのに未収載; トリエンチン — 犬銅関連性肝障害のペニシラミン不耐例の
#  名指し第二選択キレート剤; オロパタジン0.1%点眼 — アレルギー性結膜炎プロトコルが参照。
#  DOCPは既収載(desoxycorticosterone)のため頭字語エイリアスのみ追加）
for _drug44 in DRUGS_BATCH_44:
    if _drug44["id"] not in _drug_index:
        DRUGS.append(_drug44)
        _drug_index[_drug44["id"]] = _drug44

# Batch 45: 2026-08監査（第14回スイープ）— referenced-but-absent 3剤
# （フィナステリド/酢酸オサテロン — 犬BPHエントリが用量付きで参照する内科治療2剤;
#  フィルグラスチム(rhG-CSF) — パルボ・免疫介在性好中球減少・トラップド
#  ニュートロフィル症候群等7エントリが「5 μg/kg SC q24h」で参照）
for _drug45 in DRUGS_BATCH_45:
    if _drug45["id"] not in _drug_index:
        DRUGS.append(_drug45)
        _drug_index[_drug45["id"]] = _drug45

# Batch 46: 2026-08監査（第15回スイープ）— referenced-but-absent 3剤
# （ジアゾキシド — インスリノーマ標準第二選択、治療テキスト44参照;
#  リバロキサバン — 猫ATE救急プロトコルのkey drugなのに経口Xa阻害薬が皆無;
#  マムシ抗毒素血清 — マムシ咬傷救急プロトコルのkey drug、日本臨床で最重要の抗毒素）
for _drug46 in DRUGS_BATCH_46:
    if _drug46["id"] not in _drug_index:
        DRUGS.append(_drug46)
        _drug_index[_drug46["id"]] = _drug46

# Batch 47: 2026-08監査（第16回スイープ）— referenced-but-absent 2剤
# （フルオロウラシル(5-FU) — 馬サルコイド/SCCの標準補助療法11参照 + 猫絶対禁忌の
#  定義的安全事実; 硫酸鉄 — 鉄欠乏性貧血の経口維持療法26参照、注射鉄のみ収載だった）
for _drug47 in DRUGS_BATCH_47:
    if _drug47["id"] not in _drug_index:
        DRUGS.append(_drug47)
        _drug_index[_drug47["id"]] = _drug47

# ---------------------------------------------------------------------------
# 動物種カバレッジ自動拡張: 類似種への自動展開で「✕」表示を低減
# bird データ → parakeet, parrot（鳥類サブグループ、薬物動態類似）
# reptile データ → lizard（爬虫類サブグループ）
# hamster データ → degu, sugar_glider（小型げっ歯類、用量参考）
# ---------------------------------------------------------------------------
_SPECIES_COPY_RULES = [
    # (source_species, target_species, note_prefix_ja, note_prefix_en)
    ("bird", "parakeet", "（鳥類データから推定）", "(extrapolated from avian data)"),
    ("bird", "parrot", "（鳥類データから推定）", "(extrapolated from avian data)"),
    ("reptile", "lizard", "（爬虫類データから推定）", "(extrapolated from reptile data)"),
    ("reptile", "snake", "（爬虫類データから推定）", "(extrapolated from reptile data)"),
    ("reptile", "tortoise", "（爬虫類データから推定）", "(extrapolated from reptile data)"),
    ("hamster", "degu", "（小型げっ歯類データから推定）", "(extrapolated from small rodent data)"),
    ("guinea_pig", "degu", "（小型げっ歯類データから推定）", "(extrapolated from small rodent data)"),
    ("hamster", "sugar_glider", "（小型哺乳類データから推定）", "(extrapolated from small mammal data)"),
    ("chinchilla", "degu", "（小型げっ歯類データから推定）", "(extrapolated from small rodent data)"),
]

for _drug in DRUGS:
    _si = _drug.setdefault("species_info", {})
    for _src, _tgt, _note_ja, _note_en in _SPECIES_COPY_RULES:
        if _src in _si and _tgt not in _si:
            _src_info = _si[_src]
            if not isinstance(_src_info, dict):
                continue
            # Copy with extrapolation note added
            _tgt_info = dict(_src_info)
            _orig_note_ja = _tgt_info.get("notes_ja", "") or ""
            _orig_note_en = _tgt_info.get("notes", "") or ""
            _tgt_info["notes_ja"] = (_note_ja + " " + _orig_note_ja).strip()
            _tgt_info["notes"] = (_note_en + " " + _orig_note_en).strip()
            _si[_tgt] = _tgt_info

# ---------------------------------------------------------------------------
# 魚類薬品の機序・禁忌・副作用補完（12魚専用薬の臨床補完）
# ---------------------------------------------------------------------------
_FISH_DRUG_PATCHES = {
    "methylene_blue": {
        "mechanism": "Antifungal/antiparasitic dye. Inhibits cellular respiration in protozoa, fungi, and external parasites; also acts as anti-methemoglobinemia agent by reducing methemoglobin to hemoglobin.",
        "mechanism_ja": "抗真菌・抗寄生虫色素。原虫、真菌、外部寄生虫の細胞呼吸阻害。メトヘモグロビンをヘモグロビンに還元する抗メトヘモグロビン血症作用も。",
        "contraindications": "Avoid in scaleless fish (catfish, loaches, eels - sensitive). Stains silicone aquarium sealant. Remove biological filtration media before use (kills nitrifying bacteria).",
        "contraindications_ja": "無鱗魚（ナマズ、ドジョウ、ウナギ — 感受性）回避。シリコン水槽シーラントを染色。生物ろ過メディアを使用前に除去（硝化細菌を殺す）。",
        "side_effects": ["Stains all surfaces", "Kills biological filtration", "Reduces oxygen levels"],
        "side_effects_ja": ["全表面染色", "生物ろ過破壊", "酸素レベル低下"],
    },
    "malachite_green": {
        "mechanism": "Triphenylmethane dye with antifungal and antiparasitic activity. Inhibits cellular respiration in eukaryotic parasites and fungi. Highly effective against Ich (Ichthyophthirius), fungus, and external parasites.",
        "mechanism_ja": "抗真菌・抗寄生虫活性のトリフェニルメタン色素。真核寄生虫・真菌の細胞呼吸を阻害。白点病、真菌、外部寄生虫に高効果。",
        "contraindications": "TOXIC TO HUMANS - carcinogenic, banned for food fish in many countries. Avoid in scaleless fish, fry, eggs. CONTRAINDICATED in fish destined for human consumption. Toxic to invertebrates.",
        "contraindications_ja": "ヒトに毒性 — 発がん性、多くの国で食用魚に禁止。無鱗魚、稚魚、卵に回避。食用魚に禁忌。無脊椎動物に毒性。",
        "side_effects": ["Carcinogenic to humans", "Mutagenic", "Toxic to invertebrates", "Stains permanent"],
        "side_effects_ja": ["ヒト発がん性", "変異原性", "無脊椎動物に毒性", "永久染色"],
    },
    "formalin_fish": {
        "mechanism": "37% formaldehyde solution. Strong protein denaturant kills external parasites by cross-linking cellular proteins. Effective against monogenean flukes, protozoan parasites, and external fungi.",
        "mechanism_ja": "37%ホルムアルデヒド溶液。強力なタンパク質変性剤で細胞タンパク質架橋により外部寄生虫を殺す。単生類吸虫、原虫寄生虫、外部真菌に有効。",
        "contraindications": "TOXIC TO HUMANS - carcinogenic, requires PPE. Causes severe oxygen depletion in water (use only with strong aeration). Toxic to scaleless fish (catfish, loaches), young fish, sturgeon. CONTRAINDICATED with cold water (<15°C - delayed metabolism).",
        "contraindications_ja": "ヒトに毒性 — 発がん性、PPE要。水中で重度酸素枯渇（強力エアレーション併用必須）。無鱗魚（ナマズ、ドジョウ）、若魚、チョウザメに毒性。冷水（<15℃ — 代謝遅延）に禁忌。",
        "side_effects": ["Severe O2 depletion", "Human carcinogen", "Gill irritation"],
        "side_effects_ja": ["重度酸素枯渇", "ヒト発がん性", "鰓刺激"],
    },
    "copper_sulfate": {
        "mechanism": "Copper ion (Cu²⁺) is toxic to external parasites (especially Cryptocaryon irritans in marine fish), fungi, and algae. Disrupts cellular ion transport and enzyme function in lower organisms.",
        "mechanism_ja": "銅イオン（Cu²⁺）が外部寄生虫（特に海水魚のクリプトカリオン）、真菌、藻類に毒性。下等生物の細胞イオン輸送・酵素機能を阻害。",
        "contraindications": "CONTRAINDICATED in invertebrate tanks (lethal to corals, shrimp, snails). Toxic to scaleless fish, young fish, and elasmobranchs (sharks/rays). Maintain Cu level 0.15-0.20 ppm via test kit - higher doses fatal. Bonds with carbonates (KH) - effective dose varies with water chemistry.",
        "contraindications_ja": "無脊椎動物水槽に禁忌（サンゴ、エビ、貝に致死的）。無鱗魚、若魚、軟骨魚類（サメ・エイ）に毒性。テストキットでCuレベル0.15-0.20 ppm維持 — 高用量で致死的。炭酸塩（KH）と結合 — 効果用量は水化学で変動。",
        "side_effects": [
            "Toxic to invertebrates",
            "Narrow safety margin",
            "Gill damage if overdosed",
            "Suppresses immune function",
        ],
        "side_effects_ja": ["無脊椎動物に毒性", "安全域狭い", "過量で鰓損傷", "免疫機能抑制"],
    },
    "potassium_permanganate": {
        "mechanism": "Strong oxidizing agent. Destroys external parasites, bacteria, and fungi via oxidative damage to cell membranes and proteins. Effective broad-spectrum disinfectant for ponds and bath treatment.",
        "mechanism_ja": "強力な酸化剤。細胞膜・タンパク質への酸化的損傷を介して外部寄生虫、細菌、真菌を破壊。池・薬浴用の有効広域消毒剤。",
        "contraindications": "Inactivated by organic matter (waste, plants - reduces effectiveness). Toxic to scaleless fish at standard doses. CAUTION in stocked ponds - rapid depletion of dissolved oxygen possible. Stains skin, equipment.",
        "contraindications_ja": "有機物（廃棄物、植物 — 効果低下）で不活化。標準用量で無鱗魚に毒性。放養池注意 — 溶存酸素急速枯渇可能。皮膚・器具染色。",
        "side_effects": ["Organic matter inactivation", "O2 depletion", "Skin staining", "Gill damage if overdosed"],
        "side_effects_ja": ["有機物による不活化", "酸素枯渇", "皮膚染色", "過量で鰓損傷"],
    },
    "acriflavine": {
        "mechanism": "Acridine dye with antibacterial and antiparasitic activity. Intercalates with bacterial DNA, inhibiting replication. Active against external fungi, bacteria, and some protozoan parasites.",
        "mechanism_ja": "抗菌・抗寄生虫活性のアクリジン色素。細菌DNAにインターカレートし複製阻害。外部真菌、細菌、一部原虫寄生虫に活性。",
        "contraindications": "May cause photosensitization in fish - reduce light during treatment. Stains equipment and water yellow. Mutagenic in bacterial assays. Avoid in invertebrate tanks. Reduce dose in soft acidic water.",
        "contraindications_ja": "魚で光感作性可能 — 治療中光低減。器具・水を黄色に染色。細菌試験で変異原性。無脊椎動物水槽回避。軟酸性水で減量。",
        "side_effects": ["Photosensitization", "Yellow staining", "Mutagenic potential"],
        "side_effects_ja": ["光感作性", "黄色染色", "変異原性"],
    },
    "oxylinic_acid": {
        "mechanism": "First-generation fluoroquinolone antibacterial. Inhibits bacterial DNA gyrase, preventing DNA replication. Effective against gram-negative pathogens including Aeromonas, Pseudomonas, Vibrio in aquaculture.",
        "mechanism_ja": "第一世代フルオロキノロン系抗菌薬。細菌DNAジャイレース阻害でDNA複製阻止。養殖におけるAeromonas、Pseudomonas、Vibrio等のグラム陰性病原体に有効。",
        "contraindications": "Bacterial resistance developing - use only when culture-confirmed susceptible. Maximum residue limits in food fish - observe withdrawal period (typically 14-30 days). Avoid in young fish (cartilage effects). Not permitted in some countries.",
        "contraindications_ja": "細菌耐性発達中 — 培養感受性確認時のみ使用。食用魚で最大残留量 — 休薬期間遵守（典型的に14-30日）。若魚回避（軟骨影響）。一部の国で許可されない。",
        "side_effects": ["Resistance development", "Withdrawal period required", "Cartilage effects in young"],
        "side_effects_ja": ["耐性発達", "休薬期間要", "若齢で軟骨影響"],
    },
    "kanamycin_fish": {
        "mechanism": "Aminoglycoside antibiotic for bath/feed treatment. Binds bacterial 30S ribosomal subunit, inhibiting protein synthesis. Effective against gram-negative bacterial septicemias (Aeromonas, Pseudomonas, Vibrio).",
        "mechanism_ja": "薬浴/餌料用アミノグリコシド系抗菌薬。細菌30Sリボソームサブユニットに結合しタンパク質合成阻害。グラム陰性敗血症（Aeromonas、Pseudomonas、Vibrio）に有効。",
        "contraindications": "Bath treatment less effective than feed-medicated due to limited absorption through gills. Avoid concurrent use with other ototoxic/nephrotoxic agents. Bacterial resistance increasing. Withdrawal period in food fish (30+ days).",
        "contraindications_ja": "鰓からの吸収限定的のため薬浴は薬餌より効果劣。他の耳毒性/腎毒性薬剤の同時使用回避。細菌耐性増加。食用魚で休薬期間（30日以上）。",
        "side_effects": [
            "Limited bath absorption",
            "Bacterial resistance",
            "Cross-resistance with other aminoglycosides",
        ],
        "side_effects_ja": ["薬浴吸収限定", "細菌耐性", "他アミノグリコシドとの交差耐性"],
    },
    "trichlorfon": {
        "mechanism": "Organophosphate insecticide/antiparasitic. Irreversibly inhibits acetylcholinesterase in arthropod parasites (anchor worm, fish lice, gill copepods), causing paralysis and death.",
        "mechanism_ja": "有機リン系殺虫・抗寄生虫薬。節足動物寄生虫（イカリムシ、ウオジラミ、鰓カイアシ類）のアセチルコリンエステラーゼを不可逆的阻害し麻痺・死亡を起こす。",
        "contraindications": "TOXIC TO HUMANS - cholinesterase inhibitor, requires PPE. Avoid in salmonids, sturgeon, scaleless fish (high sensitivity). CONTRAINDICATED with invertebrate tanks. Banned in food fish in many countries. Toxic to bees if drift to surface water.",
        "contraindications_ja": "ヒトに毒性 — コリンエステラーゼ阻害、PPE要。サケ科、チョウザメ、無鱗魚（高感受性）回避。無脊椎動物水槽に禁忌。多くの国で食用魚に禁止。表層水に流入時にハチに毒性。",
        "side_effects": ["Human cholinesterase inhibition", "Salmonid toxicity", "Invertebrate toxicity"],
        "side_effects_ja": ["ヒトコリンエステラーゼ阻害", "サケ科に毒性", "無脊椎動物に毒性"],
    },
    "levamisole_fish": {
        "mechanism": "Imidothiazole anthelmintic. Acts as nicotinic acetylcholine receptor agonist in nematodes, causing paralysis. Also has immunostimulant effects in fish. Treatment for internal nematodes (Camallanus, Capillaria) and external monogeneans.",
        "mechanism_ja": "イミドチアゾール系駆虫薬。線虫のニコチン性アセチルコリン受容体作動薬として作用し麻痺を起こす。魚で免疫刺激作用も。内部線虫（Camallanus、Capillaria）・外部単生類治療。",
        "contraindications": "Avoid in scaleless fish (catfish, eels - sensitive to absorption). Bath treatment effective but oral/feed delivery preferred for internal parasites. Withdrawal period in food fish (typically 7-14 days). Caution with chemoreceptor stress (fast or anesthetized fish).",
        "contraindications_ja": "無鱗魚（ナマズ、ウナギ — 吸収感受性）回避。薬浴有効だが内部寄生虫には経口/餌料投与好ましい。食用魚で休薬期間（典型的に7-14日）。化学受容器ストレス（絶食または麻酔魚）注意。",
        "side_effects": ["Catfish/eel sensitivity", "Withdrawal period required", "Less effective vs cestodes"],
        "side_effects_ja": ["ナマズ/ウナギ感受性", "休薬期間要", "条虫類に効果劣"],
    },
    "epsom_salt_fish": {
        "mechanism": "Magnesium sulfate. Osmotic laxative and muscle relaxant for fish. Effective for swim bladder issues, constipation, and stress reduction. Reduces internal swelling and assists with dropsy management.",
        "mechanism_ja": "硫酸マグネシウム。魚用浸透圧下剤・筋弛緩剤。浮き袋障害、便秘、ストレス軽減に有効。内部腫脹軽減、松かさ病管理補助。",
        "contraindications": "Avoid prolonged use (electrolyte imbalance). Reduce dose for soft water fish. Not for marine fish (already high Mg in seawater). Use food-grade epsom salt only (not bath salts with fragrances).",
        "contraindications_ja": "長期使用回避（電解質バランス異常）。軟水魚で減量。海水魚に不要（海水は既に高Mg）。食品グレードエプソムソルトのみ使用（香料付きバスソルト不可）。",
        "side_effects": ["Electrolyte imbalance with prolonged use", "Lethargy at high doses"],
        "side_effects_ja": ["長期使用で電解質異常", "高用量で元気消失"],
    },
    "epsom_salt": {
        "mechanism": "Magnesium sulfate (MgSO₄). Osmotic laxative drawing water into intestinal lumen; muscle relaxant via membrane stabilization; bath/soak for limb edema, abscess drainage. Less commonly used as parenteral magnesium replacement in hypomagnesemia.",
        "mechanism_ja": "硫酸マグネシウム（MgSO₄）。腸管内腔に水分を引き込む浸透圧下剤；膜安定化による筋弛緩；四肢浮腫、膿瘍排液の薬浴/浸漬。低Mg血症の非経口Mg補充にも使用。",
        "contraindications": "Avoid oral use in renal failure (Mg retention). IV use requires slow administration (bradycardia, hypotension risk). Topical use safe but avoid open wounds. CAUTION in heart disease (Mg can cause arrhythmias at high doses).",
        "contraindications_ja": "腎不全で経口使用回避（Mg貯留）。IV使用は緩徐投与要（徐脈、低血圧リスク）。局所使用は安全だが開創回避。心疾患注意（高用量でMgが不整脈起こしうる）。",
        "side_effects": ["Diarrhea (oral)", "Bradycardia (IV)", "Hypotension (IV)", "Hypermagnesemia"],
        "side_effects_ja": ["下痢（経口）", "徐脈（IV）", "低血圧（IV）", "高Mg血症"],
    },
    "aquarium_salt": {
        "mechanism": "Sodium chloride (NaCl) - osmoregulatory supplement for freshwater fish. Reduces osmotic stress, increases slime coat production, and is mildly antiparasitic against protozoans and external parasites at higher concentrations.",
        "mechanism_ja": "塩化ナトリウム（NaCl）— 淡水魚の浸透圧調節補助。浸透圧ストレス低減、粘液層産生増加、高濃度で原虫・外部寄生虫に軽度の抗寄生虫作用。",
        "contraindications": "AVOID in salt-sensitive species: catfish, loaches, tetras (some), goldfish (long-term), live plants (kill at >2 ppt sustained). Brackish water fish may need salt. NEVER use iodized table salt (contains additives toxic to fish). Use aquarium-grade or non-iodized rock salt only.",
        "contraindications_ja": "塩感受性種に回避：ナマズ、ドジョウ、テトラ（一部）、金魚（長期）、生きた植物（>2 ppt持続で枯死）。汽水魚は塩必要可能性。ヨウ素添加食卓塩絶対不可（魚毒性添加物含有）。水族館グレードまたは非ヨウ素岩塩のみ使用。",
        "side_effects": ["Plant toxicity", "Loach/catfish sensitivity", "Long-term goldfish issues"],
        "side_effects_ja": ["植物毒性", "ドジョウ/ナマズ感受性", "金魚長期問題"],
    },
}

# Apply fish drug patches
for _fish_id, _patch in _FISH_DRUG_PATCHES.items():
    if _fish_id in _drug_index:
        _drug = _drug_index[_fish_id]
        for _key, _value in _patch.items():
            if _key not in _drug or not _drug[_key]:
                _drug[_key] = _value

# ---------------------------------------------------------------------------
# species_info の正規化（表示層が読むキーに揃える）
#
# 背景: 後期バッチの species_info は用量キーに `dose`（および `dose_ja`）を使い、
# `safe` を持たない。一方フロントは `dosage`/`dosage_ja` しか読まず、
# `info.safe ? "✓" : "✗"` で可否を描画する。結果として **610薬品中336薬品(55%)**
# で「用量が空欄のまま ✗」と表示されていた。獣医師には「その種には使えない」と
# 読めてしまい、実際には用量が存在するため臨床的に危険な誤表示だった
# （例: ガバペンチンが犬猫馬を含む全種で ✗）。
#
# 正規化の方針:
#   - `dose`/`dose_ja` は `dosage`/`dosage_ja` が無いときだけ移送（既存値は不変）
#   - `safe` が明示されていれば尊重する（意図的な safe=False 202件は ✗ のまま）
#   - `safe` 未指定でその種の用量があるなら True。用量が載っている＝その種で
#     使用される、という意味だから。
#   - ただし **notes が禁忌を示す場合は絶対に True にしない**。ここを機械的に
#     True にすると「過酸化水素（催吐）は猫に禁忌・重度出血性胃炎」のエントリが
#     猫で ✓ になり、警告が推奨に反転する（実際に作り込んで安全テストが検出した）。
#     禁忌が疑われる場合は `safe` を付けない＝✗ のまま notes を読ませる方に倒す。
#     「NSAIDs が禁忌の症例に」等の他剤への言及は誤検出なので除外する。
#   - 用量が無い場合も `safe` を作らない（不明を「安全」と偽らない）
# ---------------------------------------------------------------------------

# 他剤・他経路への言及であって、その種の禁忌ではないもの（tests/test_drug_safety.py と同一基準）
_CONTRA_FALSE_POSITIVES = (
    "where nsaids are contraindicated",
    "nsaids are contraindicated",
    "nsaids contraindicated",
    "nsaids禁忌",
    "nsaid禁忌",
    "parenteral only",
    "注射剤のみ",
    "経口投与は絶対禁忌",
)


# 「本種では確立されていない」等は用量ではない。ここを safe=True にすると
# 「✓ 確立されていない」という矛盾表示になり、使えると誤読される。
_UNESTABLISHED_DOSE = re.compile(
    r"not established|not well established|確立されていない|not commonly needed|通常は不要|unknown|不明|データなし|no data",
    re.I,
)


def _dose_is_unestablished(info: Dict[str, Any]) -> bool:
    text = f"{info.get('dosage', '') or ''} {info.get('dosage_ja', '') or ''}"
    return bool(_UNESTABLISHED_DOSE.search(text))


def _notes_flag_contraindication(info: Dict[str, Any]) -> bool:
    notes = f"{info.get('notes', '') or ''} {info.get('notes_ja', '') or ''}"
    if "CONTRAINDICATED" not in notes.upper() and "禁忌" not in notes:
        return False
    lowered = notes.lower()
    return not any(fp in lowered for fp in _CONTRA_FALSE_POSITIVES)


for _drug in DRUGS:
    for _sp, _info in (_drug.get("species_info") or {}).items():
        if not isinstance(_info, dict):
            continue
        if not _info.get("dosage") and _info.get("dose"):
            _info["dosage"] = _info["dose"]
        if not _info.get("dosage_ja") and _info.get("dose_ja"):
            _info["dosage_ja"] = _info["dose_ja"]
        if (
            "safe" not in _info
            and (_info.get("dosage") or _info.get("dosage_ja"))
            and not _notes_flag_contraindication(_info)
            and not _dose_is_unestablished(_info)
        ):
            _info["safe"] = True

# ---------------------------------------------------------------------------
# 重複薬品の論理統合（物理削除しない）
#
# 疾患側の T103 と同じ問題が薬品辞書にもあった: 同一薬が複数エントリに分割され、
# 610薬品中 95グループ・111件が重複していた（例: ガバペンチンが Gabapentin /
# (Chronic Pain) / (Oral Analgesic) の3件）。利用者には同じ薬が別物として並び、
# 種カバレッジも分散する。
#
# 統合の安全規則:
#   - 正規エントリ（種数が最多＝最も情報量が多いもの）の用量は **絶対に上書きしない**。
#     変種側からは「正規エントリが持っていない動物種」だけを取り込む＝カバレッジは
#     増えるだけで、獣医レビュー済みの用量が書き換わることはない。
#   - 統合対象は (a) name が完全一致する純粋な重複 と (b) 獣医の明示指示がある
#     同一薬の別名エントリ のみ。投与経路や剤形で用量が本質的に異なりうる変種
#     （例: 局所 vs IV）は自動統合しない。
#   - ソースの .py は無改変。統合はロード時のみ＝サイドカーを消す感覚で即ロールバック可。
#   - 旧 id は _DRUG_ALIAS_TO_ID で正規 id に解決する（既存URL・ブックマークは維持）。
# ---------------------------------------------------------------------------

# 獣医の明示指示による同一薬統合（canonical_id: [統合される id]）
_DRUG_CURATED_MERGE: dict[str, list[str]] = {
    # ガバペンチン: 適応名違いで3分割されていた（獣医指摘により統合）
    "gabapentin": ["gabapentin_pain", "gabapentin_oral"],
}


def _merge_drug_into(canonical: Dict[str, Any], variant: Dict[str, Any]) -> None:
    """変種を正規エントリへ非破壊的に取り込む（正規側の既存値は不変）。"""
    c_si = canonical.setdefault("species_info", {})
    for _sp, _info in (variant.get("species_info") or {}).items():
        if _sp not in c_si and isinstance(_info, dict):
            c_si[_sp] = _info
    # 正規側が欠いているスカラー項目のみ補完
    for _key in (
        "mechanism",
        "mechanism_ja",
        "contraindications",
        "contraindications_ja",
        "side_effects",
        "side_effects_ja",
    ):
        if not canonical.get(_key) and variant.get(_key):
            canonical[_key] = variant[_key]
    # 相互作用は和集合（薬剤名で重複排除）
    if variant.get("drug_interactions"):
        seen = {str(i.get("drug", "")).lower() for i in canonical.get("drug_interactions", []) if isinstance(i, dict)}
        merged = list(canonical.get("drug_interactions") or [])
        for _i in variant["drug_interactions"]:
            if isinstance(_i, dict) and str(_i.get("drug", "")).lower() not in seen:
                merged.append(_i)
                seen.add(str(_i.get("drug", "")).lower())
        canonical["drug_interactions"] = merged
    aliases = canonical.setdefault("aliases", [])
    for _a in (variant.get("id"), variant.get("name"), variant.get("name_ja")):
        if _a and _a not in aliases:
            aliases.append(_a)


def _consolidate_duplicate_drugs() -> Dict[str, str]:
    """同一薬の重複を論理統合し、旧 id → 正規 id の別名表を返す。"""
    by_id = {d["id"]: d for d in DRUGS if d.get("id")}
    merged_away: dict[str, str] = {}

    groups: list[tuple[str, list[str]]] = []
    # (a) name 完全一致の重複
    _by_name: dict[str, list[Dict[str, Any]]] = {}
    for _d in DRUGS:
        _by_name.setdefault(str(_d.get("name", "")).strip().lower(), []).append(_d)
    for _name, _entries in _by_name.items():
        if len(_entries) < 2 or not _name:
            continue
        # 種数が最多のものを正規に（同数なら先勝ち＝定義順を尊重）
        _ranked = sorted(_entries, key=lambda d: -len(d.get("species_info") or {}))
        groups.append((_ranked[0]["id"], [e["id"] for e in _ranked[1:]]))
    # (b) 獣医の明示指示
    for _cid, _vids in _DRUG_CURATED_MERGE.items():
        if _cid in by_id:
            groups.append((_cid, [v for v in _vids if v in by_id]))

    for _cid, _vids in groups:
        canonical = by_id.get(_cid)
        if canonical is None:
            continue
        for _vid in _vids:
            variant = by_id.get(_vid)
            if variant is None or _vid == _cid or _vid in merged_away:
                continue
            _merge_drug_into(canonical, variant)
            merged_away[_vid] = _cid

    if merged_away:
        _keep = [d for d in DRUGS if d.get("id") not in merged_away]
        DRUGS[:] = _keep
    return merged_away


_DRUG_ALIAS_TO_ID: Dict[str, str] = _consolidate_duplicate_drugs()

# 獣医師がフォーミュラリから記入し published にした用量のみを適用する
# （api/drug_dosage_overrides.py の fail-closed ゲート）。未記入・出典なしは無視されるので、
# 何も承認されていない現状では完全な no-op。
try:
    from api.drug_dosage_overrides import apply_dosage_overrides as _apply_dosage_overrides

    _DOSAGE_OVERRIDES_APPLIED = _apply_dosage_overrides(DRUGS)
except ImportError:  # pragma: no cover - optional module
    _DOSAGE_OVERRIDES_APPLIED = 0

# dosage はあるが dosage_ja が欠落した species_info エントリを決定論的に補完する。
# 数値・単位は保持し、投与経路・投与間隔の英語略号のみ日本語化（自由文は変換しない）。
# 日本語UIで英語略号（PO/q12h 等）が露出していた問題を解消する。
try:
    from api.drug_dosage_localizer import fill_missing_dosage_ja as _fill_missing_dosage_ja

    _DOSAGE_JA_FILLED = _fill_missing_dosage_ja(DRUGS)
except ImportError:  # pragma: no cover - optional module
    _DOSAGE_JA_FILLED = 0

# 統合後にインデックスを貼り直す（以降の参照は正規エントリのみを見る）
_drug_index = {d["id"]: d for d in DRUGS if d.get("id")}

# ---------------------------------------------------------------------------
# 検索テキスト正規化（かな・全角半角ゆれの吸収）
# 「ばいとりる」「ﾊﾞｲﾄﾘﾙ」「ＢＡＹＴＲＩＬ」のような入力ゆれでも一致するよう、
# NFKC 正規化 + 小文字化 + ひらがな→カタカナ変換で照合する。
# ---------------------------------------------------------------------------
_HIRAGANA_TO_KATAKANA = str.maketrans({chr(c): chr(c + 0x60) for c in range(0x3041, 0x3097)})


def _normalize_search_text(text: str) -> str:
    """検索照合用にテキストを正規化する（NFKC + 小文字 + ひらがな→カタカナ）。"""
    return unicodedata.normalize("NFKC", text or "").lower().translate(_HIRAGANA_TO_KATAKANA)


# ---------------------------------------------------------------------------
# 商品名エイリアスの適用（drug_brand_names.py の登録簿）
# 「バイトリル」のような日本の商品名で検索・テキストマッチできるよう、
# name / name_ja に含まれない別名だけを search_aliases に追記する。
# 統合（_consolidate_duplicate_drugs）後・キーワード索引構築前に適用すること。
# ---------------------------------------------------------------------------
for _drug_id, _brand_aliases in BRAND_NAME_ALIASES.items():
    _entry = _drug_index.get(_DRUG_ALIAS_TO_ID.get(_drug_id, _drug_id))
    if _entry is None:
        continue
    # スキップ判定は括弧前ステムに限定する: キーワード索引は括弧サフィックスを
    # 剥がすため、「PZIインスリン（プロジンク）」のように括弧内にだけ載る商品名は
    # 実際には索引に到達しない。フルネーム基準でスキップすると、こうした商品名が
    # search_aliases にも索引にも入らず永久に解決不能になる（プロジンク 41参照）。
    _own_names = _normalize_search_text(
        f"{re.split(r'[（(]', _entry.get('name', ''))[0]} {re.split(r'[（(]', _entry.get('name_ja', ''))[0]}"
    )
    _alias_list = _entry.setdefault("search_aliases", [])
    _existing_aliases = {_normalize_search_text(a) for a in _alias_list}
    for _alias in _brand_aliases:
        _norm = _normalize_search_text(_alias)
        if _norm and _norm not in _own_names and _norm not in _existing_aliases:
            _alias_list.append(_alias)
            _existing_aliases.add(_norm)


def resolve_drug_id(drug_id: str) -> str:
    """旧 id（統合された薬品）を正規 id に解決する。未知の id はそのまま返す。"""
    return _DRUG_ALIAS_TO_ID.get(drug_id, drug_id)


# Pre-compute drug count per category (O(n) once instead of O(categories×n) per request)
_DRUG_COUNT_BY_CATEGORY: dict[str, int] = {}
for _d in DRUGS:
    _cat = _d.get("category", "")
    _DRUG_COUNT_BY_CATEGORY[_cat] = _DRUG_COUNT_BY_CATEGORY.get(_cat, 0) + 1

# ---------------------------------------------------------------------------
# 検索・フィルタ関数
# ---------------------------------------------------------------------------


# Drug name index for fast lookup (built once at module load).
# Each entry: lowercase keyword → drug ID
_DRUG_KEYWORD_INDEX: dict[str, str] = {}


# Generic English words that appear as the first word of compound drug names
# ("Vitamin K1", "Critical Care Herbivore", "Sodium Nitroprusside" …). Bare, they
# match unrelated prose ("critical care monitoring", "sodium restriction",
# "vitamin supplementation") and surface the wrong related-drug chip — the full
# compound name stays indexed, only the bare generic word is skipped.
_FIRST_WORD_STOPLIST = {
    "activated",
    "aluminum",
    "amino",
    "aquarium",
    "artificial",
    "calcium",
    "canine",
    "carnivore",
    "copper",
    "critical",
    "fish",
    "iron",
    "lactated",
    "liquid",
    "magnesium",
    "medical",
    "milk",
    "mineral",
    "oral",
    "potassium",
    "silver",
    "sodium",
    "vitamin",
    "zinc",
}

# Derived stems that are generic clinical phrases, not drug references
# ("Critical Care (Oxbow)" → stem "critical care" would match "critical care
# monitoring" in any emergency protocol). ジョイント/アンチオキシダント are ECVN
# product-name fragments that would surface sponsor chips from generic prose;
# ビタミンb would wrongly map ビタミンB1 (thiamine) mentions to the B12 entry.
_GENERIC_STEM_STOPLIST = {"critical care", "ジョイント", "アンチオキシダント", "ビタミンb"}

# Paren-inner brand names ("フルニキシンメグルミン（バナミン）" → バナミン) are
# indexed at the lowest tier so treatment texts citing the Japanese brand alone
# resolve ("プロジンク 0.5 IU", "セレニア 1 mg/kg"). Only pure-katakana parts are
# indexed — Latin paren parts are dominated by generic English words (oral,
# renal, saline) that would false-match English prose. Generic katakana words
# that appear inside name parens but also in ordinary prose are excluded here.
_PAREN_PART_STOPLIST = {
    "エキゾチック",  # (エキゾチック用) descriptors
    "インプラント",  # dose-form word — "ホルモンインプラント" prose would false-chip
    "プログラム",  # Program (lufenuron) — "リハビリプログラム" prose collision
    "メトロノミック",  # metronomic-chemo term, not a brand
    # Valium transliteration inside diazepam's paren — but バリウム in vet texts
    # is barium contrast (バリウム造影, 104 content refs), never the brand.
    "バリウム",
}
_PURE_KATAKANA_RE = re.compile(r"^[ァ-ヴー]{4,}$")

# Case-sensitive product references: treatment texts name the Oxbow syringe-feed
# product as capitalised "Critical Care" (1,000+ entries), while generic prose
# ("critical care monitoring") is lowercase — case distinguishes them where the
# lowercased index cannot.
_CASE_SENSITIVE_KEYWORDS = {"Critical Care": "critical_care_herbivore"}

# Keyword-level negative contexts: an occurrence that falls inside one of
# these longer strings is not a drug mention. 生食 (clinical shorthand for
# saline) must not fire inside ガス産生食物 (gas-producing food) or 生食用/
# 生食物 (raw-food senses).
_KEYWORD_NEGATIVE_CONTEXTS: dict[str, tuple[str, ...]] = {
    "生食": ("産生食", "生食物", "生食用"),
}


# Legitimate katakana spelling variants that disease treatment texts use but
# that differ from the formulary's canonical name_ja. Without these the
# treatment-text → related-drug chips silently fail to resolve (e.g. 64
# occurrences of デキサメサゾン never linked to dexamethasone). Only genuine
# alternate spellings belong here — typos in content are fixed in the content.
_KATAKANA_VARIANT_ALIASES: dict[str, tuple[str, ...]] = {
    "dexamethasone": ("デキサメサゾン",),  # canonical: デキサメタゾン
    "nystatin": ("ニスタチン",),  # canonical: ナイスタチン
    "silver_sulfadiazine": ("シルバースルファジアジン",),  # canonical: スルファジアジン銀
    "sulfasalazine": ("スルファサラジン",),  # canonical: サラゾスルファピリジン
    "fomepizole": ("フォメピゾール",),  # canonical: ホメピゾール
    "methimazole": ("チアマゾール",),  # thiamazole = INN of methimazole
    "penicillin_g": (
        "プロカインペニシリン",
        "ペニシリン",
    ),  # procaine formulation / bare class-archetype (732 treatment refs incl. guinea-pig contraindication notes)
    "l_carnitine": ("カルニチン",),  # canonical: L-カルニチン
    "salbutamol": ("アルブテロール",),  # albuterol = USAN of salbutamol
    "leuprolide": ("リュープロリド",),  # canonical: リュープロレリン酢酸塩
    "darbepoetin": ("ダーベポエチン",),  # canonical: ダルベポエチンアルファ
    "thiamine_b1": (
        "ビタミンb1",
    ),  # canonical: チアミン（ビタミンB1） — bare "ビタミンB1" must resolve to thiamine, never the B12 entry
    # 2026-08 sweep #6: treatment texts cite these agents by bare/variant
    # spellings that the canonical name_ja never reduces to.
    "flunixin": ("フルニキシン",),  # canonical: フルニキシンメグルミン（バナミン） — 198 bare refs
    "n_acetylcysteine": ("アセチルシステイン",),  # canonical: N-アセチルシステイン — 131 bare refs
    "dextrose_50": ("デキストロース",),  # canonical: 50%ブドウ糖（デキストロース）注射液
    "amphotericin_b": ("アンホテリシンb",),  # ン variant of アムホテリシンB
    "rifampin": ("リファンピシン",),  # rifampicin = INN; canonical name_ja is リファンピン
    "sulfadimethoxine": ("サルファジメトキシン",),  # サル variant of スルファジメトキシン
    "interferon_omega": (
        "インターフェロンオメガ",
        "インターフェロンω",
    ),  # canonical: 猫インターフェロンオメガ（…） — texts omit the 猫 prefix / use ω
    "pyrimethamine": ("ピリメサミン",),  # サ transliteration variant of ピリメタミン
    "alpha_casozepine": ("α-カソゼピン",),  # canonical: αカソゼピン（ジルケーン） — texts hyphenate
    # 2026-08 sweep #7: treatment texts cite these agents by variant spellings
    # that the canonical name_ja never reduces to.
    "dopamine": ("ドーパミン",),  # long-vowel variant of ドパミン — 19 treatment refs
    "sodium_bicarbonate": ("重炭酸ナトリウム",),  # canonical: 炭酸水素ナトリウム
    "vitamin_k1": ("フィトナジオン",),  # phytonadione = INN of vitamin K1
    "calcium_gluconate": ("カルシウムグルコネート",),  # canonical: グルコン酸カルシウム
    "ursodiol": ("ウルソジオール",),  # canonical: ウルソデオキシコール酸
    "calcium_supplement_reptile": (
        "炭酸カルシウム",
    ),  # canonical: 炭酸カルシウム粉末（爬虫類用） — 粉末 suffix defeats the stem index (13 treatment refs)
    # 2026-08 sweep #8: variant spellings in anesthesia/treatment texts.
    "atipamezole": ("アティパメゾール",),  # ティ variant of アチパメゾール — emergency-kit refs
    "milbemycin_oxime": (
        "ミルベマイシン",
    ),  # canonical: ミルベマイシンオキシム — texts cite the bare stem (ミルベマイシンA錠 等)
    # 2026-08 sweep #11: SARDS/IMHA texts cite bare "ミコフェノール酸 20 mg/kg"
    # (without モフェチル) — the full canonical name never reduces to the acid stem.
    "mycophenolate": ("ミコフェノール酸", "ミコフェノレート"),
    # 2026-08 sweep #12: Addison's texts cite the acronym "DOCP" alone — the
    # canonical name only carries it inside a paren suffix, which the stem index
    # strips. デソキシ/デスオキシ are transliteration variants of デオキシ.
    "desoxycorticosterone": ("DOCP", "デソキシコルチコステロン", "デスオキシコルチコステロン"),
    # 2026-08 sweep #13: chelation / hepatoprotectant / fluid texts cite these
    # acronyms and variant word orders that the canonical names never reduce to.
    "calcium_edta": ("CaEDTA",),  # canonical: カルシウムEDTA — 51 treatment refs cite the acronym
    # ursodiol already aliases ウルソジオール above; UDCA is the standard clinical
    # acronym (41 treatment refs: "UDCA 10-15 mg/kg PO q24h").
    "hetastarch": ("ヘタスターチ",),  # canonical: ヒドロキシエチルデンプン（HES 6%）
    # 2026-08 sweep #15: equine navicular/ringbone texts cite tiludronate by the
    # ティ/チ transliteration variants — canonical name_ja is チルドロン酸（チルドレン）.
    "tiludronate": ("ティルドロネート", "チルドロネート"),
    # Diabetes texts cite insulin analogues by the bare INN stem without the
    # インスリン prefix ("グラルギン 1 U SC q12h") — the lead-word index only
    # carries インスリン, which is too generic to map to a specific analogue.
    "insulin_glargine": ("グラルギン",),
    "insulin_detemir": ("デテミル",),
    # プロジンク must map to the dedicated PZI entry, not the umbrella
    # insulin_vetsulin entry whose paren list also names ProZinc (tier-2
    # beats the paren-brand tier-4 first-wins ordering).
    "insulin_pzi": ("プロジンク",),
    # canonical: グルコン酸カルシウム — texts also write the reversed word order
    # "カルシウムグルコン酸(塩)" (21 refs, horse hypocalcemia / amphibian MBD).
    # Bare prefix covers both 酸 and 酸塩 endings via substring match.
    # 2026-08 sweep #15: treatment texts cite these agents by transliteration /
    # word-order variants the canonical names never reduce to.
    # （tiludronate ティルドロネート/チルドロネート は上に収載済み）
    # 救急プロトコルのkey drug表記（"グルコン酸Ca10%" / "Plasmalyte"）は
    # 正準名（グルコン酸カルシウム / Plasma-Lyte A）に還元されない。
    "normosol_r": ("プラズマライト", "plasmalyte"),
    "selenium_vitamin_e": (
        "セレン酸ナトリウム",
        "亜セレン酸ナトリウム",
    ),  # white-muscle-disease texts cite the sodium selenite salt (9 refs)
}
# canonical: スルファジアジン銀 — texts write the reversed word order
# "銀スルファジアジン" (47 refs, burn/wound care) which resolved to the plain
# systemic sulfadiazine entry instead of the topical silver product. Registry
# key already exists above (ruff F601 guard), so extend here.
_KATAKANA_VARIANT_ALIASES["silver_sulfadiazine"] = _KATAKANA_VARIANT_ALIASES["silver_sulfadiazine"] + (
    "銀スルファジアジン",
)
# UDCA acronym for ursodiol (registry key already exists above, so extend here
# rather than duplicating the dict key — ruff F601 guard).
_KATAKANA_VARIANT_ALIASES["ursodiol"] = _KATAKANA_VARIANT_ALIASES["ursodiol"] + ("UDCA",)
_KATAKANA_VARIANT_ALIASES["calcium_gluconate"] = _KATAKANA_VARIANT_ALIASES["calcium_gluconate"] + (
    "カルシウムグルコン酸",
    "グルコン酸ca",  # 救急key drug表記 "グルコン酸Ca10%"（小文字化後に照合）
)


# Japanese dose-form / salt / strength suffixes that formulary names carry but
# treatment texts omit ("オフロキサシン点眼" is cited as "オフロキサシン 1滴 q6h",
# "キニジン硫酸塩" as "キニジン 22 mg/kg"). Stripped iteratively so stacked
# suffixes ("ナタマイシン点眼5%") reduce to the bare agent name.
_JA_FORM_SUFFIX_RE = re.compile(
    r"(配合点眼|点眼液|点眼|注射|吸入|外用|クリーム|軟膏|ゲル|リンス"
    r"|酢酸塩|塩酸塩|硫酸塩|リン酸塩|アルファ"
    r"|[0-9.]+[%％]?|[-–])$"
)


def _strip_ja_form_suffixes(name: str) -> str:
    """Strip trailing Japanese dose-form/salt/strength suffixes from a drug name."""
    s = name
    for _ in range(6):
        m = _JA_FORM_SUFFIX_RE.search(s)
        if not m or m.start() == 0:
            break
        s = s[: m.start()].strip()
    return s


def _build_drug_keyword_index() -> None:
    """Build keyword → drug_id mapping for treatment-text scanning.

    Indexed keys (lowercase, length ≥ 4 chars to avoid false matches), in
    priority tiers so a drug's own full name always beats another drug's
    derived variant:
      1. Full English / Japanese names (e.g., "amoxicillin", "アモキシシリン")
      2. Parenthetical-suffix-stripped stems ("ミネラルオイル（流動パラフィン）" →
         "ミネラルオイル"), slash-separated alternates ("ノルモソルR／プラズマライトA" →
         both), ・-separated combination halves ("トリメトプリム・スルファメトキサゾール"
         → both — treatment texts frequently cite one half alone), trailing-液
         stems for fluids (treatment texts write "乳酸リンゲル 10-20 mL/kg"
         without the 液), and Japanese dose-form/salt-suffix-stripped stems
         ("オフロキサシン点眼" → "オフロキサシン", "リュープロレリン酢酸塩" →
         "リュープロレリン", "ダルベポエチンアルファ" → "ダルベポエチン")
      3. First word of multi-word names ("Toceranib" from "Toceranib
         Phosphate") — except bare generic words (_FIRST_WORD_STOPLIST)
    """
    tier1: list[tuple[str, str]] = []
    tier2: list[tuple[str, str]] = []
    tier3: list[tuple[str, str]] = []
    tier4: list[tuple[str, str]] = []
    for d in DRUGS:
        drug_id = d.get("id")
        if not drug_id:
            continue
        # Katakana spelling variants (legitimate alternates used by treatment
        # texts) — indexed at tier 2 so a drug's own full name still wins.
        # Central registry + optional per-drug "search_aliases" field.
        for alias in list(_KATAKANA_VARIANT_ALIASES.get(drug_id, ())) + list(d.get("search_aliases") or ()):
            a = alias.strip().lower()
            # Pure-kanji compounds are dense enough to be specific at 2-3
            # chars (硫酸鉄, 生食 — clinical shorthand for saline); katakana
            # and Latin aliases still need ≥4 chars, since bare substring
            # matching would false-positive inside longer katakana runs.
            if len(a) >= 4 or (len(a) >= 2 and all("一" <= ch <= "鿿" for ch in a)):
                tier2.append((a, drug_id))
        for key in (d.get("name", ""), d.get("name_ja", "")):
            if not key or len(key) < 4:
                continue
            k = key.strip().lower()
            tier1.append((k, drug_id))
            variants: list[str] = []
            stem = re.split(r"[（(]", k)[0].strip()
            if stem and stem != k:
                variants.append(stem)
            for part in re.split(r"[／/・]", stem or k):
                part = part.strip()
                if part and part != k and part not in variants:
                    variants.append(part)
            for v in list(variants) + [k]:
                if v.endswith("液") and len(v) >= 5 and v[:-1] not in variants:
                    variants.append(v[:-1])
            for v in list(variants) + [k]:
                s = _strip_ja_form_suffixes(v)
                if s and s != v and s not in variants:
                    variants.append(s)
            tier2.extend((v, drug_id) for v in variants if len(v) >= 4 and v not in _GENERIC_STEM_STOPLIST)
            first_word = k.split()[0] if " " in k else k.split("-")[0]
            if first_word != k and len(first_word) >= 4 and first_word not in _FIRST_WORD_STOPLIST:
                tier3.append((first_word, drug_id))
            # Paren-inner Japanese brand names ("（バナミン）", "（プロジンク）") —
            # lowest tier so a drug's own indexed stems always win first.
            for paren in re.finditer(r"[（(]([^）)]*)[）)]", key):
                for part in re.split(r"[／/・、,;；\s]+", paren.group(1)):
                    part = part.strip()
                    if (
                        _PURE_KATAKANA_RE.match(part)
                        and part not in _PAREN_PART_STOPLIST
                        and part not in _GENERIC_STEM_STOPLIST
                    ):
                        tier4.append((part, drug_id))
    for keyword, drug_id in tier1 + tier2 + tier3 + tier4:
        if keyword not in _DRUG_KEYWORD_INDEX:
            _DRUG_KEYWORD_INDEX[keyword] = drug_id


_build_drug_keyword_index()


def find_drugs_in_text(text: str, max_results: int = 25) -> List[Dict]:
    """Extract drugs mentioned in a free-text treatment description.

    Returns a list of compact drug dicts {id, name, name_ja, category} in
    order of first occurrence. Duplicates and near-duplicates are de-duplicated.
    """
    if not text:
        return []
    text_lower = text.lower()
    found_ids: list[str] = []
    seen: set[str] = set()
    for keyword, drug_id in _CASE_SENSITIVE_KEYWORDS.items():
        if drug_id not in seen and keyword in text:
            found_ids.append(drug_id)
            seen.add(drug_id)
    for keyword, drug_id in _DRUG_KEYWORD_INDEX.items():
        if drug_id in seen:
            continue
        if keyword in text_lower:
            # Digit-boundary guard: a keyword ending in a digit ("ビタミンb1")
            # must not match inside a longer number ("ビタミンB12") — otherwise
            # every B12 mention spuriously chips the thiamine entry.
            if keyword[-1].isdigit():
                pos, hit = 0, False
                while True:
                    pos = text_lower.find(keyword, pos)
                    if pos == -1:
                        break
                    nxt = pos + len(keyword)
                    if nxt >= len(text_lower) or not text_lower[nxt].isdigit():
                        hit = True
                        break
                    pos += 1
                if not hit:
                    continue
            negatives = _KEYWORD_NEGATIVE_CONTEXTS.get(keyword)
            if negatives:
                pos, hit = 0, False
                while True:
                    pos = text_lower.find(keyword, pos)
                    if pos == -1:
                        break
                    if not any(
                        neg in text_lower[max(0, pos - len(neg)) : pos + len(keyword) + len(neg)] for neg in negatives
                    ):
                        hit = True
                        break
                    pos += 1
                if not hit:
                    continue
            found_ids.append(drug_id)
            seen.add(drug_id)
            if len(found_ids) >= max_results:
                break
    # Return compact info from index
    results: list[dict] = []
    for drug_id in found_ids:
        d = _drug_index.get(drug_id)
        if d:
            results.append(
                {
                    "id": d.get("id"),
                    "name": d.get("name", ""),
                    "name_ja": d.get("name_ja", ""),
                    "category": d.get("category", ""),
                }
            )
    return results


def find_drugs_for_disease(species: str, disease_name: str, lang: str = "") -> List[Dict]:
    """Find drugs typically used to treat a named disease in a given species.

    Scans the disease's treatment text (treatment_ja or treatment) for drug
    name keywords. Returns drugs ordered by appearance in treatment.
    """
    # Lazy import to avoid circular dependency
    try:
        import importlib

        # Map species to module + attribute
        species_modules = {
            "dog": ("api.species.dog_diseases", "DISEASES"),
            "cat": ("api.species.cat_diseases", "DISEASES"),
            "horse": ("api.species.equine_diseases", "DISEASE_DATABASE"),
            "rabbit": ("api.species.rabbit_diseases", "DISEASES"),
            "hamster": ("api.species.hamster_diseases", "DISEASES"),
            "guinea_pig": ("api.species.guinea_pig_diseases", "DISEASES"),
            "chinchilla": ("api.species.chinchilla_diseases", "DISEASES"),
            "ferret": ("api.species.ferret_diseases", "DISEASES"),
            "hedgehog": ("api.species.hedgehog_diseases", "DISEASES"),
            "sugar_glider": ("api.species.sugar_glider_diseases", "DISEASES"),
            "degu": ("api.species.degu_diseases", "DISEASES"),
            "bird": ("api.species.bird_diseases", "DISEASES"),
            "parakeet": ("api.species.parakeet_diseases", "DISEASES"),
            "parrot": ("api.species.parrot_diseases", "DISEASES"),
            "reptile": ("api.species.reptile_diseases", "DISEASES"),
            "tortoise": ("api.species.tortoise_diseases", "DISEASES"),
            "snake": ("api.species.snake_diseases", "DISEASES"),
            "lizard": ("api.species.lizard_diseases", "DISEASES"),
            "amphibian": ("api.species.amphibian_diseases", "DISEASES"),
            "fish": ("api.species.fish_diseases", "DISEASES"),
            "exotic_other": ("api.species.exotic_other_diseases", "DISEASES"),
        }
        sp_key = (species or "dog").lower()
        if sp_key not in species_modules:
            return []
        mod_name, attr = species_modules[sp_key]
        mod = importlib.import_module(mod_name)
        diseases = getattr(mod, attr, [])
    except (ImportError, AttributeError):
        return []

    # Find matching disease by name (case-insensitive, both languages)
    target_lower = (disease_name or "").lower().strip()
    if not target_lower:
        return []
    matched_disease = None
    for d in diseases:
        if isinstance(d, dict):
            name_en = (d.get("name", "") or "").lower()
            name_ja = (d.get("name_ja", "") or "").lower()
            if target_lower in name_en or target_lower in name_ja or name_en == target_lower:
                matched_disease = d
                break
        elif hasattr(d, "name_en"):
            # Equine Disease dataclass
            name_en = (getattr(d, "name_en", "") or "").lower()
            name_ja = (getattr(d, "name_ja", "") or "").lower()
            if target_lower in name_en or target_lower in name_ja:
                matched_disease = d
                break
    if matched_disease is None:
        return []

    # Extract treatment text (prefer Japanese if requested, fall back to English)
    if isinstance(matched_disease, dict):
        treatment_text = (
            matched_disease.get("treatment_ja", "") if lang == "ja" else matched_disease.get("treatment", "")
        )
        if not treatment_text:
            treatment_text = matched_disease.get("treatment_ja", "") or matched_disease.get("treatment", "")
    else:
        # Equine Disease dataclass
        treatment_text = getattr(matched_disease, "treatment_protocol", "") or ""

    return find_drugs_in_text(treatment_text)


# Cache reverse-lookup index built lazily on first request: drug_id → list[disease_ref]
_DRUG_TO_DISEASES_CACHE: dict[str, list[dict]] | None = None


def _build_drug_to_diseases_index() -> dict[str, list[dict]]:
    """Build a reverse index from drug_id to list of disease references mentioning it.

    Scans all species' disease entries' treatment_ja / treatment fields for
    drug names from the keyword index. Returns:
      {drug_id: [{species, name, name_ja, urgency}, ...]}
    """
    import importlib

    species_modules = {
        "dog": ("api.species.dog_diseases", "DISEASES"),
        "cat": ("api.species.cat_diseases", "DISEASES"),
        "horse": ("api.species.equine_diseases", "DISEASE_DATABASE"),
        "rabbit": ("api.species.rabbit_diseases", "DISEASES"),
        "hamster": ("api.species.hamster_diseases", "DISEASES"),
        "guinea_pig": ("api.species.guinea_pig_diseases", "DISEASES"),
        "chinchilla": ("api.species.chinchilla_diseases", "DISEASES"),
        "ferret": ("api.species.ferret_diseases", "DISEASES"),
        "hedgehog": ("api.species.hedgehog_diseases", "DISEASES"),
        "sugar_glider": ("api.species.sugar_glider_diseases", "DISEASES"),
        "degu": ("api.species.degu_diseases", "DISEASES"),
        "bird": ("api.species.bird_diseases", "DISEASES"),
        "parakeet": ("api.species.parakeet_diseases", "DISEASES"),
        "parrot": ("api.species.parrot_diseases", "DISEASES"),
        "reptile": ("api.species.reptile_diseases", "DISEASES"),
        "tortoise": ("api.species.tortoise_diseases", "DISEASES"),
        "snake": ("api.species.snake_diseases", "DISEASES"),
        "lizard": ("api.species.lizard_diseases", "DISEASES"),
        "amphibian": ("api.species.amphibian_diseases", "DISEASES"),
        "fish": ("api.species.fish_diseases", "DISEASES"),
        "exotic_other": ("api.species.exotic_other_diseases", "DISEASES"),
    }
    index: dict[str, list[dict]] = {}

    # Corpus-inverted scan: the naive per-(text, keyword) substring loop is
    # O(texts × keywords) Python-level iterations (~26k texts × ~1.9k keywords
    # after the JSON overlay was added) and took ~27s on the production tier.
    # Instead all texts are concatenated once (NUL-fenced so no keyword can
    # match across a text boundary) and each keyword runs a single C-speed
    # str.find sweep over the corpus, mapping hit offsets back to text indices
    # via bisect. Semantics are identical: a drug is referenced by a text iff
    # any of its keywords is a substring of that text.
    _texts: list[str] = []  # lowercased text per collected field
    _texts_raw: list[str] = []  # original case (for _CASE_SENSITIVE_KEYWORDS)
    _refs: list[dict] = []  # parallel disease ref per collected field

    def _scan(text: str, sp: str, name_en: str, name_ja: str, urgency: str) -> None:
        if not text:
            return
        _texts.append(text.lower())
        _texts_raw.append(text)
        _refs.append({"species": sp, "name": name_en, "name_ja": name_ja, "urgency": urgency or ""})

    for sp_key, (mod_name, attr) in species_modules.items():
        try:
            mod = importlib.import_module(mod_name)
            diseases = getattr(mod, attr, [])
        except (ImportError, AttributeError):
            continue
        for d in diseases:
            if isinstance(d, dict):
                name_en = d.get("name", "") or ""
                name_ja = d.get("name_ja", "") or ""
                urgency = d.get("urgency", "") or ""
                _scan(d.get("treatment", ""), sp_key, name_en, name_ja, urgency)
                _scan(d.get("treatment_ja", ""), sp_key, name_en, name_ja, urgency)
            else:
                # Equine Disease dataclass
                name_en = getattr(d, "name_en", "") or ""
                name_ja = getattr(d, "name_ja", "") or ""
                urgency = getattr(d, "urgency", "") or ""
                _scan(getattr(d, "treatment_protocol", ""), sp_key, name_en, name_ja, urgency)

    # Curated JSON overlay: the served treatment text for many diseases lives
    # only in diseases_all_species.json (applied at enrich time), so drugs
    # cited exclusively there (e.g. tiludronate in the equine navicular
    # entries) had an empty "used by diseases" card while the forward
    # disease→drug chips resolved fine. Scan the overlay too; the (species,
    # name) de-duplication below collapses module/overlay double hits.
    _overlay_path = os.path.join(os.path.dirname(__file__), "..", "diseases_all_species.json")
    try:
        with open(_overlay_path, encoding="utf-8") as _fh:
            _overlay = json.load(_fh)
    except (OSError, ValueError):
        _overlay = []
    _sp_from_json = {
        "Dog": "dog",
        "Cat": "cat",
        "Horse": "horse",
        "Rabbit": "rabbit",
        "Hamster": "hamster",
        "Guinea Pig": "guinea_pig",
        "Chinchilla": "chinchilla",
        "Ferret": "ferret",
        "Hedgehog": "hedgehog",
        "Sugar Glider": "sugar_glider",
        "Degu": "degu",
        "Bird": "bird",
        "Parakeet": "parakeet",
        "Parrot": "parrot",
        "Reptile": "reptile",
        "Tortoise": "tortoise",
        "Snake": "snake",
        "Lizard": "lizard",
        "Amphibian": "amphibian",
        "Fish": "fish",
        "Exotic Other": "exotic_other",
    }
    for entry in _overlay:
        sp_key = _sp_from_json.get(entry.get("species") or "")
        if not sp_key:
            continue
        name_en = entry.get("name", "") or ""
        name_ja = entry.get("name_ja", "") or ""
        urgency = entry.get("urgency", "") or ""
        _scan(entry.get("treatment", ""), sp_key, name_en, name_ja, urgency)
        _scan(entry.get("treatment_ja", ""), sp_key, name_en, name_ja, urgency)

    # Single inverted sweep over the concatenated corpus.
    import bisect

    _SEP = "\x00"

    def _offsets_for(texts: list[str]) -> list[int]:
        offs: list[int] = []
        pos = 0
        for t in texts:
            offs.append(pos)
            pos += len(t) + len(_SEP)
        return offs

    # lower() can change string length for exotic code points, so the raw
    # (case-sensitive) corpus gets its own offset table.
    offsets = _offsets_for(_texts)
    offsets_raw = _offsets_for(_texts_raw)
    corpus = _SEP.join(_texts)
    corpus_raw = _SEP.join(_texts_raw)

    def _sweep(haystack: str, offs: list[int], keyword: str, drug_id: str, hits: set) -> None:
        start = haystack.find(keyword)
        while start != -1:
            ti = bisect.bisect_right(offs, start) - 1
            hits.add((drug_id, ti))
            # Jump past the current text so each text counts at most once.
            next_pos = offs[ti + 1] if ti + 1 < len(offs) else len(haystack)
            start = haystack.find(keyword, next_pos)

    hits: set[tuple[str, int]] = set()
    for keyword, drug_id in _CASE_SENSITIVE_KEYWORDS.items():
        _sweep(corpus_raw, offsets_raw, keyword, drug_id, hits)
    for keyword, drug_id in _DRUG_KEYWORD_INDEX.items():
        _sweep(corpus, offsets, keyword, drug_id, hits)

    # Emit refs in text order per drug, de-duplicating identical
    # (species, name) tuples (occurs when both treatment + treatment_ja match
    # the same drug for the same disease).
    per_drug: dict[str, list[int]] = {}
    for drug_id, ti in hits:
        per_drug.setdefault(drug_id, []).append(ti)
    for drug_id, tis in per_drug.items():
        seen_pairs: set[tuple] = set()
        unique: list[dict] = []
        for ti in sorted(tis):
            r = _refs[ti]
            key = (r["species"], r["name"], r["name_ja"])
            if key in seen_pairs:
                continue
            seen_pairs.add(key)
            unique.append(r)
        index[drug_id] = unique
    return index


def find_diseases_for_drug(drug_id: str, species: str | None = None, limit: int = 50) -> list[dict]:
    """Return list of diseases whose treatment text mentions this drug.

    Optional `species` filter restricts to one species. Results are sorted
    by urgency (emergency first) then alphabetically.
    """
    global _DRUG_TO_DISEASES_CACHE
    if _DRUG_TO_DISEASES_CACHE is None:
        # Normally the import-time warm thread has already populated the
        # cache; if a request arrives first (or the thread died in a fork),
        # build synchronously. The build is idempotent, so a rare duplicate
        # build is acceptable — no lock, so a fork can never deadlock us.
        _DRUG_TO_DISEASES_CACHE = _build_drug_to_diseases_index()
    refs = _DRUG_TO_DISEASES_CACHE.get(drug_id, [])
    if species:
        refs = [r for r in refs if r.get("species") == species]
    urgency_order = {"emergency": 0, "high": 1, "urgent": 1, "moderate": 2, "normal": 3, "": 4}
    refs_sorted = sorted(
        refs,
        key=lambda r: (urgency_order.get(r.get("urgency", ""), 5), r.get("name", "").lower()),
    )
    return refs_sorted[:limit]


def _warm_drug_to_diseases_index() -> None:
    """Populate the reverse drug→disease index off the request path.

    The corpus scan takes tens of seconds (all species' treatment texts plus
    the curated JSON overlay), which previously landed on the first request
    that expanded a drug card's "used by diseases" chips — long enough to hit
    the production worker timeout. Warm it in a daemon thread at import so
    the build runs during process boot instead. Lock-free by design: if a
    request races the thread (or a fork killed it), find_diseases_for_drug
    simply builds synchronously and the last assignment wins.
    """
    global _DRUG_TO_DISEASES_CACHE
    try:
        built = _build_drug_to_diseases_index()
    except Exception:  # pragma: no cover - warm-up must never crash a worker
        return
    if _DRUG_TO_DISEASES_CACHE is None:
        _DRUG_TO_DISEASES_CACHE = built


def _start_drug_to_diseases_warmup() -> None:
    import threading

    threading.Thread(
        target=_warm_drug_to_diseases_index,
        name="drug-disease-index-warmup",
        daemon=True,
    ).start()


_start_drug_to_diseases_warmup()


def search_drugs(query: str, category: str | None = None, species: str | None = None) -> List[Dict]:
    """薬品名・商品名エイリアス・カテゴリ・動物種で検索する。

    照合は _normalize_search_text で正規化して行うため、ひらがな入力
    （ばいとりる）・全角英数・半角カナでも一致する。
    """
    query_norm = _normalize_search_text(query) if query else ""
    results = []
    for drug in DRUGS:
        if category and drug["category"] != category:
            continue
        if species and species in drug.get("species_info", {}):
            info = drug["species_info"][species]
            if not info.get("safe", True):
                continue
        elif species:
            continue
        if query_norm:
            alias_text = " ".join(list(drug.get("search_aliases") or []) + list(drug.get("aliases") or []))
            searchable = _normalize_search_text(
                f"{drug['name']} {drug['name_ja']} {alias_text} "
                f"{drug.get('mechanism', '')} {drug.get('mechanism_ja', '')}"
            )
            if query_norm not in searchable:
                continue
        results.append(drug)
    return results


def get_drugs_by_category(category: str) -> List[Dict]:
    """カテゴリIDで薬品を取得する。"""
    return [d for d in DRUGS if d["category"] == category]


def get_drugs_by_species(species: str) -> List[Dict]:
    """動物種名で安全な薬品を取得する。"""
    results = []
    for drug in DRUGS:
        if species in drug.get("species_info", {}):
            info = drug["species_info"][species]
            results.append({**drug, "_species_dosage": info})
    return results


def get_drug_by_id(drug_id: str) -> Optional[Dict]:
    """薬品IDで単一薬品を取得する。

    統合された重複エントリの旧IDは正規IDへ解決するため、既存のURL・ブックマーク・
    外部リンクは統合後も 404 にならない（疾患側の 301 リダイレクトと同じ考え方）。
    詳細API・SEOページ・疾患リンクはすべてこの関数を通るので、ここ1箇所で足りる。
    """
    resolved = resolve_drug_id(drug_id)
    for drug in DRUGS:
        if drug["id"] == resolved:
            return drug
    return None


# ---------------------------------------------------------------------------
# Flask Blueprint API
# ---------------------------------------------------------------------------


_LIST_FIELDS = frozenset(
    {
        "side_effects",
        "side_effects_ja",
        "routes",
        "routes_ja",
        "formulations",
        "formulations_ja",
    }
)


def _as_list(value):
    """Normalize a list-typed field so the API contract is consistent.

    Some drug entries store ``side_effects`` (etc.) as a comma-separated
    string rather than a list. The frontend renders these as tags / joins
    them, so a stray string crashes the whole list render. Split such strings
    on Japanese (、) and ASCII/fullwidth commas; pass lists through unchanged.
    """
    if isinstance(value, list):
        return value
    if isinstance(value, str):
        parts = re.split(r"[、,，]", value)
        return [p.strip() for p in parts if p.strip()]
    return value


def _drug_list_payload(d: Dict) -> Dict:
    """薬品一覧用のペイロードを構築する。

    一覧と展開詳細パネルの両方を1リクエストで賄うため、臨床的に重要な
    フィールド（作用機序・副作用・薬物相互作用・禁忌・投与経路・製剤・
    スポンサー情報）を含める。存在するフィールドのみを含めてペイロードを
    肥大化させない。
    """
    payload = {
        "id": d["id"],
        "name": d["name"],
        "name_ja": d["name_ja"],
        "category": d["category"],
        "category_ja": DRUG_CATEGORIES.get(d["category"], {}).get("ja", d["category"]),
        "contraindications": d.get("contraindications", ""),
        "contraindications_ja": d.get("contraindications_ja", ""),
        "species_info": d.get("species_info", {}),
    }
    for field in (
        "mechanism",
        "mechanism_ja",
        "side_effects",
        "side_effects_ja",
        "drug_interactions",
        "routes",
        "routes_ja",
        "formulations",
        "formulations_ja",
        "search_aliases",
        "aliases",
        "sponsor",
        "sponsor_name",
        "sponsor_url",
        "sponsor_url_dog",
    ):
        value = d.get(field)
        if value:
            payload[field] = _as_list(value) if field in _LIST_FIELDS else value
    return payload


@drug_bp.route("/api/drugs", methods=["GET"])
def api_list_drugs():
    """薬品一覧を返す。クエリパラメータ: search, category, species"""
    query = request.args.get("search", "")
    category = request.args.get("category")
    species = request.args.get("species")
    results = search_drugs(query, category, species)
    return jsonify(
        {
            "drugs": [_drug_list_payload(d) for d in results],
            "total": len(results),
            "categories": DRUG_CATEGORIES,
        }
    )


@drug_bp.route("/api/drugs/<drug_id>", methods=["GET"])
def api_get_drug(drug_id: str):
    """単一薬品の詳細を返す。"""
    drug = get_drug_by_id(drug_id)
    if not drug:
        return jsonify({"error": "Drug not found"}), 404
    return jsonify({"drug": drug})


@drug_bp.route("/api/drugs/for-disease", methods=["GET"])
def api_drugs_for_disease():
    """疾患名から関連薬品リストを返す（治療テキストからの自動抽出）。

    Query params:
      - species: 動物種コード（dog, cat, horse 等）
      - name: 疾患名（日本語または英語、部分一致）
      - lang: 'ja' で日本語治療テキスト優先、空または 'en' で英語

    Response: {drugs: [{id, name, name_ja, category}, ...]}
    """
    species = (request.args.get("species") or "").strip()
    disease_name = (request.args.get("name") or "").strip()
    lang = (request.args.get("lang") or "").strip().lower()
    if not species or not disease_name:
        return jsonify({"error": "species and name parameters required"}), 400
    drugs = find_drugs_for_disease(species, disease_name, lang=lang)
    return jsonify({"species": species, "disease_name": disease_name, "drugs": drugs, "count": len(drugs)})


@drug_bp.route("/api/drugs/<drug_id>/diseases", methods=["GET"])
def api_diseases_for_drug(drug_id: str):
    """単一薬品を治療に含む疾患リストを返す（逆方向リンク）。

    Query params:
      - species: 動物種コード（任意、フィルタ用）
      - limit: 最大件数（既定50）

    Response: {drug_id, count, diseases: [{species, name, name_ja, urgency}, ...]}
    """
    if not get_drug_by_id(drug_id):
        return jsonify({"error": "Drug not found"}), 404
    species = (request.args.get("species") or "").strip() or None
    try:
        limit = max(1, min(int(request.args.get("limit", 50)), 200))
    except (TypeError, ValueError):
        limit = 50
    diseases = find_diseases_for_drug(drug_id, species=species, limit=limit)
    return jsonify({"drug_id": drug_id, "count": len(diseases), "diseases": diseases})


@drug_bp.route("/api/drug-categories", methods=["GET"])
def api_drug_categories():
    """薬品カテゴリ一覧を返す。"""
    cats = []
    for cat_id, names in DRUG_CATEGORIES.items():
        count = _DRUG_COUNT_BY_CATEGORY.get(cat_id, 0)
        cats.append({"id": cat_id, "name_ja": names["ja"], "name_en": names["en"], "count": count})
    cats.sort(key=lambda c: c["count"], reverse=True)
    return jsonify({"categories": cats, "total_drugs": len(DRUGS)})


# ---------------------------------------------------------------------------
# 用量計算機 + 相互作用チェック API
# ---------------------------------------------------------------------------

from api.dose_calculator import calculate_dose
from api.dose_calculator import to_dict as dose_to_dict
from api.drug_interactions import (
    find_interactions,
    find_species_specific_warnings,
    get_all_interactions_for_drug,
)


@drug_bp.route("/api/drugs/calculate-dose", methods=["POST"])
def api_calculate_dose():
    """
    体重ベース用量計算。
    Body JSON: {drug_id, species, body_weight_kg, concentration_mg_per_ml?}
    """
    data = request.get_json(silent=True) or {}
    drug_id = data.get("drug_id", "").strip()
    species = data.get("species", "").strip().lower()
    try:
        weight = float(data.get("body_weight_kg", 0))
    except (TypeError, ValueError):
        return jsonify({"error": "body_weight_kg must be a number"}), 400
    if not drug_id or not species or weight <= 0:
        return jsonify({"error": "drug_id, species, body_weight_kg required"}), 400

    drug = get_drug_by_id(drug_id)
    if not drug:
        return jsonify({"error": "Drug not found"}), 404

    conc = data.get("concentration_mg_per_ml")
    try:
        conc = float(conc) if conc is not None else None
    except (TypeError, ValueError):
        conc = None

    calc = calculate_dose(drug, species, weight, concentration_mg_per_ml=conc)
    species_warnings = find_species_specific_warnings(drug_id, species)
    return jsonify(
        {
            "calculation": dose_to_dict(calc),
            "species_specific_warnings": species_warnings,
        }
    )


@drug_bp.route("/api/drugs/check-interactions", methods=["POST"])
def api_check_interactions():
    """
    薬品-薬品相互作用チェック。
    Body JSON: {drug_ids: [...], species?: "..."}
    Returns unknown_drug_ids so the UI can tell the user which inputs didn't match.
    """
    data = request.get_json(silent=True) or {}
    drug_ids = data.get("drug_ids", []) or []
    species = (data.get("species") or "").strip().lower()
    if not isinstance(drug_ids, list):
        return jsonify({"error": "drug_ids must be a list"}), 400
    if len(drug_ids) < 1:
        return jsonify(
            {
                "interactions": [],
                "species_specific_warnings": [],
                "total_interactions": 0,
                "unknown_drug_ids": [],
                "recognized_drug_ids": [],
            }
        )

    # Identify which submitted IDs are recognized so the UI can warn on typos.
    recognized = [did for did in drug_ids if get_drug_by_id(did) is not None]
    unknown = [did for did in drug_ids if get_drug_by_id(did) is None]

    interactions = find_interactions(drug_ids)
    species_warnings = []
    if species:
        for did in drug_ids:
            species_warnings.extend(find_species_specific_warnings(did, species))

    return jsonify(
        {
            "interactions": interactions,
            "species_specific_warnings": species_warnings,
            "total_interactions": len(interactions),
            "recognized_drug_ids": recognized,
            "unknown_drug_ids": unknown,
        }
    )


@drug_bp.route("/api/drugs/<drug_id>/interactions", methods=["GET"])
def api_drug_interactions(drug_id: str):
    """単一薬品に関わる全相互作用を返す（参考表示用）"""
    drug = get_drug_by_id(drug_id)
    if not drug:
        return jsonify({"error": "Drug not found"}), 404
    interactions = get_all_interactions_for_drug(drug_id)
    return jsonify({"drug_id": drug_id, "interactions": interactions, "total": len(interactions)})


# ---------------------------------------------------------------------------
# エビデンスグレード API
# ---------------------------------------------------------------------------
from api.evidence_grading import (
    AI_CONTENT_DISCLAIMER,
    DIAGNOSTIC_DISCLAIMER,
    DOSE_CALCULATOR_DISCLAIMER,
    assess,
)
from api.evidence_grading import (
    to_dict as evidence_to_dict,
)


@drug_bp.route("/api/evidence/assess", methods=["POST"])
def api_evidence_assess():
    """
    治療文字列のエビデンス評価。
    Body JSON: {text: "..."}
    """
    data = request.get_json(silent=True) or {}
    text = data.get("text", "") or ""
    assessment = assess(text)
    return jsonify({"assessment": evidence_to_dict(assessment)})


@drug_bp.route("/api/disclaimers", methods=["GET"])
def api_disclaimers():
    """免責事項テキストを返す"""
    return jsonify(
        {
            "ai_content": AI_CONTENT_DISCLAIMER,
            "diagnostic": DIAGNOSTIC_DISCLAIMER,
            "dose_calculator": DOSE_CALCULATOR_DISCLAIMER,
        }
    )


# ---------------------------------------------------------------------------
# 治療プラン生成 API
# ---------------------------------------------------------------------------
from api.treatment_plan import build_treatment_plan
from api.treatment_plan import to_dict as plan_to_dict


def _get_drug_lookup() -> dict:
    """drug_id → drug_dict のマッピングを構築"""
    return {d["id"]: d for d in DRUGS}


@drug_bp.route("/api/treatment-plan/generate", methods=["POST"])
def api_generate_treatment_plan():
    """
    確定診断から構造化治療プランを生成。
    Body JSON: {disease: {...}, species: "...", body_weight_kg?: ...}
    """
    data = request.get_json(silent=True) or {}
    disease = data.get("disease") or {}
    species = (data.get("species") or "").strip().lower()
    weight = data.get("body_weight_kg")
    try:
        weight = float(weight) if weight is not None else None
    except (TypeError, ValueError):
        weight = None
    if not disease or not species:
        return jsonify({"error": "disease and species required"}), 400

    lang = data.get("lang", "ja")
    drug_lookup = _get_drug_lookup()
    plan = build_treatment_plan(
        disease=disease,
        drug_lookup=drug_lookup,
        species=species,
        body_weight_kg=weight,
        lang=lang,
    )
    return jsonify({"plan": plan_to_dict(plan)})
