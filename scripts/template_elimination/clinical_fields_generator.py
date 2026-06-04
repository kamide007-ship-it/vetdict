"""Disease-specific clinical fields generator.

Eliminates category-level template contamination in non-treatment JA fields
(``causes_ja``, ``prognosis_ja``, ``prevention_ja``, ``transmission_ja``,
``clinical_signs_ja``, ``differential_diagnosis_ja``, ``nutrition_management_ja``,
``prognosis_detailed_ja``, ``rehabilitation_protocol_ja``).

The pipeline previously addressed only ``treatment_ja``, leaving the other
clinical fields filled with category-level templates that — critically —
were often **mis-applied across categories**. Examples of damaging errors:

- ``transmission_ja: "腫瘍は感染性疾患ではない..."`` on FeLV (a contagious virus)
- ``causes_ja`` neoplasia template applied to FIV
- ``differential_diagnosis_ja`` metabolic template applied to nutritional diseases
- ``causes_ja`` parasite template applied to feline asthma

Strategy:

1. **Resolve the disease's true category** from disease name patterns
   (priority) with fallback to the tagged ``category`` field.
2. **Generate per-(species, disease, category, field) content** that includes
   the disease name in the lead sentence, making each output instance unique.
3. For *high-priority diseases* (FeLV, FIV, FIP, diabetes, hyperthyroidism,
   CKD, FLUTD, hyperadrenocorticism, etc.), use **curated, evidence-based,
   fully disease-specific** content (not just disease-name-prefixed templates).

The generator returns a dict mapping field name -> new text. Caller decides
which fields to actually overwrite (typically only those currently holding
template content).
"""

from __future__ import annotations

import re
from typing import Optional

# ---------------------------------------------------------------------------
# Category resolution
# ---------------------------------------------------------------------------

# Disease name patterns -> canonical category. First match wins; ordering
# matters (more specific patterns first).
NAME_CATEGORY_PATTERNS: list[tuple[re.Pattern, str]] = [
    # Viral infections (must come before neoplasia — FeLV / FIV cause lymphoma
    # but are themselves viral infections)
    (re.compile(r"FeLV|FIV|FIP|FCV|FHV|FPV|FCoV|FECV|FRV"), "viral_infection"),
    (
        re.compile(
            r"ウイルス|レトロウイルス|パルボウイルス|パルボ|ジステンパー|カリシウイルス|"
            r"カリシ|ヘルペスウイルス|ヘルペス|コロナウイルス|コロナ|インフルエンザ|"
            r"アデノウイルス|ロタウイルス|狂犬病|レオウイルス|パピローマウイルス|パピローマ|"
            r"PBFD|BFDV|サーコウイルス|ボルナ|ニューカッスル|マレック|鳥痘|オウム嘴羽病|"
            r"伝染性気管支炎|伝染性ファブリキウス嚢病|伝染性喉頭気管炎|"
            r"伝染性腹膜炎|伝染性肝炎|伝染性貧血|流産ウイルス|脳脊髄炎ウイルス|"
            r"日本脳炎|ウエストナイル|EHV|EIV|EAV|EVA|VHD|RHD|ミクソーマ|"
            r"白血病ウイルス|免疫不全ウイルス|エボラ|ボルナ病"
        ),
        "viral_infection",
    ),
    # Bacterial infections (specific bacterial diseases)
    (
        re.compile(
            r"パスツレラ|Pasteurella|ボルデテラ|Bordetella|クロストリジウム|Clostridium|"
            r"クラミジア|Chlamydia|マイコプラズマ|Mycoplasma|マイコバクテリア|Mycobacterium|"
            r"ブドウ球菌|Staphylococcus|連鎖球菌|Streptococcus|大腸菌|E\. coli|サルモネラ|"
            r"Salmonella|レプトスピラ|Leptospira|エールリッヒア|Ehrlichia|アナプラズマ|"
            r"Anaplasma|ライム病|Borrelia|ボレリア|破傷風|Tetanus|botulism|ボツリヌス|"
            r"野兎病|Tularemia|ブルセラ|Brucella|腺疫|Strangles|トレポネーマ|Treponema|"
            r"スピロヘータ|Spirochete|リステリア|Listeria|エルシニア|Yersinia|"
            r"バルトネラ|Bartonella|ヘモバルトネラ|ヘモプラズマ|hemoplasma|"
            r"猫ひっかき病|cat scratch|肺炎球菌|髄膜炎菌|淋菌|破傷風|"
            r"豚丹毒|Erysipelothrix|Q熱|Coxiella|リケッチア|Rickettsia"
        ),
        "bacterial_infection",
    ),
    # Respiratory infections (specific subset of bacterial/viral with respiratory focus)
    (
        re.compile(
            r"スナッフル|kennel cough|ケンネルコフ|気管支敗血症|気管支炎|"
            r"肺炎|pneumonia|ニューモニア|"
            r"上気道感染|URI|気道感染症|鼻気管炎|"
            r"伝染性鼻気管炎"
        ),
        "respiratory_infection",
    ),
    # Fungal infections
    (
        re.compile(
            r"真菌|fungal|mycos|皮膚糸状菌|白癬|Microsporum|Trichophyton|"
            r"アスペルギルス|Aspergillus|カンジダ|Candida|クリプトコッカス|Cryptococcus|"
            r"ブラストミセス|Blastomyces|ヒストプラズマ|Histoplasma|"
            r"コクシジオイデス|Coccidioides|スポロトリックス|Sporothrix|"
            r"マラセチア|Malassezia|ニューモシスチス|Pneumocystis|"
            r"ピシウム|Pythium|サプロレグニア|Saprolegnia"
        ),
        "fungal_infection",
    ),
    # Parasitic
    (
        re.compile(
            r"寄生虫|parasit|フィラリア|heartworm|犬糸状虫|フィラリア症|"
            r"コクシジウム|Coccidi|ジアルジア|Giardia|トリコモナス|Trichomonas|"
            r"ヘキサミタ|Hexamita|スピロヌクレウス|Spironucleus|"
            r"トキソプラズマ|Toxoplasma|エンセファリトゾーン|Encephalitozoon|"
            r"クリプトスポリジウム|Cryptosporidium|住血吸虫|Schistosoma|"
            r"バベシア|Babesia|トリパノソーマ|Trypanosoma|リーシュマニア|Leishmania|"
            r"ダニ|mite|tick|ツメダニ|ヒゼンダニ|アカルス|Demodex|ノミ|flea|"
            r"アタマジラミ|シラミ|louse|ノミ症|ハジラミ|ウマバエ|"
            r"線虫|nematod|条虫|tapeworm|吸虫|fluke|蟯虫|pinworm|回虫|"
            r"ascarid|鞭虫|whipworm|鉤虫|hookworm|肝吸虫|"
            r"白点病|ich|白点虫|イクチオフチリウス|"
            r"イカリ虫|Lernaea|ウオジラミ|Argulus|住血吸虫|"
            r"羽ダニ|気嚢ダニ"
        ),
        "parasitic",
    ),
    # Neoplasia (after viral so FeLV doesn't match lymphoma)
    (
        re.compile(
            r"腫瘍|tumor|tumour|癌|cancer|肉腫|sarcoma|carcinoma|リンパ腫|lymphoma|"
            r"白血病(?!ウイルス)|leukemia|leukaemia|メラノーマ|melanoma|"
            r"肥満細胞腫|mast cell tumor|MCT|血管肉腫|hemangiosarcoma|"
            r"骨肉腫|osteosarcoma|軟部組織肉腫|"
            r"扁平上皮癌|squamous cell|乳腺腫|mammary tumor|"
            r"インスリノーマ|insulinoma|"
            r"褐色細胞腫|pheochromocytoma|腺癌|adenocarcinoma|"
            r"腺腫|adenoma|脂肪腫|lipoma|血管腫|hemangioma|"
            r"巨大食道|megaesophagus|脊索腫|chordoma"
        ),
        "neoplasia",
    ),
    # Endocrine / metabolic
    (
        re.compile(
            r"糖尿病|diabetes|低血糖|hypoglycemia|高血糖|hyperglycemia|"
            r"甲状腺機能亢進|hyperthyroid|甲状腺機能低下|hypothyroid|"
            r"クッシング|Cushing|副腎皮質機能亢進|副腎皮質機能低下|"
            r"アジソン|Addison|hyperadrenocorticism|hypoadrenocorticism|"
            r"副甲状腺|parathyroid|栄養性二次性|代謝性|metabolic|"
            r"インスリン|insulin|糖原病|glycogen storage|脂肪肝|肝リピドーシス|"
            r"hepatic lipidosis|ケトーシス|ketosis|アシドーシス|acidosis|"
            r"アルカローシス|電解質異常|electrolyte"
        ),
        "endocrine_metabolic",
    ),
    # Renal / urinary
    (
        re.compile(
            r"腎臓|腎不全|腎症|腎結石|renal|kidney|nephritis|nephropathy|"
            r"CKD|AKI|尿石|尿路結石|urolith|膀胱炎|cystitis|"
            r"下部尿路|lower urinary|FLUTD|FIC|間質性膀胱炎|"
            r"尿閉|urinary obstruction|蛋白尿|proteinuria|"
            r"糸球体|glomerular|腎盂腎炎|pyelonephritis|"
            r"前立腺|prostate|前立腺炎|prostatitis|"
            r"水腎症|hydronephrosis|腎瘤|ureter"
        ),
        "renal_urinary",
    ),
    # Cardiac
    (
        re.compile(
            r"心臓|心筋|心房|心室|弁膜|心不全|cardiac|cardio|heart|"
            r"DCM|HCM|拡張型心筋症|肥大型心筋症|"
            r"僧帽弁|mitral|三尖弁|tricuspid|心房中隔|心室中隔|"
            r"動脈管開存|PDA|不整脈|arrhythmia|"
            r"心嚢液貯留|pericardial|心タンポナーデ|"
            r"血栓塞栓症|thromboembolism|FATE|サドル血栓"
        ),
        "cardiac",
    ),
    # Respiratory (non-infectious)
    (
        re.compile(
            r"呼吸器|気道|気管|気管支|肺(?!炎)|喘息|asthma|"
            r"短頭種気道症候群|BOAS|気道閉塞|喉頭麻痺|"
            r"laryngeal paralysis|気管虚脱|tracheal collapse|"
            r"肺水腫|pulmonary edema|気胸|pneumothorax|"
            r"胸水|pleural effusion|呼吸窮迫|RAO|recurrent airway obstruction"
        ),
        "respiratory_other",
    ),
    # Gastrointestinal
    (
        re.compile(
            r"胃(?!腸炎)|腸炎(?!ウイルス)|消化器|GI stasis|消化管うっ滞|"
            r"鼓腸|bloat|tympany|腸閉塞|腸捻転|腸重積|intussusception|"
            r"巨大結腸|megacolon|便秘|constipation|下痢(?!性)|"
            r"膵炎|pancreatitis|EPI|膵外分泌不全|"
            r"肝炎(?!ウイルス)|肝硬変|肝障害|liver|hepatic(?!.*lipidosis)|"
            r"胆管|biliary|cholangiohepatitis|胆嚢|gallbladder|"
            r"IBD|inflammatory bowel|炎症性腸疾患|リンパ球性形質細胞性腸炎|"
            r"GDV|胃拡張捻転|疝痛(?!性)|colic|"
            r"幽門狭窄|アクアラジア|食道|esophag"
        ),
        "gastrointestinal",
    ),
    # Neurological
    (
        re.compile(
            r"脳(?!炎)|神経|癲癇|てんかん|epilepsy|seizure|痙攣|convulsion|"
            r"前庭|vestibular|斜頸|head tilt|head torsion|"
            r"認知機能|cognitive|dementia|CDS|"
            r"脊髄|spinal cord|椎間板|IVDD|disc disease|"
            r"麻痺|paralysis|paresis|"
            r"重症筋無力症|myasthenia|"
            r"水頭症|hydrocephalus|髄膜|meningitis|脳炎|encephalitis"
        ),
        "neurological",
    ),
    # Ophthalmic
    (
        re.compile(
            r"眼(?!球突出)|角膜|cornea|緑内障|glaucoma|白内障|cataract|"
            r"網膜|retina|ぶどう膜炎|uveitis|結膜炎|conjunctivitis|"
            r"涙嚢|nasolacrimal|チェリーアイ|cherry eye|乾性角結膜炎|KCS|"
            r"眼科|ophthalmic|ophth|眼疾患"
        ),
        "ophthalmic",
    ),
    # Musculoskeletal
    (
        re.compile(
            r"骨折|fracture|脱臼|luxation|"
            r"靭帯|ligament|十字靭帯|cruciate|腱|tendon|"
            r"関節炎|arthritis|変形性関節症|osteoarthritis|OA|"
            r"股関節|hip dysplasia|肘関節|elbow dysplasia|"
            r"膝蓋骨|patella|patellar|ステーキ|"
            r"骨髄炎|osteomyelitis|筋ジストロフィー|"
            r"代謝性骨疾患|MBD|metabolic bone|"
            r"クル病|くる病|rickets|歯学|"
            r"舟状骨|navicular|蹄|hoof|laminitis|蹄葉炎|蹄壁|"
            r"骨粗鬆症|osteoporosis"
        ),
        "musculoskeletal",
    ),
    # Dental
    (
        re.compile(
            r"歯(?!科)|歯肉|歯周|歯石|歯髄|齲歯|dental|tooth|periodontal|"
            r"歯科疾患|不正咬合|malocclusion|過長歯|"
            r"歯根膿瘍|tooth root abscess|歯瘻"
        ),
        "dental",
    ),
    # Dermatological (non-fungal, non-parasitic)
    (
        re.compile(
            r"皮膚炎|dermatitis|湿疹|eczema|"
            r"アトピー|atopic|アレルギー|allergy|allergic|"
            r"膿皮症|pyoderma|細菌性皮膚感染|"
            r"脱毛|alopecia|hair loss|barbering|"
            r"接触性皮膚炎|contact|"
            r"ホットスポット|hot spot|pyotraumatic|"
            r"自咬|self-mutilation|自傷|"
            r"褥瘡|decubital|pressure sore|"
            r"ポドダーマタイティス|pododermatitis|bumble foot|"
            r"耳疥癬|耳ダニ|otoacariasis(?:.*)|otitis|耳炎"
        ),
        "dermatological",
    ),
    # Hematological
    (
        re.compile(
            r"貧血|anemia|溶血|hemolytic|hemolysis|"
            r"凝固|coagulation|coagulopathy|DIC|播種性血管内凝固|"
            r"血小板減少|thrombocytopenia|血小板|platelet|"
            r"白血球減少|leukopenia|好中球減少|neutropenia|"
            r"再生不良性貧血|aplastic|骨髄異形成|MDS|"
            r"血友病|hemophilia|"
            r"出血(?!熱)|bleeding|hemorrhage"
        ),
        "hematological",
    ),
    # Reproductive
    (
        re.compile(
            r"妊娠|出産|分娩|産後|難産|dystocia|帝王切開|cesarean|"
            r"子宮蓄膿症|pyometra|子宮内膜|endometritis|子宮炎|metritis|"
            r"乳腺炎|mastitis|偽妊娠|pseudopregnancy|"
            r"前立腺|prostate|prostat|"
            r"潜在精巣|cryptorchid|"
            r"陰嚢|scrotal|精巣|testicular|testes|"
            r"胎盤|placental|placenta|"
            r"妊娠中毒|pregnancy toxemia|"
            r"流産|abortion|stillbirth|"
            r"発情|estrus|estrous"
        ),
        "reproductive",
    ),
    # Toxicity
    (
        re.compile(
            r"中毒|toxicity|toxicosis|poisoning|"
            r"鉛中毒|lead poisoning|"
            r"アスピリン中毒|アセトアミノフェン|"
            r"チョコレート中毒|ブドウ中毒|ユリ中毒|"
            r"殺鼠剤|rodenticide|農薬|pesticide|"
            r"有毒植物|plant toxicity|"
            r"重金属|heavy metal|"
            r"化学物質曝露|chemical exposure"
        ),
        "toxicity",
    ),
    # Trauma
    (
        re.compile(
            r"^(?!.*中毒).*外傷|trauma|injury|laceration|裂傷|"
            r"圧迫損傷|crush|"
            r"咬傷|bite wound|"
            r"火傷|burn|熱傷|"
            r"電撃|electrocution|"
            r"溺水|drowning"
        ),
        "trauma",
    ),
    # Autoimmune / immune-mediated
    (
        re.compile(
            r"自己免疫|autoimmune|"
            r"免疫介在|immune-mediated|"
            r"IMHA|IMTP|"
            r"天疱瘡|pemphigus|"
            r"狼瘡|lupus|SLE|"
            r"重症筋無力症|myasthenia"
        ),
        "autoimmune",
    ),
    # Nutritional
    (
        re.compile(
            r"栄養|nutritional|nutrition|"
            r"ビタミン[ABCDEK]|vitamin\s*[ABCDEK]|"
            r"カルシウム|calcium|"
            r"欠乏|deficiency|deficit|"
            r"壊血病|scurvy|"
            r"低カルシウム血症|hypocalcemia|"
            r"くる病|rickets|"
            r"MBD|metabolic bone disease"
        ),
        "nutritional",
    ),
    # Genetic / congenital
    (
        re.compile(
            r"遺伝性|genetic|hereditary|congenital|先天性|"
            r"染色体|chromosomal"
        ),
        "genetic_congenital",
    ),
    # Degenerative
    (
        re.compile(
            r"変性|degenerative|degeneration|"
            r"加齢性|age-related|geriatric|老齢性"
        ),
        "degenerative",
    ),
    # Behavioral
    (
        re.compile(
            r"行動学|behavioral|behavior|anxiety|不安症|"
            r"強迫|compulsive|分離不安|separation|"
            r"恐怖|phobia|aggression|攻撃行動"
        ),
        "behavioral",
    ),
]


def resolve_true_category(name_ja: str, name_en: str, tagged_category: str) -> str:
    """Resolve the canonical category from disease name (priority) + tagged category (fallback).

    Returns one of: viral_infection, bacterial_infection, respiratory_infection,
    fungal_infection, parasitic, neoplasia, endocrine_metabolic, renal_urinary,
    cardiac, respiratory_other, gastrointestinal, neurological, ophthalmic,
    musculoskeletal, dental, dermatological, hematological, reproductive,
    toxicity, trauma, autoimmune, nutritional, genetic_congenital, degenerative,
    behavioral, generic.
    """
    name = f"{name_ja or ''} {name_en or ''}"
    for pattern, cat in NAME_CATEGORY_PATTERNS:
        if pattern.search(name):
            return cat

    # Fall back to tagged category
    tagged_norm = (tagged_category or "").lower().strip()
    tagged_map = {
        "infectious": "bacterial_infection",
        "infection": "bacterial_infection",
        "oncology": "neoplasia",
        "tumor": "neoplasia",
        "nutritional": "nutritional",
        "trauma": "trauma",
        "parasite": "parasitic",
        "toxic": "toxicity",
        "congenital": "genetic_congenital",
        "fungal": "fungal_infection",
        "musculoskeletal": "musculoskeletal",
        "metabolic": "endocrine_metabolic",
        "cardiac": "cardiac",
        "cardiovascular": "cardiac",
        "immune": "autoimmune",
        "autoimmune": "autoimmune",
        "gi": "gastrointestinal",
        "digestive": "gastrointestinal",
        "urinary": "renal_urinary",
        "renal": "renal_urinary",
        "respiratory": "respiratory_other",
        "skin": "dermatological",
        "neurological": "neurological",
        "neuro": "neurological",
        "eye": "ophthalmic",
        "degenerative": "degenerative",
        "reproductive": "reproductive",
        "dental": "dental",
        "behavioral": "behavioral",
    }
    return tagged_map.get(tagged_norm, "generic")


