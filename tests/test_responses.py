from dataclasses import dataclass

import pytest

from openapi_specgen import OpenApiResponse


@dataclass
class SomeObject():
    some_field: str


def test_response_primitive():
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
    assert expected_openapi_dict == openapi_response.as_dict()


def test_response_object():
    expected_openapi_dict = {
        '200': {
            'description': 'Test Response',
            'content': {
                'application/json': {
                    'schema':
                    {
                        '$ref': '#/components/schemas/SomeObject'
                    }
                }
            }
        }
    }
    openapi_response = OpenApiResponse('Test Response', data_type=SomeObject)
    assert expected_openapi_dict == openapi_response.as_dict()


def test_response_empty():
    expected_openapi_dict = {
        '201': {
            'description': 'Test Empty Response'
        }
    }
    openapi_response = OpenApiResponse('Test Empty Response', '201')
    assert expected_openapi_dict == openapi_response.as_dict()


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
