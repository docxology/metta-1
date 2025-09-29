# eval.eval_stats_db

**Module**: `eval.eval_stats_db`

**Source**: `metta/eval/eval_stats_db.py`

**Imports**:
- `__future__.annotations`
- `contextlib.contextmanager`
- `math`
- `metta.rl.checkpoint_manager.CheckpointManager`
- `metta.sim.simulation_stats_db.SimulationStatsDB`
- `metta.utils.file.local_copy`
- `pandas`
- `pathlib.Path`
- `typing.Dict`
- `typing.Optional`

## Classes (1)

### EvalStatsDB

**Class**: `eval.eval_stats_db.EvalStatsDB`

**Constructor**: `EvalStatsDB(self, path: Path) -> Any`

**Methods**: 8

#### from_uri

**Signature**: `EvalStatsDB.from_uri(cls, path: str)`

**Documentation**: Download (if remote), open, and yield an EvalStatsDB.

**Location**: line 58

#### tables

**Signature**: `EvalStatsDB.tables(self) -> Dict`

**Location**: line 65

#### potential_samples_for_metric

**Signature**: `EvalStatsDB.potential_samples_for_metric(self, policy_key: str, policy_version: int, filter_condition: Any = ...) -> int`

**Location**: line 95

#### count_metric_agents

**Signature**: `EvalStatsDB.count_metric_agents(self, policy_key: str, policy_version: int, metric: str, filter_condition: Any = ...) -> int`

**Documentation**: How many samples actually recorded *metric* > 0.

**Location**: line 103

#### get_average_metric

**Signature**: `EvalStatsDB.get_average_metric(self, metric: str, policy_uri: str, filter_condition: Any = ...) -> Optional[float]`

**Documentation**: URI-native version to get average metric.

**Location**: line 167

#### get_std_metric

**Signature**: `EvalStatsDB.get_std_metric(self, metric: str, policy_uri: str, filter_condition: Any = ...) -> Optional[float]`

**Documentation**: URI-native version to get standard deviation metric.

**Location**: line 173

#### sample_count_uri

**Signature**: `EvalStatsDB.sample_count_uri(self, policy_uri: Optional[str] = ..., sim_name: Optional[str] = ..., sim_env: Optional[str] = ...) -> int`

**Documentation**: URI-native version to get sample count.

**Location**: line 179

#### simulation_scores

**Signature**: `EvalStatsDB.simulation_scores(self, policy_uri: str, metric: str) -> Dict`

**Documentation**: Return { (name,env) : normalized mean(metric) } for a policy URI.

**Location**: line 197


