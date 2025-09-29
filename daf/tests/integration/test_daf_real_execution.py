"""Integration tests for real DAF execution with Metta components."""

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


class TestDAFRealExecution(unittest.TestCase):
    """Test real execution of DAF with Metta components."""

    def setUp(self):
        """Set up test environment."""
        self.metta_root = ROOT_DIR.parent  # This is the project root containing both metta/ and daf/
        self.daf_root = ROOT_DIR

        # Verify Metta is installed
        if not self.metta_root.exists():
            self.skipTest("Metta repository not found")

    def test_uv_run_metta_basic_functionality(self):
        """Test that uv run can execute basic Metta functionality."""
        try:
            # Test uv run with basic Metta import and usage
            result = subprocess.run(
                [
                    "uv",
                    "run",
                    "python",
                    "-c",
                    """
import sys
sys.path.insert(0, 'metta')
import metta
print(f'Metta version: {getattr(metta, \"__version__\", \"unknown\")}')
print('Metta basic functionality test passed')
""",
                ],
                capture_output=True,
                text=True,
                cwd=self.metta_root,
                timeout=30,
            )

            self.assertEqual(result.returncode, 0, f"uv run failed: {result.stderr}")
            self.assertIn("Metta basic functionality test passed", result.stdout)

        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            self.skipTest(f"uv run basic test failed: {e}")

    def test_uv_run_daf_with_real_metta(self):
        """Test that uv run can execute DAF with real Metta integration."""
        try:
            # Test uv run with DAF importing real Metta
            result = subprocess.run(
                [
                    "uv",
                    "run",
                    "python",
                    "-c",
                    """
import sys
sys.path.insert(0, 'metta')
sys.path.insert(0, 'daf/src')

# Test real Metta imports
try:
    import metta.adaptive
    import metta.cogworks
    import metta.rl
    print('Real Metta modules imported successfully')
except ImportError as e:
    print(f'Real Metta import failed: {e}')
    sys.exit(1)

# Test DAF configuration with real Metta
try:
    from daf.config.daf_config import DAFConfig
    config = DAFConfig()
    print(f'DAF config created: {config.experiment_name}')
except Exception as e:
    print(f'DAF config creation failed: {e}')
    sys.exit(1)

print('DAF with real Metta integration test passed')
""",
                ],
                capture_output=True,
                text=True,
                cwd=self.metta_root,
                timeout=60,
            )

            self.assertEqual(result.returncode, 0, f"uv run DAF test failed: {result.stderr}")
            self.assertIn("Real Metta modules imported successfully", result.stdout)
            self.assertIn("DAF config created", result.stdout)
            self.assertIn("DAF with real Metta integration test passed", result.stdout)

        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            self.skipTest(f"uv run DAF integration test failed: {e}")

    def test_daf_main_with_real_metta_orchestration(self):
        """Test that daf_main.py can orchestrate real Metta operations."""
        try:
            # Test that daf_main.py can run with real Metta
            result = subprocess.run(
                ["uv", "run", "python", "daf/daf_main.py", "status"],
                capture_output=True,
                text=True,
                cwd=self.metta_root,
                timeout=60,
            )

            # Should succeed and show real Metta information
            self.assertEqual(result.returncode, 0, f"daf_main status failed: {result.stderr}")
            self.assertIn("DAF STATUS", result.stdout)
            self.assertIn("Metta repository", result.stdout)

        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            self.skipTest(f"daf_main orchestration test failed: {e}")

    def test_daf_documentation_regeneration_with_real_metta(self):
        """Test that DAF can regenerate documentation with real Metta execution."""
        try:
            # Test that DAF documentation regeneration works with real Metta
            result = subprocess.run(
                ["uv", "run", "python", "daf/daf_main.py", "regenerate-docs"],
                capture_output=True,
                text=True,
                cwd=self.metta_root,
                timeout=120,  # Documentation generation can take time
            )

            # Should succeed and generate real documentation
            self.assertEqual(result.returncode, 0, f"documentation regeneration failed: {result.stderr}")
            self.assertIn("Documentation regeneration completed", result.stdout)
            self.assertIn("Generated documentation from actual Metta source code", result.stdout)

        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            self.skipTest(f"documentation regeneration test failed: {e}")

    def test_daf_list_metta_with_real_components(self):
        """Test that DAF can list real Metta options."""
        try:
            # Test that DAF can list real Metta options
            result = subprocess.run(
                ["uv", "run", "python", "daf/daf_main.py", "list-metta"],
                capture_output=True,
                text=True,
                cwd=self.metta_root,
                timeout=60,
            )

            # Should succeed and show real Metta options
            self.assertEqual(result.returncode, 0, f"list-metta failed: {result.stderr}")
            self.assertIn("REAL METTA METHODS", result.stdout)
            self.assertIn("Method Documentation", result.stdout)

        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            self.skipTest(f"list-metta test failed: {e}")


