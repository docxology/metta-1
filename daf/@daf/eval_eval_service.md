# eval.eval_service

**Module**: `eval.eval_service`

**Source**: `metta/eval/eval_service.py`

**Imports**:
- `logging`
- `metta.app_backend.clients.stats_client.StatsClient`
- `metta.common.util.collections.is_unique`
- `metta.common.util.heartbeat.record_heartbeat`
- `metta.eval.eval_request_config.EvalResults`
- `metta.eval.eval_request_config.EvalRewardSummary`
- `metta.eval.eval_stats_db.EvalStatsDB`
- `metta.rl.checkpoint_manager.CheckpointManager`
- `metta.sim.simulation.Simulation`
- `metta.sim.simulation.SimulationCompatibilityError`
- `metta.sim.simulation_config.SimulationConfig`
- `metta.sim.simulation_stats_db.SimulationStatsDB`
- `pathlib.Path`
- `torch`
- `uuid`

## Functions (2)

### evaluate_policy

**Signature**: `eval.eval_service.evaluate_policy() -> EvalResults`

**Documentation**: Evaluate one policy URI, merging all simulations into a single StatsDB.

**Location**: line 20

### extract_scores

**Signature**: `eval.eval_service.extract_scores(checkpoint_uri: str, simulations: list[SimulationConfig], stats_db: EvalStatsDB) -> EvalRewardSummary`

**Location**: line 107

