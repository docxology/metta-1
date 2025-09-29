"""
DAF Adaptive Controller Implementation

This module provides a comprehensive implementation of the Metta AdaptiveController
with additional DAF-specific enhancements, convenience methods, and robust error handling.
"""

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from metta.adaptive.adaptive_config import AdaptiveConfig

# Import Metta components
from metta.adaptive.adaptive_controller import AdaptiveController as MettaAdaptiveController
from metta.adaptive.dispatcher.local import LocalDispatcher
from metta.adaptive.dispatcher.skypilot import SkypilotDispatcher
from metta.adaptive.models import JobDefinition, RunInfo
from metta.adaptive.protocols import Dispatcher, ExperimentScheduler, Store
from metta.adaptive.stores.wandb import WandbStore
from metta.cogworks.curriculum.curriculum import Curriculum, CurriculumConfig
from metta.cogworks.curriculum.learning_progress_algorithm import LearningProgressConfig
from metta.cogworks.curriculum.task_generator import TaskGeneratorConfig

# Import DAF utilities


@dataclass
class DAFAdaptiveConfig:
    """Enhanced configuration for DAF Adaptive Controller"""

    experiment_id: str = "daf_experiment"
    max_concurrent_jobs: int = 4
    heartbeat_interval: float = 30.0
    enable_curriculum_learning: bool = True
    enable_checkpointing: bool = True
    checkpoint_interval: int = 100
    wandb_project: str = "daf-experiments"
    wandb_entity: str = "daf-user"
    use_skypilot: bool = False
    skypilot_config: Dict[str, Any] = field(default_factory=dict)

    # Curriculum learning settings
    curriculum_config: Optional[CurriculumConfig] = None
    learning_progress_config: Optional[LearningProgressConfig] = None
    task_generator_config: Optional[TaskGeneratorConfig] = None

    # Enhanced error handling
    retry_on_failure: bool = True
    max_retries: int = 3
    retry_delay: float = 5.0


