# cogworks.curriculum.curriculum_env

**Module**: `cogworks.curriculum.curriculum_env`

**Source**: `metta/cogworks/curriculum/curriculum_env.py`

**Imports**:
- `__future__.annotations`
- `curriculum.Curriculum`
- `pufferlib.PufferEnv`
- `typing.Any`

## Classes (1)

### CurriculumEnv

**Class**: `cogworks.curriculum.curriculum_env.CurriculumEnv`

**Constructor**: `CurriculumEnv(self, env: Any, curriculum: Curriculum)`

**Documentation**: Environment wrapper that integrates with a curriculum system.

This wrapper passes all function calls to the wrapped environment, with special
handling for reset() and step() methods to integrate with curriculum task management.

**Methods**: 4

#### reset

**Signature**: `CurriculumEnv.reset(self, *args, **kwargs)`

**Documentation**: Reset the environment and get a new task from curriculum.

**Location**: line 65

#### step

**Signature**: `CurriculumEnv.step(self, *args, **kwargs)`

**Documentation**: Step the environment and handle task completion.

Calls the environment's step method, then checks if the episode is done
and completes the current task with the curriculum if so. Then gives the
environment a new env config.

**Location**: line 85

#### set_stats_update_frequency

**Signature**: `CurriculumEnv.set_stats_update_frequency(self, frequency: int) -> Any`

**Documentation**: Set the frequency of curriculum stats updates during steps.

Args:
    frequency: Number of steps between stats updates (default: 50)

**Location**: line 111

#### force_stats_update

**Signature**: `CurriculumEnv.force_stats_update(self) -> Any`

**Documentation**: Force an immediate update of curriculum stats.

**Location**: line 120


