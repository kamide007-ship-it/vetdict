"""ステージ7：マルチ種別診断API統合

種別対応の診断エンドポイントと統合。
"""

from flask import Blueprint, request, jsonify
from typing import Any, Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

from api.ai.symptom_disambiguator import disambiguate_symptom, validate_symptoms_for_species
from api.ai.species_disease_scorer import SpeciesDiseaseScorer
from api.ai.species_question_optimizer import SpeciesQuestionOptimizer
from api.ai.multispecies_session import MultiSpeciesSession
from api.ai.session_persistence import (
    SessionPersistenceManager,
    get_or_create_session,
    cache_session,
)


# Blueprintを作成
diagnostic_multi_bp = Blueprint(
    "diagnostic_multi",
    __name__,
    url_prefix="/api/diagnostic/v2",
)

# セッション永続化マネージャー
session_manager = SessionPersistenceManager()
question_optimizer = SpeciesQuestionOptimizer()
disease_scorer = SpeciesDiseaseScorer()

# サポートされている種別
SUPPORTED_SPECIES = {
    "dog", "cat", "rabbit", "hamster", "guinea_pig", "ferret",
    "bird", "reptile", "horse", "hedgehog"
}


@diagnostic_multi_bp.route("/analyze", methods=["POST"])
def analyze_symptoms():
    """
    症状を分析して疾患診断を行います。

    Request JSON:
    {
        "session_id": "...",  // オプション：既存セッション
        "species": "dog",
        "symptoms": ["vomiting", "lethargy"],
        "patient_info": {
            "name": "...",
            "age": 5,
            "weight": 25,
            "breed": "Golden Retriever"  // 犬の場合
        }
    }

    Returns:
    {
        "success": true,
        "session_id": "...",
        "species": "dog",
        "symptoms_validated": ["vomiting", "lethargy"],
        "symptoms_invalid": [],
        "disease_candidates": [
            {
                "name": "Pancreatitis",
                "confidence": 0.75,
                "match_percent": 75,
                "explanation_ja": "..."
            }
        ],
        "next_question": {
            "question_id": "...",
            "question_ja": "症状はどのくらい続いていますか？",
            "priority": 1
        },
        "session_summary": {...}
    }
    """
    try:
        data = request.get_json() or {}

        # パラメータを検証
        species = data.get("species", "dog").lower()
        if species not in SUPPORTED_SPECIES:
            return jsonify({
                "success": False,
                "error": f"サポートされていない種別：{species}",
            }), 400

        symptoms = data.get("symptoms", [])
        if not symptoms:
            return jsonify({
                "success": False,
                "error": "症状リストが空です",
            }), 400

        # セッションを取得または作成
        session_id = data.get("session_id")
        session = get_or_create_session(
            session_id=session_id,
            species=species,
            patient_name=data.get("patient_info", {}).get("name"),
            patient_age=data.get("patient_info", {}).get("age"),
            patient_weight=data.get("patient_info", {}).get("weight"),
        )

        # 患者コンテキストを更新
        if "patient_info" in data:
            session.patient_context.update(data["patient_info"])

        # 症状を検証
        valid_symptoms, invalid_symptoms = validate_symptoms_for_species(
            symptoms,
            species,
        )

        if not valid_symptoms:
            return jsonify({
                "success": False,
                "error": "有効な症状がありません",
                "invalid_symptoms": invalid_symptoms,
            }), 400

        # 症状を曖昧性解消
        disambiguated = []
        for symptom in valid_symptoms:
            disamb = disambiguate_symptom(symptom, species)
            disambiguated.append({
                "original": symptom,
                "normalized": disamb.normalized_symptom,
                "confidence": disamb.confidence,
                "severity_threshold": disamb.severity_threshold,
            })

            # セッションに症状を追加
            session.add_symptom(
                symptom_id=symptom,
                confidence=0.8,  # 仮の値、実際はより複雑な計算が必要
                severity="moderate",
            )

        # ユーザーメッセージを記録
        session.add_message(
            content=f"症状：{', '.join(valid_symptoms)}",
            role="user",
            message_type="symptom_report",
        )

        # 次のターンに進む
        session.next_turn()

        # ここで疾患候補を取得（簡略化、実際はより複雑）
        disease_candidates = [
            {
                "name": "Pancreatitis",
                "confidence": 0.7,
                "match_percent": 70,
                "explanation_ja": "嘔吐と疲労は膵炎と一致しています",
            },
            {
                "name": "Gastroenteritis",
                "confidence": 0.6,
                "match_percent": 60,
                "explanation_ja": "胃腸炎も同様の症状を示します",
            },
        ]

        # 種別固有のスコアリングを適用
        adjusted_diseases = disease_scorer.score_diseases_for_species(
            disease_candidates,
            valid_symptoms,
            species,
            context=session.get_species_specific_context(),
        )

        # 仮説を更新
        for disease in adjusted_diseases[:2]:
            session.update_disease_hypothesis(
                disease_name=disease.get("name", ""),
                confidence=disease.get("confidence", 0),
            )

        # 最適な次の質問を選択
        optimized_questions = question_optimizer.optimize_questions_for_species(
            adjusted_diseases,
            species,
            valid_symptoms,
            max_questions=1,
        )

        next_question = None
        if optimized_questions:
            q = optimized_questions[0]
            next_question = {
                "question_id": q.question_id,
                "question_ja": q.question_ja,
                "question_en": q.question_en,
                "priority": q.priority,
                "reasoning": q.reasoning,
            }

            # アシスタントメッセージを記録
            session.ask_question(
                question_id=q.question_id,
                question_text_ja=q.question_ja,
                question_text_en=q.question_en,
            )

        # セッションをキャッシュ・保存
        cache_session(session)
        session_manager.save_session(session, include_messages=True)

        return jsonify({
            "success": True,
            "session_id": session.session_id,
            "species": species,
            "turn": session.current_turn,
            "symptoms_validated": valid_symptoms,
            "symptoms_invalid": invalid_symptoms,
            "symptoms_disambiguated": disambiguated,
            "disease_candidates": adjusted_diseases,
            "next_question": next_question,
            "session_summary": {
                "total_questions": session.total_questions_asked,
                "total_symptoms": session.total_symptoms_detected,
            },
        }), 200

    except Exception as e:
        logger.exception(f"分析エラー：{e}")
        return jsonify({
            "success": False,
            "error": str(e),
        }), 500


