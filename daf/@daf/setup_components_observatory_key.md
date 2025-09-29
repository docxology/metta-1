# setup.components.observatory_key

**Module**: `setup.components.observatory_key`

**Source**: `metta/setup/components/observatory_key.py`

**Imports**:
- `metta.app_backend.clients.base_client.get_machine_token`
- `metta.common.util.constants.DEV_STATS_SERVER_URI`
- `metta.common.util.constants.PROD_STATS_SERVER_URI`
- `metta.setup.components.base.SetupModule`
- `metta.setup.registry.register_module`
- `metta.setup.saved_settings.get_saved_settings`
- `metta.setup.utils.error`
- `metta.setup.utils.info`
- `metta.setup.utils.success`
- `metta.setup.utils.warning`
- `os`
- `subprocess`

## Classes (2)

### ObservatoryKeySetup

**Class**: `setup.components.observatory_key.ObservatoryKeySetup`

**Constructor**: `ObservatoryKeySetup()`

**Methods**: 8

#### name

**Signature**: `ObservatoryKeySetup.name(self) -> str`

**Location**: line 19

#### description

**Signature**: `ObservatoryKeySetup.description(self) -> str`

**Location**: line 23

#### get_token

**Signature**: `ObservatoryKeySetup.get_token(self, server_url: Any = ...) -> Any`

**Documentation**: Get token for specific server using the shared implementation

**Location**: line 26

#### check_installed

**Signature**: `ObservatoryKeySetup.check_installed(self) -> bool`

**Location**: line 30

#### install

**Signature**: `ObservatoryKeySetup.install(self, non_interactive: bool = ..., force: bool = ...) -> Any`

**Location**: line 38

#### check_connected_as

**Signature**: `ObservatoryKeySetup.check_connected_as(self) -> Any`

**Location**: line 62

#### can_remediate_connected_status_with_install

**Signature**: `ObservatoryKeySetup.can_remediate_connected_status_with_install(self) -> bool`

**Location**: line 73

#### to_config_settings

**Signature**: `ObservatoryKeySetup.to_config_settings(self) -> dict`

**Location**: line 76


### ObservatoryKeyLocalSetup

**Class**: `setup.components.observatory_key.ObservatoryKeyLocalSetup`

**Constructor**: `ObservatoryKeyLocalSetup()`

**Methods**: 2

#### name

**Signature**: `ObservatoryKeyLocalSetup.name(self) -> str`

**Location**: line 89

#### description

**Signature**: `ObservatoryKeyLocalSetup.description(self) -> str`

**Location**: line 93


