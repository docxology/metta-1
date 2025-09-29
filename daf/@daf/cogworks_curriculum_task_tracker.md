# cogworks.curriculum.task_tracker

**Module**: `cogworks.curriculum.task_tracker`

**Source**: `metta/cogworks/curriculum/task_tracker.py`

**Imports**:
- `collections.deque`
- `time`
- `typing.Any`
- `typing.Dict`
- `typing.Optional`
- `typing.Tuple`

## Classes (1)

### TaskTracker

**Class**: `cogworks.curriculum.task_tracker.TaskTracker`

**Constructor**: `TaskTracker(self, max_memory_tasks: int = ...)`

**Documentation**: Tracks task metadata, performance history, and completion statistics.

**Methods**: 8

#### track_task_creation

**Signature**: `TaskTracker.track_task_creation(self, task_id: int) -> Any`

**Documentation**: Track when a task is created.

**Location**: line 32

#### update_task_performance

**Signature**: `TaskTracker.update_task_performance(self, task_id: int, score: float) -> Any`

**Documentation**: Update task performance with new completion score.

**Location**: line 45

#### get_task_stats

**Signature**: `TaskTracker.get_task_stats(self, task_id: int) -> Optional[Dict]`

**Documentation**: Get statistics for a specific task.

**Location**: line 71

#### get_all_tracked_tasks

**Signature**: `TaskTracker.get_all_tracked_tasks(self) -> list[int]`

**Documentation**: Get all currently tracked task IDs.

**Location**: line 93

#### remove_task

**Signature**: `TaskTracker.remove_task(self, task_id: int) -> Any`

**Documentation**: Remove a task from tracking.

**Location**: line 97

#### get_global_stats

**Signature**: `TaskTracker.get_global_stats(self) -> Dict`

**Documentation**: Get global performance statistics.

**Location**: line 112

#### get_state

**Signature**: `TaskTracker.get_state(self) -> Dict`

**Documentation**: Get task tracker state for checkpointing.

**Location**: line 153

#### load_state

**Signature**: `TaskTracker.load_state(self, state: Dict) -> Any`

**Documentation**: Load task tracker state from checkpoint.

**Location**: line 172


