# Updated Implementation of PreProcessCodeBeforeExecution.split_main_and_example function
import re
from typing import Tuple


class PreProcessCodeBeforeExecution:
    def split_main_and_example(self, code: str) -> Tuple[set, set]:
        problematic_lines = set()
        undefined_names = set()

        # Split the code into lines for easier processing
        lines = code.splitlines()

        # Regular expression to match undefined names and imported but unused modules
        undefined_name_pattern = re.compile(r"undefined name '([^']+)'")
        imported_but_unused_pattern = re.compile(r"imported but unused '([^']+)")

        for line in lines:
            # Check for undefined names
            match = undefined_name_pattern.search(line)
            if match:
                name = match.group(1)
                if len(name) > 2:  # Ensure the name is meaningful
                    undefined_names.add(name)

            # Check for imported but unused modules
            match = imported_but_unused_pattern.search(line)
            if match and "undefined name" not in line:
                module = match.group(1)
                problematic_lines.add(lines.index(line) + 1)  # Line numbers are 1-based

        return problematic_lines, undefined_names


from unittest.mock import patch

# Updated pytest tests for the PreProcessCodeBeforeExecution.split_main_and_example function
import pytest

from code_autoeval.llm_model.utils.preprocess_code_before_execution import (
    PreProcessCodeBeforeExecution,
)


@patch(
    "code_autoeval.llm_model.utils.preprocess_code_before_execution.PreProcessCodeBeforeExecution.__init__",
    return_value=None,
)
def test_normal_use_case(mock_init):
    flake8_output = """example.py:2: F401 'os' imported but unused
example.py:3: F821 undefined name 'undefined_var'
example.py:5: E231 missing whitespace around ','
"""
    preprocess = PreProcessCodeBeforeExecution()
    problematic_lines, undefined_names = preprocess.split_main_and_example(
        flake8_output
    )

    assert problematic_lines == {2}
    assert undefined_names == {"undefined_var"}


def test_no_errors():
    flake8_output = """example.py:1: F401 'os' imported but unused
"""
    preprocess = PreProcessCodeBeforeExecution()
    problematic_lines, undefined_names = preprocess.split_main_and_example(
        flake8_output
    )

    assert not problematic_lines
    assert not undefined_names


def test_no_undefined_names():
    flake8_output = """example.py:2: F401 'os' imported but unused
example.py:3: E231 missing whitespace around ','
"""
    preprocess = PreProcessCodeBeforeExecution()
    problematic_lines, undefined_names = preprocess.split_main_and_example(
        flake8_output
    )

    assert problematic_lines == {3}
    assert not undefined_names


def test_no_problematic_lines():
    flake8_output = """example.py:1: F401 'os' imported but unused
example.py:2: F821 undefined name 'undefined_var'
"""
    preprocess = PreProcessCodeBeforeExecution()
    problematic_lines, undefined_names = preprocess.split_main_and_example(
        flake8_output
    )

    assert not problematic_lines
    assert undefined_names == {"undefined_var"}


def test_empty_input():
    flake8_output = ""
    preprocess = PreProcessCodeBeforeExecution()
    problematic_lines, undefined_names = preprocess.split_main_and_example(
        flake8_output
    )

    assert not problematic_lines
    assert not undefined_names


def test_undefined_name_with_quotes():
    flake8_output = """example.py:2: F821 undefined name 'quote'"""
    preprocess = PreProcessCodeBeforeExecution()
    problematic_lines, undefined_names = preprocess.split_main_and_example(
        flake8_output
    )

    assert not problematic_lines
    assert undefined_names == {"quote"}


def test_imported_but_unused():
    flake8_output = """example.py:1: F401 'os' imported but unused"""
    preprocess = PreProcessCodeBeforeExecution()
    problematic_lines, undefined_names = preprocess.split_main_and_example(
        flake8_output
    )

    assert problematic_lines == {1}
    assert not undefined_names
    assert problematic_lines == {1}
    assert not undefined_names
