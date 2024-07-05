from unittest.mock import patch

import pytest


@patch("code_autoeval.clients.llm_model.utils.code_cleaning.run_pyflakes_isort.RunPyflakesIsort.__init__", return_value=None)
def test_remove_unused_imports_normal(mock_init):
    code = """
import os
import sys
import math

print("Hello, World!")
"""
    unused_imports = ["os", "math"]
    expected_output = """
print("Hello, World!")
"""
    from code_autoeval.clients.llm_model.utils.code_cleaning.run_pyflakes_isort import RunPyflakesIsort
    run_pyflakes_isort = RunPyflakesIsort()
    result = run_pyflakes_isort.remove_unused_imports(code, unused_imports)
    assert result == expected_output.strip()

def test_remove_unused_imports_no_unused():
    code = """
import os
import sys

print("Hello, World!")
"""
    unused_imports = ["math"]
    expected_output = """
import os
import sys

print("Hello, World!")
"""
    from code_autoeval.clients.llm_model.utils.code_cleaning.run_pyflakes_isort import RunPyflakesIsort
    run_pyflakes_isort = RunPyflakesIsort()
    result = run_pyflakes_isort.remove_unused_imports(code, unused_imports)
    assert result == expected_output.strip()

def test_remove_unused_imports_empty_unused():
    code = """
import os
import sys

print("Hello, World!")
"""
    unused_imports = []
    expected_output = """
import os
import sys

print("Hello, World!")
"""
    from code_autoeval.clients.llm_model.utils.code_cleaning.run_pyflakes_isort import RunPyflakesIsort
    run_pyflakes_isort = RunPyflakesIsort()
    result = run_pyflakes_isort.remove_unused_imports(code, unused_imports)
    assert result == expected_output.strip()

def test_remove_unused_imports_empty_code():
    code = ""
    unused_imports = ["os"]
    expected_output = ""
    from code_autoeval.clients.llm_model.utils.code_cleaning.run_pyflakes_isort import RunPyflakesIsort
    run_pyflakes_isort = RunPyflakesIsort()
    result = run_pyflakes_isort.remove_unused_imports(code, unused_imports)
    assert result == expected_output.strip()

def test_remove_unused_imports_no_imports():
    code = """
print("Hello, World!")
"""
    unused_imports = ["os"]
    expected_output = """
print("Hello, World!")
"""
    from code_autoeval.clients.llm_model.utils.code_cleaning.run_pyflakes_isort import RunPyflakesIsort
    run_pyflakes_isort = RunPyflakesIsort()
    result = run_pyflakes_isort.remove_unused_imports(code, unused_imports)
    assert result == expected_output.strip()