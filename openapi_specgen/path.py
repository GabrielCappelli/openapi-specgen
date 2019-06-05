from typing import List

from .param import OpenApiParam
from .response import OpenApiResponse


class OpenApiPath():

    def __init__(self,
                 path: str,
                 method: str,
                 responses: List[OpenApiResponse],
                 params: List[OpenApiParam] = [],
                 descr: str = '',
                 summary: str = '',
                 ):
        self.path = path
        self.method = method
        self.responses = responses
        self.params = params
        self.summary = summary
        self.descr = descr

    def as_dict(self):
        return {
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
