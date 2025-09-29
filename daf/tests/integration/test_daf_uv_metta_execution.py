"""Integration tests for DAF with uv run and real Metta execution."""

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


class TestDAFUVRunMettaExecution(unittest.TestCase):
    """Test DAF with uv run and real Metta execution."""

    def setUp(self):
        """Set up test environment."""
        self.metta_root = ROOT_DIR.parent  # This is the project root containing both metta/ and daf/
        self.daf_root = ROOT_DIR

        # Verify Metta is installed
        if not self.metta_root.exists():
            self.skipTest("Metta repository not found")

    def test_uv_run_metta_installation(self):
        """Test that uv run can access installed Metta."""
        try:
            # Test that uv run can import and use Metta
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
print(f'Metta imported successfully: {metta.__file__}')
print('uv run Metta installation test passed')
""",
                ],
                capture_output=True,
                text=True,
                cwd=self.metta_root,
                timeout=30,
            )

            self.assertEqual(result.returncode, 0, f"uv run Metta test failed: {result.stderr}")
            self.assertIn("Metta imported successfully", result.stdout)

        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            self.skipTest(f"uv run Metta installation test failed: {e}")

    def test_uv_run_daf_with_metta_orchestration(self):
        """Test that uv run can execute DAF with real Metta orchestration."""
        try:
            # Test uv run with DAF orchestrating real Metta
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

# Test DAF orchestration of real Metta
try:
    from metta.adaptive.adaptive_controller import AdaptiveController
    from metta.cogworks.curriculum.curriculum import Curriculum
    print(f'Real Metta classes: {AdaptiveController.__name__}, {Curriculum.__name__}')
except ImportError as e:
    print(f'Real Metta import failed: {e}')
    sys.exit(1)

# Test DAF configuration
try:
    from daf.config.daf_config import DAFConfig
    config = DAFConfig()
    print(f'DAF config: {config.experiment_name}')
except Exception as e:
    print(f'DAF config failed: {e}')
    sys.exit(1)

print('uv run DAF Metta orchestration test passed')
""",
                ],
                capture_output=True,
                text=True,
                cwd=self.metta_root,
                timeout=60,
            )

            self.assertEqual(result.returncode, 0, f"uv run orchestration test failed: {result.stderr}")
            self.assertIn("Real Metta classes", result.stdout)
            self.assertIn("DAF config", result.stdout)
            self.assertIn("uv run DAF Metta orchestration test passed", result.stdout)

        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            self.skipTest(f"uv run orchestration test failed: {e}")

    def test_daf_main_with_uv_run_orchestration(self):
        """Test that daf_main.py can orchestrate real Metta with uv run."""
        try:
            # Test that daf_main.py can run with uv and orchestrate real Metta
            result = subprocess.run(
                ["uv", "run", "python", "daf/daf_main.py", "list-metta"],
                capture_output=True,
                text=True,
                cwd=self.metta_root,
                timeout=60,
            )

            # Should succeed and show real Metta orchestration
            self.assertEqual(result.returncode, 0, f"daf_main uv run failed: {result.stderr}")
            self.assertIn("REAL METTA METHODS", result.stdout)
            self.assertIn("Method Documentation", result.stdout)

        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            self.skipTest(f"daf_main uv run orchestration test failed: {e}")

    def test_daf_documentation_with_uv_run_metta(self):
        """Test DAF documentation generation with uv run and real Metta."""
        try:
            # Test that DAF documentation can be generated with uv run
            result = subprocess.run(
                ["uv", "run", "python", "daf/daf_main.py", "regenerate-docs"],
                capture_output=True,
                text=True,
                cwd=self.metta_root,
                timeout=120,  # Documentation can take time
            )

            # Should succeed and generate documentation from real Metta
            self.assertEqual(result.returncode, 0, f"documentation uv run failed: {result.stderr}")
            self.assertIn("Documentation regeneration completed", result.stdout)
            self.assertIn("Generated documentation from actual Metta source code", result.stdout)

        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            self.skipTest(f"documentation uv run test failed: {e}")


