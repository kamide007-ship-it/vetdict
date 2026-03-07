"""
Comprehensive tests for the 24-hour auto-cycle analysis engine (api/auto_cycle.py).

Tests cover:
- load_cycle_state / save_cycle_state -- state persistence with mocked file paths
- load_breed_calibration / save_breed_calibration -- calibration persistence
- aggregate_by_breed -- statistical aggregation of analysis records
- get_evidence_based_gait_params -- uses 'axis_scores' key (was fixed from 'expected_scores')
- get_evidence_based_disease_params -- breed-disease mapping and categorisation
- REFERENCE_CASES data integrity -- required fields on every reference case
- append_cycle_log -- history log appending
- apply_calibration_to_analysis -- calibration offset application
- calibrate_against_fci -- FCI calibration drift detection
- should_run_cycle / run_cycle / try_auto_cycle -- cycle orchestration
- get_breed_fci_params -- FCI parameter extraction from breed descriptions
- collect_recent_analyses -- database collection (mocked)
- _ensure_data_dir -- directory creation utility
"""

import json
import sys
import time
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# Ensure repo root is importable
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import api.auto_cycle as ac


# ============================================================================
# Fixtures
# ============================================================================


@pytest.fixture(autouse=True)
def _isolate_data_dir(tmp_path, monkeypatch):
    """Redirect all auto_cycle file I/O to a temporary directory.

    Patches the module-level path constants so that every test gets its
    own clean data directory without touching the real filesystem.
    """
    data_dir = tmp_path / "cycle_data"
    data_dir.mkdir()

    monkeypatch.setattr(ac, "CYCLE_DATA_DIR", data_dir)
    monkeypatch.setattr(ac, "CYCLE_STATE_PATH", data_dir / "cycle_state.json")
    monkeypatch.setattr(ac, "CYCLE_HISTORY_PATH", data_dir / "cycle_history.jsonl")
    monkeypatch.setattr(ac, "BREED_CALIBRATION_PATH", data_dir / "breed_calibration.json")


# ============================================================================
# Helper to simulate import failures
# ============================================================================


def _import_error_for(module_name):
    """Return an __import__ side_effect that fails only for *module_name*."""
    _real_import = __import__

    def _fake_import(name, *args, **kwargs):
        if name == module_name:
            raise ImportError(f"Mocked import failure for {name}")
        return _real_import(name, *args, **kwargs)

    return _fake_import


# ============================================================================
# load_cycle_state / save_cycle_state
# ============================================================================


class TestCycleStatePersistence:
    """State is round-tripped through JSON correctly."""

    def test_load_returns_default_when_no_file(self):
        state = ac.load_cycle_state()
        assert state == {
            "last_cycle_ts": 0,
            "total_cycles": 0,
            "total_analyses_processed": 0,
            "breed_stats": {},
        }

    def test_save_then_load_roundtrip(self):
        expected = {
            "last_cycle_ts": 1700000000,
            "total_cycles": 5,
            "total_analyses_processed": 42,
            "breed_stats": {"labrador": {"count": 10}},
        }
        ac.save_cycle_state(expected)
        loaded = ac.load_cycle_state()
        assert loaded == expected

    def test_save_uses_atomic_replace(self):
        """The tmp-then-rename pattern should leave no .tmp artefact."""
        ac.save_cycle_state({"last_cycle_ts": 1})
        tmp_file = Path(str(ac.CYCLE_STATE_PATH) + ".tmp")
        assert not tmp_file.exists()
        assert ac.CYCLE_STATE_PATH.exists()

    def test_load_handles_corrupted_file(self):
        """Corrupted JSON falls back to defaults."""
        ac.CYCLE_STATE_PATH.write_text("NOT VALID JSON {{{", encoding="utf-8")
        state = ac.load_cycle_state()
        assert state["last_cycle_ts"] == 0
        assert state["total_cycles"] == 0

    def test_save_preserves_unicode(self):
        expected = {
            "last_cycle_ts": 0,
            "total_cycles": 0,
            "total_analyses_processed": 0,
            "breed_stats": {},
            "note": "日本語テスト",
        }
        ac.save_cycle_state(expected)
        loaded = ac.load_cycle_state()
        assert loaded["note"] == "日本語テスト"

    def test_save_creates_data_dir_if_missing(self, tmp_path, monkeypatch):
        """_ensure_data_dir creates the directory tree."""
        nested = tmp_path / "deep" / "nested" / "dir"
        monkeypatch.setattr(ac, "CYCLE_DATA_DIR", nested)
        monkeypatch.setattr(ac, "CYCLE_STATE_PATH", nested / "cycle_state.json")
        ac.save_cycle_state({
            "last_cycle_ts": 0, "total_cycles": 0,
            "total_analyses_processed": 0, "breed_stats": {},
        })
        assert nested.exists()
        assert (nested / "cycle_state.json").exists()

    def test_load_creates_data_dir_if_missing(self, tmp_path, monkeypatch):
        nested = tmp_path / "nonexistent" / "dir"
        monkeypatch.setattr(ac, "CYCLE_DATA_DIR", nested)
        monkeypatch.setattr(ac, "CYCLE_STATE_PATH", nested / "cycle_state.json")
        state = ac.load_cycle_state()
        assert nested.exists()
        assert state["last_cycle_ts"] == 0

    def test_overwrite_replaces_previous_state(self):
        ac.save_cycle_state({"last_cycle_ts": 1, "total_cycles": 1,
                             "total_analyses_processed": 0, "breed_stats": {}})
        ac.save_cycle_state({"last_cycle_ts": 2, "total_cycles": 2,
                             "total_analyses_processed": 0, "breed_stats": {}})
        loaded = ac.load_cycle_state()
        assert loaded["last_cycle_ts"] == 2
        assert loaded["total_cycles"] == 2


# ============================================================================
# load_breed_calibration / save_breed_calibration
# ============================================================================


class TestBreedCalibrationPersistence:
    """Breed calibration data is persisted correctly."""

    def test_load_returns_empty_dict_when_no_file(self):
        cal = ac.load_breed_calibration()
        assert cal == {}

    def test_save_then_load_roundtrip(self):
        expected = {
            "172d_poodle_toy": {
                "breed_id": "172d_poodle_toy",
                "sample_size": 10,
                "adjustments": {"structure": {"offset": -2.5}},
            }
        }
        ac.save_breed_calibration(expected)
        loaded = ac.load_breed_calibration()
        assert loaded == expected

    def test_save_uses_atomic_replace(self):
        ac.save_breed_calibration({"a": 1})
        tmp_file = Path(str(ac.BREED_CALIBRATION_PATH) + ".tmp")
        assert not tmp_file.exists()
        assert ac.BREED_CALIBRATION_PATH.exists()

    def test_load_handles_corrupted_file(self):
        ac.BREED_CALIBRATION_PATH.write_text("CORRUPTED", encoding="utf-8")
        cal = ac.load_breed_calibration()
        assert cal == {}

    def test_save_preserves_unicode_in_calibration(self):
        data = {
            "breed_x": {
                "adjustments": {"structure": {"reason": "FCI基準との乖離補正"}}
            }
        }
        ac.save_breed_calibration(data)
        loaded = ac.load_breed_calibration()
        assert loaded["breed_x"]["adjustments"]["structure"]["reason"] == "FCI基準との乖離補正"

    def test_overwrite_replaces_previous(self):
        ac.save_breed_calibration({"v1": True})
        ac.save_breed_calibration({"v2": True})
        loaded = ac.load_breed_calibration()
        assert "v1" not in loaded
        assert loaded["v2"] is True


