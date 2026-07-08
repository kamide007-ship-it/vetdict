"""Sponsor product adjunct annotations for disease treatment fields.

Equine & Canine Vet Nutrition (https://www.caninevet.jp/) products are
appended as a single compact block to applicable disease treatment fields.
The block uses one idempotency marker ([ECVN:Block]) so re-enrichment is safe.

Products:
  For Joint, For Antioxidant, MSM+Amino Complete, NMN Mitochondria Assist,
  CP Powder (Prebiotics+Probiotics+Psyllium), Relax & CBD, Protain,
  Booster & Relax, Kamide Milk
"""

from __future__ import annotations

import re
from typing import Any, Dict, List

# ---------------------------------------------------------------------------
# Disease-name keyword patterns
# ---------------------------------------------------------------------------

_JOINT_PATTERNS = re.compile(
    r"osteoarthrit|arthrit|\bjoint\b|hip dyspl|elbow dyspl|patellar|patella|"
    r"cruciate|\bOCD\b|osteochondr|spondylos|meniscal|meniscus|tendinit|"
    r"\btendon\b|laminit|navicular|suspensory|desmit|sesamoid|"
    r"ringbone|sidebone|bog spavin|bone spavin|splint|bucked shin|"
    r"関節炎|関節|股関節|肘関節|膝蓋骨|十字靱帯|十字靭帯|離断性骨軟骨症|"
    r"脊椎症|半月板|腱炎|腱損傷|蹄葉炎|舟状骨|繋靭帯|種子骨|"
    r"輪骨瘤|側骨瘤|飛節腫|管骨瘤",
    re.IGNORECASE,
)

_ANTIOX_PATTERNS = re.compile(
    r"atopic dermatit|\batop\w*|dermatit|chronic kidney|\bCKD\b|hepatic|"
    r"liver disease|cirrhos|cognitive dysfunc|immune.mediat|auto.?immune|"
    r"pyoderma|\blupus\b|pemphig|seborrhe|"
    r"toxicos|toxicit|poisoning|envenom|snakebite|mamushi|"
    r"rodenticid|bromethalin|cholecalciferol|ivermectin|"
    r"sepsis|septic|\bSIRS\b|peritoniti|"
    r"ehrlichi|babesi|leptospir|tick.?borne|"
    r"vestibular|geriatric|aging|"
    r"glaucoma|cataract|"
    r"アトピー|皮膚炎|慢性腎臓病|肝疾患|肝炎|肝硬変|認知機能|免疫介在|自己免疫|"
    r"中毒|毒|咬傷|マムシ|蛇咬|"
    r"殺鼠剤|ブロメタリン|コレカルシフェロール|イベルメクチン|"
    r"敗血症|腹膜炎|"
    r"エールリヒア|バベシア|レプトスピラ|"
    r"前庭|高齢|加齢|"
    r"緑内障|白内障",
    re.IGNORECASE,
)

_MSM_AMINO_PATTERNS = re.compile(
    r"osteoarthrit|arthrit|\bjoint\b|hip dyspl|elbow dyspl|patellar|patella|"
    r"cruciate|\bOCD\b|osteochondr|spondylos|\bIVDD\b|intervertebral disc|"
    r"disc disease|spinal cord|degenerative myelop|\bDM\b|wobbler|"
    r"meniscal|meniscus|tendinit|\btendon\b|ligament|desmit|myopath|"
    r"myositis|rhabdomyol|muscle\s+(wasting|atroph)|sarcopen|cachex|"
    r"fracture|\btrauma\w*|wound healing|chronic wound|decubit|"
    r"malnutrit|debilit|convalescen|post.?surg|"
    r"hepatic|hepatopath|\bliver\b|cirrhos|hepatic lipidos|cholang|"
    r"hepatic encephalop|portosystem|hepatitis|"
    r"chronic kidney|\bCKD\b|renal failure|nephropath|\bnephritis\b|"
    r"uremia|uraemia|azotemi|glomerulonephr|pyelonephr|renal insuff|"
    r"関節炎|関節|股関節|肘関節|膝蓋骨|十字靱帯|十字靭帯|離断性骨軟骨症|"
    r"脊椎症|椎間板|脊髄|変性性脊髄症|半月板|腱炎|腱|靭帯|筋炎|"
    r"筋萎縮|筋肉減少|悪液質|骨折|外傷|創傷|褥瘡|栄養失調|衰弱|"
    r"回復期|術後|"
    r"肝疾患|肝炎|肝硬変|肝リピドーシス|肝性脳症|門脈体循環シャント|"
    r"胆管肝炎|慢性腎臓病|腎不全|腎症|尿毒症|糸球体腎炎|腎盂腎炎",
    re.IGNORECASE,
)

