#!/usr/bin/env python3
"""Run the VetDict read-only detectors across all 21 species and aggregate.

Writes per-species reports (reports/quality/<species>/) and an aggregate
summary (reports/quality/_rollout_summary.{json,md}).  READ-ONLY — never
mutates disease data.

Usage:
    python3 scripts/quality/rollout.py
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scripts.quality.detect import ALL_SPECIES, _markdown_summary, run  # noqa: E402

# Heuristic failure-guard: per SPEC, halt & report if a detector flags far more
# than expected. These are generous per-species ceilings for a read-only sweep;
# exceeding one does not stop the sweep but is surfaced prominently.
_GUARD = {
    "exact_duplicate_cluster_count": 60,
    "family_cluster_count": 80,
    "nonclinical": 30,
    "heading_only": 150,
    "drug_mismatch": 200,
    "citation_mismatch": 120,
    "mt_review": 200,
}


def main() -> int:
    ap = argparse.ArgumentParser(description="Run VetDict read-only detectors across all species")
    ap.add_argument(
        "--served",
        action="store_true",
        help="report the post-consolidation served view (dedup + canonical) instead of raw source; "
        "writes *_served reports so the raw baseline is preserved",
    )
    args = ap.parse_args()
    served = args.served
    suffix = "_served" if served else ""

    out_root = REPO_ROOT / "reports" / "quality"
    rows = []
    warnings = []
    for sp in ALL_SPECIES:
        report = run(sp, served=served)
        sp_dir = out_root / sp
        sp_dir.mkdir(parents=True, exist_ok=True)
        (sp_dir / f"detectors{suffix}.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        (sp_dir / f"detectors{suffix}.md").write_text(_markdown_summary(report), encoding="utf-8")

        t1, t2, t4, t8, t9 = (report["T101"], report["T102"], report["T104"], report["T108"], report["T109"])
        row = {
            "species": sp,
            "records": report["record_count"],
            "dup_clusters": t1["exact_duplicate_cluster_count"],
            "redundant": t1["redundant_record_count"],
            "families": t1["family_cluster_count"],
            "nonclinical": t2["flagged_count"],
            "empty_tx": t4["empty_count"],
            "heading_only_tx": t4["heading_only_count"],
            "drug_mismatch": t8["drug_mismatch_count"],
            "citation_mismatch": t8["citation_mismatch_count"],
            "drug_mismatch_residual": t8.get("drug_mismatch_residual_count", 0),
            "citation_mismatch_residual": t8.get("citation_mismatch_residual_count", 0),
            "mt_hits": t9["hit_count"],
            "mt_safe": t9["safe_occurrences"],
            "mt_review": t9["review_occurrences"],
        }
        rows.append(row)

        # failure-guard checks
        for key, ceiling in _GUARD.items():
            val = row.get(key) or row.get(
                {"nonclinical": "nonclinical", "heading_only": "heading_only_tx", "mt_review": "mt_review"}.get(
                    key, key
                ),
                0,
            )
            if val > ceiling:
                warnings.append(f"{sp}: {key}={val} exceeds guard ceiling {ceiling}")
        print(
            f"[{sp:12}] rec={row['records']:4} dup={row['dup_clusters']:3} fam={row['families']:3} "
            f"nonclin={row['nonclinical']:2} tx∅/head={row['empty_tx']}/{row['heading_only_tx']:3} "
            f"drug!={row['drug_mismatch']:3} cite!={row['citation_mismatch']:3} mt={row['mt_hits']:3}"
        )

    totals = {
        k: sum(r[k] for r in rows)
        for k in (
            "records", "dup_clusters", "redundant", "families", "nonclinical",
            "empty_tx", "heading_only_tx", "drug_mismatch", "citation_mismatch",
            "drug_mismatch_residual", "citation_mismatch_residual",
            "mt_hits", "mt_safe", "mt_review",
        )
    }  # fmt: skip

    summary = {"view": "served" if served else "raw", "species": rows, "totals": totals, "guard_warnings": warnings}
    (out_root / f"_rollout_summary{suffix}.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    view_label = (
        "統合適用後の**配信ビュー**（dedup + canonical map 適用済み＝サイトが実際に配信する状態）"
        if served
        else "**生ソース**ビュー（統合前の元データ＝問題の元規模）"
    )
    # markdown table
    md = [
        f"# VetDict 品質検出 — 全21種横展開サマリー（read-only, {'served' if served else 'raw'}）",
        "",
        f"ビュー: {view_label}。",
        "",
        f"総疾患: **{totals['records']}** / 完全重複クラスタ計: **{totals['dup_clusters']}**（冗長 {totals['redundant']}） "
        f"/ 非臨床計: **{totals['nonclinical']}** / 投与量なし治療計: **{totals['heading_only_tx']}** "
        f"/ 薬品誤リンク計: **{totals['drug_mismatch']}** / 犬猫論文誤紐付け計: **{totals['citation_mismatch']}** "
        f"/ 機械翻訳臭計: **{totals['mt_hits']}**",
        "",
        f"> **T108 種ガード適用済み**（`api/pubmed_references.py` + `api/vetdict_api.py`）。"
        f"上記の薬品誤リンク・論文誤紐付けは *未ガード時の問題規模*。"
        f"出荷済みガード適用後の残存: 薬品 **{totals['drug_mismatch_residual']}** / "
        f"論文 **{totals['citation_mismatch_residual']}**（目標0＝本番では表示されない）。",
        "",
        "| 種 | 疾患 | 重複ｸﾗｽﾀ | 冗長 | ﾌｧﾐﾘｰ候補 | 非臨床 | 空治療 | 投与量無 | 薬品誤 | 論文誤 | MT臭(safe/rev) |",
        "|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|",
    ]
    for r in rows:
        md.append(
            f"| {r['species']} | {r['records']} | {r['dup_clusters']} | {r['redundant']} | {r['families']} | "
            f"{r['nonclinical']} | {r['empty_tx']} | {r['heading_only_tx']} | {r['drug_mismatch']} | "
            f"{r['citation_mismatch']} | {r['mt_hits']} ({r['mt_safe']}/{r['mt_review']}) |"
        )
    if warnings:
        md += ["", "## ⚠️ 失敗ガード超過（要確認）", *[f"- {w}" for w in warnings]]
    else:
        md += ["", "失敗ガード（10倍相当のヒューリスティック上限）超過: **なし**"]
    (out_root / f"_rollout_summary{suffix}.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    print(
        f"\nTOTAL diseases={totals['records']} dup_clusters={totals['dup_clusters']} "
        f"nonclinical={totals['nonclinical']} heading_only_tx={totals['heading_only_tx']} "
        f"drug_mismatch={totals['drug_mismatch']} citation_mismatch={totals['citation_mismatch']} "
        f"mt_hits={totals['mt_hits']}"
    )
    if warnings:
        print("GUARD WARNINGS:")
        for w in warnings:
            print("  -", w)
    print(f"summary -> {out_root}/_rollout_summary{suffix}.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
