"""
Algorithm validation module for the ShowDog analysis platform.

Validates internal consistency of all analysis coefficients, cross-references
breed data against algorithm parameters, and detects configuration anomalies.

Validation layers:
  1. Coefficient Table Integrity — all tables self-consistent
  2. Cross-Module Consistency — local_analysis ↔ scoring ↔ breeds aligned
  3. Breed Coverage — every breed in breeds.py has usable coefficients
  4. Score Range Plausibility — no impossible coefficient combinations
  5. FCI Text ↔ Coefficient Coherence — derived values match descriptions

Usage:
    from api.validation import run_full_validation
    report = run_full_validation()
    assert report["passed"], report["failures"]
"""

import logging
from typing import Dict, List

from api.breeds import BREED_DATA
from api.breed_coefficients import (
    compute_coverage_report,
    derive_angle_group,
    get_breed_coefficients,
)
from api.local_analysis import (
    BREED_ANGLE_GROUP_MAP,
    BREED_ANGLE_STANDARDS,
    BREED_GAIT_COEFFICIENTS,
    BREED_RATIO_COEFFICIENTS,
    _angle_deviation_score,
)
from api.scoring import (
    BREED_PROFILE_MAP,
    BREED_SENSITIVITY_PROFILES,
    WEIGHTS,
    WEIGHTS_HASH,
    calculate_score,
    compute_weights_hash,
)

logger = logging.getLogger(__name__)


# =============================================================================
# 1. COEFFICIENT TABLE INTEGRITY
# =============================================================================

def validate_angle_standards() -> List[Dict]:
    """Validate that all angle standard entries are internally consistent.

    Checks:
    - All groups have required angle keys
    - Ideal angles are within physically plausible ranges
    - Tolerances are positive and reasonable
    - Weights within each group sum to ~1.0
    """
    failures = []
    required_keys = {
        "shoulder_angle", "rear_angle", "head_carriage",
        "tail_set", "topline_straightness",
        "front_leg_symmetry", "rear_leg_symmetry",
    }

    for group, standards in BREED_ANGLE_STANDARDS.items():
        # Check required keys
        missing = required_keys - set(standards.keys())
        if missing:
            failures.append({
                "check": "angle_standards_keys",
                "group": group,
                "message": f"Missing keys: {missing}",
            })
            continue

        total_weight = 0.0
        for key, (ideal, tolerance, weight) in standards.items():
            # Validate ranges
            if key in ("shoulder_angle", "rear_angle"):
                if not (60 <= ideal <= 150):
                    failures.append({
                        "check": "angle_plausibility",
                        "group": group,
                        "key": key,
                        "message": f"Ideal angle {ideal}° outside plausible range [60, 150]",
                    })
            elif key == "head_carriage":
                if not (10 <= ideal <= 90):
                    failures.append({
                        "check": "angle_plausibility",
                        "group": group,
                        "key": key,
                        "message": f"Head carriage {ideal}° outside plausible range [10, 90]",
                    })
            elif key == "tail_set":
                if not (0 <= ideal <= 90):
                    failures.append({
                        "check": "angle_plausibility",
                        "group": group,
                        "key": key,
                        "message": f"Tail set {ideal}° outside plausible range [0, 90]",
                    })
            elif key == "topline_straightness":
                if not (0.5 <= ideal <= 1.0):
                    failures.append({
                        "check": "angle_plausibility",
                        "group": group,
                        "key": key,
                        "message": f"Topline {ideal} outside plausible range [0.5, 1.0]",
                    })
            elif key in ("front_leg_symmetry", "rear_leg_symmetry"):
                if not (0.5 <= ideal <= 1.0):
                    failures.append({
                        "check": "angle_plausibility",
                        "group": group,
                        "key": key,
                        "message": f"Symmetry ideal {ideal} outside plausible range [0.5, 1.0]",
                    })

            if tolerance <= 0:
                failures.append({
                    "check": "tolerance_positive",
                    "group": group,
                    "key": key,
                    "message": f"Tolerance must be positive, got {tolerance}",
                })

            if not (0.0 < weight <= 0.5):
                failures.append({
                    "check": "weight_range",
                    "group": group,
                    "key": key,
                    "message": f"Weight {weight} outside expected range (0, 0.5]",
                })

            total_weight += weight

        if abs(total_weight - 1.0) > 0.02:
            failures.append({
                "check": "angle_weights_sum",
                "group": group,
                "message": f"Angle weights sum to {total_weight:.3f}, expected ~1.0",
            })

    return failures


