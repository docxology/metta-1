# rl.loss.ppo

**Module**: `rl.loss.ppo`

**Source**: `metta/rl/loss/ppo.py`

**Imports**:
- `metta.agent.policy.Policy`
- `metta.rl.advantage.compute_advantage`
- `metta.rl.advantage.normalize_advantage_distributed`
- `metta.rl.loss.Loss`
- `metta.rl.training.ComponentContext`
- `metta.rl.training.TrainingEnvironment`
- `metta.utils.batch.calculate_prioritized_sampling_params`
- `mettagrid.config.Config`
- `numpy`
- `pydantic.Field`
- `tensordict.NonTensorData`
- `tensordict.TensorDict`
- `torch`
- `torch.Tensor`
- `torchrl.data.Composite`
- `torchrl.data.MultiCategorical`
- `torchrl.data.UnboundedContinuous`
- `typing.Any`
- `typing.Tuple`

## Classes (4)

### PrioritizedExperienceReplayConfig

**Class**: `rl.loss.ppo.PrioritizedExperienceReplayConfig`

**Constructor**: `PrioritizedExperienceReplayConfig()`

### VTraceConfig

**Class**: `rl.loss.ppo.VTraceConfig`

**Constructor**: `VTraceConfig()`

### PPOConfig

**Class**: `rl.loss.ppo.PPOConfig`

**Constructor**: `PPOConfig()`

**Methods**: 1

#### create

**Signature**: `PPOConfig.create(self, policy: Policy, trainer_cfg: Any, env: TrainingEnvironment, device: Any, instance_name: str, loss_config: Any)`

**Documentation**: Points to the PPO class for initialization.

**Location**: line 68


### PPO

**Class**: `rl.loss.ppo.PPO`

**Constructor**: `PPO(self, policy: Policy, trainer_cfg: Any, env: TrainingEnvironment, device: Any, instance_name: str, loss_config: Any)`

**Documentation**: PPO loss with prioritized replay and V-trace tweaks.

**Methods**: 5

#### get_experience_spec

**Signature**: `PPO.get_experience_spec(self) -> Composite`

**Location**: line 118

#### run_rollout

**Signature**: `PPO.run_rollout(self, td: TensorDict, context: ComponentContext) -> Any`

**Location**: line 136

#### run_train

**Signature**: `PPO.run_train(self, shared_loss_data: TensorDict, context: ComponentContext, mb_idx: int) -> tuple`

**Documentation**: This is the PPO algorithm training loop.

**Location**: line 152

#### on_train_phase_end

**Signature**: `PPO.on_train_phase_end(self, context: ComponentContext) -> Any`

**Location**: line 201

#### compute_ppo_losses

**Signature**: `PPO.compute_ppo_losses(self, minibatch: TensorDict, new_logprob: Tensor, entropy: Tensor, newvalue: Tensor, importance_sampling_ratio: Tensor, adv: Tensor) -> Tuple`

**Documentation**: Compute PPO losses for policy and value functions.

**Location**: line 303


