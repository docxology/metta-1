"""
DAF Curriculum Learning Manager

This module provides comprehensive curriculum learning functionality
integrated with the DAF Adaptive Controller and Metta curriculum components.
"""

import logging
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass, field
from pathlib import Path

# Import Metta curriculum components
from metta.cogworks.curriculum.curriculum import Curriculum, CurriculumConfig
from metta.cogworks.curriculum.curriculum_env import CurriculumEnv
from metta.cogworks.curriculum.task_generator import (
    TaskGenerator,
    TaskGeneratorConfig,
    SingleTaskGenerator,
    BucketedTaskGenerator,
    TaskGeneratorSet,
)
from metta.cogworks.curriculum.learning_progress_algorithm import LearningProgressAlgorithm, LearningProgressConfig
from metta.cogworks.curriculum.task_tracker import TaskTracker
from metta.cogworks.curriculum.stats import SliceAnalyzer, StatsLogger
from metta.cogworks.curriculum.__init__ import single_task, bucketed, multi_task, merge, env_curriculum

# Import Metta grid configuration
from mettagrid.config.mettagrid_config import MettaGridConfig


@dataclass
class DAFCurriculumConfig:
    """Configuration for DAF Curriculum Learning"""

    name: str = "daf_curriculum"
    max_active_tasks: int = 10
    min_task_presentations: int = 5
    enable_learning_progress: bool = True
    enable_slice_analysis: bool = True
    enable_task_tracking: bool = True
    stats_update_frequency: int = 50

    # Task generation settings
    task_generator_type: str = "single"  # single, bucketed, multi
    num_buckets: int = 5
    difficulty_range: tuple = (0.0, 1.0)

    # Learning progress settings
    lp_config: Optional[LearningProgressConfig] = None

    # Slice analysis settings
    max_slice_axes: int = 10
    slice_analysis_enabled: bool = True


