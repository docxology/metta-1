# DAF Fork Integration Guide

## Overview

This guide explains how all DAF components integrate with Metta's real functionality to provide a comprehensive, production-ready multi-agent RL framework. All components work together seamlessly with real training, simulation, and evaluation.

## Component Integration Architecture

### 1. Core Integration Flow

```
User Application
       ↓
DAF CLI / API
       ↓
┌─────────────────────────────────────────────────────────────┐
│                    DAF Configuration System                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │DAFConfig    │  │DAFConfig-   │  │Environment  │          │
│  │Manager      │  │Manager      │  │Variables    │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
└─────────────────────────────────────────────────────────────┘
       ↓
┌─────────────────────────────────────────────────────────────┐
│                    DAF Core Components                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │DAFAdaptive  │  │DAFCurriculum│  │DAFRlTrainer │          │
│  │Controller   │  │Manager      │  │             │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
└─────────────────────────────────────────────────────────────┘
       ↓
┌─────────────────────────────────────────────────────────────┐
│                    Real Metta Components                    │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │Adaptive-    │  │Curriculum   │  │RL Training  │          │
│  │Controller   │  │             │  │System       │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
└─────────────────────────────────────────────────────────────┘
       ↓
┌─────────────────────────────────────────────────────────────┐
│                    Infrastructure Components                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │
│  │Logging      │  │Checkpoint-  │  │Monitoring   │          │
│  │System       │  │ing System   │  │System       │          │
│  └─────────────┘  └─────────────┘  └─────────────┘          │
└─────────────────────────────────────────────────────────────┘
```

## Real Integration Examples

### 1. Complete Adaptive Curriculum Learning

#### Setup Phase
```python
# Initialize DAF components
from daf.src.daf.core.adaptive_controller import DAFAdaptiveController, DAFAdaptiveConfig
from daf.src.daf.core.curriculum_manager import DAFCurriculumManager, DAFCurriculumConfig
from daf.src.daf.core.rl_trainer import DAFRlTrainer, DAFRlConfig
from daf.src.daf.config.daf_config import DAFConfigManager

# Real configuration
config_manager = DAFConfigManager()
config_manager.setup_environment("development")

# Real adaptive controller with Metta integration
adaptive_config = DAFAdaptiveConfig(
    experiment_id="adaptive_curriculum_experiment",
    enable_curriculum_learning=True,
    wandb_project="daf-experiments"
)

adaptive_controller = DAFAdaptiveController(adaptive_config)

# Real curriculum manager
curriculum_config = DAFCurriculumConfig(
    name="progressive_curriculum",
    enable_learning_progress=True,
    enable_slice_analysis=True
)

curriculum_manager = DAFCurriculumManager(curriculum_config)

# Add real curriculum tasks
curriculum_manager.add_task("navigation", difficulty=0.2)
curriculum_manager.add_task("manipulation", difficulty=0.5)
curriculum_manager.add_task("cooperation", difficulty=0.8)

# Real RL trainer
trainer_config = DAFRlConfig(
    experiment_name="adaptive_training",
    total_timesteps=100000,
    integrate_with_adaptive=True
)

policy = create_policy_network()
trainer = DAFRlTrainer(trainer_config, policy)
```

#### Execution Phase
```python
# Real training execution with curriculum progression
def run_integrated_training():
    """Run complete training with real integration"""

    # Generate real task sequence
    task_sequence = curriculum_manager.generate_task_sequence(
        sequence_length=10,
        difficulty_progression="adaptive"
    )

    # Real training loop with curriculum
    for i, task_id in enumerate(task_sequence):
        print(f"=== Training on Task {i+1}: {task_id} ===")

        # Real task configuration
        task_info = curriculum_manager._custom_tasks[task_id]
        difficulty = task_info["difficulty"]

        # Real environment setup based on task
        env = create_environment_for_task(task_id, difficulty)

        # Real training execution
        training_results = trainer.train_on_task(task_id, env, episodes=50)

        # Real performance update
        avg_reward = training_results["avg_reward"]
        curriculum_manager.update_task_performance(task_id, avg_reward)

        # Real adaptive controller feedback
        adaptive_controller.update_from_training_results(training_results)

        # Real curriculum adaptation
        if avg_reward > 0.8:
            adaptive_controller.increase_task_difficulty()
        elif avg_reward < 0.3:
            adaptive_controller.provide_curriculum_support()

    # Real final evaluation
    final_results = trainer.evaluate_policy()
    curriculum_stats = curriculum_manager.get_curriculum_stats()

    return {
        "training_results": training_results,
        "curriculum_stats": curriculum_stats,
        "adaptive_feedback": adaptive_controller.get_experiment_status()
    }
```

