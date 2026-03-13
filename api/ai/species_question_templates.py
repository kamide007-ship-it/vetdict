"""ステージ5：種別別の適応的質問テンプレート

各動物種に特化した質問テンプレート、翻訳、スコアリング情報を提供。
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set


@dataclass
class QuestionTemplate:
    """質問テンプレートの構造"""

    question_id: str
    question_en: str
    question_ja: str
    question_type: str  # "yes_no", "multiple_choice", "severity", "duration"
    species: List[str]  # 適用可能な種別
    symptom_targets: List[str]  # この質問が対象とする症状
    entropy_weight: float  # 情報ゲインでの重み
    followup_questions: List[str] = None  # フォローアップ質問ID
    explanation_ja: str = ""
    explanation_en: str = ""


# 犬用質問テンプレート
DOG_QUESTIONS = {
    "limping_location": {
        "question_id": "limping_location",
        "question_en": "Which leg is affected by the limping?",
        "question_ja": "どの足に跛行が見られますか？",
        "question_type": "multiple_choice",
        "species": ["dog"],
        "symptom_targets": ["lameness"],
        "entropy_weight": 0.85,
        "followup_questions": ["limping_duration", "lameness_severity"],
        "explanation_ja": "跛行の位置は関節炎、靭帯損傷、骨折などの原因を特定するのに重要です",
    },
    "vomiting_frequency": {
        "question_id": "vomiting_frequency",
        "question_en": "How often is your dog vomiting?",
        "question_ja": "犬は何回嘔吐していますか？",
        "question_type": "multiple_choice",
        "species": ["dog"],
        "symptom_targets": ["vomiting"],
        "entropy_weight": 0.80,
        "followup_questions": ["vomit_appearance", "vomiting_timing"],
        "explanation_ja": "嘔吐の頻度は膵炎、胃腸炎、異物誤飲などの重症度を示します",
    },
    "lameness_severity": {
        "question_id": "lameness_severity",
        "question_en": "How severe is the lameness?",
        "question_ja": "跛行の重症度はどの程度ですか？",
        "question_type": "severity",
        "species": ["dog"],
        "symptom_targets": ["lameness"],
        "entropy_weight": 0.75,
        "explanation_ja": "重症度は診断の確信度を調整するために使用されます",
    },
    "vomit_appearance": {
        "question_id": "vomit_appearance",
        "question_en": "What does the vomit look like?",
        "question_ja": "嘔吐物はどのような外観ですか？",
        "question_type": "multiple_choice",
        "species": ["dog"],
        "symptom_targets": ["vomiting"],
        "entropy_weight": 0.70,
        "explanation_ja": "嘔吐物の外観は胃腸疾患の原因を特定するのに役立ちます",
    },
    "appetite_change_timing": {
        "question_id": "appetite_change_timing",
        "question_en": "When did the appetite loss start?",
        "question_ja": "食欲不振はいつから始まりましたか？",
        "question_type": "duration",
        "species": ["dog"],
        "symptom_targets": ["appetite_loss"],
        "entropy_weight": 0.75,
        "explanation_ja": "発症のタイミングは急性または慢性の疾患を区別します",
    },
}

# 猫用質問テンプレート
CAT_QUESTIONS = {
    "urinary_frequency": {
        "question_id": "urinary_frequency",
        "question_en": "How often is your cat urinating?",
        "question_ja": "猫の排尿頻度はどの程度ですか？",
        "question_type": "multiple_choice",
        "species": ["cat"],
        "symptom_targets": ["urinary_frequency", "urinary_straining"],
        "entropy_weight": 0.90,
        "followup_questions": ["urine_appearance", "straining_signs"],
        "explanation_ja": "猫の排尿異常は特発性膀胱炎、尿路結石、尿路感染を示唆します",
    },
    "vomiting_hairballs": {
        "question_id": "vomiting_hairballs",
        "question_en": "Are hairballs visible in the vomit?",
        "question_ja": "嘔吐物に毛玉が見られますか？",
        "question_type": "yes_no",
        "species": ["cat"],
        "symptom_targets": ["vomiting"],
        "entropy_weight": 0.65,
        "explanation_ja": "毛玉は猫の嘔吐の一般的な原因です",
    },
    "litter_box_behavior": {
        "question_id": "litter_box_behavior",
        "question_en": "Is the cat avoiding the litter box?",
        "question_ja": "猫はトイレを避けていますか？",
        "question_type": "yes_no",
        "species": ["cat"],
        "symptom_targets": ["urinary_frequency", "behavioral_changes"],
        "entropy_weight": 0.80,
        "explanation_ja": "トイレ回避行動は尿路疾患または行動的な問題を示唆します",
    },
    "respiratory_effort": {
        "question_id": "respiratory_effort",
        "question_en": "Is the cat having difficulty breathing?",
        "question_ja": "猫に呼吸困難が見られますか？",
        "question_type": "severity",
        "species": ["cat"],
        "symptom_targets": ["labored_breathing", "wheezing"],
        "entropy_weight": 0.85,
        "explanation_ja": "呼吸困難は猫喘息や心疾患を示唆する重大な兆候です",
    },
    "appetite_pattern": {
        "question_id": "appetite_pattern",
        "question_en": "Is the appetite loss complete or partial?",
        "question_ja": "食欲不振は完全ですか、それとも部分的ですか？",
        "question_type": "multiple_choice",
        "species": ["cat"],
        "symptom_targets": ["appetite_loss"],
        "entropy_weight": 0.70,
        "explanation_ja": "完全な食欲不振はより重篤な疾患を示唆します",
    },
}

# ウサギ用質問テンプレート
RABBIT_QUESTIONS = {
    "fecal_changes": {
        "question_id": "fecal_changes",
        "question_en": "Have the rabbit's droppings changed?",
        "question_ja": "ウサギの糞便に変化がありますか？",
        "question_type": "multiple_choice",
        "species": ["rabbit"],
        "symptom_targets": ["diarrhea", "constipation"],
        "entropy_weight": 0.90,
        "followup_questions": ["fecal_consistency", "appetite_change"],
        "explanation_ja": "ウサギの糞便変化は胃腸停滞や寄生虫を示唆する重要な兆候です",
    },
    "appetite_reduction": {
        "question_id": "appetite_reduction",
        "question_en": "Is the rabbit eating less than usual?",
        "question_ja": "ウサギはいつもより食べていますか？",
        "question_type": "severity",
        "species": ["rabbit"],
        "symptom_targets": ["appetite_loss"],
        "entropy_weight": 0.95,
        "explanation_ja": "食欲低下は胃腸停滞の最初の兆候であり、緊急対応が必要です",
    },
    "teeth_grinding": {
        "question_id": "teeth_grinding",
        "question_en": "Are you hearing teeth grinding sounds?",
        "question_ja": "歯ぎしりの音が聞こえますか？",
        "question_type": "yes_no",
        "species": ["rabbit"],
        "symptom_targets": ["abdominal_pain"],
        "entropy_weight": 0.85,
        "explanation_ja": "歯ぎしりはウサギの痛みの主な指標です",
    },
    "stool_consistency": {
        "question_id": "stool_consistency",
        "question_en": "What is the consistency of the droppings?",
        "question_ja": "糞便の固さはどうですか？",
        "question_type": "multiple_choice",
        "species": ["rabbit"],
        "symptom_targets": ["diarrhea", "constipation"],
        "entropy_weight": 0.80,
        "explanation_ja": "糞便の固さは原因となる腸疾患の特定を助けます",
    },
    "environmental_stress": {
        "question_id": "environmental_stress",
        "question_en": "Has there been any recent environmental change?",
        "question_ja": "最近、環境に変化がありましたか？",
        "question_type": "yes_no",
        "species": ["rabbit"],
        "symptom_targets": ["appetite_loss", "behavioral_changes"],
        "entropy_weight": 0.65,
        "explanation_ja": "ウサギはストレスに非常に敏感であり、胃腸停滞を引き起こす可能性があります",
    },
}

# 鳥用質問テンプレート
BIRD_QUESTIONS = {
    "respiratory_effort": {
        "question_id": "respiratory_effort",
        "question_en": "Is the bird fluffing its feathers and breathing heavily?",
        "question_ja": "鳥は羽を膨らませて重く呼吸していますか？",
        "question_type": "severity",
        "species": ["bird"],
        "symptom_targets": ["labored_breathing"],
        "entropy_weight": 0.95,
        "explanation_ja": "羽の膨張と呼吸困難は呼吸器疾患または全身的な問題を示唆します",
    },
    "appetite_pattern": {
        "question_id": "appetite_pattern",
        "question_en": "Is the bird eating and drinking normally?",
        "question_ja": "鳥は通常通り食べたり飲んだりしていますか？",
        "question_type": "yes_no",
        "species": ["bird"],
        "symptom_targets": ["appetite_loss"],
        "entropy_weight": 0.90,
        "explanation_ja": "鳥の食欲低下は重篤な疾患を示唆します",
    },
    "feather_condition": {
        "question_id": "feather_condition",
        "question_en": "What is the condition of the feathers?",
        "question_ja": "羽の状態はどうですか？",
        "question_type": "multiple_choice",
        "species": ["bird"],
        "symptom_targets": ["hair_loss", "itching", "behavioral_changes"],
        "entropy_weight": 0.75,
        "explanation_ja": "羽の状態は栄養状態、ストレス、寄生虫を示唆します",
    },
    "perching_ability": {
        "question_id": "perching_ability",
        "question_en": "Can the bird perch normally?",
        "question_ja": "鳥は正常に止まり木に止まることができますか？",
        "question_type": "yes_no",
        "species": ["bird"],
        "symptom_targets": ["lameness"],
        "entropy_weight": 0.80,
        "explanation_ja": "止まり木能力の喪失は脚の問題または全身的な衰弱を示唆します",
    },
    "droppings_appearance": {
        "question_id": "droppings_appearance",
        "question_en": "What do the droppings look like?",
        "question_ja": "糞の外観はどうですか？",
        "question_type": "multiple_choice",
        "species": ["bird"],
        "symptom_targets": ["diarrhea"],
        "entropy_weight": 0.70,
        "explanation_ja": "糞の異常は消化器疾患を示唆します",
    },
}

# 馬用質問テンプレート
HORSE_QUESTIONS = {
    "colic_severity": {
        "question_id": "colic_severity",
        "question_en": "What is the severity of the colic?",
        "question_ja": "疝痛の重症度はどの程度ですか？",
        "question_type": "severity",
        "species": ["horse"],
        "symptom_targets": ["abdominal_pain"],
        "entropy_weight": 0.95,
        "explanation_ja": "疝痛の重症度は治療の緊急性を決定します",
    },
    "lameness_details": {
        "question_id": "lameness_details",
        "question_en": "Which leg and how severe is the lameness?",
        "question_ja": "どの脚に跛行が見られ、重症度はどの程度ですか？",
        "question_type": "multiple_choice",
        "species": ["horse"],
        "symptom_targets": ["lameness"],
        "entropy_weight": 0.90,
        "explanation_ja": "跛行の詳細な情報は骨格系の特定の問題を示唆します",
    },
    "exercise_tolerance": {
        "question_id": "exercise_tolerance",
        "question_en": "Has exercise tolerance decreased?",
        "question_ja": "運動耐性は低下していますか？",
        "question_type": "severity",
        "species": ["horse"],
        "symptom_targets": ["lethargy", "labored_breathing"],
        "entropy_weight": 0.80,
        "explanation_ja": "運動耐性の低下は心肺または筋骨格系の問題を示唆します",
    },
    "respiratory_pattern": {
        "question_id": "respiratory_pattern",
        "question_en": "Is the respiratory pattern normal at rest?",
        "question_ja": "休息時に呼吸パターンは正常ですか？",
        "question_type": "yes_no",
        "species": ["horse"],
        "symptom_targets": ["labored_breathing"],
        "entropy_weight": 0.75,
        "explanation_ja": "異常な呼吸パターンは呼吸器疾患を示唆します",
    },
}

# すべての質問テンプレートをまとめる
ALL_SPECIES_QUESTIONS = {
    "dog": DOG_QUESTIONS,
    "cat": CAT_QUESTIONS,
    "rabbit": RABBIT_QUESTIONS,
    "bird": BIRD_QUESTIONS,
    "horse": HORSE_QUESTIONS,
}

# 汎用質問テンプレート（すべての種別に適用可能）
UNIVERSAL_QUESTIONS = {
    "symptom_duration": {
        "question_id": "symptom_duration",
        "question_en": "How long have the symptoms been present?",
        "question_ja": "症状はどのくらいの間、存在していますか？",
        "question_type": "duration",
        "species": [
            "dog", "cat", "rabbit", "hamster", "guinea_pig", "ferret",
            "bird", "reptile", "horse", "hedgehog"
        ],
        "symptom_targets": ["general"],
        "entropy_weight": 0.70,
        "explanation_ja": "症状の期間は急性対慢性を区別するのに役立ちます",
    },
    "symptom_progression": {
        "question_id": "symptom_progression",
        "question_en": "Are the symptoms getting worse, better, or staying the same?",
        "question_ja": "症状は悪化していますか、改善していますか、それとも同じままですか？",
        "question_type": "multiple_choice",
        "species": [
            "dog", "cat", "rabbit", "hamster", "guinea_pig", "ferret",
            "bird", "reptile", "horse", "hedgehog"
        ],
        "symptom_targets": ["general"],
        "entropy_weight": 0.75,
        "explanation_ja": "症状の進行は予後と治療の必要性を示唆します",
    },
    "recent_changes": {
        "question_id": "recent_changes",
        "question_en": "Have there been any recent diet, medication, or environment changes?",
        "question_ja": "最近、食事、薬物投与、または環境に変化がありましたか？",
        "question_type": "yes_no",
        "species": [
            "dog", "cat", "rabbit", "hamster", "guinea_pig", "ferret",
            "bird", "reptile", "horse", "hedgehog"
        ],
        "symptom_targets": ["general"],
        "entropy_weight": 0.70,
        "explanation_ja": "最近の変化は症状のきっかけを示す可能性があります",
    },
}


def get_questions_for_species(species: str) -> Dict[str, Dict[str, Any]]:
    """
    種別の質問テンプレートを取得します。

    Args:
        species: 対象種別

    Returns:
        その種別の質問テンプレート辞書
    """
    species_lower = species.lower()

    species_questions = ALL_SPECIES_QUESTIONS.get(species_lower, {})

    # 汎用質問も含める
    combined = UNIVERSAL_QUESTIONS.copy()
    combined.update(species_questions)

    return combined


def get_question_by_id(question_id: str, species: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    質問IDで質問テンプレートを取得します。

    Args:
        question_id: 質問ID
        species: オプションの対象種別

    Returns:
        質問テンプレートまたはNone
    """
    # 汎用質問をチェック
    if question_id in UNIVERSAL_QUESTIONS:
        return UNIVERSAL_QUESTIONS[question_id]

    # 種別固有の質問をチェック
    if species:
        species_lower = species.lower()
        questions = ALL_SPECIES_QUESTIONS.get(species_lower, {})
        if question_id in questions:
            return questions[question_id]

    # すべての種別から検索
    for species_questions in ALL_SPECIES_QUESTIONS.values():
        if question_id in species_questions:
            return species_questions[question_id]

    return None


def get_target_symptoms_for_question(question_id: str) -> List[str]:
    """
    質問の対象症状を取得します。

    Args:
        question_id: 質問ID

    Returns:
        対象症状のリスト
    """
    question = get_question_by_id(question_id)
    if question:
        return question.get("symptom_targets", [])
    return []


def get_followup_questions(question_id: str) -> List[str]:
    """
    質問のフォローアップ質問を取得します。

    Args:
        question_id: 質問ID

    Returns:
        フォローアップ質問IDのリスト
    """
    question = get_question_by_id(question_id)
    if question:
        return question.get("followup_questions", [])
    return []


def filter_questions_by_species(
    question_ids: List[str],
    species: str,
) -> List[str]:
    """
    種別に適用可能な質問をフィルタリングします。

    Args:
        question_ids: 質問IDのリスト
        species: 対象種別

    Returns:
        種別に適用可能な質問IDのリスト
    """
    species_lower = species.lower()
    questions = get_questions_for_species(species)

    filtered = []
    for q_id in question_ids:
        if q_id in questions:
            filtered.append(q_id)

    return filtered
