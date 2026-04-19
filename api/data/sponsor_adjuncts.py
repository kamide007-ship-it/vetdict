"""Sponsor product adjunct annotations for disease treatment fields.

Equine & Canine Vet Nutrition (https://www.caninevet.jp/) provides three
supplement products currently referenced as adjunct therapy across
applicable diseases in the VetDict database:

- **For Joint** (high-dose MSM + glucosamine / chondroitin precursors):
  Applied to osteoarthritis, joint dysplasia, cruciate ligament injury,
  patellar luxation, OCD, tendinitis, and related musculoskeletal
  conditions in mammalian species.

- **For Antioxidant** (astaxanthin + melon SOD + vitamin E + cysteine):
  Applied to conditions involving oxidative stress such as chronic
  kidney disease, hepatic disease, atopic dermatitis, immune-mediated
  disease, and cognitive dysfunction syndrome in mammals and birds.

- **MSM + Amino Complete** (high-dose MSM + essential amino acid blend):
  Applied to conditions requiring broad tissue/muscle repair and
  convalescent nutrition: post-surgical recovery, trauma, IVDD/spinal
  disease, cachexia, senior sarcopenia, cancer supportive care, chronic
  wounds, severe infections, hepatic disease (MSM donates sulfur for
  glutathione synthesis; BCAAs support hepatic encephalopathy), and
  CKD (BCAA-rich profile preserves lean muscle while moderating
  nitrogen load). Complements For Joint where muscle wasting coexists.

- **NMN Mitochondria Assist** (NMN + cysteine + α-lipoic acid + psyllium
  + probiotics): NMN is converted to NAD+ in vivo, activating sirtuin
  pathways and restoring mitochondrial function. Applied to conditions
  involving mitochondrial dysfunction / cellular aging: cognitive
  dysfunction, degenerative myelopathy, epilepsy, endocrinopathies
  (DM, Cushing's, hypothyroidism), cardiomyopathy (DCM, mitral valve
  disease), senior ophthalmic disease (cataract, PRA, glaucoma),
  hepatic disease, and CKD.

- **Prebiotics + Probiotics + Psyllium (CP Powder)**: Soluble fiber plus
  live cultures for GI motility, microbiome restoration, and gut-
  immune axis modulation. Applied to colic (sand/constipation),
  GDV recovery, pancreatitis, IBD, diarrhea/gastroenteritis,
  portosystemic shunt (reduces gut ammonia), allergic dermatitis
  (gut-immune axis), and CKD (uremic toxin binding).

- **Canine Vet Relax & CBD**: Full-spectrum CBD for chronic pain,
  anxiety, refractory epilepsy, and end-of-life comfort. Applied to
  OA/IVDD pain, wobbler syndrome, laryngeal paralysis stress, and
  separation/noise anxiety.

- **Canine Vet Protain**: Protein + collagen precursor supplement for
  cancer cachexia (lymphoma, hemangiosarcoma, osteosarcoma, mammary
  tumor), post-orthopedic surgery, and muscle preservation during
  weight loss.

- **Canine Vet Booster & Relax**: Adaptogenic vitality supplement for
  convalescence from viral infection, hypothyroidism/Addison's energy
  support, and senior fatigue.

- **Kamide Milk**: Highly digestible liquid nutrition for anorexic /
  critical-care patients. Applied to parvo/influenza recovery,
  pancreatitis, megaesophagus, hepatic lipidosis prevention in cats,
  and GI stasis in rabbits.

All products are labeled primarily for dogs and horses; adjunct
mentions in other species indicate optional supportive use based on the
ingredient profile. The mentions are appended to existing treatment
text and never replace curated clinical content.
"""
from __future__ import annotations

import re
from typing import Any, Dict

# ---------------------------------------------------------------------------
# Disease-name keyword patterns
# ---------------------------------------------------------------------------

