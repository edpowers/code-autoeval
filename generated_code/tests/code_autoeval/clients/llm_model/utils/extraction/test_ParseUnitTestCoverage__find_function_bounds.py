# Updated Implementation of ParseUnitTestCoverage._find_function_bounds Function
import re
from typing import Optional, Tuple


class ParseUnitTestCoverage:
    def _find_function_bounds(self, file_path: str, function_name: str) -> Optional[Tuple[int, int]]:
        try:
            with open(file_path, "r") as file:
                lines = file.readlines()
        except FileNotFoundError:
            return None  # Return None if the file does not exist

        start_line = None
        end_line = None
        in_function = False
        indent_level = 0

        for i, line in enumerate(lines, 1):
            if re.match(rf"\s*def\s+{re.escape(function_name)}\s*\(", line):
                start_line = i
                in_function = True
                indent_level = len(line) - len(line.lstrip())
            elif in_function:
                if line.strip() and len(line) - len(line.lstrip()) <= indent_level:
                    end_line = i - 1
                    break

        return (start_line, end_line) if start_line and end_line else None

##################################################
# TESTS
##################################################

from unittest.mock import mock_open, patch

import pytest


@patch("builtins.open", new_callable=mock_open, read_data="def test_func():\n    pass\ndef other_func():\n    pass")
def test_find_function_bounds_normal(mock_file):
    parser = ParseUnitTestCoverage()
    result = parser._find_function_bounds("fake_path", "test_func")
    assert result == (1, 1)

@patch("builtins.open", new_callable=mock_open, read_data="def test_func():\n    pass\ndef other_func():\n    pass")
def test_find_function_bounds_nonexistent_function(mock_file):
    parser = ParseUnitTestCoverage()
    result = parser._find_function_bounds("fake_path", "non_existent_func")
    assert result is None

@patch("builtins.open", new_callable=mock_open, read_data="def test_func():\n pass\ndef other_func():\n  pass")
def test_find_function_bounds_no_indentation(mock_file):
    parser = ParseUnitTestCoverage()
    result = parser._find_function_bounds("fake_path", "other_func")
    assert result == (2, 2)

@patch("builtins.open", new_callable=mock_open, read_data="def test_func():\n pass\n def other_func():\n   pass")
def test_find_function_bounds_multiple_functions(mock_file):
    parser = ParseUnitTestCoverage()
    result = parser._find_function_bounds("fake_path", "other_func")
    assert result == (3, 3)

@patch("builtins.open", new_callable=mock_open, read_data="def test_func():\n pass\ndef other_func():\n pass\n")
def test_find_function_bounds_empty_body(mock_file):
    parser = ParseUnitTestCoverage()
    result = parser._find_function_bounds("fake_path", "other_func")
    assert result == (2, 2)

@patch("builtins.open", new_callable=mock_open, read_data="def test_func():\n pass\ndef other_func():\n pass\n")
def test_find_function_bounds_file_not_found(mock_file):
    parser = ParseUnitTestCoverage()
    result = parser._find_function_bounds("non_existent_path", "test_func")
    assert result is None