# utils.uri

**Module**: `utils.uri`

**Source**: `metta/utils/uri.py`

**Imports**:
- `__future__.annotations`
- `dataclasses.dataclass`
- `pathlib.Path`
- `typing.Optional`
- `urllib.parse.unquote`
- `urllib.parse.urlparse`

## Classes (1)

### ParsedURI

**Class**: `utils.uri.ParsedURI`

**Constructor**: `ParsedURI()`

**Documentation**: Canonical representation for supported URI schemes.

**Methods**: 5

#### canonical

**Signature**: `ParsedURI.canonical(self) -> str`

**Documentation**: Return a normalized string representation.

**Location**: line 26

#### require_local_path

**Signature**: `ParsedURI.require_local_path(self) -> Path`

**Location**: line 36

#### require_s3

**Signature**: `ParsedURI.require_s3(self) -> tuple`

**Location**: line 41

#### is_remote

**Signature**: `ParsedURI.is_remote(self) -> bool`

**Documentation**: Return True if the URI references a remote resource.

**Location**: line 46

#### parse

**Signature**: `ParsedURI.parse(cls, value: str) -> Any`

**Location**: line 51


