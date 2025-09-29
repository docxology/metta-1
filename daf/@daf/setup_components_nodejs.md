# setup.components.nodejs

**Module**: `setup.components.nodejs`

**Source**: `metta/setup/components/nodejs.py`

**Imports**:
- `metta.setup.components.base.SetupModule`
- `metta.setup.registry.register_module`
- `metta.setup.utils.info`
- `metta.setup.utils.warning`
- `os`
- `platform`
- `re`
- `shutil`
- `subprocess`

## Classes (1)

### NodejsSetup

**Class**: `setup.components.nodejs.NodejsSetup`

**Constructor**: `NodejsSetup()`

**Methods**: 4

#### description

**Signature**: `NodejsSetup.description(self) -> str`

**Location**: line 15

#### dependencies

**Signature**: `NodejsSetup.dependencies(self) -> list[str]`

**Location**: line 18

#### check_installed

**Signature**: `NodejsSetup.check_installed(self) -> bool`

**Location**: line 24

#### install

**Signature**: `NodejsSetup.install(self, non_interactive: bool = ..., force: bool = ...) -> Any`

**Location**: line 73


