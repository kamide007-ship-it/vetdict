"""Name the antiparasitic products a Japanese clinic can actually dispense.

The parasitology records listed generic actives — "適切な駆虫薬", pyrantel,
selamectin — but almost never the product a vet in Japan orders by name, so the
text stopped short of the decision the reader is actually making. This module
appends a compact 【日本国内で入手可能な代表的製剤】 block, keyed by the parasite
the record is about.

Dosing is stated the way each product is genuinely dosed:

* oral suspensions/tablets with a published per-kilogram figure carry it
  (Procox: 製剤 0.5 mL/kg PO 単回 = emodepside 0.45 mg/kg + toltrazuril 9 mg/kg,
  from Elanco Japan's product information);
* spot-ons and chewables are dosed by WEIGHT BAND from the pack, not by mg/kg, so
  the block says 体重帯別に製品ラベルに従う rather than inventing a figure. Making
  up a mg/kg for a weight-band product would be the same class of error the rest
  of this package exists to remove.

Two safety notes ride along because they are the ones that kill patients:

* canine permethrin/pyrethroid spot-ons are fatal in cats, so every feline
  ectoparasite block carries that warning;
* the isoxazolines (afoxolaner, fluralaner, lotilaner, sarolaner) carry a
  neurological adverse-event signal, so records naming them flag caution in
  animals with a seizure history (FDA/EMA class warning).
"""

from __future__ import annotations

import re

_MARKER = "【日本国内で入手可能な代表的製剤】"

# Weight-band products must not be given an invented mg/kg.
_BAND = "体重帯別に製品ラベルに従う"

_CAT_PERMETHRIN_WARNING = (
    "⚠猫には犬用のペルメトリン／ピレスロイド系スポットオンを絶対に使用しない"
    "（猫はグルクロン酸抱合能が低く、振戦・重積痙攣から死に至る）。猫用として承認された製剤のみを用いる。"
)
_ISOXAZOLINE_WARNING = (
    "※イソオキサゾリン系（アフォキソラネル・フルララネル・ロチラネル・サロラネル）は"
    "痙攣・振戦等の神経系副作用の報告があり、てんかん既往例では慎重に選択する。"
)

