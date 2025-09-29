"""
DAF Configuration Validation

Validation system for DAF configurations.
"""

from typing import Any, List, Optional

from daf.config.models import SimulationConfig, GlobalConfig, ProfileConfig
from daf.core.validation import ValidationResult


class ConfigurationValidator:
    """Validates DAF configurations."""

    def validate_config(self, config: Any) -> ValidationResult:
        """Validate any configuration object."""
        try:
            # Basic validation - check if it's a valid object
            if not config:
                return ValidationResult(
                    is_valid=False,
                    message="Configuration cannot be empty",
                    issues=["Configuration is empty or None"]
                )

            # Type-specific validation
            if isinstance(config, SimulationConfig):
                return self._validate_simulation_config(config)
            elif isinstance(config, GlobalConfig):
                return self._validate_global_config(config)
            elif isinstance(config, ProfileConfig):
                return self._validate_profile_config(config)
            else:
                # For dict configs, do basic structure validation
                return self._validate_basic_config(config)

        except Exception as e:
            return ValidationResult(
                is_valid=False,
                message=f"Configuration validation failed: {e}",
                issues=[str(e)]
            )

    def _validate_simulation_config(self, config: SimulationConfig) -> ValidationResult:
        """Validate simulation configuration."""
        issues = []

        if not config.name:
            issues.append("Simulation configuration must have a name")

        if config.environment.num_agents < 1:
            issues.append("Number of agents must be positive")

        if config.training.total_timesteps < 1:
            issues.append("Total timesteps must be positive")

        if issues:
            return ValidationResult(
                is_valid=False,
                message="Simulation configuration validation failed",
                issues=issues
            )

        return ValidationResult(
            is_valid=True,
            message="Simulation configuration is valid"
        )

    def _validate_global_config(self, config: GlobalConfig) -> ValidationResult:
        """Validate global configuration."""
        return ValidationResult(
            is_valid=True,
            message="Global configuration is valid"
        )

    def _validate_profile_config(self, config: ProfileConfig) -> ValidationResult:
        """Validate profile configuration."""
        issues = []

        if not config.name:
            issues.append("Profile configuration must have a name")

        if issues:
            return ValidationResult(
                is_valid=False,
                message="Profile configuration validation failed",
                issues=issues
            )

        return ValidationResult(
            is_valid=True,
            message="Profile configuration is valid"
        )

    def _validate_basic_config(self, config: dict) -> ValidationResult:
        """Validate basic configuration structure."""
        issues = []

        if not isinstance(config, dict):
            issues.append("Configuration must be a dictionary")

        if issues:
            return ValidationResult(
                is_valid=False,
                message="Basic configuration validation failed",
                issues=issues
            )

        return ValidationResult(
            is_valid=True,
            message="Basic configuration structure is valid"
        )
