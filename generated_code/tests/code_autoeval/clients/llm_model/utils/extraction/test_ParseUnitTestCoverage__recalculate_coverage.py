from typing import Dict, Tuple
from unittest.mock import patch

import pytest
from code_autoeval.clients.llm_model.utils.extraction.parse_unit_test_coverage import ParseUnitTestCoverage


# Updated implementation of the _recalculate_coverage method
def _recalculate_coverage(self, range_string: str, concerned_lines: Dict[Tuple[int, int], str]) -> float:
    def parse_range(s):
        result = []
        for part in s.split(","):
            if "-" in part:
                a, b = map(int, part.split("-"))
                result.extend(range(a, b + 1))
            else:
                a = int(part)
                result.append(a)
        return set(result)

    # Parse the range string
    all_lines = parse_range(range_string)

    # Convert concerned_lines to a set of line numbers
    concerned_set = {line for ranges in concerned_lines.keys() for line in ranges}

    # Find the intersection of all_lines and concerned_lines
    covered_lines = all_lines.intersection(concerned_set)

    # Calculate coverage
    if not concerned_set:
        return 100.0  # If there are no lines to be concerned about, consider it 100% covered

    coverage_percentage = (len(covered_lines) / len(concerned_set)) * 100

    return coverage_percentage

# Test for normal use case
def test_normal_use_case(setup):
    range_string = "1,2-3"
    concerned_lines = {(1, 2), (2, 3)}
    result = setup._recalculate_coverage(range_string, concerned_lines)
    assert pytest.approx(result, abs=0.01) == 66.67

# Test for edge case with no coverage
def test_no_coverage(setup):
    range_string = "4-5"
    concerned_lines = {(1, 2), (3, 4)}
    result = setup._recalculate_coverage(range_string, concerned_lines)
    assert pytest.approx(result, abs=0.01) == 0.00

# Test for edge case with full coverage
def test_full_coverage(setup):
    range_string = "1-3"
    concerned_lines = {(1, 2), (2, 3)}
    result = setup._recalculate_coverage(range_string, concerned_lines)
    assert pytest.approx(result, abs=0.01) == 100.00

# Test for edge case with empty range string
def test_empty_range_string(setup):
    range_string = ""
    concerned_lines = {(1, 2), (2, 3)}
    result = setup._recalculate_coverage(range_string, concerned_lines)
    assert pytest.approx(result, abs=0.01) == 100.00

# Test for edge case with empty concerned lines
def test_empty_concerned_lines(setup):
    range_string = "1-3"
    concerned_lines = {}
    result = setup._recalculate_coverage(range_string, concerned_lines)
    assert pytest.approx(result, abs=0.01) == 100.00