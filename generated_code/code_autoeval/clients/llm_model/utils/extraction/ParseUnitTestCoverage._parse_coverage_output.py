import re
from typing import Optional, Tuple

class CoverageParsingError(Exception):
    pass

class ParseUnitTestCoverage:
    def __init__(self, data: str):
        self.data = data

    async def _parse_coverage_output(self) -> Optional[Tuple[str, str]]:
        lines = self.data.split("\n")

        for line in lines:
            if ".py" in line and "%" in line:
                parts = re.split(r"\s+(\d+%)\s+", line)
                if len(parts) >= 3:
                    file_info = parts[0].strip()
                    missing_ranges = parts[-1].strip()

                    if file_path_match := re.search(r"(/[^\s]+\.py)", file_info):
                        file_path = file_path_match[1]
                        return file_path, missing_ranges

        raise CoverageParsingError("Failed to parse coverage output - likely due to error running tests.")

import pytest
from unittest.mock import patch

@pytest.fixture
def sample_coverage_output():
    return """
        example/path/to/file.py    10%   loklak.py:234-256, mello.py:12-34
        another/example.py          90%   test_module.py:1-50
    """

@pytest.mark.asyncio
async def test_parse_coverage_output(sample_coverage_output):
    parse_unit_test = ParseUnitTestCoverage(sample_coverage_output)
    result = await parse_unit_test._parse_coverage_output()
    assert result == ('example/path/to/file.py', 'loklak.py:234-256, mello.py:12-34')

@pytest.mark.asyncio
async def test_no_coverage_info(sample_coverage_output):
    parse_unit_test = ParseUnitTestCoverage("No coverage information here.")
    with pytest.raises(CoverageParsingError):
        await parse_unit_test._parse_coverage_output()

@pytest.mark.asyncio
async def test_no_py_files():
    parse_unit_test = ParseUnitTestCoverage("This output does not contain any .py files.")
    with pytest.raises(CoverageParsingError):
        await parse_unit_test._parse_coverage_output()

@pytest.mark.asyncio
async def test_missing_percentage():
    parse_unit_test = ParseUnitTestCoverage("example/path/to/file.py missing percentage")
    with pytest.raises(CoverageParsingError):
        await parse_unit_test._parse_coverage_output()

@pytest.mark.asyncio
async def test_multiple_files():
    sample_output = """
        file1.py 50% loklak.py:234-256, mello.py:12-34
        file2.py 75% another.py:1-50
    """
    parse_unit_test = ParseUnitTestCoverage(sample_output)
    result = await parse_unit_test._parse_coverage_output()
    assert result == ('file1.py', 'loklak.py:234-256, mello.py:12-34')