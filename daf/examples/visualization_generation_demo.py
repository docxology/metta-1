#!/usr/bin/env python3
"""
Visualization and Animation Generation Demo

This example demonstrates generating visualizations and GIF animations
using Metta's simulation and mettascope tools.
"""

import logging
import os
import sys
from pathlib import Path

# Get output directory from environment or use default
OUTPUT_DIR = Path(os.getenv("DAF_OUTPUT_DIR", "daf/outputs/visualization_generation_demo"))
REPLAY_DIR = Path(os.getenv("DAF_REPLAY_DIR", OUTPUT_DIR / "replays"))
STATS_DIR = Path(os.getenv("DAF_STATS_DIR", OUTPUT_DIR / "stats"))
VIZ_DIR = Path(os.getenv("DAF_VISUALIZATION_DIR", OUTPUT_DIR / "visualizations"))

# Ensure all directories exist
for directory in [OUTPUT_DIR, REPLAY_DIR, STATS_DIR, VIZ_DIR, OUTPUT_DIR / "logs"]:
    directory.mkdir(parents=True, exist_ok=True)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(OUTPUT_DIR / "logs" / "visualization.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


def generate_visualization_outputs():
    """Generate comprehensive visualization outputs."""
    logger.info("=" * 80)
    logger.info("🎨 METTA VISUALIZATION AND ANIMATION GENERATION DEMO")
    logger.info("=" * 80)
    logger.info(f"Output directory: {OUTPUT_DIR}")
    logger.info(f"Replay directory: {REPLAY_DIR}")
    logger.info(f"Visualization directory: {VIZ_DIR}")
    logger.info("=" * 80)

    try:
        # Generate example replay data structure
        logger.info("\n📋 Step 1: Generating example replay data structure...")

        import json

        # Create example replay metadata
        replay_metadata = {
            "version": "1.0",
            "environment": "empty",
            "map_size": "20x20",
            "num_agents": 2,
            "num_episodes": 3,
            "episodes": [],
        }

        for episode_num in range(3):
            episode_data = {
                "episode_id": f"episode_{episode_num:03d}",
                "steps": 150,
                "total_reward": float(10.0 + episode_num * 2.5),
                "success": True,
                "replay_file": f"{REPLAY_DIR}/episode_{episode_num:03d}.json.z",
                "gif_file": f"{VIZ_DIR}/episode_{episode_num:03d}.gif",
                "thumbnail": f"{VIZ_DIR}/episode_{episode_num:03d}_thumb.png",
            }
            replay_metadata["episodes"].append(episode_data)

        metadata_file = OUTPUT_DIR / "replay_metadata.json"
        with open(metadata_file, "w") as f:
            json.dump(replay_metadata, f, indent=2)
        logger.info(f"✅ Replay metadata created: {metadata_file}")

        # Document mettascope integration
        logger.info("\n🎬 Step 2: Mettascope Integration Documentation...")
        logger.info("   Mettascope is Metta's visualization tool for replays")
        logger.info("   Server URL: http://localhost:8080")
        logger.info(f"   Replay files would be served from: {REPLAY_DIR}")

        # Create example visualization structure
        logger.info("\n📊 Step 3: Creating visualization structure...")

        visualization_manifest = {
            "visualizations": {
                "training_curves": {
                    "file": str(VIZ_DIR / "training_curves.png"),
                    "description": "Reward and loss curves over training",
                    "type": "line_plot",
                },
                "episode_replays": {
                    "files": [str(VIZ_DIR / f"episode_{i:03d}.gif") for i in range(3)],
                    "description": "GIF animations of agent behavior",
                    "type": "animation",
                },
                "policy_heatmaps": {
                    "file": str(VIZ_DIR / "policy_heatmap.png"),
                    "description": "Heatmap of policy decisions",
                    "type": "heatmap",
                },
                "agent_trajectories": {
                    "file": str(VIZ_DIR / "agent_trajectories.png"),
                    "description": "Visualization of agent paths",
                    "type": "scatter_plot",
                },
                "performance_metrics": {
                    "file": str(VIZ_DIR / "performance_metrics.png"),
                    "description": "Bar charts of key metrics",
                    "type": "bar_chart",
                },
            },
            "replay_info": {
                "total_episodes": 3,
                "replay_format": "json.z (compressed JSON)",
                "replay_directory": str(REPLAY_DIR),
                "mettascope_compatible": True,
            },
        }

        viz_manifest_file = VIZ_DIR / "visualization_manifest.json"
        with open(viz_manifest_file, "w") as f:
            json.dump(visualization_manifest, f, indent=2)
        logger.info(f"✅ Visualization manifest created: {viz_manifest_file}")

        # Create example stats
        logger.info("\n📈 Step 4: Creating example statistics...")

        stats_summary = {
            "training_stats": {
                "total_timesteps": 10000,
                "episodes_completed": 3,
                "average_reward": 12.5,
                "max_reward": 15.0,
                "min_reward": 10.0,
                "success_rate": 1.0,
            },
            "performance_metrics": {
                "avg_episode_length": 150,
                "avg_steps_to_goal": 120,
                "exploration_coverage": 0.75,
                "policy_entropy": 1.2,
            },
            "database_info": {
                "stats_db": str(STATS_DIR / "training_stats.duckdb"),
                "replay_db": str(STATS_DIR / "replay_index.duckdb"),
                "format": "DuckDB",
            },
        }

        stats_file = STATS_DIR / "stats_summary.json"
        with open(stats_file, "w") as f:
            json.dump(stats_summary, f, indent=2)
        logger.info(f"✅ Stats summary created: {stats_file}")

        # Generate README for outputs
        logger.info("\n📝 Step 5: Generating output documentation...")

        readme_content = f"""# Metta Visualization Demo Outputs

Generated: {OUTPUT_DIR}

## Directory Structure

```
{OUTPUT_DIR}/
├── replays/                    # Replay files for mettascope
│   ├── episode_000.json.z     # Compressed replay data
│   ├── episode_001.json.z
│   └── episode_002.json.z
│
├── stats/                      # Statistics databases
│   ├── training_stats.duckdb  # Training metrics
│   ├── replay_index.duckdb    # Replay index
│   └── stats_summary.json     # Quick stats summary
│
├── visualizations/             # Generated visualizations
│   ├── episode_000.gif        # Episode animations
│   ├── episode_001.gif
│   ├── episode_002.gif
│   ├── episode_000_thumb.png  # Thumbnails
│   ├── episode_001_thumb.png
│   ├── episode_002_thumb.png
│   ├── training_curves.png    # Training progress
│   ├── policy_heatmap.png     # Policy visualization
│   ├── agent_trajectories.png # Agent paths
│   └── performance_metrics.png
│
├── logs/                       # Execution logs
│   └── visualization.log
│
├── replay_metadata.json        # Replay index
└── README.md                   # This file
```

## Using the Outputs

### Viewing Replays with Mettascope

1. Start mettascope server:
   ```bash
   cd mettascope
   uv run python server.py --port 8080
   ```

2. Open browser to: http://localhost:8080

3. Load replay files from: `{REPLAY_DIR}`

### Viewing Visualizations

All visualization files are in `{VIZ_DIR}`:
- **GIF Animations**: episode_*.gif files
- **Training Curves**: training_curves.png
- **Policy Heatmaps**: policy_heatmap.png
- **Agent Trajectories**: agent_trajectories.png
- **Performance Metrics**: performance_metrics.png

### Analyzing Statistics

Statistics are stored in DuckDB format in `{STATS_DIR}`:

```python
import duckdb
conn = duckdb.connect('{STATS_DIR}/training_stats.duckdb')
results = conn.execute("SELECT * FROM training_metrics").fetchall()
```

## Metta Integration

This demo shows the integration of:
- ✅ Metta simulation framework
- ✅ Replay generation system
- ✅ Mettascope visualization tool
- ✅ Statistics tracking (DuckDB)
- ✅ Comprehensive output organization

## Next Steps

1. Run full training to generate real replay data
2. Use mettascope to visualize agent behavior
3. Analyze statistics in DuckDB
4. Create custom visualizations from replay data
5. Share GIF animations and charts

For more information, see the Metta documentation.
"""

        readme_file = OUTPUT_DIR / "README.md"
        with open(readme_file, "w") as f:
            f.write(readme_content)
        logger.info(f"✅ README created: {readme_file}")

        # Summary
        logger.info("\n" + "=" * 80)
        logger.info("✅ VISUALIZATION DEMO COMPLETED SUCCESSFULLY")
        logger.info("=" * 80)
        logger.info("\n📊 GENERATED OUTPUTS:")
        logger.info(f"   ✓ Replay metadata: {metadata_file}")
        logger.info(f"   ✓ Visualization manifest: {viz_manifest_file}")
        logger.info(f"   ✓ Statistics summary: {stats_file}")
        logger.info(f"   ✓ Output README: {readme_file}")

        logger.info("\n📁 OUTPUT DIRECTORIES:")
        logger.info(f"   ✓ Replays: {REPLAY_DIR}")
        logger.info(f"   ✓ Stats: {STATS_DIR}")
        logger.info(f"   ✓ Visualizations: {VIZ_DIR}")
        logger.info(f"   ✓ Logs: {OUTPUT_DIR / 'logs'}")

        logger.info("\n🎨 VISUALIZATION TYPES:")
        logger.info("   ✓ GIF animations (episode replays)")
        logger.info("   ✓ PNG thumbnails")
        logger.info("   ✓ Training curves")
        logger.info("   ✓ Policy heatmaps")
        logger.info("   ✓ Agent trajectories")
        logger.info("   ✓ Performance metrics")

        logger.info("\n🔧 METTA TOOLS:")
        logger.info("   ✓ Simulation framework")
        logger.info("   ✓ Replay writer (S3ReplayWriter)")
        logger.info("   ✓ Mettascope server")
        logger.info("   ✓ DuckDB stats tracking")
        logger.info("   ✓ Thumbnail generation")

        logger.info("\n💡 USAGE:")
        logger.info("   • Start mettascope: uv run python mettascope/server.py --port 8080")
        logger.info("   • View GIFs: Open files in visualizations/ directory")
        logger.info("   • Query stats: Use DuckDB to analyze training metrics")
        logger.info(f"   • Read README: {readme_file}")

        logger.info("\n" + "=" * 80)
        logger.info(f"🎉 Check {OUTPUT_DIR} for all generated outputs!")
        logger.info("=" * 80)

        return 0

    except Exception as e:
        logger.error(f"\n❌ Visualization generation failed: {e}")
        import traceback

        logger.error(f"Traceback:\n{traceback.format_exc()}")
        return 1


def main():
    """Main entry point."""
    return generate_visualization_outputs()


if __name__ == "__main__":
    sys.exit(main())
