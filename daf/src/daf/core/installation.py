"""
DAF Installation Manager

Handles automated installation and setup of DAF and Metta AI components
with comprehensive validation and error recovery.
"""

import asyncio
import logging
import platform
import subprocess
from pathlib import Path
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from daf.config.configuration import ConfigurationManager
from daf.core.validation import SystemValidator, ValidationResult

logger = logging.getLogger(__name__)


class InstallationProgress(BaseModel):
    """Track installation progress."""

    current_step: str = Field("", description="Current installation step")
    completed_steps: List[str] = Field(default_factory=list, description="Completed steps")
    failed_steps: List[str] = Field(default_factory=list, description="Failed steps")
    warnings: List[str] = Field(default_factory=list, description="Installation warnings")


class InstallationManager:
    """
    Manages installation and setup of DAF and Metta AI.

    Provides automated, hands-off installation with validation,
    error recovery, and progress tracking.
    """

    def __init__(self, project_root: Path):
        """
        Initialize installation manager.

        Args:
            project_root: Root directory of the DAF project
        """
        self.project_root = Path(project_root)
        self.system_validator = SystemValidator()
        self.config_manager = ConfigurationManager()
        self.progress = InstallationProgress()
        self.logger = logging.getLogger(__name__)

    async def setup_uv(self) -> None:
        """Setup uv package manager if not present."""
        self.logger.info("Setting up uv package manager...")

        if self._is_uv_installed():
            self.logger.info("uv already installed")
            return

        # Install uv using the official installer
        try:
            self.logger.info("Installing uv...")
            install_cmd = ["curl", "-LsSf", "https://astral.sh/uv/install.sh", "|", "sh"]

            result = subprocess.run(" ".join(install_cmd), shell=True, check=True, capture_output=True, text=True)

            if result.returncode != 0:
                raise RuntimeError(f"uv installation failed: {result.stderr}")

            self.logger.info("uv installed successfully")

        except Exception as e:
            self.logger.error(f"Failed to install uv: {e}")
            raise RuntimeError("Could not install uv package manager")

    def _is_uv_installed(self) -> bool:
        """Check if uv is installed and available."""
        try:
            result = subprocess.run(["uv", "--version"], capture_output=True, text=True, check=True)
            return result.returncode == 0
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    async def install_dependencies(self, groups: List[str], upgrade: bool = False) -> None:
        """Install Python dependencies using uv."""
        self.logger.info(f"Installing dependencies: {groups}")

        cmd = ["uv", "sync"]
        if upgrade:
            cmd.append("--upgrade")

        # Add dependency groups
        for group in groups:
            cmd.extend([f"--group={group}"])

        try:
            result = subprocess.run(cmd, cwd=self.project_root, check=True, capture_output=True, text=True)

            if result.returncode != 0:
                raise RuntimeError(f"Dependency installation failed: {result.stderr}")

            self.logger.info("Dependencies installed successfully")

        except Exception as e:
            self.logger.error(f"Failed to install dependencies: {e}")
            raise RuntimeError("Dependency installation failed")

    async def install_metta_components(self) -> None:
        """Install and setup Metta AI components."""
        self.logger.info("Installing Metta AI components...")

        # Check if Metta is already available
        if self._is_metta_available():
            self.logger.info("Metta AI already available")
            return

        # Try different installation methods
        installation_methods = [
            self._install_metta_from_git,
            self._install_metta_from_pypi,
            self._install_metta_from_local,
        ]

        for method in installation_methods:
            try:
                await method()
                if self._is_metta_available():
                    self.logger.info("Metta AI installed successfully")
                    return
            except Exception as e:
                self.logger.warning(f"Installation method failed: {e}")
                continue

        raise RuntimeError("Could not install Metta AI components")

    async def _install_metta_from_git(self) -> None:
        """Install Metta from Git repository."""
        self.logger.info("Attempting to install Metta from Git...")

        metta_repo = "https://github.com/Metta-AI/metta.git"
        metta_path = self.project_root / "metta"

        if metta_path.exists():
            self.logger.info("Metta directory exists, updating...")
            await self._run_git_command(["pull"], cwd=metta_path)
        else:
            self.logger.info("Cloning Metta repository...")
            await self._run_git_command(["clone", "--depth=1", metta_repo, str(metta_path)])

        # Install Metta dependencies
        self.logger.info("Installing Metta dependencies...")
        await self._run_command(
            ["uv", "sync"], cwd=metta_path, env={"UV_PROJECT_ENVIRONMENT": str(self.project_root / ".venv")}
        )

    async def _install_metta_from_pypi(self) -> None:
        """Install Metta from PyPI."""
        self.logger.info("Attempting to install Metta from PyPI...")

        try:
            await self._run_command(["uv", "add", "metta-ai", "mettagrid"], cwd=self.project_root)
        except Exception as e:
            self.logger.warning(f"PyPI installation failed: {e}")
            raise

    async def _install_metta_from_local(self) -> None:
        """Try to use existing local Metta installation."""
        self.logger.info("Looking for local Metta installation...")

        # Look for metta in common locations
        search_paths = [
            Path.home() / "metta",
            Path("/usr/local/lib/metta"),
            Path("/opt/metta"),
        ]

        for path in search_paths:
            if self._is_metta_installed(path):
                self.logger.info(f"Found Metta installation at: {path}")
                # Could copy or symlink here
                return

        raise RuntimeError("No local Metta installation found")

    def _is_metta_available(self) -> bool:
        """Check if Metta AI components are available."""
        try:
            import metta
            import mettagrid

            return True
        except ImportError:
            return False

    def _is_metta_installed(self, path: Path) -> bool:
        """Check if Metta is installed at given path."""
        if not path.exists():
            return False

        # Check for key indicators
        indicators = [
            path / "metta" / "__init__.py",
            path / "pyproject.toml",
            path / "tools" / "run.py",
        ]

        return any(indicator.exists() for indicator in indicators)

    async def configure_metta(self, profile: str, non_interactive: bool = True) -> None:
        """Configure Metta AI installation."""
        self.logger.info(f"Configuring Metta AI with profile: {profile}")

        # Load DAF configuration
        config = self.config_manager.load_profile_config(profile)

        # Apply Metta-specific configuration
        metta_config = {
            "system.device": "cpu" if platform.system() == "Darwin" else "auto",
            "trainer.total_timesteps": 1000000,
            "env.num_agents": 24,
        }

        # Merge with profile overrides
        final_config = self.config_manager.merge_configs(metta_config, config.overrides)

        # Save Metta configuration
        metta_config_path = self.project_root / "metta_config.yaml"
        self.config_manager.save_config(final_config, metta_config_path)

        self.logger.info(f"Metta configuration saved to: {metta_config_path}")

    async def validate_metta_installation(self) -> ValidationResult:
        """Validate Metta AI installation."""
        self.logger.info("Validating Metta AI installation...")

        validation_results = []

        # Check if Metta modules can be imported
        try:
            import metta
            import mettagrid

            validation_results.append(ValidationResult(is_valid=True, message="Metta modules importable"))
        except ImportError as e:
            validation_results.append(ValidationResult(is_valid=False, message=f"Metta import failed: {e}"))

        # Check if Metta tools are available
        metta_tools = [
            self.project_root / "metta" / "tools" / "run.py",
        ]

        tools_available = all(tool.exists() for tool in metta_tools)
        validation_results.append(
            ValidationResult(
                is_valid=tools_available, message="Metta tools available" if tools_available else "Metta tools missing"
            )
        )

        # Test basic Metta functionality
        try:
            result = await self._run_command(
                ["python", "-c", "import metta; print('Metta version:', getattr(metta, '__version__', 'unknown'))"],
                cwd=self.project_root,
            )
            validation_results.append(ValidationResult(is_valid=True, message="Metta basic functionality works"))
        except Exception as e:
            validation_results.append(ValidationResult(is_valid=False, message=f"Metta functionality test failed: {e}"))

        return ValidationResult.combine(validation_results)

    async def validate_daf_installation(self) -> ValidationResult:
        """Validate DAF installation."""
        self.logger.info("Validating DAF installation...")

        validation_results = []

        # Check DAF package structure
        daf_path = self.project_root / "src" / "daf"
        if daf_path.exists():
            validation_results.append(ValidationResult(is_valid=True, message="DAF package structure exists"))
        else:
            validation_results.append(ValidationResult(is_valid=False, message="DAF package structure missing"))

        # Check configuration files
        config_files = [
            self.project_root / "configs" / "base" / "global.yaml",
            self.project_root / "pyproject.toml",
        ]

        configs_exist = all(cf.exists() for cf in config_files)
        validation_results.append(
            ValidationResult(
                is_valid=configs_exist,
                message="Configuration files present" if configs_exist else "Configuration files missing",
            )
        )

        # Check if DAF can be imported
        try:
            import sys

            sys.path.insert(0, str(self.project_root / "src"))
            import daf

            validation_results.append(ValidationResult(is_valid=True, message="DAF package importable"))
        except ImportError as e:
            validation_results.append(ValidationResult(is_valid=False, message=f"DAF import failed: {e}"))

        return ValidationResult.combine(validation_results)

    async def validate_metta_integration(self) -> ValidationResult:
        """Validate DAF-Metta integration."""
        self.logger.info("Validating DAF-Metta integration...")

        validation_results = []

        # Test basic integration
        try:
            from daf.core.engine import MettaEngine

            engine = MettaEngine()
            if engine.is_ready():
                validation_results.append(ValidationResult(is_valid=True, message="Metta engine ready"))
            else:
                validation_results.append(ValidationResult(is_valid=False, message="Metta engine not ready"))
        except Exception as e:
            validation_results.append(ValidationResult(is_valid=False, message=f"Metta engine creation failed: {e}"))

        return ValidationResult.combine(validation_results)

    async def run_smoke_tests(self) -> None:
        """Run basic smoke tests."""
        self.logger.info("Running smoke tests...")

        # Test basic import
        try:
            import sys

            sys.path.insert(0, str(self.project_root / "src"))
            import daf

            self.logger.info("✓ DAF import test passed")
        except ImportError as e:
            raise RuntimeError(f"DAF import test failed: {e}")

        # Test configuration loading
        try:
            config = self.config_manager.load_base_config()
            self.logger.info("✓ Configuration loading test passed")
        except Exception as e:
            raise RuntimeError(f"Configuration loading test failed: {e}")

        # Test Metta integration
        try:
            from daf.core.engine import MettaEngine

            engine = MettaEngine()
            if engine.is_ready():
                self.logger.info("✓ Metta integration test passed")
            else:
                self.logger.warning("⚠ Metta integration test inconclusive")
        except Exception as e:
            self.logger.warning(f"⚠ Metta integration test failed: {e}")

    async def setup_dev_tools(self) -> None:
        """Setup development tools."""
        self.logger.info("Setting up development tools...")

        # Setup pre-commit hooks
        await self.setup_pre_commit_hooks()

        # Setup IDE configuration
        await self.setup_ide_config()

        # Setup documentation tools
        await self.setup_docs_tools()

    async def setup_pre_commit_hooks(self) -> None:
        """Setup pre-commit hooks."""
        try:
            # Check if pre-commit is available
            result = await self._run_command(["pre-commit", "--version"])
            self.logger.info("Setting up pre-commit hooks...")

            # Install pre-commit hooks
            await self._run_command(["pre-commit", "install"], cwd=self.project_root)

            self.logger.info("✓ Pre-commit hooks installed")

        except Exception as e:
            self.logger.warning(f"⚠ Could not setup pre-commit hooks: {e}")

    async def setup_ide_config(self) -> None:
        """Setup IDE configuration files."""
        # Create VS Code configuration
        vscode_config = {
            "python.defaultInterpreterPath": str(self.project_root / ".venv" / "bin" / "python"),
            "python.terminal.activateEnvironment": True,
            "python.linting.enabled": True,
            "python.linting.ruffEnabled": True,
            "python.formatting.provider": "black",
            "editor.formatOnSave": True,
            "editor.codeActionsOnSave": {
                "source.fixAll.ruff": True,
            },
        }

        vscode_dir = self.project_root / ".vscode"
        vscode_dir.mkdir(exist_ok=True)

        import json

        settings_file = vscode_dir / "settings.json"
        with open(settings_file, "w") as f:
            json.dump(vscode_config, f, indent=2)

        self.logger.info("✓ IDE configuration created")

    async def setup_docs_tools(self) -> None:
        """Setup documentation tools."""
        try:
            # Check if mkdocs is available
            result = await self._run_command(["mkdocs", "--version"])

            # Create basic mkdocs configuration
            mkdocs_config = {
                "site_name": "DAF Documentation",
                "nav": [
                    {"Home": "index.md"},
                    {"API": "api.md"},
                    {"Configuration": "configuration.md"},
                ],
                "plugins": ["mkdocstrings"],
                "theme": "material",
            }

            import yaml

            mkdocs_file = self.project_root / "mkdocs.yml"
            with open(mkdocs_file, "w") as f:
                yaml.safe_dump(mkdocs_config, f, default_flow_style=False)

            self.logger.info("✓ Documentation tools configured")

        except Exception as e:
            self.logger.warning(f"⚠ Could not setup documentation tools: {e}")

    async def _run_command(
        self, cmd: List[str], cwd: Optional[Path] = None, env: Optional[Dict[str, str]] = None
    ) -> str:
        """Run a command asynchronously."""
        result = await asyncio.create_subprocess_exec(
            *cmd,
            cwd=cwd or self.project_root,
            env=env,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            text=True,
        )

        stdout, stderr = await result.communicate()

        if result.returncode != 0:
            raise RuntimeError(f"Command failed: {' '.join(cmd)}\nError: {stderr}")

        return stdout

    async def _run_git_command(self, cmd: List[str], cwd: Path) -> None:
        """Run git command."""
        git_cmd = ["git"] + cmd
        await self._run_command(git_cmd, cwd=cwd)
