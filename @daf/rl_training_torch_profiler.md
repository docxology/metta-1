# rl.training.torch_profiler

**Module**: `rl.training.torch_profiler`

**Source**: `metta/rl/training/torch_profiler.py`

**Imports**:
- `gzip`
- `logging`
- `metta.common.wandb.context.WandbRun`
- `metta.rl.training.ComponentContext`
- `metta.rl.training.TrainerComponent`
- `metta.rl.utils.should_run`
- `metta.utils.file.http_url`
- `metta.utils.file.is_public_uri`
- `metta.utils.file.write_file`
- `os`
- `pathlib.Path`
- `shutil`
- `tempfile`
- `torch.profiler`
- `typing.Any`
- `typing.Optional`
- `wandb`

## Classes (2)

### TorchProfileSession

**Class**: `rl.training.torch_profiler.TorchProfileSession`

**Constructor**: `TorchProfileSession(self) -> Any`

**Documentation**: Context-managed wrapper around ``torch.profiler`` for periodic traces.

**Methods**: 1

#### on_epoch_end

**Signature**: `TorchProfileSession.on_epoch_end(self, epoch: int) -> Any`

**Location**: line 43


### TorchProfiler

**Class**: `rl.training.torch_profiler.TorchProfiler`

**Constructor**: `TorchProfiler(self) -> Any`

**Documentation**: Manages torch profiling during training.

**Methods**: 3

#### register

**Signature**: `TorchProfiler.register(self, context: ComponentContext) -> Any`

**Location**: line 162

#### on_epoch_end

**Signature**: `TorchProfiler.on_epoch_end(self, epoch: int) -> Any`

**Location**: line 188

#### on_training_complete

**Signature**: `TorchProfiler.on_training_complete(self) -> Any`

**Location**: line 192