@diagnostic_multi_bp.route("/next-question", methods=["POST"])
def get_next_question():
    """
    現在のセッション状態に基づいて次の質問を取得します。

    Request JSON:
    {
        "session_id": "...",
        "answer": "yes"  // 前の質問への回答（オプション）
    }

    Returns:
    {
        "success": true,
        "next_question": {...},
        "should_continue": true,
        "session_info": {...}
    }
    """
    try:
        data = request.get_json() or {}
        session_id = data.get("session_id")

        if not session_id:
            return jsonify({
                "success": False,
                "error": "session_id が必要です",
            }), 400

        # セッションを読み込む
        session = session_manager.load_session(session_id)
        if not session:
            return jsonify({
                "success": False,
                "error": "セッションが見つかりません",
            }), 404

        # 前の質問への回答を処理
        answer = data.get("answer")
        if answer:
            session.add_message(
                content=str(answer),
                role="user",
                message_type="answer",
            )

        # 診断を継続すべきか判定
        should_continue, reason = session.should_continue_diagnosis()

        if not should_continue:
            return jsonify({
                "success": True,
                "should_continue": False,
                "reason": reason,
                "is_complete": session.is_complete,
                "final_diagnosis": session.final_diagnosis,
                "confidence_score": session.confidence_score,
            }), 200

        # 次の質問を選択
        disease_candidates = [
            {
                "name": h.disease_name,
                "confidence": h.current_confidence,
            }
            for h in session.disease_hypotheses.values()
        ]

        optimized_questions = question_optimizer.optimize_questions_for_species(
            disease_candidates,
            session.species,
            list(session.detected_symptoms.keys()),
            max_questions=1,
        )

        next_question = None
        if optimized_questions:
            q = optimized_questions[0]
            next_question = {
                "question_id": q.question_id,
                "question_ja": q.question_ja,
                "question_en": q.question_en,
                "priority": q.priority,
            }

            session.ask_question(
                question_id=q.question_id,
                question_text_ja=q.question_ja,
                question_text_en=q.question_en,
            )

        session.next_turn()
        session_manager.save_session(session, include_messages=True)

        return jsonify({
            "success": True,
            "session_id": session.session_id,
            "turn": session.current_turn,
            "next_question": next_question,
            "should_continue": True,
            "disease_hypotheses": [
                {
                    "disease": h.disease_name,
                    "confidence": round(h.current_confidence, 3),
                }
                for h in session.disease_hypotheses.values()
            ],
        }), 200

    except Exception as e:
        logger.exception(f"質問取得エラー：{e}")
        return jsonify({
            "success": False,
            "error": str(e),
        }), 500


