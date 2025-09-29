# eval.eval_request_config

**Module**: `eval.eval_request_config`

**Source**: `metta/eval/eval_request_config.py`

**Imports**:
- `mettagrid.config.Config`
- `pydantic.Field`

## Classes (2)

### EvalRewardSummary

**Class**: `eval.eval_request_config.EvalRewardSummary`

**Constructor**: `EvalRewardSummary()`

**Methods**: 3

#### avg_category_score

**Signature**: `EvalRewardSummary.avg_category_score(self) -> float`

**Location**: line 13

#### avg_simulation_score

**Signature**: `EvalRewardSummary.avg_simulation_score(self) -> float`

**Location**: line 17

#### to_wandb_metrics_format

**Signature**: `EvalRewardSummary.to_wandb_metrics_format(self) -> dict`

**Location**: line 20


### EvalResults

**Class**: `eval.eval_request_config.EvalResults`

**Constructor**: `EvalResults()`

