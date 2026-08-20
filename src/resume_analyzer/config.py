"""Application configuration loaded from environment variables."""

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Validated runtime configuration.

    Secrets are read from the environment or a local `.env` file and are never
    given a default value in source code.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    openai_api_key: str = Field(default="", repr=False)
    openai_model: str = "gpt-4o-mini"
    app_env: str = "development"
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    max_resume_chars: int = Field(default=30_000, ge=1_000, le=100_000)
    openai_timeout_seconds: float = Field(default=45.0, gt=0, le=180)

    @property
    def has_openai_key(self) -> bool:
        """Return whether an OpenAI key has been configured."""

        return bool(self.openai_api_key.strip())


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Return the process-wide validated settings instance."""

    return Settings()
