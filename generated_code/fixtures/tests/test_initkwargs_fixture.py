import pytest
from generated_code.fixtures.fixtures.initkwargs_fixture import fixture_mock_initkwargs
from code_autoeval.llm_model.utils.base_llm_class import InitKwargs
def test_mock_initkwargs(fixture_mock_initkwargs):
    assert isinstance(fixture_mock_initkwargs, InitKwargs)
    assert hasattr(fixture_mock_initkwargs, 'verbose')
    assert isinstance(fixture_mock_initkwargs.verbose, bool)
    assert hasattr(fixture_mock_initkwargs, 'debug')
    assert isinstance(fixture_mock_initkwargs.debug, bool)
    assert hasattr(fixture_mock_initkwargs, 'func_name')
    assert isinstance(fixture_mock_initkwargs.func_name, str)