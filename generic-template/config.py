"""
=============================================================================
 Analysis Platform - Configuration
=============================================================================
 このファイルを編集するだけで、任意のドメインの解析プラットフォームに変更できます。
 例: 料理の品質評価、建築物の状態診断、植物の健康チェック、車両の外装診断 etc.

 変更箇所:
   1. PLATFORM_* : プラットフォーム名・説明
   2. CATEGORIES : 解析対象のカテゴリ（犬種の代わりに料理名、建物タイプ等）
   3. PHOTO_AXES : 写真解析の評価軸
   4. VIDEO_AXES : 動画解析の評価軸
   5. SCORING_WEIGHTS : 各軸のスコア重み
   6. AI_PROMPTS : AI解析用プロンプトテンプレート
=============================================================================
"""

# ---------------------------------------------------------------------------
# 1. Platform Identity
# ---------------------------------------------------------------------------
PLATFORM_NAME = "Analysis Platform"
PLATFORM_DESCRIPTION = "AI画像・動画解析プラットフォーム"
PLATFORM_VERSION = "1.0.0"
PLATFORM_EMOJI = "🔍"  # ヘッダーアイコン

# ---------------------------------------------------------------------------
# 2. Categories (解析対象のカテゴリ)
# ---------------------------------------------------------------------------
# key: カテゴリID, value: カテゴリ情報
# 各カテゴリに自由な属性を追加可能（AI promptで参照される）
CATEGORIES = {
    "sample_category_a": {
        "name": "カテゴリA",
        "name_en": "Category A",
        "description": "カテゴリAの説明",
        # 以下はドメイン固有の属性（AI promptから参照）
        "ideal_standard": "理想的な基準の説明",
        "ideal_ratio": 1.4,  # ローカル解析で使用される参照値
    },
    "sample_category_b": {
        "name": "カテゴリB",
        "name_en": "Category B",
        "description": "カテゴリBの説明",
        "ideal_standard": "理想的な基準の説明",
        "ideal_ratio": 1.2,
    },
}

DEFAULT_CATEGORY = "sample_category_a"

# ---------------------------------------------------------------------------
# 3. Photo Analysis Axes (写真解析の評価軸)
# ---------------------------------------------------------------------------
# 各軸は name(表示名), key(JSONキー), description(説明) を持つ
PHOTO_AXES_PRIMARY = {
    "name": "構造解析",
    "axes": [
        {"key": "proportion", "name": "プロポーション", "description": "全体のバランス"},
        {"key": "detail", "name": "ディテール", "description": "細部の精度"},
        {"key": "quality", "name": "品質", "description": "全体的な品質"},
    ],
}

PHOTO_AXES_SECONDARY = {
    "name": "外観解析",
    "axes": [
        {"key": "texture", "name": "テクスチャ", "description": "表面の質感"},
        {"key": "color", "name": "色彩", "description": "色のバランスと鮮やかさ"},
        {"key": "condition", "name": "状態", "description": "手入れ・保存状態"},
    ],
}

# ---------------------------------------------------------------------------
# 4. Video Analysis Axes (動画解析の評価軸)
# ---------------------------------------------------------------------------
VIDEO_AXES = {
    "motion": {
        "name": "動作解析",
        "axes": [
            {"key": "fluidity", "name": "流動性", "description": "動きの滑らかさ"},
            {"key": "stability", "name": "安定性", "description": "動きの安定さ"},
            {"key": "rhythm", "name": "リズム", "description": "動きのリズム"},
        ],
    },
    "behavior": {
        "name": "振る舞い解析",
        "axes": [
            {"key": "consistency", "name": "一貫性", "description": "動作の一貫性"},
            {"key": "responsiveness", "name": "反応性", "description": "環境への反応"},
            {"key": "composure", "name": "安定度", "description": "全体的な安定度"},
        ],
    },
    "surface_motion": {
        "name": "表面動態",
        "axes": [],
    },
}

# ---------------------------------------------------------------------------
# 5. Scoring Weights (スコア重み)
# ---------------------------------------------------------------------------
# 写真のみの場合と、写真+動画の場合で重みを分ける
WEIGHTS_PHOTO_ONLY = {
    "primary": 0.55,    # 構造解析
    "secondary": 0.45,  # 外観解析
}

WEIGHTS_WITH_VIDEO = {
    "primary": 0.30,    # 構造解析
    "secondary": 0.25,  # 外観解析
    "motion": 0.25,     # 動作解析
    "behavior": 0.20,   # 振る舞い解析
}

# グレード定義
GRADE_THRESHOLDS = [
    (95, "Excellent", "卓越"),
    (85, "Very Good", "非常に良い"),
    (75, "Good", "良好"),
    (65, "Sufficient", "十分"),
    (0, "Needs Improvement", "要改善"),
]

# ---------------------------------------------------------------------------
# 6. AI Prompts (AI解析用プロンプトテンプレート)
# ---------------------------------------------------------------------------
# {category_name}, {category_data}, {axes_json} はランタイムで置換される

AI_PROMPT_PRIMARY = """あなたはプロフェッショナルな{platform_name}の専門家です。
この{category_name}の画像を詳細に分析し、100点満点で評価してください。

【基準】
{standard}

【評価項目】
{axes_description}

【出力形式】JSON形式のみで返してください:
{axes_json}"""

AI_PROMPT_SECONDARY = """あなたはプロフェッショナルな{platform_name}の専門家です。
この{category_name}の外観を詳細に分析し、100点満点で評価してください。

【基準】
{standard}

【評価項目】
{axes_description}

【出力形式】JSON形式のみで返してください:
{axes_json}"""

AI_PROMPT_VIDEO = """あなたはプロフェッショナルな{platform_name}の専門家です。
この{category_name}の動画フレーム（複数枚）を分析し、以下を100点満点で評価してください。

【基準】
{standard}

【評価項目】
{axes_description}

【出力形式】JSON形式のみで返してください:
{axes_json}"""
