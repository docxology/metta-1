"""
DAF Validation System

Comprehensive validation system for DAF including:
- System requirements validation
- Configuration validation
- Installation validation
- Runtime validation
"""

import logging
import platform
from pathlib import Path
from typing import Any, Dict, List

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class ValidationResult(BaseModel):
    """Result of a validation check."""

    is_valid: bool = Field(..., description="Whether validation passed")
    message: str = Field(..., description="Validation message")
    issues: List[str] = Field(default_factory=list, description="Specific issues found")
    suggestions: List[str] = Field(default_factory=list, description="Suggested fixes")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

    @classmethod
    def combine(cls, results: List["ValidationResult"]) -> "ValidationResult":
        """Combine multiple validation results."""
        all_valid = all(r.is_valid for r in results)
        messages = [r.message for r in results if r.message]
        issues = [issue for r in results for issue in r.issues]
        suggestions = [suggestion for r in results for suggestion in r.suggestions]
        metadata = {}

        combined_message = "; ".join(messages) if messages else "Validation complete"

        return cls(
            is_valid=all_valid,
            message=combined_message,
            issues=issues,
            suggestions=suggestions,
            metadata=metadata,
        )


class SystemInfo(BaseModel):
    """System information for validation."""

    os: str = Field(..., description="Operating system")
    architecture: str = Field(..., description="System architecture")
    python_version: str = Field(..., description="Python version")
    cpu_count: int = Field(..., description="CPU core count")
    memory_gb: float = Field(..., description="System memory in GB")
    gpu_available: bool = Field(False, description="GPU availability")
    gpu_info: Dict[str, Any] = Field(default_factory=dict, description="GPU information")

    is_compatible: bool = Field(..., description="System compatibility")
    issues: List[str] = Field(default_factory=list, description="Compatibility issues")


