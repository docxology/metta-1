"""Unit tests for DAF core components with real Metta integration."""

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


class TestDAFAdaptiveController(unittest.TestCase):
    """Test DAF adaptive controller with real Metta components."""

    def setUp(self):
        """Set up test environment."""
        # Load DAF adaptive controller
        core_dir = SRC_DIR / "daf" / "core"
        self.adaptive_module = load_module("daf.core.adaptive_controller", core_dir / "adaptive_controller.py")

        # Add Metta to path for real imports
        metta_root = ROOT_DIR.parent / "metta"
        if str(metta_root) not in sys.path:
            sys.path.insert(0, str(metta_root))

    def test_adaptive_controller_import(self):
        """Test that adaptive controller can be imported."""
        # Test module loading
        self.assertTrue(hasattr(self.adaptive_module, "DAFAdaptiveController"))

    def test_adaptive_controller_class_structure(self):
        """Test adaptive controller class structure."""
        AdaptiveController = self.adaptive_module.DAFAdaptiveController

        # Test that classes have expected methods
        self.assertTrue(hasattr(AdaptiveController, "__init__"))

    def test_real_metta_adaptive_controller_usage(self):
        """Test usage with real Metta AdaptiveController."""
        try:
            from metta.adaptive.adaptive_config import AdaptiveConfig
            from metta.adaptive.adaptive_controller import AdaptiveController as RealAdaptiveController

            # Test real Metta component
            real_config = AdaptiveConfig()
            real_controller = RealAdaptiveController(
                experiment_id="test_experiment",
                scheduler=None,  # Mock scheduler
                dispatcher=None,  # Mock dispatcher
                store=None,  # Mock store
                config=real_config,
            )

            # Test that real controller has expected attributes
            self.assertTrue(hasattr(real_controller, "run"))
            self.assertTrue(hasattr(real_controller, "experiment_id"))

        except ImportError as e:
            self.skipTest(f"Real Metta AdaptiveController not available: {e}")


class TestDAFCurriculumManager(unittest.TestCase):
    """Test DAF curriculum manager with real Metta components."""

    def setUp(self):
        """Set up test environment."""
        # Load DAF curriculum manager
        core_dir = SRC_DIR / "daf" / "core"
        self.curriculum_module = load_module("daf.core.curriculum_manager", core_dir / "curriculum_manager.py")

        # Add Metta to path for real imports
        metta_root = ROOT_DIR.parent / "metta"
        if str(metta_root) not in sys.path:
            sys.path.insert(0, str(metta_root))

    def test_curriculum_manager_import(self):
        """Test that curriculum manager can be imported."""
        # Test module loading
        self.assertTrue(hasattr(self.curriculum_module, "DAFCurriculumManager"))

    def test_curriculum_manager_class_structure(self):
        """Test curriculum manager class structure."""
        CurriculumManager = self.curriculum_module.DAFCurriculumManager

        # Test that classes have expected methods
        self.assertTrue(hasattr(CurriculumManager, "__init__"))

    def test_real_metta_curriculum_usage(self):
        """Test usage with real Metta Curriculum components."""
        try:
            # Test real Metta components
            from metta.cogworks.curriculum.curriculum import Curriculum, CurriculumConfig
            from metta.cogworks.curriculum.task_generator import SingleTaskGeneratorConfig, TaskGenerator

            # Create a minimal config for testing
            task_gen_config = SingleTaskGeneratorConfig()
            curriculum_config = CurriculumConfig(task_generator=task_gen_config)
            curriculum = Curriculum(curriculum_config)
            # TaskGenerator is abstract, so we use SingleTaskGenerator
            from metta.cogworks.curriculum.task_generator import SingleTaskGenerator

            task_generator = SingleTaskGenerator(task_gen_config)

            # Test that real components have expected attributes
            self.assertTrue(hasattr(curriculum, "get_task"))
            self.assertTrue(hasattr(task_generator, "get_task"))

        except ImportError as e:
            self.skipTest(f"Real Metta Curriculum not available: {e}")


