# Analysis of the Function:
# The function `add_class_import` is designed to add an import statement for a given class if it's not already present in the provided code. It handles splitting the code into lines, checking for existing imports, and inserting new import statements as needed. This function is crucial for maintaining correct module dependencies within larger codebases.

import re
from unittest.mock import patch

# Pytest Tests:
import pytest
from code_autoeval.clients.llm_model.utils.code_cleaning.run_pyflakes_isort import RunPyflakesIsort
from code_autoeval.clients.llm_model.utils.data_models import ClassDataModel


@pytest.fixture
def run_pyflakes_isort():
    return RunPyflakesIsort()

@pytest.fixture
def class_model():
    return ClassDataModel(absolute_path="module.Class", class_name="Class")

def test_add_class_import_normal(run_pyflakes_isort, class_model):
    code = "existing_code\nanother_line"
    expected_code = "from module import Class\nexisting_code\nanother_line"
    result, modified = run_pyflakes_isort.add_class_import(code, class_model)
    assert result == expected_code
    assert modified is True

def test_add_class_import_already_exists(run_pyflakes_isort, class_model):
    code = "from module import Class\nanother_line"
    expected_code = "from module import Class\nanother_line"
    result, modified = run_pyflakes_isort.add_class_import(code, class_model)
    assert result == expected_code
    assert modified is False

def test_add_class_import_empty_code(run_pyflakes_isort, class_model):
    code = ""
    expected_code = "from module import Class"
    result, modified = run_pyflakes_isort.add_class_import(code, class_model)
    assert result == expected_code
    assert modified is True

def test_add_class_import_no_module_path(run_pyflakes_isort, class_model):
    class_model = ClassDataModel(absolute_path="Class", class_name="Class")
    code = "existing_code\nanother_line"
    expected_code = "from . import Class\nexisting_code\nanother_line"
    result, modified = run_pyflakes_isort.add_class_import(code, class_model)
    assert result == expected_code
    assert modified is True

def test_add_class_import_multiple_imports(run_pyflakes_isort, class_model):
    code = "from othermodule import OtherClass\nexisting_code\nanother_line"
    expected_code = "from othermodule import OtherClass\nfrom module import Class\nexisting_code\nanother_line"
    result, modified = run_pyflakes_isort.add_class_import(code, class_model)
    assert result == expected_code
    assert modified is True