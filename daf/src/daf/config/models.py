"""
DAF Configuration Models

Pydantic models for DAF configuration system providing type safety
and validation for all configuration objects.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, field_validator, model_validator


class SystemConfig(BaseModel):
    """System-wide configuration settings."""

    python_version: str = Field("3.11.7", description="Required Python version")
    device: str = Field("auto", description="Compute device (auto, cpu, cuda)")
    parallel_workers: Union[int, str] = Field("auto", description="Number of parallel workers")
    max_memory_gb: Optional[float] = Field(None, description="Maximum memory usage in GB")
    timeout_seconds: int = Field(3600, description="Default timeout for operations")

    log_level: str = Field("INFO", description="Logging level")
    log_format: str = Field("structured", description="Log format style")
    log_output: str = Field("both", description="Log output destination")

    validation_strict: bool = Field(True, description="Enable strict validation")
    schema_validation: bool = Field(True, description="Enable schema validation")

    class Config:
        """Pydantic configuration."""

        validate_assignment = True


class MettaConfig(BaseModel):
    """Metta AI specific configuration."""

    installation_path: Optional[Path] = Field(None, description="Metta installation path")
    version_requirement: str = Field(">=0.1.0", description="Required Metta version")

    # Environment settings
    default_environment: str = Field("mettagrid", description="Default simulation environment")
    num_agents: int = Field(24, description="Default number of agents")
    map_size: List[int] = Field([50, 50], description="Default map dimensions")

    # Training settings
    default_timesteps: int = Field(1000000, description="Default training timesteps")
    default_learning_rate: float = Field(0.0003, description="Default learning rate")
    batch_size: int = Field(2048, description="Default batch size")

    # Curriculum settings
    curriculum_algorithm: str = Field("learning_progress", description="Curriculum learning algorithm")
    enable_curriculum: bool = Field(True, description="Enable curriculum learning")

    # Evaluation settings
    evaluation_frequency: int = Field(10000, description="Evaluation frequency")
    evaluation_episodes: int = Field(100, description="Episodes per evaluation")

    # Checkpoint settings
    checkpoint_frequency: int = Field(1000, description="Checkpoint save frequency")
    keep_checkpoints: int = Field(5, description="Number of checkpoints to keep")

    class Config:
        """Pydantic configuration."""

        validate_assignment = True


class SimulationEnvironmentConfig(BaseModel):
    """Configuration for simulation environment."""

    name: str = Field(..., description="Environment name")
    type: str = Field("mettagrid", description="Environment type")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Environment parameters")

    # Agent configuration
    num_agents: int = Field(24, description="Number of agents")
    agent_config: Dict[str, Any] = Field(default_factory=dict, description="Agent-specific settings")

    # Map/world configuration
    map_config: Dict[str, Any] = Field(default_factory=dict, description="Map configuration")
    world_size: List[int] = Field([50, 50], description="World dimensions")

    # Resource configuration
    resource_config: Dict[str, Any] = Field(default_factory=dict, description="Resource settings")

    class Config:
        """Pydantic configuration."""

        validate_assignment = True


class CurriculumConfig(BaseModel):
    """Curriculum learning configuration."""

    algorithm: str = Field("learning_progress", description="Curriculum algorithm")
    enable_buckets: bool = Field(True, description="Enable parameter bucketing")
    bucket_config: Dict[str, Any] = Field(default_factory=dict, description="Bucket configuration")

    # Learning progress settings
    learning_progress_config: Dict[str, Any] = Field(default_factory=dict, description="LP algorithm settings")

    # Task progression
    task_progression: List[str] = Field(default_factory=list, description="Task progression order")
    difficulty_ramp: Dict[str, Any] = Field(default_factory=dict, description="Difficulty progression")

    class Config:
        """Pydantic configuration."""

        validate_assignment = True


class TrainingConfig(BaseModel):
    """Training configuration."""

    total_timesteps: int = Field(1000000, description="Total training timesteps")
    learning_rate: float = Field(0.0003, description="Learning rate")
    batch_size: int = Field(2048, description="Training batch size")
    num_workers: int = Field(4, description="Number of training workers")

    # PPO settings
    ppo_epochs: int = Field(4, description="PPO epochs")
    ppo_clip_range: float = Field(0.2, description="PPO clip range")
    value_loss_coef: float = Field(0.5, description="Value loss coefficient")
    entropy_coef: float = Field(0.01, description="Entropy coefficient")

    # Optimization
    max_grad_norm: float = Field(0.5, description="Maximum gradient norm")
    use_mixed_precision: bool = Field(False, description="Use mixed precision training")

    class Config:
        """Pydantic configuration."""

        validate_assignment = True


class EvaluationConfig(BaseModel):
    """Evaluation configuration."""

    frequency: int = Field(10000, description="Evaluation frequency")
    num_episodes: int = Field(100, description="Episodes per evaluation")
    metrics: List[str] = Field(
        default_factory=lambda: ["reward", "success_rate", "episode_length"], description="Metrics to track"
    )

    # Checkpoint evaluation
    evaluate_checkpoints: bool = Field(True, description="Evaluate saved checkpoints")
    checkpoint_selection: str = Field("latest", description="Checkpoint selection strategy")

    # Output configuration
    save_replays: bool = Field(False, description="Save replay files")
    save_stats: bool = Field(True, description="Save statistics database")

    class Config:
        """Pydantic configuration."""

        validate_assignment = True


class SimulationConfig(BaseModel):
    """Main simulation configuration."""

    # Basic information
    name: str = Field(..., description="Simulation name")
    description: Optional[str] = Field(None, description="Simulation description")
    version: str = Field("1.0", description="Configuration version")

    # Environment configuration
    environment: SimulationEnvironmentConfig = Field(..., description="Simulation environment settings")

    # Learning configuration
    curriculum: Optional[CurriculumConfig] = Field(None, description="Curriculum learning settings")

    # Training configuration
    training: TrainingConfig = Field(..., description="Training parameters")

    # Evaluation configuration
    evaluation: EvaluationConfig = Field(..., description="Evaluation settings")

    # Output configuration
    output_dir: Optional[Path] = Field(None, description="Output directory")
    save_artifacts: bool = Field(True, description="Save simulation artifacts")
    artifact_types: List[str] = Field(
        default_factory=lambda: ["checkpoints", "logs", "metrics"], description="Types of artifacts to save"
    )

    # Runtime settings
    seed: Optional[int] = Field(None, description="Random seed")
    device: str = Field("auto", description="Compute device")
    parallel_execution: bool = Field(True, description="Enable parallel execution")

    # Metadata
    tags: List[str] = Field(default_factory=list, description="Configuration tags")
    created_at: Optional[str] = Field(None, description="Creation timestamp")
    author: Optional[str] = Field(None, description="Configuration author")

    class Config:
        """Pydantic configuration."""

        validate_assignment = True

    @field_validator("environment", mode="before")
    @classmethod
    def parse_environment(cls, v):
        """Parse environment configuration."""
        if isinstance(v, dict):
            return SimulationEnvironmentConfig(**v)
        return v

    @field_validator("curriculum", mode="before")
    @classmethod
    def parse_curriculum(cls, v):
        """Parse curriculum configuration."""
        if isinstance(v, dict) and v:
            return CurriculumConfig(**v)
        return v

    @field_validator("training", mode="before")
    @classmethod
    def parse_training(cls, v):
        """Parse training configuration."""
        if isinstance(v, dict):
            return TrainingConfig(**v)
        return v

    @field_validator("evaluation", mode="before")
    @classmethod
    def parse_evaluation(cls, v):
        """Parse evaluation configuration."""
        if isinstance(v, dict):
            return EvaluationConfig(**v)
        return v

    @model_validator(mode="after")
    def validate_configuration(self):
        """Validate overall configuration consistency."""
        # Validate device compatibility
        device = self.device
        if device == "cuda" and not self._is_cuda_available():
            # Fall back to CPU if CUDA not available
            self.device = "cpu"

        # Set default output directory if not specified
        if not self.output_dir:
            from daf.core.output import get_experiment_output_path

            self.output_dir = get_experiment_output_path(self.name)

        # Generate timestamp if not provided
        if not self.created_at:
            from datetime import datetime

            self.created_at = datetime.now().isoformat()

        return self

    @staticmethod
    def _is_cuda_available() -> bool:
        """Check if CUDA is available."""
        try:
            import torch

            return torch.cuda.is_available()
        except ImportError:
            return False


class ProfileConfig(BaseModel):
    """Configuration profile for different use cases."""

    name: str = Field(..., description="Profile name")
    description: str = Field(..., description="Profile description")
    base_config: str = Field(..., description="Base configuration to extend")

    # Profile-specific overrides
    overrides: Dict[str, Any] = Field(default_factory=dict, description="Configuration overrides")
    environment_overrides: Dict[str, Any] = Field(default_factory=dict, description="Environment overrides")
    training_overrides: Dict[str, Any] = Field(default_factory=dict, description="Training overrides")

    # Profile metadata
    use_case: str = Field("general", description="Intended use case")
    performance_target: str = Field("balanced", description="Performance target")
    resource_level: str = Field("medium", description="Resource requirements")

    class Config:
        """Pydantic configuration."""

        validate_assignment = True


class GlobalConfig(BaseModel):
    """Global DAF configuration."""

    system: SystemConfig = Field(..., description="System configuration")
    metta: MettaConfig = Field(..., description="Metta AI configuration")

    # Default configurations
    default_simulation: str = Field("arena_basic", description="Default simulation config")
    default_environment: str = Field("mettagrid", description="Default environment")

    # Global settings
    enable_validation: bool = Field(True, description="Enable global validation")
    enable_monitoring: bool = Field(True, description="Enable monitoring")
    enable_profiling: bool = Field(False, description="Enable performance profiling")

    # Paths
    config_dir: Path = Field(Path("configs"), description="Configuration directory")
    output_dir: Path = Field(Path("outputs"), description="Default output directory")
    data_dir: Path = Field(Path("data"), description="Data directory")

    class Config:
        """Pydantic configuration."""

        validate_assignment = True

    @field_validator("system", "metta", mode="before")
    @classmethod
    def parse_subconfigs(cls, v, info):
        """Parse sub-configurations."""
        field_name = info.field_name
        if isinstance(v, dict):
            if field_name == "system":
                return SystemConfig(**v)
            elif field_name == "metta":
                return MettaConfig(**v)
        return v
