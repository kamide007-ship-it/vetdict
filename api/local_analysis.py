"""
Local image/video analysis using OpenCV.
PRIMARY analysis engine — algorithm-first architecture.

The algorithm is the primary scorer; AI provides optional correction only.
This module implements deterministic, measurement-based evaluation:

Photo Analysis:
  - Silhouette → center lines for each body part
  - Angle measurement between body parts (shoulder, rear, head carriage, tail set)
  - Ratio calculation (body length:height, head:body, limb proportions)
  - Comparison with breed-specific FCI standard DB
  - Fine-grained coefficients for natural score variability

Video Analysis:
  - Per-frame skeleton detection and center line tracking
  - Stride length measurement from center line displacement
  - Pitch (body angle oscillation) measurement across frames
  - Gait cycle regularity analysis
  - Comparison with breed-specific FCI gait standards
"""

import base64
import contextlib
import logging
import math

import numpy as np

from api.errors import AnalysisError

logger = logging.getLogger(__name__)

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    logger.warning("OpenCV not available – local analysis will return default scores")


# =============================================================================
# BREED-SPECIFIC STRUCTURAL COEFFICIENTS (犬種別構造係数)
# =============================================================================
# Fine-grained coefficients for deterministic scoring with natural variability.
# Each breed group has ideal angles, ratios, and tolerance ranges from FCI standards.
# Score = f(measured_value, ideal_value, tolerance, coefficient_weight)

# Ideal joint angles in degrees (FCI-based)
BREED_ANGLE_STANDARDS = {
    # Format: (ideal_angle_deg, tolerance_deg, weight)
    "default": {
        "shoulder_angle": (100, 15, 0.20),       # Spine-to-front-leg: ~90-110°
        "rear_angle": (100, 15, 0.20),            # Spine-to-rear-leg: ~90-110°
        "head_carriage": (45, 20, 0.15),          # Head-to-spine angle
        "tail_set": (30, 25, 0.10),               # Tail-to-spine angle
        "topline_straightness": (1.0, 0.3, 0.20), # 1.0 = perfectly straight
        "front_leg_symmetry": (1.0, 0.2, 0.08),   # 1.0 = perfectly symmetric
        "rear_leg_symmetry": (1.0, 0.2, 0.07),    # 1.0 = perfectly symmetric
    },
    "herding": {  # GSD, Border Collie, etc.
        "shoulder_angle": (95, 10, 0.22),
        "rear_angle": (105, 12, 0.22),
        "head_carriage": (40, 15, 0.14),
        "tail_set": (25, 20, 0.10),
        "topline_straightness": (0.95, 0.25, 0.18),  # slight slope OK
        "front_leg_symmetry": (1.0, 0.15, 0.07),
        "rear_leg_symmetry": (1.0, 0.15, 0.07),
    },
    "sporting": {  # Retrievers, Setters
        "shoulder_angle": (100, 12, 0.20),
        "rear_angle": (100, 12, 0.20),
        "head_carriage": (45, 18, 0.15),
        "tail_set": (35, 20, 0.12),
        "topline_straightness": (1.0, 0.2, 0.18),
        "front_leg_symmetry": (1.0, 0.18, 0.08),
        "rear_leg_symmetry": (1.0, 0.18, 0.07),
    },
    "working": {  # Dobermann, Rottweiler, Boxer
        "shoulder_angle": (105, 12, 0.22),
        "rear_angle": (100, 10, 0.22),
        "head_carriage": (50, 18, 0.14),
        "tail_set": (30, 22, 0.10),
        "topline_straightness": (1.0, 0.2, 0.18),
        "front_leg_symmetry": (1.0, 0.15, 0.07),
        "rear_leg_symmetry": (1.0, 0.15, 0.07),
    },
    "toy": {  # Poodle Toy, Chihuahua, Maltese
        "shoulder_angle": (100, 18, 0.18),
        "rear_angle": (100, 18, 0.18),
        "head_carriage": (50, 22, 0.16),
        "tail_set": (40, 25, 0.12),
        "topline_straightness": (1.0, 0.3, 0.18),
        "front_leg_symmetry": (1.0, 0.25, 0.09),
        "rear_leg_symmetry": (1.0, 0.25, 0.09),
    },
    "sighthound": {  # Whippet, Saluki, Afghan
        "shoulder_angle": (95, 10, 0.22),
        "rear_angle": (110, 12, 0.22),
        "head_carriage": (55, 15, 0.14),
        "tail_set": (20, 18, 0.10),
        "topline_straightness": (0.9, 0.25, 0.18),  # graceful arch OK
        "front_leg_symmetry": (1.0, 0.15, 0.07),
        "rear_leg_symmetry": (1.0, 0.15, 0.07),
    },
    "brachycephalic": {  # Bulldog, Pug, French Bulldog
        "shoulder_angle": (105, 18, 0.18),
        "rear_angle": (95, 18, 0.18),
        "head_carriage": (55, 20, 0.16),
        "tail_set": (35, 30, 0.10),
        "topline_straightness": (0.95, 0.3, 0.20),
        "front_leg_symmetry": (1.0, 0.25, 0.09),
        "rear_leg_symmetry": (1.0, 0.25, 0.09),
    },
    "spitz": {  # Shiba, Akita, Husky, Pomeranian
        "shoulder_angle": (105, 15, 0.20),
        "rear_angle": (100, 15, 0.20),
        "head_carriage": (50, 18, 0.16),
        "tail_set": (60, 20, 0.12),  # curled tail higher angle
        "topline_straightness": (1.0, 0.2, 0.18),
        "front_leg_symmetry": (1.0, 0.18, 0.07),
        "rear_leg_symmetry": (1.0, 0.18, 0.07),
    },
}

# Map breed IDs to angle standard groups
BREED_ANGLE_GROUP_MAP = {
    "166_german_shepherd": "herding", "002_collie_border": "herding",
    "297_australian_shepherd": "herding", "156_weimaraner": "herding",
    "122_labrador_retriever": "sporting", "111_golden_retriever": "sporting",
    "099_vizsla": "sporting", "010_papillon": "toy",
    "153_dobermann": "working", "144_rottweiler": "working",
    "235_boxer": "working", "065_mastiff": "working",
    "101_great_dane": "working",
    "172d_poodle_toy": "toy", "206_maltese": "toy",
    "009_yorkshire_terrier": "toy", "004_yorkshire_terrier": "toy",
    "016_shih_tzu": "toy", "039_bichon_frise": "toy",
    "195_pomeranian": "spitz",
    "251_whippet": "sighthound", "270_saluki": "sighthound",
    "262_afghan_hound": "sighthound",
    "058_bulldog_english": "brachycephalic", "057_bulldog_french": "brachycephalic",
    "343_bull_terrier": "brachycephalic",
    "218_akita": "spitz", "257_shiba_inu": "spitz",
    "158_siberian_husky": "spitz", "162_alaskan_malamute": "spitz",
    "315_chow_chow": "spitz",
}

# Body proportion ratio coefficients per breed group
BREED_RATIO_COEFFICIENTS = {
    # Format: (ideal_body_ratio, ratio_tolerance, head_body_coeff, limb_body_coeff)
    "default":         (1.40, 0.25, 0.28, 0.35),
    "herding":         (1.35, 0.20, 0.26, 0.38),
    "sporting":        (1.40, 0.18, 0.30, 0.36),
    "working":         (1.30, 0.20, 0.28, 0.34),
    "toy":             (1.20, 0.30, 0.32, 0.30),
    "sighthound":      (1.50, 0.20, 0.24, 0.42),
    "brachycephalic":  (1.15, 0.30, 0.34, 0.28),
    "spitz":           (1.25, 0.22, 0.30, 0.32),
}

# Gait stride/pitch coefficients per breed group
BREED_GAIT_COEFFICIENTS = {
    # Format: (ideal_stride_ratio, stride_tolerance, ideal_pitch_stability,
    #          pitch_tolerance, cycle_regularity_weight)
    # stride_ratio = displacement_per_frame / spine_length
    "default":         (0.15, 0.08, 0.02, 0.015, 0.25),
    "herding":         (0.18, 0.06, 0.015, 0.012, 0.28),
    "sporting":        (0.16, 0.07, 0.018, 0.012, 0.26),
    "working":         (0.14, 0.07, 0.02, 0.015, 0.24),
    "toy":             (0.12, 0.09, 0.025, 0.02, 0.22),
    "sighthound":      (0.22, 0.06, 0.012, 0.01, 0.30),
    "brachycephalic":  (0.10, 0.10, 0.03, 0.025, 0.20),
    "spitz":           (0.15, 0.08, 0.02, 0.015, 0.25),
}


def _get_breed_angle_group(breed_data):
    """Get the angle standard group for a breed."""
    breed_id = breed_data.get('breed_id', '')
    return BREED_ANGLE_GROUP_MAP.get(breed_id, 'default')


def _get_angle_standards(breed_data):
    """Get breed-specific angle standards."""
    group = _get_breed_angle_group(breed_data)
    return BREED_ANGLE_STANDARDS.get(group, BREED_ANGLE_STANDARDS['default'])


def _get_ratio_coefficients(breed_data):
    """Get breed-specific ratio coefficients."""
    group = _get_breed_angle_group(breed_data)
    return BREED_RATIO_COEFFICIENTS.get(group, BREED_RATIO_COEFFICIENTS['default'])


def _get_gait_coefficients(breed_data):
    """Get breed-specific gait coefficients."""
    group = _get_breed_angle_group(breed_data)
    return BREED_GAIT_COEFFICIENTS.get(group, BREED_GAIT_COEFFICIENTS['default'])


