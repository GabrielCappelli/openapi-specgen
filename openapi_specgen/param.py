from .schema import get_openapi_schema


class OpenApiParam():
    '''Object to represent an OpenApi Param as defined on
    https://swagger.io/docs/specification/describing-parameters/
    '''

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
        '''
        Returns:
            dict: dict representing this object as a OpenApi Param.
        '''
        openapi_dict = {
            'required': self.required,
            'name': self.name,
            'in': self.location
        }

        schema = {}

        if self.data_type is not None:
            schema = get_openapi_schema(self.data_type)
        if self.default is not None:
            schema['default'] = self.default

        schema['title'] = self.name.title()
        openapi_dict['schema'] = schema
        return openapi_dict
