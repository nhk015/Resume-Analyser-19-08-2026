"""Shared test configuration and fixtures."""

import pytest

from resume_analyzer.domain.models import (
    ExperienceAssessment,
    JobRecommendation,
    LearningSuggestion,
    ResumeAnalysis,
    ResumeImprovement,
    Skill,
)


@pytest.fixture
def sample_analysis() -> ResumeAnalysis:
    """Return a representative valid analysis for application tests."""

    return ResumeAnalysis(
        resume_summary="Python developer with project experience in data applications.",
        technical_skills=[
            Skill(
                name="Python",
                evidence="Built a Python application.",
                confidence=0.95,
            )
        ],
        soft_skills=[
            Skill(
                name="Communication",
                evidence="Presented project outcomes.",
                confidence=0.8,
            )
        ],
        experience_assessment=ExperienceAssessment(
            level="Entry-level",
            strengths=["Strong project evidence"],
            gaps=["Limited professional experience"],
            assessment="The resume demonstrates practical entry-level experience.",
        ),
        job_recommendations=[
            JobRecommendation(
                role="Junior Python Developer",
                fit_score=82,
                rationale="Python project evidence aligns with the role.",
                matching_skills=["Python"],
                missing_skills=["Docker"],
            )
        ],
        missing_skills=["Docker"],
        learning_suggestions=[
            LearningSuggestion(
                skill="Docker",
                action="Containerize one existing project and document it.",
                priority="High",
            )
        ],
        resume_improvements=[
            ResumeImprovement(
                area="Experience bullets",
                suggestion="Add measurable outcomes to project bullets.",
                priority="High",
            )
        ],
    )
