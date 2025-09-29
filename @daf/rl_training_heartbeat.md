# rl.training.heartbeat

**Module**: `rl.training.heartbeat`

**Source**: `metta/rl/training/heartbeat.py`

**Imports**:
- `logging`
- `metta.common.util.heartbeat.record_heartbeat`
- `metta.rl.training.TrainerComponent`
- `mettagrid.config.Config`

## Classes (2)

### HeartbeatConfig

**Class**: `rl.training.heartbeat.HeartbeatConfig`

**Constructor**: `HeartbeatConfig()`

**Documentation**: Configuration for heartbeat monitoring.

### Heartbeat

**Class**: `rl.training.heartbeat.Heartbeat`

**Constructor**: `Heartbeat()`

**Documentation**: Writes heartbeat signals for monitoring training progress.

**Methods**: 1

#### on_epoch_end

**Signature**: `Heartbeat.on_epoch_end(self, epoch: int) -> Any`

**Location**: line 22


