import re
from typing import Dict, Any
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

# Test cases for ExecuteUnitTests.parse_coverage function
@pytest.mark.asyncio
async def test_parse_coverage_normal():
    # Arrange
    output = "File1 80%\nFile2 90%\nTOTAL 85%"
    target_file = "File1"
    execute_unit_tests = ExecuteUnitTests(None)

    # Act
    result = await execute_unit_tests.parse_coverage(output, target_file)

    # Assert
    assert result == {"File1": 80}

@pytest.mark.asyncio
async def test_parse_coverage_no_total():
    # Arrange
    output = "File1 80%\nFile2 90%"
    target_file = "File1"
    execute_unit_tests = ExecuteUnitTests(None)

    # Act & Assert
    with pytest.raises(CoverageParsingError):
        await execute_unit_tests.parse_coverage(output, target_file)

@pytest.mark.asyncio
async def test_parse_coverage_invalid_percentage():
    # Arrange
    output = "File1 80%\nFile2 invalid\nTOTAL 85%"
    target_file = "File1"
    execute_unit_tests = ExecuteUnitTests(None)

    # Act & Assert
    with pytest.raises(ValueError):
        await execute_unit_tests.parse_coverage(output, target_file)

@pytest.mark.asyncio
async def test_parse_coverage_no_files():
    # Arrange
    output = "TOTAL 85%"
    target_file = "File1"
    execute_unit_tests = ExecuteUnitTests(None)

    # Act & Assert
    with pytest.raises(CoverageParsingError):
        await execute_unit_tests.parse_coverage(output, target_file)

@pytest.mark.asyncio
async def test_parse_coverage_empty_output():
    # Arrange
    output = ""
    target_file = "File1"
    execute_unit_tests = ExecuteUnitTests(None)

    # Act & Assert
    with pytest.raises(CoverageParsingError):
        await execute_unit_tests.parse_coverage(output, target_file)