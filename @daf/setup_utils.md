# setup.utils

**Module**: `setup.utils`

**Source**: `metta/setup/utils.py`

**Imports**:
- `contextlib.contextmanager`
- `functools`
- `importlib`
- `itertools`
- `pathlib.Path`
- `rich.console.Console`
- `textwrap`
- `threading`
- `time`
- `typing.TypeVar`

## Functions (5)

### get_console

**Signature**: `setup.utils.get_console() -> Console`

**Location**: line 17

### colorize

**Signature**: `setup.utils.colorize(message: str, color: str) -> str`

**Location**: line 25

### spinner

**Signature**: `setup.utils.spinner(message: str = ...)`

**Documentation**: Context manager that shows a spinner while executing code.

Usage:
    with spinner("Checking status..."):
        # Do some work
        time.sleep(2)

**Location**: line 45

### prompt_choice

**Signature**: `setup.utils.prompt_choice(prompt: str, choices: list[tuple], default: Any = ..., current: Any = ..., non_interactive: bool = ...) -> T`

**Documentation**: Prompt user to select from a list of choices with arrow key support.

Args:
    prompt: The prompt message
    choices: List of (value, description) tuples
    default: Default choice if user presses Enter
    current: Current value to highlight
    non_interactive: If True, automatically return default/current/first choice

Returns:
    The selected value

**Location**: line 72

### import_all_modules_from_subpackage

**Signature**: `setup.utils.import_all_modules_from_subpackage(package_name: str, subpackage: str) -> Any`

**Documentation**: Import all Python modules from a subpackage directory.

This is useful for auto-registering modules that use decorators.
Works with PEP 420 namespace packages.

Args:
    package_name: The parent package name (e.g., 'metta.setup')
    subpackage: The subpackage name (e.g., 'components')

**Location**: line 192

