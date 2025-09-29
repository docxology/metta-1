# tools.play

**Module**: `tools.play`

**Source**: `metta/tools/play.py`

**Imports**:
- `json`
- `logging`
- `metta.common.tool.Tool`
- `metta.common.util.constants.DEV_METTASCOPE_FRONTEND_URL`
- `metta.common.wandb.context.WandbConfig`
- `metta.sim.simulation.Simulation`
- `metta.sim.simulation_config.SimulationConfig`
- `metta.tools.utils.auto_config.auto_wandb_config`
- `mettagrid.util.grid_object_formatter.format_grid_object`
- `numpy`
- `torch`

## Classes (1)

### PlayTool

**Class**: `tools.play.PlayTool`

**Constructor**: `PlayTool()`

**Methods**: 3

#### effective_replay_dir

**Signature**: `PlayTool.effective_replay_dir(self) -> str`

**Documentation**: Get the replay directory, defaulting to system.data_dir/replays if not specified.

**Location**: line 30

#### effective_stats_dir

**Signature**: `PlayTool.effective_stats_dir(self) -> str`

**Documentation**: Get the stats directory, defaulting to system.data_dir/stats if not specified.

**Location**: line 35

#### invoke

**Signature**: `PlayTool.invoke(self, args: dict) -> Any`

**Location**: line 39


