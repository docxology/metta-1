# setup.components.system_packages.installers.brew

**Module**: `setup.components.system_packages.installers.brew`

**Source**: `metta/setup/components/system_packages/installers/brew.py`

**Imports**:
- `metta.setup.components.system_packages.installers.base.PackageInstaller`
- `metta.setup.components.system_packages.types.BrewPackageConfig`
- `metta.setup.utils.info`
- `subprocess`

## Classes (1)

### BrewInstaller

**Class**: `setup.components.system_packages.installers.brew.BrewInstaller`

**Constructor**: `BrewInstaller()`

**Methods**: 6

#### name

**Signature**: `BrewInstaller.name(self) -> str`

**Location**: line 10

#### is_available

**Signature**: `BrewInstaller.is_available(self) -> bool`

**Location**: line 13

#### get_installed_casks

**Signature**: `BrewInstaller.get_installed_casks(self) -> list[str]`

**Location**: line 23

#### install_casks

**Signature**: `BrewInstaller.install_casks(self, casks: list[str]) -> Any`

**Location**: line 26

#### check_installed

**Signature**: `BrewInstaller.check_installed(self, packages: list[BrewPackageConfig]) -> bool`

**Documentation**: Returns True when no changes are required.

**Location**: line 52

#### install

**Signature**: `BrewInstaller.install(self, packages: list[BrewPackageConfig]) -> Any`

**Location**: line 61


