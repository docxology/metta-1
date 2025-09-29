"""Unit tests for DAF operational helpers."""

from __future__ import annotations

import json
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import MagicMock

CURRENT_DIR = Path(__file__).resolve()
ROOT_DIR = CURRENT_DIR.parents[2]
SRC_DIR = ROOT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

if "daf" not in sys.modules:
    daf_pkg = types.ModuleType("daf")
    daf_pkg.__path__ = [str(SRC_DIR / "daf")]
    sys.modules["daf"] = daf_pkg

import contextlib
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
validation_module = load_module("daf.validation.real_usage", SRC_DIR / "daf" / "validation" / "real_usage.py")

ExampleResult = examples_module.ExampleResult
run_examples = examples_module.run_examples
discover_examples = examples_module.discover_examples
run_tests_helper = tests_module.run_tests
validate_real_usage_fn = validation_module.validate_real_usage
ValidationResults = validation_module.ValidationResults


class DiscoverExamplesTests(unittest.TestCase):
    """Tests for example discovery helper."""

    def test_discovers_only_runnable_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            (tmp_path / "alpha.py").write_text("print('alpha')\n", encoding="utf-8")
            (tmp_path / "__init__.py").write_text("", encoding="utf-8")
            (tmp_path / "conftest.py").write_text("", encoding="utf-8")
            (tmp_path / "_hidden.py").write_text("", encoding="utf-8")
            (tmp_path / "beta.py").write_text("print('beta')\n", encoding="utf-8")

            discovered = list(discover_examples(tmp_path))

        self.assertEqual([p.name for p in discovered], ["alpha.py", "beta.py"])


class RunExamplesTests(unittest.TestCase):
    """Tests for running examples via uv."""

    def test_run_examples_records_success(self):
        run_mock = subprocess_completed("stdout", "", 0)

        def mock_run(*args, **kwargs):
            return run_mock

        with (
            patch_module(examples_module.subprocess, "run", mock_run),
            patch_module(examples_module.time, "perf_counter", lambda: 0.5),
        ):
            with tempfile.TemporaryDirectory() as tmp_dir:
                examples_dir = Path(tmp_dir) / "examples"
                examples_dir.mkdir()
                (examples_dir / "demo.py").write_text("print('demo')\n", encoding="utf-8")
                output_dir = Path(tmp_dir) / "out"

                results = run_examples(examples_dir, output_dir=output_dir)

                self.assertEqual(len(results), 1)
                result = results[0]
                self.assertTrue(result.success)
                self.assertTrue(result.output_file.is_file())
                output_payload = json.loads(result.output_file.read_text(encoding="utf-8"))
                self.assertEqual(output_payload["returncode"], 0)
                self.assertEqual(output_payload["stdout"], "stdout")

    def test_run_examples_records_failure(self):
        fail_mock = subprocess_completed("", "boom", 1)

        def mock_run(*args, **kwargs):
            return fail_mock

        with (
            patch_module(examples_module.subprocess, "run", mock_run),
            patch_module(examples_module.time, "perf_counter", lambda: 1.0),
        ):
            with tempfile.TemporaryDirectory() as tmp_dir:
                examples_dir = Path(tmp_dir) / "examples"
                examples_dir.mkdir()
                (examples_dir / "fail.py").write_text("print('fail')\n", encoding="utf-8")
                output_dir = Path(tmp_dir) / "out"

                results = run_examples(examples_dir, output_dir=output_dir)

                result = results[0]
                self.assertFalse(result.success)
                payload = json.loads(result.output_file.read_text(encoding="utf-8"))
                self.assertEqual(payload["returncode"], 1)
                self.assertEqual(payload["stderr"], "boom")

    def test_run_examples_missing_directory(self) -> None:
        with self.assertRaises(FileNotFoundError):
            run_examples(Path("/non/existent/path"))


class RunTestsHelperTests(unittest.TestCase):
    """Tests for test orchestration helper."""

    def test_run_tests_invokes_unittest_discover(self):
        def mock_run(*args, **kwargs):
            return subprocess_completed("", "", 0)

        with patch_module(tests_module.subprocess, "run", mock_run):
            exit_code = run_tests_helper()

        self.assertEqual(exit_code, 0)

    def test_run_tests_propagates_return_code(self):
        def mock_run(*args, **kwargs):
            return subprocess_completed("", "", 5)

        with patch_module(tests_module.subprocess, "run", mock_run):
            self.assertEqual(run_tests_helper(), 5)


class ValidationTests(unittest.TestCase):
    """Tests for validation orchestration."""

    def test_validation_success(self):
        with (
            patch_module(validation_module, "run_examples", lambda *_: True),
            patch_module(validation_module, "run_tests", lambda *_: True),
        ):
            results = validate_real_usage_fn()

        self.assertTrue(results.overall_success)

    def test_validation_failure_details(self):
        with (
            patch_module(validation_module, "run_examples", lambda *_: True),
            patch_module(validation_module, "run_tests", lambda *_: False),
        ):
            results = validate_real_usage_fn()

        self.assertFalse(results.overall_success)


def subprocess_completed(stdout: str, stderr: str, returncode: int) -> MagicMock:
    """Helper to build a CompletedProcess-like object."""

    completed = MagicMock()
    completed.stdout = stdout
    completed.stderr = stderr
    completed.returncode = returncode
    return completed


def run_examples_with_mock(run_result: MagicMock, duration: float):
    def mock_run(*args, **kwargs):
        return run_result

    def mock_perf_counter():
        return duration

    return mock_run, mock_perf_counter


@contextlib.contextmanager
def patch_module(obj, attribute, value):
    original = getattr(obj, attribute)
    setattr(obj, attribute, value)
    try:
        yield
    finally:
        setattr(obj, attribute, original)


if __name__ == "__main__":
    unittest.main()
