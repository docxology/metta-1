# rl.stats

**Module**: `rl.stats`

**Source**: `metta/rl/stats.py`

**Imports**:
- `collections.defaultdict`
- `logging`
- `metta.common.wandb.context.WandbRun`
- `metta.eval.eval_request_config.EvalResults`
- `metta.rl.evaluate.upload_replay_html`
- `metta.rl.trainer_config.TrainerConfig`
- `metta.rl.training.Experience`
- `metta.rl.wandb.POLICY_EVALUATOR_EPOCH_METRIC`
- `metta.rl.wandb.POLICY_EVALUATOR_METRIC_PREFIX`
- `metta.rl.wandb.POLICY_EVALUATOR_STEP_METRIC`
- `metta.rl.wandb.setup_policy_evaluator_metrics`
- `mettagrid.profiling.stopwatch.Stopwatch`
- `mettagrid.util.dict_utils.unroll_nested_dict`
- `numpy`
- `torch`
- `typing.Any`

## Functions (5)

### accumulate_rollout_stats

**Signature**: `rl.stats.accumulate_rollout_stats(raw_infos: list, stats: dict) -> Any`

**Documentation**: Accumulate rollout statistics from info dictionaries.

**Location**: line 27

### filter_movement_metrics

**Signature**: `rl.stats.filter_movement_metrics(stats: dict) -> dict`

**Documentation**: Filter movement metrics to only keep core values, removing derived stats.

**Location**: line 61

### process_training_stats

**Signature**: `rl.stats.process_training_stats(raw_stats: dict, losses_stats: dict, experience: Experience, trainer_config: TrainerConfig) -> dict`

**Documentation**: Process training statistics into a clean format.

Args:
    raw_stats: Raw statistics dictionary (possibly with lists of values)
    losses_stats: Loss statistics dictionary
    experience: Experience object with stats() method
    trainer_config: Training configuration

Returns:
    Dictionary with processed statistics including:
    - mean_stats: Raw stats converted to means
    - losses_stats: Loss statistics
    - experience_stats: Experience buffer statistics
    - environment_stats: Environment-specific stats
    - overview: High-level metrics like average reward

**Location**: line 93

### compute_timing_stats

**Signature**: `rl.stats.compute_timing_stats(timer: Stopwatch, agent_step: int) -> dict`

**Documentation**: Compute timing statistics from a Stopwatch timer.

**Location**: line 150

### process_policy_evaluator_stats

**Signature**: `rl.stats.process_policy_evaluator_stats(policy_uri: str, eval_results: EvalResults, run: WandbRun, epoch: int, agent_step: int, should_finish_run: bool) -> Any`

**Location**: line 199

