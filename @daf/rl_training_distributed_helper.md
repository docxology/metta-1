# rl.training.distributed_helper

**Module**: `rl.training.distributed_helper`

**Source**: `metta/rl/training/distributed_helper.py`

**Imports**:
- `metta.agent.policy.DistributedPolicy`
- `metta.agent.policy.Policy`
- `metta.common.util.log_config.getRankAwareLogger`
- `metta.rl.system_config.SystemConfig`
- `metta.rl.trainer_config.TrainerConfig`
- `metta.rl.training.TrainingEnvironmentConfig`
- `mettagrid.config.Config`
- `os`
- `torch`
- `torch.distributed`
- `typing.Any`
- `typing.Optional`

## Classes (2)

### TorchDistributedConfig

**Class**: `rl.training.distributed_helper.TorchDistributedConfig`

**Constructor**: `TorchDistributedConfig()`

### DistributedHelper

**Class**: `rl.training.distributed_helper.DistributedHelper`

**Constructor**: `DistributedHelper(self, system_cfg: SystemConfig)`

**Methods**: 14

#### is_distributed

**Signature**: `DistributedHelper.is_distributed(self) -> bool`

**Location**: line 104

#### is_master

**Signature**: `DistributedHelper.is_master(self) -> bool`

**Location**: line 107

#### get_world_size

**Signature**: `DistributedHelper.get_world_size(self) -> int`

**Location**: line 110

#### get_rank

**Signature**: `DistributedHelper.get_rank(self) -> int`

**Location**: line 113

#### scale_batch_config

**Signature**: `DistributedHelper.scale_batch_config(self, trainer_cfg: TrainerConfig, env_cfg: TrainingEnvironmentConfig) -> Any`

**Documentation**: Scale batch sizes for distributed training if configured.

When scale_batches_by_world_size is True, this divides batch sizes
by the world size to maintain consistent global batch size across
different numbers of GPUs.

Args:
    trainer_cfg: Trainer configuration to modify in-place
    env_cfg: Optional environment configuration to modify

**Location**: line 116

#### wrap_policy

**Signature**: `DistributedHelper.wrap_policy(self, policy: Policy, device: Optional[torch] = ...) -> Any`

**Documentation**: Wrap policy for distributed training if needed.

Args:
    policy: Policy to wrap
    device: Device to use (defaults to self.config.device)

Returns:
    Wrapped policy if distributed, original otherwise

**Location**: line 151

#### synchronize

**Signature**: `DistributedHelper.synchronize(self) -> Any`

**Documentation**: Synchronize across all distributed processes.

**Location**: line 171

#### broadcast_from_master

**Signature**: `DistributedHelper.broadcast_from_master(self, obj: Any) -> Any`

**Documentation**: Broadcast object from master to all processes.

**Location**: line 176

#### should_log

**Signature**: `DistributedHelper.should_log(self) -> bool`

**Documentation**: Check if this process should perform logging.

**Location**: line 185

#### should_checkpoint

**Signature**: `DistributedHelper.should_checkpoint(self) -> bool`

**Documentation**: Check if this process should save checkpoints.

**Location**: line 189

#### should_evaluate

**Signature**: `DistributedHelper.should_evaluate(self) -> bool`

**Documentation**: Check if this process should run evaluation.

**Location**: line 193

#### all_gather

**Signature**: `DistributedHelper.all_gather(self, tensor: Any) -> list[torch]`

**Documentation**: Gather tensors from all processes.

**Location**: line 197

#### all_reduce

**Signature**: `DistributedHelper.all_reduce(self, tensor: Any, op: Any = ...) -> Any`

**Documentation**: Reduce tensor across all processes.

Args:
    tensor: Tensor to reduce
    op: Reduction operation (default: SUM)

Returns:
    Reduced tensor (in-place operation)

**Location**: line 206

#### cleanup

**Signature**: `DistributedHelper.cleanup(self) -> Any`

**Documentation**: Destroy the torch distributed process group if initialized.

**Location**: line 220


