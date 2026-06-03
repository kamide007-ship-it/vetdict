"""One-shot repair: fix the garbled phrase "single-agent修正治療" in neoplasia content.

The phrase "single-agent修正治療を施行" was emitted by the fallback generator's
neoplasia branch (now fixed in fallback_generator.py). It is medically nonsense:
"single-agent revision/correction treatment" does not describe wide-margin surgical
resection, which is the actual clinical intent of the surrounding sentence.

This script performs a controlled in-place replacement across:
- ``diseases_all_species.json``
- ``api/species/*_diseases.py``

The replacement preserves the surrounding sentence structure and produces
clinically correct language (wide-margin resection guidance).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


OLD_PHRASES = [
    # Original garbled fallback-generator output (full sentence)
    "外科的完全切除が可能ならsingle-agent修正治療を施行（マージン3-5cm目安、種・部位で調整）。",
    # Defensive: any standalone occurrence of the typo
]

NEW_SENTENCE = "外科的完全切除が可能なら広範マージン外科的切除を第一選択（推奨マージン2-3cm、攻撃的肉腫・MCT高グレードは3-5cm、種・部位・組織型で調整）。"

# Defensive replacement for the bare malformed token (in case it ever appears outside the
# full sentence above — protects against partial edits).
BARE_OLD = "single-agent修正治療を施行"
BARE_NEW = "広範マージン外科的切除を第一選択"

# Also update the next-sentence template that previously said "切除不能例・残存例には化学療法（プロトコルは腫瘍型別）または緩和的放射線療法。"
# to give specific protocol hints.
OLD_NEXT = "切除不能例・残存例には化学療法（プロトコルは腫瘍型別）または緩和的放射線療法。"
NEW_NEXT = "切除不能例・残存例には化学療法（プロトコルは腫瘍型別、リンパ腫はCHOP、肥満細胞腫はビンブラスチン+プレドニゾロン等）または緩和的放射線療法。"


def _apply_replacements(text: str) -> tuple[str, int]:
    n = 0
    for old in OLD_PHRASES:
        if old in text:
            n += text.count(old)
            text = text.replace(old, NEW_SENTENCE)
    # Bare-token fallback
    if BARE_OLD in text:
        n += text.count(BARE_OLD)
        text = text.replace(BARE_OLD, BARE_NEW)
    if OLD_NEXT in text:
        # Only upgrade when next-sentence template is unmodified
        n += text.count(OLD_NEXT)
        text = text.replace(OLD_NEXT, NEW_NEXT)
    return text, n


def fix_json(path: Path) -> int:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    total = 0
    for entry in data:
        for fld in ("treatment_ja", "treatment", "prognosis_ja", "causes_ja"):
            v = entry.get(fld)
            if not isinstance(v, str):
                continue
            new_v, n = _apply_replacements(v)
            if n:
                entry[fld] = new_v
                total += n
    if total:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    return total


def fix_python_modules(species_dir: Path) -> int:
    total = 0
    for p in sorted(species_dir.glob("*_diseases.py")):
        text = p.read_text(encoding="utf-8")
        new_text, n = _apply_replacements(text)
        if n:
            p.write_text(new_text, encoding="utf-8")
            print(f"  {p.name}: {n} fixes")
            total += n
    return total


def main() -> int:
    print("Fixing garbled neoplasia phrase across data files…")
    json_path = ROOT / "diseases_all_species.json"
    json_n = fix_json(json_path)
    print(f"  {json_path.name}: {json_n} fixes")
    py_n = fix_python_modules(ROOT / "api" / "species")
    print(f"Total: {json_n + py_n} replacements")
    return 0


if __name__ == "__main__":
    sys.exit(main())
