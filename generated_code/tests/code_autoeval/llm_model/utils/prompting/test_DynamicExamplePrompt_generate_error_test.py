from unittest.mock import MagicMock

import pytest
from code_autoeval.llm_model.utils.prompting.dynamic_example_prompt import DynamicExamplePrompt
from generated_code.fixtures.fixtures.dynamicexampleprompt_fixture import fixture_mock_dynamicexampleprompt


@pytest.fixture(scope='module')
def mock_dynamicexampleprompt():
    return fixture_mock_dynamicexampleprompt()

def test_generate_error_test(mock_dynamicexampleprompt):
    # Arrange
    self = MagicMock()
    class_name = "DynamicExamplePrompt"
    func_name = "some_function"
    method_name = "some_method"
    error_condition = "instance.some_attribute = None"
    expected_error = "ValueError"

    instance = mock_dynamicexampleprompt

    # Act
    result = instance.generate_error_test(class_name, func_name, method_name, error_condition, expected_error)

    # Assert
    assert isinstance(result, str)
    assert "def test_" in result
    assert f"instance.{method_name}(" in result
    assert f"{expected_error}" in result