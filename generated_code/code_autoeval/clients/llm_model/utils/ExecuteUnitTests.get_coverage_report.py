import pytest
from unittest.mock import patch, MagicMock
import re
from typing import Dict, Any

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
        test_summary = re.search(r"(=+ .*? =+)$", coverage_output, re.MULTILINE | re.DOTALL)
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

@pytest.fixture
def setup():
    return ExecuteUnitTests(data="mocked data")

async def test_get_coverage_report_normal(setup):
    # Arrange
    function_name = "test_function"
    mock_stdout = f"{function_name}.py  100%  0"
    setup.coverage_result.stdout = mock_stdout
    
    # Act
    result = await setup.get_coverage_report(function_name)
    
    # Assert
    assert result["total_coverage"] == 100
    assert result["uncovered_lines"] == "0"
    assert result["test_summary"] == "No test summary available."
    assert result["full_output"] == mock_stdout

async def test_get_coverage_report_no_match(setup):
    # Arrange
    function_name = "nonexistent_function"
    mock_stdout = "Some other output without coverage info"
    setup.coverage_result.stdout = mock_stdout
    
    # Act
    result = await setup.get_coverage_report(function_name)
    
    # Assert
    assert result["total_coverage"] == 0
    assert result["uncovered_lines"] == "None"
    assert result["test_summary"] == "No test summary available."
    assert result["full_output"] == mock_stdout

async def test_get_coverage_report_with_uncovered(setup):
    # Arrange
    function_name = "test_function"
    mock_stdout = f"{function_name}.py  90%  1-5,7"
    setup.coverage_result.stdout = mock_stdout
    
    # Act
    result = await setup.get_coverage_report(function_name)
    
    # Assert
    assert result["total_coverage"] == 90
    assert result["uncovered_lines"] == "1-5,7"
    assert result["test_summary"] == "No test summary available."
    assert result["full_output"] == mock_stdout

async def test_get_coverage_report_empty_output(setup):
    # Arrange
    function_name = "test_function"
    mock_stdout = ""
    setup.coverage_result.stdout = mock_stdout
    
    # Act
    result = await setup.get_coverage_report(function_name)
    
    # Assert
    assert result["total_coverage"] == 0
    assert result["uncovered_lines"] == "None"
    assert result["test_summary"] == "No test summary available."
    assert result["full_output"] == mock_stdout

async def test_get_coverage_report_multiple_matches(setup):
    # Arrange
    function_name = "test_function"
    mock_stdout = f"{function_name}.py  90%  1-5,7\nOther unrelated output {function_name}.py  80%  2-6"
    setup.coverage_result.stdout = mock_stdout
    
    # Act
    result = await setup.get_coverage_report(function_name)
    
    # Assert
    assert result["total_coverage"] == 90
    assert result["uncovered_lines"] == "1-5,7"
    assert result["test_summary"] == "No test summary available."
    assert result["full_output"] == mock_stdout