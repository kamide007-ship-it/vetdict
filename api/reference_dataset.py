#!/usr/bin/env python3
"""
ShowDog Reference Dataset — FCI Show Report-Based Validation

Grounded in publicly available FCI/AKC/KC show reports and judging criteria.
Each case represents a realistic score profile derived from show-level
descriptions found in published critiques and breed evaluations.

FCI Grading System Mapping:
    FCI "Excellent"   → ShowDog S (95+) or A+ (90-94)
    FCI "Very Good"   → ShowDog A (85-89) or B+ (80-84)
    FCI "Good"        → ShowDog B (70-79)
    FCI "Sufficient"  → ShowDog C (<70)

Sources:
    - FCI Regulations for Dog Shows (fci.be/medias/EXP-REG-en-17234.pdf)
    - FCI Show Judges Regulations (fci.be/medias/JUG-REG-en-18458.pdf)
    - AKC Conformation Judging Guidelines (akc.org)
    - DPCA Top 20 Score Sheet System
    - Published breed critiques from international shows
"""

from typing import Dict, List

# =============================================================================
# FCI GRADE CRITERIA (from official regulations)
# =============================================================================

FCI_GRADE_CRITERIA = {
    "Excellent": {
        "description": "犬種標準の理想にきわめて近い。優れたコンディションで、犬種の典型的な気質を示す。",
        "description_en": "Comes very close to the ideal standard. Presented in excellent condition, "
                         "harmonious temperament, high class. Minor imperfections may be tolerated.",
        "showdog_grades": ["S", "A+"],
        "score_range": (90, 100),
    },
    "Very Good": {
        "description": "全体的に調和がとれ、犬種の典型的特徴を高度に示す。軽微な欠点がいくつかある場合がある。",
        "description_en": "Harmonious overall appearance, breed-typical to a high degree. "
                         "A few minor faults may be tolerated, none of a morphological nature.",
        "showdog_grades": ["A", "B+"],
        "score_range": (80, 89),
    },
    "Good": {
        "description": "主な犬種特徴を十分に満たすが、複数の軽微な欠点または単一の重大な欠点がある。",
        "description_en": "Possesses main features of the breed but showing faults. "
                         "Good points outweigh faults.",
        "showdog_grades": ["B"],
        "score_range": (70, 79),
    },
    "Sufficient": {
        "description": "犬種特性を十分に満たさなくなった、または身体的・気質的コンディションが不足。",
        "description_en": "No longer sufficiently meets breed characteristics. "
                         "Physical or temperament condition deficient.",
        "showdog_grades": ["C"],
        "score_range": (0, 69),
    },
}


# =============================================================================
# REFERENCE CASES — FCI Show Report-Derived Profiles
# =============================================================================
# Each case simulates a realistic dog evaluated at an FCI international show.
# Axis scores are derived from typical critique language found in published
# show reports (e.g. "excellent topline", "slightly loose movement",
# "good coat texture but lacking density").

