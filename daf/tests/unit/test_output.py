"""
Unit tests for DAF output management.
"""

import tempfile
from pathlib import Path

import pytest

from daf.core.output import OutputManager, get_output_manager, setup_output_manager


class TestOutputManager:
    """Test output manager functionality."""

    @pytest.fixture
    def temp_output_dir(self):
        """Create a temporary output directory for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    def test_output_manager_creation(self, temp_output_dir):
        """Test creating an output manager."""
        manager = OutputManager(temp_output_dir)

        assert manager.base_output_dir == temp_output_dir
        assert temp_output_dir.exists()

    def test_standard_directories_creation(self, temp_output_dir):
        """Test that standard directories are created."""
        manager = OutputManager(temp_output_dir)

        standard_dirs = ["tests", "examples", "experiments", "logs", "checkpoints", "artifacts"]
        for dir_name in standard_dirs:
            assert (temp_output_dir / dir_name).exists()
            assert (temp_output_dir / dir_name).is_dir()

    def test_get_output_path(self, temp_output_dir):
        """Test getting output paths for different categories."""
        manager = OutputManager(temp_output_dir)

        # Test experiment path
        exp_path = manager.get_output_path("experiments", "test_experiment")
        assert exp_path == temp_output_dir / "experiments" / "test_experiment"
        assert exp_path.exists()

        # Test test path
        test_path = manager.get_output_path("tests", "test_component")
        assert test_path == temp_output_dir / "tests" / "test_component"
        assert test_path.exists()

    def test_specific_path_methods(self, temp_output_dir):
        """Test specific path methods."""
        manager = OutputManager(temp_output_dir)

        # Test experiment path
        exp_path = manager.get_experiment_output_path("my_experiment")
        assert exp_path == temp_output_dir / "experiments" / "my_experiment"

        # Test test path
        test_path = manager.get_test_output_path("my_test")
        assert test_path == temp_output_dir / "tests" / "my_test"

        # Test example path
        example_path = manager.get_example_output_path("my_example")
        assert example_path == temp_output_dir / "examples" / "my_example"

    def test_checkpoint_and_artifact_paths(self, temp_output_dir):
        """Test checkpoint and artifact path methods."""
        manager = OutputManager(temp_output_dir)

        # Test checkpoint path
        checkpoint_path = manager.get_checkpoint_path("experiment1", "checkpoint_100.pt")
        expected = temp_output_dir / "checkpoints" / "experiment1" / "checkpoint_100.pt"
        assert checkpoint_path == expected

        # Test artifact path
        artifact_path = manager.get_artifact_path("experiment1", "results.json")
        expected = temp_output_dir / "artifacts" / "experiment1" / "results.json"
        assert artifact_path == expected

    def test_output_info(self, temp_output_dir):
        """Test getting output information."""
        manager = OutputManager(temp_output_dir)

        # Create some test files
        test_file = temp_output_dir / "tests" / "test1" / "output.txt"
        test_file.parent.mkdir(exist_ok=True)
        test_file.write_text("test content")

        info = manager.get_output_info()

        assert "base_output_dir" in info
        assert "categories" in info
        assert "tests" in info["categories"]
        assert info["categories"]["tests"]["item_count"] >= 1

    def test_cleanup_old_outputs(self, temp_output_dir):
        """Test cleaning up old output directories."""
        manager = OutputManager(temp_output_dir)

        # Create some directories and files
        old_dir = temp_output_dir / "tests" / "old_test"
        old_dir.mkdir()
        (old_dir / "old_file.txt").write_text("old content")

        # Cleanup should not remove recently created directories
        cleaned = manager.cleanup_old_outputs(days_old=30)  # Only remove very old files
        assert cleaned == 0  # Nothing should be cleaned

    def test_global_output_manager(self):
        """Test global output manager functionality."""
        # Reset any existing manager
        import daf.core.output

        daf.core.output._output_manager = None

        # Get global manager
        manager = get_output_manager()
        assert isinstance(manager, OutputManager)

        # Setup with custom directory
        with tempfile.TemporaryDirectory() as tmpdir:
            custom_manager = setup_output_manager(tmpdir)
            assert custom_manager.base_output_dir == Path(tmpdir)

            # Global manager should be updated
            global_manager = get_output_manager()
            assert global_manager.base_output_dir == Path(tmpdir)


class TestOutputIntegration:
    """Test output integration with other components."""

    def test_simulation_output_integration(self, temp_dir):
        """Test that simulation components use output manager correctly."""
        from daf.config.models import SimulationConfig
        from daf.core.output import setup_output_manager

        # Setup output manager with temp directory
        manager = setup_output_manager(temp_dir)

        # Create simulation config
        config = SimulationConfig(
            name="integration_test",
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

        # Check that output directory is set correctly
        expected_output = temp_dir / "experiments" / "integration_test"
        assert config.output_dir == expected_output
        assert expected_output.exists()

    def test_multiple_experiments_output_isolation(self, temp_dir):
        """Test that multiple experiments get isolated output directories."""
        from daf.config.models import SimulationConfig
        from daf.core.output import setup_output_manager

        manager = setup_output_manager(temp_dir)

        # Create multiple experiment configs
        exp1_config = SimulationConfig(
            name="experiment_1",
            environment={"name": "env1", "type": "mettagrid", "num_agents": 8},
            training={"total_timesteps": 1000},
            evaluation={"frequency": 100, "num_episodes": 1},
        )

        exp2_config = SimulationConfig(
            name="experiment_2",
            environment={"name": "env2", "type": "mettagrid", "num_agents": 16},
            training={"total_timesteps": 2000},
            evaluation={"frequency": 200, "num_episodes": 2},
        )

        # Check that each has its own directory
        exp1_dir = temp_dir / "experiments" / "experiment_1"
        exp2_dir = temp_dir / "experiments" / "experiment_2"

        assert exp1_config.output_dir == exp1_dir
        assert exp2_config.output_dir == exp2_dir
        assert exp1_dir != exp2_dir
        assert exp1_dir.exists()
        assert exp2_dir.exists()
