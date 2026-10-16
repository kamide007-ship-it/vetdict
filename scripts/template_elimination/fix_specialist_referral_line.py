"""2026-10 第71弾: 汎用ワークアップ・テンプレートの「専門医紹介」行の是正。

fallback_generator の general クラスが全種に
「複雑症例は{種}専門医（ACZMまたはAVMAエキゾチック分科会等）に紹介を検討。」
を出力していた。ACZM は動物園動物医学の専門医団体で犬・猫・馬には誤り、
「AVMAエキゾチック分科会」は実在しない組織名。種ごとに正しい専門医制度に置換する:
  - 犬・猫: 各分野の専門医（ACVIM/ECVIM 内科・循環器・腫瘍、ACVD 皮膚、
    ACVS 外科 等）
  - 馬: 馬の専門医（ACVIM 大動物内科・ACVS 大動物外科、ECEIM 等）
  - 鳥類: ABVP（Avian Practice）または ECZM（Avian）
  - 爬虫類・両生類・魚: ABVP（Reptile & Amphibian）または ECZM（Herpetology）
  - 小型哺乳類・その他: ABVP（Exotic Companion Mammal）または ECZM（Small Mammal）

用法: python3 -m scripts.template_elimination.fix_specialist_referral_line [--apply]
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OLD_RE = re.compile(r"複雑症例は([^。（]*?)専門医（ACZMまたはAVMAエキゾチック分科会等）に紹介を検討。")

_SPECIES_KEY = {
    "dog": "small",
    "cat": "small",
    "horse": "equine",
    "bird": "avian",
    "parakeet": "avian",
    "parrot": "avian",
    "reptile": "herp",
    "tortoise": "herp",
    "snake": "herp",
    "lizard": "herp",
    "amphibian": "herp",
    "fish": "herp",
    "rabbit": "mammal",
    "hamster": "mammal",
    "guinea_pig": "mammal",
    "chinchilla": "mammal",
    "ferret": "mammal",
    "hedgehog": "mammal",
    "sugar_glider": "mammal",
    "degu": "mammal",
}

_LINES = {
    "small": "複雑症例は各分野の専門医（ACVIM/ECVIM 内科・循環器・腫瘍、ACVD 皮膚科、ACVS 外科 等）への紹介を検討。",
    "equine": "複雑症例は馬の専門医（ACVIM 大動物内科・ACVS 大動物外科・ECEIM 等）への紹介を検討。",
    "avian": "複雑症例は鳥類の専門医（ABVP Avian Practice・ECZM Avian）への紹介を検討。",
    "herp": "複雑症例は爬虫類・両生類の専門医（ABVP Reptile & Amphibian・ECZM Herpetology）への紹介を検討。",
    "mammal": "複雑症例はエキゾチック哺乳類の専門医（ABVP Exotic Companion Mammal・ECZM Small Mammal）への紹介を検討。",
    "exotic": "複雑症例はエキゾチック動物の専門医（ABVP Exotic Companion Mammal / Avian / Reptile & Amphibian・ECZM）への紹介を検討。",
}

_JA_TO_KEY = {
    "犬": "small",
    "猫": "small",
    "馬": "equine",
    "鳥": "avian",
    "インコ": "avian",
    "オウム": "avian",
    "鳥類": "avian",
    "ウサギ": "mammal",
    "ハムスター": "mammal",
    "モルモット": "mammal",
    "チンチラ": "mammal",
    "フェレット": "mammal",
    "ハリネズミ": "mammal",
    "フクロモモンガ": "mammal",
    "デグー": "mammal",
    "爬虫類": "herp",
    "リクガメ": "herp",
    "ヘビ": "herp",
    "トカゲ": "herp",
    "両生類": "herp",
    "魚": "herp",
}


def referral_line(species: str) -> str:
    key = _SPECIES_KEY.get((species or "").lower().replace(" ", "_"), "exotic")
    return _LINES[key]


def _sub_by_ja_species(text: str) -> str:
    def rep(m: re.Match) -> str:
        return _LINES[_JA_TO_KEY.get(m.group(1).strip(), "exotic")]

    return OLD_RE.sub(rep, text)


def fix_obj(obj, species: str) -> int:
    """Rewrite every string field of a JSON record in place; return count."""
    n = 0
    for k, v in list(obj.items()):
        if isinstance(v, str) and OLD_RE.search(v):
            obj[k] = OLD_RE.sub(referral_line(species), v)
            n += 1
    return n


def main(apply: bool) -> None:
    total = 0
    p = ROOT / "diseases_all_species.json"
    raw = p.read_text(encoding="utf-8")
    data = json.loads(raw)
    for d in data:
        total += fix_obj(d, d.get("species", ""))
    if apply:
        p.write_text(
            json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ("\n" if raw.endswith("\n") else ""),
            encoding="utf-8",
        )
    files = list((ROOT / "api" / "species").glob("*_diseases.py")) + list(
        (ROOT / "api" / "data" / "treatment_overrides").glob("*.json")
    )
    for f in files:
        s = f.read_text(encoding="utf-8")
        new = _sub_by_ja_species(s)
        if new != s:
            total += len(OLD_RE.findall(s))
            if apply:
                f.write_text(new, encoding="utf-8")
    print(("applied" if apply else "dry-run"), total)


if __name__ == "__main__":
    main("--apply" in sys.argv)
