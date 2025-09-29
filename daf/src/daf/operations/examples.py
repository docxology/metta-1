"""Example execution orchestrators for DAF.

This module centralises the logic required to discover, execute, and report on
DAF example scripts. It wraps the functionality that previously lived in the
top-level ``run_metta_examples.py`` and ``run_examples_daf.py`` scripts so
those wrappers can simply call ``run_examples`` while keeping logic here, under
version control with the rest of ``src/daf``.
"""

from __future__ import annotations

import json
import logging
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional

LOGGER = logging.getLogger(__name__)


@dataclass(slots=True)
class ExampleResult:
    """Structured record for an executed example."""

    script: Path
    returncode: int
    duration: float
    stdout: str = ""
    stderr: str = ""
    output_file: Optional[Path] = None

    @property
    def success(self) -> bool:
        return self.returncode == 0


def discover_examples(examples_dir: Path) -> Iterable[Path]:
    """Yield runnable example scripts."""

    for candidate in sorted(examples_dir.glob("*.py")):
        if candidate.name in {"__init__.py", "conftest.py"} or candidate.stem.startswith("_"):
            continue
        yield candidate


def run_examples(examples_dir: Path, output_dir: Optional[Path] = None) -> List[ExampleResult]:
    """Execute each example via ``uv`` and collect results."""

    if not examples_dir.exists():
        raise FileNotFoundError(f"Examples directory not found: {examples_dir}")

    results: List[ExampleResult] = []
    for script in discover_examples(examples_dir):
        LOGGER.info("Running DAF example", {"script": str(script)})

        timestamp = int(time.time())
        # Create unique output directory for each example run
        resolved_output_dir = output_dir or examples_dir.parent.parent / "@outputs"
        example_output_dir = resolved_output_dir / f"{script.stem}_{timestamp}"
        example_output_dir.mkdir(parents=True, exist_ok=True)

        # Create subdirectories for organized outputs
        (example_output_dir / "replays").mkdir(exist_ok=True)
        (example_output_dir / "stats").mkdir(exist_ok=True)
        (example_output_dir / "checkpoints").mkdir(exist_ok=True)
        (example_output_dir / "visualizations").mkdir(exist_ok=True)
        (example_output_dir / "logs").mkdir(exist_ok=True)

        output_file = example_output_dir / "execution_log.json"

        # Set environment variables to direct outputs to the example directory
        import os

        env = os.environ.copy()
        env["DAF_OUTPUT_DIR"] = str(example_output_dir)
        env["DAF_REPLAY_DIR"] = str(example_output_dir / "replays")
        env["DAF_STATS_DIR"] = str(example_output_dir / "stats")
        env["DAF_CHECKPOINT_DIR"] = str(example_output_dir / "checkpoints")
        env["DAF_VISUALIZATION_DIR"] = str(example_output_dir / "visualizations")

        cmd = ["uv", "run", "python", str(script)]
        start = time.perf_counter()
        completed = subprocess.run(cmd, capture_output=True, text=True, cwd=examples_dir.parent, env=env)
        duration = time.perf_counter() - start

        result = ExampleResult(
            script=script,
            returncode=completed.returncode,
            duration=duration,
            stdout=completed.stdout,
            stderr=completed.stderr,
            output_file=output_file,
        )

        output_file.write_text(
            json.dumps(
                {
                    "script": str(script),
                    "returncode": completed.returncode,
                    "duration": duration,
                    "stdout": completed.stdout,
                    "stderr": completed.stderr,
                    "output_directory": str(example_output_dir),
                },
                indent=2,
            )
        )

        if completed.returncode != 0:
            LOGGER.error("Example failed", {"script": str(script), "stderr": completed.stderr})
        else:
            LOGGER.info(f"Example completed successfully. Outputs in: {example_output_dir}")

        results.append(result)

    return results
