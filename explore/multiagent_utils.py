#!/usr/bin/env python3
"""
Utility functions for multi-agent experiments in Metta
Usage: from explore.multiagent_utils import *
"""

import os
import sys
import yaml
import argparse
from pathlib import Path

# Add the parent directory to the path
sys.path.append(str(Path(__file__).parent.parent))

def create_multiagent_experiment(name, num_agents=2, agent_types=None, environment="default"):
    """
    Create a new multi-agent experiment configuration
    
    Args:
        name: Name of the experiment
        num_agents: Number of agents to create
        agent_types: List of agent types (default: ["navigator", "manipulator"])
        environment: Environment configuration to use
    
    Returns:
        Path to the created experiment config
    """
    if agent_types is None:
        agent_types = ["navigator", "manipulator"]
        
    # Ensure we have enough agent types
    if len(agent_types) < num_agents:
        agent_types = agent_types * (num_agents // len(agent_types) + 1)
    agent_types = agent_types[:num_agents]
    
    # Create experiment directory
    config_dir = Path("configs/experiments")
    config_dir.mkdir(exist_ok=True, parents=True)
    
    experiment_path = config_dir / f"{name}.yaml"
    
    # Create experiment config
    config = {
        "_target_": "experiments.MultiAgentExperiment",
        "name": name,
        "env": {
            "_target_": f"environments.{environment}",
            "num_agents": num_agents,
        },
        "agents": []
    }
    
    # Add agent configurations
    for i, agent_type in enumerate(agent_types):
        agent_config = {
            "id": f"agent_{i}",
            "type": agent_type,
            "policy": {
                "_target_": f"policies.{agent_type}.Policy",
                "observation_space": "${env.observation_space}",
                "action_space": "${env.action_space}",
            }
        }
        config["agents"].append(agent_config)
    
    # Save config to file
    with open(experiment_path, "w") as f:
        yaml.dump(config, f, default_flow_style=False)
    
    print(f"Created multi-agent experiment config: {experiment_path}")
    return experiment_path

def run_multiagent_experiment(name, mode="play", hardware="poplinux"):
    """
    Run a multi-agent experiment
    
    Args:
        name: Name of the experiment
        mode: Mode to run (train, eval, play)
        hardware: Hardware configuration to use
    """
    script_dir = Path(__file__).parent
    run_script = script_dir / "run_metta.sh"
    
    if not run_script.exists():
        print(f"Error: Run script not found at {run_script}")
        return False
    
    # Make sure script is executable
    os.chmod(run_script, 0o755)
    
    # Run the experiment
    cmd = f"{run_script} {mode} {name} {hardware}"
    print(f"Running command: {cmd}")
    return os.system(cmd) == 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multi-agent experiment utilities")
    parser.add_argument("action", choices=["create", "run"], help="Action to perform")
    parser.add_argument("name", help="Experiment name")
    parser.add_argument("--agents", type=int, default=2, help="Number of agents")
    parser.add_argument("--types", nargs="+", help="Agent types")
    parser.add_argument("--env", default="default", help="Environment to use")
    parser.add_argument("--mode", default="play", choices=["train", "eval", "play"], help="Mode to run")
    parser.add_argument("--hardware", default="poplinux", help="Hardware configuration")
    
    args = parser.parse_args()
    
    if args.action == "create":
        create_multiagent_experiment(args.name, args.agents, args.types, args.env)
    elif args.action == "run":
        run_multiagent_experiment(args.name, args.mode, args.hardware) 