import traceback
from typing import Optional


class ExtractContextFromException:
    def __init__(self):
        pass

    def format_error(self, exception: Exception, generated_code: Optional[str] = None, context_lines: int = 3) -> str:
        if exception is None:
            raise AttributeError("Exception object cannot be None")
        
        tb = traceback.extract_tb(exception.__traceback__)
        error_type = type(exception).__name__
        error_message = str(exception)

        # Get the most recent frame from the traceback
        last_frame = tb[-1]
        filename, line_number, func_name, text = last_frame

        formatted_description = f"""
        Error Type: {error_type}
        Error Message: {error_message}

        Error occurred in file: {filename}
        At line number: {line_number}
        In function: {func_name}

        Full traceback:
        {traceback.format_exc()}
        """

        if generated_code:
            relevant_code = self._get_relevant_code(generated_code, line_number, context_lines=context_lines)
            formatted_description += f"""
        Relevant code context:
        {relevant_code}

        Generated code that caused the error:
        {generated_code}
        """

        return formatted_description.strip()

    def _get_relevant_code(self, generated_code: str, line_number: int, context_lines: int = 3) -> str:
        if not isinstance(context_lines, int) or context_lines < 0:
            raise ValueError("Context lines must be a non-negative integer")
        
        if not generated_code:
            return ""
        
        lines = generated_code.split('\n')
        start_line = max(1, line_number - context_lines)
        end_line = min(len(lines), line_number + context_lines)

        relevant_code = ''
        for i in range(start_line - 1, end_line):
            relevant_code += f"{i+1:>4}: {lines[i]}\n"

        return relevant_code.strip()

from unittest.mock import patch

import pytest


# Mocking the ExtractContextFromException class and its dependencies
@patch("traceback.extract_tb")
@patch("type(exception).__name__", return_value="ExceptionType")
@patch("str(exception)", return_value="Error message")
def test_format_error_normal_case(mock_str, mock_type, mock_extract_tb):
    # Arrange
    exception = Exception("Error message")
    generated_code = "print('Hello, World!')"
    context_lines = 3
    instance = ExtractContextFromException()

    # Act
    result = instance.format_error(exception, generated_code, context_lines)

    # Assert
    expected_output = """
    Error Type: ExceptionType
    Error Message: Error message

    Error occurred in file: <doctest temp_generated_code.py[0]>
    At line number: 1
    In function: <module>

    Full traceback:
    Traceback (most recent call last):
      File "<doctest temp_generated_code.py[0]>", line 1, in <module>
        print('Hello, World!')
    Exception: Error message

    Relevant code context:
         1: print('Hello, World!')

    Generated code that caused the error:
    print('Hello, World!')
    """
    assert result == expected_output.strip()

def test_format_error_no_generated_code():
    # Arrange
    exception = Exception("Error message")
    generated_code = None
    context_lines = 3
    instance = ExtractContextFromException()

    # Act
    result = instance.format_error(exception, generated_code, context_lines)

    # Assert
    expected_output = """
    Error Type: Exception
    Error Message: Error message

    Error occurred in file: <doctest temp_generated_code.py[0]>
    At line number: 1
    In function: <module>

    Full traceback:
    Traceback (most recent call last):
      File "<doctest temp_generated_code.py[0]>", line 1, in <module>
        print('Hello, World!')
    Exception: Error message
    """
    assert result == expected_output.strip()

def test_format_error_empty_exception():
    # Arrange
    exception = None
    generated_code = "print('Hello, World!')"
    context_lines = 3
    instance = ExtractContextFromException()

    # Act & Assert
    with pytest.raises(AttributeError):
        instance.format_error(exception, generated_code, context_lines)

def test_format_error_invalid_context_lines():
    # Arrange
    exception = Exception("Error message")
    generated_code = "print('Hello, World!')"
    context_lines = -1  # Invalid value
    instance = ExtractContextFromException()

    # Act & Assert
    with pytest.raises(ValueError):
        instance.format_error(exception, generated_code, context_lines)