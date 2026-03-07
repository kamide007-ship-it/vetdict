#!/usr/bin/env python3
"""
ShowDog Analysis Platform - Deterministic Scoring Core

This module implements the IMMUTABLE scoring algorithm as defined in
docs/Algorithm_Declaration.md

IMPORTANT: This module contains hard-coded weights and formulas.
Any modifications require formal version change process per
docs/Model_Governance.md
"""

import hashlib
import json
from datetime import datetime
from typing import Dict, Optional, Tuple

# =============================================================================
# VERSION CONSTANTS (IMMUTABLE)
# =============================================================================

ALGORITHM_VERSION = "2.0.0"  # v2: Algorithm-first architecture (AI non-dependent)
MODEL_VERSION = "gpt-4o-20260206"

# =============================================================================
# FIXED WEIGHTS (IMMUTABLE - DO NOT MODIFY)
# =============================================================================
# These weights are hard-coded as per Algorithm_Declaration.md
# Any modification requires a new algorithm version

WEIGHTS: Dict[str, float] = {
    "skeletal": 0.25,      # 25% - Skeletal structure
    "gait": 0.25,          # 25% - Movement/gait
    "muscle": 0.20,        # 20% - Muscle development
    "coat": 0.20,          # 20% - Coat quality (increased from 15%)
    "temperament": 0.10    # 10% - Temperament
}  # Total: 100%

# Verify weights sum to 1.0
assert abs(sum(WEIGHTS.values()) - 1.0) < 0.0001, "Weights must sum to 1.0"

# =============================================================================
# WEIGHTS HASH (for audit verification)
# =============================================================================

def compute_weights_hash() -> str:
    """Compute SHA256 hash of weights for tamper detection."""
    weights_json = json.dumps(WEIGHTS, sort_keys=True)
    return hashlib.sha256(weights_json.encode()).hexdigest()[:16]

WEIGHTS_HASH = compute_weights_hash()

# =============================================================================
# AGE ADJUSTMENT TABLE (IMMUTABLE)
# =============================================================================

def get_age_adjustment(age_months: int) -> int:
    """
    Get deterministic age adjustment.

    Args:
        age_months: Age in months (integer)

    Returns:
        Integer adjustment between -5 and +5

    Age adjustment rationale:
    - Puppies: Incomplete development
    - Young adults: Near maturity
    - Prime adults: Peak condition
    - Veterans: Age-related changes
    """
    if age_months < 0:
        age_months = 0

    if age_months <= 6:
        return -5
    elif age_months <= 12:
        return -3
    elif age_months <= 24:
        return -1
    elif age_months <= 84:  # 2-7 years
        return 0
    elif age_months <= 108:  # 7-9 years
        return -1
    elif age_months <= 132:  # 9-11 years
        return -3
    else:  # 11+ years
        return -5


def age_years_to_months(age_years: float) -> int:
    """Convert age in years (float) to months (int)."""
    return int(round(age_years * 12))

# =============================================================================
# GRADE BOUNDARIES (IMMUTABLE)
# =============================================================================

GRADE_BOUNDARIES = [
    # ShowDog grade | FCI equivalent      | Score range
    # S  (卓越)      Excellent (top tier)   95-100
    # A+ (優秀)      Excellent              90-94
    # A  (良好)      Very Good (top tier)   85-89
    # B+ (標準以上)   Very Good              80-84
    # B  (標準)      Good                   70-79
    # C  (要改善)     Sufficient / below     0-69
    (95, "S", "S (卓越)"),
    (90, "A+", "A+ (優秀)"),
    (85, "A", "A (良好)"),
    (80, "B+", "B+ (標準以上)"),
    (70, "B", "B (標準)"),
    (0, "C", "C (要改善)")
]

# FCI Official Grading (4 grades per FCI Show Regulations)
# Reference: FCI Regulations for Dog Shows, Chapter V, Article 20
FCI_GRADE_MAP = {
    "S": ("Excellent", "エクセレント"),
    "A+": ("Excellent", "エクセレント"),
    "A": ("Very Good", "ベリーグッド"),
    "B+": ("Very Good", "ベリーグッド"),
    "B": ("Good", "グッド"),
    "C": ("Sufficient", "サフィシエント"),
}


