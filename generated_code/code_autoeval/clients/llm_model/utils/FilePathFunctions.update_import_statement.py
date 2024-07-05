import os
import re
from unittest.mock import MagicMock, patch

import pytest


class FilePathFunctions:
    def __init__(self, data):
        self.data = data

    def find_function_file(self, func_name, base_dir):
        # Mock implementation for testing purposes
        return os.path.join(base_dir, f"{func_name}.py")

    def update_import_statement(self, code: str, func_name: str, base_dir: str, debug: bool = False) -> str:
        if not (file_path := self.find_function_file(func_name, base_dir)):
            raise FileNotFoundError(f"Function {func_name} not found in {base_dir}")

        module_name = os.path.splitext(file_path)[0]
        new_import = f"from {module_name} import {func_name}"

        if debug:
            print(f"Updating import statement to: {new_import}")

        return re.sub(f"from.*import.*{func_name}", new_import, code)

# Analysis of the function:
# The function `update_import_statement` is designed to update the import statement in a given code snippet to point to a specific function located in a specified directory. It first finds the file containing the function and then constructs a new import statement based on that information. If debugging is enabled, it prints out the updated import statement before applying it to the code.

##################################################
# TESTS
##################################################

@pytest.fixture
def setup_filepathfunctions():
    return FilePathFunctions(None)

@patch("code_autoeval.llm_model.utils.file_path_functions.FilePathFunctions.find_function_file", return_value="test_dir/test_func.py")
def test_update_import_statement_normal(mock_find_function_file, setup_filepathfunctions):
    code = "from some_module import another_func"
    func_name = "another_func"
    base_dir = "test_dir"
    result = setup_filepathfunctions.update_import_statement(code, func_name, base_dir)
    assert result == "from test_dir.test_func import another_func"

@pytest.mark.parametrize("debug", [True, False])
def test_update_import_statement_debug(setup_filepathfunctions, debug):
    code = "from some_module import another_func"
    func_name = "another_func"
    base_dir = "test_dir"
    with patch('builtins.print') as mock_print:
        result = setup_filepathfunctions.update_import_statement(code, func_name, base_dir, debug)
        if debug:
            mock_print.assert_called_once_with("Updating import statement to: from test_dir.test_func import another_func")
        else:
            mock_print.assert_not_called()
        assert result == "from test_dir.test_func import another_func"

def test_update_import_statement_file_not_found(setup_filepathfunctions):
    code = "from some_module import another_func"
    func_name = "non_existent_func"
    base_dir = "nonexistent_dir"
    with pytest.raises(FileNotFoundError):
        setup_filepathfunctions.update_import_statement(code, func_name, base_dir)    with pytest.raises(FileNotFoundError):
        setup_filepathfunctions.update_import_statement(code, func_name, base_dir)