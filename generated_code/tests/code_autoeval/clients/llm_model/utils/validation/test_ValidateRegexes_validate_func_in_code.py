import re
from typing import Callable
from unittest.mock import patch

import pytest


@patch(
    "code_autoeval.llm_model.utils.validation.validate_regexes.ValidateRegexes.validate_func_name_in_code",
    return_value=True,
)
def test_normal_case(mock_validate):
    validate = ValidateRegexes()
    code = "def example_function(): pass"
    func = lambda: None  # Mock function
    func.__name__ = "example_function"
    validate.validate_func_in_code(code, func)
    assert mock_validate.called


@patch(
    "code_autoeval.llm_model.utils.validation.validate_regexes.ValidateRegexes.validate_func_name_in_code",
    return_value=False,
)
def test_function_not_found(mock_validate):
    validate = ValidateRegexes()
    code = "def another_function(): pass"
    func = lambda: None  # Mock function
    func.__name__ = "example_function"
    with pytest.raises(ValueError):
        validate.validate_func_in_code(code, func)
    assert mock_validate.called


def test_empty_code():
    validate = ValidateRegexes()
    code = ""
    func = lambda: None  # Mock function
    func.__name__ = "example_function"
    with pytest.raises(ValueError):
        validate.validate_func_in_code(code, func)


def test_nonexistent_function():
    validate = ValidateRegexes()
    code = "def example_function(): pass"
    func = lambda: None  # Mock function
    func.__name__ = "non_existent_function"
    with pytest.raises(ValueError):
        validate.validate_func_in_code(code, func)


@patch(
    "code_autoeval.llm_model.utils.validation.validate_regexes.ValidateRegexes.validate_func_name_in_code",
    return_value=True,
)
def test_large_codebase(mock_validate):
    validate = ValidateRegexes()
    code = "def example_function(): pass\n" * 1000
    func = lambda: None  # Mock function
    func.__name__ = "example_function"
    validate.validate_func_in_code(code, func)
    assert mock_validate.called
