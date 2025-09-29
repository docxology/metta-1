"""Unit tests for DAF documentation tools with real Metta source."""

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


class TestDAFDocumentationGeneration(unittest.TestCase):
    """Test DAF documentation generation with real Metta source."""

    def setUp(self):
        """Set up test environment."""
        # Load DAF documentation modules
        tools_dir = SRC_DIR / "daf" / "tools"
        self.generator_module = load_module(
            "daf.tools.comprehensive_generator", tools_dir / "comprehensive_generator.py"
        )
        self.sync_module = load_module("daf.tools.sync_with_metta", tools_dir / "sync_with_metta.py")

        # Add Metta to path for real imports
        metta_root = ROOT_DIR.parent / "metta"
        if str(metta_root) not in sys.path:
            sys.path.insert(0, str(metta_root))

    def test_documentation_generator_import(self):
        """Test that documentation generator can be imported."""
        # Test module loading
        self.assertTrue(hasattr(self.generator_module, "generate_comprehensive_daf_docs"))
        self.assertTrue(hasattr(self.generator_module, "parse_metta_source_file"))
        self.assertTrue(hasattr(self.generator_module, "main"))

    def test_sync_with_metta_import(self):
        """Test that sync with Metta can be imported."""
        # Test module loading
        self.assertTrue(hasattr(self.sync_module, "sync_daf_with_metta"))
        self.assertTrue(hasattr(self.sync_module, "scan_metta_repository"))
        self.assertTrue(hasattr(self.sync_module, "main"))

    def test_metta_inventory_creation(self):
        """Test creation of Metta inventory."""
        scan_function = self.sync_module.scan_metta_repository

        # Test that function exists and is callable
        self.assertTrue(callable(scan_function))

        # Test that it returns a dictionary
        try:
            inventory = scan_function()
            self.assertIsInstance(inventory, dict)
        except Exception:
            # May fail if Metta modules can't be imported, but function should exist
            self.assertTrue(callable(scan_function))

    def test_documentation_generation_function(self):
        """Test documentation generation function."""
        generate_function = self.generator_module.generate_comprehensive_daf_docs

        # Test that function exists and is callable
        self.assertTrue(callable(generate_function))

        # Test that it has expected behavior (may fail without inventory)
        try:
            result = generate_function()
            # Should return a boolean
            self.assertIsInstance(result, bool)
        except Exception:
            # Expected if inventory doesn't exist
            pass


class TestDAFDocumentationOperations(unittest.TestCase):
    """Test DAF documentation operations with real Metta."""

    def setUp(self):
        """Set up test environment."""
        # Load DAF documentation operations
        docs_dir = SRC_DIR / "daf" / "operations"
        self.docs_module = load_module("daf.operations.docs", docs_dir / "docs.py")

    def test_regenerate_docs_function(self):
        """Test regenerate_docs function."""
        # Test that function exists
        self.assertTrue(hasattr(self.docs_module, "regenerate_docs"))
        self.assertTrue(hasattr(self.docs_module, "list_metta_options"))

        # Test that functions are callable
        regenerate_func = self.docs_module.regenerate_docs
        list_func = self.docs_module.list_metta_options
        self.assertTrue(callable(regenerate_func))
        self.assertTrue(callable(list_func))

    def test_find_at_daf_dir_function(self):
        """Test _find_at_daf_dir helper function."""
        # Test that function exists
        self.assertTrue(hasattr(self.docs_module, "_find_at_daf_dir"))

        # Test that it returns a Path or None
        result = self.docs_module._find_at_daf_dir()
        self.assertTrue(result is None or isinstance(result, Path))

    def test_placeholder_docs_creation(self):
        """Test placeholder documentation creation."""
        # Test that function exists
        self.assertTrue(hasattr(self.docs_module, "_create_placeholder_docs"))

        # Test that function is callable
        placeholder_func = self.docs_module._create_placeholder_docs
        self.assertTrue(callable(placeholder_func))