_NMN_PATTERNS = re.compile(
    r"cognitive dysfunc|\bCDS\b|dementia|degenerative myelop|\bDM\b|wobbler|"
    r"epilep|seizure|hypothyroid|cushing|hyperadrenocort|diabet|\bDKA\b|"
    r"obesity|\bobese\b|dilated cardiomyop|\bDCM\b|hypertrophic cardiomyop|"
    r"\bHCM\b|mitral valve|mvd\b|valvular|congestive heart|aortic stenos|"
    r"patent ductus|cataract|progressive retinal|\bPRA\b|glaucoma|"
    r"hepatic|hepatopath|\bliver\b|cirrhos|cholang|"
    r"chronic kidney|\bCKD\b|\bIMHA\b|autoimmune hemolytic|"
    r"認知機能|認知障害|変性性脊髄症|てんかん|痙攣|甲状腺機能低下|"
    r"クッシング|糖尿病|肥満|拡張型心筋症|肥大型心筋症|僧帽弁|心不全|"
    r"大動脈狭窄|動脈管開存|白内障|進行性網膜萎縮|緑内障|肝疾患|肝炎|"
    r"肝硬変|慢性腎臓病|免疫介在性溶血|溶血性貧血",
    re.IGNORECASE,
)

_PREBIOTIC_PATTERNS = re.compile(
    r"colic|gastroenterit|enterit|diarrh|constipat|megacolon|megaesophag|"
    r"\bGDV\b|gastric dilat|bloat|pancreatit|\bIBD\b|inflammatory bowel|"
    r"chronic enteropath|food allerg|food sensitivit|atopic dermatit|"
    r"allergic dermatit|portosystem|hepatic encephalop|urolithi|"
    r"\bstruvite\b|calcium oxal|cystit|sand colic|impact|"
    r"chronic kidney|\bCKD\b|uremia|uraemia|dysbios|"
    r"gastrinoma|zollinger.?ellison|gastric ulcer|"
    r"疝痛|胃腸炎|腸炎|下痢|便秘|巨大結腸|巨大食道|胃拡張|胃捻転|"
    r"膵炎|炎症性腸疾患|慢性腸症|食物アレルギー|アトピー性皮膚炎|"
    r"アレルギー性皮膚炎|門脈体循環シャント|肝性脳症|尿石症|ストラバイト|"
    r"シュウ酸カルシウム|膀胱炎|砂疝|便塞|慢性腎臓病|尿毒症|腸内細菌叢|"
    r"ガストリノーマ|ゾリンジャー|胃潰瘍",
    re.IGNORECASE,
)

_RELAX_CBD_PATTERNS = re.compile(
    r"osteoarthrit|\barthrit|\bIVDD\b|intervertebral disc|disc disease|"
    r"wobbler|lumbar.?sacral|laryngeal paraly|separation anxiety|"
    r"cognitive dysfunc|\bCDS\b|dementia|"
    r"noise phobia|storm phobia|thunderstorm|generalized anxiety|"
    r"feather.*(pluck|destruct)|self.?mutilat|compulsive|stereotyp|"
    r"cribbing|weaving|wind.?suck|stall walk|head.?shak|"
    r"\bepilep|seizure|refractory seizure|status epilepticus|"
    r"cancer pain|end.?of.?life|palliative|chronic pain|"
    r"変形性関節症|関節炎|椎間板|脊髄|ウォブラー|腰仙部|喉頭麻痺|"
    r"分離不安|騒音恐怖|雷恐怖|全般性不安|てんかん|痙攣|難治性痙攣|"
    r"がん性疼痛|終末期|緩和ケア|慢性疼痛",
    re.IGNORECASE,
)

_PROTAIN_PATTERNS = re.compile(
    r"lymphom|hemangiosarcom|osteosarcom|mammary.*(tumor|neopl)|"
    r"squamous cell carcinom|mast cell tumor|"
    r"cruciate|\bTPLO\b|patellar|hip dyspl|elbow dyspl|"
    r"cachex|sarcopen|muscle wast|obesit|\bobese\b|weight.loss|"
    r"リンパ腫|血管肉腫|骨肉腫|乳腺腫瘍|扁平上皮癌|肥満細胞腫|"
    r"十字靱帯|十字靭帯|膝蓋骨|股関節形成不全|肘関節形成不全|"
    r"悪液質|サルコペニア|筋肉減少|筋萎縮|肥満|減量",
    re.IGNORECASE,
)

