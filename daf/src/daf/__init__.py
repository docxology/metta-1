"""
DAF (Data Analysis Framework) Fork

Main package for the DAF fork providing comprehensive Metta integration,
documentation generation, testing, and management capabilities.

This package contains all the infrastructure needed to work with Metta methods
through the DAF fork, including tools, wrappers, setup, logging, and CLI.
"""

from .cli.daf_cli import DAFCLI
from .cli.daf_cli import main as cli_main
from .config.daf_config import DAFConfig, DAFConfigManager
from .logging.daf_logger import DAFLogger
from .logging.log_manager import LogManager
from .logging import setup_daf_logging
from .setup.daf_setup import initialize_daf_environment
from .tools import generate_comprehensive_daf_docs, sync_daf_with_metta, verify_daf_coverage
from .wrappers.metta_wrapper import AdaptiveWrapper, CurriculumWrapper, MettaWrapper, RLWrapper

__version__ = "1.0.0"

__all__ = [
    # Setup and initialization
    "initialize_daf_environment",
    "DAFConfigManager",
    "DAFConfig",
    # Documentation tools
    "generate_comprehensive_daf_docs",
    "verify_daf_coverage",
    "sync_daf_with_metta",
    # Logging system
    "setup_daf_logging",
    "LogManager",
    "DAFLogger",
    # Wrappers
    "MettaWrapper",
    "AdaptiveWrapper",
    "RLWrapper",
    "CurriculumWrapper",
    # CLI interface
    "DAFCLI",
    "cli_main",
    # Version
    "__version__",
]
