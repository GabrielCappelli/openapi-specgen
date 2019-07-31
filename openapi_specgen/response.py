from .schema import get_openapi_schema


class OpenApiResponse():
    '''Object to represent an OpenApi Response as defined on
    https://swagger.io/docs/specification/describing-responses/

    Args:
        descr (str): A description for this response
        status_code (str, optional): HTTP code this response will return. Defaults to '200'.
        data_type (type, optional): Python type this response will return. Defaults to None.
        http_content_type (str, optional): HTTP MIME type of this response. Defaults to 'application/json'.
    '''

    def __init__(self,
                 descr: str,
                 status_code: str = '200',
                 data_type: type = None,
                 http_content_type: str = 'application/json'):

        self.descr = descr
        self.data_type = data_type
        self.status_code = status_code
        self.http_content_type = http_content_type

    def as_dict(self) -> dict:
        '''
        Returns:
            dict: dict representing this object as a OpenApi Response.
        '''
        openapi_dict = {
            self.status_code: {
                'description': self.descr
            }
        }

        if self.data_type is None:
            return openapi_dict

        openapi_dict[self.status_code]['content'] = {
            self.http_content_type: {
                'schema': get_openapi_schema(self.data_type)
            }
        }

        return openapi_dict
