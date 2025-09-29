# rl.training.monitor

**Module**: `rl.training.monitor`

**Source**: `metta/rl/training/monitor.py`

**Imports**:
- `__future__.annotations`
- `logging`
- `metta.rl.training.TrainerComponent`
- `mettagrid.profiling.memory_monitor.MemoryMonitor`
- `mettagrid.profiling.system_monitor.SystemMonitor`
- `typing.Optional`

## Classes (1)

### Monitor

**Class**: `rl.training.monitor.Monitor`

**Constructor**: `Monitor(self) -> Any`

**Documentation**: Manage memory and system monitors independently of stats reporting.

**Methods**: 3

#### register

**Signature**: `Monitor.register(self, context) -> Any`

**Location**: line 26

#### on_training_complete

**Signature**: `Monitor.on_training_complete(self) -> Any`

**Location**: line 41

#### on_failure

**Signature**: `Monitor.on_failure(self) -> Any`

**Location**: line 44


