"""ステージ5：種別別の適応的質問最適化

エントロピー計算に基づいて、各種別に最適な質問を動的に選択します。
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set, Tuple
import logging
import math

logger = logging.getLogger(__name__)

from api.ai.species_question_templates import (
    get_questions_for_species,
    get_question_by_id,
    get_target_symptoms_for_question,
    filter_questions_by_species,
)


@dataclass
class OptimizedQuestion:
    """最適化されたフォローアップ質問"""

    question_id: str
    question_en: str
    question_ja: str
    entropy_reduction: float  # この質問でどれだけエントロピーが減るか
    information_gain: float  # 情報ゲイン値
    priority: int  # 1 = 最優先、値が大きいほど優先度が低い
    reasoning: str


class SpeciesQuestionOptimizer:
    """種別別の適応的質問最適化エンジン"""

    def __init__(self):
        """質問最適化エンジンを初期化"""
        self.question_cache: Dict[str, Dict[str, Any]] = {}

    def optimize_questions_for_species(
        self,
        disease_candidates: List[Dict[str, Any]],
        species: str,
        detected_symptoms: List[str],
        language: str = "ja",
        max_questions: int = 5,
    ) -> List[OptimizedQuestion]:
        """
        種別の疾患候補に基づいて最適な質問を選択します。

        Args:
            disease_candidates: 疾患候補のリスト（confidence付き）
            species: 対象種別
            detected_symptoms: 検出された症状のリスト
            language: 言語（"ja" または "en"）
            max_questions: 返す最大質問数

        Returns:
            最適化されたOptimizedQuestionのリスト
        """
        species_lower = species.lower()

        # 質問プールを取得
        available_questions = get_questions_for_species(species)

        # すでに検出された症状に関連する質問を除外
        candidate_questions = self._filter_relevant_questions(
            available_questions,
            detected_symptoms,
            disease_candidates,
        )

        if not candidate_questions:
            logger.warning(f"No candidate questions for {species}")
            return []

        # 各質問のエントロピー削減を計算
        scored_questions = []

        for q_id, question in candidate_questions.items():
            entropy_reduction = self.calculate_question_entropy_reduction(
                q_id,
                disease_candidates,
                detected_symptoms,
                species,
            )

            # 情報ゲインを計算
            info_gain = entropy_reduction * question.get("entropy_weight", 0.5)

            if info_gain > 0.0:
                reasoning = self._generate_question_reasoning(
                    q_id, info_gain, disease_candidates
                )

                scored_questions.append({
                    "question_id": q_id,
                    "question_en": question.get("question_en", ""),
                    "question_ja": question.get("question_ja", ""),
                    "entropy_reduction": entropy_reduction,
                    "information_gain": info_gain,
                    "reasoning": reasoning,
                })

        # 情報ゲインでソート（降順）
        scored_questions.sort(
            key=lambda x: x["information_gain"],
            reverse=True
        )

        # 最大質問数に制限
        top_questions = scored_questions[:max_questions]

        # OptimizedQuestionオブジェクトに変換
        optimized = []
        for idx, q in enumerate(top_questions, 1):
            optimized.append(OptimizedQuestion(
                question_id=q["question_id"],
                question_en=q["question_en"],
                question_ja=q["question_ja"],
                entropy_reduction=q["entropy_reduction"],
                information_gain=q["information_gain"],
                priority=idx,
                reasoning=q["reasoning"],
            ))

        return optimized

    def calculate_species_entropy(
        self,
        diseases: List[Dict[str, Any]],
        species: str,
    ) -> float:
        """
        種別の疾患候補に基づいてエントロピーを計算します。

        Args:
            diseases: 疾患候補のリスト（confidence付き）
            species: 対象種別

        Returns:
            エントロピー値（0-1）
        """
        if not diseases:
            return 0.0

        # 信頼度を正規化
        confidences = []
        for disease in diseases:
            conf = disease.get("confidence", disease.get("match_percent", 0))
            if conf > 1.0:
                conf /= 100.0
            confidences.append(conf)

        # 合計が1.0になるように正規化
        total_conf = sum(confidences)
        if total_conf == 0:
            return 0.0

        normalized = [c / total_conf for c in confidences]

        # シャノンエントロピーを計算
        entropy = 0.0
        for p in normalized:
            if p > 0:
                entropy -= p * math.log2(p)

        # 最大エントロピーで正規化（0-1の範囲に）
        max_entropy = math.log2(len(normalized)) if len(normalized) > 1 else 1.0
        normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0.0

        return min(normalized_entropy, 1.0)

    def calculate_question_entropy_reduction(
        self,
        question_id: str,
        diseases: List[Dict[str, Any]],
        detected_symptoms: List[str],
        species: str,
    ) -> float:
        """
        質問がエントロピーをどれだけ減らすかを計算します。

        Args:
            question_id: 質問ID
            diseases: 疾患候補のリスト
            detected_symptoms: 検出済み症状
            species: 対象種別

        Returns:
            エントロピー削減値（0-1）
        """
        question = get_question_by_id(question_id, species)
        if not question:
            return 0.0

        # この質問の対象症状を取得
        target_symptoms = get_target_symptoms_for_question(question_id)
        if not target_symptoms or "general" in target_symptoms:
            # 汎用質問
            target_symptoms = []

        # 対象症状がすでに検出されているか確認
        if target_symptoms:
            overlap = set(target_symptoms) & set(detected_symptoms)
            if overlap:
                # すでに検出された症状に関する質問は価値が低い
                return 0.1

        # この質問に関連する疾患を見つける
        relevant_diseases = self._get_diseases_related_to_question(
            question_id,
            diseases,
        )

        if not relevant_diseases:
            return 0.2  # 関連疾患がない場合は低い値

        # 関連疾患の信頼度分布
        confidences = [d.get("confidence", 0) for d in relevant_diseases]
        confidences = [c / 100.0 if c > 1.0 else c for c in confidences]

        # 現在のエントロピー
        current_entropy = self._calculate_distribution_entropy(confidences)

        # 質問の回答後の予想エントロピー
        # （理想的には50-50に分割されると仮定）
        expected_entropy = 0.5 * current_entropy  # エントロピーが50%削減されると仮定

        entropy_reduction = max(0.0, current_entropy - expected_entropy)

        return min(entropy_reduction, 1.0)

    def _filter_relevant_questions(
        self,
        available_questions: Dict[str, Dict[str, Any]],
        detected_symptoms: List[str],
        disease_candidates: List[Dict[str, Any]],
    ) -> Dict[str, Dict[str, Any]]:
        """
        関連性のある質問をフィルタリングします。

        Args:
            available_questions: 利用可能な質問
            detected_symptoms: 検出済み症状
            disease_candidates: 疾患候補

        Returns:
            関連性のある質問の辞書
        """
        filtered = {}

        for q_id, question in available_questions.items():
            # 対象症状を取得
            target_symptoms = question.get("symptom_targets", [])

            # すでに検出された症状に関連する質問は除外
            if target_symptoms and "general" not in target_symptoms:
                overlap = set(target_symptoms) & set(detected_symptoms)
                if overlap:
                    continue  # スキップ

            # 疾患候補に関連しているか確認
            is_relevant = False

            if "general" in target_symptoms:
                is_relevant = True
            else:
                # より詳細な関連性チェック
                for disease in disease_candidates[:3]:  # トップ3の疾患
                    disease_name = disease.get("name", "")
                    if self._is_question_relevant_to_disease(
                        q_id,
                        disease_name,
                    ):
                        is_relevant = True
                        break

            if is_relevant:
                filtered[q_id] = question

        return filtered

    def _get_diseases_related_to_question(
        self,
        question_id: str,
        diseases: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        質問に関連する疾患を取得します。

        Args:
            question_id: 質問ID
            diseases: 疾患候補のリスト

        Returns:
            関連疾患のリスト
        """
        target_symptoms = get_target_symptoms_for_question(question_id)
        if not target_symptoms:
            return diseases[:3]  # デフォルトでトップ3を返す

        # この質問の対象症状を持つ疾患を見つける
        related = []
        for disease in diseases:
            disease_symptoms = disease.get("symptoms", [])
            if any(s in disease_symptoms for s in target_symptoms):
                related.append(disease)

        return related if related else diseases[:3]

    @staticmethod
    def _is_question_relevant_to_disease(
        question_id: str,
        disease_name: str,
    ) -> bool:
        """
        質問が疾患に関連しているかをチェックします。

        Args:
            question_id: 質問ID
            disease_name: 疾患名

        Returns:
            関連があればTrue
        """
        # 簡単な実装：実際にはより複雑なマッピングが必要
        target_symptoms = get_target_symptoms_for_question(question_id)

        if not target_symptoms or "general" in target_symptoms:
            return True

        # より詳細な関連性チェック（後で実装可能）
        return True

    @staticmethod
    def _calculate_distribution_entropy(values: List[float]) -> float:
        """
        値の分布のエントロピーを計算します。

        Args:
            values: 正規化された値のリスト

        Returns:
            エントロピー値
        """
        if not values:
            return 0.0

        # 合計が1.0になるように正規化
        total = sum(values)
        if total == 0:
            return 0.0

        normalized = [v / total for v in values]

        # シャノンエントロピー
        entropy = 0.0
        for p in normalized:
            if p > 0:
                entropy -= p * math.log2(p)

        return entropy

    @staticmethod
    def _generate_question_reasoning(
        question_id: str,
        information_gain: float,
        disease_candidates: List[Dict[str, Any]],
    ) -> str:
        """
        質問選択の理由を生成します。

        Args:
            question_id: 質問ID
            information_gain: 情報ゲイン値
            disease_candidates: 疾患候補

        Returns:
            日本語の説明
        """
        # 情報ゲインレベルを判定
        if information_gain > 0.6:
            gain_desc = "非常に有用な"
        elif information_gain > 0.4:
            gain_desc = "有用な"
        else:
            gain_desc = "適度に有用な"

        # トップ疾患を取得
        if disease_candidates:
            top_disease = disease_candidates[0].get("name", "不明")
            return f"{gain_desc}質問。{top_disease}と他の疾患の鑑別に役立ちます。"

        return f"{gain_desc}質問。診断の確実性を向上させるのに役立ちます。"

    def get_followup_question_sequence(
        self,
        initial_question_id: str,
        species: str,
    ) -> List[str]:
        """
        質問のフォローアップ質問シーケンスを取得します。

        Args:
            initial_question_id: 最初の質問ID
            species: 対象種別

        Returns:
            フォローアップ質問IDのシーケンス
        """
        sequence = [initial_question_id]
        current_id = initial_question_id

        while len(sequence) < 5:  # 最大5問のシーケンス
            question = get_question_by_id(current_id, species)
            if not question:
                break

            followups = question.get("followup_questions", [])
            if not followups:
                break

            # 最初のフォローアップ質問を選択
            current_id = followups[0]
            sequence.append(current_id)

        return sequence


# モジュールレベルの便利関数
def optimize_questions(
    disease_candidates: List[Dict[str, Any]],
    species: str,
    detected_symptoms: List[str],
    max_questions: int = 5,
) -> List[OptimizedQuestion]:
    """
    質問を最適化する便利関数。

    Args:
        disease_candidates: 疾患候補
        species: 対象種別
        detected_symptoms: 検出済み症状
        max_questions: 最大質問数

    Returns:
        最適化された質問のリスト
    """
    optimizer = SpeciesQuestionOptimizer()
    return optimizer.optimize_questions_for_species(
        disease_candidates,
        species,
        detected_symptoms,
        max_questions=max_questions,
    )
