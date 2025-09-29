# rl.training.evaluator

**Module**: `rl.training.evaluator`

**Source**: `metta/rl/training/evaluator.py`

**Imports**:
- `gitta`
- `logging`
- `metta.app_backend.clients.stats_client.StatsClient`
- `metta.cogworks.curriculum.Curriculum`
- `metta.common.util.git_repo.REPO_SLUG`
- `metta.eval.eval_request_config.EvalResults`
- `metta.eval.eval_request_config.EvalRewardSummary`
- `metta.eval.eval_service.evaluate_policy`
- `metta.rl.evaluate.evaluate_policy_remote_with_checkpoint_manager`
- `metta.rl.evaluate.upload_replay_html`
- `metta.rl.training.TrainerComponent`
- `metta.sim.simulation_config.SimulationConfig`
- `metta.tools.utils.auto_config.auto_replay_dir`
- `mettagrid.config.Config`
- `pydantic.Field`
- `torch`
- `typing.Any`
- `typing.Optional`
- `uuid.UUID`

## Classes (3)

### EvaluatorConfig

**Class**: `rl.training.evaluator.EvaluatorConfig`

**Constructor**: `EvaluatorConfig()`

**Documentation**: Configuration for evaluation.

### NoOpEvaluator

**Class**: `rl.training.evaluator.NoOpEvaluator`

**Constructor**: `NoOpEvaluator(self) -> Any`

**Documentation**: No-op evaluator for when evaluation is disabled.

**Methods**: 3

#### get_latest_scores

**Signature**: `NoOpEvaluator.get_latest_scores(self) -> EvalRewardSummary`

**Location**: line 48

#### register

**Signature**: `NoOpEvaluator.register(self, context) -> Any`

**Location**: line 51

#### on_epoch_end

**Signature**: `NoOpEvaluator.on_epoch_end(self, epoch: int) -> Any`

**Location**: line 55


### Evaluator

**Class**: `rl.training.evaluator.Evaluator`

**Constructor**: `Evaluator(self, config: EvaluatorConfig, device: Any, system_cfg: Any, stats_client: Optional[StatsClient] = ...)`

**Documentation**: Manages policy evaluation.

**Methods**: 5

#### register

**Signature**: `Evaluator.register(self, context) -> Any`

**Location**: line 82

#### should_evaluate

**Signature**: `Evaluator.should_evaluate(self, epoch: int) -> bool`

**Location**: line 115

#### evaluate

**Signature**: `Evaluator.evaluate(self, policy_uri: Optional[str], curriculum: Any, epoch: int, agent_step: int, stats_epoch_id: Optional[UUID] = ...) -> EvalRewardSummary`

**Location**: line 121

#### get_latest_scores

**Signature**: `Evaluator.get_latest_scores(self) -> EvalRewardSummary`

**Location**: line 235

#### on_epoch_end

**Signature**: `Evaluator.on_epoch_end(self, epoch: int) -> Any`

**Location**: line 238


