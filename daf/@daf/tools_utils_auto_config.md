# tools.utils.auto_config

**Module**: `tools.utils.auto_config`

**Source**: `metta/tools/utils/auto_config.py`

**Imports**:
- `dataclasses.dataclass`
- `datetime.datetime`
- `metta.common.util.collections.remove_falsey`
- `metta.common.util.collections.remove_none_values`
- `metta.common.util.constants.METTA_AWS_ACCOUNT_ID`
- `metta.common.wandb.context.WandbConfig`
- `metta.setup.components.aws.AWSSetup`
- `metta.setup.components.observatory_key.ObservatoryKeySetup`
- `metta.setup.components.wandb.WandbSetup`
- `os`
- `pydantic.Field`
- `pydantic_settings.BaseSettings`
- `pydantic_settings.SettingsConfigDict`
- `typing.Any`
- `typing.Literal`

## Classes (4)

### SupportedWandbEnvOverrides

**Class**: `tools.utils.auto_config.SupportedWandbEnvOverrides`

**Constructor**: `SupportedWandbEnvOverrides()`

**Methods**: 1

#### to_config_settings

**Signature**: `SupportedWandbEnvOverrides.to_config_settings(self) -> dict`

**Location**: line 26


### SupportedObservatoryEnvOverrides

**Class**: `tools.utils.auto_config.SupportedObservatoryEnvOverrides`

**Constructor**: `SupportedObservatoryEnvOverrides()`

**Methods**: 1

#### to_config_settings

**Signature**: `SupportedObservatoryEnvOverrides.to_config_settings(self) -> dict`

**Location**: line 75


### SupportedAwsEnvOverrides

**Class**: `tools.utils.auto_config.SupportedAwsEnvOverrides`

**Constructor**: `SupportedAwsEnvOverrides()`

**Methods**: 1

#### to_config_settings

**Signature**: `SupportedAwsEnvOverrides.to_config_settings(self) -> dict`

**Location**: line 103


### PolicyStorageDecision

**Class**: `tools.utils.auto_config.PolicyStorageDecision`

**Constructor**: `PolicyStorageDecision()`

**Methods**: 1

#### using_remote

**Signature**: `PolicyStorageDecision.using_remote(self) -> bool`

**Location**: line 143


## Functions (5)

### auto_wandb_config

**Signature**: `tools.utils.auto_config.auto_wandb_config(run: Any = ...) -> WandbConfig`

**Location**: line 49

### auto_stats_server_uri

**Signature**: `tools.utils.auto_config.auto_stats_server_uri() -> Any`

**Location**: line 88

### auto_replay_dir

**Signature**: `tools.utils.auto_config.auto_replay_dir() -> str`

**Location**: line 115

### auto_policy_storage_decision

**Signature**: `tools.utils.auto_config.auto_policy_storage_decision(run: Any = ...) -> PolicyStorageDecision`

**Location**: line 147

### auto_run_name

**Signature**: `tools.utils.auto_config.auto_run_name(prefix: Any = ...) -> str`

**Location**: line 173

