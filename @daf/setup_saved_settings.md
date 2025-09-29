# setup.saved_settings

**Module**: `setup.saved_settings`

**Source**: `metta/setup/saved_settings.py`

**Imports**:
- `functools`
- `metta.setup.profiles.ComponentConfig`
- `metta.setup.profiles.PROFILE_DEFINITIONS`
- `metta.setup.profiles.UserType`
- `pathlib.Path`
- `typing.TypeVar`
- `typing.cast`
- `yaml`

## Classes (1)

### SavedSettings

**Class**: `setup.saved_settings.SavedSettings`

**Constructor**: `SavedSettings(self, config_path: Path) -> Any`

**Methods**: 12

#### exists

**Signature**: `SavedSettings.exists(self) -> bool`

**Location**: line 20

#### save

**Signature**: `SavedSettings.save(self) -> Any`

**Location**: line 29

#### get

**Signature**: `SavedSettings.get(self, key: str, default: T) -> T`

**Location**: line 33

#### set

**Signature**: `SavedSettings.set(self, key: str, value: T) -> Any`

**Location**: line 44

#### user_type

**Signature**: `SavedSettings.user_type(self, value: UserType) -> Any`

**Location**: line 61

#### config_version

**Signature**: `SavedSettings.config_version(self) -> int`

**Location**: line 65

#### is_custom_config

**Signature**: `SavedSettings.is_custom_config(self) -> bool`

**Location**: line 69

#### get_components

**Signature**: `SavedSettings.get_components(self) -> dict`

**Documentation**: Get the components configuration based on mode.

**Location**: line 72

#### is_component_enabled

**Signature**: `SavedSettings.is_component_enabled(self, component: str) -> bool`

**Location**: line 82

#### get_expected_connection

**Signature**: `SavedSettings.get_expected_connection(self, component: str) -> Any`

**Location**: line 87

#### apply_profile

**Signature**: `SavedSettings.apply_profile(self, profile: UserType) -> Any`

**Documentation**: Apply a profile configuration (uses dynamic resolution).

**Location**: line 92

#### setup_custom_profile

**Signature**: `SavedSettings.setup_custom_profile(self, base_profile: UserType) -> Any`

**Documentation**: Set up a custom configuration based on a profile.

**Location**: line 102


## Functions (1)

### get_saved_settings

**Signature**: `setup.saved_settings.get_saved_settings(config_path: Any = ...) -> SavedSettings`

**Location**: line 116

