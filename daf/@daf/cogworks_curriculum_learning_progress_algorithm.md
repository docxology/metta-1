# cogworks.curriculum.learning_progress_algorithm

**Module**: `cogworks.curriculum.learning_progress_algorithm`

**Source**: `metta/cogworks/curriculum/learning_progress_algorithm.py`

**Imports**:
- `curriculum.CurriculumAlgorithm`
- `curriculum.CurriculumAlgorithmConfig`
- `curriculum.CurriculumTask`
- `numpy`
- `random`
- `task_tracker.TaskTracker`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

## Classes (2)

### LearningProgressConfig

**Class**: `cogworks.curriculum.learning_progress_algorithm.LearningProgressConfig`

**Constructor**: `LearningProgressConfig()`

**Documentation**: Configuration for learning progress with bidirectional scoring as default.

**Methods**: 2

#### algorithm_type

**Signature**: `LearningProgressConfig.algorithm_type(self) -> str`

**Location**: line 44

#### create

**Signature**: `LearningProgressConfig.create(self, num_tasks: int) -> Any`

**Location**: line 47


### LearningProgressAlgorithm

**Class**: `cogworks.curriculum.learning_progress_algorithm.LearningProgressAlgorithm`

**Constructor**: `LearningProgressAlgorithm(self, num_tasks: int, hypers: LearningProgressConfig)`

**Documentation**: Learning Progress Algorithm with integrated bidirectional scoring.

Uses bidirectional learning progress by default, combining fast and slow
exponential moving averages to detect learning opportunities and guide
intelligent task selection.

**Methods**: 16

#### lp_scorer

**Signature**: `LearningProgressAlgorithm.lp_scorer(self)`

**Documentation**: Compatibility property for tests that expect lp_scorer attribute.

**Location**: line 82

#### exploration_bonus

**Signature**: `LearningProgressAlgorithm.exploration_bonus(self)`

**Documentation**: Compatibility property for tests that expect exploration_bonus attribute.

**Location**: line 87

#### get_base_stats

**Signature**: `LearningProgressAlgorithm.get_base_stats(self) -> Dict`

**Documentation**: Get basic statistics that all algorithms must provide.

**Location**: line 91

#### stats

**Signature**: `LearningProgressAlgorithm.stats(self, prefix: str = ...) -> Dict`

**Documentation**: Get all statistics with optional prefix. Always includes learning progress stats.

**Location**: line 102

#### score_tasks

**Signature**: `LearningProgressAlgorithm.score_tasks(self, task_ids: List[int]) -> Dict`

**Documentation**: Score tasks using the configured method (bidirectional by default).

**Location**: line 155

#### recommend_eviction

**Signature**: `LearningProgressAlgorithm.recommend_eviction(self, task_ids: List[int]) -> Optional[int]`

**Documentation**: Recommend which task to evict based on learning progress.

**Location**: line 246

#### should_evict_task

**Signature**: `LearningProgressAlgorithm.should_evict_task(self, task_id: int, min_presentations: int = ...) -> bool`

**Documentation**: Check if a task should be evicted based on criteria.

**Location**: line 257

#### on_task_evicted

**Signature**: `LearningProgressAlgorithm.on_task_evicted(self, task_id: int) -> Any`

**Documentation**: Clean up when a task is evicted.

**Location**: line 283

#### update_task_performance

**Signature**: `LearningProgressAlgorithm.update_task_performance(self, task_id: int, score: float) -> Any`

**Documentation**: Update task performance using the appropriate scoring method.

**Location**: line 307

#### get_learning_progress_score

**Signature**: `LearningProgressAlgorithm.get_learning_progress_score(self, task_id: int, task_tracker = ...) -> float`

**Documentation**: Get learning progress score for a specific task (compatibility method for tests).

**Location**: line 339

#### get_stats

**Signature**: `LearningProgressAlgorithm.get_stats(self) -> Dict`

**Documentation**: Get learning progress statistics (compatibility method for tests).

**Location**: line 346

#### update_task_with_slice_values

**Signature**: `LearningProgressAlgorithm.update_task_with_slice_values(self, task_id: int, score: float, slice_values: Dict) -> Any`

**Documentation**: Update task performance including slice values for analysis.

**Location**: line 353

#### on_task_created

**Signature**: `LearningProgressAlgorithm.on_task_created(self, task: CurriculumTask) -> Any`

**Documentation**: Handle task creation by tracking it.

**Location**: line 403

#### get_detailed_stats

**Signature**: `LearningProgressAlgorithm.get_detailed_stats(self) -> Dict`

**Documentation**: Get detailed stats including learning progress and slice distribution analysis.

**Location**: line 416

#### get_state

**Signature**: `LearningProgressAlgorithm.get_state(self) -> Dict`

**Documentation**: Get learning progress algorithm state for checkpointing.

**Location**: line 675

#### load_state

**Signature**: `LearningProgressAlgorithm.load_state(self, state: Dict) -> Any`

**Documentation**: Load learning progress algorithm state from checkpoint.

**Location**: line 705


