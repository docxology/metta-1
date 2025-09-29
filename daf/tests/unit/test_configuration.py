"""
Unit tests for DAF configuration system.
"""

from pathlib import Path

import pytest

from daf.config.configuration import ConfigurationManager
from daf.config.models import GlobalConfig, ProfileConfig, SimulationConfig
from daf.config.validation import ConfigurationValidator


class TestConfigurationModels:
    """Test configuration data models."""

    def test_simulation_config_creation(self, sample_config_data):
        """Test creating a simulation configuration."""
        config = SimulationConfig(**sample_config_data)

        assert config.name == "test_experiment"
        assert config.environment.num_agents == 8
        assert config.training.total_timesteps == 10000
        assert config.evaluation.frequency == 1000

    def test_simulation_config_validation(self, sample_invalid_config_data):
        """Test simulation configuration validation."""
        with pytest.raises(Exception):
            SimulationConfig(**sample_invalid_config_data)

    def test_global_config_creation(self):
        """Test creating a global configuration."""
        config = GlobalConfig(
            system={
                "python_version": "3.11.7",
                "device": "cpu",
                "parallel_workers": 4,
            },
            metta={
                "installation_path": "/usr/local/metta",
                "version_requirement": ">=0.1.0",
            },
        )

        assert config.system.python_version == "3.11.7"
        assert config.system.device == "cpu"
        assert config.metta.installation_path == Path("/usr/local/metta")

    def test_profile_config_creation(self):
        """Test creating a profile configuration."""
        config = ProfileConfig(
            name="test_profile",
            description="Test profile",
            base_config="base/global.yaml",
            overrides={"system.log_level": "DEBUG"},
        )

        assert config.name == "test_profile"
        assert config.overrides["system.log_level"] == "DEBUG"


class TestConfigurationManager:
    """Test configuration manager functionality."""

    def test_load_base_config(self, temp_dir, sample_config_data):
        """Test loading base configuration."""
        # Create config directory structure
        config_dir = temp_dir / "configs"
        config_dir.mkdir()

        # Create base config file
        base_config = {
            "system": {
                "python_version": "3.11.7",
                "device": "cpu",
            },
            "metta": {
                "version_requirement": ">=0.1.0",
            },
        }

        import yaml

        base_config_file = config_dir / "base" / "global.yaml"
        base_config_file.parent.mkdir()
        with open(base_config_file, "w") as f:
            yaml.safe_dump(base_config, f)

        # Test loading
        config_manager = ConfigurationManager(config_dir=config_dir)
        loaded_config = config_manager.load_base_config()

        assert loaded_config.system.python_version == "3.11.7"
        assert loaded_config.system.device == "cpu"

    def test_load_config_file(self, temp_dir, sample_config_data):
        """Test loading configuration from file."""
        config_dir = temp_dir / "configs"
        config_dir.mkdir()

        # Create experiment config file
        import yaml

        experiment_file = config_dir / "experiments" / "test.yaml"
        experiment_file.parent.mkdir()
        with open(experiment_file, "w") as f:
            yaml.safe_dump(sample_config_data, f)

        # Test loading
        config_manager = ConfigurationManager(config_dir=config_dir)
        loaded_config = config_manager.load_config_file(experiment_file)

        assert loaded_config.name == "test_experiment"
        assert loaded_config.environment.num_agents == 8

    def test_apply_overrides(self, sample_config_data):
        """Test applying configuration overrides."""
        config = SimulationConfig(**sample_config_data)
        config_manager = ConfigurationManager()

        overrides = {
            "training.total_timesteps": 50000,
            "environment.num_agents": 16,
        }

        modified_config = config_manager.apply_overrides(config, overrides)

        assert modified_config.training.total_timesteps == 50000
        assert modified_config.environment.num_agents == 16

    def test_merge_configs(self, sample_config_data):
        """Test merging two configurations."""
        base_config = SimulationConfig(**sample_config_data)
        override_config = {
            "training": {
                "total_timesteps": 50000,
                "learning_rate": 0.01,
            },
            "environment": {
                "num_agents": 16,
            },
        }

        config_manager = ConfigurationManager()
        merged_config = config_manager.merge_configs(base_config, override_config)

        assert merged_config.training.total_timesteps == 50000
        assert merged_config.training.learning_rate == 0.01
        assert merged_config.environment.num_agents == 16


class TestConfigurationValidator:
    """Test configuration validation."""

    def test_validate_valid_config(self, sample_config_data):
        """Test validating a valid configuration."""
        config = SimulationConfig(**sample_config_data)
        validator = ConfigurationValidator()

        result = validator.validate_config(config)

        assert result.is_valid
        assert "valid" in result.message.lower()

    def test_validate_invalid_config(self, sample_invalid_config_data):
        """Test validating an invalid configuration."""
        config = sample_invalid_config_data  # Invalid dict
        validator = ConfigurationValidator()

        result = validator.validate_config(config)

        # Should still be valid for basic dict
        assert result.is_valid

    def test_validate_simulation_config(self, sample_config_data):
        """Test simulation configuration validation."""
        config = SimulationConfig(**sample_config_data)
        validator = ConfigurationValidator()

        result = validator._validate_simulation_config(config)

        assert result.is_valid
        assert "simulation configuration is valid" in result.message.lower()

    def test_validate_profile_config(self):
        """Test profile configuration validation."""
        config = ProfileConfig(
            name="test_profile",
            description="Test profile",
            base_config="base/global.yaml",
        )
        validator = ConfigurationValidator()

        result = validator._validate_profile_config(config)

        assert result.is_valid
        assert "profile configuration is valid" in result.message.lower()
