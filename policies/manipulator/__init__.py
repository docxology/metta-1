"""
Manipulator agent policy.
"""

import torch
import torch.nn as nn
import numpy as np
import gymnasium as gym

class Policy(nn.Module):
    """
    Manipulator agent policy - specializes in object manipulation.
    """
    
    def __init__(self, observation_space, action_space):
        """
        Initialize the manipulator policy.
        
        Args:
            observation_space: The observation space
            action_space: The action space
        """
        super().__init__()
        
        self.observation_space = observation_space
        self.action_space = action_space
        
        # Simple linear policy
        self.network = nn.Sequential(
            nn.Linear(3, 64),  # Input: x, y, agent_id
            nn.ReLU(),
            nn.Linear(64, 64),
            nn.ReLU(),
            nn.Linear(64, 6)  # Output: 6 action probabilities
        )
        
    def forward(self, obs):
        """
        Forward pass through the policy.
        
        Args:
            obs: Observation tensor
            
        Returns:
            Action logits
        """
        # Convert observation to tensor if needed
        if isinstance(obs, np.ndarray):
            obs = torch.FloatTensor(obs)
        
        return self.network(obs) 