"""Localise English species names that leaked into Japanese clinical fields.

Some template-generated Japanese fields still contain the *English* species
placeholder, e.g. ``Hamsterにおける粘着眼`` or ``心血管系行動障害（Cat）はCatに
おける行動疾患である``. To a Japanese-reading clinician these are an obvious
broken-localisation tell. This pass rewrites an English species token to its
Japanese name wherever it is unambiguously the species placeholder — i.e. it is
immediately followed by a Japanese particle (に・の・は・を・における・にみられる)
or wrapped in full-width/half-width parentheses.

Run with::

    python3 scripts/template_elimination/fix_english_species_in_ja.py --apply

Then regenerate the delivery DB with ``python3 scripts/migrate_to_sqlite.py``.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
JSON_PATH = ROOT / "diseases_all_species.json"

# Longest names first so "Guinea Pig" matches before "Pig" etc.
EN_TO_JA = {
    "Guinea Pig": "モルモット",
    "Sugar Glider": "フクロモモンガ",
    "Exotic Other": "その他",
    "Hedgehog": "ハリネズミ",
    "Chinchilla": "チンチラ",
    "Parakeet": "インコ",
    "Hamster": "ハムスター",
    "Tortoise": "リクガメ",
    "Amphibian": "両生類",
    "Reptile": "爬虫類",
    "Rabbit": "ウサギ",
    "Ferret": "フェレット",
    "Parrot": "オウム",
    "Lizard": "トカゲ",
    "Horse": "馬",
    "Snake": "ヘビ",
    "Degu": "デグー",
    "Bird": "鳥",
    "Cat": "猫",
    "Dog": "犬",
}

# 小文字・snake_case の内部種ID（"hamsterにおける" / "guinea_pigの" 等）も
# プレースホルダとして漏れることがあるため、同じ日本語名に解決する。
# "Fish" は従来マップに欠落していたため大文字・小文字とも追加。
EN_TO_JA.update({"Fish": "魚"})
EN_TO_JA.update(
    {k.lower().replace(" ", "_"): v for k, v in list(EN_TO_JA.items()) if k.lower().replace(" ", "_") not in EN_TO_JA}
)

_NAMES = sorted(EN_TO_JA, key=len, reverse=True)
_ALT = "|".join(re.escape(n) for n in _NAMES)

# English species token directly followed by a Japanese particle. The species
# placeholder is a standalone token, so reject matches preceded by another
# English word + space ("Quarter Horse", "American Paint Horse") or any letter,
# which are breed/proper names rather than the species placeholder.
_PARTICLE = re.compile(
    rf"(?<![A-Za-z])(?<![A-Za-z]\s)(?P<sp>{_ALT})(?=(に|の|は|を|では|における|にみられる|に発症|に好発))"
)
# English species token wrapped in parentheses.
_PAREN = re.compile(rf"[（(](?P<sp>{_ALT})[）)]")

# Japanese disease *name* tag plus all Japanese content fields. ``name_ja`` is
# included because the supplementary-disease records tag the localized name with
# the English species (e.g. ``Bsal感染症（Amphibian）``), which is shown directly
# in the database browser.
JA_FIELDS = (
    "name_ja",
    "description_ja",
    "treatment_ja",
    "prognosis_ja",
    "causes_ja",
    "pathophysiology_ja",
    "clinical_signs_ja",
    "prevention_ja",
    "diagnosis_ja",
    "transmission_ja",
    "differential_diagnosis_ja",
    "nutrition_management_ja",
    "prognosis_detailed_ja",
    "rehabilitation_protocol_ja",
)

SUPPLEMENTARY_PATH = ROOT / "api" / "data" / "supplementary_diseases.json"


def localise(text: str) -> tuple[str, int]:
    n = 0

    def _p(m: re.Match) -> str:
        nonlocal n
        n += 1
        return EN_TO_JA[m.group("sp")]

    def _pp(m: re.Match) -> str:
        nonlocal n
        n += 1
        return f"（{EN_TO_JA[m.group('sp')]}）"

    text = _PARTICLE.sub(_p, text)
    text = _PAREN.sub(_pp, text)
    return text, n


def process_file(path: Path, apply: bool) -> int:
    records = json.loads(path.read_text(encoding="utf-8"))
    field_counts: Counter[str] = Counter()
    total = 0
    samples: list[str] = []

    for r in records:
        for f in JA_FIELDS:
            v = r.get(f)
            if not v or not any(n in v for n in _NAMES):
                continue
            new, n = localise(v)
            if n:
                field_counts[f] += n
                total += n
                if len(samples) < 8:
                    samples.append(f"[{r.get('species')}] .{f}: …{new[:64]}…")
                if apply:
                    r[f] = new

    print(f"\n{path.name}: localised {total} English species tokens across {len(field_counts)} fields")
    print("  by field:", dict(field_counts.most_common()))
    for s in samples:
        print("   ", s)

    if apply and total == 0:
        # Nothing changed — do not rewrite the file. Re-serialising a file with
        # zero content changes produces a formatting-only diff of tens of
        # thousands of lines when the on-disk layout differs from json.dumps.
        return total

    if apply:
        # Preserve each file's on-disk format so the diff stays minimal:
        # diseases_all_species.json is compact, supplementary uses 2-space indent.
        if path == SUPPLEMENTARY_PATH:
            text = json.dumps(records, ensure_ascii=False, indent=2)
        else:
            text = json.dumps(records, ensure_ascii=False, separators=(",", ":"))
        path.write_text(text, encoding="utf-8")
        residual = 0
        for r in records:
            for f in JA_FIELDS:
                v = r.get(f) or ""
                residual += len(_PARTICLE.findall(v)) + len(_PAREN.findall(v))
        print(f"  residual contamination after apply: {residual}")
    return total


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    grand = process_file(JSON_PATH, args.apply)
    if SUPPLEMENTARY_PATH.exists():
        grand += process_file(SUPPLEMENTARY_PATH, args.apply)
    print(f"\nTOTAL localised: {grand}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
