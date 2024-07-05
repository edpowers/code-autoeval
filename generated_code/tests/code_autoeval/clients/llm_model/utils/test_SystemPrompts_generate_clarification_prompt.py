import json
from unittest.mock import MagicMock, patch

import pytest
from code_autoeval.clients.llm_model.utils.model.function_attributes import FunctionAttributes
from code_autoeval.clients.llm_model.utils.system_prompts import SystemPrompts


def test_generate_clarification_prompt():
    # Mock data for testing
    query = "Example task"
    error_message = "Error message example"
    coverage_report = {'total_coverage': 90, 'uncovered_lines': ['line1', 'line2']}
    previous_code = "Previous code example"
    pytest_tests = "Existing pytest tests"
    function_attributes = FunctionAttributes(function_signature="def func():", is_coroutine=False, function_docstring="Example docstring")
    unit_test_coverage_missing = {('1', '5'): "Code snippet"}
    
    # Create an instance of SystemPrompts for testing
    system_prompts = SystemPrompts()
    
    # Call the method under test
    result = system_prompts.generate_clarification_prompt(query, error_message, coverage_report, previous_code, pytest_tests, function_attributes, unit_test_coverage_missing)
    
    # Check if the result is a string and contains expected data
    assert isinstance(result, str), "Expected result to be a string"
    assert query in result, "Expected query to be included in the prompt"
    assert error_message in result, "Expected error message to be included in the prompt"
    assert coverage_report['total_coverage'] in result, "Expected total coverage to be included in the prompt"
    assert previous_code in result, "Expected previous code to be included in the prompt"
    assert pytest_tests in result, "Expected existing pytest tests to be included in the prompt"
    assert function_attributes.function_signature in result, "Expected function signature to be included in the prompt"
    assert unit_test_coverage_missing[('1', '5')] in result, "Expected uncovered code snippet to be included in the prompt"

# Additional tests for edge cases and error conditions can be added here