# setup.components.codebot

**Module**: `setup.components.codebot`

**Source**: `metta/setup/components/codebot.py`

**Imports**:
- `metta.setup.components.base.SetupModule`
- `metta.setup.registry.register_module`
- `metta.setup.utils.info`
- `metta.setup.utils.success`
- `metta.setup.utils.warning`
- `subprocess`

## Classes (1)

### CodebotSetup

**Class**: `setup.components.codebot.CodebotSetup`

**Constructor**: `CodebotSetup()`

**Methods**: 3

#### description

**Signature**: `CodebotSetup.description(self) -> str`

**Location**: line 13

#### check_installed

**Signature**: `CodebotSetup.check_installed(self) -> bool`

**Documentation**: Check if codebot is installed.

**Location**: line 16

#### install

**Signature**: `CodebotSetup.install(self, non_interactive: bool = ..., force: bool = ...) -> Any`

**Documentation**: Install codebot as a uv tool.

**Location**: line 24


