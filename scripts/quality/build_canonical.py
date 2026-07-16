"""Build the canonical consolidation map for a species (T103 groundwork).

READ-MOSTLY: reads the served records via the read-only detector, computes a
NON-DESTRUCTIVE consolidation plan, and writes a reviewable data artifact
``api/data/canonical/<species>.json``. It does NOT modify any disease source
module or overlay. The map is applied at load time by ``api/species/canonical.py``.

Conservative, safe-by-default policy (only unambiguous actions are auto-applied;
everything requiring clinical judgement is emitted under ``review`` and left
inactive):

- ``merges``  : exact orthographic duplicate clusters (e.g. "熱中症" vs
  "熱中症（呼吸器型）（デグー）") — same disease, differing only by a species/suffix
  tag. The richest entry becomes canonical; the rest redirect to it.
- ``archives``: entries that are research models, not spontaneous companion-animal
  diseases (e.g. "アルツハイマー様疾患" — degus are an Alzheimer research model).
- ``review``  : over-split disease families and human-medicine-transplant
  complications. Emitted for veterinarian review; NOT applied.

Each entry carries a stable ``slug`` (URL identity) so redirects can be resolved
after merged/archived records are dropped from the served list.

Idempotent: re-running reproduces the same file. Backs up any existing map to
``backups/<UTC>/``.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

import scripts.quality.detect as detect  # reuse the read-only loaders + clustering

ROOT = Path(__file__).resolve().parents[2]
CANON_DIR = ROOT / "api" / "data" / "canonical"

# Japanese species tags used as the "（<species>）" duplicate marker.
_SPECIES_JA = {
    "dog": "犬",
    "cat": "猫",
    "horse": "馬",
    "rabbit": "ウサギ",
    "ferret": "フェレット",
    "hamster": "ハムスター",
    "guinea_pig": "モルモット",
    "chinchilla": "チンチラ",
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
    "exotic_other": "その他",
}


# Curated do-NOT-merge guards: entries that the strict key would auto-merge
# because they share a name_ja, but are clinically DISTINCT diseases (mislabeled
# name_ja). Vet-reviewed. Keeps them as separate served records. The underlying
# name_ja rename is tracked separately (touches stable-id/URL resolution).
_DO_NOT_MERGE: dict[str, list[set[str]]] = {
    # Warble Fly (Hypoderma) vs Cuterebra bot fly — different parasites sharing
    # the mislabeled name_ja "ウマバエ幼虫症".
    "rabbit": [{"rabbit_0212", "rabbit_0298"}],
    # Proptosis (acute traumatic globe prolapse) vs Exophthalmos (chronic
    # retrobulbar protrusion) — clinically distinct; vet decision to keep apart
    # (both share the base name_ja 眼球突出).
    "hamster": [{"hamster_0056", "hamster_0228"}],
    "chinchilla": [{"chinchilla_0123", "chinchilla_0265"}],
    "hedgehog": [{"hedgehog_0040", "hedgehog_0218"}],
    "sugar_glider": [{"sugar_glider_0038", "sugar_glider_0188"}],
    # Ileus (functional/paralytic) vs Intestinal Obstruction (mechanical) —
    # distinct pathophysiology; vet decision to keep apart (base name_ja 腸閉塞).
    "guinea_pig": [{"guinea_pig_0085", "guinea_pig_0209"}],
}


def _is_forbidden_pair(species: str, ids: list[str]) -> bool:
    idset = set(ids)
    return any(len(pair & idset) >= 2 for pair in _DO_NOT_MERGE.get(species, []))


# Curated vet-approved same-disease merges that the STRICT auto key holds back
# because BOTH members carry an informative qualifier (so they differ by more
# than the species tag) yet are the same disease. First id = canonical (kept).
# Vet-reviewed and approved (see .spec/<species>_CONSOLIDATION_REVIEW.md).
_CURATED_MERGE: dict[str, list[list[str]]] = {
    "rabbit": [
        ["rabbit_0001", "rabbit_0314"],  # 胃拡張（鼓脹症） = 胃拡張
        ["rabbit_0026", "rabbit_0294"],  # ツメダニ症 (Cheyletiella)
        ["rabbit_0027", "rabbit_0295"],  # ハエウジ症 (Myiasis/Flystrike)
        ["rabbit_0030", "rabbit_0274"],  # ウサギ出血病 RHDV = RHD
        ["rabbit_0056", "rabbit_0360"],  # 涙嚢炎 (Dacryocystitis)
        ["rabbit_0105", "rabbit_0385"],  # カルシウム欠乏症
        ["rabbit_0194", "rabbit_0389"],  # 播種性血管内凝固 (DIC)
        ["rabbit_0202", "rabbit_0320"],  # 麻痺性イレウス = イレウス
        ["rabbit_0206", "rabbit_0289"],  # 増殖性腸症 (Lawsonia = cause)
        ["rabbit_0234", "rabbit_0402"],  # ハッチバーン (Hutch Burn)
        ["rabbit_0252", "rabbit_0352"],  # 脊椎骨折（胸腰椎） = 脊椎骨折
    ],
    "cat": [
        # NB: pairs with IDENTICAL English names (→ identical slug) are already
        # collapsed by dedupe_disease_list in the served path; the slug-based
        # canonical loader cannot merge them, so they are NOT listed here
        # (e.g. Feline Idiopathic Cystitis (FIC) cat_0040/cat_0218).
        ["cat_0034", "cat_0531"],  # 慢性腎臓病 (CKD)
        ["cat_0198", "cat_0465"],  # アセトアミノフェン中毒 = 急性型
        ["cat_0257", "cat_0484"],  # 猫ビタミンA過剰症 = 慢性型
    ],
    # horse: acronym / synonym pairs of the SAME disease (explicit slug ids).
    # Kept separate in review (distinct): SCC non-ocular vs cutaneous,
    # Inguinal Hernia general vs stallion.
    "horse": [
        ["rp_laryngeal", "rp_laryngeal_hemiplegia"],  # 喉頭片麻痺 (Roaring)
        ["rp_ddsp", "rp_ddsp2"],  # 軟口蓋背方変位 (DDSP)
        ["rp_strangles", "if_strangles"],  # 腺疫 (S. equi)
        ["if_piroplamosis", "if_equine_piroplasmosis", "if_piroplasmosis"],  # ピロプラズマ症
        ["eye_uveitis_signs", "ey_recurrent_uveitis"],  # 馬再発性ぶどう膜炎 (ERU)
        ["nr_epm", "nr_epm_extended"],  # 馬原虫性脊髄脳炎 (EPM)
        ["mt_ems", "mt_ems2"],  # 馬メタボリック症候群 (EMS)
        ["mt_ppid", "mt_ppid2"],  # 下垂体中葉機能障害 (PPID)
        ["mt_rhabdomyolysis", "mt_rhabdomyolysis2"],  # 横紋筋融解症 (Tying Up)
        ["ms_bucked_shin", "ms_bucked_shins"],  # バックドシン
        ["if_rhodococcus", "fl_rhodococcus_pneumonia"],  # ロドコッカス肺炎(子馬)
        ["if_eve", "if_equine_viral_arteritis"],  # 馬ウイルス性動脈炎 (EVA)
        ["tx_acorn", "tx_acorn2"],  # ドングリ中毒 (Tannin)
        ["tx_fescue", "tx_endophyte_fescue", "rp_fescue_toxicosis_repro"],  # フェスク中毒
        ["ms_angular_limb", "fl_angular_limb_deformity"],  # 肢軸異常 (ALD)
        ["ms_capped_elbow", "ms_elbow_hygroma"],  # 肘腫 (Shoe Boil)
        ["ms_sdft", "mc_tendinitis_sdft"],  # 浅指屈腱炎 (Bowed Tendon)
        ["sk_ulcerative_lymph", "if_corynebacterium2"],  # 潰瘍性リンパ管炎
        ["if_ehv1_myeloencephalopathy", "if_ehv1_neuro"],  # EHV-1 脊髄脳症 (EHM)
        ["mt_hypocalcemia", "mt_hypocalcemia2"],  # 低カルシウム血症 (Transport Tetany)
        ["fl_perinatal_asphyxia", "fl_perinatal_asphyxia2"],  # 周産期仮死 (Dummy Foal)
    ],
    # The remaining species below encode ONLY the "firm" same-disease rows from
    # each .spec/<SPECIES>_CONSOLIDATION_REVIEW.md worksheet (species-tag / synonym
    # / abbreviation / staging / severity duplicates). Rows the worksheets flag as
    # ✏️要確認 (parent/child, morphotype, umbrella-vs-etiology, distinct-disease) and
    # all C-tier "分離維持" pairs are intentionally NOT included — they await an
    # explicit per-item veterinarian decision. A group may extend an auto cluster
    # (the loop attaches the extra members to the existing auto canonical).
    "ferret": [
        ["ferret_0003", "ferret_0193"],  # 副腎皮質機能亢進症
        ["ferret_0006", "ferret_0170"],  # 炎症性腸疾患 (IBD)
        ["ferret_0010", "ferret_0174"],  # 肝リピドーシス
        ["ferret_0012", "ferret_0166"],  # 流行性カタル性腸炎 (ECE)
        ["ferret_0014", "ferret_0183"],  # 拡張型心筋症 (DCM)
        ["ferret_0015", "ferret_0184"],  # 肥大型心筋症 (HCM)
        ["ferret_0018", "ferret_0164"],  # インフルエンザ
        ["ferret_0025", "ferret_0179"],  # 肥満細胞腫（皮膚型）
        ["ferret_0031", "ferret_0176"],  # 耳ダニ症
        ["ferret_0032", "ferret_0274"],  # 皮膚糸状菌症（auto 0177 に追加）
        ["ferret_0034", "ferret_0178"],  # 尾部脱毛（ラットテイル）
        ["ferret_0037", "ferret_0195"],  # 前立腺嚢胞
        ["ferret_0042", "ferret_0196"],  # 陰門腫脹
        ["ferret_0043", "ferret_0190"],  # 前立腺疾患
        ["ferret_0050", "ferret_0165"],  # アリューシャン病 (ADV)
        ["ferret_0054", "ferret_0167"],  # フェレット全身性コロナ (FRSCV)
        ["ferret_0066", "ferret_0194"],  # 低血糖症（インスリノーマ）
        ["ferret_0078", "ferret_0129"],  # 増殖性大腸炎
        ["ferret_0082", "ferret_0213"],  # 播種性特発性筋膜炎 (DIM)
    ],
    "hamster": [
        ["hamster_0000", "hamster_0155", "hamster_0156"],  # ウェットテイル（増殖性回腸炎）
        ["hamster_0001", "hamster_0174"],  # ティザー病
        ["hamster_0007", "hamster_0148"],  # 条虫症（Rodentolepis = Hymenolepis）
        ["hamster_0017", "hamster_0210"],  # 肺炎
        ["hamster_0020", "hamster_0160", "hamster_0161"],  # ニキビダニ症
        ["hamster_0023", "hamster_0269"],  # 皮膚糸状菌症（auto 0192 に追加）
        ["hamster_0026", "hamster_0196"],  # 脱毛症（非寄生虫性）
        ["hamster_0030", "hamster_0283"],  # 皮膚腫瘍
        ["hamster_0038", "hamster_0162", "hamster_0163", "hamster_0191"],  # クッシング病
        ["hamster_0045", "hamster_0164", "hamster_0165"],  # 心房血栓症
        ["hamster_0049", "hamster_0172", "hamster_0173", "hamster_0238"],  # ケージ麻痺
        ["hamster_0059", "hamster_0157", "hamster_0158"],  # ポリオーマウイルス
        ["hamster_0060", "hamster_0159"],  # リンパ球性脈絡髄膜炎 (LCMV)
        ["hamster_0068", "hamster_0221"],  # 熱中症（auto 0217 に追加）
        ["hamster_0123", "hamster_0318"],  # 趾瘤症（バンブルフット）
    ],
    "guinea_pig": [
        ["guinea_pig_0006", "guinea_pig_0201"],  # 鼓脹症（胃拡張）
        ["guinea_pig_0013", "guinea_pig_0126", "guinea_pig_0235"],  # 皮膚糸状菌症
        ["guinea_pig_0017", "guinea_pig_0168", "guinea_pig_0169"],  # 足底皮膚炎（バンブルフット）
        ["guinea_pig_0028", "guinea_pig_0166"],  # 難産
        ["guinea_pig_0029", "guinea_pig_0150", "guinea_pig_0164", "guinea_pig_0165"],  # 妊娠中毒症
        ["guinea_pig_0050", "guinea_pig_0157", "guinea_pig_0158", "guinea_pig_0159"],  # 壊血病
        ["guinea_pig_0066", "guinea_pig_0119"],  # 白血病（リンパ球性）
        ["guinea_pig_0074", "guinea_pig_0172"],  # 毛ダニ症
        ["guinea_pig_0077", "guinea_pig_0260"],  # 中耳炎・内耳炎
        ["guinea_pig_0082", "guinea_pig_0214"],  # 肝リピドーシス
        ["guinea_pig_0084", "guinea_pig_0102", "guinea_pig_0160"],  # 頸部リンパ節炎（auto 0246 に追加）
        ["guinea_pig_0087", "guinea_pig_0241"],  # 脱毛症
        ["guinea_pig_0121", "guinea_pig_0336"],  # ケトーシス（非妊娠）
        ["guinea_pig_0123", "guinea_pig_0175"],  # ビタミンA欠乏症
        ["guinea_pig_0191", "guinea_pig_0200"],  # 盲腸内細菌叢異常
    ],
    "chinchilla": [
        ["chinchilla_0000", "chinchilla_0163"],  # 不正咬合
        ["chinchilla_0003", "chinchilla_0143", "chinchilla_0174"],  # 流涎症
        ["chinchilla_0009", "chinchilla_0130"],  # 肝リピドーシス
        ["chinchilla_0013", "chinchilla_0167", "chinchilla_0171"],  # ファーリング（陰茎毛輪）
        ["chinchilla_0014", "chinchilla_0226"],  # 皮膚糸状菌症（auto 0251 に追加）
        ["chinchilla_0015", "chinchilla_0077", "chinchilla_0151", "chinchilla_0152", "chinchilla_0172"],  # 毛噛み
        ["chinchilla_0018", "chinchilla_0248"],  # 肺炎
        ["chinchilla_0020", "chinchilla_0038", "chinchilla_0168"],  # 熱中症（auto 0149 に追加）
        ["chinchilla_0028", "chinchilla_0104"],  # 乳腺炎
        ["chinchilla_0031", "chinchilla_0270"],  # 四肢骨折
        ["chinchilla_0048", "chinchilla_0237"],  # ケトーシス（妊娠中毒症）
        ["chinchilla_0103", "chinchilla_0190"],  # 妊娠中毒症
        ["chinchilla_0061", "chinchilla_0198"],  # 中耳炎・内耳炎
        ["chinchilla_0106", "chinchilla_0177"],  # 耳感染症（外耳炎）
        ["chinchilla_0115", "chinchilla_0271"],  # 変形性関節症
        ["chinchilla_0127", "chinchilla_0276"],  # 貧血
    ],
    "sugar_glider": [
        ["sugar_glider_0001", "sugar_glider_0135"],  # カルシウム欠乏症
        ["sugar_glider_0006", "sugar_glider_0088"],  # 低血糖症
        ["sugar_glider_0008", "sugar_glider_0080"],  # 鉄過剰症
        ["sugar_glider_0019", "sugar_glider_0155"],  # ダニ感染症
        ["sugar_glider_0022", "sugar_glider_0097"],  # トキソプラズマ症
        ["sugar_glider_0024", "sugar_glider_0219"],  # 肺炎
        ["sugar_glider_0026", "sugar_glider_0147"],  # 下痢
        ["sugar_glider_0043", "sugar_glider_0073", "sugar_glider_0193"],  # 育児嚢感染症（Joeyitis）
        ["sugar_glider_0044", "sugar_glider_0166"],  # てんかん発作（MBD関連）
        ["sugar_glider_0051", "sugar_glider_0153"],  # 肝リピドーシス
        ["sugar_glider_0059", "sugar_glider_0071", "sugar_glider_0138"],  # 飛膜損傷
        ["sugar_glider_0061", "sugar_glider_0180"],  # 熱中症
        ["sugar_glider_0069", "sugar_glider_0133"],  # 栄養性骨異栄養症（MBD）
        ["sugar_glider_0075", "sugar_glider_0170"],  # 難産
        ["sugar_glider_0038", "sugar_glider_0165"],  # 眼球突出 Proptosis（0188 Exophthalmos は分離）
    ],
    "hedgehog": [
        ["hedgehog_0002", "hedgehog_0093", "hedgehog_0149"],  # 皮膚糸状菌症（auto 0243 に追加）
        ["hedgehog_0015", "hedgehog_0121"],  # 肥満
        ["hedgehog_0016", "hedgehog_0174"],  # 下痢
        ["hedgehog_0017", "hedgehog_0143"],  # 消化管内異物
        ["hedgehog_0018", "hedgehog_0118"],  # 肝リピドーシス
        ["hedgehog_0026", "hedgehog_0241"],  # 肺炎
        ["hedgehog_0028", "hedgehog_0057"],  # マイコバクテリア症
        ["hedgehog_0040", "hedgehog_0166"],  # 眼球突出 Proptosis（0218 Exophthalmos は分離）
        ["hedgehog_0055", "hedgehog_0164"],  # 脂肪肝
        ["hedgehog_0069", "hedgehog_0140"],  # バルーン症候群
        ["hedgehog_0090", "hedgehog_0150"],  # カパリニアダニ症
    ],
    "dog": [
        ["dog_0065", "dog_0619"],  # 肢端舐性皮膚炎（舐性肉芽腫）
        ["dog_0077", "dog_0273"],  # 肥大性骨異栄養症 HOD
        ["dog_0080", "dog_0456"],  # 脊髄空洞症
        ["dog_0085", "dog_0600"],  # 乳腺炎
        ["dog_0087", "dog_0475"],  # 良性前立腺肥大症 BPH
        ["dog_0099", "dog_0454"],  # 変性性脊髄症 DM
        ["dog_0116", "dog_0228"],  # インスリノーマ
        ["dog_0121", "dog_0479"],  # 犬ヘルペスウイルス感染症 CHV
        ["dog_0204", "dog_0599"],  # 産後子宮炎
        ["dog_0215", "dog_0469"],  # エチレングリコール中毒
        ["dog_0277", "dog_0452"],  # 壊死性髄膜脳炎 NME（パグ脳炎）
        ["dog_0367", "dog_0458"],  # 肺血栓塞栓症 PTE
        ["dog_0398", "dog_0487"],  # 唾液腺嚢胞
        ["dog_0416", "dog_0418"],  # 中枢性尿崩症
        ["dog_0434", "dog_0477"],  # 犬ブルセラ症
        ["dog_0527", "dog_0620"],  # 肩関節離断性骨軟骨炎 OCD
    ],
    "bird": [
        ["bird_0000", "bird_0341"],  # 嘴羽毛病（PBFD）
        ["bird_0001", "bird_0400"],  # 腺胃拡張症（PDD）
        ["bird_0006", "bird_0403"],  # パチェコ病
        ["bird_0007", "bird_0343"],  # パラミクソウイルス感染症
        ["bird_0013", "bird_0437"],  # 大腸菌感染症
        ["bird_0023", "bird_0308"],  # カンジダ症
        ["bird_0024", "bird_0307"],  # メガバクテリア症（auto 0410 に追加）
        ["bird_0033", "bird_0408"],  # 嗉嚢停滞
        ["bird_0034", "bird_0409"],  # 嗉嚢火傷
        ["bird_0052", "bird_0444"],  # 腎腫瘍
        ["bird_0058", "bird_0414"],  # ヨウ素欠乏症
        ["bird_0063", "bird_0404"],  # 毛引き症
        ["bird_0069", "bird_0452"],  # 扁平上皮癌（皮膚）
        ["bird_0071", "bird_0431"],  # 代謝性骨疾患（MBD）
        ["bird_0073", "bird_0405"],  # 卵詰まり（難産）
        ["bird_0096", "bird_0421"],  # ワクモ（赤ダニ）
        ["bird_0098", "bird_0423"],  # 回虫症
        ["bird_0100", "bird_0232", "bird_0424"],  # 毛細線虫症
        ["bird_0112", "bird_0387"],  # 亜鉛中毒（auto 0461 に追加）
        ["bird_0126", "bird_0227"],  # 鳥脳脊髄炎
        ["bird_0127", "bird_0224"],  # マレック病
        ["bird_0130", "bird_0233"],  # 伝染性喉頭気管炎 ILT
        ["bird_0133", "bird_0235"],  # 鳥スピロヘータ症
        ["bird_0174", "bird_0439"],  # 総排泄腔炎
        ["bird_0176", "bird_0292"],  # 素嚢結石
    ],
    "parakeet": [
        ["parakeet_0011", "parakeet_0300"],  # マイコバクテリア症（鳥結核）
        ["parakeet_0023", "parakeet_0186"],  # 条虫症
        ["parakeet_0027", "parakeet_0252", "parakeet_0272"],  # メガバクテリア症
        ["parakeet_0053", "parakeet_0203", "parakeet_0254"],  # 開脚症
        ["parakeet_0058", "parakeet_0264"],  # 羽嚢腫
        ["parakeet_0059", "parakeet_0268"],  # 毛引き症
        ["parakeet_0067", "parakeet_0265", "parakeet_0270"],  # そ嚢停滞（サワークロップ）
        ["parakeet_0082", "parakeet_0330"],  # 熱傷・化学熱傷
        ["parakeet_0113", "parakeet_0299"],  # 大腸菌感染症
        ["parakeet_0133", "parakeet_0455"],  # 慢性羽包嚢胞
        ["parakeet_0241", "parakeet_0195"],  # 亜鉛中毒
        ["parakeet_0228", "parakeet_0362"],  # 慢性呼吸器疾患 CRD
        ["parakeet_0235", "parakeet_0262"],  # 蝋膜肥大
    ],
    "parrot": [
        ["parrot_0000", "parrot_0162"],  # 嘴羽毛病 PBFD
        ["parrot_0017", "parrot_0184"],  # カンジダ症
        ["parrot_0024", "parrot_0169"],  # 重金属中毒（鉛・亜鉛）
        ["parrot_0039", "parrot_0187"],  # 痛風（関節型・内臓型）
        ["parrot_0040", "parrot_0166"],  # 動脈硬化症（auto 0228 に追加）
        ["parrot_0043", "parrot_0181"],  # 卵塞（卵詰まり）
        ["parrot_0047", "parrot_0183"],  # 嗉嚢停滞
        ["parrot_0079", "parrot_0242"],  # 熱中症
        ["parrot_0108", "parrot_0215"],  # 大腸菌感染症
    ],
    "reptile": [
        ["reptile_0007", "reptile_0170"],  # チアミン欠乏症
        ["reptile_0020", "reptile_0187"],  # アメーバ感染症
        ["reptile_0027", "reptile_0190"],  # スケイルロット
        ["reptile_0033", "reptile_0188"],  # 吻部擦過傷
        ["reptile_0034", "reptile_0189"],  # 甲羅腐敗症（Shell Rot）
        ["reptile_0040", "reptile_0205"],  # 肝リピドーシス
        ["reptile_0063", "reptile_0198"],  # 腎不全
        ["reptile_0064", "reptile_0200"],  # 膀胱結石
        ["reptile_0074", "reptile_0244"],  # 高体温症
        ["reptile_0081", "reptile_0164"],  # 黄色真菌症（CANV）
        ["reptile_0153", "reptile_0168"],  # 壊死性皮膚炎
        ["reptile_0162", "reptile_0167"],  # 敗血症性皮膚潰瘍症（SCUD）
    ],
    "tortoise": [
        ["tortoise_0000", "tortoise_0167"],  # 甲羅腐敗症
        ["tortoise_0006", "tortoise_0224"],  # 肺炎
        ["tortoise_0032", "tortoise_0215"],  # 肝リピドーシス
        ["tortoise_0043", "tortoise_0162"],  # 卵塞
        ["tortoise_0063", "tortoise_0253"],  # 高体温症
        ["tortoise_0072", "tortoise_0250"],  # カルシウム欠乏症
        ["tortoise_0075", "tortoise_0231"],  # 眼感染症
        ["tortoise_0097", "tortoise_0186"],  # マイコバクテリア症
        ["tortoise_0041", "tortoise_0206"],  # 関節痛風（関節型どうし）
        ["tortoise_0042", "tortoise_0205"],  # 内臓痛風（内臓型どうし）
        ["tortoise_0158", "tortoise_0176"],  # 膀胱結石（尿酸塩型どうし）
        ["tortoise_0002", "tortoise_0233"],  # 甲羅骨折（甲羅どうし）
        ["tortoise_0035", "tortoise_0170"],  # 嘴の過成長・不正咬合
    ],
    "snake": [
        ["snake_0008", "snake_0201"],  # 肺炎
        ["snake_0012", "snake_0148"],  # ヘビダニ
        ["snake_0014", "snake_0170"],  # アメーバ感染症
        ["snake_0016", "snake_0167"],  # 舌虫症
        ["snake_0019", "snake_0172"],  # 水疱症
        ["snake_0020", "snake_0174"],  # スケイルロット
        ["snake_0026", "snake_0171"],  # 吻部擦過傷
        ["snake_0030", "snake_0190"],  # 肝リピドーシス
        ["snake_0044", "snake_0185"],  # 排卵後卵停滞
        ["snake_0082", "snake_0142", "snake_0143"],  # ヘビ真菌症（SFD）
        ["snake_0088", "snake_0165"],  # 条虫感染症
    ],
    "lizard": [
        ["lizard_0000", "lizard_0149"],  # 代謝性骨疾患（MBD）（NSHP 0001 は分離）
        ["lizard_0009", "lizard_0144"],  # アタデノウイルス感染症
        ["lizard_0014", "lizard_0142", "lizard_0145"],  # 黄色真菌症（CANV）
        ["lizard_0018", "lizard_0207"],  # 肺炎
        ["lizard_0024", "lizard_0170"],  # ダニ寄生（Ophionyssus）
        ["lizard_0026", "lizard_0177"],  # アメーバ感染症
        ["lizard_0033", "lizard_0181"],  # スケイルロット
        ["lizard_0036", "lizard_0178"],  # 吻部擦過傷
        ["lizard_0040", "lizard_0197"],  # 肝リピドーシス
        ["lizard_0064", "lizard_0236"],  # 高体温症
        ["lizard_0096", "lizard_0172"],  # 条虫感染症
        ["lizard_0019", "lizard_0161"],  # 感染性口内炎（auto 0141 に追加）
        ["lizard_0050", "lizard_0188"],  # 関節痛風（関節型どうし）
        ["lizard_0051", "lizard_0187"],  # 内臓痛風（内臓型どうし）
        ["lizard_0091", "lizard_0176"],  # 鞭毛虫感染症
        ["lizard_0030", "lizard_0151"],  # 脱皮残りによる趾壊死
        ["lizard_0049", "lizard_0194"],  # 半陰茎脱出
        ["lizard_0110", "lizard_0193"],  # 卵関連体腔炎
    ],
    "amphibian": [
        ["amphibian_0020", "amphibian_0178"],  # 代謝性骨疾患
        ["amphibian_0022", "amphibian_0254"],  # カルシウム欠乏症
        ["amphibian_0130", "amphibian_0198"],  # 熱傷（ヒートランプ）
    ],
    "exotic_other": [
        # generic-tag × generic-tag same-name merges only; specific-animal tags
        # (豚/ヤギ/スカンク/プレーリードッグ/有袋類/タランチュラ 等) stay separate (C-tier).
        ["exotic_other_0016", "exotic_other_0164"],  # 肝リピドーシス
        ["exotic_other_0017", "exotic_other_0172"],  # 糖尿病
        ["exotic_other_0019", "exotic_other_0182"],  # 上部気道感染症
        ["exotic_other_0025", "exotic_other_0199"],  # 直腸脱
        ["exotic_other_0027", "exotic_other_0211"],  # 歯根膿瘍
        ["exotic_other_0028", "exotic_other_0234"],  # 子宮蓄膿症
        ["exotic_other_0029", "exotic_other_0236"],  # 難産
        ["exotic_other_0030", "exotic_other_0237"],  # 乳腺腫瘍
        ["exotic_other_0033", "exotic_other_0143"],  # 狂犬病
        ["exotic_other_0034", "exotic_other_0220"],  # 前庭疾患
        ["exotic_other_0035", "exotic_other_0187"],  # 皮膚糸状菌症
        ["exotic_other_0038", "exotic_other_0191"],  # 接触性皮膚炎
        ["exotic_other_0045", "exotic_other_0238"],  # リンパ腫
        ["exotic_other_0046", "exotic_other_0167"],  # 皮膚腫瘍
        ["exotic_other_0048", "exotic_other_0154"],  # 野兎病
        ["exotic_other_0049", "exotic_other_0203"],  # サルモネラ症
        ["exotic_other_0054", "exotic_other_0165"],  # 腎疾患
        ["exotic_other_0056", "exotic_other_0173"],  # 副腎疾患
        ["exotic_other_0024", "exotic_other_0147"],  # 腸管寄生虫症（汎用のみ）
        ["exotic_other_0015", "exotic_other_0163"],  # 代謝性骨疾患（汎用のみ）
        ["exotic_other_0053", "exotic_other_0233"],  # 尿路結石症（汎用のみ）
        ["exotic_other_0057", "exotic_other_0174"],  # 心疾患（汎用のみ）
        ["exotic_other_0044", "exotic_other_0171", "exotic_other_0229"],  # 肥満症（汎用のみ）
    ],
}


# Second tier: worksheet ✏️要確認 rows that a veterinarian has since confirmed
# are the SAME disease (staging/severity/species-tag/spelling/synonym/subset-of-
# umbrella/complication-annotation). Kept SEPARATE from _CURATED_MERGE so the two
# approval waves stay auditable and independently reversible. Rows that are rename
# candidates (label errors = different entities), genuine parent/child, or require
# taxonomic review are deliberately NOT here (they stay unmerged pending a rename
# or an explicit keep-distinct decision).
_CURATED_MERGE_VETFLAGGED: dict[str, list[list[str]]] = {
    "hamster": [
        ["hamster_0041", "hamster_0166", "hamster_0167"],  # 全身性アミロイドーシス（臓器優位型）
        ["hamster_0086", "hamster_0170", "hamster_0171"],  # 冬眠症候群（重症度）
        ["hamster_0092", "hamster_0202"],  # 腸閉塞（糞便嵌頓＝機械性）
        ["hamster_0168", "hamster_0169"],  # 多発性嚢胞性疾患（臓器型）
    ],
    "guinea_pig": [
        ["guinea_pig_0162", "guinea_pig_0163", "guinea_pig_0290"],  # 抗生物質関連腸性中毒（薬剤クラス別）
    ],
    "chinchilla": [
        ["chinchilla_0006", "chinchilla_0150"],  # 便秘（慢性）※巨大結腸症 0175 は別疾患で分離維持
    ],
    "reptile": [
        ["reptile_0043", "reptile_0212", "reptile_0254"],  # 食欲不振（非特異/行動性/ストレス性）
        ["reptile_0058", "reptile_0161"],  # 排卵前卵胞停滞（卵黄性体腔炎の続発注記）
    ],
    "tortoise": [
        ["tortoise_0050", "tortoise_0201"],  # 皮下膿瘍（一般膿瘍＝皮下）
        ["tortoise_0079", "tortoise_0190"],  # ダニ寄生（Ophionyssus）
        ["tortoise_0116", "tortoise_0178"],  # 慢性濾胞停滞
        ["tortoise_0221", "tortoise_0262"],  # 拒食（行動性/ストレス性）
        ["tortoise_0017", "tortoise_0172", "tortoise_0196"],  # 鞭毛虫感染症（綴り差）
        ["tortoise_0008", "tortoise_0185"],  # マイコプラズマ症（0166 URTD は別）
        ["tortoise_0018", "tortoise_0195"],  # コクシジウム症（TINC 0013 は別病原体で分離）
        ["tortoise_0057", "tortoise_0212"],  # 陰茎/半陰茎脱出
        ["tortoise_0056", "tortoise_0222"],  # 総排泄腔/直腸脱
        ["tortoise_0115", "tortoise_0211"],  # 卵黄性体腔炎
    ],
    "snake": [
        ["snake_0001", "snake_0156"],  # パラミクソウイルス感染症（種タグ）
        ["snake_0051", "snake_0151"],  # 脊椎骨症（種タグ）
        ["snake_0045", "snake_0187"],  # 半陰茎脱出（種タグ）
        ["snake_0089", "snake_0169"],  # 鞭毛虫感染症（綴り差）
        ["snake_0012", "snake_0163"],  # ヘビダニ（Ophionyssus 追加）
        ["snake_0049", "snake_0180"],  # 内臓痛風（二重登録・同型）
        ["snake_0048", "snake_0181"],  # 関節痛風（二重登録・同型）
    ],
    "lizard": [
        ["lizard_0017", "lizard_0208"],  # 上部呼吸器感染症（URI/URTD）
        ["lizard_0048", "lizard_0205"],  # 総排泄腔/直腸脱
    ],
    "parakeet": [
        ["parakeet_0034", "parakeet_0257"],  # 肝リピドーシス（種子食）
        ["parakeet_0038", "parakeet_0196"],  # テフロン中毒（PTFE）
        ["parakeet_0042", "parakeet_0256"],  # 精巣腫瘍（ろう膜変色）
        ["parakeet_0043", "parakeet_0177", "parakeet_0263"],  # 黄色腫（進行型/翼）
        ["parakeet_0127", "parakeet_0226"],  # 腺胃潰瘍（セキセイ）
    ],
    "parrot": [
        ["parrot_0001", "parrot_0160", "parrot_0161", "parrot_0177"],  # 腺胃拡張症 PDD を 0001 に一本化
    ],
    "bird": [
        ["bird_0048", "bird_0445"],  # 腎不全（急性を急性/慢性 umbrella へ）
        ["bird_0111", "bird_0079"],  # 鉛中毒（神経型は一発現）
        ["bird_0295", "bird_0383"],  # 卵停滞（産卵前）
        ["bird_0406", "bird_0349"],  # バンブルフット（外科ステージ）
    ],
}


def _slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", (name or "").lower()).strip("-")


def _richness(rec: dict) -> tuple[int, int]:
    """Mirror dedupe_disease_list's richness: (#non-empty content fields, total len)."""
    fields = (
        "description",
        "description_ja",
        "causes",
        "causes_ja",
        "pathophysiology",
        "pathophysiology_ja",
        "treatment",
        "treatment_ja",
        "prevention",
        "prevention_ja",
        "prognosis",
        "prognosis_ja",
    )
    non_empty = sum(1 for f in fields if str(rec.get(f, "") or "").strip())
    total = sum(len(str(rec.get(f, "") or "")) for f in fields)
    return (non_empty, total)


