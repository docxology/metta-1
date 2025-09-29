# sweep.optimizer.protein

**Module**: `sweep.optimizer.protein`

**Source**: `metta/sweep/optimizer/protein.py`

**Imports**:
- `logging`
- `metta.common.util.numpy_helpers.clean_numpy_types`
- `metta.sweep.protein.Protein`
- `metta.sweep.protein_config.ProteinConfig`
- `typing.Any`

## Classes (1)

### ProteinOptimizer

**Class**: `sweep.optimizer.protein.ProteinOptimizer`

**Constructor**: `ProteinOptimizer(self, config: ProteinConfig)`

**Documentation**: Adapter for Protein optimizer.

**Methods**: 1

#### suggest

**Signature**: `ProteinOptimizer.suggest(self, observations: list[dict], n_suggestions: int = ...) -> list[dict]`

**Documentation**: Generate hyperparameter suggestions.

**Location**: line 24


