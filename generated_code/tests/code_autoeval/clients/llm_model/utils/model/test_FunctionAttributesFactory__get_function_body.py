import inspect
from unittest.mock import patch

import pytest
from code_autoeval.clients.llm_model.utils.model.function_attributes import FunctionAttributesFactory


# Mocking the FunctionAttributesFactory class and its dependencies
@patch("code_autoeval.clients.llm_model.utils.model.function_attributes.FunctionAttributesFactory")
def test_get_function_body(mock_factory):
    # Arrange
    def mock_func():
        """Mock function docstring"""
        pass
    
    expected_body = "pass"

    with patch("inspect.getsourcelines", return_value=(["def mock_func():\n    \"\"\"Mock function docstring\"\"\"\n    pass"], 1)):
        # Act
        result = FunctionAttributesFactory._get_function_body(mock_func)
        
        # Assert
        assert result == expected_body

# Additional tests to cover different scenarios and edge cases
def test_with_decorator():
    def mock_func_with_decorator():
        """Mock function with decorator"""
        pass
    
    @patch("code_autoeval.clients.llm_model.utils.model.function_attributes.FunctionAttributesFactory")
    def test_mock_func(mock_factory):
        expected_body = "pass"
        
        source_lines = ["@decorator\n", "def mock_func_with_decorator():\n    \"\"\"Mock function with decorator\"\"\"\n    pass"]
        with patch("inspect.getsourcelines", return_value=(source_lines, 1)):
            result = FunctionAttributesFactory._get_function_body(mock_func_with_decorator)
            assert result == expected_body
    
    test_mock_func()

def test_with_docstring():
    def mock_func_with_docstring():
        """Mock function with docstring"""
        pass
    
    @patch("code_autoeval.clients.llm_model.utils.model.function_attributes.FunctionAttributesFactory")
    def test_mock_func(mock_factory):
        expected_body = "pass"
        
        source_lines = ["def mock_func_with_docstring():\n", "\"\"\"Mock function with docstring\"\"\"\n", "    pass"]
        with patch("inspect.getsourcelines", return_value=(source_lines, 1)):
            result = FunctionAttributesFactory._get_function_body(mock_func_with_docstring)
            assert result == expected_body
    
    test_mock_func()

def test_empty_function():
    def mock_empty_func():
        pass
    
    @patch("code_autoeval.clients.llm_model.utils.model.function_attributes.FunctionAttributesFactory")
    def test_mock_func(mock_factory):
        expected_body = "pass"
        
        source_lines = ["def mock_empty_func():\n", "    pass"]
        with patch("inspect.getsourcelines", return_value=(source_lines, 1)):
            result = FunctionAttributesFactory._get_function_body(mock_empty_func)
            assert result == expected_body
    
    test_mock_func()

def test_multiple_decorators():
    def mock_func_with_multiple_decorators():
        """Mock function with multiple decorators"""
        pass
    
    @patch("code_autoeval.clients.llm_model.utils.model.function_attributes.FunctionAttributesFactory")
    def test_mock_func(mock_factory):
        expected_body = "pass"
        
        source_lines = ["@decorator1\n", "@decorator2\n", "def mock_func_with_multiple_decorators():\n", "\"\"\"Mock function with multiple decorators\"\"\"\n", "    pass"]
        with patch("inspect.getsourcelines", return_value=(source_lines, 1)):
            result = FunctionAttributesFactory._get_function_body(mock_func_with_multiple_decorators)
            assert result == expected_body
    
    test_mock_func()