# ============================================================================
# append_cycle_log
# ============================================================================


class TestAppendCycleLog:
    """History log is appended correctly as JSONL."""

    def test_single_entry(self):
        entry = {"status": "completed", "cycle": 1}
        ac.append_cycle_log(entry)
        text = ac.CYCLE_HISTORY_PATH.read_text(encoding="utf-8")
        lines = text.strip().split("\n")
        assert len(lines) == 1
        assert json.loads(lines[0]) == entry

    def test_multiple_entries_appended(self):
        ac.append_cycle_log({"cycle": 1})
        ac.append_cycle_log({"cycle": 2})
        ac.append_cycle_log({"cycle": 3})
        text = ac.CYCLE_HISTORY_PATH.read_text(encoding="utf-8")
        lines = text.strip().split("\n")
        assert len(lines) == 3
        assert json.loads(lines[0])["cycle"] == 1
        assert json.loads(lines[2])["cycle"] == 3

    def test_unicode_in_log(self):
        ac.append_cycle_log({"note": "サイクル完了"})
        text = ac.CYCLE_HISTORY_PATH.read_text(encoding="utf-8")
        assert "サイクル完了" in text


# ============================================================================
# aggregate_by_breed
# ============================================================================


class TestAggregateByBreed:
    """Statistical aggregation of analysis records by breed."""

    @staticmethod
    def _make_analysis(breed_id, overall=80, structure=75,
                       coat=70, gait=85, temperament=90):
        return {
            "breed_id": breed_id,
            "overall_score": overall,
            "structure_score": structure,
            "coat_score": coat,
            "gait_score": gait,
            "temperament_score": temperament,
        }

    def test_empty_input_returns_empty(self):
        result = ac.aggregate_by_breed([])
        assert result == {}

    def test_single_breed_single_record(self):
        analyses = [self._make_analysis("poodle", overall=80, structure=75,
                                        coat=70, gait=85, temperament=90)]
        result = ac.aggregate_by_breed(analyses)
        assert "poodle" in result
        stats = result["poodle"]
        assert stats["count"] == 1
        assert stats["overall"]["mean"] == 80.0
        assert stats["overall"]["n"] == 1

    def test_single_breed_multiple_records(self):
        analyses = [
            self._make_analysis("lab", overall=80, structure=70,
                                coat=60, gait=90, temperament=85),
            self._make_analysis("lab", overall=90, structure=80,
                                coat=70, gait=95, temperament=90),
        ]
        result = ac.aggregate_by_breed(analyses)
        stats = result["lab"]
        assert stats["count"] == 2
        assert stats["overall"]["mean"] == 85.0
        assert stats["overall"]["min"] == 80.0
        assert stats["overall"]["max"] == 90.0
        assert stats["overall"]["n"] == 2

    def test_multiple_breeds_separated(self):
        analyses = [
            self._make_analysis("poodle", overall=80),
            self._make_analysis("labrador", overall=90),
            self._make_analysis("poodle", overall=70),
        ]
        result = ac.aggregate_by_breed(analyses)
        assert set(result.keys()) == {"poodle", "labrador"}
        assert result["poodle"]["count"] == 2
        assert result["labrador"]["count"] == 1

    def test_missing_breed_id_uses_unknown(self):
        analyses = [{"overall_score": 50}]
        result = ac.aggregate_by_breed(analyses)
        assert "unknown" in result
        assert result["unknown"]["count"] == 1

    def test_none_scores_are_skipped(self):
        analyses = [{
            "breed_id": "poodle",
            "overall_score": None,
            "structure_score": 80,
            "coat_score": None,
            "gait_score": 70,
            "temperament_score": None,
        }]
        result = ac.aggregate_by_breed(analyses)
        stats = result["poodle"]
        assert stats["count"] == 1
        assert stats["overall"] is None
        assert stats["structure"]["mean"] == 80.0
        assert stats["coat"] is None
        assert stats["gait"]["mean"] == 70.0
        assert stats["temperament"] is None

    def test_missing_score_keys_treated_as_none(self):
        analyses = [{"breed_id": "x"}]  # no score keys at all
        result = ac.aggregate_by_breed(analyses)
        stats = result["x"]
        assert stats["count"] == 1
        for key in ("overall", "structure", "coat", "gait", "temperament"):
            assert stats[key] is None

    def test_std_is_zero_for_identical_scores(self):
        analyses = [
            self._make_analysis("poodle", overall=80),
            self._make_analysis("poodle", overall=80),
            self._make_analysis("poodle", overall=80),
        ]
        result = ac.aggregate_by_breed(analyses)
        assert result["poodle"]["overall"]["std"] == 0.0

    def test_result_contains_all_stat_keys(self):
        analyses = [self._make_analysis("poodle")]
        result = ac.aggregate_by_breed(analyses)
        for component in ("overall", "structure", "coat", "gait", "temperament"):
            comp_stats = result["poodle"][component]
            assert comp_stats is not None
            assert set(comp_stats.keys()) == {"mean", "std", "min", "max", "n"}

    def test_mean_calculation_accuracy(self):
        analyses = [
            self._make_analysis("a", overall=60),
            self._make_analysis("a", overall=70),
            self._make_analysis("a", overall=80),
            self._make_analysis("a", overall=90),
        ]
        result = ac.aggregate_by_breed(analyses)
        assert result["a"]["overall"]["mean"] == 75.0
        assert result["a"]["overall"]["min"] == 60.0
        assert result["a"]["overall"]["max"] == 90.0
        assert result["a"]["overall"]["n"] == 4


# ============================================================================
# get_evidence_based_gait_params -- uses 'axis_scores' key
# ============================================================================