_JOINT_PATTERNS = re.compile(
    r"osteoarthrit|arthrit|\bjoint\b|hip dyspl|elbow dyspl|patellar|patella|"
    r"cruciate|\bOCD\b|osteochondr|spondylos|meniscal|meniscus|tendinit|"
    r"\btendon\b|"
    r"関節炎|関節|股関節|肘関節|膝蓋骨|十字靱帯|十字靭帯|離断性骨軟骨症|"
    r"脊椎症|半月板|腱炎|腱損傷",
    re.IGNORECASE,
)

_ANTIOX_PATTERNS = re.compile(
    r"atopic dermatit|\batop\w*|dermatit|chronic kidney|\bCKD\b|hepatic|"
    r"liver disease|cirrhos|cognitive dysfunc|immune.mediat|auto.?immune|"
    r"pyoderma|\blupus\b|pemphig|seborrhe|"
    r"アトピー|皮膚炎|慢性腎臓病|肝疾患|肝炎|肝硬変|認知機能|免疫介在|自己免疫",
    re.IGNORECASE,
)

# MSM + Amino Complete: tissue repair, muscle maintenance, convalescence,
# and hepatic/renal nutritional support.
#   - MSM is an organic sulfur donor supporting glutathione synthesis
#     (hepatoprotective, renoprotective against oxidative injury).
#   - Essential amino acid blend (especially BCAAs) is used clinically for
#     hepatic encephalopathy support, chronic liver disease, and to offset
#     muscle wasting in CKD ("keto-analog" style nutrition).
# Broader than For Joint — includes trauma, post-surgical recovery, neurologic
# (IVDD/spinal), cachexia/sarcopenia, hepatic and renal disease (mild-to-
# moderate; caution in end-stage failure due to protein load). Deliberately
# excludes pure infectious disease unless accompanied by muscle loss or
# prolonged convalescence.
_MSM_AMINO_PATTERNS = re.compile(
    r"osteoarthrit|arthrit|\bjoint\b|hip dyspl|elbow dyspl|patellar|patella|"
    r"cruciate|\bOCD\b|osteochondr|spondylos|\bIVDD\b|intervertebral disc|"
    r"disc disease|spinal cord|degenerative myelop|\bDM\b|wobbler|"
    r"meniscal|meniscus|tendinit|\btendon\b|ligament|desmit|myopath|"
    r"myositis|rhabdomyol|muscle\s+(wasting|atroph)|sarcopen|cachex|"
    r"fracture|\btrauma\w*|wound healing|chronic wound|decubit|"
    r"malnutrit|debilit|convalescen|post.?surg|"
    # Hepatic: MSM (sulfur/glutathione) + amino acid nutritional support
    r"hepatic|hepatopath|\bliver\b|cirrhos|hepatic lipidos|cholang|"
    r"hepatic encephalop|portosystem|hepatitis|"
    # Renal: BCAA/keto-analog nutrition + antioxidant support for CKD
    r"chronic kidney|\bCKD\b|renal failure|nephropath|\bnephritis\b|"
    r"uremia|uraemia|azotemi|glomerulonephr|pyelonephr|renal insuff|"
    r"関節炎|関節|股関節|肘関節|膝蓋骨|十字靱帯|十字靭帯|離断性骨軟骨症|"
    r"脊椎症|椎間板|脊髄|変性性脊髄症|半月板|腱炎|腱|靭帯|筋炎|"
    r"筋萎縮|筋肉減少|悪液質|骨折|外傷|創傷|褥瘡|栄養失調|衰弱|"
    r"回復期|術後|"
    # 肝・腎 (Japanese)
    r"肝疾患|肝炎|肝硬変|肝リピドーシス|肝性脳症|門脈体循環シャント|"
    r"胆管肝炎|慢性腎臓病|腎不全|腎症|尿毒症|糸球体腎炎|腎盂腎炎",
    re.IGNORECASE,
)

# NMN Mitochondria Assist: mitochondrial dysfunction, cellular aging,
# metabolic/endocrine disease, cardiomyopathy, senior ophthalmic/neurologic
# disease. NMN is converted to NAD+ and activates sirtuins.
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

