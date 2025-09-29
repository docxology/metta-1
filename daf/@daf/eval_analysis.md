# eval.analysis

**Module**: `eval.analysis`

**Source**: `metta/eval/analysis.py`

**Imports**:
- `fnmatch`
- `logging`
- `metta.eval.analysis_config.AnalysisConfig`
- `metta.eval.eval_stats_db.EvalStatsDB`
- `metta.rl.checkpoint_manager.CheckpointManager`
- `metta.utils.file.local_copy`
- `tabulate.tabulate`
- `typing.Dict`
- `typing.List`

## Functions (5)

### analyze

**Signature**: `eval.analysis.analyze(policy_uri: str, config: AnalysisConfig) -> Any`

**Location**: line 13

### get_available_metrics

**Signature**: `eval.analysis.get_available_metrics(stats_db: EvalStatsDB, policy_uri: str) -> List[str]`

**Location**: line 43

### filter_metrics

**Signature**: `eval.analysis.filter_metrics(available_metrics: List[str], patterns: List[str]) -> List[str]`

**Location**: line 58

### get_metrics_data

**Signature**: `eval.analysis.get_metrics_data(stats_db: EvalStatsDB, policy_uri: str, metrics: List[str], sim_name: Any = ...) -> Dict`

**Documentation**: Return {metric: {"mean": μ, "std": σ,
                 "count": K_recorded,
                 "samples": N_potential}}
    • μ, σ are normalized (missing values = 0).
    • K_recorded  – rows in policy_simulation_agent_metrics.
    • N_potential – total agent-episode pairs for that filter.

**Location**: line 67

### print_metrics_table

**Signature**: `eval.analysis.print_metrics_table(metrics_data: Dict, policy_uri: str) -> Any`

**Location**: line 104

