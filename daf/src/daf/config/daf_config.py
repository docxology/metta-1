"""
DAF Configuration System

This module provides comprehensive configuration management for the DAF system,
integrating with Metta's configuration components while providing DAF-specific enhancements.
"""

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

# Import Metta configuration components (optional)
try:
    from metta.setup.metta_cli import MettaCLI
    from metta.setup.registry import get_all_modules, register_module
    from metta.setup.saved_settings import SavedSettings

    METTA_AVAILABLE = True
except ImportError:
    SavedSettings = None
    MettaCLI = None
    get_all_modules = None
    register_module = None
    METTA_AVAILABLE = False

try:
    from mettagrid.config import Config as MettaGridConfig

    METTAGRID_AVAILABLE = True
except ImportError:
    MettaGridConfig = None
    METTAGRID_AVAILABLE = False


@dataclass
class DAFConfig:
    """Main DAF configuration"""

    experiment_name: str = "daf_experiment"
    version: str = "1.0.0"
    description: str = "DAF Adaptive Learning Experiment"

    # Core settings
    enable_adaptive_learning: bool = True
    enable_curriculum_learning: bool = True
    enable_rl_training: bool = True
    enable_evaluation: bool = True

    # Integration settings
    integrate_with_wandb: bool = True
    integrate_with_skypilot: bool = False
    integrate_with_aws: bool = False

    # System settings
    data_dir: Optional[str] = None
    output_dir: Optional[str] = None
    log_level: str = "INFO"
    enable_profiling: bool = False

    # Component configurations
    adaptive_config: Dict[str, Any] = field(default_factory=dict)
    curriculum_config: Dict[str, Any] = field(default_factory=dict)
    rl_config: Dict[str, Any] = field(default_factory=dict)
    evaluation_config: Dict[str, Any] = field(default_factory=dict)

    # Advanced settings
    enable_distributed_training: bool = False
    max_workers: int = 4
    timeout_seconds: int = 3600
    retry_attempts: int = 3

    # DAF-specific features
    enable_auto_tuning: bool = False
    enable_model_selection: bool = False
    enable_ensemble_learning: bool = False

    # Documentation settings
    generate_docs_on_startup: bool = True


