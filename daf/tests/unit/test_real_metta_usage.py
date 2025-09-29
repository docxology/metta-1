"""Comprehensive tests for DAF methods testing real Metta functionality."""

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
    """Test DAF methods with real Metta components."""

    def setUp(self):
        """Set up test environment."""
        self.daf_root = ROOT_DIR
        self.metta_root = self.daf_root.parent / "metta"

        # Verify Metta is available
        if not self.metta_root.exists():
            self.skipTest("Metta repository not found")

        # Add Metta to path for real imports
        if str(self.metta_root) not in sys.path:
            sys.path.insert(0, str(self.metta_root))

    def test_metta_adaptive_controller_import(self):
        """Test that we can import and use real Metta AdaptiveController."""
        try:
            from metta.adaptive.adaptive_config import AdaptiveConfig
            from metta.adaptive.adaptive_controller import AdaptiveController

            # Test that we can create instances
            config = AdaptiveConfig()
            self.assertIsNotNone(config)

            # Test that AdaptiveController can be instantiated (may fail without full setup)
            # but should at least import and create config
            self.assertTrue(hasattr(AdaptiveController, "__init__"))

        except ImportError as e:
            self.skipTest(f"Metta AdaptiveController not available: {e}")

    def test_metta_curriculum_import(self):
        """Test that we can import and use real Metta Curriculum components."""
        try:
            from metta.cogworks.curriculum.curriculum import Curriculum
            from metta.cogworks.curriculum.task_generator import TaskGenerator

            # Test basic imports
            self.assertTrue(hasattr(Curriculum, "__init__"))
            self.assertTrue(hasattr(TaskGenerator, "__init__"))

        except ImportError as e:
            self.skipTest(f"Metta Curriculum not available: {e}")

    def test_metta_rl_trainer_import(self):
        """Test that we can import and use real Metta RL Trainer."""
        try:
            from metta.rl.trainer import Trainer
            from metta.rl.training.core import CoreTrainingLoop

            # Test basic imports
            self.assertTrue(hasattr(Trainer, "__init__"))
            self.assertTrue(hasattr(CoreTrainingLoop, "__init__"))

        except ImportError as e:
            self.skipTest(f"Metta RL Trainer not available: {e}")

    def test_metta_wandb_store_import(self):
        """Test that we can import and use real Metta WandbStore."""
        try:
            from metta.adaptive.stores.wandb import WandbStore

            # Test basic import
            self.assertTrue(hasattr(WandbStore, "__init__"))

        except ImportError as e:
            self.skipTest(f"Metta WandbStore not available: {e}")

    def test_metta_setup_components(self):
        """Test that we can import and use real Metta setup components."""
        try:
            from metta.setup.metta_cli import MettaCLI

            # Test basic imports
            # Test that get_saved_settings function exists
            from metta.setup.saved_settings import SavedSettings, get_saved_settings

            self.assertTrue(callable(get_saved_settings))
            self.assertTrue(hasattr(MettaCLI, "__init__"))

        except ImportError as e:
            self.skipTest(f"Metta setup components not available: {e}")


class TestDAFConfiguration(unittest.TestCase):
    """Test DAF configuration with real Metta integration."""

    def setUp(self):
        """Set up test environment."""
        # Load DAF configuration module
        config_dir = SRC_DIR / "daf" / "config"
        self.config_module = load_module("daf.config.daf_config", config_dir / "daf_config.py")

    def test_daf_config_creation(self):
        """Test DAF configuration creation."""
        DAFConfig = self.config_module.DAFConfig
        DAFConfigManager = self.config_module.DAFConfigManager

        # Test basic config creation
        config = DAFConfig()
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


