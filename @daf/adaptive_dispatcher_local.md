# adaptive.dispatcher.local

**Module**: `adaptive.dispatcher.local`

**Source**: `metta/adaptive/dispatcher/local.py`

**Imports**:
- `logging`
- `metta.adaptive.models.JobDefinition`
- `metta.adaptive.utils.get_display_id`
- `subprocess`
- `threading`

## Classes (1)

### LocalDispatcher

**Class**: `adaptive.dispatcher.local.LocalDispatcher`

**Constructor**: `LocalDispatcher(self, capture_output: bool = ...)`

**Documentation**: Runs jobs as local subprocesses.

**Methods**: 2

#### check_processes

**Signature**: `LocalDispatcher.check_processes(self)`

**Documentation**: Check status of all processes.

**Location**: line 45

#### dispatch

**Signature**: `LocalDispatcher.dispatch(self, job: JobDefinition) -> str`

**Documentation**: Dispatch job locally as subprocess.

**Location**: line 75


