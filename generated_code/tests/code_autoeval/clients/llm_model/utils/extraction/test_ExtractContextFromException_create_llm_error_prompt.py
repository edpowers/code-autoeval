from unittest.mock import patch

import pytest


def create_llm_error_prompt(self, formatted_error: str) -> str:
    if not isinstance(formatted_error, str):
        raise ValueError("formatted_error must be a string")
    
    return f"""
The previous code generation attempt resulted in an error. Here are the details:

{formatted_error}

Please analyze this error and provide a corrected version of the code that addresses the issue.
"""

# Test cases for create_llm_error_prompt function
def test_create_llm_error_prompt_normal():
    # Arrange
    formatted_error = "Error Type: Exception\nError Message: Failed to parse coverage output."
    
    # Act
    result = create_llm_error_prompt(None, formatted_error)
    
    # Assert
    assert "The previous code generation attempt resulted in an error. Here are the details:" in result
    assert "Error Type: Exception" in result
    assert "Error Message: Failed to parse coverage output." in result
    assert "Please analyze this error and provide a corrected version of the code that addresses the issue." in result

def test_create_llm_error_prompt_empty():
    # Arrange
    formatted_error = ""
    
    # Act
    result = create_llm_error_prompt(None, formatted_error)
    
    # Assert
    assert "The previous code generation attempt resulted in an error. Here are the details:" in result
    assert "Please analyze this error and provide a corrected version of the code that addresses the issue." in result

def test_create_llm_error_prompt_none():
    # Arrange
    formatted_error = None
    
    # Act
    with pytest.raises(ValueError):
        create_llm_error_prompt(None, formatted_error)

def test_create_llm_error_prompt_invalid_input():
    # Arrange
    formatted_error = "Invalid input"
    
    # Act
    result = create_llm_error_prompt(None, formatted_error)
    
    # Assert
    assert "The previous code generation attempt resulted in an error. Here are the details:" in result
    assert "Invalid input" in result
    assert "Please analyze this error and provide a corrected version of the code that addresses the issue." in result