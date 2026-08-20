"""Deterministic integration tests for the service and OpenAI adapter."""

import json
from types import SimpleNamespace

from resume_analyzer.application.services.analyze_resume import AnalyzeResumeService
from resume_analyzer.config import Settings
from resume_analyzer.infrastructure.ai.openai_client import OpenAIResumeAnalyzer


def make_openai_response(payload: dict) -> SimpleNamespace:
    """Build the smallest response shape consumed by the adapter."""

    return SimpleNamespace(
        choices=[
            SimpleNamespace(
                message=SimpleNamespace(content=json.dumps(payload))
            )
        ]
    )


def test_service_and_openai_adapter_return_structured_analysis(
    monkeypatch, sample_analysis
):
    """A mocked OpenAI response flows through adapter and service validation."""

    settings = Settings(_env_file=None, openai_api_key="test-key")
    analyzer = OpenAIResumeAnalyzer(settings)
    service = AnalyzeResumeService(provider=analyzer, max_chars=1_000)
    calls: list[dict] = []

    def fake_create(**kwargs):
        calls.append(kwargs)
        return make_openai_response(sample_analysis.model_dump())

    monkeypatch.setattr(analyzer._client.chat.completions, "create", fake_create)

    result = service.execute("  Python developer resume  ")

    assert result.analysis == sample_analysis
    assert result.input_characters == len("Python developer resume")
    assert len(calls) == 1
    assert calls[0]["model"] == "gpt-4o-mini"
    assert calls[0]["response_format"] == {"type": "json_object"}
    assert "Python developer resume" in calls[0]["messages"][1]["content"]


def test_integration_path_never_constructs_network_transport(
    monkeypatch, sample_analysis
):
    """The mocked completion call proves this flow has no internet dependency."""

    settings = Settings(_env_file=None, openai_api_key="test-key")
    analyzer = OpenAIResumeAnalyzer(settings)
    service = AnalyzeResumeService(provider=analyzer, max_chars=1_000)

    def fake_create(**kwargs):
        return make_openai_response(sample_analysis.model_dump())

    monkeypatch.setattr(analyzer._client.chat.completions, "create", fake_create)
    monkeypatch.setattr(
        analyzer._client,
        "request",
        lambda *args, **kwargs: (_ for _ in ()).throw(
            AssertionError("network transport must not be used")
        ),
    )

    result = service.execute("resume")

    assert result.analysis == sample_analysis