def get_grade(score: float) -> Tuple[str, str]:
    """
    Get grade from score.

    Args:
        score: Final score (0-100)

    Returns:
        Tuple of (grade_short, grade_full)
    """
    for threshold, grade, grade_full in GRADE_BOUNDARIES:
        if score >= threshold:
            return grade, grade_full
    return "C", "C (要改善)"


def get_fci_grade(showdog_grade: str) -> Tuple[str, str]:
    """
    Map ShowDog grade to FCI official grade.

    FCI uses 4 grades: Excellent, Very Good, Good, Sufficient
    (per FCI Show Regulations, Chapter V, Article 20)

    Args:
        showdog_grade: ShowDog grade code (S, A+, A, B+, B, C)

    Returns:
        Tuple of (fci_grade_en, fci_grade_ja)
    """
    return FCI_GRADE_MAP.get(showdog_grade, ("Sufficient", "サフィシエント"))

# =============================================================================
# CORE SCORING FUNCTION
# =============================================================================

def calculate_score(
    axis_scores: Dict[str, float],
    age_years: float,
    validate: bool = True
) -> Dict:
    """
    Calculate deterministic final score.

    This is the SINGLE SOURCE OF TRUTH for all scoring.
    All numeric scores in the system MUST pass through this function.

    Args:
        axis_scores: Dictionary with keys: skeletal, gait, muscle, coat, temperament
                     Each value should be 0-100
        age_years: Age in years (float, e.g., 3.5)
        validate: Whether to validate inputs (default True)

    Returns:
        Dictionary with:
        - weighted_sum: Pre-adjustment weighted sum
        - age_adjustment: Applied age adjustment
        - final_score: Clamped final score
        - grade: Grade code (S, A+, A, B+, B, C)
        - grade_full: Full grade description
        - algorithm_version: Current algorithm version
        - model_version: Current model version
        - weights_hash: Hash for verification
        - axis_scores: Normalized axis scores used
        - calculation_timestamp: ISO timestamp

    Raises:
        ValueError: If required axis is missing or scores out of range
    """
    # Validate inputs
    if validate:
        required_axes = set(WEIGHTS.keys())
        provided_axes = set(axis_scores.keys())
        missing = required_axes - provided_axes

        if missing:
            raise ValueError(f"Missing required axes: {missing}")

    # Normalize and clamp axis scores
    normalized_scores = {}
    for axis, _weight in WEIGHTS.items():
        raw_score = axis_scores.get(axis, 0)

        # Ensure numeric
        if raw_score is None:
            raw_score = 0

        # Clamp to valid range
        score = max(0, min(100, float(raw_score)))
        normalized_scores[axis] = score

    # Calculate weighted sum
    weighted_sum = sum(
        normalized_scores[axis] * weight
        for axis, weight in WEIGHTS.items()
    )

    # Apply age adjustment
    age_months = age_years_to_months(age_years)
    age_adj = get_age_adjustment(age_months)

    # Calculate final score (clamped)
    final_score = max(0, min(100, weighted_sum + age_adj))
    final_score = round(final_score, 1)

    # Get grade
    grade, grade_full = get_grade(final_score)
    fci_grade_en, fci_grade_ja = get_fci_grade(grade)

    return {
        "weighted_sum": round(weighted_sum, 2),
        "age_months": age_months,
        "age_adjustment": age_adj,
        "final_score": final_score,
        "grade": grade,
        "grade_full": grade_full,
        "fci_grade": fci_grade_en,
        "fci_grade_ja": fci_grade_ja,
        "algorithm_version": ALGORITHM_VERSION,
        "model_version": MODEL_VERSION,
        "weights_hash": WEIGHTS_HASH,
        "axis_scores": normalized_scores,
        "weights": WEIGHTS.copy(),
        "calculation_timestamp": datetime.utcnow().isoformat() + "Z"
    }

# =============================================================================
# MAPPING FROM AI SCORES TO AXIS SCORES
# =============================================================================

