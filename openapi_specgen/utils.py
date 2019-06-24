import dataclasses
from typing import List, TypeVar, _GenericAlias

import marshmallow

OPENAPI_TYPE_MAP = {
    str: "string",
    float: "number",
    int: "integer",
    bool: "boolean",
    list: "array",
}

OPENAPI_ARRAY_ITEM_MAP = {
    List[str]: "string",
    List[float]: "number",
    List[int]: "integer",
    List[bool]: "boolean",
    List: None
}


def get_openapi_type(data_type: type) -> str:
    if isinstance(data_type, _GenericAlias):
        if data_type.__origin__ == list:
            return "array"

    return OPENAPI_TYPE_MAP.get(data_type, "object")


def get_openapi_array_schema(array_type: type) -> dict:

    item_type = None
    if isinstance(array_type, _GenericAlias):
        item_type = array_type.__args__[0]

    if item_type is None or isinstance(item_type, TypeVar):
        return {
            'type': 'array',
            'items': {}
        }
    return {
        'type': 'array',
        'items': get_openapi_schema(item_type)
    }


def get_openapi_schema_from_dataclass(data_type: type) -> dict:
    openapi_schema = {
        data_type.__name__: {
            'title': data_type.__name__,
            'required': [field.name for field in dataclasses.fields(data_type)],
            'type': 'object',
            'properties': {
                field.name: get_openapi_schema(field.type) for field in dataclasses.fields(data_type)
            }
        }
    }
    for field in dataclasses.fields(data_type):
        if get_openapi_type(field.type) == 'object':
            openapi_schema.update(get_openapi_schema(field.type, reference=False))
    return openapi_schema


def get_openapi_schema_from_marshmallow_field(marshmallow_field: marshmallow.fields.Field) -> dict:

    if isinstance(marshmallow_field, marshmallow.fields.Nested):
        if isinstance(marshmallow_field.nested, str):
            return {'$ref': f'#/components/schemas/{marshmallow_field.nested}'}
        else:
            return {'$ref': f'#/components/schemas/{marshmallow_field.nested.__name__}'}
    if isinstance(marshmallow_field, marshmallow.fields.String):
        return {'type': 'string'}
    if isinstance(marshmallow_field, marshmallow.fields.Boolean):
        return {'type': 'boolean'}
    if isinstance(marshmallow_field, marshmallow.fields.Integer):
        return {'type': 'integer'}
    if isinstance(marshmallow_field, marshmallow.fields.Float):
        return {'type': 'number'}
    if isinstance(marshmallow_field, marshmallow.fields.List):
        return {
            'type': 'array',
            'items': get_openapi_schema_from_marshmallow_field(marshmallow_field.container)
        }


def get_openapi_schema_from_mashmallow_schema(data_type: type) -> dict:
    if issubclass(data_type, marshmallow.Schema):
        openapi_schema = {
            data_type.__name__: {
                'title': data_type.__name__,
                'required': [name for name, field in data_type._declared_fields.items() if field.required],
                'type': 'object',
                'properties': {
                    name: get_openapi_schema_from_marshmallow_field(field) for name, field in data_type._declared_fields.items()
                }
            }
        }
        for _, field in data_type._declared_fields.items():
            if isinstance(field, marshmallow.fields.Nested):
                nested_schema = field.nested
                if isinstance(nested_schema, str):
                    nested_schema = marshmallow.class_registry.get_class(nested_schema)
                if nested_schema.__name__ not in openapi_schema.keys():
                    openapi_schema.update(get_openapi_schema_from_mashmallow_schema(nested_schema))
        return openapi_schema


def get_openapi_schema(data_type: type, reference=True) -> dict:
    openapi_type = get_openapi_type(data_type)
    if openapi_type == 'object':
        if reference:
            return {'$ref': f'#/components/schemas/{data_type.__name__}'}
        if dataclasses.is_dataclass(data_type):
            return get_openapi_schema_from_dataclass(data_type)
        if issubclass(data_type, marshmallow.Schema):
            return get_openapi_schema_from_mashmallow_schema(data_type)
    if openapi_type == 'array':
        return get_openapi_array_schema(data_type)
    return {'type': openapi_type}
