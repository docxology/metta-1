# tools.eval_remote

**Module**: `tools.eval_remote`

**Source**: `metta/tools/eval_remote.py`

**Imports**:
- `gitta.get_git_hash_for_remote_task`
- `logging`
- `metta.app_backend.clients.stats_client.HttpStatsClient`
- `metta.app_backend.routes.eval_task_routes.TaskCreateRequest`
- `metta.common.tool.tool.Tool`
- `metta.common.util.constants.PROD_STATS_SERVER_URI`
- `metta.rl.checkpoint_manager.CheckpointManager`
- `metta.sim.simulation_config.SimulationConfig`
- `metta.sim.utils.get_or_create_policy_ids`
- `typing.Sequence`

## Classes (1)

### EvalRemoteTool

**Class**: `tools.eval_remote.EvalRemoteTool`

**Constructor**: `EvalRemoteTool()`

**Methods**: 1

#### invoke

**Signature**: `EvalRemoteTool.invoke(self, args: dict) -> Any`

**Location**: line 22


