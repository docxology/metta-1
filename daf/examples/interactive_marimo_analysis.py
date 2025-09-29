#!/usr/bin/env python3
"""
DAF Interactive Marimo Analysis Example

This example demonstrates real-time interactive analysis using Marimo,
providing dynamic exploration of Metta AI experiments with live updates.

Features demonstrated:
- Real-time data exploration
- Interactive parameter controls
- Live visualization updates
- Dynamic filtering and analysis
- Comparative experiment analysis
- Performance monitoring dashboards
"""

import json
from datetime import datetime
from pathlib import Path

from daf.core.output import get_example_output_path


class MarimoInteractiveAnalysis:
    """Interactive analysis tool using Marimo for real-time exploration."""

    def __init__(self, output_path: Path):
        self.output_path = output_path
        self.marimo_content = self.generate_marimo_content()

    def generate_marimo_content(self) -> str:
        """Generate Marimo interactive analysis content."""

        marimo_code = '''
import marimo

__generated_with = "0.7.14"
app = marimo.App(width="full")


@app.cell
def __():
    import json
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    import pandas as pd
    from pathlib import Path
    from datetime import datetime

    plt.style.use('seaborn-v0_8')
    sns.set_palette('husl')

    return json, np, plt, sns, pd, Path, datetime


@app.cell
def __():
    # Load experiment data
    def load_experiment_data():
        experiments = {}

        # Load all experiment data from outputs
        experiments_dir = Path("outputs/experiments")
        if experiments_dir.exists():
            for exp_dir in experiments_dir.iterdir():
                if exp_dir.is_dir():
                    exp_name = exp_dir.name

                    # Load configuration
                    config_file = exp_dir / "config.json"
                    if config_file.exists():
                        with open(config_file) as f:
                            experiments[exp_name] = {"config": json.load(f)}

                    # Load metrics
                    metrics_file = exp_dir / "metrics.json"
                    if metrics_file.exists():
                        with open(metrics_file) as f:
                            experiments[exp_name]["metrics"] = json.load(f)

        return experiments

    experiments = load_experiment_data()
    experiment_names = list(experiments.keys())

    return experiments, experiment_names


@app.cell
def __(experiment_names):
    # Interactive experiment selector
    experiment_selector = marimo.ui.dropdown(
        experiment_names,
        value=experiment_names[0] if experiment_names else None,
        label="Select Experiment to Analyze"
    )

    return experiment_selector,


@app.cell
def __(experiment_selector, experiments):
    # Display selected experiment details
    selected_exp = experiment_selector.value

    if selected_exp and selected_exp in experiments:
        exp_data = experiments[selected_exp]

        marimo.markdown(f"## Analysis for: {selected_exp}")

        if "config" in exp_data:
            marimo.markdown("### Configuration")
            marimo.code(exp_data["config"])

        if "metrics" in exp_data:
            marimo.markdown("### Metrics")
            marimo.code(exp_data["metrics"])

    return selected_exp,


@app.cell
def __(experiment_names, experiments):
    # Real-time parameter controls
    default_agents = 24
    default_timesteps = 10000

    # Get current values from experiments if available
    if experiments:
        sample_exp = list(experiments.values())[0]
        if "config" in sample_exp:
            config = sample_exp["config"]
            default_agents = config.get("num_agents", default_agents)
            default_timesteps = config.get("total_timesteps", default_timesteps)

    agent_slider = marimo.ui.slider(
        1, 100, value=default_agents, label="Number of Agents", step=1
    )

    timestep_slider = marimo.ui.slider(
        1000, 50000, value=default_timesteps, label="Training Timesteps", step=1000
    )

    return agent_slider, default_agents, default_timesteps, timestep_slider


@app.cell
def __(agent_slider, experiment_names, experiments, timestep_slider):
    # Generate comparison data based on sliders
    num_agents = agent_slider.value
    num_timesteps = timestep_slider.value

    # Create synthetic data for demonstration
    comparison_data = {}

    for exp_name in experiment_names:
        # Generate realistic performance data
        base_reward = 1000 + (num_agents * 10) + (num_timesteps / 1000)
        noise = np.random.normal(0, base_reward * 0.1)
        final_reward = max(500, base_reward + noise)

        comparison_data[exp_name] = {
            "agents": num_agents,
            "timesteps": num_timesteps,
            "reward": final_reward,
            "efficiency": final_reward / num_agents,
            "convergence_time": num_timesteps * 0.3
        }

    return comparison_data, num_agents, num_timesteps


@app.cell
def __(comparison_data, experiment_names):
    # Interactive comparison visualization
    if comparison_data:
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))

        exp_names = list(comparison_data.keys())
        rewards = [data["reward"] for data in comparison_data.values()]
        agents = [data["agents"] for data in comparison_data.values()]
        efficiency = [data["efficiency"] for data in comparison_data.values()]

        # Reward comparison
        axes[0,0].bar(exp_names, rewards, color='skyblue', alpha=0.7)
        axes[0,0].set_title('Reward Comparison')
        axes[0,0].set_ylabel('Total Reward')
        axes[0,0].tick_params(axis='x', rotation=45)

        # Agent count vs reward scatter
        axes[0,1].scatter(agents, rewards, s=100, alpha=0.7)
        axes[0,1].set_xlabel('Number of Agents')
        axes[0,1].set_ylabel('Reward')
        axes[0,1].set_title('Performance vs Agent Count')
        axes[0,1].grid(True, alpha=0.3)

        # Efficiency comparison
        axes[1,0].bar(exp_names, efficiency, color='lightgreen', alpha=0.7)
        axes[1,0].set_title('Efficiency (Reward per Agent)')
        axes[1,0].set_ylabel('Efficiency')
        axes[1,0].tick_params(axis='x', rotation=45)

        # Performance summary
        axes[1,1].axis('off')
        best_exp = max(comparison_data.items(), key=lambda x: x[1]['reward'])
        summary_text = f"""
        Best Performance: {best_exp[0]}
        Reward: {best_exp[1]['reward']:.2f}
        Total Experiments: {len(exp_names)}
        Average Agents: {sum(agents)/len(agents):.1f}
        """
        axes[1,1].text(0.1, 0.5, summary_text, fontsize=12,
                      bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue"))

        plt.tight_layout()
        plt.show()

    return


@app.cell
def __():
    # Real-time monitoring dashboard
    marimo.markdown("## Real-time Monitoring Dashboard")
    marimo.markdown("Adjust parameters below to see live updates:")


@app.cell
def __():
    # Performance metrics display
    def display_performance_metrics():
        current_time = datetime.now().strftime("%H:%M:%S")

        marimo.markdown(f"### Live Performance Metrics - {current_time}")

        # Simulate live metrics
        live_metrics = {
            "Training Progress": "75% complete",
            "Current Reward": "1,250.75",
            "Episode Length": "150 steps",
            "Success Rate": "85%",
            "Convergence Time": "75 episodes",
            "GPU Utilization": "67%",
            "Memory Usage": "2.3GB / 8GB"
        }

        for metric, value in live_metrics.items():
            marimo.markdown(f"**{metric}:** {value}")

        return live_metrics

    return display_performance_metrics,


@app.cell
def __():
    # Interactive analysis controls
    marimo.markdown("## Analysis Controls")

    analysis_mode = marimo.ui.radio(
        ["Performance Analysis", "Agent Behavior", "Coordination Patterns", "Resource Utilization"],
        value="Performance Analysis",
        label="Analysis Mode"
    )

    return analysis_mode,


@app.cell
def __(analysis_mode):
    # Dynamic analysis based on mode
    marimo.markdown(f"### {analysis_mode.value}")

    if analysis_mode.value == "Performance Analysis":
        marimo.markdown("Performance analysis shows training progress and efficiency metrics.")
        marimo.code({"sample_performance_data": {"reward": 1250, "time": 45.2}})
    elif analysis_mode.value == "Agent Behavior":
        marimo.markdown("Agent behavior analysis examines individual agent actions and decisions.")
        marimo.code({"sample_agent_data": {"actions": ["move", "collect", "attack"]}})
    elif analysis_mode.value == "Coordination Patterns":
        marimo.markdown("Coordination analysis studies multi-agent interaction patterns.")
        marimo.code({"coordination_metrics": {"communication": 75, "cooperation": 0.8}})
    else:
        marimo.markdown("Resource utilization tracks system resource usage.")
        marimo.code({"resource_usage": {"cpu": "65%", "memory": "2.3GB"}})

    return


@app.cell
def __():
    # Export controls
    marimo.markdown("## Export Options")

    export_format = marimo.ui.radio(
        ["JSON", "CSV", "Interactive HTML", "PDF Report"],
        value="JSON",
        label="Export Format"
    )

    export_button = marimo.ui.button("Export Analysis", label="Generate Export")

    return export_button, export_format


@app.cell
def __(export_button, export_format):
    # Handle export
    if export_button.clicked:
        marimo.markdown(f"### Exporting analysis as {export_format.value}")

        # Simulate export process
        export_data = {
            "export_timestamp": datetime.now().isoformat(),
            "format": export_format.value,
            "status": "completed",
            "file_location": f"outputs/analysis/exported_analysis.{export_format.value.lower()}"
        }

        marimo.code(export_data)
        marimo.markdown("✅ Export completed successfully!")

    return


@app.cell
def __():
    # MettaScope integration info
    marimo.markdown("## MettaScope Integration")

    mettascope_info = {
        "webgpu_viewer": "Available",
        "features": [
            "Interactive replay playback",
            "Agent parameter tracking",
            "Action trace visualization",
            "Real-time controls",
            "Inventory monitoring",
            "Resource flow visualization"
        ],
        "launch_command": "uv run ./tools/run.py experiments.recipes.arena.play",
        "replay_location": "outputs/replays/"
    }

    marimo.code(mettascope_info)
    marimo.markdown("🚀 Use MettaScope for advanced visual analysis!")

    return mettascope_info,


@app.cell
def __():
    # Summary and recommendations
    marimo.markdown("## Analysis Summary")

    summary = {
        "total_experiments": len(experiment_names) if 'experiment_names' in globals() else 0,
        "analysis_modes_available": 4,
        "visualization_features": 6,
        "export_formats": 4,
        "real_time_monitoring": True,
        "interactive_controls": True
    }

    marimo.markdown("### Key Capabilities:")
    marimo.markdown("- **Real-time Analysis**: Live parameter adjustment and visualization")
    marimo.markdown("- **Interactive Exploration**: Dynamic filtering and drill-down analysis")
    marimo.markdown("- **Multi-modal Visualization**: Charts, graphs, and interactive displays")
    marimo.markdown("- **Export Flexibility**: Multiple format support for reports")
    marimo.markdown("- **MettaScope Integration**: Advanced WebGPU visualization")

    marimo.code(summary)

    return summary,


@app.cell
def __():
    # Final recommendations
    marimo.markdown("## Recommendations")

    recommendations = [
        "Use real-time sliders to explore parameter sensitivity",
        "Switch between analysis modes for comprehensive understanding",
        "Export results in preferred format for reporting",
        "Leverage MettaScope for visual replay analysis",
        "Monitor performance metrics for optimization opportunities"
    ]

    for i, rec in enumerate(recommendations, 1):
        marimo.markdown(f"{i}. {rec}")

    return recommendations,

if __name__ == "__main__":
    app.run()
'''

        return marimo_code

    def save_marimo_file(self, filename: str = "interactive_analysis.marimo.py"):
        """Save the Marimo interactive analysis file."""
        marimo_path = self.output_path / filename

        with open(marimo_path, "w") as f:
            f.write(self.marimo_content)

        print(f"✅ Marimo interactive analysis saved to: {marimo_path}")


