# adaptive.adaptive_controller

**Module**: `adaptive.adaptive_controller`

**Source**: `metta/adaptive/adaptive_controller.py`

**Imports**:
- `adaptive_config.AdaptiveConfig`
- `datetime.datetime`
- `datetime.timezone`
- `logging`
- `metta.common.util.retry.retry_function`
- `models.JobDefinition`
- `models.JobStatus`
- `models.JobTypes`
- `models.RunInfo`
- `protocols.Dispatcher`
- `protocols.ExperimentScheduler`
- `protocols.Store`
- `time`
- `typing.Callable`
- `typing.Optional`
- `utils.make_monitor_table`

## Classes (1)

### AdaptiveController

**Class**: `adaptive.adaptive_controller.AdaptiveController`

**Constructor**: `AdaptiveController(self, experiment_id: str, scheduler: ExperimentScheduler, dispatcher: Dispatcher, store: Store, config: AdaptiveConfig)`

**Documentation**: Simple controller for adaptive experiments.

Everything is inlined in the main run() method for maximum clarity.

**Methods**: 1

#### run

**Signature**: `AdaptiveController.run(self, on_training_completed: Optional[Callable] = ..., on_eval_completed: Optional[Callable] = ..., on_job_dispatch: Optional[Callable] = ...) -> Any`

**Documentation**: Main adaptive experiment loop - everything inline.

**Location**: line 46


