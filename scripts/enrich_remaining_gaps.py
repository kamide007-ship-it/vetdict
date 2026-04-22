#!/usr/bin/env python3
"""Fill remaining gaps in disease databases:

1. Add recommended_tests to diseases_all_species.json (6,393 entries)
2. Add transmission/clinical_signs/diagnosis to supplementary_diseases.json (2,256 entries)
"""

import json
import os
from collections import Counter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAIN_JSON = os.path.join(ROOT, "diseases_all_species.json")
SUPP_JSON = os.path.join(ROOT, "api", "data", "supplementary_diseases.json")

# Import classifier from existing script
import sys

sys.path.insert(0, os.path.join(ROOT, "scripts"))
from enrich_all_diseases import classify_disease

# ============================================================================
# Category-specific recommended tests (bilingual)
# ============================================================================

_CATEGORY_TESTS: dict[str, list[str]] = {
    "viral": [
        "ウイルスPCR検査 (Viral PCR)",
        "ウイルス抗体価検査 (Viral Antibody Titer)",
        "全血球計算 (CBC)",
        "血液生化学検査 (Blood Chemistry Panel)",
    ],
    "bacterial": [
        "細菌培養・感受性試験 (Bacterial Culture & Sensitivity)",
        "全血球計算 (CBC)",
        "血液生化学検査 (Blood Chemistry Panel)",
        "グラム染色 (Gram Stain)",
    ],
    "fungal": [
        "真菌培養 (Fungal Culture)",
        "ウッド灯検査 (Wood's Lamp Examination)",
        "細胞診 (Cytology)",
        "全血球計算 (CBC)",
    ],
    "parasitic": [
        "糞便検査 (Fecal Examination)",
        "糞便浮遊法 (Fecal Flotation)",
        "全血球計算 (CBC)",
        "皮膚掻爬検査 (Skin Scraping)",
    ],
    "neoplastic": [
        "細胞診 (Cytology/Fine Needle Aspirate)",
        "病理組織検査 (Histopathology/Biopsy)",
        "画像診断 (Diagnostic Imaging: X-ray/Ultrasound)",
        "全血球計算 (CBC)",
        "血液生化学検査 (Blood Chemistry Panel)",
    ],
    "metabolic": [
        "血液生化学検査 (Blood Chemistry Panel)",
        "ホルモン検査 (Hormone Assay)",
        "尿検査 (Urinalysis)",
        "全血球計算 (CBC)",
    ],
    "nutritional": [
        "血液生化学検査 (Blood Chemistry Panel)",
        "全血球計算 (CBC)",
        "レントゲン検査 (Radiography)",
        "尿検査 (Urinalysis)",
    ],
    "toxic": [
        "血液生化学検査 (Blood Chemistry Panel: Liver/Kidney)",
        "全血球計算 (CBC)",
        "凝固検査 (Coagulation Panel)",
        "尿検査 (Urinalysis)",
        "毒物スクリーニング (Toxicology Screening)",
    ],
    "traumatic": [
        "レントゲン検査 (Radiography)",
        "超音波検査 (Ultrasonography/FAST scan)",
        "全血球計算 (CBC)",
        "血液生化学検査 (Blood Chemistry Panel)",
    ],
    "dental": [
        "口腔内検査 (Oral Examination)",
        "歯科レントゲン (Dental Radiography)",
        "全血球計算 (CBC)",
        "細菌培養 (Bacterial Culture)",
    ],
    "autoimmune": [
        "全血球計算 (CBC)",
        "抗核抗体検査 (ANA Test)",
        "皮膚生検 (Skin Biopsy)",
        "血液生化学検査 (Blood Chemistry Panel)",
        "免疫学的検査 (Immunological Panel)",
    ],
    "cardiovascular": [
        "心エコー検査 (Echocardiography)",
        "心電図 (Electrocardiography/ECG)",
        "胸部レントゲン (Thoracic Radiography)",
        "血圧測定 (Blood Pressure Measurement)",
        "全血球計算 (CBC)",
    ],
    "respiratory": [
        "胸部レントゲン (Thoracic Radiography)",
        "全血球計算 (CBC)",
        "動脈血ガス分析 (Arterial Blood Gas)",
        "気管洗浄液検査 (Tracheal Wash/BAL)",
    ],
    "renal": [
        "血液生化学検査 (Blood Chemistry Panel: BUN/Creatinine)",
        "尿検査 (Urinalysis)",
        "超音波検査 (Ultrasonography)",
        "全血球計算 (CBC)",
    ],
    "gastrointestinal": [
        "腹部レントゲン (Abdominal Radiography)",
        "腹部超音波検査 (Abdominal Ultrasonography)",
        "血液生化学検査 (Blood Chemistry Panel)",
        "全血球計算 (CBC)",
        "糞便検査 (Fecal Examination)",
    ],
    "reproductive": [
        "超音波検査 (Ultrasonography)",
        "ホルモン検査 (Hormone Assay)",
        "全血球計算 (CBC)",
        "血液生化学検査 (Blood Chemistry Panel)",
        "細胞診 (Vaginal Cytology)",
    ],
    "neurological": [
        "神経学的検査 (Neurological Examination)",
        "MRI/CT検査 (MRI/CT Imaging)",
        "脳脊髄液検査 (CSF Analysis)",
        "全血球計算 (CBC)",
        "血液生化学検査 (Blood Chemistry Panel)",
    ],
    "dermatological": [
        "皮膚掻爬検査 (Skin Scraping)",
        "細胞診 (Cytology)",
        "真菌培養 (Fungal Culture/DTM)",
        "皮膚生検 (Skin Biopsy)",
        "全血球計算 (CBC)",
    ],
    "ophthalmic": [
        "眼圧測定 (Tonometry)",
        "スリットランプ検査 (Slit Lamp Examination)",
        "眼底検査 (Fundoscopy)",
        "フルオレセイン染色 (Fluorescein Staining)",
        "シルマー試験 (Schirmer Tear Test)",
    ],
    "orthopedic": [
        "レントゲン検査 (Radiography)",
        "関節液検査 (Joint Fluid Analysis/Arthrocentesis)",
        "CT検査 (CT Imaging)",
        "全血球計算 (CBC)",
    ],
    "congenital": [
        "レントゲン検査 (Radiography)",
        "超音波検査 (Ultrasonography)",
        "血液生化学検査 (Blood Chemistry Panel)",
        "遺伝子検査 (Genetic Testing)",
    ],
    "behavioral": [
        "全血球計算 (CBC)",
        "血液生化学検査 (Blood Chemistry Panel)",
        "甲状腺機能検査 (Thyroid Function Test)",
        "尿検査 (Urinalysis)",
    ],
    "hematological": [
        "全血球計算 (CBC)",
        "血液塗抹検査 (Blood Smear Evaluation)",
        "凝固検査 (Coagulation Panel)",
        "血液生化学検査 (Blood Chemistry Panel)",
        "骨髄検査 (Bone Marrow Aspirate/Biopsy)",
    ],
}