# ---------------------------------------------------------------------------
# Species-specific context fragments
# ---------------------------------------------------------------------------

SPECIES_JA = {
    "dog": "犬",
    "cat": "猫",
    "horse": "馬",
    "rabbit": "ウサギ",
    "hamster": "ハムスター",
    "guinea_pig": "モルモット",
    "chinchilla": "チンチラ",
    "ferret": "フェレット",
    "hedgehog": "ハリネズミ",
    "sugar_glider": "フクロモモンガ",
    "degu": "デグー",
    "bird": "鳥",
    "parakeet": "インコ",
    "parrot": "オウム",
    "reptile": "爬虫類",
    "tortoise": "リクガメ",
    "snake": "ヘビ",
    "lizard": "トカゲ",
    "amphibian": "両生類",
    "fish": "魚",
    "exotic_other": "その他エキゾチック動物",
}

SPECIES_SUPPORTIVE_NOTES_JA = {
    "rabbit": "（ウサギは経口β-ラクタム抗菌薬禁忌、GI stasis予防が必須）",
    "guinea_pig": "（モルモットは経口ペニシリン系禁忌、Clostridium腸炎を誘発）",
    "chinchilla": "（チンチラはフィプロニル致死、経口β-ラクタム禁忌）",
    "hamster": "（ハムスターは低体温に脆弱、輸液は体温で温める）",
    "ferret": "（フェレットは低血糖に陥りやすい、絶食3時間以内）",
    "bird": "（鳥類は気嚢システムを持ち、ストレスで急変する）",
    "parakeet": "（インコは気嚢システムを持ち、ストレスで急変する）",
    "parrot": "（オウムは気嚢システムを持ち、ストレスで急変する）",
    "reptile": "（爬虫類は種別POTZ維持が免疫機能回復の前提）",
    "tortoise": "（リクガメは種別POTZ維持が免疫機能回復の前提）",
    "snake": "（ヘビは脱皮周期に注意、種別POTZ維持）",
    "lizard": "（トカゲは種別POTZ維持、UV-B不足に注意）",
    "amphibian": "（両生類は皮膚呼吸のため浸漬投薬を基本とし、塩素水接触を避ける）",
    "fish": "（魚は薬浴・浸漬投薬が基本、エラ・粘膜への直接作用）",
    "horse": "（馬は疝痛・蹄葉炎のリスクに常時注意、長時間横臥を避ける）",
}


def _species_note(species: str) -> str:
    return SPECIES_SUPPORTIVE_NOTES_JA.get(species, "")


# ---------------------------------------------------------------------------
# Curated content for top-priority diseases
# ---------------------------------------------------------------------------
# Format: { (species, name_pattern_ja_or_en): { field: text } }

CURATED: dict[tuple[str, str], dict[str, str]] = {
    ("cat", "FeLV"): {
        "causes_ja": (
            "猫白血病ウイルス感染症（FeLV）の原因は γ-レトロウイルス科 Feline Leukemia Virus 感染である。"
            "感染猫の唾液・鼻汁・尿・糞便を介した水平感染（毛繕い・咬傷・食器共有・母子伝播）が主経路。"
            "ウイルスは骨髄幹細胞のDNAに組み込まれ持続感染を成立させる。"
            "感染リスクが高いのは若齢猫（1歳未満）、屋外アクセス猫、複数頭飼育環境、免疫抑制状態。"
            "宿主免疫応答により progressive infection（持続的ウイルス血症）・regressive infection（潜伏感染）・abortive infection（消失）の3転帰をたどる。"
        ),
        "transmission_ja": (
            "感染猫からの唾液・鼻汁を介した水平感染が主経路（咬傷・毛繕い・食器共有）。"
            "経胎盤・経乳の垂直感染も成立する。環境中のウイルスは室温で数時間以内に不活化される。"
            "感染猫との同居期間が長いほど感染リスク上昇するが、適切な隔離で予防可能。"
            "ヒトには感染しないが、人獣共通感染症と誤解されることがある。"
        ),
        "clinical_signs_ja": (
            "FeLVの臨床徴候は免疫抑制・骨髄抑制・腫瘍性疾患の3系統に分類される。"
            "免疫抑制では再発性発熱・口内炎・歯肉炎・慢性鼻炎・皮膚感染・敗血症を呈する。"
            "骨髄抑制では非再生性貧血（最多）・好中球減少症・血小板減少症が認められる。"
            "腫瘍性病変では胸腺型・縦隔型・多中心性リンパ腫が特徴的で、若齢猫の前縦隔腫瘤と胸水は典型的徴候。"
            "末期では削痩・元気消失・食欲不振が進行する。"
        ),
        "differential_diagnosis_ja": (
            "鑑別診断: FIV感染（免疫抑制症状の重複、FeLV/FIV併発も多い）、"
            "FIP（湿性型は胸水・腹水で類似）、慢性腎臓病（CKD: 削痩・脱水・貧血）、"
            "歯肉口内炎（カリシウイルス・ヘルペスウイルス）、非感染性骨髄異形成、"
            "胸腺リンパ腫以外の縦隔腫瘤（胸腺腫・転移性腫瘍）。"
            "SNAP抗原検査陽性は p27 抗原の存在を示すが、IFA確認検査で持続感染を区別する。"
        ),
        "prevention_ja": (
            "予防の中核は FeLV ワクチン接種と感染猫との接触回避。"
            "ワクチン接種前に SNAP 抗原検査で感染状態を確認することが必須（陽性猫への接種は効果なし）。"
            "屋外アクセス猫・新規導入猫には初年度2回接種＋年1回追加（リスク評価次第）。"
            "感染猫は完全屋内飼育とし、未感染猫との完全隔離（別室・別食器・別トイレ）を徹底する。"
            "新規導入猫は最低4週間隔離し、抗原検査陰性確認後に合流させる。"
        ),
        "prognosis_ja": (
            "FeLV感染の予後は感染転帰により大きく異なる。"
            "持続性ウイルス血症（progressive infection）: 中央生存期間 2.4-3 年、5年生存率は約 20%。"
            "退行性感染（regressive infection）: 寿命に近い予後だが、免疫抑制下で再活性化リスクあり。"
            "リンパ腫合併例の CHOP/COP プロトコル奏功率は 50-70%、完全寛解達成例の中央生存期間 4-9 ヶ月。"
            "若齢発症・重度貧血合併・敗血症合併は予後不良因子。"
        ),
        "prognosis_detailed_ja": (
            "FeLVの予後を層別化する因子: ① ウイルス血症の持続性（progressive >24週 = 予後不良）、"
            "② CD4+ T細胞数の減少程度（200/μL未満で重度免疫不全）、"
            "③ 二次感染の有無（敗血症・FIP併発で生存期間短縮）、"
            "④ 腫瘍性合併症（リンパ腫・骨髄異形成は化学療法応答性で予後が分かれる）、"
            "⑤ 居住環境（屋内単独飼育で感染圧低下、QOL維持に有利）。"
            "Hartmann (2019) のコホート研究では適切な感染管理下で中央生存期間が 3.4 年まで延長可能と報告。"
        ),
        "nutrition_management_ja": (
            "FeLV感染猫の栄養管理では免疫機能維持と異化亢進への対応が重点となる。"
            "高品質動物性タンパク質（消化性 ≥85%）の十分な供給により抗体産生と組織修復を支援。"
            "適切なエネルギー密度（80-100 kcal/kg/日 を病態に応じて）を維持。"
            "オメガ3脂肪酸（EPA/DHA 30-40 mg/kg/日）の抗炎症作用を活用。"
            "L-リジン（250-500 mg PO q12h）はヘルペスウイルス再活性化抑制に有用。"
            "生肉食・未殺菌乳製品は二次感染リスクのため禁忌。"
        ),
        "rehabilitation_protocol_ja": (
            "FeLVの慢性管理ではQOL維持を中心としたリハビリテーションが重要。"
            "屋内飼育で感染圧低下と保温維持。低ストレス環境の構築（爪研ぎ・隠れ場所・上下運動の確保）。"
            "急性増悪期は入院支持療法（輸液・抗菌薬・輸血）で安定化後、自宅療養に移行。"
            "リンパ腫化学療法中は CBC モニタリング（週1回）と感染予防（抗菌薬予防投与の検討）。"
            "末期には緩和ケア（食欲増進・脱水補正・疼痛管理）を中心とした看取り計画を立案する。"
        ),
    },
    ("cat", "FIV"): {
        "causes_ja": (
            "猫免疫不全ウイルス感染症（FIV）の原因はレンチウイルス科 Feline Immunodeficiency Virus 感染。"
            "感染猫の咬傷（唾液中ウイルス）による水平感染が主経路で、屋外飼育の去勢前雄猫に最多発。"
            "経胎盤・経乳の垂直感染は稀。同居生活のみでは感染確率は低い（咬傷介在が必要）。"
            "感染後ウイルスは CD4+ T リンパ球に持続感染し、急性期→無症候期（数年）→AIDS類似期と進行する。"
        ),
        "transmission_ja": (
            "感染猫の咬傷を介した唾液-血液感染が主経路。"
            "去勢前雄の縄張り争いによる咬傷で感染確率が高く、雌猫・避妊済個体での感染は稀。"
            "母子感染（経胎盤・経乳）は成立するが、進行性感染に至るのは一部のみ。"
            "ヒトには感染しない（FIVはネコ科特異的）。"
            "環境中のウイルスは数分で不活化され、共有食器・トイレ経由の感染は実質的に成立しない。"
        ),
        "clinical_signs_ja": (
            "FIVの臨床徴候は感染病期により異なる。"
            "急性期（感染後4-12週）: 一過性発熱・リンパ節腫大・神経症状（軽度）が認められるが見逃されやすい。"
            "無症候期（数ヶ月〜10年）: 臨床的に正常、健康診断で偶発的に診断される。"
            "AIDS類似期: 慢性歯肉口内炎（最多、約50%）、慢性鼻炎・上気道感染、再発性下痢、削痩、貧血、二次感染の慢性化、リンパ腫リスク上昇。"
        ),
        "prevention_ja": (
            "予防の中核は咬傷リスクの低減: 完全屋内飼育、早期去勢手術（雄）、複頭飼育下での攻撃行動管理。"
            "ワクチン（FIV vaccine）はかつて存在したが現在は北米で使用中止（抗体検査干渉のため）。"
            "新規導入猫は最低60日間隔離し、抗体検査（ELISA → Western blot 確認）で陰性確認後に合流。"
            "FIV陽性猫は他猫との接触を避けるため完全屋内単独または陽性猫のみとの共同生活を推奨。"
        ),
        "prognosis_ja": (
            "FIVの予後は感染病期と並行管理により大きく異なる。"
            "適切な感染管理下の無症候期猫: 平均寿命に近い（10-15年以上の生存例多数）。"
            "AIDS類似期に進行した症例: 二次感染の重症度と治療反応性で予後が決まる。"
            "Levy (2008) によるFIV陽性猫コホート: 中央生存期間 5 年以上、非感染猫との生存差は限定的。"
            "リンパ腫合併は予後不良（中央生存 4-6 ヶ月）。"
        ),
    },
    ("cat", "甲状腺機能亢進"): {
        "causes_ja": (
            "猫の甲状腺機能亢進症の原因の98%以上は良性の甲状腺機能性腺腫（過形成性結節）。"
            "残り 1-3% が甲状腺癌（悪性）で予後を悪化させる。"
            "発症平均年齢 13歳、10歳以上の猫の 10% 以上が罹患し、最頻発の内分泌疾患。"
            "病因は完全には解明されていないが、缶詰食（特にプルタブ缶のBPA曝露）、ハロゲン化難燃剤（PBDE）、シャム猫以外の品種、屋内飼育、フリー給餌、ヨウ素過剰摂取などが疫学的リスク因子として報告されている。"
        ),
        "transmission_ja": (
            "甲状腺機能亢進症は感染性疾患ではないため猫間の伝播は生じない。"
            "ただし環境因子（缶詰食曝露・PBDE曝露）を共有する複数頭飼育環境で多頭発症することがある。"
            "ヒトには伝播しない。"
        ),
        "prevention_ja": (
            "確立された予防法はないが、リスク低減として乾燥フードへの切替（缶詰中のBPA回避）、"
            "ヨウ素過剰なフードの回避、定期的な血液検査による早期発見が推奨される。"
            "10歳以上の猫では年1回のT4スクリーニング、心雑音・体重減少のある中高齢猫では早期に評価。"
            "禁忌のヨウ素制限食（Hill's y/d）は他の管理オプションが使用できない症例の選択肢として位置付けられる。"
        ),
        "prognosis_ja": (
            "適切な管理下では予後良好。I-131 治療: 治癒率 95% 以上、中央生存期間 4 年以上。"
            "メチマゾール内服管理: 5年生存率約 70%（甲状腺癌でなければ）、副作用（食欲不振・嘔吐・皮膚掻痒・血液障害）で 10-15% が薬剤変更を要する。"
            "甲状腺摘出: 治癒可能だが術後低カルシウム血症のリスク。"
            "未治療例は心不全・腎不全・削痩で 1-2 年以内に死亡。"
            "治療後の腎機能不全顕在化が約 15-25% で起こり、CKD並行管理が予後を左右する。"
        ),
    },
    ("cat", "CKD"): {
        "causes_ja": (
            "猫の慢性腎臓病（CKD）の原因は多くの場合特定困難で、加齢に伴うネフロン進行性喪失が主機序。"
            "明らかな原因として、慢性間質性腎炎、糸球体腎症、腎尿細管性アミロイドーシス、多発性嚢胞腎（PKD：ペルシャ系遺伝性）、虚血性腎障害（FATE後遺症）、腎盂腎炎（細菌性）、腎リンパ腫、毒性物質（ユリ・抗凍液・NSAID過量）の慢性的影響が挙げられる。"
            "10歳以上の猫の 30%、15歳以上の猫の 50% 以上が罹患する。"
        ),
        "transmission_ja": (
            "CKDは非感染性疾患のため猫間の伝播は生じない。"
            "原因が感染性腎盂腎炎（細菌・レプトスピラ）の場合のみ間接的に伝播の可能性があるが、CKDそのものは個別罹患。"
            "ペルシャ系のPKDは常染色体優性遺伝で繁殖管理により予防可能。"
        ),
        "prevention_ja": (
            "現時点で確立された予防法は限定的だが、定期的な腎機能スクリーニング（7歳以上は年1回、10歳以上は半年に1回）が早期発見の鍵。"
            "SDMA測定で従来のクレアチニン異常より早期に検出可能。"
            "ペルシャ系の繁殖前PKD遺伝子検査、毒性物質（ユリ・抗凍液・NSAID）の管理徹底、適切な水分摂取の維持（ウェットフード推奨）、歯科ケアの徹底（細菌の血行性腎播種予防）が予防に寄与する。"
        ),
        "prognosis_ja": (
            "予後は IRIS ステージにより大きく異なる。"
            "IRIS ステージ2（クレアチニン 1.6-2.8 mg/dL）: 中央生存期間 3 年以上。"
            "ステージ3（2.9-5.0）: 中央生存期間 1.5-2 年。"
            "ステージ4（>5.0）: 中央生存期間 数週〜数ヶ月。"
            "予後悪化因子: 蛋白尿（UPC>0.4）、高リン血症、貧血、高血圧。"
            "適切な栄養管理（腎臓食）・降圧療法・低リン療法・赤血球造血刺激療法・水分補給により生存期間延長可能。"
        ),
    },
    ("cat", "FLUTD"): {
        "causes_ja": (
            "猫下部尿路疾患（FLUTD）の原因は多因子性で複数病態が含まれる。"
            "最多は猫特発性膀胱炎（FIC：60-70%、ストレス関連神経内分泌障害）、"
            "次いで尿石症（ストルバイト・シュウ酸カルシウム結石：15-25%）、"
            "尿道閉塞（雄猫に多い、結石・尿道栓子・痙攣）、"
            "尿路感染（10歳以上の高齢猫で頻度上昇、若齢猫では稀）、"
            "尿道腫瘍・解剖学的異常（稀）。"
            "FIC のリスク因子: 多頭飼育、屋内飼育、乾燥フード単独給餌、運動不足、過体重、不衛生なトイレ。"
        ),
        "transmission_ja": (
            "FLUTDは非感染性のため猫間の直接伝播は生じない。"
            "細菌性尿路感染が原因の場合のみ感染源との接触で発症する可能性があるが、これは FLUTD 全体の少数派。"
            "多頭飼育環境ではストレス関連の FIC が複数頭で同時発症することがあるが、これは共通環境ストレスによるもので感染ではない。"
        ),
        "prevention_ja": (
            "予防の中核はストレス管理と水分摂取量増加。"
            "1日複数のトイレ提供（頭数+1個）、清潔な砂の維持、隠れ場所と上下運動の確保、フード切替時の段階的移行。"
            "ウェットフード比率を高める（70%以上）、循環式給水器の活用、ストルバイト・シュウ酸カルシウム両対応の食事療法（Hill's c/d Multicare、Royal Canin Urinary SO 等）の利用。"
            "FIC既往例にはフェロモン療法（Feliway）、抗不安薬（重症例にアミトリプチリン・フルオキセチン）を考慮。"
            "尿閉雄猫では尿道造瘻術（PU術）も予防的選択肢。"
        ),
        "prognosis_ja": (
            "FLUTDの予後は原因病態により大きく異なる。"
            "FIC：自然寛解率約 50%（5-7日）、再発率 50-60%、適切な環境管理で再発率を低下可能。"
            "尿石症：食事療法でストルバイト溶解率 80% 以上（4-6週）、シュウ酸カルシウムは溶解不能で外科適応。"
            "尿閉雄猫：閉塞解除後の再閉塞率 15-35%、再発例は PU 術（成功率 90% 以上）。"
            "尿路感染：適切な抗菌薬で治癒率高いが、CKD・糖尿病併発で再発リスク上昇。"
        ),
    },
    ("cat", "糖尿病"): {
        "causes_ja": (
            "猫の糖尿病はインスリン分泌不全と末梢インスリン抵抗性の併存により発症する。"
            "ヒト2型糖尿病に類似し、80-90% が肥満関連の2型相当。"
            "病因因子: 肥満（BCS≥6）、加齢（中央発症 10歳）、雄猫（雌の 1.5倍）、屋内飼育、運動不足、高炭水化物食、ストレス、ステロイド・酢酸メゲストロール投与歴、慢性膵炎・末端肥大症・クッシング症候群（インスリン抵抗性誘発）。"
            "膵島アミロイドーシスによる β 細胞減少が病理学的特徴。"
        ),
        "transmission_ja": (
            "糖尿病は非感染性のため猫間の伝播は生じない。"
            "ただし同一環境（高炭水化物食・運動不足・肥満）を共有する複数頭飼育で同時罹患することがある。"
        ),
        "prevention_ja": (
            "予防の中核は適正体重維持と低炭水化物食。"
            "BCS 5/9 を目標にカロリー管理、毎日の遊び運動（10-15分×2回）、低炭水化物・高タンパク質食（炭水化物 <12% メタボリックエネルギー、タンパク質 ≥40%）。"
            "酢酸メゲストロール（ペット用避妊薬）と長期ステロイド療法は糖尿病リスクのため避ける。"
            "中高齢肥満猫では年1回のスクリーニング（血糖・フルクトサミン・尿糖）。"
        ),
        "prognosis_ja": (
            "猫の糖尿病は適切な治療で 20-40% が寛解（インスリン離脱）達成可能。"
            "寛解因子: 早期診断、グラルギンまたはPZIインスリン使用、低炭水化物食、肥満解消、ストレス管理、CGM活用。"
            "未寛解例も適切な管理で中央生存期間 3 年以上。"
            "予後悪化因子: 糖尿病性ケトアシドーシス（DKA）合併（救急対応で生存率 70-80%）、慢性膵炎・末端肥大症併発、感染症合併。"
            "Bexagliflozin（SGLT2阻害薬）が2023年AAHAガイドラインで適応症例に推奨されている。"
        ),
    },
    ("cat", "FIP"): {
        "causes_ja": (
            "猫伝染性腹膜炎（FIP）は猫腸コロナウイルス（FECV）の体内変異により発症する。"
            "FECV は若齢猫の腸管に広く感染し通常は無症候だが、ごく一部の個体で変異株（FIPV）が腹腔内マクロファージに感染し、免疫複合体性血管炎を引き起こす。"
            "リスク因子: 若齢（生後 3 ヶ月-2 歳が好発、平均 8-12 ヶ月）、ストレス（断乳・引っ越し・多頭飼育）、純血種（ペルシャ・バーマン・ベンガル等）、免疫不全（FeLV・FIV併発）、近親交配。"
            "FIP は致死的だが、近年 GS-441524 / モルヌピラビル等の抗ウイルス薬で 80% 以上の治癒率が報告されている（Pedersen 2019, Krentz 2021）。"
        ),
        "transmission_ja": (
            "FECV（前駆ウイルス）は感染猫の糞便を介して経口感染（共有トイレ・毛繕い）。"
            "ただし体内変異後のFIPV自体は猫間で伝播しない（変異は個体内で偶発的に発生）。"
            "そのためFIP発症猫からの直接伝播リスクは低いが、FECVキャリアからの感染リスクが残る。"
            "多頭飼育環境では FECV 持続感染が成立しやすく、ストレス増大で FIP 発症率上昇。"
        ),
        "prognosis_ja": (
            "従来は致死率 95% 以上の予後不良疾患だったが、抗ウイルス薬（GS-441524, EIDD-2801/モルヌピラビル）で大きく改善。"
            "GS-441524 84日投与プロトコル: 治癒率 80-95%（Pedersen 2019, Dickinson 2020）。"
            "ドライ型・神経/眼型は治療反応がやや遅いが治癒可能。"
            "予後不良因子: 神経症状・眼症状の重度進行、重度の貧血、肝機能著明低下、診断遅延。"
            "治癒後の再発率は約 5-10%（投与終了後 1 年以内）。"
        ),
    },
    ("dog", "ジステンパー"): {
        "causes_ja": (
            "犬ジステンパー（Canine Distemper Virus, CDV）はパラミクソウイルス科モルビリウイルス属。"
            "感染犬の呼吸器・尿・糞便からの飛沫感染（咳・くしゃみ）で水平伝播。"
            "リスク因子: ワクチン未接種・移行抗体減弱期の子犬（6-12週齢）、避難所・ペットショップ・繁殖場の集団飼育環境、免疫抑制状態。"
            "感染後、ウイルスはリンパ系→骨髄→中枢神経・呼吸器・消化器・皮膚に系統的に伝播する。"
            "野生動物（アライグマ・タヌキ・キツネ・フェレット）も保有宿主となる。"
        ),
        "transmission_ja": (
            "感染犬の呼吸器分泌物・尿・糞便からの飛沫感染が主経路。"
            "ウイルスは環境中で不安定（紫外線・乾燥・消毒薬に弱い）だが寒冷湿潤環境では数時間生存。"
            "経胎盤感染も成立し、新生子犬に致死的影響。"
            "ヒトには感染しないが、フェレット・タヌキ・アライグマには高致死率で感染するため、野生動物との接触に注意。"
        ),
        "prognosis_ja": (
            "予後はワクチン接種歴・年齢・神経症状の有無で大きく異なる。"
            "未接種子犬での全身性感染: 致死率 50-80%、生存例も神経学的後遺症が高頻度（hard pad disease、ミオクローヌス、慢性発作）。"
            "成犬の不顕性〜軽症例: 良好予後。"
            "神経型（亜急性〜慢性）: 進行性で予後不良、安楽死選択も考慮。"
            "適切なワクチネーション（DHPP/DHLPP コアワクチン、子犬は 6-8 / 10-12 / 14-16週齢、追加 1 年後・以後 3 年毎）で予防効果はほぼ完全。"
        ),
    },
    ("dog", "パルボ"): {
        "causes_ja": (
            "犬パルボウイルス（Canine Parvovirus, CPV-2）感染症の原因は CPV-2 とその変異株（CPV-2a/2b/2c）。"
            "急速増殖細胞（腸陰窩細胞・骨髄・心筋）を標的にする一本鎖DNAウイルス。"
            "リスク因子: ワクチン未接種・移行抗体減弱期の子犬（6-20週齢で最多）、ロットワイラー・ドーベルマン・アメリカンピットブル等の素因犬種、ストレス（断乳・移動・寄生虫・他感染症併発）、過密飼育（避難所・ペットショップ）。"
            "環境中で長期間（>6ヶ月）安定で再汚染リスクが高い。"
        ),
        "transmission_ja": (
            "感染犬の糞便を介した経口感染が主経路。"
            "ウイルスは環境中で極めて安定で、汚染環境・器具・衣服・手指を介した間接感染が成立。"
            "1g の糞便中に 10^9 個以上のウイルス粒子が含まれる。"
            "消毒には次亜塩素酸（1:30 漂白剤）・過酢酸が有効、アルコール・第四級アンモニウムは無効。"
            "経胎盤感染は稀（成獣感染時のみ）。"
            "ヒトには感染しない。"
        ),
        "prognosis_ja": (
            "予後は早期発見・早期治療で大きく改善。"
            "適切な入院支持療法を受けた症例の生存率 80-95%（Hartmann 2019）。"
            "自宅治療または無治療例の致死率 50-80%。"
            "心筋型（生後3週未満感染）: 高致死率、生存例も心筋線維症の後遺症。"
            "予後不良因子: 重度白血球減少（<1,000/μL）、低血糖、敗血症併発、腸壁穿孔。"
            "適切なワクチネーション（DHPP コアワクチン）で予防効果 ~95%。"
        ),
    },
}


