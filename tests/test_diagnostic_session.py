import pytest

from api.ai.diagnostic_session import DiagnosticSession, DiagnosticSessionManager


@pytest.fixture
def isolated_session_manager(tmp_path, monkeypatch):
    monkeypatch.setattr(DiagnosticSessionManager, "_storage_dir", tmp_path)
    monkeypatch.setattr(DiagnosticSessionManager, "_sessions", {})
    return DiagnosticSessionManager


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


def test_manager_loads_persisted_session_after_cache_clear(isolated_session_manager):
    session = isolated_session_manager.create_session(
        symptoms=["vomiting"],
        suspected_diseases=[
            {"name": "Pancreatitis", "name_ja": "膵炎", "match_percent": 81},
        ],
        species="dog",
    )
    session_id = session.session_id

    isolated_session_manager._sessions = {}

    reloaded = isolated_session_manager.get_session(session_id)

    assert reloaded is not None
    assert reloaded.session_id == session_id
    assert reloaded.current_candidates == session.current_candidates
    assert reloaded.get_diagnosis_summary()["top_disease"] == "Pancreatitis"


def test_manager_rejects_invalid_session_ids_without_touching_files(tmp_path, monkeypatch):
    monkeypatch.setattr(DiagnosticSessionManager, "_storage_dir", tmp_path / "sessions")
    monkeypatch.setattr(DiagnosticSessionManager, "_sessions", {})
    outside_file = tmp_path / "outside.json"
    outside_file.write_text("keep", encoding="utf-8")

    assert DiagnosticSessionManager.get_session("../../outside") is None
    DiagnosticSessionManager.clear_session("../../outside")

    assert outside_file.read_text(encoding="utf-8") == "keep"
    assert not DiagnosticSessionManager._storage_dir.exists()


def test_manager_clear_session_removes_persisted_file(isolated_session_manager):
    session = isolated_session_manager.create_session(
        symptoms=["lethargy"],
        suspected_diseases=[
            {"name": "Anemia", "name_ja": "貧血", "match_percent": 55},
        ],
    )

    session_file = isolated_session_manager._get_session_file_path(session.session_id)
    assert session_file.exists()

    isolated_session_manager.clear_session(session.session_id)

    assert isolated_session_manager.get_session(session.session_id) is None
    assert not session_file.exists()