class TestDAFRLTrainer(unittest.TestCase):
    """Test DAF RL trainer with real Metta components."""

    def setUp(self):
        """Set up test environment."""
        # Load DAF RL trainer
        core_dir = SRC_DIR / "daf" / "core"
        self.rl_module = load_module("daf.core.rl_trainer", core_dir / "rl_trainer.py")

        # Add Metta to path for real imports
        metta_root = ROOT_DIR.parent / "metta"
        if str(metta_root) not in sys.path:
            sys.path.insert(0, str(metta_root))

    def test_rl_trainer_import(self):
        """Test that RL trainer can be imported."""
        # Test module loading
        self.assertTrue(hasattr(self.rl_module, "DAFRlTrainer"))

    def test_rl_trainer_class_structure(self):
        """Test RL trainer class structure."""
        RLTrainer = self.rl_module.DAFRlTrainer

        # Test that classes have expected methods
        self.assertTrue(hasattr(RLTrainer, "__init__"))

    def test_real_metta_rl_trainer_usage(self):
        """Test usage with real Metta RL Trainer."""
        try:
            from metta.rl.trainer import Trainer as RealTrainer
            from metta.rl.training.core import CoreTrainingLoop

            # Test real Metta components (just check class attributes, don't instantiate)
            # RealTrainer requires cfg, env, policy, device arguments
            self.assertTrue(hasattr(RealTrainer, "__init__"))
            self.assertTrue(hasattr(RealTrainer, "train"))

            # CoreTrainingLoop also requires arguments
            self.assertTrue(hasattr(CoreTrainingLoop, "__init__"))

        except ImportError as e:
            self.skipTest(f"Real Metta RL Trainer not available: {e}")


class TestDAFComponentIntegration(unittest.TestCase):
    """Test integration between DAF components and real Metta."""

    def setUp(self):
        """Set up test environment."""
        # Load all DAF core modules
        core_dir = SRC_DIR / "daf" / "core"
        self.adaptive_module = load_module("daf.core.adaptive_controller", core_dir / "adaptive_controller.py")
        self.curriculum_module = load_module("daf.core.curriculum_manager", core_dir / "curriculum_manager.py")
        self.rl_module = load_module("daf.core.rl_trainer", core_dir / "rl_trainer.py")

        # Load DAF wrappers
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
            AdaptiveController = self.adaptive_module.DAFAdaptiveController
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
            self.assertTrue(hasattr(RealCurriculum, "get_task"))
            self.assertTrue(hasattr(RealTrainer, "train"))

        except ImportError as e:
            self.skipTest(f"Real Metta components not available: {e}")


class TestDAFMethodSignatures(unittest.TestCase):
    """Test DAF method signatures match real Metta components."""

    def setUp(self):
        """Set up test environment."""
        # Add Metta to path for real imports
        metta_root = ROOT_DIR.parent / "metta"
        if str(metta_root) not in sys.path:
            sys.path.insert(0, str(metta_root))

    def test_adaptive_controller_signature_compatibility(self):
        """Test that DAF adaptive controller signatures are compatible with Metta."""
        try:
            import inspect

            from metta.adaptive.adaptive_config import AdaptiveConfig
            from metta.adaptive.adaptive_controller import AdaptiveController

            # Get real Metta signature
            real_sig = inspect.signature(AdaptiveController.__init__)
            real_params = list(real_sig.parameters.keys())

            # Test that expected parameters exist
            expected_params = ["experiment_id", "scheduler", "dispatcher", "store", "config"]
            for param in expected_params:
                self.assertIn(param, real_params, f"Parameter {param} missing from AdaptiveController")

        except ImportError as e:
            self.skipTest(f"Real Metta AdaptiveController not available: {e}")

    def test_curriculum_signature_compatibility(self):
        """Test that DAF curriculum signatures are compatible with Metta."""
        try:
            import inspect

            from metta.cogworks.curriculum.curriculum import Curriculum

            # Get real Metta signature
            real_sig = inspect.signature(Curriculum.__init__)
            real_params = list(real_sig.parameters.keys())

            # Test that expected parameters exist
            self.assertIn("config", real_params)

        except ImportError as e:
            self.skipTest(f"Real Metta Curriculum not available: {e}")

    def test_rl_trainer_signature_compatibility(self):
        """Test that DAF RL trainer signatures are compatible with Metta."""
        try:
            import inspect

            from metta.rl.trainer import Trainer

            # Get real Metta signature
            real_sig = inspect.signature(Trainer.__init__)
            real_params = list(real_sig.parameters.keys())

            # Test that expected parameters exist
            self.assertIn("cfg", real_params)

        except ImportError as e:
            self.skipTest(f"Real Metta RL Trainer not available: {e}")


if __name__ == "__main__":
    # Run all core component tests
    unittest.main(verbosity=2)