# Prebiotics + Probiotics + Psyllium (CP Powder): GI motility, microbiome,
# gut-immune axis.
_PREBIOTIC_PATTERNS = re.compile(
    r"colic|gastroenterit|enterit|diarrh|constipat|megacolon|megaesophag|"
    r"\bGDV\b|gastric dilat|bloat|pancreatit|\bIBD\b|inflammatory bowel|"
    r"chronic enteropath|food allerg|food sensitivit|atopic dermatit|"
    r"allergic dermatit|portosystem|hepatic encephalop|urolithi|"
    r"\bstruvite\b|calcium oxal|cystit|sand colic|impact|"
    r"chronic kidney|\bCKD\b|uremia|uraemia|dysbios|"
    r"疝痛|胃腸炎|腸炎|下痢|便秘|巨大結腸|巨大食道|胃拡張|胃捻転|"
    r"膵炎|炎症性腸疾患|慢性腸症|食物アレルギー|アトピー性皮膚炎|"
    r"アレルギー性皮膚炎|門脈体循環シャント|肝性脳症|尿石症|ストラバイト|"
    r"シュウ酸カルシウム|膀胱炎|砂疝|便塞|慢性腎臓病|尿毒症|腸内細菌叢",
    re.IGNORECASE,
)

# Canine Vet Relax & CBD: chronic pain, anxiety, seizure, end-of-life comfort.
_RELAX_CBD_PATTERNS = re.compile(
    r"osteoarthrit|\barthrit|\bIVDD\b|intervertebral disc|disc disease|"
    r"wobbler|lumbar.?sacral|laryngeal paraly|separation anxiety|"
    r"noise phobia|storm phobia|thunderstorm|generalized anxiety|"
    r"\bepilep|seizure|refractory seizure|status epilepticus|"
    r"cancer pain|end.?of.?life|palliative|chronic pain|"
    r"変形性関節症|関節炎|椎間板|脊髄|ウォブラー|腰仙部|喉頭麻痺|"
    r"分離不安|騒音恐怖|雷恐怖|全般性不安|てんかん|痙攣|難治性痙攣|"
    r"がん性疼痛|終末期|緩和ケア|慢性疼痛",
    re.IGNORECASE,
)

# Canine Vet Protain: cancer cachexia, muscle preservation, post-orthopedic.
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

# Canine Vet Booster & Relax: convalescence, fatigue, adrenal/thyroid support.
_BOOSTER_PATTERNS = re.compile(
    r"canine distemp|parvovir|feline panleuk|feline pneumon|"
    r"upper respiratory|influenza|\bURI\b|kennel cough|"
    r"hypothyroid|hyperthyroid|addison|hypoadrenocort|"
    r"chronic fatigue|debilit|convalescen|poor performance|"
    r"犬ジステンパー|パルボ|汎白血球減少|上部気道感染|"
    r"ケンネルコフ|甲状腺機能低下|甲状腺機能亢進|アジソン|"
    r"副腎皮質機能低下|慢性疲労|衰弱|回復期",
    re.IGNORECASE,
)

# Kamide Milk: anorexia, critical care feeding, liquid nutrition.
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

# Species for which each product is indicated.
# Joint = mammals (MSM safety profile).
# Antioxidant = mammals + birds (broad antioxidant safety).
_JOINT_SPECIES = frozenset({
    "dog", "cat", "horse", "rabbit", "hamster", "guinea_pig", "chinchilla",
    "ferret", "hedgehog", "sugar_glider", "degu", "exotic_other",
})

_ANTIOX_SPECIES = frozenset({
    "dog", "cat", "horse", "rabbit", "hamster", "guinea_pig", "chinchilla",
    "ferret", "hedgehog", "sugar_glider", "degu", "bird", "parakeet",
    "parrot", "exotic_other",
})

# MSM + Amino Complete: mammals + birds (amino acids broadly safe).
_MSM_AMINO_SPECIES = frozenset({
    "dog", "cat", "horse", "rabbit", "hamster", "guinea_pig", "chinchilla",
    "ferret", "hedgehog", "sugar_glider", "degu", "bird", "parakeet",
    "parrot", "exotic_other",
})