# ---------------------------------------------------------------------------
# Category-aware template generators (with disease-name embedding)
# ---------------------------------------------------------------------------


def _disease_prefix(name_ja: str, species_ja: str) -> str:
    """Build a disease-specific lead phrase.

    Avoid double-prefixing when the disease name already starts with the
    species name (e.g. "猫下部尿路疾患" + species "猫" -> avoid "猫における猫下部尿路疾患").
    """
    if name_ja:
        if species_ja and name_ja.startswith(species_ja):
            return name_ja
        return f"{species_ja}における{name_ja}"
    return f"{species_ja}における本疾患"


def gen_causes_ja(category: str, name_ja: str, species: str) -> str:
    sp_ja = SPECIES_JA.get(species, species)
    prefix = _disease_prefix(name_ja, sp_ja)
    note = _species_note(species)

    if category == "viral_infection":
        return (
            f"{prefix}の原因はウイルス感染である。"
            f"特異的ウイルス病原体が宿主細胞に侵入し、細胞内で複製することで組織傷害と全身炎症反応を引き起こす。"
            f"主な感染リスク因子はワクチン未接種、免疫抑制状態、若齢・高齢、集団飼育環境、新規導入個体との接触、媒介動物（節足動物・野生動物）への曝露である。"
            f"病原体の毒力と宿主免疫応答のバランスが発症と重症度を規定する。{note}"
        )
    if category == "bacterial_infection":
        return (
            f"{prefix}の原因は特定の細菌病原体の感染である。"
            f"病原性細菌が体内に侵入（経口・経皮・経気道・媒介動物）し、増殖・毒素産生・組織浸潤により疾患を引き起こす。"
            f"宿主免疫抑制（ストレス・栄養不良・併発疾患）、抗菌薬の不適切使用による菌叢異常、汚染環境への持続的曝露、咬傷・外傷からの侵入が主要リスク。"
            f"近年の薬剤耐性菌（MRSP・ESBL産生菌）の出現が治療上の課題となっている。{note}"
        )
    if category == "respiratory_infection":
        return (
            f"{prefix}の原因は気道病原体（細菌・ウイルス・真菌）の上気道または下気道への感染である。"
            f"環境ストレス（温度急変・湿度変動・換気不良）、過密飼育、集団輸送、煙草の煙・粉塵への曝露が発症リスクを増大させる。"
            f"短頭種・気道解剖学的異常を有する個体、若齢・高齢、免疫抑制状態は重症化しやすい。"
            f"複数病原体の併発感染（例: ボルデテラ＋パラインフルエンザウイルス）が病態を悪化させることが多い。{note}"
        )
    if category == "fungal_infection":
        return (
            f"{prefix}の原因は真菌病原体への感染である。"
            f"皮膚糸状菌（Microsporum/Trichophyton）、酵母様真菌（Malassezia/Candida）、深在性真菌（Aspergillus/Cryptococcus/Histoplasma 等）が含まれる。"
            f"湿潤環境、免疫抑制状態、長期抗菌薬投与による菌叢撹乱、外傷・皮膚バリア破綻、地理的流行地（コクシジオイデス症など）への居住歴がリスクとなる。"
            f"人獣共通感染症（特に皮膚糸状菌症）として公衆衛生上も重要である。{note}"
        )
    if category == "parasitic":
        return (
            f"{prefix}の原因は寄生虫（蠕虫・原虫・節足動物）の感染である。"
            f"感染経路は寄生虫種により多様で、経口摂取（汚染食物・水・中間宿主の捕食）、経皮侵入、節足動物媒介（ダニ・蚊・ノミ）、経胎盤・経乳感染を含む。"
            f"過密飼育、衛生管理不良、免疫抑制、定期的駆虫の不足が感染リスクを高める。"
            f"寄生虫のライフサイクル理解が治療成功と再感染予防の鍵となる。"
            f"気候変動に伴う媒介動物分布拡大により、従来は低リスクとされた地域での発症増加が報告されている。{note}"
        )
    if category == "neoplasia":
        return (
            f"{prefix}の発生には複数要因が複合的に関与する。"
            f"遺伝的素因（品種特異的好発性）、慢性炎症の持続、発癌性ウイルス感染（FeLV関連リンパ腫等の特異的例を除く）、化学発癌物質への長期曝露、ホルモン異常（性ホルモン依存性腫瘍）、免疫監視機構の破綻、紫外線・電離放射線曝露が主要因子。"
            f"加齢に伴うDNA修復能低下と細胞増殖制御異常が促進因子となる。"
            f"早期発見と病期診断（TNM分類）が予後改善と治療選択の基盤である。{note}"
        )
    if category == "endocrine_metabolic":
        return (
            f"{prefix}の原因は内分泌腺の機能異常または代謝経路の障害である。"
            f"具体的には自己免疫性内分泌腺破壊、腫瘍性ホルモン産生（機能性腺腫・癌）、医原性（長期ステロイド・薬剤）、栄養性（食事性ミネラル・ビタミン異常）、遺伝性酵素欠損が含まれる。"
            f"年齢、肥満、品種特異的素因、併発疾患（膵炎・腎不全による二次性内分泌異常）が発症リスクを修飾する。"
            f"早期診断のための内分泌スクリーニング検査の活用が重要。{note}"
        )
    if category == "renal_urinary":
        return (
            f"{prefix}の原因はネフロンの進行性損傷、尿路の閉塞・感染、または特発性の下部尿路炎症反応である。"
            f"加齢、慢性脱水、腎毒性物質曝露（NSAID・抗凍液・ユリ・特定の抗菌薬）、全身性高血圧、糖尿病性腎症、免疫複合体性糸球体腎炎、遺伝性腎構造異常、ストレス関連の神経内分泌障害が主要リスク因子。"
            f"早期は無症候性に進行するため、定期的な腎機能スクリーニング（SDMA・尿比重・尿蛋白）が重要となる。{note}"
        )
    if category == "cardiac":
        return (
            f"{prefix}の原因には品種特異的遺伝素因が大きく関与する。"
            f"心筋症（DCM/HCM）の素因犬種・猫品種、変性性弁膜疾患（小型犬の僧帽弁粘液腫様変性）、先天性心奇形（PDA・VSD・ASD）、不整脈源性心筋症が主要病因。"
            f"二次性要因として高血圧、甲状腺機能亢進症（猫）、栄養性（タウリン・カルニチン・グレインフリー食関連DCM）、薬剤性、感染性心内膜炎が含まれる。"
            f"早期診断（雑音検出後の心エコー）と段階的治療が予後改善に直結する。{note}"
        )
    if category == "respiratory_other":
        return (
            f"{prefix}は非感染性気道疾患を含み、原因は多岐にわたる。"
            f"アレルギー性（猫喘息・好酸球性気管支炎）、解剖学的異常（短頭種気道症候群BOAS・気管虚脱・喉頭麻痺）、腫瘍性、栄養性（肥満による拘束性換気障害）、慢性炎症性（COPD様病態）、誤嚥性が含まれる。"
            f"環境因子としてタバコの煙、家庭用化学物質、香料、過剰な粉塵への曝露が重要なリスク。"
            f"気道のリモデリングと不可逆的構造変化を防ぐため早期介入が望ましい。{note}"
        )
    if category == "gastrointestinal":
        return (
            f"{prefix}の原因は感染性、食事性、免疫介在性、機械的、機能的要因に分類される。"
            f"感染性（細菌・ウイルス・寄生虫・原虫）、食事性（不適切な食材・異物・急激な食事変更・食物アレルギー）、免疫介在性（炎症性腸疾患IBD）、機械的（腸閉塞・腸捻転・腫瘍）、機能的（運動機能障害）が含まれる。"
            f"草食動物では繊維質不足と急激な食餌変更が消化管うっ滞の主原因となり、種特異的な栄養要求の理解が重要。"
            f"ストレス因子（環境変化・新規動物導入）も発症に寄与する。{note}"
        )
    if category == "neurological":
        return (
            f"{prefix}の原因は多岐にわたり、感染性（脳炎・髄膜炎）、免疫介在性、変性性、腫瘍性、外傷性、血管性、代謝性、毒性、遺伝性、特発性（特発性てんかん）に分類される。"
            f"品種特異的好発性（コリーのCDS、ボーダーコリーのストーム不安、特発性てんかんの素因犬種）も重要な背景因子。"
            f"急性発症は外傷・血管障害・中毒を、慢性進行性は変性・腫瘍・代謝性を、再発性発作は特発性てんかんを示唆する。{note}"
        )
    if category == "ophthalmic":
        breed_note = ""
        if species in ("dog", "cat"):
            breed_note = "品種特異的素因（短頭種の眼球突出・乾性角結膜炎、コッカースパニエルの白内障、コリーアイ症候群、進行性網膜萎縮の素因犬種）が重要。"
        elif species == "horse":
            breed_note = "馬では月盲（再帰性ぶどう膜炎ERU）が遺伝性素因（Appaloosa等）と関連する。角膜潰瘍はサラブレッドの飼育環境（堆肥・敷材）が誘因となる。"
        elif species in ("bird", "parakeet", "parrot"):
            breed_note = (
                "鳥類では栄養性（ビタミンA欠乏）・感染性（ヘルペスウイルス・クラミジア・ポックス）・外傷性が主要原因。"
            )
        elif species in ("reptile", "tortoise", "snake", "lizard"):
            breed_note = "爬虫類では栄養性（ビタミンA欠乏・MBD）・脱皮不全による眼瞼閉塞・低POTZが主要要因。"
        return (
            f"{prefix}の原因は感染性（細菌・ウイルス・真菌・寄生虫）、外傷性、免疫介在性、先天性、変性性、腫瘍性、代謝性、医原性が含まれる。"
            f"{breed_note}"
            f"治療遅延は不可逆的視力喪失につながるため早期診断（眼圧測定・眼底検査・角膜染色）と専門医紹介が肝要。{note}"
        )
    if category == "musculoskeletal":
        species_specific = ""
        if species == "horse":
            species_specific = "馬では蹄葉炎・舟状骨症候群・腱炎・関節炎が運動性能を著しく低下させる主要疾患。"
        elif species in ("reptile", "tortoise", "snake", "lizard", "amphibian"):
            species_specific = "爬虫類・両生類ではビタミンD/UV-B不足・Ca/P比不均衡による代謝性骨疾患（MBD）が最頻発。"
        elif species in ("bird", "parakeet", "parrot"):
            species_specific = "鳥類では栄養性骨軟化症・産卵関連カルシウム枯渇・気骨折（中空気骨）が主要病態。"
        elif species in ("rabbit", "guinea_pig", "chinchilla", "hamster", "degu", "sugar_glider"):
            species_specific = "小型哺乳類では骨折・脱臼（取り扱い時・落下）・脊椎損傷が主要外傷で、脆い骨格が背景。"
        return (
            f"{prefix}の原因は外傷性（骨折・脱臼・靭帯損傷）、変性性（変形性関節症）、発達異常（股関節形成不全・肘関節形成不全・膝蓋骨脱臼）、免疫介在性（多発性関節炎）、感染性（骨髄炎・敗血症性関節炎）、栄養性（代謝性骨疾患・栄養性二次性副甲状腺機能亢進症）、腫瘍性（骨肉腫）、遺伝性（軟骨異形成）に分類される。"
            f"{species_specific}"
            f"肥満、過剰運動、不適切な栄養管理（成長期の過剰カロリー・カルシウム）が変性・発達性疾患のリスクを増大させる。{note}"
        )
    if category == "dental":
        return (
            f"{prefix}の原因は歯垢・歯石蓄積による細菌性炎症（歯周病）、不正咬合、外傷性歯破折、根尖周囲膿瘍、過長歯（草食動物・げっ歯類）、悪性腫瘍（口腔扁平上皮癌・線維肉腫）が主要因。"
            f"草食動物（ウサギ・モルモット・チンチラ・デグー）では歯は生涯成長し、繊維質不足・遺伝性不正咬合・外傷で過長歯と臼歯スパイク形成が起こる。"
            f"小型犬・短頭種では歯列圧迫による歯周病が多発。早期口腔ケアと年1回の歯科スケーリングが予防の基盤。{note}"
        )
    if category == "dermatological":
        return (
            f"{prefix}の原因は多岐にわたり、アレルギー性（アトピー性皮膚炎・食物アレルギー・蚤アレルギー性皮膚炎）、感染性（細菌性膿皮症・皮膚糸状菌症・マラセチア症）、寄生虫性（疥癬・毛包虫症・耳ダニ症）、免疫介在性（天疱瘡・狼瘡）、内分泌性（甲状腺機能低下症・クッシング症候群関連皮膚症）、栄養性、心理行動学的（過剰グルーミング・自咬）、腫瘍性に分類される。"
            f"環境因子（湿度・温度・寝床の衛生）と品種特異的素因が重要な発症修飾因子となる。{note}"
        )
    if category == "hematological":
        return (
            f"{prefix}の原因は産生不全（骨髄低形成・栄養欠乏・腎不全による造血刺激低下）、溶血（免疫介在性・寄生虫性・酸化的損傷・遺伝性赤血球膜異常）、出血（外傷・凝固障害・血小板異常）、消費（DIC・血栓症）、隔離（脾腫）に分類される。"
            f"感染性原因（FeLV・FIV・バベシア・ヘモプラズマ・エールリッヒア）、免疫介在性原因（IMHA・ITP）、薬剤性（化学療法・特定抗菌薬）、毒性（玉ねぎ・アセトアミノフェン・抗凝固殺鼠剤）が重要。{note}"
        )
    if category == "reproductive":
        return (
            f"{prefix}の原因は感染性（細菌・ウイルス・寄生虫）、解剖学的（胎位異常・骨盤狭窄）、内分泌性（黄体機能不全・プロラクチン異常）、代謝性（妊娠中毒症・低カルシウム血症）、外傷性、腫瘍性（乳腺腫瘍・精巣腫瘍・前立腺癌）、遺伝性、加齢性が含まれる。"
            f"早期避妊去勢手術はホルモン依存性腫瘍・子宮蓄膿症・前立腺肥大症の予防効果が明確に示されている（特に雌の早期避妊と乳腺腫瘍リスク低下の関係）。{note}"
        )
    if category == "toxicity":
        return (
            f"{prefix}の原因は特定の毒性物質への摂取・吸入・経皮吸収である。"
            f"代表的毒性源: 家庭用化学物質（漂白剤・洗剤・界面活性剤）、医薬品の過量投与（人用 OTC・NSAID・抗うつ薬）、有毒植物（種特異的: 犬のチョコレート・ブドウ、猫のユリ、馬の Ergot 等）、農薬・殺鼠剤、重金属（鉛・銅）、煙・煙草、食品中の毒（玉ねぎ・キシリトール）。"
            f"毒性の発現は用量依存性で、体重・種差・代謝能力・曝露経路・曝露時間により重症度が大きく異なる。"
            f"肝臓と腎臓が主要な標的臓器となる。{note}"
        )
    if category == "trauma":
        return (
            f"{prefix}の原因は外力（落下・衝突・圧迫・咬傷・鋭利物による切創）による組織の物理的損傷である。"
            f"不適切な飼育環境（狭小・過度に高い構造物・鋭利な突起物・滑りやすい床面）、他動物との闘争、不注意な取り扱い、逃走・脱走、交通事故が主要原因。"
            f"小型・幼若個体は重度の外傷を負いやすく、適切な飼育設備設計と安全管理により多くの外傷は予防可能である。"
            f"二次的合併症（感染・出血性ショック・組織壊死）を見越した初期評価が重要。{note}"
        )
    if category == "autoimmune":
        return (
            f"{prefix}の原因は自己免疫寛容の破綻による自己抗原への異常免疫応答である。"
            f"遺伝的素因、感染症による分子擬態、薬物投与、紫外線曝露、ホルモン変動、ワクチン接種が誘因として報告されている。"
            f"自己抗体と自己反応性T細胞が正常組織を攻撃・破壊することで多臓器障害を引き起こす。"
            f"診断には特異的自己抗体検査と組織病理学的評価が必要であり、長期免疫抑制療法と再発モニタリングが管理の中核となる。{note}"
        )
    if category == "nutritional":
        return (
            f"{prefix}の原因は必須栄養素の不足・過剰・不均衡である。"
            f"不適切な食事組成、吸収障害、代謝異常、需要増大（成長期・妊娠期・泌乳期）が関与する。"
            f"ビタミン・ミネラル・必須アミノ酸・必須脂肪酸の不均衡は骨格発育異常、免疫機能低下、皮膚・被毛変化、繁殖障害として顕在化する。"
            f"市販総合栄養食の品質、手作り食の栄養バランス、サプリメントの過剰補給、種特異的要求（猫のタウリン、モルモットのビタミンC、爬虫類のカルシウム/UV-B）の理解不足が主要リスク。{note}"
        )
    if category == "genetic_congenital":
        return (
            f"{prefix}の原因は胚発生期の遺伝子変異または染色体異常である。"
            f"遺伝様式は多様（常染色体優性・劣性、X連鎖、多因子遺伝）で、子宮内環境の異常、母体の感染症・薬物曝露・栄養欠乏も胎児器官形成に影響する。"
            f"近交係数の高い純血種・特定の閉鎖個体群で発生頻度が高い。"
            f"繁殖前の遺伝子検査と保因者除外プログラムが集団レベルでの発生抑制に重要。{note}"
        )
    if category == "degenerative":
        return (
            f"{prefix}の原因は加齢に伴う組織の進行性変性と修復能低下である。"
            f"軟骨・椎間板・神経組織など再生能力が限られる組織で特に顕著に進行する。"
            f"遺伝的素因、過体重による慢性的機械的負荷、反復性微小外傷、酸化ストレス、慢性炎症の持続が促進因子。"
            f"早期発見と適切な体重管理・運動療法・抗炎症療法により進行を遅延可能。{note}"
        )
    if category == "behavioral":
        return (
            f"{prefix}の原因は神経内分泌系の調節障害、遺伝的素因、社会化不足、過去のトラウマ体験、環境ストレス、内科疾患（疼痛・甲状腺疾患・認知機能不全）の影響が複雑に関与する。"
            f"発達期（社会化期）の経験不足、慢性的環境ストレス、罰主体の躾、生活変化（飼い主変更・引越し・新規動物導入）が誘因となる。"
            f"行動学的問題は患畜のQOLと飼い主との関係性に直結するため、内科疾患の除外と環境改善＋行動修正＋必要に応じた薬物療法の統合的アプローチが必要。{note}"
        )
    # generic
    return (
        f"{prefix}の正確な病因は症例により異なる。"
        f"遺伝的素因、環境要因（温度・湿度・衛生状態の不適切な管理）、感染性病原体への曝露、栄養バランスの偏り、免疫系の調節異常、加齢に伴う組織変化が単独または複合的に関与する。"
        f"原因の同定は治療方針の決定と再発予防に不可欠であり、病歴聴取・身体検査・補助検査の統合的評価により行う。{note}"
    )


