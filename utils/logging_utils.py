"""
logging_utils.py
----------------

Centralised logging configuration for the Æther system.  This module
defines helper functions to configure Python's logging subsystem and
retrieve loggers with consistent formatting across all modules.

Two output formats are supported:

* Human‑readable logs with ISO‑8601 timestamps and module names.
* JSON logs suitable for ingestion by log aggregation systems.

The choice of format can be controlled via the `AE_LOG_JSON`
environment variable; set it to a truthy value (e.g. ``1``) to
enable JSON output.
"""

from __future__ import annotations

import json
import logging
import os
from typing import Any, Dict


class JsonFormatter(logging.Formatter):
    """Format log records as structured JSON."""

    def format(self, record: logging.LogRecord) -> str:
        log_dict: Dict[str, Any] = {
            'timestamp': self.formatTime(record, datefmt='%Y-%m-%dT%H:%M:%SZ'),
            'level': record.levelname,
            'name': record.name,
            'message': record.getMessage(),
        }
        if record.exc_info:
            log_dict['exception'] = self.formatException(record.exc_info)
        return json.dumps(log_dict)


def setup_logging(default_level: int = logging.INFO) -> None:
    """Configure the root logger according to environment settings.

    If the ``AE_LOG_JSON`` environment variable is truthy the logs
    will be emitted in JSON format; otherwise they default to a
    human‑readable format.  The configuration is applied only once.

    Parameters
    ----------
    default_level : int, optional
        Logging level to set if not already configured.  Defaults to
        ``logging.INFO``.
    """
    root = logging.getLogger()
    if root.handlers:
        # Assume logging is already configured by the parent
        return
    handler = logging.StreamHandler()
    if os.getenv('AE_LOG_JSON', '').lower() in {'1', 'true', 'yes'}:
        formatter = JsonFormatter()
    else:
        formatter = logging.Formatter(
            fmt='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            datefmt='%Y-%m-%dT%H:%M:%SZ',
        )
    handler.setFormatter(formatter)
    root.addHandler(handler)
    root.setLevel(default_level)


def get_logger(name: str) -> logging.Logger:
    """Retrieve a named logger after ensuring logging is configured."""
    setup_logging()
    return logging.getLogger(name)


__all__ = ['setup_logging', 'get_logger']