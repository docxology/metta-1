# setup.components.system

**Module**: `setup.components.system`

**Source**: `metta/setup/components/system.py`

**Imports**:
- `functools`
- `metta.common.util.collections.remove_falsey`
- `metta.common.util.fs.get_repo_root`
- `metta.setup.components.base.SetupModule`
- `metta.setup.components.system_packages.installers.base.PackageInstaller`
- `metta.setup.components.system_packages.installers.brew.BrewInstaller`
- `metta.setup.components.system_packages.types.SystemDepsConfig`
- `metta.setup.registry.register_module`
- `metta.setup.utils.error`
- `metta.setup.utils.info`
- `metta.setup.utils.success`
- `metta.setup.utils.warning`
- `platform`
- `subprocess`
- `sys`
- `typing_extensions.override`
- `yaml`

## Classes (1)

### SystemSetup

**Class**: `setup.components.system.SystemSetup`

**Constructor**: `SystemSetup()`

**Methods**: 3

#### description

**Signature**: `SystemSetup.description(self) -> str`

**Location**: line 39

#### check_installed

**Signature**: `SystemSetup.check_installed(self) -> bool`

**Location**: line 51

#### install

**Signature**: `SystemSetup.install(self, non_interactive: bool = ..., force: bool = ...) -> Any`

**Location**: line 64


## Functions (2)

### get_package_installer

**Signature**: `setup.components.system.get_package_installer() -> Any`

**Location**: line 20

### get_system_deps_config

**Signature**: `setup.components.system.get_system_deps_config() -> SystemDepsConfig`

**Location**: line 27

