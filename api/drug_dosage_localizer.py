"""薬用量文字列の日本語ローカライザ（決定論的・fail-closed）。

多くの薬品（特にエキゾチック種）の ``species_info[species]`` は英語の ``dosage``
だけを持ち、``dosage_ja`` が欠落している。フロントエンドは ``dosage_ja || dosage``
で表示するため、日本語UIでも "5-10 mg/kg PO/IM q24h" のように投与経路・投与間隔が
英語略号のまま表示されていた（主対象＝日本の獣医師にとって読みにくい）。

このモジュールは、**用量文字列が管理された語彙のみで構成されている場合に限り**、
``dosage`` から ``dosage_ja`` を決定論的に生成する。

安全設計（患者安全上、機械翻訳のリスクを排除）:
  * 数値・単位（``10-20 mg/kg`` 等）は**一切改変せずそのまま保持**する。
  * 投与経路・投与間隔・接続語は**ホワイトリストの語彙のみ**を日本語化する。
  * 認識できない英単語（``Apply``, ``titrate``, ``nebulized`` 等の自由文）が
    1語でも含まれていれば **None を返して変換を中止**する（誤訳を出さない）。
  * 既存の ``dosage_ja`` は**上書きしない**（欠落エントリのみ補完）。

生成される日本語は既存の獣医師記入済み ``dosage_ja`` と同じ表記規約に従う
（例: ``5-20 mg/kg 経口/静注 24時間毎``）。
"""

from __future__ import annotations

import re
from typing import Any, Optional

# 投与経路の略号 → 日本語（複合経路 "PO/IM" は "/" 分割で処理）
_ROUTE_MAP: dict[str, str] = {
    "PO": "経口",
    "IV": "静注",
    "IM": "筋注",
    "SC": "皮下",
    "SQ": "皮下",
    "IO": "骨髄内",
    "IP": "腹腔内",
    "ICe": "体腔内",
    "IT": "気管内",
    "IN": "経鼻",
    "IA": "関節内",
    "PR": "直腸内",
    "SL": "舌下",
    "ID": "皮内",
    "IC": "心臓内",
}

# 単独トークンとして現れる接続語・修飾語 → 日本語
_WORD_MAP: dict[str, str] = {
    "or": "または",
    "then": "その後",
    "once": "単回",
    "single": "単回",
    "bath": "薬浴",
    "immersion": "浸漬浴",
    "topical": "局所",
    "sublingual": "舌下",
    "oral": "経口",
    "slow": "緩徐",
    "slowly": "緩徐に",
    "bolus": "ボーラス",
    "loading": "負荷",
    "maintenance": "維持",
    "divided": "分割",
    "diluted": "希釈",
    "dilute": "希釈",
}

# そのまま保持する頻度・投与法略号（言語非依存で維持する慣用語）
_KEEP_TOKENS: frozenset[str] = frozenset({"CRI", "PRN", "prn"})

# 大文字小文字を無視して一致させる固定フレーズ（末尾ピリオドは除去して判定）
_FIXED_PHRASES: dict[str, str] = {
    "not established": "用量未確立",
    "not well established": "十分に確立されていない",
    "dose not established": "用量未確立",
    "not indicated": "適応なし",
    "not recommended": "非推奨",
    "contraindicated": "禁忌",
    "unknown": "不明",
    "not applicable": "該当なし",
}

# 数値・単位トークンとみなす（＝そのまま保持）。数字を含めば単位付き用量とみなす。
_HAS_DIGIT = re.compile(r"\d")
# CJK（日本語）を含むか。原文が既に日本語混じりなら変換対象外とする。
_HAS_CJK = re.compile(r"[぀-ヿ㐀-䶿一-鿿ｦ-ﾟ]")
# 純粋な単位語（数字なし）。例: "mg/kg" 単独で現れることは稀だが保持対象。
_UNIT_WORDS: frozenset[str] = frozenset(
    {
        "mg",
        "g",
        "kg",
        "mL",
        "ml",
        "L",
        "cm",
        "mm",
        "m²",
        "m2",
        "IU",
        "U",
        "mEq",
        "mcg",
        "µg",
        "μg",
        "ug",
        "tsp",
        "puff",
        "day",
        "hr",
        "min",
        "joint",
        "gallon",
        "eye",
    }
)
# 分母として現れる動物単位（"mg/cat" → "mg/頭"）。日本語の慣用に合わせて「頭」に統一。
_DENOM_MAP: dict[str, str] = {
    "cat": "頭",
    "dog": "頭",
    "animal": "頭",
    "bird": "頭",
    "head": "頭",
    "patient": "頭",
}

# 頻度略号: q24h / q8-12h / q24-48h / q12h など
_FREQ_H = re.compile(r"^q(\d+)(?:-(\d+))?h$")
# 頻度略号: q14d / q7-14d / q21d（日単位、"d" サフィックス）
_FREQ_D = re.compile(r"^q(\d+)(?:-(\d+))?d$")
# 頻度略号（英語表記）: SID/BID/TID/QID
_FREQ_LATIN: dict[str, str] = {
    "SID": "1日1回",
    "BID": "1日2回",
    "TID": "1日3回",
    "QID": "1日4回",
}


