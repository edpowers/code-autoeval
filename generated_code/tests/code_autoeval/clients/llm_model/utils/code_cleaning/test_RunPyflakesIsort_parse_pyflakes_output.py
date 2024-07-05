from unittest.mock import patch

import pytest
from code_autoeval.clients.llm_model.utils.code_cleaning.run_pyflakes_isort import RunPyflakesIsort


def test_parse_pyflakes_output_normal():
    output = "Some line\nimported but unused 'os'\nAnother line"
    expected_result = ['os']
    run_pyflakes = RunPyflakesIsort()
    result = run_pyflakes.parse_pyflakes_output(output)
    assert result == expected_result

def test_parse_pyflakes_output_no_unused():
    output = "Some line\nAnother line"
    expected_result = []
    run_pyflakes = RunPyflakesIsort()
    result = run_pyflakes.parse_pyflakes_output(output)
    assert result == expected_result

def test_parse_pyflakes_output_multiple_unused():
    output = "imported but unused 'os'\nimported but unused 'sys'\nAnother line"
    expected_result = ['os', 'sys']
    run_pyflakes = RunPyflakesIsort()
    result = run_pyflakes.parse_pyflakes_output(output)
    assert result == expected_result

def test_parse_pyflakes_output_no_match():
    output = "Some line\nAnother line"
    expected_result = []
    run_pyflakes = RunPyflakesIsort()
    result = run_pyflakes.parse_pyflakes_output(output)
    assert result == expected_result

def test_parse_pyflakes_output_empty():
    output = ""
    expected_result = []
    run_pyflakes = RunPyflakesIsort()
    result = run_pyflakes.parse_pyflakes_output(output)
    assert result == expected_result