def map_ai_scores_to_axes(
    structure_score: Optional[float] = None,
    structure_details: Optional[Dict] = None,
    coat_score: Optional[float] = None,
    gait_score: Optional[float] = None,
    gait_details: Optional[Dict] = None,
    temperament_score: Optional[float] = None,
    temperament_details: Optional[Dict] = None
) -> Dict[str, float]:
    """
    Map AI-provided scores to the 5 canonical evaluation axes.

    This function translates the various scores from AI analysis
    into the fixed axis format required by the scoring algorithm.

    Args:
        structure_score: Overall structure score from photo analysis
        structure_details: Detailed structure breakdown (proportion, skeletal, muscular)
        coat_score: Coat quality score
        gait_score: Gait score from video analysis
        gait_details: Detailed gait breakdown (stride, balance, fluidity)
        temperament_score: Temperament score from video analysis
        temperament_details: Detailed temperament breakdown

    Returns:
        Dictionary with keys: skeletal, gait, muscle, coat, temperament
    """
    # Default scores (used when data not available)
    DEFAULT_SCORE = 75.0

    # Extract skeletal score
    if structure_details and "skeletal" in structure_details:
        skeletal = float(structure_details.get("skeletal", DEFAULT_SCORE))
    elif structure_details and "proportion" in structure_details:
        # Use proportion as proxy for skeletal if direct score not available
        skeletal = float(structure_details.get("proportion", DEFAULT_SCORE))
    elif structure_score is not None:
        skeletal = float(structure_score)
    else:
        skeletal = DEFAULT_SCORE

    # Extract muscle score
    if structure_details and "muscular" in structure_details:
        muscle = float(structure_details.get("muscular", DEFAULT_SCORE))
    elif structure_score is not None:
        # Use structure score as proxy
        muscle = float(structure_score) * 0.95  # Slight reduction
    else:
        muscle = DEFAULT_SCORE

    # Extract gait score
    if gait_score is not None:
        gait = float(gait_score)
    elif gait_details:
        # Average of gait components
        components = ["stride", "balance", "fluidity"]
        values = [float(gait_details.get(c, DEFAULT_SCORE)) for c in components if c in gait_details]
        gait = sum(values) / len(values) if values else DEFAULT_SCORE
    else:
        gait = DEFAULT_SCORE

    # Extract coat score
    coat = float(coat_score) if coat_score is not None else DEFAULT_SCORE

    # Extract temperament score
    if temperament_score is not None:
        temperament = float(temperament_score)
    elif temperament_details:
        # Average of temperament components
        components = ["confidence", "alertness", "composure"]
        values = [float(temperament_details.get(c, DEFAULT_SCORE)) for c in components if c in temperament_details]
        temperament = sum(values) / len(values) if values else DEFAULT_SCORE
    else:
        temperament = DEFAULT_SCORE

    return {
        "skeletal": skeletal,
        "gait": gait,
        "muscle": muscle,
        "coat": coat,
        "temperament": temperament
    }

# =============================================================================
# HYBRID PIPELINE: ALGORITHM (主導) → AI CORRECTION (伴奏)
# =============================================================================

# Maximum AI correction magnitude per axis (keeps algorithm as primary)
AI_CORRECTION_CAP = 8.0  # AI can adjust each axis by at most ±8 points

# =============================================================================
# BREED-SPECIFIC CORRECTION SENSITIVITY (犬種別補正感度)
# =============================================================================
# Each breed type emphasizes different axes. A coat deviation matters far more
# for a Poodle than a Labrador. These multipliers modulate correction strength.
# Values > 1.0 = this axis matters MORE for this breed type
# Values < 1.0 = this axis matters LESS for this breed type

BREED_SENSITIVITY_PROFILES: Dict[str, Dict[str, float]] = {
    # Coat-dominant breeds (show coat is defining feature)
    "coat_dominant": {
        "skeletal": 0.9, "gait": 0.8, "muscle": 0.7,
        "coat": 1.6, "temperament": 1.0
    },
    # Structure-dominant breeds (working/sport builds)
    "structure_dominant": {
        "skeletal": 1.5, "gait": 1.2, "muscle": 1.3,
        "coat": 0.6, "temperament": 0.9
    },
    # Gait-dominant breeds (movement is key evaluation)
    "gait_dominant": {
        "skeletal": 1.1, "gait": 1.6, "muscle": 1.0,
        "coat": 0.7, "temperament": 0.9
    },
    # Temperament-dominant breeds (character/working ability)
    "temperament_dominant": {
        "skeletal": 0.8, "gait": 0.9, "muscle": 0.8,
        "coat": 0.7, "temperament": 1.8
    },
    # Balanced breeds (no single axis dominates)
    "balanced": {
        "skeletal": 1.0, "gait": 1.0, "muscle": 1.0,
        "coat": 1.0, "temperament": 1.0
    },
}

