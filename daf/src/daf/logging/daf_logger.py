#!/usr/bin/env python3
"""
DAF Logger System

Provides comprehensive logging for the DAF fork with structured output.
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional


class DAFLogger:
    """
    Enhanced Logger for DAF Fork

    Provides structured logging with context and metadata.
    """

    def __init__(self, name: str, context: Optional[Dict[str, Any]] = None):
        """
        Initialize DAF logger

        Args:
            name: Logger name
            context: Additional context for logging
        """
        self.logger = logging.getLogger(name)
        self.context = context or {}
        self.component = name

    def _format_message(self, level: str, message: str, extra: Optional[Dict] = None) -> str:
        """Format log message with context"""
        context_str = ""
        if self.context:
            context_items = [f"{k}={v}" for k, v in self.context.items()]
            context_str = f"[{', '.join(context_items)}] "

        extra_str = ""
        if extra:
            extra_items = [f"{k}={v}" for k, v in extra.items()]
            extra_str = f" | {', '.join(extra_items)}"

        timestamp = datetime.now().strftime("%H:%M:%S")
        return f"[{timestamp}] {context_str}{message}{extra_str}"

    def info(self, message: str, extra: Optional[Dict] = None):
        """Log info message"""
        formatted = self._format_message("INFO", message, extra)
        self.logger.info(formatted)

    def debug(self, message: str, extra: Optional[Dict] = None):
        """Log debug message"""
        formatted = self._format_message("DEBUG", message, extra)
        self.logger.debug(formatted)

    def warning(self, message: str, extra: Optional[Dict] = None):
        """Log warning message"""
        formatted = self._format_message("WARNING", message, extra)
        self.logger.warning(formatted)

    def error(self, message: str, extra: Optional[Dict] = None):
        """Log error message"""
        formatted = self._format_message("ERROR", message, extra)
        self.logger.error(formatted)

    def critical(self, message: str, extra: Optional[Dict] = None):
        """Log critical message"""
        formatted = self._format_message("CRITICAL", message, extra)
        self.logger.critical(formatted)

    def with_context(self, **kwargs) -> "DAFLogger":
        """Create logger with additional context"""
        new_context = self.context.copy()
        new_context.update(kwargs)
        return DAFLogger(self.logger.name, new_context)


def setup_daf_logging(log_level: str = "INFO", log_file: Optional[str] = None, console_output: bool = True) -> None:
    """
    Setup comprehensive logging for DAF

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Optional log file path
        console_output: Whether to output to console
    """
    # Create loggers
    root_logger = logging.getLogger()
    daf_logger = logging.getLogger("daf")

    # Clear existing handlers
    root_logger.handlers.clear()
    daf_logger.handlers.clear()

    # Set log level
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    root_logger.setLevel(numeric_level)
    daf_logger.setLevel(numeric_level)

    # Create formatters
    detailed_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    simple_formatter = logging.Formatter("%(levelname)s: %(message)s")

    # File handler
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(detailed_formatter)
        root_logger.addHandler(file_handler)
        daf_logger.addHandler(file_handler)

    # Console handler
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(numeric_level)
        console_handler.setFormatter(simple_formatter)
        root_logger.addHandler(console_handler)
        daf_logger.addHandler(console_handler)

    # Create specific loggers for DAF components
    components = ["daf.core", "daf.tools", "daf.setup", "daf.logging", "daf.wrappers"]

    for component in components:
        comp_logger = logging.getLogger(component)
        comp_logger.setLevel(numeric_level)

    logging.info("DAF logging system initialized")
