from typing import List

from .param import OpenApiParam
from .response import OpenApiResponse
from .schema import get_openapi_schema


class OpenApiPath():
    '''Object to represent an OpenApi Path as defined on
    https://swagger.io/docs/specification/paths-and-operations/

    Args:
        path (str): HTTP Path of this api operation, e.g /test. Must start with /.
        method (str): HTTP method for this path
        responses (List[OpenApiResponse]): List of all possible OpenApiResponse
        params (List[OpenApiParam], optional): List of any OpenApiParams. Defaults to [].
        descr (str, optional): Description of this API operation. Defaults to ''.
        summary (str, optional): Summary of this API operation. Defaults to ''.
        request_body ([type], optional): Python type expected in request body. Defaults to None.
    '''

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
        '''Returns a dict representing this object as a OpenApi Path.

        Returns:
            dict: dict representing this object as a OpenApi Path.
        '''
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




