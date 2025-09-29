"""
DAF Main CLI Interface

Entry point for DAF command-line interface providing unified access
to all DAF functionality.
"""

import asyncio
import sys
from pathlib import Path
from typing import Optional

import typer

# Add src to path for imports
src_path = Path(__file__).parent.parent.parent
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from daf.cli.install import install_command
from daf.cli.run import run_command
from daf.cli.validate import validate_command
from daf.core.logging import setup_logging

# Create main CLI app
app = typer.Typer(
    name="daf",
    help="Distributed Agent Framework - Professional Metta AI fork",
    no_args_is_help=True,
    add_completion=False,
)

# Add subcommands
app.add_typer(install_command, name="install", help="Installation and setup commands")
app.add_typer(run_command, name="run", help="Run experiments and simulations")
app.add_typer(validate_command, name="validate", help="Validation and diagnostic commands")


@app.callback()
def main_callback(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
    debug: bool = typer.Option(False, "--debug", help="Enable debug mode"),
    config: Optional[Path] = typer.Option(None, "--config", help="Configuration file path"),
):
    """DAF - Distributed Agent Framework for multi-agent RL simulations."""
    # Setup logging based on verbosity
    log_level = "DEBUG" if debug else ("INFO" if verbose else "WARNING")
    setup_logging(level=log_level)

    # Store configuration context
    if config:
        # Could set global config context here
        pass


@app.command("version")
def version_command():
    """Show DAF version information."""
    from daf import get_version, get_info

    version = get_version()
    info = get_info()

    typer.echo(f"DAF (Distributed Agent Framework) v{version}")
    typer.echo(f"Author: {info['author']}")
    typer.echo(f"Description: {info['description']}")
    typer.echo(f"Package: {info['package']}")


@app.command("info")
def info_command():
    """Show DAF system information."""
from daf.config.configuration import ConfigurationManager

    typer.echo("DAF System Information")
    typer.echo("=" * 50)

    # System information
    typer.echo("\n📊 System:")
    from daf.core.validation import SystemValidator
    validator = SystemValidator()
    system_info = validator._get_system_info()
    typer.echo(f"  OS: {system_info.os}")
    typer.echo(f"  Architecture: {system_info.architecture}")
    typer.echo(f"  Python: {system_info.python_version}")
    typer.echo(f"  CPU Cores: {system_info.cpu_count}")
    typer.echo(f"  Memory: {system_info.memory_gb}GB")
    typer.echo(f"  GPU Available: {'Yes' if system_info.gpu_available else 'No'}")
    if system_info.gpu_available:
        typer.echo(f"  GPUs: {system_info.gpu_info.get('count', 'Unknown')}")

    # DAF information
    typer.echo("\n🔧 DAF:")
    config_manager = ConfigurationManager()
    try:
        base_config = config_manager.load_base_config()
        typer.echo(f"  Configuration: {base_config.system.log_level} logging")
        typer.echo(f"  Device: {base_config.system.device}")
        typer.echo(f"  Parallel Workers: {base_config.system.parallel_workers}")
    except Exception as e:
        typer.echo(f"  Status: Configuration not loaded ({e})")

    # Metta information
    typer.echo("\n🤖 Metta AI:")
    try:
        import metta
        metta_version = getattr(metta, "__version__", "unknown")
        typer.echo(f"  Version: {metta_version}")
        typer.echo("  Status: Available")
    except ImportError:
        typer.echo("  Status: Not installed"
    try:
        import mettagrid
        typer.echo("  MettaGrid: Available")
    except ImportError:
        typer.echo("  MettaGrid: Not available")

    # Configuration information
    typer.echo("\n⚙️  Configuration:")
    config_manager = ConfigurationManager()
    available_configs = config_manager.list_available_configs()
    typer.echo(f"  Available configs: {len(available_configs)}")

    config_types = {}
    for config in available_configs:
        config_type = config.split('/')[0] if '/' in config else 'other'
        config_types[config_type] = config_types.get(config_type, 0) + 1

    for config_type, count in config_types.items():
        typer.echo(f"  - {config_type}: {count} configs")


@app.command("status")
def status_command():
    """Show DAF system status."""
    from daf.core.validation import InstallationValidator

    typer.echo("DAF System Status")
    typer.echo("=" * 50)

    async def check_status():
        validator = InstallationValidator()

        # Check all components
        typer.echo("\n🔍 Checking system...")
        system_result = await validator.validate_system()
        _print_validation_result("System", system_result)

        typer.echo("\n🔧 Checking DAF installation...")
        daf_result = await validator.validate_daf_installation()
        _print_validation_result("DAF Installation", daf_result)

        typer.echo("\n🤖 Checking Metta AI...")
        metta_result = await validator.validate_metta_installation()
        _print_validation_result("Metta AI", metta_result)

        typer.echo("\n🌍 Checking environment...")
        env_result = await validator.validate_environment_setup()
        _print_validation_result("Environment", env_result)

        # Overall status
        all_results = [system_result, daf_result, metta_result, env_result]
        overall_valid = all(r.is_valid for r in all_results)

        typer.echo(f"\n{'='*50}")
        if overall_valid:
            typer.echo("✅ Overall Status: READY")
        else:
            typer.echo("❌ Overall Status: ISSUES DETECTED")
            typer.echo("\nRun 'daf validate system' for detailed diagnostics")
        typer.echo("=" * 50)

    def _print_validation_result(name: str, result: any):
        """Print validation result in a nice format."""
        status = "✅" if result.is_valid else "❌"
        typer.echo(f"  {status} {name}: {result.message}")
        if result.issues and not result.is_valid:
            for issue in result.issues:
                typer.echo(f"    - {issue}")
        if result.suggestions:
            for suggestion in result.suggestions:
                typer.echo(f"    💡 {suggestion}")

    # Run async status check
    asyncio.run(check_status())


def main():
    """Main entry point for DAF CLI."""
    try:
        app()
    except KeyboardInterrupt:
        typer.echo("\n👋 Goodbye!")
        sys.exit(0)
    except Exception as e:
        typer.echo(f"❌ Error: {e}", err=True)
        if "--debug" in sys.argv:
            import traceback
            typer.echo(traceback.format_exc(), err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
