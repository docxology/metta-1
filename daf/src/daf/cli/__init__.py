"""
<<<<<<< Updated upstream
DAF CLI Package

Provides command-line interface for the DAF fork.
"""

from .daf_cli import DAFCLI, main

__all__ = ["DAFCLI", "main"]
=======
DAF Command Line Interface

Main CLI interface for DAF providing commands for:
- Installation and setup
- Running experiments
- Configuration management
- Validation and diagnostics
"""

from daf.cli.install import install_command
from daf.cli.main import main
from daf.cli.run import run_command
from daf.cli.validate import validate_command

__all__ = [
    "main",
    "install_command",
    "run_command",
    "validate_command",
]
>>>>>>> Stashed changes
