"""
DAF Metta Engine

Interface layer between DAF and Metta AI framework providing:
- Unified API for Metta operations
- Configuration translation
- Result processing and validation
- Error handling and recovery
"""

import asyncio
import logging
import subprocess
from pathlib import Path
from typing import Any, Dict, Optional, Union

from daf.config.models import SimulationConfig
from daf.core.validation import SystemValidator, ValidationResult

logger = logging.getLogger(__name__)


class MettaEngine:
    """
    Engine for interfacing with Metta AI framework.

    Provides a unified interface for running Metta simulations with
    automatic configuration, validation, and error handling.
    """

    def __init__(self, metta_path: Optional[Union[str, Path]] = None):
        """
        Initialize Metta engine.

        Args:
            metta_path: Path to Metta installation or auto-detect
        """
        self.metta_path = Path(metta_path) if metta_path else None
        self.validator = SystemValidator()
        self._metta_available = None  # Cache availability check

    def _find_metta(self) -> Path:
        """Find Metta installation path."""
        # Try common locations
        common_paths = [
            Path.cwd() / "metta",  # Current directory
            Path.home() / "metta",  # Home directory
            Path("/usr/local/lib/metta"),  # System location
            Path("/opt/metta"),  # Alternative system location
        ]

        for path in common_paths:
            if self._is_metta_installed(path):
                logger.info(f"Found Metta installation at: {path}")
                return path

        # Try to find via Python imports
        try:
            import metta

            metta_path = Path(metta.__file__).parent.parent
            logger.info(f"Found Metta via Python import at: {metta_path}")
            return metta_path
        except ImportError:
            pass

        raise RuntimeError("Metta AI not found. Please install Metta AI or specify path.")

    def _is_metta_installed(self, path: Path) -> bool:
        """Check if Metta is installed at the given path."""
        if not path.exists():
            return False

        # Check for key Metta components
        indicators = [
            path / "metta" / "__init__.py",
            path / "pyproject.toml",
            path / "tools" / "run.py",
        ]

        return any(indicator.exists() for indicator in indicators)

    def _ensure_metta_available(self) -> None:
        """Ensure Metta components are available."""
        try:
            # Try importing Metta modules
            import metta
            import mettagrid
            from metta.tools.run import run_tool

            self.metta_version = getattr(metta, "__version__", "unknown")
            logger.info(f"Metta AI version: {self.metta_version}")

        except ImportError as e:
            raise RuntimeError(f"Metta AI components not available: {e}")

    def is_ready(self) -> bool:
        """Check if the engine is ready to run simulations."""
        if self._metta_available is None:
            try:
                self._ensure_metta_available()
                self._metta_available = True
            except RuntimeError:
                self._metta_available = False
        return self._metta_available

    def get_validator(self) -> SystemValidator:
        """Get system validator instance."""
        return self.validator

    async def simulate(self, config: SimulationConfig) -> Dict[str, Any]:
        """
        Run a simulation using Metta AI.

        Args:
            config: DAF simulation configuration

        Returns:
            Dictionary with simulation results and metrics
        """
        logger.info(f"Starting simulation: {config.name}")

        # Convert DAF config to Metta format
        metta_config = self._convert_to_metta_config(config)

        # Validate Metta configuration
        validation_result = await self._validate_metta_config(metta_config)
        if not validation_result.is_valid:
            raise RuntimeError(f"Metta configuration validation failed: {validation_result.message}")

        # Run simulation using Metta tools
        result = await self._run_metta_simulation(metta_config)

        # Process and validate results
        processed_result = self._process_results(result, config)

        logger.info(f"Simulation completed: {config.name}")
        return processed_result

    def _convert_to_metta_config(self, config: SimulationConfig) -> Dict[str, Any]:
        """Convert DAF config to Metta-compatible format."""
        # This would translate DAF configuration to Metta's expected format
        # Implementation depends on Metta's configuration schema

        metta_config = {
            "experiment_name": config.name,
            "simulation": {
                "environment": config.environment,
                "num_agents": getattr(config, "num_agents", 24),
                "map_size": getattr(config, "map_size", [50, 50]),
                "max_episodes": getattr(config, "max_episodes", 1000),
                "max_timesteps": getattr(config, "max_timesteps", 100000),
            },
            "curriculum": getattr(config, "curriculum", {}),
            "training": getattr(config, "training", {}),
            "evaluation": getattr(config, "evaluation", {}),
        }

        return metta_config

    async def _validate_metta_config(self, config: Dict[str, Any]) -> ValidationResult:
        """Validate Metta configuration."""
        try:
            # Use Metta's validation if available
            if hasattr(self, "_metta_validator"):
                return await self._metta_validator.validate(config)

            # Basic validation
            required_fields = ["experiment_name", "simulation.environment"]
            missing_fields = [field for field in required_fields if field not in config]

            if missing_fields:
                return ValidationResult(
                    is_valid=False,
                    message=f"Missing required fields: {missing_fields}",
                    issues=missing_fields,
                )

            return ValidationResult(is_valid=True, message="Configuration is valid")

        except Exception as e:
            return ValidationResult(
                is_valid=False,
                message=f"Validation error: {e}",
                issues=[str(e)],
            )

    async def _run_metta_simulation(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Run simulation using Metta tools."""
        try:
            # Use Metta's recipe system via subprocess or direct import
            if self._use_subprocess():
                return await self._run_via_subprocess(config)
            else:
                return await self._run_via_direct_import(config)

        except Exception as e:
            logger.error(f"Simulation execution failed: {e}")
            raise RuntimeError(f"Failed to run Metta simulation: {e}")

    def _use_subprocess(self) -> bool:
        """Determine if we should use subprocess for Metta execution."""
        # Use subprocess for better isolation and error handling
        return True

    async def _run_via_subprocess(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Run Metta simulation via subprocess call."""
        import json
        import tempfile

        # Save config to temporary file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(config, f, indent=2)
            config_file = f.name

        try:
            # Build Metta command
            cmd = [
                str(self.metta_path / "tools" / "run.py"),
                "experiments.recipes.arena.train",
                f"run={config['experiment_name']}",
                f"config={config_file}",
            ]

            # Add additional parameters
            if "simulation" in config:
                sim_config = config["simulation"]
                if "num_agents" in sim_config:
                    cmd.append(f"env.num_agents={sim_config['num_agents']}")
                if "max_timesteps" in sim_config:
                    cmd.append(f"trainer.total_timesteps={sim_config['max_timesteps']}")

            # Run command
            logger.info(f"Running Metta command: {' '.join(cmd)}")

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=3600,  # 1 hour timeout
                cwd=self.metta_path,
            )

            if result.returncode != 0:
                logger.error(f"Metta command failed: {result.stderr}")
                raise RuntimeError(f"Metta execution failed: {result.stderr}")

            # Parse output (this would need to be adapted based on Metta's output format)
            return self._parse_metta_output(result.stdout)

        finally:
            # Clean up temporary file
            Path(config_file).unlink(missing_ok=True)

    async def _run_via_direct_import(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Run simulation using direct Metta imports."""
        try:
            # This would use Metta's Python API directly
            # Implementation depends on Metta's internal APIs

            # Example (pseudo-code):
            # from metta.experiments.recipes.arena import train
            # result = await train(**config)

            raise NotImplementedError("Direct import execution not yet implemented")

        except Exception as e:
            logger.error(f"Direct import execution failed: {e}")
            raise RuntimeError(f"Direct execution failed: {e}")

    def _parse_metta_output(self, output: str) -> Dict[str, Any]:
        """Parse Metta output into DAF format."""
        # This would parse Metta's output format into DAF metrics
        # Implementation depends on Metta's actual output format

        # Placeholder implementation
        return {
            "total_reward": 0.0,
            "episode_length": 0,
            "convergence_time": 0.0,
            "final_checkpoint": "path/to/checkpoint.pt",
        }

    def _process_results(self, raw_result: Dict[str, Any], config: SimulationConfig) -> Dict[str, Any]:
        """Process and validate raw simulation results."""
        # Validate required metrics are present
        required_metrics = ["total_reward", "episode_length"]
        missing_metrics = [metric for metric in required_metrics if metric not in raw_result]

        if missing_metrics:
            logger.warning(f"Missing expected metrics: {missing_metrics}")

        # Add metadata
        processed_result = {
            "experiment_name": config.name,
            "config_summary": {
                "environment": getattr(config, "environment", "unknown"),
                "num_agents": getattr(config, "num_agents", 0),
                "max_timesteps": getattr(config, "max_timesteps", 0),
            },
            "timestamp": asyncio.get_event_loop().time(),
            **raw_result,
        }

        return processed_result
