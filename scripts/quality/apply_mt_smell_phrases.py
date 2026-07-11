"""Apply PHRASE-level machine-translation-smell fixes (T109, curated).

The T109 lexicon flags some terms as ``review`` because the same token is right
in one context and wrong in another — e.g. ``遺伝学的`` is correct in
``遺伝学的スクリーニング`` (genetic screening) but wrong in
``遺伝学的インスリン抵抗`` (should be ``遺伝的``). A bare term replace is therefore
unsafe. This script fixes only the specific WRONG PHRASES, leaving the valid
uses of the same token untouched, so every replacement preserves clinical
meaning (it corrects a mistranslated word choice, never a concept).

Fixed phrases (all meaning-preserving corrections of clear MT errors):
    遺伝学的インスリン抵抗 -> 遺伝的インスリン抵抗
    遺伝学的素因           -> 遺伝的素因
    遺伝学的易感受性       -> 遺伝的易感受性
    遺伝学的疾患           -> 遺伝性疾患
    細胞失敗               -> 細胞不全        (β cell "failure" mistranslation)
    可遺伝                 -> 遺伝性

Deliberately NOT touched (valid or defensible, left for veterinarian review):
    遺伝学的スクリーニング / 遺伝学的検査 / 遺伝学的背景 / 遺伝学的異常
    易感受性 / 貧弱な  (stylistic MT-smell, no clinical error)

Edits the JSON overlays and the Python species modules in place, backing each
changed file up to ``backups/<UTC>/`` first. Idempotent (a second run is a
no-op). Dry-run by default; pass ``--apply`` to write.
"""

from __future__ import annotations

import argparse
import shutil
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

_TARGETS = [
    ROOT / "diseases_all_species.json",
    ROOT / "api" / "data" / "supplementary_diseases.json",
    *sorted((ROOT / "api" / "species").glob("*_diseases.py")),
]

# Ordered so the most specific phrase is replaced before any shorter substring.
_PHRASE_FIXES: list[tuple[str, str]] = [
    ("遺伝学的インスリン抵抗", "遺伝的インスリン抵抗"),
    ("遺伝学的易感受性", "遺伝的易感受性"),
    ("遺伝学的素因", "遺伝的素因"),
    ("遺伝学的疾患", "遺伝性疾患"),
    ("細胞失敗", "細胞不全"),
    ("可遺伝", "遺伝性"),
    # Vet-approved stylistic MT-smell fixes (T109 review terms, degu 糖尿病).
    # Ordered: the 遺伝的 compound is fixed before the bare 易感受性 cases, and
    # the 産科ショック idiom before the generic ones. 遺伝学的スクリーニング /
    # 検査 / 背景 / 異常 are legitimate terms and are never matched here.
    ("遺伝的易感受性", "遺伝的に感受性が高い"),
    ("産科ショック易感受性を示す", "産科ショックへの高い感受性を示す"),
    ("易感受性動物", "感受性が高い動物"),
    ("易感受性デグー", "感受性が高いデグー"),
    ("易感受性個体", "感受性が高い個体"),
    ("貧弱な耐性", "乏しい耐性"),
]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="write changes (otherwise dry-run)")
    args = ap.parse_args()

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H%M")
    bak = ROOT / "backups" / stamp
    total = 0
    changed_files = 0

    for path in _TARGETS:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        new = text
        n = 0
        for wrong, right in _PHRASE_FIXES:
            c = new.count(wrong)
            if c:
                new = new.replace(wrong, right)
                n += c
        if n and new != text:
            print(f"{path.relative_to(ROOT)}: {n} replacement(s)")
            total += n
            changed_files += 1
            if args.apply:
                bak.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, bak / path.name)
                path.write_text(new, encoding="utf-8")

    verb = "applied" if args.apply else "would apply"
    print(f"\n{verb}: {total} replacement(s) across {changed_files} file(s).")
    if not args.apply:
        print("(dry-run — pass --apply to write)")
    elif changed_files:
        print(f"backups -> {bak}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