class TestGetEvidenceBasedGaitParams:
    """Gait params are correctly derived from REFERENCE_CASES using axis_scores."""

    def test_breed_with_reference_data(self):
        """Toy Poodle (172d_poodle_toy) exists in REFERENCE_CASES."""
        with patch.object(ac, "load_breed_calibration", return_value={}):
            params = ac.get_evidence_based_gait_params("172d_poodle_toy")
        assert params["has_reference_data"] is True
        assert params["reference_count"] >= 1
        assert "expected_gait_mean" in params
        assert "expected_gait_std" in params
        assert "expected_gait_range" in params

    def test_breed_without_reference_data(self):
        """Unknown breed returns no reference data."""
        with patch.object(ac, "load_breed_calibration", return_value={}):
            params = ac.get_evidence_based_gait_params("999_nonexistent_breed")
        assert params["has_reference_data"] is False
        assert params["reference_count"] == 0
        assert "expected_gait_mean" not in params

    def test_axis_scores_key_is_used_not_expected_scores(self):
        """Regression test: code was fixed from 'expected_scores' to 'axis_scores'.

        We mock REFERENCE_CASES with both keys to prove only axis_scores is read.
        """
        fake_cases = [
            {
                "breed_id": "test_breed",
                "axis_scores": {"gait": 88},
                # Old key that must NOT be read
                "expected_scores": {"gait": 50},
            }
        ]
        with patch("api.reference_dataset.REFERENCE_CASES", fake_cases), \
             patch.object(ac, "load_breed_calibration", return_value={}):
            params = ac.get_evidence_based_gait_params("test_breed")

        assert params["has_reference_data"] is True
        # Must use axis_scores value (88), NOT expected_scores (50)
        assert params["expected_gait_mean"] == 88.0

    def test_reference_case_without_gait_in_axis_scores(self):
        """A reference case may not have a gait key in axis_scores."""
        fake_cases = [
            {
                "breed_id": "test_breed",
                "axis_scores": {"skeletal": 90},  # no 'gait' key
            }
        ]
        with patch("api.reference_dataset.REFERENCE_CASES", fake_cases), \
             patch.object(ac, "load_breed_calibration", return_value={}):
            params = ac.get_evidence_based_gait_params("test_breed")

        assert params["has_reference_data"] is True
        assert params["reference_count"] == 1
        assert "expected_gait_mean" not in params

    def test_calibration_offset_is_included(self):
        """If breed calibration has a gait offset, it should be returned."""
        cal_data = {
            "172d_poodle_toy": {
                "adjustments": {"gait": {"offset": -3.5}}
            }
        }
        with patch.object(ac, "load_breed_calibration", return_value=cal_data):
            params = ac.get_evidence_based_gait_params("172d_poodle_toy")
        assert params["calibration_offset"] == -3.5

    def test_no_calibration_offset_when_absent(self):
        with patch.object(ac, "load_breed_calibration", return_value={}):
            params = ac.get_evidence_based_gait_params("172d_poodle_toy")
        assert "calibration_offset" not in params

    def test_multiple_reference_cases_aggregated(self):
        """Multiple reference cases for same breed should be aggregated."""
        fake_cases = [
            {"breed_id": "test_breed", "axis_scores": {"gait": 80}},
            {"breed_id": "test_breed", "axis_scores": {"gait": 90}},
        ]
        with patch("api.reference_dataset.REFERENCE_CASES", fake_cases), \
             patch.object(ac, "load_breed_calibration", return_value={}):
            params = ac.get_evidence_based_gait_params("test_breed")

        assert params["reference_count"] == 2
        assert params["expected_gait_mean"] == 85.0
        assert params["expected_gait_range"] == (80.0, 90.0)

    def test_gait_range_with_single_case(self):
        """Range min and max should be equal for a single reference case."""
        fake_cases = [
            {"breed_id": "test_breed", "axis_scores": {"gait": 75}},
        ]
        with patch("api.reference_dataset.REFERENCE_CASES", fake_cases), \
             patch.object(ac, "load_breed_calibration", return_value={}):
            params = ac.get_evidence_based_gait_params("test_breed")

        assert params["expected_gait_range"] == (75.0, 75.0)
        assert params["expected_gait_std"] == 0.0

    def test_reference_cases_not_imported_gracefully(self):
        """If api.reference_dataset cannot be imported, use empty list."""
        with patch("builtins.__import__",
                   side_effect=_import_error_for("api.reference_dataset")), \
             patch.object(ac, "load_breed_calibration", return_value={}):
            params = ac.get_evidence_based_gait_params("test_breed")
        assert params["has_reference_data"] is False
        assert params["reference_count"] == 0

    def test_all_real_reference_cases_use_axis_scores(self):
        """Verify that every real reference case uses 'axis_scores', not
        the old 'expected_scores' key."""
        from api.reference_dataset import REFERENCE_CASES
        for case in REFERENCE_CASES:
            assert "axis_scores" in case, (
                f"Case {case['id']} missing 'axis_scores'"
            )
            assert "expected_scores" not in case, (
                f"Case {case['id']} has obsolete 'expected_scores' key"
            )


# ============================================================================
# get_evidence_based_disease_params
# ============================================================================