_DEFAULT_TESTS = [
    "全血球計算 (CBC)",
    "血液生化学検査 (Blood Chemistry Panel)",
    "レントゲン検査 (Radiography)",
    "尿検査 (Urinalysis)",
]

# ============================================================================
# Category-specific transmission templates (bilingual)
# ============================================================================

_TRANSMISSION_TEMPLATES: dict[str, tuple[str, str]] = {
    "viral": (
        "Transmitted through direct contact with infected animals, aerosol droplets, "
        "fomites, or contaminated environments. Some viruses may be transmitted via "
        "vectors (insects) or vertically from mother to offspring.",
        "感染動物との直接接触、飛沫、汚染物、汚染環境を介して伝播する。"
        "一部のウイルスは媒介動物（昆虫）を介して、または母子垂直感染で伝播する。",
    ),
    "bacterial": (
        "Transmitted through direct contact with infected animals or contaminated "
        "environments, ingestion of contaminated food or water, wound contamination, "
        "or aerosol transmission. Some bacteria can survive in the environment for extended periods.",
        "感染動物や汚染環境との直接接触、汚染された食物・水の摂取、"
        "創傷汚染、飛沫感染を介して伝播する。一部の細菌は環境中で長期間生存できる。",
    ),
    "fungal": (
        "Transmitted through contact with fungal spores in the environment, "
        "contaminated soil, infected animals, or fomites. Spores can remain viable "
        "in the environment for months to years.",
        "環境中の真菌胞子、汚染された土壌、感染動物、汚染物との接触で伝播する。"
        "胞子は環境中で数ヶ月〜数年間生存可能である。",
    ),
    "parasitic": (
        "Transmitted through ingestion of parasitic eggs/larvae, direct contact with "
        "infected animals, vector-mediated transmission (fleas, ticks, mosquitoes), "
        "or penetration of larvae through skin.",
        "寄生虫卵・幼虫の経口摂取、感染動物との直接接触、"
        "媒介動物（ノミ、ダニ、蚊）による伝播、幼虫の経皮侵入で伝播する。",
    ),
    "neoplastic": (
        "Not directly transmissible between animals in most cases. Certain virus-associated "
        "tumors (e.g., FeLV-associated lymphoma) may be indirectly transmissible through "
        "the causative viral agent. Genetic predisposition may increase risk in certain breeds.",
        "ほとんどの場合、動物間で直接伝播しない。特定のウイルス関連腫瘍"
        "（例：FeLV関連リンパ腫）は原因ウイルスを介して間接的に伝播しうる。"
        "遺伝的素因により特定品種でリスクが高まることがある。",
    ),
    "metabolic": (
        "Not transmissible. Metabolic and endocrine disorders arise from internal "
        "physiological dysfunction, genetic predisposition, dietary factors, or "
        "age-related changes.",
        "伝播性はない。代謝・内分泌疾患は内因性の生理的機能障害、遺伝的素因、食事因子、加齢変化により発生する。",
    ),
    "nutritional": (
        "Not transmissible. Nutritional disorders result from dietary imbalances, "
        "inappropriate feeding, or individual malabsorption conditions.",
        "伝播性はない。栄養障害は食事の不均衡、不適切な給餌、個体の吸収不良により発生する。",
    ),
    "toxic": (
        "Not transmissible between animals. Toxicosis results from exposure to "
        "environmental toxins, ingestion of toxic substances, or contact with "
        "poisonous organisms.",
        "動物間で伝播しない。中毒は環境毒素への曝露、有毒物質の摂取、有毒生物との接触により発生する。",
    ),
    "traumatic": (
        "Not transmissible. Traumatic conditions result from physical injury, environmental hazards, or accidents.",
        "伝播性はない。外傷性疾患は物理的損傷、環境的危険、事故により発生する。",
    ),
    "dental": (
        "Not directly transmissible. Dental conditions arise from anatomical factors, "
        "dietary influences, genetic predisposition, or secondary to other diseases. "
        "Periodontal bacteria may be shared between cohabiting animals.",
        "直接伝播しない。歯科疾患は解剖学的要因、食事の影響、遺伝的素因、"
        "他疾患の続発症として発生する。歯周病菌は同居動物間で共有されることがある。",
    ),
    "autoimmune": (
        "Not transmissible. Immune-mediated conditions arise from genetic predisposition "
        "and environmental triggers that cause immune system dysregulation.",
        "伝播性はない。免疫介在性疾患は遺伝的素因と免疫系の調節障害を引き起こす環境トリガーにより発生する。",
    ),
    "cardiovascular": (
        "Not transmissible in most cases. Cardiovascular disease arises from genetic "
        "predisposition, age-related degeneration, or secondary to other systemic diseases. "
        "Infectious endocarditis may result from bacteremia.",
        "ほとんどの場合伝播しない。心血管疾患は遺伝的素因、加齢性変性、"
        "他の全身性疾患の続発症として生じる。感染性心内膜炎は菌血症に起因しうる。",
    ),
    "respiratory": (
        "Many respiratory diseases are transmitted via aerosol droplets, direct contact, "
        "or contaminated environments. Infectious agents spread rapidly in crowded "
        "or poorly ventilated conditions.",
        "多くの呼吸器疾患は飛沫、直接接触、汚染環境を介して伝播する。"
        "感染性病原体は過密状態や換気不良の環境で急速に拡散する。",
    ),
    "renal": (
        "Not directly transmissible. Renal diseases arise from genetic predisposition, "
        "toxin exposure, infectious agents, dietary factors, or age-related degeneration.",
        "直接伝播しない。腎疾患は遺伝的素因、毒素曝露、感染性病原体、食事因子、加齢性変性により発生する。",
    ),
    "gastrointestinal": (
        "Infectious GI diseases may be transmitted through the fecal-oral route, "
        "contaminated food or water, or direct contact. Non-infectious GI conditions "
        "are not transmissible.",
        "感染性消化器疾患は糞口感染、汚染された食物・水、直接接触を介して"
        "伝播しうる。非感染性消化器疾患は伝播性がない。",
    ),
    "reproductive": (
        "Some reproductive infections may be transmitted through mating, direct contact, "
        "or vertically from mother to offspring. Non-infectious reproductive conditions "
        "are not transmissible.",
        "一部の生殖器感染症は交配、直接接触、母子垂直感染で伝播しうる。非感染性の生殖器疾患は伝播性がない。",
    ),
    "neurological": (
        "Most neurological conditions are not directly transmissible. Certain infectious "
        "causes (e.g., rabies, encephalitis viruses) may be transmitted through bites, "
        "vectors, or direct contact.",
        "ほとんどの神経疾患は直接伝播しない。特定の感染性原因"
        "（例：狂犬病、脳炎ウイルス）は咬傷、媒介動物、直接接触で伝播しうる。",
    ),
    "dermatological": (
        "Some dermatological conditions (fungal, parasitic) are transmissible through "
        "direct contact or contaminated environments. Non-infectious skin conditions "
        "are not transmissible.",
        "一部の皮膚疾患（真菌性、寄生虫性）は直接接触や汚染環境を介して伝播する。非感染性の皮膚疾患は伝播性がない。",
    ),
    "ophthalmic": (
        "Most ophthalmic conditions are not directly transmissible. Infectious "
        "conjunctivitis or keratitis may spread through direct contact or fomites.",
        "ほとんどの眼科疾患は直接伝播しない。感染性結膜炎や角膜炎は直接接触や汚染物を介して拡散しうる。",
    ),
    "orthopedic": (
        "Not transmissible. Orthopedic conditions arise from genetic predisposition, "
        "developmental abnormalities, degenerative changes, or traumatic injury.",
        "伝播性はない。整形外科疾患は遺伝的素因、発達異常、変性変化、外傷により発生する。",
    ),
    "congenital": (
        "Not transmissible. Congenital conditions result from genetic mutations, "
        "developmental errors during embryogenesis, or teratogenic exposures.",
        "伝播性はない。先天性疾患は遺伝子変異、胚発生中の発達異常、催奇形因子への曝露により発生する。",
    ),
    "behavioral": (
        "Not transmissible. Behavioral conditions arise from neurochemical imbalances, "
        "environmental stressors, inadequate socialization, or learned behaviors.",
        "伝播性はない。行動疾患は神経化学的不均衡、環境ストレス、不適切な社会化、学習行動により発生する。",
    ),
    "hematological": (
        "Most hematological conditions are not directly transmissible. Blood-borne "
        "infectious agents causing hematological changes may be transmitted via "
        "vectors, blood contact, or transplacentally.",
        "ほとんどの血液疾患は直接伝播しない。血液学的変化を引き起こす"
        "血液媒介性感染性病原体は媒介動物、血液接触、経胎盤的に伝播しうる。",
    ),
}

