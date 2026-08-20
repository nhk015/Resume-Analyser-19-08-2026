"""Unit tests for application settings."""

import pytest
from pydantic import ValidationError

from resume_analyzer.config import Settings


def test_settings_loads_uppercase_dotenv_key_without_exposing_value(tmp_path):
    """The conventional uppercase key name maps to the Settings field."""

    env_file = tmp_path / ".env"
    env_file.write_text(
        "OPENAI_API_KEY=unit-test-key\nOPENAI_MODEL=test-model\n",
        encoding="utf-8",
    )

    settings = Settings(_env_file=env_file)

    assert settings.openai_api_key == "unit-test-key"
    assert settings.openai_model == "test-model"
    assert settings.has_openai_key
    assert "unit-test-key" not in repr(settings)


def test_settings_defaults_are_deterministic(monkeypatch):
    """Settings can be built without a key and use stable development defaults."""

    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_MODEL", raising=False)

    settings = Settings(_env_file=None)

    assert settings.openai_api_key == ""
    assert settings.openai_model == "gpt-4o-mini"
    assert settings.app_env == "development"
    assert settings.log_level == "INFO"
    assert settings.max_resume_chars == 30_000
    assert settings.openai_timeout_seconds == 45.0
    assert not settings.has_openai_key


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("max_resume_chars", 999),
        ("max_resume_chars", 100_001),
        ("openai_timeout_seconds", 0),
        ("openai_timeout_seconds", 181),
        ("log_level", "verbose"),
    ],
)
def test_settings_rejects_invalid_values(field, value):
    """Invalid operational settings fail before application startup."""

    with pytest.raises(ValidationError):
        Settings(_env_file=None, **{field: value})


def test_settings_ignores_unknown_environment_values(tmp_path):
    """Unrelated environment entries do not become application settings."""

    env_file = tmp_path / ".env"
    env_file.write_text(
        "OPENAI_API_KEY=test-key\nUNSUPPORTED_SETTING=ignored\n",
        encoding="utf-8",
    )

    settings = Settings(_env_file=env_file)

    assert settings.openai_api_key == "test-key"
    assert not hasattr(settings, "unsupported_setting")
