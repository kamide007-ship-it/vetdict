"""Tests for reco2/llm_adapter.py – adapter pattern, error handling, mocked HTTP."""

import json
import os
from io import BytesIO
from unittest.mock import MagicMock, patch, PropertyMock

import pytest

from reco2.llm_adapter import (
    BaseLLMAdapter,
    DummyAdapter,
    ClaudeAdapter,
    OpenAIAdapter,
    create_adapter,
)


# ===================================================================
# DummyAdapter
# ===================================================================

class TestDummyAdapter:
    def test_name_property(self):
        adapter = DummyAdapter()
        assert adapter.name == "dummy"

    def test_default_response(self):
        adapter = DummyAdapter()
        result = adapter.generate("hello")
        assert result["text"] == "これはダミー応答です。"
        assert result["model"] == "dummy-v1"
        assert result["usage"] is None

    def test_custom_fixed_response(self):
        adapter = DummyAdapter(fixed_response="custom response")
        result = adapter.generate("any prompt")
        assert result["text"] == "custom response"

    def test_generate_signature_ignored_params(self):
        adapter = DummyAdapter()
        result = adapter.generate(
            "prompt",
            temperature=0.0,
            max_tokens=512,
            system_prompt="system",
        )
        assert "text" in result
        assert "model" in result
        assert "usage" in result

    def test_generate_returns_dict(self):
        adapter = DummyAdapter()
        result = adapter.generate("test")
        assert isinstance(result, dict)

    def test_is_subclass_of_base(self):
        assert issubclass(DummyAdapter, BaseLLMAdapter)

    def test_extra_kwargs_ignored(self):
        # Extra kwargs should not raise
        adapter = DummyAdapter(fixed_response="ok", irrelevant_key="ignored")
        assert adapter.name == "dummy"


# ===================================================================
# ClaudeAdapter – no network calls
# ===================================================================

class TestClaudeAdapter:
    def test_name_property(self):
        adapter = ClaudeAdapter(api_key="test-key")
        assert adapter.name == "claude"

    def test_no_api_key_raises(self):
        adapter = ClaudeAdapter(api_key="")
        with pytest.raises(RuntimeError, match="ANTHROPIC_API_KEY"):
            adapter.generate("hello")

    def test_api_key_from_env(self, monkeypatch):
        monkeypatch.setenv("ANTHROPIC_API_KEY", "env-key")
        adapter = ClaudeAdapter()
        assert adapter.api_key == "env-key"

    def test_explicit_api_key_takes_precedence(self, monkeypatch):
        monkeypatch.setenv("ANTHROPIC_API_KEY", "env-key")
        adapter = ClaudeAdapter(api_key="explicit-key")
        assert adapter.api_key == "explicit-key"

    def test_default_model(self):
        adapter = ClaudeAdapter(api_key="key")
        assert "claude" in adapter.model.lower()

    def test_custom_model(self):
        adapter = ClaudeAdapter(api_key="key", model="claude-3-opus")
        assert adapter.model == "claude-3-opus"

    def test_custom_endpoint(self):
        adapter = ClaudeAdapter(api_key="key", endpoint="https://custom.endpoint/v1/messages")
        assert adapter.endpoint == "https://custom.endpoint/v1/messages"

    def test_is_subclass_of_base(self):
        assert issubclass(ClaudeAdapter, BaseLLMAdapter)

    def _make_mock_response(self, body: dict) -> MagicMock:
        """Helper: create a mock urllib response context manager."""
        raw = json.dumps(body).encode("utf-8")
        mock_resp = MagicMock()
        mock_resp.read.return_value = raw
        mock_resp.__enter__ = MagicMock(return_value=mock_resp)
        mock_resp.__exit__ = MagicMock(return_value=False)
        return mock_resp

    def test_generate_success(self):
        adapter = ClaudeAdapter(api_key="test-key")
        response_body = {
            "content": [{"type": "text", "text": "Hello from Claude"}],
            "model": "claude-sonnet-4-5",
            "usage": {"input_tokens": 10, "output_tokens": 5},
        }
        mock_resp = self._make_mock_response(response_body)
        with patch("urllib.request.urlopen", return_value=mock_resp):
            result = adapter.generate("Test prompt")
        assert result["text"] == "Hello from Claude"
        assert result["model"] == "claude-sonnet-4-5"
        assert result["usage"] == {"input_tokens": 10, "output_tokens": 5}

    def test_generate_multiple_content_blocks(self):
        adapter = ClaudeAdapter(api_key="test-key")
        response_body = {
            "content": [
                {"type": "text", "text": "Part one. "},
                {"type": "text", "text": "Part two."},
            ],
            "model": "claude-sonnet",
            "usage": None,
        }
        mock_resp = self._make_mock_response(response_body)
        with patch("urllib.request.urlopen", return_value=mock_resp):
            result = adapter.generate("prompt")
        assert result["text"] == "Part one. Part two."

    def test_generate_non_text_content_block_skipped(self):
        adapter = ClaudeAdapter(api_key="test-key")
        response_body = {
            "content": [
                {"type": "image", "source": "..."},
                {"type": "text", "text": "text only"},
            ],
            "model": "claude-sonnet",
            "usage": None,
        }
        mock_resp = self._make_mock_response(response_body)
        with patch("urllib.request.urlopen", return_value=mock_resp):
            result = adapter.generate("prompt")
        assert result["text"] == "text only"

    def test_generate_empty_content(self):
        adapter = ClaudeAdapter(api_key="test-key")
        response_body = {"content": [], "model": "claude-sonnet", "usage": None}
        mock_resp = self._make_mock_response(response_body)
        with patch("urllib.request.urlopen", return_value=mock_resp):
            result = adapter.generate("prompt")
        assert result["text"] == ""

    def test_generate_missing_content_key(self):
        adapter = ClaudeAdapter(api_key="test-key")
        response_body = {"model": "claude-sonnet", "usage": None}
        mock_resp = self._make_mock_response(response_body)
        with patch("urllib.request.urlopen", return_value=mock_resp):
            result = adapter.generate("prompt")
        assert result["text"] == ""

    def test_generate_model_fallback(self):
        adapter = ClaudeAdapter(api_key="test-key", model="fallback-model")
        response_body = {"content": [], "usage": None}  # no "model" key
        mock_resp = self._make_mock_response(response_body)
        with patch("urllib.request.urlopen", return_value=mock_resp):
            result = adapter.generate("prompt")
        assert result["model"] == "fallback-model"

    def test_generate_with_system_prompt(self):
        adapter = ClaudeAdapter(api_key="test-key")
        response_body = {
            "content": [{"type": "text", "text": "response"}],
            "model": "claude-sonnet",
            "usage": None,
        }
        mock_resp = self._make_mock_response(response_body)
        with patch("urllib.request.urlopen", return_value=mock_resp) as mock_urlopen:
            result = adapter.generate("prompt", system_prompt="Be helpful")
        assert result["text"] == "response"

    def test_generate_with_custom_temperature_and_tokens(self):
        adapter = ClaudeAdapter(api_key="test-key")
        response_body = {
            "content": [{"type": "text", "text": "ok"}],
            "model": "claude-sonnet",
            "usage": None,
        }
        mock_resp = self._make_mock_response(response_body)
        with patch("urllib.request.urlopen", return_value=mock_resp):
            result = adapter.generate("prompt", temperature=0.1, max_tokens=256)
        assert result["text"] == "ok"

    def test_generate_network_error_propagates(self):
        adapter = ClaudeAdapter(api_key="test-key")
        with patch("urllib.request.urlopen", side_effect=Exception("Network error")):
            with pytest.raises(Exception, match="Network error"):
                adapter.generate("prompt")

    def test_extra_kwargs_ignored(self):
        adapter = ClaudeAdapter(api_key="key", irrelevant="ignored")
        assert adapter.api_key == "key"


