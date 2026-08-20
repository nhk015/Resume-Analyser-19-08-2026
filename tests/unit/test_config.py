"""Tests for environment-backed application settings."""

import pytest
from pydantic import ValidationError

from resume_analyzer.config import Settings


def test_settings_load_uppercase_dotenv_key(tmp_path):
    """Conventional uppercase .env names should populate lowercase fields."""

    env_file = tmp_path / ".env"
    env_file.write_text("OPENAI_API_KEY=test-key\n", encoding="utf-8")

    settings = Settings(_env_file=env_file)

    assert settings.openai_api_key == "test-key"
    assert settings.has_openai_key


def test_settings_reject_unknown_log_level():
    """Invalid logging configuration should fail during settings validation."""

    with pytest.raises(ValidationError):
        Settings(log_level="verbose")