REFERENCE_CASES: List[Dict] = [

    # =========================================================================
    # EXCELLENT tier (FCI Excellent → ShowDog S or A+)
    # =========================================================================

    {
        "id": "REF-001",
        "description": "Toy Poodle — FCI Excellent 1 / Best of Breed典型例",
        "source": "FCI European Dog Show critique pattern",
        "breed_id": "172d_poodle_toy",
        "age_years": 3.5,
        "expected_fci_grade": "Excellent",
        "expected_showdog_grade": "A+",
        "expected_score_range": (90, 96),
        "axis_scores": {
            "skeletal": 93, "gait": 90, "muscle": 88,
            "coat": 96, "temperament": 92
        },
        "sub_scores": {
            "skeletal": {"proportion": 94, "skeletal": 92},
            "muscle": {"muscular": 88},
            "gait": {"stride": 91, "balance": 90, "fluidity": 89},
            "coat": {"texture": 97, "volume": 95, "grooming": 96},
            "temperament": {"confidence": 93, "alertness": 91, "composure": 92}
        },
        "critique_ja": "見事なコートクオリティ。プロポーション良好、軽快な動き。"
    },

    {
        "id": "REF-002",
        "description": "German Shepherd — FCI Excellent / VA Rating典型例",
        "source": "BSZS (Bundessiegerprüfung) evaluation pattern",
        "breed_id": "166_german_shepherd",
        "age_years": 4.0,
        "expected_fci_grade": "Excellent",
        "expected_showdog_grade": "A+",
        "expected_score_range": (90, 96),
        "axis_scores": {
            "skeletal": 91, "gait": 96, "muscle": 93,
            "coat": 88, "temperament": 94
        },
        "sub_scores": {
            "skeletal": {"proportion": 90, "skeletal": 92},
            "muscle": {"muscular": 93},
            "gait": {"stride": 97, "balance": 95, "fluidity": 96},
            "coat": {"texture": 89, "volume": 87, "grooming": 88},
            "temperament": {"confidence": 95, "alertness": 93, "composure": 94}
        },
        "critique_ja": "長いストライドで地面を覆う理想的なトロット。背線が安定。VA級。"
    },

    {
        "id": "REF-003",
        "description": "Labrador Retriever — FCI Excellent / CACIB級典型例",
        "source": "Crufts/FCI international critique pattern",
        "breed_id": "122_labrador_retriever",
        "age_years": 3.0,
        "expected_fci_grade": "Excellent",
        "expected_showdog_grade": "A+",
        "expected_score_range": (90, 96),
        "axis_scores": {
            "skeletal": 95, "gait": 91, "muscle": 94,
            "coat": 89, "temperament": 90
        },
        "sub_scores": {
            "skeletal": {"proportion": 96, "skeletal": 94},
            "muscle": {"muscular": 94},
            "gait": {"stride": 92, "balance": 90, "fluidity": 91},
            "coat": {"texture": 90, "volume": 88, "grooming": 89},
            "temperament": {"confidence": 91, "alertness": 89, "composure": 90}
        },
        "critique_ja": "筋肉質で均整の取れた体型。広い胸、力強い腰。典型的なオッターテール。"
    },

    # =========================================================================
    # VERY GOOD tier (FCI Very Good → ShowDog A or B+)
    # =========================================================================

    {
        "id": "REF-004",
        "description": "Shiba Inu — FCI Very Good / 軽微な歩様問題",
        "source": "JKC/FCI Asia show critique pattern",
        "breed_id": "257_shiba_inu",
        "age_years": 2.5,
        "expected_fci_grade": "Very Good",
        "expected_showdog_grade": "A",
        "expected_score_range": (85, 89),
        "axis_scores": {
            "skeletal": 87, "gait": 80, "muscle": 85,
            "coat": 86, "temperament": 92
        },
        "sub_scores": {
            "skeletal": {"proportion": 88, "skeletal": 86},
            "muscle": {"muscular": 85},
            "gait": {"stride": 81, "balance": 78, "fluidity": 81},
            "coat": {"texture": 87, "volume": 85, "grooming": 86},
            "temperament": {"confidence": 94, "alertness": 91, "composure": 91}
        },
        "critique_ja": "柴犬らしい凛々しい表情と気質。歩様にやや硬さ。被毛は犬種標準通り。"
    },

    {
        "id": "REF-005",
        "description": "French Bulldog — FCI Very Good / 骨格良好だが呼吸懸念",
        "source": "FCI European show critique pattern",
        "breed_id": "057_bulldog_french",
        "age_years": 2.0,
        "expected_fci_grade": "Very Good",
        "expected_showdog_grade": "B+",
        "expected_score_range": (80, 85),
        "axis_scores": {
            "skeletal": 86, "gait": 76, "muscle": 84,
            "coat": 82, "temperament": 85
        },
        "sub_scores": {
            "skeletal": {"proportion": 87, "skeletal": 85},
            "muscle": {"muscular": 84},
            "gait": {"stride": 77, "balance": 75, "fluidity": 76},
            "coat": {"texture": 83, "volume": 81, "grooming": 82},
            "temperament": {"confidence": 86, "alertness": 84, "composure": 85}
        },
        "critique_ja": "良好なプロポーション。歩様は短めのストライドで犬種標準内だが改善余地あり。"
    },

    {
        "id": "REF-006",
        "description": "Golden Retriever — FCI Very Good / 若齢で未成熟",
        "source": "AKC national specialty critique pattern",
        "breed_id": "111_golden_retriever",
        "age_years": 1.5,
        "expected_fci_grade": "Very Good",
        "expected_showdog_grade": "A",
        "expected_score_range": (84, 89),
        "axis_scores": {
            "skeletal": 88, "gait": 85, "muscle": 82,
            "coat": 90, "temperament": 87
        },
        "sub_scores": {
            "skeletal": {"proportion": 89, "skeletal": 87},
            "muscle": {"muscular": 82},
            "gait": {"stride": 86, "balance": 84, "fluidity": 85},
            "coat": {"texture": 91, "volume": 89, "grooming": 90},
            "temperament": {"confidence": 88, "alertness": 86, "composure": 87}
        },
        "critique_ja": "美しいゴールドの被毛。若齢のため筋肉の成熟はこれから。構造は良好。"
    },

    # =========================================================================
    # GOOD tier (FCI Good → ShowDog B)
    # =========================================================================

    {
        "id": "REF-007",
        "description": "Pomeranian — FCI Good / 被毛不足と体重超過",
        "source": "FCI show critique pattern",
        "breed_id": "195_pomeranian",
        "age_years": 5.0,
        "expected_fci_grade": "Good",
        "expected_showdog_grade": "B",
        "expected_score_range": (70, 79),
        "axis_scores": {
            "skeletal": 78, "gait": 72, "muscle": 70,
            "coat": 68, "temperament": 80
        },
        "sub_scores": {
            "skeletal": {"proportion": 76, "skeletal": 80},
            "muscle": {"muscular": 70},
            "gait": {"stride": 73, "balance": 71, "fluidity": 72},
            "coat": {"texture": 70, "volume": 65, "grooming": 69},
            "temperament": {"confidence": 82, "alertness": 78, "composure": 80}
        },
        "critique_ja": "犬種の基本特徴は備えるが、被毛の密度不足。やや体重超過で動きに影響。"
    },

    {
        "id": "REF-008",
        "description": "Siberian Husky — FCI Good / 歩様に課題",
        "source": "FCI Nordic show critique pattern",
        "breed_id": "158_siberian_husky",
        "age_years": 3.0,
        "expected_fci_grade": "Good",
        "expected_showdog_grade": "B",
        "expected_score_range": (70, 79),
        "axis_scores": {
            "skeletal": 80, "gait": 68, "muscle": 75,
            "coat": 78, "temperament": 76
        },
        "sub_scores": {
            "skeletal": {"proportion": 81, "skeletal": 79},
            "muscle": {"muscular": 75},
            "gait": {"stride": 70, "balance": 65, "fluidity": 69},
            "coat": {"texture": 79, "volume": 77, "grooming": 78},
            "temperament": {"confidence": 77, "alertness": 75, "composure": 76}
        },
        "critique_ja": "骨格は標準を満たすが、歩様に揺れあり。ダブルコートの密度はやや不足。"
    },

    # =========================================================================
    # SUFFICIENT tier (FCI Sufficient → ShowDog C)
    # =========================================================================

    {
        "id": "REF-009",
        "description": "Bulldog English — FCI Sufficient / 構造的課題複数",
        "source": "FCI/KC critique pattern for structure-challenged dogs",
        "breed_id": "058_bulldog_english",
        "age_years": 4.0,
        "expected_fci_grade": "Sufficient",
        "expected_showdog_grade": "C",
        "expected_score_range": (55, 69),
        "axis_scores": {
            "skeletal": 65, "gait": 55, "muscle": 60,
            "coat": 70, "temperament": 72
        },
        "sub_scores": {
            "skeletal": {"proportion": 63, "skeletal": 67},
            "muscle": {"muscular": 60},
            "gait": {"stride": 56, "balance": 53, "fluidity": 56},
            "coat": {"texture": 71, "volume": 69, "grooming": 70},
            "temperament": {"confidence": 73, "alertness": 71, "composure": 72}
        },
        "critique_ja": "複数の構造的欠点。歩様に困難あり。犬種標準を十分には満たさない。"
    },

    # =========================================================================
    # AGE EDGE CASES (年齢による影響テスト)
    # =========================================================================

    {
        "id": "REF-010",
        "description": "Toy Poodle — パピークラス（6ヶ月）",
        "source": "FCI puppy class evaluation pattern",
        "breed_id": "172d_poodle_toy",
        "age_years": 0.5,
        "expected_fci_grade": "Very Promising",
        "expected_showdog_grade": "B",
        "expected_score_range": (75, 82),
        "axis_scores": {
            "skeletal": 85, "gait": 80, "muscle": 78,
            "coat": 88, "temperament": 82
        },
        "sub_scores": {
            "skeletal": {"proportion": 86, "skeletal": 84},
            "muscle": {"muscular": 78},
            "gait": {"stride": 81, "balance": 79, "fluidity": 80},
            "coat": {"texture": 89, "volume": 87, "grooming": 88},
            "temperament": {"confidence": 83, "alertness": 81, "composure": 82}
        },
        "critique_ja": "将来有望。パピー期のため骨格は未完成だが、プロポーションの素質は高い。"
    },

    {
        "id": "REF-011",
        "description": "Labrador Retriever — ベテランクラス（11歳）",
        "source": "FCI veteran class evaluation pattern",
        "breed_id": "122_labrador_retriever",
        "age_years": 11.0,
        "expected_fci_grade": "Very Good",
        "expected_showdog_grade": "B+",
        "expected_score_range": (78, 84),
        "axis_scores": {
            "skeletal": 88, "gait": 78, "muscle": 80,
            "coat": 85, "temperament": 90
        },
        "sub_scores": {
            "skeletal": {"proportion": 89, "skeletal": 87},
            "muscle": {"muscular": 80},
            "gait": {"stride": 79, "balance": 77, "fluidity": 78},
            "coat": {"texture": 86, "volume": 84, "grooming": 85},
            "temperament": {"confidence": 91, "alertness": 89, "composure": 90}
        },
        "critique_ja": "年齢を感じさせない堂々とした気質。歩様に加齢変化あるが骨格構造は健全。"
    },

    # =========================================================================
    # PHOTO-ONLY CASES (動画なし — gait/temperament デフォルト)
    # =========================================================================

    {
        "id": "REF-012",
        "description": "Cavalier — 写真のみ評価（動画なし）",
        "source": "Photo-only evaluation baseline",
        "breed_id": "044_cavalier_king_charles",
        "age_years": 3.0,
        "expected_fci_grade": "Very Good",
        "expected_showdog_grade": "B+",
        "expected_score_range": (79, 84),
        "axis_scores": {
            "skeletal": 86, "gait": 75, "muscle": 83,
            "coat": 88, "temperament": 75
        },
        "sub_scores": {
            "skeletal": {"proportion": 87, "skeletal": 85},
            "muscle": {"muscular": 83},
            "coat": {"texture": 89, "volume": 87, "grooming": 88},
        },
        "critique_ja": "写真からの評価。骨格・被毛は良好。歩様・気質は動画なしのためデフォルト値。"
    },
]


