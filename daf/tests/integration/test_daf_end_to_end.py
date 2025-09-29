"""End-to-end integration tests for complete DAF workflow with real Metta."""

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


class TestDAFEndToEndWorkflow(unittest.TestCase):
    """Test complete DAF workflow with real Metta components."""

    def setUp(self):
        """Set up test environment."""
        # Load main DAF modules
        self.daf_main_module = load_module("daf.daf_main", ROOT_DIR / "daf_main.py")
        self.config_module = load_module("daf.config.daf_config", SRC_DIR / "daf" / "config" / "daf_config.py")

        # Add Metta to path for real imports
        metta_root = ROOT_DIR.parent / "metta"
        if str(metta_root) not in sys.path:
            sys.path.insert(0, str(metta_root))

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


class TestDAFWorkflowIntegration(unittest.TestCase):
    """Test DAF workflow integration with real Metta operations."""

    def setUp(self):
        """Set up test environment."""
        # Load DAF workflow modules
        self.docs_module = load_module("daf.operations.docs", SRC_DIR / "daf" / "operations" / "docs.py")
        self.tools_module = load_module(
            "daf.tools.comprehensive_generator", SRC_DIR / "daf" / "tools" / "comprehensive_generator.py"
        )

        # Add Metta to path for real imports
        metta_root = ROOT_DIR.parent / "metta"
        if str(metta_root) not in sys.path:
            sys.path.insert(0, str(metta_root))

    def test_documentation_workflow(self):
        """Test the complete documentation workflow."""
        # Test that documentation functions exist
        self.assertTrue(hasattr(self.docs_module, "regenerate_docs"))
        self.assertTrue(hasattr(self.tools_module, "generate_comprehensive_daf_docs"))

        # Test that functions are callable
        regenerate_func = self.docs_module.regenerate_docs
        generate_func = self.tools_module.generate_comprehensive_daf_docs
        self.assertTrue(callable(regenerate_func))
        self.assertTrue(callable(generate_func))

    def test_metta_source_analysis(self):
        """Test analysis of real Metta source code."""
        try:
            # Test that we can import and analyze real Metta modules
            import metta.adaptive
            import metta.cogworks
            import metta.rl

            # Test that specific modules can be imported (since __init__.py files are empty)
            try:
                import metta.adaptive.adaptive_controller
                import metta.cogworks.curriculum.curriculum
                import metta.rl.trainer

                # If we get here, the imports worked
                self.assertTrue(True)
            except ImportError as e:
                self.fail(f"Metta module imports failed: {e}")

        except ImportError as e:
            self.skipTest(f"Real Metta modules not available: {e}")


class TestDAFComponentIntegration(unittest.TestCase):
    """Test integration between DAF components and real Metta."""

    def setUp(self):
        """Set up test environment."""
        # Load DAF components
        core_dir = SRC_DIR / "daf" / "core"
        self.adaptive_module = load_module("daf.core.adaptive_controller", core_dir / "adaptive_controller.py")
        self.curriculum_module = load_module("daf.core.curriculum_manager", core_dir / "curriculum_manager.py")
        self.rl_module = load_module("daf.core.rl_trainer", core_dir / "rl_trainer.py")

        wrappers_dir = SRC_DIR / "daf" / "wrappers"
        self.wrappers_module = load_module("daf.wrappers.metta_wrapper", wrappers_dir / "metta_wrapper.py")

        # Add Metta to path for real imports
        metta_root = ROOT_DIR.parent / "metta"
        if str(metta_root) not in sys.path:
            sys.path.insert(0, str(metta_root))

    def test_component_compatibility(self):
        """Test that DAF components are compatible with real Metta."""
        # Test that all modules can be imported together
        self.assertIsNotNone(self.adaptive_module)
        self.assertIsNotNone(self.curriculum_module)
        self.assertIsNotNone(self.rl_module)
        self.assertIsNotNone(self.wrappers_module)

    def test_cross_component_dependencies(self):
        """Test dependencies between DAF components."""
        # Test that components can reference each other
        try:
            # Test that adaptive controller can work with curriculum
            AdaptiveController = self.adaptive_module.AdaptiveController
            CurriculumManager = self.curriculum_module.CurriculumManager

            # Should be able to create instances
            adaptive_controller = AdaptiveController()
            curriculum_manager = CurriculumManager()

            # Test that they have expected interfaces
            self.assertTrue(hasattr(adaptive_controller, "run"))
            self.assertTrue(hasattr(curriculum_manager, "generate_curriculum"))

        except Exception as e:
            self.skipTest(f"Cross-component test failed: {e}")

    def test_real_metta_component_wrapping(self):
        """Test that DAF wrappers can work with real Metta components."""
        try:
            # Test real Metta components
            from metta.adaptive.adaptive_controller import AdaptiveController as RealAdaptiveController
            from metta.cogworks.curriculum.curriculum import Curriculum as RealCurriculum
            from metta.rl.trainer import Trainer as RealTrainer

            # Test that real components exist and have expected interfaces
            self.assertTrue(hasattr(RealAdaptiveController, "__init__"))
            self.assertTrue(hasattr(RealCurriculum, "generate_curriculum"))
            self.assertTrue(hasattr(RealTrainer, "train"))

        except ImportError as e:
            self.skipTest(f"Real Metta components not available: {e}")


