"""Ports used by the application layer."""

from collections.abc import Callable
from typing import Protocol

from resume_analyzer.domain.models import ResumeAnalysis


class AnalysisProvider(Protocol):
    """Provider capable of analyzing resume text."""

    def analyze(self, resume_text: str) -> ResumeAnalysis:
        """Return a validated analysis for resume text."""


class Clock(Protocol):
    """Clock abstraction for deterministic tests."""

    def now(self) -> str:
        """Return the current UTC timestamp as an ISO-8601 string."""


Logger = Callable[[str, object], None]
