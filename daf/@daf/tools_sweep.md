# tools.sweep

**Module**: `tools.sweep`

**Source**: `metta/tools/sweep.py`

**Imports**:
- `cogweb.cogweb_client.CogwebClient`
- `enum.StrEnum`
- `logging`
- `metta.adaptive.AdaptiveConfig`
- `metta.adaptive.AdaptiveController`
- `metta.adaptive.dispatcher.LocalDispatcher`
- `metta.adaptive.dispatcher.SkypilotDispatcher`
- `metta.adaptive.stores.WandbStore`
- `metta.common.tool.Tool`
- `metta.common.util.log_config.init_logging`
- `metta.common.wandb.context.WandbConfig`
- `metta.sweep.protein_config.ParameterConfig`
- `metta.sweep.protein_config.ProteinConfig`
- `metta.sweep.schedulers.batched_synced.BatchedSyncedOptimizingScheduler`
- `metta.sweep.schedulers.batched_synced.BatchedSyncedSchedulerConfig`
- `metta.tools.utils.auto_config.auto_stats_server_uri`
- `metta.tools.utils.auto_config.auto_wandb_config`
- `os`
- `pathlib.Path`
- `typing.Any`
- `typing.Optional`
- `uuid`

## Classes (2)

### DispatcherType

**Class**: `tools.sweep.DispatcherType`

**Constructor**: `DispatcherType()`

**Documentation**: Available dispatcher types for job execution.

### SweepTool

**Class**: `tools.sweep.SweepTool`

**Constructor**: `SweepTool()`

**Documentation**: Tool for Bayesian hyperparameter optimization using adaptive experiments.

This tool is specialized for hyperparameter tuning using Bayesian optimization.
For other experiment types (GPU sweeps, architecture comparisons), use the
AdaptiveController directly in Python code.

**Methods**: 1

#### invoke

**Signature**: `SweepTool.invoke(self, args: dict) -> Any`

**Documentation**: Execute the sweep.

**Location**: line 137


## Functions (1)

### create_on_eval_completed_hook

**Signature**: `tools.sweep.create_on_eval_completed_hook(metric_path: str)`

**Documentation**: Create an on_eval_completed hook that extracts the specified metric.

Args:
    metric_path: The path to the metric in the summary (e.g., "evaluator/eval_arena/score")

Returns:
    A hook function that extracts the metric and updates the observation.

**Location**: line 24

