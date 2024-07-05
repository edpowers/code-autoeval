import os
import re
from unittest.mock import MagicMock, patch

import pytest


class FilePathFunctions:
    def __init__(self):
        pass

    @staticmethod
    def find_function_file(func_name, base_dir):
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                if file.endswith('.py') and func_name in open(os.path.join(root, file)).read():
                    return os.path.join(root, file)
        return None

    @staticmethod
    def update_import_statement(self, code: str, func_name: str, base_dir: str, debug: bool = False) -> str:
        if not (file_path := self.find_function_file(func_name, base_dir)):
            raise FileNotFoundError(f"Function {func_name} not found in {base_dir}")

        module_name = os.path.splitext(file_path)[0]
        new_import = f"from {module_name} import {func_name}"

        if debug:
            print(f"Updating import statement to: {new_import}")

        return re.sub(r"from.*import.*{func_name}", new_import, code)

# Updated implementation of the FilePathFunctions.update_import_statement function.

@pytest.fixture
def file_path_functions():
    return FilePathFunctions()

@patch("code_autoeval.clients.llm_model.utils.file_path_functions.FilePathFunctions.find_function_file", return_value="mocked_file_path")
def test_update_import_statement_normal(mock_find_function_file, file_path_functions):
    code = "from some_module import some_func"
    func_name = "some_func"
    base_dir = "."
    debug = False
    expected_output = "from mocked_file_path import some_func"
    
    result = file_path_functions.update_import_statement(self=None, code=code, func_name=func_name, base_dir=base_dir, debug=debug)
    
    assert result == expected_output

def test_update_import_statement_not_found(file_path_functions):
    code = "from some_module import some_func"
    func_name = "nonexistent_func"
    base_dir = "."
    debug = False
    
    with pytest.raises(FileNotFoundError):
        file_path_functions.update_import_statement(self=None, code=code, func_name=func_name, base_dir=base_dir, debug=debug)

def test_update_import_statement_empty_code(file_path_functions):
    code = ""
    func_name = "some_func"
    base_dir = "."
    debug = False
    
    result = file_path_functions.update_import_statement(self=None, code=code, func_name=func_name, base_dir=base_dir, debug=debug)
    
    assert result == f"from mocked_file_path import {func_name}"

def test_update_import_statement_empty_func_name(file_path_functions):
    code = "from some_module import some_func"
    func_name = ""
    base_dir = "."
    debug = False
    
    with pytest.raises(FileNotFoundError):
        file_path_functions.update_import_statement(self=None, code=code, func_name=func_name, base_dir=base_dir, debug=debug)

def test_update_import_statement_empty_base_dir(file_path_functions):
    code = "from some_module import some_func"
    func_name = "some_func"
    base_dir = ""
    debug = False
    
    with pytest.raises(FileNotFoundError):
        file_path_functions.update_import_statement(self=None, code=code, func_name=func_name, base_dir=base_dir, debug=debug)