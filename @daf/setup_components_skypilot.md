# setup.components.skypilot

**Module**: `setup.components.skypilot`

**Source**: `metta/setup/components/skypilot.py`

**Imports**:
- `metta.common.util.constants.METTA_SKYPILOT_URL`
- `metta.setup.components.base.SetupModule`
- `metta.setup.registry.register_module`
- `metta.setup.saved_settings.get_saved_settings`
- `metta.setup.utils.info`
- `metta.setup.utils.success`
- `os`
- `signal`
- `subprocess`

## Classes (1)

### SkypilotSetup

**Class**: `setup.components.skypilot.SkypilotSetup`

**Constructor**: `SkypilotSetup()`

**Methods**: 6

#### dependencies

**Signature**: `SkypilotSetup.dependencies(self) -> list[str]`

**Location**: line 18

#### description

**Signature**: `SkypilotSetup.description(self) -> str`

**Location**: line 22

#### check_installed

**Signature**: `SkypilotSetup.check_installed(self) -> bool`

**Location**: line 25

#### install

**Signature**: `SkypilotSetup.install(self, non_interactive: bool = ..., force: bool = ...) -> Any`

**Location**: line 44

#### can_remediate_connected_status_with_install

**Signature**: `SkypilotSetup.can_remediate_connected_status_with_install(self) -> bool`

**Location**: line 93

#### check_connected_as

**Signature**: `SkypilotSetup.check_connected_as(self) -> Any`

**Location**: line 101