# Map breed IDs to sensitivity profiles
BREED_PROFILE_MAP: Dict[str, str] = {
    # Coat-dominant
    "172d_poodle_toy": "coat_dominant",
    "172_poodle_standard": "coat_dominant",
    "172m_poodle_miniature": "coat_dominant",
    "172n_poodle_medium": "coat_dominant",
    "206_maltese": "coat_dominant",
    "009_yorkshire_terrier": "coat_dominant",
    "016_shih_tzu": "coat_dominant",
    "039_bichon_frise": "coat_dominant",
    "195_pomeranian": "coat_dominant",
    "004_yorkshire_terrier": "coat_dominant",
    "262_afghan_hound": "coat_dominant",
    "010_papillon": "coat_dominant",
    # Structure-dominant
    "122_labrador_retriever": "structure_dominant",
    "111_golden_retriever": "structure_dominant",
    "144_rottweiler": "structure_dominant",
    "235_boxer": "structure_dominant",
    "153_dobermann": "structure_dominant",
    "058_bulldog_english": "structure_dominant",
    "101_great_dane": "structure_dominant",
    "110_dalmatian": "structure_dominant",
    "057_bulldog_french": "structure_dominant",
    "343_bull_terrier": "structure_dominant",
    "065_mastiff": "structure_dominant",
    "332_staffordshire_bull_terrier": "structure_dominant",
    # Gait-dominant
    "166_german_shepherd": "gait_dominant",
    "156_weimaraner": "gait_dominant",
    "099_vizsla": "gait_dominant",
    "002_collie_border": "gait_dominant",
    "297_australian_shepherd": "gait_dominant",
    "251_whippet": "gait_dominant",
    "158_siberian_husky": "gait_dominant",
    "270_saluki": "gait_dominant",
    "162_alaskan_malamute": "gait_dominant",
    # Temperament-dominant
    "218_akita": "temperament_dominant",
    "257_shiba_inu": "temperament_dominant",
    "315_chow_chow": "temperament_dominant",
    "044_cavalier_king_charles": "temperament_dominant",
    "264_basenji": "temperament_dominant",
}


def get_breed_sensitivity(breed_id: Optional[str]) -> Dict[str, float]:
    """Get correction sensitivity profile for a breed."""
    if not breed_id:
        return BREED_SENSITIVITY_PROFILES["balanced"]
    profile_key = BREED_PROFILE_MAP.get(breed_id, "balanced")
    return BREED_SENSITIVITY_PROFILES[profile_key]


# =============================================================================
# SUB-SCORE AGGREGATION (全サブスコア集約)
# =============================================================================

def aggregate_ai_correction(
    sub_scores: Dict[str, float],
    base_axis_score: float,
    breed_sensitivity: float = 1.0
) -> float:
    """
    Aggregate multiple AI sub-scores into a single correction delta.

    Instead of picking ONE sub-score, this uses all available sub-scores
    to compute a weighted correction that captures the full signal.

    Args:
        sub_scores: Dict of sub-score name → value (0-100)
        base_axis_score: The algorithm's base score for this axis
        breed_sensitivity: Breed-specific multiplier for this axis

    Returns:
        Correction delta (will be capped later by hybrid_score)
    """
    if not sub_scores:
        return 0.0

    # Compute mean deviation from base axis score
    deviations = []
    for _name, value in sub_scores.items():
        if value is not None:
            deviations.append(float(value) - base_axis_score)

    if not deviations:
        return 0.0

    mean_deviation = sum(deviations) / len(deviations)

    # Confidence factor: more sub-scores = more confident in correction
    # 1 sub-score: 60% confidence, 2: 80%, 3+: 100%
    confidence = min(1.0, 0.4 + 0.2 * len(deviations))

    # Apply breed sensitivity and confidence
    # Base scaling: 0.25 (conservative — algorithm leads, AI fine-tunes)
    correction = mean_deviation * 0.25 * confidence * breed_sensitivity

    return correction


