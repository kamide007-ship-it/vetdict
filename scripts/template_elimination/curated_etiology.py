"""Curated causes_ja / pathophysiology_ja for diseases that resist single-category
templating.

Some diseases are multifactorial and do not map cleanly onto any one of the
``NAME_CATEGORY_PATTERNS`` buckets, so the category-recategorisation pass can only
swap one imperfect template for another. Equine **laminitis** (predominantly
endocrinopathic/inflammatory/mechanical, not orthopaedic) and **hepatic fibrosis**
(the fibrotic end-stage of chronic liver injury, with no dedicated hepatic
etiology bucket) are the two flagged in the previous session.

Rather than force them into a marginal category, this module supplies concise,
textbook-accurate, disease-specific etiology and pathophysiology. The text encodes
established veterinary knowledge (not per-record generation), so it carries no
fabrication risk; it is applied ONLY to fields that are currently a recognised
category template or vague stub, so genuinely curated content (e.g. the existing
disease-specific laminitis pathophysiology) is never overwritten.

References: Belknap & Geor, *Equine Laminitis* (2017); AAEP/ECEIM laminitis
consensus; Stashak, *Adams' Lameness in Horses* 6th ed; Carpenter, *Exotic Animal
Formulary* 6th ed; Harrison & Lightfoot, *Clinical Avian Medicine* (hepatic
disease); Cullen & Stalker, *Jubb, Kennedy & Palmer's Pathology of Domestic
Animals* (liver).
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.template_elimination.clinical_fields_generator import SPECIES_JA  # noqa: E402
from scripts.template_elimination.curated_common_diseases import COMMON_DISEASES  # noqa: E402

# A field is replaceable (safe to overwrite with curated text) when it is empty,
# carries a category template (detected by the caller via fingerprint), or is one
# of these vague generic stubs.
STUB_SIGNATURES: tuple[str, ...] = (
    "正確な病因は症例により異なる",
    "病因は症例により異なる",
)


def _laminitis_causes(species_ja: str) -> str:
    return (
        f"{species_ja}における蹄葉炎の原因は多くが全身性で、現在は内分泌性が最多とされる。"
        "(1) 内分泌性（インスリン調節異常）: 馬代謝症候群（EMS）や下垂体中葉機能不全（PPID/クッシング）に伴う"
        "高インスリン血症が葉層を傷害する（最も一般的）。"
        "(2) 炎症性・敗血症性（SIRS）: 穀物過食（炭水化物過負荷）、大腸炎、子宮内膜炎・胎盤停滞、"
        "重度感染症などの全身性炎症。"
        "(3) 過重負重性（supporting-limb）: 対側肢の重度疼痛・非負重による患肢への持続的荷重。"
        "(4) その他: 硬地での過度な運動（road founder）、コルチコステロイド誘発。"
        "肥満・過肥、ポニーや特定品種、過去の蹄葉炎既往が主要なリスク因子である。"
    )


def _laminitis_patho(species_ja: str) -> str:
    return (
        f"{species_ja}の蹄葉炎は、蹄骨と蹄壁をつなぐ葉状層（葉層）の機能不全により蹄骨の回転・沈下が生じる病態である。"
        "発症機序は原因により異なる: 内分泌性では高インスリン血症がIGF-1受容体等を介して葉層上皮を伸長・脆弱化させる。"
        "敗血症・炎症性では循環中のサイトカイン・エンドトキシンが葉層の微小循環障害（血管収縮・血栓・虚血再灌流）と"
        "基質メタロプロテアーゼ（MMP-2/9）の活性化を引き起こし、基底膜の酵素的分解を招く。"
        "過重負重性では持続的な機械的ストレスと灌流低下が関与する。"
        "葉層結合の破綻により蹄骨が深指屈腱の牽引と体重で回転・沈下し、重症例では蹄底穿孔に至る。"
        "急性期は強い疼痛と拍動性の指動脈拍動、慢性期は蹄輪の乖離（founder lines）・白帯の開大・蹄骨変位を呈する。"
    )


def _hepatic_fibrosis_causes(species_ja: str) -> str:
    return (
        f"{species_ja}における肝線維症は、慢性的な肝傷害が持続した結果として肝実質が線維性結合組織へ置換される終末像であり、"
        "原因は基礎となる慢性肝疾患に依存する。"
        "慢性胆管肝炎・胆管閉塞（胆汁うっ滞）、栄養性（肝リピドーシス関連、ビタミン・ミネラル不均衡、肥満や高脂肪の種子食）、"
        "毒性（アフラトキシン等のカビ毒、重金属、薬剤性、植物毒）、感染性（細菌・ウイルス・寄生虫による慢性肝炎）、"
        "鉄過剰症（一部の鳥類・果実食種でのヘモクロマトーシス）、慢性うっ血（右心不全）が主な誘因である。"
        "多くは長期にわたる不適切な飼育・栄養管理を背景とする。"
    )


def _hepatic_fibrosis_patho(species_ja: str) -> str:
    return (
        f"{species_ja}の肝線維症は、持続的な肝細胞傷害に対する創傷治癒反応の結果として進行する。"
        "傷害により活性化された肝星細胞（伊東細胞）が筋線維芽細胞へ形質転換し、"
        "I型・III型コラーゲンなどの細胞外基質を過剰に産生・沈着させる。"
        "基質の産生と分解の均衡が崩れることで類洞周囲から門脈域に線維性隔壁が形成され、肝小葉構造が改変される。"
        "進行すると肝内血流抵抗の上昇（門脈圧亢進）と肝細胞機能の低下（低アルブミン血症・凝固異常・胆汁うっ滞・高アンモニア血症）を招き、"
        "不可逆的な肝硬変・肝不全へ至る。早期は無症状だが、食欲不振・体重減少・黄疸・腹水・出血傾向として顕在化する。"
    )


# (species_set_or_None, name_substrings, {field: generator})
_CURATED: tuple[tuple[frozenset | None, tuple[str, ...], dict], ...] = (
    (
        frozenset({"horse"}),
        ("蹄葉炎", "Laminitis"),
        {"causes_ja": _laminitis_causes, "pathophysiology_ja": _laminitis_patho},
    ),
    (
        None,
        ("肝線維症", "肝繊維症", "Hepatic Fibrosis"),
        {"causes_ja": _hepatic_fibrosis_causes, "pathophysiology_ja": _hepatic_fibrosis_patho},
    ),
)


def curated_etiology(species: str, name_ja: str, name_en: str) -> dict | None:
    """Return {field: curated_text} for a curated disease, or None.

    The caller decides per-field whether the existing value is replaceable (a
    template / stub / empty); this function only supplies the correct text.
    """
    species = (species or "").lower()
    name = f"{name_ja or ''} {name_en or ''}"
    species_ja = SPECIES_JA.get(species, species)

    # Static, disease-specific curated text for high-traffic conditions. Checked
    # first; name_exclusions guard against substring collisions (e.g.
    # 甲状腺機能低下 ⊂ 副甲状腺機能低下症).
    for species_set, name_subs, name_excl, fields in COMMON_DISEASES:
        if species not in species_set:
            continue
        if not any(sub in name for sub in name_subs):
            continue
        if any(bad in name for bad in name_excl):
            continue
        return dict(fields)

    for species_set, name_subs, fields in _CURATED:
        if species_set is not None and species not in species_set:
            continue
        if not any(sub in name for sub in name_subs):
            continue
        return {field: gen(species_ja) for field, gen in fields.items()}
    return None
