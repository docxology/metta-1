"""Operational entry points for DAF infrastructure."""

from .docs import regenerate_docs, list_metta_options, run_docs
from .examples import run_examples
from .setup import perform_setup
from .tests import run_tests
from .validation import run_validation

__all__ = [
    "perform_setup",
    "run_examples",
    "run_tests",
    "run_validation",
    "regenerate_docs",
    "list_metta_options",
    "run_docs",
]
