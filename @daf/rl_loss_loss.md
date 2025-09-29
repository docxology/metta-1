# rl.loss.loss

**Module**: `rl.loss.loss`

**Source**: `metta/rl/loss/loss.py`

**Imports**:
- `collections.OrderedDict`
- `collections.defaultdict`
- `copy`
- `dataclasses.dataclass`
- `dataclasses.field`
- `metta.agent.policy.Policy`
- `metta.rl.training.ComponentContext`
- `metta.rl.training.Experience`
- `metta.rl.training.TrainingEnvironment`
- `tensordict.TensorDict`
- `torch`
- `torch.Tensor`
- `torchrl.data.Composite`
- `typing.Any`
- `typing.Mapping`

## Classes (1)

### Loss

**Class**: `rl.loss.loss.Loss`

**Constructor**: `Loss()`

**Documentation**: Base class coordinating rollout and training behaviour for concrete losses.

**Methods**: 17

#### attach_context

**Signature**: `Loss.attach_context(self, context: ComponentContext) -> Any`

**Documentation**: Register the shared trainer context for this loss instance.

**Location**: line 49

#### get_experience_spec

**Signature**: `Loss.get_experience_spec(self) -> Composite`

**Documentation**: Optional extension of the experience replay buffer spec required by this loss.

**Location**: line 61

#### on_new_training_run

**Signature**: `Loss.on_new_training_run(self, context: Any = ...) -> Any`

**Documentation**: Called at the very beginning of a training epoch.

**Location**: line 67

#### on_rollout_start

**Signature**: `Loss.on_rollout_start(self, context: Any = ...) -> Any`

**Documentation**: Called before starting a rollout phase.

**Location**: line 71

#### rollout

**Signature**: `Loss.rollout(self, td: TensorDict, context: Any = ...) -> Any`

**Documentation**: Rollout step executed while experience buffer requests more data.

**Location**: line 76

#### run_rollout

**Signature**: `Loss.run_rollout(self, td: TensorDict, context: ComponentContext) -> Any`

**Documentation**: Override in subclasses to implement rollout logic.

**Location**: line 85

#### train

**Signature**: `Loss.train(self, shared_loss_data: TensorDict, context: Any, mb_idx: int) -> tuple`

**Documentation**: Training step executed while scheduler allows it.

**Location**: line 89

#### run_train

**Signature**: `Loss.run_train(self, shared_loss_data: TensorDict, context: ComponentContext, mb_idx: int) -> tuple`

**Documentation**: Override in subclasses to implement training logic.

**Location**: line 101

#### on_mb_end

**Signature**: `Loss.on_mb_end(self, context: Any, mb_idx: int) -> Any`

**Documentation**: Hook executed at the end of each minibatch.

**Location**: line 110

#### on_train_phase_end

**Signature**: `Loss.on_train_phase_end(self, context: Any = ...) -> Any`

**Documentation**: Hook executed after the training phase completes.

**Location**: line 114

#### save_loss_states

**Signature**: `Loss.save_loss_states(self, context: Any = ...) -> Any`

**Documentation**: Save loss states at the end of training (optional).

**Location**: line 118

#### stats

**Signature**: `Loss.stats(self) -> dict`

**Documentation**: Aggregate tracked statistics into mean values.

**Location**: line 158

#### zero_loss_tracker

**Signature**: `Loss.zero_loss_tracker(self) -> Any`

**Documentation**: Zero all values in the loss tracker.

**Location**: line 162

#### attach_replay_buffer

**Signature**: `Loss.attach_replay_buffer(self, experience: Experience) -> Any`

**Documentation**: Attach the replay buffer to the loss.

**Location**: line 180

#### register_state_attr

**Signature**: `Loss.register_state_attr(self, *names) -> Any`

**Documentation**: Register attributes that should be persisted in the loss state.

**Location**: line 189

#### state_dict

**Signature**: `Loss.state_dict(self) -> OrderedDict`

**Documentation**: Return a CPU-friendly snapshot of registered attributes.

**Location**: line 197

#### load_state_dict

**Signature**: `Loss.load_state_dict(self, state_dict: Mapping) -> tuple`

**Documentation**: Restore registered attributes from a state dictionary.

**Location**: line 206


