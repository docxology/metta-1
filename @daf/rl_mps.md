# rl.mps

**Module**: `rl.mps`

**Source**: `metta/rl/mps.py`

**Imports**:
- `torch`
- `torch.Tensor`

## Functions (1)

### advantage

**Signature**: `rl.mps.advantage(values: Tensor, rewards: Tensor, dones: Tensor, importance_sampling_ratio: Tensor, vtrace_rho_clip: float, vtrace_c_clip: float, gamma: float, gae_lambda: float, device: Any) -> Tensor`

**Documentation**: Native PyTorch implementation (MPS-compatible)

**Location**: line 5