def gen_transmission_ja(category: str, name_ja: str, species: str) -> str:
    sp_ja = SPECIES_JA.get(species, species)
    prefix = _disease_prefix(name_ja, sp_ja)

    if category == "viral_infection":
        return (
            f"{prefix}の伝播経路はウイルス病原体に依存する。"
            f"飛沫感染（呼吸器症状を呈するウイルス）、糞口感染（腸管ウイルス）、媒介動物（節足動物媒介ウイルス）、性的接触、経胎盤・経乳の垂直感染が主経路。"
            f"環境中のウイルス安定性により間接感染（汚染環境・器具・衣服）の成立リスクが異なる。"
            f"感染力の高いウイルスでは集団免疫獲得のためのワクチネーション普及率維持が公衆衛生上重要である。"
        )
    if category == "bacterial_infection":
        return (
            f"{prefix}の伝播経路は病原細菌の生態により多様である。"
            f"直接接触（咬傷・性的接触・経胎盤）、飛沫感染、糞口感染、媒介節足動物、環境内常在菌の日和見感染、汚染食品・水を介した経口感染を含む。"
            f"感染源動物の特定と隔離、適切な手指衛生、汚染器具・環境の消毒、媒介動物制御が伝播阻止の柱。"
            f"人獣共通病原体の場合は公衆衛生当局への報告と接触者検査が必要となる。"
        )
    if category == "respiratory_infection":
        return (
            f"{prefix}の主要な伝播経路は呼吸器分泌物の飛沫感染（咳・くしゃみ）である。"
            f"密閉空間での近接接触、共有食器・寝床、汚染した手・衣服を介した間接感染も成立する。"
            f"換気・密度管理・新規導入個体の隔離検疫（最低14日）・汚染環境の消毒（次亜塩素酸またはアルコール系）が伝播阻止に有効。"
            f"症状回復後も数週間にわたりウイルス・細菌を排出することがあるため、完全治癒確認まで他個体との接触を制限する。"
        )
    if category == "fungal_infection":
        return (
            f"{prefix}の伝播は真菌種により異なる。"
            f"皮膚糸状菌症は感染動物との直接接触または汚染環境（敷物・カーペット・グルーミング用品）の関節胞子経由で伝播する。"
            f"深在性真菌症（コクシジオイデス・ブラストミセス・ヒストプラズマ）は環境中の真菌胞子吸入により発症するため、動物間直接伝播は基本的に起こらない。"
            f"カンジダ・マラセチアは常在性で、免疫抑制下の日和見感染として発症する。"
        )
    if category == "parasitic":
        return (
            f"{prefix}の伝播経路は寄生虫種により決定される。"
            f"経口摂取（汚染食物・水・中間宿主の捕食）、経皮侵入（鉤虫・住血吸虫）、節足動物媒介（ダニ・蚊・ノミ）、糞口経路（コクシジウム・ジアルジア）、性的接触・経胎盤（特定原虫）が含まれる。"
            f"中間宿主と終宿主のライフサイクル理解が伝播阻止の鍵。"
            f"環境衛生の徹底、媒介動物制御、定期的駆虫が予防策となる。"
        )
    if category == "neoplasia":
        return (
            f"{prefix}を含む腫瘍性疾患は基本的に感染性ではなく、動物間の直接伝播は通常生じない。"
            f"ただし発癌性ウイルス（FeLV・パピローマウイルス等）の感染は動物間伝播し、後にウイルス関連腫瘍を引き起こす可能性がある。"
            f"犬伝染性性器腫瘍（CTVT）とタスマニアデビル顔面腫瘍は例外的に腫瘍細胞そのものが直接伝播する稀な例。"
            f"遺伝的素因は親から子へ垂直的に継承されるため、罹患家系の繁殖管理が重要。"
        )
    if category == "endocrine_metabolic":
        return (
            f"{prefix}は非感染性疾患のため動物間の直接伝播は生じない。"
            f"ただし同一環境要因（高炭水化物食・運動不足・肥満を誘発する飼育条件）を共有する複数頭飼育で同時罹患することがある。"
            f"遺伝性素因（特定品種のクッシング症候群・糖尿病感受性）は親から子へ継承される。"
            f"ヒトには伝播しないが、感染源として誤解されないよう飼い主への正確な情報提供が必要。"
        )
    if category == "toxicity":
        return (
            f"{prefix}は感染性疾患ではないため動物間の直接伝播は生じない。"
            f"毒性物質への曝露は環境要因であり、同一環境内の複数の動物が同時に罹患する集団中毒は伝播ではなく共通曝露による。"
            f"原因物質の特定と環境からの除去、他動物への曝露リスク評価、適切な保管・廃棄方法の指導が同種事故防止に重要。"
            f"ヒトへの曝露リスクも同時に評価する。"
        )
    if category == "trauma":
        return (
            f"{prefix}は外傷性疾患のため動物間の直接伝播は生じない。"
            f"ただし同一環境の物理的危険因子（狭小ケージ・滑床・他動物との接触）により複数の動物が連続的に外傷を受けることがある。"
            f"事故原因の特定と環境改善（飼育設備の見直し・他動物分離・床材の改良）が再発と他個体への波及防止に必須。"
        )
    if category == "autoimmune":
        return (
            f"{prefix}は自己免疫性疾患のため動物間の直接伝播は生じない。"
            f"ただし発症誘因として感染症（分子擬態によるT細胞活性化）、ワクチン接種、薬物投与、紫外線曝露が報告されており、これらの環境要因を共有する集団では発症率が上昇する可能性がある。"
            f"遺伝的素因（HLA/DLA関連）は親から子へ継承されるため、罹患個体の繁殖は慎重に検討する。"
        )
    if category == "nutritional":
        return (
            f"{prefix}は非感染性のため動物間の直接伝播は生じない。"
            f"同一群内で複数動物が同時発症する場合があるが、これは共通の不適切な食餌に起因する集団発生であり伝染ではない。"
            f"群全体への食事改善と栄養素補正により集団的に解決する必要がある。"
            f"飼育者教育（栄養学的基礎・種特異的要求の理解）が再発防止に最も重要。"
        )
    if category == "renal_urinary":
        return (
            f"{prefix}は主に非感染性疾患のため動物間の直接伝播は通常生じない。"
            f"細菌性尿路感染・腎盂腎炎の場合のみ間接的伝播の可能性があるが、本質的には個別罹患。"
            f"レプトスピラ症は人獣共通感染症として尿を介して伝播するため、感染確認時には公衆衛生当局への報告と接触者管理が必要。"
            f"遺伝性腎疾患（PKD等）は親から子へ継承され、繁殖管理が重要。"
        )
    if category == "cardiac":
        return (
            f"{prefix}は非感染性疾患のため動物間の直接伝播は生じない。"
            f"ただし遺伝性心疾患（DCM・HCMの素因品種）は親から子へ継承されるため、罹患個体の繁殖を避けることが集団レベルでの発生抑制に重要。"
            f"感染性心内膜炎の場合は原因菌が他の感染部位から血行性に心臓に到達するもので、心臓自体からの動物間伝播はない。"
        )
    if category == "respiratory_other":
        return (
            f"{prefix}は非感染性疾患のため動物間の直接伝播は生じない。"
            f"ただしアレルギー性疾患では同一環境（タバコの煙・室内塵・化学物質）への曝露で複数個体が同時発症することがある。"
            f"短頭種気道症候群・気管虚脱・喉頭麻痺は解剖学的素因によるもので、品種ごとの遺伝的素因が背景にある。"
        )
    if category == "gastrointestinal":
        return (
            f"{prefix}の伝播は原因により異なる。"
            f"感染性原因（パルボウイルス・サルモネラ・寄生虫）は糞口経路で他個体に伝播する。"
            f"非感染性原因（IBD・腫瘍・機械的閉塞・運動機能障害）は動物間で伝播しない。"
            f"汚染環境の消毒、新規導入個体の検疫、糞便管理の徹底が感染性消化器疾患の予防に重要。"
        )
    if category == "neurological":
        return (
            f"{prefix}は原因により伝播性が異なる。"
            f"感染性脳炎・髄膜炎（細菌性・ウイルス性・原虫性）は原因病原体に応じた経路で伝播する。"
            f"特発性てんかん・変性性疾患・腫瘍性疾患は動物間で伝播しない。"
            f"狂犬病（人獣共通）は唾液を介した咬傷で伝播するため、ワクチネーションと野生動物との接触回避が決定的に重要。"
        )
    if category == "ophthalmic":
        return (
            f"{prefix}の伝播は原因により異なる。"
            f"感染性結膜炎（猫ヘルペスウイルス・クラミジア・マイコプラズマ）は飛沫・接触感染で他猫に伝播。"
            f"非感染性原因（白内障・緑内障・網膜変性）は動物間で伝播しない。"
            f"遺伝性眼疾患（コリーアイ症候群・PRA等）は親から子へ継承される。"
        )
    if category == "musculoskeletal":
        return (
            f"{prefix}は非感染性疾患のため動物間の直接伝播は通常生じない。"
            f"感染性骨髄炎・敗血症性関節炎の場合のみ原因病原体が血行性に伝播する可能性があるが、関節疾患自体は個別罹患。"
            f"遺伝性整形外科疾患（股関節形成不全・椎間板変性等）は親から子へ継承され、繁殖管理が集団的発生抑制に重要。"
        )
    if category == "dental":
        return (
            f"{prefix}は非感染性疾患のため動物間の直接伝播は生じない。"
            f"歯周病の原因細菌は口腔常在菌であり、外部感染源ではない。"
            f"不正咬合の遺伝性素因（短頭種・小型犬）は親から子へ継承される。"
            f"草食動物の不正咬合は繊維質不足という共通飼育要因により集団的に発症することがある。"
        )
    if category == "dermatological":
        return (
            f"{prefix}の伝播は原因により異なる。"
            f"感染性皮膚疾患（皮膚糸状菌症・疥癬・耳ダニ）は接触感染で動物間伝播する。"
            f"アレルギー性・免疫介在性・内分泌性皮膚疾患は伝播しない。"
            f"皮膚糸状菌症（特にMicrosporum canis）と疥癬は人獣共通感染症として飼い主にも伝播するため公衆衛生上の配慮が必要。"
        )
    if category == "hematological":
        return (
            f"{prefix}の伝播は原因により異なる。"
            f"感染性血液疾患（バベシア・エールリッヒア・ヘモプラズマ）はダニ媒介で伝播する。"
            f"FeLV関連の貧血・骨髄抑制はウイルス感染が背景。"
            f"免疫介在性・栄養性・遺伝性血液疾患は動物間で伝播しない。"
            f"輸血関連感染症リスクのため、供血動物は血液感染症スクリーニングを実施。"
        )
    if category == "reproductive":
        return (
            f"{prefix}の伝播は原因により異なる。"
            f"感染性生殖器疾患（ブルセラ症・ヘルペスウイルス・性器腫瘍CTVT）は性的接触・経胎盤で伝播する。"
            f"非感染性原因（子宮蓋膿症・難産・腫瘍）は伝播しない。"
            f"早期避妊去勢手術と感染性生殖器疾患のスクリーニング（特にブルセラ症は人獣共通）が予防に重要。"
        )
    if category == "genetic_congenital":
        return (
            f"{prefix}は遺伝性または先天性疾患のため動物間での後天的伝播は生じない。"
            f"遺伝形式（常染色体優性・劣性・X連鎖・多因子）に応じて親から子へ継承される。"
            f"集団レベルでの発生抑制には、繁殖前遺伝子検査、保因者除外、近親交配の回避が不可欠。"
            f"罹患家系の追跡と血統管理が重要となる。"
        )
    # generic fallback
    return (
        f"{prefix}の伝播性は原因病態により異なる。"
        f"感染性原因の場合は病原体特異的な経路（接触・飛沫・媒介動物・経胎盤）で動物間伝播する。"
        f"非感染性原因（外傷・代謝性・腫瘍性・変性性・遺伝性）は動物間で伝播しない。"
        f"原因の正確な同定により伝播リスク評価と予防策の立案が可能となる。"
    )


