# setup.tools.book

**Module**: `setup.tools.book`

**Source**: `metta/setup/tools/book.py`

**Imports**:
- `metta.common.util.fs.get_repo_root`
- `metta.setup.utils.error`
- `metta.setup.utils.info`
- `metta.setup.utils.prompt_choice`
- `metta.setup.utils.success`
- `pathlib.Path`
- `rich.console.Console`
- `subprocess`
- `typer`
- `typing.Annotated`

## Functions (6)

### cmd_home

**Signature**: `setup.tools.book.cmd_home()`

**Documentation**: Open marimo home page.

**Location**: line 57

### cmd_open

**Signature**: `setup.tools.book.cmd_open(filename: Annotated = ...)`

**Documentation**: Open an existing notebook.

**Location**: line 64

### cmd_run

**Signature**: `setup.tools.book.cmd_run(filename: Annotated = ...)`

**Documentation**: Run a notebook in read-only mode.

**Location**: line 81

### cmd_new

**Signature**: `setup.tools.book.cmd_new(name: Annotated = ...)`

**Documentation**: Create a new notebook.

**Location**: line 98

### cmd_list

**Signature**: `setup.tools.book.cmd_list()`

**Documentation**: List all available notebooks.

**Location**: line 121

### main

**Signature**: `setup.tools.book.main()`

**Location**: line 133

