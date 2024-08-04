from unittest.mock import MagicMock

import pytest
from code_autoeval.llm_model.utils.prompting.system_prompts import SystemPrompts


@pytest.fixture(scope='module')
def mock_systemprompts():
    return SystemPrompts()

def test_SystemPrompts_generate_clarification_prompt(mock_systemprompts):
    # Arrange
    self = MagicMock()
    query = "Improve the function to handle edge cases."
    error_message = "Execution error encountered: Some unexpected issue."
    coverage_report = {'total_coverage': 80, 'uncovered_lines': ['line1', 'line2']}
    previous_code = "previous code"
    pytest_tests = "existing pytest tests"
    function_attributes = MagicMock()
    function_attributes.func_name = "example_function"
    function_attributes.is_coroutine = False
    function_attributes.function_signature = "(self, arg1: int, arg2: str) -> None"
    function_attributes.function_docstring = "A sample function."
    function_attributes.function_body = """
def example_function(self, arg1: int, arg2: str):
    result = arg1 + len(arg2)
"""
    function_attributes.class_name = "ExampleClass"
    fixture_import_paths = {'DynamicExamplePrompt': 'from generated_code.fixtures.fixtures.dynamicexampleprompt_fixture import fixture_mock_dynamicexampleprompt', 'SystemPrompts': 'from generated_code.fixtures.fixtures.systemprompts_fixture import fixture_mock_systemprompts'}
    unit_test_coverage_missing = {(10, 20): "line to be tested"}

    instance = mock_systemprompts

    # Act
    result = instance.generate_clarification_prompt(self, query, error_message, coverage_report, previous_code, pytest_tests, function_attributes, fixture_import_paths, unit_test_coverage_missing)

    # Assert
    assert isinstance(result, str)
    expected_output = f"""
The previous response encountered issues. Please address the following problems and improve the code:

Task: {query}

1. Function Details:

Function Name: example_function

Function is async coroutine: False

Signature: (self, arg1: int, arg2: str) -> None

Docstring: A sample function.

Function Body:
def example_function(self, arg1: int, arg2: str):
    result = arg1 + len(arg2)
"""
    if "coverage is not 100%" in error_message:
        expected_output += f"""
Current code coverage: {coverage_report['total_coverage']}%

Uncovered lines in example_function.py:

{coverage_report['uncovered_lines']}

To improve coverage:

1. Ensure all branches of conditional statements are tested.
2. Add test cases for edge cases and error conditions.
3. If there are any exception handlers, make sure they are triggered in tests.
4. Check if all parameters of the function are tested with different types of inputs.

Previous pytest tests:

{pytest_tests}

The following lines from the original code are not covered by tests.
Write tests that cover these lines.
"""
        expected_output += "Lines 10-20:\nline to be tested\n"
    else:
        expected_output += f"""
Execution error encountered:
{error_message}

Please review the code and address the following:
1. Check for syntax errors or logical issues in the implementation.
2. Ensure all necessary imports are included.
3. Verify that the function handles all possible input scenarios correctly.

Previous code that generated the error:
{previous_code}
"""
    assert result == expected_output