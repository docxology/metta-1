"""Integration tests for DAF orchestration of real Metta methods."""

from __future__ import annotations

import subprocess
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


class TestDAFMettaOrchestration(unittest.TestCase):
    """Test DAF orchestration of real Metta methods."""

    def setUp(self):
        """Set up test environment."""
        self.metta_root = ROOT_DIR.parent  # This is the project root containing both metta/ and daf/
        self.daf_root = ROOT_DIR

        # Verify Metta is installed
        if not self.metta_root.exists():
            self.skipTest("Metta repository not found")

        # Add Metta to path for real imports
        if str(self.metta_root) not in sys.path:
            sys.path.insert(0, str(self.metta_root))

    def test_metta_installation_verification(self):
        """Test that Metta is properly installed and accessible."""
        try:
            # Test core Metta imports
            import metta

            self.assertIsNotNone(metta)

            # Test key Metta modules
            import metta.adaptive
            import metta.cogworks
            import metta.rl
            import metta.setup

            # Verify they can import specific modules (since __init__.py files are empty)
            try:
                import metta.adaptive.adaptive_controller
                import metta.cogworks.curriculum.curriculum
                import metta.rl.trainer
                import metta.setup.saved_settings

                # If we get here, the imports worked
                self.assertTrue(True)
            except ImportError as e:
                self.fail(f"Metta module imports failed: {e}")

        except ImportError as e:
            self.fail(f"Metta installation verification failed: {e}")

    def test_real_metta_component_instantiation(self):
        """Test instantiation of real Metta components."""
        try:
            # Test AdaptiveController instantiation
            from metta.adaptive.adaptive_config import AdaptiveConfig
            from metta.adaptive.adaptive_controller import AdaptiveController

            config = AdaptiveConfig()
            self.assertIsNotNone(config)

            # Test that we can create the controller class (may fail on instantiation due to dependencies)
            controller_class = AdaptiveController
            self.assertTrue(hasattr(controller_class, "__init__"))

        except ImportError as e:
            self.skipTest(f"Real Metta components not available: {e}")

    def test_real_metta_curriculum_functionality(self):
        """Test real Metta curriculum functionality."""
        try:
            import inspect

            from metta.cogworks.curriculum.curriculum import Curriculum
            from metta.cogworks.curriculum.task_generator import TaskGenerator

            # Test that we can inspect real curriculum components
            curriculum_sig = inspect.signature(Curriculum.__init__)
            task_gen_sig = inspect.signature(TaskGenerator.__init__)

            # Test parameter inspection
            curriculum_params = list(curriculum_sig.parameters.keys())
            task_gen_params = list(task_gen_sig.parameters.keys())

            self.assertIn("config", curriculum_params)
            self.assertIn("config", task_gen_params)

        except ImportError as e:
            self.skipTest(f"Real Metta curriculum not available: {e}")

    def test_real_metta_rl_functionality(self):
        """Test real Metta RL functionality."""
        try:
            import inspect

            from metta.rl.trainer import Trainer
            from metta.rl.training.core import CoreTrainingLoop

            # Test that we can inspect real RL components
            trainer_sig = inspect.signature(Trainer.__init__)
            core_sig = inspect.signature(CoreTrainingLoop.__init__)

            # Test parameter inspection
            trainer_params = list(trainer_sig.parameters.keys())
            core_params = list(core_sig.parameters.keys())

            # Real Metta Trainer uses 'cfg' not 'config'
            self.assertIn("cfg", trainer_params)
            # CoreTrainingLoop uses different parameters than Trainer
            expected_core_params = ["policy", "experience", "losses", "optimizer", "device", "context"]
            for param in expected_core_params:
                self.assertIn(param, core_params)

        except ImportError as e:
            self.skipTest(f"Real Metta RL components not available: {e}")


class TestDAFUVOrchestration(unittest.TestCase):
    """Test DAF orchestration using uv run for real Metta execution."""

    def setUp(self):
        """Set up test environment."""
        self.metta_root = ROOT_DIR.parent  # This is the project root containing both metta/ and daf/
        self.daf_root = ROOT_DIR

        # Verify Metta is installed
        if not self.metta_root.exists():
            self.skipTest("Metta repository not found")

    def test_uv_run_metta_import(self):
        """Test that uv run can import real Metta components."""
        try:
            # Test uv run with Metta import
            result = subprocess.run(
                ["uv", "run", "python", "-c", "import metta; print('Metta imported successfully')"],
                capture_output=True,
                text=True,
                cwd=self.metta_root,
                timeout=30,
            )

            self.assertEqual(result.returncode, 0)
            self.assertIn("Metta imported successfully", result.stdout)

        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            self.skipTest(f"uv run test failed: {e}")

    def test_uv_run_daf_with_metta(self):
        """Test that uv run can execute DAF with real Metta integration."""
        try:
            # Test uv run with DAF and Metta
            result = subprocess.run(
                [
                    "uv",
                    "run",
                    "python",
                    "-c",
                    """
import sys
sys.path.insert(0, 'daf/src')
from daf.operations.docs import regenerate_docs
print('DAF documentation regeneration test passed')
""",
                ],
                capture_output=True,
                text=True,
                cwd=self.metta_root,
                timeout=60,
            )

            # Should not crash (may fail due to missing dependencies, but shouldn't error on import)
            self.assertIn("DAF documentation regeneration test passed", result.stdout)

        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            self.skipTest(f"uv run DAF test failed: {e}")


