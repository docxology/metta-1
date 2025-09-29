# eval.dashboard_data

**Module**: `eval.dashboard_data`

**Source**: `metta/eval/dashboard_data.py`

**Imports**:
- `__future__.annotations`
- `logging`
- `metta.sim.simulation_stats_db.SimulationStatsDB`
- `metta.utils.file.write_data`
- `mettagrid.config.Config`
- `pydantic.BaseModel`
- `typing.Dict`
- `typing.List`

## Classes (4)

### DashboardConfig

**Class**: `eval.dashboard_data.DashboardConfig`

**Constructor**: `DashboardConfig()`

### PolicyEvalMetric

**Class**: `eval.dashboard_data.PolicyEvalMetric`

**Constructor**: `PolicyEvalMetric()`

### PolicyEval

**Class**: `eval.dashboard_data.PolicyEval`

**Constructor**: `PolicyEval()`

### DashboardData

**Class**: `eval.dashboard_data.DashboardData`

**Constructor**: `DashboardData()`

## Functions (2)

### get_policy_eval_metrics

**Signature**: `eval.dashboard_data.get_policy_eval_metrics(db: SimulationStatsDB) -> List[PolicyEval]`

**Location**: line 39

### write_dashboard_data

**Signature**: `eval.dashboard_data.write_dashboard_data(dashboard_cfg: DashboardConfig)`

**Location**: line 136

