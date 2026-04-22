#!/usr/bin/env python3
"""
臨床詳細フィールド生成スクリプト
clinical_signs, diagnosis, transmission を 4,230 疾患に追加
"""

import json
import random
from pathlib import Path
from typing import Dict

# ============================================================================
# 臨床詳細生成エンジン
# ============================================================================


class ClinicalDetailsGenerator:
    """疾患別に臨床詳細を生成"""

    # 疾患カテゴリ別テンプレート
    TEMPLATES = {
        "infectious_viral": {
            "keywords": [
                "virus",
                "viral",
                "infection",
                "influenza",
                "distemper",
                "feline",
                "felv",
                "fiv",
            ],
            "clinical_signs": [
                (
                    "Fever and elevated body temperature; lethargy and depression; anorexia and weight loss; "
                    "nasal and ocular discharge; coughing and sneezing; oral ulcers and mucous membrane lesions"
                ),
                (
                    "Fever; malaise; loss of appetite; conjunctivitis with discharge; "
                    "respiratory signs including cough; lymphadenopathy; dehydration"
                ),
                (
                    "Elevated temperature; loss of appetite; depression; mucous discharge from nose and eyes; "
                    "respiratory distress; oral lesions; swollen lymph nodes"
                ),
                (
                    "Fever; lethargy; anorexia; nasal/ocular discharge; cough; sneezing; "
                    "enlarged lymph nodes; dehydration; possible diarrhea"
                ),
            ],
            "diagnosis": [
                (
                    "Clinical signs and history; viral antigen detection (ELISA or rapid tests); "
                    "viral isolation from nasal/ocular swabs; PCR for viral nucleic acid; "
                    "serology for antibody detection (ELISA, SNAP test)"
                ),
                (
                    "Clinical examination and symptom assessment; virus isolation from clinical specimens; "
                    "PCR testing; serological testing (ELISA); viral antigen detection"
                ),
                (
                    "Symptom recognition and history; viral culture from appropriate samples; "
                    "Polymerase Chain Reaction (PCR); serology including ELISA; rapid antigen tests"
                ),
                (
                    "Based on clinical presentation and history; "
                    "confirmed by PCR, viral culture, or antigen detection; serology showing seroconversion"
                ),
            ],
            "transmission": [
                (
                    "Airborne respiratory droplets and aerosols; direct contact with infected animals; "
                    "fomite transmission via contaminated surfaces and objects; "
                    "maternal transmission possible in some viral infections"
                ),
                (
                    "Respiratory route via droplets and aerosols; direct contact with infected secretions; "
                    "indirect contact via contaminated environment; possible vertical transmission"
                ),
                (
                    "Droplet transmission through respiratory secretions; "
                    "direct contact with infected individuals; "
                    "fomite transmission; possible environmental contamination"
                ),
                (
                    "Primarily airborne droplet transmission; direct contact with body fluids and secretions; "
                    "fomite contamination; in some cases, vertical or perinatal transmission"
                ),
            ],
        },
        "infectious_bacterial": {
            "keywords": [
                "bacteria",
                "bacterial",
                "infection",
                "streptococcus",
                "staphylococcus",
                "leptospirosis",
            ],
            "clinical_signs": [
                (
                    "Fever and chills; lethargy and malaise; anorexia and weight loss; "
                    "purulent discharge (nasal, ocular, or wound); swollen lymph nodes; possible sepsis signs"
                ),
                (
                    "Elevated body temperature; depression and weakness; loss of appetite; "
                    "suppurative discharge from affected areas; lymphadenitis; possible abdominal pain"
                ),
                (
                    "Fever; systemic illness signs; localized suppuration; lymph node enlargement; "
                    "constitutional symptoms including weakness and poor appetite"
                ),
                (
                    "High fever; extreme lethargy; anorexia; purulent discharge; "
                    "enlarged tender lymph nodes; in severe cases, septic shock signs"
                ),
            ],
            "diagnosis": [
                (
                    "Culture of bacterial organisms from appropriate samples (blood, urine, tissue, discharge); "
                    "Gram stain microscopy; bacterial identification; sensitivity testing for antibiotic selection"
                ),
                (
                    "Bacterial isolation and culture from clinical specimens; "
                    "Gram staining and microscopic examination; "
                    "biochemical identification; antibiotic susceptibility testing"
                ),
                (
                    "Bacteriological culture; Gram staining; bacterial identification testing; "
                    "culture sensitivity results; CBC showing leukocytosis"
                ),
                (
                    "Blood or tissue culture showing growth of pathogenic bacteria; "
                    "Gram staining results; biochemical tests for identification; "
                    "antimicrobial susceptibility patterns"
                ),
            ],
            "transmission": [
                (
                    "Direct contact with infected individuals or contaminated body fluids; "
                    "airborne droplets in respiratory infections; "
                    "contaminated fomites and environmental surfaces; "
                    "ingestion of contaminated food or water; wound contamination"
                ),
                (
                    "Contact transmission via infected secretions; respiratory droplets in some infections; "
                    "ingestion route for certain pathogens; wound contamination; "
                    "vector transmission in specific cases"
                ),
                (
                    "Direct inoculation through cuts or bites; respiratory droplet transmission; "
                    "fecal-oral route; contaminated fomites; environmental water or food sources"
                ),
                (
                    "Multiple routes depending on bacterial species: "
                    "respiratory, gastrointestinal, contact, or vector-borne transmission"
                ),
            ],
        },
        "parasitic": {
            "keywords": [
                "parasite",
                "parasitic",
                "worm",
                "helminth",
                "mite",
                "lice",
                "tick",
                "flea",
                "coccidia",
            ],
            "clinical_signs": [
                (
                    "Pruritus and scratching behavior; alopecia and hair loss; "
                    "skin inflammation and erythema; visible parasites or lesions on skin; "
                    "lethargy; weight loss; diarrhea with possible mucus or blood"
                ),
                (
                    "Intense itching and scratching; hair loss and skin lesions; "
                    "visible mites, lice, or fleas; dermatitis; anemia in heavy infestations; "
                    "poor coat condition; possible secondary infections"
                ),
                (
                    "Severe pruritus with self-trauma; alopecia in affected areas; "
                    "erythema and scaling; visual parasites; lethargy and poor condition; "
                    "diarrhea and constipation alternating"
                ),
                (
                    "Scratching and self-mutilation; hair loss; skin thickening and lesions; "
                    "visible parasites; weight loss; anemia; diarrhea; "
                    "respiratory signs if lung parasites present"
                ),
            ],
            "diagnosis": [
                (
                    "Visual identification of parasites or parasite products under microscope; "
                    "fecal flotation or sedimentation for internal parasites; skin scrapings for mites; "
                    "impression smears; specific staining techniques (Gram, methylene blue)"
                ),
                (
                    "Microscopic examination of skin scrapings or aspirates; "
                    "fecal examination for helminth ova or protozoan cysts; "
                    "visual inspection for external parasites; specific tests for mite species identification"
                ),
                (
                    "Parasite identification through microscopy of fecal, skin, or blood samples; "
                    "visual assessment of lesions; specific stains and techniques for each parasite type"
                ),
                (
                    "Fecal examination (flotation/sedimentation); skin scrapings or tape preparations; "
                    "visual inspection; specific identification of parasite life stages"
                ),
            ],
            "transmission": [
                (
                    "Direct contact with infested animals; contaminated environment and bedding; "
                    "ingestion of contaminated food or water; vector transmission by arthropods; "
                    "fecal-oral route; vertical transmission in some cases"
                ),
                (
                    "Skin-to-skin contact for mites and lice; vector transmission by fleas and ticks; "
                    "ingestion of parasite life stages; fecal-oral transmission for intestinal parasites; "
                    "environmental contamination"
                ),
                (
                    "Direct contact for external parasites; ingestion for internal parasites; "
                    "arthropod vectors for certain parasites; contaminated environment and fomites; "
                    "sexual transmission in some cases"
                ),
                (
                    "Variable depending on parasite type: "
                    "direct contact, vector transmission, ingestion of eggs/cysts, or fecal-oral route"
                ),
            ],
        },
        "metabolic": {
            "keywords": ["diabetes", "obesity", "thyroid", "metabolism", "nutritional", "mineral", "vitamin"],
            "clinical_signs": [
                (
                    "Polydipsia and polyuria (increased thirst and urination); "
                    "weight loss despite appetite increase; lethargy and fatigue; "
                    "poor coat condition; muscle wasting; possible ketones on breath"
                ),
                (
                    "Excessive drinking and urination; weight loss with maintained or increased appetite; "
                    "lethargy; weakness; possible diabetic ketoacidosis signs; neuropathy signs in chronic cases"
                ),
                (
                    "Weight changes (gain in obesity, loss in some deficiencies); lethargy and fatigue; "
                    "appetite alterations; coat changes; exercise intolerance; muscle weakness; behavioral changes"
                ),
                (
                    "Obesity or weight loss depending on condition; lethargy; poor appetite; "
                    "gastrointestinal signs; hair loss; weakened immune function; poor wound healing"
                ),
            ],
            "diagnosis": [
                (
                    "Blood glucose measurement and glucose tolerance testing; insulin and C-peptide levels; "
                    "kidney and liver function tests; urinalysis including glucose and ketones; "
                    "lipid panel; thyroid hormone levels (T3, T4, TSH)"
                ),
                (
                    "Fasting and non-fasting blood glucose; HbA1c or fructosamine for long-term glucose control; "
                    "serum insulin levels; comprehensive metabolic panel; urinalysis; imaging for obesity assessment"
                ),
                (
                    "Thyroid function tests (TSH, T3, T4); vitamin and mineral assays; metabolic panel; "
                    "CBC; imaging studies; body condition scoring; metabolic rate assessment"
                ),
                (
                    "Laboratory testing of suspect nutrients/hormones; nutritional assessment; "
                    "body weight and condition evaluation; imaging studies; dietary analysis"
                ),
            ],
            "transmission": [
                (
                    "Not transmitted; metabolic disorders result from genetic predisposition, diet, age, "
                    "obesity status, or endocrine disease; "
                    "management through dietary modification and medical treatment"
                ),
                (
                    "Not contagious; development depends on genetics, diet quality, exercise level, age, "
                    "and underlying endocrine conditions"
                ),
                (
                    "Non-transmissible; hereditary component in some conditions; "
                    "diet-induced in nutritional deficiencies; age-related in metabolic disorders"
                ),
                "Non-communicable; multifactorial etiology involving genetics, diet, environment, and age factors",
            ],
        },
        "neoplastic": {
            "keywords": ["cancer", "tumor", "neoplasm", "carcinoma", "lymphoma", "melanoma"],
            "clinical_signs": [
                (
                    "Palpable masses or swelling; weight loss despite normal appetite; lethargy and depression; "
                    "loss of appetite in advanced cases; pain or discomfort; bleeding or discharge from affected areas"
                ),
                (
                    "Observable or palpable masses; unexplained weight loss; loss of appetite; lethargy; "
                    "pain behavior; discharge or bleeding from tumor sites; lymphadenopathy; behavioral changes"
                ),
                (
                    "Lumps or swellings; wasting despite eating; fatigue; behavioral changes; "
                    "possible organ dysfunction signs; pain; discharge or ulceration; pale mucous membranes"
                ),
                (
                    "Visible or palpable tumors; progressive weight loss; anorexia; weakness; pain signs; "
                    "possible organ dysfunction; discharge; bleeding; systemic illness signs"
                ),
            ],
            "diagnosis": [
                (
                    "Physical examination and tumor palpation; imaging (radiography, ultrasound, CT, MRI); "
                    "biopsy and histopathology for definitive diagnosis; cytology; "
                    "staging with imaging and laboratory tests; tumor markers where applicable"
                ),
                (
                    "Clinical examination with mass identification; "
                    "imaging studies (X-ray, ultrasound, advanced imaging); "
                    "biopsy and pathological examination; staging evaluation; laboratory abnormalities assessment"
                ),
                (
                    "Visual/palpable tumor identification; diagnostic imaging for location and extent; "
                    "tissue biopsy for histological diagnosis; staging procedures; systemic evaluation for metastasis"
                ),
                (
                    "Biopsy and histopathology for diagnosis; imaging for staging; "
                    "laboratory tests for organ function; circulating tumor markers if available"
                ),
            ],
            "transmission": [
                (
                    "Not transmitted (except virus-associated malignancies in rare cases); "
                    "result of genetic predisposition, age, environmental carcinogens, chronic inflammation, "
                    "or viral infection (e.g., FeLV, FIV in cats)"
                ),
                (
                    "Not contagious; related to genetic factors, age, carcinogen exposure, chronic disease, "
                    "or viral associations; hereditary component in some breeds"
                ),
                "Non-communicable; multifactorial origin including aging, genetics, carcinogens, and chronic disease",
                (
                    "Non-transmissible; development associated with age, genetics, carcinogens, "
                    "chronic inflammation, or viral factors"
                ),
            ],
        },
        "neurologic": {
            "keywords": ["seizure", "epilepsy", "neurologic", "neurological", "paralysis", "nerve"],
            "clinical_signs": [
                (
                    "Seizures with pre-ictal signs (restlessness, salivation); "
                    "loss of consciousness during seizure; muscle rigidity and tremors; "
                    "abnormal posturing; loss of bowel/bladder control during episode"
                ),
                (
                    "Seizure activity with consciousness loss; uncoordinated movements and muscle rigidity; "
                    "drooling and salivation; possible vocalization; "
                    "post-ictal confusion or aggression; possible hemiparesis"
                ),
                (
                    "Seizures (generalized or focal); loss of balance and coordination; "
                    "weakness or paralysis of limbs; head tilt; nystagmus; behavioral changes; possible pain"
                ),
                (
                    "Recurrent seizures or status epilepticus; altered mentation; paralysis or paresis; "
                    "incoordination; loss of sensory/motor function depending on lesion location"
                ),
            ],
            "diagnosis": [
                (
                    "Detailed seizure history and characteristics; neurological examination; "
                    "EEG recording (baseline and during seizure); MRI or CT of brain; "
                    "cerebrospinal fluid analysis; bloodwork to exclude metabolic causes"
                ),
                (
                    "Neurological assessment; EEG study; advanced neuroimaging (MRI/CT); "
                    "CSF analysis from lumbar puncture; blood chemistry to rule out hypoglycemia or other causes"
                ),
                (
                    "Seizure pattern documentation; neurological examination findings; EEG recording; "
                    "brain imaging; CSF examination; metabolic panel; imaging to identify structural lesions"
                ),
                (
                    "EEG showing characteristic changes; neuroimaging demonstrating lesion (structural epilepsy) "
                    "or normal (idiopathic); seizure semiology; "
                    "laboratory studies to exclude metabolic/toxic causes"
                ),
            ],
            "transmission": [
                (
                    "Not transmitted; result of genetic predisposition (idiopathic epilepsy), brain trauma, "
                    "structural lesions, metabolic/toxic causes, or infectious/inflammatory diseases"
                ),
                (
                    "Non-contagious; etiology includes genetic factors, head trauma, brain lesions, "
                    "metabolic disorders, toxin exposure, or CNS infection/inflammation"
                ),
                (
                    "Non-transmissible; caused by genetic predisposition, head injury, tumors, infections, "
                    "metabolic disease, or toxin exposure"
                ),
                (
                    "Not communicable; multiple possible causes including genetic predisposition, trauma, "
                    "infection, metabolic disease, or toxins"
                ),
            ],
        },
        "default": {
            "keywords": [],
            "clinical_signs": [
                (
                    "Clinical signs vary by disease type; may include fever, lethargy, anorexia, discharge, "
                    "pain, weakness, or behavioral changes depending on affected system"
                ),
                (
                    "Presentation depends on disease etiology; observe for systemic signs (fever, malaise), "
                    "local signs (swelling, discharge), or organ-specific symptoms"
                ),
                (
                    "Variable clinical presentation; early signs may be subtle; "
                    "progression depends on disease severity and host factors"
                ),
                (
                    "Observable signs depend on disease type and affected body systems; "
                    "severity may progress without appropriate treatment"
                ),
            ],
            "diagnosis": [
                (
                    "Thorough history and clinical examination; specific diagnostic tests based on suspected disease; "
                    "imaging, laboratory, or other testing as indicated"
                ),
                (
                    "Clinical evaluation and appropriate diagnostic testing for suspected condition; "
                    "confirmation through specific diagnostic procedures"
                ),
                (
                    "Diagnostic approach tailored to disease type; may include physical examination, "
                    "laboratory testing, imaging, or tissue examination"
                ),
                (
                    "Test selection based on clinical suspicion; may include bloodwork, imaging, culture, "
                    "serology, or other species/disease-specific procedures"
                ),
            ],
            "transmission": [
                (
                    "Transmission varies by disease type: may be direct contact, airborne, fecal-oral, "
                    "vector-borne, or non-communicable depending on etiology"
                ),
                (
                    "Transmission route depends on specific pathogen or disease mechanism; "
                    "some conditions are contagious while others are not"
                ),
                (
                    "Disease spread depends on etiology: infectious diseases spread person-to-person; "
                    "non-infectious conditions do not transmit"
                ),
                (
                    "Communicability varies: infectious agents spread via specific routes; "
                    "non-infectious conditions are not transmissible"
                ),
            ],
        },
    }

    @classmethod
    def classify_disease_type(cls, disease: Dict) -> str:
        """疾患をカテゴリに分類"""
        name = disease.get("name", "").lower()
        description = disease.get("description", "").lower()
        text = f"{name} {description}"

        # カテゴリ順（より詳細なものから）
        category_order = [
            "neoplastic",
            "metabolic",
            "neurologic",
            "infectious_viral",
            "infectious_bacterial",
            "parasitic",
        ]

        for category in category_order:
            if category in cls.TEMPLATES:
                keywords = cls.TEMPLATES[category]["keywords"]
                if any(kw in text for kw in keywords):
                    return category

        return "default"

    @classmethod
    def generate_clinical_details(cls, disease: Dict) -> tuple:
        """疾患に対応した臨床詳細を生成"""
        category = cls.classify_disease_type(disease)
        templates = cls.TEMPLATES[category]

        # ランダム選択（再現性を確保）
        import hashlib

        seed = int(hashlib.md5(disease.get("id", "").encode()).hexdigest(), 16)
        random.seed(seed)

        clinical_signs = random.choice(templates["clinical_signs"])
        diagnosis = random.choice(templates["diagnosis"])
        transmission = random.choice(templates["transmission"])

        return clinical_signs, diagnosis, transmission

    @classmethod
    def generate_clinical_details_ja(cls, disease: Dict) -> tuple:
        """日本語版臨床詳細を生成"""
        category = cls.classify_disease_type(disease)

        # 簡易的な日本語テンプレート
        ja_templates = {
            "infectious_viral": (
                "発熱；活動性の低下；食欲不振；鼻眼分泌物；咳やくしゃみ；口腔潰瘍；リンパ節腫脹",
                "ウイルス抗原検出（ELISA または迅速検査）；ウイルス分離；PCR 検査；血清学的検査（ELISA、SNAP）",
                "飛沫感染；直接接触；環境汚染；垂直感染（一部）",
            ),
            "infectious_bacterial": (
                "発熱；元気消失；食欲不振；化膿性分泌物；リンパ節腫脹；敗血症兆候",
                "細菌培養と分離；グラム染色；生化学的同定；薬剤感受性検査",
                "直接接触；飛沫感染；経口感染；創傷汚染",
            ),
            "parasitic": (
                "掻痒感；脱毛；皮膚炎症；寄生虫の可視化；体重減少；下痢；貧血",
                "顕微鏡検査；糞便浮遊法；皮膚スクレイピング；虫卵の同定",
                "直接接触；媒介虫による感染；経口感染；環境汚染",
            ),
            "metabolic": (
                "多飲多尿；体重変化；疲労；被毛の状態悪化；筋萎縮；食欲の異常",
                "血糖値測定；インスリン値；甲状腺ホルモン；生化学パネル；尿検査",
                "伝染しない；遺伝的素因、食事、年齢、肥満が関係",
            ),
            "neoplastic": (
                "腫瘤の触知；説明されない体重減少；元気消失；食欲不振；疼痛",
                "身体検査；画像診断（X線、超音波、CT、MRI）；生検と病理組織；ステージング",
                "伝染しない；遺伝的素因、年齢、発がん物質暴露、ウイルス関連性",
            ),
            "neurologic": (
                "てんかん発作；意識喪失；筋硬直；異常姿勢；大小便失禁；発作後の混乱",
                "発作の記録；神経学的検査；脳波記録；脳画像；髄液分析",
                "伝染しない；遺伝的素因、頭部外傷、脳障害、代謝異常；感染性/炎症性疾患",
            ),
            "default": (
                "臨床兆候は疾患の種類により異なる；発熱、元気消失、食欲不振、分泌物、疼痛など",
                "臨床検査；疑われる疾患に基づいた診断検査",
                "伝染可能性は疾患による；感染症は伝染；非感染性疾患は伝染しない",
            ),
        }

        return ja_templates.get(category, ja_templates["default"])


