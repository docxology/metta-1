#!/usr/bin/env python3
"""
DAF Log Manager

Manages logging configuration and log files for the DAF fork.
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional


class LogManager:
    """
    Log Manager for DAF Fork

    Handles log file management, rotation, and configuration.
    """

    def __init__(self, log_directory: Optional[str] = None):
        """
        Initialize log manager

        Args:
            log_directory: Directory for log files
        """
        self.log_directory = Path(log_directory) if log_directory else Path("daf/logs")
        self.log_directory.mkdir(parents=True, exist_ok=True)

        self.main_log = self.log_directory / "daf.log"
        self.test_log = self.log_directory / "tests.log"
        self.performance_log = self.log_directory / "performance.log"
        self.error_log = self.log_directory / "errors.log"

    def setup_component_logging(self, component: str, level: str = "INFO"):
        """Setup logging for a specific DAF component"""
        logger = logging.getLogger(component)
        numeric_level = getattr(logging, level.upper(), logging.INFO)
        logger.setLevel(numeric_level)

        # Create component-specific log file
        component_log = self.log_directory / f"{component.replace('.', '_')}.log"

        # File handler for component
        handler = logging.FileHandler(component_log)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        handler.setLevel(numeric_level)

        # Avoid duplicate handlers
        if handler not in logger.handlers:
            logger.addHandler(handler)

        return logger

    def rotate_logs(self, max_files: int = 10):
        """Rotate log files to prevent them from growing too large"""
        log_files = [self.main_log, self.test_log, self.performance_log, self.error_log]

        for log_file in log_files:
            if log_file.exists() and log_file.stat().st_size > 10 * 1024 * 1024:  # 10MB
                self._rotate_file(log_file, max_files)

    def _rotate_file(self, log_file: Path, max_files: int):
        """Rotate a single log file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Create backup files
        for i in range(max_files - 1, 0, -1):
            old_file = log_file.with_suffix(f".{i}.bak")
            new_file = log_file.with_suffix(f".{i + 1}.bak")

            if old_file.exists():
                old_file.rename(new_file)

        # Create first backup
        first_backup = log_file.with_suffix(".1.bak")
        log_file.rename(first_backup)

        # Create new empty log file
        log_file.touch()

        logging.info(f"Rotated log file: {log_file} -> {first_backup}")

    def get_log_stats(self) -> Dict[str, Any]:
        """Get statistics about log files"""
        stats = {}

        log_files = {
            "main": self.main_log,
            "tests": self.test_log,
            "performance": self.performance_log,
            "errors": self.error_log,
        }

        total_size = 0
        for name, log_file in log_files.items():
            if log_file.exists():
                size = log_file.stat().st_size
                stats[name] = {"size": size, "lines": self._count_lines(log_file), "exists": True}
                total_size += size
            else:
                stats[name] = {"size": 0, "lines": 0, "exists": False}

        stats["total_size"] = total_size
        stats["directory"] = str(self.log_directory)

        return stats

    def _count_lines(self, file_path: Path) -> int:
        """Count lines in a file"""
        try:
            with open(file_path, "r") as f:
                return sum(1 for _ in f)
        except:
            return 0

    def cleanup_old_logs(self, days_old: int = 30):
        """Clean up log files older than specified days"""
        cutoff_time = datetime.now().timestamp() - (days_old * 24 * 3600)

        for log_file in self.log_directory.glob("*.log"):
            if log_file.stat().st_mtime < cutoff_time:
                log_file.unlink()
                logging.info(f"Cleaned up old log file: {log_file}")

    def archive_logs(self, archive_dir: Optional[str] = None) -> Optional[str]:
        """
        Archive current log files

        Args:
            archive_dir: Directory to store archives

        Returns:
            Path to archive if successful
        """
        if not archive_dir:
            archive_dir = self.log_directory / "archives"
            archive_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_name = f"daf_logs_{timestamp}.tar.gz"
        archive_path = Path(archive_dir) / archive_name

        try:
            import tarfile

            with tarfile.open(archive_path, "w:gz") as tar:
                for log_file in self.log_directory.glob("*.log"):
                    tar.add(log_file, arcname=log_file.name)

            logging.info(f"Created log archive: {archive_path}")
            return str(archive_path)

        except Exception as e:
            logging.error(f"Failed to create log archive: {e}")
            return None