_DEFAULT_TRANSMISSION = (
    "Transmissibility varies depending on the specific etiology. Infectious causes "
    "may be transmissible through direct contact, aerosol, fecal-oral route, or vectors. "
    "Non-infectious causes are not transmissible.",
    "伝播性は原因により異なる。感染性の原因は直接接触、飛沫、糞口感染、"
    "媒介動物を介して伝播しうる。非感染性の原因は伝播性がない。",
)

# ============================================================================
# Category-specific clinical signs templates
# ============================================================================

_CLINICAL_SIGNS_TEMPLATES: dict[str, tuple[str, str]] = {
    "viral": (
        "Fever, lethargy, anorexia, nasal/ocular discharge, respiratory signs, "
        "diarrhea/vomiting (depending on tropism), lymphadenopathy, dehydration. "
        "Species-specific signs may include skin lesions, neurological signs, or hemorrhage.",
        "発熱、無気力、食欲不振、鼻汁・眼脂、呼吸器症状、下痢・嘔吐（指向性により異なる）、"
        "リンパ節腫大、脱水。種特異的徴候として皮膚病変、神経症状、出血が見られることがある。",
    ),
    "bacterial": (
        "Fever, localized swelling/redness/heat/pain, purulent discharge, lethargy, "
        "anorexia, elevated white blood cell count. Specific signs depend on organ system affected.",
        "発熱、局所の腫脹・発赤・熱感・疼痛、膿性分泌物、無気力、食欲不振、"
        "白血球数増加。臓器特異的な徴候は罹患臓器系に依存する。",
    ),
    "fungal": (
        "Skin lesions (alopecia, crusting, scaling), nasal discharge, respiratory distress, "
        "subcutaneous nodules, lymphadenopathy, fever, weight loss. "
        "Systemic mycoses may cause multi-organ involvement.",
        "皮膚病変（脱毛、痂皮、鱗屑）、鼻汁、呼吸困難、皮下結節、リンパ節腫大、"
        "発熱、体重減少。全身性真菌症では多臓器障害を引き起こしうる。",
    ),
    "parasitic": (
        "Pruritus, skin lesions, hair/feather loss, diarrhea, weight loss, anemia, "
        "poor coat/feather condition, visible parasites or eggs, pot-bellied appearance "
        "in heavy infestations.",
        "掻痒、皮膚病変、脱毛・脱羽、下痢、体重減少、貧血、被毛・羽毛の悪化、"
        "寄生虫・虫卵の目視、重度寄生では腹部膨満が見られる。",
    ),
    "neoplastic": (
        "Palpable mass or swelling, weight loss, decreased appetite, lethargy, "
        "organ-specific signs depending on tumor location, paraneoplastic syndromes "
        "(hypercalcemia, anemia, cachexia).",
        "触知可能な腫瘤・腫脹、体重減少、食欲低下、無気力、"
        "腫瘍部位に応じた臓器特異的徴候、腫瘍随伴症候群"
        "（高カルシウム血症、貧血、悪液質）。",
    ),
    "metabolic": (
        "Polyuria/polydipsia, weight changes, changes in appetite, lethargy, skin/coat changes, "
        "muscle weakness, altered mentation. Specific signs depend on the affected endocrine axis.",
        "多尿・多飲、体重変化、食欲変化、無気力、皮膚・被毛変化、"
        "筋力低下、意識状態の変化。特異的徴候は障害された内分泌軸に依存する。",
    ),
    "nutritional": (
        "Poor growth, weight loss/obesity, dull coat, lethargy, skeletal abnormalities "
        "(MBD), weakness, reproductive failure, organ-specific signs related to "
        "the deficient or excess nutrient.",
        "成長不良、体重減少/肥満、被毛の悪化、無気力、骨格異常（MBD）、"
        "衰弱、繁殖障害、欠乏または過剰な栄養素に関連した臓器特異的徴候。",
    ),
    "toxic": (
        "Acute onset vomiting, diarrhea, tremors, seizures, hypersalivation, "
        "ataxia, collapse, dyspnea. Signs vary by toxin and may include bleeding, "
        "organ-specific failure (hepatic, renal), or death.",
        "急性発症の嘔吐、下痢、振戦、痙攣、流涎過多、運動失調、虚脱、呼吸困難。"
        "毒物により徴候は異なり、出血、臓器特異的不全（肝、腎）、死亡を含みうる。",
    ),
    "traumatic": (
        "Pain, swelling, bruising, bleeding, limping/lameness, reduced mobility, "
        "wound or tissue damage visible, behavioral changes (hiding, aggression), "
        "shock signs in severe cases.",
        "疼痛、腫脹、打撲、出血、跛行、運動性低下、創傷・組織損傷の視認、"
        "行動変化（隠れる、攻撃性）、重症例ではショック徴候。",
    ),
    "dental": (
        "Dysphagia, reduced food intake, ptyalism/drooling, facial swelling, "
        "weight loss, halitosis, preference for soft foods, teeth chattering, "
        "visible tooth abnormalities on examination.",
        "嚥下困難、食餌量減少、流涎、顔面腫脹、体重減少、口臭、軟食の選好、歯ぎしり、検査での歯の異常。",
    ),
    "autoimmune": (
        "Skin lesions (crusting, ulceration, vesicles), joint pain/swelling, "
        "mucosal erosions, fever, lethargy, lymphadenopathy, organ-specific dysfunction "
        "depending on the target tissue.",
        "皮膚病変（痂皮、潰瘍、水疱）、関節痛・腫脹、粘膜びらん、"
        "発熱、無気力、リンパ節腫大、標的組織に応じた臓器特異的機能障害。",
    ),
    "cardiovascular": (
        "Exercise intolerance, coughing, dyspnea, syncope, ascites, cyanosis, "
        "weak pulse, heart murmur or arrhythmia on auscultation, jugular distension.",
        "運動不耐性、咳嗽、呼吸困難、失神、腹水、チアノーゼ、脈拍微弱、聴診での心雑音・不整脈、頸静脈怒張。",
    ),
    "respiratory": (
        "Dyspnea, tachypnea, coughing, nasal discharge, open-mouth breathing, "
        "wheezing/crackles on auscultation, exercise intolerance, cyanosis, "
        "tail-bobbing (birds).",
        "呼吸困難、頻呼吸、咳嗽、鼻汁、開口呼吸、聴診でのラ音・断続性ラ音、"
        "運動不耐性、チアノーゼ、尾振り呼吸（鳥類）。",
    ),
    "renal": (
        "Polyuria/polydipsia, decreased appetite, weight loss, vomiting, dehydration, "
        "uremic breath, oral ulcers, hematuria, stranguria, anuria in obstruction.",
        "多尿・多飲、食欲低下、体重減少、嘔吐、脱水、尿毒症性口臭、口腔潰瘍、血尿、排尿困難、閉塞時の無尿。",
    ),
    "gastrointestinal": (
        "Vomiting, diarrhea, anorexia, weight loss, abdominal pain/distension, "
        "dehydration, melena or hematochezia, tenesmus, changes in fecal consistency.",
        "嘔吐、下痢、食欲不振、体重減少、腹痛・腹部膨満、脱水、黒色便・血便、しぶり、便性状の変化。",
    ),
    "reproductive": (
        "Vulvar/preputial discharge, dystocia, mammary swelling, infertility, "
        "behavioral changes, abdominal distension, straining, egg binding (birds/reptiles).",
        "外陰部・包皮分泌物、難産、乳腺腫脹、不妊、行動変化、腹部膨満、怒責、卵づまり（鳥類・爬虫類）。",
    ),
    "neurological": (
        "Seizures, ataxia, head tilt, circling, paralysis/paresis, tremors, "
        "altered mentation, abnormal reflexes, nystagmus, behavioral changes.",
        "痙攣、運動失調、斜頸、旋回、麻痺・不全麻痺、振戦、意識状態の変化、異常反射、眼振、行動変化。",
    ),
    "dermatological": (
        "Alopecia, erythema, pruritus, scaling/crusting, papules/pustules, "
        "hyperpigmentation, lichenification, secondary excoriation, malodor.",
        "脱毛、紅斑、掻痒、鱗屑・痂皮、丘疹・膿疱、色素沈着、苔癬化、二次的擦過傷、悪臭。",
    ),
    "ophthalmic": (
        "Blepharospasm, epiphora, conjunctival hyperemia, corneal opacity, "
        "ocular discharge, photophobia, vision changes, enlarged/shrunken globe.",
        "眼瞼痙攣、流涙、結膜充血、角膜混濁、眼脂、羞明、視力変化、眼球の腫大・萎縮。",
    ),
    "orthopedic": (
        "Lameness, joint swelling, stiffness, reduced range of motion, crepitus, "
        "reluctance to move/jump, muscle atrophy, abnormal gait.",
        "跛行、関節腫脹、硬直、可動域制限、軋音、運動・跳躍の忌避、筋萎縮、異常歩様。",
    ),
    "congenital": (
        "Signs present from birth or early life: failure to thrive, abnormal anatomy, "
        "developmental delay, organ dysfunction, seizures if CNS involved.",
        "出生時または幼少期からの徴候：発育不良、解剖学的異常、発達遅延、臓器機能障害、CNS関与時の痙攣。",
    ),
    "behavioral": (
        "Abnormal repetitive behaviors, self-mutilation, feather/fur plucking, "
        "aggression, excessive vocalization, pacing, reduced activity, "
        "appetite changes, avoidance behaviors.",
        "異常反復行動、自傷、羽毛・毛引き、攻撃性、過度の発声、常同歩行、活動量低下、食欲変化、回避行動。",
    ),
    "hematological": (
        "Pale mucous membranes, weakness, lethargy, tachycardia, tachypnea, "
        "petechiae/ecchymoses, prolonged bleeding, splenomegaly, icterus.",
        "粘膜蒼白、衰弱、無気力、頻脈、頻呼吸、点状出血・斑状出血、出血延長、脾腫、黄疸。",
    ),
}