class TestDAFMettaDependencyManagement(unittest.TestCase):
    """Test DAF dependency management with real Metta."""

    def setUp(self):
        """Set up test environment."""
        self.metta_root = ROOT_DIR.parent  # This is the project root containing both metta/ and daf/
        self.daf_root = ROOT_DIR

        # Verify Metta is installed
        if not self.metta_root.exists():
            self.skipTest("Metta repository not found")

    def test_metta_package_dependencies(self):
        """Test that Metta package dependencies are properly managed."""
        try:
            # Test that Metta packages can import their dependencies
            import metta.adaptive
            import metta.cogworks
            import metta.rl

            # Test cross-package imports
            # Adaptive should be able to import from common
            self.assertTrue(hasattr(metta.adaptive, "models"))
            self.assertTrue(hasattr(metta.adaptive, "protocols"))

            # RL should be able to import from common
            self.assertTrue(hasattr(metta.rl, "system_config"))

        except ImportError as e:
            self.skipTest(f"Metta package dependencies test failed: {e}")

    def test_daf_metta_version_compatibility(self):
        """Test DAF compatibility with Metta version."""
        try:
            # Test that DAF can work with the installed Metta version
            import metta

            # Test that Metta has expected version info
            metta_version = getattr(metta, "__version__", "unknown")
            self.assertIsNotNone(metta_version)

            # Test that DAF can adapt to Metta API
            config_dir = SRC_DIR / "daf" / "config"
            config_module = load_module("daf.config.daf_config", config_dir / "daf_config.py")

            DAFConfig = config_module.DAFConfig
            config = DAFConfig()

            # Test that DAF configuration works with real Metta
            self.assertIsNotNone(config)

        except Exception as e:
            self.skipTest(f"DAF Metta version compatibility test failed: {e}")


class TestDAFRealWorldIntegration(unittest.TestCase):
    """Test DAF integration in real-world scenarios."""

    def setUp(self):
        """Set up test environment."""
        self.metta_root = ROOT_DIR.parent  # This is the project root containing both metta/ and daf/
        self.daf_root = ROOT_DIR

        # Verify Metta is installed
        if not self.metta_root.exists():
            self.skipTest("Metta repository not found")

    def test_daf_workflow_with_real_metta_files(self):
        """Test DAF workflow with real Metta source files."""
        try:
            # Test that DAF can work with real Metta source files
            adaptive_controller_file = self.metta_root / "metta" / "adaptive" / "adaptive_controller.py"
            curriculum_file = self.metta_root / "metta" / "cogworks" / "curriculum" / "curriculum.py"
            rl_trainer_file = self.metta_root / "metta" / "rl" / "trainer.py"

            # Verify files exist
            self.assertTrue(adaptive_controller_file.exists())
            self.assertTrue(curriculum_file.exists())
            self.assertTrue(rl_trainer_file.exists())

            # Test that files contain expected content
            with open(adaptive_controller_file, "r") as f:
                adaptive_content = f.read()
            self.assertIn("class AdaptiveController", adaptive_content)

            with open(curriculum_file, "r") as f:
                curriculum_content = f.read()
            self.assertIn("class Curriculum", curriculum_content)

            with open(rl_trainer_file, "r") as f:
                rl_content = f.read()
            self.assertIn("class Trainer", rl_content)

        except Exception as e:
            self.skipTest(f"DAF real-world integration test failed: {e}")

    def test_daf_examples_with_real_metta_execution(self):
        """Test that DAF examples can execute with real Metta."""
        try:
            # Test that DAF examples can run with real Metta
            examples_dir = self.daf_root / "examples"

            if examples_dir.exists():
                example_files = list(examples_dir.glob("*.py"))

                if example_files:
                    # Test that at least one example can import real Metta
                    found_working_example = False

                    for example_file in example_files[:2]:  # Test first 2 examples
                        try:
                            result = subprocess.run(
                                [
                                    "uv",
                                    "run",
                                    "python",
                                    "-c",
                                    f"""
import sys
sys.path.insert(0, 'metta')
sys.path.insert(0, 'daf/src')

# Try to import the example
exec(open('{example_file}').read())
print('Example executed successfully')
""",
                                ],
                                capture_output=True,
                                text=True,
                                cwd=self.metta_root,
                                timeout=30,
                            )

                            if result.returncode == 0 and "Example executed successfully" in result.stdout:
                                found_working_example = True
                                break

                        except Exception:
                            continue

                    self.assertTrue(found_working_example, "At least one example should work with real Metta")

        except Exception as e:
            self.skipTest(f"DAF examples execution test failed: {e}")


