# setup.tools.local.kind

**Module**: `setup.tools.local.kind`

**Source**: `metta/setup/tools/local/kind.py`

**Imports**:
- `devops.docker.push_image.push_image`
- `metta.app_backend.clients.base_client.get_machine_token`
- `metta.common.util.constants.DEV_STATS_SERVER_URI`
- `metta.common.util.constants.METTA_AWS_ACCOUNT_ID`
- `metta.common.util.constants.METTA_AWS_REGION`
- `metta.common.util.fs.get_repo_root`
- `metta.setup.utils.error`
- `metta.setup.utils.info`
- `metta.setup.utils.success`
- `pathlib.Path`
- `rich.console.Console`
- `subprocess`
- `sys`
- `typer`
- `typing.Annotated`
- `typing.Callable`

## Classes (3)

### Kind

**Class**: `setup.tools.local.kind.Kind`

**Constructor**: `Kind()`

**Methods**: 7

#### build

**Signature**: `Kind.build(self) -> Any`

**Location**: line 63

#### up

**Signature**: `Kind.up(self) -> Any`

**Documentation**: Start orchestrator in Kind cluster using Helm.

**Location**: line 69

#### down

**Signature**: `Kind.down(self) -> Any`

**Documentation**: Stop orchestrator and worker pods.

**Location**: line 104

#### clean

**Signature**: `Kind.clean(self) -> Any`

**Documentation**: Delete the Kind cluster.

**Location**: line 120

#### get_pods

**Signature**: `Kind.get_pods(self) -> Any`

**Documentation**: Get list of pods in the cluster.

**Location**: line 127

#### logs

**Signature**: `Kind.logs(self, pod_name: Any = ...) -> Any`

**Documentation**: Follow logs for orchestrator or specific pod.

**Location**: line 132

#### enter

**Signature**: `Kind.enter(self, pod_name: Any = ...) -> Any`

**Documentation**: Enter orchestrator or specific pod with an interactive shell.

**Location**: line 144


### KindLocal

**Class**: `setup.tools.local.kind.KindLocal`

**Constructor**: `KindLocal()`

**Methods**: 1

#### build

**Signature**: `KindLocal.build(self) -> Any`

**Location**: line 201


### EksProd

**Class**: `setup.tools.local.kind.EksProd`

**Constructor**: `EksProd()`

**Methods**: 1

#### build

**Signature**: `EksProd.build(self)`

**Location**: line 236


## Functions (8)

### cmd_build

**Signature**: `setup.tools.local.kind.cmd_build()`

**Location**: line 260

### cmd_up

**Signature**: `setup.tools.local.kind.cmd_up()`

**Location**: line 266

### cmd_down

**Signature**: `setup.tools.local.kind.cmd_down()`

**Location**: line 272

### cmd_clean

**Signature**: `setup.tools.local.kind.cmd_clean()`

**Location**: line 278

### cmd_get_pods

**Signature**: `setup.tools.local.kind.cmd_get_pods()`

**Location**: line 284

### cmd_logs

**Signature**: `setup.tools.local.kind.cmd_logs(pod_name: Annotated = ...)`

**Location**: line 289

### cmd_enter

**Signature**: `setup.tools.local.kind.cmd_enter(pod_name: Annotated = ...)`

**Location**: line 294

### main

**Signature**: `setup.tools.local.kind.main()`

**Location**: line 298

