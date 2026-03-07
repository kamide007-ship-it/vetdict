"""
Centralized breed coefficient registry for the ShowDog analysis platform.

Derives structured analysis coefficients from FCI text descriptions in breeds.py
and provides a unified lookup API for all analysis modules.

This module bridges the gap between:
  - breeds.py: 360 breeds with FCI text descriptions (ideal_structure, ideal_coat, ideal_gait)
  - local_analysis.py: Algorithm coefficients mapped to breed groups (~30 explicit mappings)
  - scoring.py: Breed sensitivity profiles (~35 explicit mappings)

For breeds not explicitly mapped, coefficients are derived from the Japanese FCI
text descriptions using keyword matching against known breed characteristics.
"""

import logging
from typing import Dict, Optional

from api.breeds import BREED_DATA

logger = logging.getLogger(__name__)

# =============================================================================
# DERIVATION KEYWORD TABLES (FCI日本語テキスト → 構造化係数)
# =============================================================================
# These map Japanese FCI description keywords to structured coefficient groups.
# Priority order: first match wins within each category.

# --- Angle Group Derivation ---
# Maps ideal_structure + ideal_gait keywords → BREED_ANGLE_STANDARDS group

_ANGLE_GROUP_KEYWORDS: Dict[str, list] = {
    "herding": [
        "牧羊", "牧畜", "シェパード", "コリー", "シェルティ",
        "ヒーラー", "牧場", "ハーディング",
    ],
    "sporting": [
        "レトリバー", "セッター", "ポインター", "スパニエル",
        "鳥猟", "回収", "フラッシング", "水猟",
    ],
    "working": [
        "番犬", "護衛", "警備", "マスティフ", "ロットワイラー",
        "ドーベルマン", "ボクサー", "グレートデーン",
        "救助", "そり犬", "作業",
    ],
    "toy": [
        "愛玩", "コンパニオン", "小型", "トイ",
        "膝", "抱っこ",
    ],
    "sighthound": [
        "視覚ハウンド", "サイトハウンド", "グレイハウンド",
        "ウィペット", "サルーキ", "ボルゾイ", "アフガン",
        "疾走", "スプリント",
    ],
    "brachycephalic": [
        "短頭", "ブルドッグ", "パグ", "ペキニーズ",
        "鼻は短い", "短い鼻", "バット型",
    ],
    "spitz": [
        "スピッツ", "巻き尾", "直立耳", "北方",
        "柴", "秋田", "ハスキー", "マラミュート",
        "ポメラニアン", "サモエド", "チャウチャウ",
    ],
}

# --- Coat Type Derivation ---
_COAT_TYPE_KEYWORDS: Dict[str, list] = {
    "long": [
        "長毛", "豊かな被毛", "絹糸状",
        "シルキー", "流れるような被毛",
    ],
    "curly": [
        "カーリー", "巻き毛", "コーデッド", "ウーリー",
    ],
    "wire": [
        "ワイヤー", "粗毛", "剛毛", "硬い被毛",
    ],
    "double": [
        "ダブルコート", "二重被毛", "密な下毛", "豊富な下毛",
    ],
    "short": [
        "短毛", "短く", "スムース", "滑らか", "体に密着",
    ],
}

# --- Texture Expectation Derivation ---
_TEXTURE_KEYWORDS: Dict[str, list] = {
    "high": [
        "カーリー", "巻き毛", "豊富な", "密度が高い",
        "長毛", "ワイヤー",
    ],
    "medium": [
        "ダブルコート", "二重", "中程度", "下毛",
    ],
    "low": [
        "短く", "スムース", "滑らか", "密着", "光沢",
    ],
}

# --- Body Mass Derivation ---
_BODY_MASS_KEYWORDS: Dict[str, list] = {
    "large": [
        "大型", "がっしり", "筋肉質", "力強い", "重量",
        "マスティフ", "グレートデーン", "大きな",
    ],
    "small": [
        "小型", "トイ", "コンパクト", "華奢", "軽量",
        "チワワ", "膝",
    ],
    # "medium" is the default
}

