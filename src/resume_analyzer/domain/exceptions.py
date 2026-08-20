"""Application-specific exception types."""


class ResumeAnalyzerError(Exception):
    """Base class for expected, user-safe application errors."""


class InvalidResumeError(ResumeAnalyzerError):
    """Raised when resume text cannot be analyzed safely."""


class ConfigurationError(ResumeAnalyzerError):
    """Raised when required runtime configuration is missing."""


class AIProviderError(ResumeAnalyzerError):
    """Raised when the AI provider cannot return a valid analysis."""
