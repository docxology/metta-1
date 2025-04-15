#!/usr/bin/env python3
"""
Standalone script to run a Metta experiment.
"""

import sys
import logging
import argparse
import yaml
import time
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.colors as mcolors

import hydra
from omegaconf import OmegaConf

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger("run_experiment")

def load_experiment_config(experiment_name):
    """Load an experiment configuration from file."""
    config_path = Path(f"configs/experiments/{experiment_name}.yaml")
    
    if not config_path.exists():
        logger.error(f"Experiment config not found: {config_path}")
        return None
    
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    
    return config

def instantiate_experiment(config):
    """Instantiate an experiment from a configuration."""
    if config is None:
        return None
    
    # Get the experiment class
    target_path = config["_target_"]
    module_path, class_name = target_path.rsplit(".", 1)
    
    # Import the module
    sys.path.append('.')
    module = __import__(module_path, fromlist=[class_name])
    
    # Get the class
    experiment_class = getattr(module, class_name)
    
    # Instantiate the environment
    env_config = config["env"]
    env_target = env_config["_target_"]
    env_module_path, env_func_name = env_target.rsplit(".", 1)
    env_module = __import__(env_module_path, fromlist=[env_func_name])
    env_func = getattr(env_module, env_func_name)
    
    # Create environment
    env = env_func(**{k: v for k, v in env_config.items() if k != "_target_"})
    
    # Instantiate the experiment
    experiment = experiment_class(
        name=config["name"],
        env=env,
        agents=config["agents"]
    )
    
    return experiment