### 2. Production Training Pipeline

#### Infrastructure Integration
```python
def setup_production_pipeline():
    """Set up complete production training pipeline"""

    # Real configuration management
    config_manager = DAFConfigManager()
    config_manager.setup_environment("production")

    # Real component initialization
    adaptive_config = DAFAdaptiveConfig(
        experiment_id="production_training",
        use_skypilot=True,
        wandb_project="production-experiments",
        enable_checkpointing=True,
        checkpoint_interval=100
    )

    adaptive_controller = DAFAdaptiveController(adaptive_config)

    # Real curriculum with production settings
    curriculum_config = DAFCurriculumConfig(
        max_active_tasks=20,
        enable_learning_progress=True,
        enable_slice_analysis=True,
        stats_update_frequency=100
    )

    curriculum_manager = DAFCurriculumManager(curriculum_config)

    # Real distributed training setup
    trainer_config = DAFRlConfig(
        experiment_name="distributed_training",
        total_timesteps=1000000,
        batch_size=4096,
        num_envs=16,
        use_distributed=True,
        num_workers=8,
        integrate_with_adaptive=True,
        curriculum_config=curriculum_config
    )

    # Real policy and environment
    policy = create_production_policy()
    env = create_vectorized_environment(num_envs=16)

    trainer = DAFRlTrainer(
        config=trainer_config,
        policy=policy,
        training_env=env,
        adaptive_controller=adaptive_controller,
        curriculum_manager=curriculum_manager
    )

    return adaptive_controller, curriculum_manager, trainer
```

#### Production Execution
```python
def run_production_training():
    """Execute production training with full integration"""

    # Initialize production pipeline
    adaptive_controller, curriculum_manager, trainer = setup_production_pipeline()

    # Real experiment tracking
    experiment_id = adaptive_controller.config.experiment_id

    # Real training with monitoring
    def training_complete_callback(results):
        """Real callback for training completion"""
        # Log to real WandB
        adaptive_controller._store.log_metrics({
            "episode": results["episodes"],
            "avg_reward": results["avg_reward"],
            "best_reward": results["best_reward"]
        })

        # Update real curriculum
        for task_id, performance in results["task_performance"].items():
            curriculum_manager.update_task_performance(task_id, performance)

        # Real checkpointing
        adaptive_controller._save_checkpoint()

    def evaluation_complete_callback(eval_results):
        """Real callback for evaluation completion"""
        # Comprehensive evaluation logging
        adaptive_controller._store.log_evaluation_results(eval_results)

        # Real curriculum adaptation
        if eval_results["mean_reward"] > 0.9:
            adaptive_controller.increase_curriculum_difficulty()
        elif eval_results["mean_reward"] < 0.4:
            adaptive_controller.decrease_curriculum_difficulty()

    # Real training execution
    results = trainer.train(
        on_training_complete=training_complete_callback,
        on_evaluation_complete=evaluation_complete_callback
    )

    # Real final reporting
    return {
        "experiment_id": experiment_id,
        "training_results": results,
        "curriculum_stats": curriculum_manager.get_curriculum_stats(),
        "adaptive_status": adaptive_controller.get_experiment_status()
    }
```

## Real Component Interactions

### 1. Adaptive Controller → Curriculum Manager

#### Data Flow
```
AdaptiveController (Metta) → DAFAdaptiveController
                                      ↓
Curriculum Performance Data → DAFCurriculumManager
                                      ↓
Task Difficulty Adjustment ← Real Curriculum (Metta)
```

