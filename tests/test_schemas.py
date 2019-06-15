from typing import List

import pytest

from openapi_specgen.utils import get_openapi_schema

from .utils import DataclassObject


@pytest.mark.parametrize('data_type, openapi_schema', [
    (str, {'type': 'string'}),
    (int, {'type': 'integer'}),
    (float, {'type': 'number'}),
    (bool, {'type': 'boolean'}),
    (DataclassObject, {'$ref': '#/components/schemas/DataclassObject'}),
    (List, {'type': 'array', 'items': {}}),
    (List[DataclassObject], {'type': 'array', 'items': {'$ref': '#/components/schemas/DataclassObject'}}),
    (List[str], {'type': 'array', 'items': {'type': 'string'}}),
    (List[int], {'type': 'array', 'items': {'type': 'integer'}}),
    (List[float], {'type': 'array', 'items': {'type': 'number'}}),
    (List[bool], {'type': 'array', 'items': {'type': 'boolean'}})
])
def test_openapi_schema(data_type, openapi_schema):
    assert openapi_schema == get_openapi_schema(data_type)
