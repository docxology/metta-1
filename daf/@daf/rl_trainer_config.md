# rl.trainer_config

**Module**: `rl.trainer_config`

**Source**: `metta/rl/trainer_config.py`

**Imports**:
- `metta.rl.loss.LossConfig`
- `metta.rl.training.HeartbeatConfig`
- `metta.rl.training.HyperparameterSchedulerConfig`
- `mettagrid.config.Config`
- `pydantic.ConfigDict`
- `pydantic.Field`
- `pydantic.model_validator`
- `typing.Any`
- `typing.ClassVar`
- `typing.Literal`
- `typing.Optional`

## Classes (4)

### OptimizerConfig

**Class**: `rl.trainer_config.OptimizerConfig`

**Constructor**: `OptimizerConfig()`

### InitialPolicyConfig

**Class**: `rl.trainer_config.InitialPolicyConfig`

**Constructor**: `InitialPolicyConfig()`

### TorchProfilerConfig

**Class**: `rl.trainer_config.TorchProfilerConfig`

**Constructor**: `TorchProfilerConfig()`

**Methods**: 2

#### enabled

**Signature**: `TorchProfilerConfig.enabled(self) -> bool`

**Location**: line 37

#### validate_fields

**Signature**: `TorchProfilerConfig.validate_fields(self) -> Any`

**Location**: line 41


### TrainerConfig

**Class**: `rl.trainer_config.TrainerConfig`

**Constructor**: `TrainerConfig()`

**Methods**: 1

#### validate_fields

**Signature**: `TrainerConfig.validate_fields(self) -> Any`

**Location**: line 77


