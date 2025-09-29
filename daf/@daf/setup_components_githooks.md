# setup.components.githooks

**Module**: `setup.components.githooks`

**Source**: `metta/setup/components/githooks.py`

**Imports**:
- `enum.Enum`
- `metta.common.util.fs.get_file_hash`
- `metta.setup.components.base.SetupModule`
- `metta.setup.registry.register_module`
- `metta.setup.utils.colorize`
- `metta.setup.utils.error`
- `metta.setup.utils.info`
- `metta.setup.utils.prompt_choice`
- `metta.setup.utils.success`
- `os`
- `pathlib.Path`
- `subprocess`
- `sys`
- `tomllib`

## Classes (3)

### CommitHookMode

**Class**: `setup.components.githooks.CommitHookMode`

**Constructor**: `CommitHookMode()`

**Methods**: 3

#### get_description

**Signature**: `CommitHookMode.get_description(self) -> str`

**Location**: line 19

#### get_default

**Signature**: `CommitHookMode.get_default(cls) -> Any`

**Location**: line 28

#### parse

**Signature**: `CommitHookMode.parse(cls, value: Any) -> Any`

**Location**: line 32


### GitLeaksMode

**Class**: `setup.components.githooks.GitLeaksMode`

**Constructor**: `GitLeaksMode()`

**Methods**: 3

#### get_description

**Signature**: `GitLeaksMode.get_description(self) -> str`

**Location**: line 44

#### get_default

**Signature**: `GitLeaksMode.get_default(cls) -> Any`

**Location**: line 53

#### parse

**Signature**: `GitLeaksMode.parse(cls, value: Any) -> Any`

**Location**: line 57


### GitHooksSetup

**Class**: `setup.components.githooks.GitHooksSetup`

**Constructor**: `GitHooksSetup()`

**Methods**: 6

#### description

**Signature**: `GitHooksSetup.description(self) -> str`

**Location**: line 69

#### check_installed

**Signature**: `GitHooksSetup.check_installed(self) -> bool`

**Documentation**: Check if all hooks from devops/git-hooks are installed with matching content

**Location**: line 114

#### install

**Signature**: `GitHooksSetup.install(self, non_interactive: bool = ..., force: bool = ...) -> Any`

**Documentation**: Install git hooks by symlinking from devops/git-hooks to .git/hooks

**Location**: line 129

#### get_configuration_options

**Signature**: `GitHooksSetup.get_configuration_options(self) -> dict`

**Location**: line 159

#### configure

**Signature**: `GitHooksSetup.configure(self) -> Any`

**Location**: line 165

#### run

**Signature**: `GitHooksSetup.run(self, args: list[str]) -> Any`

**Location**: line 245


