#!/usr/bin/env python3
"""
Generate animated GIF from Metta replay files.

This script extracts multiple frames from a replay file and combines them
into an animated GIF visualization.
"""

import argparse
import logging
import subprocess
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_frame(replay_file: Path, step: int, output_file: Path, width: int = 800, height: int = 600) -> bool:
    """Generate a single frame from replay at given step."""
    try:
        cmd = [
            "uv",
            "run",
            "python",
            "mettascope/tools/gen_thumb.py",
            "--file",
            str(replay_file),
            "--output",
            str(output_file),
            "--step",
            str(step),
            "--width",
            str(width),
            "--height",
            str(height),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            logger.info(f"Generated frame for step {step}")
            return True
        else:
            logger.error(f"Failed to generate frame for step {step}: {result.stderr}")
            return False
    except Exception as e:
        logger.error(f"Error generating frame for step {step}: {e}")
        return False


def create_gif(frame_files: list[Path], output_gif: Path, duration: int = 100) -> bool:
    """Create animated GIF from frame images using ImageMagick convert or PIL."""
    try:
        # Try using Pillow/PIL first (more portable)
        from PIL import Image

        logger.info(f"Creating GIF with {len(frame_files)} frames...")
        images = []
        for frame_file in frame_files:
            if frame_file.exists():
                images.append(Image.open(frame_file))

        if images:
            images[0].save(
                output_gif, save_all=True, append_images=images[1:], duration=duration, loop=0, optimize=False
            )
            logger.info(f"✅ GIF created successfully: {output_gif}")
            return True
        else:
            logger.error("No valid frames to create GIF")
            return False

    except ImportError:
        logger.warning("PIL/Pillow not available, trying ImageMagick...")
        # Fallback to ImageMagick
        try:
            cmd = (
                ["convert", "-delay", str(duration // 10), "-loop", "0"]
                + [str(f) for f in frame_files]
                + [str(output_gif)]
            )
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                logger.info(f"✅ GIF created successfully: {output_gif}")
                return True
            else:
                logger.error(f"ImageMagick convert failed: {result.stderr}")
                return False
        except FileNotFoundError:
            logger.error("ImageMagick not found. Please install PIL/Pillow or ImageMagick")
            return False
    except Exception as e:
        logger.error(f"Error creating GIF: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Generate animated GIF from Metta replay file")
    parser.add_argument("--replay", "-r", required=True, help="Path to replay file (.json.z)")
    parser.add_argument("--output", "-o", default="simulation.gif", help="Output GIF filename")
    parser.add_argument("--frames", "-f", type=int, default=30, help="Number of frames to extract")
    parser.add_argument("--step-interval", "-s", type=int, default=10, help="Step interval between frames")
    parser.add_argument("--duration", "-d", type=int, default=100, help="Frame duration in milliseconds")
    parser.add_argument("--width", "-W", type=int, default=800, help="Frame width")
    parser.add_argument("--height", "-H", type=int, default=600, help="Frame height")

    args = parser.parse_args()

    replay_file = Path(args.replay)
    if not replay_file.exists():
        logger.error(f"Replay file not found: {replay_file}")
        return 1

    output_gif = Path(args.output)
    temp_dir = output_gif.parent / "temp_frames"
    temp_dir.mkdir(exist_ok=True)

    logger.info(f"Generating {args.frames} frames from replay: {replay_file}")
    logger.info(f"Output GIF: {output_gif}")

    # Generate frames
    frame_files = []
    for i in range(args.frames):
        step = i * args.step_interval
        frame_file = temp_dir / f"frame_{i:04d}.png"
        if generate_frame(replay_file, step, frame_file, args.width, args.height):
            frame_files.append(frame_file)

    if not frame_files:
        logger.error("No frames generated successfully")
        return 1

    logger.info(f"Generated {len(frame_files)} frames successfully")

    # Create GIF
    if create_gif(frame_files, output_gif, args.duration):
        # Clean up temp frames
        for frame_file in frame_files:
            frame_file.unlink()
        temp_dir.rmdir()

        logger.info(f"🎉 Success! Animated GIF saved to: {output_gif.absolute()}")
        logger.info(f"   Size: {output_gif.stat().st_size / 1024:.1f} KB")
        logger.info(f"   Frames: {len(frame_files)}")
        return 0
    else:
        logger.error("Failed to create GIF")
        return 1


if __name__ == "__main__":
    sys.exit(main())
