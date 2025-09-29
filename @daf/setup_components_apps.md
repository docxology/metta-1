# setup.components.apps

**Module**: `setup.components.apps`

**Source**: `metta/setup/components/apps.py`

**Imports**:
- `metta.common.util.fs.get_repo_root`
- `metta.setup.components.base.SetupModule`
- `metta.setup.components.system.get_package_installer`
- `metta.setup.components.system_packages.installers.brew.BrewInstaller`
- `metta.setup.registry.register_module`
- `os`
- `platform`
- `pydantic.main.BaseModel`
- `typing_extensions.override`
- `yaml`

## Classes (3)

### AppConfig

**Class**: `setup.components.apps.AppConfig`

**Constructor**: `AppConfig()`

### SystemAppsConfig

**Class**: `setup.components.apps.SystemAppsConfig`

**Constructor**: `SystemAppsConfig()`

### AppsSetup

**Class**: `setup.components.apps.AppsSetup`

**Constructor**: `AppsSetup()`

**Methods**: 5

#### description

**Signature**: `AppsSetup.description(self) -> str`

**Location**: line 33

#### dependencies

**Signature**: `AppsSetup.dependencies(self) -> list[str]`

**Location**: line 36

#### check_installed

**Signature**: `AppsSetup.check_installed(self) -> bool`

**Location**: line 40

#### is_applicable

**Signature**: `AppsSetup.is_applicable(self) -> bool`

**Location**: line 64

#### install

**Signature**: `AppsSetup.install(self, non_interactive: bool = ..., force: bool = ...) -> Any`

**Location**: line 68


## Functions (1)

### get_system_apps_config

**Signature**: `setup.components.apps.get_system_apps_config() -> SystemAppsConfig`

**Location**: line 24

