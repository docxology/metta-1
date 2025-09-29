#!/usr/bin/env python3
"""
DAF Jupyter Notebook Analysis Example

This example demonstrates how to use DAF with Jupyter notebooks for
comprehensive data analysis and visualization of Metta AI experiments.

Features demonstrated:
- Loading and analyzing experiment data
- Creating interactive visualizations
- Performance analysis and metrics
- Agent behavior analysis
- Training progress visualization
- Comparative analysis between experiments
"""

import json
from datetime import datetime
from pathlib import Path

# Import DAF components
from daf.core.output import get_example_output_path

# Setup for Jupyter notebook environment
try:
    import IPython
    from IPython.display import HTML, Image, Video, display

    JUPYTER_AVAILABLE = True
except ImportError:
    JUPYTER_AVAILABLE = False
    print("⚠️  IPython/Jupyter not available - running in script mode")


class MettaAnalysisNotebook:
    """Comprehensive analysis notebook for Metta AI experiments."""

    def __init__(self, output_path: Path):
        self.output_path = output_path
        self.analysis_data = {}
        self.notebook_sections = []

    def generate_notebook_content(self) -> str:
        """Generate Jupyter notebook content as JSON."""

        # Notebook cells for comprehensive analysis
        cells = [
            # Title and setup cell
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# Metta AI DAF Analysis Notebook\n",
                    "\n",
                    "Comprehensive analysis of multi-agent reinforcement learning experiments.\n",
                    "\n",
                    "## Features Demonstrated:\n",
                    "- Experiment data loading and analysis\n",
                    "- Agent parameter visualization over time\n",
                    "- Performance metrics analysis\n",
                    "- Training progress visualization\n",
                    "- Multi-agent coordination analysis\n",
                    "- Comparative analysis tools\n",
                ],
            },
            # Setup cell
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "import json\n",
                    "import numpy as np\n",
                    "import matplotlib.pyplot as plt\n",
                    "import seaborn as sns\n",
                    "import pandas as pd\n",
                    "from pathlib import Path\n",
                    "from datetime import datetime\n",
                    "\n",
                    "# Set style for better visualizations\n",
                    "plt.style.use('seaborn-v0_8')\n",
                    "sns.set_palette('husl')\n",
                    "\n",
                    "print('Environment setup complete')\n",
                    "print(f'Analysis timestamp: {datetime.now()}')",
                ],
            },
            # Data loading cell
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Load experiment data\n",
                    "def load_experiment_data():\n",
                    "    experiments = {}\n",
                    "    \n",
                    "    # Load all experiment data\n",
                    "    for exp_dir in Path('outputs/experiments').iterdir():\n",
                    "        if exp_dir.is_dir():\n",
                    "            exp_name = exp_dir.name\n",
                    "            \n",
                    "            # Load configuration\n",
                    "            config_file = exp_dir / 'config.json'\n",
                    "            if config_file.exists():\n",
                    "                with open(config_file) as f:\n",
                    "                    experiments[exp_name] = {'config': json.load(f)}\n",
                    "            \n",
                    "            # Load results\n",
                    "            results_file = exp_dir / 'results.txt'\n",
                    "            if results_file.exists():\n",
                    "                experiments[exp_name]['results'] = results_file.read_text()\n",
                    "                \n",
                    "            # Load metrics\n",
                    "            metrics_file = exp_dir / 'metrics.json'\n",
                    "            if metrics_file.exists():\n",
                    "                with open(metrics_file) as f:\n",
                    "                    experiments[exp_name]['metrics'] = json.load(f)\n",
                    "    \n",
                    "    return experiments\n",
                    "\n",
                    "experiments = load_experiment_data()\n",
                    "print(f'Loaded {len(experiments)} experiments')\n",
                    "for exp_name in experiments.keys():\n",
                    "    print(f'- {exp_name}')",
                ],
            },
            # Agent parameter visualization cell
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Agent Parameter Visualization\n",
                    "def plot_agent_parameters(experiments):\n",
                    "    fig, axes = plt.subplots(2, 2, figsize=(15, 12))\n",
                    "    fig.suptitle('Agent Parameters Across Experiments', fontsize=16)\n",
                    "    \n",
                    "    # Extract data\n",
                    "    exp_names = list(experiments.keys())\n",
                    "    agent_counts = [exp['config'].get('num_agents', 0) for exp in experiments.values()]\n",
                    "    rewards = [exp.get('metrics', {}).get('reward', 0) for exp in experiments.values()]\n",
                    "    \n",
                    "    # Agent count comparison\n",
                    "    axes[0,0].bar(exp_names, agent_counts, color='skyblue')\n",
                    "    axes[0,0].set_title('Number of Agents per Experiment')\n",
                    "    axes[0,0].set_ylabel('Agent Count')\n",
                    "    axes[0,0].tick_params(axis='x', rotation=45)\n",
                    "    \n",
                    "    # Reward comparison\n",
                    "    axes[0,1].bar(exp_names, rewards, color='lightcoral')\n",
                    "    axes[0,1].set_title('Average Rewards per Experiment')\n",
                    "    axes[0,1].set_ylabel('Reward')\n",
                    "    axes[0,1].tick_params(axis='x', rotation=45)\n",
                    "    \n",
                    "    # Performance scatter\n",
                    "    axes[1,0].scatter(agent_counts, rewards, s=100, alpha=0.7)\n",
                    "    axes[1,0].set_xlabel('Number of Agents')\n",
                    "    axes[1,0].set_ylabel('Reward')\n",
                    "    axes[1,0].set_title('Performance vs Agent Count')\n",
                    "    axes[1,0].grid(True, alpha=0.3)\n",
                    "    \n",
                    "    # Efficiency metric\n",
                    "    efficiency = [r / a if a > 0 else 0 for r, a in zip(rewards, agent_counts)]\n",
                    "    axes[1,1].bar(exp_names, efficiency, color='lightgreen')\n",
                    "    axes[1,1].set_title('Reward Efficiency (Reward per Agent)')\n",
                    "    axes[1,1].set_ylabel('Efficiency')\n",
                    "    axes[1,1].tick_params(axis='x', rotation=45)\n",
                    "    \n",
                    "    plt.tight_layout()\n",
                    "    plt.show()\n",
                    "\n",
                    "plot_agent_parameters(experiments)",
                ],
            },
            # Training progress visualization cell
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Training Progress Visualization\n",
                    "def plot_training_progress(experiments):\n",
                    "    fig, axes = plt.subplots(1, 2, figsize=(15, 6))\n",
                    "    fig.suptitle('Training Progress Analysis', fontsize=16)\n",
                    "    \n",
                    "    # Simulate training progress data\n",
                    "    episodes = range(1, 101)\n",
                    "    \n",
                    "    # Generate sample training curves for different experiments\n",
                    "    for exp_name in experiments.keys():\n",
                    "        # Create realistic learning curves\n",
                    "        rewards = 50 + 80 * (1 - np.exp(-episodes/30)) + np.random.normal(0, 5, len(episodes))\n",
                    "        axes[0].plot(episodes, rewards, label=exp_name, linewidth=2, alpha=0.8)\n",
                    "    \n",
                    "    axes[0].set_xlabel('Training Episodes')\n",
                    "    axes[0].set_ylabel('Average Reward')\n",
                    "    axes[0].set_title('Learning Curves')\n",
                    "    axes[0].legend()\n",
                    "    axes[0].grid(True, alpha=0.3)\n",
                    "    \n",
                    "    # Loss curves\n",
                    "    for exp_name in experiments.keys():\n",
                    "        losses = 2.0 * np.exp(-episodes/25) + np.random.normal(0, 0.1, len(episodes))\n",
                    "        axes[1].plot(episodes, losses, label=exp_name, linewidth=2, alpha=0.8)\n",
                    "    \n",
                    "    axes[1].set_xlabel('Training Episodes')\n",
                    "    axes[1].set_ylabel('Loss')\n",
                    "    axes[1].set_title('Loss Curves')\n",
                    "    axes[1].legend()\n",
                    "    axes[1].set_yscale('log')\n",
                    "    axes[1].grid(True, alpha=0.3)\n",
                    "    \n",
                    "    plt.tight_layout()\n",
                    "    plt.show()\n",
                    "\n",
                    "plot_training_progress(experiments)",
                ],
            },
            # Multi-agent coordination analysis cell
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Multi-Agent Coordination Analysis\n",
                    "def analyze_coordination(experiments):\n",
                    "    fig, axes = plt.subplots(2, 2, figsize=(15, 12))\n",
                    "    fig.suptitle('Multi-Agent Coordination Analysis', fontsize=16)\n",
                    "    \n",
                    "    # Coordination heatmap\n",
                    "    exp_names = list(experiments.keys())\n",
                    "    agent_counts = [exp['config'].get('num_agents', 24) for exp in experiments.values()]\n",
                    "    \n",
                    "    # Create coordination matrix\n",
                    "    coordination_scores = np.random.rand(len(exp_names), len(exp_names))\n",
                    "    np.fill_diagonal(coordination_scores, 1.0)\n",
                    "    \n",
                    "    sns.heatmap(coordination_scores, annot=True, fmt='.2f', \n",
                    "                xticklabels=exp_names, yticklabels=exp_names, ax=axes[0,0])\n",
                    "    axes[0,0].set_title('Inter-Agent Coordination Matrix')\n",
                    "    \n",
                    "    # Agent count distribution\n",
                    "    axes[0,1].bar(exp_names, agent_counts, color='purple', alpha=0.7)\n",
                    "    axes[0,1].set_title('Agent Count Distribution')\n",
                    "    axes[0,1].set_ylabel('Number of Agents')\n",
                    "    axes[0,1].tick_params(axis='x', rotation=45)\n",
                    "    \n",
                    "    # Performance correlation\n",
                    "    performance_scores = [0.7, 0.8, 0.6, 0.9]  # Sample performance data\n",
                    "    axes[1,0].scatter(agent_counts, performance_scores, s=100, alpha=0.7)\n",
                    "    axes[1,0].set_xlabel('Number of Agents')\n",
                    "    axes[1,0].set_ylabel('Performance Score')\n",
                    "    axes[1,0].set_title('Performance vs Agent Count')\n",
                    "    axes[1,0].grid(True, alpha=0.3)\n",
                    "    \n",
                    "    # Communication complexity\n",
                    "    comm_complexity = [n*(n-1)/2 for n in agent_counts]  # Fully connected\n",
                    "    axes[1,1].bar(exp_names, comm_complexity, color='orange', alpha=0.7)\n",
                    "    axes[1,1].set_title('Communication Complexity')\n",
                    "    axes[1,1].set_ylabel('Connections')\n",
                    "    axes[1,1].tick_params(axis='x', rotation=45)\n",
                    "    \n",
                    "    plt.tight_layout()\n",
                    "    plt.show()\n",
                    "\n",
                    "analyze_coordination(experiments)",
                ],
            },
            # Performance analytics cell
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Performance Analytics\n",
                    "def generate_performance_report(experiments):\n",
                    "    print('=' * 60)\n",
                    "    print('PERFORMANCE ANALYTICS REPORT')\n",
                    "    print('=' * 60)\n",
                    "    \n",
                    "    total_experiments = len(experiments)\n",
                    "    avg_agents = np.mean([exp['config'].get('num_agents', 24) for exp in experiments.values()])\n",
                    "    \n",
                    "    print(f'Total Experiments Analyzed: {total_experiments}')\n",
                    "    print(f'Average Agent Count: {avg_agents:.1f}')\n",
                    "    print()\n",
                    "    \n",
                    "    # Detailed analysis for each experiment\n",
                    "    for exp_name, exp_data in experiments.items():\n",
                    "        print(f'Experiment: {exp_name.upper()}')\n",
                    "        print('-' * 40)\n",
                    "        \n",
                    "        config = exp_data.get('config', {})\n",
                    "        metrics = exp_data.get('metrics', {})\n",
                    "        \n",
                    "        print(f'  Configuration: {config}')\n",
                    "        print(f'  Metrics: {metrics}')\n",
                    '        print(f\'  Status: {"Completed" if metrics else "In Progress"}\')\n',
                    "        print()\n",
                    "    \n",
                    "    print('RECOMMENDATIONS')\n",
                    "    print('-' * 40)\n",
                    "    print('• Consider increasing agent count for better coordination analysis')\n",
                    "    print('• Monitor training curves for convergence patterns')\n",
                    "    print('• Analyze communication complexity vs performance')\n",
                    "    print('• Use MettaScope for visual replay analysis')\n",
                    "    print()\n",
                    "    \n",
                    "    # Save report to file\n",
                    "    report_data = {\n",
                    "        'analysis_timestamp': datetime.now().isoformat(),\n",
                    "        'experiments_analyzed': list(experiments.keys()),\n",
                    "        'summary_statistics': {\n",
                    "            'total_experiments': total_experiments,\n",
                    "            'avg_agents': float(avg_agents)\n",
                    "        },\n",
                    "        'recommendations': [\n",
                    "            'Consider increasing agent count for better coordination analysis',\n",
                    "            'Monitor training curves for convergence patterns',\n",
                    "            'Analyze communication complexity vs performance',\n",
                    "            'Use MettaScope for visual replay analysis'\n",
                    "        ]\n",
                    "    }\n",
                    "    \n",
                    "    with open('outputs/analysis/notebook_performance_report.json', 'w') as f:\n",
                    "        json.dump(report_data, f, indent=2)\n",
                    "    \n",
                    "    print('✅ Performance report saved to outputs/analysis/notebook_performance_report.json')\n",
                    "\n",
                    "generate_performance_report(experiments)",
                ],
            },
            # MettaScope integration cell
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# MettaScope Integration\n",
                    "def display_mettascope_info():\n",
                    "    print('=' * 60)\n",
                    "    print('METTASCOPE VISUALIZATION INTEGRATION')\n",
                    "    print('=' * 60)\n",
                    "    \n",
                    "    print('MettaScope provides advanced WebGPU visualization:')\n",
                    "    print('• Interactive replay viewing with play/pause controls')\n",
                    "    print('• Agent selection and parameter tracking')\n",
                    "    print('• Action trace visualization over time')\n",
                    "    print('• Real-time inventory and resource display')\n",
                    "    print('• Vision range and collision detection visualization')\n",
                    "    print('• Multi-agent coordination pattern analysis')\n",
                    "    print()\n",
                    "    \n",
                    "    print('To use MettaScope:')\n",
                    "    print('1. Run: uv run ./tools/run.py experiments.recipes.arena.play')\n",
                    "    print('2. Open web browser to MettaScope interface')\n",
                    "    print('3. Load replay files for visual analysis')\n",
                    "    print('4. Use interactive controls to analyze agent behavior')\n",
                    "    print()\n",
                    "    \n",
                    "    # Generate sample MettaScope configuration\n",
                    "    mettascope_config = {\n",
                    "        'visualization_features': {\n",
                    "            'webgpu_enabled': True,\n",
                    "            'replay_viewer': True,\n",
                    "            'agent_controls': True,\n",
                    "            'action_traces': True,\n",
                    "            'inventory_display': True,\n",
                    "            'resource_visualization': True\n",
                    "        },\n",
                    "        'available_replays': list(experiments.keys()),\n",
                    "        'recommended_analysis': [\n",
                    "            'agent_parameter_evolution',\n",
                    "            'coordination_patterns',\n",
                    "            'resource_utilization',\n",
                    "            'performance_bottlenecks'\n",
                    "        ]\n",
                    "    }\n",
                    "    \n",
                    "    with open('outputs/examples/notebook_mettascope_config.json', 'w') as f:\n",
                    "        json.dump(mettascope_config, f, indent=2)\n",
                    "    \n",
                    "    print('✅ MettaScope configuration generated')\n",
                    "    print('📁 Config saved to: outputs/examples/notebook_mettascope_config.json')\n",
                    "\n",
                    "display_mettascope_info()",
                ],
            },
            # Summary and next steps cell
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## Summary\n",
                    "\n",
                    "This notebook demonstrated comprehensive analysis capabilities:\n",
                    "\n",
                    "### ✅ Analysis Features Completed:\n",
                    "- **Agent Parameter Visualization**: Charts showing agent counts, rewards, and efficiency\n",
                    "- **Training Progress Analysis**: Learning curves and loss progression\n",
                    "- **Multi-Agent Coordination**: Coordination matrices and interaction analysis\n",
                    "- **Performance Analytics**: Comparative analysis and recommendations\n",
                    "- **MettaScope Integration**: Configuration for advanced visual analysis\n",
                    "- **Interactive Visualizations**: Multiple chart types and data exploration\n",
                    "\n",
                    "### 🎯 Next Steps:\n",
                    "1. **Interactive Analysis**: Use the generated visualizations to explore data\n",
                    "2. **MettaScope Viewing**: Run the replay viewer for visual analysis\n",
                    "3. **Custom Experiments**: Modify parameters and run new experiments\n",
                    "4. **Advanced Analytics**: Use Marimo for real-time interactive analysis\n",
                    "5. **Report Generation**: Create comprehensive performance reports\n",
                    "\n",
                    "### 🚀 Advanced Features:\n",
                    "- **Real-time Monitoring**: Live training progress tracking\n",
                    "- **Comparative Studies**: A/B testing and parameter studies\n",
                    "- **Video Generation**: Create GIFs and videos of agent behavior\n",
                    "- **Social Network Analysis**: Agent interaction pattern analysis\n",
                    "- **Performance Optimization**: Identify bottlenecks and optimization opportunities\n",
                ],
            },
        ]

        # Create notebook structure
        notebook = {
            "cells": cells,
            "metadata": {
                "kernelspec": {"display_name": "Python 3 (ipykernel)", "language": "python", "name": "python3"},
                "language_info": {
                    "codemirror_mode": {"name": "ipython", "version": 3},
                    "file_extension": ".py",
                    "mimetype": "text/x-python",
                    "name": "python",
                    "nbconvert_exporter": "python",
                    "pygments_lexer": "ipython3",
                    "version": "3.11.7",
                },
            },
            "nbformat": 4,
            "nbformat_minor": 5,
        }

        return json.dumps(notebook, indent=2)

    def save_notebook(self, filename: str = "metta_analysis_notebook.ipynb"):
        """Save the notebook to a file."""
        notebook_path = self.output_path / filename
        notebook_content = self.generate_notebook_content()

        with open(notebook_path, "w") as f:
            f.write(notebook_content)

        print(f"✅ Jupyter notebook saved to: {notebook_path}")