# --- Gait Type Derivation ---
_GAIT_TYPE_KEYWORDS: Dict[str, list] = {
    "powerful": [
        "力強", "パワフル", "推進力", "ドライブ",
    ],
    "elegant": [
        "優雅", "エレガント", "軽快", "スプリング",
        "流れるような", "なめらか",
    ],
    "steady": [
        "安定", "直線的", "堅実", "確実",
    ],
    # "balanced" is the default
}


def _match_keywords(text: str, keyword_map: Dict[str, list]) -> Optional[str]:
    """Match text against keyword groups, return first matching group or None.

    Handles Japanese negation: skips matches where the keyword is immediately
    followed by negation particles (がない, はない, のない, でない).
    """
    _NEG_SUFFIXES = ("がない", "はない", "のない", "でない", "なく", "ではなく", "がなく")
    for group, keywords in keyword_map.items():
        for kw in keywords:
            idx = text.find(kw)
            if idx == -1:
                continue
            # Check for negation immediately after the keyword
            after = text[idx + len(kw):]
            if any(after.startswith(neg) for neg in _NEG_SUFFIXES):
                continue
            return group
    return None


# =============================================================================
# BREED COEFFICIENT DERIVATION
# =============================================================================

def derive_angle_group(breed_entry: dict) -> str:
    """Derive angle standard group from FCI text descriptions.

    Checks ideal_structure, ideal_gait, and name fields.
    Returns one of: herding, sporting, working, toy, sighthound,
    brachycephalic, spitz, or 'default'.
    """
    texts = " ".join([
        breed_entry.get("ideal_structure", ""),
        breed_entry.get("ideal_gait", ""),
        breed_entry.get("name", ""),
        breed_entry.get("name_en", ""),
    ])
    return _match_keywords(texts, _ANGLE_GROUP_KEYWORDS) or "default"


def derive_coat_type(breed_entry: dict) -> str:
    """Derive coat type from ideal_coat description.

    Returns one of: long, curly, wire, double, short, or 'medium'.
    """
    text = breed_entry.get("ideal_coat", "")
    return _match_keywords(text, _COAT_TYPE_KEYWORDS) or "medium"


def derive_texture_expectation(breed_entry: dict) -> str:
    """Derive texture expectation from ideal_coat description.

    Returns one of: high, medium, low.
    """
    text = breed_entry.get("ideal_coat", "")
    return _match_keywords(text, _TEXTURE_KEYWORDS) or "medium"


def derive_body_mass(breed_entry: dict) -> str:
    """Derive body mass category from ideal_structure description.

    Returns one of: large, medium, small.
    """
    text = breed_entry.get("ideal_structure", "")
    return _match_keywords(text, _BODY_MASS_KEYWORDS) or "medium"


def derive_gait_type(breed_entry: dict) -> str:
    """Derive gait type from ideal_gait description.

    Returns one of: powerful, elegant, steady, balanced.
    """
    text = breed_entry.get("ideal_gait", "")
    return _match_keywords(text, _GAIT_TYPE_KEYWORDS) or "balanced"


def derive_ideal_ratio(breed_entry: dict) -> float:
    """Derive ideal body ratio from structure description.

    Looks for ratio hints like '体高と体長がほぼ等しく' (square)
    or '長めの体型' (elongated).
    Returns a float ratio (body_length / body_height).
    """
    text = breed_entry.get("ideal_structure", "")

    # Square breeds (~1.0 ratio)
    if any(kw in text for kw in ["正方形", "等しく", "スクエア"]):
        return 1.10

    # Elongated breeds
    if any(kw in text for kw in ["長め", "やや長", "長い体"]):
        return 1.40

    # Compact breeds
    if any(kw in text for kw in ["コンパクト", "短い体"]):
        return 1.20

    # Default moderate ratio
    return 1.30


# =============================================================================
# COEFFICIENT BUNDLE
# =============================================================================

