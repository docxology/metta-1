# sim.replay_writer

**Module**: `sim.replay_writer`

**Source**: `metta/sim/replay_writer.py`

**Imports**:
- `__future__.annotations`
- `json`
- `logging`
- `metta.utils.file.http_url`
- `metta.utils.file.write_data`
- `mettagrid.util.grid_object_formatter.format_grid_object`
- `mettagrid.util.replay_writer.ReplayWriter`
- `numpy`
- `typing.TYPE_CHECKING`
- `zlib`

## Classes (2)

### S3ReplayWriter

**Class**: `sim.replay_writer.S3ReplayWriter`

**Constructor**: `S3ReplayWriter(self, replay_dir: Any = ...)`

**Documentation**: ReplayWriter implementation that uploads replays to S3.

**Methods**: 3

#### start_episode

**Signature**: `S3ReplayWriter.start_episode(self, episode_id: str, env: MettaGridCore) -> Any`

**Documentation**: Start recording a new episode.

**Location**: line 35

#### log_step

**Signature**: `S3ReplayWriter.log_step(self, episode_id: str, actions: Any, rewards: Any) -> Any`

**Documentation**: Log a single step in an episode.

**Location**: line 39

#### write_replay

**Signature**: `S3ReplayWriter.write_replay(self, episode_id: str) -> Any`

**Documentation**: Write the replay to the replay directory and return the URL.

**Location**: line 43


### EpisodeReplay

**Class**: `sim.replay_writer.EpisodeReplay`

**Constructor**: `EpisodeReplay(self, env: MettaGridCore)`

**Documentation**: Helper class for managing replay data for a single episode.

**Methods**: 3

#### log_step

**Signature**: `EpisodeReplay.log_step(self, actions: Any, rewards: Any)`

**Documentation**: Log a single step of the episode.

**Location**: line 80

#### get_replay_data

**Signature**: `EpisodeReplay.get_replay_data(self)`

**Documentation**: Gets full replay as a tree of plain python dictionaries.

**Location**: line 113

#### write_replay

**Signature**: `EpisodeReplay.write_replay(self, path: str)`

**Documentation**: Writes a replay to a file.

**Location**: line 124