def gen_clinical_signs_ja(category: str, name_ja: str, species: str) -> str:
    sp_ja = SPECIES_JA.get(species, species)
    prefix = _disease_prefix(name_ja, sp_ja)

    if category in ("viral_infection", "bacterial_infection", "respiratory_infection", "fungal_infection"):
        sys_specific = ""
        if category == "respiratory_infection":
            sys_specific = " 呼吸器症状（咳・くしゃみ・鼻汁・呼吸困難）が前景となり、進行例では肺炎徴候を呈する。"
        elif category == "fungal_infection":
            sys_specific = (
                " 皮膚病変（円形脱毛・落屑・痂皮）、慢性鼻汁、または深在性真菌症では咳・体重減少・神経症状が見られる。"
            )
        return (
            f"{prefix}の臨床徴候は感染部位と病原体特性により多様だが、共通所見として発熱・元気消失・食欲不振・体重減少が認められる。"
            f"局所感染では発赤・腫脹・疼痛・排膿を、全身感染では脱水・敗血症・多臓器不全に進展しうる。{sys_specific}"
            f"幼若・高齢・免疫抑制状態は重症化リスクが高く、早期介入が予後改善に直結する。"
        )
    if category == "parasitic":
        return (
            f"{prefix}の臨床徴候は寄生虫種・寄生部位・寄生数により異なる。"
            f"消化管寄生では下痢・嘔吐・体重減少・腹部膨満、外部寄生では掻痒・脱毛・皮膚炎、心血管寄生では咳・運動不耐性・腹水、血液寄生では貧血・発熱・元気消失を呈する。"
            f"幼若・栄養不良個体では重症化しやすく、慢性経過では発育不良が顕著となる。"
        )
    if category == "neoplasia":
        return (
            f"{prefix}の臨床徴候は罹患臓器と腫瘍の種類により多様。"
            f"一般的所見: 進行性の腫瘤形成・体重減少・食欲不振・元気消失・貧血。"
            f"体表腫瘤では触知可能な腫脹・疼痛を、内臓腫瘍では腹部膨満・嘔吐・下痢・呼吸困難・リンパ節腫大などの非特異的症状を呈する。"
            f"傍腫瘍症候群として高カルシウム血症（リンパ腫・肛門周囲腺癌）や低血糖（インスリノーマ）を合併することがある。"
        )
    if category == "endocrine_metabolic":
        return (
            f"{prefix}の臨床徴候はホルモン異常または代謝障害の種類により特異的パターンを示す。"
            f"糖尿病: 多飲多尿・多食・体重減少。甲状腺機能亢進: 体重減少・多食・多動・心拍数上昇。"
            f"クッシング症候群: 腹部膨満・脱毛・多飲多尿・薄い皮膚。アジソン病: 元気消失・嘔吐・下痢・電解質異常。"
            f"低血糖: 振戦・痙攣・意識低下。早期は無症候性に進行することが多く、定期的内分泌スクリーニングが早期発見の鍵。"
        )
    if category == "renal_urinary":
        return (
            f"{prefix}の臨床徴候は病態と進行段階により異なる。"
            f"慢性腎臓病: 多飲多尿・体重減少・食欲不振・嘔吐・口臭・脱水（早期は無症候）。"
            f"急性腎障害: 無尿/乏尿・嘔吐・元気消失・電解質異常。"
            f"下部尿路疾患（FLUTD/FIC）: 頻尿・排尿困難・血尿・排尿時痛・不適切排尿、雄では尿閉（緊急）。"
            f"尿路感染: 頻尿・血尿・濁尿・発熱（腎盂腎炎時）。"
        )
    if category == "cardiac":
        return (
            f"{prefix}の臨床徴候は心機能低下の程度により段階的に進行する。"
            f"代償期（無症候）: 心雑音が唯一の所見、聴診で発見される。"
            f"早期心不全: 運動不耐性・咳（左心不全）・腹水（右心不全）。"
            f"進行性心不全: 呼吸困難・チアノーゼ・失神・夜間咳。"
            f"末期: 起座呼吸・肺水腫・心原性ショック。"
            f"猫では FATE（大動脈血栓塞栓症）として急性後肢麻痺・冷感・疼痛・パルス消失で発症することがある。"
        )
    if category == "respiratory_other":
        return (
            f"{prefix}の臨床徴候は気道閉塞・換気障害の部位により異なる。"
            f"上気道: いびき・吸気性ストライダー・運動不耐性・吸気性チアノーゼ（短頭種気道症候群）。"
            f"気管: 短く乾性の発作的咳（gander-honk）・ストライダー（気管虚脱）。"
            f"下気道: 慢性咳・呼気性呼吸困難・喘鳴・換気不全（喘息・COPD様病態）。"
            f"突発的悪化はストレス・運動・気温変化で誘発される。"
        )
    if category == "gastrointestinal":
        return (
            f"{prefix}の臨床徴候は消化管病変の部位と病態により異なる。"
            f"上部消化管: 嘔吐・吐血・食欲不振。"
            f"小腸: 下痢（小腸性: 量多・回数少・体重減少を伴う）・嘔吐・腹痛。"
            f"大腸: 下痢（大腸性: 量少・回数多・粘液・血便・テネスムス）。"
            f"急性腹症: 強い腹痛・嘔吐・ショック徴候・腹部触診で腫瘤や緊張感（GDV・腸捻転・腸閉塞）は緊急評価が必要。"
        )
    if category == "neurological":
        return (
            f"{prefix}の臨床徴候は罹患部位（前脳・脳幹・小脳・脊髄・末梢神経）により局在化所見を示す。"
            f"前脳: 発作・行動変化・盲目・周徊・運動失調。"
            f"脳幹: 脳神経障害・運動失調・意識障害。"
            f"小脳: 企図振戦・低測定運動失調・広基歩行。"
            f"脊髄: 四肢麻痺/対麻痺・排尿障害・反射異常（病変高位で異なる）。"
            f"末梢神経: 筋萎縮・反射低下・遠位部優位の弛緩性麻痺。"
        )
    if category == "ophthalmic":
        return (
            f"{prefix}の臨床徴候は罹患部位（角膜・結膜・前房・水晶体・網膜）と病態により異なる。"
            f"結膜炎: 結膜充血・分泌物・流涙・眼瞼痙攣。"
            f"角膜潰瘍: 流涙・眼瞼痙攣・羞明・角膜混濁（蛍光染色陽性）。"
            f"緑内障: 急性眼痛・角膜浮腫・散瞳・眼球膨大・視覚消失。"
            f"白内障: 水晶体混濁による進行性視覚障害。"
            f"網膜疾患: 夜盲先行の進行性視覚障害（PRA等）・急性視覚消失（網膜剥離）。"
        )
    if category == "musculoskeletal":
        return (
            f"{prefix}の臨床徴候は罹患部位と病態の急性/慢性により異なる。"
            f"急性外傷: 跛行（非荷重）・腫脹・疼痛・変形（骨折・脱臼）。"
            f"慢性変性: 起立困難・運動不耐性・跛行（運動後悪化・寒冷で悪化）・関節腫脹（OA等）。"
            f"発達性異常: 子犬期から軽度跛行（股関節・肘関節形成不全）。"
            f"感染性: 発熱を伴う関節腫脹・疼痛（敗血症性関節炎）。"
        )
    if category == "dental":
        return (
            f"{prefix}の臨床徴候は歯科疾患の種類と進行により多様。"
            f"歯周病: 口臭・歯肉発赤/腫脹・流涎・採食困難・顔面腫脹（根尖膿瘍時）。"
            f"不正咬合（草食動物）: 流涎・採食速度低下・選択的採食・体重減少・糞便量減少・眼球突出・顎下膿瘍。"
            f"歯根破折: 採食困難・片側咀嚼・口臭。"
            f"口腔腫瘍: 口腔内腫瘤・出血・流涎・口臭・採食困難。"
        )
    if category == "dermatological":
        return (
            f"{prefix}の臨床徴候は原因と病期により異なる。"
            f"急性: 紅斑・水疱・湿潤性病変・激しい掻痒・脱毛（接触性皮膚炎・蕁麻疹）。"
            f"慢性: 苔癬化・色素沈着・脱毛・落屑・痂皮（アトピー性皮膚炎・慢性膿皮症）。"
            f"分布パターンが診断に有用: 顔面・指趾（アトピー）、耳・腹側（蚤アレルギー）、対称性脱毛（内分泌性）、円形病変（皮膚糸状菌・毛包虫）。"
        )
    if category == "hematological":
        return (
            f"{prefix}の臨床徴候は血液成分異常の種類により異なる。"
            f"貧血: 粘膜蒼白・元気消失・運動不耐性・頻脈・呼吸促迫（重度では失神・心雑音）。"
            f"出血傾向: 紫斑・粘膜出血・血尿・血便・関節血腫（凝固障害・血小板異常）。"
            f"血栓症: 急性肢痛・麻痺（FATE等）・呼吸困難（肺塞栓）。"
            f"白血球減少: 発熱・敗血症・反復性感染。"
            f"溶血性貧血: 黄疸・暗色尿・脾腫。"
        )
    if category == "reproductive":
        return (
            f"{prefix}の臨床徴候は生殖器病態により異なる。"
            f"子宮蓋膿症: 多飲多尿・嘔吐・元気消失・腹部膨満・陰部分泌物（開放型）または無症候進行（閉鎖型）。"
            f"乳腺炎: 乳房腫脹・疼痛・発熱・乳汁異常。"
            f"前立腺疾患: 排尿困難・血尿・排便困難・後肢跛行。"
            f"難産: 分娩遷延・努責持続・分娩間隔異常・母体ぐったり。"
            f"妊娠中毒症: 終末期妊娠の元気消失・食欲不振・神経症状。"
        )
    if category == "toxicity":
        return (
            f"{prefix}の臨床徴候は毒性物質の種類と曝露量により急性〜慢性まで多様。"
            f"消化器症状（嘔吐・下痢・流涎・腹痛）が最も一般的な初期所見。"
            f"神経毒では振戦・痙攣・運動失調・昏睡。"
            f"肝毒では黄疸・凝固障害・肝性脳症。"
            f"腎毒では乏尿・尿毒症徴候。"
            f"血液毒では貧血・出血傾向・メトヘモグロビン血症。"
            f"心血管毒では不整脈・低血圧・ショック。"
            f"急性曝露では症状発現が迅速で、早期除染と支持療法が予後を決定する。"
        )
    if category == "trauma":
        return (
            f"{prefix}の臨床徴候は外傷部位と重症度により異なる。"
            f"骨折: 跛行（非荷重）・腫脹・捻髪音・変形・疼痛。"
            f"裂傷: 出血・組織欠損・感染リスク。"
            f"内臓損傷: ショック徴候・腹部緊張・呼吸困難（横隔膜ヘルニア・気胸）。"
            f"脳挫傷: 意識低下・瞳孔異常・運動失調・発作。"
            f"脊椎損傷: 麻痺・反射異常・排尿障害。"
            f"重度外傷では多発外傷の評価と緊急安定化が予後を左右する。"
        )
    if category == "autoimmune":
        return (
            f"{prefix}の臨床徴候は罹患組織により多様。"
            f"IMHA: 黄疸・蒼白・元気消失・呼吸促迫。"
            f"IMTP: 紫斑・粘膜出血・血便・血尿。"
            f"多発性関節炎: 移動性跛行・発熱・関節腫脹。"
            f"天疱瘡: 鱗状/水疱性皮膚病変・粘膜病変・痂皮形成。"
            f"狼瘡（SLE）: 多臓器症状（皮膚・関節・腎・血液）。"
            f"再燃寛解を繰り返す経過が特徴的。"
        )
    if category == "nutritional":
        return (
            f"{prefix}の臨床徴候は欠乏または過剰の栄養素により特異的パターンを示す。"
            f"カルシウム不足: 骨軟化・病的骨折・痙攣・成長不良。"
            f"ビタミンA不足: 眼疾患・皮膚角化異常・夜盲・繁殖障害。"
            f"ビタミンC不足（モルモット）: 関節腫脹・出血傾向・歯周病・成長不良。"
            f"タンパク質-エネルギー欠乏: 削痩・筋萎縮・低アルブミン血症・浮腫。"
            f"ビタミンD/UV-B不足（爬虫類）: 代謝性骨疾患・骨軟化。"
        )
    if category == "behavioral":
        return (
            f"{prefix}の臨床徴候は行動学的問題の種類により異なる。"
            f"分離不安: 飼い主不在時の破壊行動・過剰な発声・不適切な排泄。"
            f"恐怖症（雷・花火）: 震え・隠れる・パンティング・破壊行動・脱走企図。"
            f"攻撃行動: 唸り・歯むき・咬みつき（恐怖・縄張り・資源防衛など分類）。"
            f"強迫行動: 反復性無目的行動（尾追い・脇腹吸引・過剰グルーミング）。"
            f"認知機能不全: 周徊・夜鳴き・社会的相互作用低下・排泄場所異常。"
        )
    # generic
    return (
        f"{prefix}の臨床徴候は病態と進行段階により多様である。"
        f"一般的非特異的所見（食欲不振・元気消失・体重減少）に加え、罹患臓器・系統に特異的な症状が顕在化する。"
        f"病歴聴取と詳細な身体検査により症状パターンを把握し、補助検査で確定診断に至る。"
        f"早期発見と適切な介入が予後改善の鍵となる。"
    )


