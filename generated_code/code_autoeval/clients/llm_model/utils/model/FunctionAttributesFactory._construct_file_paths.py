import pathlib
from unittest.mock import MagicMock, patch

import pytest

from code_autoeval.llm_model.utils.model.function_attributes import \
    FunctionAttributesFactory

# Analysis of the function:
# The function constructs file paths for test files based on a given function name and module relative path.
# It ensures that directories exist before returning the constructed file paths.

def test_construct_file_paths_normal():
    func_name = "test_function"
    module_relative_path = pathlib.Path("module/submodule")
    generated_base_dir = pathlib.Path("/generated/base/dir")

    with patch('code_autoeval.llm_model.utils.model.function_attributes.SystemUtils.make_file_dir') as mock_make_file_dir:
        result = FunctionAttributesFactory._construct_file_paths(func_name, module_relative_path, generated_base_dir)

        assert isinstance(result, tuple) and len(result) == 2
        test_relative_file_path, test_absolute_file_path = result
        assert isinstance(test_relative_file_path, pathlib.Path)
        assert isinstance(test_absolute_file_path, pathlib.Path)

        expected_relative_path = pathlib.Path("tests") / module_relative_path.parent / f"test_{func_name}.py"
        expected_absolute_path = generated_base_dir / expected_relative_path
        assert test_relative_file_path == expected_relative_path
        assert test_absolute_file_path == expected_absolute_path

        mock_make_file_dir.assert_called_once_with(test_absolute_file_path)

def test_construct_file_paths_dots_in_func_name():
    func_name = "test.function"
    module_relative_path = pathlib.Path("module/submodule")
    generated_base_dir = pathlib.Path("/generated/base/dir")

    with patch('code_autoeval.llm_model.utils.model.function_attributes.SystemUtils.make_file_dir') as mock_make_file_dir:
        result = FunctionAttributesFactory._construct_file_paths(func_name, module_relative_path, generated_base_dir)

        assert isinstance(result, tuple) and len(result) == 2
        test_relative_file_path, test_absolute_file_path = result
        assert "test_function" in str(test_relative_file_path.stem)
        assert "test_function" in str(test_absolute_file_path.stem)

        mock_make_file_dir.assert_called_once_with(test_absolute_file_path)

def test_construct_file_paths_empty_func_name():
    func_name = ""
    module_relative_path = pathlib.Path("module/submodule")
    generated_base_dir = pathlib.Path("/generated/base/dir")

    with patch('code_autoeval.llm_model.utils.model.function_attributes.SystemUtils.make_file_dir') as mock_make_file_dir:
        result = FunctionAttributesFactory._construct_file_paths(func_name, module_relative_path, generated_base_dir)

        assert isinstance(result, tuple) and len(result) == 2
        test_relative_file_path, test_absolute_file_path = result
        assert "test_" in str(test_relative_file_path.name)
        assert "test_" in str(test_absolute_file_path.name)

        mock_make_file_dir.assert_called_once_with(test_absolute_file_path)

def test_construct_file_paths_invalid_module_relative_path():
    func_name = "test_function"
    module_relative_path = None  # Invalid path
    generated_base_dir = pathlib.Path("/generated/base/dir")

    with patch('code_autoeval.llm_model.utils.model.function_attributes.SystemUtils.make_file_dir') as mock_make_file_dir:
        result = FunctionAttributesFactory._construct_file_paths(func_name, module_relative_path, generated_base_dir)

        assert isinstance(result, tuple) and len(result) == 2
        test_relative_file_path, test_absolute_file_path = result
        assert "test_" in str(test_relative_file_path.name)
        assert "test_" in str(test_absolute_file_path.name)

        mock_make_file_dir.assert_called_once_with(test_absolute_file_path)

def test_construct_file_paths_invalid_generated_base_dir():
    func_name = "test_function"
    module_relative_path = pathlib.Path("module/submodule")
    generated_base_dir = None  # Invalid path

    with patch('code_autoeval.llm_model.utils.model.function_attributes.SystemUtils.make_file_dir') as mock_make_file_dir:
        result = FunctionAttributesFactory._construct_file_paths(func_name, module_relative_path, generated_base_dir)

        assert isinstance(result, tuple) and len(result) == 2
        test_relative_file_path, test_absolute_file_path = result
        assert "test_" in str(test_relative_file_path.name)
        assert "test_" in str(test_absolute_file_path.name)

        mock_make_file_dir.assert_called_once_with(test_absolute_file_path)        assert "test_" in str(test_relative_file_path.name)
        assert "test_" in str(test_absolute_file_path.name)

        mock_make_file_dir.assert_called_once_with(test_absolute_file_path)