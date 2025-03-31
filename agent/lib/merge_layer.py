import copy

import omegaconf
import torch
from tensordict import TensorDict

from agent.lib.metta_layer import LayerBase

class MergeLayerBase(LayerBase):
    def __init__(self, name, **cfg):
        self._ready = False
        super().__init__(name, **cfg)

        # redefine _input_source to only be the names so MettaAgent can find the components
        # it's ugly but it maintains consistency in the YAML config
        self.sources_full_list = self._input_source
        self._input_source = []
        for src_cfg in self.sources_full_list:
            self._input_source.append(src_cfg['source_name'])

    @property
    def ready(self):
        return self._ready

    def setup(self, input_source_components=None):
        if self._ready:
            return

        self.input_source_components = input_source_components

        # NOTE: in and out tensor shapes do not include batch sizes
        # however, all other sizes do, including processed_lengths
        self._in_tensor_shape = []
        self._out_tensor_shape = []

        self.dims = []
        self.processed_lengths = []
        for src_cfg in self.sources_full_list:
            source_name = src_cfg['source_name']
            
            processed_size = self.input_source_components[source_name]._out_tensor_shape.copy()
            self._in_tensor_shape.append(processed_size)

            processed_size = processed_size[0]
            if src_cfg.get('slice') is not None:
                slice_range = src_cfg['slice']
                if isinstance(slice_range, omegaconf.listconfig.ListConfig):
                    slice_range = list(slice_range)
                if not (isinstance(slice_range, (list, tuple)) and len(slice_range) == 2):
                    raise ValueError(f"'slice' must be a two-element list/tuple for source {source_name}.")

                start, end = slice_range
                slice_dim = src_cfg.get("dim", None)
                if slice_dim is None:
                    raise ValueError(f"Slice 'dim' must be specified for source {source_name}. If a vector, use dim=1 (0 is batch size).")
                length = end - start
                src_cfg['_slice_params'] = {
                    'start': start,
                    'length': length,
                    'dim': slice_dim
                }
                processed_size = length

            self.processed_lengths.append(processed_size)

            self.dims.append(src_cfg.get("dim", 1)) # check if default dim is good to have or will cause problems

        self._setup_merge_layer()
        self._ready = True

    def _setup_merge_layer(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def forward(self, td: TensorDict):
        outputs = []
        for src_cfg in self.sources_full_list:
            source_name = src_cfg['source_name']
            self.input_source_components[source_name].forward(td)
            src_tensor = td[source_name]

            if '_slice_params' in src_cfg:
                params = src_cfg['_slice_params']
                src_tensor = torch.narrow(src_tensor, dim=params['dim'], start=params['start'], length=params['length'])
            outputs.append(src_tensor)

        return self._merge(outputs, td)

    def _merge(self, outputs, td):
        raise NotImplementedError("Subclasses should implement this method.")


class ConcatMergeLayer(MergeLayerBase):
    '''Concatenates tensors along a specified dimension. For vectors, use dim=1.
    Using this for observations can concat channels (dim=1) with their
    associated fields (). But concattenating widths and heights (dim=2 or dim=3) would 
    lead to different shapes of the field of view.'''
    def _setup_merge_layer(self):
        if not all(d == self.dims[0] for d in self.dims):
            raise ValueError(f"For 'concat', all sources must have the same 'dim'. Got dims: {self.dims}")
        self._merge_dim = self.dims[0]
        cat_dim_length = 0
        for size in self.processed_lengths:
            cat_dim_length += size
        self._out_tensor_shape = self._in_tensor_shape[0].copy()
        self._out_tensor_shape[self._merge_dim - 1] = cat_dim_length # the -1 is to account for batch size

    def _merge(self, outputs, td):
        merged = torch.cat(outputs, dim=self._merge_dim)
        td[self._name] = merged
        return td


class AddMergeLayer(MergeLayerBase):
    '''Combines tensors by adding their elements along a specified dimension,
    keeping the same shape.'''
    def _setup_merge_layer(self):
        if not all(s == self._in_tensor_shape[0] for s in self._in_tensor_shape):
            raise ValueError(f"For 'add', all source sizes must match. Got sizes: {self.sizes}")
        self._merge_dim = self.dims[0]
        self._out_tensor_shape = self._in_tensor_shape[0]

    def _merge(self, outputs, td):
        merged = outputs[0]
        for tensor in outputs[1:]:
            merged = merged + tensor
        td[self._name] = merged
        return td


class SubtractMergeLayer(MergeLayerBase):
    def _setup_merge_layer(self):
        if not all(s == self._in_tensor_shape[0] for s in self._in_tensor_shape):
            raise ValueError(f"For 'subtract', all source sizes must match. Got sizes: {self.sizes}")
        self._merge_dim = self.dims[0]
        self._out_tensor_shape = self._in_tensor_shape[0]

    def _merge(self, outputs, td):
        if len(outputs) != 2:
            raise ValueError("Subtract merge_op requires exactly two sources.")
        merged = outputs[0] - outputs[1]
        td[self._name] = merged
        return td


class MeanMergeLayer(MergeLayerBase):
    '''Angrily takes the average, keeping the same shape.'''
    def _setup_merge_layer(self):
        if not all(s == self._in_tensor_shape[0] for s in self._in_tensor_shape):
            raise ValueError(f"For 'mean', all source sizes must match. Got sizes: {self.sizes}")
        self._merge_dim = self.dims[0]
        self._out_tensor_shape = self._in_tensor_shape[0]

    def _merge(self, outputs, td):
        merged = outputs[0]
        for tensor in outputs[1:]:
            merged = merged + tensor
        merged = merged / len(outputs)
        td[self._name] = merged
        return td


class ExpandLayer(LayerBase):
    '''Expand a tensor along a specified dimension by either a given value (expand_value)
      or a value from another tensor (dims_source and input_dim).'''
    def __init__(self, name, expand_dim, input_source, expand_value=None, input_dim=None, dims_source=None, **cfg):
        self._ready = False
        self.expand_dim = expand_dim
        self.input_source = input_source
        self.expand_value = expand_value
        self.input_dim = input_dim
        if dims_source is not None:
            self.dims_source = dims_source
            self.input_source = [input_source, dims_source]
        super().__init__(name, **cfg)

    @property
    def ready(self):
        return self._ready

    def setup(self, input_source_components=None):
        if self._ready:
            return

        self.input_source_components = input_source_components
        self._out_tensor_shape = self.input_source_components[self.input_source[0]]._out_tensor_shape

        if self.dims_source is not None:
            expanded_size = self.input_source_components[self.dims_source]._out_tensor_shape[self.input_dim] 
            self._out_tensor_shape.insert(self.expand_dim, expanded_size)
        else:
            self._out_tensor_shape.insert(self.expand_dim, self.expand_value)

    def _forward(self, td: TensorDict):
        tensor = td[self.input_source[0]]

        if self.dims_source is not None:
            self.expand_value = td[self.dims_source].size(self.input_dim)

        expanded = tensor.unsqueeze(self.expand_dim)
        expand_shape = [-1] * expanded.dim()
        expand_shape[self.expand_dim] = self.expand_value
        tensor = expanded.expand(*expand_shape)

        td[self._name] = tensor
        return td

class CompressLayer(LayerBase):
    '''Multiply two of the dims together, squeezing them into the squeezed_dim.'''
    def __init__(self, name, popped_dim, squeezed_dim, input_source, **cfg):
        self._ready = False
        self.popped_dim = popped_dim
        self.squeezed_dim = squeezed_dim
        self.input_source = input_source
        super().__init__(name, **cfg)

    def setup(self, input_source_components=None):
        if self._ready:
            return

        self.input_source_components = input_source_components
        self._out_tensor_shape = self.input_source_components[self.input_source]._out_tensor_shape
        if self.squeezed_dim == 0 or self.popped_dim == 0:
            # we are multiplying by the batch size, which we don't have ahead of time  
            self._out_tensor_shape.pop(self.popped_dim)
        else:
            compressed_size = self._out_tensor_shape[self.popped_dim] * self._out_tensor_shape[self.squeezed_dim]
            self._out_tensor_shape[self.squeezed_dim] = compressed_size
            self._out_tensor_shape.pop(self.popped_dim)

    def _forward(self, td: TensorDict):
        tensor = td[self.input_source]
        shape = list(tensor.shape)
        compressed_size = shape[self.squeezed_dim] * shape[self.popped_dim]
        shape.pop(self.popped_dim)
        shape[self.squeezed_dim] = compressed_size
        tensor = tensor.reshape(*shape)
        td[self._name] = tensor