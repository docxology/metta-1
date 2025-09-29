# rl.loss.sl_kickstarter

**Module**: `rl.loss.sl_kickstarter`

**Source**: `metta/rl/loss/sl_kickstarter.py`

**Imports**:
- `einops`
- `metta.agent.policy.Policy`
- `metta.rl.loss.Loss`
- `metta.rl.trainer_config.TrainerConfig`
- `metta.rl.training.ComponentContext`
- `mettagrid.config.Config`
- `pydantic.Field`
- `tensordict.TensorDict`
- `torch`
- `torch.Tensor`
- `torchrl.data.Composite`
- `torchrl.data.UnboundedContinuous`
- `typing.Any`

## Classes (2)

### SLKickstarterConfig

**Class**: `rl.loss.sl_kickstarter.SLKickstarterConfig`

**Constructor**: `SLKickstarterConfig()`

**Methods**: 1

#### create

**Signature**: `SLKickstarterConfig.create(self, policy: Policy, trainer_cfg: TrainerConfig, vec_env: Any, device: Any, instance_name: str, loss_config: Any)`

**Documentation**: Create SLKickstarter loss instance.

**Location**: line 23


### SLKickstarter

**Class**: `rl.loss.sl_kickstarter.SLKickstarter`

**Constructor**: `SLKickstarter(self, policy: Policy, trainer_cfg: TrainerConfig, vec_env: Any, device: Any, instance_name: str, loss_config: Any = ...)`

**Methods**: 2

#### get_experience_spec

**Signature**: `SLKickstarter.get_experience_spec(self) -> Composite`

**Location**: line 93

#### run_train

**Signature**: `SLKickstarter.run_train(self, shared_loss_data: TensorDict, context: ComponentContext, mb_idx: int) -> tuple`

**Location**: line 104


