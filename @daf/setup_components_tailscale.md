# setup.components.tailscale

**Module**: `setup.components.tailscale`

**Source**: `metta/setup/components/tailscale.py`

**Imports**:
- `json`
- `metta.setup.components.base.SetupModule`
- `metta.setup.registry.register_module`
- `metta.setup.saved_settings.UserType`
- `metta.setup.saved_settings.get_saved_settings`
- `metta.setup.utils.info`
- `metta.setup.utils.success`
- `metta.setup.utils.warning`
- `os`
- `platform`
- `subprocess`

## Classes (1)

### TailscaleSetup

**Class**: `setup.components.tailscale.TailscaleSetup`

**Constructor**: `TailscaleSetup()`

**Methods**: 5

#### description

**Signature**: `TailscaleSetup.description(self) -> str`

**Location**: line 17

#### check_installed

**Signature**: `TailscaleSetup.check_installed(self) -> bool`

**Location**: line 24

#### can_remediate_connected_status_with_install

**Signature**: `TailscaleSetup.can_remediate_connected_status_with_install(self) -> bool`

**Location**: line 32

#### check_connected_as

**Signature**: `TailscaleSetup.check_connected_as(self) -> Any`

**Location**: line 35

#### install

**Signature**: `TailscaleSetup.install(self, non_interactive: bool = ..., force: bool = ...) -> Any`

**Location**: line 61