def gen_differential_diagnosis_ja(category: str, name_ja: str, species: str) -> str:
    sp_ja = SPECIES_JA.get(species, species)
    prefix = _disease_prefix(name_ja, sp_ja)

    if category in ("viral_infection", "bacterial_infection", "respiratory_infection"):
        return (
            f"{prefix}の鑑別診断では、他の感染性病原体（細菌・ウイルス・真菌・寄生虫）による類似症状、"
            f"非感染性炎症疾患（自己免疫・アレルギー）、腫瘍性疾患、中毒を考慮する。"
            f"発熱と全身症状を呈する場合は免疫介在性疾患・リンパ腫・全身性炎症反応症候群との鑑別が必要。"
            f"特異的診断には培養・PCR・血清学的検査・組織病理学的評価が有用。"
        )
    if category == "fungal_infection":
        return (
            f"{prefix}の鑑別診断では、細菌性皮膚感染・寄生虫性皮膚疾患（疥癬・毛包虫症）、"
            f"アレルギー性皮膚炎（アトピー・食物アレルギー）、自己免疫性皮膚疾患（天疱瘡）、"
            f"内分泌性皮膚症（甲状腺機能低下症・クッシング症候群）、"
            f"皮膚腫瘍を考慮する。"
            f"深在性真菌症の場合は他の慢性感染症・腫瘍性疾患・多臓器免疫介在性疾患との鑑別が重要。"
        )
    if category == "parasitic":
        return (
            f"{prefix}の鑑別診断では、他の寄生虫感染、感染性腸炎（ウイルス・細菌）、IBD、食物不耐性、"
            f"消化管腫瘍、消化管異物、慢性膵炎を考慮する。"
            f"皮膚寄生虫感染では他の皮膚感染症・アレルギー性皮膚炎との鑑別が重要。"
            f"血液寄生虫では免疫介在性溶血性貧血・非再生性貧血との鑑別が必要。"
            f"糞便検査（直接塗抹・浮遊法・PCR）と血液検査による多角的評価を行う。"
        )
    if category == "neoplasia":
        return (
            f"{prefix}の鑑別診断では、良性腫瘍と悪性腫瘍の区別、"
            f"非腫瘍性腫瘤（肉芽腫・膿瘍・嚢胞・血腫）、過形成性病変、炎症性偽腫瘍を考慮する。"
            f"体表腫瘤では脂肪腫・皮膚付属器腫瘍・マスト細胞腫・軟部組織肉腫の鑑別が必要。"
            f"内臓腫瘍では臓器特異的な良性病変と悪性腫瘍の鑑別に画像診断と細胞診/組織診が不可欠。"
            f"転移性腫瘍と原発性腫瘍の区別も重要。"
        )
    if category == "endocrine_metabolic":
        return (
            f"{prefix}の鑑別診断では、他の内分泌疾患（甲状腺疾患・副腎疾患・糖尿病・副甲状腺疾患）、"
            f"慢性腎臓病、肝疾患（門脈体循環シャント）、慢性炎症性疾患、腫瘍性疾患（傍腫瘍症候群）、"
            f"医原性（長期ステロイド・薬剤性）を考慮する。"
            f"内分泌スクリーニング（T4・ACTH刺激試験・低用量デキサメタゾン抑制試験・血糖・フルクトサミン）と画像診断（副腎・甲状腺超音波）による多角的評価が必要。"
        )
    if category == "renal_urinary":
        return (
            f"{prefix}の鑑別診断では、他の腎疾患（CKD・AKI・腎盂腎炎・腎リンパ腫）、"
            f"下部尿路疾患（尿石症・FIC・尿路感染・尿道閉塞）、"
            f"全身性疾患による二次性腎障害（糖尿病・甲状腺機能亢進症・高血圧）、"
            f"中毒（NSAID・抗凍液・ユリ）、"
            f"前立腺疾患（雄）を考慮する。"
            f"尿検査（比重・蛋白・尿沈渣）・尿培養・血液生化学・SDMA・腹部画像診断による評価を行う。"
        )
    if category == "cardiac":
        return (
            f"{prefix}の鑑別診断では、他の心疾患（DCM/HCM・弁膜疾患・先天性心奇形・不整脈・心嚢液貯留）、"
            f"呼吸器疾患（肺炎・気管支炎・気管虚脱・肺水腫の心原性以外の原因）、"
            f"循環血液量異常、貧血、甲状腺機能亢進症（猫）、心筋炎（感染性・免疫介在性）を考慮する。"
            f"心エコー検査が第一選択で、心電図・胸部X線・NT-proBNPなどのバイオマーカーを併用する。"
        )
    if category == "respiratory_other":
        return (
            f"{prefix}の鑑別診断では、他の呼吸器疾患（肺炎・気管支炎・腫瘍・胸水・気胸・肺塞栓）、"
            f"心原性肺水腫、上気道閉塞（短頭種気道症候群・気管虚脱・喉頭麻痺）、"
            f"アレルギー性疾患（喘息・好酸球性気管支炎）、"
            f"全身性疾患による呼吸困難（貧血・敗血症・酸塩基平衡異常）を考慮する。"
            f"胸部X線・胸部CT・気管支洗浄液検査・心エコー検査による多角的評価を行う。"
        )
    if category == "gastrointestinal":
        return (
            f"{prefix}の鑑別診断では、他の消化器疾患（感染性・IBD・腫瘍・閉塞・運動機能障害・膵炎・肝胆道疾患）、"
            f"全身性疾患による消化器症状（CKD・甲状腺機能亢進症・副腎機能低下症）、"
            f"中毒、ストレス性、食物アレルギーを考慮する。"
            f"糞便検査、血液生化学、腹部超音波、内視鏡検査と生検による組織学的評価が確定診断に有用。"
        )
    if category == "neurological":
        return (
            f"{prefix}の鑑別診断では、DAMNIT-V分類（変性性・解剖学的・代謝性・腫瘍性・栄養性・炎症性/感染性・特発性・外傷性・血管性）に基づき体系的に検討する。"
            f"発作では特発性てんかん・代謝性発作（低血糖・低カルシウム血症）・腫瘍・脳炎を、"
            f"運動失調では小脳疾患・前庭疾患・脊髄疾患を、"
            f"麻痺では椎間板疾患・脳血管障害・末梢神経障害を考慮する。"
            f"MRI/CT・脳脊髄液検査・神経学的検査の局在診断が鑑別の柱。"
        )
    if category == "ophthalmic":
        return (
            f"{prefix}の鑑別診断では、他の眼科疾患（感染性結膜炎・角膜潰瘍・緑内障・白内障・網膜疾患・ぶどう膜炎・眼内腫瘍）、"
            f"全身性疾患の眼科徴候（高血圧性網膜症・FIP・FeLV・甲状腺機能亢進症・糖尿病性白内障）を考慮する。"
            f"眼圧測定・蛍光染色・スリットランプ検査・眼底検査・眼超音波検査による系統的評価を行う。"
            f"重度急性眼痛・視覚消失は緊急対応が必要。"
        )
    if category == "musculoskeletal":
        return (
            f"{prefix}の鑑別診断では、他の整形外科疾患（骨折・脱臼・靭帯損傷・OA・発達性疾患・感染性関節炎・腫瘍）、"
            f"神経学的疾患による跛行（椎間板疾患・末梢神経障害）、"
            f"免疫介在性多発性関節炎、"
            f"代謝性骨疾患を考慮する。"
            f"X線検査・関節液検査・MRI・整形外科的検査による局在診断を行う。"
        )
    if category == "dental":
        return (
            f"{prefix}の鑑別診断では、他の歯科疾患（歯周病・歯根膿瘍・不正咬合・歯破折・歯瘻）、"
            f"口腔腫瘍（扁平上皮癌・線維肉腫・メラノーマ）、"
            f"口腔粘膜疾患（口内炎・自己免疫性疾患）、"
            f"鼻腔疾患（鼻炎・腫瘍）の二次的歯科症状を考慮する。"
            f"歯科X線検査・口腔内視診・必要に応じた組織病理学的評価を行う。"
        )
    if category == "dermatological":
        return (
            f"{prefix}の鑑別診断では、他の皮膚疾患（アレルギー性・感染性・寄生虫性・免疫介在性・内分泌性・腫瘍性）を考慮する。"
            f"診断アプローチ: 皮膚搔爬検査（疥癬・毛包虫）、テープ採取（マラセチア・細菌）、培養（細菌・真菌）、皮膚生検（自己免疫性・腫瘍）、内分泌検査（甲状腺・副腎）、食物除去試験（食物アレルギー）。"
            f"分布パターンと臨床経過から原因を絞り込む。"
        )
    if category == "hematological":
        return (
            f"{prefix}の鑑別診断では、他の血液疾患（産生不全・溶血性・出血性・凝固性）と原因病態を考慮する。"
            f"貧血では再生性/非再生性の区別を行い、再生性では溶血（IMHA・寄生虫）・失血を、非再生性では骨髄抑制・慢性疾患・腎性貧血を鑑別する。"
            f"血小板異常では産生（骨髄）・破壊（免疫介在性）・消費（DIC）・隔離（脾）を、"
            f"凝固異常では凝固因子欠乏・抗凝固薬中毒・肝不全を鑑別する。"
            f"CBC・末梢血塗抹標本・骨髄検査・凝固系検査が必須。"
        )
    if category == "reproductive":
        return (
            f"{prefix}の鑑別診断では、他の生殖器疾患（感染性・解剖学的・内分泌性・腫瘍性）、"
            f"全身性疾患の生殖器徴候、"
            f"非生殖器疾患による類似症状（CKD等の多飲多尿）を考慮する。"
            f"生殖器超音波検査、ホルモン測定、細菌培養、必要に応じた組織病理学的評価を行う。"
        )
    if category == "toxicity":
        return (
            f"{prefix}の鑑別診断では、急性感染症（敗血症・急性肝炎・急性腎炎）、"
            f"代謝性緊急症（糖尿病性ケトアシドーシス・副腎クリーゼ）、"
            f"急性腹症、神経疾患（てんかん・前庭疾患）、"
            f"内因性毒素（尿毒症・肝性脳症）を考慮する。"
            f"曝露歴の詳細な聴取と毒性物質の検出（血中濃度測定・尿中代謝物検出）が確定診断に有用。"
        )
    if category == "trauma":
        return (
            f"{prefix}の鑑別診断では、外傷の部位と機序の特定が中心となる。"
            f"骨折部位・脱臼関節の同定、内臓損傷（実質臓器破裂・中空臓器穿孔）の評価、"
            f"頭部外傷の脳震盪・脳挫傷・頭蓋内出血の鑑別、"
            f"脊椎損傷の高位診断、"
            f"鈍的外傷と穿通性外傷の区別を行う。"
            f"画像診断（X線・超音波・FAST法・CT）と継続的バイタル評価が必須。"
        )
    if category == "autoimmune":
        return (
            f"{prefix}の鑑別診断では、感染性疾患（自己免疫類似症状）、腫瘍性疾患、代謝性疾患、薬剤性、医原性、原発性自己免疫疾患を考慮する。"
            f"自己抗体検査・組織病理学的評価（免疫蛍光染色含む）・補体検査・CBC・凝固系検査が診断の柱。"
            f"治療反応性も診断補助となる（免疫抑制療法への応答）。"
        )
    if category == "nutritional":
        return (
            f"{prefix}の鑑別診断では、吸収不良症候群（IBD・膵外分泌不全・リンパ管拡張症）、"
            f"内分泌疾患（副甲状腺機能亢進症・クッシング症候群）、"
            f"先天性代謝異常、腫瘍性疾患（傍腫瘍症候群）、"
            f"中毒（特定栄養素過剰）、慢性消耗性疾患を考慮する。"
            f"食事歴の詳細聴取と血中・尿中栄養素濃度測定、関連内分泌検査による評価を行う。"
        )
    if category == "behavioral":
        return (
            f"{prefix}の鑑別診断では、内科疾患による行動変化（疼痛・甲状腺疾患・認知機能不全・聴覚/視覚障害）、"
            f"神経学的疾患（脳腫瘍・てんかん・前頭葉症候群）、"
            f"環境性ストレス、"
            f"飼育管理上の不備（社会化不足・運動不足・栄養不良）を考慮する。"
            f"完全な内科的評価による身体疾患除外が行動学的診断の前提となる。"
        )
    # generic
    return (
        f"{prefix}の鑑別診断では、類似症状を呈する他疾患の系統的除外が必要である。"
        f"病歴聴取と身体検査による原因病態の絞り込み、血液検査・画像診断・組織病理学的評価による確定診断、"
        f"治療反応性による診断補助を組み合わせた多角的アプローチを行う。"
    )


def gen_prevention_ja(category: str, name_ja: str, species: str) -> str:
    sp_ja = SPECIES_JA.get(species, species)
    prefix = _disease_prefix(name_ja, sp_ja)

    if category in ("viral_infection", "bacterial_infection", "respiratory_infection"):
        return (
            f"{prefix}の予防は適切なワクチネーションプログラムの実施が中核である（利用可能な場合）。"
            f"衛生的飼育環境の維持、新規導入動物の検疫期間設定（最低14日、感染症によっては60日以上）、過密飼育の回避、適切な栄養管理による免疫力維持、ストレス軽減が重要。"
            f"感染動物との接触回避、汚染器具・環境の消毒（次亜塩素酸・アルコール系・第四級アンモニウム製剤を病原体に応じて選択）を徹底する。"
            f"定期的健康診断による早期発見と治療が蔓延防止に寄与する。"
        )
    if category == "fungal_infection":
        return (
            f"{prefix}の予防は感染源との接触回避と環境管理が中心。"
            f"皮膚糸状菌症: 感染動物・汚染環境（グルーミング用品・カーペット・寝具）との接触回避、新規導入動物のWood lamp検査と培養スクリーニング。"
            f"深在性真菌症: 流行地での過剰な土壌粉塵曝露回避（猟犬・農用動物）、地理的リスク評価。"
            f"カンジダ/マラセチアの日和見感染予防には基礎疾患（内分泌異常・免疫抑制）の適切な管理と長期抗菌薬使用の慎重な評価が重要。"
        )
    if category == "parasitic":
        return (
            f"{prefix}の予防は定期的駆虫・媒介動物制御・環境衛生の3本柱。"
            f"消化管寄生虫: 子犬子猫は2-4週齢から繰返し駆虫、成獣は便検査結果に基づく定期投与。"
            f"心血管寄生虫（フィラリア）: 流行地での年間予防投与（イベルメクチン・ミルベマイシン等）。"
            f"外部寄生虫: 月1回の外部寄生虫予防薬投与、環境清掃。"
            f"散歩後のダニチェック、媒介動物（ダニ・蚊・ノミ）の生息環境改善も重要。"
        )
    if category == "neoplasia":
        return (
            f"{prefix}の予防には、ホルモン依存性腫瘍に対する早期避妊去勢手術（乳腺腫瘍・前立腺癌・精巣腫瘍・子宮腺癌・肛門腺癌等）が確立された予防策。"
            f"発癌性物質への曝露回避（タバコの煙・農薬・タール・特定の合成樹脂）、適正体重維持、抗酸化物質を含むバランスの取れた食事、紫外線過剰曝露の回避が予防に寄与する。"
            f"定期的健康診断（触診・画像診断・血液検査）による早期発見が最も実効性ある予防策。"
            f"発癌性ウイルス予防（FeLV ワクチン）も重要。"
        )
    if category == "endocrine_metabolic":
        return (
            f"{prefix}の予防は適正体重維持と適切な栄養管理が中核。"
            f"糖尿病: 肥満予防（BCS 4-5/9）、低炭水化物食、定期運動、ステロイド長期使用の回避。"
            f"甲状腺機能亢進症（猫）: ヨウ素過剰摂取の回避、缶詰食のBPA曝露低減、年1回のT4スクリーニング（10歳以上）。"
            f"クッシング症候群: 早期発見のための定期的臨床評価。"
            f"アジソン病: 確立された予防法なし、症状の早期認識が重要。"
        )
    if category == "renal_urinary":
        return (
            f"{prefix}の予防は腎機能の早期スクリーニングと環境管理が中心。"
            f"定期的健康診断（7歳以上は年1回、10歳以上は半年に1回）でクレアチニン・SDMA・尿比重・尿蛋白・血圧を評価。"
            f"水分摂取量増加（ウェットフード・循環式給水器）、腎毒性物質（NSAID過量・抗凍液・ユリ・特定抗菌薬）の管理。"
            f"FLUTD予防: ストレス軽減・低マグネシウム食・複数トイレ提供。"
            f"歯科ケアによる細菌の腎播種予防。"
        )
    if category == "cardiac":
        return (
            f"{prefix}の予防は遺伝性疾患の繁殖管理と早期発見が中核。"
            f"DCM/HCM素因品種（ドーベルマン・コッカースパニエル・メインクーン・ラグドール）の繁殖前心エコースクリーニング。"
            f"グレインフリー食関連DCM予防のためタウリン・カルニチン適切量含有食を選択。"
            f"フィラリア予防徹底による右心不全予防。"
            f"歯科ケアによる感染性心内膜炎予防。"
            f"定期的聴診による心雑音早期発見。"
        )
    if category == "respiratory_other":
        return (
            f"{prefix}の予防は環境因子の管理が中心。"
            f"タバコの煙・室内塵・化学香料・粉塵への曝露回避。"
            f"短頭種気道症候群: 適正体重維持、暑熱環境回避、必要に応じた外科的気道形成術。"
            f"気管虚脱: 適正体重維持、ハーネス使用（首輪回避）、誘発因子（興奮・暑熱・脱水）の管理。"
            f"喘息（猫）: アレルゲン特定と回避、室内環境改善。"
        )
    if category == "gastrointestinal":
        return (
            f"{prefix}の予防は栄養管理と環境管理が中心。"
            f"バランスの取れた高品質食、急激な食事変更回避、食物アレルゲンの特定と除去食。"
            f"草食動物（ウサギ・モルモット・チンチラ・デグー）: 高繊維チモシー乾草を給与量の80%以上、ペレット過剰摂取回避、新鮮野菜の段階的導入。"
            f"異物誤食予防（玩具・包装材・植物の管理）。"
            f"定期的駆虫、ストレス管理、適切なワクチネーション。"
        )
    if category == "neurological":
        return (
            f"{prefix}の予防は原因病態によって異なる。"
            f"感染性脳炎: 適切なワクチネーション（特に狂犬病・ジステンパー・FIP予防）と媒介動物制御。"
            f"特発性てんかん: 遺伝性素因品種の繁殖管理。"
            f"認知機能不全症候群: 知的刺激の提供、適度な運動、抗酸化サプリメント、SAMe等の補完療法。"
            f"外傷性脳脊髄損傷: 交通事故・落下事故予防、適切な飼育環境。"
            f"中毒予防: 環境管理。"
        )
    if category == "ophthalmic":
        return (
            f"{prefix}の予防は感染症対策と早期発見が中心。"
            f"感染性結膜炎: ワクチネーション（FHV-1・FCV）と感染猫との接触回避。"
            f"角膜潰瘍: 短頭種の眼球突出予防（眼球保護環境）、グルーミング時の眼科ケア。"
            f"白内障: 糖尿病の良好な血糖管理、遺伝性品種の繁殖管理、抗酸化物質補給。"
            f"緑内障: 素因品種の定期的眼圧測定。"
            f"全動物で年1回以上の眼科検診。"
        )
    if category == "musculoskeletal":
        return (
            f"{prefix}の予防は適正体重・適切な栄養・適度な運動が3本柱。"
            f"発達性疾患（HD・ED・OCD・FCP）予防: 大型犬の成長期過剰カロリー回避、適切なカルシウム/リン比、過度な運動・階段使用回避。"
            f"OA予防: 適正体重維持、関節サプリメント（グルコサミン・コンドロイチン・MSM）、低衝撃運動。"
            f"骨折・外傷予防: 安全な飼育環境、リード散歩、滑床対策。"
            f"代謝性骨疾患予防: 適切な栄養とUV-B（爬虫類・若齢動物）。"
        )
    if category == "dental":
        return (
            f"{prefix}の予防は口腔ケアと栄養管理が中心。"
            f"小動物（犬猫）: 毎日の歯磨き、デンタルガム・歯科食、年1回の歯科スケーリング（麻酔下）。"
            f"草食動物（ウサギ・モルモット・チンチラ・デグー）: 高繊維チモシー乾草を主食（自然な摩耗）、定期的歯科検診、不正咬合早期発見。"
            f"鳥類: 適切なくちばし磨耗のための硬質食材・カトルボーン。"
            f"早期の歯垢蓄積予防が歯周病・歯根膿瘍予防の鍵。"
        )
    if category == "dermatological":
        return (
            f"{prefix}の予防はアレルゲン管理と環境衛生が中心。"
            f"蚤アレルギー: 年間を通じた蚤予防薬。"
            f"アトピー性皮膚炎: 環境アレルゲン低減（フィルター・寝具洗濯）、皮膚バリア機能維持（オメガ3補給）。"
            f"細菌性皮膚感染: 基礎皮膚疾患の管理、適切な被毛グルーミング、湿潤環境回避。"
            f"皮膚糸状菌症: 感染動物隔離、環境消毒。"
            f"耳のケアと定期的耳洗浄による外耳炎予防。"
        )
    if category == "hematological":
        return (
            f"{prefix}の予防は基礎疾患の管理が中心。"
            f"感染性血液疾患（バベシア・エールリッヒア・ヘモプラズマ・FeLV）: ワクチネーションと媒介動物制御。"
            f"中毒性貧血: 玉ねぎ・アセトアミノフェン・抗凝固殺鼠剤の管理徹底。"
            f"免疫介在性疾患: 確立された予防法なし、早期発見と治療が重要。"
            f"輸血関連感染症予防: 供血動物の感染症スクリーニング。"
        )
    if category == "reproductive":
        return (
            f"{prefix}の予防は適切な繁殖管理と早期避妊去勢手術が中心。"
            f"早期避妊（雌・初発情前）: 乳腺腫瘍リスクを劇的に低下（0.5%）。"
            f"避妊（成熟前）: 子宮蓋膿症リスクゼロ。"
            f"早期去勢（雄）: 前立腺肥大症・前立腺癌（一部）・精巣腫瘍・肛門周囲腺癌リスク低下。"
            f"繁殖前のブルセラ症・ヘルペスウイルス検査による感染性生殖器疾患予防。"
            f"妊娠中毒症予防: 妊娠終末期の高エネルギー食給与。"
        )
    if category == "toxicity":
        return (
            f"{prefix}の予防は毒性物質へのアクセス防止が最重要。"
            f"有毒植物（種特異的）・農薬・殺鼠剤・洗剤の安全な保管（施錠可能な棚）、"
            f"人用医薬品の動物への不適切な使用防止、種特異的食品毒性（犬のチョコレート・ブドウ・キシリトール、猫のユリ・玉ねぎ）の飼い主教育。"
            f"環境中の化学物質への慢性的曝露低減。"
            f"中毒事故の大部分は適切な飼育者教育により予防可能。"
        )
    if category == "trauma":
        return (
            f"{prefix}の予防は飼育環境の安全管理が中心。"
            f"屋外アクセス制限（猫の屋内飼育）、リード散歩の徹底、"
            f"自宅内の鋭利物・落下物の除去、滑床対策（マット）、階段事故予防（小型犬・高齢動物）。"
            f"小型動物のケージ内安全（突起物・粗い金網の除去）、他動物との接触管理。"
            f"交通事故予防（迷子札・マイクロチップ・首輪・リード）。"
            f"自然災害（地震・火災）対策。"
        )
    if category == "autoimmune":
        return (
            f"{prefix}の確立された予防法はないが、誘因と考えられる因子の管理が重要。"
            f"過剰な薬剤投与の回避、不要なワクチン接種の回避（コアワクチンは適切に接種）、紫外線過剰曝露回避、感染症の適切な管理。"
            f"遺伝性素因の品種では繁殖管理（保因者除外）。"
            f"罹患個体の再燃予防には維持免疫抑制療法と継続的モニタリング。"
        )
    if category == "nutritional":
        return (
            f"{prefix}の予防は種特異的な栄養要求量に基づく適切な食事提供が基本。"
            f"商業用総合栄養食の利用（AAFCO基準準拠）、手作り食の場合は獣医栄養学専門医による栄養設計、"
            f"成長期・妊娠期・泌乳期の特殊要求対応。"
            f"草食動物（モルモット）のビタミンC、爬虫類のカルシウム/UV-B、猫のタウリン、フェレットの動物性タンパク質など、種特異的要求の理解。"
            f"サプリメント過剰摂取の回避（特に脂溶性ビタミン）。"
        )
    if category == "behavioral":
        return (
            f"{prefix}の予防は発達期の適切な社会化と環境管理が中心。"
            f"子犬子猫の社会化期（3-14週齢）における多様な刺激・人・動物との適切な接触。"
            f"適度な運動・知的刺激の提供（おもちゃ・パズルフィーダー・トリック訓練）。"
            f"罰主体ではなく報酬主体の躾の実施。"
            f"生活変化（引越し・新規動物導入・飼い主変更）時の段階的適応。"
            f"環境ストレス因子の特定と除去。"
            f"認知機能不全予防には知的刺激と抗酸化サプリメントを継続する。"
        )
    # generic fallback
    return (
        f"{prefix}の予防は原因病態の理解に基づく個別的アプローチが基本となる。"
        f"適切な飼育環境（温度・湿度・衛生）、種特異的な栄養管理、ストレス低減、定期的健康診断による早期発見が共通する予防策。"
        f"既知の誘因の回避と適切な医学的介入により多くの場合発症リスクを低減可能。"
    )


