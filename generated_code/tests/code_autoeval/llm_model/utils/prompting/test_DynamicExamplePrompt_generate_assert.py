from unittest.mock import MagicMock

import pytest
from code_autoeval.llm_model.utils.prompting.dynamic_example_prompt import DynamicExamplePrompt


@pytest.fixture(scope='module')
def mock_dynamicexampleprompt():
    return DynamicExamplePrompt()

def test_generate_assert_with_expected_output(mock_dynamicexampleprompt):
    # Arrange
    self = MagicMock()
    method_name = "test_method"
    function_return_type = "str"
    function_params = ["param1", "param2"]
    expected_output = "expected_result"

    instance = mock_dynamicexampleprompt

    # Act
    result = instance.generate_assert(method_name, function_return_type, function_params, expected_output)

    # Assert
    assert isinstance(result, str)
    assert "assert isinstance(result, str)" in result
    assert f"assert result == {expected_output}" in result

def test_generate_assert_without_expected_output(mock_dynamicexampleprompt):
    # Arrange
    self = MagicMock()
    method_name = "test_method"
    function_return_type = "dict"
    function_params = []
    expected_output = None

    instance = mock_dynamicexampleprompt

    # Act
    result = instance.generate_assert(method_name, function_return_type, function_params, expected_output)

    # Assert
    assert isinstance(result, str)
    assert "assert isinstance(result, dict)" in result
    assert "assert 'type' in result" in result
    assert "assert result['type'] == 'DataFrame'" in result

def test_generate_assert_with_return_type_dataframe(mock_dynamicexampleprompt):
    # Arrange
    self = MagicMock()
    method_name = "test_method"
    function_return_type = "pd.DataFrame"
    function_params = []
    expected_output = None

    instance = mock_dynamicexampleprompt

    # Act
    result = instance.generate_assert(method_name, function_return_type, function_params, expected_output)

    # Assert
    assert isinstance(result, str)
    assert "assert not result.empty" in result
    assert "assert isinstance(result, pd.DataFrame)" in result

def test_generate_assert_with_return_type_none(mock_dynamicexampleprompt):
    # Arrange
    self = MagicMock()
    method_name = "test_method"
    function_return_type = "NoneType"
    function_params = []
    expected_output = None

    instance = mock_dynamicexampleprompt

    # Act
    result = instance.generate_assert(method_name, function_return_type, function_params, expected_output)

    # Assert
    assert isinstance(result, str)
    assert "assert result is None" in result