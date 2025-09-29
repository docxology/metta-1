#!/usr/bin/env python3
"""
DAF Real Simulation Data Generator

This module generates realistic simulation data that mimics actual Metta AI outputs
for comprehensive visualization testing. Due to build environment limitations,
we're using realistic mock data that demonstrates the full DAF visualization
capabilities with Metta-like data structures.

HONEST REPORTING: This uses realistic mock data, not actual Metta simulation outputs.
Real Metta integration would require Bazel build environment setup.
"""

import json
import random
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from daf.core.output import get_example_output_path


class RealSimulationDataGenerator:
    """Generate realistic simulation data for comprehensive testing."""

    def __init__(self, output_path: Path):
        self.output_path = output_path
        self.simulation_metadata = self._generate_simulation_metadata()

    def _generate_simulation_metadata(self) -> Dict[str, Any]:
        """Generate realistic simulation metadata."""
        return {
            "simulation_id": f"sim_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "environment": "arena_complex",
            "num_agents": 24,
            "map_size": [25, 20],
            "total_episodes": 1000,
            "current_episode": 750,
            "simulation_time": 45.2,
            "seed": 42,
            "metta_version": "0.1.0",
            "daf_version": "1.0.0",
            "build_environment": "mock_data_for_visualization",
        }

    def generate_agent_data(self, num_agents: int = 24, num_frames: int = 150) -> Dict[str, Any]:
        """Generate realistic agent trajectory and state data."""
        print(f"🤖 Generating realistic agent data for {num_agents} agents over {num_frames} frames...")

        agent_data = {}
        base_positions = [
            [5, 5],
            [15, 10],
            [8, 15],
            [22, 8],
            [12, 3],
            [18, 18],
            [3, 12],
            [20, 6],
            [7, 20],
            [16, 14],
            [10, 9],
            [14, 16],
            [6, 7],
            [19, 11],
            [9, 13],
            [17, 5],
            [4, 17],
            [21, 15],
            [11, 4],
            [13, 19],
            [8, 8],
            [16, 12],
            [7, 6],
            [18, 9],
        ][:num_agents]

        for i in range(num_agents):
            agent_id = f"agent_{i}"
            start_pos = base_positions[i]

            # Generate realistic movement pattern
            positions = []
            current_pos = list(start_pos)

            for frame in range(num_frames):
                # Add some realistic movement with exploration
                if frame % 20 == 0 and random.random() < 0.3:
                    # Change direction occasionally
                    dx = random.choice([-1, 0, 1])
                    dy = random.choice([-1, 0, 1])
                    if dx != 0 or dy != 0:
                        current_pos[0] = max(0, min(24, current_pos[0] + dx))
                        current_pos[1] = max(0, min(19, current_pos[1] + dy))

                # Add small random movement for realism
                noise_x = random.gauss(0, 0.1)
                noise_y = random.gauss(0, 0.1)
                positions.append([max(0, min(24, current_pos[0] + noise_x)), max(0, min(19, current_pos[1] + noise_y))])

            agent_data[agent_id] = {
                "positions": positions,
                "inventory": {
                    "ore_red": random.randint(0, 5),
                    "battery_red": random.randint(1, 8),
                    "laser": random.randint(0, 2),
                    "armor": random.randint(0, 3),
                },
                "actions": [
                    random.choice(
                        [
                            "move_north",
                            "move_south",
                            "move_east",
                            "move_west",
                            "collect_ore",
                            "attack",
                            "defend",
                            "build_generator",
                            "resource_sharing",
                            "communication",
                        ]
                    )
                    for _ in range(num_frames)
                ],
                "rewards": [random.gauss(0.5, 0.3) for _ in range(num_frames)],
                "health": [max(0, 100 - frame * 0.1 + random.gauss(0, 5)) for frame in range(num_frames)],
                "energy": [max(0, 100 - frame * 0.05 + random.gauss(0, 2)) for _ in range(num_frames)],
                "experience": [frame * 0.1 + random.gauss(0, 1) for frame in range(num_frames)],
            }

        return agent_data

    def generate_environment_data(self, num_frames: int = 150) -> Dict[str, Any]:
        """Generate realistic environment state data."""
        print("🌍 Generating realistic environment data...")

        return {
            "resource_distribution": {
                "ore_red": [random.randint(0, 5) for _ in range(num_frames)],
                "battery_red": [random.randint(0, 3) for _ in range(num_frames)],
                "generator_active": [random.choice([True, False]) for _ in range(num_frames)],
                "resource_spawn_rate": [0.1 + random.gauss(0, 0.02) for _ in range(num_frames)],
            },
            "collision_events": [
                {
                    "frame": random.randint(0, num_frames - 1),
                    "agent_1": f"agent_{random.randint(0, 23)}",
                    "agent_2": f"agent_{random.randint(0, 23)}",
                    "collision_type": random.choice(["physical", "resource_dispute", "communication"]),
                    "resolution": random.choice(["avoidance", "conflict", "cooperation"]),
                }
                for _ in range(random.randint(10, 20))
            ],
            "resource_depletion_events": [
                {
                    "frame": random.randint(0, num_frames - 1),
                    "resource": random.choice(["ore_red", "battery_red"]),
                    "location": [random.randint(0, 24), random.randint(0, 19)],
                    "cause": random.choice(["overharvesting", "natural_depletion", "agent_activity"]),
                }
                for _ in range(random.randint(5, 15))
            ],
            "environmental_hazards": [
                {
                    "frame": random.randint(0, num_frames - 1),
                    "hazard_type": random.choice(["radiation_zone", "unstable_terrain", "energy_field"]),
                    "location": [random.randint(0, 24), random.randint(0, 19)],
                    "severity": random.gauss(0.5, 0.2),
                }
                for _ in range(random.randint(3, 8))
            ],
        }

    def generate_training_progress(self, num_episodes: int = 1000) -> Dict[str, Any]:
        """Generate realistic training progress data."""
        print("📈 Generating realistic training progress data...")

        # Create realistic learning curve
        episode_rewards = []
        episode_lengths = []
        success_rates = []
        exploration_rates = []

        base_reward = 100
        for i in range(num_episodes):
            # Learning curve with noise
            progress_factor = min(1.0, i / 200.0)  # Learning phase
            noise = random.gauss(0, 20)
            reward = base_reward * (0.3 + 0.7 * progress_factor) + noise
            episode_rewards.append(max(0, reward))

            # Episode length decreases as agents learn
            base_length = 200
            length_noise = random.gauss(0, 10)
            length = base_length * (0.8 - 0.6 * progress_factor) + length_noise
            episode_lengths.append(max(50, length))

            # Success rate improves
            success_noise = random.gauss(0, 0.1)
            success_rate = min(1.0, 0.2 + 0.7 * progress_factor + success_noise)
            success_rates.append(success_rate)

            # Exploration rate decreases
            exploration_noise = random.gauss(0, 0.05)
            exploration_rate = max(0.05, 0.3 - 0.25 * progress_factor + exploration_noise)
            exploration_rates.append(exploration_rate)

        return {
            "episode_rewards": episode_rewards,
            "episode_lengths": episode_lengths,
            "success_rates": success_rates,
            "exploration_rates": exploration_rates,
            "training_times": [random.gauss(120, 15) for _ in range(num_episodes)],
            "convergence_metrics": {
                "final_avg_reward": episode_rewards[-1],
                "best_reward": max(episode_rewards),
                "convergence_episode": next(i for i, r in enumerate(episode_rewards) if r > base_reward * 0.8),
                "training_stability": 0.85,
            },
        }

    def generate_diagnostic_data(self, num_frames: int = 150) -> Dict[str, Any]:
        """Generate comprehensive diagnostic information."""
        print("🔍 Generating comprehensive diagnostic data...")

        return {
            "system_performance": {
                "cpu_usage": [random.gauss(65, 10) for _ in range(num_frames)],
                "memory_usage": [random.gauss(2.3, 0.3) for _ in range(num_frames)],
                "gpu_memory": [random.gauss(8.0, 1.0) for _ in range(num_frames)],
                "simulation_fps": [random.gauss(30, 5) for _ in range(num_frames)],
            },
            "agent_diagnostics": {
                "decision_times": [random.gauss(0.02, 0.005) for _ in range(num_frames)],
                "action_success_rates": [random.gauss(0.85, 0.1) for _ in range(num_frames)],
                "communication_overhead": [random.gauss(0.1, 0.02) for _ in range(num_frames)],
                "coordination_efficiency": [random.gauss(0.82, 0.08) for _ in range(num_frames)],
            },
            "environment_diagnostics": {
                "resource_spawn_success": [random.gauss(0.95, 0.05) for _ in range(num_frames)],
                "collision_resolution_rate": [random.gauss(0.90, 0.05) for _ in range(num_frames)],
                "pathfinding_success": [random.gauss(0.88, 0.07) for _ in range(num_frames)],
                "state_consistency": [random.gauss(0.99, 0.01) for _ in range(num_frames)],
            },
        }

    def generate_comprehensive_simulation_data(self) -> Dict[str, Any]:
        """Generate all types of realistic simulation data."""
        print("🎯 Generating comprehensive simulation data...")

        num_frames = 150
        num_agents = 24

        simulation_data = {
            "metadata": self.simulation_metadata,
            "agent_data": self.generate_agent_data(num_agents, num_frames),
            "environment_data": self.generate_environment_data(num_frames),
            "training_data": self.generate_training_progress(1000),
            "diagnostic_data": self.generate_diagnostic_data(num_frames),
            "generated_at": datetime.now().isoformat(),
            "data_type": "realistic_mock_for_visualization",
            "note": "This is realistic mock data for DAF visualization testing. "
            "Real Metta integration requires Bazel build environment.",
        }

        return simulation_data

    def save_simulation_data(self, data: Dict[str, Any], filename: str = "comprehensive_simulation_data.json"):
        """Save comprehensive simulation data to file."""
        output_file = self.output_path / filename
        with open(output_file, "w") as f:
            json.dump(data, f, indent=2)

        print(f"💾 Comprehensive simulation data saved: {output_file}")
        return str(output_file)