def build(species: str) -> dict:
    records = detect.load_species_records(species)
    by_id = {r["id"]: r for r in records}
    dup = detect.detect_duplicates(records)
    nonclin = detect.detect_nonclinical(records)

    def ident(rid: str) -> dict:
        r = by_id.get(rid, {})
        return {
            "id": rid,
            "slug": _slug(r.get("name") or r.get("name_en") or ""),
            "name": r.get("name") or r.get("name_en"),
            "name_ja": r.get("name_ja"),
        }

    # The species tag "（デグー）" / "(Degu)" marks the auto-added duplicate; the
    # clean base entry should win as canonical. Demote that tag specifically
    # rather than penalising all parentheses (informative qualifiers like
    # "Ringworm (Dermatophytosis)" must not be demoted).
    sp_ja = _SPECIES_JA.get(species, species)
    _species_tags = [f"（{sp_ja}）", f"({species})", f"({species.title()})"]

    def _cleanliness(rid: str) -> tuple:
        """Lower is cleaner: prefer names without the species tag, then shorter
        name, then richer content."""
        r = by_id[rid]
        ja = str(r.get("name_ja") or "")
        en = str(r.get("name") or r.get("name_en") or "")
        has_species_tag = int(any(t in ja or t in en for t in _species_tags))
        rich = _richness(r)
        return (has_species_tag, len(ja) + len(en), -rich[0], -rich[1])

    # STRICT safe-merge key: identity AFTER removing only the species tag
    # "（<species>）"/"(<species>)" (other qualifiers kept). detect.py clusters on
    # parenthesis-STRIPPED names, which conflates clinical subtypes
    # (e.g. "パスツレラ症（結膜型）" vs "（敗血症型）"). Only entries that are the same
    # disease modulo the species tag are auto-merged; the rest go to review.
    def _mergekey(rid: str) -> str:
        r = by_id[rid]
        ja = str(r.get("name_ja") or "")
        en = str(r.get("name") or r.get("name_en") or "")
        for t in _species_tags:
            ja = ja.replace(t, "")
            en = en.replace(t, "")
        base = ja.strip() or en.strip().lower()
        return re.sub(r"[\s・、,，。.\-ー―－]", "", base)

    # --- merges: STRICT — only species-tag / identical duplicates auto-apply ---
    # The canonical keeps the CLEANEST name; the loader inherits the richest
    # content from all merged siblings (non-destructive, at load time).
    merges = []
    review_oversplit = []
    for cluster in dup.get("exact_duplicate_clusters", []):
        ids = [m["id"] for m in cluster.get("members", []) if m.get("id") in by_id]
        if len(ids) < 2:
            continue
        # Sub-group cluster members by the strict safe-merge key.
        groups: dict[str, list[str]] = {}
        for rid in ids:
            groups.setdefault(_mergekey(rid), []).append(rid)
        safe_groups = [g for g in groups.values() if len(g) >= 2]
        for g in safe_groups:
            if _is_forbidden_pair(species, g):
                review_oversplit.append(
                    {
                        "base": by_id[g[0]].get("name"),
                        "note": "mislabeled name_ja shared by clinically DISTINCT diseases — do NOT merge (rename pending)",
                        "members": [ident(rid) for rid in g],
                    }
                )
                continue
            canonical_id = min(g, key=_cleanliness)
            merged = [rid for rid in g if rid != canonical_id]
            merges.append(
                {
                    "canonical": ident(canonical_id),
                    "merged": [ident(rid) for rid in merged],
                    "reason": "same disease modulo species tag / identical name",
                    "inherit_content": True,
                }
            )
        # Members that are NOT safe-mergeable but detect grouped them (differ by a
        # non-species qualifier = possible over-split subtype) → review, not applied.
        if len(groups) > 1:
            review_oversplit.append(
                {
                    "base": cluster.get("members", [{}])[0].get("name"),
                    "note": "detect grouped these by base name; differ by qualifier — review whether subtypes or duplicates",
                    "members": [ident(rid) for rid in ids],
                }
            )

    # --- curated vet-approved same-disease merges (held back by the strict key) ---
    # A curated group may either stand alone OR extend a cluster the strict auto
    # key already merged (e.g. worksheet "0002 ← 0093, 0149" where 0002 is the
    # auto canonical). Track where each id has been placed so curated members
    # attach to the existing canonical instead of forming a wrong split cluster.
    _placed: dict[str, str] = {}
    for m in merges:
        cid = m["canonical"]["id"]
        _placed[cid] = cid
        for mm in m["merged"]:
            _placed[mm["id"]] = cid
    _merge_by_canon = {m["canonical"]["id"]: m for m in merges}

    for group in _CURATED_MERGE.get(species, []) + _CURATED_MERGE_VETFLAGGED.get(species, []):
        present = [rid for rid in group if rid in by_id]
        if len(present) < 2:
            continue  # ids absent → skip (idempotent)
        # If any member already belongs to a cluster, attach the rest to it.
        existing = next((_placed[rid] for rid in present if rid in _placed), None)
        if existing is not None:
            new_members = [rid for rid in present if rid not in _placed]
            if not new_members:
                continue  # everything already merged here (idempotent re-run)
            target = _merge_by_canon[existing]
            for rid in new_members:
                target["merged"].append(ident(rid))
                _placed[rid] = existing
            target["curated"] = True
        else:
            canonical_id = present[0]
            entry = {
                "canonical": ident(canonical_id),
                "merged": [ident(rid) for rid in present[1:]],
                "reason": "vet-approved same disease (curated; differs by an informative qualifier)",
                "inherit_content": True,
                "curated": True,
            }
            merges.append(entry)
            _merge_by_canon[canonical_id] = entry
            for rid in present:
                _placed[rid] = canonical_id
    _auto_ids = set(_placed)
    # Drop review-oversplit entries whose members are now FULLY resolved by a
    # merge (keep entries that still contain an unmerged subtype).
    review_oversplit = [o for o in review_oversplit if not all(m["id"] in _auto_ids for m in o.get("members", []))]

    # --- archives: unambiguous non-clinical (research models) ---
    # detect.py flags research_model / human_medicine_transplant by keyword, but
    # a keyword alone is unsafe (e.g. "Equine Parkinsonism" is a real toxicosis,
    # not a model). Auto-archive ONLY when the NAME itself declares a model
    # ("様疾患", "-like disease", "model"/"モデル"). Everything else → review.
    def _is_declared_model(rid: str) -> bool:
        r = by_id[rid]
        ja = str(r.get("name_ja") or "")
        en = str(r.get("name") or r.get("name_en") or "").lower()
        return ("様疾患" in ja) or ("モデル" in ja) or ("-like" in en) or ("model" in en)

    archives = []
    review_nonclinical = []
    for f in nonclin.get("flags", []):
        entry = ident(f["id"]) | {"matches": f.get("matches", [])}
        if _is_declared_model(f["id"]):
            archives.append(entry | {"reason": "declared research model (name says model/様疾患/-like)"})
        else:
            review_nonclinical.append(
                entry | {"note": "keyword-flagged non-clinical — review (may be a real toxicosis/transplant)"}
            )

    # --- review: over-split families (NOT applied) ---
    review_families = []
    for fam in dup.get("family_clusters", []):
        review_families.append(fam)

    merged_slugs = {m["slug"] for grp in merges for m in grp["merged"]}
    archived_slugs = {a["slug"] for a in archives}

    return {
        "species": species,
        "schema_version": 1,
        "generated_note": "Non-destructive consolidation map. Applied at load time; sources unchanged.",
        "counts": {
            "records": len(records),
            "merge_clusters": len(merges),
            "records_merged_away": len(merged_slugs),
            "archived": len(archived_slugs),
            "served_after": len(records) - len(merged_slugs) - len(archived_slugs),
        },
        "merges": merges,
        "archives": archives,
        "review": {
            "nonclinical_transplants": review_nonclinical,
            "oversplit_subtypes": review_oversplit,
            "split_families": review_families,
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("species", nargs="?", default="degu")
    ap.add_argument("--apply", action="store_true", help="write the map file (otherwise dry-run to stdout)")
    args = ap.parse_args()

    result = build(args.species)
    counts = result["counts"]
    print(
        f"[{args.species}] records={counts['records']} "
        f"merge_clusters={counts['merge_clusters']} "
        f"merged_away={counts['records_merged_away']} "
        f"archived={counts['archived']} -> served_after={counts['served_after']}"
    )

    if not args.apply:
        print("(dry-run — pass --apply to write the map)")
        print(json.dumps(result, ensure_ascii=False, indent=2)[:2000])
        return 0

    CANON_DIR.mkdir(parents=True, exist_ok=True)
    out = CANON_DIR / f"{args.species}.json"
    if out.exists():
        stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H%M")
        bak = ROOT / "backups" / stamp
        bak.mkdir(parents=True, exist_ok=True)
        shutil.copy2(out, bak / out.name)
        print(f"backed up existing map -> {bak / out.name}")
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