_BOOSTER_PATTERNS = re.compile(
    r"canine distemp|parvovir|feline panleuk|feline pneumon|"
    r"upper respiratory|influenza|\bURI\b|kennel cough|"
    r"hypothyroid|hyperthyroid|addison|hypoadrenocort|atypical hypoadrenocort|"
    r"chronic fatigue|debilit|convalescen|poor performance|"
    r"sepsis|septic|\bSIRS\b|peritoniti|pyothora|"
    r"toxicos|toxicit|poisoning|envenom|snakebite|mamushi|"
    r"botulis|tetanus|anaplasm|ehrlichi|babesi|leptospir|"
    r"vestibul|cognitive dysfunc|"
    r"犬ジステンパー|パルボ|汎白血球減少|上部気道感染|"
    r"ケンネルコフ|甲状腺機能低下|甲状腺機能亢進|アジソン|"
    r"副腎皮質機能低下|慢性疲労|衰弱|回復期|"
    r"敗血症|腹膜炎|膿胸|"
    r"中毒|毒|咬傷|マムシ|蛇咬|"
    r"ボツリヌス|破傷風|アナプラズマ|エールリヒア|バベシア|レプトスピラ|"
    r"前庭|認知機能",
    re.IGNORECASE,
)

_KAMIDE_MILK_PATTERNS = re.compile(
    r"parvovir|canine distemp|influenza|pancreatit|megaesophag|"
    r"hepatic lipidos|\bGI stasis|gastrointestinal stasis|"
    r"anorexia|inappetence|cachex|hepatic encephalop|"
    r"orphan|foaling complic|neonat|failure of passive transfer|\bFPT\b|"
    r"feeding tube|enteral nutri|"
    r"パルボ|犬ジステンパー|インフルエンザ|膵炎|巨大食道|肝リピドーシス|"
    r"消化管うっ滞|食欲不振|食欲低下|悪液質|肝性脳症|"
    r"孤児|分娩合併|新生児|初乳不足|経管栄養",
    re.IGNORECASE,
)

# ---------------------------------------------------------------------------
# Species sets
# ---------------------------------------------------------------------------

_JOINT_SPECIES = frozenset(
    {
        "dog",
        "cat",
        "horse",
        "rabbit",
        "hamster",
        "guinea_pig",
        "chinchilla",
        "ferret",
        "hedgehog",
        "sugar_glider",
        "degu",
        "exotic_other",
    }
)

_ANTIOX_SPECIES = frozenset(
    {
        "dog",
        "cat",
        "horse",
        "rabbit",
        "hamster",
        "guinea_pig",
        "chinchilla",
        "ferret",
        "hedgehog",
        "sugar_glider",
        "degu",
        "bird",
        "parakeet",
        "parrot",
        "exotic_other",
    }
)

_MSM_AMINO_SPECIES = frozenset(
    {
        "dog",
        "cat",
        "horse",
        "rabbit",
        "hamster",
        "guinea_pig",
        "chinchilla",
        "ferret",
        "hedgehog",
        "sugar_glider",
        "degu",
        "bird",
        "parakeet",
        "parrot",
        "exotic_other",
    }
)

_NMN_SPECIES = frozenset(
    {
        "dog",
        "cat",
        "horse",
        "rabbit",
        "ferret",
        "hamster",
        "guinea_pig",
        "chinchilla",
        "hedgehog",
        "sugar_glider",
        "degu",
        "exotic_other",
    }
)

_PREBIOTIC_SPECIES = frozenset(
    {
        "dog",
        "cat",
        "horse",
        "rabbit",
        "hamster",
        "guinea_pig",
        "chinchilla",
        "ferret",
        "hedgehog",
        "sugar_glider",
        "degu",
        "bird",
        "parakeet",
        "parrot",
        "exotic_other",
    }
)

_RELAX_CBD_SPECIES = frozenset(
    {
        "dog",
        "cat",
        "horse",
        "rabbit",
        "ferret",
    }
)

_PROTAIN_SPECIES = frozenset(
    {
        "dog",
        "cat",
        "horse",
        "rabbit",
        "ferret",
        "hamster",
        "guinea_pig",
        "chinchilla",
        "hedgehog",
        "sugar_glider",
        "degu",
        "exotic_other",
    }
)