class DAFCurriculumManager:
    """
    Enhanced curriculum manager with DAF-specific features

    Integrates with Metta curriculum components while providing:
    - Enhanced task management and scheduling
    - Advanced learning progress tracking
    - Comprehensive statistics and analysis
    - Automatic curriculum adaptation
    """

    def __init__(self, config: DAFCurriculumConfig):
        """
        Initialize DAF Curriculum Manager

        Args:
            config: DAF curriculum configuration
        """
        self.config = config
        self.logger = logging.getLogger(f"DAFCurriculumManager.{config.name}")

        # Initialize core components
        self._curriculum = self._create_curriculum()
        self._task_tracker = TaskTracker() if config.enable_task_tracking else None
        self._slice_analyzer = (
            SliceAnalyzer(max_slice_axes=config.max_slice_axes) if config.enable_slice_analysis else None
        )

        # DAF-specific state
        self._custom_tasks: Dict[str, Dict[str, Any]] = {}
        self._task_scores: Dict[str, List[float]] = {}
        self._adaptation_history: List[Dict[str, Any]] = []

        self.logger.info(f"DAF Curriculum Manager initialized: {config.name}")

    def _create_curriculum(self) -> Curriculum:
        """Create curriculum with appropriate configuration"""
        curriculum_config = CurriculumConfig()

        if self.config.lp_config:
            curriculum_config.algorithm_config = self.config.lp_config

        return Curriculum(config=curriculum_config, seed=42)

    def add_task(
        self,
        task_id: str,
        task_config: Optional[Dict[str, Any]] = None,
        difficulty: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        Add a custom task to the curriculum

        Args:
            task_id: Unique task identifier
            task_config: Task-specific configuration
            difficulty: Task difficulty level (0.0 to 1.0)
            metadata: Additional task metadata
        """
        if task_config is None:
            task_config = {}

        # Store task information
        task_info = {
            "config": task_config,
            "difficulty": difficulty or 0.5,
            "metadata": metadata or {},
            "created_at": self._get_timestamp(),
        }

        self._custom_tasks[task_id] = task_info

        # Add to curriculum
        self._curriculum.add_task(task_id, difficulty=difficulty)

        self.logger.info(f"Added custom task: {task_id} (difficulty: {difficulty})")

    def add_task_from_metta_config(self, mg_config: MettaGridConfig, task_id: Optional[str] = None):
        """
        Add a task from a MettaGridConfig

        Args:
            mg_config: MettaGrid configuration
            task_id: Optional custom task ID
        """
        if task_id is None:
            task_id = f"metta_task_{len(self._custom_tasks)}"

        self.add_task(task_id, task_config=mg_config.model_dump(), difficulty=0.5)
        return task_id

    def generate_task_sequence(self, sequence_length: int, difficulty_progression: str = "linear") -> List[str]:
        """
        Generate a sequence of tasks with specified difficulty progression

        Args:
            sequence_length: Number of tasks in sequence
            difficulty_progression: "linear", "exponential", "random", "adaptive"

        Returns:
            List of task IDs in the generated sequence
        """
        import random

        if difficulty_progression == "linear":
            difficulties = [i / max(sequence_length - 1, 1) for i in range(sequence_length)]
        elif difficulty_progression == "exponential":
            difficulties = [min(1.0, 0.1 * (2**i)) for i in range(sequence_length)]
        elif difficulty_progression == "random":
            difficulties = [random.random() for _ in range(sequence_length)]
        else:  # adaptive
            difficulties = self._generate_adaptive_difficulties(sequence_length)

        # Create tasks with generated difficulties
        sequence_tasks = []
        for i, difficulty in enumerate(difficulties):
            task_id = f"seq_task_{i}"
            self.add_task(task_id, difficulty=difficulty)
            sequence_tasks.append(task_id)

        self.logger.info(f"Generated task sequence: {sequence_tasks}")
        return sequence_tasks

    def _generate_adaptive_difficulties(self, length: int) -> List[float]:
        """Generate adaptive difficulty progression based on learning progress"""
        # Simple adaptive progression - can be enhanced with ML models
        base_difficulty = 0.1
        increment = 0.9 / max(length - 1, 1)

        return [min(1.0, base_difficulty + i * increment) for i in range(length)]

    def update_task_performance(self, task_id: str, score: float, episode_info: Optional[Dict] = None):
        """
        Update task performance and trigger curriculum adaptation

        Args:
            task_id: Task identifier
            score: Performance score
            episode_info: Additional episode information
        """
        # Update curriculum
        self._curriculum.update_task_performance(task_id, score)

        # Update task tracker
        if self._task_tracker:
            self._task_tracker.update_task_performance(task_id, score)

        # Update slice analyzer
        if self._slice_analyzer and episode_info:
            slice_values = self._extract_slice_values(episode_info)
            if slice_values:
                self._slice_analyzer.update_task_completion(task_id, slice_values, score)

        # Store score for analysis
        if task_id not in self._task_scores:
            self._task_scores[task_id] = []
        self._task_scores[task_id].append(score)

        # Check for adaptation
        self._check_curriculum_adaptation(task_id, score)

        self.logger.debug(f"Updated performance for {task_id}: {score}")

    def _extract_slice_values(self, episode_info: Dict) -> Dict[str, Any]:
        """Extract slice values from episode information"""
        slice_values = {}

        # Extract relevant parameters for slice analysis
        for key in ["map_size", "num_agents", "difficulty", "complexity"]:
            if key in episode_info:
                slice_values[key] = episode_info[key]

        return slice_values

    def _check_curriculum_adaptation(self, task_id: str, score: float):
        """Check if curriculum should be adapted based on performance"""
        if task_id not in self._task_scores:
            return

        scores = self._task_scores[task_id]
        if len(scores) < self.config.min_task_presentations:
            return

        # Calculate average performance
        avg_score = sum(scores) / len(scores)

        # Adaptation logic - can be made more sophisticated
        if avg_score > 0.8 and len(scores) >= 10:
            # Task is too easy, increase difficulty
            self._adapt_curriculum("increase_difficulty", task_id)
        elif avg_score < 0.3 and len(scores) >= 5:
            # Task is too hard, decrease difficulty
            self._adapt_curriculum("decrease_difficulty", task_id)

    def _adapt_curriculum(self, adaptation_type: str, task_id: str):
        """Adapt curriculum based on performance"""
        adaptation = {
            "type": adaptation_type,
            "task_id": task_id,
            "timestamp": self._get_timestamp(),
            "current_state": self.get_curriculum_stats(),
        }

        self._adaptation_history.append(adaptation)

        # Log adaptation
        self.logger.info(f"Curriculum adaptation: {adaptation_type} for task {task_id}")

        # Limit history size
        if len(self._adaptation_history) > 100:
            self._adaptation_history = self._adaptation_history[-100:]

    def get_next_task(self) -> Optional[str]:
        """
        Get the next task from curriculum

        Returns:
            Task ID or None if no suitable task available
        """
        try:
            task = self._curriculum.get_task()
            return task.task_id
        except Exception as e:
            self.logger.warning(f"Failed to get next task: {e}")
            return None

    def get_curriculum_stats(self) -> Dict[str, Any]:
        """Get comprehensive curriculum statistics"""
        stats = {
            "num_custom_tasks": len(self._custom_tasks),
            "num_task_scores": len(self._task_scores),
            "total_scores_recorded": sum(len(scores) for scores in self._task_scores.values()),
            "adaptation_history_length": len(self._adaptation_history),
        }

        # Add curriculum stats
        if hasattr(self._curriculum, "stats"):
            stats["curriculum"] = self._curriculum.stats()

        # Add task tracker stats
        if self._task_tracker:
            stats["task_tracker"] = self._task_tracker.get_global_stats()

        # Add slice analyzer stats
        if self._slice_analyzer:
            stats["slice_analysis"] = self._slice_analyzer.get_base_stats()

        return stats

    def get_task_difficulty_distribution(self) -> Dict[str, float]:
        """Get distribution of task difficulties"""
        difficulties = {}
        for task_id, task_info in self._custom_tasks.items():
            difficulties[task_id] = task_info["difficulty"]
        return difficulties

    def get_performance_history(self, task_id: Optional[str] = None) -> Dict[str, List[float]]:
        """Get performance history for tasks"""
        if task_id:
            return {task_id: self._task_scores.get(task_id, [])}
        return self._task_scores.copy()

    def export_curriculum_state(self, export_path: str):
        """
        Export curriculum state for persistence

        Args:
            export_path: Path to export file
        """
        export_data = {
            "config": self.config,
            "custom_tasks": self._custom_tasks,
            "task_scores": self._task_scores,
            "adaptation_history": self._adaptation_history,
            "curriculum_state": self._curriculum.get_state(),
            "timestamp": self._get_timestamp(),
        }

        if self._task_tracker:
            export_data["task_tracker_state"] = self._task_tracker.get_state()

        if self._slice_analyzer:
            export_data["slice_analyzer_state"] = self._slice_analyzer.get_base_stats()

        import json

        with open(export_path, "w") as f:
            json.dump(export_data, f, indent=2)

        self.logger.info(f"Curriculum state exported to {export_path}")

    def import_curriculum_state(self, import_path: str) -> bool:
        """
        Import curriculum state from file

        Args:
            import_path: Path to import file

        Returns:
            True if successfully imported, False otherwise
        """
        try:
            import json

            with open(import_path, "r") as f:
                import_data = json.load(f)

            # Restore state
            self._custom_tasks = import_data.get("custom_tasks", {})
            self._task_scores = import_data.get("task_scores", {})
            self._adaptation_history = import_data.get("adaptation_history", [])

            # Restore curriculum state
            if "curriculum_state" in import_data:
                self._curriculum.load_state(import_data["curriculum_state"])

            # Restore other components
            if self._task_tracker and "task_tracker_state" in import_data:
                self._task_tracker.load_state(import_data["task_tracker_state"])

            self.logger.info(f"Curriculum state imported from {import_path}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to import curriculum state: {e}")
            return False

    def _get_timestamp(self) -> str:
        """Get current timestamp as string"""
        from datetime import datetime

        return datetime.now().isoformat()


# Convenience functions for common curriculum operations
def create_simple_curriculum(name: str, difficulties: List[float]) -> DAFCurriculumManager:
    """
    Create a simple curriculum with specified difficulties

    Args:
        name: Curriculum name
        difficulties: List of task difficulties

    Returns:
        Configured DAFCurriculumManager
    """
    config = DAFCurriculumConfig(name=name)
    manager = DAFCurriculumManager(config)

    for i, difficulty in enumerate(difficulties):
        task_id = f"simple_task_{i}"
        manager.add_task(task_id, difficulty=difficulty)

    return manager


def create_progressive_curriculum(
    name: str, num_tasks: int, start_difficulty: float = 0.1, end_difficulty: float = 1.0
) -> DAFCurriculumManager:
    """
    Create a progressive curriculum with increasing difficulty

    Args:
        name: Curriculum name
        num_tasks: Number of tasks
        start_difficulty: Starting difficulty
        end_difficulty: Ending difficulty

    Returns:
        Configured DAFCurriculumManager
    """
    config = DAFCurriculumConfig(name=name)
    manager = DAFCurriculumManager(config)

    # Generate difficulties
    difficulties = [
        start_difficulty + (end_difficulty - start_difficulty) * (i / max(num_tasks - 1, 1)) for i in range(num_tasks)
    ]

    for i, difficulty in enumerate(difficulties):
        task_id = f"progressive_task_{i}"
        manager.add_task(task_id, difficulty=difficulty)

    return manager
