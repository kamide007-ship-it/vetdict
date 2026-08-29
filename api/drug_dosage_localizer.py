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
    "empirical": "経験的に",
    "solution": "溶液",
    "ointment": "軟膏",
    "shampoo": "シャンプー",
    "spray": "スプレー",
    "gel": "ジェル",
    "cream": "クリーム",
    "suspension": "懸濁液",
    "monthly": "月1回",
    "weekly": "週1回",
    "biweekly": "隔週",
    "daily": "1日1回",
}

# そのまま保持する頻度・投与法略号（言語非依存で維持する慣用語）
_KEEP_TOKENS: frozenset[str] = frozenset({"CRI", "PRN", "prn", "+"})

# 大文字小文字を無視して一致させる固定フレーズ（末尾ピリオドは除去して判定）
_FIXED_PHRASES: dict[str, str] = {
    "not established": "用量未確立",
    "not well established": "十分に確立されていない",
    "dose not established": "用量未確立",
    "not indicated": "適応なし",
    "not recommended": "非推奨",
    "not recommended due to toxicity": "毒性のため非推奨",
    "not commonly used": "一般的に使用されない",
    "contraindicated": "禁忌",
    "do not use": "使用しない",
    "unknown": "不明",
    "not applicable": "該当なし",
}

# 部分フレーズ → 日本語（トークン分割前に置換する管理語彙のフレーズ集）。
# 数値はキャプチャグループでそのまま保持し、置換結果はプレースホルダで保護して
# 残りのトークンには従来どおり fail-closed の語彙判定を適用する。
# 順序が重要: より特異的なフレーズ（"repeat in N days"）を汎用（"N days"）より先に置く。
_PHRASE_PATTERNS: list[tuple[re.Pattern, str]] = [
    (re.compile(r"(?i)\brepeat (?:in|after) (\d+(?:-\d+)?) ?days?\b"), r"\1日後に再投与"),
    (re.compile(r"(?i)\brepeat (?:in|after) (\d+(?:-\d+)?) ?weeks?\b"), r"\1週後に再投与"),
    (re.compile(r"(?i)\bq(\d+(?:-\d+)?) ?days\b"), r"\1日毎"),
    (re.compile(r"(?i)\bq(\d+(?:-\d+)?) ?weeks?\b"), r"\1週毎"),
    (re.compile(r"(?i)\bfor (\d+(?:-\d+)?) ?min(?:utes)?\b"), r"\1分間"),
    (re.compile(r"(?i)\bfor (\d+(?:-\d+)?) ?days?\b"), r"\1日間"),
    (re.compile(r"(?i)\bfor (\d+(?:-\d+)?) ?weeks?\b"), r"\1週間"),
    (re.compile(r"(?i)\bover (\d+(?:-\d+)?) ?min(?:utes)?\b"), r"\1分かけて"),
    (re.compile(r"(?i)\bover (\d+(?:-\d+)?) ?(?:hr|hrs|hours?)\b"), r"\1時間かけて"),
    (re.compile(r"(?i)\bsingle dose\b"), "単回投与"),
    (re.compile(r"(?i)\bonce daily\b"), "1日1回"),
    (re.compile(r"(?i)\btwice daily\b"), "1日2回"),
    (re.compile(r"(?i)\bthree times daily\b"), "1日3回"),
    (re.compile(r"(?i)\b(\d+(?:-\d+)?) ?drops?\b"), r"\1滴"),
    (re.compile(r"(?i)\b(\d+(?:-\d+)?) ?puffs?\b"), r"\1噴霧"),
    (re.compile(r"(?i)\b(\d+(?:-\d+)?) ?doses\b"), r"\1回投与"),
    (re.compile(r"(?i)\b(\d+(?:-\d+)?) ?injections\b"), r"\1回注射"),
    (re.compile(r"(?i)\bunder (?:the )?tongue\b"), "舌下"),
    (re.compile(r"(?i)\bmixed (?:in|with) food\b"), "フードに混和"),
    (re.compile(r"(?i)\bin food\b"), "フードに混和"),
    (re.compile(r"(?i)\bin drinking water\b"), "飲水に添加"),
    (re.compile(r"(?i)\bper meal\b"), "毎食"),
    (re.compile(r"(?i)\bwith meals?\b"), "食事と共に"),
    (re.compile(r"(?i)\bon (?:an )?empty stomach\b"), "空腹時"),
    (re.compile(r"(?i)\bas needed\b"), "必要時"),
    (re.compile(r"(?i)\bto effect\b"), "効果発現まで"),
    (re.compile(r"(?i)\bvia spacer\b"), "スペーサー使用"),
    (re.compile(r"(?i)\bwith mask\b"), "マスク併用"),
    (re.compile(r"(?i)\bvia nebulizer\b"), "ネブライザー投与"),
    (re.compile(r"(?i)\bnebulized\b"), "ネブライザー投与"),
    (re.compile(r"(?i)\bapply (?:a )?thin layer to (?:the )?wound\b"), "創部に薄く塗布"),
    (re.compile(r"(?i)\bapply (?:a )?thin layer to (?:the )?affected areas?\b"), "患部に薄く塗布"),
    (re.compile(r"(?i)\bapply (?:a )?thin layer\b"), "薄く塗布"),
    (re.compile(r"(?i)\bapply to (?:the )?affected areas?\b"), "患部に塗布"),
    (re.compile(r"(?i)\bto (?:the )?affected areas?\b"), "患部に"),
    (
        re.compile(r"(?i)\bapply (\d+(?:\.\d+)?) ?cm ribbon to (?:the )?affected eyes?\b"),
        r"患眼に\1cmリボン状に塗布",
    ),
    (re.compile(r"(?i)\bto (?:the )?affected eyes?\b"), "患眼に"),
    (re.compile(r"(?i)\btopical for wounds\b"), "創部に局所塗布"),
    (re.compile(r"(?i)\brepeat (?:in|after) (\d+(?:-\d+)?) ?min(?:utes)?\b"), r"\1分後に再投与"),
    (re.compile(r"(?i)\bif needed\b"), "必要に応じて"),
    (re.compile(r"(?i)\bwith food\b"), "食事と共に"),
    (re.compile(r"(?i)\bnot established\b"), "用量未確立"),
    (re.compile(r"(?i)\bnot approved for cats\b"), "猫では未承認"),
    (re.compile(r"(?i)\bnot approved for dogs\b"), "犬では未承認"),
    (
        re.compile(r"(?i)\bstart very low and titrate over weeks\b"),
        "ごく低用量から開始し数週間かけて漸増",
    ),
    (re.compile(r"(?i)\bstart (?=\d)"), "開始用量 "),
    (re.compile(r"(?i)\bin (\d+(?:\.\d+)?) ?m[lL] (?:of )?saline\b"), r"生理食塩水\1mLに溶解"),
    (re.compile(r"(?i)\bin (\d+(?:\.\d+)?) ?L (?:of )?water\b"), r"水\1Lに溶解"),
    (re.compile(r"(?i)\bin (\d+(?:\.\d+)?) ?m[lL]\b"), r"\1mLに溶解"),
    (re.compile(r"(?i)\bvia nasogastric tube\b"), "経鼻胃チューブ投与"),
    # 汎用の期間表現は特異的フレーズの後に置く（"× 3-5 days" 等の残余を捕捉）
    (re.compile(r"(?i)\b(\d+(?:-\d+)?) ?days\b"), r"\1日間"),
    (re.compile(r"(?i)\b(\d+(?:-\d+)?) ?weeks\b"), r"\1週間"),
]

