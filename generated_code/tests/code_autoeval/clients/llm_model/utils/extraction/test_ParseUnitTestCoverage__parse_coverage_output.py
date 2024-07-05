import re
from typing import Optional, Tuple


class ParseUnitTestCoverage:
    def _parse_coverage_output(self, coverage_output: str) -> Optional[Tuple[str, str]]:
        """
        Parse the coverage output to extract file path and missing ranges.
        
        This method splits the output line by line and looks for the percentage and missing ranges.
        """
        if not coverage_output:
            return None

        lines = coverage_output.split("\n")

        for line in lines:
            if ".py" in line and "%" in line:
                parts = re.split(r"\s+(\d+%)\s+", line)
                if len(parts) >= 3:
                    file_info = parts[0].strip()
                    missing_ranges = parts[-1].strip()

                    if file_path_match := re.search(r"(/[^\s]+\.py)", file_info):
                        file_path = file_path_match[1]
                        return file_path, missing_ranges

        raise Exception("Failed to parse coverage output.")

from unittest.mock import patch

import pytest


@pytest.fixture
def parse_unit_test_coverage():
    return ParseUnitTestCoverage()

def test_parse_coverage_output_normal(parse_unit_test_coverage):
    coverage_output = """
        /path/to/file1.py    23%   lorem ipsum...
        /path/to/file2.py    45%   lorem ipsum...
    """
    result = parse_unit_test_coverage._parse_coverage_output(coverage_output)
    assert isinstance(result, tuple) and len(result) == 2
    assert isinstance(result[0], str) and result[0].endswith('.py')
    assert isinstance(result[1], str)

def test_parse_coverage_output_empty(parse_unit_test_coverage):
    coverage_output = ""
    with pytest.raises(Exception):
        parse_unit_test_coverage._parse_coverage_output(coverage_output)

def test_parse_coverage_output_no_match(parse_unit_test_coverage):
    coverage_output = "No file paths or percentages here."
    with pytest.raises(Exception):
        parse_unit_test_coverage._parse_coverage_output(coverage_output)

def test_parse_coverage_output_none(parse_unit_test_coverage):
    coverage_output = None
    result = parse_unit_test_coverage._parse_coverage_output(coverage_output)
    assert result is None

@patch("code_autoeval.clients.llm_model.utils.extraction.parse_unit_test_coverage.ParseUnitTestCoverage._parse_coverage_output")
def test_run_parse_unit_test_cov(mock_parse):
    mock_parse.return_value = ("/path/to/file.py", "missing ranges")
    instance = ParseUnitTestCoverage()
    result = instance.run_parse_unit_test_cov("coverage output")
    assert result == ("/path/to/file.py", "missing ranges")