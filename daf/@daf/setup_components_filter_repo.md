# setup.components.filter_repo

**Module**: `setup.components.filter_repo`

**Source**: `metta/setup/components/filter_repo.py`

**Imports**:
- `metta.setup.components.base.SetupModule`
- `metta.setup.registry.register_module`
- `metta.setup.utils.error`
- `metta.setup.utils.info`
- `metta.setup.utils.success`
- `pathlib.Path`
- `subprocess`
- `tempfile`

## Classes (1)

### FilterRepoSetup

**Class**: `setup.components.filter_repo.FilterRepoSetup`

**Constructor**: `FilterRepoSetup()`

**Methods**: 5

#### name

**Signature**: `FilterRepoSetup.name(self) -> str`

**Location**: line 15

#### description

**Signature**: `FilterRepoSetup.description(self) -> str`

**Location**: line 19

#### check_installed

**Signature**: `FilterRepoSetup.check_installed(self) -> bool`

**Documentation**: Check if git-filter-repo is installed.

**Location**: line 22

#### install

**Signature**: `FilterRepoSetup.install(self, non_interactive: bool = ..., force: bool = ...) -> Any`

**Documentation**: Install git-filter-repo.

**Location**: line 30

#### run

**Signature**: `FilterRepoSetup.run(self, args: list[str]) -> Any`

**Documentation**: Run filter-repo commands via metta.

**Location**: line 108