def visualize_gridworld(env, step, history):
    """Create a visualization of the gridworld environment."""
    grid_size = env.grid_size
    num_agents = env.num_agents
    
    # Create a new figure for the gridworld
    plt.figure(figsize=(10, 8))
    
    # Create a subplot for the grid
    ax_grid = plt.subplot2grid((3, 3), (0, 0), colspan=2, rowspan=2)
    grid = np.zeros((grid_size, grid_size))
    
    # Generate distinct colors for each agent
    colors = list(mcolors.TABLEAU_COLORS.values())
    if num_agents > len(colors):
        colors = colors * (num_agents // len(colors) + 1)
    
    # Plot agent positions
    for i, pos in enumerate(env.agent_positions):
        # Mark current position
        ax_grid.plot(pos[0], pos[1], 'o', markersize=15, color=colors[i], label=f"Agent {i}")
        
        # Plot agent trajectories if history is available
        if history and len(history) > 1:
            agent_history = np.array([h[i] for h in history])
            ax_grid.plot(agent_history[:, 0], agent_history[:, 1], '-', color=colors[i], alpha=0.5)
    
    # Set grid properties
    ax_grid.set_xlim(-0.5, grid_size - 0.5)
    ax_grid.set_ylim(-0.5, grid_size - 0.5)
    ax_grid.set_xticks(np.arange(0, grid_size, 1))
    ax_grid.set_yticks(np.arange(0, grid_size, 1))
    ax_grid.grid(True)
    ax_grid.set_title(f"Step {step}")
    
    # Add agent information subplot
    ax_info = plt.subplot2grid((3, 3), (0, 2), rowspan=2)
    agent_types = [f"Agent {i}: {agent['type'].capitalize()}" for i, agent in enumerate(env.experiment.agent_configs)]
    ax_info.axis('off')
    ax_info.text(0.1, 0.9, "\n".join(agent_types), fontsize=12, verticalalignment='top')
    
    # Add history plot
    if history and len(history) > 1:
        ax_history = plt.subplot2grid((3, 3), (2, 0), colspan=3)
        steps = np.arange(len(history))
        
        # Plot distance between agents over time
        if num_agents > 1:
            distances = []
            for h in history:
                dist = np.sqrt(np.sum((h[0] - h[1])**2))
                distances.append(dist)
            ax_history.plot(steps, distances, 'b-', label='Distance between agents')
            ax_history.set_xlabel('Step')
            ax_history.set_ylabel('Distance')
            ax_history.set_title('Agent Metrics')
            ax_history.legend()
    
    plt.tight_layout()
    return plt.gcf()

def run_experiment(experiment, steps=10, visualize=True, save_animation=False):
    """Run an experiment for a specified number of steps."""
    if experiment is None:
        logger.error("Cannot run experiment: experiment is None")
        return
    
    # Setup the experiment
    experiment.setup()
    
    # Reset the experiment
    experiment.reset()
    
    # Store environment reference and history
    env = experiment.env
    env.experiment = experiment  # Add reference to experiment for visualization
    position_history = []
    
    # For animation
    fig = None
    if save_animation:
        plt.ion()
        fig = plt.figure(figsize=(12, 10))
    
    # Run for specified number of steps
    for i in range(steps):
        logger.info(f"Step {i+1} of {steps}")
        
        # Record positions before step
        position_history.append(env.agent_positions.copy())
        
        # In a real system, we would collect actions from policies here
        # For now, we'll just generate random actions
        actions = []
        for _ in range(len(experiment.agent_configs)):
            # Generate random movement (0-4) with 0 parameter
            actions.append([np.random.randint(0, 5), 0])
        
        # Execute step
        experiment.step(actions)
        
        # Render environment (text-based)
        logger.info("Environment state:")
        env.render()
        
        # Visualize the environment state if requested
        if visualize:
            plt.close('all')  # Close previous figures
            fig = visualize_gridworld(env, i+1, position_history)
            plt.pause(0.5)
            
    # Create animation if requested
    if save_animation and len(position_history) > 1:
        # Create animation
        fig = plt.figure(figsize=(10, 8))
        ax = plt.subplot(111)
        ax.set_xlim(-0.5, env.grid_size - 0.5)
        ax.set_ylim(-0.5, env.grid_size - 0.5)
        ax.set_xticks(np.arange(0, env.grid_size, 1))
        ax.set_yticks(np.arange(0, env.grid_size, 1))
        ax.grid(True)
        
        # Generate colors for agents
        colors = list(mcolors.TABLEAU_COLORS.values())
        if env.num_agents > len(colors):
            colors = colors * (env.num_agents // len(colors) + 1)
        
        scatters = []
        for i in range(env.num_agents):
            scatter = ax.scatter([], [], s=200, color=colors[i], label=f"Agent {i}")
            scatters.append(scatter)
        
        ax.legend()
        
        def update(frame):
            for i, scatter in enumerate(scatters):
                scatter.set_offsets([position_history[frame][i]])
            ax.set_title(f"Step {frame}")
            return scatters
        
        ani = FuncAnimation(fig, update, frames=len(position_history), interval=500, blit=False)
        ani.save(f'experiment_{experiment.name}_animation.gif', writer='pillow', fps=2)
        logger.info(f"Animation saved as experiment_{experiment.name}_animation.gif")

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Run a Metta experiment")
    parser.add_argument("experiment", help="Name of the experiment")
    parser.add_argument("--steps", type=int, default=10, help="Number of steps to run")
    parser.add_argument("--no-viz", action="store_true", help="Disable visualization")
    parser.add_argument("--save-animation", action="store_true", help="Save animation of the experiment")
    
    args = parser.parse_args()
    
    logger.info(f"Loading experiment: {args.experiment}")
    config = load_experiment_config(args.experiment)
    
    if config is None:
        return 1
    
    logger.info(f"Instantiating experiment: {config['name']}")
    experiment = instantiate_experiment(config)
    
    if experiment is None:
        return 1
    
    logger.info(f"Running experiment for {args.steps} steps")
    run_experiment(experiment, args.steps, not args.no_viz, args.save_animation)
    
    logger.info("Experiment complete")
    return 0

if __name__ == "__main__":
    sys.exit(main()) 