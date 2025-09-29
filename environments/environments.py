"""
Environment implementations for Metta.
"""

import logging
from typing import List, Tuple, Dict, Any

import gymnasium as gym
import numpy as np
from gymnasium.spaces import Discrete, MultiDiscrete, Box

logger = logging.getLogger("environments")

class GridWorld(gym.Env):
    """
    Simple GridWorld environment for multi-agent testing.
    """
    
    def __init__(self, num_agents=2, grid_size=10):
        """
        Initialize the GridWorld environment.
        
        Args:
            num_agents: Number of agents in the environment
            grid_size: Size of the grid (grid_size x grid_size)
        """
        super().__init__()
        
        self.num_agents = num_agents
        self.grid_size = grid_size
        self.player_count = num_agents  # Required for compatibility
        
        # Define observation space: position (x,y) and agent ID
        self.observation_space = Box(
            low=0,
            high=max(grid_size, num_agents),
            shape=(3,),
            dtype=np.int32
        )
        
        # Define action space:
        # First component: action type (0-4: move in 4 directions, 5: stay)
        # Second component: parameter for future expansion
        self.action_space = MultiDiscrete([6, 1])
        
        # Grid features
        self.grid_features = ['position_x', 'position_y', 'agent_id']
        self.global_features = []
        
        # Agent positions
        self.agent_positions = np.zeros((num_agents, 2), dtype=np.int32)
        
        logger.info(f"Initialized GridWorld with {num_agents} agents on {grid_size}x{grid_size} grid")
    
    def reset(self, **kwargs):
        """Reset the environment."""
        # Randomly place agents on the grid
        self.agent_positions = np.zeros((self.num_agents, 2), dtype=np.int32)
        for i in range(self.num_agents):
            self.agent_positions[i] = [
                np.random.randint(0, self.grid_size),
                np.random.randint(0, self.grid_size)
            ]
        
        # Create observations for each agent
        observations = self._get_observations()
        
        # Reset termination and truncation flags
        terminated = np.zeros(self.num_agents, dtype=bool)
        truncated = np.zeros(self.num_agents, dtype=bool)
        
        info = {
            "game": {"step": 0},
            "agent_raw": [{} for _ in range(self.num_agents)]
        }
        
        return observations, info
    
    def step(self, actions):
        """
        Execute actions in the environment.
        
        Args:
            actions: Array of actions for each agent
        
        Returns:
            observations, rewards, terminated, truncated, info
        """
        actions = np.array(actions).astype(np.int32)
        
        # Process agent actions
        for i in range(self.num_agents):
            action_type = actions[i][0]
            
            # Movement actions
            if action_type < 4:  # Move in cardinal directions
                dx, dy = [(0, -1), (1, 0), (0, 1), (-1, 0)][action_type]
                new_pos = self.agent_positions[i] + np.array([dx, dy])
                
                # Check bounds
                if (0 <= new_pos[0] < self.grid_size and 
                    0 <= new_pos[1] < self.grid_size):
                    self.agent_positions[i] = new_pos
            
            # Action 4 is "stay" - no movement
        
        # Calculate rewards
        rewards = np.zeros(self.num_agents, dtype=np.float32)
        
        # Check termination conditions
        terminated = np.zeros(self.num_agents, dtype=bool)
        truncated = np.zeros(self.num_agents, dtype=bool)
        
        # Get observations
        observations = self._get_observations()
        
        # Info dictionary
        info = {
            "game": {"step": 0},
            "agent_raw": [{} for _ in range(self.num_agents)]
        }
        
        return observations, rewards, terminated, truncated, info
    
    def _get_observations(self):
        """Create observation arrays for each agent."""
        observations = np.zeros((self.num_agents, 3), dtype=np.int32)
        
        for i in range(self.num_agents):
            observations[i] = [
                self.agent_positions[i][0],
                self.agent_positions[i][1],
                i  # Agent ID
            ]
        
        return observations
    
    def render(self, mode='human'):
        """Render the environment."""
        grid = np.zeros((self.grid_size, self.grid_size), dtype=str)
        grid.fill('.')
        
        for i, pos in enumerate(self.agent_positions):
            grid[pos[1], pos[0]] = str(i)
        
        for row in grid:
            print(' '.join(row))
        print()
    
    def close(self):
        """Close the environment."""
        pass
    
    def action_names(self):
        """Return the names of possible actions."""
        return ["UP", "RIGHT", "DOWN", "LEFT", "STAY", "NONE"]

# Alias for the gridworld environment
gridworld = GridWorld

# Default environment is just a smaller gridworld
default = lambda **kwargs: GridWorld(grid_size=5, **kwargs) 