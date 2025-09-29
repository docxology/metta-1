#!/usr/bin/env python3
"""
Replay Generator - Version 2 Format

Generates proper Metta replay files in version 2 format compatible with mettascope.
Based on specification in mettascope/docs/replay_spec.md
"""

import json
import logging
import random
import zlib
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)


class ReplayGeneratorV2:
    """Generate Metta replay files in version 2 format."""

    def __init__(self, map_size: Tuple[int, int] = (20, 20), num_agents: int = 2):
        """
        Initialize replay generator.

        Args:
            map_size: (width, height) of the map
            num_agents: Number of agents in the simulation
        """
        self.map_size = map_size
        self.num_agents = num_agents
        self.type_names = ["agent", "wall", "floor", "goal", "obstacle"]
        self.action_names = ["noop", "move_forward", "move_backward", "turn_left", "turn_right"]
        self.item_names = ["key", "coin", "health", "shield"]
        self.group_names = [f"group_{i}" for i in range(max(1, num_agents // 2))]

    def generate_agent_trajectory(
        self, agent_id: int, max_steps: int, start_pos: Optional[Tuple[int, int]] = None
    ) -> Dict[str, Any]:
        """
        Generate realistic agent trajectory with time series data.

        Args:
            agent_id: Agent identifier
            max_steps: Maximum number of steps
            start_pos: Starting position (x, y), or random if None

        Returns:
            Agent object dictionary
        """
        if start_pos is None:
            start_x = random.randint(2, self.map_size[0] - 3)
            start_y = random.randint(2, self.map_size[1] - 3)
        else:
            start_x, start_y = start_pos

        # Generate location time series (agent moves around)
        location_series = []
        x, y = start_x, start_y
        rotation = 0

        for step in range(0, max_steps, 5):  # Update position every 5 steps
            # Random walk
            if random.random() < 0.5:
                dx = random.choice([-1, 0, 1])
                dy = random.choice([-1, 0, 1])
                x = max(1, min(self.map_size[0] - 2, x + dx))
                y = max(1, min(self.map_size[1] - 2, y + dy))

            location_series.append([step, [x, y, 0]])  # z=0 for layer

        # Generate rotation time series
        rotation_series = []
        for step in range(0, max_steps, 10):
            rotation = (rotation + random.randint(0, 3)) % 4
            rotation_series.append([step, rotation])

        # Generate action time series
        action_series = []
        for step in range(max_steps):
            action_id = random.randint(0, len(self.action_names) - 1)
            if step == 0 or action_id != action_series[-1][1]:
                action_series.append([step, action_id])

        # Generate reward time series
        reward_series = []
        total_reward = 0.0
        for step in range(0, max_steps, 10):
            step_reward = random.uniform(-0.1, 0.5)
            total_reward += step_reward
            reward_series.append([step, round(step_reward, 3)])

        # Generate total reward time series
        total_reward_series = []
        cumulative = 0.0
        for step in range(0, max_steps, 10):
            cumulative += random.uniform(-0.1, 0.5)
            total_reward_series.append([step, round(cumulative, 3)])

        # Generate inventory time series (occasionally pick up items)
        inventory_series = [[0, []]]  # Start empty
        current_inventory = []
        for step in range(20, max_steps, 30):
            if random.random() < 0.3 and len(current_inventory) < 3:
                item_id = random.randint(0, len(self.item_names) - 1)
                current_inventory.append(item_id)
                inventory_series.append([step, current_inventory.copy()])

        return {
            "id": agent_id,  # Object ID
            "type_id": 0,  # References type_names[0] = "agent"
            "agent_id": agent_id,  # Agent-specific ID
            "location": location_series,
            "orientation": rotation_series,
            "action_id": action_series,
            "action_success": [[0, True]],  # Most actions succeed
            "current_reward": reward_series,
            "total_reward": total_reward_series,
            "inventory": inventory_series,
            "inventory_max": 5,
            "color": (agent_id * 60) % 256,
            "group_id": agent_id % len(self.group_names),
            "frozen": [[0, False]],
        }

    def generate_static_objects(self) -> List[Dict[str, Any]]:
        """
        Generate static environment objects (walls, goals, etc.).

        Returns:
            List of object dictionaries
        """
        objects = []
        object_id = 100  # Start after agent IDs

        # Create walls around perimeter
        for x in range(self.map_size[0]):
            # Top and bottom walls
            for y in [0, self.map_size[1] - 1]:
                objects.append(
                    {
                        "id": object_id,
                        "type_id": 1,  # wall
                        "location": [x, y, 0],  # Static, not time series
                        "orientation": 0,
                        "color": 100,
                    }
                )
                object_id += 1

        for y in range(1, self.map_size[1] - 1):
            # Left and right walls
            for x in [0, self.map_size[0] - 1]:
                objects.append(
                    {
                        "id": object_id,
                        "type_id": 1,  # wall
                        "location": [x, y, 0],
                        "orientation": 0,
                        "color": 100,
                    }
                )
                object_id += 1

        # Add a goal in the center
        goal_x = self.map_size[0] // 2
        goal_y = self.map_size[1] // 2
        objects.append(
            {
                "id": object_id,
                "type_id": 3,  # goal
                "location": [goal_x, goal_y, 0],
                "orientation": 0,
                "color": 200,
            }
        )

        return objects

    def generate_replay(
        self,
        episode_name: str,
        max_steps: int = 200,
        seed: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Generate complete replay in version 2 format.

        Args:
            episode_name: Name of the episode/replay
            max_steps: Maximum number of simulation steps
            seed: Random seed for reproducibility

        Returns:
            Complete replay dictionary
        """
        if seed is not None:
            random.seed(seed)

        logger.info(f"Generating replay: {episode_name}")
        logger.info(f"  Map size: {self.map_size}")
        logger.info(f"  Agents: {self.num_agents}")
        logger.info(f"  Steps: {max_steps}")

        # Generate agent objects
        agents = []
        for agent_id in range(self.num_agents):
            agent = self.generate_agent_trajectory(agent_id, max_steps)
            agents.append(agent)

        # Generate static objects
        static_objects = self.generate_static_objects()

        # Combine all objects
        all_objects = agents + static_objects

        # Create replay structure (version 2 format)
        replay = {
            "version": 2,  # MUST be number 2
            "file_name": f"{episode_name}.json.z",
            "num_agents": self.num_agents,
            "max_steps": max_steps,
            "map_size": list(self.map_size),
            "type_names": self.type_names,
            "action_names": self.action_names,
            "item_names": self.item_names,
            "group_names": self.group_names,
            "objects": all_objects,
        }

        logger.info(f"✅ Generated replay with {len(all_objects)} objects")
        logger.info(f"   Agents: {self.num_agents}")
        logger.info(f"   Static objects: {len(static_objects)}")

        return replay

    def save_replay(self, replay: Dict[str, Any], output_path: Path) -> Path:
        """
        Save replay as compressed JSON (.json.z).

        Args:
            replay: Replay dictionary
            output_path: Output file path

        Returns:
            Path to saved file
        """
        # Convert to JSON
        replay_json = json.dumps(replay, separators=(",", ":"))  # Compact format
        replay_bytes = replay_json.encode("utf-8")

        # Compress
        compressed = zlib.compress(replay_bytes, level=9)

        # Save
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(compressed)

        compression_ratio = len(compressed) / len(replay_bytes)
        logger.info(f"✅ Saved replay: {output_path}")
        logger.info(f"   Original: {len(replay_bytes):,} bytes")
        logger.info(f"   Compressed: {len(compressed):,} bytes")
        logger.info(f"   Ratio: {compression_ratio:.1%}")

        return output_path

    def generate_episode_batch(
        self,
        output_dir: Path,
        num_episodes: int = 3,
        max_steps: int = 200,
    ) -> List[Path]:
        """
        Generate a batch of episode replays.

        Args:
            output_dir: Directory to save replay files
            num_episodes: Number of episodes to generate
            max_steps: Maximum steps per episode

        Returns:
            List of generated replay file paths
        """
        logger.info(f"Generating {num_episodes} episode replays...")

        replay_paths = []
        for episode_num in range(num_episodes):
            episode_name = f"episode_{episode_num:03d}"
            replay = self.generate_replay(episode_name, max_steps, seed=episode_num)

            output_path = output_dir / f"{episode_name}.json.z"
            self.save_replay(replay, output_path)
            replay_paths.append(output_path)

        logger.info(f"✅ Generated {len(replay_paths)} replay files")
        return replay_paths


def main():
    """CLI entry point for replay generation."""
    import argparse

    parser = argparse.ArgumentParser(description="Generate Metta replay files (version 2 format)")
    parser.add_argument("--output-dir", type=Path, default=Path("replays"), help="Output directory")
    parser.add_argument("--episodes", type=int, default=3, help="Number of episodes")
    parser.add_argument("--steps", type=int, default=200, help="Steps per episode")
    parser.add_argument("--map-width", type=int, default=20, help="Map width")
    parser.add_argument("--map-height", type=int, default=20, help="Map height")
    parser.add_argument("--agents", type=int, default=2, help="Number of agents")

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    generator = ReplayGeneratorV2(
        map_size=(args.map_width, args.map_height),
        num_agents=args.agents,
    )

    replay_paths = generator.generate_episode_batch(
        output_dir=args.output_dir,
        num_episodes=args.episodes,
        max_steps=args.steps,
    )

    print(f"\n✅ Generated {len(replay_paths)} replay files:")
    for path in replay_paths:
        print(f"  - {path}")


if __name__ == "__main__":
    main()
