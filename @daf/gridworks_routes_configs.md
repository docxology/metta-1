# gridworks.routes.configs

**Module**: `gridworks.routes.configs`

**Source**: `metta/gridworks/routes/configs.py`

**Imports**:
- `fastapi.APIRouter`
- `fastapi.HTTPException`
- `logging`
- `metta.cogworks.curriculum.curriculum.CurriculumConfig`
- `metta.gridworks.common.ErrorResult`
- `metta.gridworks.common.dump_config_with_implicit_info`
- `metta.gridworks.configs.registry.ConfigMaker`
- `metta.gridworks.configs.registry.ConfigMakerKind`
- `metta.gridworks.configs.registry.ConfigMakerRegistry`
- `metta.sim.simulation_config.SimulationConfig`
- `metta.tools.play.PlayTool`
- `metta.tools.replay.ReplayTool`
- `metta.tools.sim.SimTool`
- `metta.tools.train.TrainTool`
- `mettagrid.config.Config`
- `mettagrid.config.MettaGridConfig`
- `mettagrid.map_builder.map_builder.AnyMapBuilderConfig`
- `mettagrid.mapgen.utils.storable_map.StorableMap`
- `mettagrid.mapgen.utils.storable_map.StorableMapDict`

## Functions (1)

### make_configs_router

**Signature**: `gridworks.routes.configs.make_configs_router() -> APIRouter`

**Location**: line 20