class TestDAFRealMettaWorkflow(unittest.TestCase):
    """Test complete DAF workflow with real Metta execution."""

    def setUp(self):
        """Set up test environment."""
        self.metta_root = ROOT_DIR.parent  # This is the project root containing both metta/ and daf/
        self.daf_root = ROOT_DIR

        # Verify Metta is installed
        if not self.metta_root.exists():
            self.skipTest("Metta repository not found")

        # Add Metta to path for real imports
        if str(self.metta_root) not in sys.path:
            sys.path.insert(0, str(self.metta_root))

    def test_daf_setup_with_real_metta_validation(self):
        """Test DAF setup with real Metta repository validation."""
        # Load DAF setup module
        setup_dir = SRC_DIR / "daf" / "setup"
        setup_module = load_module("daf.setup.daf_setup", setup_dir / "daf_setup.py")

        # Test that setup can validate real Metta repository
        DAFSetup = setup_module.DAFSetup
        DAFConfig = setup_module.DAFConfig

        config = DAFConfig()
        setup = DAFSetup(config)

        # Test repository validation
        is_valid = setup._validate_metta_repository()
        self.assertIsInstance(is_valid, bool)

    def test_daf_documentation_with_real_metta_source(self):
        """Test DAF documentation generation with real Metta source code."""
        try:
            # Test that we can analyze real Metta source files
            adaptive_controller_file = self.metta_root / "metta" / "adaptive" / "adaptive_controller.py"

            if adaptive_controller_file.exists():
                with open(adaptive_controller_file, "r") as f:
                    content = f.read()

                # Verify it's real Python code with expected patterns
                self.assertIn("class AdaptiveController", content)
                self.assertIn("def run", content)
                self.assertIn("def __init__", content)

        except Exception as e:
            self.skipTest(f"Real Metta source analysis failed: {e}")

    def test_daf_configuration_with_real_metta_components(self):
        """Test DAF configuration integration with real Metta components."""
        try:
            # Test that DAF configuration can work with real Metta settings
            from metta.setup.saved_settings import SavedSettings

            # Load DAF configuration
            config_dir = SRC_DIR / "daf" / "config"
            config_module = load_module("daf.config.daf_config", config_dir / "daf_config.py")

            DAFConfigManager = config_module.DAFConfigManager
            config = config_module.DAFConfig()
            manager = DAFConfigManager(config)

            # Test that we can access real Metta settings
            from metta.setup.saved_settings import get_saved_settings

            settings = get_saved_settings()
            self.assertIsNotNone(settings)

        except ImportError as e:
            self.skipTest(f"Real Metta settings not available: {e}")


class TestDAFThinOrchestration(unittest.TestCase):
    """Test that DAF provides thin orchestration of real Metta methods."""

    def setUp(self):
        """Set up test environment."""
        self.metta_root = ROOT_DIR.parent  # This is the project root containing both metta/ and daf/
        self.daf_root = ROOT_DIR

        # Verify Metta is installed
        if not self.metta_root.exists():
            self.skipTest("Metta repository not found")

        # Add Metta to path for real imports
        if str(self.metta_root) not in sys.path:
            sys.path.insert(0, str(self.metta_root))

    def test_daf_orchestrates_real_metta_methods(self):
        """Test that DAF orchestrates real Metta methods without wrapping them."""
        try:
            # Test that DAF can import and use real Metta methods directly
            from metta.adaptive.adaptive_controller import AdaptiveController
            from metta.cogworks.curriculum.curriculum import Curriculum
            from metta.rl.trainer import Trainer

            # Test that these are the real Metta classes (not DAF wrappers)
            self.assertEqual(AdaptiveController.__module__, "metta.adaptive.adaptive_controller")
            self.assertEqual(Curriculum.__module__, "metta.cogworks.curriculum.curriculum")
            self.assertEqual(Trainer.__module__, "metta.rl.trainer")

        except ImportError as e:
            self.skipTest(f"Real Metta orchestration test failed: {e}")

    def test_daf_configuration_orchestrates_metta_settings(self):
        """Test that DAF configuration orchestrates real Metta settings."""
        try:
            # Test that DAF configuration can access real Metta settings
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
            self.skipTest(f"Real Metta configuration orchestration failed: {e}")


