"""Unit tests for the resume analysis application service."""

from dataclasses import dataclass

import pytest

from resume_analyzer.application.services.analyze_resume import (
    AnalyzeResumeService,
)
from resume_analyzer.domain.exceptions import InvalidResumeError
from resume_analyzer.domain.models import ResumeAnalysis


@dataclass
class RecordingProvider:
    """Deterministic provider double that records the submitted text."""

    analysis: ResumeAnalysis
    received_text: str = ""
    calls: int = 0

    def analyze(self, resume_text: str) -> ResumeAnalysis:
        self.received_text = resume_text
        self.calls += 1
        return self.analysis


def test_execute_returns_analysis_and_normalizes_input(sample_analysis):
    """Valid input is trimmed before exactly one provider call."""

    provider = RecordingProvider(sample_analysis)
    service = AnalyzeResumeService(provider=provider, max_chars=100)

    result = service.execute("  Python developer resume  ")

    assert result.analysis == sample_analysis
    assert result.input_characters == len("Python developer resume")
    assert provider.received_text == "Python developer resume"
    assert provider.calls == 1


def test_execute_accepts_input_at_exact_limit(sample_analysis):
    """The configured maximum is inclusive."""

    provider = RecordingProvider(sample_analysis)
    service = AnalyzeResumeService(provider=provider, max_chars=4)

    result = service.execute("  test  ")

    assert result.input_characters == 4
    assert provider.received_text == "test"


def test_execute_preserves_provider_analysis_identity(sample_analysis):
    """The service returns the validated provider result unchanged."""

    provider = RecordingProvider(sample_analysis)
    service = AnalyzeResumeService(provider=provider, max_chars=100)

    result = service.execute("resume")

    assert result.analysis is sample_analysis


def test_execute_does_not_call_provider_for_invalid_input(sample_analysis):
    """Validation failures happen before provider invocation."""

    provider = RecordingProvider(sample_analysis)
    service = AnalyzeResumeService(provider=provider, max_chars=10)

    with pytest.raises(InvalidResumeError):
        service.execute(" ")

    assert provider.calls == 0


def test_execute_does_not_mutate_provider_errors(sample_analysis):
    """Provider exceptions remain visible to the application boundary."""

    class FailingProvider:
        def analyze(self, resume_text: str) -> ResumeAnalysis:
            raise RuntimeError("deterministic provider failure")

    service = AnalyzeResumeService(provider=FailingProvider(), max_chars=100)

    with pytest.raises(RuntimeError, match="deterministic provider failure"):
        service.execute("resume")