# Product blocks by parasite class. Each entry: (species set, marker regexes, text).
_PRODUCTS: list[tuple[frozenset[str], tuple[str, ...], str]] = [
    (
        frozenset({"dog"}),
        ("回虫", "鉤虫", "鞭虫", "roundworm", "hookworm", "whipworm", "toxocar", "ascarid"),
        "プロコックス®経口懸濁液（エモデプシド＋トルトラズリル）: 製剤 0.5 mL/kg PO 単回"
        "（＝エモデプシド 0.45 mg/kg＋トルトラズリル 9 mg/kg）。犬回虫・犬鉤虫・犬鞭虫＋コクシジウムを同時駆除。"
        "2週齢以上かつ体重400 g以上から使用可。／"
        "ドロンタール®プラス錠（プラジクアンテル＋パモ酸ピランテル＋フェバンテル）: 回虫・鉤虫・鞭虫・条虫を一剤で駆除、"
        f"{_BAND}。／"
        "ミルベマイシンオキシム製剤（ミルベマイシンA錠 等）0.5-1 mg/kg PO 月1回: 消化管内線虫の駆除とフィラリア予防を兼ねる。／"
        "ネクスガード®スペクトラ（アフォキソラネル＋ミルベマイシンオキシム）: 月1回経口で"
        f"ノミ・マダニ＋フィラリア予防＋消化管内線虫をカバー、{_BAND}。",
    ),
    (
        frozenset({"cat"}),
        ("回虫", "鉤虫", "roundworm", "hookworm", "toxocar", "ascarid"),
        "ブロードライン®（フィプロニル＋(S)-メトプレン＋エプリノメクチン＋プラジクアンテル）: スポットオン1剤で"
        f"猫回虫・鉤虫・条虫＋ノミ・マダニ＋フィラリア予防をカバー、{_BAND}。／"
        f"レボリューション®（セラメクチン）: 猫回虫・ノミ・ミミヒゼンダニ・フィラリア予防、{_BAND}。／"
        "パモ酸ピランテル 5-10 mg/kg PO（2-3週後に再投与）。",
    ),
    (
        frozenset({"dog", "cat"}),
        ("条虫", "tapeworm", "cestode", "dipylidium", "echinococc"),
        "犬: ドロンタール®プラス錠（プラジクアンテル配合）。猫: ドロンシット®錠（プラジクアンテル）"
        "またはブロードライン®（プラジクアンテル配合スポットオン）。"
        "プラジクアンテル 5 mg/kg PO/SC/IM 単回が標準。"
        "瓜実条虫はノミが中間宿主のため、駆虫と同時にノミ対策を行わないと必ず再感染する。"
        "⚠エキノコックス（多包条虫）は感染症法の四類感染症で獣医師に届出義務があり、北海道を中心に公衆衛生上きわめて重要。"
        "疑わしい場合は自治体・家畜保健衛生所に相談する。",
    ),
    (
        frozenset({"dog"}),
        ("ノミ", "マダニ", "flea", "tick"),
        "経口: ネクスガード®／ネクスガード®スペクトラ（アフォキソラネル）、ブラベクト®（フルララネル、1回で約12週間持続）、"
        "クレデリオ®（ロチラネル）、シンパリカ®（サロラネル）。／"
        "スポットオン: フロントライン®プラス（フィプロニル＋(S)-メトプレン）、ブラベクト®スポット。"
        f"いずれも{_BAND}。"
        "駆除は同居動物すべてに同時実施し、寝床・カーペットの洗濯と掃除機がけで環境中の未成熟ステージを並行して除去する。"
        + _ISOXAZOLINE_WARNING,
    ),
    (
        frozenset({"cat"}),
        ("ノミ", "マダニ", "flea", "tick"),
        "猫用として承認された製剤のみを使用する: ブロードライン®（フィプロニル＋(S)-メトプレン＋エプリノメクチン＋"
        "プラジクアンテル）、レボリューション®（セラメクチン）、フロントライン®プラス、ブラベクト®スポット（フルララネル）。"
        f"いずれも{_BAND}。" + _CAT_PERMETHRIN_WARNING + _ISOXAZOLINE_WARNING,
    ),
    (
        frozenset({"dog"}),
        ("フィラリア", "heartworm", "dirofilar"),
        "予防: ミルベマイシンオキシム製剤（消化管内線虫も駆除）、イベルメクチン＋パモ酸ピランテル配合チュアブル、"
        "ネクスガード®スペクトラ（ノミ・マダニと兼用）、プロハート®SR-12（モキシデクチン徐放性注射、年1回）。"
        f"いずれも{_BAND}。"
        "⚠投与開始前に必ず抗原検査／ミクロフィラリア検査で感染の有無を確認する"
        "（感染犬にマクロライド系を投与するとミクロフィラリアの急速死によりショックを起こしうる）。"
        "蚊の発生期間に応じて通年または季節投与を選択し、投与忘れが最大のリスク因子であることを飼い主に説明する。",
    ),
    (
        frozenset({"cat"}),
        ("フィラリア", "heartworm", "dirofilar"),
        "予防: レボリューション®（セラメクチン）、ブロードライン®（エプリノメクチン配合）、ミルベマイシンオキシム製剤。"
        f"いずれも{_BAND}。"
        "猫は非好適宿主で虫体数が少なく成虫駆除薬（メラルソミン）は禁忌のため、"
        "治療より予防が決定的に重要である。室内飼育でも感染例があり通年予防が推奨される。",
    ),
    (
        frozenset({"dog", "cat"}),
        (
            "疥癬",
            "ヒゼンダニ",
            "ミミヒゼンダニ",
            "耳ダニ",
            "毛包虫",
            "ニキビダニ",
            "sarcopt",
            "demodic",
            "ear mite",
            "otodect",
        ),
        "レボリューション®（セラメクチン）はミミヒゼンダニ・疥癬に汎用され、犬猫とも適応。"
        "イソオキサゾリン系（ブラベクト®・ネクスガード®・シンパリカ®・クレデリオ®）は疥癬・毛包虫症にも有効との報告が多く、"
        "近年は毛包虫症の第一選択として用いられる。猫の耳ダニにはブロードライン®も使用可。"
        f"いずれも{_BAND}。"
        "疥癬は接触感染するため同居動物すべてを同時に治療し、寝具・ブラシを洗浄する。"
        "疥癬は人にも一過性の丘疹を生じうる（人体では自然消退）。" + _ISOXAZOLINE_WARNING,
    ),
    (
        frozenset({"dog", "cat"}),
        ("コクシジウム", "イソスポラ", "coccidi", "isospora", "cystoisospora"),
        "犬: プロコックス®経口懸濁液（トルトラズリル 9 mg/kg 相当を含む、製剤 0.5 mL/kg PO 単回）が"
        "コクシジウムと消化管内線虫を同時に処理でき、下痢を伴う子犬に有用。"
        "／トルトラズリル単剤、ST合剤（スルファジメトキシン等）も用いられる。"
        "多頭飼育・繁殖施設ではオーシストが環境中で長期生存するため、"
        "熱湯・スチームによる消毒と糞便の即時除去を治療と並行して行わないと再感染が続く。",
    ),
    (
        frozenset({"dog", "cat"}),
        ("ジアルジア", "giardi"),
        "フェンベンダゾール 50 mg/kg PO q24h × 3-5日（第一選択、妊娠中も比較的安全）、"
        "またはメトロニダゾール 15-25 mg/kg PO q12h × 5-7日。"
        "被毛に付着したシストによる再感染を断つため、治療最終日にシャンプーで洗浄し、"
        "環境は四級アンモニウム系で消毒する。人獣共通感染の可能性があり、飼い主の手洗いを指導する。",
    ),
]


