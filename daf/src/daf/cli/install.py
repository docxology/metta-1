"""
DAF Install CLI Command

Provides installation and setup commands for DAF and Metta AI.
"""

import asyncio
import sys
from pathlib import Path
from typing import Optional

import typer

from daf.core.installation import InstallationManager

# Create install command group
install_command = typer.Typer(
    name="install",
    help="Installation and setup commands",
    no_args_is_help=True,
)


@install_command.callback()
def install_callback(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
    debug: bool = typer.Option(False, "--debug", help="Enable debug mode"),
):
    """DAF installation and setup commands."""
    pass


@install_command.command("daf")
def install_daf(
    profile: str = typer.Option("research", help="Installation profile"),
    config: Optional[Path] = typer.Option(None, help="Configuration file"),
    clean: bool = typer.Option(False, help="Clean existing installation"),
    validate: bool = typer.Option(True, help="Run validation after installation"),
    dev: bool = typer.Option(False, help="Setup development environment"),
    non_interactive: bool = typer.Option(False, help="Run without prompts"),
):
    """Install and setup DAF framework."""
    from daf.core.logging import setup_logging

    # Setup logging
    log_level = "DEBUG" if debug else "INFO"
    setup_logging(level=log_level)

    # Import here to avoid circular imports
    from scripts.install import DAFInstaller

    # Create installer with provided arguments
    args = type(
        "Args",
        (),
        {
            "profile": profile,
            "config": config,
            "clean": clean,
            "validate": validate,
            "dev": dev,
            "non_interactive": non_interactive,
            "verbose": verbose,
        },
    )()

    installer = DAFInstaller(args)

    async def run_install():
        try:
            typer.echo(f"🚀 Installing DAF with profile: {profile}")
            result = await installer.run()

            if result == 0:
                typer.echo("✅ DAF installation completed successfully!")
                _print_post_install_info()
            else:
                typer.echo("❌ Installation failed!")
                sys.exit(result)

        except KeyboardInterrupt:
            typer.echo("\n👋 Installation cancelled by user")
            sys.exit(1)
        except Exception as e:
            typer.echo(f"❌ Installation failed: {e}")
            if debug:
                import traceback

                typer.echo(traceback.format_exc())
            sys.exit(1)

    # Run installation
    asyncio.run(run_install())


@install_command.command("metta")
def install_metta(
    path: Optional[Path] = typer.Option(None, help="Metta installation path"),
    force: bool = typer.Option(False, help="Force reinstallation"),
    validate: bool = typer.Option(True, help="Validate installation"),
):
    """Install Metta AI framework."""
    from daf.core.logging import setup_logging

    setup_logging()

    async def run_metta_install():
        project_root = Path.cwd()
        installer = InstallationManager(project_root)

        try:
            typer.echo("🤖 Installing Metta AI...")

            # Install Metta components
            await installer.install_metta_components()

            if validate:
                typer.echo("🔍 Validating Metta installation...")
                validation_result = await installer.validate_metta_installation()

                if validation_result.is_valid:
                    typer.echo("✅ Metta AI installation validated successfully!")
                else:
                    typer.echo("⚠️  Metta AI installation has issues:")
                    for issue in validation_result.issues:
                        typer.echo(f"  - {issue}")
                    if validation_result.suggestions:
                        typer.echo("💡 Suggestions:")
                        for suggestion in validation_result.suggestions:
                            typer.echo(f"  - {suggestion}")

            typer.echo("✅ Metta AI installation completed!")

        except Exception as e:
            typer.echo(f"❌ Metta installation failed: {e}")
            sys.exit(1)

    asyncio.run(run_metta_install())


@install_command.command("deps")
def install_dependencies(
    groups: str = typer.Option("core", help="Dependency groups to install"),
    upgrade: bool = typer.Option(False, help="Upgrade existing packages"),
    clean: bool = typer.Option(False, help="Clean installation"),
):
    """Install Python dependencies using uv."""
    from daf.core.logging import setup_logging

    setup_logging()

    async def run_deps_install():
        project_root = Path.cwd()
        installer = InstallationManager(project_root)

        # Parse groups
        group_list = [g.strip() for g in groups.split(",") if g.strip()]

        try:
            typer.echo(f"📦 Installing dependencies: {group_list}")

            await installer.install_dependencies(groups=group_list, upgrade=clean or upgrade)

            typer.echo("✅ Dependencies installed successfully!")

        except Exception as e:
            typer.echo(f"❌ Dependency installation failed: {e}")
            sys.exit(1)

    asyncio.run(run_deps_install())


@install_command.command("dev")
def setup_development(
    tools: bool = typer.Option(True, help="Setup development tools"),
    hooks: bool = typer.Option(True, help="Setup pre-commit hooks"),
    ide: bool = typer.Option(True, help="Setup IDE configuration"),
):
    """Setup development environment."""
    from daf.core.logging import setup_logging

    setup_logging()

    async def run_dev_setup():
        project_root = Path.cwd()
        installer = InstallationManager(project_root)

        try:
            typer.echo("🛠️  Setting up development environment...")

            if tools or hooks or ide:
                await installer.setup_dev_tools()

            if hooks:
                typer.echo("🔧 Setting up pre-commit hooks...")
                await installer.setup_pre_commit_hooks()

            if ide:
                typer.echo("💻 Setting up IDE configuration...")
                await installer.setup_ide_config()

            typer.echo("✅ Development environment setup completed!")

        except Exception as e:
            typer.echo(f"❌ Development setup failed: {e}")
            sys.exit(1)

    asyncio.run(run_dev_setup())


def _print_post_install_info():
    """Print information after successful installation."""
    typer.echo("\n" + "=" * 60)
    typer.echo("🎉 DAF Installation Completed!")
    typer.echo("=" * 60)
    typer.echo("\n📁 Project Location: .")
    typer.echo("\n🚀 Quick Start:")
    typer.echo("  daf run experiment configs/experiments/quick_test.yaml")
    typer.echo("  daf validate system")
    typer.echo("  daf info")
    typer.echo("\n📖 Documentation:")
    typer.echo("  See README.md for detailed usage")
    typer.echo("  Run 'daf --help' for command help")
    typer.echo("\n🔧 Development:")
    typer.echo("  Run 'daf validate system' to check status")
    typer.echo("  Edit configurations in configs/ directory")
    typer.echo("=" * 60)