class TestGetEvidenceBasedDiseaseParams:
    """Disease risk parameters are correctly derived from BREED_DATA."""

    @staticmethod
    def _mock_breed_data(diseases):
        return {"test_breed": {"hereditary_diseases": diseases}}

    def test_breed_with_diseases(self):
        diseases = ["股関節形成不全", "進行性網膜萎縮症", "心臓弁膜症"]
        with patch("api.breeds.BREED_DATA", self._mock_breed_data(diseases)):
            result = ac.get_evidence_based_disease_params("test_breed")

        assert result["breed_id"] == "test_breed"
        assert result["total_known_risks"] == 3
        assert result["hereditary_diseases"] == diseases

    def test_breed_without_diseases(self):
        with patch("api.breeds.BREED_DATA",
                   {"test_breed": {"hereditary_diseases": []}}):
            result = ac.get_evidence_based_disease_params("test_breed")
        assert result["total_known_risks"] == 0
        assert result["overall_risk_level"] == "low"

    def test_unknown_breed(self):
        with patch("api.breeds.BREED_DATA", {}):
            result = ac.get_evidence_based_disease_params("unknown_breed")
        assert result["breed_id"] == "unknown_breed"
        assert result["total_known_risks"] == 0
        assert result["hereditary_diseases"] == []

    # ---- Disease categorisation by body system ----

    def test_orthopedic_categorisation(self):
        diseases = ["股関節形成不全", "膝蓋骨脱臼", "肘関節形成不全"]
        with patch("api.breeds.BREED_DATA", self._mock_breed_data(diseases)):
            result = ac.get_evidence_based_disease_params("test_breed")
        assert len(result["by_system"]["orthopedic"]) == 3

    def test_ophthalmologic_categorisation(self):
        diseases = ["進行性網膜萎縮症", "白内障", "緑内障"]
        with patch("api.breeds.BREED_DATA", self._mock_breed_data(diseases)):
            result = ac.get_evidence_based_disease_params("test_breed")
        assert len(result["by_system"]["ophthalmologic"]) == 3

    def test_cardiac_categorisation(self):
        diseases = ["大動脈弁下狭窄症（SAS）", "心臓弁膜症"]
        with patch("api.breeds.BREED_DATA", self._mock_breed_data(diseases)):
            result = ac.get_evidence_based_disease_params("test_breed")
        assert len(result["by_system"]["cardiac"]) == 2

    def test_neurological_categorisation(self):
        diseases = ["てんかん", "変性性脊髄症"]
        with patch("api.breeds.BREED_DATA", self._mock_breed_data(diseases)):
            result = ac.get_evidence_based_disease_params("test_breed")
        assert len(result["by_system"]["neurological"]) == 2

    def test_dermatological_categorisation(self):
        diseases = ["脂腺炎", "アトピー性皮膚炎"]
        with patch("api.breeds.BREED_DATA", self._mock_breed_data(diseases)):
            result = ac.get_evidence_based_disease_params("test_breed")
        assert len(result["by_system"]["dermatological"]) == 2

    def test_uncategorised_goes_to_other(self):
        diseases = ["運動誘発性虚脱（EIC）", "気管虚脱"]
        with patch("api.breeds.BREED_DATA", self._mock_breed_data(diseases)):
            result = ac.get_evidence_based_disease_params("test_breed")
        assert len(result["by_system"]["other"]) == 2

    def test_mixed_system_categorisation(self):
        """Diseases across multiple systems are correctly separated."""
        diseases = [
            "股関節形成不全",       # orthopedic
            "進行性網膜萎縮症",     # ophthalmologic
            "心臓弁膜症",          # cardiac
            "てんかん",             # neurological
            "アトピー性皮膚炎",     # dermatological
            "気管虚脱",             # other
        ]
        with patch("api.breeds.BREED_DATA", self._mock_breed_data(diseases)):
            result = ac.get_evidence_based_disease_params("test_breed")
        by_sys = result["by_system"]
        assert len(by_sys["orthopedic"]) == 1
        assert len(by_sys["ophthalmologic"]) == 1
        assert len(by_sys["cardiac"]) == 1
        assert len(by_sys["neurological"]) == 1
        assert len(by_sys["dermatological"]) == 1
        assert len(by_sys["other"]) == 1

    # ---- Risk level thresholds ----

    def test_risk_level_low(self):
        diseases = ["膝蓋骨脱臼", "白内障"]
        with patch("api.breeds.BREED_DATA", self._mock_breed_data(diseases)):
            result = ac.get_evidence_based_disease_params("test_breed")
        assert result["overall_risk_level"] == "low"

    def test_risk_level_moderate(self):
        diseases = ["膝蓋骨脱臼", "白内障", "心臓弁膜症"]
        with patch("api.breeds.BREED_DATA", self._mock_breed_data(diseases)):
            result = ac.get_evidence_based_disease_params("test_breed")
        assert result["overall_risk_level"] == "moderate"

    def test_risk_level_high(self):
        diseases = ["d1", "d2", "d3", "d4", "d5", "d6"]
        with patch("api.breeds.BREED_DATA", self._mock_breed_data(diseases)):
            result = ac.get_evidence_based_disease_params("test_breed")
        assert result["overall_risk_level"] == "high"

    def test_risk_level_boundary_exactly_3(self):
        """3 diseases => moderate."""
        diseases = ["a", "b", "c"]
        with patch("api.breeds.BREED_DATA", self._mock_breed_data(diseases)):
            result = ac.get_evidence_based_disease_params("test_breed")
        assert result["overall_risk_level"] == "moderate"

    def test_risk_level_boundary_exactly_6(self):
        """6 diseases => high."""
        diseases = ["a", "b", "c", "d", "e", "f"]
        with patch("api.breeds.BREED_DATA", self._mock_breed_data(diseases)):
            result = ac.get_evidence_based_disease_params("test_breed")
        assert result["overall_risk_level"] == "high"

    def test_risk_level_boundary_5_is_moderate(self):
        """5 diseases => still moderate (< 6)."""
        diseases = ["a", "b", "c", "d", "e"]
        with patch("api.breeds.BREED_DATA", self._mock_breed_data(diseases)):
            result = ac.get_evidence_based_disease_params("test_breed")
        assert result["overall_risk_level"] == "moderate"

    def test_risk_level_zero_is_low(self):
        with patch("api.breeds.BREED_DATA", self._mock_breed_data([])):
            result = ac.get_evidence_based_disease_params("test_breed")
        assert result["overall_risk_level"] == "low"

    # ---- Structural checks ----

    def test_all_system_keys_present(self):
        with patch("api.breeds.BREED_DATA", {"b": {"hereditary_diseases": []}}):
            result = ac.get_evidence_based_disease_params("b")
        expected_keys = {"orthopedic", "ophthalmologic", "cardiac",
                         "neurological", "dermatological", "other"}
        assert set(result["by_system"].keys()) == expected_keys

    def test_import_error_returns_empty_profile(self):
        """If api.breeds cannot be imported, return empty disease profile."""
        with patch("builtins.__import__",
                   side_effect=_import_error_for("api.breeds")):
            result = ac.get_evidence_based_disease_params("test_breed")
        assert result["total_known_risks"] == 0
        assert result["hereditary_diseases"] == []

    def test_disease_only_counted_in_first_matching_category(self):
        """A disease should appear in exactly one category, not multiple."""
        # "椎間板ヘルニア" matches orthopedic (椎間板), should NOT also appear elsewhere
        diseases = ["椎間板ヘルニア"]
        with patch("api.breeds.BREED_DATA", self._mock_breed_data(diseases)):
            result = ac.get_evidence_based_disease_params("test_breed")
        by_sys = result["by_system"]
        total_categorised = sum(len(v) for v in by_sys.values())
        assert total_categorised == 1


# ============================================================================
# REFERENCE_CASES data integrity
# ============================================================================


