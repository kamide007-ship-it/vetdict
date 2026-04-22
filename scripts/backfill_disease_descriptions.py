"""疾患エントリの description_ja / description を既存フィールドから補完するスクリプト。

対象:
1. 5,039件: description_ja が完全に空のエントリ
2. 197件: 「○○は{種}に影響を与える○○疾患です。早期診断と…」形式のテンプレート description_ja
3. 945件: 60文字未満の極端に短い description_ja

抽出ロジック:
- pathophysiology_ja から最初の1-2文を抽出（80-260字）
- pathophysiology_ja が無い場合は clinical_signs_ja + treatment_ja から要約を合成
- 既存の良質な description_ja は維持

獣医師が即座に疾患概要を把握できる「臨床メモ」として読める粒度を目指す。
"""

from __future__ import annotations

import json
import re
import shutil
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JSON_PATH = ROOT / "diseases_all_species.json"

# ---------- テンプレート検出 ----------
DESCRIPTION_TEMPLATE_PATTERNS = (
    "は犬に影響を与える",
    "は猫に影響を与える",
    "は馬に影響を与える",
    "は鳥に影響を与える",
    "はウサギに影響を与える",
    "はうさぎに影響を与える",
    "はハムスターに影響を与える",
    "は爬虫類に影響を与える",
    "はフェレットに影響を与える",
    "は両生類に影響を与える",
    "は魚に影響を与える",
    "はトカゲに影響を与える",
    "はヘビに影響を与える",
    "はリクガメに影響を与える",
    "はインコに影響を与える",
    "はオウムに影響を与える",
    "はモルモットに影響を与える",
    "はチンチラに影響を与える",
    "はデグーに影響を与える",
    "はハリネズミに影響を与える",
    "はフクロモモンガに影響を与える",
    "は他のエキゾチックに影響を与える",
    "早期診断と適切な獣医学的管理が重要",
    "早期発見と治療が重要です",
)

# clinical_signs_ja のテンプレート（参考用）
CLINICAL_SIGNS_TEMPLATE_FRAGMENTS = (
    "臨床兆候は疾患の種類により異なる",
    "臨床兆候は重症度と病期により異なる",
)


def is_template_description(text: str | None) -> bool:
    if not text:
        return False
    return any(p in text for p in DESCRIPTION_TEMPLATE_PATTERNS)


def needs_backfill(entry: dict) -> bool:
    desc = entry.get("description_ja") or ""
    if not desc.strip():
        return True
    if is_template_description(desc):
        return True
    if len(desc) < 60:  # 短すぎるエントリも対象
        return True
    return False


# ---------- 文章抽出ロジック ----------

JA_SENTENCE_RE = re.compile(r"(?<=。)")


def split_sentences(text: str) -> list[str]:
    if not text:
        return []
    parts = JA_SENTENCE_RE.split(text.strip())
    return [p.strip() for p in parts if p.strip()]


def extract_summary(
    text: str | None,
    *,
    min_chars: int = 70,
    max_chars: int = 260,
) -> str:
    """先頭から1-2文を抽出して短く整形した要約を返す。"""
    if not text:
        return ""
    text = text.strip()
    if not text:
        return ""

    sentences = split_sentences(text)
    if not sentences:
        return text[:max_chars].rstrip()

    out = ""
    for sentence in sentences:
        candidate = (out + sentence).strip()
        if len(candidate) > max_chars:
            if out and len(out) >= min_chars:
                return out
            # 1文目だけで上限超過 → 上限で切って末尾に「…」
            return candidate[: max_chars - 1].rstrip() + "…"
        out = candidate
        if len(out) >= min_chars and out.endswith("。"):
            return out
    return out


def is_template_pathophysiology(text: str | None) -> bool:
    """pathophysiology_ja のテンプレ判定（生成用に避けるべきもの）。"""
    if not text:
        return False
    # Very generic templates we want to avoid using as descriptions verbatim
    bad_fragments = (
        "の臨床兆候は重症度と病期により異なる",
        "に発生する疾患または状態",
        "早期診断と適切な獣医学的管理が重要",
    )
    if any(f in text for f in bad_fragments):
        return True
    # description テンプレが pathophysiology にも入っているケース
    return is_template_description(text)


def is_template_clinical_signs(text: str | None) -> bool:
    if not text:
        return False
    return any(f in text for f in CLINICAL_SIGNS_TEMPLATE_FRAGMENTS)


_SPECIES_JA_MAP = {
    "Dog": "犬",
    "Cat": "猫",
    "Horse": "馬",
    "Rabbit": "ウサギ",
    "Hamster": "ハムスター",
    "Guinea Pig": "モルモット",
    "Chinchilla": "チンチラ",
    "Ferret": "フェレット",
    "Hedgehog": "ハリネズミ",
    "Sugar Glider": "フクロモモンガ",
    "Degu": "デグー",
    "Bird": "鳥",
    "Parakeet": "インコ",
    "Parrot": "オウム",
    "Reptile": "爬虫類",
    "Tortoise": "リクガメ",
    "Snake": "ヘビ",
    "Lizard": "トカゲ",
    "Amphibian": "両生類",
    "Fish": "魚",
    "Exotic Other": "エキゾチックアニマル",
    "Multiple": "複数種",
    "Cattle": "牛",
    "Sheep": "羊",
    "Goat": "ヤギ",
    "Pig": "豚",
}