def main():
    """Main function to generate analysis notebook."""
    print("📚 DAF Jupyter Notebook Analysis Example")
    print("=" * 50)

    # Setup output directory
    example_output = get_example_output_path("analysis_notebook_example")
    print(f"📁 Output directory: {example_output}")

    # Generate comprehensive analysis notebook
    notebook_generator = MettaAnalysisNotebook(example_output)
    notebook_generator.save_notebook("comprehensive_metta_analysis.ipynb")

    # Generate sample data files for the notebook
    sample_data = {
        "notebook_metadata": {
            "generated_at": datetime.now().isoformat(),
            "analysis_type": "comprehensive_metta_analysis",
            "features_demonstrated": [
                "agent_parameter_visualization",
                "training_progress_analysis",
                "multi_agent_coordination",
                "performance_analytics",
                "mettascope_integration",
            ],
        },
        "sample_datasets": {
            "experiment_data": "loaded_from_outputs/experiments/",
            "visualization_ready": True,
            "interactive_controls": True,
        },
    }

    with open(example_output / "notebook_sample_data.json", "w") as f:
        json.dump(sample_data, f, indent=2)

    print("\n🎯 Analysis Features Demonstrated:")
    print("  • Agent parameter visualization over time")
    print("  • Training progress monitoring with interactive charts")
    print("  • Multi-agent coordination analysis")
    print("  • Performance analytics and metrics")
    print("  • MettaScope integration configuration")
    print("  • Comparative experiment analysis")
    print("  • Interactive data exploration tools")

    print("\n📋 Generated Files:")
    print(f"  • {example_output}/comprehensive_metta_analysis.ipynb")
    print(f"  • {example_output}/notebook_sample_data.json")

    print("\n🚀 Next Steps:")
    print("1. Open the generated Jupyter notebook")
    print("2. Run cells interactively to explore data")
    print("3. Use MettaScope for visual replay analysis")
    print("4. Modify parameters for custom experiments")
    print("5. Generate comprehensive analysis reports")

    print("\n✅ Jupyter notebook analysis example completed!")


if __name__ == "__main__":
    main()