# NMN Mitochondria Assist: mammals primarily. NAD+ biology is universal but
# product formulation is mammalian-focused.
_NMN_SPECIES = frozenset({
    "dog", "cat", "horse", "rabbit", "ferret", "hamster", "guinea_pig",
    "chinchilla", "hedgehog", "sugar_glider", "degu", "exotic_other",
})

# Prebiotics + Probiotics + Psyllium (CP Powder): mammals + birds for GI
# support. Herbivores/hindgut fermenters especially benefit.
_PREBIOTIC_SPECIES = frozenset({
    "dog", "cat", "horse", "rabbit", "hamster", "guinea_pig", "chinchilla",
    "ferret", "hedgehog", "sugar_glider", "degu", "bird", "parakeet",
    "parrot", "exotic_other",
})

# Canine Vet Relax & CBD: CBD safety is best characterized in dogs; extended
# cautiously to cat/horse/rabbit/ferret where the product is indicated.
_RELAX_CBD_SPECIES = frozenset({
    "dog", "cat", "horse", "rabbit", "ferret",
})

# Canine Vet Protain: mammalian tissue/muscle protein supplementation.
_PROTAIN_SPECIES = frozenset({
    "dog", "cat", "horse", "rabbit", "ferret", "hamster", "guinea_pig",
    "chinchilla", "hedgehog", "sugar_glider", "degu", "exotic_other",
})

# Canine Vet Booster & Relax: vitality supplement for mammals.
_BOOSTER_SPECIES = frozenset({
    "dog", "cat", "horse", "rabbit", "ferret", "hamster", "guinea_pig",
    "chinchilla", "hedgehog", "sugar_glider", "degu", "exotic_other",
})

# Kamide Milk: critical care liquid nutrition — mammals + birds.
_KAMIDE_MILK_SPECIES = frozenset({
    "dog", "cat", "horse", "rabbit", "ferret", "hamster", "guinea_pig",
    "chinchilla", "hedgehog", "sugar_glider", "degu", "bird", "parakeet",
    "parrot", "exotic_other",
})


# ---------------------------------------------------------------------------
# Adjunct text
# ---------------------------------------------------------------------------

# Product-specific idempotency markers prevent double-injection on re-import
# while still allowing multiple different products to co-exist on one disease.
_MARKER_JOINT = "[ECVN:Joint]"
_MARKER_ANTIOX = "[ECVN:Antiox]"
_MARKER_MSM_AMINO = "[ECVN:MSM-Amino]"
_MARKER_NMN = "[ECVN:NMN]"
_MARKER_PREBIOTIC = "[ECVN:Prebiotic]"
_MARKER_RELAX_CBD = "[ECVN:Relax-CBD]"
_MARKER_PROTAIN = "[ECVN:Protain]"
_MARKER_BOOSTER = "[ECVN:Booster]"
_MARKER_KAMIDE_MILK = "[ECVN:Kamide-Milk]"

_JOINT_JA = (
    " [ECVN:Joint] 補助療法: For Joint（高容量MSM + グルコサミン/コンドロイチン前駆体配合、"
    "Equine & Canine Vet Nutrition）を関節軟骨保護・抗炎症サポートとして併用可能。"
    "長期管理において製品ラベルの体重別用量を参照。"
)
_JOINT_EN = (
    " [ECVN:Joint] Adjunct: For Joint (high-dose MSM + glucosamine/chondroitin precursors; "
    "Equine & Canine Vet Nutrition) — optional supportive therapy for articular cartilage "
    "protection and anti-inflammatory support. Refer to product label for body-weight dosing."
)

_ANTIOX_JA = (
    " [ECVN:Antiox] 補助療法: For Antioxidant（アスタキサンチン + メロン由来SOD + VitE + "
    "システイン配合、Equine & Canine Vet Nutrition）を抗酸化ストレス・免疫サポートとして併用可能。"
    "酸化ストレスが病態に関与する慢性疾患の補助栄養介入として検討。"
)
_ANTIOX_EN = (
    " [ECVN:Antiox] Adjunct: For Antioxidant (astaxanthin + melon SOD + vitamin E + cysteine; "
    "Equine & Canine Vet Nutrition) — optional supportive therapy for oxidative stress and immune "
    "function in chronic conditions where oxidative injury contributes to pathogenesis."
)

