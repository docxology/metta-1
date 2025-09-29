# adaptive.stores.wandb

**Module**: `adaptive.stores.wandb`

**Source**: `metta/adaptive/stores/wandb.py`

**Imports**:
- `datetime.datetime`
- `datetime.timezone`
- `dateutil.parser`
- `json`
- `logging`
- `metta.adaptive.models.RunInfo`
- `metta.common.util.numpy_helpers.clean_numpy_types`
- `metta.common.util.retry.retry_on_exception`
- `typing.Any`
- `typing.List`
- `typing.Optional`
- `wandb`

## Classes (1)

### WandbStore

**Class**: `adaptive.stores.wandb.WandbStore`

**Constructor**: `WandbStore(self, entity: str, project: str)`

**Documentation**: WandB implementation of adaptive experiment store.

**Methods**: 3

#### init_run

**Signature**: `WandbStore.init_run(self, run_id: str, group: Any = ..., tags: Any = ..., initial_summary: Any = ...) -> Any`

**Documentation**: Initialize a new run in WandB with optional initial summary data.

**Location**: line 33

#### fetch_runs

**Signature**: `WandbStore.fetch_runs(self, filters: dict, limit: Optional[int] = ...) -> List[RunInfo]`

**Documentation**: Fetch runs matching filter criteria.

Args:
    filters: Dictionary of filter criteria
    limit: Maximum number of runs to fetch (None for no limit)

**Location**: line 77

#### update_run_summary

**Signature**: `WandbStore.update_run_summary(self, run_id: str, summary_update: dict) -> bool`

**Documentation**: Update run summary in WandB.

**Location**: line 123


## Functions (1)

### deep_clean

**Signature**: `adaptive.stores.wandb.deep_clean(obj)`

**Documentation**: Convert object to JSON-serializable types.

**Location**: line 305

