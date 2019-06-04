from .utils import get_openapi_list_generic_type, get_openapi_type


class OpenApiParam():

    def __init__(self,
                 name: str,
                 location: str,
                 data_type: type = None,
                 default=None,
                 required: bool = True):
        self.name = name
        self.location = location
        self.data_type = data_type
        self.default = default
        self.required = required

    def as_dict(self):

        openapi_dict = {
            'required': self.required,
            'name': self.name,
            'in': self.location
        }

        schema = {
            'title': self.name.title()
        }

        if self.default is not None:
            schema['default'] = self.default

        if self.data_type is not None:
            schema['type'] = get_openapi_type(self.data_type)
            if schema['type'] == 'array':
                array_type = get_openapi_list_generic_type(self.data_type)
                if array_type is not None:
                    schema['items'] = {'type': array_type}
                else:
                    schema['items'] = {}
        openapi_dict['schema'] = schema
        return openapi_dict