# =============================================================================
# CROSS-AXIS CONSISTENCY VALIDATION (軸間整合性検証)
# =============================================================================

# Axes that should correlate positively (high skeletal → likely high gait)
AXIS_CORRELATIONS = [
    ("skeletal", "gait", 0.6),       # Good skeleton → good movement
    ("skeletal", "muscle", 0.7),     # Good frame → good muscle attachment
    ("gait", "temperament", 0.4),    # Good movement → often good attitude
]


def validate_cross_axis_consistency(
    axis_scores: Dict[str, float]
) -> Dict:
    """
    Check if axis scores are internally consistent.

    Large unexpected divergences between correlated axes may indicate
    measurement error or unusual specimens worth flagging.

    Returns:
        Dict with anomalies list and consistency_score (0-1)
    """
    anomalies = []
    total_penalty = 0.0

    for axis_a, axis_b, expected_r in AXIS_CORRELATIONS:
        score_a = axis_scores.get(axis_a, 75)
        score_b = axis_scores.get(axis_b, 75)
        # Divergence: how far apart are they relative to expected correlation?
        divergence = abs(score_a - score_b)
        # Threshold: lower correlation expectation → higher divergence allowed
        threshold = 25 * (1 - expected_r)  # e.g. r=0.7 → threshold=7.5

        if divergence > threshold:
            severity = (divergence - threshold) / 25  # 0-1 scale
            anomalies.append({
                "axes": [axis_a, axis_b],
                "divergence": round(divergence, 1),
                "threshold": round(threshold, 1),
                "severity": round(min(1.0, severity), 2),
                "note": f"{axis_a}({score_a:.0f}) vs {axis_b}({score_b:.0f}): "
                        f"乖離{divergence:.0f}点（閾値{threshold:.0f}）"
            })
            total_penalty += severity

    consistency = max(0.0, 1.0 - total_penalty * 0.2)

    return {
        "consistency_score": round(consistency, 3),
        "anomalies": anomalies,
        "axes_checked": len(AXIS_CORRELATIONS)
    }


# =============================================================================
# HYBRID SCORE (upgraded)
# =============================================================================