def _species_ja(species: str | None) -> str:
    if not species:
        return "対象動物"
    return _SPECIES_JA_MAP.get(species, species)


def is_template_causes(text: str | None) -> bool:
    if not text:
        return False
    fragments = (
        "の原因は多因子性であり、遺伝的素因、環境要因、感染性要因、栄養要因",
        "創傷汚染、経口摂取、吸入、日和見的過剰増殖",
        "の原因: 卵・幼虫・中間宿主の経口摂取、経皮的侵入、ベクター媒介伝播",
    )
    return any(f in text for f in fragments)


def is_template_treatment(text: str | None) -> bool:
    if not text:
        return False
    fragments = (
        "の治療は基礎となるホルモン・代謝異常を標的とする",
        "の治療には、同定された寄生虫に応じた適切な駆虫薬",
        "ウイルス感染症には特異的抗ウイルス薬がない",
    )
    return any(f in text for f in fragments)


def build_synth_description(entry: dict) -> str:
    """pathophysiology_ja が無いエントリ向けの簡易合成。"""
    name = (entry.get("name_ja") or "").strip()
    species_ja = _species_ja(entry.get("species"))

    parts: list[str] = []

    causes = entry.get("causes_ja") or ""
    if causes and not is_template_pathophysiology(causes) and not is_template_causes(causes):
        causes_summary = extract_summary(causes, min_chars=50, max_chars=160)
        if causes_summary:
            parts.append(causes_summary)

    signs = entry.get("clinical_signs_ja") or ""
    if signs and not is_template_clinical_signs(signs):
        # 主要徴候のみ抜粋（先頭3つ）
        items = re.split(r"[；;、,]", signs)
        items = [i.strip() for i in items if i.strip()]
        if items:
            top = "・".join(items[:3])
            parts.append(f"主要な臨床徴候は{top}など。")

    treatment = entry.get("treatment_ja") or ""
    if treatment and not is_template_treatment(treatment):
        # 治療の要点（先頭フレーズのみ）
        first_treatment = extract_summary(treatment, min_chars=40, max_chars=140)
        if first_treatment:
            parts.append(first_treatment)

    if not parts:
        return ""

    intro = f"{name}は{species_ja}にみられる疾患である。" if name else ""
    body = "".join(parts)
    full = (intro + body).strip()
    return full[:300].rstrip()


def derive_description_ja(entry: dict) -> str | None:
    """description_ja を新規生成または改善して返す。生成不能なら None。"""
    patho = entry.get("pathophysiology_ja") or ""
    if patho and not is_template_pathophysiology(patho):
        candidate = extract_summary(patho, min_chars=60, max_chars=260)
        if len(candidate) >= 35:
            # 本文が短い場合は名前と種を冒頭に補完して文脈を明確化
            if len(candidate) < 60:
                name = (entry.get("name_ja") or "").strip()
                species_ja = _species_ja(entry.get("species"))
                if name and species_ja:
                    candidate = f"{name}は{species_ja}にみられる疾患である。{candidate}"
            return candidate

    synth = build_synth_description(entry)
    if synth and len(synth) >= 35:
        return synth

    # 最終フォールバック: 名前と種から構成
    name = (entry.get("name_ja") or "").strip()
    species_ja = _species_ja(entry.get("species"))
    treatment = entry.get("treatment_ja") or ""
    if name and species_ja:
        base = f"{name}は{species_ja}に発生する疾患である。"
        if treatment and not is_template_treatment(treatment):
            tail = extract_summary(treatment, min_chars=30, max_chars=140)
            return base + tail if tail else base + "獣医師による診断と種特異的な治療管理が必要である。"
        return base + "獣医師による診断と種特異的な治療管理が必要である。"
    return None


# ---------- メインフロー ----------


def main() -> None:
    data = json.loads(JSON_PATH.read_text(encoding="utf-8"))

    # バックアップ
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    backup_path = JSON_PATH.with_suffix(f".json.backup_{timestamp}_pre_desc_backfill")
    if not backup_path.exists():
        shutil.copy2(JSON_PATH, backup_path)
        print(f"backup written: {backup_path.name}")

    stats = {
        "total": len(data),
        "needed": 0,
        "filled_from_patho": 0,
        "filled_from_synth": 0,
        "still_missing": 0,
        "templates_replaced": 0,
        "short_replaced": 0,
        "null_filled": 0,
    }

    for entry in data:
        original = entry.get("description_ja") or ""
        if not needs_backfill(entry):
            continue
        stats["needed"] += 1

        # 分類カウンタ
        if not original.strip():
            stats["null_filled"] += 1
        elif is_template_description(original):
            stats["templates_replaced"] += 1
        elif len(original) < 60:
            stats["short_replaced"] += 1

        new_desc = derive_description_ja(entry)
        if new_desc is None:
            stats["still_missing"] += 1
            continue

        # 出典トラッキング
        if entry.get("pathophysiology_ja") and not is_template_pathophysiology(entry["pathophysiology_ja"]):
            stats["filled_from_patho"] += 1
        else:
            stats["filled_from_synth"] += 1

        entry["description_ja"] = new_desc
        entry.setdefault("enrichment_phase", 2)
        entry["description_backfilled_at"] = datetime.utcnow().isoformat()

    # 書き出し
    JSON_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("=== description_ja backfill ===")
    for k, v in stats.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
