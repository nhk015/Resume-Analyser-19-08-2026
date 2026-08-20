"""Tests for strict AI output models."""

import pytest
from pydantic import ValidationError

from resume_analyzer.domain.models import ResumeAnalysis


def test_analysis_rejects_unknown_fields(sample_analysis):
    """Unexpected provider fields must not silently enter application state."""

    payload = sample_analysis.model_dump()
    payload["untrusted_field"] = "unexpected"

    with pytest.raises(ValidationError):
        ResumeAnalysis.model_validate(payload)


def test_analysis_removes_blank_missing_skills(sample_analysis):
    """Blank skill labels are not useful to users."""

    payload = sample_analysis.model_dump()
    payload["missing_skills"] = ["Docker", "", "  "]

    analysis = ResumeAnalysis.model_validate(payload)

    assert analysis.missing_skills == ["Docker"]


def test_analysis_rejects_oversized_nested_text(sample_analysis):
    """Provider output must bound individual list items as well as list counts."""

    payload = sample_analysis.model_dump()
    payload["experience_assessment"]["strengths"] = ["x" * 501]

    with pytest.raises(ValidationError):
        ResumeAnalysis.model_validate(payload)
