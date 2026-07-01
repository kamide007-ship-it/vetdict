"""Curated etiology / pathophysiology for named-nutrient (deficiency/excess) diseases.

Fifth companion to the pathogen libraries. Nutritional diseases whose name names
the nutrient (vitamin-A deficiency, hypocalcaemia/NSHP, rickets, scurvy, taurine
deficiency, goitre …) shipped the generic nutritional category template — JA
「…栄養バランスの是正が中心…」/「…の原因は栄養素の欠乏または過剰である…」 and English
"Caused by dietary deficiency or excess…", "Nutritional imbalance…", "Nutritional
diseases result from…". The name deterministically implies the aetiology (a
deficiency of, or excess of, the named nutrient), so it is curated with zero
fabrication risk — the nutritional analogue of the named-pathogen batches.

Generators return nutrient-specific ``causes`` + ``pathophysiology`` (JA + EN),
species-aware where the biology differs (guinea pigs cannot synthesise vitamin C;
cats are obligate taurine-dependent; reptiles/birds develop NSHP/MBD).

References: NRC Nutrient Requirements; Hand et al., *Small Animal Clinical
Nutrition* 5th ed; Carpenter, *Exotic Animal Formulary* 6th ed.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from scripts.template_elimination.clinical_fields_generator import (  # noqa: E402
    SPECIES_EN,
    SPECIES_JA,
    _neutralise_negations,
)


def _ja(sp: str) -> str:
    return SPECIES_JA.get(sp, sp)


def _en(sp: str) -> str:
    return SPECIES_EN.get(sp, sp)


def _calcium(sp):
    j, e = _ja(sp), _en(sp)
    cja = f"{j}の栄養性二次性上皮小体機能亢進症（代謝性骨疾患・低カルシウム血症）は、Ca不足・過剰なリン・ビタミンD不足（爬虫類ではUV-B不足）を招く不適切な食事による。"
    cen = f"Caused in {e} by a diet low in calcium, high in phosphorus and/or deficient in vitamin D (with inadequate UV-B in reptiles), producing nutritional secondary hyperparathyroidism / metabolic bone disease."
    pja = "低血中Caを代償する上皮小体ホルモン(PTH)の持続分泌が骨からCaを動員し、線維性骨異栄養症・骨密度低下・病的骨折・成長異常を起こす。急性の低Ca血症では筋振戦・テタニー・痙攣を生じる。"
    pen = "Sustained parathyroid-hormone secretion to correct hypocalcaemia mobilises calcium from bone, causing fibrous osteodystrophy, low bone density, pathological fractures and growth deformity; acute hypocalcaemia causes tremors, tetany and seizures."
    return cja, cen, pja, pen


def _vitamin_a(sp):
    j, e = _ja(sp), _en(sp)
    cja = f"{j}のビタミンA欠乏症は、レチノール/前駆体（β-カロテン）の乏しい不適切な食餌（種子食・不適切な配合）による。過剰症は肝・サプリの過給による。"
    cen = f"Caused in {e} by a diet deficient in retinol/pro-vitamin-A (all-seed or unbalanced diets); the excess form results from over-supplementation or liver-rich diets."
    pja = "ビタミンAは上皮の正常な分化に必須で、欠乏により扁平上皮化生が起こる。呼吸器・消化器・腎・生殖器上皮や涙腺・ハーダー腺が角化し、眼病変・鼻口腔の膿瘍・二次感染・繁殖障害を招く。"
    pen = "Vitamin A is essential for normal epithelial differentiation; deficiency causes squamous metaplasia of respiratory, GI, renal, reproductive and glandular epithelium, leading to ocular lesions, oral/nasal abscessation, secondary infection and reproductive failure."
    return cja, cen, pja, pen


def _vitamin_d(sp):
    j, e = _ja(sp), _en(sp)
    cja = f"{j}のビタミンD欠乏症（くる病・骨軟化症）は、食餌性ビタミンD不足やCa/P不均衡、日光/UV-B曝露の不足による。過剰症は殺鼠剤・サプリ過剰による高Ca血症を起こす。"
    cen = f"Caused in {e} by deficient dietary vitamin D, calcium/phosphorus imbalance and inadequate sunlight/UV-B exposure (rickets/osteomalacia); the excess form (rodenticide, over-supplementation) causes hypercalcaemia."
    pja = "ビタミンDは腸管からのCa・P吸収に必須で、欠乏すると骨基質の石灰化が障害される。成長板・類骨の石灰化不全により骨の変形・脆弱化（くる病/骨軟化症）を、過剰では軟部組織の石灰化・腎障害を起こす。"
    pen = "Vitamin D is essential for intestinal calcium/phosphorus absorption; deficiency impairs mineralisation of bone matrix, causing failure of growth-plate/osteoid mineralisation with skeletal deformity and fragility (rickets/osteomalacia), while excess causes soft-tissue mineralisation and renal injury."
    return cja, cen, pja, pen


def _vitamin_e_se(sp):
    j, e = _ja(sp), _en(sp)
    cja = f"{j}のビタミンE/セレン欠乏症（白筋症・栄養性筋変性）は、抗酸化に働くビタミンE・セレンの乏しい食餌（古い/酸化した飼料・不適切な配合）による。"
    cen = f"Caused in {e} by a diet deficient in the antioxidants vitamin E and selenium (stale/oxidised or unbalanced feed), producing nutritional muscular dystrophy (white muscle disease)."
    pja = "ビタミンE・セレンは細胞膜を酸化傷害から守る。欠乏により骨格筋・心筋の細胞膜が過酸化障害を受け、変性・壊死（白色化）を起こして起立不能・虚弱・心不全・嚥下障害を生じる。"
    pen = "Vitamin E and selenium protect cell membranes from oxidative injury; deficiency lets peroxidative damage degenerate and necrose skeletal and cardiac muscle (pale 'white' muscle), causing weakness, recumbency, heart failure and dysphagia."
    return cja, cen, pja, pen


def _vitamin_c(sp):
    j, e = _ja(sp), _en(sp)
    cja = f"{j}の壊血病（ビタミンC欠乏症）は、L-グロノラクトン酸化酵素を欠きビタミンCを体内合成できない種で、食餌性ビタミンCの不足（無添加・劣化ペレット）により発症する。"
    cen = f"Caused in {e} — a species unable to synthesise vitamin C (lacking L-gulonolactone oxidase) — by inadequate dietary vitamin C (unsupplemented or degraded pellets), producing scurvy."
    pja = "ビタミンCはコラーゲン合成に必須で、欠乏するとコラーゲン・結合組織・血管壁・骨基質・象牙質の形成が障害される。出血傾向・関節腫脹と疼痛による跛行・創傷治癒遅延・歯や骨の異常・易感染性を生じる。"
    pen = "Vitamin C is essential for collagen synthesis; deficiency impairs formation of collagen, connective tissue, vessel walls, bone matrix and dentine, causing a bleeding tendency, painful swollen joints with lameness, delayed wound healing, dental/skeletal abnormalities and susceptibility to infection."
    return cja, cen, pja, pen


def _vitamin_b(sp):
    j, e = _ja(sp), _en(sp)
    cja = f"{j}のビタミンB群欠乏症は、水溶性B群（B12/コバラミン・葉酸・ナイアシン・ビオチン等）の摂取不足、吸収不良、または腸内細菌叢の乱れによる。"
    cen = f"Caused in {e} by inadequate intake, malabsorption or dysbiosis affecting the water-soluble B vitamins (B12/cobalamin, folate, niacin, biotin)."
    pja = "B群は多くの代謝酵素の補酵素で、欠乏によりエネルギー・アミノ酸・造血・神経機能が障害される。食欲不振・体重減少・貧血・皮膚被毛異常・末梢神経障害・成長不良を生じる。"
    pen = "B vitamins are coenzymes for many metabolic enzymes; deficiency impairs energy, amino-acid, haematopoietic and neurological function, causing anorexia, weight loss, anaemia, skin/coat changes, peripheral neuropathy and poor growth."
    return cja, cen, pja, pen


def _thiamine(sp):
    j, e = _ja(sp), _en(sp)
    cja = f"{j}のチアミン（ビタミンB1）欠乏症は、チアミナーゼを含む生魚・ワラビの給与、加熱/亜硫酸処理による破壊、または反芻動物での産生障害による。"
    cen = f"Caused in {e} by diets containing thiaminase (raw fish, bracken fern), destruction by heat/sulphite, or impaired ruminal synthesis (polioencephalomalacia)."
    pja = "チアミンは糖代謝（ピルビン酸・α-ケトグルタル酸脱水素酵素）の補酵素で、欠乏によりエネルギー代謝の高い神経組織が選択的に障害される。中枢神経症状（発作・散瞳・斜頸・運動失調・後弓反張）を生じる。"
    pen = "Thiamine is a coenzyme of carbohydrate metabolism (pyruvate and α-ketoglutarate dehydrogenase); deficiency selectively injures the energy-dependent nervous system, causing neurological signs (seizures, mydriasis, head tilt, ataxia, opisthotonos)."
    return cja, cen, pja, pen


def _iodine(sp):
    j, e = _ja(sp), _en(sp)
    cja = f"{j}の甲状腺腫（ヨウ素欠乏症）は、ヨウ素の乏しい食餌やゴイトロゲン（キャベツ類・大豆等）の過剰摂取による甲状腺ホルモン合成障害による。"
    cen = f"Caused in {e} by iodine-deficient diets or excess goitrogens (brassicas, soy) impairing thyroid-hormone synthesis (goitre)."
    pja = "ヨウ素不足で甲状腺ホルモン合成が低下すると、下垂体からのTSH分泌が代償的に亢進して甲状腺が過形成・腫大（甲状腺腫）する。甲状腺機能低下により成長遅延・低体温・元気消失・被毛/羽毛不良を生じる。"
    pen = "When iodine deficiency lowers thyroid-hormone synthesis, compensatory pituitary TSH drives thyroid hyperplasia and enlargement (goitre); the resulting hypothyroid state causes stunting, hypothermia, lethargy and poor coat/plumage."
    return cja, cen, pja, pen


def _zinc(sp):
    j, e = _ja(sp), _en(sp)
    cja = f"{j}の亜鉛欠乏症は、亜鉛の乏しい食餌、フィチン酸/過剰なCaによる吸収阻害、または遺伝的な亜鉛吸収障害（特定犬種）による。"
    cen = f"Caused in {e} by zinc-deficient diets, impaired absorption from phytate/excess calcium, or a breed-related genetic zinc-absorption defect."
    pja = "亜鉛は多くの酵素・上皮の分化・免疫に必須で、欠乏により角化異常（口周・関節・肉球の痂皮性皮膚炎）・創傷治癒遅延・免疫低下・成長不良を生じる。"
    pen = "Zinc is essential for numerous enzymes, epithelial differentiation and immunity; deficiency causes parakeratotic, crusting dermatitis (muzzle, joints, footpads), delayed wound healing, immunosuppression and poor growth."
    return cja, cen, pja, pen


def _protein_energy(sp):
    j, e = _ja(sp), _en(sp)
    cja = f"{j}の蛋白・エネルギー栄養失調は、摂取量の絶対的不足（飢餓・給餌不良）や吸収不良・慢性消耗性疾患による需要増大とのアンバランスによる。"
    cen = f"Caused in {e} by an absolute shortfall of intake (starvation, poor husbandry) or by malabsorption/increased demand from chronic wasting disease outstripping supply."
    pja = "エネルギー・蛋白の不足で体は筋・脂肪を異化してエネルギーを得るため、進行性の削痩・筋萎縮・低アルブミン血症・免疫低下・低体温を生じる。重度・急速な再給餌では再栄養症候群のリスクがある。"
    pen = "With insufficient energy and protein the body catabolises muscle and fat, producing progressive wasting, muscle atrophy, hypoalbuminaemia, immunosuppression and hypothermia; rapid refeeding risks refeeding syndrome."
    return cja, cen, pja, pen


def _obesity(sp):
    j, e = _ja(sp), _en(sp)
    cja = f"{j}の肥満は、摂取エネルギーが消費エネルギーを慢性的に上回ることによる。過給餌・高カロリー食・運動不足・不妊手術後の代謝変化が主因となる。"
    cen = f"Caused in {e} by chronic energy intake exceeding expenditure — overfeeding, calorie-dense diets, inactivity and post-neuter metabolic change are the main drivers."
    pja = "過剰なエネルギーが脂肪組織に蓄積し、脂肪組織由来の炎症性アディポカインを介してインスリン抵抗性・全身性の軽度炎症を招く。関節・心肺への負荷、糖尿病・肝リピドーシス・尿路疾患のリスクを高める。"
    pen = "Surplus energy is stored as adipose tissue, whose inflammatory adipokines drive insulin resistance and low-grade systemic inflammation; the excess load strains joints and the cardiorespiratory system and raises the risk of diabetes, hepatic lipidosis and urinary disease."
    return cja, cen, pja, pen


def _taurine(sp):
    cja = "猫のタウリン欠乏症は、タウリンを合成できずアミノ酸として食事に必須とする猫で、タウリンの乏しい食餌（不適切な手作り食・犬用フード）により発症する。"
    cen = "Caused in cats — an obligate taurine-dependent species unable to synthesise it adequately — by taurine-deficient diets (unbalanced home-cooked food or dog food)."
    pja = "タウリンは心筋の収縮と網膜光受容体・胆汁酸抱合に必須で、欠乏により拡張型心筋症（可逆性）・中心性網膜変性（失明）・繁殖/発育障害を生じる。"
    pen = "Taurine is essential for myocardial contractility, retinal photoreceptors and bile-acid conjugation; deficiency causes (reversible) dilated cardiomyopathy, central retinal degeneration (blindness) and reproductive/developmental failure."
    return cja, cen, pja, pen


# name-pattern -> generator. Collision-safe keys (see comments).
_AGENTS: tuple[tuple[tuple[str, ...], object], ...] = (
    # Calcium / NSHP / metabolic bone disease.
    # Nutritional hyperparathyroidism only — NOT primary (parathyroid tumour) or
    # renal secondary HPT, which are excluded below.
    (
        (
            "栄養性二次性",
            "栄養性上皮小体",
            "nutritional secondary hyperparathyroid",
            "nutritional hyperparathyroid",
            "nshp",
            "metabolic bone",
            "代謝性骨疾患",
            "低カルシウム",
            "hypocalc",
            "milk fever",
            "eclampsia",
            "子癇",
        ),
        _calcium,
    ),
    (("ビタミンa", "vitamin a", "hypovitaminosis a", "retinol", "レチノール"), _vitamin_a),
    # Vitamin D / rickets — never bare "goiter" etc. here.
    (("ビタミンd", "vitamin d", "rickets", "くる病", "骨軟化", "osteomalacia"), _vitamin_d),
    (("ビタミンe", "vitamin e", "セレン", "selenium", "white muscle", "白筋", "栄養性筋"), _vitamin_e_se),
    (("壊血病", "scurvy", "ビタミンc", "vitamin c", "ascorb"), _vitamin_c),
    (("チアミン", "thiamin", "ビタミンb1", "vitamin b1", "polioencephalomalacia"), _thiamine),
    (
        (
            "ビタミンb",
            "vitamin b",
            "コバラミン",
            "cobalamin",
            "b12",
            "葉酸",
            "folate",
            "niacin",
            "biotin",
            "riboflavin",
            "ペラグラ",
            "pellagra",
        ),
        _vitamin_b,
    ),
    # Iodine / goitre — "甲状腺腫"/"goiter" (a hyperplasia), not thyroid neoplasia.
    (("ヨウ素", "iodine", "甲状腺腫", "goiter", "goitre"), _iodine),
    (("亜鉛", "zinc"), _zinc),
    (("タウリン", "taurine"), _taurine),
    # "肥満" but not "肥満細胞腫" (mast cell tumour); "obesity" is safe.
    (("obesity", "肥満症"), _obesity),
    (
        (
            "蛋白エネルギー",
            "蛋白・エネルギー",
            "protein-energy",
            "protein energy",
            "malnutrition",
            "栄養失調",
            "starvation",
            "飢餓",
            "cachexia",
            "悪液質",
        ),
        _protein_energy,
    ),
)

# Exclusions: names that contain a key substring but are a different disease.
# Toxicoses (中毒/toxicosis) are poisonings handled by toxicology_library — a
# zinc/vitamin-D toxicosis must NOT be described as a dietary *deficiency*.
_EXCLUSIONS = (
    "肥満細胞",
    "mast cell",
    "甲状腺腫瘍",
    "甲状腺癌",
    "thyroid carcinoma",
    "副甲状腺",
    "中毒",
    "toxicosis",
    "toxicity",
    "poisoning",
    "hardware disease",
    "原発性上皮小体",
    "腎性",
    "primary hyperparathyroid",
    "renal secondary hyperparathyroid",
)


def resolve_nutrient_agent(name_ja: str, name_en: str):
    """Return the generator for a named-nutrient disease, or None."""
    name = _neutralise_negations(f"{name_ja or ''} {name_en or ''}").lower()
    if any(x.lower() in name for x in _EXCLUSIONS):
        return None
    for keys, gen in _AGENTS:
        if any(k.lower() in name for k in keys):
            return gen
    return None


def nutrient_clinical_fields(species: str, name_ja: str, name_en: str) -> dict | None:
    """Curated causes / pathophysiology (JA+EN) for a named-nutrient disease, or
    None when the name does not resolve to a known nutrient."""
    gen = resolve_nutrient_agent(name_ja, name_en)
    if gen is None:
        return None
    # Taurine deficiency is feline-specific; do not stamp feline prose elsewhere.
    if gen is _taurine and (species or "").lower() != "cat":
        return None
    cja, cen, pja, pen = gen((species or "").lower())
    return {
        "causes_ja": cja,
        "causes": cen,
        "pathophysiology_ja": pja,
        "pathophysiology": pen,
    }