_BOOSTER_SPECIES = frozenset(
    {
        "dog",
        "cat",
        "horse",
        "rabbit",
        "ferret",
        "hamster",
        "guinea_pig",
        "chinchilla",
        "hedgehog",
        "sugar_glider",
        "degu",
        "exotic_other",
    }
)

_KAMIDE_MILK_SPECIES = frozenset(
    {
        "dog",
        "cat",
        "horse",
        "rabbit",
        "ferret",
        "hamster",
        "guinea_pig",
        "chinchilla",
        "hedgehog",
        "sugar_glider",
        "degu",
        "bird",
        "parakeet",
        "parrot",
        "exotic_other",
    }
)

# ---------------------------------------------------------------------------
# Product registry — drives both matching and compact block rendering
# ---------------------------------------------------------------------------

_PRODUCTS = [
    {
        "pattern": _JOINT_PATTERNS,
        "species": _JOINT_SPECIES,
        "name_ja": "For Joint",
        "name_en": "For Joint",
        "ingredients_ja": "MSM+グルコサミン/コンドロイチン",
        "ingredients_en": "MSM + glucosamine/chondroitin",
        "indication_ja": "関節軟骨保護・抗炎症。MSMの抗炎症作用+グルコサミン/コンドロイチンの軟骨基質合成促進。変形性関節症の疼痛緩和・進行抑制、術後の関節リハビリ、馬の蹄葉炎回復期サポートに",
        "indication_en": "articular cartilage protection & anti-inflammatory",
        "caution_ja": None,
        "caution_en": None,
    },
    {
        "pattern": _ANTIOX_PATTERNS,
        "species": _ANTIOX_SPECIES,
        "name_ja": "For Antioxidant",
        "name_en": "For Antioxidant",
        "ingredients_ja": "アスタキサンチン+メロンSOD+VitE+システイン（アスタアミノ処方）",
        "ingredients_en": "astaxanthin + melon SOD + VitE + cysteine (Asta-Amino formula)",
        "indication_ja": "抗酸化・慢性疾患免疫サポート。アスタキサンチン(カロテノイド系)+SOD(スーパーオキシドジスムターゼ)が活性酸素種を消去。CKD・肝疾患・アトピー・ダニ媒介性感染症の酸化ストレス軽減、高齢動物の免疫機能維持に",
        "indication_en": "antioxidant & immune support in chronic disease",
        "caution_ja": None,
        "caution_en": None,
    },
    {
        "pattern": _MSM_AMINO_PATTERNS,
        "species": _MSM_AMINO_SPECIES,
        "name_ja": "MSM+アミノコンプリート",
        "name_en": "MSM + Amino Complete",
        "ingredients_ja": "MSM+必須アミノ酸(BCAA中心)",
        "ingredients_en": "high-dose MSM + essential amino acid blend",
        "indication_ja": "組織修復・筋肉維持・肝腎栄養サポート。BCAA(分岐鎖アミノ酸)が筋蛋白合成を促進+MSMが結合組織の修復をサポート。術後回復、骨折治癒、CKD/肝疾患の筋肉量維持、競走馬・スポーツ犬の運動器サポートに",
        "indication_en": "tissue repair, muscle maintenance, hepatic/renal nutrition",
        "caution_ja": "重度肝・腎不全は蛋白負荷に留意",
        "caution_en": "caution: protein load in severe hepatic/renal failure",
    },
    {
        "pattern": _NMN_PATTERNS,
        "species": _NMN_SPECIES,
        "name_ja": "NMNミトコンドリアアシスト",
        "name_en": "NMN Mitochondria Assist",
        "ingredients_ja": "NMN+α-リポ酸+システイン+プロバイオティクス",
        "ingredients_en": "NMN + α-lipoic acid + cysteine + probiotics",
        "indication_ja": "細胞エネルギー代謝・サーチュイン活性化・抗老化。NMN 5000mgがNAD+産生を促進→ミトコンドリア機能改善+サーチュイン(SIRT1-7)活性化。認知機能低下(CDS)、変性性脊髄症、慢性代謝疾患(糖尿病/クッシング)、加齢性臓器機能低下のサポートに",
        "indication_en": "cellular energy metabolism, sirtuin activation, anti-aging",
        "caution_ja": None,
        "caution_en": None,
    },
    {
        "pattern": _PREBIOTIC_PATTERNS,
        "species": _PREBIOTIC_SPECIES,
        "name_ja": "CPパウダー",
        "name_en": "CP Powder",
        "ingredients_ja": "プレバイオ+プロバイオ+サイリウム",
        "ingredients_en": "prebiotics + probiotics + psyllium",
        "indication_ja": "腸内細菌叢正常化・腸管バリア強化・腸腎連関サポート。サイリウム(水溶性繊維)が腸管運動を促進+プレバイオティクスが有益菌(Lactobacillus/Bifidobacterium)の増殖を支援。IBD、慢性腸症、抗菌薬関連dysbiosis、CKDの尿毒素軽減(インドキシル硫酸低減)に",
        "indication_en": "microbiome restoration, gut barrier, gut-kidney axis",
        "caution_ja": "完全腸閉塞は禁忌",
        "caution_en": "contraindicated in complete intestinal obstruction",
    },
    {
        "pattern": _RELAX_CBD_PATTERNS,
        "species": _RELAX_CBD_SPECIES,
        "name_ja": "Relax & CBD",
        "name_en": "Relax & CBD",
        "ingredients_ja": "フルスペクトラムCBD",
        "ingredients_en": "full-spectrum CBD",
        "indication_ja": "慢性疼痛・不安・難治性てんかん・緩和ケア。フルスペクトラムCBDがECS(エンドカンナビノイドシステム)のCB1/CB2受容体に作用→抗炎症・抗不安・抗けいれん。変形性関節症の疼痛、分離不安・騒音恐怖症、難治性てんかんの発作頻度低減、終末期QOL改善に",
        "indication_en": "chronic pain, anxiety, refractory epilepsy, palliative care",
        "caution_ja": "肝代謝(CYP450)薬物相互作用に注意",
        "caution_en": "CYP450 hepatic metabolism — monitor concurrent drug levels",
    },
    {
        "pattern": _PROTAIN_PATTERNS,
        "species": _PROTAIN_SPECIES,
        "name_ja": "Protain",
        "name_en": "Protain",
        "ingredients_ja": "高品質タンパク質+コラーゲン前駆体",
        "ingredients_en": "high-quality protein + collagen precursors",
        "indication_ja": "がん悪液質・術後筋肉維持・除脂肪体重保持。高品質タンパク質+コラーゲン前駆体が筋蛋白合成を促進。腫瘍関連悪液質のLBM(除脂肪体重)維持、大手術後の回復促進、サルコペニア予防、肥満管理時の筋量維持に",
        "indication_en": "cancer cachexia, post-surgical muscle preservation, lean mass retention",
        "caution_ja": "重度肝・腎不全は蛋白負荷に留意",
        "caution_en": "caution: protein load in severe hepatic/renal failure",
    },
    {
        "pattern": _BOOSTER_PATTERNS,
        "species": _BOOSTER_SPECIES,
        "name_ja": "Booster & Relax",
        "name_en": "Booster & Relax",
        "ingredients_ja": "アダプトゲン+Bビタミン複合体",
        "ingredients_en": "adaptogens + B-complex vitamins",
        "indication_ja": "ウイルス後回復・内分泌疾患エネルギー補給・高齢期慢性疲労。アダプトゲン(ストレス適応促進)+Bビタミン複合体がエネルギー代謝と副腎機能をサポート。パルボ/ジステンパー回復期、甲状腺機能低下症/アジソン病の倦怠感、ダニ媒介性感染症回復期のエネルギー補給に",
        "indication_en": "post-viral convalescence, endocrinopathy energy support, senior fatigue",
        "caution_ja": None,
        "caution_en": None,
    },
    {
        "pattern": _KAMIDE_MILK_PATTERNS,
        "species": _KAMIDE_MILK_SPECIES,
        "name_ja": "カミデミルク",
        "name_en": "Kamide Milk",
        "ingredients_ja": "消化吸収しやすい流動性栄養",
        "ingredients_en": "highly digestible liquid nutrition",
        "indication_ja": "食欲不振・クリティカルケア・経管栄養。消化吸収しやすい流動性栄養で、肝リピドーシス予防(猫/ウサギ)、パルボウイルス回復期、膵炎の低脂肪栄養、巨大食道症の経口流動食、新生子の人工哺乳補助に",
        "indication_en": "anorexia, critical-care feeding, enteral/tube feeding",
        "caution_ja": "完全腸閉塞は禁忌; 重症膵炎は低脂肪配合",
        "caution_en": "contraindicated in complete obstruction; use low-fat version in severe pancreatitis",
    },
]

