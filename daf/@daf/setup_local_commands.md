# setup.local_commands

**Module**: `setup.local_commands`

**Source**: `metta/setup/local_commands.py`

**Imports**:
- `metta.common.util.fs.get_repo_root`
- `metta.setup.tools.local.kind.kind_app`
- `metta.setup.utils.error`
- `metta.setup.utils.info`
- `pathlib.Path`
- `rich.console.Console`
- `subprocess`
- `sys`
- `typer`
- `typing.Annotated`

## Functions (6)

### build_policy_evaluator_img_internal

**Signature**: `setup.local_commands.build_policy_evaluator_img_internal(tag: str = ..., build_args: Any = ...)`

**Location**: line 33

### build_policy_evaluator_img

**Signature**: `setup.local_commands.build_policy_evaluator_img(ctx: Any, tag: Annotated = ...)`

**Location**: line 44

### build_app_backend_img

**Signature**: `setup.local_commands.build_app_backend_img()`

**Location**: line 58

### stats_server

**Signature**: `setup.local_commands.stats_server(ctx: Any)`

**Location**: line 64

### observatory

**Signature**: `setup.local_commands.observatory(ctx: Any)`

**Location**: line 85

### main

**Signature**: `setup.local_commands.main()`

**Location**: line 103