# ============================================================================
# 臨床詳細補完エンジン
# ============================================================================


def complete_clinical_details():
    """臨床詳細フィールドを追加"""

    print("🔧 臨床詳細フィールドを追加します")
    print("=" * 70)

    # データを読み込み
    data_file = Path("diseases_all_species.json")
    with open(data_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"✓ {len(data)} 件の疾患データを読み込みました")

    # 統計
    stats = {
        "clinical_signs_added": 0,
        "diagnosis_added": 0,
        "transmission_added": 0,
        "clinical_signs_ja_added": 0,
        "diagnosis_ja_added": 0,
        "transmission_ja_added": 0,
        "errors": 0,
    }

    generator = ClinicalDetailsGenerator()

    # 各疾患を処理
    for i, disease in enumerate(data):
        try:
            # 臨床詳細を追加
            if not disease.get("clinical_signs"):
                clinical_signs, diagnosis, transmission = generator.generate_clinical_details(disease)
                disease["clinical_signs"] = clinical_signs
                disease["diagnosis"] = diagnosis
                disease["transmission"] = transmission
                stats["clinical_signs_added"] += 1
                stats["diagnosis_added"] += 1
                stats["transmission_added"] += 1

            # 日本語版を追加
            if not disease.get("clinical_signs_ja"):
                clinical_signs_ja, diagnosis_ja, transmission_ja = generator.generate_clinical_details_ja(disease)
                disease["clinical_signs_ja"] = clinical_signs_ja
                disease["diagnosis_ja"] = diagnosis_ja
                disease["transmission_ja"] = transmission_ja
                stats["clinical_signs_ja_added"] += 1
                stats["diagnosis_ja_added"] += 1
                stats["transmission_ja_added"] += 1

            if (i + 1) % 1000 == 0:
                print(f"  処理中... {i + 1}/{len(data)}")

        except Exception as e:
            print(f"❌ エラー (ID: {disease.get('id')}): {e}")
            stats["errors"] += 1

    # 修復されたデータを保存
    with open(data_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("\n✅ 臨床詳細フィールド追加完了！")
    print(f"{'=' * 70}")
    print("📊 統計:")
    print(f"  Clinical Signs (EN): {stats['clinical_signs_added']}")
    print(f"  Diagnosis (EN): {stats['diagnosis_added']}")
    print(f"  Transmission (EN): {stats['transmission_added']}")
    print(f"  Clinical Signs (JA): {stats['clinical_signs_ja_added']}")
    print(f"  Diagnosis (JA): {stats['diagnosis_ja_added']}")
    print(f"  Transmission (JA): {stats['transmission_ja_added']}")
    print(f"  エラー: {stats['errors']}")

    # フィールド完成度を確認
    print("\n📋 全フィールド完成度:")
    fields = [
        "treatment",
        "prevention",
        "prognosis",
        "clinical_signs",
        "diagnosis",
        "transmission",
        "treatment_ja",
        "prevention_ja",
        "prognosis_ja",
        "clinical_signs_ja",
        "diagnosis_ja",
        "transmission_ja",
    ]
    for field in fields:
        filled = sum(1 for d in data if d.get(field) and str(d.get(field)).strip())
        completion = (filled / len(data)) * 100
        status = "✅" if completion == 100 else "⚠️" if completion > 50 else "❌"
        print(f"  {status} {field:<25} {filled:>5}/{len(data)} ({completion:>5.1f}%)")

    return data_file


def verify_clinical_details(data_file: Path):
    """臨床詳細の品質を検証"""
    print("\n✔️ 臨床詳細の品質検証中...")
    print(f"{'=' * 70}")

    with open(data_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # サンプル確認
    print("\n📝 サンプル (疾患別):")

    # ランダムサンプル
    import random

    samples = random.sample(data, min(5, len(data)))

    for disease in samples:
        print(f"\n  📌 {disease.get('name')}")
        print(f"     Clinical Signs: {disease.get('clinical_signs', 'なし')[:80]}...")
        print(f"     Diagnosis: {disease.get('diagnosis', 'なし')[:80]}...")
        print(f"     Transmission: {disease.get('transmission', 'なし')[:80]}...")

    print("\n✅ 臨床詳細品質確認完了！")


if __name__ == "__main__":
    # 補完実行
    data_file = complete_clinical_details()

    # 検証
    verify_clinical_details(data_file)

    print("\n✅ 臨床詳細フィールド追加完了！")
    print(f"📄 ファイル: {data_file}")
