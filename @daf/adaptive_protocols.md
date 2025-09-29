# adaptive.protocols

**Module**: `adaptive.protocols`

**Source**: `metta/adaptive/protocols.py`

**Imports**:
- `typing.Any`
- `typing.Protocol`
- `typing.TYPE_CHECKING`
- `typing.runtime_checkable`

## Classes (6)

### ExperimentScheduler

**Class**: `adaptive.protocols.ExperimentScheduler`

**Constructor**: `ExperimentScheduler()`

**Documentation**: Simple scheduler protocol - gets runs, returns jobs to dispatch.

The scheduler contains all experiment logic. Examples:
- HyperparameterScheduler: Bayesian optimization
- ValidationScheduler: Multi-seed validation
- AblationScheduler: Component ablation study

**Methods**: 2

#### schedule

**Signature**: `ExperimentScheduler.schedule(self, runs: list, available_training_slots: int) -> list`

**Documentation**: Decide which jobs to dispatch next based on current run state and available resources.

Args:
    runs: All runs in the experiment (completed, running, failed)
    available_training_slots: How many LAUNCH_TRAINING jobs can be dispatched right now

Returns:
    Jobs to dispatch. LAUNCH_TRAINING jobs should not exceed available_training_slots.
    LAUNCH_EVAL jobs don't count against the limit and can always be dispatched.

**Location**: line 20

#### is_experiment_complete

**Signature**: `ExperimentScheduler.is_experiment_complete(self, runs: list) -> bool`

**Documentation**: Check if the experiment is finished and no more work will be scheduled.

Args:
    runs: All runs in the experiment (completed, running, failed)

Returns:
    True if experiment is complete and controller should terminate

**Location**: line 34


### Store

**Class**: `adaptive.protocols.Store`

**Constructor**: `Store()`

**Documentation**: Single source of truth for all run and experiment state.
All operations are synchronous with retry logic built in.

**Methods**: 3

#### init_run

**Signature**: `Store.init_run(self, run_id: str, group: Any = ..., tags: Any = ..., initial_summary: Any = ...) -> Any`

**Documentation**: Initialize a new run with optional initial summary data

**Location**: line 55

#### fetch_runs

**Signature**: `Store.fetch_runs(self, filters: dict) -> list`

**Documentation**: Fetch runs matching filter criteria, returns standardized RunInfo objects

**Location**: line 65

#### update_run_summary

**Signature**: `Store.update_run_summary(self, run_id, summary_update: dict) -> bool`

**Location**: line 69


### Dispatcher

**Class**: `adaptive.protocols.Dispatcher`

**Constructor**: `Dispatcher()`

**Documentation**: Handles the mechanics of starting and monitoring jobs.
All operations are synchronous with timeouts.

**Methods**: 1

#### dispatch

**Signature**: `Dispatcher.dispatch(self, job: Any) -> str`

**Documentation**: Start a job and return a dispatch ID

**Location**: line 80


### Optimizer

**Class**: `adaptive.protocols.Optimizer`

**Constructor**: `Optimizer()`

**Documentation**: Suggests hyperparameters for new jobs.

**Methods**: 1

#### suggest

**Signature**: `Optimizer.suggest(self, observations: list[dict], n_suggestions: int = ...) -> list[dict]`

**Documentation**: Suggest configurations for new jobs

**Location**: line 89


### SchedulerConfig

**Class**: `adaptive.protocols.SchedulerConfig`

**Constructor**: `SchedulerConfig()`

**Documentation**: Protocol for scheduler configuration objects expected by AdaptiveTool.

Must be serializable; at minimum provide a model_dump() -> dict interface
(e.g., Pydantic models). Dataclasses are also acceptable if converted prior
to passing into the tool.

**Methods**: 1

#### model_dump

**Signature**: `SchedulerConfig.model_dump(self) -> dict`

**Location**: line 103


### ExperimentState

**Class**: `adaptive.protocols.ExperimentState`

**Constructor**: `ExperimentState()`

**Documentation**: Optional typed state object for experiments (serializable, Pydantic-like).

Experiments that benefit from persistent or shared state (e.g., learning
progress, advanced optimizers) can define a dedicated state model.

**Methods**: 2

#### model_dump

**Signature**: `ExperimentState.model_dump(self) -> dict`

**Location**: line 115

#### model_validate

**Signature**: `ExperimentState.model_validate(cls, data: dict) -> Any`

**Location**: line 119


