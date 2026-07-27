#!/usr/bin/env python3
"""Turn the dosage-gap report into per-species fill-in sheets for the vet.

Writes ``api/data/dosage_overrides/<species>.json`` with one entry per gap, every
value blank and ``review_status: draft``. Filling in ``dosage`` + ``source`` and
flipping ``review_status`` to ``published`` is what puts a dose on the site —
see ``api/drug_dosage_overrides.py`` for the fail-closed gate.

Idempotent: re-running preserves anything already filled in and only adds gaps
that are not yet listed, so it can be re-run after the detector picks up new
gaps without clobbering the vet's work.

Usage:
    python3 scripts/quality/build_dosage_worklist.py            # dry run
    python3 scripts/quality/build_dosage_worklist.py --apply
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

OUT_DIR = REPO_ROOT / "api" / "data" / "dosage_overrides"

_NOTE = (
    "獣医師記入用。dosage と source を埋め、review_status を published にした行だけが配信される"
    "（api/drug_dosage_overrides.py の fail-closed ゲート）。source が空のまま published にしても配信されない。"
    "evidence_grade: A=当該種の一次文献 / B=近縁種からの外挿 / C=フォーミュラリの経験的用量。"
)


def _load_pubmed(path: Path) -> dict[tuple[str, str], dict[str, Any]]:
    if not path.is_file():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return {(r["drug"], r["species"]): r for r in payload.get("results", [])}


def main() -> int:
    ap = argparse.ArgumentParser(description="Build vet fill-in sheets for dosage gaps")
    ap.add_argument("--gaps", default="reports/quality/_dosage_gaps.json")
    ap.add_argument("--pubmed", default="reports/quality/_dosage_pubmed.json")
    ap.add_argument("--apply", action="store_true", help="write the files (otherwise dry-run)")
    args = ap.parse_args()

    gaps = json.loads((REPO_ROOT / args.gaps).read_text(encoding="utf-8"))["gaps"]
    pubmed = _load_pubmed(REPO_ROOT / args.pubmed)

    by_species: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for gap in gaps:
        candidate = pubmed.get((gap["drug"], gap["species"])) or {}
        by_species[gap["species"]].append(
            {
                "drug_id": gap["drug_id"],
                "drug": gap["drug"],
                "species": gap["species"],
                "current_dosage": gap["dosage"],
                "missing": [
                    k for k, v in (("route", gap["missing_route"]), ("frequency", gap["missing_frequency"])) if v
                ],
                # Vet fills these:
                "dosage": "",
                "dosage_ja": "",
                "source": "",
                "evidence_grade": "",
                "review_status": "draft",
                # Research aid only — a PMID here is a candidate to read, never a dose.
                "pubmed_candidates": (candidate.get("pmids") or [])[:3],
                "pubmed_hits": candidate.get("hits"),
            }
        )

    written = 0
    for species, entries in sorted(by_species.items()):
        path = OUT_DIR / f"{species}.json"
        existing_by_key: dict[tuple[str, str], dict[str, Any]] = {}
        if path.is_file():
            try:
                for old in json.loads(path.read_text(encoding="utf-8")).get("entries", []):
                    existing_by_key[(old.get("drug_id"), old.get("species"))] = old
            except (OSError, json.JSONDecodeError):
                pass

        merged = []
        for entry in entries:
            old = existing_by_key.get((entry["drug_id"], entry["species"]))
            # Never clobber vet-entered values on a re-run.
            merged.append(old if old and (old.get("dosage") or old.get("source")) else entry)

        payload = {
            "species": species,
            "schema_version": 1,
            "note": _NOTE,
            "counts": {"total": len(merged), "filled": sum(1 for e in merged if e.get("dosage"))},
            "entries": merged,
        }
        if args.apply:
            OUT_DIR.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        written += len(merged)
        print(f"  {species:14} {len(merged):3} entries")

    print(f"\n{'wrote' if args.apply else 'would write'} {written} entries across {len(by_species)} species")
    if not args.apply:
        print("(dry run — pass --apply to write)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
