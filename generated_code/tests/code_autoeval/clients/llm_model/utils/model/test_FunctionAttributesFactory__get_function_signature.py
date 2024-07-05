import inspect
from unittest.mock import patch


class FunctionAttributesFactory:
    @staticmethod
    def _get_function_signature(func):
        return str(inspect.signature(func))

import inspect
from unittest.mock import patch

import pytest


# Mocking the FunctionAttributesFactory class and its method
@patch("code_autoeval.clients.llm_model.utils.model.function_attributes.FunctionAttributesFactory._get_function_signature")
def test_normal_case(mocked_method):
    # Arrange: Prepare a normal function for testing
    def example_func():
        pass
    
    # Act: Call the method with the example function
    FunctionAttributesFactory._get_function_signature(example_func)
    
    # Assert: Check that the mock was called with the correct arguments
    mocked_method.assert_called_once_with(example_func)

def test_edge_case_no_args():
    # Arrange: Prepare a function without any arguments
    def example_func():
        pass
    
    # Act: Call the method with the example function
    result = FunctionAttributesFactory._get_function_signature(example_func)
    
    # Assert: Check that the result is as expected for no arguments
    assert result == "()"

def test_error_condition():
    # Arrange: Prepare an invalid input (not a callable)
    with pytest.raises(TypeError):
        FunctionAttributesFactory._get_function_signature("not a function")

# Add more tests to cover other edge cases and error conditions as needed