# sim.map_preview

**Module**: `sim.map_preview`

**Source**: `metta/sim/map_preview.py`

**Imports**:
- `json`
- `logging`
- `metta.common.util.constants.METTASCOPE_REPLAY_URL`
- `metta.common.util.fs.get_repo_root`
- `metta.utils.file.write_file`
- `mettagrid.MettaGridEnv`
- `mettagrid.config.mettagrid_config.MettaGridConfig`
- `os`
- `tempfile`
- `typing.Optional`
- `wandb`
- `wandb.sdk.wandb_run`
- `zlib`

## Functions (3)

### write_map_preview_file

**Signature**: `sim.map_preview.write_map_preview_file(preview_path: str, env: MettaGridEnv, gzipped: bool)`

**Location**: line 20

### write_local_map_preview

**Signature**: `sim.map_preview.write_local_map_preview(env: MettaGridEnv)`

**Location**: line 43

### upload_map_preview

**Signature**: `sim.map_preview.upload_map_preview(s3_path: str, env_cfg: MettaGridConfig, wandb_run: Optional[wandb_run] = ...)`

**Documentation**: Builds a map preview of the simulation environment and uploads it to S3.

Args:
    cfg: Configuration for the simulation
    s3_path: Path to upload the map preview to
    wandb_run: Weights & Biases run object for logging

**Location**: line 57

