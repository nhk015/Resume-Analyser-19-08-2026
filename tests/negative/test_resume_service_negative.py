"""Negative tests for invalid resume service inputs."""

import pytest

from resume_analyzer.application.services.analyze_resume import AnalyzeResumeService
from resume_analyzer.domain.exceptions import InvalidResumeError


class NeverCalledProvider:
    """Provider double that fails if validation lets an invalid request through."""

    def __init__(self):
        self.calls = 0

    def analyze(self, resume_text: str):
        self.calls += 1
        raise AssertionError("provider must not be called")


@pytest.mark.parametrize("resume_text", ["", " ", "\n\t", "  \n  "])
def test_blank_resume_is_rejected(resume_text):
    """Blank and whitespace-only resumes are invalid."""

    provider = NeverCalledProvider()
    service = AnalyzeResumeService(provider=provider, max_chars=100)

    with pytest.raises(InvalidResumeError, match="Paste resume text"):
        service.execute(resume_text)

    assert provider.calls == 0


def test_resume_over_limit_is_rejected_before_provider_call():
    """Oversized text cannot reach the provider."""

    provider = NeverCalledProvider()
    service = AnalyzeResumeService(provider=provider, max_chars=5)

    with pytest.raises(InvalidResumeError, match="too long"):
        service.execute("123456")

    assert provider.calls == 0


def test_whitespace_is_not_counted_against_resume_limit(sample_analysis):
    """Validation uses normalized input, matching the user-visible character count."""

    class Provider:
        def analyze(self, resume_text: str):
            return sample_analysis

    service = AnalyzeResumeService(provider=Provider(), max_chars=5)

    result = service.execute("  12345  ")

    assert result.input_characters == 5
