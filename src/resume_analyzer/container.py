"""Application dependency composition root."""

from dataclasses import dataclass

from resume_analyzer.application.services.analyze_resume import AnalyzeResumeService
from resume_analyzer.config import Settings
from resume_analyzer.infrastructure.ai.openai_client import OpenAIResumeAnalyzer


@dataclass(frozen=True)
class ApplicationContainer:
    """Concrete services used by the Streamlit application."""

    analyze_resume: AnalyzeResumeService


def build_container(settings: Settings) -> ApplicationContainer:
    """Build application services from the supplied runtime settings."""

    provider = OpenAIResumeAnalyzer(settings)
    return ApplicationContainer(
        analyze_resume=AnalyzeResumeService(
            provider=provider,
            max_chars=settings.max_resume_chars,
        )
    )
