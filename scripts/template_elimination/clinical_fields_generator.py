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
            r"カリシ(?!ン)|ヘルペスウイルス|ヘルペス|コロナウイルス|コロナ|インフルエンザ|"
            r"アデノウイルス|ロタウイルス|狂犬病|レオウイルス|パピローマウイルス|パピローマ|"
            r"PBFD|BFDV|サーコウイルス|ボルナ|ニューカッスル|マレック|鳥痘|オウム嘴羽病|"
            r"伝染性気管支炎|伝染性ファブリキウス嚢病|伝染性喉頭気管炎|"
            r"伝染性腹膜炎|伝染性肝炎|感染性肝炎|infectious hepatitis|"
            r"伝染性貧血|流産ウイルス|脳脊髄炎ウイルス|"
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
            r"Salmonella|レプトスピラ|Leptospira|エールリッヒア|エールリヒア|エーリキア|エーリヒア|"
            r"Ehrlichia|アナプラズマ|"
            r"Anaplasma|ライム病|Borrelia|ボレリア|破傷風|Tetanus|botulism|ボツリヌス|"
            r"野兎病|Tularemia|ブルセラ|Brucella|腺疫|Strangles|トレポネーマ|Treponema|"
            r"スピロヘータ|Spirochete|リステリア|Listeria|エルシニア|Yersinia|"
            r"バルトネラ|Bartonella|ヘモバルトネラ|ヘモプラズマ|hemoplasma|"
            r"猫ひっかき病|cat scratch|肺炎球菌|髄膜炎菌|淋菌|破傷風|"
            r"ノカルジア|Nocardia|紅斑熱|spotted fever|"
            r"豚丹毒|Erysipelothrix|Q熱|Coxiella|リケッチア|Rickettsia|"
            # Bacterial hoof/foot infections (anaerobic, Fusobacterium,
            # Dichelobacter). Must precede the musculoskeletal "蹄/hoof"
            # catch-all so e.g. Thrush is not given a fracture etiology.
            r"蹄叉腐爛|thrush|蹄膿瘍|hoof abscess|蹄底膿瘍|subsolar abscess|"
            r"蹄腐敗|foot rot|蹄冠瘻|quittor"
        ),
        "bacterial_infection",
    ),
    # Respiratory infections (specific subset of bacterial/viral with respiratory focus)
    (
        re.compile(
            r"スナッフル|kennel cough|ケンネルコフ|気管支敗血症|気管支炎|"
            r"肺炎|pneumonia|ニューモニア|"
            r"上気道感染|URI|気道感染症|鼻気管炎|"
            r"鼻炎|rhinitis|副鼻腔炎|sinusitis|"
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
            r"原虫|protozoa|protozoan|鞭毛虫|flagellate|アメーバ|amoeb|ameb|"
            r"微胞子虫|microspor|住肉胞子虫|Sarcocystis|"
            r"クリプトスポリジウム|Cryptosporidium|住血吸虫|Schistosoma|"
            r"バベシア|Babesia|トリパノソーマ|Trypanosoma|リーシュマニア|Leishmania|"
            r"ダニ|mite|tick|ツメダニ|ヒゼンダニ|アカルス|Demodex|ノミ|flea|"
            r"アタマジラミ|シラミ|louse|ノミ症|ハジラミ|ウマバエ|"
            r"線虫|nematod|条虫|tapeworm|吸虫|fluke|蟯虫|pinworm|回虫|"
            r"ascarid|鞭虫|whipworm|鉤虫|hookworm|肝吸虫|"
            # Worm diseases with organ-based names (must be matched here so they
            # are not mis-resolved to the organ system: gapeworm is respiratory,
            # eyeworm is ophthalmic — both are PARASITIC). NB: never a bare
            # "worm" token because ringworm is a dermatophyte (fungal).
            r"眼虫|eyeworm|eye worm|Thelazia|ガペworm|gapeworm|gape worm|Syngamus|"
            r"lungworm|肺虫|kidney worm|腎虫|stomach worm|gizzard worm|"
            r"白点病|\bich\b|白点虫|イクチオフチリウス|"
            r"イカリ虫|Lernaea|ウオジラミ|Argulus|住血吸虫|"
            r"羽ダニ|気嚢ダニ"
        ),
        "parasitic",
    ),
    # Goiter (thyroid hyperplasia) — must precede neoplasia because the
    # substring "腺腫" in "甲状腺腫" would otherwise match the adenoma pattern.
    # In exotics (esp. budgerigars) goiter is iodine-deficiency driven.
    (
        re.compile(r"甲状腺腫(?!瘍)|goiter|goitre|ヨウ素欠乏|iodine deficienc"),
        "nutritional",
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
            r"毛芽腫|trichoblastoma|毛包腫|trichoepithelioma|"
            r"セミノーマ|seminoma|精上皮腫|基底細胞腫|basal cell tumor|"
            r"形質細胞腫|plasmacytoma|髄膜腫|meningioma|神経鞘腫|schwannoma|"
            r"線維肉腫|fibrosarcoma|線維腫|fibroma|骨腫|osteoma|軟骨肉腫|chondrosarcoma|"
            r"乳頭腫|papilloma(?!virus|ウイルス)|胸腺腫|thymoma|中皮腫|mesothelioma|"
            r"組織球腫|histiocytoma|奇形腫|teratoma|髄芽腫|"
            r"脊索腫|chordoma"
        ),
        "neoplasia",
    ),
    # Endocrine / metabolic
    (
        re.compile(
            r"糖尿病|diabetes|低血糖|hypoglycemia|高血糖|hyperglycemia|"
            r"甲状腺機能亢進|hyperthyroid|甲状腺機能低下|hypothyroid|"
            r"甲状腺クリーゼ|甲状腺中毒症|thyroid storm|thyroid crisis|thyrotoxic|"
            r"クッシング|Cushing|副腎皮質機能亢進|副腎皮質機能低下|副腎|adrenal|"
            r"アジソン|Addison|hyperadrenocorticism|hypoadrenocorticism|"
            r"副甲状腺|parathyroid|栄養性二次性|代謝性|metabolic|"
            r"インスリン|insulin|糖原病|glycogen storage|脂肪肝|肝リピドーシス|"
            r"hepatic lipidosis|ケトーシス|ketosis|アシドーシス|acidosis|"
            r"アルカローシス|電解質異常|electrolyte|"
            # Specific electrolyte derangements (were mis-tagged cardiac/renal).
            # Require 血症 in JA so HYPP (高カリウム血性周期性四肢麻痺) keeps its
            # neurological classification rather than flipping to metabolic.
            r"高リン血症|hyperphosphat|低リン血症|hypophosphat|"
            r"高カリウム血症|hyperkal|低カリウム血症|hypokal|"
            r"高ナトリウム血症|hypernatr|低ナトリウム血症|hyponatr|"
            r"高マグネシウム血症|hypermagnes|低マグネシウム血症|hypomagnes"
        ),
        "endocrine_metabolic",
    ),
    # Renal / urinary
    (
        re.compile(
            r"腎臓|腎不全|腎症|腎炎|腎結石|腎疾患|腎障害|腎石灰化|nephrocalcin|"
            r"腎アミロイド|renal amyloid|尿道|urethra|尿管|ureter|(?<!ad)renal|kidney|nephritis|nephropathy|"
            r"CKD|AKI|尿石|尿路結石|urolith|膀胱炎|\bcystitis|"
            r"下部尿路|lower urinary|FLUTD|FIC|間質性膀胱炎|"
            r"尿閉|urinary obstruction|蛋白尿|proteinuria|"
            r"糸球体|glomerular|腎盂腎炎|pyelonephritis|"
            r"前立腺|prostate|前立腺炎|prostatitis|"
            r"水腎症|hydronephrosis|腎瘤|ureter|"
            r"尿腹症|uroperitoneum|膀胱破裂|bladder rupture|尿膜管|urachal"
        ),
        "renal_urinary",
    ),
    # Cardiac
    (
        re.compile(
            r"心臓|心筋|心房|心室|弁膜|心不全|cardiac|\bcardio|heart|"
            r"DCM|HCM|拡張型心筋症|肥大型心筋症|"
            r"僧帽弁|mitral|三尖弁|tricuspid|心房中隔|心室中隔|"
            r"動脈管開存|PDA|不整脈|arrhythmia|"
            r"心嚢液貯留|心嚢水|pericardial|心膜炎|pericarditis|心内膜炎|endocarditis|心タンポナーデ|"
            r"房室ブロック|atrioventricular block|洞不全|sick sinus|"
            r"全身性高血圧|動脈性高血圧|hypertension|"
            r"血栓塞栓症|thromboembolism|FATE|サドル血栓|"
            # Vascular / aortic disease — previously fell through to a
            # musculoskeletal "fracture" etiology or no category at all.
            r"心疾患|心血管疾患|動脈硬化|アテローム|atheroscler|arterioscler|"
            # NB: 動脈瘤(?!様) excludes "動脈瘤様" (aneurysm-*like*), which is a
            # descriptor for aneurysmal bone cysts — a bone lesion, not vascular.
            r"大動脈|aortic|動脈瘤(?!様)|aneurysm"
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
            r"幽門狭窄|アクアラジア|食道|esophag|"
            r"胎便停滞|胎便|meconium|直腸脱|rectal prolapse|脱肛|"
            r"消化管運動|gastrointestinal motility|イレウス|ileus|"
            r"消化管うっ滞|enteritis|colitis|gastroenteritis|胃腸炎"
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
            r"重症筋無力症|筋無力症|myasthenia|myasthenic|"
            r"水頭症|hydrocephalus|髄膜|meningitis|脳炎|encephalitis|"
            # Neurodegenerative syndromes previously mis-tagged musculoskeletal.
            r"ふらつき|wobbly hedgehog|WHS|運動失調|ataxia|脱髄|demyelin"
        ),
        "neurological",
    ),
    # Ophthalmic
    (
        re.compile(
            r"眼(?!球突出)|角膜|cornea|緑内障|glaucoma|白内障|cataract|"
            r"網膜|retina|ぶどう膜炎|uveitis|結膜炎|conjunctivitis|水晶体|lens|"
            r"涙嚢|鼻涙管|涙管|涙小管|nasolacrimal|チェリーアイ|cherry eye|乾性角結膜炎|KCS|"
            r"睫毛|eyelash|distichiasis|ectopic cilia|眼瞼|eyelid|entropion|"
            r"内反症|外反症|ectropion|prolapsed gland|"
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
            r"骨髄炎|osteomyelitis|筋ジストロフィー|筋炎|myositis|腱炎|tendonitis|tendinitis|滑液包炎|bursitis|"
            r"代謝性骨疾患|MBD|metabolic bone|"
            # NB: rickets (くる病) is a vitamin-D/Ca/P *nutritional* disease — it
            # is intentionally NOT matched here so the nutritional pattern (and
            # nutritional etiology) wins. Likewise bacterial hoof infections
            # (thrush/hoof abscess) are matched by the bacterial pattern above.
            r"舟状骨|navicular|蹄|hoof|laminitis|蹄葉炎|蹄壁|"
            r"挫跖|sole bruise|釘傷|nail bind|nail prick|"
            r"骨粗鬆症|osteoporosis"
        ),
        "musculoskeletal",
    ),
    # Dental
    (
        re.compile(
            r"歯(?!科)|歯肉|歯周|歯石|歯髄|齲歯|dental|tooth|periodontal|"
            r"歯科疾患|不正咬合|malocclusion|過長歯|"
            r"歯根膿瘍|tooth root abscess|歯瘻|口内炎|stomatitis|口唇炎|cheilitis|"
            # Slobbers/ptyalism in rodents & rabbits is a dental sign; buccal
            # spurs are tooth points. NB: 頬棘 only (臼歯棘 already matches via
            # 歯) so 棘下筋/棘突起 (muscle/spine) are never mis-tagged dental.
            r"流涎|スロバーズ|slobber|ptyalism|頬棘|buccal spur|cheek teeth point"
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
            r"発情|estrus|estrous|"
            # Egg-laying / oviductal disorders (common avian & reptile repro
            # emergencies) — were scattered across respiratory/endocrine/bacterial
            # templates. NB: specific terms (卵巣嚢胞, not bare 卵巣) so ovarian
            # *tumours* (卵巣腺癌/奇形腫/顆粒膜細胞腫) keep their neoplasia class.
            r"卵詰|卵塞|卵秘|egg bind|egg-bind|"
            r"卵胞停滞|卵停滞|卵停|follicular stasis|egg stasis|egg retention|卵閉塞|"
            r"卵管炎|卵管脱|卵管閉塞|卵管|salping|oviduct|"
            r"卵巣嚢胞|嚢胞性卵巣|多嚢胞性卵巣|ovarian cyst|polycystic ovar|"
            r"卵黄性腹膜炎|卵黄体腔炎|卵黄性体腔炎|yolk perito|yolk coelom|卵黄塞栓|"
            # NB: 慢性/過剰産卵 only — bare 産卵 would mis-claim "産卵鳥" (a
            # laying-hen descriptor) in calcium-deficiency, which is nutritional.
            r"慢性産卵|過剰産卵|chronic egg lay|excessive egg lay|"
            r"卵巣遺残|ovarian remnant|繁殖障害"
        ),
        "reproductive",
    ),
    # Toxicity
    (
        re.compile(
            r"中毒|toxicity|toxicosis|poisoning|"
            r"咬傷毒|毒蛇|マムシ|ハブ|envenom|snakebite|snake bite|venom|"
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
    # Behavioral. NB: precise tokens (不安症 not 不安, 攻撃行動 not 攻撃) so spinal
    # "不安定症" and trauma "攻撃損傷" are never mis-tagged behavioral. This is the
    # last pattern, so it only claims diseases no organ-system pattern matched.
    (
        re.compile(
            r"行動学|behavioral|behavior|anxiety|不安症|不安障害|"
            r"行動障害|行動性|ストレス関連疾患|"
            r"強迫|compulsive|分離不安|separation|"
            r"恐怖|phobia|aggression|攻撃行動|"
            # Stereotypies / self-directed / husbandry-behaviour disorders
            r"毛引き|barbering|常同行動|stereotyp|過剰グルーミング|overgroom|over-groom|over groom|"
            r"毛噛み|毛咬み|毛むしり|fur chew|fur-chew|fur pluck|"
            r"ケージ噛み|バー噛み|cage bit|cage chew|bar chew|bar-bit|"
            r"自己塗布|self-anoint|self anoint|"
            r"羽毛破壊|羽咬|羽毛むしり|feather destruct|feather pick|feather-pick|feather pluck|"
            r"過度発声|過剰発声|夜間発声|scream|excessive vocal|night vocal|vocalization issue|barking|"
            r"マーキング|尿スプレー|尿マーキング|urine spray|urine mark|territorial marking|spraying behavior|"
            r"行動性拒食|behavioral anorexia|"
            r"共食い|子食い|子拒絶|食殺|cannibal|joey reject|infanticide|"
            r"資源防衛|resource guard|"
            r"過活動症|hyperkinesis|ADHD|"
            r"異食症|\bpica\b|"
            r"つがい攻撃|縄張り攻撃|同居個体攻撃|ケージメイト攻撃|mate aggression|territorial aggression|"
            r"ストレス症候群|ストレス関連行動|ストレス性自己|社会的ストレス|ストレス誘発性自己|"
            r"うつ・ストレス|psychogenic|心因性|オウム目ストレス|環境ストレス症候群|psittacine stress"
        ),
        "behavioral",
    ),
    # ---------------------------------------------------------------------
    # Low-priority ORGAN-SYSTEM fallbacks. These run LAST so every specific
    # pattern above wins first (e.g. "Cardiovascular Neoplasia" -> neoplasia,
    # not cardiac). They exist to catch synthetic composite names such as
    # "Gastrointestinal Inflammatory Disease" / "泌尿生殖器炎症性疾患" that no
    # specific rule matches, so the dangerous "toxic substances" template is
    # never left on an inflammatory disease.
    (re.compile(r"心血管|cardiovascular"), "cardiac"),
    (re.compile(r"消化管|消化器|gastrointestinal"), "gastrointestinal"),
    (re.compile(r"筋骨格|musculoskeletal"), "musculoskeletal"),
    (re.compile(r"泌尿生殖器|泌尿|urogenital|urinary tract"), "renal_urinary"),
    (re.compile(r"生殖器|reproductive"), "reproductive"),
    (re.compile(r"呼吸器|鼻汁|nasal discharge|respiratory"), "respiratory_other"),
    (re.compile(r"神経系|neurological"), "neurological"),
    (re.compile(r"内分泌|代謝性|endocrine|metabolic"), "endocrine_metabolic"),
    (re.compile(r"眼科|ophthalmolog"), "ophthalmic"),
    (re.compile(r"血液系|hematolog|haematolog"), "hematological"),
    (re.compile(r"尿やけ|尿焼け|ハッチバーン|urine scald|hutch burn"), "dermatological"),
    (re.compile(r"全身性炎症反応|systemic inflammatory"), "generic"),
    (re.compile(r"皮膚|dermatolog|integument"), "dermatological"),
    (re.compile(r"口腔|口内|oral ulcer"), "dental"),
]


# Negated phrases whose embedded category keyword would otherwise produce a
# false-positive match (e.g. "非寄生虫性脱毛症" must NOT resolve to parasitic,
# "猫角膜炎（非ヘルペス性）" must NOT resolve to viral). We neutralise the
# negation by blanking the negated token before pattern matching.
_NEGATION_TOKENS: tuple[str, ...] = (
    "非寄生虫性",
    "非寄生虫",
    "非感染性",
    "非感染",
    "非腫瘍性",
    "非腫瘍",
    "非ヘルペス性",
    "非ヘルペス",
    "非炎症性",
    "非ウイルス性",
    "non-parasitic",
    "non-infectious",
    "non-neoplastic",
    "non-herpetic",
    "非pdd",
    "non-pdd",
)


_NEGATION_RE = re.compile("|".join(re.escape(tok) for tok in _NEGATION_TOKENS), re.IGNORECASE)


def _neutralise_negations(name: str) -> str:
    return _NEGATION_RE.sub("—", name)


def resolve_category_from_name(name_ja: str, name_en: str) -> Optional[str]:
    """Resolve category from the disease *name* only, or None if no pattern matches.

    Used for the disease description (the most visible headline field), where
    trusting a possibly-wrong stored ``category`` tag would yield embarrassing
    mis-categorisations such as "cheek pouch impaction is a bacterial infection".
    """
    name = _neutralise_negations(f"{name_ja or ''} {name_en or ''}")
    for pattern, cat in NAME_CATEGORY_PATTERNS:
        if pattern.search(name):
            return cat
    return None


def resolve_true_category(name_ja: str, name_en: str, tagged_category: str) -> str:
    """Resolve the canonical category from disease name (priority) + tagged category (fallback).

    Returns one of: viral_infection, bacterial_infection, respiratory_infection,
    fungal_infection, parasitic, neoplasia, endocrine_metabolic, renal_urinary,
    cardiac, respiratory_other, gastrointestinal, neurological, ophthalmic,
    musculoskeletal, dental, dermatological, hematological, reproductive,
    toxicity, trauma, autoimmune, nutritional, genetic_congenital, degenerative,
    behavioral, generic.
    """
    name = _neutralise_negations(f"{name_ja or ''} {name_en or ''}")
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


# Species-appropriate examples of common toxic exposures. The generic toxicity
# template previously listed dog/cat toxins (chocolate, lily) for *every*
# species — embarrassing and clinically misleading when shown for a horse,
# bird or reptile. These fragments keep the toxin examples relevant to the
# animal actually being treated.
TOXIN_SOURCES_JA: dict[str, str] = {
    "dog": "チョコレート（テオブロミン）・キシリトール・ブドウ/レーズン・タマネギ/ニンニク・抗凝固性殺鼠剤・人用NSAID/アセトアミノフェン・不凍液（エチレングリコール）",
    "cat": "ユリ科植物（腎毒性）・アセトアミノフェン・犬用ペルメトリン製剤・タマネギ/ニンニク・不凍液・抗凝固性殺鼠剤",
    "horse": "有毒植物（イチイ・キョウチクトウ・カエデ赤葉・ワラビ・キバナハウチワマメ）・カビ毒（アフラトキシン・フモニシン）・モネンシン（飼料添加物）・鉛・有機リン系駆虫薬の過量",
    "rabbit": "経口β-ラクタム/リンコサミド系抗菌薬（致死的腸内菌叢崩壊）・有毒観葉植物・殺鼠剤・農薬・鉛",
    "guinea_pig": "経口ペニシリン系抗菌薬（Clostridium腸毒血症を誘発）・有毒植物・殺鼠剤・フィプロニル",
    "chinchilla": "経口β-ラクタム系抗菌薬・フィプロニル（致死的）・有毒植物・殺鼠剤",
    "degu": "経口β-ラクタム系抗菌薬・糖分過剰（糖尿病誘発）・有毒植物・殺鼠剤",
    "hamster": "経口β-ラクタム系抗菌薬・有毒植物・殺鼠剤・家庭用化学物質",
    "ferret": "イブプロフェン/人用NSAID・抗凝固性殺鼠剤・タマネギ・カフェイン・人用薬剤",
    "hedgehog": "有毒植物・殺虫剤・家庭用化学物質・重金属",
    "sugar_glider": "有毒植物・殺虫剤・カルシウム拮抗性食餌（高リン）・家庭用化学物質",
    "bird": "重金属（鉛・亜鉛）・PTFE（フッ素樹脂）加熱煙・アボカド・タマネギ・有毒観葉植物・殺虫剤・カビ毒",
    "parakeet": "重金属（鉛・亜鉛）・PTFE加熱煙・アボカド・有毒観葉植物・殺虫剤・カビ毒",
    "parrot": "重金属（鉛・亜鉛）・PTFE加熱煙・アボカド・有毒観葉植物・殺虫剤・カビ毒",
    "reptile": "殺虫剤（有機リン・ピレスロイド）・不適切な消毒剤・重金属・イベルメクチン（一部種で致死）・有毒植物",
    "tortoise": "殺虫剤・不適切な消毒剤・重金属・有毒植物・シュウ酸過剰植物",
    "snake": "殺虫剤・不適切な消毒剤（ヒノキ/杉チップの揮発成分）・重金属・イベルメクチン",
    "lizard": "殺虫剤・不適切な消毒剤・重金属・イベルメクチン・有毒植物",
    "amphibian": "水質毒性（アンモニア・亜硝酸・残留塩素/クロラミン）・重金属・農薬流入・不適切なpH",
    "fish": "水質毒性（アンモニア・亜硝酸・残留塩素・重金属）・農薬流入・過剰投薬（銅・ホルマリン）",
    "exotic_other": "有毒植物・殺虫剤・家庭用化学物質・重金属・不適切な飼育用品からの化学物質溶出",
}


def _toxin_sources(species: str) -> str:
    return TOXIN_SOURCES_JA.get(
        species,
        "有毒植物・殺鼠剤/農薬・家庭用化学物質・重金属・医薬品の過量投与",
    )


# English counterpart of TOXIN_SOURCES_JA, used by ``gen_causes_en``.
TOXIN_SOURCES_EN: dict[str, str] = {
    "dog": "chocolate (theobromine), xylitol, grapes/raisins, onion/garlic, anticoagulant rodenticides, human NSAIDs/acetaminophen, and antifreeze (ethylene glycol)",
    "cat": "lilies (nephrotoxic), acetaminophen, canine permethrin spot-ons, onion/garlic, antifreeze, and anticoagulant rodenticides",
    "horse": "toxic plants (yew, oleander, red maple leaves, bracken fern, lupins), mycotoxins (aflatoxin, fumonisin), monensin (feed additive), lead, and organophosphate anthelmintic overdose",
    "rabbit": "oral beta-lactam/lincosamide antibiotics (fatal gut dysbiosis), toxic houseplants, rodenticides, pesticides, and lead",
    "guinea_pig": "oral penicillins (Clostridium enterotoxaemia), toxic plants, rodenticides, and fipronil",
    "chinchilla": "oral beta-lactam antibiotics, fipronil (fatal), toxic plants, and rodenticides",
    "degu": "oral beta-lactam antibiotics, excess dietary sugar (diabetogenic), toxic plants, and rodenticides",
    "hamster": "oral beta-lactam antibiotics, toxic plants, rodenticides, and household chemicals",
    "ferret": "ibuprofen/human NSAIDs, anticoagulant rodenticides, onion, caffeine, and human medications",
    "hedgehog": "toxic plants, insecticides, household chemicals, and heavy metals",
    "sugar_glider": "toxic plants, insecticides, high-phosphorus calcium-binding diets, and household chemicals",
    "bird": "heavy metals (lead, zinc), heated PTFE (non-stick) fumes, avocado, onion, toxic houseplants, insecticides, and mycotoxins",
    "parakeet": "heavy metals (lead, zinc), heated PTFE fumes, avocado, toxic houseplants, insecticides, and mycotoxins",
    "parrot": "heavy metals (lead, zinc), heated PTFE fumes, avocado, toxic houseplants, insecticides, and mycotoxins",
    "reptile": "insecticides (organophosphates, pyrethroids), inappropriate disinfectants, heavy metals, ivermectin (fatal in some species), and toxic plants",
    "tortoise": "insecticides, inappropriate disinfectants, heavy metals, toxic plants, and oxalate-rich plants",
    "snake": "insecticides, inappropriate disinfectants (cedar/pine shaving volatiles), heavy metals, and ivermectin",
    "lizard": "insecticides, inappropriate disinfectants, heavy metals, ivermectin, and toxic plants",
    "amphibian": "water-quality toxins (ammonia, nitrite, residual chlorine/chloramine), heavy metals, agricultural pesticide run-off, and inappropriate pH",
    "fish": "water-quality toxins (ammonia, nitrite, residual chlorine, heavy metals), pesticide run-off, and medication overdose (copper, formalin)",
    "exotic_other": "toxic plants, insecticides, household chemicals, heavy metals, and chemical leaching from inappropriate enclosure materials",
}


def _toxin_sources_en(species: str) -> str:
    return TOXIN_SOURCES_EN.get(
        species,
        "toxic plants, rodenticides/pesticides, household chemicals, heavy metals, and medication overdose",
    )


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
        # Drop a trailing "（<species>）" tag so the species is not repeated by
        # the "<species>における…" lead-in (e.g. "四肢骨折（ハムスター）" ->
        # "ハムスターにおける四肢骨折"). Descriptive tags such as
        # "（ヨウ素欠乏性）" are kept because they do not name the species.
        m = _PAREN_TAG_RE.search(name_ja)
        if m and species_ja and species_ja in m.group(0):
            name_ja = _PAREN_TAG_RE.sub("", name_ja).strip()
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
            f"{sp_ja}で問題となりやすい代表的毒性源: {_toxin_sources(species)}。"
            f"毒性の発現は用量依存性で、体重・代謝能力・曝露経路・曝露時間により重症度が大きく異なる。"
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


def gen_causes_en(category: str, name_en: str, species: str) -> str:
    """English category aetiology mirroring ``gen_causes_ja``.

    Produces professional veterinary English for the same category set the
    Japanese generator uses, so the English ``causes`` field reaches parity
    with the (vet-reviewed) Japanese text and no longer shows the wrong
    organ-system template (e.g. an inflammatory disease described as a
    toxicosis). Category is resolved from the disease *name* by the caller.
    """
    sp_en = SPECIES_EN.get(species, species)
    prefix = _disease_prefix_en(name_en, sp_en)

    if category == "viral_infection":
        return (
            f"{prefix} is caused by viral infection. "
            f"A specific viral pathogen enters host cells and replicates intracellularly, producing tissue injury and a systemic inflammatory response. "
            f"Major risk factors include incomplete vaccination, immunosuppression, very young or old age, group housing, contact with newly introduced animals, and exposure to vectors (arthropods, wildlife). "
            f"The balance between pathogen virulence and host immune response determines onset and severity."
        )
    if category == "bacterial_infection":
        return (
            f"{prefix} is caused by infection with a specific bacterial pathogen. "
            f"Pathogenic bacteria enter the body (oral, percutaneous, respiratory, or vector-borne routes) and cause disease through proliferation, toxin production and tissue invasion. "
            f"Key risk factors are host immunosuppression (stress, malnutrition, concurrent disease), dysbiosis from inappropriate antimicrobial use, persistent exposure to a contaminated environment, and entry through bites or wounds. "
            f"The emergence of drug-resistant organisms (MRSP, ESBL producers) complicates treatment."
        )
    if category == "respiratory_infection":
        return (
            f"{prefix} is caused by infection of the upper or lower airway with respiratory pathogens (bacteria, viruses, fungi). "
            f"Environmental stress (abrupt temperature or humidity change, poor ventilation), overcrowding, group transport, and exposure to smoke or dust increase the risk of disease. "
            f"Brachycephalic animals or those with anatomical airway abnormalities, and the very young, old or immunosuppressed, are prone to severe disease. "
            f"Co-infection with multiple pathogens (e.g. Bordetella plus parainfluenza virus) frequently worsens the clinical picture."
        )
    if category == "fungal_infection":
        return (
            f"{prefix} is caused by infection with fungal pathogens. "
            f"These include dermatophytes (Microsporum/Trichophyton), yeasts (Malassezia/Candida) and deep/systemic fungi (Aspergillus/Cryptococcus/Histoplasma). "
            f"Risk factors include a humid environment, immunosuppression, disruption of normal flora by prolonged antimicrobial therapy, trauma or breakdown of the skin barrier, and residence in a geographically endemic area (e.g. coccidioidomycosis). "
            f"Dermatophytosis in particular is an important zoonosis with public-health implications."
        )
    if category == "parasitic":
        return (
            f"{prefix} is caused by infection with parasites (helminths, protozoa, arthropods). "
            f"Routes of infection vary by parasite species and include ingestion (contaminated food or water, predation of intermediate hosts), percutaneous penetration, arthropod vectors (ticks, mosquitoes, fleas), and transplacental or lactogenic transmission. "
            f"Overcrowding, poor hygiene, immunosuppression and inadequate routine deworming increase the risk of infection. "
            f"Understanding the parasite life cycle is key to successful treatment and to preventing re-infection; climate-driven expansion of vector ranges is increasing disease in areas previously considered low-risk."
        )
    if category == "neoplasia":
        return (
            f"The development of {prefix} is multifactorial. "
            f"Major factors include genetic predisposition (breed-specific tendencies), persistent chronic inflammation, oncogenic viral infection (aside from specific examples such as FeLV-associated lymphoma), prolonged exposure to chemical carcinogens, hormonal imbalance (sex-hormone-dependent tumours), failure of immune surveillance, and ultraviolet or ionising radiation. "
            f"Age-related decline in DNA repair capacity and dysregulated control of cell proliferation are promoting factors. "
            f"Early detection and staging (TNM classification) underpin prognosis and treatment selection."
        )
    if category == "endocrine_metabolic":
        return (
            f"{prefix} is caused by dysfunction of an endocrine gland or disruption of a metabolic pathway. "
            f"Specific mechanisms include autoimmune endocrine gland destruction, neoplastic hormone production (functional adenoma/carcinoma), iatrogenic causes (long-term steroids or other drugs), nutritional factors (dietary mineral or vitamin imbalance) and inherited enzyme deficiencies. "
            f"Age, obesity, breed-specific predisposition and concurrent disease (secondary endocrine disturbance from pancreatitis or renal failure) modify the risk. "
            f"Endocrine screening tests are important for early diagnosis."
        )
    if category == "renal_urinary":
        return (
            f"{prefix} is caused by progressive nephron injury, urinary tract obstruction or infection, or idiopathic lower-urinary-tract inflammation. "
            f"Major risk factors include ageing, chronic dehydration, exposure to nephrotoxins (NSAIDs, antifreeze, lilies, certain antibiotics), systemic hypertension, diabetic nephropathy, immune-complex glomerulonephritis, inherited structural renal anomalies, and stress-related neuroendocrine disturbance. "
            f"Because early disease is asymptomatic, periodic renal screening (SDMA, urine specific gravity, urine protein) is important."
        )
    if category == "cardiac":
        return (
            f"{prefix} is strongly influenced by breed-specific genetic predisposition. "
            f"Major primary causes are cardiomyopathy (DCM/HCM) in predisposed breeds, degenerative valve disease (myxomatous mitral valve degeneration in small-breed dogs), congenital defects (PDA, VSD, ASD) and arrhythmogenic cardiomyopathy. "
            f"Secondary factors include hypertension, hyperthyroidism (cats), nutritional causes (taurine/carnitine deficiency, grain-free-diet-associated DCM), drugs, and infective endocarditis. "
            f"Early diagnosis (echocardiography after murmur detection) and staged therapy directly improve prognosis."
        )
    if category == "respiratory_other":
        return (
            f"{prefix} comprises non-infectious airway disease with diverse causes. "
            f"These include allergic disease (feline asthma, eosinophilic bronchitis), anatomical abnormality (brachycephalic obstructive airway syndrome, tracheal collapse, laryngeal paralysis), neoplasia, nutritional causes (restrictive ventilation from obesity), chronic inflammatory disease (COPD-like conditions), and aspiration. "
            f"Environmental exposure to tobacco smoke, household chemicals, fragrances and excessive dust is an important risk factor. "
            f"Early intervention is desirable to prevent airway remodelling and irreversible structural change."
        )
    if category == "gastrointestinal":
        return (
            f"{prefix} has infectious, dietary, immune-mediated, mechanical and functional causes. "
            f"These include infectious (bacterial, viral, parasitic, protozoal), dietary (inappropriate food, foreign material, abrupt diet change, food allergy), immune-mediated (inflammatory bowel disease), mechanical (obstruction, torsion, neoplasia) and functional (motility disorder) causes. "
            f"In herbivores, insufficient dietary fibre and abrupt diet change are the leading causes of gastrointestinal stasis, so understanding species-specific nutritional requirements is important. "
            f"Stressors (environmental change, introduction of new animals) also contribute to onset."
        )
    if category == "neurological":
        return (
            f"{prefix} has diverse causes classified as infectious (encephalitis, meningitis), immune-mediated, degenerative, neoplastic, traumatic, vascular, metabolic, toxic, genetic and idiopathic (idiopathic epilepsy). "
            f"Breed-specific predisposition (cognitive dysfunction in older dogs, predisposed breeds for idiopathic epilepsy) is an important background factor. "
            f"Acute onset suggests trauma, vascular events or intoxication; chronic progression suggests degenerative, neoplastic or metabolic disease; and recurrent seizures suggest idiopathic epilepsy."
        )
    if category == "ophthalmic":
        breed_note = ""
        if species in ("dog", "cat"):
            breed_note = "Breed-specific predisposition is important (brachycephalic proptosis and keratoconjunctivitis sicca, cataract in Cocker Spaniels, Collie eye anomaly, breeds predisposed to progressive retinal atrophy). "
        elif species == "horse":
            breed_note = "In horses, equine recurrent uveitis (moon blindness) is associated with genetic predisposition (e.g. Appaloosa), and corneal ulceration is precipitated by stabling conditions (bedding, manure). "
        elif species in ("bird", "parakeet", "parrot"):
            breed_note = "In birds, nutritional (vitamin A deficiency), infectious (herpesvirus, Chlamydia, pox) and traumatic causes predominate. "
        elif species in ("reptile", "tortoise", "snake", "lizard"):
            breed_note = "In reptiles, nutritional causes (vitamin A deficiency, metabolic bone disease), eyelid obstruction from dysecdysis, and low POTZ predominate. "
        return (
            f"{prefix} has infectious (bacterial, viral, fungal, parasitic), traumatic, immune-mediated, congenital, degenerative, neoplastic, metabolic and iatrogenic causes. "
            f"{breed_note}"
            f"Because delayed treatment leads to irreversible vision loss, early diagnosis (tonometry, fundic examination, corneal staining) and specialist referral are essential."
        )
    if category == "musculoskeletal":
        species_specific = ""
        if species == "horse":
            species_specific = "In horses, laminitis, navicular syndrome, tendonitis and arthritis are the leading diseases that markedly reduce athletic performance. "
        elif species in ("reptile", "tortoise", "snake", "lizard", "amphibian"):
            species_specific = "In reptiles and amphibians, metabolic bone disease from vitamin D/UV-B deficiency and Ca/P imbalance is most common. "
        elif species in ("bird", "parakeet", "parrot"):
            species_specific = "In birds, nutritional osteomalacia, egg-laying-related calcium depletion and pneumatic (air-filled) bone fractures are the major conditions. "
        elif species in ("rabbit", "guinea_pig", "chinchilla", "hamster", "degu", "sugar_glider"):
            species_specific = "In small mammals, fractures and luxations (during handling or falls) and spinal injury are the major traumas, against a background of a fragile skeleton. "
        return (
            f"{prefix} is classified as traumatic (fracture, luxation, ligament injury), degenerative (osteoarthritis), developmental/genetic (hip or elbow dysplasia, patellar luxation), immune-mediated (polyarthritis), infectious (osteomyelitis, septic arthritis), nutritional (metabolic bone disease, nutritional secondary hyperparathyroidism), neoplastic (osteosarcoma) and hereditary (chondrodysplasia). "
            f"{species_specific}"
            f"Obesity, excessive exercise and inappropriate nutrition (excess calories or calcium during growth) increase the risk of degenerative and developmental disease."
        )
    if category == "dental":
        return (
            f"{prefix} is chiefly caused by bacterial inflammation from plaque and calculus accumulation (periodontal disease), malocclusion, traumatic tooth fracture, periapical abscess, overgrown (elodont) teeth in herbivores and rodents, and malignancy (oral squamous cell carcinoma, fibrosarcoma). "
            f"In herbivores (rabbit, guinea pig, chinchilla, degu) the teeth grow continuously throughout life, and insufficient fibre, hereditary malocclusion or trauma leads to overgrowth and molar spur formation. "
            f"In small and brachycephalic dogs, dental crowding causes frequent periodontal disease. Early oral care and annual dental scaling are the foundation of prevention."
        )
    if category == "dermatological":
        return (
            f"{prefix} has diverse causes classified as allergic (atopic dermatitis, food allergy, flea-allergy dermatitis), infectious (bacterial pyoderma, dermatophytosis, Malassezia dermatitis), parasitic (mange, demodicosis, ear mites), immune-mediated (pemphigus, lupus), endocrine (dermatoses associated with hypothyroidism or Cushing's), nutritional, psychogenic/behavioural (over-grooming, self-trauma) and neoplastic. "
            f"Environmental factors (humidity, temperature, bedding hygiene) and breed-specific predisposition are important modifiers of onset."
        )
    if category == "hematological":
        return (
            f"{prefix} is classified by mechanism as decreased production (marrow hypoplasia, nutritional deficiency, reduced erythropoietic drive in renal failure), haemolysis (immune-mediated, parasitic, oxidative injury, hereditary membrane defects), haemorrhage (trauma, coagulopathy, platelet disorders), consumption (DIC, thrombosis) and sequestration (splenomegaly). "
            f"Important specific causes include infectious agents (FeLV, FIV, Babesia, haemoplasma, Ehrlichia), immune-mediated disease (IMHA, ITP), drugs (chemotherapy, certain antibiotics) and toxins (onion, acetaminophen, anticoagulant rodenticides)."
        )
    if category == "reproductive":
        return (
            f"{prefix} has infectious (bacterial, viral, parasitic), anatomical (fetal malposition, pelvic stenosis), endocrine (luteal insufficiency, prolactin disturbance), metabolic (pregnancy toxaemia, hypocalcaemia), traumatic, neoplastic (mammary, testicular, prostatic tumours), hereditary and age-related causes. "
            f"Early neutering has a clear protective effect against hormone-dependent tumours, pyometra and prostatic hyperplasia (notably the relationship between early spaying and reduced mammary tumour risk)."
        )
    if category == "toxicity":
        return (
            f"{prefix} is caused by ingestion, inhalation or dermal absorption of a specific toxic substance. "
            f"Toxic sources of particular concern in {sp_en} include {_toxin_sources_en(species)}. "
            f"Toxicity is dose-dependent, and severity varies markedly with body weight, metabolic capacity, route of exposure and duration of exposure. "
            f"The liver and kidneys are the principal target organs."
        )
    if category == "trauma":
        return (
            f"{prefix} is caused by physical tissue injury from external force (falls, collision, crushing, bites, lacerations from sharp objects). "
            f"Major causes include inappropriate housing (cramped or excessively tall enclosures, sharp protrusions, slippery flooring), fighting with other animals, careless handling, escape/flight, and road traffic accidents. "
            f"Small and young animals are prone to severe trauma, and much of it is preventable through appropriate enclosure design and safety management. "
            f"Initial assessment should anticipate secondary complications (infection, haemorrhagic shock, tissue necrosis)."
        )
    if category == "autoimmune":
        return (
            f"{prefix} is caused by loss of self-tolerance and an aberrant immune response against self-antigens. "
            f"Reported triggers include genetic predisposition, molecular mimicry from infection, drug administration, ultraviolet exposure, hormonal fluctuation and vaccination. "
            f"Autoantibodies and self-reactive T cells attack and destroy normal tissue, causing multi-organ injury. "
            f"Diagnosis requires specific autoantibody testing and histopathology; long-term immunosuppression and relapse monitoring are central to management."
        )
    if category == "nutritional":
        return (
            f"{prefix} is caused by deficiency, excess or imbalance of essential nutrients. "
            f"Inappropriate diet composition, malabsorption, metabolic disturbance and increased demand (growth, pregnancy, lactation) contribute. "
            f"Imbalances of vitamins, minerals, essential amino acids and essential fatty acids manifest as skeletal developmental abnormalities, impaired immune function, skin and coat changes, and reproductive failure. "
            f"Key risks include the quality of commercial complete diets, the nutritional balance of home-prepared food, over-supplementation, and inadequate understanding of species-specific requirements (taurine in cats, vitamin C in guinea pigs, calcium/UV-B in reptiles)."
        )
    if category == "genetic_congenital":
        return (
            f"{prefix} is caused by gene mutation or chromosomal abnormality arising during embryonic development. "
            f"Inheritance patterns are varied (autosomal dominant or recessive, X-linked, polygenic), and abnormal intrauterine environment, maternal infection, drug exposure or nutritional deficiency can also affect fetal organogenesis. "
            f"Incidence is higher in highly inbred purebreds and specific closed populations. "
            f"Pre-breeding genetic testing and carrier-exclusion programmes are important for population-level control."
        )
    if category == "degenerative":
        return (
            f"{prefix} is caused by progressive age-related tissue degeneration and declining repair capacity. "
            f"It progresses particularly in tissues with limited regenerative capacity such as cartilage, intervertebral discs and nervous tissue. "
            f"Genetic predisposition, chronic mechanical load from excess body weight, repetitive microtrauma, oxidative stress and persistent chronic inflammation are promoting factors. "
            f"Progression can be slowed by early detection and appropriate weight management, physical therapy and anti-inflammatory treatment."
        )
    if category == "behavioral":
        return (
            f"{prefix} arises from a complex interplay of neuroendocrine dysregulation, genetic predisposition, inadequate socialisation, past traumatic experience, environmental stress, and the influence of medical disease (pain, thyroid disease, cognitive dysfunction). "
            f"Triggers include insufficient experience during the developmental (socialisation) period, chronic environmental stress, punishment-based training, and life changes (change of owner, moving house, introduction of a new animal). "
            f"Because behavioural problems directly affect the animal's quality of life and the owner relationship, an integrated approach of ruling out medical disease plus environmental enrichment, behaviour modification and, where indicated, medication is required."
        )
    # generic
    return (
        f"The precise aetiology of {prefix} varies between cases. "
        f"Genetic predisposition, environmental factors (inappropriate management of temperature, humidity and hygiene), exposure to infectious pathogens, dietary imbalance, immune dysregulation and age-related tissue change contribute alone or in combination. "
        f"Identifying the cause is essential for treatment planning and relapse prevention, and is achieved through integrated assessment of history, physical examination and ancillary tests."
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


def _disease_prefix_en(name_en: str, species_en: str) -> str:
    """English disease subject phrase, species-qualified for prose.

    Embeds the species (mirroring the JA ``_disease_prefix``) so the same
    disease name in different species yields distinct, species-aware text —
    a fracture in a bird with pneumatic bones is not the fracture of a cat.
    """
    name = _clean_name(name_en)
    if name:
        return f"{name} in {species_en}"
    return f"this disease in {species_en}"


def gen_clinical_signs(category: str, name_en: str, species: str) -> str:
    """Disease-specific English clinical signs (replaces category templates)."""
    sp_en = SPECIES_EN.get(species, species)
    name = _disease_prefix_en(name_en, sp_en)

    if category in ("viral_infection", "bacterial_infection", "respiratory_infection", "fungal_infection"):
        sys_specific = ""
        if category == "respiratory_infection":
            sys_specific = " Respiratory signs predominate (cough, sneezing, nasal discharge, dyspnoea), with pneumonia in advanced cases."
        elif category == "fungal_infection":
            sys_specific = " Skin lesions (circular alopecia, scaling, crusting), chronic nasal discharge, or—in systemic mycoses—cough, weight loss and neurological signs may occur."
        return (
            f"Clinical signs of {name} vary with the site of infection and the pathogen, "
            f"but fever, lethargy, inappetence and weight loss are common shared findings. "
            f"Local infection causes redness, swelling, pain and purulent discharge, while systemic infection may progress to dehydration, sepsis and multi-organ failure.{sys_specific} "
            f"Juvenile, geriatric and immunosuppressed animals are at higher risk of severe disease, so early intervention improves outcome."
        )
    if category == "parasitic":
        return (
            f"Clinical signs of {name} depend on the parasite species, location and burden. "
            f"Gastrointestinal parasitism causes diarrhoea, vomiting, weight loss and abdominal distension; ectoparasites cause pruritus, alopecia and dermatitis; "
            f"cardiovascular parasites cause cough, exercise intolerance and ascites; and haemoparasites cause anaemia, fever and lethargy. "
            f"Young or malnourished animals are prone to severe disease, with poor growth in chronic cases."
        )
    if category == "neoplasia":
        return (
            f"Clinical signs of {name} depend on the affected organ and tumour type. "
            f"Common findings include a progressive mass, weight loss, inappetence, lethargy and anaemia. "
            f"Cutaneous tumours present as a palpable swelling, while internal tumours cause non-specific signs such as abdominal distension, vomiting, diarrhoea, dyspnoea or lymphadenopathy. "
            f"Paraneoplastic syndromes such as hypercalcaemia (lymphoma, anal-sac carcinoma) or hypoglycaemia (insulinoma) may accompany the disease."
        )
    if category == "endocrine_metabolic":
        return (
            f"Clinical signs of {name} follow the specific hormonal or metabolic disturbance. "
            f"Diabetes mellitus: polyuria/polydipsia, polyphagia and weight loss. Hyperthyroidism: weight loss, polyphagia, hyperactivity and tachycardia. "
            f"Cushing's syndrome: abdominal distension, alopecia, polyuria/polydipsia and thin skin. Addison's disease: lethargy, vomiting, diarrhoea and electrolyte derangement. "
            f"Early disease is often subclinical, so periodic endocrine screening aids early detection."
        )
    if category == "renal_urinary":
        return (
            f"Clinical signs of {name} vary with the underlying lesion and stage. "
            f"Chronic kidney disease: polyuria/polydipsia, weight loss, inappetence, vomiting, halitosis and dehydration (subclinical when early). "
            f"Acute kidney injury: oliguria/anuria, vomiting, lethargy and electrolyte disturbance. "
            f"Lower urinary tract disease: pollakiuria, dysuria, haematuria and inappropriate urination, with urethral obstruction (an emergency) in males."
        )
    if category == "cardiac":
        return (
            f"Clinical signs of {name} progress in stages with declining cardiac function. "
            f"Compensated (asymptomatic): a murmur may be the only finding on auscultation. "
            f"Early failure: exercise intolerance, cough (left-sided) or ascites (right-sided). "
            f"Advanced failure: dyspnoea, cyanosis, syncope and nocturnal cough. "
            f"In cats, feline aortic thromboembolism may present acutely with hindlimb paresis, cold limbs, pain and absent pulses."
        )
    if category == "respiratory_other":
        return (
            f"Clinical signs of {name} depend on the site of airway obstruction or ventilatory compromise. "
            f"Upper airway: stertor, inspiratory stridor, exercise intolerance and inspiratory cyanosis (brachycephalic airway syndrome). "
            f"Trachea: a short, dry, paroxysmal cough and stridor (tracheal collapse). "
            f"Lower airway: chronic cough, expiratory dyspnoea and wheezing (asthma/COPD-like disease), often triggered by stress, exercise or temperature change."
        )
    if category == "gastrointestinal":
        return (
            f"Clinical signs of {name} vary with the site and nature of the gastrointestinal lesion. "
            f"Upper GI: vomiting, haematemesis and inappetence. Small intestine: small-bowel diarrhoea (large volume, low frequency, weight loss), vomiting and abdominal pain. "
            f"Large intestine: large-bowel diarrhoea (small volume, high frequency, mucus, haematochezia, tenesmus). "
            f"Acute abdomen with severe pain, vomiting, shock or a palpable mass (GDV, volvulus, obstruction) requires emergency evaluation."
        )
    if category == "neurological":
        return (
            f"Clinical signs of {name} localise to the affected region (forebrain, brainstem, cerebellum, spinal cord or peripheral nerve). "
            f"Forebrain: seizures, behavioural change, blindness, circling and ataxia. Brainstem: cranial nerve deficits, ataxia and altered consciousness. "
            f"Cerebellum: intention tremor, hypermetria and a broad-based stance. Spinal cord: para-/tetraparesis, urinary dysfunction and reflex changes that vary with the lesion level. "
            f"Peripheral nerve: muscle atrophy, hyporeflexia and distal flaccid paresis."
        )
    if category == "ophthalmic":
        return (
            f"Clinical signs of {name} vary with the affected structure (cornea, conjunctiva, anterior chamber, lens, retina). "
            f"Conjunctivitis: conjunctival hyperaemia, discharge, epiphora and blepharospasm. Corneal ulcer: epiphora, blepharospasm, photophobia and corneal opacity (fluorescein positive). "
            f"Glaucoma: acute ocular pain, corneal oedema, mydriasis, buphthalmos and vision loss. "
            f"Cataract: progressive vision loss from lens opacity; retinal disease: progressive or acute vision loss (PRA, retinal detachment)."
        )
    if category == "musculoskeletal":
        return (
            f"Clinical signs of {name} depend on the site and whether the process is acute or chronic. "
            f"Acute trauma: non-weight-bearing lameness, swelling, pain and deformity (fracture, luxation). "
            f"Chronic degeneration: difficulty rising, exercise intolerance, lameness worse after exercise or in cold, and joint swelling (osteoarthritis). "
            f"Developmental disease: mild lameness from a young age (hip/elbow dysplasia); infectious: febrile joint swelling and pain (septic arthritis)."
        )
    if category == "dental":
        return (
            f"Clinical signs of {name} vary with the dental condition and its progression. "
            f"Periodontal disease: halitosis, gingival redness/swelling, ptyalism, difficulty eating and facial swelling with apical abscessation. "
            f"Malocclusion (herbivores): drooling, slow or selective eating, weight loss, reduced faecal output, exophthalmos and mandibular abscesses. "
            f"Tooth-root fracture: difficulty eating, unilateral chewing and halitosis; oral tumours: an oral mass, bleeding, ptyalism and dysphagia."
        )
    if category == "dermatological":
        return (
            f"Clinical signs of {name} vary with the cause and stage. "
            f"Acute: erythema, vesicles, moist lesions, intense pruritus and alopecia (contact dermatitis, urticaria). "
            f"Chronic: lichenification, hyperpigmentation, alopecia, scaling and crusting (atopic dermatitis, chronic pyoderma). "
            f"Distribution aids diagnosis: face/paws (atopy), ears/ventrum (flea allergy), symmetrical alopecia (endocrine), circular lesions (dermatophytosis, demodicosis)."
        )
    if category == "hematological":
        return (
            f"Clinical signs of {name} vary with the blood component affected. "
            f"Anaemia: pale mucous membranes, lethargy, exercise intolerance, tachycardia and tachypnoea (syncope and a murmur when severe). "
            f"Bleeding tendency: petechiae, mucosal bleeding, haematuria, melena and haemarthrosis (coagulopathy, thrombocytopathy). "
            f"Thrombosis: acute limb pain and paresis (FATE) or dyspnoea (pulmonary embolism); haemolysis: icterus, dark urine and splenomegaly."
        )
    if category == "reproductive":
        return (
            f"Clinical signs of {name} vary with the reproductive lesion. "
            f"Pyometra: polyuria/polydipsia, vomiting, lethargy, abdominal distension and vulvar discharge (open) or insidious progression (closed). "
            f"Mastitis: mammary swelling, pain, fever and abnormal milk. Prostatic disease: dysuria, haematuria, dyschezia and hindlimb lameness. "
            f"Dystocia: prolonged labour, persistent straining and abnormal interval between offspring; eclampsia: peripartum lethargy, inappetence and neurological signs."
        )
    if category == "toxicity":
        return (
            f"Clinical signs of {name} range from acute to chronic depending on the toxicant and dose. "
            f"Gastrointestinal signs (vomiting, diarrhoea, ptyalism, abdominal pain) are the most common early finding. "
            f"Neurotoxins cause tremor, seizures, ataxia and coma; hepatotoxins cause icterus, coagulopathy and hepatic encephalopathy; nephrotoxins cause oliguria and uraemia. "
            f"Acute exposure produces rapid onset, where early decontamination and supportive care determine the outcome."
        )
    if category == "trauma":
        return (
            f"Clinical signs of {name} vary with the site and severity of injury. "
            f"Fracture: non-weight-bearing lameness, swelling, crepitus, deformity and pain. Laceration: bleeding, tissue loss and infection risk. "
            f"Visceral injury: shock, abdominal guarding and dyspnoea (diaphragmatic hernia, pneumothorax). "
            f"Brain contusion: depressed consciousness, pupillary abnormalities, ataxia and seizures; spinal injury: paralysis, abnormal reflexes and urinary dysfunction."
        )
    if category == "autoimmune":
        return (
            f"Clinical signs of {name} are diverse and depend on the tissue affected. "
            f"IMHA: icterus, pallor, lethargy and tachypnoea. ITP: petechiae, mucosal bleeding, melena and haematuria. "
            f"Immune-mediated polyarthritis: shifting-leg lameness, fever and joint swelling. Pemphigus: scaly/vesicular skin and mucosal lesions with crusting. "
            f"SLE: multi-organ involvement (skin, joints, kidney, blood). A relapsing-remitting course is characteristic."
        )
    if category == "nutritional":
        return (
            f"Clinical signs of {name} show specific patterns according to the deficient or excess nutrient. "
            f"Calcium deficiency: osteomalacia, pathological fractures, seizures and poor growth. Vitamin A deficiency: ocular disease, abnormal keratinisation, night blindness and reproductive failure. "
            f"Vitamin C deficiency (guinea pigs): joint swelling, bleeding tendency, periodontal disease and poor growth. "
            f"Protein-energy malnutrition: emaciation, muscle wasting, hypoalbuminaemia and oedema; vitamin D/UV-B deficiency (reptiles): metabolic bone disease."
        )
    if category == "behavioral":
        return (
            f"Clinical signs of {name} vary with the behavioural problem. "
            f"Separation anxiety: destructive behaviour, excessive vocalisation and inappropriate elimination when the owner is absent. "
            f"Phobias (thunder, fireworks): trembling, hiding, panting, destruction and escape attempts. Aggression: growling, baring teeth and biting (fear, territorial, resource-guarding). "
            f"Compulsive disorder: repetitive purposeless behaviour (tail-chasing, flank-sucking, over-grooming); cognitive dysfunction: circling, night vocalisation, reduced interaction and altered elimination."
        )
    return (
        f"Clinical signs of {name} are varied and depend on the disease process and its stage. "
        f"In addition to non-specific findings (inappetence, lethargy, weight loss), signs specific to the affected organ or system become apparent. "
        f"History-taking and a thorough physical examination establish the pattern of signs, with ancillary testing used to reach a definitive diagnosis. "
        f"Early detection and appropriate intervention are key to an improved outcome."
    )


def gen_transmission(category: str, name_en: str, species: str) -> str:
    """Disease-specific English transmission text (replaces category templates)."""
    sp_en = SPECIES_EN.get(species, species)
    name = _disease_prefix_en(name_en, sp_en)

    if category == "viral_infection":
        return (
            f"Transmission of {name} depends on the causative virus. "
            f"Major routes include aerosol/droplet spread (respiratory viruses), faecal-oral spread (enteric viruses), arthropod vectors (arboviruses), sexual contact, and vertical transplacental or lactogenic transmission. "
            f"Environmental stability of the virus determines the risk of indirect (fomite) transmission via contaminated surfaces, equipment and clothing. "
            f"For highly contagious viruses, maintaining vaccination coverage for herd immunity is an important public-health measure."
        )
    if category == "bacterial_infection":
        return (
            f"Transmission of {name} is diverse and reflects the ecology of the causative organism. "
            f"Routes include direct contact (bites, sexual contact, transplacental), droplet spread, faecal-oral spread, arthropod vectors, opportunistic infection by environmental commensals, and ingestion of contaminated food or water. "
            f"Identifying and isolating the source animal, hand hygiene, disinfection of contaminated equipment and the environment, and vector control are the mainstays of breaking transmission. "
            f"Zoonotic pathogens require notification of public-health authorities and screening of contacts."
        )
    if category == "respiratory_infection":
        return (
            f"The principal route of transmission for {name} is droplet spread of respiratory secretions (coughing, sneezing). "
            f"Close contact in confined spaces, shared food and water bowls or bedding, and indirect spread via contaminated hands and clothing also occur. "
            f"Ventilation, density management, quarantine of new arrivals (minimum 14 days) and environmental disinfection (hypochlorite or alcohol-based) help interrupt transmission. "
            f"Animals may shed the pathogen for weeks after clinical recovery, so contact should be limited until full recovery is confirmed."
        )
    if category == "fungal_infection":
        return (
            f"Transmission of {name} varies with the fungal species. "
            f"Dermatophytosis spreads by direct contact with infected animals or by arthrospores in a contaminated environment (bedding, carpet, grooming tools). "
            f"Systemic mycoses (Coccidioides, Blastomyces, Histoplasma) follow inhalation of environmental spores, so animal-to-animal transmission essentially does not occur. "
            f"Candida and Malassezia are commensals that cause opportunistic infection under immunosuppression."
        )
    if category == "parasitic":
        return (
            f"Transmission of {name} is determined by the parasite species. "
            f"Routes include ingestion (contaminated food/water or predation of intermediate hosts), percutaneous penetration (hookworm, schistosomes), arthropod vectors (ticks, mosquitoes, fleas), the faecal-oral route (coccidia, Giardia), and sexual or transplacental transmission of certain protozoa. "
            f"Understanding the life cycle of intermediate and definitive hosts is key to interrupting transmission. "
            f"Strict environmental hygiene, vector control and routine deworming are preventive measures."
        )
    if category == "neoplasia":
        return (
            f"As a neoplastic disease, {name} is essentially non-infectious and is not directly transmitted between animals. "
            f"However, oncogenic viruses (e.g. FeLV, papillomaviruses) are transmissible and can later cause virus-associated tumours. "
            f"Canine transmissible venereal tumour (CTVT) and Tasmanian devil facial tumour are rare exceptions in which the tumour cells themselves spread directly. "
            f"Genetic predisposition is inherited vertically, so breeding management of affected lines is important."
        )
    if category == "endocrine_metabolic":
        return (
            f"As a non-infectious disease, {name} is not directly transmitted between animals. "
            f"Several animals sharing the same environmental factors (high-carbohydrate diet, inactivity, obesity-promoting husbandry) may, however, be affected concurrently. "
            f"Hereditary predisposition (breed susceptibility to Cushing's syndrome or diabetes) is passed from parent to offspring. "
            f"It is not transmissible to humans, and accurate owner education prevents the misperception that the animal is an infectious source."
        )
    if category == "toxicity":
        return (
            f"As a non-infectious condition, {name} is not directly transmitted between animals. "
            f"Exposure to the toxicant is environmental; concurrent poisoning of several animals in the same environment reflects common exposure rather than transmission. "
            f"Identifying and removing the source, assessing exposure risk to other animals, and advising on safe storage and disposal are important to prevent recurrence. "
            f"The risk of human exposure should be assessed at the same time."
        )
    if category == "trauma":
        return (
            f"As a traumatic condition, {name} is not directly transmitted between animals. "
            f"Shared environmental hazards (cramped cages, slippery flooring, contact with other animals) may, however, cause sequential injury to several animals. "
            f"Identifying the cause and improving the environment (reviewing housing, separating animals, improving flooring) is essential to prevent recurrence and spread to other individuals."
        )
    if category == "autoimmune":
        return (
            f"As an autoimmune disease, {name} is not directly transmitted between animals. "
            f"Reported triggers include infection (T-cell activation by molecular mimicry), vaccination, drug administration and UV exposure, so incidence may rise in groups sharing these environmental factors. "
            f"Genetic predisposition (HLA/DLA associations) is inherited, so breeding of affected animals should be considered carefully."
        )
    if category == "nutritional":
        return (
            f"As a non-infectious disease, {name} is not directly transmitted between animals. "
            f"Several animals in a group may be affected at once, but this represents a common-source outbreak from an inappropriate diet rather than contagion. "
            f"Dietary correction for the whole group is required to resolve it collectively. "
            f"Owner education (basic nutrition and species-specific requirements) is most important for prevention of recurrence."
        )
    if category == "renal_urinary":
        return (
            f"As a predominantly non-infectious disease, {name} is usually not transmitted between animals. "
            f"Indirect transmission is possible only with bacterial urinary tract infection or pyelonephritis, but the condition is essentially individual. "
            f"Leptospirosis is a zoonosis transmitted via urine, so confirmed cases require notification of public-health authorities and contact management. "
            f"Hereditary renal disease (e.g. PKD) is inherited, making breeding management important."
        )
    if category == "cardiac":
        return (
            f"As a non-infectious disease, {name} is not directly transmitted between animals. "
            f"Hereditary cardiac disease (breeds predisposed to DCM or HCM) is inherited, so avoiding breeding of affected animals is important for population-level control. "
            f"In infective endocarditis the organism reaches the heart haematogenously from another site of infection; there is no animal-to-animal transmission from the heart itself."
        )
    if category == "respiratory_other":
        return (
            f"As a non-infectious disease, {name} is not directly transmitted between animals. "
            f"In allergic disease, several individuals may be affected concurrently through exposure to the same environment (tobacco smoke, house dust, chemicals). "
            f"Brachycephalic airway syndrome, tracheal collapse and laryngeal paralysis arise from anatomical predisposition with a breed-specific genetic background."
        )
    if category == "gastrointestinal":
        return (
            f"Transmission of {name} varies with the cause. "
            f"Infectious causes (parvovirus, Salmonella, parasites) spread to other animals by the faecal-oral route. "
            f"Non-infectious causes (IBD, neoplasia, mechanical obstruction, motility disorders) are not transmitted between animals. "
            f"Environmental disinfection, quarantine of new arrivals and strict faecal management are important to prevent infectious gastrointestinal disease."
        )
    if category == "neurological":
        return (
            f"Transmissibility of {name} varies with the cause. "
            f"Infectious encephalitis/meningitis (bacterial, viral, protozoal) spreads by the route appropriate to the pathogen. "
            f"Idiopathic epilepsy, degenerative disease and neoplasia are not transmitted between animals. "
            f"Rabies (a zoonosis) is transmitted via saliva through bite wounds, so vaccination and avoiding contact with wildlife are critically important."
        )
    if category == "ophthalmic":
        return (
            f"Transmission of {name} varies with the cause. "
            f"Infectious conjunctivitis (feline herpesvirus, Chlamydia, Mycoplasma) spreads to other cats by droplet and contact. "
            f"Non-infectious causes (cataract, glaucoma, retinal degeneration) are not transmitted between animals. "
            f"Hereditary ocular disease (collie eye anomaly, PRA) is inherited from parent to offspring."
        )
    if category == "musculoskeletal":
        return (
            f"As a non-infectious disease, {name} is usually not transmitted between animals. "
            f"Only in septic osteomyelitis or septic arthritis can the organism spread haematogenously; the joint disease itself is individual. "
            f"Hereditary orthopaedic disease (hip dysplasia, intervertebral disc degeneration) is inherited, so breeding management is important for population-level control."
        )
    if category == "dental":
        return (
            f"As a non-infectious disease, {name} is not directly transmitted between animals. "
            f"The bacteria causing periodontal disease are oral commensals, not an external source of infection. "
            f"Hereditary predisposition to malocclusion (brachycephalic and small-breed dogs) is inherited. "
            f"Malocclusion in herbivores can affect a group through the shared husbandry factor of inadequate dietary fibre."
        )
    if category == "dermatological":
        return (
            f"Transmission of {name} varies with the cause. "
            f"Infectious skin disease (dermatophytosis, scabies, ear mites) spreads between animals by contact. "
            f"Allergic, immune-mediated and endocrine skin disease is not transmitted. "
            f"Dermatophytosis (especially Microsporum canis) and scabies are zoonoses that can spread to owners, requiring public-health consideration."
        )
    if category == "hematological":
        return (
            f"Transmission of {name} varies with the cause. "
            f"Infectious blood diseases (Babesia, Ehrlichia, haemoplasma) are tick-borne. "
            f"FeLV-associated anaemia and myelosuppression have an underlying viral infection. "
            f"Immune-mediated, nutritional and hereditary blood diseases are not transmitted between animals. "
            f"Because of transfusion-associated infection risk, blood donors are screened for blood-borne disease."
        )
    if category == "reproductive":
        return (
            f"Transmission of {name} varies with the cause. "
            f"Infectious reproductive disease (brucellosis, herpesvirus, the venereal tumour CTVT) spreads by sexual contact or transplacentally. "
            f"Non-infectious causes (pyometra, dystocia, neoplasia) are not transmitted. "
            f"Early spay/neuter and screening for infectious reproductive disease (brucellosis in particular is zoonotic) are important for prevention."
        )
    if category == "genetic_congenital":
        return (
            f"As a genetic or congenital disorder, {name} is not acquired by transmission between animals. "
            f"It is inherited from parent to offspring according to the mode of inheritance (autosomal dominant, recessive, X-linked or polygenic). "
            f"Population-level control requires pre-breeding genetic testing, exclusion of carriers and avoidance of inbreeding. "
            f"Tracking affected lines and pedigree management are important."
        )
    return (
        f"Transmissibility of {name} depends on the underlying cause. "
        f"Infectious causes spread between animals by pathogen-specific routes (contact, droplet, vectors, transplacental). "
        f"Non-infectious causes (traumatic, metabolic, neoplastic, degenerative, hereditary) are not transmitted between animals. "
        f"Accurate identification of the cause allows assessment of transmission risk and design of preventive measures."
    )


# Category-specific diagnostic workups. {p} = species-qualified disease prefix.
_DIAGNOSIS_JA: dict[str, str] = {
    "viral_infection": "{p}の診断は病歴（ワクチン歴・曝露歴・発症経過）と身体検査を起点とし、PCR・抗原検査・ペア血清抗体価でウイルスを同定する。CBC・生化学で全身状態と臓器障害を評価し、画像検査で罹患臓器を確認する。確定診断と他疾患の除外が治療方針を決定する。",
    "bacterial_infection": "{p}の診断は病歴・身体検査に加え、罹患部位の細菌培養・感受性試験を基本とする。CBC（白血球増多・核左方移動）・生化学・CRP/SAAなど炎症マーカー、グラム染色・細胞診、必要に応じPCRで起因菌を同定する。感受性結果に基づく抗菌薬選択が治療成功の鍵となる。",
    "respiratory_infection": "{p}の診断は呼吸器症状の評価と病歴聴取を起点に、胸部X線・必要に応じCTで肺病変を評価する。鼻腔・咽頭スワブまたはBALのPCR・培養で病原体を同定し、CBC・生化学で全身状態を確認する。低酸素血症の評価にSpO2・血液ガスを用いる。",
    "fungal_infection": "{p}の診断は病変部の細胞診・真菌培養・KOH直接鏡検を基本とし、皮膚糸状菌ではウッド灯検査・毛検査を併用する。深在性真菌症では抗原・抗体検査、画像検査、組織生検による確定診断を要する。再発・難治例では薬剤感受性評価も検討する。",
    "parasitic": "{p}の診断は寄生部位に応じた検査を選択する。消化管寄生では糞便浮遊法・直接塗抹・抗原検査、外部寄生では皮膚掻爬・セロハンテープ法・被毛検査、血液・心血管寄生では血液塗抹・抗原検査・画像検査を用いる。寄生虫種とライフサイクルの同定が治療・予防計画の基盤となる。",
    "neoplasia": "{p}の診断はFNA細胞診を第一選択とし、確定には組織生検・病理組織学的検査を要する。CBC・生化学、胸腹部X線・超音波・必要に応じCT/MRIで原発巣と転移を評価し、所属リンパ節の細胞診を含めた病期分類（ステージング）を行う。腫瘍型と病期が治療法と予後を左右する。",
    "endocrine_metabolic": "{p}の診断はホルモン・代謝指標の測定を中心とする。糖尿病: 血糖・尿糖・フルクトサミン。甲状腺機能: T4・freeT4・TSH。副腎皮質機能亢進: ACTH刺激試験・低用量デキサメサゾン抑制試験。電解質・血液ガスで代謝状態を評価する。早期は無症候のため定期的内分泌スクリーニングが有用。",
    "renal_urinary": "{p}の診断は尿検査（比重・蛋白・沈渣）・血液検査（クレアチニン・BUN・SDMA・リン・カリウム）を基本とし、尿蛋白クレアチニン比（UPC）、画像検査（超音波・X線）で形態を評価する。細菌感染では尿培養、結石では成分分析を行う。IRISステージ分類で病期を判定する。",
    "cardiac": "{p}の診断は聴診（心雑音・不整脈・奔馬調律）を起点に、胸部X線（心拡大・肺水腫）、心エコー図（構造・機能評価の中心）、心電図（不整脈評価）を組み合わせる。NT-proBNP・トロポニン、血圧測定を補助的に用い、心不全のステージ分類で治療方針を決定する。",
    "respiratory_other": "{p}の診断は胸部X線・必要に応じCTで気道・肺実質を評価し、気管支鏡・気管支肺胞洗浄（BAL）で細胞診・培養を行う。上気道閉塞では喉頭・咽頭の内視鏡評価、気管虚脱では透視（呼気・吸気）が有用。SpO2・血液ガスで換気・酸素化を確認する。",
    "gastrointestinal": "{p}の診断は病歴・身体検査・腹部触診を起点に、糞便検査、血液検査、腹部X線・超音波で評価する。慢性・難治例では内視鏡・生検による組織診断、消化吸収試験（cobalamin・folate・TLI）を行う。急性腹症では緊急画像評価で外科適応を判断する。",
    "neurological": "{p}の診断は神経学的検査による病変局在診断を起点とし、MRI（脳・脊髄の第一選択）・CTで構造を評価する。脳脊髄液（CSF）検査で炎症・感染・腫瘍を鑑別し、末梢神経・筋疾患では電気生理学的検査（筋電図・神経伝導速度）・筋生検を用いる。",
    "ophthalmic": "{p}の診断は眼科検査（細隙灯顕微鏡・眼底検査）を基本とし、フルオレセイン染色（角膜潰瘍）、眼圧測定（緑内障）、シルマー涙液試験（乾性角結膜炎）を組み合わせる。網膜疾患では眼底検査・網膜電図（ERG）、眼内構造評価には眼超音波を用いる。",
    "musculoskeletal": "{p}の診断は整形外科的検査（跛行評価・触診・関節可動域）を起点に、X線で骨・関節を評価する。必要に応じCT/MRI、関節液検査（敗血症性・免疫介在性関節炎の鑑別）、関節鏡を用いる。発達性疾患では特定肢位での撮影、感染では培養を行う。",
    "dental": "{p}の診断は口腔内視診（歯牙・歯肉・咬合・口腔粘膜）を起点に、歯科X線で歯根・歯槽骨を評価する。草食動物では臼歯の過長・スパー・歯根膿瘍を頬側・舌側から評価し、頭部X線で歯根伸長・骨融解を確認する。麻酔下の精密検査が確定診断に有用。",
    "dermatological": "{p}の診断は病変分布の評価を起点に、皮膚掻爬（疥癬・毛包虫）、被毛検査・真菌培養（皮膚糸状菌）、押捺・掻爬細胞診（細菌・マラセチア）、ウッド灯を用いる。アレルギーでは除外診断・食物試験・皮内/血清IgE検査、難治例では皮膚生検を行う。",
    "hematological": "{p}の診断はCBC・血液塗抹（形態評価）を基本とし、貧血では網赤血球数・鉄指標・クームス試験、出血傾向では血小板数・凝固系（PT/APTT）・D-ダイマーを評価する。必要に応じ骨髄検査、感染では病原体PCR・血液塗抹、画像検査で脾腫・出血源を確認する。",
    "reproductive": "{p}の診断は病歴（発情・交配・分娩歴）と身体検査を起点に、腹部・生殖器の超音波検査・X線で評価する。子宮蓄膿症ではCBC（白血球増多）・超音波、膣スメア細胞診、感染ではブルセラ等の血清・培養検査を行う。難産では胎子・産道評価を緊急に行う。",
    "toxicity": "{p}の診断は曝露歴の聴取が最も重要で、原因物質の特定を起点とする。CBC・生化学・血液ガス・電解質で臓器障害を評価し、特異的毒物では血中・尿中濃度測定や特異検査（コリンエステラーゼ活性等）を行う。摂取物・包装の確認と中毒管理センターへの照会が有用。",
    "trauma": "{p}の診断はプライマリーサーベイ（ABC）による全身状態評価を最優先とし、X線・FAST超音波・必要に応じCTで損傷部位を評価する。骨折では二方向撮影、内臓・胸腔損傷では超音波・X線、神経損傷では神経学的検査を行う。多発外傷では系統的な損傷検索が重要。",
    "autoimmune": "{p}の診断は除外診断（感染・腫瘍・薬剤性の除外）を前提に、CBC・血液塗抹、自己抗体検査（ANA・クームス）、罹患組織の生検・病理を組み合わせる。免疫介在性多発性関節炎では関節液検査、IMHA/ITPでは溶血・血小板減少の確認と二次性原因の検索を行う。",
    "nutritional": "{p}の診断は詳細な食餌歴の聴取を起点とし、欠乏・過剰栄養素を推定する。血液検査（カルシウム・リン・ビタミン濃度・総蛋白・アルブミン）、代謝性骨疾患ではX線で骨密度・病的骨折を評価する。飼育環境（UV-B・食餌組成）の評価が原因同定に不可欠。",
    "behavioral": "{p}の診断は詳細な行動歴・環境歴の聴取を中核とし、誘因・頻度・状況を評価する。まず疼痛・内分泌・神経疾患など医学的原因を血液検査・画像で除外し、その上で行動学的評価（恐怖・不安・葛藤の分類）を行う。飼育環境とヒト-動物関係の評価が治療計画の基盤となる。",
}

_DIAGNOSIS_EN: dict[str, str] = {
    "viral_infection": "Diagnosis of {p} begins with history (vaccination, exposure, course) and physical examination, with the virus identified by PCR, antigen testing or paired serology. CBC and biochemistry assess systemic status and organ injury, and imaging localises affected organs. Confirmation and exclusion of differentials guide treatment.",
    "bacterial_infection": "Diagnosis of {p} rests on history, physical examination and culture with sensitivity testing from the affected site. CBC (leukocytosis, left shift), biochemistry, inflammatory markers (CRP/SAA), Gram stain and cytology—plus PCR where needed—identify the organism. Sensitivity-guided antimicrobial selection is key to success.",
    "respiratory_infection": "Diagnosis of {p} combines assessment of respiratory signs and history with thoracic radiography (and CT where indicated) to evaluate lung lesions. Nasal/pharyngeal swabs or BAL undergo PCR and culture to identify the pathogen, while CBC and biochemistry assess systemic status. SpO2 and blood gas evaluate hypoxaemia.",
    "fungal_infection": "Diagnosis of {p} relies on cytology, fungal culture and KOH direct microscopy of lesions, with Wood's-lamp and hair examination for dermatophytosis. Systemic mycoses require antigen/antibody testing, imaging and tissue biopsy for confirmation. Antifungal susceptibility is considered in refractory or relapsing cases.",
    "parasitic": "Diagnosis of {p} uses tests matched to the parasite's location: faecal flotation, direct smear and antigen testing for gastrointestinal parasites; skin scraping, acetate-tape and hair examination for ectoparasites; and blood smear, antigen tests and imaging for haemo- or cardiovascular parasites. Identifying the species and life cycle underpins treatment and prevention.",
    "neoplasia": "Diagnosis of {p} starts with FNA cytology, with biopsy and histopathology required for confirmation. CBC and biochemistry, thoracic/abdominal radiography, ultrasonography and CT/MRI as needed evaluate the primary and metastasis, and staging includes cytology of regional lymph nodes. Tumour type and stage determine treatment and prognosis.",
    "endocrine_metabolic": "Diagnosis of {p} centres on hormonal and metabolic assays. Diabetes: glucose, glucosuria, fructosamine. Thyroid: T4, free T4, TSH. Hyperadrenocorticism: ACTH-stimulation and low-dose dexamethasone suppression testing. Electrolytes and blood gas assess metabolic status. As early disease is subclinical, periodic endocrine screening is useful.",
    "renal_urinary": "Diagnosis of {p} rests on urinalysis (specific gravity, protein, sediment) and bloodwork (creatinine, BUN, SDMA, phosphorus, potassium), with the urine protein:creatinine ratio and imaging (ultrasound, radiography) assessing morphology. Urine culture is used for infection and stone analysis for urolithiasis, with IRIS staging defining the stage.",
    "cardiac": "Diagnosis of {p} begins with auscultation (murmur, arrhythmia, gallop) and proceeds to thoracic radiography (cardiomegaly, pulmonary oedema), echocardiography (the mainstay of structural and functional assessment) and ECG (arrhythmia). NT-proBNP, troponin and blood pressure are adjuncts, and heart-failure staging guides management.",
    "respiratory_other": "Diagnosis of {p} uses thoracic radiography and CT where indicated to evaluate the airways and lung parenchyma, with bronchoscopy and bronchoalveolar lavage (BAL) for cytology and culture. Laryngeal/pharyngeal endoscopy is useful for upper airway obstruction and fluoroscopy (expiratory/inspiratory) for tracheal collapse. SpO2 and blood gas confirm ventilation and oxygenation.",
    "gastrointestinal": "Diagnosis of {p} begins with history, physical examination and abdominal palpation, supported by faecal testing, bloodwork and abdominal radiography/ultrasonography. Chronic or refractory cases warrant endoscopy with biopsy and digestive testing (cobalamin, folate, TLI). In acute abdomen, emergency imaging determines the need for surgery.",
    "neurological": "Diagnosis of {p} begins with a neurological examination to localise the lesion, with MRI (the first choice for brain and spinal cord) or CT for structure. Cerebrospinal fluid analysis differentiates inflammation, infection and neoplasia, while electrodiagnostics (EMG, nerve conduction) and muscle biopsy are used for peripheral nerve and muscle disease.",
    "ophthalmic": "Diagnosis of {p} rests on an ophthalmic examination (slit lamp, fundoscopy) with fluorescein staining (corneal ulcer), tonometry (glaucoma) and the Schirmer tear test (keratoconjunctivitis sicca). Fundoscopy and electroretinography (ERG) assess retinal disease, and ocular ultrasound evaluates intraocular structures.",
    "musculoskeletal": "Diagnosis of {p} begins with an orthopaedic examination (lameness assessment, palpation, range of motion) and radiography of bone and joint. CT/MRI, joint-fluid analysis (to distinguish septic from immune-mediated arthritis) and arthroscopy are used as needed. Specific-view radiography is used for developmental disease and culture for infection.",
    "dental": "Diagnosis of {p} begins with oral examination (teeth, gingiva, occlusion, mucosa) and dental radiography of roots and alveolar bone. In herbivores, cheek-tooth overgrowth, spurs and apical abscesses are assessed buccally and lingually, with skull radiography confirming root elongation and bone lysis. Examination under anaesthesia aids definitive diagnosis.",
    "dermatological": "Diagnosis of {p} begins with the lesion distribution, using skin scraping (scabies, demodicosis), hair examination and fungal culture (dermatophytosis), impression/scraping cytology (bacteria, Malassezia) and Wood's lamp. Allergy is approached by exclusion, diet trials and intradermal/serum IgE testing, with skin biopsy for refractory cases.",
    "hematological": "Diagnosis of {p} rests on CBC and blood smear (morphology), with reticulocyte count, iron indices and a Coombs test for anaemia, and platelet count and coagulation (PT/APTT, D-dimer) for bleeding tendency. Bone marrow examination, pathogen PCR/blood smear for infection, and imaging for splenomegaly or a bleeding source are used as needed.",
    "reproductive": "Diagnosis of {p} begins with history (oestrus, mating, parturition) and physical examination, with abdominal and reproductive-tract ultrasonography and radiography. Pyometra is assessed by CBC (leukocytosis) and ultrasound, vaginal cytology is used as indicated, and serology/culture (e.g. Brucella) for infection. Dystocia requires urgent fetal and birth-canal assessment.",
    "toxicity": "Diagnosis of {p} hinges on an exposure history to identify the toxicant. CBC, biochemistry, blood gas and electrolytes assess organ injury, and specific toxicants warrant blood/urine concentrations or targeted assays (e.g. cholinesterase activity). Inspection of the ingested material/packaging and consultation with a poison-control centre are valuable.",
    "trauma": "Diagnosis of {p} prioritises a primary survey (ABC) of overall status, with radiography, FAST ultrasound and CT as needed to evaluate injuries. Two-view radiography is used for fractures, ultrasound/radiography for visceral and thoracic injury, and a neurological examination for nerve injury. Systematic injury search is important in polytrauma.",
    "autoimmune": "Diagnosis of {p} requires exclusion of infection, neoplasia and drug reaction, combined with CBC and blood smear, autoantibody testing (ANA, Coombs) and biopsy/histopathology of affected tissue. Joint-fluid analysis is used for immune-mediated polyarthritis, and confirmation of haemolysis/thrombocytopenia with a search for secondary causes for IMHA/ITP.",
    "nutritional": "Diagnosis of {p} begins with a detailed dietary history to identify the deficient or excess nutrient. Bloodwork (calcium, phosphorus, vitamin levels, total protein, albumin) and—for metabolic bone disease—radiography of bone density and pathological fractures are used. Assessment of husbandry (UV-B, diet composition) is essential to identify the cause.",
    "behavioral": "Diagnosis of {p} centres on a detailed behavioural and environmental history assessing triggers, frequency and context. Medical causes (pain, endocrine, neurological disease) are first excluded with bloodwork and imaging, followed by behavioural assessment (classifying fear, anxiety and conflict). Evaluation of the environment and human-animal relationship underpins the treatment plan.",
}

_DIAGNOSIS_JA_GENERIC = "{p}の診断は病歴聴取と身体検査を起点に、CBC・生化学などの血液検査と画像検査（X線・超音波）で全身状態と罹患臓器を評価する。病態に応じた特異的検査（細胞診・培養・PCR・内視鏡・生検）で確定診断に至り、他疾患の除外を行う。早期診断が予後改善の鍵となる。"
_DIAGNOSIS_EN_GENERIC = "Diagnosis of {p} begins with history and physical examination, with bloodwork (CBC, biochemistry) and imaging (radiography, ultrasonography) assessing systemic status and the affected organs. Condition-specific testing (cytology, culture, PCR, endoscopy, biopsy) reaches a definitive diagnosis while excluding differentials. Early diagnosis is key to an improved outcome."


def gen_diagnosis_ja(category: str, name_ja: str, species: str) -> str:
    """Disease-specific Japanese diagnostic workup (replaces category templates)."""
    sp_ja = SPECIES_JA.get(species, species)
    p = _disease_prefix(name_ja, sp_ja)
    return _DIAGNOSIS_JA.get(category, _DIAGNOSIS_JA_GENERIC).format(p=p)


def gen_diagnosis(category: str, name_en: str, species: str) -> str:
    """Disease-specific English diagnostic workup (replaces category templates)."""
    sp_en = SPECIES_EN.get(species, species)
    p = _disease_prefix_en(name_en, sp_en)
    return _DIAGNOSIS_EN.get(category, _DIAGNOSIS_EN_GENERIC).format(p=p)


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


def _species_class(species: str) -> str:
    """Group a species into a husbandry class for species-appropriate guidance.

    Prevention advice for an exotic species must never borrow dog/cat-specific
    examples (DCM-predisposed breeds, puppy/kitten deworming schedules, indoor-cat
    confinement, monthly flea products). Each class gets husbandry guidance that
    actually applies to it.
    """
    if species in ("dog", "cat"):
        return "companion"
    if species == "horse":
        return "equine"
    if species in ("bird", "parakeet", "parrot"):
        return "avian"
    if species in ("reptile", "tortoise", "snake", "lizard"):
        return "reptile"
    if species == "amphibian":
        return "amphibian"
    if species == "fish":
        return "fish"
    # rabbit, hamster, guinea_pig, chinchilla, ferret, hedgehog, sugar_glider,
    # degu, exotic_other
    return "exotic_mammal"


# Husbandry foundation each non-companion class shares — the baseline that every
# prevention statement for that class rests on, free of dog/cat-specific advice.
_PREVENT_CLASS_CORE = {
    "equine": (
        "良質な粗飼料を中心とした給餌と計画的な飼料変更、十分な飲水と運動の確保、"
        "糞便検査に基づく計画的駆虫、定期的な装蹄と歯科ケア、コアワクチン接種（破傷風・日本脳炎・馬インフルエンザ）、"
        "衛生的な馬房環境の維持"
    ),
    "exotic_mammal": (
        "種に適した飼育環境（ケージサイズ・温湿度・床材・隠れ家）の整備、種特異的な栄養管理、"
        "ストレスの最小化、新規導入個体の検疫、定期的な健康診断"
    ),
    "avian": (
        "適切な飼育環境（ケージサイズ・止まり木・温度・換気）の確保、種子過多を避けたバランスの良いペレット主体の給餌、"
        "気道刺激物（タバコ煙・調理時の蒸気・エアロゾル）の回避、新規鳥の検疫、定期的な健康診断"
    ),
    "reptile": (
        "種特異的な適温域（POTZ）と温度勾配の維持、昼行性種への適切なUV-B照射、適切な湿度・基質・隠れ家の提供、"
        "カルシウム/ビタミンD3を考慮した給餌、新規個体の検疫"
    ),
    "amphibian": (
        "清潔な水質（脱塩素・適切なpHと水温）の維持、適切な湿度環境と隠れ家の確保、"
        "取り扱い時の濡れた清潔な手袋使用、新規個体の検疫"
    ),
    "fish": (
        "良好な水質管理（アンモニア・亜硝酸・硝酸塩・pH・水温の定期測定）、適切な濾過と計画的な水換え、"
        "新規魚の検疫とトリートメント、過密飼育と給餌過多の回避"
    ),
}


def _prevention_overlay(category: str, sp_class: str) -> str:
    """Category-specific prevention concern, written to apply to ``sp_class``.

    Returns a trailing sentence (or "") that refines the class husbandry core
    with the concern most relevant to the disease category for that class.
    """
    if category in ("viral_infection", "bacterial_infection", "respiratory_infection"):
        base = "感染個体との接触回避、器具・環境の消毒、検疫期間の遵守、過密と換気不良の改善が蔓延防止の鍵となる。"
        if sp_class == "avian":
            return base + "新規導入鳥はクラミジア・ポリオーマ・PBFDのスクリーニング後に合流させる。"
        if sp_class == "equine":
            return base + "輸送・競技でのストレスと鼻腔分泌物を介した伝播に留意し、発症馬は速やかに隔離する。"
        return base
    if category == "fungal_infection":
        return "過度な湿潤・結露を避けた清潔で乾燥した環境の維持、罹患個体の隔離、汚染した床材・器具の交換と消毒が中心となる。"
    if category == "parasitic":
        overlay = (
            "定期的な糞便・体表検査と結果に基づく適切な駆虫、媒介動物・中間宿主の制御、こまめな環境清掃が3本柱となる。"
        )
        if sp_class == "fish":
            return (
                "新規魚・水草・生餌の検疫と必要に応じた予防的薬浴、適切な水質維持により外部・内部寄生虫の侵入を防ぐ。"
            )
        if sp_class == "amphibian":
            return "新規個体・餌昆虫の検疫、水質と基質の清潔維持、こまめな糞便検査により寄生虫負荷を抑える。"
        return overlay
    if category == "neoplasia":
        return "確立された一次予防は限られるが、発癌性物質・過度な紫外線曝露の回避と定期的な健康診断による早期発見が中心となる。"
    if category in ("endocrine_metabolic", "nutritional"):
        if sp_class == "reptile":
            return "代謝性骨疾患・栄養障害の予防には種に応じたカルシウム/リン比とビタミンD3、適切なUV-B照射、多様な食餌の給与が要となる。"
        if sp_class == "avian":
            return "種子偏重による栄養障害・肥満を避け、ビタミンA・カルシウムを適正に含むペレット主体食へ段階的に移行する。"
        if sp_class == "fish":
            return "栄養性疾患の予防には種に適した良質な配合飼料の給与と過給・偏食の回避、ビタミン保持のための適切な飼料保管が重要となる。"
        if sp_class == "equine":
            return "代謝性疾患の予防には適正体重の維持、過剰な穀物・糖質の制限、放牧草の管理（蹄葉炎・EMS予防）が重要となる。"
        # exotic_mammal
        return (
            "種特異的な栄養要求を満たす給餌が要となる（草食性小動物は高繊維チモシー乾草を主体に、"
            "モルモットはビタミンCを継続補給、糖質過多を避ける）。"
        )
    if category == "musculoskeletal":
        if sp_class == "reptile":
            return "代謝性骨疾患の予防が中核で、適切なUV-B照射とカルシウム/D3補給、適温域維持が骨格の健全性を支える。"
        if sp_class == "equine":
            return "適切な装蹄と蹄管理、硬い馬場や過度な運動負荷の回避、計画的なウォームアップが運動器疾患の予防に重要となる。"
        if sp_class == "avian":
            return "適切な止まり木の太さ・材質、十分な飛翔運動、カルシウム充足によりバンブルフット・骨折・骨格異常を予防する。"
        return "安全な飼育環境（落下・挟み込みの防止）、適正体重の維持、種に応じたカルシウム・ビタミンD栄養の充足が予防の基本となる。"
    if category == "dental":
        if sp_class in ("exotic_mammal",):
            return "草食性小動物では高繊維チモシー乾草を主体に歯の自然摩耗を促し、定期的な歯科検診で不正咬合・過長歯を早期に発見する。"
        if sp_class == "avian":
            return "嘴の適切な摩耗のための硬質食材・カトルボーンの提供と、定期的な嘴の点検が予防に役立つ。"
        return "適切な食餌構成と定期的な口腔・咬合の点検により歯科疾患の進行を防ぐ。"
    if category == "gastrointestinal":
        if sp_class == "exotic_mammal":
            return "草食性小動物では高繊維食と十分な飲水で消化管うっ滞を予防し、急な食事変更・絶食・ストレスを避ける。"
        if sp_class == "equine":
            return "疝痛予防には規則的な給餌と十分な飲水、急な飼料変更の回避、計画的駆虫、砂の摂取防止が重要となる。"
        if sp_class == "fish":
            return (
                "消化器疾患の予防には適切な水温・水質の維持、良質な飼料の適量給与、過給と急な餌替えの回避が要となる。"
            )
        return "高品質な食餌の給与、急激な食事変更の回避、異物誤食の防止、清潔な飲食環境の維持が中心となる。"
    if category == "renal_urinary":
        return "十分な飲水の確保と適切なミネラルバランスの食餌、定期的な健康診断による腎機能・尿性状の早期評価が予防に役立つ。"
    if category == "cardiac":
        return "確立された一次予防は限られるが、適正体重の維持、定期的な健康診断による早期発見、基礎疾患の適切な管理が重要となる。"
    if category in ("respiratory_other",):
        if sp_class == "avian":
            return "気道刺激物（タバコ煙・テフロン加熱蒸気・エアロゾル・粉塵）の徹底回避と適切な換気・湿度管理が予防の要となる。"
        return "粉塵・刺激性ガス・アレルゲンへの曝露低減、適切な換気と湿度管理、適正体重の維持が予防に重要となる。"
    if category == "neurological":
        return "外傷の防止、中毒物質へのアクセス制限、感染症対策、適切な栄養管理により神経疾患の発症リスクを低減する。"
    if category == "ophthalmic":
        return "眼の外傷・刺激物からの保護、適切な飼育環境の衛生維持、初期の眼症状の早期受診が予防に役立つ。"
    if category == "dermatological":
        if sp_class == "fish":
            return "皮膚・鰭疾患の予防には良好な水質、傷つけない取り扱い、過密回避、新規個体の検疫が中心となる。"
        return (
            "適切な床材・基質と湿度管理、清潔な被毛・羽毛・皮膚の維持、外部寄生虫対策、外傷の防止が予防の基本となる。"
        )
    if category == "hematological":
        return "感染性・中毒性の原因への曝露回避と基礎疾患の管理、定期的な健康診断による早期発見が予防に役立つ。"
    if category == "reproductive":
        return (
            "計画的な繁殖管理、適切な栄養と分娩環境の整備、生殖器疾患の早期発見、必要に応じた避妊去勢が予防に寄与する。"
        )
    if category == "toxicity":
        return "有毒物質（植物・化学物質・重金属・医薬品）への接触防止と安全な保管、種特異的な毒性食材の排除が最も実効性ある予防策となる。"
    if category == "trauma":
        return "安全な飼育環境（鋭利物・落下・挟み込みの排除）、同居個体間の闘争管理、適切な取り扱いが外傷予防の中心となる。"
    if category == "autoimmune":
        return (
            "確立された予防法はないが、誘因と考えられる感染・薬剤・ストレスの管理と、早期発見・早期介入が重要となる。"
        )
    if category == "behavioral":
        return "適切な環境エンリッチメント、十分な運動・採食行動の機会、同居個体との適切な社会的環境、ストレス要因の除去が予防に重要となる。"
    return ""


def _prevention_noncompanion(category: str, prefix: str, sp_class: str) -> str:
    """Build species-class-appropriate prevention text (no dog/cat-specific advice)."""
    core = _PREVENT_CLASS_CORE.get(sp_class, _PREVENT_CLASS_CORE["exotic_mammal"])
    overlay = _prevention_overlay(category, sp_class)
    text = f"{prefix}の予防は、{core}が基本となる。"
    if overlay:
        text += overlay
    return text


def gen_prevention_ja(category: str, name_ja: str, species: str) -> str:
    sp_ja = SPECIES_JA.get(species, species)
    prefix = _disease_prefix(name_ja, sp_ja)

    sp_class = _species_class(species)
    if sp_class != "companion":
        # Exotic, avian, reptile, equine, amphibian and fish species must not
        # receive the dog/cat-specific examples baked into the branches below.
        return _prevention_noncompanion(category, prefix, sp_class)

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


# English mirror of _PREVENT_CLASS_CORE — husbandry prevention core per species
# class, free of dog/cat-specific advice. Used to regenerate contaminated
# non-companion English prevention (see gen_prevention_en_noncompanion).
_PREVENT_CLASS_CORE_EN = {
    "equine": (
        "feeding built around good-quality forage with gradual ration changes, adequate water and turnout, "
        "a planned deworming programme guided by faecal egg counts, regular farriery and dental care, "
        "core vaccination (tetanus, Japanese encephalitis, equine influenza) and a clean stable environment"
    ),
    "exotic_mammal": (
        "a species-appropriate enclosure (cage size, temperature and humidity, substrate, hiding places), "
        "species-specific nutrition, minimised stress, quarantine of new arrivals and regular health checks"
    ),
    "avian": (
        "an appropriate enclosure (cage size, perches, temperature, ventilation), a balanced pellet-based diet "
        "rather than an all-seed diet, avoidance of airway irritants (tobacco smoke, cooking fumes, aerosols), "
        "quarantine of new birds and regular health checks"
    ),
    "reptile": (
        "a species-specific preferred optimum temperature zone (POTZ) with a thermal gradient, appropriate UV-B "
        "for diurnal species, adequate humidity, substrate and hides, calcium/vitamin-D3-conscious feeding, "
        "and quarantine of new animals"
    ),
    "amphibian": (
        "clean water quality (dechlorinated, appropriate pH and temperature), an adequately humid environment "
        "with hiding places, use of wet clean gloves when handling, and quarantine of new animals"
    ),
    "fish": (
        "good water-quality management (regular testing of ammonia, nitrite, nitrate, pH and temperature), "
        "adequate filtration and planned water changes, quarantine and treatment of new fish, and avoidance of "
        "overstocking and overfeeding"
    ),
}


def _prevention_overlay_en(category: str, sp_class: str) -> str:
    """English mirror of _prevention_overlay — class-appropriate category concern."""
    if category in ("viral_infection", "bacterial_infection", "respiratory_infection"):
        base = (
            " Avoiding contact with infected animals, disinfecting equipment and the environment, observing "
            "quarantine periods, and improving crowding and ventilation are key to limiting spread."
        )
        if sp_class == "avian":
            return base + " Screen new birds for chlamydiosis, polyomavirus and PBFD before introducing them."
        if sp_class == "equine":
            return (
                base
                + " Note transport- and competition-related stress and nasal-secretion spread, and isolate affected horses promptly."
            )
        return base
    if category == "fungal_infection":
        return (
            " Maintaining a clean, dry environment free of excess moisture and condensation, isolating affected "
            "animals, and replacing and disinfecting contaminated bedding and equipment are central."
        )
    if category == "parasitic":
        if sp_class == "fish":
            return (
                " Quarantine and, where appropriate, prophylactic baths for new fish, plants and live food, together "
                "with good water quality, prevent introduction of external and internal parasites."
            )
        if sp_class == "amphibian":
            return (
                " Quarantine of new animals and feeder insects, clean water and substrate, and frequent faecal checks "
                "keep parasite burdens low."
            )
        return (
            " Regular faecal and skin examinations with treatment guided by the results, control of vectors and "
            "intermediate hosts, and frequent environmental cleaning are the three pillars."
        )
    if category == "neoplasia":
        return (
            " Established primary prevention is limited, but avoiding carcinogens and excess UV exposure and "
            "detecting tumours early through regular health checks are central."
        )
    if category in ("endocrine_metabolic", "nutritional"):
        if sp_class == "reptile":
            return (
                " Preventing metabolic bone disease and nutritional disorders requires a species-appropriate "
                "calcium/phosphorus ratio and vitamin D3, adequate UV-B, and a varied diet."
            )
        if sp_class == "avian":
            return (
                " Avoid seed-heavy diets that cause nutritional disease and obesity, transitioning gradually to a "
                "pelleted diet with appropriate vitamin A and calcium."
            )
        if sp_class == "fish":
            return (
                " Prevention rests on a good species-appropriate formulated feed, avoidance of overfeeding and "
                "selective feeding, and proper feed storage to preserve vitamins."
            )
        if sp_class == "equine":
            return (
                " Prevention rests on maintaining an appropriate body weight, restricting excess grain and sugar, and "
                "managing pasture (to prevent laminitis and equine metabolic syndrome)."
            )
        return (
            " Feeding to meet species-specific nutritional requirements is central (herbivorous small mammals on "
            "mostly high-fibre timothy hay, guinea pigs with continuous vitamin C, avoiding excess sugar)."
        )
    if category == "musculoskeletal":
        if sp_class == "reptile":
            return (
                " Preventing metabolic bone disease is central: appropriate UV-B, calcium/D3 supplementation and a "
                "correct thermal range support skeletal health."
            )
        if sp_class == "equine":
            return (
                " Appropriate farriery and hoof care, avoidance of hard footing and excessive workloads, and planned "
                "warm-up are important for preventing musculoskeletal disease."
            )
        if sp_class == "avian":
            return (
                " Appropriate perch diameter and material, adequate flight exercise and calcium sufficiency prevent "
                "bumblefoot, fractures and skeletal abnormalities."
            )
        return (
            " A safe enclosure (preventing falls and entrapment), maintenance of appropriate body weight, and "
            "species-appropriate calcium and vitamin-D nutrition are the basis of prevention."
        )
    if category == "dental":
        if sp_class == "exotic_mammal":
            return (
                " In herbivorous small mammals, a mostly high-fibre timothy-hay diet promotes natural tooth wear, and "
                "regular dental checks detect malocclusion and overgrowth early."
            )
        if sp_class == "avian":
            return " Providing hard foods and a cuttlebone for proper beak wear and regular beak inspection help prevention."
        return " Appropriate diet composition and regular oral and occlusal inspection limit progression of dental disease."
    if category == "gastrointestinal":
        if sp_class == "exotic_mammal":
            return (
                " In herbivorous small mammals, a high-fibre diet and adequate water intake prevent gastrointestinal "
                "stasis; avoid abrupt diet changes, fasting and stress."
            )
        if sp_class == "equine":
            return (
                " Colic prevention rests on regular feeding and adequate water, avoiding abrupt feed changes, planned "
                "deworming, and preventing sand ingestion."
            )
        if sp_class == "fish":
            return (
                " Prevention of digestive disease rests on appropriate water temperature and quality, feeding a good "
                "diet in appropriate amounts, and avoiding overfeeding and abrupt diet changes."
            )
        return (
            " Feeding a high-quality diet, avoiding abrupt diet changes, preventing foreign-body ingestion, and "
            "maintaining a clean feeding environment are central."
        )
    if category == "renal_urinary":
        return (
            " Ensuring adequate water intake, an appropriate mineral balance in the diet, and early evaluation of "
            "renal function and urine quality through regular health checks aid prevention."
        )
    if category == "cardiac":
        return (
            " Established primary prevention is limited, but maintaining appropriate body weight, early detection "
            "through regular health checks, and proper management of underlying disease are important."
        )
    if category in ("respiratory_other",):
        if sp_class == "avian":
            return (
                " Strict avoidance of airway irritants (tobacco smoke, overheated PTFE fumes, aerosols, dust) and "
                "appropriate ventilation and humidity are the keys to prevention."
            )
        return (
            " Reducing exposure to dust, irritant gases and allergens, appropriate ventilation and humidity control, "
            "and maintaining appropriate body weight are important for prevention."
        )
    if category == "neurological":
        return (
            " Preventing trauma, restricting access to toxic substances, controlling infectious disease, and "
            "appropriate nutrition reduce the risk of neurological disease."
        )
    if category == "ophthalmic":
        return (
            " Protecting the eyes from trauma and irritants, maintaining a clean enclosure, and seeking early care "
            "for initial ocular signs aid prevention."
        )
    if category == "dermatological":
        if sp_class == "fish":
            return (
                " Prevention of skin and fin disease rests on good water quality, gentle handling, avoidance of "
                "overstocking, and quarantine of new animals."
            )
        return (
            " Appropriate substrate and humidity management, a clean coat, feathers or skin, ectoparasite control, and "
            "prevention of trauma are the basis of prevention."
        )
    if category == "hematological":
        return (
            " Avoiding infectious and toxic causes, managing underlying disease, and early detection through regular "
            "health checks aid prevention."
        )
    if category == "reproductive":
        return (
            " Planned breeding management, appropriate nutrition and a suitable birthing environment, early detection "
            "of reproductive disease, and neutering where appropriate contribute to prevention."
        )
    if category == "toxicity":
        return (
            " Preventing access to toxic substances (plants, chemicals, heavy metals, medicines) with safe storage, "
            "and removing species-specific toxic foods, are the most effective preventive measures."
        )
    if category == "trauma":
        return (
            " A safe enclosure (removing sharp objects, fall and entrapment hazards), managing conflict between "
            "cohabiting animals, and appropriate handling are central to preventing trauma."
        )
    if category == "autoimmune":
        return (
            " There is no established prevention, but managing suspected triggers (infection, drugs, stress) and "
            "early detection and intervention are important."
        )
    if category == "behavioral":
        return (
            " Appropriate environmental enrichment, adequate exercise and foraging opportunities, a suitable social "
            "environment with cohabitants, and removal of stressors are important for prevention."
        )
    return ""


def gen_prevention_en_noncompanion(category: str, name_en: str, species: str) -> str:
    """Species-class-appropriate English prevention for non-companion species.

    English mirror of the non-companion path of gen_prevention_ja. Used only to
    regenerate contaminated non-companion English prevention in the served-DB
    build; the dog/cat (companion) English path is untouched.
    """
    sp_en = SPECIES_EN.get(species, species)
    prefix = _disease_prefix_en(name_en, sp_en)
    sp_class = _species_class(species)
    core = _PREVENT_CLASS_CORE_EN.get(sp_class, _PREVENT_CLASS_CORE_EN["exotic_mammal"])
    text = f"Prevention of {prefix} rests on {core}."
    overlay = _prevention_overlay_en(category, sp_class)
    if overlay:
        text += overlay
    return text


def _neoplasia_subtype(name_ja: str) -> str:
    """Classify a tumour from its Japanese name into a prognostic subtype.

    Order matters: malignant suffixes (肉腫 / 癌) must be tested before the
    benign ones (腫) because e.g. 血管肉腫 contains 腫 and 骨肉腫 contains 腫.
    """
    n = name_ja or ""
    if "良性" in n:
        return "benign"
    if any(k in n for k in ("リンパ腫", "リンパ肉腫", "白血病", "骨髄腫", "形質細胞腫")):
        return "lymphoid"
    if "肥満細胞腫" in n:
        return "mast_cell"
    if any(k in n for k in ("黒色腫", "メラノーマ")):
        return "melanoma"
    if "肉腫" in n:  # 血管肉腫・骨肉腫・線維肉腫・軟骨肉腫・横紋筋肉腫…
        return "sarcoma"
    if "癌" in n or "carcinoma" in n.lower():  # 腺癌・扁平上皮癌・移行上皮癌…
        return "carcinoma"
    # A generic "<organ>腫瘍" / "tumour" name is unspecified: classify it as such
    # *before* the benign check so e.g. 甲状腺腫瘍 / 乳腺腫瘍 are not mis-read as
    # adenomas via the spurious 腺腫 substring (甲状[腺腫]瘍).
    if "腫瘍" in n or "新生物" in n or "tumor" in n.lower() or "neoplas" in n.lower():
        return "unspecified"
    # Benign neoplasms: adenoma(腺腫)/lipoma(脂肪腫)/papilloma(乳頭腫)/cyst(嚢胞)…
    if any(
        k in n
        for k in (
            "脂肪腫",
            "腺腫",
            "乳頭腫",
            "嚢胞",
            "組織球腫",
            "線維腫",
            "血管腫",
            "平滑筋腫",
            "軟骨腫",
            "ポリープ",
            "母斑",
            "色素細胞腫",
        )
    ):
        return "benign"
    return "unspecified"


_NEOPLASIA_PROGNOSIS: dict[str, str] = {
    "benign": (
        "は良性腫瘍で、外科的完全切除により治癒が期待でき予後は良好。"
        "切除困難な部位・高齢・基礎疾患で麻酔リスクが高い場合は経過観察も選択肢となる。"
        "不完全切除では局所再発がありうるため切除マージンの病理評価が望ましい。"
        "急速な増大・出血・潰瘍化を認める場合は悪性転化を疑い再評価する。"
    ),
    "lymphoid": (
        "は全身性に進展する造血器腫瘍であり外科的治癒は困難。"
        "多剤併用化学療法（CHOP系等）が治療の主体で、寛解導入により生存期間の延長が期待できる。"
        "完全寛解率・寛解期間・生存期間は病型・免疫表現型（B/T細胞）・臨床ステージにより異なる。"
        "再発例では救援プロトコルを検討する。猫ではFeLV/FIV感染が予後を悪化させる。"
        "無治療では進行性で予後不良。"
    ),
    "mast_cell": (
        "の予後は組織学的グレード（Patnaik/Kiupel分類）・c-kit変異・臨床ステージにより層別化される。"
        "低悪性度・完全切除例は予後良好。"
        "高悪性度・転移例では予後不良で、外科＋放射線±チロシンキナーゼ阻害薬（トセラニブ等）の集学的治療を要する。"
        "脱顆粒による全身症状（胃十二指腸潰瘍・凝固異常）の管理も予後に影響する。"
    ),
    "melanoma": (
        "の予後は発生部位と組織学的悪性度に強く依存する。"
        "口腔・爪床メラノーマは悪性度が高く転移率が高い一方、皮膚（被毛部）メラノーマの多くは良性挙動を示す。"
        "外科的広範切除が基本で、悪性例では所属リンパ節・遠隔転移評価と補助療法（放射線・免疫療法）を検討する。"
    ),
    "carcinoma": (
        "は上皮性悪性腫瘍で、臨床ステージ・組織学的グレード・切除マージン・転移の有無が予後を規定する。"
        "早期・限局例は外科的広範切除で良好な予後が得られるが、浸潤・転移例では予後不良。"
        "完全切除が難しい部位では放射線療法・化学療法を併用する集学的治療を検討する。"
    ),
    "sarcoma": (
        "は間葉系悪性腫瘍で、局所浸潤性が高く広範切除でも局所再発しやすい。"
        "組織学的グレードと切除マージンが予後を左右し、不完全切除例では放射線療法の追加が再発抑制に有効。"
        "高悪性度・転移例（特に血管肉腫）は予後不良で、化学療法の併用を検討する。"
    ),
    "unspecified": (
        "の予後は組織型・悪性度・臨床ステージ・転移の有無・治療反応性により大きく異なる。"
        "確定診断（細胞診・病理組織検査）と病期診断（画像・所属リンパ節評価）に基づき、"
        "外科・化学療法・放射線療法を組み合わせた治療方針を決定する。"
        "早期診断・早期介入が予後改善の鍵となる。"
    ),
}


# Enumerated-catalog categories: instead of dumping every sub-disease's
# prognosis on every member (a "textbook chapter" that reads as generic
# template content), pick the clause whose keywords match THIS disease's name.
# Each entry is (keywords, clause-without-prefix). Clause text is reused from
# the previously vetted category catalogue, so no new medical claim is made —
# only the relevant statement is selected. ``None`` keywords = category lead.
_PROGNOSIS_CATALOG: dict[str, tuple[tuple[tuple[str, ...], str], ...]] = {
    "endocrine_metabolic": (
        (
            ("糖尿", "diabet"),
            "の予後は早期診断・適切なインスリン療法・食事管理により管理可能で、猫では20-40%が寛解を達成しうる。",
        ),
        (
            ("甲状腺機能亢進", "hyperthyroid"),
            "の予後はI-131治療で治癒可能（猫95%以上）、メチマゾール内服でも長期管理良好。",
        ),
        (
            ("甲状腺機能低下", "hypothyroid"),
            "の予後はレボチロキシン補充により良好で、適切な用量調整で寿命に近い予後が期待できる。",
        ),
        (
            ("クッシング", "副腎皮質機能亢進", "cushing"),
            "の予後はトリロスタン・ミトタンによる症状制御で中央生存2年以上が期待できる。",
        ),
        (
            ("アジソン", "副腎皮質機能低下", "addison"),
            "の予後は適切な鉱質・糖質コルチコイド補充療法により寿命に近い良好な予後。",
        ),
        (
            ("インスリノーマ", "insulinoma"),
            "の予後は外科的切除で無症状期間の延長が可能だが、多くは進行性で内科管理（プレドニゾロン・ジアゾキシド）を要する。",
        ),
        (
            ("上皮小体", "副甲状腺", "parathyroid"),
            "の予後は原因（原発性・腎性・栄養性）により異なり、原因是正とカルシウム・リン管理で多くは改善する。",
        ),
    ),
    "renal_urinary": (
        (
            ("慢性腎", "CKD", "腎不全"),
            "の予後はIRISステージと進行速度により異なり、早期（ステージ2）は腎臓食・降圧・低リン療法で中央生存3年以上、進行例（ステージ3-4）は数週〜2年。",
        ),
        (("急性腎", "AKI"), "の予後は原因除去と早期介入により可逆性があり、乏尿・無尿の遷延例では予後不良。"),
        (
            ("膀胱炎", "FLUTD", "FIC", "特発性膀胱"),
            "の予後は自然寛解率が約50%だが再発も多く、ストレス・環境・飲水管理で長期予後が改善する。",
        ),
        (
            ("尿石", "結石", "urolith"),
            "の予後は結石組成に応じた溶解食・外科的摘出で良好だが、食事・飲水管理を怠ると再発する。",
        ),
        (
            ("尿路感染", "膀胱感染", "UTI"),
            "の予後は培養感受性に基づく適切な抗菌薬で治癒率が高く、基礎疾患の管理が再発予防の鍵。",
        ),
        (
            ("尿閉", "尿道閉塞", "obstruction"),
            "の予後は閉塞解除の迅速さに依存し、緊急対応で良好、遅延例では急性腎障害・高K血症で致死的となりうる。",
        ),
    ),
    "cardiac": (
        (
            ("肥大型心筋症", "HCM"),
            "の予後は症状発現後の中央生存が約1.3年（猫）で、動脈血栓塞栓症（FATE）の併発が予後を悪化させる。",
        ),
        (("拡張型心筋症", "DCM"), "の予後は基礎疾患として予後不良で、特にドーベルマンでは突然死リスクが高い。"),
        (
            ("僧帽弁", "弁膜症", "粘液腫様"),
            "の予後は代償期は数年以上良好だが、心不全発症後はACE阻害薬・利尿薬・ピモベンダンで中央生存1-2年程度。",
        ),
        (("動脈血栓", "FATE", "血栓塞栓"), "の予後は急性期生存率が約30-50%と低く、再発予防（抗血栓療法）が重要。"),
        (
            ("動脈管開存", "心室中隔", "心房中隔", "ファロー", "先天性心"),
            "の予後は欠損の種類・大きさによるが、早期の外科的・カテーテル治療で良好となりうる。",
        ),
        (("心不全", "うっ血"), "の予後は進行度により異なり、早期は薬物療法で1-2年以上、末期は数ヶ月。"),
    ),
    "respiratory_other": (
        (("短頭種", "軟口蓋"), "の予後は外科的気道形成術（軟口蓋切除・鼻孔形成）で良好。"),
        (
            ("気管虚脱",),
            "の予後は内科的管理（鎮咳・抗炎症・体重管理）で長期管理可能、重度例では気管ステントを検討する。",
        ),
        (("喉頭麻痺",), "の予後は片側披裂軟骨側方化術で良好。"),
        (("喘息", "気管支"), "の予後は適切なステロイド・気管支拡張薬とアレルゲン回避により長期管理可能。"),
        (
            ("肺炎", "誤嚥"),
            "の予後は原因と重症度により異なり、早期の抗菌薬・支持療法で多くは回復するが、重症例は予後注意。",
        ),
        (("肺水腫", "胸水", "膿胸", "気胸"), "の予後は原因疾患の管理と排液・酸素療法により左右される。"),
    ),
    "gastrointestinal": (
        (("拡張", "捻転", "GDV", "鼓脹"), "の予後は早期手術で生存率80%以上、診断・整復の遅延で急速に悪化する。"),
        (
            ("うっ滞", "stasis", "イレウス", "鼓腸"),
            "の予後は早期介入で良好だが、草食動物では遷延すると致死的となりうる。",
        ),
        (("炎症性腸", "IBD"), "の予後は食事療法・免疫抑制療法で長期管理可能だが、生涯治療を要することが多い。"),
        (
            ("リンパ腫", "腺癌", "消化器腫瘍"),
            "の予後は組織型により異なり、リンパ腫は化学療法で寛解可能だが腺癌・肉腫は予後不良。",
        ),
        (("膵炎",), "の予後は軽症例は支持療法で良好だが、重症・壊死性では全身性合併症により予後不良となりうる。"),
        (
            ("巨大結腸", "便秘", "宿便"),
            "の予後は内科管理（食事・緩下剤・摘便）で管理可能だが、難治例では外科的結腸亜全摘を検討する。",
        ),
        (
            ("肝", "胆管", "胆嚢"),
            "の予後は基礎病態と肝予備能により異なり、早期介入で可逆的だが線維化進行例は予後注意。",
        ),
    ),
    "neurological": (
        (
            ("てんかん", "発作", "痙攣"),
            "の予後は抗てんかん薬による発作管理で多くは寿命に近い予後だが、難治性では生活の質の低下を伴う。",
        ),
        (
            ("椎間板", "IVDD", "脊髄"),
            "の予後は神経学的重症度により異なり、深部痛覚が温存されていれば外科的予後良好、消失例は予後不良。",
        ),
        (("脳炎", "髄膜"), "の予後は病因により異なり、自己免疫性は免疫抑制で寛解可能、感染性は病原体により異なる。"),
        (("脳腫瘍", "腫瘍"), "の予後は外科切除・放射線療法で延命可能だが、部位・組織型により制限される。"),
        (
            ("認知機能", "認知症"),
            "の予後は進行性だが、薬物・サプリメント・環境エンリッチメントで進行遅延とQOL改善が可能。",
        ),
        (("前庭", "斜頸"), "の予後は末梢性（特発性）は数週で改善することが多く良好、中枢性は原因により異なる。"),
        (("水頭症",), "の予後は重症度により異なり、内科的減圧・外科的シャント術で管理しうる。"),
    ),
    "ophthalmic": (
        (
            ("角膜潰瘍", "角膜"),
            "の予後は早期治療で良好だが、感染性深層潰瘍は穿孔リスクがあり眼科専門医への紹介を要する。",
        ),
        (("白内障",), "の予後は外科的水晶体乳化吸引術で視力回復が可能。"),
        (("緑内障",), "の予後は急性期治療で視覚温存が可能だが、慢性期は視覚消失が多く義眼・眼球摘出となる。"),
        (("網膜",), "の予後は早期復位・原因治療で視覚温存が可能な場合がある。"),
        (("ぶどう膜炎", "虹彩"), "の予後は基礎疾患の治療により決定される。"),
        (("結膜炎", "眼瞼", "流涙"), "の予後は原因に応じた治療で概ね良好。"),
    ),
    "musculoskeletal": (
        (("骨折",), "の予後は部位・粉砕度に応じた整復・固定で良好だが、開放骨折・感染併発例は治癒が遷延する。"),
        (
            ("変形性関節", "OA", "関節症"),
            "の予後は進行性だが、体重管理・運動療法・NSAID・関節保護で長期に良好なQOLを維持しうる。",
        ),
        (("十字靭帯", "靭帯", "膝蓋骨"), "の予後は外科的整復（TPLO・TTA・側方制動術）で良好。"),
        (("股関節形成", "肘異形成", "発達性"), "の予後は軽度は内科管理、重度は外科介入（人工股関節等）で改善する。"),
        (("椎間板", "脊椎"), "の予後は神経学的重症度と治療時期により決定される。"),
        (("骨髄炎", "感染"), "の予後は起因菌に応じた長期抗菌薬と外科的デブリードマンで管理する。"),
    ),
    "dermatological": (
        (("アトピー", "アレルギー"), "の予後は根治は困難だが、環境・薬物・減感作療法による長期管理で症状制御が可能。"),
        (("膿皮症", "細菌"), "の予後は適切な抗菌薬で良好、基礎疾患の管理が再発予防の鍵。"),
        (("皮膚糸状菌", "真菌"), "の予後は抗真菌薬で治癒可能（通常4-12週）。"),
        (("天疱瘡", "自己免疫", "エリテマトーデス"), "の予後は免疫抑制療法で寛解可能だが、長期維持療法を要する。"),
        (
            ("疥癬", "ニキビダニ", "毛包虫", "ダニ", "寄生"),
            "の予後は適切な駆虫薬で良好だが、基礎免疫状態が経過に影響する。",
        ),
        (("膿瘍", "蜂窩織"), "の予後は排膿・洗浄と抗菌薬で良好。"),
    ),
    "hematological": (
        (
            ("免疫介在性溶血", "IMHA", "自己免疫性溶血"),
            "の予後は急性期死亡率20-50%だが、免疫抑制療法に反応した長期生存例は良好。",
        ),
        (("血小板減少", "IMTP", "ITP"), "の予後は適切な免疫抑制療法で多くは良好。"),
        (("貧血",), "の予後は基礎疾患（FeLV・FIV・CKD・出血等）により左右される。"),
        (("失血", "出血"), "の予後は早期止血と輸血で生存可能。"),
        (("凝固", "DIC", "血友病"), "の予後は原因（抗凝固殺鼠剤中毒・肝不全・DIC）により異なる。"),
    ),
    "reproductive": (
        (("子宮蓄膿", "子宮蓄膿症", "pyometra"), "の予後は卵巣子宮全摘術で良好、早期診断が鍵。"),
        (("乳腺炎",), "の予後は抗菌薬・支持療法で良好。"),
        (("難産", "帝王切開"), "の予後は早期診断（必要時は緊急帝王切開）で母子ともに良好。"),
        (("子癇", "妊娠中毒", "周産期"), "の予後は早期治療で良好、遅延で致死的となりうる。"),
        (("前立腺",), "の予後は良性過形成は去勢で良好、前立腺癌は診断時進行例が多く予後不良。"),
        (("乳腺腫瘍", "乳腺腫"), "の予後は早期完全切除で良好、悪性度に応じて化学療法を併用する。"),
        (("精巣", "卵巣", "停留"), "の予後は外科的摘出で良好。"),
    ),
    "dental": (
        (("歯周",), "の予後は早期スケーリングと適切な口腔ケアで進行を抑制できる。"),
        (("歯根膿瘍", "根尖"), "の予後は抜歯・根管治療で治癒可能。"),
        (("不正咬合", "過長歯"), "の予後は定期的歯科処置（4-6週毎）で長期管理可能だが、咬合の根本的矯正は困難。"),
        (("口腔腫瘍", "扁平上皮"), "の予後は良性は完全切除で治癒、悪性（扁平上皮癌等）は予後不良。"),
        (("吸収病巣", "破歯細胞"), "の予後は罹患歯の抜歯により疼痛は解消するが、進行を止める内科治療はない。"),
    ),
}


# Category-specific prognostic determinants for the no-keyword-match fallback,
# so the general statement reflects the organ system rather than reading
# identically across cardiac / GI / musculoskeletal / etc.
_CATALOG_FALLBACK: dict[str, str] = {
    "endocrine_metabolic": "ホルモン・代謝異常の種類と是正の可否、合併症の有無",
    "renal_urinary": "腎機能・尿路病変の重症度と進行速度",
    "cardiac": "基礎心疾患の種類と心不全の進行度",
    "respiratory_other": "気道・肺病変の部位と重症度、基礎疾患",
    "gastrointestinal": "原因病態・脱水と電解質異常の程度・治療開始時期",
    "neurological": "病因と神経学的重症度（特に深部痛覚の有無）",
    "ophthalmic": "病変の部位・進行度と治療開始時期、視覚温存の可否",
    "musculoskeletal": "罹患部位・損傷の重症度と治療法",
    "dental": "病変の進行度と早期介入の可否",
    "dermatological": "原因（アレルギー性・感染性・自己免疫性）と慢性度",
    "hematological": "基礎病態と貧血・出血・凝固異常の重症度",
    "reproductive": "病態と治療時期、緊急性の有無",
}


def gen_prognosis_ja(category: str, name_ja: str, species: str) -> str:
    sp_ja = SPECIES_JA.get(species, species)
    prefix = _disease_prefix(name_ja, sp_ja)

    if category == "neoplasia":
        subtype = _neoplasia_subtype(name_ja)
        return prefix + _NEOPLASIA_PROGNOSIS[subtype]

    catalog = _PROGNOSIS_CATALOG.get(category)
    if catalog:
        name_l = (name_ja or "").lower()
        for keywords, clause in catalog:
            if any(k.lower() in name_l for k in keywords):
                return prefix + clause
        # No sub-type keyword matched: emit a concise, honest statement framed by
        # the *category's* key prognostic determinants (so a navicular case reads
        # differently from an arrhythmia) rather than dumping the full catalogue.
        lead = _CATALOG_FALLBACK.get(category, "基礎病態・重症度・治療開始時期")
        return (
            f"{prefix}の予後は{lead}により異なる。"
            f"早期診断と病態に応じた適切な治療・モニタリングにより多くの症例で良好な経過が期待できるが、"
            f"進行例・合併症を伴う例では予後が悪化しうる。"
        )

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


def _neoplasia_subtype_en(name_en: str) -> str:
    """English-name counterpart of ``_neoplasia_subtype``."""
    n = (name_en or "").lower()
    if "benign" in n:
        return "benign"
    if any(k in n for k in ("lymphoma", "leukemia", "leukaemia", "myeloma", "plasmacytoma", "lymphosarcoma")):
        return "lymphoid"
    if "mast cell" in n or "mastocytoma" in n:
        return "mast_cell"
    if "melanoma" in n:
        return "melanoma"
    if "sarcoma" in n:
        return "sarcoma"
    if "carcinoma" in n:
        return "carcinoma"
    if any(k in n for k in ("tumor", "tumour", "neoplas", "mass", "cancer")):
        return "unspecified"
    if any(
        k in n for k in ("adenoma", "lipoma", "papilloma", "cyst", "histiocytoma", "fibroma", "hemangioma", "polyp")
    ):
        return "benign"
    return "unspecified"


_NEOPLASIA_PROGNOSIS_EN: dict[str, str] = {
    "benign": (
        " is a benign neoplasm: complete surgical excision is usually curative and the prognosis is good. "
        "Observation is reasonable when the location, age or comorbidities make anaesthesia high-risk. "
        "Incomplete excision can recur locally, so histopathological margin assessment is advised, and "
        "rapid enlargement, ulceration or bleeding warrants re-evaluation for malignant transformation."
    ),
    "lymphoid": (
        " is a systemic haematopoietic malignancy that is not cured by surgery. "
        "Multi-agent chemotherapy (CHOP-based protocols) is the mainstay; remission induction can extend survival. "
        "Remission rate, remission duration and survival vary with subtype, immunophenotype (B/T cell) and clinical stage. "
        "Rescue protocols are considered at relapse, and FeLV/FIV co-infection worsens the prognosis in cats. "
        "Untreated disease is progressive with a poor outcome."
    ),
    "mast_cell": (
        " carries a prognosis stratified by histological grade (Patnaik/Kiupel), c-kit mutation status and clinical stage. "
        "Low-grade, completely excised tumours have a good prognosis. "
        "High-grade or metastatic disease has a guarded prognosis and warrants multimodal therapy "
        "(surgery + radiation ± tyrosine-kinase inhibitors such as toceranib). "
        "Management of degranulation-related systemic signs (gastroduodenal ulceration) also affects outcome."
    ),
    "melanoma": (
        " has a prognosis that depends strongly on anatomic site and histological grade. "
        "Oral and subungual melanomas are highly malignant with a high metastatic rate, whereas most haired-skin "
        "melanomas behave benignly. Wide surgical excision is the basis of treatment, and malignant cases warrant "
        "regional lymph-node and distant-metastasis staging with adjunctive therapy (radiation, immunotherapy)."
    ),
    "carcinoma": (
        " is an epithelial malignancy whose prognosis is governed by clinical stage, histological grade, surgical "
        "margins and the presence of metastasis. Early, localised disease can do well after wide excision, while "
        "invasive or metastatic disease carries a poor prognosis. Where complete excision is not feasible, multimodal "
        "therapy combining radiation and chemotherapy is considered."
    ),
    "sarcoma": (
        " is a mesenchymal malignancy that is locally invasive and prone to local recurrence even after wide excision. "
        "Histological grade and surgical margins drive the prognosis; adjunctive radiation reduces recurrence after "
        "incomplete excision. High-grade or metastatic disease (notably haemangiosarcoma) has a poor prognosis and "
        "chemotherapy is considered."
    ),
    "unspecified": (
        " has a prognosis that varies widely with tumour type, grade, clinical stage, presence of metastasis and "
        "treatment response. A definitive diagnosis (cytology, histopathology) and staging (imaging, regional "
        "lymph-node assessment) guide a treatment plan combining surgery, chemotherapy and radiation. "
        "Early diagnosis and intervention are key to an improved outcome."
    ),
}


_PROGNOSIS_CATALOG_EN: dict[str, tuple[tuple[tuple[str, ...], str], ...]] = {
    "endocrine_metabolic": (
        (
            ("diabet",),
            "'s prognosis is favourable with early diagnosis, appropriate insulin therapy and dietary management; up to 20-40% of cats achieve remission.",
        ),
        (
            ("hyperthyroid",),
            "'s prognosis is excellent — I-131 is curative in over 95% of cats and methimazole gives good long-term control.",
        ),
        (
            ("hypothyroid",),
            "'s prognosis is good with levothyroxine supplementation and dose titration, approaching a normal lifespan.",
        ),
        (
            ("cushing", "hyperadrenocortic"),
            "'s prognosis is reasonable, with trilostane or mitotane control giving median survival over 2 years.",
        ),
        (
            ("addison", "hypoadrenocortic"),
            "'s prognosis is excellent with appropriate mineralocorticoid/glucocorticoid replacement, approaching a normal lifespan.",
        ),
        (
            ("insulinoma",),
            "'s prognosis is improved by surgery, but most cases are progressive and require medical management (prednisolone, diazoxide).",
        ),
        (
            ("parathyroid",),
            "'s prognosis depends on the cause (primary, renal, nutritional); most improve with correction of the cause and calcium/phosphorus management.",
        ),
    ),
    "renal_urinary": (
        (
            ("chronic kidney", "chronic renal", "ckd"),
            "'s prognosis depends on IRIS stage and rate of progression — early disease can have median survival over 3 years with renal diet and supportive care, advanced disease weeks to 2 years.",
        ),
        (
            ("acute kidney", "acute renal", "aki"),
            "'s prognosis is potentially reversible with early intervention and removal of the cause; persistent oliguria/anuria carries a poor prognosis.",
        ),
        (
            ("cystitis", "flutd", "fic", "idiopathic"),
            "'s prognosis includes a roughly 50% spontaneous remission rate but frequent recurrence; stress, environmental and water-intake management improve long-term outcome.",
        ),
        (
            ("urolith", "stone", "calculi"),
            "'s prognosis is good with composition-appropriate dissolution diets or surgical removal, but recurs without ongoing dietary and water management.",
        ),
        (
            ("urinary tract infection", "uti", "bacteriuria"),
            "'s prognosis is good with culture-guided antimicrobials; management of underlying disease is key to preventing recurrence.",
        ),
        (
            ("obstruction", "blocked"),
            "'s prognosis depends on how rapidly the obstruction is relieved — good with prompt management, but delay risks fatal acute kidney injury and hyperkalaemia.",
        ),
    ),
    "cardiac": (
        (
            ("hypertrophic", "hcm"),
            "'s prognosis after onset of signs is a median survival of about 1.3 years in cats, worsened by arterial thromboembolism (FATE).",
        ),
        (("dilated", "dcm"), "'s prognosis is guarded, with a high risk of sudden death, particularly in Dobermans."),
        (
            ("mitral", "valv", "myxomatous", "endocardiosis"),
            "'s prognosis is good for years in the compensated phase; after heart failure, ACE inhibitors, diuretics and pimobendan give a median survival of 1-2 years.",
        ),
        (
            ("thromboembolism", "fate", "aortic thrombo"),
            "'s prognosis is guarded, with an acute survival rate of about 30-50%; antithrombotic prophylaxis is important.",
        ),
        (
            ("patent ductus", "septal defect", "tetralogy", "congenital"),
            "'s prognosis varies with the defect, but early surgical or catheter-based correction can give a good outcome.",
        ),
        (
            ("heart failure", "congestive"),
            "'s prognosis depends on stage — early disease has 1-2+ years with medical therapy, end-stage a few months.",
        ),
    ),
    "respiratory_other": (
        (
            ("brachycephalic", "soft palate"),
            "'s prognosis is good after surgical airway correction (soft-palate resection, nares widening).",
        ),
        (
            ("tracheal collapse",),
            "'s prognosis allows long-term medical management (antitussives, anti-inflammatories, weight control); a tracheal stent is considered in severe cases.",
        ),
        (("laryngeal paralysis",), "'s prognosis is good after unilateral arytenoid lateralisation."),
        (
            ("asthma", "bronch"),
            "'s prognosis allows long-term control with appropriate corticosteroids, bronchodilators and allergen avoidance.",
        ),
        (
            ("pneumonia", "aspiration"),
            "'s prognosis varies with cause and severity — most recover with early antimicrobials and supportive care, but severe cases are guarded.",
        ),
        (
            ("pulmonary oedema", "pleural effusion", "pyothorax", "pneumothorax"),
            "'s prognosis is governed by management of the underlying disease together with drainage and oxygen therapy.",
        ),
    ),
    "gastrointestinal": (
        (
            ("dilatation", "volvulus", "gdv", "bloat"),
            "'s prognosis is over 80% survival with early surgery, deteriorating rapidly with delayed decompression.",
        ),
        (
            ("stasis", "ileus"),
            "'s prognosis is good with early intervention but can be fatal in herbivores if it persists.",
        ),
        (
            ("inflammatory bowel", "ibd"),
            "'s prognosis allows long-term control with dietary and immunosuppressive therapy, though lifelong treatment is often required.",
        ),
        (
            ("lymphoma", "adenocarcinoma", "gastrointestinal tumor", "gi tumor"),
            "'s prognosis varies with histology — lymphoma can achieve remission with chemotherapy, but adenocarcinoma and sarcoma are poor.",
        ),
        (
            ("pancreatitis",),
            "'s prognosis is good for mild cases with supportive care, but severe or necrotising disease carries a guarded prognosis from systemic complications.",
        ),
        (
            ("megacolon", "constipation", "obstipation"),
            "'s prognosis allows medical management (diet, laxatives, deobstipation), with subtotal colectomy considered for refractory cases.",
        ),
        (
            ("hepat", "liver", "cholang", "gallbladder"),
            "'s prognosis depends on the underlying disease and hepatic reserve — reversible with early intervention, but guarded once fibrosis is advanced.",
        ),
    ),
    "neurological": (
        (
            ("epilep", "seizure"),
            "'s prognosis with anti-seizure medication is good (near-normal lifespan) in many cases, though refractory disease reduces quality of life.",
        ),
        (
            ("intervertebral", "ivdd", "disc", "spinal cord"),
            "'s prognosis depends on neurological severity — good surgical outcome when deep pain is preserved, poor when it is absent.",
        ),
        (
            ("encephalitis", "meningitis", "meningo"),
            "'s prognosis depends on the cause — autoimmune forms can remit with immunosuppression, infectious forms vary with the pathogen.",
        ),
        (
            ("brain tumor", "brain tumour", "tumor", "tumour"),
            "'s prognosis can be extended with surgery and radiation, but is limited by location and histology.",
        ),
        (
            ("cognitive", "dementia"),
            "'s prognosis is progressive, but medication, supplements and environmental enrichment can slow progression and improve quality of life.",
        ),
        (
            ("vestibular", "head tilt", "torticollis"),
            "'s prognosis is good for peripheral (idiopathic) disease, which often improves within weeks; central disease varies with the cause.",
        ),
        (
            ("hydrocephalus",),
            "'s prognosis varies with severity and can be managed with medical decompression or surgical shunting.",
        ),
    ),
    "ophthalmic": (
        (
            ("corneal ulcer", "cornea"),
            "'s prognosis is good with early treatment, but infected deep ulcers risk perforation and warrant ophthalmology referral.",
        ),
        (("cataract",), "'s prognosis allows vision restoration with phacoemulsification surgery."),
        (
            ("glaucoma",),
            "'s prognosis allows vision preservation with acute treatment, but chronic disease often loses vision, requiring a prosthesis or enucleation.",
        ),
        (("retina", "retinal"), "'s prognosis can preserve vision with early reattachment and treatment of the cause."),
        (("uveitis", "iris"), "'s prognosis is determined by treatment of the underlying disease."),
        (("conjunctivitis", "eyelid", "epiphora"), "'s prognosis is generally good with cause-directed treatment."),
    ),
    "musculoskeletal": (
        (
            ("fracture",),
            "'s prognosis is good with site- and configuration-appropriate reduction and fixation, though open or infected fractures heal more slowly.",
        ),
        (
            ("osteoarthritis", " oa", "degenerative joint"),
            "'s prognosis is progressive but a good quality of life is sustainable long-term with weight control, physiotherapy, NSAIDs and joint protection.",
        ),
        (
            ("cruciate", "ligament", "patellar luxation"),
            "'s prognosis is good after surgical stabilisation (TPLO, TTA, lateral suture).",
        ),
        (
            ("hip dysplasia", "elbow dysplasia", "developmental"),
            "'s prognosis is good — mild disease is managed medically, severe disease with surgery (e.g. total hip replacement).",
        ),
        (("intervertebral", "spinal"), "'s prognosis is determined by neurological severity and timing of treatment."),
        (
            ("osteomyelitis", "infection"),
            "'s prognosis depends on long-term pathogen-directed antimicrobials and surgical debridement.",
        ),
    ),
    "dermatological": (
        (
            ("atopic", "allergy", "allergic"),
            "'s prognosis is not curative but allows symptom control through long-term environmental, pharmacological and desensitisation management.",
        ),
        (
            ("pyoderma", "bacterial"),
            "'s prognosis is good with appropriate antimicrobials; management of underlying disease is key to preventing recurrence.",
        ),
        (
            ("dermatophyt", "ringworm", "fungal"),
            "'s prognosis is good — antifungal therapy is usually curative (typically 4-12 weeks).",
        ),
        (
            ("pemphigus", "autoimmune", "lupus"),
            "'s prognosis allows remission with immunosuppression, but long-term maintenance therapy is required.",
        ),
        (
            ("mange", "demodic", "sarcoptic", "mite", "parasit"),
            "'s prognosis is good with appropriate antiparasitics, though underlying immune status affects the course.",
        ),
        (("abscess", "cellulitis"), "'s prognosis is good with drainage, lavage and antimicrobials."),
    ),
    "hematological": (
        (
            ("immune-mediated hemolytic", "imha", "autoimmune hemolytic"),
            "'s prognosis has an acute mortality of 20-50%, but long-term survivors do well after immunosuppression.",
        ),
        (
            ("thrombocytopenia", "itp", "imtp"),
            "'s prognosis is good in most cases with appropriate immunosuppressive therapy.",
        ),
        (("anemia", "anaemia"), "'s prognosis depends on the underlying disease (FeLV, FIV, CKD, haemorrhage)."),
        (
            ("blood loss", "hemorrhage", "haemorrhage"),
            "'s prognosis allows survival with early haemostasis and transfusion.",
        ),
        (
            ("coagulopathy", "dic", "hemophilia"),
            "'s prognosis depends on the cause (anticoagulant rodenticide toxicity, hepatic failure, DIC).",
        ),
    ),
    "reproductive": (
        (("pyometra",), "'s prognosis is good with ovariohysterectomy; early diagnosis is key."),
        (("mastitis",), "'s prognosis is good with antimicrobials and supportive care."),
        (
            ("dystocia", "cesarean", "caesarean"),
            "'s prognosis is good for dam and offspring with early diagnosis (emergency caesarean when indicated).",
        ),
        (
            ("eclampsia", "toxemia", "toxaemia"),
            "'s prognosis is good with early treatment but can be fatal if delayed.",
        ),
        (
            ("prostat",),
            "'s prognosis is good for benign hyperplasia after castration, but prostatic carcinoma is poor (often advanced at diagnosis).",
        ),
        (
            ("mammary tumor", "mammary tumour"),
            "'s prognosis is good with early complete excision, with chemotherapy added according to grade.",
        ),
        (("testic", "ovari", "retained", "cryptorchid"), "'s prognosis is good after surgical removal."),
    ),
    "dental": (
        (
            ("periodont", "gingivit"),
            "'s prognosis allows arrest of progression with early scaling and appropriate oral care.",
        ),
        (
            ("tooth root abscess", "apical", "endodontic"),
            "'s prognosis allows cure with extraction or root-canal therapy.",
        ),
        (
            ("malocclusion", "overgrown", "elongated crown"),
            "'s prognosis allows long-term management with regular dental procedures (every 4-6 weeks), though definitive occlusal correction is difficult.",
        ),
        (
            ("oral tumor", "oral tumour", "squamous"),
            "'s prognosis is good for benign masses after complete excision, but malignant disease (e.g. squamous cell carcinoma) is poor.",
        ),
        (
            ("resorpt",),
            "'s prognosis: extraction of the affected tooth resolves the pain, but there is no medical treatment to halt progression.",
        ),
    ),
}


_CATALOG_FALLBACK_EN: dict[str, str] = {
    "endocrine_metabolic": "the type of hormonal/metabolic derangement, whether it can be corrected, and the presence of complications",
    "renal_urinary": "the severity and rate of progression of the renal or urinary-tract disease",
    "cardiac": "the type of underlying cardiac disease and the stage of heart failure",
    "respiratory_other": "the site and severity of the airway or lung disease and any underlying condition",
    "gastrointestinal": "the underlying disease, the degree of dehydration and electrolyte derangement, and treatment timing",
    "neurological": "the cause and neurological severity (particularly the presence of deep pain)",
    "ophthalmic": "the location and progression of the lesion, treatment timing, and whether vision can be preserved",
    "musculoskeletal": "the site and severity of the injury and the treatment used",
    "dental": "the progression of the lesion and the availability of early intervention",
    "dermatological": "the cause (allergic, infectious or autoimmune) and chronicity",
    "hematological": "the underlying disease and the severity of anaemia, bleeding or coagulopathy",
    "reproductive": "the disease process, treatment timing and urgency",
}

# English general-statement category paragraphs (faithful to the JA bodies).
_PROGNOSIS_GENERAL_EN: dict[str, str] = {
    "infection": (
        "'s prognosis varies widely with pathogen virulence, host immune status, treatment timing and "
        "any underlying disease. Most infections do well with early diagnosis and appropriate "
        "antimicrobial and supportive therapy. Immunosuppressed, very young, geriatric or "
        "multi-organ-failure cases can have a guarded prognosis. Recurrence, chronicity and "
        "antimicrobial resistance are also important prognostic factors."
    ),
    "parasitic": (
        "'s prognosis varies with the parasite species, burden, host immune status and treatment "
        "response. Most parasitic disease does well with early detection and appropriate "
        "antiparasitics, but heavy, cardiovascular or blood-borne infections respond more slowly. "
        "Ongoing environmental and vector management is key to long-term outcome, and concurrent "
        "management of underlying disease is needed when the host is immunocompromised."
    ),
    "toxicity": (
        "'s prognosis depends heavily on the toxin, the dose, the time from exposure to treatment and "
        "the degree of organ injury. Most acute intoxications do well with early decontamination "
        "(emesis, gastric lavage, activated charcoal) and aggressive supportive care. Severe cases "
        "with hepatic necrosis or renal failure carry a guarded prognosis, and chronic intoxication "
        "may cause irreversible organ damage. Early use of a specific antidote, where one exists "
        "(N-acetylcysteine, vitamin K1, chelators), greatly improves the outcome."
    ),
    "trauma": (
        "'s prognosis varies with the site, severity and timing of treatment. Simple fractures and "
        "minor lacerations do well with appropriate treatment; polytrauma is survivable with early "
        "stabilisation and staged repair; severe visceral injury is survivable with emergency surgery "
        "but fatal if diagnosis is delayed. Brain and spinal injury have a neurological prognosis set "
        "by injury severity and treatment timing, and severe shock is survivable with early intervention."
    ),
    "autoimmune": (
        "'s prognosis varies with the affected organ, treatment response and control of relapses. "
        "Appropriate immunosuppression controls the acute phase (with disease-dependent early "
        "mortality), and long-term immunosuppressive therapy maintains remission. Relapses are managed "
        "by adjusting therapy, though repeated relapses can become treatment-resistant. Management of "
        "secondary complications (infection, thrombosis, drug side-effects) governs long-term outcome."
    ),
    "nutritional": (
        "'s prognosis is good in most cases once the underlying nutrient imbalance is corrected. Most "
        "clinical signs are reversible with early dietary correction and supplementation, though "
        "developmental or organ damage from severe chronic malnutrition may be irreversible. Owner "
        "education to prevent recurrence is key to long-term outcome."
    ),
    "behavioral": (
        "'s prognosis is improvable with an integrated approach of behaviour modification, environmental "
        "management and medication. Many cases improve with early intervention, and severe cases "
        "benefit from concurrent pharmacotherapy; concurrent medical disease must be managed first."
    ),
    "generic": (
        "'s prognosis varies with the underlying disease process, treatment timing and any comorbidity. "
        "Early diagnosis and appropriate intervention give a good outcome in many cases, while severe, "
        "advanced or complicated cases can do worse. Ongoing monitoring supports long-term outcome."
    ),
}


def _combine_prognosis_en(prefix: str, clause: str) -> str:
    """Join an EN prognosis subject and clause without the double-possessive bug.

    The catalog clauses begin ``"'s prognosis ..."`` and ``prefix`` ends in the
    (plural) species name, so naive concatenation yields ``"... in rabbits's
    prognosis ..."`` — grammatically wrong and reading like machine output.
    Render it instead as ``"The prognosis of <prefix> ..."``.
    """
    marker = "'s prognosis"
    if clause.startswith(marker):
        return f"The prognosis of {prefix}{clause[len(marker) :]}"
    return prefix + clause


def gen_prognosis_en(category: str, name_en: str, species: str) -> str:
    """English counterpart of ``gen_prognosis_ja`` (disease-specific prognosis)."""
    sp_en = SPECIES_EN.get(species, species)
    prefix = _disease_prefix_en(name_en, sp_en)

    if category == "neoplasia":
        return _combine_prognosis_en(prefix, _NEOPLASIA_PROGNOSIS_EN[_neoplasia_subtype_en(name_en)])

    catalog = _PROGNOSIS_CATALOG_EN.get(category)
    if catalog:
        name_l = (name_en or "").lower()
        for keywords, clause in catalog:
            if any(k in name_l for k in keywords):
                return _combine_prognosis_en(prefix, clause)
        lead = _CATALOG_FALLBACK_EN.get(category, "the underlying disease process, its severity and treatment timing")
        return (
            f"The prognosis of {prefix} varies with {lead}. Early diagnosis and disease-appropriate treatment "
            f"and monitoring give a good outcome in many cases, while advanced or complicated cases can do worse."
        )

    if category in ("viral_infection", "bacterial_infection", "respiratory_infection", "fungal_infection"):
        return _combine_prognosis_en(prefix, _PROGNOSIS_GENERAL_EN["infection"])
    if category in _PROGNOSIS_GENERAL_EN:
        return _combine_prognosis_en(prefix, _PROGNOSIS_GENERAL_EN[category])
    return _combine_prognosis_en(prefix, _PROGNOSIS_GENERAL_EN["generic"])


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
    if category in ("respiratory_other", "respiratory_infection"):
        return (
            f"{prefix}の病態生理は気道・肺実質・胸腔の機能/構造異常によりガス交換が障害される。"
            f"上気道閉塞（喉頭麻痺・気管虚脱・短頭種気道症候群）では吸気抵抗増大→陰圧性気道虚脱→気道炎症の悪循環を生じる。"
            f"下気道・肺実質病変（肺炎・肺水腫・気管支炎）では換気血流不均衡・拡散障害により低酸素血症を来す。"
            f"胸腔病変（胸水・気胸）では肺の物理的圧排により拘束性換気障害を生じる。"
            f"慢性低酸素は肺高血圧・右心負荷（肺性心）に進展し、急性増悪は呼吸不全・チアノーゼを呈する。"
        )
    if category == "gastrointestinal":
        return (
            f"{prefix}の病態生理は消化管の運動・分泌・吸収・粘膜バリア機能の破綻により展開する。"
            f"炎症性・潰瘍性病変では粘膜傷害→蛋白漏出・出血・吸収不良→低アルブミン血症・体重減少を生じる。"
            f"閉塞・うっ滞（イレウス・GI stasis・GDV）では内容物貯留→腸管拡張・血流障害・細菌異常増殖→内毒素血症・脱水・電解質異常に進展する。"
            f"膵・肝胆道病変では消化酵素・胆汁うっ滞による自己消化・全身炎症反応を惹起する。"
            f"重症例では循環血液量減少性ショック・敗血症・多臓器不全に至る。"
        )
    if category == "neurological":
        return (
            f"{prefix}の病態生理は中枢・末梢神経または神経筋接合部の機能/構造障害により神経伝達が破綻する。"
            f"占拠性・圧迫性病変（椎間板ヘルニア・腫瘍・水頭症）では実質圧迫→局所虚血・浮腫→神経機能脱落を生じる。"
            f"炎症性・感染性病変（髄膜脳炎）ではサイトカイン放出・血液脳関門破綻により神経細胞傷害が進行する。"
            f"発作性疾患（てんかん）では神経細胞の過剰同期性発火により痙攣を反復し、重積は不可逆的神経傷害を招く。"
            f"前庭・小脳病変では平衡・協調運動障害を、脊髄病変では病変部以下の運動・感覚・自律神経障害を呈する。"
        )
    if category == "musculoskeletal":
        return (
            f"{prefix}の病態生理は骨・関節・靱帯・腱・筋の構造的破綻と二次的炎症により展開する。"
            f"関節疾患では軟骨基質の変性・摩耗→軟骨下骨硬化・骨棘形成→滑膜炎・疼痛・可動域制限の悪循環を生じる。"
            f"骨折・靱帯損傷では構造的支持の喪失→不安定性・異常負荷→疼痛・跛行・廃用性筋萎縮を来す。"
            f"骨代謝異常（代謝性骨疾患・栄養性二次性副甲状腺機能亢進症）では骨吸収亢進・骨基質石灰化障害により病的骨折・骨変形を生じる。"
            f"慢性経過では関節拘縮・筋力低下・運動機能障害が進行する。"
        )
    if category == "dermatological":
        return (
            f"{prefix}の病態生理は皮膚バリア機能の破綻と炎症・免疫応答により展開する。"
            f"アレルギー性皮膚炎では経皮アレルゲン感作→Th2優位の免疫応答→IgE産生・肥満細胞脱顆粒→掻痒・炎症の連鎖を生じる。"
            f"角化・バリア異常では経表皮水分喪失増加・微生物定着により二次感染（膿皮症・マラセチア）を招く。"
            f"掻破による自己傷害が炎症をさらに増悪させる掻痒-掻破サイクルを形成する。"
            f"慢性炎症では苔癬化・色素沈着・脱毛が進行し、難治化する。"
        )
    if category == "ophthalmic":
        return (
            f"{prefix}の病態生理は眼組織（角膜・ぶどう膜・水晶体・網膜・眼圧調節系）の構造/機能障害により視機能が脅かされる。"
            f"角膜病変では上皮バリア破綻→間質浮腫・血管新生・潰瘍進行→穿孔リスクを生じる。"
            f"ぶどう膜炎では血液眼関門破綻・炎症細胞浸潤により続発性緑内障・白内障・網膜剥離を招く。"
            f"房水産生・流出の不均衡では眼圧上昇→視神経・網膜神経節細胞傷害（緑内障）により不可逆的失明に至る。"
            f"水晶体・網膜変性では透光体混濁・光受容器変性により進行性視覚障害を呈する。"
        )
    if category == "hematological":
        return (
            f"{prefix}の病態生理は赤血球・白血球・血小板・凝固系の産生/破壊/機能の不均衡により展開する。"
            f"貧血では赤血球産生低下（骨髄抑制・腎性エリスロポエチン低下）または喪失亢進（出血・溶血）により組織への酸素供給が低下する。"
            f"溶血では赤血球膜傷害・免疫介在性破壊によりビリルビン上昇・ヘモグロビン尿を生じる。"
            f"血小板・凝固異常では一次/二次止血の破綻により出血傾向（点状出血・体腔内出血）を、過凝固ではDIC・血栓塞栓を来す。"
            f"重症貧血・出血は循環性ショック・組織低酸素により多臓器障害に進展する。"
        )
    if category == "reproductive":
        return (
            f"{prefix}の病態生理は生殖器の構造/機能異常およびホルモン環境の変化により展開する。"
            f"子宮蓄膿症ではプロゲステロン優位下の子宮内膜過形成・嚢胞性変化に細菌感染が重畳し、内毒素血症・敗血症・急性腎傷害に進展する。"
            f"難産では胎子・産道・娩出力の異常により分娩停止→胎子仮死・子宮破裂・低カルシウム血症を生じる。"
            f"妊娠中毒・産褥疾患では代謝需要急増に対する恒常性破綻を来す。"
            f"性ホルモン依存性疾患では内分泌刺激の持続が組織増殖・腫瘍化を促進する。"
        )
    if category == "toxicity":
        return (
            f"{prefix}の病態生理は毒性物質の吸収・分布・標的分子への作用・代謝/排泄の過程により決定される。"
            f"毒物は特異的標的（酵素阻害・受容体結合・細胞膜傷害・DNA損傷）に作用し、用量依存的に細胞機能を障害する。"
            f"肝・腎は代謝・排泄の主要臓器であり、毒性代謝物の生成や蓄積により標的臓器傷害（肝壊死・急性腎傷害）を生じる。"
            f"酸化ストレス・ミトコンドリア傷害・細胞死（壊死・アポトーシス）が組織傷害の共通機序となる。"
            f"重症例では多臓器不全・凝固障害・神経症状・循環虚脱に進展する。"
        )
    if category == "trauma":
        return (
            f"{prefix}の病態生理は外力による組織の物理的破壊と続発する炎症・修復反応により展開する。"
            f"一次損傷（裂傷・骨折・挫滅・熱傷）に続き、炎症メディエーター放出・浮腫・微小循環障害による二次損傷が拡大する。"
            f"重度外傷では出血性ショック・全身性炎症反応症候群（SIRS）・凝固障害（外傷性凝固障害）を併発する。"
            f"組織修復は止血→炎症→増殖→リモデリングの過程を辿るが、感染・血流不良・異物残存は治癒遅延・瘢痕拘縮を招く。"
            f"頭部・体腔・脊髄の外傷では臓器特異的な致死的合併症を生じうる。"
        )
    if category == "autoimmune":
        return (
            f"{prefix}の病態生理は自己寛容の破綻により自己抗原に対する免疫応答が惹起されることに基づく。"
            f"自己抗体・自己反応性T細胞が標的組織を攻撃し、II型（細胞傷害性）・III型（免疫複合体）・IV型（細胞性）過敏反応により組織傷害を生じる。"
            f"免疫介在性溶血性貧血・血小板減少症では血球が破壊され、多発性関節炎・天疱瘡では関節・皮膚が標的となる。"
            f"遺伝的素因に感染・薬剤・腫瘍などの誘因が加わり発症する（続発性も多い）。"
            f"再燃と寛解を繰り返し、免疫抑制療法への反応性が予後を左右する。"
        )
    if category == "dental":
        return (
            f"{prefix}の病態生理は歯・歯周組織・咬合の異常により摂食機能と全身状態が障害される。"
            f"歯周病ではプラーク細菌→歯肉炎→歯周ポケット形成・歯槽骨吸収→歯の動揺・脱落の進行とともに、菌血症を介した全身臓器への影響を生じる。"
            f"草食・げっ歯類の不正咬合では常生歯の過長・スパー形成により口腔粘膜傷害・疼痛・摂食困難を来す。"
            f"歯根尖膿瘍では根尖部感染が顎骨・眼窩へ波及する。"
            f"摂食低下は二次的な消化管うっ滞・肝リピドーシス等の致死的病態を誘発しうる。"
        )
    if category == "fungal_infection":
        return (
            f"{prefix}の病態生理は真菌の定着・組織侵入と宿主免疫応答により展開する。"
            f"皮膚糸状菌・酵母（マラセチア等）は角質層に定着し、表在性の炎症・掻痒・脱毛を生じる。"
            f"全身性真菌（アスペルギルス・クリプトコッカス等）は経気道・経皮的に侵入し、肉芽腫性炎症を介して多臓器に播種する。"
            f"宿主の細胞性免疫低下（免疫抑制・基礎疾患）が侵襲性・播種性感染の主要リスクとなる。"
            f"慢性肉芽腫・組織破壊・線維化が進行し、中枢神経・眼への波及は予後を悪化させる。"
        )
    if category in ("genetic_congenital", "degenerative"):
        return (
            f"{prefix}の病態生理は先天的・遺伝的素因または加齢性の進行性組織変性により展開する。"
            f"遺伝性疾患では特定遺伝子変異により酵素・構造蛋白・受容体の機能異常を生じ、出生時または特定年齢で発症する。"
            f"変性性疾患では加齢・酸化ストレス・慢性機械的負荷により細胞・基質が緩徐に変性・脱落する。"
            f"代償機構により初期は無症状でも、機能予備能を超えると臨床徴候が顕在化する。"
            f"多くは不可逆性・進行性であり、進行抑制と支持療法が管理の中心となる。"
        )
    if category == "behavioral":
        return (
            f"{prefix}の病態生理は神経生物学的素因・学習・環境ストレスの相互作用により展開する。"
            f"恐怖・不安では扁桃体を中心とした情動回路の過活動と視床下部-下垂体-副腎系（HPA軸）の慢性活性化が関与する。"
            f"セロトニン・ドパミン等の神経伝達バランスの乱れが情動・衝動制御に影響する。"
            f"嫌悪的経験の学習・社会化不足・環境の不適合が問題行動を強化・維持する。"
            f"慢性ストレスは常同行動・自己傷害・身体疾患（消化管・皮膚）の併発を招く。"
        )
    # generic
    return (
        f"{prefix}の病態生理は原因病態と進行段階により多面的に展開する。"
        f"初期の局所組織傷害・機能異常から全身的代償機構の動員、最終的な臓器機能不全への進展という共通の流れがある。"
        f"病態の進行は原因と宿主の免疫・代謝状態に依存する。"
        f"早期発見・早期治療が予後改善の鍵。"
    )


def gen_pathophysiology_en(category: str, name_en: str, species: str) -> str:
    """English category pathophysiology mirroring ``gen_pathophysiology_ja``.

    Called when the English pathophysiology carries the wrong organ-system
    category template (e.g. myocarditis described with the *parasitic* template).
    Category is resolved from the disease *name* by the caller.
    """
    sp_en = SPECIES_EN.get(species, species)
    prefix = _disease_prefix_en(name_en, sp_en)

    if category == "viral_infection":
        return (
            f"The pathophysiology of {prefix} unfolds as viral entry → intracellular replication → tissue injury → immune response. "
            f"The pathogen binds specific cell-surface receptors, enters the cell and hijacks host machinery to replicate its RNA or DNA. "
            f"The balance between the host innate/adaptive immune response and viral virulence determines the course. "
            f"The acute phase produces local inflammation and systemic cytokine release, while the chronic phase causes organ-specific injury (lymphopenia, marrow suppression, neural damage)."
        )
    if category == "bacterial_infection":
        return (
            f"The pathophysiology of {prefix} unfolds as bacterial entry → colonisation/proliferation → toxin production and tissue injury → immune response. "
            f"Pathogenic bacteria breach mucosal or skin barriers, adhere to target tissue via adhesins, proliferate and release exotoxins and endotoxins. "
            f"Host neutrophil, complement and antibody responses control the organism, but an excessive response causes tissue injury (SIRS, sepsis). "
            f"Bacterial resistance mechanisms (beta-lactamases, efflux pumps, target-site mutation) affect the therapeutic response."
        )
    if category in ("respiratory_infection", "respiratory_other"):
        return (
            f"The pathophysiology of {prefix} impairs gas exchange through functional or structural abnormality of the airway, lung parenchyma or pleural space. "
            f"Upper-airway obstruction (laryngeal paralysis, tracheal collapse, brachycephalic airway syndrome) sets up a vicious cycle of increased inspiratory resistance → negative-pressure airway collapse → airway inflammation. "
            f"Lower-airway and parenchymal disease (pneumonia, oedema, bronchitis) causes hypoxaemia through ventilation-perfusion mismatch and diffusion impairment. "
            f"Chronic hypoxia progresses to pulmonary hypertension and right-heart strain (cor pulmonale)."
        )
    if category == "fungal_infection":
        return (
            f"The pathophysiology of {prefix} unfolds through fungal colonisation and tissue invasion with the host immune response. "
            f"Dermatophytes and yeasts (e.g. Malassezia) colonise the stratum corneum, producing superficial inflammation, pruritus and alopecia. "
            f"Systemic fungi (Aspergillus, Cryptococcus) enter via the airway or skin and disseminate to multiple organs through granulomatous inflammation. "
            f"Impaired cell-mediated immunity (immunosuppression, underlying disease) is the major risk for invasive, disseminated infection."
        )
    if category == "parasitic":
        return (
            f"The pathophysiology of {prefix} varies with parasite species, burden and location. "
            f"Gastrointestinal parasites cause mucosal injury, impaired nutrient absorption and, with vascular invasion, haemorrhage or obstruction. "
            f"Cardiovascular parasites (heartworm) cause pulmonary arterial obstruction, vasculitis and right-heart overload, progressing to right-sided heart failure. "
            f"Blood parasites (e.g. Babesia) cause haemolysis, immune-mediated secondary haemolysis and disseminated intravascular coagulation; ectoparasites drive skin injury, allergy and vector-borne secondary disease."
        )
    if category == "neoplasia":
        return (
            f"The pathophysiology of {prefix} begins with malignant transformation of normal cells. "
            f"Activation of oncogenes and inactivation of tumour-suppressor genes progressively confer sustained proliferative signalling, evasion of apoptosis, angiogenesis and invasive/metastatic capacity. "
            f"The tumour microenvironment builds immune-evasion mechanisms, with tumour-associated macrophages and regulatory T cells suppressing anti-tumour immunity. "
            f"Advanced disease causes cachexia, paraneoplastic syndromes (hypercalcaemia, hypoglycaemia) and systemic complications."
        )
    if category == "endocrine_metabolic":
        return (
            f"The pathophysiology of {prefix} disrupts systemic homeostasis through endocrine gland dysfunction or a deranged metabolic pathway. "
            f"Diabetes: beta-cell failure and insulin resistance cause chronic hyperglycaemia, advanced-glycation-end-product formation, microvascular injury and multi-organ complications. "
            f"Hyperthyroidism: excess T3/T4 raises basal metabolism and cardiac output, causing weight loss with secondary hypertension and renal decline. "
            f"Cushing's: chronic cortisol excess causes protein catabolism, immunosuppression, secondary diabetes and increased susceptibility to infection."
        )
    if category == "renal_urinary":
        return (
            f"The pathophysiology of {prefix} unfolds through progressive nephron loss or urinary-tract dysfunction. "
            f"CKD: loss of functional nephrons → overload of remaining nephrons → glomerular hypertension and proteinuria → further nephron injury forms a vicious cycle. "
            f"Secondary hyperphosphataemia, secondary hyperparathyroidism, anaemia (low erythropoietin), systemic hypertension and accumulation of uraemic toxins follow. "
            f"In FLUTD/FIC, a chronic neuroendocrine stress response drives bladder-wall neurogenic inflammation and increased permeability, causing spontaneous pain and abnormal urination."
        )
    if category == "nutritional":
        return (
            f"The pathophysiology of {prefix} rests on biochemical pathway derangement from deficiency or excess of essential nutrients. "
            f"Calcium/phosphorus imbalance drives secondary hyperparathyroidism with bone resorption, osteomalacia and pathological fracture. "
            f"Vitamin deficiency impairs the enzyme reactions each vitamin serves, producing specific syndromes (vitamin A deficiency → visual impairment; thiamine deficiency → neurological signs). "
            f"Protein-energy malnutrition causes catabolism, muscle wasting, impaired immunity and delayed wound healing, while nutrient excess increases hepatic/renal metabolic load and toxicity (fat-soluble vitamin excess)."
        )
    if category == "cardiac":
        return (
            f"The pathophysiology of {prefix} unfolds as functional or structural abnormality of the myocardium, valves, conduction system or pericardium drives reduced cardiac output and a cascade of compensatory mechanisms. "
            f"In HCM, myocardial hypertrophy → left-ventricular outflow obstruction → raised left-atrial pressure → pulmonary oedema. "
            f"In DCM, reduced contractility → ventricular dilation → low output → neurohormonal activation (RAAS, sympathetic) → further remodelling. "
            f"End-stage disease progresses to pulmonary oedema, ascites, cardiogenic shock and fatal arrhythmias."
        )
    if category == "gastrointestinal":
        return (
            f"The pathophysiology of {prefix} unfolds through breakdown of gastrointestinal motility, secretion, absorption and mucosal-barrier function. "
            f"Inflammatory and ulcerative lesions cause mucosal injury → protein loss, haemorrhage and malabsorption → hypoalbuminaemia and weight loss. "
            f"Obstruction and stasis (ileus, GI stasis, GDV) cause content retention → bowel distension, compromised perfusion and bacterial overgrowth → endotoxaemia, dehydration and electrolyte derangement. "
            f"Severe cases progress to hypovolaemic shock, sepsis and multi-organ failure."
        )
    if category == "neurological":
        return (
            f"The pathophysiology of {prefix} disrupts neural transmission through functional or structural injury of the central, peripheral or neuromuscular systems. "
            f"Space-occupying or compressive lesions (intervertebral disc disease, tumour, hydrocephalus) cause parenchymal compression → local ischaemia and oedema → neurological deficit. "
            f"Inflammatory and infectious lesions (meningoencephalitis) drive neuronal injury via cytokine release and blood-brain-barrier breakdown. "
            f"In seizure disorders, hypersynchronous neuronal firing produces repeated convulsions, and status epilepticus causes irreversible neural injury."
        )
    if category == "ophthalmic":
        return (
            f"The pathophysiology of {prefix} threatens vision through structural or functional injury of ocular tissues (cornea, uvea, lens, retina, pressure-regulating system). "
            f"Corneal lesions progress from epithelial-barrier breakdown → stromal oedema, vascularisation and ulceration → risk of perforation. "
            f"Uveitis breaks the blood-ocular barrier and drives inflammatory infiltration, causing secondary glaucoma, cataract and retinal detachment. "
            f"Imbalance of aqueous production and outflow raises intraocular pressure → optic-nerve and retinal ganglion cell injury (glaucoma) → irreversible blindness."
        )
    if category == "musculoskeletal":
        return (
            f"The pathophysiology of {prefix} unfolds through structural failure of bone, joint, ligament, tendon or muscle with secondary inflammation. "
            f"Joint disease sets up a vicious cycle of cartilage-matrix degeneration and wear → subchondral bone sclerosis and osteophyte formation → synovitis, pain and reduced range of motion. "
            f"Fractures and ligament injury cause loss of structural support → instability and abnormal loading → pain, lameness and disuse muscle atrophy. "
            f"Bone-metabolic disorders (metabolic bone disease, nutritional secondary hyperparathyroidism) cause increased resorption and defective mineralisation with pathological fracture and deformity."
        )
    if category == "dermatological":
        return (
            f"The pathophysiology of {prefix} unfolds through breakdown of the skin barrier with inflammatory and immune responses. "
            f"Allergic dermatitis links percutaneous allergen sensitisation → a Th2-dominant response → IgE production and mast-cell degranulation → pruritus and inflammation. "
            f"Keratinisation and barrier defects increase transepidermal water loss and microbial colonisation, inviting secondary infection (pyoderma, Malassezia). "
            f"Self-trauma from scratching establishes a pruritus-scratch cycle, and chronic inflammation progresses to lichenification, hyperpigmentation and alopecia."
        )
    if category == "hematological":
        return (
            f"The pathophysiology of {prefix} unfolds through imbalance in the production, destruction or function of red cells, white cells, platelets and the coagulation system. "
            f"Anaemia reduces tissue oxygen delivery through decreased red-cell production (marrow suppression, low renal erythropoietin) or increased loss (haemorrhage, haemolysis). "
            f"Haemolysis causes raised bilirubin and haemoglobinuria through membrane injury or immune-mediated destruction. "
            f"Platelet and coagulation disorders cause a bleeding tendency, while hypercoagulability causes DIC and thromboembolism; severe anaemia or haemorrhage progresses to shock and multi-organ injury."
        )
    if category == "reproductive":
        return (
            f"The pathophysiology of {prefix} unfolds through structural or functional abnormality of the reproductive tract and changes in the hormonal environment. "
            f"In pyometra, cystic endometrial hyperplasia under progesterone dominance is complicated by bacterial infection, progressing to endotoxaemia, sepsis and acute kidney injury. "
            f"Dystocia from fetal, birth-canal or expulsive-force abnormality causes arrested labour → fetal distress, uterine rupture and hypocalcaemia. "
            f"Sex-hormone-dependent diseases are promoted by sustained endocrine stimulation of tissue proliferation and neoplasia."
        )
    if category == "toxicity":
        return (
            f"The pathophysiology of {prefix} is determined by absorption, distribution, action on the molecular target and metabolism/excretion of the toxic substance. "
            f"The toxin acts on a specific target (enzyme inhibition, receptor binding, membrane injury, DNA damage), impairing cell function in a dose-dependent manner. "
            f"The liver and kidneys, as the principal organs of metabolism and excretion, sustain target-organ injury (hepatic necrosis, acute kidney injury) from toxic metabolites. "
            f"Oxidative stress, mitochondrial injury and cell death are common mechanisms; severe cases progress to multi-organ failure, coagulopathy and circulatory collapse."
        )
    if category == "trauma":
        return (
            f"The pathophysiology of {prefix} unfolds through physical tissue destruction by external force with a subsequent inflammatory and reparative response. "
            f"Primary injury (laceration, fracture, crush, burn) is followed by secondary injury that spreads through inflammatory-mediator release, oedema and microcirculatory compromise. "
            f"Severe trauma is complicated by haemorrhagic shock, systemic inflammatory response syndrome (SIRS) and trauma-induced coagulopathy. "
            f"Repair follows haemostasis → inflammation → proliferation → remodelling, but infection, poor perfusion or retained foreign material delays healing and causes scar contracture."
        )
    if category == "autoimmune":
        return (
            f"The pathophysiology of {prefix} rests on loss of self-tolerance and an immune response mounted against self-antigens. "
            f"Autoantibodies and self-reactive T cells attack target tissue, causing injury through type II (cytotoxic), type III (immune-complex) and type IV (cell-mediated) hypersensitivity. "
            f"In immune-mediated haemolytic anaemia and thrombocytopenia the blood cells are destroyed; in polyarthritis and pemphigus the joints and skin are targeted. "
            f"A genetic predisposition combines with triggers (infection, drugs, neoplasia) to precipitate disease, which relapses and remits, with the response to immunosuppression governing prognosis."
        )
    if category == "dental":
        return (
            f"The pathophysiology of {prefix} impairs feeding and systemic health through abnormality of the teeth, periodontium or occlusion. "
            f"In periodontal disease, plaque bacteria → gingivitis → periodontal pocket formation and alveolar bone resorption → tooth mobility and loss, with bacteraemia affecting distant organs. "
            f"In herbivore and rodent malocclusion, overgrowth and spur formation of the continuously growing teeth cause oral mucosal injury, pain and inappetence. "
            f"Reduced intake can precipitate life-threatening secondary conditions such as gastrointestinal stasis and hepatic lipidosis."
        )
    if category in ("genetic_congenital", "degenerative"):
        return (
            f"The pathophysiology of {prefix} unfolds through a congenital/genetic predisposition or age-related progressive tissue degeneration. "
            f"In genetic disease, a specific gene mutation causes dysfunction of an enzyme, structural protein or receptor, presenting at birth or a characteristic age. "
            f"In degenerative disease, ageing, oxidative stress and chronic mechanical load slowly degenerate and deplete cells and matrix. "
            f"Compensatory mechanisms keep the animal asymptomatic early, but clinical signs emerge once functional reserve is exceeded; most are irreversible and progressive."
        )
    if category == "behavioral":
        return (
            f"The pathophysiology of {prefix} unfolds through interaction between neurobiological predisposition, learning and environmental stress. "
            f"Fear and anxiety involve overactivity of amygdala-centred emotional circuits and chronic activation of the hypothalamic-pituitary-adrenal (HPA) axis. "
            f"Imbalance of neurotransmitters such as serotonin and dopamine affects emotional and impulse control. "
            f"Learning of aversive experiences, inadequate socialisation and environmental mismatch reinforce and maintain the problem, and chronic stress invites stereotypies, self-trauma and concurrent physical disease."
        )
    # generic
    return (
        f"The pathophysiology of {prefix} unfolds along multiple lines depending on the underlying cause and stage. "
        f"There is a common progression from early local tissue injury and dysfunction, through mobilisation of systemic compensatory mechanisms, to eventual organ dysfunction. "
        f"Progression depends on the cause and on the host's immune and metabolic state; early detection and treatment are key to improving prognosis."
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
# Disease description generators (concise "what is this disease" summary)
# ---------------------------------------------------------------------------

SPECIES_EN = {
    "dog": "dogs",
    "cat": "cats",
    "horse": "horses",
    "rabbit": "rabbits",
    "hamster": "hamsters",
    "guinea_pig": "guinea pigs",
    "chinchilla": "chinchillas",
    "ferret": "ferrets",
    "hedgehog": "hedgehogs",
    "sugar_glider": "sugar gliders",
    "degu": "degus",
    "bird": "birds",
    "parakeet": "parakeets",
    "parrot": "parrots",
    "reptile": "reptiles",
    "tortoise": "tortoises",
    "snake": "snakes",
    "lizard": "lizards",
    "amphibian": "amphibians",
    "fish": "fish",
    "exotic_other": "exotic pets",
}

# Trailing parenthetical species tags, e.g. "鞭毛虫原虫感染（リクガメ）" -> "鞭毛虫原虫感染".
_PAREN_TAG_RE = re.compile(r"[（(][^（）()]*[）)]\s*$")


def _clean_name(name: str) -> str:
    """Strip a trailing ``（species）`` tag so generated text reads naturally."""
    if not name:
        return name
    return _PAREN_TAG_RE.sub("", name).strip() or name


# Concise category definitions: {category: (ja_definition, en_definition)}.
# ``{n}`` = cleaned disease name, ``{s}`` = species (JA/EN).
_DESC_CATEGORY: dict[str, tuple[str, str]] = {
    "viral_infection": (
        "{n}は、{s}にみられるウイルス性感染症である。病原ウイルスが宿主細胞内で複製し組織傷害と免疫応答を引き起こす。"
        "確定診断にはPCR・抗原/抗体検査を用い、治療は支持療法と感染管理が中心となる。",
        "{n} is a viral infectious disease of {s}, in which the causative virus replicates within host "
        "cells and drives tissue injury and immune responses. Diagnosis relies on PCR and antigen/antibody "
        "testing, and management centres on supportive care and biosecurity.",
    ),
    "bacterial_infection": (
        "{n}は、{s}にみられる細菌感染症である。原因菌の定着・増殖と毒素産生により局所および全身性の炎症を生じる。"
        "培養・感受性試験に基づく抗菌薬選択と支持療法が治療の基本となる。",
        "{n} is a bacterial infection of {s}, in which colonisation, proliferation and toxin production by the "
        "causative organism drive local and systemic inflammation. Treatment is guided by culture and "
        "sensitivity testing alongside supportive care.",
    ),
    "respiratory_infection": (
        "{n}は、{s}の気道に生じる感染性呼吸器疾患である。鼻汁・くしゃみ・呼吸促迫・努力性呼吸などを呈する。"
        "病原体同定に基づく抗菌・抗ウイルス療法と、加温・酸素・ネブライザーなどの支持療法を組み合わせる。",
        "{n} is an infectious respiratory disease affecting the airways of {s}, presenting with nasal discharge, "
        "sneezing and increased respiratory effort. Care combines pathogen-directed therapy with supportive "
        "measures such as warmth, oxygen and nebulisation.",
    ),
    "fungal_infection": (
        "{n}は、{s}にみられる真菌感染症である。皮膚・呼吸器・全身臓器に病変を形成し、免疫低下個体で重症化しやすい。"
        "鏡検・培養・細胞診で診断し、長期の抗真菌療法と環境管理を要する。",
        "{n} is a fungal infection of {s} that can involve the skin, respiratory tract or internal organs and "
        "tends to be more severe in immunocompromised individuals. Diagnosis uses cytology and culture, and "
        "prolonged antifungal therapy with environmental control is required.",
    ),
    "parasitic": (
        "{n}は、{s}にみられる寄生虫性疾患である。寄生虫種・寄生数・寄生部位により消化器・血液・皮膚などに障害を生じる。"
        "糞便・血液・皮膚検査で原因虫を同定し、適切な駆虫薬と再感染予防を行う。",
        "{n} is a parasitic disease of {s} in which the species, burden and location of the parasite determine "
        "gastrointestinal, haematological or dermatological damage. Diagnosis identifies the organism on faecal, "
        "blood or skin testing, followed by targeted antiparasitic therapy and reinfection control.",
    ),
    "neoplasia": (
        "{n}は、{s}にみられる腫瘍性疾患である。正常細胞の悪性転換により異常増殖・浸潤・転移が進行しうる。"
        "細胞診・組織生検・画像診断で病型と進行度を評価し、外科・化学療法・放射線療法を病期に応じて選択する。",
        "{n} is a neoplastic disease of {s} arising from malignant transformation of normal cells, with potential "
        "for abnormal proliferation, invasion and metastasis. Cytology, biopsy and imaging establish tumour type "
        "and stage, guiding surgery, chemotherapy or radiation as appropriate.",
    ),
    "endocrine_metabolic": (
        "{n}は、{s}の内分泌・代謝機能の異常により生じる疾患である。ホルモン分泌や代謝経路の破綻が全身のホメオスタシスを乱す。"
        "血液生化学・ホルモン測定で診断し、原因に応じたホルモン補充・抑制療法と食事管理を行う。",
        "{n} is an endocrine/metabolic disorder of {s} in which disrupted hormone secretion or metabolic pathways "
        "impair systemic homeostasis. Diagnosis uses biochemistry and hormone assays, and treatment combines "
        "hormone replacement or suppression with dietary management.",
    ),
    "renal_urinary": (
        "{n}は、{s}の腎臓・尿路に生じる疾患である。ネフロン障害や尿路の閉塞・炎症により排泄・電解質調節が障害される。"
        "尿検査・血液検査・画像診断で評価し、輸液・食事療法・尿路管理を行う。",
        "{n} is a renal/urinary disease of {s} in which nephron injury or urinary obstruction and inflammation "
        "impair excretion and electrolyte balance. Diagnosis uses urinalysis, bloodwork and imaging, with "
        "treatment based on fluid therapy, diet and urinary management.",
    ),
    "cardiac": (
        "{n}は、{s}の心臓・循環系に生じる疾患である。心筋・弁・伝導系の異常が心拍出量低下と代償機構の連鎖を招く。"
        "聴診・心電図・心エコー・胸部X線で評価し、強心・利尿・血管拡張薬などで管理する。",
        "{n} is a cardiac/circulatory disease of {s} in which abnormalities of the myocardium, valves or conduction "
        "system reduce cardiac output and trigger compensatory cascades. Auscultation, ECG, echocardiography and "
        "radiography guide management with inotropes, diuretics and vasodilators.",
    ),
    "respiratory_other": (
        "{n}は、{s}の呼吸器に生じる非感染性疾患である。気道・肺・胸腔の構造または機能異常により呼吸困難・咳・運動不耐を呈する。"
        "画像診断・気道評価で病態を把握し、気管支拡張・抗炎症療法と環境管理を行う。",
        "{n} is a non-infectious respiratory disease of {s} in which structural or functional abnormalities of the "
        "airways, lungs or thorax cause dyspnoea, coughing and exercise intolerance. Imaging and airway evaluation "
        "guide bronchodilator/anti-inflammatory therapy and environmental control.",
    ),
    "gastrointestinal": (
        "{n}は、{s}の消化器に生じる疾患である。消化管の運動・吸収・分泌の障害により食欲不振・嘔吐・下痢・体重減少を呈する。"
        "画像・血液・便検査で評価し、食事療法・整腸・支持療法を組み合わせて管理する。",
        "{n} is a gastrointestinal disease of {s} in which impaired motility, absorption or secretion produces "
        "inappetence, vomiting, diarrhoea and weight loss. Imaging, bloodwork and faecal testing guide dietary "
        "therapy, gut support and supportive care.",
    ),
    "neurological": (
        "{n}は、{s}の神経系に生じる疾患である。中枢または末梢神経の障害により運動失調・発作・麻痺・行動変化などを呈する。"
        "神経学的検査と画像診断（必要に応じMRI・CT・脳脊髄液検査）で局在を診断し、原因に応じて治療する。",
        "{n} is a neurological disease of {s} in which central or peripheral nervous system injury causes ataxia, "
        "seizures, paresis or behavioural change. Neurological examination and advanced imaging (MRI/CT, CSF "
        "analysis where indicated) localise the lesion and direct cause-specific treatment.",
    ),
    "ophthalmic": (
        "{n}は、{s}の眼・付属器に生じる疾患である。角膜・結膜・水晶体・網膜などの障害により疼痛・流涙・視覚障害を呈する。"
        "細隙灯・眼圧・染色検査などで評価し、点眼・全身療法あるいは外科的治療を行う。",
        "{n} is an ophthalmic disease of {s} affecting the eye and adnexa — cornea, conjunctiva, lens or retina — "
        "and causing pain, ocular discharge and visual impairment. Slit-lamp, tonometry and staining guide topical, "
        "systemic or surgical treatment.",
    ),
    "musculoskeletal": (
        "{n}は、{s}の運動器に生じる疾患である。骨・関節・筋・腱の障害により跛行・疼痛・可動域制限・姿勢異常を呈する。"
        "触診・X線などの画像診断で評価し、鎮痛・安静・外科的整復やリハビリテーションを行う。",
        "{n} is a musculoskeletal disease of {s} in which disorders of bone, joint, muscle or tendon cause "
        "lameness, pain, reduced range of motion and postural change. Palpation and radiography guide analgesia, "
        "rest, surgical repair and rehabilitation.",
    ),
    "dental": (
        "{n}は、{s}の歯・口腔に生じる疾患である。不正咬合・歯根膿瘍・歯周病などにより採食困難・流涎・疼痛・体重減少を呈する。"
        "口腔検査と歯科X線で評価し、歯冠調整・抜歯・抗菌療法と栄養支持を行う。",
        "{n} is a dental/oral disease of {s} in which malocclusion, tooth-root abscessation or periodontal disease "
        "causes difficulty eating, drooling, pain and weight loss. Oral examination and dental radiography guide "
        "crown reduction, extraction, antimicrobial therapy and nutritional support.",
    ),
    "dermatological": (
        "{n}は、{s}の皮膚・被毛に生じる疾患である。脱毛・掻痒・発赤・痂皮・二次感染などを呈する。"
        "皮膚掻爬・細胞診・培養で原因を特定し、原因療法と局所・全身療法を組み合わせる。",
        "{n} is a dermatological disease of {s} presenting with alopecia, pruritus, erythema, crusting and "
        "secondary infection. Skin scrapings, cytology and culture identify the cause, guiding combined "
        "topical and systemic therapy.",
    ),
    "hematological": (
        "{n}は、{s}の血液・造血系に生じる疾患である。赤血球・白血球・血小板または凝固系の異常により貧血・出血・易感染を呈する。"
        "血球計算・血液塗抹・凝固検査で評価し、輸血・免疫抑制・原因療法を行う。",
        "{n} is a haematological disease of {s} in which abnormalities of red cells, white cells, platelets or "
        "coagulation cause anaemia, bleeding or susceptibility to infection. Complete blood count, blood smear "
        "and coagulation testing guide transfusion, immunosuppression and cause-specific therapy.",
    ),
    "reproductive": (
        "{n}は、{s}の生殖器系に生じる疾患である。生殖器の感染・腫瘍・ホルモン異常や周産期の合併症として発症する。"
        "触診・画像診断・ホルモン検査で評価し、内科的管理あるいは外科的治療（避妊・去勢を含む）を行う。",
        "{n} is a reproductive disease of {s} arising from genital infection, neoplasia, hormonal imbalance or "
        "peripartum complications. Palpation, imaging and hormone assays guide medical management or surgery, "
        "including spay/neuter.",
    ),
    "toxicity": (
        "{n}は、{s}における有害物質の曝露により生じる中毒性疾患である。摂取・吸入・経皮曝露した毒物が標的臓器を傷害する。"
        "曝露歴と臨床徴候から診断し、除染・拮抗薬・支持療法を迅速に行う。",
        "{n} is a toxicological condition of {s} caused by exposure to a harmful substance that injures target "
        "organs after ingestion, inhalation or dermal contact. Diagnosis rests on exposure history and clinical "
        "signs, with prompt decontamination, antidotes and supportive care.",
    ),
    "trauma": (
        "{n}は、{s}における外力により生じる外傷性疾患である。挫傷・裂傷・骨折・内臓損傷などを生じ、出血やショックを伴いうる。"
        "全身状態の安定化を最優先とし、創傷管理・整復・疼痛管理を行う。",
        "{n} is a traumatic condition of {s} resulting from external force, producing contusions, lacerations, "
        "fractures or internal injury that may be accompanied by haemorrhage and shock. Stabilisation takes "
        "priority, followed by wound management, reduction and analgesia.",
    ),
    "autoimmune": (
        "{n}は、{s}にみられる免疫介在性疾患である。自己組織に対する異常な免疫応答が標的臓器を傷害する。"
        "除外診断と免疫学的検査で診断し、免疫抑制療法と支持療法で管理する。",
        "{n} is an immune-mediated disease of {s} in which an aberrant immune response against self tissue damages "
        "target organs. Diagnosis is by exclusion with immunological testing, and management relies on "
        "immunosuppression and supportive care.",
    ),
    "nutritional": (
        "{n}は、{s}における必須栄養素の欠乏・過剰・不均衡により生じる栄養性疾患である。"
        "骨格・皮膚・神経・代謝など多系統に影響し、飼育下では食餌内容の不備が主因となる。"
        "食餌歴と血液検査で評価し、食餌是正と栄養補給により管理する。",
        "{n} is a nutritional disease of {s} caused by deficiency, excess or imbalance of essential nutrients, "
        "affecting skeletal, dermatological, neurological and metabolic systems. In captivity it usually stems "
        "from an inadequate diet, and management centres on dietary correction and supplementation.",
    ),
    "genetic_congenital": (
        "{n}は、{s}にみられる遺伝性・先天性疾患である。遺伝的素因または発生過程の異常により出生時または若齢期から徴候が現れる。"
        "臨床・画像・遺伝学的検査で診断し、対症療法と生活管理、繁殖計画への配慮を行う。",
        "{n} is a genetic/congenital disorder of {s} in which inherited predisposition or developmental "
        "abnormality produces signs from birth or early life. Clinical, imaging and genetic testing establish "
        "the diagnosis, with symptomatic care, husbandry adjustment and breeding considerations.",
    ),
    "degenerative": (
        "{n}は、{s}にみられる変性性・加齢性疾患である。組織の進行性変性により機能が緩徐に低下する。"
        "臨床経過と画像診断で評価し、進行抑制・症状緩和・QOL維持を目標に管理する。",
        "{n} is a degenerative/age-related disease of {s} in which progressive tissue degeneration causes a "
        "gradual decline in function. Clinical course and imaging guide management aimed at slowing progression, "
        "relieving signs and maintaining quality of life.",
    ),
    "behavioral": (
        "{n}は、{s}にみられる行動学的疾患である。環境・社会・神経生物学的要因が複合し、不安・攻撃性・常同行動などとして発現する。"
        "病歴と行動評価で診断し、行動修正・環境エンリッチメント・必要に応じた薬物療法を組み合わせる。",
        "{n} is a behavioural disorder of {s} arising from a combination of environmental, social and "
        "neurobiological factors, expressed as anxiety, aggression or stereotypies. History and behavioural "
        "assessment guide management with behaviour modification, enrichment and, where indicated, medication.",
    ),
    "generic": (
        "{n}は、{s}にみられる疾患である。原因・病態・進行段階により臨床像は多様で、初期の局所障害から全身性合併症に進展しうる。"
        "病歴・身体検査・各種検査で診断し、原因療法と支持療法を組み合わせて管理する。早期発見・早期治療が予後改善の鍵となる。",
        "{n} is a disease of {s} whose presentation varies with cause, pathophysiology and stage, potentially "
        "progressing from localised dysfunction to systemic complications. History, physical examination and "
        "diagnostics establish the diagnosis, and management combines cause-specific and supportive care, with "
        "early detection key to a better prognosis.",
    ),
}


def gen_description_ja(category: str, name_ja: str, species: str) -> str:
    """Concise disease-specific Japanese description (replaces category templates)."""
    sp_ja = SPECIES_JA.get(species, species)
    name = _clean_name(name_ja) or f"{sp_ja}の疾患"
    ja, _ = _DESC_CATEGORY.get(category, _DESC_CATEGORY["generic"])
    return ja.format(n=name, s=sp_ja)


def gen_description(category: str, name_en: str, species: str) -> str:
    """Concise disease-specific English description (replaces category templates)."""
    sp_en = SPECIES_EN.get(species, species)
    name = _clean_name(name_en) or f"This {sp_en[:-1] if sp_en.endswith('s') else sp_en} disease"
    _, en = _DESC_CATEGORY.get(category, _DESC_CATEGORY["generic"])
    return en.format(n=name, s=sp_en)


# ---------------------------------------------------------------------------
# Grounded descriptions
# ---------------------------------------------------------------------------
#
# The plain ``gen_description*`` helpers above only slot the disease name and
# species into a per-category paragraph, so every neoplasm (or every viral
# infection, …) of a species ends up with a *structurally identical* headline.
# Normalising out the name + species reveals these as templates even though the
# raw strings differ — an immediate "generic AI" tell when a clinician opens the
# database.
#
# ``compose_grounded_description*`` instead build a short clinical summary out of
# the data that is actually curated *per disease* in each record: its own
# presenting signs, its own recommended diagnostic work-up and its triage
# urgency. The result varies disease-to-disease (different sign set, different
# test set, different urgency) and reads like a real one-line summary rather than
# boilerplate. It only restates facts already stored in the record, so it adds no
# new (and therefore no unverified) medical claims.

# Short noun describing each category, used as the lead clause.
_CATEGORY_NOUN_JA: dict[str, str] = {
    "viral_infection": "ウイルス感染症",
    "bacterial_infection": "細菌感染症",
    "respiratory_infection": "呼吸器感染症",
    "fungal_infection": "真菌感染症",
    "parasitic": "寄生虫性疾患",
    "neoplasia": "腫瘍性疾患",
    "endocrine_metabolic": "内分泌・代謝疾患",
    "renal_urinary": "泌尿器疾患",
    "cardiac": "循環器疾患",
    "respiratory_other": "呼吸器疾患",
    "gastrointestinal": "消化器疾患",
    "neurological": "神経疾患",
    "ophthalmic": "眼疾患",
    "musculoskeletal": "運動器疾患",
    "dental": "歯科疾患",
    "dermatological": "皮膚疾患",
    "hematological": "血液疾患",
    "reproductive": "生殖器疾患",
    "toxicity": "中毒性疾患",
    "trauma": "外傷性疾患",
    "autoimmune": "免疫介在性疾患",
    "nutritional": "栄養性疾患",
    "genetic_congenital": "遺伝性・先天性疾患",
    "degenerative": "変性性疾患",
    "behavioral": "行動学的疾患",
    "generic": "疾患",
}

_CATEGORY_NOUN_EN: dict[str, str] = {
    "viral_infection": "viral infection",
    "bacterial_infection": "bacterial infection",
    "respiratory_infection": "respiratory infection",
    "fungal_infection": "fungal infection",
    "parasitic": "parasitic disease",
    "neoplasia": "neoplastic disease",
    "endocrine_metabolic": "endocrine/metabolic disorder",
    "renal_urinary": "urinary-tract disorder",
    "cardiac": "cardiovascular disorder",
    "respiratory_other": "respiratory disorder",
    "gastrointestinal": "gastrointestinal disorder",
    "neurological": "neurological disorder",
    "ophthalmic": "ophthalmic disorder",
    "musculoskeletal": "musculoskeletal disorder",
    "dental": "dental disorder",
    "dermatological": "dermatological disorder",
    "hematological": "haematological disorder",
    "reproductive": "reproductive disorder",
    "toxicity": "toxicosis",
    "trauma": "traumatic injury",
    "autoimmune": "immune-mediated disease",
    "nutritional": "nutritional disorder",
    "genetic_congenital": "genetic/congenital disorder",
    "degenerative": "degenerative disorder",
    "behavioral": "behavioural disorder",
    "generic": "disorder",
}

_URGENCY_CLAUSE_JA: dict[str, str] = {
    "emergency": "緊急性が高く、診断後は速やかな治療介入を要する。",
    "high": "早期の診断と治療が予後を大きく左右する。",
}

_URGENCY_CLAUSE_EN: dict[str, str] = {
    "emergency": "It is an emergency that requires prompt intervention once diagnosed.",
    "high": "Early diagnosis and treatment strongly influence the outcome.",
}


def _join_ja(items: list[str], limit: int) -> str:
    seen: list[str] = []
    for it in items:
        it = (it or "").strip()
        if it and it not in seen:
            seen.append(it)
        if len(seen) >= limit:
            break
    return "・".join(seen)


def _join_en(items: list[str], limit: int) -> str:
    seen: list[str] = []
    for it in items:
        it = (it or "").strip()
        if it and it not in seen:
            seen.append(it)
        if len(seen) >= limit:
            break
    if len(seen) <= 1:
        return "".join(seen)
    return ", ".join(seen[:-1]) + " and " + seen[-1]


def compose_grounded_description_ja(
    name_ja: str,
    species: str,
    category: str,
    sign_names_ja: list[str],
    test_names_ja: list[str],
    urgency: str,
) -> str:
    """Build a per-disease Japanese summary from the record's own curated data."""
    sp_ja = SPECIES_JA.get(species, species)
    name = _clean_name(name_ja) or f"{sp_ja}の疾患"
    noun = _CATEGORY_NOUN_JA.get(category, _CATEGORY_NOUN_JA["generic"])
    parts = [f"{name}は{sp_ja}にみられる{noun}。"]
    signs = _join_ja(sign_names_ja, 5)
    if signs:
        parts.append(f"主な臨床徴候は{signs}など。")
    tests = _join_ja(test_names_ja, 4)
    if tests:
        parts.append(f"診断には{tests}などを用いる。")
    clause = _URGENCY_CLAUSE_JA.get((urgency or "").lower())
    if clause:
        parts.append(clause)
    return "".join(parts)


def compose_grounded_description(
    name_en: str,
    species: str,
    category: str,
    sign_names_en: list[str],
    test_names_en: list[str],
    urgency: str,
) -> str:
    """Build a per-disease English summary from the record's own curated data."""
    sp_en = SPECIES_EN.get(species, species)
    name = _clean_name(name_en) or f"This {sp_en[:-1] if sp_en.endswith('s') else sp_en} disorder"
    noun = _CATEGORY_NOUN_EN.get(category, _CATEGORY_NOUN_EN["generic"])
    article = "an" if noun[0] in "aeiou" else "a"
    parts = [f"{name} is {article} {noun} of {sp_en}."]
    signs = _join_en(sign_names_en, 5)
    if signs:
        parts.append(f"Common clinical signs include {signs}.")
    tests = _join_en(test_names_en, 4)
    if tests:
        parts.append(f"Work-up typically uses {tests}.")
    clause = _URGENCY_CLAUSE_EN.get((urgency or "").lower())
    if clause:
        parts.append(clause)
    return " ".join(parts)


# The category prevention generators (``gen_prevention_ja`` / ``_prevention_*``)
# produce husbandry + category guidance keyed only on (species, category), so
# every disease of one category for a species shares a byte-identical paragraph
# once the disease name is normalised out. That reads as boilerplate when a
# clinician opens several diseases in a row.
#
# ``compose_grounded_prevention_ja`` keeps that vetted category/husbandry base
# (which is genuinely correct) but appends a surveillance clause built from the
# *disease's own* curated presenting signs, so the early-detection targets differ
# disease-to-disease. It only restates signs already stored on the record, adding
# no new medical claims, and is the prevention analogue of
# ``compose_grounded_description_ja``.


def compose_grounded_prevention_ja(base_text: str, sign_names_ja: list[str]) -> str:
    """Append a disease-specific early-detection clause to category prevention.

    ``base_text`` is the category/husbandry prevention paragraph; ``sign_names_ja``
    are the record's own presenting signs (Japanese). Returns ``base_text``
    unchanged when there are too few usable signs to add value.
    """
    base = (base_text or "").strip()
    # Use signs not already named in the base, so the clause adds information.
    fresh = [s for s in sign_names_ja if s and s not in base]
    signs = _join_ja(fresh or sign_names_ja, 4)
    if not signs or signs.count("・") < 1:
        # Need at least two distinct signs for a meaningful surveillance list.
        return base
    clause = f"早期発見には{signs}などの変化を見逃さず、異常時は速やかに受診することが重要。"
    if clause in base:
        return base
    return f"{base}{clause}"


def compose_grounded_prognosis_ja(base_text: str, sign_names_ja: list[str]) -> str:
    """Append a disease-specific monitoring clause to category prognosis.

    The category prognosis paragraph is shared across every disease of a
    category. Tracking the trajectory of a patient's own presenting signs to
    gauge treatment response is routine clinical practice, so appending the
    record's curated signs as monitoring targets makes the prognosis vary
    per disease without adding any unverified medical claim. Returns
    ``base_text`` unchanged when there are too few usable signs.
    """
    base = (base_text or "").strip()
    fresh = [s for s in sign_names_ja if s and s not in base]
    signs = _join_ja(fresh or sign_names_ja, 4)
    if not signs or signs.count("・") < 1:
        return base
    clause = f"経過中は{signs}などの推移を指標に重症度と治療反応を評価する。"
    if clause in base or "の推移を指標に" in base:
        return base
    return f"{base}{clause}"


# English analogues of the two grounding composers above. The English
# prevention / prognosis fields are, for most diseases, the raw category
# paragraph shared byte-for-byte across every disease of a category (only ~600
# distinct causes strings across 7k diseases), so an English-language visitor
# browsing several diseases sees the identical paragraph — the classic "generic
# AI" tell. These keep the vetted category base and append a surveillance /
# monitoring clause built from the record's *own* presenting signs (English),
# restating data already stored on the record with no new medical claim.


def compose_grounded_prevention(base_text: str, sign_names_en: list[str]) -> str:
    """Append a disease-specific early-detection clause to category prevention (EN)."""
    base = (base_text or "").strip()
    fresh = [s for s in sign_names_en if s and s not in base]
    signs = _join_en(fresh or sign_names_en, 4)
    # ``_join_en`` only emits " and " when there are >= 2 distinct signs; require
    # that so the surveillance list is meaningful.
    if not signs or " and " not in signs:
        return base
    clause = f" Early detection relies on watching for {signs}, with prompt veterinary assessment if they develop."
    if clause.strip() in base or "Early detection relies on watching for" in base:
        return base
    return f"{base}{clause}"


def compose_grounded_prognosis(base_text: str, sign_names_en: list[str]) -> str:
    """Append a disease-specific monitoring clause to category prognosis (EN)."""
    base = (base_text or "").strip()
    fresh = [s for s in sign_names_en if s and s not in base]
    signs = _join_en(fresh or sign_names_en, 4)
    if not signs or " and " not in signs:
        return base
    clause = f" Tracking the course of {signs} helps gauge severity and treatment response."
    if clause.strip() in base or "helps gauge severity and treatment response" in base:
        return base
    return f"{base}{clause}"


# Pathophysiology, unlike causes, is by definition the mechanism -> clinical
# manifestation chain, so tying the category-level mechanism paragraph to the
# record's OWN presenting signs (as the observed manifestation) is medically
# natural and, like the composers above, only restates data already on the
# record — no new claim. (Causes / etiology cannot be sign-grounded, because a
# clinical sign is not an aetiology; that field is left to named-agent curation.)


def compose_grounded_pathophysiology_ja(base_text: str, sign_names_ja: list[str]) -> str:
    """Append a disease-specific clinical-manifestation clause to category pathophysiology (JA)."""
    base = (base_text or "").strip()
    fresh = [s for s in sign_names_ja if s and s not in base]
    signs = _join_ja(fresh or sign_names_ja, 5)
    if not signs or signs.count("・") < 1:
        return base
    clause = f"本症例では臨床的に{signs}などとして顕在化する。"
    if clause in base or "などとして顕在化する" in base:
        return base
    return f"{base}{clause}"


def compose_grounded_pathophysiology(base_text: str, sign_names_en: list[str]) -> str:
    """Append a disease-specific clinical-manifestation clause to category pathophysiology (EN)."""
    base = (base_text or "").strip()
    fresh = [s for s in sign_names_en if s and s not in base]
    signs = _join_en(fresh or sign_names_en, 5)
    if not signs or " and " not in signs:
        return base
    clause = f" In this disease the process manifests clinically as {signs}."
    if clause.strip() in base or "the process manifests clinically as" in base:
        return base
    return f"{base}{clause}"


# ---------------------------------------------------------------------------
# Cross-species breed-clause filter
# ---------------------------------------------------------------------------
# Several category templates embed dog- (and a few cat-) breed predispositions —
# e.g. the neurological aetiology template names "Border Collie storm anxiety",
# the cardiac prevention template lists Doberman/Cocker Spaniel/Maine Coon. When
# such a template is applied to an unrelated species (a horse's lameness, a
# rabbit's seizures) the breed clause becomes cross-species contamination that a
# clinician spots immediately. Each rule replaces one EXACT template fragment
# with a species-neutral (or removed) version for species the breed does not
# apply to. Using fixed fragments — not bare breed tokens — means zero false
# positives (bare "コリー" would hit ブロッコリー, "ゴールデン" ゴールデンハムスター,
# "ベンガル" ローズベンガル染色, "ヨークシャー" the Yorkshire pig).
_BREED_DOG = frozenset({"dog"})
_BREED_DOG_CAT = frozenset({"dog", "cat"})

# (exact_fragment, species_where_kept, replacement_for_other_species)
_BREED_CLAUSE_RULES: tuple[tuple[str, frozenset, str], ...] = (
    # causes_ja
    (
        "品種特異的好発性（コリーのCDS、ボーダーコリーのストーム不安、特発性てんかんの素因犬種）も重要な背景因子。",
        _BREED_DOG,
        "",
    ),
    (
        "心筋症（DCM/HCM）の素因犬種・猫品種、変性性弁膜疾患（小型犬の僧帽弁粘液腫様変性）、先天性心奇形（PDA・VSD・ASD）、不整脈源性心筋症が主要病因。",
        _BREED_DOG_CAT,
        "心筋症（拡張型・肥大型）、変性性弁膜疾患、先天性心奇形（PDA・VSD・ASD）、不整脈源性心筋症が主要病因。",
    ),
    (
        "アレルギー性（猫喘息・好酸球性気管支炎）、解剖学的異常（短頭種気道症候群BOAS・気管虚脱・喉頭麻痺）、腫瘍性、栄養性（肥満による拘束性換気障害）、慢性炎症性（COPD様病態）、誤嚥性が含まれる。",
        _BREED_DOG_CAT,
        "アレルギー性・好酸球性気管支炎、解剖学的異常（気管虚脱・喉頭麻痺）、腫瘍性、栄養性（肥満による拘束性換気障害）、慢性炎症性（COPD様病態）、誤嚥性が含まれる。",
    ),
    (
        "短頭種・気道解剖学的異常を有する個体、若齢・高齢、免疫抑制状態は重症化しやすい。",
        _BREED_DOG_CAT,
        "気道解剖学的異常を有する個体、若齢・高齢、免疫抑制状態は重症化しやすい。",
    ),
    ("小型犬・短頭種では歯列圧迫による歯周病が多発。", _BREED_DOG_CAT, ""),
    # prevention_ja
    (
        "屋外アクセス制限（猫の屋内飼育）、リード散歩の徹底、自宅内の鋭利物・落下物の除去、滑床対策（マット）、階段事故予防（小型犬・高齢動物）。",
        _BREED_DOG_CAT,
        "鋭利物・落下物の除去、滑床対策（マット）、高所からの落下・脱走防止など飼育環境の安全管理。",
    ),
    (
        "発達性疾患（HD・ED・OCD・FCP）予防: 大型犬の成長期過剰カロリー回避、適切なカルシウム/リン比、過度な運動・階段使用回避。",
        _BREED_DOG,
        "発達性疾患予防: 成長期の過剰カロリー回避、適切なカルシウム/リン比、過度な運動の回避。",
    ),
    (
        "角膜潰瘍: 短頭種の眼球突出予防（眼球保護環境）、グルーミング時の眼科ケア。",
        _BREED_DOG_CAT,
        "角膜潰瘍: 眼外傷の予防、グルーミング時の眼科ケア。",
    ),
    (
        "DCM/HCM素因品種（ドーベルマン・コッカースパニエル・メインクーン・ラグドール）の繁殖前心エコースクリーニング。",
        _BREED_DOG_CAT,
        "",
    ),
    ("短頭種気道症候群: 適正体重維持、暑熱環境回避、必要に応じた外科的気道形成術。", _BREED_DOG_CAT, ""),
    # clinical_signs_ja
    (
        "上気道: いびき・吸気性ストライダー・運動不耐性・吸気性チアノーゼ（短頭種気道症候群）。",
        _BREED_DOG_CAT,
        "上気道: いびき・吸気性ストライダー・運動不耐性・吸気性チアノーゼ。",
    ),
    # pathophysiology_ja
    (
        "上気道閉塞（喉頭麻痺・気管虚脱・短頭種気道症候群）では吸気抵抗増大→陰圧性気道虚脱→気道炎症の悪循環を生じる。",
        _BREED_DOG_CAT,
        "上気道閉塞（喉頭麻痺・気管虚脱）では吸気抵抗増大→陰圧性気道虚脱→気道炎症の悪循環を生じる。",
    ),
    (
        "短頭種気道症候群・気管虚脱・喉頭麻痺は解剖学的素因によるもので、品種ごとの遺伝的素因が背景にある。",
        _BREED_DOG_CAT,
        "気管虚脱・喉頭麻痺は解剖学的素因によるものである。",
    ),
    ("短頭種は眼球露出・涙液分布不良・角膜知覚低下から難治性・自然発生性の潰瘍が多い。", _BREED_DOG_CAT, ""),
    # differential_diagnosis_ja (parenthetical within a valuable differential list)
    ("（短頭種気道症候群・気管虚脱・喉頭麻痺）", _BREED_DOG_CAT, "（気管虚脱・喉頭麻痺）"),
    # rehabilitation_protocol_ja
    ("短頭種気道症候群: 適正体重維持、暑熱回避、ハーネス使用、術後の段階的活動再開。", _BREED_DOG_CAT, ""),
    # transmission_ja
    ("遺伝性眼疾患（コリーアイ症候群・PRA等）は親から子へ継承される。", _BREED_DOG, ""),
    (
        "不正咬合の遺伝性素因（短頭種・小型犬）は親から子へ継承される。",
        _BREED_DOG_CAT,
        "不正咬合の遺伝性素因は親から子へ継承される。",
    ),
    # nutrition_management_ja
    (
        "L-カルニチン補給（DCM疑い犬・ボクサー・ドーベルマン）。",
        _BREED_DOG,
        "L-カルニチン補給（拡張型心筋症疑い例）。",
    ),
    # prognosis_ja (DCM tuple) — fixed sub-fragment, name prefix precedes it
    (
        "予後は基礎疾患として予後不良で、特にドーベルマンでは突然死リスクが高い。",
        _BREED_DOG,
        "予後は基礎疾患として予後不良である。",
    ),
    # misc toxicity / infection templates naming a dog size class
    (
        "好奇心の強い若齢個体や大量摂取が可能な大型犬で発生が多い。",
        _BREED_DOG,
        "好奇心の強い若齢個体や大量に摂取した個体で発生が多い。",
    ),
    ("浅い眼窩を持つ種（短頭種等）で発生リスクが高い。", _BREED_DOG_CAT, "浅い眼窩を持つ種で発生リスクが高い。"),
    ("水辺・湿潤な土壌が感染源で、若齢大型犬に多い。", _BREED_DOG, "水辺・湿潤な土壌が感染源となる。"),
    (
        "甘くコーティングされた鉄錠剤を大量に誤食した小型犬で重症化しやすい。",
        _BREED_DOG,
        "甘くコーティングされた鉄錠剤を大量に誤食した個体で重症化しやすい。",
    ),
    # English fields
    ("Hereditary ocular disease (collie eye anomaly, PRA) is inherited from parent to offspring.", _BREED_DOG, ""),
    (
        "Brachycephalic airway syndrome, tracheal collapse and laryngeal paralysis arise from anatomical predisposition with a breed-specific genetic background.",
        _BREED_DOG_CAT,
        "Tracheal collapse and laryngeal paralysis arise from anatomical predisposition.",
    ),
    (
        "Hereditary predisposition to malocclusion (brachycephalic and small-breed dogs) is inherited.",
        _BREED_DOG_CAT,
        "Hereditary predisposition to malocclusion is inherited.",
    ),
    (" (brachycephalic airway syndrome)", _BREED_DOG_CAT, ""),
    ("brachycephalic conformational abnormalities, ", _BREED_DOG_CAT, ""),
    (
        ", with a high risk of sudden death, particularly in Dobermans.",
        _BREED_DOG,
        ", with a high risk of sudden death.",
    ),
    ("Weight management reduces respiratory compromise in brachycephalic breeds.", _BREED_DOG_CAT, ""),
    # Curated Wobbler (cervical spondylomyelopathy) entry describes both the dog
    # and horse forms in one string; keep the dog comparison only on dog records.
    (
        "大型犬（椎間板関連型）・ドーベルマン等、馬（頸椎奇形/不安定）でみられ、遺伝・急速成長・栄養が関与する。",
        _BREED_DOG,
        "頸椎の奇形・不安定性によって生じ、遺伝・急速な成長・栄養が関与する。",
    ),
    (
        " — in large-breed dogs (disc-associated), Dobermanns, and horses (cervical malformation/instability); genetics, rapid growth and nutrition contribute.",
        _BREED_DOG,
        " from cervical vertebral malformation and instability; genetics, rapid growth and nutrition contribute.",
    ),
)


def filter_species_inapplicable_clauses(text: str, species: str) -> str:
    """Strip cross-species breed clauses inapplicable to ``species`` from ``text``.

    A no-op for dog/cat records (their own breed clauses are kept) and for any
    text that contains none of the template fragments. Safe on already-clean or
    curated content because every rule matches an exact template fragment.
    """
    if not text:
        return text
    sp = (species or "").strip().lower()
    out = text
    changed = False
    for fragment, kept_species, replacement in _BREED_CLAUSE_RULES:
        if sp in kept_species:
            continue
        if fragment in out:
            out = out.replace(fragment, replacement)
            changed = True
    if changed:
        # Tidy stray artefacts left by removals (e.g. two adjacent 。 or spaces).
        out = out.replace("。。", "。").replace("． ", ". ").replace("  ", " ").strip()
    return out


# ---------------------------------------------------------------------------
# Frozen-organ correction for the exotic "degenerative" English aetiology
# ---------------------------------------------------------------------------
# The exotic-species generator (scripts/enrichment/generate_all_exotic.py) froze
# the organ word to "cardiovascular" for every degenerative English `causes`
# field, so Cataracts, Osteoarthritis, Chronic Kidney Disease etc. all read
# "Caused by progressive deterioration of cardiovascular tissues …". The organ
# is deterministically recoverable from the disease name, so this is a pure bug
# fix (no fabrication): swap "cardiovascular" for the organ the name denotes.
_FROZEN_ORGAN_MARK = "progressive deterioration of cardiovascular tissue"

# Ordered (regex, organ_en) — first match on the English/Japanese name wins.
_NAME_ORGAN_EN: tuple[tuple[re.Pattern, str], ...] = (
    (
        re.compile(
            r"cardiomyopath|heart|cardiac|cardiovascular|aortic|arterioscler|"
            r"atheroscler|myocard|cor pulmonale|心筋|心臓|心不全|動脈|心血管",
            re.I,
        ),
        "cardiovascular",
    ),
    (re.compile(r"catarac|retina|ocular|\beye\b|lens|glaucoma|uveitis|白内障|網膜|眼", re.I), "ocular"),
    (
        re.compile(
            r"osteoarthr|arthritis|spondylo|joint|osteo|bone|skeletal|luxat|"
            r"関節|骨|脊椎|変形性",
            re.I,
        ),
        "musculoskeletal",
    ),
    (re.compile(r"nephro|kidney|renal|urinary|bladder|腎|尿", re.I), "renal and urinary"),
    (
        re.compile(
            r"neuropath|nerve|neural|cerebell|ataxia|myelopath|cauda equina|"
            r"intervertebral|\bdisc\b|wobbly|spinal|paresis|paralysis|"
            r"神経|脊髄|椎間板|運動失調|麻痺|ふらつき",
            re.I,
        ),
        "nervous system",
    ),
    (re.compile(r"pulmonary|tracheal|respiratory|bronch|lung|肺|気管|呼吸", re.I), "respiratory"),
    (
        re.compile(
            r"molar|cheek teeth|dental|tooth|teeth|slobber|malocclus|"
            r"臼歯|歯|不正咬合",
            re.I,
        ),
        "dental",
    ),
    (re.compile(r"hepat|liver|肝", re.I), "hepatic"),
    # Generic multi-organ ageing syndromes (amyloidosis, geriatric, age-related
    # degenerative) — no single organ, but "cardiovascular" is still wrong.
    (re.compile(r"amyloid|geriatric|age-related|老齢|加齢|老化", re.I), "multiple organ"),
)


def correct_degenerative_organ_en(name_ja: str, name_en: str, causes_en: str) -> str:
    """Fix the frozen "cardiovascular" organ in the degenerative English aetiology.

    Returns ``causes_en`` unchanged unless it carries the frozen-organ template
    AND the disease name denotes a non-cardiac organ system. Never fabricates —
    only substitutes the organ noun the name already implies.
    """
    if not causes_en or _FROZEN_ORGAN_MARK not in causes_en:
        return causes_en
    name = f"{name_en or ''} {name_ja or ''}"
    organ = None
    for pattern, org in _NAME_ORGAN_EN:
        if pattern.search(name):
            organ = org
            break
    if organ is None or organ == "cardiovascular":
        # Genuinely cardiac, or name gives no confident organ — leave untouched.
        return causes_en
    return causes_en.replace("cardiovascular tissue", f"{organ} tissue")


# ---------------------------------------------------------------------------
# Etiology / pathophysiology re-categorisation
# ---------------------------------------------------------------------------
# The causes_ja / pathophysiology_ja fields were generated by ``gen_causes_ja``
# / ``gen_pathophysiology_ja`` keyed on a stored category that is sometimes
# wrong — e.g. ferret adrenal disease received the *renal* etiology template
# (because "Adrenal" contains "renal"), and many non-toxicoses (anaesthetic
# complications, retained fetus, hepatic disease) received the *toxicity*
# template that falsely lists "chocolate / lily ingestion" as the cause.
#
# These helpers identify which category template a record currently carries
# (name-independent fingerprint) and decide the correct category from the
# disease *name*. Only a confident contradiction triggers a switch, so a record
# is never made worse; genuinely toxic diseases keep the toxicity category (and
# are merely re-rendered with species-appropriate toxin examples).

_ETIOLOGY_CATS: list[str] = [
    "viral_infection",
    "bacterial_infection",
    "respiratory_infection",
    "fungal_infection",
    "parasitic",
    "neoplasia",
    "endocrine_metabolic",
    "renal_urinary",
    "cardiac",
    "respiratory_other",
    "gastrointestinal",
    "neurological",
    "ophthalmic",
    "musculoskeletal",
    "dental",
    "dermatological",
    "hematological",
    "reproductive",
    "toxicity",
    "trauma",
    "autoimmune",
    "nutritional",
    "genetic_congenital",
    "degenerative",
    "behavioral",
    "generic",
]

# Near-synonym category pairs whose distinction is a coin-flip for etiology
# (e.g. pneumonia "respiratory infection" vs "respiratory other"). Never switch
# between these — it would just churn text without improving accuracy.
_NOISE_PAIRS: frozenset[tuple[str, str]] = frozenset(
    {
        ("respiratory_infection", "respiratory_other"),
        ("respiratory_other", "respiratory_infection"),
        ("genetic_congenital", "degenerative"),
        ("degenerative", "genetic_congenital"),
    }
)

# A name that genuinely denotes a toxicosis — keep the toxicity category even if
# an organ-system keyword (e.g. 神経型 in 鉛中毒（神経型）) would otherwise win.
_TOXIC_NAME_RE = re.compile(
    r"中毒|毒性|毒素|毒物|poison|toxic|intoxic|油汚染|硝酸塩|フッ素症|鉄過剰|"
    r"メトヘモグロビン|煙吸入|パーキンソニズム|殺鼠|農薬|重金属|鉛|銅中毒|ヒ素|"
    r"キシリトール|エチレングリコール|不凍液|アフラトキシン|モネンシン"
)

# A name whose etiology is fundamentally nutritional (vitamin/mineral
# deficiency) — keep the nutritional causes category even when an affected-organ
# keyword (e.g. 眼型 in ビタミンA欠乏症（眼型）) resolves to that organ system.
_NUTRITIONAL_NAME_RE = re.compile(r"欠乏|ビタミン|壊血病|deficiency|scurvy")


_FP_NAME = "ＮＡＭＥ"  # placeholder unlikely to collide with real text
_FP_SPECIES = "ＳＰＣ"  # sentinel species (absent from SPECIES_JA -> used verbatim)
_FP_MIN_CHUNK = 20


def build_etiology_fingerprints(gen_fn) -> dict[str, list[str]]:
    """Return {category: [name/species-independent marker fragments]}.

    ``gen_fn`` is ``gen_causes_ja`` or ``gen_pathophysiology_ja``. Rendering the
    template with sentinel disease *and* species names, splitting into sentences
    and stripping the sentinels (and the "における" lead-in) yields boilerplate
    fragments independent of the disease name **and** the species. A record
    matches its category if *any* fragment is a substring of its text, so
    detection stays robust when one sentence is later edited (e.g. re-speciating
    the toxicity examples): the other stable fragments still identify the
    template in already-baked data of any species.
    """
    fps: dict[str, list[str]] = {}
    for cat in _ETIOLOGY_CATS:
        rendered = gen_fn(cat, _FP_NAME, _FP_SPECIES)
        frags = []
        for sentence in rendered.split("。"):
            residual = sentence.replace(_FP_NAME, "").replace(_FP_SPECIES, "").replace("における", "")
            if len(residual) >= _FP_MIN_CHUNK:
                frags.append(residual)
        if frags:
            fps[cat] = frags
    return fps


def fingerprint_etiology(text: str, fingerprints: dict[str, list[str]]) -> Optional[str]:
    """Return the category whose template fragments appear in ``text``, else None.

    None means the text is curated / disease-specific (no category template) and
    must be left untouched.
    """
    if not text:
        return None
    for cat, chunks in fingerprints.items():
        if any(chunk in text for chunk in chunks):
            return cat
    return None


def decide_etiology_category(name_ja: str, name_en: str, applied: str) -> str:
    """Return the category the etiology text *should* use, given the applied one.

    Returns ``applied`` unchanged unless the disease name confidently indicates a
    different, non-near-synonym category. Genuinely toxic names keep toxicity;
    genuinely nutritional names keep nutritional.
    """
    resolved = resolve_category_from_name(name_ja, name_en)
    name = f"{name_ja or ''} {name_en or ''}"

    if applied == "toxicity":
        # Keep toxicity for real toxicoses (text is still re-rendered with
        # species-appropriate examples elsewhere). Otherwise move off the
        # misleading "ingested a poison" etiology to the resolved category, or
        # the safe generic etiology when the name gives no signal.
        if _TOXIC_NAME_RE.search(name):
            return "toxicity"
        return resolved or "generic"

    if applied == "nutritional" and _NUTRITIONAL_NAME_RE.search(name):
        # Deficiency diseases: etiology is nutritional even if the name carries
        # an affected-organ qualifier (e.g. ビタミンA欠乏症（眼型）).
        return "nutritional"

    if resolved and resolved != applied and (applied, resolved) not in _NOISE_PAIRS:
        return resolved
    return applied


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


# Curated-pattern false positives: a pattern that is a substring of a *different*
# disease name. e.g. "甲状腺機能亢進" (hyperthyroidism) is contained in
# "副甲状腺機能亢進症" (hyperparathyroidism) — a distinct parathyroid disease.
_CURATED_EXCLUSIONS: dict[str, tuple[str, ...]] = {
    "甲状腺機能亢進": ("副甲状腺",),
    "甲状腺機能低下": ("副甲状腺",),
}


def lookup_curated(species: str, name_ja: str, name_en: str) -> Optional[dict]:
    """Look up curated content for this disease. Returns dict of field -> text, or None."""
    name = (name_ja or "") + " " + (name_en or "")
    for (sp, pattern), fields in CURATED.items():
        if sp != species:
            continue
        if pattern not in name:
            continue
        if any(bad in name for bad in _CURATED_EXCLUSIONS.get(pattern, ())):
            continue
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
    # The description is the most visible field, so it never trusts a possibly
    # wrong stored category tag — it falls back to "generic" rather than risk a
    # mis-categorised headline (e.g. impaction labelled a bacterial infection).
    desc_category = resolve_category_from_name(name_ja, name_en) or "generic"

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
        "description_ja": gen_description_ja,
    }

    result: dict[str, str] = {}
    for field in fields_to_generate:
        # Curated content takes priority
        if field in curated:
            result[field] = curated[field]
            continue
        # English description uses the English disease name + name-only category.
        if field == "description":
            result[field] = gen_description(desc_category, name_en, species)
            continue
        if field == "description_ja":
            result[field] = gen_description_ja(desc_category, name_ja, species)
            continue
        # English clinical-signs / transmission use the English disease name.
        if field == "clinical_signs":
            result[field] = gen_clinical_signs(category, name_en, species)
            continue
        if field == "transmission":
            result[field] = gen_transmission(category, name_en, species)
            continue
        if field == "diagnosis_ja":
            result[field] = gen_diagnosis_ja(category, name_ja, species)
            continue
        if field == "diagnosis":
            result[field] = gen_diagnosis(category, name_en, species)
            continue
        # English prognosis embeds the English disease name and is disease-specific.
        if field == "prognosis":
            result[field] = gen_prognosis_en(category, name_en, species)
            continue
        # English prevention: only non-companion species have a class-aware
        # generator (mirroring gen_prevention_ja). The dog/cat companion English
        # prevention has no generator here, so leave it untouched.
        if field == "prevention":
            if _species_class(species) != "companion":
                result[field] = gen_prevention_en_noncompanion(category, name_en, species)
            continue
        gen = GENERATORS.get(field)
        if gen is None:
            continue
        result[field] = gen(category, name_ja, species)
    # Strip any cross-species breed clause the category templates may embed
    # (e.g. "Border Collie storm anxiety" in a non-dog neurological aetiology).
    for field in result:
        result[field] = filter_species_inapplicable_clauses(result[field], species)
    return result


# ``gen_causes`` is the name PR #703's generic_english_causes.py imports for the
# category-aware English aetiology generator. main independently added the same
# generator as ``gen_causes_en``; alias so both callers share one implementation
# (they were byte-for-byte-equivalent mirrors of ``gen_causes_ja``).
gen_causes = gen_causes_en
