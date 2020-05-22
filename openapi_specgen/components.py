
from typing import List, Union
from dataclasses import dataclass

@dataclass
class BasicAuth:
    protocol_type = "http"
    scheme = "basic"
    def as_dict(self):
        return {
            'type': self.protocol_type,
            'scheme': self.scheme
        }

@dataclass
class BearerAuth:
    protocol_type = "http"
    scheme = "bearer"
    def as_dict(self):
        return {
            'type': self.protocol_type,
            'scheme': self.scheme
        }

@dataclass
class ApiKeyAuth:
    protocol_type = "apiKey"
    in_location = "header"
    name = "X-API-Key"
    def as_dict(self):
        return {
            'type': self.protocol_type,
            ' in': self.in_location,
            'name': self.name
        }

SecuritySchema = Union[BasicAuth, BearerAuth, ApiKeyAuth]


class ComponentSet:
    '''Object to represent an OpenApi Path as defined on https://swagger.io/docs/specification/components/

     '''
    def __init__(self, security_schemes: List[SecuritySchema]):
        self.security_schemes = security_schemes
        self.schemas = {}


    def as_dict(self):
        '''Returns a dict representing this object as a OpenApi Components.
        '''
        openapi_dict = {
            'schemas' : self.schemas,
            'securitySchemes' : [
                schema.as_dict() for schema in self.security_schemes
            ]
        }
        return openapi_dict