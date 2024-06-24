"""Implementation for system prompts."""

from typing import Any, Dict


class SystemPrompts:

    def generate_system_prompt(
        self, query: str, goal: str, function_signature: str, function_docstring: str
    ) -> str:
        return f"""You are an expert Python code generator. Your task is to create
            Python code that solves a specific problem using a provided function signature.
            Follow these instructions carefully:

            1. Function Details:
            Signature: {function_signature}
            Docstring: {function_docstring}

            2. Task: {query} - with {goal}

            3. Code Generation Guidelines:
            - Implement the function according to the given signature.
            - Ensure all function arguments have their types explicitly mentioned.
            - Create any necessary additional code to solve the task.
            - Ensure the code is efficient, readable, and follows Python best practices.
            - Include proper error handling if appropriate.
            - Add brief, inline comments for clarity if needed.
            - If any of the function args are pandas.DataFrame, pandas.Series, verify the index.

            4. Output Format:
            - Provide the Python code.
            - After the code, on a new line, write "# Expected Output:" followed by the expected output of the function for the given task.
            - The expected output should be a string representation of the result.

            5. Pytest Tests:
            - After providing the main function and expected output, create pytest tests for the function.
            - Create at least 3 test functions covering different scenarios, including edge cases and potential error conditions.
            - Ensure 100% code coverage for the function being tested.

            Example of expected response format:

            ```python
            import pandas as pd
            import numpy as np

            def example_func(arg1: int, arg2: int) -> int:
                # Your code here
                result = arg1 + arg2
                return result

            # Test the function
            print(example_func(3, 4))

            # Expected Output: 7

            import pytest

            def test_positive_numbers():
                assert example_func(3, 4) == 7

            def test_negative_numbers():
                assert example_func(-2, -3) == -5

            def test_zero():
                assert example_func(0, 0) == 0

            def test_large_numbers():
                assert example_func(1000000, 2000000) == 3000000

            def test_type_error():
                with pytest.raises(TypeError):
                    example_func("3", 4)

            Remember to provide the main function implementation, expected output, and pytest tests as described above. Ensure 100% code coverage for the function being tested."""

    def generate_clarification_prompt(
        self,
        query: str,
        function_name: str,
        function_signature: str,
        function_docstring: str,
        error_message: str,
        coverage_report: Dict[str, Any],
        previous_code: str,
        pytest_tests: str,
    ) -> str:
        base_prompt = f"""
        The previous response encountered issues. Please address the following problems and improve the code:

        Task: {query}
        Function signature: {function_signature}
        Function docstring: {function_docstring}
        """

        if "coverage is not 100%" in error_message:
            coverage_prompt = f"""
            Current code coverage: {coverage_report['total_coverage']}%
            Uncovered lines in {function_name}.py:
            {coverage_report['uncovered_lines']}

            To improve coverage:
            1. Ensure all branches of conditional statements are tested.
            2. Add test cases for edge cases and error conditions.
            3. If there are any exception handlers, make sure they are triggered in tests.
            4. Check if all parameters of the function are tested with different types of inputs.

            Previous pytest tests:
            {pytest_tests}
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
        1. An updated implementation of the {function_name} function.
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