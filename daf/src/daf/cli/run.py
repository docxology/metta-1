"""
DAF Run CLI Command

Provides commands for running DAF experiments and simulations.
"""

import asyncio
import sys
from pathlib import Path
from typing import Optional, List

import typer

from daf.core.simulation import SimulationRunner
from daf.core.configuration import ConfigurationManager

# Create run command group
run_command = typer.Typer(
    name="run",
    help="Run experiments and simulations",
    no_args_is_help=True,
)


@run_command.callback()
def run_callback(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
    debug: bool = typer.Option(False, "--debug", help="Enable debug mode"),
):
    """DAF experiment and simulation runner."""
    pass


@run_command.command("experiment")
def run_experiment(
    config: Path = typer.Argument(..., help="Experiment configuration file"),
    overrides: List[str] = typer.Option([], help="Configuration overrides (key=value)"),
    output_dir: Optional[Path] = typer.Option(None, help="Output directory"),
    validate: bool = typer.Option(True, help="Validate configuration"),
    dry_run: bool = typer.Option(False, help="Show configuration without running"),
):
    """Run a single experiment."""
    from daf.core.logging import setup_logging

    # Setup logging
    log_level = "DEBUG" if debug else "INFO"
    setup_logging(level=log_level)

    async def run_exp():
        try:
            typer.echo(f"🚀 Running experiment: {config}")

            # Load configuration
            config_manager = ConfigurationManager()
            experiment_config = config_manager.load_config_file(config, validate=validate)

            # Apply overrides
            override_dict = {}
            for override in overrides:
                if "=" in override:
                    key, value = override.split("=", 1)
                    override_dict[key.strip()] = value.strip()

            if override_dict:
                experiment_config = config_manager.apply_overrides(experiment_config, override_dict)

            # Set output directory
            if output_dir:
                experiment_config.output_dir = output_dir

            if dry_run:
                typer.echo("🔍 Dry run - showing configuration:")
                typer.echo(experiment_config.json(indent=2))
                return

            # Create and run simulation
            runner = SimulationRunner(experiment_config, validate=validate)

            typer.echo("⏳ Running simulation...")
            result = await runner.run()

            # Display results
            _display_experiment_results(result)

        except Exception as e:
            typer.echo(f"❌ Experiment failed: {e}")
            if debug:
                import traceback
                typer.echo(traceback.format_exc())
            sys.exit(1)

    asyncio.run(run_exp())


@run_command.command("batch")
def run_batch(
    configs: List[Path] = typer.Argument(..., help="Experiment configuration files"),
    overrides: List[str] = typer.Option([], help="Configuration overrides (key=value)"),
    output_dir: Optional[Path] = typer.Option(None, help="Base output directory"),
    parallel: bool = typer.Option(True, help="Run experiments in parallel"),
    validate: bool = typer.Option(True, help="Validate configurations"),
    dry_run: bool = typer.Option(False, help="Show configurations without running"),
):
    """Run multiple experiments in batch."""
    from daf.core.logging import setup_logging

    # Setup logging
    log_level = "DEBUG" if debug else "INFO"
    setup_logging(level=log_level)

    async def run_batch_exp():
        try:
            typer.echo(f"🚀 Running batch of {len(configs)} experiments")

            # Load and process configurations
            config_manager = ConfigurationManager()
            experiment_configs = []

            for config_path in configs:
                config = config_manager.load_config_file(config_path, validate=validate)
                experiment_configs.append(config)

            # Apply overrides
            override_dict = {}
            for override in overrides:
                if "=" in override:
                    key, value = override.split("=", 1)
                    override_dict[key.strip()] = value.strip()

            if override_dict:
                experiment_configs = [
                    config_manager.apply_overrides(config, override_dict)
                    for config in experiment_configs
                ]

            # Set output directories
            if output_dir:
                for i, config in enumerate(experiment_configs):
                    if not hasattr(config, 'output_dir') or not config.output_dir:
                        config.output_dir = output_dir / f"experiment_{i+1}"

            if dry_run:
                typer.echo("🔍 Dry run - showing configurations:")
                for i, config in enumerate(experiment_configs):
                    typer.echo(f"\n--- Experiment {i+1}: {config.name} ---")
                    typer.echo(config.json(indent=2))
                return

            # Run experiments
            if parallel:
                await _run_parallel_experiments(experiment_configs)
            else:
                await _run_sequential_experiments(experiment_configs)

        except Exception as e:
            typer.echo(f"❌ Batch run failed: {e}")
            if debug:
                import traceback
                typer.echo(traceback.format_exc())
            sys.exit(1)

    async def _run_parallel_experiments(configs):
        """Run experiments in parallel."""
        import asyncio

        typer.echo("⚡ Running experiments in parallel...")

        # Create tasks
        tasks = []
        runners = []

        for config in configs:
            runner = SimulationRunner(config, validate=False)  # Already validated
            runners.append(runner)
            task = asyncio.create_task(runner.run())
            tasks.append(task)

        # Wait for all tasks
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Display results
        for i, (runner, result) in enumerate(zip(runners, results)):
            if isinstance(result, Exception):
                typer.echo(f"❌ Experiment {i+1} failed: {result}")
            else:
                typer.echo(f"\n--- Experiment {i+1}: {runner.config.name} ---")
                _display_experiment_results(result)

    async def _run_sequential_experiments(configs):
        """Run experiments sequentially."""
        typer.echo("🔄 Running experiments sequentially...")

        for i, config in enumerate(configs):
            typer.echo(f"\n--- Running Experiment {i+1}/{len(configs)}: {config.name} ---")
            runner = SimulationRunner(config, validate=False)  # Already validated
            result = await runner.run()
            _display_experiment_results(result)

    asyncio.run(run_batch_exp())


