#!/usr/bin/env python3
"""
Boilerplate Detection Script for VetDict Disease Entries

Scans all species disease files for:
1. Known boilerplate phrases (generic templates copy-pasted across diseases)
2. Wrong species references (e.g., "両生類" in non-amphibian files)
3. Empty critical fields
4. Circular causes_ja (matches description_ja)
5. Missing treatment_ja/pathophysiology_ja for emergency conditions

Usage: python scripts/detect_boilerplate.py [--verbose]
"""

from __future__ import annotations

import argparse
import importlib
import sys
from collections import defaultdict
from pathlib import Path

# Add project root to path so we can use the api package
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Boilerplate phrases that indicate generic copy-paste templates
BOILERPLATE_PHRASES = {
    "generic_endocrine": [
        "ホルモンのフィードバックループ",
        "ホルモン補充療法または抑制療法により生理的バランスを回復",
        "多くの内分泌疾患は適切な薬物療法で長期管理可能",
    ],
    "generic_gi": [
        "粘膜の完全性、運動性、分泌機能、またはマイクロバイオームバランス",
        "後腸発酵動物では盲腸/結腸フローラの破壊が致死的ディスバイオーシス",
    ],
    "generic_bacterial": [
        "細菌感染症である。病原菌は付着因子",
        "培養感受性試験に基づく標的抗菌薬療法が必要である",
        "膿瘍や壊死組織には外科的排膿またはデブリードマン",
    ],
    "generic_viral": [
        "ウイルス感染症である。ウイルスは特定の受容体を介して宿主細胞に侵入",
    ],
    "generic_neoplasia": [
        "予防は限定的であるが、ホルモン依存性腫瘍軽減のための避妊・去勢手術",
        "癌遺伝子、腫瘍抑制遺伝子、DNA修復機構における遺伝子変異の蓄積",
    ],
    "generic_prevention": [
        "適切な衛生管理・消毒、利用可能なワクチン接種、創傷の迅速な処置、ストレス軽減",
        "予防には適切な飼育管理（適切な食事・清潔な環境・最適な温湿度）",
    ],
    "generic_prognosis": [
        "早期発見と適切な治療で多くの疾患は予後良好。慢性疾患は定期的モニタリングと治療調整で長期管理可能",
        "原因により予後が大きく異なる",
    ],
    "generic_neuro": [
        "解剖学的位置に応じて運動機能、感覚処理、自律神経調節、認知状態に影響を及ぼす",
        "脱髄、軸索変性、ニューロン喪失は不可逆的な場合がある",
    ],
    "generic_renal": [
        "腎臓、尿管、膀胱、または尿道の構造的・機能的障害",
        "進行性のネフロン喪失により高窒素血症、電解質異常、酸塩基障害",
    ],
    "generic_nutritional": [
        "栄養疾患の予後は欠乏/過剰の程度と是正の速やかさに依存する",
    ],
}

# Wrong species references that indicate copy-paste between species files
WRONG_SPECIES_BY_FILE = {
    "dog_diseases.py": ["両生類", "魚類", "鳥類", "爬虫類", "ウサギ", "フェレット"],
    "cat_diseases.py": ["両生類", "魚類", "犬種"],
    "rabbit_diseases.py": ["両生類", "魚類", "犬", "猫の"],
    "ferret_diseases.py": ["両生類", "魚類", "犬種"],
    "hamster_diseases.py": ["両生類", "魚類"],
    "guinea_pig_diseases.py": ["両生類", "魚類"],
    "chinchilla_diseases.py": ["両生類", "魚類"],
    "degu_diseases.py": ["両生類", "魚類"],
    "hedgehog_diseases.py": ["両生類", "魚類"],
    "sugar_glider_diseases.py": ["両生類", "魚類"],
    "bird_diseases.py": ["両生類", "魚類", "犬", "猫"],
    "parakeet_diseases.py": ["両生類", "魚類"],
    "parrot_diseases.py": ["両生類", "魚類"],
    "reptile_diseases.py": ["両生類", "魚類", "犬", "猫"],
    "lizard_diseases.py": ["両生類", "魚類"],
    "snake_diseases.py": ["両生類", "魚類"],
    "tortoise_diseases.py": ["両生類", "魚類"],
    # amphibian_diseases.py legitimately mentions amphibians
    # fish_diseases.py legitimately mentions fish
}