class TestReferenceCasesIntegrity:
    """Every reference case must have the required fields and structure."""

    @pytest.fixture()
    def reference_cases(self):
        from api.reference_dataset import REFERENCE_CASES
        return REFERENCE_CASES

    REQUIRED_TOP_LEVEL_FIELDS = {
        "id", "description", "source", "breed_id", "age_years",
        "expected_fci_grade", "expected_showdog_grade", "expected_score_range",
        "axis_scores",
    }

    REQUIRED_AXIS_KEYS = {"skeletal", "gait", "muscle", "coat", "temperament"}

    VALID_FCI_GRADES = {"Excellent", "Very Good", "Good", "Sufficient",
                        "Very Promising"}

    VALID_SHOWDOG_GRADES = {"S", "A+", "A", "B+", "B", "C"}

    def test_cases_list_is_non_empty(self, reference_cases):
        assert len(reference_cases) > 0

    def test_all_cases_have_required_fields(self, reference_cases):
        for case in reference_cases:
            missing = self.REQUIRED_TOP_LEVEL_FIELDS - set(case.keys())
            assert missing == set(), (
                f"Case {case.get('id', '???')} missing fields: {missing}"
            )

    def test_all_cases_have_unique_ids(self, reference_cases):
        ids = [c["id"] for c in reference_cases]
        assert len(ids) == len(set(ids)), "Duplicate reference case IDs found"

    def test_all_axis_scores_have_required_keys(self, reference_cases):
        for case in reference_cases:
            axis = case["axis_scores"]
            missing = self.REQUIRED_AXIS_KEYS - set(axis.keys())
            assert missing == set(), (
                f"Case {case['id']} axis_scores missing keys: {missing}"
            )

    def test_axis_scores_are_numeric_and_in_range(self, reference_cases):
        for case in reference_cases:
            for key, value in case["axis_scores"].items():
                assert isinstance(value, (int, float)), (
                    f"Case {case['id']} axis_scores[{key}] not numeric: {value}"
                )
                assert 0 <= value <= 100, (
                    f"Case {case['id']} axis_scores[{key}]={value} out of range"
                )

    def test_expected_score_range_is_valid(self, reference_cases):
        for case in reference_cases:
            rng = case["expected_score_range"]
            assert isinstance(rng, (tuple, list)) and len(rng) == 2, (
                f"Case {case['id']} expected_score_range not a 2-element sequence"
            )
            lo, hi = rng
            assert lo <= hi, (
                f"Case {case['id']} expected_score_range lo={lo} > hi={hi}"
            )

    def test_age_years_is_positive(self, reference_cases):
        for case in reference_cases:
            assert case["age_years"] > 0, (
                f"Case {case['id']} age_years={case['age_years']} not positive"
            )

    def test_fci_grades_are_valid(self, reference_cases):
        for case in reference_cases:
            grade = case["expected_fci_grade"]
            assert grade in self.VALID_FCI_GRADES, (
                f"Case {case['id']} unexpected FCI grade: {grade}"
            )

    def test_showdog_grades_are_valid(self, reference_cases):
        for case in reference_cases:
            grade = case["expected_showdog_grade"]
            assert grade in self.VALID_SHOWDOG_GRADES, (
                f"Case {case['id']} unexpected ShowDog grade: {grade}"
            )

    def test_breed_ids_are_non_empty_strings(self, reference_cases):
        for case in reference_cases:
            assert isinstance(case["breed_id"], str) and len(case["breed_id"]) > 0

    def test_descriptions_are_non_empty(self, reference_cases):
        for case in reference_cases:
            assert isinstance(case["description"], str) and len(case["description"]) > 0

    def test_sources_are_non_empty(self, reference_cases):
        for case in reference_cases:
            assert isinstance(case["source"], str) and len(case["source"]) > 0

    def test_no_obsolete_expected_scores_key(self, reference_cases):
        """No reference case should have the old 'expected_scores' key."""
        for case in reference_cases:
            assert "expected_scores" not in case, (
                f"Case {case['id']} has obsolete 'expected_scores' key"
            )


# ============================================================================
# apply_calibration_to_analysis
# ============================================================================


class TestApplyCalibrationToAnalysis:
    """Calibration offsets are applied correctly and scores are clamped."""

    def test_no_calibration_returns_original(self):
        with patch.object(ac, "load_breed_calibration", return_value={}):
            scores = {"structure": 80, "coat": 70}
            result = ac.apply_calibration_to_analysis("breed_x", scores)
        assert result == scores

    def test_positive_offset_applied(self):
        cal = {"breed_x": {"adjustments": {"structure": {"offset": 5.0}}}}
        with patch.object(ac, "load_breed_calibration", return_value=cal):
            result = ac.apply_calibration_to_analysis(
                "breed_x", {"structure": 80, "coat": 70}
            )
        assert result["structure"] == 85
        assert result["coat"] == 70  # unchanged

    def test_negative_offset_applied(self):
        cal = {"breed_x": {"adjustments": {"gait": {"offset": -3.0}}}}
        with patch.object(ac, "load_breed_calibration", return_value=cal):
            result = ac.apply_calibration_to_analysis("breed_x", {"gait": 85})
        assert result["gait"] == 82

    def test_score_clamped_at_100(self):
        cal = {"breed_x": {"adjustments": {"coat": {"offset": 10.0}}}}
        with patch.object(ac, "load_breed_calibration", return_value=cal):
            result = ac.apply_calibration_to_analysis("breed_x", {"coat": 95})
        assert result["coat"] == 100

    def test_score_clamped_at_0(self):
        cal = {"breed_x": {"adjustments": {"coat": {"offset": -20.0}}}}
        with patch.object(ac, "load_breed_calibration", return_value=cal):
            result = ac.apply_calibration_to_analysis("breed_x", {"coat": 10})
        assert result["coat"] == 0

    def test_zero_offset_no_change(self):
        cal = {"breed_x": {"adjustments": {"structure": {"offset": 0}}}}
        with patch.object(ac, "load_breed_calibration", return_value=cal):
            result = ac.apply_calibration_to_analysis(
                "breed_x", {"structure": 80}
            )
        assert result["structure"] == 80

    def test_original_dict_not_mutated(self):
        cal = {"breed_x": {"adjustments": {"structure": {"offset": 5}}}}
        with patch.object(ac, "load_breed_calibration", return_value=cal):
            original = {"structure": 80}
            _ = ac.apply_calibration_to_analysis("breed_x", original)
        assert original["structure"] == 80

    def test_multiple_components_adjusted(self):
        cal = {
            "breed_x": {
                "adjustments": {
                    "structure": {"offset": 2.0},
                    "coat": {"offset": -3.0},
                    "gait": {"offset": 1.5},
                }
            }
        }
        with patch.object(ac, "load_breed_calibration", return_value=cal):
            result = ac.apply_calibration_to_analysis(
                "breed_x", {"structure": 80, "coat": 70, "gait": 85}
            )
        assert result["structure"] == 82
        assert result["coat"] == 67
        assert result["gait"] == 86.5

    def test_adjustment_without_offset_key_ignored(self):
        """An adjustment dict without 'offset' should not crash."""
        cal = {"breed_x": {"adjustments": {"coat": {"variance_flag": True}}}}
        with patch.object(ac, "load_breed_calibration", return_value=cal):
            result = ac.apply_calibration_to_analysis(
                "breed_x", {"coat": 70}
            )
        assert result["coat"] == 70  # unchanged because offset defaults to 0

    def test_component_not_in_scores_is_skipped(self):
        """Calibration for a component not present in scores should not crash."""
        cal = {"breed_x": {"adjustments": {"gait": {"offset": 5}}}}
        with patch.object(ac, "load_breed_calibration", return_value=cal):
            result = ac.apply_calibration_to_analysis(
                "breed_x", {"structure": 80}
            )
        assert result == {"structure": 80}


# ============================================================================
# calibrate_against_fci
# ============================================================================


