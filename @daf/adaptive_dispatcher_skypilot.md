# adaptive.dispatcher.skypilot

**Module**: `adaptive.dispatcher.skypilot`

**Source**: `metta/adaptive/dispatcher/skypilot.py`

**Imports**:
- `logging`
- `metta.adaptive.dispatcher.local.LocalDispatcher`
- `metta.adaptive.models.JobDefinition`
- `metta.adaptive.models.JobTypes`
- `metta.adaptive.protocols.Dispatcher`
- `metta.adaptive.utils.get_display_id`
- `metta.common.util.constants.SKYPILOT_LAUNCH_PATH`
- `subprocess`
- `uuid`

## Classes (1)

### SkypilotDispatcher

**Class**: `adaptive.dispatcher.skypilot.SkypilotDispatcher`

**Constructor**: `SkypilotDispatcher(self) -> Any`

**Documentation**: Dispatch training via Skypilot while keeping evals local.

**Methods**: 2

#### dispatch

**Signature**: `SkypilotDispatcher.dispatch(self, job: JobDefinition) -> str`

**Location**: line 22

#### check_local_processes

**Signature**: `SkypilotDispatcher.check_local_processes(self) -> int`

**Documentation**: Return number of active local evaluation processes.

**Location**: line 88


