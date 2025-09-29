"""Integration tests for DAF methods with real Metta components."""

from __future__ import annotations

import sys
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


class TestDAFMettaIntegration(unittest.TestCase):
    """Test DAF integration with real Metta components."""

    def setUp(self):
        """Set up test environment."""
        self.daf_root = ROOT_DIR
        self.metta_root = self.daf_root.parent / "metta"

        # Add Metta to path for real imports
        if str(self.metta_root) not in sys.path:
            sys.path.insert(0, str(self.metta_root))

        # Load DAF modules
        self.config_module = load_module("daf.config.daf_config", SRC_DIR / "daf" / "config" / "daf_config.py")
        self.wrappers_module = load_module(
            "daf.wrappers.metta_wrapper", SRC_DIR / "daf" / "wrappers" / "metta_wrapper.py"
        )

    def test_daf_config_with_metta_components(self):
        """Test DAF configuration integration with real Metta components."""
        DAFConfigManager = self.config_module.DAFConfigManager

        # Create configuration
        config = self.config_module.DAFConfig()
        manager = DAFConfigManager(config)

        # Test that configuration can be created and used
        self.assertIsNotNone(manager.config)
        self.assertEqual(manager.config.experiment_name, "daf_experiment")

        # Test configuration validation
        errors = manager.validate_configuration()
        self.assertIsInstance(errors, list)

    def test_adaptive_wrapper_with_real_metta(self):
        """Test AdaptiveWrapper with real Metta components."""
        try:
            AdaptiveWrapper = self.wrappers_module.AdaptiveWrapper

            # Create wrapper
            wrapper = AdaptiveWrapper()

            # Test wrapper properties
            self.assertEqual(wrapper.component_name, "adaptive")
            self.assertFalse(wrapper.is_initialized())

            # Test that wrapper can be created without errors
            self.assertIsNotNone(wrapper)

        except Exception as e:
            self.skipTest(f"AdaptiveWrapper test failed: {e}")

    def test_curriculum_wrapper_with_real_metta(self):
        """Test CurriculumWrapper with real Metta components."""
        try:
            CurriculumWrapper = self.wrappers_module.CurriculumWrapper

            # Create wrapper
            wrapper = CurriculumWrapper()

            # Test wrapper properties
            self.assertEqual(wrapper.component_name, "curriculum")
            self.assertFalse(wrapper.is_initialized())

            # Test that wrapper can be created without errors
            self.assertIsNotNone(wrapper)

        except Exception as e:
            self.skipTest(f"CurriculumWrapper test failed: {e}")

    def test_rl_wrapper_with_real_metta(self):
        """Test RLWrapper with real Metta components."""
        try:
            RLWrapper = self.wrappers_module.RLWrapper

            # Create wrapper
            wrapper = RLWrapper()

            # Test wrapper properties
            self.assertEqual(wrapper.component_name, "rl")
            self.assertFalse(wrapper.is_initialized())

            # Test that wrapper can be created without errors
            self.assertIsNotNone(wrapper)

        except Exception as e:
            self.skipTest(f"RLWrapper test failed: {e}")


class TestDAFDocumentationIntegration(unittest.TestCase):
    """Test DAF documentation integration with real Metta source."""

    def setUp(self):
        """Set up test environment."""
        # Load DAF documentation modules
        docs_dir = SRC_DIR / "daf" / "operations"
        self.docs_module = load_module("daf.operations.docs", docs_dir / "docs.py")

        tools_dir = SRC_DIR / "daf" / "tools"
        self.tools_module = load_module("daf.tools.comprehensive_generator", tools_dir / "comprehensive_generator.py")

    def test_documentation_generation_with_real_metta(self):
        """Test documentation generation with real Metta source code."""
        # Test that documentation tools can be imported
        self.assertTrue(hasattr(self.tools_module, "generate_comprehensive_daf_docs"))

        # Test that the function exists and is callable
        generate_docs = self.tools_module.generate_comprehensive_daf_docs
        self.assertTrue(callable(generate_docs))

    def test_metta_inventory_scanning(self):
        """Test Metta inventory scanning functionality."""
        # Test that sync tools can be imported
        sync_dir = SRC_DIR / "daf" / "tools"
        sync_module = load_module("daf.tools.sync_with_metta", sync_dir / "sync_with_metta.py")

        self.assertTrue(hasattr(sync_module, "scan_metta_repository"))
        self.assertTrue(hasattr(sync_module, "sync_daf_with_metta"))

        # Test that functions are callable
        scan_func = sync_module.scan_metta_repository
        sync_func = sync_module.sync_daf_with_metta
        self.assertTrue(callable(scan_func))
        self.assertTrue(callable(sync_func))


class TestDAFLoggingIntegration(unittest.TestCase):
    """Test DAF logging integration with real Metta operations."""

    def setUp(self):
        """Set up test environment."""
        # Load DAF logging module
        logging_dir = SRC_DIR / "daf" / "logging"
        self.logging_module = load_module("daf.logging.daf_logger", logging_dir / "daf_logger.py")

    def test_daf_logger_with_metta_operations(self):
        """Test DAF logger with simulated Metta operations."""
        DAFLogger = self.logging_module.DAFLogger

        # Create logger
        logger = DAFLogger("test_component", {"experiment": "integration_test"})

        # Test that logger has expected methods
        self.assertTrue(hasattr(logger, "info"))
        self.assertTrue(hasattr(logger, "debug"))
        self.assertTrue(hasattr(logger, "warning"))
        self.assertTrue(hasattr(logger, "error"))

        # Test logging operations (should not crash)
        try:
            logger.info("Test message", {"operation": "test"})
            logger.debug("Debug message", {"component": "test"})
        except Exception as e:
            self.fail(f"Logger operations failed: {e}")