# Critical fields to check for emptiness
CRITICAL_FIELDS = [
    "description_ja",
    "causes_ja",
    "pathophysiology_ja",
    "treatment_ja",
    "prognosis_ja",
]

# Fields that should not be empty for any disease
REQUIRED_FIELDS = ["name", "name_ja"]


def find_disease_lists(file_path: Path) -> list[dict]:
    """Load a disease module via the api.species package and extract disease list."""
    module_name = f"api.species.{file_path.stem}"
    try:
        module = importlib.import_module(module_name)
    except Exception as e:  # noqa: BLE001
        print(f"  ⚠ Failed to load {file_path.name}: {e}", file=sys.stderr)
        return []

    # Look for known list names first, then any list of dicts
    candidates = ["DISEASES", "_DISEASES", "DOG_DISEASES", "CAT_DISEASES"]
    for attr in candidates:
        obj = getattr(module, attr, None)
        if isinstance(obj, list) and obj and isinstance(obj[0], dict):
            return obj

    # Fall back to any uppercase attribute that's a list of dicts
    for attr in dir(module):
        if attr.startswith("_"):
            continue
        if attr != attr.upper():
            continue
        obj = getattr(module, attr, None)
        if isinstance(obj, list) and obj and isinstance(obj[0], dict):
            return obj
    return []


def check_disease(disease: dict, filename: str) -> list[str]:
    """Check a single disease entry for issues. Returns list of issue strings."""
    issues = []

    # Check empty critical fields
    for field in CRITICAL_FIELDS:
        value = disease.get(field, "")
        if not value or (isinstance(value, str) and value.strip() == ""):
            issues.append(f"  ❌ EMPTY: {field}")

    # Check boilerplate phrases
    full_text_ja = " ".join(
        str(disease.get(f, "")) for f in CRITICAL_FIELDS
    )
    for category, phrases in BOILERPLATE_PHRASES.items():
        for phrase in phrases:
            if phrase in full_text_ja:
                # Find which field
                for field in CRITICAL_FIELDS:
                    if phrase in str(disease.get(field, "")):
                        issues.append(
                            f"  ⚠ BOILERPLATE [{category}] in {field}: «{phrase[:40]}...»"
                        )
                        break

    # Check wrong species references
    wrong_species = WRONG_SPECIES_BY_FILE.get(filename, [])
    for species_term in wrong_species:
        for field in CRITICAL_FIELDS:
            value = str(disease.get(field, ""))
            if species_term in value:
                # Skip if it's a common pet that might legitimately be mentioned
                # in differential diagnosis context
                context_idx = value.find(species_term)
                context = value[max(0, context_idx - 20) : context_idx + 30]
                # Skip differential diagnosis mentions
                if any(
                    skip in context for skip in ["鑑別", "比較", "犬では", "猫では", "犬と", "猫と"]
                ):
                    continue
                issues.append(
                    f"  🚩 WRONG SPECIES: «{species_term}» in {field} (context: ...{context}...)"
                )
                break

    # Check circular causes_ja (matches description_ja)
    description_ja = str(disease.get("description_ja", "")).strip()
    causes_ja = str(disease.get("causes_ja", "")).strip()
    if description_ja and causes_ja:
        # Strip the prefix "X における Y の原因: " if present
        causes_stripped = causes_ja
        if "の原因:" in causes_ja:
            causes_stripped = causes_ja.split("の原因:", 1)[1].strip()
        if causes_stripped == description_ja or (
            len(causes_stripped) < 100 and causes_stripped in description_ja
        ):
            issues.append("  🔁 CIRCULAR: causes_ja just repeats description_ja")

    # Check missing treatment_ja for emergency/critical conditions
    urgency = disease.get("urgency", "")
    if urgency in ("emergency", "critical"):
        treatment_ja = str(disease.get("treatment_ja", "")).strip()
        if not treatment_ja or len(treatment_ja) < 50:
            issues.append("  ⚡ MISSING TREATMENT: emergency disease without proper treatment_ja")

    return issues


