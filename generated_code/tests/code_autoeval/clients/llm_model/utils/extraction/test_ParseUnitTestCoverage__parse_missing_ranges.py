from typing import List, Tuple
from unittest.mock import patch

import pytest


class ParseUnitTestCoverage:
    def __init__(self, data):
        self.data = data

    async def _parse_missing_ranges(self, missing_ranges: str) -> List[Tuple[int, int]]:
        parsed_ranges = []

        for range_str in missing_ranges.split(", "):
            if "-" in range_str:
                start, end = map(int, range_str.split("-"))
                parsed_ranges.append((start, end))
            else:
                line_num = int(range_str)
                parsed_ranges.append((line_num, line_num))
        return parsed_ranges

##################################################
# TESTS
##################################################

@patch("code_autoeval.clients.llm_model.utils.extraction.parse_unit_test_coverage.ParseUnitTestCoverage.__init__", return_value=None)
def test_normal_case(mock_init):
    parser = ParseUnitTestCoverage("data")
    missing_ranges = "1, 3-5, 7"
    expected_output = [(1, 1), (3, 5), (7, 7)]
    assert parser._parse_missing_ranges(missing_ranges) == expected_output

def test_single_line():
    missing_ranges = "8"
    expected_output = [(8, 8)]
    parser = ParseUnitTestCoverage("data")
    assert parser._parse_missing_ranges(missing_ranges) == expected_output

def test_empty_string():
    missing_ranges = ""
    expected_output = []
    parser = ParseUnitTestCoverage("data")
    assert parser._parse_missing_ranges(missing_ranges) == expected_output

def test_invalid_range():
    missing_ranges = "10-abc, 12"
    with pytest.raises(ValueError):
        parser = ParseUnitTestCoverage("data")
        parser._parse_missing_ranges(missing_ranges)

def test_multiple_ranges():
    missing_ranges = "20-25, 30, 40-45"
    expected_output = [(20, 25), (30, 30), (40, 45)]
    parser = ParseUnitTestCoverage("data")
    assert parser._parse_missing_ranges(missing_ranges) == expected_output