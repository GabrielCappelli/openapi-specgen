from dataclasses import fields
from typing import List

OPENAPI_TYPE_MAP = {
    str: "string",
    float: "number",
    int: "integer",
    bool: "boolean",
    list: "array",
    List: "array",
    List[str]: "array",
    List[float]: "array",
    List[int]: "array",
    List[bool]: "array"
}

OPENAPI_ARRAY_ITEM_MAP = {
    List[str]: "string",
    List[float]: "number",
    List[int]: "integer",
    List[bool]: "boolean",
    List: None
}


def get_openapi_type(data_type: type) -> str:
    return OPENAPI_TYPE_MAP.get(data_type, "object")


def get_openapi_list_generic_type(data_type: type) -> str:
    return OPENAPI_ARRAY_ITEM_MAP.get(data_type)


def get_openapi_array_schema(array_type: type) -> dict:
    openapi_array_type = get_openapi_list_generic_type(array_type)
    if openapi_array_type is None:
        return {
            'type': 'array',
            'items': {}
        }
    return {
        'type': 'array',
        'items': {
            'type': openapi_array_type
        }
    }


def get_openapi_schema(data_type: type, reference=True) -> dict:
    openapi_type = get_openapi_type(data_type)
    if openapi_type == 'object':
        if reference:
            return {
                '$ref': f'#/components/schemas/{data_type.__name__}'
            }
        return {
            data_type.__name__: {
                'title': data_type.__name__.title(),
                'required': [field.name for field in fields(data_type)],
                'type': 'object',
                'properties': {
                    field.name: {
                        'title': field.name.title(),
                        'type': get_openapi_type(field.type)
                    } for field in fields(data_type)
                }
            }
        }
    if openapi_type == 'array':
        return get_openapi_array_schema(data_type)
    return {'type': openapi_type}
