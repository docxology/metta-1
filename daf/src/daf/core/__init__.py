"""
DAF Core Components

<<<<<<< Updated upstream
This module provides core DAF functionality including:
- Adaptive Controllers
- Curriculum Managers
- RL Trainers
"""

from .adaptive_controller import DAFAdaptiveConfig, DAFAdaptiveController
from .curriculum_manager import DAFCurriculumConfig, DAFCurriculumManager
from .rl_trainer import DAFRlConfig, DAFRlTrainer

__all__ = [
    "DAFAdaptiveController",
    "DAFAdaptiveConfig",
    "DAFCurriculumManager",
    "DAFCurriculumConfig",
    "DAFRlTrainer",
    "DAFRlConfig",
=======
Core functionality for the Distributed Agent Framework including:
- Simulation engine and runners
- Installation management
- Validation systems
- Configuration management
"""

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
        elif name == "InstallationManager":
            from daf.core.installation import InstallationManager
            return InstallationManager
        elif name == "SystemValidator":
            from daf.core.validation import SystemValidator
            return SystemValidator
        elif name == "ConfigurationManager":
            from daf.config.configuration import ConfigurationManager
            return ConfigurationManager
    except ImportError as e:
        raise ImportError(f"Failed to import {name}: {e}")

# Create lazy module for public API
class _LazyModule:
    def __getattr__(self, name):
        return _lazy_import(name)

__all__ = [
    "SimulationRunner",
    "MettaEngine",
    "InstallationManager",
    "SystemValidator",
    "ConfigurationManager",
>>>>>>> Stashed changes
]
