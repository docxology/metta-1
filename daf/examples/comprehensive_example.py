#!/usr/bin/env python3
"""
DAF Comprehensive Example

This example demonstrates all major DAF functionality including:
- Configuration management
- Simulation running
- Output management
- Error handling
- Real Metta AI integration
"""

import asyncio
import json
from datetime import datetime

from daf.config.configuration import ConfigurationManager
from daf.core.output import get_example_output_path, get_output_manager
from daf.core.simulation import SimulationRunner
from daf.core.validation import SystemValidator


async def run_comprehensive_example():
    """Run a comprehensive example of DAF functionality."""
    print("🚀 DAF Comprehensive Example")
    print("=" * 50)

    # Setup output directory
    example_output = get_example_output_path("comprehensive_example")
    print(f"📁 Output directory: {example_output}")

    # Save example metadata
    metadata = {
        "example_name": "comprehensive_example",
        "timestamp": datetime.now().isoformat(),
        "description": "Comprehensive DAF functionality demonstration",
        "steps": [
            "Configuration management",
            "System validation",
            "Simulation setup",
            "Experiment execution",
            "Results analysis",
            "Output management",
        ],
    }

    with open(example_output / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)

    try:
        # Step 1: Configuration Management
        print("\n🔧 Step 1: Configuration Management")
        config_manager = ConfigurationManager()

        # Load a base configuration
        config = config_manager.load_config_file("configs/experiments/quick_test.yaml")
        print(f"✅ Loaded configuration: {config.name}")

        # Apply custom overrides
        overrides = {
            "training.total_timesteps": 50000,
            "environment.num_agents": 16,
            "evaluation.frequency": 5000,
        }
        modified_config = config_manager.apply_overrides(config, overrides)
        print(f"✅ Applied overrides: {len(overrides)} modifications")

        # Step 2: System Validation
        print("\n🔍 Step 2: System Validation")
        validator = SystemValidator()
        system_result = validator.validate_system()
        print(f"✅ System validation: {'PASSED' if system_result.is_valid else 'FAILED'}")

        if not system_result.is_valid:
            print("⚠️  System issues found:")
            for issue in system_result.issues:
                print(f"  - {issue}")
        else:
            print("✅ All system requirements met")

        # Step 3: Simulation Setup
        print("\n⚙️  Step 3: Simulation Setup")
        runner = SimulationRunner(modified_config)
        print(f"✅ Simulation runner created for: {runner.config.name}")

        # Check engine readiness
        if runner.engine.is_ready():
            print("✅ Metta engine is ready")
        else:
            print("⚠️  Metta engine is not ready (expected in test environment)")

        # Step 4: Configuration Validation
        print("\n📋 Step 4: Configuration Validation")
        validation_result = config_manager.validate_config(modified_config)
        if validation_result.is_valid:
            print("✅ Configuration is valid")
        else:
            print("❌ Configuration validation failed")
            return

        # Step 5: Output Management
        print("\n📁 Step 5: Output Management")
        output_info = get_output_manager().get_output_info()
        print(f"✅ Output manager configured: {len(output_info['categories'])} categories")

        # Step 6: Simulation Execution (Dry Run)
        print("\n🎮 Step 6: Simulation Execution")
        print("🔍 Running simulation in dry-run mode...")

        # Create a simple mock result
        mock_result = {
            "experiment_name": modified_config.name,
            "status": "completed",
            "metrics": {
                "total_reward": 1250.75,
                "episode_length": 150,
                "convergence_time": 75.0,
                "success_rate": 0.85,
            },
            "execution_time": 45.2,
            "artifacts": {
                "checkpoint": str(example_output / "model_final.pt"),
                "metrics": str(example_output / "metrics.json"),
            },
        }

        # Save mock results
        with open(example_output / "results.json", "w") as f:
            json.dump(mock_result, f, indent=2)

        print("✅ Simulation completed (mock results saved)")
        print(f"📊 Final reward: {mock_result['metrics']['total_reward']}")
        print(f"⏱️  Execution time: {mock_result['execution_time']}s")

        # Step 7: Results Analysis
        print("\n📈 Step 7: Results Analysis")
        analysis = analyze_results(mock_result)
        with open(example_output / "analysis.json", "w") as f:
            json.dump(analysis, f, indent=2)

        print("✅ Results analysis completed")
        print(f"📊 Average reward per step: {analysis['metrics']['avg_reward_per_step']:.2f}")

        # Step 8: Cleanup and Summary
        print("\n🧹 Step 8: Cleanup and Summary")
        cleanup_count = get_output_manager().cleanup_old_outputs(days_old=30)
        print(f"✅ Cleanup completed: {cleanup_count} old directories removed")

        # Final summary
        print("\n" + "=" * 50)
        print("🎉 Comprehensive Example Completed Successfully!")
        print("=" * 50)

        summary = {
            "example": "comprehensive_example",
            "status": "completed",
            "configurations_tested": 1,
            "system_validation": system_result.is_valid,
            "mock_simulation": True,
            "output_directory": str(example_output),
            "files_created": ["metadata.json", "results.json", "analysis.json"],
        }

        with open(example_output / "summary.json", "w") as f:
            json.dump(summary, f, indent=2)

        print("📋 Summary saved to summary.json")
        print(f"📁 All outputs in: {example_output}")
        print("\n💡 Next steps:")
        print("• Run 'python examples/comprehensive_example.py' to see this in action")
        print("• Modify configs/experiments/ to create custom experiments")
        print("• Check outputs/examples/comprehensive_example/ for results")

        return True

    except Exception as e:
        print(f"\n❌ Example failed: {e}")
        import traceback

        print(traceback.format_exc())

        # Save error information
        error_info = {
            "example": "comprehensive_example",
            "status": "failed",
            "error": str(e),
            "traceback": traceback.format_exc(),
            "timestamp": datetime.now().isoformat(),
        }

        with open(example_output / "error.json", "w") as f:
            json.dump(error_info, f, indent=2)

        return False


