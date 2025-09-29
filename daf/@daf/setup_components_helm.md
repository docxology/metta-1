# setup.components.helm

**Module**: `setup.components.helm`

**Source**: `metta/setup/components/helm.py`

**Imports**:
- `metta.setup.components.base.SetupModule`
- `metta.setup.registry.register_module`
- `metta.setup.utils.info`
- `shutil`

## Classes (1)

### HelmSetup

**Class**: `setup.components.helm.HelmSetup`

**Constructor**: `HelmSetup()`

**Methods**: 5

#### description

**Signature**: `HelmSetup.description(self) -> str`

**Location**: line 16

#### dependencies

**Signature**: `HelmSetup.dependencies(self) -> list[str]`

**Location**: line 19

#### get_installed_plugins

**Signature**: `HelmSetup.get_installed_plugins(self) -> list[str]`

**Location**: line 22

#### check_installed

**Signature**: `HelmSetup.check_installed(self) -> bool`

**Location**: line 29

#### install

**Signature**: `HelmSetup.install(self, non_interactive: bool = ..., force: bool = ...) -> Any`

**Location**: line 39


