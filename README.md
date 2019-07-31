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


marshmallow_response = OpenApiResponse('Response description', data_type=MarshmallowSchema)
marshmallow_path = OpenApiPath('/api_path', 'post', [sample_response], requestBody=MarshmallowSchema)

sample_api = OpenApi('Sample Api', [sample_path, marshmallow_path])

sample_api.as_dict()
```

# License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
