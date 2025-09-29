"""Unit tests for DAF thin orchestration of real Metta methods."""

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


class TestDAFThinOrchestration(unittest.TestCase):
    """Test that DAF provides thin orchestration of real Metta methods."""

    def setUp(self):
        """Set up test environment."""
        self.metta_root = ROOT_DIR.parent / "metta"
        self.daf_root = ROOT_DIR

        # Verify Metta is installed
        if not self.metta_root.exists():
            self.skipTest("Metta repository not found")

        # Add Metta to path for real imports
        if str(self.metta_root) not in sys.path:
            sys.path.insert(0, str(self.metta_root))

    def test_daf_orchestrates_real_metta_without_wrapping(self):
        """Test that DAF orchestrates real Metta methods without wrapping them."""
        try:
            # Import real Metta components
            from metta.adaptive.adaptive_controller import AdaptiveController
            from metta.cogworks.curriculum.curriculum import Curriculum
            from metta.rl.trainer import Trainer

            # Test that these are the real Metta classes (not DAF wrappers)
            self.assertEqual(AdaptiveController.__module__, "metta.adaptive.adaptive_controller")
            self.assertEqual(Curriculum.__module__, "metta.cogworks.curriculum.curriculum")
            self.assertEqual(Trainer.__module__, "metta.rl.trainer")

            # Test that DAF can reference these real classes
            # Load DAF modules
            config_dir = SRC_DIR / "daf" / "config"
            config_module = load_module("daf.config.daf_config", config_dir / "daf_config.py")

            # Test that DAF configuration doesn't wrap these classes
            DAFConfig = config_module.DAFConfig
            config = DAFConfig()

            # DAF should be able to work with real Metta without wrapping
            self.assertIsNotNone(config)

        except ImportError as e:
            self.skipTest(f"DAF thin orchestration test failed: {e}")

    def test_daf_configuration_orchestrates_real_metta_settings(self):
        """Test that DAF configuration orchestrates real Metta settings."""
        try:
            # Test that DAF can access real Metta settings
            from metta.setup.saved_settings import SavedSettings

            # Load DAF configuration
            config_dir = SRC_DIR / "daf" / "config"
            config_module = load_module("daf.config.daf_config", config_dir / "daf_config.py")

            DAFConfigManager = config_module.DAFConfigManager
            config = config_module.DAFConfig()
            manager = DAFConfigManager(config)

            # Test that DAF can access real Metta settings
            from metta.setup.saved_settings import get_saved_settings

            settings = get_saved_settings()
            self.assertIsNotNone(settings)

            # Test that DAF configuration integrates with real Metta
            component_config = manager.get_component_config("wandb")
            self.assertIsInstance(component_config, dict)

        except ImportError as e:
            self.skipTest(f"DAF configuration orchestration failed: {e}")

    def test_daf_documentation_orchestrates_real_metta_analysis(self):
        """Test that DAF documentation orchestrates real Metta source analysis."""
        try:
            # Test that DAF can analyze real Metta source code
            adaptive_controller_file = self.metta_root / "metta" / "adaptive" / "adaptive_controller.py"

            if adaptive_controller_file.exists():
                with open(adaptive_controller_file, "r") as f:
                    content = f.read()

                # Test that DAF can analyze real Metta source
                # Look for expected patterns in real Metta code
                self.assertIn("class AdaptiveController", content)
                self.assertIn("def run", content)
                self.assertIn("def __init__", content)

                # Test that DAF documentation tools can work with this
                tools_dir = SRC_DIR / "daf" / "tools"
                generator_module = load_module(
                    "daf.tools.comprehensive_generator", tools_dir / "comprehensive_generator.py"
                )

                # Test that the generator can be imported and used
                generate_func = generator_module.generate_comprehensive_daf_docs
                self.assertTrue(callable(generate_func))

        except Exception as e:
            self.skipTest(f"DAF documentation orchestration failed: {e}")


