# rl.loss.dynamics

**Module**: `rl.loss.dynamics`

**Source**: `metta/rl/loss/dynamics.py`

**Imports**:
- `einops`
- `metta.agent.policy.Policy`
- `metta.rl.loss.Loss`
- `metta.rl.training.ComponentContext`
- `mettagrid.config.Config`
- `pydantic.Field`
- `tensordict.TensorDict`
- `torch`
- `torch.Tensor`
- `torch.nn.functional`
- `typing.Any`

## Classes (2)

### DynamicsConfig

**Class**: `rl.loss.dynamics.DynamicsConfig`

**Constructor**: `DynamicsConfig()`

**Methods**: 1

#### create

**Signature**: `DynamicsConfig.create(self, policy: Policy, trainer_cfg: Any, vec_env: Any, device: Any, instance_name: str, loss_config: Any)`

**Documentation**: Create Dynamics loss instance.

**Location**: line 21


### Dynamics

**Class**: `rl.loss.dynamics.Dynamics`

**Constructor**: `Dynamics()`

**Documentation**: The dynamics term in the Muesli loss.

**Methods**: 1

#### run_train

**Signature**: `Dynamics.run_train(self, shared_loss_data: TensorDict, context: ComponentContext, mb_idx: int) -> tuple`

**Location**: line 45


