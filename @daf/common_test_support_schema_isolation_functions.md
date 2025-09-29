# common.test_support.schema_isolation_functions

**Module**: `common.test_support.schema_isolation_functions`

**Source**: `metta/common/test_support/schema_isolation_functions.py`

**Imports**:
- `psycopg`
- `urllib.parse.quote`
- `urllib.parse.urlparse`
- `urllib.parse.urlunparse`
- `uuid`

## Functions (2)

### create_isolated_schema_uri

**Signature**: `common.test_support.schema_isolation_functions.create_isolated_schema_uri(base_uri: str, schema_name: str) -> str`

**Documentation**: Create a database URI with a specific schema in the search path.

**Location**: line 7

### isolated_test_schema_uri

**Signature**: `common.test_support.schema_isolation_functions.isolated_test_schema_uri(base_uri: str) -> str`

**Documentation**: Create an isolated schema for testing.

Returns the database URI configured to use the isolated schema.

**Location**: line 25

