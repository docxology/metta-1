# setup.components.notebookwidgets

**Module**: `setup.components.notebookwidgets`

**Source**: `metta/setup/components/notebookwidgets.py`

**Imports**:
- `metta.setup.components.base.SetupModule`
- `metta.setup.registry.register_module`
- `metta.setup.utils.info`
- `metta.setup.utils.warning`
- `subprocess`

## Classes (1)

### NotebookWidgetsSetup

**Class**: `setup.components.notebookwidgets.NotebookWidgetsSetup`

**Constructor**: `NotebookWidgetsSetup(self)`

**Methods**: 6

#### dependencies

**Signature**: `NotebookWidgetsSetup.dependencies(self) -> list[str]`

**Location**: line 18

#### description

**Signature**: `NotebookWidgetsSetup.description(self) -> str`

**Location**: line 22

#### should_install_widget

**Signature**: `NotebookWidgetsSetup.should_install_widget(self, widget: str) -> bool`

**Location**: line 29

#### should_build_widget

**Signature**: `NotebookWidgetsSetup.should_build_widget(self, widget: str) -> bool`

**Location**: line 34

#### check_installed

**Signature**: `NotebookWidgetsSetup.check_installed(self) -> bool`

**Location**: line 51

#### install

**Signature**: `NotebookWidgetsSetup.install(self, non_interactive: bool = ..., force: bool = ...) -> Any`

**Location**: line 59


