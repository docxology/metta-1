# setup.components.system_packages.installers.apt

**Module**: `setup.components.system_packages.installers.apt`

**Source**: `metta/setup/components/system_packages/installers/apt.py`

**Imports**:
- `metta.setup.components.system_packages.installers.base.PackageInstaller`
- `metta.setup.components.system_packages.types.AptPackageConfig`
- `metta.setup.utils.info`
- `subprocess`

## Classes (1)

### AptInstaller

**Class**: `setup.components.system_packages.installers.apt.AptInstaller`

**Constructor**: `AptInstaller(self)`

**Methods**: 4

#### name

**Signature**: `AptInstaller.name(self) -> str`

**Location**: line 13

#### is_available

**Signature**: `AptInstaller.is_available(self) -> bool`

**Location**: line 16

#### check_installed

**Signature**: `AptInstaller.check_installed(self, packages: list[AptPackageConfig]) -> bool`

**Documentation**: Returns True when no changes are required.

**Location**: line 31

#### install

**Signature**: `AptInstaller.install(self, packages: list[AptPackageConfig]) -> Any`

**Location**: line 38


