from typing import List
from unittest.mock import MagicMock, patch

import pytest


class AutoFunctionCleaning:
    def __init__(self, data):
        self.data = data

    async def clean_func_args_from_file(self, code: str) -> str:
        # Placeholder for the actual implementation of clean_func_args_from_file
        pass

    def clean_func_args_from_lines(self, code_lines: List[str]) -> List[str]:
        full_code = "\n".join(code_lines)
        cleaned_code = self.clean_func_args_from_file(full_code)
        return cleaned_code.split("\n")


# Analysis of the function:
# The function joins the list of code lines into a single string, cleans it using another method, and then splits the cleaned code back into lines.

##################################################
# TESTS
##################################################


@pytest.fixture
def mock_auto_function_cleaning():
    return AutoFunctionCleaning(None)


@patch(
    "code_autoeval.llm_model.utils.code_cleaning.auto_function_cleaning.AutoFunctionCleaning.clean_func_args_from_file"
)
def test_clean_func_args_from_lines_normal(
    mock_clean_func, mock_auto_function_cleaning
):
    # Arrange
    code_lines = ["line1", "line2", "line3"]
    expected_output = ["cleaned_line1", "cleaned_line2", "cleaned_line3"]
    mock_clean_func.return_value = "\n".join(expected_output)

    # Act
    result = mock_auto_function_cleaning.clean_func_args_from_lines(code_lines)

    # Assert
    assert result == expected_output
    mock_clean_func.assert_called_once_with("\n".join(code_lines))


def test_clean_func_args_from_lines_empty(mock_auto_function_cleaning):
    # Arrange
    code_lines = []
    expected_output = []

    # Act
    result = mock_auto_function_cleaning.clean_func_args_from_lines(code_lines)

    # Assert
    assert result == expected_output


@patch(
    "code_autoeval.llm_model.utils.code_cleaning.auto_function_cleaning.AutoFunctionCleaning.clean_func_args_from_file"
)
def test_clean_func_args_from_lines_with_none(
    mock_clean_func, mock_auto_function_cleaning
):
    # Arrange
    code_lines = ["line1", None, "line3"]
    expected_output = ["line1", "line3"]
    mock_clean_func.return_value = "\n".join(code_lines).replace(None, "")

    # Act
    result = mock_auto_function_cleaning.clean_func_args_from_lines(code_lines)

    # Assert
    assert result == expected_output


@patch(
    "code_autoeval.llm_model.utils.code_cleaning.auto_function_cleaning.AutoFunctionCleaning.clean_func_args_from_file"
)
def test_clean_func_args_from_lines_with_empty(
    mock_clean_func, mock_auto_function_cleaning
):
    # Arrange
    code_lines = ["line1", "", "line3"]
    expected_output = ["line1", "line3"]
    mock_clean_func.return_value = "\n".join(code_lines).replace("", "")

    # Act
    result = mock_auto_function_cleaning.clean_func_args_from_lines(code_lines)

    # Assert
    assert result == expected_output


@patch(
    "code_autoeval.llm_model.utils.code_cleaning.auto_function_cleaning.AutoFunctionCleaning.clean_func_args_from_file"
)
def test_clean_func_args_from_lines_with_whitespace(
    mock_clean_func, mock_auto_function_cleaning
):
    # Arrange
    code_lines = ["line1", "   ", "line3"]
    expected_output = ["line1", "line3"]
    mock_clean_func.return_value = "\n".join(code_lines).replace("   ", "")

    # Act
    result = mock_auto_function_cleaning.clean_func_args_from_lines(code_lines)

    # Assert
    assert result == expected_output  # Assert
    assert result == expected_output
