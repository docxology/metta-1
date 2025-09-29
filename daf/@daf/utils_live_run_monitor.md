# utils.live_run_monitor

**Module**: `utils.live_run_monitor`

**Source**: `metta/utils/live_run_monitor.py`

**Imports**:
- `datetime.datetime`
- `logging`
- `metta.common.util.constants.METTA_WANDB_ENTITY`
- `metta.common.util.constants.METTA_WANDB_PROJECT`
- `os`
- `rich.console.Console`
- `rich.console.Group`
- `rich.live.Live`
- `rich.table.Table`
- `rich.text.Text`
- `sys`
- `time`
- `typer`
- `typing.Annotated`
- `typing.Optional`
- `typing.TYPE_CHECKING`

## Functions (5)

### make_rich_monitor_table

**Signature**: `utils.live_run_monitor.make_rich_monitor_table(runs: list, score_metric: str = ...) -> Table`

**Documentation**: Create rich table for run monitoring.

**Location**: line 80

### create_run_banner

**Signature**: `utils.live_run_monitor.create_run_banner(group: Optional[str], name_filter: Optional[str], runs: list, display_limit: int = ..., score_metric: str = ...)`

**Documentation**: Create a banner with run information.

**Location**: line 138

### live_monitor_runs

**Signature**: `utils.live_run_monitor.live_monitor_runs(group: Optional[str] = ..., name_filter: Optional[str] = ..., refresh_interval: int = ..., entity: str = ..., project: str = ..., clear_screen: bool = ..., display_limit: int = ..., fetch_limit: int = ..., score_metric: str = ...) -> Any`

**Documentation**: Live monitor runs with rich terminal display.

Args:
    fetch_limit: Maximum number of runs to fetch from WandB (default: 50)
    display_limit: Maximum number of runs to display in table (default: 10)

**Location**: line 229

### live_monitor_runs_test

**Signature**: `utils.live_run_monitor.live_monitor_runs_test(group: Optional[str] = ..., refresh_interval: int = ..., clear_screen: bool = ..., display_limit: int = ...) -> Any`

**Documentation**: Test mode for live run monitoring with mock data.

**Location**: line 339

### cli

**Signature**: `utils.live_run_monitor.cli(ctx: Any, group: Annotated = ..., name_filter: Annotated = ..., refresh: Annotated = ..., entity: Annotated = ..., project: Annotated = ..., test: Annotated = ..., no_clear: Annotated = ..., fetch_limit: Annotated = ..., display_limit: Annotated = ..., score_metric: Annotated = ...) -> Any`

**Documentation**: Default command for the live run monitor app.

**Location**: line 433

