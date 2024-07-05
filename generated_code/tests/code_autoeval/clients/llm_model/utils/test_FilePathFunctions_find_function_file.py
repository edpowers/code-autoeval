import ast
import os
from unittest.mock import MagicMock, patch

import pytest


class FilePathFunctions:
    @staticmethod
    def find_function_file(self, func_name: str, base_dir: str) -> str:
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    with open(file_path, "r") as f:
                        tree = ast.parse(f.read())
                    for node in ast.walk(tree):
                        if isinstance(node, ast.FunctionDef) and node.name == func_name:
                            return (
                                file_path.replace(base_dir, "")
                                .strip(os.path.sep)
                                .replace(os.path.sep, ".")
                            )
        return None

# Mocking the dependencies as per instructions
@patch("code_autoeval.clients.llm_model.utils.file_path_functions.FilePathFunctions.__init__", return_value=None)
def test_find_function_file_normal():
    # Arrange
    func_name = "example_func"
    base_dir = "/mocked/base/directory"
    mock_filepath = "/mocked/base/directory/module.py"
    
    with patch("os.walk", return_value=[[(mock_filepath, [], ["module.py"])]]):
        with patch("ast.parse"):
            with patch("ast.FunctionDef"):
                file_path_functions = FilePathFunctions()
                # Act
                result = file_path_functions.find_function_file(func_name, base_dir)
                # Assert
                assert result == "module"

def test_find_function_file_nonexistent():
    # Arrange
    func_name = "example_func"
    base_dir = "/mocked/base/directory"
    
    with patch("os.walk", return_value=[("", [], [])]):
        file_path_functions = FilePathFunctions()
        # Act
        result = file_path_functions.find_function_file(func_name, base_dir)
        # Assert
        assert result is None

def test_find_function_file_no_python_files():
    # Arrange
    func_name = "example_func"
    base_dir = "/mocked/base/directory"
    
    with patch("os.walk", return_value=[("", [], ["non_py_file"])]):
        file_path_functions = FilePathFunctions()
        # Act
        result = file_path_functions.find_function_file(func_name, base_dir)
        # Assert
        assert result is None

def test_find_function_file_no_matching_function():
    # Arrange
    func_name = "example_func"
    base_dir = "/mocked/base/directory"
    mock_filepath = "/mocked/base/directory/module.py"
    
    with patch("os.walk", return_value=[[(mock_filepath, [], ["module.py"])]]):
        with patch("ast.parse"):
            file_path_functions = FilePathFunctions()
            # Act
            result = file_path_functions.find_function_file(func_name, base_dir)
            # Assert
            assert result is None

def test_find_function_file_multiple_files():
    # Arrange
    func_name = "example_func"
    base_dir = "/mocked/base/directory"
    mock_filepath1 = "/mocked/base/directory/module1.py"
    mock_filepath2 = "/mocked/base/directory/module2.py"
    
    with patch("os.walk", return_value=[[(mock_filepath1, [], ["module1.py"]), (mock_filepath2, [], ["module2.py"])]]):
        with patch("ast.parse"):
            file_path_functions = FilePathFunctions()
            # Act
            result = file_path_functions.find_function_file(func_name, base_dir)
            # Assert
            assert result == "module1" or result == "module2"  # Assuming one of the modules contains the function