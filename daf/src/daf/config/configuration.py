"""
DAF Configuration Manager

Centralized configuration management system for DAF providing:
- Hierarchical configuration loading
- Configuration validation and merging
- Profile-based configuration management
- Runtime configuration overrides
"""

import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from pydantic import ValidationError

from daf.config.models import (
    GlobalConfig,
    ProfileConfig,
    SimulationConfig,
)
from daf.config.validation import ConfigurationValidator
from daf.core.validation import ValidationResult

logger = logging.getLogger(__name__)


class ConfigurationManager:
    """
    Central configuration management system.

    Handles loading, validation, merging, and management of all DAF
    configuration files and objects.
    """

    def __init__(self, config_dir: Optional[Path] = None):
        """
        Initialize configuration manager.

        Args:
            config_dir: Base directory for configuration files
        """
        self.config_dir = config_dir or Path("configs")
        self.validator = ConfigurationValidator()
        self._loaded_configs: Dict[str, Any] = {}
        self._profiles: Dict[str, ProfileConfig] = {}

        # Create config directory if it doesn't exist
        self.config_dir.mkdir(parents=True, exist_ok=True)

        # Load built-in profiles
        self._load_builtin_profiles()

    def load_base_config(self) -> GlobalConfig:
        """Load base global configuration."""
        config_file = self.config_dir / "base" / "global.yaml"

        if not config_file.exists():
            logger.warning(f"Base config not found at {config_file}, using defaults")
            return GlobalConfig()

        return self.load_config_file(config_file)

    def load_config_file(self, config_path: Union[str, Path], validate: bool = True) -> Any:
        """
        Load configuration from file.

        Args:
            config_path: Path to configuration file
            validate: Whether to validate configuration

        Returns:
            Loaded and validated configuration object
        """
        config_path = Path(config_path)

        # Check cache first
        cache_key = str(config_path.resolve())
        if cache_key in self._loaded_configs:
            return self._loaded_configs[cache_key]

        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        # Determine config type based on path
        config_type = self._determine_config_type(config_path)

        try:
            # Load file content
            content = self._load_config_content(config_path)

            # Parse configuration
            config = self._parse_config(content, config_type)

            # Validate if requested
            if validate:
                validation_result = self.validate_config(config)
                if not validation_result.is_valid:
                    error_msg = f"Configuration validation failed: {validation_result.message}"
                    logger.error(error_msg)
                    raise ValueError(error_msg)

            # Cache loaded configuration
            self._loaded_configs[cache_key] = config

            logger.info(f"Loaded configuration: {config_path}")
            return config

        except Exception as e:
            logger.error(f"Failed to load configuration {config_path}: {e}")
            raise

    def _determine_config_type(self, config_path: Path) -> str:
        """Determine configuration type from path."""
        path_str = str(config_path)
        filename = config_path.name.lower()

        # Check filename patterns
        if filename.startswith("experiment") or filename.endswith("experiment.yaml") or "experiment" in path_str:
            return "simulation"
        elif filename.startswith("simulation") or filename.endswith("simulation.yaml") or "simulation" in path_str:
            return "simulation"
        elif filename.startswith("environment") or filename.endswith("environment.yaml") or "environment" in path_str:
            return "environment"
        elif filename.startswith("profile") or filename.endswith("profile.yaml") or "profile" in path_str:
            return "profile"
        elif filename.startswith("global") or filename.endswith("global.yaml") or "global" in path_str:
            return "global"
        else:
            # Try to infer from content structure
            return "generic"

    def _load_config_content(self, config_path: Path) -> Dict[str, Any]:
        """Load configuration content from file."""
        import yaml

        with open(config_path, "r", encoding="utf-8") as f:
            if config_path.suffix in [".yaml", ".yml"]:
                return yaml.safe_load(f)
            elif config_path.suffix == ".json":
                return json.load(f)
            else:
                raise ValueError(f"Unsupported configuration format: {config_path.suffix}")

    def _parse_config(self, content: Dict[str, Any], config_type: str) -> Any:
        """Parse configuration content into appropriate model."""
        try:
            if config_type == "simulation":
                config = SimulationConfig(**content)
                logger.debug(f"Parsed simulation config: {config.name}")
                return config
            elif config_type == "global":
                return GlobalConfig(**content)
            elif config_type == "profile":
                return ProfileConfig(**content)
            else:
                # For generic configs, return as dict
                logger.debug(f"Returning generic config as dict: {type(content)}")
                return content

        except ValidationError as e:
            logger.error(f"Configuration validation failed: {e}")
            raise ValueError(f"Invalid configuration format: {e}")
        except Exception as e:
            logger.error(f"Configuration parsing failed: {e}")
            raise ValueError(f"Configuration parsing failed: {e}")

    def load_profile_config(self, profile_name: str) -> ProfileConfig:
        """
        Load profile configuration.

        Args:
            profile_name: Name of the profile to load

        Returns:
            Profile configuration object
        """
        # Check cache first
        if profile_name in self._profiles:
            return self._profiles[profile_name]

        # Try to load from file
        profile_paths = [
            self.config_dir / "profiles" / f"{profile_name}.yaml",
            self.config_dir / "profiles" / f"{profile_name}.json",
            self.config_dir / f"{profile_name}.yaml",
            self.config_dir / f"{profile_name}.json",
        ]

        for profile_path in profile_paths:
            if profile_path.exists():
                profile = self.load_config_file(profile_path)
                self._profiles[profile_name] = profile
                return profile

        # Try built-in profiles
        if profile_name in self._profiles:
            return self._profiles[profile_name]

        raise FileNotFoundError(f"Profile not found: {profile_name}")

    def _load_builtin_profiles(self) -> None:
        """Load built-in configuration profiles."""
        builtin_profiles = {
            "research": ProfileConfig(
                name="research",
                description="Research and development profile",
                base_config="base/global.yaml",
                use_case="research",
                performance_target="balanced",
                resource_level="medium",
                overrides={
                    "system.log_level": "DEBUG",
                    "system.validation_strict": True,
                    "metta.default_timesteps": 1000000,
                },
            ),
            "production": ProfileConfig(
                name="production",
                description="Production deployment profile",
                base_config="base/global.yaml",
                use_case="production",
                performance_target="optimized",
                resource_level="high",
                overrides={
                    "system.log_level": "INFO",
                    "system.validation_strict": True,
                    "metta.checkpoint_frequency": 10000,
                },
            ),
            "minimal": ProfileConfig(
                name="minimal",
                description="Minimal resource profile",
                base_config="base/global.yaml",
                use_case="testing",
                performance_target="minimal",
                resource_level="low",
                overrides={
                    "system.parallel_workers": 1,
                    "metta.num_agents": 8,
                    "metta.default_timesteps": 10000,
                },
            ),
            "development": ProfileConfig(
                name="development",
                description="Development and debugging profile",
                base_config="base/global.yaml",
                use_case="development",
                performance_target="debug",
                resource_level="medium",
                overrides={
                    "system.log_level": "DEBUG",
                    "system.enable_profiling": True,
                    "metta.evaluation_frequency": 1000,
                },
            ),
        }

        self._profiles.update(builtin_profiles)

    def merge_configs(self, base_config: Any, override_config: Any) -> Any:
        """
        Merge two configurations with override taking precedence.

        Args:
            base_config: Base configuration
            override_config: Override configuration

        Returns:
            Merged configuration
        """
        # Convert both to dicts for merging
        base_dict = self._config_to_dict(base_config)
        override_dict = self._config_to_dict(override_config)

        # Perform merge
        merged = base_dict.copy()
        for key, value in override_dict.items():
            if isinstance(value, dict) and key in merged and isinstance(merged[key], dict):
                merged[key] = self.merge_configs(merged[key], value)
            else:
                merged[key] = value

        # Try to convert back to original type
        return self._dict_to_config(merged, base_config)

    def _config_to_dict(self, config: Any) -> Dict[str, Any]:
        """Convert configuration object to dictionary."""
        if hasattr(config, "dict"):
            return config.dict()
        elif hasattr(config, "__dict__"):
            return config.__dict__
        elif isinstance(config, dict):
            return config
        else:
            return dict(config) if config else {}

    def _dict_to_config(self, config_dict: Dict[str, Any], original_config: Any) -> Any:
        """Convert dictionary back to configuration object."""
        if hasattr(original_config, "__class__"):
            try:
                return original_config.__class__(**config_dict)
            except Exception:
                pass
        return config_dict

    def apply_overrides(self, config: Any, overrides: Dict[str, Any]) -> Any:
        """
        Apply runtime overrides to configuration.

        Args:
            config: Base configuration
            overrides: Dictionary of overrides (dot notation keys)

        Returns:
            Configuration with overrides applied
        """
        if not overrides:
            return config

        # Convert to dict for manipulation
        if hasattr(config, "dict"):
            config_dict = config.dict()
        elif hasattr(config, "__dict__"):
            config_dict = config.__dict__
        else:
            config_dict = dict(config)

        # Apply overrides
        for override_key, override_value in overrides.items():
            self._set_nested_value(config_dict, override_key.split("."), override_value)

        # Convert back to original type if possible
        if hasattr(config, "__class__"):
            return config.__class__(**config_dict)
        else:
            return config_dict

    def _set_nested_value(self, config: Any, key_parts: List[str], value: Any) -> None:
        """Set nested configuration value using dot notation."""
        if len(key_parts) == 1:
            config[key_parts[0]] = value
        else:
            if key_parts[0] not in config:
                config[key_parts[0]] = {}
            self._set_nested_value(config[key_parts[0]], key_parts[1:], value)

    def validate_config(self, config: Any) -> ValidationResult:
        """
        Validate configuration against schema.

        Args:
            config: Configuration to validate

        Returns:
            ValidationResult object
        """
        return self.validator.validate_config(config)

    def save_config(self, config: Any, output_path: Union[str, Path]) -> None:
        """
        Save configuration to file.

        Args:
            config: Configuration to save
            output_path: Output file path
        """
        output_path = Path(output_path)

        # Create parent directory if needed
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Convert to dict if it's a Pydantic model
        if hasattr(config, "dict"):
            config_dict = config.dict()
        elif hasattr(config, "__dict__"):
            config_dict = config.__dict__
        else:
            config_dict = dict(config)

        # Save as YAML
        import yaml

        with open(output_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(config_dict, f, default_flow_style=False, sort_keys=False)

        logger.info(f"Saved configuration to: {output_path}")

    def list_available_configs(self, config_type: Optional[str] = None) -> List[str]:
        """
        List available configuration files.

        Args:
            config_type: Type of configurations to list

        Returns:
            List of configuration names
        """
        configs = []

        # Search in common config directories
        search_dirs = []
        if config_type:
            type_mapping = {
                "simulation": ["experiments", "simulation"],
                "environment": ["environments", "env"],
                "profile": ["profiles"],
                "global": ["base", "global"],
            }
            search_dirs = type_mapping.get(config_type, [config_type])
        else:
            search_dirs = ["experiments", "environments", "profiles", "base"]

        for search_dir in search_dirs:
            search_path = self.config_dir / search_dir
            if search_path.exists():
                for config_file in search_path.rglob("*.yaml"):
                    if config_file.is_file():
                        configs.append(str(config_file.relative_to(self.config_dir)))

                for config_file in search_path.rglob("*.json"):
                    if config_file.is_file():
                        configs.append(str(config_file.relative_to(self.config_dir)))

        return sorted(list(set(configs)))  # Remove duplicates and sort

    def get_config_info(self, config_name: str) -> Dict[str, Any]:
        """
        Get information about a configuration.

        Args:
            config_name: Name or path of configuration

        Returns:
            Dictionary with configuration information
        """
        try:
            config = self.load_config_file(config_name)

            info = {
                "name": getattr(config, "name", config_name),
                "type": type(config).__name__,
                "description": getattr(config, "description", None),
                "version": getattr(config, "version", None),
                "created_at": getattr(config, "created_at", None),
            }

            if hasattr(config, "environment"):
                info["environment"] = config.environment.name
                info["num_agents"] = config.environment.num_agents

            if hasattr(config, "training"):
                info["timesteps"] = config.training.total_timesteps

            return info

        except Exception as e:
            return {"name": config_name, "error": str(e), "type": "unknown"}
