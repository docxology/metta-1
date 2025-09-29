# adaptive.utils

**Module**: `adaptive.utils`

**Source**: `metta/adaptive/utils.py`

**Imports**:
- `hashlib`
- `logging`
- `metta.adaptive.models.JobDefinition`
- `metta.adaptive.models.JobTypes`
- `metta.adaptive.models.RunInfo`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`

## Functions (7)

### make_monitor_table

**Signature**: `adaptive.utils.make_monitor_table(runs: list, title: str = ..., logger_prefix: str = ..., include_score: bool = ..., truncate_run_id: bool = ...) -> list[str]`

**Documentation**: Create a formatted table showing run status.

Args:
    runs: List of RunInfo objects to display
    title: Title for the table
    logger_prefix: Prefix to add to each log line (e.g., "[OptimizingScheduler]")
    include_score: Whether to include the score column
    truncate_run_id: Whether to truncate run IDs to just show trial numbers

Returns:
    List of formatted lines that can be logged

**Location**: line 13

### get_display_id

**Signature**: `adaptive.utils.get_display_id(run_id: str) -> str`

**Documentation**: Extract clean display ID from run ID.

Args:
    run_id: Full run ID (e.g., "experiment_name_trial_0001_a1b2c3")

Returns:
    Cleaned display ID (e.g., "trial_0001")

**Location**: line 88

### build_eval_overrides

**Signature**: `adaptive.utils.build_eval_overrides(run_id: str, experiment_id: str, stats_server_uri: Optional[str] = ..., additional_overrides: Optional[Dict] = ...) -> Dict`

**Documentation**: Build evaluation override parameters.

Args:
    run_id: The run ID for WandB tracking
    experiment_id: The experiment ID for grouping
    stats_server_uri: Optional stats server URI
    additional_overrides: Optional additional overrides to merge

Returns:
    Dictionary of evaluation overrides

**Location**: line 104

### build_train_overrides

**Signature**: `adaptive.utils.build_train_overrides(stats_server_uri: Optional[str] = ..., additional_overrides: Optional[Dict] = ...) -> Dict`

**Documentation**: Build training override parameters.

Args:
    stats_server_uri: Optional stats server URI
    additional_overrides: Optional additional overrides to merge

Returns:
    Dictionary of training overrides

**Location**: line 135

### create_eval_job

**Signature**: `adaptive.utils.create_eval_job(run_id: str, experiment_id: str, recipe_module: str, eval_entrypoint: str, stats_server_uri: Optional[str] = ..., eval_overrides: Optional[Dict] = ...) -> Any`

**Documentation**: Create an evaluation job definition.

Args:
    run_id: The run ID to evaluate
    experiment_id: The experiment ID for grouping
    recipe_module: Module containing the evaluation function
    eval_entrypoint: Name of the evaluation function
    stats_server_uri: Optional stats server URI
    eval_args: Optional positional arguments for evaluation
    eval_overrides: Optional additional overrides

Returns:
    JobDefinition for evaluation

**Location**: line 159

### create_training_job

**Signature**: `adaptive.utils.create_training_job(run_id: str, experiment_id: str, recipe_module: str, train_entrypoint: str, gpus: int = ..., nodes: int = ..., stats_server_uri: Optional[str] = ..., train_overrides: Optional[Dict] = ...) -> Any`

**Documentation**: Create a training job definition.

Args:
    run_id: The unique run ID
    experiment_id: The experiment ID for grouping
    recipe_module: Module containing the training function
    train_entrypoint: Name of the training function
    config: Hyperparameter configuration from optimizer
    gpus: Number of GPUs per job
    stats_server_uri: Optional stats server URI
    train_overrides: Optional additional overrides

Returns:
    JobDefinition for training

**Location**: line 200

### generate_run_id

**Signature**: `adaptive.utils.generate_run_id(experiment_id: str, trial_num: int) -> str`

**Documentation**: Generate a standardized run ID with hash to avoid collisions.

Args:
    experiment_id: The experiment identifier
    trial_num: The trial number (1-based)

Returns:
    Formatted run ID like "experiment_id_trial_0001_a1b2c3"

**Location**: line 243

