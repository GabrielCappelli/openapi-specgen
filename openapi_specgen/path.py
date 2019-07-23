from typing import List

from .param import OpenApiParam
from .response import OpenApiResponse
from .schema import get_openapi_schema


class OpenApiPath():

    def __init__(self,
                 path: str,
                 method: str,
                 responses: List[OpenApiResponse],
                 params: List[OpenApiParam] = [],
                 descr: str = '',
                 summary: str = '',
                 request_body=None,
                 ):
        self.path = path
        self.method = method
        self.responses = responses
        self.params = params
        self.summary = summary
        self.descr = descr
        self.request_body = request_body

    def as_dict(self):
        openapi_dict = {
            self.path: {
                self.method: {
                    'description': self.descr,
                    'summary': self.summary,
                    'operationId': f'[{self.method}]_{self.path}',
                    'responses': {
                        k: v for response in self.responses for k, v in response.as_dict().items()
                    },
                    'parameters': [
                        param.as_dict() for param in self.params
                    ]
                }
            }
        }
        if self.request_body is not None:
            openapi_dict[self.path][self.method]['requestBody'] = {
                'content': {
                    'application/json': {
                        'schema': get_openapi_schema(self.request_body)
                    }
                }
            }
        return openapi_dict
