# rl.system_config

**Module**: `rl.system_config`

**Source**: `metta/rl/system_config.py`

**Imports**:
- `datetime.timedelta`
- `mettagrid.config.Config`
- `numpy`
- `os`
- `pathlib.Path`
- `platform`
- `pydantic.ConfigDict`
- `pydantic.Field`
- `random`
- `torch`
- `typing.ClassVar`
- `typing.Literal`

## Classes (1)

### SystemConfig

**Class**: `rl.system_config.SystemConfig`

**Constructor**: `SystemConfig()`

## Functions (4)

### guess_device

**Signature**: `rl.system_config.guess_device() -> str`

**Location**: line 15

### guess_vectorization

**Signature**: `rl.system_config.guess_vectorization() -> Literal`

**Location**: line 28

### guess_data_dir

**Signature**: `rl.system_config.guess_data_dir() -> Path`

**Location**: line 34

### seed_everything

**Signature**: `rl.system_config.seed_everything(system_cfg: SystemConfig)`

**Location**: line 57

