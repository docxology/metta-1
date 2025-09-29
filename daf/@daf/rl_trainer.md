# rl.trainer

**Module**: `rl.trainer`

**Source**: `metta/rl/trainer.py`

**Imports**:
- `importlib`
- `metta.agent.policy.Policy`
- `metta.common.util.log_config.getRankAwareLogger`
- `metta.rl.trainer_config.TrainerConfig`
- `metta.rl.training.ComponentContext`
- `metta.rl.training.ContextCheckpointer`
- `metta.rl.training.CoreTrainingLoop`
- `metta.rl.training.DistributedHelper`
- `metta.rl.training.Experience`
- `metta.rl.training.TrainerCallback`
- `metta.rl.training.TrainerComponent`
- `metta.rl.training.TrainerState`
- `metta.rl.training.TrainingEnvironment`
- `metta.rl.training.optimizer.create_optimizer`
- `mettagrid.profiling.stopwatch.Stopwatch`
- `torch`
- `typing.Any`
- `typing.Callable`
- `typing.Optional`

## Classes (1)

### Trainer

**Class**: `rl.trainer.Trainer`

**Constructor**: `Trainer(self, cfg: TrainerConfig, env: TrainingEnvironment, policy: Policy, device: Any, distributed_helper: Optional[DistributedHelper] = ..., run_name: Optional[str] = ...)`

**Documentation**: Main trainer facade that coordinates all training components.

**Methods**: 5

#### context

**Signature**: `Trainer.context(self) -> ComponentContext`

**Documentation**: Return the shared trainer context.

**Location**: line 131

#### train

**Signature**: `Trainer.train(self) -> Any`

**Documentation**: Run the main training loop.

**Location**: line 136

#### load_or_create

**Signature**: `Trainer.load_or_create(checkpoint_path: str, cfg: TrainerConfig, training_env: TrainingEnvironment, policy: Policy, device: Any, distributed_helper: Optional[DistributedHelper] = ..., run_name: Optional[str] = ...) -> Any`

**Documentation**: Create a trainer from a configuration.

Args:
    distributed_helper: Optional helper to reuse existing process group

**Location**: line 197

#### register

**Signature**: `Trainer.register(self, component: TrainerComponent) -> Any`

**Documentation**: Register a training component.

Args:
    component: Training component to register

**Location**: line 220

#### restore

**Signature**: `Trainer.restore(self) -> Any`

**Documentation**: Restore trainer state from checkpoints.

This should be called after setup() to restore any saved state.

**Location**: line 264


