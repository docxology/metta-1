# rl.advantage

**Module**: `rl.advantage`

**Source**: `metta/rl/advantage.py`

**Imports**:
- `contextlib.nullcontext`
- `einops`
- `importlib`
- `metta.rl.mps`
- `torch`
- `torch.Tensor`

## Functions (2)

### compute_advantage

**Signature**: `rl.advantage.compute_advantage(values: Tensor, rewards: Tensor, dones: Tensor, importance_sampling_ratio: Tensor, advantages: Tensor, gamma: float, gae_lambda: float, vtrace_rho_clip: float, vtrace_c_clip: float, device: Any) -> Tensor`

**Documentation**: CUDA kernel for puffer advantage with automatic CPU & MPS fallback.

**Location**: line 18

### normalize_advantage_distributed

**Signature**: `rl.advantage.normalize_advantage_distributed(adv: Tensor, norm_adv: bool = ...) -> Tensor`

**Documentation**: Normalize advantages with distributed training support while preserving shape.

**Location**: line 61

