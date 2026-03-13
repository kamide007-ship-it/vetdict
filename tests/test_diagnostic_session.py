import uuid

from api.ai.diagnostic_session import DiagnosticSession, DiagnosticSessionManager


def test_session_json_round_trip_restores_candidates_and_answers():
    session = DiagnosticSession.from_api_request(
        symptoms=["coughing", "fever"],
        suspected_diseases=[
            {"name": "Canine Influenza", "name_ja": "犬インフルエンザ", "match_percent": 78},
            {"name": "Kennel Cough", "name_ja": "ケンネルコフ", "match_percent": 64},
        ],
        detected_symptoms_ja="咳、発熱",
        detected_symptoms_en="Coughing, fever",
        species="dog",
        user_language="ja",
    )
    session.add_question_answer("duration", "3 days")

    restored = DiagnosticSession.from_json(session.to_json())

    assert restored is not None
    assert restored.current_candidates == session.current_candidates
    assert restored.initial_candidates == session.initial_candidates
    assert restored.answers == {"duration": "3 days"}
    assert restored.answer_timestamps["duration"] == session.answer_timestamps["duration"]
    assert restored.get_diagnosis_summary()["top_disease"] == "Canine Influenza"


def test_manager_loads_persisted_session_on_cache_miss(tmp_path):
    original_storage_dir = DiagnosticSessionManager._storage_dir
    original_sessions = DiagnosticSessionManager._sessions.copy()

    try:
        DiagnosticSessionManager._storage_dir = tmp_path
        DiagnosticSessionManager._sessions = {}

        session = DiagnosticSessionManager.create_session(
            symptoms=["vomiting"],
            suspected_diseases=[
                {"name": "Pancreatitis", "name_ja": "膵炎", "match_percent": 81},
            ],
            species="dog",
        )
        session_id = session.session_id

        DiagnosticSessionManager._sessions = {}

        reloaded = DiagnosticSessionManager.get_session(session_id)

        assert reloaded is not None
        assert reloaded.session_id == session_id
        assert reloaded.current_candidates == session.current_candidates
        assert reloaded.get_diagnosis_summary()["top_disease"] == "Pancreatitis"
    finally:
        DiagnosticSessionManager._storage_dir = original_storage_dir
        DiagnosticSessionManager._sessions = original_sessions


def test_manager_rejects_invalid_session_ids_without_touching_files(tmp_path):
    original_storage_dir = DiagnosticSessionManager._storage_dir
    original_sessions = DiagnosticSessionManager._sessions.copy()
    outside_file = tmp_path / "outside.json"
    outside_file.write_text("keep", encoding="utf-8")

    try:
        DiagnosticSessionManager._storage_dir = tmp_path / "sessions"
        DiagnosticSessionManager._sessions = {}

        assert DiagnosticSessionManager.get_session("../../outside") is None
        DiagnosticSessionManager.clear_session("../../outside")

        assert outside_file.read_text(encoding="utf-8") == "keep"
        assert not DiagnosticSessionManager._storage_dir.exists()
    finally:
        DiagnosticSessionManager._storage_dir = original_storage_dir
        DiagnosticSessionManager._sessions = original_sessions


def test_manager_clear_session_removes_persisted_file(tmp_path):
    original_storage_dir = DiagnosticSessionManager._storage_dir
    original_sessions = DiagnosticSessionManager._sessions.copy()

    try:
        DiagnosticSessionManager._storage_dir = tmp_path
        DiagnosticSessionManager._sessions = {}

        session = DiagnosticSessionManager.create_session(
            symptoms=["lethargy"],
            suspected_diseases=[
                {"name": "Anemia", "name_ja": "貧血", "match_percent": 55},
            ],
        )

        session_file = tmp_path / f"{uuid.UUID(session.session_id)}.json"
        assert session_file.exists()

        DiagnosticSessionManager.clear_session(session.session_id)

        assert DiagnosticSessionManager.get_session(session.session_id) is None
        assert not session_file.exists()
    finally:
        DiagnosticSessionManager._storage_dir = original_storage_dir
        DiagnosticSessionManager._sessions = original_sessions
