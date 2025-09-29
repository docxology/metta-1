"""
Unit tests for DAF simulation system.
"""

from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

import pytest

from daf.config.models import SimulationConfig
from daf.core.engine import MettaEngine
from daf.core.simulation import SimulationResult, SimulationRunner


class TestSimulationRunner:
    """Test simulation runner functionality."""

    @pytest.fixture
    def sample_config(self):
        """Sample simulation configuration."""
        return SimulationConfig(
            name="test_simulation",
            environment={
                "name": "test_env",
                "type": "mettagrid",
                "num_agents": 8,
                "map_config": {"width": 20, "height": 20},
            },
            training={
                "total_timesteps": 10000,
                "learning_rate": 0.001,
                "batch_size": 512,
            },
            evaluation={
                "frequency": 1000,
                "num_episodes": 10,
            },
        )

    @pytest.fixture
    def mock_engine(self):
        """Mock Metta engine."""
        engine = MagicMock(spec=MettaEngine)
        engine.is_ready.return_value = True
        engine.simulate = AsyncMock(
            return_value={
                "total_reward": 100.0,
                "episode_length": 50,
                "convergence_time": 25.0,
            }
        )
        engine.get_validator = MagicMock()
        return engine

    def test_runner_initialization(self, sample_config, mock_engine):
        """Test simulation runner initialization."""
        runner = SimulationRunner(sample_config, mock_engine)

        assert runner.config.name == "test_simulation"
        assert runner.engine == mock_engine


