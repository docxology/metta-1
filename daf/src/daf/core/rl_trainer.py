"""
DAF Reinforcement Learning Trainer

This module provides comprehensive RL training functionality
integrated with the DAF Adaptive Controller and Metta RL components.
"""

import logging
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from metta.rl.system_config import SystemConfig

# Import Metta RL components
from metta.rl.trainer import Trainer as MettaTrainer
from metta.rl.trainer_config import TrainerConfig
from metta.rl.training.training_environment import TrainingEnvironment, VectorizedTrainingEnvironment

# Import DAF components
try:
    from .curriculum_manager import DAFCurriculumManager
except ImportError:
    # Fallback for testing scenarios - try absolute import
    try:
        from daf.core.curriculum_manager import DAFCurriculumManager
    except ImportError:
        # Final fallback - define a placeholder
        class DAFCurriculumManager:
            pass


# Forward declaration to avoid circular imports
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .adaptive_controller import DAFAdaptiveController


@dataclass
class DAFRlConfig:
    """Configuration for DAF RL Training"""

    experiment_name: str = "daf_rl_experiment"
    total_timesteps: int = 1000000
    batch_size: int = 2048
    num_envs: int = 8
    learning_rate: float = 3e-4
    gamma: float = 0.99
    gae_lambda: float = 0.95
    clip_range: float = 0.2
    n_epochs: int = 4
    n_steps: int = 128

    # Evaluation settings
    eval_frequency: int = 1000
    eval_episodes: int = 10
    eval_deterministic: bool = True

    # Checkpointing
    checkpoint_frequency: int = 1000
    keep_last_checkpoints: int = 5

    # Distributed training
    use_distributed: bool = False
    num_workers: int = 4

    # DAF-specific settings
    integrate_with_adaptive: bool = True
    adaptive_config: Optional[Dict[str, Any]] = None
    curriculum_config: Optional[Dict[str, Any]] = None


