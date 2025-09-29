# cogworks.curriculum.stats

**Module**: `cogworks.curriculum.stats`

**Source**: `metta/cogworks/curriculum/stats.py`

**Imports**:
- `abc.ABC`
- `abc.abstractmethod`
- `collections.defaultdict`
- `collections.deque`
- `numpy`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`

## Classes (2)

### StatsLogger

**Class**: `cogworks.curriculum.stats.StatsLogger`

**Constructor**: `StatsLogger(self, enable_detailed_logging: bool = ...)`

**Documentation**: Base class for curriculum statistics logging.

Provides consistent interface for all curriculum components to report
statistics with caching, prefixing, and detailed logging controls.

**Methods**: 4

#### get_base_stats

**Signature**: `StatsLogger.get_base_stats(self) -> Dict`

**Documentation**: Get basic statistics that all algorithms should provide.

**Location**: line 38

#### get_detailed_stats

**Signature**: `StatsLogger.get_detailed_stats(self) -> Dict`

**Documentation**: Get detailed statistics (expensive operations).

Only computed when enable_detailed_logging=True.
Override in subclasses to provide detailed metrics.

**Location**: line 42

#### invalidate_cache

**Signature**: `StatsLogger.invalidate_cache(self)`

**Documentation**: Invalidate the stats cache.

**Location**: line 50

#### stats

**Signature**: `StatsLogger.stats(self, prefix: str = ...) -> Dict`

**Documentation**: Get all statistics with optional prefix.

Args:
    prefix: String to prepend to all stat keys

Returns:
    Dictionary of statistics with prefixed keys

**Location**: line 54


### SliceAnalyzer

**Class**: `cogworks.curriculum.stats.SliceAnalyzer`

**Constructor**: `SliceAnalyzer(self, max_slice_axes: int = ..., enable_detailed_logging: bool = ...)`

**Documentation**: Analyzes probability distributions across parameter slices.

Tracks task completion patterns across different parameter dimensions
to understand curriculum coverage and learning patterns. "Slice" refers
to cross-sections of the parameter space being analyzed.

**Methods**: 7

#### extract_slice_values

**Signature**: `SliceAnalyzer.extract_slice_values(self, task) -> Dict`

**Documentation**: Extract slice values from a task's environment configuration.

**Location**: line 121

#### update_task_completion

**Signature**: `SliceAnalyzer.update_task_completion(self, task_id: int, slice_values: Dict, score: float) -> Any`

**Documentation**: Update slice analysis with task completion data.

Args:
    task_id: Unique task identifier
    slice_values: Parameter slice values for this task (e.g., {"map_size": "large", "num_agents": 4})
    score: Task completion score

**Location**: line 134

#### get_slice_distribution_stats

**Signature**: `SliceAnalyzer.get_slice_distribution_stats(self) -> Dict`

**Documentation**: Get probability distribution statistics across parameter slices.

**Location**: line 165

#### get_underexplored_regions

**Signature**: `SliceAnalyzer.get_underexplored_regions(self, slice_name: str) -> List[int]`

**Documentation**: Get bin indices for underexplored regions in a slice.

**Location**: line 248

#### get_base_stats

**Signature**: `SliceAnalyzer.get_base_stats(self) -> Dict`

**Documentation**: Get basic slice analysis statistics.

**Location**: line 267

#### get_detailed_stats

**Signature**: `SliceAnalyzer.get_detailed_stats(self) -> Dict`

**Documentation**: Get detailed slice distribution statistics (expensive).

**Location**: line 280

#### remove_task

**Signature**: `SliceAnalyzer.remove_task(self, task_id: int) -> Any`

**Documentation**: Remove task from slice tracking.

**Location**: line 311


