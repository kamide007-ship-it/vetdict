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
    # Small exotic mammals: same disease split by stage / form / severity / organ
    # / species-tag (the "水増し" pattern). Vet-approved clear same-disease merges
    # only; "要確認/✏️" and separate-maintain (C) clusters left in review.
    # See .spec/<SPECIES>_CONSOLIDATION_REVIEW.md. First id = canonical (kept).
    "hamster": [
        ["hamster_0000", "hamster_0155", "hamster_0156"],  # ウェットテイル（増殖性回腸炎）
        ["hamster_0001", "hamster_0174"],  # ティザー病（+不顕性）
        ["hamster_0007", "hamster_0148"],  # 条虫症 Hymenolepis=Rodentolepis nana
        ["hamster_0017", "hamster_0210"],  # 肺炎（+細菌性）
        ["hamster_0020", "hamster_0160", "hamster_0161"],  # ニキビダニ症（局所/全身）
        ["hamster_0023", "hamster_0269"],  # 皮膚糸状菌症（+白癬 Trichophyton）
        ["hamster_0026", "hamster_0196"],  # 脱毛症（非寄生虫性）
        ["hamster_0030", "hamster_0283"],  # 皮膚腫瘍（+非特異的）
        ["hamster_0038", "hamster_0162", "hamster_0163", "hamster_0191"],  # クッシング病（病期4件）
        ["hamster_0045", "hamster_0164", "hamster_0165"],  # 心房血栓症（急性/慢性）
        ["hamster_0049", "hamster_0172", "hamster_0173", "hamster_0238"],  # ケージ麻痺（病期4件）
        ["hamster_0059", "hamster_0157", "hamster_0158"],  # ポリオーマウイルス（顕/不顕性）
        ["hamster_0060", "hamster_0159"],  # LCMV（+急性型）
        ["hamster_0068", "hamster_0221"],  # 熱中症（+神経型）
        ["hamster_0123", "hamster_0318"],  # 趾瘤症（バンブルフット）
    ],
    "guinea_pig": [
        ["guinea_pig_0006", "guinea_pig_0201"],  # 鼓脹症（+胃鼓脹）
        ["guinea_pig_0013", "guinea_pig_0126", "guinea_pig_0235"],  # 皮膚糸状菌症
        ["guinea_pig_0017", "guinea_pig_0168", "guinea_pig_0169"],  # 足底皮膚炎（グレード）
        ["guinea_pig_0028", "guinea_pig_0166"],  # 難産（+胎子過大）
        ["guinea_pig_0029", "guinea_pig_0150", "guinea_pig_0164", "guinea_pig_0165"],  # 妊娠中毒症（時期4件）
        ["guinea_pig_0050", "guinea_pig_0157", "guinea_pig_0158", "guinea_pig_0159"],  # 壊血病（病型4件）
        ["guinea_pig_0066", "guinea_pig_0119"],  # 白血病（+リンパ球性）
        ["guinea_pig_0074", "guinea_pig_0172"],  # 毛ダニ症（+重度）
        ["guinea_pig_0077", "guinea_pig_0260"],  # 中耳/内耳炎
        ["guinea_pig_0082", "guinea_pig_0214"],  # 肝リピドーシス
        ["guinea_pig_0084", "guinea_pig_0102", "guinea_pig_0160"],  # 頸部リンパ節炎（起因菌）
        ["guinea_pig_0087", "guinea_pig_0241"],  # 脱毛症（非特異性）
        ["guinea_pig_0121", "guinea_pig_0336"],  # ケトーシス（非妊娠）
        ["guinea_pig_0123", "guinea_pig_0175"],  # ビタミンA欠乏症（+眼型）
        ["guinea_pig_0191", "guinea_pig_0200"],  # 盲腸内細菌叢異常
    ],
    "chinchilla": [
        ["chinchilla_0000", "chinchilla_0163"],  # 不正咬合（+進行性）
        ["chinchilla_0003", "chinchilla_0143", "chinchilla_0174"],  # 流涎症
        ["chinchilla_0009", "chinchilla_0130"],  # 肝リピドーシス（+重症型）
        ["chinchilla_0013", "chinchilla_0167", "chinchilla_0171"],  # ファーリング（陰茎毛輪）
        ["chinchilla_0014", "chinchilla_0226"],  # 皮膚糸状菌症（+ミクロスポルム）
        ["chinchilla_0015", "chinchilla_0077", "chinchilla_0151", "chinchilla_0152", "chinchilla_0172"],  # 毛噛み5件
        ["chinchilla_0018", "chinchilla_0248"],  # 肺炎（+細菌性）
        ["chinchilla_0020", "chinchilla_0038", "chinchilla_0168"],  # 熱中症（病型）
        ["chinchilla_0028", "chinchilla_0104"],  # 乳腺炎（+急性）
        ["chinchilla_0031", "chinchilla_0270"],  # 四肢骨折
        ["chinchilla_0048", "chinchilla_0237"],  # ケトーシス（妊娠中毒症）
        ["chinchilla_0103", "chinchilla_0190"],  # 妊娠中毒症（早期）
        ["chinchilla_0061", "chinchilla_0198"],  # 中耳/内耳炎
        ["chinchilla_0106", "chinchilla_0177"],  # 耳感染症（外耳炎）
        ["chinchilla_0115", "chinchilla_0271"],  # 変形性関節症
        ["chinchilla_0127", "chinchilla_0276"],  # 貧血（非特異的）
    ],
    "sugar_glider": [
        ["sugar_glider_0001", "sugar_glider_0135"],  # カルシウム欠乏症
        ["sugar_glider_0006", "sugar_glider_0088"],  # 低血糖症（+新生児）
        ["sugar_glider_0008", "sugar_glider_0080"],  # 鉄過剰症（肝臓型）
        ["sugar_glider_0019", "sugar_glider_0155"],  # ダニ感染症
        ["sugar_glider_0022", "sugar_glider_0097"],  # トキソプラズマ症（+急性）
        ["sugar_glider_0024", "sugar_glider_0219"],  # 肺炎（+細菌性）
        ["sugar_glider_0026", "sugar_glider_0147"],  # 下痢（非特異的）
        ["sugar_glider_0043", "sugar_glider_0073", "sugar_glider_0193"],  # 育児嚢感染症
        ["sugar_glider_0044", "sugar_glider_0166"],  # てんかん発作（MBD関連）
        ["sugar_glider_0051", "sugar_glider_0153"],  # 肝リピドーシス
        ["sugar_glider_0059", "sugar_glider_0071", "sugar_glider_0138"],  # 飛膜損傷
        ["sugar_glider_0061", "sugar_glider_0180"],  # 熱中症（+呼吸器型）
        ["sugar_glider_0069", "sugar_glider_0133"],  # 栄養性骨異栄養症（MBD）
        ["sugar_glider_0075", "sugar_glider_0170"],  # 難産（有袋類）
        ["sugar_glider_0038", "sugar_glider_0165"],  # 眼球突出 Proptosis（0188 Exophthalmos は分離維持）
    ],
    "hedgehog": [
        ["hedgehog_0002", "hedgehog_0093", "hedgehog_0149"],  # 皮膚糸状菌症（重症/Trichophyton）
        ["hedgehog_0015", "hedgehog_0121"],  # 肥満（+重度/病的）
        ["hedgehog_0016", "hedgehog_0174"],  # 下痢（非特異的）
        ["hedgehog_0017", "hedgehog_0143"],  # 消化管内異物
        ["hedgehog_0018", "hedgehog_0118"],  # 肝リピドーシス（肥満関連）
        ["hedgehog_0026", "hedgehog_0241"],  # 肺炎（+細菌性）
        ["hedgehog_0028", "hedgehog_0057"],  # マイコバクテリア症（肺型/播種型）
        ["hedgehog_0055", "hedgehog_0164"],  # 脂肪肝（非肥満型）
        ["hedgehog_0069", "hedgehog_0140"],  # バルーン症候群（皮下気腫）
        ["hedgehog_0090", "hedgehog_0150"],  # カパリニアダニ症
        ["hedgehog_0040", "hedgehog_0166"],  # 眼球突出 Proptosis（0218 Exophthalmos は分離維持）
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
    # A curated group's canonical (group[0]) may ALSO be an existing auto-merge
    # canonical (e.g. Ringworm 0002 already absorbed 0243): extend that cluster
    # rather than dropping the canonical and forming a stray second cluster.
    canon_index = {m["canonical"]["id"]: m for m in merges}  # canonical id -> merge dict
    merged_away = {mm["id"] for m in merges for mm in m["merged"]}
    for group in _CURATED_MERGE.get(species, []):
        # Members present in the data and not already merged away by another cluster.
        members = [rid for rid in group if rid in by_id and rid not in merged_away]
        if len(members) < 2:
            continue  # nothing left to merge → skip (idempotent)
        canonical_id = members[0]
        add = [rid for rid in members[1:] if rid != canonical_id]
        if not add:
            continue
        existing = canon_index.get(canonical_id)
        if existing is not None:
            # Extend the existing (auto or curated) cluster with the new members.
            have = {mm["id"] for mm in existing["merged"]}
            for rid in add:
                if rid in have:
                    continue
                existing["merged"].append(ident(rid))
                have.add(rid)
                merged_away.add(rid)
            existing["curated"] = True
        else:
            newm = {
                "canonical": ident(canonical_id),
                "merged": [ident(rid) for rid in add],
                "reason": "vet-approved same disease (curated; differs by an informative qualifier)",
                "inherit_content": True,
                "curated": True,
            }
            merges.append(newm)
            canon_index[canonical_id] = newm
            merged_away.update(add)
    # Drop review-oversplit entries whose members are now FULLY resolved by a
    # merge (keep entries that still contain an unmerged subtype).
    _resolved_ids = set(canon_index) | merged_away
    review_oversplit = [o for o in review_oversplit if not all(m["id"] in _resolved_ids for m in o.get("members", []))]

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
