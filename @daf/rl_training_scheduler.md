# rl.training.scheduler

**Module**: `rl.training.scheduler`

**Source**: `metta/rl/training/scheduler.py`

**Imports**:
- `logging`
- `math`
- `metta.rl.training.TrainerComponent`
- `mettagrid.config.Config`

## Classes (3)

### HyperparameterSchedulerConfig

**Class**: `rl.training.scheduler.HyperparameterSchedulerConfig`

**Constructor**: `HyperparameterSchedulerConfig()`

**Documentation**: Scheduler settings applied during training.

### SchedulerConfig

**Class**: `rl.training.scheduler.SchedulerConfig`

**Constructor**: `SchedulerConfig()`

**Documentation**: Component-specific scheduling configuration.

### Scheduler

**Class**: `rl.training.scheduler.Scheduler`

**Constructor**: `Scheduler(self, config: SchedulerConfig)`

**Documentation**: Manages hyperparameter scheduling.

**Methods**: 1

#### on_epoch_end

**Signature**: `Scheduler.on_epoch_end(self, epoch: int) -> Any`

**Documentation**: Update hyperparameters for the current training epoch.

**Location**: line 40


