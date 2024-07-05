import inspect
from unittest.mock import MagicMock, patch

import pytest
from code_autoeval.clients.llm_model.utils.model.function_attributes import FunctionAttributesFactory


# Mocking the necessary dependencies
@patch("code_autoeval.clients.llm_model.utils.model.function_attributes.FunctionAttributesFactory.__init__", return_value=None)
def test_get_function_docstring_normal(mock_init):
    def example_func():
        """This is a docstring."""
        pass
    
    result = FunctionAttributesFactory._get_function_docstring(example_func)
    assert result == "This is a docstring."

def test_get_function_docstring_none():
    def example_func():
        pass
    
    result = FunctionAttributesFactory._get_function_docstring(example_func)
    assert result == ""

@patch("code_autoeval.clients.llm_model.utils.model.function_attributes.FunctionAttributesFactory.__init__", return_value=None)
def test_get_function_docstring_multiple_lines(mock_init):
    def example_func():
        """This is a docstring.
        
        It spans multiple lines."""
        pass
    
    result = FunctionAttributesFactory._get_function_docstring(example_func)
    assert result == "This is a docstring.\n\nIt spans multiple lines."

@patch("code_autoeval.clients.llm_model.utils.model.function_attributes.FunctionAttributesFactory.__init__", return_value=None)
def test_get_function_docstring_empty(mock_init):
    def example_func():
        """"""
        pass
    
    result = FunctionAttributesFactory._get_function_docstring(example_func)
    assert result == ""

@patch("code_autoeval.clients.llm_model.utils.model.function_attributes.FunctionAttributesFactory.__init__", return_value=None)
def test_get_function_docstring_none_empty(mock_init):
    def example_func():
        pass
    
    result = FunctionAttributesFactory._get_function_docstring(example_func)
    assert result == ""