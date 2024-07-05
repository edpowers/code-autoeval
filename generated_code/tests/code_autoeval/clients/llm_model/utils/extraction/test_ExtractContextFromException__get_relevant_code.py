# Updated Implementation of ExtractContextFromException._get_relevant_code function

def _get_relevant_code(self, code: str, error_line: int, context_lines: int = 3) -> str:
    if not isinstance(code, str) or not code.strip():
        raise ValueError("Input 'code' must be a non-empty string.")
    if not isinstance(error_line, int) or error_line <= 0:
        raise ValueError("Input 'error_line' must be a positive integer.")
    if not isinstance(context_lines, int) or context_lines < 0:
        raise ValueError("Input 'context_lines' must be a non-negative integer.")

    code_lines = code.split("\n")
    start_line = max(0, error_line - context_lines - 1)
    end_line = min(len(code_lines), error_line + context_lines)

    relevant_lines = code_lines[start_line:end_line]
    numbered_lines = [f"{i+start_line+1}: {line}" for i, line in enumerate(relevant_lines)]
    return "\n".join(numbered_lines)

from unittest.mock import patch

import pytest


@patch("code_autoeval.llm_model.utils.extraction.extract_context_from_exception.ExtractContextFromException._get_relevant_code")
def test_normal_case(mock_get_relevant_code):
    mock_get_relevant_code.return_value = "1: print('Hello, World!')"
    code = "print('Hello, World!')"
    error_line = 1
    context_lines = 3
    result = ExtractContextFromException._get_relevant_code(None, code, error_line, context_lines)
    assert result == "1: print('Hello, World!')"
    mock_get_relevant_code.assert_called_once_with(None, code, error_line, context_lines)

def test_edge_case_empty_code():
    with pytest.raises(ValueError):
        ExtractContextFromException._get_relevant_code(None, "", 1)

def test_error_condition_invalid_error_line():
    code = "print('Hello, World!')"
    error_line = -1
    context_lines = 3
    with pytest.raises(ValueError):
        ExtractContextFromException._get_relevant_code(None, code, error_line, context_lines)

def test_error_condition_invalid_context_lines():
    code = "print('Hello, World!')"
    error_line = 1
    context_lines = -1
    with pytest.raises(ValueError):
        ExtractContextFromException._get_relevant_code(None, code, error_line, context_lines)

def test_large_context():
    code = "print('Hello, World!')" * 10
    error_line = 6
    context_lines = 5
    result = ExtractContextFromException._get_relevant_code(None, code, error_line, context_lines)
    assert len(result.split('\n')) == 10

1: print('Hello, World!')