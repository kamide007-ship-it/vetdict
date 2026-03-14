"""Tests for api/errors.py - Custom exception classes."""

from api.errors import AnalysisError, AnalysisUnavailableError, DataCorruptionError


class TestAnalysisError:

    def test_is_exception(self):
        assert issubclass(AnalysisError, Exception)

    def test_can_raise_and_catch(self):
        with __import__("pytest").raises(AnalysisError):
            raise AnalysisError("test error")

    def test_message_preserved(self):
        try:
            raise AnalysisError("specific message")
        except AnalysisError as e:
            assert str(e) == "specific message"


class TestAnalysisUnavailableError:

    def test_is_analysis_error(self):
        assert issubclass(AnalysisUnavailableError, AnalysisError)

    def test_catchable_as_parent(self):
        with __import__("pytest").raises(AnalysisError):
            raise AnalysisUnavailableError("no opencv")


class TestDataCorruptionError:

    def test_is_exception(self):
        assert issubclass(DataCorruptionError, Exception)

    def test_not_analysis_error(self):
        assert not issubclass(DataCorruptionError, AnalysisError)
