"""Streamlit presentation for the AI Resume Analyzer."""

import logging
from typing import NoReturn

import streamlit as st

from resume_analyzer.application.services.analyze_resume import AnalyzeResumeResult
from resume_analyzer.config import get_settings
from resume_analyzer.container import ApplicationContainer, build_container
from resume_analyzer.domain.exceptions import (
    AIProviderError,
    ConfigurationError,
    InvalidResumeError,
    ResumeAnalyzerError,
)
from resume_analyzer.domain.models import (
    JobRecommendation,
    LearningSuggestion,
    ResumeImprovement,
    Skill,
)
from resume_analyzer.infrastructure.observability.logging import configure_logging

LOGGER = logging.getLogger(__name__)


@st.cache_resource
def get_container() -> ApplicationContainer:
    """Build and cache application dependencies for the Streamlit process."""

    settings = get_settings()
    configure_logging(settings.log_level)
    return build_container(settings)


def initialize_state() -> None:
    """Initialize session state without storing secrets or provider clients."""

    defaults: dict[str, object] = {
        "submitted_resume": "",
        "analysis_result": None,
        "analysis_error": "",
    }
    for key, value in defaults.items():
        st.session_state.setdefault(key, value)


def render_skill_list(title: str, skills: list[Skill]) -> None:
    """Render extracted skills with evidence and confidence."""

    st.subheader(title)
    if not skills:
        st.info("No skills were confidently identified in this category.")
        return
    for skill in skills:
        confidence = f"{skill.confidence:.0%} confidence"
        st.markdown(f"**{skill.name}** · {confidence}")
        st.caption(f"Evidence: {skill.evidence}")


def render_recommendations(recommendations: list[JobRecommendation]) -> None:
    """Render job recommendations with transparent fit factors."""

    st.subheader("Job Recommendations")
    if not recommendations:
        st.info("No strong role recommendations were identified.")
        return
    for recommendation in recommendations:
        with st.expander(
            f"{recommendation.role} · {recommendation.fit_score}% fit"
        ):
            st.write(recommendation.rationale)
            st.markdown("**Matching skills**")
            st.write(", ".join(recommendation.matching_skills) or "None identified")
            st.markdown("**Missing or unevidenced skills**")
            st.write(", ".join(recommendation.missing_skills) or "None identified")


def render_learning_suggestions(suggestions: list[LearningSuggestion]) -> None:
    """Render prioritized learning actions."""

    st.subheader("Learning Suggestions")
    if not suggestions:
        st.info("No learning suggestions were generated.")
        return
    for suggestion in suggestions:
        st.markdown(f"**{suggestion.priority} priority: {suggestion.skill}**")
        st.write(suggestion.action)


def render_improvements(improvements: list[ResumeImprovement]) -> None:
    """Render prioritized resume improvements."""

    st.subheader("Resume Improvements")
    if not improvements:
        st.info("No improvement suggestions were generated.")
        return
    for improvement in improvements:
        st.markdown(f"**{improvement.priority} priority: {improvement.area}**")
        st.write(improvement.suggestion)


def render_analysis(result: AnalyzeResumeResult) -> None:
    """Render the complete validated analysis."""

    analysis = result.analysis
    st.success(f"Analysis complete for {result.input_characters:,} characters.")

    st.subheader("Resume Summary")
    st.write(analysis.resume_summary)

    left, right = st.columns(2)
    with left:
        render_skill_list("Technical Skills", analysis.technical_skills)
    with right:
        render_skill_list("Soft Skills", analysis.soft_skills)

    st.subheader("Experience Assessment")
    assessment = analysis.experience_assessment
    st.metric("Experience level", assessment.level)
    st.write(assessment.assessment)
    if assessment.strengths:
        st.markdown("**Strengths**")
        st.write("\n".join(f"- {item}" for item in assessment.strengths))
    if assessment.gaps:
        st.markdown("**Gaps**")
        st.write("\n".join(f"- {item}" for item in assessment.gaps))

    st.subheader("Missing Skills")
    st.write(
        ", ".join(analysis.missing_skills)
        or "No major missing skills identified."
    )
    render_recommendations(analysis.job_recommendations)
    render_learning_suggestions(analysis.learning_suggestions)
    render_improvements(analysis.resume_improvements)


def show_fatal_configuration_error(error: ConfigurationError) -> NoReturn:
    """Show a setup error and stop the current Streamlit run."""

    st.error(str(error))
    st.info("Create a local .env file from .env.example and add OPENAI_API_KEY.")
    st.stop()


def _analyze_submitted_resume(container: ApplicationContainer) -> None:
    """Run analysis for the submitted resume and store user-safe state."""

    submitted_resume = str(st.session_state.submitted_resume)
    try:
        with st.spinner("Analyzing resume..."):
            st.session_state.analysis_result = container.analyze_resume.execute(
                submitted_resume
            )
        st.session_state.analysis_error = ""
    except InvalidResumeError as error:
        st.session_state.analysis_error = str(error)
    except AIProviderError as error:
        LOGGER.error("analysis_failed user_safe_error=%s", error)
        st.session_state.analysis_error = str(error)
    except ResumeAnalyzerError as error:
        LOGGER.error(
            "analysis_expected_failure error_type=%s", type(error).__name__
        )
        st.session_state.analysis_error = str(error)
    except Exception:
        LOGGER.exception("analysis_unexpected_failure")
        st.session_state.analysis_error = (
            "An unexpected error occurred. Please retry or contact support."
        )


def main() -> None:
    """Render the resume submission and analysis workflow."""

    st.set_page_config(
        page_title="AI Resume Analyzer",
        page_icon="📄",
        layout="wide",
    )
    initialize_state()
    st.title("AI Resume Analyzer")
    st.caption("Get evidence-based resume feedback and career direction.")

    try:
        container = get_container()
    except ConfigurationError as error:
        show_fatal_configuration_error(error)

    with st.form("resume_submission"):
        resume_text = st.text_area(
            "Paste Resume Text",
            height=320,
            max_chars=get_settings().max_resume_chars,
            placeholder="Paste the complete text of your resume here...",
        )
        submitted = st.form_submit_button("Submit Resume", type="primary")

    if submitted:
        st.session_state.submitted_resume = resume_text.strip()
        st.session_state.analysis_result = None
        st.session_state.analysis_error = ""
        if st.session_state.submitted_resume:
            st.success("Resume submitted. Review it, then select Analyze Resume.")
        else:
            st.warning("Paste resume text before submitting it.")

    submitted_resume = str(st.session_state.submitted_resume)
    if submitted_resume:
        st.divider()
        st.subheader("Submitted Resume")
        st.text_area(
            "Resume preview", value=submitted_resume, height=180, disabled=True
        )
        if st.button("Analyze Resume", type="primary"):
            _analyze_submitted_resume(container)

    if st.session_state.analysis_error:
        st.error(st.session_state.analysis_error)
    if st.session_state.analysis_result:
        st.divider()
        render_analysis(st.session_state.analysis_result)
        st.caption("AI output is advisory. Verify all claims before using this resume.")
