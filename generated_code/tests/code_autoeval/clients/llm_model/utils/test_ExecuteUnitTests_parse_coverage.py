import re
from typing import Any, Dict
from unittest.mock import patch

import pytest


class CoverageParsingError(Exception):
    pass

class ExecuteUnitTests:
    def __init__(self, data: Any) -> None:
        self.data = data

    async def parse_coverage(self, output: str, target_file: str) -> Dict[str, int]:
        coverage_data = {}

        # Remove ANSI escape codes
        ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
        clean_output = ansi_escape.sub("", output)

        for line in clean_output.split("\n"):
            if "TOTAL" in line:
                parts = line.split()
                # Find the part that contains the coverage percentage
                for part in parts:
                    if part.endswith("%"):
                        try:
                            coverage_percentage = int(part.rstrip("%"))
                            coverage_data[target_file] = coverage_percentage
                        except ValueError as ve:
                            print(f"Error parsing coverage percentage for {target_file}: {ve}")
                            print(f"Line content: {line}")
                        break

        if not coverage_data:
            raise CoverageParsingError("Coverage information not found in the output.")

        if target_file not in coverage_data:
            raise CoverageParsingError(f"Coverage for {target_file} not found in the output.")

        return coverage_data

##################################################
# TESTS
##################################################

@patch("code_autoeval.clients.llm_model.utils.execute_unit_tests.ExecuteUnitTests.__init__", return_value=None)
def test_parse_coverage_normal_case(mock_init):
    # Arrange
    mock_output = "File1 80%\nFile2 90%\nTOTAL 85%"
    target_file = "File1"
    expected_result = {"File1": 80}
    execute_unit_tests = ExecuteUnitTests(None)

    # Act
    result = execute_unit_tests.parse_coverage(mock_output, target_file)

    # Assert
    assert result == expected_result

def test_parse_coverage_missing_target_file():
    # Arrange
    mock_output = "File1 80%\nFile2 90%"
    target_file = "File3"
    execute_unit_tests = ExecuteUnitTests(None)

    # Act & Assert
    with pytest.raises(CoverageParsingError):
        execute_unit_tests.parse_coverage(mock_output, target_file)

def test_parse_coverage_no_total():
    # Arrange
    mock_output = "File1 80%\nFile2 90%"
    target_file = "File1"
    execute_unit_tests = ExecuteUnitTests(None)

    # Act & Assert
    with pytest.raises(CoverageParsingError):
        execute_unit_tests.parse_coverage(mock_output, target_file)

def test_parse_coverage_invalid_percentage():
    # Arrange
    mock_output = "File1 80%\nFile2 invalid\nTOTAL 85%"
    target_file = "File1"
    execute_unit_tests = ExecuteUnitTests(None)

    # Act & Assert
    with pytest.raises(ValueError):
        execute_unit_tests.parse_coverage(mock_output, target_file)

def test_parse_coverage_empty_output():
    # Arrange
    mock_output = ""
    target_file = "File1"
    execute_unit_tests = ExecuteUnitTests(None)

    # Act & Assert
    with pytest.raises(CoverageParsingError):
        execute_unit_tests.parse_coverage(mock_output, target_file)