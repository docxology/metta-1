# sim.stats.episode_stats

**Module**: `sim.stats.episode_stats`

**Source**: `metta/sim/stats/episode_stats.py`

**Imports**:
- `datetime`
- `episode_stats_db.EpisodeStatsDB`
- `mettagrid.util.stats_writer.StatsWriter`
- `os`
- `pathlib.Path`
- `typing.Dict`
- `uuid`

## Classes (1)

### DuckDBStatsWriter

**Class**: `sim.stats.episode_stats.DuckDBStatsWriter`

**Constructor**: `DuckDBStatsWriter(self, dir: Path) -> Any`

**Documentation**: DuckDB implementation of StatsWriter for tracking statistics in MettaGrid.
Can be used by multiple environments simultaneously.
Safe to serialize/deserialize with multiprocessing as long as we have not yet created a connection to a duckdb file.

**Methods**: 2

#### record_episode

**Signature**: `DuckDBStatsWriter.record_episode(self, episode_id: str, attributes: Dict, agent_metrics: Dict, agent_groups: Dict, step_count: int, replay_url: Any, created_at: Any) -> Any`

**Location**: line 41

#### close

**Signature**: `DuckDBStatsWriter.close(self) -> Any`

**Location**: line 55


