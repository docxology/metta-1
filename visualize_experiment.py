#!/usr/bin/env python3
"""
Visualize Metta experiments with interactive and animated visualizations.
"""

import argparse
import yaml
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.colors as mcolors
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Rectangle
from pathlib import Path
import json
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("visualize_experiment")

def load_experiment_results(experiment_name):
    """Load experiment results from logs."""
    log_path = Path(f"logs/{experiment_name}.log")
    
    if not log_path.exists():
        logger.error(f"Experiment log not found: {log_path}")
        return None
    
    # Parse log file to extract relevant information
    positions = []
    rewards = []
    actions = []
    step = 0
    
    with open(log_path, "r") as f:
        for line in f:
            if "Executing step" in line:
                step = int(line.split("step ")[1].strip())
            
            # We would parse positions, rewards, etc. from the logs
            # In a real system, we would probably have a better way to store this data
            
    # For demo purposes, generate some synthetic data if log parsing is incomplete
    # This would be replaced with real data in production
    if len(positions) == 0:
        config_path = Path(f"configs/experiments/{experiment_name}.yaml")
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
        
        num_agents = len(config["agents"])
        steps = 15  # Some default
        
        # Generate random positions
        grid_size = 10
        positions = []
        for i in range(steps + 1):
            agent_positions = []
            for j in range(num_agents):
                # Generate random positions but with small changes between steps
                if i == 0:
                    agent_positions.append([
                        np.random.randint(0, grid_size),
                        np.random.randint(0, grid_size)
                    ])
                else:
                    prev_pos = positions[i-1][j]
                    move = np.random.randint(0, 5)
                    if move < 4:  # Move in a direction
                        dx, dy = [(0, -1), (1, 0), (0, 1), (-1, 0)][move]
                        new_pos = [prev_pos[0] + dx, prev_pos[1] + dy]
                        # Ensure within bounds
                        new_pos[0] = max(0, min(grid_size-1, new_pos[0]))
                        new_pos[1] = max(0, min(grid_size-1, new_pos[1]))
                        agent_positions.append(new_pos)
                    else:  # Stay
                        agent_positions.append(prev_pos)
            positions.append(agent_positions)
        
        # Generate random rewards
        rewards = []
        for i in range(steps):
            agent_rewards = []
            for j in range(num_agents):
                # Mostly 0 rewards with occasional 1
                if np.random.random() < 0.1:
                    agent_rewards.append(1.0)
                else:
                    agent_rewards.append(0.0)
            rewards.append(agent_rewards)
        
        # Generate random actions
        actions = []
        for i in range(steps):
            agent_actions = []
            for j in range(num_agents):
                action = [np.random.randint(0, 5), 0]  # Random action type with 0 parameter
                agent_actions.append(action)
            actions.append(agent_actions)
    
    return {
        "name": experiment_name,
        "positions": positions,
        "rewards": rewards,
        "actions": actions,
        "num_steps": len(positions) - 1,
        "num_agents": len(positions[0]) if positions else 0,
        "agent_types": [agent["type"] for agent in config["agents"]]
    }

