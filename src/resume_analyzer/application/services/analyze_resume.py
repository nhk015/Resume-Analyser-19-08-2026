"""Use case for validating and analyzing resume text."""

import logging
from dataclasses import dataclass

from resume_analyzer.domain.exceptions import InvalidResumeError
from resume_analyzer.domain.models import ResumeAnalysis
from resume_analyzer.domain.ports import AnalysisProvider

LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class AnalyzeResumeResult:
    """Application result returned after a successful analysis."""

    analysis: ResumeAnalysis
    input_characters: int


class AnalyzeResumeService:
    """Coordinate resume validation and AI analysis."""

    def __init__(self, provider: AnalysisProvider, max_chars: int) -> None:
        """Configure the service with an injected analysis provider."""

        self._provider = provider
        self._max_chars = max_chars

    def execute(self, resume_text: str) -> AnalyzeResumeResult:
        """Validate resume text and return a provider-backed analysis."""

        normalized_text = resume_text.strip()
        if not normalized_text:
            raise InvalidResumeError("Paste resume text before submitting it.")
        if len(normalized_text) > self._max_chars:
            raise InvalidResumeError(
                f"Resume text is too long. Limit it to {self._max_chars:,} characters."
            )

        LOGGER.info("resume_analysis_requested input_chars=%d", len(normalized_text))
        analysis = self._provider.analyze(normalized_text)
        return AnalyzeResumeResult(
            analysis=analysis,
            input_characters=len(normalized_text),
        )
