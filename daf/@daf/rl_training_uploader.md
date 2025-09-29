# rl.training.uploader

**Module**: `rl.training.uploader`

**Source**: `metta/rl/training/uploader.py`

**Imports**:
- `contextlib.contextmanager`
- `logging`
- `metta.common.wandb.context.WandbRun`
- `metta.rl.checkpoint_manager.CheckpointManager`
- `metta.rl.training.DistributedHelper`
- `metta.rl.training.TrainerComponent`
- `metta.utils.file.local_copy`
- `mettagrid.config.Config`
- `pathlib.Path`
- `typing.Any`
- `typing.Iterator`
- `typing.Optional`
- `urllib.parse.urlparse`
- `wandb`

## Classes (2)

### UploaderConfig

**Class**: `rl.training.uploader.UploaderConfig`

**Constructor**: `UploaderConfig()`

**Documentation**: Configuration for policy uploading.

### Uploader

**Class**: `rl.training.uploader.Uploader`

**Constructor**: `Uploader(self) -> Any`

**Documentation**: Manages uploading policies to wandb and other destinations.

**Methods**: 3

#### update_wandb_run

**Signature**: `Uploader.update_wandb_run(self, wandb_run: Optional[WandbRun]) -> Any`

**Location**: line 45

#### on_epoch_end

**Signature**: `Uploader.on_epoch_end(self, epoch: int) -> Any`

**Location**: line 51

#### on_training_complete

**Signature**: `Uploader.on_training_complete(self) -> Any`

**Location**: line 54


