import marshmallow


def get_openapi_schema_from_marshmallow_field(marshmallow_field: marshmallow.fields.Field) -> dict:

    if isinstance(marshmallow_field, marshmallow.fields.Nested):
        if isinstance(marshmallow_field.nested, str):
            return {'$ref': f'#/components/schemas/{strip_schema_from_name(marshmallow_field.nested)}'}
        else:
            return {'$ref': f'#/components/schemas/{strip_schema_from_name(marshmallow_field.nested.__name__)}'}
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


def get_openapi_schema_from_mashmallow_schema(data_type: type, reference=True) -> dict:
    class_name = strip_schema_from_name(data_type.__name__)
    if reference:
        return {'$ref': f'#/components/schemas/{class_name}'}
    if issubclass(data_type, marshmallow.Schema):
        openapi_schema = {
            class_name: {
                'title': class_name,
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
                if strip_schema_from_name(nested_schema.__name__) not in openapi_schema.keys():
                    openapi_schema.update(get_openapi_schema_from_mashmallow_schema(
                        nested_schema, reference=reference))
        return openapi_schema


def strip_schema_from_name(name: str) -> str:
    return name[:-6] if name.endswith('Schema') else name