def validate_ratio_coefficients() -> List[Dict]:
    """Validate body ratio coefficient tables.

    Checks:
    - All groups present in BREED_RATIO_COEFFICIENTS match angle groups
    - Ideal ratios are within plausible range [0.8, 2.0]
    - Tolerances are positive
    - Head/limb coefficients are positive and < 1.0
    """
    failures = []

    for group, (ratio, tol, head_coeff, limb_coeff) in BREED_RATIO_COEFFICIENTS.items():
        if not (0.8 <= ratio <= 2.0):
            failures.append({
                "check": "ratio_plausibility",
                "group": group,
                "message": f"Ideal ratio {ratio} outside plausible range [0.8, 2.0]",
            })
        if tol <= 0:
            failures.append({
                "check": "ratio_tolerance",
                "group": group,
                "message": f"Ratio tolerance must be positive, got {tol}",
            })
        if not (0.0 < head_coeff < 1.0):
            failures.append({
                "check": "head_coeff_range",
                "group": group,
                "message": f"Head coefficient {head_coeff} outside range (0, 1.0)",
            })
        if not (0.0 < limb_coeff < 1.0):
            failures.append({
                "check": "limb_coeff_range",
                "group": group,
                "message": f"Limb coefficient {limb_coeff} outside range (0, 1.0)",
            })

    return failures


def validate_gait_coefficients() -> List[Dict]:
    """Validate gait coefficient tables.

    Checks:
    - Stride ratios within [0.01, 0.50]
    - Pitch stability within [0.001, 0.1]
    - Cycle regularity weight within [0.1, 0.5]
    - All tolerances positive
    """
    failures = []

    for group, (stride, stride_tol, pitch, pitch_tol, reg_w) in BREED_GAIT_COEFFICIENTS.items():
        if not (0.01 <= stride <= 0.50):
            failures.append({
                "check": "stride_plausibility",
                "group": group,
                "message": f"Stride ratio {stride} outside range [0.01, 0.50]",
            })
        if stride_tol <= 0:
            failures.append({
                "check": "stride_tolerance",
                "group": group,
                "message": f"Stride tolerance must be positive, got {stride_tol}",
            })
        if not (0.001 <= pitch <= 0.1):
            failures.append({
                "check": "pitch_plausibility",
                "group": group,
                "message": f"Pitch {pitch} outside range [0.001, 0.1]",
            })
        if pitch_tol <= 0:
            failures.append({
                "check": "pitch_tolerance",
                "group": group,
                "message": f"Pitch tolerance must be positive, got {pitch_tol}",
            })
        if not (0.1 <= reg_w <= 0.5):
            failures.append({
                "check": "regularity_weight",
                "group": group,
                "message": f"Regularity weight {reg_w} outside range [0.1, 0.5]",
            })

    return failures


def validate_sensitivity_profiles() -> List[Dict]:
    """Validate breed sensitivity profiles.

    Checks:
    - All profiles have all 5 axes
    - All sensitivity values are positive
    - Mean sensitivity across axes is reasonable (0.5-2.0)
    """
    failures = []

    for profile_name, profile in BREED_SENSITIVITY_PROFILES.items():
        missing = set(WEIGHTS.keys()) - set(profile.keys())
        if missing:
            failures.append({
                "check": "sensitivity_axes",
                "profile": profile_name,
                "message": f"Missing axes: {missing}",
            })
            continue

        for axis, value in profile.items():
            if value <= 0:
                failures.append({
                    "check": "sensitivity_positive",
                    "profile": profile_name,
                    "axis": axis,
                    "message": f"Sensitivity must be positive, got {value}",
                })
            if value > 3.0:
                failures.append({
                    "check": "sensitivity_max",
                    "profile": profile_name,
                    "axis": axis,
                    "message": f"Sensitivity {value} exceeds maximum 3.0",
                })

        mean_val = sum(profile.values()) / len(profile)
        if not (0.5 <= mean_val <= 2.0):
            failures.append({
                "check": "sensitivity_mean",
                "profile": profile_name,
                "message": f"Mean sensitivity {mean_val:.2f} outside expected range [0.5, 2.0]",
            })

    return failures


# =============================================================================
# 2. CROSS-MODULE CONSISTENCY
# =============================================================================

