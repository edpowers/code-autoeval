from typing import Callable


class SystemPrompts:
    def generate_fake_data_prompt(self, func: Callable, num_rows: int = 100, num_columns: int = 5) -> str:
        """Generate the system prompt for generating fake data."""
        function_signature = f"def {func.__name__}({', '.join([f'{arg}: {typ}' for arg, typ in func.__annotations__.items() if arg != 'return'])}):"
        function_docstring = f'"""{func.__doc__}"""' if func.__doc__ else ""

        return f"""
        Generate a Python script to create fake data for the following function:

        {function_signature}

        {function_docstring}

        Use only the Faker library to generate appropriate fake data.

        Create a pandas DataFrame named 'fake_data' containing the generated data.

        Ensure the generated data is diverse and suitable for testing the function.

        Do not use PandasProvider or any other external libraries besides Faker, random, and pandas.

        """

from unittest.mock import patch

import pytest

from code_autoeval.llm_model.utils.system_prompts import SystemPrompts


@pytest.fixture
def system_prompts():
    return SystemPrompts()

@patch("code_autoeval.llm_model.utils.system_prompts.SystemPrompts.__init__", return_value=None)
def test_generate_fake_data_prompt(mock_init):
    def example_func(arg1: int, arg2: int) -> int:
        """Example function."""
        return arg1 + arg2

    sp = SystemPrompts()
    prompt = sp.generate_fake_data_prompt(example_func)

    assert "Generate a Python script to create fake data for the following function:" in prompt
    assert f"def example_func(arg1: int, arg2: int):" in prompt
    assert '"""Example function."""' in prompt
    assert "Use only the Faker library to generate appropriate fake data." in prompt
    assert "Create a pandas DataFrame named 'fake_data' containing the generated data." in prompt
    assert "Ensure the generated data is diverse and suitable for testing the function." in prompt
    assert "Do not use PandasProvider or any other external libraries besides Faker, random, and pandas." in prompt

def test_generate_fake_data_prompt_with_no_docstring(system_prompts):
    def example_func(arg1: int, arg2: int) -> int:
        pass

    prompt = system_prompts.generate_fake_data_prompt(example_func)

    assert "Generate a Python script to create fake data for the following function:" in prompt
    assert f"def example_func(arg1: int, arg2: int):" in prompt
    assert '"""' not in prompt
    assert "Use only the Faker library to generate appropriate fake data." in prompt
    assert "Create a pandas DataFrame named 'fake_data' containing the generated data." in prompt
    assert "Ensure the generated data is diverse and suitable for testing the function." in prompt
    assert "Do not use PandasProvider or any other external libraries besides Faker, random, and pandas." in prompt

def test_generate_fake_data_prompt_with_default_values(system_prompts):
    def example_func(arg1: int = 5, arg2: int = 10) -> int:
        """Example function with default values."""
        return arg1 + arg2

    prompt = system_prompts.generate_fake_data_prompt(example_func)

    assert "Generate a Python script to create fake data for the following function:" in prompt
    assert f"def example_func(arg1: int = 5, arg2: int = 10):" in prompt
    assert '"""Example function with default values."""' in prompt
    assert "Use only the Faker library to generate appropriate fake data." in prompt
    assert "Create a pandas DataFrame named 'fake_data' containing the generated data." in prompt
    assert "Ensure the generated data is diverse and suitable for testing the function." in prompt
    assert "Do not use PandasProvider or any other external libraries besides Faker, random, and pandas." in prompt

def test_generate_fake_data_prompt_with_multiple_args(system_prompts):
    def example_func(arg1: int, arg2: int, arg3: str) -> int:
        """Example function with multiple arguments."""
        return arg1 + arg2

    prompt = system_prompts.generate_fake_data_prompt(example_func)

    assert "Generate a Python script to create fake data for the following function:" in prompt
    assert f"def example_func(arg1: int, arg2: int, arg3: str):" in prompt
    assert '"""Example function with multiple arguments."""' in prompt
    assert "Use only the Faker library to generate appropriate fake data." in prompt
    assert "Create a pandas DataFrame named 'fake_data' containing the generated data." in prompt
    assert "Ensure the generated data is diverse and suitable for testing the function." in prompt
    assert "Do not use PandasProvider or any other external libraries besides Faker, random, and pandas." in prompt

def test_generate_fake_data_prompt_with_no_return(system_prompts):
    def example_func(arg1: int, arg2: int):
        """Example function without return."""
        print(arg1 + arg2)

    prompt = system_prompts.generate_fake_data_prompt(example_func)

    assert "Generate a Python script to create fake data for the following function:" in prompt
    assert f"def example_func(arg1: int, arg2: int):" in prompt
    assert '"""Example function without return."""' in prompt
    assert "Use only the Faker library to generate appropriate fake data." in prompt
    assert "Create a pandas DataFrame named 'fake_data' containing the generated data." in prompt
    assert "Ensure the generated data is diverse and suitable for testing the function." in prompt
    assert "Do not use PandasProvider or any other external libraries besides Faker, random, and pandas." in prompt    assert "Use only the Faker library to generate appropriate fake data." in prompt
    assert "Create a pandas DataFrame named 'fake_data' containing the generated data." in prompt
    assert "Ensure the generated data is diverse and suitable for testing the function." in prompt
    assert "Do not use PandasProvider or any other external libraries besides Faker, random, and pandas." in prompt