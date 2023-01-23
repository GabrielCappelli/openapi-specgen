import pytest

from openapi_specgen import OpenApiResponse

from .utils import DataclassObject


def test_response_primitive(openapi_schema_resolver):
    expected_openapi_dict = {
        '200': {
            'description': 'Test Response',
            'content': {
                'application/json': {
                    'schema': {
                        'type': 'string'
                    }
                }
            }
        }
    }
    openapi_response = OpenApiResponse('Test Response', data_type=str)
    assert expected_openapi_dict == openapi_response.as_dict(openapi_schema_resolver)


def test_response_object(openapi_schema_resolver):
    expected_openapi_dict = {
        '200': {
            'description': 'Test Response',
            'content': {
                'application/json': {
                    'schema':
                    {
                        '$ref': '#/components/schemas/DataclassObject'
                    }
                }
            }
        }
    }
    openapi_response = OpenApiResponse('Test Response', data_type=DataclassObject)
    assert expected_openapi_dict == openapi_response.as_dict(openapi_schema_resolver)


def test_response_empty(openapi_schema_resolver):
    expected_openapi_dict = {
        '201': {
            'description': 'Test Empty Response'
        }
    }
    openapi_response = OpenApiResponse('Test Empty Response', '201')
    assert expected_openapi_dict == openapi_response.as_dict(openapi_schema_resolver)


@pytest.mark.skip('WIP')
def test_response_format():
    pass


@pytest.mark.skip('WIP')
def test_response_headers():
    pass


@pytest.mark.skip('WIP')
def test_response_any_of():
    pass


@pytest.mark.skip('WIP')
def test_response_links():
    pass


@pytest.mark.skip('WIP')
def test_response_multiple_media_types():
    pass