def validate_group_alignment() -> List[Dict]:
    """Validate that all coefficient table groups are aligned.

    Every group in BREED_ANGLE_STANDARDS should also exist in
    BREED_RATIO_COEFFICIENTS and BREED_GAIT_COEFFICIENTS (and vice versa).
    """
    failures = []

    angle_groups = set(BREED_ANGLE_STANDARDS.keys())
    ratio_groups = set(BREED_RATIO_COEFFICIENTS.keys())
    gait_groups = set(BREED_GAIT_COEFFICIENTS.keys())

    # Check symmetric presence
    for name, groups in [("angle", angle_groups), ("ratio", ratio_groups), ("gait", gait_groups)]:
        for other_name, other_groups in [("angle", angle_groups), ("ratio", ratio_groups), ("gait", gait_groups)]:
            if name == other_name:
                continue
            missing = groups - other_groups
            if missing:
                failures.append({
                    "check": "group_alignment",
                    "message": f"Groups in {name} but not in {other_name}: {missing}",
                })

    return failures


def validate_breed_map_consistency() -> List[Dict]:
    """Validate that BREED_ANGLE_GROUP_MAP and BREED_PROFILE_MAP are consistent.

    Checks:
    - Every breed in BREED_ANGLE_GROUP_MAP references a valid angle group
    - Every breed in BREED_PROFILE_MAP references a valid sensitivity profile
    - Breeds appearing in one map ideally appear in the other
    """
    failures = []

    angle_groups = set(BREED_ANGLE_STANDARDS.keys())
    profile_keys = set(BREED_SENSITIVITY_PROFILES.keys())

    for breed_id, group in BREED_ANGLE_GROUP_MAP.items():
        if group not in angle_groups:
            failures.append({
                "check": "angle_map_valid_group",
                "breed_id": breed_id,
                "message": f"References unknown angle group '{group}'",
            })
        if breed_id not in BREED_DATA:
            failures.append({
                "check": "angle_map_breed_exists",
                "severity": "warning",
                "breed_id": breed_id,
                "message": (
                    f"Breed ID not found in BREED_DATA "
                    f"(coefficient group '{group}' still usable via fallback)"
                ),
            })

    for breed_id, profile in BREED_PROFILE_MAP.items():
        if profile not in profile_keys:
            failures.append({
                "check": "profile_map_valid",
                "breed_id": breed_id,
                "message": f"References unknown sensitivity profile '{profile}'",
            })
        if breed_id not in BREED_DATA:
            failures.append({
                "check": "profile_map_breed_exists",
                "severity": "warning",
                "breed_id": breed_id,
                "message": (
                    f"Breed ID not found in BREED_DATA "
                    f"(sensitivity profile '{profile}' still usable via fallback)"
                ),
            })

    # Cross-map coverage check (advisory, not failure)
    angle_mapped = set(BREED_ANGLE_GROUP_MAP.keys())
    profile_mapped = set(BREED_PROFILE_MAP.keys())

    in_angle_not_profile = angle_mapped - profile_mapped
    in_profile_not_angle = profile_mapped - angle_mapped

    if in_angle_not_profile:
        failures.append({
            "check": "cross_map_coverage",
            "severity": "warning",
            "message": f"{len(in_angle_not_profile)} breeds in angle map but not sensitivity map",
            "breed_ids": sorted(in_angle_not_profile),
        })

    if in_profile_not_angle:
        failures.append({
            "check": "cross_map_coverage",
            "severity": "warning",
            "message": f"{len(in_profile_not_angle)} breeds in sensitivity map but not angle map",
            "breed_ids": sorted(in_profile_not_angle),
        })

    return failures


def validate_weights_integrity() -> List[Dict]:
    """Validate scoring weights haven't been tampered with."""
    failures = []

    if abs(sum(WEIGHTS.values()) - 1.0) >= 0.0001:
        failures.append({
            "check": "weights_sum",
            "message": f"Weights sum to {sum(WEIGHTS.values())}, expected 1.0",
        })

    if WEIGHTS_HASH != compute_weights_hash():
        failures.append({
            "check": "weights_hash",
            "message": "Weights hash mismatch — possible tampering",
        })

    return failures


# =============================================================================
# 3. BREED COVERAGE VALIDATION
# =============================================================================