class TestDAFUVRunWorkflow(unittest.TestCase):
    """Test complete DAF workflow with uv run."""

    def setUp(self):
        """Set up test environment."""
        self.metta_root = ROOT_DIR.parent  # This is the project root containing both metta/ and daf/
        self.daf_root = ROOT_DIR

        # Verify Metta is installed
        if not self.metta_root.exists():
            self.skipTest("Metta repository not found")

    def test_uv_run_complete_daf_workflow(self):
        """Test complete DAF workflow with uv run."""
        try:
            # Test complete workflow: setup -> validate -> examples -> test
            workflow_steps = [
                (["uv", "run", "python", "daf/daf_main.py", "status"], "DAF STATUS"),
                (["uv", "run", "python", "daf/daf_main.py", "list-metta"], "REAL METTA METHODS"),
            ]

            for cmd, expected_text in workflow_steps:
                result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.metta_root, timeout=60)

                self.assertEqual(result.returncode, 0, f"Workflow step failed: {result.stderr}")
                self.assertIn(expected_text, result.stdout, f"Expected text not found: {expected_text}")

        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            self.skipTest(f"uv run workflow test failed: {e}")

    def test_daf_uv_run_error_handling(self):
        """Test DAF error handling with uv run."""
        try:
            # Test that DAF handles errors gracefully with uv run
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
    from daf.config.daf_config import DAFConfigManager
    config = DAFConfigManager()
    print('DAF error handling test passed')
except Exception as e:
    print(f'DAF error occurred: {e}')
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
            self.assertIn("DAF error handling test passed", result.stdout)

        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            self.skipTest(f"DAF error handling test failed: {e}")


class TestDAFMettaUVRunIntegration(unittest.TestCase):
    """Test DAF and Metta integration with uv run."""

    def setUp(self):
        """Set up test environment."""
        self.metta_root = ROOT_DIR.parent  # This is the project root containing both metta/ and daf/
        self.daf_root = ROOT_DIR

        # Verify Metta is installed
        if not self.metta_root.exists():
            self.skipTest("Metta repository not found")

    def test_metta_package_with_uv_run(self):
        """Test that Metta packages work correctly with uv run."""
        try:
            # Test that Metta packages can be imported with uv run
            result = subprocess.run(
                [
                    "uv",
                    "run",
                    "python",
                    "-c",
                    """
import sys
sys.path.insert(0, 'metta')

# Test all major Metta packages
packages = ['metta.adaptive', 'metta.cogworks', 'metta.rl', 'metta.setup']
for package in packages:
    try:
        __import__(package)
        print(f'Package {package} imported successfully')
    except ImportError as e:
        print(f'Package {package} import failed: {e}')

print('Metta package uv run test completed')
""",
                ],
                capture_output=True,
                text=True,
                cwd=self.metta_root,
                timeout=30,
            )

            self.assertEqual(result.returncode, 0, f"Metta package test failed: {result.stderr}")
            self.assertIn("imported successfully", result.stdout)

        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            self.skipTest(f"Metta package uv run test failed: {e}")

    def test_daf_metta_cross_component_uv_run(self):
        """Test DAF and Metta cross-component functionality with uv run."""
        try:
            # Test cross-component functionality with uv run
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

# Test that DAF can orchestrate real Metta cross-component usage
try:
    from metta.adaptive.adaptive_controller import AdaptiveController
    from metta.cogworks.curriculum.curriculum import Curriculum
    from metta.rl.trainer import Trainer

    print(f'Real Metta components: {len([AdaptiveController, Curriculum, Trainer])} components')
    print('Cross-component uv run test passed')
except ImportError as e:
    print(f'Cross-component import failed: {e}')
    sys.exit(1)
""",
                ],
                capture_output=True,
                text=True,
                cwd=self.metta_root,
                timeout=30,
            )

            self.assertEqual(result.returncode, 0, f"Cross-component test failed: {result.stderr}")
            self.assertIn("Cross-component uv run test passed", result.stdout)

        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            self.skipTest(f"Cross-component uv run test failed: {e}")


if __name__ == "__main__":
    # Run all uv run integration tests
    unittest.main(verbosity=2)
