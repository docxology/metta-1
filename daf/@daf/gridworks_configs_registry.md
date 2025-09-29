# gridworks.configs.registry

**Module**: `gridworks.configs.registry`

**Source**: `metta/gridworks/configs/registry.py`

**Imports**:
- `__future__.annotations`
- `ast`
- `dataclasses.dataclass`
- `inspect`
- `logging`
- `metta.common.util.fs.get_repo_root`
- `metta.gridworks.configs.lsp.LSPClient`
- `mettagrid.config.Config`
- `mettagrid.util.module.load_symbol`
- `pathlib.Path`
- `re`
- `typing.Callable`
- `typing.Literal`
- `typing.cast`
- `typing.get_args`

## Classes (2)

### ConfigMaker

**Class**: `gridworks.configs.registry.ConfigMaker`

**Constructor**: `ConfigMaker()`

**Documentation**: Represents a function that makes a Config object, and its metadata.

**Methods**: 3

#### path

**Signature**: `ConfigMaker.path(self) -> str`

**Location**: line 59

#### to_dict

**Signature**: `ConfigMaker.to_dict(self) -> dict`

**Location**: line 62

#### from_path

**Signature**: `ConfigMaker.from_path(cls, path: str, return_type: ConfigMakerKind, line: int) -> ConfigMaker`

**Location**: line 71


### ConfigMakerRegistry

**Class**: `gridworks.configs.registry.ConfigMakerRegistry`

**Constructor**: `ConfigMakerRegistry(self, root_dir: Any = ...)`

**Documentation**: Registry of all config makers.

**Methods**: 4

#### load_file_config_makers

**Signature**: `ConfigMakerRegistry.load_file_config_makers(self, file_path: Path) -> list[ConfigMaker]`

**Location**: line 116

#### size

**Signature**: `ConfigMakerRegistry.size(self) -> int`

**Location**: line 161

#### grouped_by_kind

**Signature**: `ConfigMakerRegistry.grouped_by_kind(self) -> dict`

**Location**: line 164

#### get_by_path

**Signature**: `ConfigMakerRegistry.get_by_path(self, path: str) -> Any`

**Location**: line 172


## Functions (2)

### hover_value_to_return_type

**Signature**: `gridworks.configs.registry.hover_value_to_return_type(hover_value: str) -> str`

**Location**: line 30

### check_return_type

**Signature**: `gridworks.configs.registry.check_return_type(return_type: str) -> Any`

**Location**: line 39

