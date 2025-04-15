"""
MultiAgentExperiment implementation for Metta.
This provides basic multi-agent experiment functionality.
"""

import logging
import os
import time
from typing import List, Dict, Any, Tuple

import gymnasium as gym
import numpy as np

logger = logging.getLogger("experiments")

class MultiAgentExperiment:
    """
    Multi-agent experiment base class.
    This class defines the interface for multi-agent experiments in Metta.
    """
    
    def __init__(self, name: str, env: Any, agents: List[Dict[str, Any]]):
        """
        Initialize a multi-agent experiment.
        
        Args:
            name: Name of the experiment
            env: Environment instance or config
            agents: List of agent configurations
        """
        self.name = name
        self.env = env
        self.agent_configs = agents
        self.agents = []
        
        # Experiment tracking
        self.current_step = 0
        self.history = {
            'positions': [],  # Agent positions at each step
            'actions': [],    # Actions taken at each step
            'rewards': [],    # Rewards received at each step
        }
        
        # Setup logging
        self.setup_logging()
        
        logger.info(f"Initialized experiment: {self.name}")
        logger.info(f"Environment: {self.env}")
        logger.info(f"Agents: {len(self.agent_configs)}")
        
    def setup_logging(self):
        """Setup experiment logging."""
        if not os.path.exists("logs"):
            os.makedirs("logs")
            
        # Configure logger if not already configured
        if not logger.handlers:
            handler = logging.FileHandler(f"logs/{self.name}.log")
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
    
    def setup(self):
        """Setup the experiment, initialize environment and agents."""
        logger.info("Setting up experiment...")
        
        # Initialize agents
        for i, agent_config in enumerate(self.agent_configs):
            logger.info(f"Initializing agent {i}: {agent_config['type']}")
            # Initialize agent based on config
            # This would be replaced with actual agent initialization
            self.agents.append({
                "id": agent_config["id"],
                "type": agent_config["type"],
                "policy": agent_config["policy"]
            })
        
        logger.info("Experiment setup complete")
        
    def reset(self):
        """Reset the experiment."""
        logger.info("Resetting experiment...")
        # Reset environment and agents
        observations, info = self.env.reset()
        
        # Reset tracking
        self.current_step = 0
        self.history = {
            'positions': [self.env.agent_positions.copy()],
            'actions': [],
            'rewards': [],
        }
        
        return observations, info
    
    def step(self, actions):
        """
        Run one step of the experiment.
        
        Args:
            actions: List of actions for each agent
            
        Returns:
            Tuple of (observations, rewards, terminated, truncated, info)
        """
        self.current_step += 1
        logger.info(f"Executing step {self.current_step}")
        
        # Record actions
        self.history['actions'].append(actions.copy() if isinstance(actions, np.ndarray) else np.array(actions))
        
        # Execute actions in the environment
        observations, rewards, terminated, truncated, info = self.env.step(actions)
        
        # Record rewards and positions
        self.history['rewards'].append(rewards)
        self.history['positions'].append(self.env.agent_positions.copy())
        
        # Log step results
        logger.info(f"Step {self.current_step} complete")
        logger.info(f"  Rewards: {rewards}")
        
        return observations, rewards, terminated, truncated, info
    
    def get_agent_trajectories(self):
        """
        Get trajectories of all agents.
        
        Returns:
            Dictionary with agent trajectories
        """
        trajectories = {}
        for i in range(len(self.agent_configs)):
            agent_id = self.agent_configs[i]['id']
            positions = np.array([pos[i] for pos in self.history['positions']])
            actions = np.array([act[i] for act in self.history['actions']]) if self.history['actions'] else np.array([])
            rewards = np.array([rew[i] for rew in self.history['rewards']]) if self.history['rewards'] else np.array([])
            
            trajectories[agent_id] = {
                'positions': positions,
                'actions': actions,
                'rewards': rewards,
                'type': self.agent_configs[i]['type']
            }
        
        return trajectories
    
    def get_experiment_stats(self):
        """
        Get experiment statistics.
        
        Returns:
            Dictionary with experiment statistics
        """
        stats = {
            'name': self.name,
            'steps': self.current_step,
            'num_agents': len(self.agent_configs),
            'agent_types': [agent['type'] for agent in self.agent_configs],
        }
        
        # Add cumulative rewards if available
        if self.history['rewards']:
            rewards = np.array(self.history['rewards'])
            stats['total_rewards'] = rewards.sum(axis=0)
            stats['mean_rewards'] = rewards.mean(axis=0)
        
        return stats 