# rl.training.wandb_logger

**Module**: `rl.training.wandb_logger`

**Source**: `metta/rl/training/wandb_logger.py`

**Imports**:
- `metta.common.wandb.context.WandbRun`
- `metta.rl.training.TrainerComponent`
- `metta.rl.wandb.log_model_parameters`
- `metta.rl.wandb.setup_wandb_metrics`
- `typing.Dict`

## Classes (1)

### WandbLogger

**Class**: `rl.training.wandb_logger.WandbLogger`

**Constructor**: `WandbLogger(self, wandb_run: WandbRun, epoch_interval: int = ...)`

**Documentation**: Logs core training metrics to wandb at epoch boundaries.

**Methods**: 4

#### register

**Signature**: `WandbLogger.register(self, context) -> Any`

**Location**: line 18

#### on_epoch_end

**Signature**: `WandbLogger.on_epoch_end(self, epoch: int) -> Any`

**Location**: line 23

#### on_training_complete

**Signature**: `WandbLogger.on_training_complete(self) -> Any`

**Location**: line 46

#### on_failure

**Signature**: `WandbLogger.on_failure(self) -> Any`

**Location**: line 49