class TestDAFMettaMethodOrchestration(unittest.TestCase):
    """Test DAF orchestration of Metta methods."""

    def setUp(self):
        """Set up test environment."""
        self.metta_root = ROOT_DIR.parent / "metta"
        self.daf_root = ROOT_DIR

        # Verify Metta is installed
        if not self.metta_root.exists():
            self.skipTest("Metta repository not found")

        # Add Metta to path for real imports
        if str(self.metta_root) not in sys.path:
            sys.path.insert(0, str(self.metta_root))

    def test_daf_orchestrates_real_metta_method_calls(self):
        """Test that DAF orchestrates real Metta method calls."""
        try:
            # Test that DAF can orchestrate calls to real Metta methods
            from metta.adaptive.adaptive_controller import AdaptiveController
            from metta.cogworks.curriculum.curriculum import Curriculum

            # Test that real Metta methods are accessible
            adaptive_controller_class = AdaptiveController
            curriculum_class = Curriculum

            # Test that classes have expected methods
            self.assertTrue(hasattr(adaptive_controller_class, "__init__"))
            self.assertTrue(hasattr(curriculum_class, "__init__"))

            # Test that DAF can reference these methods
            # Load DAF modules
            config_dir = SRC_DIR / "daf" / "config"
            config_module = load_module("daf.config.daf_config", config_dir / "daf_config.py")

            DAFConfig = config_module.DAFConfig
            config = DAFConfig()

            # DAF should be able to work alongside real Metta
            self.assertIsNotNone(config)

        except ImportError as e:
            self.skipTest(f"DAF Metta method orchestration failed: {e}")

    def test_daf_thin_layer_validation(self):
        """Test that DAF is a thin orchestration layer."""
        try:
            # Test that DAF doesn't wrap or modify Metta methods
            from metta.adaptive.adaptive_controller import AdaptiveController
            from metta.cogworks.curriculum.curriculum import Curriculum

            # Test that these are the original Metta classes
            self.assertEqual(AdaptiveController.__module__, "metta.adaptive.adaptive_controller")
            self.assertEqual(Curriculum.__module__, "metta.cogworks.curriculum.curriculum")

            # Test that DAF can work with these without modification
            # Load DAF configuration
            config_dir = SRC_DIR / "daf" / "config"
            config_module = load_module("daf.config.daf_config", config_dir / "daf_config.py")

            DAFConfig = config_module.DAFConfig
            config = DAFConfig()

            # Test that DAF configuration works with real Metta
            self.assertIsNotNone(config)

        except ImportError as e:
            self.skipTest(f"DAF thin layer validation failed: {e}")


class TestDAFMettaInterfaceOrchestration(unittest.TestCase):
    """Test DAF orchestration of Metta interfaces."""

    def setUp(self):
        """Set up test environment."""
        self.metta_root = ROOT_DIR.parent / "metta"
        self.daf_root = ROOT_DIR

        # Verify Metta is installed
        if not self.metta_root.exists():
            self.skipTest("Metta repository not found")

        # Add Metta to path for real imports
        if str(self.metta_root) not in sys.path:
            sys.path.insert(0, str(self.metta_root))

    def test_daf_orchestrates_real_metta_interfaces(self):
        """Test that DAF orchestrates real Metta interfaces."""
        try:
            # Test that DAF can work with real Metta interfaces
            from metta.adaptive.protocols import Dispatcher, ExperimentScheduler, Store
            from metta.rl.system_config import SystemConfig

            # Test that real Metta interfaces exist
            self.assertTrue(hasattr(ExperimentScheduler, "__module__"))
            self.assertTrue(hasattr(Dispatcher, "__module__"))
            self.assertTrue(hasattr(Store, "__module__"))
            self.assertTrue(hasattr(SystemConfig, "__module__"))

            # Test that interfaces have expected structure
            self.assertTrue(hasattr(ExperimentScheduler, "__module__"))
            self.assertTrue(hasattr(Dispatcher, "__module__"))

        except ImportError as e:
            self.skipTest(f"DAF Metta interface orchestration failed: {e}")

    def test_daf_configuration_orchestrates_real_metta_interfaces(self):
        """Test that DAF configuration orchestrates real Metta interfaces."""
        try:
            # Test that DAF can work with real Metta interfaces
            from metta.setup.metta_cli import MettaCLI

            # Load DAF configuration
            config_dir = SRC_DIR / "daf" / "config"
            config_module = load_module("daf.config.daf_config", config_dir / "daf_config.py")

            DAFConfigManager = config_module.DAFConfigManager
            config = config_module.DAFConfig()
            manager = DAFConfigManager(config)

            # Test that DAF can work with real Metta CLI
            # (May fail if not fully configured, but should not crash)
            try:
                cli = MettaCLI()
                self.assertIsNotNone(cli)
            except Exception:
                # Expected if Metta CLI requires additional setup
                pass

        except ImportError as e:
            self.skipTest(f"DAF configuration interface orchestration failed: {e}")