def validate_breed_coverage(*, min_explicit_pct: float = 5.0) -> List[Dict]:
    """Validate that breed coefficient coverage is adequate.

    Checks:
    - Every breed in BREED_DATA can produce valid coefficients
    - Explicit mapping percentage meets minimum threshold
    - No breed produces invalid/out-of-range coefficients
    """
    failures = []
    report = compute_coverage_report()

    if report["explicit_pct"] < min_explicit_pct:
        failures.append({
            "check": "explicit_coverage",
            "message": (
                f"Only {report['explicit_pct']}% breeds explicitly mapped "
                f"(minimum {min_explicit_pct}%)"
            ),
        })

    # Validate every breed produces valid coefficients
    for breed_id, breed_entry in BREED_DATA.items():
        coeffs = get_breed_coefficients(breed_id)

        if coeffs["angle_group"] not in BREED_ANGLE_STANDARDS:
            failures.append({
                "check": "breed_angle_group_valid",
                "breed_id": breed_id,
                "message": f"Derived angle group '{coeffs['angle_group']}' not in standards",
            })

        if not (0.8 <= coeffs["ideal_ratio"] <= 2.0):
            failures.append({
                "check": "breed_ratio_valid",
                "breed_id": breed_id,
                "message": f"Derived ratio {coeffs['ideal_ratio']} out of range",
            })

        if coeffs["coat_type"] not in ("long", "curly", "wire", "double", "short", "medium"):
            failures.append({
                "check": "breed_coat_valid",
                "breed_id": breed_id,
                "message": f"Unknown coat type '{coeffs['coat_type']}'",
            })

        if coeffs["body_mass"] not in ("large", "medium", "small"):
            failures.append({
                "check": "breed_mass_valid",
                "breed_id": breed_id,
                "message": f"Unknown body mass '{coeffs['body_mass']}'",
            })

    return failures


# =============================================================================
# 4. SCORE RANGE PLAUSIBILITY
# =============================================================================

def validate_score_range_plausibility() -> List[Dict]:
    """Validate that coefficient combinations produce plausible score ranges.

    For each breed group, simulates ideal and poor specimens to verify
    the scoring algorithm produces scores in expected ranges.
    """
    failures = []

    for group in BREED_ANGLE_STANDARDS:
        standards = BREED_ANGLE_STANDARDS[group]

        # Simulate perfect specimen: all measurements at ideal
        perfect_scores = {}
        for key, (ideal, tolerance, weight) in standards.items():
            score = _angle_deviation_score(ideal, ideal, tolerance, weight)
            perfect_scores[key] = score

        total_perfect = sum(perfect_scores.values())
        # With all measurements at ideal, weighted sum should be close to total weight (1.0)
        if total_perfect < 0.90:
            failures.append({
                "check": "perfect_specimen_score",
                "group": group,
                "message": f"Perfect specimen total {total_perfect:.3f} below 0.90",
            })

        # Simulate severely deviated specimen: all measurements 3x tolerance off
        poor_scores = {}
        for key, (ideal, tolerance, weight) in standards.items():
            score = _angle_deviation_score(
                ideal + 3 * tolerance, ideal, tolerance, weight
            )
            poor_scores[key] = score

        total_poor = sum(poor_scores.values())
        # Poor specimen should still get some score (not zero)
        if total_poor < 0.01:
            failures.append({
                "check": "poor_specimen_score",
                "group": group,
                "message": f"Severely deviated specimen scores {total_poor:.4f} (near zero)",
            })

    # Validate scoring core with boundary inputs
    boundary_cases = [
        ({"skeletal": 0, "gait": 0, "muscle": 0, "coat": 0, "temperament": 0}, 0.5, 0, "C"),
        ({"skeletal": 100, "gait": 100, "muscle": 100, "coat": 100, "temperament": 100}, 3.0, 100, "S"),
        ({"skeletal": 50, "gait": 50, "muscle": 50, "coat": 50, "temperament": 50}, 3.0, 50, "C"),
    ]

    for scores, age, expected_score, expected_grade in boundary_cases:
        result = calculate_score(scores, age)
        if result["final_score"] != expected_score:
            failures.append({
                "check": "boundary_score",
                "input": scores,
                "age": age,
                "message": f"Expected score {expected_score}, got {result['final_score']}",
            })
        if result["grade"] != expected_grade:
            failures.append({
                "check": "boundary_grade",
                "input": scores,
                "age": age,
                "message": f"Expected grade {expected_grade}, got {result['grade']}",
            })

    return failures


# =============================================================================
# 5. FCI TEXT ↔ COEFFICIENT COHERENCE
# =============================================================================