class TestCalibrateAgainstFci:
    """FCI calibration produces corrections when scores drift from expected."""

    @staticmethod
    def _breed_stats(count, mean, std=5.0):
        """Build a breed_stats dict with all components at the same mean."""
        stats = {"count": count}
        for comp in ("overall", "structure", "coat", "gait", "temperament"):
            stats[comp] = {
                "mean": mean, "std": std,
                "min": mean - 5, "max": mean + 5, "n": count,
            }
        return stats

    def test_no_calibration_when_count_too_low(self):
        breed_stats = {"breed_x": self._breed_stats(count=2, mean=90)}
        result = ac.calibrate_against_fci(breed_stats, {})
        assert "breed_x" not in result

    def test_no_calibration_when_mean_near_expected(self):
        """Mean of 82 is within 5 points of the 80 target."""
        breed_stats = {"breed_x": self._breed_stats(count=5, mean=82)}
        result = ac.calibrate_against_fci(breed_stats, {})
        assert "breed_x" not in result or result["breed_x"]["adjustments"] == {}

    def test_negative_offset_when_mean_too_high(self):
        """Mean of 95 => drift = 15 => correction is negative."""
        breed_stats = {"breed_x": self._breed_stats(count=5, mean=95)}
        result = ac.calibrate_against_fci(breed_stats, {})
        assert "breed_x" in result
        adj = result["breed_x"]["adjustments"]
        for comp in ("structure", "coat", "gait", "temperament"):
            assert adj[comp]["offset"] < 0

    def test_positive_offset_when_mean_too_low(self):
        """Mean of 60 => drift = -20 => correction is positive."""
        breed_stats = {"breed_x": self._breed_stats(count=5, mean=60)}
        result = ac.calibrate_against_fci(breed_stats, {})
        assert "breed_x" in result
        adj = result["breed_x"]["adjustments"]
        for comp in ("structure", "coat", "gait", "temperament"):
            assert adj[comp]["offset"] > 0

    def test_offset_clamped_at_plus_minus_8(self):
        """Very large drift should be clamped to [-8, 8]."""
        breed_stats = {"breed_x": self._breed_stats(count=5, mean=120)}
        result = ac.calibrate_against_fci(breed_stats, {})
        adj = result["breed_x"]["adjustments"]
        for comp in ("structure", "coat", "gait", "temperament"):
            assert -8.0 <= adj[comp]["offset"] <= 8.0

    def test_offset_calculation(self):
        """Mean 95 => drift 15 => correction = -15*0.3 = -4.5."""
        breed_stats = {"breed_x": self._breed_stats(count=5, mean=95)}
        result = ac.calibrate_against_fci(breed_stats, {})
        adj = result["breed_x"]["adjustments"]
        assert adj["structure"]["offset"] == -4.5

    def test_variance_flag_set_for_high_std(self):
        """std > 15 with ideal_structure set triggers variance_flag."""
        breed_stats = {"breed_x": self._breed_stats(count=5, mean=90, std=20)}
        breed_db = {
            "breed_x": {
                "ideal_structure": "正方形で筋肉質",
                "ideal_coat": "長毛で豊富",
                "ideal_gait": "力強い推進力",
            }
        }
        result = ac.calibrate_against_fci(breed_stats, breed_db)
        adj = result["breed_x"]["adjustments"]
        assert adj["structure"].get("variance_flag") is True
        assert adj["coat"].get("variance_flag") is True
        assert adj["gait"].get("variance_flag") is True

    def test_no_variance_flag_when_std_low(self):
        breed_stats = {"breed_x": self._breed_stats(count=5, mean=90, std=5)}
        breed_db = {
            "breed_x": {
                "ideal_structure": "正方形で筋肉質",
                "ideal_coat": "長毛で豊富",
                "ideal_gait": "力強い推進力",
            }
        }
        result = ac.calibrate_against_fci(breed_stats, breed_db)
        adj = result["breed_x"]["adjustments"]
        for comp in ("structure", "coat", "gait"):
            assert adj.get(comp, {}).get("variance_flag") is not True

    def test_no_variance_flag_without_ideal_descriptions(self):
        """Even with high std, no variance flag if breed_db lacks ideal_*."""
        breed_stats = {"breed_x": self._breed_stats(count=5, mean=90, std=20)}
        result = ac.calibrate_against_fci(breed_stats, {})
        adj = result["breed_x"]["adjustments"]
        for comp in ("structure", "coat", "gait"):
            assert adj.get(comp, {}).get("variance_flag") is not True

    def test_component_with_insufficient_n_skipped(self):
        """Component with n < 2 should not generate an adjustment."""
        stats = {"count": 5}
        for comp in ("overall", "structure", "coat", "gait", "temperament"):
            stats[comp] = {"mean": 95, "std": 5, "min": 90, "max": 100, "n": 1}
        breed_stats = {"breed_x": stats}
        result = ac.calibrate_against_fci(breed_stats, {})
        assert "breed_x" not in result

    def test_none_component_stats_skipped(self):
        stats = {"count": 5}
        for comp in ("overall", "structure", "coat", "gait", "temperament"):
            stats[comp] = None
        breed_stats = {"breed_x": stats}
        result = ac.calibrate_against_fci(breed_stats, {})
        assert "breed_x" not in result

    def test_calibration_contains_metadata(self):
        breed_stats = {"breed_x": self._breed_stats(count=5, mean=95)}
        result = ac.calibrate_against_fci(breed_stats, {})
        cal = result["breed_x"]
        assert cal["breed_id"] == "breed_x"
        assert cal["sample_size"] == 5
        assert "updated_at" in cal

    def test_multiple_breeds_calibrated_independently(self):
        breed_stats = {
            "breed_a": self._breed_stats(count=5, mean=95),
            "breed_b": self._breed_stats(count=5, mean=60),
        }
        result = ac.calibrate_against_fci(breed_stats, {})
        assert "breed_a" in result
        assert "breed_b" in result
        # breed_a has high mean => negative offset; breed_b has low => positive
        assert result["breed_a"]["adjustments"]["structure"]["offset"] < 0
        assert result["breed_b"]["adjustments"]["structure"]["offset"] > 0


# ============================================================================
# get_breed_fci_params
# ============================================================================


