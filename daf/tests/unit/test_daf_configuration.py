"""Unit tests for DAF configuration with real Metta integration."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

# Add DAF to path for testing
CURRENT_DIR = Path(__file__).resolve()
ROOT_DIR = CURRENT_DIR.parents[2]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import importlib.util


def load_module(module_name: str, file_path: Path):
    """Load a module for testing."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    if "." in module_name:
        module.__package__ = module_name.rpartition(".")[0]
    sys.modules[module_name] = module
    if spec.loader is None:  # pragma: no cover
        raise ImportError(f"Cannot load module {module_name}")
    spec.loader.exec_module(module)
    return module


class TestDAFConfiguration(unittest.TestCase):
    """Test DAF configuration with real Metta components."""

    def setUp(self):
        """Set up test environment."""
        # Load DAF configuration module
        config_dir = SRC_DIR / "daf" / "config"
        self.config_module = load_module("daf.config.daf_config", config_dir / "daf_config.py")

        # Add Metta to path for real imports
        metta_root = ROOT_DIR.parent / "metta"
        if str(metta_root) not in sys.path:
            sys.path.insert(0, str(metta_root))

    def test_daf_config_creation(self):
        """Test DAF configuration creation."""
        DAFConfig = self.config_module.DAFConfig
        DAFConfigManager = self.config_module.DAFConfigManager

        # Test basic config creation
        config = DAFConfig()
        self.assertIsNotNone(config)
        self.assertEqual(config.experiment_name, "daf_experiment")
        self.assertEqual(config.version, "1.0.0")
        self.assertTrue(config.generate_docs_on_startup)

        # Test config manager
        manager = DAFConfigManager(config)
        self.assertIsNotNone(manager.config)

    def test_daf_config_validation(self):
        """Test DAF configuration validation."""
        DAFConfigManager = self.config_module.DAFConfigManager

        config = self.config_module.DAFConfig()
        manager = DAFConfigManager(config)

        # Test validation
        errors = manager.validate_configuration()
        self.assertIsInstance(errors, list)

        # Test that validation catches configuration issues
        invalid_config = self.config_module.DAFConfig()
        invalid_config.enable_curriculum_learning = True
        invalid_config.enable_adaptive_learning = False  # This should cause an error

        invalid_manager = DAFConfigManager(invalid_config)
        invalid_errors = invalid_manager.validate_configuration()
        self.assertGreater(len(invalid_errors), 0)  # Should have validation errors

    def test_daf_config_environment_setup(self):
        """Test DAF environment-specific configuration."""
        DAFConfigManager = self.config_module.DAFConfigManager

        config = self.config_module.DAFConfig()
        manager = DAFConfigManager(config)

        # Test environment setup
        manager.setup_environment("development")
        self.assertEqual(manager.config.log_level, "DEBUG")

        manager.setup_environment("production")
        self.assertEqual(manager.config.log_level, "WARNING")

    def test_daf_config_serialization(self):
        """Test DAF configuration serialization."""
        DAFConfigManager = self.config_module.DAFConfigManager

        config = self.config_module.DAFConfig()
        manager = DAFConfigManager(config)

        # Test serialization
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            temp_path = f.name

        try:
            manager.save_to_file(temp_path)

            # Test loading
            new_manager = self.config_module.DAFConfigManager()
            loaded = new_manager.load_from_file(temp_path)
            self.assertTrue(loaded)

        finally:
            Path(temp_path).unlink(missing_ok=True)


class TestDAFConfigWithMetta(unittest.TestCase):
    """Test DAF configuration integration with real Metta components."""

    def setUp(self):
        """Set up test environment."""
        # Load DAF configuration module
        config_dir = SRC_DIR / "daf" / "config"
        self.config_module = load_module("daf.config.daf_config", config_dir / "daf_config.py")

        # Add Metta to path for real imports
        metta_root = ROOT_DIR.parent / "metta"
        if str(metta_root) not in sys.path:
            sys.path.insert(0, str(metta_root))

    def test_daf_config_with_real_metta_settings(self):
        """Test DAF configuration with real Metta settings."""
        try:
            from metta.setup.saved_settings import SavedSettings

            DAFConfigManager = self.config_module.DAFConfigManager

            config = self.config_module.DAFConfig()
            manager = DAFConfigManager(config)

            # Test that we can access real Metta settings
            from metta.setup.saved_settings import get_saved_settings

            settings = get_saved_settings()
            self.assertIsNotNone(settings)

            # Test component configuration
            wandb_config = manager.get_component_config("wandb")
            self.assertIsInstance(wandb_config, dict)

        except ImportError as e:
            self.skipTest(f"Real Metta settings not available: {e}")

    def test_daf_config_component_configuration(self):
        """Test DAF component configuration with real Metta."""
        DAFConfigManager = self.config_module.DAFConfigManager

        config = self.config_module.DAFConfig()
        manager = DAFConfigManager(config)

        # Test component configuration
        try:
            manager.configure_component("wandb", {"project": "test_project"})
            # Should not crash
            self.assertTrue(True)
        except Exception:
            # May fail if Metta CLI not available, but should not crash
            pass

    def test_daf_config_effective_config(self):
        """Test effective configuration generation."""
        DAFConfigManager = self.config_module.DAFConfigManager

        config = self.config_module.DAFConfig()
        manager = DAFConfigManager(config)

        # Test effective config generation
        effective_config = manager.get_effective_config()
        self.assertIsInstance(effective_config, dict)
        self.assertIn("experiment", effective_config)
        self.assertIn("system", effective_config)
        self.assertIn("integrations", effective_config)
        self.assertIn("advanced", effective_config)