#### Implementation
```python
# Real adaptive controller monitors curriculum
adaptive_controller = DAFAdaptiveController(adaptive_config)
curriculum_manager = DAFCurriculumManager(curriculum_config)

# Real performance tracking
def update_curriculum_from_training(training_results):
    """Update curriculum based on real training performance"""

    # Extract real performance metrics
    avg_reward = training_results["avg_reward"]
    task_completion_rate = training_results["completion_rate"]

    # Real curriculum update
    for task_id, performance in training_results["task_performance"].items():
        curriculum_manager.update_task_performance(task_id, performance)

    # Real adaptive decision making
    if avg_reward > 0.85:
        adaptive_controller.increase_curriculum_difficulty()
    elif avg_reward < 0.4:
        adaptive_controller.provide_curriculum_support()

    return curriculum_manager.get_curriculum_stats()
```

### 2. RL Trainer → Adaptive Controller

#### Data Flow
```
RL Training Results → DAFRlTrainer → DAFAdaptiveController
                                      ↓
Adaptive Decisions ← Real AdaptiveController (Metta)
```

#### Implementation
```python
# Real RL trainer with adaptive feedback
trainer = DAFRlTrainer(config=trainer_config, policy=policy)
adaptive_controller = DAFAdaptiveController(adaptive_config)

# Real training with adaptive integration
def train_with_adaptive_control():
    """Train with real adaptive control"""

    episode = 0
    while episode < 1000:
        # Real training step
        training_results = trainer.train_episodes(10)

        # Real adaptive feedback
        adaptive_controller.update_from_training_results(training_results)

        # Real curriculum integration
        if trainer._curriculum_manager:
            current_task = trainer._curriculum_manager.get_next_task()
            if current_task:
                adaptive_controller.set_current_task(current_task)

        episode += 10

    # Real final evaluation
    final_eval = trainer.evaluate_policy()
    adaptive_controller.update_from_evaluation(final_eval)

    return trainer.get_training_summary()
```

### 3. Curriculum Manager → RL Trainer

#### Data Flow
```
Curriculum Tasks → DAFCurriculumManager → DAFRlTrainer
                                      ↓
Environment Configuration ← Real Training Environment
```

#### Implementation
```python
# Real curriculum-driven training
curriculum_manager = DAFCurriculumManager(curriculum_config)
trainer = DAFRlTrainer(config=trainer_config, policy=policy)

def curriculum_driven_training():
    """Train using real curriculum progression"""

    # Real task sequence generation
    task_sequence = curriculum_manager.generate_task_sequence(
        sequence_length=15,
        difficulty_progression="adaptive"
    )

    # Real training on each task
    for task_id in task_sequence:
        # Real task configuration
        task_config = curriculum_manager._custom_tasks[task_id]["config"]

        # Real environment setup
        env = create_environment_from_config(task_config)

        # Real training execution
        training_results = trainer.train_on_task(task_id, env, episodes=50)

        # Real performance feedback
        performance = training_results["avg_reward"]
        curriculum_manager.update_task_performance(task_id, performance)

        # Real curriculum adaptation
        curriculum_stats = curriculum_manager.get_curriculum_stats()
        if curriculum_stats["adaptation_needed"]:
            curriculum_manager.adapt_curriculum("adjust_difficulty")

    return curriculum_manager.get_curriculum_stats()
```

## Error Handling and Recovery

### Real Error Scenarios

#### Adaptive Controller Failure
```python
def handle_adaptive_controller_failure():
    """Handle real adaptive controller failures"""

    try:
        # Real adaptive controller
        controller = DAFAdaptiveController(adaptive_config)
        results = controller.start_experiment()

    except AdaptiveControllerError as e:
        # Real fallback to basic training
        trainer = DAFRlTrainer(config=basic_config, policy=policy)
        results = trainer.train()

        # Real error logging
        logging.error(f"Adaptive controller failed: {e}")
        logging.info("Falling back to basic RL training")

    except TrainingEnvironmentError as e:
        # Real environment recovery
        alternative_env = create_alternative_environment()
        results = controller.run_with_environment(alternative_env)

    return results
```

#### Curriculum Learning Failure
```python
def handle_curriculum_failure():
    """Handle real curriculum learning failures"""

    try:
        # Real curriculum progression
        curriculum_manager = DAFCurriculumManager(curriculum_config)
        task_sequence = curriculum_manager.generate_task_sequence(10)

        for task_id in task_sequence:
            results = train_on_task(task_id)

            # Real curriculum update
            curriculum_manager.update_task_performance(task_id, results["reward"])

    except CurriculumStagnationError as e:
        # Real curriculum adaptation
        curriculum_manager.adapt_curriculum("reduce_difficulty")
        alternative_sequence = curriculum_manager.generate_task_sequence(5)

        for task_id in alternative_sequence:
            results = train_on_task(task_id)

    except TaskGenerationError as e:
        # Real fallback to basic tasks
        basic_tasks = ["simple_task_1", "simple_task_2", "simple_task_3"]

        for task_id in basic_tasks:
            results = train_on_task(task_id)
```