def hybrid_score(
    algorithm_axis_scores: Dict[str, float],
    ai_observations: Optional[Dict[str, float]],
    age_years: float,
    breed_id: Optional[str] = None,
    sub_scores: Optional[Dict[str, Dict[str, float]]] = None
) -> Dict:
    """
    Two-layer hybrid scoring pipeline (v2 — enhanced precision).

    Layer 1 (主導): Deterministic algorithm coefficients calculate base scores
                    using fixed weights, age adjustment, and grade boundaries.
    Layer 2 (伴奏): AI observations provide breed-specific corrections using
                    full sub-score aggregation with confidence weighting.
    Layer 3 (検証): Cross-axis consistency validation flags anomalies.

    Args:
        algorithm_axis_scores: Base axis scores from deterministic evaluation
        ai_observations: AI-provided correction deltas per axis (legacy format).
                        If sub_scores is provided, this is ignored in favor of
                        the more precise sub-score aggregation.
        age_years: Age in years (float)
        breed_id: Breed identifier for breed-specific correction sensitivity
        sub_scores: Optional detailed sub-scores per axis for precision correction.
                   Format: {"skeletal": {"proportion": 88, "skeletal": 86}, ...}

    Returns:
        Dictionary with full pipeline breakdown including consistency validation.
    """
    # === LAYER 1: Algorithm (主導) ===
    base_result = calculate_score(algorithm_axis_scores, age_years)

    # === LAYER 2: AI Correction (伴奏) ===
    breed_sensitivity = get_breed_sensitivity(breed_id)
    ai_corrections_applied = {}
    corrected_axis_scores = dict(algorithm_axis_scores)

    if sub_scores:
        # v2: Full sub-score aggregation (preferred)
        for axis in WEIGHTS:
            axis_subs = sub_scores.get(axis)
            if axis_subs:
                sensitivity = breed_sensitivity.get(axis, 1.0)
                base_val = algorithm_axis_scores.get(axis, 75)
                raw_correction = aggregate_ai_correction(
                    axis_subs, base_val, sensitivity
                )
                capped_correction = max(-AI_CORRECTION_CAP,
                                       min(AI_CORRECTION_CAP, raw_correction))
                corrected_axis_scores[axis] = max(0, min(100,
                    base_val + capped_correction))
                ai_corrections_applied[axis] = {
                    "method": "sub_score_aggregation",
                    "sub_scores_used": len(axis_subs),
                    "breed_sensitivity": round(sensitivity, 2),
                    "raw_correction": round(raw_correction, 2),
                    "capped_correction": round(capped_correction, 2),
                    "base_score": round(base_val, 2),
                    "corrected_score": round(corrected_axis_scores[axis], 2)
                }
    elif ai_observations:
        # v1 legacy: single-value corrections
        for axis in WEIGHTS:
            if axis in ai_observations:
                sensitivity = breed_sensitivity.get(axis, 1.0)
                raw_correction = float(ai_observations[axis]) * sensitivity
                capped_correction = max(-AI_CORRECTION_CAP,
                                       min(AI_CORRECTION_CAP, raw_correction))
                corrected_axis_scores[axis] = max(0, min(100,
                    algorithm_axis_scores.get(axis, 75) + capped_correction))
                ai_corrections_applied[axis] = {
                    "method": "legacy_delta",
                    "breed_sensitivity": round(sensitivity, 2),
                    "raw_correction": round(raw_correction, 2),
                    "capped_correction": round(capped_correction, 2),
                    "base_score": round(algorithm_axis_scores.get(axis, 75), 2),
                    "corrected_score": round(corrected_axis_scores[axis], 2)
                }

    # Recalculate with corrected scores
    final_result = calculate_score(corrected_axis_scores, age_years) if ai_corrections_applied else base_result

    # === LAYER 3: Cross-axis consistency validation (検証) ===
    consistency = validate_cross_axis_consistency(corrected_axis_scores)

    # Compute data completeness (how many axes have real data vs defaults)
    axes_with_data = sum(1 for v in algorithm_axis_scores.values()
                        if v != 75.0)  # 75 = default/no-data
    data_completeness = axes_with_data / len(WEIGHTS)

    # Confidence rating based on data completeness + consistency + sub-score depth
    sub_score_count = sum(len(v) for v in (sub_scores or {}).values())
    confidence_factors = {
        "data_completeness": round(data_completeness, 2),
        "consistency": consistency["consistency_score"],
        "sub_score_depth": min(1.0, sub_score_count / 10),  # 10+ subs = max
    }
    overall_confidence = (
        confidence_factors["data_completeness"] * 0.4 +
        confidence_factors["consistency"] * 0.3 +
        confidence_factors["sub_score_depth"] * 0.3
    )

    breed_profile = BREED_PROFILE_MAP.get(breed_id, "balanced") if breed_id else "balanced"

    return {
        "pipeline": "algorithm_first_ai_corrects_v2",
        "layer1_algorithm": {
            "description": "決定論的アルゴリズム係数（主導）",
            "axis_scores": {k: round(v, 2) for k, v in algorithm_axis_scores.items()},
            "weighted_sum": base_result["weighted_sum"],
            "age_adjustment": base_result["age_adjustment"],
            "base_score": base_result["final_score"],
            "base_grade": base_result["grade"]
        },
        "layer2_ai_correction": {
            "description": "AI犬種特性補正（伴奏）",
            "corrections_applied": bool(ai_corrections_applied),
            "correction_cap": AI_CORRECTION_CAP,
            "breed_profile": breed_profile,
            "breed_sensitivity": {k: round(v, 2) for k, v in breed_sensitivity.items()},
            "corrections": ai_corrections_applied
        },
        "layer3_validation": {
            "description": "軸間整合性検証",
            "consistency": consistency
        },
        "confidence": {
            "overall": round(overall_confidence, 3),
            "factors": confidence_factors
        },
        "final_result": final_result,
        "breed_id": breed_id
    }


# =============================================================================
# AUDIT RECORD CREATION
# =============================================================================