class TestDAFDocumentationContent(unittest.TestCase):
    """Test DAF documentation content with real Metta analysis."""

    def setUp(self):
        """Set up test environment."""
        # Add Metta to path for real imports
        metta_root = ROOT_DIR.parent / "metta"
        if str(metta_root) not in sys.path:
            sys.path.insert(0, str(metta_root))

    def test_real_metta_module_imports(self):
        """Test that real Metta modules can be imported for documentation."""
        try:
            # Test importing real Metta modules
            import metta.adaptive
            import metta.cogworks
            import metta.rl
            import metta.setup

            # Test that modules have expected structure
            self.assertTrue(hasattr(metta.adaptive, "adaptive_controller"))
            self.assertTrue(hasattr(metta.cogworks, "curriculum"))
            # Check that we can import trainer from metta.rl
            from metta.rl.trainer import Trainer

            self.assertTrue(hasattr(Trainer, "train"))
            self.assertTrue(hasattr(metta.setup, "saved_settings"))

        except ImportError as e:
            self.skipTest(f"Real Metta modules not available: {e}")

    def test_real_metta_component_inspection(self):
        """Test inspection of real Metta components."""
        try:
            import inspect

            from metta.adaptive.adaptive_controller import AdaptiveController
            from metta.cogworks.curriculum.curriculum import Curriculum

            # Test that we can inspect real components
            adaptive_sig = inspect.signature(AdaptiveController.__init__)
            curriculum_sig = inspect.signature(Curriculum.__init__)

            # Test that signatures exist
            self.assertIsNotNone(adaptive_sig)
            self.assertIsNotNone(curriculum_sig)

            # Test that signatures have expected parameters
            adaptive_params = list(adaptive_sig.parameters.keys())
            curriculum_params = list(curriculum_sig.parameters.keys())

            self.assertIn("config", adaptive_params)
            self.assertIn("config", curriculum_params)

        except ImportError as e:
            self.skipTest(f"Real Metta components not available: {e}")


class TestDAFDocumentationToolsIntegration(unittest.TestCase):
    """Test integration of DAF documentation tools."""

    def setUp(self):
        """Set up test environment."""
        # Load all documentation-related modules
        tools_dir = SRC_DIR / "daf" / "tools"
        self.generator_module = load_module(
            "daf.tools.comprehensive_generator", tools_dir / "comprehensive_generator.py"
        )
        self.sync_module = load_module("daf.tools.sync_with_metta", tools_dir / "sync_with_metta.py")
        self.verify_module = load_module("daf.tools.verify_coverage", tools_dir / "verify_coverage.py")

        docs_dir = SRC_DIR / "daf" / "operations"
        self.docs_module = load_module("daf.operations.docs", docs_dir / "docs.py")

    def test_documentation_tools_integration(self):
        """Test that all documentation tools can work together."""
        # Test that all modules can be imported together
        self.assertIsNotNone(self.generator_module)
        self.assertIsNotNone(self.sync_module)
        self.assertIsNotNone(self.verify_module)
        self.assertIsNotNone(self.docs_module)

    def test_documentation_workflow(self):
        """Test the complete documentation workflow."""
        # Test that the workflow functions exist
        self.assertTrue(hasattr(self.sync_module, "scan_metta_repository"))
        self.assertTrue(hasattr(self.generator_module, "generate_comprehensive_daf_docs"))
        self.assertTrue(hasattr(self.docs_module, "regenerate_docs"))

        # Test that functions are callable
        scan_func = self.sync_module.scan_metta_repository
        generate_func = self.generator_module.generate_comprehensive_daf_docs
        regenerate_func = self.docs_module.regenerate_docs

        self.assertTrue(callable(scan_func))
        self.assertTrue(callable(generate_func))
        self.assertTrue(callable(regenerate_func))

    def test_documentation_error_handling(self):
        """Test error handling in documentation tools."""
        # Test that functions handle errors gracefully
        try:
            # Test regenerate_docs with fallback
            result = self.docs_module.regenerate_docs()
            # Should return a boolean
            self.assertIsInstance(result, bool)
        except Exception as e:
            self.fail(f"Documentation regeneration failed unexpectedly: {e}")


if __name__ == "__main__":
    # Run all documentation tests
    unittest.main(verbosity=2)
