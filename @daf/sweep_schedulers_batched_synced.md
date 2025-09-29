# sweep.schedulers.batched_synced

**Module**: `sweep.schedulers.batched_synced`

**Source**: `metta/sweep/schedulers/batched_synced.py`

**Imports**:
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `logging`
- `metta.adaptive.models.JobDefinition`
- `metta.adaptive.models.JobStatus`
- `metta.adaptive.models.RunInfo`
- `metta.adaptive.utils.create_eval_job`
- `metta.adaptive.utils.create_training_job`
- `metta.adaptive.utils.generate_run_id`
- `mettagrid.config.Config`
- `pydantic.Field`
- `typing.Any`

## Classes (3)

### BatchedSyncedSchedulerConfig

**Class**: `sweep.schedulers.batched_synced.BatchedSyncedSchedulerConfig`

**Constructor**: `BatchedSyncedSchedulerConfig()`

**Documentation**: Configuration for batched synchronized scheduler.

### SchedulerState

**Class**: `sweep.schedulers.batched_synced.SchedulerState`

**Constructor**: `SchedulerState()`

**Documentation**: State tracking for the batched synchronized scheduler.

Tracks which runs are in training, evaluation, and completed states
to ensure proper synchronization and prevent duplicate job dispatches.

**Methods**: 2

#### model_dump

**Signature**: `SchedulerState.model_dump(self) -> dict`

**Documentation**: Serialize state to dictionary.

**Location**: line 52

#### model_validate

**Signature**: `SchedulerState.model_validate(cls, data: dict) -> Any`

**Documentation**: Deserialize state from dictionary.

**Location**: line 61


### BatchedSyncedOptimizingScheduler

**Class**: `sweep.schedulers.batched_synced.BatchedSyncedOptimizingScheduler`

**Constructor**: `BatchedSyncedOptimizingScheduler(self, config: BatchedSyncedSchedulerConfig, state: Any = ...)`

**Documentation**: Scheduler that generates batches of suggestions synchronously.

Key behaviors:
- Only generates new suggestions when ALL current runs (including evals) are complete
- Schedules evals for any runs with training complete and eval not yet started
- Generates up to `batch_size` training jobs at a time (bounded by available slots)
- Suggestions come from a stateless Optimizer; observations are read from run summaries
- Maintains stateful tracking of runs to prevent duplicate dispatches

**Methods**: 2

#### schedule

**Signature**: `BatchedSyncedOptimizingScheduler.schedule(self, runs: list[RunInfo], available_training_slots: int) -> list[JobDefinition]`

**Documentation**: Schedule next jobs based on current state and available resources.

**Location**: line 172

#### is_experiment_complete

**Signature**: `BatchedSyncedOptimizingScheduler.is_experiment_complete(self, runs: list[RunInfo]) -> bool`

**Location**: line 282