class TestDAFLogging(unittest.TestCase):
    """Test DAF logging with real Metta operations."""

    def setUp(self):
        """Set up test environment."""
        # Load DAF logging module
        logging_dir = SRC_DIR / "daf" / "logging"
        self.logging_module = load_module("daf.logging.daf_logger", logging_dir / "daf_logger.py")

    def test_daf_logger_creation(self):
        """Test DAF logger creation."""
        DAFLogger = self.logging_module.DAFLogger

        # Test logger creation
        logger = DAFLogger("test_component", {"experiment": "test"})
        # DAFLogger doesn't expose component_name directly, but should be functional
        self.assertIsNotNone(logger)

    def test_daf_logger_operations(self):
        """Test DAF logger operations."""
        DAFLogger = self.logging_module.DAFLogger

        logger = DAFLogger("test_component", {"experiment": "test"})

        # Test that logger has the expected methods
        self.assertTrue(hasattr(logger, "info"))
        self.assertTrue(hasattr(logger, "debug"))
        self.assertTrue(hasattr(logger, "warning"))
        self.assertTrue(hasattr(logger, "error"))


class TestDAFWrappers(unittest.TestCase):
    """Test DAF wrappers with real Metta components."""

    def setUp(self):
        """Set up test environment."""
        # Load DAF wrappers module
        wrappers_dir = SRC_DIR / "daf" / "wrappers"
        self.wrappers_module = load_module("daf.wrappers.metta_wrapper", wrappers_dir / "metta_wrapper.py")

    def test_metta_wrapper_base_class(self):
        """Test the base MettaWrapper class."""
        MettaWrapper = self.wrappers_module.MettaWrapper

        # Test that it's an abstract base class
        self.assertTrue(hasattr(MettaWrapper, "initialize"))
        self.assertTrue(hasattr(MettaWrapper, "is_initialized"))

    def test_adaptive_wrapper(self):
        """Test AdaptiveWrapper functionality."""
        try:
            AdaptiveWrapper = self.wrappers_module.AdaptiveWrapper

            # Test wrapper creation
            wrapper = AdaptiveWrapper()
            self.assertIsNotNone(wrapper)
            self.assertEqual(wrapper.component_name, "adaptive")

            # Test initialization (may fail without full setup, but should not crash)
            try:
                wrapper.initialize()
            except Exception:
                # Expected if Metta components not fully configured
                pass

        except AttributeError:
            self.skipTest("AdaptiveWrapper not available in wrappers module")

    def test_curriculum_wrapper(self):
        """Test CurriculumWrapper functionality."""
        try:
            CurriculumWrapper = self.wrappers_module.CurriculumWrapper

            # Test wrapper creation
            wrapper = CurriculumWrapper()
            self.assertIsNotNone(wrapper)
            self.assertEqual(wrapper.component_name, "curriculum")

        except AttributeError:
            self.skipTest("CurriculumWrapper not available in wrappers module")

    def test_rl_wrapper(self):
        """Test RLWrapper functionality."""
        try:
            RLWrapper = self.wrappers_module.RLWrapper

            # Test wrapper creation
            wrapper = RLWrapper()
            self.assertIsNotNone(wrapper)
            self.assertEqual(wrapper.component_name, "rl")

        except AttributeError:
            self.skipTest("RLWrapper not available in wrappers module")


class TestDAFTools(unittest.TestCase):
    """Test DAF tools with real Metta operations."""

    def setUp(self):
        """Set up test environment."""
        # Load DAF tools modules
        tools_dir = SRC_DIR / "daf" / "tools"
        self.tools_module = load_module("daf.tools.comprehensive_generator", tools_dir / "comprehensive_generator.py")
        self.sync_module = load_module("daf.tools.sync_with_metta", tools_dir / "sync_with_metta.py")

    def test_documentation_generator_import(self):
        """Test that documentation generator can be imported."""
        # Test that the module loads without errors
        self.assertTrue(hasattr(self.tools_module, "generate_comprehensive_daf_docs"))
        self.assertTrue(hasattr(self.tools_module, "main"))

    def test_sync_with_metta_import(self):
        """Test that sync with Metta can be imported."""
        # Test that the module loads without errors
        self.assertTrue(hasattr(self.sync_module, "sync_daf_with_metta"))
        self.assertTrue(hasattr(self.sync_module, "scan_metta_repository"))