class TestGetBreedFciParams:
    """FCI-based parameters extracted from breed descriptions."""

    def test_square_proportion_detected(self):
        breed_db = {"b": {"ideal_structure": "正方形に近いプロポーション"}}
        params = ac.get_breed_fci_params("b", breed_db)
        assert params["ideal_ratio"] == 1.0

    def test_long_body_detected(self):
        breed_db = {"b": {"ideal_structure": "やや長めの体型"}}
        params = ac.get_breed_fci_params("b", breed_db)
        assert params["ideal_ratio"] == 1.6

    def test_compact_body_detected(self):
        breed_db = {"b": {"ideal_structure": "短い体型"}}
        params = ac.get_breed_fci_params("b", breed_db)
        assert params["ideal_ratio"] == 1.1

    def test_default_ratio_when_no_keywords(self):
        breed_db = {"b": {"ideal_structure": "バランスの取れた体型"}}
        params = ac.get_breed_fci_params("b", breed_db)
        assert params["ideal_ratio"] == 1.3

    def test_large_body_mass(self):
        breed_db = {"b": {"ideal_structure": "がっしりした体型で筋肉質"}}
        params = ac.get_breed_fci_params("b", breed_db)
        assert params["body_mass"] == "large"
        assert params["edge_density_target"] == 0.10

    def test_small_body_mass(self):
        breed_db = {"b": {"ideal_structure": "華奢な骨格"}}
        params = ac.get_breed_fci_params("b", breed_db)
        assert params["body_mass"] == "small"
        assert params["edge_density_target"] == 0.14

    def test_medium_body_mass_default(self):
        breed_db = {"b": {"ideal_structure": "バランスの取れた体型"}}
        params = ac.get_breed_fci_params("b", breed_db)
        assert params["body_mass"] == "medium"
        assert params["edge_density_target"] == 0.12

    def test_long_coat_type(self):
        breed_db = {"b": {"ideal_coat": "豊富な長毛"}}
        params = ac.get_breed_fci_params("b", breed_db)
        assert params["coat_type"] == "long"
        assert params["texture_expectation"] == "high"

    def test_short_coat_type(self):
        breed_db = {"b": {"ideal_coat": "短毛で密着"}}
        params = ac.get_breed_fci_params("b", breed_db)
        assert params["coat_type"] == "short"
        assert params["texture_expectation"] == "low"

    def test_wire_coat_type(self):
        breed_db = {"b": {"ideal_coat": "ワイヤーヘアで粗い"}}
        params = ac.get_breed_fci_params("b", breed_db)
        assert params["coat_type"] == "wire"
        assert params["texture_expectation"] == "medium"

    def test_curly_coat_type(self):
        breed_db = {"b": {"ideal_coat": "カーリー（巻き毛）"}}
        params = ac.get_breed_fci_params("b", breed_db)
        assert params["coat_type"] == "curly"
        assert params["texture_expectation"] == "high"

    def test_default_coat_type(self):
        breed_db = {"b": {"ideal_coat": "普通の被毛"}}
        params = ac.get_breed_fci_params("b", breed_db)
        assert params["coat_type"] == "medium"
        assert params["texture_expectation"] == "medium"

    def test_powerful_gait(self):
        breed_db = {"b": {"ideal_gait": "力強い推進力"}}
        params = ac.get_breed_fci_params("b", breed_db)
        assert params["gait_type"] == "powerful"
        assert params["expected_stride"] == "long"

    def test_elegant_gait(self):
        breed_db = {"b": {"ideal_gait": "軽快でスプリングのある"}}
        params = ac.get_breed_fci_params("b", breed_db)
        assert params["gait_type"] == "elegant"
        assert params["expected_stride"] == "moderate"

    def test_steady_gait(self):
        breed_db = {"b": {"ideal_gait": "安定した歩様"}}
        params = ac.get_breed_fci_params("b", breed_db)
        assert params["gait_type"] == "steady"
        assert params["expected_stride"] == "moderate"

    def test_default_gait(self):
        breed_db = {"b": {"ideal_gait": "普通の歩き方"}}
        params = ac.get_breed_fci_params("b", breed_db)
        assert params["gait_type"] == "balanced"
        assert params["expected_stride"] == "moderate"

    def test_hereditary_diseases_extracted(self):
        breed_db = {"b": {"hereditary_diseases": ["disease1", "disease2"]}}
        params = ac.get_breed_fci_params("b", breed_db)
        assert params["hereditary_diseases"] == ["disease1", "disease2"]

    def test_fci_number_and_names_extracted(self):
        breed_db = {
            "b": {
                "fci_number": 172,
                "name": "トイプードル",
                "name_en": "Toy Poodle",
            }
        }
        params = ac.get_breed_fci_params("b", breed_db)
        assert params["fci_number"] == 172
        assert params["breed_name"] == "トイプードル"
        assert params["breed_name_en"] == "Toy Poodle"

    def test_unknown_breed_returns_defaults(self):
        params = ac.get_breed_fci_params("unknown", {})
        assert params["ideal_ratio"] == 1.3
        assert params["body_mass"] == "medium"
        assert params["coat_type"] == "medium"
        assert params["gait_type"] == "balanced"
        assert params["hereditary_diseases"] == []
        assert params["fci_number"] is None
        assert params["breed_name"] == ""
        assert params["breed_name_en"] == ""


# ============================================================================
# should_run_cycle
# ============================================================================


class TestShouldRunCycle:
    """Cycle timing gate works correctly."""

    def test_should_run_when_never_run(self):
        # Default state has last_cycle_ts = 0
        assert ac.should_run_cycle() is True

    def test_should_not_run_when_recently_run(self):
        state = {
            "last_cycle_ts": time.time(),  # just now
            "total_cycles": 1,
            "total_analyses_processed": 0,
            "breed_stats": {},
        }
        ac.save_cycle_state(state)
        assert ac.should_run_cycle() is False

    def test_should_run_when_enough_time_passed(self):
        state = {
            "last_cycle_ts": time.time() - (25 * 3600),  # 25 hours ago
            "total_cycles": 1,
            "total_analyses_processed": 0,
            "breed_stats": {},
        }
        ac.save_cycle_state(state)
        assert ac.should_run_cycle() is True

    def test_boundary_exactly_24_hours(self):
        """At exactly 24 hours elapsed, should_run_cycle should return True."""
        state = {
            "last_cycle_ts": time.time() - (24 * 3600),
            "total_cycles": 1,
            "total_analyses_processed": 0,
            "breed_stats": {},
        }
        ac.save_cycle_state(state)
        assert ac.should_run_cycle() is True

    def test_boundary_just_under_24_hours(self):
        """At 23h59m, should_run_cycle should return False."""
        state = {
            "last_cycle_ts": time.time() - (23 * 3600 + 59 * 60),
            "total_cycles": 1,
            "total_analyses_processed": 0,
            "breed_stats": {},
        }
        ac.save_cycle_state(state)
        assert ac.should_run_cycle() is False


# ============================================================================
# run_cycle
# ============================================================================


