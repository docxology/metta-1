"""
DAF Scripts Package

Contains all DAF setup and utility scripts.
"""

from scripts.install import main as install_main
from scripts.run_experiment import main as run_experiment_main
from scripts.validate import main as validate_main

__all__ = [
    "install_main",
    "validate_main",
    "run_experiment_main",
]