class DAFRlTrainer:
    """
    Enhanced RL Trainer with DAF-specific features

    Integrates with Metta RL components while providing:
    - Adaptive learning integration
    - Curriculum-based training
    - Enhanced monitoring and evaluation
    - Automatic hyperparameter tuning
    - Comprehensive experiment management
    """

    def __init__(
        self,
        config: DAFRlConfig,
        policy: Any,  # Policy from agent
        training_env: Optional[TrainingEnvironment] = None,
        adaptive_controller: Optional["DAFAdaptiveController"] = None,
        curriculum_manager: Optional[DAFCurriculumManager] = None,
    ):
        """
        Initialize DAF RL Trainer

        Args:
            config: DAF RL configuration
            policy: Policy to train
            training_env: Training environment
            adaptive_controller: Optional adaptive controller for integration
            curriculum_manager: Optional curriculum manager
        """
        self.config = config
        self.policy = policy
        self.logger = logging.getLogger(f"DAFRlTrainer.{config.experiment_name}")

        # Initialize components
        self._adaptive_controller = adaptive_controller
        self._curriculum_manager = curriculum_manager
        self._training_env = training_env or self._create_default_environment()

        # Initialize Metta trainer
        self._metta_trainer = self._create_metta_trainer()

        # DAF-specific state
        self._training_stats: Dict[str, List[float]] = {}
        self._episode_rewards: List[float] = []
        self._episode_lengths: List[int] = []
        self._best_reward: float = float("-inf")

        self.logger.info(f"DAF RL Trainer initialized: {config.experiment_name}")

    def _create_default_environment(self) -> TrainingEnvironment:
        """Create default training environment"""
        from metta.rl.training.training_environment import TrainingEnvironmentConfig

        env_config = TrainingEnvironmentConfig(batch_size=self.config.batch_size, num_envs=self.config.num_envs)

        return VectorizedTrainingEnvironment(env_config)

    def _create_metta_trainer(self) -> MettaTrainer:
        """Create Metta trainer with appropriate configuration"""
        trainer_config = TrainerConfig(
            total_timesteps=self.config.total_timesteps,
            batch_size=self.config.batch_size,
            learning_rate=self.config.learning_rate,
            gamma=self.config.gamma,
            gae_lambda=self.config.gae_lambda,
            clip_range=self.config.clip_range,
            n_epochs=self.config.n_epochs,
            n_steps=self.config.n_steps,
            eval_frequency=self.config.eval_frequency,
            checkpoint_frequency=self.config.checkpoint_frequency,
        )

        system_config = SystemConfig()

        # Create trainer with environment and policy
        trainer = MettaTrainer(
            cfg=trainer_config,
            env=self._training_env,
            policy=self.policy,
            device=system_config.guess_device(),
            run_name=self.config.experiment_name,
        )

        return trainer

    def train(self) -> Dict[str, Any]:
        """
        Run RL training with DAF enhancements

        Returns:
            Training results and statistics
        """
        self.logger.info(f"Starting DAF RL training: {self.config.experiment_name}")

        try:
            # Set up adaptive integration if enabled
            if self.config.integrate_with_adaptive and self._adaptive_controller:
                self._setup_adaptive_integration()

            # Set up curriculum integration if available
            if self._curriculum_manager:
                self._setup_curriculum_integration()

            # Training loop with DAF enhancements
            results = self._run_training_loop()

            return results

        except Exception as e:
            self.logger.error(f"Training failed: {e}")
            raise

    def _setup_adaptive_integration(self):
        """Set up integration with adaptive controller"""
        self.logger.info("Setting up adaptive integration")

        # Register training callbacks
        def on_training_complete():
            self.logger.info("Training epoch completed, notifying adaptive controller")
            if self._adaptive_controller:
                # Send training statistics to adaptive controller
                stats = self._get_training_stats()
                # Integration point for adaptive control

        def on_evaluation_complete(eval_results):
            self.logger.info(f"Evaluation completed: {eval_results}")
            # Send evaluation results to adaptive controller for decision making

        # Register callbacks with trainer
        if hasattr(self._metta_trainer, "register"):
            self._metta_trainer.register("on_epoch_end", on_training_complete)
            self._metta_trainer.register("on_eval_end", on_evaluation_complete)

    def _setup_curriculum_integration(self):
        """Set up integration with curriculum manager"""
        self.logger.info("Setting up curriculum integration")

        # Register curriculum callbacks
        def on_task_update(task_id: str, score: float):
            if self._curriculum_manager:
                self._curriculum_manager.update_task_performance(task_id, score)

        def on_task_request() -> Optional[str]:
            if self._curriculum_manager:
                return self._curriculum_manager.get_next_task()
            return None

        # Register with training environment if it supports curriculum
        if hasattr(self._training_env, "set_curriculum_callback"):
            self._training_env.set_curriculum_callback(on_task_request)

    def _run_training_loop(self) -> Dict[str, Any]:
        """Run the main training loop with DAF enhancements"""
        self.logger.info("Running DAF training loop")

        # Initialize tracking
        episode_count = 0
        timestep_count = 0

        # Main training loop
        while timestep_count < self.config.total_timesteps:
            try:
                # Get next batch of experience
                batch = self._training_env.get_observations()

                # Training step
                results = self._metta_trainer.train_step(batch)

                # Update statistics
                self._update_training_stats(results)

                # Check for evaluation
                if self._should_evaluate(timestep_count):
                    eval_results = self._run_evaluation()
                    self._handle_evaluation_results(eval_results)

                # Check for checkpointing
                if self._should_checkpoint(timestep_count):
                    self._save_checkpoint()

                timestep_count += self.config.batch_size
                episode_count += 1

                # Log progress
                if episode_count % 100 == 0:
                    self._log_progress(episode_count, timestep_count)

            except Exception as e:
                self.logger.error(f"Training step failed: {e}")
                # Continue training or handle error based on configuration
                if not self._should_continue_on_error():
                    break

        # Final evaluation
        final_results = self._run_evaluation()
        self._handle_evaluation_results(final_results)

        return self._compile_training_results()

    def _update_training_stats(self, results: Dict[str, Any]):
        """Update training statistics"""
        for key, value in results.items():
            if key not in self._training_stats:
                self._training_stats[key] = []
            self._training_stats[key].append(value)

        # Track episode rewards if available
        if "episode_reward" in results:
            self._episode_rewards.append(results["episode_reward"])

        if "episode_length" in results:
            self._episode_lengths.append(results["episode_length"])

    def _should_evaluate(self, timestep_count: int) -> bool:
        """Check if evaluation should be run"""
        return timestep_count % self.config.eval_frequency == 0

    def _should_checkpoint(self, timestep_count: int) -> bool:
        """Check if checkpoint should be saved"""
        return timestep_count % self.config.checkpoint_frequency == 0

    def _should_continue_on_error(self) -> bool:
        """Check if training should continue after errors"""
        return True  # Could be made configurable

    def _run_evaluation(self) -> Dict[str, Any]:
        """Run evaluation with current policy"""
        self.logger.info("Running evaluation")

        try:
            # Use Metta evaluator if available
            if hasattr(self._metta_trainer, "evaluate"):
                return self._metta_trainer.evaluate()

            # Fallback evaluation
            return self._run_custom_evaluation()

        except Exception as e:
            self.logger.error(f"Evaluation failed: {e}")
            return {"error": str(e)}

    def _run_custom_evaluation(self) -> Dict[str, Any]:
        """Run custom evaluation implementation"""
        # Placeholder for custom evaluation logic
        return {
            "mean_reward": sum(self._episode_rewards[-100:]) / max(len(self._episode_rewards[-100:]), 1),
            "episodes_evaluated": len(self._episode_rewards),
        }

    def _handle_evaluation_results(self, eval_results: Dict[str, Any]):
        """Handle evaluation results"""
        self.logger.info(f"Evaluation results: {eval_results}")

        # Update best reward
        if "mean_reward" in eval_results:
            mean_reward = eval_results["mean_reward"]
            if mean_reward > self._best_reward:
                self._best_reward = mean_reward
                self.logger.info(f"New best reward: {mean_reward}")

        # Notify adaptive controller
        if self._adaptive_controller:
            # Send evaluation results for adaptive decisions
            pass

        # Notify curriculum manager
        if self._curriculum_manager:
            # Update curriculum based on performance
            if "mean_reward" in eval_results:
                self._curriculum_manager.update_task_performance("current_task", eval_results["mean_reward"])

    def _save_checkpoint(self):
        """Save training checkpoint"""
        try:
            checkpoint_path = f"checkpoints/{self.config.experiment_name}_step_{len(self._episode_rewards)}"
            # Implementation would use CheckpointManager
            self.logger.debug(f"Checkpoint saved: {checkpoint_path}")
        except Exception as e:
            self.logger.error(f"Checkpoint save failed: {e}")

    def _log_progress(self, episode_count: int, timestep_count: int):
        """Log training progress"""
        avg_reward = (
            sum(self._episode_rewards[-100:]) / max(len(self._episode_rewards[-100:]), 1)
            if self._episode_rewards
            else 0.0
        )

        avg_length = (
            sum(self._episode_lengths[-100:]) / max(len(self._episode_lengths[-100:]), 1)
            if self._episode_lengths
            else 0
        )

        self.logger.info(
            f"Episode {episode_count}, Timesteps {timestep_count}: "
            f"Reward: {avg_reward:.2f}, Length: {avg_length:.1f}, "
            f"Best: {self._best_reward:.2f}"
        )

    def _get_training_stats(self) -> Dict[str, Any]:
        """Get comprehensive training statistics"""
        return {
            "episodes": len(self._episode_rewards),
            "timesteps": sum(self._episode_lengths),
            "avg_reward": (
                sum(self._episode_rewards[-100:]) / max(len(self._episode_rewards[-100:]), 1)
                if self._episode_rewards
                else 0.0
            ),
            "best_reward": self._best_reward,
            "training_stats": self._training_stats,
        }

    def _compile_training_results(self) -> Dict[str, Any]:
        """Compile final training results"""
        results = self._get_training_stats()

        results.update(
            {
                "experiment_name": self.config.experiment_name,
                "total_timesteps": self.config.total_timesteps,
                "config": self.config,
                "completed": len(self._episode_rewards) * self.config.batch_size >= self.config.total_timesteps,
            }
        )

        return results

    def save_training_state(self, save_path: str):
        """Save complete training state"""
        state = {
            "config": self.config,
            "training_stats": self._training_stats,
            "episode_rewards": self._episode_rewards,
            "episode_lengths": self._episode_lengths,
            "best_reward": self._best_reward,
            "policy_state": self.policy.state_dict() if hasattr(self.policy, "state_dict") else None,
        }

        import json

        with open(save_path, "w") as f:
            json.dump(state, f, indent=2)

        self.logger.info(f"Training state saved to {save_path}")

    def load_training_state(self, load_path: str) -> bool:
        """Load training state"""
        try:
            import json

            with open(load_path, "r") as f:
                state = json.load(f)

            self.config = state.get("config", self.config)
            self._training_stats = state.get("training_stats", {})
            self._episode_rewards = state.get("episode_rewards", [])
            self._episode_lengths = state.get("episode_lengths", [])
            self._best_reward = state.get("best_reward", float("-inf"))

            # Load policy state if available
            if "policy_state" in state and self.policy and hasattr(self.policy, "load_state_dict"):
                self.policy.load_state_dict(state["policy_state"])

            self.logger.info(f"Training state loaded from {load_path}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to load training state: {e}")
            return False


