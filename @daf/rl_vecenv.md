# rl.vecenv

**Module**: `rl.vecenv`

**Source**: `metta/rl/vecenv.py`

**Imports**:
- `logging`
- `metta.cogworks.curriculum.Curriculum`
- `metta.cogworks.curriculum.CurriculumEnv`
- `metta.common.util.log_config.init_logging`
- `mettagrid.MettaGridEnv`
- `mettagrid.util.replay_writer.ReplayWriter`
- `mettagrid.util.stats_writer.StatsWriter`
- `pathlib.Path`
- `pufferlib`
- `pufferlib.pufferlib.set_buffers`
- `pufferlib.vector`
- `pydantic.validate_call`
- `typing.Any`
- `typing.Optional`

## Functions (2)

### make_env_func

**Signature**: `rl.vecenv.make_env_func(curriculum: Curriculum, render_mode = ..., stats_writer: Optional[StatsWriter] = ..., replay_writer: Optional[ReplayWriter] = ..., is_training: bool = ..., run_dir: Any = ..., buf: Optional[Any] = ..., **kwargs)`

**Location**: line 20

### make_vecenv

**Signature**: `rl.vecenv.make_vecenv(curriculum: Curriculum, vectorization: str, num_envs: int = ..., batch_size: Any = ..., num_workers: int = ..., render_mode: Any = ..., stats_writer: Any = ..., replay_writer: Any = ..., is_training: bool = ..., run_dir: Any = ..., **kwargs) -> Any`

**Location**: line 47

