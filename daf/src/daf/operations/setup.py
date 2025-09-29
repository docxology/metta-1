"""Setup operations for DAF.

This module exposes high level functions that wrap the reusable setup
components defined under ``src/daf``. It is the single place orchestrating
environment bootstrap so callers (CLI, scripts, tests) can rely on a stable
contract that automatically uses ``uv`` for subprocess management.
"""

from __future__ import annotations

import logging
import subprocess
from pathlib import Path
from typing import Optional

from ..config.daf_config import DAFConfig
from ..setup.daf_setup import initialize_daf_environment

LOGGER = logging.getLogger(__name__)


def perform_setup(config: Optional[DAFConfig] = None) -> None:
    """Run the full DAF setup sequence."""

    initialize_daf_environment(config)


def activate_environment(extra_args: Optional[list[str]] = None) -> None:
    """Activate the DAF environment using ``uv``.

    Args:
        extra_args: Optional additional arguments to pass to the activation
            script.
    """

    daf_root = Path(__file__).parent.parent.parent
    script = daf_root / "activate_daf.py"
    cmd = ["uv", "run", "python", str(script)]
    if extra_args:
        cmd.extend(extra_args)

    LOGGER.info("Activating DAF environment", {"command": cmd})
    subprocess.run(cmd, check=True)
