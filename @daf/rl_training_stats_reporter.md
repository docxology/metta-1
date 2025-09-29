# rl.training.stats_reporter

**Module**: `rl.training.stats_reporter`

**Source**: `metta/rl/training/stats_reporter.py`

**Imports**:
- `collections.defaultdict`
- `contextlib.nullcontext`
- `logging`
- `metta.app_backend.clients.stats_client.StatsClient`
- `metta.common.wandb.context.WandbRun`
- `metta.eval.eval_request_config.EvalRewardSummary`
- `metta.rl.stats.accumulate_rollout_stats`
- `metta.rl.stats.compute_timing_stats`
- `metta.rl.stats.process_training_stats`
- `metta.rl.training.component.TrainerComponent`
- `metta.rl.utils.should_run`
- `mettagrid.config.Config`
- `numpy`
- `pydantic.Field`
- `torch`
- `typing.Any`
- `typing.ContextManager`
- `typing.Optional`
- `typing.Protocol`
- `uuid.UUID`

## Classes (5)

### Timer

**Class**: `rl.training.stats_reporter.Timer`

**Constructor**: `Timer()`

### StatsReporterConfig

**Class**: `rl.training.stats_reporter.StatsReporterConfig`

**Constructor**: `StatsReporterConfig()`

**Documentation**: Configuration for stats reporting.

### StatsReporterState

**Class**: `rl.training.stats_reporter.StatsReporterState`

**Constructor**: `StatsReporterState()`

**Documentation**: State for statistics tracking.

### NoOpStatsReporter

**Class**: `rl.training.stats_reporter.NoOpStatsReporter`

**Constructor**: `NoOpStatsReporter(self)`

**Documentation**: No-op stats reporter for when stats are disabled.

**Methods**: 4

#### on_step

**Signature**: `NoOpStatsReporter.on_step(self, infos: list[dict]) -> Any`

**Location**: line 148

#### on_epoch_end

**Signature**: `NoOpStatsReporter.on_epoch_end(self, epoch: int) -> Any`

**Location**: line 151

#### on_training_complete

**Signature**: `NoOpStatsReporter.on_training_complete(self) -> Any`

**Location**: line 154

#### on_failure

**Signature**: `NoOpStatsReporter.on_failure(self) -> Any`

**Location**: line 157


### StatsReporter

**Class**: `rl.training.stats_reporter.StatsReporter`

**Constructor**: `StatsReporter(self, config: StatsReporterConfig, stats_client: Optional[StatsClient] = ..., wandb_run: Optional[WandbRun] = ...)`

**Documentation**: Aggregates and reports statistics to multiple backends.

**Methods**: 18

#### from_config

**Signature**: `StatsReporter.from_config(cls, config: Optional[StatsReporterConfig], stats_client: Optional[StatsClient] = ..., wandb_run: Optional[WandbRun] = ...) -> TrainerComponent`

**Documentation**: Create a StatsReporter from optional config, returning no-op if None.

**Location**: line 165

#### wandb_run

**Signature**: `StatsReporter.wandb_run(self, run: Any) -> Any`

**Location**: line 198

#### register

**Signature**: `StatsReporter.register(self, context) -> Any`

**Location**: line 201

#### state

**Signature**: `StatsReporter.state(self) -> StatsReporterState`

**Documentation**: Get the state for external access.

**Location**: line 230

#### process_rollout

**Signature**: `StatsReporter.process_rollout(self, raw_infos: list[dict]) -> Any`

**Location**: line 234

#### report_epoch

**Signature**: `StatsReporter.report_epoch(self, epoch: int, agent_step: int, losses_stats: dict, experience: Any, policy: Any, timer: Any, trainer_cfg: Any, optimizer: Any) -> Any`

**Location**: line 239

#### update_eval_scores

**Signature**: `StatsReporter.update_eval_scores(self, scores: EvalRewardSummary) -> Any`

**Location**: line 280

#### clear_rollout_stats

**Signature**: `StatsReporter.clear_rollout_stats(self) -> Any`

**Documentation**: Clear rollout statistics.

**Location**: line 285

#### clear_grad_stats

**Signature**: `StatsReporter.clear_grad_stats(self) -> Any`

**Documentation**: Clear gradient statistics.

**Location**: line 290

#### update_grad_stats

**Signature**: `StatsReporter.update_grad_stats(self, grad_stats: dict) -> Any`

**Location**: line 294

#### create_epoch

**Signature**: `StatsReporter.create_epoch(self, run_id: UUID, start_epoch: int, end_epoch: int, attributes: Any = ...) -> Optional[UUID]`

**Location**: line 297

#### finalize

**Signature**: `StatsReporter.finalize(self, status: str = ...) -> Any`

**Documentation**: Finalize stats reporting.

Args:
    status: Final status of the training run

**Location**: line 319

#### on_step

**Signature**: `StatsReporter.on_step(self, infos: Any) -> Any`

**Documentation**: Accumulate step infos.

Args:
    infos: Step information from environment

**Location**: line 333

#### get_latest_payload

**Signature**: `StatsReporter.get_latest_payload(self) -> Optional[dict]`

**Location**: line 341

#### on_epoch_end

**Signature**: `StatsReporter.on_epoch_end(self, epoch: int) -> Any`

**Documentation**: Report stats at epoch end.

Args:

**Location**: line 346

#### on_training_complete

**Signature**: `StatsReporter.on_training_complete(self) -> Any`

**Documentation**: Handle training completion.

Args:

**Location**: line 364

#### on_failure

**Signature**: `StatsReporter.on_failure(self) -> Any`

**Documentation**: Handle training failure.

Args:
    trainer: The trainer instance

**Location**: line 371

#### accumulate_infos

**Signature**: `StatsReporter.accumulate_infos(self, info: Any) -> Any`

**Documentation**: Accumulate rollout info dictionaries for later aggregation.

**Location**: line 383


## Functions (1)

### build_wandb_payload

**Signature**: `rl.training.stats_reporter.build_wandb_payload(processed_stats: dict, timing_info: dict, weight_stats: dict, grad_stats: dict, system_stats: dict, memory_stats: dict, parameters: dict, hyperparameters: dict, evals: EvalRewardSummary) -> dict`

**Documentation**: Create a flattened stats dictionary ready for wandb logging.

**Location**: line 44

