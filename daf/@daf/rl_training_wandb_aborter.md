# rl.training.wandb_aborter

**Module**: `rl.training.wandb_aborter`

**Source**: `metta/rl/training/wandb_aborter.py`

**Imports**:
- `__future__.annotations`
- `logging`
- `metta.common.wandb.context.WandbRun`
- `metta.common.wandb.utils.abort_requested`
- `metta.rl.training.ComponentContext`
- `metta.rl.training.TrainerComponent`
- `mettagrid.config.Config`

## Classes (2)

### WandbAborterConfig

**Class**: `rl.training.wandb_aborter.WandbAborterConfig`

**Constructor**: `WandbAborterConfig()`

**Documentation**: Configuration for wandb abort polling.

### WandbAborter

**Class**: `rl.training.wandb_aborter.WandbAborter`

**Constructor**: `WandbAborter(self) -> Any`

**Documentation**: Polls wandb for abort tags and stops training when detected.

**Methods**: 1

#### on_epoch_end

**Signature**: `WandbAborter.on_epoch_end(self, epoch: int) -> Any`

**Location**: line 36