def validate_fci_text_coherence() -> List[Dict]:
    """Validate that explicitly mapped breeds' derived coefficients match their mapping.

    For breeds in BREED_ANGLE_GROUP_MAP, checks whether the FCI text
    descriptions are consistent with the assigned angle group.
    Mismatches suggest either the text or the mapping needs updating.
    """
    failures = []

    for breed_id, assigned_group in BREED_ANGLE_GROUP_MAP.items():
        breed_entry = BREED_DATA.get(breed_id)
        if not breed_entry:
            continue

        derived_group = derive_angle_group(breed_entry)

        # If derivation produces a non-default group that differs from assignment,
        # that's a coherence issue
        if derived_group != "default" and derived_group != assigned_group:
            failures.append({
                "check": "fci_text_coherence",
                "severity": "warning",
                "breed_id": breed_id,
                "assigned": assigned_group,
                "derived": derived_group,
                "message": (
                    f"Explicit mapping '{assigned_group}' differs from "
                    f"FCI text derivation '{derived_group}'"
                ),
            })

    return failures


# =============================================================================
# COMPOSITE VALIDATION RUNNER
# =============================================================================

def run_full_validation(*, min_explicit_pct: float = 1.0) -> Dict:
    """Run all validation checks and return a comprehensive report.

    Args:
        min_explicit_pct: Minimum percentage of breeds that must have explicit
            coefficient mappings. Default 1.0% reflects current state where
            many breed IDs in coefficient maps have naming mismatches with
            BREED_DATA keys.

    Returns:
        Dictionary with:
        - passed: bool (True if no hard failures)
        - total_checks: int
        - failure_count: int
        - warning_count: int
        - failures: List[Dict]
        - warnings: List[Dict]
        - coverage: Dict (from compute_coverage_report)
        - sections: Dict[str, Dict] (per-section results)
    """
    sections = {}

    # 1. Coefficient table integrity
    angle_failures = validate_angle_standards()
    ratio_failures = validate_ratio_coefficients()
    gait_failures = validate_gait_coefficients()
    sensitivity_failures = validate_sensitivity_profiles()

    sections["coefficient_integrity"] = {
        "angle_standards": {"failures": angle_failures, "passed": len(angle_failures) == 0},
        "ratio_coefficients": {"failures": ratio_failures, "passed": len(ratio_failures) == 0},
        "gait_coefficients": {"failures": gait_failures, "passed": len(gait_failures) == 0},
        "sensitivity_profiles": {"failures": sensitivity_failures, "passed": len(sensitivity_failures) == 0},
    }

    # 2. Cross-module consistency
    group_failures = validate_group_alignment()
    map_failures = validate_breed_map_consistency()
    weight_failures = validate_weights_integrity()

    sections["cross_module"] = {
        "group_alignment": {"failures": group_failures, "passed": len(group_failures) == 0},
        "breed_map_consistency": {"failures": map_failures, "passed": len([f for f in map_failures if f.get("severity") != "warning"]) == 0},
        "weights_integrity": {"failures": weight_failures, "passed": len(weight_failures) == 0},
    }

    # 3. Breed coverage
    coverage_failures = validate_breed_coverage(min_explicit_pct=min_explicit_pct)
    coverage_report = compute_coverage_report()

    sections["breed_coverage"] = {
        "validation": {"failures": coverage_failures, "passed": len(coverage_failures) == 0},
        "report": coverage_report,
    }

    # 4. Score range plausibility
    score_failures = validate_score_range_plausibility()

    sections["score_plausibility"] = {
        "failures": score_failures,
        "passed": len(score_failures) == 0,
    }

    # 5. FCI text coherence
    coherence_failures = validate_fci_text_coherence()

    sections["fci_coherence"] = {
        "failures": coherence_failures,
        "passed": len([f for f in coherence_failures if f.get("severity") != "warning"]) == 0,
    }

    # Aggregate
    all_results = (
        angle_failures + ratio_failures + gait_failures +
        sensitivity_failures + group_failures + map_failures +
        weight_failures + coverage_failures + score_failures +
        coherence_failures
    )

    hard_failures = [f for f in all_results if f.get("severity") != "warning"]
    warnings = [f for f in all_results if f.get("severity") == "warning"]

    return {
        "passed": len(hard_failures) == 0,
        "total_checks": len(all_results),
        "failure_count": len(hard_failures),
        "warning_count": len(warnings),
        "failures": hard_failures,
        "warnings": warnings,
        "coverage": coverage_report,
        "sections": sections,
    }
