# tools.sim

**Module**: `tools.sim`

**Source**: `metta/tools/sim.py`

**Imports**:
- `datetime.datetime`
- `json`
- `logging`
- `metta.app_backend.clients.stats_client.HttpStatsClient`
- `metta.app_backend.clients.stats_client.StatsClient`
- `metta.common.tool.Tool`
- `metta.common.util.constants.SOFTMAX_S3_BASE`
- `metta.common.wandb.context.WandbContext`
- `metta.eval.eval_request_config.EvalResults`
- `metta.eval.eval_service.evaluate_policy`
- `metta.rl.checkpoint_manager.CheckpointManager`
- `metta.rl.stats`
- `metta.sim.simulation_config.SimulationConfig`
- `metta.tools.utils.auto_config.auto_wandb_config`
- `metta.utils.uri.ParsedURI`
- `pydantic.Field`
- `sys`
- `torch`
- `typing.Sequence`
- `uuid`

## Classes (1)

### SimTool

**Class**: `tools.sim.SimTool`

**Constructor**: `SimTool()`

**Documentation**: Tool for running policy evaluations on simulation suites.

Can evaluate policies specified either by:
- run: Training run name (automatically resolves to latest S3 checkpoint)
- policy_uris: Explicit list of policy URIs (file://, s3://, etc.)

Usage examples:
    # Evaluate latest checkpoint from a training run
    SimTool(simulations=my_sims, run="my_experiment_2024")

    # Evaluate specific policy URIs
    SimTool(simulations=my_sims, policy_uris=["s3://bucket/path/policy:v10.pt"])

    # Can also be invoked with run parameter
    tool.invoke({"run": "my_experiment_2024"})

**Methods**: 1

#### invoke

**Signature**: `SimTool.invoke(self, args: dict) -> Any`

**Location**: line 110


