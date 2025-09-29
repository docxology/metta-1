# rl.wandb

**Module**: `rl.wandb`

**Source**: `metta/rl/wandb.py`

**Imports**:
- `logging`
- `metta.common.wandb.context.WandbRun`
- `torch.nn`
- `torch.nn.parameter.UninitializedParameter`

## Functions (3)

### setup_wandb_metrics

**Signature**: `rl.wandb.setup_wandb_metrics(wandb_run: WandbRun) -> Any`

**Documentation**: Set up wandb metric definitions for consistent tracking across runs.

**Location**: line 18

### setup_policy_evaluator_metrics

**Signature**: `rl.wandb.setup_policy_evaluator_metrics(wandb_run: WandbRun) -> Any`

**Documentation**: Set up metrics specific to policy evaluation.

**Location**: line 29

### log_model_parameters

**Signature**: `rl.wandb.log_model_parameters(policy: Any, wandb_run: WandbRun) -> Any`

**Documentation**: Log model parameter count to wandb summary.

**Location**: line 37

