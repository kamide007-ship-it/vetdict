"""
Generic Local Analysis Module (OpenCV)
Domain-agnostic image/video analysis fallback.
Provides structure, appearance, and motion scoring from raw pixels.
"""

import base64
import logging

import numpy as np

logger = logging.getLogger(__name__)

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    logger.warning("OpenCV not available - local analysis disabled")


def _decode_base64_image(b64):
    arr = np.frombuffer(base64.b64decode(b64), dtype=np.uint8)
    return cv2.imdecode(arr, cv2.IMREAD_COLOR)


def _clamp(v, lo=0.0, hi=100.0):
    return max(lo, min(hi, v))


def _normalize(v, min_v, max_v, lo=60.0, hi=95.0):
    if max_v <= min_v:
        return (lo + hi) / 2
    return _clamp(lo + (v - min_v) / (max_v - min_v) * (hi - lo))


# =========================================================================
# Primary Analysis (structure/proportion from photo)
# =========================================================================

def analyze_primary_local(image_base64, category_name, category_data):
    """Evaluate structure: edge density, symmetry, sharpness, subject size."""
    if not CV2_AVAILABLE:
        return None
    try:
        img = _decode_base64_image(image_base64)
        if img is None:
            return None
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        h, w = gray.shape

        # Proportion: aspect ratio vs ideal
        aspect = w / h if h > 0 else 1.0
        ideal = float(category_data.get('ideal_ratio', 1.4))
        proportion = _normalize(1.0 - min(abs(aspect - ideal), 1.0), 0, 1, 65, 95)

        # Detail: edge density (Canny)
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.count_nonzero(edges) / (h * w)
        detail = _normalize(1.0 - abs(edge_density - 0.10) / 0.10, 0, 1, 65, 95)

        # Quality: Laplacian variance (sharpness)
        lap_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        quality = _normalize(lap_var, 50, 2000, 65, 95)

        # Symmetry bonus
        lh = gray[:, :w // 2]
        rh = cv2.flip(gray[:, w // 2:], 1)
        mw = min(lh.shape[1], rh.shape[1])
        h_l = cv2.calcHist([lh[:, :mw]], [0], None, [64], [0, 256]).flatten().astype(np.float32)
        h_r = cv2.calcHist([rh[:, :mw]], [0], None, [64], [0, 256]).flatten().astype(np.float32)
        sym = cv2.compareHist(h_l, h_r, cv2.HISTCMP_CORREL)
        sym_bonus = _normalize(sym, 0.5, 1.0, 0, 5)

        overall = proportion * 0.35 + detail * 0.35 + quality * 0.30 + sym_bonus
        return {
            'score': round(_clamp(overall), 1),
            'proportion': round(proportion),
            'detail': round(detail),
            'quality': round(quality),
            'comments': f'{category_name}の構造解析をローカルアルゴリズムで実施しました。',
            'details': 'ローカル解析（エッジ検出・対称性・シャープネス）'
        }
    except Exception as e:
        logger.error(f"Local primary analysis error: {e}")
        return None


# =========================================================================
# Secondary Analysis (appearance/texture from photo)
# =========================================================================

def analyze_secondary_local(image_base64, category_name, category_data):
    """Evaluate appearance: texture sharpness, color richness, uniformity."""
    if not CV2_AVAILABLE:
        return None
    try:
        img = _decode_base64_image(image_base64)
        if img is None:
            return None
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h_img, w_img = gray.shape

        # Texture (sharpness)
        lap_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        texture = _normalize(lap_var, 50, 2000, 65, 95)

        # Color richness
        sat_std = np.std(hsv[:, :, 1])
        val_std = np.std(hsv[:, :, 2])
        color = _normalize((sat_std + val_std) / 2, 20, 80, 65, 95)

        # Uniformity (block variance)
        bs = max(h_img, w_img) // 8
        if bs < 4:
            bs = 4
        bvars = []
        for y in range(0, h_img - bs, bs):
            for x in range(0, w_img - bs, bs):
                bvars.append(np.var(gray[y:y + bs, x:x + bs]))
        condition = _normalize(1.0 / (1.0 + np.std(bvars) / 500), 0.2, 0.9, 65, 95) if bvars else 78.0

        overall = texture * 0.35 + color * 0.35 + condition * 0.30
        return {
            'score': round(_clamp(overall), 1),
            'texture': round(texture),
            'color': round(color),
            'condition': round(condition),
            'comments': f'{category_name}の外観解析をローカルアルゴリズムで実施しました。',
            'details': 'ローカル解析（テクスチャ・色彩・均一性）'
        }
    except Exception as e:
        logger.error(f"Local secondary analysis error: {e}")
        return None


# =========================================================================
# Video Analysis (motion, behavior, surface)
# =========================================================================

def analyze_video_local(video_base64_frames, category_name, category_data):
    """Evaluate motion, behavior, and surface dynamics from video frames."""
    if not CV2_AVAILABLE or not video_base64_frames:
        return None
    try:
        frames = [_decode_base64_image(b) for b in video_base64_frames]
        frames = [f for f in frames if f is not None]
        if len(frames) < 2:
            return None

        grays = [cv2.cvtColor(f, cv2.COLOR_BGR2GRAY) for f in frames]

        # Optical flow
        mags, ang_stds = [], []
        for i in range(len(grays) - 1):
            flow = cv2.calcOpticalFlowFarneback(
                grays[i], grays[i + 1], None, 0.5, 3, 15, 3, 5, 1.2, 0)
            mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
            mags.append(np.mean(mag))
            ang_stds.append(np.std(ang))

        avg_mag = np.mean(mags) if mags else 0
        mag_std = np.std(mags) if len(mags) > 1 else 0
        avg_ang = np.mean(ang_stds) if ang_stds else 0

        # Motion scores
        fluidity = _normalize(avg_mag, 0.5, 8.0, 65, 95)
        stability = _normalize(1.0 / (1.0 + mag_std), 0.3, 0.9, 65, 95)
        rhythm = _normalize(1.0 - abs(avg_ang - 1.0) / 2.0, 0, 1, 65, 95)
        motion_overall = fluidity * 0.4 + stability * 0.35 + rhythm * 0.25

        # Behavior scores (histogram stability)
        corrs = []
        for i in range(len(grays) - 1):
            h1 = cv2.calcHist([grays[i]], [0], None, [64], [0, 256]).flatten().astype(np.float32)
            h2 = cv2.calcHist([grays[i + 1]], [0], None, [64], [0, 256]).flatten().astype(np.float32)
            corrs.append(cv2.compareHist(h1, h2, cv2.HISTCMP_CORREL))
        avg_corr = np.mean(corrs) if corrs else 0.9

        consistency = _normalize(avg_mag, 0.3, 5.0, 65, 95)
        responsiveness = _normalize(avg_ang, 0.3, 2.0, 65, 95)
        composure = _normalize(avg_corr, 0.7, 0.99, 65, 95)
        behavior_overall = consistency * 0.35 + responsiveness * 0.30 + composure * 0.35

        # Surface motion
        cdiffs = []
        for i in range(len(frames) - 1):
            cdiffs.append(np.mean(cv2.absdiff(frames[i], frames[i + 1])))
        surface = _normalize(np.mean(cdiffs) if cdiffs else 0, 2.0, 30.0, 65, 95)

        return {
            'motion': {
                'score': round(_clamp(motion_overall), 1),
                'fluidity': round(fluidity),
                'stability': round(stability),
                'rhythm': round(rhythm),
                'comments': f'{category_name}の動作をオプティカルフロー解析しました。',
                'details': 'ローカル解析（オプティカルフロー）'
            },
            'behavior': {
                'score': round(_clamp(behavior_overall), 1),
                'consistency': round(consistency),
                'responsiveness': round(responsiveness),
                'composure': round(composure),
                'comments': f'{category_name}の振る舞いをフレーム安定性で解析しました。',
                'details': 'ローカル解析（フレーム安定性）'
            },
            'surface_motion': {
                'score': round(_clamp(surface), 1),
                'comments': f'{category_name}の表面動態をフレーム差分で解析しました。',
                'details': 'ローカル解析（フレーム差分）'
            }
        }
    except Exception as e:
        logger.error(f"Local video analysis error: {e}")
        return None