def analyze_results(results: dict) -> dict:
    """Analyze simulation results and generate insights."""
    metrics = results.get("metrics", {})

    analysis = {
        "experiment_info": {
            "name": results.get("experiment_name", "unknown"),
            "status": results.get("status", "unknown"),
            "execution_time": results.get("execution_time", 0),
        },
        "metrics": {},
        "insights": [],
        "recommendations": [],
    }

    if metrics:
        total_reward = metrics.get("total_reward", 0)
        episode_length = metrics.get("episode_length", 1)
        convergence_time = metrics.get("convergence_time", episode_length)

        analysis["metrics"] = {
            "total_reward": total_reward,
            "avg_reward_per_step": total_reward / episode_length,
            "episode_length": episode_length,
            "convergence_rate": convergence_time / episode_length if episode_length > 0 else 0,
            "success_rate": metrics.get("success_rate", 0),
        }

        # Generate insights
        avg_reward = analysis["metrics"]["avg_reward_per_step"]

        if avg_reward > 10:
            analysis["insights"].append("Excellent performance - high reward efficiency")
        elif avg_reward > 5:
            analysis["insights"].append("Good performance - moderate reward efficiency")
        elif avg_reward > 2:
            analysis["insights"].append("Fair performance - room for improvement")
        else:
            analysis["insights"].append("Poor performance - needs optimization")

        # Generate recommendations
        if episode_length < 50:
            analysis["recommendations"].append("Consider increasing episode length for better learning")
        if convergence_time > episode_length * 0.8:
            analysis["recommendations"].append("Learning convergence is slow - check hyperparameters")

    return analysis


async def main():
    """Main function to run the comprehensive example."""
    success = await run_comprehensive_example()

    if success:
        print("\n✅ Example completed successfully!")
        print("📁 Check outputs/examples/comprehensive_example/ for all generated files")
    else:
        print("\n❌ Example failed - check error logs")
        return 1

    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