# ===================================================================
# OpenAIAdapter – no network calls
# ===================================================================

class TestOpenAIAdapter:
    def test_name_property(self):
        adapter = OpenAIAdapter(api_key="test-key")
        assert adapter.name == "openai"

    def test_no_api_key_raises(self):
        adapter = OpenAIAdapter(api_key="")
        with pytest.raises(RuntimeError, match="OPENAI_API_KEY"):
            adapter.generate("hello")

    def test_api_key_from_env(self, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "env-key-openai")
        adapter = OpenAIAdapter()
        assert adapter.api_key == "env-key-openai"

    def test_explicit_key_takes_precedence(self, monkeypatch):
        monkeypatch.setenv("OPENAI_API_KEY", "env-key")
        adapter = OpenAIAdapter(api_key="explicit")
        assert adapter.api_key == "explicit"

    def test_default_model_is_gpt4o(self):
        adapter = OpenAIAdapter(api_key="key")
        assert "gpt" in adapter.model.lower()

    def test_custom_model(self):
        adapter = OpenAIAdapter(api_key="key", model="gpt-3.5-turbo")
        assert adapter.model == "gpt-3.5-turbo"

    def test_is_subclass_of_base(self):
        assert issubclass(OpenAIAdapter, BaseLLMAdapter)

    def _make_mock_response(self, body: dict) -> MagicMock:
        raw = json.dumps(body).encode("utf-8")
        mock_resp = MagicMock()
        mock_resp.read.return_value = raw
        mock_resp.__enter__ = MagicMock(return_value=mock_resp)
        mock_resp.__exit__ = MagicMock(return_value=False)
        return mock_resp

    def test_generate_success(self):
        adapter = OpenAIAdapter(api_key="test-key")
        response_body = {
            "choices": [{"message": {"content": "Hello from GPT"}}],
            "model": "gpt-4o",
            "usage": {"prompt_tokens": 5, "completion_tokens": 10},
        }
        mock_resp = self._make_mock_response(response_body)
        with patch("urllib.request.urlopen", return_value=mock_resp):
            result = adapter.generate("Test prompt")
        assert result["text"] == "Hello from GPT"
        assert result["model"] == "gpt-4o"
        assert result["usage"] == {"prompt_tokens": 5, "completion_tokens": 10}

    def test_generate_with_system_prompt(self):
        adapter = OpenAIAdapter(api_key="test-key")
        response_body = {
            "choices": [{"message": {"content": "response"}}],
            "model": "gpt-4o",
            "usage": None,
        }
        mock_resp = self._make_mock_response(response_body)
        with patch("urllib.request.urlopen", return_value=mock_resp):
            result = adapter.generate("prompt", system_prompt="Be concise")
        assert result["text"] == "response"

    def test_generate_without_system_prompt(self):
        adapter = OpenAIAdapter(api_key="test-key")
        response_body = {
            "choices": [{"message": {"content": "no system"}}],
            "model": "gpt-4o",
            "usage": None,
        }
        mock_resp = self._make_mock_response(response_body)
        with patch("urllib.request.urlopen", return_value=mock_resp):
            result = adapter.generate("prompt")
        assert result["text"] == "no system"

    def test_generate_empty_choices(self):
        adapter = OpenAIAdapter(api_key="test-key")
        response_body = {"choices": [], "model": "gpt-4o", "usage": None}
        mock_resp = self._make_mock_response(response_body)
        with patch("urllib.request.urlopen", return_value=mock_resp):
            result = adapter.generate("prompt")
        # choices is empty → (j.get("choices") or [{}])[0] → {}
        assert result["text"] == ""

    def test_generate_model_fallback(self):
        adapter = OpenAIAdapter(api_key="test-key", model="fallback-gpt")
        response_body = {
            "choices": [{"message": {"content": "ok"}}],
            "usage": None,
            # no "model" key in response
        }
        mock_resp = self._make_mock_response(response_body)
        with patch("urllib.request.urlopen", return_value=mock_resp):
            result = adapter.generate("prompt")
        assert result["model"] == "fallback-gpt"

    def test_generate_network_error_propagates(self):
        adapter = OpenAIAdapter(api_key="test-key")
        with patch("urllib.request.urlopen", side_effect=Exception("Connection refused")):
            with pytest.raises(Exception, match="Connection refused"):
                adapter.generate("prompt")

    def test_generate_message_not_dict(self):
        # Edge case: message is not a dict
        adapter = OpenAIAdapter(api_key="test-key")
        response_body = {
            "choices": [{"message": None}],
            "model": "gpt-4o",
            "usage": None,
        }
        mock_resp = self._make_mock_response(response_body)
        with patch("urllib.request.urlopen", return_value=mock_resp):
            result = adapter.generate("prompt")
        assert result["text"] == ""

    def test_extra_kwargs_ignored(self):
        adapter = OpenAIAdapter(api_key="key", unknown_kwarg="value")
        assert adapter.api_key == "key"


