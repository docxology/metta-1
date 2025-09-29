# tools.replay

**Module**: `tools.replay`

**Source**: `metta/tools/replay.py`

**Imports**:
- `logging`
- `metta.common.tool.Tool`
- `metta.common.util.constants.DEV_METTASCOPE_FRONTEND_URL`
- `metta.common.wandb.context.WandbConfig`
- `metta.sim.simulation.Simulation`
- `metta.sim.simulation_config.SimulationConfig`
- `metta.tools.play.PlayTool`
- `metta.tools.utils.auto_config.auto_wandb_config`
- `mettascope.server`
- `os`
- `platform`
- `urllib.parse.quote`

## Classes (1)

### ReplayTool

**Class**: `tools.replay.ReplayTool`

**Constructor**: `ReplayTool()`

**Documentation**: Tool for generating and viewing replay files in MettaScope.
Creates a simulation specifically to generate replay files and automatically
opens them in a browser for visualization. This tool focuses on replay viewing
and browser integration, unlike SimTool which focuses on policy evaluation.

**Methods**: 1

#### invoke

**Signature**: `ReplayTool.invoke(self, args: dict) -> Any`

**Location**: line 33


## Functions (2)

### get_clean_path

**Signature**: `tools.replay.get_clean_path(replay_url: str) -> str`

**Location**: line 56

### open_browser

**Signature**: `tools.replay.open_browser(replay_url: str, cfg: ReplayTool) -> Any`

**Location**: line 69