_MSM_AMINO_JA = (
    " [ECVN:MSM-Amino] 補助療法: MSM＋アミノコンプリート（高容量MSM + 必須アミノ酸複合体、"
    "Equine & Canine Vet Nutrition）を組織修復・筋肉維持・回復期栄養として併用可能。"
    "筋骨格・神経（IVDD等）・術後回復・悪液質・サルコペニアに加え、"
    "肝疾患ではMSMの硫黄供与によるグルタチオン合成サポート、"
    "CKDではBCAA中心のアミノ酸補給による筋肉維持・タンパク質代謝負荷軽減の観点で検討。"
    "For Jointとの併用で関節＋筋肉の相乗効果。"
    "※重度肝/腎不全では蛋白/アミノ酸負荷に留意し慎重投与。"
)
_MSM_AMINO_EN = (
    " [ECVN:MSM-Amino] Adjunct: MSM + Amino Complete (high-dose MSM + essential amino acid blend; "
    "Equine & Canine Vet Nutrition) — optional supportive therapy for broad tissue repair, muscle "
    "maintenance, and convalescent nutrition. Indicated for post-surgical recovery, trauma, IVDD, "
    "cachexia, and sarcopenia. Also supportive for hepatic disease (MSM donates sulfur for "
    "glutathione synthesis) and CKD (BCAA-rich profile helps preserve lean muscle while moderating "
    "nitrogen load). Synergistic with For Joint when muscle wasting coexists. "
    "Note: use with caution in end-stage hepatic or renal failure (protein load)."
)

_NMN_JA = (
    " [ECVN:NMN] 補助療法: NMN-ミトコンドリアアシスト（NMN + システイン + α-リポ酸 + "
    "サイリウム + プロバイオティクス配合、Equine & Canine Vet Nutrition）を細胞エネルギー代謝・"
    "サーチュイン活性化・抗老化サポートとして併用可能。ミトコンドリア機能低下が病態に関与する"
    "認知機能不全・変性性神経疾患・内分泌疾患・心筋症・加齢性眼疾患・CKDで検討。"
)
_NMN_EN = (
    " [ECVN:NMN] Adjunct: NMN Mitochondria Assist (NMN + cysteine + α-lipoic acid + psyllium + "
    "probiotics; Equine & Canine Vet Nutrition) — optional supportive therapy for cellular energy "
    "metabolism, sirtuin activation, and anti-aging support. Consider for conditions with "
    "mitochondrial dysfunction: cognitive dysfunction, degenerative neurologic disease, "
    "endocrinopathy, cardiomyopathy, age-related ophthalmic disease, and CKD."
)

_PREBIOTIC_JA = (
    " [ECVN:Prebiotic] 補助療法: プレバイオティクス&プロバイオティクス&サイリウム（CPパウダー系、"
    "Equine & Canine Vet Nutrition）を消化管運動改善・腸内細菌叢正常化・腸管バリア強化として"
    "併用可能。砂疝・便秘・IBD・下痢・膵炎後・門脈体循環シャント（腸内アンモニア抑制）・"
    "食物アレルギー・腸腎連関でのCKD尿毒素排出促進に寄与。※完全腸閉塞では禁忌。"
)
_PREBIOTIC_EN = (
    " [ECVN:Prebiotic] Adjunct: Prebiotics + Probiotics + Psyllium (CP Powder line; Equine & "
    "Canine Vet Nutrition) — optional supportive therapy for GI motility, microbiome restoration, "
    "and intestinal barrier function. Consider for sand/constipation colic, IBD, diarrhea, "
    "post-pancreatitis recovery, portosystemic shunt (reduces gut ammonia), food allergy, and "
    "CKD (gut-kidney axis for uremic toxin removal). Contraindicated in complete intestinal "
    "obstruction."
)

