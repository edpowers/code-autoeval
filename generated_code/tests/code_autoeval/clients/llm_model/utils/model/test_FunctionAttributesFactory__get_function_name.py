from unittest.mock import patch

import pytest
from code_autoeval.clients.llm_model.utils.model.function_attributes import FunctionAttributesFactory


# Mocking ClassDataModel for testing purposes
class MockClassDataModel:
    class_name = "TestClass"

@patch("code_autoeval.clients.llm_model.utils.model.function_attributes.FunctionAttributesFactory.__init__", return_value=None)
def test_normal_use_case(mock_init):
    # Arrange
    mock_func = lambda: None
    mock_func.__name__ = "test_function"
    
    expected_output = "test_function"
    
    # Act
    result = FunctionAttributesFactory._get_function_name(mock_func)
    
    # Assert
    assert result == expected_output

def test_with_class_model():
    # Arrange
    mock_func = lambda: None
    mock_func.__name__ = "test_function"
    
    class_model = MockClassDataModel()
    expected_output = "TestClass.test_function"
    
    # Act
    result = FunctionAttributesFactory._get_function_name(mock_func, class_model)
    
    # Assert
    assert result == expected_output

def test_no_class_model():
    # Arrange
    mock_func = lambda: None
    mock_func.__name__ = "test_function"
    
    expected_output = "test_function"
    
    # Act
    result = FunctionAttributesFactory._get_function_name(mock_func)
    
    # Assert
    assert result == expected_output