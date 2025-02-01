from __future__ import annotations

from typing import List

import hydra
from omegaconf import OmegaConf
from sample_factory.model.action_parameterization import ActionParameterizationDefault
from sample_factory.model.core import ModelCoreRNN
from sample_factory.utils.typing import ActionSpace, ObsSpace
from torch import Tensor
from sample_factory.algo.utils.action_distributions import sample_actions_log_probs

from tensordict import TensorDict
from torch import Tensor, nn
import torch
from agent.agent_interface import MettaAgentInterface
from agent.lib.util import MettaComponent, MettaNet, _MettaHelperComponent
# from agent.components import Composer, Layer
import omegaconf

class MettaAgent(nn.Module, MettaAgentInterface):
    def __init__(
        self,
        obs_space: ObsSpace,
        action_space: ActionSpace,
        grid_features: List[str],
        global_features: List[str],
        **cfg
    ):
        super().__init__()
        cfg = OmegaConf.create(cfg)
        self.cfg = cfg
        self.observation_space = obs_space
        self.action_space = action_space
        self.grid_features = grid_features
        self.global_features = global_features

        self.components = []
        component_cfgs = {cfg.components}

        for component_cfg in component_cfgs.keys():
            component = hydra.utils.instantiate(component_cfgs[component_cfg], MettaAgent=self)
            self.components.append(component)

        for component in self.components:
            # check if custom components and Obs and Recurrent need these.
            component.get_input_source_size()
            component.initialize_layer()

        self.obs_encoder = MettaNet(self.components, '_encoded_obs_')
        self.atn_param = MettaNet(self.components, '_atn_param_')
        self.critic = MettaNet(self.components, '_value_')

    #def weight helper functions

class MettaLayer(nn.Module):
    def __init__(self, MettaAgent, **cfg):
        cfg = OmegaConf.create(cfg)
        super().__init__()
        self.MettaAgent = MettaAgent
        self.name = cfg.name
        self.input_source = cfg.input_source
        self.output_size = cfg.output
        self.layer_type = 'Linear' if not cfg.layer_type else cfg.layer_type
        self.nonlinearity = 'ReLU' if not cfg.nonlinearity else cfg.nonlinearity

    def set_input_source_size(self):
        self.input_size = self.MettaAgent.components[self.input_source].get_out_size()

    def initialize_layer(self):
        self.layer = getattr(nn, self.layer_type)(self.input_size, self.output_size)


    def forward(self, td: TensorDict):
        x = self.MettaAgent.components[self.input_source](td)
        x = self.layer(x)
        if self.nonlinearity:
            x = getattr(nn, self.nonlinearity)(x)
        td[self.name] = x
        return td


class SuperLayer(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        self.name = cfg.name
        # deal with list of inputs
        self.input_source = cfg.input_source
        self.output_size = cfg.output
    
    def get_out_size(self):
        return self.output_size

class MettaLinear(SuperLayer):
    def __init__(self, **cfg):
        cfg = OmegaConf.create(cfg)
        super().__init__(cfg)
        self.layer = nn.Linear(cfg.input, cfg.output)










class Layer(nn.Module):
    def __init__(self, layer_cfg):
        super().__init__()
        self.layer_type = layer_cfg.layer_type if 'layer_type' in layer_cfg else 'Linear'
        if self.layer_type in ['ReLU', 'Sigmoid', 'Tanh', 'LeakyReLU', 'Softmax', 'ELU', 'GELU', 'SELU', 'Softplus', 'Softsign']:
            self.layer = getattr(nn, self.layer_type)()
            self.layer.name = layer_cfg.name
            return
        if self.layer_type == 'Dropout':
            self.layer = getattr(nn, self.layer_type)(layer_cfg.dropout_prob)
            self.layer.name = layer_cfg.name
            return
        self.input = layer_cfg.input
        self.output = layer_cfg.output
        self.layer = getattr(nn, self.layer_type)(layer_cfg.input, layer_cfg.output)
        self.name = layer_cfg.name
        self.input_source = layer_cfg.input_source


    def forward(self, x):
        return self.layer(x)

    # we don't need this if it can just be a property, right?
    def get_out_size(self):
        return self.output
    

class Composer(nn.Module):
    def __init__(self, MettaAgent: MettaAgent, net_cfg):
    # def __init__(self, layers: ListConfig, input, output, MettaAgent: MettaAgent):
        super().__init__()
        self.MettaAgent = MettaAgent
        # self.input = self.get_size(net_cfg.input, "input")
        # self.output = self.get_size(net_cfg.output, "output")
        self.input_layers = list(net_cfg.layers)

        # self.input_layers[0].input = self.input
        # self.input_layers[-1].output = self.output
        # check if the other layers have input and output keys.
        # if not, set the input size to the output size of the previous layer and the output size to the same layer's input size
        self.layers = []
        for i in range(len(self.input_layers)):
            if 'input' not in self.input_layers[i]:
                self.input_layers[i].input = self.input_layers[i - 1].output
                self.input_layers[i].input_source = self.input_layers[i - 1].name
            else:
                self.input_layers[i].input_source = self.input_layers[i].input
                self.input_layers[i].input = self.get_size(self.input_layers[i].input, "input")

            if 'output' not in self.input_layers[i]:
                # default to output equals its input size
                self.input_layers[i].output = self.input_layers[i].input

            layer = Layer(self.input_layers[i])
            self.layers.append(layer)

        self.layers = nn.ModuleList(self.layers)
        print(self.layers)

    def get_size(self, value, type):
        if isinstance(value, int):
            return value
        elif isinstance(value, str):
            keys = value.split('.')
            if len(keys) > 1:
                # this should eventually walk the tree to get the layer within the net
                attr = getattr(self.MettaAgent, keys[-1], None)
                return attr.get_out_size()
            else:
                # find the self.layers index of the layer with the name value
                for i in range(len(self.layers)):
                    if self.layers[i].name == value:
                        return self.layers[i].get_out_size()
                raise ValueError(f"Layer with name {value} not found")


            # below, we want the out size of another net as our input size
            attr = getattr(self.MettaAgent, value, None)
            return attr.get_out_size()
        elif isinstance(value, omegaconf.listconfig.ListConfig):
            size = 0
            for layer in value:
                size += self.get_size(layer, type)
            return size
        else:
            raise ValueError(f"Invalid value type: {type(value)}")
        
    # need to figure out how to route the correct input in
    # maybe do this in MettaAgent?


    def forward(self, x):
        for layer in self.layers:
            x = layer(x)
        return x
    
    def get_out_size(self):
        return self.layers[-1].output_size
    
    def get_in_size(self):
        return self.layers[0].input_size