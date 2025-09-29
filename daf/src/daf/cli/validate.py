"""
DAF Validate CLI Command

Provides validation and diagnostic commands for DAF system.
"""

import asyncio
import sys
from pathlib import Path
from typing import Optional

import typer

from daf.core.validation import ConfigurationValidator, InstallationValidator, SystemValidator

# Create validate command group
validate_command = typer.Typer(
    name="validate",
    help="Validation and diagnostic commands",
    no_args_is_help=True,
)


@validate_command.callback()
def validate_callback(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
    debug: bool = typer.Option(False, "--debug", help="Enable debug mode"),
):
    """DAF validation and diagnostic commands."""
    pass


@validate_command.command("system")
def validate_system(
    detailed: bool = typer.Option(False, help="Show detailed system information"),
    fix: bool = typer.Option(False, help="Attempt to fix issues automatically"),
):
    """Validate system requirements and compatibility."""
    from daf.core.logging import setup_logging

    setup_logging()

    async def run_system_validation():
        try:
            typer.echo("🔍 Validating system requirements...")

            validator = SystemValidator()
            result = validator.validate_system()

            _print_validation_result("System Validation", result, detailed)

            if not result.is_valid and fix:
                typer.echo("🔧 Attempting to fix issues...")
                # Basic fix attempts
                if "Python" in str(result.issues):
                    typer.echo("💡 Suggestion: Install Python 3.11.7 or later")
                if "memory" in str(result.issues).lower():
                    typer.echo("💡 Suggestion: Ensure adequate system memory")

            if result.is_valid:
                typer.echo("✅ System validation passed!")
            else:
                typer.echo("❌ System validation failed!")
                sys.exit(1)

        except Exception as e:
            typer.echo(f"❌ System validation failed: {e}")
            if debug:
                import traceback

                typer.echo(traceback.format_exc())
            sys.exit(1)

    asyncio.run(run_system_validation())


@validate_command.command("config")
def validate_config(
    config: Optional[Path] = typer.Argument(None, help="Configuration file to validate"),
    all_configs: bool = typer.Option(False, help="Validate all configuration files"),
    fix: bool = typer.Option(False, help="Attempt to fix configuration issues"),
):
    """Validate configuration files."""
    from daf.config.configuration import ConfigurationManager
    from daf.core.logging import setup_logging

    setup_logging()

    async def run_config_validation():
        try:
            if all_configs:
                await _validate_all_configs()
            elif config:
                await _validate_single_config(config)
            else:
                typer.echo("❌ Please specify a config file or use --all-configs")
                sys.exit(1)

        except Exception as e:
            typer.echo(f"❌ Configuration validation failed: {e}")
            if debug:
                import traceback

                typer.echo(traceback.format_exc())
            sys.exit(1)

    async def _validate_all_configs():
        """Validate all configuration files."""
        typer.echo("🔍 Validating all configuration files...")

        config_manager = ConfigurationManager()
        available_configs = config_manager.list_available_configs()

        if not available_configs:
            typer.echo("📝 No configuration files found")
            return

        all_valid = True
        for config_path in available_configs:
            try:
                config = config_manager.load_config_file(config_path, validate=True)
                typer.echo(f"✅ {config_path}")
            except Exception as e:
                typer.echo(f"❌ {config_path}: {e}")
                all_valid = False

        if all_valid:
            typer.echo("✅ All configurations are valid!")
        else:
            typer.echo("❌ Some configurations have issues!")
            if fix:
                typer.echo("💡 Run 'daf validate config <file>' for individual files")

    async def _validate_single_config(config_path: Path):
        """Validate a single configuration file."""
        typer.echo(f"🔍 Validating configuration: {config_path}")

        config_manager = ConfigurationManager()
        validator = ConfigurationValidator()

        try:
            config = config_manager.load_config_file(config_path, validate=True)
            result = validator.validate_config(config)

            _print_validation_result("Configuration Validation", result, detailed=True)

            if result.is_valid:
                typer.echo("✅ Configuration is valid!")

                # Show config info
                info = config_manager.get_config_info(str(config_path))
                typer.echo("📋 Configuration info:")
                for key, value in info.items():
                    typer.echo(f"  {key}: {value}")

            else:
                typer.echo("❌ Configuration validation failed!")
                if fix:
                    typer.echo("💡 Fix suggestions:")
                    for suggestion in result.suggestions:
                        typer.echo(f"  • {suggestion}")

                sys.exit(1)

        except Exception as e:
            typer.echo(f"❌ Failed to load configuration: {e}")
            sys.exit(1)

    asyncio.run(run_config_validation())