# フレーズ置換結果を保護するプレースホルダ（私用領域文字。入力は CJK ガードで
# 日本語を含まないことが保証されるため、原文と衝突しない）。
_PH_OPEN = "\ue000"
_PH_CLOSE = "\ue001"
_PH_TOKEN = re.compile(rf"^{_PH_OPEN}(\d+){_PH_CLOSE}$")

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

    # 管理語彙フレーズ（"repeat in 14 days" 等）をプレースホルダに置換して保護する。
    # 置換後の残りトークンには従来どおり fail-closed の語彙判定が適用されるため、
    # フレーズ以外に未知語があれば全体として None になる（安全性は不変）。
    protected: list[str] = []

    def _protect(pattern: re.Pattern, repl: str, s: str) -> str:
        def _sub(m: re.Match) -> str:
            protected.append(m.expand(repl))
            return f" {_PH_OPEN}{len(protected) - 1}{_PH_CLOSE} "

        return pattern.sub(_sub, s)

    phrased = text
    for pattern, repl in _PHRASE_PATTERNS:
        phrased = _protect(pattern, repl, phrased)

    # トークン分割: 空白で分割しつつ、区切り記号（; , × ( )）は保持する。
    # 日本語では読点・記号をそのまま維持し、英単語のみ翻訳する。
    # "×"（用量回数・期間の乗算記号）は頻度略号に密着することがある（"q12h×3"）ため、
    # 分割前に前後へ空白を挿入して独立トークンにする。
    tokenizable = phrased.replace("×", " × ")
    # 全角括弧も独立トークンにする。"q24h（Carpenter）" のように括弧が頻度略号に
    # 密着すると、数値保持パス（digit-containing token は改変しない）を通って
    # 英語の頻度略号ごと日本語出力に漏れていた。分割すれば括弧内の未知語が
    # fail-closed を正しく発火させる。
    tokenizable = tokenizable.replace("（", " （ ").replace("）", " ） ")
    raw_tokens = tokenizable.split()
    out: list[str] = []
    for tok in raw_tokens:
        # 先頭・末尾の区切り記号を切り離す（例: "q12h;" → "q12h" + ";"、"q24h." → "q24h" + "."）。
        # 文末ピリオドを剥がさないと "q24h." が頻度辞書にマッチせず、数値保持パスを
        # 通って英語の頻度略号がそのまま日本語出力に漏れる（10.5 等の小数点は
        # トークン内部にあるため影響しない）。
        # 末尾のコロンも剥がす（"PO:" / "nebulized:" のようなラベル用法。
        # 数値比 "1:32" はコロンがトークン内部にあるため影響しない）。
        m = re.match(r"^([(\[]*)(.*?)([)\],;×.:]*)$", tok)
        prefix, core, suffix = (m.group(1), m.group(2), m.group(3)) if m else ("", tok, "")

        if core == "":
            out.append(prefix + suffix)
            continue

        translated: Optional[str]
        ph = _PH_TOKEN.match(core)
        if ph:
            # フレーズ置換済みプレースホルダ → 保護しておいた日本語に復元
            translated = protected[int(ph.group(1))]
        elif core in _KEEP_TOKENS:
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
    # フレーズ置換で独立トークン化された区切り記号の前の余分な空白を除去
    result = re.sub(r"\s+([;,.:])", r"\1", result)
    # 変換結果が原文と同一（＝翻訳すべき語彙が無かった）なら None
    if not result or result == text:
        return None
    return result


# 英語と日本語が同一文字列に併記されたエントリ（完全一致のみ分割）。
# "dosage" に両言語が焼き込まれていると、日本語UIには英語が、英語UIには日本語が
# それぞれ余分に表示される。既知の完全一致パターンに限り EN/JA に分割する。
_BILINGUAL_EXACT: dict[str, tuple[str, str]] = {
    "Not established in this species 本種では確立されていない": (
        "Not established in this species",
        "本種では確立されていない",
    ),
}


def fill_missing_dosage_ja(drugs: list[dict[str, Any]]) -> int:
    """DRUGS 内で dosage はあるが dosage_ja が欠落したエントリを決定論的に補完。

    補完できた species_info エントリ数を返す。既存の dosage_ja は保持。
    既知の英日併記文字列（``_BILINGUAL_EXACT``）は EN/JA の両フィールドに分割する。
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
            pair = _BILINGUAL_EXACT.get(dosage.strip())
            if pair:
                info["dosage"], info["dosage_ja"] = pair
                filled += 1
                continue
            ja = localize_dosage(dosage)
            if ja:
                info["dosage_ja"] = ja
                filled += 1
    return filled