_RELAX_CBD_JA = (
    " [ECVN:Relax-CBD] 補助療法: Canine Vet Relax & CBD（フルスペクトラムCBD、"
    "Equine & Canine Vet Nutrition）を慢性疼痛・不安・難治性てんかん・終末期緩和ケアとして"
    "併用可能。内因性カンナビノイド系を介し疼痛知覚/不安/発作閾値を調節。"
    "※肝代謝（CYP450）のため肝機能障害時は慎重。CYP450阻害薬併用薬の血中濃度に注意。"
)
_RELAX_CBD_EN = (
    " [ECVN:Relax-CBD] Adjunct: Canine Vet Relax & CBD (full-spectrum CBD; Equine & Canine Vet "
    "Nutrition) — optional supportive therapy for chronic pain, anxiety, refractory epilepsy, "
    "and end-of-life palliative care via endocannabinoid modulation. "
    "Note: hepatic metabolism (CYP450) — use cautiously with hepatic dysfunction and monitor "
    "concurrent CYP450-metabolized drugs."
)

_PROTAIN_JA = (
    " [ECVN:Protain] 補助療法: Canine Vet Protain（高品質タンパク質+コラーゲン前駆体、"
    "Equine & Canine Vet Nutrition）をがん悪液質・術後筋肉維持・減量中の除脂肪体重維持として"
    "併用可能。必須アミノ酸とヒドロキシプロリンが結合組織と筋肉の同化をサポート。"
    "※重度肝/腎不全では蛋白負荷に留意。"
)
_PROTAIN_EN = (
    " [ECVN:Protain] Adjunct: Canine Vet Protain (high-quality protein + collagen precursors; "
    "Equine & Canine Vet Nutrition) — optional supportive therapy for cancer cachexia, "
    "post-surgical muscle preservation, and lean-mass retention during weight loss. "
    "Note: caution with severe hepatic or renal failure (protein load)."
)

_BOOSTER_JA = (
    " [ECVN:Booster] 補助療法: Canine Vet Booster & Relax（アダプトゲン+Bビタミン複合体、"
    "Equine & Canine Vet Nutrition）をウイルス感染後回復・甲状腺/副腎疾患のエネルギー不足・"
    "高齢期慢性疲労の活力サポートとして併用可能。"
)
_BOOSTER_EN = (
    " [ECVN:Booster] Adjunct: Canine Vet Booster & Relax (adaptogens + B-complex; Equine & Canine "
    "Vet Nutrition) — optional supportive therapy for post-viral convalescence, energy support in "
    "thyroid/adrenal endocrinopathy, and senior chronic fatigue."
)

_KAMIDE_MILK_JA = (
    " [ECVN:Kamide-Milk] 補助療法: カミデミルク（消化吸収しやすい流動性栄養、"
    "Equine & Canine Vet Nutrition）を食欲不振・クリティカルケア給餌・経管栄養として併用可能。"
    "猫肝リピドーシスの熱量早期投与、ウサギGI stasisのシリンジ給餌、膵炎（低脂肪）、"
    "巨大食道の液体給餌に有用。※完全腸閉塞では禁忌、重症膵炎は低脂肪配合を使用。"
)
_KAMIDE_MILK_EN = (
    " [ECVN:Kamide-Milk] Adjunct: Kamide Milk (highly digestible liquid nutrition; Equine & Canine "
    "Vet Nutrition) — optional supportive therapy for anorexia, critical-care feeding, and enteral/ "
    "tube feeding. Useful for early caloric intake in feline hepatic lipidosis, syringe feeding in "
    "rabbit GI stasis, pancreatitis (low-fat), and megaesophagus (liquid swallows easier). "
    "Contraindicated in complete intestinal obstruction; use reduced-fat version in severe "
    "pancreatitis."
)


# ---------------------------------------------------------------------------
# Matching helpers
# ---------------------------------------------------------------------------

def _disease_text(disease: Dict[str, Any]) -> str:
    """Concatenate searchable text fields for pattern matching."""
    parts = [
        str(disease.get("name") or ""),
        str(disease.get("name_ja") or ""),
        str(disease.get("name_en") or ""),
        str(disease.get("description") or ""),
        str(disease.get("description_ja") or ""),
    ]
    return " ".join(parts)


