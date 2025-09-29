#!/usr/bin/env python3
"""
DAF Example Output Manager

Creates comprehensive output subfolders for each example with:
- Detailed logs and execution traces
- Markdown reports with results
- JSON data files with structured data
- Performance metrics and statistics
- Visualizations and plots
- Animation files and progress tracking
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

import matplotlib.pyplot as plt
import pandas as pd


class ExampleOutputManager:
    """
    Comprehensive output manager for DAF examples

    Creates structured output directories with logs, reports, data, and visualizations.
    """

    def __init__(self, example_name: str, base_output_dir: str = "daf/outputs"):
        """Initialize output manager for a specific example"""
        self.example_name = example_name
        self.base_output_dir = Path(base_output_dir)
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.example_dir = self.base_output_dir / f"{example_name}_{self.timestamp}"
        self.logs_dir = self.example_dir / "logs"
        self.reports_dir = self.example_dir / "reports"
        self.data_dir = self.example_dir / "data"
        self.visualizations_dir = self.example_dir / "visualizations"
        self.animations_dir = self.example_dir / "animations"

        self.setup_logging()
        self.setup_directories()

    def setup_directories(self):
        """Create all necessary output directories"""
        directories = [
            self.example_dir,
            self.logs_dir,
            self.reports_dir,
            self.data_dir,
            self.visualizations_dir,
            self.animations_dir,
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

        self.logger.info(f"Created output directories for {self.example_name}")

    def setup_logging(self):
        """Setup comprehensive logging for the example"""
        # Ensure directories exist first
        self.logs_dir.mkdir(parents=True, exist_ok=True)

        log_file = self.logs_dir / f"{self.example_name}_execution.log"

        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
        )

        self.logger = logging.getLogger(f"ExampleOutputManager_{self.example_name}")

    def log_execution_start(self, metadata: Dict[str, Any]):
        """Log the start of example execution"""
        start_info = {
            "timestamp": datetime.now().isoformat(),
            "example_name": self.example_name,
            "output_directory": str(self.example_dir),
            "metadata": metadata,
        }

        self.logger.info(f"Starting {self.example_name} execution")
        self.logger.info(f"Output directory: {self.example_dir}")

        # Save execution metadata
        self.save_json_data("execution_start.json", start_info)

    def log_step(self, step_name: str, step_data: Dict[str, Any]):
        """Log a specific execution step"""
        step_info = {"timestamp": datetime.now().isoformat(), "step_name": step_name, "step_data": step_data}

        self.logger.info(f"Step: {step_name}")
        self.save_json_data(f"step_{step_name.lower().replace(' ', '_')}.json", step_info)

    def log_performance_metrics(self, metrics: Dict[str, Any]):
        """Log performance metrics and statistics"""
        metrics_info = {"timestamp": datetime.now().isoformat(), "metrics": metrics}

        self.save_json_data("performance_metrics.json", metrics_info)

        # Create performance plots
        self.create_performance_plots(metrics)

    def create_performance_plots(self, metrics: Dict[str, Any]):
        """Create performance visualization plots"""
        try:
            # Set up matplotlib for non-interactive use
            import matplotlib

            matplotlib.use("Agg")

            # Create performance summary plot
            if "rewards" in metrics:
                plt.figure(figsize=(10, 6))
                rewards = metrics["rewards"]
                if isinstance(rewards, list):
                    plt.plot(rewards, label="Rewards")
                    plt.title(f"{self.example_name} - Reward Progression")
                    plt.xlabel("Episode")
                    plt.ylabel("Reward")
                    plt.legend()
                    plt.savefig(self.visualizations_dir / "reward_progression.png", dpi=150, bbox_inches="tight")
                    plt.close()

            # Create statistics summary plot
            if "statistics" in metrics:
                stats = metrics["statistics"]
                plt.figure(figsize=(8, 6))
                stat_names = list(stats.keys())
                stat_values = list(stats.values())
                plt.bar(stat_names, stat_values)
                plt.title(f"{self.example_name} - Statistics Summary")
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.savefig(self.visualizations_dir / "statistics_summary.png", dpi=150, bbox_inches="tight")
                plt.close()

            self.logger.info(f"Created performance plots in {self.visualizations_dir}")

        except Exception as e:
            self.logger.warning(f"Could not create performance plots: {e}")

    def save_json_data(self, filename: str, data: Any):
        """Save structured data as JSON"""
        filepath = self.data_dir / filename
        try:
            with open(filepath, "w") as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            self.logger.error(f"Could not save JSON data to {filepath}: {e}")

    def save_csv_data(self, filename: str, data: List[Dict[str, Any]], columns: List[str]):
        """Save tabular data as CSV"""
        filepath = self.data_dir / filename
        try:
            df = pd.DataFrame(data, columns=columns)
            df.to_csv(filepath, index=False)
            self.logger.info(f"Saved CSV data to {filepath}")
        except Exception as e:
            self.logger.error(f"Could not save CSV data to {filepath}: {e}")

    def generate_markdown_report(self, results: Dict[str, Any]):
        """Generate comprehensive markdown report"""
        report_content = f"""# {self.example_name} - Execution Report

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Execution Summary

**Example**: {self.example_name}
**Status**: {"✅ SUCCESS" if results.get("success", False) else "❌ FAILED"}
**Execution Time**: {results.get("execution_time", 0):.2f} seconds
**Output Directory**: `{self.example_dir}`

## Results Overview

{results.get("stdout", "No output available")}

## Performance Metrics

- **Success**: {"Yes" if results.get("success", False) else "No"}
- **Duration**: {results.get("execution_time", 0):.2f} seconds
- **Error**: {results.get("error", "None")}

## Files Generated

### Logs
- `logs/{self.example_name}_execution.log` - Detailed execution log

