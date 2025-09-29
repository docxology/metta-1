# rl.training.checkpointer

**Module**: `rl.training.checkpointer`

**Source**: `metta/rl/training/checkpointer.py`

**Imports**:
- `logging`
- `metta.agent.policy.Policy`
- `metta.agent.policy.PolicyArchitecture`
- `metta.rl.checkpoint_manager.CheckpointManager`
- `metta.rl.training.DistributedHelper`
- `metta.rl.training.EnvironmentMetaData`
- `metta.rl.training.TrainerComponent`
- `mettagrid.config.Config`
- `pydantic.Field`
- `typing.Optional`

## Classes (2)

### CheckpointerConfig

**Class**: `rl.training.checkpointer.CheckpointerConfig`

**Constructor**: `CheckpointerConfig()`

**Documentation**: Configuration for policy checkpointing.

### Checkpointer

**Class**: `rl.training.checkpointer.Checkpointer`

**Constructor**: `Checkpointer(self) -> Any`

**Documentation**: Manages policy checkpointing with distributed awareness and URI support.

**Methods**: 5

#### register

**Signature**: `Checkpointer.register(self, context) -> Any`

**Location**: line 42

#### load_or_create_policy

**Signature**: `Checkpointer.load_or_create_policy(self, env_metadata: EnvironmentMetaData, policy_architecture: PolicyArchitecture) -> Policy`

**Documentation**: Load the latest policy checkpoint or create a new policy.

**Location**: line 50

#### get_latest_policy_uri

**Signature**: `Checkpointer.get_latest_policy_uri(self) -> Optional[str]`

**Documentation**: Return the most recent checkpoint URI tracked by this component.

**Location**: line 84

#### on_epoch_end

**Signature**: `Checkpointer.on_epoch_end(self, epoch: int) -> Any`

**Location**: line 94

#### on_training_complete

**Signature**: `Checkpointer.on_training_complete(self) -> Any`

**Location**: line 103


