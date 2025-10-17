"""
Centralized logging configuration for the application.

Call `configure_logging()` early (for example from `main.py`) so all
modules inherit the same formatting and handlers. This logs to stdout
which is compatible with Render/GHA and other hosts.
"""
import logging
import os
import sys


def configure_logging(level: str | None = None) -> None:
    """Configure root logger to output to stdout.

    - level: optional string like 'INFO' or 'DEBUG'. If omitted, reads
      from the environment variable LOG_LEVEL or defaults to INFO.
    """
    root = logging.getLogger()
    if root.handlers:
        # Already configured (avoid double configuration in tests)
        return

    level_name = level or os.environ.get("LOG_LEVEL", "INFO")
    numeric_level = getattr(logging, level_name.upper(), logging.INFO)

    handler = logging.StreamHandler(stream=sys.stdout)
    fmt = "%(asctime)s %(levelname)s [%(name)s] %(message)s"
    handler.setFormatter(logging.Formatter(fmt))

    root.setLevel(numeric_level)
    root.addHandler(handler)

