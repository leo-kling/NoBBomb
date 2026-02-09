"""Structured Logger, compatible with Google Cloud Logging."""

import json
import logging
from datetime import UTC, datetime
from typing import Any

# pylint: disable=missing-function-docstring
# Because it's self explanatory here


class GCPLogger:
    """Structured JSON logger compatible with Google Cloud Logging."""

    def __init__(self, debug: bool = False) -> None:
        self.logger = logging.getLogger("GCPLogger")
        self.logger.setLevel(logging.DEBUG if debug else logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(JSONFormatter())
        self.logger.addHandler(handler)
        self.logger.propagate = False

    def _log(self, level: str, msg: str, **kwargs: Any) -> None:
        log_entry = {
            "message": msg,
            "time": datetime.now(UTC).isoformat(),
            **kwargs,
        }
        self.logger.log(getattr(logging, level.upper()), log_entry)

    def debug(self, msg: str, **kwargs: Any) -> None:
        self._log("debug", msg, **kwargs)

    def info(self, msg: str, **kwargs: Any) -> None:
        self._log("info", msg, **kwargs)

    def warning(self, msg: str, **kwargs: Any) -> None:
        self._log("warning", msg, **kwargs)

    def error(self, msg: str, **kwargs: Any) -> None:
        self._log("error", msg, **kwargs)

    def critical(self, msg: str, **kwargs: Any) -> None:
        self._log("critical", msg, **kwargs)


class JSONFormatter(logging.Formatter):
    """Formats log records as JSON."""

    def format(self, record: logging.LogRecord) -> str:
        log_record = (
            record.msg
            if isinstance(record.msg, dict)
            else {"message": record.getMessage()}
        )
        log_record.setdefault("severity", record.levelname)
        log_record.setdefault("time", datetime.now(UTC).isoformat())
        return json.dumps(log_record)
