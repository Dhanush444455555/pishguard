"""
core/logger.py — Structured logging for PhishGuard AI.
Provides color-coded console output for development and optional
JSON structured logging for production environments.
"""

import logging
import sys
import os
from datetime import datetime, timezone


# ── ANSI Colors ───────────────────────────────────────────────────────────────
class _Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    BG_RED = "\033[41m"


LEVEL_COLORS = {
    "DEBUG": _Colors.DIM + _Colors.CYAN,
    "INFO": _Colors.GREEN,
    "WARNING": _Colors.YELLOW,
    "ERROR": _Colors.RED,
    "CRITICAL": _Colors.BG_RED + _Colors.WHITE + _Colors.BOLD,
}


# ── Custom Formatters ─────────────────────────────────────────────────────────
class ColorFormatter(logging.Formatter):
    """Color-coded console formatter for development."""

    def format(self, record: logging.LogRecord) -> str:
        color = LEVEL_COLORS.get(record.levelname, _Colors.WHITE)
        ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        level = f"{color}{record.levelname:<8}{_Colors.RESET}"
        name = f"{_Colors.CYAN}{record.name}{_Colors.RESET}"
        msg = record.getMessage()
        return f"{_Colors.DIM}{ts}{_Colors.RESET} | {level} | {name} | {msg}"


class JSONFormatter(logging.Formatter):
    """Structured JSON formatter for production log aggregation."""

    def format(self, record: logging.LogRecord) -> str:
        import json
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        if record.exc_info and record.exc_info[1]:
            log_entry["exception"] = str(record.exc_info[1])
        if hasattr(record, "correlation_id"):
            log_entry["correlation_id"] = record.correlation_id
        return json.dumps(log_entry)


# ── Logger Factory ────────────────────────────────────────────────────────────
def setup_logger(
    name: str = "phishguard",
    level: str = "INFO",
    log_file: str = None,
    json_mode: bool = False,
) -> logging.Logger:
    """
    Create and configure a logger instance.

    Args:
        name: Logger name (dot-separated hierarchy supported).
        level: Logging level string.
        log_file: Optional file path for persistent logs.
        json_mode: If True, use JSON formatter for all handlers.
    """
    log = logging.getLogger(name)
    log.setLevel(getattr(logging, level.upper(), logging.INFO))

    # Prevent duplicate handlers on re-import
    if log.handlers:
        return log

    # ── Console Handler ───────────────────────────────────────────────────
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(getattr(logging, level.upper(), logging.INFO))
    if json_mode:
        console.setFormatter(JSONFormatter())
    else:
        console.setFormatter(ColorFormatter())
    log.addHandler(console)

    # ── File Handler (optional) ───────────────────────────────────────────
    if log_file:
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(
            JSONFormatter() if json_mode
            else logging.Formatter(
                "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )
        log.addHandler(file_handler)

    return log


# ── Default Application Logger ────────────────────────────────────────────────
logger = setup_logger("phishguard")

# ── Security Audit Logger (separate stream for compliance) ────────────────────
audit_logger = setup_logger(
    "phishguard.audit",
    level="INFO",
    log_file="logs/audit.log",
)
