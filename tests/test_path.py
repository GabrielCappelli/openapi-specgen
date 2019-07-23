from openapi_specgen import OpenApiParam, OpenApiPath, OpenApiResponse

from .utils import MarshmallowSchema


def test_path_with_params():
    expected_openapi_dict = {
        '/test_path': {
            'get': {
                'description': 'Test Description',
                'summary': 'Test Summary',
                'operationId': '[get]_/test_path',
                'responses': {
                    '200': {
                        'description': 'Test Response'
                    }
                },
                'parameters': [
                    {
                        'required': True,
                        'schema': {
                            'title': 'Test_Param',
                            'type': 'string'
                        },
                        'name': 'test_param',
                        'in': 'query'
                    }
                ]
            }
        }
    }
    openapi_path = OpenApiPath('/test_path',
                               'get',
                               [OpenApiResponse('Test Response')],
                               [OpenApiParam('test_param', 'query', str)],
                               'Test Description',
                               'Test Summary'
                               )
    assert expected_openapi_dict == openapi_path.as_dict()


def test_path_no_params():
    expected_openapi_dict = {
        '/test_path': {
            'get': {
                'description': 'Test Description',
                'summary': 'Test Summary',
                'operationId': '[get]_/test_path',
                'responses': {
                    '200': {
                        'description': 'Test Response'
                    }
                },
                'parameters': [
                ]
            }
        }
    }
    openapi_path = OpenApiPath('/test_path',
                               'get',
                               [OpenApiResponse('Test Response')],
                               descr='Test Description',
                               summary='Test Summary'
                               )
    assert expected_openapi_dict == openapi_path.as_dict()


def test_path_with_request_body():
    expected_openapi_dict = {
        '/test_path': {
            'post': {
                'description': 'Test Description',
                'summary': 'Test Summary',
                'operationId': '[post]_/test_path',
                'requestBody': {
                    'content': {
                        'application/json': {
                            'schema': {
                                '$ref': '#/components/schemas/MarshmallowSchema'
                            }
                        }
                    }
                },
                'responses': {
                    '200': {
                        'description': 'Test Response'
                    }
                },
                'parameters': [
                ]
            }
        }
    }
    openapi_path = OpenApiPath('/test_path',
                               'post',
                               [OpenApiResponse('Test Response')],
                               descr='Test Description',
                               summary='Test Summary',
                               request_body=MarshmallowSchema
                               )
    assert expected_openapi_dict == openapi_path.as_dict()
