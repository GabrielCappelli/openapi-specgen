
from dataclasses import dataclass
from typing import List, Optional


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
            'in': self.in_location,
            'name': self.name
        }


@dataclass
class OpenApiSecurity:
    basic_auth: Optional[BasicAuth] = None
    bearer_auth:  Optional[BearerAuth] = None
    api_key_auth:  Optional[ApiKeyAuth] = None

    def as_dict(self):
        auth_options = {}
        self._add_if_defined(auth_options, self.basic_auth, 'BasicAuth')
        self._add_if_defined(auth_options, self.bearer_auth, 'BearerAuth')
        self._add_if_defined(auth_options, self.api_key_auth, 'ApiKeyAuth')

        return auth_options

    def get_security_reference(self):
        '''Returns reference to configured openapi schemas
        '''
        auth_ref = []
        self._append_ref_if_defined(auth_ref, self.api_key_auth, 'ApiKeyAuth')
        self._append_ref_if_defined(auth_ref, self.basic_auth, 'BasicAuth')
        self._append_ref_if_defined(auth_ref, self.bearer_auth, 'BearerAuth')
        return auth_ref

    def _append_ref_if_defined(self, auth_ref, prop, key):
        if prop:
            auth_ref.append({key: []})

    def _add_if_defined(self, auth_options, prop, key):
        if prop:
            auth_options[key] = prop.as_dict()
