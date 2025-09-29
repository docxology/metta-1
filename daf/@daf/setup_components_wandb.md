# setup.components.wandb

**Module**: `setup.components.wandb`

**Source**: `metta/setup/components/wandb.py`

**Imports**:
- `metta.common.util.constants.METTA_WANDB_ENTITY`
- `metta.common.util.constants.METTA_WANDB_PROJECT`
- `metta.setup.components.base.SetupModule`
- `metta.setup.profiles.UserType`
- `metta.setup.registry.register_module`
- `metta.setup.saved_settings.get_saved_settings`
- `metta.setup.utils.info`
- `metta.setup.utils.success`
- `metta.setup.utils.warning`
- `os`
- `re`
- `subprocess`

## Classes (1)

### WandbSetup

**Class**: `setup.components.wandb.WandbSetup`

**Constructor**: `WandbSetup()`

**Methods**: 6

#### description

**Signature**: `WandbSetup.description(self) -> str`

**Location**: line 18

#### check_installed

**Signature**: `WandbSetup.check_installed(self) -> bool`

**Location**: line 21

#### install

**Signature**: `WandbSetup.install(self, non_interactive: bool = ..., force: bool = ...) -> Any`

**Documentation**: Set up Weights & Biases authentication and configuration.

Handles different user types:
- SOFTMAX: Uses internal W&B setup
- SOFTMAX_DOCKER: Expects W&B access via environment variables
- Others: Provides guidance for manual setup

Args:
    non_interactive: If True, skip interactive authentication prompts

**Location**: line 32

#### check_connected_as

**Signature**: `WandbSetup.check_connected_as(self) -> Any`

**Location**: line 83

#### can_remediate_connected_status_with_install

**Signature**: `WandbSetup.can_remediate_connected_status_with_install(self) -> bool`

**Location**: line 97

#### to_config_settings

**Signature**: `WandbSetup.to_config_settings(self) -> dict`

**Location**: line 100


