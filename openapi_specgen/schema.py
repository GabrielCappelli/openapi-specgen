'''Functions to help generate OpenApi Schemas as defined on
https://swagger.io/docs/specification/data-models/
'''
import dataclasses
import datetime
import inspect
import typing

from openapi_specgen.marshmallow_schema import resolve_marshmallow

OPENAPI_TYPE_MAP: typing.Dict[type, str] = {
    str: "string",
    datetime.date: "string",
    datetime.datetime: "string",
    float: "number",
    int: "integer",
    bool: "boolean",
}

OPENAPI_FORMAT_MAP: typing.Dict[type, str] = {
    datetime.date: "date",
    datetime.datetime: "date-time",
}


def resolve_basic(openapi_schema_resolver: "OpenApiSchemaResolver", data_type: type):
    openapi_type = OPENAPI_TYPE_MAP.get(data_type)
    openapi_format = OPENAPI_FORMAT_MAP.get(data_type)

    if openapi_type and openapi_format:
        return {"type": openapi_type, "format": openapi_format}

    if openapi_type:
        return {"type": openapi_type}


def resolve_array(openapi_schema_resolver: "OpenApiSchemaResolver", data_type: type):
    items = typing.get_args(data_type)
    data_type = typing.get_origin(data_type) or data_type

    if not inspect.isclass(data_type) or not issubclass(data_type, typing.Iterable):
        return

    if items:
        return {"type": "array", "items": openapi_schema_resolver.get_schema(items[0])}
    return {"type": "array", "items": {}}


def resolve_dataclass(openapi_schema_resolver: "OpenApiSchemaResolver", data_type: type):

    if not dataclasses.is_dataclass(data_type):
        return

    component_name = data_type.__name__

    openapi_schema_resolver.add_component(
        component_name,
        {
            'title': component_name,
            'required': [field.name for field in dataclasses.fields(data_type)],
            'type': 'object',
            'properties': {
                field.name: openapi_schema_resolver.get_schema(field.type) for field in dataclasses.fields(data_type)
            }
        }
    )

    return {'$ref': openapi_schema_resolver.get_component_ref(component_name)}


class OpenApiSchemaResolver:
    """
    Resolve python types into OpenApi schemas
    """

    def __init__(self) -> None:
        self.resolvers = [
            resolve_basic,
            resolve_array,
            resolve_dataclass,
            resolve_marshmallow,
        ]
        self.components = {}

    def get_schema(self, data_type: type) -> typing.Dict[str, typing.Any]:
        for resolver in self.resolvers:
            if result := resolver(self, data_type):
                return result
        raise ValueError(f"Cannot resolve OpenApi schema for {data_type}")

    def get_component_ref(self, component_name: str) -> str:
        return f'#/components/schemas/{component_name}'

    def add_component(self, component_name: str, component_dict: typing.Dict[str, typing.Any]):
        self.components[component_name] = component_dict

    def get_components(self) -> typing.Dict[str, typing.Any]:
        return self.components