# Single idempotency marker — one per disease regardless of how many products match.
_MARKER_BLOCK = "[ECVN:Block]"

# Labelled explicitly as sponsored/own-product (PR) so it is never mistaken for
# standard, evidence-based treatment. The frontend renders a dedicated PR badge
# + disclaimer; this text carries the same label for server-rendered/API surfaces.
_BLOCK_HEADER_JA = "【PR・自社製品｜標準治療ではありません — Equine & Canine Vet Nutrition (caninevet.jp)】"
_BLOCK_HEADER_EN = "[PR / Sponsored — not standard treatment — Equine & Canine Vet Nutrition (caninevet.jp)]"


# ---------------------------------------------------------------------------
# Block builders
# ---------------------------------------------------------------------------


def _build_block_ja(matched: List[Dict[str, Any]]) -> str:
    lines = [f"\n{_MARKER_BLOCK} {_BLOCK_HEADER_JA}"]
    cautions: List[str] = []
    for p in matched:
        lines.append(f"• {p['name_ja']} ({p['ingredients_ja']}): {p['indication_ja']}")
        if p.get("caution_ja"):
            cautions.append(f"※{p['name_ja']}: {p['caution_ja']}")
    lines.extend(cautions)
    return "\n".join(lines)


def _build_block_en(matched: List[Dict[str, Any]]) -> str:
    lines = [f"\n{_MARKER_BLOCK} {_BLOCK_HEADER_EN}"]
    cautions: List[str] = []
    for p in matched:
        lines.append(f"• {p['name_en']} ({p['ingredients_en']}): {p['indication_en']}")
        if p.get("caution_en"):
            cautions.append(f"Note — {p['name_en']}: {p['caution_en']}")
    lines.extend(cautions)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Matching helpers
