import re
from typing import Optional, Tuple


class ParseUnitTestCoverage:
    def _find_function_bounds(self, file_path: str, function_name: str) -> Optional[Tuple[int, int]]:
        """
        Finds the starting and ending line numbers of a given function in a Python file.

        Args:
            self (ParseUnitTestCoverage): The instance of the class.
            file_path (str): Path to the Python file.
            function_name (str): Name of the function to find bounds for.

        Returns:
            Optional[Tuple[int, int]]: A tuple containing the start and end line numbers if found, otherwise None.
        """
        try:
            with open(file_path, "r") as file:
                lines = file.readlines()
        except FileNotFoundError:
            return None

        start_line = None
        end_line = None
        in_function = False
        indent_level = 0

        for i, line in enumerate(lines):
            if re.match(rf"\s*def\s+{re.escape(function_name)}\s*\(", line):
                start_line = i + 1
                in_function = True
                indent_level = len(line) - len(line.lstrip())
            elif in_function:
                if line.strip() and len(line.lstrip()) <= indent_level:
                    end_line = i
                    break

        return (start_line, end_line) if start_line and end_line else None

from unittest.mock import mock_open, patch

import pytest

from code_autoeval.llm_model.utils.extraction.parse_unit_test_coverage import \
    ParseUnitTestCoverage


@pytest.fixture
def parse_unit_test_coverage():
    return ParseUnitTestCoverage()

def test_find_function_bounds_normal(parse_unit_test_coverage):
    with patch("builtins.open", mock_open(read_data="line1\nline2\ndef example_func():\n  pass\nline3")):
        result = parse_unit_test_coverage._find_function_bounds("dummy_file.py", "example_func")
        assert result == (3, 4)

def test_find_function_bounds_not_found(parse_unit_test_coverage):
    with patch("builtins.open", mock_open(read_data="line1\nline2\nline3")):
        result = parse_unit_test_coverage._find_function_bounds("dummy_file.py", "example_func")
        assert result is None

def test_find_function_bounds_empty_file(parse_unit_test_coverage):
    with patch("builtins.open", mock_open(read_data="")):
        result = parse_unit_test_coverage._find_function_bounds("dummy_file.py", "example_func")
        assert result is None

def test_find_function_bounds_no_function(parse_unit_test_coverage):
    with patch("builtins.open", mock_open(read_data="line1\nline2\nline3")):
        result = parse_unit_test_coverage._find_function_bounds("dummy_file.py", "example_func")
        assert result is None

def test_find_function_bounds_exception(parse_unit_test_coverage):
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = parse_unit_test_coverage._find_function_bounds("dummy_file.py", "example_func")
        assert result is None        assert result is None

def test_find_function_bounds_exception(parse_unit_test_coverage):
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = parse_unit_test_coverage._find_function_bounds("dummy_file.py", "example_func")
        assert result is None