class SystemValidator:
    """Validates system requirements for DAF."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def validate_system(self) -> ValidationResult:
        """Validate system requirements."""
        try:
            system_info = self._get_system_info()
            validation_results = []

            # Check Python version
            python_ok = self._validate_python_version(system_info.python_version)
            validation_results.append(python_ok)

            # Check system resources
            resources_ok = self._validate_system_resources(system_info)
            validation_results.append(resources_ok)

            # Check OS compatibility
            os_ok = self._validate_os_compatibility(system_info)
            validation_results.append(os_ok)

            return ValidationResult.combine(validation_results)

        except Exception as e:
            return ValidationResult(
                is_valid=False,
                message=f"System validation failed: {e}",
                issues=[str(e)],
            )

    def _get_system_info(self) -> SystemInfo:
        """Gather system information."""
        import sys

        # Basic system info
        os_info = f"{platform.system()} {platform.release()}"
        architecture = platform.machine()
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

        # CPU and memory info
        cpu_count = self._get_cpu_count()
        memory_gb = self._get_memory_gb()

        # GPU info
        gpu_available, gpu_info = self._get_gpu_info()

        # Compatibility assessment
        is_compatible, issues = self._assess_compatibility(os_info, python_version, memory_gb, gpu_available)

        return SystemInfo(
            os=os_info,
            architecture=architecture,
            python_version=python_version,
            cpu_count=cpu_count,
            memory_gb=memory_gb,
            gpu_available=gpu_available,
            gpu_info=gpu_info,
            is_compatible=is_compatible,
            issues=issues,
        )

    def _get_cpu_count(self) -> int:
        """Get number of CPU cores."""
        try:
            return len(self._run_command(["nproc"]).strip())
        except:
            try:
                import multiprocessing

                return multiprocessing.cpu_count()
            except:
                return 1

    def _get_memory_gb(self) -> float:
        """Get system memory in GB."""
        try:
            import psutil

            return round(psutil.virtual_memory().total / (1024**3), 1)
        except ImportError:
            # Fallback for systems without psutil
            try:
                with open("/proc/meminfo", "r") as f:
                    for line in f:
                        if line.startswith("MemTotal:"):
                            mem_kb = int(line.split()[1])
                            return round(mem_kb / (1024**2), 1)
            except:
                return 4.0  # Conservative default

    def _get_gpu_info(self) -> tuple[bool, Dict[str, Any]]:
        """Get GPU information."""
        try:
            import torch

            if torch.cuda.is_available():
                gpu_count = torch.cuda.device_count()
                gpu_info = {
                    "count": gpu_count,
                    "devices": [torch.cuda.get_device_name(i) for i in range(gpu_count)],
                }
                return True, gpu_info
        except ImportError:
            pass

        try:
            result = self._run_command(["nvidia-smi", "--query-gpu=name", "--format=csv,noheader,nounits"])
            gpu_names = result.strip().split("\n")
            if gpu_names:
                return True, {"count": len(gpu_names), "devices": gpu_names}
        except:
            pass

        return False, {}

    def _assess_compatibility(
        self, os: str, python_version: str, memory_gb: float, gpu_available: bool
    ) -> tuple[bool, List[str]]:
        """Assess overall system compatibility."""
        issues = []

        # Python version check
        major, minor, _ = map(int, python_version.split("."))
        if major < 3 or (major == 3 and minor < 11):
            issues.append(f"Python {python_version} is not supported, requires Python 3.11+")

        # Memory check
        if memory_gb < 4:
            issues.append(f"Insufficient memory: {memory_gb}GB, requires at least 4GB")

        # OS compatibility (basic check)
        if "Windows" in os and "10" not in os and "11" not in os:
            issues.append("Windows version may not be fully supported")

        return len(issues) == 0, issues

    def _validate_python_version(self, version: str) -> ValidationResult:
        """Validate Python version requirements."""
        major, minor, _ = map(int, version.split("."))

        if major < 3 or (major == 3 and minor < 11):
            return ValidationResult(
                is_valid=False,
                message=f"Python {version} not supported",
                issues=[f"Requires Python 3.11+, got {version}"],
                suggestions=["Install Python 3.11.7 or later", "Use pyenv or conda for version management"],
            )

        return ValidationResult(is_valid=True, message=f"Python {version} is compatible")

    def _validate_system_resources(self, system_info: SystemInfo) -> ValidationResult:
        """Validate system resources."""
        issues = []
        suggestions = []

        # Memory check
        if system_info.memory_gb < 4:
            issues.append(f"Low memory: {system_info.memory_gb}GB")
            suggestions.append("Consider using a machine with more RAM")

        # CPU check
        if system_info.cpu_count < 2:
            issues.append(f"Insufficient CPU cores: {system_info.cpu_count}")
            suggestions.append("Consider using a machine with more CPU cores")

        if issues:
            return ValidationResult(
                is_valid=False, message="System resources insufficient", issues=issues, suggestions=suggestions
            )

        return ValidationResult(is_valid=True, message="System resources adequate")

    def _validate_os_compatibility(self, system_info: SystemInfo) -> ValidationResult:
        """Validate OS compatibility."""
        os = system_info.os.lower()

        supported_os = ["linux", "darwin", "windows"]
        current_os = os.split()[0].lower()

        if not any(supported in current_os for supported in supported_os):
            return ValidationResult(
                is_valid=False,
                message=f"OS {system_info.os} may not be supported",
                issues=[f"Unsupported operating system: {system_info.os}"],
                suggestions=["Use Linux, macOS, or Windows 10/11"],
            )

        return ValidationResult(is_valid=True, message=f"OS {system_info.os} is supported")

    def _run_command(self, cmd: List[str]) -> str:
        """Run system command and return output."""
        import subprocess

        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout


class ConfigurationValidator:
    """Validates DAF configurations."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def validate_config(self, config: Any) -> ValidationResult:
        """Validate any configuration object."""
        try:
            # Try to validate as different config types
            validation_methods = [
                self._validate_simulation_config,
                self._validate_system_config,
                self._validate_profile_config,
            ]

            for method in validation_methods:
                try:
                    result = method(config)
                    if result.is_valid:
                        return result
                except Exception:
                    continue

            # If no specific validation succeeded, do basic validation
            return self._validate_basic_config(config)

        except Exception as e:
            return ValidationResult(is_valid=False, message=f"Configuration validation failed: {e}", issues=[str(e)])

    def _validate_simulation_config(self, config: Any) -> ValidationResult:
        """Validate simulation configuration."""
        if not hasattr(config, "name") or not config.name:
            return ValidationResult(
                is_valid=False,
                message="Simulation config missing name",
                issues=["Simulation configuration must have a name"],
            )

        if not hasattr(config, "environment"):
            return ValidationResult(
                is_valid=False,
                message="Simulation config missing environment",
                issues=["Simulation configuration must specify environment"],
            )

        # Validate environment configuration
        env = config.environment
        if hasattr(env, "num_agents") and env.num_agents < 1:
            return ValidationResult(
                is_valid=False, message="Invalid number of agents", issues=["Number of agents must be positive"]
            )

        return ValidationResult(is_valid=True, message="Simulation configuration is valid")

    def _validate_system_config(self, config: Any) -> ValidationResult:
        """Validate system configuration."""
        # Basic system config validation
        if hasattr(config, "python_version"):
            major, minor = map(int, config.python_version.split(".")[:2])
            if major < 3 or minor < 11:
                return ValidationResult(
                    is_valid=False,
                    message="Invalid Python version requirement",
                    issues=["System config requires Python 3.11+ in python_version field"],
                )

        return ValidationResult(is_valid=True, message="System configuration is valid")

    def _validate_profile_config(self, config: Any) -> ValidationResult:
        """Validate profile configuration."""
        if not hasattr(config, "name") or not config.name:
            return ValidationResult(
                is_valid=False, message="Profile config missing name", issues=["Profile configuration must have a name"]
            )

        return ValidationResult(is_valid=True, message="Profile configuration is valid")

    def _validate_basic_config(self, config: Any) -> ValidationResult:
        """Basic configuration validation."""
        if isinstance(config, dict):
            if not config:
                return ValidationResult(
                    is_valid=False, message="Configuration is empty", issues=["Configuration cannot be empty"]
                )

            return ValidationResult(is_valid=True, message="Basic configuration structure is valid")
        else:
            return ValidationResult(
                is_valid=True, message=f"Configuration object is valid (type: {type(config).__name__})"
            )


