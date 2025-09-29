# sim.stats.episode_stats_db

**Module**: `sim.stats.episode_stats_db`

**Source**: `metta/sim/stats/episode_stats_db.py`

**Imports**:
- `datetime`
- `duckdb`
- `logging`
- `os`
- `pandas`
- `pathlib.Path`
- `typing.Dict`

## Classes (1)

### EpisodeStatsDB

**Class**: `sim.stats.episode_stats_db.EpisodeStatsDB`

**Constructor**: `EpisodeStatsDB(self, path: Path) -> Any`

**Documentation**: DuckDB database for recording the outcomes of episodes.
Includes per-agent and per-group statistics along with episode metadata.

Can be extended (e.g. see SimulationStatsDb) with additional context on top of this data.

**Methods**: 5

#### initialize_schema

**Signature**: `EpisodeStatsDB.initialize_schema(self) -> Any`

**Location**: line 71

#### tables

**Signature**: `EpisodeStatsDB.tables(self) -> Dict`

**Documentation**: Return all tables in the database.

**Location**: line 81

#### record_episode

**Signature**: `EpisodeStatsDB.record_episode(self, episode_id: str, attributes: Dict, agent_metrics: Dict, agent_groups: Dict, step_count: int, replay_url: Any, created_at: Any) -> Any`

**Location**: line 85

#### query

**Signature**: `EpisodeStatsDB.query(self, sql_query: str) -> Any`

**Documentation**: Execute a SQL query and return a pandas DataFrame.

**Location**: line 149

#### close

**Signature**: `EpisodeStatsDB.close(self) -> Any`

**Location**: line 153


