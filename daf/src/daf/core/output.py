"""
DAF Output Management

Centralized output directory management for DAF ensuring all outputs
go to the proper locations and are organized consistently.
"""

import os
import shutil
from pathlib import Path
from typing import Optional, Union

from daf.core.logging import get_logger

logger = get_logger(__name__)


class OutputManager:
    """
    Manages output directories and files for DAF.

    Ensures all outputs are properly organized and accessible.
    """

    def __init__(self, base_output_dir: Optional[Union[str, Path]] = None):
        """
        Initialize output manager.

        Args:
            base_output_dir: Base directory for all outputs
        """
        self.base_output_dir = Path(base_output_dir) if base_output_dir else Path("outputs")
        self.base_output_dir.mkdir(parents=True, exist_ok=True)

        # Create standard subdirectories
        self._create_standard_directories()

    def _create_standard_directories(self) -> None:
        """Create standard output subdirectories."""
        standard_dirs = [
            "tests",
            "examples",
            "experiments",
            "logs",
            "checkpoints",
            "artifacts",
            "metrics",
            "replays",
            "analysis",
        ]

        for dir_name in standard_dirs:
            (self.base_output_dir / dir_name).mkdir(exist_ok=True)

    def get_output_path(self, category: str, name: str, create: bool = True) -> Path:
        """
        Get output path for a specific category and name.

        Args:
            category: Output category (tests, examples, experiments, etc.)
            name: Name of the specific output
            create: Whether to create the directory

        Returns:
            Path to the output location
        """
        category_dir = self.base_output_dir / category
        if create:
            category_dir.mkdir(parents=True, exist_ok=True)

        output_path = category_dir / name
        if create:
            output_path.mkdir(parents=True, exist_ok=True)

        return output_path

    def get_test_output_path(self, test_name: str, create: bool = True) -> Path:
        """
        Get output path for test outputs.

        Args:
            test_name: Name of the test
            create: Whether to create the directory

        Returns:
            Path to the test output location
        """
        return self.get_output_path("tests", test_name, create)

    def get_experiment_output_path(self, experiment_name: str, create: bool = True) -> Path:
        """
        Get output path for experiment outputs.

        Args:
            experiment_name: Name of the experiment
            create: Whether to create the directory

        Returns:
            Path to the experiment output location
        """
        return self.get_output_path("experiments", experiment_name, create)

    def get_example_output_path(self, example_name: str, create: bool = True) -> Path:
        """
        Get output path for example outputs.

        Args:
            example_name: Name of the example
            create: Whether to create the directory

        Returns:
            Path to the example output location
        """
        return self.get_output_path("examples", example_name, create)

    def get_log_path(self, name: str = "daf.log") -> Path:
        """
        Get path for log files.

        Args:
            name: Log filename

        Returns:
            Path to the log file location
        """
        return self.base_output_dir / "logs" / name

    def get_checkpoint_path(self, experiment_name: str, checkpoint_name: str) -> Path:
        """
        Get path for checkpoint files.

        Args:
            experiment_name: Name of the experiment
            checkpoint_name: Name of the checkpoint

        Returns:
            Path to the checkpoint location
        """
        checkpoint_dir = self.get_output_path("checkpoints", experiment_name)
        return checkpoint_dir / checkpoint_name

    def get_artifact_path(self, experiment_name: str, artifact_name: str) -> Path:
        """
        Get path for artifact files.

        Args:
            experiment_name: Name of the experiment
            artifact_name: Name of the artifact

        Returns:
            Path to the artifact location
        """
        artifact_dir = self.get_output_path("artifacts", experiment_name)
        return artifact_dir / artifact_name

    def get_metrics_path(self, experiment_name: str, metrics_name: str) -> Path:
        """
        Get path for metrics files.

        Args:
            experiment_name: Name of the experiment
            metrics_name: Name of the metrics file

        Returns:
            Path to the metrics location
        """
        metrics_dir = self.get_output_path("metrics", experiment_name)
        return metrics_dir / metrics_name

    def cleanup_old_outputs(self, days_old: int = 7) -> int:
        """
        Clean up old output directories.

        Args:
            days_old: Remove directories older than this many days

        Returns:
            Number of directories cleaned up
        """
        import time

        cleaned_count = 0
        cutoff_time = time.time() - (days_old * 24 * 60 * 60)

        for category_dir in self.base_output_dir.iterdir():
            if category_dir.is_dir():
                for output_dir in category_dir.iterdir():
                    if output_dir.is_dir():
                        # Check modification time
                        mtime = output_dir.stat().st_mtime
                        if mtime < cutoff_time:
                            logger.info(f"Cleaning up old output: {output_dir}")
                            shutil.rmtree(output_dir)
                            cleaned_count += 1

        if cleaned_count > 0:
            logger.info(f"Cleaned up {cleaned_count} old output directories")
        else:
            logger.info("No old output directories to clean up")

        return cleaned_count

    def get_output_info(self) -> dict:
        """
        Get information about current output structure.

        Returns:
            Dictionary with output information
        """
        info = {
            "base_output_dir": str(self.base_output_dir),
            "total_size": self._get_directory_size(self.base_output_dir),
            "categories": {},
        }

        for category_dir in self.base_output_dir.iterdir():
            if category_dir.is_dir():
                category_info = {
                    "path": str(category_dir),
                    "size": self._get_directory_size(category_dir),
                    "item_count": len(list(category_dir.iterdir())),
                }
                info["categories"][category_dir.name] = category_info

        return info

    def _get_directory_size(self, path: Path) -> int:
        """Get total size of directory in bytes."""
        total_size = 0
        try:
            for dirpath, dirnames, filenames in os.walk(path):
                for filename in filenames:
                    filepath = Path(dirpath) / filename
                    try:
                        total_size += filepath.stat().st_size
                    except (OSError, FileNotFoundError):
                        # Skip files that can't be accessed
                        pass
        except (OSError, FileNotFoundError):
            pass
        return total_size


# Global output manager instance
_output_manager: Optional[OutputManager] = None


def get_output_manager() -> OutputManager:
    """Get the global output manager instance."""
    global _output_manager
    if _output_manager is None:
        _output_manager = OutputManager()
    return _output_manager


def setup_output_manager(base_dir: Optional[Union[str, Path]] = None) -> OutputManager:
    """Setup and return the global output manager."""
    global _output_manager
    _output_manager = OutputManager(base_dir)
    return _output_manager


def get_experiment_output_path(experiment_name: str, create: bool = True) -> Path:
    """Get output path for an experiment."""
    return get_output_manager().get_experiment_output_path(experiment_name, create)


def get_test_output_path(test_name: str, create: bool = True) -> Path:
    """Get output path for a test."""
    return get_output_manager().get_test_output_path(test_name, create)


def get_example_output_path(example_name: str, create: bool = True) -> Path:
    """Get output path for an example."""
    return get_output_manager().get_example_output_path(example_name, create)


def cleanup_outputs(days_old: int = 7) -> int:
    """Clean up old output directories."""
    return get_output_manager().cleanup_old_outputs(days_old)
