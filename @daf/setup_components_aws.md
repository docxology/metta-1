# setup.components.aws

**Module**: `setup.components.aws`

**Source**: `metta/setup/components/aws.py`

**Imports**:
- `metta.common.util.constants.SOFTMAX_S3_POLICY_PREFIX`
- `metta.setup.components.base.SetupModule`
- `metta.setup.profiles.UserType`
- `metta.setup.registry.register_module`
- `metta.setup.saved_settings.get_saved_settings`
- `metta.setup.utils.info`

## Classes (1)

### AWSSetup

**Class**: `setup.components.aws.AWSSetup`

**Constructor**: `AWSSetup()`

**Methods**: 6

#### description

**Signature**: `AWSSetup.description(self) -> str`

**Location**: line 14

#### check_installed

**Signature**: `AWSSetup.check_installed(self) -> bool`

**Location**: line 17

#### install

**Signature**: `AWSSetup.install(self, non_interactive: bool = ..., force: bool = ...) -> Any`

**Documentation**: Set up AWS CLI configuration and credentials.

For softmax-docker profile, skips setup as AWS access should be provided
via IAM roles or environment variables. For other profiles, provides
guidance on configuring AWS CLI.

Args:
    non_interactive: If True, skip interactive configuration prompts

**Location**: line 25

#### check_connected_as

**Signature**: `AWSSetup.check_connected_as(self) -> Any`

**Location**: line 53

#### can_remediate_connected_status_with_install

**Signature**: `AWSSetup.can_remediate_connected_status_with_install(self) -> bool`

**Location**: line 64

#### to_config_settings

**Signature**: `AWSSetup.to_config_settings(self) -> dict`

**Location**: line 67


