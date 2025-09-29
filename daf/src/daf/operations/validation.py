"""Validation commands for DAF."""

from __future__ import annotations

import logging

from ..validation.real_usage import validate_real_usage

LOGGER = logging.getLogger(__name__)


def run_validation() -> bool:
    """Run the comprehensive DAF validation sequence."""

    LOGGER.info("Starting DAF validation")
    results = validate_real_usage()
    LOGGER.info("Validation complete", {"success": results.overall_success})
    return results.overall_success
