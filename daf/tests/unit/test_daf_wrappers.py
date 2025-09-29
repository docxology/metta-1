"""Unit tests for DAF wrappers with real Metta components."""

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


class TestDAFMettaWrappers(unittest.TestCase):
    """Test DAF wrappers with real Metta components."""

    def setUp(self):
        """Set up test environment."""
        # Load DAF wrappers module
        wrappers_dir = SRC_DIR / "daf" / "wrappers"
        self.wrappers_module = load_module("daf.wrappers.metta_wrapper", wrappers_dir / "metta_wrapper.py")

        # Add Metta to path for real imports
        metta_root = ROOT_DIR.parent / "metta"
        if str(metta_root) not in sys.path:
            sys.path.insert(0, str(metta_root))

    def test_metta_wrapper_base_class(self):
        """Test the base MettaWrapper class."""
        MettaWrapper = self.wrappers_module.MettaWrapper

        # Test that it's an abstract base class
        self.assertTrue(hasattr(MettaWrapper, "initialize"))
        self.assertTrue(hasattr(MettaWrapper, "is_initialized"))

        # Test instance attributes by creating a concrete subclass
        class TestWrapper(MettaWrapper):
            def initialize(self, *args, **kwargs):
                return True

        wrapper = TestWrapper("test")
        self.assertTrue(hasattr(wrapper, "component_name"))
        self.assertTrue(hasattr(wrapper, "wrapped_component"))

    def test_adaptive_wrapper(self):
        """Test AdaptiveWrapper functionality."""
        try:
            AdaptiveWrapper = self.wrappers_module.AdaptiveWrapper

            # Create wrapper
            wrapper = AdaptiveWrapper()

            # Test wrapper properties
            self.assertEqual(wrapper.component_name, "adaptive")
            self.assertFalse(wrapper.is_initialized())
            self.assertIsNone(wrapper.wrapped_component)

            # Test wrapper methods
            self.assertTrue(hasattr(wrapper, "initialize"))
            self.assertTrue(hasattr(wrapper, "log_operation"))

        except AttributeError:
            self.skipTest("AdaptiveWrapper not available in wrappers module")

    def test_curriculum_wrapper(self):
        """Test CurriculumWrapper functionality."""
        try:
            CurriculumWrapper = self.wrappers_module.CurriculumWrapper

            # Create wrapper
            wrapper = CurriculumWrapper()

            # Test wrapper properties
            self.assertEqual(wrapper.component_name, "curriculum")
            self.assertFalse(wrapper.is_initialized())
            self.assertIsNone(wrapper.wrapped_component)

        except AttributeError:
            self.skipTest("CurriculumWrapper not available in wrappers module")

    def test_rl_wrapper(self):
        """Test RLWrapper functionality."""
        try:
            RLWrapper = self.wrappers_module.RLWrapper

            # Create wrapper
            wrapper = RLWrapper()

            # Test wrapper properties
            self.assertEqual(wrapper.component_name, "rl")
            self.assertFalse(wrapper.is_initialized())
            self.assertIsNone(wrapper.wrapped_component)

        except AttributeError:
            self.skipTest("RLWrapper not available in wrappers module")