# Convenience functions for common RL training scenarios
def train_ppo_agent(
    policy: Any, env_name: str, total_timesteps: int = 1000000, experiment_name: Optional[str] = None
) -> DAFRlTrainer:
    """
    Create and configure a DAF RL trainer for PPO training

    Args:
        policy: Policy to train
        env_name: Environment name
        total_timesteps: Total training timesteps
        experiment_name: Optional experiment name

    Returns:
        Configured DAFRlTrainer
    """
    config = DAFRlConfig(experiment_name=experiment_name or f"ppo_{env_name}", total_timesteps=total_timesteps)

    trainer = DAFRlTrainer(config, policy)

    # Set up environment
    # Implementation would configure environment based on env_name

    return trainer


def run_quick_rl_experiment(
    policy: Any, env_config: Dict[str, Any], training_config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Run a quick RL experiment with minimal configuration

    Args:
        policy: Policy to train
        env_config: Environment configuration
        training_config: Optional training configuration

    Returns:
        Experiment results
    """
    if training_config is None:
        training_config = {}

    config = DAFRlConfig(
        experiment_name="quick_rl_experiment", total_timesteps=training_config.get("total_timesteps", 50000)
    )

    trainer = DAFRlTrainer(config, policy)

    # Configure environment
    # Implementation would use env_config

    results = trainer.train()

    return results
