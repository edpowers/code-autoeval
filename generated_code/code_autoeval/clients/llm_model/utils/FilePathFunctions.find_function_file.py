import os
import ast
from unittest.mock import patch, MagicMock
import pytest

class FilePathFunctions:
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

# Analysis of the function:
# The function walks through all files in a directory and its subdirectories to find a Python file containing a function with the specified name.
# It returns the relative path from the base_dir to the file where the function is found, formatted as a module path.
# If no such function is found, it returns None.

##################################################
# TESTS
##################################################

@pytest.fixture(autouse=True)
def mock_os_walk():
    with patch("os.walk", return_value=[("/mock/path", ["dir1"], ["file1.py"])]):
        yield

@patch("ast.parse")
@patch("builtins.open", new_callable=MagicMock)
def test_find_function_file_found(mock_open, mock_ast_parse):
    # Arrange
    func_name = "example_func"
    base_dir = "/mock/path"
    expected_output = "file1.py"
    mock_open.return_value.__enter__.return_value.read.return_value = "content"
    mock_ast_parse.return_value = MagicMock()
    mock_ast_parse.return_value.body = [MagicMock(name=func_name, body=[MagicMock()])]
    
    # Act
    result = FilePathFunctions().find_function_file(func_name, base_dir)
    
    # Assert
    assert result == expected_output

def test_find_function_file_not_found():
    # Arrange
    func_name = "non_existent_func"
    base_dir = "/mock/path"
    
    # Act
    result = FilePathFunctions().find_function_file(func_name, base_dir)
    
    # Assert
    assert result is None

@patch("ast.parse")
@patch("builtins.open", new_callable=MagicMock)
def test_find_function_file_multiple_files(mock_open, mock_ast_parse):
    # Arrange
    func_name = "example_func"
    base_dir = "/mock/path"
    expected_output = "file1.py"
    mock_open.return_value.__enter__.return_value.read.return_value = "content"
    mock_ast_parse.return_value = MagicMock()
    mock_ast_parse.return_value.body = [MagicMock(name=func_name, body=[MagicMock()])]
    
    # Act
    result = FilePathFunctions().find_function_file(func_name, base_dir)
    
    # Assert
    assert result == expected_output

@patch("ast.parse")
@patch("builtins.open", new_callable=MagicMock)
def test_find_function_file_with_subdirs(mock_open, mock_ast_parse):
    # Arrange
    func_name = "example_func"
    base_dir = "/mock/path"
    expected_output = "dir1.file1.py"
    mock_open.return_value.__enter__.return_value.read.return_value = "content"
    mock_ast_parse.return_value = MagicMock()
    mock_ast_parse.return_value.body = [MagicMock(name=func_name, body=[MagicMock()])]
    
    # Act
    result = FilePathFunctions().find_function_file(func_name, base_dir)
    
    # Assert
    assert result == expected_output

@patch("ast.parse")
@patch("builtins.open", new_callable=MagicMock)
def test_find_function_file_with_non_python_files(mock_open, mock_ast_parse):
    # Arrange
    func_name = "example_func"
    base_dir = "/mock/path"
    expected_output = None
    mock_open.return_value.__enter__.return_value.read.return_value = "content"
    mock_ast_parse.return_value = MagicMock()
    mock_ast_parse.return_value.body = [MagicMock(name=func_name, body=[MagicMock()])]
    
    # Act
    result = FilePathFunctions().find_function_file(func_name, base_dir)
    
    # Assert
    assert result == expected_output