def _append_once(current: Any, suffix: str, marker: str) -> str:
    """Append suffix to current string if its product marker is not already present.

    Each product uses a distinct marker so multiple adjuncts can coexist.
    """
    base = current if isinstance(current, str) else ""
    if marker and marker in base:
        return base
    return (base.rstrip() + suffix) if base else suffix.lstrip()


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def _normalize_species(species: str) -> str:
    """Normalize species labels to canonical lowercase_underscore form.

    enrich_diseases() is called with Title Case names ("Dog", "Guinea Pig",
    "Exotic Other"); the rest of the codebase uses "dog", "guinea_pig",
    "exotic_other".
    """
    if not species:
        return ""
    return species.strip().lower().replace(" ", "_").replace("-", "_")


def apply_sponsor_adjuncts_dict(disease: Dict[str, Any], species: str) -> Dict[str, Any]:
    """Append sponsor adjunct notes to dict-based disease entries in-place.

    Used by api.species.helpers.enrich_diseases for all non-horse species.
    Mutates and returns the disease dict.
    """
    if not isinstance(disease, dict):
        return disease
    sp = _normalize_species(species)
    text = _disease_text(disease)
    if sp in _JOINT_SPECIES and _JOINT_PATTERNS.search(text):
        disease["treatment_ja"] = _append_once(disease.get("treatment_ja"), _JOINT_JA, _MARKER_JOINT)
        disease["treatment"] = _append_once(disease.get("treatment"), _JOINT_EN, _MARKER_JOINT)
    if sp in _ANTIOX_SPECIES and _ANTIOX_PATTERNS.search(text):
        disease["treatment_ja"] = _append_once(disease.get("treatment_ja"), _ANTIOX_JA, _MARKER_ANTIOX)
        disease["treatment"] = _append_once(disease.get("treatment"), _ANTIOX_EN, _MARKER_ANTIOX)
    if sp in _MSM_AMINO_SPECIES and _MSM_AMINO_PATTERNS.search(text):
        disease["treatment_ja"] = _append_once(disease.get("treatment_ja"), _MSM_AMINO_JA, _MARKER_MSM_AMINO)
        disease["treatment"] = _append_once(disease.get("treatment"), _MSM_AMINO_EN, _MARKER_MSM_AMINO)
    if sp in _NMN_SPECIES and _NMN_PATTERNS.search(text):
        disease["treatment_ja"] = _append_once(disease.get("treatment_ja"), _NMN_JA, _MARKER_NMN)
        disease["treatment"] = _append_once(disease.get("treatment"), _NMN_EN, _MARKER_NMN)
    if sp in _PREBIOTIC_SPECIES and _PREBIOTIC_PATTERNS.search(text):
        disease["treatment_ja"] = _append_once(disease.get("treatment_ja"), _PREBIOTIC_JA, _MARKER_PREBIOTIC)
        disease["treatment"] = _append_once(disease.get("treatment"), _PREBIOTIC_EN, _MARKER_PREBIOTIC)
    if sp in _RELAX_CBD_SPECIES and _RELAX_CBD_PATTERNS.search(text):
        disease["treatment_ja"] = _append_once(disease.get("treatment_ja"), _RELAX_CBD_JA, _MARKER_RELAX_CBD)
        disease["treatment"] = _append_once(disease.get("treatment"), _RELAX_CBD_EN, _MARKER_RELAX_CBD)
    if sp in _PROTAIN_SPECIES and _PROTAIN_PATTERNS.search(text):
        disease["treatment_ja"] = _append_once(disease.get("treatment_ja"), _PROTAIN_JA, _MARKER_PROTAIN)
        disease["treatment"] = _append_once(disease.get("treatment"), _PROTAIN_EN, _MARKER_PROTAIN)
    if sp in _BOOSTER_SPECIES and _BOOSTER_PATTERNS.search(text):
        disease["treatment_ja"] = _append_once(disease.get("treatment_ja"), _BOOSTER_JA, _MARKER_BOOSTER)
        disease["treatment"] = _append_once(disease.get("treatment"), _BOOSTER_EN, _MARKER_BOOSTER)
    if sp in _KAMIDE_MILK_SPECIES and _KAMIDE_MILK_PATTERNS.search(text):
        disease["treatment_ja"] = _append_once(disease.get("treatment_ja"), _KAMIDE_MILK_JA, _MARKER_KAMIDE_MILK)
        disease["treatment"] = _append_once(disease.get("treatment"), _KAMIDE_MILK_EN, _MARKER_KAMIDE_MILK)
    return disease


