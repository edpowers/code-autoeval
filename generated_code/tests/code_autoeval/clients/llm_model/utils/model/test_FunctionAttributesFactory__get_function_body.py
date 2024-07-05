import inspect
from unittest.mock import patch

import pytest


def example_func(arg1: int, arg2: int) -> int:
    result = arg1 + arg2
    return result

class FunctionAttributesFactory:
    @staticmethod
    def _get_function_body(func):
        source_lines = inspect.getsourcelines(func)[0]
        
        # Remove decorator lines, if any
        while source_lines and source_lines[0].strip().startswith("@"):
            source_lines.pop(0)
        
        # Remove the function definition line
        source_lines.pop(0)
        
        # Remove docstring lines
        if source_lines and source_lines[0].strip().startswith('"""'):
            while source_lines and not source_lines[-1].strip().endswith('"""'):
                source_lines.pop()
        
        # Join the remaining lines and dedent
        return inspect.cleandoc("\n".join(source_lines))

##################################################
# TESTS
##################################################

@patch("inspect.getsourcelines", return_value=(["def example_func(arg1: int, arg2: int) -> int:\n    result = arg1 + arg2\n    return result".splitlines(), None))
def test_normal_case(_mock_getsourcelines):
    # Test normal use case
    assert FunctionAttributesFactory._get_function_body(example_func) == "result = arg1 + arg2\nreturn result"

@patch("inspect.getsourcelines", return_value=(["def example_func(arg1: int, arg2: int) -> int:\n    \"\"\"This is a docstring\"\"\"\n    result = arg1 + arg2\n    return result".splitlines(), None))
def test_with_docstring(_mock_getsourcelines):
    # Test with a docstring
    assert FunctionAttributesFactory._get_function_body(example_func) == "result = arg1 + arg2\nreturn result"

@patch("inspect.getsourcelines", return_value=(["def example_func(arg1: int, arg2: int) -> int:\n    @decorator\n    result = arg1 + arg2\n    return result".splitlines(), None))
def test_with_decorator(_mock_getsourcelines):
    # Test with a decorator
    assert FunctionAttributesFactory._get_function_body(example_func) == "result = arg1 + arg2\nreturn result"

@patch("inspect.getsourcelines", return_value=(["def example_func(arg1: int, arg2: int) -> int:\n    pass".splitlines(), None))
def test_with_empty_body(_mock_getsourcelines):
    # Test with an empty function body
    assert FunctionAttributesFactory._get_function_body(example_func) == "pass"

@patch("inspect.getsourcelines", return_value=(["def example_func(arg1: int, arg2: int) -> int:\n    result = arg1 + arg2\n    # This is a comment\n    return result".splitlines(), None))
def test_with_comment(_mock_getsourcelines):
    # Test with a comment in the function body
    assert FunctionAttributesFactory._get_function_body(example_func) == "result = arg1 + arg2\nreturn result"