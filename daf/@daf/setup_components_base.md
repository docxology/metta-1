# setup.components.base

**Module**: `setup.components.base`

**Source**: `metta/setup/components/base.py`

**Imports**:
- `abc.ABC`
- `abc.abstractmethod`
- `metta.common.util.fs.get_repo_root`
- `metta.setup.saved_settings.get_saved_settings`
- `metta.setup.utils.error`
- `os`
- `pathlib.Path`
- `pydantic.BaseModel`
- `subprocess`
- `typing.Any`
- `typing.TypeVar`

## Classes (2)

### SetupModuleStatus

**Class**: `setup.components.base.SetupModuleStatus`

**Constructor**: `SetupModuleStatus()`

### SetupModule

**Class**: `setup.components.base.SetupModule`

**Constructor**: `SetupModule(self)`

**Methods**: 17

#### name

**Signature**: `SetupModule.name(self) -> str`

**Location**: line 30

#### description

**Signature**: `SetupModule.description(self) -> str`

**Location**: line 35

#### setup_script_location

**Signature**: `SetupModule.setup_script_location(self) -> Any`

**Location**: line 39

#### check_installed

**Signature**: `SetupModule.check_installed(self) -> bool`

**Documentation**: Check if this module is already installed and configured and no changes are needed.

**Location**: line 47

#### is_enabled

**Signature**: `SetupModule.is_enabled(self) -> bool`

**Documentation**: Check if this module should be installed based on applicability and settings.

**Location**: line 51

#### dependencies

**Signature**: `SetupModule.dependencies(self) -> list[str]`

**Location**: line 57

#### install

**Signature**: `SetupModule.install(self, non_interactive: bool = ..., force: bool = ...) -> Any`

**Documentation**: Install this component.

This is called during a metta install if any of:
- the component is not installed
- the component is installed and SetupModule.install_once is False
- the component is installed and the user is running a force-install

Force-installs are likely called when the user is trying to repair an issue, so ideally this function
should self-doctor when force is True.

Args:
    non_interactive: If True, run in non-interactive mode without prompts

**Location**: line 62

#### run_command

**Signature**: `SetupModule.run_command(self, cmd: list[str], cwd: Any = ..., check: bool = ..., capture_output: bool = ..., input: Any = ..., env: Any = ..., non_interactive: Any = ...)`

**Documentation**: Execute a command with proper environment setup and non-interactive support.

This method handles command execution with automatic environment inheritance,
non-interactive mode configuration, and proper error handling. It ensures
commands run correctly in both interactive and CI/Docker environments.

Args:
    cmd: Command and arguments as a list of strings
    cwd: Working directory for the command (defaults to repo_root)
    check: Whether to raise CalledProcessError on non-zero exit codes
    capture_output: Whether to capture stdout/stderr
    input: Input to send to the command's stdin
    env: Additional environment variables (merged with os.environ)
    non_interactive: Force non-interactive mode (defaults to instance setting)

Returns:
    CompletedProcess object containing execution results

Raises:
    CalledProcessError: If check=True and command returns non-zero exit code
    FileNotFoundError: If the command executable is not found
    OSError: For other system-level execution errors

Note:
    In non-interactive mode, stdin is redirected to /dev/null and environment
    variables are set to prevent interactive prompts (DEBIAN_FRONTEND, etc.).

**Location**: line 84

#### run_script

**Signature**: `SetupModule.run_script(self, script_path: str, args: Any = ...)`

**Location**: line 154

#### check_connected_as

**Signature**: `SetupModule.check_connected_as(self) -> Any`

**Documentation**: Current account/profile/org the user is authenticated as, or None if not connected.

**Location**: line 165

#### can_remediate_connected_status_with_install

**Signature**: `SetupModule.can_remediate_connected_status_with_install(self) -> bool`

**Documentation**: If force-installing should be recommended to re-authenticate users when:
- check_installed is True and
- check_connected_as does not match the expected value

**Location**: line 172

#### get_configuration_options

**Signature**: `SetupModule.get_configuration_options(self) -> dict`

**Documentation**: Dict of {setting_name: (default_value, description)}

**Location**: line 180

#### configure

**Signature**: `SetupModule.configure(self) -> Any`

**Documentation**: This method is called by 'metta configure <component>'.
Override this to provide custom configuration logic.

**Location**: line 186

#### run

**Signature**: `SetupModule.run(self, args: list[str]) -> Any`

**Documentation**: Run a component-specific command.

This method is called by 'metta run <component> <args>'.
Override this to provide component-specific commands.

Args:
    args: Command arguments passed after the component name

**Location**: line 192

#### get_setting

**Signature**: `SetupModule.get_setting(self, key: str, default: T) -> T`

**Documentation**: Get a module-specific setting from the configuration.

Args:
    key: The setting key (will be prefixed with module name)
    default: Default value if setting not found

Returns:
    The setting value or default

**Location**: line 203

#### set_setting

**Signature**: `SetupModule.set_setting(self, key: str, value: Any) -> Any`

**Documentation**: Save a module-specific setting to the configuration.

Only saves if value differs from the default defined in get_configuration_options().

Args:
    key: The setting key (will be prefixed with module name)
    value: The value to save

**Location**: line 218

#### get_status

**Signature**: `SetupModule.get_status(self) -> SetupModuleStatus`

**Documentation**: Get the status of this module. Does not check if the module is enabled.

**Location**: line 273