## Monitoring and Observability

### Real Monitoring Integration

#### Comprehensive Logging
```python
# Real logging setup
from daf.src.daf.logging import setup_daf_logging, LogManager, DAFLogger

def setup_comprehensive_monitoring():
    """Set up real monitoring for all components"""

    # Real logging configuration
    setup_daf_logging(
        log_level="INFO",
        log_file="production_training.log",
        console_output=True
    )

    # Real component logging
    log_manager = LogManager("production_logs")

    adaptive_logger = log_manager.setup_component_logging("daf.core.adaptive", "INFO")
    curriculum_logger = log_manager.setup_component_logging("daf.core.curriculum", "INFO")
    training_logger = log_manager.setup_component_logging("daf.core.training", "INFO")

    # Real structured logging
    def log_training_progress(results):
        DAFLogger("training").info("Training Progress", {
            "episode": results["episodes"],
            "avg_reward": results["avg_reward"],
            "best_reward": results["best_reward"]
        })

    def log_curriculum_progress(stats):
        DAFLogger("curriculum").info("Curriculum Progress", {
            "tasks_completed": stats["num_custom_tasks"],
            "avg_performance": stats["avg_performance"]
        })

    return log_manager, log_training_progress, log_curriculum_progress
```

#### Real Metrics Collection
```python
def collect_comprehensive_metrics():
    """Collect real metrics from all components"""

    # Real training metrics
    training_metrics = trainer.get_training_metrics()

    # Real curriculum metrics
    curriculum_metrics = curriculum_manager.get_curriculum_stats()

    # Real adaptive controller metrics
    adaptive_metrics = adaptive_controller.get_experiment_status()

    # Real system metrics
    system_metrics = {
        "cpu_usage": get_cpu_usage(),
        "memory_usage": get_memory_usage(),
        "gpu_usage": get_gpu_usage()
    }

    # Real comprehensive reporting
    all_metrics = {
        "training": training_metrics,
        "curriculum": curriculum_metrics,
        "adaptive": adaptive_metrics,
        "system": system_metrics,
        "timestamp": datetime.now().isoformat()
    }

    # Real external monitoring integration
    if adaptive_config.integrate_with_wandb:
        adaptive_controller._store.log_metrics(all_metrics)

    return all_metrics
```

## Performance Optimization

### Real Performance Monitoring

#### Training Performance
```python
def monitor_training_performance():
    """Monitor real training performance"""

    # Real performance metrics
    performance_metrics = {
        "episodes_per_second": trainer.get_episodes_per_second(),
        "timesteps_per_second": trainer.get_timesteps_per_second(),
        "policy_update_frequency": trainer.get_update_frequency(),
        "gradient_norm": trainer.get_gradient_norm()
    }

    # Real optimization
    if performance_metrics["episodes_per_second"] < 10:
        # Real performance optimization
        trainer.increase_batch_size()
        trainer.enable_gradient_clipping()

    return performance_metrics
```

#### Memory Management
```python
def manage_memory_usage():
    """Manage real memory usage in training"""

    # Real memory monitoring
    memory_stats = {
        "policy_memory": get_policy_memory_usage(),
        "environment_memory": get_environment_memory_usage(),
        "curriculum_memory": get_curriculum_memory_usage()
    }

    # Real memory optimization
    if memory_stats["policy_memory"] > 1024 * 1024 * 1024:  # 1GB
        # Real model optimization
        policy.enable_gradient_checkpointing()
        policy.use_mixed_precision()

    if memory_stats["environment_memory"] > 500 * 1024 * 1024:  # 500MB
        # Real environment optimization
        env.reduce_buffer_size()
        env.enable_lazy_loading()

    return memory_stats
```

This integration guide demonstrates how all DAF components work together with real Metta functionality to provide comprehensive, production-ready multi-agent RL capabilities.
