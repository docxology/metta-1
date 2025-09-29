#!/usr/bin/env python3
"""
Visualization Generator

Generates comprehensive visualizations from training data, statistics, and replay files.
"""

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

import matplotlib

matplotlib.use("Agg")  # Non-interactive backend
import matplotlib.pyplot as plt
import numpy as np

logger = logging.getLogger(__name__)


class VisualizationGenerator:
    """Generate visualizations from training and evaluation data."""

    def __init__(self, output_dir: Optional[Path] = None):
        """
        Initialize visualization generator.

        Args:
            output_dir: Directory to save visualizations
        """
        self.output_dir = output_dir or Path("@outputs/visualizations")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Visualization output directory: {self.output_dir}")

    def generate_training_curves(
        self, metrics: Dict[str, List[float]], output_name: str = "training_curves.png"
    ) -> Path:
        """
        Generate training curves plot.

        Args:
            metrics: Dictionary of metric names to values
            output_name: Output filename

        Returns:
            Path to generated plot
        """
        logger.info("Generating training curves...")

        output_path = self.output_dir / output_name

        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle("Training Progress", fontsize=16, fontweight="bold")

        # Plot each metric
        metric_names = list(metrics.keys())
        for idx, (ax, metric_name) in enumerate(zip(axes.flat, metric_names, strict=False)):
            if idx >= len(metric_names):
                ax.axis("off")
                continue

            values = metrics[metric_name]
            ax.plot(values, linewidth=2)
            ax.set_title(metric_name.replace("_", " ").title())
            ax.set_xlabel("Episode" if len(values) < 1000 else "Step")
            ax.set_ylabel("Value")
            ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close()

        logger.info(f"✅ Training curves saved: {output_path}")
        return output_path

    def generate_reward_distribution(self, rewards: List[float], output_name: str = "reward_distribution.png") -> Path:
        """
        Generate reward distribution histogram.

        Args:
            rewards: List of reward values
            output_name: Output filename

        Returns:
            Path to generated plot
        """
        logger.info("Generating reward distribution...")

        output_path = self.output_dir / output_name

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
        fig.suptitle("Reward Distribution Analysis", fontsize=16, fontweight="bold")

        # Histogram
        ax1.hist(rewards, bins=50, alpha=0.7, edgecolor="black")
        ax1.axvline(np.mean(rewards), color="red", linestyle="--", linewidth=2, label=f"Mean: {np.mean(rewards):.2f}")
        ax1.axvline(
            np.median(rewards), color="green", linestyle="--", linewidth=2, label=f"Median: {np.median(rewards):.2f}"
        )
        ax1.set_xlabel("Reward")
        ax1.set_ylabel("Frequency")
        ax1.set_title("Reward Histogram")
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # Box plot
        ax2.boxplot(rewards, vert=True)
        ax2.set_ylabel("Reward")
        ax2.set_title("Reward Box Plot")
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close()

        logger.info(f"✅ Reward distribution saved: {output_path}")
        return output_path

    def generate_performance_comparison(
        self, scenarios: List[Dict[str, Any]], output_name: str = "performance_comparison.png"
    ) -> Path:
        """
        Generate performance comparison across scenarios.

        Args:
            scenarios: List of scenario results
            output_name: Output filename

        Returns:
            Path to generated plot
        """
        logger.info("Generating performance comparison...")

        output_path = self.output_dir / output_name

        scenario_names = [s.get("name", f"Scenario {i}") for i, s in enumerate(scenarios)]
        avg_rewards = [s.get("avg_reward", 0) for s in scenarios]
        success_rates = [s.get("success_rate", 0) for s in scenarios]

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
        fig.suptitle("Performance Comparison Across Scenarios", fontsize=16, fontweight="bold")

        # Average rewards
        bars1 = ax1.bar(range(len(scenario_names)), avg_rewards, alpha=0.7, edgecolor="black")
        ax1.set_xticks(range(len(scenario_names)))
        ax1.set_xticklabels(scenario_names, rotation=45, ha="right")
        ax1.set_ylabel("Average Reward")
        ax1.set_title("Average Reward by Scenario")
        ax1.grid(True, alpha=0.3, axis="y")

        # Color bars by value
        colors = plt.cm.RdYlGn(
            np.array(avg_rewards) / max(avg_rewards) if max(avg_rewards) > 0 else [0.5] * len(avg_rewards)
        )
        for bar, color in zip(bars1, colors, strict=False):
            bar.set_color(color)

        # Success rates
        bars2 = ax2.bar(range(len(scenario_names)), success_rates, alpha=0.7, edgecolor="black")
        ax2.set_xticks(range(len(scenario_names)))
        ax2.set_xticklabels(scenario_names, rotation=45, ha="right")
        ax2.set_ylabel("Success Rate")
        ax2.set_title("Success Rate by Scenario")
        ax2.set_ylim([0, 1.0])
        ax2.grid(True, alpha=0.3, axis="y")

        # Color bars by value
        colors = plt.cm.RdYlGn(success_rates)
        for bar, color in zip(bars2, colors, strict=False):
            bar.set_color(color)

        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close()

        logger.info(f"✅ Performance comparison saved: {output_path}")
        return output_path

    def generate_heatmap(
        self, data: np.ndarray, title: str = "Heatmap", output_name: str = "heatmap.png", labels: Optional[tuple] = None
    ) -> Path:
        """
        Generate a heatmap visualization.

        Args:
            data: 2D numpy array
            title: Plot title
            output_name: Output filename
            labels: Optional tuple of (x_labels, y_labels)

        Returns:
            Path to generated plot
        """
        logger.info(f"Generating heatmap: {title}")

        output_path = self.output_dir / output_name

        fig, ax = plt.subplots(figsize=(10, 8))

        im = ax.imshow(data, cmap="viridis", aspect="auto")
        ax.set_title(title, fontsize=14, fontweight="bold")

        if labels:
            x_labels, y_labels = labels
            if x_labels:
                ax.set_xticks(range(len(x_labels)))
                ax.set_xticklabels(x_labels, rotation=45, ha="right")
            if y_labels:
                ax.set_yticks(range(len(y_labels)))
                ax.set_yticklabels(y_labels)

        plt.colorbar(im, ax=ax)
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close()

        logger.info(f"✅ Heatmap saved: {output_path}")
        return output_path

    def generate_summary_dashboard(
        self, training_results: Dict[str, Any], output_name: str = "summary_dashboard.png"
    ) -> Path:
        """
        Generate a comprehensive summary dashboard.

        Args:
            training_results: Complete training results
            output_name: Output filename

        Returns:
            Path to generated plot
        """
        logger.info("Generating summary dashboard...")

        output_path = self.output_dir / output_name

        fig = plt.figure(figsize=(18, 12))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

        fig.suptitle(
            f"Training Summary: {training_results.get('experiment_name', 'Unknown')}", fontsize=18, fontweight="bold"
        )

        # Extract metrics
        scenario_results = training_results.get("scenario_results", [])
        if scenario_results:
            rewards = [s.get("avg_reward", 0) for s in scenario_results]
            success_rates = [s.get("success_rate", 0) for s in scenario_results]
            episode_lengths = [s.get("avg_length", 0) for s in scenario_results]

            # Plot 1: Reward progression
            ax1 = fig.add_subplot(gs[0, :2])
            ax1.plot(rewards, marker="o", linewidth=2, markersize=8)
            ax1.set_title("Average Reward Progression", fontweight="bold")
            ax1.set_xlabel("Scenario")
            ax1.set_ylabel("Average Reward")
            ax1.grid(True, alpha=0.3)

            # Plot 2: Success rates
            ax2 = fig.add_subplot(gs[0, 2])
            ax2.bar(range(len(success_rates)), success_rates, alpha=0.7)
            ax2.set_title("Success Rates", fontweight="bold")
            ax2.set_xlabel("Scenario")
            ax2.set_ylabel("Success Rate")
            ax2.set_ylim([0, 1])
            ax2.grid(True, alpha=0.3, axis="y")

            # Plot 3: Episode lengths
            ax3 = fig.add_subplot(gs[1, :])
            ax3.plot(episode_lengths, marker="s", linewidth=2, markersize=8, color="green")
            ax3.set_title("Average Episode Length", fontweight="bold")
            ax3.set_xlabel("Scenario")
            ax3.set_ylabel("Steps")
            ax3.grid(True, alpha=0.3)

            # Plot 4: Statistics summary
            ax4 = fig.add_subplot(gs[2, :])
            ax4.axis("off")

            stats_text = f"""
Training Statistics:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Total Scenarios: {len(scenario_results)}
• Average Reward: {np.mean(rewards):.3f} ± {np.std(rewards):.3f}
• Average Success Rate: {np.mean(success_rates):.2%}
• Average Episode Length: {np.mean(episode_lengths):.1f} steps
• Best Scenario: {scenario_results[np.argmax(rewards)].get("name", "Unknown")}
• Overall Improvement: {"✅ Yes" if rewards[-1] > rewards[0] else "⚠️ Limited"}
            """

            ax4.text(
                0.1,
                0.5,
                stats_text,
                fontsize=12,
                verticalalignment="center",
                family="monospace",
                bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.3),
            )

        plt.savefig(output_path, dpi=150, bbox_inches="tight")
        plt.close()

        logger.info(f"✅ Summary dashboard saved: {output_path}")
        return output_path


def main():
    """Example usage."""
    generator = VisualizationGenerator()

    # Example: Generate training curves
    example_metrics = {
        "reward": np.cumsum(np.random.randn(100) * 0.1 + 0.5).tolist(),
        "success_rate": (np.random.rand(100) * 0.3 + 0.4).tolist(),
        "episode_length": (150 + np.random.randn(100) * 20).tolist(),
        "policy_entropy": (1.5 - np.arange(100) * 0.01).tolist(),
    }

    generator.generate_training_curves(example_metrics)

    logger.info("✅ Example visualizations generated")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