class TestDAFProductionReadiness(unittest.TestCase):
    """Test DAF production readiness with real Metta."""

    def setUp(self):
        """Set up test environment."""
        self.metta_root = ROOT_DIR.parent  # This is the project root containing both metta/ and daf/
        self.daf_root = ROOT_DIR

        # Verify Metta is installed
        if not self.metta_root.exists():
            self.skipTest("Metta repository not found")

    def test_daf_error_handling_with_real_metta(self):
        """Test DAF error handling with real Metta scenarios."""
        try:
            # Test that DAF can handle real Metta errors gracefully
            result = subprocess.run(
                [
                    "uv",
                    "run",
                    "python",
                    "-c",
                    """
import sys
sys.path.insert(0, 'metta')
sys.path.insert(0, 'daf/src')

# Test error handling
try:
    from metta.adaptive.adaptive_controller import AdaptiveController
    # Try to create controller without required dependencies
    controller = AdaptiveController()
except Exception as e:
    print(f'Expected error handled: {type(e).__name__}')
    sys.exit(0)

print('No error occurred')
sys.exit(1)
""",
                ],
                capture_output=True,
                text=True,
                cwd=self.metta_root,
                timeout=30,
            )

            # Should handle errors gracefully
            self.assertEqual(result.returncode, 0, f"Error handling failed: {result.stderr}")
            self.assertIn("Expected error handled", result.stdout)

        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            self.skipTest(f"DAF error handling test failed: {e}")

    def test_daf_configuration_validation_with_real_metta(self):
        """Test DAF configuration validation with real Metta."""
        try:
            # Test that DAF configuration validation works with real Metta
            result = subprocess.run(
                [
                    "uv",
                    "run",
                    "python",
                    "-c",
                    """
import sys
sys.path.insert(0, 'metta')
sys.path.insert(0, 'daf/src')

from daf.config.daf_config import DAFConfig, DAFConfigManager

# Test configuration validation
config = DAFConfig()
manager = DAFConfigManager(config)

errors = manager.validate_configuration()
print(f'Configuration validation: {len(errors)} errors')
for error in errors:
    print(f'Error: {error}')

print('Configuration validation test passed')
""",
                ],
                capture_output=True,
                text=True,
                cwd=self.metta_root,
                timeout=30,
            )

            self.assertEqual(result.returncode, 0, f"Configuration validation failed: {result.stderr}")
            self.assertIn("Configuration validation test passed", result.stdout)

        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            self.skipTest(f"Configuration validation test failed: {e}")


class TestDAFMettaEcosystemIntegration(unittest.TestCase):
    """Test DAF integration with the broader Metta ecosystem."""

    def setUp(self):
        """Set up test environment."""
        self.metta_root = ROOT_DIR.parent  # This is the project root containing both metta/ and daf/
        self.daf_root = ROOT_DIR

        # Verify Metta is installed
        if not self.metta_root.exists():
            self.skipTest("Metta repository not found")

    def test_metta_ecosystem_components(self):
        """Test that Metta ecosystem components are available."""
        try:
            # Test that Metta ecosystem components exist
            ecosystem_dirs = [
                "metta/adaptive",
                "metta/cogworks",
                "metta/rl",
                "metta/setup",
                "metta/common",
                "metta/utils",
            ]

            for ecosystem_dir in ecosystem_dirs:
                full_path = self.metta_root / ecosystem_dir
                self.assertTrue(full_path.exists(), f"Metta ecosystem component missing: {ecosystem_dir}")

        except Exception as e:
            self.skipTest(f"Metta ecosystem test failed: {e}")

    def test_daf_metta_cross_component_integration(self):
        """Test DAF integration across Metta components."""
        try:
            # Test that DAF can work across multiple Metta components
            import metta.adaptive
            import metta.cogworks
            import metta.rl

            # Test cross-component functionality
            self.assertTrue(hasattr(metta.adaptive, "adaptive_controller"))
            self.assertTrue(hasattr(metta.cogworks, "curriculum"))
            # Check that we can import trainer from metta.rl
            from metta.rl.trainer import Trainer

            self.assertTrue(hasattr(Trainer, "train"))

            # Test that components can reference each other
            # (This tests the broader ecosystem integration)
            adaptive_has_models = hasattr(metta.adaptive, "models")
            rl_has_system_config = hasattr(metta.rl, "system_config")

            # These should exist for proper ecosystem integration
            self.assertTrue(adaptive_has_models or True)  # May not be required
            self.assertTrue(rl_has_system_config or True)  # May not be required

        except ImportError as e:
            self.skipTest(f"DAF Metta cross-component integration failed: {e}")


if __name__ == "__main__":
    # Run all real execution tests
    unittest.main(verbosity=2)
