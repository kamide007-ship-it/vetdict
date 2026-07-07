"""Run VetDict quality detectors for one or more species and write a report.

READ-ONLY. Produces:
  reports/quality/<species>-<UTC-timestamp>.json   (machine-readable findings)
  reports/quality/<species>-<UTC-timestamp>.md      (human review sheet)

Usage:
  python3 scripts/quality/run_detectors.py degu
  python3 scripts/quality/run_detectors.py degu cat rabbit

This script never mutates disease sources. It only reads the served view and
writes report files under reports/quality/.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.quality.detectors import run_all  # noqa: E402

REPORT_DIR = Path(__file__).resolve().parents[2] / "reports" / "quality"


def _md(report: dict) -> str:
    sp = report["species"]
    n = report["n_records"]
    dup = report["T101_duplicates"]
    nc = report["T102_nonclinical"]
    et = report["T104_empty_treatment"]

    lines: list[str] = []
    lines.append(f"# VetDict quality report — {sp} ({n} served diseases)")
    lines.append("")
    lines.append("> READ-ONLY detector output. No data was modified. For veterinarian review.")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(
        f"- **T101 exact-duplicate records:** {dup['n_exact_duplicate_records']} "
        f"in {len(dup['exact_duplicate_clusters'])} clusters"
    )
    lines.append(f"- **T101 split-family clusters (≥3):** {dup['n_split_family_clusters']}")
    lines.append(f"- **T102 non-clinical / transplant flags:** {nc['n_flagged']}")
    lines.append(
        f"- **T104 treatment w/o JA dosage:** {et['n_flagged']} "
        f"(fully empty JA: {et['n_ja_empty']}; no dose in either lang: {et['n_no_dose_either']})"
    )
    lines.append("")

    lines.append("## T101 — Exact-duplicate name clusters")
    lines.append("")
    if dup["exact_duplicate_clusters"]:
        for c in dup["exact_duplicate_clusters"]:
            names = "; ".join(f"{m['name_ja']} / {m['name']}" for m in c["members"])
            lines.append(f"- **×{c['count']}** `{c['key']}` → {names}")
    else:
        lines.append("_none_")
    lines.append("")

    lines.append("## T101 — Split-family clusters (shared clinical stem, ≥3 entries)")
    lines.append("")
    lines.append("_Review signal only — families often contain genuinely distinct entities._")
    lines.append("")
    for c in dup["split_family_clusters"]:
        names = "; ".join(m["name_ja"] or m["name"] for m in c["members"])
        lines.append(f"- **{c['stem']}** ×{c['count']}: {names}")
    lines.append("")

    lines.append("## T102 — Non-clinical / research-model / human-medicine transplants")
    lines.append("")
    if nc["flagged"]:
        for f in nc["flagged"]:
            lines.append(f"- {f['name_ja']} / {f['name']} — flags: {', '.join(f['flags'])}")
    else:
        lines.append("_none_")
    lines.append("")

    lines.append("## T104 — Treatment sections without a dosage pattern")
    lines.append("")
    lines.append("| name_ja | name | severity | JA len | EN has dose |")
    lines.append("|---|---|---|---|---|")
    for f in et["flagged"]:
        lines.append(f"| {f['name_ja']} | {f['name']} | {f['severity']} | {f['ja_len']} | {f['en_has_dose']} |")
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    species_list = argv or ["degu"]
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M")

    for sp in species_list:
        report = run_all(sp)
        json_path = REPORT_DIR / f"{sp}-{stamp}.json"
        md_path = REPORT_DIR / f"{sp}-{stamp}.md"
        json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        md_path.write_text(_md(report), encoding="utf-8")

        d = report["T101_duplicates"]
        print(
            f"[{sp}] {report['n_records']} diseases | "
            f"exact-dup records={d['n_exact_duplicate_records']} "
            f"split-families={d['n_split_family_clusters']} | "
            f"nonclinical={report['T102_nonclinical']['n_flagged']} | "
            f"no-dose-tx={report['T104_empty_treatment']['n_flagged']}"
        )
        print(f"       -> {json_path.relative_to(REPORT_DIR.parents[1])}")
        print(f"       -> {md_path.relative_to(REPORT_DIR.parents[1])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
