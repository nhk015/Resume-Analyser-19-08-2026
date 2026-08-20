"""Centralized redacted logging configuration."""

import logging
import sys


class SecretRedactingFilter(logging.Filter):
    """Prevent common secret values from appearing in log messages."""

    _SENSITIVE_NAMES = ("api_key", "authorization", "password", "secret", "token")

    def filter(self, record: logging.LogRecord) -> bool:
        """Redact sensitive key-value text in the formatted message."""

        message = record.getMessage()
        lowered = message.lower()
        if any(name in lowered for name in self._SENSITIVE_NAMES):
            record.msg = "Sensitive log message redacted"
            record.args = ()
        return True


def configure_logging(level: str) -> None:
    """Configure consistent, timestamped application logging."""

    handler = logging.StreamHandler(sys.stdout)
    handler.addFilter(SecretRedactingFilter())
    handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
    )
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(getattr(logging, level.upper()))
