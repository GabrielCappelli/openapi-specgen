from datetime import date, datetime
from typing import Any, Dict, List

import pytest

from openapi_specgen.schema import resolve_dataclass

from .utils import (DataclassNestedObject, DataclassObject,
                    MarshmallowNestedSchema, MarshmallowSchema)


@pytest.mark.parametrize('data_type, expected_schema', [
    (str, {'type': 'string'}),
    (date, {'type': 'string', 'format': 'date'}),
    (datetime, {'type': 'string', 'format': 'date-time'}),
    (int, {'type': 'integer'}),
    (float, {'type': 'number'}),
    (bool, {'type': 'boolean'}),
    (DataclassObject, {'$ref': '#/components/schemas/DataclassObject'}),
    (List, {'type': 'array', 'items': {}}),
    (
        List[DataclassObject],
        {'type': 'array', 'items': {'$ref': '#/components/schemas/DataclassObject'}}
    ),
    (List[str], {'type': 'array', 'items': {'type': 'string'}}),
    (List[int], {'type': 'array', 'items': {'type': 'integer'}}),
    (List[float], {'type': 'array', 'items': {'type': 'number'}}),
    (List[bool], {'type': 'array', 'items': {'type': 'boolean'}}),
    (Dict, {'type': 'object', 'additionalProperties': {}}),
    (
        Dict[str, DataclassObject],
        {'type': 'object', 'additionalProperties': {'$ref': '#/components/schemas/DataclassObject'}}
    ),
    (Dict[str, str], {'type': 'object', 'additionalProperties': {'type': 'string'}}),
    (Dict[str, int], {'type': 'object', 'additionalProperties': {'type': 'integer'}}),
    (Dict[str, float], {'type': 'object', 'additionalProperties': {'type': 'number'}}),
    (Dict[str, bool], {'type': 'object', 'additionalProperties': {'type': 'boolean'}})
])
def test_openapi_schema(data_type, expected_schema, openapi_schema_resolver):
    assert expected_schema == openapi_schema_resolver.get_schema(data_type)


def test_any(openapi_schema_resolver):
    expected_schema = {'$ref': '#/components/schemas/AnyValue'}
    assert expected_schema == openapi_schema_resolver.get_schema(Any)

    expected_components = {"AnyValue": {}}
    assert expected_components == openapi_schema_resolver.get_components()


def test_dataclass_schema(openapi_schema_resolver):
    expected_openapi_schema = {
        'DataclassObject': {
            'title': 'DataclassObject',
            'type': 'object',
            'required': ['str_field', 'int_field', 'float_field',
                         'boolean_field', 'list_field', 'date_field', 'datetime_field'],
            'properties': {
                'str_field': {'type': 'string'},
                'int_field': {'type': 'integer'},
                'float_field': {'type': 'number'},
                'boolean_field': {'type': 'boolean'},
                'list_field': {'type': 'array', 'items': {}},
                'date_field': {'type': 'string', 'format': 'date'},
                'datetime_field': {'type': 'string', 'format': 'date-time'},
            }
        }
    }
    openapi_schema_resolver.get_schema(DataclassObject)
    assert expected_openapi_schema == openapi_schema_resolver.get_components()


def test_dataclass_nested_objects(openapi_schema_resolver):
    expected_openapi_schema = {
        'DataclassNestedObject': {
            'title': 'DataclassNestedObject',
            'type': 'object',
            'required':
            [
                'str_field',
                'nested_object'
            ],
            'properties': {
                'str_field': {'type': 'string'},
                'nested_object': {'$ref': '#/components/schemas/DataclassObject'}
            }
        },
        'DataclassObject': {
            'title': 'DataclassObject',
            'required': ['str_field', 'int_field', 'float_field',
                         'boolean_field', 'list_field', 'date_field', 'datetime_field'],
            'type': 'object',
            'properties': {
                'str_field': {'type': 'string'},
                'int_field': {'type': 'integer'},
                'float_field': {'type': 'number'},
                'boolean_field': {'type': 'boolean'},
                'list_field': {'type': 'array', 'items': {}},
                'date_field': {'type': 'string', 'format': 'date'},
                'datetime_field': {'type': 'string', 'format': 'date-time'},
            }
        }
    }
    openapi_schema_resolver.get_schema(DataclassNestedObject)
    assert expected_openapi_schema == openapi_schema_resolver.get_components()


def test_marshmallow_schema(openapi_schema_resolver):
    expected_openapi_schema = {
        'Marshmallow': {
            'title': 'Marshmallow',
            'type': 'object',
            'required':
            [
                'str_field'
            ],
            'properties': {
                'str_field': {'type': 'string'},
                'int_field': {'type': 'integer'},
                'float_field': {'type': 'number'},
                'boolean_field': {'type': 'boolean'},
                'list_field': {'type': 'array', 'items': {'type': 'string'}},
                'date_field': {'type': 'string', 'format': 'date'},
                'datetime_field': {'type': 'string', 'format': 'date-time'},
            }
        }
    }
    openapi_schema_resolver.get_schema(MarshmallowSchema)
    assert expected_openapi_schema == openapi_schema_resolver.get_components()


def test_marshmallow_nested_schema(openapi_schema_resolver):
    expected_openapi_schema = {
        'Marshmallow': {
            'title': 'Marshmallow',
            'type': 'object',
            'required':
            [
                'str_field'
            ],
            'properties': {
                'str_field': {'type': 'string'},
                'int_field': {'type': 'integer'},
                'float_field': {'type': 'number'},
                'boolean_field': {'type': 'boolean'},
                'list_field': {'type': 'array', 'items': {'type': 'string'}},
                'date_field': {'type': 'string', 'format': 'date'},
                'datetime_field': {'type': 'string', 'format': 'date-time'},
            }
        },
        'MarshmallowNested': {
            'title': 'MarshmallowNested',
            'type': 'object',
            'required':
            [
                'str_field'
            ],
            'properties': {
                'str_field': {'type': 'string'},
                'int_field': {'type': 'integer'},
                'float_field': {'type': 'number'},
                'boolean_field': {'type': 'boolean'},
                'list_field': {'type': 'array', 'items': {'type': 'string'}},
                'nested_schema': {'$ref': '#/components/schemas/Marshmallow'},
                'self_reference': {'$ref': '#/components/schemas/MarshmallowNested'}
            }
        }
    }
    openapi_schema_resolver.get_schema(MarshmallowNestedSchema)
    assert expected_openapi_schema == openapi_schema_resolver.get_components()


def test_add_resolver(openapi_schema_resolver):

    class CustomType:
        pass

    def custom_type_resolver(openapi_schema_resolver, data_type):
        return {'type': 'foo'}

    openapi_schema_resolver.add_resolver(custom_type_resolver)
    assert {'type': 'foo'} == openapi_schema_resolver.get_schema(CustomType)


def test_remove_resolver(openapi_schema_resolver):
    openapi_schema_resolver.remove_resolver(resolve_dataclass)
    with pytest.raises(ValueError):
        openapi_schema_resolver.get_schema(DataclassObject)
