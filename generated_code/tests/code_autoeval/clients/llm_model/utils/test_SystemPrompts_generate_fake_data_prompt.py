from typing import Any, Callable, Dict, Optional
from unittest.mock import patch

import pytest
from code_autoeval.clients.llm_model.utils.system_prompts import SystemPrompts


# Updated Implementation of the SystemPrompts.generate_fake_data_prompt function
def generate_fake_data_prompt(self, func: Callable, num_rows: int = 100, num_columns: int = 5) -> str:
    """Generate the system prompt for generating fake data."""
    
    if not callable(func):
        raise ValueError("The provided 'func' argument must be a callable.")
    
    function_signature = f"def {func.__name__}{func.__annotations__}"
    function_docstring = func.__doc__ if func.__doc__ else ""
    
    return f"""
    Generate a Python script to create fake data for the following function:

    {function_signature}

    {function_docstring}

    Use only the Faker library to generate appropriate fake data.

    Create a pandas DataFrame named 'fake_data' containing the generated data.

    Ensure the generated data is diverse and suitable for testing the function.

    Do not use PandasProvider or any other external libraries besides Faker, random, and pandas.

    """

@pytest.fixture
def mock_function():
    def example_func(arg1: int, arg2: int) -> int:
        return arg1 + arg2
    return example_func

# Normal use case test
def test_generate_fake_data_prompt_normal(mock_function):
    system_prompts = SystemPrompts()
    result = system_prompts.generate_fake_data_prompt(mock_function)
    
    assert isinstance(result, str), "The result should be a string"
    assert "Generate a Python script to create fake data for the following function:" in result
    assert f"def example_func(arg1: int, arg2: int) -> int" in result
    assert "Use only the Faker library to generate appropriate fake data." in result
    assert "Create a pandas DataFrame named 'fake_data' containing the generated data." in result

# Edge case test with non-callable function
def test_generate_fake_data_prompt_non_callable():
    system_prompts = SystemPrompts()
    
    with pytest.raises(ValueError):
        system_prompts.generate_fake_data_prompt("not a callable")

# Edge case test with no docstring function
def test_generate_fake_data_prompt_no_docstring(mock_function):
    def func():
        pass
    
    result = SystemPrompts().generate_fake_data_prompt(func)
    
    assert "Use only the Faker library to generate appropriate fake data." in result

# Example usage of the function with mock_function fixture
def test_example(mock_function):
    system_prompts = SystemPrompts()
    result = system_prompts.generate_fake_data_prompt(mock_function)
    
    print(result)  # Expected output should be printed here for manual verification