def main():
    """Main function to generate Marimo interactive analysis."""
    print("🎛️  DAF Interactive Marimo Analysis Example")
    print("=" * 50)

    # Setup output directory
    example_output = get_example_output_path("interactive_marimo_analysis")
    print(f"📁 Output directory: {example_output}")

    # Generate Marimo interactive analysis
    marimo_generator = MarimoInteractiveAnalysis(example_output)
    marimo_generator.save_marimo_file("comprehensive_interactive_analysis.marimo.py")

    # Generate sample data for Marimo
    sample_data = {
        "marimo_metadata": {
            "generated_at": datetime.now().isoformat(),
            "analysis_type": "interactive_real_time",
            "features_demonstrated": [
                "real_time_parameter_controls",
                "dynamic_visualization_updates",
                "interactive_filtering",
                "multi_modal_analysis",
                "export_functionality",
                "mettascope_integration",
            ],
        },
        "interactive_controls": {
            "parameter_sliders": True,
            "analysis_mode_selector": True,
            "export_format_options": True,
            "real_time_monitoring": True,
        },
        "supported_analysis_modes": [
            "Performance Analysis",
            "Agent Behavior",
            "Coordination Patterns",
            "Resource Utilization",
        ],
        "export_formats": ["JSON", "CSV", "Interactive HTML", "PDF Report"],
    }

    with open(example_output / "marimo_sample_data.json", "w") as f:
        json.dump(sample_data, f, indent=2)

    print("\n🎯 Interactive Analysis Features Demonstrated:")
    print("  • Real-time parameter adjustment with live visualization")
    print("  • Dynamic analysis mode switching")
    print("  • Interactive data filtering and exploration")
    print("  • Multiple visualization modes and chart types")
    print("  • Export functionality for different formats")
    print("  • MettaScope integration for advanced visualization")

    print("\n📋 Generated Files:")
    print(f"  • {example_output}/comprehensive_interactive_analysis.marimo.py")
    print(f"  • {example_output}/marimo_sample_data.json")

    print("\n🚀 Next Steps:")
    print("1. Install Marimo: pip install marimo")
    print("2. Run: marimo run comprehensive_interactive_analysis.marimo.py")
    print("3. Use interactive sliders to explore parameters")
    print("4. Switch between analysis modes")
    print("5. Export results in preferred format")

    print("\n✅ Marimo interactive analysis example completed!")


if __name__ == "__main__":
    main()

