# rl.evaluate

**Module**: `rl.evaluate`

**Source**: `metta/rl/evaluate.py`

**Imports**:
- `__future__.annotations`
- `logging`
- `metta.app_backend.clients.stats_client.StatsClient`
- `metta.app_backend.routes.eval_task_routes.TaskCreateRequest`
- `metta.app_backend.routes.eval_task_routes.TaskResponse`
- `metta.common.util.collections.remove_none_keys`
- `metta.common.util.constants.METTASCOPE_REPLAY_URL`
- `metta.common.wandb.context.WandbRun`
- `metta.rl.checkpoint_manager.CheckpointManager`
- `metta.sim.simulation_config.SimulationConfig`
- `metta.sim.utils.get_or_create_policy_ids`
- `typing.Any`
- `typing.TYPE_CHECKING`
- `uuid`
- `wandb`

## Functions (2)

### evaluate_policy_remote_with_checkpoint_manager

**Signature**: `rl.evaluate.evaluate_policy_remote_with_checkpoint_manager(policy_uri: str, simulations: list[SimulationConfig], stats_epoch_id: Any, stats_client: Any, wandb_run: Any, evaluation_cfg: Any) -> Any`

**Documentation**: Create a remote evaluation task using a policy URI.

**Location**: line 27

### upload_replay_html

**Signature**: `rl.evaluate.upload_replay_html(replay_urls: dict, agent_step: int, epoch: int, wandb_run: WandbRun, step_metric_key: Any = ..., epoch_metric_key: Any = ...) -> Any`

**Documentation**: Upload organized replay HTML links to wandb.

**Location**: line 71

