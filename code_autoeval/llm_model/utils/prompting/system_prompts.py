"""Implementation for system prompts."""

from typing import Any, Callable, Dict, List, Optional, Tuple

from multiuse.model import class_data_model

from code_autoeval.llm_model.utils import model
from code_autoeval.llm_model.utils.prompting.dynamic_example_prompt import (
    DynamicExamplePrompt,
)


class SystemPrompts(DynamicExamplePrompt):

    def generate_system_prompt(
        self,
        query: str,
        goal: str,
        func_attributes: model.FunctionAttributes,
        class_model: Optional[class_data_model.ClassDataModel] = None,
        base_class_fixture_import_paths: Dict[str, str] = {},
    ) -> str:
        """Passthrough generation of system prompt."""
        if func_attributes.function_body and class_model:
            return self.generate_system_prompt_with_existing_function(
                query,
                goal,
                func_attributes,
                class_model,
                base_class_fixture_import_paths,
            )

        return self.generate_system_prompt_no_existing_function(
            query, goal, func_attributes
        )

    def generate_system_prompt_with_existing_function(
        self,
        query: str,
        goal: str,
        func_attributes: model.FunctionAttributes,
        class_model: class_data_model.ClassDataModel,
        base_class_fixture_import_paths: Dict[str, str],
    ) -> str:

        init_example = self.provide_init_mocking_example(
            class_model.class_name,
            class_model.import_path,
            base_class_fixture_import_paths[class_model.class_name],
            class_model.init_params,
            class_model.class_attributes,
            class_model.base_classes,
        )

        return f"""
        You are an expert Python code analyst and test writer.
        Your task is to analyze an existing Python function and create comprehensive tests for it.

        Follow these instructions carefully:

        1. Function Details:
        Function Name: {func_attributes.func_name}
        Function is async coroutine: {func_attributes.is_coroutine}
        Signature: {func_attributes.function_signature}
        Docstring: {func_attributes.function_docstring}
        Function Body:
        {func_attributes.function_body}

        Please use the following relative path provided for all mocking:
        Class Name: {class_model.class_name}
        Base Classes: {class_model.base_classes}
        Base Class Fixture Import Paths: {base_class_fixture_import_paths}
        Initialization Parameters: {class_model.init_params}
        Class Attributes: {class_model.class_attributes}

        2. Task: {query} - with {goal}

        {self.return_analyis_and_guidelines()}

        5 Test Case Structure:
        {self.provide_async_or_sync_mocking_structure(
            func_attributes.is_coroutine,
            class_model.class_name,
            class_model.import_path,
            func_attributes.func_name,
            func_attributes.method_name,
            init_example,
            class_model=class_model,
            func_attributes=func_attributes)
        }
        """
        # 6. Output Format:
        # Example of expected response format:
        # {self.return_example_output(create_function=False, create_pytests=True, is_async=function_attributes.is_coroutine)}
        # """

    def provide_init_mocking_example(
        self,
        class_name: str,
        class_relative_path: str,
        fixture_import_statement: str,
        init_params: List[str],
        class_attributes: List[str],
        base_classes: List[str],
    ) -> str:

        def analyze_inputs():
            fixture_name = fixture_import_statement.split(" import ")[-1].strip()
            init_params_str = ", ".join(init_params)
            example_values = [f"mock_{param}" for param in init_params]
            example_params_str = ", ".join(example_values)
            return fixture_name, init_params_str, example_values, example_params_str

        def create_test_components(
            fixture_name, init_params_str, example_values, example_params_str
        ):
            test_function = f"def test_{class_name.lower()}_init({fixture_name}):"

            fixture_usage = f"""
            # Use the fixture to get correctly typed dependencies
            dependencies = {fixture_name}()
            """

            init_test = f"""
            # Create an instance of the actual class
            instance = {class_name}(**dependencies.__dict__)
            """

            param_assertions = "".join(
                f"""
            assert hasattr(instance, '{param}')
            assert instance.{param} == dependencies.{param}
                """
                for param in init_params
                if param != "kwargs"
            )

            attr_assertions = "".join(
                f"""
            assert hasattr(instance, '{attr}')
                """
                for attr in class_attributes
            )

            base_class_assertions = "".join(
                f"""
            assert isinstance(instance, {base_class})
                """
                for base_class in base_classes
            )

            return (
                test_function,
                fixture_usage,
                init_test,
                param_assertions,
                attr_assertions,
                base_class_assertions,
            )

        def test_output(components):
            (
                test_function,
                fixture_usage,
                init_test,
                param_assertions,
                attr_assertions,
                base_class_assertions,
            ) = components

            example = f"""
            To test the {class_name} class initialization, use the pre-defined fixture:
            {fixture_import_statement}

            {test_function}
            {fixture_usage}
                # Test initialization
            {init_test}
                # Test if the initialization parameters are set correctly
            {param_assertions}
                # Test class attributes
            {attr_assertions}
                # Test inheritance
            {base_class_assertions}
            """
            return example

        # Execute the ACT framework
        analyzed_inputs = analyze_inputs()
        test_components = create_test_components(*analyzed_inputs)
        final_output = test_output(test_components)

        return final_output

    def provide_async_or_sync_mocking_structure(
        self,
        is_coroutine: bool,
        class_name: str,
        class_relative_path: str,
        func_name: str,
        method_name: str,
        init_example: str,
        init_params: List[str] = [],
        class_model: Optional[class_data_model.ClassDataModel] = None,
        func_attributes: Optional[model.FunctionAttributes] = None,
    ) -> str:
        if method_name == "__init__" and init_example:
            return init_example

        return self.provide_test_structure(
            is_coroutine,
            class_name,
            class_relative_path,
            func_name,
            method_name,
            func_attributes.function_params,
            init_params,
            func_attributes.function_return_type,
            class_model,
            func_attributes,
        )

    def generate_system_prompt_no_existing_function(
        self,
        query: str,
        goal: str,
        function_attributes: model.FunctionAttributes,
    ) -> str:
        return f"""You are an expert Python code generator. Your task is to create Python code that solves a specific problem using a provided function signature.
        Follow these instructions carefully:

        1. Function Details:
        Function Name: {function_attributes.func_name}
        Function is async coroutine: {function_attributes.is_coroutine}
        Signature: {function_attributes.function_signature}
        Docstring: {function_attributes.function_docstring}

        2. Task: {query} - with {goal}

        {self.return_analyis_and_guidelines()}

        Fixtures are not meant to be called directly,
        but are created automatically when test functions request them as parameters.

        Example of expected response format:

        {self.return_example_output(create_function=True, create_pytests=True)}

        Remember to provide the main function implementation, expected output, and pytest tests as described above.
        Ensure 100% code coverage for the function being tested."""

    def generate_clarification_prompt(
        self,
        query: str,
        error_message: str,
        coverage_report: Dict[str, Any],
        previous_code: str,
        pytest_tests: str,
        function_attributes: model.FunctionAttributes,
        fixture_import_paths: Dict[str, str],
        unit_test_coverage_missing: Dict[Tuple[int, int], str],
    ) -> str:
        base_prompt = f"""
        The previous response encountered issues. Please address the following problems and improve the code:

        Task: {query}
        1. Function Details:
        Function Name: {function_attributes.func_name}
        Function is async coroutine: {function_attributes.is_coroutine}
        Signature: {function_attributes.function_signature}
        Docstring: {function_attributes.function_docstring}
        Function Body:
        {function_attributes.function_body}

        2. Existing Imports and Fixtures:
        Base Class Fixture Import Paths: {fixture_import_paths}

        IMPORTANT: Use the existing imports. The fixture provides mocked dependencies for the {function_attributes.class_name} class.
        We want to test a live version of the {function_attributes.class_name} class, using the fixture to provide mocked dependencies.
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
        4. Separate the code and tests into different sections for clarity, divided by a line with only:
            ### START OF TESTS

        IMPORTANT: When writing tests, use the existing fixture to provide mocked dependencies, but test the live {function_attributes.class_name} class. Here's an example of how to structure a test:

        def test_{function_attributes.func_name}_example(fixture_mock_dependencies):
            # Use the fixture to get mocked dependencies
            mocked_dep1, mocked_dep2 = fixture_mock_dependencies

            # Create a live instance of the class using mocked dependencies
            instance = {function_attributes.class_name}(mocked_dep1, mocked_dep2)

            # Your test code here, using the live 'instance'
            result = instance.{function_attributes.func_name}(test_input)
            assert result == expected_output


        Remember to handle all possible scenarios, including:
        - Empty inputs (e.g., empty DataFrames, empty columns)
        - Invalid inputs (e.g., non-existent columns, incorrect data types)
        - Edge cases (e.g., very large or very small values, NaN values)
        - Various data types (e.g., integers, floats, strings, dates)

        Ensure that your implementation is robust and handles errors gracefully.

        Make sure to test the actual behavior of the {function_attributes.class_name} class, not just the mocked responses.
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

    @staticmethod
    def return_analyis_and_guidelines() -> str:
        """Return the standard prompt for analysis and guidelines."""
        return """
        3. Code Generation Guidelines:
        - Implement the function according to the given signature.
        - Ensure all function arguments have their types explicitly mentioned.
        - Create any necessary additional code to solve the task.
        - Ensure the code is efficient, readable, and follows Python best practices.
        - Include proper error handling if appropriate.
        - Add brief, inline comments for clarity if needed.
        - If any of the function args are pandas.DataFrame, pandas.Series, verify the index.
        - Use absolute imports for all import statements.

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
        9. Do not use any fixtures that are not explicitly defined within the test file or imported from a known source. Specifically:
            - Do not use a 'setup' fixture unless you define it in the test file.
            - Do not use a 'mock_init' fixture unless you explicitly define it.
            - Do not use a 'mock_subprocess_run' unless you define it in the test file.
            - If you need setup or teardown operations, include them directly in the test functions or use pytest's built-in fixtures like 'tmp_path' or 'capsys'.
            - If mocking is required, create the mocks within each test function using pytest.mock.patch as a decorator or context manager.
        """

    @staticmethod
    def return_example_output(
        create_function: bool = False,
        create_pytests: bool = False,
        is_async: bool = False,
    ) -> str:
        """Return the example output for either async or sync functions."""
        example_output = ""

        if create_function:
            if is_async:
                example_output += """
        ```python
        # Expected Output: 7
        import pandas as pd
        import numpy as np
        import asyncio

        async def example_async_func(arg1: int, arg2: int) -> int:
            # Simulating some async operation
            await asyncio.sleep(0.1)
            result = arg1 + arg2
            return result


        ### START OF TESTS

        class TestExampleAsyncFunc:
            @pytest.mark.asyncio
            async def test_normal_case(self):
                assert await example_async_func(3, 4) == 7

            @pytest.mark.asyncio
            async def test_edge_case(self):
                assert await example_async_func(-2, -3) == -5

            @pytest.mark.asyncio
            async def test_zero(self):
                assert await example_async_func(0, 0) == 0
        """
        else:
            example_output += """
            # Expected Output: 7
        import pandas as pd
        import numpy as np

        def example_func(arg1: int, arg2: int) -> int:
            # Your code here
            result = arg1 + arg2
            return result

        ### START OF TESTS

        class TestExampleFunc:
            def test_normal_case(self):
                assert example_func(3, 4) == 7

            def test_edge_case(self):
                assert example_func(-2, -3) == -5

            def test_zero(self):
                assert example_func(0, 0) == 0
        """

        if create_pytests:
            if is_async:
                example_output += """
        ### START OF TESTS
        import pytest
        import asyncio

        @pytest.mark.asyncio
        async def test_positive_numbers():
            assert await example_async_func(3, 4) == 7

        @pytest.mark.asyncio
        async def test_negative_numbers():
            assert await example_async_func(-2, -3) == -5

        @pytest.mark.asyncio
        async def test_zero():
            assert await example_async_func(0, 0) == 0

        @pytest.mark.asyncio
        async def test_large_numbers():
            assert await example_async_func(1000000, 2000000) == 3000000

        @pytest.mark.asyncio
        async def test_type_error():
            with pytest.raises(TypeError):
                await example_async_func("3", 4)

        @pytest.mark.asyncio
        async def test_class_normal_case():
            test_instance = TestExampleAsyncFunc()
            await test_instance.test_normal_case()

        To run these tests, use: pytest --asyncio-mode=auto test_file.py
        Remember to provide the main async function implementation, expected output, and pytest tests as described above.
        Ensure 100% code coverage for the async function being tested.
        """
            else:
                example_output += """
                Test the function
                print(example_func(3, 4))
                print(TestExampleFunc().test_normal_case())

                ### START OF TESTS

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
                Ensure 100% code coverage for the function being tested.
                """

        return example_output

    def generate_prompt_for_mock_hierarchy(
        self, class_hierarchy: Dict[str, Any]
    ) -> str:
        """Generate the prompt for mock hierarchy construction."""
        return f"""
        You are an expert Python developer specializing in creating robust testing infrastructures.
        Your task is to create a pytest conftest.py file that defines a hierarchy of mocked classes
        for use in unit tests across a project with complex class inheritance.

        Follow these instructions carefully:

        1. Class Hierarchy:
        The following is a dictionary representing the class hierarchy of the project.
        Each key is a class name, and its value is a dictionary containing information about the class:

        {class_hierarchy}

        2. Task:
        Create a pytest conftest.py file that defines fixtures for mocked versions of each class in the hierarchy.
        Start with classes that have no parent classes, then proceed to classes that inherit from those, and so on.

        3. Guidelines:
        - Use pytest fixtures to define each mocked class.
        - Use unittest.mock.MagicMock or pytest.mock.MagicMock as the base for each mock.
        - For each class, mock all methods and attributes defined in the class_info.
        - If a class has parent classes, ensure the mock inherits from the mocked parent classes.
        - Use the @pytest.fixture decorator for each mock, with an appropriate scope (usually 'function' or 'class').
        - Provide type hints for all fixtures.
        - Add docstrings to each fixture explaining its purpose and usage.

        4. Example Structure:
        ```python
        import pytest
        from unittest.mock import MagicMock

        @pytest.fixture
        def mock_base_class():
            class MockBaseClass(MagicMock):
                # Mock methods and attributes
            return MockBaseClass()

        @pytest.fixture
        def mock_derived_class(mock_base_class):
            class MockDerivedClass(MagicMock):
                # Mock methods and attributes
            mock = MockDerivedClass()
            mock.__class__ = mock_base_class.__class__  # Simulate inheritance
            return mock

        5. Output:
        Provide the complete content of the conftest.py file, including all necessary imports and fixtures.

        6. Additional Notes:
        Ensure that the mocking strategy allows for easy customization in specific tests.
        Consider using parameterized fixtures if multiple classes share similar mocking needs.
        Provide comments explaining any complex mocking setups or inheritance simulations.

        Remember, the goal is to create a flexible and maintainable set of mocks that can be easily used across all unit tests in the project."""
