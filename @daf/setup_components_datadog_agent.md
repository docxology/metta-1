# setup.components.datadog_agent

**Module**: `setup.components.datadog_agent`

**Source**: `metta/setup/components/datadog_agent.py`

**Imports**:
- `metta.setup.components.base.SetupModule`
- `metta.setup.registry.register_module`
- `metta.setup.utils.error`
- `metta.setup.utils.info`
- `metta.setup.utils.success`
- `metta.setup.utils.warning`
- `os`
- `platform`
- `softmax.aws.secrets_manager.get_secretsmanager_secret`
- `subprocess`

## Classes (1)

### DatadogAgentSetup

**Class**: `setup.components.datadog_agent.DatadogAgentSetup`

**Constructor**: `DatadogAgentSetup()`

**Methods**: 5

#### name

**Signature**: `DatadogAgentSetup.name(self) -> str`

**Location**: line 16

#### dependencies

**Signature**: `DatadogAgentSetup.dependencies(self) -> list[str]`

**Location**: line 19

#### description

**Signature**: `DatadogAgentSetup.description(self) -> str`

**Location**: line 23

#### check_installed

**Signature**: `DatadogAgentSetup.check_installed(self) -> bool`

**Location**: line 30

#### install

**Signature**: `DatadogAgentSetup.install(self, non_interactive: bool = ..., force: bool = ...) -> Any`

**Location**: line 48