def create_audit_record(
    analysis_id: Optional[int],
    input_type: str,
    axis_scores: Dict[str, float],
    score_result: Dict,
    user_id: Optional[int] = None,
    dog_id: Optional[int] = None
) -> Dict:
    """
    Create an audit record for an analysis.

    Args:
        analysis_id: Database ID of the analysis (if saved)
        input_type: "photo", "video", or "both"
        axis_scores: The axis scores used
        score_result: Result from calculate_score()
        user_id: User ID (if authenticated)
        dog_id: Dog ID (if specified)

    Returns:
        Audit record dictionary
    """
    return {
        "analysis_id": analysis_id,
        "user_id": user_id,
        "dog_id": dog_id,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "algorithm_version": ALGORITHM_VERSION,
        "model_version": MODEL_VERSION,
        "weights_hash": WEIGHTS_HASH,
        "input_type": input_type,
        "axis_scores": axis_scores,
        "final_score": score_result["final_score"],
        "grade": score_result["grade"]
    }

# =============================================================================
# VERIFICATION UTILITIES
# =============================================================================

def verify_reproducibility(
    axis_scores: Dict[str, float],
    age_years: float,
    expected_score: float,
    expected_grade: str
) -> Tuple[bool, str]:
    """
    Verify that scoring is reproducible.

    Args:
        axis_scores: The axis scores to test
        age_years: Age in years
        expected_score: Expected final score
        expected_grade: Expected grade

    Returns:
        Tuple of (is_valid, message)
    """
    result = calculate_score(axis_scores, age_years)

    score_match = abs(result["final_score"] - expected_score) < 0.1
    grade_match = result["grade"] == expected_grade

    if score_match and grade_match:
        return True, "Reproducibility verified"
    else:
        return False, f"Mismatch: got {result['final_score']}/{result['grade']}, expected {expected_score}/{expected_grade}"


def get_algorithm_info() -> Dict:
    """Get current algorithm information for display."""
    return {
        "algorithm_version": ALGORITHM_VERSION,
        "model_version": MODEL_VERSION,
        "weights_hash": WEIGHTS_HASH,
        "weights": WEIGHTS.copy(),
        "grade_boundaries": [
            {"min_score": b[0], "grade": b[1], "description": b[2]}
            for b in GRADE_BOUNDARIES
        ]
    }

# =============================================================================
# SELF-TEST (run with: python -m api.scoring)
# =============================================================================

def _self_test():
    """Run self-tests to verify scoring correctness."""
    print("=" * 60)
    print("ShowDog Scoring Core - Self Test")
    print("=" * 60)

    print(f"\nAlgorithm Version: {ALGORITHM_VERSION}")
    print(f"Model Version: {MODEL_VERSION}")
    print(f"Weights Hash: {WEIGHTS_HASH}")
    print(f"Weights: {WEIGHTS}")

    # Test 1: Basic scoring
    print("\n--- Test 1: Basic Scoring ---")
    test_scores = {
        "skeletal": 85,
        "gait": 80,
        "muscle": 82,
        "coat": 88,
        "temperament": 90
    }
    result = calculate_score(test_scores, age_years=3.0)
    print(f"Input: {test_scores}, Age: 3 years")
    print(f"Weighted Sum: {result['weighted_sum']}")
    print(f"Age Adjustment: {result['age_adjustment']}")
    print(f"Final Score: {result['final_score']}")
    print(f"Grade: {result['grade_full']}")

    # Test 2: Age adjustments
    print("\n--- Test 2: Age Adjustments ---")
    for age_months in [3, 10, 18, 48, 96, 120, 150]:
        adj = get_age_adjustment(age_months)
        print(f"  Age {age_months} months: adjustment = {adj:+d}")

    # Test 3: Reproducibility
    print("\n--- Test 3: Reproducibility ---")
    result1 = calculate_score(test_scores, age_years=3.0)
    result2 = calculate_score(test_scores, age_years=3.0)
    assert result1["final_score"] == result2["final_score"], "Reproducibility FAILED"
    print("  Two identical calls produce identical scores: PASS")

    # Test 4: Grade boundaries
    print("\n--- Test 4: Grade Boundaries ---")
    for test_score in [98, 92, 87, 82, 75, 60]:
        grade, grade_full = get_grade(test_score)
        print(f"  Score {test_score}: {grade_full}")

    print("\n" + "=" * 60)
    print("All self-tests PASSED")
    print("=" * 60)


if __name__ == "__main__":
    _self_test()
