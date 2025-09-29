# setup.metta_cli

**Module**: `setup.metta_cli`

**Source**: `metta/setup/metta_cli.py`

**Imports**:
- `metta.common.util.fs.get_repo_root`
- `metta.setup.components.base.SetupModuleStatus`
- `metta.setup.local_commands.app`
- `metta.setup.symlink_setup.app`
- `metta.setup.tools.book.app`
- `metta.setup.utils.debug`
- `metta.setup.utils.error`
- `metta.setup.utils.info`
- `metta.setup.utils.success`
- `metta.setup.utils.warning`
- `metta.tools.utils.auto_config.auto_policy_storage_decision`
- `metta.utils.live_run_monitor.app`
- `pathlib.Path`
- `re`
- `rich.console.Console`
- `rich.progress.Progress`
- `rich.progress.SpinnerColumn`
- `rich.progress.TextColumn`
- `rich.table.Table`
- `shutil`
- `softmax.dashboard.report.app`
- `subprocess`
- `sys`
- `typer`
- `typing.Annotated`
- `typing.Optional`
- `typing.TYPE_CHECKING`

## Classes (1)

### MettaCLI

**Class**: `setup.metta_cli.MettaCLI`

**Constructor**: `MettaCLI(self)`

**Methods**: 1

#### setup_wizard

**Signature**: `MettaCLI.setup_wizard(self, non_interactive: bool = ...)`

**Location**: line 60


## Functions (19)

### cmd_configure

**Signature**: `setup.metta_cli.cmd_configure(component: Annotated = ..., profile: Annotated = ..., non_interactive: Annotated = ...)`

**Documentation**: Configure Metta settings.

**Location**: line 195

### configure_component

**Signature**: `setup.metta_cli.configure_component(component_name: str)`

**Location**: line 228

### cmd_install

**Signature**: `setup.metta_cli.cmd_install(components: Annotated = ..., profile: Annotated = ..., force: Annotated = ..., no_clean: Annotated = ..., non_interactive: Annotated = ..., check_status: Annotated = ...)`

**Location**: line 258

### cmd_status

**Signature**: `setup.metta_cli.cmd_status(components: Annotated = ..., non_interactive: Annotated = ...)`

**Location**: line 312

### cmd_run

**Signature**: `setup.metta_cli.cmd_run(component: Annotated, args: Annotated = ...)`

**Location**: line 422

### cmd_clean

**Signature**: `setup.metta_cli.cmd_clean(verbose: Annotated = ...)`

**Location**: line 440

### cmd_publish

**Signature**: `setup.metta_cli.cmd_publish(package: Annotated, version_override: Annotated = ..., dry_run: Annotated = ..., remote: Annotated = ..., force: Annotated = ...)`

**Location**: line 465

### cmd_lint

**Signature**: `setup.metta_cli.cmd_lint(files: Annotated = ..., fix: Annotated = ..., staged: Annotated = ...)`

**Location**: line 566

### cmd_ci

**Signature**: `setup.metta_cli.cmd_ci()`

**Location**: line 613

### cmd_benchmark

**Signature**: `setup.metta_cli.cmd_benchmark()`

**Documentation**: Run performance benchmarks for the mettagrid package.

**Location**: line 648

### cmd_test

**Signature**: `setup.metta_cli.cmd_test(ctx: Any)`

**Location**: line 669

### cmd_pytest

**Signature**: `setup.metta_cli.cmd_pytest(ctx: Any)`

**Location**: line 693

### cmd_tool

**Signature**: `setup.metta_cli.cmd_tool(tool_name: Annotated, ctx: Any)`

**Location**: line 711

### cmd_shell

**Signature**: `setup.metta_cli.cmd_shell()`

**Location**: line 728

### cmd_go

**Signature**: `setup.metta_cli.cmd_go(ctx: Any)`

**Location**: line 737

### cmd_report_env_details

**Signature**: `setup.metta_cli.cmd_report_env_details()`

**Documentation**: Report environment details.

**Location**: line 758

### cmd_clip

**Signature**: `setup.metta_cli.cmd_clip(ctx: Any)`

**Documentation**: Copy subsets of codebase for LLM contexts.

**Location**: line 776

### cmd_gridworks

**Signature**: `setup.metta_cli.cmd_gridworks(ctx: Any)`

**Location**: line 798

### main

**Signature**: `setup.metta_cli.main() -> Any`

**Location**: line 810

