# sim.thumbnail_automation

**Module**: `sim.thumbnail_automation`

**Source**: `metta/sim/thumbnail_automation.py`

**Imports**:
- `logging`
- `metta.utils.file`
- `mettagrid.mapgen.utils.thumbnail.generate_thumbnail_from_replay`
- `os`

## Functions (4)

### episode_id_to_s3_key

**Signature**: `sim.thumbnail_automation.episode_id_to_s3_key(episode_id: str) -> str`

**Documentation**: Convert episode_id to S3 key using unique episode-based naming (like replay files).

Args:
    episode_id: Unique episode ID (UUID) like "a1b2c3d4-e5f6-7890-abcd-ef1234567890"

Returns:
    S3 key like "a1b2c3d4-e5f6-7890-abcd-ef1234567890.png"

**Location**: line 17

### episode_id_to_s3_uri

**Signature**: `sim.thumbnail_automation.episode_id_to_s3_uri(episode_id: str) -> str`

**Documentation**: Convert episode_id to full S3 URI for use with metta.utils.file functions.

Args:
    episode_id: Unique episode ID (UUID) like "a1b2c3d4-e5f6-7890-abcd-ef1234567890"

Returns:
    Full S3 URI like "s3://softmax-public/policydash/evals/img/a1b2c3d4-e5f6-7890-abcd-ef1234567890.png"

**Location**: line 30

### upload_thumbnail_to_s3

**Signature**: `sim.thumbnail_automation.upload_thumbnail_to_s3(thumbnail_data: bytes, episode_id: str) -> tuple`

**Documentation**: Upload thumbnail data to S3 using project's file utilities.

Args:
    thumbnail_data: PNG image data as bytes
    episode_id: Unique episode ID for S3 key generation

Returns:
    Tuple of (success: bool, http_thumbnail_url: str | None)

**Location**: line 44

### maybe_generate_and_upload_thumbnail

**Signature**: `sim.thumbnail_automation.maybe_generate_and_upload_thumbnail(replay_data: dict, episode_id: str) -> tuple`

**Documentation**: Main automation entry point: generate and upload thumbnail for episode.

This function is called from simulation.py after a simulation completes.
It generates a unique thumbnail for each episode (like replay files),
eliminating the need for conflict checking or shared naming schemes.

Args:
    replay_data: Replay data from simulation's episode writer
    episode_id: Unique episode ID from simulation

Returns:
    Tuple of (success: bool, thumbnail_url: str | None)

**Location**: line 71