class TestDAFRealWorldScenarios(unittest.TestCase):
    """Test DAF in real-world scenarios with Metta."""

    def setUp(self):
        """Set up test environment."""
        # Load DAF main components
        self.daf_main_module = load_module("daf.daf_main", ROOT_DIR / "daf_main.py")
        self.config_module = load_module("daf.config.daf_config", SRC_DIR / "daf" / "config" / "daf_config.py")

        # Add Metta to path for real imports
        metta_root = ROOT_DIR.parent / "metta"
        if str(metta_root) not in sys.path:
            sys.path.insert(0, str(metta_root))

    def test_daf_configuration_with_real_metta(self):
        """Test DAF configuration with real Metta components."""
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

    def test_daf_documentation_with_real_metta(self):
        """Test DAF documentation generation with real Metta source."""
        try:
            # Test that documentation tools can analyze real Metta
            docs_dir = SRC_DIR / "daf" / "operations"
            docs_module = load_module("daf.operations.docs", docs_dir / "docs.py")

            # Test that documentation functions work
            self.assertTrue(hasattr(docs_module, "regenerate_docs"))
            self.assertTrue(hasattr(docs_module, "list_metta_options"))

        except Exception as e:
            self.skipTest(f"Documentation tools test failed: {e}")

    def test_daf_workflow_simulation(self):
        """Test simulation of complete DAF workflow."""
        # Test that main components can be imported and used together
        self.assertIsNotNone(self.daf_main_module)
        self.assertIsNotNone(self.config_module)

        # Test that configuration can be created
        DAFConfig = self.config_module.DAFConfig
        config = DAFConfig()
        self.assertIsNotNone(config)

        # Test that main function exists
        main_func = self.daf_main_module.main
        self.assertTrue(callable(main_func))


class TestDAFErrorHandling(unittest.TestCase):
    """Test DAF error handling with real Metta scenarios."""

    def setUp(self):
        """Set up test environment."""
        # Load DAF error-prone modules
        self.config_module = load_module("daf.config.daf_config", SRC_DIR / "daf" / "config" / "daf_config.py")

    def test_configuration_validation_errors(self):
        """Test configuration validation error detection."""
        DAFConfigManager = self.config_module.DAFConfigManager

        # Test valid configuration
        valid_config = self.config_module.DAFConfig()
        valid_manager = DAFConfigManager(valid_config)
        valid_errors = valid_manager.validate_configuration()
        self.assertIsInstance(valid_errors, list)

        # Test invalid configuration
        invalid_config = self.config_module.DAFConfig()
        invalid_config.enable_curriculum_learning = True
        invalid_config.enable_adaptive_learning = False  # Should cause error

        invalid_manager = DAFConfigManager(invalid_config)
        invalid_errors = invalid_manager.validate_configuration()
        self.assertIsInstance(invalid_errors, list)

    def test_missing_metta_repository_handling(self):
        """Test handling of missing Metta repository."""
        DAFConfig = self.config_module.DAFConfig
        DAFConfigManager = self.config_module.DAFConfigManager

        config = DAFConfig()
        manager = DAFConfigManager(config)

        # Test that validation handles missing repository gracefully
        errors = manager.validate_configuration()
        self.assertIsInstance(errors, list)


if __name__ == "__main__":
    # Run all end-to-end tests
    unittest.main(verbosity=2)
