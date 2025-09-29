# sweep.protein

**Module**: `sweep.protein`

**Source**: `metta/sweep/protein.py`

**Imports**:
- `copy.deepcopy`
- `logging`
- `math`
- `mettagrid.util.dict_utils.unroll_nested_dict`
- `numpy`
- `pyro.contrib.gp`
- `random`
- `time`
- `torch`

## Classes (7)

### Space

**Class**: `sweep.protein.Space`

**Constructor**: `Space(self, min, max, scale, mean, is_integer = ...)`

**Methods**: 2

#### normalize

**Signature**: `Space.normalize(self, value)`

**Location**: line 27

#### unnormalize

**Signature**: `Space.unnormalize(self, value)`

**Location**: line 30


### Linear

**Class**: `sweep.protein.Linear`

**Constructor**: `Linear(self, min, max, scale, mean, is_integer = ...)`

**Methods**: 2

#### normalize

**Signature**: `Linear.normalize(self, value)`

**Location**: line 40

#### unnormalize

**Signature**: `Linear.unnormalize(self, value)`

**Location**: line 44


### Pow2

**Class**: `sweep.protein.Pow2`

**Constructor**: `Pow2(self, min, max, scale, mean, is_integer = ...)`

**Methods**: 2

#### normalize

**Signature**: `Pow2.normalize(self, value)`

**Location**: line 58

#### unnormalize

**Signature**: `Pow2.unnormalize(self, value)`

**Location**: line 62


### Log

**Class**: `sweep.protein.Log`

**Constructor**: `Log(self, min, max, scale, mean, is_integer = ...)`

**Methods**: 2

#### normalize

**Signature**: `Log.normalize(self, value)`

**Location**: line 79

#### unnormalize

**Signature**: `Log.unnormalize(self, value)`

**Location**: line 85


### Logit

**Class**: `sweep.protein.Logit`

**Constructor**: `Logit(self, min, max, scale, mean, is_integer = ...)`

**Methods**: 2

#### normalize

**Signature**: `Logit.normalize(self, value)`

**Location**: line 104

#### unnormalize

**Signature**: `Logit.unnormalize(self, value)`

**Location**: line 110


### Hyperparameters

**Class**: `sweep.protein.Hyperparameters`

**Constructor**: `Hyperparameters(self, config, verbose = ...)`

**Methods**: 3

#### sample

**Signature**: `Hyperparameters.sample(self, n, mu = ..., scale = ...)`

**Location**: line 166

#### from_dict

**Signature**: `Hyperparameters.from_dict(self, params)`

**Location**: line 177

#### to_dict

**Signature**: `Hyperparameters.to_dict(self, sample, fill = ...)`

**Location**: line 187


### Protein

**Class**: `sweep.protein.Protein`

**Constructor**: `Protein(self, sweep_config, max_suggestion_cost = ..., resample_frequency = ..., num_random_samples = ..., global_search_scale = ..., random_suggestions = ..., suggestions_per_pareto = ..., seed_with_search_center = ..., expansion_rate = ..., acquisition_fn = ..., ucb_beta = ..., randomize_acquisition = ...)`

**Methods**: 2

#### suggest

**Signature**: `Protein.suggest(self, n_suggestions = ..., fill = ...)`

**Location**: line 299

#### observe

**Signature**: `Protein.observe(self, hypers, score, cost, is_failure = ...)`

**Location**: line 571


## Functions (3)

### pareto_points

**Signature**: `sweep.protein.pareto_points(observations, eps = ...)`

**Location**: line 205

### pareto_points_oriented

**Signature**: `sweep.protein.pareto_points_oriented(observations, direction = ..., eps = ...)`

**Documentation**: Compute Pareto front on (score, cost) with goal encoded by `direction`.
direction = +1 for maximize, -1 for minimize.

**Location**: line 210

### create_gp

**Signature**: `sweep.protein.create_gp(x_dim, scale_length = ...)`

**Location**: line 227

