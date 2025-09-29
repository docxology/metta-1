"""Functional tests for core DAF methods that work with real Metta."""

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


class TestDAFCoreFunctionality(unittest.TestCase):
    """Test core DAF functionality that actually works."""

    def setUp(self):
        """Set up test environment."""
        # Ensure DAF src is in path for imports
        daf_src = ROOT_DIR / "daf" / "src"
        if str(daf_src) not in sys.path:
            sys.path.insert(0, str(daf_src))

        # Load DAF main modules
        daf_main_path = ROOT_DIR / "daf" / "daf_main.py"
        if not daf_main_path.exists():
            # Alternative path structure
            daf_main_path = ROOT_DIR.parent / "daf" / "daf_main.py"
        self.daf_main_module = load_module("daf_main", daf_main_path)

        # Load DAF configuration
        config_dir = SRC_DIR / "daf" / "config"
        self.config_module = load_module("daf.config.daf_config", config_dir / "daf_config.py")

        # Add Metta to path for real imports
        metta_root = ROOT_DIR.parent / "metta"
        if str(metta_root) not in sys.path:
            sys.path.insert(0, str(metta_root))

    def test_daf_main_basic_import(self):
        """Test that daf_main can be imported and has basic functionality."""
        # Test that the module loads
        self.assertTrue(hasattr(self.daf_main_module, "main"))
        self.assertTrue(hasattr(self.daf_main_module, "show_interactive_menu"))

        # Test that main function is callable
        main_func = self.daf_main_module.main
        self.assertTrue(callable(main_func))

    def test_daf_config_basic_functionality(self):
        """Test basic DAF configuration functionality."""
        DAFConfig = self.config_module.DAFConfig

        # Test config creation
        config = DAFConfig()
        self.assertIsNotNone(config)
        self.assertEqual(config.experiment_name, "daf_experiment")
        self.assertEqual(config.version, "1.0.0")
        self.assertTrue(config.generate_docs_on_startup)

    def test_real_metta_basic_imports(self):
        """Test basic real Metta imports that should work."""
        try:
            # Test importing basic Metta modules
            import metta.adaptive
            import metta.cogworks
            import metta.rl

            # Test that modules have expected attributes
            self.assertTrue(hasattr(metta.adaptive, "adaptive_controller"))
            self.assertTrue(hasattr(metta.rl, "trainer"))

        except ImportError as e:
            self.skipTest(f"Real Metta modules not available: {e}")


class TestDAFDocumentationBasics(unittest.TestCase):
    """Test basic DAF documentation functionality."""

    def setUp(self):
        """Set up test environment."""
        # Load DAF documentation modules
        docs_dir = SRC_DIR / "daf" / "operations"
        self.docs_module = load_module("daf.operations.docs", docs_dir / "docs.py")

    def test_documentation_functions_exist(self):
        """Test that documentation functions exist."""
        # Test that functions exist
        self.assertTrue(hasattr(self.docs_module, "regenerate_docs"))
        self.assertTrue(hasattr(self.docs_module, "list_metta_options"))
        self.assertTrue(hasattr(self.docs_module, "_find_at_daf_dir"))

        # Test that functions are callable
        self.assertTrue(callable(self.docs_module.regenerate_docs))
        self.assertTrue(callable(self.docs_module.list_metta_options))
        self.assertTrue(callable(self.docs_module._find_at_daf_dir))

    def test_find_at_daf_dir_function(self):
        """Test the _find_at_daf_dir helper function."""
        result = self.docs_module._find_at_daf_dir()
        # Should return a Path or None
        self.assertTrue(result is None or isinstance(result, Path))


class TestDAFRealMettaIntegration(unittest.TestCase):
    """Test DAF integration with real Metta components."""

    def setUp(self):
        """Set up test environment."""
        # Add Metta to path for real imports
        metta_root = ROOT_DIR.parent / "metta"
        if str(metta_root) not in sys.path:
            sys.path.insert(0, str(metta_root))

    def test_real_metta_adaptive_controller(self):
        """Test real Metta AdaptiveController functionality."""
        try:
            import inspect

            from metta.adaptive.adaptive_config import AdaptiveConfig
            from metta.adaptive.adaptive_controller import AdaptiveController

            # Test that we can create and inspect real components
            config = AdaptiveConfig()
            self.assertIsNotNone(config)

            # Test signature inspection
            sig = inspect.signature(AdaptiveController.__init__)
            params = list(sig.parameters.keys())
            self.assertIn("config", params)

        except ImportError as e:
            self.skipTest(f"Real Metta AdaptiveController not available: {e}")

    def test_real_metta_curriculum(self):
        """Test real Metta Curriculum functionality."""
        try:
            import inspect

            from metta.cogworks.curriculum.curriculum import Curriculum

            # Test that we can inspect real components
            sig = inspect.signature(Curriculum.__init__)
            params = list(sig.parameters.keys())
            self.assertIn("config", params)

        except ImportError as e:
            self.skipTest(f"Real Metta Curriculum not available: {e}")

    def test_real_metta_rl_trainer(self):
        """Test real Metta RL Trainer functionality."""
        try:
            import inspect

            from metta.rl.trainer import Trainer

            # Test that we can inspect real components
            sig = inspect.signature(Trainer.__init__)
            params = list(sig.parameters.keys())
            # Note: Real Metta Trainer uses 'cfg' not 'config'
            self.assertIn("cfg", params)

        except ImportError as e:
            self.skipTest(f"Real Metta RL Trainer not available: {e}")


class TestDAFWorkflow(unittest.TestCase):
    """Test complete DAF workflow."""

    def test_daf_main_workflow(self):
        """Test the main DAF workflow."""
        # Test that the main module can be imported
        # Ensure DAF src is in path for imports
        daf_src = ROOT_DIR / "daf" / "src"
        if str(daf_src) not in sys.path:
            sys.path.insert(0, str(daf_src))

        daf_main_path = ROOT_DIR / "daf" / "daf_main.py"
        if not daf_main_path.exists():
            # Alternative path structure
            daf_main_path = ROOT_DIR.parent / "daf" / "daf_main.py"
        daf_main_module = load_module("daf_main", daf_main_path)
        self.assertIsNotNone(daf_main_module)

        # Test that main function exists
        self.assertTrue(hasattr(daf_main_module, "main"))
        main_func = daf_main_module.main
        self.assertTrue(callable(main_func))

    def test_daf_documentation_workflow(self):
        """Test the documentation workflow."""
        # Test that documentation operations can be imported
        docs_dir = SRC_DIR / "daf" / "operations"
        docs_module = load_module("daf.operations.docs", docs_dir / "docs.py")
        self.assertIsNotNone(docs_module)

        # Test that key functions exist
        self.assertTrue(hasattr(docs_module, "regenerate_docs"))
        self.assertTrue(hasattr(docs_module, "list_metta_options"))


if __name__ == "__main__":
    # Run focused functional tests
    unittest.main(verbosity=2)
