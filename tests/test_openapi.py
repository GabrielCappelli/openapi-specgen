
from dataclasses import dataclass

from openapi_specgen import OpenApi, OpenApiParam, OpenApiPath, OpenApiResponse


@dataclass
class TestObj():
    int_field: int


def test_openapi():
    expected_openapi_dict = {
        'openapi': '3.0.2',
        'info': {
            'title': 'test_api',
            'version': '3.0.2'
        },
        'paths': {
            '/test_path': {
                'get': {
                    'description': '',
                    'summary': '',
                    'operationId': '[get]_/test_path',
                    'responses': {
                        '200': {
                            'description': 'test_response',
                            'content': {
                                'application/json': {
                                    'schema': {'$ref': '#/components/schemas/TestObj'}
                                }
                            }
                        }
                    },
                    'parameters': [
                        {
                            'required': True,
                            'name': 'test_param',
                            'in': 'query',
                            'schema': {
                                'title': 'Test_Param',
                                'type': 'string'
                            }
                        }
                    ]
                }
            }
        },
        'components': {
            'schemas': {
                'TestObj': {
                    'title': 'Testobj',
                    'required': ['int_field'],
                    'type': 'object',
                    'properties': {
                        'int_field': {
                            'title': 'Int_Field',
                            'type': 'integer'
                        }
                    }
                }
            }
        }
    }

    test_resp = OpenApiResponse('test_response', data_type=TestObj)
    test_param = OpenApiParam('test_param', 'query', data_type=str)
    test_path = OpenApiPath('/test_path', 'get', [test_resp], [test_param])
    test_api = OpenApi('test_api', [test_path])
    assert expected_openapi_dict == test_api.as_dict()
