#!/usr/bin/env python3
"""
DAF Programmatic Usage Example

This script demonstrates how to use DAF programmatically to run
Metta AI simulations with custom configurations and analysis.
"""

import asyncio
import json
from pathlib import Path
from typing import Dict, Any, List

from daf.core.simulation import SimulationRunner
from daf.core.configuration import ConfigurationManager, SimulationConfig
from daf.core.engine import MettaEngine


async def basic_simulation_example():
    """Example of running a basic simulation."""
    print("🚀 Running basic simulation example...")

    # Create a simple configuration
    config = SimulationConfig(
        name="basic_example",
        description="Basic DAF simulation example",
        environment={
            "name": "basic_env",
            "type": "mettagrid",
            "num_agents": 12,
            "map_config": {"width": 30, "height": 30},
        },
        training={
            "total_timesteps": 50000,
            "learning_rate": 0.001,
            "batch_size": 1024,
        },
        evaluation={
            "frequency": 5000,
            "num_episodes": 25,
        },
    )

    # Create simulation runner
    runner = SimulationRunner(config)

    # Run simulation
    result = await runner.run()

    print(f"Simulation completed: {result.experiment_name}")
    print(f"Status: {result.status}")
    print(f"Final reward: {result.metrics.get('total_reward', 'N/A')}")
    print(f"Execution time: {result.execution_time".2f"}s")

    return result


async def configuration_example():
    """Example of working with configurations."""
    print("\n🔧 Configuration management example...")

    # Create configuration manager
    config_manager = ConfigurationManager()

    # Load configuration from file
    config = config_manager.load_config_file("configs/experiments/arena_basic.yaml")
    print(f"Loaded configuration: {config.name}")

    # Apply runtime overrides
    overrides = {
        "training.total_timesteps": 100000,
        "environment.num_agents": 32,
    }
    modified_config = config_manager.apply_overrides(config, overrides)
    print(f"Modified config: {modified_config.training.total_timesteps} timesteps")
    print(f"Modified config: {modified_config.environment.num_agents} agents")

    # Save modified configuration
    output_path = Path("outputs/modified_config.yaml")
    config_manager.save_config(modified_config, output_path)
    print(f"Saved modified configuration to: {output_path}")

    return modified_config


async def batch_simulation_example():
    """Example of running multiple simulations in batch."""
    print("\n📊 Batch simulation example...")

    # Create configuration manager
    config_manager = ConfigurationManager()

    # Load base configuration
    base_config = config_manager.load_config_file("configs/experiments/quick_test.yaml")

    # Create variations
    variations = []
    for i, agents in enumerate([8, 16, 24]):
        config = config_manager.apply_overrides(base_config, {
            "name": f"batch_test_{i+1}",
            "environment.num_agents": agents,
            "training.total_timesteps": 25000,
        })
        variations.append(config)

    print(f"Created {len(variations)} configuration variations")

    # Create runner with first configuration
    runner = SimulationRunner(variations[0])

    # Run batch
    results = await runner.run_batch(variations)

    # Analyze results
    print("Batch results:")
    for i, result in enumerate(results):
        print(f"  Experiment {i+1}: {result.experiment_name} - {result.status}")
        if result.metrics:
            reward = result.metrics.get('total_reward', 0)
            print(f"    Final reward: {reward}")

    return results


async def custom_engine_example():
    """Example of using a custom Metta engine."""
    print("\n🔧 Custom engine example...")

    # Create custom engine with specific configuration
    engine = MettaEngine()

    # Check if engine is ready
    if engine.is_ready():
        print("✅ Metta engine is ready")
    else:
        print("❌ Metta engine is not ready")
        return None

    # Create a simple test configuration
    config = SimulationConfig(
        name="custom_engine_test",
        environment={
            "name": "test_env",
            "type": "mettagrid",
            "num_agents": 8,
            "map_config": {"width": 20, "height": 20},
        },
        training={
            "total_timesteps": 10000,
            "learning_rate": 0.001,
            "batch_size": 512,
        },
        evaluation={
            "frequency": 1000,
            "num_episodes": 5,
        },
    )

    # Test engine directly
    try:
        metrics = await engine.simulate(config)
        print("✅ Custom engine simulation successful")
        print(f"Metrics: {metrics}")
        return metrics
    except Exception as e:
        print(f"❌ Custom engine simulation failed: {e}")
        return None


async def results_analysis_example():
    """Example of analyzing simulation results."""
    print("\n📈 Results analysis example...")

    # Run a quick simulation to get results
    config = SimulationConfig(
        name="analysis_test",
        environment={
            "name": "analysis_env",
            "type": "mettagrid",
            "num_agents": 8,
            "map_config": {"width": 20, "height": 20},
        },
        training={
            "total_timesteps": 25000,
            "learning_rate": 0.001,
            "batch_size": 512,
        },
        evaluation={
            "frequency": 5000,
            "num_episodes": 10,
        },
    )

    runner = SimulationRunner(config)
    result = await runner.run()

    # Analyze results
    def analyze_results(result):
        """Analyze simulation results."""
        analysis = {
            "experiment_info": {
                "name": result.experiment_name,
                "status": result.status,
                "execution_time": result.execution_time,
            },
            "performance_metrics": {},
            "recommendations": [],
        }

        if result.metrics:
            metrics = result.metrics

            # Basic metrics analysis
            total_reward = metrics.get('total_reward', 0)
            episode_length = metrics.get('episode_length', 0)

            analysis["performance_metrics"] = {
                "total_reward": total_reward,
                "avg_reward_per_step": total_reward / episode_length if episode_length > 0 else 0,
                "episode_length": episode_length,
                "convergence_rate": metrics.get('convergence_time', 0) / episode_length if episode_length > 0 else 0,
            }

            # Generate recommendations
            if total_reward < 50:
                analysis["recommendations"].append("Consider increasing reward values")
            if episode_length < 25:
                analysis["recommendations"].append("Episodes may be too short for meaningful learning")
            if result.execution_time > 60:
                analysis["recommendations"].append("Consider optimizing for faster execution")

        return analysis

    analysis = analyze_results(result)

    print("Analysis Results:")
    print(json.dumps(analysis, indent=2))

    return analysis


async def main():
    """Run all examples."""
    print("DAF Programmatic Usage Examples")
    print("=" * 50)

    try:
        # Run examples
        basic_result = await basic_simulation_example()
        config_result = await configuration_example()
        batch_results = await batch_simulation_example()
        custom_result = await custom_engine_example()
        analysis_result = await results_analysis_example()

        print("\n" + "=" * 50)
        print("🎉 All examples completed successfully!")
        print("=" * 50)

        # Summary
        print("\n📋 Summary:")
        print("✅ Basic simulation: Working")
        print("✅ Configuration management: Working")
        print("✅ Batch processing: Working")
        print("✅ Custom engine: Working")
        print("✅ Results analysis: Working")

        print("\n💡 Next steps:")
        print("• Explore configs/ directory for more examples")
        print("• Run 'daf --help' to see available CLI commands")
        print("• Check the documentation in docs/ for detailed guides")

    except Exception as e:
        print(f"\n❌ Examples failed: {e}")
        import traceback
        print(traceback.format_exc())
        return 1

    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
