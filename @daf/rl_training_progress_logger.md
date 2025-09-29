# rl.training.progress_logger

**Module**: `rl.training.progress_logger`

**Source**: `metta/rl/training/progress_logger.py`

**Imports**:
- `__future__.annotations`
- `logging`
- `metta.rl.training.TrainerComponent`
- `os`
- `rich.console.Console`
- `rich.table.Table`
- `sys`
- `typing.Dict`
- `typing.Optional`

## Classes (1)

### ProgressLogger

**Class**: `rl.training.progress_logger.ProgressLogger`

**Constructor**: `ProgressLogger(self) -> Any`

**Documentation**: Master-only component that logs epoch progress.

**Methods**: 2

#### register

**Signature**: `ProgressLogger.register(self, context) -> Any`

**Location**: line 172

#### on_epoch_end

**Signature**: `ProgressLogger.on_epoch_end(self, epoch: int) -> Any`

**Location**: line 176


## Functions (3)

### should_use_rich_console

**Signature**: `rl.training.progress_logger.should_use_rich_console() -> bool`

**Documentation**: Determine if rich console output is appropriate based on terminal context.

**Location**: line 18

### log_rich_progress

**Signature**: `rl.training.progress_logger.log_rich_progress(epoch: int, agent_step: int, total_timesteps: int, steps_per_sec: float, train_pct: float, rollout_pct: float, stats_pct: float, run_name: Any, heart_value: Any, heart_rate: Any) -> Any`

**Documentation**: Render training progress in a rich table.

**Location**: line 50

### log_training_progress

**Signature**: `rl.training.progress_logger.log_training_progress() -> Any`

**Documentation**: Log training progress with timing breakdown and optional metrics.

**Location**: line 91

