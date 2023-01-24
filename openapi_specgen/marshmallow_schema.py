'''Functions to help generate OpenApi Schemas from Marshmallow schemas'''
import inspect

import marshmallow


def get_openapi_schema_from_marshmallow_field(openapi_schema_resolver, marshmallow_field: marshmallow.fields.Field) -> dict:
    '''Returns openapi schema of marshmallow_field type

    Args:
        marshmallow_field (marshmallow.fields.Field): Any Field from a Marshmallow schema

    Returns:
        dict: openapi schema of the given field
    '''
    if isinstance(marshmallow_field, marshmallow.fields.Nested):
        return resolve_marshmallow(openapi_schema_resolver, type(marshmallow_field.schema))
    if isinstance(marshmallow_field, marshmallow.fields.String):
        return {'type': 'string'}
    if isinstance(marshmallow_field, marshmallow.fields.Boolean):
        return {'type': 'boolean'}
    if isinstance(marshmallow_field, marshmallow.fields.Integer):
        return {'type': 'integer'}
    if isinstance(marshmallow_field, marshmallow.fields.Float):
        return {'type': 'number'}
    if isinstance(marshmallow_field, marshmallow.fields.Date):
        return {'type': 'string', 'format': 'date'}
    if isinstance(marshmallow_field, marshmallow.fields.DateTime):
        return {'type': 'string', 'format': 'date-time'}
    if isinstance(marshmallow_field, marshmallow.fields.List):
        return {
            'type': 'array',
            'items': get_openapi_schema_from_marshmallow_field(openapi_schema_resolver, marshmallow_field.inner)
        }


def resolve_marshmallow(openapi_schema_resolver, data_type: type):
    '''Returns a dict representing the openapi schema of data_type.

    When referencing assumes objects will be defined in #/components/schemas/.
    Will strip trailing Schema from name.

    Args:
        openapi_schema: Then OpenApi schema that is calling this function
        data_type (type): A Marshmallow schema

    Returns:
        dict: [description]
    '''
    if isinstance(data_type, marshmallow.Schema):
        data_type = type(data_type)

    if not inspect.isclass(data_type) or not issubclass(data_type, marshmallow.Schema):
        return

    component_name = strip_schema_from_name(data_type.__name__)

    # Avoids infinite recursion on circular or self references
    if component_name in openapi_schema_resolver.get_components():
        return {"$ref": openapi_schema_resolver.get_component_ref(component_name)}

    component = {
        'title': component_name,
        'required': [name for name, field in data_type._declared_fields.items() if field.required],
        'type': 'object',
    }

    openapi_schema_resolver.add_component(component_name, component)

    # Must be set after we add the component to avoid infinite recursion
    # on circular or self references
    component["properties"] = {
        name: get_openapi_schema_from_marshmallow_field(openapi_schema_resolver, field)
        for name, field in data_type._declared_fields.items()
    }

    return {"$ref": openapi_schema_resolver.get_component_ref(component_name)}


def strip_schema_from_name(name: str) -> str:
    return name[:-6] if name.endswith('Schema') else name
