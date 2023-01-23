
import pytest

from openapi_specgen import OpenApiParam


@pytest.mark.parametrize('location', [
    ('query'),
    ('path'),
    ('header'),
    ('cookie')
])
def test_param_location(location, openapi_schema_resolver):
    expected_param_dict = {
        'required': True,
        'schema': {
            'title': 'Test_Param',
            'type': 'string'
        },
        'name': 'test_param',
        'in': location
    }
    openapi_param = OpenApiParam('test_param', location, str)
    assert expected_param_dict == openapi_param.as_dict(openapi_schema_resolver)


def test_param_optinal(openapi_schema_resolver):
    expected_param_dict = {
        'required': False,
        'schema': {
            'title': 'Test_Param',
            'type': 'string'
        },
        'name': 'test_param',
        'in': 'path'
    }
    openapi_param = OpenApiParam('test_param', 'path', str, required=False)
    assert expected_param_dict == openapi_param.as_dict(openapi_schema_resolver)


def test_param_default(openapi_schema_resolver):
    expected_param_dict = {
        'required': True,
        'schema': {
            'title': 'Test_Param',
            'type': 'string',
            'default': 'default_value'
        },
        'name': 'test_param',
        'in': 'path'
    }
    openapi_param = OpenApiParam('test_param', 'path', str, 'default_value')
    assert expected_param_dict == openapi_param.as_dict(openapi_schema_resolver)


def test_param_any_type(openapi_schema_resolver):
    expected_param_dict = {
        'required': True,
        'schema': {
            'title': 'Test_Param'
        },
        'name': 'test_param',
        'in': 'path'
    }
    openapi_param = OpenApiParam('test_param', 'path')
    assert expected_param_dict == openapi_param.as_dict(openapi_schema_resolver)


@pytest.mark.skip('WIP')
def test_param_enum():
    pass


@pytest.mark.skip('WIP')
def test_param_examples():
    pass


@pytest.mark.skip('WIP')
def test_param_empty_value():
    pass


@pytest.mark.skip('WIP')
def test_param_nullable():
    pass


@pytest.mark.skip('WIP')
def test_param_deprecated():
    pass