def test_load_config_from_file(temp_dir, sample_config_data):
    """Test loading configuration from file."""
    import yaml

    # Create config file
    config_file = temp_dir / "test_experiment.yaml"
    config_dict = sample_config_data.copy()
    # Convert PosixPath to string for YAML serialization
    if "output_dir" in config_dict and config_dict["output_dir"]:
        config_dict["output_dir"] = str(config_dict["output_dir"])
    with open(config_file, "w") as f:
        yaml.safe_dump(config_dict, f)

        # Test loading
        runner = SimulationRunner()
        runner.load_config(config_file)

        assert runner.config.name == "test_experiment"

    def test_apply_overrides(self, sample_config):
        """Test applying runtime overrides."""
        runner = SimulationRunner(sample_config)

        overrides = {
            "training.total_timesteps": 50000,
            "environment.num_agents": 16,
        }

        modified_config = runner.config_manager.apply_overrides(runner.config, overrides)

        assert modified_config.training.total_timesteps == 50000
        assert modified_config.environment.num_agents == 16

    @pytest.mark.asyncio
    async def test_run_simulation_success(self, sample_config, mock_engine):
        """Test successful simulation run."""
        # Mock validation
        mock_validator = MagicMock()
        mock_validator.validate_system = AsyncMock(return_value=MagicMock(is_valid=True))
        mock_validator.validate_config = AsyncMock(return_value=MagicMock(is_valid=True))
        mock_validator.validate_metta_installation = AsyncMock(return_value=MagicMock(is_valid=True))
        mock_engine.get_validator.return_value = mock_validator

        runner = SimulationRunner(sample_config, mock_engine)
        result = await runner.run()

        assert isinstance(result, SimulationResult)
        assert result.status == "success"
        assert result.experiment_name == "test_simulation"
        assert result.metrics["total_reward"] == 100.0
        assert result.execution_time > 0

    @pytest.mark.asyncio
    async def test_run_simulation_validation_failure(self, sample_config, mock_engine):
        """Test simulation run with validation failure."""
        # Mock validation failure
        mock_validator = MagicMock()
        mock_validator.validate_system = AsyncMock(
            return_value=MagicMock(is_valid=False, message="System incompatible")
        )
        mock_engine.get_validator.return_value = mock_validator

        runner = SimulationRunner(sample_config, mock_engine)
        result = await runner.run()

        assert isinstance(result, SimulationResult)
        assert result.status == "failed"
        assert "validation failed" in result.error_message.lower()

    @pytest.mark.asyncio
    async def test_run_simulation_engine_failure(self, sample_config, mock_engine):
        """Test simulation run with engine failure."""
        # Mock engine failure
        mock_engine.simulate = AsyncMock(side_effect=RuntimeError("Engine failed"))

        # Mock validation success
        mock_validator = MagicMock()
        mock_validator.validate_system = AsyncMock(return_value=MagicMock(is_valid=True))
        mock_validator.validate_config = AsyncMock(return_value=MagicMock(is_valid=True))
        mock_validator.validate_metta_installation = AsyncMock(return_value=MagicMock(is_valid=True))
        mock_engine.get_validator.return_value = mock_validator

        runner = SimulationRunner(sample_config, mock_engine)
        result = await runner.run()

        assert isinstance(result, SimulationResult)
        assert result.status == "failed"
        assert "engine failed" in result.error_message.lower()

    @pytest.mark.asyncio
    async def test_batch_run_sequential(self, sample_config, mock_engine):
        """Test running multiple simulations sequentially."""
        # Mock validation
        mock_validator = MagicMock()
        mock_validator.validate_system = AsyncMock(return_value=MagicMock(is_valid=True))
        mock_validator.validate_config = AsyncMock(return_value=MagicMock(is_valid=True))
        mock_validator.validate_metta_installation = AsyncMock(return_value=MagicMock(is_valid=True))
        mock_engine.get_validator.return_value = mock_validator

        runner = SimulationRunner(sample_config, mock_engine)

        # Create multiple configs
        configs = [sample_config, sample_config]

        results = await runner.run_batch(configs, parallel=False)

        assert len(results) == 2
        assert all(isinstance(r, SimulationResult) for r in results)
        assert all(r.status == "success" for r in results)

    @pytest.mark.asyncio
    async def test_batch_run_parallel(self, sample_config, mock_engine):
        """Test running multiple simulations in parallel."""
        # Mock validation
        mock_validator = MagicMock()
        mock_validator.validate_system = AsyncMock(return_value=MagicMock(is_valid=True))
        mock_validator.validate_config = AsyncMock(return_value=MagicMock(is_valid=True))
        mock_validator.validate_metta_installation = AsyncMock(return_value=MagicMock(is_valid=True))
        mock_engine.get_validator.return_value = mock_validator

        runner = SimulationRunner(sample_config, mock_engine)

        # Create multiple configs
        configs = [sample_config, sample_config]

        results = await runner.run_batch(configs, parallel=True)

        assert len(results) == 2
        assert all(isinstance(r, SimulationResult) for r in results)
        assert all(r.status == "success" for r in results)

    def test_get_status(self, sample_config):
        """Test getting runner status."""
        runner = SimulationRunner(sample_config)

        status = runner.get_status()

        assert isinstance(status, dict)
        assert "config_loaded" in status
        assert "engine_ready" in status
        assert "experiment_name" in status

        assert status["config_loaded"] is True
        assert status["experiment_name"] == "test_simulation"


class TestSimulationResult:
    """Test simulation result handling."""

    def test_result_creation(self):
        """Test creating simulation results."""
        result = SimulationResult(
            experiment_name="test_exp",
            status="success",
            metrics={"reward": 100.0},
            artifacts={"checkpoint": Path("checkpoint.pt")},
            execution_time=25.5,
            metadata={"config": {"name": "test"}},
        )

        assert result.experiment_name == "test_exp"
        assert result.status == "success"
        assert result.metrics["reward"] == 100.0
        assert result.artifacts["checkpoint"] == Path("checkpoint.pt")
        assert result.execution_time == 25.5
        assert result.metadata["config"]["name"] == "test"

    def test_result_validation(self):
        """Test result validation logic."""
        # Valid result
        valid_result = SimulationResult(
            experiment_name="test",
            status="success",
            metrics={"total_reward": 100.0, "episode_length": 50},
            execution_time=25.0,
        )
        assert valid_result.status == "success"

        # Invalid result - no metrics
        invalid_result = SimulationResult(
            experiment_name="test",
            status="success",
            metrics={},
            execution_time=25.0,
        )
        assert invalid_result.status == "success"  # Status doesn't auto-change

        # Failed result
        failed_result = SimulationResult(
            experiment_name="test",
            status="failed",
            error_message="Test error",
            execution_time=0.0,
        )
        assert failed_result.status == "failed"
        assert failed_result.error_message == "Test error"
