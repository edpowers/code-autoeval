import re


class PreProcessCodeBeforeExecution:
    def __init__(self):
        self.log = []

    def _ensure_double_quotes(self, code: str) -> str:
        """
        Ensure the entire code block is wrapped in double quotes, preserving internal quotes.
        """
        if not isinstance(code, str):
            raise ValueError("Input must be a string")
        
        # Check if the code is already enclosed in double quotes
        if re.match(r'^".*"$', code):
            return code
        
        # Wrap the entire code block in double quotes
        wrapped_code = f'"{code}"'
        return wrapped_code

from unittest.mock import patch

import pytest


@pytest.fixture
def preprocess():
    return PreProcessCodeBeforeExecution()

def test_ensure_double_quotes_normal(preprocess):
    code = "print('Hello, World!')"
    result = preprocess._ensure_double_quotes(code)
    assert result == '"print(\'Hello, World!\')"'

def test_ensure_double_quotes_empty(preprocess):
    code = ""
    result = preprocess._ensure_double_quotes(code)
    assert result == '""'

def test_ensure_double_quotes_already_wrapped(preprocess):
    code = '"print(\'Hello, World!\')"'
    result = preprocess._ensure_double_quotes(code)
    assert result == '"print(\'Hello, World!\')"'

def test_ensure_double_quotes_invalid_input():
    with pytest.raises(ValueError):
        preprocess = PreProcessCodeBeforeExecution()
        code = 12345  # Invalid input type
        preprocess._ensure_double_quotes(code)