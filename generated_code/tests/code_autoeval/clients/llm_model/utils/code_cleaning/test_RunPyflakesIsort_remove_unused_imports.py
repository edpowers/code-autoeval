from typing import List


class RunPyflakesIsort:
    def __init__(self, data):
        self.data = data

    async def remove_unused_imports(self, code: str, unused_imports: List[str]) -> str:
        lines = code.splitlines()
        new_lines = []

        for line in lines:
            if not any(f"import {imp}" in line for imp in unused_imports):
                new_lines.append(line)

        return "\n".join(new_lines)

from unittest.mock import patch

import pytest

from code_autoeval.llm_model.utils.code_cleaning.run_pyflakes_isort import \
    RunPyflakesIsort


@pytest.fixture
def run_pyflakes_isort():
    return RunPyflakesIsort(None)

def test_remove_unused_imports_normal(run_pyflakes_isort):
    code = "import os\nimport sys\nprint('Hello, World!')"
    unused_imports = ["os"]
    expected_output = "import sys\nprint('Hello, World!')"
    result = run_pyflakes_isort.remove_unused_imports(code, unused_imports)
    assert result == expected_output

def test_remove_unused_imports_no_unused(run_pyflakes_isort):
    code = "import os\nprint('Hello, World!')"
    unused_imports = ["sys"]
    expected_output = "import os\nprint('Hello, World!')"
    result = run_pyflakes_isort.remove_unused_imports(code, unused_imports)
    assert result == expected_output

def test_remove_unused_imports_empty_unused(run_pyflakes_isort):
    code = "import os\nprint('Hello, World!')"
    unused_imports = []
    expected_output = "import os\nprint('Hello, World!')"
    result = run_pyflakes_isort.remove_unused_imports(code, unused_imports)
    assert result == expected_output

def test_remove_unused_imports_no_matches(run_pyflakes_isort):
    code = "print('Hello, World!')"
    unused_imports = ["os", "sys"]
    expected_output = "print('Hello, World!')"
    result = run_pyflakes_isort.remove_unused_imports(code, unused_imports)
    assert result == expected_output

def test_remove_unused_imports_multiple_lines(run_pyflakes_isort):
    code = "import os\nimport sys\nprint('Hello, World!')"
    unused_imports = ["os", "sys"]
    expected_output = ""
    result = run_pyflakes_isort.remove_unused_imports(code, unused_imports)
    assert result == expected_output    expected_output = ""
    result = run_pyflakes_isort.remove_unused_imports(code, unused_imports)
    assert result == expected_output