# rl.training.component_context

**Module**: `rl.training.component_context`

**Source**: `metta/rl/training/component_context.py`

**Imports**:
- `__future__.annotations`
- `dataclasses.dataclass`
- `dataclasses.field`
- `metta.agent.policy.Policy`
- `metta.eval.eval_request_config.EvalRewardSummary`
- `metta.rl.training.Experience`
- `metta.rl.training.TrainingEnvironment`
- `mettagrid.profiling.memory_monitor.MemoryMonitor`
- `mettagrid.profiling.stopwatch.Stopwatch`
- `mettagrid.profiling.system_monitor.SystemMonitor`
- `torch.optim.Optimizer`
- `typing.Any`
- `typing.Callable`
- `typing.Dict`
- `typing.Optional`
- `typing.TYPE_CHECKING`

## Classes (3)

### TrainingEnvWindow

**Class**: `rl.training.component_context.TrainingEnvWindow`

**Constructor**: `TrainingEnvWindow()`

**Documentation**: Serializable view of the environment slice used for training.

**Methods**: 2

#### to_slice

**Signature**: `TrainingEnvWindow.to_slice(self) -> slice`

**Location**: line 31

#### from_slice

**Signature**: `TrainingEnvWindow.from_slice(cls, window: slice) -> Any`

**Location**: line 35


### TrainerState

**Class**: `rl.training.component_context.TrainerState`

**Constructor**: `TrainerState()`

**Documentation**: Serializable trainer state that can be checkpointed.

### ComponentContext

**Class**: `rl.training.component_context.ComponentContext`

**Constructor**: `ComponentContext(self) -> Any`

**Documentation**: Aggregated view of trainer state and runtime dependencies.

**Methods**: 15

#### epoch

**Signature**: `ComponentContext.epoch(self, value: int) -> Any`

**Location**: line 111

#### agent_step

**Signature**: `ComponentContext.agent_step(self, value: int) -> Any`

**Location**: line 119

#### training_env_id

**Signature**: `ComponentContext.training_env_id(self, value: Any) -> Any`

**Location**: line 130

#### latest_policy_uri_value

**Signature**: `ComponentContext.latest_policy_uri_value(self, value: Optional[str]) -> Any`

**Location**: line 145

#### latest_policy_uri

**Signature**: `ComponentContext.latest_policy_uri(self) -> Optional[str]`

**Location**: line 148

#### latest_saved_policy_epoch

**Signature**: `ComponentContext.latest_saved_policy_epoch(self, value: int) -> Any`

**Location**: line 162

#### latest_eval_scores

**Signature**: `ComponentContext.latest_eval_scores(self, value: Optional[EvalRewardSummary]) -> Any`

**Location**: line 173

#### latest_losses_stats

**Signature**: `ComponentContext.latest_losses_stats(self, value: Dict) -> Any`

**Location**: line 181

#### gradient_stats

**Signature**: `ComponentContext.gradient_stats(self, value: Dict) -> Any`

**Location**: line 189

#### update_gradient_stats

**Signature**: `ComponentContext.update_gradient_stats(self, stats: Dict) -> Any`

**Location**: line 192

#### reset_for_epoch

**Signature**: `ComponentContext.reset_for_epoch(self) -> Any`

**Location**: line 198

#### record_rollout

**Signature**: `ComponentContext.record_rollout(self, agent_steps: int, world_size: int) -> Any`

**Location**: line 201

#### advance_epoch

**Signature**: `ComponentContext.advance_epoch(self, epochs: int) -> Any`

**Location**: line 204

#### get_train_epoch_callable

**Signature**: `ComponentContext.get_train_epoch_callable(self) -> Callable`

**Location**: line 210

#### set_train_epoch_callable

**Signature**: `ComponentContext.set_train_epoch_callable(self, fn: Callable) -> Any`

**Location**: line 215


