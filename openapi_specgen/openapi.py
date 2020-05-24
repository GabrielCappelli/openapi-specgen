from typing import List, Optional

from .path import OpenApiPath
from .schema import get_openapi_schema, get_openapi_type
from .security import OpenApiSecurity


class OpenApi():
    '''Object to represent an OpenApi specification as defined on
    https://swagger.io/docs/specification/about/

    Args:
        title (str): Title of your Api
        paths (List[OpenApiPath]): List of OpenApiPaths that are part of this Api
        security Optional[OpenApiSecurity]: Optional OpenApiSecurity defining authentication options for this Api
    '''
    version = '3.0.2'
    title = None
    paths = None
    security = None

    def __init__(self,
                 title: str,
                 paths: List[OpenApiPath],
                 security: Optional[OpenApiSecurity] = None):
        '''

        '''
        self.title = title
        self.paths = paths
        self.security = security

    def as_dict(self) -> dict:
        '''
        Returns:
            dict: dict representing this object as an OpenApi specification.
        '''
        openapi_dict = {
            'openapi': self.version,
            'info': {
                'title': self.title,
                'version': self.version
            },
            'paths': {
            },
            'components': {
                'schemas': {}
            }
        }
        for openapi_path in self.paths:
            if openapi_dict['paths'].get(openapi_path.path) is None:
                openapi_dict['paths'][openapi_path.path] = {}
            openapi_dict['paths'][openapi_path.path].update(
                openapi_path.as_dict()[openapi_path.path])

            if openapi_path.request_body:
                if get_openapi_type(openapi_path.request_body) == 'object':
                    openapi_dict['components']['schemas'].update(
                        get_openapi_schema(openapi_path.request_body, reference=False)
                    )

            for param in openapi_path.params:
                if get_openapi_type(param.data_type) == 'object':
                    openapi_dict['components']['schemas'].update(
                        get_openapi_schema(param.data_type, reference=False)
                    )

            for resp in openapi_path.responses:
                if get_openapi_type(resp.data_type) == 'object':
                    openapi_dict['components']['schemas'].update(
                        get_openapi_schema(resp.data_type, reference=False)
                    )
            if self.security:
                openapi_dict['security'] = self.security.get_security_reference()
                openapi_dict['components']['securitySchemes'] = self.security.as_dict()

        return openapi_dict
