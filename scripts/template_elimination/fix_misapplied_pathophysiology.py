#!/usr/bin/env python3
"""Fix misapplied generic pathophysiology_ja templates across species.

Background
----------
``enrich_diseases()`` (api/species/helpers.py) overlays ``pathophysiology_ja``
from ``diseases_all_species.json`` onto each species module's ``DISEASES`` list.
The JSON overlay contains *category-level* boilerplate (e.g. a generic
"chemical toxicant" paragraph, a generic "fungal infection" paragraph) that was
bulk-applied to the wrong disease class — for example:

  * Feline Botulism / Tetanus / clostridial enteritis (BACTERIAL toxin diseases)
    received the chemical-toxicant template ("毒性物質は細胞レベルで…").
  * Feline Dermatophilosis, avian Air Sacculitis (BACTERIAL) received the
    fungal-infection template ("真菌感染の病態生理…").
  * Avian Influenza, Bornavirus/PDD, Gumboro (VIRAL) received toxicant /
    neoplasia templates.
  * Coccidiosis, mite infestations (PARASITIC) received the toxicant template.

Because ``_is_template_text()`` does not recognise these category paragraphs as
templates, the misapplied JSON text "wins" over the module text and is served on
the live site — a factual error analogous to the horse Anaphylaxis bug.

This script replaces those misapplied entries with concise, pathogen-specific,
clinically accurate pathophysiology, writing to BOTH the JSON overlay (the
served source) and the canonical Python module (for consistency).

Idempotent: re-running only rewrites entries that still match a misapplied
template signature.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
JSON_PATH = ROOT / "diseases_all_species.json"
SPECIES_DIR = ROOT / "api" / "species"

# Category templates keyed by the disease *class* they describe, with a
# signature substring. A template is "misapplied" when its class is
# incompatible with the disease's true class (inferred from name/description).
TEMPLATE_CLASS_SIGS = {
    "toxicant": "毒性物質は細胞レベルで",
    "fungal": "真菌感染の病態生理",
    "neoplasia": "腫瘍の病態生理は正常細胞の悪性転換",
    "bacterial_colonisation": "細菌感染症である。病原菌は付着因子",
    "autoimmune": "免疫介在性疾患である。免疫系が自己抗原",
}

# Keywords that reveal a disease's TRUE class.
NAME_HINTS = {
    "bacterial": [
        "菌",
        "bacteri",
        "sepsis",
        "敗血",
        "pneumonia",
        "肺炎",
        "tetanus",
        "破傷風",
        "botulism",
        "ボツリヌス",
        "bordetella",
        "actinomyc",
        "放線菌",
        "clostrid",
        "salmonella",
        "e. coli",
        "大腸菌",
        "leptospir",
        "lyme",
        "brucell",
        "mycoplasma",
        "chlamyd",
        "クラミジア",
        "dermatophilosis",
        "erysipel",
        "pseudomonas",
        "緑膿菌",
        "strepto",
        "レンサ球菌",
        "staphylo",
        "pasteurell",
        "enterotox",
        "dysbiosis",
        "enteritis",
        "abscess",
        "膿瘍",
        "rhinitis",
        "sacculitis",
        "気嚢炎",
    ],
    "fungal": [
        "真菌",
        "fungal",
        "mycosis",
        "mycetoma",
        "aspergill",
        "candid",
        "カンジダ",
        "crypto",
        "histoplasm",
        "dermatophyt",
        "皮膚糸状菌",
        "blastomyc",
        "sporotrich",
        "malassezia",
        "ringworm",
        "白癬",
        "yeast",
        "酵母",
        "canv",
        "ophidiomyces",
    ],
    "viral": [
        "ウイルス",
        "virus",
        "viral",
        "herpes",
        "calici",
        "parvo",
        "distemper",
        "rabies",
        "狂犬",
        "influenza",
        "felv",
        "fip",
        "papilloma",
        "reovirus",
        "bornavirus",
        "birnavirus",
        "ビルナ",
        "poxvirus",
        "ポックス",
        "adenovirus",
        "iridovirus",
        "proventricular dilatation",
        "pdd",
    ],
    "parasitic": [
        "寄生虫",
        "parasit",
        "mite",
        "ダニ",
        "worm",
        "線虫",
        "coccidi",
        "コクシジウム",
        "アイメリア",
        "eimeria",
        "giardia",
        "flea",
        "ノミ",
        "heartworm",
        "フィラリア",
        "toxoplasma",
        "mange",
        "疥癬",
        "pinworm",
        "cheyletiella",
        "demodex",
        "hexamit",
    ],
}

# A template-class is incompatible with these true-classes.
INCOMPAT = {
    "toxicant": {"bacterial", "viral", "fungal", "parasitic"},
    "fungal": {"bacterial", "viral", "parasitic"},
    "neoplasia": {"bacterial", "viral", "fungal", "parasitic"},
    "bacterial_colonisation": {"viral", "fungal", "parasitic"},
    "autoimmune": {"bacterial", "viral", "fungal", "parasitic"},
}


def _true_classes(name: str, desc: str) -> set:
    blob = (name + " " + desc).lower()
    classes = {cls for cls, kws in NAME_HINTS.items() if any(k.lower() in blob for k in kws)}
    # Guard against "菌" false-positives for bacterial when the real class is fungal
    # ("真菌" contains "菌") or aseptic ("無菌" contains "菌").
    if "bacterial" in classes:
        has_fungal_context = "真菌" in blob or "fungal" in blob or "mycosis" in blob
        has_aseptic_context = "無菌" in blob
        if has_fungal_context or has_aseptic_context:
            strong = [k for k in NAME_HINTS["bacterial"] if k != "菌" and k.lower() in blob]
            if not strong:
                classes.discard("bacterial")
    return classes


def _template_class(text: str) -> str | None:
    for cls, sig in TEMPLATE_CLASS_SIGS.items():
        if sig in text:
            return cls
    return None


def is_misapplied(text: str, name: str, desc: str) -> bool:
    """True only when the template's class conflicts with the disease's class."""
    if not text:
        return False
    tcls = _template_class(text)
    if tcls is None:
        return False
    # The "bacterial" hint also fires for bacterial_colonisation (compatible).
    bench = "bacterial" if tcls == "bacterial_colonisation" else tcls
    truth = _true_classes(name, desc)
    if bench in truth:
        return False  # template class matches disease class -> correctly applied
    return bool(truth & INCOMPAT[tcls])


# --- Pathogen-specific generators -------------------------------------------
# Each returns clinically accurate JA pathophysiology. ``ja`` is the disease's
# Japanese name, woven in so the output is unique per disease (not copy-paste).


def g_botulism(ja: str) -> str:
    return (
        f"{ja}は Clostridium botulinum が産生する神経毒素（主にC型）の経口摂取により発症する。"
        "毒素は腸管から吸収後、運動神経終末の前シナプス膜に不可逆的に結合し、"
        "シナプス小胞のアセチルコリン放出を阻害する。"
        "その結果、神経筋接合部の伝達が遮断され、対称性・下行性の弛緩性麻痺が進行する。"
        "重症例では呼吸筋麻痺により致死的となる。創傷型では局所で増殖した菌が毒素を産生する。"
    )


def g_tetanus(ja: str) -> str:
    return (
        f"{ja}は Clostridium tetani が創傷の嫌気的環境で増殖し産生するテタノスパスミンによる。"
        "毒素は運動神経軸索を逆行性に輸送され中枢神経に到達し、"
        "抑制性介在ニューロンからのグリシン・GABA放出を遮断する。"
        "抑制系の喪失により運動ニューロンが過剰興奮し、持続的な筋強直、開口障害、"
        "強直性痙攣（破傷風様痙攣）を呈する。自律神経障害を伴うこともある。"
    )


def g_clostridial_enteric(ja: str) -> str:
    return (
        f"{ja}は抗菌薬投与や急激な食事変化による腸内細菌叢の撹乱を契機に、"
        "Clostridium 属菌（C. perfringens、C. difficile、C. spiroforme 等）が異常増殖し、"
        "外毒素（toxin A/B、α・ι・ε毒素など）を産生することで発症する。"
        "毒素は腸上皮細胞を傷害して粘膜壊死・透過性亢進・体液漏出を引き起こし、"
        "重度の下痢・腸毒素血症・毒素性ショックへ進展する。草食小動物では特に急速に致死的となる。"
    )


def g_erysipelas(ja: str) -> str:
    return (
        f"{ja}は Erysipelothrix rhusiopathiae の経皮・経口侵入により発症する。"
        "菌は血流に侵入して菌血症を起こし、血管内皮への接着と局所血栓形成を介して"
        "全身性血管障害を引き起こす。急性例では敗血症・突然死、亜急性例では特徴的な菱形（ダイヤ型）"
        "皮膚病変、慢性例では多発性関節炎や疣贅性心内膜炎を呈する。人獣共通感染症である。"
    )


def g_pasteurella(ja: str) -> str:
    return (
        f"{ja}は Pasteurella multocida の感染による。"
        "菌は莢膜により食細胞による貪食を回避し、粘膜上皮に付着・定着する。"
        "急性経過では菌血症から敗血症・突然死に至り、内毒素（LPS）が全身性炎症反応を増悪させる。"
        "慢性経過では鼻炎・肺炎・膿瘍・関節炎など局所の化膿性炎症を形成する。"
    )


def g_ecoli_septic(ja: str) -> str:
    return (
        f"{ja}は病原性大腸菌（avian pathogenic E. coli 等）の全身感染による。"
        "上気道や腸管から侵入した菌が血流に達して菌血症を起こし、"
        "内毒素（LPS）が補体・凝固系・サイトカインカスケードを活性化して全身性炎症反応を惹起する。"
        "線維素性の多発性漿膜炎（気嚢炎・肝周囲炎・心膜炎）を特徴とし、進行すると敗血症性ショックに至る。"
    )


def g_strepto(ja: str) -> str:
    return (
        f"{ja}は Streptococcus 属菌の感染による。"
        "菌は溶血毒素や莢膜などの病原因子により組織に侵入・定着し、"
        "血流に達すると菌血症・敗血症を引き起こす。"
        "局所では呼吸器感染や化膿性関節炎を形成し、宿主の炎症反応が組織障害を増悪させる。"
    )


def g_pseudomonas(ja: str) -> str:
    return (
        f"{ja}は Pseudomonas aeruginosa による日和見感染である。"
        "免疫抑制や衛生不良を背景に、菌はバイオフィルムを形成して定着し、"
        "外毒素A・エラスターゼ・プロテアーゼなどの病原因子により組織を破壊する。"
        "湿潤環境で増殖しやすく、呼吸器・皮膚・全身性の壊死性炎症や敗血症を引き起こす。"
    )


def g_bordetella_resp(ja: str) -> str:
    return (
        f"{ja}は Bordetella bronchiseptica の感染による下気道疾患である。"
        "菌は線毛を持つ気道上皮に特異的に付着し、線毛運動を停止（ciliostasis）させて"
        "粘液線毛クリアランスを障害する。気管気管支炎・気管支肺炎を引き起こし、"
        "幼若個体や免疫低下個体では二次感染を伴って重症化する。"
    )


def g_atrophic_rhinitis(ja: str) -> str:
    return (
        f"{ja}は Bordetella bronchiseptica や毒素産生性 Pasteurella multocida の感染による。"
        "細菌の皮膚壊死毒素（dermonecrotic toxin）が鼻甲介の骨芽細胞を傷害して骨形成を抑制し、"
        "鼻甲介の進行性萎縮を引き起こす。重症例では顔面骨の変形・吻部の偏位を呈する。"
    )


def g_dermatophilosis(ja: str) -> str:
    return (
        f"{ja}は Dermatophilus congolensis（放線菌類の細菌）による滲出性皮膚炎である。"
        "持続的な湿潤や皮膚バリアの破綻を契機に、運動性の遊走子が表皮に侵入して菌糸状に増殖する。"
        "好中球浸潤を伴う表皮の炎症と滲出が生じ、特徴的な痂皮（かさぶた）形成と"
        "毛束の固着（paintbrush lesion）を呈する。"
    )


def g_hepatic_abscess(ja: str) -> str:
    return (
        f"{ja}は細菌が肝実質に播種して形成される化膿性膿瘍である。"
        "胆道系の上行性感染、門脈・動脈を介する血行性散布、あるいは隣接臓器からの直接波及により"
        "肝内に細菌が定着する。好中球浸潤と組織壊死により被包化された膿瘍を形成し、"
        "肝機能障害・全身性炎症・敗血症を引き起こす。"
    )


def g_bacterial_skin(ja: str) -> str:
    return (
        f"{ja}は皮膚バリアの破綻部から細菌が侵入して生じる化膿性皮膚炎である。"
        "外傷・湿潤・不衛生な環境を背景に細菌が表皮・真皮で増殖し、"
        "好中球浸潤を伴う炎症・滲出・悪臭性病変を形成する。"
        "進行すると蜂窩織炎や菌血症など全身性疾患へ波及しうる。"
    )


def g_macrorhabdosis(ja: str) -> str:
    return (
        f"{ja}は子嚢菌系酵母 Macrorhabdus ornithogaster（旧称メガバクテリア）の感染による。"
        "病原体は前胃（腺胃）と筋胃の移行部の粘膜表面に定着し、胃酸分泌を障害して胃内pHを上昇させる。"
        "粘膜の炎症・潰瘍により消化不良・体重減少・未消化便を呈し、"
        "慢性経過で削痩が進行する。"
    )


def g_avian_influenza(ja: str) -> str:
    return (
        f"{ja}はA型インフルエンザウイルス感染による。"
        "ウイルスはヘマグルチニン（HA）を介して気道・消化管上皮のシアル酸受容体に結合し侵入・複製する。"
        "低病原性株は局所の呼吸器・消化器感染にとどまるが、"
        "高病原性株はHA開裂部位の多塩基性配列により全身の細胞で複製可能となり、"
        "血管内皮障害・多臓器壊死を伴う全身性致死的感染を引き起こす。"
    )


def g_reovirus(ja: str) -> str:
    return (
        f"{ja}は鳥レオウイルスの感染による。"
        "ウイルスは消化管から侵入後、関節滑膜・腱鞘で複製して関節炎・腱鞘炎を引き起こし、"
        "腱断裂に至ることもある。リンパ系組織でも複製して免疫抑制を誘導し、"
        "二次感染やワクチン反応性の低下をもたらす。"
    )


def g_gumboro(ja: str) -> str:
    return (
        f"{ja}は鳥ビルナウイルス（IBDV）の感染による。"
        "ウイルスはファブリキウス嚢に親和性を持ち、嚢内の未熟B細胞前駆体を選択的に破壊する。"
        "その結果、液性免疫が著しく障害され、持続的な免疫抑制を引き起こす。"
        "若齢鳥ほど感受性が高く、各種感染症やワクチン不応の素因となる。"
    )


def g_shope_fibroma(ja: str) -> str:
    return (
        f"{ja}はポックスウイルス（Shope線維腫ウイルス）の感染による。"
        "ウイルスは表皮細胞と線維芽細胞で複製し、局所の細胞増殖を促して皮膚に良性の線維腫を形成する。"
        "病変は主に四肢・顔面に発生し、免疫正常個体では自然退縮することが多い。"
        "媒介節足動物（蚊・ノミ）により伝播する。"
    )


def g_bornavirus_pdd(ja: str) -> str:
    return (
        f"{ja}は鳥ボルナウイルス（ABV）感染による。"
        "ウイルスは消化管および中枢・末梢神経系の神経節に親和性を持ち、"
        "リンパ形質細胞性の神経節炎（特に前胃・筋胃の自律神経叢）を引き起こす。"
        "腸管平滑筋の運動障害により前胃拡張・消化管うっ滞・削痩を生じ、"
        "中枢神経の病変では運動失調・振戦・痙攣など進行性の神経症状を呈する。"
    )


def g_pdd_nonviral(ja: str) -> str:
    return (
        f"{ja}は鳥ボルナウイルス以外の原因による前胃拡張である。"
        "重金属（鉛・亜鉛）中毒、異物による物理的閉塞、平滑筋の機能障害、"
        "腫瘍や慢性炎症などが前胃の運動低下・拡張を引き起こす。"
        "原因により病態は異なるが、共通して消化管通過障害・うっ滞・栄養吸収不全を生じる。"
    )


def g_iridovirus(ja: str) -> str:
    return (
        f"{ja}はラナウイルス以外のイリドウイルスの感染による全身性疾患である。"
        "ウイルスは血管内皮・造血組織・実質臓器の細胞で複製し、細胞変性と壊死を引き起こす。"
        "血管障害により全身性の出血・浮腫を生じ、肝・腎・脾などの多臓器不全に至る。"
    )


def g_coccidiosis(ja: str) -> str:
    return (
        f"{ja}は原虫（Eimeria属・Isospora属等のコクシジウム）の経口感染による腸管疾患である。"
        "摂取されたオーシストが腸管内でスポロゾイトを放出し、腸上皮細胞内で無性生殖（メロゴニー）と"
        "有性生殖を繰り返す。多数の上皮細胞が破壊されることで絨毛が萎縮し、"
        "吸収不良・出血性腸炎・下痢を引き起こす。若齢・過密・不衛生環境で重症化しやすい。"
    )


def g_ectoparasite_mite(ja: str) -> str:
    return (
        f"{ja}は寄生性ダニの体表・皮内・毛包への寄生による。"
        "ダニは表皮を摂食したり皮内にトンネルを形成して機械的刺激を与え、"
        "その排泄物や唾液抗原に対するⅠ型・Ⅳ型過敏反応が掻痒・皮膚炎・脱毛・落屑を引き起こす。"
        "吸血性のダニでは大量寄生により貧血を生じ、掻破による二次的細菌感染を伴うこともある。"
    )


def g_pinworm(ja: str) -> str:
    return (
        f"{ja}は腸管内寄生性線虫（Passalurus ambiguus 等の蟯虫）の感染による。"
        "成虫は盲腸・結腸の管腔内に寄生し、雌は肛門周囲に産卵する。"
        "通常は非病原性で無症状だが、大量寄生では肛門周囲の刺激・掻痒、"
        "若齢・衰弱個体では消化吸収への影響を生じうる。経口的に虫卵を摂取して伝播する。"
    )


def g_mixed_uri(ja: str) -> str:
    return (
        f"{ja}は不適切な環境温度や飼育ストレスによる免疫低下を背景に、"
        "細菌（Pseudomonas、Aeromonas等）やウイルスが鼻腔・上気道粘膜に感染して発症する。"
        "粘膜の炎症・滲出により鼻汁・開口呼吸・喘鳴を呈し、"
        "適切な環境温度（POTZ）の回復が治療・回復の鍵となる。複合感染が多い。"
    )


def g_air_sacculitis(ja: str) -> str:
    return (
        f"{ja}は細菌（E. coli等）・真菌（Aspergillus）・クラミジアなど複数の病原体による気嚢の感染・炎症である。"
        "気嚢は血管に乏しく免疫細胞の到達が困難なため、いったん感染が成立すると"
        "滲出物の貯留・肉芽腫形成・線維化が進行しやすい。"
        "ガス交換と発声に関わる気嚢機能が障害され、呼吸困難・尾の上下動・発声異常を呈する。"
    )


def g_folliculitis(ja: str) -> str:
    return (
        f"{ja}は細菌または真菌による毛包（羽包）の感染性炎症である。"
        "皮膚バリアの破綻や免疫低下を契機に病原体が毛包内で増殖し、"
        "好中球浸潤を伴う炎症・膿疱形成・羽毛の発育異常を引き起こす。"
        "掻破や羽咬により病変が拡大し、慢性化することがある。"
    )


def g_nephritis(ja: str) -> str:
    return (
        f"{ja}は細菌またはウイルス感染による腎臓の炎症である。"
        "病原体は血行性または尿路上行性に腎実質へ到達し、糸球体・尿細管・間質に炎症を引き起こす。"
        "ネフロンの障害により濾過・再吸収機能が低下し、高尿酸血症・多尿/乏尿・"
        "重症例では腎不全に進行する。脱水や腎毒性物質が病態を増悪させる。"
    )


def g_cloacitis(ja: str) -> str:
    return (
        f"{ja}は細菌・真菌の感染による総排泄腔（クロアカ）の炎症である。"
        "下痢・産卵・不衛生な環境による持続的な汚染や粘膜損傷を契機に病原体が増殖し、"
        "粘膜の充血・浮腫・潰瘍・悪臭性分泌物を生じる。"
        "慢性化すると総排泄腔狭窄や排泄障害を来すことがある。"
    )


def g_abscess(ja: str) -> str:
    return (
        f"{ja}は咬傷や外傷を介して細菌が皮下・組織内に侵入して形成される膿瘍である。"
        "侵入した細菌が増殖すると好中球が動員され、組織壊死と膿（死滅した好中球・細菌・壊死組織）が"
        "被膜に包まれて貯留する。膿瘍は周囲組織を圧迫し、破裂・全身播種により蜂窩織炎や敗血症へ進展しうる。"
        "外科的な切開排膿とドレナージが治癒に不可欠である。"
    )


def g_flagellate(ja: str) -> str:
    return (
        f"{ja}は鞭毛虫（Spironucleus／Hexamita 属の原虫）の腸管寄生による。"
        "原虫は経口的に摂取され、腸管内腔および腸陰窩に寄生して上皮を傷害し、"
        "吸収不良・慢性腸炎・体重減少を引き起こす。"
        "ストレス・過密・不衛生な環境で増殖が促進され、若齢・免疫低下個体で重症化しやすい。"
    )


def g_snake_neuro(ja: str) -> str:
    return (
        f"{ja}は複数の原因による中枢神経機能障害である。"
        "封入体病（IBD、レプタリッドアレナウイルス）やパラミクソウイルスなどの感染性要因、"
        "代謝異常、重金属・殺虫剤などの中毒性要因が神経細胞の変性・機能障害を引き起こす。"
        "原因により病態は異なるが、運動失調・スターゲイジング・筋緊張異常など共通の神経症状を呈する。"
    )


# --- Routing -----------------------------------------------------------------
# Order matters: more specific keywords first.
ROUTES = [
    (("botulism", "ボツリヌス"), g_botulism),
    (("tetanus", "破傷風"), g_tetanus),
    (("dermatophilosis",), g_dermatophilosis),
    (("bordetella pneumonia", "bordetella", "ボルデテラ"), g_bordetella_resp),
    (("atrophic rhinitis",), g_atrophic_rhinitis),
    (("macrorhabdosis", "megabacteriosis", "メガバクテリア"), g_macrorhabdosis),
    (("hepatic abscess",), g_hepatic_abscess),
    (("ick (bacterial",), g_bacterial_skin),
    (("abscess", "膿瘍", "bite wound"), g_abscess),
    (("avian influenza",), g_avian_influenza),
    (("reovirus",), g_reovirus),
    (("bursal disease", "gumboro"), g_gumboro),
    (("shope fibroma",), g_shope_fibroma),
    (("non-pdd", "non-bornavirus"), g_pdd_nonviral),
    (("proventricular dilatation", "bornavirus", "pdd", "ボルナ"), g_bornavirus_pdd),
    (("iridovirus",), g_iridovirus),
    (("coccidi", "eimeria", "コクシジウム"), g_coccidiosis),
    (("hexamit", "spironucle", "ヘキサミタ", "鞭毛"), g_flagellate),
    (("pinworm", "passalurus"), g_pinworm),
    (("mite", "cheyletiella", "demodex", "sarcopt", "dermanyssus", "hannemania", "ダニ"), g_ectoparasite_mite),
    (("erysipel", "豚丹毒"), g_erysipelas),
    (("pasteurell", "fowl cholera"), g_pasteurella),
    (("e. coli", "ecoli", "大腸菌"), g_ecoli_septic),
    (("streptococ", "レンサ球菌"), g_strepto),
    (("pseudomonas", "緑膿菌"), g_pseudomonas),
    (
        (
            "clostrid",
            "enterotox",
            "クロストリジウム",
            "dysbiosis",
            "cecal",
            "overeating",
            "enteritis (clostridial)",
            "bacterial enteritis",
            "clostridiosis",
        ),
        g_clostridial_enteric,
    ),
    (("upper respiratory", "uri"), g_mixed_uri),
    (("air sacculitis",), g_air_sacculitis),
    (("folliculitis",), g_folliculitis),
    (("nephritis",), g_nephritis),
    (("cloacitis", "vent gleet"), g_cloacitis),
    (("neurological syndrome",), g_snake_neuro),
]


def route(name: str, desc: str) -> object | None:
    blob = (name + " " + desc).lower()
    for keywords, gen in ROUTES:
        if any(k in blob for k in keywords):
            return gen
    return None


def build_replacement(name: str, name_ja: str, desc: str) -> str | None:
    gen = route(name, desc)
    if gen is None:
        return None
    ja = name_ja or name
    return gen(ja)


# --- Application -------------------------------------------------------------

SPECIES_FILE_MAP = {
    "Cat": "cat_diseases.py",
    "Dog": "dog_diseases.py",
    "Rabbit": "rabbit_diseases.py",
    "Hamster": "hamster_diseases.py",
    "Guinea Pig": "guinea_pig_diseases.py",
    "Chinchilla": "chinchilla_diseases.py",
    "Ferret": "ferret_diseases.py",
    "Hedgehog": "hedgehog_diseases.py",
    "Sugar Glider": "sugar_glider_diseases.py",
    "Degu": "degu_diseases.py",
    "Bird": "bird_diseases.py",
    "Parakeet": "parakeet_diseases.py",
    "Parrot": "parrot_diseases.py",
    "Reptile": "reptile_diseases.py",
    "Tortoise": "tortoise_diseases.py",
    "Snake": "snake_diseases.py",
    "Lizard": "lizard_diseases.py",
    "Amphibian": "amphibian_diseases.py",
    "Fish": "fish_diseases.py",
    "Other Exotic": "exotic_other_diseases.py",
}


def fix_json(targets: dict) -> int:
    """Rewrite misapplied pathophysiology_ja in the JSON overlay.

    ``targets`` maps (species, name) -> replacement text.
    Returns the number of entries changed.
    """
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    changed = 0
    for entry in data:
        key = (entry.get("species", ""), entry.get("name", ""))
        if key in targets and is_misapplied(
            entry.get("pathophysiology_ja", ""),
            entry.get("name", ""),
            entry.get("description_ja", ""),
        ):
            entry["pathophysiology_ja"] = targets[key]
            changed += 1
    if changed:
        JSON_PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return changed


def fix_python(species: str, name_to_repl: dict) -> int:
    """Rewrite (or insert) pathophysiology_ja in a species Python module.

    Each disease is a dict literal opening with ``    {`` and closing with
    ``    },`` (4-space indent; fields at 8 spaces). For each target disease we
    locate its block, then:

    * If ``pathophysiology_ja`` exists *within the block* and holds a category
      template -> replace its value.
    * If the field is absent within the block (the served text was produced by
      the runtime fallback generator) -> insert a new field after
      ``description_ja`` (or after ``name_ja``) so enrichment serves it.
    """
    fname = SPECIES_FILE_MAP.get(species)
    if not fname:
        return 0
    path = SPECIES_DIR / fname
    text = path.read_text(encoding="utf-8")
    val_re = re.compile(r'"pathophysiology_ja":\s*"((?:[^"\\]|\\.)*)"')
    changed = 0
    for name, repl in name_to_repl.items():
        anchor = f'"name": "{name}",'
        ai = text.find(anchor)
        if ai < 0:
            continue
        block_end = text.find("\n    },", ai)
        if block_end < 0:
            continue
        escaped = repl.replace("\\", "\\\\").replace('"', '\\"')
        m = val_re.search(text, ai, block_end)
        if m:
            if _template_class(m.group(1)) is None:
                continue  # already curated; leave it
            text = text[: m.start(1)] + escaped + text[m.end(1) :]
            changed += 1
            continue
        # Field absent -> insert after description_ja (preferred) or name_ja.
        ins_re = re.compile(r'( *)"(?:description_ja|name_ja)":\s*"(?:[^"\\]|\\.)*",\n')
        last = None
        for mm in ins_re.finditer(text, ai, block_end):
            last = mm
        if not last:
            continue
        indent = last.group(1)
        new_line = f'{indent}"pathophysiology_ja": "{escaped}",\n'
        text = text[: last.end()] + new_line + text[last.end() :]
        changed += 1
    if changed:
        path.write_text(text, encoding="utf-8")
    return changed


def main() -> None:
    import importlib
    import sys

    sys.path.insert(0, str(ROOT))

    # Re-derive the misapplied set from the *enriched* (served) DISEASES so we
    # operate on exactly what users see.
    species_mods = {
        "Cat": "cat_diseases",
        "Dog": "dog_diseases",
        "Rabbit": "rabbit_diseases",
        "Hamster": "hamster_diseases",
        "Guinea Pig": "guinea_pig_diseases",
        "Chinchilla": "chinchilla_diseases",
        "Ferret": "ferret_diseases",
        "Hedgehog": "hedgehog_diseases",
        "Sugar Glider": "sugar_glider_diseases",
        "Degu": "degu_diseases",
        "Bird": "bird_diseases",
        "Parakeet": "parakeet_diseases",
        "Parrot": "parrot_diseases",
        "Reptile": "reptile_diseases",
        "Tortoise": "tortoise_diseases",
        "Snake": "snake_diseases",
        "Lizard": "lizard_diseases",
        "Amphibian": "amphibian_diseases",
        "Fish": "fish_diseases",
        "Other Exotic": "exotic_other_diseases",
    }

    json_targets: dict = {}
    py_targets: dict = {}
    skipped: list = []
    for species, mn in species_mods.items():
        mod = importlib.import_module(f"api.species.{mn}")
        for d in getattr(mod, "DISEASES", []):
            if not isinstance(d, dict):
                continue
            name = d.get("name", "") or d.get("name_en", "")
            if not is_misapplied(d.get("pathophysiology_ja", ""), name, d.get("description_ja", "")):
                continue
            repl = build_replacement(name, d.get("name_ja", ""), d.get("description_ja", ""))
            if repl is None:
                skipped.append((species, name))
                continue
            json_targets[(species, name)] = repl
            py_targets.setdefault(species, {})[name] = repl

    json_changed = fix_json(json_targets)
    py_changed = 0
    for species, mapping in py_targets.items():
        py_changed += fix_python(species, mapping)

    print(f"Routed replacements: {len(json_targets)}")
    print(f"JSON entries changed: {json_changed}")
    print(f"Python entries changed: {py_changed}")
    if skipped:
        print(f"\nUNROUTED (no generator matched) — {len(skipped)}:")
        for sp, nm in skipped:
            print(f"  {sp}: {nm}")


if __name__ == "__main__":
    main()
