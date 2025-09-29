# sim.simulation

**Module**: `sim.simulation`

**Source**: `metta/sim/simulation.py`

**Imports**:
- `__future__.annotations`
- `dataclasses.dataclass`
- `einops.rearrange`
- `logging`
- `metta.agent.mocks.MockAgent`
- `metta.agent.policy.Policy`
- `metta.agent.utils.obs_to_td`
- `metta.app_backend.clients.stats_client.HttpStatsClient`
- `metta.app_backend.clients.stats_client.StatsClient`
- `metta.cogworks.curriculum.curriculum.Curriculum`
- `metta.cogworks.curriculum.curriculum.CurriculumConfig`
- `metta.common.util.heartbeat.record_heartbeat`
- `metta.rl.checkpoint_manager.CheckpointManager`
- `metta.rl.training.training_environment.EnvironmentMetaData`
- `metta.rl.vecenv.make_vecenv`
- `metta.sim.replay_writer.S3ReplayWriter`
- `metta.sim.simulation_config.SimulationConfig`
- `metta.sim.simulation_stats_db.SimulationStatsDB`
- `metta.sim.stats.DuckDBStatsWriter`
- `metta.sim.thumbnail_automation.maybe_generate_and_upload_thumbnail`
- `metta.sim.utils.get_or_create_policy_ids`
- `mettagrid.MettaGridEnv`
- `mettagrid.dtype_actions`
- `numpy`
- `os`
- `pathlib.Path`
- `time`
- `torch`
- `typing.Any`
- `typing.Dict`
- `uuid`

## Classes (3)

### SimulationCompatibilityError

**Class**: `sim.simulation.SimulationCompatibilityError`

**Constructor**: `SimulationCompatibilityError()`

**Documentation**: Raised when there's a compatibility issue that prevents simulation from running.

### Simulation

**Class**: `sim.simulation.Simulation`

**Constructor**: `Simulation(self, cfg: SimulationConfig, policy: Policy, policy_uri: str, device: Any, vectorization: str, stats_dir: str = ..., replay_dir: Any = ..., stats_client: Any = ..., stats_epoch_id: Any = ..., eval_task_id: Any = ...)`

**Documentation**: A vectorized batch of MettaGrid environments sharing the same parameters.

**Methods**: 12

#### create

**Signature**: `Simulation.create(cls, sim_config: SimulationConfig, device: str, vectorization: str, stats_dir: str = ..., replay_dir: str = ..., policy_uri: Any = ...) -> Any`

**Documentation**: Create a Simulation with sensible defaults.

**Location**: line 159

#### start_simulation

**Signature**: `Simulation.start_simulation(self) -> Any`

**Documentation**: Start the simulation.

**Location**: line 189

#### generate_actions

**Signature**: `Simulation.generate_actions(self) -> Any`

**Documentation**: Generate actions for the simulation.

**Location**: line 214

#### step_simulation

**Signature**: `Simulation.step_simulation(self, actions_np: Any) -> Any`

**Location**: line 277

#### end_simulation

**Signature**: `Simulation.end_simulation(self) -> SimulationResults`

**Location**: line 322

#### simulate

**Signature**: `Simulation.simulate(self) -> SimulationResults`

**Documentation**: Run the simulation; returns the merged `StatsDB`.

**Location**: line 338

#### get_policy_state

**Signature**: `Simulation.get_policy_state(self)`

**Documentation**: Get the policy state for memory manipulation.

**Location**: line 459

#### full_name

**Signature**: `Simulation.full_name(self) -> str`

**Location**: line 467

#### get_envs

**Signature**: `Simulation.get_envs(self)`

**Documentation**: Returns a list of all envs in the simulation.

**Location**: line 470

#### get_env

**Signature**: `Simulation.get_env(self)`

**Documentation**: Make sure this sim has a single env, and return it.

**Location**: line 474

#### get_replays

**Signature**: `Simulation.get_replays(self) -> dict`

**Documentation**: Get all replays for this simulation.

**Location**: line 480

#### get_replay

**Signature**: `Simulation.get_replay(self) -> dict`

**Documentation**: Makes sure this sim has a single replay, and return it.

**Location**: line 484


### SimulationResults

**Class**: `sim.simulation.SimulationResults`

**Constructor**: `SimulationResults()`

**Documentation**: Results of a simulation.
For now just a stats db. Replay plays can be retrieved from the stats db.