def _angle_deviation_score(measured, ideal, tolerance, scale=1.0):
    """Score an angle measurement against ideal with Gaussian-like falloff.

    Returns 0.0-1.0 where 1.0 = perfect match.
    Uses sigmoid falloff for natural variability instead of linear.
    """
    deviation = abs(measured - ideal)
    # Sigmoid-like falloff: sharp near ideal, gradual away
    normalized = deviation / max(tolerance, 0.01)
    score = 1.0 / (1.0 + normalized ** 2)
    return score * scale


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _decode_base64_image(b64_string):
    """Decode a base64 string into a cv2 image (BGR)."""
    img_bytes = base64.b64decode(b64_string)
    arr = np.frombuffer(img_bytes, dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    return img


def _clamp(value, lo=0.0, hi=100.0):
    return float(max(lo, min(hi, value)))


def _normalize(value, min_val, max_val, target_lo=60.0, target_hi=95.0):
    """Map value from [min_val, max_val] → [target_lo, target_hi], clamped."""
    if max_val <= min_val:
        return float((target_lo + target_hi) / 2)
    ratio = (value - min_val) / (max_val - min_val)
    return _clamp(target_lo + ratio * (target_hi - target_lo))


def _iqr_filter(values, k=1.5):
    """Remove outliers using IQR. Returns filtered list (or original if too few remain)."""
    if len(values) < 4:
        return values
    arr = np.array(values)
    q1, q3 = np.percentile(arr, [25, 75])
    iqr = q3 - q1
    lo = q1 - k * iqr
    hi = q3 + k * iqr
    filtered = arr[(arr >= lo) & (arr <= hi)]
    # Fallback: if IQR removed too many, keep originals
    if len(filtered) < 2:
        return values
    return filtered.tolist()


# ---------------------------------------------------------------------------
# AngleCheck — 撮影アングル推定（簡易）
# ---------------------------------------------------------------------------
# mask の形状特徴から front / side / oblique / unknown を推定する。
# OpenCV + numpy のみ。失敗しても解析全体を落とさない。


def estimate_angle_from_mask(mask):
    """Estimate shooting angle from a dog binary mask.

    Uses aspect ratio (minAreaRect), left-right symmetry (IoU), and convex
    hull solidity to classify the view as front / side / oblique / unknown.

    Args:
        mask: uint8 binary mask (255=dog, 0=background)

    Returns:
        dict with keys: label, confidence, scores, quality, note
    """
    _UNKNOWN = {
        'label': 'unknown', 'confidence': 0.0,
        'scores': {'front': 0.0, 'side': 0.0, 'oblique': 0.0},
        'quality': 'unknown', 'note': '撮影アングル不明',
    }
    if not CV2_AVAILABLE:
        return _UNKNOWN
    try:
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return _UNKNOWN
        cnt = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(cnt)
        h, w = mask.shape[:2]
        if area < h * w * 0.01:
            return {**_UNKNOWN, 'quality': 'low',
                    'note': 'マスク面積が小さすぎます'}

        # --- Feature 1: Aspect ratio via minAreaRect --------------------------
        rect = cv2.minAreaRect(cnt)
        rw, rh = rect[1]
        if rw == 0 or rh == 0:
            return _UNKNOWN
        long_side = max(rw, rh)
        short_side = min(rw, rh)
        aspect = short_side / long_side  # 0..1;  narrow=low, square=high

        # --- Feature 2: Left-right symmetry (IoU) -----------------------------
        flipped = cv2.flip(mask, 1)  # horizontal flip
        intersection = np.count_nonzero(mask & flipped)
        union = np.count_nonzero(mask | flipped)
        symmetry_iou = intersection / max(union, 1)  # 0..1; front views ~ high

        # --- Feature 3: Convex hull solidity ----------------------------------
        hull = cv2.convexHull(cnt)
        hull_area = cv2.contourArea(hull)
        solidity = area / max(hull_area, 1)  # 0..1; compact shapes ~ high

        # --- Score computation ------------------------------------------------
        # Front: high symmetry + high aspect (squarish)
        front_score = symmetry_iou * 0.6 + aspect * 0.3 + solidity * 0.1

        # Side: low aspect (elongated) + lower symmetry
        elongation = 1.0 - aspect
        side_score = elongation * 0.55 + (1.0 - symmetry_iou) * 0.25 + solidity * 0.2

        # Oblique: moderate everything
        oblique_score = (
            (1.0 - abs(symmetry_iou - 0.5) * 2) * 0.4 +
            (1.0 - abs(aspect - 0.5) * 2) * 0.4 +
            solidity * 0.2
        )

        scores = {'front': round(front_score, 3),
                  'side': round(side_score, 3),
                  'oblique': round(oblique_score, 3)}

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        best_label, best_val = ranked[0]
        second_val = ranked[1][1]

        # Confidence = gap between top two
        confidence = min(max((best_val - second_val) / max(best_val, 0.001), 0.0), 1.0)

        # Threshold: if best score is too low, call it unknown
        if best_val < 0.30:
            best_label = 'unknown'
            confidence = 0.0

        _NOTES = {
            'front': '正面からの撮影です。体構造評価には真横（サイドビュー）を推奨します。',
            'side': 'サイドビューです。体構造評価に最適な撮影角度です。',
            'oblique': '斜めからの撮影です。体構造評価には真横（サイドビュー）を推奨します。',
            'unknown': '撮影アングルを判定できませんでした。',
        }

        return {
            'label': best_label,
            'confidence': round(confidence, 3),
            'scores': scores,
            'quality': 'high' if area > h * w * 0.05 else 'low',
            'note': _NOTES.get(best_label, ''),
        }
    except Exception as e:
        logger.warning(f"AngleCheck failed: {e}")
        return _UNKNOWN


# ---------------------------------------------------------------------------
# AngleGate — 比較適格性判定
# ---------------------------------------------------------------------------

def gate_for_comparison(angle_dict, *, mode='photo'):
    """Determine whether an analysis result is eligible for comparison/ranking.

    Args:
        angle_dict: angle info dict from estimate_angle_from_mask (photo)
                    or angle_summary dict (video).  May be None.
        mode: "photo" or "video"

    Returns:
        dict with keys: eligible, required, reason, rule_version
    """
    _RULE = 'angle_gate_v1'
    _FAIL = lambda reason: {
        'eligible': False, 'required': 'side', 'reason': reason,
        'rule_version': _RULE,
    }
    _PASS = {
        'eligible': True, 'required': 'side', 'reason': None,
        'rule_version': _RULE,
    }

    if not angle_dict or not isinstance(angle_dict, dict):
        return _FAIL('unknown')

    label = angle_dict.get('label', 'unknown')
    confidence = float(angle_dict.get('confidence', 0))
    quality = angle_dict.get('quality', 'unknown')

    if label == 'unknown':
        return _FAIL('unknown')
    if label != 'side':
        return _FAIL('angle_not_side')
    if confidence < 0.55:
        return _FAIL('low_confidence')

    if mode == 'photo':
        if quality not in ('high', 'ok'):
            return _FAIL('low_confidence')
        return _PASS

    # mode == "video"
    consistency = float(angle_dict.get('consistency', 0))
    if consistency < 0.60:
        return _FAIL('angle_inconsistent')
    return _PASS


def make_capture_guide(*, mode='photo', comparison=None, angle=None):
    """Generate a 3-line shooting guide based on comparison eligibility.

    Returns dict with keys: lines (list[3]), target, rule_version
    """
    _VER = 'capture_guide_v1'
    eligible = comparison.get('eligible', False) if comparison else False
    reason = comparison.get('reason') if comparison else 'unknown'

    if eligible:
        lines = [
            '✅ 真横（横立ち）で撮れています。この条件を維持してください。',
            '犬の全身（耳〜尾先、足先まで）が1枚に収まる距離で撮影。',
            'カメラは犬の胴体中央の高さ、水平を保ってブレなく撮影。',
        ]
    elif reason == 'angle_inconsistent':
        lines = [
            '📌 動画中の向きが変わっています。横向きで一定に歩かせてください。',
            '撮影者は固定（パンしない）。犬がフレーム中央に収まる距離。',
            '5〜10秒程度、同じ方向に歩く区間を撮影してください。',
        ]
    else:
        lines = [
            '📌 真横（横立ち）で撮り直してください（正面/斜めは比較不可）。',
            '犬の全身が切れない距離で、背景は単色寄り・影が少ない場所。',
            'カメラは胴体中央の高さで水平、できれば連写してベストを選択。',
        ]

    return {'lines': lines, 'target': 'side', 'rule_version': _VER}


# ---------------------------------------------------------------------------
# Quality grading — 入力品質判定 (PASS / HOLD)
# ---------------------------------------------------------------------------

def _clamp_score(v):
    if not isinstance(v, (int, float)):
        v = 0
    return max(0, min(100, int(round(v))))


def grade_photo_quality(structure_result):
    """Grade whether a photo input is suitable for analysis & comparison.

    Returns dict with status, score, reasons, action, rule_version.
    """
    _VER = 'quality_v1'
    reasons = []
    score = 60  # baseline

    # --- angle ---
    angle = structure_result.get('angle') or {}
    label = angle.get('label', 'unknown')
    conf = angle.get('confidence', 0.0)
    quality = angle.get('quality', 'unknown')

    if label == 'side' and conf >= 0.55:
        score += 20
    elif label == 'unknown':
        score -= 30
        reasons.append('angle_unknown')
    else:
        reasons.append('angle_not_side')

    if conf < 0.55 and label != 'unknown':
        score -= 10
        reasons.append('low_confidence')

    if quality in ('low',):
        score -= 20
        reasons.append('mask_low')

    # --- comparison ---
    comp = structure_result.get('comparison') or {}
    if comp.get('eligible'):
        score += 10
    else:
        reasons.append('comparison_hold')

    score = _clamp_score(score)
    status = 'PASS' if not reasons else 'HOLD'
    action = ('真横（横立ち）で全身が入る距離で撮影してください。'
              if status == 'HOLD'
              else '撮影条件は良好です。このまま続けてください。')

    return {'status': status, 'score': score, 'reasons': reasons,
            'action': action, 'rule_version': _VER}


def grade_video_quality(video_result):
    """Grade whether a video input is suitable for gait analysis & comparison.

    Returns dict with status, score, reasons, action, rule_version.
    """
    _VER = 'quality_v1'
    reasons = []
    score = 50  # baseline

    # --- angle_summary ---
    asumm = video_result.get('angle_summary') or {}
    label = asumm.get('label', 'unknown')
    conf = asumm.get('confidence', 0.0)
    consistency = asumm.get('consistency', 0.0)

    if label == 'side' and conf >= 0.55:
        score += 5
    elif label == 'unknown':
        score -= 20
        reasons.append('angle_unknown')
    else:
        reasons.append('angle_not_side')

    if conf < 0.55 and label != 'unknown':
        score -= 10
        reasons.append('low_confidence')

    if consistency >= 0.60:
        score += 10
    else:
        reasons.append('angle_inconsistent')

    # --- comparison ---
    comp = video_result.get('comparison') or {}
    if comp.get('eligible'):
        score += 15
    else:
        reasons.append('comparison_hold')

    # --- segment checks (gait sub-dict) ---
    gait = video_result.get('gait') or {}

    for key in ('dynamic_segment', 'speed_segment'):
        seg = gait.get(key) or {}
        if seg.get('found') and seg.get('length', 0) >= 6:
            score += 8
        else:
            reasons.append(f'no_{key}')
            score -= 10

    score = _clamp_score(score)
    status = 'PASS' if not reasons else 'HOLD'
    action = ('横向きで一定方向に5〜10秒歩く区間を撮影（カメラ固定）。'
              if status == 'HOLD'
              else '撮影条件は良好です。このまま続けてください。')

    return {'status': status, 'score': score, 'reasons': reasons,
            'action': action, 'rule_version': _VER}


# ---------------------------------------------------------------------------
# Motion proxy & dynamic subsegment — 停止/立ち止まり除去
# ---------------------------------------------------------------------------

def compute_motion_proxy(prev_frame, curr_frame, prev_center=None, curr_center=None):
    """Return a scalar motion proxy between two consecutive frames.

    Uses center displacement (hypot) when centers are available, otherwise
    falls back to mean optical-flow magnitude.
    """
    if prev_center is not None and curr_center is not None:
        dx = curr_center[0] - prev_center[0]
        dy = curr_center[1] - prev_center[1]
        return math.hypot(dx, dy)

    # Fallback: lightweight optical flow mean magnitude
    if CV2_AVAILABLE:
        g0 = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY) if prev_frame.ndim == 3 else prev_frame
        g1 = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY) if curr_frame.ndim == 3 else curr_frame
        flow = cv2.calcOpticalFlowFarneback(
            g0, g1, None, pyr_scale=0.5, levels=2, winsize=15,
            iterations=2, poly_n=5, poly_sigma=1.2, flags=0)
        mag, _ = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        return float(np.mean(mag))
    return 0.0


def select_dynamic_subsegment(frames, centers, *, min_len=6):
    """Select the longest moving subsegment, excluding still frames.

    Parameters
    ----------
    frames : list[ndarray]
        Video frames (used only when centers are unavailable).
    centers : list[tuple|None]
        Per-frame center points from centerline detection.
    min_len : int
        Minimum number of consecutive moving frames required.

    Returns
    -------
    dict with keys: found, start, end, length, threshold, avg_motion, reason
    """
    n = len(frames)
    _EMPTY = {'found': False, 'start': 0, 'end': 0, 'length': 0,
              'threshold': 0.0, 'avg_motion': 0.0, 'reason': 'no_motion'}

    if n < 2:
        return _EMPTY

    # --- compute per-transition motion proxy ---
    proxies = []
    for i in range(n - 1):
        pc = centers[i] if centers and i < len(centers) else None
        cc = centers[i + 1] if centers and (i + 1) < len(centers) else None
        proxies.append(compute_motion_proxy(frames[i], frames[i + 1], pc, cc))

    arr = np.array(proxies, dtype=np.float64)
    median = float(np.median(arr))
    if median < 1e-6:
        return _EMPTY

    # --- adaptive threshold from distribution ---
    threshold = median * 0.35
    is_moving = arr >= threshold

    # --- longest run of True (moving) ---
    best_start, best_len = 0, 0
    cur_start, cur_len = 0, 0
    for i, m in enumerate(is_moving):
        if m:
            if cur_len == 0:
                cur_start = i
            cur_len += 1
            if cur_len > best_len:
                best_start, best_len = cur_start, cur_len
        else:
            cur_len = 0

    # +1 because N transitions correspond to N+1 frames
    seg_start = best_start
    seg_end = best_start + best_len + 1  # exclusive end for slice
    seg_length = seg_end - seg_start

    avg_motion = float(np.mean(arr[best_start:best_start + best_len])) if best_len else 0.0

    if seg_length < min_len:
        return {'found': False, 'start': 0, 'end': 0, 'length': seg_length,
                'threshold': round(threshold, 4), 'avg_motion': round(avg_motion, 4),
                'reason': 'min_len_not_met'}

    return {'found': True, 'start': seg_start, 'end': seg_end,
            'length': seg_length, 'threshold': round(threshold, 4),
            'avg_motion': round(avg_motion, 4), 'reason': 'ok'}


def select_speed_normalized_segment(proxies, *, min_len=6, low_q=0.20, high_q=0.95):
    """Select the longest subsegment within a normal speed range.

    Removes frames where the dog moves too fast or too slow compared to
    the overall distribution, improving stride/pitch measurement stability.

    Parameters
    ----------
    proxies : list[float]
        Per-transition motion proxy values (length = frames - 1).
    min_len : int
        Minimum consecutive *frames* (transitions + 1) required.
    low_q, high_q : float
        Quantile thresholds for acceptable speed band.

    Returns
    -------
    dict with keys: found, start, end, length, low_th, high_th, kept_ratio, reason
    """
    _EMPTY = {'found': False, 'start': 0, 'end': 0, 'length': 0,
              'low_th': 0.0, 'high_th': 0.0, 'kept_ratio': 0.0,
              'reason': 'no_proxies'}

    if not proxies or len(proxies) < 2:
        return _EMPTY

    arr = np.array(proxies, dtype=np.float64)
    low_th = float(np.quantile(arr, low_q))
    high_th = float(np.quantile(arr, high_q))

    keep = (arr >= low_th) & (arr <= high_th)
    kept_ratio = float(np.sum(keep) / len(keep)) if len(keep) else 0.0

    # Longest consecutive run of True (kept transitions)
    best_start, best_len = 0, 0
    cur_start, cur_len = 0, 0
    for i, k in enumerate(keep):
        if k:
            if cur_len == 0:
                cur_start = i
            cur_len += 1
            if cur_len > best_len:
                best_start, best_len = cur_start, cur_len
        else:
            cur_len = 0

    # N transitions → N+1 frames
    seg_start = best_start
    seg_end = best_start + best_len + 1
    seg_length = seg_end - seg_start

    if seg_length < min_len:
        return {'found': False, 'start': 0, 'end': 0, 'length': seg_length,
                'low_th': round(low_th, 4), 'high_th': round(high_th, 4),
                'kept_ratio': round(kept_ratio, 4), 'reason': 'min_len_not_met'}

    return {'found': True, 'start': seg_start, 'end': seg_end,
            'length': seg_length, 'low_th': round(low_th, 4),
            'high_th': round(high_th, 4), 'kept_ratio': round(kept_ratio, 4),
            'reason': 'ok'}


# ---------------------------------------------------------------------------
# Centerline (Spine Line) Detection — 中心線検出
# ---------------------------------------------------------------------------
# 犬は毛が生えているためエッジ・輪郭の直接検出は不正確になる。
# 体の中心線（背骨ライン）を先に推定し、それを基準に左右分割することで
# 毛のノイズに左右されない対称性・プロポーション・骨格評価を実現する。


def _detect_centerline_cv(img, mask=None):
    """Detect the dog's body centerline (spine) using OpenCV.

    Uses mask → morphological skeleton → PCA principal axis.
    Returns dict with start, end, center, angle, length, topline_straightness
    or None on failure.
    """
    if not CV2_AVAILABLE:
        return None
    try:
        h, w = img.shape[:2]

        # Get dog mask if not provided
        if mask is None:
            mask, _, _mq = _detect_dog_mask(img)

        # Morphological skeleton: thin the mask down to 1px spine
        skel = np.zeros_like(mask)
        element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
        working = mask.copy()
        while True:
            eroded = cv2.erode(working, element)
            opened = cv2.dilate(eroded, element)
            diff = cv2.subtract(working, opened)
            skel = cv2.bitwise_or(skel, diff)
            working = eroded.copy()
            if cv2.countNonZero(working) == 0:
                break

        # Get skeleton points
        pts = np.column_stack(np.where(skel > 0))  # (row, col)
        if len(pts) < 10:
            # Fallback: use mask contour moments
            pts = np.column_stack(np.where(mask > 0))
            if len(pts) < 10:
                return None

        # PCA to find principal axis
        pts_xy = pts[:, ::-1].astype(np.float32)  # (col, row) = (x, y)
        mean, eigvec = cv2.PCACompute(pts_xy, mean=np.empty(0))
        center = (int(mean[0, 0]), int(mean[0, 1]))
        principal = eigvec[0]  # first eigenvector = major axis direction
        angle = math.atan2(principal[1], principal[0])

        # Project skeleton points onto principal axis to find extent
        centered = pts_xy - mean
        projections = centered @ principal
        min_proj = float(np.min(projections))
        max_proj = float(np.max(projections))
        spine_length = max_proj - min_proj

        # Start/end points along the spine
        start = (int(center[0] + principal[0] * min_proj),
                 int(center[1] + principal[1] * min_proj))
        end = (int(center[0] + principal[0] * max_proj),
               int(center[1] + principal[1] * max_proj))

        # Topline straightness: how well skeleton points fit the line
        # Perpendicular distances from skeleton to the principal axis
        perp_vec = np.array([-principal[1], principal[0]])
        perp_dists = np.abs(centered @ perp_vec)
        mean_deviation = float(np.mean(perp_dists))
        # Normalize by spine length; lower = straighter
        straightness = 1.0 - min(mean_deviation / max(spine_length * 0.1, 1.0), 1.0)

        return {
            'start': start,
            'end': end,
            'center': center,
            'angle': angle,
            'length': spine_length,
            'topline_straightness': straightness,
        }
    except Exception as e:
        logger.warning(f"Centerline CV detection failed: {e}")
        return None


def _numpy_morph_dilate(mask, ksize, iterations=1):
    """Binary dilation using numpy (no scipy)."""
    pad = ksize // 2
    result = mask.copy()
    for _ in range(iterations):
        padded = np.pad(result, pad, mode='constant', constant_values=0)
        out = np.zeros_like(result)
        for dy in range(ksize):
            for dx in range(ksize):
                out |= padded[dy:dy + result.shape[0], dx:dx + result.shape[1]]
        result = out
    return result


def _numpy_morph_erode(mask, ksize, iterations=1):
    """Binary erosion using numpy (no scipy)."""
    pad = ksize // 2
    result = mask.copy()
    for _ in range(iterations):
        padded = np.pad(result, pad, mode='constant', constant_values=0)
        out = np.ones_like(result)
        for dy in range(ksize):
            for dx in range(ksize):
                out &= padded[dy:dy + result.shape[0], dx:dx + result.shape[1]]
        result = out
    return result


