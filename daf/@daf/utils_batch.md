# utils.batch

**Module**: `utils.batch`

**Source**: `metta/utils/batch.py`

**Imports**:
- `typing.Tuple`

## Functions (2)

### calculate_batch_sizes

**Signature**: `utils.batch.calculate_batch_sizes(forward_pass_minibatch_target_size: int, num_agents: int, num_workers: int, async_factor: int) -> Tuple`

**Documentation**: Calculate target batch size, actual batch size, and number of environments.

**Location**: line 6

### calculate_prioritized_sampling_params

**Signature**: `utils.batch.calculate_prioritized_sampling_params(epoch: int, total_timesteps: int, batch_size: int, prio_alpha: float, prio_beta0: float) -> float`

**Documentation**: Calculate annealed beta for prioritized experience replay.

**Location**: line 24

