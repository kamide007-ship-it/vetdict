"""
24時間自動循環解析エンジン — ShowDog Data Cycle

すべてのデータに関わることを24時間に1回自動で循環し、解析、データとして蓄積。
アルゴリズムに反映する。

Architecture:
  1. Collect: 過去24時間の全解析結果を収集
  2. Aggregate: 犬種別・スコア別に統計集約
  3. Calibrate: FCI基準とのギャップを検出
  4. Update: アルゴリズムパラメータを自動調整
  5. Store: 結果をデータとして蓄積

Data Sources:
  - 写真解析: FCIデータ（ideal_structure/coat/gait）に基づく
  - 動画解析: エビデンスとデータに基づく（reference_dataset）
  - 疾患: エビデンスに基づく（health_checker epidemiological data）
"""

import json
import logging
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

# Persistent storage for cycle results
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
CYCLE_DATA_DIR = Path(os.environ.get('SHOWDOG_DATA_DIR', str(_PROJECT_ROOT / 'data')))
CYCLE_STATE_PATH = CYCLE_DATA_DIR / 'cycle_state.json'
CYCLE_HISTORY_PATH = CYCLE_DATA_DIR / 'cycle_history.jsonl'
BREED_CALIBRATION_PATH = CYCLE_DATA_DIR / 'breed_calibration.json'
CYCLE_INTERVAL_HOURS = 24


# ---------------------------------------------------------------------------
# State management
# ---------------------------------------------------------------------------

def _ensure_data_dir():
    CYCLE_DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_cycle_state() -> Dict[str, Any]:
    """Load the current cycle state."""
    _ensure_data_dir()
    if CYCLE_STATE_PATH.exists():
        try:
            return json.loads(CYCLE_STATE_PATH.read_text(encoding='utf-8'))
        except Exception as e:
            logger.warning(f"Cycle state file corrupted, resetting: {e}")
    return {
        'last_cycle_ts': 0,
        'total_cycles': 0,
        'total_analyses_processed': 0,
        'breed_stats': {},
    }


def save_cycle_state(state: Dict[str, Any]):
    _ensure_data_dir()
    tmp = str(CYCLE_STATE_PATH) + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    os.replace(tmp, str(CYCLE_STATE_PATH))


def load_breed_calibration() -> Dict[str, Any]:
    """Load breed-specific calibration parameters.

    These are adjustments learned from accumulated data that
    fine-tune the scoring algorithms per breed.
    """
    _ensure_data_dir()
    if BREED_CALIBRATION_PATH.exists():
        try:
            return json.loads(BREED_CALIBRATION_PATH.read_text(encoding='utf-8'))
        except Exception as e:
            logger.warning(f"Breed calibration file corrupted, using defaults: {e}")
    return {}


def save_breed_calibration(cal: Dict[str, Any]):
    _ensure_data_dir()
    tmp = str(BREED_CALIBRATION_PATH) + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(cal, f, ensure_ascii=False, indent=2)
    os.replace(tmp, str(BREED_CALIBRATION_PATH))


def append_cycle_log(entry: Dict[str, Any]):
    """Append a cycle result to the history log."""
    _ensure_data_dir()
    line = json.dumps(entry, ensure_ascii=False)
    with open(CYCLE_HISTORY_PATH, 'a', encoding='utf-8') as f:
        f.write(line + '\n')


# ---------------------------------------------------------------------------
# Data Collection (Step 1)
# ---------------------------------------------------------------------------