@validate_command.command("installation")
def validate_installation():
    """Validate DAF and Metta installation."""
    from daf.core.logging import setup_logging

    setup_logging()

    async def run_installation_validation():
        try:
            typer.echo("🔍 Validating installation...")

            validator = InstallationValidator()

            # Validate all components
            system_result = await validator.validate_system()
            _print_validation_result("System", system_result)

            daf_result = await validator.validate_daf_installation()
            _print_validation_result("DAF Installation", daf_result)

            metta_result = await validator.validate_metta_installation()
            _print_validation_result("Metta AI", metta_result)

            env_result = await validator.validate_environment_setup()
            _print_validation_result("Environment", env_result)

            # Overall assessment
            all_results = [system_result, daf_result, metta_result, env_result]
            overall_valid = all(r.is_valid for r in all_results)

            typer.echo(f"\n{'=' * 50}")
            if overall_valid:
                typer.echo("✅ Installation validation passed!")
                typer.echo("🚀 DAF is ready to run experiments!")
            else:
                typer.echo("❌ Installation validation failed!")
                typer.echo("🔧 Run 'daf install daf' to fix installation issues")
            typer.echo("=" * 50)

        except Exception as e:
            typer.echo(f"❌ Installation validation failed: {e}")
            if debug:
                import traceback

                typer.echo(traceback.format_exc())
            sys.exit(1)

    asyncio.run(run_installation_validation())


@validate_command.command("metta")
def validate_metta():
    """Validate Metta AI installation and integration."""
    from daf.core.logging import setup_logging

    setup_logging()

    async def run_metta_validation():
        try:
            typer.echo("🔍 Validating Metta AI integration...")

            validator = InstallationValidator()
            result = await validator.validate_metta_installation()

            _print_validation_result("Metta AI Validation", result, detailed=True)

            if result.is_valid:
                typer.echo("✅ Metta AI integration is working!")

                # Show additional Metta info
                try:
                    import metta

                    metta_version = getattr(metta, "__version__", "unknown")
                    typer.echo(f"🤖 Metta AI version: {metta_version}")

                    import mettagrid

                    typer.echo("🎮 MettaGrid is available")

                    from metta.core.simulation import SimulationRunner

                    typer.echo("⚙️  Metta simulation engine is available")

                except ImportError as e:
                    typer.echo(f"⚠️  Some Metta components not available: {e}")

            else:
                typer.echo("❌ Metta AI validation failed!")
                typer.echo("🔧 Run 'daf install metta' to install Metta AI")

                if result.suggestions:
                    typer.echo("💡 Suggestions:")
                    for suggestion in result.suggestions:
                        typer.echo(f"  • {suggestion}")

                sys.exit(1)

        except Exception as e:
            typer.echo(f"❌ Metta validation failed: {e}")
            if debug:
                import traceback

                typer.echo(traceback.format_exc())
            sys.exit(1)

    asyncio.run(run_metta_validation())


def _print_validation_result(name: str, result: any, detailed: bool = False):
    """Print validation result in a nice format."""
    status = "✅" if result.is_valid else "❌"
    typer.echo(f"\n{status} {name}: {result.message}")

    if not result.is_valid:
        if result.issues:
            typer.echo("  Issues:")
            for issue in result.issues:
                typer.echo(f"    • {issue}")

        if detailed and result.suggestions:
            typer.echo("  Suggestions:")
            for suggestion in result.suggestions:
                typer.echo(f"    💡 {suggestion}")

    if detailed and result.metadata:
        typer.echo("  Details:")
        for key, value in result.metadata.items():
            typer.echo(f"    • {key}: {value}")
