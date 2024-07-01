"""Implementation for system prompts."""

from typing import Any, Callable, Dict, Optional

from code_autoeval.clients.llm_model.utils.model.class_data_model import ClassDataModel
from code_autoeval.clients.llm_model.utils.model.function_attributes import (
    FunctionAttributes,
)


class SystemPrompts:

    def generate_system_prompt(
        self,
        query: str,
        goal: str,
        function_attributes: FunctionAttributes,
        class_model: Optional[ClassDataModel] = None,
    ) -> str:
        """Passthrough generation of system prompt."""
        if function_attributes.function_body and class_model:
            return self.generate_system_prompt_with_existing_function(
                query,
                goal,
                function_attributes,
                class_model,
            )

        return self.generate_system_prompt_no_existing_function(
            query, goal, function_attributes
        )

    def generate_system_prompt_with_existing_function(
        self,
        query: str,
        goal: str,
        function_attributes: FunctionAttributes,
        class_model: ClassDataModel,
    ) -> str:
        return f"""
        You are an expert Python code analyst and test writer.
        Your task is to analyze an existing Python function and create comprehensive tests for it.

        Follow these instructions carefully:

        1. Function Details:
        Function Name: {function_attributes.func_name}
        Function is async coroutine: {function_attributes.is_coroutine}
        Signature: {function_attributes.function_signature}
        Docstring: {function_attributes.function_docstring}
        Function Body:
        {function_attributes.function_body}

        If there are base classes, initialization parameters, or class attributes,
        please mock all of the dependencies so that we can properly unit test.
        Use unittest.mock or any other pytest.patch method to mock these dependencies.

        Please use the following relative path provided for all mocking:
        {class_model.absolute_path}

        Function Base Classes:
        {class_model.base_classes}

        Initialization Parameters:
        {class_model.init_params}

        Class Attributes:
        {class_model.class_attributes}

        Mocking __init__ functions should return None, like the following:
        @patch("code_autoeval.clients.llm_model.llm_model.LLMModel.__init__", return_value=None)

        2. Task: {query} - with {goal}

        3. Analysis Guidelines:
        - Review the function implementation carefully.
        - Identify the function's purpose, inputs, and expected outputs.
        - Note any potential edge cases or error conditions.

        4. Test Generation Guidelines:
        - Create pytest tests for the function.
        - Write at least 5 test functions covering different scenarios, including:
            a) Normal use cases
            b) Edge cases
            c) Potential error conditions
        - Ensure 100% code coverage for the function being tested.
        - If any of the function args are pandas.DataFrame or pandas.Series, include tests that verify the index and data integrity.

        When writing pytest tests, please adhere to the following guidelines:

        1. Only use variables that are explicitly defined within each test function.
        2. Avoid relying on global variables or undefined mocks.
        3. If you need to mock a method or function, define the mock within the test function using pytest.mock.patch as a decorator or context manager.
        4. Ensure that each test function is self-contained and does not depend on the state from other tests.
        5. Use descriptive names for test functions that clearly indicate what is being tested.
        6. Follow the Arrange-Act-Assert (AAA) pattern in your tests:
        - Arrange: Set up the test data and conditions.
        - Act: Perform the action being tested.
        - Assert: Check that the results are as expected.
        7. Use assert statements to verify the expected behavior.
        8. When testing for exceptions, use pytest.raises() as a context manager.

        5. Output Format:
        - Provide a brief analysis of the function (2-3 sentences).
        - Then, provide the pytest tests.

        Example of expected response format:

        ```python
        # Expected Output: 7

        import pytest
        import pandas as pd
        import numpy as np

        def example_func_provided(arg1: int, arg2: int) -> int:
            # Your code here
            result = arg1 + arg2
            return result

        # Test the function
        print(example_func_provided(3, 4))

        ##################################################
        # TESTS
        ##################################################

        def test_normal_case():
            # Test normal use case
            assert function_name(normal_args) == expected_output

        def test_edge_case_1():
            # Test an edge case
            assert function_name(edge_case_args) == expected_edge_output

        def test_error_condition():
            # Test an error condition
            with pytest.raises(ExpectedErrorType):
                function_name(error_inducing_args)

        # Add more tests to ensure 100% coverage
        """

    def generate_system_prompt_no_existing_function(
        self,
        query: str,
        goal: str,
        function_attributes: FunctionAttributes,
    ) -> str:
        return f"""You are an expert Python code generator. Your task is to create Python code that solves a specific problem using a provided function signature.
        Follow these instructions carefully:

        1. Function Details:
        Function Name: {function_attributes.func_name}
        Function is async coroutine: {function_attributes.is_coroutine}
        Signature: {function_attributes.function_signature}
        Docstring: {function_attributes.function_docstring}

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

        When writing pytest tests, please adhere to the following guidelines:

        1. Only use variables that are explicitly defined within each test function.
        2. Avoid relying on global variables or undefined mocks.
        3. If you need to mock a method or function, define the mock within the test function using pytest.mock.patch as a decorator or context manager.
        4. Ensure that each test function is self-contained and does not depend on the state from other tests.
        5. Use descriptive names for test functions that clearly indicate what is being tested.
        6. Follow the Arrange-Act-Assert (AAA) pattern in your tests:
        - Arrange: Set up the test data and conditions.
        - Act: Perform the action being tested.
        - Assert: Check that the results are as expected.
        7. Use assert statements to verify the expected behavior.
        8. When testing for exceptions, use pytest.raises() as a context manager.

        Example of expected response format:

        ```python
        # Expected Output: 7

        import pandas as pd
        import numpy as np

        def example_func(arg1: int, arg2: int) -> int:
            # Your code here
            result = arg1 + arg2
            return result

        class TestExampleFunc:
            def test_normal_case(self):
                assert example_func(3, 4) == 7

            def test_edge_case(self):
                assert example_func(-2, -3) == -5

            def test_zero(self):
                assert example_func(0, 0) == 0

        # Test the function
        print(example_func(3, 4))

        print(TestExampleFunc().test_normal_case())

        # Tests
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

        def test_class_normal_case():
            assert TestExampleFunc().test_normal_case() == None

        Remember to provide the main function implementation, expected output, and pytest tests as described above.
        Ensure 100% code coverage for the function being tested."""

    def generate_clarification_prompt(
        self,
        query: str,
        error_message: str,
        coverage_report: Dict[str, Any],
        previous_code: str,
        pytest_tests: str,
        function_attributes: FunctionAttributes,
        unit_test_coverage_missing: Dict[str, Any],
    ) -> str:
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

    def generate_fake_data_prompt(
        self, func: Callable, num_rows: int = 100, num_columns: int = 5
    ) -> str:
        """Generate the system prompt for generating fake data."""
        function_signature = f"def {func.__name__}{func.__annotations__}"
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