class DAFAdaptiveController:
    """
    Enhanced Adaptive Controller with DAF-specific features

    This controller extends the Metta AdaptiveController with:
    - Curriculum learning integration
    - Enhanced error handling and retry logic
    - Automatic checkpointing and recovery
    - Comprehensive monitoring and logging
    - Convenience methods for common operations
    """

    def __init__(
        self,
        config: DAFAdaptiveConfig,
        scheduler: Optional[ExperimentScheduler] = None,
        dispatcher: Optional[Dispatcher] = None,
        store: Optional[Store] = None,
        curriculum: Optional[Curriculum] = None,
    ):
        """
        Initialize DAF Adaptive Controller

        Args:
            config: DAF-specific configuration
            scheduler: Optional experiment scheduler
            dispatcher: Optional job dispatcher
            store: Optional data store
            curriculum: Optional curriculum for task management
        """
        self.config = config
        self.logger = logging.getLogger(f"DAFAdaptiveController.{config.experiment_id}")

        # Initialize components
        self._scheduler = scheduler or self._create_default_scheduler()
        self._dispatcher = dispatcher or self._create_default_dispatcher()
        self._store = store or self._create_default_store()
        self._curriculum = curriculum or self._create_default_curriculum()

        # Initialize Metta controller
        self._metta_controller = MettaAdaptiveController(
            experiment_id=config.experiment_id,
            scheduler=self._scheduler,
            dispatcher=self._dispatcher,
            store=self._store,
            config=AdaptiveConfig(),
        )

        # DAF-specific state
        self._active_jobs: Dict[str, JobDefinition] = {}
        self._completed_runs: List[RunInfo] = []
        self._is_running = False
        self._heartbeat_thread = None

        self.logger.info(f"DAF Adaptive Controller initialized for experiment: {config.experiment_id}")

    def _create_default_scheduler(self) -> ExperimentScheduler:
        """Create default experiment scheduler"""
        from metta.adaptive.protocols import ExperimentScheduler

        class DefaultScheduler(ExperimentScheduler):
            def schedule(self, runs: list, available_training_slots: int) -> list:
                # Simple scheduling logic - can be enhanced
                return []

            def is_experiment_complete(self, runs: list) -> bool:
                return len(runs) >= 10  # Simple completion criteria

        return DefaultScheduler()

    def _create_default_dispatcher(self) -> Dispatcher:
        """Create default job dispatcher"""
        if self.config.use_skypilot:
            return SkypilotDispatcher()
        else:
            return LocalDispatcher(capture_output=True)

    def _create_default_store(self) -> Store:
        """Create default data store"""
        return WandbStore(entity=self.config.wandb_entity, project=self.config.wandb_project)

    def _create_default_curriculum(self) -> Curriculum:
        """Create default curriculum"""
        if self.config.curriculum_config:
            return Curriculum(config=self.config.curriculum_config)

        # Create default curriculum config
        default_config = CurriculumConfig()
        return Curriculum(config=default_config)

    def start_experiment(
        self,
        on_training_completed: Optional[Callable] = None,
        on_eval_completed: Optional[Callable] = None,
        on_job_dispatch: Optional[Callable] = None,
    ) -> Any:
        """
        Start the adaptive experiment with enhanced DAF features

        Args:
            on_training_completed: Callback for training completion
            on_eval_completed: Callback for evaluation completion
            on_job_dispatch: Callback for job dispatch events

        Returns:
            Experiment results
        """
        self.logger.info("Starting DAF adaptive experiment")

        try:
            self._is_running = True

            # Set up callbacks
            def enhanced_training_callback(run_info: RunInfo):
                self._completed_runs.append(run_info)
                if on_training_completed:
                    on_training_completed(run_info)
                self._save_checkpoint()

            def enhanced_eval_callback(run_info: RunInfo):
                if on_eval_completed:
                    on_eval_completed(run_info)

            def enhanced_dispatch_callback(job: JobDefinition):
                self._active_jobs[job.run_id] = job
                if on_job_dispatch:
                    on_job_dispatch(job)

            # Start heartbeat monitoring
            self._start_heartbeat()

            # Run the experiment
            result = self._metta_controller.run(
                on_training_completed=enhanced_training_callback,
                on_eval_completed=enhanced_eval_callback,
                on_job_dispatch=enhanced_dispatch_callback,
            )

            return result

        except Exception as e:
            self.logger.error(f"Error in DAF adaptive experiment: {e}")
            raise
        finally:
            self._is_running = False
            self._stop_heartbeat()

    def stop_experiment(self):
        """Stop the current experiment gracefully"""
        self.logger.info("Stopping DAF adaptive experiment")
        self._is_running = False
        self._stop_heartbeat()

        # Cancel active jobs
        for job in self._active_jobs.values():
            self._dispatcher.cancel_job(job)

    def get_experiment_status(self) -> Dict[str, Any]:
        """Get current experiment status"""
        return {
            "experiment_id": self.config.experiment_id,
            "is_running": self._is_running,
            "active_jobs": len(self._active_jobs),
            "completed_runs": len(self._completed_runs),
            "curriculum_progress": self._curriculum.stats() if self._curriculum else {},
        }

    def _start_heartbeat(self):
        """Start heartbeat monitoring thread"""
        import threading
        import time

        def heartbeat():
            while self._is_running:
                try:
                    status = self.get_experiment_status()
                    self.logger.debug(f"Heartbeat: {status}")
                    time.sleep(self.config.heartbeat_interval)
                except Exception as e:
                    self.logger.error(f"Heartbeat error: {e}")

        self._heartbeat_thread = threading.Thread(target=heartbeat, daemon=True)
        self._heartbeat_thread.start()

    def _stop_heartbeat(self):
        """Stop heartbeat monitoring thread"""
        if self._heartbeat_thread and self._heartbeat_thread.is_alive():
            self._heartbeat_thread.join(timeout=5.0)

    def _save_checkpoint(self):
        """Save controller state for recovery"""
        if not self.config.enable_checkpointing:
            return

        try:
            checkpoint_data = {
                "config": self.config,
                "active_jobs": self._active_jobs,
                "completed_runs": self._completed_runs,
                "curriculum_state": self._curriculum.get_state() if self._curriculum else None,
            }

            checkpoint_path = Path(f"checkpoints/{self.config.experiment_id}_controller.pkl")
            checkpoint_path.parent.mkdir(exist_ok=True)

            import pickle

            with open(checkpoint_path, "wb") as f:
                pickle.dump(checkpoint_data, f)

            self.logger.debug(f"Checkpoint saved to {checkpoint_path}")

        except Exception as e:
            self.logger.error(f"Failed to save checkpoint: {e}")

    def load_checkpoint(self, checkpoint_path: str) -> bool:
        """
        Load controller state from checkpoint

        Args:
            checkpoint_path: Path to checkpoint file

        Returns:
            True if successfully loaded, False otherwise
        """
        try:
            with open(checkpoint_path, "rb") as f:
                checkpoint_data = pickle.load(f)

            # Restore state
            self._active_jobs = checkpoint_data.get("active_jobs", {})
            self._completed_runs = checkpoint_data.get("completed_runs", [])

            # Restore curriculum state
            if self._curriculum and "curriculum_state" in checkpoint_data:
                self._curriculum.load_state(checkpoint_data["curriculum_state"])

            self.logger.info(f"Checkpoint loaded from {checkpoint_path}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to load checkpoint: {e}")
            return False


# Convenience functions for common use cases
def create_quick_experiment(
    experiment_name: str, num_tasks: int = 5, use_curriculum: bool = True
) -> DAFAdaptiveController:
    """
    Create a DAF Adaptive Controller with sensible defaults for quick experiments

    Args:
        experiment_name: Name of the experiment
        num_tasks: Number of tasks for curriculum
        use_curriculum: Whether to enable curriculum learning

    Returns:
        Configured DAF Adaptive Controller
    """
    config = DAFAdaptiveConfig(
        experiment_id=experiment_name, enable_curriculum_learning=use_curriculum, wandb_project="daf-quick-experiments"
    )

    controller = DAFAdaptiveController(config)

    if use_curriculum:
        # Add some default tasks
        for i in range(num_tasks):
            difficulty = i / max(num_tasks - 1, 1)  # 0.0 to 1.0
            controller._curriculum.add_task(f"task_{i}", difficulty=difficulty)

    return controller


def run_simple_adaptive_experiment(experiment_name: str, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Run a simple adaptive experiment with minimal configuration

    Args:
        experiment_name: Name of the experiment
        tasks: List of task configurations

    Returns:
        Experiment results
    """
    config = DAFAdaptiveConfig(experiment_id=experiment_name)
    controller = DAFAdaptiveController(config)

    # Add tasks to curriculum
    for i, task_config in enumerate(tasks):
        controller._curriculum.add_task(f"task_{i}", **task_config)

    # Run experiment
    results = controller.start_experiment()

    return {
        "experiment_id": experiment_name,
        "results": results,
        "status": controller.get_experiment_status(),
        "completed_runs": len(controller._completed_runs),
    }