# Substring collisions that would attach the wrong product list. These are the
# same trap the rest of this package documents (coccidio- vs coccidia-):
#   * coccidioidomycosis / コクシジオイデス症 is a systemic FUNGAL infection
#     (Coccidioides immitis), not a protozoal coccidiosis — offering it an
#     anticoccidial is precisely the error this package exists to remove;
#   * cytauxzoonosis is a protozoal disease *transmitted by* ticks, not a tick
#     infestation, so an acaricide block would misdescribe its treatment.
_EXCLUSIONS = (
    "coccidioidomyc",
    "coccidioides",
    "コクシジオイデス",
    "cytauxzoon",
    "シタウクソーン",
)


def _matches(markers: tuple[str, ...], text: str) -> bool:
    lowered = text.lower()
    if any(x in lowered for x in _EXCLUSIONS):
        return False
    return any(m.lower() in lowered for m in markers)


def jp_product_block(species: str, name: str, name_ja: str, treatment_ja: str) -> str | None:
    """Return the product block to append, or ``None`` when not applicable.

    ``None`` means the record is not one of the covered parasitoses, or the block
    is already present (the function is idempotent).
    """
    if not treatment_ja or _MARKER in treatment_ja:
        return None
    subject = f"{name} {name_ja}"
    for species_set, markers, body in _PRODUCTS:
        if species not in species_set:
            continue
        if not _matches(markers, subject):
            continue
        return f"{_MARKER}{body}"
    return None


def apply_jp_products(species: str, name: str, name_ja: str, treatment_ja: str) -> str | None:
    """Append the product block to ``treatment_ja``; ``None`` when unchanged."""
    block = jp_product_block(species, name, name_ja, treatment_ja)
    if not block:
        return None
    text = treatment_ja.rstrip()
    if text and not re.search(r"[。．]$", text):
        text += "。"
    return f"{text}{block}"