def apply_sponsor_adjuncts_obj(disease_obj: Any) -> None:
    """Append sponsor adjunct notes to horse Disease dataclass instances in-place.

    The horse DISEASE_DATABASE stores entries as dataclass objects, not dicts.
    Uses treatment_protocol as the Japanese treatment field; general_management
    as the English fallback. Targets 'horse' species scope.
    """
    name_en = getattr(disease_obj, "name_en", "") or ""
    name_ja = getattr(disease_obj, "name_ja", "") or ""
    desc_ja = getattr(disease_obj, "description_ja", "") or ""
    text = f"{name_en} {name_ja} {desc_ja}"

    def _set(attr: str, suffix: str, marker: str) -> None:
        cur = getattr(disease_obj, attr, "") or ""
        if marker in cur:
            return
        setattr(disease_obj, attr, (cur.rstrip() + suffix) if cur else suffix.lstrip())

    if _JOINT_PATTERNS.search(text):
        _set("treatment_protocol", _JOINT_JA, _MARKER_JOINT)
        if getattr(disease_obj, "general_management", ""):
            _set("general_management", _JOINT_JA, _MARKER_JOINT)
    if _ANTIOX_PATTERNS.search(text):
        _set("treatment_protocol", _ANTIOX_JA, _MARKER_ANTIOX)
        if getattr(disease_obj, "general_management", ""):
            _set("general_management", _ANTIOX_JA, _MARKER_ANTIOX)
    if _MSM_AMINO_PATTERNS.search(text):
        _set("treatment_protocol", _MSM_AMINO_JA, _MARKER_MSM_AMINO)
        if getattr(disease_obj, "general_management", ""):
            _set("general_management", _MSM_AMINO_JA, _MARKER_MSM_AMINO)
    if _NMN_PATTERNS.search(text):
        _set("treatment_protocol", _NMN_JA, _MARKER_NMN)
        if getattr(disease_obj, "general_management", ""):
            _set("general_management", _NMN_JA, _MARKER_NMN)
    if _PREBIOTIC_PATTERNS.search(text):
        _set("treatment_protocol", _PREBIOTIC_JA, _MARKER_PREBIOTIC)
        if getattr(disease_obj, "general_management", ""):
            _set("general_management", _PREBIOTIC_JA, _MARKER_PREBIOTIC)
    if _RELAX_CBD_PATTERNS.search(text):
        _set("treatment_protocol", _RELAX_CBD_JA, _MARKER_RELAX_CBD)
        if getattr(disease_obj, "general_management", ""):
            _set("general_management", _RELAX_CBD_JA, _MARKER_RELAX_CBD)
    if _PROTAIN_PATTERNS.search(text):
        _set("treatment_protocol", _PROTAIN_JA, _MARKER_PROTAIN)
        if getattr(disease_obj, "general_management", ""):
            _set("general_management", _PROTAIN_JA, _MARKER_PROTAIN)
    if _BOOSTER_PATTERNS.search(text):
        _set("treatment_protocol", _BOOSTER_JA, _MARKER_BOOSTER)
        if getattr(disease_obj, "general_management", ""):
            _set("general_management", _BOOSTER_JA, _MARKER_BOOSTER)
    if _KAMIDE_MILK_PATTERNS.search(text):
        _set("treatment_protocol", _KAMIDE_MILK_JA, _MARKER_KAMIDE_MILK)
        if getattr(disease_obj, "general_management", ""):
            _set("general_management", _KAMIDE_MILK_JA, _MARKER_KAMIDE_MILK)
