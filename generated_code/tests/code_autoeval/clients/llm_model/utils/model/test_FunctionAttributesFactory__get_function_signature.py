import inspect
from typing import Callable


class FunctionAttributesFactory:
    @staticmethod
    def _get_function_signature(func: Callable) -> str:
        """
        Extract the function signature.

        Args:
            func (Callable): The callable object whose signature is to be extracted.

        Returns:
            str: A string representation of the function's signature.
        """
        return str(inspect.signature(func))


from unittest.mock import patch

import pytest

from code_autoeval.llm_model.utils.model.function_attributes import (
    FunctionAttributesFactory,
)


# Test function to check if the signature is correctly extracted from a normal function
def test_get_signature_normal():
    def example_func(arg1, arg2=None):
        pass

    with patch(
        "code_autoeval.llm_model.utils.model.function_attributes.inspect.signature",
        return_value="(*args, **kwargs)",
    ):
        result = FunctionAttributesFactory._get_function_signature(example_func)
        assert result == "(*args, **kwargs)"


# Test function to check if the signature is correctly extracted from a method
def test_get_signature_method():
    class ExampleClass:
        def example_method(self, arg1, arg2=None):
            pass

    with patch(
        "code_autoeval.llm_model.utils.model.function_attributes.inspect.signature",
        return_value="(self, *args, **kwargs)",
    ):
        result = FunctionAttributesFactory._get_function_signature(
            ExampleClass.example_method
        )
        assert result == "(self, *args, **kwargs)"


# Test function to check if the signature extraction handles errors gracefully
def test_get_signature_error():
    with pytest.raises(TypeError):
        FunctionAttributesFactory._get_function_signature(
            None
        )  # Passing None should raise a TypeErrordef test_get_signature_error():
    with pytest.raises(TypeError):
        FunctionAttributesFactory._get_function_signature(
            None
        )  # Passing None should raise a TypeError
