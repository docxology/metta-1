# rl.loss.tl_kickstarter

**Module**: `rl.loss.tl_kickstarter`

**Source**: `metta/rl/loss/tl_kickstarter.py`

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
- `typing.Any`

## Classes (2)

### TLKickstarterConfig

**Class**: `rl.loss.tl_kickstarter.TLKickstarterConfig`

**Constructor**: `TLKickstarterConfig()`

**Methods**: 1

#### create

**Signature**: `TLKickstarterConfig.create(self, policy: Policy, trainer_cfg: TrainerConfig, vec_env: Any, device: Any, instance_name: str, loss_config: Any)`

**Documentation**: Create TLKickstarter loss instance.

**Location**: line 21


### TLKickstarter

**Class**: `rl.loss.tl_kickstarter.TLKickstarter`

**Constructor**: `TLKickstarter(self, policy: Policy, trainer_cfg: TrainerConfig, vec_env: Any, device: Any, instance_name: str, loss_config: Any = ...)`

**Methods**: 1

#### run_train

**Signature**: `TLKickstarter.run_train(self, shared_loss_data: TensorDict, context: ComponentContext, mb_idx: int) -> tuple`

**Location**: line 76