# ===================================================================
# create_adapter factory
# ===================================================================

class TestCreateAdapter:
    def test_dummy_by_name(self):
        adapter = create_adapter("dummy")
        assert isinstance(adapter, DummyAdapter)

    def test_test_alias_for_dummy(self):
        adapter = create_adapter("test")
        assert isinstance(adapter, DummyAdapter)

    def test_claude_by_name(self):
        adapter = create_adapter("claude", api_key="key")
        assert isinstance(adapter, ClaudeAdapter)

    def test_anthropic_alias_for_claude(self):
        adapter = create_adapter("anthropic", api_key="key")
        assert isinstance(adapter, ClaudeAdapter)

    def test_openai_by_name(self):
        adapter = create_adapter("openai", api_key="key")
        assert isinstance(adapter, OpenAIAdapter)

    def test_gpt_alias_for_openai(self):
        adapter = create_adapter("gpt", api_key="key")
        assert isinstance(adapter, OpenAIAdapter)

    def test_unknown_name_raises_value_error(self):
        with pytest.raises(ValueError, match="Unknown adapter"):
            create_adapter("nonexistent_adapter")

    def test_default_is_dummy(self):
        adapter = create_adapter()
        assert isinstance(adapter, DummyAdapter)

    def test_name_case_insensitive(self):
        adapter = create_adapter("DUMMY")
        assert isinstance(adapter, DummyAdapter)

    def test_name_with_whitespace(self):
        adapter = create_adapter("  dummy  ")
        assert isinstance(adapter, DummyAdapter)

    def test_empty_string_defaults_to_dummy(self):
        adapter = create_adapter("")
        assert isinstance(adapter, DummyAdapter)

    def test_kwargs_forwarded_to_adapter(self):
        adapter = create_adapter("dummy", fixed_response="forwarded")
        assert adapter.generate("x")["text"] == "forwarded"

    def test_claude_kwargs_forwarded(self):
        adapter = create_adapter("claude", api_key="my-key", model="claude-3-opus")
        assert adapter.api_key == "my-key"
        assert adapter.model == "claude-3-opus"

    def test_openai_kwargs_forwarded(self):
        adapter = create_adapter("openai", api_key="my-key", model="gpt-3.5-turbo")
        assert adapter.api_key == "my-key"
        assert adapter.model == "gpt-3.5-turbo"
