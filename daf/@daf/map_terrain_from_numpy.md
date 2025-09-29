# map.terrain_from_numpy

**Module**: `map.terrain_from_numpy`

**Source**: `metta/map/terrain_from_numpy.py`

**Imports**:
- `boto3`
- `botocore.exceptions.NoCredentialsError`
- `filelock.FileLock`
- `metta.common.util.log_config.getRankAwareLogger`
- `metta.utils.uri.ParsedURI`
- `mettagrid.map_builder.map_builder.GameMap`
- `mettagrid.map_builder.map_builder.MapBuilder`
- `mettagrid.map_builder.map_builder.MapBuilderConfig`
- `numpy`
- `os`
- `pydantic.ConfigDict`
- `pydantic.Field`
- `random`
- `typing.Optional`
- `zipfile`

## Classes (3)

### TerrainFromNumpy

**Class**: `map.terrain_from_numpy.TerrainFromNumpy`

**Constructor**: `TerrainFromNumpy(self, config: Config)`

**Documentation**: This class is used to load a terrain environment from numpy arrays on s3.

It's not a MapGen scene, because we don't know the grid size until we load the file.

**Methods**: 4

#### setup

**Signature**: `TerrainFromNumpy.setup(self)`

**Location**: line 69

#### get_valid_positions

**Signature**: `TerrainFromNumpy.get_valid_positions(self, level)`

**Location**: line 88

#### clean_grid

**Signature**: `TerrainFromNumpy.clean_grid(self, grid)`

**Location**: line 112

#### build

**Signature**: `TerrainFromNumpy.build(self)`

**Location**: line 127


### NavigationFromNumpy

**Class**: `map.terrain_from_numpy.NavigationFromNumpy`

**Constructor**: `NavigationFromNumpy(self, config: Any)`

**Methods**: 1

#### build

**Signature**: `NavigationFromNumpy.build(self)`

**Location**: line 135


### InContextLearningFromNumpy

**Class**: `map.terrain_from_numpy.InContextLearningFromNumpy`

**Constructor**: `InContextLearningFromNumpy(self, config: Any)`

**Methods**: 1

#### build

**Signature**: `InContextLearningFromNumpy.build(self)`

**Location**: line 171


## Functions (2)

### pick_random_file

**Signature**: `map.terrain_from_numpy.pick_random_file(path, rng)`

**Location**: line 21

### download_from_s3

**Signature**: `map.terrain_from_numpy.download_from_s3(s3_path: str, save_path: str)`

**Location**: line 33

