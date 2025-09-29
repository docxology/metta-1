# utils.file

**Module**: `utils.file`

**Source**: `metta/utils/file.py`

**Imports**:
- `__future__.annotations`
- `boto3`
- `botocore.exceptions.ClientError`
- `botocore.exceptions.NoCredentialsError`
- `contextlib.contextmanager`
- `logging`
- `metta.utils.uri.ParsedURI`
- `os`
- `pathlib.Path`
- `shutil`
- `tempfile`
- `typing.Union`
- `urllib.parse.urlparse`

## Functions (7)

### exists

**Signature**: `utils.file.exists(path: str) -> bool`

**Documentation**: Return *True* if *path* points to an existing local file or S3 object.
Network errors are propagated so callers can decide how to handle them.

**Location**: line 28

### write_data

**Signature**: `utils.file.write_data(path: str, data: Union) -> Any`

**Documentation**: Write in-memory bytes/str to *local*, *s3://* destinations.

**Location**: line 55

### write_file

**Signature**: `utils.file.write_file(path: str, local_file: str) -> Any`

**Documentation**: Upload a file from disk to *s3://*, or copy locally.

**Location**: line 84

### read

**Signature**: `utils.file.read(path: str) -> bytes`

**Documentation**: Read bytes from a local path or S3 object.

**Location**: line 106

### local_copy

**Signature**: `utils.file.local_copy(path: str)`

**Documentation**: Yield a local *Path* for *path* (supports local paths and *s3://* URIs).

• Local paths are yielded as-is.
• Remote S3 URIs are streamed into a NamedTemporaryFile that is removed
  when the context exits, so callers never worry about cleanup.

Usage:
    with local_copy(uri) as p:
        do_something_with(Path(p))

**Location**: line 131

### http_url

**Signature**: `utils.file.http_url(path: str) -> str`

**Documentation**: Convert *s3://* URIs to a public browser URL.

**Location**: line 162

### is_public_uri

**Signature**: `utils.file.is_public_uri(url: Any) -> bool`

**Documentation**: Check if a URL is a public HTTP/HTTPS URL.

**Location**: line 170

