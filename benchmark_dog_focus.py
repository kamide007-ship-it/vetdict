"""
Benchmark: Dog Focus Preprocessing Accuracy Comparison

犬フォーカス前処理（背景ぼかし＋犬シャープ化＋解剖学的追跡）の
精度向上を定量的に計測するベンチマーク。

合成テストフレーム（犬領域＋背景ノイズ）を生成し、
前処理あり/なしでオプティカルフローの精度を比較する。
"""

import json
import sys
import time

import numpy as np

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    print("ERROR: OpenCV (cv2) is required for this benchmark")
    sys.exit(1)

# Import the analysis functions
sys.path.insert(0, '/home/user/showdog-app')
from api.local_analysis import (
    _normalize,
    preprocess_dog_focus,
)

# ---------------------------------------------------------------------------
# Synthetic Test Frame Generator
# ---------------------------------------------------------------------------

def generate_test_frames(num_frames=5, width=640, height=480, seed=42):
    """Generate realistic synthetic video frames simulating a dog show ring.

    - Background: smooth green floor with fence lines and spectators (uniform colors)
    - Dog: warm brown subject with fur-like texture, moving horizontally
    - Background objects: people (dark, different color) moving independently

    Returns:
        frames: list of BGR images
        dog_masks_gt: list of ground truth binary masks (255=dog)
        dog_flow_gt: ground truth optical flow magnitude for dog region
    """
    rng = np.random.RandomState(seed)
    frames = []
    dog_masks_gt = []

    # Dog parameters
    dog_cx_start = width // 4
    dog_cy = height // 2 + 20
    dog_rx = 130
    dog_ry = 75
    dog_speed_x = 15
    dog_speed_y = 2
    # Dog color (warm brown BGR)
    dog_color_body = (65, 120, 175)
    dog_color_head = (55, 110, 165)

    # Background people (dark clothing, different hue from dog)
    bg_people = []
    for _ in range(3):
        bg_people.append({
            'cx': rng.randint(100, width - 100),
            'cy': rng.randint(30, height - 80),
            'w': rng.randint(25, 45),
            'h': rng.randint(60, 100),
            'vx': rng.choice([-8, -5, -3, 3, 5, 8]),
            'vy': rng.randint(-2, 3),
            'color': (rng.randint(30, 70), rng.randint(30, 70), rng.randint(30, 70)),
        })

    for i in range(num_frames):
        # --- Smooth green background (show ring floor) ---
        bg = np.full((height, width, 3), [60, 140, 80], dtype=np.uint8)
        # Slight gradient for realism
        for y in range(height):
            shade = int(y / height * 30)
            bg[y, :] = np.clip(bg[y, :].astype(int) + shade - 15, 0, 255).astype(np.uint8)
        # Add subtle floor texture (not random noise)
        texture = rng.randint(-8, 9, (height, width, 1), dtype=np.int16)
        bg = np.clip(bg.astype(np.int16) + texture, 0, 255).astype(np.uint8)

        # Ring fence (horizontal white lines near edges)
        cv2.line(bg, (0, 40), (width, 40), (200, 200, 200), 2)
        cv2.line(bg, (0, height - 30), (width, height - 30), (200, 200, 200), 2)

        # --- Draw background people (dark, moving) ---
        for person in bg_people:
            px = int(person['cx'] + person['vx'] * i) % width
            py = int(person['cy'] + person['vy'] * i) % height
            cv2.rectangle(bg, (px - person['w'] // 2, py - person['h'] // 2),
                          (px + person['w'] // 2, py + person['h'] // 2),
                          person['color'], -1)
            # Head
            cv2.circle(bg, (px, py - person['h'] // 2 - 10), 12,
                       (person['color'][0] + 30, person['color'][1] + 20,
                        person['color'][2] + 20), -1)

        # --- Draw the dog (warm brown, textured) ---
        dog_cx = int(dog_cx_start + dog_speed_x * i)
        dog_cy_actual = int(dog_cy + dog_speed_y * np.sin(i * 0.8))

        # Body with fur texture
        body_mask = np.zeros((height, width), dtype=np.uint8)
        cv2.ellipse(body_mask, (dog_cx, dog_cy_actual), (dog_rx, dog_ry),
                    0, 0, 360, 255, -1)
        # Head
        cv2.ellipse(body_mask, (dog_cx + dog_rx - 15, dog_cy_actual - 35),
                    (38, 32), -10, 0, 360, 255, -1)
        # Legs
        for lx_off in [-65, -25, 25, 65]:
            leg_phase = np.sin(i * 1.5 + lx_off * 0.05) * 10
            cv2.line(body_mask,
                     (dog_cx + lx_off, dog_cy_actual + dog_ry - 10),
                     (dog_cx + lx_off + int(leg_phase), dog_cy_actual + dog_ry + 55),
                     255, 12)
        # Tail
        tail_angle = 30 + 15 * np.sin(i * 2.0)
        tx = dog_cx - dog_rx + int(35 * np.cos(np.radians(180 + tail_angle)))
        ty = dog_cy_actual - 25 + int(35 * np.sin(np.radians(180 + tail_angle)))
        cv2.line(body_mask, (dog_cx - dog_rx + 10, dog_cy_actual - 25),
                 (tx, ty), 255, 8)

        # Fill dog region with warm brown + fur texture
        fur_texture = rng.randint(-12, 13, (height, width, 3), dtype=np.int16)
        dog_pixels = np.array(dog_color_body, dtype=np.int16) + fur_texture
        dog_pixels = np.clip(dog_pixels, 0, 255).astype(np.uint8)
        # Head slightly different shade
        head_mask = np.zeros((height, width), dtype=np.uint8)
        cv2.ellipse(head_mask, (dog_cx + dog_rx - 15, dog_cy_actual - 35),
                    (38, 32), -10, 0, 360, 255, -1)
        head_pixels = np.array(dog_color_head, dtype=np.int16) + fur_texture
        head_pixels = np.clip(head_pixels, 0, 255).astype(np.uint8)

        # Apply dog to background
        body_3ch = cv2.merge([body_mask, body_mask, body_mask])
        bg = np.where(body_3ch == 255, dog_pixels, bg)
        head_3ch = cv2.merge([head_mask, head_mask, head_mask])
        bg = np.where(head_3ch == 255, head_pixels, bg)

        # Slight camera shake
        shake_x = rng.randint(-2, 3)
        shake_y = rng.randint(-1, 2)
        M = np.float32([[1, 0, shake_x], [0, 1, shake_y]])
        bg = cv2.warpAffine(bg, M, (width, height), borderMode=cv2.BORDER_REFLECT)

        frames.append(bg)

        # Ground truth mask
        mask_gt = body_mask.copy()
        dog_masks_gt.append(mask_gt)

    dog_flow_gt = dog_speed_x
    return frames, dog_masks_gt, dog_flow_gt


# ---------------------------------------------------------------------------
# Metrics
# ---------------------------------------------------------------------------

def compute_optical_flow_metrics(frames, dog_masks_gt):
    """Compute optical flow and measure how much comes from the dog vs background.

    Returns dict with:
        - dog_flow_ratio: fraction of flow energy from dog region (higher = better)
        - bg_flow_ratio: fraction of flow energy from background (lower = better)
        - flow_magnitude_dog: average flow magnitude in dog region
        - flow_magnitude_bg: average flow magnitude in background
        - snr: signal-to-noise ratio (dog flow / bg flow)
    """
    grays = [cv2.cvtColor(f, cv2.COLOR_BGR2GRAY) for f in frames]

    total_dog_flow = 0.0
    total_bg_flow = 0.0
    dog_pixels = 0
    bg_pixels = 0
    flow_mags = []
    flow_angle_stds = []

    for i in range(len(grays) - 1):
        flow = cv2.calcOpticalFlowFarneback(
            grays[i], grays[i + 1], None,
            pyr_scale=0.5, levels=3, winsize=15,
            iterations=3, poly_n=5, poly_sigma=1.2, flags=0
        )
        mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])

        # Use ground truth mask to separate dog vs background flow
        mask = dog_masks_gt[i]
        dog_region = mask == 255
        bg_region = mask == 0

        np.mean(mag[dog_region]) if np.any(dog_region) else 0
        np.mean(mag[bg_region]) if np.any(bg_region) else 0

        total_dog_flow += np.sum(mag[dog_region])
        total_bg_flow += np.sum(mag[bg_region])
        dog_pixels += np.count_nonzero(dog_region)
        bg_pixels += np.count_nonzero(bg_region)

        flow_mags.append(np.mean(mag))
        flow_angle_stds.append(np.std(ang))

    avg_dog_flow = total_dog_flow / max(dog_pixels, 1)
    avg_bg_flow = total_bg_flow / max(bg_pixels, 1)
    total_flow = total_dog_flow + total_bg_flow

    snr = avg_dog_flow / max(avg_bg_flow, 0.001)

    # Gait scores (same as analyze_video_local)
    avg_magnitude = np.mean(flow_mags)
    mag_std = np.std(flow_mags) if len(flow_mags) > 1 else 0
    avg_angle_std = np.mean(flow_angle_stds)

    stride_score = _normalize(avg_magnitude, 0.5, 8.0, 65, 95)
    balance_score = _normalize(1.0 / (1.0 + mag_std), 0.3, 0.9, 65, 95)
    fluidity_score = _normalize(
        1.0 - abs(avg_angle_std - 1.0) / 2.0, 0.0, 1.0, 65, 95
    )
    gait_overall = stride_score * 0.4 + balance_score * 0.35 + fluidity_score * 0.25

    return {
        'dog_flow_ratio': total_dog_flow / max(total_flow, 1),
        'bg_flow_ratio': total_bg_flow / max(total_flow, 1),
        'flow_magnitude_dog': round(avg_dog_flow, 4),
        'flow_magnitude_bg': round(avg_bg_flow, 4),
        'snr': round(snr, 2),
        'stride_score': round(stride_score, 1),
        'balance_score': round(balance_score, 1),
        'fluidity_score': round(fluidity_score, 1),
        'gait_overall': round(gait_overall, 1),
        'avg_magnitude': round(avg_magnitude, 4),
    }


def compute_mask_iou(predicted_frames, gt_masks):
    """Compute IoU between preprocessing's implicit focus and ground truth dog masks.

    Uses variance of Laplacian as proxy: sharp regions = dog, blurred = background.
    """
    ious = []
    for pred_frame, gt_mask in zip(predicted_frames, gt_masks):
        gray = cv2.cvtColor(pred_frame, cv2.COLOR_BGR2GRAY)
        # Sharp regions (dog) will have high Laplacian variance
        lap = cv2.Laplacian(gray, cv2.CV_64F)
        lap_abs = np.abs(lap)
        # Threshold: above median = sharp (dog)
        threshold = np.median(lap_abs) + np.std(lap_abs) * 0.5
        sharp_mask = (lap_abs > threshold).astype(np.uint8) * 255

        # Morphological cleanup
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
        sharp_mask = cv2.morphologyEx(sharp_mask, cv2.MORPH_CLOSE, kernel)

        # IoU
        intersection = np.count_nonzero(np.bitwise_and(sharp_mask, gt_mask))
        union = np.count_nonzero(np.bitwise_or(sharp_mask, gt_mask))
        iou = intersection / max(union, 1)
        ious.append(iou)

    return round(np.mean(ious), 4)


# ---------------------------------------------------------------------------
# Main Benchmark
# ---------------------------------------------------------------------------

def run_benchmark():
    print("=" * 70)
    print("  ShowDog 歩様解析 精度ベンチマーク")
    print("  犬フォーカス前処理 改善前 vs 改善後")
    print("=" * 70)
    print()

    # Generate test scenarios
    scenarios = [
        {"name": "標準シーン（背景動き少）", "num_frames": 5, "seed": 42},
        {"name": "激しい背景（人多数）", "num_frames": 5, "seed": 123},
        {"name": "長いシーケンス", "num_frames": 8, "seed": 77},
    ]

    all_results = []

    for scenario in scenarios:
        print(f"━━━ {scenario['name']} ━━━")
        print(f"  フレーム数: {scenario['num_frames']}")

        frames, gt_masks, gt_flow = generate_test_frames(
            num_frames=scenario['num_frames'],
            seed=scenario['seed']
        )

        # --- BEFORE: No preprocessing ---
        t0 = time.time()
        metrics_before = compute_optical_flow_metrics(frames, gt_masks)
        time_before = time.time() - t0

        # --- AFTER: Dog focus preprocessing ---
        t0 = time.time()
        processed_frames = preprocess_dog_focus(frames)
        preprocess_time = time.time() - t0

        t0 = time.time()
        metrics_after = compute_optical_flow_metrics(processed_frames, gt_masks)
        time_after = time.time() - t0

        # Mask quality (IoU)
        iou = compute_mask_iou(processed_frames, gt_masks)

        # Compute improvements
        snr_improvement = ((metrics_after['snr'] - metrics_before['snr'])
                           / max(metrics_before['snr'], 0.01) * 100)
        dog_ratio_improvement = ((metrics_after['dog_flow_ratio'] - metrics_before['dog_flow_ratio'])
                                 / max(metrics_before['dog_flow_ratio'], 0.01) * 100)
        gait_improvement = ((metrics_after['gait_overall'] - metrics_before['gait_overall'])
                            / max(metrics_before['gait_overall'], 0.01) * 100)

        print()
        print("  ┌─────────────────────┬──────────┬──────────┬──────────┐")
        print("  │ 指標                │ 改善前   │ 改善後   │ 変化率   │")
        print("  ├─────────────────────┼──────────┼──────────┼──────────┤")
        print(f"  │ SNR (信号/ノイズ)   │ {metrics_before['snr']:>7.2f}  │ {metrics_after['snr']:>7.2f}  │ {snr_improvement:>+6.1f}%  │")
        print(f"  │ 犬フロー割合        │ {metrics_before['dog_flow_ratio']:>7.1%} │ {metrics_after['dog_flow_ratio']:>7.1%} │ {dog_ratio_improvement:>+6.1f}%  │")
        print(f"  │ 背景フロー割合      │ {metrics_before['bg_flow_ratio']:>7.1%} │ {metrics_after['bg_flow_ratio']:>7.1%} │          │")
        print(f"  │ 犬フロー強度        │ {metrics_before['flow_magnitude_dog']:>7.4f}  │ {metrics_after['flow_magnitude_dog']:>7.4f}  │          │")
        print(f"  │ 背景フロー強度      │ {metrics_before['flow_magnitude_bg']:>7.4f}  │ {metrics_after['flow_magnitude_bg']:>7.4f}  │          │")
        print("  ├─────────────────────┼──────────┼──────────┼──────────┤")
        print(f"  │ ストライドスコア    │ {metrics_before['stride_score']:>7.1f}  │ {metrics_after['stride_score']:>7.1f}  │          │")
        print(f"  │ バランススコア      │ {metrics_before['balance_score']:>7.1f}  │ {metrics_after['balance_score']:>7.1f}  │          │")
        print(f"  │ 流動性スコア        │ {metrics_before['fluidity_score']:>7.1f}  │ {metrics_after['fluidity_score']:>7.1f}  │          │")
        print(f"  │ 歩様総合スコア      │ {metrics_before['gait_overall']:>7.1f}  │ {metrics_after['gait_overall']:>7.1f}  │ {gait_improvement:>+6.1f}%  │")
        print("  ├─────────────────────┼──────────┼──────────┼──────────┤")
        print(f"  │ マスク精度 (IoU)    │    N/A   │ {iou:>7.4f}  │          │")
        print(f"  │ 前処理時間          │    N/A   │ {preprocess_time:>5.3f}秒  │          │")
        print(f"  │ 解析時間            │ {time_before:>5.3f}秒  │ {time_after:>5.3f}秒  │          │")
        print("  └─────────────────────┴──────────┴──────────┴──────────┘")
        print()

        all_results.append({
            'scenario': scenario['name'],
            'snr_before': metrics_before['snr'],
            'snr_after': metrics_after['snr'],
            'snr_improvement_pct': round(snr_improvement, 1),
            'dog_ratio_before': round(metrics_before['dog_flow_ratio'], 4),
            'dog_ratio_after': round(metrics_after['dog_flow_ratio'], 4),
            'gait_before': metrics_before['gait_overall'],
            'gait_after': metrics_after['gait_overall'],
            'gait_improvement_pct': round(gait_improvement, 1),
            'mask_iou': iou,
            'preprocess_time_sec': round(preprocess_time, 3),
        })

    # --- Summary ---
    print("=" * 70)
    print("  総合結果サマリー")
    print("=" * 70)
    avg_snr_imp = np.mean([r['snr_improvement_pct'] for r in all_results])
    avg_gait_imp = np.mean([r['gait_improvement_pct'] for r in all_results])
    avg_iou = np.mean([r['mask_iou'] for r in all_results])
    avg_preprocess = np.mean([r['preprocess_time_sec'] for r in all_results])

    print(f"  平均SNR向上率:       {avg_snr_imp:>+.1f}%")
    print(f"  平均歩様スコア向上率: {avg_gait_imp:>+.1f}%")
    print(f"  平均マスク精度(IoU): {avg_iou:.4f}")
    print(f"  平均前処理時間:      {avg_preprocess:.3f}秒")
    print()

    # Save results as JSON (convert numpy types to native Python)
    def _to_native(obj):
        if isinstance(obj, (np.integer,)):
            return int(obj)
        if isinstance(obj, (np.floating,)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return obj

    output_path = '/home/user/showdog-app/benchmark_results.json'
    clean_results = json.loads(json.dumps(all_results, default=_to_native))
    with open(output_path, 'w') as f:
        json.dump({
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'scenarios': clean_results,
            'summary': {
                'avg_snr_improvement_pct': float(round(avg_snr_imp, 1)),
                'avg_gait_improvement_pct': float(round(avg_gait_imp, 1)),
                'avg_mask_iou': float(round(avg_iou, 4)),
                'avg_preprocess_time_sec': float(round(avg_preprocess, 3)),
            }
        }, f, indent=2, ensure_ascii=False)
    print(f"  結果をJSONに保存: {output_path}")
    print()

    return all_results


if __name__ == '__main__':
    run_benchmark()
