"""
DAF Simulation Runner

Main simulation engine for running Metta AI experiments with automated
configuration, validation, and execution.
"""

import asyncio
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field
from typing_extensions import Literal

from daf.config.configuration import ConfigurationManager
from daf.config.models import SimulationConfig
from daf.core.engine import MettaEngine
from daf.core.validation import ValidationResult

logger = logging.getLogger(__name__)


class SimulationResult(BaseModel):
    """Results from a simulation run."""

    experiment_name: str = Field(..., description="Name of the experiment")
    status: Literal["success", "failed", "partial"] = Field(..., description="Final status")
    metrics: Dict[str, Any] = Field(default_factory=dict, description="Final metrics")
    artifacts: Dict[str, Path] = Field(default_factory=dict, description="Generated artifacts")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    execution_time: float = Field(..., description="Total execution time in seconds")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class SimulationRunner:
    """
    Main simulation runner for DAF experiments.

    Provides automated configuration, validation, and execution of Metta AI
    simulations with comprehensive error handling and reporting.
    """

    def __init__(
        self,
        config: Optional[Union[SimulationConfig, Path, str]] = None,
        engine: Optional[MettaEngine] = None,
        validate: bool = True,
    ):
        """
        Initialize simulation runner.

        Args:
            config: Simulation configuration or path to config file
            engine: Custom Metta engine instance
            validate: Whether to validate configuration on load
        """
        self.config_manager = ConfigurationManager()
        self.engine = engine or MettaEngine()
        self.logger = logging.getLogger(__name__)

        if config:
            self.load_config(config, validate=validate)

    def load_config(
        self,
        config: Union[SimulationConfig, Path, str],
        validate: bool = True,
    ) -> None:
        """
        Load simulation configuration.

        Args:
            config: Configuration object, path to config file, or config name
            validate: Whether to validate configuration
        """
        if isinstance(config, (Path, str)):
            self.config = self.config_manager.load_config_file(config)
        else:
            self.config = config

        if validate:
            self.config_manager.validate_config(self.config)

        self.logger.info(f"Loaded configuration for experiment: {self.config.name}")

    async def run(
        self,
        config: Optional[Union[SimulationConfig, Path, str]] = None,
        **overrides: Any,
    ) -> SimulationResult:
        """
        Run a simulation with the configured parameters.

        Args:
            config: Optional configuration override
            **overrides: Runtime parameter overrides

        Returns:
            SimulationResult with results and metrics
        """
        if config:
            self.load_config(config, validate=True)

        # Apply runtime overrides
        if overrides:
            self.config = self.config_manager.apply_overrides(self.config, overrides)

        self.logger.info(f"Starting simulation: {self.config.name}")

        try:
            # Pre-run validation
            validation_result = await self._validate_prerequisites()
            if not validation_result.is_valid:
                return SimulationResult(
                    experiment_name=self.config.name,
                    status="failed",
                    error_message="Prerequisites validation failed",
                    execution_time=0.0,
                    metadata={"validation": validation_result.dict()},
                )

            # Setup simulation environment
            await self._setup_simulation()

            # Run simulation
            start_time = asyncio.get_event_loop().time()
            metrics = await self._execute_simulation()
            execution_time = asyncio.get_event_loop().time() - start_time

            # Post-processing
            artifacts = await self._collect_artifacts()

            # Validate results
            final_status = await self._validate_results(metrics)

            return SimulationResult(
                experiment_name=self.config.name,
                status=final_status,
                metrics=metrics,
                artifacts=artifacts,
                execution_time=execution_time,
                metadata={"config": self.config.dict()},
            )

        except Exception as e:
            self.logger.error(f"Simulation failed: {e}")
            return SimulationResult(
                experiment_name=self.config.name,
                status="failed",
                error_message=str(e),
                execution_time=0.0,
                metadata={"config": self.config.dict()},
            )

    async def _validate_prerequisites(self) -> ValidationResult:
        """Validate system prerequisites for simulation."""
        validator = self.engine.get_validator()

        # Check system resources
        system_ok = await validator.validate_system()

        # Check configuration compatibility
        config_ok = await validator.validate_config(self.config)

        # Check Metta AI availability
        metta_ok = await validator.validate_metta_installation()

        return ValidationResult.combine([system_ok, config_ok, metta_ok])

    async def _setup_simulation(self) -> None:
        """Setup simulation environment and resources."""
        self.logger.info("Setting up simulation environment...")

        # Create output directories
        await self._create_output_directories()

        # Initialize logging
        await self._setup_logging()

        # Setup monitoring
        await self._setup_monitoring()

    async def _execute_simulation(self) -> Dict[str, Any]:
        """Execute the actual simulation."""
        self.logger.info("Executing simulation...")

        # Use Metta engine to run simulation
        return await self.engine.simulate(self.config)

    async def _collect_artifacts(self) -> Dict[str, Path]:
        """Collect generated artifacts from simulation."""
        self.logger.info("Collecting artifacts...")

        artifacts = {}
        # Implementation would collect checkpoints, logs, etc.
        return artifacts

    async def _validate_results(self, metrics: Dict[str, Any]) -> str:
        """Validate simulation results."""
        # Basic validation - can be extended
        if not metrics:
            return "failed"

        # Check for required metrics
        required_metrics = ["total_reward", "episode_length"]
        if not all(metric in metrics for metric in required_metrics):
            return "partial"

        return "success"

    async def _create_output_directories(self) -> None:
        """Create necessary output directories."""
        from daf.core.output import get_experiment_output_path

        output_dir = get_experiment_output_path(self.config.name, create=True)

        # Ensure subdirectories exist
        subdirs = ["checkpoints", "logs", "artifacts", "metrics"]
        for subdir in subdirs:
            (output_dir / subdir).mkdir(exist_ok=True)

        logger.info(f"Output directory created: {output_dir}")

    async def _setup_logging(self) -> None:
        """Setup simulation-specific logging."""
        # Implementation would configure logging
        pass

    async def _setup_monitoring(self) -> None:
        """Setup monitoring and metrics collection."""
        # Implementation would setup monitoring
        pass

    async def run_batch(
        self,
        configs: List[Union[SimulationConfig, Path, str]],
        **common_overrides: Any,
    ) -> List[SimulationResult]:
        """
        Run multiple simulations in batch.

        Args:
            configs: List of configurations to run
            **common_overrides: Overrides applied to all simulations

        Returns:
            List of simulation results
        """
        results = []

        for config in configs:
            # Apply common overrides
            if common_overrides:
                if hasattr(config, "dict"):
                    config_dict = self.config_manager.apply_overrides(config, common_overrides)
                    config = type(config)(**config_dict)

            result = await self.run(config)
            results.append(result)

            # Add small delay between runs to avoid resource conflicts
            await asyncio.sleep(1.0)

        return results

    def get_status(self) -> Dict[str, Any]:
        """Get current runner status."""
        return {
            "config_loaded": hasattr(self, "config"),
            "engine_ready": self.engine.is_ready(),
            "experiment_name": getattr(self.config, "name", None) if hasattr(self, "config") else None,
        }
