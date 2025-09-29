# sweep.protein_config

**Module**: `sweep.protein_config`

**Source**: `metta/sweep/protein_config.py`

**Imports**:
- `mettagrid.config.Config`
- `pydantic.Field`
- `typing.Any`
- `typing.Dict`
- `typing.Literal`

## Classes (3)

### ParameterConfig

**Class**: `sweep.protein_config.ParameterConfig`

**Constructor**: `ParameterConfig()`

**Documentation**: Configuration for a single hyperparameter to optimize.

### ProteinSettings

**Class**: `sweep.protein_config.ProteinSettings`

**Constructor**: `ProteinSettings()`

**Documentation**: Settings for the Protein optimizer algorithm.

### ProteinConfig

**Class**: `sweep.protein_config.ProteinConfig`

**Constructor**: `ProteinConfig()`

**Documentation**: Configuration for Protein hyperparameter optimization.

**Methods**: 1

#### to_protein_dict

**Signature**: `ProteinConfig.to_protein_dict(self) -> dict`

**Documentation**: Convert to the dict format expected by Protein class.

Returns:
    Dictionary with flattened parameters and optimization settings

**Location**: line 67


