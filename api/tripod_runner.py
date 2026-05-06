"""tripod_runner.py - TRIPOD検証の自動実行ランナー

tripod_test_cases.jsonのテストケースを診断エンジンに自動投入し、
TRIPOD準拠のメトリクスレポートを生成する。

使用法:
    python -m api.tripod_runner [--json-path tests/tripod_test_cases.json]
"""

from __future__ import annotations

import json
import logging
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


def run_single_case(species: str, symptoms: list[str], primary_disease: str) -> dict:
    """診断エンジンに症状を投入して結果を取得（Flask test client経由）"""
    import os

    os.environ.setdefault("SECRET_KEY", "tripod_validation")

    from api.vetdict_api import app

    client = app.test_client()
    message = " ".join(symptoms)
    resp = client.post(
        "/api/diagnostic-chat/chat",
        json={"message": message, "species": species.lower(), "lang": "en"},
    )
    if resp.status_code != 200:
        return {"rank": -1, "confidence": 0.0, "candidates": []}

    data = resp.get_json()
    candidates = data.get("disease_candidates", [])

    rank = -1
    confidence = 0.0
    target_lower = primary_disease.lower().strip()

    for i, m in enumerate(candidates):
        name = (m.get("name") or m.get("name_en") or "").lower().strip()
        name_ja = (m.get("name_ja") or "").lower().strip()
        disease_id = (m.get("disease_id") or "").lower().strip()
        if target_lower in name or target_lower in name_ja or name in target_lower or target_lower in disease_id:
            rank = i + 1
            conf_raw = m.get("confidence", m.get("confidence_percent", 0))
            try:
                confidence = float(conf_raw)
                if confidence > 1:
                    confidence /= 100.0
            except (TypeError, ValueError):
                confidence = 0.0
            break

    top5 = []
    for m in candidates[:5]:
        n = m.get("name") or m.get("name_en") or ""
        c = float(m.get("confidence", m.get("confidence_percent", 0)) or 0)
        if c > 1:
            c /= 100.0
        top5.append((n, c))

    return {"rank": rank, "confidence": confidence, "candidates": top5}


def run_validation(json_path: str = "tests/tripod_test_cases.json") -> dict:
    """全テストケースを実行してレポートを生成"""
    from api.tripod_validation import DiagnosticValidationFramework

    fw = DiagnosticValidationFramework()
    fw.add_test_cases_from_json(json_path)

    passed_rank1 = 0
    passed_top3 = 0
    passed_top5 = 0
    total = len(fw.test_cases)
    species_results: dict[str, dict] = {}
    failed_cases: list[dict] = []

    for case in fw.test_cases:
        result = run_single_case(case.species, case.symptoms, case.primary_disease)
        rank = result["rank"]
        conf = result["confidence"]

        fw.record_result(
            case_id=case.case_id,
            predicted_rank=rank if rank > 0 else 999,
            confidence_score=conf,
            top_n_predictions=[(n, c) for n, c in result["candidates"]],
        )

        if rank == 1:
            passed_rank1 += 1
        if 1 <= rank <= 3:
            passed_top3 += 1
        if 1 <= rank <= 5:
            passed_top5 += 1

        sp = case.species.lower()
        if sp not in species_results:
            species_results[sp] = {"total": 0, "rank1": 0, "top3": 0, "confidences": []}
        species_results[sp]["total"] += 1
        if rank == 1:
            species_results[sp]["rank1"] += 1
            species_results[sp]["confidences"].append(conf)
        if 1 <= rank <= 3:
            species_results[sp]["top3"] += 1

        if rank != 1:
            failed_cases.append(
                {
                    "case_id": case.case_id,
                    "species": case.species,
                    "disease": case.primary_disease,
                    "actual_rank": rank,
                    "confidence": round(conf, 4),
                    "symptoms": case.symptoms,
                    "top3": [(n, round(c, 3)) for n, c in result["candidates"][:3]],
                }
            )

    # TRIPOD metrics
    metrics = fw.calculate_metrics()

    report = {
        "total_cases": total,
        "rank1_accuracy": passed_rank1 / total if total else 0,
        "top3_accuracy": passed_top3 / total if total else 0,
        "top5_accuracy": passed_top5 / total if total else 0,
        "by_species": {
            sp: {
                "total": d["total"],
                "rank1_accuracy": d["rank1"] / d["total"] if d["total"] else 0,
                "top3_accuracy": d["top3"] / d["total"] if d["total"] else 0,
                "mean_confidence": sum(d["confidences"]) / len(d["confidences"]) if d["confidences"] else 0,
            }
            for sp, d in sorted(species_results.items())
        },
        "tripod_metrics": metrics,
        "failed_cases": failed_cases,
    }

    return report


def print_report(report: dict) -> None:
    """レポートをコンソール出力"""
    print("=" * 60)
    print("TRIPOD Diagnostic Accuracy Validation Report")
    print("=" * 60)
    print(f"Total test cases: {report['total_cases']}")
    print(f"Rank 1 accuracy:  {report['rank1_accuracy']:.1%}")
    print(f"Top 3 accuracy:   {report['top3_accuracy']:.1%}")
    print(f"Top 5 accuracy:   {report['top5_accuracy']:.1%}")
    print()
    print("By species:")
    for sp, m in report["by_species"].items():
        print(
            f"  {sp:15s}: rank1={m['rank1_accuracy']:.0%}  top3={m['top3_accuracy']:.0%}  "
            f"mean_conf={m['mean_confidence']:.1%}  (n={m['total']})"
        )
    print()

    tm = report.get("tripod_metrics", {})
    cm = tm.get("confusion_matrix", {})
    if cm:
        print("Confusion Matrix:")
        print(f"  Sensitivity: {cm.get('sensitivity', 0):.1%}")
        print(f"  Specificity: {cm.get('specificity', 0):.1%}")
        print(f"  PPV:         {cm.get('ppv', 0):.1%}")
        print(f"  NPV:         {cm.get('npv', 0):.1%}")
        print(f"  Accuracy:    {cm.get('accuracy', 0):.1%}")
        print(f"  F1 Score:    {cm.get('f1_score', 0):.3f}")

    failed = report.get("failed_cases", [])
    if failed:
        print(f"\nFailed cases ({len(failed)}):")
        for fc in failed[:10]:
            print(
                f"  {fc['case_id']}: {fc['disease']} → rank {fc['actual_rank']} "
                f"(conf {fc['confidence']:.1%}, {len(fc['symptoms'])} symptoms)"
            )
            if fc.get("top3"):
                for name, c in fc["top3"]:
                    print(f"    - {name}: {c:.1%}")

    print("=" * 60)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run TRIPOD diagnostic validation")
    parser.add_argument("--json-path", default="tests/tripod_test_cases.json")
    parser.add_argument("--output", help="Save JSON report to file")
    args = parser.parse_args()

    report = run_validation(args.json_path)
    print_report(report)

    if args.output:
        with open(args.output, "w") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"\nJSON report saved to: {args.output}")