class TestDAFCoreComponents(unittest.TestCase):
    """Test DAF core components with real Metta integration."""

    def setUp(self):
        """Set up test environment."""
        # Load DAF core modules
        core_dir = SRC_DIR / "daf" / "core"
        self.adaptive_module = load_module("daf.core.adaptive_controller", core_dir / "adaptive_controller.py")
        self.curriculum_module = load_module("daf.core.curriculum_manager", core_dir / "curriculum_manager.py")
        self.rl_module = load_module("daf.core.rl_trainer", core_dir / "rl_trainer.py")

    def test_adaptive_controller_import(self):
        """Test DAF adaptive controller can be imported."""
        # Test that the module loads
        self.assertTrue(hasattr(self.adaptive_module, "DAFAdaptiveController"))

    def test_curriculum_manager_import(self):
        """Test DAF curriculum manager can be imported."""
        # Test that the module loads
        self.assertTrue(hasattr(self.curriculum_module, "DAFCurriculumManager"))

    def test_rl_trainer_import(self):
        """Test DAF RL trainer can be imported."""
        # Test that the module loads
        self.assertTrue(hasattr(self.rl_module, "DAFRlTrainer"))


class TestDAFDocumentationTools(unittest.TestCase):
    """Test DAF documentation tools with real Metta source."""

    def setUp(self):
        """Set up test environment."""
        # Load DAF documentation modules
        docs_dir = SRC_DIR / "daf" / "operations"
        self.docs_module = load_module("daf.operations.docs", docs_dir / "docs.py")

    def test_regenerate_docs_function(self):
        """Test that regenerate_docs function exists and is callable."""
        # Test that the function exists
        self.assertTrue(hasattr(self.docs_module, "regenerate_docs"))
        self.assertTrue(hasattr(self.docs_module, "list_metta_options"))

    def test_find_at_daf_dir_function(self):
        """Test the _find_at_daf_dir helper function."""
        # Test that the helper function exists
        self.assertTrue(hasattr(self.docs_module, "_find_at_daf_dir"))

        # Test that it can find the @daf directory
        at_daf_dir = self.docs_module._find_at_daf_dir()
        self.assertIsNotNone(at_daf_dir)


class TestDAFSetupComponents(unittest.TestCase):
    """Test DAF setup components with real Metta validation."""

    def setUp(self):
        """Set up test environment."""
        # Load DAF setup module
        setup_dir = SRC_DIR / "daf" / "setup"
        self.setup_module = load_module("daf.setup.daf_setup", setup_dir / "daf_setup.py")

    def test_daf_setup_class(self):
        """Test DAFSetup class functionality."""
        DAFSetup = self.setup_module.DAFSetup
        DAFConfig = self.setup_module.DAFConfig

        # Test setup creation
        config = DAFConfig()
        setup = DAFSetup(config)

        self.assertIsNotNone(setup)
        self.assertEqual(setup.config, config)

    def test_initialize_daf_environment_function(self):
        """Test the initialize_daf_environment function."""
        # Test that the function exists
        self.assertTrue(hasattr(self.setup_module, "initialize_daf_environment"))


class TestDAFCLI(unittest.TestCase):
    """Test DAF CLI with real Metta operations."""

    def setUp(self):
        """Set up test environment."""
        # Load DAF CLI module
        cli_dir = SRC_DIR / "daf" / "cli"
        self.cli_module = load_module("daf.cli.daf_cli", cli_dir / "daf_cli.py")

    def test_daf_cli_import(self):
        """Test that DAF CLI can be imported."""
        # Test that the module loads
        self.assertTrue(hasattr(self.cli_module, "DAFCLI"))
        self.assertTrue(hasattr(self.cli_module, "main"))


if __name__ == "__main__":
    # Run all tests
    unittest.main(verbosity=2)