def gen_prognosis_ja(category: str, name_ja: str, species: str) -> str:
    sp_ja = SPECIES_JA.get(species, species)
    prefix = _disease_prefix(name_ja, sp_ja)

    if category in ("viral_infection", "bacterial_infection", "respiratory_infection", "fungal_infection"):
        return (
            f"{prefix}の予後は病原体の毒力・宿主免疫状態・治療開始時期・基礎疾患の有無により大きく異なる。"
            f"早期診断と適切な抗病原体療法・支持療法により多くの感染症は良好な予後となる。"
            f"宿主の免疫抑制・若齢・高齢・多臓器不全併発例は予後不良となりうる。"
            f"再発・慢性化・薬剤耐性発現も予後に影響する重要因子である。"
        )
    if category == "parasitic":
        return (
            f"{prefix}の予後は寄生虫種・寄生数・宿主免疫状態・治療反応性により異なる。"
            f"早期発見と適切な駆虫薬投与により多くの寄生虫症は良好な予後だが、重度感染・心血管寄生虫・血液寄生虫では治療反応が遅延する。"
            f"再感染予防のための環境管理・媒介動物制御の継続が長期予後を左右する。"
            f"免疫不全状態では治療抵抗性となるため、基礎疾患管理も並行する。"
        )
    if category == "neoplasia":
        return (
            f"{prefix}の予後は腫瘍の種類・組織学的悪性度・臨床ステージ・転移の有無・治療反応性により大きく異なる。"
            f"良性腫瘍は完全切除により治癒が期待できる。"
            f"悪性腫瘍では早期発見・早期介入が生存期間を有意に延長させる。"
            f"不完全切除・高悪性度腫瘍では再発・転移リスクが高く、定期的経過観察と追加治療検討が必要。"
            f"集学的治療（外科＋化学療法＋放射線療法）により単独治療より生存期間延長が期待できる場合がある。"
        )
    if category == "endocrine_metabolic":
        return (
            f"{prefix}の予後は適切な治療と継続的モニタリングにより多くの場合良好に管理可能。"
            f"糖尿病: 早期診断・適切なインスリン療法・食事管理により猫では20-40%が寛解達成可能。"
            f"甲状腺機能亢進症: I-131治療は治癒可能（猫95%以上）、メチマゾール内服も長期管理良好。"
            f"クッシング症候群: トリロスタン・ミトタンによる症状制御で中央生存2年以上。"
            f"アジソン病: 適切な補充療法で寿命に近い予後。"
        )
    if category == "renal_urinary":
        return (
            f"{prefix}の予後はIRISステージと進行速度により異なる。"
            f"早期CKD（ステージ2）: 適切な管理（腎臓食・降圧療法・低リン療法）で中央生存3年以上。"
            f"進行CKD（ステージ3-4）: 中央生存数週〜2年。"
            f"FLUTD/FIC: 自然寛解率約50%だが再発率も高い、ストレス管理で長期予後改善。"
            f"尿路感染: 適切な抗菌薬で治癒率高い。"
            f"急性腎障害: 早期介入で可逆性、原因除去後の腎機能回復可能。"
        )
    if category == "cardiac":
        return (
            f"{prefix}の予後は基礎心疾患の種類と心不全の進行度により異なる。"
            f"代償期: 適切な管理で長期予後良好（数年以上）。"
            f"早期心不全: 薬物療法（ACE阻害薬・利尿薬・ピモベンダン）で中央生存1-2年以上。"
            f"末期心不全: 中央生存数ヶ月。"
            f"DCM（ドーベルマン）は予後不良、HCM（猫）は症状発現後の中央生存約1.3年。"
            f"FATE（猫）: 急性期生存率約30-50%、再発予防が重要。"
        )
    if category == "respiratory_other":
        return (
            f"{prefix}の予後は基礎疾患により異なる。"
            f"短頭種気道症候群: 外科的気道形成術（軟口蓋切除・鼻孔形成）で良好予後。"
            f"気管虚脱: 内科的管理（鎮咳・抗炎症）で長期管理可能、重度では気管ステント検討。"
            f"喉頭麻痺: 片側披裂軟骨側方化術で良好予後。"
            f"猫喘息: 適切なステロイド・気管支拡張剤で長期管理可能。"
            f"アレルゲン回避と環境管理が長期予後を左右する。"
        )
    if category == "gastrointestinal":
        return (
            f"{prefix}の予後は原因病態により異なる。"
            f"急性感染性: 適切な支持療法で多くは良好予後。"
            f"IBD: 食事療法・免疫抑制療法で長期管理可能、生涯治療が必要なことが多い。"
            f"消化器腫瘍: リンパ腫は化学療法で寛解可能だが、その他の腺癌・肉腫は予後不良。"
            f"GDV（犬）: 早期手術で生存率80%以上、診断遅延で予後悪化。"
            f"GI stasis（草食動物）: 早期介入で良好予後、遅延で致死的。"
        )
    if category == "neurological":
        return (
            f"{prefix}の予後は病因により大きく異なる。"
            f"特発性てんかん: 抗痙攣薬で発作頻度低下、寿命に近い予後。"
            f"椎間板疾患: 早期手術で良好回復、深部痛覚消失例は予後不良。"
            f"脳炎: 自己免疫性は免疫抑制で寛解可能、感染性は病原体により異なる。"
            f"脳腫瘍: 外科切除可能例は予後改善、放射線療法併用で中央生存延長。"
            f"認知機能不全: 進行性だが薬物・サプリで進行遅延可能。"
        )
    if category == "ophthalmic":
        return (
            f"{prefix}の予後は病態の進行度と治療開始時期により異なる。"
            f"角膜潰瘍: 早期治療で良好予後、感染性深層潰瘍は穿孔リスクで眼科専門医紹介。"
            f"白内障: 外科的水晶体摘出術で視力回復可能。"
            f"緑内障: 急性期治療で視覚温存可能、慢性期は視覚消失多く義眼または眼球摘出。"
            f"網膜剥離: 早期復位手術で視覚温存可能。"
            f"ぶどう膜炎: 原因治療で予後決定。"
        )
    if category == "musculoskeletal":
        return (
            f"{prefix}の予後は損傷部位・重症度・治療法により異なる。"
            f"単純骨折: 適切な整復・固定で良好予後。"
            f"複雑骨折: プレート固定・専門医対応で良好予後。"
            f"OA: 進行性だが体重管理・運動療法・NSAID等で長期管理可能。"
            f"靭帯損傷: TPLO・TTA・側方制動術で良好予後（犬の十字靭帯）。"
            f"発達性疾患: 軽度は内科管理、重度は外科介入（人工股関節等）。"
        )
    if category == "dental":
        return (
            f"{prefix}の予後は早期介入により概ね良好。"
            f"歯周病: 早期スケーリング・適切な口腔ケアで進行抑制。"
            f"歯根膿瘍: 抜歯・根管治療で治癒可能。"
            f"不正咬合（草食動物）: 定期的な歯科処置（4-6週毎）で長期管理可能、咬合関係の根本的矯正は困難。"
            f"口腔腫瘍: 良性は完全切除で治癒、悪性（扁平上皮癌）は予後不良。"
            f"重度歯科疾患は全身状態（栄養・敗血症）に影響するため早期介入が重要。"
        )
    if category == "dermatological":
        return (
            f"{prefix}の予後は原因により異なる。"
            f"急性アレルギー: 原因除去で良好予後。"
            f"慢性アトピー性皮膚炎: 長期管理（環境・薬物・免疫療法）で症状制御可能、根治は困難。"
            f"細菌性膿皮症: 適切な抗菌薬で良好予後、基礎疾患管理が再発予防の鍵。"
            f"皮膚糸状菌症: 抗真菌薬で治癒可能（4-12週）。"
            f"自己免疫性皮膚疾患: 免疫抑制療法で寛解可能、長期維持療法が必要。"
        )
    if category == "hematological":
        return (
            f"{prefix}の予後は基礎病態により異なる。"
            f"IMHA: 急性期死亡率20-50%、長期生存例は良好予後。"
            f"IMTP: 適切な免疫抑制療法で多くは良好予後。"
            f"非再生性貧血: 基礎疾患（FeLV・FIV・CKD等）の予後に依存。"
            f"急性失血: 早期止血と輸血で生存可能。"
            f"凝固障害: 原因（抗凝固殺鼠剤・肝不全・DIC）により異なる。"
            f"血液腫瘍は他章参照。"
        )
    if category == "reproductive":
        return (
            f"{prefix}の予後は病態と治療時期により異なる。"
            f"子宮蓋膿症: 卵巣子宮全摘術で良好予後、早期診断が鍵。"
            f"乳腺炎: 抗菌薬・支持療法で良好予後。"
            f"難産: 早期診断（緊急帝王切開含む）で良好予後。"
            f"妊娠中毒症: 早期治療で良好予後、遅延で致死的。"
            f"前立腺癌: 予後不良、診断時に既に進行例多い。"
            f"乳腺腫瘍: 早期完全切除で良好予後、悪性度に応じて化学療法併用。"
        )
    if category == "toxicity":
        return (
            f"{prefix}の予後は毒性物質の種類・摂取量・曝露から治療開始までの時間・臓器障害の程度に大きく依存。"
            f"早期の除染処置（催吐・胃洗浄・活性炭投与）と積極的支持療法で多くの急性中毒は良好な転帰。"
            f"肝壊死・腎不全を呈する重症例では予後不良となりうる。"
            f"慢性中毒では臓器損傷が不可逆的な場合があり、長期的機能モニタリングが必要。"
            f"特異的解毒薬がある場合の早期投与が予後を大きく改善（N-アセチルシステイン・ビタミンK1・キレート剤等）。"
        )
    if category == "trauma":
        return (
            f"{prefix}の予後は外傷部位・重症度・治療時期により異なる。"
            f"単純骨折・軽度裂傷: 適切な治療で良好予後。"
            f"多発外傷: 早期安定化・段階的修復で生存可能。"
            f"重度内臓損傷: 緊急手術での生存可能、診断遅延で致死的。"
            f"脳挫傷・脊椎損傷: 損傷重症度と治療時期により神経学的予後決定。"
            f"重度ショック: 早期介入で生存可能、遅延で多臓器不全。"
        )
    if category == "autoimmune":
        return (
            f"{prefix}の予後は罹患臓器・治療反応性・再燃管理により異なる。"
            f"急性期: 適切な免疫抑制療法で症状制御可能、初期死亡率は疾患により異なる（IMHA 20-50%）。"
            f"寛解後維持期: 長期免疫抑制療法（プレドニゾロン±追加免疫抑制薬）で寛解維持可能。"
            f"再燃は治療調整で対応、複数回再燃例は治療抵抗性となる場合あり。"
            f"二次性合併症（感染・血栓症・薬剤副作用）の管理が長期予後を左右する。"
        )
    if category == "nutritional":
        return (
            f"{prefix}の多くは原因栄養素不均衡の是正により良好予後。"
            f"早期に適切な食事矯正とサプリメント補充開始で多くの臨床症状は可逆的。"
            f"急性ビタミンC欠乏（モルモット壊血病）は補給開始後24-48時間で臨床改善開始。"
            f"代謝性骨疾患（MBD）: 早期介入で進行抑制可能だが、骨格異常の完全回復は困難。"
            f"重度の慢性栄養失調による発達異常・臓器障害は不可逆的な場合あり。"
            f"飼育者教育による再発防止が長期予後の鍵。"
        )
    if category == "behavioral":
        return (
            f"{prefix}の予後は行動修正・環境管理・薬物療法の統合的アプローチにより改善可能。"
            f"分離不安: 早期介入と行動修正で多くは改善、重度例は薬物療法併用。"
            f"恐怖症: 系統的脱感作・拮抗条件付けと抗不安薬で症状制御可能。"
            f"攻撃行動: 原因分類（恐怖・縄張り・資源防衛等）に応じた個別対応で改善可能。"
            f"認知機能不全: 進行性だが薬物・サプリ・環境工夫で進行遅延・QOL改善可能。"
            f"内科疾患合併例は基礎疾患管理が前提。"
        )
    # generic
    return (
        f"{prefix}の予後は基礎病態・治療時期・併存疾患により異なる。"
        f"早期診断と適切な治療介入により多くの症例で良好な予後が期待される。"
        f"継続的なモニタリングと飼育環境管理が長期予後改善に重要である。"
        f"重症例・進行例・基礎疾患合併例では予後が悪化することがある。"
    )


def gen_pathophysiology_ja(category: str, name_ja: str, species: str) -> str:
    """Generate pathophysiology when it's templated (52% of entries have unique pathophys).

    This is only called when the existing pathophys_ja is identified as templated.
    """
    sp_ja = SPECIES_JA.get(species, species)
    prefix = _disease_prefix(name_ja, sp_ja)

    if category in ("viral_infection",):
        return (
            f"{prefix}の病態生理はウイルス侵入→宿主細胞内複製→組織傷害→免疫応答の連鎖により展開する。"
            f"病原ウイルスは特異的細胞受容体に結合し細胞内に侵入、ウイルスRNAまたはDNAを宿主細胞の機構を利用して複製・転写・翻訳する。"
            f"宿主免疫応答（先天性免疫・適応免疫）の発動と病原体毒力のバランスが病態を決定する。"
            f"急性期は局所炎症と全身性サイトカイン放出を、慢性期は臓器特異的傷害（リンパ球減少・骨髄抑制・神経傷害等）を引き起こす。"
        )
    if category == "bacterial_infection":
        return (
            f"{prefix}の病態生理は細菌侵入→定着・増殖→毒素産生・組織傷害→免疫応答の流れで展開する。"
            f"病原細菌は粘膜バリア・皮膚バリアを突破し、付着因子で標的組織に定着、増殖し外毒素・内毒素を産生する。"
            f"宿主の好中球・補体・抗体応答が病原体を制御する一方、過剰免疫応答は組織傷害（SIRS・敗血症）を引き起こす。"
            f"細菌の薬剤耐性メカニズム（β-ラクタマーゼ・効率排出ポンプ・標的部位変異）が治療効果に影響する。"
        )
    if category == "neoplasia":
        return (
            f"{prefix}の病態生理は正常細胞の悪性転換から始まる。"
            f"癌遺伝子（c-Myc, Ras等）の活性化と癌抑制遺伝子（p53, Rb等）の不活化により、細胞増殖シグナルの恒常的活性化、アポトーシス回避、血管新生誘導、浸潤・転移能の獲得が段階的に進行する。"
            f"腫瘍微小環境では免疫逃避機構が構築され、腫瘍関連マクロファージや制御性T細胞が抗腫瘍免疫を抑制する。"
            f"進行例では悪液質、傍腫瘍症候群（高Ca血症・低血糖等）、全身合併症を引き起こす。"
        )
    if category == "endocrine_metabolic":
        return (
            f"{prefix}の病態生理は内分泌腺機能異常または代謝経路障害により全身ホメオスタシスが破綻する。"
            f"糖尿病: β細胞機能不全とインスリン抵抗性により慢性高血糖、終末糖化産物形成、微小血管障害、多臓器合併症を引き起こす。"
            f"甲状腺機能亢進: T3/T4過剰により基礎代謝亢進、心拍出量増加、体重減少、二次性高血圧と腎機能低下を引き起こす。"
            f"クッシング症候群: 慢性的コルチゾール過剰により蛋白異化、免疫抑制、二次性糖尿病、感染感受性増大を引き起こす。"
        )
    if category == "renal_urinary":
        return (
            f"{prefix}の病態生理はネフロン進行性喪失または尿路機能障害により展開する。"
            f"CKD: 機能ネフロン減少→残存ネフロン過剰負荷→糸球体高血圧・蛋白尿→更なるネフロン傷害という悪循環を形成する。"
            f"二次性に高リン血症、二次性副甲状腺機能亢進症、貧血（エリスロポエチン低下）、全身性高血圧、尿毒症性中毒物質蓄積が起こる。"
            f"FLUTD/FIC: 神経内分泌系の慢性ストレス応答が膀胱壁神経炎症・透過性亢進を引き起こし、自発的疼痛・排尿異常を生じる。"
        )
    if category == "nutritional":
        return (
            f"{prefix}の病態生理は必須栄養素不足・過剰による生化学的経路障害に基づく。"
            f"カルシウム/リン不均衡では二次性副甲状腺機能亢進症により骨吸収促進・骨軟化・病的骨折が生じる。"
            f"ビタミン欠乏は各ビタミン関与酵素反応の障害により特異的臨床症候群を引き起こす（ビタミンA欠乏: 視覚障害、ビタミンB1欠乏: 神経症状）。"
            f"タンパク質-エネルギー栄養障害では異化亢進、筋萎縮、免疫機能低下、創傷治癒遅延を生じる。"
            f"栄養素過剰では肝胆道・腎の代謝負荷増大、毒性発現（脂溶性ビタミン過剰）を引き起こす。"
        )
    if category == "parasitic":
        return (
            f"{prefix}の病態生理は寄生虫種・寄生数・寄生部位により異なる。"
            f"消化管寄生虫: 粘膜傷害・栄養素吸収阻害・血管侵入による出血・腸閉塞を引き起こす。"
            f"心血管寄生虫（フィラリア）: 肺動脈閉塞・血管炎・右心後負荷増大により右心不全に進展。"
            f"血液寄生虫（バベシア等）: 赤血球内寄生で溶血、免疫介在性二次溶血、播種性血管内凝固を引き起こす。"
            f"外部寄生虫: 皮膚傷害・アレルギー反応・媒介病原体伝播を介して二次性疾患を引き起こす。"
        )
    if category == "cardiac":
        return (
            f"{prefix}の病態生理は心筋・弁・伝導系・心膜の機能/構造異常により心拍出量低下と二次的代償機構が連鎖的に展開する。"
            f"HCMでは心筋肥厚→左室流出路狭窄→左房圧上昇→肺水腫を引き起こす。"
            f"DCMでは心筋収縮力低下→心室拡張→低心拍出量→神経内分泌系活性化（RAAS・交感神経）→さらなる心室リモデリングが進行する。"
            f"弁膜疾患では逆流による前負荷増大→心室拡張→不全進行。"
            f"末期では肺水腫・腹水・心原性ショック・致死的不整脈に進展する。"
        )
    # generic
    return (
        f"{prefix}の病態生理は原因病態と進行段階により多面的に展開する。"
        f"初期の局所組織傷害・機能異常から全身的代償機構の動員、最終的な臓器機能不全への進展という共通の流れがある。"
        f"病態の進行は原因と宿主の免疫・代謝状態に依存する。"
        f"早期発見・早期治療が予後改善の鍵。"
    )


