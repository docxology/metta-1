# rl.training.training_environment

**Module**: `rl.training.training_environment`

**Source**: `metta/rl/training/training_environment.py`

**Imports**:
- `abc.ABC`
- `abc.abstractmethod`
- `dataclasses.dataclass`
- `logging`
- `metta.cogworks.curriculum.Curriculum`
- `metta.cogworks.curriculum.CurriculumConfig`
- `metta.cogworks.curriculum.env_curriculum`
- `metta.rl.vecenv.make_vecenv`
- `metta.utils.batch.calculate_batch_sizes`
- `mettagrid.builder.envs.make_arena`
- `mettagrid.config.Config`
- `mettagrid.core.ObsFeature`
- `mettagrid.mettagrid_c.dtype_actions`
- `numpy`
- `os`
- `platform`
- `pydantic.Field`
- `torch`
- `torch.Tensor`
- `typing.Any`
- `typing.List`
- `typing.Literal`
- `typing.Tuple`

## Classes (5)

### TrainingEnvironmentConfig

**Class**: `rl.training.training_environment.TrainingEnvironmentConfig`

**Constructor**: `TrainingEnvironmentConfig()`

**Documentation**: Configuration for training environment.

### EnvironmentMetaData

**Class**: `rl.training.training_environment.EnvironmentMetaData`

**Constructor**: `EnvironmentMetaData()`

### BatchInfo

**Class**: `rl.training.training_environment.BatchInfo`

**Constructor**: `BatchInfo()`

### TrainingEnvironment

**Class**: `rl.training.training_environment.TrainingEnvironment`

**Constructor**: `TrainingEnvironment()`

**Documentation**: Abstract base class for training environment.

**Methods**: 7

#### close

**Signature**: `TrainingEnvironment.close(self) -> Any`

**Documentation**: Close the environment.

**Location**: line 84

#### get_observations

**Signature**: `TrainingEnvironment.get_observations(self) -> Tuple`

**Documentation**: Get the observations.

**Location**: line 88

#### send_actions

**Signature**: `TrainingEnvironment.send_actions(self, actions: Any) -> Any`

**Documentation**: Send the actions.

**Location**: line 92

#### batch_info

**Signature**: `TrainingEnvironment.batch_info(self) -> BatchInfo`

**Documentation**: Get the batch information.

**Location**: line 97

#### single_action_space

**Signature**: `TrainingEnvironment.single_action_space(self) -> Any`

**Documentation**: Get the single action space.

**Location**: line 102

#### single_observation_space

**Signature**: `TrainingEnvironment.single_observation_space(self) -> Any`

**Documentation**: Get the single observation space.

**Location**: line 107

#### meta_data

**Signature**: `TrainingEnvironment.meta_data(self) -> EnvironmentMetaData`

**Documentation**: Get the environment metadata.

**Location**: line 112


### VectorizedTrainingEnvironment

**Class**: `rl.training.training_environment.VectorizedTrainingEnvironment`

**Constructor**: `VectorizedTrainingEnvironment(self, cfg: TrainingEnvironmentConfig)`

**Documentation**: Manages the vectorized training environment and experience generation.

**Methods**: 10

#### close

**Signature**: `VectorizedTrainingEnvironment.close(self) -> Any`

**Documentation**: Close the environment.

**Location**: line 197

#### meta_data

**Signature**: `VectorizedTrainingEnvironment.meta_data(self) -> EnvironmentMetaData`

**Location**: line 202

#### batch_info

**Signature**: `VectorizedTrainingEnvironment.batch_info(self) -> BatchInfo`

**Location**: line 206

#### total_parallel_agents

**Signature**: `VectorizedTrainingEnvironment.total_parallel_agents(self) -> int`

**Documentation**: Total agent slots tracked across all vectorized environments.

**Location**: line 212

#### single_action_space

**Signature**: `VectorizedTrainingEnvironment.single_action_space(self) -> Any`

**Location**: line 220

#### single_observation_space

**Signature**: `VectorizedTrainingEnvironment.single_observation_space(self) -> Any`

**Location**: line 224

#### vecenv

**Signature**: `VectorizedTrainingEnvironment.vecenv(self) -> Any`

**Documentation**: Return the underlying PufferLib vectorized environment.

**Location**: line 228

#### driver_env

**Signature**: `VectorizedTrainingEnvironment.driver_env(self) -> Any`

**Documentation**: Expose the driver environment for components that need direct access.

**Location**: line 233

#### get_observations

**Signature**: `VectorizedTrainingEnvironment.get_observations(self) -> Tuple`

**Location**: line 237

#### send_actions

**Signature**: `VectorizedTrainingEnvironment.send_actions(self, actions: Any) -> Any`

**Location**: line 253


## Functions (1)

### guess_vectorization

**Signature**: `rl.training.training_environment.guess_vectorization() -> Literal`

**Location**: line 26

