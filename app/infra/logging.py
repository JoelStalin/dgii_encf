"""Logging configuration with JSON output."""
from __future__ import annotations

import logging
import sys
from typing import Any, Mapping

import structlog
from pythonjsonlogger import jsonlogger


class _JsonFormatter(jsonlogger.JsonFormatter):
    """Ensure timestamps are ISO formatted and message key is consistent."""

    def process_log_record(self, log_record: Mapping[str, Any]) -> dict[str, Any]:
        record = dict(log_record)
        record.setdefault("level", record.pop("levelname", "").lower())
        return record


def configure_logging() -> None:
    """Configure stdlib and structlog JSON logging."""

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(_JsonFormatter())

    logging.basicConfig(level=logging.INFO, handlers=[handler], force=True)

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer(),
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