def collect_recent_analyses(hours: int = 24) -> List[Dict[str, Any]]:
    """Collect all analyses from the past N hours from the database."""
    try:
        from api.database import get_db
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT a.*, d.breed_id, d.name as dog_name
            FROM analyses a
            JOIN dogs d ON a.dog_id = d.id
            WHERE a.created_at >= datetime('now', ?)
            ORDER BY a.created_at DESC
        ''', (f'-{hours} hours',))
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except Exception as e:
        logger.warning(f"Failed to collect recent analyses: {e}")
        return []


# ---------------------------------------------------------------------------
# Statistical Aggregation (Step 2)
# ---------------------------------------------------------------------------

def aggregate_by_breed(analyses: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """Aggregate analysis scores by breed.

    Returns dict mapping breed_id to statistical summary:
      count, mean/std/min/max for each score component.
    """
    breed_data = {}
    for a in analyses:
        breed = a.get('breed_id', 'unknown')
        if breed not in breed_data:
            breed_data[breed] = {
                'count': 0,
                'overall': [], 'structure': [], 'coat': [],
                'gait': [], 'temperament': [],
            }
        bd = breed_data[breed]
        bd['count'] += 1

        if a.get('overall_score') is not None:
            bd['overall'].append(float(a['overall_score']))
        if a.get('structure_score') is not None:
            bd['structure'].append(float(a['structure_score']))
        if a.get('coat_score') is not None:
            bd['coat'].append(float(a['coat_score']))
        if a.get('gait_score') is not None:
            bd['gait'].append(float(a['gait_score']))
        if a.get('temperament_score') is not None:
            bd['temperament'].append(float(a['temperament_score']))

    # Compute statistics
    import numpy as np
    result = {}
    for breed, bd in breed_data.items():
        stats = {'count': bd['count']}
        for key in ('overall', 'structure', 'coat', 'gait', 'temperament'):
            vals = bd[key]
            if vals:
                stats[key] = {
                    'mean': float(np.mean(vals)),
                    'std': float(np.std(vals)),
                    'min': float(np.min(vals)),
                    'max': float(np.max(vals)),
                    'n': len(vals),
                }
            else:
                stats[key] = None
        result[breed] = stats
    return result


# ---------------------------------------------------------------------------
# FCI Calibration (Step 3) — 写真解析はFCIデータに基づく
# ---------------------------------------------------------------------------

def calibrate_against_fci(breed_stats: Dict[str, Dict], breed_db: Dict) -> Dict[str, Dict]:
    """Compare accumulated scores against FCI breed standards.

    For each breed, compute calibration adjustments based on:
    - Expected score distribution per FCI grading tier
    - Breed-specific ideal structure/coat/gait descriptions
    - Historical score drift detection

    Args:
        breed_stats: aggregated statistics from aggregate_by_breed()
        breed_db: BREED_DATA from api.breeds

    Returns:
        dict mapping breed_id to calibration parameters
    """

    calibration = {}

    for breed_id, stats in breed_stats.items():
        if stats['count'] < 3:
            continue  # Need minimum data to calibrate

        cal = {
            'breed_id': breed_id,
            'sample_size': stats['count'],
            'adjustments': {},
            'updated_at': datetime.now(timezone.utc).isoformat(),
        }

        # Get breed FCI data if available
        breed_info = breed_db.get(breed_id, {})

        for component in ('structure', 'coat', 'gait', 'temperament'):
            comp_stats = stats.get(component)
            if comp_stats is None or comp_stats['n'] < 2:
                continue

            mean = comp_stats['mean']
            std = comp_stats['std']

            # FCI calibration: scores should follow expected distribution
            # FCI "Excellent" = 90-100, "Very Good" = 80-89, "Good" = 70-79
            # If mean is consistently too high or too low, apply correction
            expected_mean = 80.0  # FCI "Very Good" is the expected average
            drift = mean - expected_mean

            # Only apply correction if drift is significant (>5 points)
            if abs(drift) > 5.0:
                # Correction factor: reduce scores if too high, boost if too low
                # But limit to ±10% to avoid over-correction
                correction = -drift * 0.3  # 30% of drift
                correction = max(-8.0, min(8.0, correction))
                cal['adjustments'][component] = {
                    'offset': round(correction, 2),
                    'reason': f'FCI基準との乖離補正 (平均{mean:.1f} → 目標{expected_mean:.1f})',
                }

            # Breed-specific: if ideal description exists, weight adjustment
            if component == 'structure' and breed_info.get('ideal_structure') and std > 15:
                cal['adjustments'].setdefault(component, {})
                cal['adjustments'][component]['variance_flag'] = True
                cal['adjustments'][component]['variance_note'] = (
                    f'スコアのバラつきが大きい (σ={std:.1f})'
                )

            if component == 'coat' and breed_info.get('ideal_coat') and std > 15:
                cal['adjustments'].setdefault(component, {})
                cal['adjustments'][component]['variance_flag'] = True

            if component == 'gait' and breed_info.get('ideal_gait') and std > 15:
                cal['adjustments'].setdefault(component, {})
                cal['adjustments'][component]['variance_flag'] = True

        if cal['adjustments']:
            calibration[breed_id] = cal

    return calibration


# ---------------------------------------------------------------------------
# Algorithm Parameter Update (Step 4) — アルゴリズムに反映
# ---------------------------------------------------------------------------

def apply_calibration_to_analysis(breed_id: str, scores: Dict[str, float]) -> Dict[str, float]:
    """Apply breed-specific calibration offsets to analysis scores.

    Called by the analysis pipeline to adjust raw scores based on
    accumulated data and FCI calibration.

    Args:
        breed_id: the breed identifier
        scores: dict of component → raw score

    Returns:
        adjusted scores dict
    """
    calibration = load_breed_calibration()
    breed_cal = calibration.get(breed_id)
    if not breed_cal:
        return scores

    adjusted = dict(scores)
    adjustments = breed_cal.get('adjustments', {})

    for component, adj in adjustments.items():
        if component in adjusted and isinstance(adj, dict):
            offset = adj.get('offset', 0)
            if offset != 0:
                raw = adjusted[component]
                adjusted[component] = max(0, min(100, raw + offset))

    return adjusted


def get_breed_fci_params(breed_id: str, breed_data: Dict) -> Dict[str, Any]:
    """Extract FCI-based analysis parameters for a breed.

    写真解析はFCIのデータに基づく。
    Returns breed-specific parameters that inform the analysis algorithms.
    """
    info = breed_data.get(breed_id, {})
    params = {}

    # Extract structural parameters from FCI description
    ideal_structure = info.get('ideal_structure', '')
    if '正方形' in ideal_structure or 'スクエア' in ideal_structure:
        params['ideal_ratio'] = 1.0  # Square proportions
    elif '長め' in ideal_structure or '長い体' in ideal_structure:
        params['ideal_ratio'] = 1.6  # Longer body
    elif '短い' in ideal_structure:
        params['ideal_ratio'] = 1.1  # Compact
    else:
        params['ideal_ratio'] = 1.3  # Default moderate

    # Weight class affects expected edge density
    if '大型' in ideal_structure or 'がっしり' in ideal_structure or '筋肉質' in ideal_structure:
        params['body_mass'] = 'large'
        params['edge_density_target'] = 0.10
    elif '華奢' in ideal_structure or '小型' in ideal_structure or '細い' in ideal_structure:
        params['body_mass'] = 'small'
        params['edge_density_target'] = 0.14
    else:
        params['body_mass'] = 'medium'
        params['edge_density_target'] = 0.12

    # Coat type parameters from FCI description
    ideal_coat = info.get('ideal_coat', '')
    if '長毛' in ideal_coat or '豊富' in ideal_coat or 'ロング' in ideal_coat:
        params['coat_type'] = 'long'
        params['texture_expectation'] = 'high'
    elif '短毛' in ideal_coat or '短く' in ideal_coat or '密着' in ideal_coat:
        params['coat_type'] = 'short'
        params['texture_expectation'] = 'low'
    elif 'ワイヤー' in ideal_coat or '粗い' in ideal_coat:
        params['coat_type'] = 'wire'
        params['texture_expectation'] = 'medium'
    elif 'カーリー' in ideal_coat or '巻き毛' in ideal_coat:
        params['coat_type'] = 'curly'
        params['texture_expectation'] = 'high'
    else:
        params['coat_type'] = 'medium'
        params['texture_expectation'] = 'medium'

    # Gait type from FCI description
    ideal_gait = info.get('ideal_gait', '')
    if '力強い' in ideal_gait or '推進力' in ideal_gait:
        params['gait_type'] = 'powerful'
        params['expected_stride'] = 'long'
    elif '軽快' in ideal_gait or '優雅' in ideal_gait:
        params['gait_type'] = 'elegant'
        params['expected_stride'] = 'moderate'
    elif '安定' in ideal_gait or '堅実' in ideal_gait:
        params['gait_type'] = 'steady'
        params['expected_stride'] = 'moderate'
    else:
        params['gait_type'] = 'balanced'
        params['expected_stride'] = 'moderate'

    # Hereditary disease list
    params['hereditary_diseases'] = info.get('hereditary_diseases', [])

    # FCI number for reference dataset lookup
    params['fci_number'] = info.get('fci_number')
    params['breed_name'] = info.get('name', '')
    params['breed_name_en'] = info.get('name_en', '')

    return params


# ---------------------------------------------------------------------------
# Evidence-based scoring — 動画解析はエビデンスとデータに基づく
# ---------------------------------------------------------------------------

def get_evidence_based_gait_params(breed_id: str) -> Dict[str, Any]:
    """Get evidence-based gait analysis parameters.

    動画解析はエビデンスとデータに基づく。
    Uses reference_dataset FCI show report data and accumulated analysis history.
    """
    try:
        from api.reference_dataset import REFERENCE_CASES
    except ImportError:
        REFERENCE_CASES = []

    # Find reference cases for this breed
    breed_refs = []
    for case in REFERENCE_CASES:
        if case.get('breed_id') == breed_id:
            breed_refs.append(case)

    params = {
        'has_reference_data': len(breed_refs) > 0,
        'reference_count': len(breed_refs),
    }

    if breed_refs:
        # Extract gait score expectations from reference cases
        gait_scores = []
        for ref in breed_refs:
            gait = ref.get('axis_scores', {}).get('gait')
            if gait is not None:
                gait_scores.append(float(gait))

        if gait_scores:
            import numpy as np
            params['expected_gait_mean'] = float(np.mean(gait_scores))
            params['expected_gait_std'] = float(np.std(gait_scores))
            params['expected_gait_range'] = (
                float(np.min(gait_scores)),
                float(np.max(gait_scores))
            )

    # Also use accumulated calibration data
    calibration = load_breed_calibration()
    breed_cal = calibration.get(breed_id)
    if breed_cal:
        gait_adj = breed_cal.get('adjustments', {}).get('gait', {})
        if gait_adj:
            params['calibration_offset'] = gait_adj.get('offset', 0)

    return params


def get_evidence_based_disease_params(breed_id: str) -> Dict[str, Any]:
    """Get evidence-based disease risk parameters.

    疾患はエビデンスに基づく。
    Combines breed-specific hereditary disease data with epidemiological evidence.
    """
    try:
        from api.breeds import BREED_DATA
        breed_info = BREED_DATA.get(breed_id, {})
    except ImportError:
        breed_info = {}

    diseases = breed_info.get('hereditary_diseases', [])

    # Build evidence-based risk profile
    risk_profile = {
        'breed_id': breed_id,
        'hereditary_diseases': diseases,
        'total_known_risks': len(diseases),
    }

    # Categorize by system
    orthopedic = []
    ophthalmologic = []
    cardiac = []
    neurological = []
    dermatological = []
    other = []

    orthopedic_kw = ['股関節', '膝蓋骨', '肘', '骨', '関節', 'レッグ', 'ペルテス', '椎間板']
    eye_kw = ['網膜', '白内障', '緑内障', '眼', 'PRA', '角膜']
    cardiac_kw = ['心臓', '心', '弁', '動脈']
    neuro_kw = ['脳', '神経', 'てんかん', '脊髄', '変性']
    skin_kw = ['皮膚', '脂腺', 'アレルギー', '皮膚炎', 'アトピー']

    for d in diseases:
        categorized = False
        for kw in orthopedic_kw:
            if kw in d:
                orthopedic.append(d)
                categorized = True
                break
        if categorized:
            continue
        for kw in eye_kw:
            if kw in d:
                ophthalmologic.append(d)
                categorized = True
                break
        if categorized:
            continue
        for kw in cardiac_kw:
            if kw in d:
                cardiac.append(d)
                categorized = True
                break
        if categorized:
            continue
        for kw in neuro_kw:
            if kw in d:
                neurological.append(d)
                categorized = True
                break
        if categorized:
            continue
        for kw in skin_kw:
            if kw in d:
                dermatological.append(d)
                categorized = True
                break
        if not categorized:
            other.append(d)

    risk_profile['by_system'] = {
        'orthopedic': orthopedic,
        'ophthalmologic': ophthalmologic,
        'cardiac': cardiac,
        'neurological': neurological,
        'dermatological': dermatological,
        'other': other,
    }

    # Risk level based on number and severity
    total = len(diseases)
    if total >= 6:
        risk_profile['overall_risk_level'] = 'high'
    elif total >= 3:
        risk_profile['overall_risk_level'] = 'moderate'
    else:
        risk_profile['overall_risk_level'] = 'low'

    return risk_profile


# ---------------------------------------------------------------------------
# Main Cycle Execution (Step 5) — 24時間循環
# ---------------------------------------------------------------------------

def should_run_cycle() -> bool:
    """Check if enough time has passed since the last cycle."""
    state = load_cycle_state()
    last_ts = state.get('last_cycle_ts', 0)
    elapsed_hours = (time.time() - last_ts) / 3600
    return elapsed_hours >= CYCLE_INTERVAL_HOURS


def run_cycle(force: bool = False) -> Dict[str, Any]:
    """Execute the full 24-hour data cycle.

    1. Collect recent analyses
    2. Aggregate by breed
    3. Calibrate against FCI standards
    4. Update breed calibration parameters
    5. Log results

    Returns cycle result summary.
    """
    state = load_cycle_state()

    if not force and not should_run_cycle():
        return {
            'status': 'skipped',
            'reason': f'Last cycle was less than {CYCLE_INTERVAL_HOURS}h ago',
            'last_cycle': state.get('last_cycle_ts', 0),
        }

    logger.info("Starting 24-hour data cycle...")
    cycle_start = time.time()
    now_iso = datetime.now(timezone.utc).isoformat()

    # Step 1: Collect
    analyses = collect_recent_analyses(hours=CYCLE_INTERVAL_HOURS)
    logger.info(f"Collected {len(analyses)} analyses from past {CYCLE_INTERVAL_HOURS}h")

    # Step 2: Aggregate
    breed_stats = aggregate_by_breed(analyses)
    logger.info(f"Aggregated stats for {len(breed_stats)} breeds")

    # Step 3: Calibrate against FCI
    try:
        from api.breeds import BREED_DATA
    except ImportError:
        BREED_DATA = {}

    calibration = calibrate_against_fci(breed_stats, BREED_DATA)
    logger.info(f"Generated calibration for {len(calibration)} breeds")

    # Step 4: Update persistent calibration
    existing_cal = load_breed_calibration()
    # Merge: new calibrations override old ones, keep breeds not in current cycle
    for breed_id, cal in calibration.items():
        existing_cal[breed_id] = cal
    save_breed_calibration(existing_cal)

    # Step 5: Update state and log
    state['last_cycle_ts'] = time.time()
    state['total_cycles'] = state.get('total_cycles', 0) + 1
    state['total_analyses_processed'] = (
        state.get('total_analyses_processed', 0) + len(analyses)
    )
    state['breed_stats'] = breed_stats
    save_cycle_state(state)

    result = {
        'status': 'completed',
        'timestamp': now_iso,
        'cycle_number': state['total_cycles'],
        'analyses_processed': len(analyses),
        'breeds_analyzed': len(breed_stats),
        'calibrations_updated': len(calibration),
        'duration_seconds': round(time.time() - cycle_start, 2),
    }

    append_cycle_log(result)
    logger.info(f"Cycle #{state['total_cycles']} completed: {result}")

    return result


def try_auto_cycle():
    """Attempt to run the auto-cycle if due. Safe to call on every request."""
    try:
        if should_run_cycle():
            return run_cycle()
    except Exception as e:
        logger.warning(f"Auto-cycle failed: {e}")
    return None