class TestRunCycle:
    """Full cycle orchestration."""

    def test_skips_when_not_due(self):
        state = {
            "last_cycle_ts": time.time(),
            "total_cycles": 1,
            "total_analyses_processed": 0,
            "breed_stats": {},
        }
        ac.save_cycle_state(state)

        with patch.object(ac, "collect_recent_analyses", return_value=[]):
            result = ac.run_cycle(force=False)
        assert result["status"] == "skipped"

    def test_force_runs_even_when_not_due(self):
        state = {
            "last_cycle_ts": time.time(),
            "total_cycles": 0,
            "total_analyses_processed": 0,
            "breed_stats": {},
        }
        ac.save_cycle_state(state)

        with patch.object(ac, "collect_recent_analyses", return_value=[]), \
             patch("api.auto_cycle.aggregate_by_breed", return_value={}), \
             patch("api.auto_cycle.calibrate_against_fci", return_value={}):
            result = ac.run_cycle(force=True)

        assert result["status"] == "completed"
        assert result["cycle_number"] == 1
        assert result["analyses_processed"] == 0

    def test_cycle_increments_state(self):
        with patch.object(ac, "collect_recent_analyses", return_value=[]), \
             patch("api.auto_cycle.aggregate_by_breed", return_value={}), \
             patch("api.auto_cycle.calibrate_against_fci", return_value={}):
            ac.run_cycle(force=True)
            ac.run_cycle(force=True)

        state = ac.load_cycle_state()
        assert state["total_cycles"] == 2

    def test_cycle_processes_analyses(self):
        fake_analyses = [{
            "breed_id": "poodle",
            "overall_score": 80,
            "structure_score": 75,
            "coat_score": 70,
            "gait_score": 85,
            "temperament_score": 90,
        }]
        with patch.object(ac, "collect_recent_analyses",
                          return_value=fake_analyses), \
             patch("api.auto_cycle.calibrate_against_fci", return_value={}):
            result = ac.run_cycle(force=True)

        assert result["analyses_processed"] == 1
        assert result["breeds_analyzed"] == 1

    def test_cycle_writes_history(self):
        with patch.object(ac, "collect_recent_analyses", return_value=[]), \
             patch("api.auto_cycle.aggregate_by_breed", return_value={}), \
             patch("api.auto_cycle.calibrate_against_fci", return_value={}):
            ac.run_cycle(force=True)

        text = ac.CYCLE_HISTORY_PATH.read_text(encoding="utf-8")
        lines = text.strip().split("\n")
        assert len(lines) >= 1
        entry = json.loads(lines[-1])
        assert entry["status"] == "completed"

    def test_cycle_merges_calibration(self):
        """New calibrations merge with existing; old breeds are preserved."""
        existing = {
            "breed_a": {
                "breed_id": "breed_a",
                "adjustments": {"structure": {"offset": 1}},
            }
        }
        ac.save_breed_calibration(existing)

        new_cal = {
            "breed_b": {
                "breed_id": "breed_b",
                "adjustments": {"coat": {"offset": -2}},
            }
        }
        with patch.object(ac, "collect_recent_analyses", return_value=[]), \
             patch("api.auto_cycle.aggregate_by_breed", return_value={}), \
             patch("api.auto_cycle.calibrate_against_fci", return_value=new_cal):
            ac.run_cycle(force=True)

        cal = ac.load_breed_calibration()
        assert "breed_a" in cal  # kept from existing
        assert "breed_b" in cal  # added from new

    def test_cycle_result_has_duration(self):
        with patch.object(ac, "collect_recent_analyses", return_value=[]), \
             patch("api.auto_cycle.aggregate_by_breed", return_value={}), \
             patch("api.auto_cycle.calibrate_against_fci", return_value={}):
            result = ac.run_cycle(force=True)
        assert "duration_seconds" in result
        assert isinstance(result["duration_seconds"], float)

    def test_cycle_result_has_timestamp(self):
        with patch.object(ac, "collect_recent_analyses", return_value=[]), \
             patch("api.auto_cycle.aggregate_by_breed", return_value={}), \
             patch("api.auto_cycle.calibrate_against_fci", return_value={}):
            result = ac.run_cycle(force=True)
        assert "timestamp" in result

    def test_cycle_accumulates_total_analyses(self):
        fake = [{"breed_id": "a", "overall_score": 80, "structure_score": 70,
                 "coat_score": 65, "gait_score": 75, "temperament_score": 80}]
        with patch.object(ac, "collect_recent_analyses", return_value=fake), \
             patch("api.auto_cycle.calibrate_against_fci", return_value={}):
            ac.run_cycle(force=True)
        with patch.object(ac, "collect_recent_analyses", return_value=fake), \
             patch("api.auto_cycle.calibrate_against_fci", return_value={}):
            ac.run_cycle(force=True)

        state = ac.load_cycle_state()
        assert state["total_analyses_processed"] == 2


# ============================================================================
# try_auto_cycle
# ============================================================================


class TestTryAutoCycle:
    """Safe wrapper for auto-cycle."""

    def test_returns_none_when_not_due(self):
        state = {
            "last_cycle_ts": time.time(),
            "total_cycles": 1,
            "total_analyses_processed": 0,
            "breed_stats": {},
        }
        ac.save_cycle_state(state)
        result = ac.try_auto_cycle()
        assert result is None

    def test_runs_when_due(self):
        # Default state has last_cycle_ts=0, so it is due
        with patch.object(ac, "collect_recent_analyses", return_value=[]), \
             patch("api.auto_cycle.aggregate_by_breed", return_value={}), \
             patch("api.auto_cycle.calibrate_against_fci", return_value={}):
            result = ac.try_auto_cycle()
        assert result is not None
        assert result["status"] == "completed"

    def test_returns_none_on_exception(self):
        with patch.object(ac, "should_run_cycle",
                          side_effect=RuntimeError("boom")):
            result = ac.try_auto_cycle()
        assert result is None


# ============================================================================
# collect_recent_analyses (mocked database)
# ============================================================================


class TestCollectRecentAnalyses:
    """Database collection with mocked database calls."""

    def test_returns_empty_list_on_import_error(self):
        with patch("builtins.__import__",
                   side_effect=_import_error_for("api.database")):
            result = ac.collect_recent_analyses(hours=24)
        assert result == []

    def test_returns_empty_list_on_db_error(self):
        mock_db = MagicMock()
        mock_db.cursor.side_effect = Exception("DB connection failed")
        with patch("api.database.get_db", return_value=mock_db):
            result = ac.collect_recent_analyses(hours=24)
        assert result == []

    def test_returns_rows_as_dicts(self):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [
            {"id": 1, "breed_id": "poodle"},
        ]

        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        with patch("api.database.get_db", return_value=mock_conn):
            result = ac.collect_recent_analyses(hours=24)
        assert len(result) == 1
        assert result[0]["breed_id"] == "poodle"

    def test_custom_hours_parameter(self):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = []

        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        with patch("api.database.get_db", return_value=mock_conn):
            ac.collect_recent_analyses(hours=48)
        # Verify the SQL parameter used the custom hours value
        call_args = mock_cursor.execute.call_args
        assert "-48 hours" in call_args[0][1][0]


# ============================================================================
# _ensure_data_dir
# ============================================================================


class TestEnsureDataDir:
    """Data directory creation utility."""

    def test_creates_dir_if_missing(self, tmp_path, monkeypatch):
        target = tmp_path / "new_dir"
        monkeypatch.setattr(ac, "CYCLE_DATA_DIR", target)
        ac._ensure_data_dir()
        assert target.exists() and target.is_dir()

    def test_no_error_if_already_exists(self, tmp_path, monkeypatch):
        target = tmp_path / "existing"
        target.mkdir()
        monkeypatch.setattr(ac, "CYCLE_DATA_DIR", target)
        ac._ensure_data_dir()  # should not raise
        assert target.exists()

    def test_creates_nested_dirs(self, tmp_path, monkeypatch):
        target = tmp_path / "a" / "b" / "c"
        monkeypatch.setattr(ac, "CYCLE_DATA_DIR", target)
        ac._ensure_data_dir()
        assert target.exists() and target.is_dir()
