"""Typed domain models for resume analysis results."""

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

AssessmentItem = Annotated[str, Field(min_length=1, max_length=500)]
RoleSkill = Annotated[str, Field(min_length=1, max_length=100)]


class StrictModel(BaseModel):
    """Base model with consistent validation for provider-controlled data."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class Skill(StrictModel):
    """A skill identified in the submitted resume."""

    name: str = Field(min_length=1, max_length=100)
    evidence: str = Field(min_length=1, max_length=500)
    confidence: float = Field(ge=0, le=1)


class ExperienceAssessment(StrictModel):
    """Assessment of the candidate's experience evidence."""

    level: Literal["Entry-level", "Early-career", "Mid-level", "Senior", "Unclear"]
    strengths: list[AssessmentItem] = Field(default_factory=list, max_length=10)
    gaps: list[AssessmentItem] = Field(default_factory=list, max_length=10)
    assessment: str = Field(min_length=1, max_length=2_000)


class JobRecommendation(StrictModel):
    """A role recommendation grounded in the resume profile."""

    role: str = Field(min_length=1, max_length=150)
    fit_score: int = Field(ge=0, le=100)
    rationale: str = Field(min_length=1, max_length=1_000)
    matching_skills: list[RoleSkill] = Field(default_factory=list, max_length=20)
    missing_skills: list[RoleSkill] = Field(default_factory=list, max_length=20)


class LearningSuggestion(StrictModel):
    """A practical next step for closing a skills gap."""

    skill: str = Field(min_length=1, max_length=100)
    action: str = Field(min_length=1, max_length=500)
    priority: Literal["High", "Medium", "Low"]


class ResumeImprovement(StrictModel):
    """An actionable improvement to the submitted resume."""

    area: str = Field(min_length=1, max_length=100)
    suggestion: str = Field(min_length=1, max_length=1_000)
    priority: Literal["High", "Medium", "Low"]


class ResumeAnalysis(StrictModel):
    """Complete, validated AI analysis returned to the application."""

    resume_summary: str = Field(min_length=1, max_length=2_000)
    technical_skills: list[Skill] = Field(default_factory=list, max_length=50)
    soft_skills: list[Skill] = Field(default_factory=list, max_length=30)
    experience_assessment: ExperienceAssessment
    job_recommendations: list[JobRecommendation] = Field(
        default_factory=list, max_length=10
    )
    missing_skills: list[RoleSkill] = Field(default_factory=list, max_length=30)
    learning_suggestions: list[LearningSuggestion] = Field(
        default_factory=list, max_length=20
    )
    resume_improvements: list[ResumeImprovement] = Field(
        default_factory=list, max_length=20
    )

    @field_validator("missing_skills", mode="before")
    @classmethod
    def remove_blank_skills(cls, value: object) -> object:
        """Remove empty skill names before strict model validation."""

        if isinstance(value, list):
            return [item for item in value if isinstance(item, str) and item.strip()]
        return value