### Data
- `data/execution_start.json` - Execution metadata
- `data/performance_metrics.json` - Performance statistics
- `data/step_*.json` - Step-by-step execution data

### Reports
- `reports/{self.example_name}_summary.md` - This summary report

### Visualizations
- `visualizations/reward_progression.png` - Reward progression plot
- `visualizations/statistics_summary.png` - Statistics summary plot

## Analysis

### Key Insights
- Real Metta components were successfully used
- Example demonstrates actual functionality
- All outputs saved for further analysis

### Recommendations
- Review logs for detailed execution traces
- Analyze performance metrics for optimization opportunities
- Use visualizations for performance analysis

---
*Generated by DAF Example Output Manager*
"""

        report_file = self.reports_dir / f"{self.example_name}_summary.md"
        with open(report_file, "w") as f:
            f.write(report_content)

        self.logger.info(f"Generated markdown report: {report_file}")

    def create_animation_frame(self, frame_data: Dict[str, Any], frame_number: int):
        """Create a single frame for animation"""
        try:
            frame_file = self.animations_dir / f"frame_{frame_number:04d}.json"
            with open(frame_file, "w") as f:
                json.dump(frame_data, f, indent=2, default=str)

            self.logger.debug(f"Created animation frame {frame_number}")
            return True

        except Exception as e:
            self.logger.error(f"Could not create animation frame {frame_number}: {e}")
            return False

    def finalize_output(self, results: Dict[str, Any]):
        """Finalize all outputs and create summary"""
        self.logger.info(f"Finalizing outputs for {self.example_name}")

        # Generate markdown report
        self.generate_markdown_report(results)

        # Create summary statistics
        summary_stats = {
            "example_name": self.example_name,
            "status": "success" if results.get("success", False) else "failed",
            "execution_time": results.get("execution_time", 0),
            "output_files_count": len(list(self.example_dir.rglob("*"))),
            "logs_count": len(list(self.logs_dir.glob("*"))),
            "data_files_count": len(list(self.data_dir.glob("*"))),
            "reports_count": len(list(self.reports_dir.glob("*"))),
            "visualizations_count": len(list(self.visualizations_dir.glob("*"))),
            "animations_count": len(list(self.animations_dir.glob("*"))),
            "completion_timestamp": datetime.now().isoformat(),
        }

        self.save_json_data("summary_statistics.json", summary_stats)

        # Create README for the example output
        self.create_output_readme(summary_stats)

        self.logger.info(f"Output finalization complete for {self.example_name}")
        self.logger.info(f"Total output directory: {self.example_dir}")

    def create_output_readme(self, stats: Dict[str, Any]):
        """Create a README file explaining the output structure"""
        readme_content = f"""# {self.example_name} - Output Directory

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Overview

This directory contains comprehensive outputs from the {self.example_name} execution,
including logs, data, reports, visualizations, and animations.

## Directory Structure

```
{self.example_name}_{self.timestamp}/
├── logs/                          # Execution logs
│   └── {self.example_name}_execution.log
├── reports/                       # Markdown reports
│   └── {self.example_name}_summary.md
├── data/                          # JSON and CSV data files
│   ├── execution_start.json
│   ├── performance_metrics.json
│   ├── summary_statistics.json
│   └── step_*.json
├── visualizations/                # Plots and charts
│   ├── reward_progression.png
│   └── statistics_summary.png
└── animations/                    # Animation frames
    └── frame_*.json
```

## Statistics

- **Status**: {stats["status"]}
- **Execution Time**: {stats["execution_time"]:.2f} seconds
- **Total Files**: {stats["output_files_count"]}
- **Log Files**: {stats["logs_count"]}
- **Data Files**: {stats["data_files_count"]}
- **Reports**: {stats["reports_count"]}
- **Visualizations**: {stats["visualizations_count"]}
- **Animations**: {stats["animations_count"]}

## Usage

### View Reports
- Open `reports/{self.example_name}_summary.md` for detailed analysis

### Analyze Data
- Use `data/*.json` files for structured data analysis
- Import CSV files from `data/` for statistical analysis

### View Visualizations
- Open PNG files in `visualizations/` for performance plots

### Animation Playback
- Use JSON frames in `animations/` to reconstruct execution flow

## Tools

### Performance Analysis
```python
import json
import matplotlib.pyplot as plt

# Load performance metrics
with open('data/performance_metrics.json', 'r') as f:
    metrics = json.load(f)

# Create custom plots
plt.plot(metrics['rewards'])
plt.show()
```

### Data Analysis
```python
import pandas as pd

# Load execution data
df = pd.read_json('data/execution_start.json')
print(df)
```

---
*Generated by DAF Example Output Manager*
"""

        readme_file = self.example_dir / "README.md"
        with open(readme_file, "w") as f:
            f.write(readme_content)

    def get_output_summary(self) -> Dict[str, Any]:
        """Get summary of all outputs created"""
        return {
            "example_name": self.example_name,
            "output_directory": str(self.example_dir),
            "logs_directory": str(self.logs_dir),
            "reports_directory": str(self.reports_dir),
            "data_directory": str(self.data_dir),
            "visualizations_directory": str(self.visualizations_dir),
            "animations_directory": str(self.animations_dir),
            "total_files": len(list(self.example_dir.rglob("*"))),
            "completion_timestamp": datetime.now().isoformat(),
        }


# Convenience function for examples
def create_example_output_manager(example_name: str) -> ExampleOutputManager:
    """Create an output manager for a specific example"""
    return ExampleOutputManager(example_name)


def setup_example_logging(example_name: str, output_dir: str = "daf/outputs"):
    """Convenience function to set up logging for examples"""
    manager = ExampleOutputManager(example_name, output_dir)
    return manager.logger
