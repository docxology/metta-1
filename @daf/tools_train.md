# tools.train

**Module**: `tools.train`

**Source**: `metta/tools/train.py`

**Imports**:
- `contextlib`
- `datetime.timedelta`
- `metta.agent.policies.vit.ViTDefaultConfig`
- `metta.agent.policy.Policy`
- `metta.agent.policy.PolicyArchitecture`
- `metta.app_backend.clients.stats_client.StatsClient`
- `metta.common.tool.Tool`
- `metta.common.util.heartbeat.record_heartbeat`
- `metta.common.util.log_config.getRankAwareLogger`
- `metta.common.util.log_config.init_logging`
- `metta.common.wandb.context.WandbConfig`
- `metta.common.wandb.context.WandbContext`
- `metta.rl.checkpoint_manager.CheckpointManager`
- `metta.rl.trainer.Trainer`
- `metta.rl.trainer_config.TorchProfilerConfig`
- `metta.rl.trainer_config.TrainerConfig`
- `metta.rl.training.Checkpointer`
- `metta.rl.training.CheckpointerConfig`
- `metta.rl.training.ContextCheckpointer`
- `metta.rl.training.ContextCheckpointerConfig`
- `metta.rl.training.DistributedHelper`
- `metta.rl.training.Evaluator`
- `metta.rl.training.EvaluatorConfig`
- `metta.rl.training.GradientReporter`
- `metta.rl.training.GradientReporterConfig`
- `metta.rl.training.Heartbeat`
- `metta.rl.training.Monitor`
- `metta.rl.training.ProgressLogger`
- `metta.rl.training.Scheduler`
- `metta.rl.training.SchedulerConfig`
- `metta.rl.training.StatsReporter`
- `metta.rl.training.StatsReporterConfig`
- `metta.rl.training.TorchProfiler`
- `metta.rl.training.TrainerComponent`
- `metta.rl.training.TrainingEnvironmentConfig`
- `metta.rl.training.Uploader`
- `metta.rl.training.UploaderConfig`
- `metta.rl.training.VectorizedTrainingEnvironment`
- `metta.rl.training.WandbAborter`
- `metta.rl.training.WandbAborterConfig`
- `metta.rl.training.WandbLogger`
- `metta.tools.utils.auto_config.auto_run_name`
- `metta.tools.utils.auto_config.auto_stats_server_uri`
- `metta.tools.utils.auto_config.auto_wandb_config`
- `os`
- `platform`
- `pydantic.Field`
- `pydantic.model_validator`
- `torch`
- `typing.Optional`

## Classes (1)

### TrainTool

**Class**: `tools.train.TrainTool`

**Constructor**: `TrainTool()`

**Methods**: 2

#### validate_fields

**Signature**: `TrainTool.validate_fields(self) -> Any`

**Location**: line 81

#### invoke

**Signature**: `TrainTool.invoke(self, args: dict) -> Any`

**Location**: line 91


