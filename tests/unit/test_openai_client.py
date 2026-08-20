"""Tests for the OpenAI provider adapter."""

from types import SimpleNamespace

import httpx
import pytest
from openai import RateLimitError

from resume_analyzer.config import Settings
from resume_analyzer.domain.exceptions import AIProviderError
from resume_analyzer.infrastructure.ai.openai_client import OpenAIResumeAnalyzer


def test_insufficient_quota_returns_billing_message(monkeypatch):
    """Quota exhaustion should tell the user to check billing and usage limits."""

    settings = Settings(openai_api_key="test-key")
    analyzer = OpenAIResumeAnalyzer(settings)
    response = httpx.Response(
        429,
        request=httpx.Request("POST", "https://api.openai.com/v1/chat/completions"),
        json={
            "error": {
                "message": "You exceeded your current quota.",
                "type": "insufficient_quota",
                "code": "insufficient_quota",
            }
        },
    )

    def raise_quota_error(*args, **kwargs):
        raise RateLimitError(
            "You exceeded your current quota.", response=response, body=response.json()
        )

    monkeypatch.setattr(
        analyzer._client.chat.completions, "create", raise_quota_error
    )

    with pytest.raises(AIProviderError, match="quota is exhausted"):
        analyzer.analyze("resume text")


def test_empty_provider_response_returns_user_safe_error(monkeypatch):
    """An empty provider message must not become application state."""

    analyzer = OpenAIResumeAnalyzer(Settings(openai_api_key="test-key"))
    response = SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content=None))]
    )
    monkeypatch.setattr(
        analyzer._client.chat.completions, "create", lambda **_: response
    )

    with pytest.raises(AIProviderError, match="empty response"):
        analyzer.analyze("resume text")


def test_invalid_provider_json_returns_user_safe_error(monkeypatch):
    """Malformed provider JSON must be rejected before UI rendering."""

    analyzer = OpenAIResumeAnalyzer(Settings(openai_api_key="test-key"))
    response = SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content="not-json"))]
    )
    monkeypatch.setattr(
        analyzer._client.chat.completions, "create", lambda **_: response
    )

    with pytest.raises(AIProviderError, match="invalid analysis"):
        analyzer.analyze("resume text")