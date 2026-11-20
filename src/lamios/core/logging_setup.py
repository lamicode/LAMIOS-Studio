"""Structured rotating file and console logging subsystem for LAMIOS Studio."""

from __future__ import annotations

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def configure_logging(
    logs_dir: Path,
    log_level: str = "INFO",
    log_filename: str = "lamios.log",
    max_bytes: int = 5 * 1024 * 1024,
    backup_count: int = 3,
) -> logging.Logger:
    """Configure the root `lamios` logger with console and rotating file handlers."""
    logs_dir.mkdir(parents=True, exist_ok=True)
    log_file = logs_dir / log_filename

    level = getattr(logging, log_level.upper(), logging.INFO)
    logger = logging.getLogger("lamios")
    logger.setLevel(level)
    logger.propagate = False

    for existing_handler in list(logger.handlers):
        existing_handler.close()
        logger.removeHandler(existing_handler)

    formatter = logging.Formatter(fmt=LOG_FORMAT, datefmt=DATE_FORMAT)

    file_handler = RotatingFileHandler(
        filename=log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.info("LAMIOS logging initialized (level=%s, file=%s)", log_level.upper(), log_file)
    return logger


def get_logger(name: str) -> logging.Logger:
    """Return a child logger within the `lamios` namespace."""
    if name.startswith("lamios.") or name == "lamios":
        return logging.getLogger(name)
    return logging.getLogger(f"lamios.{name}")