# =============================================================================
# VALIDATION RUNNER
# =============================================================================

def run_validation(verbose: bool = True) -> Dict:
    """
    Run all reference cases through the hybrid scoring pipeline
    and compare against expected FCI grades and score ranges.

    Returns:
        Dict with pass/fail counts, grade accuracy, and score deviation stats.
    """
    try:
        from api.scoring import hybrid_score
    except ImportError:
        from scoring import hybrid_score

    results = []
    grade_matches = 0
    range_matches = 0
    fci_matches = 0
    total_deviation = 0.0

    for case in REFERENCE_CASES:
        result = hybrid_score(
            algorithm_axis_scores=case["axis_scores"],
            ai_observations=None,
            age_years=case["age_years"],
            breed_id=case["breed_id"],
            sub_scores=case.get("sub_scores")
        )

        final_score = result["final_result"]["final_score"]
        final_grade = result["final_result"]["grade"]
        lo, hi = case["expected_score_range"]
        in_range = lo <= final_score <= hi
        grade_ok = final_grade == case["expected_showdog_grade"]

        # Check FCI grade mapping
        fci_expected = case["expected_fci_grade"]
        fci_info = FCI_GRADE_CRITERIA.get(fci_expected, {})
        fci_ok = final_grade in fci_info.get("showdog_grades", [])

        if in_range:
            range_matches += 1
        if grade_ok:
            grade_matches += 1
        if fci_ok:
            fci_matches += 1

        # Deviation from expected range midpoint
        midpoint = (lo + hi) / 2
        deviation = final_score - midpoint
        total_deviation += abs(deviation)

        entry = {
            "id": case["id"],
            "breed_id": case["breed_id"],
            "description": case["description"],
            "expected_range": (lo, hi),
            "expected_grade": case["expected_showdog_grade"],
            "expected_fci": fci_expected,
            "actual_score": final_score,
            "actual_grade": final_grade,
            "base_score": result["layer1_algorithm"]["base_score"],
            "in_range": in_range,
            "grade_match": grade_ok,
            "fci_match": fci_ok,
            "confidence": result["confidence"]["overall"],
        }
        results.append(entry)

        if verbose:
            status = "PASS" if (in_range and grade_ok) else "FAIL"
            print(f"  [{status}] {case['id']} {case['description'][:40]:40s} "
                  f"Score={final_score:5.1f} (expect {lo}-{hi}) "
                  f"Grade={final_grade} (expect {case['expected_showdog_grade']}) "
                  f"FCI={fci_expected}")

    n = len(REFERENCE_CASES)
    mae = total_deviation / n if n > 0 else 0

    summary = {
        "total_cases": n,
        "score_range_accuracy": round(range_matches / n * 100, 1),
        "grade_accuracy": round(grade_matches / n * 100, 1),
        "fci_grade_accuracy": round(fci_matches / n * 100, 1),
        "mean_absolute_deviation": round(mae, 2),
        "range_matches": range_matches,
        "grade_matches": grade_matches,
        "fci_matches": fci_matches,
        "cases": results,
    }

    if verbose:
        print(f"\n{'='*65}")
        print(f"  Score Range Accuracy:  {summary['score_range_accuracy']}%  ({range_matches}/{n})")
        print(f"  Grade Accuracy:        {summary['grade_accuracy']}%  ({grade_matches}/{n})")
        print(f"  FCI Grade Accuracy:    {summary['fci_grade_accuracy']}%  ({fci_matches}/{n})")
        print(f"  Mean Absolute Dev:     {mae:.2f} points")
        print(f"{'='*65}")

    return summary


if __name__ == "__main__":
    print("=" * 65)
    print("ShowDog Reference Dataset Validation")
    print("Based on FCI/AKC/KC show report patterns")
    print("=" * 65)
    run_validation(verbose=True)
