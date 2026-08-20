"""Validation tests for settings and AI provider output."""

import json
from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from resume_analyzer.config import Settings
from resume_analyzer.domain.exceptions import AIProviderError, ConfigurationError
from resume_analyzer.domain.models import ResumeAnalysis
from resume_analyzer.infrastructure.ai.openai_client import OpenAIResumeAnalyzer


def test_missing_openai_key_is_rejected_at_adapter_boundary():
    """The adapter must fail before constructing an OpenAI client without a key."""

    settings = Settings(_env_file=None, openai_api_key=" ")

    with pytest.raises(ConfigurationError, match="OPENAI_API_KEY"):
        OpenAIResumeAnalyzer(settings)


def test_unknown_provider_fields_are_rejected(sample_analysis):
    """Unexpected top-level provider output cannot enter application state."""

    payload = sample_analysis.model_dump()
    payload["unexpected"] = "untrusted"

    with pytest.raises(ValidationError):
        ResumeAnalysis.model_validate(payload)


def test_oversized_nested_provider_fields_are_rejected(sample_analysis):
    """Nested free text is bounded to protect UI and memory usage."""

    payload = sample_analysis.model_dump()
    payload["experience_assessment"]["strengths"] = ["x" * 501]

    with pytest.raises(ValidationError):
        ResumeAnalysis.model_validate(payload)


def test_invalid_provider_payload_becomes_safe_adapter_error(
    monkeypatch, sample_analysis
):
    """Schema-invalid JSON is translated to an application provider error."""

    del sample_analysis
    analyzer = OpenAIResumeAnalyzer(
        Settings(_env_file=None, openai_api_key="test-key")
    )
    response = SimpleNamespace(
        choices=[
            SimpleNamespace(
                message=SimpleNamespace(
                    content=json.dumps({"resume_summary": "incomplete"})
                )
            )
        ]
    )
    monkeypatch.setattr(
        analyzer._client.chat.completions,
        "create",
        lambda **kwargs: response,
    )

    with pytest.raises(AIProviderError, match="invalid analysis"):
        analyzer.analyze("resume")