def main():
    """Main function to generate comprehensive simulation data."""
    print("🎯 DAF Realistic Simulation Data Generator")
    print("=" * 60)
    print("📝 HONEST REPORTING: Using realistic mock data due to build environment limitations")
    print("📝 Real Metta integration requires Bazel setup: https://bazel.build/install")
    print("=" * 60)

    # Setup output directory
    example_output = get_example_output_path("real_simulation_data")
    print(f"📁 Output directory: {example_output}")

    # Generate comprehensive data
    generator = RealSimulationDataGenerator(example_output)
    simulation_data = generator.generate_comprehensive_simulation_data()

    # Save data
    data_file = generator.save_simulation_data(simulation_data)

    # Generate summary report
    summary = {
        "realistic_simulation_data_report": {
            "status": "completed",
            "data_type": "realistic_mock_for_visualization",
            "simulation_metadata": simulation_data["metadata"],
            "data_files_generated": [data_file],
            "output_directory": str(example_output),
            "generated_at": datetime.now().isoformat(),
            "note": "This data represents realistic Metta AI simulation outputs for visualization testing. "
            "Real Metta integration requires proper build environment setup.",
        },
        "data_characteristics": {
            "total_frames": 150,
            "num_agents": 24,
            "episodes_simulated": 1000,
            "data_categories": [
                "agent_trajectories",
                "environment_states",
                "training_progress",
                "system_diagnostics",
                "collision_events",
                "resource_management",
            ],
            "realism_level": "high",
        },
        "visualization_ready": {
            "agent_parameter_tracking": True,
            "environment_variable_monitoring": True,
            "diagnostic_data_available": True,
            "multi_agent_coordination": True,
            "training_progress_analysis": True,
            "performance_monitoring": True,
        },
    }

    summary_file = example_output / "realistic_data_summary.json"
    with open(summary_file, "w") as f:
        json.dump(summary, f, indent=2)

    print("\n🎯 Realistic Simulation Data Features Generated:")
    print("  ✅ Agent trajectory data with realistic movement patterns")
    print("  ✅ Environment state tracking with resource dynamics")
    print("  ✅ Training progress data with learning curves")
    print("  ✅ System diagnostics with performance metrics")
    print("  ✅ Multi-agent coordination events")
    print("  ✅ Resource management and depletion events")
    print("  ✅ Collision detection and resolution")
    print("  ✅ Health, energy, and experience tracking")

    print("\n📋 Generated Files:")
    print(f"  ✅ {data_file}")
    print(f"  ✅ {summary_file}")

    print(f"\n📁 All outputs in: {example_output}")
    print("\n🚀 Ready for DAF Visualization:")
    print("  • Use this data with DAF visualization tools")
    print("  • Run: python examples/metta_visualization_master.py")
    print("  • View: outputs/examples/metta_visualization_master/")
    print("  • Analyze: outputs/examples/analysis_notebook_example/")

    print("\n✅ Realistic simulation data generation completed!")
    print("📝 Note: Real Metta integration requires Bazel build environment")


if __name__ == "__main__":
    main()

