from typing import List, Optional

from openapi_specgen.schema import OpenApiSchemaResolver, ResolverProto

from .path import OpenApiPath
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
                 security: Optional[OpenApiSecurity] = None,
                 schema_resolver: Optional[OpenApiSchemaResolver] = None,
                 ):
        '''

        '''
        self.title = title
        self.paths = paths
        self.security = security
        self.openapi_schema_resolver = schema_resolver or OpenApiSchemaResolver()

    def add_resolver(self, resolver: ResolverProto):
        self.openapi_schema_resolver.add_resolver(resolver)

    def remove_resolver(self, resolver: ResolverProto):
        self.openapi_schema_resolver.remove_resolver(resolver)

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
                openapi_path.as_dict(self.openapi_schema_resolver)[openapi_path.path])

        openapi_dict['components']['schemas'] = self.openapi_schema_resolver.get_components()

        if self.security:
            openapi_dict['security'] = self.security.get_security_reference()
            openapi_dict['components']['securitySchemes'] = self.security.as_dict()

        return openapi_dict
