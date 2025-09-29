# rl.rollout

**Module**: `rl.rollout`

**Source**: `metta/rl/rollout.py`

**Imports**:
- `logging`
- `mettagrid.profiling.stopwatch.Stopwatch`
- `numpy`
- `torch`
- `torch.Tensor`
- `typing.Any`

## Functions (2)

### get_observation

**Signature**: `rl.rollout.get_observation(vecenv: PufferlibVecEnv, device: Any, timer: Stopwatch) -> tuple`

**Documentation**: Get observations from vectorized environment and convert to tensors.

**Location**: line 18

### send_observation

**Signature**: `rl.rollout.send_observation(vecenv: PufferlibVecEnv, actions: Tensor, dtype_actions: Any, timer: Stopwatch) -> Any`

**Documentation**: Send actions back to the vectorized environment.

**Location**: line 41

