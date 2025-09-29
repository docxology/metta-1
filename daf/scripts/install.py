#!/usr/bin/env python3
"""
DAF (Distributed Agent Framework) Installation Script

This script provides hands-off installation and configuration of the DAF framework,
including Metta AI setup, dependency management, and validation.

Usage:
    python scripts/install.py [OPTIONS]

Options:
    --profile PROFILE     Installation profile (research, production, dev) [default: research]
    --non-interactive     Run without user prompts
    --with-tests         Include test dependencies
    --validate           Run full validation after installation
    --clean             Clean existing installation before setup
    --dev               Setup development environment with debug tools
    --config FILE       Use custom configuration file
    --verbose           Enable verbose output
"""

import argparse
import asyncio
import logging
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from daf.core.configuration import ConfigurationManager
from daf.core.installation import InstallationManager
from daf.core.logging import setup_logging
from daf.core.validation import SystemValidator

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class DAFInstaller:
    """Main installation orchestrator for DAF framework."""

    def __init__(self, args: argparse.Namespace):
        self.args = args
        self.project_root = Path(__file__).parent.parent
        self.install_manager = InstallationManager(self.project_root)
        self.system_validator = SystemValidator()
        self.config_manager = ConfigurationManager()

    async def run(self) -> int:
        """Main installation workflow."""
        try:
            logger.info("🚀 Starting DAF installation...")

            # Phase 1: System validation
            await self._validate_system()

            # Phase 2: Clean existing installation if requested
            if self.args.clean:
                await self._clean_installation()

            # Phase 3: Setup configuration
            await self._setup_configuration()

            # Phase 4: Install dependencies
            await self._install_dependencies()

            # Phase 5: Setup Metta AI
            await self._setup_metta()

            # Phase 6: Validate installation
            if self.args.validate:
                await self._validate_installation()

            # Phase 7: Setup development environment if requested
            if self.args.dev:
                await self._setup_development_environment()

            logger.info("✅ DAF installation completed successfully!")
            self._print_success_message()
            return 0

        except Exception as e:
            logger.error(f"❌ Installation failed: {e}")
            if self.args.verbose:
                import traceback

                logger.error(traceback.format_exc())
            return 1

    async def _validate_system(self) -> None:
        """Validate system requirements and compatibility."""
        logger.info("🔍 Validating system requirements...")

        system_info = self.system_validator.validate_system()
        if not system_info.is_compatible:
            logger.error("❌ System is not compatible with DAF:")
            for issue in system_info.issues:
                logger.error(f"  - {issue}")
            raise RuntimeError("System compatibility check failed")

        logger.info("✅ System validation passed")

        if self.args.verbose:
            logger.info(f"System info: {system_info}")

    async def _clean_installation(self) -> None:
        """Clean existing installation."""
        logger.info("🧹 Cleaning existing installation...")

        clean_targets = [
            ".venv",
            "build",
            "dist",
            "*.egg-info",
            "__pycache__",
            ".pytest_cache",
            ".coverage",
            "htmlcov",
            ".mypy_cache",
        ]

        for target in clean_targets:
            if Path(target).exists():
                import shutil

                if Path(target).is_dir():
                    shutil.rmtree(target)
                else:
                    Path(target).unlink()

        logger.info("✅ Cleanup completed")

    async def _setup_configuration(self) -> None:
        """Setup DAF configuration."""
        logger.info("⚙️ Setting up configuration...")

        # Load base configuration
        config = self.config_manager.load_base_config()

        # Apply profile-specific configuration
        if self.args.profile:
            profile_config = self.config_manager.load_profile_config(self.args.profile)
            config = self.config_manager.merge_configs(config, profile_config)

        # Apply custom configuration if provided
        if self.args.config:
            custom_config = self.config_manager.load_config_file(self.args.config)
            config = self.config_manager.merge_configs(config, custom_config)

        # Validate configuration
        self.config_manager.validate_config(config)

        # Save configuration
        self.config_manager.save_config(config, "configs/active_config.yaml")

        logger.info("✅ Configuration setup completed")

    async def _install_dependencies(self) -> None:
        """Install Python dependencies using uv."""
        logger.info("📦 Installing Python dependencies...")

        # Setup uv if not present
        await self.install_manager.setup_uv()

        # Install dependencies based on profile
        dependency_groups = ["core"]
        if self.args.with_tests:
            dependency_groups.append("testing")
        if self.args.dev:
            dependency_groups.extend(["dev", "interactive"])

        await self.install_manager.install_dependencies(groups=dependency_groups, upgrade=self.args.clean)

        logger.info("✅ Dependencies installed")

    async def _setup_metta(self) -> None:
        """Setup and configure Metta AI framework."""
        logger.info("🤖 Setting up Metta AI framework...")

        # Install Metta AI components
        await self.install_manager.install_metta_components()

        # Configure Metta AI
        await self.install_manager.configure_metta(profile=self.args.profile, non_interactive=self.args.non_interactive)

        # Validate Metta installation
        await self.install_manager.validate_metta_installation()

        logger.info("✅ Metta AI setup completed")

    async def _validate_installation(self) -> None:
        """Run comprehensive installation validation."""
        logger.info("🔍 Running installation validation...")

        # Validate DAF components
        await self.install_manager.validate_daf_installation()

        # Validate Metta integration
        await self.install_manager.validate_metta_integration()

        # Run smoke tests
        await self.install_manager.run_smoke_tests()

        logger.info("✅ Installation validation passed")

    async def _setup_development_environment(self) -> None:
        """Setup development environment with debug tools."""
        logger.info("🛠️ Setting up development environment...")

        # Install development tools
        await self.install_manager.setup_dev_tools()

        # Setup pre-commit hooks
        await self.install_manager.setup_pre_commit_hooks()

        # Setup IDE configuration
        await self.install_manager.setup_ide_config()

        logger.info("✅ Development environment setup completed")

    def _print_success_message(self) -> None:
        """Print success message with next steps."""
        print("\n" + "=" * 60)
        print("🎉 DAF Installation Completed Successfully!")
        print("=" * 60)
        print(f"📁 Project Location: {self.project_root}")
        print("🚀 Quick Start Commands:")
        print("   daf run experiment configs/experiments/quick_test.yaml")
        print("   daf list experiments")
        print("   daf validate system")
        print("📖 Documentation: See README.md for detailed usage")
        print("🔧 Development: Run 'python scripts/validate.py system' to check status")
        print("=" * 60)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="DAF (Distributed Agent Framework) Installation Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic research setup
  python scripts/install.py --profile research

  # Production setup with validation
  python scripts/install.py --profile production --with-tests --validate

  # Development setup
  python scripts/install.py --dev --clean

  # Custom configuration
  python scripts/install.py --config configs/custom.yaml
        """,
    )

    parser.add_argument(
        "--profile",
        choices=["research", "production", "dev", "minimal"],
        default="research",
        help="Installation profile (default: research)",
    )
    parser.add_argument("--non-interactive", action="store_true", help="Run without user prompts")
    parser.add_argument("--with-tests", action="store_true", help="Include test dependencies")
    parser.add_argument("--validate", action="store_true", help="Run full validation after installation")
    parser.add_argument("--clean", action="store_true", help="Clean existing installation before setup")
    parser.add_argument("--dev", action="store_true", help="Setup development environment with debug tools")
    parser.add_argument("--config", type=Path, help="Use custom configuration file")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    # Setup logging based on verbosity
    log_level = logging.DEBUG if args.verbose else logging.INFO
    setup_logging(level=log_level)

    # Run installation
    installer = DAFInstaller(args)
    exit_code = asyncio.run(installer.run())
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