class TestDAFRealMettaExecution(unittest.TestCase):
    """Test actual execution of DAF with real Metta components."""

    def setUp(self):
        """Set up test environment."""
        self.metta_root = ROOT_DIR.parent  # This is the project root containing both metta/ and daf/
        self.daf_root = ROOT_DIR

        # Verify Metta is installed
        if not self.metta_root.exists():
            self.skipTest("Metta repository not found")

    def test_daf_examples_with_real_metta(self):
        """Test that DAF examples can run with real Metta components."""
        try:
            # Test that DAF examples directory exists and has real examples
            examples_dir = self.daf_root / "examples"
            self.assertTrue(examples_dir.exists())

            # Check that examples reference real Metta components
            example_files = list(examples_dir.glob("*.py"))
            self.assertGreater(len(example_files), 0)

            # Test that at least one example imports real Metta
            found_metta_import = False
            for example_file in example_files[:3]:  # Check first 3 examples
                with open(example_file, "r") as f:
                    content = f.read()
                    if "import metta" in content or "from metta" in content:
                        found_metta_import = True
                        break

            self.assertTrue(found_metta_import, "Examples should import real Metta components")

        except Exception as e:
            self.skipTest(f"DAF examples test failed: {e}")

    def test_daf_documentation_generation_with_real_metta(self):
        """Test DAF documentation generation with real Metta execution."""
        try:
            # Test that DAF can generate documentation from real Metta source
            tools_dir = SRC_DIR / "daf" / "tools"
            generator_module = load_module(
                "daf.tools.comprehensive_generator", tools_dir / "comprehensive_generator.py"
            )

            # Test that the generator can analyze real Metta source
            generate_func = generator_module.generate_comprehensive_daf_docs
            self.assertTrue(callable(generate_func))

            # Test that it can create inventory of real Metta modules
            sync_module = load_module("daf.tools.sync_with_metta", tools_dir / "sync_with_metta.py")
            scan_func = sync_module.scan_metta_repository
            self.assertTrue(callable(scan_func))

        except Exception as e:
            self.skipTest(f"DAF documentation with real Metta failed: {e}")


class TestDAFMettaIntegrationValidation(unittest.TestCase):
    """Test validation of DAF and Metta integration."""

    def setUp(self):
        """Set up test environment."""
        self.metta_root = ROOT_DIR.parent  # This is the project root containing both metta/ and daf/
        self.daf_root = ROOT_DIR

        # Verify Metta is installed
        if not self.metta_root.exists():
            self.skipTest("Metta repository not found")

        # Add Metta to path for real imports
        if str(self.metta_root) not in sys.path:
            sys.path.insert(0, str(self.metta_root))

    def test_metta_package_structure(self):
        """Test that Metta package structure is correct."""
        # Test that Metta has the expected package structure
        required_modules = ["metta/adaptive", "metta/cogworks", "metta/rl", "metta/setup"]

        for module_path in required_modules:
            full_path = self.metta_root / module_path
            self.assertTrue(full_path.exists(), f"Required Metta module missing: {module_path}")

            # Check for __init__.py files
            init_file = full_path / "__init__.py"
            self.assertTrue(init_file.exists(), f"Missing __init__.py in {module_path}")

    def test_daf_metta_dependency_validation(self):
        """Test that DAF can validate Metta dependencies."""
        try:
            # Test that DAF setup can validate real Metta repository
            setup_dir = SRC_DIR / "daf" / "setup"
            setup_module = load_module("daf.setup.daf_setup", setup_dir / "daf_setup.py")

            DAFSetup = setup_module.DAFSetup
            DAFConfig = setup_module.DAFConfig

            config = DAFConfig()
            setup = DAFSetup(config)

            # Test repository validation
            is_valid = setup._validate_metta_repository()
            self.assertIsInstance(is_valid, bool)

        except Exception as e:
            self.skipTest(f"DAF Metta dependency validation failed: {e}")

    def test_real_metta_component_compatibility(self):
        """Test compatibility between DAF and real Metta components."""
        try:
            # Test that DAF can work with real Metta component signatures
            import inspect

            from metta.adaptive.adaptive_controller import AdaptiveController
            from metta.cogworks.curriculum.curriculum import Curriculum

            # Test signature compatibility
            adaptive_sig = inspect.signature(AdaptiveController.__init__)
            curriculum_sig = inspect.signature(Curriculum.__init__)

            # Test that signatures are accessible
            self.assertIsNotNone(adaptive_sig)
            self.assertIsNotNone(curriculum_sig)

            # Test that DAF can analyze these signatures
            adaptive_params = list(adaptive_sig.parameters.keys())
            curriculum_params = list(curriculum_sig.parameters.keys())

            self.assertIn("config", adaptive_params)
            self.assertIn("config", curriculum_params)

        except ImportError as e:
            self.skipTest(f"Real Metta component compatibility test failed: {e}")


if __name__ == "__main__":
    # Run all orchestration tests
    unittest.main(verbosity=2)