_DEFAULT_CLINICAL_SIGNS = (
    "Clinical signs vary depending on the specific disease process and organs involved. "
    "Common signs include changes in appetite, activity level, and appearance. "
    "Specific examination findings guide further diagnostic workup.",
    "臨床徴候は疾患過程と罹患臓器により異なる。食欲、活動量、外見の変化が"
    "一般的な徴候である。特異的な検査所見に基づき追加検査を進める。",
)


def enrich_main_json():
    """Add recommended_tests to diseases_all_species.json."""
    with open(MAIN_JSON, encoding="utf-8") as f:
        data = json.load(f)

    added = 0
    cats: Counter = Counter()
    for d in data:
        if d.get("recommended_tests"):
            continue
        name = d.get("name", "")
        desc = d.get("description", "")
        cat = classify_disease(name, desc)
        cats[cat] += 1
        d["recommended_tests"] = _CATEGORY_TESTS.get(cat, _DEFAULT_TESTS)
        added += 1

    with open(MAIN_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"[Main JSON] Added recommended_tests to {added}/{len(data)} entries")
    for c, n in cats.most_common():
        print(f"  {c:<20}: {n}")


def enrich_supplementary_json():
    """Add transmission/clinical_signs/diagnosis to supplementary_diseases.json."""
    with open(SUPP_JSON, encoding="utf-8") as f:
        data = json.load(f)

    trans_added = 0
    cs_added = 0
    diag_added = 0

    for d in data:
        name = d.get("name", "")
        name_ja = d.get("name_ja", name)
        species = d.get("species", "")
        desc = d.get("description", "")
        cat = classify_disease(name, desc)
        name_l = name.lower()
        species_l = species.lower()

        # Transmission
        if not d.get("transmission"):
            tmpl = _TRANSMISSION_TEMPLATES.get(cat, _DEFAULT_TRANSMISSION)
            d["transmission"] = tmpl[0]
            d["transmission_ja"] = tmpl[1]
            trans_added += 1

        # Clinical signs
        if not d.get("clinical_signs"):
            tmpl = _CLINICAL_SIGNS_TEMPLATES.get(cat, _DEFAULT_CLINICAL_SIGNS)
            d["clinical_signs"] = tmpl[0]
            d["clinical_signs_ja"] = tmpl[1]
            cs_added += 1

        # Diagnosis
        if not d.get("diagnosis"):
            tests = d.get("recommended_tests", [])
            if tests:
                test_str = ", ".join(str(t) for t in tests[:5])
                d["diagnosis"] = (
                    f"Diagnosis of {name_l} is based on clinical signs, thorough history, "
                    f"and physical examination. Recommended diagnostics include: {test_str}. "
                    f"Differential diagnosis should consider other conditions presenting "
                    f"with similar clinical signs in {species_l}."
                )
                d["diagnosis_ja"] = (
                    f"{name_ja}の診断は臨床徴候、詳細な病歴、身体検査に基づく。"
                    f"推奨される検査: {test_str}。"
                    f"{species}における類似の臨床徴候を呈する他疾患との鑑別が必要である。"
                )
            else:
                d["diagnosis"] = (
                    f"Diagnosis of {name_l} is based on clinical presentation, "
                    f"thorough history, physical examination, and appropriate diagnostic workup."
                )
                d["diagnosis_ja"] = f"{name_ja}の診断は臨床像、詳細な病歴、身体検査、および適切な検査に基づく。"
            diag_added += 1

    with open(SUPP_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"[Supplementary JSON] Total: {len(data)}")
    print(f"  transmission added: {trans_added}")
    print(f"  clinical_signs added: {cs_added}")
    print(f"  diagnosis added: {diag_added}")


def main():
    print("=" * 60)
    print("Enriching remaining gaps in disease databases")
    print("=" * 60)
    print()
    enrich_main_json()
    print()
    enrich_supplementary_json()
    print()
    print("Done!")


if __name__ == "__main__":
    main()
