# cogworks.curriculum.curriculum

**Module**: `cogworks.curriculum.curriculum`

**Source**: `metta/cogworks/curriculum/curriculum.py`

**Imports**:
- `__future__.annotations`
- `abc`
- `abc.ABC`
- `logging`
- `metta.cogworks.curriculum.learning_progress_algorithm.LearningProgressConfig`
- `metta.cogworks.curriculum.stats.SliceAnalyzer`
- `metta.cogworks.curriculum.stats.StatsLogger`
- `metta.cogworks.curriculum.task_generator.AnyTaskGeneratorConfig`
- `metta.cogworks.curriculum.task_generator.SingleTaskGenerator`
- `mettagrid.config.Config`
- `mettagrid.config.mettagrid_config.MettaGridConfig`
- `pydantic.ConfigDict`
- `pydantic.Field`
- `random`
- `typing.Any`
- `typing.ClassVar`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.TYPE_CHECKING`
- `typing.Union`

## Classes (7)

### CurriculumTask

**Class**: `cogworks.curriculum.curriculum.CurriculumTask`

**Constructor**: `CurriculumTask(self, task_id: int, env_cfg, slice_values: Optional[Dict] = ...)`

**Documentation**: A task instance with a task_id and env_cfg.

**Methods**: 4

#### complete

**Signature**: `CurriculumTask.complete(self, score: float)`

**Documentation**: Complete the task with a score.

**Location**: line 43

#### get_env_cfg

**Signature**: `CurriculumTask.get_env_cfg(self)`

**Documentation**: Get the environment configuration for this task.

**Location**: line 49

#### get_slice_values

**Signature**: `CurriculumTask.get_slice_values(self)`

**Documentation**: Get the slice values that were used to generate this task.

**Location**: line 53

#### get_bucket_values

**Signature**: `CurriculumTask.get_bucket_values(self)`

**Documentation**: Get the slice values (backward compatibility alias).

**Location**: line 57


### CurriculumAlgorithmConfig

**Class**: `cogworks.curriculum.curriculum.CurriculumAlgorithmConfig`

**Constructor**: `CurriculumAlgorithmConfig()`

**Documentation**: Hyperparameters for the CurriculumAlgorithm.

**Methods**: 2

#### algorithm_type

**Signature**: `CurriculumAlgorithmConfig.algorithm_type(self) -> str`

**Documentation**: Return the algorithm type string used in configs.

**Location**: line 69

#### create

**Signature**: `CurriculumAlgorithmConfig.create(self, num_tasks: int) -> Any`

**Documentation**: Create the curriculum algorithm with these hyperparameters.

Args:
    num_tasks: Number of tasks the algorithm will manage

Returns:
    Configured curriculum algorithm instance

**Location**: line 73


### CurriculumAlgorithm

**Class**: `cogworks.curriculum.curriculum.CurriculumAlgorithm`

**Constructor**: `CurriculumAlgorithm(self, num_tasks: int, hypers: Optional[CurriculumAlgorithmConfig] = ..., initialize_weights: bool = ...)`

**Documentation**: Curriculum algorithms are responsible for:
1. Scoring tasks based on their learning progress or other metrics
2. Recommending which tasks to evict when the pool is full
3. Tracking task performance for algorithm-specific purposes
4. Providing feedback to Curriculum for task selection

The Curriculum maintains the task pool and lifecycle, while algorithms provide guidance.
Inherits from StatsLogger to provide unified statistics interface.

**Methods**: 13

#### score_tasks

**Signature**: `CurriculumAlgorithm.score_tasks(self, task_ids: List[int]) -> Dict`

**Documentation**: Score tasks for selection purposes. Higher scores = more likely to be selected.

**Location**: line 109

#### recommend_eviction

**Signature**: `CurriculumAlgorithm.recommend_eviction(self, task_ids: List[int]) -> Optional[int]`

**Documentation**: Recommend which task to evict. Return None for random selection.

**Location**: line 114

#### on_task_evicted

**Signature**: `CurriculumAlgorithm.on_task_evicted(self, task_id: int) -> Any`

**Documentation**: Notification that a task has been evicted from the pool.

**Location**: line 119

#### update_task_performance

**Signature**: `CurriculumAlgorithm.update_task_performance(self, task_id: int, score: float)`

**Documentation**: Update task performance. Override in subclasses that track performance.

**Location**: line 124

#### get_state

**Signature**: `CurriculumAlgorithm.get_state(self) -> Dict`

**Documentation**: Get algorithm state for checkpointing. Override in subclasses that have state.

**Location**: line 128

#### load_state

**Signature**: `CurriculumAlgorithm.load_state(self, state: Dict) -> Any`

**Documentation**: Load algorithm state from checkpoint. Override in subclasses that have state.

**Location**: line 132

#### on_task_created

**Signature**: `CurriculumAlgorithm.on_task_created(self, task: Any) -> Any`

**Documentation**: Notification that a new task has been created. Override if needed.

**Location**: line 136

#### set_curriculum_reference

**Signature**: `CurriculumAlgorithm.set_curriculum_reference(self, curriculum: Any) -> Any`

**Documentation**: Set reference to curriculum for stats updates. Override if needed.

**Location**: line 140

#### should_evict_task

**Signature**: `CurriculumAlgorithm.should_evict_task(self, task_id: int, min_presentations: int = ...) -> bool`

**Documentation**: Check if a task should be evicted based on algorithm-specific criteria.

Default implementation returns False (no eviction). Subclasses should override
to implement their own eviction criteria.

Args:
    task_id: The task to check
    min_presentations: Minimum number of task presentations before eviction

Returns:
    True if task should be evicted

**Location**: line 144

#### get_base_stats

**Signature**: `CurriculumAlgorithm.get_base_stats(self) -> Dict`

**Documentation**: Get basic statistics that all algorithms must provide.

**Location**: line 178

#### get_detailed_stats

**Signature**: `CurriculumAlgorithm.get_detailed_stats(self) -> Dict`

**Documentation**: Get detailed stats including expensive slice analysis.

**Location**: line 182

#### stats

**Signature**: `CurriculumAlgorithm.stats(self, prefix: str = ...) -> dict`

**Documentation**: Return statistics for logging purposes. Add `prefix` to all keys.

**Location**: line 186

#### get_task_from_pool

**Signature**: `CurriculumAlgorithm.get_task_from_pool(self, task_generator, rng) -> Any`

**Documentation**: Get a task from the pool. Default implementation creates a simple task.

**Location**: line 191


### DiscreteRandomConfig

**Class**: `cogworks.curriculum.curriculum.DiscreteRandomConfig`

**Constructor**: `DiscreteRandomConfig()`

**Documentation**: Hyperparameters for DiscreteRandomCurriculum.

**Methods**: 1

#### algorithm_type

**Signature**: `DiscreteRandomConfig.algorithm_type(self) -> str`

**Location**: line 204


### DiscreteRandomCurriculum

**Class**: `cogworks.curriculum.curriculum.DiscreteRandomCurriculum`

**Constructor**: `DiscreteRandomCurriculum()`

**Documentation**: Curriculum algorithm that samples from a discrete distribution of weights.

A named class for the simplest case where weights don't change based on
task performance.

**Methods**: 4

#### score_tasks

**Signature**: `DiscreteRandomCurriculum.score_tasks(self, task_ids: List[int]) -> Dict`

**Documentation**: All tasks have equal score for random selection.

**Location**: line 215

#### recommend_eviction

**Signature**: `DiscreteRandomCurriculum.recommend_eviction(self, task_ids: List[int]) -> Optional[int]`

**Documentation**: No preference for eviction - let Curriculum choose randomly.

**Location**: line 219

#### on_task_evicted

**Signature**: `DiscreteRandomCurriculum.on_task_evicted(self, task_id: int) -> Any`

**Documentation**: No action needed for random curriculum.

**Location**: line 223

#### update_task_performance

**Signature**: `DiscreteRandomCurriculum.update_task_performance(self, task_id: int, score: float)`

**Documentation**: Update task performance - no-op for discrete random curriculum.

**Location**: line 227


### CurriculumConfig

**Class**: `cogworks.curriculum.curriculum.CurriculumConfig`

**Constructor**: `CurriculumConfig()`

**Documentation**: Base configuration for Curriculum.

**Methods**: 3

#### from_mg

**Signature**: `CurriculumConfig.from_mg(cls, mg_config: MettaGridConfig) -> Any`

**Documentation**: Create a CurriculumConfig from a MettaGridConfig.

**Location**: line 249

#### model_post_init

**Signature**: `CurriculumConfig.model_post_init(self, __context) -> Any`

**Documentation**: Validate configuration after initialization.

**Location**: line 261

#### make

**Signature**: `CurriculumConfig.make(self) -> Any`

**Documentation**: Create a Curriculum from this configuration.

**Location**: line 270


### Curriculum

**Class**: `cogworks.curriculum.curriculum.Curriculum`

**Constructor**: `Curriculum(self, config: CurriculumConfig, seed: int = ...)`

**Documentation**: Base curriculum class that uses TaskGenerator to generate EnvConfigs and returns Tasks.

Curriculum takes a CurriculumConfig, and supports get_task(). It uses the task generator
to generate the EnvConfig and then returns a Task(env_cfg). It can optionally use a
CurriculumAlgorithm for intelligent task selection.

Inherits from StatsLogger to provide unified statistics interface.

**Methods**: 6

#### get_task

**Signature**: `Curriculum.get_task(self) -> CurriculumTask`

**Documentation**: Sample a task from the population.

**Location**: line 307

#### update_task_performance

**Signature**: `Curriculum.update_task_performance(self, task_id: int, score: float)`

**Documentation**: Update the curriculum algorithm with task performance.

**Location**: line 394

#### get_base_stats

**Signature**: `Curriculum.get_base_stats(self) -> Dict`

**Documentation**: Get basic curriculum statistics.

**Location**: line 402

#### stats

**Signature**: `Curriculum.stats(self) -> dict`

**Documentation**: Return curriculum statistics for logging purposes.

**Location**: line 419

#### get_state

**Signature**: `Curriculum.get_state(self) -> Dict`

**Documentation**: Get curriculum state for checkpointing.

**Location**: line 424

#### load_state

**Signature**: `Curriculum.load_state(self, state: Dict) -> Any`

**Documentation**: Load curriculum state from checkpoint.

**Location**: line 450


## Functions (1)

### get_algorithm_hypers_discriminator

**Signature**: `cogworks.curriculum.curriculum.get_algorithm_hypers_discriminator(v)`

**Documentation**: Discriminator function for algorithm hypers types.

**Location**: line 24

