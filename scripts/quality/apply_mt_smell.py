"""Apply the SAFE machine-translation-smell fixes to disease sources (T109).

Only the ``safe`` entries of the curated T109 lexicon (pure typo / orthography
fixes that never change clinical meaning — e.g. 葡萄糖→ブドウ糖, 並発→併発,
疲出→疲弊) are applied. The ``review`` entries (context-dependent, meaning may
change — e.g. 遺伝学的, 貧弱な) are only REPORTED, never auto-replaced.

These terms are Japanese medical strings that appear only inside data string
literals (never in code/identifiers), so a file-level replace is safe. Edits the
JSON overlays and the Python species modules in place, backing each changed file
up to ``backups/<UTC>/`` first. Idempotent (a second run changes nothing).
"""

from __future__ import annotations

import argparse
import shutil
from datetime import datetime, timezone
from pathlib import Path

import scripts.quality.detect as detect

ROOT = Path(__file__).resolve().parents[2]

_TARGETS = [
    ROOT / "diseases_all_species.json",
    ROOT / "api" / "data" / "supplementary_diseases.json",
    *sorted((ROOT / "api" / "species").glob("*_diseases.py")),
]


def _safe_pairs() -> list[tuple[str, str]]:
    return [(e["term"], e["suggest"]) for e in detect._MT_LEXICON if e["category"] == "safe"]


def _review_terms() -> list[dict]:
    return [e for e in detect._MT_LEXICON if e["category"] != "safe"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="write changes (otherwise dry-run)")
    args = ap.parse_args()

    pairs = _safe_pairs()
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H%M")
    bak = ROOT / "backups" / stamp
    total_changes = 0
    changed_files = 0

    for path in _TARGETS:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        new = text
        file_changes = 0
        for term, suggest in pairs:
            # suggest may be "A / B"; use the first canonical form.
            repl = suggest.split("/")[0].strip()
            c = new.count(term)
            if c:
                new = new.replace(term, repl)
                file_changes += c
        if file_changes and new != text:
            total_changes += file_changes
            changed_files += 1
            print(f"{path.relative_to(ROOT)}: {file_changes} replacement(s)")
            if args.apply:
                bak.mkdir(parents=True, exist_ok=True)
                shutil.copy2(path, bak / path.name)
                path.write_text(new, encoding="utf-8")

    print(f"\nSAFE fixes: {total_changes} occurrence(s) across {changed_files} file(s).")
    if args.apply and changed_files:
        print(f"backups -> {bak.relative_to(ROOT)}/")
    elif not args.apply:
        print("(dry-run — pass --apply to write)")

    # Report review-only terms (never auto-applied).
    print("\nREVIEW terms (NOT applied — veterinarian to decide per context):")
    for e in _review_terms():
        n = 0
        for path in _TARGETS:
            if path.exists():
                n += path.read_text(encoding="utf-8").count(e["term"])
        print(f"  {e['term']} -> {e['suggest']}  occurrences={n}  ({e['note']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
