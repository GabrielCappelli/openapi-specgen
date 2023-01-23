import pytest

from openapi_specgen.schema import OpenApiSchemaResolver


@pytest.fixture
def openapi_schema_resolver():
    return OpenApiSchemaResolver()
