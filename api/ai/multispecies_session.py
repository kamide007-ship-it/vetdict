"""ステージ6：種別対応マルチターン診断セッション管理

複数ターンの会話コンテキスト、種別固有の診断状態、セッション履歴を管理します。
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime
import uuid
import logging

logger = logging.getLogger(__name__)


@dataclass
class SessionMessage:
    """セッション内の単一メッセージ"""

    message_id: str
    timestamp: datetime
    role: str  # "user" または "assistant"
    content: str
    message_type: str  # "question", "symptom_report", "response", etc.
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SymptomSnapshot:
    """セッション内の症状スナップショット"""

    symptom_id: str
    detected_at_turn: int
    confidence: float
    severity: str  # "mild", "moderate", "severe"
    context: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DiseaseHypothesis:
    """セッション内の疾患仮説"""

    disease_name: str
    first_suggested_at_turn: int
    current_confidence: float
    confidence_history: List[float] = field(default_factory=list)
    supporting_symptoms: List[str] = field(default_factory=list)
    contradicting_symptoms: List[str] = field(default_factory=list)


class MultiSpeciesSession:
    """マルチターン診断セッションの管理"""

    def __init__(
        self,
        session_id: Optional[str] = None,
        species: str = "dog",
        patient_name: Optional[str] = None,
        patient_age: Optional[float] = None,
        patient_weight: Optional[float] = None,
    ):
        """
        セッションを初期化します。

        Args:
            session_id: セッションID（Noneなら自動生成）
            species: 動物種
            patient_name: 患者名
            patient_age: 患者年齢（年）
            patient_weight: 患者体重（kg）
        """
        self.session_id = session_id or str(uuid.uuid4())
        self.species = species.lower()
        self.patient_name = patient_name
        self.patient_age = patient_age
        self.patient_weight = patient_weight

        # セッション状態
        self.created_at = datetime.now()
        self.last_updated = self.created_at
        self.current_turn = 0
        self.language = "ja"

        # 検出された情報
        self.detected_symptoms: Dict[str, SymptomSnapshot] = {}
        self.disease_hypotheses: Dict[str, DiseaseHypothesis] = {}
        self.patient_context: Dict[str, Any] = {}

        # メッセージ履歴
        self.messages: List[SessionMessage] = []
        self.question_history: List[str] = []  # 質問IDの履歴

        # 診断状態
        self.is_complete = False
        self.final_diagnosis: Optional[str] = None
        self.confidence_score = 0.0

        # セッション統計
        self.total_questions_asked = 0
        self.total_symptoms_detected = 0

    def add_message(
        self,
        content: str,
        role: str,
        message_type: str = "general",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> SessionMessage:
        """
        メッセージをセッションに追加します。

        Args:
            content: メッセージ内容
            role: "user" または "assistant"
            message_type: メッセージ型
            metadata: オプションのメタデータ

        Returns:
            追加されたSessionMessage
        """
        message = SessionMessage(
            message_id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            role=role,
            content=content,
            message_type=message_type,
            metadata=metadata or {},
        )

        self.messages.append(message)
        self.last_updated = datetime.now()

        return message

    def add_symptom(
        self,
        symptom_id: str,
        confidence: float,
        severity: str = "moderate",
        context: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        症状をセッションに追加します。

        Args:
            symptom_id: 症状ID
            confidence: 信頼度（0-1）
            severity: 重症度（"mild", "moderate", "severe"）
            context: オプションのコンテキスト
        """
        self.detected_symptoms[symptom_id] = SymptomSnapshot(
            symptom_id=symptom_id,
            detected_at_turn=self.current_turn,
            confidence=confidence,
            severity=severity,
            context=context or {},
        )

        self.total_symptoms_detected = len(self.detected_symptoms)
        self.last_updated = datetime.now()

    def update_disease_hypothesis(
        self,
        disease_name: str,
        confidence: float,
        supporting_symptoms: Optional[List[str]] = None,
        contradicting_symptoms: Optional[List[str]] = None,
    ) -> None:
        """
        疾患仮説を更新または追加します。

        Args:
            disease_name: 疾患名
            confidence: 信頼度（0-1）
            supporting_symptoms: サポートする症状リスト
            contradicting_symptoms: 矛盾する症状リスト
        """
        if disease_name not in self.disease_hypotheses:
            # 新規仮説
            self.disease_hypotheses[disease_name] = DiseaseHypothesis(
                disease_name=disease_name,
                first_suggested_at_turn=self.current_turn,
                current_confidence=confidence,
                confidence_history=[confidence],
                supporting_symptoms=supporting_symptoms or [],
                contradicting_symptoms=contradicting_symptoms or [],
            )
        else:
            # 既存仮説を更新
            hypothesis = self.disease_hypotheses[disease_name]
            hypothesis.current_confidence = confidence
            hypothesis.confidence_history.append(confidence)
            if supporting_symptoms:
                hypothesis.supporting_symptoms = supporting_symptoms
            if contradicting_symptoms:
                hypothesis.contradicting_symptoms = contradicting_symptoms

        self.last_updated = datetime.now()

    def ask_question(
        self,
        question_id: str,
        question_text_ja: str,
        question_text_en: str,
    ) -> None:
        """
        質問を記録します。

        Args:
            question_id: 質問ID
            question_text_ja: 日本語の質問文
            question_text_en: 英語の質問文
        """
        self.question_history.append(question_id)
        self.total_questions_asked += 1

        question_text = question_text_ja if self.language == "ja" else question_text_en

        self.add_message(
            content=question_text,
            role="assistant",
            message_type="question",
            metadata={
                "question_id": question_id,
                "question_ja": question_text_ja,
                "question_en": question_text_en,
            },
        )

        self.last_updated = datetime.now()

    def next_turn(self) -> int:
        """
        次のターンに進みます。

        Returns:
            新しいターン番号
        """
        self.current_turn += 1
        self.last_updated = datetime.now()
        return self.current_turn

    def complete_diagnosis(
        self,
        final_diagnosis: str,
        confidence_score: float,
    ) -> None:
        """
        診断を完了します。

        Args:
            final_diagnosis: 最終診断
            confidence_score: 確信度（0-1）
        """
        self.is_complete = True
        self.final_diagnosis = final_diagnosis
        self.confidence_score = confidence_score
        self.last_updated = datetime.now()

    def get_session_summary(self) -> Dict[str, Any]:
        """
        セッションの要約を取得します。

        Returns:
            セッション要約の辞書
        """
        return {
            "session_id": self.session_id,
            "species": self.species,
            "patient_name": self.patient_name,
            "patient_age": self.patient_age,
            "patient_weight": self.patient_weight,
            "created_at": self.created_at.isoformat(),
            "last_updated": self.last_updated.isoformat(),
            "current_turn": self.current_turn,
            "total_questions": self.total_questions_asked,
            "total_symptoms_detected": self.total_symptoms_detected,
            "is_complete": self.is_complete,
            "final_diagnosis": self.final_diagnosis,
            "confidence_score": self.confidence_score,
            "detected_symptoms": {
                s_id: {
                    "symptom_id": s.symptom_id,
                    "detected_at_turn": s.detected_at_turn,
                    "confidence": s.confidence,
                    "severity": s.severity,
                }
                for s_id, s in self.detected_symptoms.items()
            },
            "disease_hypotheses": {
                d_name: {
                    "disease_name": d.disease_name,
                    "first_suggested_at_turn": d.first_suggested_at_turn,
                    "current_confidence": d.current_confidence,
                    "confidence_history": d.confidence_history,
                }
                for d_name, d in self.disease_hypotheses.items()
            },
            "message_count": len(self.messages),
            "question_history": self.question_history,
        }

    def get_conversation_context(self) -> Dict[str, Any]:
        """
        会話コンテキストを取得します。

        Returns:
            会話コンテキストの辞書
        """
        return {
            "session_id": self.session_id,
            "species": self.species,
            "current_turn": self.current_turn,
            "detected_symptoms": list(self.detected_symptoms.keys()),
            "hypothesis_count": len(self.disease_hypotheses),
            "messages": [
                {
                    "role": m.role,
                    "content": m.content,
                    "type": m.message_type,
                }
                for m in self.messages[-10:]  # 最新10メッセージ
            ],
        }

    def should_continue_diagnosis(self) -> Tuple[bool, str]:
        """
        診断を継続すべきかを判定します。

        Returns:
            (should_continue, reason) のタプル
        """
        # 既に完了している場合
        if self.is_complete:
            return False, "診断は既に完了しています"

        # ターン数が多すぎる場合
        if self.current_turn > 15:
            return False, "最大ターン数に達しました"

        # 信頼度が高い場合
        top_hypothesis = self._get_top_hypothesis()
        if top_hypothesis and top_hypothesis[1].current_confidence > 0.85:
            return False, "信頼度が十分に高くなりました"

        # 症状が十分に検出されている場合
        if self.total_symptoms_detected >= 8:
            if any(h.current_confidence > 0.7 for h in self.disease_hypotheses.values()):
                return False, "診断に必要な症状が十分に検出されました"

        return True, "診断を継続してください"

    def get_species_specific_context(self) -> Dict[str, Any]:
        """
        種別固有のコンテキストを取得します。

        Returns:
            種別固有のコンテキスト情報
        """
        context = {
            "species": self.species,
            "age_years": self.patient_age,
        }

        # 種別固有の情報を追加
        species_contexts = {
            "dog": {
                "breed_info_available": "breed" in self.patient_context,
                "typical_senior_age": 7,
            },
            "cat": {
                "indoor_outdoor": self.patient_context.get("indoor_outdoor"),
                "typical_senior_age": 7,
            },
            "rabbit": {
                "diet_type": self.patient_context.get("diet_type"),
                "typical_senior_age": 5,
            },
            "horse": {
                "discipline": self.patient_context.get("discipline"),
                "typical_senior_age": 15,
            },
        }

        if self.species in species_contexts:
            context.update(species_contexts[self.species])

        return context

    def _get_top_hypothesis(self) -> Optional[Tuple[str, DiseaseHypothesis]]:
        """
        最も信頼度の高い仮説を取得します。

        Returns:
            (disease_name, hypothesis) のタプルまたはNone
        """
        if not self.disease_hypotheses:
            return None

        top = max(
            self.disease_hypotheses.items(),
            key=lambda x: x[1].current_confidence,
        )

        return top

    def export_session_json(self) -> Dict[str, Any]:
        """
        セッションをJSON形式にエクスポートします。

        Returns:
            JSON形式のセッションデータ
        """
        return {
            "session": self.get_session_summary(),
            "messages": [
                {
                    "id": m.message_id,
                    "timestamp": m.timestamp.isoformat(),
                    "role": m.role,
                    "content": m.content,
                    "type": m.message_type,
                    "metadata": m.metadata,
                }
                for m in self.messages
            ],
        }
