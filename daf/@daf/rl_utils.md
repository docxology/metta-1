# rl.utils

**Module**: `rl.utils`

**Source**: `metta/rl/utils.py`

**Imports**:
- `tensordict.TensorDict`
- `torch`

## Functions (2)

### ensure_sequence_metadata

**Signature**: `rl.utils.ensure_sequence_metadata(td: TensorDict) -> Any`

**Documentation**: Attach required sequence metadata to ``td`` if missing.

**Location**: line 7

### should_run

**Signature**: `rl.utils.should_run(epoch: int, interval: int) -> bool`

**Documentation**: Check if a periodic task should run based on interval. It is assumed this is only called on master.

**Location**: line 18

