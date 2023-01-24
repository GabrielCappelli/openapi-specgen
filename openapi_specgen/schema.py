'''Functions to help generate OpenApi Schemas as defined on
https://swagger.io/docs/specification/data-models/
'''
import dataclasses
import datetime
import inspect
import typing

try:
    from openapi_specgen.marshmallow_schema import resolve_marshmallow
except ImportError:
    resolve_marshmallow = None

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

    if not inspect.isclass(data_type) or not issubclass(data_type, typing.Sequence):
        return

    if items:
        return {"type": "array", "items": openapi_schema_resolver.get_schema(items[0])}
    return {"type": "array", "items": {}}


def resolve_mapping(openapi_schema_resolver: "OpenApiSchemaResolver", data_type: type):
    items = typing.get_args(data_type)
    data_type = typing.get_origin(data_type) or data_type

    if not inspect.isclass(data_type) or not issubclass(data_type, typing.Mapping):
        return

    if items:
        return {"type": "object", "additionalProperties": openapi_schema_resolver.get_schema(items[1])}
    return {"type": "object", "additionalProperties": {}}


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


def resolve_any(openapi_schema_resolver: "OpenApiSchemaResolver", data_type: type):
    if data_type is not typing.Any:
        return

    openapi_schema_resolver.add_component(
        "AnyValue",
        {}
    )

    return {"$ref": openapi_schema_resolver.get_component_ref("AnyValue")}


class ResolverProto(typing.Protocol):

    def __call__(
        self,
        openapi_schema_resolver: "OpenApiSchemaResolver",
        data_type: type
    ) -> typing.Union[typing.Dict[str, typing.Any], None]:
        ...


class OpenApiSchemaResolver:
    """
    Resolve python types into OpenApi schemas
    """

    def __init__(self) -> None:
        self._resolvers: typing.List[ResolverProto] = [
            resolve_basic,
            resolve_array,
            resolve_mapping,
            resolve_dataclass,
            resolve_any,
        ]
        if resolve_marshmallow is not None:
            self.add_resolver(resolve_marshmallow)
        self._components = {}

    def get_schema(self, data_type: type) -> typing.Dict[str, typing.Any]:
        for resolver in self._resolvers:
            if result := resolver(self, data_type):
                return result
        raise ValueError(f"Cannot resolve OpenApi schema for {data_type}")

    def get_component_ref(self, component_name: str) -> str:
        return f'#/components/schemas/{component_name}'

    def add_component(self, component_name: str, component_dict: typing.Dict[str, typing.Any]):
        self._components[component_name] = component_dict

    def get_components(self) -> typing.Dict[str, typing.Any]:
        return self._components

    def add_resolver(self, resolver: ResolverProto):
        self._resolvers.append(resolver)

    def remove_resolver(self, resolver: ResolverProto):
        self._resolvers.remove(resolver)