@diagnostic_multi_bp.route("/species-info", methods=["GET"])
def get_species_info():
    """
    種別の診断機能情報を取得します。

    Query Parameters:
    - species: 対象種別（オプション、指定なしならすべて）

    Returns:
    {
        "success": true,
        "species": {
            "dog": {
                "supported": true,
                "min_confidence_threshold": 0.25,
                "senior_age_threshold": 7,
                "...": "..."
            },
            ...
        }
    }
    """
    try:
        species_param = request.args.get("species", "").lower()

        species_info = {}

        if species_param and species_param in SUPPORTED_SPECIES:
            species_list = [species_param]
        else:
            species_list = sorted(SUPPORTED_SPECIES)

        for species in species_list:
            profile = disease_scorer.get_species_profile(species)
            species_info[species] = {
                "supported": True,
                "min_confidence_threshold": profile.get("min_confidence_threshold"),
                "prevalence_adjustment": profile.get("prevalence_adjustment"),
                "symptom_weight_multiplier": profile.get("symptom_weight_multiplier"),
                "senior_age_threshold": profile.get("senior_age_threshold"),
            }

        return jsonify({
            "success": True,
            "supported_species": len(SUPPORTED_SPECIES),
            "species": species_info,
        }), 200

    except Exception as e:
        logger.exception(f"種別情報取得エラー：{e}")
        return jsonify({
            "success": False,
            "error": str(e),
        }), 500


@diagnostic_multi_bp.route("/session/<session_id>", methods=["GET"])
def get_session_info(session_id: str):
    """
    セッション情報を取得します。

    Returns:
    {
        "success": true,
        "session": {...}
    }
    """
    try:
        session = session_manager.load_session(session_id)
        if not session:
            return jsonify({
                "success": False,
                "error": "セッションが見つかりません",
            }), 404

        return jsonify({
            "success": True,
            "session": session.get_session_summary(),
        }), 200

    except Exception as e:
        logger.exception(f"セッション情報取得エラー：{e}")
        return jsonify({
            "success": False,
            "error": str(e),
        }), 500


@diagnostic_multi_bp.route("/session/<session_id>", methods=["DELETE"])
def delete_session_endpoint(session_id: str):
    """
    セッションを削除します。

    Returns:
    {
        "success": true,
        "message": "セッションが削除されました"
    }
    """
    try:
        success = session_manager.delete_session(session_id)
        if success:
            return jsonify({
                "success": True,
                "message": "セッションが削除されました",
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": "セッションが見つかりません",
            }), 404

    except Exception as e:
        logger.exception(f"セッション削除エラー：{e}")
        return jsonify({
            "success": False,
            "error": str(e),
        }), 500
