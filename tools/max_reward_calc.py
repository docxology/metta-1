#%%
import numpy as np
import math
import yaml
import re
from typing import Dict, List, Tuple, Union, Set
from dataclasses import dataclass

###
# This script calculates the maximum reward for a gridworld environment, defined by the total inventory contents at the end of the max_timesteps.
# It does this by finding all enclosed spaces in the map and then calculating the maximum reward for each space.
# It then returns the minimum of either:
# - the maximum reward for a single agent multiplied by the number of agents in each enclosed space, summed over all enclosed spaces.
# - the maximum reward assuming that the resources are flowing at their maximum possible rate for each enclosed space, summed over all enclosed spaces.

# To run:   
# gridworld = GridWorld(mettagrid_yaml_path, map_array)
# est_max_reward = gridworld.estimate_max_reward()
# print(gridworld.simulation_summary())

# Current limitations:
# - Needs further testing to ensure robustness to all map configurations.
# - Only provides an estimate of the maximum reward - will need to refine to get the exact maximum reward if we want this in the future
# - Assumes no conversion ticks.
# - Assumes walls are indestructible.
###

# Constants for resource types
class ResourceType:
    ORE = 'ore'  # For uncolored resources
    ORE_RED = 'ore.red'
    ORE_BLUE = 'ore.blue'
    ORE_GREEN = 'ore.green'
    BATTERY = 'battery'
    HEART = 'heart'

@dataclass
class ResourceConfig:
    """Configuration for a resource in the environment."""
    cooldown: int
    max_output: int
    input_battery: int = 0  # Altar conversion ratio
    input_ore: int = 0     # Generator conversion ratio

@dataclass
class ColoredResourceConfig:
    """Configuration for colored resources (mines and generators)."""
    red: ResourceConfig
    blue: ResourceConfig
    green: ResourceConfig

@dataclass
class EnclosedSpace:
    """Represents an enclosed section in the map."""
    width: int
    height: int
    mines: Dict[str, List[Tuple[int, int]]]  # dict with color keys
    generators: Dict[str, List[Tuple[int, int]]]  # dict with color keys
    altars: List[Tuple[int, int]]
    agents: List[Tuple[int, int]]
    walls: List[Tuple[int, int]]

