# cogworks.curriculum.__init__

**Module**: `cogworks.curriculum.__init__`

**Source**: `metta/cogworks/curriculum/__init__.py`

**Imports**:
- `curriculum.Curriculum`
- `curriculum.CurriculumConfig`
- `curriculum.CurriculumTask`
- `curriculum_env.CurriculumEnv`
- `learning_progress_algorithm.LearningProgressAlgorithm`
- `learning_progress_algorithm.LearningProgressConfig`
- `mettagrid.config.mettagrid_config.MettaGridConfig`
- `stats.SliceAnalyzer`
- `stats.StatsLogger`
- `task_generator.AnyTaskGeneratorConfig`
- `task_generator.BucketedTaskGenerator`
- `task_generator.SingleTaskGenerator`
- `task_generator.Span`
- `task_generator.TaskGenerator`
- `task_generator.TaskGeneratorConfig`
- `task_generator.TaskGeneratorSet`
- `task_tracker.TaskTracker`

## Functions (5)

### single_task

**Signature**: `cogworks.curriculum.__init__.single_task(mg_config: MettaGridConfig) -> Any`

**Documentation**: Create a `SingleTaskGenerator.Config` from a `MettaGridConfig`.

**Location**: line 43

### bucketed

**Signature**: `cogworks.curriculum.__init__.bucketed(mg_config: MettaGridConfig) -> Any`

**Documentation**: Create a `BucketedTaskGenerator.Config` from a `MettaGridConfig`.

**Location**: line 48

### multi_task

**Signature**: `cogworks.curriculum.__init__.multi_task(mg_config: MettaGridConfig) -> Any`

**Documentation**: Create a `TaskGeneratorSet.Config` from a `MettaGridConfig`.

**Location**: line 53

### merge

**Signature**: `cogworks.curriculum.__init__.merge(task_generator_configs: list[AnyTaskGeneratorConfig]) -> Any`

**Documentation**: Merge configs into a `TaskGeneratorSet.Config`.

**Location**: line 63

### env_curriculum

**Signature**: `cogworks.curriculum.__init__.env_curriculum(mg_config: MettaGridConfig) -> CurriculumConfig`

**Documentation**: Create a curriculum configuration from an MettaGridConfig.

**Location**: line 68

