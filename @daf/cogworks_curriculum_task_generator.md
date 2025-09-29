# cogworks.curriculum.task_generator

**Module**: `cogworks.curriculum.task_generator`

**Source**: `metta/cogworks/curriculum/task_generator.py`

**Imports**:
- `__future__.annotations`
- `abc.ABC`
- `abc.abstractmethod`
- `logging`
- `mettagrid.config.Config`
- `mettagrid.config.mettagrid_config.MettaGridConfig`
- `mettagrid.util.module.load_symbol`
- `pydantic.ConfigDict`
- `pydantic.Field`
- `pydantic.SerializeAsAny`
- `pydantic.WrapValidator`
- `pydantic.field_validator`
- `pydantic.model_serializer`
- `random`
- `typing.Annotated`
- `typing.Any`
- `typing.ClassVar`
- `typing.Optional`
- `typing.Sequence`
- `typing.Type`
- `typing.TypeVar`
- `typing_extensions.Generic`

## Classes (6)

### TaskGeneratorConfig

**Class**: `cogworks.curriculum.task_generator.TaskGeneratorConfig`

**Constructor**: `TaskGeneratorConfig()`

**Documentation**: Base configuration for TaskGenerator.

Subclasses *optionally* know which TaskGenerator they build via `_generator_cls`
(auto-filled when nested inside a TaskGenerator subclass).

**Methods**: 3

#### create

**Signature**: `TaskGeneratorConfig.create(self) -> TTaskGenerator`

**Documentation**: Instantiate the bound TaskGenerator.

Subclasses nested under a TaskGenerator automatically bind `_generator_cls`.
If you define a standalone Config subclass, either set `_generator_cls`
on the class or override `create()`.

**Location**: line 49

#### generator_cls

**Signature**: `TaskGeneratorConfig.generator_cls(cls) -> Type[TTaskGenerator]`

**Location**: line 59

#### to_curriculum

**Signature**: `TaskGeneratorConfig.to_curriculum(self, num_active_tasks: int = ..., algorithm_config = ...)`

**Documentation**: Create a CurriculumConfig from this TaskGeneratorConfig.

**Location**: line 67


### TaskGenerator

**Class**: `cogworks.curriculum.task_generator.TaskGenerator`

**Constructor**: `TaskGenerator(self, config: TaskGeneratorConfig)`

**Documentation**: Base class for generating tasks with deterministic seeding.

TaskGenerator supports .get_task(task_id) where task_id is used as the seed.
It should always be constructed with a TaskGeneratorConfig.

If a subclass declares a nested class `Config` that inherits from TaskGeneratorConfig,
it will be *automatically bound*.

**Methods**: 1

#### get_task

**Signature**: `TaskGenerator.get_task(self, task_id: int) -> MettaGridConfig`

**Documentation**: Generate a task (MettaGridConfig) using task_id as seed.

**Location**: line 111


### SingleTaskGenerator

**Class**: `cogworks.curriculum.task_generator.SingleTaskGenerator`

**Constructor**: `SingleTaskGenerator(self, config: Any)`

**Documentation**: TaskGenerator that always returns the same MettaGridConfig.

### TaskGeneratorSet

**Class**: `cogworks.curriculum.task_generator.TaskGeneratorSet`

**Constructor**: `TaskGeneratorSet(self, config: Any)`

**Documentation**: TaskGenerator that contains a list of TaskGenerators with weights.

When get_task() is called, rng is initialized with seed, then we sample
from the list by weight and return child.get_task().

### Span

**Class**: `cogworks.curriculum.task_generator.Span`

**Constructor**: `Span(self, range_min: Any = ..., range_max: Any = ..., **kwargs)`

**Documentation**: A range of values with minimum and maximum bounds.

**Methods**: 1

#### validate_range

**Signature**: `Span.validate_range(cls, v, info)`

**Documentation**: Ensure range_min is less than range_max.

**Location**: line 236


### BucketedTaskGenerator

**Class**: `cogworks.curriculum.task_generator.BucketedTaskGenerator`

**Constructor**: `BucketedTaskGenerator(self, config: Any)`

**Documentation**: TaskGenerator that picks values from buckets and applies them as overrides to a child generator.

When get_task() is called:
1. Sample a value from each bucket
2. Call the child TaskGenerator's get_task()
3. Apply the sampled bucket values as overrides to the returned MettaGridConfig

