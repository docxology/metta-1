# rl.training.gradient_reporter

**Module**: `rl.training.gradient_reporter`

**Source**: `metta/rl/training/gradient_reporter.py`

**Imports**:
- `logging`
- `metta.rl.training.TrainerComponent`
- `mettagrid.config.Config`
- `pydantic.Field`
- `torch`

## Classes (2)

### GradientReporterConfig

**Class**: `rl.training.gradient_reporter.GradientReporterConfig`

**Constructor**: `GradientReporterConfig()`

**Documentation**: Configuration for gradient statistics computation.

### GradientReporter

**Class**: `rl.training.gradient_reporter.GradientReporter`

**Constructor**: `GradientReporter(self, config: GradientReporterConfig)`

**Documentation**: Computes gradient statistics for monitoring.

**Methods**: 1

#### on_epoch_end

**Signature**: `GradientReporter.on_epoch_end(self, epoch: int) -> Any`

**Documentation**: Compute gradient statistics and stash on trainer.

**Location**: line 31