class GridWorld:
    """A class to calculate maximum possible reward in a gridworld environment.
    
    This class finds all enclosed spaces in the map and calculates
    the maximum reward using two methods:
    1. Single agent reward multiplied by number of agents
    2. Maximum resource flow rate calculation
    """

    def __init__(self, mettagrid_yaml_path: str, map_array: np.ndarray):
        self.map_array = map_array
        self._load_config(mettagrid_yaml_path)
        self._setup_resource_configs()
        self._setup_rewards()
        self.enclosed_spaces = self.find_enclosed_spaces(map_array)

    def _load_config(self, mettagrid_yaml_path: str) -> None:
        """Load and parse the mettagrid configuration file."""
        with open(mettagrid_yaml_path, 'r') as file:
            env_config = yaml.safe_load(file)

        self.game_env = env_config['game']
        self.agent_config = self.game_env['agent']
        self.objects_config = self.game_env['objects']

    def _parse_yaml(self, param: Union[str, int]) -> int:
        """Parse YAML parameter, handling uniform distribution syntax."""
        if isinstance(param, str):
            match = re.match(r'\$\{uniform:[^,]+,[^,]+,([^\}]+)\}', param)
            return int(match.group(1)) if match else int(param)
        return param
    
    def _create_resource_config(self, resource_type: str) -> ResourceConfig:
        """Create a ResourceConfig for a given resource type."""
        config = self.objects_config[resource_type]
        return ResourceConfig(
            cooldown=self._parse_yaml(config['cooldown']),
            max_output=self._parse_yaml(config['max_output']),
            input_battery=self._parse_yaml(config.get('input_battery', 0)),
            input_ore=self._parse_yaml(config.get('input_ore', 0))
        )

    def _create_colored_resource_config(self, resource_type: str) -> ColoredResourceConfig:
        """Create a ColoredResourceConfig for a given resource type."""
        return ColoredResourceConfig(
            red=self._create_resource_config(f'{resource_type}.red'),
            blue=self._create_resource_config(f'{resource_type}.blue'),
            green=self._create_resource_config(f'{resource_type}.green')
        )
    
    def _setup_resource_configs(self) -> None:
        """Set up resource configurations based on map contents."""
        # Check if using colored resources by looking at the map array
        unique_elements = np.unique(self.map_array)
        self.using_colors = any(f'mine.{color}' in unique_elements for color in ['red', 'blue', 'green'])
        
        # Set up mine and generator configs
        if self.using_colors:
            self.mine_config = self._create_colored_resource_config('mine')
            self.generator_config = self._create_colored_resource_config('generator')
        else:
            self.using_red_as_default = 'mine' not in self.objects_config or 'generator' not in self.objects_config
            if self.using_red_as_default:
                self.mine_config = self._create_resource_config('mine.red')
                self.generator_config = self._create_resource_config('generator.red')
            else:
                self.mine_config = self._create_resource_config('mine')
                self.generator_config = self._create_resource_config('generator')

        # Set up altar config (always uncolored)
        self.altar_config = self._create_resource_config('altar')

        # Load environment parameters
        self.inventory_limit = self._parse_yaml(self.agent_config['max_inventory'])
        self.max_timesteps = self._parse_yaml(self.game_env['max_steps'])

    def _setup_rewards(self) -> None:
        """Set up reward values based on yaml config."""
        if self.using_colors:
            self.rewards = {
                ResourceType.ORE_RED: self._parse_yaml(self.agent_config['rewards']['ore.red']),
                ResourceType.ORE_BLUE: self._parse_yaml(self.agent_config['rewards']['ore.blue']),
                ResourceType.ORE_GREEN: self._parse_yaml(self.agent_config['rewards']['ore.green']),
                ResourceType.BATTERY: self._parse_yaml(self.agent_config['rewards']['battery']),
                ResourceType.HEART: self._parse_yaml(self.agent_config['rewards']['heart'])
            }
        else:
            self.using_red_ore_reward = 'ore' not in self.agent_config['rewards']
            ore_reward_key = 'ore.red' if self.using_red_ore_reward else 'ore'
            self.rewards = {
                ResourceType.ORE: self._parse_yaml(self.agent_config['rewards'][ore_reward_key]),
                ResourceType.BATTERY: self._parse_yaml(self.agent_config['rewards']['battery']),
                ResourceType.HEART: self._parse_yaml(self.agent_config['rewards']['heart'])
            }



    def find_enclosed_spaces(self, map_array: np.ndarray) -> List[EnclosedSpace]:
        """Find enclosed spaces in a numpy array map."""
        height, width = map_array.shape
        visited = np.zeros((height, width), dtype=bool)
        enclosed_spaces = []
        
        def flood_fill(x: int, y: int, space: Set[Tuple[int, int]]) -> None:
            """Flood fill to identify connected empty spaces."""
            if x < 0 or x >= width or y < 0 or y >= height:
                return
            if visited[y, x]:
                return
            if map_array[y, x] == "wall":
                return
                
            visited[y, x] = True
            space.add((x, y))
            
            flood_fill(x + 1, y, space)
            flood_fill(x - 1, y, space)
            flood_fill(x, y + 1, space)
            flood_fill(x, y - 1, space)
        
        # Find all enclosed spaces
        for y in range(height):
            for x in range(width):
                if not visited[y, x] and map_array[y, x] != "wall":
                    space = set()
                    flood_fill(x, y, space)
                    
                    # Get space boundaries
                    x_coords = [pos[0] for pos in space]
                    y_coords = [pos[1] for pos in space]
                    space_width = max(x_coords) - min(x_coords) + 1
                    space_height = max(y_coords) - min(y_coords) + 1
                    
                    # Get objects in space
                    mines = self._get_resource_positions(space, "mine")
                    generators = self._get_resource_positions(space, "generator")
                    altars = [(x, y) for x, y in space if map_array[y, x] == "altar"]
                    agents = [(x, y) for x, y in space if map_array[y, x] == "agent.agent"]
                    walls = [(x, y) for x, y in space if map_array[y, x] == "wall"]
                    
                    enclosed_spaces.append(EnclosedSpace(
                        width=space_width,
                        height=space_height,
                        mines=mines,
                        generators=generators,
                        altars=altars,
                        agents=agents,
                        walls=walls
                    ))
        
        return enclosed_spaces
    
    def _get_resource_positions(self, space: Set[Tuple[int, int]], resource_type: str) -> Dict[str, List[Tuple[int, int]]]:
        """Get positions of resources in a space."""
        if self.using_colors:
            return {
                color: [(x, y) for x, y in space if self.map_array[y, x] == f"{resource_type}.{color}"]
                for color in ['red', 'blue', 'green']
            }
        return {'default': [(x, y) for x, y in space if self.map_array[y, x] == resource_type]}

    def _manhattan_distance(self, pos_a: Tuple[int, int], pos_b: Tuple[int, int]) -> int:
        """Calculate Manhattan distance between two positions."""
        return abs(pos_a[0] - pos_b[0]) + abs(pos_a[1] - pos_b[1])

    def _get_minimal_distances(self, space: EnclosedSpace) -> Dict[str, Tuple[int, int, int]]:
        """Calculate the minimal distances between objects in an enclosed space."""
        distances = {}
        colors = ['red', 'blue', 'green'] if self.using_colors else ['default']
        
        for color in colors:
            # Find closest mine to generator for each color
            mine_to_generator = float('inf')
            for mine_pos in space.mines[color]:
                for gen_pos in space.generators[color]:
                    dist = self._manhattan_distance(mine_pos, gen_pos)
                    mine_to_generator = min(mine_to_generator, dist)
            
            # Find closest generator to altar
            generator_to_altar = float('inf')
            for gen_pos in space.generators[color]:
                for altar_pos in space.altars:
                    dist = self._manhattan_distance(gen_pos, altar_pos)
                    generator_to_altar = min(generator_to_altar, dist)
            
            # Find closest altar to mine
            altar_to_mine = float('inf')
            for altar_pos in space.altars:
                for mine_pos in space.mines[color]:
                    dist = self._manhattan_distance(altar_pos, mine_pos)
                    altar_to_mine = min(altar_to_mine, dist)
            
            distances[color] = (mine_to_generator, generator_to_altar, altar_to_mine)
        
        return distances

    def _estimate_max_reward_simple(self, space: EnclosedSpace) -> float:
        """Calculate max reward for a single space by calculating the max reward for a single agent 
        and multiplying by number of agents. Returns the maximum reward given the best color strategy."""
        inventory_space = self.inventory_limit
        time_remaining = self.max_timesteps
        max_reward = 0

        # Calculate rewards for each color strategy
        colors = ['red', 'blue', 'green'] if self.using_colors else ['default']
        for color in colors:
            ore, batteries, hearts = 0, 0, 0
            time_left = time_remaining
            
            # Get configurations for this color
            if self.using_colors:
                mine_config = getattr(self.mine_config, color)
                generator_config = getattr(self.generator_config, color)
            else:
                mine_config = self.mine_config
                generator_config = self.generator_config
            
            # Get distances for this color
            mine_to_generator, generator_to_altar, altar_to_mine = self._get_minimal_distances(space)[color]
            
            while time_left > 0 and inventory_space > 0:
                # Travel to Mine
                if time_left < altar_to_mine:
                    break
                time_left -= altar_to_mine

                # Mining phase
                mine_time = inventory_space * (mine_config.cooldown + 1)
                if time_left < mine_time:
                    ore += time_left // (mine_config.cooldown + 1)
                    break
                time_left -= mine_time
                ore += inventory_space

                # Travel to Generator
                if time_left < mine_to_generator:
                    break
                time_left -= mine_to_generator

                # Generator put phase
                generator_put_time = ore
                if time_left < generator_put_time:
                    ore -= time_left
                    break
                time_left -= generator_put_time

                # Generator get phase
                generator_get_actions = math.ceil(ore / generator_config.max_output)
                generator_get_time = generator_get_actions + (generator_get_actions - 1) * generator_config.cooldown
                if time_left < generator_get_time:
                    completed_gets = (time_left + generator_config.cooldown) // (1 + generator_config.cooldown)
                    batteries += min(ore, completed_gets * generator_config.max_output)
                    ore -= batteries
                    break
                batteries += ore
                ore = 0
                time_left -= generator_get_time

                # Travel to Altar
                if time_left < generator_to_altar:
                    break
                time_left -= generator_to_altar

                # Altar put phase
                altar_put_time = batteries
                if time_left < altar_put_time:
                    batteries -= time_left
                    break
                time_left -= altar_put_time

                # Altar get phase
                hearts_generated = batteries // self.altar_config.input_battery
                altar_get_actions = math.ceil(hearts_generated / self.altar_config.max_output)
                altar_get_time = altar_get_actions + (altar_get_actions - 1) * self.altar_config.cooldown
                if time_left < altar_get_time:
                    completed_gets = (time_left + self.altar_config.cooldown) // (1 + self.altar_config.cooldown)
                    hearts += min(hearts_generated, completed_gets * self.altar_config.max_output)
                    batteries -= hearts * self.altar_config.input_battery
                    break
                hearts += hearts_generated
                batteries = 0
                inventory_space -= hearts_generated
                time_left -= altar_get_time

            # Calculate reward for this color
            if self.using_colors:
                color_reward = (
                    ore * self.rewards[f'ore.{color}'] + 
                    batteries * self.rewards[ResourceType.BATTERY] + 
                    hearts * self.rewards[ResourceType.HEART]
                ) * len(space.agents)
            else:
                color_reward = (
                    ore * self.rewards[ResourceType.ORE] +  # Use single ore reward
                    batteries * self.rewards[ResourceType.BATTERY] + 
                    hearts * self.rewards[ResourceType.HEART]
                ) * len(space.agents)
            
            # Update maximum reward if this color's reward is higher
            max_reward = max(max_reward, color_reward)
        
        return max_reward
    
    def _estimate_max_reward_max_flow(self, space: EnclosedSpace) -> float:
        """Calculate max reward for a single space assuming maximum resource flow rate."""
        total_reward = 0
        colors = ['red', 'blue', 'green'] if self.using_colors else ['default']
        
        # Calculate maximum flow for each color
        for color in colors:
            # Get configurations for this color
            if self.using_colors:
                mine_config = getattr(self.mine_config, color)
                generator_config = getattr(self.generator_config, color)
            else:
                mine_config = self.mine_config
                generator_config = self.generator_config
            
            # 1. Mine throughput (ore per timestep)
            time_per_mine_op = mine_config.cooldown + 1
            ore_per_timestep_per_mine = 1 / time_per_mine_op
            max_ore_rate = ore_per_timestep_per_mine * len(space.mines[color])
            
            # 2. Generator throughput (batteries per timestep)
            ore_needed = generator_config.max_output * generator_config.input_ore
            time_per_generator_cycle = (
                ore_needed +                    # Time to put ore
                generator_config.cooldown +      # Cooldown period
                1                               # Action to get batteries
            )
            batteries_per_timestep_per_generator = generator_config.max_output / time_per_generator_cycle
            max_battery_rate = batteries_per_timestep_per_generator * len(space.generators[color])
            
            # 3. Altar throughput (hearts per timestep)
            batteries_needed = self.altar_config.max_output * self.altar_config.input_battery
            time_per_altar_cycle = batteries_needed + self.altar_config.cooldown + 1
            hearts_per_timestep_per_altar = self.altar_config.max_output / time_per_altar_cycle
            max_heart_rate = hearts_per_timestep_per_altar * len(space.altars)
            
            # Convert all rates to the same unit (hearts per timestep) for comparison
            max_heart_rate_from_ore = max_ore_rate / self.altar_config.input_battery
            max_heart_rate_from_batteries = max_battery_rate / self.altar_config.input_battery
            
            # Identify the bottleneck (lowest potential heart production rate)
            max_possible_heart_rate = min(
                max_heart_rate_from_ore, 
                max_heart_rate_from_batteries, 
                max_heart_rate
            )
            
            # Calculate total maximum heart production over the entire simulation
            total_hearts = max_possible_heart_rate * self.max_timesteps
            total_reward += total_hearts * self.rewards[ResourceType.HEART]
        
        return total_reward
    
    def _calculate_space_reward(self, space: EnclosedSpace) -> float:
        """Calculate the maximum reward for a single space."""
        return min(
            self._estimate_max_reward_simple(space),
            self._estimate_max_reward_max_flow(space)
        )

    def estimate_max_reward(self) -> float:
        """Calculate the estimated maximum reward across all spaces."""
        return sum(self._calculate_space_reward(space) for space in self.enclosed_spaces)

    def simulation_summary(self) -> str:
        """Generate a summary of the simulation parameters and results."""
        estimated_reward = self.estimate_max_reward()
        
        summary = (
            f"The estimated maximum reward is {estimated_reward:.2f}. \n"
            f"Key parameters are:\n"
            f"Number of Enclosed Spaces: {len(self.enclosed_spaces)}\n"
            f"Inventory Limit: {self.inventory_limit}\n"
            f"Max Timesteps: {self.max_timesteps}\n"
            f"Using Colored Resources: {self.using_colors}\n"
        )

        if not self.using_colors:
            if self.using_red_as_default:
                summary += "WARNING: Using red mine/generator parameters as defaults since uncolored parameters are not available in the yaml.\n"
            if self.using_red_ore_reward:
                summary += "WARNING: Using red ore reward as default since uncolored ore reward is not available in the yaml.\n"
            
        summary += f"Rewards:\n"
        
        if self.using_colors:
            summary += (
                f"  - Red Ore: {self.rewards[ResourceType.ORE_RED]}\n"
                f"  - Blue Ore: {self.rewards[ResourceType.ORE_BLUE]}\n"
                f"  - Green Ore: {self.rewards[ResourceType.ORE_GREEN]}\n"
            )
        else:
            summary += f"  - Ore: {self.rewards[ResourceType.ORE]}\n"
            
        summary += (
            f"  - Battery: {self.rewards[ResourceType.BATTERY]}\n"
            f"  - Heart: {self.rewards[ResourceType.HEART]}\n"
        )
        
        # Add space-specific information
        for i, space in enumerate(self.enclosed_spaces):
            summary += f"\nEnclosed Space {i+1}:\n"
            summary += f"Size: {space.width}x{space.height}\n"
            if self.using_colors:
                for color in ['red', 'blue', 'green']:
                    summary += f"Number of {color.capitalize()} Mines: {len(space.mines[color])}\n"
                    summary += f"Number of {color.capitalize()} Generators: {len(space.generators[color])}\n"
            else:
                summary += f"Number of Mines: {len(space.mines['default'])}\n"
                summary += f"Number of Generators: {len(space.generators['default'])}\n"
            summary += f"Number of Altars: {len(space.altars)}\n"
            summary += f"Number of Agents: {len(space.agents)}\n"
            
            # Calculate and show max reward per agent for this space
            space_reward = self._calculate_space_reward(space)
            if len(space.agents) > 0:
                max_reward_per_agent = space_reward / len(space.agents)
                summary += f"Maximum Reward per Agent: {max_reward_per_agent:.2f}\n"
            else:
                summary += "Maximum Reward per Agent: N/A (no agents in space)\n"
        
        return summary