class DAFConfigManager:
    """
    Enhanced configuration manager for DAF system

    Provides centralized configuration management with:
    - Integration with Metta's configuration system
    - Environment-specific configurations
    - Component registration and management
    - Configuration validation and defaults
    """

    def __init__(self, config: Optional[DAFConfig] = None):
        """
        Initialize DAF Configuration Manager

        Args:
            config: Optional DAF configuration
        """
        self.config = config or DAFConfig()
        self.logger = logging.getLogger("DAFConfigManager")

        # Initialize Metta CLI for component management (with error handling)
        try:
            self._metta_cli = MettaCLI()
            from metta.setup.saved_settings import get_saved_settings

            self._saved_settings = get_saved_settings()
        except (AttributeError, ImportError):
            # Handle API differences in Metta versions
            self._metta_cli = None
            self._saved_settings = None

        # Track registered components
        self._registered_components: Dict[str, Any] = {}

        self.logger.info(f"DAF Config Manager initialized for: {self.config.experiment_name}")

    def load_from_file(self, config_path: str) -> bool:
        """
        Load configuration from file

        Args:
            config_path: Path to configuration file

        Returns:
            True if loaded successfully, False otherwise
        """
        try:
            import json

            with open(config_path, "r") as f:
                config_data = json.load(f)

            # Update configuration
            for key, value in config_data.items():
                if hasattr(self.config, key):
                    setattr(self.config, key, value)

            self.logger.info(f"Configuration loaded from {config_path}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to load configuration: {e}")
            return False

    def save_to_file(self, config_path: str):
        """
        Save configuration to file

        Args:
            config_path: Path to save configuration file
        """
        try:
            import json

            config_data = {}

            # Extract serializable attributes
            for key, value in self.config.__dict__.items():
                if isinstance(value, (str, int, float, bool, list, dict, type(None))):
                    config_data[key] = value

            with open(config_path, "w") as f:
                json.dump(config_data, f, indent=2)

            self.logger.info(f"Configuration saved to {config_path}")

        except Exception as e:
            self.logger.error(f"Failed to save configuration: {e}")

    def configure_component(self, component_name: str, config: Dict[str, Any]):
        """
        Configure a specific component

        Args:
            component_name: Name of the component to configure
            config: Configuration dictionary
        """
        try:
            self._metta_cli.configure_component(component_name, config)

            # Store in our configuration
            if component_name == "wandb":
                self.config.integrate_with_wandb = True
            elif component_name == "aws":
                self.config.integrate_with_aws = True
                self.config.adaptive_config.update(config)
            elif component_name == "adaptive":
                self.config.adaptive_config.update(config)
            elif component_name == "curriculum":
                self.config.curriculum_config.update(config)
            elif component_name == "rl":
                self.config.rl_config.update(config)

            self.logger.info(f"Component {component_name} configured")

        except Exception as e:
            self.logger.error(f"Failed to configure component {component_name}: {e}")
            raise

    def register_component(self, component_name: str, component_class: Any):
        """
        Register a custom component

        Args:
            component_name: Name of the component
            component_class: Component class
        """
        try:
            register_module(component_name, component_class)
            self._registered_components[component_name] = component_class
            self.logger.info(f"Component {component_name} registered")

        except Exception as e:
            self.logger.error(f"Failed to register component {component_name}: {e}")
            raise

    def get_component_config(self, component_name: str) -> Dict[str, Any]:
        """
        Get configuration for a specific component

        Args:
            component_name: Name of the component

        Returns:
            Component configuration dictionary
        """
        try:
            return self._saved_settings.get_component_config(component_name)
        except Exception:
            # Return default configuration
            return {}

    def setup_environment(self, environment_name: str):
        """
        Set up environment-specific configuration

        Args:
            environment_name: Name of the environment (dev, staging, prod)
        """
        self.logger.info(f"Setting up environment: {environment_name}")

        # Environment-specific configurations
        env_configs = {
            "development": {"log_level": "DEBUG", "enable_profiling": True, "integrate_with_wandb": False},
            "staging": {
                "log_level": "INFO",
                "enable_profiling": False,
                "integrate_with_wandb": True,
                "integrate_with_skypilot": False,
            },
            "production": {
                "log_level": "WARNING",
                "enable_profiling": False,
                "integrate_with_wandb": True,
                "integrate_with_skypilot": True,
                "integrate_with_aws": True,
            },
        }

        if environment_name in env_configs:
            env_config = env_configs[environment_name]
            for key, value in env_config.items():
                if hasattr(self.config, key):
                    setattr(self.config, key, value)

            self.logger.info(f"Environment {environment_name} configured")

        # Configure Metta CLI components
        self._configure_metta_components()

    def _configure_metta_components(self):
        """Configure Metta CLI components based on DAF configuration"""
        try:
            # Configure WandB if enabled
            if self.config.integrate_with_wandb:
                wandb_config = self.config.adaptive_config.get("wandb", {})
                if not wandb_config:
                    wandb_config = {"project": self.config.experiment_name, "entity": "daf-user"}
                self.configure_component("wandb", wandb_config)

            # Configure AWS if enabled
            if self.config.integrate_with_aws:
                aws_config = self.config.adaptive_config.get("aws", {})
                if not aws_config:
                    aws_config = {"region": "us-west-2"}
                self.configure_component("aws", aws_config)

        except Exception as e:
            self.logger.warning(f"Failed to configure some Metta components: {e}")

    def validate_configuration(self) -> List[str]:
        """
        Validate the current configuration

        Returns:
            List of validation errors (empty if valid)
        """
        errors = []

        # Check required fields
        if not self.config.experiment_name:
            errors.append("experiment_name is required")

        # Check component compatibility
        if self.config.enable_curriculum_learning and not self.config.enable_adaptive_learning:
            errors.append("curriculum_learning requires adaptive_learning to be enabled")

        if self.config.enable_distributed_training and self.config.max_workers < 2:
            errors.append("distributed_training requires max_workers >= 2")

        # Check integration consistency
        if self.config.integrate_with_skypilot and not self.config.integrate_with_aws:
            errors.append("skypilot integration typically requires AWS integration")

        return errors

    def get_effective_config(self) -> Dict[str, Any]:
        """
        Get the effective configuration with all components resolved

        Returns:
            Complete configuration dictionary
        """
        config_dict = {}

        # Base configuration
        for key, value in self.config.__dict__.items():
            if isinstance(value, (str, int, float, bool, type(None))):
                config_dict[key] = value
            elif isinstance(value, (list, dict)):
                config_dict[key] = value

        # Component configurations
        config_dict["components"] = {}
        available_components = get_all_modules()
        for component_name in available_components:
            config_dict["components"][component_name] = self.get_component_config(component_name)

        return config_dict

    def create_experiment_config(self) -> Dict[str, Any]:
        """
        Create a complete experiment configuration

        Returns:
            Experiment configuration dictionary
        """
        experiment_config = {
            "experiment": {
                "name": self.config.experiment_name,
                "version": self.config.version,
                "description": self.config.description,
            },
            "system": {
                "enable_adaptive_learning": self.config.enable_adaptive_learning,
                "enable_curriculum_learning": self.config.enable_curriculum_learning,
                "enable_rl_training": self.config.enable_rl_training,
                "enable_evaluation": self.config.enable_evaluation,
            },
            "integrations": {
                "wandb": self.config.integrate_with_wandb,
                "skypilot": self.config.integrate_with_skypilot,
                "aws": self.config.integrate_with_aws,
            },
            "advanced": {
                "distributed_training": self.config.enable_distributed_training,
                "max_workers": self.config.max_workers,
                "timeout": self.config.timeout_seconds,
                "auto_tuning": self.config.enable_auto_tuning,
                "model_selection": self.config.enable_model_selection,
                "ensemble_learning": self.config.enable_ensemble_learning,
            },
        }

        return experiment_config

    def print_configuration_summary(self):
        """Print a summary of the current configuration"""
        self.logger.info("=== DAF Configuration Summary ===")
        self.logger.info(f"Experiment: {self.config.experiment_name} v{self.config.version}")
        self.logger.info(f"Description: {self.config.description}")
        self.logger.info(f"Log Level: {self.config.log_level}")

        self.logger.info("\nComponents:")
        self.logger.info(f"  Adaptive Learning: {'Enabled' if self.config.enable_adaptive_learning else 'Disabled'}")
        self.logger.info(
            f"  Curriculum Learning: {'Enabled' if self.config.enable_curriculum_learning else 'Disabled'}"
        )
        self.logger.info(f"  RL Training: {'Enabled' if self.config.enable_rl_training else 'Disabled'}")
        self.logger.info(f"  Evaluation: {'Enabled' if self.config.enable_evaluation else 'Disabled'}")

        self.logger.info("\nIntegrations:")
        self.logger.info(f"  WandB: {'Enabled' if self.config.integrate_with_wandb else 'Disabled'}")
        self.logger.info(f"  SkyPilot: {'Enabled' if self.config.integrate_with_skypilot else 'Disabled'}")
        self.logger.info(f"  AWS: {'Enabled' if self.config.integrate_with_aws else 'Disabled'}")

        self.logger.info("\nAdvanced:")
        self.logger.info(
            f"  Distributed Training: {'Enabled' if self.config.enable_distributed_training else 'Disabled'}"
        )
        self.logger.info(f"  Max Workers: {self.config.max_workers}")
        self.logger.info(f"  Auto Tuning: {'Enabled' if self.config.enable_auto_tuning else 'Disabled'}")
        self.logger.info(f"  Model Selection: {'Enabled' if self.config.enable_model_selection else 'Disabled'}")
        self.logger.info(f"  Ensemble Learning: {'Enabled' if self.config.enable_ensemble_learning else 'Disabled'}")

        # Validation errors
        validation_errors = self.validate_configuration()
        if validation_errors:
            self.logger.warning(f"\nValidation Errors: {len(validation_errors)}")
            for error in validation_errors:
                self.logger.warning(f"  - {error}")
        else:
            self.logger.info("\nValidation: PASSED")


