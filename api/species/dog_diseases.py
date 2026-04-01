"""Dog disease dictionary and analysis module.

Extracted from symptom_checker.py. Contains 579 diseases, 63 symptom names,
and 14 diagnostic tests for canine differential diagnosis.
"""

from __future__ import annotations

from typing import Any, Dict, List

from . import prevalence_data
from .helpers import ADVICE, analyze_symptoms_generic, enrich_diseases

_ANY_LIMPING = {"limping_fl", "limping_fr", "limping_rl", "limping_rr"}

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
    "circling", "scratching", "seizures",
    # Urinary / Reproductive
    "straining_urinate", "blood_urine", "incontinence",
    "genital_discharge",
    # Additional
    "swelling", "collapse", "ear_discharge", "head_shaking",
    "skin_lesions",
}

SYMPTOM_NAMES: dict[str, dict[str, str]] = {
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
    "scratching": {"ja": "掻く動作", "en": "Scratching"},
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

_PREVALENCE_MULTIPLIER: dict[str, float] = {
    "very_common": 1.4,
    "common": 1.2,
    "uncommon": 0.9,
    "rare": 0.7,
}

_DISEASE_PREVALENCE: dict[str, str] = {
    # ===== VERY COMMON (日常的に遭遇する疾患) =====
    # -- 消化器 --
    "Gastroenteritis":                           "very_common",
    "Intestinal Parasites":                      "very_common",
    "Hemorrhagic Gastroenteritis (HGE)":         "very_common",
    "Pancreatitis":                              "very_common",
    "Foreign Body Obstruction":                  "very_common",
    "Gastric Foreign Body":                      "very_common",
    "Colitis":                                   "very_common",
    # -- 皮膚 --
    "Allergic Dermatitis":                       "very_common",
    "Flea Allergy Dermatitis":                   "very_common",
    "Pyoderma":                                  "very_common",
    "Ear Infection (Otitis)":                    "very_common",
    # -- 整形外科 --
    "Patellar Luxation":                         "very_common",
    "Cranial Cruciate Ligament Rupture":         "very_common",
    "Hip Dysplasia":                             "very_common",
    # -- 感染症 --
    "Canine Parvovirus":                         "very_common",
    "Kennel Cough (Bordetella)":                 "very_common",
    # -- その他 --
    "Periodontal Disease":                       "very_common",
    "Urinary Tract Infection":                   "very_common",
    "Anal Sac Disease":                          "very_common",

    # ===== COMMON (頻繁に遭遇する疾患) =====
    # -- 内科 --
    "Hypothyroidism":                            "common",
    "Cushing's Disease":                         "common",
    "Diabetes Mellitus":                         "common",
    "Addison's Disease":                         "common",
    "Kidney Disease (CKD)":                      "common",
    "Liver Disease":                             "common",
    "Chronic Hepatitis":                         "common",
    "Heart Disease/CHF":                         "common",
    "Mitral Valve Disease (MMVD)":               "common",
    "Dilated Cardiomyopathy (DCM)":              "common",
    "Immune-Mediated Hemolytic Anemia":          "common",
    "Epilepsy":                                  "common",
    # -- 腫瘍 --
    "Mast Cell Tumor":                           "common",
    "Lymphoma":                                  "common",
    "Hemangiosarcoma":                           "common",
    "Mammary Tumor":                             "common",
    "Lipoma":                                    "common",
    "Osteosarcoma":                              "common",
    "Oral Melanoma":                             "common",
    "Melanoma":                                  "common",
    # -- 感染症 --
    "Canine Distemper":                           "common",
    "Leptospirosis":                             "common",
    "Giardiasis":                                "common",
    "Babesiosis":                                "common",
    # -- 整形外科 --
    "Intervertebral Disc Disease (IVDD)":        "common",
    "Elbow Dysplasia":                           "common",
    "Osteochondritis Dissecans (OCD)":           "common",
    # -- 眼科 --
    "Keratoconjunctivitis Sicca (Dry Eye)":      "common",
    "Corneal Ulcer":                             "common",
    "Cherry Eye":                                "common",
    "Cataracts":                                 "common",
    # -- 皮膚 --
    "Sarcoptic Mange (Scabies)":                 "common",
    "Fungal Infection (Ringworm)":               "common",
    "Seborrhea":                                 "common",
    # -- 泌尿器 --
    "Bladder Stones":                            "common",
    "Pyometra":                                  "common",

    # ===== UNCOMMON (時折遭遇する疾患) =====
    "Megaesophagus":                             "uncommon",
    "Myasthenia Gravis":                         "uncommon",
    "Pemphigus":                                 "uncommon",
    "Systemic Lupus Erythematosus (SLE)":        "uncommon",
    "Portosystemic Shunt (Liver Shunt)":         "uncommon",
    "Copper Storage Disease":                    "uncommon",
    "Wobbler Syndrome":                          "uncommon",
    "Pericardial Effusion":                      "uncommon",
    "Chylothorax":                               "uncommon",
    "Exocrine Pancreatic Insufficiency (EPI)":   "uncommon",
    "Histiocytic Sarcoma":                       "uncommon",
    "Transitional Cell Carcinoma":               "uncommon",
    "Insulinoma":                                "uncommon",
    "Pheochromocytoma":                          "uncommon",

    # ===== RARE (稀に遭遇する疾患) =====
    "Hepatic Microvascular Dysplasia":           "rare",
    "Mucopolysaccharidosis":                     "rare",
    "Glycogen Storage Disease":                  "rare",
    "Malignant Hyperthermia":                    "rare",
    "Alopecia X":                                "rare",
    "Chemodectoma (Heart Base Tumor)":           "rare",
    "Plasmacytoma":                              "rare",
    "Hepatozoonosis":                            "rare",
    "Sick Sinus Syndrome":                       "rare",
    "Sebaceous Adenitis":                        "rare",
    "Infective Endocarditis":                    "rare",
    "Pulmonary Fibrosis":                        "rare",
    "Dermatomyositis":                           "rare",
    "Juvenile Cellulitis (Puppy Strangles)":     "rare",
}

DISEASES: List[Dict[str, Any]] = [
    {
        "name": "Canine Parvovirus",
        "name_ja": "犬パルボウイルス感染症",
        "symptoms": {"vomiting", "bloody_stool", "lethargy", "appetite_loss",
                      "fever", "diarrhea"},
        "description": "A highly contagious and potentially fatal viral illness "
                       "that attacks the gastrointestinal tract, most dangerous "
                       "in puppies.",
        "description_ja": "犬パルボウイルス2型（CPV-2）による高伝染性のウイルス疾患。腸管上皮の急速に分裂する細胞を標的とし、"
                          "重度の出血性腸炎を引き起こす。ワクチン未接種の子犬（6週〜6ヶ月齢）で最も致死率が高い。"
                          "ロットワイラー、ドーベルマン、ジャーマンシェパード等が好発品種。",
        "pathophysiology_ja": "経口感染後、ウイルスはまずリンパ組織で増殖し、ウイルス血症を経て腸管陰窩上皮細胞に到達する。"
                              "陰窩上皮の壊死により絨毛が崩壊し、吸収障害・出血性下痢・細菌の二次感染（敗血症）を引き起こす。"
                              "同時に骨髄の造血前駆細胞も攻撃され、白血球減少症（特にリンパ球減少）を伴う。",
        "causes_ja": "犬パルボウイルス2型（CPV-2a, 2b, 2c亜型）。糞口経路で感染し、環境中で数ヶ月〜1年以上生存可能。"
                     "ワクチン未接種、母体移行抗体の低下期、免疫抑制状態がリスク因子。",
        "treatment_ja": "特異的抗ウイルス薬はなく、支持療法が主体。(1)積極的な輸液療法（乳酸リンゲル液、晶質液＋膠質液）、"
                        "(2)制吐薬（マロピタント0.1mg/kg IV q24h）、(3)広域抗菌薬（アンピシリン＋エンロフロキサシン等）で二次感染予防、"
                        "(4)栄養サポート（早期経腸栄養が推奨）。重症例ではFFP輸血や抗エンドトキシン抗体も検討。",
        "prognosis_ja": "早期の積極的治療で生存率85〜95%。無治療では致死率91%以上。白血球数<1,000/μLや低アルブミン血症は予後不良因子。",
        "prevention_ja": "コアワクチン（MLV）を6〜8週齢から2〜4週間隔で16週齢以降まで接種。年1回の追加接種。"
                         "感染環境の次亜塩素酸ナトリウム消毒（1:30希釈）。",
        "urgency": "emergency",
    },
    {
        "name": "Canine Distemper",
        "name_ja": "犬ジステンパー",
        "symptoms": {"fever", "nasal_discharge", "eye_discharge", "coughing",
                      "lethargy", "seizures", "vomiting"},
        "description": "A serious viral disease affecting the respiratory, "
                       "gastrointestinal, and nervous systems.",
        "description_ja": "犬ジステンパーウイルス（CDV、パラミクソウイルス科モルビリウイルス属）による多臓器感染症。"
                          "呼吸器→消化器→神経系と段階的に進行し、特にワクチン未接種の若齢犬で致死率が高い。"
                          "二相性発熱（初期発熱→一時解熱→再発熱）が特徴的。",
        "pathophysiology_ja": "エアロゾル感染後、上気道リンパ組織で初期増殖→ウイルス血症→全身のリンパ組織、上皮組織、中枢神経系へ播種。"
                              "リンパ球融解によるリンパ球減少→免疫抑制→日和見感染の併発。晩期には脱髄性脳脊髄炎を引き起こし、"
                              "ミオクローヌス（チューインガム発作）や痙攣が出現。ハードパッド病（足底角化）も特徴的。",
        "causes_ja": "犬ジステンパーウイルス（CDV）。飛沫感染・直接接触で伝播。"
                     "ワクチン未接種犬、免疫不全犬、3〜6ヶ月齢の子犬が高リスク。フェレット等の野生動物も感受性あり。",
        "treatment_ja": "特異的治療薬なし。支持療法が主体：(1)広域抗菌薬で二次細菌感染の制御、(2)輸液・栄養管理、"
                        "(3)抗痙攣薬（ジアゼパム、フェノバルビタール）で神経症状の管理。"
                        "インターフェロン投与の報告もあるが、エビデンスは限定的。",
        "prognosis_ja": "神経症状出現前の呼吸器型では回復の可能性あり。神経型に進行した場合は予後不良で致死率50%以上。"
                        "回復しても永続的な神経後遺症（ミオクローヌス、エナメル質低形成）が残ることがある。",
        "prevention_ja": "コアワクチン（MLVジステンパーワクチン）を子犬期に3回接種後、年1回追加接種。"
                         "感染犬との接触回避。",
        "urgency": "high",
    },
    {
        "name": "Kennel Cough (Bordetella)",
        "name_ja": "ケンネルコフ（犬伝染性気管気管支炎）",
        "symptoms": {"coughing", "sneezing", "nasal_discharge",
                      "reverse_sneezing", "lethargy"},
        "description": "A highly contagious respiratory infection causing a "
                       "persistent, forceful cough.",
        "description_ja": "Bordetella bronchisepticaを主な原因菌とする犬の急性伝染性気管気管支炎。"
                          "犬アデノウイルス2型、犬パラインフルエンザウイルス等との混合感染が多い。"
                          "ペットホテルやドッグランなど多頭飼育環境で発生しやすい。",
        "pathophysiology_ja": "飛沫・エアロゾル感染により気道上皮に付着→線毛運動障害と粘膜炎症→"
                              "乾性〜湿性の発作的な咳（ガチョウ様咳嗽）。気管圧迫で誘発される特徴的な咳反射。"
                              "通常は上気道に限局するが、免疫不全犬では気管支肺炎に進展する場合がある。",
        "causes_ja": "Bordetella bronchiseptica（最主要）、犬パラインフルエンザウイルス、犬アデノウイルス2型、"
                     "犬呼吸器コロナウイルス、マイコプラズマ等の混合感染。多頭飼育、ストレス、換気不良がリスク因子。",
        "treatment_ja": "軽症例：自然回復（1〜3週間）、鎮咳薬（ブトルファノール）、環境整備（加湿・安静）。"
                        "重症例・二次感染：ドキシサイクリン(5mg/kg BID 10〜14日)またはアジスロマイシン。"
                        "ネブライザー療法も有効。気管支肺炎への進展時は入院管理。",
        "prognosis_ja": "免疫正常犬では1〜3週間で自然回復し予後良好。子犬や免疫不全犬では気管支肺炎への進展に注意。",
        "prevention_ja": "ワクチン（注射型または経鼻型）接種。多頭飼育環境の換気改善。感染犬の隔離。",
        "urgency": "normal",
    },
    {
        "name": "Gastric Dilatation-Volvulus (GDV/Bloat)",
        "name_ja": "胃拡張胃捻転症候群（GDV）",
        "symptoms": {"bloated_abdomen", "vomiting", "excessive_panting",
                      "lethargy", "anxiety", "collapse", "drooling"},
        "description": "A life-threatening condition where the stomach fills "
                       "with gas and rotates, cutting off blood supply. "
                       "Requires immediate emergency surgery.",
        "description_ja": "胃がガスで急速に拡張し、時計方向に180〜360°捻転する致死的緊急疾患。"
                          "大型〜超大型犬（グレートデン、セントバーナード、ジャーマンシェパード等）の深胸種に好発。"
                          "食後の運動、一日一回の大量給餌、ストレスがリスク因子。",
        "pathophysiology_ja": "胃の捻転により噴門・幽門が閉塞→胃内ガス蓄積→胃壁の虚血壊死。"
                              "脾臓を巻き込み脾捻転を併発。後大静脈の圧迫による静脈還流障害→心拍出量低下→"
                              "分布性ショック。再灌流障害によりDIC、心室性不整脈（再灌流性不整脈）を合併。",
        "causes_ja": "明確な単一原因は不明。リスク因子：大型深胸種、一日一食の大量給餌、食後直後の運動、"
                     "早食い、エアロファジア（空気嚥下）、加齢、GDVの家族歴、ストレス・不安気質。",
        "treatment_ja": "【超緊急】(1)ショック治療：大量輸液（晶質液60-90mL/kg/hr）、(2)胃減圧（経口胃管または経皮的穿刺脱気）、"
                        "(3)安定化後に緊急開腹手術→胃の整復＋胃固定術（gastropexy）、壊死組織の切除、脾摘（必要時）。"
                        "(4)術後：心電図モニター（再灌流性心室性不整脈にリドカイン）、電解質補正。",
        "prognosis_ja": "早期手術で生存率85〜90%。胃壁壊死やDIC合併例では致死率30〜50%。"
                        "胃固定術を行えば再発率3〜5%（未実施では80%再発）。",
        "prevention_ja": "予防的胃固定術（高リスク犬種で推奨、避妊去勢手術時に同時実施可）。"
                         "一日2〜3回の分割給餌。食後1時間の安静。ストレス軽減。",
        "urgency": "emergency",
    },
    {
        "name": "Pancreatitis",
        "name_ja": "膵炎",
        "symptoms": {"vomiting", "appetite_loss", "lethargy", "pain_on_touch",
                      "diarrhea", "fever"},
        "description": "Inflammation of the pancreas causing severe abdominal "
                       "pain and digestive disturbance.",
        "description_ja": "膵臓の自己消化による急性または慢性の炎症性疾患。犬では急性壊死性膵炎が多く、"
                          "中年〜高齢の肥満犬、ミニチュアシュナウザー、コッカースパニエルに好発。"
                          "高脂肪食の摂取後や副腎皮質機能亢進症の併発例で発症リスクが上昇する。",
        "pathophysiology_ja": "膵腺房細胞内でトリプシノーゲンが異常活性化→膵実質の自己消化→局所炎症→"
                              "全身性炎症反応症候群（SIRS）。重症例ではDIC、多臓器不全（MOF）に進展。"
                              "慢性例では膵線維化→外分泌機能不全（EPI）や糖尿病の原因となる。",
        "causes_ja": "高脂肪食・ゴミ漁り（最多）、副腎皮質機能亢進症、甲状腺機能低下症、高脂血症、"
                     "薬物（アザチオプリン、L-アスパラギナーゼ、臭化カリウム等）、膵管閉塞、外傷。"
                     "多くは特発性。",
        "treatment_ja": "(1)絶食→早期経腸栄養（24〜48時間以内に少量から開始が推奨）、"
                        "(2)積極的輸液療法、(3)鎮痛：マロピタント（制吐＋内臓痛緩和）、ブプレノルフィン、"
                        "フェンタニルCRI、(4)制吐薬：マロピタント＋オンダンセトロン（難治例）、"
                        "(5)抗菌薬は感染合併時のみ。慢性例では低脂肪食＋膵酵素補充。",
        "prognosis_ja": "軽症〜中等症：適切な治療で回復良好（生存率90%以上）。"
                        "重症壊死性膵炎：致死率30〜40%。DIC・MOF合併は予後不良因子。再発率は高い。",
        "prevention_ja": "低脂肪食の維持、テーブルフードの禁止、肥満防止、原疾患（高脂血症等）の管理。",
        "urgency": "high",
    },
    {
        "name": "Hypothyroidism",
        "name_ja": "甲状腺機能低下症",
        "symptoms": {"weight_gain", "lethargy", "hair_loss", "dry_skin",
                      "stiffness"},
        "description": "An endocrine disorder where the thyroid gland produces "
                       "insufficient hormones, slowing metabolism.",
        "description_ja": "犬で最も一般的な内分泌疾患の一つ。甲状腺ホルモン（T4）の産生低下により全身の代謝率が低下する。"
                          "中年〜高齢犬（4〜10歳）に好発。ゴールデンレトリバー、ドーベルマン、"
                          "アイリッシュセッター、グレートデン等の中〜大型犬に多い。",
        "pathophysiology_ja": "95%以上がリンパ球性甲状腺炎（自己免疫性）または特発性甲状腺萎縮により甲状腺が破壊される原発性。"
                              "T4低下→TSH上昇（負のフィードバック）。代謝率低下により体重増加、皮膚代謝異常（脱毛・角化異常）、"
                              "神経伝導速度低下（末梢神経障害）、心拍出量低下を引き起こす。",
        "causes_ja": "リンパ球性甲状腺炎（自己免疫性、最多）、特発性甲状腺萎縮、"
                     "稀に甲状腺腫瘍、医原性（放射性ヨード治療後、抗甲状腺薬）。遺伝的素因あり。",
        "treatment_ja": "レボチロキシン（L-T4）0.02mg/kg BID経口投与（生涯投与）。"
                        "投与開始4〜8週後にT4値を再検査し用量調整。活動性改善は1〜2週間、"
                        "皮膚・被毛改善は4〜6ヶ月かかる。定期的な甲状腺機能モニタリング（6ヶ月〜1年毎）。",
        "prognosis_ja": "適切な補充療法で予後は極めて良好。生活の質は正常に近い状態まで回復する。治療は生涯必要。",
        "prevention_ja": "確立された予防法はないが、好発品種では中年期以降の定期的な甲状腺機能検査を推奨。",
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
        "name_ja": "クッシング症候群（副腎皮質機能亢進症）",
        "symptoms": {"excessive_thirst", "excessive_urination", "weight_gain",
                      "hair_loss", "lethargy", "excessive_panting", "appetite_increase"},
        "description": "Overproduction of cortisol by the adrenal glands, "
                       "leading to a range of systemic effects.",
        "description_ja": "コルチゾールの慢性的過剰産生による多臓器障害。中高齢犬（8歳以上）に好発。"
                          "下垂体依存性（PDH、85%）と副腎腫瘍性（AT、15%）に分類。"
                          "プードル、ダックスフント、ビーグル、ボストンテリアに多い。",
        "pathophysiology_ja": "PDH：下垂体腺腫→ACTH過剰分泌→両側副腎皮質過形成→コルチゾール過剰。"
                              "AT：副腎皮質腫瘍（腺腫or腺癌）から自律的にコルチゾール分泌。"
                              "慢性的高コルチゾール血症→肝臓のグリコーゲン蓄積（ステロイド肝症）、筋萎縮、"
                              "皮膚菲薄化、免疫抑制、インスリン抵抗性（二次性糖尿病リスク）。",
        "causes_ja": "下垂体微小腺腫（PDH、最多）、副腎皮質腫瘍（腺腫・腺癌）、"
                     "医原性（長期ステロイド投与）。",
        "treatment_ja": "PDH：トリロスタン（2〜5mg/kg SID〜BID、第一選択）でコルチゾール合成阻害。"
                        "ACTH刺激試験で用量調整。代替薬：ミトタン（o,p'-DDD）。"
                        "AT：外科的副腎摘出（可能であれば根治的）。転移例にはミトタン。"
                        "医原性：ステロイドの漸減中止。全例で定期的なACTH刺激試験モニタリング必須。",
        "prognosis_ja": "PDH：トリロスタン治療で中央生存期間約2年。QOLは大きく改善。"
                        "AT腺腫：外科切除で予後良好。AT腺癌：転移例は予後不良。"
                        "無治療では糖尿病、肺血栓塞栓症、尿路感染症の合併リスクが高い。",
        "prevention_ja": "確立された予防法なし。好発品種では多飲多尿・腹部膨満等の初期症状に注意し早期診断を推奨。",
        "urgency": "normal",
    },
    {
        "name": "Addison's Disease",
        "name_ja": "アジソン病（副腎皮質機能低下症）",
        "symptoms": {"lethargy", "appetite_loss", "vomiting", "diarrhea",
                      "weight_loss", "dehydration", "collapse"},
        "description": "Insufficient production of adrenal hormones, causing "
                       "weakness, dehydration, and episodic collapse.",
        "description_ja": "副腎皮質からのグルココルチコイドおよびミネラルコルチコイドの分泌不全。"
                          "「偉大なる模倣者（Great Pretender）」と呼ばれ、非特異的症状のため見逃されやすい。"
                          "若齢〜中年の雌犬に好発。スタンダードプードル、ポルトガルウォータードッグ等に遺伝的素因。",
        "pathophysiology_ja": "免疫介在性副腎皮質破壊（最多）→コルチゾール・アルドステロン欠乏。"
                              "アルドステロン欠乏→Na喪失・K貯留→高K血症による徐脈・不整脈（致死的）。"
                              "コルチゾール欠乏→ストレス耐性低下、低血糖、消化器症状。"
                              "アジソンクリーゼ：急性副腎不全による循環虚脱・低血圧性ショック。",
        "causes_ja": "免疫介在性副腎皮質炎（原発性、最多）、医原性（長期ステロイド投与の急な中止）、"
                     "肉芽腫性疾患（真菌症等）、副腎出血、転移性腫瘍。稀に下垂体性（二次性）。",
        "treatment_ja": "【急性クリーゼ】大量生理食塩水輸液、デキサメタゾン0.5〜2mg/kg IV、高K血症の補正。"
                        "【維持療法】フルドロコルチゾン（0.01〜0.02mg/kg/日）またはDOCP（2.2mg/kg SC q25日）"
                        "＋プレドニゾロン（0.1〜0.2mg/kg/日）。電解質の定期モニタリング。"
                        "ストレス時（手術・旅行等）はステロイド増量。",
        "prognosis_ja": "適切な補充療法で予後は良好〜極めて良好。正常な生活が可能。治療は生涯必要。"
                        "アジソンクリーゼは早期治療で回復可能だが、診断遅延は致死的。",
        "prevention_ja": "確立された予防法なし。好発品種では消化器症状の間欠的な発現に注意。"
                         "ステロイド長期投与からの離脱は必ず漸減で行う。",
        "urgency": "high",
    },
    {
        "name": "Diabetes Mellitus",
        "name_ja": "糖尿病",
        "symptoms": {"excessive_thirst", "excessive_urination", "weight_loss",
                      "appetite_increase", "lethargy"},
        "description": "A metabolic disorder where the body cannot properly "
                       "regulate blood sugar levels.",
        "description_ja": "インスリン分泌不全または作用不全による持続性高血糖。犬では1型（インスリン依存性）が多い。"
                          "中高齢の未避妊雌犬に好発。サモエド、オーストラリアンテリア、ミニチュアシュナウザー等に多い。",
        "pathophysiology_ja": "膵β細胞の免疫介在性破壊→絶対的インスリン欠乏→高血糖。"
                              "腎糖排泄閾値（約180mg/dL）超過→浸透圧利尿（多尿）→代償性多飲。"
                              "脂肪分解亢進→ケトン体産生→糖尿病性ケトアシドーシス（DKA、致死的合併症）。"
                              "長期的に白内障（犬で非常に多い）、糖尿病性神経障害を合併。",
        "causes_ja": "免疫介在性膵β細胞破壊（犬の1型DM、最多）、慢性膵炎による二次性、"
                     "発情後の黄体期プロゲステロン→GH過剰（未避妊雌犬）、"
                     "副腎皮質機能亢進症、長期ステロイド投与。肥満はリスク因子。",
        "treatment_ja": "インスリン療法（生涯）：中間型インスリン（NPH、Vetsulin/Caninsulin）0.25〜0.5IU/kg BID SC。"
                        "血糖曲線で用量調整。食事管理：高繊維・低脂肪食、一定時間・一定量の給餌。"
                        "未避妊雌犬は避妊手術（プロゲステロンによるインスリン抵抗性解除）。"
                        "DKA：入院管理、レギュラーインスリンCRI、輸液、電解質補正。",
        "prognosis_ja": "適切なインスリン管理と食事管理で中央生存期間2〜3年以上。多くの犬で良好なQOLを維持。"
                        "白内障は高頻度（75%以上）に発生するが、白内障手術で視力回復可能。DKAは致死率20〜40%。",
        "prevention_ja": "肥満予防、未避妊雌犬の早期避妊手術（プロゲステロン性DM予防）。"
                         "好発品種では血糖・フルクトサミン値の定期検査。",
        "urgency": "normal",
    },
    {
        "name": "Urinary Tract Infection",
        "name_ja": "尿路感染症（UTI）",
        "symptoms": {"straining_urinate", "blood_urine",
                      "excessive_urination", "fever", "lethargy"},
        "description": "A bacterial infection of the urinary tract causing "
                       "pain, frequent urination, and sometimes blood in urine.",
        "description_ja": "下部尿路（膀胱）の細菌感染が最も多い。雌犬に好発（解剖学的に尿道が短い）。"
                          "単純性UTIと、基礎疾患（糖尿病、クッシング、尿石症等）に伴う複雑性UTIに分類。",
        "pathophysiology_ja": "上行性感染（会陰部の常在菌→尿道→膀胱）が主経路。"
                              "E. coli（最多、約50%）、Staphylococcus、Proteus等が原因菌。"
                              "膀胱粘膜の炎症→頻尿・血尿・排尿痛。上部尿路への波及で腎盂腎炎を合併する場合がある。",
        "causes_ja": "大腸菌（最多）、ブドウ球菌、プロテウス、クレブシエラ等の上行性感染。"
                     "リスク因子：雌犬、免疫抑制（糖尿病、クッシング、ステロイド投与）、尿石症、解剖学的異常。",
        "treatment_ja": "尿培養＋感受性試験に基づく抗菌薬選択が理想。経験的治療：アモキシシリン/クラブラン酸"
                        "（12.5〜25mg/kg BID）7〜14日間。複雑性UTIは4〜6週間投与。"
                        "治療終了1週間後に尿培養で陰性確認。基礎疾患の同時管理が重要。",
        "prognosis_ja": "単純性UTI：適切な抗菌薬治療で完治率95%以上。"
                        "複雑性UTI：基礎疾患の管理が不十分だと再発を繰り返す。",
        "prevention_ja": "十分な飲水量の確保、定期的な排尿機会、基礎疾患の管理。"
                         "再発性UTIではクランベリーサプリメントの有効性を示す報告もある。",
        "urgency": "normal",
    },
    {
        "name": "Bladder Stones",
        "name_ja": "膀胱結石",
        "symptoms": {"straining_urinate", "blood_urine",
                      "excessive_urination", "pain_on_touch"},
        "description": "Mineral formations in the bladder causing urinary "
                       "obstruction and discomfort.",
        "description_ja": "膀胱内のミネラル結石により、排尿障害や不快感を引き起こします。"
                          "結石の種類にはストラバイト、シュウ酸カルシウム、シスチン、尿酸等があり、"
                          "種類により治療法が異なります。",
        "pathophysiology_ja": "尿中のミネラル（リン酸マグネシウムアンモニウム、シュウ酸カルシウム等）が"
                              "過飽和状態となり結晶化→結石形成。尿pH、食事内容、飲水量、"
                              "尿路感染の有無が結石形成に影響。結石による膀胱粘膜刺激→血尿・頻尿。",
        "causes_ja": "食事（高ミネラル食）、飲水量不足、尿路感染（ストラバイト形成促進）、"
                     "遺伝的素因（シスチン尿症等）、代謝異常。犬種素因あり。",
        "treatment_ja": "結石分析が治療方針決定に必須。"
                        "ストラバイト：溶解食（Hill's s/d等）＋尿路感染治療で内科的溶解可能。"
                        "シュウ酸カルシウム：内科的溶解不可→外科的摘出（膀胱切開術）。"
                        "再発予防：療法食＋十分な飲水＋定期的尿検査・画像検査。",
        "prognosis_ja": "適切な治療で予後良好。再発率が高い（特にシュウ酸カルシウム）ため、"
                        "生涯にわたる食事管理と定期モニタリングが必要。",
        "prevention_ja": "療法食、十分な飲水量確保、定期的な尿検査。"
                         "ストラバイト：尿路感染の早期治療。",
        "urgency": "normal",
    },
    {
        "name": "Struvite Urolithiasis",
        "name_ja": "ストラバイト尿石症（リン酸マグネシウムアンモニウム結石）",
        "symptoms": {"straining_urinate", "blood_urine",
                      "excessive_urination", "pain_on_touch"},
        "description": "Struvite (magnesium ammonium phosphate) stone formation "
                       "in the urinary tract, often associated with UTI.",
        "description_ja": "リン酸マグネシウムアンモニウム（ストラバイト）結石。"
                          "犬では尿路感染（特にウレアーゼ産生菌）に続発することが多い。"
                          "雌犬に多い。ミニチュアシュナウザー、シーズー、ビション・フリーゼに好発。",
        "pathophysiology_ja": "ウレアーゼ産生菌（Staphylococcus, Proteus等）の感染→"
                              "尿素をアンモニア＋CO₂に分解→尿pH上昇（アルカリ化）→"
                              "マグネシウム・アンモニウム・リン酸が過飽和→ストラバイト結晶化→結石形成。"
                              "犬では感染誘発型が主（猫とは異なる）。",
        "causes_ja": "尿路感染（ウレアーゼ産生菌）が最大の原因。"
                     "アルカリ尿、高ミネラル食、飲水量不足も寄与。",
        "treatment_ja": "内科的溶解が可能（犬のストラバイト結石の大きな利点）。"
                        "(1)適切な抗菌薬で尿路感染を治療（培養感受性試験に基づく）、"
                        "(2)溶解食（Hill's s/d, Royal Canin S/O等）→2〜4週間で溶解開始、"
                        "(3)溶解確認まで月1回のX線/超音波モニタリング、"
                        "(4)結石消失後も2〜4週間の溶解食継続を推奨。"
                        "大結石・尿道閉塞時は外科的摘出（膀胱切開術）。",
        "prognosis_ja": "溶解食＋感染治療で良好。再発予防の鍵は尿路感染の管理。"
                        "適切な管理で再発率を低く抑えられる。",
        "prevention_ja": "尿路感染の早期発見・治療。療法食（維持食）。"
                         "十分な飲水量。定期的な尿培養検査。",
        "urgency": "normal",
    },
    {
        "name": "Calcium Oxalate Urolithiasis",
        "name_ja": "シュウ酸カルシウム尿石症",
        "symptoms": {"straining_urinate", "blood_urine",
                      "excessive_urination", "pain_on_touch"},
        "description": "Calcium oxalate stone formation in the urinary tract, "
                       "the most common stone type in certain breeds.",
        "description_ja": "シュウ酸カルシウム結石は内科的溶解が不可能で、外科的摘出が必要。"
                          "ミニチュアシュナウザー、ヨークシャーテリア、シーズー、"
                          "ビション・フリーゼ、ポメラニアンに好発。中高齢の雄犬に多い。",
        "pathophysiology_ja": "高カルシウム尿症・高シュウ酸尿症→尿中でシュウ酸カルシウムが過飽和→"
                              "結晶核形成→結石成長。酸性尿でより形成されやすい。"
                              "副甲状腺機能亢進症、高カルシウム血症も原因となりうる。",
        "causes_ja": "高カルシウム食・高シュウ酸食（ほうれん草等）、代謝性アシドーシス、"
                     "副甲状腺機能亢進症、特発性高カルシウム尿症、遺伝的素因。"
                     "尿酸性化食の過剰使用も原因。",
        "treatment_ja": "内科的溶解不可→外科的摘出が標準治療。"
                        "(1)膀胱切開術で結石摘出、(2)術後結石分析で確定診断、"
                        "(3)再発予防食（Hill's u/d, Royal Canin U/C等）、"
                        "(4)クエン酸カリウム（75mg/kg BID）で尿アルカリ化、"
                        "(5)ヒドロクロロチアジド（2〜4mg/kg BID）で尿中Ca排泄低減、"
                        "(6)3〜6ヶ月毎のX線/超音波モニタリング。",
        "prognosis_ja": "外科的摘出後の短期予後は良好。再発率が高い（3年以内に30〜50%）。"
                        "生涯にわたる食事管理とモニタリングが必要。",
        "prevention_ja": "療法食（中程度タンパク、低シュウ酸、低ナトリウム）。"
                         "十分な飲水量。尿アルカリ化。定期的な画像検査。",
        "urgency": "normal",
    },
    {
        "name": "Urate Urolithiasis",
        "name_ja": "尿酸アンモニウム尿石症",
        "symptoms": {"straining_urinate", "blood_urine",
                      "excessive_urination", "pain_on_touch"},
        "description": "Ammonium urate stone formation, common in Dalmatians "
                       "and dogs with portosystemic shunts.",
        "description_ja": "尿酸アンモニウム結石。ダルメシアン（尿酸代謝の遺伝的特異性）と"
                          "門脈体循環シャントを有する犬に好発。"
                          "ダルメシアンでは品種の100%が高尿酸尿症を示す。",
        "pathophysiology_ja": "ダルメシアン：SLC2A9遺伝子変異→肝臓での尿酸→アラントインへの変換障害"
                              "＋腎尿細管での尿酸再吸収障害→高尿酸尿症→尿酸結石形成。"
                              "門脈シャント犬：肝臓での尿酸代謝低下＋高アンモニア血症→"
                              "尿酸アンモニウム結石形成。",
        "causes_ja": "ダルメシアン（SLC2A9変異、品種特異的）、門脈体循環シャント、"
                     "高プリン食（内臓肉等）。イングリッシュブルドッグ、"
                     "ロシアンブラックテリアでも報告あり。",
        "treatment_ja": "内科的溶解が可能な場合あり。"
                        "(1)低プリン食（Hill's u/d等）、(2)アロプリノール（10〜15mg/kg BID）"
                        "→キサンチンオキシダーゼ阻害で尿酸産生抑制、"
                        "(3)尿アルカリ化（クエン酸カリウム）、(4)十分な飲水。"
                        "門脈シャント犬：シャント結紮術が根本治療。"
                        "大結石は外科的摘出。",
        "prognosis_ja": "アロプリノール＋低プリン食で良好に管理可能。"
                        "門脈シャントの外科的修正後は結石形成リスク低下。"
                        "ダルメシアンでは生涯管理が必要。",
        "prevention_ja": "低プリン食、十分な飲水、アロプリノール予防投与（ダルメシアン）。"
                         "門脈シャント犬はシャント結紮後も定期モニタリング。",
        "urgency": "normal",
    },
    {
        "name": "Kidney Disease (CKD)",
        "name_ja": "慢性腎臓病（CKD）",
        "symptoms": {"excessive_thirst", "excessive_urination", "appetite_loss",
                      "vomiting", "weight_loss", "lethargy"},
        "description": "Progressive loss of kidney function leading to waste "
                       "build-up and systemic illness.",
        "description_ja": "不可逆的なネフロン喪失による進行性の腎機能低下。IRIS分類でStage 1〜4に病期分類。"
                          "高齢犬に多いが、先天性腎疾患（腎異形成等）で若齢犬にも発生する。"
                          "症状が顕在化するのは腎機能の75%以上が失われた時点（Stage 3以降）。",
        "pathophysiology_ja": "原因を問わず、ネフロンの進行性喪失→残存ネフロンの代償性過濾過→"
                              "糸球体硬化→さらなるネフロン喪失の悪循環。BUN・クレアチニン上昇、"
                              "リン貯留→二次性上皮小体機能亢進症→腎性骨異栄養症。"
                              "尿濃縮能低下→多尿→代償性多飲。末期には尿毒症性消化器症状・貧血。",
        "causes_ja": "加齢性変化（最多）、慢性糸球体腎炎、腎アミロイドーシス、先天性腎異形成、"
                     "慢性腎盂腎炎、腎結石、NSAID等の腎毒性薬物、レプトスピラ症後遺症。"
                     "コッカースパニエル、シーズー、ブルテリアに遺伝的素因。",
        "treatment_ja": "根治療法なし。進行抑制と症状管理が目標。"
                        "(1)腎臓療法食（低リン・低タンパク・高品質タンパク）—Stage 2以降で推奨、"
                        "(2)リン吸着剤（水酸化アルミニウム、炭酸ランタン）、"
                        "(3)ACE阻害薬（ベナゼプリル0.25〜0.5mg/kg SID）—タンパク尿軽減、"
                        "(4)制吐薬・胃粘膜保護薬、(5)皮下輸液（在宅）、"
                        "(6)エリスロポエチン（腎性貧血に対して）。SDMA値で早期診断可能。",
        "prognosis_ja": "IRIS Stage 2：中央生存期間1,000日以上。Stage 3：約300〜500日。"
                        "Stage 4：約100〜200日。腎臓療法食による生存期間延長のエビデンスあり。"
                        "タンパク尿の程度が最も重要な予後因子。",
        "prevention_ja": "7歳以降の定期的な血液検査（BUN、Cre、SDMA）＋尿検査（UPC比）。"
                         "腎毒性薬物の回避。十分な飲水量の確保。",
        "urgency": "normal",
    },
    {
        "name": "Liver Disease",
        "name_ja": "肝臓病（肝障害）",
        "symptoms": {"appetite_loss", "vomiting", "lethargy", "weight_loss",
                      "excessive_thirst", "bloated_abdomen"},
        "description": "Impaired liver function affecting digestion, "
                       "detoxification, and metabolism.",
        "description_ja": "急性または慢性の肝細胞障害による消化・解毒・合成機能の低下。"
                          "慢性肝炎はコッカースパニエル、ドーベルマン、ラブラドール、ベドリントンテリアに好発。"
                          "黄疸、腹水、肝性脳症が進行した肝不全の三大徴候。",
        "pathophysiology_ja": "肝細胞障害→ALT・AST上昇。胆汁うっ滞→ALP・GGT上昇・高ビリルビン血症（黄疸）。"
                              "合成機能低下→低アルブミン血症→腹水・浮腫。凝固因子合成低下→出血傾向。"
                              "アンモニア代謝障害→高アンモニア血症→肝性脳症（神経症状）。"
                              "慢性肝炎→線維化→肝硬変への進行。",
        "causes_ja": "慢性肝炎（免疫介在性、銅蓄積性、特発性）、急性肝障害（薬物性、中毒性）、"
                     "門脈体循環シャント（先天性/後天性）、肝腫瘍、胆管疾患、感染症（レプトスピラ等）。"
                     "ベドリントンテリアの銅蓄積症は常染色体劣性遺伝。",
        "treatment_ja": "原因に応じた治療。慢性肝炎：免疫抑制療法（プレドニゾロン±アザチオプリン）、"
                        "ウルソデオキシコール酸（15mg/kg/日、肝保護・利胆）、SAMe（肝細胞保護）、"
                        "銅蓄積症にはD-ペニシラミン＋低銅食。"
                        "肝性脳症：低タンパク食、ラクツロース（高アンモニア血症軽減）、メトロニダゾール。"
                        "腹水：フロセミド＋スピロノラクトン、ナトリウム制限。",
        "prognosis_ja": "慢性肝炎：早期治療で数年の生存が可能。肝硬変に進行した場合は予後不良。"
                        "急性肝障害：原因除去と支持療法で回復可能な場合がある。"
                        "銅蓄積症：キレート療法で進行抑制可能。",
        "prevention_ja": "肝毒性薬物の注意深い使用、中毒物質への暴露回避、好発品種での定期的肝機能検査。",
        "urgency": "normal",
    },
    {
        "name": "Heart Disease/CHF",
        "name_ja": "うっ血性心不全（CHF）",
        "symptoms": {"coughing", "difficulty_breathing", "lethargy",
                      "excessive_panting", "bloated_abdomen"},
        "description": "Deterioration of heart function leading to fluid "
                       "build-up and reduced exercise tolerance.",
        "description_ja": "心臓のポンプ機能不全により全身のうっ血と体液貯留を来す症候群。"
                          "犬では僧帽弁粘液腫様変性（MMVD、小型犬）と拡張型心筋症（DCM、大型犬）が二大原因。"
                          "ACVIM分類でStage A〜Dに病期分類。",
        "pathophysiology_ja": "左心不全：僧帽弁逆流→左房圧上昇→肺静脈うっ血→肺水腫（咳、呼吸困難）。"
                              "右心不全：三尖弁逆流or肺高血圧→全身静脈うっ血→腹水、頸静脈怒張。"
                              "神経体液性代償機構（RAAS活性化、交感神経亢進）→Na・水貯留→さらなる前負荷増大の悪循環。"
                              "心房拡大→心房細動リスク上昇。",
        "causes_ja": "僧帽弁粘液腫様変性（MMVD/MVD、小型犬で最多）、拡張型心筋症（DCM、大型犬）、"
                     "心膜疾患、先天性心疾患（PDA、PS、SAS等）、心筋炎、フィラリア症。"
                     "キャバリア、チワワ、マルチーズ等にMMVD好発。ドーベルマン、ボクサーにDCM好発。",
        "treatment_ja": "Stage B2（無症候性だが心拡大あり）：ピモベンダン(0.25mg/kg BID)で心不全発症を遅延。"
                        "Stage C（症候性CHF）：フロセミド(2〜4mg/kg BID〜TID)＋ピモベンダン＋ACE阻害薬(ベナゼプリル)。"
                        "Stage D（難治性）：利尿薬の増量、スピロノラクトン追加、ヒドララジン追加。"
                        "肺水腫急性期：酸素療法＋フロセミドIV bolus。心房細動にはジルチアゼム。"
                        "安静＋低ナトリウム食。",
        "prognosis_ja": "MMVD Stage B2：ピモベンダン投与で心不全発症までの中央期間約1,228日。"
                        "Stage C：中央生存期間約9〜12ヶ月（治療下）。DCMはより予後不良（中央生存期間6〜12ヶ月）。",
        "prevention_ja": "好発品種では定期的な心臓聴診＋胸部X線＋心エコー検査。"
                         "DCM好発犬種ではタウリン・L-カルニチン含有食。フィラリア予防。",
        "urgency": "normal",
    },
    {
        "name": "Allergic Dermatitis",
        "name_ja": "犬アトピー性皮膚炎（CAD）",
        "symptoms": {"itching", "skin_redness", "hair_loss", "ear_scratching",
                      "hot_spots"},
        "description": "An inflammatory skin condition triggered by "
                       "environmental or food allergens.",
        "description_ja": "遺伝的素因を持つ犬がIgE介在性に環境アレルゲンに反応する慢性掻痒性皮膚疾患。"
                          "犬の皮膚疾患で最も多い原因の一つ。1〜3歳で発症が多い。"
                          "柴犬、フレンチブルドッグ、シーズー、ゴールデンレトリバー、ウエストハイランドホワイトテリアに好発。",
        "pathophysiology_ja": "皮膚バリア機能の先天的異常（フィラグリン等の構造タンパク異常）→経皮的アレルゲン侵入→"
                              "Th2優位の免疫応答→IgE産生→マスト細胞脱顆粒→ヒスタミン・サイトカイン放出→"
                              "掻痒・紅斑。慢性化すると苔癬化・色素沈着。二次感染（ブドウ球菌・マラセチア）が併発しやすい。",
        "causes_ja": "環境アレルゲン（ハウスダストマイト、花粉、カビ胞子等）が主因。"
                     "食物アレルゲン（牛肉、鶏肉、小麦、乳製品等）との併発も多い（30%）。"
                     "遺伝的素因、皮膚バリア機能障害がベース。",
        "treatment_ja": "多角的アプローチ：(1)アレルゲン回避（環境整備）、"
                        "(2)薬物療法—オクラシチニブ（アポキル0.4〜0.6mg/kg BID→SID）、"
                        "ロキベトマブ（サイトポイント2mg/kg SC月1回）が第一選択。重症急性期のみ短期プレドニゾロン。"
                        "(3)スキンケア—セラミド配合シャンプー・保湿（週1〜2回）、"
                        "(4)二次感染管理—抗菌薬・抗真菌薬、"
                        "(5)減感作療法（ASIT）—唯一の根治的アプローチ（成功率60〜70%）。",
        "prognosis_ja": "完治は困難だが、適切な管理で良好なQOLを維持可能。"
                        "生涯にわたる管理が必要。二次感染のコントロールが重要。",
        "prevention_ja": "好発品種の繁殖選択、早期からのスキンケア。"
                         "完全な予防は困難だが、皮膚バリア機能の維持が発症抑制に寄与する可能性。",
        "urgency": "normal",
    },
    {
        "name": "Ear Infection (Otitis)",
        "name_ja": "外耳炎",
        "symptoms": {"ear_scratching", "ear_odor", "head_tilting",
                      "pain_on_touch"},
        "description": "Infection or inflammation of the ear canal, often "
                       "bacterial or yeast-related.",
        "description_ja": "外耳道の炎症で、犬の受診理由の上位を占める。垂れ耳犬種（コッカースパニエル、"
                          "ラブラドール、ゴールデンレトリバー等）や耳道が狭い犬種（シャーペイ、フレンチブルドッグ等）に好発。"
                          "基礎疾患としてアトピー性皮膚炎が75%以上に併存。",
        "pathophysiology_ja": "一次因子（アレルギー、異物、角化異常）→耳道環境変化→二次感染因子の増殖"
                              "（マラセチア、ブドウ球菌、緑膿菌）→炎症・浮腫→耳道狭窄→換気不良→さらなる感染の悪循環。"
                              "慢性化すると耳道の線維化・石灰化（end-stage ear）、中耳炎への進展。",
        "causes_ja": "一次因子：アトピー性皮膚炎（最多）、食物アレルギー、耳ダニ（Otodectes cynotis）、異物（草の実）。"
                     "素因：垂れ耳、多毛耳道、狭窄耳道、水泳。二次感染：マラセチア、ブドウ球菌、緑膿菌。",
        "treatment_ja": "耳細胞診（cytology）で原因菌同定→適切な点耳薬選択。"
                        "マラセチア性：ミコナゾール/クロトリマゾール含有点耳薬。"
                        "細菌性：フルオロキノロン含有点耳薬。緑膿菌：トリスEDTA洗浄＋フルオロキノロン。"
                        "耳洗浄（クロルヘキシジン含有洗浄液）。重症例：全身性抗菌薬＋ステロイド。"
                        "End-stage ear：全耳道切除術（TECA-LBO）。基礎疾患（アトピー等）の同時管理が必須。",
        "prognosis_ja": "急性外耳炎：適切な治療で良好。慢性・再発性外耳炎：基礎疾患の管理が鍵。"
                        "耳道石灰化（end-stage）では外科的介入が必要。",
        "prevention_ja": "耳の定期清掃（過剰清掃は禁忌）、水泳後の耳乾燥、基礎アレルギーの管理。",
        "urgency": "normal",
    },
    {
        "name": "Eye Infection (Conjunctivitis)",
        "name_ja": "\u7d50\u819c\u708e",
        "symptoms": {"eye_redness", "eye_discharge", "squinting"},
        "description": "Inflammation of the conjunctiva causing redness, "
                       "discharge, and discomfort.",
        "description_ja": "結膜の炎症により、充血・分泌物・不快感を引き起こします。",
        "pathophysiology_ja": "結膜上皮への感染・アレルゲン・異物刺激→局所免疫反応→血管拡張（充血）・血管透過性亢進（浮腫・漿液/粘液膿性分泌物）。慢性化すると濾胞形成・結膜肥厚が生じる。",
        "causes_ja": "細菌性（Staphylococcus, Streptococcus）、ウイルス性（CDV）、アレルギー性（花粉・ハウスダスト）、異物、乾性角結膜炎（KCS）に続発、化学刺激。短頭種は解剖学的に罹患しやすい。",
        "prevention_ja": "定期的な眼周囲の清拭、刺激物（煙・粉塵）の回避、基礎疾患（KCS・アレルギー）の管理、感染犬との接触回避。",
        "urgency": "normal",
    },
    {
        "name": "Glaucoma",
        "name_ja": "\u7dd1\u5185\u969c",
        "symptoms": {"eye_redness", "squinting", "lethargy", "pain_on_touch"},
        "description": "Increased intraocular pressure that can rapidly lead "
                       "to blindness if untreated.",
        "description_ja": "眼圧の上昇により、治療しないと急速に失明に至る可能性があります。",
        "pathophysiology_ja": "房水の産生・流出バランスの破綻→眼圧上昇（>25mmHg）→視神経乳頭の圧迫・網膜神経節細胞の変性→不可逆的失明。原発性：隅角閉塞（狭隅角）が犬で最多。続発性：水晶体脱臼・ぶどう膜炎・眼内腫瘍に伴う。",
        "causes_ja": "原発性閉塞隅角緑内障（最多、遺伝性）。続発性（水晶体脱臼、ぶどう膜炎、眼内出血、腫瘍）。好発犬種：コッカースパニエル、バセットハウンド、柴犬、シバ、ビーグル。",
        "prevention_ja": "好発犬種の定期的眼圧測定（隅角鏡検査）、片眼発症時の対側眼予防投薬（チモロール・ドルゾラミド）、ぶどう膜炎の早期治療。",
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
        "pathophysiology_ja": "関節軟骨の変性・菲薄化→軟骨下骨の硬化・骨棘形成→滑膜炎→炎症性サイトカイン（IL-1β, TNF-α, MMP）放出→軟骨破壊の悪循環。加齢・肥満・関節不安定性（前十字靭帯断裂後等）が促進因子。",
        "causes_ja": "一次性（加齢性）、二次性（股関節/肘関節形成不全、前十字靭帯断裂、OCD、関節内骨折後）。肥満は最大の修正可能リスク因子。大型犬・超大型犬に好発。",
        "prevention_ja": "適正体重の維持（BCS 4-5/9）、関節に負担の少ない適度な運動、好発犬種の股関節/肘関節スクリーニング、関節サプリメント（グルコサミン・EPA/DHA）の早期投与。",
        "prognosis_ja": "治癒は不可能だが、マルチモーダル管理（NSAIDs＋体重管理＋リハビリ＋関節サプリメント）で多くの症例がQOLを維持。抗NGF抗体（ベジンベトマブ）が新たな選択肢。末期は人工関節置換術を検討。",
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
        "pathophysiology_ja": "前十字靭帯（CrCL）の進行性変性→部分断裂→完全断裂→脛骨前方変位→半月板損傷・関節不安定性→二次性変形性関節症。犬では外傷性より変性性断裂が多い。対側肢も40〜60%が2年以内に断裂。",
        "causes_ja": "慢性変性性靭帯症（最多）、肥満、脛骨高平部角（TPA）の急峻、免疫介在性滑膜炎。好発：ラブラドール、ゴールデンレトリーバー、ロットワイラー。未避妊雌は避妊雌よりリスク低。",
        "prevention_ja": "適正体重の維持、過度のジャンプ・急旋回運動の回避、好発犬種の筋力強化（水泳・リハビリ）、関節サプリメント。",
        "urgency": "normal",
    },
    {
        "name": "Hip Dysplasia",
        "name_ja": "股関節形成不全",
        "symptoms": {"limping_rl", "limping_rr", "stiffness",
                      "reluctance_move", "pain_on_touch"},
        "description": "A genetic skeletal condition where the hip joint "
                       "develops abnormally, leading to arthritis and pain.",
        "description_ja": "股関節の不安定性と亜脱臼を伴う遺伝性の発達性骨格疾患。"
                          "大型〜超大型犬（ジャーマンシェパード、ラブラドール、ゴールデンレトリバー、"
                          "セントバーナード等）に好発。多因子遺伝で環境因子（成長速度、栄養、運動）も関与。",
        "pathophysiology_ja": "寛骨臼と大腿骨頭の適合性不良→関節弛緩→亜脱臼→関節軟骨の摩耗→"
                              "二次性変形性関節症（OA）。成長期の急速な体重増加と不適切な運動が悪化因子。"
                              "関節包の炎症と骨棘形成が慢性疼痛の原因。",
        "causes_ja": "多因子遺伝（遺伝率0.2〜0.6）。環境因子：急速な成長、過剰カロリー摂取、"
                     "成長期の過度な運動。大型犬種に圧倒的に多い。",
        "treatment_ja": "保存療法：体重管理（最重要）、適度な運動（水泳推奨）、NSAIDs（カルプロフェン、メロキシカム）、"
                        "関節サプリメント（グルコサミン＋コンドロイチン）、理学療法。"
                        "外科：若齢犬—JPS、DPO/TPO、FHO。成犬—人工股関節全置換術（THR、根治的）、FHO。",
        "prognosis_ja": "軽症例：保存療法で良好なQOLを維持可能。"
                        "重症例：THRで機能的に正常に近い回復が期待できる。体重管理が予後を大きく左右する。",
        "prevention_ja": "罹患犬の繁殖制限、PennHIP/OFA評価による繁殖適性判定。"
                         "大型犬の成長期のカロリー制限（成長曲線に沿った適正体重管理）。",
        "urgency": "normal",
    },
    {
        "name": "Intervertebral Disc Disease (IVDD)",
        "name_ja": "椎間板ヘルニア（IVDD）",
        "symptoms": {"pain_on_touch", "reluctance_move", *_ANY_LIMPING,
                      "stiffness", "anxiety"},
        "description": "Degeneration or herniation of spinal discs causing "
                       "pain, nerve damage, and potential paralysis.",
        "description_ja": "椎間板の変性・脱出による脊髄圧迫。Hansen I型（急性、軟骨異栄養性犬種）と"
                          "Hansen II型（慢性、大型犬）に分類。ダックスフント（発生率10〜25倍）、"
                          "コーギー、ビーグル、フレンチブルドッグ、ペキニーズに好発。",
        "pathophysiology_ja": "Hansen I型：髄核の軟骨様変性→急性に線維輪を破って脊柱管内へ脱出→脊髄の急性圧迫・挫傷。"
                              "Hansen II型：線維輪の慢性変性・膨隆→脊髄の緩徐な圧迫。"
                              "胸腰部（T11〜L3）が最好発部位。脊髄圧迫の程度によりGrade I（疼痛のみ）〜"
                              "Grade V（深部痛覚消失＋麻痺）に分類。",
        "causes_ja": "軟骨異栄養性犬種の遺伝的素因（Hansen I型）。加齢性変性（Hansen II型）。"
                     "肥満、階段昇降、ジャンプ等の物理的負荷が誘発因子。",
        "treatment_ja": "Grade I〜II（疼痛・歩行可能）：ケージレスト4〜6週間、NSAIDs、ガバペンチン、筋弛緩薬。"
                        "Grade III〜V（麻痺・深部痛覚消失）：緊急外科手術（片側椎弓切除術/腹側減圧術）→"
                        "術後リハビリテーション（水中トレッドミル、理学療法）。"
                        "Grade V（深部痛覚消失48時間以上）：手術の成功率は低い（<5%）。",
        "prognosis_ja": "Grade I〜III：保存療法で80〜90%が改善。外科手術で95%以上。"
                        "Grade IV：外科手術で85〜90%。Grade V（深部痛覚消失<48h）：約60%。"
                        "Grade V（>48h）：予後不良（<5%）。再発率は保存療法で30〜50%。",
        "prevention_ja": "体重管理（最重要）、階段やジャンプの制限（スロープ使用）、"
                         "適度な運動による背筋強化。軟骨異栄養性犬種の飼い主への啓蒙。",
        "urgency": "urgent",
    },
    {
        "name": "Epilepsy",
        "name_ja": "特発性てんかん",
        "symptoms": {"seizures", "circling", "anxiety", "lethargy"},
        "description": "A neurological disorder causing recurrent seizures "
                       "due to abnormal brain activity.",
        "description_ja": "6ヶ月〜6歳で初発する反復性けいれん発作を特徴とする脳の機能性障害。"
                          "構造的・代謝的原因が除外された場合に診断。犬のてんかんの約60%を占める。"
                          "ボーダーコリー、ジャーマンシェパード、ラブラドール、ビーグル、ゴールデンレトリバーに好発。",
        "pathophysiology_ja": "大脳皮質ニューロンの過剰同期性発火→発作。興奮性（グルタミン酸）と"
                              "抑制性（GABA）の神経伝達物質のバランス異常が基盤。"
                              "全般性発作（意識消失・全身強直間代性）と焦点性発作（局所的筋攣縮、意識変容）に分類。"
                              "発作後期（postictal phase）に一時的な失明、徘徊、攻撃性が見られることがある。",
        "causes_ja": "特発性（遺伝性、最多）：多くの犬種で遺伝的背景が示唆されている。"
                     "構造的原因（脳腫瘍、脳炎、外傷、水頭症）や代謝性原因（低血糖、肝性脳症、"
                     "電解質異常）を除外した上で診断。",
        "treatment_ja": "抗てんかん薬による生涯管理：フェノバルビタール（2.5〜5mg/kg BID、第一選択）、"
                        "臭化カリウム（20〜40mg/kg/日、単独or併用）、レベチラセタム（20mg/kg TID、新規薬）。"
                        "血中薬物濃度モニタリング（フェノバルビタール15〜40μg/mL）。"
                        "重積発作：ジアゼパム0.5〜1mg/kg IV/IR→レベチラセタム負荷→"
                        "フェノバルビタールCRI（必要時）。肝機能の定期検査（フェノバルビタール使用時）。",
        "prognosis_ja": "適切な抗てんかん薬で60〜70%の犬が発作の良好なコントロールを達成。"
                        "薬剤抵抗性てんかん（30〜40%）は予後が劣る。"
                        "重積発作や群発発作の反復は予後不良因子。中央生存期間は治療反応犬で2〜5年。",
        "prevention_ja": "確立された予防法なし。好発品種での遺伝的スクリーニングの研究が進行中。"
                         "発作の誘発因子（ストレス、睡眠不足、過度の興奮）の回避。",
        "urgency": "normal",
    },
    {
        "name": "Vestibular Disease",
        "name_ja": "前庭疾患",
        "symptoms": {"head_tilting", "circling", "vomiting", "anxiety",
                      "lethargy"},
        "description": "A condition affecting the inner ear or brainstem, "
                       "causing loss of balance and disorientation.",
        "description_ja": "末梢性（内耳/前庭神経）または中枢性（脳幹/小脳）の前庭系障害。"
                          "特発性（老齢性）前庭疾患が最も多く、高齢犬に突然発症する。"
                          "斜頸、眼振、運動失調、嘔吐が特徴的。脳卒中と間違われやすい。",
        "pathophysiology_ja": "末梢性：内耳の前庭器官または前庭神経の障害→一側性の斜頸・水平眼振（患側向き速相）。"
                              "特発性：原因不明の急性一側性前庭機能障害（ウイルス性前庭神経炎が推測されている）。"
                              "中枢性：脳幹の前庭核障害→垂直眼振・方向変換眼振・固有位置感覚障害→意識レベル変化。"
                              "末梢性と中枢性の鑑別が臨床的に極めて重要。",
        "causes_ja": "末梢性：特発性（老齢犬、最多）、中耳炎/内耳炎、甲状腺機能低下症、耳毒性薬物。"
                     "中枢性：脳腫瘍、脳炎（GME等）、脳血管障害（脳梗塞・出血）、外傷。"
                     "特発性前庭疾患は高齢犬（12歳以上）に好発。",
        "treatment_ja": "特発性前庭疾患：対症療法（制吐薬マロピタント、ジアゼパム短期間で過度の不安に対して）。"
                        "多くは2〜3週間で自然改善。支持療法（補助歩行、スリップ防止マット、給餌補助）。"
                        "中耳炎性：抗菌薬長期投与（4〜6週間）±手術（TECA-LBO）。"
                        "中枢性：原因に応じた治療（脳腫瘍→ステロイド/化学療法/放射線、脳炎→免疫抑制療法）。",
        "prognosis_ja": "特発性前庭疾患：予後良好。72時間で改善開始、2〜3週間でほぼ回復。"
                        "軽度の恒常的斜頸が残る場合があるが、QOLへの影響は少ない。"
                        "中枢性：原因による。脳腫瘍の場合は予後不良。",
        "prevention_ja": "特発性は予防法なし。中耳炎予防のための耳の定期管理。"
                         "甲状腺機能低下症の適切な管理。",
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
        "pathophysiology_ja": "経口・経皮感染→消化管粘膜への付着・穿入→栄養吸収障害・粘膜損傷・出血。回虫は腸管内腔で栄養を奪い、鉤虫は吸血による貧血、鞭虫は大腸粘膜炎症、条虫は栄養吸収競合を引き起こす。大量感染時は腸閉塞のリスク。",
        "causes_ja": "回虫（Toxocara canis）、鉤虫（Ancylostoma caninum）、鞭虫（Trichuris vulpis）、条虫（Dipylidium caninum）、コクシジウム、ジアルジア。糞口感染が主経路。子犬は経胎盤・経乳感染あり。",
        "prevention_ja": "月1回の広域駆虫薬（イベルメクチン・ミルベマイシン・フェンベンダゾール系）、子犬は2週齢から2週間隔で駆虫、年1〜2回の糞便検査、環境の糞便除去、ノミ駆除（条虫予防）。",
        "urgency": "normal",
    },
    {
        "name": "Heartworm Disease",
        "name_ja": "フィラリア症（犬糸状虫症）",
        "symptoms": {"coughing", "lethargy", "difficulty_breathing",
                      "weight_loss", "bloated_abdomen", "excessive_panting"},
        "description": "Parasitic worms residing in the heart and pulmonary "
                       "arteries, causing progressive organ damage.",
        "description_ja": "Dirofilaria immitisが犬の肺動脈と右心室に寄生する致死的寄生虫疾患。"
                          "蚊を介して感染し、成虫は体長15〜30cmに達する。感染から症状発現まで"
                          "6〜7ヶ月の潜伏期間。日本を含む温暖な地域で広く分布。",
        "pathophysiology_ja": "感染性L3幼虫（蚊刺咬）→皮下・筋肉で発育→L5幼虫→血流経由で肺動脈に到達→成虫化。"
                              "肺動脈内膜の機械的損傷→増殖性動脈内膜炎→肺高血圧→右心不全。"
                              "大量寄生時：後大静脈症候群（Caval syndrome）→溶血性貧血、DIC、ショック。"
                              "死滅虫体による肺動脈血栓塞栓症も重大な合併症。",
        "causes_ja": "Dirofilaria immitis。蚊（Aedes, Culex, Anopheles等）が中間宿主。"
                     "感染犬の血液中のミクロフィラリア→蚊体内でL3に発育→新たな犬への感染。"
                     "屋外飼育犬、予防薬未投与犬がハイリスク。",
        "treatment_ja": "【成虫駆除】メラルソミン（イミティサイド）2.5mg/kg 深部筋注×3回（AHSプロトコール）。"
                        "駆除前：ドキシサイクリン（10mg/kg BID 4週間、共生菌Wolbachia駆除）"
                        "＋予防薬開始（ミクロフィラリア対策）。"
                        "成虫駆除後6〜8週間の厳格な運動制限（死滅虫体による肺血栓塞栓症予防）。"
                        "Caval syndrome：外科的虫体摘出（経頸静脈法）。"
                        "Slow kill法（予防薬のみ長期投与）は耐性形成リスクがあり非推奨。",
        "prognosis_ja": "クラス1〜2（軽症〜中等症）：メラルソミン治療で良好（成功率98%）。"
                        "クラス3（重症）：治療リスクは高いが多くは回復可能。"
                        "Caval syndrome：緊急手術で50〜80%生存。無治療では致死的。",
        "prevention_ja": "月1回の予防薬投与（イベルメクチン、ミルベマイシン、モキシデクチン等）が最も有効。"
                         "年1回の抗原検査。蚊の発生する4月〜12月（日本）に通年投与が推奨。"
                         "投与開始前のフィラリア検査が必須。",
        "urgency": "high",
    },
    {
        "name": "Lyme Disease",
        "name_ja": "\u30e9\u30a4\u30e0\u75c5",
        "symptoms": {"fever", *_ANY_LIMPING, "swollen_joints", "lethargy",
                      "appetite_loss"},
        "description": "A tick-borne bacterial infection causing joint "
                       "inflammation, fever, and malaise.",
        "description_ja": "マダニ媒介の細菌感染症で、関節炎・発熱・倦怠感を引き起こします。",
        "pathophysiology_ja": "Ixodes属マダニ刺咬→Borrelia burgdorferiが真皮に侵入→血行性播種→関節滑膜への好中球浸潤→免疫複合体沈着性多発性関節炎。腎糸球体への免疫複合体沈着→致死的ライム腎症（特にラブラドール・ゴールデン）。",
        "causes_ja": "Borrelia burgdorferi sensu lato（マダニIxodes属媒介）。マダニの吸血24〜48時間以上で伝播。日本では北海道に多い。好発：屋外活動犬、猟犬。ラブラドール・ゴールデンはライム腎症リスク高。",
        "prevention_ja": "マダニ駆除薬の通年投与（イソキサゾリン系）、ライム病ワクチン（流行地域）、散歩後のマダニチェック・24時間以内の除去。",
        "urgency": "normal",
    },
    {
        "name": "Pyometra",
        "name_ja": "子宮蓄膿症",
        "symptoms": {"genital_discharge", "excessive_thirst", "lethargy",
                      "fever", "bloated_abdomen", "vomiting"},
        "description": "A serious uterine infection in unspayed females "
                       "requiring emergency surgical intervention.",
        "description_ja": "未避妊の中高齢雌犬に発生する子宮内膜の化膿性感染症。発情後期（黄体期）に発生し、"
                          "開放型（膣からの排膿あり）と閉鎖型（排膿なし→より危険）に分類。"
                          "6歳以上の未避妊雌犬の約25%が発症するとされる。",
        "pathophysiology_ja": "反復する発情周期→プロゲステロンの影響で子宮内膜の嚢胞性過形成（CEH）→"
                              "細菌（主にE. coli）の上行性感染→子宮内膿貯留。"
                              "閉鎖型：膿の排出なし→子宮内圧上昇→菌血症・敗血症・エンドトキシン血症→"
                              "敗血症性ショック。腎障害（内毒素によるADH抵抗性→多飲多尿）を合併。",
        "causes_ja": "プロゲステロンの慢性的子宮内膜刺激（CEH）＋E. coliの上行性感染（最多）。"
                     "外因性プロゲステロン製剤、エストロゲン投与（交配後避妊）がリスク因子。"
                     "未避妊の中高齢雌犬（特に未経産犬）に好発。",
        "treatment_ja": "【第一選択】卵巣子宮摘出術（OHE）→緊急手術。術前に循環安定化（輸液、広域抗菌薬）。"
                        "抗菌薬：アンピシリン＋エンロフロキサシン（E. coli対策）。"
                        "【内科的治療】繁殖温存が必要な場合のみ：アグレプリストン（抗プロゲステロン薬）"
                        "＋プロスタグランジンF2α＋抗菌薬。ただし再発率70%以上。"
                        "閉鎖型は子宮破裂リスクがあり外科が強く推奨。",
        "prognosis_ja": "外科治療：生存率95%以上（敗血症合併がなければ）。"
                        "内科治療：繁殖犬では次の発情での妊娠率50〜60%。再発率が非常に高い。"
                        "敗血症・DIC合併例は予後不良。",
        "prevention_ja": "若齢での避妊手術（OHE）が最も確実な予防法。"
                         "外因性ホルモン投与の回避。繁殖計画終了後の早期避妊。",
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
        "pathophysiology_ja": "ニキビダニ症：Demodex canisの毛包内過剰増殖→毛包炎・脂腺炎→脱毛・二次細菌感染。細胞性免疫の欠陥が基礎にある。疥癬：Sarcoptes scabieiが角質層に穿孔→激しいI型・IV型過敏反応→強烈な掻痒。",
        "causes_ja": "ニキビダニ（D. canis）：免疫抑制・遺伝的素因・若齢/高齢。疥癬（S. scabiei var. canis）：感染犬との直接接触。好発：ニキビダニは短毛種の子犬、疥癬は全犬種。",
        "prevention_ja": "イソキサゾリン系駆虫薬（フルララネル・アフォキソラネル・サロラネル）の通年投与。感染犬との接触回避。免疫抑制の原因（副腎皮質機能亢進症等）の管理。",
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
        "name_ja": "免疫介在性溶血性貧血（IMHA）",
        "symptoms": {"lethargy", "rapid_breathing", "appetite_loss", "fever"},
        "description": "The immune system destroys the body's own red blood "
                       "cells, causing severe anemia.",
        "description_ja": "自己免疫機序により赤血球が破壊される重篤な貧血。犬の免疫介在性疾患で最も多い。"
                          "中年の雌犬に好発。コッカースパニエル、スプリンガースパニエル、プードル、"
                          "アイリッシュセッターに多い。致死率20〜40%の緊急疾患。",
        "pathophysiology_ja": "IgGまたはIgM自己抗体が赤血球膜に結合→脾臓・肝臓のマクロファージによる"
                              "血管外溶血（主要）、または補体活性化による血管内溶血。"
                              "球状赤血球の出現が特徴的。重症例では播種性血管内凝固（DIC）、"
                              "肺血栓塞栓症（PTE）を合併し致死的。赤血球自己凝集が診断的。",
        "causes_ja": "原発性（特発性、70%）：自己免疫の異常活性化。"
                     "二次性（30%）：薬物（セファロスポリン等）、感染症（バベシア、エーリキア）、"
                     "腫瘍（リンパ腫）、ワクチン接種後、蜂刺症。"
                     "免疫介在性血小板減少症（ITP）との併発=エバンス症候群。",
        "treatment_ja": "免疫抑制療法：プレドニゾロン（2mg/kg/日→漸減、4〜6ヶ月かけて減量）。"
                        "難治例：ミコフェノール酸モフェチル、シクロスポリン、アザチオプリンを併用。"
                        "支持療法：輸血（PCV<15%）、酸素療法、輸液。"
                        "血栓予防：クロピドグレル＋低用量アスピリン。DIC時はヘパリン。"
                        "脾摘：薬物抵抗性の場合に検討。",
        "prognosis_ja": "初回発症の生存率60〜80%（適切な治療下）。致死率20〜40%。"
                        "DIC・PTE合併は予後不良。再発率は30〜50%。"
                        "免疫抑制剤の長期投与が必要な場合が多い。",
        "prevention_ja": "確立された予防法なし。既往犬ではワクチン接種のリスク/ベネフィット評価が必要。",
        "urgency": "emergency",
    },
    {
        "name": "Gastroenteritis",
        "name_ja": "急性胃腸炎",
        "symptoms": {"vomiting", "diarrhea", "appetite_loss", "lethargy", "dehydration", "abdominal_pain"},
        "description": "Inflammation of the stomach and intestines, commonly "
                       "from dietary indiscretion or infection.",
        "description_ja": "胃・小腸粘膜の急性炎症で、犬の消化器疾患で最も多い。"
                          "食餌性（ゴミ漁り、食べ慣れないもの）が最も一般的な原因。"
                          "全犬種・全年齢で発生するが、若齢犬に多い。",
        "pathophysiology_ja": "有害物質・病原体による胃腸粘膜の直接障害→粘膜炎症→"
                              "消化吸収障害（下痢）、胃粘膜刺激（嘔吐）→脱水・電解質異常。"
                              "重症例（出血性胃腸炎/HGE/AHDS）では腸管透過性亢進→菌血症・エンドトキシン血症。",
        "causes_ja": "食餌性（ゴミ漁り、食事変更、過食、腐敗食）が最多。"
                     "感染性（パルボウイルス、コロナウイルス、サルモネラ、カンピロバクター、ジアルジア）。"
                     "ストレス性、薬物性（NSAIDs、抗菌薬）。",
        "treatment_ja": "軽症例：24時間の消化管安静→消化の良い低脂肪食（茹で鶏肉＋白米）で再開。"
                        "中等症以上：制吐薬（マロピタント）、皮下or静脈輸液、"
                        "下痢止め（スメクタイト等の吸着薬）。抗菌薬は細菌感染が確認された場合のみ。"
                        "HGE/AHDSでは積極的輸液＋抗菌薬（アンピシリン）。",
        "prognosis_ja": "食餌性の単純な胃腸炎：2〜3日で自然回復し予後良好。"
                        "HGE/AHDS：積極的治療で90%以上が回復。脱水放置は危険。",
        "prevention_ja": "ゴミ漁り防止、急な食事変更を避ける（5〜7日かけて移行）、"
                         "テーブルフードや高脂肪食の制限。",
        "urgency": "normal",
    },
    {
        "name": "Brachycephalic Airway Syndrome",
        "name_ja": "短頭種気道症候群（BAS）",
        "symptoms": {"difficulty_breathing", "snoring", "excessive_panting",
                      "reverse_sneezing", "coughing"},
        "description": "A set of upper airway abnormalities common in "
                       "short-nosed breeds, causing breathing difficulties.",
        "description_ja": "短頭種犬（フレンチブルドッグ、パグ、ブルドッグ、ペキニーズ等）に見られる"
                          "複数の上気道狭窄の複合病態。外鼻孔狭窄、軟口蓋過長、喉頭小嚢外転、"
                          "気管低形成を特徴とする。暑熱・興奮・運動時に呼吸困難が悪化。",
        "pathophysiology_ja": "頭蓋骨の短縮→上気道の解剖学的スペース不足→一次的異常（外鼻孔狭窄、軟口蓋過長、"
                              "気管低形成）→呼吸抵抗増大→代償的な強吸気→二次的変化（喉頭小嚢外転、喉頭虚脱）。"
                              "悪化の悪循環により最終的に喉頭虚脱→致死的上気道閉塞。肥満が大きな悪化因子。",
        "causes_ja": "遺伝的に決定された頭蓋骨構造の短縮。短頭種犬全般に見られる。"
                     "重症度は品種と個体により異なる。肥満、高温多湿環境、過度の興奮が症状を増悪させる。",
        "treatment_ja": "外科矯正（若齢時に推奨）：外鼻孔拡大術（alaeplasty）、軟口蓋切除術（staphylectomy）、"
                        "喉頭小嚢切除術。二次的喉頭虚脱（Stage III）では永久気管切開が必要な場合も。"
                        "内科管理：体重管理（最重要）、涼しい環境、興奮回避、短時間の散歩。"
                        "急性呼吸困難：酸素療法、鎮静、ステロイド（気道浮腫軽減）、緊急挿管。",
        "prognosis_ja": "早期外科矯正で良好〜極めて良好。術後呼吸状態の著明な改善が期待できる。"
                        "喉頭虚脱に進行した場合は予後が劣る。体重管理が長期予後を大きく左右。",
        "prevention_ja": "繁殖選択による極端な短頭化の回避。体重管理。高温多湿環境の回避。"
                         "外鼻孔狭窄は避妊去勢手術時の同時矯正が推奨。",
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
        "description_ja": "Leptospira interrogansを原因とする人獣共通感染症。急性腎不全および肝不全を引き起こす。"
                          "野生動物の尿に汚染された水や土壌との接触で感染。秋〜冬の降雨後に多い。"
                          "都市部でも増加傾向にあり、公衆衛生上も重要。",
        "pathophysiology_ja": "経皮・経粘膜感染→レプトスピラ血症→腎尿細管上皮への定着→間質性腎炎→急性腎障害（AKI）。"
                              "肝臓では肝細胞の腫大・胆汁うっ滞→黄疸。血管内皮障害→出血傾向、肺出血。"
                              "感染犬は回復後も数ヶ月間尿中にレプトスピラを排菌し、感染源となる。",
        "causes_ja": "Leptospira interrogans（L. canicola, L. icterohaemorrhagiae, L. pomona, L. grippotyphosa等）。"
                     "感染動物（ネズミ、野生動物）の尿に汚染された水・土壌との接触。"
                     "外飼い犬、狩猟犬、水辺活動犬がハイリスク。人にも感染する（人獣共通感染症）。",
        "treatment_ja": "急性期：ペニシリン系（アンピシリン20mg/kg IV TID）で菌血症を制御→"
                        "その後ドキシサイクリン（5mg/kg BID 2〜3週間）で腎排菌を停止。"
                        "支持療法：AKIに対する積極的輸液（乏尿期の管理が重要）、電解質補正、"
                        "制吐薬、必要時に透析。肝障害に対する支持療法。"
                        "飼い主への感染リスク説明（手洗い、尿の取り扱い注意）。",
        "prognosis_ja": "早期治療で生存率80〜90%。乏尿性AKI合併例は予後が劣る（透析が必要な場合あり）。"
                        "肺出血型（LPHS）は致死率が高い。腎機能の完全回復は症例による。",
        "prevention_ja": "ワクチン接種（4価レプトスピラワクチン、年1回）。"
                         "汚染水域への暴露回避。野生動物との接触制限。",
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
        "pathophysiology_ja": "CAV-1の経口鼻感染→扁桃リンパ組織で増殖→ウイルス血症→肝細胞・血管内皮・腎尿細管上皮への親和性→肝細胞壊死・DIC・腎間質性腎炎。回復期に免疫複合体沈着→「ブルーアイ」（前部ぶどう膜炎・角膜浮腫）。",
        "causes_ja": "犬アデノウイルス1型（CAV-1）。感染犬の尿・唾液・糞便から排泄。環境中で数ヶ月生存。ワクチン未接種犬、特に1歳未満がリスク高。",
        "prevention_ja": "コアワクチン（CAV-2含有5種・7種ワクチン）の適切な接種スケジュール。CAV-2ワクチンがCAV-1に交差防御を与える。",
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
        "pathophysiology_ja": "マダニ（Rhipicephalus sanguineus）刺咬→Ehrlichia canisが単球・マクロファージに感染→細胞内で封入体（morula）を形成→3相の経過：急性期（1〜3週間：発熱・リンパ節腫大・血小板減少）→無症候キャリア期（数ヶ月〜数年：脾臓でのEhrlichia持続感染）→慢性期（汎血球減少・骨髄低形成・出血傾向→致死的）。免疫複合体沈着→多発性関節炎・糸球体腎炎。",
        "causes_ja": "Ehrlichia canis（最多、マダニRhipicephalus sanguineus媒介）。日本では西日本を中心に分布。輸入犬・沖縄に多い。慢性キャリア犬が感染源。ジャーマンシェパードは慢性期への進展リスクが高い。",
        "prevention_ja": "マダニ駆除薬（イソキサゾリン系）の通年投与、散歩後のマダニチェック、海外渡航犬のスクリーニング（4DxSNAP検査）。",
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
        "pathophysiology_ja": "A. phagocytophilum：マダニ（Ixodes属）刺咬→好中球に感染→morula形成→免疫介在性血小板減少・多発性関節炎→発熱・跛行・血小板減少。A. platys：血小板に感染→周期的血小板減少症。多くは急性期のみで自然治癒するが、免疫抑制犬では重症化。Lyme病との重複感染（同じIxodes属マダニ媒介）がある。",
        "causes_ja": "Anaplasma phagocytophilum（Ixodes属マダニ媒介、北半球に分布）、A. platys（R. sanguineus媒介）。日本ではA. phagocytophilumの報告あり。ライム病・バベシア症との共感染に注意。4DxSNAP検査でスクリーニング可能。",
        "prevention_ja": "マダニ駆除薬の通年投与、マダニ媒介感染症流行地域での注意強化。ドキシサイクリン14日間で治療反応良好。",
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
        "pathophysiology_ja": "マダニ刺咬→Babesia canis/gibsoniのスポロゾイトが赤血球に侵入→赤血球内増殖→赤血球の破壊（血管内溶血）→溶血性貧血・ヘモグロビン尿・黄疸。重症型では免疫介在性溶血の合併、DIC、急性腎障害、脳バベシア症（中枢神経症状）。B. gibsoniは日本で主流、慢性キャリアとなりやすい。",
        "causes_ja": "B. canis（大型バベシア、マダニRhipicephalus属媒介）、B. gibsoni（小型バベシア、マダニHaemaphysalis属媒介）。日本ではB. gibsoniが主流（西日本に多い）。マダニ刺咬、輸血、闘犬による直接血液接触でも伝播。アメリカンピットブルテリアに好発。",
        "prevention_ja": "マダニ駆除薬（イソキサゾリン系）の通年投与、散歩後のマダニチェック、流行地域での注意強化、輸血前のPCRスクリーニング。",
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
        "pathophysiology_ja": "腸管粘膜の免疫調節障害→常在腸内細菌叢に対する過剰な免疫応答→リンパ球・形質細胞浸潤（リンパ球形質細胞性が最多）→粘膜障害・絨毛萎縮→吸収不良。蛋白漏出性腸症（PLE）を合併する場合は低アルブミン血症。",
        "causes_ja": "正確な原因は不明。遺伝的素因・腸内細菌叢異常・食物抗原に対する免疫異常が複合。確定診断には内視鏡生検が必須（リンパ腫との鑑別が重要）。好発：ジャーマンシェパード、バセンジー、シャーペイ。",
        "prevention_ja": "確実な予防法はないが、良質な消化性の高い食事、プロバイオティクス、ストレス軽減が有用。",
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
        "pathophysiology_ja": "食道の蠕動運動障害→食道の全般的拡張→食物の口腔側への逆流（吐出、regurgitation：嘔吐と異なり腹部の収縮を伴わない受動的排出）→誤嚥性肺炎（最も重大な合併症、主要な死因）。先天性（食道壁の神経叢発育不全）と後天性（重症筋無力症・甲状腺機能低下症・アジソン病等）に分類。",
        "causes_ja": "先天性（ワイヤーヘアードフォックステリア・ミニチュアシュナウザーで遺伝性、ジャーマンシェパード・グレートデーンに好発）。後天性：特発性（最多）、重症筋無力症（最も重要な鑑別）、甲状腺機能低下症、アジソン病、鉛中毒、食道炎後。",
        "prevention_ja": "確実な予防法はない。後天性の場合は基礎疾患（重症筋無力症・甲状腺機能低下症）の検索と治療が必須。管理：立位給餌（Bailey chair、食後10〜15分保持）、高カロリー流動食、誤嚥性肺炎の早期発見・治療。",
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
        "pathophysiology_ja": "膵腺房細胞の90%以上が喪失→消化酵素（リパーゼ・アミラーゼ・プロテアーゼ）の著明な分泌低下→脂肪・蛋白質・炭水化物の消化不全→吸収不良→大量の黄色〜灰白色・脂肪光沢のある軟便（脂肪便）・体重減少・多食。小腸内細菌過増殖（SIBO）の合併が高率。コバラミン（VitB12）欠乏が予後に影響。",
        "causes_ja": "膵腺房萎縮（PAA、免疫介在性、最多）：ジャーマンシェパードに好発（遺伝性）、ラフコリー。慢性膵炎の末期。膵腫瘍。若齢〜中齢犬に多い（PAA：1〜5歳）。血清TLI（trypsin-like immunoreactivity）<2.5μg/Lで確定診断。",
        "prevention_ja": "好発犬種の繁殖管理。確定診断後は膵酵素補充療法（パンクレアチン散を毎食混合）が生涯必要。コバラミン補充（注射）、低脂肪・高消化性食。",
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
        "pathophysiology_ja": "異物による腸管内腔の閉塞→口側の腸管拡張・液体貯留→腸壁の虚血→穿孔のリスク。線状異物（糸・紐）は特に危険：腸管のアコーディオン状plication→多発穿孔→腹膜炎。脱水・電解質異常・敗血症が急速に進行。",
        "causes_ja": "玩具・靴下・コーンコブ・骨片・果物の種・縫い針・紐状異物。好発：若齢犬（1〜3歳）、ラブラドール、ゴールデン等の口に入れやすい犬種。",
        "prevention_ja": "飲み込み可能な物の管理（小さな玩具・靴下・紐の放置禁止）、適切なサイズの咀嚼玩具の選択、拾い食い防止のトレーニング。",
        "urgency": "emergency",
    },
    {
        "name": "Hemorrhagic Gastroenteritis (HGE)",
        "name_ja": "急性出血性下痢症候群（AHDS/HGE）",
        "symptoms": {"bloody_stool", "vomiting", "diarrhea", "lethargy",
                      "appetite_loss"},
        "description": "Acute hemorrhagic diarrhea syndrome with sudden onset "
                       "of bloody stool and rapid dehydration.",
        "description_ja": "突然発症のジャム状〜ケチャップ様血便と急速な脱水を特徴とする急性症候群。"
                          "小型犬（ミニチュアシュナウザー、トイプードル、ヨークシャーテリア等）に好発。"
                          "現在はAHDS（Acute Hemorrhagic Diarrhea Syndrome）と呼称。",
        "pathophysiology_ja": "正確な機序は不明だが、Clostridium perfringens（netF毒素産生株）が"
                              "主要な病因として示唆されている。腸管粘膜の急性壊死性障害→"
                              "大量の血液・タンパク質の腸管内喪失→急速な血液濃縮（PCV 60〜80%）→"
                              "粘度上昇→DIC・血栓塞栓症のリスク。敗血症の合併もあり。",
        "causes_ja": "Clostridium perfringens（netF毒素陽性株）が最も有力な原因菌。"
                     "ストレス、食餌性因子、免疫学的要因も関与。明確な原因は不明で特発性とされることが多い。"
                     "小型犬に好発（体質的要因の関与を示唆）。",
        "treatment_ja": "【緊急】(1)積極的静脈輸液（晶質液＋膠質液）→循環血液量回復が最優先、"
                        "(2)制吐薬（マロピタント）、(3)広域抗菌薬（アンピシリン＋メトロニダゾール）で"
                        "菌血症予防、(4)早期経腸栄養（可能な限り早期に開始）。"
                        "輸血はPCV低下時に検討（血液濃縮が解除された後に貧血が顕在化する場合がある）。",
        "prognosis_ja": "積極的な輸液療法で生存率95%以上。多くは2〜3日で劇的に改善。"
                        "DIC合併や治療遅延は致死的。再発率は比較的低い（約10〜15%）。",
        "prevention_ja": "確実な予防法はないが、ストレス回避、良質な食事管理、"
                         "プロバイオティクスの投与が有用である可能性。",
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
        "pathophysiology_ja": "大腸粘膜の炎症→水分・電解質吸収障害→少量頻回の粘液/血液混じり軟便。テネスムス（しぶり）が特徴的。急性：ストレス性・食餌性・感染性。慢性：IBD・好酸球性腸炎・組織球性潰瘍性大腸炎（ボクサー）。",
        "causes_ja": "急性：食餌性（不適切な食物・食物不耐性）、ストレス性、Clostridium/Campylobacter感染、鞭虫。慢性：IBD、食物アレルギー、好酸球性腸炎。好発：ボクサー（組織球性潰瘍性大腸炎）。",
        "prevention_ja": "良質な一定した食事、食餌変更の漸進的実施、ストレス管理、定期的な寄生虫駆除（鞭虫予防）。",
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
        "pathophysiology_ja": "門脈血が肝臓を迂回して全身循環に流入→肝臓での解毒・代謝が不十分→高アンモニア血症→肝性脳症（旋回運動・失見当・けいれん・昏迷）。尿酸塩結石の形成（肝臓での尿酸代謝障害）。肝臓の発育不全（microhepatica）。先天性（肝外性/肝内性）と後天性（門脈圧亢進に続発する多発性）に分類。",
        "causes_ja": "先天性（最多）：肝外性は小型犬（ヨークシャーテリア、マルチーズ、シーズー、ミニチュアシュナウザー）に好発。肝内性は大型犬（アイリッシュウルフハウンド、ラブラドール）。後天性：慢性肝疾患・門脈圧亢進に続発。多くは1歳未満で発症。",
        "prevention_ja": "好発犬種の繁殖管理（罹患犬の繁殖制限）。食後の異常行動（食後脳症）を示す若齢犬は早期に血清胆汁酸検査でスクリーニング。",
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
        "pathophysiology_ja": "心筋細胞の変性・線維化→心室壁の菲薄化・心室拡大→収縮力低下（FS<20%）→心拍出量低下→神経体液性代償機構（RAAS活性化）→体液貯留→うっ血性心不全。心房細動の合併が多い。突然死（心室頻拍）のリスク。",
        "causes_ja": "特発性（最多）、遺伝性（ドーベルマン：PDK4/TTN遺伝子変異）、タウリン/L-カルニチン欠乏（コッカースパニエル等）、穀物フリーダイエット関連（FDA調査中）。好発：ドーベルマン、グレートデーン、ボクサー、アイリッシュウルフハウンド。",
        "prevention_ja": "好発犬種の定期的心臓スクリーニング（心エコー・ホルター心電図）、適切な栄養（タウリン・L-カルニチン含有食）、穀物フリーダイエットの回避。",
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
        "pathophysiology_ja": "出生後に動脈管（大動脈-肺動脈間）が閉鎖しない→左-右シャント→肺血流増加→左房・左室の容量負荷→左心拡大→うっ血性心不全。大型シャントでは肺高血圧→アイゼンメンジャー症候群（シャント逆転、右-左）→チアノーゼ（差別的チアノーゼ：後肢のみ）。聴診で連続性心雑音（machinery murmur）が特徴的。",
        "causes_ja": "多遺伝子性の先天性心疾患。犬で最も多い先天性心疾患の一つ。好発犬種：マルチーズ、ポメラニアン、シェルティ、ミニチュアプードル、ジャーマンシェパード。雌に多い（3:1）。",
        "prevention_ja": "好発犬種の心臓聴診スクリーニング（子犬検診時）。罹患犬の繁殖制限。早期発見後の外科的閉鎖術（カテーテルコイル塞栓 or 開胸結紮）で予後良好。",
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
        "pathophysiology_ja": "大動脈弁下部（SAS、犬で最多）・弁性・弁上部の狭窄→左室流出路閉塞→左室圧負荷→左室求心性肥大→心筋酸素需要増大→心筋虚血→失神・突然死（心室性不整脈）。圧較差>80mmHgの重症例は突然死リスクが高い。聴診で左心基底部のcrescendo-decrescendo収縮期雑音。",
        "causes_ja": "先天性（多遺伝子性遺伝）。大型犬：ゴールデンレトリーバー、ニューファンドランド、ロットワイラー、ボクサー、ジャーマンシェパード。弁下性線維輪（SAS）が犬で最も多い型。軽度は無症状で偶然発見、重度は運動不耐性・失神・突然死。",
        "prevention_ja": "好発犬種の心臓聴診スクリーニング（子犬検診〜繁殖前）、罹患犬の繁殖制限、心エコーによる圧較差測定で重症度評価。重度は激しい運動制限。",
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
        "pathophysiology_ja": "心嚢腔への液体（血液・漿液）貯留→心嚢内圧上昇→心臓の拡張障害（心タンポナーデ）→心拍出量低下→右心不全徴候（頸静脈怒張・腹水・肝腫大）→心原性ショック。急性大量貯留は致死的。腫瘍性（血管肉腫が犬で最多）と特発性に大別。心エコーで診断、心嚢穿刺が緊急的治療。",
        "causes_ja": "腫瘍性（右心房血管肉腫が最多、中皮腫、心基底部腫瘍）、特発性（良性反復性）、心不全性、感染性、凝固障害。大型犬・大型犬種（ゴールデンレトリーバー、ジャーマンシェパード、ラブラドール）に好発。",
        "prevention_ja": "確実な予防法はない。好発犬種の定期的な心臓聴診・心エコー。特発性反復性は心嚢膜切除術（pericardiectomy）で再発防止。腫瘍性は原疾患の管理が鍵。",
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
        "pathophysiology_ja": "皮膚バリア機能の破綻→常在菌（主にStaphylococcus pseudintermedius）の過剰増殖→表在性：表皮小環（epidermal collarette）・膿疱形成。深在性：毛包破裂→真皮・皮下組織への細菌浸潤→蜂窩織炎・瘻管形成。",
        "causes_ja": "基礎疾患（アトピー性皮膚炎、食物アレルギー、甲状腺機能低下症、クッシング症候群）による皮膚バリア破綻が最多。主要起因菌はS. pseudintermedius。メチシリン耐性株（MRSP）の増加が問題。",
        "prevention_ja": "基礎疾患の適切な管理、定期的なシャンプー療法（クロルヘキシジン2〜4%）、皮膚の乾燥・湿潤環境の回避。再発性の場合は基礎疾患の精査が必須。",
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
        "pathophysiology_ja": "病態は完全に解明されていない。毛周期の休止期（telogen）への停止→二次毛（アンダーコート）は残存するが一次毛（ガードヘア）が再生しない→体幹の対称性脱毛。副腎性ホルモン（sex hormone）の不均衡が疑われるが一貫した所見はない。皮膚の色素沈着が進行。全身的には健康で痒みはない。",
        "causes_ja": "原因不明（「X」は未知の意）。副腎sex hormoneの代謝異常が疑われる。好発犬種：ポメラニアン（最多）、チャウチャウ、サモエド、アラスカンマラミュート、ケースホンド。去勢/避妊済みの若齢〜中齢犬に多い。甲状腺機能低下症・クッシング症候群の除外が必要。",
        "prevention_ja": "確実な予防法はない。美容的問題であり全身的健康に影響しない。メラトニン（3〜6mg PO BID）で約50%に発毛効果。トリロスタンは一部で有効だが副作用のリスクあり。",
        "urgency": "normal",
    },
    {
        "name": "Acral Lick Dermatitis",
        "name_ja": "肢端舐性皮膚炎",
        "symptoms": {"itching", "skin_redness", "hair_loss", "anxiety"},
        "description": "A self-inflicted skin lesion from compulsive licking, "
                       "often with underlying psychological or physical causes.",
        "description_ja": "強迫的な舐め行動により生じる自傷性皮膚病変で、心因性または身体的原因があります。",
        "pathophysiology_ja": "反復的な舐め行動→表皮の機械的損傷→真皮の線維化・肉芽組織形成→掻痒-舐め-損傷の悪循環。慢性化すると表皮肥厚・毛包炎・深部細菌感染。内因性オピオイド放出が自己強化行動を維持。",
        "causes_ja": "心因性（退屈・分離不安・強迫性障害）、身体的（変形性関節症・神経障害性疼痛・異物・アレルギー）が複合。好発：ドーベルマン、ラブラドール、グレートデーン等の大型犬。",
        "prevention_ja": "十分な運動と精神的刺激（知育玩具・トレーニング）、分離不安の早期対応、基礎疾患（OA・アレルギー）の管理、環境エンリッチメント。",
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
        "pathophysiology_ja": "第三眼瞼腺（瞬膜腺）を固定する結合組織の先天的脆弱性→腺組織の脱出→露出した腺の乾燥・炎症・二次感染→涙液産生の約30〜40%を担う腺の機能障害→KCS（ドライアイ）リスク。",
        "causes_ja": "先天的な結合組織の脆弱性。好発犬種：コッカースパニエル、ブルドッグ、ビーグル、バセットハウンド、シャーペイ。通常2歳未満で発症。",
        "prevention_ja": "確実な予防法はない。発症後は腺の切除ではなく外科的整復（ポケット法・アンカー法）を推奨（切除するとKCSリスク上昇）。",
        "urgency": "normal",
    },
    {
        "name": "Keratoconjunctivitis Sicca (Dry Eye)",
        "name_ja": "乾性角結膜炎（ドライアイ）",
        "symptoms": {"eye_discharge", "squinting", "eye_redness"},
        "description": "Insufficient tear production causing chronic eye "
                       "irritation, discharge, and potential corneal damage.",
        "description_ja": "涙液分泌不足による慢性的な眼の刺激・分泌物・角膜障害のリスクがあります。",
        "pathophysiology_ja": "涙腺の免疫介在性破壊（最多）→涙液分泌低下（STT<15mm/min）→眼表面の乾燥→角膜上皮の角化・色素沈着→粘液膿性分泌物の蓄積→二次細菌感染・角膜潰瘍のリスク上昇。",
        "causes_ja": "免疫介在性（最多、約80%）、薬剤性（サルファ剤・エトドラク）、神経性（顔面神経麻痺）、先天性、内分泌性（甲状腺機能低下症）、CDV後遺症。好発：コッカースパニエル、ブルドッグ、シーズー、WHWT。",
        "prevention_ja": "好発犬種では定期的なSTT（シルマー涙液試験）によるスクリーニング。サルファ剤等の起因薬剤の慎重投与。早期発見・治療開始が角膜障害予防の鍵。",
        "urgency": "normal",
    },
    {
        "name": "Entropion",
        "name_ja": "眼瞼内反症",
        "symptoms": {"eye_redness", "eye_discharge", "squinting"},
        "description": "Inward rolling of the eyelid causing the lashes to "
                       "rub against the cornea, leading to irritation.",
        "description_ja": "眼瞼が内側に反転し、睫毛が角膜を擦って刺激を引き起こします。",
        "pathophysiology_ja": "眼瞼縁の内方回転→睫毛・被毛が角膜に接触→機械的刺激→角膜びらん・潰瘍→角膜血管新生・色素沈着（慢性例）→視力低下。痙攣性内反は疼痛による二次的筋痙攣で悪化。",
        "causes_ja": "先天性（最多）：眼瞼形態の遺伝的要因。好発犬種：シャーペイ、チャウチャウ、ブルドッグ、ラブラドール、ロットワイラー。後天性：慢性眼疾患、急激な体重減少。",
        "prevention_ja": "好発犬種の計画的繁殖、早期発見・外科矯正（Hotz-Celsus法）、子犬期の一時的タッキング。",
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
        "pathophysiology_ja": "角膜上皮の欠損→実質の露出→細菌性コラゲナーゼ（特にPseudomonas）による融解性潰瘍のリスク→デスメ膜瘤（descemetocele）→穿孔。表在性：上皮のみ。深在性：実質の1/3以上。難治性（SCCED/ボクサー潰瘍）：基底膜異常で上皮接着不良。",
        "causes_ja": "外傷（最多）、異物、KCS、内反症・睫毛乱生、化学刺激、Pseudomonas/Streptococcus感染。短頭種（眼球突出で角膜露出増加）に好発。SCCED：中高齢犬に好発。",
        "prevention_ja": "眼刺激の原因除去（内反症矯正、KCS治療）、短頭種の眼球保護、外傷予防。SCCED既往犬は再発注意。",
        "urgency": "urgent",
    },
    {
        "name": "Lens Luxation",
        "name_ja": "水晶体脱臼",
        "symptoms": {"eye_redness", "squinting", "pain_on_touch"},
        "description": "Displacement of the lens from its normal position, "
                       "potentially leading to glaucoma and blindness.",
        "description_ja": "水晶体の正常位置からのずれで、緑内障や失明に至る可能性があります。",
        "pathophysiology_ja": "毛様体小帯（チン小帯）の変性・断裂→水晶体の前方脱臼（緊急）または後方脱臼。前方脱臼→瞳孔ブロック→急性緑内障→失明。ADAMTS17遺伝子変異が原発性の主因。続発性は慢性緑内障・ぶどう膜炎・腫瘍に伴う。",
        "causes_ja": "原発性（遺伝性、ADAMTS17変異）：テリア種に好発（ジャックラッセル、ミニチュアブルテリア、チベタンテリア）。3〜8歳で発症。続発性：慢性緑内障・ぶどう膜炎・眼内腫瘍・外傷。",
        "prevention_ja": "好発犬種のADAMTS17遺伝子検査、キャリア犬の繁殖制限、定期眼科検診（水晶体の亜脱臼の早期発見）。",
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
        "pathophysiology_ja": "3つの病態の総称：(1)内側鈎状突起離断（FCP）、(2)肘頭内側面のOCD、(3)肘突起癒合不全（UAP）。橈骨尺骨の成長不均衡→関節の不整合→軟骨損傷→早期OA。遺伝的要因＋急速な成長・過剰栄養が誘因。",
        "causes_ja": "多因子性（遺伝＋環境）。好発：ラブラドール、ゴールデン、ジャーマンシェパード、ロットワイラー、バーニーズ。4〜8月齢で発症。急速な成長・高カロリー食がリスク。",
        "prevention_ja": "好発犬種の肘関節スクリーニング（X線）、子犬期の適正な成長速度維持（過剰栄養の回避）、責任ある繁殖（スコアリング制度利用）。",
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
        "pathophysiology_ja": "長骨骨幹部の骨髄腔内の炎症→骨内膜の肥厚・骨髄浮腫→骨膜の刺激→深部骨痛。移動性跛行（shifting lameness）が特徴的：日によって異なる肢が跛行する。X線で骨髄腔内の不透過性亢進（骨幹部の雲状影）。自己限定的で通常2〜5ヶ月齢〜18ヶ月齢の間に発症し、2歳までに自然治癒。",
        "causes_ja": "原因不明。急速な骨成長に伴う骨髄内血管の変化・ストレスが疑われる。大型犬・超大型犬の雄犬（5〜18ヶ月齢）に好発：ジャーマンシェパード（最多）、バセットハウンド、ゴールデン、ラブラドール。遺伝的素因あり。骨肉腫との鑑別が重要。",
        "prevention_ja": "確実な予防法はない。自己限定的疾患のため対症療法（NSAIDs）で疼痛管理。過度の安静は不要。骨肉腫との鑑別のため経過観察が重要（通常は数週間で自然寛解）。",
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
        "pathophysiology_ja": "脳脊髄液（CSF）の産生・吸収・循環の不均衡→脳室内のCSF蓄積→脳室拡大→脳実質の圧迫・萎縮→神経機能障害。先天性（中脳水道狭窄が最多）と後天性（腫瘍・炎症による閉塞）に分類。開放泉門（molera）が触知可能な場合が多い。",
        "causes_ja": "先天性（トイ犬種：チワワ、ポメラニアン、マルチーズ、ヨークシャーテリア、トイプードル）、後天性（脳腫瘍・脳炎・脳内出血によるCSF循環障害）。先天性は生後数ヶ月で発症。ドーム状頭蓋・斜視が身体的特徴。",
        "prevention_ja": "好発犬種の責任ある繁殖（極端な小型化の回避）、子犬期の神経学的異常の早期発見。軽度は内科管理（オメプラゾール・プレドニゾロン・アセタゾラミド）、重度は脳室-腹腔シャント術。",
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
        "pathophysiology_ja": "大脳皮質のβアミロイド沈着・ニューロン喪失・酸化的損傷→前頭葉・海馬の萎縮→DISHAAL症状（見当識障害・社会的交流変化・睡眠覚醒サイクルの乱れ・不適切排泄・活動性変化・不安・学習記憶低下）。ドーパミン・セロトニン系の減少も関与。",
        "causes_ja": "加齢に伴う脳の変性（βアミロイド蓄積・酸化ストレス・ミトコンドリア機能障害）。11歳以上の犬の28%、15歳以上の68%が罹患。全犬種で発症するが、小型犬はより長寿のため臨床的に顕在化しやすい。",
        "prevention_ja": "脳への抗酸化物質（ビタミンE・C、α-リポ酸・L-カルニチン）含有食、精神的刺激（トレーニング・知育玩具）、適度な運動、EPA/DHAサプリメント。",
        "urgency": "normal",
    },
    {
        "name": "Myasthenia Gravis",
        "name_ja": "重症筋無力症",
        "symptoms": {"lethargy", "reluctance_move", "difficulty_breathing",
                      "regurgitation"},
        "description": "An autoimmune neuromuscular disease causing muscle "
                       "weakness, often associated with megaesophagus.",
        "description_ja": "筋力低下を引き起こす自己免疫性神経筋疾患で、巨大食道症を伴うことが多いです。",
        "pathophysiology_ja": "後天性（最多）：ニコチン性アセチルコリン受容体（AChR）に対する自己抗体→神経筋接合部でのAChR破壊→神経筋伝達障害→骨格筋の易疲労性。局所型：食道筋（巨大食道症→誤嚥性肺炎）・咽頭筋・顔面筋に限局。全身型：四肢筋力低下・運動不耐性。胸腺腫の合併が5〜15%。",
        "causes_ja": "後天性免疫介在性（最多）、先天性（ジャックラッセルテリア・スムースフォックステリア等のAChR遺伝子変異）。後天性は中高齢犬（5〜10歳）に多い。ゴールデンレトリーバー、ジャーマンシェパード、ダックスフンドに好発。",
        "prevention_ja": "確実な予防法はない。巨大食道症の犬では抗AChR抗体価の測定でスクリーニング。誤嚥性肺炎の予防（立位給餌）が生命予後に直結。自然寛解例も報告（約50%が6〜18ヶ月で寛解）。",
        "urgency": "high",
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
        "symptoms": {"swelling", "abdominal_pain"},
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
        "pathophysiology_ja": "授乳による急速なCa喪失→血清Ca<7mg/dL→神経筋興奮性亢進→筋線維束攣縮・テタニー→全身性けいれん→高体温→DIC→死亡。泌乳量がCa動員能を超えた時に発症。分娩後1〜3週間がピーク。",
        "causes_ja": "泌乳によるCa喪失が骨吸収・腸管吸収を上回る状態。リスク因子：小型犬、多産、初産、妊娠中の不適切なCaサプリメント（PTH抑制）、栄養不良。好発：チワワ、トイプードル、ヨークシャーテリア。",
        "prevention_ja": "妊娠中のCaサプリメント過剰投与の回避（PTH分泌を抑制するため逆効果）、分娩後のバランスの取れた高栄養食、大型の産子には早期から人工補乳、子犬の早期離乳（3〜4週齢から）。",
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
        "pathophysiology_ja": "気管軟骨のグリコサミノグリカン・コンドロイチン硫酸の減少→軟骨輪の扁平化→背側膜の弛緩→吸気時（頸部気管）/呼気時（胸腔内気管）の気管内腔狭窄→ガチョウ鳴様咳嗽。慢性気道刺激→気管支炎・気管粘膜の化生。Grade I-IV（25〜100%狭窄）。",
        "causes_ja": "先天性軟骨形成異常（グリコサミノグリカン欠乏）、肥満、慢性気道刺激。好発：ヨークシャーテリア、ポメラニアン、チワワ、トイプードル、マルチーズ。中高齢で臨床的に顕在化。",
        "prevention_ja": "肥満防止、首輪よりハーネスの使用、気管刺激の回避（煙・粉塵）、興奮の抑制、高温多湿環境の回避。",
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
        "pathophysiology_ja": "反回喉頭神経の変性→披裂軟骨の外転障害→声門の開大不全→吸気時の喉頭閉塞→吸気努力増大→吸気性喘鳴（stridor）→高体温・呼吸窮迫。多くは全身性多発神経障害（GOLPP: Geriatric Onset Laryngeal Paralysis Polyneuropathy）の一部として後肢の運動失調を伴う。熱中症・興奮時に急性呼吸窮迫のリスク。",
        "causes_ja": "特発性/GOLPP（最多、高齢大型犬の加齢性多発神経障害）、甲状腺機能低下症関連（稀だが精査すべき）、外傷性（頸部手術後）、先天性（ブービエ・デ・フランダース、ダルメシアン子犬）。好発：ラブラドール、ゴールデン、セントバーナード、アイリッシュセッター。10歳以上に多い。",
        "prevention_ja": "確実な予防法はない。甲状腺機能低下症の適切な管理。罹患犬の高温環境・興奮の回避、ハーネスの使用。重症例は片側披裂軟骨側方化術（tie-back手術）で呼吸改善。",
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
        "pathophysiology_ja": "病原体の気道侵入→肺胞マクロファージの防御突破→肺胞内の炎症性滲出液貯留→ガス交換障害→低酸素血症。細菌性が最多：Bordetella, Pasteurella, Streptococcus, E. coli。ウイルス性（CDV, CAV-2, CIV）は細菌二次感染を招きやすい。",
        "causes_ja": "細菌性（最多）：免疫抑制・誤嚥・上気道感染後。ウイルス性（CDV, インフルエンザ）。真菌性（Blastomyces, Histoplasma：米国流行地域）。寄生虫性（肺虫、条虫幼虫移行）。好発：若齢犬、免疫抑制犬、短頭種。",
        "prevention_ja": "コアワクチンの適切な接種、ケンネルコフワクチン（集団飼育犬）、誤嚥リスクの管理（巨大食道症の管理）、免疫抑制状態の早期治療。",
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
        "pathophysiology_ja": "異物（胃内容物・食物・液体）の気管支・肺胞への吸引→胃酸による化学性肺障害（Mendelson症候群）→肺胞上皮・毛細血管損傷→二次細菌感染（嫌気性菌含む）→壊死性肺炎・肺膿瘍。右中葉・右前葉に好発（気管支角度の関係）。",
        "causes_ja": "巨大食道症（最多の基礎疾患）、全身麻酔後の嘔吐、喉頭麻痺、重症筋無力症、強制経口投薬時の誤嚥、意識障害時の嘔吐。短頭種は解剖学的にリスク高。",
        "prevention_ja": "巨大食道症犬の立位給餌（Bailey chair）、麻酔前の適切な絶食、経口投薬時の慎重な投与、嘔吐犬の頭部挙上。",
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
        "pathophysiology_ja": "肺動脈圧の上昇（収縮期>30mmHg）→右心室の圧負荷→右室肥大→右心不全→三尖弁逆流・腹水・頸静脈怒張。原因分類：(1)動脈性PH（特発性、フィラリア症）、(2)左心疾患性（MMVD・DCMの肺うっ血に続発）、(3)呼吸器疾患性（慢性気管支炎・肺線維症）、(4)血栓塞栓性。失神・チアノーゼは重症の徴候。",
        "causes_ja": "左心疾患（MMVD/DCMに続発、最多）、慢性呼吸器疾患（気管虚脱・慢性気管支炎・肺線維症）、フィラリア症、肺血栓塞栓症、先天性心疾患（Eisenmenger症候群）。特発性は犬では稀。WHWT（肺線維症関連）に好発。",
        "prevention_ja": "基礎疾患の早期管理（左心疾患・フィラリア予防・慢性呼吸器疾患）。心エコー（三尖弁逆流速度）でスクリーニング。シルデナフィル（PDE5阻害剤）が主要な治療薬。",
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
        "pathophysiology_ja": "フォンウィルブランド因子（vWF）の量的/質的異常→一次止血（血小板粘着・凝集）の障害→粘膜出血傾向（鼻出血・歯肉出血・消化管出血・尿路出血・発情期出血遷延）。3型に分類：Type 1（vWF量の低下、最多・軽度）、Type 2（vWF多量体の異常、中等度）、Type 3（vWF完全欠損、重度・致死的出血のリスク）。術前・外傷後に初めて診断されることが多い。",
        "causes_ja": "常染色体遺伝。Type 1：ドーベルマン（最多、約70%がキャリアまたは罹患）、コーギー、シェルティ、ゴールデン。Type 2：ジャーマンワイヤーヘアードポインター。Type 3：スコティッシュテリア、シェルティ、チェサピークベイレトリーバー。遺伝子検査が可能。",
        "prevention_ja": "好発犬種のvWF遺伝子検査による繁殖管理、罹患犬の術前にvWF活性測定・デスモプレシン（DDAVP）前投与、止血に影響する薬剤（NSAIDs・アスピリン）の回避。",
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
        "pathophysiology_ja": "網膜視細胞（桿体→錐体の順）の進行性変性・消失→暗所視障害（夜盲）→明所視も障害→完全失明。早発型（rod-cone dysplasia：生後数ヶ月で発症）と遅発型（progressive rod-cone degeneration：3〜5歳で発症）に大別。ERG（網膜電図）で早期診断可能。二次性白内障の合併が高率。",
        "causes_ja": "常染色体劣性遺伝が多い。品種ごとに異なる遺伝子変異：PRCD（プードル・コッカースパニエル・ラブラドール）、PDE6B（アイリッシュセッター）、CNGB1（パピヨン）等。50以上の犬種で報告。遺伝子検査パネルが市販（OptiGen・Embark等）。",
        "prevention_ja": "繁殖前のDNA検査（品種別のPRA遺伝子パネル）による繁殖管理が最も有効。キャリア同士の交配回避。定期的な眼科検診（CERF/OFA）。治療法はないが、犬は他の感覚で適応し、環境の一貫性を保つことでQOLを維持できる。",
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
        "pathophysiology_ja": "水晶体線維のタンパク質（クリスタリン）の変性・凝集→水晶体の透明性喪失→光の散乱→視力低下。糖尿病性：ソルビトール蓄積→浸透圧性水晶体膨化→急速な成熟。遺伝性：品種特異的な水晶体蛋白異常。成熟白内障では水晶体誘発性ぶどう膜炎のリスク。",
        "causes_ja": "遺伝性（最多）、糖尿病性（75%が発症1年以内に白内障進行）、老齢性、外傷性、ぶどう膜炎後、PRA続発性。好発犬種：コッカースパニエル、プードル、ビションフリーゼ、ミニチュアシュナウザー。",
        "prevention_ja": "糖尿病の早期管理（血糖コントロール）、好発犬種の定期眼科検診、遺伝子検査（HSF4等）による繁殖管理。ALR2阻害剤（キジン酸）の研究中。",
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
        "description_ja": "膝蓋骨が滑車溝から内側（MPL、小型犬に多い）または外側（LPL、大型犬に多い）に脱臼する疾患。"
                          "小型犬で最も多い整形外科疾患の一つ。チワワ、ポメラニアン、トイプードル、"
                          "ヨークシャーテリア、マルチーズに好発。Grade 1〜4に分類。",
        "pathophysiology_ja": "大腿骨滑車溝の浅小化→膝蓋骨の不安定性→脱臼の反復。"
                              "脱臼に伴い大腿四頭筋のアライメント異常→脛骨内旋→"
                              "さらなる脱臼の促進と関節軟骨の摩耗→二次性変形性関節症。"
                              "Grade 3〜4では恒常的脱臼→持続的跛行・骨変形。前十字靭帯断裂の併発リスクも高い。",
        "causes_ja": "先天性・発達性（多因子遺伝、最多）。稀に外傷性。"
                     "内側脱臼（MPL）が小型犬の90%を占め、両側性が50%。"
                     "外側脱臼（LPL）は大型犬に多い。",
        "treatment_ja": "Grade 1：保存療法（体重管理、関節サプリメント、適度な運動）で経過観察。"
                        "Grade 2〜4：外科矯正が推奨。術式：滑車溝形成術（溝深化術）＋"
                        "内側関節包縫縮＋脛骨粗面転位術の組み合わせ。"
                        "重度の骨変形：矯正骨切り術。術後リハビリテーション6〜8週間。",
        "prognosis_ja": "Grade 1〜2の外科矯正：成功率90%以上、長期予後良好。"
                        "Grade 3〜4：外科矯正で機能改善するが再脱臼率は10〜15%。"
                        "前十字靭帯断裂の併発例ではTPLO等の追加手術が必要。",
        "prevention_ja": "罹患犬の繁殖制限。体重管理。成長期の過度なジャンプ・滑りやすい床面を避ける。",
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
        "pathophysiology_ja": "僧帽弁尖の粘液腫様変性→弁の肥厚・伸長→弁尖の逸脱・腱索断裂→僧帽弁逆流（MR）→左房拡大→肺静脈うっ血→肺水腫。左房拡大→左主気管支圧排→咳嗽。心房細動の合併。ACVIM Stage A〜D分類。",
        "causes_ja": "加齢性弁変性（最多）。病因不明だが遺伝的要因が示唆。好発：CKCS（若齢発症）、マルチーズ、ダックスフンド、チワワ、ポメラニアン等の小型犬。全犬の75%が心不全の原因。",
        "prevention_ja": "確実な予防法はないが、CKCSの繁殖プロトコル（心臓聴診・心エコースクリーニング）、定期的な心臓聴診（年1回以上）で早期発見。肥満予防。",
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
        "symptoms": {"straining_urinate", "blood_urine", "pain_on_touch",
                      "excessive_urination"},
        "description": "A hereditary condition causing cystine stones in the "
                       "urinary tract, common in certain breeds.",
        "description_ja": "腎尿細管でのシスチン再吸収障害による遺伝性疾患。"
                          "尿中シスチン濃度上昇→シスチン結石形成。"
                          "ニューファンドランド、イングリッシュブルドッグ、ダックスフンド、"
                          "マスティフ、バセットハウンドに好発。雄に多い。",
        "pathophysiology_ja": "腎近位尿細管のアミノ酸トランスポーター（SLC3A1/SLC7A9）の遺伝子変異→"
                              "シスチン再吸収障害→尿中シスチン過排泄→酸性尿中でシスチン結晶化→結石形成。"
                              "シスチンは全アミノ酸中で最も溶解度が低い。",
        "causes_ja": "常染色体劣性遺伝（Type I：ニューファンドランド等）、"
                     "常染色体優性遺伝（Type II-A/B：ミニチュアピンシャー等）。"
                     "SLC3A1またはSLC7A9遺伝子変異が原因。",
        "treatment_ja": "尿アルカリ化（クエン酸カリウム 75mg/kg BID）→シスチン溶解度上昇。"
                        "チオプロニン（2-MPG、15〜20mg/kg BID）→シスチンをより可溶性の化合物に変換。"
                        "低タンパク食＋十分な飲水。大結石は外科的摘出（膀胱切開術）。"
                        "尿道閉塞時は緊急カテーテル処置。",
        "prognosis_ja": "生涯にわたる管理が必要。チオプロニン投与で再発率を大幅に低減可能。"
                        "遺伝子検査で繁殖管理が推奨される。",
        "prevention_ja": "遺伝子検査による繁殖管理。低タンパク食、十分な飲水、尿アルカリ化。"
                         "定期的な尿検査・画像検査でモニタリング。",
        "urgency": "normal",
    },
    # ---- Tumors / Oncology ----
    {
        "name": "Hemangiosarcoma",
        "name_ja": "血管肉腫（HSA）",
        "symptoms": {"lethargy", "bloated_abdomen", "weight_loss",
                      "appetite_loss", "rapid_breathing"},
        "description": "An aggressive malignant tumor of blood vessel walls, "
                       "most common in the spleen and heart. Often presents "
                       "with sudden internal bleeding.",
        "description_ja": "血管内皮由来の高悪性度肉腫。脾臓（最多）、右心房、肝臓、皮下に好発。"
                          "ジャーマンシェパード、ゴールデンレトリバー、ラブラドールの中高齢犬に多い。"
                          "脾臓HSAの50%以上は腫瘍破裂による急性腹腔内出血で発見される。",
        "pathophysiology_ja": "血管内皮細胞の悪性形質転換→血管腔を形成する腫瘍増殖→脆弱な腫瘍血管の破裂→"
                              "大量内出血（血腹、心タンポナーデ）。高い転移率（診断時にはほぼ転移あり）。"
                              "DICの併発が多い。右心房HSAでは心タンポナーデ→心原性ショック。",
        "causes_ja": "明確な原因は不明。遺伝的素因（犬種好発性）、慢性的な抗原刺激、"
                     "紫外線暴露（皮膚型HSA）が示唆されている。",
        "treatment_ja": "脾臓HSA：緊急脾摘→術後化学療法（ドキソルビシンベース、5〜6サイクル）。"
                        "心臓HSA：心膜穿刺（緊急）→心膜切除±化学療法。"
                        "化学療法：ドキソルビシン(30mg/m² IV q3w)±シクロフォスファミド or ビンクリスチン。"
                        "メトロノミック化学療法も報告あり。出血ショック時は輸血＋大量輸液。",
        "prognosis_ja": "予後不良。脾摘のみ：中央生存期間1〜3ヶ月。脾摘＋化学療法：中央生存期間4〜6ヶ月。"
                        "1年生存率10〜20%。皮膚型（真皮限局）のみ手術で根治の可能性あり。",
        "prevention_ja": "確立された予防法なし。好発品種の中高齢犬では腹部超音波検査の定期実施が推奨。",
        "urgency": "emergency",
    },
    {
        "name": "Lymphoma",
        "name_ja": "リンパ腫",
        "symptoms": {"lumps", "weight_loss", "lethargy", "appetite_loss",
                      "excessive_thirst"},
        "description": "A common cancer of the lymphatic system, presenting "
                       "as enlarged lymph nodes throughout the body.",
        "description_ja": "リンパ球由来の悪性腫瘍で犬の腫瘍の中で最も多い疾患の一つ。"
                          "多中心型（全身リンパ節腫大、80%）が最多。ゴールデンレトリバー、"
                          "ボクサー、バーニーズマウンテンドッグに好発。中高齢犬（6〜9歳）に多い。",
        "pathophysiology_ja": "リンパ球（主にB細胞またはT細胞）のクローナルな悪性増殖。"
                              "多中心型：全身のリンパ節に浸潤→無痛性のリンパ節腫大（顎下、前肩甲、膝窩等）。"
                              "消化器型：腸管浸潤→吸収障害・下痢。縦隔型：前縦隔リンパ節→呼吸困難。"
                              "WHO分類でStage I〜Vに病期分類。サブステージa（無症候性）vs b（症候性）。",
        "causes_ja": "明確な原因は不明。遺伝的素因、免疫抑制、環境因子（除草剤2,4-D暴露との疫学的関連報告）。"
                     "T細胞型はB細胞型より予後不良。",
        "treatment_ja": "多剤併用化学療法が標準：CHOPプロトコール（シクロフォスファミド、ドキソルビシン、"
                        "ビンクリスチン、プレドニゾロン）19〜25週。寛解率80〜90%。"
                        "単剤プレドニゾロン：化学療法非実施の場合（中央生存期間1〜2ヶ月）。"
                        "再発時：レスキュープロトコール（CCNU、ラバムスチン等）。"
                        "消化器型：外科切除±化学療法。",
        "prognosis_ja": "CHOP化学療法：第1寛解の中央生存期間12〜14ヶ月。1年生存率50%、2年生存率20%。"
                        "B細胞型はT細胞型より予後良好。Stage a（無症候性）はbより予後良好。"
                        "無治療の場合：中央生存期間4〜6週間。",
        "prevention_ja": "確立された予防法なし。好発品種での定期的なリンパ節触診。",
        "urgency": "normal",
    },
    {
        "name": "Osteosarcoma",
        "name_ja": "骨肉腫（OSA）",
        "symptoms": {*_ANY_LIMPING, "swollen_joints",
                      "pain_on_touch", "reluctance_move"},
        "description": "An aggressive bone cancer primarily affecting large "
                       "and giant breed dogs, usually in the limbs.",
        "description_ja": "犬の骨原発性悪性腫瘍の85%を占める。大型〜超大型犬（体重>40kg）の中高齢犬に好発。"
                          "前肢の橈骨遠位端と上腕骨近位端（away from the elbow）に好発。"
                          "グレートデン、セントバーナード、アイリッシュウルフハウンド、ロットワイラーに多い。",
        "pathophysiology_ja": "骨芽細胞由来の悪性腫瘍→骨破壊性と骨増殖性の混合病変→病的骨折。"
                              "診断時に90%以上の症例で微小転移（主に肺）が存在。"
                              "腫瘍による骨膜挙上→激しい疼痛。アルカリフォスファターゼ（ALP）高値は予後不良因子。",
        "causes_ja": "明確な原因は不明。大型犬の急速な骨成長、骨内固定材の存在、慢性骨炎、"
                     "放射線照射後が報告されている。遺伝的素因あり。",
        "treatment_ja": "標準治療：患肢切断＋術後化学療法（カルボプラチン30mg/m² IV q3w×4〜6回、"
                        "またはドキソルビシン＋カルボプラチン交互投与）。"
                        "四肢温存手術（limb-sparing surgery）：切断を望まない場合。"
                        "疼痛管理：NSAIDs、ガバペンチン、トラマドール、ビスフォスフォネート。"
                        "緩和的放射線療法（疼痛緩和、切断非実施の場合）。",
        "prognosis_ja": "切断のみ：中央生存期間4〜5ヶ月。切断＋化学療法：中央生存期間10〜12ヶ月。"
                        "2年生存率15〜20%。ALP正常値の方が予後良好。"
                        "無治療：激しい疼痛により早期安楽死が多い。",
        "prevention_ja": "確立された予防法なし。大型犬種の跛行が持続する場合はX線検査での早期発見。",
        "urgency": "urgent",
    },
    {
        "name": "Mast Cell Tumor",
        "name_ja": "肥満細胞腫（MCT）",
        "symptoms": {"lumps", "itching", "vomiting", "lethargy",
                      "appetite_loss"},
        "description": "The most common malignant skin tumor in dogs, "
                       "varying from benign to highly aggressive forms.",
        "description_ja": "犬の皮膚腫瘍で最も多い悪性腫瘍（全皮膚腫瘍の16〜21%）。"
                          "Patnaik分類（Grade I〜III）またはKiupel分類（低悪性度/高悪性度）で組織学的に分類。"
                          "ボクサー、パグ、ボストンテリア、ラブラドール、ゴールデンレトリバーに好発。",
        "pathophysiology_ja": "肥満細胞（マスト細胞）の腫瘍性増殖。顆粒内にヒスタミン、ヘパリン、"
                              "プロテアーゼ等のメディエーターを含有→脱顆粒により局所の紅斑・浮腫（Darier徴候）、"
                              "全身性ヒスタミン放出（消化管潰瘍、低血圧、アナフィラキシー様反応）。"
                              "c-KIT変異がある場合、チロシンキナーゼ阻害薬の標的となる。",
        "causes_ja": "明確な原因は不明。c-KIT遺伝子変異（特に内部タンデム重複、ITD）が約30%で検出。"
                     "遺伝的素因（犬種好発性）。慢性炎症との関連も示唆。",
        "treatment_ja": "低悪性度（Kiupel Low grade）：外科切除（2cmマージン＋深部筋膜一層）が第一選択。"
                        "マージン不十分：追加切除または放射線療法。"
                        "高悪性度/転移陽性：外科＋補助化学療法（ビンブラスチン＋プレドニゾロン）。"
                        "チロシンキナーゼ阻害薬：トセラニブ（パラディア）—c-KIT変異陽性例や切除不能例に有効。"
                        "H1/H2ブロッカー（ジフェンヒドラミン＋ファモチジン）で脱顆粒症状管理。",
        "prognosis_ja": "Low grade：完全切除で中央生存期間>2年、多くは根治可能。"
                        "High grade：中央生存期間4〜6ヶ月（治療下）。転移率高い。"
                        "c-KIT変異陽性例はTKI治療に反応良好。",
        "prevention_ja": "確立された予防法なし。皮膚のしこりを発見したら早期にFNA（細胞診）で評価。"
                         "MCTは細胞診での診断精度が高い（90%以上）。",
        "urgency": "normal",
    },
    {
        "name": "Melanoma",
        "name_ja": "メラノーマ（黒色腫）",
        "symptoms": {"lumps", "weight_loss", "appetite_loss"},
        "description": "A tumor of melanocyte cells, most aggressive when "
                       "found in the mouth. Common in senior dogs.",
        "description_ja": "メラノサイト由来の腫瘍で、口腔内発生時に最も悪性度が高いです。",
        "pathophysiology_ja": "メラノサイトの腫瘍性増殖。発生部位により生物学的挙動が大きく異なる：(1)口腔：最も悪性（転移率80%以上、肺・リンパ節転移）、(2)皮膚（有毛部）：多くは良性、完全切除で治癒、(3)爪床/趾：中〜高悪性度、骨浸潤あり、(4)眼内：中等度悪性。メラニン欠乏型（無色素性）は組織学的に見逃されやすく注意が必要。",
        "causes_ja": "原因不明。好発犬種（口腔）：コッカースパニエル、スコティッシュテリア、ゴールデン、ミニチュアプードル。爪床：黒色被毛の犬種に多い。皮膚：全犬種。中高齢犬（9〜12歳）。口腔内の色素性腫瘤は全てメラノーマを疑い生検が必要。",
        "prevention_ja": "確実な予防法はない。口腔内・爪床・皮膚のしこり・色素性病変の早期受診。皮膚メラノーマは早期切除で予後良好。口腔メラノーマは広範囲切除＋メラノーマワクチン（Oncept）の併用を検討。",
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
        "pathophysiology_ja": "扁平上皮細胞の異型増殖→局所浸潤性腫瘤形成→骨破壊（爪床・口腔で顕著）。転移率は発生部位により異なる：皮膚（無色素部位のUV誘発型）は低転移率で予後良好、口腔SCCは扁桃原発が最も高転移率（>90%）、爪床SCCは中等度（黒色犬種に好発）。",
        "causes_ja": "皮膚：紫外線暴露（色素の薄い犬の腹部・鼻鏡：ダルメシアン、ブルテリア、ピットブル）。口腔：原因不明（扁桃SCCは都市部の犬に多い→大気汚染説あり）。爪床：大型犬の黒色犬種（ラブラドール、プードル、ジャイアントシュナウザー）。",
        "prevention_ja": "色素の薄い犬のUV暴露制限（日焼け止め使用、日中の屋外活動制限）。皮膚の非治癒性潰瘍・爪床の腫脹・口腔内腫瘤の早期生検。早期切除が治癒の鍵。",
        "urgency": "normal",
    },
    {
        "name": "Mammary Tumor",
        "name_ja": "乳腺腫瘍",
        "symptoms": {"lumps", "weight_loss", "appetite_loss"},
        "description": "Tumors of the mammary glands, common in unspayed "
                       "females. About 50% are malignant.",
        "description_ja": "乳腺の腫瘍で、未避妊の雌犬に多いです。約50%が悪性です。",
        "pathophysiology_ja": "エストロゲン・プロゲステロンの反復的刺激→乳腺上皮の過形成→良性/悪性腫瘍への進展。犬では約50%が悪性（腺癌が最多）。悪性腫瘍はリンパ行性・血行性に転移（肺転移が最多）。第4・5乳腺に好発。",
        "causes_ja": "ホルモン依存性。初回発情前の避妊でリスク0.5%、1回後8%、2回後26%。未避妊犬の発症率は約25%。肥満（若齢期）、外因性プロゲステロン投与もリスク因子。スパニエル・プードル・ダックスフンドに好発。",
        "prevention_ja": "早期避妊手術（初回発情前が最も有効）。定期的な乳腺触診（特に中高齢の未避妊/遅期避妊犬）。プロゲステロン製剤の回避。",
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
        "pathophysiology_ja": "膀胱移行上皮の悪性増殖→膀胱壁への浸潤→膀胱三角部に好発（尿管口を巻き込みやすい）→水腎症・腎後性腎不全。局所リンパ節・肺への転移あり。犬の膀胱腫瘍の>90%がTCC/尿路上皮癌。尿中のVEGFやBRAF V595E変異（犬のTCCの約80%で検出）が早期診断マーカーとして注目。",
        "causes_ja": "環境因子（除草剤・殺虫剤曝露、特にフェノキシ酢酸系）、遺伝的素因。好発犬種：スコティッシュテリア（リスク18倍）、シェルティ、ビーグル、WHWT、ワイヤーヘアードフォックステリア。雌犬・肥満犬に多い。中高齢犬。",
        "prevention_ja": "除草剤・殺虫剤への曝露制限（散歩後の足の洗浄、散布直後の芝生回避）、好発犬種のスクリーニング（尿検査・BRAF変異検出・膀胱超音波）。NSAIDs（ピロキシカム・メロキシカム）が腫瘍増殖抑制に有効。",
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
        "pathophysiology_ja": "抗血小板自己抗体（IgG）→血小板表面への結合→脾臓マクロファージによる貪食・破壊→血小板数の急速な低下（<50,000/μL）→点状出血・斑状出血・粘膜出血。重症（<10,000/μL）では消化管出血・血尿・致死的出血のリスク。IMHA（免疫介在性溶血性貧血）との併発（Evans症候群）は予後不良。",
        "causes_ja": "一次性（特発性、最多）：自己免疫性。二次性：腫瘍（リンパ腫・血管肉腫）、感染症（Ehrlichia・Babesia・Leishmania）、薬剤性、ワクチン後。コッカースパニエル、プードル、オールドイングリッシュシープドッグに好発。中年雌犬に多い。",
        "prevention_ja": "確実な予防法はない。基礎疾患（感染症・腫瘍）の管理。点状出血・粘膜出血・鼻出血の早期受診。ワクチン接種後は一過性の血小板減少に注意。",
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
        "pathophysiology_ja": "歯垢（細菌バイオフィルム）の蓄積→歯肉溝への嫌気性菌侵入（Porphyromonas, Prevotella等）→歯肉炎（Stage 1）→歯周靭帯・歯槽骨の破壊（Stage 2-4）→歯の動揺・脱落。菌血症により心臓・肝臓・腎臓への転移性感染のリスク。3歳以上の犬の80%以上が罹患。",
        "causes_ja": "歯垢・歯石の蓄積が主因。リスク因子：小型犬（歯の過密）、短頭種、歯磨き不足、軟質食、加齢、免疫抑制。好発犬種：ダックスフンド、ヨークシャーテリア、チワワ、トイプードル。",
        "prevention_ja": "毎日の歯磨き（犬用酵素歯磨き粉）、歯科用ガム・デンタルチュー（VOHC認定製品推奨）、年1回の麻酔下歯科スケーリング、歯科用処方食。",
        "prognosis_ja": "Stage 1-2は適切な歯科処置で管理可能。Stage 3-4は抜歯が必要だが術後のQOLは良好。無治療では疼痛・菌血症による全身合併症のリスク。",
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
        "pathophysiology_ja": "歯周病・歯の破折→歯髄腔への細菌侵入→歯髄壊死→根尖周囲膿瘍形成→骨溶解→顔面瘻管（上顎第4前臼歯では眼窩下瘻管として眼下部から排膿）。上顎犬歯の根尖膿瘍は鼻腔と交通し鼻汁を呈することがある。",
        "causes_ja": "歯周病の進行、歯の破折（硬い物の咀嚼）、エナメル質の欠損。上顎第4前臼歯（裂肉歯）に最多。嫌気性菌を含む混合感染。",
        "prevention_ja": "定期的な歯科ケア（歯磨き・スケーリング）、硬すぎる咀嚼物（蹄・角・骨）の回避、歯の破折の早期治療。",
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
        "pathophysiology_ja": "膵臓β細胞の腫瘍性増殖→インスリンの自律的過剰分泌→低血糖（BG<60mg/dL）→脳のグルコース欠乏→脱力・運動失調・けいれん・昏迷。低血糖時にインスリン値が高値（修正インスリン:グルコース比>30が疑い）。約50%が悪性で肝臓・リンパ節への転移あり。",
        "causes_ja": "膵β細胞の腫瘍性増殖（機能性膵島細胞腫瘍）。中高齢犬（8〜12歳）に好発。大型犬：ジャーマンシェパード、アイリッシュセッター、ラブラドール。低血糖発作は空腹時・運動後に誘発されやすい（Whippleの三徴）。",
        "prevention_ja": "確実な予防法はない。空腹時低血糖エピソード（ぼんやり・ふらつき・けいれん）の早期受診。食事は少量頻回（1日4〜6回、低炭水化物・高蛋白・高脂肪食）で低血糖を最小化。",
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
        "pathophysiology_ja": "感染動物の咬傷→唾液中のリッサウイルスが末梢神経に侵入→軸索内を逆行性に中枢神経へ伝播（1〜3ヶ月の潜伏期間）→脳幹・大脳辺縁系の神経細胞壊死→狂躁型（攻撃性・興奮・水恐怖）または麻痺型（進行性麻痺）→脳幹機能不全→呼吸停止→死亡。発症後の致死率はほぼ100%。ネグリ小体（神経細胞内封入体）が病理学的特徴。",
        "causes_ja": "狂犬病ウイルス（Lyssavirus属）。感染動物（犬・コウモリ・アライグマ・キツネ・スカンク）の咬傷。日本は1957年以降清浄国（島嶼国の利点）だが、世界では年間約59,000人が死亡（WHO）。東南アジア・アフリカで高リスク。日本では狂犬病予防法により年1回のワクチン接種が義務。",
        "prevention_ja": "法定ワクチン接種（日本：狂犬病予防法に基づく年1回接種の義務）、海外渡航犬の事前ワクチン接種・抗体価確認、野生動物との接触回避。日本入国時は180日前までにワクチン接種・抗体価検査が必要。",
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
        "pathophysiology_ja": "犬パピローマウイルス（CPV-1等）の粘膜感染→上皮基底細胞での増殖→乳頭状の良性腫瘤形成。免疫成熟後（1〜5ヶ月）に自然退縮する自己限定性疾患。免疫抑制犬では持続・悪性化（SCC）のリスクあり。",
        "causes_ja": "犬パピローマウイルス（CPV-1が最多）。感染犬との直接接触または汚染物（玩具・食器）経由。潜伏期間1〜2ヶ月。免疫未成熟な若齢犬（<2歳）に好発。",
        "prevention_ja": "感染犬との接触制限（多頭飼育環境・ドッグパーク）、免疫抑制犬の感染環境回避。通常自然治癒するため過度な心配は不要。",
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
        "pathophysiology_ja": "経口感染→L2幼虫が腸管壁穿通→肝臓→肺（咳嗽の原因）→嚥下→小腸で成虫化。体内移行型（成犬では組織内休眠幼虫として存在）。大量感染→腸閉塞・腸穿孔のリスク。経胎盤感染で新生子犬に先天性感染。人獣共通（幼虫移行症）。",
        "causes_ja": "Toxocara canis。経胎盤・経乳・糞口感染。虫卵は環境中で数年生存。子犬は出生時に既に感染していることが多い。人への感染（内臓/眼幼虫移行症）のリスクあり。",
        "prevention_ja": "子犬は2週齢から2週間隔で8週齢まで駆虫、その後月1回の広域駆虫薬。妊娠犬のフェンベンダゾール投与（分娩前40日〜分娩後14日）。環境の糞便除去。",
        "urgency": "normal",
    },
    {
        "name": "Hookworm Infection",
        "name_ja": "鉤虫症",
        "symptoms": {"diarrhea", "bloody_stool", "weight_loss", "lethargy"},
        "description": "Blood-sucking intestinal parasites causing anemia, especially dangerous in puppies.",
        "description_ja": "吸血性の腸管寄生虫で、特に子犬では貧血を引き起こし危険です。",
        "pathophysiology_ja": "Ancylostoma caninumのL3幼虫が経口・経皮・経乳感染→小腸粘膜に咬着→吸血（成虫1匹あたり0.1mL/日）→鉄欠乏性貧血・低蛋白血症。大量感染の子犬では急性出血性貧血で致死的。経皮感染時は皮膚の足底皮膚炎。",
        "causes_ja": "Ancylostoma caninum（最多）、A. braziliense、Uncinaria stenocephala。糞口感染・経皮感染・経胎盤/経乳感染。温暖湿潤環境で幼虫が生存。子犬・屋外飼育犬にリスク高。",
        "prevention_ja": "月1回のマクロサイクリックラクトン系駆虫薬（イベルメクチン・ミルベマイシン等）、子犬は2週齢から2週間隔で駆虫開始、環境の糞便除去、妊娠犬の駆虫。",
        "urgency": "normal",
    },
    {
        "name": "Whipworm Infection (Trichuris)",
        "name_ja": "鞭虫症",
        "symptoms": {"diarrhea", "bloody_stool", "weight_loss"},
        "description": "Large intestine parasite causing chronic bloody diarrhea and weight loss.",
        "description_ja": "大腸に寄生し、慢性の血便と体重減少を引き起こします。",
        "pathophysiology_ja": "Trichuris vulpisの虫卵経口摂取→盲腸・結腸で幼虫が粘膜に穿入→成虫が頭部を粘膜に埋没させ吸血→大腸粘膜の炎症・出血→粘血便。大量感染時はアジソン病様の電解質異常（低Na・高K）を呈する偽アジソン症候群。",
        "causes_ja": "Trichuris vulpis。糞口感染。虫卵は環境中で極めて抵抗性が高く数年間生存。都市部の公園や庭に汚染が残存。感染力量型（prepatent period 3ヶ月と長い）。",
        "prevention_ja": "月1回のフェンベンダゾール含有駆虫薬（ミルベマイシン・モキシデクチンは鞭虫に有効）、環境の糞便除去、定期的な糞便検査（浮遊法）。",
        "urgency": "normal",
    },
    {
        "name": "Tapeworm Infection (Dipylidium/Echinococcus)",
        "name_ja": "条虫症（瓜実条虫・エキノコックス）",
        "symptoms": {"weight_loss", "diarrhea", "appetite_increase"},
        "description": "Intestinal tapeworms transmitted by fleas or contaminated prey. Echinococcus is a serious zoonotic risk.",
        "description_ja": "ノミや汚染獲物から感染する条虫で、エキノコックスは重大な人獣共通感染リスクがあります。",
        "pathophysiology_ja": "Dipylidium：ノミ（中間宿主）を経口摂取→小腸で成虫化→片節が肛門から排出。Echinococcus multilocularis：げっ歯類捕食→犬の小腸で成虫化→糞便中に虫卵排出（人への感染源）。犬では無症状〜軽度の消化器症状。",
        "causes_ja": "Dipylidium caninum（最多）：ノミ経由。Taenia属：生肉経由。Echinococcus multilocularis：北海道で重要（人獣共通感染症）。Echinococcus granulosus：世界的分布。",
        "prevention_ja": "ノミの徹底駆除（Dipylidium予防）、プラジカンテル含有駆虫薬の定期投与、生肉の非給餌、北海道ではエキノコックス定期検診。",
        "urgency": "normal",
    },
    {
        "name": "Ear Mite Infestation (Otodectes)",
        "name_ja": "耳ダニ感染症（ミミヒゼンダニ）",
        "symptoms": {"ear_scratching", "ear_odor", "head_tilting"},
        "description": "Highly contagious ear parasites causing intense itching and dark discharge, common in puppies.",
        "description_ja": "子犬に多い高伝染性の耳寄生虫で、激しい痒みと暗色分泌物を引き起こします。",
        "pathophysiology_ja": "Otodectes cynotisが外耳道内で増殖→耳道上皮の刺激→暗褐色のコーヒー粕様分泌物（ダニの糞・耳垢・炎症産物）→掻痒→自傷（耳介血腫のリスク）。重症例では鼓膜穿孔→中耳炎。過敏反応で掻痒が増幅。",
        "causes_ja": "Otodectes cynotis。感染動物との直接接触で伝播（高伝染性）。猫からの感染も多い。子犬・多頭飼育環境・ブリーダー犬舎に好発。",
        "prevention_ja": "イソキサゾリン系駆虫薬（フルララネル等）の通年投与、新規導入犬の検査、感染犬の隔離・同居動物全頭の同時治療。",
        "urgency": "normal",
    },
    {
        "name": "Flea Allergy Dermatitis",
        "name_ja": "ノミアレルギー性皮膚炎",
        "symptoms": {"itching", "hair_loss", "skin_redness", "hot_spots"},
        "description": "An allergic reaction to flea saliva causing intense itching, especially at the tail base.",
        "description_ja": "ノミ唾液に対するアレルギー反応で、特に尾根部に激しい痒みを引き起こします。",
        "pathophysiology_ja": "Ctenocephalides felis/canisの唾液中ハプテン（分子量15-40kDa）に対するI型（即時型）・IV型（遅延型）過敏反応→肥満細胞脱顆粒・ヒスタミン/ロイコトリエン放出→激しい掻痒→自傷性脱毛・二次感染。1匹のノミ刺咬でも発症可能。",
        "causes_ja": "ノミ（主にCtenocephalides felis）唾液中のアレルゲン蛋白に対する過敏反応。アトピー素因のある犬でリスク上昇。温暖湿潤気候で通年発症、温帯では夏〜秋に好発。",
        "prevention_ja": "通年のノミ駆除（イソキサゾリン系：フルララネル・アフォキソラネル、スピノサド等）、環境駆除（室内の吸引清掃・寝具洗濯・IGR処理）、同居動物全頭の駆虫。",
        "urgency": "normal",
    },
    {
        "name": "Sarcoptic Mange (Scabies)",
        "name_ja": "疥癬（ヒゼンダニ症）",
        "symptoms": {"itching", "hair_loss", "skin_redness", "dry_skin", "ear_scratching"},
        "description": "A highly contagious mite infestation causing intense itching and crusty skin. Zoonotic.",
        "description_ja": "激しい痒みと痂皮を引き起こす高伝染性のダニ感染症で、人にも感染します。",
        "pathophysiology_ja": "Sarcoptes scabiei var. canisが角質層に穿孔・産卵→I型＋IV型過敏反応→激烈な掻痒（ダニ数が少なくても強い）。耳介辺縁・肘・飛節・腹部に好発（pinnal-pedal reflex陽性が診断的）。人獣共通だが人体上では自己限定的。",
        "causes_ja": "Sarcoptes scabiei var. canis。感染犬との直接接触、環境中ダニ（数日生存）。野生動物（キツネ・タヌキ）からの感染あり。全犬種・全年齢。",
        "prevention_ja": "イソキサゾリン系駆虫薬の通年投与、感染犬の早期発見・隔離、野生動物との接触回避、同居動物全頭の同時治療。",
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
        "pathophysiology_ja": "下眼瞼の外方回転→結膜の露出→慢性結膜炎・角膜乾燥→粘液膿性分泌物。露出した結膜が異物・環境刺激に曝される→反復性結膜炎。重度では角膜障害のリスク。",
        "causes_ja": "先天性：顔面皮膚の過剰（大型犬種）。好発：セントバーナード、ブラッドハウンド、バセットハウンド、マスティフ、コッカースパニエル。後天性：外傷、眼窩脂肪萎縮、顔面神経麻痺。",
        "prevention_ja": "好発犬種の計画的繁殖。軽度は点眼管理、中等度以上はV字切除等の外科的矯正。",
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
        "symptoms": {"eye_discharge"},
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
        "pathophysiology_ja": "角膜実質への脂質（コレステロール・リン脂質・中性脂肪）またはミネラル（カルシウム）の異常沈着→角膜の透明性喪失。3型に分類：上皮性（稀）、実質性（最多、脂質沈着）、内皮性（角膜浮腫→水疱性角膜症）。実質性は通常視力に影響少。内皮性は進行性で視力低下あり。",
        "causes_ja": "遺伝性（常染色体劣性が多い）。実質性：シベリアンハスキー、ビーグル、シェルティに好発。内皮性：ボストンテリア、チワワ、ダックスフンドに好発。高脂血症に伴う脂質角膜症は鑑別が必要（後天性）。",
        "prevention_ja": "好発犬種の繁殖前眼科検査（CERF/OFA認定）、遺伝的キャリアの繁殖制限。後天性脂質角膜症は高脂血症の管理で予防。",
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
        "pathophysiology_ja": "交感神経の3ニューロン経路のいずれかの障害→患側眼への交感神経支配喪失→(1)縮瞳（miosis：散瞳筋の弛緩）、(2)眼瞼下垂（ptosis：ミュラー筋の弛緩）、(3)眼球陥凹（enophthalmos：眼窩平滑筋の弛緩）、(4)第三眼瞼突出（瞬膜の弛緩）。犬では節後性（中耳・内耳の病変）が最多。",
        "causes_ja": "特発性（犬で最多、約50%、自然寛解あり）。中耳炎/内耳炎（節後性）、胸腔腫瘍・頸部外傷（節前性）、脳幹病変（中枢性、稀）。ゴールデンレトリーバー・コッカースパニエルに報告多い。片側性が多い。原因検索（耳鏡検査・CT/MRI・胸部X線）が推奨。",
        "prevention_ja": "基礎疾患（中耳炎等）の早期治療。特発性は数週間〜数ヶ月で自然回復することが多い。フェニレフリン点眼による薬理学的局在診断が有用。",
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
        "pathophysiology_ja": "心房の電気的リモデリング→心房内の多数のリエントリー回路→心房の無秩序な電気活動→心房の有効な収縮喪失→不規則で通常は速い心室応答（HR 160〜250/min）→心拍出量低下→うっ血性心不全の悪化。基礎心疾患（DCM・MMVD・先天性心疾患）の合併がほぼ必発。大型犬では孤立性AFもあり。",
        "causes_ja": "DCM（最多の基礎疾患）、進行したMMVD、先天性心疾患、甲状腺機能亢進症（稀）。大型犬・超大型犬（心房が大きく維持しやすい）：アイリッシュウルフハウンド、グレートデーン、ニューファンドランド、ドーベルマン。小型犬では孤立性AFは極めて稀。",
        "prevention_ja": "確実な予防法はない。基礎心疾患の早期管理、定期的な心臓聴診・心電図。レート管理（ジルチアゼム・ジゴキシン）で心室応答を制御。",
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
        "pathophysiology_ja": "鼻腔内の上皮性/間葉性腫瘍→鼻腔の閉塞→一側性→両側性の鼻汁（粘液性→血性に進行）。篩骨板への浸潤→脳への直接浸潤→神経症状。顔面の骨破壊→顔面変形・眼球突出。犬の鼻腔腫瘍の約60%が腺癌、20%がSCC、10%が軟骨肉腫。遠隔転移率は低い（10〜20%）が局所浸潤性が高い。",
        "causes_ja": "原因不明。長頭種（コリー・シェルティ）は短頭種より高リスク（鼻腔粘膜面積が広い）。都市部の犬に多いとの報告（大気汚染の関与示唆）。受動喫煙との関連も指摘。中高齢犬（平均10歳）。一側性の慢性鼻汁が初発症状であることが多い。",
        "prevention_ja": "確実な予防法はない。一側性の慢性鼻汁・鼻出血は早期にCT→鼻腔内生検で精査。放射線療法（メガボルテージ）が標準治療（MST 12〜18ヶ月）。外科単独は効果不十分。",
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
        "pathophysiology_ja": "マダニ唾液中の神経毒素（ホロシクロトキシン等）→神経筋接合部でのアセチルコリン放出阻害→下位運動ニューロン型の弛緩性上行性麻痺。後肢から始まり前肢→呼吸筋に進行。ダニ除去後24〜72時間で回復。オーストラリアのIxodes holocyclusは特に毒性が強い。",
        "causes_ja": "Ixodes属（オーストラリアI. holocyclus、北米Dermacentor属）マダニの長期間の寄生（5〜7日以上の吸血）。雌成ダニが最も多くの毒素を産生。",
        "prevention_ja": "マダニ駆除薬（イソキサゾリン系）の通年投与、散歩後のマダニチェック、流行地域での注意。",
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
        "pathophysiology_ja": "原発性（髄膜腫・神経膠腫が最多）または転移性（血管肉腫・乳腺癌・肺癌から）→腫瘤効果→頭蓋内圧亢進→神経組織の圧迫・虚血→進行性神経症状。前頭葉：行動変化・旋回・けいれん。脳幹：前庭症状・意識障害。小脳：運動失調。けいれんが高齢犬で新規発症した場合は脳腫瘍を最も疑うべき。",
        "causes_ja": "原発性脳腫瘍（髄膜腫、星状膠細胞腫、乏突起膠細胞腫、脈絡叢腫瘍）。中高齢犬（>5歳）に好発。長頭種は髄膜腫に好発（コリー、ゴールデン）、短頭種は神経膠腫に好発（ボクサー、ブルドッグ、ボストンテリア）。",
        "prevention_ja": "確実な予防法はない。高齢犬の新規けいれんは緊急精査（MRI）。早期発見でQOL改善：外科的切除（髄膜腫で最も有効）、放射線療法、緩和ケア（抗けいれん薬・ステロイド）。",
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
        "pathophysiology_ja": "咀嚼筋に特異的な2M筋線維のミオシン結合蛋白に対する自己抗体→咀嚼筋（側頭筋・咬筋・翼状筋）の免疫介在性炎症→急性期：筋腫脹・疼痛・開口障害・摂食困難。慢性期：筋萎縮・線維化→恒常的開口制限。四肢の筋は2M線維を含まないため侵されない（咀嚼筋に限局）。",
        "causes_ja": "免疫介在性（2M線維ミオシン結合蛋白に対する自己抗体）。大型犬：ジャーマンシェパード、ラブラドール、ゴールデン、キャバリアに好発。若齢〜中齢犬に多い。血清抗2M抗体検査（UCSD）で確定診断。",
        "prevention_ja": "確実な予防法はない。急性期の早期免疫抑制療法（プレドニゾロン1〜2mg/kg/日、4〜6ヶ月の漸減）が線維化予防に重要。治療中止が早すぎると再発しやすい。",
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
        "pathophysiology_ja": "Malassezia pachydermatis（常在菌）の過剰増殖→酵母由来リパーゼによる皮脂分解→遊離脂肪酸が皮膚を刺激→掻痒・炎症→脂漏性皮膚炎。酵母抗原に対するI型・IV型過敏反応が痒みを増幅。皮膚皺部・耳道・指間に好発。",
        "causes_ja": "基礎疾患（アトピー性皮膚炎、甲状腺機能低下症、クッシング症候群、角化異常症）による皮膚微小環境の変化が過剰増殖を促進。多湿環境、過度の皮膚皺（シャーペイ、バセットハウンド等）。",
        "prevention_ja": "基礎疾患の管理、定期的な薬浴（ミコナゾール・クロルヘキシジン配合シャンプー週2回→維持期週1回）、耳の定期清掃、皮膚の乾燥維持。",
        "urgency": "normal",
    },
    {
        "name": "Systemic Lupus Erythematosus (SLE)",
        "name_ja": "全身性エリテマトーデス（SLE）",
        "symptoms": {"fever", "swollen_joints", "skin_redness", "lethargy", "appetite_loss"},
        "description": "A serious autoimmune disease affecting multiple organ systems including skin, joints, and kidneys.",
        "description_ja": "皮膚・関節・腎臓を含む多臓器を侵す重篤な自己免疫疾患です。",
        "pathophysiology_ja": "免疫寛容の破綻→抗核抗体（ANA）・抗dsDNA抗体等の多種自己抗体産生→免疫複合体の全身組織沈着→補体活性化→多臓器の炎症性障害：関節（多発性関節炎）、腎臓（糸球体腎炎→蛋白尿・腎不全）、皮膚（紅斑・潰瘍・脱毛）、血液（溶血性貧血・血小板減少症）。複数の臓器系が同時または逐次的に侵される。",
        "causes_ja": "原因不明の多因子性自己免疫疾患。遺伝的素因（MHCクラスII関連）、紫外線暴露、薬剤誘発性（sulfonamide等）。好発犬種：シェルティ、コリー、ジャーマンシェパード。中年犬に多い。ANA検査陽性が支持的だが確定的ではない。",
        "prevention_ja": "確実な予防法はない。SLE疑い犬種の繁殖管理。紫外線暴露の軽減。薬剤誘発性が疑われる場合は原因薬の中止。早期診断と免疫抑制療法の開始が臓器障害の予防に重要。",
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
        "pathophysiology_ja": "腸管粘膜のリンパ管・毛細血管からのアルブミン・グロブリン漏出→低アルブミン血症（<2.0g/dL）→膠質浸透圧低下→腹水・胸水・末梢浮腫。腸リンパ管拡張症（最多）、IBD、腸管リンパ腫が基礎疾患。低Ca血症（アルブミン結合Ca喪失）、低コレステロール血症、リンパ球減少を伴うことが多い。血栓塞栓症のリスク（アンチトロンビンIII喪失）。",
        "causes_ja": "腸リンパ管拡張症（最多、ヨークシャーテリアに好発）、IBD（リンパ球形質細胞性腸炎）、腸管リンパ腫。好発犬種：ヨークシャーテリア、ソフトコーテッドウィートンテリア、ノルウェージャンルンデフンド。確定診断には内視鏡生検が必要。",
        "prevention_ja": "確実な予防法はない。好発犬種の定期的な血液検査（アルブミン値）。低脂肪食が腸リンパ管拡張症の管理に有効。",
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
        "pathophysiology_ja": "肛門嚢の排泄管閉塞→分泌物の貯留（嵌頓）→細菌増殖→感染→膿瘍形成→肛門嚢の破裂・瘻管形成。慢性的な嵌頓→嚢壁の線維化→排泄困難の悪循環。軟便・低食物繊維食は自然排泄を妨げる。",
        "causes_ja": "分泌物の自然排泄障害（軟便・肥満・解剖学的要因）。アレルギー性皮膚炎の併発で肛門周囲の炎症がリスク。好発：小型犬（チワワ、トイプードル、ダックスフンド）、肥満犬。",
        "prevention_ja": "高食物繊維食で便の硬さを維持、適正体重の管理、必要時の定期的な肛門嚢圧迫（ただし過度の圧迫は炎症を誘発）。反復例では肛門嚢摘出術を検討。",
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
        "pathophysiology_ja": "副腎髄質クロマフィン細胞の腫瘍性増殖→カテコラミン（エピネフリン・ノルエピネフリン）の不規則な大量放出→発作的高血圧→頻脈・不整脈・振戦・不安・虚脱。持続性高血圧→網膜障害・心肥大・腎障害。約50%が悪性で後大静脈への浸潤・肝臓や肺への転移あり。副腎皮質腫瘍（クッシング）との鑑別が重要。",
        "causes_ja": "副腎髄質クロマフィン細胞の腫瘍性増殖。高齢犬（>10歳）に好発。特定の犬種素因は明確でない。副腎偶発腫として超音波で発見されることも多い。クッシング症候群との併存が20〜50%。",
        "prevention_ja": "確実な予防法はない。副腎腫瘤発見時のカテコラミン/メタネフリン測定による機能評価。手術時の高血圧クリーゼに対する麻酔管理が重要（フェノキシベンザミンによる術前α遮断）。",
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
        "pathophysiology_ja": "セルトリ細胞腫：エストロゲン産生→雌性化（女性化乳房・対側精巣萎縮・骨髄抑制→致死的汎血球減少症）。セミノーマ：精祖細胞由来、多くは良性。間質細胞腫：テストステロン産生。停留精巣（陰睾）は腫瘍化リスク13.6倍。",
        "causes_ja": "停留精巣が最大のリスク因子（特に腹腔内停留）。加齢（平均10歳）。セルトリ細胞腫・セミノーマは停留精巣に好発。未去勢の高齢犬。",
        "prevention_ja": "早期去勢手術（特に停留精巣犬は必須）、未去勢犬の精巣の定期触診。",
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
        "pathophysiology_ja": "母体性：子宮無力症（最多）、産道狭窄（骨盤骨折歴・品種的骨盤形態）。胎児性：過大胎児、胎位異常、水頭症。活動期の陣痛が30分以上持続しても児娩出がない場合、または緑色分泌物（胎盤剥離）後60分以内に出産がない場合は緊急。",
        "causes_ja": "短頭種（ブルドッグ・フレンチブルドッグ：胎児頭部と母体骨盤の不適合で帝王切開率80%以上）、小型犬の単胎妊娠（過大胎児）、高齢初産、肥満、子宮無力症。",
        "prevention_ja": "交配前のX線による骨盤評価、妊娠末期のX線で胎児数確認、短頭種での計画的帝王切開、栄養管理と適度な運動。",
        "urgency": "emergency",
    },
    # ---- Toxicology / Poisoning ----
    {
        "name": "Chocolate Toxicosis",
        "name_ja": "チョコレート中毒",
        "pathophysiology_ja": "テオブロミン・カフェイン（メチルキサンチン）の摂取→ホスホジエステラーゼ阻害・アデノシン受容体拮抗→心筋興奮性亢進（頻脈・不整脈）、CNS興奮（振戦・けいれん）、平滑筋弛緩（嘔吐・下痢）、腎血管拡張（多尿）。犬のテオブロミン半減期は17.5時間と長い。",
        "causes_ja": "カカオ含有製品の摂取。毒性量はテオブロミン20mg/kg（軽度）〜60mg/kg（重度）。ダークチョコ（130-450mg/oz）>ミルクチョコ（44-58mg/oz）>ホワイトチョコ（0.25mg/oz）。小型犬で板チョコ1枚が致死的になりうる。",
        "prevention_ja": "チョコレート製品への犬のアクセス遮断、家族（特に子供）への教育、バレンタイン・ハロウィン等のイベント時の特に注意。",
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
        "pathophysiology_ja": "毒性物質は酒石酸（tartaric acid）が有力候補（2021年ASPCA報告）。近位尿細管上皮の急性壊死→乏尿性急性腎障害（AKI）。摂取後2〜6時間で嘔吐開始、24〜72時間で腎不全進行。個体差が大きく、少量で致死例もある一方、大量摂取でも無症状の例あり。",
        "causes_ja": "ブドウ・レーズン・カレンツ・干しブドウの摂取。毒性量は不明確（最低3g/kgで報告、個体差極大）。レーズンは乾燥により毒素が濃縮され少量でも危険。品種・産地による差は不明。",
        "prevention_ja": "ブドウ・レーズン・カレンツ製品の完全な犬からの隔離、テーブルフードの禁止、レーズン入り菓子パン・シリアル等の注意。",
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
        "pathophysiology_ja": "COX-1/COX-2の非選択的阻害→胃粘膜保護プロスタグランジン減少→胃潰瘍・穿孔。腎臓：輸入細動脈のPG依存性拡張阻害→腎血流低下→急性腎障害。イブプロフェン>50mg/kgで腎障害、100mg/kgでCNS症状。ナプロキセンは犬で半減期72時間と長い。",
        "causes_ja": "ヒト用NSAIDの誤食（イブプロフェン、ナプロキセン、アスピリン）。犬用NSAIDの過量投与。イブプロフェンが最も多い。小型犬では1錠で中毒量に達しうる。",
        "prevention_ja": "ヒト用薬のペットからの隔離、犬用NSAIDの正確な用量投与、腎機能低下犬へのNSAID投与回避。",
        "urgency": "emergency",
    },
    {
        "name": "Rodenticide Poisoning",
        "name_ja": "殺鼠剤中毒",
        "symptoms": {"lethargy", "difficulty_breathing", "bloated_abdomen", "appetite_loss"},
        "description": "Anticoagulant rat poison causing internal bleeding, or bromethalin causing neurological signs.",
        "description_ja": "抗凝固性殺鼠剤による内出血、またはブロメタリンによる神経症状です。",
        "pathophysiology_ja": "抗凝固性（ワルファリン系）：ビタミンKエポキシド還元酵素阻害→凝固因子（II,VII,IX,X）枯渇→出血素因→体腔内出血・肺出血。摂取後2〜5日で症状発現。ブロメタリン：酸化的リン酸化の脱共役→脳浮腫→振戦・けいれん・麻痺。コレカルシフェロール：高Ca血症→腎石灰化。",
        "causes_ja": "殺鼠剤の誤食。第二世代抗凝固剤（ブロディファコウム・ブロマジオロン）は少量で致死的かつ半減期が長い。ブロメタリン：致死量2.5mg/kg。日本では主にワルファリン系が流通。",
        "prevention_ja": "殺鼠剤のペットアクセス不能な場所への設置、ベイトステーション使用、代替的な害獣駆除法の検討、使用場所の明確な記録。",
        "urgency": "emergency",
    },
    {
        "name": "Onion/Garlic Toxicosis",
        "name_ja": "タマネギ・ニンニク中毒（ネギ属中毒）",
        "symptoms": {"vomiting", "diarrhea", "lethargy", "rapid_breathing"},
        "description": "Heinz body anemia from allium family vegetables destroying red blood cells.",
        "description_ja": "ネギ属植物（タマネギ、ニンニク、ニラ、ネギ、エシャロット等）に含まれる"
                          "有機チオ硫酸化合物による酸化的赤血球障害。犬の体重1kgあたりタマネギ15〜30g（約0.5%体重）で"
                          "中毒量に達する。加工食品中のオニオンパウダーは特に高濃度で危険。",
        "pathophysiology_ja": "有機チオ硫酸化合物（n-propyl disulfide等）→ヘモグロビンの酸化→"
                              "ハインツ小体（変性ヘモグロビン凝集体）形成→赤血球膜の脆弱化→"
                              "脾臓での偏心細胞・球状赤血球除去→溶血性貧血。"
                              "摂取後1〜5日の潜伏期を経て貧血症状が発現（遅発性）。"
                              "メトヘモグロビン血症も併発→チアノーゼ・チョコレート色血液。",
        "causes_ja": "ネギ属植物の摂取：生・加熱・乾燥いずれの形態でも毒性あり。"
                     "オニオンスープ、ハンバーグ、すき焼き等の料理、ベビーフード（オニオンパウダー含有）。"
                     "ニンニクはタマネギの3〜5倍の毒性。秋田犬・柴犬は品種感受性が高い。",
        "treatment_ja": "摂取2時間以内：催吐（3%過酸化水素1〜2mL/kg PO）＋活性炭。"
                        "すでに貧血発症後：輸血（PCV<15%）、酸素療法、輸液。"
                        "メトヘモグロビン血症：N-アセチルシステイン（初回140mg/kg→70mg/kg q6h）。"
                        "特異的解毒薬なし。支持療法が主体。血液検査でPCV・ハインツ小体を経時的にモニター。",
        "prognosis_ja": "軽度摂取（<0.5%体重）：支持療法で回復良好。"
                        "大量摂取：重度の溶血性貧血→致死的となりうる。早期の催吐処置が予後を改善。"
                        "赤血球の再生には2〜4週間かかる。",
        "prevention_ja": "ネギ属植物を含む全ての食品へのアクセス制限。"
                         "テーブルフードの禁止。加工食品の成分確認。ガーリックサプリメントの禁止。",
        "urgency": "urgent",
    },
    {
        "name": "Ethylene Glycol Poisoning (Antifreeze)",
        "name_ja": "エチレングリコール中毒（不凍液）",
        "symptoms": {"vomiting", "excessive_thirst", "seizures", "lethargy"},
        "description": "Lethal antifreeze poisoning causing rapid kidney failure. Treatment must begin within hours.",
        "description_ja": "不凍液による致命的な中毒で、急速な腎不全を引き起こします。数時間以内の治療が必要です。",
        "pathophysiology_ja": "エチレングリコール摂取→肝臓でアルコールデヒドロゲナーゼ（ADH）により代謝→グリコアルデヒド→グリコール酸→シュウ酸。(1)代謝性アシドーシス（高アニオンギャップ）、(2)シュウ酸カルシウム結晶が腎尿細管に沈着→急性尿細管壊死→乏尿性腎不全。3段階の経過：I期（30分〜12h：酩酊様）→II期（12〜24h：心肺症状）→III期（24〜72h：腎不全）。致死量は犬で4.4mL/kg。",
        "causes_ja": "自動車用不凍液（エチレングリコール）の摂取。甘味があるため犬が好んで飲む。ガレージの不凍液漏れ、水たまりの汚染水。冬季に多い。少量でも致死的。摂取後8〜12時間以内のエタノールまたはフォメピゾール投与が救命に不可欠。",
        "prevention_ja": "不凍液のペットからの完全隔離、漏れの即時清掃、プロピレングリコール系の安全な代替品の使用、ガレージへのペットアクセス制限。",
        "urgency": "emergency",
    },
    {
        "name": "Marijuana Toxicosis",
        "name_ja": "大麻中毒",
        "symptoms": {"lethargy", "vomiting", "incontinence", "anxiety", "seizures"},
        "description": "THC intoxication causing depression, incoordination, and urinary incontinence.",
        "description_ja": "THC中毒で、沈鬱・運動失調・尿失禁を引き起こします。",
        "pathophysiology_ja": "THC（Δ9-tetrahydrocannabinol）のCB1受容体作用→CNS抑制（沈鬱・運動失調・散瞳）、尿失禁、低体温、徐脈。犬はCB1受容体密度が高く感受性が高い。エディブル（食用大麻製品）はチョコレート・キシリトールとの複合中毒リスク。",
        "causes_ja": "大麻（花穂・葉）、エディブル製品（グミ・クッキー・ブラウニー）、濃縮物（ワックス・オイル）の摂取。致死量は稀だが、高濃度THC製品やエディブルのチョコレート成分で重篤化。",
        "prevention_ja": "大麻製品のペットアクセス不能な場所での保管、エディブルの安全管理。",
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
        "pathophysiology_ja": "異物が胃内に停滞→幽門通過不能→持続的嘔吐。鋭利物→胃粘膜損傷・穿孔→腹膜炎。金属異物（亜鉛含有：1円硬貨・ボルト）→亜鉛中毒（溶血性貧血）。長期滞留→慢性胃炎・幽門閉塞。",
        "causes_ja": "玩具・骨片・石・靴下・コーンコブ・果物の種・硬貨。好発：若齢犬、ラブラドール・ゴールデン等。拾い食い癖のある犬。",
        "prevention_ja": "飲み込み可能な物へのアクセス制限、適切なサイズの玩具、拾い食い防止トレーニング、ゴミ箱の蓋の管理。",
        "urgency": "urgent",
    },
    # ---- Tumors (expanded) ----
    {
        "name": "Histiocytic Sarcoma",
        "name_ja": "組織球肉腫",
        "symptoms": {"lethargy", "weight_loss", "appetite_loss", "difficulty_breathing", *_ANY_LIMPING},
        "description": "An aggressive cancer of histiocyte cells, common in Bernese Mountain Dogs and Flat-Coated Retrievers.",
        "description_ja": "組織球由来の悪性腫瘍で、バーニーズやフラットコーテッドレトリーバーに多いです。",
        "pathophysiology_ja": "樹状細胞またはマクロファージ由来の悪性腫瘍。局在型（脾臓・四肢関節周囲に単発腫瘤）と播種型（多臓器同時浸潤：脾臓・肝臓・肺・骨髄・リンパ節）に分類。播種型は急速に進行し、診断時にはすでに多臓器浸潤。貧血・血小板減少・DICを高率に合併。",
        "causes_ja": "遺伝的素因が強い。バーニーズマウンテンドッグ（生涯発症リスク25%）、フラットコーテッドレトリーバー、ロットワイラー、ゴールデンレトリーバーに好発。中高齢犬。CDKN2A等の腫瘍抑制遺伝子の変異が関与。",
        "prevention_ja": "確実な予防法はない。好発犬種の繁殖管理（罹患犬系統の繁殖制限）、定期的な健康診断（血液検査・腹部エコー）。ロムスチン（CCNU）化学療法のMSTは約5ヶ月。",
        "urgency": "urgent",
    },
    {
        "name": "Fibrosarcoma",
        "name_ja": "線維肉腫",
        "symptoms": {"lumps", "pain_on_touch", *_ANY_LIMPING},
        "description": "A malignant tumor of connective tissue, locally aggressive with high recurrence rate.",
        "description_ja": "結合組織の悪性腫瘍で、局所浸潤性が高く再発率も高いです。",
        "pathophysiology_ja": "線維芽細胞由来の悪性腫瘍→局所的に浸潤性の増殖→偽被膜を超えた微視的浸潤→不完全切除では高率に再発（60〜70%）。転移率は比較的低い（20〜30%）が、高グレードでは肺転移あり。口腔・四肢・体幹に好発。骨への浸潤もある。放射線誘発性線維肉腫（過去の放射線治療部位）の報告もある。",
        "causes_ja": "原因不明。ゴールデンレトリーバー・大型犬に好発。中高齢犬。口腔の線維肉腫は犬の口腔腫瘍の第3位。ワクチン接種部位関連（猫では有名だが犬では稀）。",
        "prevention_ja": "確実な予防法はない。しこりの早期発見・FNA→生検→広範囲切除（2〜3cm以上のマージン）。不完全切除後は追加手術または放射線療法。",
        "urgency": "normal",
    },
    {
        "name": "Anal Sac Adenocarcinoma",
        "name_ja": "肛門嚢腺癌",
        "symptoms": {"constipation", "pain_on_touch", "excessive_thirst"},
        "description": "A malignant tumor of the anal glands causing elevated calcium levels and straining.",
        "description_ja": "肛門腺の悪性腫瘍で、高カルシウム血症と排便困難を引き起こします。",
        "pathophysiology_ja": "肛門嚢のアポクリン腺上皮の悪性増殖→肛門周囲の浸潤性腫瘤→仙骨下リンパ節転移（50〜90%で診断時に転移あり）→肺転移。腫瘍随伴性高カルシウム血症（PTHrP産生、約25〜50%）→多飲多尿・腎障害・筋力低下。高Ca血症が初発症状となり偶然発見されることがある。",
        "causes_ja": "原因不明。中高齢犬（平均10〜11歳）。スパニエル種に好発との報告あるが、全犬種で発生。避妊/去勢との関連は不明確。直腸検査での偶然発見が多い。片側性が多いが両側性もある。",
        "prevention_ja": "確実な予防法はない。中高齢犬の定期的な直腸検査（肛門嚢の触診）。高Ca血症の犬では本疾患を鑑別に挙げる。外科的切除＋仙骨下リンパ節郭清が標準治療。MST 12〜18ヶ月（手術＋化学療法）。",
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
        "pathophysiology_ja": "甲状腺濾胞上皮細胞の悪性増殖→頸部の固着性腫瘤→気管・食道・頸静脈への浸潤→呼吸困難・嚥下障害。犬の甲状腺腫瘍の85〜90%が悪性（人とは逆で良性が少ない）。約35〜40%が機能性（甲状腺機能亢進症を伴う）。肺・局所リンパ節への転移率は診断時30〜40%。可動性の場合は予後良好、固着性は予後不良。",
        "causes_ja": "原因不明。ビーグル、ボクサー、ゴールデンレトリーバーに好発。中高齢犬（9〜11歳）。多くは非機能性で甲状腺ホルモン値は正常。頸部の触診で偶然発見されることが多い。腫瘤がfree（可動性あり）かfixed（固着性）かで手術適応と予後が大きく異なる。",
        "prevention_ja": "確実な予防法はない。中高齢犬の定期的な頸部触診。可動性のある腫瘤は外科的切除で予後良好（MST >3年）。固着性は放射性ヨウ素療法（I-131）またはドキソルビシン化学療法を検討。",
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
        "pathophysiology_ja": "愛着対象（飼い主）との分離→HPA軸の過剰活性化→コルチゾール上昇→パニック様行動（破壊・鳴き声・排泄・自傷）。過覚醒状態→セロトニン系の調節障害。出発前の儀式的行動（鍵の音・靴を履く等）が条件刺激として不安を誘発。",
        "causes_ja": "早期離乳・社会化不足、飼い主の生活パターンの急変（在宅勤務→出社）、転居、単頭飼育、保護犬の過去のトラウマ。疼痛・認知機能不全が根底にある場合もある。",
        "prevention_ja": "子犬期からの段階的な一人時間の訓練、出発/帰宅時の過度な挨拶の回避、安心できる場所（クレート）の確保、環境エンリッチメント（知育玩具・Kong）。",
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
        "pathophysiology_ja": "大きな音→扁桃体の過剰活性化→交感神経系亢進→頻脈・パンティング・振戦・逃避行動。反復暴露で感作が進行（脱感作ではなく増悪）。雷恐怖症では気圧変化・静電気も条件刺激となる。加齢に伴い悪化する傾向。",
        "causes_ja": "遺伝的素因（牧羊犬・猟犬種に多い）、社会化期の音響暴露不足、過去のトラウマ体験、疼痛・認知機能低下との併存。好発：ボーダーコリー、ジャーマンシェパード、オーストラリアンシェパード。",
        "prevention_ja": "子犬期（3〜14週齢）の段階的な音響暴露・脱感作、安全な避難場所の確保、興奮時の過度な慰め（恐怖の強化）の回避。",
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
        "pathophysiology_ja": "基礎疾患→組織因子の大量放出/内皮障害→凝固カスケードの全身的活性化→微小血管内血栓形成（多臓器微小梗塞）→凝固因子・血小板の消費→消費性凝固障害→出血傾向（点状出血・体腔内出血・穿刺部出血）。フィブリン分解産物（FDP/D-dimer）上昇、血小板減少、PT/APTT延長が診断指標。",
        "causes_ja": "単独疾患ではなく基礎疾患の合併症。犬で多い原因：血管肉腫、IMHA、GDV、膵炎、敗血症、蛇咬傷、熱射病。致死率は基礎疾患と進行度に依存するが50〜70%と高い。",
        "prevention_ja": "基礎疾患の早期・適切な治療が最重要。DIC早期徴候（点状出血・穿刺部持続出血・血小板減少）のモニタリング。新鮮凍結血漿・ヘパリン投与は基礎疾患治療と並行。",
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
        "pathophysiology_ja": "下部尿路感染→尿管を経由した上行性感染→腎盂・腎実質の細菌感染→化膿性炎症→腎実質の破壊。慢性化すると腎線維化→CKDへの進行。敗血症のリスク。片側性が多いが両側性もある。",
        "causes_ja": "E. coli（最多）、Staphylococcus、Proteus、Enterococcus。リスク因子：尿路結石、先天性尿管異所開口、免疫抑制、クッシング症候群、糖尿病。雌犬に多い。",
        "prevention_ja": "下部尿路感染の適切な治療、尿路結石の管理、免疫抑制状態の早期対応、定期的な尿検査。",
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
        "pathophysiology_ja": "外力→歯の破折（エナメル質のみ/象牙質露出/歯髄露出）。歯髄露出（complicated fracture）→歯髄炎→歯髄壊死→根尖周囲膿瘍。上顎第4前臼歯（裂肉歯）と犬歯に最多。未治療の歯髄露出は100%感染する。",
        "causes_ja": "硬い物の咀嚼（蹄・角・鹿の骨・硬すぎるナイロン製咀嚼玩具・氷）、外傷、ケージバイティング。上顎第4前臼歯のスラブ骨折が最多パターン。",
        "prevention_ja": "爪で跡がつかないほど硬い物の回避（「ニーテスト」：自分の膝蓋骨に当てて痛ければ硬すぎる）、適切な硬さの咀嚼玩具の選択。",
        "urgency": "normal",
    },
    {
        "name": "Oral Melanoma",
        "name_ja": "口腔メラノーマ",
        "symptoms": {"appetite_loss", "lumps", "weight_loss"},
        "description": "The most common malignant oral tumor in dogs, highly aggressive with early metastasis.",
        "description_ja": "犬で最も多い口腔悪性腫瘍で、早期に転移する高悪性度腫瘍です。",
        "pathophysiology_ja": "口腔粘膜メラノサイトの悪性増殖→局所浸潤性腫瘤形成→歯槽骨破壊→早期リンパ節転移（転移率80%以上）→肺転移。高度な局所浸潤性と全身転移性を有する犬で最も予後不良な口腔腫瘍。WHO Stage I〜IV（腫瘤径と転移有無で分類）。メラニン欠乏型（無色素性メラノーマ）は診断が困難。",
        "causes_ja": "原因不明。口腔粘膜のメラノサイト由来。好発：コッカースパニエル、スコティッシュテリア、ゴールデンレトリーバー、ミニチュアプードル、ダックスフンド。中高齢犬（10〜12歳）。口腔メラノーマの約80%が悪性。歯肉に最も多い。",
        "prevention_ja": "確実な予防法はない。口腔内のしこり・出血・口臭・摂食困難の早期受診。早期発見が予後を改善。メラノーマワクチン（Oncept DNA）がStage II-III/術後の補助療法として承認。",
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
        "pathophysiology_ja": "胸管またはその分枝の損傷・閉塞・圧迫→乳び液の胸腔内漏出→胸水貯留→肺の圧排→呼吸困難。慢性乳び胸→線維性胸膜炎（constrictive pleuritis）→肺の拡張障害（不可逆的）。乳び液はトリグリセリド高値（>100mg/dL）・コレステロール低値が特徴。",
        "causes_ja": "特発性（最多、犬では60〜70%）。二次性：心疾患（右心不全、心膜炎）、縦隔腫瘍（リンパ腫）、外傷、胸管奇形。好発犬種：アフガンハウンド、柴犬（日本の報告で多い）。中高齢犬に多い。",
        "prevention_ja": "確実な予防法はない。基礎疾患（心疾患・縦隔腫瘍）の管理。低脂肪食（MCTオイル食）で乳び産生を減少。内科不応例は胸管結紮＋心嚢膜部分切除術。",
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
        "pathophysiology_ja": "ランゲルハンス細胞（皮膚樹状細胞）由来の良性腫瘍。急速に増大（数週間）→免疫系によるT細胞浸潤→1〜3ヶ月で自然退縮。頭部・耳介・四肢に好発。多発例は悪性の可能性を検討。",
        "causes_ja": "原因不明。3歳未満の若齢犬に好発（特にボクサー、ダックスフンド、コッカースパニエル、グレートデーン）。ウイルス関与説あるが未確定。",
        "prevention_ja": "予防法はない。通常自然退縮するため経過観察。2〜3ヶ月で退縮しない場合や多発例は生検で悪性腫瘍との鑑別が必要。",
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
        "pathophysiology_ja": "耳の掻破・頭部振盪→耳介軟骨と皮膚間の血管破裂→血腫形成。無治療では線維化・耳介の変形（カリフラワー耳）。基礎に外耳炎・アレルギー→掻痒→掻破の悪循環。免疫介在性の血管炎が関与するとの説もある。",
        "causes_ja": "外耳炎・耳ダニ・アレルギーによる掻痒→耳の掻破・頭振り。垂れ耳犬種（コッカースパニエル、バセットハウンド）に好発。凝固異常がある場合は大きな血腫になりやすい。",
        "prevention_ja": "基礎疾患（外耳炎・アレルギー）の早期・適切な治療、耳の掻痒の原因精査と管理。",
        "urgency": "normal",
    },
    # ---- NEW DISEASES BATCH 1 (Orthopedic / Musculoskeletal) ----
    {
        "name": "Carpal Hyperextension Injury",
        "name_ja": "手根関節過伸展損傷",
        "symptoms": {"limping_fl", "limping_fr", "swollen_joints", "pain_on_touch", "reluctance_move"},
        "description": "Breakdown of the carpal ligaments causing the carpus to drop, often from jumping or falling from a height.",
        "description_ja": "手根靭帯の断裂により手根関節が過伸展する状態で、高所からの飛び降りや落下が原因となることが多いです。",
        "urgency": "urgent",
    },
    {
        "name": "Fragmented Medial Coronoid Process (FMCP)",
        "name_ja": "内側鉤状突起分離症",
        "symptoms": {"limping_fl", "limping_fr", "stiffness", "swollen_joints", "reluctance_move"},
        "description": "A developmental condition where a small piece of bone breaks off inside the elbow joint, causing pain and lameness.",
        "description_ja": "肘関節内の小さな骨片が分離する発達性疾患で、痛みと跛行を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Ununited Anconeal Process (UAP)",
        "name_ja": "肘突起癒合不全",
        "symptoms": {"limping_fl", "limping_fr", "stiffness", "swollen_joints", "pain_on_touch"},
        "description": "Failure of the anconeal process to fuse with the ulna, leading to elbow joint instability and arthritis.",
        "description_ja": "肘突起が尺骨と癒合しない状態で、肘関節の不安定性と関節炎を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Temporomandibular Joint (TMJ) Dysplasia",
        "name_ja": "顎関節形成不全",
        "symptoms": {"pain_on_touch", "appetite_loss", "drooling", "reluctance_move"},
        "description": "Malformation of the jaw joint causing difficulty opening or closing the mouth, pain when chewing.",
        "description_ja": "顎関節の形成不全で、口の開閉が困難になり、咀嚼時に痛みが生じます。",
        "urgency": "normal",
    },
    {
        "name": "Bicipital Tenosynovitis",
        "name_ja": "上腕二頭筋腱鞘炎",
        "symptoms": {"limping_fl", "limping_fr", "pain_on_touch", "stiffness", "reluctance_move"},
        "description": "Inflammation of the biceps tendon and its sheath in the shoulder, causing forelimb lameness.",
        "description_ja": "肩の上腕二頭筋腱とその鞘の炎症で、前肢の跛行を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Infraspinatus Contracture",
        "name_ja": "棘下筋拘縮",
        "symptoms": {"limping_fl", "limping_fr", "stiffness", "reluctance_move"},
        "description": "Fibrosis and contracture of the infraspinatus muscle after injury, causing a characteristic gait abnormality.",
        "description_ja": "損傷後の棘下筋の線維化と拘縮で、特徴的な歩行異常を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Hypertrophic Osteodystrophy (HOD) - Severe",
        "name_ja": "肥大性骨異栄養症（重症型）",
        "symptoms": {"fever", "swollen_joints", "limping_fl", "limping_fr", "limping_rl", "limping_rr", "appetite_loss", "lethargy"},
        "description": "Severe form of HOD in rapidly growing large-breed puppies with high fever and significant bone pain.",
        "description_ja": "急速に成長する大型犬の子犬に見られるHODの重症型で、高熱と著しい骨の痛みを伴います。",
        "urgency": "urgent",
    },
    {
        "name": "Iliopsoas Muscle Strain",
        "name_ja": "腸腰筋損傷",
        "symptoms": {"limping_rl", "limping_rr", "pain_on_touch", "stiffness", "reluctance_move"},
        "description": "Strain or tear of the iliopsoas muscle causing hind limb lameness and pain on hip extension.",
        "description_ja": "腸腰筋の損傷または断裂で、後肢の跛行と股関節伸展時の痛みを引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Gracilis/Semitendinosus Myopathy",
        "name_ja": "薄筋・半腱様筋ミオパチー",
        "symptoms": {"limping_rl", "limping_rr", "stiffness", "reluctance_move"},
        "description": "Fibrotic myopathy of the thigh muscles, common in German Shepherds, causing a characteristic short-strided gait.",
        "description_ja": "大腿筋の線維性ミオパチーで、ジャーマンシェパードに多く、特徴的な短い歩幅の歩行を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Sesamoid Disease",
        "name_ja": "種子骨疾患",
        "symptoms": {"limping_fl", "limping_fr", "limping_rl", "limping_rr", "pain_on_touch", "swollen_joints"},
        "description": "Fragmentation or inflammation of the sesamoid bones in the paw, causing intermittent lameness.",
        "description_ja": "足の種子骨の断片化または炎症で、間欠的な跛行を引き起こします。",
        "urgency": "normal",
    },
    # ---- Neurological ----
    {
        "name": "Necrotizing Meningoencephalitis (NME)",
        "name_ja": "壊死性髄膜脳炎",
        "symptoms": {"seizures", "circling", "head_tilting", "lethargy", "aggression_change", "collapse"},
        "description": "A fatal inflammatory brain disease most common in Pugs, Maltese, and Chihuahuas, causing seizures and neurological decline.",
        "description_ja": "パグ、マルチーズ、チワワに多い致死性の炎症性脳疾患で、けいれんと神経学的衰退を引き起こします。",
        "urgency": "emergency",
    },
    {
        "name": "Necrotizing Leukoencephalitis (NLE)",
        "name_ja": "壊死性白質脳炎",
        "symptoms": {"seizures", "circling", "head_tilting", "lethargy", "difficulty_breathing"},
        "description": "An inflammatory brain disease affecting the white matter, seen primarily in Yorkshire Terriers.",
        "description_ja": "白質を侵す炎症性脳疾患で、主にヨークシャーテリアに見られます。",
        "urgency": "emergency",
    },
    {
        "name": "Spinal Arachnoid Diverticulum",
        "name_ja": "脊髄くも膜憩室",
        "symptoms": {"limping_rl", "limping_rr", "stiffness", "reluctance_move", "incontinence"},
        "description": "A fluid-filled cyst in the spinal canal that compresses the spinal cord, causing progressive hind limb weakness.",
        "description_ja": "脊柱管内の液体で満たされた嚢胞が脊髄を圧迫し、進行性の後肢の衰弱を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Steroid-Responsive Meningitis-Arteritis (SRMA)",
        "name_ja": "ステロイド反応性髄膜炎-動脈炎",
        "symptoms": {"fever", "lethargy", "pain_on_touch", "stiffness", "reluctance_move", "appetite_loss"},
        "description": "An immune-mediated inflammatory disease of the meninges and arteries causing severe neck pain and fever in young dogs.",
        "description_ja": "髄膜と動脈の免疫介在性炎症性疾患で、若い犬に重度の頸部痛と発熱を引き起こします。",
        "pathophysiology_ja": "免疫調節障害→髄膜血管への好中球浸潤（急性型）→フィブリノイド壊死性動脈炎→重度の頸部硬直・疼痛・高熱（40〜41℃）。CSF解析：好中球性多細胞症・IgA上昇が特徴的。慢性型は肉芽腫性変化→線維化。適切なステロイド療法で予後良好だが、減薬が早すぎると50%が再発。",
        "causes_ja": "原因不明の免疫介在性疾患。IgA系の異常が主因とされる。若齢犬（6〜18ヶ月）に好発。好発犬種：ビーグル、バーニーズマウンテンドッグ、ボクサー、ノバスコシアダックトーリングレトリーバー。ワクチン接種との時間的関連が報告されるが因果関係は未確定。",
        "prevention_ja": "確実な予防法はない。「首が痛くて動けない若い犬」はSRMAを疑う。早期のCSF検査・ステロイド開始が予後を改善。プレドニゾロン2mg/kg/日で開始→6ヶ月以上かけて漸減が標準プロトコル。",
        "urgency": "urgent",
    },
    {
        "name": "Canine Spinal Muscular Atrophy",
        "name_ja": "犬脊髄性筋萎縮症",
        "symptoms": {"limping_rl", "limping_rr", "stiffness", "reluctance_move", "lethargy"},
        "description": "A hereditary degeneration of motor neurons in the spinal cord causing progressive muscle weakness and atrophy.",
        "description_ja": "脊髄の運動ニューロンの遺伝性変性で、進行性の筋力低下と萎縮を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Lissencephaly",
        "name_ja": "滑脳症",
        "symptoms": {"seizures", "circling", "aggression_change", "anxiety", "lethargy"},
        "description": "A congenital brain malformation where the brain surface lacks normal folds, causing seizures and behavioral abnormalities.",
        "description_ja": "脳表面に正常なひだがない先天性脳奇形で、けいれんと行動異常を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Peripheral Nerve Sheath Tumor",
        "name_ja": "末梢神経鞘腫瘍",
        "symptoms": {"limping_fl", "limping_fr", "limping_rl", "limping_rr", "pain_on_touch", "stiffness"},
        "description": "A tumor arising from the nerve sheath causing progressive lameness and muscle atrophy in the affected limb.",
        "description_ja": "神経鞘から発生する腫瘍で、患肢の進行性の跛行と筋萎縮を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Spongiform Leukoencephalomyelopathy",
        "name_ja": "海綿状白質脳脊髄症",
        "symptoms": {"limping_rl", "limping_rr", "stiffness", "reluctance_move", "head_tilting"},
        "description": "A degenerative disease of the spinal cord white matter seen in certain breeds, causing progressive ataxia.",
        "description_ja": "特定の犬種に見られる脊髄白質の変性疾患で、進行性の運動失調を引き起こします。",
        "urgency": "normal",
    },
    # ---- Cardiac ----
    {
        "name": "Tricuspid Valve Dysplasia",
        "name_ja": "三尖弁形成不全",
        "symptoms": {"lethargy", "difficulty_breathing", "bloated_abdomen", "collapse", "coughing"},
        "description": "A congenital malformation of the tricuspid valve causing right-sided heart failure, common in Labrador Retrievers.",
        "description_ja": "三尖弁の先天性奇形で右心不全を引き起こし、ラブラドールレトリバーに多く見られます。",
        "urgency": "urgent",
    },
    {
        "name": "Subaortic Stenosis (SAS)",
        "name_ja": "大動脈弁下狭窄症",
        "symptoms": {"lethargy", "collapse", "difficulty_breathing", "coughing", "excessive_panting"},
        "description": "A congenital narrowing below the aortic valve causing left ventricular outflow obstruction, common in large breeds.",
        "description_ja": "大動脈弁下の先天性狭窄で左心室流出路閉塞を引き起こし、大型犬に多く見られます。",
        "urgency": "urgent",
    },
    {
        "name": "Cardiac Tamponade",
        "name_ja": "心タンポナーデ",
        "symptoms": {"collapse", "difficulty_breathing", "rapid_breathing", "lethargy", "excessive_panting"},
        "description": "Life-threatening compression of the heart by fluid accumulation in the pericardial sac, requiring emergency drainage.",
        "description_ja": "心嚢液の貯留による心臓の圧迫で、緊急排液が必要な致死的状態です。",
        "urgency": "emergency",
    },
    {
        "name": "Cor Pulmonale",
        "name_ja": "肺性心",
        "symptoms": {"coughing", "difficulty_breathing", "lethargy", "bloated_abdomen", "collapse"},
        "description": "Right-sided heart failure secondary to chronic lung disease or pulmonary hypertension.",
        "description_ja": "慢性肺疾患または肺高血圧症に続発する右心不全です。",
        "urgency": "urgent",
    },
    {
        "name": "Ventricular Tachycardia",
        "name_ja": "心室頻拍",
        "symptoms": {"collapse", "lethargy", "difficulty_breathing", "excessive_panting", "rapid_breathing"},
        "description": "A dangerous rapid heart rhythm originating from the ventricles that can lead to sudden death.",
        "description_ja": "心室から発生する危険な頻拍で、突然死につながる可能性があります。",
        "urgency": "emergency",
    },
    {
        "name": "Third-Degree Atrioventricular Block",
        "name_ja": "第三度房室ブロック",
        "symptoms": {"collapse", "lethargy", "reluctance_move", "excessive_panting", "stiffness"},
        "description": "Complete block of electrical signals from the atria to ventricles, causing dangerously slow heart rate.",
        "description_ja": "心房から心室への電気信号の完全遮断で、危険な徐脈を引き起こします。",
        "urgency": "emergency",
    },
    # ---- Endocrine ----
    {
        "name": "Hyperaldosteronism (Conn's Syndrome)",
        "name_ja": "高アルドステロン症",
        "symptoms": {"excessive_thirst", "excessive_urination", "lethargy", "stiffness", "weight_loss"},
        "description": "Excess aldosterone production causing potassium depletion, muscle weakness, and hypertension.",
        "description_ja": "アルドステロンの過剰産生によりカリウム欠乏、筋力低下、高血圧を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Acromegaly (Growth Hormone Excess)",
        "name_ja": "先端巨大症",
        "symptoms": {"weight_gain", "excessive_thirst", "excessive_urination", "lethargy", "stiffness", "difficulty_breathing"},
        "description": "Excessive growth hormone production causing enlargement of body tissues, insulin resistance, and organ dysfunction.",
        "description_ja": "成長ホルモンの過剰産生により体組織の肥大、インスリン抵抗性、臓器機能障害を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Hypoparathyroidism",
        "name_ja": "副甲状腺機能低下症",
        "symptoms": {"seizures", "stiffness", "lethargy", "anxiety", "excessive_panting"},
        "description": "Deficient parathyroid hormone causing dangerously low blood calcium levels, muscle tremors and seizures.",
        "description_ja": "副甲状腺ホルモンの欠乏により危険な低カルシウム血症、筋肉の震えとけいれんを引き起こします。",
        "urgency": "emergency",
    },
    {
        "name": "Diabetic Ketoacidosis (DKA)",
        "name_ja": "糖尿病性ケトアシドーシス",
        "symptoms": {"vomiting", "lethargy", "appetite_loss", "dehydration", "excessive_thirst", "rapid_breathing", "collapse"},
        "description": "A life-threatening complication of diabetes where the body produces excess ketones, causing metabolic acidosis.",
        "description_ja": "糖尿病の致死的合併症で、体が過剰なケトン体を産生し、代謝性アシドーシスを引き起こします。",
        "pathophysiology_ja": "絶対的または相対的インスリン欠乏→高血糖→浸透圧利尿→重度脱水・電解質喪失（K、Na、P）。同時に脂肪分解亢進→肝臓でケトン体（β-ヒドロキシ酪酸・アセト酢酸）過剰産生→代謝性アシドーシス（高アニオンギャップ）→嘔吐・腹痛→さらなる脱水の悪循環。低K血症→心不整脈→死亡。併発疾患（膵炎・UTI・クッシング）が誘因。",
        "causes_ja": "未診断の糖尿病、インスリン投与の中断/不足、併発疾患（膵炎・感染症・クッシング症候群）による急性増悪。犬糖尿病の約40%がDKAとして初診。中高齢の未避妊雌犬（プロゲステロンによるインスリン抵抗性）にリスク高。",
        "prevention_ja": "糖尿病の適切なインスリン管理・血糖モニタリング、併発疾患の早期治療、食欲低下時のインスリン用量調整（自己判断でインスリン中止しない）、定期的なフルクトサミン/HbA1c測定。",
        "urgency": "emergency",
    },
    {
        "name": "Hyperadrenocorticism - Iatrogenic",
        "name_ja": "医原性副腎皮質機能亢進症",
        "symptoms": {"excessive_thirst", "excessive_urination", "weight_gain", "hair_loss", "lethargy", "excessive_panting"},
        "description": "Cushing's-like syndrome caused by prolonged corticosteroid medication use.",
        "description_ja": "長期間のコルチコステロイド薬の使用による副腎皮質機能亢進症様症候群です。",
        "urgency": "normal",
    },
    # ---- Dermatologic ----
    {
        "name": "Canine Atopic Dermatitis",
        "name_ja": "犬アトピー性皮膚炎",
        "symptoms": {"itching", "skin_redness", "hair_loss", "ear_scratching", "hot_spots", "skin_lesions"},
        "description": "A chronic allergic skin disease with genetic predisposition, causing intense itching and recurrent skin infections.",
        "description_ja": "遺伝的素因を持つ慢性アレルギー性皮膚疾患で、強い痒みと再発性皮膚感染を引き起こします。",
        "pathophysiology_ja": "フィラグリン等の皮膚バリア蛋白の遺伝的異常→経皮アレルゲン侵入→ランゲルハンス細胞がTh2応答を誘導→IgE産生→肥満細胞脱顆粒→ヒスタミン/IL-31放出→激しい掻痒。慢性化で皮膚の苔癬化・色素沈着・二次感染（細菌・マラセチア）。",
        "causes_ja": "環境アレルゲン（ハウスダストマイト、花粉、カビ胞子）に対する遺伝的過敏性。発症1〜3歳。好発犬種：フレンチブルドッグ、柴犬、ウエストハイランドテリア、ラブラドール、ゴールデンレトリーバー。",
        "prevention_ja": "完全予防は困難。環境アレルゲンの軽減（HEPA空気清浄機・寝具の頻回洗濯）、皮膚バリア強化（EFA含有食・セラミド配合シャンプー）、好発犬種での早期スクリーニング、減感作療法（ASIT）の早期開始。",
        "prognosis_ja": "生涯管理が必要。マルチモーダル治療（オクラシチニブ・ロキベトマブ・減感作療法・スキンケア）で80%以上が良好なQOL維持。二次感染の反復管理が鍵。",
        "urgency": "normal",
    },
    {
        "name": "Zinc-Responsive Dermatosis - Syndrome I",
        "name_ja": "亜鉛反応性皮膚症候群I型",
        "symptoms": {"skin_lesions", "hair_loss", "skin_redness", "dry_skin", "itching"},
        "description": "Crusting and scaling skin disease around the face and pressure points in Arctic breeds due to zinc malabsorption.",
        "description_ja": "亜鉛の吸収不良により北極犬種の顔と圧迫部位に痂皮と鱗屑を生じる皮膚疾患です。",
        "urgency": "normal",
    },
    {
        "name": "Dermatomyositis",
        "name_ja": "皮膚筋炎",
        "symptoms": {"skin_lesions", "hair_loss", "skin_redness", "stiffness", "lethargy"},
        "description": "An inherited inflammatory disease of the skin and muscles in Collies and Shetland Sheepdogs.",
        "description_ja": "コリーとシェットランドシープドッグに見られる皮膚と筋肉の遺伝性炎症性疾患です。",
        "urgency": "normal",
    },
    {
        "name": "Canine Pattern Baldness",
        "name_ja": "犬パターン脱毛症",
        "symptoms": {"hair_loss", "dry_skin"},
        "description": "Non-inflammatory hereditary alopecia affecting specific body regions, common in Dachshunds and other breeds.",
        "description_ja": "特定の体部位に影響する非炎症性の遺伝性脱毛症で、ダックスフンドなどに多いです。",
        "urgency": "normal",
    },
    {
        "name": "Cutaneous Vasculitis",
        "name_ja": "皮膚血管炎",
        "symptoms": {"skin_lesions", "skin_redness", "swelling", "hair_loss", "fever", "lethargy"},
        "description": "Inflammation and necrosis of blood vessels in the skin caused by immune-mediated reactions or infections.",
        "description_ja": "免疫介在性反応や感染症による皮膚の血管の炎症と壊死です。",
        "urgency": "urgent",
    },
    {
        "name": "Nasal Hyperkeratosis",
        "name_ja": "鼻鏡角化症",
        "symptoms": {"dry_skin", "nasal_discharge"},
        "description": "Excessive keratinization of the nose causing a dry, crusty, and cracked nasal planum.",
        "description_ja": "鼻の過度な角質化により、乾燥し、痂皮を形成し、ひび割れた鼻鏡を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Calcinosis Cutis",
        "name_ja": "皮膚石灰沈着症",
        "symptoms": {"skin_lesions", "skin_redness", "itching", "hair_loss", "lumps"},
        "description": "Deposition of calcium salts in the skin, often associated with Cushing's disease or corticosteroid use.",
        "description_ja": "皮膚へのカルシウム塩の沈着で、クッシング病やコルチコステロイドの使用に関連することが多いです。",
        "urgency": "normal",
    },
    {
        "name": "Vitiligo",
        "name_ja": "白斑症",
        "symptoms": {"skin_lesions", "hair_loss"},
        "description": "Loss of pigment in the skin and hair due to immune-mediated destruction of melanocytes.",
        "description_ja": "メラノサイトの免疫介在性破壊による皮膚と被毛の色素脱失です。",
        "urgency": "normal",
    },
    # ---- Ophthalmologic ----
    {
        "name": "Iris Atrophy",
        "name_ja": "虹彩萎縮",
        "symptoms": {"squinting", "eye_redness", "eye_discharge"},
        "description": "Age-related thinning of the iris tissue, causing sensitivity to bright light and irregular pupil shape.",
        "description_ja": "加齢に伴う虹彩組織の菲薄化で、強い光に対する過敏性と不整な瞳孔形状を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Anterior Lens Luxation",
        "name_ja": "前方水晶体脱臼",
        "symptoms": {"eye_redness", "squinting", "eye_discharge", "pain_on_touch"},
        "description": "The lens displaces forward into the anterior chamber, causing acute glaucoma and pain; a surgical emergency.",
        "description_ja": "水晶体が前房に前方脱臼し、急性緑内障と痛みを引き起こす外科的緊急症です。",
        "urgency": "emergency",
    },
    {
        "name": "Eyelid Mass (Meibomian Gland Adenoma)",
        "name_ja": "眼瞼腫瘤（マイボーム腺腫）",
        "symptoms": {"eye_discharge", "squinting", "eye_redness", "lumps"},
        "description": "A benign tumor of the meibomian glands in the eyelid, common in older dogs, that may irritate the cornea.",
        "description_ja": "眼瞼のマイボーム腺の良性腫瘍で、高齢犬に多く、角膜を刺激することがあります。",
        "urgency": "normal",
    },
    {
        "name": "Optic Neuritis",
        "name_ja": "視神経炎",
        "symptoms": {"eye_redness", "squinting", "circling", "anxiety", "reluctance_move"},
        "description": "Inflammation of the optic nerve causing sudden blindness, often immune-mediated or infectious in origin.",
        "description_ja": "視神経の炎症で突然の失明を引き起こし、免疫介在性や感染性が原因となることが多いです。",
        "urgency": "urgent",
    },
    {
        "name": "Hyphema",
        "name_ja": "前房出血",
        "symptoms": {"eye_redness", "squinting", "eye_discharge", "pain_on_touch"},
        "description": "Bleeding into the anterior chamber of the eye, which may indicate trauma, coagulopathy, or intraocular tumor.",
        "description_ja": "眼の前房内の出血で、外傷、凝固障害、または眼内腫瘍を示唆することがあります。",
        "urgency": "urgent",
    },
    # ---- Dental / Oral ----
    {
        "name": "Canine Chronic Ulcerative Stomatitis (CCUS)",
        "name_ja": "犬慢性潰瘍性口内炎",
        "symptoms": {"drooling", "appetite_loss", "pain_on_touch", "skin_lesions", "weight_loss"},
        "description": "Severe immune-mediated oral mucosal ulceration triggered by contact with dental plaque.",
        "description_ja": "歯垢との接触により誘発される重度の免疫介在性口腔粘膜潰瘍です。",
        "urgency": "urgent",
    },
    {
        "name": "Mandibular Fracture",
        "name_ja": "下顎骨骨折",
        "symptoms": {"drooling", "pain_on_touch", "appetite_loss", "swelling", "aggression_change"},
        "description": "A fracture of the lower jaw bone, often caused by trauma or weakened bone from periodontal disease.",
        "description_ja": "下顎骨の骨折で、外傷や歯周病による骨の弱化が原因となることが多いです。",
        "urgency": "emergency",
    },
    {
        "name": "Oral Papillomatosis",
        "name_ja": "口腔乳頭腫症",
        "symptoms": {"drooling", "lumps", "appetite_loss"},
        "description": "Viral wart-like growths in the mouth caused by canine papillomavirus, most common in young dogs.",
        "description_ja": "犬パピローマウイルスによる口腔内のイボ状腫瘤で、若い犬に最も多く見られます。",
        "pathophysiology_ja": "犬パピローマウイルス（CPV-1）の口腔粘膜感染→基底上皮細胞でのウイルス増殖→乳頭状（カリフラワー様）の良性腫瘤形成。口唇・舌・硬口蓋・咽頭に多発。免疫成熟に伴い細胞性免疫が誘導され1〜5ヶ月で自然退縮。大量発生時は摂食・嚥下障害。",
        "causes_ja": "犬パピローマウイルス1型（CPV-1）。感染犬との直接接触・汚染物（共有の水飲み・玩具）経由。潜伏期間1〜2ヶ月。免疫未成熟な若齢犬（2歳未満）に好発。免疫抑制犬では退縮せず持続・悪性化のリスク。",
        "prevention_ja": "感染犬との接触制限（ドッグパーク・多頭飼育環境）、免疫抑制犬の感染環境回避。免疫正常犬では自然治癒するため基本的に治療不要。重症例ではアザシチジン局所投与やインターフェロン療法を検討。",
        "urgency": "normal",
    },
    {
        "name": "Enamel Hypoplasia",
        "name_ja": "エナメル質形成不全",
        "symptoms": {"drooling", "pain_on_touch", "appetite_loss"},
        "description": "Incomplete development of tooth enamel due to fever, infection, or nutritional deficiencies during tooth formation.",
        "description_ja": "歯の形成期の発熱、感染、栄養不足によるエナメル質の不完全な発達です。",
        "urgency": "normal",
    },
    {
        "name": "Dentigerous Cyst",
        "name_ja": "含歯性嚢胞",
        "symptoms": {"swelling", "drooling", "pain_on_touch", "appetite_loss"},
        "description": "A fluid-filled cyst that develops around an unerupted tooth, causing bone destruction in the jaw.",
        "description_ja": "未萌出歯の周囲に発生する液体で満たされた嚢胞で、顎骨の破壊を引き起こします。",
        "urgency": "normal",
    },
    # ---- NEW DISEASES BATCH 2 (Oncologic / Autoimmune / Toxicoses) ----
    {
        "name": "Thyroid Adenoma (Benign)",
        "name_ja": "甲状腺腺腫（良性）",
        "symptoms": {"lumps", "swelling", "difficulty_breathing", "coughing"},
        "description": "A benign thyroid gland tumor that may cause a visible neck mass and occasionally compress the trachea.",
        "description_ja": "甲状腺の良性腫瘍で、頸部の腫瘤が目に見え、時に気管を圧迫することがあります。",
        "urgency": "normal",
    },
    {
        "name": "Hepatic Lymphoma",
        "name_ja": "肝臓リンパ腫",
        "symptoms": {"lethargy", "appetite_loss", "weight_loss", "vomiting", "bloated_abdomen", "fever"},
        "description": "Lymphoma primarily affecting the liver, causing hepatomegaly, jaundice, and systemic illness.",
        "description_ja": "主に肝臓を侵すリンパ腫で、肝腫大、黄疸、全身性の病態を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Anal Gland Carcinoma",
        "name_ja": "肛門腺癌",
        "symptoms": {"constipation", "straining_urinate", "lethargy", "excessive_thirst", "weight_loss", "lumps"},
        "description": "Malignant tumor of the anal glands that often causes hypercalcemia and can metastasize to lymph nodes.",
        "description_ja": "肛門腺の悪性腫瘍で、高カルシウム血症を引き起こし、リンパ節に転移することがあります。",
        "urgency": "urgent",
    },
    {
        "name": "Chondrosarcoma",
        "name_ja": "軟骨肉腫",
        "symptoms": {"limping_fl", "limping_fr", "limping_rl", "limping_rr", "swelling", "pain_on_touch", "lumps"},
        "description": "A malignant tumor of cartilage that can occur in bones, nasal cavity, or ribs.",
        "description_ja": "軟骨の悪性腫瘍で、骨、鼻腔、または肋骨に発生することがあります。",
        "urgency": "urgent",
    },
    {
        "name": "Pulmonary Adenocarcinoma",
        "name_ja": "肺腺癌",
        "symptoms": {"coughing", "difficulty_breathing", "lethargy", "weight_loss", "appetite_loss", "rapid_breathing"},
        "description": "Primary lung cancer originating from the glandular tissue of the lung, causing chronic cough and respiratory distress.",
        "description_ja": "肺の腺組織から発生する原発性肺癌で、慢性咳嗽と呼吸困難を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Leiomyosarcoma (Intestinal)",
        "name_ja": "平滑筋肉腫（腸管）",
        "symptoms": {"vomiting", "diarrhea", "weight_loss", "appetite_loss", "bloody_stool", "lethargy"},
        "description": "A malignant smooth muscle tumor of the intestine causing GI obstruction, bleeding, and weight loss.",
        "description_ja": "腸管の悪性平滑筋腫瘍で、消化管閉塞、出血、体重減少を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Multiple Myeloma",
        "name_ja": "多発性骨髄腫",
        "symptoms": {"lethargy", "limping_fl", "limping_fr", "limping_rl", "limping_rr", "weight_loss", "excessive_thirst", "excessive_urination"},
        "description": "Cancer of plasma cells in bone marrow causing bone pain, kidney damage, and immunodeficiency.",
        "description_ja": "骨髄の形質細胞の癌で、骨痛、腎障害、免疫不全を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Meningioma",
        "name_ja": "髄膜腫",
        "symptoms": {"seizures", "circling", "head_tilting", "aggression_change", "lethargy"},
        "description": "A usually benign but space-occupying tumor of the meninges, the most common brain tumor in dogs.",
        "description_ja": "髄膜の通常は良性だが占拠性の腫瘍で、犬で最も一般的な脳腫瘍です。",
        "pathophysiology_ja": "くも膜キャップ細胞由来の腫瘍→脳表面からの外方発育→脳実質の圧排→頭蓋内圧亢進→けいれん・行動変化・神経学的欠損。犬の原発性脳腫瘍の45〜50%を占める最多腫瘍。多くは組織学的に良性（WHO Grade I）だが、占拠効果による神経障害が問題。前頭葉・嗅覚野に好発。犬の髄膜腫は猫と異なり浸潤性が高い傾向。",
        "causes_ja": "原因不明。長頭種（コリー・ゴールデンレトリーバー）に好発。中高齢犬（>7歳）。雌犬にやや多い。プロゲステロン受容体陽性のことがあり、ホルモン関与が示唆されるが未確定。",
        "prevention_ja": "確実な予防法はない。高齢犬の新規けいれん・行動変化はMRIで精査。外科的切除可能な部位では手術が第一選択（MST 7ヶ月〜2年）。放射線療法の併用で生存期間延長。定位放射線治療（SRS）が新しい選択肢。",
        "urgency": "urgent",
    },
    {
        "name": "Perianal Gland Adenocarcinoma",
        "name_ja": "肛門周囲腺癌",
        "symptoms": {"lumps", "constipation", "bloody_stool", "straining_urinate", "weight_loss"},
        "description": "Malignant perianal gland tumor, more common in neutered males; tends to invade locally and metastasize.",
        "description_ja": "肛門周囲腺の悪性腫瘍で、去勢した雄犬に多く、局所浸潤と転移の傾向があります。",
        "urgency": "urgent",
    },
    {
        "name": "Nasal Lymphoma",
        "name_ja": "鼻腔リンパ腫",
        "symptoms": {"nasal_discharge", "sneezing", "difficulty_breathing", "eye_discharge", "appetite_loss"},
        "description": "Lymphoma arising in the nasal cavity, causing chronic nasal discharge, epistaxis, and facial deformity.",
        "description_ja": "鼻腔に発生するリンパ腫で、慢性鼻汁、鼻出血、顔面変形を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Splenic Hemangiosarcoma",
        "name_ja": "脾臓血管肉腫",
        "symptoms": {"collapse", "lethargy", "bloated_abdomen", "rapid_breathing", "appetite_loss", "weight_loss"},
        "description": "A highly malignant tumor of the spleen's blood vessels that can rupture, causing life-threatening internal bleeding.",
        "description_ja": "脾臓の血管の高悪性度腫瘍で、破裂すると致死的な内出血を引き起こします。",
        "pathophysiology_ja": "血管内皮細胞由来の悪性腫瘍→脾臓内で血液充満腔を形成→破裂→致命的な腹腔内出血（血腹）→出血性ショック。早期に肝臓・肺・心臓に血行性転移（診断時に80%以上が転移あり）。DICの合併が高率。脾臓の腫瘤の2/3は血管肉腫（残り1/3は良性の血腫・結節性過形成）。",
        "causes_ja": "原因不明。大型犬（ゴールデンレトリーバー、ジャーマンシェパード、ラブラドール）に好発。中高齢犬（8〜12歳）。ゴールデンレトリーバーは生涯発症リスクが約20%。被毛色の薄い犬種にも多い。脾臓・右心房・皮下が好発部位。",
        "prevention_ja": "確実な予防法はない。好発犬種の中高齢期での定期的腹部エコー。突然の虚脱・腹部膨満は緊急受診。脾摘後のドキソルビシン併用化学療法でMST 4〜6ヶ月（脾摘のみでは1〜3ヶ月）。",
        "urgency": "emergency",
    },
    {
        "name": "Cardiac Hemangiosarcoma",
        "name_ja": "心臓血管肉腫",
        "symptoms": {"collapse", "difficulty_breathing", "lethargy", "rapid_breathing", "bloated_abdomen"},
        "description": "Hemangiosarcoma of the right atrium causing pericardial effusion, cardiac tamponade, and sudden collapse.",
        "description_ja": "右心房の血管肉腫で、心嚢液貯留、心タンポナーデ、突然の虚脱を引き起こします。",
        "urgency": "emergency",
    },
    # ---- Autoimmune ----
    {
        "name": "Immune-Mediated Neutropenia",
        "name_ja": "免疫介在性好中球減少症",
        "symptoms": {"fever", "lethargy", "appetite_loss", "skin_lesions", "swelling"},
        "description": "Immune destruction of neutrophils leading to severe susceptibility to bacterial infections.",
        "description_ja": "好中球の免疫介在性破壊で、細菌感染に対する重度の感受性を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Bullous Pemphigoid",
        "name_ja": "水疱性類天疱瘡",
        "symptoms": {"skin_lesions", "skin_redness", "itching", "hair_loss", "fever"},
        "description": "An autoimmune blistering skin disease where antibodies attack the basement membrane zone.",
        "description_ja": "抗体が基底膜帯を攻撃する自己免疫性水疱性皮膚疾患です。",
        "urgency": "urgent",
    },
    {
        "name": "Immune-Mediated Meningitis",
        "name_ja": "免疫介在性髄膜炎",
        "symptoms": {"fever", "pain_on_touch", "stiffness", "lethargy", "reluctance_move", "appetite_loss"},
        "description": "Non-infectious inflammation of the meninges caused by immune dysregulation, causing neck pain and fever.",
        "description_ja": "免疫調節障害による非感染性髄膜炎で、頸部痛と発熱を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Vogt-Koyanagi-Harada-like Syndrome (VKH)",
        "name_ja": "フォークト・小柳・原田様症候群",
        "symptoms": {"eye_redness", "squinting", "skin_lesions", "hair_loss", "eye_discharge"},
        "description": "An autoimmune disease targeting melanocytes causing uveitis, depigmentation of the nose and skin.",
        "description_ja": "メラノサイトを標的とする自己免疫疾患で、ぶどう膜炎と鼻・皮膚の色素脱失を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Cold Agglutinin Disease",
        "name_ja": "寒冷凝集素症",
        "symptoms": {"lethargy", "skin_lesions", "limping_fl", "limping_fr", "limping_rl", "limping_rr", "skin_redness"},
        "description": "An autoimmune condition where antibodies attack red blood cells at low temperatures, causing peripheral tissue necrosis.",
        "description_ja": "低温で赤血球を攻撃する抗体による自己免疫疾患で、末梢組織壊死を引き起こします。",
        "urgency": "urgent",
    },
    # ---- Toxicoses ----
    {
        "name": "Macadamia Nut Toxicosis",
        "name_ja": "マカダミアナッツ中毒",
        "symptoms": {"vomiting", "lethargy", "stiffness", "fever", "limping_rl", "limping_rr", "reluctance_move"},
        "description": "Ingestion of macadamia nuts causing weakness, vomiting, hyperthermia, and hind limb tremors in dogs.",
        "description_ja": "マカダミアナッツの摂取により犬に衰弱、嘔吐、高体温、後肢の震えを引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Ibuprofen Toxicosis",
        "name_ja": "イブプロフェン中毒",
        "symptoms": {"vomiting", "diarrhea", "appetite_loss", "bloody_stool", "lethargy", "excessive_thirst"},
        "description": "NSAID poisoning causing gastric ulceration, kidney failure, and potentially seizures at high doses.",
        "description_ja": "NSAIDの中毒で胃潰瘍、腎不全を引き起こし、高用量ではけいれんの可能性があります。",
        "urgency": "emergency",
    },
    {
        "name": "Acetaminophen Toxicosis",
        "name_ja": "アセトアミノフェン中毒",
        "symptoms": {"vomiting", "lethargy", "difficulty_breathing", "swelling", "drooling", "appetite_loss"},
        "description": "Tylenol poisoning causing methemoglobinemia, liver failure, and facial/paw edema in dogs.",
        "description_ja": "タイレノール中毒でメトヘモグロビン血症、肝不全、顔面・足の浮腫を引き起こします。",
        "pathophysiology_ja": "アセトアミノフェンの肝代謝→グルタチオン抱合能の飽和→毒性代謝物（NAPQI）の蓄積→(1)肝細胞壊死（小葉中心性壊死）→急性肝不全、(2)ヘモグロビンの酸化→メトヘモグロビン血症→チアノーゼ・チョコレート色粘膜、(3)赤血球内ハインツ小体形成→溶血。顔面・足の浮腫は犬に特徴的な症状。",
        "causes_ja": "ヒト用アセトアミノフェン（タイレノール・カロナール等）の誤食。毒性量：犬75mg/kg以上で肝障害、200mg/kgで致死的。配合鎮痛薬（カフェイン・コデイン含有）や風邪薬にも含まれるため注意。",
        "prevention_ja": "ヒト用薬のペットからの完全隔離、自己判断でのアセトアミノフェン投与禁止、薬品棚の施錠管理。犬にアセトアミノフェンを使用する場合は獣医師の処方下でのみ。",
        "urgency": "emergency",
    },
    {
        "name": "Mushroom Toxicosis",
        "name_ja": "キノコ中毒",
        "symptoms": {"vomiting", "diarrhea", "lethargy", "seizures", "drooling", "abdominal_pain", "collapse"},
        "description": "Ingestion of toxic mushrooms causing GI distress, liver failure, neurological signs, or death depending on species.",
        "description_ja": "有毒キノコの摂取により種類に応じて消化器症状、肝不全、神経症状、または死亡を引き起こします。",
        "pathophysiology_ja": "キノコ種により毒性メカニズムが異なる：(1)アマニタ属（テングタケ・ドクツルタケ）：アマトキシン→RNA ポリメラーゼII阻害→肝細胞壊死→急性肝不全（摂取6〜12時間後に発症、致死率50〜90%）、(2)ムスカリン含有種→副交感神経興奮（SLUDGE徴候）、(3)イボテン酸/ムシモール含有種→CNS症状（幻覚・運動失調・けいれん）、(4)消化器刺激型→嘔吐・下痢のみ。",
        "causes_ja": "庭・公園・散歩道に自生する野生キノコの摂取。犬は匂いに引かれて食べやすい。日本ではツキヨタケ・カエンタケ・ドクツルタケが特に危険。雨季・秋に発生増加。キノコの種同定が困難なため、野生キノコ摂取は全て中毒として対応すべき。",
        "prevention_ja": "庭・散歩道の野生キノコの定期除去、リードでの管理、拾い食い防止トレーニング。キノコ摂取が疑われた場合は種同定のため残存キノコを保存して受診。",
        "urgency": "emergency",
    },
    {
        "name": "Snail Bait (Metaldehyde) Poisoning",
        "name_ja": "ナメクジ駆除剤（メタアルデヒド）中毒",
        "symptoms": {"seizures", "excessive_panting", "drooling", "fever", "vomiting", "collapse"},
        "description": "Metaldehyde ingestion causing severe tremors, seizures, and hyperthermia that can be rapidly fatal.",
        "description_ja": "メタアルデヒドの摂取により重度の震え、けいれん、高体温を引き起こし、急速に致死的となります。",
        "pathophysiology_ja": "メタアルデヒドの代謝物アセトアルデヒド→脳内のGABA・セロトニン・ノルエピネフリン系の撹乱→重度の筋線維束攣縮・全身性けいれん→横紋筋融解→高体温（>41℃）→DIC・多臓器不全。摂取後1〜3時間で発症。致死量：100〜300mg/kg だが少量でも危険。",
        "causes_ja": "ナメクジ・カタツムリ駆除剤（メタアルデヒドペレット）の摂取。ペレットはしばしば穀物基材で犬にとって嗜好性が高い。日本の家庭菜園・庭園で広く使用。雨季（梅雨・秋）に使用頻度増加。",
        "prevention_ja": "ペットがアクセスできない場所での駆除剤使用、鉄リン酸塩ベースの代替品（ペットに安全）の使用推奨、庭への犬の立入制限。",
        "urgency": "emergency",
    },
    {
        "name": "Lily Toxicosis",
        "name_ja": "ユリ中毒",
        "symptoms": {"vomiting", "lethargy", "appetite_loss", "excessive_thirst", "dehydration"},
        "description": "While more dangerous to cats, certain lily species can cause GI upset in dogs; peace lilies cause oral irritation.",
        "description_ja": "猫にはより危険ですが、特定のユリ種は犬に消化器症状を引き起こし、スパティフィラムは口腔刺激を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Sago Palm Toxicosis",
        "name_ja": "ソテツ中毒",
        "symptoms": {"vomiting", "diarrhea", "lethargy", "bloody_stool", "appetite_loss", "bloated_abdomen", "seizures"},
        "description": "Ingestion of any part of the sago palm, especially seeds, causing severe liver failure in dogs.",
        "description_ja": "ソテツの種子を含むあらゆる部位の摂取により犬に重度の肝不全を引き起こします。",
        "pathophysiology_ja": "ソテツ全部位に含まれるサイカシン（cycasin）→肝臓でメチルアゾキシメタノール（MAM）に代謝→肝細胞のDNAアルキル化→小葉中心性〜びまん性肝壊死→急性肝不全。種子（ナッツ）に最も高濃度。摂取後15分〜数時間で嘔吐開始、24〜72時間で肝不全が進行。致死率50%以上。",
        "causes_ja": "ソテツ（Cycas revoluta）の種子・葉・根の摂取。観葉植物・庭園に広く栽培。日本では九州・沖縄に自生するが、全国で観葉植物として流通。種子1〜2個の摂取でも致死的。犬は種子を噛んで遊ぶことがある。",
        "prevention_ja": "犬がアクセスできる場所へのソテツ植栽の回避、落果の即時除去、屋内観葉ソテツの犬の届かない場所への配置。犬のいる家庭ではソテツの栽培を避けることが最善。",
        "urgency": "emergency",
    },
    {
        "name": "Blue-Green Algae (Cyanobacteria) Toxicosis",
        "name_ja": "藍藻（シアノバクテリア）中毒",
        "symptoms": {"vomiting", "diarrhea", "seizures", "collapse", "lethargy", "drooling", "difficulty_breathing"},
        "description": "Exposure to cyanotoxins in stagnant water causing rapid onset liver failure or neurotoxicity.",
        "description_ja": "停滞水中のシアノトキシンへの曝露により急速に肝不全または神経毒性を引き起こします。",
        "urgency": "emergency",
    },
    {
        "name": "Permethrin Toxicosis",
        "name_ja": "ペルメトリン中毒",
        "symptoms": {"seizures", "drooling", "stiffness", "vomiting", "fever", "excessive_panting"},
        "description": "Toxicity from concentrated permethrin products (typically cat flea products applied to dogs at high doses).",
        "description_ja": "高濃度ペルメトリン製品による中毒（通常は猫用ノミ製品を犬に高用量で適用した場合）。",
        "urgency": "emergency",
    },
    {
        "name": "Caffeine Toxicosis",
        "name_ja": "カフェイン中毒",
        "symptoms": {"vomiting", "excessive_panting", "rapid_breathing", "seizures", "excessive_thirst", "excessive_urination"},
        "description": "Caffeine ingestion causing hyperactivity, tachycardia, tremors, seizures, and potentially cardiac arrest.",
        "description_ja": "カフェインの摂取により多動、頻脈、震え、けいれん、心停止の可能性を引き起こします。",
        "pathophysiology_ja": "カフェイン（メチルキサンチン）→ホスホジエステラーゼ阻害→cAMP上昇→心筋興奮性亢進・平滑筋弛緩。アデノシン受容体拮抗→CNS興奮（落ち着きのなさ・振戦・けいれん）。カテコラミン放出促進→頻脈・不整脈。犬の半減期は4.5時間。致死量は犬で140〜150mg/kg。",
        "causes_ja": "コーヒー豆・茶葉・エナジードリンク・カフェイン錠剤・ダイエットサプリメントの摂取。コーヒー粕（庭の堆肥利用）の誤食も多い。チョコレートにもカフェインが含まれるため複合中毒に注意。",
        "prevention_ja": "コーヒー豆・茶葉・カフェイン含有製品のペットからの隔離、コーヒー粕の堆肥利用時の犬のアクセス制限、エナジードリンクの放置禁止。",
        "urgency": "emergency",
    },
    {
        "name": "Corn Cob Foreign Body",
        "name_ja": "トウモロコシの芯の異物",
        "symptoms": {"vomiting", "appetite_loss", "lethargy", "abdominal_pain", "constipation", "dehydration"},
        "description": "Ingested corn cob causing intestinal obstruction; corn cobs do not digest and require surgical removal.",
        "description_ja": "トウモロコシの芯の摂取による腸閉塞で、消化されないため外科的除去が必要です。",
        "urgency": "emergency",
    },
    # ---- Parasitic ----
    {
        "name": "Cuterebra Infestation",
        "name_ja": "ウマバエ幼虫症",
        "symptoms": {"swelling", "skin_lesions", "lumps", "lethargy", "fever"},
        "description": "Botfly larval infestation causing a cyst-like swelling with a breathing pore, usually on the head or neck.",
        "description_ja": "ウマバエ幼虫の寄生により頭部や頸部に呼吸孔を持つ嚢胞様腫脹を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Toxascaris Infection",
        "name_ja": "トキサスカリス感染症",
        "symptoms": {"diarrhea", "vomiting", "weight_loss", "bloated_abdomen", "appetite_loss"},
        "description": "Intestinal infection with Toxascaris leonina roundworms causing malnutrition in puppies and adult dogs.",
        "description_ja": "トキサスカリス回虫による腸管感染で、子犬と成犬に栄養不良を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Spirocerca lupi Infection",
        "name_ja": "食道虫症",
        "symptoms": {"vomiting", "regurgitation", "weight_loss", "coughing", "difficulty_breathing"},
        "description": "Esophageal worm infection forming granulomas that can transform into sarcomas; endemic in warm climates.",
        "description_ja": "食道に肉芽腫を形成する食道虫感染で、肉腫に変化する可能性があり、温暖な気候で流行します。",
        "urgency": "urgent",
    },
    {
        "name": "Lungworm (Angiostrongylus vasorum)",
        "name_ja": "肺虫症（アンギオストロンギルス）",
        "symptoms": {"coughing", "difficulty_breathing", "lethargy", "weight_loss", "bloody_stool", "collapse"},
        "description": "Parasitic worm living in the pulmonary arteries and heart, causing coagulopathy, coughing, and potentially fatal bleeding.",
        "description_ja": "肺動脈と心臓に寄生する線虫で、凝固障害、咳嗽、致死的出血を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Thelazia Eye Worm",
        "name_ja": "眼虫症（テラジア）",
        "symptoms": {"eye_redness", "eye_discharge", "squinting", "itching"},
        "description": "Parasitic nematode found in the conjunctival sac, transmitted by fruit flies, causing conjunctivitis.",
        "description_ja": "ショウジョウバエにより伝播される結膜嚢内に寄生する線虫で、結膜炎を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Canine Schistosomiasis",
        "name_ja": "犬住血吸虫症",
        "symptoms": {"diarrhea", "bloody_stool", "weight_loss", "lethargy", "vomiting", "fever"},
        "description": "Blood fluke infection causing granulomatous inflammation of the intestines and liver.",
        "description_ja": "住血吸虫の感染により腸管と肝臓の肉芽腫性炎症を引き起こします。",
        "urgency": "urgent",
    },
    # ---- Congenital / Breed-Specific ----
    {
        "name": "Portosystemic Shunt (Acquired)",
        "name_ja": "後天性門脈体循環シャント",
        "symptoms": {"lethargy", "seizures", "vomiting", "appetite_loss", "excessive_thirst", "excessive_urination", "circling"},
        "description": "Acquired abnormal blood vessels bypassing the liver, usually secondary to chronic liver disease and portal hypertension.",
        "description_ja": "慢性肝疾患と門脈圧亢進症に続発する後天性の肝臓を迂回する異常血管です。",
        "urgency": "urgent",
    },
    {
        "name": "Ciliary Dyskinesia (Primary)",
        "name_ja": "原発性線毛機能不全症",
        "symptoms": {"nasal_discharge", "coughing", "sneezing", "difficulty_breathing", "lethargy"},
        "description": "A congenital defect in cilia function causing chronic respiratory infections and sometimes situs inversus.",
        "description_ja": "線毛機能の先天性欠陥で、慢性呼吸器感染症と時に内臓逆位を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Pulmonic Valve Dysplasia",
        "name_ja": "肺動脈弁形成不全",
        "symptoms": {"lethargy", "collapse", "difficulty_breathing", "bloated_abdomen", "coughing"},
        "description": "Congenital malformation of the pulmonic valve causing right ventricular outflow obstruction.",
        "description_ja": "肺動脈弁の先天性奇形で右心室流出路閉塞を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Mitral Valve Dysplasia",
        "name_ja": "僧帽弁形成不全",
        "symptoms": {"coughing", "difficulty_breathing", "lethargy", "collapse", "rapid_breathing"},
        "description": "Congenital malformation of the mitral valve causing mitral regurgitation and left heart failure in young dogs.",
        "description_ja": "僧帽弁の先天性奇形で僧帽弁逆流と若い犬の左心不全を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Phosphofructokinase (PFK) Deficiency",
        "name_ja": "ホスホフルクトキナーゼ欠損症",
        "symptoms": {"lethargy", "fever", "weight_loss", "blood_urine", "excessive_panting"},
        "description": "A hereditary enzyme deficiency in English Springer Spaniels and Cocker Spaniels causing hemolytic crises.",
        "description_ja": "イングリッシュスプリンガースパニエルやコッカースパニエルの遺伝性酵素欠損症で、溶血性発作を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Pyruvate Kinase Deficiency",
        "name_ja": "ピルビン酸キナーゼ欠損症",
        "symptoms": {"lethargy", "weight_loss", "excessive_panting", "fever", "appetite_loss"},
        "description": "Hereditary red blood cell enzyme deficiency causing chronic hemolytic anemia, seen in Basenjis and Beagles.",
        "description_ja": "バセンジーやビーグルに見られる遺伝性赤血球酵素欠損症で、慢性溶血性貧血を引き起こします。",
        "urgency": "urgent",
    },
    # ---- NEW DISEASES BATCH 3 (GI / Respiratory / Urogenital / Behavioral) ----
    {
        "name": "Gastric Carcinoma",
        "name_ja": "胃癌",
        "symptoms": {"vomiting", "weight_loss", "appetite_loss", "lethargy", "bloody_stool", "abdominal_pain"},
        "description": "Malignant stomach tumor causing chronic vomiting, weight loss, and GI bleeding; poor prognosis.",
        "description_ja": "慢性嘔吐、体重減少、消化管出血を引き起こす胃の悪性腫瘍で、予後は不良です。",
        "urgency": "urgent",
    },
    {
        "name": "Intestinal Adenocarcinoma",
        "name_ja": "腸腺癌",
        "symptoms": {"vomiting", "diarrhea", "weight_loss", "appetite_loss", "bloody_stool", "lethargy"},
        "description": "Malignant tumor of the intestinal lining, most common in the colon and duodenum of older dogs.",
        "description_ja": "腸管内壁の悪性腫瘍で、高齢犬の結腸と十二指腸に最も多く見られます。",
        "urgency": "urgent",
    },
    {
        "name": "Pyloric Stenosis",
        "name_ja": "幽門狭窄症",
        "symptoms": {"vomiting", "vomiting_after_drinking", "weight_loss", "appetite_loss", "dehydration"},
        "description": "Narrowing of the pyloric outflow of the stomach causing projectile vomiting, seen in brachycephalic breeds.",
        "description_ja": "胃の幽門部の狭窄で噴出性嘔吐を引き起こし、短頭種に多く見られます。",
        "urgency": "urgent",
    },
    {
        "name": "Gallbladder Mucocele",
        "name_ja": "胆嚢粘液嚢腫",
        "symptoms": {"vomiting", "appetite_loss", "lethargy", "abdominal_pain", "fever", "bloated_abdomen"},
        "description": "Abnormal accumulation of thick mucus in the gallbladder that can lead to rupture and bile peritonitis.",
        "description_ja": "胆嚢内の異常な粘液蓄積で、破裂と胆汁性腹膜炎を引き起こす可能性があります。",
        "pathophysiology_ja": "胆嚢粘膜上皮の異常なムチン過分泌→半固形の粘液物質が胆嚢内に蓄積→胆嚢壁の伸展・菲薄化→胆嚢壁壊死→破裂→胆汁性腹膜炎（致死的）。エコーで「キウイフルーツ様」の特徴的パターン。胆管閉塞→閉塞性黄疸も起こりうる。高脂血症・甲状腺機能低下症・クッシング症候群との関連が報告。",
        "causes_ja": "原因不明だが、胆嚢運動障害・胆汁組成の変化・ABCB4遺伝子変異が関与。高脂血症・甲状腺機能低下症・クッシング症候群が基礎にあることが多い。好発犬種：シェルティ、コッカースパニエル、ミニチュアシュナウザー、ポメラニアン。中高齢犬。",
        "prevention_ja": "確実な予防法はない。高脂血症の管理（低脂肪食）、甲状腺機能低下症の治療。定期的な腹部エコーで早期発見。無症状でも粘液嚢腫が確認された場合は予防的胆嚢摘出を検討。",
        "urgency": "emergency",
    },
    {
        "name": "Cholangitis/Cholangiohepatitis",
        "name_ja": "胆管炎/胆管肝炎",
        "symptoms": {"vomiting", "appetite_loss", "fever", "lethargy", "abdominal_pain", "weight_loss"},
        "description": "Inflammation of the bile ducts and liver causing fever, jaundice, and abdominal pain.",
        "description_ja": "胆管と肝臓の炎症で、発熱、黄疸、腹痛を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Chronic Hepatitis",
        "name_ja": "慢性肝炎",
        "symptoms": {"lethargy", "appetite_loss", "weight_loss", "vomiting", "excessive_thirst", "excessive_urination", "bloated_abdomen"},
        "description": "Progressive inflammatory liver disease causing fibrosis and eventually cirrhosis; certain breeds are predisposed.",
        "description_ja": "線維化と最終的に肝硬変を引き起こす進行性の炎症性肝疾患で、特定の犬種に好発します。",
        "pathophysiology_ja": "持続的な肝細胞炎症→ステラート細胞の活性化→コラーゲン沈着（線維化）→肝硬変→門脈圧亢進→腹水。肝細胞の大量喪失→肝不全（低アルブミン血症・凝固障害・肝性脳症・黄疸）。銅蓄積性肝炎では銅によるフリーラジカル産生が病態の根幹。",
        "causes_ja": "銅蓄積性肝炎（ベドリントンテリア：COMMD1遺伝子変異、ラブラドール、ドーベルマン、WHWT）、免疫介在性、薬剤性、感染後。ベドリントンテリアでは遺伝子検査が可能。",
        "prevention_ja": "好発犬種の遺伝子検査（COMMD1）と繁殖管理、銅制限食、定期的な肝酵素モニタリング、銅キレート剤（D-ペニシラミン）の早期投与。",
        "urgency": "urgent",
    },
    {
        "name": "Hepatic Lipidosis",
        "name_ja": "肝リピドーシス",
        "symptoms": {"appetite_loss", "lethargy", "vomiting", "weight_loss", "bloated_abdomen"},
        "description": "Excessive fat accumulation in the liver causing hepatic dysfunction, often secondary to other diseases.",
        "description_ja": "肝臓への過剰な脂肪蓄積で肝機能障害を引き起こし、他の疾患に続発することが多いです。",
        "urgency": "urgent",
    },
    {
        "name": "Small Intestinal Bacterial Overgrowth (SIBO)",
        "name_ja": "小腸細菌過増殖症",
        "symptoms": {"diarrhea", "weight_loss", "excessive_gas", "appetite_increase", "bloated_abdomen"},
        "description": "Excessive bacterial colonization of the small intestine causing malabsorption and chronic diarrhea.",
        "description_ja": "小腸の過剰な細菌増殖による吸収不良と慢性下痢を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Antibiotic-Responsive Diarrhea",
        "name_ja": "抗生物質反応性下痢",
        "symptoms": {"diarrhea", "weight_loss", "excessive_gas", "appetite_loss", "lethargy"},
        "description": "Chronic small bowel diarrhea responsive to antibiotic therapy, possibly related to dysbiosis.",
        "description_ja": "抗生物質療法に反応する慢性小腸性下痢で、腸内細菌叢の不均衡に関連する可能性があります。",
        "urgency": "normal",
    },
    {
        "name": "Lymphangiectasia",
        "name_ja": "リンパ管拡張症",
        "symptoms": {"diarrhea", "weight_loss", "bloated_abdomen", "lethargy", "appetite_loss", "vomiting"},
        "description": "Dilation of intestinal lymphatic vessels causing protein-losing enteropathy and malabsorption.",
        "description_ja": "腸リンパ管の拡張による蛋白漏出性腸症と吸収不良を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Esophageal Stricture",
        "name_ja": "食道狭窄",
        "symptoms": {"regurgitation", "drooling", "weight_loss", "appetite_loss", "vomiting_after_drinking"},
        "description": "Narrowing of the esophagus due to scarring from foreign bodies, caustic substances, or anesthesia reflux.",
        "description_ja": "異物、腐食性物質、麻酔時逆流による瘢痕で食道が狭窄した状態です。",
        "urgency": "urgent",
    },
    {
        "name": "Gastroesophageal Reflux Disease (GERD)",
        "name_ja": "胃食道逆流症",
        "symptoms": {"regurgitation", "drooling", "vomiting_after_drinking", "appetite_loss", "excessive_gas"},
        "description": "Chronic reflux of gastric contents into the esophagus causing esophagitis and discomfort.",
        "description_ja": "胃内容物の食道への慢性的逆流により食道炎と不快感を引き起こします。",
        "urgency": "normal",
    },
    # ---- Respiratory ----
    {
        "name": "Pulmonary Thromboembolism (PTE)",
        "name_ja": "肺血栓塞栓症",
        "symptoms": {"difficulty_breathing", "rapid_breathing", "collapse", "coughing", "lethargy", "excessive_panting"},
        "description": "Blood clot in the pulmonary arteries causing acute respiratory distress; often secondary to other conditions.",
        "description_ja": "肺動脈の血栓による急性呼吸困難で、他の疾患に続発することが多いです。",
        "urgency": "emergency",
    },
    {
        "name": "Eosinophilic Bronchopneumopathy",
        "name_ja": "好酸球性気管支肺症",
        "symptoms": {"coughing", "difficulty_breathing", "nasal_discharge", "lethargy", "rapid_breathing"},
        "description": "Allergic lung disease with eosinophilic infiltration causing chronic cough and breathing difficulty.",
        "description_ja": "好酸球浸潤を伴うアレルギー性肺疾患で、慢性咳嗽と呼吸困難を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Lung Lobe Consolidation",
        "name_ja": "肺葉硬化",
        "symptoms": {"coughing", "difficulty_breathing", "fever", "lethargy", "appetite_loss", "nasal_discharge"},
        "description": "Replacement of air in lung tissue with fluid, pus, or cellular infiltrate from severe infection or inflammation.",
        "description_ja": "重度の感染や炎症による肺組織の空気が液体、膿、細胞浸潤で置換された状態です。",
        "urgency": "urgent",
    },
    {
        "name": "Nasopharyngeal Polyp",
        "name_ja": "鼻咽頭ポリープ",
        "symptoms": {"snoring", "nasal_discharge", "sneezing", "difficulty_breathing", "reverse_sneezing"},
        "description": "A benign growth in the nasopharynx causing upper airway obstruction, snoring, and nasal discharge.",
        "description_ja": "鼻咽頭の良性腫瘤で、上気道閉塞、いびき、鼻汁を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Allergic Rhinitis",
        "name_ja": "アレルギー性鼻炎",
        "symptoms": {"sneezing", "nasal_discharge", "reverse_sneezing", "itching", "eye_discharge"},
        "description": "Seasonal or perennial allergic inflammation of the nasal passages causing sneezing and clear nasal discharge.",
        "description_ja": "鼻腔の季節性または通年性アレルギー性炎症で、くしゃみと透明な鼻汁を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Tracheal Foreign Body",
        "name_ja": "気管異物",
        "symptoms": {"coughing", "difficulty_breathing", "rapid_breathing", "drooling", "excessive_panting"},
        "description": "Foreign object lodged in the trachea causing acute respiratory distress and violent coughing.",
        "description_ja": "気管内に異物が嵌頓し、急性呼吸困難と激しい咳嗽を引き起こします。",
        "urgency": "emergency",
    },
    # ---- Urogenital ----
    {
        "name": "Renal Dysplasia",
        "name_ja": "腎形成不全",
        "symptoms": {"excessive_thirst", "excessive_urination", "weight_loss", "vomiting", "lethargy", "dehydration"},
        "description": "Abnormal kidney development causing early-onset chronic kidney failure in young dogs.",
        "description_ja": "腎臓の異常発達で若い犬に早期発症の慢性腎不全を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Renal Amyloidosis",
        "name_ja": "腎アミロイドーシス",
        "symptoms": {"excessive_thirst", "excessive_urination", "weight_loss", "lethargy", "vomiting", "bloated_abdomen"},
        "description": "Deposition of amyloid protein in the kidneys causing progressive renal failure; seen in Shar Peis.",
        "description_ja": "腎臓へのアミロイド蛋白沈着で進行性腎不全を引き起こし、シャーペイに多く見られます。",
        "urgency": "urgent",
    },
    {
        "name": "Nephrolithiasis (Kidney Stones)",
        "name_ja": "腎結石症",
        "symptoms": {"blood_urine", "straining_urinate", "vomiting", "abdominal_pain", "lethargy"},
        "description": "Mineral stones in the kidney pelvis that can cause obstruction, infection, and chronic kidney damage.",
        "description_ja": "腎盂の鉱物結石で、閉塞、感染、慢性腎障害を引き起こす可能性があります。",
        "urgency": "urgent",
    },
    {
        "name": "Urethral Prolapse",
        "name_ja": "尿道脱",
        "symptoms": {"blood_urine", "genital_discharge", "straining_urinate", "excessive_urination"},
        "description": "Protrusion of urethral mucosa beyond the external urethral orifice, seen in young male English Bulldogs.",
        "description_ja": "尿道粘膜が外尿道口を超えて突出する状態で、若い雄のイングリッシュブルドッグに見られます。",
        "urgency": "urgent",
    },
    {
        "name": "Uterine Stump Pyometra",
        "name_ja": "子宮断端蓄膿症",
        "symptoms": {"fever", "lethargy", "genital_discharge", "vomiting", "excessive_thirst", "appetite_loss"},
        "description": "Infection of residual uterine tissue after spay surgery, mimicking pyometra in a spayed dog.",
        "description_ja": "避妊手術後の残存子宮組織の感染で、避妊済みの犬に子宮蓄膿症様の症状を引き起こします。",
        "pathophysiology_ja": "卵巣摘出不全（卵巣遺残症候群、ORS）→残存卵巣組織からのプロゲステロン分泌→残存子宮断端の嚢胞性内膜過形成→細菌感染→蓄膿。または卵巣は完全摘出されたが子宮断端組織が長めに残存→慢性的な炎症→二次感染。避妊後数ヶ月〜数年で発症しうる。",
        "causes_ja": "避妊手術時の卵巣遺残（ORS、最も多い原因）、子宮断端の過剰残存、術後の縫合部汚染。外因性プロゲステロン投与後にも発症しうる。避妊済み犬の膣分泌物・発情徴候がある場合にORS/断端蓄膿を疑う。",
        "prevention_ja": "卵巣の完全摘出（避妊手術時の確実な卵巣同定）、子宮断端の最小化、無菌手術手技の徹底。避妊済み犬の発情徴候（陰部腫脹・分泌物）は早期に精査。",
        "urgency": "emergency",
    },
    {
        "name": "Testicular Torsion",
        "name_ja": "精巣捻転",
        "symptoms": {"pain_on_touch", "vomiting", "lethargy", "swelling", "fever"},
        "description": "Rotation of the testicle cutting off blood supply, causing acute pain; more common with retained testes.",
        "description_ja": "精巣の回転により血液供給が遮断され急性痛を引き起こし、停留精巣でより多く見られます。",
        "urgency": "emergency",
    },
    {
        "name": "Penile/Preputial Tumor",
        "name_ja": "陰茎/包皮腫瘍",
        "symptoms": {"genital_discharge", "blood_urine", "lumps", "straining_urinate"},
        "description": "Tumors of the penis or prepuce including transmissible venereal tumor (TVT) and squamous cell carcinoma.",
        "description_ja": "可移植性性器腫瘍（TVT）や扁平上皮癌を含む陰茎または包皮の腫瘍です。",
        "urgency": "urgent",
    },
    # ---- Behavioral ----
    {
        "name": "Fear Aggression",
        "name_ja": "恐怖性攻撃行動",
        "symptoms": {"aggression_change", "anxiety", "hiding", "excessive_panting"},
        "description": "Defensive aggression triggered by fear of perceived threats, often worsened by punitive training methods.",
        "description_ja": "脅威と感じるものへの恐怖により引き起こされる防御的攻撃行動で、罰を用いた訓練により悪化します。",
        "pathophysiology_ja": "恐怖刺激→扁桃体の過剰活性化→闘争-逃走反応（交感神経系亢進）→逃走不可能な状況で防御的攻撃に転化。警告段階（耳の後方、尾を巻く、唇を舐める）→escalation（唸り・歯をむく）→咬傷。罰による抑圧は警告シグナルを消去し、予測不能な咬傷のリスクを増大させる。",
        "causes_ja": "社会化不足（子犬期の社会化臨界期3〜14週齢の経験不足）、過去のトラウマ体験、罰を用いた訓練、遺伝的気質（不安傾向の強い犬種）、疼痛。痛みが基礎にある場合は身体的原因の精査が先決。",
        "prevention_ja": "子犬期の適切な社会化プログラム（3〜14週齢に多様な人・犬・環境への段階的暴露）、陽性強化トレーニング（罰の回避）、恐怖反応の初期段階での行動学的介入。",
        "urgency": "normal",
    },
    {
        "name": "Resource Guarding",
        "name_ja": "資源防衛行動",
        "symptoms": {"aggression_change", "anxiety"},
        "description": "Aggressive behavior when a dog protects food, toys, or resting spots from people or other animals.",
        "description_ja": "食物、おもちゃ、休息場所を人や他の動物から守る際の攻撃的行動です。",
        "urgency": "normal",
    },
    {
        "name": "Storm/Noise Anxiety",
        "name_ja": "雷/騒音不安症",
        "symptoms": {"anxiety", "hiding", "excessive_panting", "drooling", "incontinence"},
        "description": "Extreme fear response to thunderstorms, fireworks, or other loud noises causing panic and destructive behavior.",
        "description_ja": "雷雨、花火、その他の大きな音に対する極度の恐怖反応でパニックと破壊的行動を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Canine Fly-Snapping Syndrome",
        "name_ja": "犬ハエ追い症候群",
        "symptoms": {"anxiety", "circling", "aggression_change", "seizures"},
        "description": "Repetitive snapping at imaginary flies, possibly related to partial seizures or compulsive disorder.",
        "description_ja": "想像上のハエを繰り返し噛む行動で、部分発作や強迫性障害に関連する可能性があります。",
        "urgency": "normal",
    },
    {
        "name": "Territorial Aggression",
        "name_ja": "縄張り性攻撃行動",
        "symptoms": {"aggression_change", "anxiety", "excessive_panting"},
        "description": "Aggressive behavior directed at people or animals entering the dog's perceived territory.",
        "description_ja": "犬が認識する縄張りに侵入する人や動物に向けられた攻撃的行動です。",
        "urgency": "normal",
    },
    {
        "name": "Hyperkinesis (Canine ADHD)",
        "name_ja": "過活動症（犬のADHD）",
        "symptoms": {"anxiety", "excessive_panting", "aggression_change", "rapid_breathing"},
        "description": "True hyperactivity disorder characterized by inability to habituate, elevated heart rate, and response to stimulants.",
        "description_ja": "慣れることができず、心拍数の上昇、興奮剤への反応を特徴とする真の過活動障害です。",
        "urgency": "normal",
    },
    # ---- Infectious ----
    {
        "name": "Canine Adenovirus Type 1 (CAV-1)",
        "name_ja": "犬アデノウイルス1型",
        "symptoms": {"fever", "lethargy", "appetite_loss", "vomiting", "bloated_abdomen", "eye_redness"},
        "description": "Infectious canine hepatitis virus causing liver inflammation, corneal edema ('blue eye'), and coagulopathy.",
        "description_ja": "犬伝染性肝炎ウイルスで肝臓の炎症、角膜浮腫（ブルーアイ）、凝固障害を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Canine Parainfluenza Virus",
        "name_ja": "犬パラインフルエンザウイルス",
        "symptoms": {"coughing", "sneezing", "nasal_discharge", "lethargy", "fever"},
        "description": "A common respiratory virus contributing to kennel cough complex, causing mild upper respiratory signs.",
        "description_ja": "ケンネルコフ複合体の一因となる一般的な呼吸器ウイルスで、軽度の上部呼吸器症状を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Canine Respiratory Coronavirus",
        "name_ja": "犬呼吸器コロナウイルス",
        "symptoms": {"coughing", "sneezing", "nasal_discharge", "lethargy"},
        "description": "A respiratory pathogen contributing to infectious respiratory disease complex in dogs.",
        "description_ja": "犬の感染性呼吸器疾患複合体の一因となる呼吸器病原体です。",
        "urgency": "normal",
    },
    {
        "name": "Streptococcal Toxic Shock Syndrome",
        "name_ja": "連鎖球菌性毒素性ショック症候群",
        "symptoms": {"fever", "collapse", "rapid_breathing", "lethargy", "vomiting", "skin_redness", "pain_on_touch"},
        "description": "Rapidly progressive systemic infection causing septic shock, organ failure, and necrotizing fasciitis.",
        "description_ja": "敗血症性ショック、臓器不全、壊死性筋膜炎を引き起こす急速進行性の全身感染症です。",
        "urgency": "emergency",
    },
    {
        "name": "Pythiosis",
        "name_ja": "ピシウム症",
        "symptoms": {"vomiting", "diarrhea", "weight_loss", "bloody_stool", "skin_lesions", "lethargy"},
        "description": "Infection by the aquatic oomycete Pythium insidiosum causing GI or cutaneous disease, common in the Gulf states.",
        "description_ja": "水生卵菌ピシウムによる感染で消化管または皮膚疾患を引き起こし、湾岸諸州に多いです。",
        "urgency": "urgent",
    },
    {
        "name": "Protothecosis",
        "name_ja": "プロトテカ症",
        "symptoms": {"diarrhea", "bloody_stool", "eye_redness", "weight_loss", "lethargy", "skin_lesions"},
        "description": "Rare infection by achlorophyllous algae causing chronic hemorrhagic diarrhea and disseminated disease.",
        "description_ja": "無葉緑素藻類による稀な感染で、慢性出血性下痢と播種性疾患を引き起こします。",
        "urgency": "urgent",
    },
    # ---- NEW DISEASES BATCH 4 (Mixed categories to reach 450+) ----
    {
        "name": "Hepatic Abscess",
        "name_ja": "肝膿瘍",
        "symptoms": {"fever", "lethargy", "appetite_loss", "vomiting", "abdominal_pain", "bloated_abdomen"},
        "description": "Focal collection of pus within the liver parenchyma, usually from ascending biliary or hematogenous infection.",
        "description_ja": "肝実質内の局所的な膿の集積で、通常は上行性胆道感染または血行性感染が原因です。",
        "urgency": "urgent",
    },
    {
        "name": "Splenic Torsion",
        "name_ja": "脾捻転",
        "symptoms": {"vomiting", "bloated_abdomen", "lethargy", "collapse", "abdominal_pain"},
        "description": "Twisting of the spleen on its vascular pedicle causing acute ischemia and potentially splenic necrosis.",
        "description_ja": "脾臓が血管茎で捻転し、急性虚血と脾壊死を引き起こす可能性があります。",
        "urgency": "emergency",
    },
    {
        "name": "Diaphragmatic Hernia",
        "name_ja": "横隔膜ヘルニア",
        "symptoms": {"difficulty_breathing", "rapid_breathing", "vomiting", "lethargy", "appetite_loss"},
        "description": "Tear in the diaphragm allowing abdominal organs to enter the chest cavity, usually from trauma.",
        "description_ja": "横隔膜の裂傷により腹腔臓器が胸腔に侵入する状態で、通常は外傷が原因です。",
        "pathophysiology_ja": "外傷性（最多）：交通事故・落下→横隔膜破裂→腹腔臓器（肝臓・胃・腸管・脾臓）の胸腔内脱出→肺圧排→換気障害→呼吸窮迫。先天性（心膜腹膜横隔膜ヘルニア：PPDH）は心嚢と腹腔が交通。胃の胸腔内嵌頓→GDV様の急性虚血→致死的。慢性例は無症状で偶然発見されることもある。",
        "causes_ja": "外傷性（交通事故・落下・腹部の鈍的外傷：80%以上）。先天性PPDH（ウェイマラナー・コッカースパニエルに報告）。腹腔内圧の急上昇（過度のいきみ等）も原因。多臓器外傷の合併が多い。",
        "prevention_ja": "交通事故の防止（リードでの管理・柵付き庭）、外傷の予防。外傷犬は胸部X線で横隔膜の連続性を確認。安定化後に外科的整復。",
        "urgency": "emergency",
    },
    {
        "name": "Perineal Hernia",
        "name_ja": "会陰ヘルニア",
        "symptoms": {"constipation", "straining_urinate", "swelling", "lethargy", "pain_on_touch"},
        "description": "Weakening of the pelvic diaphragm muscles allowing herniation of pelvic/abdominal contents, common in intact males.",
        "description_ja": "骨盤隔膜筋の衰弱により骨盤・腹腔内容がヘルニアする状態で、未去勢の雄犬に多いです。",
        "pathophysiology_ja": "骨盤隔膜の筋群（尾骨筋・肛門挙筋）のテストステロン依存性萎縮→骨盤腔の支持構造の脆弱化→直腸・膀胱・前立腺・腹腔脂肪の会陰部への脱出。直腸の偏位→排便困難。膀胱の後方脱出（retroflexion）→尿路閉塞（緊急）。両側性が多い。",
        "causes_ja": "未去勢雄犬（テストステロン依存性筋萎縮）。中高齢犬（7〜9歳）に好発。前立腺肥大の合併が多い。好発犬種：コーギー、ボストンテリア、コリー、ボクサー、ペキニーズ。稀に雌犬でも発症。",
        "prevention_ja": "去勢手術（テストステロン依存性萎縮の予防、前立腺縮小）。前立腺肥大の管理。片側発症後の対側発症リスクが高い。外科的修復時の同時去勢が強く推奨。",
        "urgency": "urgent",
    },
    {
        "name": "Inguinal Hernia",
        "name_ja": "鼠径ヘルニア",
        "symptoms": {"swelling", "pain_on_touch", "vomiting", "lethargy"},
        "description": "Protrusion of abdominal contents through the inguinal canal; may become strangulated requiring emergency surgery.",
        "description_ja": "鼠径管を通じた腹腔内容の突出で、絞扼され緊急手術が必要になることがあります。",
        "urgency": "urgent",
    },
    {
        "name": "Umbilical Hernia",
        "name_ja": "臍ヘルニア",
        "symptoms": {"swelling", "lumps"},
        "description": "Congenital defect where abdominal contents protrude through an incomplete closure of the umbilical ring.",
        "description_ja": "臍輪の不完全閉鎖により腹腔内容が突出する先天性欠損です。",
        "urgency": "normal",
    },
    {
        "name": "Salivary Mucocele (Sialocele)",
        "name_ja": "唾液腺嚢胞",
        "symptoms": {"swelling", "drooling", "appetite_loss", "difficulty_breathing"},
        "description": "Accumulation of saliva in tissues after salivary gland or duct rupture, causing a soft fluctuant swelling.",
        "description_ja": "唾液腺または唾液管の破裂後に組織に唾液が蓄積し、軟らかい波動性の腫脹を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Sinonasal Aspergillosis",
        "name_ja": "鼻腔アスペルギルス症",
        "symptoms": {"nasal_discharge", "sneezing", "pain_on_touch", "appetite_loss", "lethargy"},
        "description": "Fungal infection of the nasal cavity and sinuses causing destructive rhinitis and profuse nasal discharge.",
        "description_ja": "鼻腔と副鼻腔の真菌感染で、破壊性鼻炎と大量の鼻汁を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Peritonitis",
        "name_ja": "腹膜炎",
        "symptoms": {"fever", "abdominal_pain", "vomiting", "lethargy", "collapse", "bloated_abdomen", "dehydration"},
        "description": "Life-threatening inflammation of the peritoneum, often from GI perforation, bile leakage, or ruptured abscess.",
        "description_ja": "腹膜の致死的炎症で、消化管穿孔、胆汁漏出、膿瘍破裂が原因となることが多いです。",
        "urgency": "emergency",
    },
    {
        "name": "Hemoabdomen",
        "name_ja": "血腹",
        "symptoms": {"collapse", "rapid_breathing", "lethargy", "bloated_abdomen", "excessive_panting"},
        "description": "Free blood in the abdominal cavity from splenic/hepatic mass rupture, trauma, or coagulopathy.",
        "description_ja": "脾臓・肝臓腫瘤の破裂、外傷、凝固障害による腹腔内遊離血液です。",
        "urgency": "emergency",
    },
    {
        "name": "Urinary Bladder Tumor (TCC)",
        "name_ja": "膀胱腫瘍（移行上皮癌）",
        "symptoms": {"blood_urine", "straining_urinate", "excessive_urination", "incontinence", "lethargy"},
        "description": "Most common bladder tumor in dogs, causing hematuria and dysuria; Scottish Terriers are predisposed.",
        "description_ja": "犬で最も一般的な膀胱腫瘍で、血尿と排尿困難を引き起こし、スコティッシュテリアに好発します。",
        "urgency": "urgent",
    },
    {
        "name": "Pancreatic Adenocarcinoma",
        "name_ja": "膵腺癌",
        "symptoms": {"vomiting", "weight_loss", "appetite_loss", "abdominal_pain", "lethargy", "bloated_abdomen"},
        "description": "Highly malignant pancreatic tumor with very poor prognosis, often diagnosed at advanced stage.",
        "description_ja": "非常に予後不良な高悪性度の膵腫瘍で、進行期に診断されることが多いです。",
        "urgency": "urgent",
    },
    {
        "name": "Adrenal Gland Tumor",
        "name_ja": "副腎腫瘍",
        "symptoms": {"excessive_thirst", "excessive_urination", "weight_gain", "hair_loss", "lethargy", "excessive_panting"},
        "description": "Benign or malignant tumor of the adrenal gland causing Cushing's syndrome or pheochromocytoma signs.",
        "description_ja": "クッシング症候群または褐色細胞腫の症状を引き起こす副腎の良性または悪性腫瘍です。",
        "urgency": "urgent",
    },
    {
        "name": "Canine Hemotropic Mycoplasmosis",
        "name_ja": "犬ヘモトロピックマイコプラズマ症",
        "symptoms": {"lethargy", "fever", "appetite_loss", "weight_loss", "excessive_panting"},
        "description": "Blood parasite (Mycoplasma haemocanis) attaching to red blood cells, causing anemia in immunocompromised dogs.",
        "description_ja": "赤血球に付着する血液寄生虫で、免疫不全の犬に貧血を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Fibrotic Myopathy",
        "name_ja": "線維性ミオパチー",
        "symptoms": {"limping_rl", "limping_rr", "stiffness", "reluctance_move", "pain_on_touch"},
        "description": "Replacement of normal muscle tissue with fibrous tissue, causing mechanical lameness without pain.",
        "description_ja": "正常な筋組織が線維組織に置換され、痛みを伴わない機械的跛行を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Oronasal Fistula",
        "name_ja": "口腔鼻腔瘻",
        "symptoms": {"sneezing", "nasal_discharge", "appetite_loss", "drooling"},
        "description": "Abnormal communication between the oral and nasal cavities, usually from severe periodontal disease or tooth extraction.",
        "description_ja": "口腔と鼻腔の異常な交通で、通常は重度の歯周病や抜歯が原因です。",
        "urgency": "normal",
    },
    {
        "name": "Hypertensive Retinopathy",
        "name_ja": "高血圧性網膜症",
        "symptoms": {"eye_redness", "squinting", "circling", "anxiety"},
        "description": "Retinal damage from systemic hypertension causing sudden blindness, retinal detachment, or hemorrhage.",
        "description_ja": "全身性高血圧による網膜障害で、突然の失明、網膜剥離、出血を引き起こします。",
        "urgency": "emergency",
    },
    {
        "name": "Chronic Otitis Media",
        "name_ja": "慢性中耳炎",
        "symptoms": {"ear_scratching", "head_tilting", "ear_odor", "head_shaking", "ear_discharge", "pain_on_touch"},
        "description": "Persistent infection of the middle ear, often from untreated external ear infections penetrating the tympanic membrane.",
        "description_ja": "中耳の持続的感染で、未治療の外耳炎が鼓膜を貫通することが原因となることが多いです。",
        "pathophysiology_ja": "慢性外耳炎→鼓膜の損傷・穿孔→中耳腔への細菌・酵母感染の波及→鼓室内の炎症性滲出液貯留・骨溶解。Pseudomonas, Staphylococcus, Malasseziaが主要起因菌。鼓室包の骨増殖・狭窄により難治化。",
        "causes_ja": "慢性外耳炎の不適切な管理（最多）、耳道の解剖学的異常（垂れ耳・狭窄耳道）、アレルギー性疾患、ポリープ、異物。好発：コッカースパニエル、ラブラドール、シャーペイ等の垂れ耳犬種。",
        "prevention_ja": "外耳炎の早期・適切な治療、基礎疾患（アトピー・食物アレルギー）の管理、定期的な耳道検査・清掃、過度の耳洗浄の回避。",
        "urgency": "urgent",
    },
    {
        "name": "Inner Ear Infection (Otitis Interna)",
        "name_ja": "内耳炎",
        "symptoms": {"head_tilting", "circling", "head_shaking", "vomiting", "lethargy", "eye_redness"},
        "description": "Infection of the inner ear causing severe vestibular signs including head tilt, nystagmus, and ataxia.",
        "description_ja": "内耳の感染で、頭位傾斜、眼振、運動失調を含む重度の前庭症状を引き起こします。",
        "pathophysiology_ja": "中耳炎からの感染波及→内耳（蝸牛・前庭器官）の炎症→前庭神経障害→末梢性前庭症候群（頭位傾斜・水平眼振・旋回運動・運動失調）。蝸牛障害を伴うと感音性難聴。重症例では髄膜炎のリスク。",
        "causes_ja": "慢性中耳炎からの進展（最多）、血行性感染、外傷性鼓膜穿孔後の感染。起因菌：Pseudomonas aeruginosa, Staphylococcus, Streptococcus, Malassezia。",
        "prevention_ja": "外耳炎・中耳炎の早期治療、耳道の定期管理、基礎疾患（アレルギー）のコントロール、耳に水が入る状況の回避。",
        "urgency": "urgent",
    },
    {
        "name": "Acanthomatous Ameloblastoma",
        "name_ja": "棘細胞性エナメル上皮腫",
        "symptoms": {"drooling", "appetite_loss", "swelling", "pain_on_touch", "lumps"},
        "description": "A locally aggressive oral tumor invading bone; benign but destructive, requiring mandibulectomy or maxillectomy.",
        "description_ja": "骨に浸潤する局所的に攻撃的な口腔腫瘍で、良性ですが破壊的であり、下顎切除や上顎切除が必要です。",
        "pathophysiology_ja": "歯原性上皮（エナメル器）由来の良性腫瘍だが局所浸潤性が極めて高い→歯槽骨の進行性破壊→歯の脱落・顎骨変形。遠隔転移はしないが、不完全切除では100%再発。下顎前部の歯肉に最も好発。X線で骨溶解像を呈し、扁平上皮癌との鑑別が重要（生検必須）。",
        "causes_ja": "原因不明。歯原性上皮の腫瘍性増殖。中高齢犬（7〜10歳）。大型犬に多い。口腔良性腫瘍の中では最も浸潤性が高い。メラノーマ・SCCとの鑑別診断が臨床的に重要。",
        "prevention_ja": "確実な予防法はない。口腔内のしこり・歯の動揺・歯肉出血の早期受診。広範囲切除（下顎切除・上顎切除、腫瘍縁から1cm以上）で治癒率90%以上。術後のQOLは概ね良好。",
        "urgency": "urgent",
    },
    {
        "name": "Tracheal Perforation",
        "name_ja": "気管穿孔",
        "symptoms": {"difficulty_breathing", "swelling", "coughing", "rapid_breathing", "lethargy"},
        "description": "Tear in the tracheal wall from trauma, bite wounds, or iatrogenic injury causing subcutaneous emphysema.",
        "description_ja": "外傷、咬傷、医原性損傷による気管壁の裂傷で、皮下気腫を引き起こします。",
        "urgency": "emergency",
    },
    {
        "name": "Masticatory Myositis (Acute)",
        "name_ja": "急性咀嚼筋炎",
        "symptoms": {"swelling", "pain_on_touch", "appetite_loss", "fever", "drooling"},
        "description": "Acute immune-mediated inflammation of the muscles of mastication causing painful jaw swelling and trismus.",
        "description_ja": "咀嚼筋の急性免疫介在性炎症で、有痛性の顎の腫脹と開口障害を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Polymyositis",
        "name_ja": "多発性筋炎",
        "symptoms": {"stiffness", "lethargy", "pain_on_touch", "reluctance_move", "fever", "weight_loss"},
        "description": "Immune-mediated inflammation of multiple skeletal muscles causing generalized weakness and muscle pain.",
        "description_ja": "複数の骨格筋の免疫介在性炎症で、全身性の衰弱と筋肉痛を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Polyradiculoneuritis (Coonhound Paralysis)",
        "name_ja": "多発性神経根炎（クーンハウンド麻痺）",
        "symptoms": {"limping_fl", "limping_fr", "limping_rl", "limping_rr", "stiffness", "reluctance_move", "difficulty_breathing"},
        "description": "Acute inflammatory polyradiculoneuritis causing ascending paralysis, similar to Guillain-Barré syndrome in humans.",
        "description_ja": "急性炎症性多発性神経根炎で上行性麻痺を引き起こし、ヒトのギラン・バレー症候群に類似します。",
        "urgency": "emergency",
    },
    {
        "name": "Central Diabetes Insipidus",
        "name_ja": "中枢性尿崩症",
        "symptoms": {"excessive_thirst", "excessive_urination", "dehydration", "lethargy"},
        "description": "Deficient ADH production from the pituitary gland causing extreme polyuria and polydipsia.",
        "description_ja": "下垂体からのADH産生不足で、極度の多尿と多飲を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Nephrogenic Diabetes Insipidus",
        "name_ja": "腎性尿崩症",
        "symptoms": {"excessive_thirst", "excessive_urination", "dehydration", "lethargy", "weight_loss"},
        "description": "Kidney unresponsiveness to ADH causing inability to concentrate urine; may be congenital or acquired.",
        "description_ja": "腎臓のADHに対する不応答で尿の濃縮ができない状態で、先天性または後天性です。",
        "urgency": "urgent",
    },
    {
        "name": "Cervical Spondylomyelopathy (Wobbler - Disc Associated)",
        "name_ja": "頸椎脊椎脊髄症（椎間板関連型）",
        "symptoms": {"limping_rl", "limping_rr", "stiffness", "reluctance_move", "pain_on_touch"},
        "description": "Disc-associated form of Wobbler syndrome causing spinal cord compression, common in large breed dogs.",
        "description_ja": "椎間板関連型のウォブラー症候群で脊髄圧迫を引き起こし、大型犬に多く見られます。",
        "urgency": "urgent",
    },
    {
        "name": "Discospondylitis",
        "name_ja": "椎間板脊椎炎",
        "symptoms": {"fever", "pain_on_touch", "stiffness", "reluctance_move", "lethargy", "appetite_loss", "weight_loss"},
        "description": "Infection of the intervertebral disc and adjacent vertebral endplates, often bacterial or fungal in origin.",
        "description_ja": "椎間板と隣接する椎体終板の感染で、細菌性または真菌性が原因となることが多いです。",
        "pathophysiology_ja": "血行性感染→椎体終板の血管豊富な領域に細菌が定着→椎間板・隣接椎体の感染→骨溶解・新生骨形成→脊柱管内への波及→硬膜外膿瘍→脊髄圧迫→疼痛・神経学的障害。腰仙部（L7-S1）に最も多い。多発性病変が30〜40%。",
        "causes_ja": "細菌性（Staphylococcus intermedius/aureus、Streptococcus、Brucella canis が主要起因菌）。真菌性（Aspergillus、Coccidioides）は免疫抑制犬。感染源：尿路感染・歯周病・皮膚感染からの血行性播種。大型犬に好発。ブルセラ症の鑑別が重要（人獣共通）。",
        "prevention_ja": "尿路感染・歯周病等の感染巣の早期治療。原因不明の発熱＋脊椎痛では本疾患を疑い、脊椎X線・MRI・血液/尿培養を実施。抗菌薬治療は最低6〜8週間の長期投与が必要。",
        "urgency": "urgent",
    },
    {
        "name": "Atlantoaxial Subluxation",
        "name_ja": "環軸椎亜脱臼",
        "symptoms": {"pain_on_touch", "stiffness", "reluctance_move", "seizures", "collapse"},
        "description": "Instability between the first and second cervical vertebrae causing spinal cord compression; seen in toy breeds.",
        "description_ja": "第1・第2頸椎間の不安定性で脊髄圧迫を引き起こし、小型犬種に見られます。",
        "urgency": "emergency",
    },
    {
        "name": "Cutaneous Lymphoma (Epitheliotropic)",
        "name_ja": "皮膚リンパ腫（上皮向性）",
        "symptoms": {"skin_lesions", "itching", "hair_loss", "skin_redness", "lumps", "dry_skin"},
        "description": "T-cell lymphoma targeting the skin, causing chronic skin lesions that mimic dermatitis before diagnosis.",
        "description_ja": "皮膚を標的とするT細胞リンパ腫で、診断前は皮膚炎に類似した慢性皮膚病変を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Digital Squamous Cell Carcinoma",
        "name_ja": "指趾部扁平上皮癌",
        "symptoms": {"limping_fl", "limping_fr", "limping_rl", "limping_rr", "swelling", "lumps", "pain_on_touch"},
        "description": "Malignant tumor of the toe digits, common in large black-coated breeds, causing nail loss and toe swelling.",
        "description_ja": "足趾の悪性腫瘍で、大型の黒い被毛の犬種に多く、爪の脱落と趾の腫脹を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Gastric Polyps",
        "name_ja": "胃ポリープ",
        "symptoms": {"vomiting", "appetite_loss", "weight_loss", "bloody_stool"},
        "description": "Benign growths in the stomach lining that may cause chronic vomiting or GI bleeding if large.",
        "description_ja": "胃粘膜の良性腫瘤で、大きい場合は慢性嘔吐や消化管出血を引き起こすことがあります。",
        "urgency": "normal",
    },
    {
        "name": "Megacolon (Acquired)",
        "name_ja": "後天性巨大結腸症",
        "symptoms": {"constipation", "bloated_abdomen", "appetite_loss", "lethargy", "straining_urinate"},
        "description": "Severe chronic dilation of the colon with loss of motility, causing intractable constipation.",
        "description_ja": "結腸の重度の慢性拡張と運動性の喪失で、難治性の便秘を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Keratoacanthoma",
        "name_ja": "角化棘細胞腫",
        "symptoms": {"lumps", "skin_lesions"},
        "description": "A benign keratinizing skin tumor appearing as a horn-like growth, most common in Norwegian Elkhounds.",
        "description_ja": "角状の増殖を呈する良性の角化性皮膚腫瘍で、ノルウェジアンエルクハウンドに最も多いです。",
        "urgency": "normal",
    },
    {
        "name": "Apocrine Gland Adenocarcinoma",
        "name_ja": "アポクリン腺癌",
        "symptoms": {"lumps", "swelling", "skin_lesions", "lethargy", "weight_loss"},
        "description": "Malignant tumor of the apocrine sweat glands, often found on the limbs or trunk.",
        "description_ja": "アポクリン汗腺の悪性腫瘍で、四肢や体幹に多く見られます。",
        "urgency": "urgent",
    },
    {
        "name": "Cranial Cruciate Ligament Disease (Partial Tear)",
        "name_ja": "前十字靭帯部分断裂",
        "symptoms": {"limping_rl", "limping_rr", "stiffness", "reluctance_move", "swollen_joints"},
        "description": "Partial tearing of the cranial cruciate ligament causing intermittent hind limb lameness that worsens over time.",
        "description_ja": "前十字靭帯の部分断裂で、時間の経過とともに悪化する間欠的な後肢跛行を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Septic Arthritis",
        "name_ja": "感染性関節炎",
        "symptoms": {"swollen_joints", "fever", "limping_fl", "limping_fr", "limping_rl", "limping_rr", "pain_on_touch", "lethargy"},
        "description": "Bacterial infection of a joint causing acute swelling, heat, pain, and systemic illness.",
        "description_ja": "関節の細菌感染で、急性腫脹、熱感、疼痛、全身症状を引き起こします。",
        "urgency": "emergency",
    },
    {
        "name": "Bone Cyst (Aneurysmal)",
        "name_ja": "骨嚢腫（動脈瘤様）",
        "symptoms": {"limping_fl", "limping_fr", "limping_rl", "limping_rr", "swelling", "pain_on_touch"},
        "description": "A blood-filled cystic lesion in bone causing expansion, pain, and pathologic fracture risk.",
        "description_ja": "骨内の血液で満たされた嚢胞性病変で、膨張、痛み、病的骨折のリスクを引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Chronic Bronchitis",
        "name_ja": "慢性気管支炎",
        "symptoms": {"coughing", "excessive_panting", "difficulty_breathing", "lethargy", "rapid_breathing"},
        "description": "Chronic inflammation of the bronchi causing persistent cough for more than 2 months without other identifiable cause.",
        "description_ja": "気管支の慢性炎症で、他に特定可能な原因のない2か月以上の持続的な咳嗽を引き起こします。",
        "pathophysiology_ja": "気管支粘膜の慢性炎症→杯細胞過形成→粘液過分泌→気道クリアランスの低下→二次細菌感染の反復。気管支壁の肥厚・気道リモデリング→不可逆的な気道狭窄。気管虚脱との併存が多い。除外診断（心疾患・肺炎・腫瘍を除外後に診断）。",
        "causes_ja": "原因不明（除外診断）。環境刺激物（煙・粉塵・大気汚染）、慢性気道感染、アレルギー性気道炎症が関与。中高齢の小型犬に好発。肥満は増悪因子。",
        "prevention_ja": "環境刺激物の回避（受動喫煙・芳香剤・粉塵）、肥満防止、気道感染の早期治療。",
        "urgency": "normal",
    },
    {
        "name": "Bronchiectasis",
        "name_ja": "気管支拡張症",
        "symptoms": {"coughing", "nasal_discharge", "difficulty_breathing", "lethargy", "fever"},
        "description": "Irreversible dilation of the bronchi from chronic infection or inflammation, causing recurrent pneumonia.",
        "description_ja": "慢性感染や炎症による気管支の不可逆的拡張で、再発性肺炎を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Myxomatous Mitral Valve Degeneration (Early Stage)",
        "name_ja": "粘液腫様僧帽弁変性症（初期）",
        "symptoms": {"coughing", "lethargy", "excessive_panting"},
        "description": "Early degenerative changes of the mitral valve causing a murmur but not yet clinical heart failure.",
        "description_ja": "僧帽弁の初期変性変化で心雑音を生じますが、まだ臨床的心不全には至っていません。",
        "urgency": "normal",
    },
    {
        "name": "Canine Brucellosis (Reproductive)",
        "name_ja": "犬ブルセラ症（生殖器型）",
        "symptoms": {"genital_discharge", "fever", "lethargy", "swelling", "weight_loss"},
        "description": "Brucella canis infection primarily affecting the reproductive system, causing abortion and infertility.",
        "description_ja": "主に生殖器系を侵すブルセラ菌感染で、流産と不妊を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Pituitary Dwarfism",
        "name_ja": "下垂体性小人症",
        "symptoms": {"hair_loss", "dry_skin", "lethargy", "weight_loss"},
        "description": "Growth hormone deficiency from pituitary cyst or hypoplasia, causing proportionate dwarfism and alopecia in German Shepherds.",
        "description_ja": "下垂体嚢胞や低形成による成長ホルモン欠乏で、ジャーマンシェパードに均衡性小人症と脱毛を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Canine Familial Nephropathy",
        "name_ja": "犬家族性腎症",
        "symptoms": {"excessive_thirst", "excessive_urination", "weight_loss", "vomiting", "lethargy"},
        "description": "Hereditary progressive kidney disease in breeds like English Cocker Spaniels, causing early-onset renal failure.",
        "description_ja": "イングリッシュコッカースパニエルなどの犬種の遺伝性進行性腎疾患で、早期発症の腎不全を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Acquired Myasthenia Gravis (Focal)",
        "name_ja": "後天性重症筋無力症（局所型）",
        "symptoms": {"regurgitation", "drooling", "coughing", "difficulty_breathing"},
        "description": "Focal form of myasthenia gravis primarily affecting esophageal muscles, causing megaesophagus and regurgitation.",
        "description_ja": "主に食道筋を侵す重症筋無力症の局所型で、巨大食道と逆流を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Hepatocutaneous Syndrome (SND)",
        "name_ja": "肝皮症候群",
        "symptoms": {"skin_lesions", "hair_loss", "skin_redness", "lethargy", "appetite_loss", "weight_loss"},
        "description": "Severe crusting dermatitis of the footpads and face associated with liver disease and amino acid deficiency.",
        "description_ja": "肝疾患とアミノ酸欠乏に関連する足裏と顔面の重度の痂皮性皮膚炎です。",
        "urgency": "urgent",
    },
    {
        "name": "Idiopathic Head Tremor Syndrome",
        "name_ja": "特発性頭部振戦症候群",
        "symptoms": {"head_shaking", "anxiety"},
        "description": "Benign episodic head bobbing of unknown cause, seen in Bulldogs and Dobermans; dogs remain alert and responsive.",
        "description_ja": "原因不明の良性のエピソード性頭部振動で、ブルドッグやドーベルマンに見られ、犬は覚醒し反応します。",
        "urgency": "normal",
    },
    {
        "name": "Idiopathic Chylothorax",
        "name_ja": "特発性乳び胸",
        "symptoms": {"difficulty_breathing", "coughing", "lethargy", "appetite_loss", "rapid_breathing"},
        "description": "Accumulation of chyle in the pleural space without identifiable cause, common in Afghan Hounds and Shiba Inus.",
        "description_ja": "原因不明の胸腔内乳び液貯留で、アフガンハウンドや柴犬に多く見られます。",
        "urgency": "urgent",
    },
    {
        "name": "Canine Leproid Granuloma",
        "name_ja": "犬ハンセン病様肉芽腫",
        "symptoms": {"skin_lesions", "lumps", "hair_loss"},
        "description": "Mycobacterial skin disease causing firm nodules on the ears and face, most common in short-coated breeds.",
        "description_ja": "耳と顔面に硬い結節を形成する抗酸菌性皮膚疾患で、短毛種に最も多く見られます。",
        "urgency": "normal",
    },
    {
        "name": "Canine Distemper - Hardpad Disease",
        "name_ja": "犬ジステンパー硬蹠症",
        "symptoms": {"dry_skin", "fever", "coughing", "nasal_discharge", "seizures", "lethargy"},
        "description": "Late-stage distemper causing hyperkeratosis of the footpads and nose, with neurological complications.",
        "description_ja": "足裏と鼻の角質増殖を引き起こすジステンパーの後期段階で、神経学的合併症を伴います。",
        "urgency": "urgent",
    },
    {
        "name": "Cranial Cruciate Ligament Rupture",
        "name_ja": "前十字靭帯断裂",
        "symptoms": {"limping_rl", "limping_rr", "stiffness", "reluctance_move", "swollen_joints"},
        "description": "Rupture of the cranial cruciate ligament, one of the most common orthopedic injuries in dogs.",
        "description_ja": "前十字靭帯の断裂で、犬で最も一般的な整形外科的損傷の一つです。",
        "pathophysiology_ja": "前十字靭帯（CrCL）の進行性変性→コラーゲン線維の微小断裂の蓄積→部分断裂→完全断裂→脛骨の前方変位（cranial tibial thrust）→半月板の圧挫損傷→関節不安定性→二次性変形性関節症の急速な進行。犬の靭帯断裂は人と異なり外傷性よりも変性性が主因。",
        "causes_ja": "慢性変性性靭帯症（最多）。リスク因子：肥満、急峻な脛骨高平部角（TPA）、大型犬（ラブラドール、ゴールデン、ロットワイラー）、避妊/去勢後のホルモン変化。対側肢も40〜60%が2年以内に罹患。急性外傷性断裂は小型犬や若齢犬に多い。",
        "prevention_ja": "適正体重の維持、過度の急停止・旋回運動の回避、好発犬種の筋力維持（水泳・コントロールされた運動）、関節サプリメント（グルコサミン・EPA/DHA）。",
        "urgency": "urgent",
    },
    {
        "name": "Medial Patellar Luxation",
        "name_ja": "膝蓋骨内方脱臼",
        "symptoms": {"limping_rl", "limping_rr", "stiffness", "reluctance_move"},
        "description": "Displacement of the kneecap medially, common in small breed dogs.",
        "description_ja": "膝蓋骨が内側に変位する疾患で、小型犬に多く見られます。",
        "pathophysiology_ja": "大腿骨滑車溝の浅小化＋大腿四頭筋のアライメント異常→膝蓋骨の内方変位→脱臼の反復→脛骨内旋・弓状変形（慢性例）→関節軟骨の摩耗→二次性変形性関節症。Grade 1（手動で脱臼、自然整復）〜Grade 4（恒常的脱臼、整復不能）。前十字靭帯断裂の併発リスクが高い（15〜20%）。",
        "causes_ja": "先天性・発達性（多因子遺伝、最多）。内側脱臼（MPL）が小型犬の90%以上を占め、両側性が50%。好発犬種：チワワ、ポメラニアン、トイプードル、ヨークシャーテリア、マルチーズ、柴犬。外側脱臼（LPL）は大型犬に多い。",
        "prevention_ja": "好発犬種の繁殖管理（膝蓋骨の評価）、適正体重の維持、滑りやすい床面の回避（滑り止めマット）、過度のジャンプの制限。Grade 2以上では外科矯正（滑車溝形成術・脛骨粗面転位術）の早期検討が二次的OA予防に重要。",
        "urgency": "normal",
    },
    {
        "name": "Legg-Calve-Perthes Disease",
        "name_ja": "レッグ・カルベ・ペルテス病",
        "symptoms": {"limping_rl", "limping_rr", "pain_on_touch", "reluctance_move", "stiffness"},
        "description": "Avascular necrosis of the femoral head in young small breed dogs.",
        "description_ja": "大腿骨頭の無血管性壊死で若い小型犬に多い疾患です。",
        "urgency": "normal",
    },
    {
        "name": "Fragmented Coronoid Process",
        "name_ja": "肘突起分離症",
        "symptoms": {"limping_fl", "limping_fr", "swollen_joints", "stiffness", "reluctance_move"},
        "description": "Component of elbow dysplasia where the coronoid process fragments.",
        "description_ja": "肘関節形成不全の一つで鉤状突起が分離する疾患です。",
        "urgency": "normal",
    },
    {
        "name": "Cervical Spondylomyelopathy (Wobbler Syndrome)",
        "name_ja": "頸部脊椎脊髄症",
        "symptoms": {"stiffness", "reluctance_move", "limping_rl", "limping_rr", "circling"},
        "description": "Cervical spinal cord compression causing wobbly gait in large breed dogs.",
        "description_ja": "頸部脊髄の圧迫により不安定な歩行を引き起こす大型犬の疾患です。",
        "urgency": "urgent",
    },
    {
        "name": "Lumbosacral Stenosis",
        "name_ja": "腰仙部狭窄症",
        "symptoms": {"limping_rl", "limping_rr", "pain_on_touch", "reluctance_move", "incontinence"},
        "description": "Compression of nerve roots at the lumbosacral junction.",
        "description_ja": "腰仙部の神経根圧迫により痛みと尿失禁を引き起こす疾患です。",
        "urgency": "urgent",
    },
    {
        "name": "Granulomatous Meningoencephalomyelitis (GME)",
        "name_ja": "肉芽腫性髄膜脳脊髄炎",
        "symptoms": {"seizures", "circling", "head_tilting", "lethargy", "fever", "collapse"},
        "description": "Inflammatory CNS disease causing seizures and neurological deficits in small breed dogs.",
        "description_ja": "小型犬の中枢神経系の炎症性疾患で痙攣を引き起こします。",
        "urgency": "emergency",
    },
    {
        "name": "Necrotizing Meningoencephalitis (Pug Dog Encephalitis)",
        "name_ja": "壊死性髄膜脳炎",
        "symptoms": {"seizures", "circling", "head_tilting", "lethargy", "collapse"},
        "description": "Fatal inflammatory brain disease most commonly seen in Pugs.",
        "description_ja": "パグに多い致死的な炎症性脳疾患です。",
        "urgency": "emergency",
    },
    {
        "name": "Fibrocartilaginous Embolic Myelopathy",
        "name_ja": "線維軟骨塞栓性脊髄症",
        "symptoms": {"collapse", "limping_rl", "limping_rr", "reluctance_move", "incontinence"},
        "description": "Acute spinal cord infarction caused by fibrocartilaginous embolism.",
        "description_ja": "線維軟骨性物質による急性脊髄梗塞です。",
        "urgency": "emergency",
    },
    {
        "name": "Degenerative Myelopathy",
        "name_ja": "変性性脊髄症",
        "symptoms": {"limping_rl", "limping_rr", "stiffness", "reluctance_move", "incontinence"},
        "description": "Progressive degenerative disease of the spinal cord causing hind limb weakness.",
        "description_ja": "脊髄の進行性変性疾患で後肢の脱力を引き起こします。",
        "pathophysiology_ja": "SOD1遺伝子変異→スーパーオキシドジスムターゼ1の異常→脊髄白質（特に胸腰椎領域の背側索・側索）の進行性軸索変性・脱髄→上位運動ニューロン性後肢不全麻痺→進行して下位運動ニューロン性麻痺→前肢にも波及→最終的に呼吸筋障害。人のALS（筋萎縮性側索硬化症）と類似。発症から完全対麻痺まで6〜36ヶ月。非疼痛性。",
        "causes_ja": "SOD1遺伝子変異（常染色体劣性）。ホモ接合体（A/A）で発症リスクが高い。好発犬種：ジャーマンシェパード（最多）、ウェルシュコーギー・ペンブローク、ボクサー、ロードシアンリッジバック、チェサピークベイレトリーバー。8歳以上で発症。除外診断（IVDD等を除外後）＋SOD1遺伝子検査で臨床診断。確定は剖検時の脊髄病理のみ。",
        "prevention_ja": "SOD1遺伝子検査による繁殖管理（ホモ接合体犬の繁殖制限）。治療法はないが、リハビリテーション（水泳・車椅子）でQOLと筋量維持。ビタミンE・B群・EPA/DHAの補充が一部で推奨されるがエビデンスは限定的。",
        "urgency": "normal",
    },
    {
        "name": "Canine Cognitive Dysfunction Syndrome",
        "name_ja": "犬認知機能不全症候群",
        "symptoms": {"anxiety", "circling", "hiding", "aggression_change", "incontinence"},
        "description": "Age-related cognitive decline causing disorientation and behavioral changes.",
        "description_ja": "加齢性認知機能低下で見当識障害と行動変化を引き起こします。",
        "pathophysiology_ja": "大脳皮質のβアミロイド沈着→ニューロンの脱落・シナプス機能低下→前頭葉・海馬の萎縮→DISHAAL症状群：見当識障害（Disorientation）、社会的交流変化（Interactions）、睡眠覚醒サイクルの乱れ（Sleep-wake）、不適切排泄（Housesoiling）、活動性変化（Activity）、不安（Anxiety）、学習記憶低下（Learning）。ドーパミン・セロトニン・アセチルコリン系の減少も関与。",
        "causes_ja": "加齢に伴う脳の変性（βアミロイド蓄積・酸化ストレス・ミトコンドリア機能障害・脳血管障害）。11歳以上の犬の28%、15歳以上の68%が何らかの認知機能低下を示す。全犬種で発症し、小型犬は長寿のため臨床的に多く認識される。",
        "prevention_ja": "抗酸化物質含有食（ビタミンE・C、α-リポ酸・L-カルニチン）、EPA/DHAサプリメント、精神的刺激（トレーニング・知育玩具・ノーズワーク）、適度な社会的交流・運動を生涯にわたり継続。セレギリン（MAO-B阻害剤）やS-アデノシルメチオニン（SAMe）の早期投与も検討。",
        "urgency": "normal",
    },
    {
        "name": "Syringomyelia",
        "name_ja": "脊髄空洞症",
        "symptoms": {"pain_on_touch", "itching", "stiffness", "anxiety", "hiding"},
        "description": "Fluid-filled cavities within the spinal cord, common in Cavalier King Charles Spaniels.",
        "description_ja": "脊髄内の液体充満空洞でキャバリアに多い疾患です。",
        "urgency": "normal",
    },
    {
        "name": "Tetralogy of Fallot",
        "name_ja": "ファロー四徴症",
        "symptoms": {"collapse", "difficulty_breathing", "lethargy", "excessive_panting", "seizures"},
        "description": "Complex congenital heart defect causing cyanosis and exercise intolerance.",
        "description_ja": "4つの異常からなる複合先天性心疾患です。",
        "urgency": "emergency",
    },
    {
        "name": "Pulmonary Thromboembolism",
        "name_ja": "肺血栓塞栓症",
        "symptoms": {"difficulty_breathing", "rapid_breathing", "collapse", "coughing", "lethargy"},
        "description": "Blood clot obstructing pulmonary vasculature.",
        "description_ja": "肺血管を閉塞する血栓で他の疾患に続発することが多いです。",
        "urgency": "emergency",
    },
    {
        "name": "Hemangiosarcoma (Splenic)",
        "name_ja": "脾臓血管肉腫",
        "symptoms": {"collapse", "bloated_abdomen", "lethargy", "appetite_loss", "excessive_panting"},
        "description": "Aggressive malignant tumor of blood vessel walls in the spleen.",
        "description_ja": "脾臓の血管壁の悪性腫瘍で内出血を引き起こします。",
        "urgency": "emergency",
    },
    {
        "name": "Hemangiosarcoma (Cardiac)",
        "name_ja": "心臓血管肉腫",
        "symptoms": {"collapse", "difficulty_breathing", "lethargy", "bloated_abdomen"},
        "description": "Malignant tumor of the heart causing pericardial effusion.",
        "description_ja": "心臓の悪性腫瘍で心嚢液貯留を引き起こします。",
        "urgency": "emergency",
    },
    {
        "name": "Primary Hyperparathyroidism",
        "name_ja": "原発性副甲状腺機能亢進症",
        "symptoms": {"excessive_thirst", "excessive_urination", "lethargy", "appetite_loss", "vomiting"},
        "description": "Overproduction of parathyroid hormone causing elevated blood calcium.",
        "description_ja": "副甲状腺ホルモンの過剰産生により高カルシウム血症を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Pemphigus Foliaceus",
        "name_ja": "落葉状天疱瘡",
        "symptoms": {"skin_lesions", "itching", "skin_redness", "hair_loss", "fever"},
        "description": "Autoimmune skin disease causing pustules and crusting.",
        "description_ja": "膿疱と痂皮を形成する自己免疫性皮膚疾患です。",
        "pathophysiology_ja": "表皮細胞間接着蛋白（デスモグレイン-1）に対する自己抗体（IgG）→棘融解（acantholysis）→表層の表皮内水疱・膿疱形成→破裂後に痂皮・びらん。鼻梁・耳介・足底パッド・爪周囲に好発。犬で最も多い自己免疫性皮膚疾患。全身症状（発熱・食欲不振）を伴うことがある。",
        "causes_ja": "一次性（特発性、最多）：自己免疫性。二次性：薬剤誘発性（トリメトプリム・サルファ等）。好発犬種：秋田犬、チャウチャウ、ダックスフンド、ビーグル、ニューファンドランド。中年犬に多い。皮膚生検で棘融解細胞を伴う表皮内膿疱が確定診断。",
        "prevention_ja": "確実な予防法はない。薬剤誘発性が疑われる場合は原因薬の中止。免疫抑制療法（プレドニゾロン→アザチオプリン/ミコフェノール酸モフェチル併用）で管理。生涯治療が必要なことが多い。",
        "urgency": "urgent",
    },
    {
        "name": "Discoid Lupus Erythematosus",
        "name_ja": "円板状エリテマトーデス",
        "symptoms": {"skin_lesions", "skin_redness", "hair_loss", "dry_skin"},
        "description": "Autoimmune skin disease primarily affecting the nose.",
        "description_ja": "主に鼻を侵す自己免疫性皮膚疾患で脱色素と潰瘍を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Color Dilution Alopecia",
        "name_ja": "希釈色脱毛症",
        "symptoms": {"hair_loss", "dry_skin", "skin_lesions"},
        "description": "Hereditary condition in dilute-colored dogs causing hair loss.",
        "description_ja": "希釈色の犬に見られる遺伝性疾患で脱毛を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Pulmonary Carcinoma",
        "name_ja": "肺癌",
        "symptoms": {"coughing", "difficulty_breathing", "lethargy", "weight_loss", "appetite_loss"},
        "description": "Primary or metastatic lung cancer.",
        "description_ja": "原発性または転移性肺癌で呼吸窮迫を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Xylitol Toxicosis",
        "name_ja": "キシリトール中毒",
        "symptoms": {"vomiting", "collapse", "seizures", "lethargy"},
        "description": "Potentially fatal poisoning from xylitol causing hypoglycemia and liver failure.",
        "description_ja": "キシリトールによる中毒で低血糖と肝不全を引き起こします。",
        "pathophysiology_ja": "キシリトール摂取→犬の膵β細胞からの急速なインスリン放出（用量依存的）→重度の低血糖（摂取後10〜60分、BG<60mg/dL）→けいれん・虚脱。高用量（>0.5g/kg）では急性肝壊死→凝固障害・DIC→致死的肝不全（摂取後12〜48時間）。犬のキシリトール感受性は人の7倍以上。",
        "causes_ja": "シュガーフリーガム（最多の原因、1粒あたりキシリトール0.3〜1g含有）、キシリトール含有飴・歯磨き粉・ベーキング製品・ピーナッツバター。毒性量：低血糖は0.1g/kg、肝不全は0.5g/kg以上。小型犬ではガム数粒で致死的。",
        "prevention_ja": "キシリトール含有製品のペットからの完全隔離、ガム・飴のバッグやポーチの犬の届かない場所への保管、ピーナッツバター購入時の成分確認（キシリトール不使用品を選択）。",
        "urgency": "emergency",
    },
    {
        "name": "Grape and Raisin Toxicosis",
        "name_ja": "ブドウ・レーズン中毒",
        "symptoms": {"vomiting", "diarrhea", "appetite_loss", "lethargy", "excessive_thirst"},
        "description": "Poisoning causing acute kidney failure.",
        "description_ja": "急性腎不全を引き起こす中毒です。",
        "urgency": "emergency",
    },
    {
        "name": "Anticoagulant Rodenticide Toxicosis",
        "name_ja": "抗凝固性殺鼠剤中毒",
        "symptoms": {"bloody_stool", "coughing", "difficulty_breathing", "lethargy", "collapse"},
        "description": "Poisoning from rat bait causing coagulopathy.",
        "description_ja": "殺鼠剤による中毒で凝固障害と内出血を引き起こします。",
        "pathophysiology_ja": "抗凝固性殺鼠剤→肝臓のビタミンKエポキシド還元酵素（VKOR）阻害→ビタミンK依存性凝固因子（II, VII, IX, X）の活性型への再生阻害→凝固因子の枯渇（摂取後2〜5日）→内出血（胸腔・腹腔・皮下・関節内）。第二世代（ブロディファコウム・ブロマジオロン）は半減期が数週間〜数ヶ月と極めて長い。",
        "causes_ja": "殺鼠剤ペレットの直接摂取、または中毒したネズミの二次摂取（リレー中毒）。第一世代（ワルファリン）：日本で広く流通、毒性は比較的低い。第二世代（ブロディファコウム）：1回の摂取で致死的、半減期が極長。犬は嗜好性の高いペレットを好んで食べる。",
        "prevention_ja": "殺鼠剤のペットアクセス不能な密閉型ベイトステーションの使用、設置場所の記録、使用後の残余ペレットの回収、代替的害獣駆除法（トラップ・超音波）の検討。",
        "urgency": "emergency",
    },
    {
        "name": "Ethylene Glycol Toxicosis",
        "name_ja": "エチレングリコール中毒",
        "symptoms": {"vomiting", "excessive_thirst", "excessive_urination", "seizures", "collapse", "lethargy"},
        "description": "Antifreeze poisoning causing acute kidney failure.",
        "description_ja": "不凍液による中毒で急性腎不全を引き起こします。",
        "urgency": "emergency",
    },
    {
        "name": "Metaldehyde Toxicosis",
        "name_ja": "メタアルデヒド中毒",
        "symptoms": {"seizures", "excessive_panting", "vomiting", "diarrhea", "collapse"},
        "description": "Severe poisoning from slug bait causing status epilepticus.",
        "description_ja": "ナメクジ駆除剤による中毒で痙攣重積を引き起こします。",
        "urgency": "emergency",
    },
    # REMOVED: duplicate of "Onion/Garlic Toxicosis" (line ~2591)
    {
        "name": "Esophageal Foreign Body",
        "name_ja": "食道異物",
        "symptoms": {"regurgitation", "drooling", "appetite_loss", "vomiting"},
        "description": "Lodged object in the esophagus.",
        "description_ja": "食道に異物が嵌頓し嚥下困難と吐出を引き起こします。",
        "pathophysiology_ja": "骨片・フック・果物の種等が食道（特に胸郭入口部・心基底部・横隔膜裂孔の3つの生理的狭窄部）に嵌頓→食道壁の圧迫壊死→食道穿孔→縦隔炎・胸膜炎→敗血症。嵌頓時間が長いほど（>24時間）穿孔リスクが上昇。食道狭窄の後遺症あり。",
        "causes_ja": "骨片（鶏骨・魚骨が最多）、釣り針・針付き糸、果物の種（桃・アボカド）、デンタルチュー。食道の3つの狭窄部に嵌頓しやすい。テリア種・小型犬に好発。骨を丸呑みする犬で多い。",
        "prevention_ja": "加熱した鶏骨・魚骨の給餌回避（加熱で脆くなり鋭利な破片に）、適切なサイズの食物・おやつの選択、丸呑み防止の食器（スローフィーダー）の使用、釣り具の安全管理。",
        "urgency": "emergency",
    },
    {
        "name": "Gastric Ulceration",
        "name_ja": "胃潰瘍",
        "symptoms": {"vomiting", "bloody_stool", "appetite_loss", "abdominal_pain", "lethargy"},
        "description": "Erosion of the gastric mucosa.",
        "description_ja": "胃粘膜の侵食により嘔吐と黒色便を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Intestinal Lymphangiectasia",
        "name_ja": "腸リンパ管拡張症",
        "symptoms": {"diarrhea", "weight_loss", "vomiting", "bloated_abdomen", "lethargy"},
        "description": "Dilation of intestinal lymphatics causing protein-losing enteropathy.",
        "description_ja": "腸リンパ管の拡張により蛋白漏出性腸症を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Prostatic Abscess",
        "name_ja": "前立腺膿瘍",
        "symptoms": {"fever", "straining_urinate", "lethargy", "vomiting", "bloody_stool"},
        "description": "Bacterial infection of the prostate forming an abscess.",
        "description_ja": "前立腺の細菌感染による膿瘍形成です。",
        "pathophysiology_ja": "前立腺炎の進行→膿瘍腔の形成（被包化された膿汁貯留）→破裂→腹膜炎・敗血症。前立腺嚢胞の二次感染からの発展もある。E. coli, Staphylococcus, Streptococcus, Proteus等が主な起因菌。未去勢雄の前立腺はテストステロン依存性に肥大→感染リスク上昇。",
        "causes_ja": "未去勢雄犬の前立腺肥大に伴う尿路上行性感染、慢性前立腺炎の進行、前立腺嚢胞の感染。中高齢の未去勢雄犬に好発。免疫抑制状態がリスク因子。",
        "prevention_ja": "早期去勢手術（前立腺のテストステロン依存性増殖を防止）、前立腺炎の早期・適切な抗菌薬治療、定期的な前立腺触診（直腸検査）。",
        "urgency": "emergency",
    },
    {
        "name": "Benign Prostatic Hyperplasia",
        "name_ja": "前立腺肥大症",
        "symptoms": {"straining_urinate", "constipation", "blood_urine"},
        "description": "Age-related enlargement of the prostate in intact male dogs.",
        "description_ja": "未去勢雄犬の加齢に伴う前立腺の肥大です。",
        "pathophysiology_ja": "テストステロンとジヒドロテストステロン（DHT）の作用→前立腺腺上皮・間質の過形成→前立腺の対称性肥大→直腸圧排（便秘・しぶり）→尿道圧排（排尿困難・血尿）。6歳以上の未去勢雄犬の80%以上に何らかの程度のBPHが存在。前立腺嚢胞・前立腺炎への進展リスク。",
        "causes_ja": "テストステロン依存性の前立腺組織増殖。未去勢雄犬の加齢に伴い進行。6歳以上の未去勢雄で最多。前立腺炎・膿瘍・嚢胞・腫瘍との鑑別が重要。",
        "prevention_ja": "去勢手術（最も効果的、前立腺は去勢後数週間で著明に縮小）。去勢を希望しない場合はフィナステリド（5α-還元酵素阻害剤）またはデスロレリンインプラント（GnRHアゴニスト）。",
        "urgency": "normal",
    },
    {
        "name": "Nictitans Gland Prolapse (Cherry Eye)",
        "name_ja": "瞬膜腺突出",
        "symptoms": {"eye_redness", "eye_discharge", "squinting"},
        "description": "Prolapse of the third eyelid gland.",
        "description_ja": "瞬膜腺の突出で目の隅に赤い腫瘤として現れます。",
        "pathophysiology_ja": "瞬膜腺（第三眼瞼腺）を固定する結合組織の先天的脆弱性→腺組織の脱出→露出腺の乾燥・炎症・二次感染→粘液膿性分泌物。瞬膜腺は涙液の30〜40%を産生するため、切除するとKCS（ドライアイ）リスクが顕著に上昇。両側性の発症が多い。",
        "causes_ja": "先天的な結合組織の脆弱性。好発犬種：コッカースパニエル、ブルドッグ、ビーグル、バセットハウンド、シャーペイ、ケーン・コルソ。通常2歳未満で発症。片側発症後、対側も罹患することが多い。",
        "prevention_ja": "確実な予防法はない。発症後は腺の切除ではなく外科的整復（Morgan pocket法・tucking法）を強く推奨。腺を切除するとKCSリスクが58%に上昇するとの報告あり。好発犬種の繁殖管理。",
        "urgency": "normal",
    },
    {
        "name": "Canine Brucellosis",
        "name_ja": "犬ブルセラ症",
        "symptoms": {"fever", "lethargy", "genital_discharge", "swollen_joints", "hair_loss"},
        "description": "Bacterial infection causing reproductive failure.",
        "description_ja": "繁殖障害と椎間板脊椎炎を引き起こす細菌感染症です。",
        "urgency": "urgent",
    },
    {
        "name": "Canine Leptospirosis",
        "name_ja": "犬レプトスピラ症",
        "symptoms": {"fever", "vomiting", "lethargy", "excessive_thirst", "excessive_urination", "appetite_loss"},
        "description": "Spirochetal infection causing acute kidney and liver failure.",
        "description_ja": "スピロヘータ感染症で急性腎不全と肝不全を引き起こします。",
        "urgency": "emergency",
    },
    {
        "name": "Canine Herpesvirus",
        "name_ja": "犬ヘルペスウイルス",
        "symptoms": {"nasal_discharge", "lethargy", "genital_discharge"},
        "description": "Viral infection fatal in neonatal puppies.",
        "description_ja": "新生子犬に致死的なウイルス感染症です。",
        "urgency": "urgent",
    },
    {
        "name": "Salmon Poisoning Disease",
        "name_ja": "サケ中毒症",
        "symptoms": {"fever", "vomiting", "diarrhea", "appetite_loss", "lethargy", "bloody_stool"},
        "description": "Fatal rickettsia infection transmitted by flukes in raw salmon.",
        "description_ja": "生サケの吸虫を介して感染する致死的リケッチア感染症です。",
        "pathophysiology_ja": "生のサケ科魚類に寄生する吸虫（Nanophyetus salmincola）内のリケッチア（Neorickettsia helminthoeca）が原因。生魚摂取→吸虫が腸管に付着→リケッチアが全身に播種→リンパ節腫大・出血性腸炎・肝脾腫。未治療での致死率90%。犬に特異的（猫は臨床的に無症状）。摂取後5〜7日で発症。",
        "causes_ja": "太平洋岸のサケ科魚類（サケ・マス・スチールヘッド）の生食。北米太平洋岸（カリフォルニア〜アラスカ）に限局した地理的分布。日本での報告はないが、輸入生魚に注意。感染魚の生食・不完全加熱が原因。",
        "prevention_ja": "犬へのサケ科魚類の生食禁止（十分な加熱または冷凍処理で安全）、川辺での生魚の拾い食い防止、流行地域での散歩時のリード管理。",
        "urgency": "emergency",
    },
    {
        "name": "Leishmaniosis",
        "name_ja": "リーシュマニア症",
        "symptoms": {"weight_loss", "hair_loss", "skin_lesions", "lethargy", "swollen_joints"},
        "description": "Protozoal disease transmitted by sandflies.",
        "description_ja": "サシチョウバエ媒介の原虫疾患で皮膚と内臓疾患を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Primary Ciliary Dyskinesia",
        "name_ja": "原発性線毛機能不全症",
        "symptoms": {"coughing", "nasal_discharge", "sneezing", "difficulty_breathing"},
        "description": "Inherited defect in ciliary function causing chronic respiratory infections.",
        "description_ja": "線毛機能の遺伝性欠陥で慢性呼吸器感染症を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Compulsive Disorder",
        "name_ja": "強迫性障害",
        "symptoms": {"anxiety", "circling", "itching", "aggression_change"},
        "description": "Repetitive out-of-context behaviors such as tail chasing.",
        "description_ja": "尾追いなどの持続的な反復行動です。",
        "urgency": "normal",
    },
    {
        "name": "Portosystemic Shunt (PSS)",
        "name_ja": "門脈体循環シャント",
        "symptoms": {"seizures", "circling", "vomiting", "excessive_thirst", "excessive_urination", "lethargy"},
        "description": "Abnormal vascular connection bypassing the liver.",
        "description_ja": "肝臓を迂回する異常な血管接続で肝性脳症を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Uroabdomen",
        "name_ja": "尿腹",
        "symptoms": {"lethargy", "vomiting", "bloated_abdomen", "appetite_loss", "collapse"},
        "description": "Leakage of urine into the abdominal cavity.",
        "description_ja": "尿路破裂により尿が腹腔内に漏出する状態です。",
        "urgency": "emergency",
    },
    {
        "name": "Bile Peritonitis",
        "name_ja": "胆汁性腹膜炎",
        "symptoms": {"vomiting", "abdominal_pain", "lethargy", "fever", "appetite_loss"},
        "description": "Leakage of bile into the abdomen.",
        "description_ja": "胆嚢または胆管の破裂により胆汁が腹腔に漏出します。",
        "urgency": "emergency",
    },
    {
        "name": "Salivary Mucocele",
        "name_ja": "唾液腺嚢腫",
        "symptoms": {"swelling", "drooling", "appetite_loss"},
        "description": "Accumulation of saliva in tissues adjacent to damaged salivary gland.",
        "description_ja": "損傷した唾液腺に隣接する組織への唾液貯留です。",
        "urgency": "normal",
    },
    {
        "name": "Immune-Mediated Polyarthritis",
        "name_ja": "免疫介在性多発性関節炎",
        "symptoms": {"swollen_joints", "stiffness", "fever", "lethargy", "appetite_loss"},
        "description": "Autoimmune inflammation of multiple joints.",
        "description_ja": "複数の関節の自己免疫性炎症です。",
        "pathophysiology_ja": "関節滑膜への免疫複合体沈着→補体活性化→好中球浸潤→滑膜炎→関節液の好中球性多細胞症。非びらん性（Type I〜IV、犬で最多）：軟骨・骨の破壊なし。びらん性（関節リウマチ）：パンヌス形成→軟骨・骨の進行性破壊。複数の関節が同時に対称性に侵される。移動性跛行（shifting lameness）が特徴的。",
        "causes_ja": "一次性/特発性（Type I、最多）。二次性：腫瘍（リンパ腫・白血病）、感染症（Ehrlichia・Borrelia）、薬剤性（サルファ剤）、ワクチン後、IBD関連。全犬種に発症するが、スパニエル、ボクサーに報告多い。中年犬。関節液の分析（FNA→好中球性）で確定診断。",
        "prevention_ja": "確実な予防法はない。原因不明の発熱＋多発性跛行＋関節腫脹では本疾患を疑い関節穿刺を実施。免疫抑制療法（プレドニゾロン→レフルノミド/アザチオプリン併用）で管理。",
        "urgency": "urgent",
    },
    {
        "name": "Extraocular Myositis",
        "name_ja": "外眼筋炎",
        "symptoms": {"eye_redness", "squinting", "swelling"},
        "description": "Immune-mediated inflammation of the extraocular muscles.",
        "description_ja": "外眼筋の免疫介在性炎症です。",
        "urgency": "urgent",
    },
    {
        "name": "Immune-Mediated Thrombocytopenia (ITP)",
        "name_ja": "免疫介在性血小板減少症",
        "symptoms": {"skin_lesions", "bloody_stool", "blood_urine", "lethargy"},
        "description": "Autoimmune destruction of platelets causing bleeding.",
        "description_ja": "血小板の自己免疫性破壊により出血を引き起こします。",
        "urgency": "emergency",
    },
    {
        "name": "Immune-Mediated Hemolytic Anemia (IMHA)",
        "name_ja": "免疫介在性溶血性貧血",
        "symptoms": {"lethargy", "collapse", "excessive_panting", "appetite_loss", "vomiting"},
        "description": "Autoimmune destruction of red blood cells.",
        "description_ja": "赤血球の自己免疫性破壊による貧血です。",
        "pathophysiology_ja": "抗赤血球自己抗体（IgG/IgM）→赤血球表面に結合→(1)脾臓マクロファージによる血管外溶血（球状赤血球化・脾腫）、(2)補体活性化→血管内溶血（ヘモグロビン尿・黄疸）。急性重症型はPCV<15%に急速に低下。DICの合併が高率（50%）で予後不良因子。血栓塞栓症（肺塞栓）が主要な死因。",
        "causes_ja": "一次性（特発性、約75%）：自己免疫性。二次性：腫瘍（リンパ腫）、感染症（Babesia・Ehrlichia・Mycoplasma haemocanis）、薬剤性、ワクチン後、蜂刺傷後。コッカースパニエル、プードル、バイション・フリーゼ、オールドイングリッシュシープドッグに好発。中年雌犬に多い。",
        "prevention_ja": "確実な予防法はない。急性貧血（粘膜蒼白・頻脈・嗜眠）の早期受診。再発率20〜30%。マダニ媒介感染症の予防（二次性IMHA予防）。ITP併発（Evans症候群）に注意。",
        "urgency": "emergency",
    },
    {
        "name": "Canine Chronic Hepatitis",
        "name_ja": "犬慢性肝炎",
        "symptoms": {"vomiting", "appetite_loss", "weight_loss", "excessive_thirst", "lethargy"},
        "description": "Chronic inflammation of the liver leading to fibrosis and cirrhosis.",
        "description_ja": "肝臓の慢性炎症で線維化と肝硬変に至ります。",
        "urgency": "urgent",
    },
    {
        "name": "Copper Storage Hepatopathy",
        "name_ja": "銅蓄積性肝症",
        "symptoms": {"vomiting", "appetite_loss", "lethargy", "weight_loss", "excessive_thirst"},
        "description": "Excessive copper accumulation in the liver causing hepatitis.",
        "description_ja": "肝臓への過剰な銅蓄積により肝炎を引き起こします。",
        "urgency": "urgent",
    },
    {
        "name": "Perianal Fistula",
        "name_ja": "肛門周囲瘻",
        "symptoms": {"bloody_stool", "constipation", "pain_on_touch", "itching"},
        "description": "Chronic draining tracts around the anus, common in German Shepherds.",
        "description_ja": "肛門周囲の慢性瘻管でジャーマンシェパードに多いです。",
        "pathophysiology_ja": "肛門周囲の皮膚・肛門嚢・直腸壁の慢性炎症→瘻管（sinus tract）形成→持続的な排膿・出血・悪臭。免疫介在性の要素が大きい（IBDの腸管外症状と類似）。肛門の尾根部位に好発し、尾の位置が低い犬種では通気性低下が悪化因子。排便時の激しい疼痛→しぶり・排便忌避→便秘。",
        "causes_ja": "免疫介在性の病態（T細胞介在性）。好発：ジャーマンシェパード（圧倒的に多い、約84%）、アイリッシュセッター。低い尾根・広い肛門周囲皮膚皺が解剖学的リスク因子。IBDとの併存あり。食物アレルギーの関与も示唆。",
        "prevention_ja": "確実な予防法はない。シクロスポリン（5mg/kg/日）が第一選択薬（奏効率80〜90%）。タクロリムス外用併用。食事管理（新奇蛋白食）。外科的治療は免疫抑制療法が無効な場合のみ検討。",
        "urgency": "normal",
    },
    {
        "name": "Idiopathic Epilepsy",
        "name_ja": "特発性てんかん",
        "symptoms": {"seizures", "collapse", "drooling", "anxiety"},
        "description": "Recurrent seizures with no identifiable underlying cause.",
        "description_ja": "原因不明の再発性痙攣発作です。",
        "urgency": "urgent",
    },
    {
        "name": "Ventricular Premature Complexes",
        "name_ja": "心室性期外収縮",
        "symptoms": {"collapse", "lethargy", "excessive_panting"},
        "description": "Abnormal heartbeats originating from the ventricles.",
        "description_ja": "心室から発生する異常な心拍です。",
        "urgency": "urgent",
    },
    {
        "name": "Aortic Thromboembolism",
        "name_ja": "大動脈血栓塞栓症",
        "symptoms": {"limping_rl", "limping_rr", "collapse", "pain_on_touch"},
        "description": "Blood clot lodging in the aorta causing hind limb ischemia.",
        "description_ja": "大動脈に血栓が詰まり後肢の虚血を引き起こします。",
        "urgency": "emergency",
    },
    {
        "name": "Protein-Losing Nephropathy",
        "name_ja": "蛋白漏出性腎症",
        "symptoms": {"swelling", "weight_loss", "lethargy", "excessive_thirst", "excessive_urination"},
        "description": "Kidney disease causing excessive protein loss in urine.",
        "description_ja": "尿中への過剰な蛋白喪失を引き起こす腎疾患です。",
        "urgency": "urgent",
    },
    {
        "name": "Canine Influenza",
        "name_ja": "犬インフルエンザ",
        "symptoms": {"coughing", "nasal_discharge", "fever", "lethargy", "sneezing"},
        "description": "Highly contagious viral respiratory infection.",
        "description_ja": "高伝染性のウイルス性呼吸器感染症です。",
        "urgency": "normal",
    },
    {
        "name": "Aspergillosis (Nasal)",
        "name_ja": "鼻アスペルギルス症",
        "symptoms": {"nasal_discharge", "sneezing", "swelling", "pain_on_touch"},
        "description": "Fungal infection of the nasal cavity causing chronic nasal discharge.",
        "description_ja": "鼻腔の真菌感染症で慢性鼻水を引き起こします。",
        "urgency": "normal",
    },
    {
        "name": "Bronchoesophageal Fistula",
        "name_ja": "気管支食道瘻",
        "symptoms": {"coughing", "regurgitation", "difficulty_breathing", "fever"},
        "description": "Abnormal connection between the esophagus and bronchus.",
        "description_ja": "食道と気管支の間の異常な交通です。",
        "urgency": "urgent",
    },
    {
        "name": "Tracheal Hypoplasia",
        "name_ja": "気管低形成",
        "symptoms": {"difficulty_breathing", "coughing", "snoring", "rapid_breathing"},
        "description": "Congenital underdevelopment of the trachea in brachycephalic breeds.",
        "description_ja": "短頭種に見られる気管の先天的な発育不全です。",
        "urgency": "normal",
    },
    {
        "name": "Elongated Soft Palate",
        "name_ja": "軟口蓋過長症",
        "symptoms": {"snoring", "difficulty_breathing", "excessive_panting", "collapse"},
        "description": "Excessively long soft palate obstructing the airway in brachycephalic breeds.",
        "description_ja": "短頭種で軟口蓋が過長し気道を閉塞する疾患です。",
        "urgency": "urgent",
    },
    {
        "name": "Stenotic Nares",
        "name_ja": "鼻孔狭窄",
        "symptoms": {"snoring", "difficulty_breathing", "nasal_discharge", "reverse_sneezing"},
        "description": "Abnormally narrow nostrils restricting airflow in brachycephalic breeds.",
        "description_ja": "短頭種で鼻孔が異常に狭く気流を制限する疾患です。",
        "urgency": "normal",
    },
    {
        "name": "Hypoplastic Trachea",
        "name_ja": "低形成気管",
        "symptoms": {"coughing", "difficulty_breathing", "rapid_breathing"},
        "description": "Congenitally small tracheal diameter causing chronic respiratory issues.",
        "description_ja": "先天的に気管径が小さく慢性呼吸器問題を引き起こします。",
        "urgency": "normal",
    },
    # --- Rare Infectious Diseases ---
    {
        "name": "Canine Monocytic Ehrlichiosis",
        "name_ja": "犬単球性エールリヒア症",
        "symptoms": {"fever", "lethargy", "weight_loss", "appetite_loss", "nasal_discharge", "limping_fl", "limping_fr"},
        "description": "Tick-borne infection by Ehrlichia canis causing acute, subclinical, or chronic multi-systemic disease.",
        "description_ja": "エールリヒア・カニスによるダニ媒介感染症で、急性・不顕性・慢性の多臓器疾患を引き起こします。",
        "urgency": "high",
        "recommended_tests": ["blood_chemistry", "cbc", "tick_panel"],
    },
    {
        "name": "Canine Granulocytic Anaplasmosis",
        "name_ja": "犬顆粒球性アナプラズマ症",
        "symptoms": {"fever", "lethargy", "appetite_loss", "limping_fl", "limping_fr", "limping_rl", "limping_rr", "stiffness"},
        "description": "Tick-borne infection by Anaplasma phagocytophilum causing fever, joint pain, and thrombocytopenia.",
        "description_ja": "アナプラズマ・ファゴサイトフィルムによるダニ媒介感染症で、発熱・関節痛・血小板減少を引き起こします。",
        "urgency": "high",
        "recommended_tests": ["blood_chemistry", "cbc", "tick_panel"],
    },
    {
        "name": "Tularemia",
        "name_ja": "野兎病",
        "symptoms": {"fever", "lethargy", "appetite_loss", "swollen_joints", "swelling"},
        "description": "Bacterial infection by Francisella tularensis transmitted by ticks or contact with infected animals.",
        "description_ja": "フランシセラ・ツラレンシスによる細菌感染症で、ダニや感染動物との接触で伝播します。",
        "urgency": "high",
        "recommended_tests": ["blood_chemistry", "cbc", "serology"],
    },
    {
        "name": "Q Fever (Coxiellosis)",
        "name_ja": "Q熱（コクシエラ症）",
        "symptoms": {"fever", "lethargy", "appetite_loss", "weight_loss"},
        "description": "Zoonotic infection by Coxiella burnetii; often subclinical in dogs but may cause fever and reproductive issues.",
        "description_ja": "コクシエラ・バーネッティによる人獣共通感染症で、犬では不顕性が多いが発熱や生殖障害を引き起こすことがあります。",
        "urgency": "moderate",
        "recommended_tests": ["blood_chemistry", "cbc", "serology"],
    },
    {
        "name": "Brucella canis Infection",
        "name_ja": "ブルセラ・カニス感染症",
        "symptoms": {"lethargy", "fever", "swelling", "genital_discharge", "stiffness"},
        "description": "Bacterial infection causing reproductive failure, discospondylitis, and uveitis.",
        "description_ja": "細菌感染症で、繁殖障害・椎間板脊椎炎・ぶどう膜炎を引き起こします。",
        "urgency": "high",
        "recommended_tests": ["blood_chemistry", "cbc", "brucella_serology"],
    },
    {
        "name": "Lagenidiosis",
        "name_ja": "ラゲニジウム症",
        "symptoms": {"skin_lesions", "swelling", "lumps", "limping_rl", "limping_rr"},
        "description": "Oomycete infection causing progressive cutaneous and subcutaneous granulomatous lesions, often in limbs.",
        "description_ja": "卵菌感染症で、四肢に進行性の皮膚・皮下肉芽腫性病変を引き起こします。",
        "urgency": "high",
        "recommended_tests": ["biopsy", "culture", "histopathology"],
    },
    # --- Additional Cancers ---
    {
        "name": "Bronchogenic Carcinoma",
        "name_ja": "気管支原発性癌",
        "symptoms": {"coughing", "difficulty_breathing", "lethargy", "weight_loss", "appetite_loss"},
        "description": "Primary malignant tumor arising from bronchial epithelium, often causing chronic cough and respiratory distress.",
        "description_ja": "気管支上皮から発生する原発性悪性腫瘍で、慢性咳嗽や呼吸困難を引き起こします。",
        "urgency": "high",
        "recommended_tests": ["thoracic_xray", "ct_scan", "bronchoscopy", "biopsy"],
    },
    {
        "name": "Bladder Transitional Cell Carcinoma",
        "name_ja": "膀胱移行上皮癌",
        "symptoms": {"straining_urinate", "blood_urine", "excessive_urination", "incontinence"},
        "description": "Malignant tumor of the urinary bladder urothelium; most common bladder tumor in dogs.",
        "description_ja": "膀胱尿路上皮の悪性腫瘍で、犬の膀胱腫瘍として最も一般的です。",
        "urgency": "high",
        "recommended_tests": ["urinalysis", "abdominal_ultrasound", "cystoscopy", "biopsy"],
    },
    {
        "name": "Hepatocellular Carcinoma (Massive)",
        "name_ja": "肝細胞癌（巨塊型）",
        "symptoms": {"lethargy", "appetite_loss", "weight_loss", "bloated_abdomen", "vomiting"},
        "description": "Most common primary hepatic tumor in dogs; the massive form has the best surgical prognosis.",
        "description_ja": "犬で最も一般的な原発性肝腫瘍で、巨塊型は外科的予後が最も良好です。",
        "urgency": "high",
        "recommended_tests": ["blood_chemistry", "abdominal_ultrasound", "ct_scan", "biopsy"],
    },
    {
        "name": "Biliary Carcinoma",
        "name_ja": "胆管癌",
        "symptoms": {"lethargy", "appetite_loss", "weight_loss", "vomiting", "bloated_abdomen"},
        "description": "Malignant tumor of the bile duct epithelium causing biliary obstruction and hepatic dysfunction.",
        "description_ja": "胆管上皮の悪性腫瘍で、胆道閉塞と肝機能障害を引き起こします。",
        "urgency": "high",
        "recommended_tests": ["blood_chemistry", "abdominal_ultrasound", "biopsy"],
    },
    {
        "name": "Cholangiocellular Carcinoma",
        "name_ja": "胆管細胞癌",
        "symptoms": {"lethargy", "appetite_loss", "weight_loss", "vomiting", "bloated_abdomen", "dehydration"},
        "description": "Intrahepatic bile duct carcinoma with high metastatic potential; second most common hepatic tumor.",
        "description_ja": "肝内胆管から発生する癌で転移性が高く、肝臓腫瘍として2番目に多い腫瘍です。",
        "urgency": "high",
        "recommended_tests": ["blood_chemistry", "abdominal_ultrasound", "ct_scan", "biopsy"],
    },
    {
        "name": "Renal Carcinoma",
        "name_ja": "腎臓癌",
        "symptoms": {"weight_loss", "appetite_loss", "blood_urine", "lethargy", "excessive_thirst"},
        "description": "Primary malignant tumor of the kidney; may cause hematuria, abdominal mass, and paraneoplastic syndromes.",
        "description_ja": "腎臓の原発性悪性腫瘍で、血尿・腹部腫瘤・腫瘍随伴症候群を引き起こすことがあります。",
        "urgency": "high",
        "recommended_tests": ["blood_chemistry", "urinalysis", "abdominal_ultrasound", "ct_scan"],
    },
    {
        "name": "Adrenal Cortical Carcinoma",
        "name_ja": "副腎皮質癌",
        "symptoms": {"excessive_thirst", "excessive_urination", "weight_gain", "hair_loss", "bloated_abdomen", "excessive_panting"},
        "description": "Malignant tumor of the adrenal cortex causing Cushing's-like signs or local invasion.",
        "description_ja": "副腎皮質の悪性腫瘍で、クッシング様症状や局所浸潤を引き起こします。",
        "urgency": "high",
        "recommended_tests": ["blood_chemistry", "acth_stimulation", "abdominal_ultrasound", "ct_scan"],
    },
    {
        "name": "Glomus Tumor",
        "name_ja": "グロムス腫瘍",
        "symptoms": {"limping_fl", "limping_fr", "pain_on_touch", "swelling"},
        "description": "Rare tumor of the glomus body, typically found in the digits causing pain and lameness.",
        "description_ja": "グロムス小体の稀な腫瘍で、通常趾に発生し疼痛と跛行を引き起こします。",
        "urgency": "moderate",
        "recommended_tests": ["xray", "biopsy", "histopathology"],
    },
    {
        "name": "Myxosarcoma",
        "name_ja": "粘液肉腫",
        "symptoms": {"lumps", "swelling", "pain_on_touch", "lethargy"},
        "description": "Malignant mesenchymal tumor producing abundant myxoid matrix; locally invasive with low metastatic rate.",
        "description_ja": "豊富な粘液基質を産生する悪性間葉系腫瘍で、局所浸潤性が高いが転移率は低いです。",
        "urgency": "moderate",
        "recommended_tests": ["biopsy", "ct_scan", "histopathology"],
    },
    {
        "name": "Liposarcoma",
        "name_ja": "脂肪肉腫",
        "symptoms": {"lumps", "swelling", "weight_loss", "lethargy"},
        "description": "Malignant tumor of adipose tissue; locally aggressive but metastasis is uncommon.",
        "description_ja": "脂肪組織の悪性腫瘍で、局所的に攻撃性が高いが転移は稀です。",
        "urgency": "moderate",
        "recommended_tests": ["biopsy", "ct_scan", "histopathology"],
    },
    {
        "name": "Leiomyoma",
        "name_ja": "平滑筋腫",
        "symptoms": {"vomiting", "diarrhea", "weight_loss", "appetite_loss"},
        "description": "Benign smooth muscle tumor most commonly found in the gastrointestinal tract or reproductive organs.",
        "description_ja": "消化管や生殖器に最も多く見られる良性の平滑筋腫瘍です。",
        "urgency": "low",
        "recommended_tests": ["abdominal_ultrasound", "biopsy", "histopathology"],
    },
    {
        "name": "Rhabdomyosarcoma",
        "name_ja": "横紋筋肉腫",
        "symptoms": {"lumps", "swelling", "pain_on_touch", "lethargy", "weight_loss"},
        "description": "Rare malignant tumor of striated muscle; highly aggressive with early metastatic potential.",
        "description_ja": "横紋筋の稀な悪性腫瘍で、攻撃性が高く早期転移の可能性があります。",
        "urgency": "high",
        "recommended_tests": ["biopsy", "ct_scan", "thoracic_xray", "histopathology"],
    },
    {
        "name": "Mesothelioma",
        "name_ja": "中皮腫",
        "symptoms": {"difficulty_breathing", "bloated_abdomen", "lethargy", "weight_loss", "appetite_loss"},
        "description": "Rare tumor of serosal surfaces (pleura, peritoneum, pericardium) causing effusion and respiratory distress.",
        "description_ja": "漿膜面（胸膜・腹膜・心膜）の稀な腫瘍で、滲出液貯留や呼吸困難を引き起こします。",
        "urgency": "high",
        "recommended_tests": ["thoracic_xray", "abdominal_ultrasound", "cytology", "biopsy"],
    },
    # --- Orthopedic ---
    {
        "name": "Quadriceps Contracture",
        "name_ja": "大腿四頭筋拘縮",
        "symptoms": {"limping_rl", "limping_rr", "stiffness", "reluctance_move", "pain_on_touch"},
        "description": "Fibrosis and contracture of the quadriceps muscle group, often following femoral fracture in young dogs.",
        "description_ja": "大腿四頭筋群の線維化と拘縮で、若齢犬の大腿骨骨折後に多く見られます。",
        "urgency": "moderate",
        "recommended_tests": ["xray", "orthopedic_exam"],
    },
    {
        "name": "Tarsal Osteochondritis Dissecans (OCD)",
        "name_ja": "足根関節離断性骨軟骨炎",
        "symptoms": {"limping_rl", "limping_rr", "swollen_joints", "stiffness"},
        "description": "Developmental cartilage defect of the tarsal (hock) joint causing lameness in large breed dogs.",
        "description_ja": "足根（飛節）関節の発達性軟骨欠損で、大型犬に跛行を引き起こします。",
        "urgency": "moderate",
        "recommended_tests": ["xray", "ct_scan", "arthroscopy"],
    },
    {
        "name": "Shoulder Osteochondritis Dissecans (OCD)",
        "name_ja": "肩関節離断性骨軟骨炎",
        "symptoms": {"limping_fl", "limping_fr", "stiffness", "pain_on_touch"},
        "description": "Developmental cartilage defect of the humeral head causing forelimb lameness in young large breed dogs.",
        "description_ja": "上腕骨頭の発達性軟骨欠損で、若齢大型犬に前肢跛行を引き起こします。",
        "urgency": "moderate",
        "recommended_tests": ["xray", "ct_scan", "arthroscopy"],
    },
    {
        "name": "Elbow Incongruity",
        "name_ja": "肘関節不適合",
        "symptoms": {"limping_fl", "limping_fr", "stiffness", "swollen_joints"},
        "description": "Mismatch in the articular surfaces of the elbow joint contributing to elbow dysplasia and osteoarthritis.",
        "description_ja": "肘関節面の不適合で、肘異形成や変形性関節症の原因となります。",
        "urgency": "moderate",
        "recommended_tests": ["xray", "ct_scan"],
    },
    {
        "name": "Pes Varus",
        "name_ja": "内反足",
        "symptoms": {"limping_rl", "limping_rr", "stiffness"},
        "description": "Inward angular limb deformity of the distal tibia, most common in Dachshunds.",
        "description_ja": "脛骨遠位の内反変形で、ダックスフントに最も多く見られます。",
        "urgency": "moderate",
        "recommended_tests": ["xray", "ct_scan"],
    },
    {
        "name": "Metacarpal/Metatarsal Fracture",
        "name_ja": "中手骨/中足骨骨折",
        "symptoms": {"limping_fl", "limping_fr", "limping_rl", "limping_rr", "swelling", "pain_on_touch"},
        "description": "Fracture of the metacarpal or metatarsal bones due to trauma; may cause non-weight-bearing lameness.",
        "description_ja": "外傷による中手骨または中足骨の骨折で、荷重不能な跛行を引き起こすことがあります。",
        "urgency": "high",
        "recommended_tests": ["xray"],
    },
    # --- Neurological ---
    {
        "name": "Cerebellar Abiotrophy",
        "name_ja": "小脳変性症",
        "symptoms": {"circling", "stiffness", "seizures", "head_tilting"},
        "description": "Premature degeneration of cerebellar neurons causing progressive ataxia and intention tremor in specific breeds.",
        "description_ja": "小脳神経細胞の早期変性で、特定犬種に進行性の運動失調と企図振戦を引き起こします。",
        "urgency": "moderate",
        "recommended_tests": ["mri", "neurologic_exam"],
    },
    {
        "name": "Dancing Doberman Disease",
        "name_ja": "ダンシング・ドーベルマン病",
        "symptoms": {"limping_rl", "limping_rr", "stiffness", "reluctance_move"},
        "description": "Progressive neuromyopathy of Doberman Pinschers causing alternating flexion of the pelvic limbs while standing.",
        "description_ja": "ドーベルマン・ピンシャーの進行性神経筋障害で、起立時に後肢を交互に屈曲させます。",
        "urgency": "low",
        "recommended_tests": ["emg", "neurologic_exam", "muscle_biopsy"],
    },
    {
        "name": "Laryngeal Paralysis-Polyneuropathy Complex (GOLPP)",
        "name_ja": "喉頭麻痺-多発神経障害複合（GOLPP）",
        "symptoms": {"difficulty_breathing", "coughing", "stiffness", "limping_rl", "limping_rr", "excessive_panting"},
        "description": "Geriatric onset polyneuropathy presenting with laryngeal paralysis and progressive hindlimb weakness.",
        "description_ja": "老齢発症の多発神経障害で、喉頭麻痺と進行性後肢虚弱を呈します。",
        "urgency": "moderate",
        "recommended_tests": ["laryngeal_exam", "emg", "neurologic_exam"],
    },
    {
        "name": "Trigeminal Neuritis",
        "name_ja": "三叉神経炎",
        "symptoms": {"drooling", "appetite_loss", "dehydration"},
        "description": "Idiopathic inflammation of the trigeminal nerve causing acute-onset dropped jaw and inability to close the mouth.",
        "description_ja": "三叉神経の特発性炎症で、急性の下顎下垂と口を閉じられなくなる症状を引き起こします。",
        "urgency": "moderate",
        "recommended_tests": ["neurologic_exam", "mri"],
    },
    {
        "name": "Facial Nerve Paralysis",
        "name_ja": "顔面神経麻痺",
        "symptoms": {"drooling", "eye_discharge", "ear_discharge"},
        "description": "Unilateral or bilateral loss of facial nerve function causing drooped ear, lip, and inability to blink.",
        "description_ja": "片側性または両側性の顔面神経機能喪失で、耳・唇の垂れ下がりや瞬きの障害を引き起こします。",
        "urgency": "moderate",
        "recommended_tests": ["neurologic_exam", "mri", "emg"],
    },
    {
        "name": "Chiari-like Malformation",
        "name_ja": "キアリ様奇形",
        "symptoms": {"pain_on_touch", "scratching", "circling", "seizures"},
        "description": "Caudal fossa overcrowding causing cerebellar herniation; common in Cavalier King Charles Spaniels.",
        "description_ja": "後頭蓋窩の過密による小脳ヘルニアで、キャバリア・キング・チャールズ・スパニエルに多く見られます。",
        "urgency": "moderate",
        "recommended_tests": ["mri", "neurologic_exam"],
    },
    # --- Toxicology ---
    {
        "name": "Ethanol Toxicosis",
        "name_ja": "エタノール中毒",
        "symptoms": {"vomiting", "lethargy", "circling", "collapse", "seizures", "difficulty_breathing"},
        "description": "Toxicosis from ingestion of alcoholic beverages or fermenting dough causing CNS depression and metabolic acidosis.",
        "description_ja": "アルコール飲料や発酵生地の摂取による中毒で、中枢神経抑制と代謝性アシドーシスを引き起こします。",
        "urgency": "emergency",
        "recommended_tests": ["blood_chemistry", "blood_gas"],
    },
    {
        "name": "Organophosphate Toxicosis",
        "name_ja": "有機リン中毒",
        "symptoms": {"drooling", "vomiting", "diarrhea", "seizures", "difficulty_breathing", "excessive_urination"},
        "description": "Cholinesterase inhibitor poisoning causing SLUDGE signs (salivation, lacrimation, urination, defecation, GI distress, emesis).",
        "description_ja": "コリンエステラーゼ阻害剤中毒で、SLUDGE徴候（流涎・流涙・排尿・排便・消化器症状・嘔吐）を引き起こします。",
        "urgency": "emergency",
        "recommended_tests": ["blood_chemistry", "cholinesterase_level"],
    },
    {
        "name": "Pyrethrin/Permethrin Toxicosis (Canine)",
        "name_ja": "ピレスリン/ペルメトリン中毒（犬）",
        "symptoms": {"seizures", "drooling", "vomiting", "stiffness"},
        "description": "Toxicosis from excessive pyrethrin/permethrin exposure causing muscle tremors and seizures.",
        "description_ja": "ピレスリン/ペルメトリンの過量暴露による中毒で、筋振戦や痙攣を引き起こします。",
        "urgency": "emergency",
        "recommended_tests": ["neurologic_exam", "blood_chemistry"],
    },
    {
        "name": "Zinc Toxicosis",
        "name_ja": "亜鉛中毒",
        "symptoms": {"vomiting", "diarrhea", "lethargy", "appetite_loss", "bloody_stool"},
        "description": "Toxicosis from ingestion of zinc-containing objects (coins, hardware) causing hemolytic anemia and GI signs.",
        "description_ja": "亜鉛含有物（硬貨・金具）の摂取による中毒で、溶血性貧血と消化器症状を引き起こします。",
        "pathophysiology_ja": "摂取した亜鉛含有物が胃酸で溶解→血中亜鉛濃度の上昇→赤血球膜の酸化的損傷→ハインツ小体形成→血管内溶血→溶血性貧血・ヘモグロビン尿→急性腎障害。胃粘膜の直接腐食→嘔吐・下痢。膵臓への直接毒性→膵炎。多臓器不全に進展しうる。",
        "causes_ja": "日本の1円硬貨（100%亜鉛）、米国のペニー（1982年以降は97.5%亜鉛）、ボルト・ナット・ジッパー・亜鉛メッキ金属部品、亜鉛含有軟膏（酸化亜鉛）。腹部X線で金属異物を確認。犬は硬貨を飲み込みやすい。",
        "prevention_ja": "小さな金属物品・硬貨のペットからの隔離、亜鉛含有軟膏の犬の舐められない部位への使用、子犬の環境整備（硬貨や小物の放置禁止）。",
        "urgency": "emergency",
        "recommended_tests": ["blood_chemistry", "cbc", "abdominal_xray"],
    },
    {
        "name": "Strychnine Poisoning",
        "name_ja": "ストリキニーネ中毒",
        "symptoms": {"seizures", "stiffness", "difficulty_breathing", "collapse"},
        "description": "Rodenticide poisoning causing severe muscle rigidity and tonic-clonic seizures triggered by stimulation.",
        "description_ja": "殺鼠剤中毒で、刺激誘発性の重度筋硬直と強直間代痙攣を引き起こします。",
        "urgency": "emergency",
        "recommended_tests": ["toxicology_screen", "blood_chemistry"],
    },
    {
        "name": "Iron Toxicosis",
        "name_ja": "鉄中毒",
        "symptoms": {"vomiting", "bloody_stool", "diarrhea", "lethargy", "collapse", "abdominal_pain"},
        "description": "Toxicosis from ingestion of iron-containing supplements or products causing GI necrosis and hepatic failure.",
        "description_ja": "鉄含有サプリメント等の摂取による中毒で、消化管壊死や肝不全を引き起こします。",
        "urgency": "emergency",
        "recommended_tests": ["blood_chemistry", "serum_iron_level", "abdominal_xray"],
    },
    {
        "name": "Vitamin D Toxicosis",
        "name_ja": "ビタミンD中毒",
        "symptoms": {"excessive_thirst", "excessive_urination", "vomiting", "appetite_loss", "lethargy", "weight_loss"},
        "description": "Toxicosis from cholecalciferol rodenticides or supplements causing hypercalcemia and renal failure.",
        "description_ja": "コレカルシフェロール殺鼠剤やサプリメントによる中毒で、高カルシウム血症と腎不全を引き起こします。",
        "pathophysiology_ja": "コレカルシフェロール（ビタミンD3）の過剰摂取→肝臓で25-OHD3に変換→活性型1,25-(OH)2D3の上昇→腸管Ca吸収増加＋骨からのCa動員→高カルシウム血症→軟部組織の石灰化（腎臓・胃粘膜・血管壁・心筋）→急性腎障害→多臓器不全。効果が2〜3週間持続するため長期治療が必要。",
        "causes_ja": "コレカルシフェロール含有殺鼠剤（第三世代殺鼠剤）、ヒト用ビタミンDサプリメントの過剰摂取、乾癬治療用ビタミンD軟膏の摂取、ビタミンD過剰配合ペットフード（リコール事例あり）。毒性量は犬で0.1mg/kg以上。",
        "prevention_ja": "コレカルシフェロール殺鼠剤のペットからの隔離、ヒト用サプリメントの安全管理、ペットフードのリコール情報の確認。",
        "urgency": "emergency",
        "recommended_tests": ["blood_chemistry", "calcium_level", "urinalysis"],
    },
    # --- Breed-Specific and Other Conditions ---
    {
        "name": "Copper-Associated Chronic Hepatitis (Breed-Specific)",
        "name_ja": "銅関連慢性肝炎（犬種特異性）",
        "symptoms": {"lethargy", "appetite_loss", "vomiting", "weight_loss", "excessive_thirst"},
        "description": "Hereditary copper accumulation in hepatocytes causing progressive hepatitis; common in Bedlington Terriers, Labrador Retrievers, and Dobermans.",
        "description_ja": "肝細胞への遺伝性銅蓄積による進行性肝炎で、ベドリントン・テリア・ラブラドール・ドーベルマンに多く見られます。",
        "urgency": "high",
        "recommended_tests": ["blood_chemistry", "liver_biopsy", "hepatic_copper_quantification"],
    },
    {
        "name": "Basenji Fanconi-like Syndrome",
        "name_ja": "バセンジー型ファンコニ症候群",
        "symptoms": {"excessive_thirst", "excessive_urination", "weight_loss", "lethargy", "dehydration"},
        "description": "Inherited proximal renal tubular dysfunction in Basenjis causing glucosuria, aminoaciduria, and electrolyte wasting.",
        "description_ja": "バセンジーの遺伝性近位尿細管機能障害で、糖尿・アミノ酸尿・電解質喪失を引き起こします。",
        "urgency": "moderate",
        "recommended_tests": ["urinalysis", "blood_chemistry", "venous_blood_gas"],
    },
    {
        "name": "Dalmatian Hyperuricosuria",
        "name_ja": "ダルメシアン高尿酸尿症",
        "symptoms": {"straining_urinate", "blood_urine", "excessive_urination"},
        "description": "Breed-specific defect in uric acid metabolism predisposing to urate urolithiasis.",
        "description_ja": "犬種特異的な尿酸代謝異常で、尿酸塩尿石症の素因となります。",
        "urgency": "moderate",
        "recommended_tests": ["urinalysis", "abdominal_ultrasound", "urine_culture"],
    },
    {
        "name": "Cavalier King Charles Spaniel Mitral Valve Disease (Early-Onset)",
        "name_ja": "CKCS早期発症僧帽弁疾患",
        "symptoms": {"coughing", "difficulty_breathing", "lethargy", "collapse"},
        "description": "Breed-predisposed early-onset myxomatous mitral valve disease with rapid progression.",
        "description_ja": "犬種素因のある早期発症粘液腫様僧帽弁疾患で、急速に進行します。",
        "pathophysiology_ja": "僧帽弁尖の粘液腫様変性（GAG沈着→弁の肥厚・伸長・逸脱）→弁閉鎖不全→僧帽弁逆流→左房拡大→肺うっ血→心不全。CKCSは他犬種より5〜10年早く発症し、進行速度も速い。5歳で50%、10歳で100%近くが心雑音陽性。多遺伝子性の遺伝形式。併発するキアリ様奇形（CM/SM）も本犬種の問題。",
        "causes_ja": "多遺伝子性の遺伝的素因。CKCSの品種形成過程で僧帽弁変性の遺伝子が固定された。他犬種のMMVDと同じ疾患だが、発症年齢が顕著に若い（1〜3歳で心雑音検出例あり）。",
        "prevention_ja": "繁殖プロトコル（MVD Heart Screening Protocol：5歳以上で心雑音のない個体のみ繁殖許可）の遵守、定期的な心臓聴診・心エコー検査（年1回、5歳以降は半年毎）、ACVIM Stage B2でのピモベンダン早期投与（EPIC trial）。",
        "urgency": "high",
        "recommended_tests": ["echocardiogram", "thoracic_xray", "ecg"],
    },
    {
        "name": "German Shepherd Dog Exocrine Pancreatic Insufficiency",
        "name_ja": "ジャーマン・シェパード膵外分泌不全",
        "symptoms": {"weight_loss", "diarrhea", "appetite_increase", "excessive_gas"},
        "description": "Breed-predisposed pancreatic acinar atrophy causing maldigestion and malabsorption.",
        "description_ja": "犬種素因のある膵腺房萎縮で、消化不良と吸収不良を引き起こします。",
        "urgency": "moderate",
        "recommended_tests": ["tli_test", "blood_chemistry", "fecal_exam"],
    },
    {
        "name": "Boxer Arrhythmogenic Right Ventricular Cardiomyopathy",
        "name_ja": "ボクサー不整脈源性右室心筋症",
        "symptoms": {"collapse", "difficulty_breathing", "lethargy", "coughing"},
        "description": "Breed-specific cardiomyopathy with fibro-fatty replacement of right ventricular myocardium causing ventricular arrhythmias.",
        "description_ja": "右室心筋の線維脂肪置換による犬種特異的心筋症で、心室性不整脈を引き起こします。",
        "pathophysiology_ja": "デスモソーム蛋白（ストリアチン：STRN遺伝子変異）の異常→心筋細胞間接着障害→右室心筋の脂肪・線維組織への進行性置換→電気的不安定→心室期外収縮（VPC）→心室頻拍→失神・突然死。3つの表現型：(1)不整脈のみ（最多）、(2)心筋収縮障害→うっ血性心不全、(3)混合型。ホルター心電図で24時間中VPC>300個/日で疑い。",
        "causes_ja": "STRN遺伝子変異（常染色体優性、不完全浸透性）。ボクサーに特異的。ヘテロ接合体でも発症するが、ホモ接合体はより重篤。成犬で発症（4〜10歳が多い）。運動・興奮がVTの誘因。遺伝子検査（STRNスクリーニング）が可能。",
        "prevention_ja": "STRN遺伝子検査による繁殖管理（ホモ・ヘテロ陽性犬の繁殖制限）、定期的なホルター心電図モニタリング（年1回）、無症状キャリアの早期同定、激しい運動の制限。",
        "urgency": "high",
        "recommended_tests": ["echocardiogram", "ecg", "holter_monitor"],
    },
    {
        "name": "English Bulldog Hemivertebra",
        "name_ja": "イングリッシュ・ブルドッグ半椎体",
        "symptoms": {"limping_rl", "limping_rr", "stiffness", "reluctance_move", "incontinence"},
        "description": "Congenital vertebral malformation causing spinal cord compression; common in screw-tailed breeds.",
        "description_ja": "先天性椎骨奇形による脊髄圧迫で、巻尾犬種に多く見られます。",
        "urgency": "moderate",
        "recommended_tests": ["xray", "mri", "ct_scan"],
    },
    {
        "name": "Shar-Pei Fever (Familial Shar-Pei Fever)",
        "name_ja": "シャーペイ熱（家族性シャーペイ熱）",
        "symptoms": {"fever", "swollen_joints", "lethargy", "appetite_loss", "swelling"},
        "description": "Autoinflammatory disorder in Shar-Peis causing recurrent episodes of fever and swollen hocks; risk of systemic amyloidosis.",
        "description_ja": "シャーペイの自己炎症性疾患で、再発性の発熱と飛節腫脹を引き起こし、全身性アミロイドーシスのリスクがあります。",
        "urgency": "high",
        "recommended_tests": ["blood_chemistry", "cbc", "urinalysis", "amyloid_screening"],
    },
    {
        "name": "Doberman Dilated Cardiomyopathy (Occult)",
        "name_ja": "ドーベルマン潜在性拡張型心筋症",
        "symptoms": {"lethargy", "collapse", "difficulty_breathing", "coughing"},
        "description": "Breed-specific occult phase of DCM detectable by Holter monitoring before clinical signs appear.",
        "description_ja": "臨床症状が出現する前にホルター検査で検出可能なドーベルマン特異的なDCMの潜在期です。",
        "pathophysiology_ja": "PDK4遺伝子変異（ミトコンドリア代謝異常）およびTTN遺伝子変異（タイチン構造異常）→心筋細胞の進行性変性・線維化→左室拡大・収縮力低下。潜在期（Occult phase）：心雑音なし・臨床症状なし→ホルター心電図でVPC検出＋心エコーで左室拡大（LVIDD>46mm）。潜在期から臨床期へ移行後の生存期間中央値は3〜6ヶ月（心不全）または突然死。",
        "causes_ja": "PDK4遺伝子変異（北米系ドーベルマンの約40%がキャリア）、TTN遺伝子変異（ヨーロッパ系に多い）。常染色体優性遺伝。ドーベルマンの58%が生涯でDCMを発症するとの報告。オスはメスより早期・重症の傾向。3〜5歳からスクリーニング推奨。",
        "prevention_ja": "PDK4/TTN遺伝子検査による繁殖管理、3歳以降の年1回のホルター心電図＋心エコースクリーニング、潜在期のピモベンダン早期投与（PROTECT study）。キャリア犬への早期介入が発症遅延・生存期間延長に有効。",
        "urgency": "high",
        "recommended_tests": ["holter_monitor", "echocardiogram", "ecg", "nt_probnp"],
    },
    {
        "name": "Golden Retriever Pigmentary Uveitis",
        "name_ja": "ゴールデン・レトリーバー色素性ぶどう膜炎",
        "symptoms": {"eye_redness", "eye_discharge", "squinting"},
        "description": "Breed-specific bilateral pigment dispersion in the anterior chamber causing secondary glaucoma.",
        "description_ja": "犬種特異的な両側性前房色素分散で、続発性緑内障を引き起こします。",
        "urgency": "moderate",
        "recommended_tests": ["ophthalmic_exam", "tonometry"],
    },
    {
        "name": "West Highland White Terrier Pulmonary Fibrosis",
        "name_ja": "ウエスト・ハイランド・ホワイト・テリア肺線維症",
        "symptoms": {"coughing", "difficulty_breathing", "rapid_breathing", "lethargy"},
        "description": "Breed-specific idiopathic pulmonary fibrosis causing progressive respiratory distress.",
        "description_ja": "犬種特異的な特発性肺線維症で、進行性の呼吸困難を引き起こします。",
        "urgency": "high",
        "recommended_tests": ["thoracic_xray", "ct_scan", "blood_gas"],
    },
    {
        "name": "Bull Terrier Lethal Acrodermatitis",
        "name_ja": "ブル・テリア致死性肢端皮膚炎",
        "symptoms": {"skin_lesions", "hair_loss", "lethargy", "diarrhea"},
        "description": "Hereditary zinc metabolism defect in Bull Terriers causing severe skin lesions and immunodeficiency.",
        "description_ja": "ブル・テリアの遺伝性亜鉛代謝異常で、重度の皮膚病変と免疫不全を引き起こします。",
        "urgency": "high",
        "recommended_tests": ["skin_biopsy", "blood_chemistry", "zinc_level"],
    },
    {
        "name": "Shetland Sheepdog Dermatomyositis",
        "name_ja": "シェットランド・シープドッグ皮膚筋炎",
        "symptoms": {"skin_lesions", "hair_loss", "skin_redness", "stiffness"},
        "description": "Hereditary inflammatory disease of skin and muscle in Shelties and Collies causing facial alopecia and muscle atrophy.",
        "description_ja": "シェルティとコリーの皮膚・筋肉の遺伝性炎症性疾患で、顔面脱毛と筋萎縮を引き起こします。",
        "urgency": "moderate",
        "recommended_tests": ["skin_biopsy", "emg", "muscle_biopsy"],
    },
    {
        "name": "Miniature Schnauzer Hyperlipidemia",
        "name_ja": "ミニチュア・シュナウザー高脂血症",
        "symptoms": {"vomiting", "abdominal_pain", "lethargy", "appetite_loss"},
        "description": "Breed-predisposed idiopathic hyperlipidemia increasing risk of pancreatitis and gallbladder disease.",
        "description_ja": "犬種素因の特発性高脂血症で、膵炎や胆嚢疾患のリスクを増加させます。",
        "urgency": "moderate",
        "recommended_tests": ["blood_chemistry", "lipid_panel", "abdominal_ultrasound"],
    },
    {
        "name": "Chinese Crested Dog Multisystem Degeneration",
        "name_ja": "チャイニーズ・クレステッド多臓器変性症",
        "symptoms": {"circling", "seizures", "stiffness", "lethargy"},
        "description": "Progressive cerebellar and extrapyramidal degeneration in young Chinese Crested dogs.",
        "description_ja": "若齢チャイニーズ・クレステッドの進行性小脳・錐体外路変性です。",
        "urgency": "moderate",
        "recommended_tests": ["mri", "neurologic_exam"],
    },
    {
        "name": "Lagotto Romagnolo Juvenile Epilepsy",
        "name_ja": "ラゴット・ロマニョーロ若年性てんかん",
        "symptoms": {"seizures", "stiffness", "circling"},
        "description": "Breed-specific benign familial juvenile epilepsy with onset at 5-9 weeks; typically self-resolving by 4 months.",
        "description_ja": "5-9週齢で発症する犬種特異的な良性家族性若年性てんかんで、通常4ヶ月までに自然寛解します。",
        "urgency": "moderate",
        "recommended_tests": ["neurologic_exam", "eeg"],
    },
    {
        "name": "Bernese Mountain Dog Histiocytic Sarcoma Complex",
        "name_ja": "バーニーズ・マウンテン・ドッグ組織球肉腫複合",
        "symptoms": {"lethargy", "weight_loss", "appetite_loss", "difficulty_breathing", "limping_fl", "limping_fr"},
        "description": "Breed-predisposed aggressive malignancy arising from histiocytic cells; high incidence in Bernese Mountain Dogs.",
        "description_ja": "組織球系細胞から発生する犬種素因の攻撃的な悪性腫瘍で、バーニーズ・マウンテン・ドッグに高発生率です。",
        "urgency": "high",
        "recommended_tests": ["cytology", "biopsy", "ct_scan", "thoracic_xray"],
    },
    {
        "name": "Great Dane Gastric Dilatation-Volvulus Predisposition",
        "name_ja": "グレート・デーン胃拡張捻転素因",
        "symptoms": {"bloated_abdomen", "vomiting", "excessive_panting", "collapse", "drooling", "abdominal_pain"},
        "description": "Breed-predisposed emergency condition where the stomach dilates and rotates on its mesentery.",
        "description_ja": "胃が拡張し腸間膜を軸に回転する犬種素因の緊急疾患です。",
        "urgency": "emergency",
        "recommended_tests": ["abdominal_xray", "blood_chemistry", "ecg"],
    },
    {
        "name": "Newfoundland Subvalvular Aortic Stenosis",
        "name_ja": "ニューファンドランド大動脈弁下狭窄症",
        "symptoms": {"lethargy", "collapse", "difficulty_breathing", "coughing"},
        "description": "Breed-predisposed congenital narrowing below the aortic valve causing left ventricular outflow obstruction.",
        "description_ja": "犬種素因の先天性大動脈弁下狭窄で、左室流出路閉塞を引き起こします。",
        "urgency": "high",
        "recommended_tests": ["echocardiogram", "ecg"],
    },
    {
        "name": "Irish Wolfhound Dilated Cardiomyopathy",
        "name_ja": "アイリッシュ・ウルフハウンド拡張型心筋症",
        "symptoms": {"lethargy", "difficulty_breathing", "coughing", "collapse", "bloated_abdomen"},
        "description": "Breed-predisposed DCM with atrial fibrillation; among the highest breed incidence.",
        "description_ja": "心房細動を伴う犬種素因のDCMで、犬種別発生率が最も高い部類に入ります。",
        "urgency": "high",
        "recommended_tests": ["echocardiogram", "ecg", "holter_monitor"],
    },
    {
        "name": "Cocker Spaniel Immune-Mediated Hemolytic Anemia",
        "name_ja": "コッカー・スパニエル免疫介在性溶血性貧血",
        "symptoms": {"lethargy", "appetite_loss", "rapid_breathing", "collapse", "vomiting"},
        "description": "Breed-predisposed autoimmune destruction of red blood cells; higher incidence in Cocker Spaniels.",
        "description_ja": "犬種素因のある赤血球の自己免疫性破壊で、コッカー・スパニエルに高発生率です。",
        "urgency": "emergency",
        "recommended_tests": ["cbc", "blood_chemistry", "coombs_test", "reticulocyte_count"],
    },
    {
        "name": "Rottweiler Parvoviral Enteritis (Breed Susceptibility)",
        "name_ja": "ロットワイラー犬パルボウイルス腸炎（犬種感受性）",
        "symptoms": {"vomiting", "bloody_stool", "diarrhea", "lethargy", "fever", "dehydration", "appetite_loss"},
        "description": "Rottweilers show increased susceptibility and severity to canine parvovirus; requires aggressive fluid therapy.",
        "description_ja": "ロットワイラーは犬パルボウイルスに対する感受性と重症度が高く、積極的な輸液療法が必要です。",
        "urgency": "emergency",
        "recommended_tests": ["parvo_snap_test", "cbc", "blood_chemistry"],
    },
    {
        "name": "Labrador Retriever Exercise-Induced Collapse",
        "name_ja": "ラブラドール・レトリーバー運動誘発性虚脱",
        "symptoms": {"collapse", "stiffness", "lethargy", "excessive_panting"},
        "description": "Inherited dynamin-1 gene mutation causing episodic weakness and collapse after intense exercise.",
        "description_ja": "ダイナミン-1遺伝子の遺伝性変異による激しい運動後の発作性虚弱と虚脱です。",
        "urgency": "moderate",
        "recommended_tests": ["genetic_test", "neurologic_exam"],
    },
    {
        "name": "Poodle Sebaceous Adenitis",
        "name_ja": "プードル脂腺炎",
        "symptoms": {"hair_loss", "dry_skin", "skin_lesions", "itching"},
        "description": "Breed-predisposed immune-mediated destruction of sebaceous glands causing scaling and alopecia.",
        "description_ja": "犬種素因のある脂腺の免疫介在性破壊で、鱗屑と脱毛を引き起こします。",
        "urgency": "low",
        "recommended_tests": ["skin_biopsy", "dermatologic_exam"],
    },
    {
        "name": "German Shepherd Dog Perianal Fistula (Breed-Specific)",
        "name_ja": "ジャーマン・シェパード肛門周囲瘻（犬種特異性）",
        "symptoms": {"diarrhea", "bloody_stool", "constipation", "pain_on_touch", "lethargy"},
        "description": "Breed-predisposed chronic draining tracts around the anus; immune-mediated etiology suspected.",
        "description_ja": "犬種素因のある肛門周囲の慢性瘻管で、免疫介在性の病因が疑われています。",
        "urgency": "moderate",
        "recommended_tests": ["rectal_exam", "biopsy"],
    },
    {
        "name": "Scottish Terrier Bladder Cancer Predisposition",
        "name_ja": "スコティッシュ・テリア膀胱癌素因",
        "symptoms": {"straining_urinate", "blood_urine", "excessive_urination"},
        "description": "Scottish Terriers have 18-fold increased risk of bladder transitional cell carcinoma; screening recommended.",
        "description_ja": "スコティッシュ・テリアは膀胱移行上皮癌のリスクが18倍高く、スクリーニングが推奨されます。",
        "urgency": "moderate",
        "recommended_tests": ["urinalysis", "abdominal_ultrasound", "bvet_tcc_antigen_test"],
    },
    {
        "name": "Flat-Coated Retriever Histiocytic Sarcoma",
        "name_ja": "フラットコーテッド・レトリーバー組織球肉腫",
        "symptoms": {"lethargy", "weight_loss", "lumps", "limping_fl", "limping_fr", "appetite_loss"},
        "description": "Breed with very high predisposition to disseminated histiocytic sarcoma; early detection crucial.",
        "description_ja": "播種性組織球肉腫への素因が非常に高い犬種で、早期発見が重要です。",
        "urgency": "high",
        "recommended_tests": ["cytology", "biopsy", "ct_scan"],
    },
    {
        "name": "Weimaraner Hypertrophic Osteodystrophy (Breed-Specific)",
        "name_ja": "ワイマラナー肥大性骨異栄養症（犬種特異性）",
        "symptoms": {"fever", "swollen_joints", "limping_fl", "limping_fr", "limping_rl", "limping_rr", "appetite_loss", "lethargy"},
        "description": "Severe form of HOD in Weimaraners potentially linked to vaccination; can be life-threatening.",
        "description_ja": "ワイマラナーの重症型HODで、ワクチン接種との関連が示唆されており、致死的な場合があります。",
        "urgency": "high",
        "recommended_tests": ["xray", "blood_chemistry", "cbc"],
    },
    {
        "name": "Border Collie Trapped Neutrophil Syndrome",
        "name_ja": "ボーダー・コリー好中球封入症候群",
        "symptoms": {"fever", "lethargy", "weight_loss", "diarrhea"},
        "description": "Autosomal recessive disorder in Border Collies where neutrophils cannot exit the bone marrow despite hyperproduction.",
        "description_ja": "ボーダー・コリーの常染色体劣性遺伝疾患で、好中球が過剰産生されても骨髄から出られません。",
        "urgency": "high",
        "recommended_tests": ["cbc", "bone_marrow_biopsy", "genetic_test"],
    },
    {
        "name": "English Springer Spaniel Rage Syndrome",
        "name_ja": "イングリッシュ・スプリンガー・スパニエル激昂症候群",
        "symptoms": {"aggression_change", "seizures"},
        "description": "Breed-associated episodes of sudden unprovoked aggression; may represent a form of partial seizure.",
        "description_ja": "犬種関連の突然の無誘発性攻撃エピソードで、部分発作の一形態の可能性があります。",
        "urgency": "moderate",
        "recommended_tests": ["neurologic_exam", "eeg", "mri"],
    },
    {
        "name": "Akita Immune-Mediated Polyarthritis",
        "name_ja": "秋田犬免疫介在性多発性関節炎",
        "symptoms": {"fever", "swollen_joints", "limping_fl", "limping_fr", "limping_rl", "limping_rr", "stiffness", "lethargy"},
        "description": "Breed-predisposed immune-mediated non-erosive polyarthritis causing cyclic fever and joint swelling.",
        "description_ja": "犬種素因のある免疫介在性非びらん性多発性関節炎で、周期的な発熱と関節腫脹を引き起こします。",
        "urgency": "high",
        "recommended_tests": ["joint_fluid_analysis", "cbc", "blood_chemistry", "ana_test"],
    },
    {
        "name": "Alaskan Malamute Polyneuropathy",
        "name_ja": "アラスカン・マラミュート多発性神経障害",
        "symptoms": {"stiffness", "limping_rl", "limping_rr", "reluctance_move", "lethargy"},
        "description": "Hereditary demyelinating polyneuropathy in Alaskan Malamutes causing progressive weakness starting in hindlimbs.",
        "description_ja": "アラスカン・マラミュートの遺伝性脱髄性多発性神経障害で、後肢から始まる進行性の虚弱を引き起こします。",
        "urgency": "moderate",
        "recommended_tests": ["emg", "nerve_biopsy", "neurologic_exam"],
    },
    {
        "name": "Samoyed Hereditary Glomerulopathy",
        "name_ja": "サモエド遺伝性糸球体症",
        "symptoms": {"excessive_thirst", "excessive_urination", "weight_loss", "lethargy", "dehydration"},
        "description": "X-linked hereditary nephritis in Samoyeds causing progressive renal failure; males affected earlier and more severely.",
        "description_ja": "サモエドのX連鎖遺伝性腎炎で、進行性腎不全を引き起こし、雄がより早期・重度に罹患します。",
        "urgency": "high",
        "recommended_tests": ["urinalysis", "blood_chemistry", "renal_biopsy"],
    },
    {
        "name": "Shih Tzu Renal Dysplasia",
        "name_ja": "シー・ズー腎異形成",
        "symptoms": {"excessive_thirst", "excessive_urination", "weight_loss", "vomiting", "lethargy"},
        "description": "Congenital abnormal kidney development in Shih Tzus causing early-onset chronic kidney disease.",
        "description_ja": "シー・ズーの先天性腎臓発達異常で、早期発症の慢性腎臓病を引き起こします。",
        "urgency": "high",
        "recommended_tests": ["blood_chemistry", "urinalysis", "abdominal_ultrasound"],
    },
    {
        "name": "Canine Compulsive Flank Sucking (Doberman)",
        "name_ja": "ドーベルマン強迫性わき腹吸引",
        "symptoms": {"anxiety", "skin_lesions", "hair_loss"},
        "description": "Breed-specific compulsive disorder in Dobermans involving repetitive sucking of the flank skin.",
        "description_ja": "ドーベルマンの犬種特異的強迫性障害で、わき腹の皮膚を反復的に吸引します。",
        "urgency": "low",
        "recommended_tests": ["behavioral_assessment", "dermatologic_exam"],
    },
    {
        "name": "Canine Thyroid Storm",
        "name_ja": "犬甲状腺クリーゼ",
        "symptoms": {"fever", "rapid_breathing", "vomiting", "diarrhea", "collapse", "seizures"},
        "description": "Rare acute thyrotoxicosis in dogs with functional thyroid carcinoma causing multi-organ dysfunction.",
        "description_ja": "機能性甲状腺癌の犬における稀な急性甲状腺中毒症で、多臓器不全を引き起こします。",
        "urgency": "emergency",
        "recommended_tests": ["thyroid_panel", "blood_chemistry", "ecg"],
    },
    {
        "name": "Canine Hemophilia B",
        "name_ja": "犬血友病B",
        "symptoms": {"swelling", "limping_fl", "limping_fr", "limping_rl", "limping_rr", "bloody_stool"},
        "description": "X-linked factor IX deficiency causing recurrent hemorrhage into joints and soft tissues.",
        "description_ja": "X連鎖性第IX因子欠乏症で、関節や軟部組織への再発性出血を引き起こします。",
        "urgency": "high",
        "recommended_tests": ["coagulation_panel", "factor_ix_assay"],
    },
    {
        "name": "Idiopathic Immune-Mediated Myositis",
        "name_ja": "特発性免疫介在性筋炎",
        "symptoms": {"stiffness", "pain_on_touch", "reluctance_move", "lethargy", "fever"},
        "description": "Immune-mediated generalized muscle inflammation causing diffuse myalgia and weakness.",
        "description_ja": "免疫介在性の全身性筋炎で、びまん性筋痛と虚弱を引き起こします。",
        "urgency": "moderate",
        "recommended_tests": ["ck_level", "emg", "muscle_biopsy"],
    },
    {
        "name": "Canine Chronic Enteropathy (Non-IBD)",
        "name_ja": "犬慢性腸症（非IBD）",
        "symptoms": {"diarrhea", "weight_loss", "vomiting", "appetite_loss"},
        "description": "Chronic gastrointestinal signs responsive to diet, antibiotics, or immunosuppressants but not classified as classic IBD.",
        "description_ja": "食事・抗生物質・免疫抑制剤に反応する慢性消化器症状で、典型的なIBDに分類されないものです。",
        "urgency": "moderate",
        "recommended_tests": ["blood_chemistry", "fecal_exam", "abdominal_ultrasound", "intestinal_biopsy"],
    },
    {
        "name": "Hepatic Microvascular Dysplasia",
        "name_ja": "肝微小血管異形成（MVD）",
        "symptoms": {"vomiting", "diarrhea", "lethargy", "weight_loss"},
        "description": "Microscopic portal vascular malformation without macroscopic shunt causing mild hepatic dysfunction.",
        "description_ja": "肉眼的な門脈体循環シャント（PSS）を伴わない微小な肝内門脈血管の先天的異常。"
                          "ヨークシャーテリア、ケアンテリア、マルチーズ等に好発。"
                          "多くは無症候性で胆汁酸値の軽度上昇のみ。PSSとの鑑別が重要。",
        "pathophysiology_ja": "肝内の微小門脈分枝の先天的低形成→門脈血の一部が肝類洞を迂回→"
                              "軽度の肝機能低下。PSSほど重度ではなく、アンモニア代謝能は部分的に保たれる。"
                              "胆汁酸値は軽度〜中等度上昇するが、アンモニア値は正常〜軽度上昇。",
        "causes_ja": "先天的な肝内微小血管の発達異常。遺伝的素因（小型テリア犬種）。"
                     "PSSの修復術後に残存する微小シャントとしても見られることがある。",
        "treatment_ja": "多くは治療不要（無症候性の場合）。症候性の場合：肝臓サポート食（低〜中タンパク・高品質タンパク）、"
                        "ウルソデオキシコール酸、SAMe、ラクツロース（高アンモニア血症時）。"
                        "外科適応なし（微小血管の異常であり手術で矯正不可）。PSSとの鑑別診断が最も重要。",
        "prognosis_ja": "予後良好〜極めて良好。多くの症例で正常な寿命を全うする。"
                        "臨床症状が出ることは稀であり、偶発的に発見されることが多い。",
        "prevention_ja": "罹患犬の繁殖制限。好発品種では胆汁酸検査によるスクリーニング。",
        "urgency": "low",
        "recommended_tests": ["blood_chemistry", "bile_acids_test", "abdominal_ultrasound"],
    },
    {
        "name": "Canine Idiopathic Polyradiculoneuritis (Acute)",
        "name_ja": "犬急性特発性多発性神経根炎",
        "symptoms": {"limping_rl", "limping_rr", "limping_fl", "limping_fr", "stiffness", "difficulty_breathing"},
        "description": "Acute inflammatory demyelinating polyneuropathy (dog equivalent of Guillain-Barré syndrome) causing ascending paralysis.",
        "description_ja": "急性炎症性脱髄性多発性神経障害（ギラン・バレー症候群の犬版）で、上行性麻痺を引き起こします。",
        "urgency": "high",
        "recommended_tests": ["emg", "csf_analysis", "neurologic_exam"],
    },
    {
        "name": "Canine Hemangiopericytoma",
        "name_ja": "犬血管周皮腫",
        "symptoms": {"lumps", "swelling", "limping_fl", "limping_fr"},
        "description": "Locally invasive soft tissue tumor arising from perivascular cells; common on limbs of older large-breed dogs.",
        "description_ja": "血管周囲細胞から発生する局所浸潤性軟部組織腫瘍で、高齢大型犬の四肢に多く見られます。",
        "urgency": "moderate",
        "recommended_tests": ["biopsy", "ct_scan", "histopathology"],
    },
    {
        "name": "Canine Retroperitoneal Fibrosis",
        "name_ja": "犬後腹膜線維症",
        "symptoms": {"abdominal_pain", "straining_urinate", "constipation", "lethargy"},
        "description": "Rare fibroinflammatory condition of the retroperitoneum causing ureteral obstruction and renal compromise.",
        "description_ja": "後腹膜の稀な線維炎症性疾患で、尿管閉塞と腎障害を引き起こします。",
        "urgency": "high",
        "recommended_tests": ["abdominal_ultrasound", "ct_scan", "blood_chemistry"],
    },
    {
        "name": "Canine Splenic Nodular Hyperplasia",
        "name_ja": "犬脾臓結節性過形成",
        "symptoms": {"bloated_abdomen", "lethargy", "appetite_loss"},
        "description": "Benign splenic nodules common in older dogs; must be differentiated from hemangiosarcoma.",
        "description_ja": "高齢犬に一般的な良性脾臓結節で、血管肉腫との鑑別が必要です。",
        "urgency": "moderate",
        "recommended_tests": ["abdominal_ultrasound", "cytology", "biopsy"],
    },
    {
        "name": "Canine Necrotizing Sialometaplasia",
        "name_ja": "犬壊死性唾液腺化生",
        "symptoms": {"drooling", "appetite_loss", "swelling"},
        "description": "Self-limiting ischemic necrosis of salivary gland tissue causing oral/pharyngeal swelling; mimics malignancy.",
        "description_ja": "唾液腺組織の自己限定性虚血性壊死で口腔/咽頭の腫脹を引き起こし、悪性腫瘍に類似します。",
        "urgency": "moderate",
        "recommended_tests": ["biopsy", "histopathology"],
    },
    {
        "name": "Canine Myocardial Contusion",
        "name_ja": "犬心筋挫傷",
        "symptoms": {"lethargy", "difficulty_breathing", "collapse"},
        "description": "Cardiac bruising from blunt thoracic trauma causing arrhythmias and decreased cardiac output.",
        "description_ja": "鈍的胸部外傷による心臓打撲で、不整脈と心拍出量低下を引き起こします。",
        "urgency": "emergency",
        "recommended_tests": ["ecg", "echocardiogram", "cardiac_troponin"],
    },
    {
        "name": "Canine Bronchoesophageal Fistula (Congenital)",
        "name_ja": "犬先天性気管支食道瘻",
        "symptoms": {"coughing", "regurgitation", "difficulty_breathing", "fever"},
        "description": "Abnormal communication between bronchus and esophagus causing recurrent aspiration pneumonia.",
        "description_ja": "気管支と食道の異常な交通で、再発性誤嚥性肺炎を引き起こします。",
        "urgency": "high",
        "recommended_tests": ["thoracic_xray", "contrast_esophagram", "bronchoscopy"],
    },
    {
        "name": "Canine Spinal Arachnoid Cyst",
        "name_ja": "犬脊髄くも膜嚢胞",
        "symptoms": {"limping_rl", "limping_rr", "stiffness", "pain_on_touch", "incontinence"},
        "description": "CSF-filled cyst within the spinal arachnoid causing progressive myelopathy; common in large breeds.",
        "description_ja": "脊髄くも膜内の髄液嚢胞で進行性脊髄障害を引き起こし、大型犬に多く見られます。",
        "urgency": "moderate",
        "recommended_tests": ["mri", "ct_myelogram"],
    },
    {
        "name": "Canine Cricopharyngeal Dysphagia",
        "name_ja": "犬輪状咽頭嚥下障害",
        "symptoms": {"regurgitation", "coughing", "weight_loss", "nasal_discharge"},
        "description": "Failure of the cricopharyngeal muscle to relax during swallowing causing dysphagia and aspiration risk.",
        "description_ja": "嚥下時の輪状咽頭筋弛緩不全で、嚥下障害と誤嚥リスクを引き起こします。",
        "urgency": "moderate",
        "recommended_tests": ["fluoroscopy", "endoscopy"],
    },
    {
        "name": "Canine Pulmonary Alveolar Proteinosis",
        "name_ja": "犬肺胞蛋白症",
        "symptoms": {"coughing", "difficulty_breathing", "rapid_breathing", "lethargy"},
        "description": "Accumulation of surfactant-derived material in alveoli impairing gas exchange; rare in dogs.",
        "description_ja": "肺胞内のサーファクタント由来物質の蓄積によりガス交換が障害される犬の稀な疾患です。",
        "urgency": "high",
        "recommended_tests": ["thoracic_xray", "bronchoalveolar_lavage", "ct_scan"],
    },
    {
        "name": "Canine Primary Ciliary Dyskinesia (Breed-Specific)",
        "name_ja": "犬原発性繊毛運動不全症（犬種特異性）",
        "symptoms": {"coughing", "nasal_discharge", "sneezing", "difficulty_breathing"},
        "description": "Inherited ciliary motility defect causing chronic rhinosinusitis, bronchiectasis, and sometimes situs inversus.",
        "description_ja": "遺伝性繊毛運動障害で、慢性副鼻腔炎・気管支拡張症・時に内臓逆位を引き起こします。",
        "urgency": "moderate",
        "recommended_tests": ["thoracic_xray", "ciliary_biopsy", "electron_microscopy"],
    },
    {
        "name": "Canine Chronic Superficial Keratitis (Pannus) - Severe",
        "name_ja": "犬慢性表在性角膜炎（パンヌス）重症型",
        "symptoms": {"eye_redness", "eye_discharge", "squinting"},
        "description": "Severe progressive immune-mediated corneal vascularization and pigmentation; worst at high altitudes.",
        "description_ja": "重度の進行性免疫介在性角膜血管新生と色素沈着で、高地で悪化します。",
        "urgency": "moderate",
        "recommended_tests": ["ophthalmic_exam"],
    },
    {
        "name": "Canine Megaesophagus (Congenital)",
        "name_ja": "犬先天性巨大食道症",
        "symptoms": {"regurgitation", "coughing", "weight_loss", "nasal_discharge", "difficulty_breathing"},
        "description": "Congenital esophageal hypomotility causing regurgitation, malnutrition, and aspiration pneumonia risk.",
        "description_ja": "先天性食道運動低下で、吐出・栄養不良・誤嚥性肺炎のリスクを引き起こします。",
        "urgency": "high",
        "recommended_tests": ["thoracic_xray", "contrast_esophagram"],
    },
]

TEST_DB: List[Dict[str, Any]] = [
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
# Merge optional dog_disease_enrichment data
# ---------------------------------------------------------------------------
from importlib.util import find_spec as _find_spec

if _find_spec("api.dog_disease_enrichment") is not None:
    from api.dog_disease_enrichment import DOG_ENRICHMENT as _DOG_ENRICH

    _enrich_index = {d["name"]: d for d in DISEASES}
    for _name, _data in _DOG_ENRICH.items():
        if _name in _enrich_index:
            _enrich_index[_name].update(_data)
    del _enrich_index, _DOG_ENRICH

# ---------------------------------------------------------------------------
# Enrich diseases from JSON database
# ---------------------------------------------------------------------------
enrich_diseases(DISEASES, "Dog")

# ---------------------------------------------------------------------------
# Fill missing content fields with fallback for unenriched diseases
# ---------------------------------------------------------------------------
for _d in DISEASES:
    _name = _d.get("name", "")
    _name_ja = _d.get("name_ja", _name)
    _urg = _d.get("urgency", "moderate")
    _urg_ja = {"emergency": "緊急", "high": "高", "moderate": "中等度", "low": "軽度"}.get(_urg, "中等度")
    if not _d.get("pathophysiology") and not _d.get("pathophysiology_ja"):
        _d["pathophysiology"] = _d["pathophysiology_ja"] = (
            f"{_name_ja}は罹患組織および臓器系に病理学的変化をもたらす。"
            f"細胞障害・炎症反応・未治療の場合の組織損傷の段階を経て進行する。"
            f"早期の病態把握と介入が予後改善の鍵となる。")
    elif _d.get("pathophysiology_ja") and not _d.get("pathophysiology"):
        _d["pathophysiology"] = _d["pathophysiology_ja"]
    elif _d.get("pathophysiology") and not _d.get("pathophysiology_ja"):
        _d["pathophysiology_ja"] = _d["pathophysiology"]
    if not _d.get("causes") and not _d.get("causes_ja"):
        _d["causes"] = _d["causes_ja"] = (
            f"{_name_ja}の原因には遺伝的要因、環境要因、食事・飼育管理に関連する素因が含まれる。"
            f"複数の要因が複合的に作用することが多い。")
    elif _d.get("causes_ja") and not _d.get("causes"):
        _d["causes"] = _d["causes_ja"]
    elif _d.get("causes") and not _d.get("causes_ja"):
        _d["causes_ja"] = _d["causes"]
    if not _d.get("treatment") and not _d.get("treatment_ja"):
        _d["treatment"] = _d["treatment_ja"] = (
            f"{_name_ja}の治療: 獣医師による診断に基づく適切な治療計画が必要。"
            f"緊急度: {_urg_ja}。疼痛管理・輸液・栄養サポートを含む支持療法を基本とし、"
            f"原因に応じた特異的治療を実施。")
    elif _d.get("treatment_ja") and not _d.get("treatment"):
        _d["treatment"] = _d["treatment_ja"]
    elif _d.get("treatment") and not _d.get("treatment_ja"):
        _d["treatment_ja"] = _d["treatment"]
    if not _d.get("prevention") and not _d.get("prevention_ja"):
        _d["prevention"] = _d["prevention_ja"] = (
            f"{_name_ja}の予防には適切な栄養管理、定期的な健康診断、"
            f"ワクチン接種、寄生虫予防、安全な環境の維持が含まれる。")
    elif _d.get("prevention_ja") and not _d.get("prevention"):
        _d["prevention"] = _d["prevention_ja"]
    elif _d.get("prevention") and not _d.get("prevention_ja"):
        _d["prevention_ja"] = _d["prevention"]
    if not _d.get("prognosis") and not _d.get("prognosis_ja"):
        _d["prognosis"] = _d["prognosis_ja"] = (
            f"{_name_ja}の予後は重症度、診断の迅速さ、治療への反応に依存する。"
            f"早期発見と適切な介入が転帰を改善する。")
    elif _d.get("prognosis_ja") and not _d.get("prognosis"):
        _d["prognosis"] = _d["prognosis_ja"]
    elif _d.get("prognosis") and not _d.get("prognosis_ja"):
        _d["prognosis_ja"] = _d["prognosis"]

# Build SYMPTOM_CATEGORIES from disease symptoms
SYMPTOM_CATEGORIES = {
    "general": {"name_ja": "全身症状", "name_en": "General", "symptoms": [
        "lethargy", "fever", "weight_loss", "weight_gain", "appetite_loss",
        "appetite_increase", "excessive_thirst", "excessive_urination"
    ]},
    "digestive": {"name_ja": "消化器", "name_en": "Digestive", "symptoms": [
        "vomiting", "diarrhea", "constipation", "bloody_stool",
        "bloated_abdomen", "excessive_gas", "regurgitation",
        "vomiting_after_drinking", "drooling", "abdominal_pain", "dehydration"
    ]},
    "respiratory": {"name_ja": "呼吸器", "name_en": "Respiratory", "symptoms": [
        "coughing", "sneezing", "nasal_discharge", "difficulty_breathing",
        "rapid_breathing", "reverse_sneezing", "snoring"
    ]},
    "eyes_ears": {"name_ja": "眼・耳", "name_en": "Eyes/Ears", "symptoms": [
        "eye_redness", "eye_discharge", "squinting", "ear_scratching",
        "ear_odor", "head_tilting"
    ]},
    "skin": {"name_ja": "皮膚・被毛", "name_en": "Skin/Coat", "symptoms": [
        "itching", "hair_loss", "skin_redness", "lumps", "dry_skin", "hot_spots"
    ]},
    "musculoskeletal": {"name_ja": "筋骨格", "name_en": "Musculoskeletal", "symptoms": [
        "limping_fl", "limping_fr", "limping_rl", "limping_rr", "stiffness",
        "reluctance_move", "swollen_joints", "pain_on_touch"
    ]},
    "behavioral": {"name_ja": "行動", "name_en": "Behavioral", "symptoms": [
        "aggression_change", "anxiety", "excessive_panting", "hiding",
        "circling", "scratching", "seizures"
    ]},
    "urinary": {"name_ja": "泌尿・生殖器", "name_en": "Urinary/Reproductive", "symptoms": [
        "straining_urinate", "blood_urine", "incontinence", "genital_discharge"
    ]},
    "other": {"name_ja": "その他", "name_en": "Other", "symptoms": [
        "swelling", "collapse", "ear_discharge", "head_shaking", "skin_lesions"
    ]},
}


def analyze_symptoms(symptoms, age_stage="", breed=None, *, onset=None,
                     age_years=None, species=None, lab_values=None,
                     gender=None, vaccines=None, vaccination_status=None):
    """Analyze dog symptoms and return differential diagnosis."""
    prevalence_map = prevalence_data.SPECIES_PREVALENCE.get("dog", {})
    return analyze_symptoms_generic(
        symptoms=symptoms,
        diseases=DISEASES,
        symptom_names=SYMPTOM_NAMES,
        species="dog",
        advice=ADVICE,
        breed=breed,
        onset=onset,
        age_years=age_years,
        lab_values=lab_values,
        gender=gender,
        vaccines=vaccines,
        vaccination_status=vaccination_status,
        prevalence_map=prevalence_map,
    )