def _localize_route(token: str) -> Optional[str]:
    """複合経路（"PO/IM"）を含む投与経路トークンを日本語化。未知経路は None。"""
    parts = token.split("/")
    out: list[str] = []
    for p in parts:
        if p in _ROUTE_MAP:
            out.append(_ROUTE_MAP[p])
        else:
            return None
    return "/".join(out)


def _localize_freq(token: str) -> Optional[str]:
    """頻度トークン（q24h, q8-12h, q14d, SID 等）を日本語化。未知は None。"""
    m = _FREQ_H.match(token)
    if m:
        lo, hi = m.group(1), m.group(2)
        rng = f"{lo}-{hi}" if hi else lo
        return f"{rng}時間毎"
    m = _FREQ_D.match(token)
    if m:
        lo, hi = m.group(1), m.group(2)
        rng = f"{lo}-{hi}" if hi else lo
        return f"{rng}日毎"
    if token in _FREQ_LATIN:
        return _FREQ_LATIN[token]
    return None


def _localize_unit_token(token: str) -> Optional[str]:
    """数値・単位トークンを返す（動物分母は「頭」に変換）。単位でなければ None。

    数字を含むトークン（"10-20", "IU/30g" 等）はそのまま保持する。数字を含まない
    スラッシュ区切り（"mg/kg", "mg/cat"）は各部が既知の単位か動物分母のときのみ
    単位とみなし、分母のみ日本語化する。
    """
    if _HAS_DIGIT.search(token):
        return token  # 数値付きトークンは改変しない
    parts = token.split("/")
    out: list[str] = []
    for part in parts:
        if part in _UNIT_WORDS:
            out.append(part)
        elif part in _DENOM_MAP:
            out.append(_DENOM_MAP[part])
        else:
            return None
    return "/".join(out)


def localize_dosage(dosage: str) -> Optional[str]:
    """英語の用量文字列を日本語化する。管理語彙で完全に構成される場合のみ変換。

    変換できない（自由文を含む）場合は None を返す（fail-closed）。
    """
    if not dosage or not isinstance(dosage, str):
        return None
    text = dosage.strip()
    if not text:
        return None

    # 原文に日本語（CJK）が含まれる場合は「清潔な英語」ではないため変換しない。
    # ホワイトリスト方式の前提（英語略号のみ）が崩れ、誤変換のリスクがあるため。
    if _HAS_CJK.search(text):
        return None

    # 固定フレーズ（"Not established" 等）
    key = text.rstrip(".").strip().lower()
    if key in _FIXED_PHRASES:
        return _FIXED_PHRASES[key]

    # トークン分割: 空白で分割しつつ、区切り記号（; , × ( )）は保持する。
    # 日本語では読点・記号をそのまま維持し、英単語のみ翻訳する。
    # "×"（用量回数・期間の乗算記号）は頻度略号に密着することがある（"q12h×3"）ため、
    # 分割前に前後へ空白を挿入して独立トークンにする。
    tokenizable = text.replace("×", " × ")
    raw_tokens = tokenizable.split()
    out: list[str] = []
    for tok in raw_tokens:
        # 先頭・末尾の区切り記号を切り離す（例: "q12h;" → "q12h" + ";"）
        m = re.match(r"^([(\[]*)(.*?)([)\],;×]*)$", tok)
        prefix, core, suffix = (m.group(1), m.group(2), m.group(3)) if m else ("", tok, "")

        if core == "":
            out.append(prefix + suffix)
            continue

        translated: Optional[str]
        if core in _KEEP_TOKENS:
            translated = core
        elif _localize_freq(core) is not None:
            # 頻度略号（q12h 等）は数字を含むが単位ではないため先に判定
            translated = _localize_freq(core)
        elif _localize_unit_token(core) is not None:
            translated = _localize_unit_token(core)  # 数値・単位（分母のみ日本語化）
        elif core in _ROUTE_MAP or ("/" in core and _localize_route(core) is not None):
            translated = _localize_route(core)
        elif core in _WORD_MAP:
            translated = _WORD_MAP[core]
        elif core.lower() in _WORD_MAP:
            translated = _WORD_MAP[core.lower()]
        else:
            # 認識できない英単語 → 変換中止（誤訳を出さない）
            return None

        out.append(prefix + (translated or core) + suffix)

    result = " ".join(out).strip()
    # 変換結果が原文と同一（＝翻訳すべき語彙が無かった）なら None
    if not result or result == text:
        return None
    return result


def fill_missing_dosage_ja(drugs: list[dict[str, Any]]) -> int:
    """DRUGS 内で dosage はあるが dosage_ja が欠落したエントリを決定論的に補完。

    補完できた species_info エントリ数を返す。既存の dosage_ja は保持。
    """
    filled = 0
    for drug in drugs:
        species_info = drug.get("species_info") or {}
        for _sp, info in species_info.items():
            if not isinstance(info, dict):
                continue
            if info.get("dosage_ja"):
                continue
            dosage = info.get("dosage")
            if not dosage:
                continue
            ja = localize_dosage(dosage)
            if ja:
                info["dosage_ja"] = ja
                filled += 1
    return filled
