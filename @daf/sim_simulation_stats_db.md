# sim.simulation_stats_db

**Module**: `sim.simulation_stats_db`

**Source**: `metta/sim/simulation_stats_db.py`

**Imports**:
- `__future__.annotations`
- `contextlib.contextmanager`
- `duckdb`
- `logging`
- `metta.rl.checkpoint_manager.CheckpointManager`
- `metta.sim.stats.episode_stats_db.EpisodeStatsDB`
- `metta.utils.file.exists`
- `metta.utils.file.local_copy`
- `metta.utils.file.write_file`
- `pathlib.Path`
- `typing.Dict`
- `typing.List`
- `typing.Tuple`
- `typing.Union`

## Classes (1)

### SimulationStatsDB

**Class**: `sim.simulation_stats_db.SimulationStatsDB`

**Constructor**: `SimulationStatsDB(self, path: Path) -> Any`

**Methods**: 7

#### tables

**Signature**: `SimulationStatsDB.tables(self) -> Dict`

**Documentation**: Add simulation tables to the parent tables.
super().initialize_schema() will read this to initialize the schema.

**Location**: line 45

#### from_uri

**Signature**: `SimulationStatsDB.from_uri(cls, path: str)`

**Documentation**: Creates a StatsDB instance from a URI and yields it as a context manager.
Supports local paths and s3:// URIs.
The temporary file is automatically cleaned up when the context exits.

Usage:
    with StatsDB.from_uri(uri) as db:
        # do something with the StatsDB instance

**Location**: line 54

#### from_shards_and_context

**Signature**: `SimulationStatsDB.from_shards_and_context() -> Any`

**Location**: line 69

#### export

**Signature**: `SimulationStatsDB.export(self, dest: str) -> Any`

**Documentation**: Export **self** to *dest*.

• If *dest* already holds a DuckDB file/artifact, merge **self**
  into the existing DB first and re-upload the result.
• Otherwise simply upload **self**.

Supported URI schemes: local paths and `s3://`.

**Location**: line 139

#### get_replay_urls

**Signature**: `SimulationStatsDB.get_replay_urls(self, policy_uri: Any = ..., sim_suite: Any = ..., env: Any = ...) -> List[str]`

**Documentation**: Get replay URLs, optionally filtered by policy URI and/or environment.

**Location**: line 159

#### get_all_policy_uris

**Signature**: `SimulationStatsDB.get_all_policy_uris(self) -> List[str]`

**Documentation**: Get all unique policy identifiers from the database.

**Location**: line 188

#### merge_in

**Signature**: `SimulationStatsDB.merge_in(self, other: Any) -> Any`

**Location**: line 243