class InstallationValidator:
    """Validates DAF and Metta installations."""

    def __init__(self):
        self.system_validator = SystemValidator()
        self.config_validator = ConfigurationValidator()
        self.logger = logging.getLogger(__name__)

    async def validate_system(self) -> ValidationResult:
        """Validate system for DAF installation."""
        return self.system_validator.validate_system()

    async def validate_config(self, config: Any) -> ValidationResult:
        """Validate DAF configuration."""
        return self.config_validator.validate_config(config)

    async def validate_metta_installation(self) -> ValidationResult:
        """Validate Metta AI installation."""
        validation_results = []

        # Check if Metta modules can be imported
        try:
            import metta
            import mettagrid

            validation_results.append(ValidationResult(is_valid=True, message="Metta modules are importable"))
        except ImportError as e:
            validation_results.append(
                ValidationResult(
                    is_valid=False,
                    message="Metta modules not available",
                    issues=[f"Import error: {e}"],
                    suggestions=["Install Metta AI", "Check Python path"],
                )
            )

        # Check Metta version
        try:
            metta_version = getattr(metta, "__version__", "unknown")
            # Basic version check
            validation_results.append(
                ValidationResult(is_valid=True, message=f"Metta version {metta_version} detected")
            )
        except:
            pass

        return ValidationResult.combine(validation_results)

    async def validate_daf_installation(self) -> ValidationResult:
        """Validate DAF installation."""
        validation_results = []

        # Check DAF package structure
        daf_path = Path(__file__).parent.parent.parent / "src" / "daf"
        if daf_path.exists():
            validation_results.append(ValidationResult(is_valid=True, message="DAF package structure exists"))
        else:
            validation_results.append(
                ValidationResult(
                    is_valid=False,
                    message="DAF package structure missing",
                    suggestions=["Run installation script", "Check project structure"],
                )
            )

        # Check DAF can be imported
        try:
            import sys

            sys.path.insert(0, str(daf_path.parent.parent))
            import daf

            validation_results.append(ValidationResult(is_valid=True, message="DAF package is importable"))
        except ImportError as e:
            validation_results.append(
                ValidationResult(
                    is_valid=False,
                    message="DAF package import failed",
                    issues=[f"Import error: {e}"],
                    suggestions=["Check Python path", "Verify installation"],
                )
            )

        return ValidationResult.combine(validation_results)

    async def validate_environment_setup(self) -> ValidationResult:
        """Validate complete environment setup."""
        validations = [
            await self.validate_system(),
            await self.validate_daf_installation(),
            await self.validate_metta_installation(),
        ]

        return ValidationResult.combine(validations)