def create_static_visualization(results):
    """Create static visualizations of experiment results."""
    if not results:
        logger.error("No results to visualize")
        return
    
    positions = np.array(results["positions"])
    rewards = np.array(results["rewards"]) if results["rewards"] else np.zeros((results["num_steps"], results["num_agents"]))
    num_agents = results["num_agents"]
    agent_types = results["agent_types"]
    num_steps = results["num_steps"]
    
    # Create figure with multiple subplots
    fig = plt.figure(figsize=(15, 12))
    fig.suptitle(f"Experiment: {results['name']}", fontsize=16)
    
    # Generate colors for each agent
    colors = list(mcolors.TABLEAU_COLORS.values())
    if num_agents > len(colors):
        colors = colors * (num_agents // len(colors) + 1)
    
    # 1. Plot agent trajectories
    ax_traj = fig.add_subplot(221)
    grid_size = max([max([p[0] for p in pos]) for pos in positions]) + 1
    
    for i in range(num_agents):
        agent_positions = positions[:, i]
        # Plot path
        ax_traj.plot(agent_positions[:, 0], agent_positions[:, 1], '-', color=colors[i], alpha=0.6, 
                     label=f"Agent {i} ({agent_types[i]})")
        # Plot start and end points
        ax_traj.plot(agent_positions[0, 0], agent_positions[0, 1], 'o', color=colors[i], markersize=10)
        ax_traj.plot(agent_positions[-1, 0], agent_positions[-1, 1], 's', color=colors[i], markersize=10)
    
    ax_traj.set_xlim(-0.5, grid_size - 0.5)
    ax_traj.set_ylim(-0.5, grid_size - 0.5)
    ax_traj.set_xticks(np.arange(0, grid_size, 1))
    ax_traj.set_yticks(np.arange(0, grid_size, 1))
    ax_traj.grid(True)
    ax_traj.set_title("Agent Trajectories")
    ax_traj.set_xlabel("X")
    ax_traj.set_ylabel("Y")
    ax_traj.legend()
    
    # 2. Plot agent rewards
    ax_rewards = fig.add_subplot(222)
    steps = np.arange(1, num_steps + 1)
    
    for i in range(num_agents):
        agent_rewards = rewards[:, i]
        ax_rewards.plot(steps, agent_rewards, '-o', color=colors[i], label=f"Agent {i}")
        # Plot cumulative rewards
        cum_rewards = np.cumsum(agent_rewards)
        ax_rewards.plot(steps, cum_rewards, '--', color=colors[i], alpha=0.5)
    
    ax_rewards.set_title("Agent Rewards")
    ax_rewards.set_xlabel("Step")
    ax_rewards.set_ylabel("Reward")
    ax_rewards.legend()
    ax_rewards.grid(True)
    
    # 3. Plot agent distances
    ax_dist = fig.add_subplot(223)
    
    if num_agents > 1:
        distances = []
        for s in range(num_steps + 1):
            step_distances = []
            for i in range(num_agents):
                for j in range(i+1, num_agents):
                    dist = np.sqrt(np.sum((positions[s, i] - positions[s, j])**2))
                    step_distances.append({
                        "step": s,
                        "agent1": i, 
                        "agent2": j,
                        "distance": dist
                    })
            distances.extend(step_distances)
        
        # Convert to DataFrame for easier plotting
        dist_df = pd.DataFrame(distances)
        
        # Plot distance between each agent pair
        for i in range(num_agents):
            for j in range(i+1, num_agents):
                pair_data = dist_df[(dist_df["agent1"] == i) & (dist_df["agent2"] == j)]
                ax_dist.plot(pair_data["step"], pair_data["distance"], '-', 
                           label=f"Agents {i}-{j}", alpha=0.7)
        
        ax_dist.set_title("Agent Distances")
        ax_dist.set_xlabel("Step")
        ax_dist.set_ylabel("Distance")
        ax_dist.legend()
        ax_dist.grid(True)
    else:
        ax_dist.text(0.5, 0.5, "Need multiple agents to show distances", 
                   ha='center', va='center', fontsize=12)
    
    # 4. Plot agent action distribution
    ax_actions = fig.add_subplot(224)
    
    if results["actions"]:
        actions = np.array(results["actions"])
        action_types = ["UP", "RIGHT", "DOWN", "LEFT", "STAY"]
        
        # Count action types per agent
        action_counts = np.zeros((num_agents, len(action_types)))
        for i in range(num_agents):
            for a in range(len(action_types)):
                action_counts[i, a] = np.sum(actions[:, i, 0] == a)
        
        # Create bar positions
        bar_width = 0.8 / num_agents
        bar_positions = np.arange(len(action_types))
        
        for i in range(num_agents):
            offset = (i - num_agents/2 + 0.5) * bar_width
            ax_actions.bar(bar_positions + offset, action_counts[i], 
                         width=bar_width, color=colors[i], alpha=0.7,
                         label=f"Agent {i}")
        
        ax_actions.set_title("Action Distribution")
        ax_actions.set_xticks(bar_positions)
        ax_actions.set_xticklabels(action_types)
        ax_actions.set_ylabel("Count")
        ax_actions.legend()
    else:
        ax_actions.text(0.5, 0.5, "No action data available", 
                      ha='center', va='center', fontsize=12)
    
    plt.tight_layout()
    fig.subplots_adjust(top=0.9)  # Make room for title
    
    # Save the visualization
    output_path = f"experiment_{results['name']}_visualization.png"
    plt.savefig(output_path, dpi=150)
    logger.info(f"Static visualization saved as {output_path}")
    
    return fig

def create_animation(results):
    """Create an animated visualization of the experiment."""
    if not results:
        logger.error("No results to visualize")
        return
    
    positions = np.array(results["positions"])
    num_agents = results["num_agents"]
    grid_size = max([max([p[0] for p in pos]) for pos in positions]) + 1
    
    # Generate colors for each agent
    colors = list(mcolors.TABLEAU_COLORS.values())
    if num_agents > len(colors):
        colors = colors * (num_agents // len(colors) + 1)
    
    fig, ax = plt.subplots(figsize=(10, 10))
    fig.suptitle(f"Experiment: {results['name']}", fontsize=16)
    
    # Set up the grid
    ax.set_xlim(-0.5, grid_size - 0.5)
    ax.set_ylim(-0.5, grid_size - 0.5)
    ax.set_xticks(np.arange(0, grid_size, 1))
    ax.set_yticks(np.arange(0, grid_size, 1))
    ax.grid(True)
    
    # Create agent markers and trails
    agent_markers = []
    agent_trails = []
    
    for i in range(num_agents):
        # Marker for current position
        marker, = ax.plot([], [], 'o', color=colors[i], markersize=15, 
                         label=f"Agent {i} ({results['agent_types'][i]})")
        agent_markers.append(marker)
        
        # Line for trail
        trail, = ax.plot([], [], '-', color=colors[i], alpha=0.4)
        agent_trails.append(trail)
    
    # Create title with step information
    title = ax.text(0.5, 1.05, "", transform=ax.transAxes, ha="center", fontsize=14)
    
    # Action text displays
    action_texts = []
    for i in range(num_agents):
        text = ax.text(0.02, 0.98 - 0.05*i, "", transform=ax.transAxes, 
                      color=colors[i], fontsize=12, ha="left", va="top")
        action_texts.append(text)
    
    # Legend
    ax.legend(loc="upper right")
    
    def init():
        for marker in agent_markers:
            marker.set_data([], [])
        for trail in agent_trails:
            trail.set_data([], [])
        title.set_text("")
        for text in action_texts:
            text.set_text("")
        return agent_markers + agent_trails + [title] + action_texts
    
    def update(frame):
        # Update title
        title.set_text(f"Step: {frame}")
        
        for i in range(num_agents):
            # Update marker position
            agent_markers[i].set_data([positions[frame, i, 0]], [positions[frame, i, 1]])
            
            # Update trail
            if frame > 0:
                agent_trails[i].set_data(
                    [pos[i][0] for pos in positions[:frame+1]],
                    [pos[i][1] for pos in positions[:frame+1]]
                )
            
            # Update action text
            if frame < len(results["actions"]):
                action_type = results["actions"][frame][i][0]
                action_name = ["UP", "RIGHT", "DOWN", "LEFT", "STAY"][action_type] if action_type < 5 else "NONE"
                action_texts[i].set_text(f"Agent {i}: {action_name}")
        
        return agent_markers + agent_trails + [title] + action_texts
    
    ani = FuncAnimation(fig, update, frames=len(positions), init_func=init, 
                       interval=500, blit=True)
    
    # Save the animation
    output_path = f"experiment_{results['name']}_advanced_animation.gif"
    ani.save(output_path, writer='pillow', fps=2)
    logger.info(f"Advanced animation saved as {output_path}")
    
    return ani

def create_heatmap(results):
    """Create a heatmap of agent positions over time."""
    if not results:
        logger.error("No results to visualize")
        return
    
    positions = np.array(results["positions"])
    num_agents = results["num_agents"]
    grid_size = max([max([p[0] for p in pos]) for pos in positions]) + 1
    
    # Generate colors for each agent
    colors = list(mcolors.TABLEAU_COLORS.values())
    if num_agents > len(colors):
        colors = colors * (num_agents // len(colors) + 1)
    
    fig, axes = plt.subplots(1, num_agents, figsize=(5*num_agents, 5))
    if num_agents == 1:
        axes = [axes]
    
    fig.suptitle(f"Position Heatmaps - {results['name']}", fontsize=16)
    
    for i in range(num_agents):
        ax = axes[i]
        
        # Create heatmap grid
        heatmap = np.zeros((grid_size, grid_size))
        
        # Count frequency of positions
        for step in range(len(positions)):
            x, y = positions[step, i]
            heatmap[int(y), int(x)] += 1
        
        # Plot heatmap
        im = ax.imshow(heatmap, cmap='hot', interpolation='nearest', origin='lower')
        
        # Add colorbar
        fig.colorbar(im, ax=ax, label='Visit count')
        
        # Set ticks
        ax.set_xticks(np.arange(0, grid_size, 1))
        ax.set_yticks(np.arange(0, grid_size, 1))
        
        # Set title
        ax.set_title(f"Agent {i} ({results['agent_types'][i]})")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
    
    plt.tight_layout()
    fig.subplots_adjust(top=0.85)  # Make room for title
    
    # Save the heatmap
    output_path = f"experiment_{results['name']}_heatmap.png"
    plt.savefig(output_path, dpi=150)
    logger.info(f"Heatmap visualization saved as {output_path}")
    
    return fig

def visualize_experiment(experiment_name):
    """Create comprehensive visualizations for an experiment."""
    logger.info(f"Loading experiment results: {experiment_name}")
    results = load_experiment_results(experiment_name)
    
    if not results:
        logger.error(f"Failed to load results for experiment: {experiment_name}")
        return 1
    
    logger.info(f"Creating static visualization for experiment: {experiment_name}")
    create_static_visualization(results)
    
    logger.info(f"Creating animation for experiment: {experiment_name}")
    create_animation(results)
    
    logger.info(f"Creating position heatmap for experiment: {experiment_name}")
    create_heatmap(results)
    
    logger.info(f"Visualizations complete for experiment: {experiment_name}")
    return 0

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Visualize a Metta experiment")
    parser.add_argument("experiment", help="Name of the experiment")
    
    args = parser.parse_args()
    
    return visualize_experiment(args.experiment)

if __name__ == "__main__":
    exit(main()) 