# Convenience functions for common configuration scenarios
def create_development_config(experiment_name: str) -> DAFConfigManager:
    """
    Create a configuration optimized for development

    Args:
        experiment_name: Name of the experiment

    Returns:
        Configured DAFConfigManager
    """
    config = DAFConfig(
        experiment_name=experiment_name,
        log_level="DEBUG",
        enable_profiling=True,
        integrate_with_wandb=False,
        enable_distributed_training=False,
    )

    manager = DAFConfigManager(config)
    manager.setup_environment("development")

    return manager


def create_production_config(experiment_name: str) -> DAFConfigManager:
    """
    Create a configuration optimized for production

    Args:
        experiment_name: Name of the experiment

    Returns:
        Configured DAFConfigManager
    """
    config = DAFConfig(
        experiment_name=experiment_name,
        log_level="INFO",
        integrate_with_wandb=True,
        integrate_with_skypilot=True,
        integrate_with_aws=True,
        enable_distributed_training=True,
        max_workers=8,
    )

    manager = DAFConfigManager(config)
    manager.setup_environment("production")

    return manager


def load_config_from_environment() -> DAFConfigManager:
    """
    Load configuration from environment variables

    Returns:
        DAFConfigManager configured from environment
    """
    import os

    config = DAFConfig(
        experiment_name=os.getenv("DAF_EXPERIMENT_NAME", "daf_experiment"),
        log_level=os.getenv("DAF_LOG_LEVEL", "INFO"),
        data_dir=os.getenv("DAF_DATA_DIR"),
        output_dir=os.getenv("DAF_OUTPUT_DIR"),
    )

    # Enable integrations based on environment
    if os.getenv("WANDB_API_KEY"):
        config.integrate_with_wandb = True

    if os.getenv("AWS_REGION"):
        config.integrate_with_aws = True

    if os.getenv("SKYPILOT_CONFIG"):
        config.integrate_with_skypilot = True

    manager = DAFConfigManager(config)

    return manager