def main():
    parser = argparse.ArgumentParser(description="Detect boilerplate in disease entries")
    parser.add_argument(
        "--verbose", action="store_true", help="Show all issues for each disease"
    )
    parser.add_argument(
        "--max-per-file",
        type=int,
        default=10,
        help="Limit displayed issues per file (default: 10)",
    )
    parser.add_argument(
        "--summary-only",
        action="store_true",
        help="Show only summary statistics",
    )
    parser.add_argument(
        "--filter",
        type=str,
        default="",
        help="Only show issues containing this string (e.g., 'EMPTY' or 'WRONG SPECIES')",
    )
    args = parser.parse_args()

    species_dir = Path(__file__).parent.parent / "api" / "species"
    if not species_dir.exists():
        print(f"❌ Species directory not found: {species_dir}", file=sys.stderr)
        sys.exit(1)

    total_diseases = 0
    total_issues = 0
    issues_by_type = defaultdict(int)
    issues_by_file = defaultdict(list)

    disease_files = sorted(
        f
        for f in species_dir.glob("*_diseases.py")
        if f.name not in ("__init__.py",)
    )

    print(f"🔍 Scanning {len(disease_files)} disease files...\n")

    for file_path in disease_files:
        diseases = find_disease_lists(file_path)
        if not diseases:
            continue

        file_issues = []
        for disease in diseases:
            total_diseases += 1
            issues = check_disease(disease, file_path.name)
            if issues:
                name = disease.get("name", "<no name>")
                name_ja = disease.get("name_ja", "")
                file_issues.append((name, name_ja, issues))
                total_issues += len(issues)
                for issue in issues:
                    if "EMPTY:" in issue:
                        issues_by_type["empty_field"] += 1
                    elif "BOILERPLATE" in issue:
                        issues_by_type["boilerplate"] += 1
                    elif "WRONG SPECIES" in issue:
                        issues_by_type["wrong_species"] += 1
                    elif "CIRCULAR" in issue:
                        issues_by_type["circular_causes"] += 1
                    elif "MISSING TREATMENT" in issue:
                        issues_by_type["missing_emergency_tx"] += 1

        if file_issues:
            issues_by_file[file_path.name] = file_issues

    # Print summary
    print(f"{'=' * 70}")
    print("📊 SUMMARY")
    print(f"{'=' * 70}")
    print(f"Total diseases scanned:  {total_diseases:,}")
    print(f"Diseases with issues:    {sum(len(v) for v in issues_by_file.values()):,}")
    print(f"Total issues found:      {total_issues:,}")
    print()
    print("Issues by type:")
    for issue_type, count in sorted(issues_by_type.items(), key=lambda x: -x[1]):
        print(f"  {issue_type:25} {count:,}")
    print()
    print("Issues by file:")
    for filename, file_issues in sorted(
        issues_by_file.items(), key=lambda x: -sum(len(i[2]) for i in x[1])
    ):
        total = sum(len(i[2]) for i in file_issues)
        print(f"  {filename:35} {len(file_issues):3} diseases / {total:4} issues")

    if args.summary_only:
        return

    # Detailed report per file
    print()
    print(f"{'=' * 70}")
    print("📋 DETAILED REPORT")
    print(f"{'=' * 70}")
    for filename, file_issues in sorted(issues_by_file.items()):
        # Filter by issue type if requested
        if args.filter:
            filtered = []
            for name, name_ja, issues in file_issues:
                matching = [i for i in issues if args.filter in i]
                if matching:
                    filtered.append((name, name_ja, matching))
            if not filtered:
                continue
            file_issues = filtered

        print(f"\n📁 {filename}")
        print(f"   ({len(file_issues)} affected diseases)")
        shown = file_issues[: args.max_per_file]
        for name, name_ja, issues in shown:
            print(f"\n  • {name} / {name_ja}")
            for issue in issues:
                print(issue)
        if len(file_issues) > args.max_per_file:
            print(
                f"\n  ... and {len(file_issues) - args.max_per_file} more affected diseases"
            )


if __name__ == "__main__":
    main()
