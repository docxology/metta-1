#!/usr/bin/env python3
"""
DAF Setup System

Handles initialization and setup of the DAF fork environment.
"""

import logging
import sys
from pathlib import Path
from typing import Optional

try:
    from ..config.daf_config import DAFConfig
except ImportError:
    # Fallback for testing scenarios
    try:
        from daf.config.daf_config import DAFConfig
    except ImportError:
        # Final fallback - create a placeholder
        from dataclasses import dataclass

        @dataclass
        class DAFConfig:
            experiment_name: str = "daf_experiment"


class DAFSetup:
    """
    DAF Setup and Initialization System

    Handles the setup and configuration of the DAF fork environment.
    """

    def __init__(self, config: Optional[DAFConfig] = None):
        """
        Initialize DAF setup

        Args:
            config: DAF configuration object
        """
        self.logger = logging.getLogger(__name__)
        self.config = config or DAFConfig()
        self.daf_root = Path(__file__).parent.parent.parent.parent
        self.at_daf_root = Path("@daf")

    def initialize_environment(self) -> bool:
        """
        Initialize the DAF environment

        Returns:
            True if initialization successful
        """
        try:
            self.logger.info("Initializing DAF environment...")

            # Create necessary directories
            self._create_directories()

            # Setup logging
            self._setup_logging()

            # Validate Metta repository
            if not self._validate_metta_repository():
                self.logger.error("Metta repository not found or incomplete")
                return False

            # Generate initial documentation if needed
            if self.config.generate_docs_on_startup:
                self._generate_initial_docs()

            self.logger.info("✅ DAF environment initialized successfully")
            return True

        except Exception as e:
            self.logger.error(f"Failed to initialize DAF environment: {e}")
            return False

    def _create_directories(self):
        """Create necessary DAF directories"""
        directories = [
            self.at_daf_root / "methods",
            self.at_daf_root / "structure",
            self.daf_root / "test_outputs",
            self.daf_root / "outputs",
            self.daf_root / "logs",
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            self.logger.debug(f"Created directory: {directory}")

    def _setup_logging(self):
        """Setup comprehensive logging for DAF"""
        log_file = self.daf_root / "daf.log"

        # Create formatters
        file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        console_formatter = logging.Formatter("%(levelname)s: %(message)s")

        # Setup file handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_formatter)

        # Setup console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(console_formatter)

        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)

        self.logger.info(f"DAF logging initialized: {log_file}")

    def _validate_metta_repository(self) -> bool:
        """Validate that Metta repository is available"""
        # Look for metta directory in multiple possible locations
        possible_paths = [
            self.daf_root.parent / "metta",  # Project root/metta
            Path.cwd() / "metta",  # Current working directory/metta
            Path(__file__).parent.parent.parent.parent.parent / "metta",  # From daf/src/daf/setup/
        ]

        metta_path = None
        for path in possible_paths:
            if path.exists() and (path / "adaptive").exists():
                metta_path = path
                break

        if metta_path is None:
            self.logger.error("Metta repository not found in any expected location")
            for path in possible_paths:
                self.logger.debug(f"Checked: {path} - exists: {path.exists()}")
            return False

        required_modules = ["adaptive", "cogworks", "rl", "setup"]

        for module in required_modules:
            module_path = metta_path / module
            if not module_path.exists():
                self.logger.warning(f"Required Metta module not found: {module} at {module_path}")
                return False

        self.logger.info(f"✅ Metta repository validation passed at: {metta_path}")
        return True

    def _generate_initial_docs(self):
        """Generate initial documentation if needed"""
        from ..tools import generate_comprehensive_daf_docs

        try:
            self.logger.info("Generating initial DAF documentation...")
            success = generate_comprehensive_daf_docs()
            if success:
                self.logger.info("✅ Initial documentation generated")
            else:
                self.logger.warning("Initial documentation generation failed")
        except Exception as e:
            self.logger.error(f"Error generating initial docs: {e}")


def initialize_daf_environment(config: Optional[DAFConfig] = None) -> DAFSetup:
    """
    Initialize DAF environment

    Args:
        config: DAF configuration

    Returns:
        Initialized DAFSetup instance
    """
    setup = DAFSetup(config)
    success = setup.initialize_environment()

    if not success:
        raise RuntimeError("Failed to initialize DAF environment")

    return setup
