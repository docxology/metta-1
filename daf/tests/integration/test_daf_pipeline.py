"""Integration smoke tests for DAF operational pipeline."""

from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

CURRENT_DIR = Path(__file__).resolve()
ROOT_DIR = CURRENT_DIR.parents[2]
METTA_ROOT = ROOT_DIR.parent
SRC_DIR = ROOT_DIR / "src"
OPERATIONS_DIR = SRC_DIR / "daf" / "operations"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
if str(METTA_ROOT) not in sys.path:
    sys.path.insert(0, str(METTA_ROOT))
if str(OPERATIONS_DIR.parent.parent) not in sys.path:
    sys.path.insert(0, str(OPERATIONS_DIR.parent.parent))

import importlib.util


def load_module(module_name: str, file_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    if "." in module_name:
        module.__package__ = module_name.rpartition(".")[0]
    sys.modules[module_name] = module
    if spec.loader is None:  # pragma: no cover
        raise ImportError(f"Cannot load module {module_name}")
    spec.loader.exec_module(module)
    return module


operations_dir = SRC_DIR / "daf" / "operations"
examples_module = load_module("daf.operations.examples", operations_dir / "examples.py")
tests_module = load_module("daf.operations.tests", operations_dir / "tests.py")

# Load real_usage first to avoid import error in validation.py
real_usage_module = load_module("daf.validation.real_usage", SRC_DIR / "daf" / "validation" / "real_usage.py")

validation_module = load_module("daf.operations.validation", operations_dir / "validation.py")

run_examples = examples_module.run_examples
run_tests_helper = tests_module.run_tests
run_validation = validation_module.run_validation


class PipelineSmokeTests(unittest.TestCase):
    """End-to-end pipeline tests using patched subprocess execution."""

    @patch.object(examples_module.subprocess, "run")
    def test_examples_pipeline_records_outputs(self, mock_run):
        mock_run.return_value = subprocess_completed("ok", "", 0)

        with tempfile.TemporaryDirectory() as tmp_dir:
            examples_dir = Path(tmp_dir) / "examples"
            examples_dir.mkdir()
            (examples_dir / "demo.py").write_text("print('demo')\n", encoding="utf-8")
            output_dir = Path(tmp_dir) / "outputs"
            results = run_examples(examples_dir, output_dir=output_dir)

            self.assertEqual(len(results), 1)
            payload_path = results[0].output_file
            self.assertTrue(payload_path.is_file())
            payload = json.loads(payload_path.read_text(encoding="utf-8"))
            self.assertEqual(payload["stdout"], "ok")

    @patch.object(tests_module.subprocess, "run")
    def test_test_runner_failure_is_detected(self, mock_run):
        mock_run.return_value = subprocess_completed("", "boom", 2)
        self.assertEqual(run_tests_helper(), 2)

    @patch.object(real_usage_module, "run_examples", return_value=True)
    @patch.object(real_usage_module, "run_tests", return_value=True)
    def test_validation_succeeds_when_examples_and_tests_pass(self, mock_tests, mock_examples):
        result = run_validation()
        self.assertTrue(result)


def subprocess_completed(stdout: str, stderr: str, returncode: int) -> MagicMock:
    completed = MagicMock()
    completed.stdout = stdout
    completed.stderr = stderr
    completed.returncode = returncode
    return completed


if __name__ == "__main__":
    unittest.main()
