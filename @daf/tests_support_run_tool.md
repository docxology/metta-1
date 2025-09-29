# tests_support.run_tool

**Module**: `tests_support.run_tool`

**Source**: `metta/tests_support/run_tool.py`

**Imports**:
- `__future__.annotations`
- `logging`
- `metta.common.tool.run_tool`
- `metta.common.util.log_config`
- `os`
- `signal`
- `sys`
- `typing.Mapping`
- `typing.NamedTuple`
- `warnings`

## Classes (2)

### _LoggerState

**Class**: `tests_support.run_tool._LoggerState`

**Constructor**: `_LoggerState()`

**Documentation**: Snapshot of a logger's mutable state for restoration.

### RunToolResult

**Class**: `tests_support.run_tool.RunToolResult`

**Constructor**: `RunToolResult()`

**Documentation**: Captured result from invoking the tool runner in-process.

## Functions (1)

### run_tool_in_process

**Signature**: `tests_support.run_tool.run_tool_in_process(*cli_args) -> RunToolResult`

**Documentation**: Invoke `metta.common.tool.run_tool.main()` without spawning a subprocess.

Parameters
----------
cli_args: str
    Arguments to pass to the CLI (after the entry point).
monkeypatch: pytest.MonkeyPatch
    Pytest monkeypatch fixture, used to adjust sys modules and env vars.
capsys: pytest.CaptureFixture[str]
    Capture fixture for stdout/stderr.
env_overrides: Mapping[str, str] | None
    Optional environment variables to inject for the duration of the call.
argv0: str
    Value to use for argv[0]; defaults to "tools/run.py" for consistency with scripts.

**Location**: line 84

