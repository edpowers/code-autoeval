import re
from typing import Any, Dict
from unittest.mock import MagicMock, patch

import pytest


class ExecuteUnitTests:
    def __init__(self, data):
        self.data = data
        self.coverage_result = MagicMock()
    
    async def get_coverage_report(self, function_name: str) -> Dict[str, Any]:
        # Initialize default values
        total_coverage = 0
        uncovered_lines = "None"

        # Parse the coverage report
        coverage_output = self.coverage_result.stdout

        # Find the line containing coverage information for our function
        coverage_pattern = rf"{function_name}\.py\s+\d+\s+\d+\s+(\d+)%\s+([\d,-]+)?"

        if match := re.search(coverage_pattern, coverage_output):
            total_coverage = int(match[1])
            uncovered_lines = match[2] or "None"

        # Extract test results summary
        test_summary = re.search(
            r"(=+ .*? =+)$", coverage_output, re.MULTILINE | re.DOTALL
        )
        test_summary = test_summary[1] if test_summary else "No test summary available."

        return {
            "total_coverage": total_coverage,
            "uncovered_lines": uncovered_lines,
            "test_summary": test_summary,
            "full_output": coverage_output,
        }

##################################################
# TESTS
##################################################

@patch("code_autoeval.clients.llm_model.utils.execute_unit_tests.ExecuteUnitTests.__init__", return_value=None)
def test_get_coverage_report_normal(mock_init):
    # Arrange
    mock_instance = ExecuteUnitTests(data="test_data")
    mock_instance.coverage_result = MagicMock()
    mock_instance.coverage_result.stdout = "FunctionName.py 10 20 80% 1-3,5"
    
    # Act
    result = mock_instance.get_coverage_report("FunctionName")
    
    # Assert
    assert result["total_coverage"] == 80
    assert result["uncovered_lines"] == "1-3,5"
    assert result["test_summary"] == "No test summary available."
    assert result["full_output"] == "FunctionName.py 10 20 80% 1-3,5"

@patch("code_autoeval.clients.llm_model.utils.execute_unit_tests.ExecuteUnitTests.__init__", return_value=None)
def test_get_coverage_report_no_coverage(mock_init):
    # Arrange
    mock_instance = ExecuteUnitTests(data="test_data")
    mock_instance.coverage_result = MagicMock()
    mock_instance.coverage_result.stdout = "FunctionName.py 10 20 No coverage information"
    
    # Act
    result = mock_instance.get_coverage_report("FunctionName")
    
    # Assert
    assert result["total_coverage"] == 0
    assert result["uncovered_lines"] == "None"
    assert result["test_summary"] == "No test summary available."
    assert result["full_output"] == "FunctionName.py 10 20 No coverage information"

@patch("code_autoeval.clients.llm_model.utils.execute_unit_tests.ExecuteUnitTests.__init__", return_value=None)
def test_get_coverage_report_no_match(mock_init):
    # Arrange
    mock_instance = ExecuteUnitTests(data="test_data")
    mock_instance.coverage_result = MagicMock()
    mock_instance.coverage_result.stdout = "No function name match"
    
    # Act
    result = mock_instance.get_coverage_report("FunctionName")
    
    # Assert
    assert result["total_coverage"] == 0
    assert result["uncovered_lines"] == "None"
    assert result["test_summary"] == "No test summary available."
    assert result["full_output"] == "No function name match"

@patch("code_autoeval.clients.llm_model.utils.execute_unit_tests.ExecuteUnitTests.__init__", return_value=None)
def test_get_coverage_report_empty_stdout(mock_init):
    # Arrange
    mock_instance = ExecuteUnitTests(data="test_data")
    mock_instance.coverage_result = MagicMock()
    mock_instance.coverage_result.stdout = ""
    
    # Act
    result = mock_instance.get_coverage_report("FunctionName")
    
    # Assert
    assert result["total_coverage"] == 0
    assert result["uncovered_lines"] == "None"
    assert result["test_summary"] == "No test summary available."
    assert result["full_output"] == ""