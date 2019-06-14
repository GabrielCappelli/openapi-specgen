
from dataclasses import dataclass
from typing import List

from openapi_specgen import OpenApi, OpenApiParam, OpenApiPath, OpenApiResponse

from .utils import SimpleObject


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
                                    'schema': {'$ref': '#/components/schemas/SimpleObject'}
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
                'SimpleObject': {
                    'title': 'SimpleObject',
                    'required': ['str_field', 'int_field', 'float_field', 'boolean_field', 'list_field'],
                    'type': 'object',
                    'properties': {
                        'str_field': {
                            'title': 'Str_Field',
                            'type': 'string'
                        },
                        'int_field': {
                            'title': 'Int_Field',
                            'type': 'integer'
                        },
                        'float_field': {
                            'title': 'Float_Field',
                            'type': 'number'
                        },
                        'boolean_field': {
                            'title': 'Boolean_Field',
                            'type': 'boolean'
                        },
                        'list_field': {
                            'title': 'List_Field',
                            'type': 'array'
                        }
                    }
                }
            }
        }
    }

    test_resp = OpenApiResponse('test_response', data_type=SimpleObject)
    test_param = OpenApiParam('test_param', 'query', data_type=str)
    test_path = OpenApiPath('/test_path', 'get', [test_resp], [test_param])
    test_api = OpenApi('test_api', [test_path])
    assert expected_openapi_dict == test_api.as_dict()
