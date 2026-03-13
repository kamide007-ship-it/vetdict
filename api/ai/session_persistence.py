"""ステージ6：セッション永続化と復元管理

セッション状態をデータベース/ファイルに保存し、後で復元します。
"""

import json
import logging
from datetime import datetime
from typing import Any, Dict, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

from api.ai.multispecies_session import MultiSpeciesSession


class SessionPersistenceManager:
    """セッションの永続化と復元を管理"""

    def __init__(self, storage_dir: Optional[str] = None):
        """
        永続化マネージャーを初期化します。

        Args:
            storage_dir: セッションファイルの保存ディレクトリ
        """
        if storage_dir:
            self.storage_dir = Path(storage_dir)
            self.storage_dir.mkdir(parents=True, exist_ok=True)
        else:
            # デフォルト: プロジェクトの.sessions/ディレクトリ
            self.storage_dir = Path(".sessions")
            self.storage_dir.mkdir(parents=True, exist_ok=True)

    def save_session(
        self,
        session: MultiSpeciesSession,
        include_messages: bool = True,
    ) -> str:
        """
        セッションをファイルに保存します。

        Args:
            session: 保存するセッション
            include_messages: メッセージ履歴を含めるか

        Returns:
            保存されたファイルのパス
        """
        session_data = self._session_to_dict(session, include_messages)

        # ファイル名：session_id.json
        file_path = self.storage_dir / f"{session.session_id}.json"

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(session_data, f, ensure_ascii=False, indent=2)

            logger.info(f"セッション {session.session_id} を保存しました：{file_path}")
            return str(file_path)

        except Exception as e:
            logger.error(f"セッション保存エラー：{e}")
            raise

    def load_session(self, session_id: str) -> Optional[MultiSpeciesSession]:
        """
        ファイルからセッションを復元します。

        Args:
            session_id: セッションID

        Returns:
            復元されたMultiSpeciesSessionまたはNone
        """
        file_path = self.storage_dir / f"{session_id}.json"

        if not file_path.exists():
            logger.warning(f"セッションファイルが見つかりません：{file_path}")
            return None

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                session_data = json.load(f)

            session = self._dict_to_session(session_data)
            logger.info(f"セッション {session_id} を復元しました")
            return session

        except Exception as e:
            logger.error(f"セッション復元エラー：{e}")
            return None

    def delete_session(self, session_id: str) -> bool:
        """
        セッションファイルを削除します。

        Args:
            session_id: セッションID

        Returns:
            成功時True
        """
        file_path = self.storage_dir / f"{session_id}.json"

        try:
            if file_path.exists():
                file_path.unlink()
                logger.info(f"セッション {session_id} を削除しました")
                return True
            return False

        except Exception as e:
            logger.error(f"セッション削除エラー：{e}")
            return False

    def list_sessions(self) -> list:
        """
        保存されているすべてのセッションをリストします。

        Returns:
            セッションIDのリスト
        """
        sessions = []
        for file_path in self.storage_dir.glob("*.json"):
            session_id = file_path.stem
            sessions.append(session_id)

        return sorted(sessions)

    def get_session_metadata(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        セッションのメタデータを取得します。

        Args:
            session_id: セッションID

        Returns:
            メタデータの辞書またはNone
        """
        file_path = self.storage_dir / f"{session_id}.json"

        if not file_path.exists():
            return None

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # セッション情報のみを抽出
            session_info = data.get("session_summary", {})
            return {
                "session_id": session_info.get("session_id"),
                "species": session_info.get("species"),
                "patient_name": session_info.get("patient_name"),
                "created_at": session_info.get("created_at"),
                "last_updated": session_info.get("last_updated"),
                "is_complete": session_info.get("is_complete"),
                "final_diagnosis": session_info.get("final_diagnosis"),
                "confidence_score": session_info.get("confidence_score"),
            }

        except Exception as e:
            logger.error(f"メタデータ取得エラー：{e}")
            return None

    def export_session_for_sharing(
        self,
        session_id: str,
        include_sensitive: bool = False,
    ) -> Optional[str]:
        """
        セッションを共有可能な形式でエクスポートします。

        Args:
            session_id: セッションID
            include_sensitive: 患者名などの機密情報を含めるか

        Returns:
            JSON文字列またはNone
        """
        file_path = self.storage_dir / f"{session_id}.json"

        if not file_path.exists():
            return None

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            # 機密情報を削除
            if not include_sensitive:
                session = data.get("session_summary", {})
                session.pop("patient_name", None)

            return json.dumps(data, ensure_ascii=False, indent=2)

        except Exception as e:
            logger.error(f"エクスポートエラー：{e}")
            return None

    @staticmethod
    def _session_to_dict(
        session: MultiSpeciesSession,
        include_messages: bool = True,
    ) -> Dict[str, Any]:
        """
        セッションを辞書に変換します。

        Args:
            session: セッションオブジェクト
            include_messages: メッセージを含めるか

        Returns:
            セッションデータの辞書
        """
        data = {
            "version": "1.0",
            "exported_at": datetime.now().isoformat(),
            "session_summary": session.get_session_summary(),
        }

        if include_messages:
            data["messages"] = [
                {
                    "id": m.message_id,
                    "timestamp": m.timestamp.isoformat(),
                    "role": m.role,
                    "content": m.content,
                    "type": m.message_type,
                    "metadata": m.metadata,
                }
                for m in session.messages
            ]

        return data

    @staticmethod
    def _dict_to_session(data: Dict[str, Any]) -> MultiSpeciesSession:
        """
        辞書からセッションを復元します。

        Args:
            data: セッションデータの辞書

        Returns:
            MultiSpeciesSessionオブジェクト
        """
        summary = data.get("session_summary", {})

        # 基本セッションを作成
        session = MultiSpeciesSession(
            session_id=summary.get("session_id"),
            species=summary.get("species", "dog"),
            patient_name=summary.get("patient_name"),
            patient_age=summary.get("patient_age"),
            patient_weight=summary.get("patient_weight"),
        )

        # セッション状態を復元
        session.is_complete = summary.get("is_complete", False)
        session.final_diagnosis = summary.get("final_diagnosis")
        session.confidence_score = summary.get("confidence_score", 0.0)
        session.current_turn = summary.get("current_turn", 0)

        # 症状を復元
        for symptom_id, s_data in summary.get("detected_symptoms", {}).items():
            session.detected_symptoms[symptom_id] = {
                "symptom_id": s_data.get("symptom_id"),
                "detected_at_turn": s_data.get("detected_at_turn"),
                "confidence": s_data.get("confidence"),
                "severity": s_data.get("severity"),
            }

        # 疾患仮説を復元
        for d_name, d_data in summary.get("disease_hypotheses", {}).items():
            session.disease_hypotheses[d_name] = {
                "disease_name": d_name,
                "first_suggested_at_turn": d_data.get("first_suggested_at_turn"),
                "current_confidence": d_data.get("current_confidence"),
                "confidence_history": d_data.get("confidence_history", []),
            }

        # メッセージ履歴を復元
        for msg_data in data.get("messages", []):
            session.add_message(
                content=msg_data.get("content", ""),
                role=msg_data.get("role", "user"),
                message_type=msg_data.get("type", "general"),
                metadata=msg_data.get("metadata", {}),
            )

        return session


class SessionCache:
    """メモリ内のセッションキャッシュ"""

    def __init__(self, max_sessions: int = 100):
        """
        セッションキャッシュを初期化します。

        Args:
            max_sessions: キャッシュする最大セッション数
        """
        self.cache: Dict[str, MultiSpeciesSession] = {}
        self.max_sessions = max_sessions
        self.access_times: Dict[str, datetime] = {}

    def put(self, session: MultiSpeciesSession) -> None:
        """
        セッションをキャッシュに保存します。

        Args:
            session: 保存するセッション
        """
        # キャッシュサイズを超えた場合は古いセッションを削除
        if len(self.cache) >= self.max_sessions:
            oldest_id = min(
                self.access_times.items(),
                key=lambda x: x[1],
            )[0]
            self.cache.pop(oldest_id, None)
            self.access_times.pop(oldest_id, None)

        self.cache[session.session_id] = session
        self.access_times[session.session_id] = datetime.now()

    def get(self, session_id: str) -> Optional[MultiSpeciesSession]:
        """
        キャッシュからセッションを取得します。

        Args:
            session_id: セッションID

        Returns:
            キャッシュされたセッションまたはNone
        """
        session = self.cache.get(session_id)
        if session:
            self.access_times[session_id] = datetime.now()
        return session

    def remove(self, session_id: str) -> None:
        """
        セッションをキャッシュから削除します。

        Args:
            session_id: セッションID
        """
        self.cache.pop(session_id, None)
        self.access_times.pop(session_id, None)

    def clear(self) -> None:
        """キャッシュをクリアします"""
        self.cache.clear()
        self.access_times.clear()

    def size(self) -> int:
        """
        キャッシュサイズを取得します。

        Returns:
            キャッシュされたセッション数
        """
        return len(self.cache)


# グローバルなセッションキャッシュ
_session_cache = SessionCache()


def get_or_create_session(
    session_id: Optional[str] = None,
    species: str = "dog",
    **kwargs,
) -> MultiSpeciesSession:
    """
    セッションを取得または作成します。

    Args:
        session_id: セッションID（Noneなら新規作成）
        species: 動物種
        **kwargs: MultiSpeciesSessionのその他のパラメータ

    Returns:
        MultiSpeciesSession
    """
    if session_id:
        # キャッシュから取得を試みる
        session = _session_cache.get(session_id)
        if session:
            return session

    # 新規セッションを作成
    session = MultiSpeciesSession(
        session_id=session_id,
        species=species,
        **kwargs,
    )

    _session_cache.put(session)
    return session


def cache_session(session: MultiSpeciesSession) -> None:
    """
    セッションをキャッシュに保存します。

    Args:
        session: セッション
    """
    _session_cache.put(session)