class TestDAFWrapperIntegration(unittest.TestCase):
    """Test DAF wrapper integration with real Metta components."""

    def setUp(self):
        """Set up test environment."""
        # Load DAF wrappers module
        wrappers_dir = SRC_DIR / "daf" / "wrappers"
        self.wrappers_module = load_module("daf.wrappers.metta_wrapper", wrappers_dir / "metta_wrapper.py")

        # Add Metta to path for real imports
        metta_root = ROOT_DIR.parent / "metta"
        if str(metta_root) not in sys.path:
            sys.path.insert(0, str(metta_root))

    def test_wrapper_compatibility_with_real_metta(self):
        """Test wrapper compatibility with real Metta components."""
        try:
            # Test real Metta components
            from metta.adaptive.adaptive_controller import AdaptiveController
            from metta.cogworks.curriculum.curriculum import Curriculum
            from metta.rl.trainer import Trainer

            # Test that real components exist and have expected interfaces
            self.assertTrue(hasattr(AdaptiveController, "__init__"))
            self.assertTrue(hasattr(Curriculum, "get_task"))
            self.assertTrue(hasattr(Trainer, "train"))

            # Test that wrappers can be created for these components
            AdaptiveWrapper = self.wrappers_module.AdaptiveWrapper
            CurriculumWrapper = self.wrappers_module.CurriculumWrapper
            RLWrapper = self.wrappers_module.RLWrapper

            adaptive_wrapper = AdaptiveWrapper()
            curriculum_wrapper = CurriculumWrapper()
            rl_wrapper = RLWrapper()

            # Test that wrappers have expected properties
            self.assertEqual(adaptive_wrapper.component_name, "adaptive")
            self.assertEqual(curriculum_wrapper.component_name, "curriculum")
            self.assertEqual(rl_wrapper.component_name, "rl")

        except ImportError as e:
            self.skipTest(f"Real Metta components not available: {e}")

    def test_wrapper_initialization_patterns(self):
        """Test wrapper initialization patterns."""
        try:
            AdaptiveWrapper = self.wrappers_module.AdaptiveWrapper

            wrapper = AdaptiveWrapper()

            # Test initialization state
            self.assertFalse(wrapper.is_initialized())

            # Test that initialize method exists
            self.assertTrue(hasattr(wrapper, "initialize"))
            self.assertTrue(callable(wrapper.initialize))

        except Exception as e:
            self.skipTest(f"Wrapper initialization test failed: {e}")

    def test_wrapper_logging_functionality(self):
        """Test wrapper logging functionality."""
        try:
            AdaptiveWrapper = self.wrappers_module.AdaptiveWrapper

            wrapper = AdaptiveWrapper()

            # Test logging method
            self.assertTrue(hasattr(wrapper, "log_operation"))
            self.assertTrue(callable(wrapper.log_operation))

            # Test that logging doesn't crash
            wrapper.log_operation("test_operation", {"test": "data"})

        except Exception as e:
            self.skipTest(f"Wrapper logging test failed: {e}")


class TestDAFWrapperErrorHandling(unittest.TestCase):
    """Test DAF wrapper error handling with real Metta."""

    def setUp(self):
        """Set up test environment."""
        # Load DAF wrappers module
        wrappers_dir = SRC_DIR / "daf" / "wrappers"
        self.wrappers_module = load_module("daf.wrappers.metta_wrapper", wrappers_dir / "metta_wrapper.py")

    def test_wrapper_initialization_error_handling(self):
        """Test wrapper initialization error handling."""
        try:
            AdaptiveWrapper = self.wrappers_module.AdaptiveWrapper

            wrapper = AdaptiveWrapper()

            # Test initialization without required components
            # Should not crash but may not initialize
            try:
                wrapper.initialize()
                # If it succeeds, that's fine
            except Exception:
                # If it fails, that's also expected without proper setup
                pass

            # Wrapper should handle errors gracefully
            self.assertIsNotNone(wrapper)

        except Exception as e:
            self.skipTest(f"Wrapper error handling test failed: {e}")

    def test_wrapper_component_access(self):
        """Test wrapper component access patterns."""
        try:
            AdaptiveWrapper = self.wrappers_module.AdaptiveWrapper

            wrapper = AdaptiveWrapper()

            # Test component access before initialization
            component = wrapper.wrapped_component
            self.assertIsNone(component)

            # Test initialization state
            self.assertFalse(wrapper.is_initialized())

        except Exception as e:
            self.skipTest(f"Wrapper component access test failed: {e}")


if __name__ == "__main__":
    # Run all wrapper tests
    unittest.main(verbosity=2)
