import pathlib
from unittest.mock import MagicMock, patch

import pytest
from code_autoeval.clients.llm_model.utils.model.function_attributes import FunctionAttributesFactory

# Analysis of the function _construct_file_paths:
# The function constructs file paths for test files based on a given function name and module relative path.
# It ensures that directories exist before returning the constructed file paths.

def test_normal_case():
    func_name = "example_function"
    module_relative_path = pathlib.Path("module/submodule")
    generated_base_dir = pathlib.Path("/generated/base/dir")
    
    with patch('code_autoeval.clients.llm_model.utils.model.function_attributes.SystemUtils.make_file_dir') as mock_make_file_dir:
        result = FunctionAttributesFactory._construct_file_paths(func_name, module_relative_path, generated_base_dir)
        
        expected_test_relative_path = pathlib.Path("tests") / module_relative_path.parent / f"test_{func_name}.py"
        expected_test_absolute_path = generated_base_dir / expected_test_relative_path
        
        assert result == (expected_test_relative_path, expected_test_absolute_path)
        mock_make_file_dir.assert_called_once_with(expected_test_absolute_path)

def test_edge_case_dot_in_func_name():
    func_name = "example.function"
    module_relative_path = pathlib.Path("module/submodule")
    generated_base_dir = pathlib.Path("/generated/base/dir")
    
    with patch('code_autoeval.clients.llm_model.utils.model.function_attributes.SystemUtils.make_file_dir') as mock_make_file_dir:
        result = FunctionAttributesFactory._construct_file_paths(func_name, module_relative_path, generated_base_dir)
        
        expected_test_relative_path = pathlib.Path("tests") / module_relative_path.parent / f"test_example_function.py"
        expected_test_absolute_path = generated_base_dir / expected_test_relative_path
        
        assert result == (expected_test_relative_path, expected_test_absolute_path)
        mock_make_file_dir.assert_called_once_with(expected_test_absolute_path)

def test_error_condition():
    func_name = "example_function"
    module_relative_path = pathlib.Path("module/submodule")
    generated_base_dir = pathlib.Path("/generated/base/dir")
    
    with patch('code_autoeval.clients.llm_model.utils.model.function_attributes.SystemUtils.make_file_dir') as mock_make_file_dir:
        result = FunctionAttributesFactory._construct_file_paths(func_name, module_relative_path, generated_base_dir)
        
        expected_test_relative_path = pathlib.Path("tests") / module_relative_path.parent / f"test_{func_name}.py"
        expected_test_absolute_path = generated_base_dir / expected_test_relative_path
        
        assert result == (expected_test_relative_path, expected_test_absolute_path)
        mock_make_file_dir.assert_called_once_with(expected_test_absolute_path)