# ---------------------------------------------------------------------------


def _disease_text(disease: Dict[str, Any]) -> str:
    parts = [
        str(disease.get("name") or ""),
        str(disease.get("name_ja") or ""),
        str(disease.get("name_en") or ""),
        str(disease.get("description") or ""),
        str(disease.get("description_ja") or ""),
    ]
    return " ".join(parts)


def _normalize_species(species: str) -> str:
    """Normalize species labels to canonical lowercase_underscore form."""
    if not species:
        return ""
    return species.strip().lower().replace(" ", "_").replace("-", "_")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def apply_sponsor_adjuncts_dict(disease: Dict[str, Any], species: str) -> Dict[str, Any]:
    """Append a single compact ECVN adjunct block to dict-based disease entries.

    Used by api.species.helpers.enrich_diseases for all non-horse species.
    Mutates and returns the disease dict.
    """
    if not isinstance(disease, dict):
        return disease

    existing_ja = disease.get("treatment_ja") or ""
    existing_en = disease.get("treatment") or ""
    if _MARKER_BLOCK in existing_ja:
        return disease

    sp = _normalize_species(species)
    text = _disease_text(disease)
    matched = [p for p in _PRODUCTS if sp in p["species"] and p["pattern"].search(text)]
    if not matched:
        return disease

    block_ja = _build_block_ja(matched)
    block_en = _build_block_en(matched)
    disease["treatment_ja"] = (existing_ja.rstrip() + block_ja) if existing_ja else block_ja.lstrip()
    disease["treatment"] = (existing_en.rstrip() + block_en) if existing_en else block_en.lstrip()
    return disease


def apply_sponsor_adjuncts_obj(disease_obj: Any) -> None:
    """Append a single compact ECVN adjunct block to horse Disease dataclass instances.

    The horse DISEASE_DATABASE stores entries as dataclass objects.
    Uses treatment_protocol as the primary field; general_management as secondary.
    """
    name_en = getattr(disease_obj, "name_en", "") or ""
    name_ja = getattr(disease_obj, "name_ja", "") or ""
    desc_ja = getattr(disease_obj, "description_ja", "") or ""
    text = f"{name_en} {name_ja} {desc_ja}"

    existing = getattr(disease_obj, "treatment_protocol", "") or ""
    if _MARKER_BLOCK in existing:
        return

    matched = [p for p in _PRODUCTS if "horse" in p["species"] and p["pattern"].search(text)]
    if not matched:
        return

    block_ja = _build_block_ja(matched)

    def _set(attr: str, block: str) -> None:
        cur = getattr(disease_obj, attr, "") or ""
        if _MARKER_BLOCK in cur:
            return
        setattr(disease_obj, attr, (cur.rstrip() + block) if cur else block.lstrip())

    _set("treatment_protocol", block_ja)
    if getattr(disease_obj, "general_management", ""):
        _set("general_management", block_ja)
