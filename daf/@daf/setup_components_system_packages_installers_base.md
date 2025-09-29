# setup.components.system_packages.installers.base

**Module**: `setup.components.system_packages.installers.base`

**Source**: `metta/setup/components/system_packages/installers/base.py`

**Imports**:
- `abc.ABC`
- `abc.abstractmethod`
- `typing.Generic`
- `typing.TypeVar`

## Classes (1)

### PackageInstaller

**Class**: `setup.components.system_packages.installers.base.PackageInstaller`

**Constructor**: `PackageInstaller()`

**Methods**: 4

#### name

**Signature**: `PackageInstaller.name(self) -> str`

**Location**: line 10

#### is_available

**Signature**: `PackageInstaller.is_available(self) -> bool`

**Documentation**: Check if this package manager is available on the system.

**Location**: line 14

#### install

**Signature**: `PackageInstaller.install(self, packages: list[T]) -> Any`

**Location**: line 19

#### check_installed

**Signature**: `PackageInstaller.check_installed(self, packages: list[T]) -> bool`

**Location**: line 23


