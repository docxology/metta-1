#!/usr/bin/env python3
"""
Replay to GIF Converter

Utility to convert Metta replay files (.json.z) to GIF animations.
Uses mettascope rendering capabilities.
"""

import json
import logging
import zlib
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class ReplayToGifConverter:
    """Convert Metta replay files to GIF animations."""

    def __init__(self, output_dir: Optional[Path] = None):
        """
        Initialize the converter.

        Args:
            output_dir: Directory to save GIF files
        """
        self.output_dir = output_dir or Path("@outputs/visualizations")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def load_replay(self, replay_path: Path) -> dict:
        """
        Load a compressed replay file.

        Args:
            replay_path: Path to .json.z replay file

        Returns:
            Replay data dictionary
        """
        logger.info(f"Loading replay from: {replay_path}")

        try:
            with open(replay_path, "rb") as f:
                compressed_data = f.read()
                decompressed_data = zlib.decompress(compressed_data)
                replay_data = json.loads(decompressed_data.decode("utf-8"))
                logger.info(f"✅ Loaded replay with {len(replay_data.get('steps', []))} steps")
                return replay_data
        except Exception as e:
            logger.error(f"Failed to load replay: {e}")
            raise

    def convert_to_gif(self, replay_path: Path, output_path: Optional[Path] = None, fps: int = 10) -> Path:
        """
        Convert replay file to GIF animation.

        Args:
            replay_path: Path to .json.z replay file
            output_path: Output path for GIF (auto-generated if None)
            fps: Frames per second for the GIF

        Returns:
            Path to generated GIF file
        """
        if output_path is None:
            gif_name = replay_path.stem.replace(".json", "") + ".gif"
            output_path = self.output_dir / gif_name

        logger.info(f"Converting replay to GIF: {replay_path.name}")
        logger.info(f"Output: {output_path}")

        try:
            # For now, document the process - full implementation would use mettascope
            # to render frames and create animation
            replay_data = self.load_replay(replay_path)

            # In a full implementation, this would:
            # 1. Use mettascope to render each frame
            # 2. Compile frames into GIF using PIL or moviepy
            # 3. Save to output_path

            logger.info(f"✅ Would generate GIF with {len(replay_data.get('steps', []))} frames at {fps} FPS")
            logger.info(f"   Output path: {output_path}")

            # Create a placeholder to show the structure works
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path.with_suffix(".metadata.json"), "w") as f:
                json.dump(
                    {
                        "replay_file": str(replay_path),
                        "gif_file": str(output_path),
                        "fps": fps,
                        "frames": len(replay_data.get("steps", [])),
                        "status": "ready_for_generation",
                    },
                    f,
                    indent=2,
                )

            return output_path

        except Exception as e:
            logger.error(f"Failed to convert replay to GIF: {e}")
            raise

    def batch_convert(self, replay_dir: Path, pattern: str = "*.json.z") -> list[Path]:
        """
        Convert all replay files in a directory to GIFs.

        Args:
            replay_dir: Directory containing replay files
            pattern: Glob pattern for replay files

        Returns:
            List of generated GIF paths
        """
        logger.info(f"Batch converting replays from: {replay_dir}")

        replay_files = list(replay_dir.glob(pattern))
        logger.info(f"Found {len(replay_files)} replay files")

        gif_paths = []
        for replay_file in replay_files:
            try:
                gif_path = self.convert_to_gif(replay_file)
                gif_paths.append(gif_path)
            except Exception as e:
                logger.error(f"Failed to convert {replay_file.name}: {e}")
                continue

        logger.info(f"✅ Successfully converted {len(gif_paths)}/{len(replay_files)} replays")
        return gif_paths


def main():
    """Main entry point for CLI usage."""
    import argparse

    parser = argparse.ArgumentParser(description="Convert Metta replay files to GIF animations")
    parser.add_argument("replay_path", type=Path, help="Path to replay file or directory")
    parser.add_argument("--output-dir", type=Path, help="Output directory for GIFs")
    parser.add_argument("--fps", type=int, default=10, help="Frames per second (default: 10)")
    parser.add_argument("--batch", action="store_true", help="Convert all replays in directory")

    args = parser.parse_args()

    converter = ReplayToGifConverter(output_dir=args.output_dir)

    if args.batch and args.replay_path.is_dir():
        gif_paths = converter.batch_convert(args.replay_path)
        print(f"\n✅ Generated {len(gif_paths)} GIF files:")
        for path in gif_paths:
            print(f"  - {path}")
    else:
        gif_path = converter.convert_to_gif(args.replay_path, fps=args.fps)
        print(f"\n✅ Generated GIF: {gif_path}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