def gen_nutrition_management_ja(category: str, name_ja: str, species: str) -> str:
    sp_ja = SPECIES_JA.get(species, species)
    prefix = _disease_prefix(name_ja, sp_ja)

    if category in ("viral_infection", "bacterial_infection", "respiratory_infection", "fungal_infection"):
        return (
            f"{prefix}における栄養管理では免疫機能維持・強化と異化亢進への対応が重要。"
            f"高品質タンパク質の十分な供給で抗体産生と組織修復を支援。"
            f"発熱による代謝率上昇（10-13%/℃）に対応した適切なエネルギー量を給与。"
            f"水分摂取量増加（脱水予防）、ビタミン（A・C・E）・ミネラル（亜鉛）の十分な補給。"
            f"重症例では経腸栄養・経管栄養を早期に開始し、回復力維持を図る。"
        )
    if category == "parasitic":
        return (
            f"{prefix}における栄養管理では寄生虫による消耗と二次性栄養不良に対応する。"
            f"高品質タンパク質・カロリーの補給で削痩・低タンパク血症を改善。"
            f"鉄・ビタミンB12・葉酸の補給で寄生虫性貧血の回復を支援。"
            f"消化管寄生虫例では消化吸収機能の回復に応じた段階的食事復帰を計画。"
            f"再感染予防の観点から飲水・食事の衛生管理を徹底する。"
        )
    if category == "neoplasia":
        return (
            f"{prefix}における栄養管理では悪液質予防と治療が最重要課題。"
            f"高タンパク質・高脂肪・低炭水化物の食事構成が推奨される（腫瘍細胞は解糖系に依存するため）。"
            f"オメガ3脂肪酸（EPA/DHA）の補給は抗炎症作用と腫瘍増殖抑制に寄与。"
            f"食欲不振に対しては嗜好性高い食事の提供、少量頻回給餌、必要に応じた食欲刺激薬（カプロモレリン・ミルタザピン・酢酸メゲストロール）の使用を検討。"
            f"化学療法中は嘔吐・口内炎対応のため軟食または液状栄養を提供する。"
        )
    if category == "endocrine_metabolic":
        return (
            f"{prefix}における栄養管理は内分泌異常により異なる。"
            f"糖尿病: 低炭水化物（<12% ME, 猫）または中炭水化物・高繊維（犬）食、規則的給餌時間、肥満解消。"
            f"甲状腺機能亢進症: 高品質タンパク質と十分なエネルギー（基礎代謝亢進対応）、ヨウ素制限食オプション。"
            f"クッシング症候群: 低脂肪・高品質タンパク質食、適度な繊維で便通管理。"
            f"アジソン病: 適切なナトリウム摂取（食事性塩分制限不要）、ストレス時の追加栄養。"
        )
    if category == "renal_urinary":
        return (
            f"{prefix}における栄養管理は腎機能保護が中心。"
            f"CKD: 適度なタンパク質制限（IRIS ステージ3-4）、低リン食（<0.5% DM）、低ナトリウム、オメガ3脂肪酸補給、十分な水分摂取（ウェットフード・循環式給水器）。"
            f"市販腎臓食（Hill's k/d, Royal Canin Renal等）の利用が推奨される。"
            f"FLUTD: 尿pH管理（ストルバイト溶解にはpH 6.0未満を維持）、適切なミネラル含量、水分摂取量増加。"
            f"尿石症: 結石タイプに応じた食事（ストルバイト・シュウ酸カルシウム）。"
        )
    if category == "cardiac":
        return (
            f"{prefix}における栄養管理は心機能保護と二次的合併症予防が中心。"
            f"ナトリウム制限（軽度心不全: <100 mg/100 kcal、重度心不全: <60 mg/100 kcal）。"
            f"タウリン補給（500-1000 mg/日 経口、特に猫・グレインフリー食関連DCM）。"
            f"L-カルニチン補給（DCM疑い犬・ボクサー・ドーベルマン）。"
            f"心臓食（Hill's h/d, Royal Canin Cardiac等）の利用、悪液質予防のための適切なエネルギー・タンパク質維持。"
            f"オメガ3脂肪酸（EPA/DHA）の抗炎症・抗不整脈効果を活用。"
        )
    if category == "gastrointestinal":
        return (
            f"{prefix}における栄養管理は消化管病態により異なる。"
            f"IBD: 加水分解タンパク質食（Royal Canin Anallergenic, Hill's z/d）または新規タンパク質源食、十分な可溶性繊維、プロバイオティクス。"
            f"急性下痢: 24-48時間の絶食後、低脂肪・易消化食を段階的に再導入。"
            f"嘔吐: 制吐後に少量頻回給餌、トリプル療法（制吐薬・粘膜保護薬・PPI）併用。"
            f"草食動物GI stasis: 強制給餌（Critical Care/Recovery）、プロモティリティ療法、痛み管理。"
        )
    # generic
    return (
        f"{prefix}における栄養管理は基礎病態と全身状態の評価に基づく個別的アプローチが必要。"
        f"適切なエネルギー量（基礎代謝量×活動係数×疾患係数）、高品質タンパク質、必須微量栄養素の十分な補給を基本とする。"
        f"嗜好性向上のための食事温度・調理法工夫、少量頻回給餌、食欲刺激薬の活用、必要に応じた経腸栄養・経静脈栄養を検討する。"
        f"病態進行とともに栄養要求量が変化するため、継続的なモニタリングと調整が重要。"
    )


def gen_prognosis_detailed_ja(category: str, name_ja: str, species: str) -> str:
    """Detailed prognosis with stratification factors."""
    sp_ja = SPECIES_JA.get(species, species)
    prefix = _disease_prefix(name_ja, sp_ja)

    if category in ("viral_infection", "bacterial_infection", "respiratory_infection", "fungal_infection"):
        return (
            f"{prefix}の詳細な予後は病原体毒力・宿主免疫状態・治療反応性により層別化される。"
            f"予後良好因子: 早期診断、適切な抗病原体療法、宿主免疫機能維持、基礎疾患なし、若中年成獣。"
            f"予後不良因子: 重度免疫抑制、多臓器不全併発、敗血症進展、薬剤耐性病原体、若齢・高齢個体、診断遅延、慢性化・反復感染。"
            f"治療開始後72時間以内の臨床改善（解熱・食欲改善）が良好予後の指標となる。"
            f"再発・慢性化リスク評価のため治療後のフォローアップ検査（PCR・血清学・培養）を計画する。"
        )
    if category == "parasitic":
        return (
            f"{prefix}の詳細な予後は寄生虫負荷量・寄生臓器・宿主状態により層別化される。"
            f"予後良好因子: 軽度〜中等度寄生、駆虫薬感受性、宿主免疫状態良好、早期介入。"
            f"予後不良因子: 重度寄生、薬剤耐性、心血管/中枢神経寄生、宿主免疫不全、慢性栄養失調合併。"
            f"駆虫後の経過モニタリング（糞便検査・血液検査）で治療成功と再感染を評価する。"
        )
    if category == "neoplasia":
        return (
            f"{prefix}の詳細な予後は組織学的グレード・臨床ステージ（TNM分類）・マージン評価・有糸分裂指数により層別化される。"
            f"完全切除例（クリーンマージン）では再発率が大幅に低下。"
            f"リンパ腫はCHOP系プロトコルで犬の中央生存期間10-14ヶ月、猫はCOP療法で中央生存4-9ヶ月。"
            f"血管肉腫は予後不良で脾臓摘出後の中央生存1-3ヶ月、化学療法追加で5-7ヶ月。"
            f"肥満細胞腫はPatnaikグレード/Kiupelグレードと完全切除の有無で予後決定。"
            f"骨肉腫: 截肢＋カルボプラチンで中央生存約1年。"
        )
    if category == "endocrine_metabolic":
        return (
            f"{prefix}の詳細な予後は内分泌病態・治療方針・治療反応性により異なる。"
            f"糖尿病（猫）: 早期診断＋低炭水化物食＋グラルギン/PZIで寛解率20-40%（中央寛解期間 約114日）。"
            f"糖尿病（犬）: 寛解は稀、適切なインスリン管理で中央生存2年以上。"
            f"甲状腺機能亢進症（猫）: I-131治療で治癒率95%以上・中央生存4年以上、メチマゾール内服で5年生存率約70%。"
            f"クッシング症候群: トリロスタンで中央生存2-2.5年。"
            f"アジソン病: 適切な補充療法で寿命に近い予後。"
        )
    if category == "renal_urinary":
        return (
            f"{prefix}の詳細な予後はIRIS ステージにより層別化される。"
            f"ステージ1 (Cre <1.4): 早期介入で正常寿命に近い予後。"
            f"ステージ2 (Cre 1.4-2.0): 中央生存1100日以上。"
            f"ステージ3 (Cre 2.1-5.0): 中央生存680日。"
            f"ステージ4 (Cre >5.0): 中央生存35-110日。"
            f"予後悪化因子: 蛋白尿（UPC>0.4）、高リン血症、高血圧、貧血、若齢発症。"
            f"FLUTD/FIC: 自然寛解率50%、再発率50-60%、適切なストレス管理で再発率低下。"
        )
    # generic
    return (
        f"{prefix}の詳細な予後は基礎病態・臨床ステージ・併存疾患・治療反応性により層別化される。"
        f"予後良好因子: 早期診断、適切な治療介入、基礎疾患なし、若中年成獣、良好な全身状態。"
        f"予後不良因子: 診断遅延、進行例、多臓器障害、併存疾患、若齢・高齢個体、治療反応不良。"
        f"治療開始後の臨床的・検査値改善が予後を予測する重要な指標となる。"
    )


def gen_rehabilitation_protocol_ja(category: str, name_ja: str, species: str) -> str:
    sp_ja = SPECIES_JA.get(species, species)
    prefix = _disease_prefix(name_ja, sp_ja)

    if category in ("viral_infection", "bacterial_infection", "respiratory_infection", "fungal_infection"):
        return (
            f"{prefix}回復期のリハビリテーションは段階的活動量増加と体力回復を目標とする。"
            f"急性期の安静後、低強度短時間散歩から開始し臨床症状改善に応じて漸増する。"
            f"呼吸器系感染回復期では換気機能改善のための呼吸理学療法・体位ドレナージを実施。"
            f"高齢動物・基礎疾患合併例ではフレイル予防のため積極的栄養・運動介入を行う。"
            f"完全治癒確認まで他個体との接触を制限し、再感染予防の環境管理を継続する。"
        )
    if category == "neoplasia":
        return (
            f"{prefix}における患者のリハビリテーションは手術後の機能回復と生活の質向上を目的とする。"
            f"外科切除後は疼痛管理を最優先とし、段階的活動量増加を計画。"
            f"四肢腫瘍の截肢後は残存肢への負荷分散のためバランストレーニングと筋力強化を実施。"
            f"化学療法中は全身状態に配慮した低強度運動プログラムを維持し、筋萎縮と体力低下を最小限に抑える。"
            f"リンパ浮腫管理にはマッサージと圧迫療法を検討。"
            f"末期緩和ケアでは活動制限ではなくQOL維持を目的とした柔軟な対応が必要。"
        )
    if category == "musculoskeletal":
        return (
            f"{prefix}のリハビリテーションは段階的負荷増加と機能回復が中心。"
            f"術後早期: 受動的関節可動域訓練、軽度マッサージ、コールド/ホットセラピー。"
            f"中期: 等長性筋収縮訓練、バランス訓練（バランスボード・トロッターボード）、水中トレッドミル（浮力・抵抗活用）。"
            f"後期: 機能的活動訓練、軽度ジャンプ・段差訓練、漸進的耐久性訓練。"
            f"OA管理: 体重管理、低衝撃運動（散歩・水泳）、関節サプリメント、必要に応じた電気刺激療法。"
        )
    if category == "neurological":
        return (
            f"{prefix}のリハビリテーションは神経学的機能回復と二次的合併症予防が中心。"
            f"急性期: 圧迫性褥瘡予防（体位変換 q4h）、関節拘縮予防（受動的可動域訓練）、膀胱・直腸管理。"
            f"亜急性期: 受動的→補助的→自動運動への段階的移行、バランス訓練、固有感覚刺激。"
            f"慢性期: 機能的活動訓練、補助具利用（カートなど）。"
            f"認知機能不全症候群では知的刺激の継続提供、社会的相互作用維持、ルーチン化された日常生活を支援する。"
        )
    if category == "cardiac":
        return (
            f"{prefix}のリハビリテーションは心機能に応じた段階的運動と二次性筋萎縮予防が中心。"
            f"代償期: 中等度有酸素運動（毎日20-30分の散歩）、適度な筋力訓練。"
            f"早期心不全: 軽度活動（短時間散歩を頻回）、過剰な努力を回避。"
            f"進行心不全: 室内活動主体、安静と最小限活動の組み合わせ。"
            f"いずれの段階でも体重管理・栄養管理を継続し、心臓食を併用する。"
            f"運動誘発症状（咳・失神・呼吸困難）の早期認識と評価が安全な運動プログラム継続に必須。"
        )
    if category == "endocrine_metabolic":
        return (
            f"{prefix}のリハビリテーションは内分泌バランス回復と二次性合併症予防が中心。"
            f"糖尿病管理: 定期運動（毎日同時間・同量）による血糖変動安定化、過剰運動による低血糖回避。"
            f"クッシング症候群: 筋萎縮回復のための漸進的筋力訓練、皮膚バリア機能回復のためのスキンケア。"
            f"甲状腺機能亢進症（猫）: 治療開始後の体重管理（過体重への注意）、適度な活動レベル維持。"
            f"アジソン病: ストレス時の追加グルココルチコイド対応を含む生活管理。"
        )
    if category == "renal_urinary":
        return (
            f"{prefix}のリハビリテーションは腎機能保護と全身状態維持が中心。"
            f"適度な活動レベル維持（過剰運動による脱水・心負荷増大を回避）。"
            f"環境エンリッチメント（多頭飼育環境の改善・隠れ場所・上下運動）でストレス低減（特にFIC/FLUTD）。"
            f"水分摂取促進: 複数の水飲み場所、循環式給水器、ウェットフード活用。"
            f"高齢動物では筋量維持のための漸進的筋力訓練、関節サポートを併用する。"
        )
    if category == "respiratory_other":
        return (
            f"{prefix}のリハビリテーションは呼吸機能改善と運動耐性向上が中心。"
            f"喘息（猫）: ストレス低減環境、適度な活動レベル維持、急性発作時の安静と緊急対応訓練。"
            f"短頭種気道症候群: 適正体重維持、暑熱回避、ハーネス使用、術後の段階的活動再開。"
            f"気管虚脱: 興奮制御、リード使用、咳発作時の落ち着き対応訓練。"
            f"いずれも環境因子（タバコの煙・粉塵）の管理を継続。"
        )
    if category == "gastrointestinal":
        return (
            f"{prefix}のリハビリテーションは消化機能回復と栄養状態改善が中心。"
            f"急性期: 安静と適切な水分・栄養補給。"
            f"回復期: 段階的食事復帰（易消化食→通常食）、適度な活動再開。"
            f"慢性疾患管理: 規則的給餌時間、適切な食事選択（IBD: 加水分解食、膵炎: 低脂肪食）、ストレス管理。"
            f"草食動物では繊維摂取確保とプロモティリティ維持のための環境調整を継続する。"
        )
    # generic
    return (
        f"{prefix}におけるリハビリテーションは病態に応じた段階的機能回復と二次合併症予防が中心。"
        f"急性期は安静と適切な支持療法、亜急性期は機能評価に基づく段階的活動再開、慢性期は維持リハビリテーションを実施。"
        f"飼育環境改善（運動環境・栄養管理・ストレス管理）と継続的モニタリングにより長期的QOL維持を図る。"
        f"運動療法・物理療法・補助具利用・薬物療法を統合的に適用する。"
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def lookup_curated(species: str, name_ja: str, name_en: str) -> Optional[dict]:
    """Look up curated content for this disease. Returns dict of field -> text, or None."""
    name = (name_ja or "") + " " + (name_en or "")
    for (sp, pattern), fields in CURATED.items():
        if sp != species:
            continue
        if pattern in name:
            return dict(fields)
    return None


def generate_clinical_fields(
    species: str,
    name_ja: str,
    name_en: str,
    tagged_category: str,
    fields_to_generate: list[str],
) -> dict[str, str]:
    """Generate disease-specific content for the requested clinical fields.

    Returns a dict {field_name: new_text}. Only includes fields successfully generated.
    """
    curated = lookup_curated(species, name_ja, name_en) or {}
    category = resolve_true_category(name_ja, name_en, tagged_category)

    GENERATORS = {
        "causes_ja": gen_causes_ja,
        "transmission_ja": gen_transmission_ja,
        "clinical_signs_ja": gen_clinical_signs_ja,
        "differential_diagnosis_ja": gen_differential_diagnosis_ja,
        "prevention_ja": gen_prevention_ja,
        "prognosis_ja": gen_prognosis_ja,
        "pathophysiology_ja": gen_pathophysiology_ja,
        "nutrition_management_ja": gen_nutrition_management_ja,
        "prognosis_detailed_ja": gen_prognosis_detailed_ja,
        "rehabilitation_protocol_ja": gen_rehabilitation_protocol_ja,
    }

    result: dict[str, str] = {}
    for field in fields_to_generate:
        # Curated content takes priority
        if field in curated:
            result[field] = curated[field]
            continue
        gen = GENERATORS.get(field)
        if gen is None:
            continue
        result[field] = gen(category, name_ja, species)
    return result