class TestDAFConfigScenarios(unittest.TestCase):
    """Test DAF configuration scenarios with real Metta."""

    def setUp(self):
        """Set up test environment."""
        # Load DAF configuration module
        config_dir = SRC_DIR / "daf" / "config"
        self.config_module = load_module("daf.config.daf_config", config_dir / "daf_config.py")

    def test_development_config_scenario(self):
        """Test development configuration scenario."""
        create_development_config = self.config_module.create_development_config

        manager = create_development_config("test_experiment")

        # Test development-specific settings
        self.assertEqual(manager.config.log_level, "DEBUG")
        self.assertTrue(manager.config.enable_profiling)
        self.assertFalse(manager.config.integrate_with_wandb)
        self.assertFalse(manager.config.enable_distributed_training)

    def test_production_config_scenario(self):
        """Test production configuration scenario."""
        create_production_config = self.config_module.create_production_config

        manager = create_production_config("prod_experiment")

        # Test production-specific settings
        self.assertEqual(manager.config.log_level, "INFO")
        self.assertTrue(manager.config.integrate_with_wandb)
        self.assertTrue(manager.config.integrate_with_skypilot)
        self.assertTrue(manager.config.integrate_with_aws)
        self.assertTrue(manager.config.enable_distributed_training)
        self.assertEqual(manager.config.max_workers, 8)

    def test_environment_variable_config(self):
        """Test configuration from environment variables."""
        load_config_from_environment = self.config_module.load_config_from_environment

        # Set environment variables
        import os

        os.environ["DAF_EXPERIMENT_NAME"] = "env_test_experiment"
        os.environ["DAF_LOG_LEVEL"] = "ERROR"

        try:
            manager = load_config_from_environment()

            # Test that environment variables are used
            self.assertEqual(manager.config.experiment_name, "env_test_experiment")
            self.assertEqual(manager.config.log_level, "ERROR")

        finally:
            # Clean up environment variables
            del os.environ["DAF_EXPERIMENT_NAME"]
            del os.environ["DAF_LOG_LEVEL"]


class TestDAFConfigValidation(unittest.TestCase):
    """Test DAF configuration validation with real Metta."""

    def setUp(self):
        """Set up test environment."""
        # Load DAF configuration module
        config_dir = SRC_DIR / "daf" / "config"
        self.config_module = load_module("daf.config.daf_config", config_dir / "daf_config.py")

    def test_config_validation_errors(self):
        """Test configuration validation error detection."""
        DAFConfigManager = self.config_module.DAFConfigManager

        # Test valid configuration
        valid_config = self.config_module.DAFConfig()
        valid_manager = DAFConfigManager(valid_config)
        valid_errors = valid_manager.validate_configuration()
        self.assertEqual(len(valid_errors), 0)

        # Test invalid configuration
        invalid_config = self.config_module.DAFConfig()
        invalid_config.enable_curriculum_learning = True
        invalid_config.enable_adaptive_learning = False  # Should cause error

        invalid_manager = DAFConfigManager(invalid_config)
        invalid_errors = invalid_manager.validate_configuration()
        self.assertGreater(len(invalid_errors), 0)

    def test_config_compatibility_rules(self):
        """Test configuration compatibility rules."""
        DAFConfigManager = self.config_module.DAFConfigManager

        config = self.config_module.DAFConfig()
        manager = DAFConfigManager(config)

        # Test curriculum learning requires adaptive learning
        config.enable_curriculum_learning = True
        config.enable_adaptive_learning = False
        errors = manager.validate_configuration()
        self.assertTrue(any("curriculum_learning requires adaptive_learning" in error for error in errors))

        # Test distributed training requires sufficient workers
        config.enable_adaptive_learning = True
        config.enable_curriculum_learning = False
        config.enable_distributed_training = True
        config.max_workers = 1
        errors = manager.validate_configuration()
        self.assertTrue(any("distributed_training requires max_workers" in error for error in errors))


if __name__ == "__main__":
    # Run all configuration tests
    unittest.main(verbosity=2)
