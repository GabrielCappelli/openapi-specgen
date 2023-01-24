[![Test](https://github.com/GabrielCappelli/openapi-specgen/actions/workflows/test.yml/badge.svg)](https://github.com/GabrielCappelli/openapi-specgen/actions/workflows/test.yml)

# openapi-specgen
Openapi-Specgen helps you generate [OpenApi specification](https://swagger.io/docs/specification/about/) from your python code.

Includes support for automatically generating OpenApi schemas for Dataclasses and Marshamllow Schemas.

# Installation

Install using pip

```pip install openapi-specgen```

# Quick Start

Define your objects using dataclasses or marshmallow schemas.
Import the required OpenApi classes and define your Api with it`s paths, params and responses.

```python
from typing import List
from dataclasses import dataclass

@dataclass
class DataclassObject():
    str_field: str
    int_field: int
    float_field: float
    boolean_field: bool
    list_field: List[str]

from openapi_specgen import OpenApi, OpenApiParam, OpenApiPath, OpenApiResponse

sample_response = OpenApiResponse('Response description', data_type=DataclassObject)
sample_param = OpenApiParam('param_name', 'query', data_type=str)
sample_path = OpenApiPath('/api_path', 'get', [sample_response], [sample_param])

sample_api = OpenApi('Sample Api', [sample_path, marshmallow_path])

sample_api.as_dict()
```

# Adding custom type resolvers

The following code snippet expands on the quick start example to show you how to add custom resolvers for any other types.

```python

# Create a func with the following signature:
def custom_resolver(openapi_schema_resolver, data_type):
    # Resolver must return None if it cannot resolve the data_type
    if data_type is not CustomType:
        return

    # For simple types the schema can be returned now, e.g
    # return {"type": "string", "format": "byte"}

    # Optionally for objects we can use a reference using the following syntax

    # Register the actual component
    component_name = "CustomType"
    openapi_schema_resolver.add_component(
        component_name,
        {
            "title": component_name,
            "type": "object",
            "required": ["foo"],
            "properties": {
                # use openapi_schema_resolver.get_schema
                # to recursively resolve other schemas
                "foo": openapi_schema_resolver.get_schema(int)
            }
        }
    )

    # Return the reference
    return {'$ref': openapi_schema_resolver.get_component_ref(component_name)}

# Register your func on your OpenApi instance
test_api.add_resolver(custom_resolver)
```

# License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