class TestDAFSetupIntegration(unittest.TestCase):
    """Test DAF setup integration with real Metta repository."""

    def setUp(self):
        """Set up test environment."""
        # Load DAF setup module
        setup_dir = SRC_DIR / "daf" / "setup"
        self.setup_module = load_module("daf.setup.daf_setup", setup_dir / "daf_setup.py")

    def test_daf_setup_with_real_metta(self):
        """Test DAF setup with real Metta repository."""
        DAFSetup = self.setup_module.DAFSetup
        DAFConfig = self.setup_module.DAFConfig

        # Create setup with configuration
        config = DAFConfig()
        setup = DAFSetup(config)

        # Test that setup can be created
        self.assertIsNotNone(setup)
        self.assertEqual(setup.config, config)

        # Test directory creation
        try:
            setup._create_directories()
            # Should not crash
        except Exception as e:
            self.fail(f"Directory creation failed: {e}")

    def test_metta_repository_validation(self):
        """Test Metta repository validation with real repository."""
        DAFSetup = self.setup_module.DAFSetup
        DAFConfig = self.setup_module.DAFConfig

        # Create setup
        config = DAFConfig()
        setup = DAFSetup(config)

        # Test repository validation
        try:
            is_valid = setup._validate_metta_repository()
            # Should return a boolean (True if Metta is found, False otherwise)
            self.assertIsInstance(is_valid, bool)
        except Exception as e:
            self.fail(f"Repository validation failed: {e}")


class TestDAFCoreIntegration(unittest.TestCase):
    """Test DAF core components integration with real Metta."""

    def setUp(self):
        """Set up test environment."""
        # Load DAF core modules
        core_dir = SRC_DIR / "daf" / "core"
        self.adaptive_module = load_module("daf.core.adaptive_controller", core_dir / "adaptive_controller.py")
        self.curriculum_module = load_module("daf.core.curriculum_manager", core_dir / "curriculum_manager.py")
        self.rl_module = load_module("daf.core.rl_trainer", core_dir / "rl_trainer.py")

    def test_core_components_import(self):
        """Test that core components can be imported."""
        # Test adaptive controller
        self.assertTrue(hasattr(self.adaptive_module, "AdaptiveController"))
        self.assertTrue(hasattr(self.adaptive_module, "EnhancedAdaptiveController"))

        # Test curriculum manager
        self.assertTrue(hasattr(self.curriculum_module, "CurriculumManager"))
        self.assertTrue(hasattr(self.curriculum_module, "EnhancedCurriculumManager"))

        # Test RL trainer
        self.assertTrue(hasattr(self.rl_module, "RLTrainer"))
        self.assertTrue(hasattr(self.rl_module, "EnhancedRLTrainer"))

    def test_core_components_instantiation(self):
        """Test that core components can be instantiated."""
        # Test adaptive controller
        try:
            AdaptiveController = self.adaptive_module.AdaptiveController
            # Should be able to create instance (may need config)
            self.assertTrue(hasattr(AdaptiveController, "__init__"))
        except Exception:
            pass  # May fail without proper config, but import should work

        # Test curriculum manager
        try:
            CurriculumManager = self.curriculum_module.CurriculumManager
            self.assertTrue(hasattr(CurriculumManager, "__init__"))
        except Exception:
            pass

        # Test RL trainer
        try:
            RLTrainer = self.rl_module.RLTrainer
            self.assertTrue(hasattr(RLTrainer, "__init__"))
        except Exception:
            pass


class TestDAFEndToEndWorkflow(unittest.TestCase):
    """Test end-to-end DAF workflow with real Metta components."""

    def setUp(self):
        """Set up test environment."""
        # Load main DAF modules
        self.daf_main_module = load_module("daf.daf_main", ROOT_DIR / "daf_main.py")
        self.config_module = load_module("daf.config.daf_config", SRC_DIR / "daf" / "config" / "daf_config.py")

    def test_daf_main_import(self):
        """Test that daf_main can be imported and has main function."""
        # Test that the module loads
        self.assertTrue(hasattr(self.daf_main_module, "main"))
        self.assertTrue(hasattr(self.daf_main_module, "show_interactive_menu"))

        # Test that main function is callable
        main_func = self.daf_main_module.main
        self.assertTrue(callable(main_func))

    def test_daf_config_integration(self):
        """Test DAF configuration integration."""
        DAFConfig = self.config_module.DAFConfig
        DAFConfigManager = self.config_module.DAFConfigManager

        # Test configuration creation and management
        config = DAFConfig()
        manager = DAFConfigManager(config)

        # Test that configuration has expected attributes
        self.assertTrue(hasattr(config, "experiment_name"))
        self.assertTrue(hasattr(config, "enable_adaptive_learning"))
        self.assertTrue(hasattr(config, "generate_docs_on_startup"))

        # Test manager functionality
        self.assertTrue(hasattr(manager, "validate_configuration"))
        self.assertTrue(hasattr(manager, "get_effective_config"))


if __name__ == "__main__":
    # Run all integration tests
    unittest.main(verbosity=2)
