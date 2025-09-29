# gridworks.configs.lsp

**Module**: `gridworks.configs.lsp`

**Source**: `metta/gridworks/configs/lsp.py`

**Imports**:
- `contextlib`
- `json`
- `logging`
- `os`
- `pathlib`
- `queue`
- `subprocess`
- `threading`
- `time`
- `typing.IO`

## Classes (1)

### LSPClient

**Class**: `gridworks.configs.lsp.LSPClient`

**Constructor**: `LSPClient(self)`

**Documentation**: This class implements a simple LSP client.

There are some python libraries for LSP, but they either don't support pyright, or aren't very mature (lack
documentation, etc.).

**Methods**: 10

#### shutdown

**Signature**: `LSPClient.shutdown(self)`

**Location**: line 90

#### next_id

**Signature**: `LSPClient.next_id(self) -> int`

**Location**: line 97

#### send

**Signature**: `LSPClient.send(self, msg: dict)`

**Location**: line 101

#### send_with_id

**Signature**: `LSPClient.send_with_id(self, msg: dict)`

**Location**: line 107

#### recv_ids

**Signature**: `LSPClient.recv_ids(self, wanted_ids: list[int], timeout = ...) -> dict`

**Documentation**: Drain queue until we see all the wanted ids.

**Location**: line 112

#### recv_id

**Signature**: `LSPClient.recv_id(self, wanted_id: int, timeout = ...) -> dict`

**Location**: line 149

#### with_file

**Signature**: `LSPClient.with_file(self, file_path: Any)`

**Location**: line 153

#### get_file_symbols

**Signature**: `LSPClient.get_file_symbols(self, file_path: Any)`

**Location**: line 179

#### get_hover

**Signature**: `LSPClient.get_hover(self, file_path: Any, line: int, column: int)`

**Location**: line 193

#### get_hover_bulk

**Signature**: `LSPClient.get_hover_bulk(self, file_path: Any, positions: list[tuple])`

**Location**: line 207


