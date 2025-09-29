# rl.checkpoint_manager

**Module**: `rl.checkpoint_manager`

**Source**: `metta/rl/checkpoint_manager.py`

**Imports**:
- `collections.OrderedDict`
- `logging`
- `metta.agent.mocks.MockAgent`
- `metta.agent.policy.Policy`
- `metta.rl.puffer_policy._is_puffer_state_dict`
- `metta.rl.puffer_policy.load_pufferlib_checkpoint`
- `metta.rl.system_config.SystemConfig`
- `metta.tools.utils.auto_config.auto_policy_storage_decision`
- `metta.utils.file.local_copy`
- `metta.utils.file.write_file`
- `metta.utils.uri.ParsedURI`
- `os`
- `pathlib.Path`
- `pickle`
- `torch`
- `typing.Any`
- `typing.Dict`
- `typing.List`
- `typing.Optional`
- `typing.TypedDict`

## Classes (2)

### PolicyMetadata

**Class**: `rl.checkpoint_manager.PolicyMetadata`

**Constructor**: `PolicyMetadata()`

**Documentation**: Type definition for policy metadata returned by get_policy_metadata.

### CheckpointManager

**Class**: `rl.checkpoint_manager.CheckpointManager`

**Constructor**: `CheckpointManager(self, run: str, system_cfg: SystemConfig, cache_size: int = ...)`

**Documentation**: Checkpoint manager with filename-embedded metadata and LRU cache.

**Methods**: 11

#### remote_checkpoints_enabled

**Signature**: `CheckpointManager.remote_checkpoints_enabled(self) -> bool`

**Location**: line 314

#### clear_cache

**Signature**: `CheckpointManager.clear_cache(self)`

**Documentation**: Clear the instance's LRU cache.

**Location**: line 317

#### load_from_uri

**Signature**: `CheckpointManager.load_from_uri(uri: str, device: Any = ...) -> Policy`

**Documentation**: Load a policy from a URI (file://, s3://, or mock://).

Supports :latest selector for automatic resolution to the most recent checkpoint:
    file:///path/to/run/checkpoints/run_name:latest.pt
    s3://bucket/path/run/checkpoints/run_name:latest.pt

**Location**: line 322

#### normalize_uri

**Signature**: `CheckpointManager.normalize_uri(uri: str) -> str`

**Documentation**: Convert paths to file:// URIs. Keep other URI schemes as-is.

**Location**: line 357

#### get_policy_metadata

**Signature**: `CheckpointManager.get_policy_metadata(uri: str) -> PolicyMetadata`

**Documentation**: Extract metadata from policy URI.

**Location**: line 363

#### load_agent

**Signature**: `CheckpointManager.load_agent(self, epoch: Optional[int] = ..., device: Optional[torch] = ...)`

**Documentation**: Load agent checkpoint from local directory with LRU caching.

**Location**: line 394

#### load_trainer_state

**Signature**: `CheckpointManager.load_trainer_state(self) -> Optional[Dict]`

**Location**: line 421

#### save_agent

**Signature**: `CheckpointManager.save_agent(self, agent, epoch: int, metadata: Dict) -> str`

**Documentation**: Save agent checkpoint to disk and upload to remote storage if configured.

Returns URI of saved checkpoint (s3:// if remote prefix configured, otherwise file://).

**Location**: line 439

#### save_trainer_state

**Signature**: `CheckpointManager.save_trainer_state(self, optimizer, epoch: int, agent_step: int, stopwatch_state: Optional[Dict] = ..., curriculum_state: Optional[Dict] = ..., loss_states: Optional[Dict] = ...)`

**Location**: line 471

#### select_checkpoints

**Signature**: `CheckpointManager.select_checkpoints(self, strategy: str = ..., count: int = ...) -> List[str]`

**Documentation**: Select checkpoints and return their URIs.

Strategy can be "latest" or "all". Checkpoints are ordered purely by epoch.

**Location**: line 491

#### cleanup_old_checkpoints

**Signature**: `CheckpointManager.cleanup_old_checkpoints(self, keep_last_n: int = ...) -> int`

**Location**: line 505


## Functions (1)

### key_and_version

**Signature**: `rl.checkpoint_manager.key_and_version(uri: str) -> tuple`

**Documentation**: Extract key (run name) and version (epoch) from a policy URI.

Examples:
    "file:///tmp/my_run/checkpoints/my_run:v5.pt" -> ("my_run", 5)
    "s3://bucket/policies/my_run/checkpoints/my_run:v10.pt" -> ("my_run", 10)
    "file:///tmp/my_run/checkpoints/my_run:latest.pt" -> ("my_run", latest_epoch)
    "s3://bucket/policies/my_run/checkpoints/my_run:latest.pt" -> ("my_run", latest_epoch)
    "mock://test_agent" -> ("test_agent", 0)

The :latest selector automatically resolves to the highest epoch number
available in the checkpoint directory.

**Location**: line 34

