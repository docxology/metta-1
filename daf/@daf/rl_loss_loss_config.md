# rl.loss.loss_config

**Module**: `rl.loss.loss_config`

**Source**: `metta/rl/loss/loss_config.py`

**Imports**:
- `metta.agent.policy.Policy`
- `mettagrid.config.Config`
- `pydantic.Field`
- `torch`
- `typing.Any`
- `typing.Dict`
- `typing.TYPE_CHECKING`

## Classes (2)

### LossSchedule

**Class**: `rl.loss.loss_config.LossSchedule`

**Constructor**: `LossSchedule()`

### LossConfig

**Class**: `rl.loss.loss_config.LossConfig`

**Constructor**: `LossConfig()`

**Methods**: 2

#### model_post_init

**Signature**: `LossConfig.model_post_init(self, __context: Any) -> Any`

**Documentation**: Called after the model is initialized.

**Location**: line 21

#### init_losses

**Signature**: `LossConfig.init_losses(self, policy: Policy, trainer_cfg: Any, env: Any, device: Any)`

**Location**: line 32


