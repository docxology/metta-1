"""Test orchestration helpers for DAF."""

from __future__ import annotations

import logging
import subprocess
from pathlib import Path
from typing import Optional

LOGGER = logging.getLogger(__name__)


def run_tests(test_pattern: Optional[str] = None) -> int:
    """Execute the DAF test suite via ``uv``.

    Args:
        test_pattern: Optional test pattern to filter tests.

    Returns:
        Exit code from the test run.
    """

    # Project root (metta/) and daf/tests
    project_root = Path(__file__).parents[4]  # operations -> daf -> src -> daf -> metta
    tests_dir = project_root / "daf" / "tests"

    cmd = ["uv", "run", "pytest", str(tests_dir), "-v"]

    if test_pattern:
        cmd.extend(["-k", test_pattern])

    LOGGER.info("Running DAF tests", {"command": cmd})
    completed = subprocess.run(cmd, cwd=project_root, check=False)
    return completed.returncode
