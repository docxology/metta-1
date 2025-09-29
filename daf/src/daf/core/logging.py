"""
DAF Logging Configuration

Centralized logging configuration for DAF framework.
"""

import logging
import sys
from typing import Optional


def setup_logging(
    level: str = "INFO",
    format: str = "structured",
    output: str = "both"
) -> None:
    """
    Setup logging configuration for DAF.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
        format: Log format style (structured, simple)
        output: Output destination (console, file, both)
    """
    # Clear existing handlers
    root_logger = logging.getLogger("daf")
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Set logging level
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    root_logger.setLevel(numeric_level)

    # Create formatter
    if format == "structured":
        formatter = logging.Formatter(
            fmt='%(asctime)s | %(name)s | %(levelname)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    else:
        formatter = logging.Formatter(
            fmt='%(levelname)s: %(message)s'
        )

    # Setup console handler
    if output in ["console", "both"]:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        console_handler.setLevel(numeric_level)
        root_logger.addHandler(console_handler)

    # Setup file handler
    if output in ["file", "both"]:
        try:
            file_handler = logging.FileHandler("daf.log")
            file_handler.setFormatter(formatter)
            file_handler.setLevel(numeric_level)
            root_logger.addHandler(file_handler)
        except Exception:
            # If file logging fails, continue with console only
            pass

    # Prevent duplicate messages from parent loggers
    root_logger.propagate = False


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for the given name."""
    return logging.getLogger(f"daf.{name}")
