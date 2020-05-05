'''Functions to help generate OpenApi Schemas as defined on
https://swagger.io/docs/specification/data-models/
'''
import dataclasses
from datetime import date, datetime
from typing import List, TypeVar, _GenericAlias

import marshmallow

from .marshmallow_schema import get_openapi_schema_from_mashmallow_schema

OPENAPI_TYPE_MAP = {
    str: "string",
    date: "string",
    datetime: "string",
    float: "number",
    int: "integer",
    bool: "boolean",
    list: "array",
}

OPENAPI_FORMAT_MAP = {
    date: "date",
    datetime: "date-time",
}

OPENAPI_ARRAY_ITEM_MAP = {
    List[str]: "string",
    List[float]: "number",
    List[int]: "integer",
    List[bool]: "boolean",
    List: None
}


def get_openapi_array_schema(array_type: type) -> dict:
    '''Returns openapi schema of an array

    Use List[T] to specify the type of items in the list

    Args:
        array_type (type): The type list or List[T]

    Returns:
        dict: openapi schema of an array
    '''
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


def get_openapi_schema(data_type: type, reference=True) -> dict:
    '''Returns a dict representing the openapi schema of data_type.

    When referencing assumes objects will be defined in #/components/schemas/.

    Args:
        data_type (type): Any Python type
        reference (bool, optional): If true returns only a reference to objects. Defaults to True.

    Returns:
        dict: dict representing the openapi schema of data_type
    '''
    openapi_type = get_openapi_type(data_type)
    if openapi_type == 'object':
        if issubclass(data_type, marshmallow.Schema):
            return get_openapi_schema_from_mashmallow_schema(data_type, reference=reference)
        if reference:
            return {'$ref': f'#/components/schemas/{data_type.__name__}'}
        if dataclasses.is_dataclass(data_type):
            return get_openapi_schema_from_dataclass(data_type)

    if openapi_type == 'array':
        return get_openapi_array_schema(data_type)

    openapi_format = get_openapi_format(data_type)
    if openapi_format:
        return {'type': openapi_type, 'format': openapi_format}
    return {'type': openapi_type}


def get_openapi_schema_from_dataclass(data_type: type) -> dict:
    '''Returns a dict representing the openapi schema of the dataclass data_type.

    Assumes all fields declared by this dataclass are required.

    Args:
        data_type (type): Any dataclass

    Returns:
        dict: A dict representing this dataclass as a openapi schema
    '''
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


def get_openapi_type(data_type: type) -> str:
    '''Returns data_type`s openapi type equivalent.

    Args:
        data_type (type): Any python type

    Returns:
        str: String representation of openapi type
    '''
    if isinstance(data_type, _GenericAlias):
        if data_type.__origin__ == list:
            return "array"

    return OPENAPI_TYPE_MAP.get(data_type, "object")


def get_openapi_format(data_type: type) -> str:
    '''Returns the openapi format for this type.
    More information on https://swagger.io/docs/specification/data-models/data-types/#format

    Args:
        data_type (type): Any python type

    Returns:
        str: OpenApi format as a string, None if there isnt any
    '''
    return OPENAPI_FORMAT_MAP.get(data_type)
