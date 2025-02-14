from tensordict import TensorDict
import omegaconf
import torch.nn as nn

from agent.lib.metta_layer import LayerBase

class LSTM(LayerBase):
    def __init__(self, agent_attributes, **cfg):
        '''Taken from models.py.
        Wraps your policy with an LSTM without letting you shoot yourself in the
        foot with bad transpose and shape operations. This saves much pain.'''

        super().__init__(**cfg)
        self.obs_shape = agent_attributes.obs_shape
        self.hidden_size = self.output_size

# what about num layers??

    def _make_layer(self, nn_params={}, **cfg):
        layer = nn.LSTM(
            self.input_size,
            self.hidden_size,
            **nn_params
        )
    
        for name, param in layer.named_parameters():
            if "bias" in name:
                nn.init.constant_(param, 1) # Joseph originally had this as 0 
            elif "weight" in name:
                nn.init.orthogonal_(param, 1.0) # torch's default is uniform

        return layer

    def _forward(self, td: TensorDict):
        x = td['x']
        hidden = td[self.input_source]
        state = td["state"]

        # for some reason, td seems to convert state from a tuple to a tensor
        if state is not None:
            state = tuple(state)

        x_shape, space_shape = x.shape, self.obs_shape
        x_n, space_n = len(x_shape), len(space_shape)
        if x_shape[-space_n:] != space_shape:
            raise ValueError('Invalid input tensor shape', x.shape)

        if x_n == space_n + 1:
            B, TT = x_shape[0], 1
        elif x_n == space_n + 2:
            B, TT = x_shape[:2]
        else:
            raise ValueError('Invalid input tensor shape', x.shape)

        if state is not None:
            assert state[0].shape[1] == state[1].shape[1] == B
        assert hidden.shape == (B*TT, self.input_size)

        hidden = hidden.reshape(B, TT, self.input_size)
        hidden = hidden.transpose(0, 1)

        hidden, state = self.layer(hidden, state)

        hidden = hidden.transpose(0, 1)
        hidden = hidden.reshape(B*TT, self.hidden_size)

        if state is not None:
            state = tuple(s.detach() for s in state)

        td[self.name] = hidden
        td["state"] = state

        return td