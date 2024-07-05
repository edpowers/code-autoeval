from typing import Any, Dict
from unittest.mock import patch

import pytest

from code_autoeval.llm_model.utils.model.function_attributes import \
    FunctionAttributes
from code_autoeval.llm_model.utils.system_prompts import SystemPrompts


def generate_clarification_prompt(self, query: str, error_message: str, coverage_report: Dict[str, Any], previous_code: str, pytest_tests: str, function_attributes: FunctionAttributes, unit_test_coverage_missing: Dict[str, Any]) -> str:
    base_prompt = f"""
    The previous response encountered issues. Please address the following problems and improve the code:

    Task: {query}

    Function signature: {function_attributes.function_signature}

    Function is async coroutine: {function_attributes.is_coroutine}

    Function docstring: {function_attributes.function_docstring}
    """

    if "coverage is not 100%" in error_message:
        coverage_prompt = f"""
        Current code coverage: {coverage_report['total_coverage']}%

        Uncovered lines in {function_attributes.func_name}.py:

        {coverage_report['uncovered_lines']}

        To improve coverage:
        1. Ensure all branches of conditional statements are tested.
        2. Add test cases for edge cases and error conditions.
        3. If there are any exception handlers, make sure they are triggered in tests.
        4. Check if all parameters of the function are tested with different types of inputs.

        Previous pytest tests:
        {pytest_tests}

        The following lines from the original code are not covered by tests.
        Please write additional tests that target these lines.
        Write tests that cover all possible code paths to achieve 100% coverage.
        """

        for range_tuple, code_snippet in unit_test_coverage_missing.items():
            coverage_prompt += f"""
        Lines {range_tuple[0]}-{range_tuple[1]}:
        {code_snippet}
        """

        base_prompt += coverage_prompt
    else:
        execution_error_prompt = f"""
        Execution error encountered:
        {error_message}

        Please review the code and address the following:
        1. Check for syntax errors or logical issues in the implementation.
        2. Ensure all necessary imports are included.
        3. Verify that the function handles all possible input scenarios correctly.

        Previous code that generated the error:
        {previous_code}
        """

        base_prompt += execution_error_prompt

    base_prompt += f"""
    Please provide:
    1. An updated implementation of the {function_attributes.func_name} function.
    2. A comprehensive set of pytest tests that cover all code paths.
    3. Expected output for a sample input.

    Remember to handle all possible scenarios, including:
    - Empty inputs (e.g., empty DataFrames, empty columns)
    - Invalid inputs (e.g., non-existent columns, incorrect data types)
    - Edge cases (e.g., very large or very small values, NaN values)
    - Various data types (e.g., integers, floats, strings, dates)

    Ensure that your implementation is robust and handles errors gracefully.
    """

    return base_prompt

from typing import Any, Dict
from unittest.mock import patch

import pytest

from code_autoeval.llm_model.utils.model.function_attributes import \
    FunctionAttributes
from code_autoeval.llm_model.utils.system_prompts import SystemPrompts


@pytest.mark.parametrize("query, error_message, coverage_report, previous_code, pytest_tests, function_attributes, unit_test_coverage_missing, expected_prompt", [
    (
        "Fix the function to handle empty inputs correctly.",
        "Execution error encountered: The function does not handle empty strings properly.",
        {'total_coverage': 80, 'uncovered_lines': ['line1', 'line2']},
        "def example_func(arg): return arg",
        "test_example_func",
        FunctionAttributes(function_signature="def example_func(arg: int) -> int", is_coroutine=False, function_docstring="A sample function"),
        {'range': ('10', '20')},
        """The previous response encountered issues. Please address the following problems and improve the code:

    Task: Fix the function to handle empty inputs correctly.

    Function signature: def example_func(arg: int) -> int

    Function is async coroutine: False

    Function docstring: A sample function

        Execution error encountered:
        The function does not handle empty strings properly.

        Please review the code and address the following:
        1. Check for syntax errors or logical issues in the implementation.
        2. Ensure all necessary imports are included.
        3. Verify that the function handles all possible input scenarios correctly.

        Previous code that generated the error:
        def example_func(arg): return arg

    Please provide:
    1. An updated implementation of the example_func function.
    2. A comprehensive set of pytest tests that cover all code paths.
    3. Expected output for a sample input.

    Remember to handle all possible scenarios, including:
    - Empty inputs (e.g., empty DataFrames, empty columns)
    - Invalid inputs (e.g., non-existent columns, incorrect data types)
    - Edge cases (e.g., very large or very small values, NaN values)
    - Various data types (e.g., integers, floats, strings, dates)

    Ensure that your implementation is robust and handles errors gracefully."""
    )
])
def test_generate_clarification_prompt(query, error_message, coverage_report, previous_code, pytest_tests, function_attributes, unit_test_coverage_missing, expected_prompt):
    with patch("code_autoeval.llm_model.utils.system_prompts.SystemPrompts.__init__", return_value=None):
        result = SystemPrompts().generate_clarification_prompt(query, error_message, coverage_report, previous_code, pytest_tests, function_attributes, unit_test_coverage_missing)
        assert result == expected_prompt    )
])
def test_generate_clarification_prompt(query, error_message, coverage_report, previous_code, pytest_tests, function_attributes, unit_test_coverage_missing, expected_prompt):
    with patch("code_autoeval.llm_model.utils.system_prompts.SystemPrompts.__init__", return_value=None):
        result = SystemPrompts().generate_clarification_prompt(query, error_message, coverage_report, previous_code, pytest_tests, function_attributes, unit_test_coverage_missing)
        assert result == expected_prompt