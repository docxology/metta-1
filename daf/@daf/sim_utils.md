# sim.utils

**Module**: `sim.utils`

**Source**: `metta/sim/utils.py`

**Imports**:
- `bidict.bidict`
- `metta.app_backend.clients.stats_client.StatsClient`
- `metta.rl.checkpoint_manager.CheckpointManager`
- `uuid`

## Functions (1)

### get_or_create_policy_ids

**Signature**: `sim.utils.get_or_create_policy_ids(stats_client: StatsClient, policies: list[tuple], epoch_id: Any = ..., create: bool = ...) -> bidict`

**Documentation**: Get or create policy IDs in the stats database.

Args:
    stats_client: Client for stats database
    policies: List of (uri, description) tuples
    epoch_id: Optional epoch ID for policy creation
    create: Whether to create policies that don't exist

Returns:
    Bidirectional mapping of URI to policy UUID

**Location**: line 9

