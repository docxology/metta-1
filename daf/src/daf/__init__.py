"""
<<<<<<< Updated upstream
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
=======
DAF (Distributed Agent Framework)

A professional, hands-off fork of Metta AI focused on providing automated,
configurable multi-agent reinforcement learning simulations.

This package provides:
- Automated setup and installation
- Configurable simulation environments
- Production-ready tooling and validation
- Comprehensive testing and documentation
"""

from typing import Any, Dict, Optional

# Lazy imports to avoid circular dependencies
def _lazy_import(name: str):
    """Lazy import to avoid circular dependencies."""
    try:
        if name == "SimulationRunner":
            from daf.core.simulation import SimulationRunner
            return SimulationRunner
        elif name == "MettaEngine":
            from daf.core.engine import MettaEngine
            return MettaEngine
        elif name == "ConfigurationManager":
            from daf.config.configuration import ConfigurationManager
            return ConfigurationManager
        elif name == "SystemValidator":
            from daf.core.validation import SystemValidator
            return SystemValidator
    except ImportError as e:
        raise ImportError(f"Failed to import {name}: {e}")

# Create lazy module for public API
class _LazyModule:
    def __getattr__(self, name):
        return _lazy_import(name)

# Create lazy module for public API
core = _LazyModule()

__version__ = "0.1.0"
__author__ = "DAF Contributors"
__description__ = "Distributed Agent Framework - Professional Metta AI fork"

# Main API exports
__all__ = [
    "core",
    "__version__",
]


def get_version() -> str:
    """Get the current version of DAF."""
    return __version__


def get_info() -> Dict[str, Any]:
    """Get information about the DAF installation."""
    return {
        "version": __version__,
        "author": __author__,
        "description": __description__,
        "package": "daf",
    }


# Initialize logging when the package is imported
def _initialize_logging() -> None:
    """Initialize logging configuration."""
    import logging

    from daf.core.logging import setup_logging

    # Only setup if not already configured
    if not logging.getLogger("daf").handlers:
        setup_logging()


_initialize_logging()
>>>>>>> Stashed changes
