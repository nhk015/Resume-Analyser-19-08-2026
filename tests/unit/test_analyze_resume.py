"""Tests for the resume analysis application service."""

import pytest

from resume_analyzer.application.services.analyze_resume import AnalyzeResumeService
from resume_analyzer.domain.exceptions import InvalidResumeError


class FakeAnalysisProvider:
    """Deterministic provider test double."""

    def __init__(self, analysis):
        self.analysis = analysis
        self.received_text = ""

    def analyze(self, resume_text: str):
        self.received_text = resume_text
        return self.analysis


def test_execute_strips_text_and_returns_provider_analysis(sample_analysis):
    """The service should normalize whitespace before provider invocation."""

    provider = FakeAnalysisProvider(sample_analysis)
    service = AnalyzeResumeService(provider=provider, max_chars=1000)

    result = service.execute("  Python developer resume  ")

    assert result.analysis == sample_analysis
    assert result.input_characters == len("Python developer resume")
    assert provider.received_text == "Python developer resume"


def test_execute_rejects_empty_resume(sample_analysis):
    """Blank input must fail before any provider call."""

    provider = FakeAnalysisProvider(sample_analysis)
    service = AnalyzeResumeService(provider=provider, max_chars=1000)

    with pytest.raises(InvalidResumeError, match="Paste resume text"):
        service.execute(" \n ")

    assert provider.received_text == ""


def test_execute_rejects_resume_over_configured_limit(sample_analysis):
    """Oversized input must be rejected deterministically."""

    provider = FakeAnalysisProvider(sample_analysis)
    service = AnalyzeResumeService(provider=provider, max_chars=10)

    with pytest.raises(InvalidResumeError, match="too long"):
        service.execute("12345678901")