def get_breed_coefficients(breed_id: str) -> Dict:
    """Get the full coefficient bundle for a breed.

    Combines explicit mappings (from local_analysis.py / scoring.py)
    with derived values from FCI text descriptions.

    Args:
        breed_id: Breed identifier (e.g. '122_labrador_retriever')

    Returns:
        Dictionary with all derived coefficients:
        - angle_group: str
        - coat_type: str
        - texture_expectation: str
        - body_mass: str
        - gait_type: str
        - ideal_ratio: float
        - source: 'explicit' | 'derived' | 'default'
    """
    from api.local_analysis import BREED_ANGLE_GROUP_MAP

    breed_entry = BREED_DATA.get(breed_id, {})

    # Check if breed has explicit mapping
    explicit_group = BREED_ANGLE_GROUP_MAP.get(breed_id)

    if explicit_group:
        angle_group = explicit_group
        source = "explicit"
    elif breed_entry:
        angle_group = derive_angle_group(breed_entry)
        source = "derived" if angle_group != "default" else "default"
    else:
        angle_group = "default"
        source = "default"

    coat_type = derive_coat_type(breed_entry) if breed_entry else "medium"
    texture = derive_texture_expectation(breed_entry) if breed_entry else "medium"
    body_mass = derive_body_mass(breed_entry) if breed_entry else "medium"
    gait_type = derive_gait_type(breed_entry) if breed_entry else "balanced"
    ideal_ratio = derive_ideal_ratio(breed_entry) if breed_entry else 1.30

    return {
        "breed_id": breed_id,
        "angle_group": angle_group,
        "coat_type": coat_type,
        "texture_expectation": texture,
        "body_mass": body_mass,
        "gait_type": gait_type,
        "ideal_ratio": ideal_ratio,
        "source": source,
    }


# =============================================================================
# COVERAGE REPORT
# =============================================================================

def compute_coverage_report() -> Dict:
    """Compute coefficient coverage statistics across all 360 breeds.

    Returns:
        Dictionary with:
        - total_breeds: int
        - explicit_count: int (breeds with explicit angle group mapping)
        - derived_count: int (breeds with angle group derived from FCI text)
        - default_count: int (breeds falling back to 'default')
        - angle_group_distribution: Dict[str, int]
        - coat_type_distribution: Dict[str, int]
        - body_mass_distribution: Dict[str, int]
        - gait_type_distribution: Dict[str, int]
    """
    from api.local_analysis import BREED_ANGLE_GROUP_MAP

    total = len(BREED_DATA)
    explicit = 0
    derived = 0
    default = 0

    angle_dist: Dict[str, int] = {}
    coat_dist: Dict[str, int] = {}
    mass_dist: Dict[str, int] = {}
    gait_dist: Dict[str, int] = {}

    for breed_id in BREED_DATA:
        coeffs = get_breed_coefficients(breed_id)

        if coeffs["source"] == "explicit":
            explicit += 1
        elif coeffs["source"] == "derived":
            derived += 1
        else:
            default += 1

        angle_dist[coeffs["angle_group"]] = angle_dist.get(coeffs["angle_group"], 0) + 1
        coat_dist[coeffs["coat_type"]] = coat_dist.get(coeffs["coat_type"], 0) + 1
        mass_dist[coeffs["body_mass"]] = mass_dist.get(coeffs["body_mass"], 0) + 1
        gait_dist[coeffs["gait_type"]] = gait_dist.get(coeffs["gait_type"], 0) + 1

    return {
        "total_breeds": total,
        "explicit_count": explicit,
        "derived_count": derived,
        "default_count": default,
        "explicit_pct": round(explicit / max(total, 1) * 100, 1),
        "derived_pct": round(derived / max(total, 1) * 100, 1),
        "default_pct": round(default / max(total, 1) * 100, 1),
        "angle_group_distribution": dict(sorted(angle_dist.items())),
        "coat_type_distribution": dict(sorted(coat_dist.items())),
        "body_mass_distribution": dict(sorted(mass_dist.items())),
        "gait_type_distribution": dict(sorted(gait_dist.items())),
    }
