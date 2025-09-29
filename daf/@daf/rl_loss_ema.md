# rl.loss.ema

**Module**: `rl.loss.ema`

**Source**: `metta/rl/loss/ema.py`

**Imports**:
- `copy`
- `metta.agent.policy.Policy`
- `metta.rl.loss.Loss`
- `metta.rl.training.ComponentContext`
- `metta.rl.utils.ensure_sequence_metadata`
- `mettagrid.config.Config`
- `pydantic.Field`
- `tensordict.TensorDict`
- `torch`
- `torch.Tensor`
- `torch.nn.functional`
- `typing.Any`

## Classes (2)

### EMAConfig

**Class**: `rl.loss.ema.EMAConfig`

**Constructor**: `EMAConfig()`

**Methods**: 1

#### create

**Signature**: `EMAConfig.create(self, policy: Policy, trainer_cfg: Any, vec_env: Any, device: Any, instance_name: str, loss_config: Any)`

**Documentation**: Create EMA loss instance.

**Location**: line 21


### EMA

**Class**: `rl.loss.ema.EMA`

**Constructor**: `EMA(self, policy: Policy, trainer_cfg: Any, vec_env: Any, device: Any, instance_name: str, loss_config: Any)`

**Methods**: 2

#### update_target_model

**Signature**: `EMA.update_target_model(self)`

**Documentation**: Update target model with exponential moving average

**Location**: line 65

#### run_train

**Signature**: `EMA.run_train(self, shared_loss_data: TensorDict, context: ComponentContext, mb_idx: int) -> tuple`

**Location**: line 73


