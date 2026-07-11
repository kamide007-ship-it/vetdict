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
    # dog: same-disease synonym/acronym/qualifier pairs. Kept SEPARATE in review
    # (distinct): PSS congenital vs acquired, HSA splenic vs cardiac, nasal
    # aspergillosis, acquired megacolon.
    "dog": [
        ["dog_0019", "dog_0297"],  # 犬アトピー性皮膚炎 (CAD)
        ["dog_0055", "dog_0484"],  # 門脈体循環シャント (generic; keep 先天性/後天性)
        ["dog_0065", "dog_0619"],  # 肢端舐性皮膚炎 (舐性肉芽腫)
        ["dog_0077", "dog_0273"],  # 肥大性骨異栄養症 (HOD)
        ["dog_0080", "dog_0456"],  # 脊髄空洞症
        ["dog_0085", "dog_0600"],  # 乳腺炎
        ["dog_0087", "dog_0475"],  # 前立腺肥大症 (BPH)
        ["dog_0099", "dog_0454"],  # 変性性脊髄症 (DM)
        ["dog_0116", "dog_0228"],  # インスリノーマ = 膵β細胞腫瘍
        ["dog_0121", "dog_0479"],  # 犬ヘルペスウイルス感染症
        ["dog_0204", "dog_0599"],  # 産後子宮炎
        ["dog_0215", "dog_0469"],  # エチレングリコール中毒
        ["dog_0231", "dog_0514"],  # 肝細胞癌
        ["dog_0277", "dog_0452"],  # 壊死性髄膜脳炎 (NME/パグ脳炎)
        ["dog_0367", "dog_0458"],  # 肺血栓塞栓症 (PTE)
        ["dog_0398", "dog_0487"],  # 唾液腺嚢胞/嚢腫
        ["dog_0416", "dog_0418"],  # 中枢性尿崩症
        ["dog_0419", "dog_0449"],  # 頸部脊椎脊髄症 (CSM/Wobbler)
        ["dog_0434", "dog_0477"],  # 犬ブルセラ症
        ["dog_0527", "dog_0620"],  # 肩関節離断性骨軟骨炎 (OCD)
    ],
    # ferret: base+qualifier vs species-tag duplicates (all same disease).
    "ferret": [
        ["ferret_0003", "ferret_0193"],  # 副腎皮質機能亢進症
        ["ferret_0004", "ferret_0147"],  # 消化管異物
        ["ferret_0006", "ferret_0170"],  # 炎症性腸疾患 (IBD)
        ["ferret_0010", "ferret_0174"],  # 肝リピドーシス
        ["ferret_0012", "ferret_0166"],  # 流行性カタル性腸炎 (ECE)
        ["ferret_0014", "ferret_0183"],  # 拡張型心筋症 (DCM)
        ["ferret_0015", "ferret_0184"],  # 肥大型心筋症 (HCM)
        ["ferret_0018", "ferret_0164"],  # インフルエンザ
        ["ferret_0025", "ferret_0179"],  # 肥満細胞腫
        ["ferret_0031", "ferret_0176"],  # 耳ダニ症
        ["ferret_0032", "ferret_0177", "ferret_0274"],  # 皮膚糸状菌症 (Microsporum)
        ["ferret_0034", "ferret_0178"],  # 尾部脱毛 (副腎性)
        ["ferret_0037", "ferret_0195"],  # 前立腺嚢胞
        ["ferret_0042", "ferret_0196"],  # 陰門/外陰部腫脹
        ["ferret_0043", "ferret_0190"],  # 前立腺疾患
        ["ferret_0050", "ferret_0165"],  # アリューシャン病
        ["ferret_0054", "ferret_0167"],  # 全身性コロナウイルス感染症
        ["ferret_0066", "ferret_0194"],  # 低血糖症 (インスリノーマ)
        ["ferret_0078", "ferret_0129"],  # 増殖性大腸炎
        ["ferret_0082", "ferret_0213"],  # 播種性特発性筋膜炎 (DIM)
        ["ferret_0088", "ferret_0143"],  # 骨腫
    ],
    # bird: same-disease synonym / species-tag / severity pairs. Kept SEPARATE:
    # 翼骨折 vs 脚骨折 (different bones).
    "bird": [
        ["bird_0000", "bird_0341"],  # PBFD
        ["bird_0001", "bird_0400"],  # 前胃拡張症 (PDD)
        ["bird_0006", "bird_0403"],  # パチェコ病
        ["bird_0007", "bird_0343"],  # パラミクソウイルス
        ["bird_0013", "bird_0437"],  # 大腸菌感染症
        ["bird_0023", "bird_0308"],  # カンジダ症
        ["bird_0024", "bird_0307", "bird_0410"],  # メガバクテリア症
        ["bird_0031", "bird_0417"],  # 細菌性肺炎
        ["bird_0033", "bird_0408"],  # そ嚢うっ滞
        ["bird_0034", "bird_0409"],  # そ嚢火傷
        ["bird_0048", "bird_0445"],  # 腎不全
        ["bird_0052", "bird_0444"],  # 腎腫瘍
        ["bird_0058", "bird_0414"],  # ヨウ素欠乏症
        ["bird_0059", "bird_0415"],  # 鉄蓄積症
        ["bird_0063", "bird_0404"],  # 毛引き症
        ["bird_0069", "bird_0452"],  # 扁平上皮癌
        ["bird_0071", "bird_0431"],  # 代謝性骨疾患
        ["bird_0073", "bird_0405"],  # 卵詰まり
        ["bird_0079", "bird_0111", "bird_0460"],  # 鉛中毒
        ["bird_0096", "bird_0421"],  # ワクモ
        ["bird_0098", "bird_0423"],  # 回虫症
        ["bird_0100", "bird_0232", "bird_0424"],  # 毛細線虫症
        ["bird_0112", "bird_0387", "bird_0461"],  # 亜鉛中毒
        ["bird_0126", "bird_0227"],  # 鳥脳脊髄炎
        ["bird_0127", "bird_0224"],  # マレック病
        ["bird_0130", "bird_0233"],  # 伝染性喉頭気管炎
        ["bird_0133", "bird_0235"],  # 鳥スピロヘータ症
        ["bird_0174", "bird_0439"],  # 総排泄腔炎
        ["bird_0176", "bird_0292"],  # そ嚢結石
        ["bird_0295", "bird_0383"],  # 卵停滞
        ["bird_0349", "bird_0406"],  # バンブルフット
    ],
    # parakeet: Kept SEPARATE: 内臓痛風 vs 関節痛風 (distinct forms), 肝炎 vs
    # 肝リピドーシス, そ嚢異物閉塞 (obstruction) vs stasis.
    "parakeet": [
        ["parakeet_0011", "parakeet_0300"],  # 鳥結核症
        ["parakeet_0023", "parakeet_0186"],  # 条虫症
        ["parakeet_0024", "parakeet_0155"],  # ダニ寄生症
        ["parakeet_0027", "parakeet_0252", "parakeet_0272"],  # メガバクテリア症
        ["parakeet_0034", "parakeet_0257"],  # 肝リピドーシス
        ["parakeet_0038", "parakeet_0196"],  # テフロン中毒
        ["parakeet_0042", "parakeet_0256", "parakeet_0305"],  # 精巣腫瘍
        ["parakeet_0043", "parakeet_0177", "parakeet_0263", "parakeet_0317"],  # 黄色腫
        ["parakeet_0053", "parakeet_0203", "parakeet_0254"],  # 開脚症
        ["parakeet_0058", "parakeet_0264"],  # 羽嚢腫
        ["parakeet_0059", "parakeet_0268"],  # 毛引き症
        ["parakeet_0067", "parakeet_0265", "parakeet_0270", "parakeet_0334"],  # そ嚢停滞 (keep 0206 異物閉塞 separate)
        ["parakeet_0070", "parakeet_0335"],  # 乳頭腫症
        ["parakeet_0082", "parakeet_0330"],  # 熱傷
        ["parakeet_0113", "parakeet_0299"],  # 大腸菌感染症
        ["parakeet_0127", "parakeet_0226"],  # 腺胃潰瘍
        ["parakeet_0133", "parakeet_0455"],  # 羽包嚢胞
        ["parakeet_0195", "parakeet_0241"],  # 亜鉛中毒
        ["parakeet_0228", "parakeet_0362"],  # 慢性呼吸器疾患
        ["parakeet_0235", "parakeet_0262"],  # 蝋膜肥大
    ],
    # parrot: Kept SEPARATE: 翼骨折 vs 脚骨折, 肝炎 vs 肝リピドーシス.
    "parrot": [
        ["parrot_0000", "parrot_0162"],  # PBFD
        ["parrot_0006", "parrot_0167", "parrot_0251"],  # 乳頭腫症
        ["parrot_0017", "parrot_0184"],  # カンジダ症
        ["parrot_0024", "parrot_0169"],  # 重金属中毒
        ["parrot_0039", "parrot_0187"],  # 痛風 (両型ラベル)
        ["parrot_0040", "parrot_0166", "parrot_0228"],  # 動脈硬化症
        ["parrot_0043", "parrot_0181"],  # 卵塞
        ["parrot_0047", "parrot_0183"],  # そ嚢うっ滞
        ["parrot_0079", "parrot_0242"],  # 熱中症
        ["parrot_0108", "parrot_0215"],  # 大腸菌感染症
        ["parrot_0125", "parrot_0270"],  # 消化管閉塞
        ["parrot_0160", "parrot_0161", "parrot_0177"],  # 前胃拡張症 (PDD)
    ],
    # reptile group + exotic_other: same-disease base+species-tag pairs
    # (exact base-name match only; synonym pairs like スケイルロット/鱗腐敗 and
    # multi-form clusters — 内臓/関節痛風, 四肢/甲羅骨折, 熱傷/化学熱傷, 温熱/低温,
    # Bd/Bsal ツボカビ, 食欲不振/拒食 — deliberately left in review).
    "reptile": [
        ["reptile_0007", "reptile_0170"],
        ["reptile_0040", "reptile_0205"],
        ["reptile_0058", "reptile_0161"],
        ["reptile_0063", "reptile_0198"],
        ["reptile_0064", "reptile_0200"],
        ["reptile_0074", "reptile_0244"],
        ["reptile_0153", "reptile_0168"],
    ],
    "tortoise": [
        ["tortoise_0006", "tortoise_0224"],
        ["tortoise_0032", "tortoise_0215"],
        ["tortoise_0040", "tortoise_0158", "tortoise_0176", "tortoise_0209"],
        # NB: Egg Binding (Dystocia) tortoise_0043/0162 share an identical English
        # name (→ identical slug); dedupe_disease_list already collapses them, so
        # not listed here (the slug-based loader cannot merge same-slug entries).
        ["tortoise_0063", "tortoise_0253"],
        ["tortoise_0072", "tortoise_0250"],
        ["tortoise_0075", "tortoise_0231"],
    ],
    "snake": [
        ["snake_0008", "snake_0201"],
        ["snake_0012", "snake_0148"],
        ["snake_0030", "snake_0190"],
        ["snake_0044", "snake_0185"],
    ],
    "lizard": [
        ["lizard_0018", "lizard_0207"],
        ["lizard_0040", "lizard_0197"],
        ["lizard_0064", "lizard_0236"],
    ],
    "amphibian": [
        ["amphibian_0020", "amphibian_0178"],
        ["amphibian_0022", "amphibian_0254"],
        ["amphibian_0036", "amphibian_0220"],
        ["amphibian_0130", "amphibian_0198"],
    ],
    "exotic_other": [
        ["exotic_other_0005", "exotic_other_0202"],
        ["exotic_other_0012", "exotic_other_0149"],
        ["exotic_other_0013", "exotic_other_0024", "exotic_other_0066", "exotic_other_0147"],
        ["exotic_other_0015", "exotic_other_0065", "exotic_other_0163"],
        ["exotic_other_0016", "exotic_other_0164"],
        ["exotic_other_0017", "exotic_other_0172"],
        ["exotic_other_0019", "exotic_other_0182"],
        ["exotic_other_0025", "exotic_other_0199"],
        ["exotic_other_0028", "exotic_other_0234"],
        ["exotic_other_0029", "exotic_other_0236"],
        ["exotic_other_0030", "exotic_other_0237"],
        ["exotic_other_0032", "exotic_other_0144"],
        ["exotic_other_0033", "exotic_other_0143"],
        ["exotic_other_0034", "exotic_other_0220"],
        ["exotic_other_0035", "exotic_other_0187"],
        ["exotic_other_0038", "exotic_other_0191"],
        ["exotic_other_0045", "exotic_other_0238"],
        ["exotic_other_0046", "exotic_other_0167"],
        ["exotic_other_0047", "exotic_other_0155"],
        ["exotic_other_0048", "exotic_other_0154"],
        ["exotic_other_0049", "exotic_other_0203"],
        ["exotic_other_0052", "exotic_other_0150"],
        ["exotic_other_0054", "exotic_other_0165"],
        ["exotic_other_0056", "exotic_other_0173"],
        ["exotic_other_0057", "exotic_other_0063", "exotic_other_0174"],
        ["exotic_other_0067", "exotic_other_0240"],
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
    _auto_ids = {m["canonical"]["id"] for m in merges} | {mm["id"] for m in merges for mm in m["merged"]}
    for group in _CURATED_MERGE.get(species, []):
        present = [rid for rid in group if rid in by_id and rid not in _auto_ids]
        if len(present) < 2:
            continue  # already handled by auto-merge or ids absent → skip (idempotent)
        canonical_id = present[0]
        merged = present[1:]
        merges.append(
            {
                "canonical": ident(canonical_id),
                "merged": [ident(rid) for rid in merged],
                "reason": "vet-approved same disease (curated; differs by an informative qualifier)",
                "inherit_content": True,
                "curated": True,
            }
        )
        _auto_ids.update(present)
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
