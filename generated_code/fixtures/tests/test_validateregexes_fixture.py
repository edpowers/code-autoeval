import pytest
from generated_code.fixtures.fixtures.validateregexes_fixture import fixture_mock_validateregexes
from code_autoeval.llm_model.utils.validation.validate_regexes import ValidateRegexes
def test_mock_validateregexes(fixture_mock_validateregexes):
    assert isinstance(fixture_mock_validateregexes, ValidateRegexes)
    assert hasattr(fixture_mock_validateregexes, 'validate_class_name_in_local_vars')
    assert callable(fixture_mock_validateregexes.validate_class_name_in_local_vars)
    assert hasattr(fixture_mock_validateregexes, 'validate_func_in_code')
    assert callable(fixture_mock_validateregexes.validate_func_in_code)
    assert hasattr(fixture_mock_validateregexes, 'validate_func_name_in_code')
    assert callable(fixture_mock_validateregexes.validate_func_name_in_code)
    assert hasattr(fixture_mock_validateregexes, 'validate_target_node')
    assert callable(fixture_mock_validateregexes.validate_target_node)
    assert hasattr(fixture_mock_validateregexes, 'validate_test_in_pytest_code')
    assert callable(fixture_mock_validateregexes.validate_test_in_pytest_code)