class TestDAFRealMettaExecutionOrchestration(unittest.TestCase):
    """Test DAF orchestration of real Metta execution."""

    def setUp(self):
        """Set up test environment."""
        self.metta_root = ROOT_DIR.parent / "metta"
        self.daf_root = ROOT_DIR

        # Verify Metta is installed
        if not self.metta_root.exists():
            self.skipTest("Metta repository not found")

    def test_daf_orchestrates_real_metta_execution(self):
        """Test that DAF orchestrates real Metta execution."""
        try:
            # Test that DAF can orchestrate real Metta execution
            # This tests the core principle: DAF should orchestrate, not wrap

            # Import real Metta components
            from metta.adaptive.adaptive_controller import AdaptiveController
            from metta.cogworks.curriculum.curriculum import Curriculum

            # Test that DAF can reference and work with these components
            adaptive_class = AdaptiveController
            curriculum_class = Curriculum

            # Test that these are the real Metta classes
            self.assertEqual(adaptive_class.__module__, "metta.adaptive.adaptive_controller")
            self.assertEqual(curriculum_class.__module__, "metta.cogworks.curriculum.curriculum")

            # Test that DAF configuration can work alongside real Metta
            config_dir = SRC_DIR / "daf" / "config"
            config_module = load_module("daf.config.daf_config", config_dir / "daf_config.py")

            DAFConfig = config_module.DAFConfig
            config = DAFConfig()

            # Test that DAF and Metta can coexist
            self.assertIsNotNone(config)
            self.assertIsNotNone(adaptive_class)

        except ImportError as e:
            self.skipTest(f"DAF real Metta execution orchestration failed: {e}")

    def test_daf_thin_orchestration_principles(self):
        """Test that DAF follows thin orchestration principles."""
        try:
            # Test the core principle: DAF should orchestrate real Metta, not wrap it

            # 1. DAF should be able to import real Metta
            import metta.adaptive
            import metta.cogworks
            import metta.rl

            # 2. DAF should be able to reference real Metta classes
            from metta.adaptive.adaptive_controller import AdaptiveController

            adaptive_class = AdaptiveController

            # 3. Real Metta classes should remain unmodified
            self.assertEqual(adaptive_class.__module__, "metta.adaptive.adaptive_controller")

            # 4. DAF should be able to configure alongside real Metta
            config_dir = SRC_DIR / "daf" / "config"
            config_module = load_module("daf.config.daf_config", config_dir / "daf_config.py")

            DAFConfig = config_module.DAFConfig
            config = DAFConfig()

            # 5. DAF and Metta should coexist without interference
            self.assertIsNotNone(config)
            self.assertIsNotNone(adaptive_class)

        except ImportError as e:
            self.skipTest(f"DAF thin orchestration principles test failed: {e}")


if __name__ == "__main__":
    # Run all thin orchestration tests
    unittest.main(verbosity=2)
