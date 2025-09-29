"""Validation utilities for ensuring real Metta usage in DAF."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict


@dataclass(slots=True)
class ValidationResults:
    """Simplified validation result container."""

    overall_success: bool
    details: Dict[str, bool]


def validate_real_usage() -> ValidationResults:
    """Run core validation routines using ``uv``."""

    root = Path(__file__).parent.parent.parent
    examples_dir = root / "examples"

    examples_success = run_examples(examples_dir)
    tests_success = run_tests()

    details = {
        "examples": examples_success,
        "tests": tests_success,
    }

    return ValidationResults(overall_success=all(details.values()), details=details)


def run_examples(examples_dir: Path) -> bool:
    """Execute examples via ``uv``."""

    from ..operations.examples import run_examples as run_examples_op

    results = run_examples_op(examples_dir)
    return all(result.success for result in results)


def run_tests() -> bool:
    """Execute tests via ``uv``."""

    from ..operations.tests import run_tests as run_tests_op

    return run_tests_op() == 0
