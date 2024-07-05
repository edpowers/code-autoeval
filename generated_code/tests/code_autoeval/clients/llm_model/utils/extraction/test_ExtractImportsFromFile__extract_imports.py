import ast
from unittest.mock import patch

import pytest
from code_autoeval.clients.llm_model.utils.extraction.extract_imports_from_file import ExtractImportsFromFile


def test_normal_use():
    file_content = """
    import os
    from math import sin, cos
    from submodule import func1 as f1, func2 as f2
    """
    expected_output = {
        'os': "import os",
        'sin': "from math import sin",
        'cos': "from math import cos",
        '(f1, f2)': "from submodule import (f1, f2)"
    }
    extractor = ExtractImportsFromFile()
    result = extractor._extract_imports(file_content)
    assert result == expected_output

def test_no_imports():
    file_content = "print('Hello, World!')"
    expected_output = {}
    extractor = ExtractImportsFromFile()
    result = extractor._extract_imports(file_content)
    assert result == expected_output

def test_malformed_input():
    file_content = "this is not a valid Python code"
    with pytest.raises(SyntaxError):
        extractor = ExtractImportsFromFile()
        extractor._extract_imports(file_content)

def test_empty_input():
    file_content = ""
    expected_output = {}
    extractor = ExtractImportsFromFile()
    result = extractor._extract_imports(file_content)
    assert result == expected_output

def test_single_alias():
    file_content = """
    from math import sin as sinn
    """
    expected_output = {
        'sinn': "from math import sin"
    }
    extractor = ExtractImportsFromFile()
    result = extractor._extract_imports(file_content)
    assert result == expected_output