def _numpy_morph_close(mask, ksize, iterations=1):
    """Binary closing (dilate then erode) — no scipy."""
    return _numpy_morph_erode(_numpy_morph_dilate(mask, ksize, iterations), ksize, iterations)


def _numpy_morph_open(mask, ksize, iterations=1):
    """Binary opening (erode then dilate) — no scipy."""
    return _numpy_morph_dilate(_numpy_morph_erode(mask, ksize, iterations), ksize, iterations)


def _detect_centerline_pil(pil_img):
    """Detect the dog's body centerline using Pillow + numpy.

    Uses Otsu-like thresholding → moments → principal axis.
    Returns same dict structure as _detect_centerline_cv or None.
    """
    try:
        gray = pil_img.convert('L')
        arr = np.array(gray, dtype=np.float32)
        h, w = arr.shape

        # Simple foreground detection: pixels that differ from border mean
        border = np.concatenate([
            arr[0, :], arr[-1, :], arr[:, 0], arr[:, -1]
        ])
        bg_mean = float(np.mean(border))
        bg_std = float(np.std(border)) + 1.0
        diff_map = np.abs(arr - bg_mean) / bg_std
        fg_mask = (diff_map > 1.0).astype(np.uint8)

        # Morphological cleanup — numpy-only (no scipy dependency)
        kernel_size = max(3, min(h, w) // 40)
        if kernel_size % 2 == 0:
            kernel_size += 1
        fg_mask = _numpy_morph_close(fg_mask, kernel_size, iterations=2)
        fg_mask = _numpy_morph_open(fg_mask, kernel_size, iterations=1)

        # Get foreground points
        pts = np.column_stack(np.where(fg_mask > 0))  # (row, col)
        if len(pts) < 20:
            return None

        # PCA via covariance matrix
        pts_xy = pts[:, ::-1].astype(np.float64)  # (x, y)
        cx = float(np.mean(pts_xy[:, 0]))
        cy = float(np.mean(pts_xy[:, 1]))
        centered = pts_xy - np.array([cx, cy])
        cov = np.cov(centered.T)
        eigvals, eigvecs = np.linalg.eigh(cov)
        # Principal axis = eigenvector with largest eigenvalue
        idx = np.argmax(eigvals)
        principal = eigvecs[:, idx]
        angle = math.atan2(principal[1], principal[0])

        # Project points onto principal axis
        projections = centered @ principal
        min_proj = float(np.min(projections))
        max_proj = float(np.max(projections))
        spine_length = max_proj - min_proj

        center = (int(cx), int(cy))
        start = (int(cx + principal[0] * min_proj),
                 int(cy + principal[1] * min_proj))
        end = (int(cx + principal[0] * max_proj),
               int(cy + principal[1] * max_proj))

        # Topline straightness
        perp_vec = np.array([-principal[1], principal[0]])
        perp_dists = np.abs(centered @ perp_vec)
        mean_deviation = float(np.mean(perp_dists))
        straightness = 1.0 - min(mean_deviation / max(spine_length * 0.1, 1.0), 1.0)

        return {
            'start': start,
            'end': end,
            'center': center,
            'angle': angle,
            'length': spine_length,
            'topline_straightness': straightness,
        }
    except Exception as e:
        logger.warning(f"Centerline PIL detection failed: {e}")
        # Fallback to minimal detection
        return _detect_centerline_pil_minimal(pil_img)


def _detect_centerline_pil_minimal(pil_img):
    """Minimal centerline detection without scipy (numpy only)."""
    try:
        gray = pil_img.convert('L')
        arr = np.array(gray, dtype=np.float32)
        h, w = arr.shape

        border = np.concatenate([arr[0, :], arr[-1, :], arr[:, 0], arr[:, -1]])
        bg_mean = float(np.mean(border))
        bg_std = float(np.std(border)) + 1.0
        diff_map = np.abs(arr - bg_mean) / bg_std
        fg_mask = (diff_map > 1.0).astype(np.uint8)

        pts = np.column_stack(np.where(fg_mask > 0))
        if len(pts) < 20:
            return None

        pts_xy = pts[:, ::-1].astype(np.float64)
        cx = float(np.mean(pts_xy[:, 0]))
        cy = float(np.mean(pts_xy[:, 1]))
        centered = pts_xy - np.array([cx, cy])
        cov = np.cov(centered.T)
        eigvals, eigvecs = np.linalg.eigh(cov)
        idx = np.argmax(eigvals)
        principal = eigvecs[:, idx]
        angle = math.atan2(principal[1], principal[0])

        projections = centered @ principal
        min_proj = float(np.min(projections))
        max_proj = float(np.max(projections))
        spine_length = max_proj - min_proj

        center = (int(cx), int(cy))
        start = (int(cx + principal[0] * min_proj),
                 int(cy + principal[1] * min_proj))
        end = (int(cx + principal[0] * max_proj),
               int(cy + principal[1] * max_proj))

        perp_vec = np.array([-principal[1], principal[0]])
        perp_dists = np.abs(centered @ perp_vec)
        mean_deviation = float(np.mean(perp_dists))
        straightness = 1.0 - min(mean_deviation / max(spine_length * 0.1, 1.0), 1.0)

        return {
            'start': start, 'end': end, 'center': center,
            'angle': angle, 'length': spine_length,
            'topline_straightness': straightness,
        }
    except Exception as e:
        logger.warning(f"Centerline minimal detection failed: {e}")
        return None


def _split_by_centerline_cv(gray, centerline):
    """Split a grayscale image into two halves along the centerline.

    Returns (side_a, side_b) as masked numpy arrays, or None on failure.
    Uses the perpendicular to the spine to determine left/right.
    """
    if centerline is None:
        return None
    try:
        h, w = gray.shape[:2]
        cx, cy = centerline['center']
        angle = centerline['angle']
        perp_x = -math.sin(angle)
        perp_y = math.cos(angle)

        # Create coordinate grid
        yy, xx = np.mgrid[0:h, 0:w]
        # Signed distance from centerline
        signed_dist = (xx - cx) * perp_x + (yy - cy) * perp_y

        mask_a = (signed_dist >= 0).astype(np.uint8)
        mask_b = (signed_dist < 0).astype(np.uint8)

        if gray.ndim == 2:
            side_a = gray * mask_a
            side_b = gray * mask_b
        else:
            side_a = gray * mask_a[..., np.newaxis]
            side_b = gray * mask_b[..., np.newaxis]

        return side_a, side_b, mask_a, mask_b
    except Exception as e:
        logger.warning(f"Centerline split failed: {e}")
        return None


def _split_by_centerline_np(arr, centerline):
    """Split a numpy array image into two halves along centerline (no OpenCV)."""
    return _split_by_centerline_cv(arr, centerline)


def _centerline_symmetry(gray, centerline):
    """Compute symmetry score by comparing the two sides of the centerline.

    More robust than simple left-right split because it follows the actual
    body axis rather than the image center (which may not align with the dog).
    Returns float 0.0-1.0 (1.0 = perfectly symmetric).
    """
    result = _split_by_centerline_cv(gray, centerline)
    if result is None:
        return 0.5
    side_a, side_b, mask_a, mask_b = result

    # Flip side_b across the centerline for comparison
    h, w = gray.shape[:2]
    cx, cy = centerline['center']
    angle = centerline['angle']
    -math.sin(angle)
    math.cos(angle)

    # Compare pixel distributions (histograms) of both sides
    # This is robust to fur noise because it compares statistical distributions
    bins = 32
    a_pixels = side_a[mask_a > 0].flatten()
    b_pixels = side_b[mask_b > 0].flatten()
    if len(a_pixels) < 10 or len(b_pixels) < 10:
        return 0.5

    hist_a, _ = np.histogram(a_pixels, bins=bins, range=(0, 255), density=True)
    hist_b, _ = np.histogram(b_pixels, bins=bins, range=(0, 255), density=True)
    hist_a = hist_a.astype(np.float32)
    hist_b = hist_b.astype(np.float32)

    # Bhattacharyya coefficient: 1.0 = identical distributions
    sqrt_product = np.sqrt(hist_a * hist_b)
    bc = float(np.sum(sqrt_product))
    # Normalize (histograms are density-normalized, so sum of sqrt products ≤ 1)
    bc = min(bc * (256.0 / bins), 1.0)

    return bc


# ---------------------------------------------------------------------------
# Multi-Part Skeleton — 全身多部位中心線検出
# ---------------------------------------------------------------------------
# 体の全てに中心線のラインを引いてから検出する。
# 背骨だけでなく、頭・首・胴体・前脚×2・後脚×2・尾の各パーツに
# 中心線を引くことで、毛に覆われた犬の体構造をより精密に把握する。


def _skeleton_branch_points(skel):
    """Find branch points (junctions) in a morphological skeleton.

    A branch point is a skeleton pixel with 3+ skeleton neighbors.
    Returns list of (x, y) tuples.
    """
    pts = []
    h, w = skel.shape
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            if skel[y, x] == 0:
                continue
            # Count 8-connected skeleton neighbors
            neighbors = 0
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if dy == 0 and dx == 0:
                        continue
                    if skel[y + dy, x + dx] > 0:
                        neighbors += 1
            if neighbors >= 3:
                pts.append((x, y))
    return pts


def _skeleton_endpoints(skel):
    """Find endpoints in a morphological skeleton.

    An endpoint is a skeleton pixel with exactly 1 skeleton neighbor.
    Returns list of (x, y) tuples.
    """
    pts = []
    h, w = skel.shape
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            if skel[y, x] == 0:
                continue
            neighbors = 0
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if dy == 0 and dx == 0:
                        continue
                    if skel[y + dy, x + dx] > 0:
                        neighbors += 1
            if neighbors == 1:
                pts.append((x, y))
    return pts


def _trace_branch(skel, start, visited, max_steps=500):
    """Trace a skeleton branch from start point, returning ordered point list."""
    path = [start]
    visited.add(start)
    h, w = skel.shape
    current = start
    for _ in range(max_steps):
        x, y = current
        found = False
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dy == 0 and dx == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in visited and skel[ny, nx] > 0:
                    visited.add((nx, ny))
                    path.append((nx, ny))
                    current = (nx, ny)
                    found = True
                    break
            if found:
                break
        if not found:
            break
    return path


def _branch_centerline(points):
    """Compute a centerline dict from a list of (x, y) points."""
    if len(points) < 2:
        return None
    pts_arr = np.array(points, dtype=np.float64)
    cx = float(np.mean(pts_arr[:, 0]))
    cy = float(np.mean(pts_arr[:, 1]))

    # PCA for direction
    centered = pts_arr - np.array([cx, cy])
    cov = np.cov(centered.T) if centered.shape[0] > 2 else np.eye(2)
    eigvals, eigvecs = np.linalg.eigh(cov)
    idx = np.argmax(eigvals)
    principal = eigvecs[:, idx]
    angle = math.atan2(principal[1], principal[0])

    # Straightness
    projections = centered @ principal
    perp_vec = np.array([-principal[1], principal[0]])
    perp_dists = np.abs(centered @ perp_vec)
    length = float(np.max(projections) - np.min(projections))
    mean_dev = float(np.mean(perp_dists))
    straightness = 1.0 - min(mean_dev / max(length * 0.1, 1.0), 1.0)

    return {
        'start': points[0],
        'end': points[-1],
        'center': (int(cx), int(cy)),
        'angle': angle,
        'length': length,
        'topline_straightness': straightness,
        'points': points,
    }


def _classify_dog_parts_cv(branches, spine_cl, bbox, mask):
    """Classify skeleton branches into dog body parts.

    Uses anatomical heuristics for a side-profile dog:
      - Spine runs roughly horizontal across the upper-middle of the body
      - Head/neck: branches extending forward (left side in standard pose)
      - Tail: branch extending rearward (right side)
      - Front legs: downward branches in the front third
      - Rear legs: downward branches in the rear third

    Args:
        branches: list of (centerline_dict, points_list)
        spine_cl: the main spine centerline dict
        bbox: (x, y, w, h) bounding box of the dog mask
        mask: dog binary mask

    Returns:
        dict mapping part names to centerline dicts
    """
    bx, by, bw, bh = bbox
    # Reference points along the spine
    spine_cx, spine_cy = spine_cl['center']
    spine_cl['angle']

    # Determine which end is head vs tail:
    # In standard show dog side profile, head is the end with more
    # vertical extent above the spine (skull rises above topline)
    sx, sy = spine_cl['start']
    ex, ey = spine_cl['end']
    # Check mask density above each endpoint
    check_r = max(10, int(bh * 0.15))
    region_s = mask[max(0, sy - check_r):sy, max(0, sx - check_r):sx + check_r]
    region_e = mask[max(0, ey - check_r):ey, max(0, ex - check_r):ex + check_r]
    density_s = np.count_nonzero(region_s) / max(region_s.size, 1)
    density_e = np.count_nonzero(region_e) / max(region_e.size, 1)

    if density_s >= density_e:
        head_end = (sx, sy)
        tail_end = (ex, ey)
    else:
        head_end = (ex, ey)
        tail_end = (sx, sy)

    # Horizontal midpoint of bounding box
    bx + bw * 0.5
    # Vertical midpoint (spine level)
    mid_y = spine_cy

    parts = {
        'spine': spine_cl,
        'head': None,
        'neck': None,
        'tail': None,
        'front_leg_near': None,
        'front_leg_far': None,
        'rear_leg_near': None,
        'rear_leg_far': None,
    }

    # Score each branch for each possible body part
    leg_front_candidates = []
    leg_rear_candidates = []

    for cl, _pts in branches:
        if cl is None or cl['length'] < bh * 0.05:
            continue  # too short

        bcx, bcy = cl['center']
        bangle = cl['angle']
        # Is this branch mostly below the spine? (legs go down)
        below_spine = bcy > mid_y
        # Is this branch mostly vertical? (legs are vertical-ish)
        vert = abs(math.sin(bangle)) > 0.5
        # Is this branch in the front or rear half?
        head_dist = math.hypot(bcx - head_end[0], bcy - head_end[1])
        tail_dist = math.hypot(bcx - tail_end[0], bcy - tail_end[1])
        in_front = head_dist < tail_dist

        # Head/neck detection: near head_end, above or at spine level
        if head_dist < bw * 0.35 and not below_spine:
            if parts['head'] is None or cl['length'] > parts['head']['length']:
                parts['head'] = cl
            continue

        # Tail detection: near tail_end
        if tail_dist < bw * 0.3 and (not below_spine or not vert):
            if parts['tail'] is None or cl['length'] > parts['tail']['length']:
                parts['tail'] = cl
            continue

        # Leg detection: below spine and somewhat vertical
        if below_spine and vert:
            if in_front:
                leg_front_candidates.append(cl)
            else:
                leg_rear_candidates.append(cl)

    # Assign legs (up to 2 per front/rear, sorted by length)
    leg_front_candidates.sort(key=lambda c: c['length'], reverse=True)
    leg_rear_candidates.sort(key=lambda c: c['length'], reverse=True)

    if len(leg_front_candidates) >= 1:
        parts['front_leg_near'] = leg_front_candidates[0]
    if len(leg_front_candidates) >= 2:
        parts['front_leg_far'] = leg_front_candidates[1]
    if len(leg_rear_candidates) >= 1:
        parts['rear_leg_near'] = leg_rear_candidates[0]
    if len(leg_rear_candidates) >= 2:
        parts['rear_leg_far'] = leg_rear_candidates[1]

    return parts


def _detect_full_skeleton_cv(img, mask=None):
    """Detect the full multi-part dog skeleton using OpenCV.

    Returns dict mapping body part names to centerline dicts:
      spine, head, neck, tail, front_leg_near, front_leg_far,
      rear_leg_near, rear_leg_far

    Each centerline dict has: start, end, center, angle, length,
    topline_straightness, points.
    """
    if not CV2_AVAILABLE:
        return None
    try:
        h, w = img.shape[:2]
        if mask is None:
            mask, _, _mq = _detect_dog_mask(img)

        # Morphological skeleton
        skel = np.zeros_like(mask)
        element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
        working = mask.copy()
        while True:
            eroded = cv2.erode(working, element)
            opened = cv2.dilate(eroded, element)
            diff = cv2.subtract(working, opened)
            skel = cv2.bitwise_or(skel, diff)
            working = eroded.copy()
            if cv2.countNonZero(working) == 0:
                break

        if cv2.countNonZero(skel) < 20:
            return None

        # Get bounding box of mask
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                                        cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return None
        largest_c = max(contours, key=cv2.contourArea)
        bbox = cv2.boundingRect(largest_c)

        # Get spine (overall centerline) first
        spine_cl = _detect_centerline_cv(img, mask)
        if spine_cl is None:
            return None

        # Downsample skeleton for faster branch detection on large images
        # Work on the original resolution for accuracy
        branch_pts = _skeleton_branch_points(skel)
        end_pts = _skeleton_endpoints(skel)

        # Trace branches from each endpoint
        visited = set()
        # First mark branch points as visited to segment the skeleton
        for bp in branch_pts:
            visited.add(bp)

        branches = []
        for ep in end_pts:
            if ep in visited:
                continue
            path = _trace_branch(skel, ep, visited)
            if len(path) >= 5:
                cl = _branch_centerline(path)
                if cl:
                    branches.append((cl, path))

        # Also trace between branch points
        for bp in branch_pts:
            visited_bp = visited.copy()
            visited_bp.discard(bp)
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if dy == 0 and dx == 0:
                        continue
                    nx, ny = bp[0] + dx, bp[1] + dy
                    if (0 <= nx < w and 0 <= ny < h and
                            skel[ny, nx] > 0 and (nx, ny) not in visited):
                        path = _trace_branch(skel, (nx, ny), visited)
                        if len(path) >= 5:
                            cl = _branch_centerline(path)
                            if cl:
                                branches.append((cl, path))

        # Classify branches into body parts
        parts = _classify_dog_parts_cv(branches, spine_cl, bbox, mask)

        return parts

    except Exception as e:
        logger.warning(f"Full skeleton CV detection failed: {e}")
        return None


def _detect_full_skeleton_pil(pil_img):
    """Detect multi-part dog skeleton using Pillow + numpy.

    Uses geometric heuristics on the foreground mask to estimate body part
    locations and draw centerlines through each region.

    Returns same structure as _detect_full_skeleton_cv.
    """
    try:
        gray = pil_img.convert('L')
        arr = np.array(gray, dtype=np.float32)
        h, w = arr.shape

        # Foreground detection
        border = np.concatenate([arr[0, :], arr[-1, :], arr[:, 0], arr[:, -1]])
        bg_mean = float(np.mean(border))
        bg_std = float(np.std(border)) + 1.0
        diff_map = np.abs(arr - bg_mean) / bg_std
        fg_mask = (diff_map > 1.0).astype(np.uint8)

        # Morphological cleanup — numpy-only (no scipy dependency)
        kernel_sz = max(3, min(h, w) // 40)
        if kernel_sz % 2 == 0:
            kernel_sz += 1
        fg_mask = _numpy_morph_close(fg_mask, kernel_sz, iterations=2)
        fg_mask = _numpy_morph_open(fg_mask, kernel_sz, iterations=1)

        fg_pts = np.column_stack(np.where(fg_mask > 0))
        if len(fg_pts) < 40:
            return None

        # Get overall spine
        spine_cl = _detect_centerline_pil(pil_img)
        if spine_cl is None:
            return None

        # Bounding box of foreground
        rows = fg_pts[:, 0]
        cols = fg_pts[:, 1]
        min_r, max_r = int(np.min(rows)), int(np.max(rows))
        min_c, max_c = int(np.min(cols)), int(np.max(cols))
        max_c - min_c
        bbox_h = max_r - min_r

        # Determine head vs tail direction from spine
        sx, sy = spine_cl['start']
        ex, ey = spine_cl['end']
        # Head end: check for more mass above the spine endpoint
        check_r = max(8, bbox_h // 6)
        region_s = fg_mask[max(0, sy - check_r):sy, max(0, sx - check_r):sx + check_r]
        region_e = fg_mask[max(0, ey - check_r):ey, max(0, ex - check_r):ex + check_r]
        ds = np.count_nonzero(region_s) / max(region_s.size, 1)
        de = np.count_nonzero(region_e) / max(region_e.size, 1)
        if ds >= de:
            head_end = (sx, sy)
            tail_end = (ex, ey)
        else:
            head_end = (ex, ey)
            tail_end = (sx, sy)

        spine_cy = spine_cl['center'][1]

        # Divide the body into vertical zones along the spine direction
        # Zone boundaries (along major axis)
        parts = {'spine': spine_cl}

        # --- Head region: around head_end, above spine level -----------------
        hx, hy = head_end
        head_region = fg_mask[max(0, hy - check_r * 2):hy + check_r,
                              max(0, hx - check_r * 2):hx + check_r * 2]
        if np.count_nonzero(head_region) > 10:
            head_pts = np.column_stack(np.where(head_region > 0))
            if len(head_pts) > 3:
                # Offset to image coordinates
                offset_y = max(0, hy - check_r * 2)
                offset_x = max(0, hx - check_r * 2)
                head_pts_xy = [(int(p[1] + offset_x), int(p[0] + offset_y))
                               for p in head_pts[::max(1, len(head_pts) // 30)]]
                parts['head'] = _branch_centerline(head_pts_xy)

        # --- Tail region: around tail_end ------------------------------------
        tx, ty = tail_end
        tail_region = fg_mask[max(0, ty - check_r):ty + check_r * 2,
                              max(0, tx - check_r):tx + check_r * 2]
        if np.count_nonzero(tail_region) > 5:
            tail_pts = np.column_stack(np.where(tail_region > 0))
            if len(tail_pts) > 3:
                offset_y = max(0, ty - check_r)
                offset_x = max(0, tx - check_r)
                tail_pts_xy = [(int(p[1] + offset_x), int(p[0] + offset_y))
                               for p in tail_pts[::max(1, len(tail_pts) // 20)]]
                parts['tail'] = _branch_centerline(tail_pts_xy)

        # --- Leg regions: below spine, in front/rear halves ------------------
        mid_x = (head_end[0] + tail_end[0]) // 2
        below_mask = fg_mask.copy()
        below_mask[:spine_cy, :] = 0  # Only below spine

        # Front legs (head side)
        front_x_start = min(head_end[0], tail_end[0])
        front_x_end = mid_x
        front_region = below_mask[:, max(0, front_x_start):front_x_end]
        if np.count_nonzero(front_region) > 10:
            front_pts = np.column_stack(np.where(front_region > 0))
            if len(front_pts) > 5:
                offset_x = max(0, front_x_start)
                front_pts_xy = [(int(p[1] + offset_x), int(p[0]))
                                for p in front_pts[::max(1, len(front_pts) // 30)]]
                parts['front_leg_near'] = _branch_centerline(front_pts_xy)

        # Rear legs (tail side)
        rear_x_start = mid_x
        rear_x_end = max(head_end[0], tail_end[0])
        rear_region = below_mask[:, rear_x_start:min(w, rear_x_end)]
        if np.count_nonzero(rear_region) > 10:
            rear_pts = np.column_stack(np.where(rear_region > 0))
            if len(rear_pts) > 5:
                rear_pts_xy = [(int(p[1] + rear_x_start), int(p[0]))
                               for p in rear_pts[::max(1, len(rear_pts) // 30)]]
                parts['rear_leg_near'] = _branch_centerline(rear_pts_xy)

        # Fill missing parts with None
        for key in ('head', 'neck', 'tail', 'front_leg_near', 'front_leg_far',
                     'rear_leg_near', 'rear_leg_far'):
            if key not in parts:
                parts[key] = None

        return parts

    except Exception as e:
        logger.warning(f"Full skeleton PIL detection failed: {e}")
        return None


def _score_part_angles(skeleton, breed_data=None):
    """Score angular relationships between body parts against breed-specific standards.

    犬のシルエットから引いた中心線の角度・比率を犬種スタンダードDBと比較し、
    細かい係数で算出した偏差スコアを返す。

    Uses breed-specific ideal angles, tolerances, and weights from
    BREED_ANGLE_STANDARDS for fine-grained scoring with natural variability.

    Returns dict of angle scores (0.0-1.0) for each relationship found,
    plus raw measurements in degrees for audit/transparency.
    """
    if skeleton is None:
        return {}

    # Get breed-specific angle standards
    standards = _get_angle_standards(breed_data or {})

    scores = {}
    raw_angles = {}  # Raw measurements for transparency
    spine = skeleton.get('spine')
    if spine is None:
        return scores

    # Topline straightness
    topline_std = standards.get('topline_straightness', (1.0, 0.3, 0.20))
    ideal_tl, tol_tl, weight_tl = topline_std
    topline_val = spine['topline_straightness']
    scores['topline'] = _angle_deviation_score(topline_val, ideal_tl, tol_tl)
    scores['topline_weight'] = weight_tl
    raw_angles['topline_straightness'] = round(topline_val, 3)

    # Head carriage angle
    head = skeleton.get('head')
    if head and spine:
        angle_diff = abs(head['angle'] - spine['angle'])
        if angle_diff > math.pi:
            angle_diff = 2 * math.pi - angle_diff
        angle_deg = math.degrees(angle_diff)
        hc_std = standards.get('head_carriage', (45, 20, 0.15))
        ideal_hc, tol_hc, weight_hc = hc_std
        scores['head_carriage'] = _angle_deviation_score(angle_deg, ideal_hc, tol_hc)
        scores['head_carriage_weight'] = weight_hc
        raw_angles['head_carriage_deg'] = round(angle_deg, 1)

    # Shoulder angulation (spine-to-front-leg angle)
    front_leg = skeleton.get('front_leg_near')
    if front_leg and spine:
        angle_diff = abs(front_leg['angle'] - spine['angle'])
        if angle_diff > math.pi:
            angle_diff = 2 * math.pi - angle_diff
        angle_deg = math.degrees(angle_diff)
        sa_std = standards.get('shoulder_angle', (100, 15, 0.20))
        ideal_sa, tol_sa, weight_sa = sa_std
        scores['shoulder_angle'] = _angle_deviation_score(angle_deg, ideal_sa, tol_sa)
        scores['shoulder_angle_weight'] = weight_sa
        raw_angles['shoulder_angle_deg'] = round(angle_deg, 1)

    # Rear angulation (spine-to-rear-leg angle)
    rear_leg = skeleton.get('rear_leg_near')
    if rear_leg and spine:
        angle_diff = abs(rear_leg['angle'] - spine['angle'])
        if angle_diff > math.pi:
            angle_diff = 2 * math.pi - angle_diff
        angle_deg = math.degrees(angle_diff)
        ra_std = standards.get('rear_angle', (100, 15, 0.20))
        ideal_ra, tol_ra, weight_ra = ra_std
        scores['rear_angle'] = _angle_deviation_score(angle_deg, ideal_ra, tol_ra)
        scores['rear_angle_weight'] = weight_ra
        raw_angles['rear_angle_deg'] = round(angle_deg, 1)

    # Tail set angle
    tail = skeleton.get('tail')
    if tail and spine:
        angle_diff = abs(tail['angle'] - spine['angle'])
        if angle_diff > math.pi:
            angle_diff = 2 * math.pi - angle_diff
        angle_deg = math.degrees(angle_diff)
        ts_std = standards.get('tail_set', (30, 25, 0.10))
        ideal_ts, tol_ts, weight_ts = ts_std
        scores['tail_set'] = _angle_deviation_score(angle_deg, ideal_ts, tol_ts)
        scores['tail_set_weight'] = weight_ts
        raw_angles['tail_set_deg'] = round(angle_deg, 1)

    # Leg symmetry (front pair and rear pair)
    fl_near = skeleton.get('front_leg_near')
    fl_far = skeleton.get('front_leg_far')
    if fl_near and fl_far:
        len_diff = abs(fl_near['length'] - fl_far['length'])
        avg_len = (fl_near['length'] + fl_far['length']) / 2
        sym_val = max(0.0, 1.0 - len_diff / max(avg_len, 1))
        fls_std = standards.get('front_leg_symmetry', (1.0, 0.2, 0.08))
        ideal_fls, tol_fls, weight_fls = fls_std
        scores['front_leg_symmetry'] = _angle_deviation_score(sym_val, ideal_fls, tol_fls)
        scores['front_leg_symmetry_weight'] = weight_fls
        raw_angles['front_leg_symmetry'] = round(sym_val, 3)

    rl_near = skeleton.get('rear_leg_near')
    rl_far = skeleton.get('rear_leg_far')
    if rl_near and rl_far:
        len_diff = abs(rl_near['length'] - rl_far['length'])
        avg_len = (rl_near['length'] + rl_far['length']) / 2
        sym_val = max(0.0, 1.0 - len_diff / max(avg_len, 1))
        rls_std = standards.get('rear_leg_symmetry', (1.0, 0.2, 0.07))
        ideal_rls, tol_rls, weight_rls = rls_std
        scores['rear_leg_symmetry'] = _angle_deviation_score(sym_val, ideal_rls, tol_rls)
        scores['rear_leg_symmetry_weight'] = weight_rls
        raw_angles['rear_leg_symmetry'] = round(sym_val, 3)

    # Store raw measurements for transparency
    scores['_raw_angles'] = raw_angles

    return scores


def _compute_weighted_angulation_score(part_angles):
    """Compute overall angulation score using breed-specific weights.

    Each angle measurement contributes according to its weight coefficient,
    producing a weighted composite score with natural variability.
    Returns 0-100 score.
    """
    if not part_angles:
        return 75.0  # default when no measurements available

    weighted_sum = 0.0
    weight_total = 0.0
    for key, val in part_angles.items():
        if key.startswith('_') or key.endswith('_weight'):
            continue
        weight_key = f'{key}_weight'
        weight = part_angles.get(weight_key, 0.1)
        weighted_sum += val * weight
        weight_total += weight

    if weight_total < 0.01:
        return 75.0

    # Map weighted average (0-1) to score range with breed-appropriate spread
    raw = weighted_sum / weight_total
    # Sigmoid mapping for natural bell-curve distribution
    # Produces scores roughly in 60-98 range
    score = 60.0 + raw * 38.0
    return round(score, 1)


def _skeleton_summary(skeleton):
    """Generate a summary string of detected body parts and their properties."""
    if skeleton is None:
        return '中心線検出失敗'
    detected = []
    part_names_ja = {
        'spine': '背骨', 'head': '頭部', 'neck': '首',
        'tail': '尾', 'front_leg_near': '前脚(手前)',
        'front_leg_far': '前脚(奥)', 'rear_leg_near': '後脚(手前)',
        'rear_leg_far': '後脚(奥)',
    }
    for key, name in part_names_ja.items():
        cl = skeleton.get(key)
        if cl is not None:
            detected.append(name)
    return f'検出パーツ: {", ".join(detected)}' if detected else '検出パーツなし'


# ---------------------------------------------------------------------------
# Dog Focus Preprocessing (背景ぼかし + 犬シャープ化 + 解剖学的追跡)
# ---------------------------------------------------------------------------

def _detect_dog_mask(frame, prev_centroid=None):
    """Detect the dog as the primary subject and return a binary mask.

    Uses a multi-layered approach for robust detection:
      Layer 1: Saliency-based detection (color distance from frame borders)
      Layer 2: Edge-guided contour detection with flood fill
      Layer 3: Centroid continuity for anatomical tracking across frames
      Layer 4: GrabCut refinement with contour-seeded initialization

    Returns (mask, centroid) where mask is uint8 (255=dog, 0=background).
    """
    h, w = frame.shape[:2]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # --- Layer 1: Saliency map (subject differs from border colors) ---------
    # Sample border pixels to estimate background color distribution
    border_size = max(10, min(h, w) // 20)
    border_top = frame[:border_size, :].reshape(-1, 3)
    border_bottom = frame[-border_size:, :].reshape(-1, 3)
    border_left = frame[:, :border_size].reshape(-1, 3)
    border_right = frame[:, -border_size:].reshape(-1, 3)
    border_pixels = np.vstack([border_top, border_bottom, border_left, border_right])
    bg_mean = border_pixels.mean(axis=0).astype(np.float32)
    bg_std = border_pixels.std(axis=0).astype(np.float32) + 1.0

    # Color distance from background (higher = more likely dog)
    frame_f = frame.astype(np.float32)
    color_dist = np.sqrt(np.sum(((frame_f - bg_mean) / bg_std) ** 2, axis=2))
    saliency = cv2.normalize(color_dist, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    _, saliency_mask = cv2.threshold(saliency, 0, 255,
                                      cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # --- Layer 2: Edge-guided contour detection -----------------------------
    edges = cv2.Canny(gray, 50, 150)
    edges_dilated = cv2.dilate(edges, np.ones((7, 7), np.uint8), iterations=3)
    # Fill enclosed regions from edges
    edge_filled = edges_dilated.copy()
    flood_mask = np.zeros((h + 2, w + 2), dtype=np.uint8)
    cv2.floodFill(edge_filled, flood_mask, (0, 0), 255)
    edge_interior = cv2.bitwise_not(edge_filled)

    # Combine saliency + edge interior
    combined = cv2.bitwise_or(saliency_mask, edge_interior)

    # Strong morphological cleanup
    kernel_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (21, 21))
    kernel_open = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    combined = cv2.morphologyEx(combined, cv2.MORPH_CLOSE, kernel_close)
    combined = cv2.morphologyEx(combined, cv2.MORPH_OPEN, kernel_open)

    # Find contours
    contours, _ = cv2.findContours(combined, cv2.RETR_EXTERNAL,
                                    cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        mask = np.zeros((h, w), dtype=np.uint8)
        cv2.ellipse(mask, (w // 2, h // 2), (w // 3, h // 3), 0, 0, 360, 255, -1)
        return mask, (w // 2, h // 2), 'low'

    # Filter: dog should occupy > 3% of frame
    min_area = h * w * 0.03
    valid = [c for c in contours if cv2.contourArea(c) > min_area]
    if not valid:
        valid = sorted(contours, key=cv2.contourArea, reverse=True)[:3]

    # --- Layer 3: Anatomical tracking via centroid continuity ---------------
    if prev_centroid is not None:
        def _score_contour(c):
            M = cv2.moments(c)
            if M['m00'] == 0:
                return float('inf')
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            dist = math.hypot(cx - prev_centroid[0], cy - prev_centroid[1])
            area = cv2.contourArea(c)
            # Balance proximity (lower=better) vs size (larger=better)
            return dist - area / (h * w) * 500

        valid.sort(key=_score_contour)
        dog_contour = valid[0]
    else:
        dog_contour = max(valid, key=cv2.contourArea)

    # Compute centroid
    M = cv2.moments(dog_contour)
    centroid = (int(M['m10'] / max(M['m00'], 1)),
                int(M['m01'] / max(M['m00'], 1)))

    # --- Layer 4: Fast GrabCut on downscaled frame ---------------------------
    # GrabCut is O(n) on pixel count; downscale 4x for ~16x speedup
    SCALE = 4
    small_h, small_w = h // SCALE, w // SCALE
    small_frame = cv2.resize(frame, (small_w, small_h), interpolation=cv2.INTER_AREA)

    # Scale contour to small dimensions
    small_contour = (dog_contour / SCALE).astype(np.int32)

    x, y, bw, bh = cv2.boundingRect(small_contour)
    margin_x = int(bw * 0.20)
    margin_y = int(bh * 0.20)
    x1 = max(0, x - margin_x)
    y1 = max(0, y - margin_y)
    x2 = min(small_w, x + bw + margin_x)
    y2 = min(small_h, y + bh + margin_y)

    # Seed GrabCut with contour (not just rect) for better accuracy
    gc_mask = np.full((small_h, small_w), cv2.GC_BGD, dtype=np.uint8)
    gc_mask[y1:y2, x1:x2] = cv2.GC_PR_BGD
    cv2.drawContours(gc_mask, [small_contour], -1, cv2.GC_PR_FGD, -1)
    # Eroded core = definite foreground
    core_mask = np.zeros((small_h, small_w), dtype=np.uint8)
    cv2.drawContours(core_mask, [small_contour], -1, 255, -1)
    erode_k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    core_eroded = cv2.erode(core_mask, erode_k)
    gc_mask[core_eroded == 255] = cv2.GC_FGD

    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)
    with contextlib.suppress(cv2.error):
        cv2.grabCut(small_frame, gc_mask, None, bgd_model, fgd_model,
                     2, cv2.GC_INIT_WITH_MASK)  # 2 iterations (was 5)

    # Upscale mask back to original resolution
    small_result = np.where(
        (gc_mask == cv2.GC_FGD) | (gc_mask == cv2.GC_PR_FGD), 255, 0
    ).astype(np.uint8)
    final_mask = cv2.resize(small_result, (w, h), interpolation=cv2.INTER_LINEAR)
    _, final_mask = cv2.threshold(final_mask, 127, 255, cv2.THRESH_BINARY)

    # Validate mask size (dog = 3-80% of frame)
    mask_ratio = np.count_nonzero(final_mask) / (h * w)
    mask_quality = 'high'
    if mask_ratio < 0.03 or mask_ratio > 0.80:
        # Fallback: contour + convex hull — degraded mode (don't crash)
        final_mask = np.zeros((h, w), dtype=np.uint8)
        hull = cv2.convexHull(dog_contour)
        cv2.drawContours(final_mask, [hull], -1, 255, -1)
        mask_quality = 'low'
        logger.debug(f"Mask degraded mode: ratio={mask_ratio:.3f}, using convex hull fallback")
    elif mask_ratio < 0.08 or mask_ratio > 0.65:
        mask_quality = 'medium'

    # Smooth edges for natural alpha blending
    final_mask = cv2.GaussianBlur(final_mask, (11, 11), 4)
    _, final_mask = cv2.threshold(final_mask, 100, 255, cv2.THRESH_BINARY)

    return final_mask, centroid, mask_quality


def _sharpen_region(image, mask):
    """Apply unsharp mask sharpening to the dog region only.

    Enhances anatomical detail: muscle definition, bone structure,
    coat texture for more accurate gait and structure evaluation.
    """
    # Unsharp mask: sharpened = original + (original - blurred) * amount
    blurred = cv2.GaussianBlur(image, (0, 0), 3)
    sharpened = cv2.addWeighted(image, 1.5, blurred, -0.5, 0)

    # Slight CLAHE on luminance for better anatomical detail visibility
    lab = cv2.cvtColor(sharpened, cv2.COLOR_BGR2LAB)
    l_channel = lab[:, :, 0]
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    lab[:, :, 0] = clahe.apply(l_channel)
    sharpened = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    # Apply only within mask region
    mask_3ch = cv2.merge([mask, mask, mask])
    result = np.where(mask_3ch == 255, sharpened, image)
    return result


def _blur_background(image, mask, blur_strength=31):
    """Apply Gaussian blur to non-dog regions.

    Removes visual noise from background: people, other dogs, fences,
    ring equipment, spectators — isolating the subject dog.
    """
    # Heavy background blur
    bg_blurred = cv2.GaussianBlur(image, (blur_strength, blur_strength), 0)

    # Feather the mask for smooth blending at dog boundary
    mask_feathered = cv2.GaussianBlur(mask, (15, 15), 5)
    alpha = mask_feathered.astype(np.float32) / 255.0
    alpha_3ch = cv2.merge([alpha, alpha, alpha])

    # Blend: dog region (sharp) ← alpha → background (blurred)
    result = (image.astype(np.float32) * alpha_3ch +
              bg_blurred.astype(np.float32) * (1.0 - alpha_3ch))
    return result.astype(np.uint8)


def preprocess_dog_focus(frames):
    """Preprocess video frames: isolate dog, blur background, sharpen dog.

    Implements anatomical tracking across frames to maintain consistent
    focus on the same dog throughout the video sequence.

    Args:
        frames: list of BGR numpy arrays (video frames)

    Returns:
        list of preprocessed BGR numpy arrays
    """
    if not CV2_AVAILABLE or not frames:
        return frames

    processed = []
    prev_centroid = None

    for frame in frames:
        try:
            # Detect dog region with anatomical tracking
            mask, centroid, _mq = _detect_dog_mask(frame, prev_centroid)
            prev_centroid = centroid  # Track across frames

            # Blur everything except the dog
            result = _blur_background(frame, mask)

            # Sharpen the dog for anatomical detail
            result = _sharpen_region(result, mask)

            processed.append(result)
        except Exception as e:
            logger.warning(f"Dog focus preprocessing failed for frame: {e}")
            processed.append(frame)  # Use original if preprocessing fails

    return processed


# ---------------------------------------------------------------------------
# Structure Analysis (photo)
# ---------------------------------------------------------------------------

def analyze_structure_local(image_base64, breed_name, breed_data):
    """Analyse body structure from a single photo using OpenCV.

    アルゴリズム主導の構造評価エンジン（AIに依存しない）:
    1. 犬のシルエットから中心線をそれぞれ引く
    2. 各距離の角度、比率などの総合的評価
    3. スタンダードDBと比較してスコアリング
    4. 犬種別の細かい係数で自然なバラツキを実現
    """
    if not CV2_AVAILABLE:
        return None  # caller falls back to default dict

    try:
        img = _decode_base64_image(image_base64)
        if img is None:
            return None
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape

        # --- Step 1: Detect dog mask, centerline, and full skeleton -----------
        mask, centroid, mask_quality = _detect_dog_mask(img)
        angle_info = estimate_angle_from_mask(mask)
        centerline = _detect_centerline_cv(img, mask)
        skeleton = _detect_full_skeleton_cv(img, mask)
        part_angles = _score_part_angles(skeleton, breed_data)

        # Get breed-specific coefficients
        ratio_coeff = _get_ratio_coefficients(breed_data)
        ideal_body_ratio, ratio_tolerance, head_body_coeff, limb_body_coeff = ratio_coeff

        # --- Proportion: body length along spine vs height perpendicular -----
        measured_ratio = None
        if centerline and centerline['length'] > 0:
            cx, cy = centerline['center']
            angle = centerline['angle']
            perp_x = -math.sin(angle)
            perp_y = math.cos(angle)
            perp_widths = []
            for offset in range(-5, 6):
                px = int(cx + math.cos(angle) * offset * centerline['length'] / 20)
                py = int(cy + math.sin(angle) * offset * centerline['length'] / 20)
                if 0 <= py < h and 0 <= px < w:
                    count = 0
                    for d in range(1, max(h, w)):
                        nx = int(px + perp_x * d)
                        ny = int(py + perp_y * d)
                        if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] > 0:
                            count += 1
                        else:
                            break
                    for d in range(1, max(h, w)):
                        nx = int(px - perp_x * d)
                        ny = int(py - perp_y * d)
                        if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] > 0:
                            count += 1
                        else:
                            break
                    if count > 0:
                        perp_widths.append(count)
            body_width = float(np.mean(perp_widths)) if perp_widths else h * 0.5
            measured_ratio = centerline['length'] / max(body_width, 1.0)
            # Use breed-specific ideal ratio and tolerance for scoring
            breed_ideal = float(breed_data.get('ideal_ratio', ideal_body_ratio))
            ratio_dev = abs(measured_ratio - breed_ideal) / max(ratio_tolerance, 0.01)
            proportion_raw = 1.0 / (1.0 + ratio_dev ** 2)  # Gaussian falloff
            proportion_score = _normalize(proportion_raw, 0.0, 1.0, 62, 97)
        else:
            aspect = w / h if h > 0 else 1.0
            breed_ideal = float(breed_data.get('ideal_ratio', ideal_body_ratio))
            ratio_diff = abs(aspect - breed_ideal)
            proportion_score = _normalize(1.0 - min(ratio_diff, 1.0), 0.0, 1.0, 62, 95)

        # --- Head-to-body ratio (from skeleton) --------------------------------
        head_ratio_score = 0.0
        if skeleton and skeleton.get('head') and skeleton.get('spine'):
            head_len = skeleton['head']['length']
            spine_len = skeleton['spine']['length']
            if spine_len > 0:
                head_body = head_len / spine_len
                # Most breeds: head is ~25-35% of spine length
                ideal_hb = 0.30
                abs(head_body - ideal_hb) / 0.12
                head_ratio_score = _angle_deviation_score(head_body, ideal_hb, 0.12) * head_body_coeff * 10

        # --- Limb-to-body ratio (from skeleton) --------------------------------
        limb_ratio_score = 0.0
        if skeleton and skeleton.get('spine'):
            spine_len = skeleton['spine']['length']
            limb_lengths = []
            for part in ('front_leg_near', 'front_leg_far', 'rear_leg_near', 'rear_leg_far'):
                p = skeleton.get(part)
                if p:
                    limb_lengths.append(p['length'])
            if limb_lengths and spine_len > 0:
                avg_limb = np.mean(limb_lengths)
                limb_body = avg_limb / spine_len
                # Most breeds: limb is ~40-60% of spine length
                ideal_lb = 0.50
                limb_ratio_score = _angle_deviation_score(limb_body, ideal_lb, 0.15) * limb_body_coeff * 10

        # --- Skeletal: topline straightness + edge density -------------------
        edges = cv2.Canny(gray, 50, 150)
        edges_masked = cv2.bitwise_and(edges, mask)
        dog_pixels = max(np.count_nonzero(mask), 1)
        edge_density = np.count_nonzero(edges_masked) / dog_pixels
        edge_density_target = float(breed_data.get('edge_density_target', 0.12))
        edge_dev = abs(edge_density - edge_density_target) / max(edge_density_target, 0.01)
        edge_score = _normalize(
            1.0 / (1.0 + edge_dev ** 2), 0.0, 1.0, 62, 95
        )
        if centerline:
            topline_bonus = centerline['topline_straightness'] * 8.0
            skeletal_score = _normalize(
                (edge_score * 0.5 + topline_bonus * 3.5) / 4.0, 0.0, 1.0, 62, 96
            )
        else:
            skeletal_score = edge_score

        # --- Muscular: Laplacian variance within dog mask --------------------
        body_mass = breed_data.get('body_mass', 'medium')
        if body_mass == 'large':
            musc_min, musc_max = 80, 2500
        elif body_mass == 'small':
            musc_min, musc_max = 30, 1500
        else:
            musc_min, musc_max = 50, 2000
        lap = cv2.Laplacian(gray, cv2.CV_64F)
        lap_masked = lap.copy()
        lap_masked[mask == 0] = 0
        lap_var = np.var(lap_masked[mask > 0]) if np.count_nonzero(mask) > 0 else 0
        muscular_score = _normalize(lap_var, musc_min, musc_max, 62, 95)

        # --- Symmetry: centerline-based (robust to fur noise) ----------------
        if centerline:
            symmetry = _centerline_symmetry(gray, centerline)
        else:
            left_half = gray[:, :w // 2]
            right_half = cv2.flip(gray[:, w // 2:], 1)
            min_w2 = min(left_half.shape[1], right_half.shape[1])
            h_l = cv2.calcHist([left_half[:, :min_w2]], [0], None, [64], [0, 256]).flatten()
            h_r = cv2.calcHist([right_half[:, :min_w2]], [0], None, [64], [0, 256]).flatten()
            symmetry = cv2.compareHist(h_l.astype(np.float32), h_r.astype(np.float32),
                                       cv2.HISTCMP_CORREL)
        symmetry_bonus = _normalize(symmetry, 0.5, 1.0, 0, 5)

        # --- Subject size bonus ----------------------------------------------
        area_ratio = np.count_nonzero(mask) / (h * w)
        size_bonus = _normalize(1.0 - abs(area_ratio - 0.5) / 0.5, 0.0, 1.0, 0, 5)

        # --- Angulation score from full skeleton (breed-weighted) -----------
        angulation_score = _compute_weighted_angulation_score(part_angles)

        # === FINAL COMPOSITE SCORE ==========================================
        # Algorithm-driven: each component has fine-grained breed coefficients
        # The weights produce natural variability via measurement precision
        overall = (
            proportion_score * 0.22 +
            skeletal_score * 0.22 +
            muscular_score * 0.16 +
            angulation_score * 0.25 +   # Largest weight: structural angles
            head_ratio_score +           # Up to ~2.8 bonus
            limb_ratio_score +           # Up to ~3.5 bonus
            symmetry_bonus +             # Up to 5 bonus
            size_bonus                   # Up to 5 bonus
        )
        overall = _clamp(overall)

        comments = _build_structure_comments(
            breed_name, proportion_score, skeletal_score, muscular_score, symmetry
        )
        if centerline:
            comments += f' トップラインの直線性: {centerline["topline_straightness"]:.0%}。'
        if part_angles.get('shoulder_angle') is not None:
            sa = part_angles['shoulder_angle']
            raw_sa = part_angles.get('_raw_angles', {}).get('shoulder_angle_deg', '')
            if sa >= 0.7:
                comments += f' 肩のアンギュレーションが良好です（{raw_sa}°）。'
            else:
                comments += f' 肩のアンギュレーションに改善の余地があります（{raw_sa}°）。'
        if part_angles.get('rear_angle') is not None:
            ra = part_angles['rear_angle']
            raw_ra = part_angles.get('_raw_angles', {}).get('rear_angle_deg', '')
            if ra >= 0.7:
                comments += f' 後躯のアンギュレーションが良好です（{raw_ra}°）。'
            else:
                comments += f' 後躯のアンギュレーションに改善の余地があります（{raw_ra}°）。'
        if skeleton:
            comments += f' ({_skeleton_summary(skeleton)})'

        # Build angulation detail dict (excluding internal keys)
        angle_detail = {}
        if part_angles:
            for k, v in part_angles.items():
                if not k.startswith('_') and isinstance(v, (int, float)):
                    angle_detail[k] = round(v, 3)
        raw_measurements = part_angles.get('_raw_angles', {})

        # Build reasons[] for explainability
        reasons = []
        if centerline:
            reasons.append(f'spine_straightness={centerline["topline_straightness"]:.2f}')
        reasons.append(f'symmetry={symmetry:.2f}')
        reasons.append(f'proportion_score={proportion_score:.1f}')
        reasons.append(f'skeletal_score={skeletal_score:.1f}')
        reasons.append(f'muscular_score={muscular_score:.1f}')
        reasons.append(f'angulation_score={angulation_score:.1f}')
        if measured_ratio is not None:
            reasons.append(f'body_ratio={measured_ratio:.3f}')
        reasons.append(f'mask_quality={mask_quality}')
        reasons.append(f'angle={angle_info["label"]}')

        # AngleCheck: non-side views reduce confidence
        warnings = []
        if angle_info['label'] not in ('side', 'unknown'):
            overall = _clamp(overall * 0.75)
            warnings.append('angle_not_side')
            comments += f' {angle_info["note"]}'

        return {
            'score': float(round(overall, 1)),
            'proportion': int(round(proportion_score)),
            'skeletal': int(round(skeletal_score)),
            'muscular': int(round(muscular_score)),
            'angulation_score': round(angulation_score, 1),
            'comments': comments,
            'details': 'アルゴリズム主導: シルエット中心線→角度/比率→犬種スタンダードDB比較',
            'centerline_detected': centerline is not None,
            'skeleton_parts': _skeleton_summary(skeleton) if skeleton else None,
            'angulation': angle_detail,
            'raw_measurements': raw_measurements,
            'measured_body_ratio': round(measured_ratio, 3) if measured_ratio else None,
            'breed_angle_group': _get_breed_angle_group(breed_data),
            'reasons': reasons,
            'mask_quality': mask_quality,
            'angle': angle_info,
            'warnings': warnings,
        }

    except Exception as e:
        logger.error(f"Local structure analysis error: {e}")
        raise AnalysisError(f"Structure analysis failed: {e}") from e


def _build_structure_comments(breed_name, proportion, skeletal, muscular, symmetry):
    parts = []
    if proportion >= 80:
        parts.append(f'{breed_name}のプロポーションは良好です')
    else:
        parts.append(f'{breed_name}のプロポーションに改善の余地があります')

    if skeletal >= 80:
        parts.append('体の輪郭が明確で骨格構造がしっかりしています')
    else:
        parts.append('骨格の輪郭がやや不明瞭です')

    if muscular >= 80:
        parts.append('筋肉の発達が適度に確認できます')
    else:
        parts.append('筋肉の定義がやや弱い可能性があります')

    if symmetry >= 0.85:
        parts.append('左右のバランスが良好です')

    return '。'.join(parts) + '。'


# ---------------------------------------------------------------------------
# Coat Analysis (photo)
# ---------------------------------------------------------------------------

def analyze_coat_local(image_base64, breed_name, breed_data):
    """Analyse coat quality from a single photo using OpenCV.

    中心線で左右分割し、犬の体のみ（背景除外）で被毛テクスチャ・
    色彩・均一性を評価する。毛のノイズの影響を最小化。
    """
    if not CV2_AVAILABLE:
        return None

    try:
        img = _decode_base64_image(image_base64)
        if img is None:
            return None
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h_img, w_img = gray.shape

        # --- Step 1: Detect dog mask, centerline, and full skeleton -----------
        mask, centroid, _mask_quality = _detect_dog_mask(img)
        centerline = _detect_centerline_cv(img, mask)
        skeleton = _detect_full_skeleton_cv(img, mask)
        dog_pixels = max(np.count_nonzero(mask), 1)

        # --- FCI coat type parameters ----------------------------------------
        coat_type = breed_data.get('coat_type', 'medium')
        texture_expectation = breed_data.get('texture_expectation', 'medium')

        # Adjust texture range based on FCI coat type
        # Long/curly coats have higher Laplacian variance (more texture detail)
        # Short coats have lower Laplacian variance
        if texture_expectation == 'high':  # long/curly coat
            tex_min, tex_max = 100, 2500
        elif texture_expectation == 'low':  # short coat
            tex_min, tex_max = 20, 1200
        else:
            tex_min, tex_max = 50, 2000

        # --- Texture: Laplacian variance within dog mask ---------------------
        lap = cv2.Laplacian(gray, cv2.CV_64F)
        lap_dog = lap.copy()
        lap_dog[mask == 0] = 0
        lap_var = np.var(lap_dog[mask > 0]) if dog_pixels > 100 else 0
        texture_score = _normalize(lap_var, tex_min, tex_max, 65, 95)

        # --- Volume: saturation & value spread within dog region -------------
        sat_channel = hsv[:, :, 1].astype(np.float32)
        val_channel = hsv[:, :, 2].astype(np.float32)
        sat_dog = sat_channel[mask > 0]
        val_dog = val_channel[mask > 0]
        sat_std = float(np.std(sat_dog)) if len(sat_dog) > 10 else 0
        val_std = float(np.std(val_dog)) if len(val_dog) > 10 else 0
        color_richness = (sat_std + val_std) / 2
        # Adjust volume expectation by coat type
        if coat_type in ('long', 'curly'):
            vol_min, vol_max = 25, 90  # Long coats show more color richness
        elif coat_type == 'short':
            vol_min, vol_max = 15, 65  # Short coats have less variation
        else:
            vol_min, vol_max = 20, 80
        volume_score = _normalize(color_richness, vol_min, vol_max, 65, 95)

        # --- Grooming: uniformity within dog region, left/right balance ------
        block_size = max(h_img, w_img) // 8
        if block_size < 4:
            block_size = 4
        block_vars = []
        for y in range(0, h_img - block_size, block_size):
            for x in range(0, w_img - block_size, block_size):
                block_mask = mask[y:y + block_size, x:x + block_size]
                if np.count_nonzero(block_mask) < block_size * block_size * 0.3:
                    continue  # Skip blocks that are mostly background
                block = gray[y:y + block_size, x:x + block_size].astype(np.float32)
                block[block_mask == 0] = np.nan
                block_var = np.nanvar(block)
                if not np.isnan(block_var):
                    block_vars.append(block_var)
        if block_vars:
            var_of_vars = np.std(block_vars)
            grooming_score = _normalize(1.0 / (1.0 + var_of_vars / 500), 0.2, 0.9, 65, 95)
        else:
            grooming_score = 78.0

        # Centerline left/right coat uniformity bonus
        coat_balance_bonus = 0.0
        if centerline:
            result = _split_by_centerline_cv(gray, centerline)
            if result:
                side_a, side_b, mask_a, mask_b = result
                # Compare coat texture on each side
                dog_a = mask_a & (mask > 0).astype(np.uint8)
                dog_b = mask_b & (mask > 0).astype(np.uint8)
                a_vals = gray[dog_a > 0]
                b_vals = gray[dog_b > 0]
                if len(a_vals) > 10 and len(b_vals) > 10:
                    # Compare means and stds
                    mean_diff = abs(float(np.mean(a_vals)) - float(np.mean(b_vals)))
                    std_diff = abs(float(np.std(a_vals)) - float(np.std(b_vals)))
                    balance = 1.0 - min((mean_diff + std_diff) / 100.0, 1.0)
                    coat_balance_bonus = balance * 3.0

        # --- Brightness check ------------------------------------------------
        mean_val = float(np.mean(val_dog)) if len(val_dog) > 0 else 150
        brightness_penalty = abs(mean_val - 150) / 150 * 5
        brightness_bonus = max(0, 5 - brightness_penalty)

        overall = (texture_score * 0.35 + volume_score * 0.35
                   + grooming_score * 0.30 + brightness_bonus + coat_balance_bonus)
        overall = _clamp(overall)

        comments = _build_coat_comments(
            breed_name, texture_score, volume_score, grooming_score
        )
        if centerline and coat_balance_bonus > 1.5:
            comments += ' 中心線基準で左右の被毛バランスが良好です。'
        if skeleton:
            comments += f' ({_skeleton_summary(skeleton)})'

        return {
            'score': float(round(overall, 1)),
            'texture': int(round(texture_score)),
            'volume': int(round(volume_score)),
            'grooming': int(round(grooming_score)),
            'comments': comments,
            'details': '全身中心線検出＋犬マスク抽出＋テクスチャ解析・色彩分析・均一性評価',
            'centerline_detected': centerline is not None,
        }

    except Exception as e:
        logger.error(f"Local coat analysis error: {e}")
        raise AnalysisError(f"Coat analysis failed: {e}") from e


def _build_coat_comments(breed_name, texture, volume, grooming):
    parts = []
    if texture >= 80:
        parts.append(f'{breed_name}の被毛のテクスチャは鮮明で良好です')
    else:
        parts.append(f'{breed_name}の被毛のテクスチャがやや不鮮明です')

    if volume >= 80:
        parts.append('毛量と色彩の豊かさが確認できます')
    else:
        parts.append('毛量や色彩にやや物足りなさがあります')

    if grooming >= 80:
        parts.append('グルーミング状態は均一で手入れが行き届いています')
    else:
        parts.append('グルーミングのムラが見受けられます')

    return '。'.join(parts) + '。'


# ---------------------------------------------------------------------------
# Video Analysis (gait, temperament, coat motion)
# ---------------------------------------------------------------------------

def analyze_video_local(video_base64_frames, breed_name, breed_data):
    """Analyse video frames for gait, temperament, and coat motion using OpenCV.

    アルゴリズム主導の動画評価エンジン（AIに依存しない）:
    1. 各フレームで犬のシルエットから全身中心線を検出
    2. ストライド（歩幅）をフレーム間中心線変位から算出
    3. ピッチ（体軸の上下動）を中心線角度変動から算出
    4. 各体の中心線からスタンダードにて評価・スコアリング
    5. 犬種別の細かい係数で自然なバラツキを実現
    """
    if not CV2_AVAILABLE or not video_base64_frames:
        return None

    try:
        frames = []
        for b64 in video_base64_frames:
            img = _decode_base64_image(b64)
            if img is not None:
                frames.append(img)

        if len(frames) < 2:
            return None

        # --- Dog Focus Preprocessing ----------------------------------------
        frames = preprocess_dog_focus(frames)

        grays = [cv2.cvtColor(f, cv2.COLOR_BGR2GRAY) for f in frames]

        # Get breed-specific gait coefficients
        gait_coeff = _get_gait_coefficients(breed_data)
        ideal_stride_ratio, stride_tolerance, ideal_pitch, pitch_tolerance, cycle_reg_weight = gait_coeff

        # --- Step 1: Detect full skeleton + angle in each frame ----------------
        centerlines = []
        skeletons = []
        frame_angles = []
        for f in frames:
            cl = _detect_centerline_cv(f)
            sk = _detect_full_skeleton_cv(f)
            centerlines.append(cl)
            skeletons.append(sk)
            # AngleCheck per frame (lightweight — reuses existing contours)
            try:
                m, _, _mq = _detect_dog_mask(f)
                frame_angles.append(estimate_angle_from_mask(m))
            except Exception:
                frame_angles.append({'label': 'unknown', 'confidence': 0.0,
                                     'scores': {'front': 0, 'side': 0, 'oblique': 0},
                                     'quality': 'unknown', 'note': ''})

        valid_centerlines = [cl for cl in centerlines if cl is not None]
        valid_skeletons = [sk for sk in skeletons if sk is not None]

        # --- Dynamic subsegment: remove still / stopped frames -------------
        total_frame_count = len(frames)
        all_centers = [cl['center'] if cl is not None else None for cl in centerlines]
        dynamic_seg = select_dynamic_subsegment(frames, all_centers, min_len=6)
        dynamic_applied = False

        if dynamic_seg['found']:
            ds, de = dynamic_seg['start'], dynamic_seg['end']
            frames = frames[ds:de]
            grays = grays[ds:de]
            centerlines = centerlines[ds:de]
            skeletons = skeletons[ds:de]
            frame_angles = frame_angles[ds:de]
            # Rebuild valid lists from sliced data
            valid_centerlines = [cl for cl in centerlines if cl is not None]
            valid_skeletons = [sk for sk in skeletons if sk is not None]
            dynamic_applied = True

        # --- Speed normalization: remove too-fast / too-slow frames --------
        dynamic_frame_count = len(frames)
        if dynamic_seg['found']:
            speed_centers = [cl['center'] if cl is not None else None
                             for cl in centerlines]
            speed_proxies = [
                compute_motion_proxy(frames[i], frames[i + 1],
                                     speed_centers[i], speed_centers[i + 1])
                for i in range(len(frames) - 1)
            ]
            speed_seg = select_speed_normalized_segment(
                speed_proxies, min_len=6, low_q=0.20, high_q=0.95)

            if speed_seg['found']:
                ss, se = speed_seg['start'], speed_seg['end']
                frames = frames[ss:se]
                grays = grays[ss:se]
                centerlines = centerlines[ss:se]
                skeletons = skeletons[ss:se]
                frame_angles = frame_angles[ss:se]
                valid_centerlines = [cl for cl in centerlines if cl is not None]
                valid_skeletons = [sk for sk in skeletons if sk is not None]
        else:
            speed_seg = {'found': False, 'start': 0, 'end': 0, 'length': 0,
                         'low_th': 0.0, 'high_th': 0.0, 'kept_ratio': 0.0,
                         'reason': 'no_dynamic_segment'}

        # --- Centerline tracking metrics ------------------------------------
        topline_scores = []
        angle_changes = []  # pitch: body angle oscillation
        center_displacements = []  # stride: horizontal displacement
        spine_lengths = []
        frame_angulations = []

        for cl in valid_centerlines:
            topline_scores.append(cl['topline_straightness'])
            spine_lengths.append(cl['length'])

        for sk in valid_skeletons:
            angles = _score_part_angles(sk, breed_data)
            if angles:
                frame_angulations.append(angles)

        # === STRIDE MEASUREMENT =============================================
        # Measure stride as principal-axis projected forward displacement
        # (more stable than hypot which conflates lateral sway with forward stride)
        stride_ratios_raw = []
        for i in range(1, len(centerlines)):
            if centerlines[i] is not None and centerlines[i - 1] is not None:
                # Pitch: angle change between frames (body oscillation)
                da = abs(centerlines[i]['angle'] - centerlines[i - 1]['angle'])
                if da > math.pi:
                    da = 2 * math.pi - da
                angle_changes.append(da)
                # Stride: project center displacement onto principal axis
                avg_angle = (centerlines[i]['angle'] + centerlines[i - 1]['angle']) / 2
                u = (math.cos(avg_angle), math.sin(avg_angle))
                dx = centerlines[i]['center'][0] - centerlines[i - 1]['center'][0]
                dy = centerlines[i]['center'][1] - centerlines[i - 1]['center'][1]
                forward_stride = abs(dx * u[0] + dy * u[1])
                center_displacements.append(forward_stride)
                # Normalize by average spine length for breed-comparable metric
                avg_spine = (centerlines[i]['length'] + centerlines[i - 1]['length']) / 2
                if avg_spine > 0:
                    stride_ratios_raw.append(forward_stride / avg_spine)

        # IQR outlier removal for stability (fallback to raw if too few remain)
        stride_ratios = _iqr_filter(stride_ratios_raw) if stride_ratios_raw else []

        # === PITCH MEASUREMENT ==============================================
        # Pitch = body angle oscillation (vertical bobbing of centerline)
        # IQR outlier removal for pitch stability
        pitch_values = _iqr_filter(angle_changes) if angle_changes else []

        # --- Optical flow between consecutive frames -------------------------
        flow_magnitudes = []
        flow_angle_stds = []
        for i in range(len(grays) - 1):
            flow = cv2.calcOpticalFlowFarneback(
                grays[i], grays[i + 1], None,
                pyr_scale=0.5, levels=3, winsize=15,
                iterations=3, poly_n=5, poly_sigma=1.2, flags=0
            )
            mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
            flow_magnitudes.append(np.mean(mag))
            flow_angle_stds.append(np.std(ang))

        avg_magnitude = np.mean(flow_magnitudes) if flow_magnitudes else 0
        mag_std = np.std(flow_magnitudes) if len(flow_magnitudes) > 1 else 0
        avg_angle_std = np.mean(flow_angle_stds) if flow_angle_stds else 0

        # --- FCI gait type parameters ----------------------------------------
        gait_type = breed_data.get('gait_type', 'balanced')
        expected_stride = breed_data.get('expected_stride', 'moderate')
        gait_evidence = breed_data.get('gait_evidence', {})

        # Adjust stride expectations based on FCI gait type
        if expected_stride == 'long' or gait_type == 'powerful':
            stride_min, stride_max = 10.0, 100.0
            flow_min, flow_max = 1.0, 12.0
        elif gait_type == 'elegant':
            stride_min, stride_max = 5.0, 70.0
            flow_min, flow_max = 0.5, 8.0
        else:
            stride_min, stride_max = 5.0, 80.0
            flow_min, flow_max = 0.5, 8.0

        # === GAIT SCORING (algorithm-driven) =================================

        # --- Stride score: measured ratio vs breed ideal ---
        if stride_ratios:
            avg_stride_ratio = np.mean(stride_ratios)
            stride_dev = abs(avg_stride_ratio - ideal_stride_ratio) / max(stride_tolerance, 0.001)
            stride_match = 1.0 / (1.0 + stride_dev ** 2)
            stride_score = _normalize(stride_match, 0.0, 1.0, 60, 97)

            # Stride regularity (consistency of gait cycle)
            stride_std = np.std(stride_ratios)
            regularity = 1.0 / (1.0 + stride_std / max(np.mean(stride_ratios), 0.001) * 5)
            stride_regularity = _normalize(regularity, 0.0, 1.0, 60, 97)
            stride_score = stride_score * (1.0 - cycle_reg_weight) + stride_regularity * cycle_reg_weight
        elif center_displacements:
            avg_displacement = np.mean(center_displacements)
            disp_std = np.std(center_displacements)
            stride_score_cl = _normalize(avg_displacement, stride_min, stride_max, 62, 95)
            stride_regularity = _normalize(1.0 / (1.0 + disp_std / max(avg_displacement, 1)),
                                           0.3, 0.9, 62, 95)
            stride_score = stride_score_cl * 0.6 + stride_regularity * 0.4
        else:
            stride_score = _normalize(avg_magnitude, flow_min / 2, flow_max, 62, 95)

        # --- Pitch score: measured oscillation vs breed ideal ---
        if pitch_values:
            avg_pitch = np.mean(pitch_values)
            pitch_dev = abs(avg_pitch - ideal_pitch) / max(pitch_tolerance, 0.0001)
            pitch_match = 1.0 / (1.0 + pitch_dev ** 2)
            pitch_score = _normalize(pitch_match, 0.0, 1.0, 60, 97)
        else:
            # Fallback: topline angle stability
            pitch_score = _normalize(1.0 / (1.0 + mag_std), 0.3, 0.9, 62, 95)

        # --- Balance: topline angle stability + pitch ---
        if angle_changes:
            avg_angle_change = np.mean(angle_changes)
            stability_weight = 12 if gait_type == 'steady' else 10
            balance_score = _normalize(1.0 / (1.0 + avg_angle_change * stability_weight),
                                       0.3, 0.9, 60, 97)
        else:
            balance_score = _normalize(1.0 / (1.0 + mag_std), 0.3, 0.9, 62, 95)

        # --- Fluidity from optical flow ---
        fluidity_score = _normalize(
            1.0 - abs(avg_angle_std - 1.0) / 2.0, 0.0, 1.0, 62, 95
        )

        # Evidence-based calibration offset
        evidence_offset = float(gait_evidence.get('calibration_offset', 0))

        # Topline maintenance (spine straightness across frames)
        topline_bonus = 0.0
        if topline_scores:
            avg_topline = np.mean(topline_scores)
            topline_bonus = avg_topline * 4.0

        gait_overall = (stride_score * 0.28 + pitch_score * 0.22 +
                        balance_score * 0.25 + fluidity_score * 0.15 +
                        topline_bonus)
        if evidence_offset:
            gait_overall += evidence_offset
        gait_overall = _clamp(gait_overall)

        # Mild penalty when dynamic subsegment could not be isolated
        if not dynamic_seg['found']:
            gait_overall = _clamp(gait_overall * 0.9)
        # Mild penalty when speed normalization could not be applied
        if dynamic_seg['found'] and not speed_seg['found']:
            gait_overall = _clamp(gait_overall * 0.9)

        # --- Temperament scoring ---------------------------------------------
        hist_corrs = []
        for i in range(len(grays) - 1):
            h1 = cv2.calcHist([grays[i]], [0], None, [64], [0, 256]).flatten().astype(np.float32)
            h2 = cv2.calcHist([grays[i + 1]], [0], None, [64], [0, 256]).flatten().astype(np.float32)
            corr = cv2.compareHist(h1, h2, cv2.HISTCMP_CORREL)
            hist_corrs.append(corr)

        avg_corr = np.mean(hist_corrs) if hist_corrs else 0.9

        confidence_score = _normalize(avg_magnitude, 0.3, 5.0, 62, 95)
        alertness_score = _normalize(avg_angle_std, 0.3, 2.0, 62, 95)
        composure_score = _normalize(avg_corr, 0.7, 0.99, 62, 95)

        temperament_overall = (confidence_score * 0.35 + alertness_score * 0.30
                               + composure_score * 0.35)
        temperament_overall = _clamp(temperament_overall)

        # --- Coat motion scoring ---------------------------------------------
        color_diffs = []
        for i in range(len(frames) - 1):
            diff = cv2.absdiff(frames[i], frames[i + 1])
            color_diffs.append(np.mean(diff))

        avg_color_diff = np.mean(color_diffs) if color_diffs else 0
        coat_motion_score = _normalize(avg_color_diff, 2.0, 30.0, 62, 95)
        coat_motion_score = _clamp(coat_motion_score)

        gait_comments = _build_gait_comments(breed_name, stride_score, balance_score, fluidity_score)
        temperament_comments = _build_temperament_comments(
            breed_name, confidence_score, alertness_score, composure_score
        )

        # Stride/pitch measurement comments
        if stride_ratios:
            avg_sr = np.mean(stride_ratios)
            gait_comments += f' ストライド比: {avg_sr:.3f}（犬種理想: {ideal_stride_ratio:.3f}）。'
        if pitch_values:
            avg_pv = np.mean(pitch_values)
            gait_comments += f' ピッチ安定性: {math.degrees(avg_pv):.1f}°/フレーム。'

        # Topline comment
        if topline_scores:
            avg_tl = np.mean(topline_scores)
            if avg_tl >= 0.7:
                gait_comments += f' トップラインが安定して維持されています（直線性{avg_tl:.0%}）。'
            else:
                gait_comments += f' トップラインにやや変動が見られます（直線性{avg_tl:.0%}）。'

        # Angulation tracking from skeleton
        angulation_bonus = 0.0
        if frame_angulations:
            shoulder_vals = [a['shoulder_angle'] for a in frame_angulations
                           if 'shoulder_angle' in a]
            rear_vals = [a['rear_angle'] for a in frame_angulations
                        if 'rear_angle' in a]
            if shoulder_vals:
                avg_sa = np.mean(shoulder_vals)
                sa_std = np.std(shoulder_vals) if len(shoulder_vals) > 1 else 0
                if avg_sa >= 0.7 and sa_std < 0.15:
                    gait_comments += ' 肩のアンギュレーションが動作中も安定しています。'
                    angulation_bonus += 2.0
            if rear_vals:
                avg_ra = np.mean(rear_vals)
                ra_std = np.std(rear_vals) if len(rear_vals) > 1 else 0
                if avg_ra >= 0.7 and ra_std < 0.15:
                    gait_comments += ' 後躯の推進力が安定しています。'
                    angulation_bonus += 2.0
            fl_sym = [a['front_leg_symmetry'] for a in frame_angulations
                     if 'front_leg_symmetry' in a]
            if fl_sym:
                avg_sym = np.mean(fl_sym)
                if avg_sym >= 0.8:
                    gait_comments += ' 前脚の動きが左右対称です。'
                    angulation_bonus += 1.0

        gait_overall = _clamp(gait_overall + angulation_bonus)

        cl_count = len(valid_centerlines)
        sk_count = len(valid_skeletons)
        cl_detail = (f'全身骨格検出{sk_count}/{len(frames)}フレーム, '
                     f'中心線{cl_count}/{len(frames)}フレーム')

        # Build raw measurements for transparency
        raw_gait_measurements = {
            'stride_ratio_avg': round(np.mean(stride_ratios), 4) if stride_ratios else None,
            'stride_ratio_std': round(np.std(stride_ratios), 4) if stride_ratios else None,
            'stride_samples': len(stride_ratios),
            'stride_samples_raw': len(stride_ratios_raw),
            'pitch_avg_deg': round(math.degrees(np.mean(pitch_values)), 2) if pitch_values else None,
            'pitch_std_deg': round(math.degrees(np.std(pitch_values)), 2) if len(pitch_values) > 1 else None,
            'pitch_samples': len(pitch_values),
            'topline_avg': round(np.mean(topline_scores), 3) if topline_scores else None,
            'spine_length_avg': round(np.mean(spine_lengths), 1) if spine_lengths else None,
            'ideal_stride_ratio': ideal_stride_ratio,
            'ideal_pitch_stability': ideal_pitch,
            'breed_gait_group': _get_breed_angle_group(breed_data),
            'frames_analyzed': len(frames),
        }

        # Build reasons[] for explainability
        gait_reasons = []
        if stride_ratios:
            gait_reasons.append(f'stride_ratio={np.mean(stride_ratios):.4f}')
        if pitch_values:
            gait_reasons.append(f'pitch_deg={math.degrees(np.mean(pitch_values)):.2f}')
        if topline_scores:
            gait_reasons.append(f'topline={np.mean(topline_scores):.3f}')
        gait_reasons.append(f'stride_score={stride_score:.1f}')
        gait_reasons.append(f'balance_score={balance_score:.1f}')
        gait_reasons.append(f'fluidity={fluidity_score:.1f}')
        gait_reasons.append(f'frames={len(frames)}')

        # Low frame count warning (analysable but lower confidence)
        gait_confidence = 'high' if len(frames) >= 8 else ('medium' if len(frames) >= 4 else 'low')

        # Dynamic / speed segment confidence damping
        video_warnings = []
        if not dynamic_seg['found'] and dynamic_seg['reason'] != 'no_motion':
            video_warnings.append('no_dynamic_segment')
        if not dynamic_seg['found'] and gait_confidence == 'high':
            gait_confidence = 'medium'
        if dynamic_seg['found'] and not speed_seg['found']:
            video_warnings.append('no_speed_segment')
            if gait_confidence == 'high':
                gait_confidence = 'medium'

        # --- AngleCheck: aggregate per-frame angle estimates -------------------
        angle_labels = [a['label'] for a in frame_angles if a['label'] != 'unknown']
        angle_confs = [a['confidence'] for a in frame_angles]
        if angle_labels:
            from collections import Counter
            label_counts = Counter(angle_labels)
            majority_label = label_counts.most_common(1)[0][0]
            majority_ratio = label_counts[majority_label] / len(angle_labels)
            avg_angle_conf = float(np.mean(angle_confs)) if angle_confs else 0.0
            # Consistency check
            if majority_ratio < 0.6:
                video_warnings.append('angle_inconsistent')
            if majority_label != 'side':
                video_warnings.append('angle_not_side')
                gait_overall = _clamp(gait_overall * 0.85)
                gait_confidence = 'medium' if gait_confidence == 'high' else gait_confidence
        else:
            majority_label = 'unknown'
            avg_angle_conf = 0.0
            majority_ratio = 0.0

        angle_summary = {
            'label': majority_label,
            'confidence': round(avg_angle_conf, 3),
            'consistency': round(majority_ratio, 3),
            'frame_count': len(frame_angles),
            'note': ('サイドビューで安定した撮影です。' if majority_label == 'side' and majority_ratio >= 0.6
                     else '歩様評価には横向き（サイドビュー）での撮影を推奨します。'),
        }

        return {
            'gait': {
                'score': float(round(gait_overall, 1)),
                'stride': int(round(stride_score)),
                'pitch': int(round(pitch_score)),
                'balance': int(round(balance_score)),
                'fluidity': int(round(fluidity_score)),
                'comments': gait_comments,
                'details': f'アルゴリズム主導: ストライド/ピッチ/中心線→犬種スタンダード比較 ({cl_detail})',
                'raw_measurements': raw_gait_measurements,
                'reasons': gait_reasons,
                'confidence': gait_confidence,
                'dynamic_segment': dynamic_seg,
                'speed_segment': speed_seg,
                'frames_used': {
                    'total': total_frame_count,
                    'dynamic_used': dynamic_frame_count,
                    'speed_used': speed_seg['length'] if speed_seg['found'] else dynamic_frame_count,
                },
            },
            'temperament': {
                'score': float(round(temperament_overall, 1)),
                'confidence': int(round(confidence_score)),
                'alertness': int(round(alertness_score)),
                'composure': int(round(composure_score)),
                'comments': temperament_comments,
                'details': f'{cl_detail}＋犬フォーカス前処理＋フレーム安定性解析'
            },
            'coat_motion': {
                'score': float(round(coat_motion_score, 1)),
                'comments': f'{breed_name}の動きの中での被毛の状態をフレーム差分で評価しました。',
                'details': f'{cl_detail}＋犬フォーカス前処理＋フレーム差分解析'
            },
            'angle_summary': angle_summary,
            'warnings': video_warnings,
        }

    except Exception as e:
        logger.error(f"Local video analysis error: {e}")
        raise AnalysisError(f"Video analysis failed: {e}") from e


def _build_gait_comments(breed_name, stride, balance, fluidity):
    parts = []
    if stride >= 80:
        parts.append(f'{breed_name}の歩幅は適度で力強い動きが確認できます')
    elif stride >= 65:
        parts.append(f'{breed_name}の歩幅はやや控えめです')
    else:
        parts.append(f'{breed_name}の動きが少なく歩様の評価が困難です')

    if balance >= 80:
        parts.append('動きのバランスが安定しています')
    else:
        parts.append('動きにやや不安定さが見られます')

    if fluidity >= 80:
        parts.append('流れるような滑らかな動きです')
    else:
        parts.append('動きの流動性に改善の余地があります')

    return '。'.join(parts) + '。'


def _build_temperament_comments(breed_name, confidence, alertness, composure):
    parts = []
    if confidence >= 80:
        parts.append(f'{breed_name}は自信に満ちた動きを見せています')
    else:
        parts.append(f'{breed_name}の動きにやや自信のなさが見受けられます')

    if alertness >= 80:
        parts.append('注意力が高く周囲への反応が良好です')
    else:
        parts.append('注意力がやや低い印象です')

    if composure >= 80:
        parts.append('落ち着きがあり安定した気質です')
    else:
        parts.append('やや落ち着きに欠ける様子が見られます')

    return '。'.join(parts) + '。'


# ---------------------------------------------------------------------------
# Pillow Fallback Analysis (when OpenCV is not available)
# ---------------------------------------------------------------------------
# Uses Pillow (PIL) for basic image feature extraction.
# Less accurate than OpenCV but provides real image-based scoring.

try:
    import io as _io

    from PIL import Image as PILImage
    from PIL import ImageFilter, ImageStat
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False


def _decode_base64_pil(b64_string):
    """Decode base64 string into a PIL Image."""
    img_bytes = base64.b64decode(b64_string)
    return PILImage.open(_io.BytesIO(img_bytes))


def analyze_structure_pil(image_base64, breed_name, breed_data):
    """Analyse body structure using Pillow (fallback when OpenCV unavailable).

    中心線を検出し、それを基準に骨格・対称性・プロポーションを評価。
    毛のノイズに影響されない分析を実現。
    """
    if not PIL_AVAILABLE:
        return None
    try:
        img = _decode_base64_pil(image_base64)
        w, h = img.size
        gray = img.convert('L')
        gray_arr = np.array(gray, dtype=np.float32)
        stat = ImageStat.Stat(gray)

        # --- Step 1: Detect centerline and full skeleton -----------------------
        centerline = _detect_centerline_pil(img)
        skeleton = _detect_full_skeleton_pil(img)
        part_angles = _score_part_angles(skeleton)

        # --- Proportion: spine length vs perpendicular body width ------------
        if centerline and centerline['length'] > 0:
            # Estimate body width by measuring perpendicular extent
            cx, cy = centerline['center']
            angle = centerline['angle']
            perp_x = -math.sin(angle)
            perp_y = math.cos(angle)
            # Use foreground detection to measure width
            border = np.concatenate([
                gray_arr[0, :], gray_arr[-1, :], gray_arr[:, 0], gray_arr[:, -1]
            ])
            bg_mean = float(np.mean(border))
            bg_std = float(np.std(border)) + 1.0
            fg_mask = (np.abs(gray_arr - bg_mean) / bg_std > 1.0).astype(np.uint8)
            widths = []
            for offset in range(-5, 6):
                px = int(cx + math.cos(angle) * offset * centerline['length'] / 20)
                py = int(cy + math.sin(angle) * offset * centerline['length'] / 20)
                if 0 <= py < h and 0 <= px < w:
                    count = 0
                    for d in range(1, max(h, w)):
                        nx, ny = int(px + perp_x * d), int(py + perp_y * d)
                        if 0 <= ny < h and 0 <= nx < w and fg_mask[ny, nx] > 0:
                            count += 1
                        else:
                            break
                    for d in range(1, max(h, w)):
                        nx, ny = int(px - perp_x * d), int(py - perp_y * d)
                        if 0 <= ny < h and 0 <= nx < w and fg_mask[ny, nx] > 0:
                            count += 1
                        else:
                            break
                    if count > 0:
                        widths.append(count)
            body_width = float(np.mean(widths)) if widths else h * 0.5
            body_ratio = centerline['length'] / max(body_width, 1.0)
            ideal_ratio = float(breed_data.get('ideal_ratio', 1.4))
            ratio_diff = abs(body_ratio - ideal_ratio)
            proportion_score = _normalize(1.0 - min(ratio_diff / ideal_ratio, 1.0),
                                          0.0, 1.0, 65, 95)
        else:
            aspect = w / h if h > 0 else 1.0
            ideal_ratio = float(breed_data.get('ideal_ratio', 1.4))
            ratio_diff = abs(aspect - ideal_ratio)
            proportion_score = _normalize(1.0 - min(ratio_diff, 1.0), 0.0, 1.0, 65, 95)

        # --- Skeletal: edge + topline straightness ---------------------------
        edges = gray.filter(ImageFilter.FIND_EDGES)
        edge_stat = ImageStat.Stat(edges)
        edge_mean = edge_stat.mean[0] / 255.0
        edge_density_target = float(breed_data.get('edge_density_target', 0.12))
        edge_score = _normalize(
            1.0 - abs(edge_mean - edge_density_target) / edge_density_target, 0.0, 1.0, 65, 95
        )
        if centerline:
            topline = centerline['topline_straightness']
            skeletal_score = edge_score * 0.6 + _normalize(topline, 0.3, 0.9, 65, 95) * 0.4
        else:
            skeletal_score = edge_score

        # --- Muscular: sharpness (pixel value standard deviation) ------------
        sharpness = stat.stddev[0]
        muscular_score = _normalize(sharpness, 30, 80, 65, 95)

        # --- Symmetry: centerline-based (robust to fur noise) ----------------
        if centerline:
            symmetry_val = _centerline_symmetry(gray_arr, centerline)
        else:
            left = gray.crop((0, 0, w // 2, h))
            right = gray.crop((w // 2, 0, w, h)).transpose(PILImage.FLIP_LEFT_RIGHT)
            min_w2 = min(left.size[0], right.size[0])
            left = left.crop((0, 0, min_w2, h))
            right = right.crop((0, 0, min_w2, h))
            left_arr = np.array(left, dtype=np.float32)
            right_arr = np.array(right, dtype=np.float32)
            diff = np.mean(np.abs(left_arr - right_arr))
            symmetry_val = 1.0 - min(diff / 60.0, 1.0)
        symmetry_bonus = _normalize(symmetry_val, 0.5, 1.0, 0, 5)

        # --- Angulation bonus from full skeleton ----------------------------
        angulation_bonus = 0.0
        if part_angles:
            angle_scores = [v for v in part_angles.values() if isinstance(v, (int, float))]
            if angle_scores:
                avg_angle_score = sum(angle_scores) / len(angle_scores)
                angulation_bonus = avg_angle_score * 5.0

        overall = (proportion_score * 0.30 + skeletal_score * 0.30
                   + muscular_score * 0.25 + symmetry_bonus + angulation_bonus)
        overall = _clamp(overall)

        comments = _build_structure_comments(
            breed_name, proportion_score, skeletal_score, muscular_score, symmetry_val
        )
        if centerline:
            comments += f' トップラインの直線性: {centerline["topline_straightness"]:.0%}。'
        if part_angles.get('shoulder_angle') is not None:
            sa = part_angles['shoulder_angle']
            if sa >= 0.7:
                comments += ' 肩のアンギュレーションが良好です。'
            else:
                comments += ' 肩のアンギュレーションに改善の余地があります。'
        if part_angles.get('rear_angle') is not None:
            ra = part_angles['rear_angle']
            if ra >= 0.7:
                comments += ' 後躯のアンギュレーションが良好です。'
            else:
                comments += ' 後躯のアンギュレーションに改善の余地があります。'
        if skeleton:
            comments += f' ({_skeleton_summary(skeleton)})'

        # Build reasons[] for explainability
        reasons = []
        if centerline:
            reasons.append(f'spine_straightness={centerline["topline_straightness"]:.2f}')
        reasons.append(f'symmetry={symmetry_val:.2f}')
        reasons.append(f'proportion_score={proportion_score:.1f}')
        reasons.append(f'skeletal_score={skeletal_score:.1f}')
        reasons.append(f'muscular_score={muscular_score:.1f}')

        return {
            'score': float(round(overall, 1)),
            'proportion': int(round(proportion_score)),
            'skeletal': int(round(skeletal_score)),
            'muscular': int(round(muscular_score)),
            'comments': comments,
            'details': '全身中心線検出＋画像特徴量抽出・多部位骨格解析（Pillowフォールバック）',
            'centerline_detected': centerline is not None,
            'skeleton_parts': _skeleton_summary(skeleton) if skeleton else None,
            'angulation': {k: round(v, 2) for k, v in part_angles.items()} if part_angles else None,
            'reasons': reasons,
        }
    except Exception as e:
        logger.error(f"PIL structure analysis error: {e}")
        raise AnalysisError(f"PIL structure analysis failed: {e}") from e


def analyze_coat_pil(image_base64, breed_name, breed_data):
    """Analyse coat quality using Pillow (fallback when OpenCV unavailable).

    中心線で左右分割し、被毛の均一性を中心線基準で評価。
    """
    if not PIL_AVAILABLE:
        return None
    try:
        img = _decode_base64_pil(image_base64)
        gray = img.convert('L')
        hsv = img.convert('HSV')
        stat_hsv = ImageStat.Stat(hsv)
        gray_arr = np.array(gray, dtype=np.float32)
        w, h = gray.size

        # --- Step 1: Detect centerline and full skeleton -----------------------
        centerline = _detect_centerline_pil(img)
        skeleton = _detect_full_skeleton_pil(img)

        # --- FCI coat type parameters ----------------------------------------
        coat_type = breed_data.get('coat_type', 'medium')
        texture_expectation = breed_data.get('texture_expectation', 'medium')

        # Adjust texture range based on FCI coat type
        if texture_expectation == 'high':
            tex_min, tex_max = 20, 80
        elif texture_expectation == 'low':
            tex_min, tex_max = 10, 50
        else:
            tex_min, tex_max = 15, 70

        # --- Texture: sharpness via edge filter ------------------------------
        edges = gray.filter(ImageFilter.FIND_EDGES)
        edge_stat = ImageStat.Stat(edges)
        texture_score = _normalize(edge_stat.stddev[0], tex_min, tex_max, 65, 95)

        # --- Volume: saturation & brightness spread --------------------------
        sat_std = stat_hsv.stddev[1]
        val_std = stat_hsv.stddev[2]
        color_richness = (sat_std + val_std) / 2
        if coat_type in ('long', 'curly'):
            vol_min, vol_max = 25, 80
        elif coat_type == 'short':
            vol_min, vol_max = 15, 55
        else:
            vol_min, vol_max = 20, 70
        volume_score = _normalize(color_richness, vol_min, vol_max, 65, 95)

        # --- Grooming: pixel uniformity --------------------------------------
        block_size = max(w, h) // 8
        if block_size < 4:
            block_size = 4
        block_vars = []
        for y in range(0, h - block_size, block_size):
            for x in range(0, w - block_size, block_size):
                block = gray_arr[y:y + block_size, x:x + block_size]
                block_vars.append(np.var(block))
        if block_vars:
            var_of_vars = np.std(block_vars)
            grooming_score = _normalize(1.0 / (1.0 + var_of_vars / 500), 0.2, 0.9, 65, 95)
        else:
            grooming_score = 78.0

        # --- Centerline left/right coat balance bonus ------------------------
        coat_balance_bonus = 0.0
        if centerline:
            result = _split_by_centerline_np(gray_arr, centerline)
            if result:
                side_a, side_b, mask_a, mask_b = result
                a_vals = side_a[mask_a > 0].flatten()
                b_vals = side_b[mask_b > 0].flatten()
                if len(a_vals) > 10 and len(b_vals) > 10:
                    mean_diff = abs(float(np.mean(a_vals)) - float(np.mean(b_vals)))
                    std_diff = abs(float(np.std(a_vals)) - float(np.std(b_vals)))
                    balance = 1.0 - min((mean_diff + std_diff) / 100.0, 1.0)
                    coat_balance_bonus = balance * 3.0

        # --- Brightness bonus ------------------------------------------------
        mean_val = stat_hsv.mean[2]
        brightness_penalty = abs(mean_val - 150) / 150 * 5
        brightness_bonus = max(0, 5 - brightness_penalty)

        overall = (texture_score * 0.35 + volume_score * 0.35
                   + grooming_score * 0.30 + brightness_bonus + coat_balance_bonus)
        overall = _clamp(overall)

        comments = _build_coat_comments(
            breed_name, texture_score, volume_score, grooming_score
        )
        if centerline and coat_balance_bonus > 1.5:
            comments += ' 中心線基準で左右の被毛バランスが良好です。'
        if skeleton:
            comments += f' ({_skeleton_summary(skeleton)})'

        return {
            'score': float(round(overall, 1)),
            'texture': int(round(texture_score)),
            'volume': int(round(volume_score)),
            'grooming': int(round(grooming_score)),
            'comments': comments,
            'details': '全身中心線検出＋テクスチャ解析・色彩分析・均一性評価（Pillowフォールバック）',
            'centerline_detected': centerline is not None,
        }
    except Exception as e:
        logger.error(f"PIL coat analysis error: {e}")
        raise AnalysisError(f"PIL coat analysis failed: {e}") from e