@run_command.command("list")
def list_experiments(
    config_type: Optional[str] = typer.Option(None, help="Filter by configuration type"),
    show_details: bool = typer.Option(False, help="Show detailed information"),
):
    """List available experiment configurations."""
    from daf.core.logging import setup_logging

    setup_logging()

    try:
        config_manager = ConfigurationManager()
        available_configs = config_manager.list_available_configs(config_type)

        if not available_configs:
            typer.echo("📝 No experiment configurations found")
            typer.echo("💡 Create configurations in the configs/experiments/ directory")
            return

        typer.echo(f"📋 Available configurations ({len(available_configs)}):")
        typer.echo("")

        # Group by type
        configs_by_type = {}
        for config in available_configs:
            config_type = config.split('/')[0] if '/' in config else 'other'
            if config_type not in configs_by_type:
                configs_by_type[config_type] = []
            configs_by_type[config_type].append(config)

        for config_type, configs in configs_by_type.items():
            typer.echo(f"📁 {config_type.title()}:")
            for config in sorted(configs):
                if show_details:
                    try:
                        info = config_manager.get_config_info(config)
                        typer.echo(f"  • {config}")
                        typer.echo(f"    Description: {info.get('description', 'No description')}")
                        if info.get('environment'):
                            typer.echo(f"    Environment: {info['environment']}")
                        if info.get('num_agents'):
                            typer.echo(f"    Agents: {info['num_agents']}")
                    except Exception:
                        typer.echo(f"  • {config}")
                else:
                    typer.echo(f"  • {config}")
            typer.echo("")

        typer.echo("💡 Usage:")
        typer.echo("  daf run experiment <config-file>")
        typer.echo("  daf run batch <config-file-1> <config-file-2> ...")

    except Exception as e:
        typer.echo(f"❌ Failed to list configurations: {e}")
        sys.exit(1)


@run_command.command("interactive")
def run_interactive(
    config: Optional[Path] = typer.Option(None, help="Base experiment configuration"),
    num_agents: int = typer.Option(24, help="Number of agents"),
    timesteps: int = typer.Option(100000, help="Training timesteps"),
):
    """Run interactive simulation session."""
    from daf.core.logging import setup_logging

    setup_logging()

    typer.echo("🎮 Interactive Simulation Mode")
    typer.echo("This feature is not yet implemented.")
    typer.echo("Please use 'daf run experiment <config>' for now.")


def _display_experiment_results(result):
    """Display experiment results in a nice format."""
    from daf.core.simulation import SimulationResult

    if not isinstance(result, SimulationResult):
        typer.echo(f"📊 Result: {result}")
        return

    typer.echo(f"📊 Experiment: {result.experiment_name}")
    typer.echo(f"🏁 Status: {result.status.upper()}")

    if result.status == "success":
        typer.echo("✅ Simulation completed successfully!")
    elif result.status == "failed":
        typer.echo(f"❌ Simulation failed: {result.error_message}")
    else:
        typer.echo("⚠️  Simulation completed with issues")

    if result.metrics:
        typer.echo("📈 Metrics:"        for key, value in result.metrics.items():
            typer.echo(f"  • {key}: {value}")

    if result.artifacts:
        typer.echo("📁 Artifacts:"        for name, path in result.artifacts.items():
            typer.echo(f"  • {name}: {path}")

    typer.echo(f"⏱️  Execution time: {result.execution_time".2f"}s")

    if result.metadata:
        typer.echo("🔍 Additional info:"        for key, value in result.metadata.items():
            typer.echo(f"  • {key}: {value}")
