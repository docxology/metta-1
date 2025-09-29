# rl.training.component

**Module**: `rl.training.component`

**Source**: `metta/rl/training/component.py`

**Imports**:
- `enum.Enum`
- `logging`
- `metta.rl.training.ComponentContext`
- `pydantic.Field`
- `typing.Any`
- `typing.Optional`

## Classes (2)

### TrainerCallback

**Class**: `rl.training.component.TrainerCallback`

**Constructor**: `TrainerCallback()`

**Documentation**: Types of callbacks that can be invoked on trainer components.

### TrainerComponent

**Class**: `rl.training.component.TrainerComponent`

**Constructor**: `TrainerComponent(self, epoch_interval: int = ..., step_interval: int = ...) -> Any`

**Documentation**: Base class for training components.

**Methods**: 8

#### register

**Signature**: `TrainerComponent.register(self, context: ComponentContext) -> Any`

**Documentation**: Register this component with the trainer context.

**Location**: line 36

#### should_handle_step

**Signature**: `TrainerComponent.should_handle_step(self) -> bool`

**Documentation**: Return True when this component should receive a step callback.

**Location**: line 44

#### should_handle_epoch

**Signature**: `TrainerComponent.should_handle_epoch(self, epoch: int) -> bool`

**Documentation**: Return True when this component should receive an epoch callback.

**Location**: line 52

#### context

**Signature**: `TrainerComponent.context(self) -> ComponentContext`

**Documentation**: Return the trainer context associated with this component.

**Location**: line 61

#### on_step

**Signature**: `TrainerComponent.on_step(self, infos: list[dict]) -> Any`

**Documentation**: Called after each environment step.

**Location**: line 68

#### on_epoch_end

**Signature**: `TrainerComponent.on_epoch_end(self, epoch: int) -> Any`

**Documentation**: Called at the end of an epoch.

**Location**: line 72

#### on_training_complete

**Signature**: `TrainerComponent.on_training_complete(self) -> Any`

**Documentation**: Called when training completes successfully.

**Location**: line 76

#### on_failure

**Signature**: `TrainerComponent.on_failure(self) -> Any`

**Documentation**: Called when training fails.

**Location**: line 80


