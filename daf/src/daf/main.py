#!/usr/bin/env python3
"""
DAF Main Module

Main entry point for the DAF fork providing unified access to all functionality.
"""

import logging
from typing import Any, Dict, Optional

from .cli import DAFCLI
from .config.daf_config import DAFConfig, DAFConfigManager
from .logging import LogManager, setup_daf_logging
from .setup.daf_setup import initialize_daf_environment
from .tools import generate_comprehensive_daf_docs, sync_daf_with_metta, verify_daf_coverage
from .wrappers import AdaptiveWrapper, CurriculumWrapper, RLWrapper


class DAF:
    """
    Main DAF Class

    Provides unified interface to all DAF fork functionality.
    """

    def __init__(self, config: Optional[DAFConfig] = None):
        """
        Initialize DAF instance

        Args:
            config: DAF configuration
        """
        self.logger = logging.getLogger(__name__)
        self.config_manager = DAFConfigManager()
        self.config = config or self.config_manager.get_config()

        # Initialize core components
        self.setup = None
        self.log_manager = None
        self.wrappers = {}

        # Setup logging
        setup_daf_logging(log_level=self.config.log_level, console_output=True)

    def initialize(self) -> bool:
        """
        Initialize DAF environment

        Returns:
            True if initialization successful
        """
        try:
            self.logger.info("Initializing DAF environment...")

            # Initialize setup
            self.setup = initialize_daf_environment(self.config)

            # Initialize log manager
            self.log_manager = LogManager("daf/logs")

            # Initialize wrappers
            self._initialize_wrappers()

            self.logger.info("✅ DAF initialized successfully")
            return True

        except Exception as e:
            self.logger.error(f"DAF initialization failed: {e}")
            return False

    def _initialize_wrappers(self):
        """Initialize component wrappers"""
        try:
            self.wrappers["adaptive"] = AdaptiveWrapper()
            self.wrappers["rl"] = RLWrapper()
            self.wrappers["curriculum"] = CurriculumWrapper()

            self.logger.info("Component wrappers initialized")
        except Exception as e:
            self.logger.error(f"Wrapper initialization failed: {e}")

    def generate_docs(self, enhanced: bool = True) -> bool:
        """
        Generate documentation

        Args:
            enhanced: Whether to generate enhanced docs with signatures

        Returns:
            True if generation successful
        """
        try:
            self.logger.info("Generating DAF documentation...")
            success = generate_comprehensive_daf_docs()
            return success
        except Exception as e:
            self.logger.error(f"Documentation generation failed: {e}")
            return False

    def verify_coverage(self) -> bool:
        """
        Verify documentation coverage

        Returns:
            True if coverage is complete
        """
        try:
            self.logger.info("Verifying documentation coverage...")
            success = verify_daf_coverage()
            return success
        except Exception as e:
            self.logger.error(f"Coverage verification failed: {e}")
            return False

    def sync_with_metta(self) -> bool:
        """
        Synchronize with Metta repository

        Returns:
            True if sync successful
        """
        try:
            self.logger.info("Synchronizing with Metta repository...")
            success = sync_daf_with_metta()
            return success
        except Exception as e:
            self.logger.error(f"Metta sync failed: {e}")
            return False

    def run_tests(self) -> Dict[str, Any]:
        """
        Run DAF test suite

        Returns:
            Test results
        """
        try:
            self.logger.info("Running DAF test suite...")
            from ..tools.test_runner import DAFTestRunner

            runner = DAFTestRunner()
            results = runner.run_all_tests()

            self.logger.info(
                f"Tests completed: {results['summary']['passed']} passed, {results['summary']['failed']} failed"
            )
            return results

        except Exception as e:
            self.logger.error(f"Test execution failed: {e}")
            return {"error": str(e)}

    def get_status(self) -> Dict[str, Any]:
        """
        Get DAF status information

        Returns:
            Status dictionary
        """
        return {
            "initialized": self.setup is not None,
            "config": {
                "adaptive_enabled": self.config.adaptive_enabled,
                "rl_enabled": self.config.rl_enabled,
                "log_level": self.config.log_level,
            },
            "wrappers": {name: wrapper.is_initialized() for name, wrapper in self.wrappers.items()},
            "logs": self.log_manager.get_log_stats() if self.log_manager else {},
            "version": "1.0.0",
        }

    def run_cli(self, args: Optional[list] = None):
        """
        Run DAF CLI with arguments

        Args:
            args: CLI arguments
        """
        cli = DAFCLI()
        cli.run(args)


def create_daf_instance(config: Optional[DAFConfig] = None) -> DAF:
    """
    Create and initialize DAF instance

    Args:
        config: DAF configuration

    Returns:
        Initialized DAF instance
    """
    daf = DAF(config)
    success = daf.initialize()

    if not success:
        raise RuntimeError("Failed to initialize DAF instance")

    return daf


# Convenience functions
def quick_start() -> DAF:
    """Quick start DAF with default configuration"""
    return create_daf_instance()


def generate_docs() -> bool:
    """Generate comprehensive DAF documentation"""
    daf = create_daf_instance()
    return daf.generate_docs()


def run_tests() -> Dict[str, Any]:
    """Run DAF test suite"""
    daf = create_daf_instance()
    return daf.run_tests()


def verify_coverage() -> bool:
    """Verify documentation coverage"""
    daf = create_daf_instance()
    return daf.verify_coverage()


def sync_with_metta() -> bool:
    """Synchronize with Metta repository"""
    daf = create_daf_instance()
    return daf.sync_with_metta()
