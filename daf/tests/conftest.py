"""
DAF Test Configuration

Pytest configuration and fixtures for DAF testing.
"""

import asyncio
import tempfile
from pathlib import Path
from typing import Generator

import pytest

from daf.config.configuration import ConfigurationManager
from daf.core.validation import SystemValidator


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as temp_path:
        yield Path(temp_path)


@pytest.fixture
def config_manager(temp_dir: Path) -> ConfigurationManager:
    """Create a configuration manager for testing."""
    return ConfigurationManager(config_dir=temp_dir / "configs")


@pytest.fixture
def system_validator() -> SystemValidator:
    """Create a system validator for testing."""
    return SystemValidator()


@pytest.fixture(scope="session")
def sample_config_data():
    """Sample configuration data for tests."""
    return {
        "name": "test_experiment",
        "description": "Test experiment configuration",
        "environment": {
            "name": "test_env",
            "type": "mettagrid",
            "num_agents": 8,
            "map_config": {"width": 20, "height": 20},
        },
        "training": {
            "total_timesteps": 10000,
            "learning_rate": 0.001,
            "batch_size": 512,
        },
        "evaluation": {
            "frequency": 1000,
            "num_episodes": 10,
        },
    }


@pytest.fixture(scope="session")
def sample_invalid_config_data():
    """Sample invalid configuration data for tests."""
    return {
        "name": "",  # Invalid: empty name
        "environment": {
            "num_agents": -1,  # Invalid: negative agents
        },
        "training": {
            "total_timesteps": -1000,  # Invalid: negative timesteps
        },
    }
