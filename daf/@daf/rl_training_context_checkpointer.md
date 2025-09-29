# rl.training.context_checkpointer

**Module**: `rl.training.context_checkpointer`

**Source**: `metta/rl/training/context_checkpointer.py`

**Imports**:
- `logging`
- `metta.rl.checkpoint_manager.CheckpointManager`
- `metta.rl.training.ComponentContext`
- `metta.rl.training.DistributedHelper`
- `metta.rl.training.TrainerComponent`
- `mettagrid.config.Config`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`

## Classes (2)

### ContextCheckpointerConfig

**Class**: `rl.training.context_checkpointer.ContextCheckpointerConfig`

**Constructor**: `ContextCheckpointerConfig()`

**Documentation**: Configuration for trainer state checkpointing.

### ContextCheckpointer

**Class**: `rl.training.context_checkpointer.ContextCheckpointer`

**Constructor**: `ContextCheckpointer(self) -> Any`

**Documentation**: Persist and restore optimizer/timing state alongside policy checkpoints.

**Methods**: 4

#### register

**Signature**: `ContextCheckpointer.register(self, context) -> Any`

**Location**: line 43

#### restore

**Signature**: `ContextCheckpointer.restore(self, context: ComponentContext) -> Any`

**Documentation**: Load trainer state if checkpoints exist and broadcast to all ranks.

**Location**: line 52

#### on_epoch_end

**Signature**: `ContextCheckpointer.on_epoch_end(self, epoch: int) -> Any`

**Location**: line 128

#### on_training_complete

**Signature**: `ContextCheckpointer.on_training_complete(self) -> Any`

**Location**: line 137


