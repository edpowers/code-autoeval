import ast
from typing import Dict


class ExtractImportsFromFile:
    def __init__(self, *args, **kwargs):
        pass

    def _extract_imports(self, file_content: str) -> Dict[str, str]:
        tree = ast.parse(file_content)

        imports = {}

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports[alias.name] = f"import {alias.name}"
            elif isinstance(node, ast.ImportFrom):
                module = node.module
                names = [alias.name for alias in node.names]
                if len(names) == 1:
                    imports[names[0]] = f"from {module} import {names[0]}"
                else:
                    imports[tuple(names)] = f"from {module} import ({', '.join(names)})"

        return imports

from unittest.mock import patch

import pytest

from code_autoeval.llm_model.utils.extraction.extract_imports_from_file import \
    ExtractImportsFromFile


@pytest.fixture
def extract_imports():
    return ExtractImportsFromFile()

def test_normal_import(extract_imports):
    file_content = "import os\nimport sys"
    result = extract_imports._extract_imports(file_content)
    assert result == {'os': 'import os', 'sys': 'import sys'}

def test_from_import(extract_imports):
    file_content = "from math import sqrt\nfrom random import randint"
    result = extract_imports._extract_imports(file_content)
    assert result == {'sqrt': 'from math import sqrt', 'randint': 'from random import randint'}

def test_multiple_imports(extract_imports):
    file_content = "import os\nfrom math import sqrt, pi"
    result = extract_imports._extract_imports(file_content)
    assert result == {'os': 'import os', 'sqrt': 'from math import sqrt', 'pi': 'from math import pi'}

def test_error_invalid_syntax(extract_imports):
    file_content = "import os\n from math import sqrt"  # Invalid syntax due to extra space
    with pytest.raises(SyntaxError):
        extract_imports._extract_imports(file_content)

def test_empty_content(extract_imports):
    file_content = ""
    result = extract_imports._extract_imports(file_content)
    assert result == {}    file_content = ""
    result = extract_imports._extract_imports(file_content)
    assert result == {}