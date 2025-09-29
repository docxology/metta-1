# rl.training.experience

**Module**: `rl.training.experience`

**Source**: `metta/rl/training/experience.py`

**Imports**:
- `metta.common.util.collections.duplicates`
- `tensordict.TensorDict`
- `torch`
- `torch.Tensor`
- `torchrl.data.Composite`
- `typing.Any`
- `typing.Dict`

## Classes (1)

### Experience

**Class**: `rl.training.experience.Experience`

**Constructor**: `Experience(self, total_agents: int, batch_size: int, bptt_horizon: int, minibatch_size: int, max_minibatch_size: int, experience_spec: Composite, device: Any)`

**Documentation**: Segmented tensor storage for RL experience with BPTT support.

**Methods**: 8

#### ready_for_training

**Signature**: `Experience.ready_for_training(self) -> bool`

**Documentation**: Check if buffer has enough data for training.

**Location**: line 86

#### store

**Signature**: `Experience.store(self, data_td: TensorDict, env_id: slice) -> Any`

**Documentation**: Store a batch of experience.

**Location**: line 90

#### reset_for_rollout

**Signature**: `Experience.reset_for_rollout(self) -> Any`

**Documentation**: Reset tracking variables for a new rollout.

**Location**: line 113

#### update

**Signature**: `Experience.update(self, indices: Tensor, data_td: TensorDict) -> Any`

**Documentation**: Update buffer with new data for given indices.

**Location**: line 120

#### reset_importance_sampling_ratios

**Signature**: `Experience.reset_importance_sampling_ratios(self) -> Any`

**Documentation**: Reset the importance sampling ratio to 1.0.

**Location**: line 124

#### stats

**Signature**: `Experience.stats(self) -> Dict`

**Documentation**: Get mean values of all tracked buffers.

**Location**: line 129

#### give_me_empty_md_td

**Signature**: `Experience.give_me_empty_md_td(self) -> TensorDict`

**Location**: line 162

#### from_losses

**Signature**: `Experience.from_losses(total_agents: int, batch_size: int, bptt_horizon: int, minibatch_size: int, max_minibatch_size: int, policy_experience_spec: Composite, losses: Dict, device: Any) -> Any`

**Documentation**: Create experience buffer with merged specs from policy and losses.

**Location**: line 170


