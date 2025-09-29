# rl.training.core

**Module**: `rl.training.core`

**Source**: `metta/rl/training/core.py`

**Imports**:
- `logging`
- `metta.agent.policy.Policy`
- `metta.rl.loss.Loss`
- `metta.rl.training.ComponentContext`
- `metta.rl.training.Experience`
- `metta.rl.training.TrainingEnvironment`
- `mettagrid.config.Config`
- `numpy`
- `pydantic.ConfigDict`
- `tensordict.TensorDict`
- `torch`
- `typing.Any`

## Classes (2)

### RolloutResult

**Class**: `rl.training.core.RolloutResult`

**Constructor**: `RolloutResult()`

**Documentation**: Results from a rollout phase.

### CoreTrainingLoop

**Class**: `rl.training.core.CoreTrainingLoop`

**Constructor**: `CoreTrainingLoop(self, policy: Policy, experience: Experience, losses: dict, optimizer: Any, device: Any, context: ComponentContext)`

**Documentation**: Handles the core training loop with rollout and training phases.

**Methods**: 4

#### rollout_phase

**Signature**: `CoreTrainingLoop.rollout_phase(self, env: TrainingEnvironment, context: ComponentContext) -> RolloutResult`

**Documentation**: Perform rollout phase to collect experience.

Args:
    env: Vectorized environment to collect from
    context: Shared trainer context providing rollout state

Returns:
    RolloutResult with collected info

**Location**: line 64

#### training_phase

**Signature**: `CoreTrainingLoop.training_phase(self, context: ComponentContext, update_epochs: int, max_grad_norm: float = ...) -> tuple`

**Documentation**: Perform training phase on collected experience.

Args:
    context: Shared trainer context providing training state
    update_epochs: Number of epochs to train for
    max_grad_norm: Maximum gradient norm for clipping

Returns:
    Dictionary of loss statistics

**Location**: line 168

#### on_epoch_start

**Signature**: `CoreTrainingLoop.on_epoch_start(self, context: ComponentContext) -> Any`

**Documentation**: Called at the start of each epoch.

Args:
    context: Shared trainer context providing epoch state

**Location**: line 257

#### add_last_action_to_td

**Signature**: `CoreTrainingLoop.add_last_action_to_td(self, td: TensorDict, env: TrainingEnvironment) -> Any`

**Location**: line 266


